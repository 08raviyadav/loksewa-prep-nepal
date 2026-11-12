/// Home cards for the Daily Challenge and the Question of the Day
/// (v1.0.4). Both listen to the ProgressStore (a ChangeNotifier), so the
/// "done today" state updates the moment the quiz finishes — no manual
/// refresh needed.
library;

import 'package:flutter/material.dart';

import '../data/data_repository.dart';
import '../gamification/analytics.dart';
import '../gamification/daily.dart';
import '../l10n/dashboard_strings.dart';
import '../l10n/v104_strings.dart';
import '../models/models.dart';
import '../state/progress_store.dart';
import '../theme/app_theme.dart';
import 'app_scaffold.dart';

/// Daily Challenge card: 10 seeded questions, same set for everyone.
/// Shows a "done today" chip once today's challenge is finished.
class DailyChallengeCard extends StatefulWidget {
  final VoidCallback onStart;
  const DailyChallengeCard({super.key, required this.onStart});

  @override
  State<DailyChallengeCard> createState() => _DailyChallengeCardState();
}

class _DailyChallengeCardState extends State<DailyChallengeCard> {
  ProgressStore? _store;

  @override
  void initState() {
    super.initState();
    ProgressStore.instance.then((s) {
      if (mounted) setState(() => _store = s);
    });
  }

  @override
  Widget build(BuildContext context) {
    final store = _store;
    if (store == null) return _card(context, done: false);
    return AnimatedBuilder(
      animation: store,
      builder: (context, _) =>
          _card(context, done: store.isDailyDone(dailySeed())),
    );
  }

  Widget _card(BuildContext context, {required bool done}) {
    final s = AppStateScope.of(context).strings;
    return Card(
      margin: const EdgeInsets.symmetric(
        horizontal: AppSpacing.s4,
        vertical: AppSpacing.s2,
      ),
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s5),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(s.dashDailyTitle, style: AppType.h3),
                ),
                if (done)
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 4,
                    ),
                    decoration: const BoxDecoration(
                      color: AppColors.greenSoft,
                      borderRadius: BorderRadius.all(AppRadius.pill),
                    ),
                    child: Text(
                      s.dailyDoneLabel,
                      style: AppType.small.copyWith(
                        color: AppColors.green,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: AppSpacing.s2),
            Text(s.dailyCardBody, style: AppType.body),
            const SizedBox(height: AppSpacing.s3),
            FilledButton.icon(
              onPressed: widget.onStart,
              icon: const Icon(Icons.calendar_today_outlined),
              label: Text(done ? s.dailyRepeatYes : s.dailyStart),
              style: FilledButton.styleFrom(
                backgroundColor: AppColors.accent,
                foregroundColor: AppColors.accentInk,
                minimumSize: const Size(0, AppSpacing.minTap),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// Question of the Day card: one deterministic question, fresh every day.
/// Tapping Answer opens it as a 1-question quiz.
class QuestionOfTheDayCard extends StatefulWidget {
  final void Function(Question question) onAnswer;

  /// Test seam: replaces the asset load.
  final Future<Question?> Function()? loadQuestion;

  const QuestionOfTheDayCard({
    super.key,
    required this.onAnswer,
    this.loadQuestion,
  });

  @override
  State<QuestionOfTheDayCard> createState() => _QuestionOfTheDayCardState();
}

class _QuestionOfTheDayCardState extends State<QuestionOfTheDayCard> {
  late final Future<Question?> _future;
  ProgressStore? _store;

  @override
  void initState() {
    super.initState();
    _future = widget.loadQuestion?.call() ??
        loadQuestionOfTheDay(DataRepository());
    ProgressStore.instance.then((s) {
      if (mounted) setState(() => _store = s);
    });
  }

  @override
  Widget build(BuildContext context) {
    final store = _store;
    if (store == null) return _card(context, done: false);
    return AnimatedBuilder(
      animation: store,
      builder: (context, _) =>
          _card(context, done: store.isQotdDone(dailySeed())),
    );
  }

  Widget _card(BuildContext context, {required bool done}) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;
    return Card(
      margin: const EdgeInsets.symmetric(
        horizontal: AppSpacing.s4,
        vertical: AppSpacing.s2,
      ),
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s5),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(child: Text(s.qotdTitle, style: AppType.h3)),
                if (done)
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 4,
                    ),
                    decoration: const BoxDecoration(
                      color: AppColors.greenSoft,
                      borderRadius: BorderRadius.all(AppRadius.pill),
                    ),
                    child: Text(
                      s.qotdDoneLabel,
                      style: AppType.small.copyWith(
                        color: AppColors.green,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: AppSpacing.s2),
            FutureBuilder<Question?>(
              future: _future,
              builder: (context, snap) {
                if (snap.connectionState != ConnectionState.done) {
                  return Text(s.qotdBody, style: AppType.body);
                }
                final q = snap.data;
                if (q == null) {
                  return Text(s.qotdBody, style: AppType.body);
                }
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      q.text(ne),
                      style: AppType.body.copyWith(
                        fontWeight: FontWeight.w600,
                      ),
                      maxLines: 3,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: AppSpacing.s3),
                    OutlinedButton.icon(
                      onPressed: () => widget.onAnswer(q),
                      icon: const Icon(Icons.lightbulb_outline),
                      label: Text(done ? s.qotdTryAgain : s.qotdAnswer),
                      style: OutlinedButton.styleFrom(
                        minimumSize: const Size(0, AppSpacing.minTap),
                      ),
                    ),
                  ],
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
