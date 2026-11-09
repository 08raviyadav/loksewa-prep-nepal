# BACKEND_SETUP.md — going live with the reports backend

**Stack:** Vercel Serverless Functions (Node) + Vercel Postgres, in this
same repo (`api/`, `db/schema.sql`). The frontend is progressive
enhancement: **before you do any of this, the site already works** — reports
save on the visitor's device and the GitHub Issues button sends them to you.
These steps only switch the report flow from "local save + GitHub" to
"sent straight to you, visible in the Review view".

**What you must do yourself (4 steps, ~10 minutes, all in the Vercel
dashboard — nobody can do these from the repo):**

## Step 1 — Create the Postgres database
1. Open [vercel.com](https://vercel.com) → your **loksewa-prep-nepal** project.
2. Top menu → **Storage** → **Create Database** → choose **Postgres**.
3. Name it `loksewa-reports` (any name works), region **Singapore**
   (closest to Nepal; any region works, this is just lowest latency).
4. Click **Create**. Vercel automatically adds `DATABASE_URL` (plus
   `POSTGRES_URL` etc.) to the project's env vars — you do not type the
   connection string by hand.

## Step 2 — Add the admin token
1. Project → **Settings** → **Environment Variables**.
2. Add: key `ADMIN_TOKEN`, value = a long random string you invent
   (e.g. run `openssl rand -hex 32` on your computer and paste the output;
   at least 32 characters, letters + digits).
3. Scope: **Production** (and Preview if you want to test on preview
   deploys). Save.
4. Keep this token private — anyone holding it can list, resolve and
   delete reports. If it ever leaks, change it here and redeploy.

## Step 3 — Create the table (run the schema once)
1. Still in the project → **Storage** → click your Postgres database →
   **Query** tab.
2. Open `db/schema.sql` in this repo, copy the whole file, paste it into
   the Query editor, click **Run**.
3. You should see the `reports` table created (id, type, description,
   context, status, created_at, resolved_at) plus two indexes. No rows yet —
   that is normal.
4. Alternative (if you prefer a terminal): `psql "$DATABASE_URL" -f db/schema.sql`
   after linking the project with `vercel link` and `vercel env pull`.

## Step 4 — Redeploy
- Push this code to GitHub (or press **Redeploy** on the latest deployment
  in Vercel). Vercel auto-deploys on push; the deploy installs `pg`
  (from `package.json`) and the `api/*.js` files become live functions.
- Wait for the deployment to finish (green check).

## Verify it works (2 minutes)
1. **Health:** `curl https://<your-vercel-domain>/api/health` — expect
   `{"ok":true,"db":"up"}`. If you see `{"ok":false,"db":"down"}`, the
   database is not connected yet — re-check Step 1 (is `DATABASE_URL` in
   Environment Variables?) and Step 3 (did the schema run?).
2. **Submit a test report:** open the live site → **Report an issue** →
   type a test description → Submit. The success message should now say
   **"Reported — the maintainer can see it."** (Before the backend, it said
   "Saved on this device…".)
3. **Check the Review view:** open **Maintainer Review** → the top line
   should say **"Backend: connected ✓"**. Paste your `ADMIN_TOKEN` in the
   admin box → **Connect backend** → your test report appears under
   **Reports (server)**. Click **Resolve** — it disappears from the open
   list. (The token is kept in that browser tab only; closing the tab
   forgets it.)
4. **Delete the test report** (or resolve it) so the queue starts clean.

## What happens before you do these steps
Everything, with the local + GitHub fallback:
- Report form: validates, saves on the visitor's device, success message
  says honestly "Saved on this device — will reach the maintainer once the
  backend is connected", GitHub button still offered.
- Review view: shows local reports only, line reads "Backend: not
  connected".
- `/api/health` answers `{"ok":false,"db":"down"}` (or 404 on GitHub Pages,
  which has no functions — the Vercel deployment is where the API lives).
- The rest of the site (practice, mocks, exams, festivals, birthday) is
  untouched — none of it calls the backend.

## Cost — free tier
- **Vercel Hobby (free):** serverless functions + 100 GB bandwidth/month —
  a report form is a rounding error against this.
- **Vercel Postgres free tier:** at the time of writing, 256 MB storage and
  60 hours of compute per month. A text report is ~1 KB; 256 MB holds
  hundreds of thousands of reports. Compute hours are the tighter limit
  only if the database is queried constantly — it is queried only when a
  visitor submits a report or you open the Review view, seconds per day.
- **At the limit:** Vercel pauses the database (writes fail) rather than
  charging you. The site keeps working: the frontend sees `/api/health`
  go down and falls back to local save + GitHub, honestly labelled. To
  resume, upgrade Storage in the dashboard or delete old resolved reports.
- **No other paid service is involved.** No Supabase, no third-party auth,
  no analytics, no tracking.

## Security notes (read once)
- `ADMIN_TOKEN` is report-triage level security, not enterprise auth.
  One shared token, no per-person audit trail. Good enough for one
  maintainer triaging bug reports; do not reuse the token anywhere else.
- The API never stores IP addresses, user agents, names, emails, or page
  URLs. Rate limiting (10 reports/hour/IP) hashes the IP in function
  memory only (`api/_lib/ratelimit.js`).
- `DATABASE_URL` is a secret: Vercel injects it as an env var; it is never
  in the repo. `.env.local` and `.vercel/` are git-ignored.
- The frontend token lives in `sessionStorage` only (forgotten when the
  tab closes) — never `localStorage`, never in the repo, never in a URL.

## Local development (test without deploying)
```bash
# 1. Install the one backend dependency (pg) — frontend needs nothing.
npm install

# 2. Unit + handler tests with a mocked database (no live DB needed):
node scripts/test-backend.js

# 3. Full site suites (unchanged behaviour must stay green):
node scripts/test-report.js
node scripts/test-v2.js

# 4. Against a real database (optional):
#    a. Create a free Postgres anywhere (Vercel Storage, or local Postgres).
#    b. cp .env.example .env.local  — fill in DATABASE_URL + ADMIN_TOKEN.
#    c. psql "$DATABASE_URL" -f db/schema.sql   (DATABASE_URL from .env.local)
#    d. npx vercel dev
#       (first run: `vercel link` to connect the local folder to the project)
#    e. curl http://localhost:3000/api/health  -> {"ok":true,"db":"up"}
#       Submit a report from http://localhost:3000 and watch it land in
#       the database: psql "$DATABASE_URL" -c "SELECT id, type, status FROM reports;"
```
`vercel dev` serves the static site and the `api/` functions together on
localhost, so the report form, health check, and Review view can all be
exercised end to end before anything is pushed.
