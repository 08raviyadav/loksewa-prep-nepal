/// Language switcher + default language tests (v1.0.9).
///
/// v1.0.8 bug: tapping the EN/NE toggle changed the stored preference
/// but nothing on screen changed until the app restarted — AppState
/// notified listeners, but the only rebuild path was an AnimatedBuilder
/// above MaterialApp, and the route contents sit behind a `const`
/// NetworkGate so Flutter short-circuited the update; the AppStateScope
/// InheritedWidget was created once and never notified its dependents.
/// The fix makes AppStateScope rebuild (and notify dependents) on every
/// AppState change. These tests pin that behaviour, plus the Nepali
/// default (v1.0.9) and persistence.
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/l10n/app_strings.dart';
import 'package:loksewa_vidyapeeth/l10n/topic_names.dart';
import 'package:loksewa_vidyapeeth/main.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  group('AppState language', () {
    test('no saved preference defaults to Nepali', () async {
      SharedPreferences.setMockInitialValues({});
      final state = AppState();
      await state.init();
      expect(state.lang, AppLang.ne);
      expect(state.isNe, isTrue);
    });

    test('a saved English preference wins over the Nepali default',
        () async {
      SharedPreferences.setMockInitialValues({'loksewa_lang_v1': 'en'});
      final state = AppState();
      await state.init();
      expect(state.lang, AppLang.en);
      expect(state.isNe, isFalse);
    });

    test('a saved Nepali preference is honoured', () async {
      SharedPreferences.setMockInitialValues({'loksewa_lang_v1': 'ne'});
      final state = AppState();
      await state.init();
      expect(state.lang, AppLang.ne);
    });

    test('setLang persists across a fresh AppState', () async {
      SharedPreferences.setMockInitialValues({});
      final first = AppState();
      await first.init();
      expect(first.lang, AppLang.ne);
      await first.setLang(AppLang.en);
      final second = AppState();
      await second.init();
      expect(second.lang, AppLang.en);
      await second.setLang(AppLang.ne);
      final third = AppState();
      await third.init();
      expect(third.lang, AppLang.ne);
    });
  });

  group('topic and difficulty labels', () {
    test('all 25 bank topics have a Nepali name', () {
      expect(topicNamesNe.length, 25);
      for (final entry in topicNamesNe.entries) {
        expect(entry.value, isNotEmpty);
        expect(entry.value, isNot(entry.key));
      }
    });

    test('topicLabel localizes in Nepali mode, English otherwise', () {
      expect(topicLabel('Nepal History', true), 'नेपालको इतिहास');
      expect(topicLabel('Nepal History', false), 'Nepal History');
      expect(topicLabel('Maths & Numerical', true), 'गणित तथा संख्यात्मक');
    });

    test('difficultyLabel localizes all three levels', () {
      expect(difficultyLabel('easy', true), 'सजिलो');
      expect(difficultyLabel('medium', true), 'मध्यम');
      expect(difficultyLabel('hard', true), 'गाह्रो');
      expect(difficultyLabel('medium', false), 'medium');
    });

    test('unknown values fall back to the English original', () {
      expect(topicLabel('Some New Topic', true), 'Some New Topic');
      expect(difficultyLabel('extreme', true), 'extreme');
      expect(topicLabel('', true), '');
    });
  });

  group('language switcher', () {
    /// Pumps the real RootNav (same shell as main.dart: AppStateScope
    /// above an AnimatedBuilder-driven MaterialApp), with the tour
    /// already done so no coachmark covers the app bar.
    Future<AppState> pumpApp(
      WidgetTester tester, {
      String? lang,
    }) async {
      SharedPreferences.setMockInitialValues({
        if (lang != null) 'loksewa_lang_v1': lang,
        'loksewa_tour_done_v1': true,
      });
      tester.view.physicalSize = const Size(480 * 3, 844 * 3);
      tester.view.devicePixelRatio = 3.0;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      final state = AppState();
      await state.init();
      await tester.runAsync(() async {
        await tester.pumpWidget(
          AppStateScope(
            state: state,
            child: AnimatedBuilder(
              animation: state,
              builder: (context, _) => MaterialApp(
                theme: buildAppTheme(),
                darkTheme: buildDarkTheme(),
                themeMode: state.themeMode,
                home: const RootNav(),
              ),
            ),
          ),
        );
        await Future<void>.delayed(const Duration(seconds: 2));
        await tester.pump();
      });
      // Bounded settling: the countdown card ticks every second, so
      // pumpAndSettle would never return.
      for (var i = 0; i < 10; i++) {
        await tester.pump(const Duration(milliseconds: 100));
      }
      return state;
    }

    testWidgets('the app opens in Nepali by default', (tester) async {
      await pumpApp(tester); // no saved preference
      expect(find.text('अभ्यास'), findsOneWidget); // Practice tab
      expect(find.text('होम'), findsOneWidget); // Home tab
      expect(find.text('Practice'), findsNothing);
      // The toggle offers English from Nepali mode.
      expect(find.text('EN'), findsOneWidget);
    });

    testWidgets('tapping the toggle switches the visible language',
        (tester) async {
      await pumpApp(tester, lang: 'en');
      expect(find.text('Practice'), findsOneWidget);
      expect(find.text('अभ्यास'), findsNothing);
      expect(find.text('NE'), findsOneWidget); // toggle offers Nepali

      // Tap NE: the whole UI — bottom nav AND the toggle label itself
      // — must switch to Nepali without a restart.
      await tester.tap(find.text('NE'));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));
      expect(find.text('अभ्यास'), findsOneWidget);
      expect(find.text('Practice'), findsNothing);
      expect(find.text('EN'), findsOneWidget);

      // Tap EN: back to English.
      await tester.tap(find.text('EN'));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));
      expect(find.text('Practice'), findsOneWidget);
      expect(find.text('अभ्यास'), findsNothing);
      expect(find.text('NE'), findsOneWidget);
    });

    testWidgets('a toggled language persists across a fresh AppState',
        (tester) async {
      final state = await pumpApp(tester, lang: 'en');
      await tester.tap(find.text('NE'));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));
      expect(state.lang, AppLang.ne);
      final fresh = AppState();
      await fresh.init();
      expect(fresh.lang, AppLang.ne);
    });
  });
}
