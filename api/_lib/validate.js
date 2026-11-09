'use strict';
/* Shared validation for the reports API (api/report.js).
   Pure functions, no dependencies, no I/O — unit-tested in
   scripts/test-backend.js. The browser-side validateReport() in
   assets/js/report.js mirrors the 10–2000 char rule; this file is the
   server-side authority and must never be loosened to match the client. */

const REPORT_TYPES = ['bug', 'wrong-info', 'wrong-question', 'other'];
const QUESTION_REASONS = ['wrong-answer', 'wrong-explanation', 'typo', 'outdated', 'duplicate', 'other'];
const REPORT_STATUSES = ['open', 'resolved'];
const MAX_DESCRIPTION = 2000;
const MIN_DESCRIPTION = 10;
const MAX_CONTEXT_FIELD = 200;
const MAX_QUESTION_ID = 100;
const MAX_LIMIT = 200;
const DEFAULT_LIMIT = 50;
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function isPlainObject(v) {
  return v !== null && typeof v === 'object' && !Array.isArray(v);
}

function cleanContextField(v, max) {
  if (v === null || v === undefined) return null;
  if (typeof v !== 'string') return undefined; // signals "wrong type"
  const s = v.trim();
  if (s.length > max) return undefined;
  return s === '' ? null : s;
}

/* Validate a POST /api/report body.
   Accepts { type, description, context? } and, for convenience, a top-level
   questionId / reason (the frontend sends them inside context; accepting
   them top-level too keeps old clients working). Returns
   { ok: true, value: { type, description, context } } or
   { ok: false, error } where error is a short machine code ('type',
   'description', 'context', 'honeypot', 'body'). Human wording lives in
   the handler, so no user-facing string is duplicated here. */
function validateReportInput(body) {
  if (!isPlainObject(body)) return { ok: false, error: 'body' };
  // Honeypot: the form carries a hidden "website" field no human ever
  // fills. A filled value means a bot — reject without saying why.
  if (typeof body.website === 'string' && body.website.trim() !== '') {
    return { ok: false, error: 'honeypot' };
  }
  if (!REPORT_TYPES.includes(body.type)) return { ok: false, error: 'type' };
  if (typeof body.description !== 'string') return { ok: false, error: 'description' };
  const description = body.description.trim();
  if (description.length < MIN_DESCRIPTION || description.length > MAX_DESCRIPTION) {
    return { ok: false, error: 'description' };
  }
  const rawCtx = body.context === undefined ? {} : body.context;
  if (!isPlainObject(rawCtx)) return { ok: false, error: 'context' };
  const context = {};
  const fields = [
    ['view', MAX_CONTEXT_FIELD],
    ['questionId', MAX_QUESTION_ID],
    ['exam', MAX_CONTEXT_FIELD],
    ['topic', MAX_CONTEXT_FIELD],
    ['reason', MAX_CONTEXT_FIELD],
  ];
  for (const [key, max] of fields) {
    // Top-level questionId / reason win over context when both are present.
    const raw = (key === 'questionId' || key === 'reason') && body[key] !== undefined
      ? body[key]
      : rawCtx[key];
    if (raw === undefined) { context[key] = null; continue; }
    const cleaned = cleanContextField(raw, max);
    if (cleaned === undefined) return { ok: false, error: 'context' };
    context[key] = cleaned;
  }
  if (context.reason !== null && !QUESTION_REASONS.includes(context.reason)) {
    return { ok: false, error: 'context' };
  }
  return { ok: true, value: { type: body.type, description, context } };
}

/* Validate GET /api/report query params. */
function validateListQuery(query) {
  const q = query || {};
  const status = q.status === undefined ? 'open' : String(q.status);
  if (![...REPORT_STATUSES, 'all'].includes(status)) return { ok: false, error: 'status' };
  const type = q.type === undefined ? null : String(q.type);
  if (type !== null && !REPORT_TYPES.includes(type)) return { ok: false, error: 'type' };
  let limit = DEFAULT_LIMIT;
  if (q.limit !== undefined) {
    limit = Number.parseInt(String(q.limit), 10);
    if (!Number.isFinite(limit) || limit < 1 || limit > MAX_LIMIT) return { ok: false, error: 'limit' };
  }
  let offset = 0;
  if (q.offset !== undefined) {
    offset = Number.parseInt(String(q.offset), 10);
    if (!Number.isFinite(offset) || offset < 0) return { ok: false, error: 'offset' };
  }
  return { ok: true, value: { status, type, limit, offset } };
}

/* Validate a PATCH /api/report body — resolving only. */
function validateResolveBody(body) {
  if (!isPlainObject(body)) return { ok: false, error: 'body' };
  if (body.status !== 'resolved') return { ok: false, error: 'status' };
  return { ok: true, value: { status: 'resolved' } };
}

function isUuid(v) {
  return typeof v === 'string' && UUID_RE.test(v);
}

module.exports = {
  REPORT_TYPES,
  QUESTION_REASONS,
  REPORT_STATUSES,
  MIN_DESCRIPTION,
  MAX_DESCRIPTION,
  DEFAULT_LIMIT,
  MAX_LIMIT,
  validateReportInput,
  validateListQuery,
  validateResolveBody,
  isUuid,
};
