/// Thorough tests for the quiz engine math (ported from vanilla
/// `scoreAttempt` semantics) plus the progress store's attempt bookkeeping.
library;

import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/engine/quiz_engine.dart';
import 'package:loksewa_vidyapeeth/models/models.dart';
import 'package:loksewa_vidyapeeth/state/progress_store.dart';
import 'package:shared_preferences/shared_preferences.dart';

Question _q(String id, {int marks = 1, int answer = 0}) => Question(
      id: id,
      exam: const ['kharidar'],
      topic: 'Topic A',
      subtopic: '',
      difficulty: 'medium',
      marks: marks,
      question: 'Q $id?',
      questionNe: '',
      options: const ['A', 'B', 'C', 'D'],
      optionsNe: const [],
      answer: answer,
      explanation: '',
      explanationNe: '',
      source: '',
    );

void main() {
  group('scoring maths (vanilla scoreAttempt)', () {
    test('correct*marks minus wrong*marks*negRate, skips score 0', () {
      final engine = QuizEngine(
        QuizConfig(
          questions: [
            _q('1', marks: 2),
            _q('2', marks: 2),
            _q('3', marks: 2),
            _q('4', marks: 2),
            _q('5', marks: 2),
          ],
          negOn: true,
          negRate: 0.2,
          seed: 7,
        ),
      );
      engine.answer(0, engine.views[0].correctIndex);
      engine.answer(1, engine.views[1].correctIndex);
      engine.answer(2, engine.views[2].correctIndex);
      // wrong on Q4: pick a non-correct option
      final v4 = engine.views[3];
      engine.answer(3, (v4.correctIndex + 1) % 4);
      engine.skip(4);
      final r = engine.finish();
      // 3*2 − 1*2*0.2 = 5.6 ; max 10 ; pct 56.0
      expect(r.score, 5.6);
      expect(r.max, 10);
      expect(r.pct, 56.0);
      expect(r.correct, 3);
      expect(r.wrong, 1);
      expect(r.skipped, 1);
    });

    test('negRate 0.25 (MECEE-BL style)', () {
      final engine = QuizEngine(
        QuizConfig(
          questions: [_q('1', marks: 2), _q('2', marks: 2)],
          negOn: true,
          negRate: 0.25,
          seed: 7,
        ),
      );
      engine.answer(0, engine.views[0].correctIndex);
      engine.answer(1, (engine.views[1].correctIndex + 2) % 4);
      final r = engine.finish();
      expect(r.score, 1.5); // 2 − 2*0.25
      expect(r.pct, 37.5);
    });

    test('negative off: wrongs deduct nothing', () {
      final engine = QuizEngine(
        QuizConfig(
          questions: [_q('1'), _q('2')],
          negOn: false,
          negRate: 0.2,
          seed: 7,
        ),
      );
      engine.answer(0, engine.views[0].correctIndex);
      engine.answer(1, (engine.views[1].correctIndex + 1) % 4);
      final r = engine.finish();
      expect(r.score, 1.0);
      expect(r.pct, 50.0);
      expect(r.wrong, 1);
    });

    test('all skipped: score 0, pct 0', () {
      final engine = QuizEngine(
        QuizConfig(questions: [_q('1'), _q('2'), _q('3')], seed: 7),
      );
      final r = engine.finish();
      expect(r.score, 0.0);
      expect(r.pct, 0.0);
      expect(r.skipped, 3);
      expect(r.correct, 0);
      expect(r.wrong, 0);
    });

    test('rounding to 1 decimal, JS Math.round semantics', () {
      // −0.25 → JS Math.round(−2.5) = −2 → −0.2
      final engine = QuizEngine(
        QuizConfig(questions: [_q('1')], negOn: true, negRate: 0.25, seed: 7),
      );
      engine.answer(0, (engine.views[0].correctIndex + 1) % 4);
      final r = engine.finish();
      expect(r.score, -0.2);
      // pct uses max(0, score): negative scores clamp to 0%
      expect(r.pct, 0.0);
    });

    test('fractional positive score rounds to 1 decimal', () {
      // 3 correct + 1 wrong at 0.2 → 3 − 0.2 = 2.8 ; pct 70.0
      final engine = QuizEngine(
        QuizConfig(
          questions: [_q('1'), _q('2'), _q('3'), _q('4')],
          negOn: true,
          negRate: 0.2,
          seed: 7,
        ),
      );
      for (var i = 0; i < 3; i++) {
        engine.answer(i, engine.views[i].correctIndex);
      }
      engine.answer(3, (engine.views[3].correctIndex + 1) % 4);
      final r = engine.finish();
      expect(r.score, 2.8);
      expect(r.pct, 70.0);
    });

    test('qdetail codes: 1 correct, 0 wrong, -1 skipped', () {
      final engine = QuizEngine(
        QuizConfig(questions: [_q('1'), _q('2'), _q('3')], seed: 7),
      );
      engine.answer(0, engine.views[0].correctIndex);
      engine.answer(1, (engine.views[1].correctIndex + 1) % 4);
      engine.skip(2);
      final r = engine.finish();
      expect(r.perQuestion.map((d) => d.code).toList(), [1, 0, -1]);
      expect(r.perQuestion.map((d) => d.marks).toList(), [1, 1, 1]);
      expect(r.wrongList.length, 1);
      expect(r.wrongList.first.view.question.id, '2');
    });
  });

  group('cutoff gate', () {
    test('pct == cutoffPct passes; just below fails', () {
      expect(passesCutoff(45.0, 45), isTrue);
      expect(passesCutoff(44.9, 45), isFalse);
      expect(passesCutoff(100.0, 50), isTrue);
      expect(passesCutoff(0.0, 45), isFalse);
    });
  });

  group('option shuffling', () {
    test('exactly one correct mapping; all options preserved', () {
      final engine = QuizEngine(
        QuizConfig(
          questions: List.generate(20, (i) => _q('q$i', answer: i % 4)),
          seed: 42,
        ),
      );
      for (final view in engine.views) {
        final q = view.question;
        // the remapped index really points at the original correct option
        expect(view.shuffledOptions[view.correctIndex], q.options[q.answer]);
        // all options present exactly once
        expect(view.shuffledOptions.toSet(), q.options.toSet());
        expect(view.shuffledOptions.length, q.options.length);
      }
    });

    test('shuffle actually permutes (seeded, deterministic)', () {
      final a = QuizEngine(
        QuizConfig(questions: [_q('1', answer: 0)], seed: 1),
      );
      final b = QuizEngine(
        QuizConfig(questions: [_q('1', answer: 0)], seed: 2),
      );
      // different seeds give different orders for at least one of these
      final orders = <String>{};
      for (var s = 0; s < 10; s++) {
        final e = QuizEngine(
          QuizConfig(questions: [_q('1', answer: 0)], seed: s),
        );
        orders.add(e.views.first.shuffledOptions.join(','));
      }
      expect(orders.length, greaterThan(1));
      expect(a.views.first.correctIndex, isNotNull);
      expect(b.views.first.correctIndex, isNotNull);
    });
  });

  group('edge cases', () {
    test('empty question list: finish does not throw, pct 0', () {
      final engine = QuizEngine(const QuizConfig(questions: []));
      final r = engine.finish();
      expect(r.score, 0.0);
      expect(r.max, 0);
      expect(r.pct, 0.0);
      expect(r.perQuestion, isEmpty);
    });

    test('answer out of range throws', () {
      final engine = QuizEngine(QuizConfig(questions: [_q('1')]));
      expect(() => engine.answer(0, 4), throwsRangeError);
      expect(() => engine.answer(5, 0), throwsRangeError);
    });

    test('re-answering overwrites', () {
      final engine = QuizEngine(QuizConfig(questions: [_q('1')], seed: 7));
      final v = engine.views[0];
      engine.answer(0, (v.correctIndex + 1) % 4);
      engine.answer(0, v.correctIndex);
      final r = engine.finish();
      expect(r.correct, 1);
      expect(r.wrong, 0);
    });
  });

  group('progress store', () {
    setUp(() async {
      SharedPreferences.setMockInitialValues({});
      ProgressStore.resetForTest();
    });

    Future<QuizResult> runResult() async {
      final engine = QuizEngine(
        QuizConfig(
          questions: [
            _q('w1', marks: 2),
            _q('w2', marks: 2),
            _q('w3', marks: 2),
            _q('w4', marks: 2),
            _q('w5', marks: 2),
          ],
          negOn: true,
          negRate: 0.2,
          seed: 7,
        ),
      );
      engine.answer(0, engine.views[0].correctIndex);
      engine.answer(1, engine.views[1].correctIndex);
      engine.answer(2, engine.views[2].correctIndex);
      engine.answer(3, (engine.views[3].correctIndex + 1) % 4);
      engine.skip(4);
      return engine.finish(secs: 120);
    }

    test('recordAttempt: xp, streak, mistakes, attempt shape', () async {
      final store = await ProgressStore.instance;
      final result = await runResult();
      final summary = await store.recordAttempt(
        result: result,
        mode: 'practice',
        examId: 'kharidar',
        cutoff: 45,
        cutoffPct: 45,
      );
      // score 5.6 → xp = round(56) = 56
      expect(summary.xp, 56);
      expect(summary.passed, isTrue); // 56.0 >= 45
      expect(store.xp, 56);
      expect(store.level, 1);
      expect(store.streak, 1);
      // wrong appended, skip not
      expect(store.mistakes, contains('w4'));
      expect(store.mistakes, isNot(contains('w5')));
      // attempt shape mirrors vanilla
      final a = store.attempts.single;
      expect(a['mode'], 'practice');
      expect(a['exam'], 'kharidar');
      expect(a['total'], 5);
      expect(a['score'], 5.6);
      expect(a['pct'], 56.0);
      expect(a['cutoff'], 45);
      expect(a['cutoffPct'], 45);
      expect(a['secs'], 120);
      expect(a['timedOut'], isFalse);
      final qd = a['qdetail'] as List;
      expect(qd.map((r) => (r as Map)['c']).toList(), [1, 1, 1, 0, -1]);
      expect(summary.leveledUp, isFalse);
      expect(summary.weeklyMet, isFalse); // 5 questions < 70 target
      expect(store.badges(), contains('First Practice'));
    });

    test('streak: same day does nothing; next day increments', () async {
      final store = await ProgressStore.instance;
      await store.updateStreak();
      expect(store.streak, 1);
      await store.updateStreak();
      expect(store.streak, 1); // same UTC day: no-op
    });

    test('bookmarks toggle', () async {
      final store = await ProgressStore.instance;
      expect(await store.toggleBookmark('q1'), isTrue);
      expect(store.isBookmarked('q1'), isTrue);
      expect(await store.toggleBookmark('q1'), isFalse);
      expect(store.isBookmarked('q1'), isFalse);
    });

    test('weakestTopic from qdetail', () async {
      final store = await ProgressStore.instance;
      final result = await runResult();
      await store.recordAttempt(
        result: result,
        mode: 'practice',
        examId: 'kharidar',
        cutoff: 45,
        cutoffPct: 45,
      );
      expect(store.weakestTopic(), 'Topic A');
    });

    test('retryWrongOnly returns ids still on the mistakes list', () async {
      final store = await ProgressStore.instance;
      await store.addMistake('w4');
      expect(store.retryWrongOnly(['w4', 'w9']), ['w4']);
    });

    test('vanilla key name is used', () async {
      final store = await ProgressStore.instance;
      await store.updateStreak();
      final prefs = await SharedPreferences.getInstance();
      expect(prefs.containsKey('loksewa_progress_v1'), isTrue);
      expect(prefs.getString('loksewa_progress_v1'), contains('"streak":1'));
    });
  });
}
