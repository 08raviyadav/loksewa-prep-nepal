# Lok Sewa Prep Nepal — SOURCES.md

**Purpose:** a sourced inventory for builders writing verified MCQs for this portal.
**Do NOT use this file as question content itself** — use it to find the source, read it,
and then write original questions in the project schema
(`{id, exam[], topic, subtopic, difficulty, marks, question, options[4], answer,
explanation, source}`).

**Compiled:** 2026-10-25 (research session, text-fetch only — no live browser visits).
**Prior research this builds on:** `~/workspace/research_notes/nepal-govt-exams-research-20261025-1743/report.md`
(read first; it has the exam-pattern tables this file does not repeat in full).

**Counts:** **38 sources inventoried** (see tables). **10 pages opened/read via text fetch**
(9 read successfully, 1 blocked by a bot-check page — see §9). All other entries are
**search-snippet only** and are marked as such — treat their claims as unverified leads,
not as facts, until someone opens them.

## How to use this file

1. Pick a source, open the URL, and confirm the fact / question against the source itself.
2. Put the **exact URL you actually read** in the question's `source` field.
3. **Never invent a "previous year" label or a URL.** If a paper's year/exam/date is not
   stated on the source page, say so in the question's explanation or leave the year out.
4. **Copyright rule:** government syllabi, Acts, the Constitution, and census data are
   public/government material — facts from them can be freely turned into original MCQs.
   Exam papers themselves are government papers widely reproduced by prep sites; use them
   as a **pattern/topic guide and write original questions** — do not wholesale-copy a
   prep site's or a book's question bank, and do not copy scanned paper images into the repo.
   Anything marked **copyrighted / paywalled** below is paraphrase-only or do-not-use.
5. Label every question set by **syllabus year** (2081/82+ vs pre-2081). The prelim format
   changed — see Conflicts (§8).

## Licence / access key

| Tag | Meaning |
|---|---|
| `OFFICIAL-GOVT` | Published by a Government of Nepal body (PSC, TSC, NRB, NSO, Nepal Army). Free to cite; facts reusable. |
| `OPEN-SHARED` | Freely readable on the open web (prep site / blog / wiki). Facts reusable; do not bulk-copy their question text. |
| `OPEN-DATA` | Open data / reference (Wikipedia, NSO census PDF). Facts reusable; re-verify against the primary source for exam-critical numbers. |
| `PAYWALLED` | Behind a paywall / login / app purchase. Do not rely on it; do not copy from it. |
| `COPYRIGHTED-BOOK` | A commercial book/guide reproduced on a sharing site. Paraphrase-only at most; prefer an official or open source instead. |
| `BLOCKED` | Could not be read in this session (bot-check / dead / login). Listed so nobody wastes time re-trying blind. |

---

## 1. Official government sources (syllabi, notices, data)

| # | Source | Publisher | Contains | Licence / access | Read? |
|---|---|---|---|---|---|
| 1.1 | https://psc.gov.np/uploads/course/20161128034930583c012e8e2d91.pdf | Public Service Commission (psc.gov.np) | PSC course syllabus PDF (Computer Officer stream, per search index) | OFFICIAL-GOVT | Snippet only |
| 1.2 | https://psc.gov.np/uploads/course/20161129030230583d47aa401ed1.pdf | Public Service Commission | PSC course syllabus PDF (Computer Officer / aviation stream) | OFFICIAL-GOVT | Snippet only |
| 1.3 | https://psc.gov.np/uploads/course/202110221211386172aa7a91e4d1.pdf | Public Service Commission | PSC syllabus PDF — Gazetted Class II Officer (plant protection / agriculture) | OFFICIAL-GOVT | Snippet only |
| 1.4 | https://psc.gov.np/site_uploads/course/2025101012513368e9015530a622.pdf | Public Service Commission | PSC syllabus PDF — Foreign Service, Paper III: Nepal's Foreign Policy & Contemporary International Affairs (5 questions, 3×25 + 2×25) | OFFICIAL-GOVT | Snippet only |
| 1.5 | http://psc.gov.np/uploads/course/2017092602060559ca0df1b79272.pdf | Public Service Commission | PSC syllabus PDF — Foreign Service Paper III (same paper, older upload) | OFFICIAL-GOVT | Snippet only |
| 1.6 | https://psc.gov.np/assets/uploads/files/सैन्य_तथा_फलोअर्स_पदको_विज्ञापन.pdf | Public Service Commission | PSC vacancy notice PDF — Nepal Army Sainya & followers posts (advertisement text in Nepali) | OFFICIAL-GOVT | Snippet only |
| 1.7 | http://psc.gov.np/uploads/course/20161111011610582573beb42eb.pdf | Public Service Commission | PSC syllabus PDF — Nepal Forest Service, Subba (Gazetted non-class 1st); written 50 MCQ × 1, 45 min, 20% negative; practical 50 + interview 20; syllabus effective 2074/02/24 | OFFICIAL-GOVT | Snippet only |
| 1.8 | https://tsc.gov.np/ | Teacher Service Commission (TSC) | Official site; syllabus under Publication → Curriculum (पाठ्यक्रम). Secondary-level licence curriculum 2075; general paper + subject paper + interview 25 | OFFICIAL-GOVT | Snippet only (via secondary guide https://samikshas.com.np/posts/what-is-tsc/ — opened? No, snippet only) |
| 1.9 | https://www.nrb.org.np/ (via https://en.wikipedia.org/wiki/Nepal_Rastra_Bank) | Nepal Rastra Bank | NRB official site (not directly opened). NRB facts verified instead from the Wikipedia page (opened) and Edusanjal (opened, §5) | OFFICIAL-GOVT | Snippet only for nrb.org.np itself |
| 1.10 | https://censusnepal.cbs.gov.np/results/files/result-folder/Final%20Population%20Composition.pdf | National Statistics Office (NSO / CBS) | **Official 2021 census thematic report (Population Composition)** — province population, growth, density tables; total 29,164,578 | OFFICIAL-GOVT / OPEN-DATA | Snippet only (PDF text indexed in search; figures cross-checked against the opened Wikipedia census page, §7) |
| 1.11 | https://giwmscdnone.gov.np/media/app/public/36/posts/1710821571_26.pdf | Government of Nepal (NSO report mirror) | Same NSO census population-composition tables as 1.10 | OFFICIAL-GOVT | Snippet only |
| 1.12 | https://media.edusanjal.com/u/cadet_english_20761022.pdf | Edusanjal-hosted copy of an official syllabus | **Nepal Army Officer Cadet English syllabus** — 100 marks, pass 40, 2 hrs 30 min; objective (20 × 1) + subjective (7 × 5, 3 × 10, 1 × 15); effective from 2076/10/22 | OFFICIAL-GOVT (hosted copy) | Snippet only |

**Gap:** no single psc.gov.np URL for the **2081/82 Kharidar / Nayab Subba / Section Officer
first-paper syllabi** was returned by search. The PSC site hosts syllabi as dated PDF uploads
under `/uploads/course/` and `/site_uploads/course/` (see 1.1–1.7), so the 2081/82 PDFs exist
there but were not individually located in this session. **Do not guess their URLs.**
Next step: browse psc.gov.np → syllabus section (live browser) and record the exact links.

---

## 2. Previous-year / old question papers (PSC — Kharidar / NaSu / Section Officer)

| # | Source | Publisher | Contains | Licence / access | Read? |
|---|---|---|---|---|---|
| 2.1 | https://blog.educatenepal.com/2026/09/lok-sewapsc-pre-qualifying-exam-pretest.html | EducateNepal (blog.educatenepal.com) | **Kharidar / Assistant 2nd Class pre-qualifying (pretest) paper, held 2083/06/04 BS, Key A** — 100 marks, 45 min, pass 45; GK, Management, Math, Services-related. Paper itself is **8 scanned images** (blogger.googleusercontent.com); text fetch could not read the questions. Links onward to 2082 pretest paper, 2082-83 syllabi, and "Old Exam Questions for Assistant and Officer Level" reading-material pages for 2080–2083. | OPEN-SHARED (reproduction of a govt paper; images, not text) | **OPENED — text read; question images NOT transcribed** |
| 2.2 | https://www.bidhyamandir.com/nayab-subba-nasu-first-paper-exam-2083-01-20-with-answers-pdf/ | Bidhya Mandir (bidhyamandir.com) | **NaSu First Paper, exam date 2083-01-20** — 50 MCQs, 100 marks, pass 45, 20% negative, 45 min; paper shown as images + a single-PDF download with answer key. Also links Kharidar First Paper 2083-01-26 and Koshi Province 4th Level First Paper 2083-01-26 with answers. | OPEN-SHARED | **OPENED — text read; question images NOT transcribed** |
| 2.3 | https://www.loksewasathi.com/nayab-subba-nasu-2nd-paper-old-questions-2082-83/ | Loksewa Sathi (loksewasathi.com) | **NaSu 2nd Paper old questions 2082-83** — exam date 2083/03/14, 100 marks, pass 40, 2 hrs 30 min; free PDF (images). Same site hosts NaSu 1st Paper 2082 with answers, NaSu/Kharidar 2081/82 syllabi, Section Officer syllabus 2081/82 PDF. | OPEN-SHARED | Snippet only |
| 2.4 | https://loksewaaspirants.com/nayab-subba-old-question-collection-pdf/ | Loksewa Aspirants | NaSu old-question collection PDF (~1 MB) — 2nd & 3rd papers, plus Revenue, MoFA and Law papers; PSC as publisher; Nepali & English | OPEN-SHARED | Snippet only |
| 2.5 | https://dotnepal.com/category/psc-question-collection/page/4/ | DotNepal | **PSC Question Collection archive (8 pages)** — NaSu Foreign Affairs questions 2074 & 2075, NaSu questions 2075, Nepal Police Inspector questions 2073, APF Sipahi questions 2074, Under Secretary (Justice Service) questions 2074, District Judge questions 2075 (1st & 2nd papers), Section Officer computer skill-test model sets (2075, sets 2–5), Computer Operator quiz 2075. **Oldest, broadest archive found; mostly 2073–2075 papers, i.e. pre-2081 pattern — label by year.** | OPEN-SHARED | **OPENED — archive page read; individual paper pages NOT opened** |
| 2.6 | https://www.ioebooster.com/chapter.php?course=Kharidaar-Lok-Sewa-Model-Questions-(First-Paper)&&chapter=Kharidaar-Model-Set-20&&id=60a096bff15ad&&page=3 | IOEBooster | Kharidar model sets — numbered sets (Set 20, Sets 50–60 listed); questions in Nepali; includes dated GK (e.g. FY 2073/74, 2074/75 monetary policy) so sets are old — check dates before reuse | OPEN-SHARED | Snippet only |
| 2.7 | https://edusanjal.com/news/lok-sewa-exam-general-awareness-knowledge-model-questions-part-i/ | Edusanjal | Section Officer General Awareness model questions Part I — matching-type questions (Aristotle/Socrates/Lincoln/Marx; SAARC regional centres; continents; SAARC countries by area). Note: answers were to be posted later in comments — **verify answers independently; do not trust comment-section keys.** | OPEN-SHARED | Snippet only |
| 2.8 | https://loksewaprep.com/na-su-preparation-class | LokSewaPrep | NaSu hub: syllabus guide with official PSC source, **old question papers with hosted PDFs**, topic notes (Constitution 2072, federalism, LDC/landlocked countries). Content-first, recent (Jan–Oct 2026 posts). | OPEN-SHARED | Snippet only |

---

## 3. Syllabus reproductions & prep guides (PSC)

| # | Source | Publisher | Contains | Licence / access | Read? |
|---|---|---|---|---|---|
| 3.1 | https://www.collegenp.com/news/lok-sewa-aayog-revised-syllabus-for-sakha-adhikrit-nayab-subba-and-kharidar | CollegeNP | **2081/82 revision confirmed:** prelim pass mark raised 40 → 45 for Section Officer, NaSu, Kharidar; prelim now qualifying only; the old rule adding 50% of first-paper marks to the main exam removed. Quotes PSC spokesperson Geeta Kumari Humagain. Published 2024-07-26, updated 2026-01-28. | OPEN-SHARED | **OPENED** |
| 3.2 | https://merokalam.com/blog/lok-sewa-aayog-preparation-guide/ | MeroKalam | Kharidar/NaSu/Section Officer preparation guide 2082/83. **CONFLICTS with §8:** states Kharidar/NaSu first paper as 100 Q × 1 mark, 90 min. Treat as outdated/wrong on that point until checked against PSC. | OPEN-SHARED | Snippet only |
| 3.3 | https://www.edusoftacademy.com/blog/kharidar-syllabus-2083-84 | Edusoft Academy | Kharidar syllabus 2083-84 reproduction | OPEN-SHARED | Snippet only (from prior report) |
| 3.4 | https://www.edusoftacademy.com/blog/nayab-subba-syllabus-2082-83 and https://www.edusoftacademy.com/blog/nayab-subba-syllabus-2083-84 | Edusoft Academy | NaSu syllabus 2082-83 and 2083-84 reproductions | OPEN-SHARED | Snippet only (from prior report) |
| 3.5 | https://www.loksewasathi.com/section-officer-syllabus-2081-82-pdf-download/ | Loksewa Sathi | Section Officer syllabus 2081/82 PDF download; stages: Stage I 100 marks (pass 45, not added), Stage II 300 marks (400 for Foreign Service), Final stage 60 marks (70 for Foreign Service) | OPEN-SHARED | Snippet only |
| 3.6 | https://blog.educatenepal.com/2025/12/lok-sewa-exam-syllabus-for-section.html | EducateNepal | Section Officer syllabus 2082-2083; approval date 2081/03/20, exam plan revised 2082/08/22; integrated & unified system; skill/group test + interview in final stage | OPEN-SHARED | Snippet only |
| 3.7 | https://www.gyanpark.com.np/2020/10/section-officer-syllabus.html | GyanPark | Section Officer syllabus (older, 2020 post, updated 2025-03-19) — auditing, parliamentary process & federal system sections | OPEN-SHARED | Snippet only |
| 3.8 | https://www.bidhyamandir.com/nayab-subba-third-paper-service-group-related-free-pdf-notes/ | Bidhya Mandir | NaSu Third Paper (service-group related) syllabus + free PDF notes, effective vacancy year 2081/82 — Office Management & Administrative Behaviour, Public Administration & Management, Legal Provisions Related to Public Service Administration | OPEN-SHARED | Snippet only |
| 3.9 | https://shikshasanjal.com/blog/sakha-adhikrit-section-officer-syllabus | Shiksha Sanjal | Section Officer syllabus guide (source of the "main-paper pass 45" claim in the prior report) | OPEN-SHARED | Snippet only (from prior report) |
| 3.10 | https://loksewajob.com/latest-loksewa-section-officer-syllabus-psc-adhikrit-level-syllabus/ | LoksewaJob | Section Officer syllabus reproduction | OPEN-SHARED | Snippet only (from prior report) |
| 3.11 | https://lokshewa.online/blog/section-officer-adhikrit-preparation.html (and https://lokshewa.online/blog/kharidar-exam-preparation-guide.html, https://lokshewa.online/blog/nayab-subba-exam-preparation.html) | Crack Lokshewa (lokshewa.online) | Exam preparation guides for Section Officer, Kharidar, NaSu | OPEN-SHARED | Snippet only (from prior report) |

---

## 4. Teacher Service Commission (TSC) & teaching licence

| # | Source | Publisher | Contains | Licence / access | Read? |
|---|---|---|---|---|---|
| 4.1 | https://www.collegenp.com/service/teachers-service-commission-tsc-bhaktapur-tsc-exams-utility-service | CollegeNP | TSC exam details: general paper 50 × 2 = 100, pass 50, 20% negative; subject paper 100, pass 40, 3 hrs; interview 25; OMR-sheet rules (black ball pen, Key A/B/C/D must be filled or sheet cancelled); syllabus areas (GK, education knowledge, ICT, Constitution/Acts, IQ) | OPEN-SHARED | Snippet only |
| 4.2 | https://edusanjal.com/post/lower-secondary-level-curriculum-of-english-tsc/ | Edusanjal | TSC Lower Secondary English curriculum (subjective exam 2076) — 10 units × 10 marks = 100, Sections A (pedagogy) & B (content); effective 2077/02/30 | OPEN-SHARED | Snippet only |
| 4.3 | https://www.collegenp.com/exam/secondary-level-teachers-license-english-subject-curriculum-tsc | CollegeNP | TSC Secondary-level teachers' licence English curriculum 2075 — First Paper English 65 marks; Sections A (content knowledge, 40) & B (pedagogical content knowledge); based on Teacher Competency Framework 2072 | OPEN-SHARED | Snippet only |
| 4.4 | https://english.headlinenepal.com/details/20661 | Headline Nepal (English) | **Teaching licence exam now 100% objective:** 50 Q × 2 = 100, pass 50; previously 60% thematic / 40% objective; change effective 16 March (year not stated in snippet — verify); applies to secondary & lower-secondary licence; TSC Deputy Secretary / Information Officer Sudarshan Marhattha quoted | OPEN-SHARED | Snippet only |
| 4.5 | https://www.collegenp.com/blog/becoming-a-government-teacher-process-prep-and-success-strategy | CollegeNP | TSC strategy guide: general paper is the main filter (~90% eliminated, pass 50 + 20% negative); section weightage (GK 30–40%, education knowledge 20–30%, ICT ~10%, law: Education Act 2028, TSC Regulations 2057, Constitution Art. 31); IQ section | OPEN-SHARED | Snippet only |
| 4.6 | https://shikshasanjal.com/syllabus/tsc-lower-secondary-and-primary-level-syllabus | Shiksha Sanjal | TSC lower-secondary & primary syllabus | OPEN-SHARED | Snippet only (from prior report) |
| 4.7 | https://exammate.barala.com.np/2026/01/tsc-ma-vi-first-paper-syllabus-for-all.html | ExamMate (Barala) | TSC Ma Vi (secondary) first-paper syllabus | OPEN-SHARED | Snippet only (from prior report) |

**Gap:** no Nepal-specific TSC **previous-year general-paper** set with questions + answer key
was found in this session. The licence-exam change (4.4) is recent — confirm the year and
whether primary-level licence is also 100% objective before writing licence questions.

---

## 5. Nepal Rastra Bank & public banks (NRB / RBB / NBL / ADBL)

| # | Source | Publisher | Contains | Licence / access | Read? |
|---|---|---|---|---|---|
| 5.1 | https://edusanjal.com/exam/assistant-second-class-nrb/ | Edusanjal | **NRB Assistant 2nd Class, full pattern (verified live):** Prelim 50 × 2 = 100, 45 min, pass 40, 20% negative — Mgmt & Accounting 30 (15 Q), Econ & Banking 30 (15 Q), Maths 14 (7 Q), Computer 14 (7 Q), GK 12 (6 Q); Written Paper I (Banking 4×10, Accounting 3×10, Maths 4×5, Computer 2×5) 100/pass 40/2.5 hrs; Paper II (Econ, Mgmt, Banking Laws & Policies; 8×5 + 6×10) 100/pass 40/2.5 hrs; Interview 30 (30 min oral). Prelim marks not added. | OPEN-SHARED | **OPENED** |
| 5.2 | https://blog.educatenepal.com/search?updated-max=2026-02-13T02:40:00-08:00&max-results=7&reverse-paginate=true&start=126&by-date=false | EducateNepal (blog search page) | RBB/NBL/ADBL unified Level-4 syllabus 2082-2083 (approved 2082-06-09): Written 200 (Paper I Banking/Mgmt/Accounting/Maths/IT 100/pass 40/2.5 hrs subjective; Paper II service/group/institution-related 100/pass 40/2.5 hrs) + Interview 30 | OPEN-SHARED | Snippet only (from prior report; search-page URL, not a stable article link) |
| 5.3 | http://loksevasarathi.blogspot.com/2026/07/rbb-level-5-exam-preparation-2083-2026.html | Loksewa Sarathi (Blogspot) | **RBB Level 5 (Senior Assistant) 2083:** Paper I Econ/Banking/GK — 50 MCQ × 1 + 10 × 5 subjective = 100, pass 40; Paper II Governance & Office Management — 12 × 5 + 4 × 10 = 100, pass 40; Interview 30; black ballpoint pen only | OPEN-SHARED | Snippet only |
| 5.4 | https://www.collegenp.com/career/how-to-get-job-in-nepal-rastra-bank-nrb-step-by-step-guide | CollegeNP | NRB guide: 16-week plan; Officer track (macro, monetary policy, NRB Act 2058, BAFIA 2017); Assistant track; IT stream split (30 min objective + 2.5 hrs descriptive per paper); practical 50 for IT | OPEN-SHARED | Snippet only |
| 5.5 | https://en.wikipedia.org/wiki/Nepal_Rastra_Bank | Wikipedia | NRB history & facts — see fact-checks §10 (est. 1956, first governor, first banknotes, IMF/WB 1961, ACU 1974, dual currency ended 1964, NRB Act 2058, first monetary policy 2002/03, 8 provincial offices) | OPEN-DATA | **OPENED** |
| 5.6 | https://shyamkumarkc20.com.np/nepalrastrabank | Shyam Kumar KC (personal/educational site) | NRB introduction: est. 1956 (2013 Baisakh 14) under NRB Act 1955 (2012 BS); NRB Act 2058 preamble objectives (monetary & forex policy, price stability, balance of payments, secure payment system, supervision, public confidence) | OPEN-SHARED | Snippet only |
| 5.7 | https://english.nepalnews.com/s/explainers/everything-you-need-to-know-about-nepal-rastra-bank-nrb/ | NepalNews (English) | NRB explainer: est. 26 Apr 1956; NRB Act 2058 (2002); Governor Biswo Nath Poudel; FATF grey-list context (current-affairs, date-sensitive — do not bake into timeless questions) | OPEN-SHARED | Snippet only |

---

## 6. Nepal Police, Armed Police Force, Nepal Army

| # | Source | Publisher | Contains | Licence / access | Read? |
|---|---|---|---|---|---|
| 6.1 | https://www.pratimaedu.com/nepal-army-officer-cadet-entrance-exam/ | Pratima Academy (pratimaedu.com) | **Officer Cadet 2083 (Advt. 083/84/01, dated 2083/04/29): 280 posts** (Open 146, women 24, Janajati 39, Madhesi 33, Dalit 18, backward regions 6, deceased/disabled soldiers' children 14); age 18–21 (+2) / 18–24 (Bachelor's) / to 26 (serving soldiers); height M 5'3" F 5'0", weight M 50 kg F 40 kg, chest 32"/34"; **written: IQ 60 marks/30 min, English 100/3 hrs, Nepali 100/3 hrs, Maths 100/3 hrs, GK 100/90 min**; PFT standards (sit-ups M15/F8, push-ups M12/F7, chin-ups M5/F3, 300 m M55s/F65s, 2-mile M16 min/F19 min); 8 stages incl. IQ test, officer-quality assessment, final interview; model questions (Nepali 2076) linked. **Note: pattern table says English 3 hrs but the official English syllabus (1.12) says 2 hrs 30 min — flag, verify.** | OPEN-SHARED (coaching site summarising an official notice) | **OPENED** |
| 6.2 | https://loksewatayariapp.com/syllabus/officer-cadet/iq-test-syllabus-officer-cadet | Loksewa Tayari App | Officer Cadet IQ syllabus; written papers English/Nepali/Maths/GK each 100, pass 40 each; English split subjective 60 (3×10 + 3×5 + 2×5 + 5×1) + objective 40 × 1 | OPEN-SHARED | Snippet only |
| 6.3 | https://www.collegenp.com/service/nepal-army-nepal-army-exam-list-career | CollegeNP | Nepal Army exam list: stages (bearing, medical, PFT, written by PSC, Pre-OCS psychological/IQ — TO/GT/IO, final interview at Jangi Adda); Sainya written at Grade 8/10 level; Officer Cadet at +2/Bachelor's level + IQ | OPEN-SHARED | Snippet only |
| 6.4 | https://www.collegenp.com/service/nepal-police-nepal-prahari-list-of-syllabus-career | CollegeNP | **Nepal Police syllabus:** Inspector 3 papers × 100 (GK & IQ; English & Nepali; Professional Practical Knowledge & Legal System — Constitution, Muluki Criminal Code, Criminal Procedure Code, Nepal Police Act 2012, Police Regulations 2071, human rights); ASI 3 papers × 100 (GK & IQ; Nepali 60 + English 40; Professional Practical Knowledge); Constable 100 (Nepali 30, English 15, Maths 25, GK & police service 30) | OPEN-SHARED | Snippet only |
| 6.5 | https://policereportonlinenp.com/nepal-police-asi/ | Police Report Online NP | Nepal Police ASI 2026 guide: eligibility, age, physical, exam; advises studying Constitution (fundamental rights, directive principles, state structure), Nepal Police Act, basic criminal law; previous-year papers under timed conditions | OPEN-SHARED | Snippet only |
| 6.6 | https://www.collegenp.com/exam/nepal-police-inspector-and-asi-written-exam-re-schedule-2077 | CollegeNP | Nepal Police Inspector & ASI written exam re-schedule 2077: Paper 1 GK & IQ (50 min), Paper 2 English & Nepali (2.5 hrs), Paper 3-I Professional Theory (2 hrs 15 min), Paper 3-II Professional Behavioural Test (45 min); 2,014 candidates (Inspector stream) | OPEN-SHARED | Snippet only |
| 6.7 | https://www.collegenp.com/service/apf-nepal-vacancy-list | CollegeNP | **APF eligibility:** Inspector age 21–25, Bachelor's, height M 5'2" F 5'0", chest M 31"–33"; ASI age 18–23, +2, height M 5'2" F 5'0", weight M 50 kg F 42 kg; Jawan age 18–22, Class 8; Followers age 18–25; selection: registration/initial medical → physical endurance (300 m, long/high jump, sit-ups, push-ups, 2-mile/3.2 km) → detailed medical → written (PSC) → special medical → interview | OPEN-SHARED | Snippet only |
| 6.8 | https://www.collegenp.com/vacancy/apf-nepal-vacancy-for-asi-and-inspector-posts-2082 | CollegeNP | APF ASI & Inspector vacancy 2082: application, fee, documents, 8 selection stages (incl. IQ test + aptitude test for Inspector-General group only) | OPEN-SHARED | Snippet only |
| 6.9 | https://www.collegenp.com/exam/written-exam-schedule-for-armed-police-inspector-and-asi-2081 | CollegeNP | APF Inspector & ASI written schedule 2081: Inspector — Nepali, English, GK, Constitution & Law, Professional Subjects (2082 Jestha 12–14) + psychological personality test; ASI — Nepali & English, GK, Constitution & Professional Subjects (2082 Baisakh 30–Jestha 1); Advt. 01/081-82 & 02/081-82 | OPEN-SHARED | Snippet only |
| 6.10 | https://edusanjal.com/vacancy/vacancy-for-various-posts-armed-police-force-apf/ | Edusanjal | APF vacancy 2081/82: Inspector 68 posts, ASI 83, Constable 981, Parichar (cook/cleaner/sweeper/hairdresser/leatherworker) 86; contact/initial exam 2081/11/06 | OPEN-SHARED | Snippet only |
| 6.11 | https://www.collegenp.com/vacancy/nepal-army-officer-cadet-vacancy-2083 | CollegeNP | Nepal Army Officer Cadet vacancy 2083 (secondary report of the same notice as 6.1) | OPEN-SHARED | Snippet only (from prior report) |

**Gap:** no Nepal Police / APF **previous-year MCQ paper with answer key** was found as a
readable text source in this session. DotNepal (2.5) has Inspector 2073 and APF Sipahi 2074
papers as scanned posts — open those individual pages next. The Scribd "ASI Darpan" book (§9)
is not a substitute.

---

## 7. Reference / fact sources (Constitution, census, geography)

| # | Source | Publisher | Contains | Licence / access | Read? |
|---|---|---|---|---|---|
| 7.1 | https://en.wikipedia.org/wiki/Constitution_of_Nepal | Wikipedia | **Constitution of Nepal 2072** — 35 parts, 308 articles, 9 schedules; effective 20 Sep 2015; 31 fundamental rights (Part 3, Arts. 16–46); Art. 4 federal democratic republic; HoR 275 + NA 59; President elected by electoral college; Council of Ministers ≤ 25; amended twice (2016, 2020 — 2nd amendment 18 June 2020); 538 of 598 CA members voted in favour. **Note: page carries a "needs more citations" banner (Sep 2026).** | OPEN-DATA | **OPENED** |
| 7.2 | https://en.wikipedia.org/wiki/Constitution_of_Nepal_2015 | Wikipedia | Same constitution, alternate article (fundamental-rights list Arts. 16–46 identical) | OPEN-DATA | Snippet only |
| 7.3 | https://lokshewa.online/blog/nepal-constitution-important-questions.html | Crack Lokshewa | Constitution 2072 important questions for Lok Sewa: 9 schedules, 31 fundamental rights (Arts. 16–46), Art. 4, 753 local levels (6 metro, 11 sub-metro, 276 municipalities, 460 rural municipalities); free 50-Q constitution mock sets | OPEN-SHARED | Snippet only |
| 7.4 | https://loksewapathsala.com/constitution-of-nepal/ | Loksewa Pathsala | Constitution of Nepal at a glance: promulgated Ashoj 3, 2072 (20 Sep 2015) by President Ram Baran Yadav; 2nd Constituent Assembly (601 members), chair Subas Chandra Nembang; **507 votes in favour (CONFLICTS with 7.1's 538 — see §8)**; 35 parts, 308 articles, 9 schedules; 2 amendments (2016, 2020); Constitution Day Ashoj 3; table of all 7 constitutions (2004–2072 BS) | OPEN-SHARED | **BLOCKED — bot-check page ("One moment, please...") on text fetch; figures above are search-snippet only** |
| 7.5 | https://meroadalat.com/fundamental-rights-and-duties/ | Mero Adalat (law firm) | Full numbered list of the 31 fundamental rights, Arts. 16–46 (dignity 16, freedom 17, equality 18, communication 19, justice 20, victim of crime 21, against torture 22, against preventive detention 23, against untouchability/discrimination 24, property 25, religion 26, information 27, privacy 28, against exploitation 29, clean environment 30, education 31, language & culture 32, employment 33, labour 34, health 35, food 36, housing 37, women 38, child 39, Dalit 40, senior citizens 41, social justice 42, social security 43, consumer 44, against exile 45, constitutional remedies 46) | OPEN-SHARED | Snippet only |
| 7.6 | https://en.wikipedia.org/wiki/2021_Nepal_census | Wikipedia | **2021 census (12th census, 11–25 Nov 2021, first under federal structure):** total 29,164,578; M 14,253,551 / F 14,911,027; growth 0.92%/yr; density 198/km²; sex ratio 95.59; households 6,666,937; literacy 76.2% (M 83.6%, F 69.4%); province table (Bagmati 6,116,866 most populous; Karnali 1,688,412 least; Madhesh density 633 highest); belt split Terai 53.61% / Hill 40.31% / Mountain 6.08%; urban 66.17% / rural 33.83%; largest district Kathmandu 2,041,587; smallest Manang 5,658; largest caste Chhetri 16.45% (4,796,995); 146 castes/ethnicities | OPEN-DATA | **OPENED** |
| 7.7 | http://topnepali.com/population-of-nepal-district-and-province | TopNepali | Same 2021 census province/district populations as 7.6, in table form | OPEN-SHARED | Snippet only |
| 7.8 | https://en.wikipedia.org/wiki/List_of_Nepalese_provinces_by_population | Wikipedia | Provinces by 2021 population (same figures as 7.6) | OPEN-DATA | Snippet only |
| 7.9 | https://saudigazette.com.sa/article/601156/World/Asia/China-and-Nepal-end-dispute-over-Mount-Everests-height | Saudi Gazette | Everest height 8,848.86 m jointly announced by Nepal & China, 8 Dec 2020; previous 8,848 m (1954/1955 Indian survey); China 2005 estimate 8,844 m not recognised by Nepal | OPEN-SHARED | Snippet only |
| 7.10 | https://nepaldivorce.com/blog/the-legal-system-of-nepal | Nepal Divorce (law blog) | Legal-system guide: Constitution 35 parts / 308 articles / 9 schedules; HoR 275 + NA 59; Supreme Court + 7 High Courts + 77 District Courts; Art. 274 amendment (two-thirds majority); Civil Code 2074 & Penal Code 2074 | OPEN-SHARED | Snippet only |

---

## 8. Free practice platforms & tools (do NOT copy their question banks)

| # | Source | Publisher | Contains | Licence / access | Read? |
|---|---|---|---|---|---|
| 8.1 | https://lokshewa.online/ | Crack Lokshewa | Free bilingual mock tests; 50 MCQ / 45 min with 20% negative marking; Kharidar, NaSu, Section Officer, Police Constable, Staff Nurse, Computer Operator, GK, Constitution, IQ | OPEN-SHARED (free site; its questions are its own content — use as pattern reference only) | Snippet only |
| 8.2 | https://loksewapathsala.com/ | Loksewa Pathsala | Free notes, 270+ quizzes, mock tests, current affairs with MCQs, old questions; Kharidar/NaSu/Section Officer/Computer Operator; vacancy tracker (e.g. Nepal Police ASI 211 posts, 2083) | OPEN-SHARED | Snippet only (constitution page blocked, §7.4) |
| 8.3 | https://techpsc.com/ | TechPSC | Technical PSC prep (civil, NEC/NHPC); free MCQs, old papers, syllabus PDFs. **Open-sourced only its MCQ validator** (`techpsc-mcq-toolkit`, MIT, Node.js, validates MCQ JSON incl. Nepali Unicode) — the question library itself is NOT open. | OPEN-SHARED (validator MIT; questions proprietary) | Snippet only |
| 8.4 | https://hamroloksewa.com/ | Hamro Loksewa | Topic-wise MCQs, free & premium sets, previous questions, leaderboard/streaks (from prior report) | OPEN-SHARED / freemium | Snippet only (from prior report) |
| 8.5 | https://www.kbr.com.np/ | Loksewa Solution (KBR) | Claims 50k+ verified questions, AI-adaptive mocks, previous-year papers with keys (from prior report) — premium; do not copy | PAYWALLED | Snippet only (from prior report) |
| 8.6 | https://psc.guru/ | PSC Guru | 2,000+ exam-style questions, daily quizzes, mocks mirroring exact paper (from prior report) | OPEN-SHARED / freemium | Snippet only (from prior report) |
| 8.7 | https://play.google.com/store/apps/details?id=com.divas_regmi.loksewaapp&hl=en-US | Loksewa by GyanUdaan (Play Store) | App: 50,000+ questions incl. past papers; states its govt info is collected from public domains & official sites; official source listed as https://psc.gov.np | PAYWALLED / app | Snippet only |

---

## 9. Promising but paywalled / copyrighted / blocked — do NOT use as sources

| Source | Why it looked promising | Why it is listed here instead |
|---|---|---|
| https://www.scribd.com/document/624801371/2nd-paper | Section Officer 2nd-paper syllabus text (governance systems, constitutionalism, public service, resource management) | **Scribd — paywalled/login.** Syllabus content itself is a PSC document; get it from psc.gov.np (1.x) instead. |
| https://www.scribd.com/document/670226442/Loksewa-Iq-Neptechpal-com | "Loksewa IQ" — NaSu model question sets 23 & 29 (2022), Kharidar sets, Nepal history GK | **Scribd — paywalled.** Model sets of unknown authorship; paraphrase-only at most. |
| https://www.scribd.com/doc/51511659/ASI-Darpan | "ASI Darpan: Nepal Police Exam Guide" — book for Nepal Police ASI entrance, publ. Pinnacle Publications, Bagbazar | **COPYRIGHTED-BOOK.** Commercial guide. Do not copy; use the official ASI syllabus (6.4–6.6) instead. |
| https://www.scribd.com/document/469773441/Nepal-Army-Officer-Cadet-English-Exam-Question | Nepal Army Officer Cadet English exam syllabus (same text as the Edusanjal-hosted PDF, 1.12) | **Scribd — paywalled.** Use the Edusanjal-hosted PDF (1.12) instead. |
| https://www.scribd.com/document/616735633/2079-8-10-Engineer | Engineering Lok Sewa / ME entrance MCQs | **Scribd — paywalled.** Not in current scope anyway. |
| https://www.scribd.com/document/721183780/downloaded-file-2 | Teachers' licensing test handbook (not Nepal-specific; generic pedagogy) | **Scribd — paywalled; wrong country context.** Ignore. |
| https://loksewapathsala.com/constitution-of-nepal/ | Constitution at-a-glance page (see 7.4) | **BLOCKED** — Cloudflare-style bot-check on text fetch ("One moment, please..."). Figures cited here are snippet-only. Retry via live browser if needed. |
| https://testpointpk.com/v2.testpoint.pk/public/index.php/past-papers-mcqs/asf-past-papers?page=20 | ASF (Airport Security Force) past papers — surfaced for "ASI" search | **Wrong country (Pakistan ASF, not Nepal APF/Police).** Ignore. |
| https://www.slideshare.net/slideshow/licensure-examination-for-teachers-set-2-part-2-79947373/79947373 | Teacher licensure exam, 50 items with answers | **Wrong country (Philippines-style licensure exam).** Ignore for Nepal TSC. |
| https://boame.net/wp-content/uploads/2023/10/MULTIPLE-SUBJECTS-CONTENT-FOR-PRIMARY-EDUCATION-PAST-QUESTIONS.pdf | Primary teacher licensure past questions | **Wrong country (Ghana GTLE).** Ignore for Nepal TSC. |
| https://www.academia.edu/76411037/Evolutionary_Overview_of_Central_Banking_in_Nepal_An_Account_of_Law_and_Practice | Central banking in Nepal — NRB Act 2012, first banknotes Ashwin 3, 2016 BS (19 Sep 1959), dual currency, IMF/WB 1961 | Academia.edu — login-gated for full text; snippet gives useful dates but **verify against nrb.org.np / Wikipedia (opened, 5.5)**. Note the first-banknote date conflict in §10. |
| YouTube: https://www.youtube.com/watch?v=fQniYiLBumQ | TSC Secondary English specification grid / testing system video | Video, not a citable text source; use the Edusanjal/CollegeNP curriculum pages (4.2, 4.3) instead. |

**No open GitHub question bank was found.** Search for "github loksewa question bank" returned
no GitHub repo with an open MCQ bank — only TechPSC's MIT validator toolkit (8.3, validator only,
no questions) and commercial apps. If a builder later finds a repo, record its licence before
using a single question from it.

---

## 10. Conflicts, dead links & things to verify before writing questions

1. **Kharidar / NaSu prelim format — MAJOR CONFLICT.**
   - 50 MCQs × 2 marks = 100, 45 min, pass 45: Bidhya Mandir NaSu paper 2083-01-20 (**opened**),
     EducateNepal Kharidar paper 2083/06/04 (**opened**), Crack Lokshewa (50 MCQ/45 min).
   - 100 MCQs × 1 mark = 100, 90 min: MeroKalam guide (snippet only, §3.2) and pre-2081 sources.
   - Resolution: the 50×2/45-min format is the **2081/82-revised** format; the 100×1 format is
     pre-revision. The prior report already flagged this. **Portal rule: label every prelim set
     by syllabus year; never mix the two formats in one mock.**
2. **Section Officer main-paper pass marks: 40 vs 45.** Older reproductions say 40; newer guides
   (Shiksha Sanjal) say 45. Unresolved — verify against the PSC syllabus PDF.
3. **Section Officer final-stage total: 60 vs 70.** Loksewa Sathi (§3.5): 60 (70 for Foreign
   Service); Edusanjal (prior report): 70 (80 for Foreign Affairs). Unresolved.
4. **Section Officer prelim pass: 40 (pre-2081/82) vs 45 (from 2081/82).** Resolved in favour
   of 45 — CollegeNP (**opened**, §3.1) quotes the PSC spokesperson; EducateNepal 2083 paper
   (**opened**) also requires 45. The old 40 figure is pre-revision.
5. **TSC general-paper merit weightage:** one Ma Vi source says 50% of general-paper marks
   count toward final merit; CollegeNP says only the subjective paper counts. Unresolved.
6. **Nepal Police ASI age/education:** 18–24 with +2 (general) vs 21–30 / Bachelor's in some
   notices — varies by technical vs general stream and vacancy year. Always cite the vacancy
   notice year.
7. **Officer Cadet English paper duration: 3 hrs (PratimaEdu, opened) vs 2 hrs 30 min**
   (official English syllabus PDF, §1.12). Verify against the 2083 notice.
8. **Constitution votes in favour: 538 of 598 (Wikipedia, opened) vs 507 (Loksewa Pathsala,
   snippet only).** The 507 figure likely counts something else (or is an error). **Do not
   write a question on the vote count until this is resolved** against the Constituent
   Assembly record.
9. **NRB first banknotes: 19 Sep 1959 (Ashwin 3, 2016 BS — Academia.edu snippet; also the
   "started issuing" date) vs 19 Feb 1960 (Wikipedia NRB page, opened: "released its first
   bank notes … Mohru 1").** Possibly two different events (first issue vs first release of a
   denomination). **Do not write a first-banknote-date question until resolved** via nrb.org.np.
10. **NRB Assistant prelim pass mark is 40, NOT 45** — unlike PSC prelims. Confirmed on the
    opened Edusanjal page (§5.1). Do not copy the PSC 45 into NRB mocks.
11. **NaSu paper date vs weekday:** Bidhya Mandir labels the 2083-01-20 paper "Sunday".
    2083-01-20 BS converts to ~3 May 2026; weekday not verified. Do not repeat the weekday
    claim in questions.
12. **EducateNepal Kharidar paper (2.1) is images only** — the 8 scanned pages were not
    transcribed in this session. A builder with OCR (or a live-browser read) still needs to
    extract the actual questions; the answer key (Key A) is in the images, not in the text.
13. **Edusanjal Section Officer model questions (2.7)** promise answers "later in comments" —
    answers are unverified. Re-derive every answer from a primary source.
14. **Current-affairs volatility:** NRB governor (Biswo Nath Poudel, appointed May 2025),
    vacancy counts (Officer Cadet 280 in 2083; APF Inspector 68 / ASI 83 / Constable 981 in
    2081/82; Nepal Police ASI 211 posts in 2083 per Loksewa Pathsala) and FATF grey-list status
    change. Date-stamp any such question and prefer timeless facts for the core bank.

---

## 11. Verified fact-checks / question ideas (25)

Every item below was verified in a page **actually opened and read** in this session
(URL given per item). A builder may turn each into one MCQ in the project schema, using the
listed URL as the question's `source`. Suggested exam/topic tags are hints only.

### Constitution of Nepal 2072 (source: https://en.wikipedia.org/wiki/Constitution_of_Nepal — OPENED)

1. The Constitution has **35 parts, 308 articles and 9 schedules**. → exam: `section-officer, nayab-subba, kharidar, tsc`; topic: `constitution`.
2. It was promulgated on **20 September 2015 (Ashoj 3, 2072 BS)**, replacing the Interim Constitution of 2007. → topic: `constitution`.
3. **31 fundamental rights** are guaranteed in **Part 3, Articles 16–46**. → topic: `constitution`.
4. **Article 4** declares Nepal an independent, indivisible, sovereign, secular, inclusive, democratic, socialism-oriented federal democratic republican state. → topic: `constitution`.
5. **Article 31** is the right relating to education (TSC-relevant; Art. 31 is also cited in the TSC law section — CollegeNP snippet, §4.5). → exam: `tsc`; topic: `constitution`.
6. The right to constitutional remedies is **Article 46**; the right to live with dignity is **Article 16**; the right to equality is **Article 18**. → topic: `constitution`.
7. The Constitution has been **amended twice** since promulgation (1st in 2016, 2nd on 18 June 2020); amendment is by **Article 274** (two-thirds majority — Art. 274 per §7.10 snippet; verify article number against the Constitution text before finalising). → topic: `constitution`.
8. The Federal Parliament is bicameral: **House of Representatives 275 seats + National Assembly 59 seats**. → topic: `constitution`.
9. The **President is elected by an electoral college** of Federal Parliament + State Assembly members; a person elected twice as President cannot stand again; President and Vice-President must be of different sex or community. → topic: `constitution`.
10. The **Council of Ministers shall not exceed 25 ministers** including the Prime Minister. → topic: `constitution`.

### Census 2021 (source: https://en.wikipedia.org/wiki/2021_Nepal_census — OPENED; figures match the official NSO report, §1.10)

11. Total population **29,164,578** (male 14,253,551; female 14,911,027); annual growth rate **0.92%**; density **198 persons/km²**. → topic: `nepal-gk`.
12. **Bagmati is the most populous province (6,116,866)** and **Karnali the least (1,688,412)**. → topic: `nepal-gk`.
13. **Madhesh has the highest population density (633/km²)**; Karnali the lowest (60/km²). → topic: `nepal-gk`.
14. By ecological belt: **Terai 53.61%, Hill 40.31%, Mountain 6.08%** of the population. → topic: `nepal-gk`.
15. Literacy rate **76.2%** overall (male 83.6%, female 69.4%); **6,666,937 households**. → topic: `nepal-gk`.
16. **Kathmandu is the most populous district (2,041,587)**; **Manang the smallest (5,658)**. → topic: `nepal-gk`.
17. The 2021 census was the **12th nationwide census**, held **11–25 November 2021**, and the **first conducted under the federal structure** (7 provinces, 77 districts, 753 local bodies). → topic: `nepal-gk`.
18. Largest caste/ethnic group: **Chhetri, 16.45% (4,796,995)**; **146 castes/ethnicities** were recorded in 2021. → topic: `nepal-gk`.

### Nepal Rastra Bank (sources: https://en.wikipedia.org/wiki/Nepal_Rastra_Bank — OPENED; https://edusanjal.com/exam/assistant-second-class-nrb/ — OPENED)

19. NRB was established on **26 April 1956 (Baisakh 14, 2013 BS)** under the Nepal Rastra Bank Act, 1955; its first governor was **Himalaya Shumsher J.B. Rana** (26 Apr 1956 – 7 Feb 1961). → exam: `nrb-assistant`; topic: `banking`.
20. NRB now operates under the **Nepal Rastra Bank Act, 2058 (2002)**; it formulated its **first monetary policy in FY 2002/03**. → exam: `nrb-assistant`; topic: `banking`.
21. Nepal's first commercial bank, **Nepal Bank Ltd., was established in 1937** — 19 years before NRB. → exam: `nrb-assistant`; topic: `banking`.
22. Nepal joined the **IMF and the World Bank in 1961**; NRB became a founding member of the **Asian Clearing Union in 1974**; the **dual-currency period ended in 1964**. → exam: `nrb-assistant`; topic: `banking`.
23. NRB has its central office in **Baluwatar, Kathmandu**, and **eight provincial offices** (Biratnagar, Janakpur, Birgunj, Pokhara, Siddharthanagar, Nepalgunj, Surkhet, Dhangadhi). → exam: `nrb-assistant`; topic: `banking`.
24. **NRB Assistant prelim pattern (exam fact, not GK):** 50 × 2 = 100, 45 min, **pass 40**, 20% negative — Mgmt & Accounting 30, Econ & Banking 30, Maths 14, Computer 14, GK 12; prelim marks are **not added** to later stages. → exam: `nrb-assistant`; topic: `exam-pattern`. (Use to build/verify a mock, not as a GK question.)
25. **NaSu prelim pattern (exam fact):** 50 MCQs × 2 = 100, **45 min, pass 45**, 20% negative — confirmed by the actual 2083-01-20 paper (https://www.bidhyamandir.com/nayab-subba-nasu-first-paper-exam-2083-01-20-with-answers-pdf/ — OPENED) and the Kharidar paper held 2083/06/04 (https://blog.educatenepal.com/2026/09/lok-sewapsc-pre-qualifying-exam-pretest.html — OPENED). → exam: `nayab-subba, kharidar`; topic: `exam-pattern`.

### Deliberately NOT included as verified fact-checks

- Everest height 8,848.86 m (joint Nepal–China announcement, 8 Dec 2020) — seen only in search
  snippets (§7.9); **not opened**, so it is not in the verified list above. It is a strong
  candidate for the next round: open the Saudi Gazette / a Nepal government source and add it.
- Any question taken from the scanned paper images (2.1, 2.2) — the images were not transcribed;
  a builder must OCR/read them first and cite the paper page URL.

---

## 12. Gaps — what was NOT found (next research round)

- Direct psc.gov.np URLs for the 2081/82 Kharidar, NaSu and Section Officer syllabi (§1, Gap).
- A readable-text Nepal Police / APF previous-year MCQ paper with answer key (§6, Gap).
- A Nepal-specific TSC previous-year general-paper set with questions + key (§4, Gap).
- An openly licensed / GitHub-hosted MCQ bank for any of these exams (§9 — none found).
- Official tsc.gov.np syllabus PDFs (site structure known: Publication → Curriculum; exact PDF
  URLs not captured — live-browser task).
- The official Constitution text itself (lawcommission.gov.np / Nepal Law Commission) — the
  fact-checks above rest on Wikipedia; re-verify article numbers against the official text
  before publishing constitution questions.
- NRB Assistant / Officer previous-year papers (only the pattern, §5.1, was verified — no past
  paper with questions was found).
- RBB/NBL/ADBL previous-year papers (only the unified syllabus, §5.2–5.3).

---

*End of SOURCES.md — 38 sources inventoried; 10 pages opened (9 read, 1 bot-blocked);
25 verified fact-checks from opened pages. Do not edit question JSON or app code from this file;
it is an inventory only.*

## 13. Previous-year transcription (2026-10-26) — 133 real questions landed

Round 3 (text-fetch only) got **0** — the papers are scanned images. A live-browser/OCR
pass on 2026-10-26 then read all four 2083 papers question by question from the source
pages/PDFs and transcribed them into `data/questions/previous-year-2083.json` (**133
questions**, all bilingual, all with a verified answer from the source):

| Paper | Transcribed | PDF |
|---|---|---|
| NaSu First Paper 2083-01-20 | **43 of 50** | https://www.bidhyamandir.com/wp-content/uploads/2026/05/Nasu-First-Paper-2082-83.pdf |
| Kharidar First Paper 2083-01-26 | **45 of 50** | https://www.bidhyamandir.com/wp-content/uploads/2026/05/Kharidar-first-paper-2083-01-26.pdf |
| Koshi Province 4th Level First Paper 2083-01-26 | **45 of 50** | https://www.bidhyamandir.com/wp-content/uploads/2026/05/4th-Koshi-first-paper-2083-01-26.pdf |
| Kharidar pretest 2083/06/04 (Key A) | **0 — scanned-only, no answer key exists** | https://blog.educatenepal.com/2026/09/lok-sewapsc-pre-qualifying-exam-pretest.html |

Excluded from the text bank: figure-based questions (image options/diagrams — NaSu
Q40/Q44/Q47/Q48/Q49/Q50, Kharidar Q23/Q25/Q28/Q41/Q48, Koshi Q46–Q50) and NaSu Q45,
whose options differ only by capitalisation (FridAY vs FRIday) and cannot be scored
fairly as a text MCQ. Koshi's paper numbers two questions 40 — kept as 40a and 40b.
NaSu Q11 is a dual-answer (flawed) question: both Tuberculosis and Leprosy are correct
per the paper's own note; the explanation says so, and the answer field keeps the
paper's first-listed answer (A). Answers are exactly as printed/highlighted in the
sources, even where a key looks factually debatable (e.g. NaSu Q2, Q28; Kharidar Q37)
— they were **not corrected**. A few single words could not be read clearly in the
scans and are flagged in the question text/notes rather than guessed. The Kharidar
pretest's "KEY [A]" is only the paper code; no answer key is printed on any of its
8 scanned pages or the blog page, so none of its 50 questions are in the scored bank
and no answers were invented for it.

## 14. Old Papers page (2026-10-26) — `data/papers.json`, 17 entries, 3 transcribed (133 questions)

Every URL below was **opened and read on 2026-10-26** (text fetch); no URL was guessed.
All papers are scanned images/PDFs on the source site — nothing is hosted in this repo.
`pdf_url` is now set for the three transcribed 2083 first papers (direct PDF URLs read
by the live-browser pass, above); it stays null on the other 14 entries, whose PDFs sit
behind download buttons the text fetch cannot resolve. Transcribed questions tag their
`source` with the paper name + date (e.g. "Previous Year — NaSu First Paper 2083-01-20");
`practicePaper()` in `app.js` matches on paper-name keyword + date, since Kharidar
First and Koshi share the date 2083-01-26.

| # | Paper | Source (opened 2026-10-26) |
|---|---|---|
| 14.1 | NaSu First Paper 2083-01-20 — 50 MCQ, 100 marks, 45 min, pass 45 | https://www.bidhyamandir.com/nayab-subba-nasu-first-paper-exam-2083-01-20-with-answers-pdf/ |
| 14.2 | Kharidar pretest 2083/06/04, Key A — 100 marks, 45 min, pass 45, 8 scanned images | https://blog.educatenepal.com/2026/09/lok-sewapsc-pre-qualifying-exam-pretest.html |
| 14.3 | Kharidar First Paper 2083-01-26 — 50 MCQ, 100 marks, 45 min, pass 45; full 50-answer key in page text | https://www.bidhyamandir.com/kharidar-first-paper-exam-2083-01-26-with-answers-pdf/ |
| 14.4 | Koshi Province 4th Level First Paper 2083-01-26 — 50 MCQ, 100 marks, 45 min, pass 45 | https://www.bidhyamandir.com/koshi-province-4th-level-first-paper-2083-01-26-with-answers/ |
| 14.5 | NaSu 2nd Paper old questions 2082-83 — exam 2083/03/14, 100 marks, pass 40, 2 hrs 30 min | https://www.loksewasathi.com/nayab-subba-nasu-2nd-paper-old-questions-2082-83/ |
| 14.6 | NaSu old-question collection PDF (~1 MB; 2nd & 3rd papers + Revenue, MoFA, Law) | https://loksewaaspirants.com/nayab-subba-old-question-collection-pdf/ |
| 14.7 | DotNepal PSC Question Collection archive, page 4 of 8 (2073–2075 papers) | https://dotnepal.com/category/psc-question-collection/page/4/ |
| 14.8 | NaSu Foreign Affairs 2074 | https://dotnepal.com/lok-sewa-aayog-nasu-questions-2074-foreign-affairs-questions/ |
| 14.9 | NaSu Foreign Affairs 2075 | https://dotnepal.com/lok-sewa-aayog-questions-2075-loksewa-pararastra-na-su-questions/ |
| 14.10 | NaSu 2075 | https://dotnepal.com/nayab-subba-questions-2075-loksewa-questions/ |
| 14.11 | Nepal Police Inspector 2073 (Janapad) | https://dotnepal.com/nepal-police-exam-question-nepal-police-inspector-questions-2073/ |
| 14.12 | APF Sipahi 2074 | https://dotnepal.com/nepal-armed-police-force-sipahi-questions-2074-apf-sipahi-questions/ |
| 14.13 | District Judge 2nd Paper 2075 (Criminal Law & Procedure; exam 2075-12-10–14) | https://dotnepal.com/district-judge-question-2075-district-judge-second-paper-criminal-law-criminal-procedural-law/ |
| 14.14 | Under Secretary, Justice Service / Govt Attorney 2074 (exam 2074-11-30) | https://dotnepal.com/under-secretary-questions-2074-psc-justice-service-government-attorney/ |
| 14.15 | NaSu First Paper 2082-01-20 — 50 MCQ, 100 marks, 45 min, pass 45. **Date flag:** overview says 2082-01-20 but the paper-image caption on the same page reads 2083/01/20 — year unverified, recorded as stated in the overview. | https://www.loksewasathi.com/nayab-subba-nasu-first-paper-exam-2082-01-20-with-answers-pdf/ |
| 14.16 | TSC Lower Secondary (NiMaVi) First Paper 2082-02-17 — 50×2=100, 60 min, pass 50, Key D (key sheet "Updating Soon" on the page) | https://www.loksewasathi.com/lower-secondary-level-first-paper-question-2082nimavi-first-paper-2082/ |
| 14.17 | Sangathit Sanstha pre-qualifying paper 2082 Kartik 15 — 50 MCQ, 100 marks, 45 min, pass 45; full key in page text | https://www.loksewasathi.com/pre-qualifying-question-paper-2082-with-answer-key/ |

BS→AD dates in `papers.json` were converted with the `nepali-datetime` library and
cross-checked: 2083-01-20 → 2026-05-03 and 2083-01-26 → 2026-05-09 match the conversions
already recorded in §10.

## 15. Notices page (2026-10-26) — `data/notices.json`, 10 entries, checked 2026-10-26

Researched live on 2026-10-26. **Rule applied throughout: no deadline, post count, fee or
apply link is shown unless a source reported it.** Unverified items have
`close_date: null`, `status: "unverified"` and the on-page label "Check official site —
dates not verified on 2026-10-26". BS→AD conversions use `nepali-datetime` and were
cross-checked against AD dates stated in the sources.

| # | Notice | Status / deadline | Source (checked 2026-10-26) |
|---|---|---|---|
| 15.1 | PSC Under Secretary & Health 9th Level, Notice 582/2083-84 — 159 posts, fee NPR 2000, closes 2026-11-03 | open | https://brightcareernepal.com/lok-sewa-vacancy-2083/ (secondary; PSC homepage https://psc.gov.np/ confirms the advertisement is listed; fee + portal corroborated by https://www.collegenp.com/vacancy/psc-undersecretary-ninth-level-vacancy-2083) |
| 15.2 | Nepal Police ASI 211 + Office Assistant 123 (334 posts), Advt 01–04 (083/84), closes 2026-10-27; ASI applies online via ORMS at https://careers.nepalpolice.gov.np (verified 2026-10-26 from Nepal Police career pages; Office Assistant applies in person) | closing-soon | https://www.collegenp.com/vacancy/nepal-police-vacancy-for-asi-and-office-assistant-posts-2083 (dates/posts corroborated by https://www.shivapaswan.com.np/nepal-police-vacancy-2083-asi-and-office-assistant-334-posts.html and https://english.onlinekhabar.com/nepal-police-opens-recruitment-for-334-positions.html; one source gave a conflicting 06/23–07/20 window — the 06/12–07/10 window is used, as three sources agree) |
| 15.3 | Lumbini PPSC Level 8 Health Service, Notice 85/083-84 — fee NPR 1000, closes 2026-11-05; post count not stated | open | https://www.collegenp.com/vacancy/lumbini-lok-sewa-aayog-level-8-health-service-vacancy-2083 |
| 15.4 | Gandaki PPSC 9th & 8th Level, Notice 129/2083-84 — 39 posts reported, closes 2026-10-27 | closing-soon | https://www.educatenepal.com/vacancies/detail/vacancy-notice-from-province-lok-sewa-aayog-gandaki-province (39-post figure from Loksewa Pathsala's vacancy listing, https://loksewapathsala.com/ — verify against the notice) |
| 15.5 | TSC Lower Secondary (NiMaVi) Teacher 2082-83 — 678 posts, closed 2026-05-06 | closed | https://www.collegenp.com/vacancy/tsc-lower-secondary-nimavi-teacher-vacancy-2082 |
| 15.6 | TSC Secondary (MaVi) Teacher 2082 — 449 posts, closed 2026-02-15 | closed | https://exammate.barala.com.np/2026/01/tsc-ma-vi-vaccancy-2082-tsc-bigyapan.html |
| 15.7 | NRB contract posts 2083 — 34 posts, closed 2026-09-08 | closed | https://www.examsanjal.com/nepal-rastra-bank-driver-vacancy-notice-exam-interview-date/ |
| 15.8 | RBB vacancy 2083 — 138 posts, closed 2026-07-23 | closed | https://www.educatenepal.com/vacancies/detail/vacancy-notice-from-rastriya-banijya-bank |
| 15.9 | TSC Teaching Licence 2082/83 — reported open; deadline/fee/posts not verified | unverified | https://www.rram.com.np/2025/08/tsc-mabi-teacher-license-application.html |
| 15.10 | Bagmati Province PSC vacancy 2083-84 — details not verified | unverified | https://www.educatenepal.com/vacancies/detail/vacancy-notice-from-province-lok-sewa-aayog-bagmati-province |

Official "where to check" links shown on the Notices page: psc.gov.np,
psconline1.psc.gov.np, tsc.gov.np, online.tsc.gov.np, nrb.org.np,
onlineppsc.gandaki.gov.np, ppsconline.lumbini.gov.np. No live APF, Nepal Army, NHPC,
NMC, NNC or NPC vacancy notice could be verified on 2026-10-26 — re-check those bodies
on the next notices refresh; do not add them from memory.

## 16. Round 5 expansion (2026-10-26) — 2,259 new questions, 6 new files

All questions are original, written from syllabus topics and verified facts — no
question bank from another prep site or book was copied. Generated arithmetic/IQ
items were computed from rules (percentages, ratios, series, work/time, speed,
number theory) and checked against the existing bank; 5 cross-file duplicates
found and removed before writing. Bilingual (EN/NE) 100%.

### 16.1 Nepal 2025–2026 current affairs (verified by web search 2026-10-26)

| Fact | Source |
|---|---|
| Gen Z protests after the government banned 26 social media platforms; erupted 8–9 September 2025 | economictimes.indiatimes.com; dailypioneer.com; whro.org / NPR 2025-09-20 |
| K. P. Sharma Oli resigned 9 September 2025 | thehindu.com; indianexpress.com |
| Sushila Karki (former Chief Justice, first woman CJ) sworn in as interim Prime Minister 12 September 2025; appointed by President Ram Chandra Poudel, who dissolved the House the same day | thehindu.com; english.ratopati.com; risingnepaldaily.com |
| House election 5 March 2026; ~18.9 million eligible voters; ~60% turnout; 3,406 FPTP + 3,135 PR candidates | en.wikipedia.org/wiki/House_of_Representatives_(Nepal); english.nepalnews.com |
| Rastriya Swatantra Party won 182/275 seats, led by Balendra "Balen" Shah; Nepali Congress 89 → 38; CPN-UML 78 → 25; inaugural session 2 April 2026 | spotlightnepal.com/2026/10/20/when-popularity-replaces-rules/; testbook.com |
| Pro-monarchist clash in Kathmandu 28 March 2025, 2 civilians killed incl. a photojournalist | thehindu.com |
| First woman Attorney General (2025 interim government): Sabita Bhandari | english.ratopati.com |

Death toll of the September 2025 protests is reported differently by different
sources (>70 / at least 77) — no question states a precise toll.

### 16.2 Other facts used in round 5

Constitution of Nepal 2015 (35 parts, 308 articles, 9 schedules; 31 fundamental
rights, Articles 16–46); 2021 census (population 29,164,578; Bagmati 6,116,866;
Kathmandu district 2,041,587; literacy 76.2%; growth 0.92%); Nobel Prizes 2025
(Peace: María Corina Machado; Literature: László Krasznahorkai; Physics: Clarke,
Devoret, Martinis; Chemistry: Kitagawa, Robson, Yaghi; Medicine: Brunkow,
Ramsdell, Sakaguchi; Economics: Mokyr, Aghion, Howitt); FIFA World Cup 2026
(USA/Canada/Mexico, 48 teams); Nepal electricity export to Bangladesh began
November 2024; Upper Tamakoshi 456 MW; load shedding ended May 2018; 16th
Periodic Plan 2024/25–2028/29; NEPSE established 1993; Nepal Rastra Bank
established 26 April 1956; VAT 13%; NHPC/NAMC/BAMS syllabus topics; FDI tooth
notation; Ayurvedic texts (Brihat Trayi), doshas, Panchakarma; Bar Council Act
2050; Muluki Codes 2074 in force 17 August 2018; CSIT/IOE entrance patterns;
Nepal Telecom / NTA history (Telecom Act 2053, GSM 1999, 3G 2007, 4G LTE
January 2017, NepalSat-1 18 April 2019). These were written from general
knowledge and the fact-checks already recorded in earlier sections of this file;
any date-sensitive claim that could not be confirmed was dropped.

## 17. Round 6b expansion (2026-10-26) — 1,580 new questions, 3 new files

Files: `data/questions/expansion-r6b-licence-entrance.json` (741),
`data/questions/expansion-r6b-language.json` (487),
`data/questions/expansion-r6b-banking-health.json` (352).
All 100% bilingual (EN/NE). Answer positions balanced (no letter above 28%
in any file). Deduplication: every candidate was checked against the existing
bank (exact match) and near-duplicates (word-set Jaccard > 0.85) — 393
candidates dropped as exact/near duplicates of the existing bank before
writing. All questions are original, written from syllabus topics and
verified facts — no question bank from another prep site or book was copied.

### 17.1 Facts used in round 6b

Banking & finance: Nepal Rastra Bank established 26 April 1956; first
Governor Himalaya Shumsher J. B. Rana; NRB Act 2058; Bank and Financial
Institution Act 2073 (BAFIA); Nepal Bank Ltd 1937 (first commercial bank);
Rastriya Banijya Bank 1966; Agricultural Development Bank 1968; NPR pegged
1.60 NPR = 1 INR; 1 rupee = 100 paisa; fiscal year begins Shrawan 1; budget
presented Jestha 15; Nepal joined IMF 6 September 1961 and ADB 1966;
Credit Information Bureau 1989; SEBON and NEPSE both established 1993;
NEPSE index base 100; deposit insurance limit Rs 500,000 per depositor per
bank (Deposit and Credit Guarantee Fund); cheque bounce punishable under the
Banking Offence and Punishment Act 2064; commercial banks Class 'A',
development banks 'B', finance companies 'C', microfinance 'D'; VAT 13%;
16th Periodic Plan 2024/25–2028/29; first periodic plan 1956 (2013 BS);
Upper Tamakoshi 456 MW; hydropower potential ~83,000 MW; Kolkata main port
for third-country trade. No current interest rates, exchange rates or bank
counts were stated — rates and counts change frequently and were avoided.

Medicine/pharmacy: standard antidotes (atropine + pralidoxime for
organophosphate, flumazenil for benzodiazepine, naloxone for opioid,
protamine for heparin, vitamin K for warfarin, N-acetylcysteine for
paracetamol, ethanol/fomepizole for methanol, desferrioxamine for iron,
EDTA/succimer for lead, hydroxocobalamin for cyanide, Fab antibodies for
digoxin); tumour markers (AFP liver, PSA prostate, CA-125 ovarian, CEA
colorectal); Widal (typhoid), VDRL (syphilis), Mantoux (TB), Ziehl–Neelsen
(acid-fast bacilli); standard TB treatment 6 months; MDT 12 months for
multibacillary leprosy; normal values (Hb men 13–17, women 12–15 g/dL;
WBC 4,000–11,000/µL; platelets 150,000–400,000/µL; fasting sugar 70–100
mg/dL; creatinine 0.6–1.2 mg/dL; bilirubin 0.3–1.2 mg/dL; adult pulse
60–100/min; newborn pulse 120–160/min, respiratory rate 40–60/min;
foetal heart rate 110–160/min); APGAR at 1 and 5 minutes; Depo-Provera 3
months, implant 3–5 years, copper IUCD 10–12 years; vitamin A 6 months–5
years every 6 months; Nepal EPI began 1979; sources of drugs (morphine —
opium poppy; quinine — cinchona bark; digoxin — Digitalis; atropine —
belladonna; aspirin — willow bark/salicin; artemisinin — Artemisia annua).

Dentistry/optometry/ayurveda: FDI two-digit tooth numbering; Angle's
Class I/II/III molar relationships; normal visual acuity 6/6; myopia —
concave lens, hypermetropia — convex lens, astigmatism — cylindrical lens;
cataract leading cause of blindness in Nepal; glaucoma commonest cause of
irreversible blindness; normal intraocular pressure 10–21 mmHg; three
doshas (Vata, Pitta, Kapha); Panchamahabhuta; Panchakarma five therapies;
Charaka Samhita (Charaka), Sushruta Samhita (Sushruta); seven dhatus
beginning with Rasa.

Law: Muluki Civil Code and Muluki Criminal Code 2074, both in force 17
August 2018 (2075 BS); murder punishable by life imprisonment; right to
justice Article 20, right to information Article 27, right to privacy
Article 28 of the Constitution of Nepal 2015; 7 High Courts; burden of
proof on the prosecution in criminal cases; civil standard — balance of
probabilities.

Nepali literature: Devkota — Mahakavi, born Dilli Bazaar, Kathmandu;
Bhanubhakta — Adikavi, born Chundi Ramgha, Tanahun; Lekhnath Paudyal —
Kavi Shiromani, born Arghau Archale, Kaski, author of Tarun Tapasi,
Pinjadako Suga, Rituvichar; Balkrishna Sama — Mukunda Indira; Parijat —
Shirishko Phool, real name Bishnu Kumari Waiba; Bhupi Sherchan — Ghumne
Mechmathi Andho Manche; Siddhicharan Shrestha — Yugkavi; Madhav Ghimire —
Rashtrakavi; Madan Puraskar founded 2012 BS, first winner Satya Mohan
Joshi (Hamro Lok Sanskriti); first Nepali newspaper Gorkhapatra 1958 BS;
first Nepali novel Bir Charitra by Girish Ballabh Joshi; Motiram Bhatta —
Jhyaure chhanda; Nepali alphabet 46 letters (12 vowels, 33 consonants,
1 ayogavaha). English vocabulary, idioms, phrasal verbs and comprehension
passages are original wording; passages on the Himalayas, remittance,
honeybees, libraries, monsoon, leadership, rhinos, tea, the internet and
water use were written for this batch.

## 18. Round 6a + Round 7 expansion (2026-10-26) — 2,451 new questions net, 5 new files

Round 6a files: `data/questions/expansion-r6a-thin-exams.json` (535),
`data/questions/expansion-r6a-hard.json` (561),
`data/questions/expansion-r6a-current.json` (437) — 1,533 total. Thin-exam
coverage (police/army/NRB/engineering/health tags that were under 300),
hard science/maths/IQ/law/banking questions, and 2025–2026 current affairs
(Gen Z protests, interim government, 2026 House election — same verified
items as §16.1). Round 7 files: `data/questions/expansion-r7a-licence.json`
(500) and `data/questions/expansion-r7a-technical.json` (418 net — 500
written, 82 removed as duplicate stems of older bank questions under the
F08 rule, newer copy deleted, older original kept). All 100% bilingual
(EN/NE). All questions original, written from syllabus topics and verified
facts — no question bank from another prep site or book was copied. Topic
"Health" used by the round-6a/7 writers was normalised to the existing
"Health/Technical basics" so no stray topic appears in the app.

### 18.1 Facts used in rounds 6a + 7

NHPC licence (r7a-licence): haematology normals (Hb men 13.5–17.5 g/dL);
eye anatomy (lateral rectus abducts, supplied by abducens VI), refraction
(myopia most common refractive error; cylindrical lens corrects
astigmatism; Jaeger chart for near vision; Snellen for distance);
cataract treated by surgical lens removal; blepharitis = eyelid-margin
inflammation; dental (32 permanent teeth, 20 deciduous; first permanent
molar erupts first; enamel hardest tissue; Streptococcus mutans and
caries; fluoride remineralises enamel; white-spot lesion earliest caries
sign; gingivitis vs periodontitis; calculus removed by scaling; dry
socket commonest post-extraction complication); ayurveda (three doshas,
Panchamahabhuta, Panchakarma, Charaka/Sushruta Samhitas, seven dhatus
from Rasa; "Ayurveda" = science of life); midwifery/nursing normals as
in §17.1.

Technical (r7a-technical): surveying (purpose — measure and map the
earth's surface; back bearing differs from fore bearing by 180°);
concrete (Ordinary Portland Cement initial setting time 30 minutes;
slump test measures workability of fresh concrete; isolated footing for
a single column); average speed = distance ÷ time; standard engineering
drawing, physics, chemistry, biology and computer/ICT syllabus facts for
Sub-Engineer / Computer Operator / CSIT / IOE entrance. No current
rates, counts or syllabus figures that change yearly were stated.

### 18.2 Fun-fact check (FF-070, 2026-10-26)

"Nepal has not yet won an Olympic medal" was challenged on the grounds
that Palesha Goverdhan won bronze at Paris 2024 — verified still TRUE
and left unchanged: her medal was at the **Paralympic** Games, a separate
event from the Olympic Games. Nepal still has no medal at the Olympic
Games (Summer or Winter). Sources: Kathmandu Post, 2024-08-31
("Nepal has never won a medal at the Summer Games in its 60-year long
Olympic history"); Wikipedia, "Nepal Olympic Committee" ("Nepal had not
secured an official medal in either event — until … Palesha Goverdhan …
at the Paris 2024 Paralympic Games"). Note for a future edit: Nepali
media loosely call her bronze "Nepal's first Olympic medal", so the
fact's Olympic-vs-Paralympic wording may still confuse readers.

## 19. Historical events (2026-11-09) — `data/historical-events.json`, 95 entries

Compiled 2026-11-09 by web research (search + page text; no app code touched).
Every date verified against at least 2 reputable sources; where sources
disagreed the exact date was excluded (see `scripts/historical-events-notes.md`
§5 for the full excluded list with conflicting dates). BS day (`day_bs`) set
only when a source explicitly gave the BS month/day; `year_bs` set when the BS
year was documented or is deterministic from a known AD month.

Counts: nepal-history 35, constitution 13, nepal-institutions 17,
international 16, world-history 14. Confidence: 54 high, 41 medium.

Sources relied on most: Wikipedia history/constitution/institution articles
(cross-checked per entry); Nepal News diplomatic timeline (UN, treaties,
SAARC, peacekeeping); Nepali Times / Rising Nepal Daily / The Himalayan Times
/ Online Khabar; official treaty texts via FAO and the Government of India
(Mahakali Treaty); NRB official history PDF; Tribhuvan University official
site; Colombo Plan official member list; Britannica / Encyclopedia.com.

Excluded for disagreement (examples): Kathmandu conquered 25 vs 26 vs
29 Sep 1768; Gorkhapatra first issue 6 vs 7 May 1901; Radio Nepal 1 vs
2 Apr 1951; Durbar High School 1853 vs 1854 vs 1883 vs 1884 (excluded
entirely); Nepal joined WTO 23 vs 24 Apr 2004; Civil Service Act 6 vs
7 Sep 1956; Nepal joined BIMSTEC Feb 2004 vs 2003. Previously logged
conflicts NOT reused: constitution vote count 538 vs 507 (§10.8) and NRB
first banknotes 19 Sep 1959 vs 19 Feb 1960 (§10.9).

Still unverified (candidates for a future pass): first census (1911), first
five-year plan (1956), Nepal Academy, NHRC, first president elected
(21 July 2008), Rastriya Banijya Bank founding (23 Jan 1966), Bir Hospital
founding (1890?).
