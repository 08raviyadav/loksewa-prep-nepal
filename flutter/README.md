# Outrank — Flutter app

**Outrank** — Nepal's biggest free, open-source
Lok Sewa exam practice platform, rebuilt as a professional Flutter app:
**one codebase → Android + iOS + Web.**

This is now THE app codebase going forward. The vanilla HTML/CSS/JS site in
`../loksewa-prep-nepal/` stays live until this app reaches feature parity.

- 100% free · Open source (MIT) · No login · No ads · **No tracking**
  (no analytics SDKs — that's a feature, not an oversight)
- Bilingual EN/NE from day one
- Offline-first: the entire question bank ships bundled in `assets/`

## Architecture

```
lib/
  main.dart            # entry, theme wiring, bottom-nav root
  theme/app_theme.dart # design system: saffron/indigo, dark+light,
                       #   4px spacing rhythm, Devanagari-friendly type —
                       #   ported 1:1 from the vanilla site's CSS tokens
  l10n/app_strings.dart# hand-rolled EN/NE tables (no intl codegen yet;
                       #   translators edit one obvious file)
  models/models.dart   # Question, Exam, ExamDate, CourseChapter —
                       #   JSON shapes mirror the vanilla bank exactly
  utils/bs_calendar.dart # Bikram Sambat engine (anchor 2026-10-31 = 2083-07-14)
  utils/countdown.dart # pure countdown maths (DD:HH:MM:SS, pager, states)
  data/data_repository.dart # asset JSON loaders with in-memory cache
  state/app_state.dart # ChangeNotifier: language, theme, reminders
                       #   (lean on purpose — no Riverpod/Bloc until earned)
  services/notifications.dart # NotificationService interface + stub
  widgets/             # app_scaffold, countdown_card, reminder_banner, …
  screens/             # home_screen, practice_screen, … (Phase 2 below)
assets/data/           # exams.json, exam-dates.json, questions/*.json
test/                  # bs_calendar_test, countdown_test, models_test
```

## How the JSON data maps

All data files are shared verbatim with the vanilla site (`../loksewa-prep-nepal/data/`):

| File | Model | Notes |
|---|---|---|
| `data/exams.json` | `Exam` | 47 exams; only `id`/`name`/`name_ne` are read |
| `data/exam-dates.json` | `ExamDate` | 20 verified dates; BS `YYYY-MM-DD` strings |
| `data/questions/*.json` | `Question` | 131 files, 64,671 questions; `answer` = option index |
| `data/courses/*.json` | `CourseChapter` | chapter-wise bilingual theory (framework-agnostic) |

Copy new/updated files into `assets/data/` when the bank changes.
The full bank is ~large; Phase 1 bundles a sample question file, Phase 2
adds a per-exam file manifest so screens load only what they need.

## Run

```bash
flutter pub get
flutter run            # device / emulator
flutter run -d chrome  # web
flutter build web --release   # static output for Vercel / GitHub Pages
```

CI (`.github/workflows/build.yml`): `flutter analyze` + `flutter test` +
`flutter build web` on every push to main.

## Push notifications

Exam reminders are the killer feature for native apps. The app depends only
on the `NotificationService` interface (`lib/services/notifications.dart`);
Phase 1 ships a stub so everything compiles without native plugins.

To go live (needs Ravi's Firebase project — **do not create one on his
behalf, do not hardcode keys**):

1. Create a Firebase project, add Android / iOS / Web apps, download the
   config files (`google-services.json`, `GoogleService-Info.plist`).
2. Add `firebase_core` + `firebase_messaging` to `pubspec.yaml`.
3. Implement `FcmNotificationService implements NotificationService`
   (see the documented steps at the bottom of `notifications.dart`).
4. Swap one line in `main.dart` — screens never touch FCM directly.

For on-device scheduled reminders without a server,
`flutter_local_notifications` is the lighter alternative.

## Roadmap — Phase 2 port priority

1. **Quiz runner** — practice session: shuffled Q&A, timer, negative marking,
   instant feedback, bookmarks, wrong-answer review, results screen
   (mirrors the vanilla practice engine + real cutoffs)
2. **Mock exams** — exact patterns (Kharidar 50Q/45min etc.), OMR palette,
   auto-submit, printable paper
3. **Exam Dates screen** — full list, kind filters, countdown chips
4. **Courses** — chapter reader, progress rings, "Practice this chapter"
   deep-links (data is ready: `data/courses/*.json`, 56 chapters)
5. **Dashboard** — XP, streak, weak-topic analysis, personal records
6. **FCM push** — real exam-reminder notifications (see above)
7. **Discussion Hub / Submit-a-Question** — needs the Supabase backend
   (`../loksewa-prep-nepal/docs/BACKEND.md`); ships after backend exists
8. **Festival wishes** — greeting card on festival days (same behaviour as
   the web portal: card + tomorrow teaser + upcoming strip, dismissible per
   window). Data is ready: `assets/data/festivals.json` (63 verified
   festivals, Kartik 2083 → Chaitra 2084; Eid al-Fitr / Bakr Eid excluded
   per user instruction — see `../loksewa-prep-nepal/CONTRIBUTING.md`).
   Needs the BS calendar window logic ported, not the data.
9. **Play Store release** — app bundle, store listing, privacy policy
10. **Historical events / Dates to Remember** — ✅ DONE 2026-11-12:
    On This Day card on Home (renders nothing on a quiet day), full
    list with search + category filter + "Quiz me" flashcards, with
    the web portal's behaviour (only `day_bs` entries recur; dateless
    entries excluded from quiz; medium-confidence ⚠️ re-verify marks;
    dates never render "null"). Data: `assets/data/historical-events.json`
    (95 verified dates; 19 with a BS month/day, 8 year-only in text).
    The Flutter matcher additionally applies the corrected BS month
    lengths (a day that doesn't exist in that year's month, e.g.
    Mangsir 30 in 2083, never matches). Still open: My Day digest
    merge — waits on the birthday / My Day feature (roadmap item 8).

## Painful-to-port watchlist (flagged early)

- **The 3,804-line vanilla practice/mock engine** (`app.js`) mixes UI,
  timing, scoring and persistence. Port it as a clean `QuizEngine`
  (pure Dart, fully unit-tested) *before* building quiz UI — don't port
  the spaghetti, port the behavior.
- **localStorage key parity**: keep key names (`loksewa_*_v1`) so users
  switching between web portal and app don't lose progress where the
  platforms share storage semantics.
- **Devanagari shaping on old Android**: system fonts handle it, but test
  on a real low-end device; the vanilla site's line-height rules
  (>=1.5 body) are already in `AppType`.
- **Asset size**: the full question bank as bundled JSON will bloat the
  APK/IPA. Plan: ship per-exam packs, download-on-demand later, or keep
  the heavy bank web-only. Decide before the Play Store build.
