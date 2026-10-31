# PDF Extraction Report — 10,000 New Questions (2026-10-27)

Source PDF: `~/workspace/user/files/loksewa-10000-new-questions-answer-key_0_3hfx.pdf`
(15,510,459 bytes; title "Lok Sewa Prep Nepal — 10,000 New Exam Questions & Master Answer Key (2082/83 BS)";
919 pages, A4; created 2026-10-26; Chrome/Skia print-to-PDF — real text layer, **not scanned**, no OCR needed.)

Parser: `scripts/pdf-extract-2026-10-27.py` (runs `pdftotext -layout`, re-runnable).
Output: `data/pdf-extract-raw.json` (11,792,026 bytes; JSON array, 10,000 objects).

## Result

| Check | Outcome |
|---|---|
| Questions parsed | **10,000 / 10,000 claimed** (pdf_num 1–10000, sequential, none missing) |
| Parse failures | **0** |
| Master answer key entries | 10,000 unique, Q1–Q10000 complete |
| Answers recorded | Exactly as printed in the master key; nothing "fixed" |
| Explanations | **None exist in the PDF** — every `explanation` is `null` (no "explanation" string anywhere in the document) |
| Spot check | 20/20 random questions re-verified: stem + all 4 options found verbatim in raw text (seed 20261027; pdf_nums 421, 454, 669, 818, 1285, 1657, 2121, 2507, 3074, 3124, 3725, 3816, 6691, 6881, 6905, 7096, 8069, 8106, 9082, 9806) |
| Answer distribution (as printed) | A 2,468 · B 2,505 · C 2,501 · D 2,526 |

## Per-topic counts (all match the PDF's own overview table exactly)

| # | Topic (as printed) | Range | Parsed |
|---|---|---|---|
| 1 | Constitution & Governance | Q1–Q450 | 450 |
| 2 | Current Affairs | Q451–Q900 | 450 |
| 3 | Nepal Geography | Q901–Q1350 | 450 |
| 4 | Nepal History | Q1351–Q1800 | 450 |
| 5 | Culture & Society | Q1801–Q2200 | 400 |
| 6 | Economy & Development | Q2201–Q2650 | 450 |
| 7 | Economy | Q2651–Q2850 | 200 |
| 8 | Office Management & Public Service | Q2851–Q3300 | 450 |
| 9 | Banking & Finance | Q3301–Q3750 | 450 |
| 10 | Computer & ICT | Q3751–Q4200 | 450 |
| 11 | Education & Pedagogy | Q4201–Q4650 | 450 |
| 12 | English | Q4651–Q5100 | 450 |
| 13 | Nepali Language | Q5101–Q5550 | 450 |
| 14 | IQ & Reasoning | Q5551–Q6050 | 500 |
| 15 | IQ | Q6051–Q6250 | 200 |
| 16 | Maths & Numerical | Q6251–Q6750 | 500 |
| 17 | Mathematics | Q6751–Q7100 | 350 |
| 18 | Science & Tech | Q7101–Q7550 | 450 |
| 19 | Biology | Q7551–Q7850 | 300 |
| 20 | Chemistry | Q7851–Q8150 | 300 |
| 21 | Physics | Q8151–Q8450 | 300 |
| 22 | Law | Q8451–Q8800 | 350 |
| 23 | Foreign Service & Diplomacy | Q8801–Q9100 | 300 |
| 24 | Engineering Drawing | Q9101–Q9300 | 200 |
| 25 | Health/Technical basics | Q9301–Q10000 | 700 |
| | **Total** | | **10,000** |

## Output schema (per question)

`pdf_num` (1–10000) · `topic` (section name as printed) · `question` (stem text) ·
`options` (array of 4 strings, A–D as printed) · `pdf_answer` (0–3 index as printed in the master key) ·
`explanation` (always `null` — none in PDF) · `raw_text` (full cleaned block, whitespace-normalised, for audit).

## Formatting quirks found (all handled by the parser)

1. **Options are inline, bullet-separated:** `(A) … • (B) … • (C) … • (D) …` — every block has exactly 3 `•` separators.
2. **Look-alike markers inside content:** 94 blocks contain `(A)`/`(B)`/`(C)` inside option or stem text
   (e.g. `Tr(A)` in maths Q6885–Q6904, `Carbon (C)` in Q7331, `Boron (B)` quoted in the stem of Q7371).
   The parser splits on the full `(A) … • (B) … • (C) … • (D) …` bullet chain, never on bare `(A)`, so these never mis-split.
3. **Paragraph break before (D):** 15 questions (Q1601, Q1719, Q2141, Q2871, Q3710, Q3946, Q4000, Q4054,
   Q4658, Q6332, Q7290, Q7822, Q8514, Q8855, Q9015) have blank lines between the last `•` and `(D)`;
   handled with `\s+` around bullets.
4. **Repeating page headers/footers** (`LOK SEWA PREP NEPAL • …` / `Zero-Duplicate Verified Expansion Set … Page N of 919`)
   can land mid-question at page breaks; stripped line-wise before parsing.
5. **Section header lines** sit inside the preceding question's raw block; stripped line-wise (with line-join
   for headers that wrap, e.g. Section 8 "Office Management & Public Service").
6. **"Verified answer to:" / "Exam Paper Analysis" questions** (~999 of the former) quote an earlier question's
   *stem only* — the (A)–(D) that follow are that question's own real options, not a nested set.
7. **Master answer key is a grid at the end** (after the heading "Master Answer Key & Verified Correct Responses"),
   entries `Q<n>(<letter>)`; the key section is split off before question parsing so it cannot contaminate Q10000.
8. No explanations, no images/diagrams with questions, no True/False or 5-option questions — every question has exactly 4 options.

## Notes for downstream workers

- `pdf_answer` is the PDF's own printed key, preserved verbatim — verification/dedupe workers must treat it as
  "as printed", not as ground truth.
- The PDF's front matter claims "0% duplicate overlap" and "verified" answers; those claims were **not** checked here.
- Existing bank (`data/questions/*`, `app.js`) was not touched; no generator module was imported.
