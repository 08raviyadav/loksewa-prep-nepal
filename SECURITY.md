# Security Policy

## This project stores no user data on any server

Lok Sewa Prep Nepal is a static, frontend-only site. There is no backend, no database, no account system, and no analytics. Progress (XP, streaks, attempts, bookmarks) is stored only in the visitor's own browser via `localStorage`.

## Reporting a vulnerability

If you find a security issue (for example, a script-injection flaw in how questions are rendered, or a way the site could leak data), please report it privately:

- Open a GitHub issue titled **"SECURITY: …"** with as little exploit detail in public as possible, **or**
- Contact the maintainer, Ravi Yadav, via GitHub (@08raviyadav).

Please do not open a public proof-of-concept exploit before the maintainer has had a chance to fix it.

## What we will do

- Acknowledge the report, fix the issue, and credit the reporter in the fix (unless they prefer not to be named).
- There is no bug bounty; this is a free community project.

## Out of scope

- Reports that the site works offline / stores data in `localStorage` (by design).
- Reports about exam-pattern figures being out of date — those are content corrections, not security issues; file them as a bug report with the question/exam ID and a source.
