/* Backend checks: Vercel Functions + Vercel Postgres reports API.
   Node, no deps. Usage: node scripts/test-backend.js
   The API handlers run against a MOCKED pool (no live database, no `pg`
   needed locally) — that is stated, not hidden: db.setPoolForTests().
   Live-DB verification is a dashboard step (docs/BACKEND_SETUP.md).
   Frontend fallback logic runs in a vm sandbox with a controllable fetch
   mock, mirroring scripts/test-report.js. */
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
let fail = 0, pass = 0;
function check(name, ok, extra = '') {
  if (ok) { pass++; console.log('PASS  ' + name + (extra ? ' — ' + extra : '')); }
  else { fail++; console.log('FAIL  ' + name + (extra ? ' — ' + extra : '')); }
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

const validateLib = require(path.join(root, 'api/_lib/validate.js'));
const rateLib = require(path.join(root, 'api/_lib/ratelimit.js'));
const authLib = require(path.join(root, 'api/_lib/auth.js'));
const dbLib = require(path.join(root, 'api/_lib/db.js'));
const reportHandler = require(path.join(root, 'api/report.js'));
const healthHandler = require(path.join(root, 'api/health.js'));

// ---------- fake HTTP ----------
function makeReq(opts) {
  opts = opts || {};
  return {
    method: opts.method || 'GET',
    body: opts.body,
    query: opts.query || {},
    headers: opts.headers || {},
    socket: { remoteAddress: opts.ip || '9.9.9.9' },
  };
}
function makeRes() {
  const r = {
    statusCode: 0, headers: {}, body: '',
    setHeader(k, v) { this.headers[String(k).toLowerCase()] = v; },
    end(s) { this.body = s; },
    json() { try { return JSON.parse(this.body); } catch (e) { return null; } },
  };
  return r;
}

// ---------- mock pool ----------
const UUID_INSERT = '11111111-1111-4111-8111-111111111111';
const UUID_RESOLVABLE = '22222222-2222-4222-8222-222222222222';
const UUID_DELETABLE = '33333333-3333-4333-8333-333333333333';
const UUID_UNKNOWN = '44444444-4444-4444-8444-444444444444';
const SERVER_ROWS = [
  { id: UUID_RESOLVABLE, type: 'bug', description: 'Server bug report here.', context: { view: 'home' }, status: 'open', created_at: '2026-11-09T10:00:00.000Z', resolved_at: null },
  { id: '55555555-5555-4555-8555-555555555555', type: 'wrong-question', description: 'Server question report here.', context: { view: 'practice', questionId: 'Q-1', reason: 'typo' }, status: 'open', created_at: '2026-11-09T11:00:00.000Z', resolved_at: null },
  { id: '66666666-6666-4666-8666-666666666666', type: 'bug', description: 'Already resolved server bug.', context: {}, status: 'resolved', created_at: '2026-11-08T10:00:00.000Z', resolved_at: '2026-11-09T09:00:00.000Z' },
];
const poolCalls = [];
function makeMockPool() {
  return {
    on() {},
    query: async (text, params) => {
      poolCalls.push({ text, params: params || [] });
      if (text === 'SELECT 1') return { rows: [{ '?column?': 1 }] };
      if (text.startsWith('INSERT')) return { rows: [{ id: UUID_INSERT, created_at: '2026-11-09T12:00:00.000Z' }] };
      if (text.startsWith('SELECT')) {
        const hasStatus = text.includes('status = $');
        const hasType = text.includes('type = $');
        let idx = 0, rows = SERVER_ROWS.slice();
        if (hasStatus) { const s = params[idx++]; rows = rows.filter(r => r.status === s); }
        if (hasType) { const t = params[idx++]; rows = rows.filter(r => r.type === t); }
        const limit = params[params.length - 2], offset = params[params.length - 1];
        return { rows: rows.slice(offset, offset + limit) };
      }
      if (text.startsWith('UPDATE')) {
        return params[0] === UUID_RESOLVABLE
          ? { rows: [{ id: UUID_RESOLVABLE, status: 'resolved', resolved_at: '2026-11-09T12:30:00.000Z' }] }
          : { rows: [] };
      }
      if (text.startsWith('DELETE')) {
        return params[0] === UUID_DELETABLE ? { rows: [{ id: UUID_DELETABLE }] } : { rows: [] };
      }
      return { rows: [] };
    },
  };
}

(async () => {
  // ================= 1. Validation (pure) =================
  const V = validateLib;
  check('validate accepts a full general report', V.validateReportInput({ type: 'bug', description: 'A long enough description here.', context: { view: 'home' } }).ok);
  check('validate accepts exactly 10 chars', V.validateReportInput({ type: 'other', description: '1234567890' }).ok);
  check('validate accepts exactly 2000 chars', V.validateReportInput({ type: 'bug', description: 'x'.repeat(2000) }).ok);
  check('validate rejects unknown type', !V.validateReportInput({ type: 'nope', description: 'A long enough description here.' }).ok);
  check('validate rejects 9-char description', !V.validateReportInput({ type: 'bug', description: '123456789' }).ok);
  check('validate rejects 2001-char description', !V.validateReportInput({ type: 'bug', description: 'x'.repeat(2001) }).ok);
  check('validate rejects missing description', !V.validateReportInput({ type: 'bug' }).ok);
  check('validate rejects missing type', !V.validateReportInput({ description: 'A long enough description here.' }).ok);
  check('validate rejects non-object body', !V.validateReportInput(null).ok && !V.validateReportInput('x').ok && !V.validateReportInput([]).ok);
  check('validate rejects filled honeypot', V.validateReportInput({ type: 'bug', description: 'A long enough description here.', website: 'http://spam.example' }).error === 'honeypot');
  check('validate accepts empty honeypot', V.validateReportInput({ type: 'bug', description: 'A long enough description here.', website: '' }).ok);
  check('validate rejects over-long context field', !V.validateReportInput({ type: 'bug', description: 'A long enough description here.', context: { view: 'v'.repeat(201) } }).ok);
  check('validate rejects unknown question reason', !V.validateReportInput({ type: 'wrong-question', description: 'A long enough description here.', context: { reason: 'made-up' } }).ok);
  check('validate merges top-level questionId/reason into context', (() => {
    const r = V.validateReportInput({ type: 'wrong-question', description: 'A long enough description here.', questionId: 'Q-9', reason: 'typo' });
    return r.ok && r.value.context.questionId === 'Q-9' && r.value.context.reason === 'typo';
  })());
  check('validate drops unknown context keys', (() => {
    const r = V.validateReportInput({ type: 'bug', description: 'A long enough description here.', context: { view: 'home', sneaky: 'x' } });
    return r.ok && !('sneaky' in r.value.context);
  })());
  check('validate trims the description', V.validateReportInput({ type: 'bug', description: '   padded description here   ' }).value.description === 'padded description here');
  check('list query defaults to open/50/0', (() => { const r = V.validateListQuery({}); return r.ok && r.value.status === 'open' && r.value.limit === 50 && r.value.offset === 0; })());
  check('list query accepts status=all + type filter', (() => { const r = V.validateListQuery({ status: 'all', type: 'bug', limit: '10' }); return r.ok && r.value.status === 'all' && r.value.type === 'bug' && r.value.limit === 10; })());
  check('list query rejects bad status/type/limit', !V.validateListQuery({ status: 'nope' }).ok && !V.validateListQuery({ type: 'nope' }).ok && !V.validateListQuery({ limit: '0' }).ok && !V.validateListQuery({ limit: '201' }).ok);
  check('resolve body accepts resolved only', V.validateResolveBody({ status: 'resolved' }).ok && !V.validateResolveBody({ status: 'open' }).ok && !V.validateResolveBody({}).ok);
  check('isUuid accepts uuids, rejects junk', V.isUuid(UUID_RESOLVABLE) && !V.isUuid('not-a-uuid') && !V.isUuid(''));

  // ================= 2. Rate limiter (pure) =================
  const lim = rateLib.createRateLimiter({ windowMs: 1000, max: 2 });
  check('limiter allows up to max', lim.check('a', 100).allowed && lim.check('a', 100).allowed);
  check('limiter blocks the (max+1)th hit', !lim.check('a', 100).allowed);
  check('limiter is per-key', lim.check('b', 100).allowed);
  check('limiter resets after the window', lim.check('a', 100 + 1001).allowed);
  check('limiter reports remaining honestly', rateLib.createRateLimiter({ windowMs: 1000, max: 3 }).check('x', 0).remaining === 2);
  check('hashKey is deterministic hex, never the raw IP', rateLib.hashKey('1.2.3.4') === rateLib.hashKey('1.2.3.4') && rateLib.hashKey('1.2.3.4') !== '1.2.3.4' && /^[0-9a-f]{64}$/.test(rateLib.hashKey('1.2.3.4')));
  check('hashKey differs per IP', rateLib.hashKey('1.2.3.4') !== rateLib.hashKey('5.6.7.8'));

  // ================= 3. Admin auth (pure) =================
  process.env.ADMIN_TOKEN = 'test-admin-token';
  check('requireAdmin passes the right token', authLib.requireAdmin(makeReq({ headers: { authorization: 'Bearer test-admin-token' } })).ok);
  check('requireAdmin rejects a wrong token', authLib.requireAdmin(makeReq({ headers: { authorization: 'Bearer nope' } })).status === 401);
  check('requireAdmin rejects a missing token', authLib.requireAdmin(makeReq({})).status === 401);
  check('requireAdmin rejects a non-Bearer header', authLib.requireAdmin(makeReq({ headers: { authorization: 'Token test-admin-token' } })).status === 401);
  delete process.env.ADMIN_TOKEN;
  check('requireAdmin 503s when no token is configured', authLib.requireAdmin(makeReq({ headers: { authorization: 'Bearer x' } })).status === 503);
  process.env.ADMIN_TOKEN = 'test-admin-token';

  // ================= 4. Handlers with a mocked pool =================
  delete process.env.DATABASE_URL;
  dbLib.setPoolForTests(makeMockPool());
  const goodReport = () => ({ type: 'bug', description: 'The mock timer keeps running after submit.' });
  const post = async (body, ip) => {
    const res = makeRes();
    await reportHandler(makeReq({ method: 'POST', body, ip: ip || '1.2.3.4', headers: { 'x-forwarded-for': ip || '1.2.3.4' } }), res);
    return res;
  };
  rateLib.reportLimiter.reset();
  let r = await post(goodReport());
  check('POST valid report -> 201 with id', r.statusCode === 201 && r.json() && r.json().id === UUID_INSERT, 'status ' + r.statusCode);
  check('POST uses parameterised INSERT (no string-built SQL)', poolCalls.some(c => c.text.startsWith('INSERT INTO reports') && c.params[0] === 'bug' && c.params[1] === goodReport().description));
  r = await post({ type: 'nope', description: 'A long enough description here.' });
  check('POST bad type -> 400', r.statusCode === 400 && r.json().error === 'invalid_report');
  r = await post({ type: 'bug', description: 'short' });
  check('POST short description -> 400', r.statusCode === 400);
  r = await post({ type: 'bug', description: 'x'.repeat(2001) });
  check('POST 2001-char description -> 400', r.statusCode === 400);
  r = await post({ type: 'bug' });
  check('POST missing description -> 400', r.statusCode === 400);
  r = await post({ type: 'bug', description: 'A long enough description here.', website: 'http://spam.example' });
  check('POST filled honeypot -> 400', r.statusCode === 400);
  r = await post({ type: 'bug', description: '1234567890' });
  check('POST exactly-10-char description -> 201', r.statusCode === 201);
  // Rate limit: 10/hour/IP on the shared limiter.
  rateLib.reportLimiter.reset();
  let statuses = [];
  for (let i = 0; i < 11; i++) statuses.push((await post(goodReport(), '5.5.5.5')).statusCode);
  check('POST rate limit: 10 pass, 11th is 429', statuses.slice(0, 10).every(s => s === 201) && statuses[10] === 429, statuses.join(','));
  r = await post(goodReport(), '5.5.5.5');
  check('POST 429 carries Retry-After + honest error', r.json().error === 'rate_limited' && !!r.headers['retry-after']);
  rateLib.reportLimiter.reset();
  // No database configured -> 503, not a crash and not a fake success.
  dbLib.clearPoolForTests();
  delete process.env.DATABASE_URL;
  r = await post(goodReport(), '6.6.6.6');
  check('POST with no DATABASE_URL -> 503 backend_not_configured', r.statusCode === 503 && r.json().error === 'backend_not_configured');
  dbLib.setPoolForTests(makeMockPool());
  // GET (admin)
  const get = async (opts) => {
    const res = makeRes();
    await reportHandler(makeReq(Object.assign({ method: 'GET', query: {} }, opts)), res);
    return res;
  };
  r = await get({});
  check('GET without token -> 401', r.statusCode === 401);
  r = await get({ headers: { authorization: 'Bearer wrong' } });
  check('GET with wrong token -> 401', r.statusCode === 401);
  r = await get({ headers: { authorization: 'Bearer test-admin-token' }, query: { status: 'all' } });
  check('GET with token + status=all -> 200, all 3 rows', r.statusCode === 200 && r.json().reports.length === 3, 'status ' + r.statusCode + ', rows ' + (r.json() && r.json().reports ? r.json().reports.length : '?'));
  r = await get({ headers: { authorization: 'Bearer test-admin-token' } });
  check('GET with token defaults to open rows only', r.statusCode === 200 && r.json().reports.length === 2);
  r = await get({ headers: { authorization: 'Bearer test-admin-token' }, query: { status: 'resolved' } });
  check('GET status=resolved filters to 1 row', r.statusCode === 200 && r.json().reports.length === 1 && r.json().reports[0].status === 'resolved');
  r = await get({ headers: { authorization: 'Bearer test-admin-token' }, query: { status: 'all', type: 'wrong-question' } });
  check('GET type=wrong-question filters to 1 row', r.statusCode === 200 && r.json().reports.length === 1 && r.json().reports[0].type === 'wrong-question');
  r = await get({ headers: { authorization: 'Bearer test-admin-token' }, query: { status: 'bogus' } });
  check('GET bad status filter -> 400', r.statusCode === 400);
  delete process.env.ADMIN_TOKEN;
  r = await get({ headers: { authorization: 'Bearer test-admin-token' } });
  check('GET with ADMIN_TOKEN unconfigured -> 503, never open', r.statusCode === 503 && r.json().error === 'admin_not_configured');
  process.env.ADMIN_TOKEN = 'test-admin-token';
  // PATCH (resolve)
  const patch = async (id, body, token) => {
    const res = makeRes();
    await reportHandler(makeReq({ method: 'PATCH', body, query: { id }, headers: token === null ? {} : { authorization: 'Bearer ' + (token || 'test-admin-token') } }), res);
    return res;
  };
  r = await patch(UUID_RESOLVABLE, { status: 'resolved' });
  check('PATCH resolve -> 200 with resolved_at', r.statusCode === 200 && r.json().status === 'resolved' && !!r.json().resolved_at);
  r = await patch(UUID_UNKNOWN, { status: 'resolved' });
  check('PATCH unknown id -> 404', r.statusCode === 404);
  r = await patch('not-a-uuid', { status: 'resolved' });
  check('PATCH malformed id -> 400', r.statusCode === 400);
  r = await patch(UUID_RESOLVABLE, { status: 'open' });
  check('PATCH non-resolved status -> 400', r.statusCode === 400);
  r = await patch(UUID_RESOLVABLE, { status: 'resolved' }, null);
  check('PATCH without token -> 401', r.statusCode === 401);
  // DELETE
  const del = async (id, token) => {
    const res = makeRes();
    await reportHandler(makeReq({ method: 'DELETE', query: { id }, headers: token === null ? {} : { authorization: 'Bearer ' + (token || 'test-admin-token') } }), res);
    return res;
  };
  r = await del(UUID_DELETABLE);
  check('DELETE known id -> 200 deleted:true', r.statusCode === 200 && r.json().deleted === true && r.json().id === UUID_DELETABLE);
  r = await del(UUID_UNKNOWN);
  check('DELETE unknown id -> 404', r.statusCode === 404);
  r = await del(UUID_DELETABLE, null);
  check('DELETE without token -> 401', r.statusCode === 401);
  r = makeRes();
  await reportHandler(makeReq({ method: 'PUT' }), r);
  check('PUT -> 405 with Allow header', r.statusCode === 405 && (r.headers.allow || '').includes('GET'));
  // No secret ever logged: capture console.error across a failing POST.
  const seen = [];
  const origErr = console.error;
  console.error = (...a) => { seen.push(a.join(' ')); };
  dbLib.setPoolForTests({ on() {}, query: async () => { throw new Error('db exploded'); } });
  rateLib.reportLimiter.reset();
  await post({ type: 'bug', description: 'SECRET-DESCRIPTION-xyz unique string here.' });
  console.error = origErr;
  check('failing POST logs no description', !seen.join(' ').includes('SECRET-DESCRIPTION-xyz'));
  dbLib.setPoolForTests(makeMockPool());
  // Health
  const health = async () => { const res = makeRes(); await healthHandler(makeReq({ method: 'GET' }), res); return res; };
  r = await health();
  check('GET /api/health with mock DB -> {ok:true, db:up}', r.statusCode === 200 && r.json().ok === true && r.json().db === 'up');
  dbLib.setPoolForTests({ on() {}, query: async () => { throw new Error('db down'); } });
  r = await health();
  check('GET /api/health with failing DB -> {ok:false, db:down} (still 200)', r.statusCode === 200 && r.json().ok === false && r.json().db === 'down');
  dbLib.clearPoolForTests();
  r = await health();
  check('GET /api/health with no DATABASE_URL -> {ok:false, db:down}', r.json().ok === false && r.json().db === 'down');
  dbLib.setPoolForTests(makeMockPool());
  r = makeRes();
  await healthHandler(makeReq({ method: 'POST' }), r);
  check('POST /api/health -> 405', r.statusCode === 405);

  // ================= 5. Schema SQL sanity =================
  const schema = fs.readFileSync(path.join(root, 'db/schema.sql'), 'utf8');
  const tableBlock = (schema.match(/CREATE TABLE IF NOT EXISTS reports \(([\s\S]*?)\n\);/) || [])[1] || '';
  const colNames = tableBlock.split('\n').map(l => l.trim().split(/\s+/)[0]).filter(Boolean);
  for (const col of ['id', 'type', 'description', 'context', 'status', 'created_at', 'resolved_at']) {
    check('schema has column ' + col, colNames.includes(col));
  }
  check('schema forbids storing personal-data columns', !['ip_address', 'ip', 'user_agent', 'email', 'phone', 'name', 'page_url'].some(c => colNames.includes(c)), 'columns: ' + colNames.join(','));
  check('schema constrains type values', tableBlock.includes("type IN ('bug', 'wrong-info', 'wrong-question', 'other')"));
  check('schema constrains description to 10..2000 chars', tableBlock.includes('char_length(description) >= 10') && tableBlock.includes('char_length(description) <= 2000'));
  check('schema constrains status values', tableBlock.includes("status IN ('open', 'resolved')"));
  check('schema defaults status to open', tableBlock.includes("DEFAULT 'open'"));
  check('schema has status+created index', schema.includes('reports_status_created_idx'));
  check('schema has type index', schema.includes('reports_type_idx'));
  check('schema uses uuid PK with gen_random_uuid', tableBlock.includes('uuid PRIMARY KEY DEFAULT gen_random_uuid()'));
  check('schema is re-runnable (IF NOT EXISTS)', schema.includes('CREATE TABLE IF NOT EXISTS') && schema.includes('CREATE INDEX IF NOT EXISTS'));

  // ================= 6. Wiring: vercel.json / package.json / no new frontend deps =================
  const vercel = JSON.parse(fs.readFileSync(path.join(root, 'vercel.json'), 'utf8'));
  check('vercel.json configures api functions', vercel.functions && vercel.functions['api/*.js'] && vercel.functions['api/*.js'].maxDuration === 10);
  const pkg = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'));
  check('package.json declares pg (backend only)', pkg.dependencies && typeof pkg.dependencies.pg === 'string');
  check('package.json is private (never published)', pkg.private === true);
  const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
  check('index.html gains no new script tags (frontend still zero-dep)', (html.match(/<script src=/g) || []).length === 3);
  check('.gitignore keeps .env.local + .vercel out of the repo', fs.readFileSync(path.join(root, '.gitignore'), 'utf8').includes('.env.local') && fs.readFileSync(path.join(root, '.gitignore'), 'utf8').includes('.vercel/'));
  check('api sources contain no console.log at all', ['api/report.js', 'api/health.js', 'api/_lib/auth.js', 'api/_lib/db.js', 'api/_lib/ratelimit.js', 'api/_lib/validate.js', 'api/_lib/respond.js'].every(f => !fs.readFileSync(path.join(root, f), 'utf8').includes('console.log(')));
  check('api sources never read the Authorization header except in auth.js', ['api/report.js', 'api/health.js', 'api/_lib/db.js', 'api/_lib/ratelimit.js', 'api/_lib/validate.js', 'api/_lib/respond.js'].every(f => !fs.readFileSync(path.join(root, f), 'utf8').includes('authorization')));

  // ================= 7. Frontend fallback logic (vm sandbox) =================
  const fetchCalls = [];
  let fetchMode = 'up'; // 'up' | 'down' | 'throw' | 'post500'
  const serverRowsForUi = [
    { id: UUID_RESOLVABLE, type: 'bug', description: 'Server bug report here.', context: { view: 'home' }, status: 'open', created_at: '2026-11-09T10:00:00.000Z', resolved_at: null },
  ];
  function fakeFetch(url, opts) {
    opts = opts || {};
    fetchCalls.push({ url, method: opts.method || 'GET', auth: (opts.headers && opts.headers.Authorization) || null, body: opts.body || null });
    if (fetchMode === 'throw') return Promise.reject(new Error('network down'));
    if (String(url).startsWith('/api/health')) {
      const up = fetchMode === 'up' || fetchMode === 'post500';
      return Promise.resolve({ ok: true, status: 200, json: async () => ({ ok: up, db: up ? 'up' : 'down' }) });
    }
    if (String(url).startsWith('/api/report')) {
      if ((opts.method || 'GET') === 'POST') {
        if (fetchMode === 'post500') return Promise.resolve({ ok: false, status: 500, json: async () => ({ error: 'internal_error' }) });
        return Promise.resolve({ ok: true, status: 201, json: async () => ({ id: UUID_INSERT, created_at: '2026-11-09T12:00:00.000Z' }) });
      }
      if ((opts.method || 'GET') === 'GET') {
        if (!opts.headers || opts.headers.Authorization !== 'Bearer tok-abc') return Promise.resolve({ ok: false, status: 401, json: async () => ({ error: 'unauthorized' }) });
        return Promise.resolve({ ok: true, status: 200, json: async () => ({ reports: serverRowsForUi, count: serverRowsForUi.length }) });
      }
      return Promise.resolve({ ok: true, status: 200, json: async () => ({ id: UUID_RESOLVABLE, status: 'resolved' }) });
    }
    return Promise.reject(new Error('unexpected url ' + url));
  }
  function fakeEl(id) {
    return { id, innerHTML: '', hidden: false, textContent: '', value: '',
      classList: { _s: new Set(), contains(c) { return this._s.has(c); }, add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); } },
      style: {}, dataset: {}, appendChild() {}, setAttribute() {}, addEventListener() {},
      querySelector() { return null; }, querySelectorAll() { return []; } };
  }
  const elStore = {};
  const sessionStore = {};
  const sandbox = {
    module: { exports: {} }, console,
    localStorage: { _s: {}, getItem(k) { return (k in this._s) ? this._s[k] : null; }, setItem(k, v) { this._s[k] = String(v); }, removeItem(k) { delete this._s[k]; } },
    sessionStorage: { getItem(k) { return (k in sessionStore) ? sessionStore[k] : null; }, setItem(k, v) { sessionStore[k] = String(v); }, removeItem(k) { delete sessionStore[k]; } },
    navigator: { onLine: true },
    document: { addEventListener: () => {}, querySelector: () => null, querySelectorAll: () => [],
      getElementById(id) { if (!elStore[id]) elStore[id] = fakeEl(id); return elStore[id]; },
      createElement(tag) { return fakeEl(tag); }, documentElement: { dataset: {} } },
    window: {}, alert: () => {}, fetch: fakeFetch,
    scrollTo: () => {}, setInterval: () => 0, clearInterval: () => {},
    setTimeout, clearTimeout,
    Notification: undefined, matchMedia: undefined, confirm: () => true,
    AbortController: class { constructor() { this.signal = {}; } abort() {} },
    open(url) { return null; },
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  const appSrc = fs.readFileSync(path.join(root, 'assets/js/app.js'), 'utf8');
  const repSrc = fs.readFileSync(path.join(root, 'assets/js/report.js'), 'utf8');
  try {
    vm.runInContext(appSrc, sandbox);
    vm.runInContext(repSrc + '\nmodule.exports={B,setLang,getLang,validateReport,submitGeneralReport,openIssueForm,submitIssueForm,showIssueSuccess,buildGithubIssueUrl,resolveReport,deleteReport,renderReportsSection,loadReports,saveReports,checkBackendHealth,postReportToBackend,syncReportToBackend,getAdminToken,setAdminToken,forgetAdminToken,connectAdminToken,refreshBackendReports,backendState,getServerReports,backendStatusLineHtml,adminTokenBlockHtml,submitReport,closeModal};', sandbox);
    check('app.js + report.js parse in the backend sandbox', true);
  } catch (e) { check('app.js + report.js parse in the backend sandbox', false, e.message); process.exit(1); }
  const t = sandbox.module.exports;
  const run = code => vm.runInContext(code, sandbox);
  const el = id => elStore[id] || (elStore[id] = fakeEl(id));
  const store = () => JSON.parse(sandbox.localStorage._s['loksewa_reports_v1'] || '[]');
  const posts = () => fetchCalls.filter(c => c.url === '/api/report' && c.method === 'POST');
  const resetUi = () => { run(`localStorage.removeItem('loksewa_reports_v1')`); fetchCalls.length = 0; for (const k of Object.keys(sessionStore)) delete sessionStore[k]; };
  const submitViaForm = (desc) => {
    el('iss-type').value = 'wrong-info'; el('iss-desc').value = desc; el('iss-website').value = '';
    return run('submitIssueForm()');
  };

  // 7a. health states
  fetchMode = 'up';
  check('health up -> backendState() is up', (await run('checkBackendHealth(true)')) === true && t.backendState() === 'up');
  fetchMode = 'down';
  check('health down -> backendState() is down', (await run('checkBackendHealth(true)')) === false && t.backendState() === 'down');
  fetchMode = 'throw';
  check('fetch throwing -> backendState() is down, no crash', (await run('checkBackendHealth(true)')) === false && t.backendState() === 'down');
  sandbox.navigator.onLine = false;
  const callsBeforeOffline = fetchCalls.length;
  await run('checkBackendHealth(true)');
  check('offline -> health check never calls fetch', fetchCalls.length === callsBeforeOffline);
  check('offline -> backendState() is offline', (await run('checkBackendHealth(true)')) === false && t.backendState() === 'offline');
  sandbox.navigator.onLine = true;

  // 7b. API up: submit once -> one local save + exactly one POST + honest success
  fetchMode = 'up'; resetUi();
  await run('checkBackendHealth(true)'); // fresh state for the new fetch mode (the 60s cache is real behaviour)
  run(`openIssueForm({})`);
  check('submit with backend up returns true', submitViaForm('The mock timer keeps running after submit, please fix it.') === true);
  await sleep(150);
  check('backend-up submit saves exactly one local entry', store().length === 1);
  check('backend-up submit makes exactly one POST (no double-submit)', posts().length === 1, posts().length + ' POSTs');
  check('backend-up POST carries type + description + context, no name', (() => {
    const b = JSON.parse(posts()[0].body);
    return b.type === 'wrong-info' && b.description.includes('mock timer') && b.context && !('by' in b) && !b.description.includes('Guest');
  })());
  check('backend-up submit marks the entry synced with the server id', store()[0].synced === true && store()[0].serverId === UUID_INSERT);
  check('backend-up success line says the maintainer can see it', el('iss-backend-status').textContent.includes('maintainer can see it'));
  check('modal is unhidden after submit (question path included)', el('modal').hidden === false);

  // 7c. API down (fetch throws): local save + honest local message, no fake success
  fetchMode = 'throw'; resetUi();
  await run('checkBackendHealth(true)'); // health itself throws -> state down, so no POST is even attempted
  run(`openIssueForm({})`);
  check('submit with backend down returns true (local save)', submitViaForm('The guide page shows the wrong article count here.') === true);
  await sleep(150);
  check('backend-down submit still saves locally exactly once', store().length === 1);
  check('backend-down submit makes no successful POST', posts().length === 0);
  check('backend-down entry stays unsynced', store()[0].synced === false && store()[0].serverId === null);
  check('backend-down success line is the honest local message', el('iss-backend-status').textContent.includes('will reach the maintainer once the backend is connected'));

  // 7d. Health up but POST 500s: same honest fallback
  fetchMode = 'post500'; resetUi();
  await run('checkBackendHealth(true)');
  run(`openIssueForm({})`);
  submitViaForm('A report that the server will reject with 500 here.');
  await sleep(150);
  check('POST 500 keeps the local save + honest message', store().length === 1 && el('iss-backend-status').textContent.includes('will reach the maintainer once the backend is connected'));

  // 7e. Offline: no fetch at all to /api/report
  fetchMode = 'up'; resetUi();
  sandbox.navigator.onLine = false;
  run(`openIssueForm({})`);
  const beforeOffline = fetchCalls.length;
  submitViaForm('An offline report about the practice page here.');
  await sleep(150);
  check('offline submit saves locally with zero fetch calls', store().length === 1 && fetchCalls.length === beforeOffline);
  check('offline success line is the honest local message', el('iss-backend-status').textContent.includes('will reach the maintainer once the backend is connected'));
  sandbox.navigator.onLine = true;

  // 7f. Two submits -> two entries, two POSTs (never double per submit)
  fetchMode = 'up'; resetUi();
  await run('checkBackendHealth(true)');
  run(`openIssueForm({})`);
  submitViaForm('First report about the mock timer issue here.');
  submitViaForm('Second report about the guide page issue here.');
  await sleep(200);
  check('two submits -> two local entries, two POSTs', store().length === 2 && posts().length === 2, store().length + ' entries, ' + posts().length + ' POSTs');

  // 7g. Honeypot: filled hidden field -> nothing saved, nothing posted
  fetchMode = 'up'; resetUi();
  run(`openIssueForm({})`);
  el('iss-type').value = 'bug'; el('iss-desc').value = 'A bot report that should be dropped here.'; el('iss-website').value = 'http://spam.example';
  check('honeypot submit returns true but saves nothing', run('submitIssueForm()') === true && store().length === 0);
  await sleep(100);
  check('honeypot submit posts nothing', posts().length === 0);

  // 7h. Admin token: sessionStorage only, server merge, resolve/delete via API
  fetchMode = 'up'; resetUi();
  await run('checkBackendHealth(true)');
  check('token starts absent', t.getAdminToken() === null);
  run(`setAdminToken('tok-abc')`);
  check('token lands in sessionStorage', sessionStore['loksewa_admin_token_v1'] === 'tok-abc');
  check('token never lands in localStorage', !JSON.stringify(sandbox.localStorage._s).includes('tok-abc'));
  el('admin-token').value = 'tok-abc';
  check('connectAdminToken reads the input', run('connectAdminToken()') === true && sessionStore['loksewa_admin_token_v1'] === 'tok-abc');
  await sleep(150);
  check('connect fetches server reports with the Bearer token', fetchCalls.some(c => c.url.startsWith('/api/report') && c.method === 'GET' && c.auth === 'Bearer tok-abc'));
  check('server reports are held in memory', t.getServerReports().length === 1);
  const sec = t.renderReportsSection();
  check('moderation section merges the server report (marked server)', sec.includes('Server bug report here.') && sec.includes('server'));
  check('moderation section shows Backend: connected', sec.includes('Backend: connected'));
  check('moderation section shows the token-is-tab-only note', sec.includes('this tab only'));
  check('server resolve returns true + PATCHes the API', (() => {
    const n = fetchCalls.length;
    const ok = t.resolveReport('SRV-' + UUID_RESOLVABLE);
    return ok === true && fetchCalls.length === n + 1 && fetchCalls[fetchCalls.length - 1].method === 'PATCH';
  })());
  // Re-seed the in-memory server list (refresh is async; seed directly via a fresh GET)
  await run('refreshBackendReports()');
  await sleep(150);
  check('server list re-fetched after resolve flow', t.getServerReports().length === 1);
  check('server delete returns true + DELETEs the API (2)', (() => {
    const n = fetchCalls.length;
    const ok = t.deleteReport('SRV-' + UUID_RESOLVABLE);
    return ok === true && fetchCalls.length === n + 1 && fetchCalls[fetchCalls.length - 1].method === 'DELETE';
  })());
  check('unknown server id resolve returns false', t.resolveReport('SRV-00000000-0000-4000-8000-000000000000') === false);
  run(`forgetAdminToken()`);
  check('forgetAdminToken clears sessionStorage + memory list', t.getAdminToken() === null && !('loksewa_admin_token_v1' in sessionStore) && t.getServerReports().length === 0);
  // Local resolve/delete still work with the backend down (existing contract)
  fetchMode = 'throw'; resetUi();
  run(`submitGeneralReport('bug', 'A local-only report for moderation here.', {})`);
  const localId = store()[0].id;
  check('local resolve still works when backend is down', t.resolveReport(localId) === true && store()[0].status === 'resolved');
  check('local delete still works when backend is down', t.deleteReport(localId) === true && store().length === 0);
  // Status line when down (force a fresh health check in throw mode first)
  fetchMode = 'throw';
  await run('checkBackendHealth(true)');
  check('status line says not connected when backend is down', t.backendStatusLineHtml().includes('Backend: not connected'));
  // Token never in localStorage, never in source as a localStorage write
  const repSrcCheck = fs.readFileSync(path.join(root, 'assets/js/report.js'), 'utf8');
  check('report.js never writes the token to localStorage', !repSrcCheck.includes('localStorage.setItem(ADMIN_TOKEN') && !/lsSet\(ADMIN_TOKEN/.test(repSrcCheck));
  check('report.js keeps the token in sessionStorage', repSrcCheck.includes('sessionStorage.setItem(ADMIN_TOKEN_KEY'));
  check('report.js POST body carries no name or page URL', (() => {
    const start = repSrcCheck.indexOf('async function postReportToBackend');
    const end = repSrcCheck.indexOf('async function syncReportToBackend', start);
    const fn = repSrcCheck.slice(start, end);
    return fn.length > 0 && !fn.includes('currentUserName') && !fn.includes('location.href') && !fn.includes('window.location');
  })());
  check('report.js has no literal </script (bundle-safe)', !repSrcCheck.toLowerCase().includes('</script'));
  check('report.js has no literal asset path (bundle-safe)', !repSrcCheck.includes('assets/js/report.js'));

  console.log('\n' + pass + ' passed, ' + fail + ' failed');
  console.log(fail === 0 ? 'ALL BACKEND CHECKS PASSED ✔' : fail + ' BACKEND CHECK(S) FAILED ✘');
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => { console.error('BACKEND TEST CRASH:', e); process.exit(1); });
