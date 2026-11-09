'use strict';
/* In-memory per-key rate limiting for the reports API.
   Deliberately NOT persisted: the key is a SHA-256 hash of the client IP
   (see hashKey), the map lives only in the function's memory, and entries
   expire with their window. A cold start resets all counters — acceptable
   for report triage, and it means no visitor identifier ever reaches the
   database or a log. Pure except for the clock, which tests inject. */
const crypto = require('crypto');

function hashKey(value) {
  return crypto.createHash('sha256').update(String(value || 'unknown')).digest('hex');
}

/* Sliding-window counter: at most `max` hits per `windowMs` per key.
   Returns { allowed, remaining, resetAt }. */
function createRateLimiter({ windowMs, max }) {
  const hits = new Map(); // key -> { count, resetAt }
  function prune(now) {
    for (const [k, v] of hits) {
      if (v.resetAt <= now) hits.delete(k);
    }
  }
  function check(key, nowMs) {
    const now = nowMs === undefined ? Date.now() : nowMs;
    prune(now);
    const entry = hits.get(key);
    if (!entry) {
      hits.set(key, { count: 1, resetAt: now + windowMs });
      return { allowed: true, remaining: max - 1, resetAt: now + windowMs };
    }
    if (entry.count >= max) {
      return { allowed: false, remaining: 0, resetAt: entry.resetAt };
    }
    entry.count += 1;
    return { allowed: true, remaining: max - entry.count, resetAt: entry.resetAt };
  }
  function reset() { hits.clear(); }
  function size() { return hits.size; }
  return { check, reset, size };
}

// Reports: 10 submissions per IP per hour. Generous for a human filing
// real issues, tight enough to blunt a spray-and-pray bot.
const reportLimiter = createRateLimiter({ windowMs: 60 * 60 * 1000, max: 10 });

module.exports = { hashKey, createRateLimiter, reportLimiter };
