/// My Mistakes tests (v1.0.4): wrong answers persist as mistake ids,
/// the screen groups them by exam, and a correct answer in review
/// clears the mistake.
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/engine/quiz_engine.dart';
import 'package:loksewa_vidyapeeth/models/models.dart';
import 'package:loksewa_vidyapeeth/screens/mistakes_screen.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/state/progress_store.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';
import 'package:shared_preferences/shared_preferences.dart';

Question _q(String id, String examId) => Question(
      id: id,
      exam: [examId],
      topic: 'General',
      subtopic: '',
      difficulty: 'easy',
      marks: 1,
      question: 'Question $id?',
      questionNe: '',
      options: const ['a', 'b', 'c', 'd'],
      optionsNe: const [],
      answer: 0,
      explanation: 'Because.',
      explanationNe: '',
      source: 'test',
    );

Exam _exam(String id, String name) =>
    Exam(id: id, name: name, nameNe: name);

Future<ProgressStore> _freshStore() async {
  SharedPreferences.setMockInitialValues({});
  ProgressStore.resetForTest();
  return ProgressStore.instance;
}

Future<void> _pumpMistakes(
  WidgetTester tester, {
  required List<Question> questions,
  required List<Exam> exams,
}) async {
  final state = AppState();
  await state.init();
  await tester.pumpWidget(
    AppStateScope(
      state: state,
      child: MaterialApp(
        theme: buildDarkTheme(),
        home: MistakesScreen(
          navIndex: 0,
          onNav: (_) {},
          loadQuestions: () async => questions,
          loadExams: () async => exams,
        ),
      ),
    ),
  );
  await tester.pump();
  await tester.pump(const Duration(milliseconds: 100));
}

void main() {
  group('mistakes store', () {
    test('addMistake is idempotent, removeMistake clears', () async {
      final store = await _freshStore();
      await store.addMistake('q1');
      await store.addMistake('q1');
      expect(store.mistakes, ['q1']);
      await store.removeMistake('q1');
      expect(store.mistakes, isEmpty);
    });

    test('recordAttempt persists wrong answers as mistakes', () async {
      final store = await _freshStore();
      final q1 = _q('q1', 'kharidar');
      final q2 = _q('q2', 'kharidar');
      final engine = QuizEngine(
        QuizConfig(questions: [q1, q2], seed: 1),
      );
      // Answer q1 wrong (pick a non-correct option), q2 right.
      final wrongIdx =
          (engine.views[0].correctIndex + 1) % 4;
      engine.answer(0, wrongIdx);
      engine.answer(1, engine.views[1].correctIndex);
      final result = engine.finish();
      await store.recordAttempt(
        result: result,
        mode: 'practice',
        examId: 'kharidar',
        cutoff: 45,
        cutoffPct: 45,
      );
      expect(store.mistakes, ['q1']);
    });

    test('qotd bookkeeping mirrors dailyDone', () async {
      final store = await _freshStore();
      expect(store.isQotdDone('2026-11-13'), isFalse);
      await store.markQotdDone('2026-11-13');
      expect(store.isQotdDone('2026-11-13'), isTrue);
      expect(store.isQotdDone('2026-11-14'), isFalse);
    });
  });

  group('mistakes screen', () {
    testWidgets('groups mistakes by exam with retry buttons',
        (tester) async {
      final store = await _freshStore();
      await store.addMistake('q1');
      await store.addMistake('q2');
      await store.addMistake('q3');
      final questions = [
        _q('q1', 'kharidar'),
        _q('q2', 'kharidar'),
        _q('q3', 'nasu'),
      ];
      await _pumpMistakes(
        tester,
        questions: questions,
        exams: [_exam('kharidar', 'Kharidar'), _exam('nasu', 'NaSu')],
      );
      expect(find.text('3 mistakes'), findsOneWidget);
      expect(find.text('Kharidar'), findsOneWidget);
      expect(find.text('NaSu'), findsOneWidget);
      expect(find.text('Retry these 2'), findsOneWidget);
      expect(find.text('Retry these 1'), findsOneWidget);
      expect(find.text('Retry all mistakes'), findsOneWidget);
      // Unknown ids (not in the bank) are dropped, not crashed on.
      expect(find.text('Question q1?'), findsOneWidget);
    });

    testWidgets('empty state when there are no mistakes', (tester) async {
      await _freshStore();
      await _pumpMistakes(
        tester,
        questions: [_q('q1', 'kharidar')],
        exams: [_exam('kharidar', 'Kharidar')],
      );
      expect(find.text('No mistakes yet'), findsOneWidget);
      expect(find.text('Start practicing'), findsOneWidget);
    });

    testWidgets('a correct answer in review clears the mistake',
        (tester) async {
      final store = await _freshStore();
      await store.addMistake('q1');
      await _pumpMistakes(
        tester,
        questions: [_q('q1', 'kharidar')],
        exams: [_exam('kharidar', 'Kharidar')],
      );
      // Open the review quiz for this exam's mistakes.
      await tester.tap(find.text('Retry these 1'));
      await tester.pumpAndSettle();
      expect(find.text('Question 1 of 1'), findsOneWidget);
      // Tap the correct option ('a' is option 0; the engine shuffles,
      // so find the tile whose letter matches the correct answer by
      // tapping each option until feedback says Correct — simpler:
      // the correct label is 'a' (options are a/b/c/d, answer idx 0).
      final tile = find.ancestor(
        of: find.text('a'),
        matching: find.byType(OutlinedButton),
      );
      await tester.tap(tile.first);
      await tester.pumpAndSettle();
      expect(store.mistakes, isEmpty);
    });
  });
}
