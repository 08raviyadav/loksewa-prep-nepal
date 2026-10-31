/* v2 checks: demo sign-in, discussion hub, question submissions
   (duplicate detection, validation, spam + rate limit), moderation
   approve/reject, report-wrong-question. Node, no deps.
   Usage: node scripts/test-v2.js */
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

function makeEl() {
  return { innerHTML: '', textContent: '', value: '', checked: false, disabled: false, hidden: false,
    classList: { add() {}, remove() {}, toggle() {} }, style: {}, dataset: {},
    addEventListener() {}, setAttribute() {}, select() {},
    getContext: () => ({ clearRect() {}, beginPath() {}, moveTo() {}, lineTo() {}, stroke() {}, fillRect() {}, fillText() {} }) };
}
const els = {};
function el(id) { if (!els[id]) els[id] = makeEl(); return els[id]; }
const store = {};
const sandbox = { module: { exports: {} }, console,
  localStorage: { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = v; }, removeItem: k => { delete store[k]; } },
  document: { addEventListener() {}, querySelector: s => (s.startsWith('#') ? el(s.slice(1)) : null),
    querySelectorAll: () => [], getElementById: id => el(id), createElement: () => makeEl() },
  window: {}, alert: () => {}, prompt: () => 'spam',
  setInterval: () => 1, clearInterval: () => {},
  fetch: async url => { const p = path.join(root, url); return { json: async () => JSON.parse(fs.readFileSync(p, 'utf8')), ok: true, text: async () => fs.readFileSync(p, 'utf8') }; } };
sandbox.window = { scrollTo: () => {} };
vm.createContext(sandbox);
const src = fs.readFileSync(path.join(root, 'assets/js/app.js'), 'utf8');
vm.runInContext(src + '\nmodule.exports={normaliseText,tokenJaccard,findDuplicate,validateSubmission,rateLimitCheck,isGmailAddress,communityBadge,seedDiscussions,loadDiscussions,postReply,upvoteThread,reportPost,submitReport,approveSubmission,rejectSubmission,communityApprovedQuestions,submissionCounts,isDemoMode,signInDemo,signOut,submitQuestion};', sandbox);
const run = code => vm.runInContext(code, sandbox);
const exp = sandbox.module.exports;

(async () => {
  // --- Progress migration: fresh device gets a cloud-ready shape ---
  const prog0 = JSON.parse(store['loksewa_progress_v1'] || 'null') || run('progress');
  check('progress migrates to cloud-ready shape (user_id, email, name)', !!run('progress.user_id') && run('progress.email') === '' && run('progress.name') === '', JSON.stringify({ uid: run('progress.user_id') }));
  check('demo mode is ON with no config.js', run('isDemoMode()') === true);

  // --- Gmail validation ---
  check('isGmailAddress accepts a gmail address', exp.isGmailAddress('test.user@gmail.com'));
  check('isGmailAddress rejects yahoo', !exp.isGmailAddress('test.user@yahoo.com'));
  check('isGmailAddress rejects outlook', !exp.isGmailAddress('test.user@outlook.com'));
  check('isGmailAddress rejects a non-email', !exp.isGmailAddress('not-an-email'));

  // --- Demo sign-in: valid gmail creates a local profile; bad gmail is refused ---
  el('auth-name').value = 'Test User'; el('auth-email').value = 'test.user@gmail.com';
  run('signInDemo()');
  check('demo sign-in stores name + gmail in progress', run('progress.name') === 'Test User' && run('progress.email') === 'test.user@gmail.com');
  el('auth-name').value = 'Bad User'; el('auth-email').value = 'bad@yahoo.com';
  run('signInDemo()');
  check('demo sign-in refuses a non-Gmail address', el('auth-error').textContent.includes('Gmail') && run('progress.email') === 'test.user@gmail.com');
  run('signOut()');
  check('sign-out clears name + email but keeps the device user_id', run('progress.name') === '' && run('progress.email') === '' && !!run('progress.user_id'));

  // Expected count computed from disk at run time, not hard-coded (see
  // test-e2e.js): the dedupe worker is removing questions concurrently, so a
  // fixed number goes stale within minutes. Computed BEFORE loadData, with
  // one retry per file in case a read catches a file mid-write (torn JSON).
  const diskQ = await (async () => {
    const dir = path.join(root, 'data', 'questions');
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.json'));
    let total = 0; const broken = [];
    for (const f of files) {
      let ok = false;
      for (let attempt = 0; attempt < 2 && !ok; attempt++) {
        try { total += JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).length; ok = true; }
        catch (e) { if (attempt === 0) await new Promise(r => setTimeout(r, 500)); }
      }
      if (!ok) broken.push(f);
    }
    if (broken.length) console.log('NOTE  unparseable question files at test time (mid-write?): ' + broken.join(', '));
    return total;
  })();
  await run('loadData()');
  check('loadData loads every question on disk (' + diskQ + ')', run('QUESTIONS.length') === diskQ, run('QUESTIONS.length') + ' loaded');

  // --- Duplicate detection ---
  const q0 = run('QUESTIONS[0]');
  const dupExact = exp.findDuplicate(q0.question, q0.question_ne, run('QUESTIONS'));
  check('duplicate detection blocks an exact copy of an existing question', dupExact && dupExact.type === 'exact' && dupExact.match.id === q0.id);
  // Near-duplicate: a long real question with one extra word appended.
  const longQ = run('QUESTIONS').find(q => q.question.split(' ').length >= 12);
  const near = exp.findDuplicate(longQ.question + ' please', (longQ.question_ne || longQ.question) + ' कृपया', run('QUESTIONS'));
  check('duplicate detection flags a near-duplicate (token-Jaccard >= 0.8)', near && near.type === 'near' && near.score >= 0.8, near ? 'score=' + near.score.toFixed(2) : 'no match');
  check('duplicate detection passes a genuinely different question', exp.findDuplicate('What is the capital city of the fictional country of Zorbania and why was it chosen in 1999?', 'काल्पनिक देश जोर्बानियाको राजधानी के हो र सन् १९९९ मा किन छानियो?', run('QUESTIONS')) === null);
  check('tokenJaccard: identical = 1, disjoint = 0', exp.tokenJaccard('a b c', 'a b c') === 1 && exp.tokenJaccard('a b c', 'x y z') === 0);
  check('normaliseText ignores case / punctuation / whitespace', exp.normaliseText('  Who UNIFIED Nepal? ') === exp.normaliseText('who unified nepal'));

  // --- Submission validation ---
  const valid = { exam: 'kharidar', topic: 'Constitution & Governance', subtopic: 'Rights', difficulty: 'medium', marks: 2,
    question: 'Which article of the Constitution of Nepal 2072 guarantees the right to freedom of opinion and expression?',
    question_ne: 'नेपालको संविधान २०७२ को कुन धाराले विचार तथा अभिव्यक्तिको स्वतन्त्रताको हकको ग्यारेन्टी गर्छ?',
    options: ['Article 17', 'Article 18', 'Article 19', 'Article 20'], options_ne: ['धारा १७', 'धारा १८', 'धारा १९', 'धारा २०'],
    answer: 0, explanation: 'Article 17 guarantees the right to freedom.', explanation_ne: 'धारा १७ ले स्वतन्त्रताको हकको ग्यारेन्टी गर्छ।',
    source: 'Constitution of Nepal 2072, Part 3', contributor: 'Test User' };
  check('validation accepts a complete, well-formed submission', exp.validateSubmission(valid).ok);
  const noOpts = { ...valid, options: ['A', 'B', 'C', ''] };
  check('validation rejects a submission with fewer than 4 filled options', !exp.validateSubmission(noOpts).ok && exp.validateSubmission(noOpts).errors.some(e => e.includes('option D')));
  const dupOpts = { ...valid, options: ['Article 17', 'Article 17', 'Article 19', 'Article 20'] };
  check('validation rejects duplicate options', !exp.validateSubmission(dupOpts).ok && exp.validateSubmission(dupOpts).errors.some(e => e.includes('different')));
  const noExpl = { ...valid, explanation: '' };
  check('validation rejects an empty explanation', !exp.validateSubmission(noExpl).ok && exp.validateSubmission(noExpl).errors.some(e => e.includes('Explanation')));
  const noSrc = { ...valid, source: '' };
  check('validation rejects a missing source', !exp.validateSubmission(noSrc).ok && exp.validateSubmission(noSrc).errors.some(e => e.includes('Source')));
  const shortQ = { ...valid, question: 'Too short?' };
  check('validation rejects a question under 15 characters', !exp.validateSubmission(shortQ).ok);
  const urlQ = { ...valid, question: 'See https://example.com for this question about the constitution of Nepal?' };
  check('validation rejects a URL inside the question text', !exp.validateSubmission(urlQ).ok && exp.validateSubmission(urlQ).errors.some(e => e.includes('links')));
  const capsQ = { ...valid, question: 'WHICH ARTICLE OF THE CONSTITUTION OF NEPAL GUARANTEES FREEDOM OF OPINION?' };
  check('validation rejects mostly ALL-CAPS question text', !exp.validateSubmission(capsQ).ok);

  // --- Rate limit: max 5 per hour ---
  const now = Date.now();
  check('rate limit allows the 1st–5th submission in an hour', exp.rateLimitCheck([now - 1000, now - 2000, now - 3000, now - 4000], now).allowed);
  const blocked = exp.rateLimitCheck([now - 1000, now - 2000, now - 3000, now - 4000, now - 5000], now);
  check('rate limit blocks a 6th submission within the hour', !blocked.allowed && blocked.minutesLeft > 0, 'minutesLeft=' + blocked.minutesLeft);
  check('rate limit ignores submissions older than an hour', exp.rateLimitCheck([now - 3700e3, now - 3800e3, now - 3900e3, now - 4000e3, now - 4100e3, now - 4200e3], now).allowed);

  // --- Full submit path (DOM stub): valid new question queues as pending ---
  const setForm = d => {
    el('sub-exam').value = d.exam; el('sub-topic').value = d.topic; el('sub-subtopic').value = d.subtopic;
    el('sub-diff').value = d.difficulty; el('sub-marks').value = String(d.marks);
    el('sub-q-en').value = d.question; el('sub-q-ne').value = d.question_ne;
    d.options.forEach((o, i) => { el('sub-opt-en-' + i).value = o; });
    d.options_ne.forEach((o, i) => { el('sub-opt-ne-' + i).value = o; });
    el('sub-answer').value = String(d.answer);
    el('sub-expl-en').value = d.explanation; el('sub-expl-ne').value = d.explanation_ne;
    el('sub-source').value = d.source; el('sub-name').value = d.contributor;
  };
  const freshQ = { ...valid, question: 'In which year was the fictional Zorbania test question first asked in a mock exam in Nepal?', question_ne: 'काल्पनिक जोर्बानिया परीक्षण प्रश्न नेपालमा पहिलो पटक कुन वर्षको मक परीक्षामा सोधिएको थियो?', options: ['1999', '2001', '2003', '2005'], options_ne: ['१९९९', '२००१', '२००३', '२००५'], answer: 1, explanation: 'This is a test-only question, not a real fact.', explanation_ne: 'यो परीक्षणका लागि मात्र हो, वास्तविक तथ्य होइन।', source: 'test-v2.js fixture' };
  setForm(freshQ);
  run('submitQuestion()');
  const queue1 = JSON.parse(store['loksewa_submissions_v1']);
  check('submitQuestion queues a valid new question as pending', queue1.length === 1 && queue1[0].status === 'pending');
  // §T (2026-10-28): double-submit guard — submitting the same question
  // again while it is already pending must not queue a second copy.
  setForm(freshQ);
  run('submitQuestion()');
  check('submitQuestion does not double-queue an already-pending question', JSON.parse(store['loksewa_submissions_v1']).length === 1);
  // Duplicate via the same path is refused and the queue does not grow.
  setForm({ ...freshQ, question: q0.question, question_ne: q0.question_ne || q0.question });
  run('submitQuestion()');
  check('submitQuestion refuses an exact duplicate of a bank question', JSON.parse(store['loksewa_submissions_v1']).length === 1);

  // --- Moderation: approve -> appears in the bank with a Community badge ---
  const subId = queue1[0].id;
  const approvedQ = run(`approveSubmission('${subId}')`);
  check('approve returns the new community question (COMM- id)', approvedQ && approvedQ.id === 'COMM-001', approvedQ && approvedQ.id);
  check('approved question is in localStorage community list', run('communityApprovedQuestions()').length === 1);
  check('approved question joins the live bank immediately', run('QUESTIONS').some(q => q.id === 'COMM-001' && q._community === true));
  check('communityBadge marks community questions', exp.communityBadge({ _community: true }).includes('Community') && exp.communityBadge({}) === '');
  await run('loadData()');
  check('after reload, the approved question is still in the bank with its badge', run('QUESTIONS').some(q => q.id === 'COMM-001' && q._community === true));
  check('moderation counts show 1 approved / 0 pending for this submission', (() => { const c = exp.submissionCounts(); return c.approved === 1 && c.pending === 0; })());

  // --- Moderation: reject -> never appears in the bank ---
  setForm({ ...freshQ, question: 'Which river flows through the Kathmandu Valley and is considered sacred in Hindu tradition?', question_ne: 'काठमाडौं उपत्यकाबाट बग्ने र हिन्दू परम्परामा पवित्र मानिने नदी कुन हो?', options: ['Bagmati', 'Koshi', 'Gandaki', 'Karnali'], options_ne: ['बागमती', 'कोशी', 'गण्डकी', 'कर्णाली'], answer: 0, explanation: 'The Bagmati flows through the Kathmandu Valley.', explanation_ne: 'बागमती काठमाडौं उपत्यकाबाट बग्छ।' });
  run('submitQuestion()');
  const queue2 = JSON.parse(store['loksewa_submissions_v1']);
  const subId2 = queue2.find(s => s.status === 'pending').id;
  const rejected = run(`rejectSubmission('${subId2}', 'Test-only question, not a real fact')`);
  check('reject returns true with a reason', rejected === true);
  check('rejected question does not appear in the community list or the bank', run('communityApprovedQuestions()').length === 1 && !run('QUESTIONS').some(q => q.question && q.question.includes('flows through the Kathmandu Valley')));
  check('moderation counts show 1 approved / 1 rejected / 0 pending', (() => { const c = exp.submissionCounts(); return c.approved === 1 && c.rejected === 1 && c.pending === 0; })());

  // --- Report a wrong question is stored ---
  const repOk = run(`submitReport('${q0.id}', 'wrong-answer', 'The correct answer should be checked against the source.')`);
  const reports = JSON.parse(store['loksewa_reports_v1']);
  check('report-wrong-question is stored with id, reason and comment', repOk === true && reports.length === 1 && reports[0].questionId === q0.id && reports[0].reason === 'wrong-answer');
  check('report with no comment is refused', run(`submitReport('${q0.id}', 'typo', '')`) === false && JSON.parse(store['loksewa_reports_v1']).length === 1);

  // --- Discussion Hub: seeds + post + reply + upvote + report ---
  const threads = exp.loadDiscussions();
  const examSet = new Set(threads.map(t => t.exam));
  check('discussion hub seeds at least one thread per exam + General doubts', ['kharidar', 'nasu', 'section-officer', 'tsc-license', 'nrb-assistant', 'nmc-mbbs', 'nnc-rn', 'npc-pharmacy', 'general'].every(e => examSet.has(e)), threads.length + ' seeded threads');
  el('reply-DIS-001').value = 'Thanks — that clears it up for me.';
  const beforeReplies = exp.loadDiscussions().find(t => t.id === 'DIS-001').replies.length;
  run(`postReply('DIS-001')`);
  check('replying to a thread stores the reply', exp.loadDiscussions().find(t => t.id === 'DIS-001').replies.length === beforeReplies + 1);
  run(`upvoteThread('DIS-001')`);
  check('upvoting a thread increments its count', exp.loadDiscussions().find(t => t.id === 'DIS-001').upvotes === 1);
  run(`reportPost('DIS-001', null)`);
  check('reporting a post stores the report on the thread', exp.loadDiscussions().find(t => t.id === 'DIS-001').reports.length === 1);

  console.log(fail ? `\n${fail} V2 CHECK(S) FAILED` : '\nALL V2 CHECKS PASSED ✔');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('V2 CRASH:', e); process.exit(1); });
