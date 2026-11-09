/* Beta warning + Report an issue checks: banner show/dismiss/reappear,
   report validation, localStorage round-trip, moderation resolve/delete,
   GitHub issue URL builder (encoding, no PII), question-report context
   capture, and HTML/CSS/bundle wiring.
   Node, no deps. Usage: node scripts/test-report.js */
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

// --- 1. Load app.js + report.js in a sandbox with a FIXED clock ---------
// Fixed clock: 2026-11-09 12:00 UTC (Gai Tihar day, Kartik 23, 2083).
const FIXED_NOW = Date.UTC(2026, 10, 9, 12, 0, 0);
const DAY = 24 * 60 * 60 * 1000;
function fakeEl(id){
  return { id, innerHTML: '', hidden: false, textContent: '', value: '',
    classList: { _s: new Set(), contains(c){ return this._s.has(c); }, add(c){ this._s.add(c); }, remove(c){ this._s.delete(c); } },
    style: {}, dataset: {}, appendChild(){}, setAttribute(){}, addEventListener(){},
    querySelector(){ return null; }, querySelectorAll(){ return []; } };
}
const elStore = {};
const opened = [];
const sandbox = {
  module: { exports: {} }, console,
  Date: class extends Date { static now() { return FIXED_NOW; } },
  localStorage: { _s: {}, getItem(k) { return (k in this._s) ? this._s[k] : null; }, setItem(k, v) { this._s[k] = String(v); }, removeItem(k) { delete this._s[k]; } },
  document: { addEventListener: () => {}, querySelector: () => null, querySelectorAll: () => [],
    getElementById(id) { if (!elStore[id]) elStore[id] = fakeEl(id); return elStore[id]; },
    createElement(tag) { return fakeEl(tag); }, documentElement: { dataset: {} } },
  window: {}, alert: () => {}, fetch: async () => { throw new Error('no fetch in test'); },
  scrollTo: () => {}, setInterval: () => 0, clearInterval: () => {}, setTimeout: (fn) => 0, clearTimeout: () => {},
  Notification: undefined, matchMedia: undefined,
  open(url) { opened.push(url); return null; }
};
sandbox.window = sandbox;
vm.createContext(sandbox);
const appSrc = fs.readFileSync(path.join(root, 'assets/js/app.js'), 'utf8');
const repSrc = fs.readFileSync(path.join(root, 'assets/js/report.js'), 'utf8');
try {
  vm.runInContext(appSrc, sandbox);
  vm.runInContext(repSrc + '\nmodule.exports={B,setLang,getLang,betaShouldShow,dismissBetaBanner,renderBetaBanner,validateReport,submitGeneralReport,openIssueForm,submitIssueForm,buildGithubIssueUrl,reportOnGithub,resolveReport,deleteReport,renderReportsSection,loadReports,saveReports,reportTypeLabel,currentViewName,openReportForm,submitReport,closeModal,BETA_DISMISSED,REPORT_ISSUE_URL};', sandbox);
  check('app.js + report.js parse', true);
} catch (e) { check('app.js + report.js parse', false, e.message); process.exit(1); }
const t = sandbox.module.exports;
const run = code => vm.runInContext(code, sandbox);
const el = id => elStore[id] || (elStore[id] = fakeEl(id));
const store = () => JSON.parse(sandbox.localStorage._s['loksewa_reports_v1'] || '[]');

// --- 2. Beta banner show / dismiss / reappear ----------------------------
check('beta shows when never dismissed', t.betaShouldShow(FIXED_NOW));
run(`localStorage.setItem('loksewa_beta_dismissed_v1', JSON.stringify(new Date(${FIXED_NOW}).toISOString()))`);
check('beta hidden right after dismiss', !t.betaShouldShow(FIXED_NOW));
check('beta still hidden 6 days later', !t.betaShouldShow(FIXED_NOW + 6 * DAY));
check('beta hidden at exactly 7 days (strictly older)', !t.betaShouldShow(FIXED_NOW + 7 * DAY));
check('beta shows again 8 days later', t.betaShouldShow(FIXED_NOW + 8 * DAY));
run(`localStorage.setItem('loksewa_beta_dismissed_v1', JSON.stringify('not-a-date'))`);
check('beta shows on garbage dismissal value', t.betaShouldShow(FIXED_NOW));
run(`localStorage.removeItem('loksewa_beta_dismissed_v1')`);

run('renderBetaBanner()');
check('banner renders with beta text + report button', el('beta-banner').innerHTML.includes('Beta') && el('beta-banner').innerHTML.includes('Report an issue'));
run('dismissBetaBanner()');
check('dismiss hides the banner', el('beta-banner').innerHTML === '');
check('dismiss stores the date', !!sandbox.localStorage._s['loksewa_beta_dismissed_v1']);
run('renderBetaBanner()');
check('banner stays hidden after dismiss', el('beta-banner').innerHTML === '');
run(`localStorage.setItem('loksewa_beta_dismissed_v1', JSON.stringify(new Date(${FIXED_NOW} - 8 * ${DAY}).toISOString()))`);
run('renderBetaBanner()');
check('banner reappears after 8 days', el('beta-banner').innerHTML.includes('Beta'));
run(`localStorage.removeItem('loksewa_beta_dismissed_v1')`);
run('setLang("ne")');
run('renderBetaBanner()');
check('banner renders in Nepali', el('beta-banner').innerHTML.includes('बिटा'));
run('setLang("en")');

// --- 3. Report validation -------------------------------------------------
check('validate rejects unknown type', !t.validateReport('nope', 'a long enough description').ok);
check('validate rejects empty description', !t.validateReport('bug', '').ok);
check('validate rejects whitespace description', !t.validateReport('bug', '     ').ok);
check('validate rejects 9-char description', !t.validateReport('bug', '123456789').ok);
check('validate accepts exactly 10 chars', t.validateReport('bug', '1234567890').ok);
check('validate accepts all four types', ['bug', 'wrong-info', 'wrong-question', 'other'].every(x => t.validateReport(x, 'a long enough description').ok));

// --- 4. General report save / round-trip ----------------------------------
run(`localStorage.removeItem('loksewa_reports_v1')`);
const saved = run(`submitGeneralReport('bug', 'The mock timer keeps running after submit.', {})`);
check('general report saves and returns the entry', saved && saved.id && saved.kind === 'general' && saved.type === 'bug' && saved.status === 'open');
check('general report stores context view + no PII name in entry', saved && saved.context && saved.context.view === 'unknown');
check('general report is in localStorage', store().length === 1);
check('invalid general report saves nothing', run(`submitGeneralReport('bug', 'short', {})`) === null && store().length === 1);

// --- 5. GitHub issue URL builder (encoding, no PII) -----------------------
const url = t.buildGithubIssueUrl(store()[0]);
check('github URL starts with the issues/new endpoint', url.startsWith(t.REPORT_ISSUE_URL + '?title='));
check('github title carries the type + short description', url.includes(encodeURIComponent('[Report] Bug: The mock timer keeps running')));
check('github body carries the description', url.includes(encodeURIComponent('The mock timer keeps running after submit.')));
check('github URL contains no reporter name (no PII)', !url.includes('Guest'));
check('github URL contains no page URL', !url.includes('github.io') && !url.includes('vercel.app'));
check('github URL carries the app version', url.includes(encodeURIComponent('LokSewa Vidyapeeth (web, beta)')));
const tricky = t.buildGithubIssueUrl({ type: 'wrong-info', description: 'Fix A & B? #test <tag>', context: { view: 'practice' }, comment: '' });
check('github URL encodes & ? # < >', !tricky.includes('A & B') && tricky.includes('A%20%26%20B') && tricky.includes('%23test') && tricky.includes('%3Ctag%3E'));
check('reportOnGithub opens the URL once', (() => { opened.length = 0; const u = t.reportOnGithub(store()[0].id); return u === url && opened.length === 1 && opened[0] === url; })());
check('reportOnGithub on unknown id returns null', t.reportOnGithub('REP-nope') === null);

// --- 6. Unified form: general path (fake DOM) -----------------------------
el('iss-type').value = 'wrong-info';
el('iss-desc').value = 'The Constitution article count on the guide page says 308 articles but the summary says 307.';
check('unified form submits a general report', run('submitIssueForm()') === true && store().length === 2);
check('success state shows GitHub button', el('modal-body').innerHTML.includes('Report on GitHub') && el('modal-body').innerHTML.includes('Thanks'));
el('iss-type').value = 'bug';
el('iss-desc').value = 'short';
check('unified form refuses a short description', run('submitIssueForm()') === false && store().length === 2);
check('short description shows an error', el('iss-error').textContent.length > 0);

// --- 7. Unified form: question path + context capture ---------------------
run(`QUESTIONS = [{id:'Q-TEST-1', topic:'Constitution & Governance', exam:['kharidar'], question:'Test?', options:['a','b','c','d'], answer:0}];`);
run(`openIssueForm({questionId:'Q-TEST-1'})`);
check('question form shows the question id + topic', el('modal-body').innerHTML.includes('Q-TEST-1') && el('modal-body').innerHTML.includes('Constitution &amp; Governance') || el('modal-body').innerHTML.includes('Constitution & Governance'));
check('question form shows the reason select', el('modal-body').innerHTML.includes('iss-reason'));
check('question form defaults type to wrong-question', el('modal-body').innerHTML.includes('value="wrong-question" selected'));
el('iss-type').value = 'wrong-question';
el('iss-reason').value = 'wrong-answer';
el('iss-desc').value = 'The keyed answer is B but the correct answer is A, see Constitution Art 76.';
check('question form submits via the existing submitReport path', run('submitIssueForm()') === true && store().length === 3);
const qrep = store()[2];
check('question report keeps the old shape + kind/type', qrep && qrep.questionId === 'Q-TEST-1' && qrep.reason === 'wrong-answer' && qrep.kind === 'question' && qrep.type === 'wrong-question');
check('question report GitHub URL carries question + exam + topic', t.buildGithubIssueUrl(qrep).includes(encodeURIComponent('Q-TEST-1')) && t.buildGithubIssueUrl(qrep).includes(encodeURIComponent('kharidar')) && t.buildGithubIssueUrl(qrep).includes(encodeURIComponent('Constitution & Governance')));
// openReportForm delegates to the unified form (old call sites keep working)
run(`openReportForm('Q-TEST-1')`);
check('openReportForm delegates to the unified form', el('modal-body').innerHTML.includes('Q-TEST-1') && el('modal-body').innerHTML.includes('iss-desc'));
// submitReport keeps its old contract (test-v2 depends on it)
const before = store().length;
check('submitReport direct call still works', run(`submitReport('Q-TEST-1', 'typo', 'A typo worth fixing here.')`) === true && store().length === before + 1);
check('submitReport still refuses an empty comment', run(`submitReport('Q-TEST-1', 'typo', '')`) === false && store().length === before + 1);

// --- 8. Moderation: resolve / delete + unified section --------------------
check('resolve marks one report resolved', t.resolveReport(store()[0].id) === true && store().filter(r => r.status === 'open').length === 3);
check('resolve unknown id returns false', t.resolveReport('REP-nope') === false);
const sec = t.renderReportsSection();
check('reports section lists open reports with counts', sec.includes('Reports') && sec.includes('3 open') && sec.includes('1 resolved'));
check('reports section shows question id + description', sec.includes('Q-TEST-1') && sec.includes('keyed answer'));
check('reports section has Resolve + Delete buttons', sec.includes('Resolve') && sec.includes('Delete'));
const delId = store().find(r => r.status === 'open').id;
check('delete removes one report', t.deleteReport(delId) === true && store().length === 3);
check('delete unknown id returns false', t.deleteReport('REP-nope') === false);
check('reports section renders empty state', (() => { run(`localStorage.removeItem('loksewa_reports_v1')`); return t.renderReportsSection().includes('No open reports'); })());
// Old-shape entries (pre-unification, no kind/type) still render
run(`localStorage.setItem('loksewa_reports_v1', JSON.stringify([{id:'REP-old', questionId:'Q-9', reason:'typo', comment:'old comment here', by:'Guest', at:'2026-10-01T00:00:00Z', status:'open'}]))`);
check('old-shape question report renders', t.renderReportsSection().includes('Q-9') && t.renderReportsSection().includes('old comment here') && t.renderReportsSection().includes('Typo'));

// --- 9. Wiring: HTML / CSS / bundle ---------------------------------------
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
check('index has the BETA badge in the header', html.includes('class="beta-badge"') && html.includes('>BETA<'));
check('index has the beta-banner container on Home', html.includes('id="beta-banner"'));
check('index footer has the beta note + report link', html.includes('foot-beta') && html.includes('openIssueForm()'));
check('index loads report.js', html.includes('<script src="assets/js/report.js"></script>'));
const css = fs.readFileSync(path.join(root, 'assets/css/style.css'), 'utf8');
check('style.css has the §27 beta/report block', css.includes('27. Beta warning + Report an issue') && css.includes('.beta-banner') && css.includes('.beta-badge'));
const bundle = fs.readFileSync(path.join(root, 'scripts/build-bundle.py'), 'utf8');
check('build-bundle.py inlines report.js', bundle.includes("report.js") && bundle.includes('report feature (inlined)'));

console.log(fail === 0 ? 'ALL REPORT CHECKS PASSED ✔' : fail + ' CHECK(S) FAILED ✘');
process.exit(fail === 0 ? 0 : 1);
