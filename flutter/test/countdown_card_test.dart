/// Countdown card pager tests (v1.0.2).
///
/// Reported 2026-11-12 (with a screenshot): the "Next exam" card showed
/// dot indicators but could not be swiped — the dots were the only way
/// to change exams, and most people never discover them. The card now
/// pages left/right on swipe. The same screenshot showed two layout
/// bugs, fixed alongside: the seconds digit wrapped onto a second row,
/// and the dots ran off the card's right edge with 8+ exams.
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/models/models.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:loksewa_vidyapeeth/utils/bs_calendar.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';
import 'package:loksewa_vidyapeeth/widgets/countdown_card.dart';
import 'package:shared_preferences/shared_preferences.dart';

ExamDate _d(String id, String title, String dateBs) => ExamDate(
      id: id,
      exam: 'kharidar',
      kind: 'exam',
      dateBs: dateBs,
      titleEn: title,
      titleNe: title,
      source: 'https://example.com',
      confidence: 'high',
    );

/// Fixtures [days] out from today, so the test never time-bombs.
List<ExamDate> _dates(List<(String, String, int)> specs) {
  final todayAbs = bsAbsDay(bsToday()!)!;
  return [
    for (final (id, title, days) in specs)
      _d(id, title, bsFromAbs(todayAbs + days)!),
  ];
}

Future<void> _pumpCard(WidgetTester tester, List<ExamDate> dates) async {
  SharedPreferences.setMockInitialValues({});
  tester.view.physicalSize = const Size(390 * 3, 844 * 3);
  tester.view.devicePixelRatio = 3.0;
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);
  final state = AppState();
  await state.init();
  await tester.pumpWidget(
    AppStateScope(
      state: state,
      child: MaterialApp(
        theme: buildAppTheme(),
        home: Scaffold(body: CountdownCard(dates: dates)),
      ),
    ),
  );
  await tester.pump(const Duration(milliseconds: 100));
}

/// Drags horizontally from the card's title (clear of the buttons and
/// the dots row).
Future<void> _swipe(WidgetTester tester, String title, double dx) async {
  final start = tester.getCenter(find.text(title));
  await tester.dragFrom(start, Offset(dx, 0));
  // Two 300ms pumps: the first starts the 250ms switcher transition,
  // the second advances past it so the outgoing child is removed.
  // (A single pump renders only the frame where the animation starts,
  // at elapsed 0 — the transition never advances.)
  await tester.pump(const Duration(milliseconds: 300));
  await tester.pump(const Duration(milliseconds: 300));
}

void main() {
  group('countdown card pager', () {
    testWidgets('swipe left/right pages through upcoming exams',
        (tester) async {
      final dates = _dates([
        ('a', 'Exam One', 3),
        ('b', 'Exam Two', 10),
        ('c', 'Exam Three', 20),
      ]);
      await _pumpCard(tester, dates);
      expect(find.text('Exam One'), findsOneWidget);

      await _swipe(tester, 'Exam One', -300);
      expect(find.text('Exam Two'), findsOneWidget);
      expect(find.text('Exam One'), findsNothing);

      await _swipe(tester, 'Exam Two', -300);
      expect(find.text('Exam Three'), findsOneWidget);

      await _swipe(tester, 'Exam Three', 300);
      expect(find.text('Exam Two'), findsOneWidget);
    });

    testWidgets('swiping past the ends stays put', (tester) async {
      final dates = _dates([
        ('a', 'Exam One', 3),
        ('b', 'Exam Two', 10),
      ]);
      await _pumpCard(tester, dates);

      // Right on the first exam: stays.
      await _swipe(tester, 'Exam One', 300);
      expect(find.text('Exam One'), findsOneWidget);

      // Left to the last exam, then left again: stays.
      await _swipe(tester, 'Exam One', -300);
      expect(find.text('Exam Two'), findsOneWidget);
      await _swipe(tester, 'Exam Two', -300);
      expect(find.text('Exam Two'), findsOneWidget);
    });

    testWidgets('countdown digits stay on one row at phone width',
        (tester) async {
      final dates = _dates([('a', 'Exam One', 3)]);
      await _pumpCard(tester, dates);
      // Before the fix the "sec" unit wrapped onto a second row.
      final daysY = tester.getCenter(find.text('days')).dy;
      final secY = tester.getCenter(find.text('sec')).dy;
      expect(secY, moreOrLessEquals(daysY, epsilon: 1.0));
    });

    testWidgets('many upcoming exams do not overflow the dots row',
        (tester) async {
      final dates = _dates([
        for (var i = 1; i <= 10; i++) ('d$i', 'Exam $i', i),
      ]);
      await _pumpCard(tester, dates);
      // 10 dots at the old 44px hit width overflowed the card (a
      // RenderFlex overflow fails the test automatically).
      expect(find.text('Exam 1'), findsOneWidget);
    });
  });
}
