// Full quiz flow: answer -> scroll -> Next advances -> Finish -> ResultScreen.
// Note: the quiz body is a ListView, so off-screen widgets (nav buttons
// after the feedback card expands) have no element until scrolled into view.
// Tests must scrollUntilVisible before tapping them.
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:plugin_platform_interface/plugin_platform_interface.dart';
import 'package:share_plus_platform_interface/share_plus_platform_interface.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:loksewa_vidyapeeth/engine/quiz_engine.dart';
import 'package:loksewa_vidyapeeth/models/models.dart';
import 'package:loksewa_vidyapeeth/screens/quiz/quiz_screen.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';

/// Records what the app tries to share, instead of opening the sheet.
class _FakeSharePlatform extends Fake
    with MockPlatformInterfaceMixin
    implements SharePlatform {
  final shared = <String>[];

  @override
  Future<ShareResult> share(ShareParams params) async {
    shared.add(params.text ?? '');
    return const ShareResult('', ShareResultStatus.success);
  }
}

/// Swaps in the fake share platform for one test. Must run before the
/// first SharePlus.instance access (it captures the platform once).
_FakeSharePlatform _useFakeShare() {
  final fake = _FakeSharePlatform();
  final real = SharePlatform.instance;
  SharePlatform.instance = fake;
  addTearDown(() => SharePlatform.instance = real);
  return fake;
}

Question _q(String id, int answer) => Question(
      id: id,
      exam: const ['kharidar'],
      topic: 'Mathematics',
      subtopic: '',
      difficulty: 'easy',
      marks: 2,
      question: 'What is $id?',
      questionNe: '$id के हो?',
      options: const ['1', '2', '3', '4'],
      optionsNe: const ['१', '२', '३', '४'],
      answer: answer,
      explanation: 'Because.',
      explanationNe: 'किनभने।',
      source: 'test',
    );

Future<void> _pumpQuiz(
  WidgetTester tester, {
  String lang = 'en', // flow tests pin English (default is Nepali, v1.0.9)
  bool nepali = false, // quiz-config language flag (v1.0.9)
}) async {
  SharedPreferences.setMockInitialValues({'loksewa_lang_v1': lang});
  final state = AppState();
  await state.init();
  final questions = [_q('Q1', 0), _q('Q2', 1), _q('Q3', 2)];
  await tester.pumpWidget(
    // Mirror main.dart: AppStateScope sits ABOVE MaterialApp so pushed
    // routes (e.g. ResultScreen) can still resolve AppStateScope.of.
    AppStateScope(
      state: state,
      child: AnimatedBuilder(
        animation: state,
        builder: (context, _) => MaterialApp(
          theme: buildAppTheme(),
          home: QuizScreen(
            config: QuizConfig(
              questions: questions,
              examId: 'kharidar',
              nepali: nepali,
            ),
            meta: const QuizMeta(
              examName: 'Kharidar',
              cutoff: 45,
              cutoffPct: 45,
              fullTotal: 100,
            ),
          ),
        ),
      ),
    ),
  );
  await tester.pumpAndSettle();
}

/// Taps the on-screen option tile whose label is [label].
Future<void> _tapOption(WidgetTester tester, String label) async {
  // The option tile shows the label text; tap the tile's OutlinedButton.
  final tile = find.ancestor(
    of: find.text(label),
    matching: find.byType(OutlinedButton),
  );
  await tester.tap(tile.first);
  await tester.pumpAndSettle();
}

Future<void> _tapNext(WidgetTester tester) async {
  await tester.scrollUntilVisible(
    find.text('Next'),
    400,
    scrollable: find.byType(Scrollable).first,
  );
  await tester.pumpAndSettle();
  await tester.tap(find.text('Next'));
  await tester.pumpAndSettle();
}

void main() {
  testWidgets('answering then Next advances to question 2', (
    WidgetTester tester,
  ) async {
    await _pumpQuiz(tester);
    expect(find.text('Question 1 of 3'), findsOneWidget);

    await _tapOption(tester, '1');
    // Feedback appears.
    expect(find.textContaining('Correct'), findsOneWidget);

    await _tapNext(tester);
    expect(find.text('Question 2 of 3'), findsOneWidget);
  });

  testWidgets('finishing shows the result screen with a score', (
    WidgetTester tester,
  ) async {
    await _pumpQuiz(tester);
    await _finishQuiz(tester);
    // Result screen: percentage shown, and counts add up (1 correct,
    // 1 wrong, 1 skipped).
    expect(find.textContaining('%'), findsWidgets);
  });

  testWidgets('Nepali mode shows options_ne and localized chips', (
    WidgetTester tester,
  ) async {
    // v1.0.9: the engine shuffles options_ne when the quiz starts in
    // Nepali mode — this locks in the behaviour the v1.0.10 data fix
    // (translating the ~981 untranslated options_ne) builds on.
    await _pumpQuiz(tester, lang: 'ne', nepali: true);
    // Devanagari options (shuffled, all four present), no English ones.
    expect(find.text('१'), findsOneWidget);
    expect(find.text('२'), findsOneWidget);
    expect(find.text('३'), findsOneWidget);
    expect(find.text('४'), findsOneWidget);
    expect(find.text('1'), findsNothing);
    // Localized chips: Mathematics -> गणित, easy -> सजिलो.
    expect(find.text('गणित'), findsOneWidget);
    expect(find.text('सजिलो'), findsOneWidget);
    expect(find.text('Mathematics'), findsNothing);
    expect(find.text('easy'), findsNothing);
    // Nepali question text.
    expect(find.text('Q1 के हो?'), findsOneWidget);
  });

  testWidgets('English mode shows English options and chips', (
    WidgetTester tester,
  ) async {
    await _pumpQuiz(tester, lang: 'en', nepali: false);
    expect(find.text('1'), findsOneWidget);
    expect(find.text('१'), findsNothing);
    expect(find.text('Mathematics'), findsOneWidget);
    expect(find.text('easy'), findsOneWidget);
    expect(find.text('गणित'), findsNothing);
    expect(find.text('सजिलो'), findsNothing);
  });

  testWidgets('result screen share button shares the score + app link', (
    WidgetTester tester,
  ) async {
    final fake = _useFakeShare();
    await _pumpQuiz(tester);
    await _finishQuiz(tester);
    await tester.scrollUntilVisible(
      find.text('Share score'),
      400,
      scrollable: find.byType(Scrollable).first,
    );
    await tester.pumpAndSettle();
    await tester.tap(find.text('Share score'));
    await tester.pumpAndSettle();
    expect(fake.shared, hasLength(1));
    expect(fake.shared.single, contains('scored'));
    expect(fake.shared.single, contains('Kharidar'));
    expect(fake.shared.single, contains('app-release.apk'));
  });
}

/// Answers Q1 correct, Q2 wrong, skips Q3, then finishes — lands on the
/// result screen.
Future<void> _finishQuiz(WidgetTester tester) async {
  // Q1 correct (answer idx 0 -> label '1'), Q2 wrong (tap '1', answer idx 1),
  // Q3 skip via Skip button.
  await _tapOption(tester, '1');
  await _tapNext(tester);
  await _tapOption(tester, '1');
  await _tapNext(tester);
  // Q3: scroll to Skip and tap it (skip keeps zero, never a mistake).
  await tester.scrollUntilVisible(
    find.text('Skip'),
    400,
    scrollable: find.byType(Scrollable).first,
  );
  await tester.pumpAndSettle();
  await tester.tap(find.text('Skip'));
  await tester.pumpAndSettle();

  // Finish -> confirm dialog -> confirm.
  await tester.scrollUntilVisible(
    find.text('Finish'),
    400,
    scrollable: find.byType(Scrollable).first,
  );
  await tester.pumpAndSettle();
  await tester.tap(find.text('Finish'));
  await tester.pumpAndSettle();
  // Confirm in the dialog (its confirm button says "Submit").
  await tester.tap(find.text('Submit'));
  await tester.pumpAndSettle();
}
