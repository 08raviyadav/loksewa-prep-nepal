/* Regression guard for the English-options-in-Nepali-mode data bug
   (user report 2026-11-18, fixed in v1.0.17): when a question asks for an
   English word — synonym, antonym, one-word substitution, "which English
   word" — its options must stay in English in Nepali mode, so options_ne
   is null and both renderers fall back to options. A Nepali options_ne on
   such a question lets the user answer without knowing the English word,
   bypassing the tested skill. This test FAILS if any such question carries
   a non-null options_ne that differs from options. Node, no deps.
   Usage: node scripts/test-options-ne.js */
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, '..', 'data', 'questions');
const files = fs.readdirSync(dir).filter(f => f.endsWith('.json'));

// Same patterns as the v1.0.17 fix (topic-agnostic, matched on the stem
// = question + question_ne), extended 2026-11-20 (scrutiny finding M2):
// "closest/opposite/nearest/similar in meaning" is a synonym/antonym
// question by another name, so it gets the same null treatment.
const CASE_A = /English word|अङ्ग्रेजी शब्द|synonym|पर्यायवाची|antonym|विपरीतार्थी|विलोम|one[\s-]?word|एक शब्द|is called a\/an|one who|closest in meaning|opposite in meaning|nearest in meaning|similar in meaning/i;
// Meaning-questions keep Nepali options: they ask for a MEANING, so a
// Nepali answer is the tested skill, not a bypass.
const EXCLUSION = /Nepali meaning|नेपाली अर्थ|what does .* mean|को अर्थ के हो/i;
// Hand-verified false positives of the Case-A patterns (2026-11-18): these
// match the stem patterns but are NOT English-word questions, so their
// Nepali options are correct and must be left alone.
const EXEMPT = {
  // Economics concept question ("one whose" contains "one who").
  'R6B-B-084': 'Giffen good — economics, not vocabulary',
  // Management concept questions ("is one who:").
  'R6B-B-323': "'line' manager — management, not vocabulary",
  'R6B-B-324': "'staff' manager — management, not vocabulary",
  // Banking concept question ("one whose" contains "one who").
  'R6B-B-338': "'delisted' company — banking, not vocabulary",
  // Computer question: which Word feature suggests synonyms (the answer is
  // a feature name, not an English word).
  'R7A-T296': 'MS Word Thesaurus feature — computer, not vocabulary',
};

let total = 0, caseA = 0, nulled = 0, sameOpts = 0, exempt = 0;
const failures = [];
let reportedQ = null;
files.forEach(f => {
  let arr;
  try { arr = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')); }
  catch (e) { failures.push(`${f}: invalid JSON — ${e.message}`); return; }
  arr.forEach((q, i) => {
    total++;
    if (q.id === 'R10-ENG3-0978') reportedQ = q;
    const stem = (q.question || '') + ' ' + (q.question_ne || '');
    if (!CASE_A.test(stem)) return;
    if (EXCLUSION.test(stem)) return;
    caseA++;
    if (EXEMPT[q.id]) { exempt++; return; }
    if (q.options_ne === null || q.options_ne === undefined) { nulled++; return; }
    if (JSON.stringify(q.options_ne) === JSON.stringify(q.options)) { sameOpts++; return; }
    failures.push(`${f}[${i}] id=${q.id}: English-word question has Nepali options_ne — "${(q.question || '').slice(0, 80)}"`);
  });
});
console.log(`TOTAL: ${total} questions in ${files.length} files`);
console.log(`Case-A (English-word) matches: ${caseA}`);
console.log(`  options_ne null (English options in Nepali mode): ${nulled}`);
console.log(`  options_ne == options (renders English either way): ${sameOpts}`);
console.log(`  hand-verified exemptions (not English-word questions): ${exempt}`);
// The reported question is the regression anchor: it must stay nulled.
if (!reportedQ) failures.push('R10-ENG3-0978 (reported question) not found in the bank');
else if (reportedQ.options_ne !== null) failures.push(`R10-ENG3-0978: options_ne must be null, found ${JSON.stringify(reportedQ.options_ne)}`);
// Sanity floor: if the patterns ever break and match nothing, the guard
// would pass vacuously — the known fixes nulled 4,966 questions (3,071 in
// v1.0.17 + 1,898 in the 2026-11-20 M2 extension).
if (nulled < 3000) failures.push(`only ${nulled} Case-A questions nulled, expected >= 3000 — patterns may have broken`);
if (failures.length) { console.log(`\nFAILURES (${failures.length}):`); failures.slice(0, 50).forEach(x => console.log(' -', x)); process.exit(1); }
console.log('\nALL OPTIONS-NE CHECKS PASSED ✔');
