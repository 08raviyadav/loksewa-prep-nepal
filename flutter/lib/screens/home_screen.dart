import 'dart:async';
import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../data/data_repository.dart';
import '../models/course.dart';
import '../models/history.dart';
import '../models/models.dart';
import '../onboarding/tour.dart';
import '../state/course_progress_store.dart';
import '../theme/app_theme.dart';
import '../widgets/app_scaffold.dart';
import '../widgets/countdown_card.dart';
import '../widgets/daily_cards.dart';
import '../widgets/history_otd_card.dart';
import '../widgets/reminder_banner.dart';
import 'courses/chapter_reader_screen.dart';

/// Home: hero, stat strip, reminder banner, next-exam countdown card.
class HomeScreen extends StatefulWidget {
  final int navIndex;
  final ValueChanged<int> onNav;
  final void Function(Exam exam) onPracticeExam;

  /// Course progress for the "Continue studying" card (null while loading).
  final CourseProgressStore? courseStore;
  final List<Course> courses;
  final OnResumeChapter? onResumeChapter;

  /// Daily Challenge + Question of the Day (v1.0.4). The cards render
  /// only when their callback is set.
  final VoidCallback? onDailyChallenge;
  final void Function(Question question)? onQuestionOfTheDay;

  const HomeScreen({
    super.key,
    required this.navIndex,
    required this.onNav,
    required this.onPracticeExam,
    this.courseStore,
    this.courses = const [],
    this.onResumeChapter,
    this.onDailyChallenge,
    this.onQuestionOfTheDay,
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late final Future<_HomeData> _future;

  // Tour (v1.0.7): on a small screen the Daily Challenge card can sit
  // just below the fold, so when the tour reaches step 1 this screen
  // scrolls the card into view (same pattern as PracticeScreen).
  final _scrollCtrl = ScrollController();
  TourController? _tour;
  int _scrollToken = 0;

  @override
  void initState() {
    super.initState();
    _future = _load();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final tour = TourScope.of(context);
    if (tour != _tour) {
      _tour?.removeListener(_onTourStep);
      _tour = tour;
      _tour?.addListener(_onTourStep);
    }
  }

  @override
  void dispose() {
    _tour?.removeListener(_onTourStep);
    _scrollCtrl.dispose();
    super.dispose();
  }

  void _onTourStep() {
    if (_tour?.currentStep?.id == 'daily') {
      _scrollIntoView(TourKeys.dailyChallenge, 'daily');
    }
  }

  /// Scrolls the tour target into view, retrying until it exists or
  /// the tour moves on. The list may not be built yet when the step
  /// becomes active (data still loading), so a fixed small retry count
  /// would give up too early — the step check bounds the loop instead.
  ///
  /// The scroll steps down one viewport at a time with [jumpTo]
  /// (synchronous — no animation future to await): jumping straight to
  /// the end can overshoot a mid-list target and leave it unbuilt above
  /// the viewport. Once the target exists, [Scrollable.ensureVisible]
  /// glides it into view (fire-and-forget — the overlay tracks the
  /// target's rect every frame, so the highlight follows the scroll).
  Future<void> _scrollIntoView(GlobalKey key, String stepId) async {
    final token = ++_scrollToken;
    for (var attempt = 0; attempt < 40; attempt++) {
      if (attempt > 0) {
        await Future<void>.delayed(const Duration(milliseconds: 100));
      }
      if (!mounted || token != _scrollToken) return;
      if (_tour?.currentStep?.id != stepId) return;
      final ctx = key.currentContext;
      if (ctx != null && ctx.mounted) {
        unawaited(
          Scrollable.ensureVisible(
            ctx,
            duration: const Duration(milliseconds: 300),
          ),
        );
        return;
      }
      // Not built yet (below the fold in the lazy list): step down so
      // the lazy builder creates the next chunk, then retry.
      if (_scrollCtrl.hasClients) {
        final pos = _scrollCtrl.position;
        final next = math.min(
          pos.pixels + pos.viewportDimension,
          pos.maxScrollExtent,
        );
        if (next == pos.pixels) return; // at the end; target can't exist
        _scrollCtrl.jumpTo(next);
      }
    }
  }

  Future<_HomeData> _load() async {
    final repo = DataRepository();
    final exams = await repo.exams();
    final dates = await repo.examDates();
    final history = await repo.historicalEvents();
    return (exams: exams, dates: dates, history: history);
  }

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    return AppScaffold(
      title: s.appName,
      currentIndex: widget.navIndex,
      onNav: widget.onNav,
      bottomNavKey: TourKeys.bottomNav,
      // Tour step 2 (v1.0.9): the language button lives in this
      // screen's app bar — only Home passes the key, so it never
      // duplicates across pushed pages.
      langToggleKey: TourKeys.langToggle,
      body: FutureBuilder<_HomeData>(
        future: _future,
        builder: (context, snap) {
          if (!snap.hasData) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(AppSpacing.s12),
                child: CircularProgressIndicator(color: AppColors.of(context).accent),
              ),
            );
          }
          final data = snap.data!;
          return ListView(
            controller: _scrollCtrl,
            children: [
              ReminderBanner(dates: data.dates),
              _Hero(
                questionCount: 64671, // full bank count; loader reads per-file
                examCount: data.exams.length,
                onStart: () => widget.onNav(1),
                onMock: () => widget.onNav(2),
              ),
              CountdownCard(
                dates: data.dates,
                onPractice: (d) {
                  final match =
                      data.exams.where((e) => e.id == d.exam).firstOrNull;
                  if (match != null) widget.onPracticeExam(match);
                },
              ),
              // Daily Challenge + Question of the Day (v1.0.4).
              if (widget.onDailyChallenge != null)
                DailyChallengeCard(onStart: widget.onDailyChallenge!),
              if (widget.onQuestionOfTheDay != null)
                QuestionOfTheDayCard(onAnswer: widget.onQuestionOfTheDay!),
              // Renders nothing on a quiet day (no event today).
              HistoryOtdCard(events: data.history),
              if (widget.courseStore != null && widget.onResumeChapter != null)
                Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: AppSpacing.s4,
                  ),
                  child: ContinueStudyingCard(
                    store: widget.courseStore!,
                    courses: widget.courses,
                    onResume: widget.onResumeChapter!,
                  ),
                ),
              _TrustRow(),
              const SizedBox(height: AppSpacing.s12),
            ],
          );
        },
      ),
    );
  }
}

typedef _HomeData = ({
  List<Exam> exams,
  List<ExamDate> dates,
  List<HistoricalEvent> history,
});

class _Hero extends StatelessWidget {
  final int questionCount;
  final int examCount;
  final VoidCallback onStart;
  final VoidCallback onMock;

  const _Hero({
    required this.questionCount,
    required this.examCount,
    required this.onStart,
    required this.onMock,
  });

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;
    String num(int n) => ne ? _neDigits(n.toString()) : n.toString();

    return Container(
      margin: const EdgeInsets.all(AppSpacing.s4),
      padding: const EdgeInsets.all(AppSpacing.s6),
      decoration: BoxDecoration(
        color: AppColors.of(context).accentSoft,
        borderRadius: AppRadius.lgAll,
        border: Border.all(color: AppColors.of(context).accentLine),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.s4,
              vertical: AppSpacing.s2,
            ),
            decoration: BoxDecoration(
              borderRadius: const BorderRadius.all(AppRadius.pill),
              border: Border.all(color: AppColors.of(context).accent),
            ),
            child: Text(
              s.heroEyebrow,
              style: AppType.tiny.copyWith(
                color: AppColors.of(context).accent,
                fontWeight: FontWeight.w700,
                letterSpacing: 1.2,
              ),
            ),
          ),
          const SizedBox(height: AppSpacing.s4),
          Text(
            s.heroTitle,
            style: AppType.display.copyWith(color: AppColors.of(context).text),
          ),
          const SizedBox(height: AppSpacing.s3),
          Text(
            s.heroSubtitle,
            style: AppType.lead.copyWith(color: AppColors.of(context).muted),
          ),
          const SizedBox(height: AppSpacing.s5),
          Wrap(
            spacing: AppSpacing.s3,
            runSpacing: AppSpacing.s3,
            children: [
              _StatCard(value: num(questionCount), label: s.questionsLabel),
              _StatCard(value: num(examCount), label: s.examsLabel),
              _StatCard(value: 'EN+NE', label: s.bilingualLabel),
              _StatCard(value: '0', label: s.noLoginLabel),
            ],
          ),
          const SizedBox(height: AppSpacing.s5),
          Wrap(
            spacing: AppSpacing.s3,
            runSpacing: AppSpacing.s3,
            children: [
              FilledButton(
                onPressed: onStart,
                style: FilledButton.styleFrom(
                  backgroundColor: AppColors.of(context).accent,
                  foregroundColor: AppColors.of(context).accentInk,
                  minimumSize: const Size(44, 52),
                  padding: const EdgeInsets.symmetric(
                    horizontal: AppSpacing.s6,
                  ),
                  textStyle: AppType.h3,
                ),
                child: Text(s.startPracticing),
              ),
              OutlinedButton(
                onPressed: onMock,
                style: OutlinedButton.styleFrom(
                  minimumSize: const Size(44, 52),
                  side: BorderSide(color: AppColors.of(context).accentLine),
                  foregroundColor: AppColors.of(context).accent,
                  textStyle: AppType.h3,
                ),
                child: Text(s.takeMock),
              ),
            ],
          ),
        ],
      ),
    );
  }

  String _neDigits(String s) => s.replaceAllMapped(
        RegExp(r'\d'),
        (m) => '०१२३४५६७८९'[int.parse(m.group(0)!)],
      );
}

class _StatCard extends StatelessWidget {
  final String value;
  final String label;
  const _StatCard({required this.value, required this.label});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 150,
      padding: const EdgeInsets.all(AppSpacing.s4),
      decoration: BoxDecoration(
        color: AppColors.of(context).card,
        borderRadius: AppRadius.mdAll,
        border: Border.all(color: AppColors.of(context).borderSoft),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(value, style: AppType.h1.copyWith(color: AppColors.of(context).accent)),
          Text(label, style: AppType.small.copyWith(color: AppColors.of(context).muted)),
        ],
      ),
    );
  }
}

class _TrustRow extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.s4),
      child: Text(
        s.trustRow,
        textAlign: TextAlign.center,
        style: AppType.small.copyWith(color: AppColors.of(context).muted),
      ),
    );
  }
}
