# LokSewa Vidyapeeth — Flutter app (Android)

**LokSewa Vidyapeeth (लोक सेवा विद्यापीठ)** — Nepal's biggest free,
open-source Lok Sewa exam practice platform, as a native Android app.
Package `com.raviyadav.loksewa_vidyapeeth`, v1.0.0+1.

- 100% free · Open source (MIT) · No login · No ads · **No tracking**
  (no analytics SDKs — that's a feature, not an oversight)
- Bilingual EN/NE from day one
- Offline-first: the question bank, exam dates, festivals and historical
  events ship bundled in the APK

This folder lives inside the web repo (`loksewa-prep-nepal`) so the app
and the website share one data source. The vanilla site in the repo root
stays live alongside the app.

## Layout

```
flutter/
  lib/                  # Dart source (see Architecture below)
  test/                 # 237 unit/widget tests (flutter test)
  assets/data/
    question_index.json # Flutter-only generated index (committed).
                        # All other data files are copied from ../data/
                        # at build time — see "Where the data comes from".
  android/              # Android shell (Gradle, manifest, res XML).
                        # Launcher PNGs + gradle-wrapper.jar are NOT
                        # committed — regenerated/downloaded by CI.
  tools/
    gen_launcher_icon.py# Draws the launcher icons + splash art
                        # (amber "लो" on navy) with Pillow.
  pubspec.yaml  pubspec.lock  analysis_options.yaml  .metadata
  PLAY_STORE_CHECKLIST.md   # maintainer steps for the Play Store
  FIREBASE_SETUP.md         # local reminders + optional FCM push
```

### Architecture

```
lib/
  main.dart                 # entry, theme wiring, bottom-nav root
  theme/app_theme.dart      # design system: saffron/indigo, dark+light,
                            #   4px spacing rhythm, Devanagari-friendly type
  l10n/*_strings.dart       # hand-rolled EN/NE tables (no intl codegen)
  models/                   # Question, Exam, ExamDate, CourseChapter —
                            #   JSON shapes mirror the web bank exactly
  utils/bs_calendar.dart    # Bikram Sambat engine (anchor 2026-10-31 = 2083-07-14)
  utils/countdown.dart      # pure countdown maths (DD:HH:MM:SS, pager, states)
  data/data_repository.dart # asset JSON loaders with in-memory cache
  state/                    # ChangeNotifiers: language, theme, progress,
                            #   community, course progress
  services/                 # NotificationService interface + local backend,
                            #   reminder scheduler (exam ≤3 days, daily nudge)
  widgets/                  # app_scaffold, countdown_card, stat_card, …
  screens/                  # home, practice, quiz, mock, exam dates,
                            #   courses, dashboard, history, community
```

## Where the data comes from

The web repo's `../data/` is the **single source of truth**. The app does
not keep its own copy of the shared files — they are copied into
`assets/data/` at build time (by CI, or by you locally before a build):

| Source (`../data/`) | Copied to | Contents |
|---|---|---|
| `exam-dates.json` | `assets/data/exam-dates.json` | 82 exam dates |
| `exams.json` | `assets/data/exams.json` | 47 exams |
| `festivals.json` | `assets/data/festivals.json` | 63 festivals |
| `historical-events.json` | `assets/data/historical-events.json` | 95 historical dates |
| `questions/*.json` | `assets/data/questions/` | 131 files, 64,671 questions |
| `courses/*.json` | `assets/data/courses/` | 3 course files |

`assets/data/question_index.json` is the exception: it is a Flutter-only
generated index (per-file question counts + exam/topic map) and **is**
committed with the project. The copied files are git-ignored (see
`.gitignore`) so a local build never accidentally commits a duplicate of
the bank.

To build or test locally, copy them first (from the repo root):

```bash
cp data/exam-dates.json data/exams.json data/festivals.json \
   data/historical-events.json flutter/assets/data/
cp -r data/questions data/courses flutter/assets/data/
```

## Run locally

Prerequisites: Flutter SDK (stable), Android Studio with an Android SDK,
and a device/emulator (or the OnePlus 11R over USB).

```bash
cd flutter
flutter pub get
flutter analyze        # must be clean (0 issues)
flutter test           # 237 tests (needs the data files copied in, above)
flutter run            # debug build on the connected device
```

Two things a fresh clone is missing (both are binary, so neither is
committed — see below):

1. **Launcher icons + splash art.** Generate them once:
   ```bash
   pip install pillow
   sudo apt-get install -y fonts-noto-core   # Ubuntu/Debian; provides
                                             # Noto Sans Devanagari Bold
   python3 tools/gen_launcher_icon.py
   ```
   This draws all 17 PNGs (5 launcher densities, 5 adaptive foregrounds,
   5 splash images, 2 solid splash backgrounds) from the amber "लो" on
   navy design. `flutter build` fails without them (the manifest
   references `@mipmap/ic_launcher`).
2. **gradle-wrapper.jar.** `flutter build` needs it; download the jar
   matching `android/gradle/wrapper/gradle-wrapper.properties`
   (Gradle 9.3.1):
   ```bash
   curl -fSL -o android/gradle/wrapper/gradle-wrapper.jar \
     https://raw.githubusercontent.com/gradle/gradle/v9.3.1/gradle/wrapper/gradle-wrapper.jar
   ```
   (Or run `gradle wrapper` if you already have Gradle installed.)

### Debug vs release signing

- **Debug builds** (`flutter run`, `flutter build apk --debug`) use the
  debug keystore automatically — no setup needed.
- **Release builds** (`flutter build apk --release`,
  `flutter build appbundle --release`) read signing from environment
  variables (see `android/app/build.gradle.kts`):
  ```bash
  export KEYSTORE_PATH="$HOME/loksewa-release.jks"
  export KEYSTORE_PASSWORD="<keystore password>"
  export KEY_ALIAS=loksewa
  export KEY_PASSWORD="<key password>"
  ```
  Without them, a release build silently falls back to the debug key —
  fine for local testing, **never** for distribution. Generate the
  keystore once with `keytool` (see `PLAY_STORE_CHECKLIST.md` step 1)
  and back it up: losing it means losing Play Store updates. There is
  no `key.properties` file anymore; do not create one.

## CI — signed release APK

`.github/workflows/flutter-release.yml` (repo root) builds the signed
release APK on every push to `main` that touches `flutter/**` or
`data/**`, and on manual dispatch. One job, `ubuntu-latest`:

1. Checks out the repo; sets up Java 17 (Temurin) + Flutter stable.
2. **Fails fast if the signing secrets are missing** — it never ships a
   debug-signed "release". Required repository secrets:
   `ANDROID_KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`,
   `KEY_PASSWORD`.
3. Decodes the keystore to `$RUNNER_TEMP/loksewa-release.p12`.
4. Copies `../data/` → `flutter/assets/data/` and **verifies the counts**
   (82/47/63/95, 131 question files, 3 course files) — the job fails on
   any mismatch, so a half-synced bank can never ship.
5. Generates the launcher icons (`tools/gen_launcher_icon.py`, after
   installing Pillow + `fonts-noto-core`).
6. Downloads `gradle-wrapper.jar` (Gradle 9.3.1, checksum-verified) and
   restores the `+x` bit on `gradlew` (snapshot pushes lose it).
7. Runs `flutter pub get`, `flutter analyze`, `flutter test`, then
   `flutter build apk --release` with the signing env vars set.
8. Publishes `app-release.apk` to the `android-v1.0.0` GitHub release
   (created or updated), as a direct download — no sign-in needed.

Bump `version: 1.0.0+1` in `pubspec.yaml` for each release, and update
the release tag in the workflow to match (`android-vX.Y.Z`).

## Platforms

Only **Android** ships from this folder. The `ios/`, `macos/`,
`windows/`, `linux/` and `web/` platform directories from the original
standalone project were deliberately omitted: they contain binary assets
and are not needed for the Android release. They can be regenerated
later with:

```bash
flutter create --platforms=ios,macos,windows,linux,web .
```

(run from this folder; it re-creates the platform shells without
touching `lib/`). The web build of the app is a separate concern from
the vanilla site in the repo root, which is what serves
loksewa-prep-nepal today.

## Push notifications

Exam reminders (exam ≤3 days, daily practice nudge) work locally with
zero setup via `flutter_local_notifications`. Server push is optional —
see `FIREBASE_SETUP.md`. No Firebase project exists yet, and none is
required for what ships today.
