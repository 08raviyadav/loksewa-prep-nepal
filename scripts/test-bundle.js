/* Bundled-file smoke test: runs loksewa-prep-nepal-full.html's inline scripts
   in a VM with a minimal DOM stub and fetch() rigged to THROW — proving the
   bundle works opened directly (file://) with no server and no fetch.
   Usage: node scripts/test-bundle.js */
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

const html = fs.readFileSync(path.join(root, 'loksewa-prep-nepal-full.html'), 'utf8');
const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
check('bundle has exactly 2 inline script blocks (data + app)', blocks.length === 2, blocks.length + ' blocks');
check('bundle has no external script/link refs (github.com footer link + canonical tag exempt)', !/src="https?:|href="https?:\/\/(?!github\.com|08raviyadav\.github\.io)/.test(html));

function makeEl() {
  return { innerHTML: '', textContent: '', value: '', checked: false, disabled: false, hidden: false,
    classList: { add() {}, remove() {}, toggle() {} }, style: {}, dataset: {},
    addEventListener() {}, setAttribute() {}, getContext: () => ({ clearRect() {}, beginPath() {}, moveTo() {}, lineTo() {}, stroke() {}, fillRect() {}, fillText() {} }) };
}
const els = {};
function el(id) { if (!els[id]) els[id] = makeEl(); return els[id]; }
const alerts = [];
const store = {};
let fetchCalls = 0;
const sandbox = { module: { exports: {} }, console,
  localStorage: { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = v; }, removeItem: k => { delete store[k]; } },
  document: { addEventListener() {}, querySelector: s => (s.startsWith('#') ? el(s.slice(1)) : null),
    querySelectorAll: () => [], getElementById: id => el(id) },
  window: { scrollTo: () => {} }, alert: m => alerts.push(m),
  setInterval: () => 1, clearInterval: () => {},
  fetch: async () => { fetchCalls++; throw new Error('fetch must not be called in the bundle'); } };
vm.createContext(sandbox);
vm.runInContext(blocks[0], sandbox); // embedded data
vm.runInContext(blocks[1], sandbox); // app
const run = code => vm.runInContext(code, sandbox);

(async () => {
  check('embedded exams = 47', run('window.EMBEDDED_EXAMS.length') === 47, run('window.EMBEDDED_EXAMS.length') + '');
  check('embedded questions = 64671', run("window.EMBEDDED_QUESTIONS.length") === 64671, run('window.EMBEDDED_QUESTIONS.length') + '');
  check('embedded fun facts >= 300', run('window.EMBEDDED_FUNFACTS.length') >= 300, run('window.EMBEDDED_FUNFACTS.length') + ' facts');
  check('embedded fun facts 100% bilingual with category + source', run('window.EMBEDDED_FUNFACTS.every(f=>f.fact_en&&f.fact_ne&&f.category&&f.source)'));
  check('embedded fun facts cover all 8 categories', run('new Set(window.EMBEDDED_FUNFACTS.map(f=>f.category)).size') === 8);
  check('embedded questions 100% bilingual', run('window.EMBEDDED_QUESTIONS.every(q=>q.question_ne&&Array.isArray(q.options_ne)&&q.options_ne.length===4&&q.explanation_ne)'));
  check('demo mode is ON (no real Google login faked)', run('isDemoMode()') === true);

  await run('loadData()');
  check('loadData loads 64671 questions from embedded data', run("QUESTIONS.length") === 64671, run('QUESTIONS.length') + ' loaded');
  check('loadData loads 47 exams from embedded data', run('EXAMS.length') === 47);
  check('loadData loads fun facts from embedded data', run('FUNFACTS.length') >= 300, run('FUNFACTS.length') + ' loaded');
  check('home fun-fact box renders the daily fact with source', el('fun-fact-box').innerHTML.includes('Did you know?') && el('fun-fact-box').innerHTML.includes('Source:'));
  run('renderFunFacts()');
  check('fun facts view renders all facts with sources', (el('funfact-box').innerHTML.match(/Source:/g) || []).length >= 300);
  check('fetch was never called (file:// works)', fetchCalls === 0, fetchCalls + ' calls');

  // EN -> NE toggle
  run('setLang("ne")');
  check('EN->NE toggle switches language', run('getLang()') === 'ne');
  const q0 = run('QUESTIONS[0]');
  check('Nepali question text differs from English', run('qText(QUESTIONS[0])') !== run('QUESTIONS[0].question'), run('qText(QUESTIONS[0])').slice(0, 60));
  run('setLang("en")');
  check('toggle back to EN', run('getLang()') === 'en' && run('qText(QUESTIONS[0])') === run('QUESTIONS[0].question'));

  // Practice: 10Q, randomisation
  el('practice-exam').value = 'kharidar'; el('practice-topic').value = ''; el('practice-diff').value = '';
  el('practice-count').value = '10'; el('practice-timer').checked = false; el('practice-neg').checked = true;
  run('startPractice()');
  check('practice starts with 10 questions', run('current.questions.length') === 10);
  const firstOrder = run('current.questions.map(q=>q.id).join(",")');
  run('startPractice()');
  check('second random set has a different question order', run('current.questions.map(q=>q.id).join(",")') !== firstOrder);

  // Discussion hub: seed threads
  const seeds = run('seedDiscussions()');
  check('discussion hub seeds 9 threads', seeds.length === 9, seeds.length + ' threads');
  check('seed threads cover exams + General doubts', seeds.some(t => t.exam === 'kharidar') && seeds.some(t => t.exam === 'nmc-mbbs') && seeds.some(t => t.exam === 'general'));

  // Submit-a-question validation (exact format, EN+NE + source required)
  const exp = sandbox.module.exports;
  const valid = { exam: 'kharidar', topic: 'Constitution & Governance', difficulty: 'easy', marks: 2,
    question: 'When was the Constitution of Nepal 2072 promulgated?',
    question_ne: 'नेपालको संविधान २०७२ कहिले जारी भयो?',
    options: ['20 Sep 2016', '20 Sep 2015', '15 Aug 2015', '3 Ashoj 2073'],
    options_ne: ['२० सेप्टेम्बर २०१६', '२० सेप्टेम्बर २०१५', '१५ अगस्ट २०१५', '३ असोज २०७३'],
    answer: 1, explanation: 'Promulgated 20 September 2015.',
    explanation_ne: '२० सेप्टेम्बर २०१५ मा जारी भयो।',
    source: 'Constitution of Nepal 2072', contributor: 'Test User' };
  check('submit-form validation accepts a complete question', exp.validateSubmission(valid).ok);
  check('submit-form validation rejects a question with no Nepali version',
    !exp.validateSubmission({ ...valid, question_ne: '' }).ok);
  check('submit-form validation rejects a question with no source',
    !exp.validateSubmission({ ...valid, source: '' }).ok);

  console.log(fail ? `\n${fail} BUNDLE CHECK(S) FAILED` : '\nALL BUNDLE CHECKS PASSED ✔');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('BUNDLE CRASH:', e); process.exit(1); });
