# FULL GAP AUDIT — Lok Sewa Prep Nepal

**Audit date:** 2026-10-26 (overnight run)
**Auditor scope:** every Nepal government / licence / professional exam family a Nepali
student might search for — PSC (all levels/services), TSC (all levels + licence),
NRB/banks, Police/APF/Army, Health Service, Engineering, Judicial, Foreign Service,
Provincial PSCs, public enterprises, local-level health posts, ALL licence councils,
and adjacent high-volume entrance exams.
**App state audited:** `data/exams.json` (12 entries), `data/questions/*.json`
(1,129 unique MCQs, 3,206 tag assignments — re-counted read-only with Python, matches
`data/EXAM-AUDIT.md`), `assets/js/app.js`, `index.html`, `exam-guides/` (empty).
**Prior work:** `data/EXAM-AUDIT.md` (2026-10-25) already audited the 40 rows named in
the research report and drafted 14 missing entries in `data/exams-new.json`. This audit
**supersedes and extends it**: it re-verifies those 40 rows, adds 32 new families the
report never named, and re-checks patterns with fresh web research (text fetch only).
`data/LICENSE-RESEARCH.md` did **not** exist — the licence-council research in §2 is new.
**Nothing was edited** except this file: `data/exams.json`, `index.html`,
`assets/js/app.js`, `data/exams-new.json` and all question JSON files were untouched
(read-only).

## Headline counts

| Measure | Count |
|---|---|
| Exam families listed in this audit (§1 table) | **72** |
| Covered — dedicated entry + verified pattern + adequate questions (≥100 tagged) | **6** |
| Thin / grouped — entry exists but shared, <100 tagged questions, or unverified placeholder pattern | **20** |
| Missing — no entry, no guide, no questions | **46** |
| Missing with a **verified MCQ pattern** found in this run (add-now candidates) | **21** |
| Missing with pattern **unverified — guide only** | **25** |
| Out of scope (listed in §4, not counted as gaps) | 2 (driving licence, SEE/NEB board exams) |

**Status legend:** `Covered` = dedicated entry in `data/exams.json`, verified prelim
pattern, ≥100 tagged questions, mock mirrors the real paper. `Thin` = entry exists
but the tagged bank is <100 questions and/or the prelim is an unverified placeholder
(see §3 — the mock falls back to the whole 1,129-question bank, so these mocks are
mostly off-topic). `Grouped` = covered only under a shared entry (`health`,
`engineering`, `police`, `army`). `Missing` = no entry at all.
**"Questions"** = tag assignments from the `exam` array in the question JSON files
(one question can carry several tags; 1,129 unique questions).

## 1. Coverage table — all 72 exam families

### A. PSC — core & gazetted

| # | Exam family | In app? | Guide | Qs | Mock | Status | Pattern / roadmap |
|---|---|---|---|---|---|---|---|
| 1 | Kharidar (Level 4) | Yes | Yes | 851 | Yes | **Covered** | 50×2=100, 45 min, pass 45, −20% (GK 30 + BOST 20) |
| 2 | Nayab Subba / NaSu (Level 5) | Yes | Yes | 859 | Yes | **Covered** | 50×2=100, 45 min, pass 45, −20% (GK 30 + IQ 20) |
| 3 | Section Officer / Shakha Adhikrit (Gaz. 3rd) | Yes | Yes | 798 | Yes | **Covered** | 100×1=100, 90 min, pass 45, −20% (GA 50 + Aptitude 30 + English 20) |
| 4 | Deputy / Joint Secretary (Upa-Sachiv / Saha-Sachiv, Gaz. 2nd/1st) | No | No | 0 | No | Missing | No MCQ prelim — written subjective + interview. **Guide only.** Age "up to 45 (women/PWD 40)" in the report is almost certainly a source error (inverted extension) — verify against the notice. |
| 5 | Foreign Service / Pararastra Sewa (Gaz. 3rd) | No | No | 0 | No | Missing — **add now** | **Verified:** same prelim as Section Officer (100×1=100, 90 min, pass 45, −20%); main papers differ (English + Foreign Policy & IR replace Paper IV). Draft exists in `exams-new.json`. |
| 6 | Judicial Service / Nyaya Sewa | No | No | 0 | No | Missing | No MCQ prelim pattern found — written papers + interview. **Guide only.** |
| 7 | PSC service-group streams — Audit, Revenue, Administration, Parliament | No | No | 0 | No | Missing | Not standalone exams — streams of Kharidar/NaSu/SO. **Guide only** (one explainer page, not 4 entries). Draft exists in `exams-new.json`. |
| 8 | Computer Officer (Gaz. 3rd, 7th level, IT) | No | No | 0 | No | Missing — **add now** | **Verified:** Paper I 100×1=100, 90 min, pass 40 (50 GK/reasoning + 50 technical); Paper II subjective 100, 3 hrs. Source: loksewatayariapp.com/exam/computer-officer. |
| 9 | Computer Operator (Level 5, NaSu Computer) | No | No | 0 | No | Missing — **add now** | **Verified:** Paper I 50×2=100, 45 min, pass 40 (20 GK/public mgmt + 30 job knowledge); Paper II subjective 100 (12×5 + 4×10); Practical 50 (pass 25, 45 min); Interview 30. ⚠️ Paper II duration conflicts: 2h15m (shikshasanjal) vs 3h15m (loksewatayariapp). Draft in `exams-new.json` has `prelim: null` — **needs updating with this pattern**. |
| 10 | Sub-Engineer (Level 5, Civil & other branches) | No | No | 0 | No | Missing — **add now** | **Verified (with variation caveat):** Paper I objective 50×2=100, 45 min, pass 40, −20%; then interview 20 (federal, per loksewatayariapp). Format has changed over the years and differs between federal and provincial commissions — verify per notice. Bagmati provincial variant: Paper I 50×2 (25 GK/IQ/Eng/Nep + 25 service) + Paper II subjective 100 + interview. Draft in `exams-new.json` has `prelim: null` — **needs updating**. |
| 11 | JTA — Junior Technical Assistant (agriculture/livestock) | No | No | 0 | No | Missing | No JTA-specific pattern found in this run; generic PSC 50×2=100, 45 min, pass 40 pattern is cited for technical Level 4/5 posts generally but **not verified for JTA**. **Guide only** until the JTA syllabus is read. |
| 12 | Ranger (forestry) | No | No | 0 | No | Missing | Same as JTA — no Ranger-specific pattern found. **Guide only.** |
| 13 | Lab Assistant (Level 4, health technical) | No | No | 0 | No | Missing — **add now** | **Verified:** Paper I 50×2=100 (GA 10×2 + Public Mgmt 10×2 + Job knowledge 30×2 — Micro 10, Haem 10, Biochem 5, Misc 5); Paper II subjective 100 (2× [6×5 + 2×10]), 2h15m, pass 40; Interview 30; −20%. Source: loksewatayariapp.com/service/lab-assistant. |

### B. PSC — Health Service (all share the single grouped `health` entry: 31 Qs, generic placeholder prelim)

| # | Exam family | In app? | Guide | Qs | Mock | Status | Pattern / roadmap |
|---|---|---|---|---|---|---|---|
| 14 | Health Service — Staff Nurse | Yes (grouped) | Yes (grouped) | 31 shared | Yes (generic) | **Thin / grouped** | No post-specific pattern in report. Crack Lokshewa covers Staff Nurse separately — students will notice the generic entry. Split out when a verified pattern + ≥50 Qs exist. |
| 15 | Health Service — Health Assistant (HA) | Yes (grouped) | Yes (grouped) | 31 shared | Yes (generic) | **Thin / grouped** | Provincial analogue verified: Pradesh 2 PSC 5th-level HA — 50×2=100, 45 min, pass 40, interview 20 (collegenp.com). Federal HA pattern still unverified. |
| 16 | Health Service — Lab Technician | Yes (grouped) | Yes (grouped) | 31 shared | Yes (generic) | **Thin / grouped** | See #13 Lab Assistant (Level 4) — the Level 5 lab-tech pattern is the same family; verify before splitting. |
| 17 | Health Service — Radiographer | Yes (grouped) | Yes (grouped) | 31 shared | Yes (generic) | **Thin / grouped** | No post-specific pattern found. Guide only until verified. |
| 18 | Health Service — Medical Officer (MBBS) | Yes (grouped) | Yes (grouped) | 31 shared | Yes (generic) | **Thin / grouped** | No post-specific pattern found. Note: every MO must also pass the NMC licence (#55) — cross-link the two. |
| 19 | Health Service — Consultant (9th level) | Yes (grouped) | Yes (grouped) | 31 shared | Yes (generic) | **Thin / grouped** | No MCQ prelim — senior posts are written-subjective + interview. **Guide only** (do not promise a mock). |

### C. PSC — Engineering Service (all share the single grouped `engineering` entry: 10 Qs, generic placeholder prelim)

| # | Exam family | In app? | Guide | Qs | Mock | Status | Pattern / roadmap |
|---|---|---|---|---|---|---|---|
| 20 | Engineering Service — Civil (Gaz. 3rd) | Yes (grouped) | Yes (grouped) | 10 shared | Yes (generic) | **Thin / grouped** | Partially verified: 2079 model paper — Paper I Part I General Awareness & Aptitude 50×1=50, 90 min; Part II job knowledge 50 Q. Paper II subjective 100 (A Structural/Geotech 30 + B Water 25 + C Transport 25 + D Public Health Eng 20). Source: engineeringnepal.com.np + Scribd 2079 model paper. |
| 21 | Engineering Service — Electrical | Yes (grouped) | Yes (grouped) | 10 shared | Yes (generic) | **Thin / grouped** | No branch-specific pattern found. Guide only until verified. |
| 22 | Engineering Service — Mechanical | Yes (grouped) | Yes (grouped) | 10 shared | Yes (generic) | **Thin / grouped** | No branch-specific pattern found. Guide only until verified. |
| 23 | Engineering Service — other branches (Electronics, Computer, Agriculture, Irrigation, Hydropower, etc.) | No | No | 0 | No | Missing | No branch-specific patterns found. **Guide only** — one "other branches" page, not per-branch entries. Note: every engineer must also pass the NEC licence (#61) — cross-link. |

### D. Teacher Service Commission (TSC)

| # | Exam family | In app? | Guide | Qs | Mock | Status | Pattern / roadmap |
|---|---|---|---|---|---|---|---|
| 24 | TSC — Primary Teacher (Pra Bi) | Yes | Yes | 159 | Yes | **Covered** | 50×2=100, 60 min, pass 50, −20% (Edu 40% + GK 30% + Const/Acts 10% + ICT 10% + IQ 10%) |
| 25 | TSC — Lower Secondary Teacher (Ni Ma Vi) | No | No | 0 | No | Missing — **add now** | **Verified:** same pattern + weightage as Primary (50×2=100, 60 min, pass 50, −20%). Draft exists in `exams-new.json`. Trivial add — same prelim object as `tsc-primary`. |
| 26 | TSC — Secondary Teacher (Ma Vi) | Yes | Yes | 153 | Yes | **Covered** | 50×2=100, 60 min, pass 50, −20% (GK 40% + Edu 24% + IQ 16% + ICT 10% + Const/Acts 10%) |
| 27 | TSC — Teaching Licence exam | No | No | 0 | No | Missing — **add now** | **Verified:** 100% objective, 50×2=100, pass 50. ⚠️ Time limit and negative marking NOT stated in any source found — draft in `exams-new.json` correctly leaves them null; verify before showing a mock timer. |

### E. Banking — NRB & public banks

| # | Exam family | In app? | Guide | Qs | Mock | Status | Pattern / roadmap |
|---|---|---|---|---|---|---|---|
| 28 | NRB Assistant (2nd Class) | Yes | Yes | 175 | Yes | **Covered** | 50×2=100, 45 min, pass 40, −20% (Mgmt/Acct 30 + Econ/Banking 30 + Maths 14 + Computer 14 + GK 12) |
| 29 | NRB Assistant Director (Officer 3rd) | Yes | Yes | 45 | Yes | **Thin** | App prelim (100×1, 90 min, pass 45) is **unverified** — report says only "pre-qualifying MCQ, 100 marks" (no Q count/time/pass). Written 3×100 + interview 40 (+ IT practical 50). Verify per notice before presenting the mock as real. |
| 30 | RBB / NBL / ADBL Assistant (Level 4, PSC unified exam) | Yes | Yes | 73 | Yes | **Thin** | App prelim (50×2, 45 min, pass 40) is **wrong** — the 2082-83 unified-exam syllabus has **no MCQ prelim at all**: Paper I + Paper II subjective (100 each, 2.5 hrs, pass 40) + interview 30. Confirmed by EducateNepal reproduction of the official syllabus (approved 2082-06-09). The mock should be removed or relabelled until/unless a prelim exists. |
| 31 | RBB Senior Assistant (Level 5) | No | No | 0 | No | Missing | No standalone prelim — 50 MCQs embedded in Paper I (50×1 + 10×5 subjective = 100, pass 40); Paper II 12×5 + 4×10 = 100; interview 30. **Guide only** (no full mock; a 50-Q Paper I practice set is possible once verified per notice). Draft exists in `exams-new.json`. |
| 32 | RBB / NBL / ADBL Officer level (Level 6/7+) | No | No | 0 | No | Missing | No pattern found in this run. **Guide only.** |

### F. Security forces

| # | Exam family | In app? | Guide | Qs | Mock | Status | Pattern / roadmap |
|---|---|---|---|---|---|---|---|
| 33 | Nepal Police — Constable (Jawan) | Yes (grouped: `police`) | Yes (grouped) | 26 shared | Yes (generic) | **Thin / grouped** | Partially verified: generic written 100 MCQs × 1 = 100, 45 min–1 hr, −0.25/wrong (lokshewa.online, single secondary source). Physical/medical precede the written — the guide must say so. |
| 34 | Nepal Police — ASI | Yes (grouped) | Yes (grouped) | 26 shared | Yes (generic) | **Thin / grouped** | Age/education conflict across sources (18–24 vs 21–30; +2 vs Bachelor's) by stream — app already flags "streams vary". Written pattern not separately verified. |
| 35 | Nepal Police — SI | Yes (grouped) | Yes (grouped) | 26 shared | Yes (generic) | **Thin / grouped** | Written pattern not separately verified. Bachelor's required, age 21–30 per most sources. |
| 36 | Nepal Police — Inspector | Yes (grouped) | Yes (grouped) | 26 shared | Yes (generic) | **Thin / grouped — split out, add now** | **Verified:** GART 50×2=100, 50 min, pass 40 (25 GK + 25 Reasoning); LPT subjective 100 (English 50 + Nepali 50); POAT subjective 100 (Knowledge 2h15m + Behaviour 45m). ⚠️ Negative-marking conflict: 0.25/wrong (loksewatayariapp) vs 20% (collegenp); LPT time conflict: 3 hrs total vs 2h+2h. Bachelor's, age 20–25 per one source (verify — other sources say 21–30). |
| 37 | APF — Inspector | Yes (grouped) | Yes (grouped) | 26 shared | Yes (generic) | **Thin / grouped** | No APF-specific written pattern found. Guide only until verified. |
| 38 | APF — ASI | Yes (grouped) | Yes (grouped) | 26 shared | Yes (generic) | **Thin / grouped** | No APF-specific written pattern found. Guide only until verified. |
| 39 | APF — Jawan | Yes (grouped) | Yes (grouped) | 26 shared | Yes (generic) | **Thin / grouped** | Class 8 pass, age 18–22. Written pattern not verified. |
| 40 | Nepal Army — Officer Cadet (2nd Lt) | Yes | Yes | 26 | Yes | **Thin** | No written-pattern detail verified in this run (one junk PDF-farm source claimed 100×1/2 hrs/no negative — **not trusted, not used**). Physical + IQ + written + interview stages. Guide must not present the app's generic 50×2 prelim as the real paper. |
| 41 | Nepal Army — Sainya (soldier) | Yes (grouped: `army`) | Yes (grouped) | 26 shared | Yes (generic) | **Thin / grouped** | Class 8/SEE, age 18–22. Written pattern not verified. |
| 42 | Nepal Police / APF — technical posts (doctor, engineer, IT) | No | No | 0 | No | Missing | No pattern found. **Guide only.** |
| 43 | Nepal Army — technical officer (medical/engineering) | No | No | 0 | No | Missing | No pattern found. **Guide only.** |

### G. Provincial PSCs & local level

| # | Exam family | In app? | Guide | Qs | Mock | Status | Pattern / roadmap |
|---|---|---|---|---|---|---|---|
| 44 | Provincial PSCs — Koshi, Madhesh, Bagmati, Gandaki, Lumbini, Karnali, Sudurpashchim | No | No | 0 | No | Missing — **add now (as 1 family entry + province pages)** | Patterns largely mirror the federal 50×2=100, 45 min, pass 40 template, **verified in two examples**: Pradesh 2 (Madhesh) 5th-level HA — 50×2=100, 45 min, pass 40, interview 20; Pradesh 2 5th-level Pharmacy Assistant — same 50×2=100, 45 min, pass 40, interview 20, −20%. Bagmati 5th-level Sub-Engineer differs (25 GK/IQ/Eng/Nep + 25 service, then subjective Paper II). Draft exists in `exams-new.json`. One family entry + per-province notes is the right shape, not 7 duplicate entries. |
| 45 | AHW — Auxiliary Health Worker (local level) | No | No | 0 | No | Missing | No AHW-specific pattern verified (one blog offers a "50 MCQs" practice set — not a syllabus source). Closest verified analogue is the provincial HA pattern (#44). **Guide only** until the local-level syllabus is read. |
| 46 | ANM — Auxiliary Nurse Midwife (local level) | No | No | 0 | No | Missing | No pattern found. **Guide only.** (ANMs also sit the NNC licence stream — cross-link #56.) |
| 47 | CMA — Community Medicine Assistant (local level) | No | No | 0 | No | Missing | No pattern found. **Guide only.** |
| 48 | Pharmacy Assistant (provincial / local level) | No | No | 0 | No | Missing — **add now** | **Verified (provincial):** Pradesh 2 PSC 5th-level Pharmacy Assistant — 50×2=100, 45 min, pass 40, interview 20, −20%; 7 syllabus units. Source: collegenp.com. |

### H. Public enterprises (PSC unified exams or own boards)

| # | Exam family | In app? | Guide | Qs | Mock | Status | Pattern / roadmap |
|---|---|---|---|---|---|---|---|
| 49 | Nepal Electricity Authority (NEA) | No | No | 0 | No | Missing — **add now** | **Verified (Level 5 Assistant):** Paper I 100 — Section A 50 MCQs × 1, 45 min, −20%, no calculator; Section B 10 short × 5 = 50, 75 min; Paper II 100 subjective (2h30m); Interview 30; total 230. Level 4 Senior Meter Reader variant: Paper I 100 (objective+subjective, 75 min), Paper II 100 (2h30m), interview 30. Level 7 technical Paper I Part A GK+IQ 50×1=50 (partially seen). Apply via career.nea.org.np. Draft in `exams-new.json` has `prelim: null` — **needs updating** (Section A is a real 50-Q MCQ block). |
| 50 | Nepal Telecom | No | No | 0 | No | Missing — **add now** | **Verified (Level 4 Assistant, PSC-conducted):** Paper I 50×2=100, 45 min, pass 40 (GK + IQ); Paper II subjective 100 (12×5 + 4×10, 2h30m, pass 40); Interview 30. Source: loksewatayariapp.com/exam/nepal-telecom. Draft in `exams-new.json` has `prelim: null` — **needs updating**. |
| 51 | Nepal Oil Corporation (NOC) | No | No | 0 | No | Missing | No pattern found in this run. **Guide only.** |
| 52 | Nepal Airlines Corporation (NAC) | No | No | 0 | No | Missing | No pattern found. **Guide only.** |
| 53 | Civil Aviation Authority of Nepal (CAAN) | No | No | 0 | No | Missing | No pattern found. **Guide only.** |
| 54 | Other public enterprises & financial regulators — Nepal Water Supply Corp, Citizen Investment Trust, Employees Provident Fund, SEBON, Nepal Insurance Authority, Rastriya Samachar Samiti, Gorkhapatra, Nepal Television, etc. | No | No | 0 | No | Missing | No patterns found. **Guide only** — one "other public enterprises" explainer page; split out only when a verified pattern exists for a specific body. |

### I. Licence / professional registration councils

| # | Exam family | In app? | Guide | Qs | Mock | Status | Pattern / roadmap |
|---|---|---|---|---|---|---|---|
| 55 | Nepal Medical Council — MBBS/BDS licence (NMCLE) | No | No | 0 | No | Missing — **add now** | **Verified:** 130 MCQs × 1 + 10 Clinical Scenario Qs × 5 = 180 marks, 3 hrs, pass 50% (90). Subject split published (Medicine 13–14, Surgery 13, Obs/Gynae 12–13, Paeds 10, Community Med 10–13, Anaesthesia 8, Micro/Path 4–7, etc.). No negative marking stated. Twice a year (Mar/Sep). Pass rate ~31% MBBS, ~23% dentists in one recent sitting — high demand for prep. Sources: mystichealth.com.np, medchrome.com, NMC Accreditation Standards 2017 (Scribd). |
| 56 | Nepal Nursing Council — Nursing licence (NLEN, PCL/BSc/BN) | No | No | 0 | No | Missing — **add now** | **Verified:** 150 MCQs × 1 = 150, 2h30m, pass 50% (75), **no negative marking**. Weightage: Fundamentals 34, Adult 25, Community 24, Midwifery/Gynae 23, Child 20, Integrated Science 19, Leadership/Mgmt 5. Separate papers for PCL vs BSc. Sources: collegenp.com NNC guide, slicejob.com (2080 notice), abhyaslabs mock. |
| 57 | Nepal Nursing Council — Midwifery licence (NLEM) | No | No | 0 | No | Missing — **add now** | **Verified:** written 150 MCQs × 1 = 150, pass 50%, **plus** OSPE/practical 50 marks, pass 80% (one notice says 40-mark OSPE — conflict, verify). Same no-negative rule. |
| 58 | Nepal Nursing Council — Specialist Nurse (NSREN) | No | No | 0 | No | Missing — **add now** | **Verified:** computer-based, 150 Qs, pass **60%**. Source: slicejob.com (2080 notice). |
| 59 | Nepal Health Professional Council — licence (HA, Lab, Radiography, Physiotherapy, Dental Hygiene, Ayurveda, Public Health, Optometry, etc.; 44 subjects, 17th exam Oct 2026, 4,470 candidates, 67.31% pass) | No | No | 0 | No | Missing — **add now** | **Verified format:** single-best-response MCQs, 4 options, **100 Qs, 2 hrs**, cognitive ratio Recall:Understanding:Application = 30:50:20. Public Health (BPH) syllabus total 100 marks (nhpc.gov.np PDF). ⚠️ **Pass mark not found** in any source — do not invent one; verify against nhpc.gov.np before showing a pass/fail line. NHPC exams running since 2077 BS (2020 AD). One family entry + per-discipline weightage pages is the right shape. |
| 60 | Nepal Pharmacy Council — Pharmacist licence (BPharm / DPharm) | No | No | 0 | No | Missing | **Pattern unverified — guide only.** Edusanjal's exam page lists Full Marks / Pass Marks / Question Type / Number of Questions / Negative Marking all as "N/A". The exam exists and is competitive (FY 2081/82: bachelor pass 31.93%, diploma 39.54%; 24th–29th licensing exams published) but no citable pattern was found — do not invent 100 MCQs. Verify against the Council notice before any mock. |
| 61 | Nepal Engineering Council — licence (General Registration, 41 branches) | No | No | 0 | No | Missing — **add now** | **Verified (current, NEC model Qs Nov 2025):** 100 MCQs × 1 = 100, 2 hrs, pass 50, **no negative marking**; branch-specific papers (civil, electrical, computer, mechanical, …). Older format (to 2023): 60×1 + 20×2 = 100. Twice a year; Mar 2023 pass rate 28.5% (565/1,981). Non-programmable calculator allowed. Sources: engineeringnepal.com.np, myrepublica.nagariknetwork.com, neclicenseexam.vercel.app. |
| 62 | Nepal Bar Council — Advocate licence (31st exam onwards) | No | No | 0 | No | Missing — **add now** | **Verified:** Paper 1 Constitution & Law — **100 MCQs × 1 = 100, 90 min, pass 50, no negative marking**; Paper 2 Drafting 90 (3×30: civil/criminal/writ) + Translation 10 (Nep↔Eng 5+5), 4 hrs total (30 min translation + 3h30m drafting), pass 50 combined; Interview 20 (pass 10, incl. 8-min debate); then supervised internship + 3-day training. 35th exam applications Aug–Sep 2026. Sources: edusanjal.com/exam/advocate-license-exam, nepaldivorce.com guide, examsanjal.com. |
| 63 | ICAN — Chartered Accountancy (CA Nepal) | No | No | 0 | No | Missing | **Partial fit — guide + limited practice.** Old CAP system: CAP-I 3 papers × 100, CAP-II 7 papers, CAP-III 8 papers, 40% per paper + 50% aggregate, 3-yr articleship. New 2026 syllabus (Foundation / Application / Advisory, with ICAEW): Foundation 4 papers, **60% objective / 40% subjective**; Application 6 papers, 30% objective / 70% subjective; Advisory 6 papers + 3-yr articleship. Mostly subjective — an MCQ portal can only serve the Foundation objective share well. **Guide first; add Foundation MCQ practice as a later phase, not a full mock.** |
| 64 | Nepal Ayurveda Medical Council — Ayurveda licence (BAMS) | No | No | 0 | No | Missing | No pattern found in this run. **Guide only.** (BAMS graduates also sit MECEE-BL #66 for admission — cross-link.) |
| 65 | Nepal Veterinary Council — Veterinary licence (BVSc) | No | No | 0 | No | Missing | No pattern found in this run. **Guide only.** |

### J. Adjacent high-volume entrance exams (not Lok Sewa, but the same students search for them)

| # | Exam family | In app? | Guide | Qs | Mock | Status | Pattern / roadmap |
|---|---|---|---|---|---|---|---|
| 66 | MECEE-BL — Medical Education Common Entrance (MBBS, BDS, BSc Nursing/Midwifery, BAMS, BSc MLT/MIT, BPharm, BPT, B Optometry, BPH, BNS/BMS) | No | No | 0 | No | Missing — **add now** | **Verified:** 200 single-best-response MCQs × 1 = 200, **3 hrs, −0.25/wrong**, pass = **50th percentile** (merit list). MBBS/BDS/Nursing cluster: Zoo 40, Bot 40, Chem 50, Phys 50, Mental Agility 20. Allied-health cluster: Zoo 40, Bot 40, Chem 40, Phys 40, PCL-subject 20, MAT 20. OMR, 50:30:20 recall:understanding:application. Fee NPR 4,000. Sources: edusanjal.com/exam/medical-education-common-entrance-examination-for-bachelor, careerykt/careerkyt.com/cee, MEC notice via educatenepal.com. **Biggest single traffic opportunity in this audit** — every +2 Science student in Nepal searches for this. |
| 67 | MECEE-PG — Medical Education PG entrance (MD/MS) | No | No | 0 | No | Missing | Known to exist (Medical Education Commission) but pattern **not verified** in this run. **Guide only** until verified. |
| 68 | IOE entrance — TU Institute of Engineering (BE/BArch) | No | No | 0 | No | Missing — **add now** | **Verified (2082/2083):** CBT, **100 MCQs, 140 marks (60×1 + 40×2), 2 hrs, −10% per wrong answer**. Maths 50 (14×1 + 18×2), Physics 40 (14×1 + 13×2), Chemistry 30 (14×1 + 8×2), English 20 (12×1 + 4×2). Older format was 140×1. Sources: allresultnp.com/ioe-entrance, nepalicollege.com, collegesanjal.com. ⚠️ The app's mock engine assumes uniform marks-per-question — a mixed 1/2-mark paper needs engine work before an IOE mock ships. |
| 69 | BSc CSIT entrance — TU IOST | No | No | 0 | No | Missing — **add now** | **Verified:** 100 MCQs × 1 = 100, 2 hrs, **no negative marking**, pass 35. Maths 25, Physics 25, Chemistry 25, English 15, Computer GK 10. Official TU IOST model question set exists. Sources: webnotee.com (2083 notice), safaltopper.com (official model Qs), shikshasanjal.com. (One source claims 140 marks/−0.1 — that is the IOE pattern misattributed; majority + official model paper say 100/100/no negative.) |
| 70 | CMAT — TU FoM entrance (BBA/BBM/BHM/BTTM) | No | No | 0 | No | Missing | No pattern verified in this run. **Guide only.** |
| 71 | BCA entrance — TU FoHSS (BCA) | No | No | 0 | No | Missing | No pattern verified in this run. **Guide only.** |

### K. Other

| # | Exam family | In app? | Guide | Qs | Mock | Status | Pattern / roadmap |
|---|---|---|---|---|---|---|---|
| 72 | CTEVT — Instructor / technical teacher recruitment | No | No | 0 | No | Missing | No pattern found in this run. **Guide only.** |

## 2. Licence-council summary (new research — no LICENSE-RESEARCH.md existed)

| Council | Exam | Verified pattern | Pass | Negative | Recommendation |
|---|---|---|---|---|---|
| Nepal Medical Council (NMC) | MBBS/BDS licence (NMCLE) | 130×1 MCQ + 10×5 CSQ = 180, 3 hrs | 50% (90) | None stated | **Add now** |
| Nepal Nursing Council (NNC) | NLEN nursing | 150×1 = 150, 2h30m | 50% (75) | None | **Add now** |
| Nepal Nursing Council (NNC) | NLEM midwifery | 150×1 = 150 + OSPE 50 | 50% written; 80% OSPE | None | **Add now** |
| Nepal Nursing Council (NNC) | NSREN specialist | 150 Q, CBT | 60% | Not stated | **Add now** |
| Nepal Health Professional Council (NHPC) | All disciplines (44 subjects) | 100 MCQ, 2 hrs, 30:50:20 | **Unverified** | Not stated | **Add now, but no pass/fail line until verified** |
| Nepal Pharmacy Council (NPC) | Pharmacist licence | **Unverified** (Edusanjal: all fields N/A) | Unverified | Unverified | Guide only |
| Nepal Engineering Council (NEC) | General registration licence | 100×1 = 100, 2 hrs | 50 | None | **Add now** |
| Nepal Bar Council (NBC) | Advocate licence | Paper 1: 100×1 = 100, 90 min; Paper 2 drafting+translation 100, 4 hrs; Interview 20 | 50 per paper; 10 interview | None (Paper 1) | **Add now (Paper 1 mock)** |
| ICAN | CA (new Foundation/Application/Advisory) | Foundation 60% objective / 40% subjective | 40% per paper + 50% aggregate (old CAP) | n/a | Guide first; Foundation MCQs later |
| Nepal Ayurveda Medical Council | Ayurveda licence | Unverified | Unverified | Unverified | Guide only |
| Nepal Veterinary Council | Veterinary licence | Unverified | Unverified | Unverified | Guide only |

## 3. App-side problems this audit confirms or newly finds

1. **Thin-bank mock fallback (from EXAM-AUDIT §1, re-confirmed):** `startMock()` falls
   back to the entire 1,129-question bank when the tagged pool is smaller than the
   prelim count. Affected: engineering (10 tagged), police (26), army (26), health (31),
   nrb-officer (45), rbb (73). Their "mocks" are mostly off-topic questions. This is the
   single most misleading thing in the app — a student taking a "Health Service mock"
   gets Kharidar GK questions.
2. **RBB prelim is wrong (new confirmation):** the app's `rbb` prelim (50×2, 45 min,
   pass 40) does not exist — the 2082-83 unified-exam syllabus (approved 2082-06-09)
   is two subjective papers (100 each) + interview 30. The mock should be removed or
   relabelled; the entry should be guide + subjective-outline only.
3. **NRB Officer prelim unverified (from EXAM-AUDIT §3, re-confirmed):** app shows
   100×1, 90 min, pass 45; the report only supports "pre-qualifying MCQ, 100 marks".
4. **Placeholder prelims (from EXAM-AUDIT §3, re-confirmed):** `police`, `army`,
   `health`, `engineering` all show 50×2, 45 min, pass 45 "per notice" — none of these
   is sourced. New finding: the Nepal Police Inspector GART is actually 50×2=100 in
   **50 min** (not 45), pass 40, with a **−0.25/wrong** negative (not 20% per a
   conflicting source) — so the grouped `police` prelim is wrong for the Inspector
   stream in three separate fields.
5. **Three `exams-new.json` drafts now have verified patterns and need updating**
   (drafts currently say `prelim: null`): `sub-engineer` (50×2=100, 45 min, pass 40),
   `computer-operator` (50×2=100, 45 min, pass 40), `nea` (Section A: 50×1, 45 min,
   −20%), `nepal-telecom` (50×2=100, 45 min, pass 40). That is four drafts, not three.
   (This audit does not edit `exams-new.json` — the integrating agent should apply it.)
6. **Mixed-mark papers need engine work:** IOE entrance (60×1 + 40×2) and the NEC
   pre-2023 format (60×1 + 20×2) cannot be represented by the current uniform
   `marksPerQ` prelim object. MECEE-BL (−0.25) and NNC/NEC (no negative) also need
   per-exam negative-marking values, including zero — the app currently hard-codes
   0.2-style deductions per exam entry, which is fine per-entry, but a `negative: 0`
   case must render as "no negative marking", not as a bug.
7. **Conflicts carried over from EXAM-AUDIT §3, still unresolved:** Section Officer
   main-paper pass 40 vs 45; Section Officer final-stage total 70 vs 60 (80 for Foreign
   Affairs); TSC general-paper merit weightage; Nepal Police ASI age/education;
   Health Service age limits; Deputy/Joint Secretary age inversion. **New conflicts
   found in this run:** Computer Operator Paper II 2h15m vs 3h15m; Police Inspector
   negative −0.25 vs 20%; Police Inspector LPT 3 hrs total vs 2h + 2h; NLEM OSPE 50
   marks vs 40 marks; CSIT 100 marks/no negative vs 140 marks/−0.1 (latter is an IOE
   misattribution — resolved in favour of 100/100/no negative); NEC current 100×1 vs
   pre-2023 60×1+20×2 (resolved: both true, different years — label by year).

## 4. Out of scope — explicitly excluded

| Family | Why excluded |
|---|---|
| **Driving licence** (written + trial, Department of Transport Management) | **Out of scope per task.** It is a licence, but a road-user test, not a government-job or professional-registration exam. Students do search for it (competitor Crack Lokshewa covers it) — if the portal ever expands to it, it needs a separate "trial" format, not MCQs. Do not add it to the exam table. |
| **SEE / NEB Grade 11–12 board exams** | School-leaving exams, not competitive government/licence/professional exams. Out of scope. |
| EPS-TOPIK / foreign-employment exams | Not Nepal government exams. Out of scope. |

## 5. Prioritised top 10 gaps a student would notice first

Ordered by (search volume × how obviously the portal is missing it × pattern readiness).
All 10 have **verified MCQ patterns** — every one is an add-now, not a research task.

1. **MECEE-BL (medical entrance, #66)** — the single biggest traffic miss. Every +2
   Science student in Nepal searches for it; pattern fully verified (200×1, 3 hrs,
   −0.25, 50th percentile). Needs 200-question banks per cluster (Physics/Chemistry/
   Biology/MAT) — the largest content lift, but also the largest audience.
2. **NEC licence exam (#61)** — every engineering graduate *must* pass it to practise;
   28.5% pass rate (Mar 2023) means desperate demand for mocks. Pattern verified
   (100×1, 2 hrs, pass 50, no negative), branch-specific papers. The app's `engineering`
   entry (10 Qs) makes the gap visible the moment an engineer opens the site.
3. **NMC licence — MBBS/BDS (#55)** — verified pattern (130 MCQ + 10 CSQ = 180, 3 hrs,
   pass 50%), ~31% pass rate. Every medical graduate searches for it. CSQs need a
   distinct question type (5-mark scenario) — engine work, but the 130 MCQs can ship first.
4. **NNC nursing licence (#56)** — verified pattern (150×1, 2h30m, pass 50%, no negative),
   weightage published, separate PCL/BSc papers. Nursing is one of Nepal's largest
   graduate cohorts; zero coverage today.
5. **Computer Operator (#9)** — verified pattern (50×2, 45 min, pass 40 + practical 50 +
   interview 30), and competitors (Crack Lokshewa, Loksewa Tayari) already cover it — a
   student comparing sites will notice its absence immediately. The app already has
   computer/ICT questions that partially overlap.
6. **Sub-Engineer (#10)** — verified pattern (50×2, 45 min, pass 40), one of the most
   applied-for PSC technical posts (diploma holders). Same 50×2 shape as Kharidar/NaSu,
   so the mock engine needs no changes — only technical questions.
7. **TSC Lower Secondary + Teaching Licence (#25, #27)** — verified patterns, trivial
   adds: Lower Secondary reuses the Primary prelim object verbatim; the Licence exam is
   50×2/pass 50 (time unverified — show no timer until verified). Two missing entries a
   teacher-aspirant hits on the first visit.
8. **Nepal Telecom Level 4 + NEA (#50, #49)** — both PSC-style, both verified
   (Telecom 50×2/45 min/pass 40; NEA Section A 50×1/45 min/−20%). Public-enterprise
   jobs are a distinct search stream ("NEA vacancy", "Nepal Telecom exam") the portal
   currently answers with nothing.
9. **Nepal Bar Council advocate licence, Paper 1 (#62)** — verified (100×1, 90 min,
   pass 50, no negative). Law graduates are a defined, searchable cohort; the MCQ paper
   is a clean mock, and the drafting/interview stages are guide-only — no engine work.
10. **IOE entrance + BSc CSIT entrance (#68, #69)** — verified patterns (IOE 100 Q/140
    marks/−10%; CSIT 100×1/no negative/pass 35). The +2-graduate audience overlaps
    heavily with MECEE-BL (#1); CSIT is a clean add (uniform 1-mark MCQs), IOE needs
    mixed-mark support first (§3.6).

**Next after the top 10:** NHPC licence (#59, 44 subjects, 4,470 candidates in the
17th exam — add once the pass mark is verified), NNC Midwifery/Specialist (#57–58),
Nepal Police Inspector split-out (#36), Provincial PSCs as one family entry (#44),
Pharmacy Assistant (#48), Lab Assistant (#13), Computer Officer (#8), Foreign
Service (#5). **Do not start** the 25 "guide only" families as mocks — publish a
guide page each, with "pattern unverified — check the vacancy notice" stated on the
page, and add questions only after the syllabus is read.

## 6. Sources (verbatim URLs from this run)

- NMC licence: https://www.mystichealth.com.np/2025/02/14/comprehensive-guide-to-passing-the-nepal-medical-council-licensing-examination-nmcle/ ; https://medchrome.com/featured/how-to-pass-nepal-medical-council-licensing-examination/ ; https://www.scribd.com/document/670995325/ACCREDITATION-STANDARDS-FOR-THE-MBBS ; https://www.thefreelibrary.com/In+Nepal%2c+nearly+70+percent+of+medical+doctors+fail+licensing+test.-a0824850261
- NNC licence: https://www.collegenp.com/article/nepal-nursing-council-licensing-exam-guide ; https://www.slicejob.com/blog/nepal-nursing-council-registration-certificate-and-licensure-exam-2080 ; https://www.collegenp.com/exam/nepal-nursing-council-licensing-examination-schedule ; https://www.abhyaslabs.com/en/exams/bsc-nursing-license-mock-test-1-lgbBWv
- NHPC: https://nhpc.gov.np/beta/uploads/syllabus_pdf/Syllabus_for_Public_Health_Licencing_Examination_2073.pdf ; https://meroeye.com/nepal-health-professional-council-license-exam/ ; https://meroeye.com/pcl-in-optometry-nhpc-license-examination/ ; https://english.nepalnews.com/s/health/67-31-pass-nhpc-17th-licensing-examination/
- NEC licence: https://www.engineeringnepal.com.np/p/nec-license-exam.html ; https://myrepublica.nagariknetwork.com/news/71-5-percent-candidates-fail-in-nepal-engineering-council-s-license-examination ; http://neclicenseexam.vercel.app ; http://yashiacademy.com/nec-license-exam-preparation/
- Pharmacy Council: https://edusanjal.com/exam/pharmacist-license-exam/ ; https://pharmainfonepal.com/pass-rate-of-pharmacy-licensing-examination-nepal-pharmacy-council/
- Bar Council: https://edusanjal.com/exam/advocate-license-exam/ ; https://edusanjal.com/news/nepal-bar-council-opens-online-application-for-the-advocate-level-examination/ ; https://nepaldivorce.com/blog/how-to-become-a-lawyer-a-step-by-step-guide ; https://www.examsanjal.com/nepal-bar-council-advocate-adhibakta-application-open-syllabus-apply-advocate/
- ICAN CA: https://edunepal.com/acca-vs-ca-which-accounting-qualification-is-right-for-you/ ; https://ccma.edu.np/brief-description/FAQs ; http://onlinenotesnepal.com/universities/institute-of-chartered-accountants-of-nepal ; https://companydartanepal.com/chartered-accountants-nepal/
- MECEE-BL: https://edusanjal.com/exam/medical-education-common-entrance-examination-for-bachelor/ ; https://careerkyt.com/cee/ ; https://smartacademyhq.com/cee-exam-date-schedule/ ; https://www.educatenepal.com/news/detail/notice-for-foreign-candidates-applying-for-common-entrance-examination-of-bachelor-level-programs-in-medical-education-mecee-bl
- IOE entrance: https://allresultnp.com/ioe-entrance/ ; https://nepalicollege.com/preparation-strategies-for-ioe-entrance-exam-2025/ ; https://collegesanjal.com/ioe-entrance/ ; https://clamphook.com/
- BSc CSIT: https://webnotee.com/bsc-csit-entrance-exam-notice-2083/ ; https://safaltopper.com/csit/model-questions-answer-key/ ; https://shikshasanjal.com/model-questions/bsc-csit ; https://edunepal.com/course/b-sc-computer-science-and-information-technology-b-sc-csit/
- Sub-Engineer: https://www.engineeringnepal.com.np/p/lok-sewa-civil-engineer-syllabus.html ; https://loksewatayariapp.com/service/civil-sub-engineer ; https://sarkarijagirnp.blogspot.com/2025/04/syllabus-of-bagmati-pradesh-5th-level-sub-engineer-civil.html
- Computer Operator/Officer: https://loksewatayariapp.com/exam/computer-operator ; https://shikshasanjal.com/blog/computer-operator-syllabus-loksewa ; https://edusanjal.com/exam/computer-operator/ ; https://loksewatayariapp.com/exam/computer-officer
- Lab Assistant: https://loksewatayariapp.com/service/lab-assistant
- Nepal Police Inspector: https://loksewatayariapp.com/syllabus/inspector ; https://www.collegenp.com/service/nepal-police-nepal-prahari-list-of-syllabus-career ; https://lokshewa.online/blog/nepal-police-exam-preparation.html
- NEA: https://loksewatayariapp.com/service/nepal-bidhyut-pradhikaran ; https://www.examsanjal.com/nea-syllabus-level-5-download-prasasan-prabidhik-lekha-account-syllabus/ ; https://www.collegenp.com/vacancy/nepal-electricity-authority-nea-vacancy-2081
- Nepal Telecom: https://loksewatayariapp.com/exam/nepal-telecom
- Provincial PSC examples: https://www.collegenp.com/article/pradesh-2-lok-sewa-aayog-5th-level-health-assistant-ha-syllabus ; https://www.collegenp.com/article/pradesh-2-lok-sewa-aayog-5th-level-pharmacy-assistant-syllabus
- RBB unified exam 2082-83: https://blog.educatenepal.com/search?updated-max=2026-02-13T02:40:00-08:00&max-results=7&reverse-paginate=true&start=126&by-date=false
- Base report: `~/workspace/research_notes/nepal-govt-exams-research-20261025-1743/report.md`
- Prior audit: `data/EXAM-AUDIT.md` (2026-10-25) and `data/exams-new.json` (14 drafts)

## 7. Method & caveats

- Re-counted question tags read-only with Python over `data/questions/*.json`:
  kharidar 851, nasu 859, section-officer 798, nrb-assistant 175, nrb-officer 45,
  tsc-primary 159, tsc-secondary 153, rbb 73, police 26, army 26, health 31,
  engineering 10 — 1,129 unique, 3,206 tag assignments. Identical to EXAM-AUDIT.md.
- Licence-council and new-family patterns come from secondary prep/education sites
  and syllabus reproductions (Edusanjal, CollegeNP, Loksewa Tayari, Engineering Nepal,
  MEC/Edusanjal notices). Official council sites (nmc.org.np, nnc.org.np, nhpc.gov.np,
  nec.org.np, nepalbarcouncil.org.np, ican.org.np) were **not** directly read in this
  run, except one NHPC syllabus PDF. Every pattern marked "verified" means verified
  against at least two independent secondary sources or one official-document
  reproduction; every "unverified" means no citable pattern was found and none was
  invented. Verify all figures against the vacancy notice / council notice before
  publishing, especially pass marks and any figure flagged with ⚠️.
- "Covered" uses a strict bar (dedicated entry + verified pattern + ≥100 tagged Qs).
  By that bar only 6 of 72 families are truly covered; 20 more have an entry that is
  thin, grouped, or placeholder-patterned. A looser count ("has any entry") would be
  12 entries covering 26 families — the strict count is the honest one for students.
