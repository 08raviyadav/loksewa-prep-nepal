'use strict';
/* Shared HTTP helpers for the Vercel functions (Node runtime).
   Vercel pre-parses a JSON request body into req.body; readBody() also
   accepts a raw string body (local test harnesses, curl) and returns null
   for an empty/unparseable one. Nothing here ever logs a body, a header,
   or a token. */

function sendJson(res, status, obj) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(obj));
}

function methodNotAllowed(res, allowed) {
  res.setHeader('Allow', allowed.join(', '));
  sendJson(res, 405, { error: 'method_not_allowed', allowed });
}

function readBody(req) {
  const b = req && req.body;
  if (b === undefined || b === null || b === '') return null;
  if (typeof b === 'object') return b;
  if (typeof b === 'string') {
    try { return JSON.parse(b); } catch (e) { return null; }
  }
  return null;
}

/* Client IP for rate limiting only. Vercel sits behind a proxy, so the
   first entry of X-Forwarded-For is the visitor. The raw value is hashed
   by the caller and never stored or logged. */
function getClientIp(req) {
  const xff = req && req.headers && (req.headers['x-forwarded-for'] || req.headers['X-Forwarded-For']);
  if (typeof xff === 'string' && xff.trim() !== '') return xff.split(',')[0].trim();
  if (req && req.socket && req.socket.remoteAddress) return req.socket.remoteAddress;
  return 'unknown';
}

module.exports = { sendJson, methodNotAllowed, readBody, getClientIp };
