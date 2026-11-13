# Push / Local Notifications — Setup & Integration (Milestone 7)

**Status: local notifications are fully wired. No Firebase project exists yet,
and none is required for what ships today.** Everything below marked
"for you (Ravi)" is a manual step only you can do (Google account, Play
console). Nothing here puts keys in the repo — ever.

## What works right now (no Firebase needed)

- `lib/services/notifications.dart` — the `NotificationService` interface
  (extended with `showNow`, `scheduleDaily`, `cancelAll`; old methods
  unchanged). `createNotificationService()` picks the backend at compile
  time: **stub on web**, `flutter_local_notifications` on
  Android/iOS/macOS/Linux/Windows.
- `lib/services/reminder_scheduler.dart` — `rescheduleAll()`:
  cancel-all-then-schedule, idempotent. Schedules:
  - one reminder per remaining day for each reminded exam **≤ 3 days away**,
    at 09:00 local — `⏰ {exam} in N days` (Nepali when the app is in Nepali);
  - the daily practice nudge at the user's chosen morning hour
    (default **07:00**, prefs `loksewa_daily_nudge_v1`,
    `loksewa_daily_nudge_hour_v1`, `loksewa_daily_nudge_minute_v1`).
- Android 13+ `POST_NOTIFICATIONS` is requested at runtime; scheduling uses
  **inexact** alarms so no exact-alarm permission is needed. `RECEIVE_BOOT_COMPLETED`
  + the plugin's receivers are in `AndroidManifest.xml` so reminders survive reboots.
- **Web is untouched**: the stub no-ops and the vanilla site's on-open
  in-app banner stays the web fallback. `flutter build web` must keep passing.

## Integration — one line in `lib/main.dart` (final integration step)

In `main()`, after `AppState().init()` (so prefs are loaded) and before/after
`runApp`, add:

```dart
import 'package:loksewa_vidyapeeth/services/reminder_scheduler.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final appState = AppState();
  await appState.init();
  await rescheduleAll(); // <-- Milestone 7: arm exam reminders + daily nudge
  runApp(AppStateScope(state: appState, child: const OutrankApp()));
}
```

`rescheduleAll()` is safe on web (stub no-ops) and cheap (~ms), so calling it
on every cold start is the intended pattern — it also re-arms the daily nudge.
Also call it after the user toggles a reminder or changes the nudge hour.

## Firebase checklist — for you (Ravi), only when you want server push

Local reminders cover the exam countdown. Add Firebase **only** if you later
want server-driven pushes (e.g. "new exam date announced", broadcast to all
installs). Steps:

1. **Create the Firebase project** at https://console.firebase.google.com
   (name it e.g. `loksewa-vidyapeeth`). No code changes needed for this step.
2. **Add the Android app**: package name `com.raviyadav.loksewa_vidyapeeth`
   (matches `android/app/build.gradle.kts`). Download `google-services.json`
   → place at `android/app/google-services.json`.
3. **Add the iOS app**: bundle id `com.raviyadav.loksewaVidyapeeth`
   (matches `ios/Runner.xcodeproj`). Download `GoogleService-Info.plist`
   → place at `ios/Runner/GoogleService-Info.plist` (add via Xcode so it
   lands in the target).
4. **Keep them out of git.** This repo is public and the zero-tracking
   promise is a feature — add to `.gitignore`:
   ```
   android/app/google-services.json
   ios/Runner/GoogleService-Info.plist
   lib/firebase_options.dart
   ```
   CI builds that need them should inject them as secrets, never commits.
5. **Generate the options file** (needs your Google login, one time):
   ```
   dart pub global activate flutterfire_cli
   flutterfire configure --project=<your-project-id>
   ```
   then add `firebase_core` + `firebase_messaging` to pubspec.
6. **FCM server key stays server-side.** Sending pushes uses the Firebase
   Admin SDK from your own server/Cloud Function. Never embed a server key,
   service-account JSON, or FCM legacy key in the app, the repo, or any
   artifact. The `google-services.json` client file is *not* a secret, but
   per (4) we still keep it out of this public repo.
7. **Flip to FCM** — implement one class, swap one line:
   ```dart
   class FcmNotificationService implements NotificationService {
     // requestPermission() -> FirebaseMessaging.instance.requestPermission()
     // exam reminders     -> keep the LOCAL scheduler (on-device, offline,
     //                       zero server cost) — FCM is only for broadcasts:
     //   await FirebaseMessaging.instance.subscribeToTopic('announcements');
   }
   ```
   Then point `createService()` (or the `main.dart` wiring) at
   `FcmNotificationService`. The `NotificationService` interface does not
   change, so screens are untouched. Recommended split long-term:
   **local** = exam reminders + daily nudge (offline, private);
   **FCM** = announcements topic only.

## Manual test steps (real device)

1. `flutter run` on an Android 13+ phone. Grant the notification permission
   when prompted (deny once to verify the app still works — reminders just
   won't display).
2. In the app, open Exam Dates → tap "Remind me" on an exam ≤ 3 days away.
3. Background the app. Change the device clock to 08:59, wait for 09:00 →
   expect `⏰ {exam} in N days`. (Inexact alarms may drift a few minutes —
   that is by design, no exact-alarm permission needed.)
4. Daily nudge: set the nudge hour to one minute in the future via prefs
   (or temporarily hardcode), background the app, wait → expect the
   `🎯 Daily challenge` notification.
5. Reboot the phone → reminders still fire (boot receiver).
6. Web: `flutter build web --release --no-web-resources-cdn` must succeed;
   opening the site shows the in-app reminder banner, no permission prompt.
7. Toggle a reminder off → `rescheduleAll()` runs → no notification fires.

## Automated verification (this milestone)

- `flutter analyze` — clean.
- `flutter test test/reminder_scheduler_test.dart` — 20 tests: lead-window
  decisions, past/far/malformed dates, per-day fan-out, past-fire-time skip,
  idempotent re-run, nudge on/off/custom time/tomorrow rollover, EN/NE
  bodies, prefs wiring, broken-feed degradation, stable notification ids.
- `flutter build web --release --no-web-resources-cdn` — the critical gate.
