/// Mock exam flow: pre-mock pattern summary card → timed exam-hall runner.
///
/// Ports the vanilla mock view (app.js `startMock`, `renderQuestion` with
/// `mode === 'mock'`, `renderMockTable`):
///
///   - Intro card summarises the real paper's pattern (questions, time,
///     marks/Q, pass, negative marking) resolved from `prelim`, with the
///     thin-bank honesty warning and a Start button.
///   - The runner is the exam hall: countdown timer (MM:SS, red under
///     5:00 — vanilla's `low` class), auto-submit at zero
///     (`timedOut: true`), an OMR-style question palette (answered =
///     green, current = blue, flagged = yellow, unanswered = grey; tap to
///     jump), Prev/Next, and NO instant feedback — answers stay hidden
///     until the paper is finished.
///   - Finish shows a confirm dialog with answered/unanswered counts, then
///     scores through `QuizEngine.finish()` and records the attempt with
///     mode `'mock'`, reusing the existing `ResultScreen`.
library;

import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;

import '../data/data_repository.dart';
import '../engine/mock_specs.dart';
import '../engine/quiz_engine.dart';
import '../l10n/mock_strings.dart';
import '../l10n/quiz_strings.dart';
import '../models/models.dart';
import '../state/progress_store.dart';
import '../theme/app_theme.dart';
import '../widgets/app_scaffold.dart';
import 'quiz/result_screen.dart';

/// Palette cell states — vanilla's palette knows answered/current; the
/// flagged state is the exam-hall "review later" marker.
enum PaletteState { answered, current, flagged, unanswered }

/// Pure palette-state rule, in precedence order (current wins over
/// answered, answered over flagged — a flagged question that gets
/// answered still shows as answered).
PaletteState paletteCellState({
  required bool answered,
  required bool current,
  required bool flagged,
}) {
  if (current) return PaletteState.current;
  if (answered) return PaletteState.answered;
  if (flagged) return PaletteState.flagged;
  return PaletteState.unanswered;
}

/// The live mock attempt: engine + navigation index + review flags +
/// countdown. Pure Dart apart from the QuizEngine it wraps, so the timer
/// and palette logic are unit-testable.
class MockSession {
  final QuizEngine engine;
  final MockSpec spec;

  /// Full paper the questions were drawn from — powers "practice weakest
  /// topic" on the result screen.
  final List<Question> bank;

  /// Question ids flagged for review (yellow in the palette).
  final Set<String> flaggedIds = {};

  int index = 0;
  int timeLeft;
  bool timedOut = false;
  bool finished = false;

  MockSession({required this.engine, required this.spec, required this.bank})
      : timeLeft = spec.timeLimitSecs ?? 0;

  bool get timerOn => spec.timed;
  int get length => engine.length;
  int get answeredCount => engine.answeredCount;
  int get unansweredCount => length - answeredCount;
  String get currentId => engine.views[index].question.id;
  bool isFlagged(int i) => flaggedIds.contains(engine.views[i].question.id);

  /// Record the tapped option for the current question. Re-tapping another
  /// option overwrites — exactly like vanilla's `answerOption` in mock
  /// mode. No feedback is produced or stored (exam-hall rule).
  void recordAnswer(int optionIdx) => engine.answer(index, optionIdx);

  /// Toggle the review flag on the current question.
  /// Returns true when the question is now flagged.
  bool toggleFlag() {
    final id = currentId;
    if (flaggedIds.contains(id)) {
      flaggedIds.remove(id);
      return false;
    }
    flaggedIds.add(id);
    return true;
  }

  /// One countdown tick. Returns true when the timer just hit zero —
  /// the runner auto-submits then (vanilla `startTimer` onTimeout).
  bool tick() {
    if (!timerOn || finished) return false;
    timeLeft--;
    if (timeLeft <= 0) {
      timeLeft = 0;
      timedOut = true;
      finished = true;
      return true;
    }
    return false;
  }
}

class MockExamScreen extends StatefulWidget {
  /// Exam id; task-list aliases (e.g. 'tsc-general') are resolved to the
  /// bank's ids.
  final String examId;

  const MockExamScreen({super.key, required this.examId});

  @override
  State<MockExamScreen> createState() => _MockExamScreenState();
}

class _MockExamScreenState extends State<MockExamScreen> {
  // Phase 1 ships one sample question file (mirrors PracticeScreen).
  // Phase 2 loads the per-exam file manifest (all 131 files).
  static const _sampleFile = 'constitution-governance-economy.json';

  bool _loading = true;
  bool _started = false;
  Exam? _exam;
  MockSpec? _spec;
  MockPaper? _paper;
  List<Question> _bank = [];

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final examId = resolveMockExamId(widget.examId);
    Exam? exam;
    Map<String, dynamic>? prelim;
    List<Question> bank = [];
    try {
      final repo = DataRepository();
      final exams = await repo.exams();
      for (final e in exams) {
        if (e.id == examId) {
          exam = e;
          break;
        }
      }
      bank = await repo.questions(_sampleFile);
      final raw = await rootBundle.loadString('assets/data/exams.json');
      final decoded = json.decode(raw);
      final list = decoded is List ? decoded : decoded['exams'] as List;
      for (final e in list) {
        final m = Map<String, dynamic>.from(e as Map);
        if (m['id'] == examId) {
          final p = m['prelim'];
          prelim = p == null ? null : Map<String, dynamic>.from(p as Map);
          break;
        }
      }
    } catch (_) {
      // _exam stays null → the error view below.
    }
    if (!mounted) return;
    MockSpec? spec;
    MockPaper? paper;
    if (exam != null) {
      try {
        spec = MockSpec.fromPrelim(examId, prelim);
        paper = buildMockPaper(examId, spec, bank);
      } on StateError {
        // Guide-only exam: spec stays null → the no-mock view below.
      }
    }
    setState(() {
      _loading = false;
      _exam = exam;
      _spec = spec;
      _paper = paper;
      _bank = bank;
    });
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final started = _started;
    final spec = _spec;
    final paper = _paper;
    final exam = _exam;

    Widget body;
    if (_loading) {
      body = Center(child: Text(s.loadingMock));
    } else if (exam == null) {
      body = Center(child: Text(s.noMockAvailable));
    } else if (started && spec != null && paper != null) {
      return _MockRunnerScreen(
        key: ValueKey('runner-${exam.id}'),
        exam: exam,
        spec: spec,
        paper: paper,
        bank: _bank,
      );
    } else {
      body = _IntroCard(
        exam: exam,
        spec: spec,
        paper: paper,
        onStart: (spec != null && paper != null && paper.questions.isNotEmpty)
            ? () => setState(() => _started = true)
            : null,
      );
    }
    return Scaffold(
      appBar: AppBar(title: Text(s.mockIntroTitle)),
      body: body,
    );
  }
}

/// Pre-mock pattern summary card — the vanilla `renderMockTable` row plus
/// the `startMock` alert text, rendered as a card instead of an alert.
class _IntroCard extends StatelessWidget {
  final Exam exam;
  final MockSpec? spec;
  final MockPaper? paper;
  final VoidCallback? onStart;

  const _IntroCard({
    required this.exam,
    required this.spec,
    required this.paper,
    required this.onStart,
  });

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;
    final spec = this.spec;

    if (spec == null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.s6),
          child: Text(s.noMockAvailable, textAlign: TextAlign.center),
        ),
      );
    }
    final negLine = !spec.negativeApplied
        ? (spec.negRate == 0 ? s.negNoneLine : s.negUnverifiedLine)
        : s.negPctLine((spec.negRate * 100).round());

    return Center(
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
                    Text(exam.title(ne), style: AppType.h2),
                    const SizedBox(height: AppSpacing.s2),
                    Text(
                      s.patternTitle,
                      style: AppType.small.copyWith(
                        color: AppColors.of(context).muted,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    const SizedBox(height: AppSpacing.s3),
                    _PatternRow(
                      label: s.patternQuestions,
                      value: '${spec.questionCount}',
                    ),
                    _PatternRow(
                      label: s.patternTime,
                      value: spec.timed
                          ? s.minutesLabel(spec.timeMin!)
                          : s.untimedLine,
                    ),
                    _PatternRow(
                      label: s.patternMarksPerQ,
                      value: '${spec.marksPerQ}',
                    ),
                    _PatternRow(
                      label: s.patternPass,
                      value:
                          '${spec.cutoff}/${spec.fullTotal} (${spec.cutoffPct}%)',
                    ),
                    _PatternRow(label: s.patternNegative, value: negLine),
                    if (paper?.thinBank == true) ...[
                      const SizedBox(height: AppSpacing.s3),
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.s3),
                        decoration: BoxDecoration(
                          color: AppColors.of(context).accentSoft,
                          borderRadius: const BorderRadius.all(AppRadius.md),
                        ),
                        child: Text(
                          s.thinBankWarning(paper!.taggedCount, exam.title(ne)),
                          style: AppType.small,
                        ),
                      ),
                    ],
                    const SizedBox(height: AppSpacing.s3),
                    Text(s.mockGoodLuck, style: AppType.small),
                  ],
                ),
              ),
            ),
            const SizedBox(height: AppSpacing.s4),
            FilledButton(
              onPressed: onStart,
              style: FilledButton.styleFrom(
                backgroundColor: AppColors.of(context).accent,
                foregroundColor: AppColors.of(context).accentInk,
                minimumSize: const Size(double.infinity, AppSpacing.minTap),
              ),
              child: Text(s.startMockBtn),
            ),
          ],
        ),
      ),
    );
  }
}

class _PatternRow extends StatelessWidget {
  final String label;
  final String value;
  const _PatternRow({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: AppSpacing.s1),
      child: Row(
        children: [
          Expanded(
            child: Text(
              label,
              style: AppType.body.copyWith(color: AppColors.of(context).muted),
            ),
          ),
          const SizedBox(width: AppSpacing.s3),
          Flexible(
            child: Text(
              value,
              textAlign: TextAlign.right,
              style: AppType.body.copyWith(fontWeight: FontWeight.w700),
            ),
          ),
        ],
      ),
    );
  }
}

/// The exam hall: countdown, question card, options (no feedback),
/// palette, prev/next, finish-with-confirm, auto-submit at zero.
class _MockRunnerScreen extends StatefulWidget {
  final Exam exam;
  final MockSpec spec;
  final MockPaper paper;
  final List<Question> bank;

  const _MockRunnerScreen({
    super.key,
    required this.exam,
    required this.spec,
    required this.paper,
    required this.bank,
  });

  @override
  State<_MockRunnerScreen> createState() => _MockRunnerScreenState();
}

class _MockRunnerScreenState extends State<_MockRunnerScreen> {
  late final MockSession _session;
  late final DateTime _startTime;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    final spec = widget.spec;
    final config = QuizConfig(
      questions: widget.paper.questions,
      negOn: spec.negativeApplied,
      negRate: spec.negRate,
      timerOn: spec.timed,
      timeLimitSecs: spec.timeLimitSecs,
      mode: 'mock',
      examId: spec.examId,
    );
    _session = MockSession(
      engine: QuizEngine(config),
      spec: spec,
      bank: widget.bank,
    );
    _startTime = DateTime.now();
    if (spec.timed) {
      _timer = Timer.periodic(const Duration(seconds: 1), (t) {
        if (!mounted) return;
        final hitZero = _session.tick();
        setState(() {});
        if (hitZero) {
          t.cancel();
          _finish(timedOut: true);
        }
      });
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _go(int i) {
    if (i < 0 || i >= _session.length || _session.finished) return;
    setState(() => _session.index = i);
  }

  void _answer(int optionIdx) {
    if (_session.finished) return;
    // The no-feedback rule (shouldShowFeedback('mock') is false): record
    // and re-render; nothing reveals whether the answer was right or wrong
    // until the paper is finished.
    _session.recordAnswer(optionIdx);
    setState(() {});
  }

  void _toggleFlag() {
    if (_session.finished) return;
    final s = AppStateScope.of(context).strings;
    final flagged = _session.toggleFlag();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(flagged ? s.flaggedSnack : s.unflaggedSnack)),
    );
    setState(() {});
  }

  Future<void> _confirmAbandon() async {
    final s = AppStateScope.of(context).strings;
    final leave = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(s.abandonMockTitle),
        content: Text(s.abandonMockBody),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: Text(s.stayLabel),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: Text(s.leaveLabel),
          ),
        ],
      ),
    );
    if (leave == true && mounted) Navigator.of(context).pop();
  }

  Future<void> _confirmFinish() async {
    if (_session.finished) return;
    final s = AppStateScope.of(context).strings;
    final go = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(s.finishMockTitle),
        content: Text(
          s.finishMockBody(_session.answeredCount, _session.unansweredCount),
        ),
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
    if (_session.finished && !timedOut) return;
    _session.finished = true;
    _timer?.cancel();
    if (timedOut && mounted) {
      final s = AppStateScope.of(context).strings;
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(s.timeUpAutoSubmitted)));
    }
    final secs = DateTime.now().difference(_startTime).inSeconds;
    final result = _session.engine.finish(
      secs: secs,
      timedOut: timedOut || _session.timedOut,
    );
    final store = await ProgressStore.instance;
    final spec = widget.spec;
    final summary = await store.recordAttempt(
      result: result,
      mode: 'mock',
      examId: spec.examId,
      cutoff: spec.cutoff,
      cutoffPct: spec.cutoffPct,
      timedOut: timedOut || _session.timedOut,
    );
    if (!mounted) return;
    final ne = AppStateScope.of(context).isNe;
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => ResultScreen(
          result: result,
          meta: QuizMeta(
            examName: widget.exam.title(ne),
            cutoff: spec.cutoff,
            cutoffPct: spec.cutoffPct,
            fullTotal: spec.fullTotal,
          ),
          config: _session.engine.config,
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
    final session = _session;
    final total = session.length;
    final idx = session.index;
    final view = session.engine.views[idx];
    final q = view.question;
    final picked = session.engine.answers[idx];
    final isFlagged = session.isFlagged(idx);
    final lowTime = session.timerOn && session.timeLeft <= 300;

    return PopScope(
      canPop: !session.timerOn || session.finished,
      onPopInvokedWithResult: (didPop, _) {
        if (!didPop && session.timerOn && !session.finished) {
          _confirmAbandon();
        }
      },
      child: Scaffold(
        appBar: AppBar(
          title: Text(s.quizProgress(idx + 1, total)),
          actions: [
            Padding(
              padding: const EdgeInsets.only(right: AppSpacing.s3),
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: session.timerOn
                        ? (lowTime
                            ? AppColors.of(context).dangerSoft
                            : AppColors.of(context).accentSoft)
                        : scheme.surfaceContainerHighest,
                    borderRadius: const BorderRadius.all(AppRadius.pill),
                  ),
                  child: Text(
                    session.timerOn
                        ? formatMockTime(session.timeLeft)
                        : s.noTimerLabel,
                    style: AppType.small.copyWith(
                      fontWeight: FontWeight.w800,
                      color: session.timerOn
                          ? (lowTime
                              ? AppColors.of(context).danger
                              : AppColors.of(context).accentStrong)
                          : AppColors.of(context).muted,
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
              value: (idx + 1) / total,
              backgroundColor: scheme.surfaceContainerHighest,
              color: AppColors.of(context).accent,
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
                Row(
                  children: [
                    Expanded(
                      child: Text(
                        s.mockRunnerTitle(widget.exam.title(ne)),
                        style: AppType.h3,
                      ),
                    ),
                    Text(
                      s.answeredOf(session.answeredCount, total),
                      style: AppType.small.copyWith(color: AppColors.of(context).muted),
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.s3),
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
                  final isPicked = picked == i;
                  return Padding(
                    padding: const EdgeInsets.only(bottom: AppSpacing.s2),
                    child: OutlinedButton(
                      // Exam-hall rule: the tapped option is marked as
                      // *selected* (neutral), never as right/wrong.
                      onPressed: () => _answer(i),
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
                        backgroundColor: isPicked ? AppColors.of(context).accentSoft : null,
                        side: BorderSide(
                          color: isPicked
                              ? AppColors.of(context).accent
                              : Theme.of(context).dividerColor,
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
                              color: isPicked
                                  ? AppColors.of(context).accent
                                  : scheme.surfaceContainerHighest,
                            ),
                            child: Text(
                              String.fromCharCode(65 + i),
                              style: AppType.small.copyWith(
                                fontWeight: FontWeight.w800,
                                color: isPicked ? AppColors.of(context).accentInk : null,
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
                        ],
                      ),
                    ),
                  );
                }),
                const SizedBox(height: AppSpacing.s2),
                Wrap(
                  spacing: AppSpacing.s2,
                  runSpacing: AppSpacing.s2,
                  children: [
                    OutlinedButton.icon(
                      onPressed: _toggleFlag,
                      icon: Icon(isFlagged ? Icons.flag : Icons.flag_outlined),
                      label: Text(isFlagged ? s.unflagBtn : s.flagBtn),
                      style: OutlinedButton.styleFrom(
                        minimumSize: const Size(0, AppSpacing.minTap),
                      ),
                    ),
                    OutlinedButton.icon(
                      onPressed: idx > 0 ? () => _go(idx - 1) : null,
                      icon: const Icon(Icons.arrow_back),
                      label: Text(s.previous),
                      style: OutlinedButton.styleFrom(
                        minimumSize: const Size(0, AppSpacing.minTap),
                      ),
                    ),
                    OutlinedButton.icon(
                      onPressed: idx < total - 1 ? () => _go(idx + 1) : null,
                      icon: const Icon(Icons.arrow_forward),
                      label: Text(s.next),
                      style: OutlinedButton.styleFrom(
                        minimumSize: const Size(0, AppSpacing.minTap),
                      ),
                    ),
                    FilledButton.icon(
                      onPressed: _confirmFinish,
                      icon: const Icon(Icons.check),
                      label: Text(s.finish),
                      style: FilledButton.styleFrom(
                        backgroundColor: AppColors.of(context).accent,
                        foregroundColor: AppColors.of(context).accentInk,
                        minimumSize: const Size(0, AppSpacing.minTap),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.s4),
                _PaletteCard(session: session, onJump: _go),
                const SizedBox(height: AppSpacing.s8),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

/// OMR-style question palette: grid of numbered buttons — answered green,
/// current blue, flagged orange, unanswered grey. Tap jumps to the
/// question (vanilla `jumpTo`).
class _PaletteCard extends StatelessWidget {
  final MockSession session;
  final void Function(int) onJump;

  const _PaletteCard({required this.session, required this.onJump});

  // The palette is resolved in build() and passed down — these helpers
  // have no BuildContext of their own.
  Color _bg(AppPalette p, PaletteState st) => switch (st) {
        PaletteState.answered => p.greenSoft,
        PaletteState.current => p.blueSoft,
        PaletteState.flagged => const Color(0x33EA580C),
        PaletteState.unanswered => p.card2,
      };

  Color _fg(AppPalette p, PaletteState st) => switch (st) {
        PaletteState.answered => p.green,
        PaletteState.current => p.blue,
        PaletteState.flagged => p.accentStrong,
        PaletteState.unanswered => p.muted,
      };

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final p = AppColors.of(context);
    final total = session.length;
    final answers = session.engine.answers;
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s4),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              s.paletteTitle,
              style: AppType.h3.copyWith(fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: AppSpacing.s2),
            Wrap(
              spacing: AppSpacing.s3,
              runSpacing: AppSpacing.s1,
              children: [
                _LegendDot(color: AppColors.of(context).green, label: s.legendAnswered),
                _LegendDot(color: AppColors.of(context).blue, label: s.legendCurrent),
                _LegendDot(
                  color: AppColors.of(context).accentStrong,
                  label: s.legendFlagged,
                ),
                _LegendDot(color: AppColors.of(context).muted, label: s.legendUnanswered),
              ],
            ),
            const SizedBox(height: AppSpacing.s3),
            GridView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: total > 50 ? 10 : 8,
                mainAxisSpacing: AppSpacing.s1,
                crossAxisSpacing: AppSpacing.s1,
              ),
              itemCount: total,
              itemBuilder: (ctx, i) {
                final st = paletteCellState(
                  answered: answers[i] != null,
                  current: i == session.index,
                  flagged: session.isFlagged(i),
                );
                return Material(
                  color: _bg(p, st),
                  borderRadius: const BorderRadius.all(AppRadius.sm),
                  child: InkWell(
                    borderRadius: const BorderRadius.all(AppRadius.sm),
                    onTap: () => onJump(i),
                    child: Center(
                      child: Text(
                        '${i + 1}',
                        style: AppType.small.copyWith(
                          fontWeight: FontWeight.w700,
                          color: _fg(p, st),
                          fontFeatures: const [FontFeature.tabularFigures()],
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}

class _LegendDot extends StatelessWidget {
  final Color color;
  final String label;
  const _LegendDot({required this.color, required this.label});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 12,
          height: 12,
          decoration: BoxDecoration(shape: BoxShape.circle, color: color),
        ),
        const SizedBox(width: AppSpacing.s1),
        Text(label, style: AppType.tiny),
      ],
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
      decoration: BoxDecoration(
        color: AppColors.of(context).accentSoft,
        borderRadius: const BorderRadius.all(AppRadius.pill),
      ),
      child: Text(
        label,
        style: AppType.tiny.copyWith(
          color: AppColors.of(context).accentStrong,
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }
}
