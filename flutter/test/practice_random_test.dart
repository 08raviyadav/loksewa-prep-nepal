/// Random mode + sticky Start bar tests (v1.0.16).
///
/// Picking an exam turns Random on (every topic, mixed) and pins a
/// Start bar above the bottom nav, so the user starts in one tap
/// instead of scrolling to the bottom of the picker to choose a topic
/// first. Picking specific topics turns Random off; tapping Random
/// again clears the picks. Deep-links ("Practice this chapter") still
/// pre-select their topic with Random off.
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/data/data_repository.dart';
import 'package:loksewa_vidyapeeth/onboarding/tour.dart';
import 'package:loksewa_vidyapeeth/screens/practice_screen.dart';
import 'package:loksewa_vidyapeeth/screens/quiz/quiz_screen.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// iPhone 14 / Pixel-class viewport, logical pixels.
const _phone = Size(390, 844);

/// Bottom edge of the content area (screen minus the bottom nav bar).
final _contentBottom = _phone.height - kBottomNavigationBarHeight;

Future<void> _setPhoneSize(WidgetTester tester) async {
  tester.view.physicalSize = Size(_phone.width * 3, _phone.height * 3);
  tester.view.devicePixelRatio = 3.0;
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);
}

/// Pre-warms the repository caches with real async (asset loads via
/// rootBundle don't flush under the test's fake-async clock) and
/// returns the AppState for [_pumpScreen]. The question index is
/// pre-warmed too: topic counts come from it, so the Random / topic
/// chips appear after a few pumps instead of never.
Future<AppState> _prewarm(
  WidgetTester tester, {
  bool warmPool = false,
}) async {
  // English pinned (the default is Nepali, v1.0.9).
  SharedPreferences.setMockInitialValues({'loksewa_lang_v1': 'en'});
  final state = AppState();
  await state.init();
  await tester.runAsync(() async {
    final repo = DataRepository();
    await repo.exams();
    await repo.questionIndex();
    if (warmPool) await repo.questionsForExam('kharidar');
  });
  return state;
}

Future<void> _pumpScreen(
  WidgetTester tester,
  AppState state,
  Widget screen,
) async {
  // AppStateScope sits ABOVE MaterialApp (not in `home`): pushed
  // routes (the QuizScreen that Start opens) are siblings of `home`,
  // so a scope inside `home` would leave them without AppState.
  await tester.pumpWidget(
    AppStateScope(
      state: state,
      child: AnimatedBuilder(
        animation: state,
        builder: (context, _) => MaterialApp(
          theme: buildAppTheme(),
          home: Builder(builder: (context) => screen),
        ),
      ),
    ),
  );
  for (var i = 0; i < 20; i++) {
    await tester.pump(const Duration(milliseconds: 50));
    if (find.byType(CircularProgressIndicator).evaluate().isEmpty) break;
  }
  expect(find.byType(CircularProgressIndicator), findsNothing);
}

Widget _practice() => PracticeScreen(
      navIndex: 1,
      onNav: (_) {},
      onStart: (_) {},
    );

/// Picks Kharidar (expand the Lok Sewa section, tap the chip) and
/// scrolls the topic chips into view. The list builds lazily, so the
/// chips don't exist until scrolled to — the loop pumps (letting the
/// topic load finish from the pre-warmed index) and steps down the
/// list until the Random chip is built and visible.
Future<void> _pickKharidar(WidgetTester tester) async {
  await tester.tap(find.text('Lok Sewa (PSC)  ·  14'));
  await tester.pumpAndSettle();
  await tester.tap(find.text('Kharidar'));
  for (var i = 0; i < 30; i++) {
    await tester.pump(const Duration(milliseconds: 50));
    if (find.text('🎲 Random').evaluate().isNotEmpty) break;
    await tester.drag(find.byType(ListView), const Offset(0, -300));
  }
  await tester.pump();
  expect(find.text('🎲 Random'), findsOneWidget);
}

/// Whether the FilterChip labelled [label] is currently selected.
bool _chipSelected(WidgetTester tester, String label) {
  final chip = tester.widget<FilterChip>(
    find.widgetWithText(FilterChip, label),
  );
  return chip.selected;
}

/// Kharidar's topic counts from the pre-warmed index (data-driven, so
/// the expectations survive bank updates).
Future<Map<String, int>> _kharidarCounts() =>
    DataRepository().topicCountsFor('kharidar');

void main() {
  group('Practice Random mode', () {
    testWidgets('Random is selected by default after picking an exam',
        (tester) async {
      await _setPhoneSize(tester);
      final state = await _prewarm(tester);
      await _pumpScreen(tester, state, _practice());
      await _pickKharidar(tester);

      final counts = await _kharidarCounts();
      final firstTopic = counts.keys.first;
      final firstLabel = '$firstTopic (${counts[firstTopic]})';

      expect(find.text('🎲 Random'), findsOneWidget);
      expect(_chipSelected(tester, '🎲 Random'), isTrue);
      // No specific topic picked.
      expect(_chipSelected(tester, firstLabel), isFalse);
    });

    testWidgets('Start is enabled immediately after picking an exam',
        (tester) async {
      await _setPhoneSize(tester);
      final state = await _prewarm(tester);
      await _pumpScreen(tester, state, _practice());

      // No exam picked yet: no bar, no Start button.
      expect(find.byKey(TourKeys.startButton), findsNothing);

      await tester.tap(find.text('Lok Sewa (PSC)  ·  14'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Kharidar'));
      await tester.pump();

      // The bar appears as soon as the exam is picked — before the
      // topics have even loaded — and Start is already enabled.
      final button = tester.widget<FilledButton>(
        find.byKey(TourKeys.startButton),
      );
      expect(button.onPressed, isNotNull);
      // Pinned above the bottom nav, not below the fold: reachable
      // without scrolling.
      final rect = tester.getRect(find.byKey(TourKeys.startButton));
      expect(rect.bottom, lessThan(_contentBottom));
      // Exactly one Start button on the screen (the old in-list
      // button is gone).
      expect(find.text('Start'), findsOneWidget);
    });

    testWidgets('tapping a specific topic turns Random off',
        (tester) async {
      await _setPhoneSize(tester);
      final state = await _prewarm(tester);
      await _pumpScreen(tester, state, _practice());
      await _pickKharidar(tester);

      final counts = await _kharidarCounts();
      final firstTopic = counts.keys.first;
      final firstLabel = '$firstTopic (${counts[firstTopic]})';

      expect(_chipSelected(tester, '🎲 Random'), isTrue);
      await tester.ensureVisible(find.text(firstLabel));
      await tester.pump();
      await tester.tap(find.text(firstLabel));
      await tester.pump();
      expect(_chipSelected(tester, '🎲 Random'), isFalse);
      expect(_chipSelected(tester, firstLabel), isTrue);
    });

    testWidgets('tapping Random clears the selected topics',
        (tester) async {
      await _setPhoneSize(tester);
      final state = await _prewarm(tester);
      await _pumpScreen(tester, state, _practice());
      await _pickKharidar(tester);

      final counts = await _kharidarCounts();
      final topics = counts.keys.toList();
      final firstLabel = '${topics[0]} (${counts[topics[0]]})';
      final secondLabel = '${topics[1]} (${counts[topics[1]]})';

      await tester.ensureVisible(find.text(firstLabel));
      await tester.pump();
      await tester.tap(find.text(firstLabel));
      await tester.pump();
      await tester.ensureVisible(find.text(secondLabel));
      await tester.pump();
      await tester.tap(find.text(secondLabel));
      await tester.pump();
      expect(_chipSelected(tester, firstLabel), isTrue);
      expect(_chipSelected(tester, secondLabel), isTrue);
      expect(_chipSelected(tester, '🎲 Random'), isFalse);

      // The Random chip may have scrolled off-screen while picking
      // topics — bring it back before tapping it.
      await tester.ensureVisible(find.text('🎲 Random'));
      await tester.pump();
      await tester.tap(find.text('🎲 Random'));
      await tester.pump();
      expect(_chipSelected(tester, '🎲 Random'), isTrue);
      expect(_chipSelected(tester, firstLabel), isFalse);
      expect(_chipSelected(tester, secondLabel), isFalse);
    });

    testWidgets('sticky bar shows the right summary and updates',
        (tester) async {
      await _setPhoneSize(tester);
      final state = await _prewarm(tester);
      await _pumpScreen(tester, state, _practice());
      await _pickKharidar(tester);

      final counts = await _kharidarCounts();
      final total = counts.values.fold(0, (a, b) => a + b);
      final topics = counts.keys.toList();
      final firstLabel = '${topics[0]} (${counts[topics[0]]})';
      final secondLabel = '${topics[1]} (${counts[topics[1]]})';

      // Random on: exam name + Random + whole-pool count. The exam
      // title finder is scoped to the bar — the exam chip in the list
      // shows the same text.
      expect(
        find.descendant(
          of: find.byKey(const ValueKey('stickyStartBar')),
          matching: find.text('Kharidar'),
        ),
        findsOneWidget,
      );
      expect(find.text('Random · $total questions'), findsOneWidget);

      // One topic: singular "1 topic" + that topic's count.
      await tester.ensureVisible(find.text(firstLabel));
      await tester.pump();
      await tester.tap(find.text(firstLabel));
      await tester.pump();
      expect(
        find.text('1 topic · ${counts[topics[0]]} questions'),
        findsOneWidget,
      );
      expect(find.text('Random · $total questions'), findsNothing);

      // Two topics: "2 topics" + combined count.
      await tester.ensureVisible(find.text(secondLabel));
      await tester.pump();
      await tester.tap(find.text(secondLabel));
      await tester.pump();
      final two = counts[topics[0]]! + counts[topics[1]]!;
      expect(find.text('2 topics · $two questions'), findsOneWidget);
    });

    testWidgets('starting with Random opens a quiz from the whole pool',
        (tester) async {
      await _setPhoneSize(tester);
      final state = await _prewarm(tester, warmPool: true);
      await _pumpScreen(tester, state, _practice());
      await _pickKharidar(tester);
      expect(_chipSelected(tester, '🎲 Random'), isTrue);

      await tester.tap(find.byKey(TourKeys.startButton));
      for (var i = 0; i < 20; i++) {
        await tester.pump(const Duration(milliseconds: 100));
        if (find.byType(QuizScreen).evaluate().isNotEmpty) break;
      }
      expect(find.byType(QuizScreen), findsOneWidget);
      expect(find.text('Question 1 of 10'), findsOneWidget);

      // Repository level: topics:null is the whole pool, strictly
      // larger than any single topic's pool — so the Random quiz
      // really draws from every topic, not a subset.
      final repo = DataRepository();
      final whole = await repo.questionsForExam('kharidar');
      final one = await repo.questionsForExam(
        'kharidar',
        topics: {'Constitution & Governance'},
      );
      expect(one.length, greaterThan(0));
      expect(whole.length, greaterThan(one.length));
    });

    testWidgets('deep-link initialTopic selects that topic, Random off',
        (tester) async {
      await _setPhoneSize(tester);
      final state = await _prewarm(tester);
      final exams = await DataRepository().exams();
      final kharidar = exams.firstWhere((e) => e.id == 'kharidar');
      await _pumpScreen(
        tester,
        state,
        PracticeScreen(
          navIndex: 1,
          onNav: (_) {},
          initialExam: kharidar,
          initialTopic: 'Constitution & Governance',
          onStart: (_) {},
        ),
      );
      // Topics load after the first frame (initialExam triggers
      // _loadTopics in initState), and the list builds lazily — so
      // pump and step down the list until the Random chip appears.
      for (var i = 0; i < 30; i++) {
        await tester.pump(const Duration(milliseconds: 50));
        if (find.text('🎲 Random').evaluate().isNotEmpty) break;
        await tester.drag(find.byType(ListView), const Offset(0, -300));
      }
      await tester.pump();
      expect(find.text('🎲 Random'), findsOneWidget);

      final counts = await _kharidarCounts();
      final topicLabel =
          'Constitution & Governance (${counts['Constitution & Governance']})';
      expect(_chipSelected(tester, '🎲 Random'), isFalse);
      expect(_chipSelected(tester, topicLabel), isTrue);
      // Start enabled, summary narrowed to the one topic.
      final button = tester.widget<FilledButton>(
        find.byKey(TourKeys.startButton),
      );
      expect(button.onPressed, isNotNull);
      expect(
        find.text(
          '1 topic · ${counts['Constitution & Governance']} questions',
        ),
        findsOneWidget,
      );
    });
  });
}
