/// First-launch tour tests (v1.0.7).
///
/// Covers the controller (start / advance / skip / complete +
/// persistence), the overlay (tooltip + Skip, tap-through to the real
/// button, dim strips swallowing taps, missing targets skipped
/// gracefully), and the full end-to-end flow over the real RootNav:
/// home -> Practice tab -> category -> exam -> topic -> Start.
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/data/data_repository.dart';
import 'package:loksewa_vidyapeeth/engine/exam_categories.dart';
import 'package:loksewa_vidyapeeth/main.dart';
import 'package:loksewa_vidyapeeth/onboarding/tour.dart';
import 'package:loksewa_vidyapeeth/screens/home_screen.dart';
import 'package:loksewa_vidyapeeth/screens/quiz/quiz_screen.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';
import 'package:shared_preferences/shared_preferences.dart';

List<TourStep> _twoSteps(GlobalKey key) => [
      TourStep(
        id: 'first',
        title: (_) => 'First step',
        body: (_) => 'Read this first.',
        targetKey: key,
      ),
      TourStep(
        id: 'tap',
        title: (_) => 'Tap it',
        body: (_) => 'Tap the button.',
        targetKey: key,
        advanceOnTap: true,
      ),
    ];

void main() {
  group('TourController', () {
    setUp(() => SharedPreferences.setMockInitialValues({}));

    test('start activates at step 0; next advances; next past last '
        'completes and persists', () async {
      final c = TourController(steps: _twoSteps(GlobalKey()));
      expect(c.isActive, isFalse);
      await c.start();
      expect(c.isActive, isTrue);
      expect(c.currentIndex, 0);
      expect(c.currentStep?.id, 'first');
      expect(c.stepCount, 2);
      c.next();
      expect(c.currentIndex, 1);
      expect(c.currentStep?.id, 'tap');
      c.next();
      expect(c.isActive, isFalse);
      expect(c.currentStep, isNull);
      await Future<void>.delayed(const Duration(milliseconds: 10));
      expect(await TourController.isTourDone(), isTrue);
    });

    test('start is a no-op when already running or already done',
        () async {
      final c = TourController(steps: _twoSteps(GlobalKey()));
      await c.start();
      c.next();
      await c.start(); // already running: stays on step 2
      expect(c.currentIndex, 1);
      await c.complete();
      final c2 = TourController(steps: _twoSteps(GlobalKey()));
      await c2.start(); // done flag set: does not activate
      expect(c2.isActive, isFalse);
    });

    test('advanceIfOn only advances on the matching step', () async {
      final c = TourController(steps: _twoSteps(GlobalKey()));
      await c.start();
      c.advanceIfOn('tap'); // wrong step: no-op
      expect(c.currentIndex, 0);
      c.advanceIfOn('first');
      expect(c.currentIndex, 1);
      c.advanceIfOn('first'); // now on 'tap': no-op
      expect(c.currentIndex, 1);
    });

    test('skip ends the tour and persists the done flag', () async {
      final c = TourController(steps: _twoSteps(GlobalKey()));
      await c.start();
      await c.skip();
      expect(c.isActive, isFalse);
      expect(await TourController.isTourDone(), isTrue);
    });

    test('completion persists across a fresh controller', () async {
      final c1 = TourController(steps: _twoSteps(GlobalKey()));
      await c1.start();
      await c1.complete();
      final c2 = TourController(steps: _twoSteps(GlobalKey()));
      await c2.start();
      expect(c2.isActive, isFalse);
    });

    test('replay clears the flag and restarts from step 1', () async {
      final c = TourController(steps: _twoSteps(GlobalKey()));
      await c.start();
      await c.complete();
      expect(await TourController.isTourDone(), isTrue);
      await c.replay();
      expect(c.isActive, isTrue);
      expect(c.currentIndex, 0);
      expect(await TourController.isTourDone(), isFalse);
    });
  });

  group('TourOverlay', () {
    /// Pumps a small shell: one target button + the overlay above it.
    Future<TourController> pumpShell(
      WidgetTester tester, {
      required List<TourStep> steps,
      required Widget target,
      ThemeMode themeMode = ThemeMode.light,
    }) async {
      SharedPreferences.setMockInitialValues({});
      final state = AppState();
      await state.init();
      final controller = TourController(steps: steps);
      await tester.pumpWidget(
        AppStateScope(
          state: state,
          child: TourScope(
            controller: controller,
            child: MaterialApp(
              theme: buildAppTheme(),
              darkTheme: buildDarkTheme(),
              themeMode: themeMode,
              home: Stack(
                children: [
                  Scaffold(body: Center(child: target)),
                  const Positioned.fill(child: TourOverlay()),
                ],
              ),
            ),
          ),
        ),
      );
      await tester.pump();
      return controller;
    }

    /// Starts the tour and lets the overlay's post-frame tick measure
    /// the target (one pump for the notify, one for the tick's
    /// setState).
    Future<void> startTour(
      WidgetTester tester,
      TourController controller,
    ) async {
      await controller.start();
      await tester.pump();
      await tester.pump();
    }

    testWidgets('renders tooltip, Skip, Next and step indicator',
        (tester) async {
      final key = GlobalKey();
      final controller = await pumpShell(
        tester,
        steps: _twoSteps(key),
        target: ElevatedButton(
          key: key,
          onPressed: () {},
          child: const Text('Target'),
        ),
      );
      await startTour(tester, controller);
      expect(find.text('First step'), findsOneWidget);
      expect(find.text('Read this first.'), findsOneWidget);
      expect(find.text('Skip'), findsOneWidget);
      expect(find.text('Next'), findsOneWidget);
      expect(find.text('1 / 2'), findsOneWidget);
    });

    testWidgets('Next advances to the next step', (tester) async {
      final key = GlobalKey();
      final controller = await pumpShell(
        tester,
        steps: _twoSteps(key),
        target: ElevatedButton(
          key: key,
          onPressed: () {},
          child: const Text('Target'),
        ),
      );
      await startTour(tester, controller);
      await tester.tap(find.text('Next'));
      await tester.pump();
      await tester.pump();
      expect(find.text('Tap it'), findsOneWidget);
      expect(find.text('2 / 2'), findsOneWidget);
      // Tap steps hide Next and show the tap hint instead.
      expect(find.text('Next'), findsNothing);
      expect(find.text('Tap the highlighted button'), findsOneWidget);
    });

    testWidgets('Skip ends the tour and sets the done flag',
        (tester) async {
      final key = GlobalKey();
      final controller = await pumpShell(
        tester,
        steps: _twoSteps(key),
        target: ElevatedButton(
          key: key,
          onPressed: () {},
          child: const Text('Target'),
        ),
      );
      await startTour(tester, controller);
      await tester.tap(find.text('Skip'));
      await tester.pump();
      expect(controller.isActive, isFalse);
      expect(find.text('First step'), findsNothing);
      await tester.pump(const Duration(milliseconds: 50));
      expect(await TourController.isTourDone(), isTrue);
    });

    testWidgets(
        'tapping the highlighted target fires its action and advances '
        '(tap-through)', (tester) async {
      var pressed = false;
      final key = GlobalKey();
      late final TourController controller;
      controller = await pumpShell(
        tester,
        steps: _twoSteps(key),
        target: ElevatedButton(
          key: key,
          onPressed: () {
            // Mirrors the real wiring: the button's own handler both
            // performs its action and advances the tour.
            pressed = true;
            controller.advanceIfOn('tap');
          },
          child: const Text('Target'),
        ),
      );
      await startTour(tester, controller);
      await tester.tap(find.text('Next')); // reach the tap step
      await tester.pump();
      await tester.pump();
      expect(find.text('Tap it'), findsOneWidget);
      // The tap lands on the real button THROUGH the overlay hole:
      // the dim strips cover everything except the target's rect.
      await tester.tap(find.text('Target'));
      await tester.pump();
      expect(pressed, isTrue);
      expect(controller.isActive, isFalse); // last step -> completed
      await tester.pump(const Duration(milliseconds: 50));
      expect(await TourController.isTourDone(), isTrue);
    });

    testWidgets('taps outside the highlight are swallowed by the dim',
        (tester) async {
      var pressed = false;
      final key = GlobalKey();
      final controller = await pumpShell(
        tester,
        steps: _twoSteps(key),
        target: ElevatedButton(
          key: key,
          onPressed: () => pressed = true,
          child: const Text('Target'),
        ),
      );
      await startTour(tester, controller);
      // Top-left corner: inside the top dim strip, far from the
      // centred button.
      await tester.tapAt(const Offset(10, 10));
      await tester.pump();
      expect(pressed, isFalse);
      expect(controller.isActive, isTrue);
      expect(controller.currentIndex, 0);
    });

    testWidgets('a step whose target never mounts is skipped, not a crash',
        (tester) async {
      final missingKey = GlobalKey(); // never attached to any widget
      final key = GlobalKey();
      final steps = [
        TourStep(
          id: 'gone',
          title: (_) => 'Gone',
          body: (_) => 'Nowhere.',
          targetKey: missingKey,
        ),
        TourStep(
          id: 'here',
          title: (_) => 'Here',
          body: (_) => 'Found.',
          targetKey: key,
        ),
      ];
      final controller = await pumpShell(
        tester,
        steps: steps,
        target: ElevatedButton(
          key: key,
          onPressed: () {},
          child: const Text('Target'),
        ),
      );
      await startTour(tester, controller);
      expect(find.text('Gone'), findsNothing); // nothing renders
      // Pump past the 300-frame grace period: the missing step is
      // skipped and the mounted step's tooltip appears.
      for (var i = 0; i < 310; i++) {
        await tester.pump(const Duration(milliseconds: 16));
      }
      expect(controller.currentIndex, 1);
      expect(find.text('Here'), findsOneWidget);
    });

    testWidgets('tooltip renders under the dark theme', (tester) async {
      final key = GlobalKey();
      final controller = await pumpShell(
        tester,
        steps: _twoSteps(key),
        target: ElevatedButton(
          key: key,
          onPressed: () {},
          child: const Text('Target'),
        ),
        themeMode: ThemeMode.dark,
      );
      await startTour(tester, controller);
      expect(find.text('First step'), findsOneWidget);
      expect(find.text('Skip'), findsOneWidget);
    });
  });

  group('tour end to end', () {
    /// Pumps the real RootNav with a TourScope + overlay, mirroring
    /// main.dart. Returns the controller so the test can observe it.
    Future<TourController> pumpRealApp(WidgetTester tester) async {
      SharedPreferences.setMockInitialValues({});
      tester.view.physicalSize = const Size(480 * 3, 844 * 3);
      tester.view.devicePixelRatio = 3.0;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      final state = AppState();
      await state.init();
      final tour = TourController();
      // Asset loads via rootBundle don't flush under the test's
      // fake-async clock, so every asset the tour touches is
      // pre-warmed with real async: the question index (topic chips)
      // and the first exam's question files (the final Start tap opens
      // a quiz from them).
      await tester.runAsync(() async {
        final repo = DataRepository();
        final exams = await repo.exams();
        await repo.examDates();
        await repo.historicalEvents();
        await repo.questionIndex();
        final firstExam = groupExams(exams).first.$2.first;
        await repo.questionsForExam(firstExam.id);
      });
      await tester.runAsync(() async {
        await tester.pumpWidget(
          AppStateScope(
            state: state,
            child: TourScope(
              controller: tour,
              child: AnimatedBuilder(
                animation: state,
                builder: (context, _) => MaterialApp(
                  theme: buildAppTheme(),
                  darkTheme: buildDarkTheme(),
                  themeMode: state.themeMode,
                  builder: (context, child) => Stack(
                    children: [
                      child!,
                      const Positioned.fill(child: TourOverlay()),
                    ],
                  ),
                  home: const RootNav(),
                ),
              ),
            ),
          ),
        );
        await Future<void>.delayed(const Duration(seconds: 2));
        await tester.pump();
      });
      await tester.pump(const Duration(milliseconds: 100));
      expect(find.byType(HomeScreen), findsOneWidget);
      return tour;
    }

    /// Bounded settling: the countdown card ticks every second, so
    /// pumpAndSettle would never return. Twenty 100ms pumps cover the
    /// 300ms scroll/expand animations, the cached repo loads, and the
    /// tour's viewport-stepped scroll-into-view (the test font makes
    /// the hero very tall, so the Daily Challenge card is several
    /// viewports down).
    Future<void> settle(WidgetTester tester) async {
      for (var i = 0; i < 20; i++) {
        await tester.pump(const Duration(milliseconds: 100));
      }
    }

    testWidgets('full tour: home -> practice -> exam -> topic -> start',
        (tester) async {
      final tour = await pumpRealApp(tester);
      // The tour auto-starts 600ms after the first frame (the 2s real
      // delay in pumpRealApp already covered it). The step-1 scroll
      // loop started during runAsync, so its retry timer runs on real
      // time — give it a beat before driving the frames.
      await tester.runAsync(
        () => Future<void>.delayed(const Duration(milliseconds: 300)),
      );
      await settle(tester);
      expect(tour.isActive, isTrue);
      expect(tour.currentIndex, 0);

      // Step 1: Daily Challenge card (Next step).
      expect(
        find.text('Start here every day — a fresh 10-question challenge.'),
        findsOneWidget,
      );
      expect(find.text('1 / 7'), findsOneWidget);
      await tester.tap(find.text('Next'));
      await settle(tester);

      // Step 2: Dashboard tab (Next step).
      expect(
        find.text('Track your XP, streak and badges here.'),
        findsOneWidget,
      );
      expect(find.text('2 / 7'), findsOneWidget);
      await tester.tap(find.text('Next'));
      await settle(tester);

      // Step 3: Practice tab (tap step — no Next button).
      expect(find.text('Tap Practice to study any exam.'), findsOneWidget);
      expect(find.text('3 / 7'), findsOneWidget);
      expect(find.text('Next'), findsNothing);
      // Tap the Practice tab by its icon — the tooltip title 'Practice'
      // duplicates the tab label, so the text finder is ambiguous.
      await tester.tap(find.byIcon(Icons.quiz_outlined));
      await settle(tester);

      // Step 4: first category tile (tap step).
      expect(find.text('Tap a category to see its exams.'), findsOneWidget);
      expect(find.text('4 / 7'), findsOneWidget);
      await tester.tap(find.byKey(TourKeys.firstCategory));
      await settle(tester);

      // Step 5: first exam chip (tap step).
      expect(find.text('Tap an exam to practise it.'), findsOneWidget);
      expect(find.text('5 / 7'), findsOneWidget);
      await tester.tap(find.byKey(TourKeys.firstExamChip));
      await settle(tester);

      // Step 6: first topic chip (tap step). The screen scrolls it
      // into view; ensureVisible is a no-op if it is already visible.
      expect(find.text('Choose a topic to practise.'), findsOneWidget);
      expect(find.text('6 / 7'), findsOneWidget);
      await tester.ensureVisible(find.byKey(TourKeys.firstTopicChip));
      await tester.pump();
      await tester.tap(find.byKey(TourKeys.firstTopicChip));
      await settle(tester);

      // Step 7: Start button (tap step).
      expect(find.text('Tap Start to begin the quiz.'), findsOneWidget);
      expect(find.text('7 / 7'), findsOneWidget);
      await tester.ensureVisible(find.byKey(TourKeys.startButton));
      await tester.pump();
      await tester.tap(find.byKey(TourKeys.startButton));
      await settle(tester);

      // The quiz opened and the tour completed + persisted.
      expect(find.byType(QuizScreen), findsOneWidget);
      expect(tour.isActive, isFalse);
      await tester.pump(const Duration(milliseconds: 50));
      expect(await TourController.isTourDone(), isTrue);
    });
  });
}
