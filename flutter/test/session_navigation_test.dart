/// Session navigation tests (v1.0.13).
///
/// Reported 2026-11-14: (1) back from the score screen walked back
/// through the questions instead of going Home; (2) back mid-session
/// left silently with no exit prompt; (3) the bottom nav bar vanished
/// during a session. Now: back on the result screen goes Home with no
/// confirmation; back mid-session asks before leaving; the bottom nav
/// stays visible during quiz/mock/result; tab taps mid-session ask
/// before closing the session and switching tabs.
///
/// The harness mimics RootNav: a tabbed home page whose onNav pops to
/// the first route and switches tabs (RootNav._popAndGo), with a log of
/// every tab switch so tests can prove where navigation landed.
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:loksewa_vidyapeeth/data/data_repository.dart';
import 'package:loksewa_vidyapeeth/engine/quiz_engine.dart';
import 'package:loksewa_vidyapeeth/models/models.dart';
import 'package:loksewa_vidyapeeth/screens/mock_exam_screen.dart';
import 'package:loksewa_vidyapeeth/screens/quiz/quiz_screen.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';

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

/// Minimal RootNav stand-in: four tab pages, a Start button on Home,
/// and an onNav that pops to the first route then switches tabs.
class _Harness extends StatefulWidget {
  final List<int> navLog;
  const _Harness({required this.navLog});

  @override
  State<_Harness> createState() => _HarnessState();
}

class _HarnessState extends State<_Harness> {
  int _tab = 0;

  void _onNav(int i) {
    Navigator.of(context).popUntil((route) => route.isFirst);
    widget.navLog.add(i);
    setState(() => _tab = i);
  }

  void _startQuiz({required int count}) {
    final questions =
        [_q('Q1', 0), _q('Q2', 1), _q('Q3', 2)].take(count).toList();
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => QuizScreen(
          config: QuizConfig(
            questions: questions,
            examId: 'kharidar',
            nepali: false,
          ),
          meta: const QuizMeta(
            examName: 'Kharidar',
            cutoff: 45,
            cutoffPct: 45,
            fullTotal: 100,
          ),
          navIndex: _tab,
          onNav: _onNav,
        ),
      ),
    );
  }

  void _startMock() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => MockExamScreen(
          examId: 'kharidar',
          navIndex: 2,
          onNav: _onNav,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    const pages = ['HOME PAGE', 'PRACTICE PAGE', 'MOCK PAGE', 'DASHBOARD PAGE'];
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(pages[_tab]),
            if (_tab == 0) ...[
              FilledButton(
                onPressed: () => _startQuiz(count: 3),
                child: const Text('Start quiz'),
              ),
              FilledButton(
                onPressed: () => _startQuiz(count: 1),
                child: const Text('Start 1Q quiz'),
              ),
              FilledButton(
                onPressed: _startMock,
                child: const Text('Start mock'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

Future<List<int>> _pumpHarness(WidgetTester tester) async {
  SharedPreferences.setMockInitialValues({'loksewa_lang_v1': 'en'});
  tester.view.physicalSize = const Size(480 * 3, 844 * 3);
  tester.view.devicePixelRatio = 3.0;
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);
  final state = AppState();
  await state.init();
  final navLog = <int>[];
  await tester.pumpWidget(
    AppStateScope(
      state: state,
      child: AnimatedBuilder(
        animation: state,
        builder: (context, _) => MaterialApp(
          theme: buildAppTheme(),
          home: _Harness(navLog: navLog),
        ),
      ),
    ),
  );
  await tester.pumpAndSettle();
  return navLog;
}

/// Taps the on-screen option tile whose label is [label].
Future<void> _tapOption(WidgetTester tester, String label) async {
  final tile = find.ancestor(
    of: find.text(label),
    matching: find.byType(OutlinedButton),
  );
  await tester.tap(tile.first);
  await tester.pumpAndSettle();
}

/// Finishes the 1-question quiz — lands on the result screen.
Future<void> _finish1QQuiz(WidgetTester tester) async {
  await _tapOption(tester, '1'); // Q1 correct (answer idx 0)
  await tester.scrollUntilVisible(
    find.text('Finish'),
    400,
    scrollable: find.byType(Scrollable).first,
  );
  await tester.pumpAndSettle();
  await tester.tap(find.text('Finish'));
  await tester.pumpAndSettle();
  await tester.tap(find.text('Submit'));
  await tester.pumpAndSettle();
}

void main() {
  testWidgets(
    'mid-quiz back asks before leaving; cancel stays, exit goes home',
    (WidgetTester tester) async {
      final navLog = await _pumpHarness(tester);
      await tester.tap(find.text('Start quiz'));
      await tester.pumpAndSettle();
      expect(find.text('Question 1 of 3'), findsOneWidget);

      // System back is vetoed by the quiz PopScope and shows the dialog.
      await tester.binding.handlePopRoute();
      await tester.pump();
      expect(find.text('Exit practice session?'), findsOneWidget);

      // Cancel stays in the quiz.
      await tester.tap(find.text('Cancel'));
      await tester.pumpAndSettle();
      expect(find.text('Question 1 of 3'), findsOneWidget);
      expect(find.text('Exit practice session?'), findsNothing);

      // Back again, this time Exit — the session ends and we go Home.
      await tester.binding.handlePopRoute();
      await tester.pump();
      await tester.tap(find.text('Exit'));
      await tester.pumpAndSettle();
      expect(find.text('Question 1 of 3'), findsNothing);
      expect(find.text('HOME PAGE'), findsOneWidget);
      expect(navLog, contains(0));
    },
  );

  testWidgets(
    'bottom nav stays visible during quiz; tab tap asks before switching',
    (WidgetTester tester) async {
      final navLog = await _pumpHarness(tester);
      await tester.tap(find.text('Start quiz'));
      await tester.pumpAndSettle();

      // The bar is visible mid-session, with the same four tabs.
      final bar = find.byType(BottomNavigationBar);
      expect(bar, findsOneWidget);
      expect(
        find.descendant(of: bar, matching: find.text('Practice')),
        findsOneWidget,
      );
      expect(
        find.descendant(of: bar, matching: find.text('Mock Exams')),
        findsOneWidget,
      );

      // Tapping Practice asks first; Cancel stays in the quiz.
      await tester.tap(
        find.descendant(of: bar, matching: find.text('Practice')),
      );
      await tester.pump();
      expect(find.text('Go to Practice?'), findsOneWidget);
      await tester.tap(find.text('Cancel'));
      await tester.pumpAndSettle();
      expect(find.text('Question 1 of 3'), findsOneWidget);

      // Confirming closes the session and switches to Practice.
      await tester.tap(
        find.descendant(of: bar, matching: find.text('Practice')),
      );
      await tester.pump();
      await tester.tap(find.text('Go'));
      await tester.pumpAndSettle();
      expect(find.text('Question 1 of 3'), findsNothing);
      expect(find.text('PRACTICE PAGE'), findsOneWidget);
      expect(navLog, contains(1));
    },
  );

  testWidgets(
    'result screen back goes home, never back to the questions',
    (WidgetTester tester) async {
      final navLog = await _pumpHarness(tester);
      await tester.tap(find.text('Start 1Q quiz'));
      await tester.pumpAndSettle();
      await _finish1QQuiz(tester);
      expect(find.text('✅ PASS'), findsOneWidget);

      // System back on the result screen: no dialog, straight Home.
      await tester.binding.handlePopRoute();
      await tester.pumpAndSettle();
      expect(find.text('Exit practice session?'), findsNothing);
      expect(find.text('✅ PASS'), findsNothing);
      expect(find.text('What is Q1?'), findsNothing);
      expect(find.text('HOME PAGE'), findsOneWidget);
      expect(navLog, contains(0));
    },
  );

  testWidgets(
    'result screen tab tap navigates directly, no dialog',
    (WidgetTester tester) async {
      final navLog = await _pumpHarness(tester);
      await tester.tap(find.text('Start 1Q quiz'));
      await tester.pumpAndSettle();
      await _finish1QQuiz(tester);
      expect(find.text('✅ PASS'), findsOneWidget);

      // The bar is visible on the result screen too.
      final bar = find.byType(BottomNavigationBar);
      expect(bar, findsOneWidget);
      await tester.tap(
        find.descendant(of: bar, matching: find.text('Mock Exams')),
      );
      await tester.pumpAndSettle();
      expect(find.text('Go to Mock Exams?'), findsNothing);
      expect(find.text('✅ PASS'), findsNothing);
      expect(find.text('MOCK PAGE'), findsOneWidget);
      expect(navLog, contains(2));
    },
  );

  testWidgets(
    'mock runner back asks before leaving; bar stays visible',
    (WidgetTester tester) async {
      final navLog = await _pumpHarness(tester);
      // Pre-warm the assets MockExamScreen._load reads (rootBundle only
      // resolves under real async), then push inside runAsync so the
      // load completes before we tap Start.
      await tester.runAsync(() async {
        await DataRepository().exams();
        await DataRepository().questions(
          'constitution-governance-economy.json',
        );
      });
      await tester.runAsync(() async {
        await tester.tap(find.text('Start mock'));
        await Future<void>.delayed(const Duration(seconds: 2));
        await tester.pump();
      });
      await tester.pump();
      expect(find.text('Start mock exam'), findsOneWidget);
      await tester.tap(find.text('Start mock exam'));
      // Fixed pumps from here: the runner's 1s countdown timer never
      // settles, so pumpAndSettle would time out.
      await tester.pump();

      // The palette sits at the bottom of the runner's ListView and the
      // first question is drawn at random, so the content above it varies
      // in height — on a long draw the palette starts below the fold and
      // finders skip offstage widgets, so the assert below would fail
      // (CI run #250 failed exactly this way; a probe measured the
      // palette's list offset at 598–746px against a 723px viewport).
      // Scroll it into view first: the scroll offset persists for the
      // rest of the test, so the later palette checks need no re-scroll.
      // scrollUntilVisible uses fixed pumps only, so the countdown
      // timer cannot break it — and no amount of pumping alone would
      // help, since pumping never scrolls.
      await tester.scrollUntilVisible(
        find.text('Question palette'),
        400,
        scrollable: find.byType(Scrollable).first,
      );
      await tester.pump();

      // The bar is visible mid-mock, and the runner is up.
      expect(find.byType(BottomNavigationBar), findsOneWidget);
      expect(find.text('Question palette'), findsOneWidget);

      // System back asks; Stay keeps the mock running.
      await tester.binding.handlePopRoute();
      await tester.pump(const Duration(milliseconds: 300));
      expect(find.text('Leave this mock?'), findsOneWidget);
      await tester.tap(find.text('Stay'));
      await tester.pump();
      expect(find.text('Question palette'), findsOneWidget);

      // Tab tap mid-mock asks too (mock wording); Cancel stays.
      final bar = find.byType(BottomNavigationBar);
      await tester.tap(
        find.descendant(of: bar, matching: find.text('Dashboard')),
      );
      await tester.pump(const Duration(milliseconds: 300));
      expect(find.text('Go to Dashboard?'), findsOneWidget);
      await tester.tap(find.text('Cancel'));
      await tester.pump();
      expect(find.text('Question palette'), findsOneWidget);

      // Back again, Leave this time — the mock ends and we go Home.
      // Pump until the runner leaves the tree: the dialog's pop must
      // finish before the exit navigation even starts, and the route
      // pop takes ~300ms after that. pumpAndSettle is unusable here
      // (the countdown timer never settles), so poll with fixed pumps.
      await tester.binding.handlePopRoute();
      await tester.pump(const Duration(milliseconds: 300));
      await tester.tap(find.text('Leave'));
      for (var i = 0;
          i < 10 && find.text('Question palette').evaluate().isNotEmpty;
          i++) {
        await tester.pump(const Duration(milliseconds: 300));
      }
      expect(find.text('Question palette'), findsNothing);
      expect(find.text('HOME PAGE'), findsOneWidget);
      expect(navLog, contains(0));
    },
  );
}
