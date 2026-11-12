/// Mock exam tests — spec resolution from prelim JSON, paper building
/// (vanilla `startMock` selection mix + thin-bank fallback), palette state
/// logic, the no-feedback-during-mock rule, and the auto-submit path.
library;

import 'dart:math';

import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/engine/mock_specs.dart';
import 'package:loksewa_vidyapeeth/engine/quiz_engine.dart';
import 'package:loksewa_vidyapeeth/models/models.dart';
import 'package:loksewa_vidyapeeth/screens/mock_exam_screen.dart';

Map<String, dynamic> _prelim({
  required int questions,
  required int? timeMin,
  required int marksPerQ,
  required num? negative,
  required int pass,
  required int total,
}) =>
    {
      'questions': questions,
      'timeMin': timeMin,
      'marksPerQ': marksPerQ,
      'negative': negative,
      'pass': pass,
      'total': total,
    };

Question _q(String id, List<String> exam, String topic, {int marks = 1}) =>
    Question(
      id: id,
      exam: exam,
      topic: topic,
      subtopic: '',
      difficulty: 'medium',
      marks: marks,
      question: 'Q $id',
      questionNe: '',
      options: const ['A', 'B', 'C', 'D'],
      optionsNe: const [],
      answer: 0,
      explanation: '',
      explanationNe: '',
      source: '',
    );

void main() {
  group('MockSpec.fromPrelim — vanilla prelim values', () {
    test('kharidar: 50Q / 45 min, 2 marks, 20% negative, cutoff 45', () {
      final spec = MockSpec.fromPrelim(
        'kharidar',
        _prelim(
          questions: 50,
          timeMin: 45,
          marksPerQ: 2,
          negative: 0.2,
          pass: 45,
          total: 100,
        ),
      );
      expect(spec.questionCount, 50);
      expect(spec.timeMin, 45);
      expect(spec.timed, isTrue);
      expect(spec.timeLimitSecs, 2700);
      expect(spec.negRate, 0.2);
      expect(spec.negativeApplied, isTrue);
      expect(spec.cutoff, 45);
      expect(spec.cutoffPct, 45);
      expect(spec.fullTotal, 100);
      expect(spec.marksPerQ, 2);
    });

    test('nasu: 50Q / 45 min, 2 marks, 20% negative, cutoff 45', () {
      final spec = MockSpec.fromPrelim(
        'nasu',
        _prelim(
          questions: 50,
          timeMin: 45,
          marksPerQ: 2,
          negative: 0.2,
          pass: 45,
          total: 100,
        ),
      );
      expect(spec.questionCount, 50);
      expect(spec.timeLimitSecs, 2700);
      expect(spec.negRate, 0.2);
      expect(spec.cutoffPct, 45);
      expect(spec.marksPerQ, 2);
    });

    test('section-officer: 100Q / 90 min, 1 mark, cutoff 45', () {
      final spec = MockSpec.fromPrelim(
        'section-officer',
        _prelim(
          questions: 100,
          timeMin: 90,
          marksPerQ: 1,
          negative: 0.2,
          pass: 45,
          total: 100,
        ),
      );
      expect(spec.questionCount, 100);
      expect(spec.timeMin, 90);
      expect(spec.timeLimitSecs, 5400);
      expect(spec.marksPerQ, 1);
      expect(spec.cutoffPct, 45);
    });

    test('tsc-primary: 50Q / 60 min, cutoff 50', () {
      final spec = MockSpec.fromPrelim(
        'tsc-primary',
        _prelim(
          questions: 50,
          timeMin: 60,
          marksPerQ: 2,
          negative: 0.2,
          pass: 50,
          total: 100,
        ),
      );
      expect(spec.questionCount, 50);
      expect(spec.timeMin, 60);
      expect(spec.cutoff, 50);
      expect(spec.cutoffPct, 50);
    });

    test('nrb-assistant: 50Q / 45 min, cutoff 40', () {
      final spec = MockSpec.fromPrelim(
        'nrb-assistant',
        _prelim(
          questions: 50,
          timeMin: 45,
          marksPerQ: 2,
          negative: 0.2,
          pass: 40,
          total: 100,
        ),
      );
      expect(spec.cutoff, 40);
      expect(spec.cutoffPct, 40);
    });

    test(
      'null timeMin (unverified) runs UNTIMED, null negative not applied',
      () {
        final spec = MockSpec.fromPrelim(
          'tsc-license',
          _prelim(
            questions: 50,
            timeMin: null,
            marksPerQ: 2,
            negative: null,
            pass: 50,
            total: 100,
          ),
        );
        expect(spec.timed, isFalse);
        expect(spec.timeLimitSecs, isNull);
        expect(spec.negRate, 0.0);
        expect(spec.negativeApplied, isFalse);
      },
    );

    test('negative 0 = no negative marking', () {
      final spec = MockSpec.fromPrelim(
        'nec-licence',
        _prelim(
          questions: 100,
          timeMin: 120,
          marksPerQ: 1,
          negative: 0,
          pass: 50,
          total: 100,
        ),
      );
      expect(spec.negRate, 0.0);
      expect(spec.negativeApplied, isFalse);
    });

    test('guide-only exam (no prelim) throws StateError', () {
      expect(() => MockSpec.fromPrelim('some-guide', null), throwsStateError);
    });

    test('cutoffPct uses JS Math.round semantics', () {
      // 45/100 = 45; a hypothetical 2/3 paper rounds 66.67 → 67.
      final spec = MockSpec.fromPrelim(
        'x',
        _prelim(
          questions: 3,
          timeMin: 10,
          marksPerQ: 1,
          negative: 0.2,
          pass: 2,
          total: 3,
        ),
      );
      expect(spec.cutoffPct, 67);
    });
  });

  group('exam id aliases', () {
    test('tsc-general resolves to tsc-primary', () {
      expect(resolveMockExamId('tsc-general'), 'tsc-primary');
    });
    test('unknown ids pass through', () {
      expect(resolveMockExamId('kharidar'), 'kharidar');
    });
  });

  group('mockMixFor — vanilla topic mixes', () {
    test('kharidar draws 20 Office Management & Public Service', () {
      expect(mockMixFor('kharidar'), {
        'Office Management & Public Service': 20,
      });
    });
    test('nasu draws 20 IQ & Reasoning', () {
      expect(mockMixFor('nasu'), {'IQ & Reasoning': 20});
    });
    test('section-officer draws 20 English', () {
      expect(mockMixFor('section-officer'), {'English': 20});
    });
    test('nrb-assistant falls back to a uniform draw', () {
      expect(mockMixFor('nrb-assistant'), isNull);
    });
  });

  group('buildMockPaper — vanilla startMock selection', () {
    test('topic mix: 20 topic questions + rest, all marks = marksPerQ', () {
      final bank = <Question>[
        for (var i = 0; i < 25; i++)
          _q(
            'omps-$i',
            const [
              'kharidar',
            ],
            'Office Management & Public Service',
          ),
        for (var i = 0; i < 40; i++)
          _q('gk-$i', const ['kharidar'], 'General Knowledge'),
      ];
      const spec = MockSpec(
        examId: 'kharidar',
        questionCount: 50,
        timeMin: 45,
        negRate: 0.2,
        cutoff: 45,
        cutoffPct: 45,
        fullTotal: 100,
        marksPerQ: 2,
      );
      final paper = buildMockPaper('kharidar', spec, bank, rng: Random(42));
      expect(paper.questions.length, 50);
      expect(paper.thinBank, isFalse);
      expect(paper.taggedCount, 65);
      // Vanilla's marks override: every paper question scores marksPerQ.
      expect(paper.questions.every((q) => q.marks == 2), isTrue);
      final topicCount = paper.questions
          .where((q) => q.topic == 'Office Management & Public Service')
          .length;
      // The mix guarantees at least 20; the "rest" refill (vanilla behavior)
      // can add more from the leftover tagged pool.
      expect(topicCount, greaterThanOrEqualTo(20));
      // No duplicates.
      final ids = paper.questions.map((q) => q.id).toSet();
      expect(ids.length, 50);
    });

    test('thin tagged pool falls back to the general bank', () {
      final bank = <Question>[
        for (var i = 0; i < 10; i++)
          _q('nrb-$i', const ['nrb-assistant'], 'Banking'),
        for (var i = 0; i < 100; i++) _q('gen-$i', const ['kharidar'], 'GK'),
      ];
      const spec = MockSpec(
        examId: 'nrb-assistant',
        questionCount: 50,
        timeMin: 45,
        negRate: 0.2,
        cutoff: 40,
        cutoffPct: 40,
        fullTotal: 100,
        marksPerQ: 2,
      );
      final paper = buildMockPaper('nrb-assistant', spec, bank, rng: Random(7));
      expect(paper.questions.length, 50);
      expect(paper.taggedCount, 10);
      expect(paper.thinBank, isTrue);
      // The fallback draws untagged questions too.
      expect(
        paper.questions.any((q) => !q.exam.contains('nrb-assistant')),
        isTrue,
      );
      final ids = paper.questions.map((q) => q.id).toSet();
      expect(ids.length, 50);
    });

    test('mix path with thin tagged pool draws from tagged only (vanilla)', () {
      // Vanilla's mix branch always draws from the tagged pool, never the
      // thin-bank fallback — a short tagged pool yields a short paper.
      final bank = <Question>[
        for (var i = 0; i < 12; i++)
          _q('k-$i', const ['kharidar'], 'Office Management & Public Service'),
        for (var i = 0; i < 200; i++) _q('gen-$i', const ['nasu'], 'GK'),
      ];
      const spec = MockSpec(
        examId: 'kharidar',
        questionCount: 50,
        timeMin: 45,
        negRate: 0.2,
        cutoff: 45,
        cutoffPct: 45,
        fullTotal: 100,
        marksPerQ: 2,
      );
      final paper = buildMockPaper('kharidar', spec, bank, rng: Random(3));
      expect(paper.thinBank, isTrue);
      expect(paper.questions.length, 12);
      expect(paper.questions.every((q) => q.exam.contains('kharidar')), isTrue);
    });
  });

  group('formatMockTime', () {
    test('MM:SS with zero padding', () {
      expect(formatMockTime(0), '00:00');
      expect(formatMockTime(65), '01:05');
      expect(formatMockTime(300), '05:00');
      expect(formatMockTime(2700), '45:00');
      expect(formatMockTime(5400), '90:00');
    });
    test('negative clamps to zero', () {
      expect(formatMockTime(-5), '00:00');
    });
  });

  group('no-feedback-during-mock rule', () {
    test('mock mode never shows instant feedback', () {
      expect(shouldShowFeedback('mock'), isFalse);
    });
    test('practice mode still shows instant feedback', () {
      expect(shouldShowFeedback('practice'), isTrue);
    });
  });

  group('paletteCellState', () {
    test('precedence: current > answered > flagged > unanswered', () {
      expect(
        paletteCellState(answered: true, current: true, flagged: true),
        PaletteState.current,
      );
      expect(
        paletteCellState(answered: true, current: false, flagged: true),
        PaletteState.answered,
      );
      expect(
        paletteCellState(answered: false, current: false, flagged: true),
        PaletteState.flagged,
      );
      expect(
        paletteCellState(answered: false, current: false, flagged: false),
        PaletteState.unanswered,
      );
    });
  });

  group('MockSession', () {
    MockSession makeSession({int? timeMin}) {
      final qs = [
        for (var i = 0; i < 5; i++)
          _q('q$i', const ['kharidar'], 'GK', marks: 2),
      ];
      final spec = MockSpec(
        examId: 'kharidar',
        questionCount: 5,
        timeMin: timeMin,
        negRate: 0.2,
        cutoff: 45,
        cutoffPct: 45,
        fullTotal: 100,
        marksPerQ: 2,
      );
      final engine = QuizEngine(
        QuizConfig(
          questions: qs,
          negOn: true,
          negRate: 0.2,
          timerOn: spec.timed,
          timeLimitSecs: spec.timeLimitSecs,
          mode: 'mock',
          examId: 'kharidar',
        ),
      );
      return MockSession(engine: engine, spec: spec, bank: qs);
    }

    test('recordAnswer updates answered/unanswered counts', () {
      final s = makeSession();
      expect(s.answeredCount, 0);
      expect(s.unansweredCount, 5);
      s.recordAnswer(1);
      expect(s.answeredCount, 1);
      expect(s.unansweredCount, 4);
      // Re-tapping overwrites (vanilla mock answerOption).
      s.recordAnswer(2);
      expect(s.answeredCount, 1);
      expect(s.engine.answers[0], 2);
    });

    test('toggleFlag flags and unflags the current question', () {
      final s = makeSession();
      expect(s.isFlagged(0), isFalse);
      expect(s.toggleFlag(), isTrue);
      expect(s.isFlagged(0), isTrue);
      expect(s.toggleFlag(), isFalse);
      expect(s.isFlagged(0), isFalse);
    });

    test('tick auto-submits at zero and records timedOut', () {
      final s = makeSession(timeMin: 1); // 60-second paper
      expect(s.timerOn, isTrue);
      var hitZero = false;
      for (var i = 0; i < 59; i++) {
        expect(s.tick(), isFalse);
      }
      hitZero = s.tick();
      expect(hitZero, isTrue);
      expect(s.timedOut, isTrue);
      expect(s.finished, isTrue);
      expect(s.timeLeft, 0);
      // Further ticks are inert after finishing.
      expect(s.tick(), isFalse);
    });

    test('untimed session never ticks to zero', () {
      final s = makeSession();
      expect(s.timerOn, isFalse);
      expect(s.tick(), isFalse);
      expect(s.timedOut, isFalse);
    });

    test('engine finish carries the timedOut flag into the result', () {
      final s = makeSession(timeMin: 1);
      for (var i = 0; i < 60; i++) {
        s.tick();
      }
      final result = s.engine.finish(secs: 60, timedOut: s.timedOut);
      expect(result.timedOut, isTrue);
      expect(result.skipped, 5);
    });

    test('negative marking uses the spec rate', () {
      final s = makeSession();
      // Answer every question wrong (correct index is 0, pick 1).
      for (var i = 0; i < 5; i++) {
        s.index = i;
        // Options are shuffled per attempt — pick a guaranteed-wrong one.
        final wrongOpt = (s.engine.views[i].correctIndex + 1) % 4;
        s.recordAnswer(wrongOpt);
      }
      final result = s.engine.finish();
      // 5 wrong × 2 marks × 0.2 = −2.0.
      expect(result.score, -2.0);
      expect(result.wrong, 5);
    });
  });
}
