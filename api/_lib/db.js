'use strict';
/* Shared Postgres access for the Vercel functions.
   - Lazy pool: created on first use, reused across warm invocations, so a
     cold start pays the connection cost once.
   - max: 1 — serverless functions scale by spinning up instances; one
     connection per instance keeps Vercel Postgres (Neon) connection
     counts small at this scale.
   - SSL on when the URL asks for it (Vercel Postgres DATABASE_URLs carry
     sslmode=require).
   - No DATABASE_URL (local dev without a DB, or the DB not provisioned
     yet) -> getPool() returns null and query() returns null; handlers
     answer 503 "backend not configured" so the frontend falls back to
     local save instead of failing silently.
   - The `pg` module is required lazily inside getPool(), so unit tests
     can inject a fake pool via setPoolForTests() on a machine with no
     `pg` installed at all. */
let _pool = null;
let _poolOverride = null;
let _warnedNoPg = false;

function setPoolForTests(pool) { _poolOverride = pool; }
function clearPoolForTests() { _poolOverride = null; _pool = null; }

function needsSsl(connectionString) {
  return /sslmode=require/i.test(connectionString || '') ||
    /\.neon\.tech/i.test(connectionString || '');
}

function getPool() {
  if (_poolOverride) return _poolOverride;
  if (_pool) return _pool;
  const url = process.env.DATABASE_URL;
  if (!url) return null;
  let pg;
  try {
    pg = require('pg');
  } catch (e) {
    if (!_warnedNoPg) {
      _warnedNoPg = true;
      console.error('[db] pg module not installed; database unavailable');
    }
    return null;
  }
  _pool = new pg.Pool({
    connectionString: url,
    ssl: needsSsl(url) ? { rejectUnauthorized: false } : undefined,
    max: 1,
    idleTimeoutMillis: 10 * 1000,
    connectionTimeoutMillis: 5 * 1000,
  });
  _pool.on('error', (err) => {
    // Idle-client errors must not crash the function; the next query
    // opens a fresh connection. Log the message only — never the query.
    console.error('[db] idle pool error:', err && err.message ? err.message : err);
  });
  return _pool;
}

/* Run a query. Returns the pg result, or null when no DB is configured.
   Throws on a real database error (handlers turn that into a 500). */
async function query(text, params) {
  const pool = getPool();
  if (!pool) return null;
  return pool.query(text, params);
}

/* Promise.race helper so /api/health never hangs on a dead database. */
function withTimeout(promise, ms) {
  let timer = null;
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error('timeout')), ms);
  });
  return Promise.race([promise, timeout]).finally(() => {
    if (timer) clearTimeout(timer);
  });
}

module.exports = { getPool, query, withTimeout, setPoolForTests, clearPoolForTests, needsSsl };
