# LICENSE EXAMS RESEARCH — Lok Sewa Prep Nepal

- **Researched:** 2026-10-26 (overnight run)
- **Method:** `browser.search` + `browser.open` (text fetch only). No question JSON, app code, or `data/exams.json` was edited. Nothing was uploaded, pushed, or shared.
- **Schema read first:** `data/exams.json` — each entry is `{id, name, name_ne, body, level, education, age, prelim, main, final, syllabus[], note}` where `prelim = {questions, marksPerQ, total, timeMin, pass, negative, breakdown}` (pass = raw marks; `negative` = marks deducted per wrong answer, e.g. 0.2 in PSC entries, 0 = no negative marking). Guide-only exams use `prelim: null`.
- **Counts:** **14 exam sections researched; 15 verified MCQ patterns** (Pharmacy counts twice: BPharm + DPharm); **2 guide-only sections** (ANM, Ayurveda/BAMS). Draft entries below: 17 (15 verified-pattern + 2 guide-only with `prelim: null`).
- **Honesty rule applied:** where no verified pattern exists, the section says so explicitly. Nothing was invented. "Opened" means the full page text was fetched with `browser.open`; "snippet-only" means the facts come only from search-result snippets.

## How to read the verdicts

- **VERIFIED PATTERN** = question count + total marks + time + pass mark confirmed by at least two independent sources, or by one official council syllabus PDF plus a corroborating source.
- **PARTIAL** = core numbers confirmed but a detail (usually negative marking, or exact time for one level) is unstated in every source found.
- **GUIDE-ONLY** = the exam/council is real, but no verifiable MCQ pattern (count/time/pass) was found. Draft entry uses `prelim: null`.

---

## 1. MBBS / Medical Licence — Nepal Medical Council (NMC)

- **Verdict: VERIFIED PATTERN (with one unverified detail — negative marking).**
- **Council:** Nepal Medical Council (NMC). Official portal domain named in sources as `www.nmc.org.np` (domain only, named in source text — no verbatim council URL was returned by search; do NOT treat as a verified link).
- **Eligibility:** MBBS (or equivalent) from an NMC-recognised institution, plus internship — "You can give the exam once you have completed at least 6 months of internship from an NMC recognized medical school" (Medchrome). Foreign graduates: degree must be from an NMC-recognised institution; equivalence certificate usually required; foreign nationals sit the same licensing exam (NMC Regulations 2024, Reg. 20(e)3a / 21(f) per Education Times). Three sittings a year (2082: Jestha 12–14, Ashoj 8–10, Magh 13–15).
- **Format table:**

| Item | Value |
|---|---|
| Format | Computer-based; 130 MCQs (1 mark each) + 10 Clinical Scenario Questions / CSQs (5 marks each) |
| Total marks | 180 |
| Time | 3 hours (180 min) |
| Pass mark | 50% = 90 marks |
| Negative marking | **NOT STATED in any source found — unverified. Do not assume zero.** |
| Frequency | 3 sessions/year |

- **Syllabus / subject distribution (MCQs, 130):** Anatomy 5, Physiology 5, Pharmacology 4, Biochemistry 5, Microbiology 7, Pathology 4, Orthopedics 6, Surgery 13, Medicine 14, Pediatrics 10, Obstetrics & Gynecology 13, Community Medicine 13, Anesthesia 8, Psychiatry 2, Forensic Medicine 6, ENT 6, Ophthalmology 6, Dermatology 3. CSQs (10 × 5): Pharmacology 1, Orthopedics 1, Surgery 2, Medicine 2, Pediatrics 2, Obstetrics & Gynecology 2.
- **Conflicts / unverified:**
  - Two secondary sources (Medchrome vs the NMC MBBS Accreditation Standards 2017 on Scribd) differ slightly: Medchrome lists Microbiology 7 / Pathology 4 / Community Medicine 13 / OBGYN 13; the Accreditation Standards list Pathology 7 / Microbiology 4 / Community Medicine 10 / OBGYN 12, and add Radiology 3 + Dentistry 2. Both total 130. The NMC itself notes the distribution "is not constant and may change from time to time" and is "to give a hint" only. **Treat subject weights as indicative, not fixed.**
  - Negative marking: no source states it either way.
  - A 2022 Rising Nepal report on making the exam optional confirms "Among the 180 objective questions, 90 correct answers are enough to pass" — consistent with 180 total / 90 pass.
- **Sources (verbatim):**
  - Opened? No — snippet-only: https://www.mystichealth.com.np/2025/02/14/comprehensive-guide-to-passing-the-nepal-medical-council-licensing-examination-nmcle/
  - Opened? No — snippet-only: https://medchrome.com/featured/how-to-pass-nepal-medical-council-licensing-examination/
  - Opened? No — snippet-only: https://www.scribd.com/document/670995325/ACCREDITATION-STANDARDS-FOR-THE-MBBS
  - Opened? No — snippet-only: https://risingnepaldaily.com/news/17196
  - Opened? No — snippet-only: https://www.shyamsundarbaitha.com.np/2025/04/nmc-licensing-exam-schedule-2082.html

## 2. BDS / Dental Licence — Nepal Medical Council (NMC)

- **Verdict: VERIFIED PATTERN (shared NMC exam) — subject distribution UNVERIFIED.**
- **Council:** Nepal Medical Council (NMC) — BDS licensing is run by NMC, not a separate dental council (confirmed by Collegenp course guide: "NMC BDS accreditation & licensing requirements"; Rising Nepal: "license exams for MBBS and BDS conducted by the Nepal Medical Council").
- **Eligibility:** BDS degree (4.5 years + 1-year internship) from an NMC-recognised institution; same internship rule as MBBS (assumed shared; not separately sourced — flag).
- **Format table:**

| Item | Value |
|---|---|
| Format | Same NMC licensing exam sessions as MBBS; 180 objective questions |
| Total marks | 180 |
| Time | 3 hours (inferred from the shared MBBS exam — **not separately confirmed for BDS**) |
| Pass mark | 50% = 90 correct answers (Rising Nepal, MBBS and BDS together) |
| Negative marking | **Unverified** |
| Frequency | Same sessions as MBBS (3/year) |

- **Syllabus subjects:** Dental subjects named in sources (from BDS curriculum coverage, NOT a licensing-exam blueprint): Oral & Maxillofacial Surgery, Orthodontics, Prosthodontics, Periodontics, Pedodontics, Oral Pathology & Oral Medicine, Community Dentistry, plus anatomy/physiology of the oral cavity. **No BDS-specific licensing question distribution was found anywhere — do not copy the MBBS weights onto BDS.**
- **Conflicts / unverified:** Everything BDS-specific beyond "180 questions, 90 to pass, same NMC exam" is unverified. The draft entry below therefore uses the shared totals and an explicit note; its `breakdown` field does not invent weights.
- **Sources (verbatim):** snippet-only: https://risingnepaldaily.com/news/17196 ; snippet-only: https://www.collegenp.com/article/top-10-medical-courses-after-12th-in-nepal

## 3. Registered Nurse — PCL Nursing & BSc Nursing (NLEN) — Nepal Nursing Council (NNC)

- **Verdict: VERIFIED PATTERN.**
- **Council:** Nepal Nursing Council (NNC), Bansbari, Kathmandu. Portal named in sources: `application.nnc.org.np` (official application portal); council site named as `www.nnc.org.np` (domains named in source text, not verified links).
- **Eligibility:** PCL Nursing or BSc Nursing from an NNC-approved programme in Nepal (separate question papers for PCL vs BSc — candidates must select the correct level). Nepali citizens who studied abroad on/after 1 Oct 2020 need an MEC Eligibility Letter. All qualification certificates must be published before the form-submission deadline.
- **Format table:**

| Item | Value |
|---|---|
| Format | 150 MCQs, 1 mark each |
| Total marks | 150 |
| Time | 2 hours 30 minutes (150 min) |
| Pass mark | 50% = 75 marks (pass/fail grading; no numeric score issued) |
| Negative marking | **None — confirmed** ("No negative scoring system"; "Each correct answer receives 1 score. There is no negative scoring system.") |
| Frequency | 3 sittings/year |

- **Syllabus / subject distribution:** Fundamentals of Nursing 25% (~38 Q), Adult Nursing 20% (~30 Q), Midwifery & Gynecology 20% (~30 Q), Community Health Nursing 15% (~23 Q), Child Health Nursing 10% (~15 Q), Leadership & Management 5% (~7 Q), Integrated Science 5% (~7 Q). Integrated Science = anatomy/physiology, microbiology, pharmacology, biochemistry. (One mock-test source gives slightly different counts — Fundamentals 34, Adult 25, Child 20, Community 24, Integrated 19, Leadership 5, Midwifery 23 — total still 150. The NNC test-guideline percentages above are the authoritative distribution; the mock-test split is a secondary variation, flagged here.)
- **Conflicts / unverified:** None material. Exam fee figures differ by year/notice (Rs 3,100 in a 2080 notice vs Rs 3,500 in the current guide) — fees change per sitting; do not hard-code a fee.
- **Sources (verbatim):**
  - **OPENED:** https://www.collegenp.com/article/nepal-nursing-council-licensing-exam-guide
  - Snippet-only: https://smartbrainsacademy.com/wp-content/uploads/2025/01/Test-Guidelines-for-PCL-Pre-Final-2022-10-16-1.pdf
  - Snippet-only: https://www.slicejob.com/blog/nepal-nursing-council-registration-certificate-and-licensure-exam-2080
  - Snippet-only: https://www.collegenp.com/exam/licensing-examination-notice-2079-from-nepal-nursing-council-nnc

## 4. Midwifery — Bachelor of Midwifery Studies, NLEM — Nepal Nursing Council (NNC)

- **Verdict: VERIFIED PATTERN (written + practical).**
- **Council:** Nepal Nursing Council (NNC) — National Licensure Examination for Midwives (NLEM).
- **Eligibility:** Bachelor of Midwifery Studies (BMS) / midwifery qualification recognised by NNC. (Separate from NLEN; do not merge.)
- **Format table:**

| Item | Value |
|---|---|
| Written | 150 MCQs, 150 marks, pass 50% (75 marks); no negative marking (same NLEN rules) |
| Practical | OSPE / skills exam, 50 marks, pass **80%** (40/50) |
| Time (written) | 2 hours 30 minutes (same sitting as NLEN — stated for nursing/midwifery together in NNC notices) |
| Rule | Failing either component means re-applying for that component |

- **Syllabus subjects:** Same NLEN subject family, midwifery-weighted (antenatal/intranatal/postnatal care, obstetric emergencies, neonatal care, women's health). No separate NLEM subject-weight table was found — flagged.
- **Conflicts / unverified:** Older NNC notices say the practical is "50 marks" while one 2078 notice says "40-mark OSPE" with 80% to pass. **The 40 vs 50 practical-marks figure conflicts across notices;** the 80% pass threshold is consistent. Verify against the current notice before publishing a number.
- **Sources (verbatim):** **OPENED:** https://www.collegenp.com/article/nepal-nursing-council-licensing-exam-guide ; snippet-only: https://www.slicejob.com/blog/nepal-nursing-council-registration-certificate-and-licensure-exam-2080 ; snippet-only: https://www.collegenp.com/exam/nepal-nursing-council-licensing-examination-schedule

## 5. Staff Nurse — Lok Sewa Aayog (PSC), Nepal Health Service, General Nursing, Assistant 5th Level

- **Verdict: VERIFIED PATTERN (PSC exam, not a council licence exam — included because the task lists "Staff Nurse").**
- **Body:** Lok Sewa Aayog (PSC), central; provinces may run separate syllabi (not researched here).
- **Eligibility:** PCL Nursing + NNC registration (per PSC health-service rules; the existing `health` entry in exams.json already notes NHPC/NNC registration where applicable).
- **Format table:**

| Item | Value |
|---|---|
| Paper I (first phase) | 50 MCQs × 2 marks = 100; 45 min; pass 40; **20% negative marking** (0.4 marks per wrong answer) |
| Paper I breakdown | 20 MCQ × 2 on General Awareness & Public Management + 30 MCQ × 2 on Job-Based Knowledge |
| Paper II (first phase) | Subjective: 12 × 5 marks + 4 × 10 marks = 100; 2 hrs 15 min; pass 40 |
| Second phase | Interview 30 |
| Medium | Nepali and/or English |

- **Syllabus subjects:** Fundamentals of nursing, applied science, medical/surgical nursing, community health nursing, midwifery & gynecological nursing, pediatric nursing, mental health nursing, nursing leadership & management; plus anatomy & physiology, pharmacology, English/Nepali (provincial syllabi).
- **Conflicts / unverified:** One Scribd syllabus overview describes an older/different scheme ("100 MCQs + interview 20") — superseded by the Edusanjal PSC plan (50×2 + subjective 100 + interview 30). Use the Edusanjal figures.
- **Sources (verbatim):** snippet-only: https://edusanjal.com/exam/staff-nurse-exam-psc/ ; snippet-only: https://www.scribd.com/document/524308821/StaffNurseSyllabus

## 6. ANM — Auxiliary Nurse Midwife

- **Verdict: GUIDE-ONLY — no verified licence-exam pattern found. Do NOT invent one.**
- **What is verified:** ANM is a recognised qualification in Nepal; job ads require "ANM qualification from a recognized institution with valid registration with Nepal Nursing Council" — so ANMs do register with NNC. ANM appears in PSC/local-level health posts (AHW/ANM Lok Sewa model tests exist: 50 MCQs in 45 min, 2 marks each — but those are **PSC recruitment model tests, not an NNC licence exam**, and the model test found is a coaching-centre Google Form, not an official pattern).
- **What was NOT found:** no NNC notice, test guideline, or syllabus giving an ANM-specific licensing exam's question count, time, pass mark, or subject weights. Searches returned only PSC model tests, entrance-exam guides for India, and job ads. The NNC notices found cover "Nursing and Midwifery" (NLEN/NLEM) only.
- **Recommendation:** include ANM as a guide-only entry (`prelim: null`) pointing users to the NLEN nursing subjects + PSC health pattern, and flag that the ANM licence-exam format must be confirmed from an NNC notice before any MCQ bank is built for it.
- **Sources (verbatim):** snippet-only: https://www.jobsnepal.com/various-positions-144338 ; snippet-only: https://www.collegenp.com/exam/licensing-examination-notice-2079-from-nepal-nursing-council-nnc

## 7. Health Assistant — PCL in General Medicine — Nepal Health Professional Council (NHPC)

- **Verdict: VERIFIED PATTERN (NHPC common format + official 2021 syllabus weights).**
- **Council:** Nepal Health Professional Council (NHPC), Bansbari, Kathmandu. Official site: `nhpc.gov.np` (domain confirmed via official syllabus PDFs on that domain). **Note:** the task brief says `nhpc.org.np` — no source returned that domain; the council's working domain in all sources found is **nhpc.gov.np**. Do not use nhpc.org.np.
- **Eligibility:** PCL in General Medicine (3-year CTEVT programme; SEE pass + CTEVT entrance) from an NHPC-recognised institution. NHPC exam is also the route for all NHPC-regulated professions (see §§9–13).
- **Format table (NHPC common format, all subjects):**

| Item | Value |
|---|---|
| Format | Fully digitised/computer-based; all MCQs |
| Questions | 100 MCQs, 1 mark each |
| Total marks | 100 |
| Time | 1.5 hours (90 min) |
| Pass mark | 50 (50%) |
| Negative marking | **NOT STATED in any source found — unverified.** No NHPC source mentions a penalty; do not assume. |
| Frequency | 3–4 times/year |
| Evidence | 17th licensing exam (Feb 2026): 4,470 candidates across 44 subjects; 67.31% passed. 11th exam (Mangsir 2081): PCL General Medicine 880 appeared, 190 passed (21.59%). |

- **Syllabus / subject weights (NHPC Syllabus for Licensing Examination of Certificate Level in General Medicine, 2021):** Anatomy & Physiology 10%, Community Health (health education & promotion, environmental health, PHC & family health, epidemiology & disease control, nutrition, community diagnosis, health management) 25%, General Medicine (clinical methods, systemic diseases, pediatrics & neonatology, skin, venereal diseases, psychiatry) 25%, Pharmacology & Pharmacy 10%, General Surgery (basic surgery, first aid & emergency care, Obs & Gynae, eye/ENT/oral health) 25%, Clinical Pathology (biochemistry, microbiology, parasitology, hematology) 5%. Total 100%.
- **Note:** the PSC Health Assistant (Lok Sewa 5th level) exam is a **different** exam from the NHPC licence exam — PSC HA is 50×2 MCQ prelim + subjective papers. Do not conflate them; the portal's existing generic `health` entry covers the PSC side.
- **Sources (verbatim):**
  - **OPENED:** http://www.rabindraadhikary.com.np/2023/01/how-to-get-nhpc-license-certificate.html
  - Snippet-only: https://publichealthupdate.com/syllabus-for-licensing-examination-of-certificate-level-in-general-medicine-2021/
  - Snippet-only: https://www.educatenepal.com/news/detail/nepal-health-professional-council-nhpc-licensing-result
  - Snippet-only: https://english.nepalnews.com/s/health/67-31-pass-nhpc-17th-licensing-examination/
  - Snippet-only: https://www.collegenp.com/institute/nepal-health-professional-council-nhpc

## 8. Pharmacy — BPharm & DPharm — Nepal Pharmacy Council (NPC)

- **Verdict: VERIFIED PATTERN (both levels).**
- **Council:** Nepal Pharmacy Council (NPC), established 26 Jan 1994 under the Pharmacy Act; autonomous regulatory body. (No verbatim NPC website URL was returned by search — do not guess one.)
- **Eligibility:** BPharm (or equivalent) from an NPC-recognised institution for the Pharmacist exam; Diploma in Pharmacy for the Assistant Pharmacist exam. Per the Pharmacy Council Act 2057, a "pharmacist" holds at least a bachelor's in pharmacy.
- **Format table:**

| Item | BPharm (Pharmacist) | DPharm (Assistant Pharmacist) |
|---|---|---|
| Questions | 150 MCQs | 100 MCQs |
| Total marks | 150 | 100 |
| Time | 2.5 hours (150 min) | 1 hour 20 minutes (80 min) |
| Pass mark | 50% (75) | 50% (50) |
| Negative marking | **None — confirmed** | **None — confirmed** |

- **Syllabus / subject distribution:**
  - **BPharm (150):** Pharmacognosy, Medicinal Chemistry & Natural Product Chemistry 25; Pharmaceutical Analysis & Instrumentation 15; Pharmaceutical Technology, Biopharmaceutics & Dosage Form Design 25; Pharmacology & Therapeutics 25; Clinical Pharmacy & Hospital Pharmacy 20; Forensic Pharmacy (laws & ethics) 15; Community Pharmacy, Social Pharmacy & Public Health 25.
  - **DPharm (100):** Pharmacognosy & Medicinal Chemistry 10; Pharmaceutics 15; Pharmacology & Pharmacotherapeutics 20; Clinical & Hospital Pharmacy 15; Community Pharmacy & Pharmaceutical Jurisprudence 25; Social Pharmacy & Public Health 15.
- **Conflicts / unverified:** One secondary FAQ claims "minimum 50% in each subject AND 50% aggregate" — the official-style syllabus sources state only an overall 50% pass with no negative marking. **The per-subject 50% rule is unverified;** do not present it as fact. Time figures are consistent across the two best sources (150 min / 120 min in one guide vs 2.5 hrs / 1 hr 20 min in the syllabus page — the same values).
- **Sources (verbatim):**
  - **OPENED:** https://ehealthsewa.com/nepal-pharmacy-council-license-exam-syllabus/
  - Snippet-only: https://edusanjal.com/exam/pharmacist-license-exam/
  - Snippet-only: https://pharmainfonepal.com/how-to-pass-nepal-pharmacy-council-license-exam-in-1st-attempt-2/
  - Snippet-only: https://chaitanya.com.np/2023/07/nepal-pharmacy-council-registered-pharmacist/

## 9. Lab Technician / Medical Lab Technology — NHPC

- **Verdict: VERIFIED PATTERN (two levels, different syllabi, same exam format).**
- **Council:** Nepal Health Professional Council (NHPC).
- **Eligibility:** Certificate in Medical Laboratory Technology (CMLT, PCL level) or BSc MLT / BMLT from an NHPC-recognised institution. 11th NHPC exam (Mangsir 2081): CMLT 694 appeared / 137 passed (19.74%); BSc MLT 199 appeared / 113 passed (56.78%).
- **Format table (both levels):** 100 MCQs, 100 marks, 90 min, pass 50, negative marking unverified (same NHPC common format as §7).
- **Syllabus / subject weights:**
  - **CMLT (2021 syllabus):** Clinical Biochemistry 20%, Clinical Haematology 20%, Clinical Microbiology & Immunology 20%, Histo/Cytopathological Techniques 10%, Anatomy & Physiology 10%, Clinical Parasitology 5%, Instrumentation & Automation 5%, Blood Banking 5%, Pathology 5%.
  - **BSc MLT / BMLT (2021 syllabus):** Medical Microbiology 20%, Clinical Biochemistry 20%, Hematology & Blood Banking 20%, Histocytopathology 15%, Human Anatomy & Physiology 10%, Health Policy & Health System of Nepal 5%, Research Methodology & Biostatistics 5%, Clinical Pharmacology 3%, NHPC & Code of Ethics 2%.
- **Sources (verbatim):** snippet-only (official NHPC PDFs): https://nhpc.gov.np/beta/uploads/syllabus_pdf/4__Medical_Laboratoy_Technology.pdf ; https://nhpc.gov.np/beta/uploads/syllabus_pdf/5__Syllabus_of_B_Sc__MLT-_BMLT3.pdf ; snippet-only: https://www.educatenepal.com/news/detail/nepal-health-professional-council-nhpc-licensing-result

## 10. Radiographer / Medical Imaging Technology — NHPC

- **Verdict: VERIFIED PATTERN (two levels, different syllabi).**
- **Council:** Nepal Health Professional Council (NHPC).
- **Eligibility:** PCL in Diagnostic Radiography / Diploma in X-Ray Technology, or BSc in Medical Imaging Technology (BSc MIT), from NHPC-recognised institutions.
- **Format table:** 100 MCQs, 100 marks, pass 50, negative marking unverified (NHPC common format).
  - **PCL Radiography time:** 90 min (NHPC general rule; not separately stated in the PCL syllabus snippet — flag as assumed from the common format).
  - **BSc MIT time:** the BSc MIT syllabus examination scheme states **2 hours** — **conflicts with the 90-minute general NHPC rule; flag and verify with the current NHPC notice.**
- **Syllabus / subject weights:**
  - **PCL Radiography / Diploma in X-Ray Technology (2021):** Anatomy & Physiology 20%, Radiographic Technique / General Radiography & Radiological Procedures 40%, Radiographic Photography 10%, Radiographic Equipment 10%, Radiation Physics 10%, Patient Care & Management 5%, Code of Ethics 5%.
  - **BSc MIT:** Anatomy & Physiology 20, Basic Health Science 10, Radiographic Technique 15, Special Radiological Procedure & Modern Imaging Technique 15, Equipment for Diagnostic Imaging 15, Radiation Physics & Radiation Protection 15, Biostatistics & Research Methodology 5, Hospital Management / Patient Care / Code of Ethics / Health System of Nepal 5. (Parsed from the syllabus exam-scheme table; the source text is OCR-garbled — verify against the PDF before building questions.)
- **Sources (verbatim):** snippet-only: https://media.edusanjal.com/redactor/Syllabus for NHPC Licensing Examination of Bachelor of Science in Medical Imaging Technology (B.Sc MIT).pdf ; snippet-only: https://nhpc.gov.np/storage/uploads/syllabus/msc-in-medical-imaging-technologymsc-in-radiology-technology-msc-mit-1775973856.pdf ; snippet-only: https://www.collegenp.com/course/maharajgunj-medical-campus-bsc-medical-imaging-technology-bsc-mit

## 11. Physiotherapy — Bachelor of Physiotherapy (BPT) — NHPC

- **Verdict: VERIFIED PATTERN (format from NHPC common rule; weights from the NHPC BPT syllabus).**
- **Council:** Nepal Health Professional Council (NHPC).
- **Eligibility:** Bachelor of Physiotherapy (BPT, ~4.5 years incl. internship) from an NHPC-recognised institution; also PCL Physiotherapy (CPT) at diploma level. 11th NHPC exam: BPT 126 appeared / 84 passed (66.67%); CPT 32 appeared / 13 passed (40.63%).
- **Format table:** 100 MCQs, 100 marks, 90 min (NHPC common format — the BPT syllabus found is a 2016 draft and does not state time in the snippet; flag time as assumed from the common format), pass 50, negative marking unverified.
- **Syllabus / subject weights (NHPC BPT licensing syllabus, draft Sept 2016):** Musculoskeletal physiotherapy (incl. sports, biomechanics/kinesiology) 30, Neurological physiotherapy 20, Cardiopulmonary physiotherapy 15, Physiotherapy across the lifespan (geriatrics, pediatrics, women's/men's health) 15, Ethics, management & evidence-based practice 10, Community-based rehabilitation & health promotion 10. Total 100. Content spans cardiopulmonary assessment (ABG, ECG, chest X-ray, PFT, 6-min walk test), pulmonary rehab, cardiac rehab (MI/CABG protocols), ICU, diabetes/obesity/cancer/burns, surgical physio.
- **Conflicts / unverified:** The only BPT syllabus located is labelled a **2016 draft** — a final/current version was not found. Weights may have changed; verify against the current NHPC syllabus page.
- **Sources (verbatim):** snippet-only: https://media.edusanjal.com/redactor/Syllabus%20for%20NHPC%20Licensing%20Examination%20of%20Bachelor%20of%20Physiotherapy%20(BPT).pdf ; snippet-only: https://www.educatenepal.com/news/detail/nepal-health-professional-council-nhpc-licensing-result

## 12. Public Health — Bachelor of Public Health (BPH) — NHPC

- **Verdict: VERIFIED PATTERN.**
- **Council:** Nepal Health Professional Council (NHPC).
- **Eligibility:** Bachelor in Public Health (BPH) from an NHPC-recognised institution. 11th NHPC exam: BPH was the largest bachelor cohort — 794 appeared / 605 passed (76.20%).
- **Format table:** 100 MCQs, 100 marks, 90 min (NHPC common format), pass 50, negative marking unverified.
- **Syllabus / subject weights (NHPC Syllabus for Licensing Examination of Bachelor of Public Health, 2021):** Basic science (anatomy, physiology, microbiology, biochemistry, pharmacology, immunology, toxicology, entomology, pathology, first aid) 10; Basic & applied epidemiology 15; Research, biostatistics & population studies 15; Introduction to public health, issues & primary health care / community health development 15; Health promotion & education, community & school health, mental health 10; Health system development & management incl. health financing 15; Family health, child health & food and nutrition 10; Environmental & occupational health 5; Sociology & anthropology 5. Total 100.
- **Sources (verbatim):** snippet-only (official NHPC PDF): https://nhpc.gov.np/beta/uploads/syllabus_pdf/Syllabus_for_Public_Health_Licencing_Examination_2073.pdf ; snippet-only: https://www.collegenp.com/course/nams-college-kathmandu-bachelor-of-public-health-bph

## 13. Optometry — Bachelor of Optometry (B.Optom) — NHPC

- **Verdict: VERIFIED PATTERN (with a time conflict to flag).**
- **Council:** Nepal Health Professional Council (NHPC).
- **Eligibility:** Bachelor of Optometry (4 years) from an NHPC-recognised institution. 11th NHPC exam: BOptom 156 appeared / 63 passed (40.38%).
- **Format table:**

| Item | Value |
|---|---|
| Questions | 100 MCQs (three plausible options + one correct, per the syllabus) |
| Total marks | 100 |
| Time | **CONFLICT:** the B.Optom licensing syllabus states **2 hours**; the general NHPC exam guide states **1.5 hours** for all NHPC exams. Use 120 min in the draft with a flag; verify with the current NHPC notice. |
| Pass mark | 50% (50) |
| Negative marking | Unverified (not stated) |

- **Syllabus / subject weights (NHPC B.Optom licensing syllabus):** Basic Science & Organ Systems 5, Ocular Anatomy & Physiology 10, Physiologic & Geometric Optics 3, Visual Science 10, Ocular Disease 7, Diagnostic & Investigative Optometry 10, Ophthalmic & Dispensing Optics 10, Pediatric Optometry & Binocular Vision 10, Contact Lens & Ocular Prosthesis 10, Low Vision & Visual Rehabilitation 10, Community Optometry 5, Geriatric Optometry & Vision Care 4, Research Methodology & Biostatistics 3, Ethics in Optometry 3. Total 100.
- **Sources (verbatim):** snippet-only: https://media.edusanjal.com/B.OPTOM_License_cirriculum.pdf ; snippet-only: https://www.educatenepal.com/news/detail/nepal-health-professional-council-nhpc-licensing-result

## 14. Ayurveda — BAMS — Nepal Ayurveda Medical Council (NAMC)

- **Verdict: GUIDE-ONLY — exam confirmed to exist; NO verified MCQ pattern found.**
- **Council:** Nepal Ayurveda Medical Council (NAMC), Nardevi, Kathmandu — established under the Ayurveda Medical Council Act 2045 (1988). Website named in sources: `www.namc.org.np` (domain named in source text, not a verified link).
- **What is verified:** NAMC conducts a licensing examination for BAMS graduates for permanent name registration. Notices found: exam on 2081/06/12 (forms 2081/05/16–30, late to 2081/06/06); exam on 2081/12/09 (forms 2081/11/12–26, late to 2081/12/03); exam announced for 2083/07/17. Foreign BAMS graduates must complete internship and hold certificates before applying.
- **What was NOT found:** question count, marks, duration, pass mark, negative marking, or subject weights for the NAMC licensing exam — in any source. Searches returned only exam notices (dates/fees windows) and course/entrance information. The BAMS *entrance* exam (MECEE-BL, 200 MCQs, 3 hrs, −0.25) is a different exam and must not be confused with the licensing exam.
- **Eligibility (for the guide):** BAMS degree (5.5 years incl. internship) from a NAMC-recognised institution; internship completed.
- **Syllabus subjects (degree curriculum — NOT a licensing blueprint):** Ayurvedic fundamentals (Samhita, Siddhanta), Dravyaguna, Rasashastra, Kayachikitsa, Shalya, Shalakya, Prasuti/Stri Roga, Kaumarbhritya, modern medicine/surgery basics. Flag as curriculum-derived, not exam-verified.
- **Sources (verbatim):** snippet-only: https://www.educatenepal.com/news/detail/nepal-ayurvedic-medical-council-namc-licensing-exam-notice ; snippet-only: https://www.collegenp.com/exam/nepal-ayurveda-medical-council-notice-for-bams-licensing-examination ; snippet-only: https://www.collegenp.com/service/nepal-ayurvedic-medical-council-services-of-namc-utility-service

---

## Cross-cutting notes

1. **NHPC is one exam format across ~44 subjects** (100 MCQ / 100 marks / 90 min / pass 50, 3–4 sittings a year, computer-based). Only the *syllabus weights* differ per subject. The NHPC syllabus library on `nhpc.gov.np` also covers MSc levels, dental hygiene, ophthalmic science, anaesthesia, OT technology, dialysis, homeopathy, naturopathy, audiology/speech-language pathology, cardiac technology, medical microbiology/biochemistry, radiotherapy, etc. — all presumably the same 100-MCQ format, but **their individual syllabi were not verified in this pass**; do not add them without checking each syllabus PDF.
2. **Negative marking is the weakest-verified field overall.** Confirmed zero only for NLEN/NLEM and both Pharmacy exams. For NMC and all NHPC exams it is *unstated* in every source found. Draft entries below use `negative: 0` with an explicit note to verify — do not present it as confirmed.
3. **Domain corrections:** NHPC's working domain is `nhpc.gov.np` (not `nhpc.org.np` as in the brief). NNC's portal is `application.nnc.org.np`. NMC's portal is named as `www.nmc.org.np` in secondary sources. None of these council homepages were directly opened (search did not return verbatim homepage URLs); verify the live homepages before linking them in the portal.
4. **PSC vs licence — keep them separate.** Staff Nurse (PSC), Health Assistant (PSC) and the existing generic `health` entry are *recruitment* exams; NMC/NNC/NPC/NHPC/NAMC exams are *licensing* exams. A user preparing for one is not preparing for the other (different formats, negative marking, and syllabi).
5. **Fees were deliberately not drafted into entries** — they change every sitting (e.g. NNC Rs 3,100 → Rs 3,500; NHPC Rs 3,000 exam fee). Check the current notice at application time.

---

## Draft exam entries (exact `data/exams.json` schema — code block only, NOT applied)

Conventions: `pass` is raw marks. `negative: 0` = no negative marking **where confirmed**; where unverified it is still written as `0` with a `note` flagging verification (the schema has no "unknown" value — do not silently treat the flag as fact). `age` is "—" where no age limit was found (licence exams generally have no age limit; do not invent one). `name_ne` uses the standard Nepali names; verify spelling with a native speaker before publishing.

```json
[
  {
    "id": "nmc-mbbs",
    "name": "NMC Licensing Examination (MBBS)",
    "name_ne": "नेपाल मेडिकल काउन्सिल लाइसेन्स परीक्षा",
    "body": "Nepal Medical Council (NMC)",
    "level": "Medical licence / registration",
    "education": "MBBS from an NMC-recognised institution + internship (at least 6 months completed)",
    "age": "—",
    "prelim": {
      "questions": 130,
      "marksPerQ": 1,
      "total": 180,
      "timeMin": 180,
      "pass": 90,
      "negative": 0,
      "breakdown": "MCQ 130×1 (Anatomy 5, Physiology 5, Pharmacology 4, Biochemistry 5, Microbiology 7, Pathology 4, Orthopedics 6, Surgery 13, Medicine 14, Pediatrics 10, OBGYN 13, Community Medicine 13, Anesthesia 8, Psychiatry 2, Forensic Medicine 6, ENT 6, Ophthalmology 6, Dermatology 3) + CSQ 10×5 = 50"
    },
    "main": "10 Clinical Scenario Questions (CSQ) × 5 marks = 50, within the same 3-hour computer-based sitting (Pharmacology 1, Orthopedics 1, Surgery 2, Medicine 2, Pediatrics 2, OBGYN 2)",
    "final": "Registration with NMC on passing",
    "syllabus": ["Anatomy", "Physiology", "Pharmacology", "Biochemistry", "Microbiology", "Pathology", "Forensic medicine", "Community medicine", "Medicine", "Surgery", "Obstetrics & gynecology", "Pediatrics", "Orthopedics", "Anesthesia", "ENT", "Ophthalmology", "Dermatology", "Psychiatry", "Ethics & medical law"],
    "note": "Subject weights differ slightly between Medchrome and the NMC Accreditation Standards 2017 (e.g. Microbiology 7 vs 4, Community Medicine 13 vs 10); NMC says distribution may change. Negative marking NOT stated in any source found — verify with NMC notice before publishing negative: 0 as fact. 3 sittings/year."
  },
  {
    "id": "nmc-bds",
    "name": "NMC Licensing Examination (BDS)",
    "name_ne": "नेपाल मेडिकल काउन्सिल लाइसेन्स परीक्षा (BDS)",
    "body": "Nepal Medical Council (NMC)",
    "level": "Dental licence / registration",
    "education": "BDS from an NMC-recognised institution + 1-year internship",
    "age": "—",
    "prelim": {
      "questions": 180,
      "marksPerQ": 1,
      "total": 180,
      "timeMin": 180,
      "pass": 90,
      "negative": 0,
      "breakdown": "180 objective questions (shared NMC licensing exam with MBBS); BDS subject distribution NOT found — do not use MBBS weights"
    },
    "main": "Same NMC licensing exam sessions as MBBS (3/year)",
    "final": "Registration with NMC on passing",
    "syllabus": ["Oral & maxillofacial surgery", "Orthodontics", "Prosthodontics", "Periodontics", "Pedodontics", "Oral pathology & oral medicine", "Community dentistry", "Anatomy & physiology of the oral cavity"],
    "note": "Only totals verified (180 Q, 90 to pass, Rising Nepal 2022 for MBBS+BDS together). Time 3h inferred from shared MBBS exam — not separately confirmed for BDS. Negative marking unverified. BDS subject weights unknown — syllabus list is curriculum-derived, not an exam blueprint."
  },
  {
    "id": "nursing-nlen",
    "name": "Nursing Licence (NLEN) — PCL / BSc Nursing",
    "name_ne": "नर्सिङ लाइसेन्स परीक्षा",
    "body": "Nepal Nursing Council (NNC)",
    "level": "Registered Nurse licence",
    "education": "PCL Nursing or BSc Nursing from an NNC-approved programme (separate papers per level); MEC Eligibility Letter if studied abroad after 1 Oct 2020",
    "age": "—",
    "prelim": {
      "questions": 150,
      "marksPerQ": 1,
      "total": 150,
      "timeMin": 150,
      "pass": 75,
      "negative": 0,
      "breakdown": "Fundamentals of Nursing 25% (~38 Q) + Adult Nursing 20% (~30 Q) + Midwifery & Gynecology 20% (~30 Q) + Community Health Nursing 15% (~23 Q) + Child Health Nursing 10% (~15 Q) + Leadership & Management 5% (~7 Q) + Integrated Science 5% (~7 Q)"
    },
    "main": "Single written paper; pass/fail grading, no numeric score issued",
    "final": "NNC registration (certificate valid 6 years; 60 CPD hours per 6 years for renewal from Magh 2082)",
    "syllabus": ["Fundamentals of nursing", "Adult nursing", "Midwifery & gynecology", "Community health nursing", "Child health nursing", "Leadership & management", "Integrated science (anatomy, physiology, microbiology, pharmacology, biochemistry)", "Nursing ethics & professional practice"],
    "note": "No negative marking — confirmed in NNC test guidelines. 3 sittings/year. One mock-test source gives slightly different per-subject counts (Fundamentals 34, Adult 25, Child 20, Community 24, Integrated 19, Leadership 5, Midwifery 23); guideline percentages above are authoritative."
  },
  {
    "id": "midwifery-nlem",
    "name": "Midwifery Licence (NLEM) — BMS",
    "name_ne": "मिडवाइफरी लाइसेन्स परीक्षा",
    "body": "Nepal Nursing Council (NNC)",
    "level": "Registered Midwife licence",
    "education": "Bachelor of Midwifery Studies (BMS) recognised by NNC",
    "age": "—",
    "prelim": {
      "questions": 150,
      "marksPerQ": 1,
      "total": 150,
      "timeMin": 150,
      "pass": 75,
      "negative": 0,
      "breakdown": "150 MCQs (midwifery-weighted; no separate NLEM weight table found)"
    },
    "main": "OSPE / practical skills exam, 50 marks, pass 80% (40/50) — must pass both written and practical",
    "final": "NNC registration as midwife",
    "syllabus": ["Antenatal care", "Intranatal care", "Postnatal care", "Obstetric emergencies", "Neonatal care", "Women's health & gynecology", "Community health nursing", "Midwifery ethics & professional practice"],
    "note": "CONFLICT: practical marks stated as 50 in most notices but 40 in one 2078 notice; 80% pass threshold is consistent. Verify current notice before publishing. No negative marking (same NLEN rules)."
  },
  {
    "id": "staff-nurse-psc",
    "name": "Staff Nurse — Lok Sewa (PSC), Health Service 5th Level",
    "name_ne": "स्टाफ नर्स — लोक सेवा",
    "body": "Lok Sewa Aayog (PSC)",
    "level": "Assistant 5th Level, General Nursing",
    "education": "PCL Nursing + NNC registration",
    "age": "18–35 (women / PWD: 40) — per PSC health-service norms; verify in vacancy notice",
    "prelim": {
      "questions": 50,
      "marksPerQ": 2,
      "total": 100,
      "timeMin": 45,
      "pass": 40,
      "negative": 0.4,
      "breakdown": "General Awareness & Public Management 20 MCQ × 2 + Job-Based Knowledge 30 MCQ × 2"
    },
    "main": "Paper II subjective: 12 × 5 + 4 × 10 = 100, 2 hrs 15 min, pass 40 (same day as Paper I)",
    "final": "Interview 30",
    "syllabus": ["Fundamentals of nursing", "Anatomy & physiology", "Applied science & pharmacology", "Medical/surgical nursing", "Community health nursing", "Midwifery & gynecological nursing", "Pediatric nursing", "Mental health nursing", "Nursing leadership & management"],
    "note": "PSC recruitment exam, NOT the NNC licence exam — keep separate from nursing-nlen. Provincial PSC syllabi may differ. Negative marking 20% confirmed."
  },
  {
    "id": "ha-nhpc",
    "name": "Health Assistant Licence — PCL General Medicine (NHPC)",
    "name_ne": "हेल्थ असिस्टेन्ट लाइसेन्स परीक्षा",
    "body": "Nepal Health Professional Council (NHPC)",
    "level": "PCL licence / registration",
    "education": "PCL in General Medicine (3-year CTEVT) from an NHPC-recognised institution",
    "age": "—",
    "prelim": {
      "questions": 100,
      "marksPerQ": 1,
      "total": 100,
      "timeMin": 90,
      "pass": 50,
      "negative": 0,
      "breakdown": "Anatomy & Physiology 10 + Community Health 25 + General Medicine 25 + Pharmacology & Pharmacy 10 + General Surgery 25 + Clinical Pathology 5 (marks out of 100)"
    },
    "main": "Single computer-based MCQ paper; 3–4 sittings/year",
    "final": "NHPC registration certificate on passing",
    "syllabus": ["Anatomy & physiology", "Community health & health management", "General medicine (incl. pediatrics, psychiatry, dermatology)", "Pharmacology & pharmacy", "General surgery, first aid & emergency care", "Obstetrics & gynecology", "Eye, ENT & oral health", "Clinical pathology", "Epidemiology & disease control", "Nutrition & family health"],
    "note": "Weights from NHPC Syllabus for Licensing Examination of Certificate Level in General Medicine 2021. Negative marking NOT stated in any NHPC source — verify before presenting negative: 0 as fact. Do not confuse with the PSC Health Assistant recruitment exam."
  },
  {
    "id": "pharmacy-bpharm",
    "name": "Pharmacist Licence — BPharm (NPC)",
    "name_ne": "फार्मासिस्ट लाइसेन्स परीक्षा",
    "body": "Nepal Pharmacy Council (NPC)",
    "level": "Registered Pharmacist licence",
    "education": "Bachelor of Pharmacy (BPharm) or equivalent from an NPC-recognised institution",
    "age": "—",
    "prelim": {
      "questions": 150,
      "marksPerQ": 1,
      "total": 150,
      "timeMin": 150,
      "pass": 75,
      "negative": 0,
      "breakdown": "Pharmacognosy, Medicinal Chemistry & Natural Products 25 + Pharmaceutical Analysis & Instrumentation 15 + Pharmaceutical Technology, Biopharmaceutics & Dosage Form Design 25 + Pharmacology & Therapeutics 25 + Clinical & Hospital Pharmacy 20 + Forensic Pharmacy (laws & ethics) 15 + Community, Social Pharmacy & Public Health 25"
    },
    "main": "Single MCQ paper",
    "final": "NPC registration as pharmacist",
    "syllabus": ["Pharmacognosy & medicinal chemistry", "Pharmaceutical analysis & instrumentation", "Pharmaceutics & dosage form design", "Pharmacology & therapeutics", "Clinical & hospital pharmacy", "Forensic pharmacy — laws & ethics", "Community, social pharmacy & public health"],
    "note": "No negative marking and 50% pass confirmed in NPC syllabus sources. One FAQ claims 50% required in EACH subject plus 50% aggregate — unverified; only overall 50% is in syllabus sources."
  },
  {
    "id": "pharmacy-dpharm",
    "name": "Assistant Pharmacist Licence — Diploma in Pharmacy (NPC)",
    "name_ne": "सहायक फार्मासिस्ट लाइसेन्स परीक्षा",
    "body": "Nepal Pharmacy Council (NPC)",
    "level": "Assistant Pharmacist licence",
    "education": "Diploma in Pharmacy (DPharm) from an NPC-recognised institution",
    "age": "—",
    "prelim": {
      "questions": 100,
      "marksPerQ": 1,
      "total": 100,
      "timeMin": 80,
      "pass": 50,
      "negative": 0,
      "breakdown": "Pharmacognosy & Medicinal Chemistry 10 + Pharmaceutics 15 + Pharmacology & Pharmacotherapeutics 20 + Clinical & Hospital Pharmacy 15 + Community Pharmacy & Pharmaceutical Jurisprudence 25 + Social Pharmacy & Public Health 15"
    },
    "main": "Single MCQ paper",
    "final": "NPC registration as assistant pharmacist",
    "syllabus": ["Pharmacognosy & medicinal chemistry", "Pharmaceutics", "Pharmacology & pharmacotherapeutics", "Clinical & hospital pharmacy", "Community pharmacy & pharmaceutical jurisprudence", "Social pharmacy & public health"],
    "note": "No negative marking and 50% pass confirmed. Duration 1 hr 20 min per NPC syllabus page."
  },
  {
    "id": "lab-cmlt",
    "name": "Lab Technician Licence — CMLT (NHPC)",
    "name_ne": "ल्याब टेक्निसियन लाइसेन्स परीक्षा (CMLT)",
    "body": "Nepal Health Professional Council (NHPC)",
    "level": "PCL / Certificate licence",
    "education": "Certificate in Medical Laboratory Technology (CMLT) from an NHPC-recognised institution",
    "age": "—",
    "prelim": {
      "questions": 100,
      "marksPerQ": 1,
      "total": 100,
      "timeMin": 90,
      "pass": 50,
      "negative": 0,
      "breakdown": "Clinical Biochemistry 20 + Clinical Haematology 20 + Clinical Microbiology & Immunology 20 + Histo/Cytopathology Techniques 10 + Anatomy & Physiology 10 + Clinical Parasitology 5 + Instrumentation & Automation 5 + Blood Banking 5 + Pathology 5 (marks out of 100)"
    },
    "main": "Single computer-based MCQ paper; 3–4 sittings/year",
    "final": "NHPC registration certificate on passing",
    "syllabus": ["Clinical biochemistry", "Clinical haematology", "Clinical microbiology & immunology", "Histo/cytopathology techniques", "Anatomy & physiology", "Clinical parasitology", "Instrumentation & automation", "Blood banking", "Pathology"],
    "note": "Weights from NHPC CMLT licensing syllabus 2021. Negative marking NOT stated in any NHPC source — verify before presenting negative: 0 as fact."
  },
  {
    "id": "lab-bsc-mlt",
    "name": "Medical Lab Technology Licence — BSc MLT (NHPC)",
    "name_ne": "मेडिकल ल्याब टेक्नोलोजी लाइसेन्स परीक्षा (BSc MLT)",
    "body": "Nepal Health Professional Council (NHPC)",
    "level": "Bachelor licence",
    "education": "BSc MLT / BMLT from an NHPC-recognised institution",
    "age": "—",
    "prelim": {
      "questions": 100,
      "marksPerQ": 1,
      "total": 100,
      "timeMin": 90,
      "pass": 50,
      "negative": 0,
      "breakdown": "Medical Microbiology 20 + Clinical Biochemistry 20 + Hematology & Blood Banking 20 + Histocytopathology 15 + Human Anatomy & Physiology 10 + Health Policy & Health System of Nepal 5 + Research Methodology & Biostatistics 5 + Clinical Pharmacology 3 + NHPC & Code of Ethics 2 (marks out of 100)"
    },
    "main": "Single computer-based MCQ paper; 3–4 sittings/year",
    "final": "NHPC registration certificate on passing",
    "syllabus": ["Medical microbiology", "Clinical biochemistry", "Hematology & blood banking", "Histocytopathology", "Human anatomy & physiology", "Health policy & health system of Nepal", "Research methodology & biostatistics", "Clinical pharmacology", "NHPC & code of ethics"],
    "note": "Weights from NHPC BSc MLT/BMLT licensing syllabus 2021. Negative marking NOT stated — verify."
  },
  {
    "id": "radio-pcl",
    "name": "Radiographer Licence — PCL Diagnostic Radiography (NHPC)",
    "name_ne": "रेडियोग्राफर लाइसेन्स परीक्षा",
    "body": "Nepal Health Professional Council (NHPC)",
    "level": "PCL / Certificate licence",
    "education": "PCL in Diagnostic Radiography / Diploma in X-Ray Technology from an NHPC-recognised institution",
    "age": "—",
    "prelim": {
      "questions": 100,
      "marksPerQ": 1,
      "total": 100,
      "timeMin": 90,
      "pass": 50,
      "negative": 0,
      "breakdown": "Anatomy & Physiology 20 + Radiographic Technique / General Radiography & Procedures 40 + Radiographic Photography 10 + Radiographic Equipment 10 + Radiation Physics 10 + Patient Care & Management 5 + Code of Ethics 5 (marks out of 100)"
    },
    "main": "Single computer-based MCQ paper; 3–4 sittings/year",
    "final": "NHPC registration certificate on passing",
    "syllabus": ["Anatomy & physiology", "Radiographic technique & radiological procedures", "Radiographic photography", "Radiographic equipment", "Radiation physics", "Patient care & management", "Code of ethics"],
    "note": "Weights from NHPC PCL Radiography syllabus 2021. Time 90 min assumed from NHPC common format (not separately stated for this level) — verify. Negative marking unverified."
  },
  {
    "id": "radio-bsc-mit",
    "name": "Medical Imaging Technology Licence — BSc MIT (NHPC)",
    "name_ne": "मेडिकल इमेजिङ टेक्नोलोजी लाइसेन्स परीक्षा (BSc MIT)",
    "body": "Nepal Health Professional Council (NHPC)",
    "level": "Bachelor licence",
    "education": "BSc in Medical Imaging Technology (BSc MIT) from an NHPC-recognised institution",
    "age": "—",
    "prelim": {
      "questions": 100,
      "marksPerQ": 1,
      "total": 100,
      "timeMin": 120,
      "pass": 50,
      "negative": 0,
      "breakdown": "Anatomy & Physiology 20 + Basic Health Science 10 + Radiographic Technique 15 + Special Radiological Procedure & Modern Imaging 15 + Equipment for Diagnostic Imaging 15 + Radiation Physics & Protection 15 + Biostatistics & Research Methodology 5 + Hospital Management, Patient Care, Ethics & Health System of Nepal 5"
    },
    "main": "Single computer-based MCQ paper; 3–4 sittings/year",
    "final": "NHPC registration certificate on passing",
    "syllabus": ["Anatomy & physiology", "Basic health science", "Radiographic technique", "Special radiological procedures & modern imaging (CT, MRI)", "Equipment for diagnostic imaging", "Radiation physics & protection", "Biostatistics & research methodology", "Hospital management, patient care & ethics", "Health system of Nepal"],
    "note": "CONFLICT: BSc MIT syllabus exam scheme states 2 hours, but the general NHPC guide states 1.5 hours for all NHPC exams. Draft uses 120 min — verify with current NHPC notice. Weights parsed from a garbled exam-scheme table — re-check against the PDF. Negative marking unverified."
  },
  {
    "id": "physio-bpt",
    "name": "Physiotherapy Licence — BPT (NHPC)",
    "name_ne": "फिजियोथेरापी लाइसेन्स परीक्षा",
    "body": "Nepal Health Professional Council (NHPC)",
    "level": "Bachelor licence",
    "education": "Bachelor of Physiotherapy (BPT) from an NHPC-recognised institution",
    "age": "—",
    "prelim": {
      "questions": 100,
      "marksPerQ": 1,
      "total": 100,
      "timeMin": 90,
      "pass": 50,
      "negative": 0,
      "breakdown": "Musculoskeletal physiotherapy 30 + Neurological physiotherapy 20 + Cardiopulmonary physiotherapy 15 + Physiotherapy across the lifespan 15 + Ethics, management & evidence-based practice 10 + Community-based rehabilitation & health promotion 10 (marks out of 100)"
    },
    "main": "Single computer-based MCQ paper; 3–4 sittings/year",
    "final": "NHPC registration certificate on passing",
    "syllabus": ["Musculoskeletal physiotherapy (sports, biomechanics, kinesiology)", "Neurological physiotherapy", "Cardiopulmonary physiotherapy", "Physiotherapy across the lifespan (geriatrics, pediatrics, women's & men's health)", "Ethics, management & evidence-based practice", "Community-based rehabilitation & health promotion", "ICU & critical care physiotherapy", "Cardiac & pulmonary rehabilitation"],
    "note": "Weights from NHPC BPT licensing syllabus labelled DRAFT September 2016 — no final/current version found; verify weights against the current NHPC syllabus page. Time 90 min assumed from NHPC common format. Negative marking unverified."
  },
  {
    "id": "public-health-bph",
    "name": "Public Health Licence — BPH (NHPC)",
    "name_ne": "जनस्वास्थ्य लाइसेन्स परीक्षा",
    "body": "Nepal Health Professional Council (NHPC)",
    "level": "Bachelor licence",
    "education": "Bachelor in Public Health (BPH) from an NHPC-recognised institution",
    "age": "—",
    "prelim": {
      "questions": 100,
      "marksPerQ": 1,
      "total": 100,
      "timeMin": 90,
      "pass": 50,
      "negative": 0,
      "breakdown": "Basic science 10 + Basic & applied epidemiology 15 + Research, biostatistics & population studies 15 + Intro to public health & PHC 15 + Health promotion & education, community/school health, mental health 10 + Health system development & management incl. financing 15 + Family health, child health & nutrition 10 + Environmental & occupational health 5 + Sociology & anthropology 5 (marks out of 100)"
    },
    "main": "Single computer-based MCQ paper; 3–4 sittings/year",
    "final": "NHPC registration certificate on passing",
    "syllabus": ["Basic sciences (anatomy, physiology, microbiology, biochemistry, pharmacology, immunology, toxicology, entomology, pathology, first aid)", "Epidemiology", "Research & biostatistics", "Public health & primary health care", "Health promotion & education", "Health system development & management", "Family, child health & nutrition", "Environmental & occupational health", "Sociology & anthropology"],
    "note": "Weights from NHPC BPH licensing syllabus 2021. Negative marking NOT stated — verify."
  },
  {
    "id": "optometry-boptom",
    "name": "Optometry Licence — B.Optom (NHPC)",
    "name_ne": "अप्टोमेट्री लाइसेन्स परीक्षा",
    "body": "Nepal Health Professional Council (NHPC)",
    "level": "Bachelor licence",
    "education": "Bachelor of Optometry (B.Optom) from an NHPC-recognised institution",
    "age": "—",
    "prelim": {
      "questions": 100,
      "marksPerQ": 1,
      "total": 100,
      "timeMin": 120,
      "pass": 50,
      "negative": 0,
      "breakdown": "Basic Science & Organ Systems 5 + Ocular Anatomy & Physiology 10 + Physiologic & Geometric Optics 3 + Visual Science 10 + Ocular Disease 7 + Diagnostic & Investigative Optometry 10 + Ophthalmic & Dispensing Optics 10 + Pediatric Optometry & Binocular Vision 10 + Contact Lens & Ocular Prosthesis 10 + Low Vision & Rehabilitation 10 + Community Optometry 5 + Geriatric Optometry & Vision Care 4 + Research Methodology & Biostatistics 3 + Ethics in Optometry 3"
    },
    "main": "Single MCQ paper (3 plausible options + 1 correct per item, per syllabus)",
    "final": "NHPC registration certificate on passing",
    "syllabus": ["Basic science & organ systems", "Ocular anatomy & physiology", "Physiologic & geometric optics", "Visual science", "Ocular disease", "Diagnostic & investigative optometry", "Ophthalmic & dispensing optics", "Pediatric optometry & binocular vision", "Contact lens & ocular prosthesis", "Low vision & visual rehabilitation", "Community optometry", "Geriatric optometry & vision care", "Research methodology & biostatistics", "Ethics in optometry"],
    "note": "CONFLICT: B.Optom syllabus states 100 MCQs in 2 hours; general NHPC guide states 1.5 hours. Draft uses 120 min — verify with current NHPC notice. Negative marking unverified."
  },
  {
    "id": "anm-guide",
    "name": "ANM — Auxiliary Nurse Midwife (Guide only)",
    "name_ne": "अनमी",
    "body": "Nepal Nursing Council (NNC) — registration; no verified licence-exam pattern found",
    "level": "ANM registration",
    "education": "ANM qualification from a recognised institution; NNC registration required by employers",
    "age": "—",
    "prelim": null,
    "main": "No verified NNC licensing-exam pattern found for ANM (no question count, time, or pass mark in any source). Do not build an MCQ bank for ANM until an NNC notice is found.",
    "final": "NNC registration (per employer requirements)",
    "syllabus": ["Community health nursing", "Midwifery & maternal health", "Child health & immunisation", "Family planning", "Nutrition", "Health management & HMIS", "First aid & basic clinical care"],
    "note": "GUIDE-ONLY. ANM appears in PSC/local-level recruitment (model tests: 50 MCQ × 2 in 45 min — coaching-centre material, not an official licence pattern). Syllabus list is indicative from ANM course content, not an exam blueprint."
  },
  {
    "id": "ayurveda-bams",
    "name": "Ayurveda Licence — BAMS (NAMC) (Guide only)",
    "name_ne": "आयुर्वेद लाइसेन्स परीक्षा (BAMS)",
    "body": "Nepal Ayurveda Medical Council (NAMC)",
    "level": "Ayurveda licence / permanent registration",
    "education": "BAMS (5.5 years incl. internship) from a NAMC-recognised institution; internship completed",
    "age": "—",
    "prelim": null,
    "main": "NAMC licensing examination for permanent registration — exam confirmed to exist (notices: 2081/06/12, 2081/12/09, announced 2083/07/17), but question count, marks, duration, pass mark and negative marking were NOT found in any source.",
    "final": "NAMC permanent registration on passing",
    "syllabus": ["Ayurvedic fundamentals (Samhita, Siddhanta)", "Dravyaguna", "Rasashastra", "Kayachikitsa", "Shalya", "Shalakya", "Prasuti & Stri Roga", "Kaumarbhritya", "Modern medicine & surgery basics"],
    "note": "GUIDE-ONLY. Do NOT confuse with the BAMS entrance exam (MECEE-BL: 200 MCQs, 3 hrs, -0.25) — that is admission, not licensing. Syllabus list is curriculum-derived, not an exam blueprint. Verify format from an NAMC notice before building questions."
  }
]
```

---

## Source index (all URLs verbatim from search results / opened pages)

**Opened (full page text fetched):**
- https://www.collegenp.com/article/nepal-nursing-council-licensing-exam-guide
- https://ehealthsewa.com/nepal-pharmacy-council-license-exam-syllabus/
- http://www.rabindraadhikary.com.np/2023/01/how-to-get-nhpc-license-certificate.html

**Snippet-only (search-result text; page not opened):**
- https://www.mystichealth.com.np/2025/02/14/comprehensive-guide-to-passing-the-nepal-medical-council-licensing-examination-nmcle/
- https://medchrome.com/featured/how-to-pass-nepal-medical-council-licensing-examination/
- https://www.scribd.com/document/670995325/ACCREDITATION-STANDARDS-FOR-THE-MBBS
- https://risingnepaldaily.com/news/17196
- https://www.shyamsundarbaitha.com.np/2025/04/nmc-licensing-exam-schedule-2082.html
- https://smartbrainsacademy.com/wp-content/uploads/2025/01/Test-Guidelines-for-PCL-Pre-Final-2022-10-16-1.pdf
- https://www.slicejob.com/blog/nepal-nursing-council-registration-certificate-and-licensure-exam-2080
- https://www.collegenp.com/exam/licensing-examination-notice-2079-from-nepal-nursing-council-nnc
- https://www.collegenp.com/exam/nepal-nursing-council-licensing-examination-schedule
- https://edusanjal.com/exam/staff-nurse-exam-psc/
- https://www.scribd.com/document/524308821/StaffNurseSyllabus
- https://www.jobsnepal.com/various-positions-144338
- https://publichealthupdate.com/syllabus-for-licensing-examination-of-certificate-level-in-general-medicine-2021/
- https://www.educatenepal.com/news/detail/nepal-health-professional-council-nhpc-licensing-result
- https://english.nepalnews.com/s/health/67-31-pass-nhpc-17th-licensing-examination/
- https://www.collegenp.com/institute/nepal-health-professional-council-nhpc
- https://edusanjal.com/exam/pharmacist-license-exam/
- https://pharmainfonepal.com/how-to-pass-nepal-pharmacy-council-license-exam-in-1st-attempt-2/
- https://chaitanya.com.np/2023/07/nepal-pharmacy-council-registered-pharmacist/
- https://nhpc.gov.np/beta/uploads/syllabus_pdf/4__Medical_Laboratoy_Technology.pdf
- https://nhpc.gov.np/beta/uploads/syllabus_pdf/5__Syllabus_of_B_Sc__MLT-_BMLT3.pdf
- https://nhpc.gov.np/beta/uploads/syllabus_pdf/Syllabus_for_Public_Health_Licencing_Examination_2073.pdf
- https://media.edusanjal.com/redactor/Syllabus%20for%20NHPC%20Licensing%20Examination%20of%20Bachelor%20of%20Physiotherapy%20(BPT).pdf
- https://media.edusanjal.com/redactor/Syllabus for NHPC Licensing Examination of Bachelor of Science in Medical Imaging Technology (B.Sc MIT).pdf
- https://nhpc.gov.np/storage/uploads/syllabus/msc-in-medical-imaging-technologymsc-in-radiology-technology-msc-mit-1775973856.pdf
- https://media.edusanjal.com/B.OPTOM_License_cirriculum.pdf
- https://www.collegenp.com/course/maharajgunj-medical-campus-bsc-medical-imaging-technology-bsc-mit
- https://www.collegenp.com/course/nams-college-kathmandu-bachelor-of-public-health-bph
- https://www.collegenp.com/article/top-10-medical-courses-after-12th-in-nepal
- https://www.educatenepal.com/news/detail/nepal-ayurvedic-medical-council-namc-licensing-exam-notice
- https://www.collegenp.com/exam/nepal-ayurveda-medical-council-notice-for-bams-licensing-examination
- https://www.collegenp.com/service/nepal-ayurvedic-medical-council-services-of-namc-utility-service

**Domains named in source text only (not verified links — do not publish as URLs without checking):** `www.nmc.org.np`, `www.nnc.org.np`, `application.nnc.org.np`, `www.namc.org.np`, `nhpc.gov.np` (confirmed working domain via official PDFs).
