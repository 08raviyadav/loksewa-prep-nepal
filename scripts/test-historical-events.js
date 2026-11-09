/* Historical events / Dates to Remember checks: data/historical-events.json
   schema + BS validity + On-This-Day matching (incl. the BS year boundary)
   + chronological sorting + date labels (never "null") + quiz-mode state
   logic + My Day digest merge (day/month/year) + render smoke tests +
   HTML/CSS/bundle/Flutter wiring. Node, no deps.
   Usage: node scripts/test-historical-events.js */
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

// --- 1. Load app.js + birthday.js in a sandbox with a FIXED clock -------
// Fixed clock: 2026-10-31 12:00 UTC = 2083-07-14 BS (Kartik 14).
const FIXED_NOW = Date.UTC(2026, 9, 31, 12, 0, 0);
function fakeEl(id){
  return { id, innerHTML: '', hidden: false, textContent: '', value: '',
    classList: { _s: new Set(), contains(c){ return this._s.has(c); }, add(c){ this._s.add(c); }, remove(c){ this._s.delete(c); } },
    style: {}, dataset: {}, appendChild(){}, setAttribute(){}, addEventListener(){},
    querySelector(){ return null; }, querySelectorAll(){ return []; } };
}
const elStore = {};
const sandbox = {
  module: { exports: {} }, console,
  Date: class extends Date { static now() { return FIXED_NOW; } },
  localStorage: { _s: {}, getItem(k) { return (k in this._s) ? this._s[k] : null; }, setItem(k, v) { this._s[k] = String(v); }, removeItem(k) { delete this._s[k]; } },
  document: { addEventListener: () => {}, querySelector: () => null, querySelectorAll: () => [],
    getElementById(id) { if (!elStore[id]) elStore[id] = fakeEl(id); return elStore[id]; },
    createElement(tag) { return fakeEl(tag); }, documentElement: { dataset: {} } },
  window: {}, alert: () => {}, fetch: async () => { throw new Error('no fetch in test'); },
  scrollTo: () => {}, setInterval: () => 0, clearInterval: () => {}, setTimeout: (fn) => 0, clearTimeout: () => {},
  Notification: undefined, matchMedia: undefined
};
sandbox.window = sandbox;
vm.createContext(sandbox);
const appSrc = fs.readFileSync(path.join(root, 'assets/js/app.js'), 'utf8');
const bdaySrc = fs.readFileSync(path.join(root, 'assets/js/birthday.js'), 'utf8');
try {
  vm.runInContext(appSrc, sandbox);
  vm.runInContext(bdaySrc + '\nmodule.exports={bsParse,bsToday,fmtBs,neDigits,B,setLang,getLang,remStore,remSave,HISTORY_CATEGORIES,historyCategoryLabel,historyById,historyHasDate,historyDateLabel,historyAdLabel,historySorted,historyEventsToday,historyQuizPool,historyMatches,historyQuizStart,historyQuizReveal,historyQuizMark,historyQuizReset,historyQuizState,renderHistory,renderHistoryList,renderHistoryOtd,digestEventsForDay,digestEventsForMonth,digestYearSummary,bdayEventRow,loadHistoryForDigest};', sandbox);
  check('app.js + birthday.js parse', true);
} catch (e) { check('app.js + birthday.js parse', false, e.message); process.exit(1); }
const t = sandbox.module.exports;
const runInApp = code => vm.runInContext(code, sandbox);
runInApp('dataReady = true;');
const setClock = (y, m, d) => runInApp(`Date.now = function(){ return Date.UTC(${y}, ${m}, ${d}, 12, 0, 0); };`);
const resetClock = () => runInApp(`Date.now = function(){ return ${FIXED_NOW}; };`);

// --- 2. data/historical-events.json schema --------------------------------
const data = JSON.parse(fs.readFileSync(path.join(root, 'data/historical-events.json'), 'utf8'));
check('historical-events.json is a 95-entry array', Array.isArray(data) && data.length === 95, data.length + ' entries');
const cats = {};
data.forEach(e => { cats[e.category] = (cats[e.category] || 0) + 1; });
check('category counts: nepal-history 35 / constitution 13 / nepal-institutions 17 / international 16 / world-history 14',
  cats['nepal-history'] === 35 && cats['constitution'] === 13 && cats['nepal-institutions'] === 17 && cats['international'] === 16 && cats['world-history'] === 14, JSON.stringify(cats));
const conf = {};
data.forEach(e => { conf[e.confidence] = (conf[e.confidence] || 0) + 1; });
check('confidence counts: 54 high / 41 medium', conf.high === 54 && conf.medium === 41, JSON.stringify(conf));
check('day_bs present on 19 entries, date_ad on 74',
  data.filter(e => e.day_bs).length === 19 && data.filter(e => e.date_ad).length === 74,
  data.filter(e => e.day_bs).length + ' day_bs / ' + data.filter(e => e.date_ad).length + ' date_ad');
const ids = new Set();
let schemaOk = true, schemaNote = '';
const bad = s => { schemaOk = false; schemaNote += s + '; '; };
const FIELDS = ['id', 'title_en', 'title_ne', 'day_bs', 'year_bs', 'date_ad', 'category', 'summary_en', 'summary_ne', 'confidence', 'sources'];
for (const e of data) {
  for (const k of FIELDS) if (!(k in e)) bad(`missing ${k} in ${e.id || '?'}`);
  if (ids.has(e.id)) bad(`duplicate id ${e.id}`);
  ids.add(e.id);
  if (!e.title_en || !e.title_ne) bad(`missing title ${e.id}`);
  if (!e.summary_en || !e.summary_ne) bad(`missing summary ${e.id}`);
  if (e.day_bs !== null && !/^\d{2}-\d{2}$/.test(e.day_bs || '')) bad(`bad day_bs ${e.id}: ${e.day_bs}`);
  if (e.day_bs !== null) {
    const [m, d] = e.day_bs.split('-').map(Number);
    if (m < 1 || m > 12 || d < 1 || d > 32) bad(`day_bs out of the day-32 bound ${e.id}: ${e.day_bs}`);
  }
  if (e.year_bs !== null && (!Number.isInteger(e.year_bs) || e.year_bs < 1000 || e.year_bs > 2100)) bad(`bad year_bs ${e.id}: ${e.year_bs}`);
  if (e.date_ad !== null && !/^\d{4}-\d{2}-\d{2}$/.test(e.date_ad || '')) bad(`bad date_ad ${e.id}: ${e.date_ad}`);
  if (!t.HISTORY_CATEGORIES.includes(e.category)) bad(`bad category ${e.id}: ${e.category}`);
  if (!['high', 'medium'].includes(e.confidence)) bad(`bad confidence ${e.id}`);
  if (!Array.isArray(e.sources) || e.sources.length < 2) bad(`<2 sources ${e.id}`);
  (e.sources || []).forEach(s => { if (!/^https?:\/\//.test(s)) bad(`bad source URL ${e.id}: ${s}`); });
}
check('historical-events.json schema valid (all fields, formats, categories, confidence, ≥2 sources each)', schemaOk, schemaNote || data.length + ' entries');
check('all ids unique', ids.size === data.length);
// The 8 entries with BOTH year_bs and date_ad null (year only in the
// title/summary text) — the known data quirk; they must render gracefully.
const dateless = data.filter(e => !e.year_bs && !e.date_ad);
check('exactly 8 entries have both year_bs and date_ad null (known quirk)',
  dateless.length === 8, dateless.map(e => e.id).join(', '));
check('dateless entries include the Gorkha Kingdom founding (1559)',
  dateless.some(e => e.id === 'gorkha-kingdom-founded-1559'));

// --- 3. Date labels: never "null", spot-checks -----------------------------
let labelOk = true, labelNote = '';
for (const e of data) {
  const lbl = t.historyDateLabel(e);
  if (/null|undefined/.test(lbl)) { labelOk = false; labelNote += `${e.id} -> ${lbl}; `; }
}
check('historyDateLabel never renders "null"/"undefined" (all 95, EN)', labelOk, labelNote);
t.setLang('ne');
labelOk = true; labelNote = '';
for (const e of data) {
  const lbl = t.historyDateLabel(e);
  if (/null|undefined/.test(lbl)) { labelOk = false; labelNote += `${e.id} -> ${lbl}; `; }
}
check('historyDateLabel never renders "null"/"undefined" (all 95, NE)', labelOk, labelNote);
t.setLang('en');
const byId = id => data.find(e => e.id === id);
check('date label: Constitution 2015 = "3 Ashwin 2072" (day_bs + year_bs)',
  t.historyDateLabel(byId('constitution-2015')) === '3 Ashwin 2072', t.historyDateLabel(byId('constitution-2015')));
check('date label: Sugauli Treaty shows BS year + AD date',
  t.historyDateLabel(byId('sugauli-treaty-1816')) === '1872 BS · 4 March 1816', t.historyDateLabel(byId('sugauli-treaty-1816')));
check('date label: Everest shows BS year + AD date',
  t.historyDateLabel(byId('everest-first-ascent-1953')) === '2010 BS · 29 May 1953', t.historyDateLabel(byId('everest-first-ascent-1953')));
check('date label: Gorkha Kingdom (dateless) is empty string, not null',
  t.historyDateLabel(byId('gorkha-kingdom-founded-1559')) === '');
check('date label: NE mode uses Devanagari digits (Constitution)',
  (() => { t.setLang('ne'); const l = t.historyDateLabel(byId('constitution-2015')); t.setLang('en'); return l === '३ असोज २०७२'; })(), (() => { t.setLang('ne'); const l = t.historyDateLabel(byId('constitution-2015')); t.setLang('en'); return l; })());
check('historyHasDate false only for the 8 dateless entries',
  data.filter(e => !t.historyHasDate(e)).length === 8 && data.every(e => t.historyHasDate(e) === !!(e.day_bs || e.year_bs || e.date_ad)));
check('historyAdLabel rejects malformed AD dates', t.historyAdLabel('junk') === '' && t.historyAdLabel('2015-13-01') === '' && t.historyAdLabel(null) === '');
check('category labels are bilingual', t.historyCategoryLabel('constitution') === 'Constitution' && (() => { t.setLang('ne'); const l = t.historyCategoryLabel('constitution'); t.setLang('en'); return l; })() === 'संविधान');

// --- 4. Chronological sorting ----------------------------------------------
const SORT_STUB = [
  { id: 'z-dateless', title_en: 'Zulu dateless', day_bs: null, year_bs: null, date_ad: null },
  { id: 'a-ad', title_en: 'Alpha AD', day_bs: null, year_bs: null, date_ad: '1945-08-15' },
  { id: 'm-year', title_en: 'Mike year-only', day_bs: null, year_bs: 1990, date_ad: null },
  { id: 'b-bs', title_en: 'Bravo BS day', day_bs: '06-03', year_bs: 2072, date_ad: '2015-09-20' },
  { id: 'c-bs', title_en: 'Charlie BS day', day_bs: '01-12', year_bs: 2072, date_ad: '2015-04-25' },
  { id: 'd-bs', title_en: 'Delta BS day', day_bs: '06-03', year_bs: 2065, date_ad: '2008-05-28' }
];
const sortedStub = t.historySorted(SORT_STUB);
check('sort: BS month/day first (01-12, then 06-03 ×2), then BS year, then AD, then dateless last',
  sortedStub.map(e => e.id).join(',') === 'c-bs,b-bs,d-bs,m-year,a-ad,z-dateless', sortedStub.map(e => e.id).join(','));
check('sort: same MM-DD ties break by title (Bravo before Delta)',
  sortedStub[1].id === 'b-bs' && sortedStub[2].id === 'd-bs');
check('sort: real data sorts with all 19 day_bs entries first, dateless last',
  (() => { const s = t.historySorted(data); return s.slice(0, 19).every(e => e.day_bs) && s.slice(-8).every(e => !t.historyHasDate(e)); })());
check('sort: does not mutate the input array', SORT_STUB[0].id === 'z-dateless' && SORT_STUB.length === 6);

// --- 5. On-This-Day matching + the BS year boundary ------------------------
const OTD_STUB = [
  { id: 'otd-a', title_en: 'A', title_ne: 'A', day_bs: '06-03', year_bs: 2072, date_ad: '2015-09-20', category: 'constitution', summary_en: 'S', summary_ne: 'स', confidence: 'high', sources: ['https://a.test/', 'https://b.test/'] },
  { id: 'otd-b', title_en: 'B', title_ne: 'B', day_bs: '07-14', year_bs: 2007, date_ad: '1950-11-07', category: 'nepal-history', summary_en: 'S', summary_ne: 'स', confidence: 'high', sources: ['https://a.test/', 'https://b.test/'] },
  { id: 'otd-c', title_en: 'C', title_ne: 'C', day_bs: null, year_bs: 2010, date_ad: '1953-05-29', category: 'nepal-history', summary_en: 'S', summary_ne: 'स', confidence: 'high', sources: ['https://a.test/', 'https://b.test/'] },
  { id: 'otd-d', title_en: 'D', title_ne: 'D', day_bs: '12-30', year_bs: 2007, date_ad: '1951-04-11', category: 'constitution', summary_en: 'S', summary_ne: 'स', confidence: 'high', sources: ['https://a.test/', 'https://b.test/'] },
  { id: 'otd-e', title_en: 'E', title_ne: 'E', day_bs: '01-01', year_bs: 2013, date_ad: '1956-04-14', category: 'nepal-institutions', summary_en: 'S', summary_ne: 'स', confidence: 'high', sources: ['https://a.test/', 'https://b.test/'] }
];
check('OTD: matches month/day regardless of year (06-03 on 2083-06-03)',
  t.historyEventsToday(OTD_STUB, '2083-06-03').map(e => e.id).join(',') === 'otd-a');
check('OTD: no match on a quiet day', t.historyEventsToday(OTD_STUB, '2083-07-15').length === 0);
check('OTD: AD-only / dateless entries never match (day_bs null excluded)',
  t.historyEventsToday(OTD_STUB, '2083-07-14').map(e => e.id).join(',') === 'otd-b');
check('OTD: null todayBs matches nothing', t.historyEventsToday(OTD_STUB, null).length === 0 && t.historyEventsToday(OTD_STUB, 'junk').length === 0);
check('OTD: real data — Constitution Day matches 2083-06-03',
  t.historyEventsToday(data, '2083-06-03').some(e => e.id === 'constitution-2015'));
check('OTD: real data — nothing matches the base clock day 2083-07-14',
  t.historyEventsToday(data, '2083-07-14').length === 0);
// Year boundary: 2083 ends on Chaitra 30 (2083-12-30 = 2027-04-13 AD);
// the next day is 2084-01-01 (2027-04-14 AD). A 12-30 event matches on
// the last day of 2083 and never again until next Chaitra; a 01-01 event
// matches only on the new-year day.
setClock(2027, 3, 13);
check('year boundary: 2027-04-13 bsToday() === 2083-12-30', t.bsToday() === '2083-12-30', t.bsToday());
check('year boundary: 12-30 event matches on 2083-12-30, 01-01 does not',
  t.historyEventsToday(OTD_STUB, t.bsToday()).map(e => e.id).join(',') === 'otd-d');
setClock(2027, 3, 14);
check('year boundary: 2027-04-14 bsToday() === 2084-01-01', t.bsToday() === '2084-01-01', t.bsToday());
check('year boundary: 01-01 event matches on 2084-01-01, 12-30 does not',
  t.historyEventsToday(OTD_STUB, t.bsToday()).map(e => e.id).join(',') === 'otd-e');
resetClock();
check('base clock bsToday() === 2083-07-14', t.bsToday() === '2083-07-14', t.bsToday());

// --- 6. Quiz-mode state logic ----------------------------------------------
check('quiz pool: 87 of 95 (the 8 dateless entries are excluded)',
  t.historyQuizPool(data).length === 87, String(t.historyQuizPool(data).length));
check('quiz pool: no dateless entry in the pool',
  t.historyQuizPool(data).every(e => t.historyHasDate(e)));
check('quiz pool: AD-only and year-only entries ARE quizzable (they have a date to reveal)',
  t.historyQuizPool(data).some(e => e.id === 'everest-first-ascent-1953') && t.historyQuizPool(data).some(e => e.id === 'sugauli-treaty-1816'));
let st = t.historyQuizState();
check('quiz state starts idle (mode false, empty pool)', st.mode === false && st.pool.length === 0 && st.correct === 0 && st.missed === 0);
t.historyQuizMark(true); // marking with no pool must be a no-op
check('quiz mark with no pool is a no-op', t.historyQuizState().correct === 0 && t.historyQuizState().idx === 0);
t.historyQuizStart(t.historyQuizPool(data));
st = t.historyQuizState();
check('quiz start: mode on, pool 87, idx 0, not revealed', st.mode === true && st.pool.length === 87 && st.idx === 0 && st.revealed === false);
check('quiz start shuffles (pool is a permutation of the dated entries)',
  st.pool.length === 87 && new Set(st.pool.map(e => e.id)).size === 87 && st.pool.every(e => t.historyHasDate(e)));
t.historyQuizMark(true); // marking before reveal must be a no-op
check('quiz mark before reveal is a no-op', t.historyQuizState().correct === 0 && t.historyQuizState().idx === 0);
t.historyQuizReveal();
check('quiz reveal sets revealed', t.historyQuizState().revealed === true);
t.historyQuizMark(true);
st = t.historyQuizState();
check('quiz mark Got it: correct 1, idx 1, revealed cleared', st.correct === 1 && st.missed === 0 && st.idx === 1 && st.revealed === false);
t.historyQuizReveal(); t.historyQuizMark(false);
st = t.historyQuizState();
check('quiz mark Missed it: missed 1, idx 2', st.correct === 1 && st.missed === 1 && st.idx === 2);
t.historyQuizReset();
check('quiz reset: idle again', t.historyQuizState().mode === false && t.historyQuizState().pool.length === 0 && t.historyQuizState().correct === 0);
t.historyQuizStart(t.historyQuizPool(data));
const poolLen = t.historyQuizState().pool.length;
for (let i = 0; i < poolLen; i++) { t.historyQuizReveal(); t.historyQuizMark(true); }
st = t.historyQuizState();
check('quiz full run: all marked, correct == pool length, idx == pool length',
  st.correct === poolLen && st.idx === poolLen, JSON.stringify({ correct: st.correct, idx: st.idx }));
t.historyQuizMark(true); // marking past the end must be a no-op
check('quiz mark past the end is a no-op', t.historyQuizState().correct === poolLen);
t.historyQuizReset();

// --- 7. My Day digest merge (day + month + year) ---------------------------
const HI = [
  { id: 'h1', title_en: 'Constitution Day Event', title_ne: 'संविधान दिवस घटना', day_bs: '07-14', year_bs: 2072, date_ad: '2015-09-20', category: 'constitution', summary_en: 'Constitution story.', summary_ne: 'संविधानको कथा।', confidence: 'high', sources: ['https://a.test/', 'https://b.test/'] },
  { id: 'h2', title_en: 'Ashoj Event', title_ne: 'असोज घटना', day_bs: '06-03', year_bs: 2072, date_ad: '2015-09-20', category: 'constitution', summary_en: 'Ashoj story.', summary_ne: 'असोजको कथा।', confidence: 'high', sources: ['https://a.test/', 'https://b.test/'] },
  { id: 'h3', title_en: 'AD only', title_ne: 'AD मात्र', day_bs: null, year_bs: 2010, date_ad: '1953-05-29', category: 'nepal-history', summary_en: 'AD story.', summary_ne: 'AD कथा।', confidence: 'high', sources: ['https://a.test/', 'https://b.test/'] },
  { id: 'h4', title_en: 'Dateless', title_ne: 'मितिविहीन', day_bs: null, year_bs: null, date_ad: null, category: 'nepal-history', summary_en: 'Year in text.', summary_ne: 'वर्ष पाठमा।', confidence: 'medium', sources: ['https://a.test/', 'https://b.test/'] },
  { id: 'h5', title_en: 'Mangsir 29', title_ne: 'मंसिर २९', day_bs: '08-29', year_bs: 2045, date_ad: '1988-08-21', category: 'nepal-history', summary_en: 'Mangsir story.', summary_ne: 'मंसिर कथा।', confidence: 'high', sources: ['https://a.test/', 'https://b.test/'] },
  { id: 'h6', title_en: 'Mangsir 30 (does not exist in 2083)', title_ne: 'मंसिर ३०', day_bs: '08-30', year_bs: 2045, date_ad: '1988-08-21', category: 'nepal-history', summary_en: 'Impossible day.', summary_ne: 'असम्भव गते।', confidence: 'medium', sources: ['https://a.test/', 'https://b.test/'] }
];
let day = t.digestEventsForDay([], [], '', '2083-07-14', HI);
check('day digest: history event on 07-14 merges in (kind history, date = today)',
  day.length === 1 && day[0].kind === 'history' && day[0].date_bs === '2083-07-14' && day[0].title_en === 'Constitution Day Event', JSON.stringify(day.map(e => e.kind)));
check('day digest: AD-only + dateless entries never merge into the day tab',
  !day.some(e => e.title_en === 'AD only' || e.title_en === 'Dateless'));
check('day digest: history sorts last (order 4, after festival)',
  t.digestEventsForDay([], [{ id: 'f1', name_en: 'Fest', name_ne: 'चाड', start_bs: '2083-07-14', end_bs: '2083-07-14' }], '', '2083-07-14', HI).map(e => e.kind).join(',') === 'festival,history');
check('day digest: optional 5th param — old 4-arg calls still work',
  t.digestEventsForDay([], [], '', '2083-07-14').length === 0);
let mo = t.digestEventsForMonth([], [], '', 2083, 6, HI);
check('month digest: Ashoj (06) includes the 06-03 event, dated 2083-06-03',
  mo.length === 1 && mo[0].kind === 'history' && mo[0].date_bs === '2083-06-03', JSON.stringify(mo));
check('month digest: Mangsir (08) includes day 29 but NOT day 30 (29-day month in 2083)',
  t.digestEventsForMonth([], [], '', 2083, 8, HI).map(e => e.title_en).join(',') === 'Mangsir 29');
check('month digest: AD-only + dateless never merge into the month tab',
  !t.digestEventsForMonth([], [], '', 2083, 7, HI).some(e => e.title_en === 'AD only' || e.title_en === 'Dateless'));
check('month digest: optional 5th param — old 5-arg calls still work',
  t.digestEventsForMonth([], [], '', 2083, 7).length === 0);
let yr = t.digestYearSummary([], [], '', 2083, HI);
check('year summary: 12 months, history counts by day_bs month (Kartik 1, Ashoj 1, Mangsir 1)',
  yr.length === 12 && yr[6].history === 1 && yr[5].history === 1 && yr[7].history === 1, JSON.stringify(yr.map(r => r.history)));
check('year summary: Mangsir 30 (non-existent day) is NOT counted',
  yr[7].history === 1);
check('year summary: months with no history count 0',
  yr[0].history === 0 && yr[11].history === 0);
check('year summary: optional 5th param — old 4-arg calls still work',
  t.digestYearSummary([], [], '', 2083)[6].history === 0);
check('digest row: history chip + expandable summary + original year',
  (() => { const row = t.bdayEventRow(day[0]); return row.includes('📜') && row.includes('Read more') && row.includes('Constitution story.') && row.includes('2072'); })());
check('digest row: history chip is bilingual (NE)',
  (() => { t.setLang('ne'); const row = t.bdayEventRow(day[0]); t.setLang('en'); return row.includes('इतिहास') && row.includes('थप पढ्नुहोस्'); })());

// --- 8. Render smoke tests (fake DOM) --------------------------------------
runInApp('HISTORY = ' + JSON.stringify(data) + ';');
// On This Day: base clock 2083-07-14 has no event → renders nothing.
t.renderHistoryOtd();
check('OTD card: empty on a quiet day (no card rendered)', elStore['history-otd-card'].innerHTML === '');
// Constitution Day: 2026-09-20 = 2083-06-03.
setClock(2026, 8, 20);
check('Constitution Day clock: 2026-09-20 bsToday() === 2083-06-03', t.bsToday() === '2083-06-03', t.bsToday());
t.renderHistoryOtd();
let otdHtml = elStore['history-otd-card'].innerHTML;
check('OTD card: renders on Constitution Day', otdHtml.includes('On This Day') && otdHtml.includes('Constitution of Nepal 2015 promulgated'), otdHtml.slice(0, 140));
check('OTD card: row shows the BS date + expandable summary', otdHtml.includes('3 Ashwin 2072') && otdHtml.includes('35 parts, 308 articles'));
check('OTD card: links to the full Dates view', otdHtml.includes("showView('history')"));
resetClock();
// Dates view: full list.
runInApp("histFilter=''; histQuery='';");
t.renderHistory();
let listHtml = elStore['history-list'].innerHTML;
check('Dates view: renders all 95 rows', (listHtml.match(/hist-row/g) || []).length === 95, (listHtml.match(/hist-row/g) || []).length + ' rows');
check('Dates view: header shows the count + SOURCES.md reference', elStore['history-box'].innerHTML.includes('95') && elStore['history-box'].innerHTML.includes('SOURCES.md'));
check('Dates view: dateless row shows the year-in-summary note, never null',
  listHtml.includes('Year in the summary below') && !/null/.test(listHtml));
check('Dates view: rows are expandable (details/summary) with sources',
  listHtml.includes('<details') && listHtml.includes('Sources:') && listHtml.includes('https://en.wikipedia.org/wiki/History_of_Nepal'));
check('Dates view: first row is the earliest BS month/day (Baisakh 12, Gorkha earthquake)',
  listHtml.indexOf('Gorkha earthquake of 2015') < listHtml.indexOf('Constitution of Nepal 2015 promulgated'));
// Category filter + search.
runInApp("histFilter='constitution';");
t.renderHistoryList();
listHtml = elStore['history-list'].innerHTML;
check('Dates view: constitution filter shows 13 rows only', (listHtml.match(/hist-row/g) || []).length === 13, (listHtml.match(/hist-row/g) || []).length + ' rows');
runInApp("histFilter=''; histQuery='everest';");
t.renderHistoryList();
listHtml = elStore['history-list'].innerHTML;
check('Dates view: search "everest" finds both Everest entries (ascent + border treaty)',
  (listHtml.match(/hist-row/g) || []).length === 2 && listHtml.includes('First ascent of Mount Everest') && listHtml.includes('Nepal–China border treaty ratified'));
runInApp("histQuery='सगरमाथा';");
t.renderHistoryList();
listHtml = elStore['history-list'].innerHTML;
check('Dates view: search matches Nepali text too (सगरमाथा)', (listHtml.match(/hist-row/g) || []).length === 1 && listHtml.includes('First ascent of Mount Everest'));
runInApp("histQuery='zzz-no-match';");
t.renderHistoryList();
check('Dates view: no-match search shows the empty state', elStore['history-list'].innerHTML.includes('No dates match'));
runInApp("histFilter=''; histQuery='';");
// Quiz mode rendering.
t.historyQuizStart(t.historyQuizPool(data));
t.renderHistory();
listHtml = elStore['history-list'].innerHTML;
check('Quiz mode: card shows the title + "Reveal the date", date hidden',
  listHtml.includes('When did this happen?') && listHtml.includes('Reveal the date') && !listHtml.includes('hist-answer'));
t.historyQuizReveal(); t.renderHistoryList();
listHtml = elStore['history-list'].innerHTML;
check('Quiz mode: after Reveal, the date + Got it / Missed it show',
  listHtml.includes('hist-answer') && listHtml.includes('Got it') && listHtml.includes('Missed it'));
t.historyQuizMark(true); t.renderHistoryList();
check('Quiz mode: running count updates after a mark', elStore['history-list'].innerHTML.includes('✓ 1'));
t.historyQuizReset(); t.renderHistory();
check('Quiz mode: reset returns to the full list', (elStore['history-list'].innerHTML.match(/hist-row/g) || []).length === 95);
// Nepali rendering of the view.
t.setLang('ne');
t.renderHistory();
check('Dates view: Nepali header + category labels after setLang(ne)',
  elStore['history-box'].innerHTML.includes('इतिहासका मिति') && elStore['history-box'].innerHTML.includes('संविधान'));
t.setLang('en');

// --- 9. History loading: embedded path + graceful degradation --------------
runInApp('BIRTHDAY_HISTORY = null; HISTORY = [{id:"hx",title_en:"Embedded Hist",title_ne:"इम्बेडेड इतिहास",day_bs:"07-14",year_bs:2072,date_ad:"2015-09-20",category:"constitution",summary_en:"S",summary_ne:"स",confidence:"high",sources:["https://a.test/","https://b.test/"]}];');
t.loadHistoryForDigest();
check('loadHistoryForDigest prefers the app.js HISTORY global', runInApp('BIRTHDAY_HISTORY').length === 1 && runInApp('BIRTHDAY_HISTORY')[0].id === 'hx');
runInApp('BIRTHDAY_HISTORY = null; HISTORY = []; window.EMBEDDED_HISTORY = [{id:"hy",title_en:"Embedded Hist 2",title_ne:"इम्बेडेड २",day_bs:"07-14",year_bs:2072,date_ad:"2015-09-20",category:"constitution",summary_en:"S",summary_ne:"स",confidence:"high",sources:["https://a.test/","https://b.test/"]}];');
t.loadHistoryForDigest();
check('loadHistoryForDigest uses window.EMBEDDED_HISTORY', Array.isArray(runInApp('BIRTHDAY_HISTORY')) && runInApp('BIRTHDAY_HISTORY').length === 1);
runInApp('BIRTHDAY_HISTORY = null; delete window.EMBEDDED_HISTORY;');
t.loadHistoryForDigest(); // fetch stub rejects -> [] (set synchronously first)
check('loadHistoryForDigest degrades to [] when historical-events.json is absent', Array.isArray(runInApp('BIRTHDAY_HISTORY')) && runInApp('BIRTHDAY_HISTORY').length === 0);

// --- 10. HTML / CSS / bundle / Flutter wiring ------------------------------
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const css = fs.readFileSync(path.join(root, 'assets/css/style.css'), 'utf8');
const bundlePy = fs.readFileSync(path.join(root, 'scripts/build-bundle.py'), 'utf8');
check('index.html has view-history + history-box', html.includes('id="view-history"') && html.includes('id="history-box"'));
check('index.html has history-otd-card on Home, below the festival card', html.includes('id="history-otd-card"') && html.indexOf('id="festival-card"') < html.indexOf('id="history-otd-card"'));
check('index.html nav has Dates (desktop More menu + mobile nav)', (html.match(/data-view="history"/g) || []).length >= 2);
check('style.css has history styles (§28)', css.includes('.hist-badge') && css.includes('.hist-row') && css.includes('.hist-otd') && css.includes('.hist-quiz'));
check('app.js VIEW_TITLES has history', appSrc.includes("history:'Dates to Remember'"));
check('app.js showView dispatches history + home renders the OTD card', appSrc.includes("if(id==='history') renderHistory()") && appSrc.includes('renderHistoryOtd()'));
check('app.js loads historical-events.json + EMBEDDED_HISTORY fallback in loadData', appSrc.includes("fetch('data/historical-events.json')") && appSrc.includes('EMBEDDED_HISTORY'));
check('build-bundle.py embeds EMBEDDED_HISTORY', bundlePy.includes('EMBEDDED_HISTORY') && bundlePy.includes('data/historical-events.json'));
check('test-app.js view list includes history', fs.readFileSync(path.join(root, 'scripts/test-app.js'), 'utf8').includes("'history'"));
check('test-birthday.js still passes the old 4-arg digest calls (no signature break)', fs.readFileSync(path.join(root, 'scripts/test-birthday.js'), 'utf8').includes('digestEventsForDay(EX, FE,'));
check('CONTRIBUTING.md documents the day_bs-null rule', fs.readFileSync(path.join(root, 'CONTRIBUTING.md'), 'utf8').includes('day_bs') && fs.readFileSync(path.join(root, 'CONTRIBUTING.md'), 'utf8').includes('Historical events'));
const flutterData = JSON.parse(fs.readFileSync(path.join(root, '..', 'loksewa-vidyapeeth-flutter', 'assets', 'data', 'historical-events.json'), 'utf8'));
check('Flutter copy: assets/data/historical-events.json has the same 95 entries', Array.isArray(flutterData) && flutterData.length === 95 && JSON.stringify(flutterData) === JSON.stringify(data));

console.log(fail === 0 ? '\nALL HISTORICAL-EVENTS CHECKS PASSED ✔' : `\n${fail} HISTORICAL-EVENTS CHECK(S) FAILED ✘`);
process.exit(fail ? 1 : 0);
