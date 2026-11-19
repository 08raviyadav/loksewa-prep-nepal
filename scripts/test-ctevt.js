/* CTEVT Health Sciences First Year guard (v1.0.18): only the 6 subjects
   whose papers have a separate MCQ section are covered — Physics,
   Chemistry, Zoology, Botany, Anatomy & Physiology, Mathematics &
   Statistics (20 MCQs / 20 marks / 20 min each, 2024 curriculum revision,
   verified against 2082 papers). English, Nepali and Social Studies have
   NO MCQ paper and must never be mapped to this exam. Node, no deps.
   Usage: node scripts/test-ctevt.js */
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const dir = path.join(root, 'data', 'questions');
const files = fs.readdirSync(dir).filter(f => f.endsWith('.json'));

const EXAM_ID = 'ctevt-health-1st-year';
const SUBJECTS = ['Physics', 'Chemistry', 'Zoology', 'Botany', 'Anatomy & Physiology', 'Mathematics & Statistics'];
const MODEL_SOURCE = 'Outrank model questions — CTEVT Health Sciences First Year';

let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

// 1. The exam entry + its MCQ-paper spec.
const exams = JSON.parse(fs.readFileSync(path.join(root, 'data', 'exams.json'), 'utf8'));
const exam = exams.find(e => e.id === EXAM_ID);
check('exams.json has the CTEVT Health Sciences First Year entry', !!exam);
if (exam) {
  const p = exam.prelim || {};
  check('prelim mirrors the real MCQ paper (20 Q × 1 mark, 20 min, pass 8, total 20)',
    p.questions === 20 && p.marksPerQ === 1 && p.timeMin === 20 && p.pass === 8 && p.total === 20,
    JSON.stringify(p));
  check('negative marking is null (unverified — mock must not apply any)', p.negative === null, 'negative=' + p.negative);
  check('syllabus lists exactly the 6 MCQ subjects',
    Array.isArray(exam.syllabus) && exam.syllabus.length === 6 && SUBJECTS.every(s => exam.syllabus.includes(s)),
    (exam.syllabus || []).join(', '));
  check('body is CTEVT', (exam.body || '').includes('Council for Technical Education and Vocational Training'));
}

// 2. The tagged pool: exactly the 6 subjects, each >= 100 questions.
const tagged = [];
files.forEach(f => {
  let arr;
  try { arr = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')); }
  catch (e) { check(f + ' parses', false, e.message); return; }
  arr.forEach(q => { if ((q.exam || []).includes(EXAM_ID)) tagged.push(q); });
});
const byTopic = {};
tagged.forEach(q => { byTopic[q.topic] = (byTopic[q.topic] || 0) + 1; });
const topics = Object.keys(byTopic).sort();
console.log('CTEVT tagged questions:', tagged.length, '| by topic:', JSON.stringify(byTopic));
check('tagged pool has exactly the 6 MCQ subjects as topics (no more, no fewer)',
  topics.length === 6 && SUBJECTS.every(s => topics.includes(s)), topics.join(', '));
SUBJECTS.forEach(s => check(`subject ${s} has >= 100 questions`, (byTopic[s] || 0) >= 100, (byTopic[s] || 0) + ' questions'));
// 3. The three no-MCQ subjects must never appear.
const banned = tagged.filter(q =>
  /english/i.test(q.topic || '') || /nepali/i.test(q.topic || '') ||
  /social studies/i.test((q.topic || '') + ' ' + (q.subtopic || '')));
check('no English / Nepali / Social Studies question is mapped to the exam', banned.length === 0,
  banned.slice(0, 3).map(q => q.id).join(', '));
// 4. New CTV-* questions are honestly labelled model questions, never PYQs.
const ctv = tagged.filter(q => (q.id || '').startsWith('CTV-'));
check('new CTV-* questions exist', ctv.length > 0, ctv.length + ' new questions');
const badSource = ctv.filter(q => q.source !== MODEL_SOURCE);
check('every CTV-* question carries the model-questions source', badSource.length === 0,
  badSource.slice(0, 3).map(q => q.id).join(', '));
const pyqClaim = ctv.filter(q => (q.source || '').startsWith('Previous Year'));
check('no CTV-* question claims PYQ status', pyqClaim.length === 0);
const wrongMarks = ctv.filter(q => q.marks !== 1);
check('every CTV-* question is 1 mark (the real MCQ paper)', wrongMarks.length === 0,
  wrongMarks.slice(0, 3).map(q => q.id).join(', '));
// 5. No retargeted question is a real PYQ (PYQs are never modified).
const pyqRetarget = tagged.filter(q => (q.source || '').startsWith('Previous Year'));
check('no real PYQ was retagged to the exam', pyqRetarget.length === 0,
  pyqRetarget.slice(0, 3).map(q => q.id).join(', '));

if (fail) { console.log(`\n${fail} CTEVT CHECK(S) FAILED`); process.exit(1); }
console.log('\nALL CTEVT CHECKS PASSED ✔');
