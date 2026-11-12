/// Mobile/desktop backend for [NotificationService], powered by
/// `flutter_local_notifications`.
///
/// Imported by notifications.dart via conditional import — this file is only
/// compiled on `dart:io` platforms, so the web build never sees the plugin.
///
/// Design notes:
/// - One-shot exam reminders and the daily nudge are scheduled with
///   [AndroidScheduleMode.inexactAllowWhileIdle], so no exact-alarm
///   permission (SCHEDULE_EXACT_ALARM / USE_EXACT_ALARM) is needed. A few
///   minutes of delivery slack is fine for study reminders.
/// - Times are converted to absolute UTC instants before scheduling, so no
///   IANA timezone-name lookup plugin is required; the device clock decides
///   the local wall-clock time.
/// - String ids from the scheduler are mapped to stable int ids with a
///   deterministic FNV-1a hash (Dart's String.hashCode is not stable across
///   runs, so it must not be used for persisted notification ids).
library;

import 'package:flutter/foundation.dart'
    show TargetPlatform, defaultTargetPlatform;
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:timezone/data/latest_all.dart' as tzdata;
import 'package:timezone/timezone.dart' as tz;

import 'notifications.dart';

/// Returns the real local-notification backend for mobile/desktop.
NotificationService createService() => LocalNotificationService();

class LocalNotificationService implements NotificationService {
  LocalNotificationService._();
  static final LocalNotificationService _instance =
      LocalNotificationService._();
  factory LocalNotificationService() => _instance;

  final FlutterLocalNotificationsPlugin _plugin =
      FlutterLocalNotificationsPlugin();
  bool _initialized = false;

  static const _channelId = 'exam_reminders';
  static const _channelName = 'Exam reminders';

  /// Deterministic 31-bit id for a scheduler string id. Public so tests can
  /// assert stability (schedule/cancel round-trips must agree).
  static int stableNotificationId(String id) {
    var hash = 0x811c9dc5;
    for (var i = 0; i < id.length; i++) {
      hash ^= id.codeUnitAt(i);
      hash = (hash * 0x01000193) & 0xffffffff;
    }
    return hash & 0x7fffffff;
  }

  Future<void> _ensureInitialized() async {
    if (_initialized) return;
    tzdata.initializeTimeZones();
    const settings = InitializationSettings(
      android: AndroidInitializationSettings('@mipmap/ic_launcher'),
      iOS: DarwinInitializationSettings(),
      macOS: DarwinInitializationSettings(),
      linux: LinuxInitializationSettings(defaultActionName: 'Open app'),
    );
    await _plugin.initialize(settings: settings);
    _initialized = true;
  }

  NotificationDetails _details() => const NotificationDetails(
        android: AndroidNotificationDetails(
          _channelId,
          _channelName,
          channelDescription:
              'Reminders for upcoming Lok Sewa exams and the daily practice nudge.',
          importance: Importance.defaultImportance,
          priority: Priority.defaultPriority,
        ),
        iOS: DarwinNotificationDetails(),
        macOS: DarwinNotificationDetails(),
      );

  /// Local wall-clock time -> absolute instant the plugin can schedule.
  tz.TZDateTime _asZoned(DateTime local) =>
      tz.TZDateTime.from(local.toUtc(), tz.UTC);

  @override
  Future<bool> requestPermission() async {
    await _ensureInitialized();
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        final android = _plugin.resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>();
        // Android 13+ runtime prompt for POST_NOTIFICATIONS; on older
        // versions the call is a no-op returning true.
        return await android?.requestNotificationsPermission() ?? false;
      case TargetPlatform.iOS:
        final ios = _plugin.resolvePlatformSpecificImplementation<
            IOSFlutterLocalNotificationsPlugin>();
        return await ios?.requestPermissions(
              alert: true,
              badge: true,
              sound: true,
            ) ??
            false;
      case TargetPlatform.macOS:
        final macos = _plugin.resolvePlatformSpecificImplementation<
            MacOSFlutterLocalNotificationsPlugin>();
        return await macos?.requestPermissions(
              alert: true,
              badge: true,
              sound: true,
            ) ??
            false;
      case TargetPlatform.linux:
      case TargetPlatform.windows:
      case TargetPlatform.fuchsia:
        return true;
    }
  }

  @override
  Future<void> scheduleExamReminder({
    required String id,
    required String title,
    required String body,
    required DateTime when,
  }) async {
    await _ensureInitialized();
    await _plugin.zonedSchedule(
      id: stableNotificationId(id),
      title: title,
      body: body,
      scheduledDate: _asZoned(when),
      notificationDetails: _details(),
      androidScheduleMode: AndroidScheduleMode.inexactAllowWhileIdle,
      payload: id,
    );
  }

  @override
  Future<void> cancelExamReminder(String id) async {
    await _ensureInitialized();
    await _plugin.cancel(id: stableNotificationId(id));
  }

  @override
  Future<void> showNow({
    required String id,
    required String title,
    required String body,
  }) async {
    await _ensureInitialized();
    await _plugin.show(
      id: stableNotificationId(id),
      title: title,
      body: body,
      notificationDetails: _details(),
      payload: id,
    );
  }

  @override
  Future<void> scheduleDaily({
    required String id,
    required String title,
    required String body,
    required int hour,
    required int minute,
  }) async {
    await _ensureInitialized();
    // One-shot at the next occurrence of hour:minute in device-local time.
    // rescheduleAll() runs on every app start, so the nudge is always
    // re-armed; this avoids needing a timezone-name plugin for a true
    // daily repeat (the plugin interprets repeats in the TZDateTime's zone,
    // and without the device's IANA name a repeat would drift for users
    // outside UTC).
    final now = DateTime.now();
    var next = DateTime(now.year, now.month, now.day, hour, minute);
    if (!next.isAfter(now)) {
      next = next.add(const Duration(days: 1));
    }
    await _plugin.zonedSchedule(
      id: stableNotificationId(id),
      title: title,
      body: body,
      scheduledDate: _asZoned(next),
      notificationDetails: _details(),
      androidScheduleMode: AndroidScheduleMode.inexactAllowWhileIdle,
      payload: id,
    );
  }

  @override
  Future<void> cancelAll() async {
    await _ensureInitialized();
    await _plugin.cancelAll();
  }
}
