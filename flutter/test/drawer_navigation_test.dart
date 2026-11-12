/// Drawer navigation regression tests (v1.0.1).
///
/// Reported 2026-11-12: opening any drawer page (Discussion Hub, Exam
/// Dates, …) and then picking another drawer option left the first page
/// on screen — the drawer just closed and nothing navigated. Root cause:
/// PushScope lived only above the home route, so on any pushed page the
/// drawer's `PushScope.of(context)` returned null and the tap silently
/// did nothing. Every pushed drawer page now carries its own PushScope,
/// and drawer taps from a pushed page replace it instead of stacking.
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/data/data_repository.dart';
import 'package:loksewa_vidyapeeth/main.dart';
import 'package:loksewa_vidyapeeth/screens/community/discussion_screen.dart';
import 'package:loksewa_vidyapeeth/screens/exam_dates_screen.dart';
import 'package:loksewa_vidyapeeth/screens/history_screen.dart';
import 'package:loksewa_vidyapeeth/screens/home_screen.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Pumps the real RootNav. Repository loads are pre-warmed with real
/// async (rootBundle doesn't flush under the test's fake-async clock).
/// The widget itself is pumped inside runAsync: RootNav's _loadShared
/// awaits course assets via rootBundle, and only resolves under real
/// async — without it, its PushScope stays a no-op and no drawer tap
/// can navigate.
Future<void> _pumpApp(WidgetTester tester) async {
  SharedPreferences.setMockInitialValues({});
  // Phone-ish viewport: the countdown card overflows at the default
  // 800px test width, while the Discussion Hub dropdown overflows
  // below ~435px under the wider test font (it fits fine on the
  // user's phone, as his screenshots show). 480px keeps both happy.
  tester.view.physicalSize = const Size(480 * 3, 844 * 3);
  tester.view.devicePixelRatio = 3.0;
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);
  final state = AppState();
  await state.init();
  await tester.runAsync(() async {
    await DataRepository().exams();
    await DataRepository().examDates();
    await DataRepository().historicalEvents();
  });
  // AppStateScope sits ABOVE MaterialApp (as in main.dart) so pushed
  // routes can resolve it too.
  await tester.runAsync(() async {
    await tester.pumpWidget(
      AppStateScope(
        state: state,
        child: AnimatedBuilder(
          animation: state,
          builder: (context, _) => MaterialApp(
            theme: buildDarkTheme(),
            home: const RootNav(),
          ),
        ),
      ),
    );
    await Future<void>.delayed(const Duration(seconds: 2));
    await tester.pump();
  });
  await tester.pump(const Duration(milliseconds: 100));
  expect(find.byType(HomeScreen), findsOneWidget);
}

Future<void> _openDrawer(WidgetTester tester) async {
  await tester.tap(find.byTooltip('Open navigation menu'));
  await tester.pumpAndSettle();
}

Future<void> _tapDrawerItem(WidgetTester tester, String title) async {
  await tester.tap(find.widgetWithText(ListTile, title));
  await tester.pumpAndSettle();
}

void main() {
  group('drawer navigation', () {
    testWidgets('drawer taps navigate from a pushed drawer page',
        (tester) async {
      await _pumpApp(tester);
      await _openDrawer(tester);
      await _tapDrawerItem(tester, 'Discussion Hub');
      expect(find.byType(DiscussionScreen), findsOneWidget);

      // The reported bug: from the pushed Discussion page, the drawer
      // must still navigate. Before the fix this tap silently did
      // nothing and the Discussion page stayed on screen.
      await _openDrawer(tester);
      await _tapDrawerItem(tester, 'Exam Dates');
      expect(find.byType(ExamDatesScreen), findsOneWidget);
      expect(find.byType(DiscussionScreen), findsNothing);

      // And again from Exam Dates to Dates to Remember.
      await _openDrawer(tester);
      await _tapDrawerItem(tester, 'Dates to Remember');
      expect(find.byType(HistoryScreen), findsOneWidget);
      expect(find.byType(ExamDatesScreen), findsNothing);

      // System back returns home: drawer pages replace, never stack.
      // (pageBack can't work here — the app bar shows the drawer
      // hamburger, not a back button, so simulate the Android back.)
      await tester.binding.handlePopRoute();
      await tester.pumpAndSettle();
      expect(find.byType(HomeScreen), findsOneWidget);
    });

    testWidgets('tapping the current drawer page just closes the drawer',
        (tester) async {
      await _pumpApp(tester);
      await _openDrawer(tester);
      await _tapDrawerItem(tester, 'Discussion Hub');
      expect(find.byType(DiscussionScreen), findsOneWidget);
      await _openDrawer(tester);
      await _tapDrawerItem(tester, 'Discussion Hub');
      expect(find.byType(DiscussionScreen), findsOneWidget);
      // Drawer closed: its items are out of the tree.
      expect(
        find.widgetWithText(ListTile, 'Exam Dates'),
        findsNothing,
      );
    });
  });
}
