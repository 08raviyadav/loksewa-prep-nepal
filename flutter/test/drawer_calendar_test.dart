/// Drawer calendar tests (v1.0.3) — AD date in English, BS date in
/// Nepali, live ticking clock in both.
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/l10n/app_strings.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:loksewa_vidyapeeth/utils/bs_calendar.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';
import 'package:loksewa_vidyapeeth/widgets/drawer_calendar.dart';
import 'package:shared_preferences/shared_preferences.dart';

const _monthsEn = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
];

Future<void> _pumpCalendar(
  WidgetTester tester, {
  bool nepali = false,
}) async {
  SharedPreferences.setMockInitialValues({});
  final state = AppState();
  await state.init();
  if (nepali) await state.setLang(AppLang.ne);
  await tester.pumpWidget(
    AppStateScope(
      state: state,
      child: MaterialApp(
        theme: buildAppTheme(),
        home: const Scaffold(body: DrawerCalendar()),
      ),
    ),
  );
  await tester.pump();
}

String _clockText(WidgetTester tester) {
  final finder = find.textContaining(RegExp(r'\d{2}:\d{2}:\d{2}'));
  expect(finder, findsOneWidget);
  return tester.widget<Text>(finder).data!;
}

void main() {
  group('drawer calendar', () {
    testWidgets('shows the Gregorian date in English', (tester) async {
      await _pumpCalendar(tester);
      final now = DateTime.now();
      expect(find.text('${now.day}'), findsOneWidget);
      expect(
        find.text('${_monthsEn[now.month - 1]} ${now.year}'),
        findsOneWidget,
      );
      // Live clock, HH:MM:SS.
      _clockText(tester);
    });

    testWidgets('shows the BS date in Nepali', (tester) async {
      await _pumpCalendar(tester, nepali: true);
      final bs = bsToday()!.split('-');
      final year = int.parse(bs[0]);
      final month = int.parse(bs[1]);
      final day = int.parse(bs[2]);
      expect(find.text(neDigits(day.toString())), findsOneWidget);
      expect(
        find.text('${bsMonthNe[month - 1]} ${neDigits(year.toString())}'),
        findsOneWidget,
      );
      // Clock in Nepali digits: २ अक्षर : २ अक्षर : २ अक्षर.
      final finder = find.textContaining(RegExp(r'[०-९]{2}:[०-९]{2}:[०-९]{2}'));
      expect(finder, findsOneWidget);
    });

    testWidgets('the clock ticks every second', (tester) async {
      await _pumpCalendar(tester);
      final before = _clockText(tester);
      // Probe-verified: DateTime.now() is REAL time in widget tests —
      // fake pumps fire the timer but don't move the clock. So wait
      // 1.5 real seconds (guaranteed to cross a second boundary), then
      // pump to fire the timer and rebuild with the new time.
      await tester.runAsync(
        () => Future<void>.delayed(const Duration(milliseconds: 1500)),
      );
      await tester.pump(const Duration(seconds: 1));
      final after = _clockText(tester);
      expect(after, isNot(before));
    });
  });
}
