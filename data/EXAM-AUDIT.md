# Exam Coverage Audit — Lok Sewa Prep Nepal

**Audit date:** 2026-10-25 (overnight run)
**Research source:** `~/workspace/research_notes/nepal-govt-exams-research-20261025-1743/report.md`
— secondary prep/education sites and syllabus reproductions (Edusanjal, Edusoft Academy,
CollegeNP, Loksewa sites). The official PSC site (psc.gov.np) was **not** directly read in that
run. Every figure below is "as stated in the report" and must be verified against the vacancy
notice / psc.gov.np before publishing.
**App state audited:** `data/exams.json` (12 entries), `data/questions/*.json`
(1,129 unique MCQs), `assets/js/app.js`, `index.html`, `exam-guides/` (empty directory).

## Headline counts

| Measure | Count |
|---|---|
| Distinct exams/posts named in the research report | **40 rows** (see table; "Nijamati / civil service" is an umbrella term, not a separate exam, and is excluded from the missing count) |
| Already covered in the app (dedicated entry or grouped entry) | **25** |
| Missing from the app (no entry at all) | **14** |
| Missing exams that get a draft entry in `data/exams-new.json` | **14** |
| Missing exams with NO MCQ prelim (prelim: null in draft) | **11** |
| Missing exams WITH a verified MCQ prelim in the draft | **3** (Foreign Service, TSC Lower Secondary, TSC Teaching Licence) |
| Exam entries currently in `data/exams.json` | 12 |

**"In app?" legend:** Yes = dedicated entry in `data/exams.json`. Yes (grouped) = covered only
under a grouped entry (e.g. all six Health Service posts share the single `health` entry; all
Police/APF posts share `police`). No = no entry at all.
**"Guide page?"** — guides are generated dynamically from `data/exams.json` by `renderGuide()`
in `assets/js/app.js`; `exam-guides/` is an empty directory with no static guide files. So every
exam in `exams.json` has a guide card, and no missing exam has one.
**"Mock exists?"** — `startMock()` in `assets/js/app.js` builds a timed mock from any entry's
`prelim` object, so every exam in `exams.json` has a mock. ⚠️ **Caveat:** if the tagged question
pool is smaller than the prelim question count, the mock silently falls back to the *entire*
question bank (`if(pool.length < p.questions) pool=QUESTIONS.slice()`). That affects the thin
banks — engineering (10 tagged), police (26), army (26), health (31), nrb-officer (45),
rbb (73) — whose "mocks" are mostly off-topic questions. See §3.
**Question counts** are tag assignments from the `exam` array in the question JSON files
(one question can carry several exam tags; 1,129 unique questions, 3,206 tag assignments).

## 1. Coverage table

| # | Exam / post (as named in report) | In app? | Guide page? | Questions tagged | Mock exists? | Prelim pattern (per report) |
|---|---|---|---|---|---|---|
| 1 | Kharidar (Level 4) | Yes | Yes | 851 | Yes | 50×2=100, 45 min, pass 45, −20% (GK 30 + BOST 20) |
| 2 | Nayab Subba / NaSu (Level 5) | Yes | Yes | 859 | Yes | 50×2=100, 45 min, pass 45, −20% (GK 30 + IQ 20) |
| 3 | Section Officer / Shakha Adhikrit (Gaz. 3rd) | Yes | Yes | 798 | Yes | 100×1=100, 90 min, pass 45, −20% (GA 50 + Aptitude 30 + English 20) |
| 4 | Deputy Secretary / Joint Secretary (Upa-Sachiv / Saha-Sachiv) | **No** | No | 0 | No | None stated in report — prelim null |
| 5 | Sub-Engineer (technical) | **No** | No | 0 | No | None stated in report — prelim null |
| 6 | JTA — Junior Technical Assistant | **No** | No | 0 | No | None stated in report — prelim null |
| 7 | Ranger | **No** | No | 0 | No | None stated in report — prelim null |
| 8 | Computer Operator | **No** | No | 0 | No | None stated in report — prelim null |
| 9 | Health Service — Staff Nurse | Yes (grouped: `health`) | Yes (grouped) | 31 (shared) | Yes (grouped, generic pattern) | No post-specific pattern in report |
| 10 | Health Service — Health Assistant | Yes (grouped: `health`) | Yes (grouped) | 31 (shared) | Yes (grouped, generic pattern) | No post-specific pattern in report |
| 11 | Health Service — Lab Technician | Yes (grouped: `health`) | Yes (grouped) | 31 (shared) | Yes (grouped, generic pattern) | No post-specific pattern in report |
| 12 | Health Service — Radiographer | Yes (grouped: `health`) | Yes (grouped) | 31 (shared) | Yes (grouped, generic pattern) | No post-specific pattern in report |
| 13 | Health Service — Medical Officer | Yes (grouped: `health`) | Yes (grouped) | 31 (shared) | Yes (grouped, generic pattern) | No post-specific pattern in report |
| 14 | Health Service — Consultant (9th level) | Yes (grouped: `health`) | Yes (grouped) | 31 (shared) | Yes (grouped, generic pattern) | No post-specific pattern in report |
| 15 | Engineering Service — Civil | Yes (grouped: `engineering`) | Yes (grouped) | 10 (shared) | Yes (grouped, generic pattern) | No branch-specific pattern in report |
| 16 | Engineering Service — Electrical | Yes (grouped: `engineering`) | Yes (grouped) | 10 (shared) | Yes (grouped, generic pattern) | No branch-specific pattern in report |
| 17 | Engineering Service — Mechanical | Yes (grouped: `engineering`) | Yes (grouped) | 10 (shared) | Yes (grouped, generic pattern) | No branch-specific pattern in report |
| 18 | Judicial Service / Nyaya Sewa | **No** | No | 0 | No | None stated in report — prelim null |
| 19 | Foreign Service / Pararastra Sewa | **No** | No | 0 | No | Same prelim as Section Officer: 100×1=100, 90 min, pass 45, −20% (report §2.3) |
| 20 | Other PSC service groups — Audit, Revenue, Administration, Parliament Service | **No** | No | 0 | No | None stated in report — prelim null (these are service-group streams of Kharidar/NaSu/SO, not standalone exams) |
| 21 | TSC — Primary Teacher (Pra Bi) | Yes | Yes | 159 | Yes | 50×2=100, 60 min, pass 50, −20% (Edu 40% + GK 30% + Const/Acts 10% + ICT 10% + IQ 10%) |
| 22 | TSC — Lower Secondary Teacher (Ni Ma Vi) | **No** | No | 0 | No | 50×2=100, 60 min, pass 50, −20% (same weightage as Primary, report §3.1) |
| 23 | TSC — Secondary Teacher (Ma Vi) | Yes | Yes | 153 | Yes | 50×2=100, 60 min, pass 50, −20% (GK 40% + Edu 24% + IQ 16% + ICT 10% + Const/Acts 10%) |
| 24 | TSC — Teaching Licence exam | **No** | No | 0 | No | 50×2=100, pass 50, 100% objective; **time limit NOT stated in report** (prelim drafted with timeMin null) |
| 25 | NRB Assistant Director (Officer 3rd) | Yes | Yes | 45 | Yes | Pre-qualifying MCQ, 100 marks (Q count / time / pass NOT stated in report — see §3) |
| 26 | NRB Assistant (2nd Class) | Yes | Yes | 175 | Yes | 50×2=100, 45 min, pass 40, −20% (Mgmt/Acct 30 + Econ/Banking 30 + Maths 14 + Computer 14 + GK 12) |
| 27 | RBB / NBL / ADBL Assistant (Level 4, unified) | Yes | Yes | 73 | Yes | **No prelim in report** — two subjective papers (100 each) + interview 30 only (see §3) |
| 28 | RBB Senior Assistant (Level 5) | **No** | No | 0 | No | No standalone prelim — 50 MCQs embedded in Paper I (see §2) — prelim null |
| 29 | Nepal Police — Constable (Jawan) | Yes (grouped: `police`) | Yes (grouped) | 26 (shared) | Yes (grouped, generic pattern) | No post-specific written pattern in report |
| 30 | Nepal Police — ASI | Yes (grouped: `police`) | Yes (grouped) | 26 (shared) | Yes (grouped, generic pattern) | No post-specific written pattern in report |
| 31 | Nepal Police — SI / Inspector | Yes (grouped: `police`) | Yes (grouped) | 26 (shared) | Yes (grouped, generic pattern) | No post-specific written pattern in report |
| 32 | APF — Inspector | Yes (grouped: `police`) | Yes (grouped) | 26 (shared) | Yes (grouped, generic pattern) | No post-specific written pattern in report |
| 33 | APF — ASI | Yes (grouped: `police`) | Yes (grouped) | 26 (shared) | Yes (grouped, generic pattern) | No post-specific written pattern in report |
| 34 | APF — Jawan | Yes (grouped: `police`) | Yes (grouped) | 26 (shared) | Yes (grouped, generic pattern) | No post-specific written pattern in report |
| 35 | Nepal Army — Officer Cadet (2nd Lt) | Yes | Yes | 26 | Yes | No written-pattern detail in report |
| 36 | Nepal Army — Sainya (soldier) | Yes (grouped: `army` note) | Yes (grouped) | 26 (shared) | Yes (grouped, generic pattern) | No written-pattern detail in report |
| 37 | Provincial PSCs (e.g. Bagmati, Lumbini) | **No** | No | 0 | No | None stated in report — prelim null |
| 38 | Nepal Electricity Authority (NEA) | **No** | No | 0 | No | None stated in report (PSC unified or own board; patterns "mirror PSC/banking") — prelim null |
| 39 | Nepal Telecom | **No** | No | 0 | No | None stated in report (same as NEA) — prelim null |
| 40 | Nijamati / civil service | n/a — umbrella term for the PSC system (§1.5), not a separate exam | — | — | — | — |

Notes on rows the report mentions only in passing: "Audit, Revenue, Administration,
Parliament Service, etc." (§1.1) are service-group streams, not standalone exams — one row (#20).
"Nijamati / civil service" is the PSC system itself, not an exam. The "etc." after the technical
posts (Sub-Engineer, JTA, Ranger, Computer Operator) is unspecified in the report and cannot be
audited. Competitor-site coverage named in report §5 (Crack Lokshewa covers Staff Nurse and
Computer Operator; Loksewa By GyanUdaan covers PSC/TSC/NRB/RBB/NBL/ADBL) adds no new exam
names beyond the rows above.

## 2. Missing exams — draft entries in `data/exams-new.json`

All 14 missing exams have a draft entry in `data/exams-new.json`, in the exact schema of
`data/exams.json` (same fields, same prelim object shape; `prelim: null` where no MCQ prelim
exists). Nothing was invented: every age / education / pattern figure comes from the report,
and anything unverified is flagged in the entry's `note` field.

| Draft id | Exam | Prelim in draft | Why |
|---|---|---|---|
| `deputy-secretary` | Deputy / Joint Secretary | null | No MCQ prelim pattern in report |
| `sub-engineer` | Sub-Engineer | null | No MCQ prelim pattern in report |
| `jta` | Junior Technical Assistant | null | No MCQ prelim pattern in report |
| `ranger` | Ranger | null | No MCQ prelim pattern in report |
| `computer-operator` | Computer Operator | null | No MCQ prelim pattern in report |
| `judicial-service` | Judicial Service (Nyaya Sewa) | null | No pattern in report |
| `foreign-service` | Foreign Service (Pararastra Sewa) | **100×1, 90 min, pass 45, −20%** | Shares Section Officer prelim (report §2.3); main papers differ (English + Foreign Policy & IR replace Paper IV) |
| `psc-service-groups` | Audit / Revenue / Admin / Parliament groups | null | Service-group streams, no separate pattern |
| `tsc-lower-secondary` | TSC Lower Secondary Teacher | **50×2, 60 min, pass 50, −20%** | Same pattern + weightage as Primary (report §3.1) |
| `tsc-licence` | TSC Teaching Licence exam | **50×2, pass 50** (timeMin null, negative null) | 100% objective per report §3.1, but time limit and negative marking are NOT stated — left null, must verify before any mock timer is shown |
| `rbb-senior-assistant` | RBB Senior Assistant (Level 5) | null | 50 MCQs are embedded in Paper I, not a standalone prelim — no mock |
| `provincial-psc` | Provincial PSCs | null | No province-specific pattern in report |
| `nea` | Nepal Electricity Authority | null | No NEA-specific pattern in report |
| `nepal-telecom` | Nepal Telecom | null | No Nepal Telecom-specific pattern in report |

**Missing exams with NO MCQ prelim (11):** Deputy/Joint Secretary, Sub-Engineer, JTA, Ranger,
Computer Operator, Judicial Service, Audit/Revenue/Administration/Parliament service groups,
RBB Senior Assistant, Provincial PSCs, NEA, Nepal Telecom. These are guide + theory/subjective
outline only — no mock. (The app's `startMock()` reads `e.prelim` directly, so merging a
`prelim: null` entry into `exams.json` as-is would break the mock flow for that exam; the
integrating agent must guard `startMock()`/guide rendering for null prelims, or keep these
entries guide-only until a pattern is verified.)

**Missing exams WITH a verified MCQ prelim (3):** Foreign Service, TSC Lower Secondary,
TSC Teaching Licence (time/negative unverified — see its note).

**Deliberately NOT duplicated in `exams-new.json`:** the six Health Service posts, the three
Engineering branches, the six Police/APF posts and Army Sainya — they are already covered by
the grouped `health`, `engineering`, `police` and `army` entries, and the report gives no
post- or branch-specific MCQ pattern that would justify a separate entry. Splitting them would
duplicate the grouped entry with `prelim: null` and no new information.

## 3. Conflicts and app-side verification gaps found

Conflicts carried over from the report (all flagged in the relevant draft `note` fields):

1. **Section Officer main-paper pass mark:** 40 vs 45 across sources (report §2.3). Already
   noted in the app's `section-officer` entry.
2. **Section Officer final-stage total:** 70 (Edusanjal) vs 60 (another guide); 80 for Foreign
   Affairs Service. Already noted in the app's `section-officer` entry; repeated in the
   `foreign-service` draft.
3. **TSC general-paper merit weightage:** whether general-paper marks count toward merit (50%
   per one Ma Vi source) or only the subjective paper counts (per CollegeNP). Noted in the
   app's `tsc-secondary` entry and the `tsc-lower-secondary` draft.
4. **Nepal Police ASI age/education:** sources differ (18–24 vs 21–30; +2 vs Bachelor's) by
   vacancy / technical vs general stream. The app's grouped `police` entry already says
   "streams vary — verify".
5. **Health Service age limits:** vary by post; the 35/40 rule does not apply uniformly.
   The app's `health` entry already says so.
6. **Deputy/Joint Secretary age:** the report states "up to 45 (women/PWD 40)" — i.e. the
   women's/PWD figure is *lower* than the general figure, the opposite of the usual extension
   pattern (18–35, women/PWD 40) used for every other exam. Almost certainly a source error;
   flagged in the `deputy-secretary` draft note — verify against the vacancy notice.
7. **Pre-2081 vs 2081/82 prelim format:** pre-2081 sources describe Kharidar/NaSu prelims as
   100×1 in 90 min; the revised 2081/82 syllabus uses 50×2 in 45 min. The app correctly uses
   the revised pattern; question sets must be labelled by syllabus year and the two formats
   must not be mixed.

App-side patterns in `data/exams.json` that are **NOT sourced in the research report**
(they read as placeholders / assumptions and must be verified before they are presented as
real patterns):

- `rbb` prelim (50×2, 45 min, pass 40): the report (§3.4) gives **no prelim at all** for
  RBB/NBL/ADBL Assistant — only two subjective papers + interview. The app's prelim is
  unverified.
- `nrb-officer` prelim (100×1, 90 min, pass 45): the report (§3.3) says only "pre-qualifying
  MCQ, 100 marks" — no question count, time, or pass mark. The app's values are unverified.
- `police`, `army`, `health`, `engineering` prelims (all 50×2, 45 min, pass 45, "per notice"):
  the report gives no written-pattern detail for any of these. They are generic placeholders.
- **Thin-bank mock fallback (§1 caveat):** `startMock()` falls back to the whole 1,129-question
  bank when the tagged pool is smaller than the prelim count. Engineering has only 10 tagged
  questions, police 26, army 26, health 31, nrb-officer 45, rbb 73 — so their "mocks" are
  currently 50–100 questions drawn mostly from other exams' topics. The mock exists
  mechanically, but it does not mirror the real paper for these exams.

## 4. Method

- Read the full research report (`report.md`) and listed every exam/post named in §1.1–§1.5,
  §2 and §3 (including sub-posts inside grouped table rows).
- Read `data/exams.json` (12 entries) and counted `exam` tags across all five question files
  with Python (`collections.Counter` over the `exam` arrays): kharidar 851, nasu 859,
  section-officer 798, nrb-assistant 175, nrb-officer 45, tsc-primary 159, tsc-secondary 153,
  rbb 73, police 26, army 26, health 31, engineering 10 (1,129 unique questions).
- Checked `renderGuide()` and `startMock()` in `assets/js/app.js` and the `exam-guides/`
  directory (empty) to determine guide/mock existence per exam.
- No files outside `data/EXAM-AUDIT.md` and `data/exams-new.json` were created or modified.
  `data/exams.json`, `index.html`, `assets/js/app.js` and all question JSON files were not
  touched (read-only).
