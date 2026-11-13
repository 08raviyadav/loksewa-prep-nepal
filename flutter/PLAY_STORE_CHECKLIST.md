# Play Store Checklist — Outrank

Everything only **you** can do, in order. Nothing here needs me.

## 1. Keystore (once, on your Acer — ~5 min)

```bash
keytool -genkey -v -keystore ~/loksewa-release.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias loksewa
```

- It asks for a keystore password + your name/org. **Write the passwords
  down somewhere safe** — lose them and you can never update the app again.
- Back up `~/loksewa-release.jks` (USB stick / encrypted cloud). This file
  is your app's identity.

## 2. Wire the keystore into the build (~2 min)

```bash
cp android/key.properties.example android/key.properties
# then edit android/key.properties with your real passwords + the
# absolute path to ~/loksewa-release.jks
```

`android/key.properties` is git-ignored — it never leaves your machine.

## 3. Build the release bundle (~3 min)

```bash
flutter build appbundle --release
```

Upload file: `build/app/outputs/bundle/release/app-release.aab`

## 4. Play Console (~30 min first time)

1. Go to [play.google.com/console](https://play.google.com/console),
   pay the one-time $25 developer fee, create the app:
   **Outrank**, package `com.raviyadav.loksewa_vidyapeeth`.
2. Upload the `.aab` to **Testing → Internal testing** first — install it
   on your own phone from the Play Store link and tap through: quiz,
   mock, exam dates, courses, dashboard. (The debug APK from CI is
   unsigned — only good for smoke tests, never for the store.)
3. Fill in the store listing: use `assets/icon/app_icon.png` (1024×1024)
   as the icon, add 2–3 phone screenshots, short + full description
   (EN + NE), content rating questionnaire, privacy policy URL.
   The app collects **zero** data — say so in the Data Safety form
   (no location, no identifiers, no analytics).
4. Roll out to **Production** when the internal test feels solid.

## 5. Firebase push notifications (later, optional)

Local reminders (exam ≤3 days, daily challenge) already work with zero
setup. For push when the app is killed, follow `FIREBASE_SETUP.md` —
you create the Firebase project under your Google account and drop in
`google-services.json`; no code changes needed (the FCM hook is already
wired behind the `NotificationService` interface).

## Versioning

Bump `version: 1.0.0+1` in `pubspec.yaml` for each release
(`1.0.1+2`, `1.1.0+3`, …) — Play Console rejects re-uploads of the
same version code (the `+N` number).
