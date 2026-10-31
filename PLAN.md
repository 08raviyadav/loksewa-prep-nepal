# Lok Sewa Prep Nepal — Plan

## What it is
Free, open-source, frontend-only exam preparation portal for Nepal government exams — an Indiabix-style practice site made for Nepal. No server, no login, no fees, no ads. Works offline after first load, from `file://` or GitHub Pages.

## Exams covered (42 entries in `data/exams.json`, 2026-10-26 merge)
| Exam | Prelim / General paper | Pass | Time |
|---|---|---|---|
| Kharidar (Level 4) | 50 MCQ × 2 = 100 (GK 30 + BOST 20) | 45 | 45 min |
| Nayab Subba (Level 5) | 50 MCQ × 2 = 100 (GK 30 + IQ 20) | 45 | 45 min |
| Section Officer (Gaz. 3rd) | 100 MCQ × 1 = 100 (GK 50 + Aptitude 30 + English 20) | 45 | 90 min |
| Foreign Service (Gaz. 3rd) | 100 MCQ × 1 = 100 (same prelim as Section Officer) | 45 | 90 min |
| TSC General — Primary / Lower Secondary / Secondary | 50 MCQ × 2 = 100 | 50 | 60 min |
| TSC Teaching Licence | 50 MCQ × 2 = 100 | 50 | — (unverified, mock runs untimed) |
| NRB Assistant (2nd) | 50 MCQ × 2 = 100 (Mgmt/Acct 30, Econ/Banking 30, Maths 14, Computer 14, GK 12) | 40 | 45 min |
| NRB Assistant Director (Officer 3rd) | Pre-qualifying MCQ, 100 marks (Q count / time / pass **unverified** — portal shows 100×1/90 min/pass 45, flagged) | — | — |
| Sub-Engineer / Computer Operator / Nepal Telecom (Level 4/5) | 50 MCQ × 2 = 100 | 40 | 45 min |
| NMC Licence MBBS (MCQ part) | 130 MCQ × 1 (+ 10 CSQ × 5 in the real paper = 180) | 90/180 (50%) | 180 min |
| NMC Licence BDS | 180 MCQ × 1 | 90 (50%) | 180 min |
| NNC Nursing Licence (NLEN) / Midwifery (NLEM) | 150 MCQ × 1, no negative marking | 75 (50%) | 150 min |
| NHPC licences (HA, Lab, Radiography, Physio, Public Health, Optometry) | 100 MCQ × 1, no negative marking* | 50 | 90 min |
| NPC Pharmacy Licence BPharm | 150 MCQ × 1, no negative marking | 75 (50%) | 150 min |
| Staff Nurse (PSC, 5th Level) | 50 MCQ × 2 = 100 (GA & Public Mgmt 20 + Job Knowledge 30) | 40 | 45 min |
| RBB/NBL/ADBL, Police, Army, Health, Engineering | Covered via shared topics + exam tags; patterns in Exam Guide | — | — |

\* NHPC negative marking is not stated in any source found — the portal deducts nothing and flags it. NHPC time is 90 min per the common format; BSc MIT / B.Optom syllabi say 2 hrs (conflict flagged).
**Guide-only (13, `prelim: null`, no mock):** Deputy/Joint Secretary, JTA, Ranger, Judicial Service, PSC Service Groups, RBB Assistant Level 4 (no MCQ prelim in the 2082-83 unified exam), RBB Senior Assistant, Provincial PSCs, NEA (Section A 50×1, no stated pass mark), NHPC Dental Hygiene, NHPC Ayurveda, ANM, Ayurveda (NAMC/BAMS). The mock dropdown lists only the 29 prelim exams; `startMock()` refuses guide-only exams; the Exam Guide shows them without a Start-mock button.

Common rule on PSC prelims: **20% negative marking** — −0.4 per wrong 2-mark Q, −0.2 per wrong 1-mark Q, 0 for skipped. Prelim marks are qualifying only. Licence exams apply their own rule per exam (see table — NNC/NPC confirmed none; NMC/NHPC none applied, unverified; TSC Licence none applied, unverified).

## Topics (16) — 6,846 questions
Nepal History (322), Nepal Geography (316), Constitution & Governance (504), Economy & Development (246), Culture & Society (272), Current Affairs (264), Science & Tech (265), IQ & Reasoning (460), Maths & Numerical (460), English (412), Nepali Language (359), Computer & ICT (338), Office Management & Public Service (316), Banking & Finance (316), Education & Pedagogy (463), Health/Technical basics (1,533). Thinnest now: Economy & Development (246), Current Affairs (264), Science & Tech (265) — English and Nepali Language were fixed by the v2 expansion (320 + 299).

## Question types
MCQ single-correct (4 options) — the only type in prelims. Numerical, reasoning, English/Nepali grammar, GK, current affairs. Subjective/theory papers are covered in the Exam Guide (structure + how to prepare), not as auto-marked MCQs — the portal is honest about that limit.

## What aspirants need (and how we meet it)
- **Timed mocks that feel like the real exam** — exact Q count, time, negative marking, cutoff, OMR-style palette, auto-submit.
- **Topic practice that is not boring** — randomised questions AND randomised option order every attempt, instant feedback + explanation, Daily Challenge, Quick Quiz, streaks/XP/badges/levels, flashcards.
- **Know how much they are scoring** — result screen with score, %, correct/wrong/skipped, marks after negative marking, pass/fail vs the real cutoff, time per question, best/worst topics, wrong-only retry.
- **Revision** — bookmarks, mistakes review, weak-topic analysis on the dashboard.
- **Free, private, offline** — progress in localStorage only; nothing leaves the device.

## Architecture
- Vanilla HTML/CSS/JS, zero build step, zero dependencies, zero CDN.
- `index.html` — single-page app (views: Home, Practice, Mock Exams, Daily Challenge, Flashcards, Bookmarks & Mistakes, Dashboard, Exam Guide, Search). Home carries a "Trending — what students are searching most" section (8 topic cards → `startPracticeTopic()`; demand-proxy ranking, not Google Trends data).
- `assets/css/style.css` — mobile-first responsive, dark/light toggle, accessible (focus states, labels, contrast).
- `assets/js/app.js` — all logic in one readable file: data loading (22 question files, `QUESTION_FILES`), shuffle (Fisher–Yates, Math.random + timestamp seed), scoring, timer, localStorage progress, charts on plain canvas. Language: EN/NE toggle (`#lang-toggle`, `loksewa_lang`) switches question/option/explanation text to the `_ne` fields (100% bilingual bank) with English fallback. Negative marking is per-exam (`mockNegRate()`): 20% on PSC prelims, 0 where the exam has none or where it is unverified. `startMock()` refuses guide-only exams (`prelim: null`), runs untimed when `timeMin` is null, and warns when the tagged pool is smaller than the paper (thin-bank fallback to the general bank). `renderGuide()` renders guide-only exams without a prelim row or Start-mock button. `finishAttempt()` / `cutoffFor()` / `renderResult()` are null-prelim safe. **v2:** demo sign-in + profile (cloud-ready progress shape `{user_id, email, name, xp, level, streak, attempts[], bookmarks[], mistakes[]}`, old progress migrated in place), Discussion Hub (seeded threads, post/reply/upvote/report, `loksewa_discussions_v1`), Submit-a-Question with duplicate detection (exact + token-Jaccard ≥ 0.8), spam heuristics and a 5/hour rate limit (`loksewa_submissions_v1`), Maintainer Review with approve/reject/edit (`loksewa_community_approved_v1` loads into the bank at startup with a "Community" badge), report-wrong-question (`loksewa_reports_v1`), and `loadConfig()` reading `config.js` (gitignored) for Supabase settings — demo mode with a visible banner when it is absent. Backend plan in `docs/BACKEND.md`.
- `data/questions/*.json` — question bank, 6,846 MCQs in 22 files, schema in CONTRIBUTING.md. Loaded with `fetch()` (works on http server / GitHub Pages; falls back to an embedded note when opened via `file://` in browsers that block fetch — see README). `data/questions/community-approved.json` holds maintainer-approved community questions (starts empty; the live bank also loads approved questions from localStorage in demo mode).
- `data/exams.json` — 42 exam patterns, eligibility, syllabus weightage (from research). 29 with MCQ prelim, 13 guide-only.
- `scripts/test-questions.js`, `scripts/test-app.js`, `scripts/test-e2e.js`, `scripts/test-v2.js` — Node, no deps.
- Docs: README, LICENSE (MIT, Ravi Yadav), CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, .github templates. Research notes kept in `data/`: `EXAM-AUDIT.md`, `GAP-AUDIT.md`, `LICENSE-RESEARCH.md`, `TRENDS.md`, `SOURCES.md`. Backend plan in `docs/BACKEND.md`; `config.example.js` is the config template (`config.js` itself is gitignored and never committed).

## Scoring maths (verified in tests)
score = Σ correct×marks − Σ wrong×marks×rate. Skipped = 0. Rounded to 1 decimal. Pass = score ≥ cutoff for the chosen exam. Rate is 0.20 on PSC prelims/practice (checkbox), 0 on no-negative and unverified-negative exams (NNC, NPC, NMC, NHPC, TSC Licence). Pass/fail is judged on percentage vs the exam's cutoff percentage.

## Caveats (unverified — see README Sources)
Official PSC syllabus PDFs (psc.gov.np) were not read directly; patterns come from secondary reproductions (Edusanjal etc.). Flagged: Section Officer main pass 40 vs 45, final-stage total 70 vs 60, TSC merit weightage, Police ASI age/education by stream, health age limits. New 2026-10-26 flags: RBB prelim removed (no MCQ prelim in the 2082-83 unified exam); NRB Officer pattern unverified beyond "100 marks"; NMC/NHPC negative marking unstated; NHPC time conflict (90 vs 120 min for BSc MIT / B.Optom); NEA Section A is 50×1 with no stated pass mark; Computer Operator Paper II 2h15m vs 3h15m; NLEM practical 50 vs 40 marks. Verify against the vacancy notice before relying on a figure.

## Roadmap update (2026-10-26 merge)
- Done: question bank 1,129 → 6,227; exams 12 → 42 (29 mocks + 13 guide-only); EN/NE question toggle (100% bilingual); Trending section; RBB correction; per-exam negative marking; thin-bank mock warning.
- **v2 (done 2026-10-26):** bank 6,227 → **6,846** (+320 English `expansion-english-v2.json`, +299 Nepali `expansion-nepali-v2.json` — the two thinnest topics, fixed); demo sign-in + profile; Discussion Hub (9 seeded threads); Submit-a-Question with duplicate/spam/rate-limit checks; Maintainer Review queue (approve/reject/edit, public log, trusted-contributor rule); report-wrong-question; community-approved questions with a "Community" badge; Supabase backend plan in `docs/BACKEND.md` (schema + RLS + Google OAuth + setup steps). **Instant live + no spam cannot both be true** — submissions go through automatic checks + maintainer review; first-time submissions never go live instantly.
- Next: fill thin banks (NHPC disciplines 30 → 100 tagged each; 7 prelim exams with 0 tagged questions; Economy & Development 246 / Current Affairs 264 / Science & Tech 265 are now the thinnest topics); verify NHPC Dental/Ayurveda syllabuses; add MECEE-BL / NEC licence / Bar Council / IOE / CSIT (verified patterns exist in `data/GAP-AUDIT.md`, no questions yet); human accuracy audit of a question sample; real-browser smoke test (still not run — see TESTING.md §H); **Supabase setup on the user's computer** (docs/BACKEND.md §5) to turn on real Gmail login, synced progress, live discussions and server-side moderation.
