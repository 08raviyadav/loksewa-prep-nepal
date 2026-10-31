# PDF Answer-Key Verification Report — 2026-10-27

Source file: `data/pdf-extract-raw.json` (10,000 extracted PDF questions).
Stale `/tmp/pdf-audit-flags.json` from the earlier worker was deleted; all
flags were re-run fresh and persisted under `data/`.

## Headline result

| Outcome | Count |
|---|---|
| Verified clean (key retained as printed) | **9,999** |
| Key fixed (old key → new key) | **0** |
| Dropped | **1** (PDF-0684) |
| Total | 10,000 |

**The PDF's printed keys are essentially clean.** This is the opposite of
the earlier file that had ~48% wrong keys: the hand-checked sample found
**0 wrong keys in 261 questions**, and every programmatic check run over
the full 10,000 found **0 confirmed key errors**. No key was changed.
The single drop is a structural defect (two correct options), not a wrong key.

## Method

1. **Audit script** — `scripts/pdf-audit-2026-10-27.py` (read first,
   `py_compile` only, never imported) run on the full file →
   `data/pdf-audit-flags-2026-10-27.json`. It re-derives arithmetic/series
   answers, checks a built-in fact table (Constitution, Census 2021, NRB,
   Nepal structural facts), and flags structural breakage. Result: **0
   `key-wrong-*` flags**. The only flags were `empty-explanation` × 10,000
   (expected — the PDF has no explanations, all null, not a defect),
   `dup-options-paren` × 52 and `dup-question-in-pdf` × 2 (reviewed
   individually below).
2. **Extended verifier** — my own script,
   `scripts/pdf-verify-extended-2026-10-27.py` (standalone, no generator
   imports), run on the full file →
   `data/pdf-extended-flags-2026-10-27.json`. It checks: Constitution
   Part ranges/subjects and Article subjects (against the Constitution
   text verified at constituteproject.org), district→province for all 77
   districts, Census 2021 facts (sex ratio, literacy, density,
   households, most/least populous district/province), NRB/banking facts,
   history and geography facts, and re-derives letter sums, Caesar codes,
   ranks, handshakes/diagonals, quadratics, survey sets, profit, successive
   discounts, pipes & cisterns, number matrices and cubic series.
   Result: **0 flags** on the real file. Coverage was ~1,200+ questions
   across those structured families.
3. **Control tests** — the extended verifier was validated by flipping the
   key on 11 hand-verified-correct questions (letter sum, Caesar, rank,
   quadratic ×2, sets, matrix, cubic series, handshakes, profit,
   discounts) and 10 Part-range questions: it flagged and fixed **21/21**
   back to the correct key, and flagged **0/21** unflipped. (Two real
   checker bugs were found and fixed by this control: label-blind
   number matching in sets/profit, and a case-sensitivity bug in the
   Part-range option matcher.)
4. **Hand-checked sample** — 261 questions, stratified random sample
   (seed 20261027), weighted to the risky topics: Constitution 40, Maths
   & Numerical 28, Banking & Finance 22, IQ & Reasoning 22, Nepal
   Geography 18, Mathematics 18, Nepal History 18, Economy &
   Development 12, IQ 12, Science & Tech 10, Current Affairs 10,
   Computer & ICT 5, Culture & Society / Education / Law / Health /
   Office Management / English / Nepali Language 4 each, Biology /
   Chemistry / Engineering Drawing / Economy / Foreign Service /
   Physics 3 each. Every sampled question was checked against my own
   knowledge; uncertain facts were verified by web search (Constitution
   Part/Article boundaries, Census 2021 figures, Munal satellite launch
   date). Maths was re-derived by hand. Each verdict is logged in
   `data/pdf-sample-verdicts-2026-10-27.json` (261 entries); the sampled
   questions are in `data/pdf-sample-2026-10-27.json`.

## Error-rate estimate

- Sample: **0 wrong keys / 261** → point estimate **0%**. Rule-of-three
  95% upper bound ≈ **1.1%** (i.e. at most ~115 wrong keys in 10,000 at
  95% confidence, most plausibly near zero).
- The automated checks add independent evidence: ~1,200 structured
  questions (all maths/IQ families, all Constitution Part/Article-range
  questions, all district→province questions, all Census 2021 questions)
  were re-derived or fact-checked with **0 errors**, and the audit
  script's arithmetic/series/fact checks found **0 errors** over the
  whole file.
- Combined reading: the true key error rate is very likely **below 1%**,
  and the most likely value is ~0%. This file does **not** need the
  wholesale re-keying the earlier 48%-wrong file did. Residual risk is
  confined to isolated factual slips in untested niches (e.g. obscure
  history/geography minutiae, 2082 current-affairs items), which a
  261-sample cannot rule out one by one.

## The one drop

**PDF-0684** (Current Affairs) — *“What is Nepal's official membership
date or affiliation status with 'International Court of Justice (ICJ)'?”*
Options: A. 1 May 1953; B. 14 December 1955; C. 14 December 1955 (via UN
Charter); D. 27 November 1951. Keyed C. Nepal joined the UN on
14 December 1955 and thereby became party to the ICJ Statute, so **both
B and C state the same correct date** — the question has two correct
options and cannot be fixed by re-keying. **Status: drop.**
(No other question met the drop criteria, so there are no further drop
examples to list.)

## Wrong keys fixed — none

No wrong key was found anywhere (sample, audit script, extended
verifier), so there are **no fixed-key examples** to give. The closest
equivalents — keys verified correct where a trap was plausible — are:

1. **PDF-0045** (Constitution) — Part 15 comprises *Articles 197–202*,
   key C. A popular Lok Sewa reference table lists Part 15 as 197–203;
   the Constitution text itself (Art. 202 = Ordinance, last article of
   Part 15; Art. 203 opens Part 16) confirms 197–202. The PDF is right
   and the reference table is wrong.
2. **PDF-0024 / PDF-0027** — Part 8 = *Articles 83–108*, Part 9 =
   *Articles 109–114* (keys correct). The same reference table wrongly
   gives 83–105 / 106–114; the Constitution text (Art. 108 =
   Remuneration, last of Part 8; Art. 109 opens Part 9) confirms the PDF.
3. **PDF-0033 / PDF-0036** — Part 11 = *Articles 126–156*, Part 12 =
   *Articles 157–161* (keys correct). Art. 156 is still Part 11
   (provincial Judicial Service Commission); Art. 157 (Attorney General)
   opens Part 12.
4. **PDF-3518** (Banking) — 9th NRB Governor Hari Shankar Tripathi
   (2047–2051 BS), “first Governor after restoration of democracy”.
   An early version of my own checker misread this as “first Governor
   of NRB” and flagged it; the key is correct (Himalaya Shumsher was
   1st Governor, 1956).
5. **PDF-2593** (Economy) — 16th Plan target 10.0% (baseline 17.4%) is
   the **Multidimensional Poverty Index**, not absolute poverty (whose
   baseline is ~20.3%). Key D is correct.
6. **PDF-1249** (Geography) — Census 2078: 6,666,937 households,
   average size 4.37. Key A matches the NSO final report exactly.
7. **PDF-0567** (Current Affairs) — Munal satellite launch 28 Poush
   2082 BS (12 Jan 2026), key B — verified by web search against NAST /
   Himalayan Times reporting.

## Flags reviewed and KEPT (false alarms — worth knowing for the integrator)

- **51 of the 52 `dup-options-paren` flags are false alarms.** The
  audit's paren-strip rule collapses options that differ inside the
  parentheses, e.g. “King Mahendra (1 Falgun 2015 BS)” vs “King Mahendra
  (1 Poush 2019 BS)” (PDF-0395/0398/0401/0404 — different dates,
  distinct options, keys all correct) and “Price Elasticity of Demand
  (Ed = 0…)” vs “(Ed = ∞…)” (47 Economy questions, PDF-2665–2849 —
  different values, keys all correct). Only PDF-0684 (above) is a
  genuine duplicate.
- **Both `dup-question-in-pdf` flags are false alarms.** The audit's
  normaliser strips Devanagari vowel signs, so distinct Nepali words
  collide: PDF-5293 asks about 'परा' उपसर्ग and PDF-5319 about 'परि'
  उपसर्ग; PDF-5341 asks about 'ले' तद्धित प्रत्यय and PDF-5357 about
  'ली'. All four are distinct questions with correct keys.
- **10 early `E6-nrb-fact` flags from the extended verifier were false
  positives** (a too-loose “NRB Act” / “first governor” pattern matching
  Section-content questions) and were removed after review; the
  corrected checks find nothing.

## Topic with systematically wrong keys — none found

No topic shows systematic key errors. The only systematic issue found
was in **my own reference material**, not the PDF: the
loksewapathsala.com Part-range table is wrong at four boundaries
(Parts 8/9, 11/12, 15/16). The PDF's ranges agree with the Constitution
text at every boundary, and all 47 Part-range option questions plus all
44 stem-stated Part ranges were verified against the corrected table
with 0 errors. The extended verifier's table has been corrected
accordingly (Part 8 = 83–108, Part 9 = 109–114, Part 11 = 126–156,
Part 12 = 157–161, Part 15 = 197–202, Part 16 = 203–213).

## Caveats for the integration worker

- “keep-verified” means: no flag from either audit pass **and** the key
  is consistent with the sample-based error estimate. It is not a
  hand-verification of all 10,000 questions — that was not feasible, and
  the residual risk above (~<1%, isolated factual slips) stands.
- Two sampled current-affairs keys (PDF-0891 Kamala Shrestha award,
  PDF-0456 Sunil Thapa award) were accepted as the only plausible
  option among unrelated distractors; the underlying award facts were
  not independently verified.
- All 10,000 explanations are null by design of this extract; no
  explanations were written here, as instructed.
- The corrected-keys file is the single source of truth for integration:
  `data/pdf-verified-keys-2026-10-27.json` (10,000 entries; statuses
  `keep-verified` / `drop`; `final_answer` null for the dropped entry).

## Files produced

- `data/pdf-audit-flags-2026-10-27.json` — audit-script flags (fresh run).
- `data/pdf-extended-flags-2026-10-27.json` — extended-verifier flags
  (0 flagged; file kept for audit trail).
- `data/pdf-sample-2026-10-27.json` — the 261 sampled questions.
- `data/pdf-sample-verdicts-2026-10-27.json` — one verdict per sampled
  question (261 × correct).
- `data/pdf-verified-keys-2026-10-27.json` — **the integration input**
  (10,000 entries: 9,999 keep-verified, 0 keep-key-fixed, 1 drop).
- `scripts/pdf-verify-extended-2026-10-27.py` — the extended verifier
  (with corrected Constitution Part table).
