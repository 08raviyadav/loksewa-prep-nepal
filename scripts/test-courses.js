/* Theory-course checks: data/courses/*.json schema, bilingual completeness,
   linked_topic validity + question-bank coverage, progress-store logic, and
   UI wiring. Node, no deps. Usage: node scripts/test-courses.js */
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

// --- 1. Load app.js in a sandbox ---
const src = fs.readFileSync(path.join(root, 'assets/js/app.js'), 'utf8');
const sandbox = {
  module: { exports: {} }, console,
  Date, localStorage: { _s: {}, getItem(k) { return (k in this._s) ? this._s[k] : null; }, setItem(k, v) { this._s[k] = String(v); }, removeItem(k) { delete this._s[k]; } },
  document: { addEventListener: () => {}, querySelector: () => null, querySelectorAll: () => [], getElementById: () => null },
  window: {}, alert: () => {}, fetch: async () => { throw new Error('no fetch in test'); },
  scrollTo: () => {}, setInterval: () => 0, clearInterval: () => {}, setTimeout: () => 0, clearTimeout: () => {}
};
sandbox.window = sandbox;
vm.createContext(sandbox);
const EXPORTS = 'module.exports={courseByExam,flattenCourseChapters,courseChapterById,calcCourseProgress,subjectProgress,COURSE_FILES,COURSE_PROG_KEY,COURSE_EXAM_MAP,getLang,setLang,B}';
try {
  vm.runInContext(src + '\n' + EXPORTS + ';', sandbox);
  check('app.js parses (courses build)', true);
} catch (e) { check('app.js parses (courses build)', false, e.message); process.exit(1); }
const t = sandbox.module.exports;
const runInApp = code => vm.runInContext(code, sandbox);

// --- 2. COURSE_FILES matches on-disk files ---
const onDisk = fs.readdirSync(path.join(root, 'data/courses')).filter(f => f.endsWith('.json')).sort();
check('COURSE_FILES matches data/courses on disk', JSON.stringify([...t.COURSE_FILES].sort()) === JSON.stringify(onDisk), onDisk.join(','));
check('COURSE_PROG_KEY versioned', t.COURSE_PROG_KEY === 'loksewa_course_progress_v1');
check('COURSE_EXAM_MAP covers all course files', t.COURSE_FILES.every(f => t.COURSE_EXAM_MAP[f.replace('.json', '')]));

// --- 3. Question-bank topic coverage map (exam -> topic -> count) ---
const cov = {};
for (const f of fs.readdirSync(path.join(root, 'data/questions'))) {
  if (!f.endsWith('.json')) continue;
  const d = JSON.parse(fs.readFileSync(path.join(root, 'data/questions', f), 'utf8'));
  const qs = Array.isArray(d) ? d : (d.questions || []);
  for (const q of qs) for (const e of (q.exam || [])) { cov[e] = cov[e] || {}; cov[e][q.topic] = (cov[e][q.topic] || 0) + 1; }
}
const VERIFIED_TAGS = new Set(['Health/Technical basics','Education & Pedagogy','Maths & Numerical','IQ & Reasoning','Constitution & Governance','Computer & ICT','Office Management & Public Service','Banking & Finance','Nepal History','Nepal Geography','Culture & Society','Science & Tech','Economy & Development','Current Affairs','English','Nepali Language']);

// --- 4. Schema + content validation per course file ---
const seenIds = new Set();
let totalChapters = 0, totalSubjects = 0;
for (const f of t.COURSE_FILES) {
  const c = JSON.parse(fs.readFileSync(path.join(root, 'data/courses', f), 'utf8'));
  const tag = f;
  check(`${tag}: top-level schema`, c.exam && Array.isArray(c.subjects) && c.subjects.length > 0 && typeof c.confidence === 'string' && Array.isArray(c.sources));
  check(`${tag}: exam id matches filename`, c.exam === f.replace('.json', ''), c.exam);
  check(`${tag}: confidence is high|medium`, c.confidence === 'high' || c.confidence === 'medium', c.confidence);
  for (const s of c.subjects) {
    totalSubjects++;
    check(`${tag}: subject has names + chapters`, (s.name_en || s.name_ne) && Array.isArray(s.chapters) && s.chapters.length > 0, s.name_en);
    for (const ch of s.chapters) {
      totalChapters++;
      const id = ch.id;
      check(`${tag}:${id} unique id`, !seenIds.has(id)); seenIds.add(id);
      check(`${tag}:${id} id prefix matches exam`, id.startsWith(c.exam === 'nayab-subba' ? 'nasu' : c.exam === 'section-officer' ? 'so' : 'kharidar'), id);
      const we = (ch.theory_en || '').split(/\s+/).filter(Boolean).length;
      const wn = (ch.theory_ne || '').split(/\s+/).filter(Boolean).length;
      check(`${tag}:${id} theory_en 150-400 words`, we >= 150 && we <= 400, String(we));
      check(`${tag}:${id} theory_ne 150-400 words`, wn >= 150 && wn <= 400, String(wn));
      check(`${tag}:${id} theory has no lorem/placeholder`, !/lorem|TODO|FIXME|xxx/i.test(ch.theory_en + ch.theory_ne));
      const kp = ch.key_points || [];
      check(`${tag}:${id} 5-10 key points`, kp.length >= 5 && kp.length <= 10, String(kp.length));
      check(`${tag}:${id} key points bilingual`, kp.every(k => (k.en && k.en.trim()) && (k.ne && k.ne.trim())));
      check(`${tag}:${id} titles bilingual`, (ch.title_en && ch.title_en.trim()) && (ch.title_ne && ch.title_ne.trim()));
      const lt = ch.linked_topics || [];
      check(`${tag}:${id} linked_topics non-empty`, lt.length > 0);
      check(`${tag}:${id} linked_topics are verified tags`, lt.every(x => VERIFIED_TAGS.has(x)), lt.filter(x => !VERIFIED_TAGS.has(x)).join(','));
      const mappedExam = t.COURSE_EXAM_MAP[c.exam];
      check(`${tag}:${id} every linked topic has questions for exam '${mappedExam}'`, lt.every(x => (cov[mappedExam] || {})[x] > 0), lt.filter(x => !((cov[mappedExam] || {})[x] > 0)).join(','));
    }
  }
}
console.log(`INFO  courses: ${t.COURSE_FILES.length} files, ${totalSubjects} subjects, ${totalChapters} chapters`);

// --- 5. Pure helper logic (stubbed course) ---
runInApp(`COURSES=[{exam:'x',subjects:[{name_en:'S1',chapters:[{id:'a'},{id:'b'}]},{name_en:'S2',chapters:[{id:'c'}]}]}];`);
check('courseByExam finds course', t.courseByExam('x') !== null && t.courseByExam('nope') === null);
check('flattenCourseChapters flattens in order', t.flattenCourseChapters(t.courseByExam('x')).map(o => o.ch.id).join(',') === 'a,b,c');
check('courseChapterById resolves + miss', t.courseChapterById(t.courseByExam('x'), 'b').subjectIdx === 0 && t.courseChapterById(t.courseByExam('x'), 'zz') === null);
const st = t.calcCourseProgress(t.courseByExam('x'), { a: true, c: true });
check('calcCourseProgress counts', st.total === 3 && st.done === 2 && st.pct === 67, JSON.stringify(st));
check('calcCourseProgress empty', t.calcCourseProgress(t.courseByExam('x'), {}).pct === 0);
const sp = t.subjectProgress(t.courseByExam('x').subjects[0], { a: true });
check('subjectProgress counts', sp.total === 2 && sp.done === 1 && sp.pct === 50);

// --- 6. Progress store round-trip (stubbed localStorage) ---
runInApp(`courseProgSave({done:{a:true},last:{exam:'x',chId:'b',ts:1}});`);
const loaded = runInApp(`courseProgLoad()`);
check('courseProgSave/Load round-trip', loaded.done.a === true && loaded.last.chId === 'b');
check('isChapterDone', runInApp(`isChapterDone('a')`) === true && runInApp(`isChapterDone('zzz')`) === false);
runInApp(`setChapterDone('b',true)`);
check('setChapterDone adds', runInApp(`isChapterDone('b')`) === true);
runInApp(`setChapterDone('a',false)`);
check('setChapterDone removes', runInApp(`isChapterDone('a')`) === false);

// --- 7. HTML / CSS wiring ---
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
check('view-courses section exists', html.includes('id="view-courses"'));
check('courses-box container exists', html.includes('id="courses-box"'));
check('nav has Courses button', html.includes('data-view="courses"'));
check('home has continue-studying box', html.includes('id="continue-studying-box"'));
const css = fs.readFileSync(path.join(root, 'assets/css/style.css'), 'utf8');
for (const cls of ['course-card-top', 'course-bar', 'subj-head', 'ch-row', 'chapter-reader', 'keypoints', 'chapter-nav', 'ring-txt', 'continue-flex'])
  check(`css has .${cls}`, css.includes('.' + cls));

// --- 8. build-bundle embeds courses ---
const bb = fs.readFileSync(path.join(root, 'scripts/build-bundle.py'), 'utf8');
check('build-bundle parses COURSE_FILES', bb.includes('COURSE_FILES'));
check('build-bundle embeds EMBEDDED_COURSES', bb.includes('EMBEDDED_COURSES'));

console.log(fail === 0 ? 'ALL COURSE CHECKS PASSED ✔' : `${fail} FAILURES`);
process.exit(fail ? 1 : 0);
