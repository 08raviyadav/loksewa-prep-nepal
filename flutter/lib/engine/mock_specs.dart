/// Mock exam specs + paper builder — pure Dart, zero Flutter imports.
///
/// Ports the vanilla site's mock logic exactly
/// (loksewa-prep-nepal/assets/js/app.js: `startMock`, `mockMixFor`,
/// `mockNegRate`, `cutoffFor`):
///
///   - The paper mirrors the real exam's prelim pattern: fixed question
///     count, time limit, per-question marks, the exam's negative-marking
///     rate and the pass cutoff — resolved from `assets/data/exams.json`,
///     never hardcoded.
///   - The paper is drawn from the exam's tagged pool with the vanilla
///     topic mix (`mockMixFor`); when the tagged pool is thinner than the
///     paper, it falls back to a uniform draw from the general bank
///     (vanilla's silent fallback, surfaced here via `thinBank`).
///   - Every question's marks are set to the prelim `marksPerQ`
///     (vanilla's `{...q, marks: p.marksPerQ}`).
///   - `timeMin: null` (unverified) runs the mock UNTIMED rather than
///     starting a 0-second timer that would auto-submit instantly.
library;

import 'dart:math';

import '../models/models.dart';
import 'quiz_engine.dart' show jsRound;

/// Task-list exam ids mapped to the bank's exam ids
/// ('TSC General' = the 50Q/60min TSC paper = tsc-primary).
const Map<String, String> kMockExamAliases = {'tsc-general': 'tsc-primary'};

/// Resolve an incoming exam id through the alias table.
String resolveMockExamId(String examId) => kMockExamAliases[examId] ?? examId;

/// One exam's mock pattern, resolved from its `prelim` table in
/// assets/data/exams.json (vanilla `e.prelim`).
class MockSpec {
  /// Exam id in the bank (aliases already resolved).
  final String examId;

  /// Questions on the paper (vanilla `p.questions`).
  final int questionCount;

  /// Minutes on the clock; null = unverified → vanilla runs UNTIMED.
  final int? timeMin;

  /// Vanilla `mockNegRate`: null/0 = no deduction, else the stored rate.
  final double negRate;

  /// Raw pass marks on the full paper (vanilla `cutoffFor` = `p.pass`).
  final int cutoff;

  /// The gate actually judged on: round(pass/total*100) — vanilla
  /// `finishAttempt` compares `res.pct` against this, never raw marks.
  final int cutoffPct;

  /// Full-paper total (vanilla `p.total`).
  final int fullTotal;

  /// Marks per question (vanilla `p.marksPerQ`).
  final int marksPerQ;

  const MockSpec({
    required this.examId,
    required this.questionCount,
    required this.timeMin,
    required this.negRate,
    required this.cutoff,
    required this.cutoffPct,
    required this.fullTotal,
    required this.marksPerQ,
  });

  /// Build from one exam's `prelim` JSON object. Throws [StateError] when
  /// the exam has no prelim (guide-only exams must never start a mock —
  /// vanilla guards this in `startMock` too).
  factory MockSpec.fromPrelim(String examId, Map<String, dynamic>? prelim) {
    if (prelim == null) {
      throw StateError('No mock available for exam "$examId" — guide only.');
    }
    final neg = prelim['negative'] as num?;
    final negRate = (neg == null || neg == 0) ? 0.0 : neg.toDouble();
    final pass = (prelim['pass'] as num?)?.toInt() ?? 45;
    final total = (prelim['total'] as num?)?.toInt() ?? 100;
    return MockSpec(
      examId: examId,
      questionCount: (prelim['questions'] as num?)?.toInt() ?? 50,
      timeMin: (prelim['timeMin'] as num?)?.toInt(),
      negRate: negRate,
      cutoff: pass,
      cutoffPct: jsRound(pass / total * 100),
      fullTotal: total,
      marksPerQ: (prelim['marksPerQ'] as num?)?.toInt() ?? 1,
    );
  }

  /// Vanilla: `const timed = p.timeMin != null`.
  bool get timed => timeMin != null;

  int? get timeLimitSecs => timed ? timeMin! * 60 : null;

  bool get negativeApplied => negRate > 0;
}

/// Vanilla `mockNegRate` as a standalone helper: null/0 = no deduction,
/// otherwise the stored rate (0.2 on PSC entries, 0.25 on MECEE-BL).
double mockNegRate(Map<String, dynamic>? prelim) {
  final neg = prelim?['negative'] as num?;
  if (neg == null || neg == 0) return 0.0;
  return neg.toDouble();
}

/// Vanilla `mockMixFor`: the plain "Topic N Q + ..." breakdowns that are a
/// topic name + count. Returns null when the breakdown is not parseable
/// (percentages, prose, licence weight tables) — those exams fall back to
/// a uniform draw from the tagged pool.
Map<String, int>? mockMixFor(String examId) {
  switch (examId) {
    case 'kharidar':
      return {'Office Management & Public Service': 20};
    case 'nasu':
      return {'IQ & Reasoning': 20};
    case 'section-officer':
      return {'English': 20};
    default:
      return null;
  }
}

/// Question with the mock paper's per-question marks —
/// vanilla's `{...q, marks: p.marksPerQ}`.
Question withMarks(Question q, int marks) => Question(
      id: q.id,
      exam: q.exam,
      topic: q.topic,
      subtopic: q.subtopic,
      difficulty: q.difficulty,
      marks: marks,
      question: q.question,
      questionNe: q.questionNe,
      options: q.options,
      optionsNe: q.optionsNe,
      answer: q.answer,
      explanation: q.explanation,
      explanationNe: q.explanationNe,
      source: q.source,
    );

/// A built mock paper.
class MockPaper {
  /// The paper in presentation order, every question's marks already set
  /// to the spec's `marksPerQ`.
  final List<Question> questions;

  /// Questions tagged for the exam before the thin-bank fallback —
  /// vanilla's `tagged` (drives the honesty warning).
  final int taggedCount;

  /// Vanilla's thin-bank guard: the tagged pool was smaller than the
  /// paper, so the mock also draws from the general bank and does not
  /// mirror the real paper yet.
  final bool thinBank;

  const MockPaper({
    required this.questions,
    required this.taggedCount,
    required this.thinBank,
  });
}

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

/// Build the mock paper — vanilla `startMock` selection logic verbatim.
///
/// `allQuestions` is the full bank; the exam id is matched against each
/// question's `exam` tag list.
MockPaper buildMockPaper(
  String examId,
  MockSpec spec,
  List<Question> allQuestions, {
  Random? rng,
}) {
  final r = rng ?? Random();
  final tagged = allQuestions.where((q) => q.exam.contains(examId)).toList();
  final thin = tagged.length < spec.questionCount;
  // Thin-bank fallback: draw from the whole bank (vanilla's
  // `pool = QUESTIONS.slice()`).
  final pool = thin ? List<Question>.from(allQuestions) : tagged;
  final mix = mockMixFor(examId);

  List<Question> picked;
  if (mix != null) {
    // Vanilla: the mix draws from `rest` = the tagged pool only, never
    // from the thin fallback.
    final rest = tagged;
    picked = <Question>[];
    for (final entry in mix.entries) {
      picked.addAll(
        _shuffled(
          rest.where((q) => q.topic == entry.key).toList(),
          r,
        ).take(entry.value),
      );
    }
    final used = picked.map((q) => q.id).toSet();
    picked.addAll(
      _shuffled(
        rest.where((q) => !used.contains(q.id)).toList(),
        r,
      ).take(spec.questionCount - picked.length),
    );
    picked = _shuffled(picked, r);
  } else {
    picked = _shuffled(pool, r).take(spec.questionCount).toList();
  }

  final questions = picked.map((q) => withMarks(q, spec.marksPerQ)).toList();
  return MockPaper(
    questions: questions,
    taggedCount: tagged.length,
    thinBank: thin,
  );
}

/// Countdown display `MM:SS` — vanilla `fmtTime`.
String formatMockTime(int secs) {
  final s = secs < 0 ? 0 : secs;
  final m = s ~/ 60;
  final r = s % 60;
  return '${m.toString().padLeft(2, '0')}:${r.toString().padLeft(2, '0')}';
}

/// The exam-hall rule: instant feedback (correct/wrong + explanation) is
/// shown in practice, never during a mock. Answers stay hidden until the
/// paper is finished — vanilla `renderQuestion` only calls `showFeedback`
/// when `c.mode === 'practice'`.
bool shouldShowFeedback(String mode) => mode != 'mock';
