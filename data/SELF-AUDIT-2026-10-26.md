# SELF-AUDIT — Lok Sewa Prep Nepal (aspirant walk-through)

**Date:** 2026-10-26
**Auditor role:** aspirant (Kharidar / NaSu / TSC / NRB) walking the whole app end-to-end in code.
**Repo state audited:** `~/workspace/loksewa-prep-nepal/` — `index.html` (201 lines), `assets/js/app.js` (1,786 lines), `assets/css/style.css` (210 lines), `data/exams.json` (47 exams), `data/papers.json` (17), `data/notices.json` (10), `data/funfacts.json` (412 facts), `README.md`, `data/SOURCES.md`, `data/EXAM-AUDIT.md`, `data/GAP-AUDIT.md`, all 6 test scripts in `scripts/` (run read-only).
**Constraint honoured:** NOTHING was edited except this file. `index.html`, `assets/js/app.js`, `assets/css/style.css` and all `data/questions/*.json` / `data/funfacts.json` were read-only — a round-6 coordinator is editing those concurrently. No bundle build, no upload.
**Headline:** 40 findings — 9 Breaks studying · 9 Wrong info · 7 Dead end · 9 UX friction · 6 Polish. The single biggest problem is **F01**: round-6's 1,763 new questions exist on disk but are never loaded, so the app still serves the old 15,087-question bank and `test-app.js` is currently FAILING. The second biggest is **F10**: no mock mirrors its real paper's topic mix (a Kharidar mock should be 20/50 office-skills questions; a random draw gives ~1.8). Two sampled questions have provably wrong answers (**F02, F03**).

## Method

Walked every view in code, in aspirant order: Home → Practice (all difficulties, counts 5/10/20/50, timer on/off, negative on/off) → Mock (all 33 mocks: countdown, auto-submit, OMR palette) → result / wrong-answer review → retry-wrong-only → Flashcards → Daily Challenge → Quick Quiz → Speed Round / Mistake Marathon / Question of the Day → Bookmarks & Mistakes → Discussion Hub → Submit a Question → Old Papers (transcribed-paper practice) → Notices → Profile / demo sign-in → Fun Facts → light/dark + EN/NE toggles.

Checks run with Python (read-only) over the data, plus `node` runs of the existing suites:

- `QUESTION_FILES` in `app.js:4` vs files on disk; per-exam tagged counts vs every mock's `questions` requirement; `questions × marksPerQ` vs `prelim.total` for all 47 exams; breakdown sums (NMC 130, NNC 150, NHPC 100s, Pharmacy 150).
- HTML `onclick="…"` handlers vs functions defined in `app.js`; `getElementById` ids vs ids in `index.html`; localStorage keys read vs written.
- Random sample: 1 per question file (45 files → 45 questions, seed 20261026) read in full (EN + NE question/options/explanation/source), plus whole-bank scans: duplicate ids/texts/options, missing `_ne` fields, Devanagari presence, explanation length, correct-option length giveaway heuristic.
- Notices checked against audit date 2026-10-26 for expired-but-marked-open; papers' `practicePaper()` matching simulated in Python (keyword + date).
- Test suites run: `test-app.js` (1 FAIL), `test-questions.js` (31 FAILURES), `test-e2e.js` (PASS), `test-v2.js` (PASS), `test-funfacts.js` (PASS), `test-bundle.js` (PASS — but see F40: it tests a stale bundle).

### What I could NOT check without a real browser (honest limits)

- Nothing was rendered. Countdown/auto-submit timing, palette taps, confetti, animations, sticky bottom nav, 360 px layout, Devanagari clipping, iframe embedding of scanned papers (F25), Google-style demo sign-in flow, and the actual visual result of the EN/NE toggle were verified **in code only**.
- No live verification of any exam pattern, notice deadline, fee or apply link against psc.gov.np / tsc.gov.np / nrb.org.np — patterns were checked only against `data/exams.json`, `SOURCES.md`, `EXAM-AUDIT.md` and `GAP-AUDIT.md`, which themselves rest on secondary sources (see "still needs real browser / human check").
- Question-answer correctness beyond the 45-question sample and the heuristic scans: the validator checks structure, not truth. The 2 wrong answers found in a 45-sample imply more wrong answers in the 16,850-question bank; the true error rate is unknown.
- The 1,807 "long correct option" hits (F31) are a heuristic signal, not 1,807 proven defects.

### Things that checked out clean (so the coordinator doesn't re-check them)

- No dead `onclick` handlers: every handler in `index.html` exists in `app.js`; every JS-generated handler exists except a false positive on the literal word `if` inside an inline `onclick="if(confirm(...))"`.
- All static element ids used by `app.js` exist in `index.html` (`test-app.js` passes this check).
- localStorage keys are consistent between read and write (`loksewa_progress_v1`, `loksewa_lang`, `loksewa_theme`, `loksewa_speed_best_v1`, `loksewa_fact_streak_v1`, `loksewa_discussions_v1`, `loksewa_submissions_v1`, `loksewa_community_approved_v1`, `loksewa_reports_v1`, `loksewa_moderation_log_v1`).
- No duplicate question ids (16,850 unique); 0 missing `question`/`options`/`answer`/`explanation`/`source`/`question_ne`/`options_ne`/`explanation_ne`; 0 duplicate options (exact match); 0 U+FFFD garbled characters; answer-position balance 24.7% / 26.6% / 24.5% / 24.1% (A/B/C/D).
- Every mock now has ≥ its required tagged questions (thinnest: `nepal-telecom` 282 tagged for a 50Q mock; `nmc-mbbs` 297 for 130Q; `mecee-bl` 228 for 200Q) — the old thin-bank fallback to the whole bank is now dead code in practice, but see F10: count is fine, mix is not.
- `practicePaper()` matching verified by simulation: NaSu 2083-01-20 → 43, Kharidar First 2083-01-26 → 45, Koshi 2083-01-26 → 45. Matches `papers.json` counts.
- Notices as of 2026-10-26: **none** expired-but-marked-open (2 open close 2026-11-03 / 2026-11-05; 2 closing-soon close 2026-10-27; 4 closed; 2 unverified with `close_date: null`). See F17 for why this will go stale tomorrow.
- Fun facts: 412 unique ids, no duplicate EN or NE texts (`test-funfacts.js` PASS).
- `test-e2e.js` and `test-v2.js` PASS (speed round, mistake marathon, dashboard records, share, discussions, submissions, moderation, reports).

## Findings table

Severity: **Breaks studying** = aspirant learns wrong things, loses work, or a feature silently does not work. **Wrong info** = the app states something false about an exam/score. **Dead end** = a path that goes nowhere or misleads. **UX friction** = works but costs taps/confusion. **Polish** = small, cosmetic or maintainability.

| ID | Severity | Where | What an aspirant experiences | Evidence |
|---|---|---|---|---|
| F01 | Breaks studying | `assets/js/app.js:4` vs `data/questions/` | Round-6's 1,763 new questions are invisible: the Home counter, practice, mocks and search all still use the old 15,087 bank. A student revising NHPC Dental / Banking / Nepali / licence topics gets none of the new material. | `QUESTION_FILES` lists 41 files; disk has 45 bank files (+ `community-approved.json`). Unlisted: `expansion-r6a-thin-exams.json` (566), `expansion-r6b-banking-health.json` (269), `expansion-r6b-language.json` (380), `expansion-r6b-licence-entrance.json` (548). Loaded total 15,087 vs disk 16,850. `node scripts/test-app.js` → `FAIL app.js QUESTION_FILES lists all 45 question files — 41 listed vs 45 on disk` (the suite's only failure). |
| F02 | Breaks studying | `data/questions/expansion-health-technical-security.json:5071`, id `HEAL2-182` | "Which vaccine protects a child against tuberculosis?" — the app marks **Measles** correct. The explanation itself says BCG. The aspirant memorises the wrong vaccine for a Health Service / Staff Nurse exam. | `answer: 2` → options `['BCG','OPV','Measles','DPT']` → Measles; `explanation: "BCG vaccine protects against tuberculosis…"`. Correct answer index must be 0. |
| F03 | Breaks studying | `data/questions/expansion-hard-core-v2.json:8913`, id `HARD2-298` | "Father 30, son 10 — after how many years will father be twice as old?" Options contain **two** "10 years" answers (`10 years (alt)` and `10 years`), and the marked answer is **20 years** while the explanation proves **10 years** (30+x=2(10+x) → x=10). Whatever the aspirant picks, the app contradicts itself. | `options: ['10 years (alt)','12 years','10 years','20 years'], answer: 3, explanation: "…gives x = 30 − 2 × 10 = 10 years."` The validator's duplicate-option check is exact-match only, so the `(alt)` suffix lets this through (see F43 in fix specs — folded into F03's spec). |
| F04 | Breaks studying | `assets/js/app.js:656` `mockNegRate()`, `data/exams.json` `mecee-bl` | MECEE-BL mock deducts **20%** per wrong answer. The real MECEE-BL deducts **−0.25** per wrong 1-mark question (25%). Scores in the mock are systematically too generous; a borderline aspirant is misled about readiness. | `function mockNegRate(p){ return (p.negative === null \|\| p.negative === 0) ? 0 : 0.2; }` — any non-zero `negative` collapses to 0.2. `mecee-bl.prelim.negative` is 0.25. `test-app.js` tests `scoreAttempt` at 0.25 but never `mockNegRate({negative:0.25})`, so the suite misses it. |
| F05 | Breaks studying | `assets/js/app.js:837-860` `answerOption()` | Wrong answers in a **mock** are never saved to Mistakes. Only practice-mode answers call `saveMistakeIfWrong()`. The aspirant finishes a 100-question Section Officer mock, opens Bookmarks & Mistakes / Mistake Marathon, and finds nothing — the highest-value revision material (mock errors) is lost. Dashboard weak topics (`weakTopics()`, from mistakes only) also undercount. | `answerOption()`: `if(c.mode==='practice'){ showFeedback(); saveMistakeIfWrong(); }` — no equivalent call in the mock branch; speed mode returns before it. `retryWrong()` only uses the in-memory `current._wrong`, lost on reload/navigation. |
| F06 | Breaks studying | `assets/js/app.js:639-654` `showView()`, `:779-785` `startTimer()` | Starting a timed mock/practice and then tapping Home/Guide/etc. does **not** stop the timer. When it hits zero, `finishAttempt(true)` fires and yanks the aspirant to the result screen from whatever view they were on, recording a half-finished attempt as an auto-submitted mock. | `showView()` contains no `clearInterval(timerId)` (verified by grep). `clearInterval` appears only in `startTimer()` and `finishAttempt()`. No `timerId` handling on navigation. |
| F07 | Breaks studying | `assets/js/app.js:759-766` `filteredQuestions()`, `data/exams.json` (10 exams with 0 tagged questions) | Picking a guide-only exam with **0 tagged questions** in Practice (Deputy Secretary, JTA, Ranger, Judicial Service, PSC Service Groups, RBB Senior Assistant, Provincial PSC, NEA, ANM guide, Ayurveda BAMS) silently serves a random set from the **whole bank**, labelled as that exam. The aspirant "practices Deputy Secretary" and gets Kharidar GK. | `filteredQuestions()`: `if(!pool.length) pool=QUESTIONS.filter(q=>!topic\|\|q.topic===topic);` — the exam filter is dropped entirely. `fillExamSelects()` puts **all** 47 exams in the practice select with no guide-only warning. (Note: `rbb` has 989 tagged questions so practice works there; `nhpc-dental`/`nhpc-ayurveda` have 190/205 tagged but are guide-only — practice works, mock correctly absent.) |
| F08 | Breaks studying | `data/questions/*.json` (31 texts) | The same question appears twice in the bank (different ids), so an aspirant can meet the identical question twice in one set and the bank count is inflated. Mostly round-6 duplicates of older questions. | `node scripts/test-questions.js` → `FAILURES (31)` — all "duplicate question text". Examples: `CONST-202` vs `R6A-A484` ("Which vitamin is produced in the skin by sunlight?"); `LAB-038` vs `R6A-A297`; `RAD-001` vs `R6A-A155`; `BDS-013`, `ALLIED-092`, `NUR-085` (pre-round-6 duplicates too). Full list is in the validator output. |
| F09 | Breaks studying | `assets/js/app.js:175,189,203,1012,1020` + `:874-911` `finishAttempt()` | (a) Speed Round bonus is added to the score with no cap: the e2e test itself records **28/18 (100%)** — a score above the maximum, shown on the result screen and in share text ("I scored 28/18"). (b) Daily Challenge, Quick Quiz, Surprise Me, Speed Round and Mistake Marathon all hardcode `exam:'kharidar'` — a TSC/NRB aspirant's result screen, dashboard history and "Beat your best" all say Kharidar, and the speed result is pass/fail-judged against the Kharidar 45% cutoff. | `finishAttempt()`: `res.score=Math.round((res.score+bonus)*10)/10; res.pct=…Math.min(100,…)` — pct capped, score not. `dailyChallenge`/`quickQuiz`/`surpriseQuiz`/`startSpeedRound`/`startMistakeMarathon` all set `exam:'kharidar'`. `cutoffPct` is then derived from the Kharidar prelim for all of them. |
| F10 | Wrong info | `assets/js/app.js:984-1011` `startMock()`; `data/exams.json` `prelim.breakdown` | **No mock mirrors its real paper's topic mix**, despite the Mock page claiming "exactly like the real prelim: same question count, same time, same marks". `startMock()` ignores `prelim.breakdown` entirely and draws uniformly at random from the exam's tagged pool. Kharidar should be GK 30 + Office Skills 20; the tagged pool has only 318/8,860 Office questions, so a random 50-draw contains **~1.8** office questions. Section Officer should be English 20/100; pool has 662/8,717 English → **~7.6**. NRB Assistant's 30+30 Management/Economics split is likewise unenforced. The mock tests the wrong syllabus weights. | `startMock()` contains no reference to `breakdown` (verified). Tagged-pool topic counts (loaded bank): kharidar Office 318/8,860 (3.6% vs required 40%); nasu same shape; section-officer English 662/8,717 (7.6% vs required 20%); nrb-assistant Banking 303 + Economy 239 of 921. |
| F11 | Wrong info | `data/exams.json` `nmc-mbbs.prelim` (`questions:130, marksPerQ:1, total:180, pass:90`); `assets/js/app.js:913` `renderResult()` | NMC-MBBS mock shows a score out of **130** but a cutoff of **"90/180"**. A student scoring 65/130 (50%) is told PASS, although 65 < 90 raw marks — because the 10 CSQs (50 marks) are not in the mock at all. The result screen never explains that the pass line is a percentage proxy over a paper the mock does not contain. | `prelim.total` (180) ≠ `questions × marksPerQ` (130) — the only such mismatch in all 47 exams. `cutoffPct = pass/total*100` (50%) while `res.max` is 130. The guide card does explain the CSQ gap; the result screen does not. |
| F12 | Wrong info | `data/exams.json` `mecee-bl.prelim` (`pass:100, total:200`); `assets/js/app.js:874-911` | MECEE-BL result says PASS/FAIL against "cutoff 50% (100/200)". The real MECEE-BL pass is the **50th percentile** (a merit-list rank), not 50% marks. The proxy is disclosed in the exam's `note` and README, but the result screen presents it as the cutoff with no "proxy" qualifier — an aspirant at 52% walks away believing they passed. | `mecee-bl` note: "Pass is the 50th percentile, not a fixed mark — the portal judges at 50% (100/200) as a proxy." `renderResult()` prints `cutoff for this exam is ${cutoffPct}% (${cutoff}/…)` with no proxy wording for any exam. |
| F13 | Wrong info | `assets/js/app.js:767-778` `startPractice()`; `:1012-1025` daily/quick | Practice ignores the exam's own marking scheme twice over: (1) negative marking is a checkbox defaulting ON at 20% for **every** exam, including no-negative exams (NNC, NHPC, NEC, Bar Council, CSIT) — practising nursing-licence questions penalises wrong answers the real exam does not; (2) practice uses each question's stored `marks` (mostly 2) even for 1-mark papers — a 10-question Section Officer / NMC / NNC practice set can show max 20 instead of 10. Mocks do override marks correctly (`{...q, marks:p.marksPerQ}` in `startMock()`); practice does not. | `startPractice()`: `negRate: negOn?0.2:0`, questions used as stored. Tagged-question marks mismatches (loaded bank): section-officer 8,388/8,717 tagged Qs are 2-mark vs prelim 1-mark; nrb-officer 775/780; nmc-mbbs 190/297; npc-pharmacy 205/250; nhpc-ha 182/266. Daily/Quick/Surprise always use `negRate:0.2`. |
| F14 | Wrong info | `data/exams.json` `police`, `army`, `health`, `engineering`, `nrb-officer` prelims | Four grouped prelims are placeholders presented as real patterns: `police`/`army`/`health`/`engineering` all show identical **50×2, 45 min, pass 45** with breakdown "GK, IQ, English, Maths (per notice)" / "GK + technical subject (per notice)" — no source in SOURCES.md, EXAM-AUDIT.md or GAP-AUDIT.md supports any of them. GAP-AUDIT already found the Police Inspector GART is actually **50 min, pass 40** (not 45/45). `nrb-officer` (100×1, 90 min, pass 45) is unverified — its `note` says so, but the mock still runs as if real; the other four entries' notes do **not** flag their prelims as unverified. | EXAM-AUDIT.md §3 and GAP-AUDIT.md §3 (both re-confirmed against current `exams.json`). `nrb-officer` note begins "VERIFY BEFORE TRUSTING THE MOCK…"; `police` note is only about physical standards; `health`/`engineering` notes do not mention the prelim at all. |
| F15 | Wrong info | `assets/js/app.js:913` `renderResult()` | The result screen's negative-marking line is hardcoded PSC text for every exam: "Negative marking ON (−0.4 per wrong 2-mark Q, −0.2 per wrong 1-mark Q)". For MECEE-BL the true deduction is −0.25 per wrong 1-mark Q; for 1-mark-only papers (Section Officer, NMC, NNC, NHPC, NEC, Bar, CSIT) the 2-mark half is meaningless. | `renderResult()`: `<p class="muted">Negative marking ${c.negOn?'ON (−0.4 per wrong 2-mark Q, −0.2 per wrong 1-mark Q)':'OFF'} — …` — no per-exam rate or marks in the string. |
| F16 | Wrong info | `README.md:5,47,90,101,126,185`; `loksewa-prep-nepal-full.html` | README and the single-file bundle state stale figures as current: "15,087 MCQs across 47 exams", "15,087 questions in 41 files", "322 fun facts", and "All 6 test suites pass". Reality on disk: **16,850** questions in **46** files, **412** fun facts, and two suites currently fail (F01, F08). The bundle embeds 15,087 Q / 322 facts (test-bundle "PASS" is against the stale bundle — see F40). A visitor trusting the README undercounts the bank by 1,763. | Counts verified by Python over disk (16,850; 46 files incl. `community-approved.json` at 0). `test-bundle.js` output: "loadData loads 15087 questions… 322 loaded". README §Round 6 also says "bank 12,828 → 15,087 is round 5" while claiming round 6 added no questions — true for round 6, stale after round-6 question files landed. |
| F17 | Wrong info | `assets/js/app.js:1169-1225` `renderNotices()` | Notices never expire in code. `renderNotices()` computes `const today=new Date().toISOString().slice(0,10)` and then **never uses it** — status comes only from the static JSON. The two "closing soon" notices (Nepal Police ASI, Gandaki PPSC) close **2026-10-27**; from 2026-10-28 they will still render "Closing soon" with an Apply button until someone hand-edits `notices.json`. (Verified: as of 2026-10-26 nothing is expired-but-marked-open — this is a tomorrow-problem, not a today-error.) | `renderNotices()`: `today` is defined at line ~1199 and referenced nowhere else in the function; filtering/sorting use only `n.status` / `n.close_date`. |
| F18 | Wrong info | `data/exams.json` `nmc-bds.prelim` | NMC-BDS mock claims 180 questions in 180 min, pass 90, as the "shared NMC licensing exam with MBBS" — but the MBBS mock in the same app is 130 MCQs (CSQs excluded). The BDS note admits subject weights are unknown and time is "inferred from the shared MBBS exam — not separately confirmed". An aspirant cannot tell whether the BDS mock is a real paper or a 180-question sample of unknown mix. | `nmc-bds.prelim.breakdown`: "180 objective questions (shared NMC licensing exam with MBBS); BDS subject distribution NOT found". `nmc-mbbs.prelim` is 130Q/180 total. Tagged BDS pool is only 218, so the mock draws 180 of 218 every time (near-deterministic set). |
| F19 | Dead end | `index.html:126-133` (mock table); `index.html` practice section | Before starting, an aspirant can see the pattern for only **5 of 33 mocks** (Kharidar, NaSu, Section Officer, TSC General, NRB Assistant in the static table). The other 28 — every licence/entrance mock — show nothing until **after** Start, when an `alert()` states the pattern. The Practice view shows no pattern at all (no questions/time/marks/pass for the selected exam). An NMC or MECEE aspirant must start a 3-hour mock blind to learn its rules. | Static table has 5 `<tr><td>` rows. `startMock()` pattern disclosure is an `alert()` after `showView('quiz'); renderQuestion();`. Practice card (`index.html` view-practice) has selects + checkboxes only. |
| F20 | Dead end | `assets/js/app.js:869` `skipQ()` | Skip does nothing on the last question: `skipQ()` sets the answer to null then calls `nextQ()`, which is a no-op at the last index. The aspirant taps Skip expecting to finish/leave it blank and nothing visibly happens (no Finish offered by Skip). | `function skipQ(){ current.answers[current.idx]=null; nextQ(); }` + `nextQ()` guards `if(current.idx<current.questions.length-1)`. |
| F21 | Dead end | `assets/js/app.js:1086-1115` `renderGuide()` | The "syllabus view" is a single page of 47 long cards with no per-exam anchor/deep-link, no filter, no search, no table of contents. There is no way to link or jump to "Section Officer syllabus", and the page re-renders all 47 cards on every visit. The cards also carry no topic weightage beyond the one-line prelim breakdown. | `renderGuide()` template emits `<div class="card"><h3>${…}</h3>` with no `id=` per exam and no anchor; `showView('guide')` has no exam parameter. (`startMockFor()` exists for mocks, but there is no `showGuideFor()`.) |
| F22 | Dead end | `assets/js/app.js:484-501` `questionOfDay()`; `:502-541` `renderQotd()`/`answerQotd()` | Question of the Day has two aspirant-facing flaws: (1) options are **not shuffled** — the same question renders identically all day, so the answer position is fixed and shareable/guessable; (2) the question comes from the **whole bank** with no exam scoping — a Kharidar aspirant can get an NHPC Ayurveda or MECEE physics question as "today's question", with no indication it is off-syllabus. | `questionOfDay()` returns `bank[h % bank.length]` with no `shuffleOptions()` call (comment in code says this is deliberate for identical rendering — the tradeoff is not disclosed to the user). `renderQotd()` shows topic/difficulty but no exam tag. |
| F23 | Dead end | `assets/js/app.js:1067` Dashboard reset button (inline `onclick`) | "Reset ALL progress" silently wipes the sign-in identity too: the replacement object omits `user_id`, `email` and `name`. The confirm text says "Reset ALL progress (XP, streak, history)?" — it does not say the profile/name will be removed. After reset, the user is signed out without being told, and the next `saveProgress()` persists a profile-less object until the next load re-migrates a fresh id. | Reset literal: `{xp:0,level:1,streak:0,lastDay:'',attempts:[],bookmarks:[],mistakes:[],flashcardsSeen:0,dailyDone:{},qotdDone:{},weeklyTarget:70,weeklyGoalsMet:0,weeklyGoalMetWeek:'',funFactsSeen:[],focusSessions:0,focusMinutes:0}` — no `user_id`/`email`/`name`. `migrateProgress()` only runs on load. |
| F24 | Dead end | `index.html` nav; `assets/js/app.js` `renderModerate()` | The Maintainer Review queue has **no nav button** — it is reachable only via a small link at the bottom of the Submit page ("Maintainer Review queue (demo)"). A contributor who submitted a question cannot find where it went, and the public moderation log is only on the Submit page. (Separately, the queue itself warns that in demo mode anyone opening the page can approve/reject — that warning is present and correct; the finding here is discoverability only.) | Nav in `index.html` lists 14 `data-view` buttons; `moderate` is not among them. `showView('moderate')` is called only from the Submit page link. |
| F25 | Dead end | `assets/js/app.js:1130-1167` `renderPapers()` | "View Scanned" embeds the paper's **source article page** (not a PDF) in an `<iframe>` for all 14 scanned-only papers (`viewerSrc = p.pdf_url || p.source_url`). Article pages on Blogspot/Bidhya Mandir/Loksewa Sathi routinely send `X-Frame-Options`/CSP that block framing, so the viewer is likely to render blank — the fallback text ("If the preview does not load… open the original") admits this. Cannot be confirmed without a real browser (listed in §"still needs real browser check"). | `renderPapers()`: `<iframe src="${esc(viewerSrc)}" …>` where `viewerSrc` is `source_url` whenever `pdf_url` is null (14 of 17 papers). Only the 3 transcribed papers have a real `pdf_url`. |
| F26 | UX friction | `assets/js/app.js:31-50` `setLang()` | The EN/NE toggle persists (localStorage `loksewa_lang` — good) but re-renders only quiz/flash/review/result/funfacts/home/search. Guide, Papers, Notices, Dashboard, Profile, Discuss and Submit keep their English chrome; the Practice view's labels stay English. The toggle is sold as a language switch; it is really a question-text switch. (README's roadmap already admits "Full Nepali UI toggle" is future work — the toggle button itself does not say that.) | `setLang()` if/else chain covers 7 view ids; `view-guide`, `view-papers`, `view-notices`, `view-dashboard`, `view-profile`, `view-discuss`, `view-submit`, `view-practice` are absent. |
| F27 | UX friction | `assets/js/app.js:1012-1019` `dailyChallenge()` | Daily Challenge writes `progress.dailyDone[seed]=true` but **nothing ever reads `dailyDone`** — there is no "already done today" state, no distinct reward, and the same seeded 10-question set can be re-run unlimited times for XP each run (XP is awarded per finished attempt). The "daily" in Daily Challenge is unenforced. | Grep: `dailyDone` appears only at load-migration (`:102`) and the write in `dailyChallenge()`. No read anywhere in `app.js`. |
| F28 | UX friction | `assets/js/app.js:981` `newRandomSet()` | "🔀 New random set" on the result screen ignores the exam just finished and starts practice with whatever the Practice-view exam select currently holds (default Kharidar). An NRB aspirant who just finished an NRB mock and taps "New random set" gets a Kharidar set. | `function newRandomSet(){ showView('practice'); startPractice(); }` — `startPractice()` reads `document.getElementById('practice-exam').value`, never `current.exam`. |
| F29 | UX friction | `assets/js/app.js:1026-1034` `startFlashcards()` | Flashcards draw 20 random questions from the **whole bank** with no exam/topic filter. A Kharidar aspirant's revision deck can be NHPC, Bar Council and MECEE questions. Same unscoped-bank issue as F22/F09 (different surface, same root: no "current exam" concept outside Practice/Mock). | `startFlashcards()`: `flashQs=shuffle(QUESTIONS).slice(0,20)` — no exam/topic parameter; the Flashcards card on Home has no filter UI. |
| F30 | UX friction | `assets/js/app.js:189-201` `startSpeedRound()`; `index.html` Home/Practice buttons | Speed Round gives no pre-start rules card: the 60-second total clock, +1 bonus under 5s, no-Previous/no-change-answer and no per-question feedback are only discoverable mid-round (the in-quiz line does state the clock/bonus; the no-going-back rule is not stated anywhere before or during). An aspirant who taps an answer by accident cannot correct it and is not warned. | Home/Practice buttons read only "⏱️ Speed Round (10 Q · 60s)". `renderQuestion()` in speed mode hides Previous/Bookmark/Report/Discuss buttons with no explanation. |
| F31 | UX friction | Whole bank (heuristic scan) | Data-quality signals that need human review, **not** proven defects: (a) **1,807** questions where the correct option is ≥1.8× the longest other option and ≥40 chars — a "longest-option-is-correct" giveaway pattern (spot-checked examples are mostly long correct definitions, e.g. LAW6-012's full Act name vs short distractors, so the true giveaway count is lower); (b) **1,085** explanations under 30 characters; (c) **197** explanations that merely restate the correct option (e.g. POL-016's explanation is just the answer text again); (d) **846** `question_ne` identical to the English question and **4,059** `options_ne` identical to options — mostly legitimate (English idioms, formulae, numbers, proper nouns), but unreviewed in bulk. | Whole-bank Python scan (16,850 Qs). Counter-examples: LAW6-012 correct option is legitimately the full Act name; ENGV3-171–195 idiom questions legitimately keep English in `question_ne`. Do not bulk-"fix" these by script; sample-review them. |
| F32 | UX friction | Sampled questions | Nepali explanation quality is uneven: `IQ3-137` — EN explanation explains ("The father of Gita's father is Gita's grandfather") but NE says only "सम्बन्धको श्रृङ्खला पछ्याएर उत्तर पत्ता लगाउनुहोस्।" (follow the chain — no answer); `CURH-208` — both explanations are tautological ("Law of gravitation — Law of gravitation means…", NE ends with the ungrammatical "…आकर्षि… गर्छ हो।"); `COMP-053` — `options_ne` drops the dots (`mp3`, `mp4` vs `.mp3`, `.mp4`), so the NE options differ from the EN ones. | Full records in the sample section of this audit's working notes (see Method — 45-question sample, seed 20261026). `CULT2-126` also shows a mojibake-adjacent NE rendering ("पकाइएक�� मिठाई") — verify: no U+FFFD was found bank-wide, so this is likely a display artefact of the sample dump, listed here only as "check in browser", not as a confirmed defect. |
| F33 | UX friction | `assets/css/style.css`; `index.html:126` | Mobile (360 px) niggles, from code reading only: (1) the Mock-view 5-column table and all Guide tables have **no horizontal-scroll wrapper** — `table{width:100%}` with no `overflow-x` container (`style.css` has `overflow` only for modal/progress/confetti/header-nav); (2) the MECEE mock palette renders **200** 44 px buttons in one wrapping block; (3) the Practice timer/negative checkboxes are native-size (<44 px) — mitigated because the wrapping `<label>` text is tappable. Positives: `.opt` is 52 px on mobile, palette buttons are 44 px, bottom nav is 52 px, header nav scrolls horizontally. | `style.css` grep for `overflow`: only `.modal-card`, `.progress-bar`, `.session-bar`, `#confetti-layer`, `header nav`. No `.table-wrap` / `overflow-x:auto` on tables. |
| F34 | UX friction | `index.html` modal; `assets/js/app.js` `openReportForm()`/`closeModal()` | The Report-wrong-question modal can only be closed with its Cancel button — no Esc key, no backdrop click. Small, but it is a modal over a quiz the aspirant may be mid-way through. | `#modal` has no click handler and no keydown handler in `app.js`; only `closeModal()` (sets `hidden=true`) wired to Cancel / successful submit. |
| F35 | Polish | `assets/js/app.js:913` `renderResult()` | TSC Teaching Licence result reads "Negative marking OFF — " with a dangling dash and empty second clause, because the template is `${c.negOn?'exactly like PSC.':''}`. | `renderResult()`: `<p class="muted">Negative marking ${c.negOn?'ON (…)':'OFF'} — ${c.negOn?'exactly like PSC.':''}</p>`. |
| F36 | Polish | `index.html` Home trending card #3 + footnote | Trending card #3 "Most-asked GK ★" practices topic **Nepal History** — the label promises most-asked GK, the button delivers one slice of it. The footnote "★ New set in progress — practising the closest topic for now" is attached to the whole grid, so it is unclear which cards are placeholders. | `onclick="startPracticeTopic('Nepal History')"` on the "Most-asked GK ★" card. Compare card #5, which correctly maps "Kharidar Office Skills" → 'Office Management & Public Service'. |
| F37 | Polish | `assets/js/app.js` `doSearch()` | Search caps at 50 results with no pagination and no total-match count beyond "N result(s) of 15,087" — an aspirant searching "Constitution" cannot reach results 51+. | `doSearch()`: `.slice(0,50)`; result line is `${res.length} result(s)${QUESTIONS.length?` of ${QUESTIONS.length}`:''}.` |
| F38 | Polish | `assets/js/app.js:767-778` `startPractice()` | Practice timer is a flat **54 s/question** for every exam, including TSC Teaching Licence — whose mock is deliberately untimed because its time limit is unverified. A licence aspirant practising with a 45-minute timer is training against an invented limit. | `startPractice()`: `timeLeft=qs.length*54` whenever the timer checkbox is on, with no per-exam time. (MECEE 200Q → 180 min happens to match; Kharidar/NaSu 50Q → 45 min matches; TSC Licence 50Q → 45 min does not match anything verified.) |
| F39 | Polish | `data/exams.json` `staff-nurse-psc.prelim.negative: 0.4` vs all others | `negative` stores **inconsistent units**: every exam stores a rate (0.2, 0.25, 0, null) except Staff Nurse, which stores **0.4** — absolute marks deducted per wrong 2-mark question (i.e. still a 20% rate). `mockNegRate()` special-cases it correctly today (any non-zero → 0.2), but the next editor to read `0.4` will reasonably conclude Staff Nurse deducts 40%. | `test-app.js:40` asserts `mockNegRate({negative:0.4}) === 0.2` with the comment "marks per wrong 2-mark Q". No other exam uses absolute marks. |
| F40 | Polish | `scripts/test-bundle.js`; `loksewa-prep-nepal-full.html` (built 2026-10-26 05:16) | `test-bundle.js` PASSES — but it tests the stale single-file bundle, which embeds 15,087 questions / 322 fun facts. The green tick certifies an artefact that no longer matches the repo. The bundle must be rebuilt after the round-6 files land (F01) or the test is meaningless. | `test-bundle.js` output: "loadData loads 15087 questions from embedded data — 15087 loaded", "fun facts … 322 loaded". Bundle mtime predates the round-6 question files. (Do NOT rebuild it in this audit — forbidden by task; the coordinator rebuilds after applying F01.) |

## Fix specs (mechanical — apply without re-reading)

Each spec gives exact file, exact current code/text, exact replacement. Line numbers are from the audited state; if round-6 shifted lines, match on the quoted text.

### F01 — load the round-6 question files

- **File:** `assets/js/app.js:4`
- **Current:** `const QUESTION_FILES = ['constitution-governance-economy.json',…,'expansion-r5-maths-hard.json','expansion-security-engineering.json',…,'tsc-education.json'];` (41 entries, ending `…'previous-year-2083.json','tsc-education.json'];`)
- **Replacement:** insert the four round-6 files in alphabetical order (the list is alphabetical; `test-app.js` compares sorted order): after `'expansion-r5-maths-hard.json',` insert `'expansion-r6a-thin-exams.json','expansion-r6b-banking-health.json','expansion-r6b-language.json','expansion-r6b-licence-entrance.json',` — i.e. the segment becomes `…'expansion-r5-law.json','expansion-r5-maths-hard.json','expansion-r6a-thin-exams.json','expansion-r6b-banking-health.json','expansion-r6b-language.json','expansion-r6b-licence-entrance.json','expansion-security-engineering.json',…`.
- **Then:** rebuild the bundle (`node scripts/build-bundle.py` — coordinator only, not this audit) and update README counts (see F16). Verify with `node scripts/test-app.js` (the QUESTION_FILES check must go green) and confirm Home shows 16,850.

### F02 — HEAL2-182 wrong answer

- **File:** `data/questions/expansion-health-technical-security.json:5071`
- **Current:** `"id": "HEAL2-182", … "options": ["BCG", "OPV", "Measles", "DPT"], "answer": 2,`
- **Replacement:** `"answer": 0,` (BCG). Explanation already correct; no other change.

### F03 — HARD2-298 wrong answer + duplicate options

- **File:** `data/questions/expansion-hard-core-v2.json:8913`
- **Current:** `"options": ["10 years (alt)", "12 years", "10 years", "20 years"], "answer": 3,` and the same four strings in `options_ne` (`["१० वर्ष (alt)", "१२ वर्ष", "१० वर्ष", "२० वर्ष"]`).
- **Replacement:** `"options": ["10 years", "12 years", "8 years", "20 years"], "answer": 0,` and `"options_ne": ["१० वर्ष", "१२ वर्ष", "८ वर्ष", "२० वर्ष"]`. (10 is correct per the explanation's own equation; the near-duplicate "10 years (alt)" is replaced with a fresh plausible distractor "8 years" so all four options are distinct. Do NOT just delete an option — the schema requires exactly 4.)
- **Validator gap (folded in, no separate ID):** `scripts/test-questions.js` duplicate-option check is exact-match only. Add a normalised check that strips a trailing ` (alt)` / parenthetical before comparing options, or flag any option containing `(alt)` as a failure. Suggested check text: treat two options as duplicates when `normalise(o1) === normalise(o2)` after removing `/\s*\(.*?\)\s*$/`.

### F04 — MECEE negative marking 25%, not 20%

- **File:** `assets/js/app.js:656`
- **Current:** `function mockNegRate(p){ return (p.negative === null || p.negative === 0) ? 0 : 0.2; }`
- **Replacement:** `function mockNegRate(p){ if (p.negative === null || p.negative === 0) return 0; if (p.negative === 0.4) return 0.2; return p.negative; }` (0.4 is Staff Nurse's absolute-marks encoding of a 20% rate — see F39; every other non-zero value is already a rate, so return it. This makes MECEE 0.25 → 0.25.)
- **Also fix the comment directly above it** (lines ~652–655): current text says "Staff Nurse stores 0.4 — marks deducted per wrong 2-mark question — which is also a 20% rate." Append: "MECEE-BL stores 0.25 (rate). mockNegRate returns the stored rate, except 0.4 which is Staff Nurse's absolute-marks encoding of 20%."
- **Also fix the quiz header** in `renderQuestion()` (same file, ~line 815): current `"${c.negOn?'(−20% if wrong)':''}"` → replace with a computed string: `const negLabel = c.negOn ? `(−${Math.round(c.negRate*100)}% if wrong)` : '';` and use `${negLabel}`. (This also fixes F15's header half.)
- **Test:** add to `scripts/test-app.js` near line 40: `check('mockNegRate: MECEE negative 0.25 → 0.25', mockNegRate({ negative: 0.25 }) === 0.25);`

### F05 — save mock wrong answers to Mistakes

- **File:** `assets/js/app.js:837-860` (`answerOption()`)
- **Current:** `if(c.mode==='practice'){ showFeedback(); saveMistakeIfWrong(); }` (and the speed-mode early return above it, which never saves).
- **Replacement:** change the block to:
```js
  if(c.mode==='practice'){ showFeedback(); saveMistakeIfWrong(); }
  if(c.mode==='mock'){ saveMistakeIfWrong(); }
```
  (`saveMistakeIfWrong()` already dedupes via `progress.mistakes.includes(q.id)` and works for any mode — it only reads `current`/`progress`. Do NOT call it for speed mode: speed answers are given under a 60 s clock and a wrong speed tap is not a knowledge gap; keep speed out.)
- **Also:** in `finishAttempt()` the in-memory `current._wrong` is the only retry source. No change needed once F05 lands (Mistake Marathon covers it), but note in the result screen that mock mistakes are now in Bookmarks & Mistakes — the existing copy already says "Wrong answers are saved automatically" on Home; it becomes true for mocks too.

### F06 — stop the timer when leaving a quiz

- **File:** `assets/js/app.js:639-654` (`showView()`)
- **Current:** `function showView(id){ document.querySelectorAll('.view').forEach(v=>v.classList.remove('active')); …`
- **Replacement:** add as the first line of `showView()`, before the view switch:
```js
  // Leaving a timed quiz abandons it: stop the countdown so it cannot
  // auto-submit while the user is on another view. The attempt is NOT
  // recorded (finishAttempt is never called for an abandoned quiz).
  if (id !== 'quiz' && id !== 'result') clearInterval(timerId);
```
  (Keep the timer running for `quiz`→`result` transitions, which `finishAttempt()` itself drives; `finishAttempt()` already clears the timer. Do NOT clear on `showView('quiz')` — every quiz entry point calls `startTimer()` itself after setting `timeLeft`.)

### F07 — don't serve the whole bank as a guide-only exam's practice

- **File:** `assets/js/app.js:759-766` (`filteredQuestions()`)
- **Current:**
```js
  let pool=QUESTIONS.filter(q=> (!topic||q.topic===topic) && (!diff||q.difficulty===diff) && (!exam||q.exam.includes(exam)));
  if(!pool.length) pool=QUESTIONS.filter(q=>!topic||q.topic===topic);
  return pool;
```
- **Replacement:**
```js
  let pool=QUESTIONS.filter(q=> (!topic||q.topic===topic) && (!diff||q.difficulty===diff) && (!exam||q.exam.includes(exam)));
  return pool;
```
  (Delete the fallback line entirely.)
- **File:** `assets/js/app.js:767-778` (`startPractice()`), current `if(!qs.length){ alert('No questions loaded yet — run via a local server and try again.'); return; }`
- **Replacement:** `if(!qs.length){ alert(exam ? 'No questions tagged for this exam yet — try another exam, or a topic instead.' : 'No questions loaded yet — run via a local server and try again.'); return; }` — `exam` is already in scope in `startPractice()`.
- **File:** `assets/js/app.js` (`fillExamSelects()`, ~line 700): current `const allOpts=EXAMS.map(e=>`<option value="${e.id}">${esc(e.name)}</option>`).join('');` used for the practice select. **Replacement:** `const allOpts=EXAMS.map(e=>`<option value="${e.id}">${esc(e.name)}${e.prelim?'':' — guide only, no practice questions'}</option>`).join('');` — keeps the exams selectable (some guide-only exams DO have tagged questions, e.g. `rbb`, `nhpc-dental`) while labelling the empty ones. Do not remove guide-only exams from the select: `nhpc-dental`/`nhpc-ayurveda`/`rbb` practice is legitimate.
- **Data note (no code change):** the 0-tagged practice exams are `deputy-secretary`, `jta`, `ranger`, `judicial-service`, `psc-service-groups`, `rbb-senior-assistant`, `provincial-psc`, `nea`, `anm-guide`, `ayurveda-bams`. After this fix, picking one with no topic filter shows the honest alert instead of a fake set.

### F08 — remove the 31 duplicate question texts

- **Files:** `data/questions/*.json` (list from `node scripts/test-questions.js` output — rerun it to get the exact current list; it changes as round-6 edits land).
- **Rule, per pair:** keep the **older** question (the non-`R6A-`/`R6B-` id where one side is round-6; otherwise keep the first file alphabetically) and delete the other object from its file. Do NOT renumber or edit the kept copy. Verify with `node scripts/test-questions.js` → `FAILURES (0)`.
- **Known pairs to start from** (from the audited run): `CONST-202` keep, delete `R6A-A484`; `LAB-038` keep, delete `R6A-A297`; `LAB-059` keep, delete `R6A-A411`; `RAD-001` keep, delete `R6A-A155`; `RAD-009` keep, delete `R6A-A159`; `RAD-031` keep, delete `R6A-A163`; `RAD-062` keep, delete `R6A-A161`; `RAD-067` keep, delete `R6A-A195`; plus `BDS-013` (in `expansion-zero-licence.json`), `ALLIED-092` (`license-allied-health.json`), `NUR-085` (`license-nursing.json`) — for these three, find the other copy with the same normalised text in the validator output and delete the newer/later one. The remaining ~17 duplicates are all in `expansion-r6a-thin-exams.json` (`R6A-A276`, `R6A-A281`, `R6A-A282`, `R6A-A332`, `R6A-A348`, `R6A-A349`, `R6A-A351`, `R6A-A356`, `R6A-A359`, `R6A-A362`, `R6A-A364`, `R6A-A371`, `R6A-A485`, `R6A-A506`, …) — delete the `R6A-` copy in each pair (the other copy is the original).

### F09 — cap Speed Round score; stop hardcoding `exam:'kharidar'`

- **File:** `assets/js/app.js:874-911` (`finishAttempt()`), speed-bonus block.
- **Current:** `res.speedBonus=bonus; res.score=Math.round((res.score+bonus)*10)/10; res.pct=res.max?Math.min(100, Math.round((Math.max(res.score,0)/res.max)*1000)/10):0;`
- **Replacement:** `res.speedBonus=bonus; res.score=Math.min(res.max, Math.round((res.score+bonus)*10)/10); res.pct=res.max?Math.min(100, Math.round((Math.max(res.score,0)/res.max)*1000)/10):0;` (cap the score at `max`, like pct already is; keep `speedBonus` recorded separately so the bonus is still visible.)
- **File:** `assets/js/app.js` — `dailyChallenge()` (~:1012), `quickQuiz()` (~:1020), `surpriseQuiz()` (~:175), `startSpeedRound()` (~:189), `startMistakeMarathon()` (~:203). **Current** in each: `exam:'kharidar',` inside the `current={…}` literal. **Replacement:** `exam:'',` in all five, plus one guard in `finishAttempt()`: current `const cutoffPct=(examObj && examObj.prelim)? Math.round(examObj.prelim.pass/examObj.prelim.total*100) : 45;` already defaults to 45 when there is no exam object — that stays correct for mixed sets. And in `renderResult()`, current `${esc(examById(c.exam)?.name||c.exam)}` renders an empty string for `''` — **replacement:** `${esc(c.title || examById(c.exam)?.name || 'Mixed practice')}` (all five modes already set a `title` except daily/quick — give them one: in `dailyChallenge()` add `title:'🔥 Daily Challenge',` to the `current` literal; in `quickQuiz()` add `title:'⚡ Quick Quiz',`). Dashboard history then shows the mode/title instead of a false "Kharidar".
- **Note:** `startMistakeMarathon()` and `startSpeedRound()` already set `title:` — only add titles to daily/quick.

### F10 — make mocks follow the prelim topic mix

- **File:** `assets/js/app.js:984-1011` (`startMock()`).
- **Current:** `let pool=QUESTIONS.filter(q=>q.exam.includes(examId)); const tagged=pool.length; if(pool.length < p.questions) pool=QUESTIONS.slice(); const qs=shuffle(pool).slice(0, p.questions).map(q=>shuffleOptions({...q, marks:p.marksPerQ}));`
- **Replacement (mechanical, no new data model):** parse the mix from `p.breakdown` only where it is machine-readable, and fall back to today's uniform draw otherwise. Minimum viable fix that fixes the worst case (Kharidar/NaSu/Section Officer/NRB):
  1. Add a helper above `startMock()`:
```js
// Topic-mix for the four prelims whose breakdown is a plain "Topic N Q + Topic M Q"
// count. Returns {topic: count} or null when the breakdown is not parseable
// (percentages, prose, or licence weight tables) — callers fall back to a
// uniform draw from the tagged pool.
function mockMixFor(e){
  const b=(e.prelim&&e.prelim.breakdown)||'';
  const m={};
  if(e.id==='kharidar'){ m['Office Management & Public Service']=20; }
  else if(e.id==='nasu'){ m['IQ & Reasoning']=20; }
  else if(e.id==='section-officer'){ m['English']=20; }
  else if(e.id==='nrb-assistant'){ /* Mgmt/Acct+Econ/Banking are not topics; fall through */ return null; }
  else return null;
  return m;
}
```
  2. In `startMock()`, after the `pool`/`tagged` lines, insert:
```js
  const mix=mockMixFor(e);
  let qs;
  if(mix){
    const rest=QUESTIONS.filter(q=>q.exam.includes(examId));
    const picked=[];
    for(const [topic,n] of Object.entries(mix)){
      picked.push(...shuffle(rest.filter(q=>q.topic===topic)).slice(0,n));
    }
    const used=new Set(picked.map(q=>q.id));
    picked.push(...shuffle(rest.filter(q=>!used.has(q.id))).slice(0, p.questions-picked.length));
    qs=shuffle(picked).map(q=>shuffleOptions({...q, marks:p.marksPerQ}));
  } else {
    qs=shuffle(pool).slice(0, p.questions).map(q=>shuffleOptions({...q, marks:p.marksPerQ}));
  }
```
  and delete the old `const qs=shuffle(pool)…` line. (Kharidar: 20 Office + 30 others from the tagged pool; NaSu: 20 IQ + 30 others; Section Officer: 20 English + 80 others. NRB and all licence/entrance mocks keep the uniform draw until their breakdowns are modelled as topics — do NOT invent topic mappings for them.)
- **Honesty fix (same finding, `index.html` Mock section):** current `<p class="muted">Full-length, timed, exactly like the real prelim: same question count, same time, same marks, 20% negative marking, auto-submit when time runs out, result judged against the real cutoff.</p>` → **replacement:** `<p class="muted">Full-length, timed, like the real prelim: same question count, same time, same marks, auto-submit when time runs out, result judged against the real cutoff. Question mix follows the real paper's section split where the app models it (Kharidar, NaSu, Section Officer); other mocks draw from the exam's tagged pool. Negative marking is per exam — see the Exam Guide.</p>`

### F11 — NMC-MBBS result must not compare a 130-mark score with a 180-mark cutoff

- **File:** `assets/js/app.js:913` (`renderResult()`).
- **Current:** `<div><strong class="${passed?'pass':'fail'}">${passed?'✅ PASS':'❌ FAIL'}</strong> — cutoff for this exam is ${cutoffPct}% (${cutoff}/${examObj && examObj.prelim?examObj.prelim.total:100} on the full paper) &nbsp;·&nbsp; ${res.pct}%</div>`
- **Replacement:** compute before the template (insert above `box.innerHTML=`): `const cutoffNote = (examObj && examObj.prelim && examObj.prelim.total !== res.max) ? ` (mock covers ${res.max} of ${examObj.prelim.total} marks — the 10 clinical scenario questions are not in this mock; pass is judged on percentage, not on ${cutoff} raw marks)` : '';` and change the div to `… — cutoff for this exam is ${cutoffPct}% (${cutoff}/${examObj && examObj.prelim?examObj.prelim.total:100} on the full paper)${cutoffNote} &nbsp;·&nbsp; ${res.pct}%</div>`. (Generic: it triggers for any exam whose mock max differs from `prelim.total` — today only NMC-MBBS.)
- **Data alternative (coordinator's choice, not both):** set `nmc-mbbs.prelim.total` to 130 and add a `note` that the real total is 180 with CSQs. If that is chosen instead, the code change above is unnecessary — but then `cutoffPct` becomes 90/130 = 69%, which is WRONG (pass is 50% of 180). So prefer the code change; do not change `total` to 130.

### F12 — label the MECEE pass as a proxy on the result screen

- **File:** `assets/js/app.js:913` (`renderResult()`).
- **Current:** same cutoff div as F11.
- **Replacement:** add above `box.innerHTML=`: `const proxyNote = (c.exam==='mecee-bl') ? ' — the real MECEE-BL pass is the 50th percentile (merit rank), not 50% marks; this is a rough proxy only' : '';` and append `${proxyNote}` inside the cutoff div after `${cutoffNote}` (or after the cutoff text if F11 is not applied). Text must read exactly: `the real MECEE-BL pass is the 50th percentile (merit rank), not 50% marks; this is a rough proxy only`.

### F13 — practice must use the exam's marks and negative rule

- **File:** `assets/js/app.js:767-778` (`startPractice()`).
- **Current:** `current={ mode:'practice', exam, questions:qs, answers:Array(qs.length).fill(null), idx:0, negOn, negRate: negOn?0.2:0, timerOn, startTime:Date.now(), perQ:[] };`
- **Replacement:**
```js
  const examObj=examById(exam);
  const examNeg=examObj&&examObj.prelim ? mockNegRate(examObj.prelim) : 0.2;
  const examMarks=examObj&&examObj.prelim ? examObj.prelim.marksPerQ : null;
  const normQs=qs.map(q=> examMarks!=null ? {...q, marks:examMarks} : q);
  current={ mode:'practice', exam, questions:normQs, answers:Array(normQs.length).fill(null), idx:0, negOn: negOn && examNeg>0, negRate: negOn?examNeg:0, timerOn, startTime:Date.now(), perQ:[] };
```
  and change the timer line `if(timerOn){ timeLeft=qs.length*54; …}` to use `normQs.length` (same number; keep the line otherwise). Effect: NNC/NHPC/NEC/Bar/CSIT practice never deducts (their `negative` is 0 → `negOn` false even if the checkbox is ticked — see also the checkbox-label fix below); 1-mark papers practise at 1 mark/question.
- **File:** `index.html` practice section, current: `<label><input type="checkbox" id="practice-neg" checked> Negative marking (−20%, like PSC)</label>` → **replacement:** `<label><input type="checkbox" id="practice-neg" checked> Negative marking (per exam — 20% on PSC papers, none on licence papers)</label>`.
- **Also** `dailyChallenge()`/`quickQuiz()`/`surpriseQuiz()`: they are mixed-bank sets with no exam — leave `negRate:0.2` as is (mixed sets have no single exam rule); no change.

### F14 — flag the placeholder prelims honestly

- **File:** `data/exams.json` — four entries. Add/extend the `note` field (exact replacement text per entry; keep the rest of each note, appending this sentence):
  - `police`: append ` "Prelim pattern UNVERIFIED: 50×2, 45 min, pass 45 is a placeholder — the Police Inspector GART is 50 min, pass 40 per GAP-AUDIT §1. Verify per vacancy notice before trusting this mock."`
  - `army`: append ` "Prelim pattern UNVERIFIED: 50×2, 45 min, pass 45 is a placeholder. Verify per vacancy notice before trusting this mock."`
  - `health`: append ` "Prelim pattern UNVERIFIED: 50×2, 45 min, pass 45 is a generic placeholder shared across all Health Service posts. Verify per vacancy notice before trusting this mock."`
  - `engineering`: append ` "Prelim pattern UNVERIFIED: 50×2, 45 min, pass 45 is a generic placeholder. Verify per vacancy notice before trusting this mock."`
- **No change** to `nrb-officer` (its note already flags it) or to the mock behaviour itself — the coordinator may later split Police Inspector into its own mock (GART 50 min/pass 40); that is a bigger change and is listed under "missing aspirant needs", not here.

### F15 — result screen negative-marking line per exam

- **File:** `assets/js/app.js:913` (`renderResult()`).
- **Current:** `<p class="muted">Negative marking ${c.negOn?'ON (−0.4 per wrong 2-mark Q, −0.2 per wrong 1-mark Q)':'OFF'} — ${c.negOn?'exactly like PSC.':''}</p>`
- **Replacement:** compute above `box.innerHTML=`:
```js
  const negLine = !c.negOn ? 'Negative marking OFF — this exam has no negative marking.'
    : `Negative marking ON (−${(c.negRate*(c.questions[0]?.marks||1)).toFixed(2).replace(/0$/,'')} per wrong question, ${Math.round(c.negRate*100)}%)`;
```
  and replace the `<p>` with `<p class="muted">${negLine}</p>`. (For a 2-mark PSC paper this renders "−0.4 per wrong question, 20%"; for MECEE "−0.25 per wrong question, 25%" once F04 lands. The `.replace(/0$/,'')` trims "0.40" to "0.4".) This also fixes F35's dangling dash — delete the old trailing `— ${…}` construction entirely.

### F16 — README + bundle counts

- **File:** `README.md:5` — current `**15,087 MCQs across 47 exams**` → replacement `**16,850 MCQs across 47 exams**` (recompute after F01/F08 land; if duplicates are removed the number drops — use the post-fix `test-questions.js` total).
- **File:** `README.md:47` — current `every one of the 15,087 questions has a Nepali translation` → same number as above.
- **File:** `README.md:90` — current `Question bank — 15,087 MCQs in 41 files` → `Question bank — 16,850 MCQs in 45 files` (45 bank files + `community-approved.json`; recompute post-fix).
- **File:** `README.md:101,126` — update the bank table + total row with the four round-6 files and their counts (566 + 269 + 380 + 548) and the new total; add a Round 6b line to the roadmap (or amend the Round 6 line — do not leave "bank 12,828 → 15,087 is round 5" as the latest figure).
- **File:** `README.md:185` — current `All 6 test suites pass (…)` → replacement `All 6 test suites pass (…)` ONLY once they do; until F01/F08 are fixed, replace with `5 of 6 test suites pass — test-app and test-questions currently fail on the unlisted round-6 files and 31 duplicate texts (see data/SELF-AUDIT-2026-10-26.md).`
- **File:** `README.md` fun-facts mentions — current `322 verified fun facts` (appears in the Fun Facts bullet and Round 6 line) → `412 verified fun facts`.
- **Bundle:** rebuild with `node scripts/build-bundle.py` AFTER F01 lands (coordinator only). Verify `test-bundle.js` then reports 16,850 questions / 412 facts.

### F17 — notices must expire by date at render time

- **File:** `assets/js/app.js:1169-1225` (`renderNotices()`).
- **Current:** `const today=new Date().toISOString().slice(0,10);` (unused) and `let list=NOTICES.filter(n=>(!fScope||n.scope===fScope)&&(!fBody||n.issuer===fBody)&&(!fStatus||n.status===fStatus));`
- **Replacement:** insert directly after the `today` line:
```js
  const effStatus=n=> (n.close_date && n.close_date < today && (n.status==='open'||n.status==='closing-soon')) ? 'closed' : n.status;
```
  and change the filter to use it: `let list=NOTICES.filter(n=>(!fScope||n.scope===fScope)&&(!fBody||n.issuer===fBody)&&(!fStatus||effStatus(n)===fStatus));` and the counts block `NOTICES.forEach(n=>{ if(counts[n.status]!=null) counts[n.status]++; });` → `NOTICES.forEach(n=>{ const s=effStatus(n); if(counts[s]!=null) counts[s]++; });` and the card label `esc(NOTICE_STATUS_LABEL[n.status]||n.status)` → `esc(NOTICE_STATUS_LABEL[effStatus(n)]||effStatus(n))`. The JSON stays the source of truth; the render only ever flips open/closing-soon → closed past the deadline, never the reverse.

### F18 — NMC-BDS mock honesty

- **File:** `data/exams.json`, `nmc-bds` entry.
- **Current note** (abridged): `"Only totals verified (180 Q, 90 to pass…). Time 3h inferred from the shared MBBS exam — not separately confirmed for BDS. Negative marking unverified. BDS subject weights unknown…"`.
- **Replacement:** append to that note: `" This mock draws 180 questions from a 218-question tagged pool of unknown subject mix — it does not mirror the real BDS paper's sections."` No code change. (If the coordinator later verifies the BDS paper is NOT 180 standalone MCQs, the prelim itself must change — human research, see "still needs real browser / human check".)

### F19 — show the pattern before starting a mock / practice

- **File:** `index.html:126-133` (mock table).
- **Current:** static 5-row table (Kharidar, NaSu, Section Officer, TSC General, NRB Assistant).
- **Replacement:** replace the whole `<div style="margin-top:14px"><table>…</table></div>` with `<div style="margin-top:14px" id="mock-pattern-table"><p class="muted">Loading mock patterns…</p></div>` and add a `renderMockTable()` in `app.js` (called from `loadData()` after `fillExamSelects()` and from `renderMockBest()`'s neighbourhood — simplest: call it at the end of `loadData()` next to `renderMockBest()`):
```js
function renderMockTable(){
  const box=document.getElementById('mock-pattern-table'); if(!box) return;
  const rows=EXAMS.filter(e=>e.prelim).map(e=>{ const p=e.prelim;
    const neg=p.negative===null?'unverified':(p.negative===0?'none':Math.round((p.negative===0.4?0.2:p.negative)*100)+'%');
    return `<tr><td>${esc(e.name)}</td><td>${p.questions}</td><td>${p.timeMin==null?'—':p.timeMin+' min'}</td><td>${p.marksPerQ}</td><td>${p.pass}</td><td>${neg}</td></tr>`; }).join('');
  box.innerHTML=`<table><tr><th>Mock</th><th>Questions</th><th>Time</th><th>Marks/Q</th><th>Pass</th><th>Negative</th></tr>${rows}</table>`;
}
```
  (33 rows, generated from `exams.json` — no hand-maintained table to go stale. Keep the existing `renderMockBest()` call site; add `renderMockTable();` next to it in `loadData()`.)
- **Practice view (`index.html`, view-practice card):** add under the Start button (after the `<button class="btn" onclick="startPractice()">…` line): `<p class="muted" id="practice-pattern"></p>` and in `app.js` `fillExamSelects()` append: `const pp=document.getElementById('practice-pattern'); const upd=()=>{ const e=examById(document.getElementById('practice-exam').value); if(pp) pp.textContent=e&&e.prelim?`${e.name}: ${e.prelim.questions} questions × ${e.prelim.marksPerQ} mark(s), ${e.prelim.timeMin==null?'time unverified':e.prelim.timeMin+' min'}, pass ${e.prelim.pass}/${e.prelim.total}.`:'Guide-only exam — no MCQ paper; practice draws from tagged questions only.'; }; const pe=document.getElementById('practice-exam'); if(pe) pe.addEventListener('change',upd); upd();` — the pattern is then visible before Start, and updates when the exam changes.

### F20 — Skip on the last question

- **File:** `assets/js/app.js:869`
- **Current:** `function skipQ(){ current.answers[current.idx]=null; nextQ(); }`
- **Replacement:** `function skipQ(){ current.answers[current.idx]=null; if(current.idx<current.questions.length-1) nextQ(); else renderQuestion(); }` (re-render so the cleared answer is visible; the Finish button is already shown on the last question.)

### F21 — per-exam guide anchors + filter

- **File:** `assets/js/app.js:1086-1115` (`renderGuide()`).
- **Current:** `` return `<div class="card"><h3>${esc(e.name)} …` ``
- **Replacement:** `` return `<div class="card" id="guide-${e.id}"><h3>${esc(e.name)} …` `` and, directly above `box.innerHTML=EXAMS.map(…`, insert a filter row: `const filterHtml=`<p><label for="guide-filter">Find an exam</label><input type="search" id="guide-filter" placeholder="e.g. Kharidar, Nursing, Bar…" oninput="filterGuide(this.value)"></p>`;` and set `box.innerHTML=filterHtml+EXAMS.map(…).join('');`. Add above `renderGuide()`:
```js
function filterGuide(term){
  const t=(term||'').toLowerCase();
  document.querySelectorAll('#guide-box .card').forEach(c=>{ c.style.display = (!t || c.textContent.toLowerCase().includes(t)) ? '' : 'none'; });
}
function showGuideFor(id){ showView('guide'); const el=document.getElementById('guide-'+id); if(el) el.scrollIntoView(); }
```
  (Deep-linking via `#guide-<id>` URL hash is a follow-up; anchors + filter fix the dead end.)

### F22 — QOTD: shuffle options, scope the pool

- **File:** `assets/js/app.js:484-501` (`questionOfDay()`).
- **Current:** `return bank[h % bank.length];` with the comment "Options are NOT shuffled here — the same question must render identically on every visit".
- **Replacement:** keep determinism but shuffle deterministically from the date seed:
```js
function questionOfDay(questions, dateStr){
  const bank = questions || QUESTIONS;
  if (!bank || !bank.length) return null;
  const seed = dateStr || todayStr(); let h = 0;
  for (const ch of seed) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  const q = bank[h % bank.length];
  const rand=()=>{ h=(h*1664525+1013904223)>>>0; return h/4294967296; };
  return shuffleOptions(q, rand);
}
```
  (Same question every visit that day, but the option order is seeded-shuffled — the daily answer position is no longer fixed. `renderQotd()`/`answerQotd()` call `questionOfDay()` fresh each time; because the shuffle is seeded by date, both calls return the same permutation. No other change needed.)
- **Scoping (same finding):** in `renderQotd()`, current `<div class="tag">${esc(q.topic)} · ${esc(q.difficulty)}</div>` → replacement `<div class="tag">${esc(q.topic)} · ${esc(q.difficulty)} · Exams: ${esc((q.exam||[]).join(', '))}</div>` so the aspirant can see when today's question is off their syllabus.

### F23 — reset must not silently wipe the profile

- **File:** `assets/js/app.js:1067` (Dashboard reset button, inline `onclick`).
- **Current:** `onclick="if(confirm('Reset ALL progress (XP, streak, history)?')){progress={xp:0,level:1,streak:0,lastDay:'',attempts:[],bookmarks:[],mistakes:[],flashcardsSeen:0,dailyDone:{},qotdDone:{},weeklyTarget:70,weeklyGoalsMet:0,weeklyGoalMetWeek:'',funFactsSeen:[],focusSessions:0,focusMinutes:0};saveProgress();renderDashboard();}"`
- **Replacement:** change the confirm text to `'Reset ALL progress (XP, streak, history) AND sign out of the local profile? This cannot be undone.'` and add the three identity fields to the literal: `progress={user_id:progress.user_id,email:'',name:'',xp:0,level:1,…}` — i.e. keep `user_id:progress.user_id` (stable device id) and explicitly clear `email:''` and `name:''` so the sign-out is deliberate and visible in code, then call `updateDemoBanner();` before `renderDashboard();`. (Keeping `user_id` avoids orphaning the device's discussions/submissions, which are keyed by name, not id — no data loss either way; the point is the confirm text must say sign-out happens.)

### F24 — add Maintainer Review to the nav

- **File:** `index.html`, header `<nav>` (after the Contribute button).
- **Current:** `<button data-view="submit">Contribute</button>`
- **Replacement:** `<button data-view="submit">Contribute</button>\n<button data-view="moderate">Review</button>` — `showView('moderate')` already renders it via the existing `if(id==='moderate') renderModerate();` branch; no JS change needed. (Mobile bottom nav stays at 5 items — Review is a desktop/header destination only, like Discuss/Profile today.)

### F25 — scanned-paper viewer: link out instead of framing article pages

- **File:** `assets/js/app.js` (`renderPapers()`, ~:1150).
- **Current:** `const viewerSrc=p.pdf_url||p.source_url;` and the `<iframe src="${esc(viewerSrc)}" …>` block.
- **Replacement:** `const viewerSrc=p.pdf_url||null;` and wrap the viewer div: `${viewerSrc?`<div class="paper-viewer" hidden …><iframe src="${esc(viewerSrc)}" …></iframe><p class="muted">If the preview does not load, the source blocks embedding — <a href="${esc(p.source_url)}" …>open the original — scanned paper</a>.</p></div>`:`<p class="muted">Scanned paper — no embeddable PDF was verified for this one. Read it on the source site via "Open Original ↗" above.</p>`}` and change the button line to `${p.pdf_url?`<button class="btn secondary" onclick="togglePaperView(this)">View Scanned</button>`:''}`. (Only the 3 transcribed papers keep an in-page viewer; the other 14 stop showing a probably-blank iframe. Requires the real-browser check in the list below to confirm which sources actually block framing — if the browser check shows some article pages DO frame, restore per-paper.)

### F26 — EN/NE toggle must re-render every view

- **File:** `assets/js/app.js:31-50` (`setLang()`).
- **Current:** if/else chain ending `else if (id === 'view-search') doSearch();`
- **Replacement:** append before the closing brace:
```js
  else if (id === 'view-guide') renderGuide();
  else if (id === 'view-papers') renderPapers();
  else if (id === 'view-notices') renderNotices();
  else if (id === 'view-dashboard') renderDashboard();
  else if (id === 'view-profile') renderProfile();
  else if (id === 'view-discuss') renderDiscuss();
  else if (id === 'view-submit') renderSubmit();
  else if (id === 'view-practice') { /* labels stay bilingual by design; nothing to re-render */ }
```
  (This re-renders question-bearing content in those views — e.g. paper titles carry `title_ne`, notices carry `title_ne`, discussion bodies stay as posted. Full Nepali chrome is still future work per README; this fix only stops the toggle silently doing nothing on 8 of 17 views.)

### F27 — enforce Daily Challenge once-per-day (or drop the flag)

- **File:** `assets/js/app.js:1012-1019` (`dailyChallenge()`).
- **Current:** `progress.dailyDone[seed]=true; saveProgress();` with no read.
- **Replacement (pick one; recommended is the first):** (a) enforce it — at the top of `dailyChallenge()`, insert:
```js
  const seed0=todayStr();
  if(progress.dailyDone[seed0]){ if(!confirm('You already did today\u2019s Daily Challenge. Do it again for practice (no extra XP)?')) return; }
```
  and gate the XP: in `finishAttempt()` the XP award is generic; the honest minimal version is the confirm + a `current._dailyRepeat` flag that `finishAttempt()` uses to award 0 XP (`const xp = c._dailyRepeat ? 0 : xpFor(…)` — set `current._dailyRepeat=true` in the repeat branch). Or (b) delete the flag: remove `progress.dailyDone[seed]=true; saveProgress();` and the `dailyDone:{}` keys from `loadProgress()`/`migrateProgress()`/reset literal, and rename the button "Daily Challenge" → "Daily Challenge (10 Q, replayable)". Do not leave a written-never-read flag.

### F28 — "New random set" keeps the finished exam

- **File:** `assets/js/app.js:981`
- **Current:** `function newRandomSet(){ showView('practice'); startPractice(); }`
- **Replacement:** `function newRandomSet(){ const s=document.getElementById('practice-exam'); if(s && current && current.exam) s.value=current.exam; showView('practice'); startPractice(); }` (If `current.exam` is `''` (mixed modes after F09), the select keeps its current value — correct fallback.)

### F29 — Flashcards scoped to an exam/topic

- **File:** `index.html`, Flashcards card in view-home.
- **Current:** `<p>20 random questions, question first, answer on reveal. Good for the bus, the tea break, the last 10 minutes before bed.</p><button class="btn" onclick="showView('flash');startFlashcards()">Start flashcards</button>`
- **Replacement:** `<p>20 random questions, question first, answer on reveal. Good for the bus, the tea break, the last 10 minutes before bed.</p><label for="flash-exam">Exam (optional)</label><select id="flash-exam"><option value="">All exams (mixed)</option></select><button class="btn" onclick="showView('flash');startFlashcards()">Start flashcards</button>` and in `app.js` `fillExamSelects()` add: `const fs=document.getElementById('flash-exam'); if(fs) fs.innerHTML='<option value="">All exams (mixed)</option>'+allOpts;` and in `startFlashcards()` (~:1026) change `flashQs=shuffle(QUESTIONS).slice(0,20);` to:
```js
  const fe=document.getElementById('flash-exam');
  const fExam=fe?fe.value:'';
  const fPool=fExam?QUESTIONS.filter(q=>q.exam.includes(fExam)):QUESTIONS;
  flashQs=shuffle(fPool.length?fPool:QUESTIONS).slice(0,20);
```

### F30 — state Speed Round rules before it starts

- **File:** `index.html` (Home hero + Practice card buttons).
- **Current:** `<button class="btn secondary" onclick="startSpeedRound()">⏱️ Speed Round (10 Q · 60s)</button>` (two places).
- **Replacement (both places):** `<button class="btn secondary" onclick="if(confirm('Speed Round: 10 questions, 60 seconds total. +1 bonus for a correct answer in under 5 seconds. No going back, no changing an answer, no explanations until the end. Ready?')) startSpeedRound()">⏱️ Speed Round (10 Q · 60s)</button>`. (A confirm is the minimal fix; a proper pre-start card is better but bigger. Do NOT change the in-round behaviour.)

### F31 — data-quality review queue (human, not script)

- **No code change.** Create a review pass over: (a) the 1,807 long-correct-option candidates — recompute with `python3` (correct-option length ≥ 1.8 × longest other AND ≥ 40 chars), sample 100, and rewrite distractors only where the length itself gives the answer away (e.g. add detail to distractors rather than shortening the correct one); (b) the 1,085 explanations < 30 chars — extend the thinnest (one-clause restatements); (c) the 197 explanations identical to the correct option (e.g. `POL-016`) — write a real explanation for each; (d) spot-check 50 of the 846 `question_ne`-identical and 50 of the 4,059 `options_ne`-identical items for genuine missing translations (idiom/formula items are fine — only fix real gaps). Track it as a checklist in `TESTING.md`, not as a code fix.

### F32 — fix the three sampled translation/explanation defects

- **File:** `data/questions/expansion-core-hard.json`, id `IQ3-137` — current `"explanation_ne": "सम्बन्धको श्रृङ्खला पछ्याएर उत्तर पत्ता लगाउनुहोस्।"` → replacement `"explanation_ne": "गिताका बुबाका बुबा गिताका हजुरबुबा हुन्।"`
- **File:** `data/questions/expansion-current-hard.json`, id `CURH-208` — current `"explanation": "Law of gravitation — Law of gravitation means every mass attracts every other mass with a force proportional to their masses."` → replacement `"explanation": "Newton's law of gravitation: every mass attracts every other mass with a force proportional to the product of their masses."` and current `"explanation_ne": "गुरुत्वाकर्षणको नियम — गुरुत्वाकर्षणको नियम को अर्थ प्रत्येक पिण्डले अर्को पिण्डलाई आफ्नो पिण्डको समानुपातिक बलले आकर्षित गर्छ हो।"` → replacement `"explanation_ne": "न्यूटनको गुरुत्वाकर्षणको नियम: प्रत्येक पिण्डले अर्को पिण्डलाई आफ्ना पिण्डहरूको गुणनफलको समानुपातिक बलले आकर्षित गर्छ।"`
- **File:** `data/questions/english-nepali-computer.json`, id `COMP-053` — current `"options_ne": [".jpg", "mp3", ".txt", "mp4"]` → replacement `"options_ne": [".jpg", ".mp3", ".txt", ".mp4"]`.

### F33 — mobile table/palette fixes

- **File:** `assets/css/style.css` — append:
```css
/* Tables scroll horizontally on narrow screens instead of squeezing. */
.table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.table-wrap table{min-width:520px}
```
- **File:** `index.html:126` — current `<div style="margin-top:14px"><table>` → replacement `<div style="margin-top:14px" class="table-wrap"><table>` (and the F19 generated table must also be wrapped: in the F19 `renderMockTable()` template, wrap with `<div class="table-wrap"><table>…</table></div>`).
- **File:** `assets/js/app.js` (`renderGuide()`) — current `<table><tr><th>Stage</th><th>Pattern</th></tr>` → replacement `<div class="table-wrap"><table><tr><th>Stage</th><th>Pattern</th></tr>` and close with `</table></div>` (the guide template ends `</table>` — change that closing tag to `</table></div>`).
- **File:** `assets/css/style.css` — append: `.palette button{max-width:44px}` is already 44 px; no change. For the 200-button MECEE palette, add in `renderQuestion()`'s palette block (no CSS needed): current `${c.mode==='mock'?`<div class="card"><strong>Question palette</strong><div class="palette">…` — add a collapse for long mocks: replace `<div class="palette">` with `<div class="palette" ${c.questions.length>100?'style="max-height:220px;overflow-y:auto"':''}>`. (Palette stays usable; 200 buttons scroll inside a capped box.)
- **Checkboxes:** `assets/css/style.css`, append: `.checks input[type=checkbox]{width:22px;height:22px;accent-color:var(--accent)}` (larger hit area; label text remains tappable).

### F34 — modal closes with Esc / backdrop click

- **File:** `assets/js/app.js`, after `function closeModal(){…}` (~:1480).
- **Current:** no listeners on `#modal`.
- **Replacement:** add:
```js
document.addEventListener('keydown', e=>{ if(e.key==='Escape'){ const m=document.getElementById('modal'); if(m && !m.hidden) closeModal(); } });
document.addEventListener('click', e=>{ const m=document.getElementById('modal'); if(m && e.target===m) closeModal(); });
```
  (Place next to the existing `DOMContentLoaded` listener registration at the end of the file, or immediately after `closeModal()` — either is fine; do not attach inside `openReportForm()`, which would stack listeners.)

### F35 — TSC Licence trailing dash (fixed by F15)

- No separate change: applying F15's replacement (`<p class="muted">${negLine}</p>`) removes the dangling `— ${…:''}` construction for every exam, including TSC Licence (which will read "Negative marking OFF — this exam has no negative marking."). If F15 is deferred, the minimal fix is: current `— ${c.negOn?'exactly like PSC.':''}` → `— ${c.negOn?'exactly like PSC.':'time limit and negative marking unverified for this exam.'}`.

### F36 — trending card #3 topic

- **File:** `index.html`, Home trending card #3.
- **Current:** `<button class="btn secondary" onclick="startPracticeTopic('Nepal History')">Practice</button>` inside the "Most-asked GK ★" card.
- **Replacement:** change the card title from `<strong>#3 · Most-asked GK ★</strong>` to `<strong>#3 · Most-asked GK ★</strong>` (unchanged) and the button to `<button class="btn secondary" onclick="startPracticeTopic('Nepal History')">Practice Nepal History</button>` — and change the footnote `★ New set in progress — practising the closest topic for now.` to `★ Card #3 practises Nepal History, the closest single topic for now — a dedicated most-asked-GK set is in progress.` (The button label now says what it does; the footnote names the card it refers to.)

### F37 — search pagination

- **File:** `assets/js/app.js` (`doSearch()`).
- **Current:** `const res=QUESTIONS.filter(…).slice(0,50);` and `` ` <p class="muted">${res.length} result(s)…` ``
- **Replacement (minimal):** keep the 50-cap but report the true total: change to `const all=QUESTIONS.filter(q=> (!topic||q.topic===topic) && (!term || hay(q).includes(term))); const res=all.slice(0,50);` and the line to `` `<p class="muted">${all.length} match(es) — showing ${res.length}.</p>` ``. Full pagination (page buttons) is a follow-up; the count fix stops the aspirant believing there are only 50 matches.

### F38 — practice timer per exam

- **File:** `assets/js/app.js:767-778` (`startPractice()`).
- **Current:** `if(timerOn){ timeLeft=qs.length*54; startTimer(()=>finishAttempt(true)); } // ~54s per Q, PSC pace (45 min / 50 Q)`
- **Replacement:**
```js
  if(timerOn){
    const examObj2=examById(exam);
    const perQSecs=(examObj2&&examObj2.prelim&&examObj2.prelim.timeMin!=null) ? Math.round(examObj2.prelim.timeMin*60/examObj2.prelim.questions) : 54;
    timeLeft=qs.length*perQSecs; startTimer(()=>finishAttempt(true));
  }
```
  (Derives the per-question pace from the exam's own paper: Kharidar/NaSu 54 s, Section Officer 54 s, TSC 72 s, NMC 83 s, MECEE 54 s, CSIT 72 s. TSC Licence has `timeMin: null` → falls back to 54 s with no verified basis — acceptable for practice, and the practice-pattern line from F19 already says "time unverified" for it.)

### F39 — Staff Nurse `negative` units

- **File:** `data/exams.json`, `staff-nurse-psc.prelim`.
- **Current:** `"negative": 0.4,`
- **Replacement:** `"negative": 0.2,` and append to that entry's `note`: `" (Negative marking is 20%: −0.4 per wrong 2-mark question. Stored as the 0.2 rate like every other exam.)"` — then F04's `mockNegRate()` special case (`if (p.negative === 0.4) return 0.2;`) becomes dead code and should be removed, leaving `if (p.negative === null || p.negative === 0) return 0; return p.negative;`. (Do the data change and the code cleanup together, or neither — a half-applied change breaks the Staff Nurse mock's deduction.)

### F40 — rebuild the bundle after F01 (coordinator only)

- **No file edit in this audit.** Run `node scripts/build-bundle.py`, then `node scripts/test-bundle.js` and confirm it reports 16,850 questions (post-F08 count) and 412 fun facts. Until then, treat the current `test-bundle.js` PASS as stale (it certifies the 2026-10-26 05:16 artefact).

## Still needs real browser / human check

1. **Render + tap-through (360 px phone + desktop):** countdown and auto-submit in a real mock; palette jumps on a 200-question MECEE mock; sticky bottom nav vs footer overlap; Devanagari clipping in options at 360 px; light theme contrast; the scanned-paper iframe behaviour per source (F25 — confirm which of the 14 sources actually block framing); EN/NE toggle mid-quiz; confetti/reduced-motion.
2. **Human accuracy audit of a question sample:** the validator checks structure, not truth. F02/F03 came from a 45-question sample (2 provably wrong ≈ 4% of sample — do not extrapolate, but do audit: minimum 200 more questions, weighted to Health/Law/licence topics and to generated arithmetic items). The 1,807 long-correct-option candidates (F31) need a human pass, not a script.
3. **Human Nepali review:** `explanation_ne` quality (F32 shows the NE explanation can be a generic instruction while EN explains); the 846 `question_ne`-identical items (mostly English idioms — confirm each is legitimately untranslatable, not a missing translation).
4. **Exam patterns against official sources:** no PSC/TSC/NRB/council PDF was read directly in this audit (same limitation as SOURCES.md). Before the next publish, verify against psc.gov.np / tsc.gov.np / nrb.org.np / council notices: Kharidar/NaSu/Section Officer 2081/82 prelims (50×2/45 min/pass 45); Section Officer main-paper pass 40 vs 45; NRB Officer prelim (F14); Police Inspector GART 50 min/pass 40 (F14); NHPC 90 vs 120 min conflict (BSc MIT / B.Optom); NMC-BDS 180Q shape (F18); MECEE-BL −0.25 (already in GAP-AUDIT, re-verify); TSC Licence time limit + negative marking (both null — the highest-value verification in the file).
5. **Notices live check:** re-verify all 10 notices after 2026-10-27 (Police ASI + Gandaki close that day); confirm the two "unverified" ones (TSC licence, Bagmati PPSC) or remove them. Apply F17 so this is a one-time check, not a weekly chore.
6. **Old papers:** the NaSu First Paper 2082-01-20 date flag (overview says 2082-01-20, paper image says 2083/01/20 — SOURCES.md §14.15) is still unresolved; the Kharidar pretest 2083/06/04 still has no answer key — do not transcribe it without one.
7. **Demo-mode honesty in a real browser:** sign-in with a non-Gmail address (rejected by design — confirm the error reads clearly); sign-out then check Dashboard/Profile still render; submit a question end-to-end and confirm it lands in Maintainer Review and NOT in the bank until approved.
8. **Performance:** Home with 16,850 questions — `renderTopics()` builds a card per topic (fine) but `doSearch()` runs `hay()` over the full bank per keystroke-free submit (fine); the real risk is `loadData()` fetching 45 files over slow mobile data — measure on a real phone, consider the bundle as the default share link until then.

## Prioritised "missing aspirant needs" (quick wins first)

| # | Need | Why it matters to an aspirant | Effort |
|---|---|---|---|
| 1 | **Pattern card before every mock + practice** (F19) | Aspirants currently start 3-hour mocks blind. | Quick win — generated table from `exams.json`, no new data. |
| 2 | **Mock topic mix** (F10) | The mock's entire promise ("exactly like the real prelim") is false on mix today. | Quick win for Kharidar/NaSu/SO (F10 spec); medium for NRB/licence (needs topic modelling). |
| 3 | **Mock mistakes → Mistakes + Marathon** (F05) | The most valuable revision list in the app is currently empty after mocks. | Quick win — 2 lines. |
| 4 | **Timer stops on navigation** (F06) | A mock auto-submitting while the user reads the Guide is a trust-killer. | Quick win — 1 line. |
| 5 | **Per-exam negative marking + marks in practice** (F13, F04) | Licence aspirants are currently penalised by rules their exam doesn't have. | Quick win — F13/F04 specs. |
| 6 | **Syllabus view per exam** (F21 + guide filter) | One 47-card page with no jump/filter; aspirants can't find "their" syllabus. | Quick win — anchors + filter input. |
| 7 | **Weak-topic summary that includes mock errors + a "study next" nudge** | Result already shows weakest-3 topics (good); Dashboard weak topics ignore mocks (F05) and there is no next-step link ("Practice Constitution now"). | Quick win once F05 lands — add a "Practice weakest topic" button on the result screen calling `startPracticeTopic(worst[0])`. |
| 8 | **Notices auto-expiry** (F17) | Two notices die tomorrow; without it the page lies within 24 h. | Quick win — F17 spec. |
| 9 | **Exam-scoped Daily / Quick / Flashcards / QOTD** (F09, F22, F29) | Everything "daily/fun" is whole-bank random; a Kharidar aspirant gets NHPC questions. Needs a "my exam" setting — the app has no current-exam concept. | Medium — add a "My exam" picker on Home persisted in `loksewa_progress_v1`, defaulting to the last practised exam; scope daily/quick/flash/QOTD to it. |
| 10 | **Subjective / Paper II practice** | Kharidar Paper II, NaSu Paper II, Section Officer mains are all descriptive — the app only does MCQs, so an aspirant who passes prelims has nowhere to go. | Large — model answers + self-marking rubric; guide-only for now. |
| 11 | **Police Inspector split-out mock** (GART 50 min/pass 40) + **NEA Section A practice** (50×1) | Both patterns are verified in GAP-AUDIT but the app serves the generic placeholder instead. | Medium — new prelim entries + tagged questions. |
| 12 | **Current-affairs feed** (dated, sourced) | Current Affairs is 830 tagged questions but static to 2025; the 2026 House election (5 Mar 2026) is already in the bank — the feed would keep it fresh. | Medium — curated monthly batch, not a live scrape. |
| 13 | **Real backend (Supabase)** | Everything social (discussions, submissions, progress sync) is local-only demo; two devices = two separate aspirants. | Large — `docs/BACKEND.md` already plans it. |
| 14 | **IOE mixed-mark mock** (60×1 + 40×2, 140 marks) | IOE is guide-only solely because the engine assumes uniform marks/question. | Medium — per-question marks already exist in the bank; `startMock()` would need to stop overriding `marks` and score per question. Do after F10. |

## Counts

- **Total questions on disk:** 16,850 in 46 files (45 bank files + `community-approved.json` at 0). **Loaded by the app:** 15,087 in 41 files. **Unloaded:** 1,763 in 4 files (F01).
- **Exams:** 47 (33 with mock, 14 guide-only). **Mocks whose tagged pool covers the paper:** 33/33 by count, 0/33 by topic mix (F10).
- **Papers:** 17 (3 transcribed, 133 questions; 14 scanned-only). **Notices:** 10 (2 open, 2 closing soon, 4 closed, 2 unverified; 0 expired-but-marked-open on 2026-10-26).
- **Fun facts:** 412 (README/bundle say 322).
- **Test suites run:** `test-app.js` 1 FAIL · `test-questions.js` 31 FAILURES · `test-e2e.js` PASS · `test-v2.js` PASS · `test-funfacts.js` PASS · `test-bundle.js` PASS (stale bundle, F40).
- **Sample audit:** 45 questions (1/file, seed 20261026) — 2 provably wrong answers (F02, F03), 1 tautological explanation, 1 NE explanation that doesn't explain, 1 NE options inconsistency (F32).

*End of self-audit — 2026-10-26. No code or data was modified; only this file was created.*

## Addendum — Wrong-answer key audit, 2026-10-26 evening

Triggered by a live user report: in practice, option D (637) was selected for the series
7, 17, 37, 77, 157, 317, ? but the app marked it wrong, showing "Correct answer: C. 636"
while its own explanation said 317 × 2 + 3 = 637. That question (HARD2-007) was fixed
first by the parent (answer 3 → 1). The same class of bug — explanation correct, key
wrong — was then audited across the whole bank.

### Method
- Script `scripts/audit-answer-mismatch.py` (saved in the repo for re-use) checked all
  20,200 questions: it extracts the value the explanation concludes with (last
  "= Rs/रू/रु number", "answer is X") and compares it with options[answer]. It flagged
  122 candidates. Every candidate was recomputed by hand from the question itself.
- A separate deterministic random spot-check (seed 42) of 100 questions across 23
  topics, excluding the two files being fixed, found 4 more key errors the script
  could not see (their explanations state the answer in words, not numbers).
- The 4.61% figure in CURH-402 was verified against live sources (Economic Survey
  2081/82 projection, Ministry of Finance; also reported by CollegeNP / CEO Tab).

### Fixes applied (78 key fixes, 0 removed)
- **74 keys fixed in `expansion-hard-core-v2.json`** — the same file as the user's
  bug, and the same pattern throughout: explanation arithmetic correct, `answer`
  index wrong. Number Series 22, Analogy 3, Percentage 9, Profit & Loss 8, Simple
  Interest 10, Compound Interest 3, Time & Work 8, Speed/Distance/Time 7, Ratio &
  Proportion 4. Changed ids: HARD2-001, 002, 004, 006, 009, 011, 012, 015, 016, 017,
  020, 021, 022, 024, 026, 027, 028, 029, 030, 032, 038, 039, 140, 143, 145, 158, 160,
  161, 163, 164, 165, 168, 169, 171, 177, 178, 182, 184, 191, 193, 199, 200, 203, 204,
  206, 208, 209, 210, 211, 212, 213, 214, 217, 223, 225, 230, 236, 237, 238, 239, 241,
  244, 245, 247, 248, 249, 252, 254, 255, 256, 263, 270, 272, 273. Only the `answer`
  index changed; no explanation text needed changing. File still 500 questions.
- **4 keys fixed from the spot-check:** CURH-163 (Albanese → Australian Labor Party,
  answer 3 → 2), PHARM-169 (pharmacy supervision → registered/assistant pharmacist,
  2 → 1), CURH-402 (Nepal 2081/82 growth forecast → 4.61 percent, 3 → 1; figure
  web-verified), HEAL2-009 (shinbone → tibia, 3 → 1).
- **1 question reworded:** CURH-132 asked "When did this happen? Who won the World
  Test Championship final?" but all options were dates — reworded to "When was the
  World Test Championship final played?" (key A, June 2025, unchanged).
- **3 Nepali explanations fixed:** OFF2-085 (garbled "Minutes" — "निर्णयले" →
  "मिनेटले"), IQ3-170 (placeholder → working: 7 − 3 + 1 = 5th), IQ3-059
  (placeholder → "each letter 3 back: RIVER → OFSBO, so ISLAND → FPIXKA").

### False positives (48 script flags, all hand-verified, no change)
- 24 in `expansion-r5-maths-hard.json`, 11 elsewhere, 13 in the hard-core file:
  the flagged number is an intermediate step, not the conclusion — father's current
  age before "+5 years", the numerator of a combined work rate (3/12 → 4 days),
  a mod result (7 mod 4 = 3 → unit digit 9), a sum (pH + pOH = 14 → pOH 7),
  total marks (50 MCQs × 2 = 100), values vs bits (2³ = 8 → 3 bits), a principal
  or marked price before the interest/discount is applied.
- After fixing the audit script to recognise Devanagari `रू`/`रु` after `=`, 24 flags
  remain, all of the intermediate-step kind above. They are documented here, not
  in the data — the questions are correct.

### Side note
- R6B-490 and R6B-736 are the same binary question (1010₂ = 10) with options in a
  different order — a duplicate pair in `expansion-r6b-licence-entrance.json`. Keys
  are both correct; deduplication/rewording is left for a later pass.

### Result
- Questions checked: 20,200 by script + 100 random spot-check. Keys fixed: 78.
  Explanations fixed: 3 (+1 reword). Removed: 0. Total stays 20,200.
- All six test suites re-run and PASS after the fixes; phone bundle rebuilt.

---

## Answer-key audit — full-bank merge, 2026-10-26 evening

Five audit workers checked the bank in parallel (a sixth, numeric, audit was
editing files at the same time). This section records the merge: what each
workstream proposed, how overlaps were resolved, what was actually applied,
what was removed, and what is still open. Full machine-readable log:
`audit-patches/merge-log-2026-10-26.json` (every applied fix with old/new
value, every skip, every removal). Pre-merge backup (questions + funfacts) is
held outside the repo at `/tmp/audit-merge/backup-before-merge/` — it does
not survive a VM rebuild; the patch files in `audit-patches/` are the durable
record of what changed and why.

### Per-workstream totals (as proposed)

| Workstream | Checked | Fixes proposed | Removals proposed | Unverifiable (left unchanged) |
|---|---|---|---|---|
| maths-iq | 3,676 | 171 | 20 | 1 (NASU-2083-31) |
| constitution-history | 2,258 | 22 | 0 | 2 |
| science-health-law | 1,332 | 142 | 0 | 5 |
| language-current-funfacts | 3,291 questions + 609 facts | 266 (+ 4 fun-fact fixes) | 36 (+ 1 fun-fact removal) | 4 |
| consistency (whole bank) | 20,200 | 456 | 19 | 9 (incl. 6 translation-gap + 2 skew notes) |
| **Raw total** | — | **1,057** (+ 4 fun-fact) | **75** (+ 1 fun-fact) | 21 |

### Merged totals

- Raw proposals: 1,057 question fixes + 4 fun-fact fixes + 75 removals + 1 fun-fact removal.
- Deduplicated by (file, id, field): **708 unique question field-changes**.
  The overlap was heavy and almost entirely agreement: 349 groups proposed by
  2+ workers with the identical new value; 359 proposed by one worker.
- **Conflicts between workers: 0.** No (id, field) was ever proposed with two
  different new values, so no conflict adjudication was needed.
- **Applied: 616 question field-changes** (552 answer keys, 24 explanations,
  23 explanations_ne, 4 options, 5 options_ne, 4 questions, 4 questions_ne)
  **+ 4 fun-fact field-changes** (FF-039 en/ne, FF-330 en/ne) = **620 field
  changes in total**. By worker (a group proposed by 2 workers counts for
  both): maths-iq 97, consistency 438, language-current-funfacts 248,
  science-health-law 142, constitution-history 22.
- **Skipped as already applied: 74** — all maths-iq answer fixes in
  `expansion-hard-core-v2.json` (HARD2-001…HARD2-193 range), where the live
  value already equalled the patch's new value: the parallel numeric audit
  had fixed them during this run. The four examples named in the merge brief
  (CURH-163, CURH-402, PHARM-169, HEAL2-009) do not appear in any patch file
  at all — they were fixed by that parallel audit, not by this merge.
- **Superseded by removal: 18** — answer fixes proposed (by both the
  consistency and language workers) for CURH degenerate label questions that
  the language worker proposed removing; removal won, the re-key was not
  applied. Ids: CURH-352, CURH-354, CURH-358, CURH-362, CURH-364,
  CURH-366, CURH-368, CURH-370, CURH-376, CURH-378, CURH-382, CURH-388,
  CURH-399, CURH-405, CURH-407, CURH-409, CURH-411, CURH-413.
- **Blocked: 0.** No patch proposed changing a previous-year-2083 answer key.
- **Removals applied: 68 questions** (raw 75 proposals → 68 unique; 7 were
  proposed by two workers). No ids were renumbered.

### Re-check method (before applying anything)

Every proposed fix was re-checked against the live file state: 551 of 552
parseable answer fixes had their reason's stated old option matching the live
keyed option exactly (the one exception, NEP2-288, is a paraphrase — the
reason says "first newspaper", the live option is गोरखापत्र, which is the
first newspaper — and the patch also carries matching explanation fixes).
Four answer fixes whose live explanation still named the old option were
hand-checked (CURH-102, CURH-189, HARD2-133, HARD2-135): in each case the
explanation actually supports the new key (a month range containing the exact
date; the odd-one-out reasoning), so no extra edit was needed. No fix was
applied blind where the live value was a third value — no such case occurred.

### Previous-year 2083 — untouched keys

Zero answer keys changed in `previous-year-2083.json`. The only change there
is an explanation correction for KHAR-2083-24 (en + ne): the old explanation
claimed the second letters increase by a constant +4 (E→I→O→U is +4,+6,+6,
not constant); the answer HOZ is unchanged and is still forced by the first
and third letters. NASU-2083-11 stays as printed: dual-answer (Tuberculosis
and Leprosy), as the paper itself notes. NASU-2083-31 (number grid with no
stated rule) was left unchanged — it cannot be recomputed from the stem.

### Removals (68 ids, by file)

- `expansion-current-hard.json` (36) — degenerate label questions: the
  "correct" option merely repeats the stem label; the same fact is properly
  tested by the paired "What is the X?" question. CURH-352, CURH-354,
  CURH-356, CURH-358, CURH-360, CURH-362, CURH-364, CURH-366, CURH-368,
  CURH-370, CURH-372, CURH-374, CURH-376, CURH-378, CURH-380, CURH-382,
  CURH-384, CURH-386, CURH-388, CURH-390, CURH-392, CURH-394, CURH-395,
  CURH-397, CURH-399, CURH-401, CURH-403, CURH-405, CURH-407, CURH-409,
  CURH-411, CURH-413, CURH-415, CURH-417, CURH-419, CURH-421.
- `expansion-hard-core-v2.json` (8) — alternating-step letter series where
  the correct next letter is not among the options: HARD2-054, HARD2-055,
  HARD2-056, HARD2-057, HARD2-058, HARD2-092, HARD2-117, HARD2-118.
- `expansion-r5-maths-hard.json` (7) — HARD5-100, HARD5-112, HARD5-183,
  HARD5-320, HARD5-328, HARD5B-041, HARD5B-049.
- `expansion-thin-exams.json` (4) — ARMY-077, ARMY-127, ARMY-129, ARMY-130.
- `iq-maths.json` (3) — IQ-036, IQ-037, IQ-046.
- `expansion-entrance-licence.json` (2) — MECEE-139, MECEE-146.
- `expansion-r6a-hard.json` (2) — R6A-B258, R6A-B453.
- `expansion-r7b-core-hard.json` (2) — R7B-117, R7B-118.
- `expansion-core-hard.json` (1) — MATH3-028.
- `expansion-iq-maths.json` (1) — IQ2-070.
- `expansion-nhpc-law.json` (1) — OPT-026.
- `expansion-r6a-current.json` (1) — R6A-C065.

Per-file counts after removal: expansion-current-hard 500 → 464,
expansion-hard-core-v2 500 → 492, expansion-r5-maths-hard 1,116 → 1,109,
expansion-thin-exams 599 → 595, iq-maths 220 → 217, expansion-entrance-licence
600 → 598, expansion-r6a-hard 561 → 559, expansion-r7b-core-hard 600 → 598,
expansion-core-hard 600 → 599, expansion-iq-maths 700 → 699,
expansion-nhpc-law 400 → 399, expansion-r6a-current 437 → 436.

### Fun facts

- Fixed (4 field changes, 2 facts): FF-330 Simone Biles 32 → 41 combined
  Olympic + World medals (11 Olympic + 30 World); FF-039 Kami Rita Sherpa
  "more than two dozen" → 32 Everest summits, most recently May 2026.
- Removed (1): FF-393, duplicate of FF-150 (Angel Falls 979 m, tallest
  waterfall). Total 609 → **608**; no duplicate fact_en/fact_ne texts remain.
- FF-039's new wording ("most recently in May 2026") will go stale again —
  current-affairs facts need a periodic re-check, same as the question bank's
  current-affairs items.

### Non-patch findings (recorded, NOT silently fixed)

- `expansion-zero-licence.json` answer skew: option B keyed 74% of the time
  (333/450; A 72, C 40, D 5). Verified by the consistency worker from a
  12-item sample: the B keys sampled are correct. Keys left as-is; the skew
  is a placement problem, not a correctness problem — re-keying would have
  made correct answers wrong. (Also noted, weaker: `expansion-entrance-
  licence.json` B 44.2% / D 13.8%, not key-verified beyond sampled flags.)
- Translation gap — `options_ne == options` for 100% of questions in 6
  files (**2,779 questions**): expansion-english-nepali-v3.json (500),
  expansion-nepali-v2.json (299), expansion-r6b-banking-health.json (352),
  expansion-r6b-language.json (487), expansion-r6b-licence-entrance.json
  (741), expansion-r7b-current.json (400). Stems are translated but options
  stay in English. NOT hand-translated in this run. Honest caveat: the test
  suite's "bilingual 100%" check verifies the Nepali fields are *present*,
  not that they differ from the English — so it passes on these files while
  the Nepali option text is verbatim English.
- Pervasive near-duplicate re-asking across exams/files (same fact re-asked
  with slightly different wording, e.g. CONST-001 / R6A-B472): flagged by the
  consistency worker, no bulk action taken — deduplication policy decision
  still open.

### Unverifiable items left unchanged (21)

- Vowel-count convention: R6B-L-482 keys 12 vowels (12 + 33 + 1 अयोगवाह =
  46) while NEP-013 keys 13 (13 + 33 = 46). Sources genuinely disagree;
  the bank should adopt one convention (worker recommends 13 + 33 = 46)
  rather than changing one item.
- First telephone line: NT2-001 keys 1916 (Nepal Telecom's own milestone
  list) vs NTEL5-040 keys 1913 (Wikipedia / OnlineKhabar). Both dates have
  reputable sources; adopt one convention and drop/reword the other.
  NTEL5-041 keys 1913 for the first *telegraph* service — no source
  confirms 1913 for telegraph (that date belongs to telephone lines).
- 2021 census caste/ethnic-group count: 142 (NSO-cited reporting) vs 146
  (Wikipedia's 2021 census page). No bank question asserts either figure.
- Teachers Service Commission establishment year: 1999 sixth amendment /
  operational Feb 2002 vs seventh amendment 2058 BS. No question written
  until one authoritative source is settled.
- HEAL2-129 (minimum antenatal check-ups: 4 vs WHO 8), HEAL2-145 (lowest
  village health institution: health post vs ward community health unit),
  LAW5-019 (Bar Council Paper 1 format unverified against an official
  source), BAR-059 (adverse possession 12 years — widely cited, exact
  section unverified).
- HEAL2-023 was applied (Cornea → Lens, both workers agreed, explanation
  supports Lens) but the science worker flags the stem itself as ambiguous:
  the cornea provides ~two-thirds of refractive power while the lens
  fine-tunes focus — if the intended point is total refractive power, the
  question should be reworded, not just re-keyed.

### Result

- Questions: 20,200 → **20,132** (68 removed, 0 added). Unique ids 20,132;
  0 duplicate ids; all answers in range; all options 4.
- Fun facts: 609 → **608**.
- Difficulty now 5,692 easy / 8,635 medium / 5,805 hard (was 5,698 / 8,642 /
  5,860). Answer balance A 25.0% / B 26.6% / C 24.4% / D 24.0% (was A 24.7% /
  B 26.2% / C 24.8% / D 24.3%).
- Counts updated to 20,132 / 608 in `scripts/test-e2e.js`, `test-v2.js`,
  `test-bundle.js`, README.md (totals, bank table, by-topic and by-exam-tag
  lines recomputed from disk, new roadmap line) and TESTING.md §P.
- All six test suites re-run and PASS after the merge; phone bundle rebuilt
  (20,086,489 bytes, md5 74512d688ecf91e372339c7b0fad5758).
- Still open (unchanged from before): no real-browser smoke test; human
  accuracy + Nepali translation spot-check recommended before GitHub upload;
  R6B-490 / R6B-736 duplicate pair still present; `community-approved.json`
  still empty (0 questions).

## Round 8 — Nepali translation pass + Gemini second-opinion fixes (2026-10-26 evening)

### Translation gap (found by the full answer-key audit)
The "100% bilingual" validator only checked that `_ne` fields exist. A scan found **3,291 questions** whose `options_ne` was a verbatim copy of English options containing English words, plus ~397 mostly-English `question_ne` and ~348 mostly-English `explanation_ne`. Six workers translated by hand, one file-group each; answer indexes and all non-`_ne` fields verified unchanged against backups.

| Group | Files | Options translated | Questions translated | Explanations translated |
|---|---|---|---|---|
| A | english-nepali-v3, r6b-language, english-nepali-computer | 105 | 82 | 19 |
| B | r6b-licence-entrance (741 q) | 678 | 2 | 1 |
| C | entrance-licence, r7b-current | 490 | 42 | 146 |
| D | r7b-core-hard, english-v2, core-hard, iq-maths, expansion-iq-maths | 230 | 139 | 66 |
| E | 14 banking/technical/law/current files | 331 | 7 | 42 hand + 64 digit |
| F | 9 small files incl. previous-year-2083 | 10 q (11 fields) | 0 | 1 |
| Final sweep (coordinator) | all files: terms + digits | ~23 option items + 7,580 digit/term fields* | — | — |

*Final sweep digit normalisation converted Arabic digits to Devanagari in Nepali prose (e.g. years, amounts); 805 bad conversions (chemical formulas H₂O, file extensions mp3, function keys F5, IPv4, 2FA) were caught and reverted — 0 remain. Binary literals, formulas and code kept in Arabic digits.
Remaining whole-list candidates after the pass: 1,426 options / 269 questions / 196 explanations — spot-checked by random sample, all legitimate keeps: tested English material (grammar, idioms, synonyms), codes, chemical symbols, formulas, acronyms, proper names, OS/product names. Proper names were deliberately kept in Latin per the brief; transliterating them (e.g. Donald Trump → डोनाल्ड ट्रम्प) is a separate follow-up decision.
Out-of-scope observations: KHAR-2083-15 `question_ne` typo `बाडिएको` fixed in final sweep; IQ-035 English option `WriteX` was malformed — changed to `Writing` (NE `लेख्दै`) as a judgement call.

### Gemini second-opinion fixes (all verified in data files before changing)
- CONST-039: "national language → Nepali" was wrong — Art. 6 makes all mother tongues national languages; Art. 7(1) makes Nepali (Devanagari) the official language. Question reworded to official language, EN + NE + explanation.
- CONST-063: Butwal is only Lumbini's temporary capital; permanent capital Deukhuri (Rapti Valley, Dang), designated Oct 2020. Question now asks for the temporary capital.
- CONST-059–065: Nepali versions reversed subject/object ("विराटनगरको राजधानी कुन प्रदेशमा छ?") → fixed to "विराटनगर कुन प्रदेशको राजधानी हो?".
- NEP-010: Shakuntala is a Mahakavya, not a play — नाटक → महाकाव्य.
- NEP-009: reworded to "नेपालको सरकारी कामकाजको (आधिकारिक) भाषा कुन हो?"
- CONST-223: Nepali dropped the negative — नविकरणीय → अनवीकरणीय.
- CONST-048: "Schedules" as कार्यतालिका → अनुसूची.
- Terms fixed everywhere verified: Speaker → सभामुख (parliamentary; computer speaker → स्पिकर, e.g. CONST-233), "No poverty" (SDG 1) → गरिबीको अन्त्य, "Sayaun Thunga Phool Ka" → सयौँ थुँगा फूलका (was साउं/सयौं), Crimson → सिम्रिक, Golgi body → गोल्गी बडी, "Read Access Memory" no longer translated as imperative ("पढ्नुहोस् र मेमोरी").
- CONST-192/193: distractors "Go"/"In" had been translated as "जानुहोस्"/"मा" — restored to the symbols Go/In (Fe too).
- CONST-019/069/089: garbled "डा"/"स्व" suffixes removed (प्रधानन्यायाधीश डा, प्रधानमन्त्री स्व, गभर्नर डा).
- CONST-129: explanation "लक्ष्य १ होइन गरिबी हो" rewritten; CONST-062 expl_ne वाग्मती → बागमती.
- CSS: duplicate @media(max-width:640px) block removed (2 → 1).
- Section Officer scoring: VERIFIED NOT A BUG — practice and mocks already override each question's marks with the exam's marksPerQ (1), so Section Officer scores out of 100, not 200.
- Bundle truncation reported by Gemini: NOT our bug — the user's downloaded copy ("loksewa-prep-nepal-full (6)") was an incomplete download; the on-disk bundle is 20MB and ends cleanly with </script></body></html>. Rebuilt bundle re-checked.

## Dedupe sweep (2026-10-26, after the answer-key audit)

### Tool
`scripts/dedupe-check.py` — detects (a) exact duplicates (normalised stem
identical), (b) near-duplicates (token-Jaccard >= 0.8 on EN or NE stem),
(c) same stem with options in a different order, (d) same fact asked two
ways with the same correct answer (content-Jaccard >= 0.7 + >= 3 shared
options + same correct answer). Normalisation: lowercase, Devanagari/Arabic
digits -> Arabic, sub/superscript digits -> Arabic, punctuation -> space,
collapse whitespace (mirrors `assets/js/app.js` normaliseText/tokenJaccard).
Run: `python3 scripts/dedupe-check.py --exclude expansion-r8-,expansion-r10-`
(report/plan JSONs in `~/workspace/dedupe-recovery/`).

### Result
- Bank (pre-R8/R10 files only): 20,132 -> **18,608** (1,530 removed, 6
  restored as false positives -> **1,524 net removed**).
- Classified duplicate pairs: 2,065 in 1,208 groups — by type: exact 309,
  near 1,206, same-options-reordered 274, same-fact 276.
- Keepers: best-written copy kept (bilingual first, then longer explanation,
  more exam tags, non-expansion file preferred); **722 keepers gained the
  removed copies' exam tags**, so no exam loses coverage.
- Reworded: 0 — no pair needed rewording; every genuine duplicate had one
  clearly keepable copy.
- `node scripts/test-questions.js` on the swept bank: TOTAL 18,608, bilingual
  100%, **ALL CHECKS PASSED**. (Full-repo run still shows 3 failures — all
  R8-vs-original duplicates, see below; not caused by this sweep.)
- Full per-id decision log (removed id, duplicate type, kept counterpart(s),
  stem, correct answer): `data/dedupe-decisions-2026-10-26.json`.

### Precision guards (each learned from a sampled false positive)
- Stem similarity alone is NOT a duplicate: the bank is full of distinct
  questions differing by one key word (primary vs secondary prevention,
  different dates/numbers) — 26,361 of 30,624 loose pairs had neither the
  same correct answer nor the same options and were rejected.
- `loose_same_correct` is strict: same numeric value alone does NOT count
  (two SI drills can both equal 3000); near-identical strings do NOT count
  ('25 years' vs '35 years', 'Article 21' vs 'Article 22'); a subset match
  does NOT count when the only extra tokens are numbers ('13 July 2025' vs
  'July 2025', 'CnH2n' vs 'CnH2n+2', '6 years' vs '6-7 years').
- Numbers veto: both stems carry numbers -> number multisets must match AND
  each number must share a neighbouring token ('2 A / 6 ohm' vs '2 ohm / 6 A'
  is a different problem).
- Tail check: last 3 content tokens of the stems must share one token
  (same-scenario different IQ sub-questions are not merged).
- Contrast veto: men/women, civil/criminal, primary/secondary, hosted/won,
  US/French Open, first/last, largest/smallest, correct/incorrect, etc.
- NE-exact alone does NOT count (template stems share one generic Nepali
  translation while testing different words); even EN-exact needs the same
  correct answer (template stems like 'Choose the correct spelling.').
- Greedy star clustering: a member is removed only if it pairs DIRECTLY
  with its keeper, never via a chain (an early version collapsed a 159-
  question Article-rights family into one keeper).
- Retired rule: the 'shared rare token' rule was removed from the script
  after the sweep — see restores below.

### Known case (from the brief)
- R6B-490 kept, **R6B-736 removed** (same-fact): 'The binary number 1010
  equals which decimal number?' vs '...equals in decimal:' — same answer
  10, options reordered (8/10/12/5 vs 8/12/10/14). R6B-490 kept on its
  clearer, complete stem ('equals which decimal number?' vs 'equals in
  decimal:'); explanations are identical. R6B-736's `csit-entrance` tag
  was merged into R6B-490.

### Previous-Year 2083 (protected)
- No PY question removed. Three bank questions removed as duplicates OF a PY
  question (PY kept, bank copy removed): CURR2-014 (ASEAN founded, dup of
  KHAR-2083-10), R7B-673 (Census 2078 caste groups 142, dup of
  KOSHI-2083-10), R7B-899 (Yoga Day 21 June, dup of KHAR-2083-39).
- KHAR-2083-35 vs KOSHI-2083-11 (16th Plan per-capita target 2351) are near
  duplicates but NOT exact -> both kept per the PY rule.

### Restored (6) — wrongly removed, put back verbatim from the pre-sweep bundle
The 'shared rare token' rule matched a shared headword while the
distinguishing token differed; the rule has been deleted from the script.
- CURH-244 'Which term is described as: Au?' (Chemical symbol of gold) vs
  CURH-266 O3 (Chemical formula of ozone) — shared token 'chemical'.
- MECEE-030 'Which gland secretes Oxytocin?' (Posterior pituitary) vs
  MECEE-028 Growth hormone (Anterior pituitary) — shared 'pituitary'.
- IOE5-127 'third-angle projection -> Third quadrant' vs IOE5-126
  first-angle (First quadrant) — shared 'quadrant'.
- R6A-A437 'HDL cholesterol is known as: Good' vs R6A-A438 LDL ('Bad') —
  shared 'cholesterol'.
- COMPOP-014 'What does PDF stand for?' vs COMPOP-016 PNG — shared
  'portable'.
- COMPOP-027 'What does OCR stand for?' vs COMPOP-028 MICR — shared
  'recognition'.
- NOT restored: CONST2-133 (High Court retirement, keyed 65) was removed as
  a dup of Supreme Court items; its key is wrong (High Court retires at 63,
  not 65) but the fact is covered correctly by live R6A-B526 (63 years), so
  no restore. (Pre-existing key error, found by this sweep, not introduced
  by it.)

### Deliberately kept (not duplicates — sampled and verified)
- 782 identical-stem/different-key pairs: template stems whose content lives
  in the options ('Choose the correct spelling.' for Beautiful vs Necessary;
  'Choose the synonym of generous.' Liberal vs Charitable; 'Choose the
  synonym of rapid.' Swift vs Fast). Same stem, different tested word.
- Same-option-set/different-answer families: computer generations (vacuum
  tubes vs transistors), Class A vs D banks, Ozone Day (16 Sep) vs
  Environment Day (5 Jun), men vs women hernia, alkenes (CnH2n) vs alkanes
  (CnH2n+2), Wimbledon men's vs women's singles, US vs French Open 2025,
  hosted vs won (2025 Women's Rugby World Cup).
- MECEE-029 (ADH/Vasopressin) vs MECEE-030 (Oxytocin): same gland
  (posterior pituitary), different hormones — flagged by the checker (NE
  template identical) but distinct questions; both kept.
- Same-template maths drills with different numbers (SI, rectangle areas,
  age problems) were NOT removed even when the answer coincided.

### Out of scope / deferred to the coordinator
- R8 + R10 files landed mid-sweep (3 R8 files, 1,159 q; 2 R10 files, 4,863+
  q and growing) and were EXCLUDED from this sweep (`--exclude`); their
  files were never touched. Re-run the dedupe after integration.
- The 3 full-repo test failures are R8 copies of existing questions:
  R8LAW-431 (rural municipalities 460, dup of CONST-008), R8LAW-436
  (provincial assembly term 5 years, dup of CONST2-235), R8LAW-443 (first
  woman Chief Justice Sushila Karki, dup of HIST-037). The R8 copies are
  the duplicates — remove those, not the originals.

### Removed ids (net 1,524; per-id type + keeper in data/dedupe-decisions-2026-10-26.json)
```
ALLIED-019, ALLIED-113, ARM3-022, ARM3-023, ARM3-025, ARM3-027, ARMY-035, ARMY-053, ARMY-055, ARMY-062, ARMY-064, ARMY-070, ARMY-071, ARMY-100, ARMY-109, ARMY-112, ARMY-113, ARMY-114, ARMY-115, ARMY-116, ARMY-118, ARMY-136, ARMY2-023, AYUR5-002, AYUR5-028, AYUR5-029, AYUR5-043, AYUR5-062, BANK-002, BANK-010, BANK-014, BANK2-009, BANK2-023, BANK2-066, BANK2-069, BANK2-079, BANK2-098, BAR-001, BAR-003, BAR-004, BAR-005, BAR-006, BAR-007, BAR-008, BAR-009, BAR-010, BAR-011, BAR-012, BAR-013, BAR-014, BAR-015, BAR-016, BAR-017, BAR-018, BAR-019, BAR-020, BAR-022, BAR-023, BAR-043, BAR-044, BAR-045, BAR-046, BAR-050, BAR-055, BAR-079, BAR-080, BAR-097, BDS-011, BDS-167, CA3-008, CA3-020, CA3-023, CA3-028, CA3-031, CA3-069, CA3-072, CA3-074, CA3-075, CA3-076, CA3-080, CA3-100, CA3-101, CA3-104, CA3-107, CA3-108, CA3-115, CA3-124, CA3-130, CA3-131, CA3-135, CA3-136, CA3-140, CA3-146, CA3-148, CA4-012, CA4-060, CA4-073, CA5-002, CA5-004, CA5-008, CA5-013, CA5-015, CA5-040, CA5-041, CA5-053, CA5-056, CA5-058, CA5-063, CA5-068, CA5-069, CA5-074, CA5-076, CA5-087, CA5-088, CA5-091, CA5-092, CA5-094, CA6-005, CA6-070, CA6-071, CA6-072, CA6-076, CA6-079, CA6-080, CA6-083, CA6-084, CA6-085, CA6-086, CA6-087, CA6-088, CA6-089, CA6-090, CA6-094, CA6-098, CA6-099, CA6-102, CA6-104, COMP-002, COMP-015, COMP-019, COMP-058, COMP2-018, COMP2-031, COMP2-032, COMP2-049, COMP2-062, COMP2-073, COMP2-193, COMP2-195, COMP2-196, COMP2-209, COMP2-228, COMP2-229, COMP2-231, COMP2-233, COMP2-234, COMP2-238, COMP2-239, COMP2-249, COMP2-257, COMPOP-023, COMPOP-033, COMPOP-035, COMPOP-036, COMPOP-040, COMPOP-043, COMPOP-044, COMPOP-067, COMPOP-070, COMPOP-072, COMPOP-073, COMPOP-074, COMPOP-075, COMPOP-078, COMPOP-079, COMPOP-081, COMPOP-082, COMPOP-086, COMPOP-092, COMPOP-093, COMPOP-099, COMPOP-104, CONST-005, CONST-006, CONST-015, CONST-018, CONST-021, CONST-028, CONST-040, CONST-041, CONST-042, CONST-047, CONST-066, CONST-071, CONST-082, CONST-083, CONST-108, CONST-111, CONST-128, CONST-131, CONST-147, CONST-149, CONST-151, CONST-158, CONST-169, CONST-170, CONST-177, CONST-184, CONST-200, CONST-207, CONST-226, CONST-243, CONST2-001, CONST2-003, CONST2-005, CONST2-007, CONST2-009, CONST2-011, CONST2-013, CONST2-015, CONST2-017, CONST2-019, CONST2-021, CONST2-023, CONST2-025, CONST2-027, CONST2-029, CONST2-031, CONST2-033, CONST2-035, CONST2-037, CONST2-039, CONST2-041, CONST2-043, CONST2-045, CONST2-047, CONST2-049, CONST2-051, CONST2-053, CONST2-055, CONST2-057, CONST2-059, CONST2-061, CONST2-062, CONST2-063, CONST2-064, CONST2-076, CONST2-095, CONST2-096, CONST2-098, CONST2-099, CONST2-100, CONST2-101, CONST2-102, CONST2-104, CONST2-105, CONST2-106, CONST2-109, CONST2-110, CONST2-111, CONST2-112, CONST2-114, CONST2-115, CONST2-123, CONST2-128, CONST2-129, CONST2-132, CONST2-133, CONST2-141, CONST2-142, CONST2-158, CONST2-164, CONST2-170, CONST2-174, CONST2-178, CONST2-179, CONST2-196, CONST2-211, CONST2-219, CONST2-233, CONST2-246, CONST3-053, CONST3-061, CONST3-063, CONST3-077, CONST3-083, CONST3-091, CONST3-095, CSIT-022, CSIT-026, CSIT-030, CSIT-031, CSIT-032, CSIT-034, CSIT-037, CSIT-038, CSIT-039, CSIT-044, CSIT-046, CSIT-047, CSIT-055, CSIT-061, CSIT-066, CSIT-069, CSIT-071, CSIT2-003, CSIT2-026, CSIT2-089, CSIT5-031, CSIT5-045, CSIT5-052, CSIT5-056, CSIT5-069, CSIT5-074, CSIT5-076, CSIT5-078, CSIT5-089, CSIT5-105, CSIT5-109, CUL3-001, CUL3-005, CUL3-008, CUL3-010, CUL3-024, CUL3-026, CUL3-027, CUL3-031, CUL3-040, CUL3-043, CUL3-044, CUL3-047, CUL3-064, CUL3-070, CUL3-087, CUL3-106, CUL3-118, CUL3-119, CUL3-121, CUL3-142, CULT2-053, CULT2-177, CURH-012, CURH-015, CURH-023, CURH-052, CURH-060, CURH-064, CURH-066, CURH-069, CURH-071, CURH-161, CURH-351, CURH-373, CURH-391, CURH-427, CURR2-003, CURR2-014, CURR2-017, CURR2-023, CURR2-025, CURR2-032, CURR2-035, CURR2-036, CURR2-067, CURR2-071, CURR2-072, CURR2-089, CURR2-090, CURR2-091, CURR2-105, CURR2-107, CURR2-112, CURR2-127, CURR2-131, CURR2-133, CURR2-134, CURR2-137, CURR2-139, CURR2-141, CURR2-144, CURR2-146, CURR2-147, CURR2-148, CURR2-150, CURR2-151, CURR2-152, CURR2-153, CURR2-157, CURR2-158, CURR2-166, CURR2-170, CURR2-171, CURR2-173, CURR2-174, CURR2-209, DENT5-002, DENT5-003, DENT5-009, DENT5-014, DENT5-029, DENT5-034, DENT5-041, DENT5-046, DENT5-059, DENT5-062, ECO3-018, ECO3-019, ECO3-024, ECO3-029, ECO3-034, ECO3-049, ECO3-051, ECO3-058, ECO3-059, ECO3-061, ECO3-066, ECO3-071, ECO3-072, ECO3-076, ECO3-085, ECO3-094, ECO3-099, ECO3-116, ECON2-011, ECON2-016, ECON2-021, ECON2-023, ECON2-024, ECON2-026, ECON2-028, ECON2-057, ECON2-074, ECON2-077, ECON2-082, ECON2-098, ECON2-100, ECON2-103, ECON2-105, ECON2-131, ECON2-149, ECON2-150, ECON2-151, ECON2-153, EDU-031, ENG-012, ENG-015, ENG-020, ENG-030, ENG-047, ENG-065, ENG-071, ENG-077, ENG-085, ENG-086, ENG-092, ENG2-019, ENG2-020, ENG2-021, ENG2-030, ENG2-034, ENG2-038, ENGG-055, ENGG-057, ENGG-064, ENGG-067, ENGG-069, ENGG-071, ENGG-082, ENGG-099, ENGG-100, ENGG-101, ENGG-103, ENGG-110, ENGG-115, ENGV2-026, ENGV2-032, ENGV2-033, ENGV2-036, ENGV2-039, ENGV2-040, ENGV2-042, ENGV2-056, ENGV2-067, ENGV2-096, ENGV2-098, ENGV2-131, ENGV2-136, ENGV2-137, ENGV2-138, ENGV2-144, ENGV2-147, ENGV2-298, ENGV2-299, ENGV2-302, ENGV3-083, ENGV3-088, ENGV3-094, ENGV3-096, ENGV3-100, ENGV3-151, ENGV3-152, ENGV3-163, ENGV3-171, ENGV3-172, ENGV3-173, ENGV3-174, ENGV3-175, ENGV3-192, ENGV3-194, FOR2-001, FOR2-005, FOR2-017, FOR2-025, FOR2-059, FOR5-010, FOR5-013, FOR5-016, FOR5-035, FOR5-053, FOR5-067, FOR6-014, FOR6-016, FOR6-027, FOR6-035, FOR6-037, FOR6-041, FOR6-042, FOR6-043, FOR6-044, FOR6-046, FOR6-048, FOR6-050, FOR6-055, FOR6-062, FOR6-072, FOR6-073, FOR6-076, FSERV-001, FSERV-002, FSERV-003, FSERV-004, FSERV-005, FSERV-006, FSERV-007, FSERV-009, FSERV-012, FSERV-013, FSERV-014, FSERV-017, FSERV-018, FSERV-019, FSERV-020, FSERV-021, FSERV-022, FSERV-023, FSERV-026, FSERV-028, FSERV-032, FSERV-034, FSERV-036, FSERV-041, FSERV-042, FSERV-048, FSERV-049, FSERV-050, FSERV-051, FSERV-055, FSERV-063, FSERV-066, GEO2-061, GEO2-070, GEO2-094, GEO2-112, GEO2-227, GEO2-228, GEO2-237, HA-004, HA-021, HA-022, HA-028, HA-035, HA-036, HA-064, HA-074, HA-087, HA-092, HA-096, HA-107, HA-114, HA-119, HA-128, HA-148, HA-158, HA-172, HA-196, HARD2-141, HARD2-144, HARD2-226, HARD2-229, HARD2-230, HARD2-246, HARD2-301, HARD2-302, HARD2-303, HARD2-339, HARD2-348, HARD5-115, HARD5-116, HARD5-129, HARD5-257, HARD5-282, HARD5-306, HARD5-311, HARD5-324, HARD5-390, HARD5-391, HARD5B-044, HARD5B-045, HARD5B-046, HARD5B-047, HARD5B-048, HARD5B-130, HARD5B-137, HARD5B-147, HARD5B-232, HARD5B-309, HARD5B-310, HARD5B-312, HARD6-073, HARD6-093, HEAL2-001, HEAL2-003, HEAL2-007, HEAL2-008, HEAL2-012, HEAL2-013, HEAL2-016, HEAL2-024, HEAL2-028, HEAL2-029, HEAL2-035, HEAL2-039, HEAL2-040, HEAL2-042, HEAL2-043, HEAL2-046, HEAL2-051, HEAL2-054, HEAL2-059, HEAL2-063, HEAL2-065, HEAL2-073, HEAL2-078, HEAL2-085, HEAL2-098, HEAL2-099, HEAL2-112, HEAL2-123, HEAL2-126, HEAL2-141, HEAL2-152, HEAL2-163, HEAL2-164, HEAL2-187, HEAL2-188, HEAL3-007, HEAL3-011, HEAL3-015, HEAL3-020, HEAL3-021, HEAL3-022, HEAL3-028, HEAL3-037, HEAL3-193, HEALTH-005, HEALTH-006, HEALTH-007, HEALTH-013, HEALTH-016, HIST-008, HIST-014, HIST-048, HIST-060, HIST-072, HIST-074, HIST-079, HIST-080, HIST-082, HIST-083, HIST-084, HIST-085, HIST-096, HIST-102, HIST-113, HIST-187, HIST-199, HIST-206, HIST-208, HIST2-023, HIST2-040, HIST2-041, HIST2-043, HIST2-058, HIST2-159, HIST2-160, HIST2-162, HIST2-172, HIST2-173, HIST2-175, HIST2-205, HIST2-206, HIST2-207, HIST2-208, HIST2-212, HIST2-224, IOE-015, IOE-017, IOE-025, IOE-026, IOE-040, IOE-043, IOE-044, IOE-046, IOE-057, IOE-064, IOE-065, IOE-067, IOE-068, IOE-071, IOE-074, IOE-075, IOE2-018, IOE2-032, IOE2-043, IOE2-045, IOE2-046, IOE2-047, IOE2-058, IOE2-059, IOE2-087, IOE2-088, IOE2-091, IOE2-092, IOE2-098, IOE5-079, IOE5-080, IOE5-081, IOE5-082, IOE5-083, IOE5-084, IOE5-085, IOE5-090, IOE5-099, IOE5-101, IOE5-103, IOE5-106, IOE5-107, IOE5-110, IOE5-115, IOE5-116, IOE5-138, IQ-011, IQ-016, IQ-018, IQ-030, IQ-032, IQ-034, IQ-039, IQ-040, IQ-047, IQ2-121, IQ2-127, IQ2-128, IQ2-136, IQ2-141, IQ2-145, IQ2-150, IQ2-151, IQ2-156, IQ2-157, IQ2-162, IQ2-176, IQ2-209, IQ2-229, IQ2-240, IQ2-242, IQ2-318, IQ2-342, IQ3-050, IQ3-080, IQ3-082, IQ3-086, IQ3-090, IQ3-098, IQ3-101, IQ3-126, IQ3-134, IQ3-135, IQ3-139, IQ3-140, IQ3-141, IQ3-143, IQ3-149, IQ3-165, LAB-011, LAB-021, LAB-038, LAB-044, LAB-059, LAW2-025, LAW2-046, LAW2-089, LAW5-001, LAW5-002, LAW5-005, LAW5-027, LAW5-047, LAW5-052, LAW5-053, LAW5-054, LAW5-057, LAW5-063, LAW6-033, LAW6-059, LAW6-065, LAW6-077, MATH-064, MATH2-165, MATH2-166, MATH2-173, MATH2-177, MATH2-223, MATH2-305, MATH2-307, MATH2-310, MATH2-346, MATH3-085, MATH3-086, MATH3-096, MATH3-099, MATH3-101, MATH3-155, MATH3-159, MATH3-161, MATH3-198, MECEE-025, MECEE-032, MECEE-077, MECEE-078, MECEE-094, MECEE-097, MECEE-133, MECEE-134, MECEE-141, MECEE-144, MECEE-180, MECEE-181, MECEE-182, MECEE-183, MECEE-184, MECEE-186, MECEE-189, MECEE-190, MECEE-191, MECEE-192, MED-001, MED-017, MED-050, MED-059, MED-083, MED-085, MED-092, MED-093, MED-114, MED-143, MED-146, MED-154, MED-156, MED-157, MED-172, MED-183, MED-200, NEC-007, NEC-009, NEC-021, NEC-023, NEC-036, NEC-037, NEC-043, NEC-048, NEC-059, NEC-064, NEC-070, NEC-084, NEC-085, NEC-086, NEC-087, NEC-091, NEC-092, NEC-107, NEC-108, NEC-116, NEC-136, NEC-146, NEP-034, NEP-035, NEP2-020, NEP2-027, NEP2-033, NEP2-034, NEP2-052, NEP2-067, NEP2-122, NEP2-124, NEP2-138, NEP2-178, NEP2-184, NEP2-190, NEP2-202, NEP2-208, NEP2-257, NEP3-001, NEP3-031, NEP3-034, NEP3-060, NEP3-089, NEP3-101, NEP3-160, NEP3-217, NEP3-218, NEP3-220, NEP3-234, NEP3-245, NLEM-133, NRBO-001, NRBO-006, NRBO-014, NRBO-017, NRBO-019, NRBO-033, NRBO-037, NRBO-039, NRBO-044, NRBO-045, NRBO-050, NRBO-054, NRBO-061, NRBO-068, NRBO-107, NRBO-112, NRBO-128, NRBO-130, NRBO-131, NRBO-135, NRBO-139, NT2-074, NT2-080, NTEL-004, NTEL-014, NTEL-019, NTEL-022, NTEL-027, NTEL-036, NTEL-044, NTEL-049, NTEL-051, NTEL-052, NTEL-059, NTEL-061, NTEL-062, NTEL-067, NTEL-070, NTEL5-020, NTEL5-041, NTEL5-045, NTEL5-049, NTEL5-063, NTEL5-067, NTEL5-068, NTEL5-088, NTEL5-101, NTEL5-112, NUR-023, NUR-048, NUR-136, NUR-181, OFF2-052, OFF2-196, OPT-008, OPT-051, PHY-005, PHY-059, PHY-063, PHY-072, POL-038, POL-040, POL-046, POL-050, POL-057, POL-071, POL-072, POL-073, POL-087, POL-089, POL-090, POL-092, POL-093, POL-094, POL-095, POL-096, POL-097, POL-099, POL-102, POL-103, POL3-002, POL3-024, POL3-041, PUB-015, PUB-016, PUB-017, PUB-027, R6A-A006, R6A-A026, R6A-A052, R6A-A084, R6A-A087, R6A-A099, R6A-A105, R6A-A133, R6A-A143, R6A-A284, R6A-A293, R6A-A296, R6A-A299, R6A-A310, R6A-A317, R6A-A322, R6A-A323, R6A-A334, R6A-A337, R6A-A338, R6A-A339, R6A-A341, R6A-A360, R6A-A386, R6A-A400, R6A-A442, R6A-A454, R6A-A478, R6A-A534, R6A-A558, R6A-B116, R6A-B117, R6A-B163, R6A-B173, R6A-B200, R6A-B203, R6A-B244, R6A-B267, R6A-B269, R6A-B274, R6A-B275, R6A-B278, R6A-B288, R6A-B289, R6A-B378, R6A-B404, R6A-B405, R6A-B422, R6A-B423, R6A-B425, R6A-B426, R6A-B427, R6A-B428, R6A-B433, R6A-B434, R6A-B435, R6A-B462, R6A-B493, R6A-B495, R6A-B497, R6A-B498, R6A-B506, R6A-B508, R6A-B517, R6A-B520, R6A-B521, R6A-B534, R6A-B540, R6A-B548, R6A-B569, R6A-B581, R6A-B589, R6A-B602, R6A-B620, R6A-B628, R6A-C123, R6A-C127, R6A-C129, R6A-C135, R6A-C138, R6A-C145, R6A-C151, R6A-C283, R6A-C292, R6A-C303, R6A-C307, R6A-C308, R6A-C309, R6A-C310, R6A-C330, R6A-C331, R6A-C332, R6A-C335, R6A-C345, R6A-C383, R6A-C394, R6A-C429, R6A-C430, R6A-C434, R6A-C435, R6A-C436, R6A-C437, R6A-C439, R6A-C445, R6B-001, R6B-013, R6B-027, R6B-033, R6B-044, R6B-048, R6B-059, R6B-078, R6B-083, R6B-086, R6B-087, R6B-096, R6B-106, R6B-111, R6B-112, R6B-120, R6B-125, R6B-126, R6B-135, R6B-146, R6B-156, R6B-160, R6B-164, R6B-168, R6B-181, R6B-190, R6B-216, R6B-247, R6B-267, R6B-286, R6B-296, R6B-302, R6B-312, R6B-320, R6B-329, R6B-352, R6B-359, R6B-397, R6B-433, R6B-438, R6B-444, R6B-452, R6B-460, R6B-464, R6B-465, R6B-469, R6B-471, R6B-473, R6B-474, R6B-477, R6B-479, R6B-488, R6B-491, R6B-509, R6B-514, R6B-526, R6B-535, R6B-538, R6B-541, R6B-548, R6B-549, R6B-555, R6B-560, R6B-561, R6B-571, R6B-574, R6B-577, R6B-580, R6B-611, R6B-614, R6B-618, R6B-625, R6B-630, R6B-637, R6B-660, R6B-673, R6B-674, R6B-675, R6B-679, R6B-684, R6B-685, R6B-686, R6B-690, R6B-698, R6B-704, R6B-712, R6B-714, R6B-715, R6B-719, R6B-721, R6B-722, R6B-730, R6B-731, R6B-736, R6B-B-005, R6B-B-011, R6B-B-013, R6B-B-014, R6B-B-018, R6B-B-019, R6B-B-026, R6B-B-029, R6B-B-042, R6B-B-078, R6B-B-088, R6B-B-092, R6B-B-118, R6B-B-122, R6B-B-135, R6B-B-179, R6B-B-183, R6B-B-195, R6B-B-228, R6B-B-245, R6B-B-247, R6B-B-248, R6B-B-249, R6B-B-252, R6B-B-254, R6B-L-006, R6B-L-026, R6B-L-038, R6B-L-042, R6B-L-059, R6B-L-062, R6B-L-072, R6B-L-092, R6B-L-172, R6B-L-210, R6B-L-233, R6B-L-244, R6B-L-247, R6B-L-265, R6B-L-275, R6B-L-319, R6B-L-320, R6B-L-329, R6B-L-340, R6B-L-341, R6B-L-406, R6B-L-407, R6B-L-451, R6B-L-452, R6B-L-453, R6B-L-477, R6B-L-483, R7A-L001, R7A-L005, R7A-L010, R7A-L017, R7A-L024, R7A-L035, R7A-L048, R7A-L075, R7A-L083, R7A-L087, R7A-L089, R7A-L109, R7A-L125, R7A-L129, R7A-L133, R7A-L186, R7A-L188, R7A-L207, R7A-L223, R7A-L228, R7A-L232, R7A-L236, R7A-L241, R7A-L242, R7A-L249, R7A-L259, R7A-L266, R7A-L269, R7A-L272, R7A-L273, R7A-L304, R7A-L305, R7A-L337, R7A-L358, R7A-L382, R7A-L397, R7A-L411, R7A-L412, R7A-L423, R7A-L424, R7A-L426, R7A-L435, R7A-L439, R7A-L448, R7A-L450, R7A-T007, R7A-T021, R7A-T171, R7A-T187, R7A-T202, R7A-T203, R7A-T222, R7A-T229, R7A-T230, R7A-T231, R7A-T233, R7A-T235, R7A-T241, R7A-T244, R7A-T248, R7A-T252, R7A-T263, R7A-T264, R7A-T266, R7A-T267, R7A-T274, R7A-T303, R7A-T369, R7A-T371, R7A-T415, R7A-T418, R7A-T439, R7A-T444, R7A-T447, R7A-T451, R7A-T452, R7A-T457, R7A-T466, R7A-T476, R7A-T480, R7A-T481, R7A-T484, R7A-T490, R7A-T493, R7B-036, R7B-039, R7B-042, R7B-144, R7B-212, R7B-218, R7B-220, R7B-223, R7B-224, R7B-225, R7B-227, R7B-255, R7B-264, R7B-281, R7B-287, R7B-294, R7B-323, R7B-338, R7B-339, R7B-354, R7B-391, R7B-426, R7B-658, R7B-673, R7B-680, R7B-687, R7B-699, R7B-720, R7B-767, R7B-769, R7B-770, R7B-771, R7B-780, R7B-786, R7B-794, R7B-798, R7B-800, R7B-801, R7B-802, R7B-803, R7B-807, R7B-832, R7B-861, R7B-863, R7B-869, R7B-870, R7B-880, R7B-881, R7B-882, R7B-887, R7B-888, R7B-899, R7B-909, R7B-913, R7B-915, R7B-929, R7B-937, R7B-939, R7B-950, R7B-956, R7B-974, R7B-978, R7B-979, R7B-986, R7B-998, RAD-016, RAD-021, RAD-035, RAD-076, SCI2-006, SCI2-010, SCI2-043, SCI2-047, SCI2-052, SCI2-065, SCI2-076, SCI2-079, SCI2-080, SCI2-083, SCI2-084, SCI2-095, SCI2-100, SCI2-105, SCI2-107, SCI2-109, SCI2-116, SCI2-129, SCI2-130, SCI2-138, SCI2-142, SCI2-148, SCI2-157, SCI2-158, SCI2-159, SCI2-165, SCI2-178, SCI2-195, SCI2-201, SCI3-041, SCI3-042, SCI3-043, SCI3-064, SCI3-090, SCI3-092, SCI3-093, SCI3-097, SCI3-108, SCI3-110, SCI3-112, SCI3-123, SCI3-125, SCI3-126, SCI3-129, SCI3-130, SCI3-134, SCI3-135, SCI3-144, SCI5-003, SCI5-004, SCI5-011, SCI5-016, SCI5-018, SCI5-019, SCI5-022, SCI5-023, SCI5-025, SCI5-026, SCI5-028, SCI5-031, SCI5-032, SCI5-035, SCI5-036, SCI5-047, SCI5-048, SCI5-053, SCI5-055, SCI5-059, SCI5-060, SCI5-061, SCI5-062, SCI5-063, SNPSC-058, SNPSC-068, SNPSC-071, SNPSC-074, SNPSC-085, SNPSC-089, SNPSC-094, SNPSC-100, SNPSC-102, SNPSC-114, SUBENG-001, SUBENG-026, SUBENG-037, SUBENG-050, SUBENG-085, TECH2-003, TECH2-006, TECH2-012, TECH2-047, TECH2-050, TECH2-053, TECH2-054, TSCLS-001, TSCLS-002, TSCLS-003, TSCLS-024, TSCLS-045, TSCLS-092
```

## Round 8 + Round 10 integration (2026-10-26, final integrator)

Bank 38,874 (coordinator-verified at handoff) → **46,415** in 79 files; 608 fun facts unchanged. Three more R10 files landed mid-integration (iq3/maths4, then iq4/maths5, then english3/maths6); the fast checks were re-run after each landing. No GitHub upload. Chain: 20,132 (post-audit old bank) + 2,000 R8 + 27,224 R10 gross − 1,524 prior-sweep removals (old bank) − 1,417 this integration = 46,415. R8 net 1,946; R10 net 25,887; old bank 18,582. Previous Year 2083: zero questions removed.

### CORRECTION to the §Dedupe sweep "Out of scope" note above
That section repeats the coordinator brief's claim that R8LAW-431/436/443 duplicate CONST-008/CONST2-235/HIST-037. Verified false by reading the questions: CONST-008 asks how many rural municipalities (460); R8LAW-431 asks which tax is levied by the local level (Property tax) — different question. CONST2-235 asks the term of a provincial assembly (5 years); R8LAW-436 asks who administers the CM's oath (Province Chief) — different question. HIST-037 asks who was the first woman Chief Justice (Sushila Karki); R8LAW-443 asks which court tries CIAA cases (Special Court) — different question. R8LAW-431 and R8LAW-436 are unique and KEPT. R8LAW-443 IS a duplicate, but of R8LAW-107 in the same file ("Which court hears corruption cases filed by the CIAA?"), not of HIST-037; R8LAW-443 was removed, R8LAW-107 kept. The R10-WORLD-0632/0685/0719 claim in the same brief was accurate — they were exact-stem dups of R10-OEL-0285/0115/0251 and were removed in the exact-stem round below.

### Removals in this integration: 1,417
- **Exact stems (test-questions.js), 837:** english2 520, maths3 83, iq2 15, maths 12, health2 6, world-science 3, science2 1; iq3 9, maths4 106, iq4 64, english3 11, maths6 7. Newer copy removed in every case; 637/640 of the first batch had different (reshuffled) distractors but the identical stem and the same tested word — same question, not a new one.
- **Exact rewordings (dedupe report), 25:** R8CUR-219 (dup NEP-037 केटा plural), R8SCI-133 (SCI2-097 laughing gas), R8NEP-313 (CULT2-031 Nepali earlier name), R8NEP-114 (HIST2-229 Birendra coronation 1975), R10-MATH3-0998/0999 (R10-DRILL-1163/1164, 12h/24h→minutes), R10-ENG2-0953/1325 (धैर्यवान/मूल्यवान spelling variants), R10-HEALTH-0219 (vitamin D), R10-IQ2-1208/1194/1199 (1st/2nd/3rd-from-right typo variants), R10-IQ-3785 (R7B-101 Bird:Nest::Bee:Hive), R10-NEP2-0251 (चोरको खुट्टा काट्नु), R10-WORLD-0714/0624/0622 (BRICS 2009, WAN, SQL), R8NEP-400/489 (SLR, NEPSE), R8CUR-306/291 (RTGS, IPO), R8CUR-209 (रामले कारक), R8SCI-332 (FCHV), R8NEP-490 (SEBON), R8SCI-321 (ORS).
- **Same-fact rewordings, 9:** R8NEP-281 (Thangka/Buddhism, dup CULT2-073), R8NEP-452 (load shedding ended 2018, dup SCI5-044), R8SCI-222 (female XX, dup R6A-B179), R8CUR-280 (BAFIA 2073, dup R6B-B-001), R8SCI-177 (STP 22.4 L, dup R7A-T468), R8NEP-402 (NRB monetary policy yearly, dup R8LAW-392), R8SCI-070 (F=ma, dup SCI3-096), R8SCI-195 (most malleable gold, dup SCI3-019), R8SCI-281 (Gram-positive purple, dup ALLIED-007).
- **Near rewordings (old bank ↔ R8/R10, all 60 hand-reviewed), 43:** R8NEP-113/394/168/431/183, R8LAW-104/442/371/044/394/004/308/443, R8SCI-199/211/135/136/302/178/179/128/301/309/356/353, R8CUR-202/204/229/230/467/221/222/303, R10-WORLD-0575/0623/0621/0560/0214, R10-NPL-0099, R10-ENG2-1721, R10-HEALTH-0005/0249, R10-OEL-0285 (full list + keepers in TESTING.md §Q).
- **Template-paraphrase / parameter-swap pairs (payload-verified), 503** from 505 genuine pairs (greedy star clustering; keeper = earliest file/id; 487 keepers): same problem restated with swapped commutative parameters (mixture quantities, rectangle length/width, train/platform lengths, SI rate↔years, HCF number order, multiplication order, district-HQ reversal, direction-walk leg swaps) or a template paraphrase (Nepali "Choose the antonym of X" vs "Which word is opposite in meaning to X", same word/options/answer). By file: r10-nepali 153, r10-iq 104, r10-maths2 38, r10-maths 26, r10-maths5 24, r10-maths3 22, r10-nepali2 18, r10-maths4 16, r10-iq4 15, r10-nepal-facts 14, r10-maths6 13, r10-iq2 13, r10-iq3 10, r10-drills 10, r5-maths-hard 14, r5-csit-ioe 6, hard-core-v2 2, thin-topics 1, core-hard 1, iq-maths 1, thin-exams 1, science2 1. 6 keepers gained exam tags from removed copies (CURR2-057, IOE5-139, R10-MATH-1085/1090/1100, R10-NPL-0775).

### Method note — why the dedupe script's numbers are not the removal numbers
The full `dedupe-check.py` run (38,234 q) classified 7,486 pairs, of which 7,484 involve R8/R10 files and were deferred by design. Sampling showed the bulk are false positives of template density: different letter series sharing a next letter and ≥3 options, different seating rows, different names in blood-relation problems, different prepositions (proud of vs fond of), different vocab words (idle vs lazy), different districts — same template, different data. Only the (a) exact, (d) same-fact and hand-reviewed cross-bank near pairs were taken from that report. The remaining genuine class was found with an O(n) payload-grouping sweep (scripts in /tmp: payload_test.py, payload_sweep.py — matra-preserving tokeniser, quoted-span equality, ordered-sequence veto; the script's normalise() strips Devanagari vowel signs, collapsing distinct words to consonant skeletons, which is why its NE Jaccard runs 0.8–1.0 on template pairs and why its NE-only flags need the payload check). A re-run of the full script against the moving bank was killed after ~20 min (candidate generation explodes on dense template families) and superseded by the sweep, which covers the final disk state in ~9 s. Sample validation: 30 flagged-genuine + 30 rejected + 15 sweep-only pairs, all judged correctly; the sweep found 150 genuine pairs the script never classified (stem Jaccard < 0.8, e.g. district-HQ reversals and parameter swaps).

### Rejected (reviewed, kept)
- **MECEE-030 (plan's only removal): REJECTED.** MECEE-029 asks which gland secretes ADH, MECEE-030 which secretes Oxytocin — different hormones, same gland. Flagged only via NE Jaccard 0.812 (identical Nepali template). Both kept; the plan file was not applied.
- **R10-ENG2-0683** ('भोक' hunger) vs R10-ENG-0875 ('भोको' hungry): the script's transliteration rule equated hungry/hunger (difflib ≥ 0.7, shared prefix). Different words, different answers. Kept.
- **R8CUR-462** ('केटी' plural) vs NEP-037/R8CUR-219 ('केटा' plural): different words. Kept (R8CUR-219 itself removed as the केटा dup).
- **11 letter-series same-fact pairs** in r10-iq: different series, different problems.
- **Compound questions:** R8LAW-050 (HoR total + PR seats) vs CONST-013 (PR seats only); R8LAW-002 (schedules + articles) vs CONST-048 (schedules only); R8CUR-083 (Operation Sindoor + 7 May 2025 date) vs CURH-030 (name only). The added fact makes a different test item.
- **Different-word template collisions:** केटा/केटी, जल/निद्रा/रानी, अमृत/शान्त, lucid/brilliant/intelligent/pure, obscure/dirty, राजा/नेता feminine, काम/हात synonyms, दाजु/विद्वान् feminine, खुसी/सुख, लेख्नु/खेल्नु tenses, प्रेम/माया synonyms, different/opposite/modern antonyms (all coincidentally share an answer).
- **Different sub-questions / directions:** Losar vs 'Lo'; IP vs TCP/IP; RIPE combination vs single first-line drug; largest ocean vs largest (river/ocean/lake/pond); R10-WORLD-0306 vs IQ-100.
- **Seating rows, walk directions, mixture quantities, alphabet positions** with different data: different problems even when the keyed answer coincides.
- **652 excluded identical-stem/different-key pairs** from the dedupe report (template stems, key conflicts): kept, per the script's own rule.

### Answer-key audit (R8/R10 only; old bank already audited in §P)
`python3 scripts/audit-answer-mismatch.py` — 326 flags total, 303 in R8/R10, **all verified false positives, zero keys changed.**
- 166 EXPL_NAMES_OPTION flags: the regex misreads "The answer is <text>" — the explanation names the marked option's text and its initial letter looks like an option letter ("About", "Argentina", "Aedes", "Daughter", "Brother"). Verified by named-text == marked-option check on all 166.
- 137 NE_CONCLUDES flags: the "last '=' value" heuristic misreads intermediate values in the Nepali explanation. 67 remainder drills recomputed (a mod b — all correct); 70 unit-digit questions recomputed (pow(base, exp, 10) — all correct); 2 letter-value sums recomputed (A+X=25, A+A=2 — both correct). R8 files: zero flags in both audit runs.
- The 23 flags in old files are the same false-positive classes left over from §P (not re-audited).

### Counts / tests / bundle
46,415 questions in 79 files, 608 fun facts, bilingual 100%. Difficulty 10,615 easy / 24,487 medium / 11,313 hard; answer balance A 28.0% / B 24.6% / C 23.9% / D 23.5% (A-skew from the R10 drill banks; options are shuffled at runtime). All six suites pass (test-questions, test-funfacts, test-app, test-e2e, test-v2, test-bundle). Bundle rebuilt: loksewa-prep-nepal-full.html, 42,181,611 bytes, md5 8082139443631565c6532ffd87021344. R8 counts (law writer's handoff never arrived; read from disk): law-office 500 (Law 214, Foreign Service & Diplomacy 143, Office Management & Public Service 143), nepal 500 (Economy & Development 133, Culture & Society 130, Nepal History 125, Nepal Geography 112), science-health 500 (Physics 152, Chemistry 127, Health/Technical basics 112, Biology 109), current-language 500 (Current Affairs 179, Nepali Language 124, English 115, Banking & Finance 82) — all 100% bilingual; after this integration's removals the live counts are 492 / 487 / 480 / 487.

### Still open (carried forward)
- The audit script's two false-positive modes (above) will re-flag the same ~300 on the next run — fix the script (named-text check before the option-letter regex; conclude from the final sentence's "is/are/हो" value, not the last '=' value) before the next audit.
- The dedupe script's NE Jaccard is unreliable for Devanagari (matra stripping) — NE-only near flags need the payload check.
- A 28.0% A-position skew in the R10 drill banks (harmless at runtime due to shuffling, but worth a rebalance pass if the bank is ever served unshuffled).
- No real-browser smoke test yet; human accuracy + Nepali spot-check still recommended before GitHub upload.

## Round 10 — Self-audit as an aspirant + wiring check (2026-10-27, ~00:10–00:40 NPT)

Read-only audit plus small wiring/code fixes. No question files touched; no GitHub upload; bundle NOT rebuilt (parent integrates). Walked every view in code (assets/js/app.js, 1,872 lines, fully read) and exercised the flows through the Node DOM-stub suites (test-app / test-e2e / test-v2), which drive the real app.js against real data on disk.

### Wiring — QUESTION_FILES (fixed)
- data/questions/ holds **85 files**, not 84 as briefed. app.js listed 82. Missing: `community-approved.json` (empty, 0 q), `expansion-r10-english4.json` (473 q), `expansion-r10-maths8.json` (394 q). All three added, list re-verified identical + sorted vs disk (85 = 85).
- Load check: exams 47, papers 17, notices 10, fun facts 608 — all fetched in loadData with embedded-data fallbacks for the bundle (EMBEDDED_PAPERS / EMBEDDED_NOTICES / EMBEDDED_FUNFACTS). All 85 files load; every question has marks, exam array, topic, difficulty, 4 options + answer (0 missing across the bank); 0 duplicate ids.
- Every prelim exam has a tagged pool ≥ its mock size (thinnest: engineering 590 vs 50 needed; nmc-bds 677 vs 180). No mock falls back to the general bank today.

### Walkthrough — all views pass (code read + stub tests)
- **Home:** live counts (#q-count / #exam-count / topics), QOTD (+10 XP once/day, second tap earns nothing), daily fact + fact streak (+5 XP once/day), weekly challenge, focus timer, all 8 trending cards point at real topics.
- **Practice:** difficulties/counts (5/10/20/50), timer on/off (~54 s/Q fallback when the exam's timeMin is null), negative marking per exam (20% PSC, 0% licence, 25% MECEE-BL). All-correct 10Q scores 100% PASS; randomisation verified (question + option order differ across sets; options_ne shuffles with the same permutation).
- **Mock:** Kharidar 50Q/45 min, 25 right / 25 wrong → 40/100 FAIL vs cutoff 45; OMR palette renders (mock-only) and jumpTo works; countdown auto-submits on time-out; result screen shows score ring, per-exam negative line, topic breakdown, wrong-answer review. TSC licence mock untimed + no deduction (negative null); NNC-RN all-wrong = 0/150; NMC MBBS 130/130 PASS with the CSQ note.
- **Wrong-answer review / retry-wrong-only:** retryWrong re-quizzes exactly the wrong set; Review view lists bookmarks + mistakes with answers, explanations, Discuss/Report buttons; wrong answers auto-save to mistakes.
- **Flashcards:** 20 cards, reveal, exam filter falls back to the full bank for 0-tagged exams (jta/ranger).
- **Daily Challenge:** deterministic per day (same seed → same 10Q); repeat asks first and gives no extra XP.
- **Quick Quiz (5Q), Speed Round (10Q/60 s, +1 bonus <5 s, best saved, share-to-clipboard), Mistake Marathon** (mistakes/bookmarks only; friendly empty state with no material) — all verified.
- **Bookmarks & Mistakes:** bookmark saves, clear-all asks for confirmation.
- **Discussion Hub:** 9 seeded threads (one per exam + General), post/reply/upvote/report all stored locally.
- **Submit a Question:** validation (bilingual fields, 4 distinct options, source required), exact + near-duplicate detection (Jaccard ≥ 0.8), spam + 5/hour rate limit, moderation approve/reject/edit, approved questions join the live bank with a Community badge.
- **Old Papers:** 17 papers; 3 transcribed (NaSu 43 + Kharidar First 45 + Koshi 45 = **133** — see fix below). practicePaper keyword+date matching verified for all three.
- **Notices:** 10 notices, scope/body/status filters, effective-status logic (past close_date → closed), official-links block.
- **Fun Facts:** 608 facts, all 8 categories, category filter counts, deterministic daily fact, interstitial after every 5th practice question (dismissable, never blocking), Fact Explorer badge at 10.
- **Profile / demo sign-in:** Gmail-only demo sign-in, sign-out keeps user_id, profile stats + weak topics from mistakes.

### Fixed in this round
1. **QUESTION_FILES +3 files** (above) — 867 questions were unloadable (english4 473 + maths8 394).
2. **index.html: "134 real questions" → "133"** — previous-year-2083.json is 43+45+45 = 133; the 134 was wrong.
3. **app.js renderSubmit: stale '6,846' fallback** — when the bank fails to load it printed a 3-round-old total. Now prints the live count when loaded and no number when not (`duplicate detection against the full bank (49,750 questions)`).
4. **app.js renderResult: CSQ note was generic** — any mock whose max ≠ prelim.total showed "the 10 clinical scenario questions are not in this mock". Only nmc-mbbs has total ≠ questions×marksPerQ, so the note is now scoped to `c.exam === 'nmc-mbbs'`; a short mock on any other exam no longer mislabels itself.
5. **test-app.js QUESTION_FILES check** updated to include community-approved.json (it previously excluded it as "not a bank file").
6. **test-e2e.js / test-v2.js load-count checks de-hard-coded** — 48,883 → computed from disk at run time. A fixed number goes stale within minutes while the dedupe worker runs; the check still proves loadData loads every file on disk. Computed BEFORE loadData with one retry per file: one run caught a file mid-write by the concurrent dedupe worker (torn JSON, `JSON.parse` crash at position 308122) — transient, all files parse cleanly on re-read.

### Still open (found in this round, not fixed)
- **Daily Challenge: abandoning burns the day.** `dailyDone[date]` is marked at start, before finishing — quit mid-challenge and the repeat is XP-free even though the first attempt was never finished. Mark it on finish instead.
- **Dashboard "Reset progress" is partial.** It resets XP/streak/attempts/bookmarks/mistakes but leaves the fact streak (`loksewa_fact_streak_v1`), Speed Round best (`loksewa_speed_best_v1`), discussions, submissions and reports behind — "reset ALL progress" overpromises.
- **Submit-a-question double-submit.** The duplicate check runs against the bank only; the spam check blocks at 3 identical queue entries, not 2 — the same question can be queued twice, and the form is not cleared after a successful submit.
- **community-approved.json double-load edge.** It is now in QUESTION_FILES *and* localStorage-approved questions load via `communityApprovedQuestions()`. If approved questions are ever committed to the file while the same questions still sit in localStorage, they load twice. The commit flow should clear LS_APPROVED after download/commit — nothing does today. (File is empty now, so no live effect.)
- **test-bundle.js still expects 48,883 embedded questions.** The bundle (44,054,188 bytes) embeds the old 82-file QUESTION_FILES — stale by design, rebuild pending with the parent. Do not "fix" the test without rebuilding the bundle.
- **Notices "Last checked 2026-10-26".** Two notices close today 2026-10-27 (Nepal Police ASI, Gandaki 9/8) and still show "Closing soon" on their last day — correct per the data, but re-check is due today.
- **loadData has no retry on torn reads.** If the concurrent dedupe worker rewrites a file while loadData fetches it, that file is silently skipped (console warning) and the bank is temporarily short. Only observed once, in the test harness, not in the app.
- **Dead code (harmless):** `renderMockTable` still carries a `p.negative===0.4` legacy branch — no exam stores 0.4 anymore.
- Carried forward from earlier rounds: no real-browser smoke test yet; human accuracy + Nepali spot-check still recommended before GitHub upload.

### Counts / tests at finish (2026-10-27 ~00:40 NPT)
- Bank on disk: **49,750 questions in 85 files** (was 50,613 at the start of this audit ~00:10, 50,201 per the 00:09 brief — the parallel dedupe worker removed ~863 during this audit; the count is still moving, re-count after it finishes). 608 fun facts, 47 exams, 17 papers, 10 notices. Difficulty/answer-balance not recomputed here (dedupe in flight).
- `node scripts/test-app.js` — **178 PASS, 0 FAIL**. `node scripts/test-e2e.js` — **89 PASS, 0 FAIL**. `node scripts/test-v2.js` — **43 PASS, 0 FAIL**. `node scripts/test-questions.js` — **ALL PASS** (it was failing on duplicates per the 00:09 brief; the parallel worker's fixes appear to have landed during this audit).
- test-bundle.js NOT run to pass (stale bundle, see above).

## Round 10 — Dedupe clean-up (2026-10-27, ~00:10–00:50 NPT)

Task: full dedupe sweep (exact + near Jaccard ≥0.8 + same-fact), fix `expansion-r10-english4.json`, `test-questions.js` must pass. No GitHub upload, no bundle rebuild (parent integrates).

### What actually happened — a parallel dedupe worker was doing the same job
A parallel dedupe worker was actively rewriting R10 files throughout this round (files changing 18:22–18:45 UTC; new files `expansion-r10-vocab5.json`, `expansion-r10-maths9.json`, `expansion-r10-iq6.json`, later `expansion-r10-maths10.json`, `expansion-r10-vocab6.json`). It removed the exact 863 duplicates this task briefed — **before I applied anything** — so my contribution was: verify those removals were correct, run the deeper near/same-fact sweep, and remove the 157 further genuine duplicates the worker's exact-text pass could not see. The bank is a moving target while the worker runs; counts below are timestamped.

### Counts
- 00:10 NPT (brief): 50,201; `node scripts/test-questions.js` at 00:10 measured **50,613** (0 broken JSON, 608 fun facts) and FAILED with 863 duplicate-text failures.
- Worker adds new files → 52,088 in 88 files (00:20 NPT); worker dedupe → 50,870.
- After my 157 removals: **50,713 questions in 90 files**, bilingual 100% (50,713/50,713), 0 duplicate ids, 0 duplicate texts.
- `node scripts/test-questions.js` — **ALL QUESTION CHECKS PASSED ✔** (final run 00:46 NPT). `QUESTION_FILES` in `assets/js/app.js` already lists all 90 files (verified by script, 90 = 90) — no wiring fix needed.

### The 863 worker removals — verified correct (not performed by me)
- `expansion-r10-english4.json` 1318 → 473 (**845 removed**): every removed stem duplicated a question in `expansion-r10-english3.json` (822), `-english2.json` (15) or `-english.json` (8). 826 of the 845 pairs shared the same correct answer; the other 19 are listed under "Answer disagreements" — both versions valid, english4 copy removed, no key changed. No within-file duplicates existed in english4. Verified by exact-normalised-text grouping on the 1318-question version before the worker rewrote the file; the removal count matches the measured duplicate count exactly (845).
- `expansion-r10-maths8.json` 412 → 394 (**18 removed**): clock-angle questions duplicating `expansion-r10-maths3.json`. The maths8 copies were **wrong**: they keyed truncated integers (172, 127, 7, 67, …) while the true angles are X.5°. Recomputed all 18 with angle = min(|30H − 5.5M|, 360 − |30H − 5.5M|); the maths3 copies key the correct .5 values, and all 64 clock-angle questions in maths3 re-verify correct. Removed maths8 ids: R10-M8-0241, 0242, 0243, 0244, 0247, 0248, 0251, 0252, 0255, 0257, 0258, 0276, 0278, 0280, 0282, 0284, 0289, 0290 (times 9:15, 4:45, 3:15, 5:15, 2:45, 6:45, 7:45, 10:45, 5:45, 10:15, 8:45, 11:15, 9:45, 1:45, 3:45, 11:45, 2:15, 1:15).

### My 157 removals (applied 19:00 UTC via `scripts/audit-duplicates.py --apply`)
Full plan saved at `audit-patches/dedupe-round10-2026-10-27.json` (remove list + tag merges + per-group notes). All groups verified on current disk before applying (same option set + same key within each group); worker had been quiet ~15 min.
- **Odd-one-out, 143 removed (45 sets, all in `expansion-r10-iq3.json`)**: same 4-number set listed in different orders, same key, identical options/explanations/tags within each set — keep lowest id per set. Worst sets: {35,36,37,38} ×10 (keep R10-IQ3-0684), {11,12,14,16} ×9 (keep R10-IQ3-0783), {143,144,145,146} ×8, {63,64,65,66} ×8, {19,20,22,24} ×8, {23,24,26,28} ×8. Full keep/remove lists in the plan JSON. Why the sweep missed most of these: `numbers_compatible`'s neighbour-context check fails when the same set is listed in very different orders — list-template families need direct set-grouping (see script notes).
- **Multiplication (commutative), 7 removed (`expansion-r10-maths9.json`)**: keep lower id — R10-M9-1182 (1.25×3.6=4.5) over 1198; R10-M9-1185 (5.5×0.8=4.4) over 1219; R10-M9-1186 (5.5×3.3=18.15) over 1205; R10-M9-1190 (5.5×1.8=9.9) over 1201; R10-M9-1193 (3.6×4.5=16.2) over 1225; R10-M9-1199 (1.2×5.5=6.6) over 1233; R10-M9-1214 (3.3×2.2=7.26) over 1217. All products re-verified.
- **Analogy reversals, 5 removed (`expansion-r10-iq.json`)**: same analogy asked forward and reversed, same answer — keep the iq3 reversed version (fuller EN+NE explanation, marks 2): keep R10-IQ3-0867 / remove R10-IQ-3792 (Day/Sun/Night→Moon); keep R10-IQ3-0883 / remove R10-IQ-3796 (Milk/Cow/Egg→Hen); keep R10-IQ3-0869 / remove R10-IQ-3800 (Thirst/Water/Hunger→Food); keep R10-IQ3-0899 / remove R10-IQ-3808 (Plant/Seed/Bird→Egg); keep R10-IQ3-0893 / remove R10-IQ-3816 (Umbrella/Rain/Sunglasses→Sun).
- **LCM (commutative), 2 removed**: keep HARD5-259 ("LCM of 10 and 8", 40, medium) over POL-068 ("LCM of 8 and 10", 40, hard); keep HARD5-283 ("LCM of 20 and 9", 180) over POL-080 ("LCM of 9 and 20", 180). Both keepers gained the `police` exam tag from the removed copy (only tag merges in this round).
- **No answer key was changed anywhere in this round.**

### Answer disagreements found and how resolved
- **19 english4 pairs, same stem, different (both valid) correct answers — english4 copy removed, kept version's key untouched.** 10× "Which English word means '<Nepali>'?" — two valid translations each: प्राप्त गर्नु acquire (E4 R10-ENG4-0030) vs achieve (R10-ENG-0024); विदेशी alien (0126) vs foreign (0659); वास्तविक actual (0036) vs genuine (0725); पीडा agony (0114) vs pain (1319); माफी apology (0174) vs pardon (1325); तीव्र acute (0042) vs rapid (1511); उठ्नु arise (0228) vs rise (1613); विश्वास belief (0624) vs trust (1853); प्रयास attempt (0330) vs endeavour (R10-ENG2-0437); बढाउनु boost (0840) vs increase (ENG2-0737). 9× idioms, same meaning worded differently: "Break a leg" (1141 vs ENG2-1416), "Out of the blue" (1154 vs 1452), "Rain cats and dogs" (1156 vs 1456), "The best of both worlds" (1158 vs 1466), "Through thick and thin" (1159 vs 1468), "Barking up the wrong tree" (1137 vs 1482), "By the skin of your teeth" (1143 vs 1494), "Cut to the chase" (1144 vs 1508), "Give someone the benefit of the doubt" (1149 vs 1522). In every case both keys are defensible; the duplication is the stem, so removal (not a key fix) is the right action.
- **18 maths clock pairs — maths8 key wrong (see above), maths8 copy removed.** No key change needed on the kept maths3 copies (all verified correct).
- **LCM pairs — same answer (40 / 180), no disagreement.**

### The full sweep and why its auto-plan was NOT applied
New reusable script `scripts/audit-duplicates.py` (exact + near Jaccard ≥0.8 + same-fact, guards adapted from `scripts/dedupe-check.py`, ~10 min for ~52k questions; `--apply` takes a plan JSON, merges exam tags onto keepers, writes repo-format JSON). Full run on the 50,870 snapshot: 28,433 classified pairs (near 2,960; same-options-reordered 25,468; same-fact 5; exact-text-only 3; 644 identical-stem/different-key excluded). Its auto-plan proposed **3,194 removals — NOT applied**: sampling showed the near families are dominated by a systematic false-positive pattern the guards don't catch:
- **NE-Jaccard ≥0.8 fires on template drills** whose Nepali translations differ by one word while the English payload differs: "How many days in January?" vs "…in May?" (both 31), "synonym of assemble" vs "…accumulate", "metres in 2 km" vs "millilitres in 2 litres", letter-sums NEPAL vs BRAVE (both 48). The option-pool generator reuses identical 4-option sets (and identical answers by coincidence) across different problems, so same-options + same-answer is not a duplicate signal here.
- **STOP-list artifact**: "antonym of select" vs "antonym of choose" scores content-Jaccard 1.0 because `choose`/`select` are both stopwords — the payload words are the very tokens being stripped.
- **`numbers_compatible` misses same-set reorderings** (the 143 odd-one-out copies) while passing different-number drills.
- The 3 "exact-text-only" pairs were false alarms vs the test's definition: "Choose the correct spelling." vs "…spelling:" and "synonym of generous." vs "synonym of 'generous':" — the test compares trim+lowercase only (punctuation kept), so these do NOT fail the test, and they are different template drills (content in the options: Beautiful vs Necessary; Liberal vs Charitable; Stingy vs Selfish). Script now matches the test's definition.
- Fixes applied to the script for re-use: near/same-options-reordered are only *planned* at a confident bar (jac_en ≥0.9 AND content-Jaccard ≥0.9); same-fact is report-only, never planned; exact-text uses the test's raw comparison. With the confident bar the 28,433 collapse to 52 survivors, of which 24 groups were genuine (the 157 removals above, via direct set-grouping) and the rest verified as distinct problems and kept: letter-sum different words (27 pairs), fraction-division reversals ("7/8 ÷ 1/1" = 7/8 vs "1/1 ÷ 7/8" = 8/7 — different answers; `loose_same_correct` treats them as same because {7,8} as a set ignores order — **bug to fix before the next sweep**), antonym select/choose, Nepali opposites खुसी→दुःखी vs सुख→दुःख. Checked and clean by direct grouping: addition/subtraction/division operand pairs (0), largest/smallest lists (0), arrange lists (0), percentage unordered pairs (0), HCF/LCM beyond the 2 above (0), sqrt/cube same-number (0).
- Two script runs were needed: the first crashed ~6 min in (`UnboundLocalError` on `jac_en`, eager-`dict.get` default) — fixed, plus precomputed guard fields (content tokens, tail tokens, number occurrences) for speed. Report from the completed run: `/tmp/audit-r10-report.json` (stale snapshot — files moved on; do not apply its plan).

### Still open (found in this round, not fixed)
- **Odd-one-out set {15,16,17,18} is ambiguous**: kept copy R10-IQ3-0702 keys 16 (only perfect square) but 17 is the only prime — a solver could defend either. Other kept sets are unambiguous (only prime / only multiple-of-9 etc.). Consider rewording or replacing this set.
- **`loose_same_correct` fraction flaw**: "7/8" vs "8/7" compare equal (token-set equality ignores order). Fix before the next dedupe sweep or it will keep flagging division-reversal pairs.
- **NE-Jaccard is unreliable for Devanagari template drills** (known from earlier rounds, re-confirmed here) — NE-only near flags need the payload check, not just the guard set.
- **Dedupe worker still active at end of this round** (last write 19:00 UTC was my own apply; worker writes stopped 18:45 UTC but it may resume) — re-count + re-run `test-questions.js` after it finishes; the bank was 50,713 here.
- Carried forward: no real-browser smoke test yet; human accuracy + Nepali spot-check still recommended before GitHub upload.

## Round 10 — Audit of new questions (replacement run) (2026-10-27, ~01:00–02:30 NPT)

Task: fresh complete audit of the r10 expansion questions (a previous audit worker ended without a final report). No GitHub upload, no bundle rebuild, no deletions — list broken questions for the parent instead. Parent integrates.

### Files audited / questions checked
- **34 `expansion-r10*.json` files, 30,187 questions** (bank total unchanged: **50,713 in 90 files**).
- `scripts/audit-answer-mismatch.py` run over the whole bank (it globs all files): **23 flags, 0 in r10 files**. Every flag recomputed by hand — **all 23 are false positives**: the script's "concluded value" regex picks up an intermediate `= N` in the explanation (e.g. "Father is now 10 x 5 = 50 … after 5 years he will be 55" flags 50 vs marked 55; "7 mod 4 = 3 … unit digit is 9" flags 3 vs marked 9). All 23 marked keys verified correct by hand. Flag ids (all pre-r10 files, no action taken): MATH2-007, MATH2-319, MATH2-323, IOE2-060, NTEL5-034, HARD5B-051, HARD5B-052, HARD5B-054, HARD5B-055, HARD5B-056, HARD5B-058, HARD5B-060, HARD5B-061, HARD5B-063, HARD5B-065, HARD5B-067, HARD5B-068, HARD5B-072, HARD6-096, HARD6-097, R6A-C245, R6B-490, R7A-T207.
- **Spot-check: 136 random r10 questions (4 per file, stratified), each hand-verified** — maths/IQ recomputed from the stem, calendar dates checked with Python `datetime`, factual claims checked against sources (see below). 134 correct as-is; 1 provably broken (listed for removal, not deleted); 1 garbled stem fixed. Calendar spot-checks all pass (25 Feb 2030 Mon, 3 Nov 2020 Tue, 3 Mar 2009 Tue, 26 May 2040 Sat, 25 May 2045 Thu, 11 Apr 1994 Mon, 7 Nov 2029 Wed; day-counts 41 and 57 correct). Current-affairs spot-checks verified: Nepali Congress 38 seats in the 2026 election (CNBC TV18 + Wikipedia), Sushila Karki first woman PM, Pope Leo XIV born Robert Prevost, Trump second term began 2025, Sixteenth Periodic Plan current.

### Wrong keys / explanations fixed
- **No answer key (answer index) was changed anywhere.** Every fix below keeps the same correct answer index; fixes correct the article number, the subject text, or the wording around it. (The 23 audit-script flags needed no key change either.)

### Constitution Articles — systematic generator-map error (the big find)
- The spot-check caught 2 wrong article questions (R10-NPL-0661 Art 247, R10-NPL-0665 Art 262); a full audit of **all 108 Constitution Articles questions** (54 "What does Article N provide?" + 54 "Which article deals with X?") against the official Constitution of Nepal 2015 text (FAO PDF, faolex.fao.org/docs/pdf/nep155698.pdf) found **35 of the 54 map entries wrong — 69 questions fixed** (EN + NE: question, options, explanations, Devanagari numerals).
- Root cause: `scripts/r10/g06_nepal_facts.py` `ARTICLES` map was shifted/wrong for whole blocks (commissions block 238–248 was off by a full part; judiciary, provinces, local level all shifted). **Generator map fixed in the same commit** (see below) so a regen cannot reintroduce these.
- Corrections applied (old → new): Art 1 "Federal Democratic Republic of Nepal" → "Constitution as the fundamental law" (that phrase is Art 4); Art 12 "Acquisition of citizenship" → "Citizenship with identity of descent and gender" (acquisition is Art 13); Art 49 "Directive principles" → Art 50 (Art 49 is "To be guiding principles"); Art 66 "Qualifications of the President" → Art 64 (66 is Functions/duties/powers of President); Art 70 "Vice-President" → Art 67 (70 is "different sex or community"); Art 74 "Federal Executive" → "Form of government" (Federal Executive is the Part 7 title); Art 88 "Qualifications of members" → Art 87 (88 is Oath); Art 101 "Vote of no confidence" → Art 100 (101 is Impeachment); Art 103 "Provisions relating to impeachment" → Art 101; Art 127 "Constitutional Bench" → Art 137; Art 128 "Chief Justice and Justices" → Art 129 (128 is Supreme Court); Art 137 "High Courts" → Art 139; Art 139 "District Courts" → Art 148; Art 176 "Provincial Executive" → Art 162; Art 178 "Provincial Assembly" → Art 175; Art 213 "Local Executive" → Art 214; Art 214 "Local Assembly" → Art 221; Art 222 "District Assembly" → Art 220; Art 223 "District Coordination Committee" → reverse question renumbered to Art 220, forward question re-subjected to "Composition of Municipal Assembly" (Art 223's true content); Art 232 "Inter-Province Council" → Art 234 "Inter-State Council" (official name); Art 238 "Election Commission" → Art 245; Art 239 "CIAA" → Art 238; Art 241 "Public Service Commission" → Art 242; Art 242 "National Human Rights Commission" → Art 248; Art 243 "National Natural Resources and Fiscal Commission" → Art 250; Art 244 "National Women Commission" → Art 252; Art 245 "National Dalit Commission" → Art 255; Art 246 "National Inclusion Commission" → Art 258; Art 247 "National Planning Commission" → "Assistance to the Election Commission" (NPC is not a constitutional body at all); Art 248 "Constitutional Council" → Art 284; Art 262 "Judicial Council" → Art 153 (262 is Madhesi Commission); Art 264 "Nepal Army" → Art 267; Art 267 "Nepal Police" → Art 268; Art 270 "National Security Council" → Art 266; Art 276 "Provisions relating to referendum" → "Pardons" (275 is the referendum article).
- Fixed question ids (69): R10-NPL-0482, 0483, 0504, 0505, 0576, 0577, 0592, 0593, 0594, 0595, 0596, 0597, 0608, 0609, 0614, 0615, 0616, 0617, 0620, 0621, 0622, 0623, 0624, 0625, 0626, 0627, 0629, 0630, 0631, 0632, 0633, 0634, 0635, 0636, 0637, 0638, 0639, 0640, 0641, 0642, 0643, 0644, 0645, 0648, 0649, 0650, 0651, 0652, 0653, 0654, 0655, 0656, 0657, 0658, 0659, 0660, 0661, 0662, 0663, 0664, 0665, 0666, 0667, 0668, 0669, 0672, 0673, 0678, 0679. (No reverse question existed for "Provincial Executive", so 35 forward + 34 reverse = 69.)
- After the renumber, R10-NPL-0669 ("Nepal Police") and R10-NPL-0671 ("Armed Police Force") both pointed at Art 268 with the identical stem "What does Article 268 … provide?" — `test-questions.js` caught the duplicate text. Fixed by rewording **R10-NPL-0671** to "Which of the following is provided for by Article 268 …?" (EN + NE, explanation now names all three bodies in Art 268). Both answers are genuinely in Art 268's heading, so both questions stay.
- Borderline, kept as-is: R10-NPL-0501 Art 10 → "Nepali citizen" (precise heading is "Not to deprive of citizenship"; the marked option is the only plausible one and Art 10 is about Nepali citizenship); R10-NPL-0503 Art 11 → "Nepali citizenship" (heading "To be citizens of Nepal"); R10-NPL-0507 Art 13 → "Termination of citizenship" (Art 13 covers acquisition, reacquisition *and* termination).

### Mountains — "highest in the world" was a Nepal-only ranking
- **13 rank questions fixed** (R10-NPL-0312, 0314, 0316, 0318, 0320, 0322, 0324, 0326, 0328, 0330, 0332, 0334, 0336): the generator ranked a Nepal-only list but labelled it "highest in the world" (EN + NE "विश्वको"). World ranks differ — K2 (2nd, 8611 m) and Nanga Parbat (9th, 8126 m) are missing from the list. All 13 reworded to "highest in Nepal" / "नेपालको" (question + explanation, EN + NE); the Nepal ranking itself is correct (Everest, Kangchenjunga, Lhotse, Makalu, Cho Oyu, Dhaulagiri, Manaslu, Annapurna I, Gyachung Kang, Annapurna II, Himalchuli, Nuptse, Machhapuchhre, Ama Dablam) and all 12 height questions re-verify correct. Generator template fixed too.
- Other nepal-facts subtopics spot-sampled clean: Provinces & Districts (Kusma/Parbat, Rautahat/Madhesh, Siddharthanagar/Rupandehi, Myaglung/Terhathum, Bhojpur/Koshi), Historical Events (Everest 1953, Rana 1846, NTV 1985, ODI status 2018, Anglo-Nepal War 1814), Firsts & Symbols, Lakes, National Parks, Festivals — all correct.

### Nepali fields fixed — 16 answer-leaking partial translations
- Full scan of all 30,187 r10 questions: **0 missing** `question_ne`/`options_ne`/`explanation_ne`; **0** `question_ne`/`explanation_ne` in English. The 9,752 `options_ne` flags from the scan are all legitimate: single letters/scrambled words (IQ), Roman numerals, English vocab/grammar/idiom options (the tested content), proper names, chemical formulas/symbols, and Nepali options identical to the EN field because the EN field itself is Nepali.
- **16 mixed-translation questions found and fixed — in all 16, only the correct option had been translated to Nepali, leaking the answer in Nepali mode:**
  - **12× `expansion-r10-english4.json` prepositions** (R10-ENG4-1224, 1225, 1236, 1237, 1252, 1253, 1258, 1259, 1282, 1283, 1312, 1313): the correct preposition was translated to a Nepali postposition in `options_ne` ("on"→"मा", "of"→"को", "to"→"लाई", "from"→"भन्दा", "with"→"सँग", "about"→"बारे"). Restored the English preposition in `options_ne` (options are the English words being tested). Also fixed the ungrammatical stems in EN + NE ("He depend ___ me" → "He depends ___ me", "He afraid" → "He is afraid", "She is depend/agree" → "She depends/agrees", "He grateful/different/worried" → "He is grateful/different/worried"). Keys verified: depend on, afraid of, grateful to, different from, agree with, worried about — all correct.
  - **4× `expansion-r10-iq5.json` syllogisms** (R10-IQ5-1194, 1200, 1206, 1212): only the correct conclusion was translated. Translated the other three `options_ne` each to proper Nepali (e.g. 1194: "No bird is an eagle" → "कुनै पनि चरा चील होइन", "All fish are birds" → "सबै माछाहरू चरा हुन्", "Some eagles are fish" → "केही चीलहरू माछा हुन्"). Syllogism keys re-verified correct.
- After fixes: 0 mixed-translation questions remain in r10.

### Other wording fixes
- **R10-WORLD-0754** (spot-check): garbled EN stem "What is the first Cricket World Cup was held in?" → "Where was the first Cricket World Cup held?"; EN explanation "was held in is England (1975)" → "The first Cricket World Cup was held in England (1975)." Answer unchanged.
- **English ordinal suffixes: 364 fields fixed** across 10 files (iq 52, iq2 20, iq3 21, iq4 112, iq5 30, iq6 15, maths2 103, maths3 6, nepal-facts 2, nepali2 3) — "2th"→"2nd", "3th"→"3rd", "22th"→"22nd", "23th"→"23rd", "21th"→"21st", "31th"→"31st", "33th"→"33rd" in EN question/explanation only (keys unaffected; e.g. "22th from the left" → V was already the right letter). Includes the spot-check find R10-IQ5-1094 ("3th" in the explanation). Generator templates still use `{n}th` in `scripts/r10/g02_iq.py`, `g03_maths2.py`, `g11_maths3.py`, `g12_iq2.py` — data fixed, generators not yet.

### Questions needing removal (listed, NOT deleted)
- **R10-ENG3-0058** — "Which word is opposite in meaning to agency?" Options: Department / Organisation / Bureau / Office. **All four are synonyms of "agency"; no valid antonym exists.** The marked answer "Office" is arbitrary. Provably broken — remove or rewrite (e.g. change the headword).
- Borderline, kept: **R10-ENG2-0085** — "antonym of anticipate": marked "Expect", but "Foresee" is also a valid synonym of anticipate. Left as-is (Expect is the standard Lok Sewa answer); consider replacing the "Foresee" distractor in a future pass.

### Generator fixes (root causes, so regens don't reintroduce the errors)
- `scripts/r10/g06_nepal_facts.py`: `ARTICLES` map corrected per the table above (35 entries; duplicate Art 50 entry removed; new entry (223, "Composition of Municipal Assembly", "नगर सभाको गठन") added; (75, "Council of Ministers") → (75, "Executive power") and (126, "Supreme Court") → (128, "Supreme Court") also corrected though not in the bank); mountain rank template "highest in the world" → "highest in Nepal" (EN + NE) with correct ordinal suffixes in the explanation. File parses (`ast.parse` OK). Backup of the pre-fix generator at `/tmp/r10-backup/g06_nepal_facts.py` (ephemeral).
- Fix script for the data: `/tmp/fix-r10.py` (ephemeral); change log `/tmp/r10-fixes-log.json` (ephemeral). Backups of the four touched data files at `/tmp/r10-backup/` (ephemeral).

### Counts / tests at finish (2026-10-27 ~02:30 NPT)
- Bank on disk: **50,713 questions in 90 files** (r10: 30,187 in 34 files) — unchanged by this audit (0 added, 0 removed; all fixes in place).
- `node scripts/test-questions.js` — **ALL QUESTION CHECKS PASSED ✔** (final run; one self-inflicted duplicate-text failure on R10-NPL-0671 found and fixed mid-run, see above).
- `scripts/audit-answer-mismatch.py` re-run after fixes: same 23 pre-r10 false positives, 0 r10 flags.
- Nepali-field scan re-run after fixes: 0 mixed-translation questions; 0 missing NE fields.
- Bundle NOT rebuilt; other suites NOT run (parent integrates).

### Still open (found in this round, not fixed)
- R10-ENG3-0058 removal decision (parent's call).
- R10-ENG2-0085 "Foresee" distractor (see above).
- Ordinal `{n}th` templates in `g02_iq.py`, `g03_maths2.py`, `g11_maths3.py`, `g12_iq2.py` still generate bad suffixes — data fixed, generators not.
- R10-NPL-0669 / R10-NPL-0671 both ask about Art 268 (different answers, different stems now) — acceptable, note for the record.
- Carried forward: no real-browser smoke test yet; human accuracy + Nepali spot-check still recommended before GitHub upload.
