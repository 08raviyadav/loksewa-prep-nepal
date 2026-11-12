/// About + Privacy screen tests (v1.0.2).
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/screens/about_screen.dart';
import 'package:loksewa_vidyapeeth/screens/privacy_screen.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';

Future<void> _pump(WidgetTester tester, Widget screen) async {
  SharedPreferences.setMockInitialValues({});
  tester.view.physicalSize = const Size(390 * 3, 844 * 3);
  tester.view.devicePixelRatio = 3.0;
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);
  PackageInfo.setMockInitialValues(
    appName: 'LokSewa Vidyapeeth',
    packageName: 'com.raviyadav.loksewa_vidyapeeth',
    version: '1.0.2',
    buildNumber: '3',
    buildSignature: '',
  );
  final state = AppState();
  await state.init();
  // Pump inside runAsync: the About screen's stats load exams.json and
  // exam-dates.json via rootBundle, which only resolves under real
  // async (same as RootNav in the drawer tests).
  await tester.runAsync(() async {
    await tester.pumpWidget(
      AppStateScope(
        state: state,
        child: MaterialApp(
          theme: buildDarkTheme(),
          home: screen,
        ),
      ),
    );
    await Future<void>.delayed(const Duration(seconds: 2));
    await tester.pump();
  });
  await tester.pump(const Duration(milliseconds: 100));
  await tester.pump(const Duration(milliseconds: 100));
}

void main() {
  group('about screen', () {
    testWidgets('shows version, tagline, links and data sources',
        (tester) async {
      await _pump(
        tester,
        AboutScreen(navIndex: 0, onNav: (_) {}),
      );
      expect(find.text('LokSewa Vidyapeeth'), findsOneWidget);
      expect(find.text('Version 1.0.2 (3)'), findsOneWidget);
      expect(
        find.textContaining('Free Lok Sewa exam preparation'),
        findsOneWidget,
      );
      expect(find.text('Made in Nepal'), findsOneWidget);

      // Live counts from the bundled data (47 exams, 82 exam dates).
      // Asserted BEFORE any scrolling: once the list scrolls down,
      // the stats row scrolls off the top and the lazy ListView
      // disposes it.
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pump(const Duration(milliseconds: 500));
      expect(find.text('47'), findsOneWidget);
      expect(find.text('82'), findsOneWidget);

      expect(find.text('raviyadav.com.np'), findsOneWidget);
      expect(
        find.text('github.com/08raviyadav/loksewa-prep-nepal'),
        findsOneWidget,
      );
      // The third link tile sits below the fold once the stats row
      // loads — scroll to it (same lazily-built ListView as the
      // drawer).
      await tester.scrollUntilVisible(
        find.text('Open-source licences'),
        200,
      );
      expect(find.text('Open-source licences'), findsOneWidget);

      // Data sources sit below the fold — scroll to them.
      await tester.scrollUntilVisible(
        find.text('Data sources'),
        200,
      );
      expect(
        find.textContaining('Public Service Commission'),
        findsOneWidget,
      );
      await tester.scrollUntilVisible(
        find.text('Created by Ravi Yadav'),
        200,
      );
      expect(find.text('Created by Ravi Yadav'), findsOneWidget);
    });
  });

  group('privacy screen', () {
    testWidgets('shows the policy sections', (tester) async {
      await _pump(
        tester,
        PrivacyScreen(navIndex: 0, onNav: (_) {}),
      );
      expect(find.text('Privacy Policy'), findsOneWidget);
      expect(
        find.text('Last updated: 12 November 2026'),
        findsOneWidget,
      );
      expect(find.text('What we collect'), findsOneWidget);
      expect(find.textContaining('no accounts'), findsOneWidget);

      await tester.scrollUntilVisible(find.text('Contact'), 200);
      expect(find.text('Reminders'), findsOneWidget);
      expect(find.text('Changes to this policy'), findsOneWidget);
      expect(find.text('Contact'), findsOneWidget);
    });
  });
}
