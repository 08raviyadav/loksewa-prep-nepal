/// Quiz runner screen: question card, 4 options, instant feedback with
/// explanation, skip/bookmark/report, timer, prev/next, finish confirm.
/// Ports the vanilla quiz view behavior (app.js `renderQuestion`,
/// `answerCurrent`, `skipQ`, `bookmarkCurrent`, `flagCurrent`).
library;

import 'dart:async';

import 'package:flutter/material.dart';

import '../../engine/quiz_engine.dart';
import '../../l10n/quiz_strings.dart';
import '../../models/models.dart';
import '../../state/progress_store.dart';
import '../../theme/app_theme.dart';
import '../../widgets/app_scaffold.dart';
import 'result_screen.dart';

class QuizScreen extends StatefulWidget {
  final QuizConfig config;
  final QuizMeta meta;

  /// Full question pool the set was drawn from — powers "practice weakest
  /// topic" on the result screen.
  final List<Question> bank;

  const QuizScreen({
    super.key,
    required this.config,
    required this.meta,
    this.bank = const [],
  });

  @override
  State<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  late final QuizEngine _engine;
  int _idx = 0;
  int? _picked; // selected option for the visible question this view
  String? _feedbackLine;
  bool? _feedbackOk;
  Timer? _timer;
  int _timeLeft = 0;
  late final DateTime _startTime;
  bool _finished = false;
  ProgressStore? _store;

  @override
  void initState() {
    super.initState();
    _engine = QuizEngine(widget.config);
    _startTime = DateTime.now();
    ProgressStore.instance.then((s) {
      if (mounted) setState(() => _store = s);
    });
    if (widget.config.timerOn && widget.config.timeLimitSecs != null) {
      _timeLeft = widget.config.timeLimitSecs!;
      _timer = Timer.periodic(const Duration(seconds: 1), (t) {
        if (!mounted) return;
        setState(() {
          _timeLeft--;
          if (_timeLeft <= 0) {
            t.cancel();
            _finish(timedOut: true);
          }
        });
      });
    }
    _syncView();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _syncView() {
    final a = _engine.answers[_idx];
    _picked = a;
    _feedbackLine = null;
    _feedbackOk = null;
  }

  String _fmtTime(int s) {
    s = s < 0 ? 0 : s;
    final m = s ~/ 60, r = s % 60;
    return '${m.toString().padLeft(2, '0')}:${r.toString().padLeft(2, '0')}';
  }

  Future<void> _answer(int optionIdx) async {
    if (_finished || _picked != null) return;
    final view = _engine.views[_idx];
    _engine.answer(_idx, optionIdx);
    final ok = optionIdx == view.correctIndex;
    final s = AppStateScope.of(context).strings;
    if (!ok) {
      // Vanilla `saveMistakeIfWrong` runs at answer time (practice + mock).
      await _store?.addMistake(view.question.id);
    } else if (widget.config.reviewMistakes) {
      // Mistake review (v1.0.4): a correct answer clears the mistake.
      await _store?.removeMistake(view.question.id);
    }
    setState(() {
      _picked = optionIdx;
      _feedbackOk = ok;
      _feedbackLine = ok ? s.praiseLine() : s.tryAgainLine();
    });
  }

  void _skip() {
    if (_finished) return;
    _engine.skip(_idx); // skips score 0 and never become mistakes
    if (_idx < _engine.length - 1) {
      setState(() {
        _idx++;
        _syncView();
      });
    } else {
      setState(_syncView);
    }
  }

  void _go(int i) {
    if (i < 0 || i >= _engine.length) return;
    setState(() {
      _idx = i;
      _syncView();
    });
  }

  Future<void> _toggleBookmark() async {
    final store = _store;
    if (store == null) return;
    final s = AppStateScope.of(context).strings;
    final id = _engine.views[_idx].question.id;
    final added = await store.toggleBookmark(id);
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(added ? s.bookmarked : s.alreadyBookmarked)),
    );
    setState(() {});
  }

  Future<void> _report() async {
    final store = _store;
    if (store == null) return;
    final s = AppStateScope.of(context).strings;
    final ctrl = TextEditingController();
    final note = await showDialog<String>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(s.reportTitle),
        content: TextField(
          controller: ctrl,
          autofocus: true,
          minLines: 2,
          maxLines: 4,
          decoration: InputDecoration(hintText: s.reportHint),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: Text(s.cancel),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(ctx, ctrl.text.trim()),
            child: Text(s.save),
          ),
        ],
      ),
    );
    if (note != null && note.isNotEmpty && mounted) {
      await store.reportQuestion(_engine.views[_idx].question.id, note);
      if (!mounted) return;
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(s.reportSaved)));
    }
  }

  Future<void> _confirmFinish() async {
    if (_finished) return;
    final s = AppStateScope.of(context).strings;
    final unanswered = _engine.length - _engine.answeredCount;
    final go = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(s.finishTitle),
        content: Text(s.finishBody(unanswered)),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: Text(s.cancel),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: Text(s.submit),
          ),
        ],
      ),
    );
    if (go == true) _finish(timedOut: false);
  }

  Future<void> _finish({required bool timedOut}) async {
    // One attempt = one record (vanilla `finishAttempt` double-tap guard).
    if (_finished) return;
    _finished = true;
    _timer?.cancel();
    final secs = DateTime.now().difference(_startTime).inSeconds;
    final result = _engine.finish(secs: secs, timedOut: timedOut);
    final store = await ProgressStore.instance;
    final dailySeed = widget.config.dailySeed;
    final qotdSeed = widget.config.qotdSeed;
    final summary = await store.recordAttempt(
      result: result,
      mode: widget.config.mode,
      examId: widget.config.examId,
      cutoff: widget.meta.cutoff,
      cutoffPct: widget.meta.cutoffPct,
      timedOut: timedOut,
      // Vanilla daily-challenge rule: repeating today's challenge burns no
      // XP. Same for a repeated Question of the Day (v1.0.4).
      noXp: (dailySeed != null && store.isDailyDone(dailySeed)) ||
          (qotdSeed != null && store.isQotdDone(qotdSeed)),
      dailySeed: dailySeed,
      qotdSeed: qotdSeed,
    );
    if (!mounted) return;
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => ResultScreen(
          result: result,
          meta: widget.meta,
          config: widget.config,
          summary: summary,
          bank: widget.bank,
          store: store,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;
    final scheme = Theme.of(context).colorScheme;
    final total = _engine.length;

    if (total == 0) {
      return Scaffold(
        appBar: AppBar(title: Text(s.practiceTitle)),
        body: Center(child: Text(s.noQuestions)),
      );
    }

    final view = _engine.views[_idx];
    final q = view.question;
    final answered = _picked != null;
    final isBookmarked = _store?.isBookmarked(q.id) ?? false;

    return Scaffold(
      appBar: AppBar(
        title: Text(s.quizProgress(_idx + 1, total)),
        actions: [
          if (widget.config.timerOn)
            Padding(
              padding: const EdgeInsets.only(right: AppSpacing.s3),
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: _timeLeft <= 300
                        ? AppColors.dangerSoft
                        : AppColors.accentSoft,
                    borderRadius: const BorderRadius.all(AppRadius.pill),
                  ),
                  child: Text(
                    _fmtTime(_timeLeft),
                    style: AppType.small.copyWith(
                      fontWeight: FontWeight.w800,
                      color: _timeLeft <= 300
                          ? AppColors.danger
                          : AppColors.accentStrong,
                      fontFeatures: const [FontFeature.tabularFigures()],
                    ),
                  ),
                ),
              ),
            ),
        ],
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(4),
          child: LinearProgressIndicator(
            value: (_idx + 1) / total,
            backgroundColor: scheme.surfaceContainerHighest,
            color: AppColors.accent,
            minHeight: 4,
          ),
        ),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: AppSpacing.maxWidth),
          child: ListView(
            padding: const EdgeInsets.all(AppSpacing.s4),
            children: [
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(AppSpacing.s5),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Wrap(
                        spacing: AppSpacing.s2,
                        children: [
                          _Tag(q.topic),
                          _Tag(q.difficulty),
                          _Tag(
                            '${q.marks} ${ne ? 'अंक' : 'mark${q.marks == 1 ? '' : 's'}'}',
                          ),
                        ],
                      ),
                      const SizedBox(height: AppSpacing.s3),
                      Text(q.text(ne), style: AppType.h3),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: AppSpacing.s3),
              ...List.generate(view.shuffledOptions.length, (i) {
                final isCorrect = i == view.correctIndex;
                final isPicked = _picked == i;
                Color? bg;
                Color? border;
                if (answered) {
                  if (isCorrect) {
                    bg = AppColors.greenSoft;
                    border = AppColors.green;
                  } else if (isPicked) {
                    bg = AppColors.dangerSoft;
                    border = AppColors.danger;
                  }
                }
                return Padding(
                  padding: const EdgeInsets.only(bottom: AppSpacing.s2),
                  child: OutlinedButton(
                    onPressed: answered ? null : () => _answer(i),
                    style: OutlinedButton.styleFrom(
                      minimumSize: const Size(
                        double.infinity,
                        AppSpacing.minTap,
                      ),
                      alignment: Alignment.centerLeft,
                      padding: const EdgeInsets.symmetric(
                        horizontal: AppSpacing.s4,
                        vertical: AppSpacing.s3,
                      ),
                      backgroundColor: bg,
                      side: BorderSide(
                        color: border ?? Theme.of(context).dividerColor,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: AppRadius.mdAll,
                      ),
                    ),
                    child: Row(
                      children: [
                        Container(
                          width: 32,
                          height: 32,
                          alignment: Alignment.center,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: isCorrect && answered
                                ? AppColors.green
                                : isPicked && answered
                                    ? AppColors.danger
                                    : scheme.surfaceContainerHighest,
                          ),
                          child: Text(
                            String.fromCharCode(65 + i),
                            style: AppType.small.copyWith(
                              fontWeight: FontWeight.w800,
                            ),
                          ),
                        ),
                        const SizedBox(width: AppSpacing.s3),
                        Expanded(
                          child: Text(
                            view.shuffledOptions[i],
                            style: AppType.body,
                          ),
                        ),
                        if (answered && isCorrect)
                          const Icon(
                            Icons.check_circle,
                            color: AppColors.green,
                          ),
                        if (answered && isPicked && !isCorrect)
                          const Icon(Icons.cancel, color: AppColors.danger),
                      ],
                    ),
                  ),
                );
              }),
              if (answered) ...[
                const SizedBox(height: AppSpacing.s2),
                Card(
                  color: _feedbackOk == true
                      ? AppColors.greenSoft
                      : AppColors.dangerSoft,
                  child: Padding(
                    padding: const EdgeInsets.all(AppSpacing.s4),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          _feedbackOk == true
                              ? s.correctFeedback
                              : s.wrongFeedback,
                          style: AppType.h3.copyWith(
                            color: _feedbackOk == true
                                ? AppColors.green
                                : AppColors.danger,
                          ),
                        ),
                        if (_feedbackOk != true) ...[
                          const SizedBox(height: AppSpacing.s2),
                          Text(
                            '${s.correctAnswerIs} ${String.fromCharCode(65 + view.correctIndex)}. ${view.shuffledOptions[view.correctIndex]}',
                            style: AppType.body.copyWith(
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ],
                        if (q.explain(ne).isNotEmpty) ...[
                          const SizedBox(height: AppSpacing.s2),
                          Text(
                            '${s.explanationLabel}: ${q.explain(ne)}',
                            style: AppType.body,
                          ),
                        ],
                        if (_feedbackLine != null) ...[
                          const SizedBox(height: AppSpacing.s2),
                          Text(
                            _feedbackLine!,
                            style: AppType.small.copyWith(
                              fontStyle: FontStyle.italic,
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ],
              const SizedBox(height: AppSpacing.s4),
              Wrap(
                spacing: AppSpacing.s2,
                runSpacing: AppSpacing.s2,
                children: [
                  OutlinedButton.icon(
                    onPressed: _skip,
                    icon: const Icon(Icons.skip_next_outlined),
                    label: Text(s.skip),
                    style: OutlinedButton.styleFrom(
                      minimumSize: const Size(0, AppSpacing.minTap),
                    ),
                  ),
                  OutlinedButton.icon(
                    onPressed: _toggleBookmark,
                    icon: Icon(
                      isBookmarked ? Icons.bookmark : Icons.bookmark_border,
                    ),
                    label: Text(s.bookmark),
                    style: OutlinedButton.styleFrom(
                      minimumSize: const Size(0, AppSpacing.minTap),
                    ),
                  ),
                  OutlinedButton.icon(
                    onPressed: _report,
                    icon: const Icon(Icons.flag_outlined),
                    label: Text(s.report),
                    style: OutlinedButton.styleFrom(
                      minimumSize: const Size(0, AppSpacing.minTap),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: AppSpacing.s6),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: _idx > 0 ? () => _go(_idx - 1) : null,
                      style: OutlinedButton.styleFrom(
                        minimumSize: const Size(0, AppSpacing.minTap),
                      ),
                      child: Text(s.previous),
                    ),
                  ),
                  const SizedBox(width: AppSpacing.s3),
                  Expanded(
                    child: OutlinedButton(
                      onPressed: _idx < total - 1 ? () => _go(_idx + 1) : null,
                      style: OutlinedButton.styleFrom(
                        minimumSize: const Size(0, AppSpacing.minTap),
                      ),
                      child: Text(s.next),
                    ),
                  ),
                  const SizedBox(width: AppSpacing.s3),
                  Expanded(
                    child: FilledButton(
                      onPressed: _confirmFinish,
                      style: FilledButton.styleFrom(
                        backgroundColor: AppColors.accent,
                        foregroundColor: AppColors.accentInk,
                        minimumSize: const Size(0, AppSpacing.minTap),
                      ),
                      child: Text(s.finish),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: AppSpacing.s8),
            ],
          ),
        ),
      ),
    );
  }
}

class _Tag extends StatelessWidget {
  final String label;
  const _Tag(this.label);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: const BoxDecoration(
        color: AppColors.accentSoft,
        borderRadius: BorderRadius.all(AppRadius.pill),
      ),
      child: Text(
        label,
        style: AppType.tiny.copyWith(
          color: AppColors.accentStrong,
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }
}
