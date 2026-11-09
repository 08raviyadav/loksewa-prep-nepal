/* Festival-wishes checks: data/festivals.json schema + Eid exclusion +
   BS window logic + dismiss store + render smoke test. Node, no deps.
   Eid al-Fitr and Bakr Eid are EXCLUDED from festivals.json by the user's
   explicit instruction (2026-11-09) — asserted here explicitly.
   Usage: node scripts/test-festivals.js */
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

// --- 1. Load app.js in a sandbox with a FIXED clock (2026-10-31 12:00 UTC) ---
const src = fs.readFileSync(path.join(root, 'assets/js/app.js'), 'utf8');
const FIXED_NOW = Date.UTC(2026, 9, 31, 12, 0, 0); // 2026-10-31 = 2083-07-14 BS
const _els = {};
const sandbox = {
  module: { exports: {} }, console,
  Date: class extends Date { static now() { return FIXED_NOW; } },
  localStorage: { _s: {}, getItem(k) { return (k in this._s) ? this._s[k] : null; }, setItem(k, v) { this._s[k] = String(v); }, removeItem(k) { delete this._s[k]; } },
  document: { addEventListener: () => {}, querySelector: () => null, querySelectorAll: () => [], getElementById: id => _els[id] || null },
  window: {}, alert: () => {}, fetch: async () => { throw new Error('no fetch in test'); },
  scrollTo: () => {}, setInterval: () => 0, clearInterval: () => {}, setTimeout: () => 0, clearTimeout: () => {}
};
sandbox.window = sandbox;
sandbox._els = _els;
vm.createContext(sandbox);
try {
  vm.runInContext(src + '\nmodule.exports={bsParse,bsAbsDay,bsFromAbs,BS_ANCHOR_ABS,bsToday,bsDaysUntil,neDigits,fmtBs,remStore,remSave,getLang,setLang,B,festivalsToday,festivalsTomorrow,festivalsUpcoming,festById,festDismissed,dismissFestival,renderFestivalCard,FEST_DISMISSED};', sandbox);
  check('app.js parses (festivals build)', true);
} catch (e) { check('app.js parses (festivals build)', false, e.message); process.exit(1); }
const t = sandbox.module.exports;
const runInApp = code => vm.runInContext(code, sandbox);
// bsToday() reads Date.now(), so the clock can be moved inside the vm.
const setClock = (y, m, d) => runInApp(`Date.now = function(){ return Date.UTC(${y}, ${m}, ${d}, 12, 0, 0); };`);
const resetClock = () => runInApp(`Date.now = function(){ return ${FIXED_NOW}; };`);

// --- 2. Corrected BS month lengths (2026-11-09 fix) ---
// Mangsir 2083 has 29 days, Poush 2083 has 30 (old tables said 30/29).
check('bsAbsDay(2083-08-29) valid (Mangsir has 29 days)', t.bsAbsDay('2083-08-29') != null, String(t.bsAbsDay('2083-08-29')));
check('bsAbsDay(2083-08-30) === null (no Mangsir 30)', t.bsAbsDay('2083-08-30') === null);
check('bsAbsDay(2083-09-30) valid (Poush has 30 days)', t.bsAbsDay('2083-09-30') != null, String(t.bsAbsDay('2083-09-30')));
check('bsAbsDay(2083-09-01) === 246', t.bsAbsDay('2083-09-01') === 246, String(t.bsAbsDay('2083-09-01')));
// Magh 2084 has 29 days, Falgun 2084 has 30 (old tables said 30/29).
check('bsAbsDay(2084-10-29) valid (Magh 2084 has 29 days)', t.bsAbsDay('2084-10-29') != null, String(t.bsAbsDay('2084-10-29')));
check('bsAbsDay(2084-10-30) === null (no Magh 30 in 2084)', t.bsAbsDay('2084-10-30') === null);
check('bsAbsDay(2084-11-30) valid (Falgun 2084 has 30 days)', t.bsAbsDay('2084-11-30') != null, String(t.bsAbsDay('2084-11-30')));
check('bsAbsDay(2084-11-11) === 680 (Maha Shivaratri 2028)', t.bsAbsDay('2084-11-11') === 680, String(t.bsAbsDay('2084-11-11')));
check('bsAbsDay(2085-01-05) === null (no 2085 table — windows use string compare)', t.bsAbsDay('2085-01-05') === null);

// --- 3. data/festivals.json schema + Eid exclusion ---
const data = JSON.parse(fs.readFileSync(path.join(root, 'data/festivals.json'), 'utf8'));
check('festivals.json is a non-empty array', Array.isArray(data) && data.length > 0, data.length + ' entries');
check('festivals.json has 63 entries', data.length === 63, String(data.length));
const ids = new Set();
let schemaOk = true, schemaNote = '';
const bad = s => { schemaOk = false; schemaNote += s + '; '; };
for (const f of data) {
  const req = ['id', 'name_en', 'name_ne', 'start_bs', 'end_bs', 'greeting_en', 'greeting_ne', 'emoji', 'accent', 'confidence', 'source', 'verified'];
  for (const k of req) if (!(k in f)) bad(`missing ${k} in ${f.id || '?'}`);
  if (ids.has(f.id)) bad(`duplicate id ${f.id}`);
  ids.add(f.id);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(f.start_bs || '') || !/^\d{4}-\d{2}-\d{2}$/.test(f.end_bs || '')) bad(`bad BS format ${f.id}`);
  if (f.start_bs > f.end_bs) bad(`start > end ${f.id}`);
  if (t.bsAbsDay(f.start_bs) == null) bad(`bad start_bs ${f.id}`);
  if (t.bsAbsDay(f.end_bs) == null && f.end_bs !== '2085-01-05') bad(`bad end_bs ${f.id}`);
  if (!f.greeting_en || !f.greeting_ne) bad(`missing greeting ${f.id}`);
  if (!f.name_en || !f.name_ne) bad(`missing name ${f.id}`);
  if (!f.emoji) bad(`missing emoji ${f.id}`);
  if (!/^#[0-9a-f]{6}$/i.test(f.accent || '')) bad(`bad accent ${f.id}`);
  if (!['high', 'medium'].includes(f.confidence)) bad(`bad confidence ${f.id}`);
  if (!/^https?:\/\//.test(f.source || '')) bad(`bad source ${f.id}`);
  if (f.verified !== '2026-11-09') bad(`bad verified ${f.id}`);
}
check('festivals.json schema valid', schemaOk, schemaNote || data.length + ' entries');
// Explicit Eid exclusion: no id/name/greeting may mention Eid or Bakr.
const eidHits = data.filter(f => /eid|bakr|bakra|al-fitr|al-adha/i.test([f.id, f.name_en, f.name_ne, f.greeting_en, f.greeting_ne].join(' ')));
check('NO Eid / Bakr Eid entries (exclusion enforced)', eidHits.length === 0, eidHits.map(f => f.id).join(','));
// Sorted by start_bs (generator sorts; the app sorts at runtime too).
const sorted = data.every((f, i) => i === 0 || data[i - 1].start_bs <= f.start_bs);
check('festivals.json sorted by start_bs', sorted);
// Spot-check the researched anchors.
const byId = id => data.find(f => f.id === id);
check('Tihar 2083: Kaag 07-21, Bhai Tika 07-25',
  byId('tihar-kaag-2026').start_bs === '2083-07-21' && byId('tihar-bhai-tika-2026').start_bs === '2083-07-25');
check('Maha Shivaratri 2028 = Falgun 11, 2084', byId('maha-shivaratri-2028').start_bs === '2084-11-11');
check('Bisket Jatra 2028 ends 2085-01-05 (outside BS table)', byId('bisket-jatra-2028').end_bs === '2085-01-05');
check('Janai Purnima 2027 = Shrawan 32, 2084 (32-day month)', byId('janai-purnima-2027').start_bs === '2084-04-32');

// --- 4. Window logic with the REAL data at the base clock (2026-10-31) ---
runInApp('FESTIVALS=' + JSON.stringify(data) + ';');
check('base clock bsToday() === 2083-07-14', t.bsToday() === '2083-07-14', t.bsToday());
check('no festival on 2083-07-14', t.festivalsToday().length === 0);
check('no festival tomorrow (2083-07-15)', t.festivalsTomorrow().length === 0);
const up3 = t.festivalsUpcoming(3);
check('upcoming(3) = Kaag, Kukur, Laxmi Puja 2026', up3.length === 3 && up3[0].id === 'tihar-kaag-2026' && up3[1].id === 'tihar-kukur-2026' && up3[2].id === 'tihar-laxmi-puja-2026', up3.map(f => f.id).join(','));

// --- 5. Real festival days (clock moved) ---
// 2026-11-06 = Kartik 20: no festival today, Kaag Tihar tomorrow.
setClock(2026, 10, 6);
check('2026-11-06 bsToday() === 2083-07-20', t.bsToday() === '2083-07-20', t.bsToday());
check('teaser day: nothing today', t.festivalsToday().length === 0);
check('teaser day: Kaag Tihar tomorrow', t.festivalsTomorrow().length === 1 && t.festivalsTomorrow()[0].id === 'tihar-kaag-2026');
// 2026-11-09 = Kartik 23 = Gai Tihar day (today, in real life).
setClock(2026, 10, 9);
check('2026-11-09 bsToday() === 2083-07-23 (Gai Tihar)', t.bsToday() === '2083-07-23', t.bsToday());
const today = t.festivalsToday();
check('Gai Tihar active today', today.length === 1 && today[0].id === 'tihar-gai-2026', today.map(f => f.id).join(','));
check('Govardhan Puja tomorrow', t.festivalsTomorrow().length === 1 && t.festivalsTomorrow()[0].id === 'tihar-govardhan-2026');
// 2026-11-20 = Mangsir 4: no festival, none tomorrow.
setClock(2026, 10, 20);
check('2026-11-20 bsToday() === 2083-08-04', t.bsToday() === '2083-08-04', t.bsToday());
check('quiet day: nothing today or tomorrow', t.festivalsToday().length === 0 && t.festivalsTomorrow().length === 0);
// 2027-04-12 = 2083-12-29: inside Bisket Jatra 2027 (2083-12-27 → 2084-01-05).
setClock(2027, 3, 12);
check('2027-04-12 bsToday() === 2083-12-29', t.bsToday() === '2083-12-29', t.bsToday());
check('Bisket Jatra 2027 active across the year boundary', t.festivalsToday().some(f => f.id === 'bisket-jatra-2027'));
// 2028-04-11 = 2084-12-29: inside Bisket Jatra 2028 (2084-12-28 →
// 2085-01-05). The end date is past the BS month table (bsAbsDay returns
// null for 2085), so only the string comparison can match this window —
// and it does, while today is still in 2084. The card cannot show during
// 2085-01-01→01-05 (14–18 Apr 2028) until BS_MONTH_LEN gains 2085.
setClock(2028, 3, 11);
check('2028-04-11 bsToday() === 2084-12-29', t.bsToday() === '2084-12-29', t.bsToday());
check('Bisket Jatra 2028 active though its end is past the BS table', t.festivalsToday().some(f => f.id === 'bisket-jatra-2028'));
resetClock();

// --- 6. Overlap + dismiss store round-trip (stubbed data) ---
runInApp(`FESTIVALS=[
  {id:'a', name_en:'Alpha', name_ne:'अल्फा', start_bs:'2083-07-14', end_bs:'2083-07-14', greeting_en:'Hi A', greeting_ne:'नमस्ते A', emoji:'🎉', accent:'#111111', confidence:'high', source:'https://x.test/', verified:'2026-11-09'},
  {id:'b', name_en:'Beta', name_ne:'बिटा', start_bs:'2083-07-13', end_bs:'2083-07-15', greeting_en:'Hi B', greeting_ne:'नमस्ते B', emoji:'🌸', accent:'#222222', confidence:'high', source:'https://x.test/', verified:'2026-11-09'},
  {id:'c', name_en:'Gamma', name_ne:'गामा', start_bs:'2083-07-15', end_bs:'2083-07-15', greeting_en:'Hi C', greeting_ne:'नमस्ते C', emoji:'🎊', accent:'#333333', confidence:'high', source:'https://x.test/', verified:'2026-11-09'}
];`);
check('overlap: earliest-starting first (Beta, then Alpha)', t.festivalsToday().map(f => f.id).join(',') === 'b,a', t.festivalsToday().map(f => f.id).join(','));
check('tomorrow: Gamma', t.festivalsTomorrow().map(f => f.id).join(',') === 'c');
check('upcoming(3) only strictly-after-today', t.festivalsUpcoming(3).map(f => f.id).join(',') === 'c');
check('festById finds entries', t.festById('b').name_en === 'Beta' && t.festById('nope') === undefined);
check('not dismissed before dismiss', !t.festDismissed(t.festById('b')));
t.dismissFestival('b');
check('dismissFestival stores {id: end_bs}', JSON.stringify(t.remStore(t.FEST_DISMISSED, {})) === '{"b":"2083-07-15"}', JSON.stringify(t.remStore(t.FEST_DISMISSED, {})));
check('dismissed festival reports dismissed', t.festDismissed(t.festById('b')));
check('dismissing one festival leaves others alone', !t.festDismissed(t.festById('a')));
t.dismissFestival('nope'); // unknown id must not throw or corrupt the store
check('dismissFestival(unknown) is a no-op', JSON.stringify(t.remStore(t.FEST_DISMISSED, {})) === '{"b":"2083-07-15"}');
// Dismiss hides for the rest of the window: next day Beta is still active
// (ends 07-15) but stays hidden — while Gamma, starting that day, shows.
setClock(2026, 10, 1); // 2026-11-01 = Kartik 15
check('2026-11-01 bsToday() === 2083-07-15', t.bsToday() === '2083-07-15', t.bsToday());
check('dismissed Beta hidden next day, Gamma (starting today) still shows',
  t.festivalsToday().filter(f => !t.festDismissed(f)).map(f => f.id).join(',') === 'c',
  t.festivalsToday().filter(f => !t.festDismissed(f)).map(f => f.id).join(','));
resetClock();

// --- 7. Render smoke test (capture element for #festival-card) ---
_els['festival-card'] = { innerHTML: '' };
runInApp('FESTIVALS=' + JSON.stringify(data) + '; dataReady=true;');
setClock(2026, 10, 9); // Gai Tihar day
t.renderFestivalCard();
let html = _els['festival-card'].innerHTML;
check('render: card shown on Gai Tihar day', html.includes('fest-card') && html.includes('Gai Tihar'), html.slice(0, 120));
check('render: greeting + accent colour present', html.includes('gentle cow') && html.includes('#f97316'));
check('render: dismiss button wired', html.includes("dismissFestival('tihar-gai-2026')"));
check('render: upcoming strip lists next festivals', html.includes('Govardhan') && html.includes('Bhai Tika'));
t.setLang('ne');
t.renderFestivalCard();
html = _els['festival-card'].innerHTML;
check('render: Nepali name + greeting after setLang(ne)', html.includes('गाइतिहार') && html.includes('गाईको आशीर्वाद'));
t.setLang('en');
// Dismiss via the real path: card disappears, tomorrow teaser appears.
t.dismissFestival('tihar-gai-2026');
html = _els['festival-card'].innerHTML;
check('render: after dismiss, tomorrow teaser shows Govardhan', !html.includes('fest-card') && html.includes('fest-teaser') && html.includes('Govardhan'), html.slice(0, 120));
// Teaser-only day: 2026-11-06 (Kaag Tihar tomorrow).
runInApp(`localStorage.removeItem('${t.FEST_DISMISSED}');`);
setClock(2026, 10, 6);
t.renderFestivalCard();
html = _els['festival-card'].innerHTML;
check('render: teaser chip on day before Kaag Tihar', html.includes('fest-teaser') && html.includes('Kaag Tihar') && html.includes('Tomorrow:'), html.slice(0, 120));
// Quiet day: 2026-11-20 — nothing renders.
setClock(2026, 10, 20);
t.renderFestivalCard();
check('render: empty on a quiet day', _els['festival-card'].innerHTML === '');
resetClock();

console.log(fail === 0 ? '\nAll festival checks passed.' : `\n${fail} festival check(s) FAILED.`);
process.exit(fail === 0 ? 0 : 1);
