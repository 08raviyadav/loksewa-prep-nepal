# TESTING-OVERNIGHT.md — Lok Sewa Prep Nepal

Overnight website-testing pass. **Read-only on app code** — no edits were made to
`index.html`, `assets/js/app.js`, any question JSON, or any `scripts/*.js`.
This file is the only output. `TESTING.md` was not touched (coordinator merges later).

- **Run:** Sun 2026-10-25, ~18:10–18:13 UTC (23:55–23:58 NPT), local machine only.
- **Scope snapshot:** files last modified 17:50–17:57 UTC the same day; **none of
  the files this run read or tested changed during the run** (mtimes re-checked
  at the end), so the snapshot below is stable. Parallel agents *did* add new
  files under `data/` during this run (`EXAM-AUDIT.md`, `SOURCES.md`,
  `TRENDS.md`, `exams-new.json`) — those are other agents' work, not tested
  here, and they do not affect the app-code snapshot below. Nothing was
  uploaded, pushed, or shared.
- **Environment:** Node test suites + `python3 -m http.server` + curl/urllib.
  **No live browser was available to this agent** (generic subagent, no browser
  control) — see §6 for everything that leaves untested.
- **Status key:** PASS = ran and passed · REVIEWED = checked by reading the code,
  not by running it live · NOT RUN = needs a real browser.

## Verdict up front

- **Node suites: 47/47 checks PASS** (`test-app.js` 29/29, `test-e2e.js` 18/18,
  both exit 0 on the first run; bonus `test-questions.js` also PASS, 1,129 Q,
  exit 0). No failures, so no re-run was needed.
- **HTTP serving: 17/17 URLs return 200**, byte sizes match disk exactly.
- **Code review: 6 of 7 items verified** (timer, shuffle, scoring, mock specs,
  viewport/breakpoint, localStorage). **1 item FAILS as specified: there is no
  EN/NE language toggle** — only bilingual labels and a dark/light theme toggle.
  (An overnight expansion order to add an EN/NE toggle exists; it had not landed
  in these files at the time of this run — re-check after the other agents finish.)
- **No real-browser test was possible.** Rendering, live countdown ticking,
  localStorage in a real browser, and click-through of every view remain
  unverified (see §6).

## 1. Views inventory — all 10 present in `index.html`

| View | Section id | Line | Reached via |
|---|---|---|---|
| Home | `view-home` | 28 | Nav button |
| Practice | `view-practice` | 49 | Nav button |
| Quiz | `view-quiz` | 63 | Start practice / mock / Daily Challenge / Quick Quiz |
| Result | `view-result` | 66 | `finishAttempt()` |
| Mock | `view-mock` | 69 | Nav button |
| Exam Guide | `view-guide` | 83 | Nav button |
| Dashboard | `view-dashboard` | 86 | Nav button |
| Bookmarks/Mistakes | `view-review` | 89 | Nav button ("Bookmarks") |
| Flashcards | `view-flash` | 92 | Home card button / "Start flashcards" |
| Search | `view-search` | 95 | Nav button |

Nav bar (`index.html:15–21`) has 7 buttons: Home, Practice, Mock Exams, Exam Guide,
Dashboard, Bookmarks, Search. Quiz, Result and Flashcards have no nav button by
design — they are reached by actions. `test-app.js` checks all 10 view ids exist:
PASS (10/10). `showView()` (`app.js:57`) toggles `.active` and calls
`renderDashboard()` / `renderGuide()` / `renderReview()` on entry.

## 2. Node test suites

### `node scripts/test-app.js` — 29/29 PASS, exit 0 (single run, 18:10 UTC)

| Area | Checks | Result |
|---|---|---|
| `app.js` parses | 1 | PASS |
| Scoring maths (20% negative) | 4 | PASS — 2.6 case, 10×2-mark = 20, 2 wrong = −0.6, negative OFF = 0 |
| XP (score 20 → 200 XP) | 1 | PASS |
| Shuffle / option remap | 3 | PASS — 20 distinct question orders; 50 remap trials correct; 13 distinct option orders |
| Static element ids exist in `index.html` | 1 | PASS — 13 ids checked |
| All 10 views exist | 10 | PASS |
| `exams.json` parses, ≥10 exams | 1 | PASS — 12 exams |
| Mock specs vs `exams.json` | 5 | PASS — kharidar 50Q/45min/2/pass 45; nasu 50/45/2/45; section-officer 100/90/1/45; tsc-primary 50/60/2/50; nrb-assistant 50/45/2/40 |
| CSS / references / no CDN | 3 | PASS — `style.css` non-empty; `index.html` references `app.js` + `style.css`; no external script/font links |

### `node scripts/test-e2e.js` — 18/18 PASS, exit 0 (single run, 18:10 UTC)

Runs `app.js` in a Node VM with a minimal DOM stub and real question data from disk.

| Check | Result |
|---|---|
| `loadData()` loads 1,129 questions / 12 exams | PASS |
| Practice starts with 10 questions | PASS |
| All-correct practice scores 100% and shows PASS | PASS — note: the set scored **19/19**, not 20/20, because one of the 10 sampled questions was 1-mark; pass/fail is judged on % vs cutoff % |
| XP recorded in localStorage progress | PASS |
| Second random set, different question order | PASS |
| Option order varies across 20 fresh sets | PASS — 20 distinct first-question option orders |
| Mock (Kharidar) starts with 50 questions, all 2-mark | PASS |
| Mock timer set to 45 min (2,700 s) | PASS |
| Mock 25 right / 25 wrong = **40/100, FAIL** vs cutoff 45 | PASS — exact PSC maths (50 − 25×0.4 = 40) |
| Daily Challenge same 10 questions twice on the same day | PASS |
| Quick Quiz is 5 questions | PASS |
| Flashcards load 20 cards | PASS |
| Search "Everest" returns results | PASS |
| Bookmark saved to progress | PASS |
| Wrong answer saved to Mistakes | PASS |
| Dashboard renders stats | PASS |
| Exam Guide renders all 12 exams | PASS |

### Bonus (not in the task scope, run read-only for completeness)

`node scripts/test-questions.js` — **PASS, exit 0.** 1,129 total
(245 constitution-governance-economy, 224 english-nepali-computer, 220 iq-maths,
220 nepal-history-geography-culture, 220 office-banking-education-health);
16 topics; exam tags: kharidar 851, nasu 859, section-officer 798,
nrb-assistant 175, tsc-primary 159, tsc-secondary 153, rbb 73, nrb-officer 45,
health 31, police 26, army 26, engineering 10.

No suite failed, so the "re-run once after a short wait" rule was never triggered.
No test file was edited.

## 3. Local serving — `python3 -m http.server 8000`

Server started in `~/workspace/loksewa-prep-nepal/`, stopped after the sweep
(process gone, port 8000 connection-refused on probe — confirmed stopped).

| Path | HTTP | Bytes | Content-Type | Matches disk |
|---|---|---|---|---|
| `/` | 200 | 8,092 | text/html | yes |
| `/index.html` | 200 | 8,092 | text/html | yes |
| `assets/css/style.css` | 200 | 4,706 | text/css | yes |
| `assets/js/app.js` | 200 | 24,465 | text/javascript | yes |
| `data/exams.json` | 200 | 9,965 | application/json | yes |
| `data/questions/nepal-history-geography-culture.json` | 200 | 122,657 | application/json | yes |
| `data/questions/constitution-governance-economy.json` | 200 | 139,776 | application/json | yes |
| `data/questions/iq-maths.json` | 200 | 102,447 | application/json | yes |
| `data/questions/english-nepali-computer.json` | 200 | 122,571 | application/json | yes |
| `data/questions/office-banking-education-health.json` | 200 | 127,907 | application/json | yes |
| `README.md` | 200 | 6,762 | text/markdown | yes |
| `PLAN.md` | 200 | 4,127 | text/markdown | yes |
| `TESTING.md` | 200 | 11,054 | text/markdown | yes |
| `LICENSE` | 200 | 1,067 | application/octet-stream | yes |
| `CONTRIBUTING.md` | 200 | 3,129 | text/markdown | yes |
| `CODE_OF_CONDUCT.md` | 200 | 2,207 | text/markdown | yes |
| `SECURITY.md` | 200 | 1,247 | text/markdown | yes |

Extra serving checks (all PASS):

- Every served JSON file parses: `exams.json` = 12 exams; question files =
  220 / 245 / 220 / 224 / 220 questions (total 1,129).
- Served `app.js` passes `node --check`.
- Missing file returns 404 (`GET /nope.txt` → 404) — the server is a real static
  server, not a catch-all.
- Zero `https://` URLs in `index.html`, `app.js`, `style.css` — fully offline,
  no CDN / external font / external script.

**Measurement note (honest):** rapid-fire `curl` in a tight loop returned
`HTTP 000` (connection failure, requests never reached the server) for most
paths after the first 1–2, while the server log showed no trace of them. The
same URLs fetched one-by-one (verbose curl, 1 s-spaced loop, and a Python
urllib fetcher with 0.6 s spacing) all returned 200 with exact byte sizes.
The 000s are a burst-rate artifact of this sandbox's localhost networking,
not a server or app fault — but a real browser loading the page fires several
parallel fetches at once, so **parallel-fetch behaviour is one more thing the
real-browser pass should confirm** (it works in Node's `loadData()` stub and in
sequential fetches; it was not observed under a browser's parallel load).

## 4. Code-review checklist (read, not run in a browser)

| # | Check | Verdict | Evidence |
|---|---|---|---|
| 1 | **EN/NE toggle exists and is wired** | **NOT PRESENT** | No language-toggle button, handler, or `lang`/`data-lang` switching code anywhere: `grep -i "lang-toggle\|toggleLang\|setLang\|language\|data-lang"` over `index.html` + `app.js` + `style.css` returns nothing. The only toggle is the dark/light **theme** toggle (`index.html:22`, `#theme-toggle`, wired at `app.js:307`, `data-theme` flip). What exists instead is **bilingual labels**: Devanagari in headings (`index.html:12` logo "लोक सेवा तयारी", `:50` "Practice — अभ्यास", `:70` "Mock Exams — नमुना परीक्षा", `:83` "Exam Guide — परीक्षा जानकारी") and `name_ne` on all 12 exams in `data/exams.json` (rendered in `renderGuide`, `app.js:291`). Font stack includes "Noto Sans Devanagari" (`style.css:5`). README Roadmap lists "Nepali-language UI toggle (full UI, not just labels)" as **future work**, and the overnight expansion order includes adding it — it had not landed in these files at the time of this run. **Re-check after the other agents finish.** |
| 2 | **Timer exists with auto-submit** | REVIEWED | `startTimer(onTimeout)` (`app.js:120–125`): `setInterval` 1 s, decrements `timeLeft`, writes `#quiz-timer` via `fmtTime()` (`app.js:126`), adds `.low` class at ≤300 s, calls `onTimeout()` at 0. Wired at both call sites: practice — `startPractice()` (`app.js:117`, `timeLeft = questions × 54`, `startTimer(()=>finishAttempt(true))` when the timer checkbox is on); mock — `startMock()` (`app.js:225`, `timeLeft = prelim.timeMin × 60`, `startTimer(()=>finishAttempt(true))`). `finishAttempt(timedOut)` (`app.js:174`) renders "(time up — auto-submitted)". E2E confirms the timer *value* is set (2,700 s for Kharidar) but the 1 s ticking and the actual auto-submit callback were **not observed live** — see §6. |
| 3 | **Fisher–Yates shuffle of questions AND options** | PASS | `shuffle()` (`app.js:7–11`) is textbook Fisher–Yates (i from end, j = random 0..i, swap, copy first). `shuffleOptions()` (`app.js:13–15`) shuffles `[0,1,2,3]` and remaps `answer` via `idx.indexOf(q.answer)`. Applied to questions in `startPractice` (`app.js:108`), `startMock` (`app.js:217`), `dailyChallenge` (`app.js:231`, date-seeded LCG), `quickQuiz` (`app.js:239`), `startFlashcards` (`app.js:245`), and to options on every question built. Verified by tests: 20/20 distinct question orders, 20/20 distinct option orders, 50/50 correct remaps (§2). Minor doc nuance: README says "Math.random + timestamp seed" — practice/mock shuffles use plain `Math.random` (no timestamp seed); only Daily Challenge is seeded (by date). |
| 4 | **Scoring maths — 20% negative** | PASS | `scoreAttempt()` (`app.js:17–24`): correct += marks; wrong −= `marks × 0.20` when `negativeOn`; skipped = 0; result rounded to 1 decimal (`Math.round(score*10)/10`); `pct` floored at 0 for negative scores. −0.4 per wrong 2-mark Q and −0.2 per wrong 1-mark Q confirmed by the 2.6 and −0.6 unit cases (§2) and the 40/100 mock E2E case. Pass/fail: `finishAttempt()` (`app.js:174`) judges **percentage vs cutoff %** (`cutoffPct = prelim.pass / prelim.total × 100`; Kharidar/NaSu/Section Officer 45%, TSC 50%, NRB Assistant 40%) — identical to the raw cutoff on full-length mocks. |
| 5 | **Mock specs match `data/exams.json`** | PASS | All 12 exams dumped from `data/exams.json` (verified against the file, not the docs): kharidar 50×2=100/45min/pass 45; nasu 50×2/45/45; section-officer 100×1/90/45; tsc-primary 50×2/60/50; tsc-secondary 50×2/60/50; nrb-assistant 50×2/45/40; nrb-officer 100×1/90/45; rbb 50×2/45/40; police 50×2/45/45; army 50×2/45/45; health 50×2/45/45; engineering 50×2/45/45. The 5 specs asserted in `test-app.js` all PASS (§2). `startMock()` (`app.js:217`) reads the spec generically from the selected exam (`p.questions`, `p.timeMin`, `p.marksPerQ`) and forces `marks = p.marksPerQ` on every question, so the mock always mirrors the data file. The HTML mock table (`index.html:69–78`) lists only the 5 headline mocks — the dropdown itself is populated with all 12 exams (`fillExamSelects`, `app.js:88`). See observation in §5 about thin-coverage mocks. |
| 6 | **Mobile viewport meta + 640 px breakpoint** | REVIEWED | Viewport meta present (`index.html:5`, `width=device-width, initial-scale=1.0`). Breakpoint present (`style.css:54`, `@media(max-width:640px)`: smaller hero `h1`, tighter hero padding, smaller nav buttons, smaller `.result-big`). Layout is mobile-first (`.grid` uses `repeat(auto-fit,minmax(220px,1fr))`; nav wraps; `.palette` wraps). **Not observed at a real 360 px viewport** — see §6. |
| 7 | **localStorage progress keys** | PASS (stub) / NOT RUN (real browser) | Key `loksewa_progress_v1` (`app.js:5`); `loadProgress()` / `saveProgress()` (`app.js:31–35`, try/catch guarded). Stored shape: `{ xp, level, streak, lastDay, attempts[], bookmarks[], mistakes[], flashcardsSeen, dailyDone{} }`. E2E (Node stub) confirms XP, bookmark and mistake writes land in the store (§2). **Persistence across real page loads in a real browser was not observed** — see §6. Streak logic (`updateStreak`, `app.js:38`) is consecutive-day increment / gap resets to 1 — code-read only, date-boundary behaviour not live-tested. |

## 5. Observations (not failures, worth the coordinator's attention)

1. **Mock dropdown covers all 12 exams, the table only 5.** `fillExamSelects()`
   puts every exam into `#mock-exam`, so mocks for nrb-officer, rbb, police,
   army, health and engineering are startable even though the HTML table lists
   only Kharidar / NaSu / Section Officer / TSC General / NRB Assistant.
   Either list the other 7 in the table or scope the dropdown — a user picking
   "Engineering Service" gets a mock whose table row doesn't exist.
2. **Thin-coverage mocks fall back to the whole bank.** `startMock()`
   (`app.js:217`): if the exam-tagged pool is smaller than the paper, `pool =
   QUESTIONS.slice()` — e.g. Engineering has 10 tagged questions but the mock
   needs 50, so ~40 of its 50 questions come from unrelated topics. Same for
   police/army (26 tagged each). The mock still runs and scores correctly, but
   it is mostly off-syllabus. Consider capping, warning, or labelling these
   mocks until coverage grows.
3. **`exam-guides/` directory is empty.** The Exam Guide is rendered entirely
   from `data/exams.json` (`renderGuide`, `app.js:291`) — the empty folder is
   dead weight / a stub for per-exam pages that don't exist. Harmless, but
   don't assume guide content lives there.
4. **"TSC General" in the mock table vs two TSC exams in data.** The table's
   TSC row (50/60/2/50) matches both `tsc-primary` and `tsc-secondary`
   identically, so no spec conflict — just a naming loose end.
5. **No external requests at all** (zero `https://` in `index.html`, `app.js`,
   `style.css`) — the offline claim holds. The only network calls the app
   makes are `fetch()` of its own JSON files.
6. **Theme toggle is not persisted.** The `data-theme` flip (`app.js:307`)
   writes nothing to localStorage, so the theme resets to dark on reload.
   Cosmetic; the progress key exists and could carry it.

## 6. What was NOT tested — no real browser was possible

This agent is a generic subagent with **no live-browser control**: it cannot
open Chrome, click, type, resize a viewport, or read a console. Everything
below is therefore **untested**, not merely unrecorded. The coordinator should
treat these as the mandatory pre-upload checklist (matches TESTING.md items
99–100, still open):

1. **Live countdown ticking** — `startTimer`'s 1 s interval, the `#quiz-timer`
   text updating each second, the `.low` red state under 5:00, and the actual
   auto-submit firing `finishAttempt(true)` at 0:00 with the "(time up —
   auto-submitted)" result. (Timer *value* set: verified in E2E; ticking:
   not observed.)
2. **Rendering at a real 360 px viewport** — nav wrapping, hero, option
   buttons, palette, tables, and the 640 px breakpoint actually applying.
   (Breakpoint *present in CSS*: verified; *applied*: not observed.)
3. **localStorage in a real browser** — progress surviving a reload, XP/streak/
   bookmarks/mistakes persisting across sessions, and the `file://` fallback
   message when the bank can't load. (Writes verified only against a Node stub.)
4. **EN/NE toggle click-through** — moot until the toggle exists (§4.1); once
   added, verify the toggle switches UI strings and persists.
5. **Full click-through** — Home → Practice (pick exam/topic/count, start,
   answer 10, skip, bookmark, report) → Result (retry-wrong-only, new random
   set) → Mock (palette jumps, finish) → Dashboard (chart draws) → Bookmarks
   → Flashcards (reveal/next) → Search → Exam Guide (start-mock button) —
   in Chrome and on a phone viewport, with **zero console errors**.
6. **Parallel `fetch()` under a browser** — the app loads 6 JSON files on
   startup; sequential fetches verified 200 here, but a browser fires them in
   parallel (see the burst-rate artifact note in §3 — almost certainly a
   sandbox quirk, but only a browser run can close it out).
7. **Devanagari rendering** — "Noto Sans Devanagari" is in the font stack
   (`style.css:5`), but no browser rendered the नेपाली labels in this run.
8. **Question accuracy audit** — TESTING.md item 100: a human re-check of a
   sample (~50 questions) against reliable sources. The validator checks
   structure, not truth; this run checked no answers.

## 7. Summary for the parent agent

- `test-app.js`: **29/29 PASS, exit 0** (one run).
- `test-e2e.js`: **18/18 PASS, exit 0** (one run).
- `test-questions.js` (extra): **PASS, exit 0**, 1,129 questions.
- HTTP: **17/17 files 200**, sizes match disk; served JSON parses; served
  `app.js` passes `node --check`; 404 behaves correctly.
- Code review: timer, Fisher–Yates (questions + options), 20% negative
  scoring (−0.4 / −0.2), mock specs vs `data/exams.json`, viewport meta +
  640 px breakpoint, localStorage keys — all verified by reading + tests.
- **One gap: no EN/NE language toggle exists yet** (bilingual labels only;
  theme toggle is the only toggle). The overnight expansion order includes
  adding it; re-check once the other agents land it.
- **No real-browser test was possible in this environment.** The 8 items in §6
  (live countdown, 360 px rendering, real-browser localStorage, click-through,
  parallel fetch, Devanagari rendering, question accuracy) remain open and
  should be done before any GitHub upload.
- HTTP server on port 8000 was **stopped** after the sweep (verified: no
  process, connection refused). No files were modified except this report.
