/// Notification service behind an interface.
///
/// Milestone 7 wires real local notifications via `flutter_local_notifications`
/// on mobile/desktop. The web build keeps the stub (no-op) — the vanilla
/// site's on-open in-app banner remains the web fallback.
///
/// The interface is unchanged in contract and only extended: screens depend
/// on [NotificationService], and [createNotificationService] picks the right
/// backend at compile time:
///   - web (`dart.library.html`)      -> [StubNotificationService] (no-op)
///   - Android/iOS/macOS/Linux/Windows -> [LocalNotificationService]
///     (see notification_backend_local.dart)
///
/// Real server-driven push (FCM) is a later step — see FIREBASE_SETUP.md.
/// No Firebase keys live in this repo, ever.
library;

import 'notification_backend_stub.dart'
    if (dart.library.io) 'notification_backend_local.dart' as backend;

abstract class NotificationService {
  /// Ask the OS for permission. Returns true if granted.
  /// Android 13+: requests POST_NOTIFICATIONS. iOS/macOS: alert+badge+sound.
  Future<bool> requestPermission();

  /// Schedule a one-shot local reminder for [when] (local time). No-op in
  /// the stub. Re-scheduling the same [id] replaces the previous one.
  Future<void> scheduleExamReminder({
    required String id,
    required String title,
    required String body,
    required DateTime when,
  });

  /// Cancel a scheduled reminder. No-op in the stub.
  Future<void> cancelExamReminder(String id);

  /// Show an immediate notification. No-op in the stub.
  Future<void> showNow({
    required String id,
    required String title,
    required String body,
  });

  /// Schedule a daily notification at [hour]:[minute] local time
  /// (e.g. the morning practice nudge). Re-scheduling the same [id]
  /// replaces the previous one. No-op in the stub.
  Future<void> scheduleDaily({
    required String id,
    required String title,
    required String body,
    required int hour,
    required int minute,
  });

  /// Cancel every notification scheduled through this service. The
  /// reminder scheduler calls this before re-scheduling, which makes
  /// [rescheduleAll] idempotent.
  Future<void> cancelAll();
}

/// Picks the platform backend. On web this is the no-op stub so
/// `flutter build web` never touches native notification APIs.
NotificationService createNotificationService() => backend.createService();

class StubNotificationService implements NotificationService {
  @override
  Future<bool> requestPermission() async => false;

  @override
  Future<void> scheduleExamReminder({
    required String id,
    required String title,
    required String body,
    required DateTime when,
  }) async {
    // Web fallback: the in-app reminder banner covers this case.
  }

  @override
  Future<void> cancelExamReminder(String id) async {}

  @override
  Future<void> showNow({
    required String id,
    required String title,
    required String body,
  }) async {}

  @override
  Future<void> scheduleDaily({
    required String id,
    required String title,
    required String body,
    required int hour,
    required int minute,
  }) async {}

  @override
  Future<void> cancelAll() async {}
}
