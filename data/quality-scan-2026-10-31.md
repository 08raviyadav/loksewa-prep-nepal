# Question Quality Scan — 2026-10-31

Bank: 131 files, **64,713 questions** (`data/questions/*.json`). Scope: quality only — answer indexes NOT touched.

## Fixed in this scan (mechanical text fixes, 35 files changed)

| Fix | Count | Notes |
|---|---|---|
| `सहि` → `सही` (misspelling) | 3,216 | explanation_ne (3,182) + question_ne (33) |
| `कु न` → `कुन` (split-word typo, PDF batch Nepali) | 466 | |
| `The correct answer is …` → `सही उत्तर …` (explanation_ne starting in English) | 279 | Panini-grammar batch PDF-5101+ |
| Zero-width space U+200B stripped | 78 | invisible artifacts |
| `के का लागि` → `केका लागि` | 69 | MT spacing garble |
| `उम्मेद्वार` → `उम्मेदवार` | 57 | |
| Arabic `गरिबीको نظام` → `गरिबीको अन्त्य` (MT contamination) | 18 | SDG "No Poverty" batch, expansion-pdf-02.json |
| `पक्ष ले ` → `पक्षले ` | 6 | |
| `के का रूपमा` → `केका रूपमा` | 5 | |
| Urdu bidi `پڑ` → `पढाइ` | 2 | PDF-5111 question + question_ne |
| PDF-5173 garbled stem fragment `(रातारात (र...)` removed | 2 | question + question_ne |
| PDF-5355 `''कार' प्रत्यय'` quote artifact | 2 | question + question_ne |
| Hand-rewritten garbled explanations | 6 | HARD2-427 exn, PDF-4832 exn, PDF-5209 exn, NEP-049 ex+exn, R10-IQ5-0548 exn |

Total string-level fixes: **4,206**. Backup of pre-fix bank: `/tmp/qscan/questions-backup` (ephemeral).

## Scan findings (after fixes)

- **Structural: 0** — no missing fields, no out-of-range answer indexes, all options lists valid.
- **Real duplicate options: 0** (136 raw hits were normalization artifacts — `Ctrl+Shift+<` vs `+>` etc.).
- **Conflicting answer keys across duplicate stems: 0.**
- **Explanation/answer text mismatches in tautological set: 0** (explanations name the keyed option consistently).
- **Encoding artifacts (U+FFFD / mojibake): 0** bank-wide.

## Open items (not fixed — needs human/curated pass)

1. **Tautological explanations: 7,546** — every one is `The correct answer is {option}.` / `सही उत्तर {option} हो।` with zero added information. All in the PDF batch (`expansion-pdf-01`…`15` × 500, `expansion-pdf-16` × 46). Not safely auto-enrichable: a real explanation needs per-item knowledge. Recommend a curated enrichment pass (or per-topic templates) before calling the PDF batch "explained".
2. **Nested-quote cosmetics: ~978** — e.g. `'Known as 'Everest's Daughter''`. Readable, but sloppy. Needs a careful regex/manual pass (risky to bulk-fix).
3. **Missing terminal punctuation: ~808 stems** — e.g. `Which is the odd one out? 45, 42, 49, 56` (no trailing `?`). Cosmetic only.
4. **One-word tautological explanation_ne: ~8+** in expansion-current-hard.json (e.g. `२०२५।`, `हंगेरी।`) — same class as item 1.
5. **Near-duplicate drill stems across files: 91 groups** (e.g. `What is 25 x 3` in drills + maths files, punctuation variants) — by design for practice repetition; answers consistent. No action needed unless dedupe policy changes.
6. **Mixed Latin numerals in Nepali explanations** (e.g. `= 10 मिटर।`) — cosmetic inconsistency; Devanagari numerals dominate.
7. **Split-word artifacts in PDF batch** (MT/PDF-extraction class): e.g. `कृ ति` (=कृति), `पङ् कज` (=पङ्कज), `एकै क` (=एकैक). The systematic `कु न` subclass (466×) was fixed; remaining instances need a careful conjunct-aware pass — a blanket regex would corrupt legitimate word-final halants (`विद्युत्`, `पढ्नुहोस्`).

## Nepali spot-check (2026-10-31)

- **Sample: 260 questions** (2 per file, stratified across all 131 files), hand-read question_ne + explanation_ne.
- **Real Devanagari Nepali: 260/260** — zero English-passthrough, zero machine-garbled beyond the items below.
- **Defect rate: ~2%** — 5 garbled items found in sample (HARD2-427 q+exn, HARD2-483 q, PDF-4832 exn, PDF-5209 exn), all fixed above. By-design keeps observed and correct: tested English vocabulary/grammar stays Latin (`'advocate' को नेपाली अर्थ…`), formulas/codes (`V = IR`, `HCF`), acronyms (`SDG`, `NHPC`), proper names (`Sunita`, `BRICS`).
- Whole-bank pattern sweeps (not just the sample) found and fixed the systematic issues: `सहि`, `कु न`, Arabic/Urdu contamination, zero-width chars.

## Ambiguity check

- Two-plausible-options / no-correct-option: **0 confirmed programmatically**. Structural scan clean; duplicate-option check clean; cross-file key conflicts: 0. (True ambiguity needs per-item subject review — flagged as a future human pass, not a defect found.)
- Wrong-key suspects from explanation/answer mismatch scan: **0**.

## Tests

- `node scripts/test-questions.js` → **PASS** (run after fixes).
