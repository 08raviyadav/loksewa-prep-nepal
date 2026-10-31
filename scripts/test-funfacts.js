/* Validate the fun-facts bank (data/funfacts.json). Node, no deps.
   Usage: node scripts/test-funfacts.js
   Every fact must be bilingual (fact_en + fact_ne), carry a valid category
   and a source, and be unique — the same bar as test-questions.js. */
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

const CATEGORIES = ['Nepal', 'World', 'Science', 'History', 'Constitution', 'Geography', 'Sports', 'Culture'];
let facts;
try { facts = JSON.parse(fs.readFileSync(path.join(root, 'data', 'funfacts.json'), 'utf8')); }
catch (e) { console.log('FAIL  funfacts.json does not parse — ' + e.message); process.exit(1); }

check('funfacts.json is an array', Array.isArray(facts));
check('at least 300 fun facts', facts.length >= 300, facts.length + ' facts');
const byCat = {};
const seenIds = new Set(), seenEn = new Set(), seenNe = new Set();
const failures = [];
facts.forEach((f, i) => {
  const where = `funfacts[${i}] id=${f.id || '?'}`;
  if (!f.id || !/^FF-(\d{3}|R7-\d{3})$/.test(f.id)) failures.push(`${where}: id must look like FF-001`);
  if (seenIds.has(f.id)) failures.push(`${where}: duplicate id`);
  seenIds.add(f.id);
  if (!f.fact_en || typeof f.fact_en !== 'string' || f.fact_en.trim().length < 10) failures.push(`${where}: fact_en missing/too short`);
  if (!f.fact_ne || typeof f.fact_ne !== 'string' || f.fact_ne.trim().length < 5) failures.push(`${where}: fact_ne missing/too short`);
  if (!CATEGORIES.includes(f.category)) failures.push(`${where}: bad category ${f.category}`);
  else byCat[f.category] = (byCat[f.category] || 0) + 1;
  if (!f.source || typeof f.source !== 'string' || !f.source.trim()) failures.push(`${where}: source missing`);
  const nEn = (f.fact_en || '').trim().toLowerCase();
  if (nEn && seenEn.has(nEn)) failures.push(`${where}: duplicate fact_en text`);
  seenEn.add(nEn);
  const nNe = (f.fact_ne || '').trim().toLowerCase();
  if (nNe && seenNe.has(nNe)) failures.push(`${where}: duplicate fact_ne text`);
  seenNe.add(nNe);
  // Bundle safety: nothing inlined may contain a literal </script>.
  if (/[</]script/i.test(f.fact_en || '') || /[</]script/i.test(f.fact_ne || '') || /[</]script/i.test(f.source || '')) failures.push(`${where}: contains </script>`);
  // No raw HTML in fact text (facts are escaped on render, but keep data clean).
  if (/[<>]/.test(f.fact_en || '') || /[<>]/.test(f.fact_ne || '')) failures.push(`${where}: fact text contains < or >`);
});
console.log('By category:', byCat);
CATEGORIES.forEach(c => check(`category ${c} has >=20 facts`, (byCat[c] || 0) >= 20, (byCat[c] || 0) + ' facts'));
check('all fact ids unique', seenIds.size === facts.length, seenIds.size + ' unique of ' + facts.length);
check('no duplicate fact_en texts', seenEn.size === facts.length);
check('no duplicate fact_ne texts', seenNe.size === facts.length);
if (failures.length) { console.log(`\nFAILURES (${failures.length}):`); failures.slice(0, 50).forEach(f => console.log(' -', f)); fail += failures.length; }
console.log(fail ? `\n${fail} FUN-FACT CHECK(S) FAILED` : '\nALL FUN-FACT CHECKS PASSED ✔');
process.exit(fail ? 1 : 0);
