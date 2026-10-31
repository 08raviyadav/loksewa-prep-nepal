/* Exam-dates checks: data/exam-dates.json schema + BS calendar maths + reminder
   logic. Node, no deps. Every date here must be VERIFIED against an official
   source — never guessed. Usage: node scripts/test-examdates.js */
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

// --- 1. Load app.js in a sandbox with a FIXED clock (2026-10-31 12:00 UTC) ---
const src = fs.readFileSync(path.join(root, 'assets/js/app.js'), 'utf8');
const FIXED_NOW = Date.UTC(2026, 9, 31, 12, 0, 0); // 2026-10-31 = 2083-07-14 BS
const sandbox = {
  module: { exports: {} }, console,
  Date: class extends Date { static now() { return FIXED_NOW; } },
  localStorage: { _s: {}, getItem(k) { return (k in this._s) ? this._s[k] : null; }, setItem(k, v) { this._s[k] = String(v); }, removeItem(k) { delete this._s[k]; } },
  document: { addEventListener: () => {}, querySelector: () => null, querySelectorAll: () => [], getElementById: () => null },
  window: {}, alert: () => {}, fetch: async () => { throw new Error('no fetch in test'); },
  scrollTo: () => {}, setInterval: () => 0, clearInterval: () => {}, setTimeout: () => 0, clearTimeout: () => {}
};
sandbox.window = sandbox;
vm.createContext(sandbox);
try {
  vm.runInContext(src + '\nmodule.exports={bsParse,bsAbsDay,bsFromAbs,BS_ANCHOR_ABS,bsToday,bsDaysUntil,neDigits,fmtBs,bsCountdown,upcomingExamDates,examDateById,remStore,remSave,REM_DISMISSED,REM_LIST,REM_NOTIFIED,REM_ASKED,renderExamReminder,dismissReminder,goPracticeExam,goMockExam,renderExamDates,toggleExamReminder,enableExamNotifications,checkExamNotifications,remKindLabel,remChip,getLang,setLang,B};', sandbox);
  check('app.js parses (examdates build)', true);
} catch (e) { check('app.js parses (examdates build)', false, e.message); process.exit(1); }
const t = sandbox.module.exports;
const runInApp = code => vm.runInContext(code, sandbox);

// --- 2. BS calendar maths against the anchor ---
check('anchor: bsAbsDay(2083-07-14) === 200', t.bsAbsDay('2083-07-14') === 200, String(t.bsAbsDay('2083-07-14')));
check('anchor const BS_ANCHOR_ABS === 200', t.BS_ANCHOR_ABS === 200);
check('bsToday() === 2083-07-14 at fixed clock', t.bsToday() === '2083-07-14', t.bsToday());
check('bsDaysUntil(today) === 0', t.bsDaysUntil('2083-07-14') === 0);
check('bsDaysUntil(tomorrow) === 1', t.bsDaysUntil('2083-07-15') === 1);
check('bsDaysUntil(2083-08-15) === 31 (Kartik has 30 days)', t.bsDaysUntil('2083-08-15') === 31, String(t.bsDaysUntil('2083-08-15')));
check('bsDaysUntil(2083-06-14) === -30 (Ashwin has 30 days)', t.bsDaysUntil('2083-06-14') === -30, String(t.bsDaysUntil('2083-06-14')));
check('bsDaysUntil(2083-07-21) === 7', t.bsDaysUntil('2083-07-21') === 7);
check('bsParse rejects garbage', t.bsParse('not-a-date') === null && t.bsParse('2083-7-14') === null && t.bsParse('') === null);
check('bsAbsDay rejects impossible day (Kartik 31)', t.bsAbsDay('2083-07-31') === null);
check('bsAbsDay rejects unknown year', t.bsAbsDay('2099-01-01') === null);
check('bsDaysUntil returns null on bad input', t.bsDaysUntil('xyz') === null);
check('bsFromAbs round-trips', t.bsFromAbs(t.bsAbsDay('2083-11-05')) === '2083-11-05' && t.bsFromAbs(t.bsAbsDay('2084-01-01')) === '2084-01-01');
check('fmtBs EN', t.fmtBs('2083-07-14') === '14 Kartik 2083', t.fmtBs('2083-07-14'));
t.setLang('ne');
check('fmtBs NE', t.fmtBs('2083-07-14') === '१४ कात्तिक २०८३', t.fmtBs('2083-07-14'));
check('bsCountdown NE today', t.bsCountdown(0) === 'आज');
check('bsCountdown NE 5 days', t.bsCountdown(5) === '५ दिनमा');
t.setLang('en');
check('bsCountdown EN today/tomorrow/days', t.bsCountdown(0) === 'Today' && t.bsCountdown(1) === 'Tomorrow' && t.bsCountdown(9) === 'in 9 days');
check('neDigits', t.neDigits('2083-07-14') === '२०८३-०७-१४');

// --- 3. Reminder store round-trip ---
t.remSave(t.REM_LIST, ['a', 'b']);
check('remStore/remSave round-trip', JSON.stringify(t.remStore(t.REM_LIST, [])) === '["a","b"]');
check('remStore falls back on missing key', JSON.stringify(t.remStore('nope', [])) === '[]');
check('remStore falls back on type mismatch', JSON.stringify(t.remStore(t.REM_LIST, {})) === '{}');

// --- 4. upcomingExamDates sorting / filtering (stubbed data) ---
runInApp(`EXAMDATES=[
  {id:'e3', date_bs:'2083-08-01', kind:'exam', title_en:'C', title_ne:'ग', exam:null},
  {id:'e1', date_bs:'2083-07-14', kind:'exam', title_en:'A', title_ne:'क', exam:null},
  {id:'e2', date_bs:'2083-07-20', kind:'deadline', title_en:'B', title_ne:'ख', exam:null},
  {id:'e0', date_bs:'2083-07-10', kind:'exam', title_en:'OLD', title_ne:'पुरानो', exam:null}
];`);
const up = t.upcomingExamDates();
check('upcomingExamDates excludes past, sorts ascending', up.length === 3 && up[0].id === 'e1' && up[1].id === 'e2' && up[2].id === 'e3', up.map(e => e.id).join(','));
check('examDateById finds entries', t.examDateById('e2').title_en === 'B' && t.examDateById('nope') === undefined);

// --- 5. data/exam-dates.json schema ---
const data = JSON.parse(fs.readFileSync(path.join(root, 'data/exam-dates.json'), 'utf8'));
check('exam-dates.json is an array', Array.isArray(data));
const ids = new Set();
let schemaOk = true, schemaNote = '';
for (const e of data) {
  const req = ['id', 'exam', 'kind', 'date_bs', 'title_en', 'title_ne', 'source', 'verified'];
  for (const k of req) if (!(k in e)) { schemaOk = false; schemaNote += `missing ${k} in ${e.id || '?'}; `; }
  if (ids.has(e.id)) { schemaOk = false; schemaNote += `duplicate id ${e.id}; `; }
  ids.add(e.id);
  if (!['exam', 'admit', 'deadline'].includes(e.kind)) { schemaOk = false; schemaNote += `bad kind ${e.id}; `; }
  if (e.confidence && !['high', 'medium'].includes(e.confidence)) { schemaOk = false; schemaNote += `bad confidence ${e.id}; `; }
  if (t.bsAbsDay(e.date_bs) == null) { schemaOk = false; schemaNote += `bad date_bs ${e.id}; `; }
  if (!/^https?:\/\//.test(e.source || '')) { schemaOk = false; schemaNote += `bad source ${e.id}; `; }
  if (!/^\d{4}-\d{2}-\d{2}$/.test(e.verified || '')) { schemaOk = false; schemaNote += `bad verified ${e.id}; `; }
  if (!e.title_en || !e.title_ne) { schemaOk = false; schemaNote += `empty title ${e.id}; `; }
}
check('exam-dates.json schema valid', schemaOk, schemaNote || data.length + ' entries');
// No stale "upcoming" entries: every date must be >= today minus 1 day grace
// (the grace covers the anchor edge if the file was verified late in the day).
const stale = data.filter(e => e.date_bs < '2083-07-13');
check('no stale past dates (grace: yesterday)', stale.length === 0, stale.map(e => e.id).join(','));
// exam cross-reference: flag entries whose exam id is not in exams.json
const exams = JSON.parse(fs.readFileSync(path.join(root, 'data/exams.json'), 'utf8'));
const examIds = new Set(exams.map(e => e.id));
const unmatched = data.filter(e => e.exam && !examIds.has(e.exam)).map(e => e.id + '->' + e.exam);
console.log('INFO  exam-dates entries without an exams.json match (no practice/mock link): ' + (unmatched.length ? unmatched.join(', ') : 'none'));
const badExamType = data.filter(e => e.exam !== null && typeof e.exam !== 'string');
check('exam field is a string id or null', badExamType.length === 0, badExamType.map(e => e.id).join(','));

console.log(fail === 0 ? 'ALL EXAMDATE CHECKS PASSED ✔' : fail + ' FAILURES ✘');
process.exit(fail ? 1 : 0);
