# PDF Extract Dedupe Report — 2026-10-27

**Inputs:** `data/pdf-extract-raw.json` (10,000 questions) vs the current bank
`data/questions/*.json` (51,530 questions, incl. 133 Previous Year 2083).
**Decisions file:** `data/pdf-dedupe-decisions-2026-10-27.json` (10,000 decisions, one per PDF question).
**Scripts:** `scripts/pdf-dedupe-2026-10-27.py` (bank-side; unchanged, verified against the real
extract schema: `pdf_num` → `PDF-0001…`, `pdf_answer` → `answer`) + a within-PDF v2 pass
(scratch, `/tmp/pdf-within-pass-v2.py`; method documented below).

**Note on the stale file:** the invalid `/tmp/pdf-dedupe-decisions.json` from the earlier worker's
wrong-schema run was deleted before this run and never used. The script was re-run fresh on the
real data (bank 51,530, PDF 10,000).

## Headline result

| Outcome | Count |
|---|---|
| **Keep (integrate)** | **7,547** |
| **Drop — duplicate of an earlier PDF question (dup-pdf-exact)** | 2,450 |
| **Drop — near-duplicate of a bank question (dup-near)** | 1 |
| **Drop — same fact as a bank question (dup-fact, human-confirmed)** | 2 |
| **Total dropped** | **2,453 (24.5%)** |
| Total PDF questions | 10,000 |

No PDF question matched a Previous Year 2083 bank question (`py_match` = 0 everywhere) —
the PY-2083 bank copy was never at risk, and no bank file was modified.
No unresolved human-review items remain: every flagged decision was hand-reviewed.

## Why the duplicate rate is 24.5% but the bank overlap is ~0

The PDF is built as **plain question + two wrapper variants of the same question**:

- plain: `Under the Constitution of Nepal 2072, which subject is governed by Part 1 …?`
- `[PSC Model Set Verification — …] Which of the following options is the verified answer to: <same question>`
- `[Exam Paper Analysis — …] Identify the ONLY factually correct statement/value regarding '<same question>':`

7,550 plain + 1,228 PSC-wrapper + 1,222 Exam-wrapper = 10,000. After stripping the wrappers,
1,230 question groups have >1 member (1,222 triples + 8 pairs) = **2,452 extra copies**.
2,450 of them agree on option set + correct answer and are dropped as `dup-pdf-exact`;
the other 2 are false groupings (see Corrections) and are kept.

Against the **bank**, the PDF is almost entirely fresh: only **3** of 10,000 questions duplicate
bank content (1 near + 2 same-fact). This was independently validated (see Spot-checks).

## Status breakdown with examples

### keep — 7,547
Integrate. Example (PDF-0001): "Under the Constitution of Nepal 2072, which subject is
governed by Part 1 (Articles 1–9)?" — no bank question shares its stem (best bank Jaccard
in the spot-check sample was ≤ 0.50).

### dup-pdf-exact — 2,450 (drop)
Wrapper variant of an earlier PDF question: identical question after wrapper-strip, same
option set (up to extraction spacing noise, e.g. `February 16– 21` vs `February 16–21`),
same correct answer. First occurrence is kept; later copies dropped.
- PDF-0416 → PDF-0001: Exam-wrapper of "…Part 1 (Articles 1–9)?", correct "Preliminary (प्रारम्भिक)".
- PDF-2082 → PDF-1802: PSC-wrapper of the Raute-community question, correct "Raute".
- PDF-8087 → PDF-7864: PSC-wrapper of the four-quantum-numbers question, correct
  "Four Quantum Numbers (n, l, m, s) & Pauli's Exclusion Principle".

### dup-near — 1 (drop, human-confirmed)
- **PDF-0837 → bank FOR6-051** (`expansion-r5-foreign-telecom.json`, Jaccard 0.80):
  PDF "On which calendar date is 'Human Rights Day' officially observed?" (December 10)
  vs bank "Human Rights Day is observed on which date?" (10 December). Same question
  reworded, same answer. **Drop.**

### dup-fact — 2 (drop, human-confirmed)
Both items in this status were hand-reviewed (only 2 exist, so the "sample ≥ 50" target
does not apply — the population is 2, and both were reviewed).
- **PDF-4807 → bank R7B-373** (`expansion-r7b-core-hard.json`, content-Jaccard 0.714):
  PDF "One-Word Substitution: 'A person who speaks many languages fluently'" (Polyglot)
  vs bank "Choose the one word for: A person who speaks many languages." (Polyglot).
  Same fact, same answer, 3 of 4 options shared. **Drop.**
- **PDF-5115 → bank R6B-L-222** (`expansion-r6b-language.json`, content-Jaccard 0.529):
  PDF "'सरकारले गरिबलाई राहत बाँड्यो' वाक्यमा 'गरिबलाई' कुन कारक हो?" (सम्प्रदान कारक)
  vs bank "'गरिबलाई दान दिनु' वाक्यमा 'गरिबलाई' कुन कारक हो?" (सम्प्रदान कारक).
  Same grammar fact, different example sentence, same answer. **Drop.**

### dup-exact / dup-options / dup-exact-key-conflict / dup-near-key-conflict — 0
No PDF question shares an exact normalised stem with any bank question (verified
independently across all 10,000), and no key conflicts were found against the bank.

## Per-topic duplicate rates

Nearly all duplicates are within-PDF wrapper copies, so the rate tracks how much of each
topic the PDF author wrapped. Four topics have no wrappers at all (0% duplicates).

| Topic | Total | Keep | dup-pdf-exact | dup-near | dup-fact | Dup % |
|---|---:|---:|---:|---:|---:|---:|
| Health/Technical basics | 700 | 459 | 241 | 0 | 0 | 34.4% |
| IQ & Reasoning | 500 | 431 | 69 | 0 | 0 | 13.8% |
| Maths & Numerical | 500 | 364 | 136 | 0 | 0 | 27.2% |
| Constitution & Governance | 450 | 414 | 36 | 0 | 0 | 8.0% |
| Current Affairs | 450 | 389 | 60 | 1 | 0 | 13.6% |
| Nepal Geography | 450 | 354 | 96 | 0 | 0 | 21.3% |
| Nepal History | 450 | 345 | 105 | 0 | 0 | 23.3% |
| Economy & Development | 450 | 306 | 144 | 0 | 0 | 32.0% |
| Office Management & Public Service | 450 | 330 | 120 | 0 | 0 | 26.7% |
| Banking & Finance | 450 | 294 | 156 | 0 | 0 | 34.7% |
| Computer & ICT | 450 | 450 | 0 | 0 | 0 | 0.0% |
| Education & Pedagogy | 450 | 270 | 180 | 0 | 0 | 40.0% |
| English | 450 | 289 | 160 | 0 | 1 | 35.8% |
| Nepali Language | 450 | 280 | 169 | 0 | 1 | 37.8% |
| Science & Tech | 450 | 305 | 145 | 0 | 0 | 32.2% |
| Culture & Society | 400 | 279 | 121 | 0 | 0 | 30.2% |
| Mathematics | 350 | 274 | 76 | 0 | 0 | 21.7% |
| Law | 350 | 230 | 120 | 0 | 0 | 34.3% |
| Biology | 300 | 210 | 90 | 0 | 0 | 30.0% |
| Chemistry | 300 | 210 | 90 | 0 | 0 | 30.0% |
| Physics | 300 | 300 | 0 | 0 | 0 | 0.0% |
| Foreign Service & Diplomacy | 300 | 200 | 100 | 0 | 0 | 33.3% |
| Economy | 200 | 200 | 0 | 0 | 0 | 0.0% |
| IQ | 200 | 164 | 36 | 0 | 0 | 18.0% |
| Engineering Drawing | 200 | 200 | 0 | 0 | 0 | 0.0% |
| **Total** | **10,000** | **7,547** | **2,450** | **1** | **2** | **24.5%** |

## Spot-checks (hand verification)

**Bank-side script validation (is the near-zero bank overlap real?)**
- Independent brute-force check over **all 10,000** PDF questions: **0 exact normalised-stem
  matches** against the 51,530-question bank.
- Independent brute-force Jaccard on a random sample of **150** PDF questions vs the full bank:
  **0** with Jaccard ≥ 0.8. The script's low duplicate count is genuine, not a miss.
- **10 keep decisions** re-verified by brute force (PDF-5309, 2473, 6473, 0792, 1188, 8784,
  1544, 5996, 9553, 0952): best bank Jaccard 0.16–0.50, all well below threshold. All keeps correct.
  (PDF-0792 at 0.50 is a same-template "On which calendar date is X observed?" drill — different
  day, correctly kept.)

**All 4 bank-side non-keep decisions hand-reviewed in full** (see examples above):
3 true positives dropped; 1 false positive corrected (PDF-5975, below).

**Within-PDF v1 pass rejected after hand review:** the first within-PDF pass (raw-stem
near/options, no wrapper stripping) flagged 198 items. Hand-reviewing 17 sampled pairs showed
only 12 were true duplicates; **186 were template drills** — different questions sharing a long
template (district/province/belt, SAARC summit number, alphanumeric-coding word, समास compound)
with a coincidentally equal correct answer. The v1 output was discarded and the pass was redone
as v2 (wrapper-strip first). The v1 false positives were caused by three guard weaknesses,
documented under Limitations.

**Within-PDF v2 verification:**
- **10 dup-pdf-exact pairs hand-checked** (random sample): all 10 are true wrapper-variant
  duplicates — identical inner question, same correct answer, same option set up to reordering /
  spacing noise (e.g. PDF-8069 vs PDF-7855 differ only in "H- atom" vs "H-atom").
- **All 2,450 dup-pdf-exact pairs verified programmatically** under a matra-preserving
  normaliser (see Limitations): 0 mismatches — every pair has an identical stripped question.
- The 190 exact-dup pairs whose option text differs raw were sampled (6 pairs): all differences
  are extraction spacing noise only ("Milan- Cortina" vs "Milan-Cortina", "hunting- gathering"
  vs "hunting-gathering"); correct answers match.
- **Near pass on stripped stems found 0** further duplicates — there are no genuine rewordings
  inside the PDF beyond the wrapper triples.

## False-positive corrections made (3)

1. **PDF-5975 — `dup-near` → `keep`.** Script matched it to bank IQ2-161 (Jaccard 0.846).
   PDF: "A is the brother of B. B is the wife of C. D is the mother of A. How is D related to C?"
   (Mother-in-law). Bank: "A is the mother of B. B is the brother of C. How is A related to C?"
   (Mother). Different relation puzzles, different answers. The script's loose-answer subset
   rule equated "Mother" with "Mother-in-law". Corrected in the decisions file
   (`corrected_from: dup-near`, `human_review` recorded).
2. **PDF-5319 — `dup-pdf-key-conflict` → `keep`.** Grouped with PDF-5293 only because the
   shared normaliser strips Devanagari vowel signs: 'परि' vs 'परा' उपसर्ग collide. The
   questions ask about different prefixes with different correct answers. Not duplicates.
3. **PDF-5357 — `dup-pdf-key-conflict` → `keep`.** Same artefact: 'ली' vs 'ले' तद्धित प्रत्यय
   collide after matra-stripping; different suffixes, different correct answers. Not duplicates.

## Limitations found (for future dedupe work — not blocking this integration)

1. **Normaliser strips Devanagari vowel signs.** `normalise()` uses `[^\w\s]`, and Devanagari
   matras (ि, ा, ी, े, …) are Unicode category Mn, not `\w` — so 'परि'/'परा' and 'ली'/'ले'
   normalise identically. It caused the 2 false groupings above (both caught, because their
   answers differ). All 2,450 accepted exact dups were re-verified under a matra-preserving
   normaliser with 0 mismatches, so this run's results stand — but the shared normaliser should
   be fixed before any future Nepali-heavy dedupe.
2. **`loose_same_correct` subset rule over-matches single-token answers** ("Mother" ⊆
   "Mother-in-law" counted as same). It caused the PDF-5975 false positive. A single-token
   subset should not count as the same answer.
3. **`strip_paren` in `loose_same_correct` erases distinguishing info** — "Koshi Province
   (Hill belt)" vs "Koshi Province (Mountain belt)" compared equal after paren-stripping.
   This contributed to the v1 within-PDF false positives (district drills). The v2 pass
   dropped that branch.
4. **`number_occurrences` misses ordinals** — "10th"/"6th" are not recognised as numbers
   (regex requires a digit-only token), so the numbers guard was blind to SAARC-summit drills.
   The v2 pass used an ordinal-aware check.

## For the integration worker

- Integrate the **7,547 `keep`** decisions only.
- Drop: `dup-pdf-exact` (2,450 — later wrapper copies; keep the first occurrence, referenced
  in `within_pdf_match_id`), `dup-near` (PDF-0837), `dup-fact` (PDF-4807, PDF-5115 — both
  human-verdict `drop` in their `human_review` field).
- Decisions carry `pdf_id`, `pdf_index`, `status`, `match_bank_id` / `match_bank_file`
  (bank matches), `within_pdf_match_id` / `within_pdf_match_index` (PDF matches),
  `human_review` (6 records) and `corrected_from` (3 records). `meta.final_counts` and
  `meta.by_status` summarise the final state.
- Answer-key verification is out of scope for this report (separate worker).
- `data/questions/*` and `assets/js/app.js` were not modified.
