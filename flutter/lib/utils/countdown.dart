/// Countdown maths for the "Next exam" card — pure functions, mirroring the
/// vanilla site's nxTargetMs / nxRemaining / nxPagerList / nxCardState
/// helpers. All testable without widgets.
library;

import '../models/models.dart';
import 'bs_calendar.dart';

/// Card display states, mirroring the vanilla site.
enum CountdownState { today, near, far, none }

/// Milliseconds for start-of-day (UTC) on [dateBs].
/// Pure: [nowUtcMs] is injectable so tests don't depend on the clock.
int? nxTargetMs(String dateBs, {int? nowUtcMs}) {
  final now = nowUtcMs ?? DateTime.now().toUtc().millisecondsSinceEpoch;
  final daysUntil = bsDaysUntil(dateBs, nowUtcDay: now ~/ 86400000);
  if (daysUntil == null) return null;
  final startOfTodayUtc = (now ~/ 86400000) * 86400000;
  return startOfTodayUtc + daysUntil * 86400000;
}

/// Remaining duration until [targetMs], clamped at zero (never negative).
Duration nxRemaining(int? targetMs, {int? nowUtcMs}) {
  if (targetMs == null) return Duration.zero;
  final now = nowUtcMs ?? DateTime.now().toUtc().millisecondsSinceEpoch;
  final diff = targetMs - now;
  return Duration(milliseconds: diff < 0 ? 0 : diff);
}

/// Exams within the next [windowDays] days, soonest first, past excluded.
List<ExamDate> nxPagerList(
  List<ExamDate> dates, {
  int windowDays = 30,
  int? nowUtcDay,
}) {
  final out = <({ExamDate d, int days})>[];
  for (final e in dates) {
    final days = bsDaysUntil(e.dateBs, nowUtcDay: nowUtcDay);
    if (days == null || days < 0 || days > windowDays) continue;
    out.add((d: e, days: days));
  }
  out.sort((a, b) => a.days.compareTo(b.days));
  return out.map((e) => e.d).toList();
}

CountdownState nxCardState(int? daysUntil) {
  if (daysUntil == null) return CountdownState.none;
  if (daysUntil == 0) return CountdownState.today;
  if (daysUntil <= 30) return CountdownState.near;
  return CountdownState.far;
}

/// Pick the nearest upcoming exam (any future date), or null.
ExamDate? nxPickNearest(List<ExamDate> dates, {int? nowUtcDay}) {
  ExamDate? best;
  int? bestDays;
  for (final e in dates) {
    final days = bsDaysUntil(e.dateBs, nowUtcDay: nowUtcDay);
    if (days == null || days < 0) continue;
    if (bestDays == null || days < bestDays) {
      best = e;
      bestDays = days;
    }
  }
  return best;
}

/// Split a duration into DD / HH / MM / SS strings.
({String dd, String hh, String mm, String ss}) splitDuration(Duration d) {
  String two(int n) => n.toString().padLeft(2, '0');
  final days = d.inDays;
  final hours = d.inHours % 24;
  final minutes = d.inMinutes % 60;
  final seconds = d.inSeconds % 60;
  return (
    dd: days.toString().padLeft(2, '0'),
    hh: two(hours),
    mm: two(minutes),
    ss: two(seconds),
  );
}
