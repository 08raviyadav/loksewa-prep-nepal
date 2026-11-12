// Tests for the reminder scheduling decisions (Milestone 7).
//
// All date maths is pure: "today" is injected via [now] (device-local) and
// [nowUtcDay] (AD epoch day, UTC), so these tests are timezone-independent.
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:loksewa_vidyapeeth/models/models.dart';
import 'package:loksewa_vidyapeeth/services/notification_backend_local.dart';
import 'package:loksewa_vidyapeeth/services/notifications.dart';
import 'package:loksewa_vidyapeeth/services/reminder_scheduler.dart';

/// 2026-10-31 AD == 2083-07-14 BS (the documented anchor).
final int _anchorNowUtcDay =
    DateTime.utc(2026, 10, 31).millisecondsSinceEpoch ~/ 86400000;

ExamDate _exam(
  String id,
  String dateBs, {
  String titleEn = 'Test Exam',
  String titleNe = 'परीक्षा',
}) =>
    ExamDate(
      id: id,
      exam: 'test-exam',
      kind: 'exam',
      dateBs: dateBs,
      titleEn: titleEn,
      titleNe: titleNe,
      source: '',
      confidence: 'high',
    );

class FakeNotificationService implements NotificationService {
  final List<Map<String, Object?>> scheduled = [];
  final List<Map<String, Object?>> daily = [];
  final List<Map<String, Object?>> shown = [];
  int cancelAllCalls = 0;
  int permissionCalls = 0;
  bool permissionResult = true;

  @override
  Future<bool> requestPermission() async {
    permissionCalls++;
    return permissionResult;
  }

  @override
  Future<void> scheduleExamReminder({
    required String id,
    required String title,
    required String body,
    required DateTime when,
  }) async {
    scheduled.add({'id': id, 'title': title, 'body': body, 'when': when});
  }

  @override
  Future<void> cancelExamReminder(String id) async {}

  @override
  Future<void> showNow({
    required String id,
    required String title,
    required String body,
  }) async {
    shown.add({'id': id, 'title': title, 'body': body});
  }

  @override
  Future<void> scheduleDaily({
    required String id,
    required String title,
    required String body,
    required int hour,
    required int minute,
  }) async {
    daily.add({
      'id': id,
      'title': title,
      'body': body,
      'hour': hour,
      'minute': minute,
    });
  }

  @override
  Future<void> cancelAll() async {
    cancelAllCalls++;
    scheduled.clear();
    daily.clear();
    shown.clear();
  }

  Set<String> get scheduledIds =>
      scheduled.map((e) => e['id'] as String).toSet();
}

void main() {
  group('adDayForBs', () {
    test('anchor round-trips to 2026-10-31', () {
      expect(adDayForBs('2083-07-14'), _anchorNowUtcDay);
    });

    test('next BS day is the next AD day', () {
      expect(adDayForBs('2083-07-15'), _anchorNowUtcDay + 1);
    });

    test('malformed input returns null', () {
      expect(adDayForBs('not-a-date'), isNull);
      expect(adDayForBs('2083-13-40'), isNull);
      expect(adDayForBs(''), isNull);
    });
  });

  group('examReminderBody', () {
    test('exact English strings', () {
      expect(examReminderBody('X', 0, ne: false), '⏰ X is today!');
      expect(examReminderBody('X', 1, ne: false), '⏰ X is tomorrow!');
      expect(examReminderBody('X', 2, ne: false), '⏰ X in 2 days!');
      expect(examReminderBody('X', 3, ne: false), '⏰ X in 3 days!');
    });

    test('exact Nepali strings', () {
      expect(examReminderBody('X', 0, ne: true), '⏰ X आज छ!');
      expect(examReminderBody('X', 1, ne: true), '⏰ X भोलि छ!');
      expect(examReminderBody('X', 3, ne: true), '⏰ X ३ दिनमा छ!');
    });
  });

  group('computeExamReminders', () {
    final now = DateTime(2026, 10, 31, 8, 0); // 08:00 local, anchor day

    test('exam 3 days away schedules one reminder per remaining day', () {
      final rs = computeExamReminders(
        exams: [_exam('e1', '2083-07-17')], // anchor + 3
        remindedIds: {'e1'},
        now: now,
        nowUtcDay: _anchorNowUtcDay,
      );
      expect(rs.map((r) => r.id).toSet(), {
        'exam:e1#3',
        'exam:e1#2',
        'exam:e1#1',
        'exam:e1#0',
      });
      expect(rs.map((r) => r.body).toSet(), {
        '⏰ Test Exam in 3 days!',
        '⏰ Test Exam in 2 days!',
        '⏰ Test Exam is tomorrow!',
        '⏰ Test Exam is today!',
      });
      // One per consecutive day, each at 09:00 local.
      final sorted = [...rs]..sort((a, b) => a.fireAt.compareTo(b.fireAt));
      for (var i = 0; i < sorted.length; i++) {
        final f = sorted[i].fireAt;
        expect(f.hour, 9);
        expect(f.minute, 0);
        expect(
          DateTime(
            f.year,
            f.month,
            f.day,
          ).difference(DateTime(now.year, now.month, now.day)).inDays,
          i,
        );
      }
    });

    test('exam more than 3 days away schedules nothing', () {
      final rs = computeExamReminders(
        exams: [_exam('e1', '2083-07-18')], // anchor + 4
        remindedIds: {'e1'},
        now: now,
        nowUtcDay: _anchorNowUtcDay,
      );
      expect(rs, isEmpty);
    });

    test('past exam schedules nothing', () {
      final rs = computeExamReminders(
        exams: [_exam('e1', '2083-07-13')], // anchor - 1
        remindedIds: {'e1'},
        now: now,
        nowUtcDay: _anchorNowUtcDay,
      );
      expect(rs, isEmpty);
    });

    test('exam without a reminder toggle schedules nothing', () {
      final rs = computeExamReminders(
        exams: [_exam('e1', '2083-07-15')],
        remindedIds: {'some-other-exam'},
        now: now,
        nowUtcDay: _anchorNowUtcDay,
      );
      expect(rs, isEmpty);
    });

    test('malformed date is skipped, not fatal', () {
      final rs = computeExamReminders(
        exams: [_exam('e1', 'garbage')],
        remindedIds: {'e1'},
        now: now,
        nowUtcDay: _anchorNowUtcDay,
      );
      expect(rs, isEmpty);
    });

    test('fire times already past today are skipped', () {
      // 10:00 local — today's 09:00 slot is gone, tomorrow's is not.
      // The '#d' suffix is days-left *at fire time*: the surviving reminder
      // is #0, firing on exam day itself.
      final late = DateTime(2026, 10, 31, 10, 0);
      final rs = computeExamReminders(
        exams: [_exam('e1', '2083-07-15')], // anchor + 1
        remindedIds: {'e1'},
        now: late,
        nowUtcDay: _anchorNowUtcDay,
      );
      expect(rs.map((r) => r.id).toSet(), {'exam:e1#0'});
      expect(rs.single.body, '⏰ Test Exam is today!');
      expect(rs.single.fireAt, DateTime(2026, 11, 1, 9, 0));
    });

    test('Nepali flag picks the Nepali title and body', () {
      final rs = computeExamReminders(
        exams: [_exam('e1', '2083-07-14')], // today
        remindedIds: {'e1'},
        now: now,
        nowUtcDay: _anchorNowUtcDay,
        ne: true,
      );
      expect(rs.map((r) => r.id).toSet(), {'exam:e1#0'});
      expect(rs.single.title, 'परीक्षा');
      expect(rs.single.body, '⏰ परीक्षा आज छ!');
    });
  });

  group('computeDailyNudge', () {
    test('fires today when the hour is still ahead', () {
      final now = DateTime(2026, 10, 31, 6, 0);
      final n = computeDailyNudge(now: now, hour: 7, minute: 0, ne: false);
      expect(n.id, 'daily_nudge');
      expect(n.fireAt, DateTime(2026, 10, 31, 7, 0));
    });

    test('rolls to tomorrow when the hour has passed', () {
      final now = DateTime(2026, 10, 31, 8, 0);
      final n = computeDailyNudge(now: now, hour: 7, minute: 0, ne: false);
      expect(n.fireAt, DateTime(2026, 11, 1, 7, 0));
    });

    test('respects a custom hour and minute', () {
      final now = DateTime(2026, 10, 31, 5, 0);
      final n = computeDailyNudge(now: now, hour: 6, minute: 30, ne: true);
      expect(n.fireAt, DateTime(2026, 10, 31, 6, 30));
      expect(n.body.contains('🎯'), isTrue);
    });
  });

  group('rescheduleAll', () {
    late FakeNotificationService fake;

    setUp(() {
      fake = FakeNotificationService();
      SharedPreferences.setMockInitialValues(<String, Object>{});
    });

    Future<int> run({
      List<ExamDate>? exams,
      Set<String>? remindedIds,
      bool? nudge,
      int? hour,
      int? minute,
      bool? ne,
      DateTime? now,
    }) =>
        rescheduleAll(
          service: fake,
          remindedIds: remindedIds,
          dailyNudgeEnabled: nudge,
          nudgeHour: hour,
          nudgeMinute: minute,
          ne: ne,
          now: now ?? DateTime(2026, 10, 31, 8, 0),
          nowUtcDay: _anchorNowUtcDay,
          examDatesLoader: () async => exams ?? const [],
        );

    test('schedules exam reminders plus the daily nudge', () async {
      final count = await run(
        exams: [
          _exam('e1', '2083-07-17'), // 3 days away, reminded
          _exam('e2', '2083-07-24'), // 10 days away, reminded -> skipped
          _exam('e3', '2083-07-13'), // past, reminded -> skipped
        ],
        remindedIds: {'e1', 'e2', 'e3'},
      );
      expect(count, 5); // 4 exam reminders + 1 nudge
      expect(fake.scheduledIds, {
        'exam:e1#3',
        'exam:e1#2',
        'exam:e1#1',
        'exam:e1#0',
      });
      expect(fake.daily, hasLength(1));
      expect(fake.daily.single['hour'], 7);
      expect(fake.daily.single['minute'], 0);
      expect(fake.cancelAllCalls, 1);
      expect(fake.permissionCalls, 1);
    });

    test(
      'is idempotent: second run cancels then reproduces the same set',
      () async {
        final exams = [_exam('e1', '2083-07-16')];
        await run(exams: exams, remindedIds: {'e1'});
        final first = fake.scheduledIds;
        await run(exams: exams, remindedIds: {'e1'});
        expect(fake.cancelAllCalls, 2);
        expect(fake.scheduledIds, first);
        // No duplicates within a single run.
        expect(fake.scheduled.length, first.length);
      },
    );

    test('disabled nudge schedules no daily notification', () async {
      final count = await run(exams: const [], nudge: false);
      expect(count, 0);
      expect(fake.daily, isEmpty);
    });

    test('custom nudge time is honoured', () async {
      await run(exams: const [], hour: 6, minute: 30);
      expect(fake.daily.single['hour'], 6);
      expect(fake.daily.single['minute'], 30);
    });

    test('reads reminder ids and nudge prefs from SharedPreferences', () async {
      SharedPreferences.setMockInitialValues(<String, Object>{
        kRemindersKey: ['e1'],
        kDailyNudgeEnabledKey: false,
        kLangKey: 'ne',
      });
      final count = await rescheduleAll(
        service: fake,
        now: DateTime(2026, 10, 31, 8, 0),
        nowUtcDay: _anchorNowUtcDay,
        examDatesLoader: () async => [_exam('e1', '2083-07-14')],
      );
      expect(count, 1); // today's reminder; nudge disabled via prefs
      expect(fake.daily, isEmpty);
      expect(fake.scheduled.single['body'], '⏰ परीक्षा आज छ!');
    });

    test('a broken exam feed degrades to just the nudge', () async {
      final count = await rescheduleAll(
        service: fake,
        remindedIds: {'e1'},
        now: DateTime(2026, 10, 31, 8, 0),
        nowUtcDay: _anchorNowUtcDay,
        examDatesLoader: () => throw StateError('no data'),
      );
      expect(count, 1);
      expect(fake.scheduled, isEmpty);
      expect(fake.daily, hasLength(1));
    });
  });

  group('LocalNotificationService.stableNotificationId', () {
    test('is deterministic and non-negative', () {
      final a = LocalNotificationService.stableNotificationId('exam:e1#3');
      final b = LocalNotificationService.stableNotificationId('exam:e1#3');
      expect(a, b);
      expect(a, greaterThanOrEqualTo(0));
      expect(a, lessThan(1 << 31));
    });

    test('distinct ids map to distinct ints', () {
      final ids = {
        for (var i = 0; i < 50; i++)
          LocalNotificationService.stableNotificationId('exam:e$i#${i % 4}'),
      };
      ids.add(LocalNotificationService.stableNotificationId('daily_nudge'));
      expect(ids.length, 51);
    });
  });
}
