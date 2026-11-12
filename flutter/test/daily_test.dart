/// Daily content determinism tests (v1.0.4): the Daily Challenge set
/// and the Question of the Day are seeded from the calendar date, so
/// every user gets the same content on the same day.
library;

import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/gamification/daily.dart';
import 'package:loksewa_vidyapeeth/models/models.dart';

Question _q(String id) => Question(
      id: id,
      exam: const ['kharidar'],
      topic: 'General',
      subtopic: '',
      difficulty: 'easy',
      marks: 1,
      question: 'Q $id?',
      questionNe: '',
      options: const ['a', 'b', 'c', 'd'],
      optionsNe: const [],
      answer: 0,
      explanation: '',
      explanationNe: '',
      source: 'test',
    );

void main() {
  group('pickDailyChallenge', () {
    final pool = List.generate(100, (i) => _q('q$i'));

    test('same seed gives the same 10 questions', () {
      final a = pickDailyChallenge(pool, '2026-11-13');
      final b = pickDailyChallenge(pool, '2026-11-13');
      expect(a, hasLength(10));
      expect(
        a.map((q) => q.id).toList(),
        b.map((q) => q.id).toList(),
      );
    });

    test('different days give different sets', () {
      final a = pickDailyChallenge(pool, '2026-11-13');
      final b = pickDailyChallenge(pool, '2026-11-14');
      expect(
        a.map((q) => q.id).toList(),
        isNot(b.map((q) => q.id).toList()),
      );
    });

    test('a small pool returns what exists, never more', () {
      final small = List.generate(4, (i) => _q('s$i'));
      expect(pickDailyChallenge(small, '2026-11-13'), hasLength(4));
    });
  });

  group('pickQuestionOfTheDay', () {
    final pool = List.generate(100, (i) => _q('q$i'));

    test('same seed gives the same question', () {
      final a = pickQuestionOfTheDay(pool, '2026-11-13');
      final b = pickQuestionOfTheDay(pool, '2026-11-13');
      expect(a, isNotNull);
      expect(a!.id, b!.id);
    });

    test('different days usually give a different question', () {
      // Two fixed days, verified distinct (a 1-in-100 coincidence
      // would fail the test — the seeds below are checked by the run).
      final a = pickQuestionOfTheDay(pool, '2026-11-13');
      final b = pickQuestionOfTheDay(pool, '2026-11-14');
      expect(a!.id, isNot(b!.id));
    });

    test('empty pool returns null', () {
      expect(pickQuestionOfTheDay(const [], '2026-11-13'), isNull);
    });
  });
}
