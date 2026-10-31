# Open-Source Checklist — Lok Sewa Prep Nepal

**Audit date:** 2026-10-26 (~22:45 NPT) · **Auditor:** Muse (readiness audit — docs, repo hygiene, privacy sweep only; no app code or question data edited)
**Counts verified at write time:** 20,132 questions · 52 question files (51 with questions + empty `community-approved.json`) · 608 fun facts · 47 exams (33 with a mock, 14 guide-only) · 17 old papers · 10 notices.

**Updated 2026-10-28 (round 11 rebuild): 64,671 questions in 131 question files (130 with questions + empty `community-approved.json`) · 608 fun facts · 47 exams · 17 old papers · 10 notices. Re-count before pushing (`python3` one-liner in §5).**
⚠️ A scale-up agent is adding questions in parallel — **re-count the bank (`python3` one-liner in §5) and re-run `node scripts/test-questions.js` immediately before pushing**, in case the totals moved after this audit.

## 1. README.md — ✅ verified, small fixes applied

- Verified as a proper open-source README: what the project is, who it is for (PSC/TSC/NRB/bank/police/army/health/engineering/licence/entrance aspirants), features (practice, mocks, Old Papers, Notices, Discussion Hub, Submit a Question, fun facts, gamification, bilingual EN/NE, dashboard, bookmarks/mistakes, exam guide, search).
- Counts verified against disk: question-bank table (51 files) sums to exactly 20,132 and every per-file count matches; 47 exams / 33 mocks / 14 guide-only verified against `data/exams.json` (`prelim` non-null = 33); 608 fun facts, 17 papers, 10 notices verified.
- Honest about demo-only parts: Gmail sign-in is demo mode (local profile only); real Google sign-in needs Supabase per `docs/BACKEND.md`. Questions are original model questions plus **133 transcribed real Previous Year questions** (NaSu/Kharidar/Koshi 2083, labelled as such in `data/questions/previous-year-2083.json`).
- Run-locally instructions verified: `python3 -m http.server 8000`, with the warning **not** to double-click `index.html` (`fetch()` is blocked from `file://`).
- **Fixed:** added the live-demo placeholder, clearly marked: "🌐 Live demo: coming after first push — enable GitHub Pages on main branch, root folder; the site will be at https://08raviyadav.github.io/loksewa-prep-nepal/" (top of README + Run-locally section).
- **Fixed:** added the single-file bundle alternative — `loksewa-prep-nepal-full.html` works by double-clicking (data embedded), rebuild with `python3 scripts/build-bundle.py`; added it + the build script to the Project structure section.
- **Fixed:** structure table now notes the bank is "51 files + `community-approved.json` (starts empty)".
- All internal links checked: `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `docs/BACKEND.md`, `PLAN.md`, `TESTING.md`, `data/SOURCES.md`, `data/TRENDS.md`, `data/SELF-AUDIT-2026-10-26.md`, `data/LICENSE-RESEARCH.md` — all resolve. README references to TESTING.md §H/§J/§K/§L/§M/§N/§O/§P all exist.

## 2. LICENSE — ✅ correct, no change needed

MIT License, **Copyright (c) 2026 Ravi Yadav** — present and correct.

## 3. Governance docs — ✅ verified, two fixes applied

| File | Status |
|---|---|
| `CONTRIBUTING.md` | ✅ Complete. Maintainer rule stated ("Ravi Yadav reviews every PR… accepts or rejects each one himself. No auto-merge, no bot approval"). Submit-a-Question flow matches the real one: EN+NE mandatory, source required, duplicate detection (token-Jaccard ≥ 0.8), spam heuristics, 5/hour limit, maintainer review, first-time submissions never go live instantly, trusted-contributor rule (3+ approved, 0 rejections = faster review, never auto-approval). **Fixed:** the valid `exam` tag list was stale (11 tags) — replaced with the full 47-tag list from `VALID_EXAMS` in `scripts/test-questions.js`, grouped by category. |
| `CODE_OF_CONDUCT.md` | ✅ Complete (Contributor Covenant 2.1, adapted). Maintainer Ravi Yadav named for enforcement; reports via GitHub issue or @08raviyadav. |
| `SECURITY.md` | ✅ Complete. States the site is static/frontend-only (no server, no analytics, `localStorage` only). Reporting via a GitHub issue titled "SECURITY: …" or via GitHub @08raviyadav — no email contact, by design (privacy rule: no personal email published). |
| `.github/PULL_REQUEST_TEMPLATE.md` | ✅ Complete (summary, change type, question checklist, tests, maintainer notes). **Fixed:** added an explicit maintainer-decision line at the top — "Ravi Yadav reviews every PR and accepts or rejects it himself — no auto-merge, no bot approval." |
| `.github/ISSUE_TEMPLATE/bug_report.md` | ✅ Complete (question ID, source for correction, repro steps, browser/device). |
| `.github/ISSUE_TEMPLATE/question-contribution.md` | ✅ Complete (topics, exams, sample schema, verification sources). |

## 4. Privacy sweep — ✅ CLEAN (after 2 removals)

Swept the **entire repo** (`.md`, `.html`, `.js`, `.json`, `.txt`) for phone numbers, email addresses, home address, `Bhairahwa`, API keys, tokens, secrets, passwords, and `config.js`.

**Found and removed:**
1. **`docs/BACKEND.md:230` — the user's real Gmail address** in the maintainer-bootstrap SQL example (value redacted here on purpose — it was his own Gmail address, known to him). Replaced with the placeholder `'you@gmail.com'` + comment "Replace with the Gmail address you sign in with". The follow-up reference (§5 step 4) was reworded from "with Ravi's Gmail" to "with your Gmail address". No backup file was created — the value is the user's own address, already known to him; nothing else in the repo referenced it.
2. **`scripts/test-v2.js:40–42` — name-based test addresses** (the maintainer's first-name + surname as Gmail/Yahoo/Outlook addresses) in Gmail-validation fixtures. Replaced with neutral fixtures (`test.user@gmail.com`, `test.user@yahoo.com`, `test.user@outlook.com`). Re-ran `node scripts/test-v2.js` → **ALL V2 CHECKS PASSED ✔**.

**Verified clean / safe:**
- No phone number anywhere (Nepali mobile patterns, `+977`, 7+-digit runs all checked; the long digit strings in `data/SOURCES.md` are psc.gov.np / Scribd source-URL IDs, not personal data).
- No `Bhairahwa`, no home/street address anywhere.
- No API keys, tokens, secrets, or real passwords anywhere. `config.example.js` contains only `YOUR-…` placeholders.
- **No `config.js` file exists in the repo**; `.gitignore` lists `config.js` (plus `node_modules/`, `.DS_Store`, `*.log`, `.vscode/`, `.idea/`). ✅
- Remaining `@` strings are all safe placeholders: `you@gmail.com` (demo placeholder in `app.js`/bundle/`BACKEND.md`), `name@example.com` (example.com, inside question content about email format), `test.user@…` / `bad@yahoo.com` (test fixtures).
- No `.git` directory exists yet — nothing has been committed or pushed from this folder (expected; see §5).

## 5. Hygiene findings

**Fixed (docs only):** the three items in §1/§3 above (demo placeholder, bundle note, tag list, PR-template maintainer line).

**Found, left as-is (do not delete without the user's word):**
- `data/funfacts-r7.json` (197 facts) — fully merged into `data/funfacts.json` (all 197 IDs present there); not loaded by `app.js` or the bundle builder. Redundant source file; harmless to keep, safe to delete later.
- `data/exams-new.json` (14 draft exam entries) — staging file from the GAP-AUDIT; its entries are now merged into `data/exams.json` (47 exams). Referenced by `data/EXAM-AUDIT.md` / `data/GAP-AUDIT.md` as the audit trail; keep for now.
- `audit-patches/` (6 JSON files) — working output of the 2026-10-26 answer-key audit (merge log + per-area patches). Unreferenced by the app; useful audit trail. Keep.
- `TESTING-OVERNIGHT.md` — snapshot test report from 2026-10-25 (1,129 questions at the time). Superseded by `TESTING.md` (§A–P, current). Kept as a historical record.
- `exam-guides/` — empty directory. Harmless; Git will not track it unless a file is added.
- `data/questions/community-approved.json` — intentionally empty (0 questions); approved community submissions land here. Not in the README per-file table (correct — it has no questions yet); now noted in the structure section.
- Stale wording (not fixed — needs the user's / scale-up agent's decision, and lives in roadmap text): README roadmap still lists "fill the thin banks… NHPC disciplines (30 → 100 tagged each)" and "human accuracy + Nepali translation audit of a sample before upload; real-browser smoke test" as open items. These are genuine open items, not errors — see §6.

**Verification runs after the fixes:** `node scripts/test-v2.js` → ALL V2 CHECKS PASSED ✔ · `node scripts/test-bundle.js` → ALL BUNDLE CHECKS PASSED ✔ · question count re-checked at write time: 20,132 (now 51,530 after round 10 — see note at top).

## 6. Exact next steps for the user (Ravi)

1. **Re-count before pushing** (a scale-up agent is still adding questions): run
   `python3 -c "import json,glob; print(sum(len(json.load(open(f))) for f in glob.glob('data/questions/*.json')))"`
   and `node scripts/test-questions.js` — both must pass and the count must match the README (20,132 at audit time). If the count moved, update the README header/table totals first.
2. **Rebuild the single-file bundle** if any question/data file changed since the last build: `python3 scripts/build-bundle.py`, then `node scripts/test-bundle.js`.
3. **Create the empty repo on GitHub** (account **08raviyadav**): github.com → New repository → name **`loksewa-prep-nepal`** → Public → **no README, no .gitignore, no licence** (all already in the folder) → Create.
4. **Push via the connector snapshot flow** (GitHub App connector cannot create repos or push directly — use the snapshot/upload flow from this folder). Do **not** push `config.js` if one exists locally — it is gitignored, but double-check `git status` shows no `config.js` before committing.
5. **Enable GitHub Pages:** repo → Settings → Pages → Build and deployment → Source: **Deploy from a branch** → Branch: **`main`** → Folder: **`/ (root)`** → Save. The site goes live at **https://08raviyadav.github.io/loksewa-prep-nepal/** — then remove the "coming after first push" wording from the README demo line.
6. **Still open before/after upload (not blockers for the repo, but on the record):** human accuracy audit of a question sample; human Nepali-translation review; real-browser smoke test (360px, EN/NE toggle, countdown + auto-submit); Supabase setup on the user's computer (see `docs/BACKEND.md` §5) for real Google sign-in — the maintainer-bootstrap SQL now uses a placeholder, so the user must substitute his own Gmail address when he runs it.

**Maintainer rule (standing):** Ravi Yadav accepts or rejects every PR — no auto-merge. Stated in README, CONTRIBUTING.md, and the PR template.
