/// Result screen: score ring, pass/fail vs the exam cutoff percentage,
/// counts, time, XP/level/streak, encouraging copy (vanilla `renderResult`
/// tone), negative-marking line, topic breakdown, wrong-answer review, and
/// retry / weakest-topic / home actions.
library;

import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';

import '../../engine/quiz_engine.dart';
import '../../l10n/quiz_strings.dart';
import '../../models/models.dart';
import '../../state/progress_store.dart';
import '../../theme/app_theme.dart';
import '../../widgets/app_scaffold.dart';
import 'quiz_screen.dart';

class ResultScreen extends StatelessWidget {
  final QuizResult result;
  final QuizMeta meta;
  final QuizConfig config;
  final AttemptSummary summary;
  final List<Question> bank;
  final ProgressStore store;

  const ResultScreen({
    super.key,
    required this.result,
    required this.meta,
    required this.config,
    required this.summary,
    required this.bank,
    required this.store,
  });

  String _fmtTime(int s) {
    final m = s ~/ 60, r = s % 60;
    return '${m.toString().padLeft(2, '0')}:${r.toString().padLeft(2, '0')}';
  }

  void _retryWrong(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final qs = result.wrongList.map((w) => w.view.question).toList();
    if (qs.isEmpty) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(s.nothingToRetry)));
      return;
    }
    // Vanilla `retryWrong`: same questions reshuffled, no timer.
    final retry = QuizConfig(
      questions: qs,
      negOn: config.negOn,
      negRate: config.negRate,
      timerOn: false,
      mode: 'practice',
      examId: config.examId,
      reviewMistakes: config.reviewMistakes,
    );
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => QuizScreen(config: retry, meta: meta, bank: bank),
      ),
    );
  }

  void _practiceWeakest(BuildContext context, String topic) {
    final pool = bank.where((q) => q.topic == topic).toList()..shuffle();
    final qs = pool.take(10).toList();
    if (qs.isEmpty) return;
    final retry = QuizConfig(
      questions: qs,
      negOn: config.negOn,
      negRate: config.negRate,
      timerOn: false,
      mode: 'practice',
      examId: config.examId,
      reviewMistakes: config.reviewMistakes,
    );
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => QuizScreen(config: retry, meta: meta, bank: bank),
      ),
    );
  }

  /// Share the score + the app download link (v1.0.4).
  Future<void> _shareScore(BuildContext context) async {
    final s = AppStateScope.of(context).strings;
    final pctStr = result.pct == result.pct.roundToDouble()
        ? '${result.pct.toInt()}'
        : '${result.pct}';
    try {
      await SharePlus.instance.share(
        ShareParams(
          text: s.shareScoreText(
            _trimNum(result.score),
            '${result.max}',
            pctStr,
            meta.examName,
          ),
        ),
      );
    } catch (_) {
      // Share sheet failure: nothing useful to show, the user just taps
      // again (same convention as the drawer's share tile).
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;
    final r = result;
    final passed = summary.passed;
    final perQSecs =
        r.perQuestion.isEmpty ? 0 : (r.secs / r.perQuestion.length).round();

    // Vanilla sorts best/worst by correct ratio, top 3 each.
    final topics = r.byTopic.entries.toList();
    final best = List.of(topics)
      ..sort((a, b) => b.value.accuracy.compareTo(a.value.accuracy));
    final worst = List.of(topics)
      ..sort((a, b) => a.value.accuracy.compareTo(b.value.accuracy));
    final weakestTopic = worst.isEmpty ? null : worst.first.key;

    final firstMark =
        config.questions.isEmpty ? 1 : config.questions.first.marks;
    final negLine = !config.negOn
        ? s.negOffLine
        : s.negOnLine(
            (config.negRate * firstMark)
                .toStringAsFixed(2)
                .replaceAll(RegExp(r'0$'), ''),
            (config.negRate * 100).round(),
          );

    return Scaffold(
      appBar: AppBar(
        title: Text(config.mode == 'mock' ? s.mockMode : s.practiceMode),
        automaticallyImplyLeading: false,
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: AppSpacing.maxWidth),
          child: ListView(
            padding: const EdgeInsets.all(AppSpacing.s4),
            children: [
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(AppSpacing.s6),
                  child: Column(
                    children: [
                      Text(
                        '${config.mode == 'mock' ? s.mockMode : s.practiceMode} · ${meta.examName}${r.timedOut ? ' (${s.timeUpTitle})' : ''}',
                        style: AppType.small.copyWith(
                          color: Theme.of(context).hintColor,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.s4),
                      _ScoreRing(pct: r.pct, passed: passed),
                      const SizedBox(height: AppSpacing.s3),
                      Text(
                        '${_trimNum(r.score)} / ${r.max}',
                        style: AppType.h1.copyWith(
                          color: passed ? AppColors.green : AppColors.danger,
                        ),
                      ),
                      Text(
                        '${r.pct}%',
                        style: AppType.h3.copyWith(
                          color: Theme.of(context).hintColor,
                        ),
                      ),
                      const SizedBox(height: AppSpacing.s3),
                      Text(
                        passed ? s.passLabel : s.failLabel,
                        style: AppType.h2.copyWith(
                          color: passed ? AppColors.green : AppColors.danger,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.s2),
                      Text(
                        s.cutoffLine(
                          meta.cutoffPct,
                          meta.cutoff,
                          meta.fullTotal,
                          r.pct,
                        ),
                        style: AppType.small,
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.s4),
                      Wrap(
                        alignment: WrapAlignment.center,
                        spacing: AppSpacing.s3,
                        runSpacing: AppSpacing.s2,
                        children: [
                          _Stat('${s.correctCount} ${r.correct}'),
                          _Stat('${s.wrongCount} ${r.wrong}'),
                          _Stat('${s.skippedCount} ${r.skipped}'),
                          _Stat(
                            '${s.timeLabel} ${_fmtTime(r.secs)} (${s.perQuestionSecs(perQSecs)})',
                          ),
                          _Stat('+${summary.xp} ${s.xpLabel}'),
                          _Stat('${s.levelLabel} ${store.level}'),
                          _Stat(
                            '🔥 ${s.streakLabel} ${store.streak} ${s.daysLabel}',
                          ),
                        ],
                      ),
                      if (summary.leveledUp) ...[
                        const SizedBox(height: AppSpacing.s3),
                        _Banner(
                          text: '${s.levelUpBanner}${store.level}!',
                          gold: false,
                        ),
                      ],
                      if (summary.weeklyMet) ...[
                        const SizedBox(height: AppSpacing.s3),
                        _Banner(text: s.weeklyBanner, gold: true),
                      ],
                      const SizedBox(height: AppSpacing.s3),
                      Text(
                        passed ? s.passLine() : s.failLine(),
                        style: AppType.body.copyWith(
                          fontStyle: FontStyle.italic,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.s2),
                      Text(
                        negLine,
                        style: AppType.small.copyWith(
                          color: Theme.of(context).hintColor,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: AppSpacing.s4),
              Wrap(
                spacing: AppSpacing.s2,
                runSpacing: AppSpacing.s2,
                children: [
                  FilledButton.icon(
                    onPressed: () => _retryWrong(context),
                    icon: const Icon(Icons.refresh),
                    label: Text(s.retryWrong(r.wrongList.length)),
                    style: FilledButton.styleFrom(
                      backgroundColor: AppColors.accent,
                      foregroundColor: AppColors.accentInk,
                      minimumSize: const Size(0, AppSpacing.minTap),
                    ),
                  ),
                  if (weakestTopic != null)
                    OutlinedButton.icon(
                      onPressed: () => _practiceWeakest(context, weakestTopic),
                      icon: const Icon(Icons.menu_book_outlined),
                      label: Text(s.practiceWeakest(weakestTopic)),
                      style: OutlinedButton.styleFrom(
                        minimumSize: const Size(0, AppSpacing.minTap),
                      ),
                    ),
                  OutlinedButton.icon(
                    onPressed: () => _shareScore(context),
                    icon: const Icon(Icons.share_outlined),
                    label: Text(s.shareScoreTitle),
                    style: OutlinedButton.styleFrom(
                      minimumSize: const Size(0, AppSpacing.minTap),
                    ),
                  ),
                  OutlinedButton.icon(
                    onPressed: () => Navigator.of(context)
                        .popUntil((route) => route.isFirst),
                    icon: const Icon(Icons.home_outlined),
                    label: Text(s.backHome),
                    style: OutlinedButton.styleFrom(
                      minimumSize: const Size(0, AppSpacing.minTap),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: AppSpacing.s4),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(AppSpacing.s5),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(s.topicBreakdown, style: AppType.h3),
                      const SizedBox(height: AppSpacing.s2),
                      Text.rich(
                        TextSpan(
                          style: AppType.body,
                          children: [
                            TextSpan(
                              text: '${s.strongestLabel} ',
                              style: const TextStyle(
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                            TextSpan(
                              text: best
                                  .take(3)
                                  .map(
                                    (e) =>
                                        '${e.key} ${e.value.correct}/${e.value.total}',
                                  )
                                  .join(' · ')
                                  .ifEmpty('—'),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: AppSpacing.s2),
                      Text.rich(
                        TextSpan(
                          style: AppType.body,
                          children: [
                            TextSpan(
                              text: '${s.weakestLabel} ',
                              style: const TextStyle(
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                            TextSpan(
                              text: worst
                                  .take(3)
                                  .map(
                                    (e) =>
                                        '${e.key} ${e.value.correct}/${e.value.total}',
                                  )
                                  .join(' · ')
                                  .ifEmpty('—'),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: AppSpacing.s4),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(AppSpacing.s5),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(s.wrongReviewTitle, style: AppType.h3),
                      const SizedBox(height: AppSpacing.s2),
                      if (r.wrongList.isEmpty)
                        Text(s.noWrongAnswers, style: AppType.body)
                      else
                        ...r.wrongList.map((w) {
                          final q = w.view.question;
                          final yourOpt = w.view.shuffledOptions[w.selected];
                          final rightOpt =
                              w.view.shuffledOptions[w.view.correctIndex];
                          return ExpansionTile(
                            tilePadding: EdgeInsets.zero,
                            title: Text(q.text(ne), style: AppType.body),
                            subtitle: Text(
                              '${s.yourAnswer} ${String.fromCharCode(65 + w.selected)}. $yourOpt',
                              style: AppType.small.copyWith(
                                color: AppColors.danger,
                              ),
                            ),
                            children: [
                              Padding(
                                padding: const EdgeInsets.only(
                                  bottom: AppSpacing.s3,
                                ),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      '${s.correctIs} ${String.fromCharCode(65 + w.view.correctIndex)}. $rightOpt',
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
                          );
                        }),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: AppSpacing.s8),
            ],
          ),
        ),
      ),
    );
  }

  /// Trim trailing ".0" so "8 / 10" doesn't render as "8.0 / 10".
  String _trimNum(double v) => v == v.roundToDouble() ? '${v.toInt()}' : '$v';
}

class _ScoreRing extends StatelessWidget {
  final double pct;
  final bool passed;
  const _ScoreRing({required this.pct, required this.passed});

  @override
  Widget build(BuildContext context) {
    final frac = (pct.clamp(0, 100)) / 100;
    return SizedBox(
      width: 148,
      height: 148,
      child: Stack(
        alignment: Alignment.center,
        children: [
          SizedBox(
            width: 148,
            height: 148,
            child: CircularProgressIndicator(
              value: frac,
              strokeWidth: 12,
              backgroundColor:
                  Theme.of(context).colorScheme.surfaceContainerHighest,
              color: passed ? AppColors.green : AppColors.danger,
            ),
          ),
          Text(
            '${pct.toStringAsFixed(pct == pct.roundToDouble() ? 0 : 1)}%',
            style: AppType.h2,
          ),
        ],
      ),
    );
  }
}

class _Stat extends StatelessWidget {
  final String label;
  const _Stat(this.label);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: const BoxDecoration(
        color: AppColors.accentSoft,
        borderRadius: BorderRadius.all(AppRadius.pill),
      ),
      child: Text(label, style: AppType.small),
    );
  }
}

class _Banner extends StatelessWidget {
  final String text;
  final bool gold;
  const _Banner({required this.text, required this.gold});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(AppSpacing.s3),
      decoration: BoxDecoration(
        color: gold ? AppColors.accentSoft : AppColors.greenSoft,
        borderRadius: AppRadius.mdAll,
        border: Border.all(color: gold ? AppColors.accent : AppColors.green),
      ),
      child: Text(
        text,
        style: AppType.body.copyWith(fontWeight: FontWeight.w700),
        textAlign: TextAlign.center,
      ),
    );
  }
}

extension _IfEmpty on String {
  String ifEmpty(String fallback) => isEmpty ? fallback : this;
}
