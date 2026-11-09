# Contributing to LokSewa Vidyapeeth — लोक सेवा विद्यापीठ · लोक सेवा तयारी

Thank you for helping Nepal's aspirants. Please read this before opening a pull request.

## Who decides

**Maintainer: Ravi Yadav ([@08raviyadav](https://github.com/08raviyadav)).** He reviews every pull request and issue, and **accepts or rejects each one himself**. There is no auto-merge, no bot approval, and no guarantee a PR will be merged — even a good one, if it duplicates work, conflicts with the syllabus, or doesn't fit the project. If your PR is closed, it is a decision, not a judgement on your effort; you are welcome to ask why in the PR thread.

## How to contribute

1. Fork the repo, create a branch (`add-questions-geography`, `fix-mock-timer`).
2. Keep changes small and focused — one topic / one fix per PR.
3. Run the tests before submitting: `node scripts/test-questions.js`, `node scripts/test-app.js`, `node scripts/test-e2e.js` and `node scripts/test-v2.js`. All four must pass (exit 0).
4. Fill in the pull-request template completely. Link the issue if there is one.
5. Write PR titles and descriptions in English.

## Adding questions — the accuracy rule (most important)

Every question must be **factually correct and verifiable**. This is an exam-prep site: a wrong answer actively harms a student.

- Use the exact JSON schema in the README. `id` must be unique (prefix per file, sequential). Exactly 4 distinct options. `answer` is the index (0–3) of the correct option — double-check it.
- Only add facts you are confident about, with a one-sentence explanation. If you are unsure of a date, number or name, **leave that question out**.
- No invented dates, vacancy numbers, or "current affairs" that will go stale. Current-affairs questions must cite a stable, checkable fact.
- No duplicate question text (the validator rejects it). No placeholder / lorem questions.
- Tag `exam` only with exams whose syllabus genuinely includes the topic. Valid tags (all 47 exam ids — enforced by `node scripts/test-questions.js`, see `VALID_EXAMS` there):
  - PSC: `kharidar`, `nasu`, `section-officer`, `deputy-secretary`, `psc-service-groups`, `provincial-psc`, `ranger`, `jta`, `nea`, `judicial-service`
  - Teaching: `tsc-primary`, `tsc-lower-secondary`, `tsc-secondary`, `tsc-license`
  - Banking: `nrb-assistant`, `nrb-officer`, `rbb`, `rbb-senior-assistant`
  - Uniformed: `police`, `army`
  - Technical / engineering: `engineering`, `sub-engineer`, `computer-operator`, `nepal-telecom`, `foreign-service`, `health`
  - Licence: `nmc-mbbs`, `nmc-bds`, `nnc-rn`, `midwifery-nlem`, `nhpc-ha`, `nhpc-lab`, `nhpc-radio`, `nhpc-physio`, `nhpc-public-health`, `nhpc-optometry`, `nhpc-dental`, `nhpc-ayurveda`, `npc-pharmacy`, `staff-nurse-psc`
  - Entrance / guide-only: `mecee-bl`, `nec-licence`, `bar-council`, `csit-entrance`, `ioe-entrance`, `anm-guide`, `ayurveda-bams`
- `marks` is 1 or 2 only. `difficulty` is `easy`, `medium` or `hard`.
- For maths/IQ questions, show the working in `explanation` and verify the calculation.
- Prefer Nepali context (Nepal history, Constitution 2072, geography, economy) over generic trivia.

Use the **Question contribution** issue template to propose a batch of questions before writing a large PR.

## Revision notes

Each topic can have a one-page revision note: key facts, formulas, article numbers and dates, in English **and** Nepali. Notes live in `data/notes/`, **one JSON file per topic** — this keeps PRs small and reviewable (one topic per PR, same as questions).

### File format

Create `data/notes/<slug>.json` and add the filename to `NOTES_FILES` in `assets/js/app.js` (keep the list sorted — `node scripts/test-app.js` enforces it).

```json
{
  "slug": "constitution-governance",
  "topic": "Constitution & Governance",
  "title_en": "Constitution & Governance — one-pager",
  "title_ne": "संविधान र शासन — एक-पृष्ठीय नोट",
  "updated": "2026-10-31",
  "source_note": "Facts cross-checked against the app's question bank and standard references.",
  "bullets": [
    { "en": "Promulgated: 3 Ashoj 2072 (20 September 2015).",
      "ne": "जारी मिति: 2072 असोज 3 (20 सेप्टेम्बर 2015)।" },
    { "en": "35 parts, 308 articles, 9 schedules.",
      "ne": "35 भाग, 308 धारा, 9 अनुसूची।" }
  ]
}
```

### Rules

- **Bilingual is mandatory** — every bullet needs both `en` and `ne`, and both `title_en` / `title_ne`. The app shows the Nepali text when the language toggle is on Nepali.
- **10–20 bullets per note.** Tight one-pagers: the facts students actually get asked, not a textbook chapter.
- **`topic` must match a question `topic` exactly** (e.g. `Constitution & Governance`). This is what the "📖 Revise this topic" button on wrong-answer review uses to jump to the right note — a mismatch means the button won't find it.
- **`slug`** is lowercase with hyphens, matching the filename (`constitution-governance.json`).
- **The accuracy rule applies to notes too**: only facts you are confident about and can verify — no invented dates, numbers or article references. Cross-check against the question bank (`data/questions/`) where possible.
- **`updated`** is the date you last verified the facts (`YYYY-MM-DD`).
- Run `node scripts/test-app.js` before submitting — it validates the schema of every note file.

## Theory courses

Chapter-wise bilingual theory so students can **read** the syllabus, not just practise MCQs. Courses live in `data/courses/`, **one JSON file per exam** (Phase 1: `kharidar.json`, `nayab-subba.json`, `section-officer.json` — First Paper only). Add the filename to `COURSE_FILES` in `assets/js/app.js` (keep the list sorted — `node scripts/test-courses.js` enforces it).

### File format

```json
{
  "exam": "kharidar",
  "exam_name_en": "Kharidar (Non-Technical)",
  "exam_name_ne": "खरिदार (अप्राविधिक)",
  "paper": "First Paper — General Knowledge & General Mental Ability",
  "confidence": "medium",
  "confidence_note_en": "Official psc.gov.np PDF not directly reachable; structure converged across 5+ independent syllabus reproductions + the portal's SOURCES.md.",
  "sources": ["loksewatayariapp.com syllabus page", "data/SOURCES.md"],
  "subjects": [{
    "name_en": "Geography & the Solar System",
    "name_ne": "भूगोल र सौर्यमण्डल",
    "weight_marks": null,
    "chapters": [{
      "id": "kharidar-solar-system",
      "title_en": "Solar System & the Earth",
      "title_ne": "सौर्यमण्डल र पृथ्वी",
      "theory_en": "150–400 words of real study-note prose…",
      "theory_ne": "150–400 words of real Nepali (Devanagari)…",
      "key_points": [{ "en": "…", "ne": "…" }],
      "linked_topics": ["Nepal Geography"]
    }]
  }]
}
```

### Rules

- **Syllabus honesty first** — the subject → chapter structure must match the official PSC syllabus. Research it on psc.gov.np. If the official PDF is unreachable, converge across multiple independent reproductions + the portal's `data/SOURCES.md`, set `confidence: "medium"`, and say so in `confidence_note_en`/`ne`. Never invent syllabus structure or per-unit mark splits.
- **Bilingual is mandatory** — `theory_en` **and** `theory_ne` (150–400 words each, real Nepali not machine-garbled), every key point needs `en` + `ne`, every title/subject name needs both languages.
- **5–10 key points per chapter.** Real facts only — the accuracy rule applies: cross-check against `data/SOURCES.md` verified facts; where uncertain, keep it general-but-true rather than specific-but-wrong. No lorem/TODO.
- **`linked_topics` must be copied exactly from the 16 verified question-bank tags** (see `node scripts/test-courses.js` `VERIFIED_TAGS`) — this powers the "✏️ Practice this chapter" buttons. Every linked topic must have ≥1 question tagged for the course's exam (the test enforces this; `test-courses.js` maps course → exam id via `COURSE_EXAM_MAP`).
- **Chapter `id`** is `<exam-prefix>-<slug>`, unique across all courses (`kharidar-*`, `nasu-*`, `so-*`).
- **`weight_marks`** is the official mark weight if published, else `null` — never guessed.
- Progress is stored on-device in `loksewa_course_progress_v1` (`{done:{chapterId:true}, last:{exam,chId,ts}}`); pure helpers (`flattenCourseChapters`, `calcCourseProgress`, `subjectProgress`, `courseChapterById`, `courseByExam`) are exported from `app.js` for tests.
- Run `node scripts/test-courses.js` before submitting — it validates schema, word counts, bilingual completeness, tag validity, and bank coverage.

## Contributing a question through the site (no PR needed)

You can also submit a question from the site itself: **Contribute → Submit a Question**.
The form shows the exact format first (copyable template below) and validates as you type.

### Format template (copy this — every field is required unless noted)

```json
{
  "id": "COMM-000",
  "exam": ["kharidar", "nasu"],
  "topic": "Constitution & Governance",
  "subtopic": "Fundamental Rights",
  "difficulty": "medium",
  "marks": 2,
  "question": "Which article of the Constitution of Nepal 2072 guarantees the right to freedom?",
  "question_ne": "नेपालको संविधान २०७२ को कुन धाराले स्वतन्त्रताको हकको ग्यारेन्टी गर्छ?",
  "options": ["Article 17", "Article 18", "Article 19", "Article 20"],
  "options_ne": ["धारा १७", "धारा १८", "धारा १९", "धारा २०"],
  "answer": 0,
  "explanation": "Article 17 guarantees the right to freedom.",
  "explanation_ne": "धारा १७ ले स्वतन्त्रताको हकको ग्यारेन्टी गर्छ।",
  "source": "Constitution of Nepal 2072, Part 3"
}
```

### Community question rules

- **Bilingual is mandatory.** Every question needs the English AND Nepali question, all 4 options in both languages, and both explanations. The bank is 100% bilingual and stays that way.
- **Question at least 15 characters.** Exactly 4 options per language, all different.
- **Answer must be A–D** and point at the correct option — double-check it.
- **Source is required** — a URL or a book / article / Act name. The source field is the only place links go; never put a link inside the question text.
- **One question per submission.** Small, focused submissions review faster than bulk dumps.

### Moderation policy — read this before you submit

> ⚠️ **Instant live + no spam cannot both be true.** Your submission does **not** go live when you send it. It goes through automatic checks (duplicate detection, spam heuristics, rate limit) **and** human review. **First-time submissions never go live instantly.**

1. **Automatic checks (first line of defence, not the real gate):** exact-duplicate and near-duplicate detection against the full bank (token-Jaccard ≥ 0.8 warns/blocks), spam heuristics (no links in question text, no repeated characters, no mostly-ALL-CAPS text), max **5 submissions per hour per device**.
2. **Maintainer review:** Ravi Yadav reviews every pending submission and **approves or rejects each one himself**. He may edit a question before approving it (fix a typo, tighten wording) — the approved version is what goes live.
3. **Approved** questions join the practice bank with a **"Community"** badge and your name in the source line. **Rejected** submissions get a reason, shown in the public moderation log (approved / rejected / pending counts are on the Contribute page).
4. **Trusted-contributor rule:** contributors with **3+ approved questions and 0 rejections** get faster review. It is not auto-approval — every question is still reviewed.
5. There is no auto-merge, no bot approval, and no guarantee a submission will be accepted — even a good one, if it duplicates work, conflicts with the syllabus, or doesn't fit the project.

### Spam policy

The following are blocked automatically and, if repeated, count against your contributor record:

- Links anywhere except the source field; repeated characters (`!!!!!`); mostly ALL-CAPS text; questions under 15 characters.
- Submitting the same question 3 times (it is already in the review queue — wait for the decision).
- More than 5 submissions in an hour (rate limit — you will see how many minutes remain).
- Bulk low-effort dumps, copied question sets, or questions with invented facts. These are rejected and, if repeated, the contributor's future submissions are deprioritised.

In demo mode these checks run in your browser (localStorage); after the backend is connected (see `docs/BACKEND.md`) they also run server-side, where they cannot be bypassed — client-side checks are the first line of defence, **server review is the real gate**.

## Reporting a wrong question

On the site, use the **⚑ Report wrong question** button on any question (quiz, result review, bookmarks, or search) — pick a reason and say what is wrong and what it should be, with a source if you can. Reports go to the maintainer's review queue.

Or open a bug report with the **question ID** (e.g. `HIST-042`), what is wrong, and the correct answer with a source. Do not just say "this is wrong".

## Exam dates (`data/exam-dates.json`) — the no-guessed-dates rule

Upcoming exam / admit-card / application-deadline dates live in `data/exam-dates.json` and power the home-page reminder banner, the Exam Dates view and the on-device reminder notifications. **Never invent a date.** Every entry must be verified against an official source (psc.gov.np, tsc.gov.np, nrb.org.np, mec.gov.np, police/apf/army sites, provincial PSC sites). If a date cannot be verified on an official page, the entry does not ship.

### Entry format

```json
{
  "id": "nasu-second-paper-2083-08",
  "exam": "nasu",
  "kind": "exam",
  "date_bs": "2083-08-02",
  "title_en": "Nayab Subba Second Paper exam",
  "title_ne": "नायब सुब्बा दोस्रो पत्र परीक्षा",
  "source": "https://psc.gov.np/...",
  "verified": "2026-10-31"
}
```

- `id`: unique slug. `exam`: an `exams.json` id so the row links to Practice/Mock (or `null` when no matching exam exists — the entry still shows, without practice links).
- `kind`: `exam` | `admit` | `deadline`.
- `date_bs`: `YYYY-MM-DD` zero-padded Bikram Sambat. Compared lexicographically; must be a real BS calendar date.
- `title_en` / `title_ne`: short bilingual titles. `source`: the official URL where the date was verified. `verified`: the AD date it was checked.
- `confidence` (optional): `high` = named official notice reproduced by 2+ independent outlets; `medium` = named official notice reproduced by one outlet (re-verify via live browser before the next refresh). Never ship below `medium`.
- BS maths in the app is anchored at 2026-10-31 AD = 2083-07-14 BS (see `BS_ANCHOR_AD` in `assets/js/app.js`); month lengths were corrected 2026-11-09 — 2083 Mangsir 29d / Poush 30d, 2084 Magh 29d / Falgun 30d (evidence: Poush 1, 2083 = 16 Dec 2026; Maha Shivaratri = Falgun 11, 2084 = 23 Feb 2028). There is no 2085 table yet — dates past Chaitra 2084 need the 2085 patro before they can be resolved.
- Stale entries (past dates) are rejected by `scripts/test-examdates.js` — refresh or drop them when re-verifying.

## Festivals (`data/festivals.json`) — the no-guessed-dates rule

Festival dates live in `data/festivals.json` and power the Home-page festival-wishes card (greeting + accent styling + confetti on the day, a "Tomorrow: {festival}" teaser the day before, an "Upcoming festivals" strip of the next 3). **Never invent a date.** Every entry must be verified against a Nepali patro source (ashesh.com.np full patro is the primary source; a second source per row where possible). Lunar dates vary year to year — if a date cannot be verified, the entry does not ship. `scripts/gen-festivals.py` generates the file; verify the generator with `python3 -m py_compile` only, never import it.

### Entry format

```json
{
  "id": "tihar-gai-2026",
  "name_en": "Gai Tihar",
  "name_ne": "गाइतिहार",
  "start_bs": "2083-07-23",
  "end_bs": "2083-07-23",
  "greeting_en": "Happy Gai Tihar! ...",
  "greeting_ne": "गाइतिहारको शुभकामना! ...",
  "emoji": "🐄",
  "accent": "#f97316",
  "confidence": "high",
  "source": "https://www.ashesh.com.np/nepali-calendar/?year=2083&month=Kartik",
  "verified": "2026-11-09"
}
```

- `id`: unique kebab-case slug + AD year (e.g. `tihar-bhai-tika-2026`; Tol Lhosar occurs twice in AD 2027, so `-2027-01` / `-2027-12`). `start_bs` / `end_bs`: `YYYY-MM-DD` zero-padded Bikram Sambat, inclusive window (same date for a single-day festival). Windows are compared as strings, so an `end_bs` in 2085 is fine even though the BS month table stops at 2084 — but note `bsToday()` is null once the year rolls to 2085, so the card cannot show during 2085-01-01→01-05 until the 2085 patro publishes.
- `greeting_en` / `greeting_ne`: warm, respectful, in both languages. `emoji`: festive only — **no religious imagery** (no 🕉️🛕🙏⛩️🪔🪷). `accent`: hex colour for the card's gradient border/glow. `confidence`: `high` = 2+ sources agree; `medium` = single reputable source (ashesh patro) — re-verify `medium` rows against the Government of Nepal holiday list / Panchanga Nirnayak Samiti patro when it publishes, especially Dashain 2084 Ghatasthapana/Phulpati and the two Lhosars. Never ship below `medium`.
- **Eid exclusion (user instruction, 2026-11-09): Eid al-Fitr and Bakr Eid (Eid al-Adha) are NOT included — do not list them, do not add them as entries, and do not "complete" the list with them.** Every other festival celebrated in Nepal is included. The exclusion is documented in the `data/festivals.json` generator header and asserted explicitly by `scripts/test-festivals.js` (any id/name/greeting mentioning Eid or Bakr fails the suite).
- National days that aren't festivals (Democracy Day, Constitution Day, etc.) are skipped. Unverifiable festivals are excluded, not carried from another year (Madhushravani was left out for exactly this reason).
- Dismissing a card stores `{festivalId: end_bs}` in `loksewa_festival_dismissed_v1` — hidden for the rest of that festival window only.

## Birthday + My Day digest

- The profile birthday lives on the existing progress object as `progress.birthday` — a BS date string `'YYYY-MM-DD'` or `''` when unset (migrated in `migrateProgress()` in `assets/js/app.js`). Same local store as name/email (`loksewa_progress_v1`); on this device only, never uploaded. Do not mint a separate profile key.
- Birthday matching is month/day only (BS), via the existing BS engine — no absolute-day maths, so birth years 2040–2083 are fine even though `BS_MONTH_LEN` only covers 2083/2084. Day validation accepts 1–32 (every BS month is 29–32 days); a day that doesn't exist in a given year simply never matches.
- Feature code lives in `assets/js/birthday.js` (pure helpers + renderers) with CSS §26; app.js hooks are `typeof`-guarded so app.js works standalone. `scripts/build-bundle.py` inlines birthday.js into the same app script block (bundle keeps exactly 2 script blocks).
- The My Day digest reads festivals from the app.js `FESTIVALS` global first, then `window.EMBEDDED_FESTIVALS`, then a direct fetch of `data/festivals.json` — and degrades to exams + birthday when the file is absent. The digest never writes festival data; `data/festivals.json` is owned by the festival-wishes feature.

## Code changes

- Vanilla HTML/CSS/JS only. No build step, no dependencies, no CDN, no tracking, no backend.
- Mobile-first, accessible (labels, focus states, contrast). Keep the app working from `file://` for the guide pages and from a static server for the question bank.
- Do not add analytics, ads, accounts, or any code that sends user data anywhere. Progress stays in `localStorage`.

## Code of Conduct

Be kind and respectful. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Harassment, spam PRs, and low-effort bulk question dumps will be closed.
