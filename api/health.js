'use strict';
/* GET /api/health — lets the frontend decide whether to use the API.
   Always answers 200 with { ok, db } so the frontend can read the JSON
   without treating "backend down" as a fetch error:
   - { ok: true,  db: 'up' }   — DATABASE_URL set and SELECT 1 succeeded.
   - { ok: false, db: 'down' } — no DATABASE_URL yet, or the DB did not
     answer within 3 seconds. The frontend then uses the local save +
     GitHub fallback and says so. */
const db = require('./_lib/db');
const { sendJson, methodNotAllowed } = require('./_lib/respond');

async function handler(req, res) {
  try {
    if (req.method !== 'GET') return methodNotAllowed(res, ['GET']);
    const pool = db.getPool();
    if (!pool) return sendJson(res, 200, { ok: false, db: 'down' });
    try {
      await db.withTimeout(pool.query('SELECT 1'), 3000);
      return sendJson(res, 200, { ok: true, db: 'up' });
    } catch (e) {
      return sendJson(res, 200, { ok: false, db: 'down' });
    }
  } catch (e) {
    return sendJson(res, 200, { ok: false, db: 'down' });
  }
}

module.exports = handler;
