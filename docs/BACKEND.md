# BACKEND.md — LokSewa Vidyapeeth: from demo mode to a real backend

## 0. Decision (2026-11-09): Vercel Serverless Functions + Vercel Postgres — for reports, now

**Stack chosen: Vercel Serverless Functions (Node) + Vercel Postgres, in this
same repo.** The code is built: `api/report.js`, `api/health.js`,
`api/_lib/` (db, validate, ratelimit, auth, respond), `db/schema.sql`,
`vercel.json`, `package.json` (`pg` only — the frontend stays
zero-dependency). Setup steps the user must do in the Vercel dashboard:
`docs/BACKEND_SETUP.md`.

Why this stack, and why not Supabase yet:
- **Zero new hosting.** The site already deploys on Vercel with auto-deploy
  on push. `api/*.js` in the same repo becomes live functions on the next
  push — no new account, no new project, no DNS, no CORS (same origin).
- **Free tier covers this scale.** Vercel Postgres free tier (256 MB storage,
  60 hours compute/month at the time of writing — verify in the dashboard)
  holds a trickle of text reports for years; function invocations are far
  below the free allowance for a report form.
- **Scope matches the need.** Reports need one table, server-side validation,
  rate limiting, and a single admin token — no user accounts, no realtime,
  no row-level security. Supabase would be the right call for the *next*
  step (real Google login, leaderboard, Discussion Hub sync — §§1–4 below),
  but standing it up now for a one-table report queue would add an account,
  a second Postgres, and OAuth plumbing for no user-facing gain.
- **No auth built.** Deliberately: there are no user accounts in this step.
  Admin access is one `ADMIN_TOKEN` env var, typed once per browser tab in
  the Review view and kept in `sessionStorage` only. That is report-triage
  level security, not enterprise auth — documented in `api/_lib/auth.js`.
- **Privacy unchanged.** The `reports` table stores only what the visitor
  typed (type, description, context). No IP, no user agent, no name, no
  page URL. Rate limiting hashes the IP in function memory only.

**Supabase remains the later path** for auth / leaderboard / discussions
(§§1–6 below are unchanged). When that lands, the reports table can move
to Supabase or stay on Vercel Postgres — the frontend talks to `/api/*`
either way, so the migration is a server-side swap, not a rewrite.

**Current state: demo mode.** Everything in v2 (sign-in, Discussion Hub,
question submissions, moderation, report-wrong-question) runs on
`localStorage` on one device. No data leaves the device, no account is
created, no Google login happens. This document is the plan to make it real.

## 1. Recommendation: Supabase (free tier) as the primary backend

| Need | Supabase (recommended) | Firebase |
|---|---|---|
| Google Auth (Gmail sign-in) | Built in — Google provider, one toggle, no extra code for the OAuth flow | Built in — Google provider, similar effort |
| Database | **Postgres** — real tables, joins, constraints, `pg_trgm` for near-duplicate search | Firestore — NoSQL documents; modelling threads/replies/moderation queues is more work |
| Row Level Security | **RLS policies in SQL** — users see only their own progress; submissions visible only after approval; maintainer-only moderation | Firestore security rules — a separate rule language, no SQL, harder to audit |
| Realtime for the Discussion Hub | **Realtime (Postgres changes → websocket)** — new threads/replies appear live | Firestore listeners — also live, comparable |
| Free tier limits | 500 MB database, 1 GB file storage, 50,000 monthly active users, 2 GB bandwidth — far more than this project needs for years | 1 GB storage, 50k reads/day, 20k writes/day — the read cap is the tighter one for a question bank |
| Self-host / lock-in | Open source, can self-host; plain Postgres you can export | Google-only; export is possible but the data model is Firestore-shaped |
| Cost beyond free | Pay-as-you-go from ~$25/mo | Pay-as-you-go (Blaze) |

**Decision: Supabase.** The deciding factors are Postgres + RLS: the
moderation model ("submissions visible only after approval", "maintainer-only
review view", "users see only their own progress") is a few SQL policies
instead of application code, and the duplicate-detection query can run in
Postgres (`pg_trgm` similarity) instead of shipping the whole bank to the
browser. Firebase would work, but its rules language and document model fit
this project worse.

## 2. Data model — exact SQL schema

Run in the Supabase SQL editor. All tables live in the `public` schema.
`auth.users` is Supabase's own table — `profiles.id` references it.

```sql
-- Profiles: one row per signed-in user. Created automatically on first sign-in.
create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  email text not null,
  name text not null default '',
  created_at timestamptz not null default now()
);

-- Progress: the cloud version of the localStorage object. One row per user.
-- Shape mirrors the demo-mode object so the migration is a straight upload:
-- { user_id, email, name, xp, level, streak, attempts[], bookmarks[], mistakes[] }
create table public.progress (
  user_id uuid primary key references public.profiles (id) on delete cascade,
  xp integer not null default 0,
  level integer not null default 1,
  streak integer not null default 0,
  last_day date,
  attempts jsonb not null default '[]'::jsonb,   -- [{date, mode, exam, total, correct, wrong, skipped, score, max, pct, passed, secs, xp}]
  bookmarks text[] not null default '{}',        -- question ids
  mistakes text[] not null default '{}',         -- question ids
  flashcards_seen integer not null default 0,
  daily_done jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

-- Discussion threads (one row per thread; replies are a separate table).
create table public.discussions (
  id uuid primary key default gen_random_uuid(),
  exam text not null default 'general',          -- exam id from data/exams.json, or 'general'
  question_id text,                              -- set when opened via "Discuss this question"
  title text not null,
  body text not null,
  author_id uuid references public.profiles (id) on delete set null,
  author_name text not null default 'Guest',
  upvotes integer not null default 0,
  created_at timestamptz not null default now()
);

create table public.discussion_replies (
  id uuid primary key default gen_random_uuid(),
  discussion_id uuid not null references public.discussions (id) on delete cascade,
  author_id uuid references public.profiles (id) on delete set null,
  author_name text not null default 'Guest',
  body text not null,
  created_at timestamptz not null default now()
);

-- Reports on discussion posts (spam / wrong info / abusive).
create table public.discussion_reports (
  id uuid primary key default gen_random_uuid(),
  discussion_id uuid not null references public.discussions (id) on delete cascade,
  reply_id uuid references public.discussion_replies (id) on delete cascade,
  reason text not null,
  reporter_id uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now()
);

-- Community question submissions. status starts as 'pending' and NOTHING
-- is visible to other users until a maintainer sets it to 'approved'.
create table public.question_submissions (
  id uuid primary key default gen_random_uuid(),
  contributor_id uuid references public.profiles (id) on delete set null,
  contributor_name text not null,
  exam text not null,
  topic text not null,
  subtopic text not null default '',
  difficulty text not null check (difficulty in ('easy', 'medium', 'hard')),
  marks integer not null check (marks in (1, 2)),
  question text not null,
  question_ne text not null,
  options jsonb not null,                        -- 4 strings (English)
  options_ne jsonb not null,                     -- 4 strings (Nepali)
  answer integer not null check (answer between 0 and 3),
  explanation text not null,
  explanation_ne text not null,
  source text not null,
  status text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  reject_reason text,
  submitted_at timestamptz not null default now(),
  reviewed_at timestamptz,
  reviewed_by uuid references public.profiles (id) on delete set null
);

-- Public, append-only moderation log: what was approved/rejected, when, by whom.
create table public.moderation_log (
  id uuid primary key default gen_random_uuid(),
  action text not null check (action in ('approved', 'rejected')),
  submission_id uuid references public.question_submissions (id) on delete set null,
  moderator_id uuid references public.profiles (id) on delete set null,
  reason text not null default '',
  created_at timestamptz not null default now()
);

-- Wrong-question reports (from the "Report wrong question" button).
create table public.question_reports (
  id uuid primary key default gen_random_uuid(),
  question_id text not null,
  reason text not null,
  comment text not null,
  reporter_id uuid references public.profiles (id) on delete set null,
  reporter_name text not null default 'Guest',
  status text not null default 'open' check (status in ('open', 'fixed', 'dismissed')),
  created_at timestamptz not null default now()
);

-- Maintainer role: a tiny table, not a column on profiles, so adding a second
-- maintainer later is one INSERT. Ravi Yadav is the first (and only) maintainer.
create table public.maintainers (
  user_id uuid primary key references public.profiles (id) on delete cascade,
  added_at timestamptz not null default now()
);

-- Enable RLS on everything. (Policies below.)
alter table public.profiles enable row level security;
alter table public.progress enable row level security;
alter table public.discussions enable row level security;
alter table public.discussion_replies enable row level security;
alter table public.discussion_reports enable row level security;
alter table public.question_submissions enable row level security;
alter table public.moderation_log enable row level security;
alter table public.question_reports enable row level security;
alter table public.maintainers enable row level security;

-- Near-duplicate search support (server-side duplicate check).
create extension if not exists pg_trgm;
create index question_submissions_question_trgm on public.question_submissions
  using gin (question gin_trgm_ops);
```

### The honest contradiction, stated once

**"Instant live" and "no spam" cannot both be true.** This schema encodes the
choice the project made: submissions are `pending` by default, invisible to
everyone except their author and maintainers, and only become live when a
maintainer approves them. First-time submissions **never** go live instantly.
Trusted contributors (3+ approved, 0 rejections — countable from
`question_submissions`) get faster review, not auto-approval.

## 3. RLS policies — exact SQL

```sql
-- Helper: is the caller a maintainer?
create or replace function public.is_maintainer()
returns boolean language sql stable as $$
  select exists (select 1 from public.maintainers where user_id = auth.uid());
$$;

-- Profiles: anyone can read names (needed to show authors); only the owner can update.
create policy "profiles readable by all" on public.profiles for select using (true);
create policy "profiles updatable by owner" on public.profiles for update using (auth.uid() = id);

-- Progress: users see and change ONLY their own row. Nobody else's.
create policy "own progress only" on public.progress for all using (auth.uid() = user_id);

-- Discussions: readable by all (signed in or not); only signed-in users can post.
create policy "threads readable by all" on public.discussions for select using (true);
create policy "threads insert by signed-in users" on public.discussions for insert with check (auth.uid() is not null);
create policy "threads delete by maintainer" on public.discussions for delete using (public.is_maintainer());
create policy "replies readable by all" on public.discussion_replies for select using (true);
create policy "replies insert by signed-in users" on public.discussion_replies for insert with check (auth.uid() is not null);
create policy "reports insert by signed-in users" on public.discussion_reports for insert with check (auth.uid() is not null);
create policy "reports readable by maintainer" on public.discussion_reports for select using (public.is_maintainer());

-- Submissions: authors see their own; everyone sees APPROVED ones only;
-- maintainers see all and are the only ones who can change status.
create policy "own submissions visible to author" on public.question_submissions for select
  using (auth.uid() = contributor_id);
create policy "approved submissions visible to all" on public.question_submissions for select
  using (status = 'approved');
create policy "submissions insert by signed-in users" on public.question_submissions for insert
  with check (auth.uid() is not null and auth.uid() = contributor_id);
create policy "submissions reviewed by maintainer only" on public.question_submissions for update
  using (public.is_maintainer());

-- Moderation log: public read (this is the "approved X / rejected Y / pending Z" counter source).
create policy "moderation log readable by all" on public.moderation_log for select using (true);
create policy "moderation log written by maintainer" on public.moderation_log for insert
  with check (public.is_maintainer());

-- Question reports: anyone signed in can file one; only maintainers read them.
create policy "question reports insert by signed-in users" on public.question_reports for insert
  with check (auth.uid() is not null);
create policy "question reports readable by maintainer" on public.question_reports for select
  using (public.is_maintainer());

-- Maintainers table: readable by all (so the UI can show who moderates);
-- writable only by an existing maintainer (bootstrap the first row in the SQL editor).
create policy "maintainers readable by all" on public.maintainers for select using (true);
create policy "maintainers written by maintainer" on public.maintainers for all
  using (public.is_maintainer());
```

**Maintainer bootstrap (run once, in the SQL editor, after Ravi's first sign-in):**

```sql
insert into public.maintainers (user_id)
select id from public.profiles where email = 'you@gmail.com';
-- Replace 'you@gmail.com' with the Gmail address you sign in with. Verify the row exists:
select * from public.maintainers;
```

## 4. Google OAuth setup

### Supabase side
1. Supabase dashboard → your project → **Authentication → Providers → Google** → Enable.
2. Paste the **Client ID** and **Client Secret** from Google Cloud (below).
3. Leave "Skip nonce checks" off. Save.

### Google Cloud Console side
1. [console.cloud.google.com](https://console.cloud.google.com) → create (or pick) a project.
2. **APIs & Services → OAuth consent screen** → User type **External** → fill app name
   "LokSewa Vidyapeeth", support email, developer contact email → Save.
3. **APIs & Services → Credentials → Create Credentials → OAuth client ID** →
   Application type **Web application** → name "LokSewa Vidyapeeth".
4. **Authorized JavaScript origins:** `http://localhost:8000` (local testing) and
   `https://08raviyadav.github.io` (GitHub Pages — adjust to the real Pages URL).
5. **Authorized redirect URIs:** `https://YOUR-PROJECT-REF.supabase.co/auth/v1/callback`
   (this is the Supabase callback — Google redirects here, Supabase redirects back to the app).
6. Copy the **Client ID** and **Client Secret** into Supabase (step above) and
   the Client ID into `config.js` as `GOOGLE_CLIENT_ID`.

### Supabase redirect URLs (the app side)
Supabase dashboard → **Authentication → URL Configuration**:
- **Site URL:** `https://08raviyadav.github.io/loksewa-prep-nepal/` (or the real Pages URL; `http://localhost:8000` for local testing).
- **Redirect URLs:** add both the localhost and the Pages URL.
- The app's sign-in button calls `supabase.auth.signInWithOAuth({ provider: 'google' })`;
  Supabase redirects to Google, Google back to Supabase, Supabase back to the Site URL
  with a session in the URL hash, which the Supabase JS client picks up.

## 5. Exact steps the user must take on his computer

1. **Create the Supabase project**
   - Go to [supabase.com](https://supabase.com) → sign in with Google → **New project** →
     name `loksewa-prep-nepal`, pick a database password (save it in a password manager),
     region **Singapore** (closest to Nepal) → Create. Wait ~2 minutes.
2. **Create the tables** — open the Supabase **SQL Editor**, paste §2 of this file,
   run it. Then paste §3 (RLS policies) and run it.
3. **Enable Google auth** — §4 above (Supabase provider + Google Cloud console).
4. **Bootstrap the maintainer** — sign in once on the site with Google (after step 6),
   then run the `insert into public.maintainers …` SQL from §3 with your Gmail address.
5. **Copy the keys** — Supabase dashboard → **Settings → API**: copy the **Project URL**
   and the **anon `public` key** (NOT the `service_role` key — that key bypasses RLS
   and must never go in the frontend).
6. **Create `config.js`** — in the project root:
   ```bash
   cp config.example.js config.js
   # edit config.js: replace YOUR-PROJECT-REF, YOUR-ANON-PUBLIC-KEY, YOUR-GOOGLE-OAUTH-CLIENT-ID
   ```
   **NEVER commit `config.js`** — it is in `.gitignore`. Only `config.example.js`
   (placeholders) is tracked. If the key ever leaks, rotate it in
   Supabase → Settings → API → "Generate new anon key".
7. **Reload the site** — the demo banner disappears; the Sign In button starts the
   real Google flow. Progress created in demo mode migrates on first sign-in:
   the app uploads the local `loksewa_progress_v1` object (same shape as the
   `progress` table) under the new `user_id`.
8. **Wire the remaining client calls** (one focused task, not done in v2 because
   it needs the live Supabase project to test against): replace the `localStorage`
   reads/writes in `assets/js/app.js` with Supabase client calls for profiles,
   discussions, submissions and moderation — the storage keys and function names
   are already the seam (`loadDiscussions`, `submitQuestion`, `approveSubmission`,
   `submitReport`, `signInDemo`). Add the Supabase JS client as a vendored file
   (the project uses no CDN — do not add a CDN script tag).

## 6. What stays demo-only until then

- Sign-in: local profile only, Gmail address validated by regex, no Google involved.
- Discussions: seeded threads + posts stored in `localStorage` (`loksewa_discussions_v1`).
- Submissions: validated client-side, queued in `loksewa_submissions_v1`, reviewed in
  the Maintainer Review view (no auth — anyone can open it; labelled as such).
- Approved questions: stored in `loksewa_community_approved_v1`, loaded into the
  bank at startup with a "Community" badge; exportable via the Download button
  as `community-approved.json` for committing to `data/questions/community-approved.json`.
- CAPTCHA: placeholder box only — hCaptcha/reCAPTCHA needs the backend (server-side
  verification; a client-side widget alone proves nothing).
- Rate limiting: per-device (localStorage timestamps) — a real per-account limit
  needs the backend; the client-side one stops casual spam, not determined abuse.
