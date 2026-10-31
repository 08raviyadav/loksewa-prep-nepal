/* Validate the question bank. Node, no deps. Usage: node scripts/test-questions.js */
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, '..', 'data', 'questions');
const files = fs.readdirSync(dir).filter(f => f.endsWith('.json'));
let total = 0, failures = [];
let neFull = 0; // questions with all three _ne fields non-empty
const seenIds = new Set(), seenQ = new Set();
const byTopic = {}, byExam = {};
const VALID_EXAMS = new Set(['anm-guide','army','ayurveda-bams','bar-council','computer-operator','csit-entrance','deputy-secretary','engineering','foreign-service','health','ioe-entrance','jta','judicial-service','kharidar','mecee-bl','midwifery-nlem','nasu','nea','nec-licence','nepal-telecom','nhpc-ayurveda','nhpc-dental','nhpc-ha','nhpc-lab','nhpc-optometry','nhpc-physio','nhpc-public-health','nhpc-radio','nmc-bds','nmc-mbbs','nnc-rn','npc-pharmacy','nrb-assistant','nrb-officer','police','provincial-psc','psc-service-groups','ranger','rbb','rbb-senior-assistant','section-officer','staff-nurse-psc','sub-engineer','tsc-license','tsc-lower-secondary','tsc-primary','tsc-secondary']);
files.forEach(f => {
  let arr;
  try { arr = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')); }
  catch (e) { failures.push(`${f}: invalid JSON — ${e.message}`); return; }
  if (!Array.isArray(arr)) { failures.push(`${f}: not an array`); return; }
  let fileNe = 0;
  console.log(`${f}: ${arr.length} questions`);
  arr.forEach((q, i) => {
    total++;
    const where = `${f}[${i}] id=${q.id || '?'}`;
    if (!q.id || seenIds.has(q.id)) failures.push(`${where}: duplicate/missing id`);
    seenIds.add(q.id);
    if (!q.question || typeof q.question !== 'string' || q.question.trim().length < 8) failures.push(`${where}: bad/empty question`);
    const norm = (q.question || '').trim().toLowerCase();
    if (seenQ.has(norm)) failures.push(`${where}: duplicate question text`);
    seenQ.add(norm);
    if (!Array.isArray(q.options) || q.options.length !== 4) failures.push(`${where}: options must be exactly 4`);
    else {
      if (q.options.some(o => !o || typeof o !== 'string' || !o.trim())) failures.push(`${where}: empty option`);
      if (new Set(q.options.map(o => o.trim().toLowerCase())).size !== 4) failures.push(`${where}: duplicate options`);
      // Normalised check (F03): two options are duplicates when one
      // EXACTLY equals the other with its single trailing parenthetical
      // removed — e.g. "10 years (alt)" vs "10 years", or "Ovary
      // (corpus luteum)" vs "Ovary". Only the LAST parenthetical is
      // stripped, and only when the stripped form matches another option
      // verbatim, so O(n)/O(log n), CPN (Maoist)/(UML), t(9;22) and
      // multi-paren options like "Agni (fire) and Jala (water)" are NOT
      // flagged: their parentheticals are the distinguishing content.
      const stripParen = o => o.trim().toLowerCase().replace(/\s*\([^()]*\)\s*$/, '');
      const parenDup = q.options.some((o, i) => q.options.some((p2, j) => i !== j && stripParen(p2) !== p2.trim().toLowerCase() && stripParen(p2) === o.trim().toLowerCase()));
      if (parenDup) failures.push(`${where}: duplicate options after stripping trailing parenthetical`);
    }
    if (!Number.isInteger(q.answer) || q.answer < 0 || q.answer > 3) failures.push(`${where}: answer out of range`);
    // Bilingual fields: if any _ne field is present, all three must be present
    // and usable — options_ne exactly 4 non-empty entries, and the (already
    // validated) answer index must point at a real Nepali option.
    const hasNe = q.question_ne !== undefined || q.options_ne !== undefined || q.explanation_ne !== undefined;
    const neOk = q.question_ne && typeof q.question_ne === 'string' && q.question_ne.trim()
      && Array.isArray(q.options_ne) && q.options_ne.length === 4
      && q.options_ne.every(o => o && typeof o === 'string' && o.trim())
      && q.explanation_ne && typeof q.explanation_ne === 'string' && q.explanation_ne.trim();
    if (neOk) { neFull++; fileNe++; }
    if (hasNe) {
      if (!q.question_ne || typeof q.question_ne !== 'string' || !q.question_ne.trim()) failures.push(`${where}: question_ne missing/empty`);
      if (!Array.isArray(q.options_ne) || q.options_ne.length !== 4) failures.push(`${where}: options_ne must be exactly 4`);
      else {
        if (q.options_ne.some(o => !o || typeof o !== 'string' || !o.trim())) failures.push(`${where}: empty option_ne`);
        if (Number.isInteger(q.answer) && q.answer >= 0 && q.answer <= 3 && !q.options_ne[q.answer]) failures.push(`${where}: answer index has no Nepali option`);
      }
      if (!q.explanation_ne || typeof q.explanation_ne !== 'string' || !q.explanation_ne.trim()) failures.push(`${where}: explanation_ne missing/empty`);
    }
    if (![1, 2].includes(q.marks)) failures.push(`${where}: marks must be 1 or 2`);
    if (!['easy','medium','hard'].includes(q.difficulty)) failures.push(`${where}: bad difficulty`);
    if (!q.topic || !q.explanation || !q.explanation.trim()) failures.push(`${where}: missing topic/explanation`);
    if (!Array.isArray(q.exam) || !q.exam.length) failures.push(`${where}: missing exam tags`);
    else q.exam.forEach(e => { if (!VALID_EXAMS.has(e)) failures.push(`${where}: unknown exam tag ${e}`); });
    byTopic[q.topic] = (byTopic[q.topic] || 0) + 1;
    (q.exam || []).forEach(e => byExam[e] = (byExam[e] || 0) + 1);
  });
  console.log(`  bilingual in ${f}: ${fileNe}/${arr.length} (${(fileNe / arr.length * 100).toFixed(1)}%)`);
});
console.log('\nTOTAL:', total);
console.log(`Bilingual coverage: ${neFull}/${total} (${(neFull / total * 100).toFixed(1)}%) questions have question_ne + options_ne[4] + explanation_ne`);
console.log('By topic:', byTopic);
console.log('By exam tag:', byExam);
if (total < 1000) failures.push(`TOTAL ${total} < 1000 required`);
if (Object.keys(byTopic).length < 16) failures.push(`Only ${Object.keys(byTopic).length} topics, need >=16`);
if (failures.length) { console.log(`\nFAILURES (${failures.length}):`); failures.slice(0, 100).forEach(f => console.log(' -', f)); process.exit(1); }
console.log('\nALL QUESTION CHECKS PASSED ✔');
