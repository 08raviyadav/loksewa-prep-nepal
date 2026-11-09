'use strict';
/* POST / GET / PATCH / DELETE /api/report — visitor reports, server-side.
   POST is public (rate-limited, validated). GET / PATCH / DELETE are
   admin-only (Authorization: Bearer <ADMIN_TOKEN>).
   Privacy: the row stores only what the visitor typed (type, description,
   context). No IP address, no user agent, no name, no page URL, no
   personal data. The client IP is hashed in memory for rate limiting and
   never persisted. Request bodies and tokens are never logged. */
const db = require('./_lib/db');
const { validateReportInput, validateListQuery, validateResolveBody, isUuid } = require('./_lib/validate');
const { hashKey, reportLimiter } = require('./_lib/ratelimit');
const { requireAdmin } = require('./_lib/auth');
const { sendJson, methodNotAllowed, readBody, getClientIp } = require('./_lib/respond');

const INSERT_SQL = 'INSERT INTO reports (type, description, context) VALUES ($1, $2, $3) RETURNING id, created_at';
const LIST_BASE = 'SELECT id, type, description, context, status, created_at, resolved_at FROM reports';

function publicReport(row) {
  return {
    id: row.id,
    type: row.type,
    description: row.description,
    context: row.context || {},
    status: row.status,
    created_at: row.created_at,
    resolved_at: row.resolved_at || null,
  };
}

async function handlePost(req, res) {
  // Rate limit first (10/hour/IP, hashed in memory, never stored).
  const ipHash = hashKey(getClientIp(req));
  const limit = reportLimiter.check(ipHash);
  if (!limit.allowed) {
    res.setHeader('Retry-After', String(Math.max(1, Math.ceil((limit.resetAt - Date.now()) / 1000))));
    return sendJson(res, 429, { error: 'rate_limited', retry_after_seconds: Math.max(1, Math.ceil((limit.resetAt - Date.now()) / 1000)) });
  }
  const v = validateReportInput(readBody(req));
  if (!v.ok) {
    // Honeypot trips get the same plain 400 as a bad type — no hint given.
    return sendJson(res, 400, { error: 'invalid_report', detail: v.error });
  }
  let result;
  try {
    result = await db.query(INSERT_SQL, [v.value.type, v.value.description, JSON.stringify(v.value.context)]);
  } catch (e) {
    console.error('[api/report] insert failed:', e && e.message ? e.message : e);
    return sendJson(res, 500, { error: 'internal_error' });
  }
  if (result === null) return sendJson(res, 503, { error: 'backend_not_configured' });
  const row = result.rows && result.rows[0];
  if (!row) return sendJson(res, 500, { error: 'internal_error' });
  return sendJson(res, 201, { id: row.id, created_at: row.created_at });
}

async function handleGet(req, res) {
  const admin = requireAdmin(req);
  if (!admin.ok) return sendJson(res, admin.status, { error: admin.error });
  const q = validateListQuery(req.query || {});
  if (!q.ok) return sendJson(res, 400, { error: 'invalid_query', detail: q.error });
  const { status, type, limit, offset } = q.value;
  const where = [];
  const params = [];
  if (status !== 'all') { params.push(status); where.push(`status = $${params.length}`); }
  if (type) { params.push(type); where.push(`type = $${params.length}`); }
  params.push(limit); const limitPos = params.length;
  params.push(offset); const offsetPos = params.length;
  const sql = LIST_BASE +
    (where.length ? ' WHERE ' + where.join(' AND ') : '') +
    ` ORDER BY created_at DESC LIMIT $${limitPos} OFFSET $${offsetPos}`;
  let result;
  try {
    result = await db.query(sql, params);
  } catch (e) {
    console.error('[api/report] list failed:', e && e.message ? e.message : e);
    return sendJson(res, 500, { error: 'internal_error' });
  }
  if (result === null) return sendJson(res, 503, { error: 'backend_not_configured' });
  return sendJson(res, 200, { reports: (result.rows || []).map(publicReport), count: (result.rows || []).length });
}

async function handlePatch(req, res) {
  const admin = requireAdmin(req);
  if (!admin.ok) return sendJson(res, admin.status, { error: admin.error });
  const id = req.query && req.query.id;
  if (!isUuid(id)) return sendJson(res, 400, { error: 'invalid_id' });
  const v = validateResolveBody(readBody(req));
  if (!v.ok) return sendJson(res, 400, { error: 'invalid_body', detail: v.error });
  let result;
  try {
    result = await db.query(
      "UPDATE reports SET status = 'resolved', resolved_at = now() WHERE id = $1 AND status = 'open' RETURNING id, status, resolved_at",
      [id],
    );
  } catch (e) {
    console.error('[api/report] resolve failed:', e && e.message ? e.message : e);
    return sendJson(res, 500, { error: 'internal_error' });
  }
  if (result === null) return sendJson(res, 503, { error: 'backend_not_configured' });
  const row = result.rows && result.rows[0];
  if (!row) return sendJson(res, 404, { error: 'not_found' });
  return sendJson(res, 200, { id: row.id, status: row.status, resolved_at: row.resolved_at });
}

async function handleDelete(req, res) {
  const admin = requireAdmin(req);
  if (!admin.ok) return sendJson(res, admin.status, { error: admin.error });
  const id = req.query && req.query.id;
  if (!isUuid(id)) return sendJson(res, 400, { error: 'invalid_id' });
  let result;
  try {
    result = await db.query('DELETE FROM reports WHERE id = $1 RETURNING id', [id]);
  } catch (e) {
    console.error('[api/report] delete failed:', e && e.message ? e.message : e);
    return sendJson(res, 500, { error: 'internal_error' });
  }
  if (result === null) return sendJson(res, 503, { error: 'backend_not_configured' });
  const row = result.rows && result.rows[0];
  if (!row) return sendJson(res, 404, { error: 'not_found' });
  return sendJson(res, 200, { deleted: true, id: row.id });
}

async function handler(req, res) {
  try {
    if (req.method === 'POST') return await handlePost(req, res);
    if (req.method === 'GET') return await handleGet(req, res);
    if (req.method === 'PATCH') return await handlePatch(req, res);
    if (req.method === 'DELETE') return await handleDelete(req, res);
    return methodNotAllowed(res, ['GET', 'POST', 'PATCH', 'DELETE']);
  } catch (e) {
    console.error('[api/report] unexpected:', e && e.message ? e.message : e);
    if (!res.headersSent) return sendJson(res, 500, { error: 'internal_error' });
    return undefined;
  }
}

module.exports = handler;
