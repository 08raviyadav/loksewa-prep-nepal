/// My Mistakes (v1.0.4): every question answered wrong, grouped by exam,
/// with per-exam and all-mistakes retry. A question leaves the list the
/// moment it is answered correctly in a review run (QuizConfig
/// reviewMistakes) — wrong answers stay on the list.
///
/// Mistake ids are the vanilla `loksewa_progress_v1` `mistakes` list,
/// already recorded by ProgressStore.recordAttempt and QuizScreen at
/// answer time; this screen only resolves the ids to questions and
/// groups them. There is no id→file index, so the whole bank is loaded
/// once (cached by the repository afterwards, same as Daily Challenge).
library;

import 'package:flutter/material.dart';

import '../data/data_repository.dart';
import '../engine/quiz_engine.dart';
import '../l10n/v104_strings.dart';
import '../models/models.dart';
import '../state/progress_store.dart';
import '../theme/app_theme.dart';
import '../widgets/app_scaffold.dart';
import 'quiz/quiz_screen.dart';

/// One review session draws at most this many questions (shuffled).
const int kMistakesRetryCap = 20;

class MistakesScreen extends StatefulWidget {
  static const routeName = '/mistakes';
  final int navIndex;
  final ValueChanged<int> onNav;

  /// Test seams: replace the whole-bank / exams loads.
  final Future<List<Question>> Function()? loadQuestions;
  final Future<List<Exam>> Function()? loadExams;

  const MistakesScreen({
    super.key,
    required this.navIndex,
    required this.onNav,
    this.loadQuestions,
    this.loadExams,
  });

  @override
  State<MistakesScreen> createState() => _MistakesScreenState();
}

class _MistakesData {
  final Map<String, List<Question>> groups; // exam id -> questions
  final Map<String, Exam> examNames;
  final int total;
  const _MistakesData({
    required this.groups,
    required this.examNames,
    required this.total,
  });
}

class _MistakesScreenState extends State<MistakesScreen> {
  late Future<_MistakesData> _future;

  @override
  void initState() {
    super.initState();
    _future = _load();
  }

  Future<_MistakesData> _load() async {
    final store = await ProgressStore.instance;
    final ids = store.mistakes.toSet();
    final all =
        await (widget.loadQuestions ?? DataRepository().allQuestions)();
    final exams = await (widget.loadExams ?? DataRepository().exams)();
    final byId = {for (final q in all) q.id: q};
    final found = <Question>[];
    for (final id in ids) {
      final q = byId[id];
      if (q != null) found.add(q);
    }
    // Group by first exam tag (a question can be tagged for several
    // exams; it appears under its first one).
    final groups = <String, List<Question>>{};
    for (final q in found) {
      final key = q.exam.isEmpty ? '' : q.exam.first;
      (groups[key] ??= []).add(q);
    }
    return _MistakesData(
      groups: groups,
      examNames: {for (final e in exams) e.id: e},
      total: found.length,
    );
  }

  void _retry(List<Question> qs, String examName) {
    final picked = (qs.toList()..shuffle()).take(kMistakesRetryCap).toList();
    Navigator.of(context)
        .push(
      MaterialPageRoute(
        builder: (_) => QuizScreen(
          config: QuizConfig(
            questions: picked,
            negOn: true,
            negRate: 0.2,
            examId: '',
            reviewMistakes: true,
          ),
          meta: QuizMeta(
            examName: examName,
            cutoff: 45,
            cutoffPct: 45,
            fullTotal: 100,
          ),
          bank: qs,
        ),
      ),
    )
        .then((_) {
      // Returning from review refreshes the list (fixed mistakes
      // drop out).
      if (mounted) setState(() => _future = _load());
    });
  }

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;
    return AppScaffold(
      title: s.mistakesTitle,
      currentIndex: widget.navIndex,
      onNav: widget.onNav,
      body: FutureBuilder<_MistakesData>(
        future: _future,
        builder: (context, snap) {
          if (!snap.hasData) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(AppSpacing.s12),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const CircularProgressIndicator(
                      color: AppColors.accent,
                    ),
                    const SizedBox(height: AppSpacing.s4),
                    Text(s.mistakesLoading, style: AppType.body),
                  ],
                ),
              ),
            );
          }
          final data = snap.data!;
          if (data.total == 0) {
            return ListView(
              padding: const EdgeInsets.all(AppSpacing.s4),
              children: [
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(AppSpacing.s6),
                    child: Column(
                      children: [
                        const Icon(
                          Icons.check_circle_outline,
                          size: 64,
                          color: AppColors.green,
                        ),
                        const SizedBox(height: AppSpacing.s4),
                        Text(
                          s.mistakesEmptyTitle,
                          style: AppType.h2,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: AppSpacing.s2),
                        Text(
                          s.mistakesEmptyBody,
                          style: AppType.body,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: AppSpacing.s4),
                        FilledButton.icon(
                          onPressed: () => widget.onNav(1),
                          icon: const Icon(Icons.quiz_outlined),
                          label: Text(s.startPracticing),
                          style: FilledButton.styleFrom(
                            backgroundColor: AppColors.accent,
                            foregroundColor: AppColors.accentInk,
                            minimumSize: const Size(0, AppSpacing.minTap),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            );
          }
          final allQs = data.groups.values.expand((g) => g).toList();
          final sortedKeys = data.groups.keys.toList()
            ..sort(
              (a, b) => data.groups[b]!.length.compareTo(
                data.groups[a]!.length,
              ),
            );
          return ListView(
            padding: const EdgeInsets.all(AppSpacing.s4),
            children: [
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(AppSpacing.s5),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        s.mistakesCount(data.total),
                        style: AppType.h2,
                      ),
                      const SizedBox(height: AppSpacing.s3),
                      FilledButton.icon(
                        onPressed: () => _retry(allQs, s.mistakesReviewTitle),
                        icon: const Icon(Icons.refresh),
                        label: Text(
                          data.total > kMistakesRetryCap
                              ? s.mistakesRetrySample(kMistakesRetryCap)
                              : s.mistakesRetryAll,
                        ),
                        style: FilledButton.styleFrom(
                          backgroundColor: AppColors.accent,
                          foregroundColor: AppColors.accentInk,
                          minimumSize: const Size(0, AppSpacing.minTap),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: AppSpacing.s4),
              for (final key in sortedKeys)
                _ExamGroup(
                  title: key.isEmpty
                      ? s.mistakesReviewTitle
                      : (data.examNames[key]?.title(ne) ?? key),
                  questions: data.groups[key]!,
                  onRetry: () => _retry(
                    data.groups[key]!,
                    key.isEmpty
                        ? s.mistakesReviewTitle
                        : (data.examNames[key]?.title(ne) ?? key),
                  ),
                ),
              const SizedBox(height: AppSpacing.s8),
            ],
          );
        },
      ),
    );
  }
}

class _ExamGroup extends StatelessWidget {
  final String title;
  final List<Question> questions;
  final VoidCallback onRetry;

  const _ExamGroup({
    required this.title,
    required this.questions,
    required this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;
    return Card(
      margin: const EdgeInsets.only(bottom: AppSpacing.s4),
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s5),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(child: Text(title, style: AppType.h3)),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 4,
                  ),
                  decoration: const BoxDecoration(
                    color: AppColors.dangerSoft,
                    borderRadius: BorderRadius.all(AppRadius.pill),
                  ),
                  child: Text(
                    s.mistakesCount(questions.length),
                    style: AppType.small.copyWith(
                      color: AppColors.danger,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppSpacing.s3),
            OutlinedButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: Text(s.mistakesRetryExam(questions.length)),
              style: OutlinedButton.styleFrom(
                minimumSize: const Size(0, AppSpacing.minTap),
              ),
            ),
            const SizedBox(height: AppSpacing.s2),
            for (final q in questions)
              ExpansionTile(
                tilePadding: EdgeInsets.zero,
                title: Text(
                  q.text(ne),
                  style: AppType.body,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                subtitle: Text(q.topic, style: AppType.small),
                children: [
                  Padding(
                    padding: const EdgeInsets.only(bottom: AppSpacing.s3),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '${s.mistakesCorrectAnswer}: ${String.fromCharCode(65 + q.answer)}. ${q.opts(ne)[q.answer]}',
                          style: AppType.body.copyWith(
                            fontWeight: FontWeight.w700,
                            color: AppColors.green,
                          ),
                        ),
                        if (q.explain(ne).isNotEmpty) ...[
                          const SizedBox(height: AppSpacing.s2),
                          Text(q.explain(ne), style: AppType.small),
                        ],
                      ],
                    ),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }
}
