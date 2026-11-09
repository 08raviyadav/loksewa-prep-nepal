/* Beta warning + Report an issue — report.js
   Own module; app.js calls renderBetaBanner() via typeof-guarded hooks
   (initial load, showView('home'), loadData(), setLang) so app.js works
   standalone if this file is absent.
   Backend (progressive enhancement): when the Vercel backend is up
   (/api/health says up), a submitted report is POSTed to /api/report and
   the success message says so ("Reported — the maintainer can see it").
   When the backend is down, offline, or absent, the report is saved in
   localStorage as before and the message says so honestly ("Saved on this
   device — will reach the maintainer once the backend is connected"), with
   the GitHub Issues button kept as the fallback channel. The site never
   depends on the backend: no fetch runs at load time, only from a user
   action (opening the form, submitting, connecting the admin token).
   Admin token (Review view) lives in sessionStorage only — never
   localStorage, never in the repo. Server reports are merged in memory
   only, never written to localStorage, so a report is never counted twice.
   No personal data is sent: only type, description and context. */

const BETA_DISMISSED = 'loksewa_beta_dismissed_v1';
const BETA_HIDE_DAYS = 7;
const BETA_HIDE_MS = BETA_HIDE_DAYS * 24 * 60 * 60 * 1000;
const REPORT_ISSUE_URL = 'https://github.com/08raviyadav/loksewa-prep-nepal/issues/new';
const APP_VERSION = 'beta'; // the web portal has no numeric version yet

const REPORT_TYPES = [
  { id: 'bug', en: 'Bug', ne: 'बग' },
  { id: 'wrong-info', en: 'Wrong information', ne: 'गलत जानकारी' },
  { id: 'wrong-question', en: 'Wrong question or answer', ne: 'गलत प्रश्न वा उत्तर' },
  { id: 'other', en: 'Other', ne: 'अन्य' },
];
// Same values as the old question-report form in app.js — kept in sync so
// the unified form and the old entries render with the same labels.
const QUESTION_REASONS = [
  { id: 'wrong-answer', en: 'Wrong answer', ne: 'गलत उत्तर' },
  { id: 'wrong-explanation', en: 'Wrong / misleading explanation', ne: 'गलत / भ्रमित व्याख्या' },
  { id: 'typo', en: 'Typo or unclear wording', ne: 'टाइपो वा अस्पष्ट शब्द' },
  { id: 'outdated', en: 'Outdated fact', ne: 'पुरानो तथ्य' },
  { id: 'duplicate', en: 'Duplicate of another question', ne: 'अर्को प्रश्नको नक्कल' },
  { id: 'other', en: 'Other', ne: 'अन्य' },
];

function reportTypeLabel(id){
  const t = REPORT_TYPES.find(x => x.id === id);
  return t ? B(t.en, t.ne) : B('Other', 'अन्य');
}
function reportTypeLabelEn(id){
  const t = REPORT_TYPES.find(x => x.id === id);
  return t ? t.en : 'Other';
}
function reportReasonLabel(id){
  const r = QUESTION_REASONS.find(x => x.id === id);
  return r ? B(r.en, r.ne) : (id || '');
}

/* ---------- Backend client (progressive enhancement) ---------- */
// The backend is an enhancement, not a dependency: every function here
// fails soft (returns false / null) when fetch is missing, the device is
// offline, or /api/health says down — the local save + GitHub fallback
// then carries the report, and the UI says so. No fetch runs at load time.
const REPORT_API = '/api/report';
const HEALTH_API = '/api/health';
const ADMIN_TOKEN_KEY = 'loksewa_admin_token_v1'; // sessionStorage ONLY
const BACKEND_CACHE_MS = 60 * 1000;
let _backendState = 'unknown'; // 'unknown' | 'up' | 'down' | 'offline'
let _backendCheckedAt = 0;
let _backendHealthPromise = null;
let _serverReports = []; // GET /api/report rows, memory only — never localStorage
let _adminAuthFailed = false;

function backendState(){ return _backendState; }
function getServerReports(){ return _serverReports; }
function isOnline(){
  try { return typeof navigator === 'undefined' || navigator.onLine !== false; }
  catch (e) { return true; }
}
function hasFetch(){ return typeof fetch === 'function'; }
// fetch with a timeout; setTimeout/AbortController are guarded so the
// vm sandboxes in the test suites (which stub them) keep working.
function fetchWithTimeout(url, opts, ms){
  if (typeof AbortController !== 'undefined' && typeof setTimeout === 'function') {
    const ctrl = new AbortController();
    const timer = setTimeout(function(){ try { ctrl.abort(); } catch (e) {} }, ms || 5000);
    const p = fetch(url, Object.assign({}, opts, { signal: ctrl.signal }));
    return p.then(function(r){ clearTimeout(timer); return r; }, function(e){ clearTimeout(timer); throw e; });
  }
  return fetch(url, opts);
}
function checkBackendHealth(force){
  const now = Date.now();
  if (!isOnline()) { _backendState = 'offline'; _backendHealthPromise = Promise.resolve(false); _backendCheckedAt = now; return _backendHealthPromise; }
  if (!force && _backendHealthPromise && (now - _backendCheckedAt) < BACKEND_CACHE_MS) return _backendHealthPromise;
  _backendCheckedAt = now;
  if (!hasFetch()) { _backendState = 'down'; _backendHealthPromise = Promise.resolve(false); return _backendHealthPromise; }
  _backendHealthPromise = fetchWithTimeout(HEALTH_API, { cache: 'no-store' }, 5000).then(function(res){
    return res.json().catch(function(){ return null; });
  }).then(function(data){
    _backendState = (data && data.ok === true && data.db === 'up') ? 'up' : 'down';
    return _backendState === 'up';
  }).catch(function(){
    _backendState = 'down';
    return false;
  });
  return _backendHealthPromise;
}
// Admin token: sessionStorage only — forgotten when the tab closes, never
// written to localStorage, never logged, never put in a URL.
function getAdminToken(){
  try {
    if (typeof sessionStorage !== 'undefined' && sessionStorage.getItem) return sessionStorage.getItem(ADMIN_TOKEN_KEY);
  } catch (e) {}
  return null;
}
function setAdminToken(t){
  try {
    if (typeof sessionStorage === 'undefined') return false;
    if (t) sessionStorage.setItem(ADMIN_TOKEN_KEY, t); else sessionStorage.removeItem(ADMIN_TOKEN_KEY);
    return true;
  } catch (e) { return false; }
}
function backendSentMessage(){ return B('Reported — the maintainer can see it.', 'रिपोर्ट गरियो — मेन्टेनरले देख्न सक्नुहुन्छ।'); }
function backendLocalMessage(){ return B('Saved on this device — will reach the maintainer once the backend is connected.', 'यो डिभाइसमा सेभ भयो — ब्याकएन्ड जोडिएपछि मेन्टेनरसम्म पुग्नेछ।'); }
function updateBackendStatusLine(sent){
  try {
    const el = document.getElementById('iss-backend-status');
    if (el) el.textContent = sent ? backendSentMessage() : backendLocalMessage();
  } catch (e) {}
}
function markEntrySynced(localId, serverId){
  try {
    const list = loadReports();
    const r = list.find(function(x){ return x && x.id === localId; });
    if (r) { r.synced = true; r.serverId = serverId || null; saveReports(list); }
    return r || null;
  } catch (e) { return null; }
}
// POST one local entry to the backend. Returns { ok, serverId? } — never
// throws, so the caller can fire-and-forget it after the local save.
async function postReportToBackend(entry){
  try {
    if (!isOnline() || !hasFetch()) return { ok: false, reason: 'offline' };
    const up = await checkBackendHealth();
    if (!up) return { ok: false, reason: 'down' };
    const ctx = entry.context || {};
    const res = await fetchWithTimeout(REPORT_API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type: entry.type || 'wrong-question',
        description: entry.description || entry.comment || '',
        context: ctx,
        questionId: entry.questionId || ctx.questionId || null,
        reason: entry.reason || ctx.reason || null
      })
    }, 8000);
    if (!res.ok) return { ok: false, reason: 'http', status: res.status };
    const data = await res.json().catch(function(){ return null; });
    return { ok: true, serverId: (data && data.id) ? data.id : null };
  } catch (e) {
    return { ok: false, reason: 'error' };
  }
}
// Fire-and-forget after the local save: local entry is the record of the
// report, the backend copy is the delivery. One call per submit — the
// local save happens exactly once, so a retry here can never double-save.
async function syncReportToBackend(entry){
  try {
    if (!entry) return { ok: false, reason: 'no-entry' };
    const res = await postReportToBackend(entry);
    if (res.ok) markEntrySynced(entry.id, res.serverId);
    updateBackendStatusLine(res.ok);
    return res;
  } catch (e) {
    updateBackendStatusLine(false);
    return { ok: false, reason: 'error' };
  }
}
// Admin: list server reports (status=all). Returns { ok, count?, reason? }.
async function refreshBackendReports(){
  try {
    if (!isOnline() || !hasFetch()) { if (!isOnline()) _backendState = 'offline'; if (typeof renderModerate === 'function') renderModerate(); return { ok: false, reason: 'offline' }; }
    const up = await checkBackendHealth();
    if (!up) { if (typeof renderModerate === 'function') renderModerate(); return { ok: false, reason: 'down' }; }
    const token = getAdminToken();
    if (!token) { if (typeof renderModerate === 'function') renderModerate(); return { ok: false, reason: 'no-token' }; }
    const res = await fetchWithTimeout(REPORT_API + '?status=all&limit=200', { headers: { 'Authorization': 'Bearer ' + token } }, 8000);
    if (res.status === 401 || res.status === 403) { _serverReports = []; _adminAuthFailed = true; if (typeof renderModerate === 'function') renderModerate(); return { ok: false, reason: 'unauthorized' }; }
    if (!res.ok) { if (typeof renderModerate === 'function') renderModerate(); return { ok: false, reason: 'http', status: res.status }; }
    const data = await res.json().catch(function(){ return null; });
    _serverReports = (data && Array.isArray(data.reports)) ? data.reports : [];
    _adminAuthFailed = false;
    if (typeof renderModerate === 'function') renderModerate();
    return { ok: true, count: _serverReports.length };
  } catch (e) {
    if (typeof renderModerate === 'function') { try { renderModerate(); } catch (e2) {} }
    return { ok: false, reason: 'error' };
  }
}
function connectAdminToken(){
  try {
    const input = document.getElementById('admin-token');
    const v = input ? String(input.value || '').trim() : '';
    if (!v) return false;
    setAdminToken(v);
    if (input) input.value = '';
    refreshBackendReports();
    return true;
  } catch (e) { return false; }
}
function forgetAdminToken(){
  setAdminToken(null);
  _serverReports = [];
  _adminAuthFailed = false;
  if (typeof renderModerate === 'function') renderModerate();
}
// Admin: resolve / delete one SERVER report. Returns a promise of bool;
// the caller optimistically updates the in-memory list first.
async function backendResolveReport(serverId){
  try {
    const token = getAdminToken(); if (!token) return false;
    const res = await fetchWithTimeout(REPORT_API + '?id=' + encodeURIComponent(serverId), {
      method: 'PATCH', headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
      body: JSON.stringify({ status: 'resolved' })
    }, 8000);
    return !!res.ok;
  } catch (e) { return false; }
}
async function backendDeleteReport(serverId){
  try {
    const token = getAdminToken(); if (!token) return false;
    const res = await fetchWithTimeout(REPORT_API + '?id=' + encodeURIComponent(serverId), {
      method: 'DELETE', headers: { 'Authorization': 'Bearer ' + token }
    }, 8000);
    return !!res.ok;
  } catch (e) { return false; }
}
function backendStatusLineHtml(){
  if (_backendState === 'up' && getAdminToken()) return B('Backend: connected ✓ — new reports reach the maintainer, and server reports are shown below.', 'ब्याकएन्ड: जडान भयो ✓ — नयाँ रिपोर्टहरू मेन्टेनरसम्म पुग्छन्, र सर्भरका रिपोर्टहरू तल देखाइएका छन्।');
  if (_backendState === 'up') return B('Backend: connected ✓ — new reports reach the maintainer. Enter the admin token below to see server reports.', 'ब्याकएन्ड: जडान भयो ✓ — नयाँ रिपोर्टहरू मेन्टेनरसम्म पुग्छन्। सर्भरका रिपोर्टहरू हेर्न तल एडमिन टोकन हाल्नुहोस्।');
  if (_backendState === 'offline') return B('Backend: not checked — you are offline. Reports stay on this device for now.', 'ब्याकएन्ड: जाँच भएन — तपाईं अफलाइन हुनुहुन्छ। रिपोर्टहरू अहिले यो डिभाइसमा मात्र रहन्छन्।');
  if (_backendState === 'down') return B('Backend: not connected — reports stay on this device; use GitHub to send them to the maintainer.', 'ब्याकएन्ड: जडान छैन — रिपोर्टहरू यो डिभाइसमा मात्र रहन्छन्; मेन्टेनरसम्म पठाउन GitHub प्रयोग गर्नुहोस्।');
  return B('Backend: not checked yet — new reports are saved on this device until the backend is connected.', 'ब्याकएन्ड: अझै जाँच भएको छैन — ब्याकएन्ड जोडिएसम्म नयाँ रिपोर्टहरू यो डिभाइसमा सेभ हुन्छन्।');
}
function adminTokenBlockHtml(){
  if (getAdminToken()) {
    return `<p class="muted">${B('Admin token saved for this tab only — it is forgotten when the tab closes.', 'एडमिन टोकन यो ट्याबका लागि मात्र सेभ छ — ट्याब बन्द हुँदा बिर्सिन्छ।')} <button class="btn secondary" onclick="refreshBackendReports()">↻ ${B('Refresh server reports', 'सर्भर रिपोर्टहरू रिफ्रेस गर्नुहोस्')}</button> <button class="btn secondary" onclick="forgetAdminToken()">${B('Forget token', 'टोकन बिर्सनुहोस्')}</button>${_adminAuthFailed ? ' <span class="error-text">' + B('That token was rejected — check the ADMIN_TOKEN value in Vercel.', 'त्यो टोकन अस्वीकृत भयो — Vercel मा ADMIN_TOKEN मान जाँच्नुहोस्।') + '</span>' : ''}</p>`;
  }
  return `<p><label for="admin-token">${B('Admin token', 'एडमिन टोकन')}</label> <input type="password" id="admin-token" autocomplete="off" placeholder="${B('Paste the ADMIN_TOKEN from Vercel', 'Vercel बाट ADMIN_TOKEN हाल्नुहोस्')}" style="max-width:320px"> <button class="btn secondary" onclick="connectAdminToken()">${B('Connect backend', 'ब्याकएन्ड जोड्नुहोस्')}</button><br><span class="muted">${B('The token is kept in this tab only (sessionStorage) — never saved on the device or in the repo.', 'टोकन यो ट्याबमा मात्र राखिन्छ (sessionStorage) — डिभाइसमा वा रिपोमा कहिल्यै सेभ हुँदैन।')}</span></p>`;
}

/* ---------- Beta banner ---------- */
// Pure (takes nowMs so tests can move the clock): show when never dismissed,
// or when the dismissal is older than BETA_HIDE_DAYS.
function betaShouldShow(nowMs){
  const d = lsGet(BETA_DISMISSED, null);
  if (!d) return true;
  const t = Date.parse(d);
  if (isNaN(t)) return true;
  return (nowMs - t) > BETA_HIDE_MS;
}
function dismissBetaBanner(){
  lsSet(BETA_DISMISSED, new Date().toISOString());
  renderBetaBanner();
}
function renderBetaBanner(){
  const box = document.getElementById('beta-banner'); if (!box) return;
  if (!betaShouldShow(Date.now())) { box.innerHTML = ''; return; }
  box.innerHTML = `<div class="beta-banner" role="note">
    <div class="beta-banner-main"><strong>${B('⚠️ Beta — this website is still in beta', '⚠️ बिटा — यो वेबसाइट अझै बिटा चरणमा छ')}</strong><br>
    <span>${B('If you find a bug, wrong information, or a wrong question/answer, please report it — it helps everyone studying here.', 'यदि तपाईंले बग, गलत जानकारी, वा गलत प्रश्न/उत्तर फेला पार्नुभयो भने कृपया रिपोर्ट गर्नुहोस् — यसले यहाँ अध्ययन गर्ने सबैलाई मद्दत गर्छ।')}</span></div>
    <div class="beta-banner-actions">
      <button class="btn" onclick="openIssueForm()">${B('Report an issue', 'समस्या रिपोर्ट गर्नुहोस्')}</button>
      <button class="btn secondary beta-dismiss" onclick="dismissBetaBanner()" aria-label="${B('Dismiss', 'बन्द गर्नुहोस्')}">✕</button>
    </div></div>`;
}

/* ---------- Report store ---------- */
function loadReports(){ return lsGet(LS_REPORTS, []); }
function saveReports(list){ lsSet(LS_REPORTS, list); }
function validateReport(type, description){
  if (!REPORT_TYPES.some(t => t.id === type)) return { ok: false, error: B('Please choose what kind of issue this is.', 'कृपया यो कस्तो समस्या हो छान्नुहोस्।') };
  const d = String(description || '').trim();
  if (d.length < 10) return { ok: false, error: B('Please describe the issue in at least 10 characters — what is wrong and where did you see it?', 'कृपया समस्या कम्तीमा १० अक्षरमा वर्णन गर्नुहोस् — के गलत छ र कहाँ देख्नुभयो?') };
  return { ok: true };
}
function currentViewName(){
  try {
    const el = document.querySelector('.view.active');
    if (el && el.id) return el.id.replace(/^view-/, '');
  } catch (e) {}
  return 'unknown';
}
function findQuestion(id){
  try {
    if (typeof QUESTIONS !== 'undefined' && QUESTIONS) return QUESTIONS.find(q => q && q.id === id) || null;
  } catch (e) {}
  return null;
}

/* ---------- Unified report form (modal) ---------- */
// ctx: { questionId?, exam?, topic? }. Question context is looked up from
// the bank so exam/topic are auto-filled; general reports carry only the view.
let _issueCtx = null;
function openIssueForm(ctx){
  ctx = ctx || {};
  const q = ctx.questionId ? findQuestion(ctx.questionId) : null;
  _issueCtx = {
    questionId: ctx.questionId || null,
    exam: q && q.exam ? (Array.isArray(q.exam) ? q.exam.join(', ') : String(q.exam)) : (ctx.exam || null),
    topic: q ? (q.topic || null) : (ctx.topic || null),
    view: currentViewName()
  };
  const m = document.getElementById('modal'), b = document.getElementById('modal-body');
  if (!m || !b) return;
  const typeOpts = REPORT_TYPES.map(t => `<option value="${t.id}"${t.id === 'wrong-question' && _issueCtx.questionId ? ' selected' : ''}>${esc(B(t.en, t.ne))}</option>`).join('');
  const reasonOpts = QUESTION_REASONS.map(r => `<option value="${r.id}">${esc(B(r.en, r.ne))}</option>`).join('');
  b.innerHTML = `<h3>${B('Report an issue', 'समस्या रिपोर्ट गर्नुहोस्')}</h3>
    ${_issueCtx.questionId ? `<p class="muted">${B('Question', 'प्रश्न')}: <strong>${esc(_issueCtx.questionId)}</strong>${_issueCtx.topic ? ' · ' + esc(_issueCtx.topic) : ''}${_issueCtx.exam ? ' · ' + esc(_issueCtx.exam) : ''}</p>` : ''}
    <p class="muted" id="iss-backend-note">${_backendState === 'up' ? B('Reports are sent straight to the maintainer.', 'रिपोर्टहरू सिधै मेन्टेनरसम्म पठाइन्छ।') : B('Reports are saved on this device. To reach the maintainer, use the GitHub button after submitting.', 'रिपोर्टहरू यो डिभाइसमा सेभ हुन्छन्। मेन्टेनरसम्म पुर्‍याउन पेस गरेपछि GitHub बटन प्रयोग गर्नुहोस्।')}</p>
    <label for="iss-type">${B('What kind of issue is this?', 'यो कस्तो समस्या हो?')}</label>
    <select id="iss-type">${typeOpts}</select>
    ${_issueCtx.questionId ? `<label for="iss-reason">${B('What is wrong with the question?', 'प्रश्नमा के गलत छ?')}</label>
    <select id="iss-reason">${reasonOpts}</select>` : ''}
    <label for="iss-desc">${B('Describe the issue', 'समस्या वर्णन गर्नुहोस्')}</label>
    <textarea id="iss-desc" rows="4" placeholder="${B('e.g. The question about the Sugauli Treaty says 1815 — the treaty was signed in 1816.', 'उदा. सुगौली सन्धिबारेको प्रश्नमा १८१५ भनिएको छ — सन्धि १८१६ मा भएको थियो।')}"></textarea>
    <input type="text" id="iss-website" name="website" autocomplete="off" tabindex="-1" aria-hidden="true" style="display:none">
    <p class="error-text" id="iss-error"></p>
    <button class="btn" onclick="submitIssueForm()">${B('Submit report', 'रिपोर्ट पेस गर्नुहोस्')}</button>
    <button class="btn secondary" onclick="closeModal()">${B('Cancel', 'रद्द गर्नुहोस्')}</button>`;
  m.hidden = false;
  // User-initiated check only (never at load): if the backend is up, say
  // so in the form note before the visitor types.
  try {
    checkBackendHealth().then(function(up){
      if (!up) return;
      const n = document.getElementById('iss-backend-note');
      if (n) n.textContent = B('Reports are sent straight to the maintainer.', 'रिपोर्टहरू सिधै मेन्टेनरसम्म पठाइन्छ।');
    }).catch(function(){});
  } catch (e) {}
}
function submitGeneralReport(type, description, ctx){
  const v = validateReport(type, description);
  if (!v.ok) return null;
  const entry = {
    id: uid('REP'), kind: 'general', type,
    description: String(description).trim(),
    context: {
      view: (ctx && ctx.view) || currentViewName(),
      questionId: (ctx && ctx.questionId) || null,
      exam: (ctx && ctx.exam) || null,
      topic: (ctx && ctx.topic) || null
    },
    by: (typeof currentUserName === 'function') ? currentUserName() : 'Guest',
    at: nowIso(), status: 'open', synced: false, serverId: null
  };
  const list = loadReports(); list.push(entry); saveReports(list);
  return entry;
}
function submitIssueForm(){
  const t = document.getElementById('iss-type'); const type = t ? t.value : '';
  const d = document.getElementById('iss-desc'); const desc = d ? d.value.trim() : '';
  const err = document.getElementById('iss-error');
  // Honeypot: a filled hidden "website" field means a bot. Drop the
  // submission silently (no save, no backend call) and show a generic
  // thanks — a human never sees this branch.
  const hp = document.getElementById('iss-website');
  if (hp && String(hp.value || '').trim() !== '') {
    const b = document.getElementById('modal-body');
    if (b) b.innerHTML = `<h3>${B('Thanks — report saved', 'धन्यवाद — रिपोर्ट सेभ भयो')}</h3><p>${backendLocalMessage()}</p><p><button class="btn secondary" onclick="closeModal()">${B('Done', 'सम्पन्न')}</button></p>`;
    return true;
  }
  const v = validateReport(type, desc);
  if (!v.ok) { if (err) err.textContent = v.error; return false; }
  let saved = null;
  if (_issueCtx && _issueCtx.questionId) {
    // Question reports go through the existing submitReport() so the
    // stored shape (questionId/reason/comment) stays compatible with the
    // moderation view and the old entries already on devices.
    const r = document.getElementById('iss-reason'); const reason = r ? r.value : 'other';
    if (typeof submitReport === 'function' && submitReport(_issueCtx.questionId, reason, desc, 'wrong-question')) {
      const list = loadReports(); saved = list[list.length - 1];
      // submitReport stores the question shape only; enrich the saved entry
      // with the auto-filled context so the GitHub link and the moderation
      // view can show the exam/topic (submitReport's own contract is
      // untouched — test-v2 depends on it).
      if (saved) {
        saved.context = { view: _issueCtx.view || currentViewName(), questionId: _issueCtx.questionId, exam: _issueCtx.exam || null, topic: _issueCtx.topic || null, reason: saved.reason || null };
        saved.synced = false; saved.serverId = null;
        saveReports(list);
      }
    } else {
      if (err) err.textContent = B('Could not save the report — please add a description.', 'रिपोर्ट सेभ गर्न सकिएन — कृपया विवरण थप्नुहोस्।');
      return false;
    }
  } else {
    saved = submitGeneralReport(type, desc, _issueCtx || {});
    if (!saved) { if (err) err.textContent = B('Could not save the report.', 'रिपोर्ट सेभ गर्न सकिएन।'); return false; }
  }
  showIssueSuccess(saved);
  // Local save already happened exactly once above; the backend attempt is
  // fire-and-forget and only ever marks that same entry as synced.
  try { const p = syncReportToBackend(saved); if (p && p.catch) p.catch(function(){}); } catch (e) {}
  return true;
}
function showIssueSuccess(saved){
  const m = document.getElementById('modal'); if (m) m.hidden = false; // the question path closes the modal in submitReport(); the success state must still be seen
  const b = document.getElementById('modal-body'); if (!b) return;
  b.innerHTML = `<h3>${B('Thanks — report saved', 'धन्यवाद — रिपोर्ट सेभ भयो')}</h3>
    <p id="iss-backend-status">${_backendState === 'up' ? B('Sending to the maintainer…', 'मेन्टेनरसम्म पठाउँदै…') : backendLocalMessage()}</p>
    <p>${B('If the backend is not connected, the GitHub button below is how the report reaches the maintainer — it takes one click.', 'ब्याकएन्ड जडान नभएको खण्डमा तलको GitHub बटनबाट रिपोर्ट मेन्टेनरसम्म पुग्छ — एक क्लिकमा हुन्छ।')}</p>
    <p><button class="btn" onclick="reportOnGithub('${esc(saved.id)}')">↗ ${B('Report on GitHub', 'GitHub मा रिपोर्ट गर्नुहोस्')}</button>
    <button class="btn secondary" onclick="closeModal()">${B('Done', 'सम्पन्न')}</button></p>
    <p class="muted">${B('Reference', 'सन्दर्भ')}: ${esc(saved.id)} · ${esc(reportTypeLabel(saved.type))}</p>`;
}

/* ---------- GitHub reporting channel ---------- */
// Pure URL builder: GitHub pre-fills /issues/new from ?title= &body=.
// Deliberately contains NO personal data: no reporter name, no page URL —
// only the issue type, the description the visitor typed, the (question)
// context, and the app version.
function buildGithubIssueUrl(r){
  const typeLabel = reportTypeLabelEn(r.type || 'wrong-question');
  const desc = String(r.description || r.comment || '').trim();
  const short = desc.replace(/\s+/g, ' ').slice(0, 60);
  const title = '[Report] ' + typeLabel + (short ? ': ' + short : '');
  const ctx = r.context || {};
  const qid = r.questionId || ctx.questionId;
  const lines = [
    'Type: ' + typeLabel,
    '',
    'Description:',
    desc,
    '',
    'Context:',
    '- View: ' + (ctx.view || 'unknown')
  ];
  if (qid) lines.push('- Question: ' + qid + (ctx.exam ? ' (' + ctx.exam + ')' : '') + (ctx.topic ? ' — ' + ctx.topic : ''));
  lines.push('- App: LokSewa Vidyapeeth (web, ' + APP_VERSION + ')', '', '_Reported from the in-app report form. The local save stays on the visitor’s device — this GitHub issue is how it reaches the maintainer._');
  return REPORT_ISSUE_URL + '?title=' + encodeURIComponent(title) + '&body=' + encodeURIComponent(lines.join('\n'));
}
function reportOnGithub(id){
  const r = loadReports().find(x => x && x.id === id);
  if (!r) return null;
  const url = buildGithubIssueUrl(r);
  if (typeof window !== 'undefined' && window.open) window.open(url, '_blank');
  return url;
}

/* ---------- Moderation: resolve / delete + reports section ---------- */
// Server reports render with id 'SRV-<uuid>' and live in _serverReports
// (memory only). Resolving/deleting one calls the API; the in-memory row
// is updated optimistically and the view re-renders. Local reports keep
// the old synchronous contract (test-report / test-v2 depend on it).
function isServerReportId(id){ return typeof id === 'string' && id.indexOf('SRV-') === 0; }
function resolveReport(id){
  if (isServerReportId(id)) {
    const sid = id.slice(4);
    const r = _serverReports.find(function(x){ return x && x.id === sid; });
    if (!r) return false;
    r.status = 'resolved'; r.resolved_at = new Date().toISOString();
    try { const p = backendResolveReport(sid); if (p && p.catch) p.catch(function(){}); } catch (e) {}
    if (typeof renderModerate === 'function') renderModerate();
    return true;
  }
  const list = loadReports(); const r = list.find(x => x && x.id === id);
  if (!r) return false;
  r.status = 'resolved'; saveReports(list);
  if (typeof renderModerate === 'function') renderModerate();
  return true;
}
function deleteReport(id){
  if (isServerReportId(id)) {
    const sid = id.slice(4);
    const before = _serverReports.length;
    _serverReports = _serverReports.filter(function(x){ return !(x && x.id === sid); });
    if (_serverReports.length === before) return false;
    try { const p = backendDeleteReport(sid); if (p && p.catch) p.catch(function(){}); } catch (e) {}
    if (typeof renderModerate === 'function') renderModerate();
    return true;
  }
  const list = loadReports();
  const kept = list.filter(x => x && x.id !== id);
  if (kept.length === list.length) return false;
  saveReports(kept);
  if (typeof renderModerate === 'function') renderModerate();
  return true;
}
// Unified list for the moderation view: all open reports (general + wrong
// question), newest last. Old entries without kind/type render as
// wrong-question reports (the shape submitReport stored before this file).
// Server reports (when an admin token is connected) are merged in-memory:
// a local entry already synced to the server (same serverId) is shown once,
// as the server copy.
function renderReportsSection(){
  const all = loadReports();
  const serverIds = new Set(_serverReports.map(function(r){ return r && r.id; }));
  const localOpen = all.filter(function(r){ return r && r.status === 'open' && !(r.serverId && serverIds.has(r.serverId)); });
  const serverOpen = _serverReports.filter(function(r){ return r && r.status === 'open'; });
  const localResolved = all.filter(function(r){ return r && r.status !== 'open'; }).length;
  const serverResolved = _serverReports.filter(function(r){ return r && r.status !== 'open'; }).length;
  const openCount = localOpen.length + serverOpen.length;
  const resolvedCount = localResolved + serverResolved;
  const rows = localOpen.map(function(r){
    const qid = r.questionId || (r.context && r.context.questionId);
    const isQ = r.kind === 'question' || !!qid;
    const title = isQ ? (qid || B('Question', 'प्रश्न')) : reportTypeLabel(r.type);
    const sub = isQ && r.reason ? reportReasonLabel(r.reason) : '';
    const desc = r.description || r.comment || '';
    const view = r.context && r.context.view ? ' · ' + B('view', 'भ्यु') + ': ' + r.context.view : '';
    const synced = r.synced ? ' · ✓ ' + B('sent to backend', 'ब्याकएन्डमा पठाइयो') : '';
    return `<div class="card"><strong>${esc(title)}</strong>${sub ? ' — ' + esc(sub) : ''} · <span class="muted">${esc(reportTypeLabel(r.type || 'wrong-question'))}</span><br>${esc(desc)}<br><span class="muted">${B('by', '—')} ${esc(r.by || 'Guest')} · ${esc((r.at || '').slice(0, 10))}${esc(view)}${esc(synced)}</span><br><button class="btn secondary" onclick="resolveReport('${esc(r.id)}')">✓ ${B('Resolve', 'समाधान भयो')}</button> <button class="btn danger" onclick="deleteReport('${esc(r.id)}')">✕ ${B('Delete', 'मेटाउनुहोस्')}</button></div>`;
  }).join('');
  const serverRows = serverOpen.map(function(r){
    const ctx = r.context || {};
    const qid = ctx.questionId;
    const isQ = (r.type === 'wrong-question') || !!qid;
    const title = isQ ? (qid || B('Question', 'प्रश्न')) : reportTypeLabel(r.type);
    const sub = isQ && ctx.reason ? reportReasonLabel(ctx.reason) : '';
    const desc = r.description || '';
    const view = ctx.view ? ' · ' + B('view', 'भ्यु') + ': ' + ctx.view : '';
    return `<div class="card"><strong>${esc(title)}</strong>${sub ? ' — ' + esc(sub) : ''} · <span class="muted">${esc(reportTypeLabel(r.type || 'wrong-question'))} · 🌐 ${B('server', 'सर्भर')}</span><br>${esc(desc)}<br><span class="muted">${esc((r.created_at || '').slice(0, 10))}${esc(view)}</span><br><button class="btn secondary" onclick="resolveReport('SRV-${esc(r.id)}')">✓ ${B('Resolve', 'समाधान भयो')}</button> <button class="btn danger" onclick="deleteReport('SRV-${esc(r.id)}')">✕ ${B('Delete', 'मेटाउनुहोस्')}</button></div>`;
  }).join('');
  return `<h3>${B('Reports', 'रिपोर्टहरू')} (${openCount} ${B('open', 'खुला')}${resolvedCount ? ' · ' + resolvedCount + ' ' + B('resolved', 'समाधान') : ''})</h3><p class="muted" id="backend-status-line">${backendStatusLineHtml()}</p>${adminTokenBlockHtml()}${openCount ? rows + serverRows : '<p class="muted">' + B('No open reports.', 'कुनै खुला रिपोर्ट छैन।') + '</p>'}`;
}
