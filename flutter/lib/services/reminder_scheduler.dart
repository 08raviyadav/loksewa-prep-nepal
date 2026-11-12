/// Reminder scheduling logic — pure-ish, unit-testable.
///
/// Decides *which* notifications to schedule from the user's reminded exam
/// ids (the `loksewa_reminders_v1` preference, owned by AppState), the
/// bundled `assets/data/exam-dates.json`, and today's BS date. The actual
/// OS scheduling goes through [NotificationService], so this file never
/// touches platform code directly.
///
/// Behaviour:
/// - An exam with a reminder fires once per remaining day while it is
///   0..3 days away (lead window), at [examReminderHour]:00 local time:
///   "⏰ {title} in N days" (Nepali variant when [ne] is true).
/// - The daily nudge fires once at the next occurrence of the
///   user's chosen morning hour (default 08:00 since v1.0.4, when it
///   became the "Your Daily Challenge is ready" reminder).
/// - [rescheduleAll] is idempotent: it cancels everything first, then
///   schedules the freshly computed set. Call it on every app start
///   (see the integration line in FIREBASE_SETUP.md) and whenever the
///   user toggles a reminder.
///
/// Web: [createNotificationService] returns the no-op stub on web, so
/// [rescheduleAll] is safe to call unconditionally — the vanilla site's
/// on-open in-app banner stays the web fallback.
library;

import 'package:shared_preferences/shared_preferences.dart';

import '../data/data_repository.dart';
import '../models/models.dart';
import '../utils/bs_calendar.dart';
import 'notifications.dart';

/// Preference keys. The reminder set is written by AppState; the nudge
/// settings are owned by this milestone (a settings UI can bind to them).
const kRemindersKey = 'loksewa_reminders_v1';
const kLangKey = 'loksewa_lang_v1';
const kDailyNudgeEnabledKey = 'loksewa_daily_nudge_v1';
const kDailyNudgeHourKey = 'loksewa_daily_nudge_hour_v1';
const kDailyNudgeMinuteKey = 'loksewa_daily_nudge_minute_v1';

/// Exam reminders fire while the exam is this many days away (inclusive).
const int examReminderLeadDays = 3;

/// Local hour exam reminders fire at (09:00).
const int examReminderHour = 9;

/// Default daily-nudge time (08:00 since v1.0.4) until the user picks
/// their own.
const int defaultNudgeHour = 8;
const int defaultNudgeMinute = 0;

/// One notification to schedule. [fireAt] is device-local time.
class PlannedReminder {
  final String id;
  final String title;
  final String body;
  final DateTime fireAt;

  const PlannedReminder({
    required this.id,
    required this.title,
    required this.body,
    required this.fireAt,
  });

  @override
  String toString() => 'PlannedReminder(id=$id, fireAt=$fireAt, body=$body)';
}

/// AD epoch day (days since 1970-01-01 UTC) for a BS "YYYY-MM-DD" date.
///
/// Uses only the public BS API plus the documented anchor
/// (2026-10-31 AD == 2083-07-14 BS). Null on malformed/out-of-range input.
int? adDayForBs(String dateBs) {
  final abs = bsAbsDay(dateBs);
  final anchorBs = bsAbsDay('2083-07-14');
  if (abs == null || anchorBs == null) return null;
  final anchorAd =
      DateTime.utc(2026, 10, 31).millisecondsSinceEpoch ~/ 86400000;
  return anchorAd + (abs - anchorBs);
}

/// "⏰ {title} in N days" (+ Nepali variant). Exported for tests.
String examReminderBody(String title, int daysLeft, {required bool ne}) {
  if (ne) {
    if (daysLeft == 0) return '⏰ $title आज छ!';
    if (daysLeft == 1) return '⏰ $title भोलि छ!';
    return '⏰ $title ${neDigits(daysLeft.toString())} दिनमा छ!';
  }
  if (daysLeft == 0) return '⏰ $title is today!';
  if (daysLeft == 1) return '⏰ $title is tomorrow!';
  return '⏰ $title in $daysLeft days!';
}

/// Compute the exam reminders to schedule.
///
/// For every reminded exam that is 0..[leadDays] days away, one reminder per
/// remaining day at [hour]:00 local time. Days whose fire time is already
/// past (relative to [now]) are skipped. Pure: [now] and [nowUtcDay] are
/// injectable for tests.
List<PlannedReminder> computeExamReminders({
  required List<ExamDate> exams,
  required Set<String> remindedIds,
  required DateTime now,
  int? nowUtcDay,
  int leadDays = examReminderLeadDays,
  int hour = examReminderHour,
  bool ne = false,
}) {
  final out = <PlannedReminder>[];
  for (final exam in exams) {
    if (!remindedIds.contains(exam.id)) continue;
    final days = bsDaysUntil(exam.dateBs, nowUtcDay: nowUtcDay);
    if (days == null || days < 0 || days > leadDays) continue;
    final title = exam.title(ne);
    // Anchor fire dates to the device-local "today": the reminder for d days
    // left fires on (today + days - d) at [hour]:00 local. This keeps the
    // firing days consistent with the countdown the app displays (both derive
    // from bsDaysUntil) and needs no timezone database.
    for (var d = days; d >= 0; d--) {
      final fireAt = DateTime(now.year, now.month, now.day + (days - d), hour);
      if (fireAt.isBefore(now)) continue;
      out.add(
        PlannedReminder(
          id: 'exam:${exam.id}#$d',
          title: title,
          body: examReminderBody(title, d, ne: ne),
          fireAt: fireAt,
        ),
      );
    }
  }
  return out;
}

/// Compute the next daily-nudge firing: today at [hour]:[minute] if still
/// ahead, otherwise tomorrow. Pure.
PlannedReminder computeDailyNudge({
  required DateTime now,
  required int hour,
  required int minute,
  required bool ne,
}) {
  var fireAt = DateTime(now.year, now.month, now.day, hour, minute);
  if (!fireAt.isAfter(now)) {
    fireAt = fireAt.add(const Duration(days: 1));
  }
  return PlannedReminder(
    id: 'daily_nudge',
    title: ne ? 'लोक सेवा विद्यापीठ' : 'LokSewa Vidyapeeth',
    body: ne
        ? '🎯 आजको दैनिक चुनौती तयार छ — १० नयाँ प्रश्न पर्खिरहेका छन्!'
        : '🎯 Your Daily Challenge is ready — 10 fresh questions are waiting!',
    fireAt: fireAt,
  );
}

/// Cancel everything, then schedule the freshly computed set.
///
/// All inputs are overridable so tests can inject fakes; in production call
/// it bare: `await rescheduleAll();`. Returns the number of notifications
/// scheduled. Safe on web (the stub service no-ops).
Future<int> rescheduleAll({
  NotificationService? service,
  Set<String>? remindedIds,
  bool? dailyNudgeEnabled,
  int? nudgeHour,
  int? nudgeMinute,
  bool? ne,
  DateTime? now,
  int? nowUtcDay,
  Future<List<ExamDate>> Function()? examDatesLoader,
}) async {
  service ??= createNotificationService();
  final prefs = await SharedPreferences.getInstance();

  final ids = remindedIds ??
      (prefs.getStringList(kRemindersKey)?.toSet() ?? <String>{});
  final nudgeOn =
      dailyNudgeEnabled ?? (prefs.getBool(kDailyNudgeEnabledKey) ?? true);
  final hour =
      nudgeHour ?? (prefs.getInt(kDailyNudgeHourKey) ?? defaultNudgeHour);
  final minute =
      nudgeMinute ?? (prefs.getInt(kDailyNudgeMinuteKey) ?? defaultNudgeMinute);
  final isNe = ne ?? (prefs.getString(kLangKey) == 'ne');
  final at = now ?? DateTime.now();

  // Idempotency: wipe the slate, then schedule the computed set.
  await service.cancelAll();
  // Permission first so the very first scheduled reminder can already show.
  // Scheduling without permission is harmless (OS drops it), so we continue
  // regardless of the answer.
  await service.requestPermission();

  var scheduled = 0;
  final loader = examDatesLoader ?? DataRepository().examDates;
  List<ExamDate> exams;
  try {
    exams = await loader();
  } catch (_) {
    exams = const [];
  }

  for (final r in computeExamReminders(
    exams: exams,
    remindedIds: ids,
    now: at,
    nowUtcDay: nowUtcDay,
    ne: isNe,
  )) {
    await service.scheduleExamReminder(
      id: r.id,
      title: r.title,
      body: r.body,
      when: r.fireAt,
    );
    scheduled++;
  }

  if (nudgeOn) {
    final nudge = computeDailyNudge(
      now: at,
      hour: hour,
      minute: minute,
      ne: isNe,
    );
    await service.scheduleDaily(
      id: nudge.id,
      title: nudge.title,
      body: nudge.body,
      hour: hour,
      minute: minute,
    );
    scheduled++;
  }

  return scheduled;
}
