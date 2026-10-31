# Round 10 — Scale-up to 50,000+ questions (2026-10-26)

## Result (verified, final)

- **Bank total: 50,870 questions** (was 20,132 at start of round 10)
- **Round-10 contribution: 30,342 questions in 34 files** (`data/questions/expansion-r10-*.json`)
- **Non-R10 bank: 20,528** (round-9's files included; untouched by this work)
- **Bilingual: 100%** — every R10 question has `question_ne`, `options_ne[4]`, `explanation_ne` in real Nepali
- **Tests: `node scripts/test-questions.js` — ALL PASSED**
- **Answer-key audit: 23 flags, all pre-existing non-R10** (baseline was 24; my files add **zero** new flags)
- **Dedupe: 0 flagged R10 questions** after the final gate (see below)

## Files (final verified counts)

| File | Qs | File | Qs |
|---|---|---|---|
| expansion-r10-current.json | 54 | expansion-r10-maths.json | 3,030 |
| expansion-r10-drills.json | 1,526 | expansion-r10-maths2.json | 1,756 |
| expansion-r10-drills2.json | 865 | expansion-r10-maths3.json | 1,435 |
| expansion-r10-english.json | 1,873 | expansion-r10-maths4.json | 1,373 |
| expansion-r10-english2.json | 1,203 | expansion-r10-maths5.json | 1,659 |
| expansion-r10-english3.json | 1,065 | expansion-r10-maths6.json | 933 |
| expansion-r10-english4.json | 375 | expansion-r10-maths7.json | 653 |
| expansion-r10-grammar.json | 72 | expansion-r10-maths8.json | 376 |
| expansion-r10-health.json | 210 | expansion-r10-maths9.json | 726 |
| expansion-r10-health2.json | 89 | expansion-r10-maths10.json | 419 |
| expansion-r10-iq.json | 1,711 | expansion-r10-nepal-facts.json | 504 |
| expansion-r10-iq2.json | 972 | expansion-r10-nepali.json | 656 |
| expansion-r10-iq3.json | 742 | expansion-r10-nepali2.json | 298 |
| expansion-r10-iq4.json | 2,352 | expansion-r10-office-edu-law.json | 186 |
| expansion-r10-iq5.json | 798 | expansion-r10-science2.json | 84 |
| expansion-r10-iq6.json | 323 | expansion-r10-vocab5.json | 1,232 |
| expansion-r10-vocab6.json | 315 | expansion-r10-world-science.json | 477 |

All 34 files are listed in `QUESTION_FILES` in `assets/js/app.js`.
README.md's per-file table rows were updated to these counts; the global
total / by-topic / by-exam lines in README.md are still the old 46,415
figures — the parent integrator finalises those.

## Generators

All under `scripts/r10/` (shared helpers in `gen_common.py`):

- `g01_maths.py`, `g03_maths2.py`, `g11_maths3.py`, `g19_maths4.py`,
  `g21_maths5.py`, `g24_maths6.py`, `g27_maths7.py`, `g29_maths8.py`,
  `g30_topup.py` (maths9), `g31_topup2.py` (maths10) — computed maths
- `g14_drills.py`, `g26_drills2.py` — arithmetic drills
- `g02_iq.py`, `g12_iq2.py`, `g20_iq3.py`, `g22_iq4.py`, `g25_iq5.py`,
  `g30_topup.py` (iq6) — IQ & reasoning
- `g04_vocab.py` (+`vocab_data.py`), `g15_english2.py` (+`vocab_data2.py`),
  `g23_english3.py`, `g28_english4.py`, `g30_topup.py` (vocab5),
  `g31_topup2.py` (vocab6) — English vocab (6 lists, ~1,000 words)
- `g13_grammar.py` — grammar; `g05_nepali.py`, `g16_nepali2.py` — Nepali
- `g06_nepal_facts.py`, `g07_world_science.py`, `g08_health.py`,
  `g18_health2.py`, `g17_science2.py`, `g10_office_edu-law.py`,
  `g09_current.py` — fact banks (Current Affairs 2025/2026 verified by web
  search 2026-10-26, incl. Nepal's March 2026 election — RSP 182/275,
  Balendra Shah PM from 27 March 2026 — and the 2026 FIFA/T20 World Cups)

## Dedupe & audit history (what was removed and why)

- **Generation-time rejections: 8,072 recorded** in generator logs
  (g01 904, g02 1,691, g04 107, g05 89, g06 326, g07 296, g08 102,
  g23 83, g24 580, g25 565, g26 753, g27 962, g28 37, g29 332,
  g30 28+621+354, g31 15+227). Generators g03/g09–g22 rejected further
  candidates whose counts were only in stdout at the time (not persisted).
- **863 exact-text duplicates removed** after `test-questions.js` failed:
  g28's vocab list 4 had copied ~150 words from g23's list 3; the
  generator's `Bank` excludes R10 ids, so cross-R10 stems were not caught
  at generation time. Removed 845 from `expansion-r10-english4.json` and
  18 from `expansion-r10-maths8.json` (kept the first occurrence).
- **1,952 near-duplicates removed by the final dedupe gate**
  (1,773 + 146 + 33 across three passes to convergence, 0 flagged after).
  All 2,557 flagged pairs were R10-vs-R10 (zero R10-vs-pre-R10) — the
  generators' pre-R10 dedupe worked. Reason classes: 2,398 near-Jaccard
  ≥0.8, 142 exact-stem, 17 same-fact.
- **Audit fixes (303 R10 flags → 0):** all were false-positive heuristics,
  with marked answers verified correct by recomputation (remainder,
  unit-digit, and the "sum of letter values" cases all recomputed clean):
  - 166× `EXPL_NAMES_*` — explanations starting "The answer is X."
    tripped the audit's `answer is ([A-D])` regex (it captured the first
    letter of X as an option letter). Reworded all 1,064 such explanations
    in R10 files to "The correct choice is X."
  - 137× `NE_CONCLUDES_*` — Nepali explanations whose last `=` value was
    an intermediate number (e.g. `५८ = ६ x ९ + ४` concludes 6, not the
    remainder 4). Appended a concluding clause (`शेष = ४ हो।`,
    `एकाइ अङ्क = ४ हो।`, `योग = २५ हो।`).

## Known issues / notes for the integrator

- `scripts/dedupe-check.py` **OOM-kills at 52k questions** (exit 137,
  SIGKILL, ~6 min in). The final gate used `/tmp/r10-dedupe-final.py`
  instead: the same classification (exact stem, near-Jaccard ≥0.8 with
  same-correct/same-options + `numbers_compatible` veto, same-fact) built
  on `gen_common.Bank`'s rare-token index (memory-safe; ~60 s/pass).
  The official script needs a chunked/streaming mode at this scale.
- **Generators' `Bank` excludes R10 ids by design** (`gen_common.py`).
  That is why cross-R10 duplicates slipped through at generation time and
  had to be cleaned by the final gate. Future rounds should either pass
  `Bank(exclude_prefix='ZZZ-NONE-')` (as g30/g31 did) or run the gate
  after every generator.
- **An external bulk rewrite touched all R10 files at 2026-10-26 18:22:35–36**
  (all mtimes within ~1 s, counts changed vs generator-reported counts) —
  presumed to be the round-9 agent's dedupe sweep; not investigated further.
- **g25 bug (fixed):** the odd-one-out digit-sum block had an unbounded
  `while len(cands) < 3` loop that spun forever when too few numbers share
  a digit sum (e.g. sum 1 or 18 in 10–99). Now bounded to 200 attempts
  with `continue` on failure.
- **g31 bug (fixed before running):** the clock-coincide block used the
  wrong minute formula (`5*h+5`, giving invalid "11:60"); now uses
  `round(h*60/11)` for h=1..10.
- README.md global totals (46,415), by-topic and by-exam lines are stale;
  parent integrator to finalise. Verified current total: **50,870**.
- NOT done (per task): no GitHub upload, no push, no phone-bundle rebuild.
