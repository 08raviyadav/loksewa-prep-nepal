/// Quiz engine — pure Dart, zero Flutter imports.
///
/// Ports the vanilla site's quiz runner math exactly
/// (loksewa-prep-nepal/assets/js/app.js):
///   - per-question option shuffling with correct-answer remapping
///     (vanilla `shuffleOptions`)
///   - `scoreAttempt` scoring: Σ correct*marks − Σ wrong*marks*negRate
///     (skips score 0), rounded to 1 decimal; pct = max(0,score)/max*100
///     rounded to 1 decimal
///   - pass/fail judged on percentage vs the exam cutoff percentage
///     (vanilla `finishAttempt`: `passed = res.pct >= cutoffPct`)
library;

import 'dart:math';

import '../models/models.dart';

/// JS `Math.round` semantics (rounds halves toward +∞), matching the
/// vanilla site. Dart's `num.round()` rounds halves away from zero, which
/// differs for exact negative halves (e.g. Math.round(-2.5) === -2).
int jsRound(num x) => (x + 0.5).floor();

double _round1(num x) => jsRound(x * 10) / 10;

/// One question with its options shuffled for this attempt.
/// [correctIndex] is the index of the correct answer inside
/// [shuffledOptions] — the remap vanilla `shuffleOptions` performs.
class QuizQuestionView {
  final Question question;
  final List<String> shuffledOptions;
  final int correctIndex;

  const QuizQuestionView({
    required this.question,
    required this.shuffledOptions,
    required this.correctIndex,
  });
}

/// Immutable launch parameters for one quiz run.
/// The question list is the *raw* bank order; the engine shuffles each
/// question's options (vanilla `startPractice` maps `shuffleOptions` over
/// the picked set).
class QuizConfig {
  final List<Question> questions;
  final bool negOn;
  final double negRate;
  final bool timerOn;
  final int? timeLimitSecs;
  final String mode; // 'practice' | 'mock'
  final String examId;
  final int? seed; // deterministic shuffles in tests
  final String?
      dailySeed; // daily-challenge day key (yyyy-MM-dd); marks dailyDone

  const QuizConfig({
    required this.questions,
    this.negOn = true,
    this.negRate = 0.2,
    this.timerOn = false,
    this.timeLimitSecs,
    this.mode = 'practice',
    this.examId = '',
    this.seed,
    this.dailySeed,
  });
}

/// Cutoff metadata for the result screen, resolved from the exam's prelim
/// table (vanilla `finishAttempt`: cutoffPct = round(pass/total*100)).
class QuizMeta {
  final String examName;
  final int cutoff; // raw pass marks on the full paper
  final int cutoffPct; // percentage gate actually judged on
  final int fullTotal; // full paper total (vanilla prelim.total)

  const QuizMeta({
    required this.examName,
    required this.cutoff,
    required this.cutoffPct,
    required this.fullTotal,
  });
}

/// Per-question scoring detail for one finished attempt.
class QuestionScore {
  /// 1 = correct, 0 = wrong, -1 = skipped (vanilla qdetail codes).
  final int code;
  final String topic;
  final int marks;
  final int? selected; // chosen shuffled-option index, null when skipped
  final bool correct;

  const QuestionScore({
    required this.code,
    required this.topic,
    required this.marks,
    required this.selected,
    required this.correct,
  });
}

/// Aggregated per-topic stats for the result screen.
class TopicStat {
  int total = 0;
  int correct = 0;
  double get accuracy => total == 0 ? 0 : correct / total;
}

/// A wrong answer for the review list: the shuffled view plus what the
/// user picked.
class WrongEntry {
  final QuizQuestionView view;
  final int selected;

  const WrongEntry({required this.view, required this.selected});
}

/// The scored outcome of one attempt. Mirrors vanilla's `scoreAttempt`
/// result plus the derived lists the result screen needs.
class QuizResult {
  final double score;
  final int max;
  final double pct;
  final int correct;
  final int wrong;
  final int skipped;
  final int secs;
  final bool timedOut;
  final List<QuestionScore> perQuestion;
  final Map<String, TopicStat> byTopic;
  final List<WrongEntry> wrongList;

  const QuizResult({
    required this.score,
    required this.max,
    required this.pct,
    required this.correct,
    required this.wrong,
    required this.skipped,
    required this.secs,
    required this.timedOut,
    required this.perQuestion,
    required this.byTopic,
    required this.wrongList,
  });
}

/// Pass/fail gate, exactly as vanilla: judged on percentage, never on raw
/// marks (a short practice set can never reach 45/100 raw).
bool passesCutoff(double pct, int cutoffPct) => pct >= cutoffPct;

List<T> _shuffled<T>(List<T> items, Random rng) {
  final list = List<T>.from(items);
  for (var i = list.length - 1; i > 0; i--) {
    final j = rng.nextInt(i + 1);
    final tmp = list[i];
    list[i] = list[j];
    list[j] = tmp;
  }
  return list;
}

/// Shuffle one question's options, remapping the correct answer —
/// vanilla `shuffleOptions`.
QuizQuestionView shuffleQuestionOptions(Question q, Random rng) {
  final idx = _shuffled(List<int>.generate(q.options.length, (i) => i), rng);
  return QuizQuestionView(
    question: q,
    shuffledOptions: idx.map((i) => q.options[i]).toList(),
    correctIndex: idx.indexOf(q.answer),
  );
}

/// Stateful runner for one attempt. Answers are stored as shuffled-option
/// indices; `null` means unanswered (a skip scores 0, like vanilla).
class QuizEngine {
  final QuizConfig config;
  final List<QuizQuestionView> views;
  final List<int?> answers;

  QuizEngine(this.config)
      : views = _buildViews(config),
        answers = List<int?>.filled(config.questions.length, null);

  static List<QuizQuestionView> _buildViews(QuizConfig config) {
    final rng = config.seed == null ? Random() : Random(config.seed as int);
    return config.questions.map((q) => shuffleQuestionOptions(q, rng)).toList();
  }

  int get length => views.length;

  /// Record an answer for question [qIndex] (shuffled option [optionIdx]).
  /// Re-answering overwrites, like tapping another option would.
  void answer(int qIndex, int optionIdx) {
    _checkIndex(qIndex);
    if (optionIdx < 0 || optionIdx >= views[qIndex].shuffledOptions.length) {
      throw RangeError('optionIdx $optionIdx out of range');
    }
    answers[qIndex] = optionIdx;
  }

  /// Mark question [qIndex] as skipped (scores 0, never a mistake).
  void skip(int qIndex) {
    _checkIndex(qIndex);
    answers[qIndex] = null;
  }

  /// Clear the answer for [qIndex] (back to unanswered).
  void clear(int qIndex) {
    _checkIndex(qIndex);
    answers[qIndex] = null;
  }

  void _checkIndex(int qIndex) {
    if (qIndex < 0 || qIndex >= views.length) {
      throw RangeError('qIndex $qIndex out of range');
    }
  }

  int get answeredCount => answers.where((a) => a != null).length;
  bool get allAnswered => answeredCount == views.length;

  /// Score the attempt — vanilla `scoreAttempt`, verbatim math.
  QuizResult finish({int secs = 0, bool timedOut = false}) {
    var correct = 0, wrong = 0, skipped = 0;
    var score = 0.0;
    var max = 0;
    final perQuestion = <QuestionScore>[];
    final byTopic = <String, TopicStat>{};
    final wrongList = <WrongEntry>[];

    for (var i = 0; i < views.length; i++) {
      final view = views[i];
      final q = view.question;
      final marks = q.marks;
      max += marks;
      final a = answers[i];
      final isCorrect = a != null && a == view.correctIndex;
      if (a == null) {
        skipped++;
      } else if (isCorrect) {
        correct++;
        score += marks;
      } else {
        wrong++;
        if (config.negOn) score -= marks * config.negRate;
        wrongList.add(WrongEntry(view: view, selected: a));
      }
      perQuestion.add(
        QuestionScore(
          code: isCorrect ? 1 : (a == null ? -1 : 0),
          topic: q.topic.isEmpty ? 'General' : q.topic,
          marks: marks,
          selected: a,
          correct: isCorrect,
        ),
      );
      final stat = byTopic.putIfAbsent(
        perQuestion.last.topic,
        () => TopicStat(),
      );
      stat.total++;
      if (isCorrect) stat.correct++;
    }

    final roundedScore = _round1(score);
    final pct = max > 0 ? _round1((score < 0 ? 0 : score) / max * 100) : 0.0;

    return QuizResult(
      score: roundedScore,
      max: max,
      pct: pct,
      correct: correct,
      wrong: wrong,
      skipped: skipped,
      secs: secs,
      timedOut: timedOut,
      perQuestion: perQuestion,
      byTopic: byTopic,
      wrongList: wrongList,
    );
  }
}
