/* Birthday wishes + "My Day" digest checks: pure birthday/BS maths, digest
   aggregation, profile-store round-trip, dismiss logic, graceful degradation
   when data/festivals.json is absent, and HTML/CSS/bundle wiring.
   Node, no deps. Usage: node scripts/test-birthday.js */
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
  vm.runInContext(bdaySrc + '\nmodule.exports={bsParse,bsToday,fmtBs,neDigits,B,setLang,getLang,remStore,remSave,migrateProgress,birthdayIsValid,birthdayIsToday,birthdayAge,birthdayMonthLen,festivalWindow,digestEventsForDay,digestEventsForMonth,digestYearSummary,BDAY_DISMISSED,renderBirthdayCard,dismissBirthdayCard,renderToday,birthdayEditorHtml,saveBirthdayFromProfile,clearBirthdayFromProfile,loadFestivalsForDigest};', sandbox);
  check('app.js + birthday.js parse', true);
} catch (e) { check('app.js + birthday.js parse', false, e.message); process.exit(1); }
const t = sandbox.module.exports;
const runInApp = code => vm.runInContext(code, sandbox);
runInApp('dataReady = true;');
runInApp('EXAMDATES = [];');

// --- 2. Birthday validation ----------------------------------------------
check('birthdayIsValid accepts 2060-07-14', t.birthdayIsValid('2060-07-14'));
check('birthdayIsValid accepts day 32 (BS months run 29-32)', t.birthdayIsValid('2050-12-32'));
check('birthdayIsValid accepts year bounds 2040/2083', t.birthdayIsValid('2040-01-01') && t.birthdayIsValid('2083-12-30'));
check('birthdayIsValid rejects garbage', !t.birthdayIsValid('not-a-date') && !t.birthdayIsValid('') && !t.birthdayIsValid(null));
check('birthdayIsValid rejects month 13 / day 0 / day 33', !t.birthdayIsValid('2060-13-01') && !t.birthdayIsValid('2060-07-00') && !t.birthdayIsValid('2060-07-33'));
check('birthdayIsValid rejects year outside 2040-2083', !t.birthdayIsValid('2039-07-14') && !t.birthdayIsValid('2084-07-14'));

// --- 3. Birthday matching + age maths (explicit todayBs: pure) -----------
check('birthdayIsToday matches month/day (2060-07-14 vs 2083-07-14)', t.birthdayIsToday('2060-07-14', '2083-07-14'));
check('birthdayIsToday ignores the year', t.birthdayIsToday('2075-07-14', '2083-07-14'));
check('birthdayIsToday rejects other days', !t.birthdayIsToday('2060-07-15', '2083-07-14') && !t.birthdayIsToday('2060-08-14', '2083-07-14'));
check('birthdayIsToday rejects bad input', !t.birthdayIsToday('', '2083-07-14') && !t.birthdayIsToday('2060-07-14', 'junk'));
check('birthdayAge is 23 on the birthday', t.birthdayAge('2060-07-14', '2083-07-14') === 23, String(t.birthdayAge('2060-07-14', '2083-07-14')));
check('birthdayAge is 22 the day before', t.birthdayAge('2060-07-14', '2083-07-13') === 22);
check('birthdayAge is 23 the day after', t.birthdayAge('2060-07-14', '2083-07-15') === 23);
check('birthdayAge is 0 in the birth year', t.birthdayAge('2083-07-14', '2083-07-14') === 0);
check('birthdayAge is null for a future birthday', t.birthdayAge('2084-07-14', '2083-07-14') === null);
check('birthdayAge is null on bad input', t.birthdayAge('', '2083-07-14') === null);
check('birthdayMonthLen Kartik 2083 = 30, Mangsir 2083 = 29', t.birthdayMonthLen(2083, 7) === 30 && t.birthdayMonthLen(2083, 8) === 29);
check('birthdayMonthLen null for unsupported year', t.birthdayMonthLen(2085, 1) === null);

// --- 4. Festival window normalisation -------------------------------------
check('festivalWindow uses start/end', JSON.stringify(t.festivalWindow({ start_bs: '2083-07-10', end_bs: '2083-07-15' })) === JSON.stringify({ start: '2083-07-10', end: '2083-07-15' }));
check('festivalWindow falls back to date_bs', JSON.stringify(t.festivalWindow({ date_bs: '2083-07-14' })) === JSON.stringify({ start: '2083-07-14', end: '2083-07-14' }));
check('festivalWindow null on empty/garbage', t.festivalWindow(null) === null && t.festivalWindow({}) === null);

// --- 5. Digest aggregation (fixed today = 2083-07-14) --------------------
const EX = [
  { id: 'e1', date_bs: '2083-07-14', kind: 'exam', title_en: 'Mock A', title_ne: 'मक A', exam: 'kharidar' },
  { id: 'e2', date_bs: '2083-07-14', kind: 'deadline', title_en: 'Apply B', title_ne: 'आवेदन B', exam: null },
  { id: 'e3', date_bs: '2083-07-20', kind: 'exam', title_en: 'Later C', title_ne: 'पछि C', exam: 'nasu' },
  { id: 'e4', date_bs: '2083-08-02', kind: 'exam', title_en: 'Next month D', title_ne: 'अर्को महिना D', exam: 'nasu' }
];
const FE = [
  { id: 'f1', name_en: 'Test Festival', name_ne: 'परीक्षण चाड', start_bs: '2083-07-13', end_bs: '2083-07-15' },
  { id: 'f2', name_en: 'Future Fest', name_ne: 'भविष्य चाड', start_bs: '2083-08-01', end_bs: '2083-08-02' }
];
let day = t.digestEventsForDay(EX, FE, '2060-07-14', '2083-07-14');
check('day digest: birthday + exam + deadline + festival = 4', day.length === 4, day.length + ' events');
check('day digest: birthday first', day[0].kind === 'birthday');
check('day digest: birthday age 23 in title', /23/.test(day[0].title_en));
check('day digest: exam/deadline/festival all present', day.some(e => e.kind === 'exam') && day.some(e => e.kind === 'deadline') && day.some(e => e.kind === 'festival'));
check('day digest: future exam excluded', !day.some(e => e.title_en === 'Later C'));
check('day digest: no birthday when none set', t.digestEventsForDay(EX, FE, '', '2083-07-14').length === 3);
check('day digest: degrades with festivals undefined', t.digestEventsForDay(EX, undefined, '2060-07-14', '2083-07-14').length === 3);
check('day digest: empty when nothing today', t.digestEventsForDay([], [], '', '2083-07-14').length === 0);

let mo = t.digestEventsForMonth(EX, FE, '2060-07-14', 2083, 7);
check('month digest: 3 exams/deadlines + birthday + festival = 5', mo.length === 5, mo.length + ' events');
check('month digest: sorted by date (festival 07-13 first, exam 07-20 last)', mo[0].date_bs === '2083-07-13' && mo[mo.length - 1].date_bs === '2083-07-20' && mo.every((e, i) => i === 0 || mo[i - 1].date_bs <= e.date_bs));
check('month digest: next-month exam excluded', !mo.some(e => e.title_en === 'Next month D'));
check('month digest: unsupported year returns []', t.digestEventsForMonth(EX, FE, '2060-07-14', 2085, 7).length === 0);
check('month digest: birthday excluded when its day exceeds month length', t.digestEventsForMonth(EX, FE, '2060-08-31', 2083, 8).filter(e => e.kind === 'birthday').length === 0);

let yr = t.digestYearSummary(EX, FE, '2060-07-14', 2083);
check('year summary: 12 months', yr.length === 12);
check('year summary: Kartik has 2 exams + 1 deadline + 1 festival + birthday', yr[6].exams === 2 && yr[6].deadlines === 1 && yr[6].festivals === 1 && yr[6].birthday === true, JSON.stringify(yr[6]));
check('year summary: Mangsir (Aug) has 1 exam, no birthday', yr[7].exams === 1 && yr[7].birthday === false);
check('year summary: empty months are zero', yr[0].exams === 0 && yr[0].deadlines === 0 && yr[0].festivals === 0 && yr[0].birthday === false);
check('year summary: unsupported year returns []', t.digestYearSummary(EX, FE, '2060-07-14', 2085).length === 0);

// --- 6. Profile store: birthday migrates in, round-trips -----------------
const migrated = t.migrateProgress({});
check('migrateProgress adds birthday "" default', migrated.birthday === '');
runInApp('progress.birthday = "2060-07-14"; progress.name = "Test User"; saveProgress();');
check('profile store round-trips birthday', JSON.parse(runInApp('localStorage.getItem("loksewa_progress_v1")')).birthday === '2060-07-14');
runInApp('progress.birthday = ""; saveProgress();');
check('clearing birthday persists', JSON.parse(runInApp('localStorage.getItem("loksewa_progress_v1")')).birthday === '');

// --- 7. Dismiss store round-trip ------------------------------------------
t.remSave(t.BDAY_DISMISSED, { date_bs: '2083-07-14' });
check('dismiss store round-trips', t.remStore(t.BDAY_DISMISSED, {}).date_bs === '2083-07-14');
check('dismiss store falls back on missing key', JSON.stringify(t.remStore('nope-key', {})) === '{}');

// --- 8. Festival loading: embedded path + graceful degradation ------------
runInApp('BIRTHDAY_FESTIVALS = null; FESTIVALS = [{id:"f8",name_en:"Global Fest",name_ne:"ग्लोबल चाड",start_bs:"2083-07-14",end_bs:"2083-07-14"}];');
t.loadFestivalsForDigest();
check('loadFestivalsForDigest prefers the app.js FESTIVALS global', runInApp('BIRTHDAY_FESTIVALS').length === 1 && runInApp('BIRTHDAY_FESTIVALS')[0].id === 'f8');
runInApp('BIRTHDAY_FESTIVALS = null; FESTIVALS = []; window.EMBEDDED_FESTIVALS = [{id:"f9",name_en:"Embedded Fest",name_ne:"इम्बेडेड चाड",start_bs:"2083-07-14",end_bs:"2083-07-14"}];');
t.loadFestivalsForDigest();
check('loadFestivalsForDigest uses window.EMBEDDED_FESTIVALS', Array.isArray(runInApp('BIRTHDAY_FESTIVALS')) && runInApp('BIRTHDAY_FESTIVALS').length === 1);
runInApp('BIRTHDAY_FESTIVALS = null; delete window.EMBEDDED_FESTIVALS;');
t.loadFestivalsForDigest(); // fetch stub rejects -> [] (set synchronously first)
check('loadFestivalsForDigest degrades to [] when festivals.json is absent', Array.isArray(runInApp('BIRTHDAY_FESTIVALS')) && runInApp('BIRTHDAY_FESTIVALS').length === 0);

// --- 9. Renderers (fake DOM) ----------------------------------------------
runInApp('progress.birthday = "2060-07-14"; progress.name = "Test User";');
runInApp('localStorage.removeItem("loksewa_birthday_dismissed_v1");');
t.renderBirthdayCard();
const cardHtml = elStore['birthday-card-box'].innerHTML;
check('birthday card renders on the birthday', /Happy Birthday/.test(cardHtml) && /Test User/.test(cardHtml), cardHtml.slice(0, 80));
check('birthday card shows age 23', /23/.test(cardHtml));
check('birthday card has dismiss + My Day buttons', /dismissBirthdayCard/.test(cardHtml) && /showView\('today'\)/.test(cardHtml));
t.dismissBirthdayCard();
check('dismiss hides the card for the day', elStore['birthday-card-box'].innerHTML === '');
t.renderBirthdayCard();
check('dismissed card stays hidden on re-render', elStore['birthday-card-box'].innerHTML === '');
runInApp('progress.birthday = "";');
t.renderBirthdayCard();
check('no card when no birthday is set', elStore['birthday-card-box'].innerHTML === '');

runInApp('EXAMDATES = ' + JSON.stringify(EX) + '; progress.birthday = "2060-07-14"; BIRTHDAY_FESTIVALS = ' + JSON.stringify(FE) + ';');
t.renderToday();
let todayHtml = elStore['today-box'].innerHTML;
check('Today tab renders birthday + exam + deadline + festival', /Your birthday/.test(todayHtml) && /Mock A/.test(todayHtml) && /Apply B/.test(todayHtml) && /Test Festival/.test(todayHtml));
check('Today tab shows today date', /14 Kartik 2083/.test(todayHtml));
runInApp("todayTab = 'month'; todaySelYear = 2083; todaySelMonth = 7;");
t.renderToday();
todayHtml = elStore['today-box'].innerHTML;
check('Month tab renders month events + birthday', /Mock A/.test(todayHtml) && /Your birthday/.test(todayHtml) && /Later C/.test(todayHtml));
runInApp("todayTab = 'year'; todaySelYear = 2083;");
t.renderToday();
todayHtml = elStore['today-box'].innerHTML;
check('Year tab renders month rows + birthday month badge', /Kartik/.test(todayHtml) && /birthday month/.test(todayHtml));
runInApp("todayTab = 'today'; EXAMDATES = []; progress.birthday = ''; BIRTHDAY_FESTIVALS = [];");
t.renderToday();
todayHtml = elStore['today-box'].innerHTML;
check('Today tab empty state when nothing is today', /Quiet day/.test(todayHtml));
check('Today tab empty state offers Practice CTA', /showView\('practice'\)/.test(todayHtml));

runInApp('progress.birthday = "2060-07-14";');
const edHtml = t.birthdayEditorHtml();
check('profile editor shows saved birthday', /14 Kartik 2060/.test(edHtml));
check('profile editor has year/month/day selects + privacy note', /bd-year/.test(edHtml) && /bd-month/.test(edHtml) && /bd-day/.test(edHtml) && /never uploaded/.test(edHtml));
check('profile editor has Save + Remove', /saveBirthdayFromProfile/.test(edHtml) && /clearBirthdayFromProfile/.test(edHtml));

// --- 10. HTML / CSS / bundle wiring ---------------------------------------
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const css = fs.readFileSync(path.join(root, 'assets/css/style.css'), 'utf8');
const appJs = fs.readFileSync(path.join(root, 'assets/js/app.js'), 'utf8');
const bundlePy = fs.readFileSync(path.join(root, 'scripts/build-bundle.py'), 'utf8');
check('index.html has view-today + today-box', html.includes('id="view-today"') && html.includes('id="today-box"'));
check('index.html has birthday-card-box on Home', html.includes('id="birthday-card-box"'));
check('index.html nav has My Day (desktop More menu + mobile nav)', html.includes('data-view="today"') && (html.match(/data-view="today"/g) || []).length >= 2);
check('index.html loads birthday.js after app.js', html.indexOf('assets/js/app.js') < html.indexOf('assets/js/birthday.js'));
check('style.css has birthday + today styles', css.includes('.bday-card') && css.includes('.today-tabs') && css.includes('.bday-badge'));
check('app.js migrates birthday field', appJs.includes("if (p.birthday === undefined) p.birthday = '';"));
check('app.js hooks renderBirthdayCard/renderToday (guarded)', appJs.includes("typeof renderBirthdayCard === 'function'") && appJs.includes("typeof renderToday === 'function'"));
check('app.js VIEW_TITLES has today', appJs.includes("today:'My Day'"));
check('test-app.js view list includes today', fs.readFileSync(path.join(root, 'scripts/test-app.js'), 'utf8').includes("'today'"));
check('build-bundle.py inlines birthday.js into the app script block', bundlePy.includes('birthday.js') && bundlePy.includes("js_patched +") && bundlePy.includes("assets/js/birthday.js"));
check('build-bundle.py removes the birthday src tag from the bundle', bundlePy.includes("html.replace('<script src=\"assets/js/birthday.js\"></script>', '', 1)"));

console.log(fail === 0 ? 'ALL BIRTHDAY CHECKS PASSED ✔' : fail + ' CHECK(S) FAILED ✘');
process.exit(fail ? 1 : 0);
