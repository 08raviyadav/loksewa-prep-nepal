/// Small live calendar at the top of the drawer (v1.0.3).
///
/// English: Gregorian date (weekday, day, month, year) + live clock.
/// Nepali: BS date in Devanagari (weekday, day, month, year) + live
/// clock in Nepali digits. Ticks every second while the drawer is open;
/// the timer is cancelled when the drawer closes.
library;

import 'dart:async';

import 'package:flutter/material.dart';

import '../theme/app_theme.dart';
import '../utils/bs_calendar.dart';
import 'app_scaffold.dart';

const _weekdaysEn = [
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
  'Sunday',
];

const _weekdaysNe = [
  'सोमबार',
  'मंगलबार',
  'बुधबार',
  'बिहिबार',
  'शुक्रबार',
  'शनिबार',
  'आइतबार',
];

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

class DrawerCalendar extends StatefulWidget {
  const DrawerCalendar({super.key});

  @override
  State<DrawerCalendar> createState() => _DrawerCalendarState();
}

class _DrawerCalendarState extends State<DrawerCalendar> {
  Timer? _timer;
  DateTime _now = DateTime.now();

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (mounted) setState(() => _now = DateTime.now());
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  String _two(int v) => v.toString().padLeft(2, '0');

  @override
  Widget build(BuildContext context) {
    final ne = AppStateScope.of(context).isNe;
    // The BS weekday is the same day of the week as the Gregorian one.
    final weekday =
        ne ? _weekdaysNe[_now.weekday - 1] : _weekdaysEn[_now.weekday - 1];
    final String dayNum;
    final String monthYear;
    if (ne) {
      final p = bsToday()?.split('-');
      if (p != null && p.length == 3) {
        dayNum = neDigits(int.parse(p[2]).toString());
        monthYear =
            '${bsMonthNe[int.parse(p[1]) - 1]} ${neDigits(p[0])}';
      } else {
        // BS tables don't cover today (shouldn't happen) — fall back
        // to the Gregorian date in Nepali digits.
        dayNum = neDigits('${_now.day}');
        monthYear =
            '${_monthsEn[_now.month - 1]} ${neDigits('${_now.year}')}';
      }
    } else {
      dayNum = '${_now.day}';
      monthYear = '${_monthsEn[_now.month - 1]} ${_now.year}';
    }
    final time =
        '${_two(_now.hour)}:${_two(_now.minute)}:${_two(_now.second)}';
    return Container(
      margin: const EdgeInsets.fromLTRB(
        AppSpacing.s3,
        AppSpacing.s3,
        AppSpacing.s3,
        AppSpacing.s1,
      ),
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.s3,
        vertical: AppSpacing.s2,
      ),
      decoration: BoxDecoration(
        color: AppColors.of(context).accentSoft,
        borderRadius: AppRadius.mdAll,
        border: Border.all(color: AppColors.of(context).accentLine),
      ),
      child: Row(
        children: [
          Text(
            dayNum,
            style: AppType.display.copyWith(color: AppColors.of(context).accent),
          ),
          const SizedBox(width: AppSpacing.s3),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  weekday,
                  style: AppType.small.copyWith(color: AppColors.of(context).muted),
                ),
                Text(monthYear, style: AppType.h3),
                const SizedBox(height: 2),
                Row(
                  children: [
                    Icon(
                      Icons.access_time,
                      size: 14,
                      color: AppColors.of(context).muted,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      ne ? neDigits(time) : time,
                      style: AppType.small.copyWith(
                        fontFeatures: const [FontFeature.tabularFigures()],
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
