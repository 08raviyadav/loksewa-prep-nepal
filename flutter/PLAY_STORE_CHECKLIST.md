# Play Store Checklist — LokSewa Vidyapeeth

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

Release signing reads **environment variables** — there is no
`key.properties` file anymore. Export them in your shell before building
(or put them in `~/.bashrc` / `~/.zshrc`):

```bash
export KEYSTORE_PATH="$HOME/loksewa-release.jks"
export KEYSTORE_PASSWORD="<keystore password>"
export KEY_ALIAS=loksewa
export KEY_PASSWORD="<key password>"
```

Without these, a release build falls back to the **debug** keystore (fine
for local testing, never for the store). CI uses the same variables from
GitHub Actions secrets — see `.github/workflows/flutter-release.yml`.

## 3. Build the release bundle (~3 min)

```bash
flutter build appbundle --release
```

Upload file: `build/app/outputs/bundle/release/app-release.aab`

## 4. Play Console (~30 min first time)

1. Go to [play.google.com/console](https://play.google.com/console),
   pay the one-time $25 developer fee, create the app:
   **LokSewa Vidyapeeth**, package `com.raviyadav.loksewa_vidyapeeth`.
2. Upload the `.aab` to **Testing → Internal testing** first — install it
   on your own phone from the Play Store link and tap through: quiz,
   mock, exam dates, courses, dashboard. (The signed release APK from
   GitHub Releases is the same build, signed with the same key — good
   for a quick install check before the store upload.)
3. Fill in the store listing: use the 1024×1024 icon produced by
   `python3 tools/gen_launcher_icon.py --store-icon app-icon-1024.png`
   (downscale it to 512×512 for the store's icon slot — the
   generator's master is square 1024×1024), add 2–3 phone screenshots,
   short + full description (EN + NE), content rating questionnaire,
   privacy policy URL.
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
