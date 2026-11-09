'use strict';
/* Admin auth for the reports API: one shared token, nothing more.
   GET / PATCH / DELETE /api/report require
   `Authorization: Bearer <ADMIN_TOKEN>` where ADMIN_TOKEN is an env var
   set by the maintainer in the Vercel dashboard. This is report-triage
   level security — it keeps casual visitors out of the queue — not
   enterprise auth: anyone holding the token can list/resolve/delete
   reports, there is no per-person audit trail, and the token must be
   rotated if it ever leaks. If ADMIN_TOKEN is not configured, the admin
   endpoints answer 503 (never open). The token is compared in constant
   time and is never logged. */
const crypto = require('crypto');

function getBearerToken(req) {
  const h = req && req.headers && (req.headers.authorization || req.headers.Authorization);
  if (typeof h !== 'string') return null;
  const m = /^Bearer\s+(.+)$/.exec(h.trim());
  return m ? m[1] : null;
}

function timingSafeEqual(a, b) {
  const ba = Buffer.from(String(a));
  const bb = Buffer.from(String(b));
  if (ba.length !== bb.length) return false;
  return crypto.timingSafeEqual(ba, bb);
}

/* Returns { ok: true } or { ok: false, status, error }.
   - 503 admin_not_configured: no ADMIN_TOKEN env var at all.
   - 401 unauthorized: missing, malformed, or wrong token. */
function requireAdmin(req) {
  const expected = process.env.ADMIN_TOKEN;
  if (!expected) return { ok: false, status: 503, error: 'admin_not_configured' };
  const supplied = getBearerToken(req);
  if (!supplied || !timingSafeEqual(supplied, expected)) {
    return { ok: false, status: 401, error: 'unauthorized' };
  }
  return { ok: true };
}

module.exports = { getBearerToken, timingSafeEqual, requireAdmin };
