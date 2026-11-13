-- Outrank — reports table (Vercel Postgres)
-- Run ONCE: Vercel dashboard -> Storage -> your Postgres database ->
-- Query tab, paste this file, Run. (Or: psql "$DATABASE_URL" -f db/schema.sql)
-- Safe to re-run: CREATE TABLE / CREATE INDEX use IF NOT EXISTS.
--
-- PRIVACY (the site promises "No tracking"): this table stores ONLY what
-- the visitor typed — the issue type, the description, and the context
-- (view / question id / exam / topic / reason). There is deliberately NO
-- column for IP address, user agent, name, email, phone number, or page
-- URL. Rate limiting hashes the IP in function memory only and never
-- persists it (see api/_lib/ratelimit.js).

CREATE TABLE IF NOT EXISTS reports (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  type text NOT NULL CHECK (type IN ('bug', 'wrong-info', 'wrong-question', 'other')),
  description text NOT NULL CHECK (char_length(description) >= 10 AND char_length(description) <= 2000),
  context jsonb NOT NULL DEFAULT '{}'::jsonb,
  status text NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'resolved')),
  created_at timestamptz NOT NULL DEFAULT now(),
  resolved_at timestamptz
);

-- Moderation queue reads newest-open first; type filter for triage.
CREATE INDEX IF NOT EXISTS reports_status_created_idx ON reports (status, created_at DESC);
CREATE INDEX IF NOT EXISTS reports_type_idx ON reports (type);

COMMENT ON TABLE reports IS 'Visitor issue reports (beta report form). No personal data: only type, description and context the visitor typed. Rate-limit IP hashes are in-memory only, never stored.';
