# Contributing to LokSewa Vidyapeeth — लोक सेवा विद्यापीठ · लोक सेवा तयारी

Thank you for helping Nepal's aspirants. Please read this before opening a pull request.

## Who decides

**Maintainer: Ravi Yadav ([@08raviyadav](https://github.com/08raviyadav)).** He reviews every pull request and issue, and **accepts or rejects each one himself**. There is no auto-merge, no bot approval, and no guarantee a PR will be merged — even a good one, if it duplicates work, conflicts with the syllabus, or doesn't fit the project. If your PR is closed, it is a decision, not a judgement on your effort; you are welcome to ask why in the PR thread.

## How to contribute

1. Fork the repo, create a branch (`add-questions-geography`, `fix-mock-timer`).
2. Keep changes small and focused — one topic / one fix per PR.
3. Run the tests before submitting: `node scripts/test-questions.js`, `node scripts/test-app.js`, `node scripts/test-e2e.js` and `node scripts/test-v2.js`. All four must pass (exit 0).
4. Fill in the pull-request template completely. Link the issue if there is one.
5. Write PR titles and descriptions in English.

## Adding questions — the accuracy rule (most important)

Every question must be **factually correct and verifiable**. This is an exam-prep site: a wrong answer actively harms a student.

- Use the exact JSON schema in the README. `id` must be unique (prefix per file, sequential). Exactly 4 distinct options. `answer` is the index (0–3) of the correct option — double-check it.
- Only add facts you are confident about, with a one-sentence explanation. If you are unsure of a date, number or name, **leave that question out**.
- No invented dates, vacancy numbers, or "current affairs" that will go stale. Current-affairs questions must cite a stable, checkable fact.
- No duplicate question text (the validator rejects it). No placeholder / lorem questions.
- Tag `exam` only with exams whose syllabus genuinely includes the topic. Valid tags (all 47 exam ids — enforced by `node scripts/test-questions.js`, see `VALID_EXAMS` there):
  - PSC: `kharidar`, `nasu`, `section-officer`, `deputy-secretary`, `psc-service-groups`, `provincial-psc`, `ranger`, `jta`, `nea`, `judicial-service`
  - Teaching: `tsc-primary`, `tsc-lower-secondary`, `tsc-secondary`, `tsc-license`
  - Banking: `nrb-assistant`, `nrb-officer`, `rbb`, `rbb-senior-assistant`
  - Uniformed: `police`, `army`
  - Technical / engineering: `engineering`, `sub-engineer`, `computer-operator`, `nepal-telecom`, `foreign-service`, `health`
  - Licence: `nmc-mbbs`, `nmc-bds`, `nnc-rn`, `midwifery-nlem`, `nhpc-ha`, `nhpc-lab`, `nhpc-radio`, `nhpc-physio`, `nhpc-public-health`, `nhpc-optometry`, `nhpc-dental`, `nhpc-ayurveda`, `npc-pharmacy`, `staff-nurse-psc`
  - Entrance / guide-only: `mecee-bl`, `nec-licence`, `bar-council`, `csit-entrance`, `ioe-entrance`, `anm-guide`, `ayurveda-bams`
- `marks` is 1 or 2 only. `difficulty` is `easy`, `medium` or `hard`.
- For maths/IQ questions, show the working in `explanation` and verify the calculation.
- Prefer Nepali context (Nepal history, Constitution 2072, geography, economy) over generic trivia.

Use the **Question contribution** issue template to propose a batch of questions before writing a large PR.

## Revision notes

Each topic can have a one-page revision note: key facts, formulas, article numbers and dates, in English **and** Nepali. Notes live in `data/notes/`, **one JSON file per topic** — this keeps PRs small and reviewable (one topic per PR, same as questions).

### File format

Create `data/notes/<slug>.json` and add the filename to `NOTES_FILES` in `assets/js/app.js` (keep the list sorted — `node scripts/test-app.js` enforces it).

```json
{
  "slug": "constitution-governance",
  "topic": "Constitution & Governance",
  "title_en": "Constitution & Governance — one-pager",
  "title_ne": "संविधान र शासन — एक-पृष्ठीय नोट",
  "updated": "2026-10-31",
  "source_note": "Facts cross-checked against the app's question bank and standard references.",
  "bullets": [
    { "en": "Promulgated: 3 Ashoj 2072 (20 September 2015).",
      "ne": "जारी मिति: 2072 असोज 3 (20 सेप्टेम्बर 2015)।" },
    { "en": "35 parts, 308 articles, 9 schedules.",
      "ne": "35 भाग, 308 धारा, 9 अनुसूची।" }
  ]
}
```

### Rules

- **Bilingual is mandatory** — every bullet needs both `en` and `ne`, and both `title_en` / `title_ne`. The app shows the Nepali text when the language toggle is on Nepali.
- **10–20 bullets per note.** Tight one-pagers: the facts students actually get asked, not a textbook chapter.
- **`topic` must match a question `topic` exactly** (e.g. `Constitution & Governance`). This is what the "📖 Revise this topic" button on wrong-answer review uses to jump to the right note — a mismatch means the button won't find it.
- **`slug`** is lowercase with hyphens, matching the filename (`constitution-governance.json`).
- **The accuracy rule applies to notes too**: only facts you are confident about and can verify — no invented dates, numbers or article references. Cross-check against the question bank (`data/questions/`) where possible.
- **`updated`** is the date you last verified the facts (`YYYY-MM-DD`).
- Run `node scripts/test-app.js` before submitting — it validates the schema of every note file.

## Contributing a question through the site (no PR needed)

You can also submit a question from the site itself: **Contribute → Submit a Question**.
The form shows the exact format first (copyable template below) and validates as you type.

### Format template (copy this — every field is required unless noted)

```json
{
  "id": "COMM-000",
  "exam": ["kharidar", "nasu"],
  "topic": "Constitution & Governance",
  "subtopic": "Fundamental Rights",
  "difficulty": "medium",
  "marks": 2,
  "question": "Which article of the Constitution of Nepal 2072 guarantees the right to freedom?",
  "question_ne": "नेपालको संविधान २०७२ को कुन धाराले स्वतन्त्रताको हकको ग्यारेन्टी गर्छ?",
  "options": ["Article 17", "Article 18", "Article 19", "Article 20"],
  "options_ne": ["धारा १७", "धारा १८", "धारा १९", "धारा २०"],
  "answer": 0,
  "explanation": "Article 17 guarantees the right to freedom.",
  "explanation_ne": "धारा १७ ले स्वतन्त्रताको हकको ग्यारेन्टी गर्छ।",
  "source": "Constitution of Nepal 2072, Part 3"
}
```

### Community question rules

- **Bilingual is mandatory.** Every question needs the English AND Nepali question, all 4 options in both languages, and both explanations. The bank is 100% bilingual and stays that way.
- **Question at least 15 characters.** Exactly 4 options per language, all different.
- **Answer must be A–D** and point at the correct option — double-check it.
- **Source is required** — a URL or a book / article / Act name. The source field is the only place links go; never put a link inside the question text.
- **One question per submission.** Small, focused submissions review faster than bulk dumps.

### Moderation policy — read this before you submit

> ⚠️ **Instant live + no spam cannot both be true.** Your submission does **not** go live when you send it. It goes through automatic checks (duplicate detection, spam heuristics, rate limit) **and** human review. **First-time submissions never go live instantly.**

1. **Automatic checks (first line of defence, not the real gate):** exact-duplicate and near-duplicate detection against the full bank (token-Jaccard ≥ 0.8 warns/blocks), spam heuristics (no links in question text, no repeated characters, no mostly-ALL-CAPS text), max **5 submissions per hour per device**.
2. **Maintainer review:** Ravi Yadav reviews every pending submission and **approves or rejects each one himself**. He may edit a question before approving it (fix a typo, tighten wording) — the approved version is what goes live.
3. **Approved** questions join the practice bank with a **"Community"** badge and your name in the source line. **Rejected** submissions get a reason, shown in the public moderation log (approved / rejected / pending counts are on the Contribute page).
4. **Trusted-contributor rule:** contributors with **3+ approved questions and 0 rejections** get faster review. It is not auto-approval — every question is still reviewed.
5. There is no auto-merge, no bot approval, and no guarantee a submission will be accepted — even a good one, if it duplicates work, conflicts with the syllabus, or doesn't fit the project.

### Spam policy

The following are blocked automatically and, if repeated, count against your contributor record:

- Links anywhere except the source field; repeated characters (`!!!!!`); mostly ALL-CAPS text; questions under 15 characters.
- Submitting the same question 3 times (it is already in the review queue — wait for the decision).
- More than 5 submissions in an hour (rate limit — you will see how many minutes remain).
- Bulk low-effort dumps, copied question sets, or questions with invented facts. These are rejected and, if repeated, the contributor's future submissions are deprioritised.

In demo mode these checks run in your browser (localStorage); after the backend is connected (see `docs/BACKEND.md`) they also run server-side, where they cannot be bypassed — client-side checks are the first line of defence, **server review is the real gate**.

## Reporting a wrong question

On the site, use the **⚑ Report wrong question** button on any question (quiz, result review, bookmarks, or search) — pick a reason and say what is wrong and what it should be, with a source if you can. Reports go to the maintainer's review queue.

Or open a bug report with the **question ID** (e.g. `HIST-042`), what is wrong, and the correct answer with a source. Do not just say "this is wrong".

## Code changes

- Vanilla HTML/CSS/JS only. No build step, no dependencies, no CDN, no tracking, no backend.
- Mobile-first, accessible (labels, focus states, contrast). Keep the app working from `file://` for the guide pages and from a static server for the question bank.
- Do not add analytics, ads, accounts, or any code that sends user data anywhere. Progress stays in `localStorage`.

## Code of Conduct

Be kind and respectful. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Harassment, spam PRs, and low-effort bulk question dumps will be closed.
