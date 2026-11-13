/// Layout tests for the v1.0.1 picker rework (Practice + Mock tabs).
///
/// v1.0.0 shipped both tabs as one long flat list — 47 exam chips on
/// Practice, 33 full mock cards on Mock Exams — so anything near the
/// bottom took many screens of scrolling to reach. Both tabs are now
/// search + collapsible category sections + compact rows. These tests
/// pin the new layout on a 390×844 phone viewport: the section headers
/// all fit on one screen, search narrows to matches only, and tapping
/// a mock row opens its detail sheet.
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/data/data_repository.dart';
import 'package:loksewa_vidyapeeth/screens/mock_list_screen.dart';
import 'package:loksewa_vidyapeeth/screens/practice_screen.dart';
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

/// Pumps [screen] with real bundled exams.json. Asset loads via
/// rootBundle don't flush under the test's fake-async clock, so the
/// repository cache is pre-warmed with real async first
/// (same pattern as exam_dates_test.dart). Both screens read exams
/// through the repository, so one pre-warm covers both.
Future<void> _pump(
  WidgetTester tester,
  Widget screen, {
  Map<String, Object> prefs = const {},
}) async {
  SharedPreferences.setMockInitialValues(prefs);
  final state = AppState();
  await state.init();
  await tester.runAsync(() async {
    await DataRepository().exams();
  });
  await tester.pumpWidget(
    AnimatedBuilder(
      animation: state,
      builder: (context, _) => MaterialApp(
        theme: buildAppTheme(),
        home: AppStateScope(
          state: state,
          child: Builder(builder: (context) => screen),
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

Widget _mocks() => MockListScreen(navIndex: 2, onNav: (_) {});

void main() {
  group('Practice picker', () {
    testWidgets('category headers replace the flat 47-chip list',
        (tester) async {
      await _setPhoneSize(tester);
      await _pump(tester, _practice());
      expect(find.text('Lok Sewa (PSC)  ·  14'), findsOneWidget);
      expect(find.text('Teaching (TSC)  ·  4'), findsOneWidget);
      expect(find.text('Health Licences  ·  16'), findsOneWidget);
      expect(find.text('Banking  ·  4'), findsOneWidget);
      // Nothing expanded yet: no exam chips on screen.
      expect(find.text('Kharidar'), findsNothing);
      // All 8 headers fit on one screen — no scrolling to see them.
      final last = tester.getRect(find.text('Public Enterprises  ·  2'));
      expect(last.bottom, lessThan(_contentBottom));
    });

    testWidgets('expanding a section reveals only its exams', (tester) async {
      await _setPhoneSize(tester);
      await _pump(tester, _practice());
      await tester.tap(find.text('Lok Sewa (PSC)  ·  14'));
      await tester.pumpAndSettle();
      expect(find.text('Kharidar'), findsOneWidget);
      expect(find.text('Nayab Subba (NaSu)'), findsOneWidget);
      // Other sections stay collapsed.
      expect(find.text('TSC — Primary Teacher'), findsNothing);
    });

    testWidgets('search filters to matching exams only', (tester) async {
      await _setPhoneSize(tester);
      await _pump(tester, _practice());
      await tester.enterText(find.byType(TextField), 'TSC');
      await tester.pumpAndSettle();
      expect(find.text('TSC — Primary Teacher'), findsOneWidget);
      expect(find.text('TSC — Secondary Teacher'), findsOneWidget);
      expect(find.text('TSC — Lower Secondary Teacher'), findsOneWidget);
      expect(find.text('TSC Teaching Licence Exam'), findsOneWidget);
      expect(find.text('Kharidar'), findsNothing);
      expect(find.text('Lok Sewa (PSC)  ·  14'), findsNothing);
    });

    testWidgets('search with no matches shows the empty state', (tester) async {
      await _setPhoneSize(tester);
      await _pump(tester, _practice());
      await tester.enterText(find.byType(TextField), 'zzz-no-such-exam');
      await tester.pumpAndSettle();
      expect(find.text('No exams match your search.'), findsOneWidget);
    });

    testWidgets('recent exams show above the categories', (tester) async {
      await _setPhoneSize(tester);
      await _pump(
        tester,
        _practice(),
        prefs: const {
          'loksewa_recent_exams_v1': ['kharidar', 'nasu'],
        },
      );
      expect(find.text('Recent'), findsOneWidget);
      expect(find.text('Kharidar'), findsOneWidget);
      expect(find.text('Nayab Subba (NaSu)'), findsOneWidget);
    });
  });

  group('Mock list', () {
    testWidgets('33 mocks become 8 section headers on one screen',
        (tester) async {
      await _setPhoneSize(tester);
      await _pump(tester, _mocks());
      expect(find.text('Lok Sewa (PSC)  ·  9'), findsOneWidget);
      expect(find.text('Health Licences  ·  12'), findsOneWidget);
      expect(find.text('Teaching (TSC)  ·  4'), findsOneWidget);
      expect(find.text('Banking  ·  2'), findsOneWidget);
      expect(find.text('Security Forces  ·  2'), findsOneWidget);
      expect(find.text('Licence & Entrance  ·  2'), findsOneWidget);
      expect(find.text('Law & Justice  ·  1'), findsOneWidget);
      expect(find.text('Public Enterprises  ·  1'), findsOneWidget);
      // No mock rows visible while collapsed.
      expect(find.text('Kharidar'), findsNothing);
      // All headers fit without scrolling.
      final last = tester.getRect(find.text('Public Enterprises  ·  1'));
      expect(last.bottom, lessThan(_contentBottom));
    });

    testWidgets('expanding a section shows compact rows with Start',
        (tester) async {
      await _setPhoneSize(tester);
      await _pump(tester, _mocks());
      await tester.tap(find.text('Teaching (TSC)  ·  4'));
      await tester.pumpAndSettle();
      expect(find.text('TSC — Primary Teacher'), findsOneWidget);
      expect(find.text('TSC — Secondary Teacher'), findsOneWidget);
      // One compact Start button per visible row.
      expect(find.text('Start'), findsNWidgets(4));
      // One-line pattern summary on the row: the three timed TSC mocks
      // share the same pattern (the licence exam is untimed).
      expect(
        find.text('50 Questions • 60 minutes • Pass 50/100 • '
            '20% per wrong answer'),
        findsNWidgets(3),
      );
    });

    testWidgets('search filters mocks to matching exams only', (tester) async {
      await _setPhoneSize(tester);
      await _pump(tester, _mocks());
      await tester.enterText(find.byType(TextField), 'NMC');
      await tester.pumpAndSettle();
      expect(find.text('NMC Licensing Examination (MBBS)'), findsOneWidget);
      expect(find.text('NMC Licensing Examination (BDS)'), findsOneWidget);
      expect(find.text('Kharidar'), findsNothing);
      expect(find.text('Lok Sewa (PSC)  ·  9'), findsNothing);
    });

    testWidgets('tapping a row opens the detail sheet', (tester) async {
      await _setPhoneSize(tester);
      await _pump(tester, _mocks());
      await tester.tap(find.text('Lok Sewa (PSC)  ·  9'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Kharidar'));
      await tester.pumpAndSettle();
      expect(find.text('Start mock exam'), findsOneWidget);
      expect(find.text('50 Questions'), findsOneWidget);
      expect(find.text('45 minutes'), findsOneWidget);
      expect(find.text('Pass 45/100'), findsOneWidget);
      expect(find.text('20% per wrong answer'), findsOneWidget);
    });
  });
}
