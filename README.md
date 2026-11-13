# 🇳🇵 Outrank — Lok Sewa Exam Preparation · लोक सेवा परीक्षा तयारी

**Outrank — free, open-source, offline-first Lok Sewa exam preparation for Nepal government exams — like Indiabix, made for Nepal.**

Practice for **Lok Sewa Aayog (PSC)** — Kharidar, Nayab Subba, Section Officer — **Shikshak Sewa Aayog (TSC)**, **Nepal Rastra Bank**, **RBB / NBL / ADBL**, **Nepal Police / APF**, **Nepal Army**, **Health** and **Engineering** services, plus **licence exams** — NMC (MBBS/BDS), NNC Nursing & Midwifery, NHPC (HA, Lab, Radiography, Physiotherapy, Public Health, Optometry, Dental, Ayurveda), NPC Pharmacy, Staff Nurse (PSC) and the NAMC Ayurveda / ANM guides — plus **entrance exams** MECEE-BL, NEC licence, Nepal Bar Council, BSc CSIT and IOE (guide-only, mixed-mark paper). **64,671 MCQs across 47 exams** (33 with a mock — 32 timed, TSC Licence untimed — and 14 guide-only — see below). No login required, no fees, no ads, no tracking. Your progress never leaves your device — unless you choose to sign in (demo mode for now; real Google sign-in via Supabase is planned — see [docs/BACKEND.md](docs/BACKEND.md)).

> Maintainer: **Ravi Yadav ([@08raviyadav](https://github.com/08raviyadav))** — he reviews and accepts or rejects every pull request. Nothing is auto-merged.
>
> **© 2026 Ravi Yadav — credit required.** This project is MIT-licensed (see [LICENSE](LICENSE) and [NOTICE](NOTICE)): anyone who uses, copies, forks or redistributes it must keep the copyright notice **and** give visible credit — *"Created by Ravi Yadav (https://github.com/08raviyadav)"* — in the footer, About page, or README of the copy.
>
> 🌐 **Live demo: coming after first push** — enable GitHub Pages on the `main` branch, root folder (`/`), and the site will be live at <https://08raviyadav.github.io/loksewa-prep-nepal/>.

## ✨ What you get

- **Practice section (the core)** — pick exam, topic(s), difficulty and count (5 / 10 / 20 / 50). Timer on/off, negative marking on/off.
  - **Randomised every time:** question order AND option order are shuffled on every attempt (Fisher–Yates, `Math.random` + timestamp seed). Hit **🔀 New random set** for a fresh set — no two attempts are the same.
  - Instant feedback per question + explanation, skip, bookmark, report a wrong question.
  - **Result screen that tells you how much you are scoring:** score, %, correct / wrong / skipped, marks after 20% negative marking, **pass/fail vs the real cutoff**, time taken, time per question, best/worst topics, wrong-answer review, **retry wrong only**.
- **Mock exams** — full-length, timed, exactly like the real prelim, with an OMR-style question palette and auto-submit on timeout:
  | Mock | Questions | Time | Marks/Q | Pass |
  |---|---|---|---|---|
  | Kharidar | 50 | 45 min | 2 | 45 |
  | Nayab Subba | 50 | 45 min | 2 | 45 |
  | Section Officer | 100 | 90 min | 1 | 45 |
  | TSC General (Primary / Lower Secondary / Secondary) | 50 | 60 min | 2 | 50 |
  | TSC Teaching Licence | 50 | — (time unverified, untimed) | 2 | 50 |
  | NRB Assistant | 50 | 45 min | 2 | 40 |
  | Foreign Service | 100 | 90 min | 1 | 45 |
  | Sub-Engineer / Computer Operator / Nepal Telecom | 50 | 45 min | 2 | 40 |
  | NMC Licence (MBBS) — MCQ part only | 130 | 180 min | 1 | 90/180 (50%) |
  | NMC Licence (BDS) | 180 | 180 min | 1 | 90 (50%) |
  | Nursing Licence (NLEN) / Midwifery (NLEM) | 150 | 150 min | 1 | 75 (50%), no negative marking |
  | NHPC licences (HA, Lab, Radiography, Physio, Public Health, Optometry) | 100 | 90 min | 1 | 50, no negative marking* |
  | Pharmacy Licence BPharm (NPC) | 150 | 150 min | 1 | 75 (50%), no negative marking |
  | Staff Nurse (PSC) | 50 | 45 min | 2 | 40 |
  | MECEE-BL (medical entrance) | 200 | 180 min | 1 | 100 (50th percentile — portal judges at 50% as a proxy) |
  | NEC Licence | 100 | 120 min | 1 | 50, no negative marking |
  | Bar Council Paper 1 | 100 | 90 min | 1 | 50, no negative marking |
  | BSc CSIT Entrance | 100 | 120 min | 1 | 35, no negative marking |
  \* NHPC negative marking is **not stated** in any source found — the portal applies none and says so on the guide card; verify against the NHPC notice. NHPC time is 90 min per the NHPC common format; the BSc MIT and B.Optom syllabi state 2 hours (conflict flagged on their guide cards). The NMC mock covers only the 130 MCQs — the real paper adds 10 Clinical Scenario Questions × 5 marks (total 180, pass 90).
  **Guide-only exams (no mock):** Deputy/Joint Secretary, JTA, Ranger, Judicial Service, PSC Service Groups, RBB Assistant Level 4 (the 2082-83 unified exam has **no MCQ prelim** — two subjective papers + interview; the mock this portal used to show was wrong and has been removed), RBB Senior Assistant, Provincial PSCs, NEA (Section A is 50×1 with no stated pass mark — no honest cutoff exists), NHPC Dental Hygiene, NHPC Ayurveda, ANM, Ayurveda (NAMC/BAMS), IOE Entrance (verified pattern: 100 MCQs, 140 marks — 60×1 + 40×2 — 2 hrs, −10%/wrong; guide-only because the mock engine assumes uniform marks per question). They appear in the Exam Guide with their verified pattern (or the reason no pattern exists) and never in the mock dropdown — a guide-only exam cannot start a mock.
  **Thin-bank warning:** mocks with fewer tagged questions than the paper needs draw from the general bank and the app **warns you when you start one** — it does not mirror the real paper yet. After the round-3 expansion the zero-tagged mocks are gone (NMC-BDS now has 180, Midwifery 150, Staff Nurse PSC 120); still thin: NHPC Dental (109) and Ayurveda (104) now cover their 100-question papers; CSIT (361) and IOE (389, guide-only) are well covered. See `TESTING.md` §H/§J/§L for the full list.
- **Daily Challenge** (10 random questions, changes daily), **Quick Quiz** (5), **Flashcards** (revision mode).
- **Fun Facts — Did you know?** — 608 verified fun facts (`data/funfacts.json`, EN + NE, with source), in 8 categories. A daily fact on Home, one after every 5th practice question (skippable, never in mocks), a Fun Facts tab with category filter + shuffle, and one on the result screen. Reading 10 facts earns the 🏅 Fact Explorer badge.
- **Study-fun / gamification** — XP, levels (animated level-up banner + confetti on pass/level-up), daily streak, badges (incl. 7-day streak, Century Day — 100 questions in a day, Perfect Mock, Weekly Champion), **Weekly Challenge** (pick a 35/70/100/140-question weekly goal), **Pomodoro focus timer** (25-min focus / 5-min break, +10 XP per completed block), **🎲 Surprise me** random mixed quiz, "Beat your best" personal-best line on every mock, and a "How to study without getting bored" tips card on Home.
- **Smooth, mobile-first UI** — fade/slide view transitions, staggered options, animated progress bars and score ring, count-up score reveal, sticky bottom nav on mobile (Home / Practice / Mock / Stats / Saved), touch targets ≥44px, persistent light/dark theme, "Question X of Y" + time-per-question, varied encouragement after answers, and a ☕ take-a-break nudge every 20 questions. No external fonts/CDN, works fully offline.
- **Dashboard** — XP, levels, daily streak, badges, score history (plain-canvas chart), weak-topic analysis, recent attempts.
- **Bookmarks & Mistakes** — wrong answers are saved automatically for revision.
- **Exam Guide** — one page per exam: pattern table, eligibility, age, syllabus weightage.
- **Search** — search any question, topic or option text.
- **Bilingual questions (EN / NE)** — every one of the 64,671 questions has a Nepali translation (question, all 4 options, explanation). Tap **EN · English / NE · नेपाली** in the header to switch; the choice is saved on your device. Where a Nepali field is missing on a question, the English text is shown instead.
- **Sign In / Profile (demo mode)** — a Google-style sign-in button creates a local profile (display name + Gmail address, validated) stored only on this device. Profile page shows XP, level, streak, attempts, accuracy and weak topics. Clearly labelled "Demo mode — local profile only"; real Google sign-in needs Supabase (see [docs/BACKEND.md](docs/BACKEND.md)).
- **Discussion Hub** — one seeded thread per exam (Kharidar, NaSu, Section Officer, TSC, NRB, NMC, NNC, Pharmacy) plus General doubts. Post a doubt, reply, upvote, report. Every question has a "💬 Discuss this question" link that opens the Hub pre-filled with that question. Local demo for now — posts stay on this device until the backend is connected.
- **Contribute — Submit a Question** — the exact JSON format first (copyable template), then a form with live validation, duplicate detection against the full bank (exact + near-duplicate, token-Jaccard ≥ 0.8), spam heuristics and a 5-per-hour rate limit. Submissions go to a **Maintainer Review** queue — approve (with edit-before-approve), reject with a reason, or download the approved set. Approved questions join the practice bank with a "Community" badge.

> ⚠️ **Instant live + no spam cannot both be true.** Submissions go through automatic checks (duplicate detection, spam heuristics, rate limit) **and** maintainer review. **First-time submissions never go live instantly** — Ravi Yadav approves or rejects every one. Contributors with 3+ approved questions and 0 rejections get faster review. The public moderation log (approved / rejected / pending) is shown on the Contribute page.
- **Analytics (added 2026-10-31)** — **Syllabus Coverage Tracker** (per-exam: topics practised vs untouched, accuracy vs estimated paper weight), **Printable mock papers with OMR sheet** (paper-exact prelim + bubble sheet + answer key, print stylesheet), **Deadline-driven study planner** (pick a target exam from Notices, daily plan that rebalances as the deadline nears), **Negative-marking guess-strategy coach** ("marks left on the table" from your skip/guess history), **PYQ heatmap** (the 133 transcribed real previous-year questions as ground truth vs bank coverage vs your practice).
- **Revision notes (added 2026-10-31)** — bilingual one-pager notes for the top-20 topics by question count (`data/notes/`, PR-contributable — see CONTRIBUTING.md "Revision notes"); "📖 Revise this topic" buttons on wrong-answer review, the Mistakes list and home topic cards.
- **Audio revision mode (added 2026-10-31)** — offline text-to-speech (Web Speech API) for Q&A, flashcards and fun facts; play/pause/next, 0.5–2× rate, en-US/ne-NP voices; graceful fallback when TTS is unavailable.
- **Ask chatbot (added 2026-10-31)** — on-device, rule-based helper (no API keys, no network): how to use the portal, exam finder, study tips, bilingual. It never invents exam facts — factual questions are routed to the relevant practice topic or Search.
- **Suggest a feature (added 2026-10-31)** — title/description/category form with upvotes, same local-demo safety posture as Submit a Question (nothing leaves your device until the backend lands).
- **Trending — what students are searching most** — 8 cards on the Home page (Constitution 2072, Current Affairs, most-asked GK, IQ & Reasoning, Kharidar Office Skills, NRB & Banking, Maths drills, TSC Teaching), each jumping straight into practice on that topic. This is a research-based ranking (researched 25–26 Oct 2026), **not** Google Trends data — Trends itself could not be verified (see `data/TRENDS.md` §5).
- Bilingual labels (English + नेपाली) where useful, dark/light theme, mobile-first responsive, accessible.

## 🧮 Scoring — exactly like PSC

Negative marking is **per exam**, not one global rule. PSC prelims deduct 20% per wrong answer (−0.4 on a 2-mark Q, −0.2 on a 1-mark Q). Licence exams with **no** negative marking (NNC Nursing/Midwifery, NPC Pharmacy — confirmed; NMC and NHPC — not stated in any source found, so the portal deducts nothing and says so) deduct **0**. The TSC Teaching Licence exam's negative marking is **unverified**, so its mock also deducts nothing and runs untimed (its time limit is unverified too). The result screen always states which rule was applied.

```
score = Σ correct × marks  −  Σ wrong × marks × 0.20
skipped = 0
```
A wrong 2-mark question costs **−0.4**; a wrong 1-mark question costs **−0.2**. Prelim marks are qualifying only in the real exam — the portal judges you against the prelim cutoff, not a made-up one. Pass/fail is judged on **percentage vs the cutoff percentage** (Kharidar/NaSu/Section Officer 45%, TSC 50%, NRB Assistant 40%), so a perfect 10-question practice set shows PASS — a short set can never reach the full paper's raw 45/100, and the portal does not pretend otherwise. On a full-length mock the percentage and the raw cutoff are the same thing.

## ▶️ Run locally

No build step, no dependencies, no install.

```bash
git clone https://github.com/08raviyadav/loksewa-prep-nepal.git
cd loksewa-prep-nepal
python3 -m http.server 8000
# open http://localhost:8000
```

> ⚠️ Don't just double-click `index.html`: browsers block `fetch()` of local JSON files from `file://`, so the question bank won't load. Use the server above (or any static host / GitHub Pages).
>
> **No-server alternative:** open `loksewa-prep-nepal-full.html` — the single-file bundle with the whole question bank embedded (built with `python3 scripts/build-bundle.py`). It works by double-clicking, straight from `file://`, and is the version to share on a phone or USB stick. Rebuild it after any question/data change so it stays in sync with the multi-file app.
>
> 🌐 **Live demo: coming after first push** — enable GitHub Pages on the `main` branch, root folder (`/`); the site will be live at <https://08raviyadav.github.io/loksewa-prep-nepal/>.

Deploy to GitHub Pages: Settings → Pages → Deploy from branch → `main` → `/ (root)`. That's it.

## 📁 Project structure

```
index.html                  Single-page app (all views)
loksewa-prep-nepal-full.html  Single-file bundle (whole bank embedded) — works from file://, rebuild with scripts/build-bundle.py
assets/css/style.css        Mobile-first, dark/light, no frameworks
assets/js/app.js            All logic: shuffle, scoring, timer, progress
data/exams.json             47 exam patterns (33 with MCQ prelim, 14 guide-only), eligibility, syllabus (from research)
data/papers.json            17 old (previous-year) papers — scanned, linked to source; 3 transcribed (133 real questions, see below)
data/notices.json           10 vacancy notices, last checked 2026-10-26 (2 open, 2 closing soon, 4 closed, 2 unverified)
data/questions/*.json       Question bank — 64,671 MCQs in 130 files (see table below) + `community-approved.json` (starts empty — approved community submissions land here)
data/questions/community-approved.json   Approved community submissions (starts empty; see CONTRIBUTING.md)
scripts/test-questions.js   Validates the question bank (node, no deps)
scripts/build-bundle.py     Rebuilds loksewa-prep-nepal-full.html from the multi-file app (python3, no deps)
scripts/test-app.js         Validates scoring, shuffle, HTML ids, mock specs
scripts/test-e2e.js         End-to-end quiz logic in a DOM stub
scripts/test-v2.js          Validates v2: sign-in, discussions, submissions, moderation, reports
docs/BACKEND.md             Backend plan: Supabase schema, RLS policies, Google OAuth, setup steps
config.example.js           Backend config template (copy to config.js — gitignored, never commit keys)
PLAN.md  TESTING.md         Plan + 100-item test checklist with real results
```

### Question bank — 59,076 MCQs (was 1,129; expanded overnight 2026-10-25/26, then de-duplicated; +619 in v2, 2026-10-26; +3,849 in round 3, 2026-10-26; +2,000 in round 4, 2026-10-26; +133 real previous-year questions, 2026-10-26; +2,259 in round 5, 2026-10-26; +3,113 in round 6, 2026-10-26, net of de-duplication; +918 in round 7, 2026-10-26, net of de-duplication; +1,082 in round 7b, 2026-10-26, net of de-duplication; −68 in answer-key audit, 2026-10-26; +2,000 in round 8 and +27,224 in the round 10 scale-up, 2026-10-26 (gross; −1,524 in the prior dedupe sweep and −1,417 in this integration); +5,115 in round 10 final integration, 2026-10-27 (dedupe −1,020 duplicates, −1 broken question removed, Constitution-article/mountain/Nepali-field/ordinal audit fixes, QUESTION_FILES +3 files that were unloadable, regenerated IQ file); +7,546 in PDF expansion, 2026-10-27 (10,000 user-supplied PDF questions; dedupe −2,453, verified-key drop −1 for PDF-0684 two-correct-options; explanations generated, not from PDF — see TESTING.md §S); +5,637 in round 11 rebuild, 2026-10-28 (dedupe-gate −63 R11 duplicates vs bank, keys fixed not dropped: R11-DRILL5-0097 train distance 192→200 m, 10 remainder Nepali explanations, 8 RF-scale distractors, 24 ordinal suffixes; dropped R11-DRILL5-0095 non-integer train distance + 1 internal duplicate; thin areas filled incl. JTA/ranger 0→42 — see TESTING.md §V)

| File | Qs | File | Qs |
|---|---|---|---|
| community-approved.json | 0 | constitution-governance-economy.json (original) | 215 |
| english-nepali-computer.json (original) | 207 | expansion-computer-office-banking.json | 751 |
| expansion-constitution-economy-current-science.json | 705 | expansion-core-hard.json (round 3 — hard IQ/Maths/Constitution/Education) | 566 |
| expansion-culture.json | 196 | expansion-current-hard.json (round 4 — hard Current Affairs/Science/Culture/Economy) | 450 |
| expansion-english-nepali-v3.json (round 3 — English + Nepali, hard) | 473 | expansion-english-v2.json (v2 — English) | 300 |
| expansion-entrance-licence.json (round 3 — MECEE/NEC/Bar/IOE/CSIT) | 493 | expansion-foreign-telecom.json (round 4 — Foreign Service + Nepal Telecom) | 240 |
| expansion-geography.json | 236 | expansion-hard-core-v2.json (round 4 — hard IQ/Maths/Constitution/Education) | 479 |
| expansion-health-technical-security.json | 309 | expansion-health-technical.json | 176 |
| expansion-history.json | 229 | expansion-iq-maths.json | 672 |
| expansion-law-csit-ioe.json (round 4 — Bar Council/CSIT/IOE) | 331 | expansion-nepali-v2.json (v2 — Nepali Language) | 284 |
| expansion-nhpc-law.json (round 4 — NHPC disciplines + Law) | 380 | expansion-pdf-01.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 |
| expansion-pdf-02.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 | expansion-pdf-03.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 |
| expansion-pdf-04.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 | expansion-pdf-05.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 |
| expansion-pdf-06.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 | expansion-pdf-07.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 |
| expansion-pdf-08.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 | expansion-pdf-09.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 |
| expansion-pdf-10.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 | expansion-pdf-11.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 |
| expansion-pdf-12.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 | expansion-pdf-13.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 |
| expansion-pdf-14.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 | expansion-pdf-15.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 500 |
| expansion-pdf-16.json (PDF expansion — 10,000 New Exam Questions (2082/83 BS)) | 46 | expansion-r10-current.json (round 10 — Current Affairs) | 54 |
| expansion-r10-drills.json (round 10 — Maths drills) | 1,526 | expansion-r10-drills2.json (round 10 — Maths drills) | 865 |
| expansion-r10-english.json (round 10 — English vocab/grammar) | 1,873 | expansion-r10-english2.json (round 10 — English vocab/grammar) | 1,203 |
| expansion-r10-english3.json (round 10 — English vocab/grammar) | 1,064 | expansion-r10-english4.json | 375 |
| expansion-r10-grammar.json (round 10 — English grammar) | 72 | expansion-r10-health.json (round 10 — Health basics) | 210 |
| expansion-r10-health2.json (round 10 — Health basics) | 89 | expansion-r10-iq.json (round 10 — IQ & Reasoning) | 2,524 |
| expansion-r10-iq2.json (round 10 — IQ & Reasoning) | 972 | expansion-r10-iq3.json (round 10 — IQ & Reasoning) | 599 |
| expansion-r10-iq4.json (round 10 — IQ & Reasoning) | 2,352 | expansion-r10-iq5.json (round 10 — IQ & Reasoning) | 798 |
| expansion-r10-iq6.json | 323 | expansion-r10-maths.json (round 10 — Maths & Numerical) | 3,030 |
| expansion-r10-maths10.json | 419 | expansion-r10-maths2.json (round 10 — Maths & Numerical) | 1,756 |
| expansion-r10-maths3.json (round 10 — Maths & Numerical) | 1,435 | expansion-r10-maths4.json (round 10 — Maths & Numerical) | 1,373 |
| expansion-r10-maths5.json (round 10 — Maths & Numerical) | 1,659 | expansion-r10-maths6.json (round 10 — Maths & Numerical) | 933 |
| expansion-r10-maths7.json (round 10 — Maths & Numerical) | 653 | expansion-r10-maths8.json | 376 |
| expansion-r10-maths9.json (round 10 — Maths & Numerical) | 719 | expansion-r10-nepal-facts.json (round 10 — Nepal GK/districts) | 504 |
| expansion-r10-nepali.json (round 10 — Nepali Language) | 656 | expansion-r10-nepali2.json | 298 |
| expansion-r10-office-edu-law.json | 186 | expansion-r10-science2.json | 84 |
| expansion-r10-vocab5.json | 1,232 | expansion-r10-vocab6.json (round 10 — English vocab) | 315 |
| expansion-r10-world-science.json | 477 | expansion-r5-csit-ioe.json | 216 |
| expansion-r5-current-science.json | 233 | expansion-r5-dental-ayurveda.json | 138 |
| expansion-r5-foreign-telecom.json | 241 | expansion-r5-law.json | 155 |
| expansion-r5-maths-hard.json | 1,071 | expansion-r6a-current.json | 407 |
| expansion-r6a-hard.json | 514 | expansion-r6a-thin-exams.json | 505 |
| expansion-r6b-banking-health.json | 327 | expansion-r6b-language.json | 460 |
| expansion-r6b-licence-entrance.json | 647 | expansion-r7a-licence.json | 455 |
| expansion-r7a-technical.json | 461 | expansion-r7b-core-hard.json | 576 |
| expansion-r7b-current.json | 357 | expansion-r8-current-language.json | 487 |
| expansion-r8-law-office.json | 492 | expansion-r8-nepal.json | 487 |
| expansion-r8-science-health.json | 480 | expansion-security-engineering.json | 137 |
| expansion-technical-psc.json | 420 | expansion-thin-exams.json | 522 |
| expansion-thin-topics.json | 517 | expansion-zero-licence.json | 437 |
| iq-maths.json | 206 | license-allied-health.json | 208 |
| license-health-assistant.json | 163 | license-medical.json | 173 |
| license-nursing.json | 189 | license-pharmacy.json | 205 |
| nepal-history-geography-culture.json | 201 | office-banking-education-health.json | 211 |
| previous-year-2083.json | 133 | tsc-education.json | 403 |
| expansion-r11-agri.json (round 11 rebuild) | 42 | expansion-r11-drills.json (round 11 rebuild) | 1043 |
| expansion-r11-drills2.json (round 11 rebuild) | 1046 | expansion-r11-drills3.json (round 11 rebuild) | 405 |
| expansion-r11-drills4.json (round 11 rebuild) | 153 | expansion-r11-drills5.json (round 11 rebuild) | 98 |
| expansion-r11-drills6.json (round 11 rebuild) | 1096 | expansion-r11-english.json (round 11 rebuild) | 133 |
| expansion-r11-english2.json (round 11 rebuild) | 65 | expansion-r11-english3.json (round 11 rebuild) | 66 |
| expansion-r11-grammar.json (round 11 rebuild) | 177 | expansion-r11-health.json (round 11 rebuild) | 28 |
| expansion-r11-iq.json (round 11 rebuild) | 242 | expansion-r11-iq2.json (round 11 rebuild) | 71 |
| expansion-r11-iq3.json (round 11 rebuild) | 77 | expansion-r11-iq4.json (round 11 rebuild) | 43 |
| expansion-r11-iq5.json (round 11 rebuild) | 83 | expansion-r11-law.json (round 11 rebuild) | 42 |
| expansion-r11-maths.json (round 11 rebuild) | 348 | expansion-r11-maths2.json (round 11 rebuild) | 69 |
| expansion-r11-nepal.json (round 11 rebuild) | 31 | expansion-r11-nepali.json (round 11 rebuild) | 94 |
| expansion-r11-nepali2.json (round 11 rebuild) | 102 | expansion-r11-science.json (round 11 rebuild) | 32 |
| expansion-r11-tech.json (round 11 rebuild) | 51 | | |
| **Total** | **64,671** | Bilingual (EN + NE) | 64,671 (100%) |

By topic: Maths & Numerical 16,133 · IQ & Reasoning 9,917 · English 7,520 · Health/Technical basics 5,047 · Nepali Language 2,369 · Current Affairs 1,547 · Computer & ICT 1,534 · Constitution & Governance 1,448 · Nepal Geography 1,309 · Science & Tech 1,295 · Economy & Development 1,180 · Education & Pedagogy 1,066 · Culture & Society 1,039 · Nepal History 966 · Banking & Finance 954 · Law 861 · Office Management & Public Service 828 · Physics 795 · Mathematics 671 · Chemistry 607 · Foreign Service & Diplomacy 592 · Biology 573 · Engineering Drawing 367 · Economy 257 · IQ 201.
By exam tag (one question can serve several exams): nasu 48,691 · kharidar 48,530 · section-officer 47,620 · nrb-assistant 35,183 · tsc-secondary 32,740 · tsc-primary 32,669 · rbb 31,263 · police 25,739 · army 25,728 · health 8,587 · foreign-service 7,180 · provincial-psc 6,115 · mecee-bl 3,856 · psc-service-groups 3,694 · ioe-entrance 3,509 · tsc-lower-secondary 3,393 · csit-entrance 3,216 · computer-operator 2,633 · sub-engineer 2,366 · tsc-license 2,052 · nrb-officer 2,049 · nea 1,470 · engineering 1,394 · nmc-mbbs 1,308 · staff-nurse-psc 1,256 · nhpc-ha 1,241 · nnc-rn 1,098 · nhpc-lab 1,048 · midwifery-nlem 1,035 · nhpc-public-health 1,022 · rbb-senior-assistant 958 · nepal-telecom 842 · npc-pharmacy 796 · bar-council 768 · nec-licence 760 · nmc-bds 667 · anm-guide 651 · judicial-service 585 · nhpc-ayurveda 580 · nhpc-physio 549 · nhpc-radio 548 · nhpc-optometry 524 · nhpc-dental 523 · deputy-secretary 19 · ayurveda-bams 18.
**Thin areas resolved in round 5:** NHPC Dental (30 → 109) and Ayurveda (30 → 104) now each cover a full 100-question paper; Law is now 329; CSIT 361, IOE 389, Foreign Service 312, Nepal Telecom 282. No prelim exam has zero tagged questions (see TESTING.md §K).

## ❓ Question format

```json
{
  "id": "HIST-001",
  "exam": ["kharidar", "nasu", "section-officer"],
  "topic": "Nepal History",
  "subtopic": "Unification",
  "difficulty": "easy",
  "marks": 2,
  "question": "Who unified Nepal?",
  "options": ["Prithvi Narayan Shah", "Tribhuvan", "Mahendra", "Birendra"],
  "answer": 0,
  "explanation": "Prithvi Narayan Shah began the unification campaign in the 18th century.",
  "source": "General knowledge"
}
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the accuracy rule before adding questions.

## 📚 Sources & caveats — read before trusting a figure

Exam patterns come from the research in `PLAN.md` and secondary syllabus reproductions (Edusanjal, Edusoft Academy, Shiksha Sanjal, CollegeNP). **The official PSC syllabus PDFs (psc.gov.np) were not read directly during research.** Before relying on any figure for a real application, verify it against **psc.gov.np / tsc.gov.np / nrb.org.np** and the vacancy notice. Known conflicts, flagged in the app and in `data/exams.json`:

- Section Officer main-paper pass mark: **40 vs 45** (sources disagree).
- Section Officer final-stage total: **70 vs 60** (Edusanjal vs another guide).
- TSC: whether general-paper marks count toward merit — disputed.
- Nepal Police ASI age/education varies by stream/vacancy.
- Health Service age limits vary by post; the 35/40 rule does not apply uniformly.
- The 2081/82 syllabus changed Kharidar/NaSu prelims from 100×1 in 90 min to **50×2 in 45 min** — the portal uses the 2081/82 pattern and labels it.
- Current-affairs questions are limited to stable facts up to 2025; vacancy numbers/dates change per notice and are deliberately not hard-coded.
- **RBB correction (2026-10-26):** the portal used to show an RBB prelim (50×2, 45 min, pass 40). The 2082-83 unified RBB/NBL/ADBL syllabus (approved 2082-06-09) has **no MCQ prelim** — two subjective papers + interview. The mock has been removed; the entry is guide-only.
- **NRB Officer prelim unverified:** the report supports only "pre-qualifying MCQ, 100 marks" — the 100×1 / 90 min / pass 45 shown in the portal is not verified against an NRB notice (flagged on the guide card).
- **Licence-exam caveats (from `data/LICENSE-RESEARCH.md`, researched 2026-10-26):** NMC negative marking is **not stated** in any source; NHPC negative marking is **not stated** for any discipline; NHPC time conflicts (BSc MIT and B.Optom syllabi say 2 hrs vs the 1.5 hr common format — portal uses 90 min, flagged); NMC subject weights differ slightly between sources (NMC says the distribution may change); NLEM practical marks conflict (50 vs 40 in different notices; 80% pass is consistent); Pharmacy "50% in EACH subject" rule is unverified (only overall 50% is in syllabus sources); BDS time (3 hrs) is inferred from the shared MBBS exam, not separately confirmed; NHPC Dental Hygiene and Ayurveda patterns are **unverified** (guide-only entries); ANM and NAMC/BAMS have no verified pattern at all (guide-only).
- **NEA pattern conflict:** the GAP-AUDIT verified pattern is Paper I Section A **50×1** (not 50×2) in 45 min, and no pass mark is stated for Section A alone — so NEA is guide-only with the pattern described in text, not a mock.
- **Other conflicts carried over:** Computer Operator Paper II duration 2h15m vs 3h15m; Nepal Police Inspector negative marking −0.25 vs 20% and LPT time 3 hrs vs 2h+2h; Deputy/Joint Secretary age "up to 45 (women/PWD 40)" is almost certainly a source error (inverted extension).
- Exam patterns for the new PSC entries (Sub-Engineer, Computer Operator, Nepal Telecom) come from the GAP-AUDIT's secondary sources (loksewatayariapp, CollegeNP), not official PSC PDFs — verify per vacancy notice. The "Trending" ranking is a demand proxy from prep-site FAQs and past-paper analysis, **not** Google Trends data (Trends returned HTTP 429 and could not be verified).
- The question bank was expanded overnight by several agents and merged 2026-10-26: 96 cross-file duplicate questions were removed (kept the original bank's copy), 200 duplicate HEAL2 IDs were fixed by renaming, and 7 duplicate options were replaced. The validator checks structure, not truth — a human accuracy audit of a sample is still open (see TESTING.md §H).

Questions were written from general knowledge and checked for answer correctness; if you find a wrong answer, please report it with the question ID — see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 Old Papers & Notices (added 2026-10-26)

**Old Papers** (`data/papers.json`, "Old Papers" nav): 17 real previous-year papers — NaSu First Paper 2083-01-20, Kharidar pretest 2083/06/04 and First Paper 2083-01-26, Koshi Province 4th Level First Paper 2083-01-26, NaSu 2nd Paper 2082-83, NaSu First Paper 2082, TSC NiMaVi First Paper 2082, Sangathit Sanstha pretest 2082, the DotNepal PSC archive (2073–2075) plus 7 individual DotNepal papers, and the Loksewa Aspirants NaSu collection PDF. Every entry was verified by opening its source page on 2026-10-26; the three 2083 first papers now have verified direct PDF URLs in `pdf_url` (the other papers' PDFs sit behind buttons the text fetch cannot resolve, so their `pdf_url` stays null). **Three papers are transcribed — 133 real questions** in `data/questions/previous-year-2083.json`: NaSu First 2083-01-20 (43 of 50), Kharidar First 2083-01-26 (45 of 50), Koshi 4th Level 2083-01-26 (45 of 50, the paper's two Q40s kept as 40a/40b). Excluded from the text bank: figure-based questions (image options/diagrams) and NaSu Q45, whose options differ only by capitalisation (FridAY vs FRIday) and cannot be scored fairly as a text MCQ. NaSu Q11 is a dual-answer (flawed) question — both Tuberculosis and Leprosy are correct per the paper's own note, and the explanation says so. Answers are exactly as printed/highlighted in the sources, not corrected. The Kharidar pretest 2083/06/04 stays **scanned-only: no answer key exists** ("KEY [A]" is only the paper code), so none of its 50 questions are in the scored bank. Transcribed papers get a "Practice these questions" button (`practicePaper()` in `app.js`, matching on paper-name keyword + date, since Kharidar First and Koshi share the date 2083-01-26); scanned-only papers show the source in an on-page viewer. Nothing is hosted here and no book scan is reproduced.

**Notices** (`data/notices.json`, "Notices" nav): 10 vacancy notices researched live on 2026-10-26 — PSC Under Secretary / Health 9th Level (Notice 582/2083-84, 159 posts, closes 2026-11-03), Nepal Police ASI + Office Assistant (334 posts, closes 2026-10-27; ASI applies via careers.nepalpolice.gov.np), Lumbini PPSC Level 8 Health (closes 2026-11-05), Gandaki PPSC 9th/8th Level (39 posts, closes 2026-10-27), plus 4 closed notices (TSC NiMaVi 678, TSC MaVi 449, NRB contract 34, RBB 138) and 2 unverified ones (TSC teaching licence, Bagmati PPSC). **No deadline, post count, fee or apply link is ever invented**: unverified items carry `close_date: null`, `status: "unverified"` and the label "Check official site — dates not verified on 2026-10-26". BS dates were converted to ISO with the `nepali-datetime` library and cross-checked against AD dates stated in the sources (e.g. 2083-01-20 → 2026-05-03, 2083-05-23 → 2026-09-08). The page also lists the official "where to check" sites (psc.gov.np, tsc.gov.np, nrb.org.np, Gandaki/Lumbini PPSC portals). Sources per notice are in `data/SOURCES.md` §15.

## 🗺️ Roadmap

- **v2 (done 2026-10-26):** demo sign-in + profile, Discussion Hub, Submit-a-Question with duplicate/spam/rate-limit checks, Maintainer Review queue with approve/reject/edit, report-wrong-question, community-approved questions with a "Community" badge, Supabase backend plan ([docs/BACKEND.md](docs/BACKEND.md)), bank 6,227 → **6,846** (English +320, Nepali +299).
- **Round 3 (done 2026-10-26):** bank 6,846 → **10,695** (+3,849 net; 3,850 written, 1 removed — unverified Nepal Army motto question ARMY-054). Zero-tagged mocks eliminated (NMC-BDS 180, Midwifery 150, Staff Nurse PSC 120); new exams MECEE-BL, NEC licence, Bar Council, BSc CSIT (with mocks) + IOE (guide-only, mixed-mark paper); hard-weighted core expansion (difficulty now 4,015 easy / 4,514 medium / 2,166 hard).
- **Round 4 (done 2026-10-26):** bank 10,695 → **12,695** (+2,000: NHPC disciplines now 110 each except Dental/Ayurveda at 30, Law 10 → 160, Bar Council 100 → 250, CSIT/IOE 75 → 175 each, Foreign Service/Telecom 80 → 160 each, +1,000 hard questions; difficulty now 4,475 easy / 5,122 medium / 3,231 hard). **Real previous-year questions transcribed by live-browser OCR: 133** — NaSu First 2083-01-20 (43), Kharidar First 2083-01-26 (45), Koshi 4th Level 2083-01-26 (45); bank 12,695 → **12,828** (1 excluded: NaSu Q45, capitalisation-only options). The Kharidar pretest 2083/06/04 has no answer key and stays scanned-only. Old Papers and Notices pages added; `practicePaper()` fixed (it matched on a paper id that never appears in question sources). See `data/SOURCES.md` §13 and TESTING.md §K.
- **Round 5 (done 2026-10-26):** bank 12,828 → **15,087** (+2,259 in 6 new `expansion-r5-*.json` files: hard IQ/Maths/Constitution 1,116; Dental + Ayurveda 153; Law 169; CSIT + IOE 250; Foreign Service + Telecom 274; Current Affairs/Science/Economy/Nepal GK 297). Dental 30 → 109, Ayurveda 30 → 104, Law 160 → 329, Bar Council 250 → 419, CSIT 175 → 361, IOE 175 → 389, Foreign Service 160 → 312, Nepal Telecom 160 → 282. Difficulty now 4,998 easy / 6,137 medium / 3,952 hard; round-5 answer balance 25.3% / 25.1% / 25.0% / 24.6%. All questions original (written from syllabus topics and verified facts, not copied from any prep site or book); generated arithmetic/IQ items were computed from rules and checked against the existing bank for duplicates (5 cross-file duplicates found and removed). Current Affairs 2025/2026 items (Gen Z protests, interim government, 2026 House election) verified against news sources — see `data/SOURCES.md` §16. Validator: `node scripts/test-questions.js` — ALL CHECKS PASSED, bilingual 100%.
- **Round 6 — fun + smooth (done 2026-10-26):** bank 12,828 → **15,087** is round 5; this round adds the UI polish, 412 fun facts, and gamification above (weekly challenge, focus timer, new badges, Surprise Me, Beat-your-best). No new exams. See TESTING.md §L.
- **Round 6b — question files + self-audit fixes (done 2026-10-26):** bank 15,087 → **18,200** (+3,113 net in 6 new files: thin exams 535, banking/health 352, language 487, licence/entrance 741, hard 561, current affairs 437 — after removing 125 duplicate texts). Self-audit fixes applied (see `data/SELF-AUDIT-2026-10-26.md` and TESTING.md §M): all question files on disk now load, mock mistakes save to Mistakes, timer stops on navigation, per-exam negative marking/marks in practice, mock topic mix for Kharidar/NaSu/Section Officer, MECEE −0.25, Staff Nurse rate stored as 0.2. Test status at the time: `test-app`, `test-e2e`, `test-v2`, `test-funfacts` pass; `test-questions` passes except `expansion-r7a-licence.json`, which was still being written by another worker (invalid JSON) at fix time; `test-bundle` still certifies the stale pre-round-6 bundle until rebuilt (F40).
- **Round 7 — licence + technical (done 2026-10-26):** bank 18,200 → **19,118** (+918 net in 2 new files: `expansion-r7a-licence.json` 500 — NHPC Lab/Radiography/Physiotherapy/Public Health/Optometry/Dental/Ayurveda + Midwifery, repaired from a malformed file that was still being written (stray comma + missing closing bracket; all 500 salvaged, 0 dropped); `expansion-r7a-technical.json` 418 — Sub-Engineer/Computer Operator/CSIT/IOE, 500 written, 82 removed as duplicate stems of older bank questions per the F08 rule, newer copy deleted). Topic "Health" normalised to "Health/Technical basics" in the r6a thin-exams file (535) and r7a-licence (500) — no stray topic remains. FF-070 reworded after verification: Nepal has never won a medal at the Olympic Games; its first Olympic-level medal was Palesha Goverdhan's Paralympic taekwondo bronze at Paris 2024 (see TESTING.md §N). Difficulty now 5,643 easy / 8,063 medium / 5,412 hard; answer balance A 24.4% / B 27.6% / C 24.3% / D 23.8%. All six test suites pass; phone bundle rebuilt (see TESTING.md §N).
- **Round 7b — core-hard + current + fun facts (done 2026-10-26):** bank 19,118 → **20,200** (+1,082 net: `expansion-r7b-core-hard.json` 600 — IQ/Maths/Constitution/English/Nepali, 45% hard; `expansion-r7b-current.json` 400 — Current Affairs/Economy/Science/Culture; plus `expansion-r7a-technical.json` restored 418 → 500 after its author replaced the 82 duplicate stems. R7B's 2026 World Cup facts independently verified (Spain beat Argentina 1-0, Ferran Torres 106', 19 July 2026; Mbappé Golden Boot, 10 goals). Fun facts 412 → **609** (+197 R7, verified, no duplicates). `VALID_EXAMS` in test-questions.js now lists all 47 exam ids (10 guide-only ids were missing, which is why R7B questions using provincial-psc / psc-service-groups / judicial-service failed validation). Difficulty now 5,698 easy / 8,642 medium / 5,860 hard; answer balance A 24.7% / B 26.2% / C 24.8% / D 24.3%. All six test suites pass; phone bundle rebuilt (see TESTING.md §O).
- **Answer-key audit (done 2026-10-26):** five audit workers checked the whole bank (maths/IQ, constitution/history, science/health/law, language/current/fun-facts, cross-file consistency) — 1,057 raw fix proposals deduplicated to 708 unique field changes, **616 applied**, 74 already fixed by the parallel numeric audit, 18 superseded by removals, 0 conflicts between workers. **68 unfixable questions removed** (36 degenerate current-affairs label questions, 8 broken letter-series, rest single-item defects) and 1 duplicate fun fact removed (FF-393). Bank 20,200 → **20,132**; fun facts 609 → **608**. Previous-year 2083 keys untouched (only a KHAR-2083-24 explanation correction). Difficulty now 5,692 easy / 8,635 medium / 5,805 hard; answer balance A 25.0% / B 26.6% / C 24.4% / D 24.0%. All six test suites pass; phone bundle rebuilt (see TESTING.md §P and `data/SELF-AUDIT-2026-10-26.md` §Answer-key audit).
- **Round 8 + Round 10 integration (done 2026-10-26):** R8 added 2,000 questions (Law/Office, Nepal, Science/Health, Current/Language — all bilingual); the R10 scale-up run added 28,700 across 25 files (English ×3, IQ ×4, Maths ×6, Nepali ×2, drills, health, grammar, world-science, Nepal facts, office/edu/law, science, current). Integration removed 1,417 duplicates in total: 837 exact-stem (test-questions.js), 25 exact rewordings, 9 same-fact, 43 near rewordings and 503 template-paraphrase/parameter-swap pairs (payload-verified; the dedupe plan's single MECEE-030 removal was REJECTED — ADH vs Oxytocin are different questions that share an answer). Answer-key audit re-run on R8/R10: 303 flags, all verified false positives of the audit script ("The answer is <text>" initial-letter misread; NE last-'='-value heuristic on remainder/unit-digit/letter-sum explanations) — no keys changed. Difficulty now 10,615 easy / 24,487 medium / 11,313 hard; answer balance A 28.0% / B 24.6% / C 23.9% / D 23.5% (A-skew comes from the R10 drill banks; options are shuffled at runtime). All six test suites pass; phone bundle rebuilt (see TESTING.md §Q and `data/SELF-AUDIT-2026-10-26.md` §Round 8 + Round 10 integration).
- **Feature round (done 2026-10-31):** bank unchanged at **64,671**; added Syllabus Coverage Tracker, Printable mock papers with OMR sheet, Deadline-driven study planner, Negative-marking guess-strategy coach, PYQ heatmap (133 transcribed PYQs), bilingual topic revision notes (top-20 topics, 238 bullets, PR-contributable), Audio revision mode (offline TTS), Ask chatbot (rule-based, on-device, never invents facts), Suggestions tab (local-only, upvoted), and renamed the portal to **Vidyapeeth (विद्यापीठ)**, then renamed again to **LokSewa Vidyapeeth (लोक सेवा विद्यापीठ)** per user request. See TESTING.md §Y–§Z.
- **Next (needs Supabase, see docs/BACKEND.md):** real Google sign-in, synced progress, live discussions, server-side submissions + moderation + CAPTCHA. **Peer leaderboard + national mock percentiles is backend-gated — do not build it localStorage-only; it ships with the Supabase rollout.**
- More previous-year papers (Kharidar pretest 2083/06/04 needs its answer key published; NaSu 2nd Paper 2082-83 is subjective, not MCQ)
- Subjective / theory practice with model answers (Kharidar Paper II, NaSu Paper II)
- Daily current-affairs quiz feed (curated, sourced)
- Fill the thin banks first: NHPC disciplines (30 → 100 tagged each), Foreign Service / Sub-Engineer / Computer Operator / Nepal Telecom / NMC-BDS / Midwifery / Staff Nurse PSC (0 tagged each), English (92) and Nepali Language (60) topics
- Licence-exam depth: NHPC Dental Hygiene & Ayurveda mocks (patterns verified, banks now 109/104 — mock engine still assumes uniform marks); human accuracy + Nepali translation audit of a sample before upload; real-browser smoke test (360px, EN/NE toggle, countdown + auto-submit).
- More mocks once their patterns are verified: NRB Officer (pattern unverified), RBB (no MCQ prelim exists), Police Inspector split-out (GART 50×2/50 min/pass 40)
- Full Nepali UI toggle (question text already switches EN/NE; chrome/nav labels are still bilingual labels, not a full UI switch)

## 🤝 Contributing

Contributions are welcome — questions, fixes, new mocks, translations. **The maintainer (Ravi Yadav) reviews every PR and decides to accept or reject it; there is no auto-merge.** Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) first.

## 📄 License

MIT — see [LICENSE](LICENSE).
