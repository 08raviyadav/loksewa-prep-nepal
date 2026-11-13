import 'package:flutter/material.dart';

import '../data/data_repository.dart';
import '../models/course.dart';
import '../models/history.dart';
import '../models/models.dart';
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

  @override
  void initState() {
    super.initState();
    _future = _load();
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
      body: FutureBuilder<_HomeData>(
        future: _future,
        builder: (context, snap) {
          if (!snap.hasData) {
            return const Center(
              child: Padding(
                padding: EdgeInsets.all(AppSpacing.s12),
                child: CircularProgressIndicator(color: AppColors.accent),
              ),
            );
          }
          final data = snap.data!;
          return ListView(
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
        color: AppColors.accentSoft,
        borderRadius: AppRadius.lgAll,
        border: Border.all(color: AppColors.accentLine),
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
              border: Border.all(color: AppColors.accent),
            ),
            child: Text(
              s.heroEyebrow,
              style: AppType.tiny.copyWith(
                color: AppColors.accent,
                fontWeight: FontWeight.w700,
                letterSpacing: 1.2,
              ),
            ),
          ),
          const SizedBox(height: AppSpacing.s4),
          Text(
            s.heroTitle,
            style: AppType.display.copyWith(color: AppColors.text),
          ),
          const SizedBox(height: AppSpacing.s3),
          Text(
            s.heroSubtitle,
            style: AppType.lead.copyWith(color: AppColors.muted),
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
                  backgroundColor: AppColors.accent,
                  foregroundColor: AppColors.accentInk,
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
                  side: const BorderSide(color: AppColors.accentLine),
                  foregroundColor: AppColors.accent,
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
        color: AppColors.card,
        borderRadius: AppRadius.mdAll,
        border: Border.all(color: AppColors.borderSoft),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(value, style: AppType.h1.copyWith(color: AppColors.accent)),
          Text(label, style: AppType.small.copyWith(color: AppColors.muted)),
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
        style: AppType.small.copyWith(color: AppColors.muted),
      ),
    );
  }
}
