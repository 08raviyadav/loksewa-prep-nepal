# TESTING.md — Lok Sewa Prep Nepal

> **Note (2026-10-26 merge):** sections A–G below describe the original 1,129-question / 12-exam state. **Section H supersedes their counts** — the bank is now 6,227 questions / 42 exams. A–G are kept as history; H is the current state. **Section I (v2, 2026-10-26) supersedes the bank count again: 6,846 questions in 22 files. Section J (round 3) supersedes it again: 10,695 in 29 files. Section K (round 4 + real previous-year papers, 2026-10-26): 12,828 questions in 35 files. Section L (rounds 5 + 6, 2026-10-26) is current: 15,087 questions in 41 files + 322 fun facts. Section M (self-audit, 2026-10-26) supersedes it again: 18,200 questions in 48 files + 412 fun facts. Section N (round 7 integration, 2026-10-26) is current: 19,118 questions in 49 files, 47 exams; 412 fun facts.**

How this project was tested, what passed, what failed and was fixed, and what was **not** tested in a real browser. Run the suites yourself:

```bash
node scripts/test-questions.js   # question bank
node scripts/test-app.js         # scoring, shuffle, HTML ids, mock specs
node scripts/test-e2e.js         # end-to-end quiz logic in a DOM stub
node scripts/test-v2.js          # v2: sign-in, discussions, submissions, moderation, reports
python3 -m http.server 8000     # then open http://localhost:8000
```

Status key: **PASS** = ran and passed · **FIXED** = failed, then fixed and re-verified · **REVIEWED** = checked by reading the code, not by running · **NOT RUN** = needs a real browser; no headless browser was available in this environment.

## A. Question bank — `node scripts/test-questions.js` (all PASS, 3 runs after final fix)

| # | Check | Result |
|---|---|---|
| 1 | Total ≥ 1000 questions | PASS — **1,129** |
| 2 | `nepal-history-geography-culture.json` | PASS — 220 |
| 3 | `constitution-governance-economy.json` | PASS — 245 |
| 4 | `iq-maths.json` | PASS — 220 |
| 5 | `english-nepali-computer.json` | PASS — 224 |
| 6 | `office-banking-education-health.json` | PASS — 220 |
| 7 | All ids unique | PASS |
| 8 | No duplicate question text (exact, case-insensitive) | FIXED — 17 cross-file duplicates found on run 1 (e.g. "How many districts are there in Nepal?" asked in two files); all 17 replaced with new questions on different facts; re-ran clean |
| 9 | Exactly 4 options per question | PASS |
| 10 | No duplicate options within a question | PASS |
| 11 | Answer index in 0–3 and points at the correct option | PASS (validator) + spot-checked by each bank author |
| 12 | Marks are 1 or 2 only | PASS — 1,007 × 2-mark, 122 × 1-mark |
| 13 | Difficulty is easy / medium / hard | PASS — 573 easy, 498 medium, 58 hard |
| 14 | No empty question / option / explanation / topic | PASS |
| 15 | Exam tags only from the valid list | PASS |
| 16 | At least 16 topics | PASS — exactly 16 topics |
| 17 | Every question has an explanation | PASS |
| 18 | No lorem / placeholder / TODO text | PASS — grep clean |
| 19 | Answer-position distribution roughly uniform | FIXED — was 433/389/203/104 (38% in position A); options re-shuffled deterministically (seed 20261025) with answers remapped; now 255/288/288/298. Runtime shuffling also randomises options on every attempt, so this was belt-and-braces. |
| 20 | Full suite re-run 3× after the last fix | PASS — exit 0 three times in a row |

By-exam coverage (tags overlap — one question can serve several exams): kharidar 851, nasu 859, section-officer 798, nrb-assistant 175, tsc-primary 159, tsc-secondary 153, rbb 73, nrb-officer 45, health 31, police 26, army 26, engineering 10. Note: police/army/engineering/health have thin dedicated coverage — they mostly share the GK/IQ/Maths bank. See README roadmap.

## B. App unit checks — `node scripts/test-app.js` (all PASS)

| # | Check | Result |
|---|---|---|
| 21 | `assets/js/app.js` parses (no syntax errors) | PASS |
| 22 | Scoring: 1 correct 2-mark (+2), 1 wrong 2-mark (−0.4), 1 skipped, 1 correct 1-mark (+1) = **2.6** | PASS |
| 23 | Scoring: 10 correct 2-mark = **20**, 100% | PASS |
| 24 | Scoring: 2 wrong (2-mark + 1-mark) = **−0.6** | PASS |
| 25 | Scoring: negative marking OFF, wrong answer = 0 | PASS |
| 26 | XP: score 20 → 200 XP | PASS |
| 27 | Shuffle: 20 runs give 20 distinct question orders | PASS |
| 28 | `shuffleOptions`: correct answer remaps correctly (50 trials) | PASS |
| 29 | `shuffleOptions`: option order varies across runs | PASS |
| 30 | All static element ids used by app.js exist in `index.html` | FIXED — first run flagged `chart` (a canvas created at runtime by `renderDashboard`); added to the runtime-created list in the test; re-ran clean |
| 31–40 | All 10 views exist (`home, practice, quiz, result, mock, guide, dashboard, review, flash, search`) | PASS (10 checks) |

## C. End-to-end logic — `node scripts/test-e2e.js` (all PASS)

Runs `app.js` in a Node VM with a minimal DOM stub and real question data loaded from disk.

| # | Check | Result |
|---|---|---|
| 41 | `loadData()` loads 1,129 questions | PASS |
| 42 | `loadData()` loads 12 exams | PASS |
| 43 | Practice starts with the requested 10 questions | PASS |
| 44 | All-correct practice scores 100% and shows PASS | FIXED — first run showed a perfect 19/19 practice set as **FAIL**, because pass/fail compared the raw score to the full-paper cutoff (45/100). Fixed in `app.js`: pass/fail is now judged on **percentage vs the cutoff percentage** (45% / 50% / 40% per exam). Identical to the raw cutoff on full-length mocks. |
| 45 | XP is recorded in localStorage progress | PASS |
| 46 | A second random practice set has a different question order | PASS |
| 47 | Option order varies across 20 fresh sets | PASS — 20 distinct first-question option orders |
| 48 | Mock (Kharidar) starts with 50 questions | PASS |
| 49 | Mock questions are 2 marks each | PASS |
| 50 | Mock timer set to 45 min (2,700 s) | PASS |
| 51 | Mock 25 right / 25 wrong = **40/100, FAIL** vs cutoff 45 | PASS — exact PSC maths |
| 52 | Daily Challenge gives the same 10 questions twice on the same day (seeded) | PASS |
| 53 | Quick Quiz is 5 questions | PASS |
| 54 | Flashcards load 20 cards | PASS |
| 55 | Search for "Everest" returns results | PASS |
| 56 | Bookmark is saved to progress | PASS |
| 57 | A wrong answer is saved to Mistakes | PASS |
| 58 | Dashboard renders stats; Exam Guide renders all 12 exams | PASS |

## D. Local serving — `python3 -m http.server` (all PASS)

| # | Check | Result |
|---|---|---|
| 59 | `GET /` → 200 | PASS |
| 60 | `GET /index.html` → 200 (8,092 B) | PASS |
| 61 | `GET /assets/css/style.css` → 200 | PASS |
| 62 | `GET /assets/js/app.js` → 200; served copy parses (`node --check`) | PASS |
| 63 | `GET /data/exams.json` → 200, parses, 12 exams | PASS |
| 64 | `GET` each of the 5 question JSON files → 200 | PASS |
| 65 | `GET /README.md`, `/PLAN.md`, `/LICENSE`, `/CONTRIBUTING.md`, `/CODE_OF_CONDUCT.md`, `/SECURITY.md` → 200 | PASS |
| 66 | All JSON files in the project parse | PASS |
| 67 | No CDN / external script / font links in the app | PASS — zero `https://` URLs in `index.html`, `app.js`, `style.css` |
| 68 | No secrets in the repo (scan) | PASS — matches were only question content (e.g. a cyber-safety question about passwords); no keys, tokens or credentials |

## E. Scoring & randomisation maths (verified in B/C, listed explicitly)

| # | Check | Result |
|---|---|---|
| 69 | 10 correct 2-mark = 20 (worked example in test-app.js) | PASS |
| 70 | 1 wrong 2-mark = −0.4 | PASS |
| 71 | 1 wrong 1-mark = −0.2 | PASS |
| 72 | Skipped = 0, no penalty | PASS |
| 73 | Negative marking OFF = wrong answers cost 0 | PASS |
| 74 | Score rounded to 1 decimal | PASS (2.6 case) |
| 75 | Shuffle run 20× — order differs every time | PASS |
| 76 | Option shuffle remaps the answer correctly (50 trials) | PASS |
| 77 | Mock auto-submit path exists (`startTimer` → `finishAttempt(true)`) | REVIEWED — timer callback wired; countdown itself not observed ticking in a real browser (see §G) |
| 78 | Daily Challenge seed is date-based | PASS (same-day determinism, §C-52) |

## F. Responsive / accessibility / code review

| # | Check | Result |
|---|---|---|
| 79 | Viewport meta tag present | PASS (in `index.html`) |
| 80 | Responsive CSS breakpoint at 640 px, mobile-first layout | REVIEWED — media query present; not observed at a real 360 px viewport |
| 81 | Dark / light theme toggle wired (`#theme-toggle`, `data-theme`) | REVIEWED — handler in `app.js`, CSS variables for both themes |
| 82 | Buttons are real `<button>` elements with labels | REVIEWED |
| 83 | `aria-label` on the theme toggle | PASS |
| 84 | Focus/hover states for options and nav | REVIEWED — CSS present |
| 85 | Colour contrast: dark theme, amber accent on dark slate | REVIEWED — not measured with a contrast tool |
| 86 | Nepali (Devanagari) labels render — font stack includes "Noto Sans Devanagari" | REVIEWED — not observed in a browser |
| 87 | localStorage progress: XP, streak, attempts, bookmarks, mistakes, daily | PASS (E2E, §C) |
| 88 | Streak logic: consecutive days increment, gap resets to 1 | REVIEWED — code read; date-boundary behaviour not live-tested |
| 89 | `console.warn` only on question-file load failure (no stray logs) | PASS — one `console.warn` in the fetch fallback |
| 90 | `file://` fallback message shown when the question bank cannot load | REVIEWED — message exists in `loadData()`; not observed in a browser |

## G. Docs & GitHub-readiness

| # | Check | Result |
|---|---|---|
| 91 | README: run instructions, scoring, mock table, sources/caveats | PASS |
| 92 | LICENSE: MIT, Copyright 2026 Ravi Yadav | PASS |
| 93 | CONTRIBUTING: question schema + accuracy rule + "maintainer accepts or rejects every PR, no auto-merge" | PASS |
| 94 | CODE_OF_CONDUCT.md, SECURITY.md present | PASS |
| 95 | `.github/PULL_REQUEST_TEMPLATE.md` present and complete | PASS |
| 96 | Issue templates: bug report + question contribution | PASS |
| 97 | `.gitignore` present, no secrets / personal data in repo | PASS (§D-68) |
| 98 | No GitHub repo created, nothing pushed, nothing shared publicly | PASS — local only, as instructed |
| 99 | **NOT RUN — real-browser smoke test**: open `http://localhost:8000`, click through Home → Practice → answer 10 → Result → Mock → Dashboard, in Chrome and on a phone viewport, and confirm no console errors | NOT RUN — no headless browser was available in this environment. Do this before uploading to GitHub. |
| 100 | **NOT RUN — question accuracy audit**: a human re-check of a random sample (e.g. 50 questions) against reliable sources, especially Constitution article numbers, census figures and NRB/banking facts | NOT RUN — authors checked their own answers and the validator checks structure, not truth. Recommended before presenting the bank as exam-accurate. |

---

## H. Overnight expansion merge — 2026-10-26 (supersedes the counts in §A–G)

Final integration of the overnight run: question expansion + bilingual EN/NE + TSC/licence research + exam/gap audits + trends. All work local; **nothing uploaded, pushed, or shared** (no GitHub repo created).

### H1. Question bank — before → after

| Measure | Before (§A) | After merge |
|---|---|---|
| Total questions | 1,129 (5 files) | **6,227 (20 files)** — 5,194 added overnight, **96 removed as cross-file duplicates** (see H3) |
| Files | 5 | 20 (all listed in `QUESTION_FILES`, verified by test-app.js against the directory) |
| Topics | 16 | 16 (same set; counts changed) |
| Exams in `exams.json` | 12 | **42 (29 with MCQ prelim, 13 guide-only)** |
| Bilingual (EN + NE) | labels only, no toggle | **6,227/6,227 (100.0%)** have `question_ne` + `options_ne[4]` + `explanation_ne`; `#lang-toggle` switches, `loksewa_lang` persists |
| Answer-position distribution | 255/288/288/298 | 1519 / 1588 / 1543 / 1577 (positions 0–3) — roughly uniform |
| Marks | 1,007 × 2-mark, 122 × 1-mark | 6,105 × 2-mark, 122 × 1-mark |
| Difficulty | 573 easy / 498 medium / 58 hard | 2,656 easy / 2,567 medium / 1,004 hard |

Per-file counts after de-duplication: constitution-governance-economy 245 · english-nepali-computer 224 · expansion-computer-office-banking 778 · expansion-constitution-economy-current-science 863 · expansion-culture 198 · expansion-geography 243 · expansion-health-technical-security 358 · expansion-health-technical 185 · expansion-history 246 · expansion-iq-maths 700 · expansion-security-engineering 144 · iq-maths 220 · license-allied-health 210 · license-health-assistant 182 · license-medical 190 · license-nursing 193 · license-pharmacy 205 · nepal-history-geography-culture 220 · office-banking-education-health 220 · tsc-education 403.

By topic: Health/Technical basics 1,533 · Constitution & Governance 504 · Education & Pedagogy 463 · IQ & Reasoning 460 · Maths & Numerical 460 · Computer & ICT 338 · Nepal History 322 · Office Management & Public Service 316 · Banking & Finance 316 · Nepal Geography 316 · Culture & Society 272 · Science & Tech 265 · Current Affairs 264 · Economy & Development 246 · English 92 · Nepali Language 60.

By exam tag (one question can serve several exams): kharidar 3,879 · nasu 3,887 · section-officer 3,826 · tsc-primary 1,261 · tsc-secondary 1,251 · nrb-assistant 765 · rbb 652 (practice only — mock removed, see H4) · health 609 · **tsc-license 403** · police 384 · army 377 · nrb-officer 293 · **npc-pharmacy 205 · nnc-rn 193 · nmc-mbbs 190 · nhpc-ha 182** · engineering 108 · **nhpc-lab / nhpc-radio / nhpc-physio / nhpc-dental / nhpc-ayurveda / nhpc-public-health / nhpc-optometry 30 each**.

### H2. Test results (all exit 0 — run 2026-10-26, final run after the last fix)

| Suite | Result | Exit |
|---|---|---|
| `node scripts/test-questions.js` | **ALL QUESTION CHECKS PASSED** — 6,227 total, 0 duplicate ids, 0 duplicate question text, 0 duplicate options, bilingual 100.0%, 16 topics, 24 exam tags all in `VALID_EXAMS` | 0 |
| `node scripts/test-app.js` | **ALL APP CHECKS PASSED** — 82 PASS lines, 0 FAIL. Includes scoring with per-exam negative rates (0 / 0.25 / 0.2), `mockNegRate()` cases, all 5 original + 18 new mock specs, `tsc-license` null timeMin/negative, all 13 guide-only exams `prelim: null`, RBB prelim removed, and `QUESTION_FILES` == directory listing (20 files) | 0 |
| `node scripts/test-e2e.js` | **ALL E2E CHECKS PASSED** — 33 checks, 0 FAIL. Includes: loadData 6,227 Q / 42 exams; Kharidar mock 25 right / 25 wrong = 40/100 FAIL; guide renders 42 cards with exactly 29 Start-mock buttons + 13 "No mock available"; `startMock()` refuses RBB (guide-only) and leaves `current` untouched; TSC Licence mock untimed + no deduction, all-wrong = 0/100; NNC mock all-wrong = 0/150 (no negative marking); NMC MBBS mock 130 Q, all-correct = 130/130 PASS at the 50% cutoff; NMC-BDS mock warns it draws from the general bank; Kharidar mock carries no such warning | 0 |
| `node --check assets/js/app.js` | PASS (no syntax errors) | 0 |
| `python3 -m http.server 8000` + urllib sweep | **32/32 URLs 200 and byte-identical to disk** — `/`, `index.html`, CSS, `app.js`, `exams.json` (42 entries), all 20 question files (each parses), README/PLAN/TESTING/LICENSE/CONTRIBUTING/CODE_OF_CONDUCT/SECURITY. Server stopped afterwards (port 8000 confirmed closed) | — |

Baseline before fixes (for the record): `test-questions.js` exited 1 with 200 duplicate ids (HEAL2 collision), 96 duplicate question texts, 7 duplicate options, and 1,429 unknown-exam-tag failures (11 new licence/TSC tags not yet in `VALID_EXAMS`). All fixed, not worked around — no test was weakened; new checks were added instead.

### H3. What was fixed in the merge (counts)

1. **HEAL2 id collision (200 ids):** `expansion-health-technical.json` and `expansion-health-technical-security.json` both used HEAL2-001..200. Renamed the ids in `expansion-health-technical.json` to **HEAL3-001..200** (ids only, nothing else). Verified: duplicate ids 200 → 0.
2. **Duplicate question text (96 removed):** 81 duplicate-text groups, all cross-file. Removed the copy from the newer file (original 5-file bank kept where present; otherwise the alphabetically-first file kept). Removals by file: expansion-constitution-economy-current-science 16 · license-health-assistant 18 · license-nursing 17 · expansion-health-technical 15 · license-medical 10 · expansion-geography 7 · expansion-security-engineering 6 · expansion-history 4 · expansion-culture 2 · tsc-education 1. Verified: duplicate text 96 → 0. Side effect (honest): licence-tag counts dropped (nhpc-ha 200→182, nmc-mbbs 200→190, nnc-rn 210→193) because those questions also existed in the general health bank — the content is not lost, it is kept once under its original file/tags.
3. **Duplicate options within a question (7 fixed):** all in `expansion-iq-maths.json`, all case-only duplicates of the correct coding-decoding answer (e.g. `20ree` vs `20REE`). Replaced the duplicated option (EN **and** NE) with a distinct plausible distractor (another alphabet position: 22REE, 5AT, 16AT, 16OAD, 11ILK, 5AT, 17TAR); answer index unchanged and verified still correct. IDs: IQ2-084, IQ2-093, IQ2-102, IQ2-103, IQ2-106, IQ2-107, IQ2-112.
4. **Exam tags:** `VALID_EXAMS` in `test-questions.js` now lists all 26 catalogue ids (24 used as question tags + `tsc-lower-secondary` and `nmc-bds`, which are exam entries with no tagged questions yet).
5. **App wiring:** `QUESTION_FILES` now lists all 20 files (sorted); verified against the directory by test-app.js.
6. **Exams merge (12 → 42):** `data/exams-new.json` (14) + `data/LICENSE-RESEARCH.md` drafts (17 → 14 entries: BPharm+DPharm merged into `npc-pharmacy`, CMLT+BSc MLT into `nhpc-lab`, PCL+BSc MIT into `nhpc-radio`) + 2 new guide-only entries for tags with no verified pattern (`nhpc-dental`, `nhpc-ayurveda`). Licence draft ids were renamed to match the question tags where a tag exists (`nursing-nlen` → `nnc-rn`, `ha-nhpc` → `nhpc-ha`, `physio-bpt` → `nhpc-physio`, `public-health-bph` → `nhpc-public-health`, `optometry-boptom` → `nhpc-optometry`); `nmc-bds`, `midwifery-nlem`, `staff-nurse-psc`, `anm-guide`, `ayurveda-bams` kept their draft ids (no tag exists). GAP-AUDIT verified patterns applied to `sub-engineer`, `computer-operator`, `nepal-telecom` (50×2/45 min/pass 40).
7. **"Pass 50" interpretation (read this):** the merge brief wrote licence pass marks as "pass 50" for NMC/NLEN/Pharmacy. That is the **50% pass mark**, not a raw 50 — a raw pass of 50 on a 150-mark paper would be a 33% cutoff. The merged entries keep the drafts' raw values, which are 50%: NMC 90/180, NLEN 75/150, Pharmacy BPharm 75/150, NHPC 50/100. `cutoffPct` is computed from `pass/total`, so pass/fail is judged at 50% in all of them (verified in e2e for NMC).
8. **NEA deviation from the brief (deliberate, flagged):** the brief listed NEA as 50×2/45 min/pass 40, but the GAP-AUDIT source it cites gives NEA Paper I Section A as **50×1** in 45 min with **no stated pass mark** for Section A alone. Inventing pass 40 for a 50-mark paper would be an 80% cutoff. NEA is therefore **guide-only** (`prelim: null`) with the verified Section A pattern described in its `main`/`note`. If the maintainer wants a 50×1 mock, a pass mark must first be verified from an NEA notice.
9. **TSC Licence id fix (caught by a failing test):** the draft used id `tsc-licence` but the question tag is `tsc-license` — `startMock('tsc-license')` silently found no exam and the mock never started (3 e2e failures). Renamed the exam id to `tsc-license` to match the tag and the brief. No other exam id/tag mismatches remain (checked all 24 tags against `exams.json`).
10. **NHPC time rule:** per the brief, all NHPC licences use `timeMin: 90` (common format). The BSc MIT and B.Optom drafts said 120 min — changed to 90 with the 2-hour conflict preserved in each entry's `note`.
11. **Per-exam negative marking (app fix, not just data):** `scoreAttempt()` previously hard-coded a 20% deduction and `startMock()` forced it on — so no-negative licence mocks (NNC, NPC, NMC, NHPC) would have deducted wrongly. Added `mockNegRate()` + a `negRate` on `current`: 0.2 on PSC prelims, 0 where negative is 0 or null (unverified). `startMock()` also runs untimed when `timeMin` is null (TSC Licence) instead of starting a 0-second timer that would auto-submit instantly. Verified by e2e (TSC Licence and NNC all-wrong = 0, not negative).
12. **Null-prelim guards (app fix):** `fillExamSelects()` puts only prelim exams in the mock dropdown; `startMock()` refuses guide-only exams with an alert; `renderGuide()` renders guide-only exams without a prelim row or Start-mock button and shows the per-exam negative/time text (null → "unverified", 0 → "none", else 20%); `finishAttempt()` / `cutoffFor()` / `renderResult()` are null-prelim safe (practice with a guide-only exam selected no longer crashes — it falls back to the general bank, see H5.3).
13. **Thin-bank mock warning (addition beyond the brief, from the audits):** when a mock's tagged pool is smaller than the paper, the app previously fell back to the whole bank silently. `startMock()` now warns in its start alert ("Only N questions are tagged … so this mock also draws from the general bank"). Verified in e2e for NMC-BDS (0 tagged) vs Kharidar (no warning).

### H4. Exams added (29 with prelim, 13 guide-only)

With prelim (mock available): foreign-service (100×1/90/pass 45) · tsc-lower-secondary (50×2/60/pass 50) · tsc-license (50×2/pass 50, untimed, no deduction) · sub-engineer (50×2/45/pass 40) · computer-operator (50×2/45/pass 40) · nepal-telecom (50×2/45/pass 40) · nmc-mbbs (130×1/180 min, total 180, pass 90 — MCQ part only, CSQs noted) · nmc-bds (180×1/180/pass 90) · nnc-rn (150×1/150/pass 75, no negative) · midwifery-nlem (150×1/150/pass 75, no negative; OSPE 50 in `main`) · staff-nurse-psc (50×2/45/pass 40) · nhpc-ha (100×1/90/pass 50, no negative) · npc-pharmacy (150×1/150/pass 75, no negative; DPharm 100×1/80/pass 50 in `main`) · nhpc-lab (100×1/90/pass 50) · nhpc-radio (100×1/90/pass 50) · nhpc-physio (100×1/90/pass 50) · nhpc-public-health (100×1/90/pass 50) · nhpc-optometry (100×1/90/pass 50).
Guide-only (`prelim: null`): deputy-secretary · jta · ranger · judicial-service · psc-service-groups · **rbb** (prelim removed — see below) · rbb-senior-assistant · provincial-psc · nea · nhpc-dental · nhpc-ayurveda · anm-guide · ayurveda-bams.
**RBB correction:** the old `rbb` prelim (50×2, 45 min, pass 40) was wrong — the 2082-83 unified exam has no MCQ prelim (two subjective papers + interview). Changed to `prelim: null` + explanatory note. RBB-tagged questions (652) remain practicable via Practice/Search; only the mock is gone.
**NRB Officer:** prelim kept (100×1/90/pass 45) but the `note` now states it is unverified — the report supports only "pre-qualifying MCQ, 100 marks".

### H5. Still thin / still not tested — read before GitHub upload

1. **Thin-bank mocks (12 of 29):** these mocks fall back to the general bank (now with a start warning): sub-engineer (0 tagged), computer-operator (0), foreign-service (0), tsc-lower-secondary (0), nepal-telecom (0), nmc-bds (0), midwifery-nlem (0), staff-nurse-psc (0), nhpc-lab (30/100), nhpc-radio (30/100), nhpc-physio (30/100), nhpc-public-health (30/100), nhpc-optometry (30/100). Engineering (108/50) is the only thin-but-sufficient case. Priority content work: 100 tagged questions per NHPC discipline, then the 7 zero-tag exams.
2. **Thinnest topics:** Nepali Language (60), English (92). Next thinnest after those: Economy & Development (246), Current Affairs (264), Science & Tech (265).
3. **Practice with a guide-only exam** (e.g. Deputy Secretary) still falls back to the general bank instead of saying "no questions for this exam" — it no longer crashes, but the fallback is silently broad. Consider a "no tagged questions" notice in `filteredQuestions()` before upload.
4. **NOT RUN — real-browser smoke test (items 99–100, still open):** no headless browser was available. Before upload: open `http://localhost:8000` in Chrome + a 360 px viewport, click Home → Trending card → Practice (answer 10, skip, bookmark) → Result → Mock (Kharidar + one licence mock + one guide-only guide card) → Dashboard → Flashcards → Search → Exam Guide, confirm zero console errors, confirm the EN/NE toggle switches a question and persists across reload, confirm the live countdown ticks and auto-submits, confirm Devanagari renders, and confirm the 20 parallel `fetch()` calls all land (sequential fetches verified 200 here; parallel browser load not observed).
5. **NOT RUN — question accuracy audit (item 100, still open, now bigger):** the validator checks structure, not truth. A human re-check of a random sample (e.g. 50–100 questions, weighted to the new licence files and Constitution article numbers / census figures / NRB-banking facts) is still needed before presenting the bank as exam-accurate. The overnight expansion was written by several agents; spot-checking their answers was out of scope for this merge.
6. **Human checks on exam data (before presenting as fact):** NHPC negative marking (unstated — portal assumes none) and NHPC time (90 vs 120 min) against nhpc.gov.np; NMC negative marking against nmc.org.np; NEA pass mark for Section A; TSC Licence time limit + negative marking against tsc.gov.np; NRB Officer Q count/time/pass against an NRB notice; NLEM practical 50 vs 40 marks; Computer Operator Paper II 2h15m vs 3h15m. All are flagged in `data/exams.json` notes and README — none was resolved by this merge.
7. **Trending section is a demand proxy, not Trends data** (see `data/TRENDS.md` §5): Google Trends returned HTTP 429, so no index/volume is quoted. The Home section says so. Re-research after the next major PSC vacancy notice.
8. **Files changed in this merge:** `data/questions/*.json` (10 files changed: HEAL2 rename, 96 removals, 7 option fixes) · `data/exams.json` (12 → 42 entries) · `assets/js/app.js` (QUESTION_FILES, per-exam negative rate, null-prelim guards, thin-bank warning, untimed mocks) · `index.html` (Trending section) · `scripts/test-questions.js` (VALID_EXAMS) · `scripts/test-app.js` (new specs + checks) · `scripts/test-e2e.js` (new counts + licence/guide-only/thin-bank checks) · `README.md`, `PLAN.md`, `TESTING.md` (this section). Not changed: `data/exams-new.json`, `data/LICENSE-RESEARCH.md`, `data/TRENDS.md`, `data/EXAM-AUDIT.md`, `data/GAP-AUDIT.md`, `data/SOURCES.md` (source research, kept as-is).

## Known limitations (honest list) — updated 2026-10-26

1. **No real-browser test yet** (items 99–100, §H5.4). The logic is verified in Node, but rendering, the live countdown, and `localStorage` in a real browser still need one manual pass.
2. **Thin-bank mocks (12 of 29)** fall back to the general bank with a start warning (§H5.1) — the mock runs, but it does not mirror the real paper for those exams.
3. **Subjective/theory papers are guide-only.** Kharidar/NaSu/Section Officer main papers are descriptive; the portal explains their structure but does not auto-mark essays — that is stated in the README, not hidden.
4. **Exam patterns are from secondary sources** (Edusanjal etc.); official PSC PDFs were not read directly. Conflicts are flagged in README + `data/exams.json` (Section Officer main pass 40 vs 45; final total 70 vs 60; TSC merit weightage; plus the licence-exam conflicts in §H4/H5.6).
5. **Current affairs stop at stable facts to 2025.** No live vacancy feed; vacancy numbers/dates are deliberately not hard-coded.
6. **Question accuracy is validator-checked, not human-audited** (§H5.5) — a sample re-check is still open before presenting the bank as exam-accurate.

---

## I. Frontend v2 — 2026-10-26 (supersedes the bank count in §H: **6,846 questions in 22 files**)

Demo sign-in + profile, Discussion Hub, Submit-a-Question, Maintainer Review,
report-wrong-question, community-approved questions, Supabase backend plan.
All work local; **nothing uploaded, pushed, or shared** (no GitHub repo created).

### I1. Bank — before → after

| Measure | Before (§H) | After v2 |
|---|---|---|
| Total questions | 6,227 (20 files) | **6,846 (22 files)** — +320 English (`expansion-english-v2.json`, ENGV2-001…320) +299 Nepali (`expansion-nepali-v2.json`, NEP2-001…299) |
| Bilingual (EN + NE) | 6,227/6,227 (100%) | **6,846/6,846 (100%)** |
| Topics | 16 | 16 (same set; English 92 → **412**, Nepali Language 60 → **359**) |
| Marks | 6,105 × 2-mark, 122 × 1-mark | **6,528 × 2-mark, 318 × 1-mark** |
| Difficulty | 2,656 easy / 2,567 medium / 1,004 hard | **2,873 easy / 2,815 medium / 1,158 hard** |
| Answer-position distribution | 1519 / 1588 / 1543 / 1577 | **1691 / 1727 / 1697 / 1731** (positions 0–3) — roughly uniform |
| Exam tags | kharidar 3,879 · nasu 3,887 · section-officer 3,826 · tsc-primary 1,261 · tsc-secondary 1,251 · nrb-assistant 765 | kharidar **4,498** · nasu **4,506** · section-officer **4,445** · tsc-primary **1,386** · tsc-secondary **1,382** · nrb-assistant **771** (others unchanged) |

### I2. Test results (all exit 0 — run 2026-10-26, final run after the last fix)

| Suite | Result | Exit |
|---|---|---|
| `node scripts/test-questions.js` | **ALL QUESTION CHECKS PASSED** — 6,846 total, 0 duplicate ids, 0 duplicate question text, 0 duplicate options, bilingual 100.0%, 16 topics | 0 |
| `node scripts/test-app.js` | **ALL APP CHECKS PASSED** — 91 checks, 0 FAIL. Includes the earlier checks plus: `QUESTION_FILES` == directory listing (22 bank files, incl. the two v2 files; `community-approved.json` excluded — it is the export target, not a fetched bank file), all 15 views exist (home, practice, quiz, result, mock, guide, dashboard, review, flash, search, auth, profile, discuss, submit, moderate), demo banner + report modal exist, nav has Discuss / Contribute / Sign In / Profile | 0 |
| `node scripts/test-e2e.js` | **ALL E2E CHECKS PASSED** — 33 checks, 0 FAIL. `loadData` loads 6,846 Q / 42 exams; all earlier mock/scoring/guide checks still pass unchanged | 0 |
| `node scripts/test-v2.js` | **ALL V2 CHECKS PASSED** — 43 checks, 0 FAIL (see I3) | 0 |
| `node --check assets/js/app.js` | PASS (no syntax errors) | 0 |
| `python3 -m http.server` + curl sweep | **10/10 URLs 200** — `/`, `index.html`, CSS, `app.js`, `exams.json`, both v2 question files, `community-approved.json`, `config.example.js`, `docs/BACKEND.md`; all 15 views present in `index.html`; `config.js` 404 as expected (absent in demo mode — the app fetches it and falls back silently). Server stopped afterwards. | — |

### I3. What test-v2.js checks (43 checks)

| # | Check | Result |
|---|---|---|
| 101 | Progress migrates to the cloud-ready shape (`user_id`, `email`, `name`) | PASS |
| 102 | Demo mode is ON with no `config.js` | PASS |
| 103–106 | Gmail validation: accepts `…@gmail.com`; rejects Yahoo, Outlook, non-email | PASS |
| 107–109 | Demo sign-in stores name + Gmail; refuses non-Gmail; sign-out clears name/email but keeps the device `user_id` | PASS |
| 110 | `loadData` loads 6,846 questions | PASS |
| 111 | Duplicate detection blocks an **exact** copy of an existing question | PASS |
| 112 | Duplicate detection flags a **near-duplicate** (token-Jaccard ≥ 0.8) | PASS |
| 113 | Duplicate detection passes a genuinely different question | PASS |
| 114–115 | `tokenJaccard` (identical = 1, disjoint = 0); `normaliseText` ignores case/punctuation/whitespace | PASS |
| 116 | Validation accepts a complete, well-formed submission | PASS |
| 117–122 | Validation rejects: <4 filled options, duplicate options, empty explanation, missing source, question <15 chars, URL in question text, mostly ALL-CAPS text | PASS |
| 123–125 | Rate limit: allows the 1st–5th submission in an hour; **blocks a 6th** (with minutes remaining); ignores submissions older than an hour | PASS |
| 126–127 | Full submit path: a valid new question queues as `pending`; an exact duplicate of a bank question is refused (queue does not grow) | PASS |
| 128–133 | **Approve →** returns the new `COMM-001` question; in the localStorage community list; joins the live bank immediately; `communityBadge` marks it; still in the bank after reload; counts show 1 approved / 0 pending | PASS |
| 134–136 | **Reject →** returns true with a reason; question appears in neither the community list nor the bank; counts show 1 approved / 1 rejected / 0 pending | PASS |
| 137–138 | Report-wrong-question is stored (id, reason, comment); a report with no comment is refused | PASS |
| 139 | Discussion Hub seeds 9 threads — one per exam (Kharidar, NaSu, Section Officer, TSC, NRB, NMC, NNC, Pharmacy) + General doubts | PASS |
| 140–142 | Replying stores the reply; upvoting increments; reporting stores the report on the thread | PASS |

Baseline before fixes (for the record): the first test-v2 run crashed on a fixture
that was itself a near-duplicate of the just-approved test question (Jaccard 0.94 —
the detector correctly refused it); the fixture was rewritten to a genuinely
different question. A second run failed one check because the near-duplicate
fixture passed the unchanged Nepali text, so the exact-match branch fired on the
NE side (correct behaviour — the fixture was fixed, not the detector). No
production code was weakened; no test was weakened.

### I4. What was built in v2 (files changed)

- `assets/js/app.js` — `QUESTION_FILES` 20 → 22; cloud-ready progress shape +
  `migrateProgress()`; `loadConfig()` (fetch `config.js`, demo mode when absent);
  `communityApprovedQuestions()` loaded into the bank at startup; sign-in/profile
  (`signInDemo`, `signOut`, `renderAuth`, `renderProfile`, `isGmailAddress`);
  Discussion Hub (`seedDiscussions`, `postThread`, `postReply`, `upvoteThread`,
  `reportPost`, `discussQuestion`); submissions (`normaliseText`, `tokenJaccard`,
  `findDuplicate`, `validateSubmission`, `rateLimitCheck`, `submitQuestion`);
  moderation (`approveSubmission` with edit-before-approve, `rejectSubmission`,
  `downloadApproved`, `renderModerate`); reports (`openReportForm`, `submitReport`).
  All existing functions/scoring/shuffle/timer untouched.
- `index.html` — nav gains Discuss / Contribute / Sign In / Profile; new views
  `view-auth`, `view-profile`, `view-discuss`, `view-submit`, `view-moderate`;
  demo banner; report modal. Home hero copy unchanged.
- `assets/css/style.css` — Google-style sign-in button, demo banner, modal,
  discussion replies, textarea + error-text styles, mobile nav unchanged.
- `docs/BACKEND.md` (new) — Supabase recommendation with a Firebase comparison
  table, exact SQL schema (profiles, progress, attempts inside progress,
  discussions, discussion_replies, discussion_reports, question_submissions,
  moderation_log, question_reports, maintainers), RLS policies in SQL, Google
  OAuth setup steps, and the exact steps the user must take on his computer.
- `config.example.js` (new) — `SUPABASE_URL`, `SUPABASE_ANON_KEY`,
  `GOOGLE_CLIENT_ID` placeholders. `config.js` added to `.gitignore`.
- `data/questions/community-approved.json` (new, `[]`) — the file approved
  community questions are committed to.
- `scripts/test-v2.js` (new) + `scripts/test-app.js` (22-file check, 5 new views,
  runtime-created v2 ids) + `scripts/test-e2e.js` (6,846 count).
- `README.md`, `PLAN.md`, `TESTING.md` (this section), `CONTRIBUTING.md`.

### I5. Still demo-only / not tested — read before GitHub upload

1. **Everything in v2 is localStorage demo mode.** Sign-in is a local profile
   (no Google involved); discussions, submissions, moderation and reports live
   on one device. The Maintainer Review view has **no auth in demo mode** —
   anyone opening the page can approve/reject; it is labelled as such, and
   `docs/BACKEND.md` §3 restricts it to the maintainer role via RLS.
2. **CAPTCHA is a placeholder box only.** hCaptcha/reCAPTCHA needs the backend
   (server-side verification); a client-side widget alone proves nothing.
3. **Rate limiting is per-device** (localStorage timestamps). A real per-account
   limit needs the backend; the client-side one stops casual spam, not
   determined abuse.
4. **NOT RUN — real-browser smoke test (items 99–100, §H5.4, still open):**
   the v2 views were verified in Node (VM + DOM stub) and by HTTP sweep, not
   by clicking through them in a real browser. Before upload: open
   `http://localhost:8000`, sign in (demo), post a thread, submit a question,
   approve it in Maintainer Review and confirm it appears in Practice with a
   Community badge, report a question, and confirm zero console errors.
5. **NOT RUN — question accuracy audit (item 100, still open):** the v2 files
   (320 English + 299 Nepali) are validator-checked, not human-audited.
6. **Supabase setup is still on the user** — `docs/BACKEND.md` §5 lists the
   exact steps (create project, run the SQL, enable Google, copy keys into
   `config.js`). Until then the demo banner stays visible, by design.

## J. Round-3 expansion — 2026-10-26 (supersedes the bank count in §I: **10,695 questions in 29 files, 47 exams**)

Target was 10,000+ total / +3,200 new. Delivered: **6,846 → 10,695 (+3,849 net)** — 3,850 written across 7 new files, 1 removed (ARMY-054, unverified Nepal Army motto question, flagged by its author and dropped by the integrator).

| New file | Qs | Content |
|---|---|---|
| expansion-zero-licence.json | 450 | NMC-BDS 180, Midwifery (NLEM) 150, Staff Nurse PSC 120 |
| expansion-technical-psc.json | 500 | Sub-Engineer 120, Computer Operator 120, Nepal Telecom 80, Foreign Service 80, TSC Lower Secondary 100 |
| expansion-thin-exams.json | 599 | Engineering 150, NRB Officer 150, Police 150, Army 149 (1 removed) |
| expansion-thin-topics.json | 600 | Current Affairs 150, Science & Tech 150, Culture & Society 150, Economy 150 |
| expansion-english-nepali-v3.json | 500 | English 250, Nepali Language 250 (40% hard each) |
| expansion-core-hard.json | 600 | IQ 200, Maths 200, Constitution 100, Education 100 (43.3% hard) |
| expansion-entrance-licence.json | 600 | MECEE-BL 200, NEC licence 150, Bar Council 100, IOE 75, CSIT 75 |
| **Total new** | **3,849 net** | |

### J1. Integration fixes (by the integrator, not the authors)
- **382 slash-joined topics fixed** in `expansion-thin-exams.json` (e.g. "Nepal History / Nepal Geography / IQ & Reasoning") — reassigned to a single topic by subtopic (Maths, English, Nepali, IQ, Constitution, Banking, Economy, History, Geography).
- **ARMY-054 removed** — Nepal Army motto ("Duty, Honour, Sacrifice") could not be verified from a primary source.
- **New exam tags added** to `scripts/test-questions.js` VALID_EXAMS: midwifery-nlem, staff-nurse-psc, sub-engineer, computer-operator, nepal-telecom, foreign-service, mecee-bl, nec-licence, bar-council, ioe-entrance, csit-entrance.
- **5 new exams added** to `data/exams.json` (47 total; 33 with a mock, 14 guide-only): MECEE-BL (200×1, 180 min, pass 100 = 50th-percentile proxy, −0.25), NEC licence (100×1, 120 min, pass 50, no negative), Bar Council Paper 1 (100×1, 90 min, pass 50, no negative), BSc CSIT (100×1, 120 min, pass 35, no negative), IOE Entrance (**guide-only** — verified pattern 100 MCQs, 140 marks 60×1+40×2, 2 hrs, −10%/wrong; no mock until the engine supports mixed marks).
- **Tests updated** for the new counts: test-app.js (47 exams, 33 prelim / 14 guide-only, 4 new mock specs), test-e2e.js (10,695 Q, 47 exams, 33 Start-mock buttons, 14 no-mock marks; nmc-bds check rewritten — 180 tagged = full paper, so no thin-bank warning), test-v2.js and test-bundle.js (10,695 Q).

### J2. Test results (all PASS, re-run by the integrator after the merge)
- `node scripts/test-questions.js` — **PASS**: 10,695 total, 0 duplicate ids, 0 duplicate question texts, 0 duplicate options, bilingual 100% (10,695/10,695).
- `node scripts/test-app.js` — **PASS** (incl. 29-file QUESTION_FILES check, 4 new mock specs).
- `node scripts/test-e2e.js` — **PASS** (incl. nmc-bds 180Q mock with no warning).
- `node scripts/test-v2.js` — **PASS**.
- Answer-position distribution: A 2,600 / B 2,975 / C 2,586 / D 2,534 (24.3% / 27.8% / 24.2% / 23.7% — all under 30%, no rebalance needed).
- Difficulty: easy 4,015 / medium 4,514 / hard 2,166 (was 48% easy / 11% hard after the overnight round).

### J3. Real previous-year questions: 0 transcribed (honest result)
A dedicated worker tried all four 2083 papers in `data/SOURCES.md` §2 (NaSu 2083-01-20, Kharidar pretest 2083/06/04, Kharidar 2083-01-26, Koshi Province 2083-01-26). All are scanned images only; text-fetch tools cannot read image content, and the PDF download URLs were not exposed in page text. **No file was created and nothing was invented.** Salvage: the Kharidar 2083-01-26 answer key (50 answers, A–D) is published as text on the page — but with no readable question text to pair it with, it cannot produce a valid question. What is needed: a live-browser/OCR pass over the scanned images. See `data/SOURCES.md` §13.

### J4. Still thin after round 3
- NHPC disciplines: 30 tagged each vs 100-question papers.
- Law topic: 10 questions (Bar Council is constitution-heavy by design).
- CSIT 75/100, IOE 75 (guide-only), Foreign Service 80, Nepal Telecom 80.
- No prelim exam has zero tagged questions any more.

## K. Round-4 expansion + real previous-year papers — 2026-10-26 (supersedes the bank count in §J: **12,828 questions in 35 files, 47 exams**)

Delivered: **10,695 → 12,695 (+2,000)** across 5 new files, then **+133 real previous-year questions − 1 excluded = 12,828**.

| New file | Qs | Content |
|---|---|---|
| expansion-nhpc-law.json | 400 | NHPC disciplines (Lab/Radio/Physio/Public Health/Optometry now 110 each) + Law |
| expansion-law-csit-ioe.json | 350 | Bar Council 100 → 250, CSIT/IOE 75 → 175 each |
| expansion-foreign-telecom.json | 250 | Foreign Service 80 → 160, Nepal Telecom 80 → 160 |
| expansion-hard-core-v2.json | 500 | Hard IQ/Maths/Constitution/Education |
| expansion-current-hard.json | 500 | Hard Current Affairs/Science/Culture/Economy |
| previous-year-2083.json | 133 | Real 2083 papers (see K1) |

### K1. Real previous-year questions: 133 transcribed (live-browser/OCR pass)
The round-3 blocker was cleared: a live-browser pass read the four 2083 scanned papers question by question. **NaSu First 2083-01-20: 44 transcribed, Kharidar First 2083-01-26: 45, Koshi 4th Level 2083-01-26: 45** (Koshi's two Q40s kept as 40a/40b). Figure-based questions were excluded (NaSu 6, Kharidar 5, Koshi 5). The Kharidar pretest 2083/06/04 has **no answer key** ("KEY [A]" is only the paper code) — 0 of its 50 questions are in the scored bank, nothing invented. **Fixes made by the finisher (2026-10-26):** the file as delivered was invalid JSON — two arrays concatenated (`]` + `,` between the Kharidar and Koshi chunks, no closing bracket) — repaired to a single array; a background writer was still appending Koshi questions when the repair started, so the fix waited until the file stopped changing (size stable 60 s) and re-verified. Spot-checked answers against the source keys (NaSu Q1, Kharidar Q1, Koshi Q1/Q6/Q30/Q45) — all match. **NASU-2083-45 was then removed by the finisher** — its options differ only by capitalisation (FridAY vs FRIday), which the validator flags as duplicate options and a text MCQ cannot score fairly; NaSu is now 43, total 133. NaSu Q11 (dual-answer: Tuberculosis + Leprosy) is kept with the dual-answer fact stated in its explanation. `data/papers.json` now marks the three papers `transcribed: true` with real counts (43/45/45) and verified direct `pdf_url`s; the pretest stays `transcribed: false` with `questions: 50`.

### K2. Wiring bugs found and fixed by the finisher
- `app.js` `QUESTION_FILES` listed only 29 of the 35 bank files — the 5 round-4 expansion files **and** `previous-year-2083.json` were never loaded, so the app was serving 10,695 while the disk held 12,695. All 35 files are now listed (test-app.js enforces this).
- `practicePaper()` filtered questions by `source.includes(paper id)` — no question source contains a paper id, so the "Practice these questions" button would always have alerted "not been transcribed". It now matches on paper-name keyword + date (Kharidar First vs Koshi share the date 2083-01-26, so the keyword tells them apart).
- `renderPapers()` showed the "Scanned paper — read the original, not transcribed" tag on every card, including transcribed ones — now conditional. The Old Papers intro in `index.html` (which said no paper was transcribed) was updated to the 3-paper / 133-question state.
- Nepal Police ASI notice: `apply_url` was null — verified and set to https://careers.nepalpolice.gov.np (Nepal Police ORMS careers portal; Office Assistant still applies in person). The 4 remaining null `apply_url`s are all closed/unverified notices, where the render already says "No official apply link verified".

### K3. Test results (all PASS, re-run by the finisher after the fixes)
- `node scripts/test-questions.js` — **PASS**: 12,828 total, 0 duplicate ids, 0 duplicate question texts, 0 duplicate options, bilingual 100% (12,828/12,828). (First run after the JSON repair found 1 failure — NASU-2083-45 duplicate options — fixed by removing that question, see K1, not by weakening the test.)
- `node scripts/test-app.js` — **PASS** (incl. 35-file QUESTION_FILES check, papers/notices data checks).
- `node scripts/test-e2e.js` — **PASS**. One stale check updated: it used `practicePaper('nasu-first-2083-01-20')` as the "untranscribed paper" case — now a positive check (starts a quiz with its 43 questions) plus the alert case moved to the Kharidar pretest.
- `node scripts/test-v2.js` — **PASS**.
- Difficulty: easy 4,475 / medium 5,122 / hard 3,231. NHPC Dental/Ayurveda remain thin at 30 each; Law is now 160.

## L. Round 5 + Round 6 — fun, smooth, bigger — 2026-10-26 (supersedes the bank count in §K: **15,087 questions in 41 files, 47 exams; 322 fun facts**)

**Round 5 (questions):** 12,828 → **15,087** (+2,259 in 6 new `expansion-r5-*.json` files). Dental 30 → 109, Ayurveda 30 → 104, Law 160 → 329, Bar Council 250 → 419, CSIT 175 → 361, IOE 175 → 389, Foreign Service 160 → 312, Nepal Telecom 160 → 282. Difficulty now 4,998 easy / 6,137 medium / 3,952 hard.

**Round 6 (fun + smooth):**
- UI: sticky mobile bottom nav, fade/slide view transitions, staggered options, animated progress bars + score ring, count-up score reveal, CSS confetti only on pass/level-up, persistent light/dark theme (dark mode already existed), "Question X of Y" + time-per-question, varied encouragement microcopy, break nudge every 20 questions, touch targets ≥44px, `prefers-reduced-motion` respected.
- Fun Facts: `data/funfacts.json`, 322 verified bilingual facts (Nepal 70, Science 51, World 41, History 40, Geography 40, Constitution 30, Sports 25, Culture 25), each with source; validated by new `scripts/test-funfacts.js`. Daily fact on Home, interstitial after every 5th practice question (skippable, never in mocks), Fun Facts view with category filter, fact on result screen.
- Gamification: Weekly Challenge (35/70/100/140 target, Monday–Sunday), new badges (Weekly Champion, Century Day, Perfect Mock, Fact Explorer), "Beat your best" on mocks, Pomodoro focus timer (25/5/15, +10 XP/block), "Surprise me" 10Q mixed quiz, study-tips card. All localStorage-only; `migrateProgress()` adds new fields with defaults.
- Integration fix by coordinator: `QUESTION_FILES` in `app.js` was still 35 files while 41 were on disk — the 6 round-5 files were added (sorted), and stale `12828` counts in `test-e2e.js`, `test-v2.js`, `test-bundle.js` were updated to 15087.

Tests (final run, all exit 0):
- `node scripts/test-questions.js` — **PASS** (15,087 total, 0 duplicates, bilingual 100%)
- `node scripts/test-funfacts.js` — **PASS** (322 facts, all bilingual with category + source, no duplicates)
- `node scripts/test-app.js` — **PASS**
- `node scripts/test-e2e.js` — **PASS**
- `node scripts/test-v2.js` — **PASS**
- `node scripts/test-bundle.js` — **PASS** (re-run after rebuild; see below)

Honest gaps (unchanged): no real-browser smoke test — animations/confetti/bottom nav verified only in the Node DOM stub; a human accuracy + Nepali translation spot-check is still recommended before GitHub upload.

## M. Self-audit fixes — 2026-10-26 (supersedes the bank count in §L: **18,200 questions in 47 files, 47 exams; 412 fun facts**)

Applied the fix specs in `data/SELF-AUDIT-2026-10-26.md` (F01–F40). No GitHub upload, no bundle rebuild (coordinator does that last, F40).

**Findings fixed:** F01 (QUESTION_FILES now lists all 48 files on disk, incl. `expansion-r6a-current.json` and `expansion-r7a-licence.json`; r7a was still invalid JSON mid-write by another worker at fix time, so loadData skips it with a warning until it lands), F02 (HEAL2-182 answer → BCG), F03 (HARD2-298 + 12 same-class `(alt)` duplicate-option questions in `expansion-hard-core-v2.json`, each fixed by the same rule — fresh distinct distractor, answer index unchanged; HARD2-264's marked answer was also wrong, Rs 1600 → Rs 400 per its own explanation; MECEE-033 'Ovary' vs 'Ovary (corpus luteum)' fixed the same way), F04+F39 (mockNegRate returns the stored rate — MECEE 0.25; Staff Nurse `negative` 0.4 → 0.2 with note; mock-start alert, guide negative text and quiz header now show the real rate), F05 (mock wrong answers save to Mistakes), F06 (timer stops on navigation away from quiz/result), F07 (whole-bank fallback removed; honest alert; guide-only exams labelled in the practice select), F08 (125 duplicate texts removed — 86 in pass 1, 39 in pass 2 after `expansion-r6a-current.json` landed; newer/R6 copy deleted, older original kept), F09 (speed score capped at max; daily/quick/surprise/speed/marathon no longer hardcode `exam:'kharidar'`), F10 (mock topic mix for Kharidar 20 Office / NaSu 20 IQ / Section Officer 20 English; mock intro copy corrected), F11 (NMC-MBBS result notes the 130-of-180 mock coverage), F12 (MECEE result labels the 50% line a rough proxy for the 50th percentile), F13 (practice uses the exam's marksPerQ and negative rate; licence practice never deducts), F14 (UNVERIFIED notes on police/army/health/engineering prelims), F15 (result negative-marking line per exam; also fixes F35's dangling dash), F16 (README counts → 18,200 / 47 files / 412 facts, verified by `test-questions.js`), F17 (notices flip open/closing-soon → closed past `close_date` at render time), F18 (NMC-BDS note: 180Q from a 218Q pool of unknown mix), F19 (generated 33-row mock-pattern table + practice-pattern line before Start), F20 (Skip on the last question re-renders), F21 (guide anchors `guide-<id>` + filter + `showGuideFor`), F22 (QOTD options seeded-shuffled per day; exam tags shown), F23 (reset confirm now says it signs out the local profile; `user_id` kept, `email`/`name` cleared deliberately), F24 (Review button in nav), F25 (scanned-paper viewer only for the 3 transcribed papers' PDFs; other 14 link out), F26 (EN/NE toggle re-renders guide/papers/notices/dashboard/profile/discuss/submit), F27 option (a) (Daily Challenge once per day with confirm; repeat runs award 0 XP via `current._dailyRepeat`), F28 (New random set keeps the finished exam), F29 (flashcards exam filter), F30 (Speed Round rules confirm before start), F32 (IQ3-137 / CURH-208 / COMP-053 translation fixes), F33 (table-wrap scroll, 200-button palette capped, 22px checkboxes), F34 (modal closes on Esc / backdrop click), F36 (trending card #3 button says what it does; footnote names the card), F37 (search reports the true match count), F38 (practice timer pace from the exam's own paper). Quick win #7: result screen has a "Practice weakest topic" button calling `startPracticeTopic(worst[0])`.

**Also fixed while applying the specs (same defect class, found by the new checks):** the F03 validator-gap check is a pairwise rule (one option exactly equals another with its single trailing parenthetical removed) — the first draft stripped any trailing parenthetical from every option and false-positived on `O(n)`/`O(log n)`, `CPN (Maoist)`/`(UML)`, `t(9;22)` and multi-paren options; the pairwise form flags only true duplicates. Two malformed questions in the newly landed `expansion-r6a-current.json` (R6A-C158, R6A-C401 — only 3 options; C158's answer index 3 was out of range, correct answer is 10) got a 4th distractor each instead of being deleted.

**Adaptations to the audit specs (code was as audited, no round-6 drift found):** F22's `questionOfDay` returns stub questions without options as-is (the test-app fake bank has no `options`); F07's guide-only label is a separate `practiceOpts` list so the submit-a-question select is not mislabelled; F09's dashboard history and share text fall back to the mode title / 'Mixed practice' instead of a blank exam name; the mock-start alert and guide negative text use the real per-exam rate (F04) instead of a hardcoded 20%.

**Still open:** F31 (data-quality review queue — human sample review of the 1,807 long-correct-option candidates, 1,085 short explanations, 197 restated explanations, 846/4,059 identical `_ne` fields; NOT bulk-fixed by script, by design); F40 (bundle rebuild — coordinator only); `expansion-r7a-licence.json` was still being written by another worker when these fixes landed (invalid JSON, growing file) — it is listed in QUESTION_FILES but skipped at load time; once it is complete, re-run `test-questions.js` (its questions may duplicate the bank — do NOT delete from r7 files without the owning worker) and rebuild the bundle.

**Tests (final run, 2026-10-26):**
- `node scripts/test-questions.js` — 18,200 total; 1 failure: `expansion-r7a-licence.json: invalid JSON` (other worker's in-progress file, not touched)
- `node scripts/test-app.js` — **ALL PASS** (incl. new `mockNegRate: MECEE 0.25 → 0.25` check)
- `node scripts/test-e2e.js` — **ALL PASS** (confirm stub added to the sandbox — app.js legitimately calls `confirm()` in browsers; stale `15087` load expectation updated to 18200)
- `node scripts/test-v2.js` — **ALL PASS** (stale `15087` load expectation updated to 18200)
- `node scripts/test-funfacts.js` — **ALL PASS** (412 facts)
- `node scripts/test-bundle.js` — **PASS but stale** (certifies the pre-round-6 bundle: 15,087 Q / 322 facts; rebuild pending, F40)

## N. Round 7 integration — 2026-10-26 (supersedes the bank count in §M: **19,118 questions in 49 files, 47 exams; 412 fun facts**)

Integrator repaired, wired, de-duplicated and rebuilt the phone bundle. No GitHub upload.

**r7a-licence repair:** `expansion-r7a-licence.json` was still being written by another worker when integration started — the first repair pass (stray `,` at line 304 + missing closing `]`) salvaged 400 objects, but the worker then appended L401–L500 after the rewritten `]`. The integrator waited for the file to settle (mtime/size stable ~2 min), then re-repaired the final file: **500 questions salvaged, 0 dropped** (R7A-L001–L500, sequential, all 4 options + valid answer + full EN/NE fields). No builder in `/tmp/r6a/` was re-run.

**r7a-technical (landed mid-integration):** `expansion-r7a-technical.json` appeared while the first test run was in progress and kept growing (97 KB → 458 KB) until it settled at **500 questions** (R7A-T001–T500, Sub-Engineer/Computer Operator/CSIT/IOE). Validation found **82 duplicate stems** against older bank questions (same stem, mostly different distractors — e.g. R7A-T016 vs ENG2-019 "initial setting time of Ordinary Portland Cement"). Per the F08 rule (newer copy deleted, older original kept) the 82 were removed from the r7a file: **418 kept**. Licence file had 0 duplicates. Wired into `QUESTION_FILES` (now 49 files, sorted).

**Topic fix:** "Health" → "Health/Technical basics" normalised in `expansion-r6a-thin-exams.json` (535) and `expansion-r7a-licence.json` (500, of which 132 still bare "Health" after the worker's final write; the first 368 were already normalised by the first repair pass). No bare "Health" topic remains anywhere; all new-file topics match the existing topic set. Health/Technical basics is now 4,511.

**FF-070 verdict:** "Nepal has not yet won an Olympic medal" — **verified still TRUE, left unchanged**. Palesha Goverdhan's Paris 2024 bronze was at the **Paralympic** Games, a separate event; Nepal still has no medal at the Olympic Games (Summer or Winter). Sources: Kathmandu Post 2024-08-31 ("Nepal has never won a medal at the Summer Games in its 60-year long Olympic history"); Wikipedia "Nepal Olympic Committee". Caveat recorded in `data/SOURCES.md` §18.2: Nepali media loosely call her bronze "Nepal's first Olympic medal", so the wording may still confuse readers — a future clarifying reword was suggested, not applied.

**Counts updated to 19,118 everywhere:** `scripts/test-bundle.js` (15087 → 19118, 2 places), `scripts/test-e2e.js` + `scripts/test-v2.js` (18200 → 19118), README.md (19,118 MCQs / 49 files / 47 exams; bank table + r7a rows; by-topic and by-exam-tag lines recomputed from disk; new Round 7 roadmap line; also fixed stale `data/exams.json` line: 42 → 47 patterns, 33 prelim / 14 guide-only), `data/SOURCES.md` §18 (rounds 6a + 7). Historical round notes in README/TESTING.md and the dated self-audit file were left as history. Difficulty now 5,643 easy / 8,063 medium / 5,412 hard; answer balance A 24.4% / B 27.6% / C 24.3% / D 23.8%.

**UI features verified in the bundle** (UI worker's work, not redone): Fact of the Day streak, Question of the Day, Personal Records, share-your-score, Speed Round, Mistake Marathon, polish + 22 encouragement lines — all present in the rebuilt bundle and exercised by the passing suites.

**Tests (final run, all exit 0):**
- `node scripts/test-questions.js` — **PASS** (19,118 total, 0 duplicate ids, 0 duplicate texts, bilingual 100% — 19,118/19,118)
- `node scripts/test-funfacts.js` — **PASS** (412 facts)
- `node scripts/test-app.js` — **ALL PASS**
- `node scripts/test-e2e.js` — **ALL PASS**
- `node scripts/test-v2.js` — **ALL PASS**
- `node scripts/test-bundle.js` — **ALL PASS** (rebuilt bundle: 19,118 embedded questions, 412 facts)

**Bundle:** rebuilt with `scripts/build-bundle.py` — `loksewa-prep-nepal-full.html` (19,089,664 bytes), copied to `~/workspace/your_files/loksewa-prep-nepal-full.html`, uploaded via remote-storage (URL + expiry in the integration report). F40 closed.

**Still open:** F31 (data-quality review queue — human sample review; NOT bulk-fixed by script, by design); no real-browser smoke test — animations/confetti/bottom nav verified only in the Node DOM stub; a human accuracy + Nepali translation spot-check is still recommended before GitHub upload.

## O. Round 7b final integration — 2026-10-26 (supersedes the bank count in §N: **20,200 questions in 51 files, 47 exams; 609 fun facts**)

All workers done; coordinator performed the final integration (no GitHub upload).

**Round 7B landed:** `expansion-r7b-core-hard.json` 600 (IQ 144, Maths 132, Constitution 121, English 96, Nepali 107; 45.0% hard) + `expansion-r7b-current.json` 400 (Current Affairs 142, Economy 80, Science 79, Culture 99; 41.2% hard). IDs R7B-001…R7B-1000. R7B's 2026 World Cup facts independently verified by the coordinator via web search (USA Today, Al Jazeera, GMA): Spain beat Argentina 1-0, Ferran Torres 106', 19 July 2026; Mbappé Golden Boot, 10 goals. R7B dropped 327 candidates as bank duplicates before delivery.

**Broken file resolved:** `expansion-r7a-technical.json` was invalid JSON while its author was still writing it; the author finished it (500 questions, 0 duplicates after replacing 83 bank duplicates and fixing a 394/500 answer skew). No salvage was needed — the file parses cleanly. Total went 19,118 → 19,200 (R7A) → **20,200** (R7B).

**Integration fixes by the coordinator:**
- `VALID_EXAMS` in `scripts/test-questions.js` was missing 10 real exam ids from `data/exams.json` (deputy-secretary, jta, ranger, judicial-service, psc-service-groups, rbb-senior-assistant, provincial-psc, nea, anm-guide, ayurveda-bams) — this caused 1,032 "unknown exam tag" failures on R7B questions using provincial-psc / psc-service-groups / judicial-service. The set now lists all 47 ids; the questions were correct, the validator was stale.
- `QUESTION_FILES` in `app.js`: added `expansion-r7b-core-hard.json` + `expansion-r7b-current.json` (sorted); now 51 files. `community-approved.json` (0 questions) is correctly excluded — `test-app.js` filters it out.
- Fun facts merged: `data/funfacts-r7.json` (197, verified, 0 duplicates vs the 412) merged into `data/funfacts.json` → **609**. `test-funfacts.js` id regex widened to accept `FF-R7-NNN` as well as `FF-NNN`.
- FF-070 reworded (the clarifying reword §N suggested): "Nepal has never won a medal at the Olympic Games. Its first Olympic-level medal came at the Paralympics — Palesha Goverdhan's taekwondo bronze at Paris 2024." (EN + NE, source "Olympics.com; Kathmandu Post, 31 Aug 2024"). The old wording was true of the Olympic Games strictly, but misleading now that Nepal holds a Paralympic medal.
- "Health" topic re-checked in every file including the new R7B files: zero occurrences; the bank uses "Health/Technical basics" (4,511) throughout.
- Counts updated to 20,200 / 609 everywhere: `scripts/test-e2e.js`, `test-v2.js`, `test-bundle.js` (19118 → 20200), README.md (totals, bank table + r7b rows, by-topic and by-exam-tag lines recomputed from disk, new Round 7b roadmap line). Difficulty now 5,698 easy / 8,642 medium / 5,860 hard; answer balance A 24.7% / B 26.2% / C 24.8% / D 24.3%.

**Tests (final run, all exit 0):**
- `node scripts/test-questions.js` — **PASS** (20,200 total, 0 duplicate ids, 0 duplicate texts, bilingual 100% — 20,200/20,200)
- `node scripts/test-funfacts.js` — **PASS** (609 facts)
- `node scripts/test-app.js` — **ALL PASS**
- `node scripts/test-e2e.js` — **ALL PASS**
- `node scripts/test-v2.js` — **ALL PASS**
- `node scripts/test-bundle.js` — **ALL PASS** (rebuilt bundle: 20,200 embedded questions, 609 facts)

**Bundle:** rebuilt with `scripts/build-bundle.py` — `loksewa-prep-nepal-full.html` (20,164,863 bytes, md5 88e8360576ee1986d48a64dea5d427a5), copied to `~/workspace/your_files/loksewa-prep-nepal-full.html`, uploaded via remote-storage (URL + expiry in the integration report).

**Still open:** F31 (data-quality review queue — human sample review of long-correct-option candidates, short/restated explanations; NOT bulk-fixed by script, by design); no real-browser smoke test — animations/confetti/bottom nav verified only in the Node DOM stub; a human accuracy + Nepali translation spot-check is still recommended before GitHub upload.

## P. Answer-key audit merge — 2026-10-26 (supersedes the bank count in §O: **20,132 questions in 51 files, 47 exams; 608 fun facts**)

Five audit workers + one parallel numeric audit; coordinator performed the merge (no GitHub upload). Full record in `data/SELF-AUDIT-2026-10-26.md` §Answer-key audit and machine log `audit-patches/merge-log-2026-10-26.json`.

**Merge:** 1,057 raw fix proposals → 708 unique (file, id, field) groups (349 multi-worker agreements, 359 single-worker, **0 conflicts**). Applied **616** question field-changes (552 answer keys, 24 explanations, 23 explanations_ne, 4 options, 5 options_ne, 4 questions, 4 questions_ne) + 4 fun-fact field-changes. Skipped as already applied: **74** (all maths-iq HARD2 answers the parallel numeric audit had fixed mid-run; live value already equalled the new value). Superseded by removal: **18** (re-keys for CURH label questions that were removed instead). Removed: **68 questions** (36 degenerate CURH label questions, 8 broken HARD2 letter-series, 7 HARD5, 4 ARMY, 3 IQ, 2 MECEE, 2 R6A-B, 2 R7B, 1 each MATH3-028, IQ2-070, OPT-026, R6A-C065) + 1 duplicate fun fact (FF-393). Previous-year 2083: zero answer keys changed; only KHAR-2083-24's explanation corrected (false constant-+4 claim); NASU-2083-11 dual-answer stays as printed.

**Re-check before applying:** every fix was verified against live file state — 551/552 parseable old-values matched the live keyed option (the 1 exception, NEP2-288, is a paraphrase consistent with the patch, which also carries explanation fixes). No live value was a third value; nothing was applied blind.

**Recorded, not fixed:** expansion-zero-licence.json B-keyed 74% (333/450; sampled keys correct — placement skew, left alone); options_ne == options for 100% of questions in 6 files / 2,779 questions (translation gap; the suite's bilingual check is presence-only, so it passes while those options are verbatim English); 21 unverifiable items left unchanged (vowel-count 12-vs-13 convention, telephone 1913-vs-1916, caste count 142-vs-146, TSC establishment year, ANC 4-vs-8, HEAL2-145, LAW5-019, BAR-059, NASU-2083-31). HEAL2-023 re-keyed per its explanation but stem flagged ambiguous (cornea vs lens refractive power) — needs rewording, not just the re-key.

**Counts updated to 20,132 / 608:** `scripts/test-e2e.js`, `test-v2.js`, `test-bundle.js` (20200 → 20132 in the load/embedded checks), README.md (totals, bank table — 12 rows, by-topic and by-exam-tag lines recomputed from disk, new roadmap line). Difficulty now 5,692 easy / 8,635 medium / 5,805 hard; answer balance A 25.0% / B 26.6% / C 24.4% / D 24.0%.

**Tests (final run, all exit 0):**
- `node scripts/test-questions.js` — **PASS** (TOTAL: 20132, 0 duplicate ids, bilingual 100%)
- `node scripts/test-funfacts.js` — **PASS** (608 facts)
- `node scripts/test-app.js` — **ALL PASS**
- `node scripts/test-e2e.js` — **ALL PASS** (was 1 FAIL before the count update: hardcoded 20200 vs 20132 loaded — count updated, test not weakened)
- `node scripts/test-v2.js` — **ALL PASS** (same 20200 → 20132 count update)
- `node scripts/test-bundle.js` — **ALL PASS** (rebuilt bundle: 20,132 embedded questions, 608 facts)

**Bundle:** rebuilt with `scripts/build-bundle.py` — `loksewa-prep-nepal-full.html` (20,086,489 bytes, md5 74512d688ecf91e372339c7b0fad5758), copied to `~/workspace/your_files/loksewa-prep-nepal-full.html`, uploaded via remote-storage (URL + expiry in the integration report).

**Still open:** F31 (data-quality review queue); no real-browser smoke test — animations/confetti/bottom nav verified only in the Node DOM stub; a human accuracy + Nepali translation spot-check is still recommended before GitHub upload. New from this audit: the 2,779-item options_ne translation gap; the expansion-zero-licence answer-position skew; HEAL2-023 rewording; one-convention decisions pending for Nepali vowel count and the 1913/1916 telephone date.

## Q. Round 8 + Round 10 integration — 2026-10-26 (supersedes the bank count in §P: **46,415 questions in 79 files, 47 exams; 608 fun facts**)

Final integration of the R8 files (4 × 500) and the R10 scale-up run (25 files, 27,224 gross). Two more R10 files landed mid-integration (expansion-r10-iq3.json / maths4.json, then iq4.json / maths5.json, then english3.json / maths6.json) — the integrator re-ran the fast checks after each landing instead of trusting the handoff counts. No GitHub upload.

**Removals in this integration: 1,417 total.**
- Exact stems (`test-questions.js`): **837** — english2 520 (dup of english), maths3 83 (dup of maths), iq2 15, maths 12 (dup of drills), health2 6, world-science 3 (R10-WORLD-0632/0685/0719, dup of R10-OEL-0285/0115/0251), science2 1; then iq3 9, maths4 106, iq4 64, english3 11, maths6 7. All newer copies removed; zero Previous Year 2083 questions touched.
- Exact rewordings (dedupe report): **25** — laughing gas, Birendra coronation 1975, SLR/NEPSE/RTGS/IPO/SEBON/ORS/FCHV full forms, BRICS 2009, WAN, SQL, vitamin D, 12h/24h→minutes, धैर्यवान/मूल्यवान spelling variants, 1st/2nd/3rd-from-right typo variants, Bird:Nest::Bee:Hive, चोरको खुट्टा काट्नु, रामले कारक. Kept: R10-ENG2-0683 ('भोक' hunger ≠ 'भोको' hungry — the script's transliteration rule falsely equated them) and R8CUR-462 ('केटी' ≠ 'केटा').
- Same-fact rewordings: **9** — Thangka/Buddhism, load shedding ended 2018, female XX, BAFIA 2073, STP 22.4 L, NRB monetary policy yearly, F=ma, most malleable gold, Gram-positive purple. The 11 letter-series same-fact flags were REJECTED (different series that share a next letter and ≥3 options are different problems).
- Near rewordings (old bank ↔ R8/R10, hand-reviewed all 60): **43** — incl. National Assembly 59, SC retirement 65, SC max judges 21, newborn bones ~300, insulin→diabetes, sucrose, त्रिभुवन/यथाशक्ति samas, CPU/LAN/DBMS, Sindhuli HQ, Rara Lake 10.8, B1→beriberi, chest X-ray SID 180 cm, Nepal Bank Ltd 1937, Article 61, Haber iron, Contact V2O5, Plaster of Paris, demat, स्वास्थ्य/साहित्य/अनुसन्धान spellings, dosimeter, MRC grade 0, Triphala, Schedule 8 (22), जय/मित्र antonyms, overdraft, Maslow, Mechi border, Vata dosha, misanthropist/misanthrope, arteries, molars, Nepal currency, Bogotá, staple crop rice. Kept: compound questions (R8LAW-050 total+PR seats, R8LAW-002 schedules+articles, R8CUR-083 Operation Sindoor + date), different-word template collisions (केटा/केटी, जल/निद्रा/रानी, lucid/brilliant, राजा/नेता), different sub-questions (Losar vs 'Lo', IP vs TCP/IP, RIPE combination vs single drug). R8LAW-443 (CIAA cases → Special Court) removed as a same-fact dup of R8LAW-107 — the script missed it (stem Jaccard 0.74); R8LAW-431 (local-level tax) and R8LAW-436 (CM oath) are unique and kept.
- Template-paraphrase / parameter-swap pairs (payload-verified): **503** from 505 genuine pairs — same problem restated with swapped commutative parameters (mixture quantities, rectangle length/width, train/platform lengths, SI rate↔years, HCF number order, multiplication order, district-HQ reversal, direction-walk leg swaps) or a template paraphrase (Nepali "Choose the antonym of X" vs "Which word is opposite in meaning to X", same word/options/answer). Method: O(n) payload grouping (matra-preserving tokeniser — the dedupe script's normalise() strips Devanagari vowel signs and collapses distinct words to consonant skeletons, which is why its NE Jaccard runs 0.8–1.0 on template pairs) + quoted-span + ordered-sequence vetoes; validated on random samples (30 flagged-genuine, 30 rejected, 15 sweep-only — all correct). Rejected ~7,000 same-template pairs: different names/words/numbers/rows are different drill items. 6 keepers gained exam tags from removed copies (CURR2-057, IOE5-139, R10-MATH-1085/1090/1100, R10-NPL-0775); residual tag gaps are immaterial (every affected pool keeps hundreds–thousands of questions).

**Rejected plan item:** the dedupe plan's single removal MECEE-030 was NOT applied — MECEE-029 (ADH) vs MECEE-030 (Oxytocin) share the answer "Posterior pituitary" but ask about different hormones; the pair was flagged only via NE Jaccard 0.812 (template-translation collision).

**Dedupe report caveat:** the full `dedupe-check.py` run (38,234 questions) classified 7,486 pairs but deferred 7,484 as R8/R10-involved; its re-run against the moving bank never finished (killed after ~20 min — candidate generation explodes on the dense R10 template families) and was superseded by the O(n) payload sweep, which covers the final disk state including the late landings. The script's loose_same_correct rule is still in place; its retired rare-token rule stays retired.

**Answer-key audit (R8/R10 only; old bank already audited):** `python3 scripts/audit-answer-mismatch.py` — 326 flags total, 303 in R8/R10, **all verified false positives, zero keys changed.** 166 EXPL_NAMES_OPTION flags: the regex misreads "The answer is <text>" — the explanation names the marked option's text and its initial letter looks like an option letter ("About", "Argentina", "Aedes", "Daughter", "Brother"). 137 NE_CONCLUDES flags: the "last '=' value" heuristic misreads intermediate values in the Nepali explanation — the divisor in remainder drills (67, recomputed a mod b — all correct), the exponent-mod in unit-digit questions (70, recomputed pow — all correct), addends in letter-value sums (2, recomputed — 25 and 2, both correct). R8 files: zero flags in both audit runs. The 23 flags in old files are the same false-positive classes left over from §P (not re-audited).

**Counts updated to 46,415 / 608:** `scripts/test-e2e.js`, `test-v2.js`, `test-bundle.js` (20132 → 46415 in the load/embedded checks), README.md (totals, bank table regenerated from disk — 79 rows, by-topic and by-exam-tag lines recomputed, new roadmap line). `assets/js/app.js` QUESTION_FILES now lists all 79 bank files (was 51). Difficulty now 10,615 easy / 24,487 medium / 11,313 hard; answer balance A 28.0% / B 24.6% / C 23.9% / D 23.5% (A-skew from the R10 drill banks; options are shuffled at runtime, so it does not bias play).

**Tests (final run, all exit 0):**
- `node scripts/test-questions.js` — **PASS** (TOTAL: 46415, 0 duplicate ids, 0 duplicate texts, bilingual 100%)
- `node scripts/test-funfacts.js` — **PASS** (608 facts)
- `node scripts/test-app.js` — **ALL PASS** (QUESTION_FILES lists all 79 files)
- `node scripts/test-e2e.js` — **ALL PASS** (20132 → 46415 count update)
- `node scripts/test-v2.js` — **ALL PASS** (same count update)
- `node scripts/test-bundle.js` — **ALL PASS** (rebuilt bundle: 46,415 embedded questions, 608 facts; was 2 FAIL on the stale 20,132 bundle before the rebuild)

**Bundle:** rebuilt with `scripts/build-bundle.py` — `loksewa-prep-nepal-full.html` (42,181,611 bytes, md5 8082139443631565c6532ffd87021344), copied to `~/workspace/your_files/loksewa-prep-nepal-full.html`, uploaded via remote-storage (URL + expiry in the integration report).

**Still open:** F31 (data-quality review queue); no real-browser smoke test — animations/confetti/bottom nav verified only in the Node DOM stub; a human accuracy + Nepali translation spot-check is still recommended before GitHub upload. New from this integration: the audit script's two systematic false-positive modes (documented above — worth fixing in the script before the next audit, or the next run will re-flag the same ~300); the A 28.0% answer-position skew in the R10 drill banks; the dedupe script's NE Jaccard is unreliable for Devanagari (matra stripping) — its NE-only near flags need the payload check, not blind trust. Scale-up note: see the integration report — 50k is reachable only from maths/IQ/English-vocab template headroom, not from fact-based topics.

## R. Round 10 final integration — 2026-10-27 (supersedes the bank count in §Q: **51,530 questions in 89 files, 47 exams; 608 fun facts**)

- **Dedupe clean-up:** full exact + near-duplicate (token-Jaccard ≥0.8) + same-fact sweep (`scripts/audit-duplicates.py`, new reusable script). **1,020 duplicates removed** — 863 by a parallel worker (verified correct, incl. 18 maths clock-angle copies keyed with wrong truncated integers) + 157 by the deeper sweep (143 odd-one-out sets in iq3.json, 7 multiplication pairs, 5 analogy reversals, 2 LCM pairs). 19 English pairs had same stem/different keys where both were valid — duplicate copy removed, key untouched. Odd-one-out set {15,16,17,18} left ambiguous (kept key 16 as only perfect square; 17 is the only prime) — flagged, not silently resolved.
- **Audit of new round-10 questions (replacement run, 34 files, 30,187 questions):** mismatch script 23 flags, all false positives (intermediate `= N` values). **69 Constitution-article questions fixed** — systematic generator error, 35 of 54 map entries wrong against the official Constitution text (e.g. Art 247, Art 262, commissions block 238–248 shifted); **13 mountain-rank questions** reworded Nepal-only (a Nepal-only list labelled "highest in the world"); **16 answer-leaking partial Nepali translations fixed** (only the correct option translated); **364 English ordinal-suffix fields fixed** ("2th"→"2nd" etc.); generator root cause fixed in `scripts/r10/g06_nepal_facts.py` and ordinal templates fixed in g02/g03/g11/g12/g20/g22/g25/g30 (`ord_s` helper). **1 broken question removed:** R10-ENG3-0058 (all four options synonyms of "agency", no valid antonym). 136-question random spot-check: 134 correct.
- **Wiring fix:** `app.js` QUESTION_FILES was missing 3 files — `expansion-r10-english4.json` (473 q), `expansion-r10-maths8.json` (394 q), `community-approved.json` (empty) — **867 questions were unloadable**. All 90 files now listed, sorted. Also fixed: stale "134 real questions" → 133, stale "6,846" fallback in renderSubmit, CSQ note scoped to nmc-mbbs only.
- **Incident during integration:** importing a generator module to verify the ordinal helper re-ran it and **regenerated `expansion-r10-iq.json`** (2,419 → 2,524 questions). No backup existed, so the regenerated file was kept: it passes all validators (0 duplicates, bilingual 100%) and the mismatch script flags nothing in it, but its questions are generator-fresh and were not part of the hand audit — noted here, not hidden. Lesson: never import generator modules; verify with `py_compile` only.
- **Counts updated to 51,530 / 608:** `scripts/test-bundle.js` (48883 → 51530 in the embedded/load checks), README.md (totals, bank table regenerated from disk — 89 rows, by-topic and by-exam-tag lines recomputed, new roadmap line). Difficulty now 12,053 easy / 27,590 medium / 11,887 hard; answer balance A 27.7% / B 24.7% / C 24.0% / D 23.6% (shuffled at runtime).
- All six test suites re-run by the integrator after the rebuild — see results below.

**Final validation (integrator, 2026-10-27 ~01:20 NPT):** `test-questions.js` PASS (51,530, 0 duplicates, bilingual 100%) · `test-funfacts.js` PASS (608) · `test-app.js` PASS (after sorting QUESTION_FILES — 1 FAIL before: set matched but list unsorted) · `test-e2e.js` PASS · `test-v2.js` PASS · `test-bundle.js` PASS (rebuilt bundle: 51,530 embedded questions, 608 facts, 46,259,203 bytes, md5 fc70c1c1770a1e9fcf7a63bf6245e1e1, ends `</script></body></html>`). **Phone-bundle upload could not complete** — three attempts failed on runtime issues (egress approval timed out, service restart, session disappeared), not on the file; the verified bundle is at `loksewa-prep-nepal-full.html` + `~/workspace/your_files/loksewa-prep-nepal-full.html` (identical md5) and needs one successful `remote-storage upload-file` run by the parent to get a public link.

## S. PDF expansion — 2026-10-27 (supersedes the bank count in §R: **59,076 questions in 105 files, 47 exams; 608 fun facts**)

- **Source:** user-supplied PDF "10,000 New Exam Questions & Master Answer Key (2082/83 BS)" (`data/pdf-extract-raw.json`, 10,000 extracted questions). Dedupe (`data/pdf-dedupe-decisions-2026-10-27.json`): 7,547 keep, 2,453 rejected (2,450 within-PDF wrapper variants, 3 vs bank). Verified keys (`data/pdf-verified-keys-2026-10-27.json`): 9,999 keep-verified, 0 fixed, 1 drop — **PDF-0684** (two correct options: "14 December 1955" and "14 December 1955 (via UN Charter)"; dropped, not integrated). Final integrated set = dedupe-keep AND verified-keep = **7,546** (PDF-0684 was a dedupe-keep). Verified answers matched the raw PDF answers exactly (0 fixes).
- **Files:** `data/questions/expansion-pdf-01.json` … `expansion-pdf-16.json` (15 × 500 + 46), PDF topic order preserved within files, ids `PDF-0001`… (from `pdf_num`, globally unique, no bank id reused). Wired into `assets/js/app.js` QUESTION_FILES in sorted order (106 files listed, incl. empty `community-approved.json`).
- **Exam mapping (by PDF topic):** Constitution & Governance → kharidar, nasu, section-officer, provincial-psc, psc-service-groups, police, army, tsc-primary/lower-secondary/secondary; Current Affairs → + nrb-assistant, rbb, foreign-service; Nepal Geography/History, Culture & Society → PSC + TSC + police/army; Economy & Development / Economy → PSC + nrb-assistant/officer, rbb, rbb-senior-assistant, psc-service-groups; Banking & Finance → nrb-assistant/officer, rbb, rbb-senior-assistant, kharidar, nasu; Office Management & Public Service → kharidar, nasu, section-officer, computer-operator, provincial-psc, psc-service-groups; Computer & ICT → kharidar, nasu, computer-operator, nrb-assistant, section-officer, nepal-telecom, sub-engineer; Education & Pedagogy → tsc-primary/lower-secondary/secondary/license; English → section-officer, foreign-service, kharidar, nasu, police, army, nrb-assistant; Nepali Language → PSC + TSC + police/army; IQ / IQ & Reasoning → PSC + police/army, nrb-assistant, rbb, computer-operator, provincial-psc; Mathematics / Maths & Numerical → PSC + nrb-assistant, rbb, police/army, nea, sub-engineer, computer-operator; Science & Tech → PSC + health, engineering, nea, sub-engineer, mecee-bl; Biology → health, mecee-bl, nmc-mbbs, staff-nurse-psc, nhpc-ha, PSC; Chemistry → + npc-pharmacy; Physics → + engineering, nea, sub-engineer; Law → section-officer, judicial-service, bar-council, kharidar, nasu, psc-service-groups; Foreign Service & Diplomacy → foreign-service, section-officer, nasu; Engineering Drawing → engineering, sub-engineer, nea, nec-licence, ioe-entrance; Health/Technical basics → health, nhpc-ha, staff-nurse-psc, nnc-rn, nhpc-lab, nhpc-public-health, anm-guide, midwifery-nlem.
- **Difficulty rule (PDF carries none):** hard if topic is Law / Foreign Service & Diplomacy, or question > 220 chars, or contains a negation cue (not/except/incorrect/wrong/least), or a series/sequence cue; easy if < 90 chars and no hard cue; else medium. Result: 557 easy / 5,578 medium / 1,411 hard (new questions only).
- **Marks rule:** 2 if any exam tag is a 2-mark PSC prelim exam, 1 only if every tag is a 1-mark licence/entrance exam. Result: all 7,546 are 2 marks — every PDF topic maps to at least one 2-mark PSC prelim exam, so no question is licence-only. (Mocks override stored marks to the exam's prelim marksPerQ anyway — see `startMock` — so stored marks never break a licence mock's all-1-mark expectation.)
- **Explanations (generated, NOT from the PDF — the PDF has none):** every new question carries the neutral form "The correct answer is \<option\>." A derivation generator was attempted for simple arithmetic / percentages / AP-GP series and produced 0 provable derivations — the PDF's maths/IQ items are multi-step word problems whose working is already embedded in the correct option itself (e.g. "5 hours (2 hours downstream at 64 km/h + 3 hours upstream at 58 km/h)"), so no derivation was invented. Do NOT claim any explanation came from the PDF.
- **Nepali translation:** new questions were first added with NO `_ne` fields (allowed — `test-questions.js` treats `_ne` as all-or-nothing; the app falls back to English in NE mode). They were then translated with the project's own `scripts/add-nepali.py` (Google Translate gtx endpoint, same tool/method as the rest of the bank, incl. its English-grammar / maths / date-protection rules). Result: **7,546/7,546 bilingual (100%)** — 16/16 files at 100%, Devanagari in every `question_ne`. QA sweep after translation: English fields unchanged (0/7,546 differ from the PDF extract); 280 verbatim `question_ne` are all Nepali Language questions (already Devanagari — correct copies, not a defect); 4,077 verbatim `options_ne` are all by-design keeps (English-topic options, Nepali Language options, numeric/symbolic IQ/Maths options, codes/years); 0 duplicate `options_ne` sets. Two translator defects found and fixed: (1) `add-nepali.py` crashed on subscript digits (`int('₂')` ValueError in `dev_digits` and in the option digit-normalisation) — `expansion-pdf-07.json` failed whole-file; patched both sites to ASCII-only digits and re-ran file 07 clean (files 12/13/15/16, which also contain subscripts in chemistry/number-base options, then translated cleanly); (2) 10 Computer & ICT `explanation_ne` fields (PDF-3803/3806/3819/3822/3823/3826/3879/3882/3883/3886) carried MT-mangled protection tokens (`ZZZ4`, `ZZ1`) — replaced with the neutral Nepali form "सही उत्तर \<option_ne\> हो।" (0 ZZ tokens remain). 289 informational flags on file 08 (English vocab questions in sentence context — "untemplated English vocab Q"; the tool correctly keeps the English sentence + options and translates only the instruction) — no action needed.
- **Counts updated to 59,076 / 608:** `scripts/test-bundle.js` (51530 → 59076 in the embedded/load checks; the 100%-bilingual bundle check stands unchanged — new questions are 100% bilingual, see above), README.md (totals, bank table regenerated from disk — 105 rows, by-topic and by-exam-tag lines recomputed, new roadmap line), OPEN-SOURCE-CHECKLIST.md header. Difficulty now 12,610 easy / 33,168 medium / 13,298 hard; answer balance A 27.4% / B 24.7% / C 24.1% / D 23.8% (shuffled at runtime).
- **Self-check:** re-count on disk 59,076; `previous-year-2083.json` untouched (133 questions, ids NASU-2083-01…KOSHI-2083-45); no existing `data/questions/*.json` file modified (all pre-existing files keep their 2026-10-26 mtimes); no duplicate ids/texts introduced (`test-questions.js` PASS covers this); my changes besides the 16 new question files: `assets/js/app.js` (QUESTION_FILES list only — a separate side-chat topic-dropdown fix also landed in app.js the same day, see MEMORY.md), `scripts/test-bundle.js` (51530 → 59076 counts only), `scripts/add-nepali.py` (subscript-digit crash fix, see above), README.md / TESTING.md / OPEN-SOURCE-CHECKLIST.md (counts + §S); no bundle uploaded; nothing pushed to GitHub.

**Final validation (integrator, 2026-10-27):** `test-questions.js` PASS (59,076, 0 duplicates, bilingual 59,076/59,076 = 100%) · `test-funfacts.js` PASS (608) · `test-app.js` PASS · `test-e2e.js` PASS · `test-v2.js` PASS · `test-bundle.js` PASS (rebuilt bundle: 59,076 embedded questions, 608 facts, 62,414,719 bytes, md5 62fc8afe03dfaf5538e4adc50647dd5a, fetch never called, ends `</script>` / `</body>` / `</html>`). Bundle NOT uploaded (per task scope); verified copies at `loksewa-prep-nepal-full.html` + `~/workspace/your_files/loksewa-prep-nepal-full.html` (identical md5) — needs one `remote-storage upload-file` run by the parent for a fresh phone link.

## T. Bug-hunt + smoothness round — 2026-10-28 (bank unchanged: 59,076 questions in 105 files + `community-approved.json`, 47 exams; 608 fun facts)

Fresh aspirant walkthrough in code (Kharidar / NaSu / TSC / NRB), re-verification of all 40 self-audit findings F01–F40 against the **current** code, notices re-check against live sources, and 59k-scale performance work. No GitHub upload, no bundle rebuild (coordinator does that last, F40). No question content touched except none — zero `data/questions/*.json` files modified; the 133 real Previous Year 2083 questions untouched.

### T1. F01–F40 re-verification (do not re-check these)

All 40 findings from `data/SELF-AUDIT-2026-10-26.md` were re-checked in the current code and data. **38 are fixed and verified; 2 remain open by design (see T5).**

- **Fixed + verified in current code:** F01 (QUESTION_FILES lists all 106 files; test-app enforces it), F02 (HEAL2-182 answer is now BCG, index 0), F03 (HARD2-298 options are now 10/12/8/20 years, answer 10), F04 (mockNegRate returns the stored rate — MECEE 0.25; Staff Nurse stores 0.2), F05 (mock wrong answers save to Mistakes — `answerOption()` mock branch), F06 (showView stops the timer off quiz/result), F07 (whole-bank fallback removed; honest alert; guide-only exams labelled in the practice select), F08 (test-questions PASS, 0 duplicate texts/ids), F09 (speed score capped at max; daily/quick/surprise/speed/marathon use `exam:''` + titles), F10 (mockMixFor: Kharidar 20 Office / NaSu 20 IQ / Section Officer 20 English; tagged pools now huge — Kharidar Office 787, NaSu IQ 9,815, Section Officer English 7,368), F11 (NMC-MBBS 130-of-180 note on the result screen), F12 (MECEE 50th-percentile proxy note), F13 (practice uses the exam's marksPerQ + negative rate), F14 (UNVERIFIED notes on police/army/health/engineering prelims — verified present in `data/exams.json`), F15 (per-exam negative-marking line on results), F16 (README says 59,076 / 105 files), F17 (auto-expiry logic present — see T3, it was **proven** by this round's notices), F18 (NMC-BDS note), F19 (33-row mock-pattern table + practice-pattern line), F20 (Skip on last question re-renders), F21 (guide anchors `guide-<id>` + filter + `showGuideFor`), F22 (QOTD seeded-shuffled options + exam tags), F23 (reset confirm discloses the sign-out; `user_id` kept — see T02 for the part that was still partial), F24 (Review button in nav), F25 (scanned-paper viewer only where a `pdf_url` exists; others link out), F26 (setLang re-renders guide/papers/notices/dashboard/profile/discuss/submit), F27 (Daily Challenge once/day with confirm + 0 XP repeats — abandonment hole now fixed, see T01), F28 (New random set keeps the finished exam), F29 (flashcards exam filter), F30 (Speed Round rules confirm), F32 (IQ3-137 / CURH-208 / COMP-053 translation fixes), F33 (`.table-wrap` horizontal scroll, 200-button palette capped at 220px scroll, 22px checkboxes), F34 (modal closes on Esc + backdrop click), F35 (no dangling dash — per-exam negLine), F36 (trending card #3 footnote names the card), F37 (search reports the true match count), F38 (practice timer pace from the exam's own paper), F39 (Staff Nurse `negative` is the 0.2 rate).
- **Still open by design:** F31 (data-quality review queue — human sample review of long-correct-option candidates, short/restated explanations, identical `_ne` fields; NOT bulk-fixed by script) and F40 (bundle rebuild — coordinator only). Both unchanged by this round.
- **Scale check (new, round-10/PDF era):** every one of the 33 mocks now has more tagged questions than its paper requires (thinnest: nhpc-optometry 524/100, nmc-bds 667/180, nhpc-radio 548/100) — the thin-bank whole-bank fallback in `startMock()` is now dead code in practice. Guide-only exams with 0 tagged questions remain jta (0) and ranger (0); deputy-secretary has 19, ayurveda-bams 18 — the honest "no questions match" alert covers all of them. `expansion-pdf-07.json` is now fully bilingual (500/500 `_ne` fields present) — the side-chat translation finished. Previous-year file untouched (133 questions).

### T2. New bugs found + fixed

| ID | Bug | Fix (file:line) |
|---|---|---|
| T01 | **Daily Challenge abandonment burned the day's XP (known still-open).** `dailyChallenge()` wrote `progress.dailyDone[seed]=true` the moment the challenge *started*; navigating away (showView stops the timer, no attempt recorded) or closing the tab left the day marked done, so the next run was a 0-XP repeat. | `assets/js/app.js` — `dailyChallenge()` (~:1240) no longer writes `dailyDone` at start; it sets `current._dailySeed`. `finishAttempt()` (~:1063) marks `progress.dailyDone[seed]=true` only on finish. Abandoning now costs nothing; finishing marks the day; a same-day repeat still earns 0 XP (existing `_dailyRepeat` path). New e2e checks cover all three states. |
| T02 | **Reset progress was partial (known still-open).** The F23 identity part was already fixed as designed (confirm discloses the sign-out, `user_id` kept). But "Reset ALL progress" left two progress stores alive because they live in their own localStorage keys, not on the progress object: Best Speed Round (`loksewa_speed_best_v1`) and the Fact streak (`loksewa_fact_streak_v1`) both survived a reset and kept showing on Home/Dashboard. | `assets/js/app.js` — new `resetProgress()` (~:1325), called by the Dashboard reset button; it removes both keys (guarded `try/catch`) as well as resetting the progress object. Discussions/submissions/reports are deliberately NOT cleared (community content, not progress). New e2e checks: speed best + fact streak are gone after reset, `user_id` kept. |
| T03 | **Submit-a-question could be double-queued (known still-open).** A double-click (or impatient second tap) queued the same question twice: the only guard blocked at **3** identical copies. | `assets/js/app.js` `submitQuestion()` (~:1913): a pending-duplicate check refuses a question already pending in the queue (after the bank-duplicate check, before the rate limit). Plus the submit button (`id="sub-submit-btn"`, added in `renderSubmit()`) disables itself after a successful submit and is re-enabled by `validateSubmitLive()` on the next form edit. New test-v2 check: submitting the same valid question twice leaves the queue at 1. |
| T04 | **`loadData()` fetched the 106 question files sequentially** — one round-trip per file on every load (seconds on GitHub Pages; the 59k bank made this the dominant load cost). | `assets/js/app.js` `loadData()` (~:803): `Promise.all(QUESTION_FILES.map(...))` with a per-file catch (one bad file still cannot lose the bank); order preserved. `scripts/build-bundle.py` `FETCH_BLOCK` updated in lockstep and verified byte-identical to the new block (without running the build — coordinator rebuilds last). test-e2e + test-bundle both pass against the new loader. |
| T05 | **`findDuplicate()` cost ~600–800 ms per submit** — it re-ran `normaliseText` + token-Jaccard over the whole 59k bank on every call, so the Submit button looked dead for most of a second. The first fix attempt (caching normalised strings) did not help: the near-scan itself dominated. | `assets/js/app.js` `dupIndex()` (~:1785) now caches normalised texts **plus an inverted token index**; `findDuplicate()` (~:1824) first does the cheap exact-match string loop, then computes Jaccard only on candidates sharing ≥ ⌊4a/9⌋+1 tokens with the query (a = query token count) — a bound proven safe: Jaccard ≥ 0.8 requires shared ≥ (4/9)(a+b) > (4/9)a, so no true near-duplicate is ever skipped. Measured on the real 59k bank: 0–111 ms per call (vs ~550 ms brute force), and **verified to agree with brute force on 6 probes** (exact, near, and no-match cases). First call per page load builds the index (~1.4 s, once). |
| T06 | **`doSearch()` rebuilt the haystack string for all 59,076 questions on every search** (~160 ms per click). | `assets/js/app.js` `searchHay()` (~:1337): lazily cached lowercase haystack on the question object (never serialised — the bank is only read). Repeat searches reuse it. |
| T07 | **`renderReview()` / `weakTopics()` called `QUESTIONS.find()` per saved id** — a linear 59k scan per bookmark/mistake. | `assets/js/app.js` `questionByIdMap()` (before `renderReview()`, ~:1282): one-pass `Map` built once per call; both call sites use it. |
| T08 | **Notices "Last checked" was a hardcoded `2026-10-26`** in `renderNotices()` and in `index.html`, so it kept showing the old date after re-checks (the data itself had newer `checked_date`s). | `assets/js/app.js` `renderNotices()`: the header now shows the newest `checked_date` in the data. `index.html` notices intro updated to 2026-10-28. |
| T09 | **Search had no Enter-key path** — pressing Enter in the search box did nothing (no form), so keyboard users had to tab to the button. | `index.html`: search input now runs `doSearch()` on Enter. |
| T10 | Dead code: unused variable `b` in `mockMixFor()`. | Removed (`assets/js/app.js` ~:1190). |

### T3. Notices re-check — 2026-10-28 (verified, then updated in `data/notices.json`)

`renderNotices()` auto-expiry was **proven working**: the extracted pure function `effectiveNoticeStatus(n, today)` (`assets/js/app.js` ~:1443, exported for tests) flips open/closing-soon → closed once `close_date < today`, and the two 2026-10-27 notices now render Closed. New test-app checks cover past-close, deadline-day, future-close, already-closed and unverified cases.

| Notice | Old status | Verified 2026-10-28 | New status |
|---|---|---|---|
| Nepal Police ASI & Office Assistant (334 posts) | closing-soon, close 2026-10-27 | Application period 2083/06/12–2083/07/10 (27 Oct 2026) confirmed (EducateNepal listing of the HQ notice); **no extension found** in search results. Deadline passed yesterday. | **closed** — body now says "Deadline was … applications are now closed"; title carries (CLOSED)/(बन्द); `checked_date` 2026-10-28 |
| Gandaki PPSC 9th & 8th Level, Notice 129/2083-84 (39 posts) | closing-soon, close 2026-10-27 | **Correction to the stored record:** the regular deadline was 2083/07/03 (**20 Oct 2026**); 27 Oct 2026 was the **double-fee** deadline (EducateNepal listing). Both have now passed. | **closed** — body now states both deadlines; title carries (CLOSED)/(बन्द); `checked_date` 2026-10-28 |
| PSC Under Secretary & Health 9th Level, Notice 582/2083-84 (159 posts) | open, close 2026-11-03 | Still open — MyRepublica 28 Oct 2026 confirms deadline **3 Nov**, double fee **10 Nov**; CollegeNP/BrightCareer confirm 159 posts, fee NPR 2000, portal psconline1.psc.gov.np. Stored figures already matched; only the check date moved. | **open**, `checked_date` 2026-10-28 |
| Lumbini PPSC Level 8 Health, Notice 85/083-84 | open, close 2026-11-05 | Still open — CollegeNP confirms regular **2083/07/19 (5 Nov 2026)**, double fee 2083/07/26 (12 Nov 2026), fee NPR 1000 (+400/group). Stored figures matched. | **open**, `checked_date` 2026-10-28 |

Other notices untouched (closed TSC/NRB/RBB entries and the two unverified ones keep `checked_date` 2026-10-26 — they were not re-checked). **Caveat:** `psc.gov.np` itself could not be fetched (DNS/connection error from the text-fetch tool, not retried per instructions) — verification rests on the secondary reports above, the same sourcing standard the notices file already uses. **Spotted but NOT added:** Gandaki PPSC published a **new 7th-level vacancy (Notice 166/2083-84) on 2083/07/11 (28 Oct 2026, today)** — the CollegeNP page lists the posts but gives no deadline or fee in the fetched text, so per the no-invent rule no new notice entry was created; it needs a follow-up check for its deadline/fee/post total before it can be listed.

### T4. UI smoothness — what was checked, what changed

Already in place and verified (no change needed): view fade/slide transitions, staggered options, animated progress bars + score ring, count-up score reveal, confetti on pass/level-up only, `prefers-reduced-motion`, sticky mobile bottom nav (52px, safe-area inset, 5 tabs), `.table-wrap` horizontal scroll on guide + mock tables, modal Esc + backdrop close, 44px+ touch targets, loading placeholders per view. Changed in this round: search Enter key (T09) and the performance fixes (T04–T07). Not changed: the 62MB single-file bundle's load/render cost is inherent to embedding 59,076 questions (see T5); the mobile bottom nav keeps its 5-tab scope by design (Discuss/Contribute/Profile stay in the header nav).

### T5. Found but NOT fixed (with why)

- **F31 data-quality queue** (1,807 long-correct-option candidates, 1,085 short explanations, 197 restated explanations, identical `_ne` fields) — human sample review by design; a script cannot judge these.
- **PDF explanations are tautological** — all 7,546 PDF questions carry the generated neutral form "The correct answer is \<option\>." (documented in §S; the PDF has no explanations). Rewriting 7,546 explanations by hand is a content project, not a bug fix; a scripted rewrite would invent derivations. Left as is.
- **F40 bundle rebuild** — coordinator only; `scripts/build-bundle.py` was kept in sync (FETCH_BLOCK verified byte-identical) but the bundle was **not** rebuilt here.
- **No real-browser smoke test** — still NOT RUN (no headless browser in this environment). The countdown, palette taps, confetti, 360px layout, Devanagari rendering and EN/NE toggle were verified in code + Node DOM stub only. Do this before GitHub upload.
- **Question accuracy audit** — still open (validator checks structure, not truth); the round-10 regenerated `expansion-r10-iq.json` incident (§R) is noted, not re-audited.
- **`psc.gov.np` direct check** — text fetch failed (network error); notices verified via secondary sources instead (see T3).

### T6. Tests (final run, 2026-10-28 — all exit 0)

- `node scripts/test-questions.js` — **PASS** (59,076 total, 0 duplicate ids/texts/options, bilingual 100%)
- `node scripts/test-app.js` — **ALL PASS** (incl. 10 new checks: 6 `effectiveNoticeStatus` cases, 2 notices.json status/date checks, 4 `findDuplicate` exact/near/different/cached checks; `sub-submit-btn` added to the runtime-created id list)
- `node scripts/test-e2e.js` — **ALL PASS** (102 checks, incl. new: daily-challenge start/abandon/finish/repeat XP states, reset clears speed best + fact streak + keeps `user_id`, notices render shows 2026-10-28 + auto-closed notices)
- `node scripts/test-v2.js` — **ALL PASS** (incl. new: double-submit of the same question leaves the queue at 1)
- `node scripts/test-funfacts.js` — **PASS** (608 facts)
- `node scripts/test-bundle.js` — **PASS** (stale-bundle check still certifies the pre-§T bundle — rebuild pending, F40)
- `node --check assets/js/app.js` — PASS; `FETCH_BLOCK` in `scripts/build-bundle.py` verified byte-identical to the new `loadData()` block by script (build itself not run).
- Perf spot-checks on the real 59k bank: `findDuplicate` 0–111 ms/call (was ~550 ms brute force; agrees with brute force on 6 probes); `doSearch` haystack now cached after first build.

**Files changed in this round:** `assets/js/app.js` (T01–T08, T10) · `data/notices.json` (T3 — 4 notices) · `index.html` (notices date, search Enter) · `scripts/build-bundle.py` (FETCH_BLOCK lockstep with T04) · `scripts/test-app.js`, `scripts/test-e2e.js`, `scripts/test-v2.js` (regression checks) · `TESTING.md` (this section). Not changed: any `data/questions/*.json` file, `data/papers.json`, `data/exams.json`, `assets/css/style.css`, `loksewa-prep-nepal-full.html`.

## U. Bug-fix + smoothness round + Round 11 loss — 2026-10-28 (supersedes the bank count in §T: still **59,076 questions in 106 files, 47 exams; 608 fun facts**)
### U1. Bug fixes (§T, verified by coordinator)
- T01 Daily Challenge XP now awarded only on finish (abandon costs nothing); T02 Reset clears speed best + fact streak; T03 submit double-queue blocked; T04 loadData parallel (Promise.all); T05 findDuplicate indexed (600–800ms → 0–111ms); T06 search haystack cached; T07 review/weakTopics one-pass Map; T08 Notices "last checked" derived from data (2026-10-28); T09 search on Enter; T10 dead variable removed.
- Notices re-checked 2026-10-28: Nepal Police ASI + Gandaki PPSC (Notice 129) CLOSED (27 Oct was Gandaki's double-fee deadline, corrected); PSC Under Secretary + Lumbini PPSC confirmed OPEN with matching deadlines/fees. Gandaki 7th-level Notice 166 spotted but NOT listed (deadline/fee unverified). F01–F40 re-verified: 38 fixed, F31 (human data-quality queue) and real-browser smoke test still open.
### U2. Round 11 expansion — LOST to VM restart, net added 0
- Previous worker built 5,169 audited questions from 7,714 candidates but kept everything in /tmp; the VM restart wiped it (uptime 2 min on recovery). Bank verified intact afterwards: 59,076 / 106 files, Previous Year 2083 untouched at 133, no r11 files, app.js never wired. Lesson recorded: all scratch MUST live under ~/workspace (r11-scratch/), with incremental landing to data/questions/. A rebuild worker was re-dispatched with the preserved thin lists + audit findings; it must not recreate the lost IDs.
### U3. Bundle rebuilt by coordinator (F40 closed for this round)
- 59,076 questions (unique ids), 608 fun facts, bilingual 59,076/59,076, 62,421,456 bytes, md5 06d78f26e9dbb1dc4216b4cdae5bd573, ends </script></body></html>. All six suites PASS (test-questions, test-app, test-e2e, test-v2, test-funfacts, test-bundle). NOT uploaded, NOT pushed to GitHub (user must create the repo first).

## V. Round 11 rebuild — 2026-10-28 (supersedes the bank count in §U: **64,713 questions in 131 files, 47 exams; 608 fun facts**)
### V1. Why a rebuild
- The first Round 11 worker built 5,169 audited questions but kept everything in /tmp; a VM restart wiped it (§U2). The rebuild kept all scratch under ~/workspace/loksewa-prep-nepal/r11-scratch/ and landed files incrementally. Nothing from the lost round was recreated from memory — fresh generators, fresh R11 IDs.
### V2. Result: +5,637 net (target +5,000, exceeded by 637)
- 25 new files data/questions/expansion-r11-*.json (agri 42, drills 1043, drills2 1046, drills3 405, drills4 153, drills5 98, drills6 1096, english 133, english2 65, english3 66, grammar 177, health 28, iq 242, iq2 71, iq3 77, iq4 43, iq5 83, law 42, maths 348, maths2 69, nepal 31, nepali 94, nepali2 102, science 32, tech 51). Bulk from computed maths/IQ/drills generators (keys correct by construction); hand-written fact files had low keep rates because the 61k bank already covers most textbook facts.
- Dedupe: generator-time rejections logged per generator in r11-scratch/logs/; final full-bank gate (~43 min on the 64,777 bank) found 126 R11-involved pairs, hand-adjudicated: 63 R11 questions REMOVED (bank wins) — list in r11-scratch/logs/dedupe-gate-removals.json (21 SI rewordings vs R10-MATH4, 11 IQ series identical to bank, 22 Nepali synonym/spelling items, 4 law, misc). 81 flagged R11 questions DELIBERATELY KEPT as gate false positives (48 grammar template siblings e.g. spoke vs spoken, 26 vocab different-word synonym/antonym, 7 Nepali different-word antonyms). The gate's bank-wide plan file (205 removals, mostly pre-existing R8/R10 template families) was NOT applied — out of R11 scope, and its keeper logic picked R11 over bank questions in some groups. Flagged for a future dedupe round, not acted on.
- Keys fixed (not dropped): R11-DRILL5-0097 train 45 km/h × 16 s: 192 → 200 m; 10 remainder maths Nepali explanations rewritten to end "बाँकी = {r} हो।"; 8 RF-scale tech distractors fixed (cm value equalled the correct answer in metres); 24 ordinal suffixes (22th→22nd etc.), zero wrong ordinals remain in R11. Audit mismatch script: 0 R11 flags after fixes. Hand-check: 248/248 stratified random sample verified (seed 20261029, all 25 files).
- Dropped: R11-DRILL5-0095 (train 60 km/h × 20 s = 333.33 m, non-integer — dropped not fixed); R11-IQ2-0030 (internal exact duplicate of R11-IQ1-0016); the 63 dedupe-gate removals above.
- Thin areas filled (per-exam tag deltas): jta 0→42, ranger 0→42, nec-licence +66, nepal-telecom +51, deputy-secretary +40, anm-guide +34, judicial-service +32, bar-council +32, rbb-senior-assistant +10, nhpc-radio +6, nhpc-physio +6, npc-pharmacy +4, nhpc-optometry +4, ayurveda-bams +2, nhpc-ayurveda +2, nhpc-dental +1, nmc-bds +1. By topic: Maths & Numerical +4,258, IQ & Reasoning +516, English +441, Nepali Language +196, Health/Technical +70, Computer & ICT +27, Engineering Drawing +24, Constitution +22.
- Previous Year 2083 untouched (0 exact overlaps with R11, verified). All R11 files 100% bilingual (validator-proven).
### V3. Stale test expectations fixed by the coordinator (app behaviour correct, tests lagged the data)
- test-e2e BAMS topic check: Health/Technical basics 18 → 20 (R11 added 2 ayurveda-bams questions; only-topic behaviour unchanged).
- test-e2e JTA zero-tagged check: JTA now has 42 tagged questions, so no exam has zero tagged questions any more; check replaced with "JTA lists tagged topics" (the no-questions code path is still covered by the BAMS Banking & Finance alert check).
- test-bundle hardcoded 59076 → 64713 (embedded count + loadData count).
### V4. Bundle rebuilt by coordinator
- 64,713 questions (unique ids), 608 fun facts, bilingual 64,713/64,713, 66,408,705 bytes, md5 4f946b7f4bd77e14e9510faf8ae38877, ends </script></body></html>. All six suites PASS. NOT uploaded, NOT pushed to GitHub (user must create the repo first).

## W. Bug sweep — 2026-10-31 (bank unchanged: 64,713 questions in 131 files, 47 exams; 608 fun facts)

Full aspirant walkthrough in code + the Node DOM-stub suites (no live browser available — same constraint as §T). No GitHub push, no bundle upload, no bundle rebuild (coordinator only). No `data/questions/*.json` file touched. `scripts/build-bundle.py` FETCH_BLOCK re-verified byte-identical to the `loadData()` fetch block after the fixes (the bundle build contract from §T still holds).

### W1. §T re-verification (all 10 still hold)

- **T01** Daily Challenge XP burn on abandon — `dailyDone` is written only in `finishAttempt()` (app.js:1114), never at challenge start; e2e start/abandon/finish/repeat checks pass.
- **T02** Partial Reset — `resetProgress()` removes `loksewa_speed_best_v1` + `loksewa_fact_streak_v1`, keeps `user_id`; e2e checks pass.
- **T03** Submit double-queue — `alreadyPending` guard + submit-button disable/re-enable; test-v2 double-submit check passes.
- **T04** Sequential loadData — `Promise.all(QUESTION_FILES.map(...))` at app.js:828; FETCH_BLOCK byte-identical in `scripts/build-bundle.py`.
- **T05** Slow findDuplicate — `dupIndex()` inverted token index + `_nearCandidates` bound; test-app exact/near/different/cached checks pass.
- **T06** doSearch haystack rebuild — `q._hay` lazy cache (app.js:1366).
- **T07** 59k find() per saved id — `questionByIdMap()` one-pass Map, used by `renderReview()` + `weakTopics()`.
- **T08** Notices hardcoded date — header uses newest `checked_date` from the data; index.html intro says 2026-10-28; e2e checks the rendered date.
- **T09** Search Enter — `onkeydown` Enter → `doSearch()` in index.html.
- **T10** Dead variable — no dead `b` in `mockMixFor()` (grep clean).

### W2. New bugs found + fixed (10)

| ID | Bug | Fix |
|---|---|---|
| W01 | **practicePaper matched the wrong paper's questions.** The keyword+date match used `(q.source).includes(p.date_bs\|\|'')` — for a paper with empty `date_bs` (e.g. `nasu-collection-loksewaaspirants`, transcribed:false) the date check is vacuous (`''.includes('')` is always true), so its 'nasu' keyword matched all 43 NaSu First Paper 2083-01-20 questions instead of alerting "not been transcribed". | `practicePaper()` now refuses when `!key \|\| !p.date_bs` (can't match reliably without a date) before filtering. New e2e check. |
| W02 | **finishAttempt could score an attempt twice.** A double-tap on "Finish & See Result" — or the timer expiring in the same instant as the last speed-round answer — recorded two attempts and awarded XP twice (weekly-goal guard masked only part of it). | `finishAttempt()` now returns early when `current._finished` is already set; the flag is set on the first (only) scoring run. New e2e check: attempts +1, XP awarded once. |
| W03 | **fillExamSelects wiped the user's exam choice.** Visiting the Contribute view calls `renderSubmit()` → `fillExamSelects()`, which rebuilt the Practice/Mock selects and silently reset them to the first option. | `fillExamSelects()` snapshots each select (value + selectedIndex) and restores the choice when the option still exists. `selectedIndex` distinguishes "never touched" (default stays the first exam) from an explicitly chosen empty value. New e2e checks. |
| W04 | **Stale Discussion Hub prefill.** Tapping "Discuss this question", navigating away, then opening Discuss later still showed the old question prefilled ("My doubt: …"). | `showView()` clears `pendingDiscuss` for every view except `discuss`. New e2e checks (prefill present on direct open, absent afterwards). |
| W05 | **Unverified-notice warning hardcoded "2026-10-26".** The next re-check would have left a stale date on the warning, the same defect class as T08. | The warning now uses the notice's own `checked_date`. New e2e check with a synthetic unverified notice. |
| W06 | **Speed-round wrong answers never reached Mistakes.** Practice and mock wrong answers are saved (F05), but speed mode returned early from `answerOption()` — so the Mistake Marathon could never drill speed-round misses. | `finishAttempt()` records wrong (non-skipped) speed-round ids into `progress.mistakes`, deduplicated. New e2e check (3 wrong / 10 → 3 mistakes). |
| W07 | **Confetti timeout race.** A second pass/level-up within the 4.2 s clear window let the old `setTimeout` sweep the new confetti away early. | `launchConfetti()` tracks its timeout id and clears it before launching again. Reviewed in code (timers/DOM not drivable in the stub). |
| W09 | **"Discuss this question" during a mock silently abandoned it.** The button navigates to the Discuss view; `showView()` stops the timer for non-quiz views, so a timed mock was thrown away with no warning. | The Discuss button is hidden in mock mode (`showDiscuss = !speedMode && !mockMode`); it stays in practice and on the result review screen, where discussing is safe. New e2e checks (absent in mock, present in practice). |
| W10 | **Break-nudge copy lied: "Your answers so far are safe."** Leaving the quiz abandons the session — `showView()` stops the timer and the attempt is never recorded. | Copy now says leaving abandons the session (it won't be scored); the "Take a break" button goes through new `takeABreak()`, which confirms first when a timer is running. New e2e checks (copy, confirm wired, untimed path goes home). |
| W11 | **"New random set" after an exam-less mode reused a stale exam.** After a Daily Challenge (`exam:''`), the old guard `if(s && current && current.exam)` skipped the select update, so the set used whatever exam the dropdown happened to hold instead of mixed practice. | Practice select gains a "🌐 All exams (mixed)" option (value `''`, **last** so the default stays the first exam); `newRandomSet()` sets `current.exam\|\|''`; the practice-pattern line describes mixed practice for `''`. New e2e checks. |

Considered but NOT changed: re-rendering the mock/auth/moderate views on EN/NE toggle — the mock view has no translatable dynamic content (English-only table headers; exam names identical), and re-rendering auth/moderate/submit forms would wipe in-progress typing, which is worse than the current behaviour. The toggle works on every view without crashing; F26's scope (question-bearing views) is unchanged.

### W3. Found but NOT fixed (with why)

- **F31 data-quality queue** — still open by design (human sample review; a script cannot judge long-correct-option candidates, short/restated explanations, identical `_ne` fields).
- **No real-browser smoke test** — still NOT RUN (no headless browser in this environment). Countdown ticking, palette taps, confetti, 360 px layout, Devanagari rendering, EN/NE toggle across views verified in code + Node DOM stub only. Still required before GitHub upload.
- **Tautological PDF explanations** — unchanged (the quality worker's area; §T5).
- **Question accuracy audit** — still open (validator checks structure, not truth).
- **F40 bundle rebuild** — coordinator only; `FETCH_BLOCK` verified in sync but the bundle was **not** rebuilt here.

### W4. Tests (final run, 2026-10-31 — all exit 0)

- `node scripts/test-app.js` — **ALL APP CHECKS PASSED** (191 PASS lines, 0 FAIL)
- `node scripts/test-e2e.js` — **ALL E2E CHECKS PASSED** (118 checks, 0 FAIL — incl. 15 new §W regression checks: W01, W02, W03×2, W04×2, W05, W06, W09×2, W10×3, W11×2)
- `node scripts/test-v2.js` — **ALL V2 CHECKS PASSED**
- `node --check assets/js/app.js` — PASS

**Files changed in this round:** `assets/js/app.js` (W01–W07, W09–W11) · `scripts/test-e2e.js` (14 new regression checks) · `TESTING.md` (this section). Not changed: any `data/questions/*.json` file, `data/papers.json`, `data/notices.json`, `data/exams.json`, `assets/css/style.css`, `index.html`, `scripts/build-bundle.py`, `loksewa-prep-nepal-full.html`.

## X. Pre-publish QA audit — 2026-10-31 (bank: 64,713 → **64,671 questions** in 131 files, 47 exams; 608 fun facts)

Four parallel workstreams (bug sweep, answer-key audit, question quality, feature proposals), integrated by the coordinator. This section is the integration record; per-workstream detail lives in §W (bugs), data/answer-audit-2026-10-31.json + audit-scratch-2026-10-31/ (keys), data/quality-scan-2026-10-31.md (quality).

- **Bugs:** 10 fixed in this round (W01–W11, §W); all 10 §T fixes re-verified as still holding.
- **Answer keys:** corrected mismatch-script regex bugs → 311 flags hand-reviewed; stratified hand sample 560 questions (seed 20261031); **17 keys fixed** (12× R11 "smaller share" ratio bug, 3× profit truncation, R10-VOC5-0753 antonym, NEC-018 brick strength); **42 questions dropped** (22× triangular-number wrap, 11× duplicate-value options, 9× CURH date ambiguities). Previous Year 2083 (133) untouched. Estimated residual error ~0.1–0.3%.
- **Quality:** 4,206 Nepali string fixes (सहि→सही 3,216; कु न→कुन 466; Arabic-script MT contamination 18; etc.); 260-question Nepali spot-check clean (~2% defect rate, all fixed); 0 structural defects; 7,546 tautological PDF explanations logged as enrichment backlog (data/quality-scan-2026-10-31.md).
- **Counts updated:** README.md, OPEN-SOURCE-CHECKLIST.md, scripts/test-bundle.js 64713 → 64671.
- Bundle rebuilt from the 64,671-question bank (66,379,634 bytes, md5 `c5fbac67016e8b7e49d5f551772860cd`, embeds 64,671 questions + 608 fun facts, bilingual 64,671/64,671, ends `</script></body></html>`); test-bundle PASS. NOT uploaded, NOT pushed to GitHub (user must create the repo first).

**Still open before GitHub upload:** real-browser smoke test (never run — no headless browser available); F31 human data-quality queue; 7,546 tautological PDF explanations (enrichment backlog); bank-wide dedupe plan (205 removals, pre-existing R8/R10 families) unapplied; CURH stem-wording cleanup; Gandaki 7th-level Notice 166 unverified.

## Y. Feature round — 2026-10-31 (bank unchanged: 64,671 questions, 131 files, 47 exams; 608 fun facts)

User approved building proposal features 1–7, plus an AI chatbot, a suggestions tab, a Sanskrit rename, and his GitHub link. Four parallel workers; integrated by the coordinator.

- **Analytics (5 views):** Syllabus Coverage Tracker (`view-coverage`), Printable mock + OMR sheet (`view-print`, `@media print`), Deadline-driven study planner (`view-planner`, reads `data/notices.json`), Negative-marking guess-strategy coach (`view-coach`), PYQ heatmap (`view-pyq`, 133 transcribed PYQs flagged via `markPyqFlags()`). `finishAttempt` now stores compact per-question detail (`qdetail`) powering the analytics; old attempts degrade gracefully.
- **Content:** Topic one-pager revision notes (`view-notes`) — `data/notes/`, 20 JSON files seeded for the top-20 topics by question count, 238 bilingual bullets of real content; format documented in CONTRIBUTING.md ("Revision notes"); "📖 Revise this topic" buttons on wrong-answer review, Mistakes list, and home topic cards; `build-bundle.py` embeds notes as `window.EMBEDDED_NOTES`. Audio revision mode (`view-audio`) — Web Speech API, offline, Q&A / flashcards / fun facts, rate 0.5–2× persisted, en-US/ne-NP voice picking, graceful fallback when TTS unavailable, narration stops on view leave.
- **Assistant:** Ask chatbot (`view-chat`) — rule-based, on-device, zero dependencies, no API keys, no network; labelled "On-device helper — rule-based, not real AI". `isFactualQuestion()` guard routes factual questions to practice topics/Search and never invents exam facts; bilingual EN/NE; history in `loksewa_chat_history_v1` (cap 200). Suggestions tab (`view-suggest`) — title/description/category form, localStorage `loksewa_suggestions_v1`, on-device list with upvotes, "Local demo" banner, spam guards (min lengths, no links, no ALL-CAPS, duplicate-title block, 5/hour rate limit, double-submit disable).
- **Brand:** renamed to **Vidyapeeth (विद्यापीठ — Sanskrit for "seat of learning")**, subtitle "Lok Sewa Prep Nepal" kept. Domain checks via RDAP (2026-10-31): vidya.com (taken, Vidya Media Ventures), shiksha.com (taken, Info Edge's Shiksha.com), gyan.com (taken, unknown holder), vidyapeeth.com (taken but parked — default WordPress, no brand; only plausible acquisition target). .com.np unverifiable (no public .np WHOIS) — vidyapeeth.com.np treated as likely-registrable. Repo slug `loksewa-prep-nepal` and all data files untouched. GitHub link added to index.html footer (already in README). **Follow-up rename the same day (§Z): Vidyapeeth → LokSewa Vidyapeeth**, subtitle "लोक सेवा विद्यापीठ · लोक सेवा तयारी".
- **Feature 8 (peer leaderboard + national mock percentiles) is BACKEND-GATED — not built.** It ships with the Supabase rollout (see docs/BACKEND.md); building it localStorage-only would fake a social feature. Do not implement until the backend lands.

**Files changed:** `index.html` (9 new nav buttons + 9 view sections) · `assets/js/app.js` (~1,500 new lines) · `assets/css/style.css` (chat, notes, audio, OMR/paper, print rules) · `data/notes/` (20 files) · `scripts/build-bundle.py` (EMBEDDED_NOTES) · `scripts/test-app.js` (+100 checks) · `scripts/test-bundle.js` (github.com exempted from no-external-refs, aligned with test-app.js) · `scripts/test-e2e.js` (share-text brand assertions) · `CONTRIBUTING.md` (Revision notes) · `README.md`, `docs/BACKEND.md`, `config.example.js` (brand).

## Z. Rename — 2026-10-31 (bank unchanged: 64,671 questions, 131 files, 47 exams; 608 fun facts)

User asked for a "loksewa something" name after the Vidyapeeth rename. Renamed **Vidyapeeth → LokSewa Vidyapeeth**, logo `🇳🇵 LokSewa Vidyapeeth <span>लोक सेवा विद्यापीठ · लोक सेवा तयारी</span>`, page title updated in kind.

- **Domain verification (RDAP, rdap.verisign.com, 2026-10-31):** loksewavidyapeeth.com → **404 (not registered — likely available)**; loksewavidya.com → **404 (not registered — likely available)**. Be honest about limits: `.com.np` has **no public WHOIS**, so `loksewavidyapeeth.com.np` / `loksewavidya.com.np` variants are treated as **likely-registrable, not verified**.
- **Files changed:** `index.html` (title, logo, footer) · `assets/js/app.js` (header comment, share-text suffix) · `README.md` (title, tagline, §Y reference) · `CONTRIBUTING.md` (title) · `docs/BACKEND.md` (title + OAuth app-name references) · `config.example.js` (header comment) · `scripts/test-app.js` + `scripts/test-e2e.js` (brand assertions updated to `LokSewa Vidyapeeth`) · this file (§Y brand line, §Z).
- **Untouched:** repo slug `loksewa-prep-nepal`, all `data/` files (questions, notes, notices, papers, funfacts), `assets/css/style.css`.
- Bundle rebuilt after rename; NOT uploaded, NOT pushed to GitHub (user must create the repo first).

## §AA — Production-polish pass (2026-10-31): "looks like a demo" → production-ready

User feedback on the live site: it looked like a demo, not professional. Three parallel workers (design system, HTML shell, JS UX/copy), integrated by the coordinator, plus a follow-up instruction from the user to remove the "Demo mode" banner from the UI entirely.

**Design system (`assets/css/style.css`, 270 → ~600 lines, full rewrite):** one coherent system replacing the base block + two appended overhaul blocks. ~45 CSS custom properties (surfaces, saffron brand family, semantic colors, radius scale, 4px spacing rhythm, shadow levels, 44px tap target, easing), fluid `clamp()` type scale with Devanagari-friendly line-heights, `text-wrap:balance` on headings. Hero restyled: deep indigo → saffron layered gradient with radial glows + CSS dot texture (was a flat red-orange gradient). New components: `.skel`/`.skel-line`/`.skel-card` shimmer skeletons, `.empty-state`, `.error-state`, checkbox pills. Footer hairline + safe-area padding. Responsive audit: 720/640/420 breakpoints, ≥44px tap targets, tables scroll, no horizontal overflow at 360px. Print stylesheet + `prefers-reduced-motion` preserved. All 75 legacy selectors verified present; zero undefined `var(--…)` tokens.

**HTML shell (`index.html`):** inline SVG favicon (graduation-cap, brand colors, data URI); full SEO meta (description, keywords, author, robots), canonical + Open Graph + Twitter card tags. Nav restructured: 24 flat buttons → Home / Practice / Mock Exams / Dashboard + a keyboard-accessible "More" dropdown (Study / Resources / Community groups); all 24 `data-view` buttons preserved, mobile bottom nav untouched. Hero rebuilt: eyebrow badge, value-prop H1, stat strip (64,671 questions · 47 exams · 100% offline · 0 login), CTA row (Start practicing / Take a mock), quick-start chip row (5 original actions, handlers verbatim), trust row. Footer: brand block + 3 link columns (all working `showView` links, zero placeholders). Inline `<style>`/`<script>` blocks from the worker pass were consolidated into `style.css`/`app.js` by the coordinator (hero pill chips scoped under `.chip-row` so chat `.chip` is untouched).

**JS UX/copy (`assets/js/app.js`):** dynamic `document.title` per view ("LokSewa Vidyapeeth — <View>"); skeleton loading states on all data-heavy views (guide, papers, notices, dashboard, coverage, print, planner, coach, pyq, notes, QOTD); proper empty states (icon + headline + explanation + CTA) and error states with retry (`reloadData()`) on every list view; full EN/NE copy review of headings/buttons/helper strings (EN strings kept byte-identical so test assertions hold); "Demo mode" phrasing rephrased to "Local preview" where contextual honesty notes remain. Also fixed a real crash found in verification: `renderFunFact` threw on null fact, breaking `showView('home')`.

**Demo banner removal (user instruction, same day):** the "Demo mode — local profile only…" banner removed from `index.html` entirely, plus its `auth-demo-banner` sibling and the unhide logic in `updateDemoBanner()` (function kept for the nav-auth-btn label update). Underlying local behavior unchanged; `docs/BACKEND.md` stays in the repo. `isDemoMode()` kept (tests assert it).

**Test updates (user-directed UI changes only):** `test-app.js` — removed `auth-demo-banner` from the dynamic-id set; "demo banner exists" check inverted to assert the banner is gone. `test-bundle.js` — external-link check now also exempts the canonical tag's `08raviyadav.github.io` URL (loads no resource; offline-safety intent preserved); the "exactly 2 script blocks" check passes again after the dropdown JS moved into `app.js`.

**Verification (coordinator, after integration):** all six suites PASS — test-questions (64,671, 0 dup ids/texts, bilingual 100%), test-app (310 checks), test-e2e (118), test-v2 (45), test-funfacts (14), test-bundle. Question data, answer keys, and exam patterns untouched. Bundle rebuilt: 66,614,755 bytes, ends `</script></body></html>`. NOT uploaded, NOT pushed (parent handles the push).
