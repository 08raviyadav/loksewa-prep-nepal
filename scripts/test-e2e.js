/* End-to-end logic test: runs app.js in a VM with a minimal DOM stub and real
   question data loaded from disk via a fetch stub. Node, no deps.
   Usage: node scripts/test-e2e.js */
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

function makeEl() {
  return { innerHTML: '', textContent: '', value: '', checked: false, disabled: false,
    classList: { add() {}, remove() {}, toggle() {} }, style: {}, dataset: {},
    addEventListener() {}, setAttribute() {}, getContext: () => ({ clearRect() {}, beginPath() {}, moveTo() {}, lineTo() {}, stroke() {}, fillRect() {}, fillText() {} }) };
}
const els = {};
function el(id) { if (!els[id]) els[id] = makeEl(); return els[id]; }
const alerts = [];
const store = {};
const sandbox = { module: { exports: {} }, console,
  localStorage: { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = v; }, removeItem: k => { delete store[k]; } },
  document: { addEventListener() {}, querySelector: s => (s.startsWith('#') ? el(s.slice(1)) : null),
    querySelectorAll: () => [], getElementById: id => el(id) },
  window: {}, alert: m => alerts.push(m), confirm: () => true,
  setInterval: () => 1, clearInterval: () => {},
  fetch: async url => { const p = path.join(root, url); return { json: async () => JSON.parse(fs.readFileSync(p, 'utf8')) }; } };
sandbox.window = { scrollTo: () => {} };
vm.createContext(sandbox);
const src = fs.readFileSync(path.join(root, 'assets/js/app.js'), 'utf8');
vm.runInContext(src, sandbox);
const run = code => vm.runInContext(code, sandbox);

(async () => {
  // Expected count is computed from disk at run time, not hard-coded: the
  // dedupe worker removes questions while this suite runs, so any fixed
  // number goes stale within minutes. The check still proves loadData loads
  // every question file on disk (i.e. QUESTION_FILES is complete). Computed
  // BEFORE loadData, with one retry per file: the dedupe worker rewrites
  // files in place, so a read can catch a file mid-write (torn JSON).
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
  check('loadData loads 47 exams', run('EXAMS.length') === 47);
  check('loadData loads >=7 old papers', run('PAPERS.length') >= 7, run('PAPERS.length') + ' papers');
  check('loadData loads notices', run('NOTICES.length') >= 1, run('NOTICES.length') + ' notices');
  check('every loaded paper has source_url + transcribed flag', run('PAPERS.every(p=>p.source_url && typeof p.transcribed==="boolean")') === true);
  check('every loaded notice has checked_date + status', run('NOTICES.every(n=>n.checked_date && n.status)') === true);
  run('renderPapers()');
  check('papers view renders paper cards with source + scanned label', el('papers-box').innerHTML.includes('Scanned paper') && el('papers-box').innerHTML.includes('Open Original'));
  run('renderNotices()');
  check('notices view renders notice cards with status + checked date (re-checked 2026-10-28, expired notices auto-closed)', el('notices-box').innerHTML.includes('2026-10-28') && el('notices-box').innerHTML.includes('Open') && el('notices-box').innerHTML.includes('Closed'));
  el('notices-status').value = 'unverified';
  run('renderNotices()');
  check('notices status filter (unverified) narrows the list', (el('notices-box').innerHTML.match(/Unverified/g) || []).length >= 1 && !el('notices-box').innerHTML.includes('>Open<'));
  el('notices-status').value = '';
  run('renderNotices()');
  // Transcribed paper: practicePaper starts a quiz with its real questions.
  run("practicePaper('nasu-first-2083-01-20')");
  check('practicePaper on a transcribed paper starts a quiz with its 43 questions', run('current.questions.length') === 43 && run('current.questions.every(q=>q.source.includes("NaSu First Paper 2083-01-20"))'));
  // Untranscribed paper (Kharidar pretest — no answer key exists): practicePaper alerts instead of starting a quiz.
  const alertsBeforePaper = alerts.length;
  run("practicePaper('kharidar-pretest-2083-06-04')");
  check('practicePaper on an untranscribed paper alerts and does not start a quiz', alerts.length === alertsBeforePaper + 1 && (alerts[alerts.length - 1] || '').includes('not been transcribed'));

  // --- Practice: 10 Q, all correct ---
  el('practice-exam').value = 'kharidar'; el('practice-topic').value = ''; el('practice-diff').value = '';
  el('practice-count').value = '10'; el('practice-timer').checked = false; el('practice-neg').checked = true;
  run('startPractice()');
  check('practice starts with 10 questions', run('current.questions.length') === 10);
  const firstOrder = run('current.questions.map(q=>q.id).join(",")');
  for (let i = 0; i < 10; i++) { run('answerOption(current.questions[current.idx].answer)'); if (i < 9) run('nextQ()'); }
  run('finishAttempt(false)');
  const resHtml = el('result-box').innerHTML;
  check('all-correct practice scores 100% and PASS', resHtml.includes('100%') && resHtml.includes('PASS'), resHtml.slice(0, 200));
  check('XP recorded in localStorage progress', JSON.parse(store['loksewa_progress_v1']).xp > 0);

  // --- Randomisation: a second set differs in both question order and option order ---
  run('startPractice()');
  const secondOrder = run('current.questions.map(q=>q.id).join(",")');
  check('second random set has a different question order', firstOrder !== secondOrder);
  const optOrders = new Set(); for (let t = 0; t < 20; t++) { run('startPractice()'); optOrders.add(run('current.questions[0].options.join("|")')); }
  check('option order varies across 20 fresh sets', optOrders.size > 1, optOrders.size + ' distinct first-question option orders');

  // --- Practice topics are filtered by exam (no impossible combinations) ---
  el('practice-exam').value = 'ayurveda-bams';
  run('updatePracticeTopics()');
  const bamsTopics = el('practice-topic').innerHTML;
  // R11 added 2 ayurveda-bams questions: count is now 20 (was 18). Behaviour unchanged — only that topic is listed.
  check('BAMS topic list shows only Health/Technical basics (20)', bamsTopics.includes('Health/Technical basics (20)') && !bamsTopics.includes('Banking &amp; Finance'), bamsTopics.slice(0, 200));
  const alertsBeforeTopic = alerts.length;
  run("startPracticeTopic('Banking & Finance')");
  check("startPracticeTopic('Banking & Finance') for BAMS alerts and does not start a quiz", alerts.length === alertsBeforeTopic + 1 && (alerts[alerts.length - 1] || '').includes("No 'Banking & Finance' questions tagged for Ayurveda Licence"));
  el('practice-exam').value = 'kharidar';
  run('updatePracticeTopics()');
  const khTopics = el('practice-topic').innerHTML;
  check('Kharidar topic list includes Banking & Finance with a count', khTopics.includes('Banking &amp; Finance ('), khTopics.slice(0, 200));
  // R11 filled JTA (0 -> 42 tagged via the agri file), so no exam has zero tagged questions any more.
  // The old "no questions" check is replaced: JTA must now list real topics, and the
  // no-questions code path is still covered by the BAMS Banking & Finance alert check above.
  el('practice-exam').value = 'jta';
  run('updatePracticeTopics()');
  check('JTA (filled by R11) now lists tagged topics instead of the no-questions option', !el('practice-topic').innerHTML.includes('No questions tagged for this exam yet') && el('practice-topic').innerHTML.includes('('), el('practice-topic').innerHTML.slice(0, 200));
  el('practice-exam').value = 'kharidar'; el('practice-topic').value = ''; el('practice-diff').value = '';

  // --- Mock: Kharidar 50Q, 25 right / 25 wrong -> 50 - 10 = 40, FAIL vs cutoff 45 ---
  el('mock-exam').value = 'kharidar';
  run('startMock()');
  check('mock starts with 50 questions', run('current.questions.length') === 50);
  check('mock questions are 2 marks each', run('current.questions.every(q=>q.marks===2)'));
  check('mock timer set to 45 min', run('timeLeft') === 2700);
  for (let i = 0; i < 50; i++) {
    const ans = i < 25 ? run('current.questions[current.idx].answer') : (run('current.questions[current.idx].answer') + 1) % 4;
    run(`answerOption(${ans})`); if (i < 49) run('nextQ()');
  }
  run('finishAttempt(false)');
  const mockHtml = el('result-box').innerHTML;
  check('mock 25 right / 25 wrong scores 40/100 and FAILS cutoff 45', mockHtml.includes('40 / 100') && mockHtml.includes('FAIL'), mockHtml.slice(0, 140));

  // --- Daily challenge is deterministic per day (same seed -> same set) ---
  run('dailyChallenge()'); const d1 = run('current.questions.map(q=>q.id).join(",")');
  run('dailyChallenge()'); const d2 = run('current.questions.map(q=>q.id).join(",")');
  check('daily challenge gives the same 10 questions twice on the same day', d1 === d2 && run('current.questions.length') === 10);

  // --- Quick quiz, flashcards, search, bookmarks ---
  run('quickQuiz()'); check('quick quiz is 5 questions', run('current.questions.length') === 5);
  run('startFlashcards()'); check('flashcards load 20 cards', run('flashQs.length') === 20);
  el('search-input').value = 'Everest'; el('search-topic').value = '';
  run('doSearch()'); check('search for Everest returns results', el('search-results').innerHTML.includes('Everest'));
  run('startPractice()'); run('bookmarkCurrent()');
  check('bookmark saved to progress', JSON.parse(store['loksewa_progress_v1']).bookmarks.length === 1);
  // wrong answer lands in mistakes
  run('startPractice()'); run('answerOption((current.questions[0].answer+1)%4)');
  check('wrong answer saved to mistakes', JSON.parse(store['loksewa_progress_v1']).mistakes.length >= 1);
  // dashboard renders without throwing
  run('renderDashboard()'); check('dashboard renders stats', el('dash-stats').innerHTML.includes('XP'));
  run('renderGuide()');
  check('exam guide renders all 47 exams', (el('guide-box').innerHTML.match(/No mock available/g) || []).length + (el('guide-box').innerHTML.match(/Start .* mock/g) || []).length === 47, el('guide-box').innerHTML.length + ' chars');
  check('exam guide shows a Start-mock button for exactly the 33 prelim exams', (el('guide-box').innerHTML.match(/Start .* mock/g) || []).length === 33);
  check('exam guide marks exactly the 14 guide-only exams as no-mock', (el('guide-box').innerHTML.match(/No mock available/g) || []).length === 14);

  // --- Guide-only exams can never start a mock ---
  const beforeMock = run('current');
  const alertsBefore = alerts.length;
  el('mock-exam').value = 'rbb';
  run('startMock()');
  check('startMock refuses a guide-only exam (rbb) and leaves current untouched', run('current') === beforeMock && alerts.length === alertsBefore + 1, alerts[alerts.length - 1] || '');

  // --- TSC licence mock: timeMin null -> untimed, negative null -> no deduction ---
  el('mock-exam').value = 'tsc-license';
  run('startMock()');
  check('tsc-license mock starts with 50 questions', run('current.questions.length') === 50);
  check('tsc-license mock is untimed (timeMin null)', run('current.timerOn') === false);
  check('tsc-license mock applies no negative marking (negative null)', run('current.negOn') === false && run('current.negRate') === 0);
  for (let i = 0; i < 50; i++) {
    const ans = (run('current.questions[current.idx].answer') + 1) % 4;
    run(`answerOption(${ans})`); if (i < 49) run('nextQ()');
  }
  run('finishAttempt(false)');
  check('tsc-license mock, all wrong, scores 0 (no deduction on unverified rule)', el('result-box').innerHTML.includes('0 / 100'), el('result-box').innerHTML.slice(0, 140));

  // --- NNC nursing licence mock: negative 0 -> all wrong scores exactly 0, not negative ---
  el('mock-exam').value = 'nnc-rn';
  run('startMock()');
  check('nnc-rn mock starts with 150 questions, all 1 mark', run('current.questions.length') === 150 && run('current.questions.every(q=>q.marks===1)'));
  check('nnc-rn mock applies no negative marking', run('current.negOn') === false);
  for (let i = 0; i < 150; i++) {
    const ans = (run('current.questions[current.idx].answer') + 1) % 4;
    run(`answerOption(${ans})`); if (i < 149) run('nextQ()');
  }
  run('finishAttempt(false)');
  check('nnc-rn mock, all wrong, scores 0 / 150', el('result-box').innerHTML.includes('0 / 150'), el('result-box').innerHTML.slice(0, 140));

  // --- nmc-bds now has 180 tagged questions = the full paper, so no thin-bank warning ---
  check('kharidar mock (full tagged pool) carries no thin-bank warning', !alerts[0].includes('general bank'));
  el('mock-exam').value = 'nmc-bds';
  const alertsBeforeBds = alerts.length;
  run('startMock()');
  check('nmc-bds mock (180 tagged questions) starts with 180 questions and no general-bank warning',
    run('current.questions.length') === 180 && !alerts[alerts.length - 1].includes('general bank'),
    (alerts[alerts.length - 1] || '').slice(0, 200));

  // --- NMC MBBS mock: 130 MCQs only (CSQs excluded), pass judged at 50% of the real 180 total ---
  el('mock-exam').value = 'nmc-mbbs';
  run('startMock()');
  check('nmc-mbbs mock starts with 130 questions (MCQ part only)', run('current.questions.length') === 130);
  for (let i = 0; i < 130; i++) { run('answerOption(current.questions[current.idx].answer)'); if (i < 129) run('nextQ()'); }
  run('finishAttempt(false)');
  const nmcHtml = el('result-box').innerHTML;
  check('nmc-mbbs mock, all correct, scores 130/130 and PASSES at the 50% cutoff', nmcHtml.includes('130 / 130') && nmcHtml.includes('PASS'), nmcHtml.slice(0, 200));

  // --- Gamification: fun facts, weekly challenge, surprise quiz, focus timer,
  // personal bests, level-up animation, new badges ---
  check('fun facts load from data/funfacts.json', run('FUNFACTS.length') >= 300, run('FUNFACTS.length') + ' facts');
  const factsBefore = run('progress.funFactsSeen.length');
  run('showFunFact()');
  check('fun-fact explorer shows a fact and counts it as read', el('fun-fact-box').innerHTML.includes('Did you know?') && run('progress.funFactsSeen.length') === factsBefore + 1, el('fun-fact-box').innerHTML.slice(0, 120));
  for (let i = 0; i < 9; i++) run('showFunFact()');
  check('reading 10 facts earns the Fact Explorer badge', run('progress.funFactsSeen.length') >= 10 && run('badges()').includes('Fact Explorer'));
  // --- Fun facts view: category filter + shuffle, daily fact, interstitial ---
  run('renderFunFacts()');
  check('fun facts view renders all facts with sources', (el('funfact-box').innerHTML.match(/Source:/g) || []).length >= 300);
  el('funfact-filter').value = 'Nepal';
  run('renderFunFacts()');
  check('fun facts category filter narrows to Nepal only', (el('funfact-box').innerHTML.match(/Source:/g) || []).length === run('FUNFACTS.filter(f=>f.category==="Nepal").length'));
  el('funfact-filter').value = '';
  run('renderFunFacts()');
  check('daily fun fact is deterministic per day and in the bank', run('dailyFunFact().id') === run('dailyFunFact().id') && run('FUNFACTS.some(f=>f.id===dailyFunFact().id)'));
  run('startPractice()');
  for (let i = 0; i < 5; i++) { run('answerOption(current.questions[current.idx].answer)'); if (i < 4) run('nextQ()'); }
  check('fun fact appears after the 5th practice question', el('quiz-box').innerHTML.includes('Did you know?'));
  run('dismissFunFact()');
  check('dismissing the fun fact returns to the question', !el('quiz-box').innerHTML.includes('Did you know?'));
  run('nextQ()');
  for (let i = 5; i < 10; i++) { run('answerOption(current.questions[current.idx].answer)'); if (i < 9) run('nextQ()'); }
  run('finishAttempt(false)');
  check('result screen shows a fun fact', el('result-box').innerHTML.includes('Did you know?'));
  run('renderWeekly()');
  check('weekly challenge card renders with progress bar + target picker', el('weekly-box').innerHTML.includes('Weekly Challenge') && el('weekly-box').innerHTML.includes('progress-bar') && el('weekly-box').innerHTML.includes('Weekly target'));
  run('setWeeklyTarget(100)');
  check('weekly target picker stores the new target', run('progress.weeklyTarget') === 100 && el('weekly-box').innerHTML.includes('100 questions'));
  run('surpriseQuiz()');
  check('surprise quiz is 10 questions', run('current.questions.length') === 10);
  check('surprise quiz mixes topics (not one topic only)', run('new Set(current.questions.map(q=>q.topic)).size') > 1, run('[...new Set(current.questions.map(q=>q.topic))].join(", ")'));
  check('surprise quiz is labelled as a mixed set', el('quiz-box').innerHTML.includes('Surprise Mix'));
  // Focus timer: start / tick / pause / reset / completion (+10 XP, next = break).
  run('focusSetMode("focus")');
  check('focus timer starts at 25:00', run('focusState.seconds') === 1500 && run('focusState.mode') === 'focus');
  run('focusStart()');
  check('focus timer runs after Start', run('focusState.running') === true);
  run('focusTick()'); run('focusTick()'); run('focusTick()');
  check('focus timer ticks down 3 seconds', run('focusState.seconds') === 1497);
  run('focusPause()');
  check('focus timer pauses', run('focusState.running') === false);
  run('focusTick()');
  check('paused focus timer does not tick', run('focusState.seconds') === 1497);
  run('focusReset()');
  check('focus timer resets to 25:00', run('focusState.seconds') === 1500);
  const xpBeforeFocus = run('progress.xp');
  run('focusState.seconds=1; focusState.mode="focus"; focusStart(); focusTick();');
  check('finishing a focus block awards +10 XP and switches to a break', run('progress.focusSessions') === 1 && run('progress.focusMinutes') === 25 && run('progress.xp') === xpBeforeFocus + 10 && run('focusState.mode') === 'short' && run('focusState.seconds') === 300, 'sessions=' + run('progress.focusSessions') + ' xp=' + run('progress.xp'));
  // Personal best: the earlier Kharidar mock scored 40/100 — the mock view
  // must show it as the score to beat; a later perfect mock replaces it.
  el('mock-exam').value = 'kharidar';
  run('renderMockBest()');
  check('mock view shows the personal best (40% Kharidar) before starting', el('mock-best').innerHTML.includes('Beat your best') && el('mock-best').innerHTML.includes('40%'), el('mock-best').innerHTML.slice(0, 160));
  run('startMock()');
  for (let i = 0; i < 50; i++) { run('answerOption(current.questions[current.idx].answer)'); if (i < 49) run('nextQ()'); }
  run('finishAttempt(false)');
  run('renderMockBest()');
  check('personal best updates to 100% after a perfect mock', el('mock-best').innerHTML.includes('100%'), el('mock-best').innerHTML.slice(0, 160));
  check('perfect mock earns the Perfect Mock badge', run('badges()').includes('Perfect Mock'));
  // Level-up animation: drop XP just below the 500-XP boundary, finish a
  // 10-question all-correct practice (+200 XP) and the result must carry the
  // animated LEVEL UP banner.
  run('progress.xp=490; progress.level=1;');
  el('practice-exam').value = 'kharidar'; el('practice-topic').value = ''; el('practice-diff').value = '';
  el('practice-count').value = '10'; el('practice-timer').checked = false; el('practice-neg').checked = true;
  run('startPractice()');
  for (let i = 0; i < 10; i++) { run('answerOption(current.questions[current.idx].answer)'); if (i < 9) run('nextQ()'); }
  run('finishAttempt(false)');
  check('level-up shows the animated LEVEL UP banner on the result', el('result-box').innerHTML.includes('levelup-banner') && el('result-box').innerHTML.includes('LEVEL UP!') && el('result-box').innerHTML.includes('Level 2'), el('result-box').innerHTML.slice(0, 300));
  // Weekly goal: a small target + one more finished set crosses the line once.
  run('progress.weeklyGoalMetWeek=""; progress.weeklyGoalsMet=0; progress.weeklyTarget=5;');
  run('quickQuiz()');
  for (let i = 0; i < 5; i++) { run('answerOption(current.questions[current.idx].answer)'); if (i < 4) run('nextQ()'); }
  run('finishAttempt(false)');
  check('finishing a set past the weekly target records the goal once', run('progress.weeklyGoalsMet') === 1 && run('progress.weeklyGoalMetWeek') !== '');
  check('weekly-goal completion shows the gold banner on the result', el('result-box').innerHTML.includes('Weekly goal smashed'));
  check('weekly goal earns the Weekly Champion badge', run('badges()').includes('Weekly Champion'));
  run('renderWeekly()');
  check('weekly card shows the goal as met', el('weekly-box').innerHTML.includes('Goal met'));
  // Century Day: 100 questions answered in a single day earns the badge.
  const todayIso = new Date().toISOString().slice(0, 10);
  run(`progress.attempts.push({date:'${todayIso}T15:00:00Z', total:100, mode:'practice', exam:'nasu', pct:55, score:110, max:200, passed:true});`);
  check('100 questions in one day earns the Century Day badge', run('badges()').includes('Century Day'));
  // Dashboard renders the new weekly + focus cards without throwing.
  run('renderDashboard()');
  check('dashboard renders weekly + focus timer cards', el('weekly-box-dash').innerHTML.includes('Weekly Challenge') && el('focus-timer-box-dash').innerHTML.includes('Focus Timer'));

  // --- New features (2026-10-26): fact streak, QOTD, speed round,
  // mistake marathon, personal records, share-my-score ---
  // Fact streak: loadData already showed the daily fact once today, so a
  // second visit the same day must NOT award XP again; tomorrow must.
  const xpBeforeFact = run('progress.xp');
  const factAgain = run('recordFactVisit()');
  check('fact streak: second visit the same day earns no extra XP', factAgain.rewarded === false && run('progress.xp') === xpBeforeFact && factAgain.streak >= 1, 'streak=' + factAgain.streak);
  const tomorrowIso = new Date(Date.now() + 864e5).toISOString().slice(0, 10);
  const factTomorrow = run(`recordFactVisit('${tomorrowIso}')`);
  check('fact streak: a consecutive day grows the streak and awards +5 XP once', factTomorrow.streak === factAgain.streak + 1 && factTomorrow.rewarded === true && run('progress.xp') === xpBeforeFact + 5, 'streak=' + factTomorrow.streak);
  check('home fun-fact box shows the fact streak', el('fun-fact-box').innerHTML.includes('Fact streak'));
  // Question of the Day: renders on Home, correct answer earns +10 XP once.
  run('renderQotd()');
  check('question of the day renders on Home with answer options', el('qotd-box').innerHTML.includes('Question of the Day') && el('qotd-box').innerHTML.includes('class="opt'));
  const xpBeforeQotd = run('progress.xp');
  run('answerQotd(questionOfDay(QUESTIONS).answer)');
  check('question of the day: correct answer earns +10 XP and shows the explanation', run('progress.xp') === xpBeforeQotd + 10 && el('qotd-box').innerHTML.includes('Correct!'));
  run('answerQotd(questionOfDay(QUESTIONS).answer)');
  check('question of the day: answering twice the same day earns no more XP', run('progress.xp') === xpBeforeQotd + 10);
  // Speed Round: 10 questions, 60 seconds, fast-correct bonus, best saved.
  run('startSpeedRound()');
  check('speed round starts with 10 questions and a 60-second timer', run('current.questions.length') === 10 && run('current.mode') === 'speed' && run('timeLeft') === 60);
  check('speed round question shows the bonus rule', el('quiz-box').innerHTML.includes('Speed Round') && el('quiz-box').innerHTML.includes('+1 bonus'));
  for (let i = 0; i < 10; i++) { run('answerOption(current.questions[current.idx].answer)'); }
  const speedHtml = el('result-box').innerHTML;
  check('speed round result shows the fast-answer bonus', speedHtml.includes('Speed Round bonus') && speedHtml.includes('+10'), speedHtml.slice(0, 200));
  check('speed round saves a best score in localStorage', (() => { const b = JSON.parse(store['loksewa_speed_best_v1'] || 'null'); return !!b && b.score > 0 && b.pct === 100; })(), store['loksewa_speed_best_v1'] || 'no best saved');
  check('result screen has a Share my score button', speedHtml.includes('Share my score'));
  // Share: clipboard is unavailable in the stub, so shareScore returns the
  // text and leaves it in the status line for copying by hand.
  const shared = run('shareScore()');
  check('share-my-score builds a short summary with score, exam and app name', typeof shared === 'string' && shared.includes('LokSewa Vidyapeeth') && shared.includes('Speed Round') && shared.length < 200, shared);
  check('share-my-score leaves the text in the status line when no clipboard exists', el('share-status').textContent.includes('LokSewa Vidyapeeth'));
  // Mistake Marathon: practices only from mistakes/bookmarks.
  run('startMistakeMarathon()');
  check('mistake marathon starts from mistakes/bookmarks only', run('current.questions.length') > 0 && run('current.questions.every(q=>progress.mistakes.includes(q.id)||progress.bookmarks.includes(q.id))') && el('quiz-box').innerHTML.includes('Mistake Marathon'));
  // …and with none recorded, a friendly empty state instead of a quiz.
  run('progress.mistakes=[]; progress.bookmarks=[]; saveProgress();');
  run('startMistakeMarathon()');
  check('mistake marathon with no mistakes shows a friendly empty state', el('quiz-box').innerHTML.includes('No mistakes or bookmarks yet') && el('quiz-box').innerHTML.includes('Start practicing'));
  // Personal records on the dashboard.
  run('renderDashboard()');
  check('dashboard shows Personal Records (longest streak, totals, best day, best mocks, best speed)', el('dash-stats').innerHTML.includes('Personal Records') && el('dash-stats').innerHTML.includes('Longest streak') && el('dash-stats').innerHTML.includes('Best day') && el('dash-stats').innerHTML.includes('Best mock score per exam') && el('dash-stats').innerHTML.includes('Best Speed Round'));

  // --- §T (2026-10-28): Daily Challenge abandonment must not burn the day ---
  run(`progress.dailyDone={}; saveProgress();`);
  const xpBeforeDaily = run('progress.xp');
  run('dailyChallenge()');
  check('daily challenge: starting it does NOT mark the day done', run(`!(progress.dailyDone||{})[todayStr()]`) === true);
  run(`showView('home')`); // abandon: navigate away mid-challenge
  check('daily challenge: abandoning it leaves the day unmarked (retry keeps full XP)', run(`!(progress.dailyDone||{})[todayStr()]`) === true);
  run('dailyChallenge()');
  for (let i = 0; i < 10; i++) { run('answerOption(current.questions[current.idx].answer)'); if (i < 9) run('nextQ()'); }
  run('finishAttempt(false)');
  check('daily challenge: finishing it marks the day done and awards XP', run(`!!(progress.dailyDone||{})[todayStr()]`) === true && run('progress.xp') > xpBeforeDaily);
  const xpBeforeRepeat = run('progress.xp');
  run('dailyChallenge()');
  for (let i = 0; i < 10; i++) { run('answerOption(current.questions[current.idx].answer)'); if (i < 9) run('nextQ()'); }
  run('finishAttempt(false)');
  check('daily challenge: a repeat run the same day awards 0 XP', run('progress.xp') === xpBeforeRepeat && run('progress.attempts[progress.attempts.length-1].xp') === 0);

  // --- §T (2026-10-28): Reset progress must clear the speed best + fact streak too ---
  run(`saveSpeedBest({score:20, max:20, pct:100, bonus:10, date:todayStr()}); recordFactVisit();`);
  check('reset test setup: speed best + fact streak exist before reset', run('getSpeedBest()') !== null && run('getFactStreak().streak') >= 1);
  run('resetProgress()');
  check('reset progress clears XP/attempts and the local profile name', run('progress.xp') === 0 && run('progress.attempts.length') === 0 && run('progress.name') === '');
  check('reset progress also clears the Best Speed Round', run('getSpeedBest()') === null);
  check('reset progress also clears the Fact streak', run('getFactStreak().streak') === 0);
  check('reset progress keeps the device user_id', run(`typeof progress.user_id === 'string' && progress.user_id.indexOf('local-') === 0`));

  // --- §W (2026-10-31 bug sweep) ---
  // W02: finishAttempt is idempotent — a double-tap (or a timer expiring in
  // the same instant as the last speed-round answer) must not record the
  // attempt twice or award XP twice.
  el('practice-exam').value = 'kharidar'; el('practice-topic').value = ''; el('practice-diff').value = '';
  el('practice-count').value = '5'; el('practice-timer').checked = false; el('practice-neg').checked = true;
  run('startPractice()');
  for (let i = 0; i < 5; i++) { run('answerOption(current.questions[current.idx].answer)'); if (i < 4) run('nextQ()'); }
  const attBeforeW2 = run('progress.attempts.length');
  run('finishAttempt(false)');
  const xpAfterOnceW2 = run('progress.xp'), attAfterOnceW2 = run('progress.attempts.length');
  run('finishAttempt(false)'); // the double-tap / timer race
  check('W02: a second finishAttempt call records no extra attempt and no extra XP',
    run('progress.attempts.length') === attAfterOnceW2 && run('progress.attempts.length') === attBeforeW2 + 1 && run('progress.xp') === xpAfterOnceW2,
    'attempts=' + run('progress.attempts.length') + ' xp=' + run('progress.xp'));

  // W06: speed-round wrong answers join Mistakes (practice + mock already did),
  // so the Mistake Marathon can drill them. Skips are not mistakes.
  run('progress.mistakes=[]; saveProgress();');
  run('startSpeedRound()');
  for (let i = 0; i < 10; i++) {
    const ans = i < 3 ? (run('current.questions[current.idx].answer') + 1) % 4 : run('current.questions[current.idx].answer');
    run(`answerOption(${ans})`);
  }
  check('W06: speed-round wrong answers are saved to Mistakes',
    run('current._wrong.length') === 3 && run('current._wrong.every(q=>progress.mistakes.includes(q.id))'),
    'wrong=' + run('current._wrong.length') + ' mistakes=' + run('progress.mistakes.length'));

  // W09: the Discuss button is hidden during mocks — tapping it navigates
  // away, which stops the timer and silently abandons the attempt. Practice
  // keeps the button (no timer at stake there).
  el('mock-exam').value = 'kharidar';
  run('startMock()');
  check('W09: mock question view has no Discuss button (it would abandon the timed mock)',
    !el('quiz-box').innerHTML.includes('Discuss this question') && el('quiz-box').innerHTML.includes('Report wrong'));
  run('showView("home")'); // abandon the mock
  el('practice-exam').value = 'kharidar'; el('practice-topic').value = ''; el('practice-diff').value = '';
  el('practice-count').value = '5'; el('practice-timer').checked = false; el('practice-neg').checked = true;
  run('startPractice()');
  check('W09: practice question view keeps the Discuss button', el('quiz-box').innerHTML.includes('Discuss this question'));

  // W10: the break nudge no longer claims "your answers so far are safe"
  // (leaving abandons the session — it is never recorded); takeABreak
  // confirms before throwing away a timed session.
  el('practice-count').value = '20';
  run('startPractice()');
  for (let i = 0; i < 20; i++) { run('answerOption(current.questions[current.idx].answer)'); if (i < 19) run('nextQ()'); }
  const nudgeHtml = el('quiz-box').innerHTML;
  check('W10: break nudge appears at 20 answered and honestly says leaving abandons the session',
    nudgeHtml.includes('break-nudge') && !nudgeHtml.includes('answers so far are safe') && nudgeHtml.includes('abandons the session'));
  check('W10: takeABreak confirms before abandoning a timed session',
    run('takeABreak.toString()').includes('confirm(') && run('takeABreak.toString()').includes('timerOn'));
  run('takeABreak()'); // untimed session: no confirm needed, goes home
  check('W10: takeABreak on an untimed session goes home', el('weekly-box').innerHTML.includes('Weekly Challenge'));

  // W11: "New random set" after an exam-less mode (Daily Challenge) must use
  // mixed practice — not whatever exam the select happened to hold.
  run('dailyChallenge()');
  for (let i = 0; i < 10; i++) { run('answerOption(current.questions[current.idx].answer)'); if (i < 9) run('nextQ()'); }
  run('finishAttempt(false)');
  el('practice-exam').value = 'nasu'; // stale leftover selection
  el('practice-count').value = '10';
  run('newRandomSet()');
  check('W11: new random set after the Daily Challenge uses mixed practice, not the stale exam',
    el('practice-exam').value === '' && run('current.exam') === '' && run('current.questions.length') === 10,
    'select=' + el('practice-exam').value + ' exam=' + run('current.exam'));
  check('W11: practice select offers the All-exams mixed option without changing the default exam',
    el('practice-exam').innerHTML.includes('value=""') && el('practice-exam').innerHTML.includes('All exams (mixed)'));

  // W03: rebuilding the selects (e.g. via the Contribute view) must not wipe
  // the user's chosen practice / mock exam.
  el('practice-exam').value = 'nasu';
  run('fillExamSelects()');
  check('W03: fillExamSelects keeps the selected practice exam', el('practice-exam').value === 'nasu');
  el('mock-exam').value = 'nnc-rn';
  run('fillExamSelects()');
  check('W03: fillExamSelects keeps the selected mock exam', el('mock-exam').value === 'nnc-rn');

  // W04: a half-started "discuss this question" must not prefill the Hub when
  // the user opens Discuss on their own afterwards.
  const someQid = run('QUESTIONS[0].id');
  run(`discussQuestion('${someQid}')`);
  check('W04: discussQuestion opens the Hub with the question prefilled', el('discuss-box').innerHTML.includes('My doubt:'));
  run(`showView('home')`);
  run(`showView('discuss')`);
  check('W04: opening Discuss later shows no stale prefill', !el('discuss-box').innerHTML.includes('My doubt:'));

  // W01: a paper with no date_bs cannot match questions by keyword+date —
  // the date check would be vacuous (''.includes('') is true) and an
  // untranscribed 'nasu' paper would wrongly open NaSu First's questions.
  const curBeforeW1 = run('current');
  const alertsBeforeW1 = alerts.length;
  run("practicePaper('nasu-collection-loksewaaspirants')");
  check("W01: practicePaper on an undated paper alerts instead of matching another paper's questions",
    alerts.length === alertsBeforeW1 + 1 && run('current') === curBeforeW1, alerts[alerts.length - 1] || '');

  // W05: the unverified-notice warning shows the notice's own checked_date,
  // not a hardcoded string that goes stale after re-checks. Last check — it
  // appends a notice to NOTICES.
  run(`NOTICES.push({id:'w05-test', title:'W05 test notice', body:'test', source_url:'https://example.com', source_name:'Test', issuer:'Test Body', scope:'nationwide', status:'unverified', close_date:null, open_date:null, posts:null, level:'', fee:'', checked_date:'2026-10-30', title_ne:''})`);
  run('renderNotices()');
  check('W05: unverified warning shows the notice\'s own checked date, not a hardcoded one',
    el('notices-box').innerHTML.includes('dates not verified (last checked 2026-10-30)'));

  console.log(fail ? `\n${fail} E2E CHECK(S) FAILED` : '\nALL E2E CHECKS PASSED ✔');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('E2E CRASH:', e); process.exit(1); });
