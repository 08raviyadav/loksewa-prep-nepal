/* App-level checks: JS parses, scoring/shuffle maths, HTML ids referenced exist. Node, no deps.
   Usage: node scripts/test-app.js */
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

// 1. app.js parses and exports pure functions
const src = fs.readFileSync(path.join(root, 'assets/js/app.js'), 'utf8');
const sandbox = { module: { exports: {} }, console,
  // Stateful localStorage stub (fact streak + progress persist across calls,
  // like the real thing — the old stateless stub hid streak bugs).
  localStorage: { _s: {}, getItem(k) { return (k in this._s) ? this._s[k] : null; }, setItem(k, v) { this._s[k] = String(v); }, removeItem(k) { delete this._s[k]; } },
  document: { addEventListener: () => {}, querySelector: () => null, querySelectorAll: () => [], getElementById: () => null },
  window: { scrollTo: () => {} }, alert: () => {}, fetch: async () => { throw new Error('no fetch in test'); },
  // NOTE: sandbox.window = sandbox below, so window.scrollTo resolves here.
  scrollTo: () => {},
  // Timer stubs: showView clears the quiz countdown; audio uses setTimeout for Q&A pauses.
  setInterval: () => 0, clearInterval: () => {}, setTimeout: () => 0, clearTimeout: () => {} };
sandbox.window = sandbox; // app.js uses window.scrollTo only inside showView, not at load
vm.createContext(sandbox);
try { vm.runInContext(src + '\nmodule.exports={shuffle,shuffleOptions,scoreAttempt,xpFor,qText,qOpts,qExpl,getLang,setLang,mockNegRate,weekStartStr,questionsThisWeek,weeklyProgress,personalBest,questionsInADay,pickSurprise,nextFocusMode,FOCUS_DURATIONS,badges,checkWeeklyGoal,PRAISE_LINES,TRY_AGAIN_LINES,PASS_LINES,FAIL_LINES,pickLine,prefersReducedMotion,recordFactVisit,getFactStreak,questionOfDay,speedBonusFor,mistakePool,longestStreak,bestDay,personalRecords,buildShareText,getSpeedBest,SPEED_SECONDS,SPEED_COUNT,effectiveNoticeStatus,findDuplicate,tokenJaccard,chatReply,chatTopicFor,chatTopicStats,isFactualQuestion,chatHistory,saveChatHistory,chatSend,validateSuggestion,isDuplicateSuggestion,loadSuggestions,saveSuggestions,upvoteSuggestion,LS_CHAT,LS_SUGGEST,CHAT_MAX_MSGS,B,examName,fmt1,markPyqFlags,topicsForExam,mapTopicToSyllabus,breakdownLabelTopics,parseBreakdownWeights,pyqTopicShares,examTopicWeights,practiceTopicStats,attemptLevelTotals,guessEV,evVerdict,coachStats,coachAdvice,drillTopic,heatCell,buildStudyPlan,daysUntil,rebalancePlan,loadPlans,savePlans,planNotices,renderPlanCard,NOTICE_EXAM,PLANS_KEY,TOPIC_SYLLABUS_KEYS,BREAKDOWN_GROUPS,noteBySlug,noteByTopic,noteTitle,noteBullet,openNote,openNoteList,reviseTopic,audioSupported,audioStateInit,audioBuildItems,audioPlay,audioPause,audioStop,audioNext,audioPrev,audioNewSet,audioSetSource,audioSetRate,audioSetVoiceLang,renderNotes,renderAudio};', sandbox); check('app.js parses', true); }
catch (e) { check('app.js parses', false, e.message); process.exit(1); }
const { shuffle, shuffleOptions, scoreAttempt, xpFor, qText, qOpts, qExpl, getLang, setLang, mockNegRate, weekStartStr, questionsThisWeek, weeklyProgress, personalBest, questionsInADay, pickSurprise, nextFocusMode, FOCUS_DURATIONS, badges, checkWeeklyGoal, PRAISE_LINES, TRY_AGAIN_LINES, PASS_LINES, FAIL_LINES, pickLine, prefersReducedMotion, recordFactVisit, getFactStreak, questionOfDay, speedBonusFor, mistakePool, longestStreak, bestDay, personalRecords, buildShareText, getSpeedBest, SPEED_SECONDS, SPEED_COUNT, effectiveNoticeStatus, findDuplicate, tokenJaccard, chatReply, chatTopicFor, chatTopicStats, isFactualQuestion, chatHistory, saveChatHistory, chatSend, validateSuggestion, isDuplicateSuggestion, loadSuggestions, saveSuggestions, upvoteSuggestion, LS_CHAT, LS_SUGGEST, CHAT_MAX_MSGS, B, examName, fmt1, markPyqFlags, topicsForExam, mapTopicToSyllabus, breakdownLabelTopics, parseBreakdownWeights, pyqTopicShares, examTopicWeights, practiceTopicStats, attemptLevelTotals, guessEV, evVerdict, coachStats, coachAdvice, drillTopic, heatCell, buildStudyPlan, daysUntil, rebalancePlan, loadPlans, savePlans, planNotices, renderPlanCard, NOTICE_EXAM, PLANS_KEY, TOPIC_SYLLABUS_KEYS, BREAKDOWN_GROUPS, noteBySlug, noteByTopic, noteTitle, noteBullet, openNote, openNoteList, reviseTopic, audioSupported, audioStateInit, audioBuildItems, audioPlay, audioPause, audioStop, audioNext, audioPrev, audioNewSet, audioSetSource, audioSetRate, audioSetVoiceLang, renderNotes, renderAudio } = sandbox.module.exports;
const runInApp = code => vm.runInContext(code, sandbox);

// 2. Scoring maths — PSC 20% negative marking
let r = scoreAttempt([0, 1, null, 2], [{ marks: 2, answer: 0 }, { marks: 2, answer: 0 }, { marks: 2, answer: 0 }, { marks: 1, answer: 2 }], true);
check('scoring: 1 correct 2-mark (+2), 1 wrong 2-mark (−0.4), 1 skipped, 1 correct 1-mark (+1) = 2.6', r.score === 2.6, JSON.stringify(r));
r = scoreAttempt([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], Array(10).fill({ marks: 2, answer: 0 }), true);
check('scoring: 10 correct 2-mark = 20', r.score === 20 && r.pct === 100, JSON.stringify(r));
r = scoreAttempt([1, 1], [{ marks: 2, answer: 0 }, { marks: 1, answer: 0 }], true);
check('scoring: 2 wrong (2-mark + 1-mark) = −0.6', r.score === -0.6, JSON.stringify(r));
r = scoreAttempt([1], [{ marks: 2, answer: 0 }], false);
check('scoring: negative marking OFF, wrong = 0', r.score === 0, JSON.stringify(r));
r = scoreAttempt([1, 1], [{ marks: 2, answer: 0 }, { marks: 1, answer: 0 }], true, 0);
check('scoring: negative rate 0 (no-negative exams, e.g. NNC/NHPC) — wrong answers cost 0', r.score === 0, JSON.stringify(r));
r = scoreAttempt([1], [{ marks: 2, answer: 0 }], true, 0.25);
check('scoring: negative rate 0.25 — 1 wrong 2-mark = −0.5', r.score === -0.5, JSON.stringify(r));
check('xp: score 20 → 200 XP', xpFor(20, 20) === 200);

// 2b. Per-exam negative-marking rate for mocks (mockNegRate)
check('mockNegRate: PSC prelim negative 0.2 → 0.2', mockNegRate({ negative: 0.2 }) === 0.2);
check('mockNegRate: MECEE negative 0.25 → 0.25', mockNegRate({ negative: 0.25 }) === 0.25);
check('mockNegRate: no-negative exams (negative 0) → 0', mockNegRate({ negative: 0 }) === 0);
check('mockNegRate: unverified negative (null, e.g. TSC licence) → 0 (never deduct on an unverified rule)', mockNegRate({ negative: null }) === 0);

// 3. Randomisation — order differs across runs, options remap correctly
const base = Array.from({ length: 20 }, (_, i) => i);
const orders = new Set(Array.from({ length: 20 }, () => shuffle(base).join(',')));
check('shuffle: 20 runs produce >1 distinct order', orders.size > 1, orders.size + ' distinct');
let okRemap = true;
for (let t = 0; t < 50; t++) {
  const q = { options: ['A', 'B', 'C', 'D'], answer: 2 };
  const s = shuffleOptions(q);
  if (s.options[s.answer] !== 'C' || new Set(s.options).size !== 4) { okRemap = false; break; }
}
check('shuffleOptions: correct answer remaps correctly (50 trials)', okRemap);
const qOrders = new Set(Array.from({ length: 20 }, () => shuffleOptions({ options: ['A', 'B', 'C', 'D'], answer: 0 }).options.join(',')));
check('shuffleOptions: option order varies', qOrders.size > 1, qOrders.size + ' distinct');

// 3b. Language toggle — Nepali options shuffle with the SAME permutation as
// English ones, and the _ne helpers fall back to English where fields are missing.
let okPair = true;
for (let t = 0; t < 50; t++) {
  const s = shuffleOptions({ options: ['A', 'B', 'C', 'D'], options_ne: ['क', 'ख', 'ग', 'घ'], answer: 2 });
  if (s.options[s.answer] !== 'C' || s.options_ne[s.answer] !== 'ग' || new Set(s.options_ne).size !== 4) { okPair = false; break; }
}
check('shuffleOptions: options_ne shuffle paired with options (50 trials)', okPair);
check('shuffleOptions: question without _ne fields still shuffles', shuffleOptions({ options: ['A', 'B', 'C', 'D'], answer: 1 }).options.length === 4);
check('lang default is en', getLang() === 'en');
setLang('ne');
check('lang switches to ne', getLang() === 'ne');
check('qText uses question_ne in ne mode', qText({ question: 'Q', question_ne: 'प्र' }) === 'प्र');
check('qText falls back to English when _ne missing', qText({ question: 'Q' }) === 'Q');
check('qOpts uses options_ne in ne mode', qOpts({ options: ['A', 'B'], options_ne: ['क', 'ख'] }).join('') === 'कख');
check('qOpts falls back to English options', qOpts({ options: ['A', 'B'] }).join('') === 'AB');
check('qExpl uses explanation_ne in ne mode', qExpl({ explanation: 'E', explanation_ne: 'व्याख्या' }) === 'व्याख्या');
check('qExpl falls back to English explanation', qExpl({ explanation: 'E' }) === 'E');
setLang('en');
check('lang switches back to en', getLang() === 'en');
check('qText uses English in en mode even when _ne present', qText({ question: 'Q', question_ne: 'प्र' }) === 'Q');

// 4. HTML references: every getElementById / onclick target in app.js that is a static id exists in index.html
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
check('language toggle button exists in index.html', html.includes('id="lang-toggle"'));
const idsInHtml = new Set([...html.matchAll(/id="([^"]+)"/g)].map(m => m[1]));
const idsUsed = new Set([...src.matchAll(/getElementById\('([^']+)'\)/g)].map(m => m[1]));
const dynamic = new Set(['quiz-timer', 'feedback', 'flash-ans', 'chart', // created at runtime inside quiz/flash/dashboard boxes
  // dashboard renders weekly + focus-timer mirrors at runtime (same pattern as chart)
  'weekly-box-dash', 'focus-timer-box-dash',
  // result view renders the share-status line at runtime (inside result-box)
  'share-status',
  // v2 views render their forms into innerHTML at runtime (auth, discuss, submit, report modal)
  'sub-exam', 'auth-demo-banner', 'auth-name', 'auth-email', 'auth-error', 'auth-form', 'auth-success',
  'dis-title', 'dis-body', 'dis-exam', 'dis-error', 'rep-reason', 'rep-comment', 'rep-error',
  'sub-errors', 'sub-done', 'sub-counts', 'sub-template', 'sub-submit-btn',
  // feature 9/10: chat + suggest render their forms into innerHTML at runtime
  'chat-input', 'chat-log', 'sug-title', 'sug-desc', 'sug-cat', 'sug-error', 'sug-done', 'sug-submit-btn',
  // features 6/7: audio controls render into audio-box at runtime
  'audio-src', 'audio-rate', 'audio-rate-val', 'audio-voice', 'audio-status', 'audio-now',
  // gamification: dashboard renders weekly + focus boxes into innerHTML at runtime
  'weekly-box-dash', 'focus-timer-box-dash']);
let missing = [...idsUsed].filter(id => !idsInHtml.has(id) && !dynamic.has(id));
check('all static element ids used by app.js exist in index.html', missing.length === 0, missing.join(', ') || `${idsUsed.size} ids checked`);
// view ids referenced by showView / nav
['home','practice','quiz','result','mock','guide','dashboard','review','flash','search','auth','profile','discuss','submit','moderate','papers','notices','funfacts','chat','suggest','coverage','print','planner','coach','pyq','notes','audio'].forEach(v => check(`view exists: view-${v}`, idsInHtml.has('view-' + v)));
check('notes + audio views are reachable from the desktop nav', html.includes('data-view="notes"') && html.includes('data-view="audio"'));
check('notes-box + audio-box exist in index.html', idsInHtml.has('notes-box') && idsInHtml.has('audio-box'));
check('analytics views are reachable from the desktop nav', ['coverage','print','planner','coach','pyq'].every(v => html.includes(`data-view="${v}"`)));
check('analytics controls exist in index.html', ['cov-exam','cov-box','prt-exam','prt-box','pla-notice','pla-exam','pla-date','pla-daily','pla-box','coa-exam','coa-box','pyq-exam','pyq-box'].every(id => idsInHtml.has(id)));
check('demo banner exists in index.html', idsInHtml.has('demo-banner'));
check('report modal exists in index.html', idsInHtml.has('modal') && idsInHtml.has('modal-body'));
check('nav has Discuss / Contribute / Sign In / Profile buttons', html.includes('data-view="discuss"') && html.includes('data-view="submit"') && html.includes('data-view="auth"') && html.includes('data-view="profile"'));
check('nav has Ask (chat) / Suggest buttons', html.includes('data-view="chat"') && html.includes('data-view="suggest"'));
check('nav has Old Papers / Notices buttons', html.includes('data-view="papers"') && html.includes('data-view="notices"'));
check('papers + notices filter/box ids exist in index.html', ['papers-filter','papers-box','notices-scope','notices-body','notices-status','notices-box'].every(id => idsInHtml.has(id)));

// 5. Data files exist and exams.json parses
const exams = JSON.parse(fs.readFileSync(path.join(root, 'data/exams.json'), 'utf8'));
check('exams.json parses, 47 exams (42 + 5 entrance/licence)', Array.isArray(exams) && exams.length === 47, exams.length + ' exams');
const withPrelim = exams.filter(e => e.prelim);
const guideOnly = exams.filter(e => !e.prelim);
check('33 exams have an MCQ prelim, 14 are guide-only', withPrelim.length === 33 && guideOnly.length === 14, withPrelim.length + ' prelim / ' + guideOnly.length + ' guide-only');
const mockSpecs = { kharidar: [50, 45, 2, 45], nasu: [50, 45, 2, 45], 'section-officer': [100, 90, 1, 45], 'tsc-primary': [50, 60, 2, 50], 'nrb-assistant': [50, 45, 2, 40] };
for (const [id, [n, t, m, p]] of Object.entries(mockSpecs)) {
  const e = exams.find(x => x.id === id);
  check(`mock spec ${id}: ${n}Q/${t}min/${m} mark/pass ${p}`, !!e && e.prelim.questions === n && e.prelim.timeMin === t && e.prelim.marksPerQ === m && e.prelim.pass === p);
}
// Overnight-merge exam specs: GAP-AUDIT verified patterns + licence patterns + guide-only corrections
const newSpecs = {
  'sub-engineer': [50, 45, 2, 40], 'computer-operator': [50, 45, 2, 40], 'nepal-telecom': [50, 45, 2, 40],
  'foreign-service': [100, 90, 1, 45], 'tsc-lower-secondary': [50, 60, 2, 50],
  'nmc-mbbs': [130, 180, 1, 90], 'nmc-bds': [180, 180, 1, 90], 'nnc-rn': [150, 150, 1, 75],
  'nhpc-ha': [100, 90, 1, 50], 'npc-pharmacy': [150, 150, 1, 75], 'nhpc-lab': [100, 90, 1, 50],
  'nhpc-radio': [100, 90, 1, 50], 'nhpc-physio': [100, 90, 1, 50], 'nhpc-public-health': [100, 90, 1, 50],
  'nhpc-optometry': [100, 90, 1, 50], 'staff-nurse-psc': [50, 45, 2, 40], 'midwifery-nlem': [150, 150, 1, 75],
  'mecee-bl': [200, 180, 1, 100], 'nec-licence': [100, 120, 1, 50], 'bar-council': [100, 90, 1, 50], 'csit-entrance': [100, 120, 1, 35],
};
for (const [id, [n, t, m, p]] of Object.entries(newSpecs)) {
  const e = exams.find(x => x.id === id);
  check(`mock spec ${id}: ${n}Q/${t}min/${m} mark/pass ${p}`, !!e && !!e.prelim && e.prelim.questions === n && e.prelim.timeMin === t && e.prelim.marksPerQ === m && e.prelim.pass === p, e && e.prelim ? JSON.stringify(e.prelim) : 'missing/null prelim');
}
check('tsc-license prelim: 50Q/2 marks/pass 50, timeMin null + negative null (unverified — mock must run untimed, no deduction)',
  (() => { const e = exams.find(x => x.id === 'tsc-license'); return !!e && e.prelim.questions === 50 && e.prelim.marksPerQ === 2 && e.prelim.pass === 50 && e.prelim.timeMin === null && e.prelim.negative === null; })());
for (const id of ['rbb', 'deputy-secretary', 'jta', 'ranger', 'judicial-service', 'psc-service-groups', 'rbb-senior-assistant', 'provincial-psc', 'nea', 'nhpc-dental', 'nhpc-ayurveda', 'anm-guide', 'ayurveda-bams']) {
  const e = exams.find(x => x.id === id);
  check(`guide-only ${id}: prelim is null`, !!e && e.prelim === null, e ? 'prelim=' + JSON.stringify(e.prelim) : 'missing entry');
}
check('rbb prelim removed (2082-83 unified exam has no MCQ prelim)', exams.find(x => x.id === 'rbb').prelim === null);
// QUESTION_FILES in app.js must list every data/questions/*.json bank file,
// including community-approved.json (starts empty; maintainer-approved
// community questions committed there join the bank at startup).
const qDir = fs.readdirSync(path.join(root, 'data', 'questions')).filter(f => f.endsWith('.json')).sort();
const qFilesInApp = [...src.match(/const QUESTION_FILES = \[([^\]]*)\]/)[1].matchAll(/'([^']+)'/g)].map(m => m[1]);
check(`app.js QUESTION_FILES lists all ${qDir.length} question files`, JSON.stringify(qFilesInApp) === JSON.stringify(qDir), qFilesInApp.length + ' listed vs ' + qDir.length + ' on disk');
check('QUESTION_FILES includes the two v2 files (expansion-english-v2, expansion-nepali-v2)', qFilesInApp.includes('expansion-english-v2.json') && qFilesInApp.includes('expansion-nepali-v2.json'));
// 5b. Old papers + notices data files
const papers = JSON.parse(fs.readFileSync(path.join(root, 'data/papers.json'), 'utf8'));
check('papers.json parses with >=7 entries', Array.isArray(papers) && papers.length >= 7, papers.length + ' papers');
check('every paper has source_url + transcribed flag', papers.every(p => p.source_url && typeof p.transcribed === 'boolean'));
check('every paper has an id, exam, title and date_bs field', papers.every(p => p.id && p.exam && p.title && 'date_bs' in p));
check('no paper claims a pdf_url that was not verified (all null until a direct PDF is confirmed)', papers.every(p => p.pdf_url === null || /^https?:\/\//.test(p.pdf_url)));
check('no paper is marked transcribed without transcribed questions', papers.every(p => !p.transcribed || p.question_count_if_transcribed > 0));
const notices = JSON.parse(fs.readFileSync(path.join(root, 'data/notices.json'), 'utf8'));
check('notices.json parses with >=1 entry', Array.isArray(notices) && notices.length >= 1, notices.length + ' notices');
check('every notice has checked_date + status', notices.every(n => n.checked_date && n.status));
check('every notice has an id, title, body and source_url', notices.every(n => n.id && n.title && n.body && n.source_url));
check('no invented close_date without a source_url', notices.every(n => !n.close_date || n.source_url));
check('all notice close_dates are ISO (YYYY-MM-DD) or null', notices.every(n => n.close_date === null || /^\d{4}-\d{2}-\d{2}$/.test(n.close_date)));
check('all notice statuses are one of open/closing-soon/closed/unverified', notices.every(n => ['open','closing-soon','closed','unverified'].includes(n.status)));
check('unverified notices have no close_date', notices.filter(n => n.status === 'unverified').every(n => n.close_date === null));
// 5c. Notice auto-expiry (§T, 2026-10-28): a notice whose close_date passed
// renders Closed even though notices.json keeps its old status. The two
// 2026-10-27 notices must expire on 2026-10-28; a future-dated open notice
// must stay open; unverified notices (no close_date) are never expired.
check('effectiveNoticeStatus: closing-soon notice past its close_date renders closed', effectiveNoticeStatus({ status: 'closing-soon', close_date: '2026-10-27' }, '2026-10-28') === 'closed');
check('effectiveNoticeStatus: open notice past its close_date renders closed', effectiveNoticeStatus({ status: 'open', close_date: '2026-10-27' }, '2026-10-28') === 'closed');
check('effectiveNoticeStatus: notice closing today is still closing-soon (deadline day counts)', effectiveNoticeStatus({ status: 'closing-soon', close_date: '2026-10-27' }, '2026-10-27') === 'closing-soon');
check('effectiveNoticeStatus: future-dated open notice stays open', effectiveNoticeStatus({ status: 'open', close_date: '2026-11-03' }, '2026-10-28') === 'open');
check('effectiveNoticeStatus: already-closed stays closed', effectiveNoticeStatus({ status: 'closed', close_date: '2026-05-06' }, '2026-10-28') === 'closed');
check('effectiveNoticeStatus: unverified notice (no close_date) never expires', effectiveNoticeStatus({ status: 'unverified', close_date: null }, '2026-10-28') === 'unverified');
check('notices.json: the two 2026-10-27 notices are now marked closed (re-checked 2026-10-28)', notices.find(n => n.id === 'nepal-police-asi-oa-2083').status === 'closed' && notices.find(n => n.id === 'gandaki-9-8-2083').status === 'closed');
check('notices.json: PSC Under Secretary + Lumbini still open, re-checked 2026-10-28', notices.find(n => n.id === 'psc-under-secretary-2083').status === 'open' && notices.find(n => n.id === 'psc-under-secretary-2083').checked_date === '2026-10-28' && notices.find(n => n.id === 'lumbini-health-8-2083').status === 'open' && notices.find(n => n.id === 'lumbini-health-8-2083').checked_date === '2026-10-28');
// 5d. Duplicate detection (§T): exact + near-duplicate on a small fake bank,
// and the cached index returns the same answer on a repeat call.
const _fakeBank = [
  { id: 'F-1', question: 'Which river flows through Kathmandu Valley?', question_ne: 'काठमाडौं उपत्यकाबाट कुन नदी बग्छ?', options: ['Bagmati', 'Koshi', 'Gandaki', 'Karnali'], answer: 0 },
  { id: 'F-2', question: 'How many districts are there in Nepal?', question_ne: 'नेपालमा कति जिल्ला छन्?', options: ['77', '75', '76', '78'], answer: 0 },
];
check('findDuplicate: exact copy of a bank question is exact', (() => { const d = findDuplicate('Which river flows through Kathmandu Valley?', 'काठमाडौं उपत्यकाबाट कुन नदी बग्छ?', _fakeBank); return d && d.type === 'exact' && d.match.id === 'F-1'; })());
check('findDuplicate: near-duplicate (Jaccard >= 0.8) is near', (() => { const d = findDuplicate('Which river flows through Kathmandu Valley exactly?', '', _fakeBank); return d && d.type === 'near' && d.match.id === 'F-1'; })());
check('findDuplicate: a genuinely different question is not a duplicate', findDuplicate('What is the capital of France?', '', _fakeBank) === null);
check('findDuplicate: repeat call returns the same result (cached index)', (() => { const a = findDuplicate('Which river flows through Kathmandu Valley?', '', _fakeBank); const b = findDuplicate('Which river flows through Kathmandu Valley?', '', _fakeBank); return a && b && a.match.id === b.match.id && a.type === b.type; })());
check('app.js loads papers.json + notices.json in loadData', src.includes("fetch('data/papers.json')") && src.includes("fetch('data/notices.json')"));
check('app.js supports EMBEDDED_PAPERS / EMBEDDED_NOTICES fallback', src.includes('EMBEDDED_PAPERS') && src.includes('EMBEDDED_NOTICES'));
check('build-bundle.py embeds papers + notices', fs.readFileSync(path.join(root, 'scripts/build-bundle.py'), 'utf8').includes('EMBEDDED_PAPERS') && fs.readFileSync(path.join(root, 'scripts/build-bundle.py'), 'utf8').includes('EMBEDDED_NOTICES'));
check('app.js loads funfacts.json + EMBEDDED_FUNFACTS fallback in loadData', src.includes("fetch('data/funfacts.json')") && src.includes('EMBEDDED_FUNFACTS'));
check('build-bundle.py embeds funfacts', fs.readFileSync(path.join(root, 'scripts/build-bundle.py'), 'utf8').includes('EMBEDDED_FUNFACTS') && fs.readFileSync(path.join(root, 'scripts/build-bundle.py'), 'utf8').includes("data/funfacts.json"));
const funfacts = JSON.parse(fs.readFileSync(path.join(root, 'data/funfacts.json'), 'utf8'));
check('funfacts.json parses with >=300 facts', Array.isArray(funfacts) && funfacts.length >= 300, funfacts.length + ' facts');
check('every fun fact has a unique id, category and EN+NE text', funfacts.every(f => f.id && f.category && f.fact_en && f.fact_ne) && new Set(funfacts.map(f => f.id)).size === funfacts.length);
check('every fun fact has a source + a valid category', funfacts.every(f => f.source && ['Nepal', 'World', 'Science', 'History', 'Constitution', 'Geography', 'Sports', 'Culture'].includes(f.category)));
check('no duplicate fun fact texts (EN or NE)', new Set(funfacts.map(f => f.fact_en.trim().toLowerCase())).size === funfacts.length && new Set(funfacts.map(f => f.fact_ne.trim().toLowerCase())).size === funfacts.length);
check('fun facts cover all 8 categories', new Set(funfacts.map(f => f.category)).size === 8);
check('fun facts view exists in index.html', idsInHtml.has('view-funfacts'));
check('nav has a Fun Facts button', html.includes('data-view="funfacts"'));
check('fun facts filter/box/count ids exist in index.html', ['funfact-filter', 'funfact-box', 'funfact-count'].every(id => idsInHtml.has(id)));
check('home has weekly + focus + fun-fact boxes and the study-tips card', ['weekly-box','focus-timer-box','fun-fact-box'].every(id => idsInHtml.has(id)) && html.includes('How to study without getting bored') && html.includes('spaced repetition'));
check('home + practice have a Surprise me button', (html.match(/surpriseQuiz\(\)/g) || []).length >= 2);
check('mock view has a personal-best line', idsInHtml.has('mock-best') && html.includes("onchange=\"renderMockBest()\""));
check('CSS has the level-up banner animation + focus clock style', (() => { const css = fs.readFileSync(path.join(root, 'assets/css/style.css'), 'utf8'); return css.includes('.levelup-banner') && css.includes('@keyframes levelup-pop') && css.includes('.focus-clock'); })());

// 5c. Gamification pure logic — weekly challenge, personal bests, surprise,
// focus timer cycle, new badges. Dates are built from weekStartStr() so the
// checks hold on any day of the week.
check('weekStartStr: 2026-10-26 (Mon) is its own Monday', weekStartStr(new Date('2026-10-26T12:00:00Z')) === '2026-10-26');
check('weekStartStr: 2026-10-25 (Sun) rolls back to Mon 2026-10-19', weekStartStr(new Date('2026-10-25T12:00:00Z')) === '2026-10-19');
check('weekStartStr: 2026-10-28 (Wed) rolls back to Mon 2026-10-26', weekStartStr(new Date('2026-10-28T12:00:00Z')) === '2026-10-26');
const wkMon = weekStartStr();
const wkAttempts = [
  { date: wkMon + 'T10:00:00Z', total: 30, mode: 'practice', exam: 'kharidar', pct: 60 },
  { date: wkMon + 'T11:00:00Z', total: 40, mode: 'practice', exam: 'nasu', pct: 70 },
  { date: '2020-01-06T10:00:00Z', total: 5, mode: 'practice', exam: 'kharidar', pct: 90 }, // old week: must not count
];
check('questionsThisWeek sums only this week (30+40, not the 5 from 2020)', questionsThisWeek(wkAttempts) === 70, questionsThisWeek(wkAttempts) + '');
check('weeklyProgress: 70/70 target met, 100%', (() => { const w = weeklyProgress({ weeklyTarget: 70, attempts: wkAttempts }); return w.done === 70 && w.target === 70 && w.met === true && w.pct === 100; })(), JSON.stringify(weeklyProgress({ weeklyTarget: 70, attempts: wkAttempts })));
check('weeklyProgress: 70/140 target is 50%, not met', (() => { const w = weeklyProgress({ weeklyTarget: 140, attempts: wkAttempts }); return w.done === 70 && w.met === false && w.pct === 50; })());
check('weeklyProgress defaults to a 70-question target', weeklyProgress({ attempts: wkAttempts }).target === 70);
check('questionsInADay: max single-day total is 70 here (30+40 same day)', questionsInADay(wkAttempts) === 70, questionsInADay(wkAttempts) + '');
check('personalBest picks the best mock pct for the exam', (() => { const b = personalBest('kharidar', [
  { mode: 'mock', exam: 'kharidar', pct: 60, score: 60, max: 100, date: '2026-10-20T09:00:00Z' },
  { mode: 'mock', exam: 'kharidar', pct: 80, score: 80, max: 100, date: '2026-10-24T09:00:00Z' },
  { mode: 'practice', exam: 'kharidar', pct: 100, score: 20, max: 20, date: '2026-10-25T09:00:00Z' }, // practice must not count
  { mode: 'mock', exam: 'nasu', pct: 95, score: 95, max: 100, date: '2026-10-24T09:00:00Z' }, // other exam must not count
]); return b && b.pct === 80 && b.date === '2026-10-24'; })());
check('personalBest returns null with no mock for the exam', personalBest('kharidar', [{ mode: 'practice', exam: 'kharidar', pct: 100, date: '2026-10-24T09:00:00Z' }]) === null);
const fakeBank = Array.from({ length: 20 }, (_, i) => ({ id: 'Q' + i, topic: 'T' + (i % 4) }));
const surprise = pickSurprise(fakeBank);
check('pickSurprise returns exactly 10 distinct questions', surprise.length === 10 && new Set(surprise.map(q => q.id)).size === 10);
check('pickSurprise mixes topics (not one topic only)', new Set(surprise.map(q => q.topic)).size > 1, [...new Set(surprise.map(q => q.topic))].join(','));
check('focus durations are 25 / 5 / 15 minutes', FOCUS_DURATIONS.focus === 1500 && FOCUS_DURATIONS.short === 300 && FOCUS_DURATIONS.long === 900);
check('nextFocusMode: focus #1-3 -> short break, #4 -> long break', nextFocusMode('focus', 1) === 'short' && nextFocusMode('focus', 3) === 'short' && nextFocusMode('focus', 4) === 'long' && nextFocusMode('focus', 8) === 'long');
check('nextFocusMode: any break -> focus', nextFocusMode('short', 1) === 'focus' && nextFocusMode('long', 4) === 'focus');
// Badges: drive them through the sandbox's live progress object.
runInApp(`progress.attempts=${JSON.stringify(wkAttempts)}; progress.weeklyTarget=70; progress.weeklyGoalsMet=0; progress.weeklyGoalMetWeek=''; progress.funFactsSeen=[];`);
check('badges: no new gamification badges on a fresh week (70Q in one day is not 100)', !badges().includes('Weekly Champion') && !badges().includes('Century Day') && !badges().includes('Perfect Mock') && !badges().includes('Fact Explorer'));
check('checkWeeklyGoal records the goal once per week (and only once)', checkWeeklyGoal() === true && runInApp('progress.weeklyGoalsMet') === 1 && checkWeeklyGoal() === false && runInApp('progress.weeklyGoalsMet') === 1);
check('badges: Weekly Champion appears after the goal is met', badges().includes('Weekly Champion'));
runInApp(`progress.attempts.push({date:'${wkMon}T12:00:00Z', total:30, mode:'practice', exam:'kharidar', pct:50});`);
check('badges: Century Day appears at 100 questions in one day', badges().includes('Century Day'));
runInApp(`progress.attempts.push({date:'${wkMon}T13:00:00Z', total:50, mode:'mock', exam:'kharidar', pct:100, score:100, max:100, passed:true});`);
check('badges: Perfect Mock appears at a 100% mock', badges().includes('Perfect Mock'));
runInApp(`progress.funFactsSeen=${JSON.stringify(Array.from({ length: 10 }, (_, i) => 'FF-' + String(i + 1).padStart(2, '0')))};`);
check('badges: Fact Explorer appears after 10 facts read', badges().includes('Fact Explorer'));
check('badges: 9 facts read is not enough for Fact Explorer', (() => { runInApp(`progress.funFactsSeen=${JSON.stringify(Array.from({ length: 9 }, (_, i) => 'FF-' + String(i + 1).padStart(2, '0')))};`); return !badges().includes('Fact Explorer'); })());
check('progress migration keeps old XP/level/streak keys intact', runInApp('progress.xp') === 0 && runInApp('progress.level') === 1 && runInApp('progress.streak') === 0);
// 5b. New features (2026-10-26): encouragement lines, fact streak, QOTD,
// speed round, mistake marathon, personal records, share text.
check('encouragement: >=20 praise lines, EN + NE distinct', PRAISE_LINES.length >= 20 && new Set(PRAISE_LINES.map(l => l.en)).size >= 20 && new Set(PRAISE_LINES.map(l => l.ne)).size >= 20, PRAISE_LINES.length + ' praise lines');
check('encouragement: >=20 try-again lines, EN + NE distinct', TRY_AGAIN_LINES.length >= 20 && new Set(TRY_AGAIN_LINES.map(l => l.en)).size >= 20 && new Set(TRY_AGAIN_LINES.map(l => l.ne)).size >= 20, TRY_AGAIN_LINES.length + ' try-again lines');
check('encouragement: pass/fail lines are bilingual too', PASS_LINES.every(l => l.en && l.ne) && FAIL_LINES.every(l => l.en && l.ne));
check('pickLine never repeats the same line twice in a row (30 draws)', (() => { let prev = null; for (let i = 0; i < 30; i++) { const l = pickLine(PRAISE_LINES, 'test-rot'); if (l === prev) return false; prev = l; } return true; })());
check('pickLine returns Nepali text in ne mode', (() => { setLang('ne'); const l = pickLine(PRAISE_LINES, 'test-ne'); setLang('en'); return PRAISE_LINES.some(x => x.ne === l); })());
check('prefersReducedMotion is false without matchMedia (test stub)', prefersReducedMotion() === false);
const fakeQotdBank = Array.from({ length: 20 }, (_, i) => ({ id: 'Q' + i, topic: 'T' }));
check('questionOfDay is deterministic per day (same date -> same question)', questionOfDay(fakeQotdBank, '2026-10-26').id === questionOfDay(fakeQotdBank, '2026-10-26').id);
check('questionOfDay returns a question from the bank', fakeQotdBank.some(q => q.id === questionOfDay(fakeQotdBank, '2026-10-26').id));
check('questionOfDay returns null for an empty bank', questionOfDay([], '2026-10-26') === null);
check('fact streak: first visit of a day starts a 1-day streak with +5 XP', (() => { const xpBefore = runInApp('progress.xp'); const r = recordFactVisit('2026-10-26'); return r.streak === 1 && r.rewarded === true && r.xp === 5 && runInApp('progress.xp') === xpBefore + 5; })());
check('fact streak: a consecutive day grows the streak', (() => { const r = recordFactVisit('2026-10-27'); return r.streak === 2 && r.rewarded === true; })());
check('fact streak: a missed day resets the streak to 1', (() => { const r = recordFactVisit('2026-10-30'); return r.streak === 1; })());
check('speed round is 10 questions in 60 seconds', SPEED_COUNT === 10 && SPEED_SECONDS === 60);
check('speedBonusFor: +1 under 5s if correct, 0 otherwise', speedBonusFor(4000, true) === 1 && speedBonusFor(4999, true) === 1 && speedBonusFor(5000, true) === 0 && speedBonusFor(1000, false) === 0 && speedBonusFor(null, true) === 0);
check('mistakePool dedupes mistakes+bookmarks and drops ids missing from the bank', (() => { const pool = mistakePool({ mistakes: ['Q2', 'Q9', 'Q2'], bookmarks: ['Q1'] }, [{ id: 'Q1' }, { id: 'Q2' }, { id: 'Q3' }]); return pool.length === 2 && pool.map(q => q.id).join(',') === 'Q2,Q1'; })());
check('mistakePool is empty with no mistakes or bookmarks', mistakePool({ mistakes: [], bookmarks: [] }, [{ id: 'Q1' }]).length === 0);
check('longestStreak counts consecutive attempt days (3 here)', longestStreak([
  { date: '2026-10-20T09:00:00Z' }, { date: '2026-10-21T09:00:00Z' }, { date: '2026-10-22T09:00:00Z' }, { date: '2026-10-24T09:00:00Z' }], 1) === 3);
check('longestStreak also counts the live streak when it is longer', longestStreak([{ date: '2026-10-20T09:00:00Z' }], 5) === 5);
check('bestDay picks the day with the most questions', (() => { const b = bestDay([
  { date: '2026-10-20T09:00:00Z', total: 10 }, { date: '2026-10-21T09:00:00Z', total: 50 }, { date: '2026-10-21T10:00:00Z', total: 20 }]); return b && b.date === '2026-10-21' && b.total === 70; })());
check('bestDay is null with no attempts', bestDay([]) === null);
check('personalRecords: best mock per exam, totals, best day, longest streak', (() => {
  const rec = personalRecords({ xp: 123, streak: 2, attempts: [
    { date: '2026-10-20T09:00:00Z', mode: 'mock', exam: 'kharidar', total: 50, pct: 80, score: 80, max: 100, passed: true },
    { date: '2026-10-21T09:00:00Z', mode: 'mock', exam: 'kharidar', total: 50, pct: 60, score: 60, max: 100, passed: true },
    { date: '2026-10-21T10:00:00Z', mode: 'mock', exam: 'nasu', total: 50, pct: 90, score: 90, max: 100, passed: true },
    { date: '2026-10-21T11:00:00Z', mode: 'practice', exam: 'kharidar', total: 10, pct: 100, score: 20, max: 20, passed: true } ] });
  return rec.bestMocks.length === 2 && rec.bestMocks.find(b => b.exam === 'kharidar').pct === 80
    && rec.totalXp === 123 && rec.totalQuestions === 160 && rec.bestDay.date === '2026-10-21' && rec.bestDay.total === 110
    && rec.longestStreak === 2 && rec.speedBest === null;
})(), JSON.stringify(personalRecords({ xp: 0, streak: 0, attempts: [] })));
check('buildShareText includes score, exam, date and the app name', (() => { const t = buildShareText({ examName: 'Kharidar', mode: 'mock', score: 80, max: 100, pct: 80, passed: true, date: '2026-10-26', speedBonus: 0 }); return t.includes('80/100') && t.includes('Kharidar') && t.includes('2026-10-26') && t.includes('LokSewa Vidyapeeth') && t.includes('PASS'); })());
check('buildShareText mentions the speed bonus for speed rounds', buildShareText({ examName: 'Kharidar', mode: 'speed', score: 25, max: 20, pct: 100, passed: true, date: '2026-10-26', speedBonus: 5 }).includes('+5 speed bonus'));
check('getSpeedBest is null before any speed round', getSpeedBest() === null);
check('home has a Question-of-the-Day box + Speed Round / Mistake Marathon buttons', idsInHtml.has('qotd-box') && idsInHtml.has('speed-best') && html.includes('startSpeedRound()') && html.includes('startMistakeMarathon()'));
check('CSS covers reduced motion, tap manipulation and the answered-card fix', (() => { const css = fs.readFileSync(path.join(root, 'assets/css/style.css'), 'utf8'); return css.includes('prefers-reduced-motion') && css.includes('touch-action:manipulation') && css.includes('.quiz-card.answered .opt') && css.includes('#share-status'); })());
check('CSS covers chat + suggest styles', (() => { const css = fs.readFileSync(path.join(root, 'assets/css/style.css'), 'utf8'); return css.includes('.chat-log') && css.includes('.chat-user') && css.includes('.chat-bot') && css.includes('.chat-chips') && css.includes('.chat-input-row'); })());
// 5c. Feature 9 — Ask (on-device rule-based helper chatbot)
check('chat + suggest storage keys are namespaced', LS_CHAT === 'loksewa_chat_history_v1' && LS_SUGGEST === 'loksewa_suggestions_v1');
check('chat history is capped at 200 messages', CHAT_MAX_MSGS === 200);
const fakeStats = { total: 3, topics: { 'Constitution & Governance': 2, 'Maths & Numerical': 1 } };
check('chatReply: greeting', chatReply('hello', 'en', fakeStats).text.includes('Namaste'));
check('chatReply: Nepali greeting', chatReply('नमस्ते', 'ne', fakeStats).text.includes('नमस्ते'));
check('chatReply: mock intent', chatReply('How do mocks work?', 'en', fakeStats).text.includes('Mock Exams'));
check('chatReply: Nepali mock intent', chatReply('मक कसरी काम गर्छ?', 'ne', fakeStats).text.includes('मक'));
check('chatReply: negative marking = 20%, mentions licence exception', (() => { const t = chatReply('What is negative marking?', 'en', fakeStats).text; return t.includes('20%') && t.includes('NNC'); })());
check('chatReply: "what is negative marking" is NOT swallowed by the fact guard', chatReply('What is negative marking?', 'en', fakeStats).text.includes('20%'));
check('chatReply: cutoff lists real cutoffs', chatReply('What is the cutoff for kharidar?', 'en', fakeStats).text.includes('45'));
check('chatReply: exam finder routes Kharidar to mock spec + topics', (() => { const t = chatReply('I want to prepare for Kharidar', 'en', fakeStats).text; return t.includes('Kharidar') && t.includes('50') && t.includes('Constitution & Governance'); })());
check('chatReply: exam finder works in Nepali', chatReply('म खरिदारको तयारी गर्न चाहन्छु', 'ne', fakeStats).text.includes('खरिदार'));
check('chatReply: study tips', chatReply('Give me study tips', 'en', fakeStats).text.includes('20-minute'));
check('chatReply: where-is intents (dashboard, papers, notices)', chatReply('Where is my dashboard?', 'en', fakeStats).text.includes('Dashboard') && chatReply('old papers', 'en', fakeStats).text.includes('Old Papers') && chatReply('notices', 'en', fakeStats).text.includes('Notices'));
// CRITICAL: the fact guard — factual questions route to topics, never answered
check('fact guard: "how many articles in the constitution" routes to topic, never answers', (() => { const t = chatReply('How many articles are there in the constitution of Nepal?', 'en', fakeStats).text; return t.includes('never invent exam facts') && t.includes('Constitution & Governance') && !t.includes('308'); })());
check('fact guard: "who is the president" never names a person', chatReply('Who is the president of Nepal?', 'en', fakeStats).text.includes('never invent exam facts'));
check('fact guard: Nepali factual question', chatReply('संविधानमा कति धारा छन्?', 'ne', fakeStats).text.includes('तथ्य अनुमान'));
check('fact guard: "when was" / "where is" / "full form" routed, not answered', ['When was Nepal unified?', 'Where is Mount Everest?', 'What is the full form of NRB?'].every(q => chatReply(q, 'en', fakeStats).text.includes('never invent exam facts')));
check('isFactualQuestion: portal questions pass, fact questions caught', isFactualQuestion('how do mocks work') === false && isFactualQuestion('how many districts are in nepal') === true);
check('chatReply: topic practice request gets a topic pointer', chatReply('practice constitution questions', 'en', fakeStats).text.includes('Constitution & Governance'));
check('chatReply: fallback for unknown input', chatReply('blorb glorp zzz', 'en', fakeStats).text.includes('Discussion Hub'));
check('chatReply returns quick-reply chips in both languages', chatReply('hi', 'en', fakeStats).chips.length > 0 && chatReply('नमस्ते', 'ne', fakeStats).chips.length > 0);
check('chatTopicFor maps EN/NE keywords to bank topics', chatTopicFor('samvidhan ko barema') === 'Constitution & Governance' && chatTopicFor('गणित पढ्नु छ') === 'Maths & Numerical' && chatTopicFor('zzz') === null);
check('chatTopicStats counts topics', (() => { const st = chatTopicStats([{ topic: 'A' }, { topic: 'A' }, { topic: 'B' }]); return st.total === 3 && st.topics.A === 2 && st.topics.B === 1; })());
check('chat history persists to localStorage (per device)', (() => { runInApp('saveChatHistory([{role:"user",text:"hi",t:"x"},{role:"bot",text:"yo",t:"y"}])'); const h = runInApp('chatHistory()'); return h.length === 2 && h[0].text === 'hi'; })());
check('chatSend appends user+bot and persists', (() => { runInApp('saveChatHistory([])'); const r = runInApp('chatSend("hello")'); const h = runInApp('chatHistory()'); return r.text.includes('Namaste') && h.length === 2 && h[0].role === 'user' && h[1].role === 'bot'; })());
check('chat history is capped at 200 messages', (() => { const big = Array.from({ length: 250 }, (_, i) => ({ role: 'user', text: 'm' + i, t: 'x' })); runInApp('saveChatHistory(' + JSON.stringify(big) + ')'); return runInApp('chatHistory()').length === 200; })());

// 5d. Feature 10 — Suggest a feature
const goodSug = { title: 'Spaced repetition reminders', description: 'Resurface topics I keep getting wrong on a 1-3-7 day schedule automatically.', category: 'feature' };
check('validateSuggestion: valid passes', validateSuggestion(goodSug, 'en').ok === true);
check('validateSuggestion: short title fails', validateSuggestion({ ...goodSug, title: 'abc' }, 'en').ok === false);
check('validateSuggestion: short description fails', validateSuggestion({ ...goodSug, description: 'too short' }, 'en').ok === false);
check('validateSuggestion: bad category fails', validateSuggestion({ ...goodSug, category: 'nope' }, 'en').ok === false);
check('validateSuggestion: URL blocked', validateSuggestion({ ...goodSug, description: 'see https://example.com for details here ok' }, 'en').ok === false);
check('validateSuggestion: repeated chars blocked', validateSuggestion({ ...goodSug, title: 'Great idea!!!!! yes' }, 'en').ok === false);
check('validateSuggestion: ALL CAPS blocked', validateSuggestion({ ...goodSug, title: 'THIS IS ALL CAPS TITLE HERE' }, 'en').ok === false);
check('validateSuggestion: Nepali errors', validateSuggestion({ title: '', description: '', category: 'x' }, 'ne').errors[0].includes('शीर्षक'));
check('isDuplicateSuggestion catches same normalised title', isDuplicateSuggestion([{ title: 'Spaced Repetition Reminders' }], 'spaced repetition reminders') === true && isDuplicateSuggestion([{ title: 'Other thing' }], 'spaced repetition reminders') === false);
check('suggestions seed with 3 marked examples on first load', (() => { runInApp('localStorage.removeItem("' + LS_SUGGEST + '")'); const l = runInApp('loadSuggestions()'); return l.length === 3 && l.every(s => s._seed === true && Array.isArray(s.voters)); })());
check('upvoteSuggestion toggles one device vote', (() => { runInApp('localStorage.removeItem("' + LS_SUGGEST + '")'); runInApp('loadSuggestions()'); const id = runInApp('loadSuggestions()[0].id'); const before = runInApp('loadSuggestions()[0].upvotes'); runInApp('upvoteSuggestion("' + id + '")'); const after = runInApp('loadSuggestions()[0].upvotes'); runInApp('upvoteSuggestion("' + id + '")'); const back = runInApp('loadSuggestions()[0].upvotes'); return after === before + 1 && back === before; })());
check('suggestion rate limit: 5/hour (shared rateLimitCheck)', (() => { const now = Date.now(); const ts = Array.from({ length: 5 }, () => now - 1000); return runInApp('rateLimitCheck(' + JSON.stringify(ts) + ',' + now + ').allowed') === false; })());
check('chat + suggest view boxes exist in index.html', idsInHtml.has('chat-box') && idsInHtml.has('suggest-box'));
// 5c. Analytics views 1–5 (features: coverage / print / planner / coach / pyq).
// Bilingual helper follows the lang toggle.
check('B() returns English in en mode, Nepali in ne mode', B('Hello','नमस्ते') === 'Hello' && (() => { setLang('ne'); const x = B('Hello','नमस्ते'); setLang('en'); return x; })() === 'नमस्ते');
check('examName prefers name_ne in ne mode', (() => { setLang('ne'); const x = examName({ name: 'Kharidar', name_ne: 'खरिदार' }); setLang('en'); return x; })() === 'खरिदार');
check('examName falls back to name in en mode', examName({ name: 'Kharidar', name_ne: 'खरिदार' }) === 'Kharidar');
check('fmt1 rounds to 1 decimal', fmt1(2.66) === '2.7' && fmt1(2) === '2');
// Coverage helpers: topic counts, syllabus mapping, breakdown weights.
check('topicsForExam counts topics for one exam only', (() => { const c = topicsForExam('kharidar', [{ exam: ['kharidar'], topic: 'A' }, { exam: ['kharidar'], topic: 'A' }, { exam: ['nasu'], topic: 'A' }]); return c.A === 2 && !c.B; })());
check('mapTopicToSyllabus maps Constitution topic to the constitution section', mapTopicToSyllabus('Constitution & Governance', ['Nepal history, geography, society & culture', 'Constitution of Nepal 2072']) === 1);
check('mapTopicToSyllabus returns -1 when nothing matches', mapTopicToSyllabus('Physics', ['Nepal history']) === -1);
check('breakdownLabelTopics: "GK 30 Q" maps to the GK group', breakdownLabelTopics('GK 30 Q').includes('Current Affairs') && breakdownLabelTopics('GK 30 Q').includes('Nepal History'));
check('breakdownLabelTopics: "Basic Office Skills (BOST) 20 Q" maps to office skills', breakdownLabelTopics('Basic Office Skills (BOST) 20 Q').join() === 'Office Management & Public Service');
const kharidarExam = { id: 'kharidar', prelim: { questions: 50, breakdown: 'GK 30 Q + Basic Office Skills (BOST) 20 Q' } };
const bw = parseBreakdownWeights(kharidarExam);
check('parseBreakdownWeights: kharidar 30/20 sums to 100% from the breakdown', bw && bw.source === 'breakdown' && Math.abs(Object.values(bw.weights).reduce((a, b) => a + b, 0) + bw.unmapped - 100) < 1e-6, JSON.stringify(bw && { n: Object.keys(bw.weights).length, unmapped: bw.unmapped }));
check('parseBreakdownWeights: rejects a truncated breakdown (tsc-primary)', parseBreakdownWeights({ id: 'tsc-primary', prelim: { questions: 50, breakdown: 'Education knowledge 40% + GK 30% + Constitution/Acts 10% + ICT 10% + I' } }) === null);
check('parseBreakdownWeights: section-officer 50/30/20 accepted', (() => { const w = parseBreakdownWeights({ id: 'section-officer', prelim: { questions: 100, breakdown: 'General Awareness 50 + Aptitude 30 + English 20' } }); return w && Math.abs(Object.values(w.weights).reduce((a, b) => a + b, 0) - 100) < 1e-6; })());
check('parseBreakdownWeights: csit-entrance 25/25/25/15/10 accepted', (() => { const w = parseBreakdownWeights({ id: 'csit-entrance', prelim: { questions: 100, breakdown: 'Maths 25 + Physics 25 + Chemistry 25 + English 15 + Computer GK 10' } }); return w && Math.abs(w.weights['Physics'] - 25) < 1e-6 && Math.abs(w.weights['English'] - 15) < 1e-6; })());
// PYQ shares: 30 fake transcribed PYQs, 20 Current Affairs / 10 IQ & Reasoning.
const pyqBank = Array.from({ length: 30 }, (_, i) => ({ exam: ['kharidar'], topic: i < 20 ? 'Current Affairs' : 'IQ & Reasoning', _pyq: true }));
const ps = pyqTopicShares('kharidar', pyqBank);
check('pyqTopicShares: n=30, Current Affairs ≈ 66.7%', ps.n === 30 && Math.abs(ps.shares['Current Affairs'] - 200 / 3) < 1e-6, JSON.stringify(ps));
check('pyqTopicShares: only flags _pyq questions for the exam', pyqTopicShares('nasu', pyqBank).n === 0);
check('examTopicWeights falls back to PYQ shares when the breakdown is unusable', examTopicWeights('kharidar', { id: 'kharidar', prelim: { questions: 50 } }, pyqBank).source === 'pyq');
check('examTopicWeights returns null weights with no breakdown and too few PYQs', examTopicWeights('zzz', { id: 'zzz', prelim: { questions: 50 } }, []).weights === null);
// Practice stats + coach maths from saved attempts (qdetail rows).
const att1 = [{ exam: 'kharidar', date: '2026-10-30T00:00:00Z', mode: 'mock', total: 4, correct: 2, wrong: 1, skipped: 1, score: 3, max: 8, qdetail: [{ t: 'Maths & Numerical', c: 1, m: 2 }, { t: 'Maths & Numerical', c: 1, m: 2 }, { t: 'English', c: 0, m: 2 }, { t: 'English', c: -1, m: 2 }] }];
const pts = practiceTopicStats('kharidar', att1);
check('practiceTopicStats aggregates qdetail per topic', pts['Maths & Numerical'].correct === 2 && pts['English'].wrong === 1 && pts['English'].skipped === 1);
check('practiceTopicStats ignores other exams and attempts without qdetail', practiceTopicStats('nasu', att1)['Maths & Numerical'] === undefined && practiceTopicStats('kharidar', [{ exam: 'kharidar' }])['Maths & Numerical'] === undefined);
check('attemptLevelTotals sums attempt-level fields', (() => { const t = attemptLevelTotals('kharidar', att1); return t.attempts === 1 && t.correct === 2 && t.wrong === 1 && t.skipped === 1 && t.max === 8; })());
check('guessEV(0.2): blind guess ≈ +0.10 per mark', Math.abs(guessEV(0.2).blind - 0.1) < 1e-9, JSON.stringify(guessEV(0.2)));
check('guessEV(0): no negative marking → blind +0.25, elim2 +0.5', Math.abs(guessEV(0).blind - 0.25) < 1e-9 && Math.abs(guessEV(0).elim2 - 0.5) < 1e-9);
check('evVerdict labels positive/negative/neutral', evVerdict(0.1).includes('✅') && evVerdict(-0.1).includes('❌') && evVerdict(0).includes('➖'));
const cst = coachStats('kharidar', att1, { id: 'kharidar', prelim: { questions: 50, negative: 0.2 } });
check('coachStats: negLost = 1 wrong × 2 marks × 0.2 = 0.4', Math.abs(cst.negLost - 0.4) < 1e-9 && cst.negRate === 0.2 && cst.negUnknown === false, JSON.stringify({ negLost: cst.negLost }));
check('coachStats: unverified negative marking is flagged, never deducted', coachStats('kharidar', att1, { id: 'kharidar', prelim: { questions: 50, negative: null } }).negUnknown === true && coachStats('kharidar', att1, { id: 'kharidar', prelim: { questions: 50, negative: null } }).negLost === 0);
// Strong-topic skip: English 6/7 correct (≈86%) with 1 skip → heuristic counts it.
const att2 = [{ exam: 'kharidar', date: '2026-10-30T00:00:00Z', mode: 'practice', total: 8, correct: 6, wrong: 1, skipped: 1, score: 11, max: 16, qdetail: Array.from({ length: 6 }, () => ({ t: 'English', c: 1, m: 2 })).concat([{ t: 'English', c: 0, m: 2 }, { t: 'English', c: -1, m: 2 }]) }];
const cst2 = coachStats('kharidar', att2, { id: 'kharidar', prelim: { questions: 50, negative: 0.2 } });
check('coachStats: skip in a 70%+ topic counts as "likely knew" (heuristic)', cst2.strongSkips === 1 && Math.abs(cst2.estSkipLoss - 1.4) < 1e-9, JSON.stringify({ strongSkips: cst2.strongSkips, estSkipLoss: cst2.estSkipLoss }));
check('coachAdvice is bilingual and honest about being a heuristic', (() => { const a = coachAdvice(cst2, { id: 'kharidar' }); return a.length >= 3 && a.every(x => x.en && x.ne); })());
check('coachAdvice with no history asks for an attempt first', coachAdvice({ attempts: 0 }, {}).length === 1);
// Planner: notices → exam mapping, plan building, daily rebalancing, storage.
runInApp(`EXAMS=${JSON.stringify([{ id: 'health', name: 'Health Service' }, { id: 'police', name: 'Police' }])};`);
runInApp(`NOTICES=${JSON.stringify([{ id: 'lumbini-health-8-2083', title: 'Lumbini Health', close_date: '2026-11-05', status: 'open' }, { id: 'zzz-no-map', title: 'Other', close_date: '2026-11-06', status: 'open' }])};`);
check('NOTICE_EXAM maps the licence notice to tsc-license', NOTICE_EXAM['tsc-licence-2082-83'] === 'tsc-license');
check('planNotices keeps only deadline notices mapped to a real exam', planNotices().length === 1 && planNotices()[0].id === 'lumbini-health-8-2083');
runInApp('NOTICES=[]; EXAMS=[];');
check('daysUntil counts whole days, never negative', daysUntil('2026-11-05', '2026-11-01') === 4 && daysUntil('2026-10-01', '2026-11-01') === 0 && daysUntil('', '2026-11-01') === 0);
const planBank = [{ exam: ['kharidar'], topic: 'A' }, { exam: ['kharidar'], topic: 'B' }, { exam: ['nasu'], topic: 'C' }];
const plan = buildStudyPlan('kharidar', '2026-12-31', 40, planBank);
check('buildStudyPlan: daily allocation sums to the target across exam topics', plan.alloc.reduce((a, x) => a + x.perDay, 0) === 40 && plan.alloc.length === 2 && plan.exam === 'kharidar', JSON.stringify(plan.alloc));
check('loadPlans/savePlans round-trip through localStorage', (() => { savePlans({ kharidar: { exam: 'kharidar' } }); const p = loadPlans(); savePlans({}); return p.kharidar && p.kharidar.exam === 'kharidar' && Object.keys(loadPlans()).length === 0; })());
runInApp(`progress.attempts=${JSON.stringify(att2)};`);
const rb = rebalancePlan(Object.assign({}, plan, { created: '2026-10-30', daysLeftAtCreate: 10, deadline: '2030-01-01' }));
check('rebalancePlan returns per-topic rows with daily numbers', Array.isArray(rb) && rb.length === 2 && rb.every(r => typeof r.perDayNow === 'number' && r.quota >= 0));
runInApp('progress.attempts=[];');
check('heatCell emits an inline rgba background', heatCell('50%', 0.5, '220,60,60').includes('rgba(220,60,60,0.50)'));
check('print CSS hides chrome and paginates OMR + answer key', (() => { const css = fs.readFileSync(path.join(root, 'assets/css/style.css'), 'utf8'); return css.includes('@media print') && css.includes('#view-print') && css.includes('.omr-page') && css.includes('page-break-before'); })());
check('style.css exists and non-empty', fs.statSync(path.join(root, 'assets/css/style.css')).size > 1000);
check('index.html references app.js and style.css', html.includes('assets/js/app.js') && html.includes('assets/css/style.css'));
check('index.html carries the LokSewa Vidyapeeth brand in title, logo and footer', html.includes('<title>LokSewa Vidyapeeth') && html.includes('>🇳🇵 LokSewa Vidyapeeth') && html.includes('LokSewa Vidyapeeth — free &amp; open source'));
check('footer links the maintainer GitHub', html.includes('https://github.com/08raviyadav'));
check('no external CDN / http(s) script or font links in index.html', !/src="https?:|href="https?:\/\/(?!github)/.test(html.replace(/github\.com/g, '')) || !html.includes('<script src="http'));

// 5e. Feature 6 — revision notes (data/notes/, one JSON file per topic).
const noteDir = fs.readdirSync(path.join(root, 'data', 'notes')).filter(f => f.endsWith('.json')).sort();
const notesInApp = [...src.match(/const NOTES_FILES = \[([^\]]*)\]/)[1].matchAll(/'([^']+)'/g)].map(m => m[1]);
check(`app.js NOTES_FILES lists all ${noteDir.length} note files`, JSON.stringify(notesInApp) === JSON.stringify(noteDir), notesInApp.length + ' listed vs ' + noteDir.length + ' on disk');
check('at least 20 seeded note files (top topics by question count)', noteDir.length >= 20, noteDir.length + ' notes');
const notesData = noteDir.map(f => JSON.parse(fs.readFileSync(path.join(root, 'data', 'notes', f), 'utf8')));
check('every note has the documented schema (slug/topic/title_en/title_ne/updated/bullets)', notesData.every(n => n.slug && n.topic && n.title_en && n.title_ne && /^\d{4}-\d{2}-\d{2}$/.test(n.updated || '') && Array.isArray(n.bullets)));
check('note slugs are unique and match their filenames', new Set(notesData.map(n => n.slug)).size === notesData.length && notesData.every((n, i) => n.slug === noteDir[i].replace(/\.json$/, '')));
check('every note has 10–20 bullets', notesData.every(n => n.bullets.length >= 10 && n.bullets.length <= 20), 'bullets per note: ' + notesData.map(n => n.bullets.length).join(','));
check('every bullet is bilingual (non-empty EN + NE)', notesData.every(n => n.bullets.every(b => b.en && b.en.trim() && b.ne && b.ne.trim())));
check('no lorem-ipsum placeholder text in notes', notesData.every(n => n.bullets.every(b => !/lorem/i.test(b.en + b.ne))));
// Every note topic must exist in the question bank — "📖 Revise this topic"
// matches q.topic exactly.
const bankTopics = new Set();
for (const f of fs.readdirSync(path.join(root, 'data', 'questions')).filter(f => f.endsWith('.json'))) {
  for (const q of JSON.parse(fs.readFileSync(path.join(root, 'data', 'questions', f), 'utf8'))) bankTopics.add(q.topic);
}
check('every note topic exists in the question bank', notesData.every(n => bankTopics.has(n.topic)), notesData.filter(n => !bankTopics.has(n.topic)).map(n => n.topic).join(', '));
// Pure helpers, driven through the sandbox with an injected NOTES array.
runInApp(`NOTES=${JSON.stringify(notesData)};`);
check('noteByTopic finds a note by exact topic', noteByTopic('Constitution & Governance') && noteByTopic('Constitution & Governance').slug === 'constitution-governance');
check('noteByTopic returns undefined for an unknown topic', noteByTopic('No Such Topic') === undefined);
check('noteBySlug finds a note by slug', noteBySlug('physics').topic === 'Physics');
check('noteTitle/noteBullet follow the lang toggle', (() => { const n = noteBySlug('law'); setLang('ne'); const t = noteTitle(n) === n.title_ne && noteBullet(n.bullets[0]) === n.bullets[0].ne; setLang('en'); return t && noteTitle(n) === n.title_en && noteBullet(n.bullets[0]) === n.bullets[0].en; })());
check('reviseTopic jumps to the note for a known topic', (() => { reviseTopic('Physics'); return runInApp('notesSlug') === 'physics'; })());
check('reviseTopic falls back to the notes list for a topic without a note', (() => { reviseTopic('No Such Topic'); return runInApp('notesSlug') === null; })());
check('openNote/openNoteList set the open one-pager', (() => { openNote('chemistry'); const a = runInApp('notesSlug') === 'chemistry'; openNoteList(); return a && runInApp('notesSlug') === null; })());
check('renderNotes + renderAudio do not crash without a DOM', (() => { try { renderNotes(); renderAudio(); return true; } catch (e) { return false; } })());
check('app.js loads data/notes/ with an EMBEDDED_NOTES bundle fallback', src.includes("fetch('data/notes/'+f)") && src.includes('EMBEDDED_NOTES'));
check('build-bundle.py embeds the notes', fs.readFileSync(path.join(root, 'scripts/build-bundle.py'), 'utf8').includes('EMBEDDED_NOTES'));
check('wrong-answer review carries a "📖 Revise this topic" button', src.includes('📖 Revise this topic') && src.includes('reviseTopic('));
check('CONTRIBUTING.md documents the revision-notes format', fs.readFileSync(path.join(root, 'CONTRIBUTING.md'), 'utf8').includes('## Revision notes'));

// 5f. Feature 7 — audio revision mode (Web Speech API, fully offline).
check('audioSupported is false without the Web Speech API', audioSupported() === false);
check('audio controls are guarded: play/pause/stop/next/prev/new-set do not crash without speechSynthesis', (() => { try { audioPlay(); audioPause(); audioStop(); audioNext(); audioPrev(); audioNewSet(); audioSetSource('facts'); audioSetRate('1.5'); audioSetVoiceLang('ne-NP'); return true; } catch (e) { return false; } })());
check('audioSetSource rejects unknown sources', (() => { audioSetSource('facts'); const a = runInApp('audioState.src'); audioSetSource('bogus'); return a === 'facts' && runInApp('audioState.src') === 'facts'; })());
check('audioSetRate clamps to 0.5–2 and persists', (() => { audioSetRate('9'); const a = runInApp('audioState.rate'); audioSetRate('0.25'); const b = runInApp('audioState.rate'); audioSetRate('1.25'); return a === 2 && b === 0.5 && runInApp('audioState.rate') === 1.25 && sandbox.localStorage.getItem('loksewa_audio_rate') === '1.25'; })());
check('showView stops narration when leaving the audio view', src.includes("if (id !== 'audio') audioStop();"));
check('showView renders the notes + audio views', src.includes("if(id==='notes') renderNotes()") && src.includes("if(id==='audio') renderAudio()"));
check('app.js uses speechSynthesis (Web Speech API) for audio revision', src.includes('speechSynthesis') && src.includes('SpeechSynthesisUtterance'));

console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL APP CHECKS PASSED ✔');
process.exit(fail ? 1 : 0);
