/* Outrank — vanilla JS, zero dependencies.
   Scoring: score = correct*marks - wrong*marks*0.20 ; skipped = 0. Rounded to 1 decimal. */
'use strict';
const QUESTION_FILES = [
  'community-approved.json',
  'constitution-governance-economy.json',
  'english-nepali-computer.json',
  'expansion-computer-office-banking.json',
  'expansion-constitution-economy-current-science.json',
  'expansion-core-hard.json',
  'expansion-culture.json',
  'expansion-current-hard.json',
  'expansion-english-nepali-v3.json',
  'expansion-english-v2.json',
  'expansion-entrance-licence.json',
  'expansion-foreign-telecom.json',
  'expansion-geography.json',
  'expansion-hard-core-v2.json',
  'expansion-health-technical-security.json',
  'expansion-health-technical.json',
  'expansion-history.json',
  'expansion-iq-maths.json',
  'expansion-law-csit-ioe.json',
  'expansion-nepali-v2.json',
  'expansion-nhpc-law.json',
  'expansion-pdf-01.json',
  'expansion-pdf-02.json',
  'expansion-pdf-03.json',
  'expansion-pdf-04.json',
  'expansion-pdf-05.json',
  'expansion-pdf-06.json',
  'expansion-pdf-07.json',
  'expansion-pdf-08.json',
  'expansion-pdf-09.json',
  'expansion-pdf-10.json',
  'expansion-pdf-11.json',
  'expansion-pdf-12.json',
  'expansion-pdf-13.json',
  'expansion-pdf-14.json',
  'expansion-pdf-15.json',
  'expansion-pdf-16.json',
  'expansion-r10-current.json',
  'expansion-r10-drills.json',
  'expansion-r10-drills2.json',
  'expansion-r10-english.json',
  'expansion-r10-english2.json',
  'expansion-r10-english3.json',
  'expansion-r10-english4.json',
  'expansion-r10-grammar.json',
  'expansion-r10-health.json',
  'expansion-r10-health2.json',
  'expansion-r10-iq.json',
  'expansion-r10-iq2.json',
  'expansion-r10-iq3.json',
  'expansion-r10-iq4.json',
  'expansion-r10-iq5.json',
  'expansion-r10-iq6.json',
  'expansion-r10-maths.json',
  'expansion-r10-maths10.json',
  'expansion-r10-maths2.json',
  'expansion-r10-maths3.json',
  'expansion-r10-maths4.json',
  'expansion-r10-maths5.json',
  'expansion-r10-maths6.json',
  'expansion-r10-maths7.json',
  'expansion-r10-maths8.json',
  'expansion-r10-maths9.json',
  'expansion-r10-nepal-facts.json',
  'expansion-r10-nepali.json',
  'expansion-r10-nepali2.json',
  'expansion-r10-office-edu-law.json',
  'expansion-r10-science2.json',
  'expansion-r10-vocab5.json',
  'expansion-r10-vocab6.json',
  'expansion-r10-world-science.json',
  'expansion-r11-agri.json',
  'expansion-r11-drills.json',
  'expansion-r11-drills2.json',
  'expansion-r11-drills3.json',
  'expansion-r11-drills4.json',
  'expansion-r11-drills5.json',
  'expansion-r11-drills6.json',
  'expansion-r11-english.json',
  'expansion-r11-english2.json',
  'expansion-r11-english3.json',
  'expansion-r11-grammar.json',
  'expansion-r11-health.json',
  'expansion-r11-iq.json',
  'expansion-r11-iq2.json',
  'expansion-r11-iq3.json',
  'expansion-r11-iq4.json',
  'expansion-r11-iq5.json',
  'expansion-r11-law.json',
  'expansion-r11-maths.json',
  'expansion-r11-maths2.json',
  'expansion-r11-nepal.json',
  'expansion-r11-nepali.json',
  'expansion-r11-nepali2.json',
  'expansion-r11-science.json',
  'expansion-r11-tech.json',
  'expansion-r5-csit-ioe.json',
  'expansion-r5-current-science.json',
  'expansion-r5-dental-ayurveda.json',
  'expansion-r5-foreign-telecom.json',
  'expansion-r5-law.json',
  'expansion-r5-maths-hard.json',
  'expansion-r6a-current.json',
  'expansion-r6a-hard.json',
  'expansion-r6a-thin-exams.json',
  'expansion-r6b-banking-health.json',
  'expansion-r6b-language.json',
  'expansion-r6b-licence-entrance.json',
  'expansion-r7a-licence.json',
  'expansion-r7a-technical.json',
  'expansion-r7b-core-hard.json',
  'expansion-r7b-current.json',
  'expansion-r8-current-language.json',
  'expansion-r8-law-office.json',
  'expansion-r8-nepal.json',
  'expansion-r8-science-health.json',
  'expansion-security-engineering.json',
  'expansion-technical-psc.json',
  'expansion-thin-exams.json',
  'expansion-thin-topics.json',
  'expansion-zero-licence.json',
  'iq-maths.json',
  'license-allied-health.json',
  'license-health-assistant.json',
  'license-medical.json',
  'license-nursing.json',
  'license-pharmacy.json',
  'nepal-history-geography-culture.json',
  'office-banking-education-health.json',
  'previous-year-2083.json',
  'tsc-education.json',
];
// Revision notes: one JSON file per topic in data/notes/ (PR-friendly — see
// CONTRIBUTING.md "Revision notes"). Keep this list sorted; test-app.js
// verifies every data/notes/*.json file on disk is listed here.
const NOTES_FILES = [
  'banking-finance.json',
  'chemistry.json',
  'computer-ict.json',
  'constitution-governance.json',
  'culture-society.json',
  'current-affairs.json',
  'economy-development.json',
  'education-pedagogy.json',
  'english.json',
  'health-technical-basics.json',
  'iq-reasoning.json',
  'law.json',
  'mathematics.json',
  'maths-numerical.json',
  'nepal-geography.json',
  'nepal-history.json',
  'nepali-language.json',
  'office-management-public-service.json',
  'physics.json',
  'science-tech.json',
];
// Theory courses: one file per exam in data/courses/ (CONTRIBUTING.md
// "Theory courses"). Sorted; test-courses.js verifies the on-disk files.
const COURSE_FILES = [
  'kharidar.json',
  'nayab-subba.json',
  'section-officer.json',
];
const LS_KEY = 'loksewa_progress_v1';
// Language: 'en' (default) or 'ne'. Persisted in localStorage as 'loksewa_lang'.
// When 'ne', question/option/explanation text comes from the *_ne fields
// when present, falling back to English where a field is missing.
const LANG_KEY = 'loksewa_lang';
let lang = 'en';
try { const _l = localStorage.getItem(LANG_KEY); if (_l === 'ne' || _l === 'en') lang = _l; } catch (e) {}
function qText(q){ return (lang === 'ne' && q.question_ne) ? q.question_ne : q.question; }
function qOpts(q){ return (lang === 'ne' && Array.isArray(q.options_ne)) ? q.options_ne : q.options; }
function qExpl(q){ return (lang === 'ne' && q.explanation_ne) ? q.explanation_ne : (q.explanation || ''); }
function getLang(){ return lang; }
// Theme: light is the default. The user's explicit choice persists in
// localStorage as 'loksewa_theme' so the toggle survives reloads.
const THEME_KEY = 'loksewa_theme';
function applyTheme(t){
  const theme = (t === 'dark') ? 'dark' : 'light';
  document.documentElement.dataset.theme = theme;
  const b = document.getElementById('theme-toggle');
  if (b) b.textContent = theme === 'dark' ? '🌙 Dark' : '☀️ Light';
}
function toggleTheme(){
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
  applyTheme(next);
}
function setLang(l){
  lang = (l === 'ne') ? 'ne' : 'en';
  try { localStorage.setItem(LANG_KEY, lang); } catch (e) {}
  const b = document.getElementById('lang-toggle');
  if (b) b.textContent = lang === 'ne' ? 'NE · नेपाली' : 'EN · English';
  // Re-render whichever question-bearing view is currently visible.
  const active = document.querySelector('.view.active');
  const id = active ? active.id : '';
  if (id === 'view-quiz' && current) renderQuestion();
  else if (id === 'view-flash') renderFlash();
  else if (id === 'view-review') renderReview();
  else if (id === 'view-result' && current && current._res) renderResult();
  else if (id === 'view-funfacts') renderFunFacts();
  else if (id === 'view-notes') renderNotes();
  else if (id === 'view-audio') { audioStop(); renderAudio(); }
  else if (id === 'view-coverage') renderCoverage();
  else if (id === 'view-print') renderPrint();
  else if (id === 'view-planner') renderPlanner();
  else if (id === 'view-coach') renderCoach();
  else if (id === 'view-pyq') renderPYQ();
  else if (id === 'view-home') { renderFunFact(); renderQotd(); }
  else if (id === 'view-search') doSearch();
  else if (id === 'view-guide') renderGuide();
  else if (id === 'view-papers') renderPapers();
  else if (id === 'view-notices') renderNotices();
  else if (id === 'view-dashboard') renderDashboard();
  else if (id === 'view-profile') renderProfile();
  else if (id === 'view-discuss') renderDiscuss();
  else if (id === 'view-submit') renderSubmit();
  else if (id === 'view-chat') renderChat();
  else if (id === 'view-suggest') renderSuggest();
  else if (id === 'view-practice') { /* labels stay bilingual by design; nothing to re-render */ }
  else if (id === 'view-history') renderHistory();
  else if (id === 'view-today' && typeof renderToday === 'function') renderToday();
  // Countdown card + exam banner follow the language toggle on every view.
  renderExamReminder(); renderFestivalCard(); if (typeof renderBirthdayCard === 'function') renderBirthdayCard(); renderHistoryOtd(); renderNextExamCard(); renderNextExamCompact(); renderContinueStudying(); if (typeof renderBetaBanner === 'function') renderBetaBanner();
}

function shuffle(arr, rand=Math.random){
  const a = arr.slice();
  for (let i=a.length-1;i>0;i--){ const j=Math.floor(rand()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; }
  return a;
}
// Shuffle options and remap the correct answer index. The Nepali options
// (options_ne) are shuffled with the SAME permutation as the English ones,
// so the two lists always stay paired and the answer index stays valid.
function shuffleOptions(q, rand=Math.random){
  const idx = shuffle([0,1,2,3], rand);
  const out = { ...q, options: idx.map(i=>q.options[i]), answer: idx.indexOf(q.answer), _origAnswer: q.answer };
  if (Array.isArray(q.options_ne)) out.options_ne = idx.map(i=>q.options_ne[i]);
  return out;
}
function scoreAttempt(answers, questions, negativeOn=true, negRate=0.2){
  let correct=0, wrong=0, skipped=0, score=0, max=0;
  questions.forEach((q,i)=>{ max+=q.marks; const a=answers[i];
    if (a===null||a===undefined){ skipped++; }
    else if (a===q.answer){ correct++; score+=q.marks; }
    else { wrong++; if(negativeOn) score-=q.marks*negRate; }
  });
  return { correct, wrong, skipped, score: Math.round(score*10)/10, max, pct: max?Math.round((Math.max(score,0)/max)*1000)/10:0 };
}
function xpFor(score, max){ return Math.max(0, Math.round(score*10)); }
// (Node exports live at the end of this file, after every const is
// initialised — an early export here hit the FOCUS_DURATIONS TDZ.)

let QUESTIONS=[], EXAMS=[], PAPERS=[], NOTICES=[], FUNFACTS=[], NOTES=[], EXAMDATES=[], COURSES=[], FESTIVALS=[], HISTORY=[], current=null, timerId=null, timeLeft=0, startTime=0;
let progress = loadProgress();
// Cloud-ready progress shape (see docs/BACKEND.md): the profile fields
// (user_id / email / name) live on the same object as the practice data, so a
// future Supabase sync can upload this object as-is. Old local progress (no
// user_id) is migrated in place — nothing is lost.
function newLocalUserId(){ return 'local-' + Date.now().toString(36) + '-' + Math.floor(Math.random()*1e9).toString(36); }
function migrateProgress(p){
  if (!p.user_id) p.user_id = newLocalUserId();
  if (p.email === undefined) p.email = '';
  if (p.name === undefined) p.name = '';
  // Birthday (BS 'YYYY-MM-DD' or '') — added for the birthday-wish card +
  // My Day digest (see birthday.js). Lives in the same local profile
  // store as name/email: on this device only, never uploaded.
  if (p.birthday === undefined) p.birthday = '';
  if (!Array.isArray(p.attempts)) p.attempts = [];
  if (!Array.isArray(p.bookmarks)) p.bookmarks = [];
  if (!Array.isArray(p.mistakes)) p.mistakes = [];
  // Gamification fields (added Oct 2026): old progress migrates in place —
  // nothing is lost, existing XP/level/streak keys are untouched.
  if (p.weeklyTarget === undefined) p.weeklyTarget = 70;
  if (p.weeklyGoalsMet === undefined) p.weeklyGoalsMet = 0;
  if (p.weeklyGoalMetWeek === undefined) p.weeklyGoalMetWeek = '';
  if (!Array.isArray(p.funFactsSeen)) p.funFactsSeen = [];
  if (p.focusSessions === undefined) p.focusSessions = 0;
  if (p.focusMinutes === undefined) p.focusMinutes = 0;
  if (!p.qotdDone || typeof p.qotdDone !== 'object') p.qotdDone = {};
  return p;
}
function loadProgress(){
  try{ const p=JSON.parse(localStorage.getItem(LS_KEY)||'null'); if(p) return migrateProgress(p); }catch(e){}
  return migrateProgress({ xp:0, level:1, streak:0, lastDay:'', attempts:[], bookmarks:[], mistakes:[], flashcardsSeen:0, dailyDone:{}, qotdDone:{}, weeklyTarget:70, weeklyGoalsMet:0, weeklyGoalMetWeek:'', funFactsSeen:[], focusSessions:0, focusMinutes:0 });
}
function saveProgress(){ try{ localStorage.setItem(LS_KEY, JSON.stringify(progress)); }catch(e){} }
function todayStr(){ return new Date().toISOString().slice(0,10); }
function updateStreak(){
  const t=todayStr(); if(progress.lastDay===t) return;
  const y=new Date(Date.now()-864e5).toISOString().slice(0,10);
  progress.streak = (progress.lastDay===y)? progress.streak+1 : 1;
  progress.lastDay=t; saveProgress();
}
function levelFromXp(xp){ return Math.floor(xp/500)+1; }
function badges(){
  const b=[]; const n=progress.attempts.length;
  if(n>=1) b.push('First Practice'); if(n>=10) b.push('10 Sessions'); if(n>=50) b.push('50 Sessions');
  if(progress.streak>=3) b.push('3-Day Streak'); if(progress.streak>=7) b.push('7-Day Streak'); if(progress.streak>=30) b.push('30-Day Streak');
  if(progress.xp>=1000) b.push('1000 XP'); if(progress.xp>=5000) b.push('5000 XP');
  const passed=progress.attempts.filter(a=>a.passed).length; if(passed>=1) b.push('First Pass'); if(passed>=5) b.push('5 Mock Passes');
  // Gamification badges (Oct 2026) — all computed from existing progress data.
  if(progress.weeklyGoalsMet>=1) b.push('Weekly Champion');
  if(questionsInADay(progress.attempts)>=100) b.push('Century Day');
  if(progress.attempts.some(a=>a.mode==='mock' && a.pct===100)) b.push('Perfect Mock');
  if((progress.funFactsSeen||[]).length>=10) b.push('Fact Explorer');
  return b;
}

/* ---------- Gamification: weekly challenge, personal bests, focus timer,
   surprise quiz, fun facts. All localStorage-only, no backend. ---------- */
// Monday (UTC) of the week containing d — matches todayStr()'s UTC dates.
function weekStartStr(d){
  const t = d ? new Date(d) : new Date();
  const diff = (t.getUTCDay()+6)%7; // days since Monday
  return new Date(Date.UTC(t.getUTCFullYear(), t.getUTCMonth(), t.getUTCDate()-diff)).toISOString().slice(0,10);
}
function questionsThisWeek(attempts, now){
  const start = weekStartStr(now);
  const end = new Date(new Date(start+'T00:00:00Z').getTime()+7*864e5).toISOString().slice(0,10);
  return (attempts||[]).reduce((s,a)=>{ const d=(a.date||'').slice(0,10); return (d>=start && d<end) ? s+(a.total||0) : s; },0);
}
function weeklyProgress(p){
  const target = p.weeklyTarget || 70;
  const done = questionsThisWeek(p.attempts);
  const start = weekStartStr();
  return { target, done, pct: Math.min(100, Math.round(done/target*100)), weekStart: start, met: done>=target };
}
// Called once per finished attempt: first time the weekly goal is met in a
// given week, record it (drives the 'Weekly Champion' badge). Returns true
// only on the attempt that crosses the line.
function checkWeeklyGoal(){
  const w = weeklyProgress(progress);
  if (w.met && progress.weeklyGoalMetWeek !== w.weekStart){
    progress.weeklyGoalMetWeek = w.weekStart;
    progress.weeklyGoalsMet = (progress.weeklyGoalsMet||0)+1;
    saveProgress();
    return true;
  }
  return false;
}
function questionsInADay(attempts){
  const per={};
  (attempts||[]).forEach(a=>{ const d=(a.date||'').slice(0,10); per[d]=(per[d]||0)+(a.total||0); });
  return Math.max(0, ...Object.values(per));
}
// Best mock result for one exam, or null if never attempted as a mock.
function personalBest(examId, attempts){
  const mocks=(attempts||[]).filter(a=>a.mode==='mock' && a.exam===examId);
  if(!mocks.length) return null;
  const best=mocks.reduce((b,a)=> a.pct>b.pct ? a : b, mocks[0]);
  return { pct: best.pct, date: (best.date||'').slice(0,10), score: best.score, max: best.max };
}
// 10 random questions from anywhere in the bank (mixed exams/topics).
function pickSurprise(questions, rand){
  return shuffle(questions||[], rand||Math.random).slice(0,10);
}
function surpriseQuiz(){
  const qs=pickSurprise(QUESTIONS).map(q=>shuffleOptions(q));
  if(!qs.length){ alert(bankNotLoadedMsg()); return; }
  current={ mode:'practice', exam:'', title:'🎲 Surprise Mix', questions:qs, answers:Array(qs.length).fill(null), idx:0, negOn:true, negRate:0.2, timerOn:false, startTime:Date.now(), perQ:[] };
  showView('quiz'); renderQuestion();
}

/* ----- Speed Round + Mistake Marathon ----- */
const SPEED_BEST_KEY = 'loksewa_speed_best_v1';
const SPEED_SECONDS = 60, SPEED_COUNT = 10, SPEED_FAST_MS = 5000;
function getSpeedBest(){ return lsGet(SPEED_BEST_KEY, null); }
function saveSpeedBest(rec){ lsSet(SPEED_BEST_KEY, rec); return rec; }
// +1 bonus point for a correct answer given in under 5 seconds.
function speedBonusFor(elapsedMs, correct){ return (correct && elapsedMs != null && elapsedMs < SPEED_FAST_MS) ? 1 : 0; }
function startSpeedRound(){
  const qs = shuffle(QUESTIONS).slice(0, SPEED_COUNT).map(q => shuffleOptions(q));
  if (!qs.length) { alert(bankNotLoadedMsg()); return; }
  current = { mode: 'speed', exam: '', title: '⚡ Speed Round', questions: qs, answers: Array(qs.length).fill(null), idx: 0, negOn: true, negRate: 0.2, timerOn: true, startTime: Date.now(), qStart: Date.now(), perQ: [] };
  timeLeft = SPEED_SECONDS; startTimer(() => finishAttempt(true));
  showView('quiz'); renderQuestion();
}
// Questions the user got wrong or bookmarked (deduped, bank order kept
// until shuffled by the caller). Pure — takes progress + bank as inputs.
function mistakePool(p, questions){
  const ids = [...new Set([...(p.mistakes || []), ...(p.bookmarks || [])])];
  const byId = new Map((questions || []).map(q => [q.id, q]));
  return ids.map(id => byId.get(id)).filter(Boolean);
}
function startMistakeMarathon(){
  const pool = shuffle(mistakePool(progress, QUESTIONS));
  if (!pool.length) {
    // Friendly empty state (not an alert): the marathon needs material first.
    showView('quiz');
    const box = document.getElementById('quiz-box');
    if (box) box.innerHTML = `<div class="card"><h2>🏃 Mistake Marathon</h2>
      <p><strong>No mistakes or bookmarks yet — nothing to revise!</strong></p>
      <p class="muted">Do a practice set first: every wrong answer is saved automatically, and anything you bookmark with 🔖 joins the marathon too. Then come back here and we will drill exactly the questions you missed.</p>
      <button class="btn" onclick="showView('practice')">Start practicing →</button>
      <button class="btn secondary" onclick="showView('review')">View Bookmarks &amp; Mistakes</button></div>`;
    return;
  }
  const qs = pool.slice(0, 20).map(q => shuffleOptions(q));
  current = { mode: 'practice', exam: '', title: '🏃 Mistake Marathon', questions: qs, answers: Array(qs.length).fill(null), idx: 0, negOn: true, negRate: 0.2, timerOn: false, startTime: Date.now(), perQ: [] };
  showView('quiz'); renderQuestion();
}

/* ----- Personal records (Stats view) — personal only, no leaderboard ----- */
// Longest run of consecutive calendar days with at least one attempt, also
// counting the live streak (which may include days with no finished attempt
// yet, e.g. a QOTD-only day). Pure — takes attempts + current streak.
function longestStreak(attempts, currentStreak){
  const days = [...new Set((attempts || []).map(a => (a.date || '').slice(0, 10)).filter(Boolean))].sort();
  let best = 0, run = 0, prev = null;
  days.forEach(d => {
    if (prev && new Date(d + 'T00:00:00Z').getTime() - new Date(prev + 'T00:00:00Z').getTime() === 864e5) run++;
    else run = 1;
    prev = d; if (run > best) best = run;
  });
  return Math.max(best, currentStreak || 0);
}
// The single day with the most questions answered, or null if no attempts.
function bestDay(attempts){
  const per = {};
  (attempts || []).forEach(a => { const d = (a.date || '').slice(0, 10); if (d) per[d] = (per[d] || 0) + (a.total || 0); });
  let bd = null;
  Object.entries(per).forEach(([date, total]) => { if (!bd || total > bd.total) bd = { date, total }; });
  return bd;
}
// Everything the Personal Records card needs, from existing progress data
// (best mock per exam reuses personalBest, so history already recorded
// counts — nothing new is recorded just for this card).
function personalRecords(p){
  p = p || progress;
  const attempts = p.attempts || [];
  const examIds = [...new Set(attempts.filter(a => a.mode === 'mock').map(a => a.exam))];
  const bestMocks = examIds.map(id => {
    const b = personalBest(id, attempts);
    return b ? { exam: id, examName: (examById(id) || {}).name || id, pct: b.pct, score: b.score, max: b.max, date: b.date } : null;
  }).filter(Boolean);
  return {
    bestMocks,
    longestStreak: longestStreak(attempts, p.streak),
    totalXp: p.xp || 0,
    totalQuestions: attempts.reduce((s, a) => s + (a.total || 0), 0),
    bestDay: bestDay(attempts),
    speedBest: getSpeedBest()
  };
}

/* ----- Share your score (clipboard only, no service, no SDK) ----- */
function buildShareText(r){
  // r: {examName, mode, score, max, pct, passed, date, speedBonus}
  const modeLabel = r.mode === 'mock' ? 'mock exam' : r.mode === 'speed' ? 'Speed Round' : 'practice set';
  const bonus = r.speedBonus ? ` (+${r.speedBonus} speed bonus)` : '';
  return `🏆 I scored ${r.score}/${r.max} (${r.pct}%) on the ${r.examName} ${modeLabel}${bonus} — ${r.passed ? 'PASS ✅' : 'keep practising 💪'} · ${r.date} · Outrank`;
}
function shareScore(){
  const c = current; if (!c || !c._res) return '';
  const r = c._res;
  const text = buildShareText({
    examName: c.title || (examById(c.exam) || {}).name || c.exam || 'Mixed practice', mode: c.mode,
    score: r.res.score, max: r.res.max, pct: r.res.pct, passed: r.passed,
    date: (r.res.date || todayStr()), speedBonus: r.res.speedBonus || 0
  });
  const statusEl = document.getElementById('share-status');
  const done = () => { if (statusEl) statusEl.textContent = B('Copied — paste it anywhere','कपी भयो — जहाँ पनि पेस्ट गर्नुहोस्'); };
  const fallback = () => {
    try {
      if (typeof document !== 'undefined' && typeof document.createElement === 'function' && document.body) {
        const ta = document.createElement('textarea');
        ta.value = text; document.body.appendChild(ta);
        if (ta.select) ta.select();
        if (typeof document.execCommand === 'function') document.execCommand('copy');
        if (ta.remove) ta.remove(); else if (document.body.removeChild) document.body.removeChild(ta);
        done(); return;
      }
    } catch (e) {}
    // No clipboard available (e.g. test stub): leave the text in the status
    // line so it can be copied by hand, and still return it.
    if (statusEl) statusEl.textContent = text;
  };
  try {
    if (typeof navigator !== 'undefined' && navigator.clipboard && navigator.clipboard.writeText) {
      const p = navigator.clipboard.writeText(text);
      if (p && typeof p.then === 'function') { p.then(done, fallback); return text; }
      done(); return text;
    }
  } catch (e) {}
  fallback();
  return text;
}

/* ----- Weekly challenge UI ----- */
function renderWeekly(){
  const w = weeklyProgress(progress);
  const html = `<h3>🎯 ${B('Weekly Challenge','साप्ताहिक चुनौती')} — ${w.done} / ${w.target} ${B('questions','प्रश्नहरू')}</h3>
  <p class="muted">${B('Week of','हप्ता')} ${w.weekStart} (Mon–Sun) · ${w.met ? B('✅ Goal met — Weekly Champion badge earned!','✅ लक्ष्य पूरा — Weekly Champion ब्याज प्राप्त भयो!') : w.pct+B('% '+B('there — keep going!','पुग्यो — जारी राख्नुहोस्!'))}</p>
  <div class="progress-bar"><div style="width:${w.pct}%"></div></div>
  <p style="margin-top:10px"><label>${B('Weekly target','साप्ताहिक लक्ष्य')}</label>
  <select onchange="setWeeklyTarget(this.value)">
    ${[35,70,100,140].map(t=>`<option value="${t}" ${w.target===t?'selected':''}>${t} ${B('questions / week','प्रश्न / हप्ता')}</option>`).join('')}
  </select></p>
  <p class="muted">🏆 ${B('Weekly goals smashed so far:','अहिलेसम्म पूरा भएका साप्ताहिक लक्ष्य:')} ${progress.weeklyGoalsMet||0}</p>`;
  const a=document.getElementById('weekly-box'); if(a) a.innerHTML=html;
  const b=document.getElementById('weekly-box-dash'); if(b) b.innerHTML=html;
}
function setWeeklyTarget(v){
  const n=parseInt(v,10);
  if([35,70,100,140].includes(n)){ progress.weeklyTarget=n; saveProgress(); renderWeekly(); }
}

/* ----- "Beat your best" personal best on the mock view ----- */
function renderMockTable(){
  const box=document.getElementById('mock-pattern-table'); if(!box) return;
  const rows=EXAMS.filter(e=>e.prelim).map(e=>{ const p=e.prelim;
    const neg=p.negative===null?'unverified':(p.negative===0?'none':Math.round((p.negative===0.4?0.2:p.negative)*100)+'%');
    return `<tr><td>${esc(e.name)}</td><td>${p.questions}</td><td>${p.timeMin==null?'—':p.timeMin+' min'}</td><td>${p.marksPerQ}</td><td>${p.pass}</td><td>${neg}</td></tr>`; }).join('');
  box.innerHTML=`<div class="table-wrap"><table><tr><th>Mock</th><th>Questions</th><th>Time</th><th>Marks/Q</th><th>Pass</th><th>Negative</th></tr>${rows}</table></div>`;
}
function renderMockBest(){
  const sel=document.getElementById('mock-exam'); if(!sel) return;
  const box=document.getElementById('mock-best'); if(!box) return;
  const best=personalBest(sel.value, progress.attempts);
  box.innerHTML = best
    ? `🏆 <strong>${B('Beat your best:','आफ्नो उत्कृष्ट तोड्नुहोस्:')}</strong> ${best.pct}% (${best.score}/${best.max}) ${B('on','मिति')} ${best.date} — ${B('can you top it?','पार गर्न सक्नुहुन्छ?')}`
    : B('No mock attempts for this exam yet — your first score here becomes the one to beat.','यस परीक्षाका लागि अझै मक प्रयास छैन — यहाँको पहिलो स्कोर नै तोड्नुपर्ने रेकर्ड बन्छ।');
}

/* ----- Focus timer (Pomodoro: 25 min focus, 5 min break, 15 min long break
   after every 4th focus block). In-memory countdown; completed blocks are
   persisted in progress (focusSessions / focusMinutes) and earn +10 XP. ----- */
const FOCUS_DURATIONS = { focus: 1500, short: 300, long: 900 };
const FOCUS_LABELS = { focus: '📚 Focus — 25 min', short: '☕ Short break — 5 min', long: '🌿 Long break — 15 min' };
let focusState = { mode:'focus', seconds: FOCUS_DURATIONS.focus, running:false, id:null, focusDone:0 };
function nextFocusMode(mode, focusDone){
  if (mode === 'focus') return (focusDone>0 && focusDone%4===0) ? 'long' : 'short';
  return 'focus';
}
function focusFmt(s){ return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0'); }
function updateFocusClock(){
  document.querySelectorAll('.focus-clock').forEach(e=>{ e.textContent=focusFmt(focusState.seconds); });
  document.querySelectorAll('.focus-mode').forEach(e=>{ e.textContent=FOCUS_LABELS[focusState.mode]+(focusState.running?' · running…':''); });
}
function renderFocusTimer(){
  const html = `<h3>⏱️ ${B('Focus Timer','फोकस टाइमर')} — Pomodoro</h3>
  <p class="muted">${B('25 minutes of focus, then a break. Every finished focus block: +10 XP.','२५ मिनेट फोकस, अनि ब्रेक। पूरा भएको हरेक फोकस ब्लक: +१० XP।')} ${B('Sessions done:','सत्र पूरा:')} ${progress.focusSessions||0} · ${progress.focusMinutes||0} ${B('min focused.','मिनेट फोकस।')}</p>
  <div class="focus-clock">${focusFmt(focusState.seconds)}</div>
  <p class="focus-mode">${FOCUS_LABELS[focusState.mode]}${focusState.running?' · running…':''}</p>
  <div>
    <button class="btn" onclick="focusStart()">▶ ${B('Start','सुरु')}</button>
    <button class="btn secondary" onclick="focusPause()">⏸ ${B('Pause','रोक्नुहोस्')}</button>
    <button class="btn secondary" onclick="focusReset()">↺ ${B('Reset','रिसेट')}</button>
  </div>
  <div style="margin-top:8px">
    <button class="btn secondary" onclick="focusSetMode('focus')">${B('Focus 25','फोकस २५')}</button>
    <button class="btn secondary" onclick="focusSetMode('short')">${B('Break 5','ब्रेक ५')}</button>
    <button class="btn secondary" onclick="focusSetMode('long')">${B('Break 15','ब्रेक १५')}</button>
  </div>
  <p class="muted focus-msg"></p>`;
  const a=document.getElementById('focus-timer-box'); if(a) a.innerHTML=html;
  const b=document.getElementById('focus-timer-box-dash'); if(b) b.innerHTML=html;
}
function focusStart(){
  if(focusState.running) return;
  focusState.running=true;
  focusState.id=setInterval(focusTick, 1000);
  updateFocusClock();
}
function focusPause(){
  focusState.running=false;
  if(focusState.id){ clearInterval(focusState.id); focusState.id=null; }
  updateFocusClock();
}
function focusReset(){ focusPause(); focusState.seconds=FOCUS_DURATIONS[focusState.mode]; updateFocusClock(); }
function focusSetMode(m){
  if(!FOCUS_DURATIONS[m]) return;
  focusPause(); focusState.mode=m; focusState.seconds=FOCUS_DURATIONS[m]; renderFocusTimer();
}
function focusTick(){
  if(!focusState.running) return;
  focusState.seconds--;
  if(focusState.seconds<=0){ focusComplete(); return; }
  updateFocusClock();
}
function focusComplete(){
  const wasFocus = focusState.mode==='focus';
  if(wasFocus){
    progress.focusSessions=(progress.focusSessions||0)+1;
    progress.focusMinutes=(progress.focusMinutes||0)+25;
    progress.xp+=10; progress.level=levelFromXp(progress.xp);
    focusState.focusDone++;
    saveProgress();
  }
  focusState.mode = nextFocusMode(focusState.mode, focusState.focusDone);
  focusState.seconds = FOCUS_DURATIONS[focusState.mode];
  focusState.running = false;
  if(focusState.id){ clearInterval(focusState.id); focusState.id=null; }
  renderFocusTimer();
  const msg = wasFocus ? B('🎉 Focus block done! +10 XP. Take a break — you earned it.','🎉 फोकस ब्लक पूरा! +१० XP। ब्रेक लिनुहोस् — तपाईंले कमाउनुभयो।') : B('Break over — ready for another focus block?','ब्रेक सकियो — अर्को फोकस ब्लकका लागि तयार?');
  document.querySelectorAll('.focus-msg').forEach(e=>{ e.textContent = msg; });
}

/* ----- Fun facts explorer ----- */
let currentFact=null;
function nextFunFact(){
  const seen = progress.funFactsSeen||[];
  const unseen = FUNFACTS.filter(f=>!seen.includes(f.id));
  const pool = unseen.length ? unseen : FUNFACTS;
  if(!pool.length) return null;
  return pool[Math.floor(Math.random()*pool.length)];
}
function showFunFact(){
  const f = nextFunFact(); if(!f){ renderFunFact(); return; }
  currentFact=f;
  if(!(progress.funFactsSeen||[]).includes(f.id)){ progress.funFactsSeen.push(f.id); saveProgress(); }
  renderFunFact();
}
function renderFunFact(){
  const box=document.getElementById('fun-fact-box'); if(!box) return;
  // Viewing the daily fact counts toward the fact streak (+5 XP once/day).
  recordFactVisit();
  const streak = getFactStreak();
  if(!currentFact){
    // First fact of a visit is the daily fact (same for everyone, same day);
    // "Another fact" shuffles from the unseen pool instead (showFunFact).
    currentFact = dailyFunFact() || (FUNFACTS.length ? FUNFACTS[Math.floor(Math.random()*FUNFACTS.length)] : null);
    if(currentFact && !(progress.funFactsSeen||[]).includes(currentFact.id)){ progress.funFactsSeen.push(currentFact.id); saveProgress(); }
  }
  const f=currentFact;
  const seen=(progress.funFactsSeen||[]).length, total=FUNFACTS.length;
  // Fun-fact schema (data/funfacts.json): {id, category, fact_en, fact_ne, source}.
  const factText = f ? ((lang==='ne' && f.fact_ne) ? f.fact_ne : (f.fact_en || f.text || '')) : '';
  box.innerHTML = f ? `<h3>💡 ${B('Did you know?','के तपाईंलाई थाहा छ?')}</h3>
    <p style="font-size:1.1rem">${esc(factText)}</p>
    <p class="muted">${esc(f.category||f.topic||'')}${f.source?` · ${B('Source:','स्रोत:')} ${esc(f.source)}`:''} · ${B('Facts explored:','हेरिएका तथ्य:')} ${seen} / ${total}${seen>=10?` · 🏅 ${B('Fact Explorer badge earned!','Fact Explorer ब्याज प्राप्त भयो!')}`:''}</p>
    <p class="muted">🔥 ${B('Fact streak:','तथ्य स्ट्रिक:')} <strong>${streak.streak} ${B(streak.streak===1?'day':'days','दिन')}</strong> — ${B('open the app each day to keep it going','यसलाई निरन्तर राख्न हरेक दिन एप खोल्नुहोस्')}${streak.lastRewardDate===todayStr()?` · ✅ +5 XP ${B('for today\u2019s fact','आजको तथ्यका लागि')}`:''}</p>
    <button class="btn secondary" onclick="showFunFact()">🎲 ${B('Another fact','अर्को तथ्य')}</button>`
  : `<h3>💡 ${B('Did you know?','के तपाईंलाई थाहा छ?')}</h3><p class="muted">${B('Fun facts did not load — reload the page and try again.','रोचक तथ्यहरू लोड भएनन् — पेज पुनः लोड गरेर प्रयास गर्नुहोस्।')}</p>`;
}
/* ----- Fact of the Day streak + Question of the Day -----
   Both are local-only. The fact streak lives in its own localStorage key
   (loksewa_fact_streak_v1) so it never touches the main progress object;
   viewing the daily fact earns +5 XP once per day. The Question of the Day
   is one fixed question per day (deterministic by date, from the bank) and
   its once-per-day XP lives in progress.qotdDone[date]. ----- */
const FACT_STREAK_KEY = 'loksewa_fact_streak_v1';
function loadFactStreak(){
  try { const v = JSON.parse(localStorage.getItem(FACT_STREAK_KEY) || 'null');
    if (v && typeof v.streak === 'number') return v; } catch (e) {}
  return { streak: 0, lastDay: '', lastRewardDate: '' };
}
function saveFactStreak(s){ try { localStorage.setItem(FACT_STREAK_KEY, JSON.stringify(s)); } catch (e) {} }
function getFactStreak(){ return loadFactStreak(); }
// Opening the app (viewing the daily fact) on consecutive days grows the
// streak; a missed day resets it to 1. +5 XP once per day, the first time
// the fact is viewed that day. dateStr is 'YYYY-MM-DD' (default: today);
// passing it lets tests step through consecutive days deterministically.
function recordFactVisit(dateStr){
  const today = dateStr || todayStr();
  const s = loadFactStreak();
  if (s.lastDay === today) return { streak: s.streak, rewarded: false, xp: 0 };
  const y = new Date(new Date(today + 'T00:00:00Z').getTime() - 864e5).toISOString().slice(0, 10);
  s.streak = (s.lastDay === y) ? s.streak + 1 : 1;
  s.lastDay = today;
  let rewarded = false;
  if (s.lastRewardDate !== today) {
    progress.xp += 5; progress.level = levelFromXp(progress.xp); saveProgress();
    s.lastRewardDate = today; rewarded = true;
  }
  saveFactStreak(s);
  return { streak: s.streak, rewarded, xp: rewarded ? 5 : 0 };
}
// One fixed question per day: same seed hash as the daily challenge/fact,
// so everyone sees the same question on the same day. Options are NOT
// shuffled here — the same question must render identically on every visit
// (and after a reload) until the day changes.
function questionOfDay(questions, dateStr){
  const bank = questions || QUESTIONS;
  if (!bank || !bank.length) return null;
  const seed = dateStr || todayStr(); let h = 0;
  for (const ch of seed) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  const q = bank[h % bank.length];
  const rand=()=>{ h=(h*1664525+1013904223)>>>0; return h/4294967296; };
  // Same question every visit that day, but the option order is
  // seeded-shuffled, so the daily answer position is no longer fixed.
  // Questions without options (test stubs) are returned as-is.
  return Array.isArray(q.options) ? shuffleOptions(q, rand) : q;
}
function renderQotd(){
  const box = document.getElementById('qotd-box'); if (!box) return;
  const q = questionOfDay(QUESTIONS);
  if (!q) { box.innerHTML = skelBlock(1); return; }
  const today = todayStr();
  const done = (progress.qotdDone || {})[today];
  const optsHtml = qOpts(q).map((o, i) => {
    const cls = done ? (i === q.answer ? ' correct' : (i === done.choice ? ' wrong' : '')) : '';
    return `<button class="opt${cls}" data-i="${i}" onclick="answerQotd(${i})" ${done ? 'disabled' : ''}>${String.fromCharCode(65 + i)}. ${esc(o)}</button>`;
  }).join('');
  const feedback = done ? `<div class="expl"><strong>${done.correct ? B('✅ Correct!','✅ सही!') : B('❌ Not quite.','❌ भएन।')}</strong> ${B('Correct answer:','सही उत्तर:')} <strong>${String.fromCharCode(65 + q.answer)}. ${esc(qOpts(q)[q.answer])}</strong><br>${esc(qExpl(q))}</div>
    <p class="muted">${done.correct ? '✅ +' : '➕ +'}${done.xp} XP ${B('earned for today\u2019s question — come back tomorrow for a new one.','आजको प्रश्नका लागि प्राप्त — भोलि नयाँ प्रश्नका लागि फर्कनुहोस्।')}</p>` : '';
  box.innerHTML = `<h3>❓ ${B('Question of the Day','आजको प्रश्न')} — ${esc(today)}</h3>
    <p style="font-size:1.05rem">${esc(qText(q))}</p>
    <div class="tag">${esc(q.topic)} · ${esc(q.difficulty)} · ${B('Exams:','परीक्षाहरू:')} ${esc((q.exam||[]).join(', '))}</div>
    ${optsHtml}${feedback}`;
}
// Answer the Question of the Day: +10 XP if correct, +2 XP for trying —
// once per day only; later taps the same day are ignored.
function answerQotd(i){
  const q = questionOfDay(QUESTIONS); if (!q) return;
  const today = todayStr();
  progress.qotdDone = progress.qotdDone || {};
  if (progress.qotdDone[today]) return;
  const ok = i === q.answer;
  const xp = ok ? 10 : 2;
  progress.xp += xp; progress.level = levelFromXp(progress.xp); updateStreak();
  progress.qotdDone[today] = { choice: i, correct: ok, xp };
  saveProgress();
  renderQotd(); renderHomeStats();
}
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

// Encouraging microcopy after answers — 20+ distinct lines each, EN + NE,
// rotated so the same line never repeats twice in a row for one list.
// Entries are {en, ne} objects; pickLine() returns the current language.
const PRAISE_LINES = [
  { en: 'Nice — that one is staying with you.', ne: 'राम्रो — यो कुरा मनमा बस्नेछ।' },
  { en: 'Sharp! Keep the streak alive.', ne: 'चुस्त! यो लय कायम राख्नुहोस्।' },
  { en: 'Exactly right. On to the next one.', ne: 'ठ्याक्कै मिल्यो। अब अर्को प्रश्नतिर।' },
  { en: 'Well done — the revision is paying off.', ne: 'स्याबास — दोहोर्याएको मिहिनेतले फल दिइरहेको छ।' },
  { en: 'Correct! You are building real momentum.', ne: 'सही! तपाईं साँच्चै गति बनाउँदै हुनुहुन्छ।' },
  { en: 'Brilliant — that is a keeper.', ne: 'उत्कृष्ट — यो कुरा सम्झन लायक छ।' },
  { en: 'Yes! One more fact locked in.', ne: 'हो! अर्को तथ्य पनि पक्का भयो।' },
  { en: 'Superb — your hard work is showing.', ne: 'उत्तम — तपाईंको मिहिनेत देखिइरहेको छ।' },
  { en: 'That was textbook. Well played.', ne: 'त्यो त किताबी उत्तर भयो। राम्रो खेल्नुभयो।' },
  { en: 'Spot on! You knew that one cold.', ne: 'ठीक ठाउँमा! त्यो त तपाईंलाई पक्कै थाहा थियो।' },
  { en: 'Excellent — one step closer to the hall.', ne: 'उत्कृष्ट — परीक्षा हलतिर एक पाइला नजिक।' },
  { en: 'Great recall — that fact is yours now.', ne: 'राम्रो सम्झना — त्यो तथ्य अब तपाईंको भयो।' },
  { en: 'You are on fire today!', ne: 'आज तपाईं त आगो बल्नुभएको छ!' },
  { en: 'Perfectly answered — keep this rhythm.', ne: 'पूर्ण रूपमा सही उत्तर — यही लय कायम राख्नुहोस्।' },
  { en: 'That is the kind of answer that passes exams.', ne: 'यस्तै उत्तरले परीक्षा पास गराउँछ।' },
  { en: 'Well remembered — revision done right.', ne: 'राम्रोसँग सम्झनुभयो — दोहोर्याइ सही तरिकाले भयो।' },
  { en: 'Clean and correct. Lovely work.', ne: 'सफा र सही। राम्रो काम।' },
  { en: 'You make it look easy.', ne: 'तपाईंले त सजिलो देखाइदिनुभयो।' },
  { en: 'Another one in the bag — keep going!', ne: 'अर्को पनि हातमा पर्यो — अगाडि बढ्नुहोस्!' },
  { en: 'Strong answer. Your future self says thanks.', ne: 'बलियो उत्तर। तपाईंको भविष्यको आफैले धन्यवाद भन्नेछ।' },
  { en: 'Nailed it — that topic is yours.', ne: 'ठ्याक्कै मिलाउनुभयो — त्यो विषय अब तपाईंको हो।' },
  { en: 'Beautifully done — confidence growing.', ne: 'राम्रोसँग गर्नुभयो — आत्मविश्वास बढ्दै छ।' }
];
const TRY_AGAIN_LINES = [
  { en: 'Not this one — but now you know it for the exam hall.', ne: 'यो मिलेन — तर अब परीक्षा हलका लागि थाहा भयो।' },
  { en: 'Close! Read the explanation slowly and it will stick.', ne: 'नजिक पुग्नुभयो! व्याख्या बिस्तारै पढ्नुहोस्, मनमा बस्छ।' },
  { en: 'Wrong today, right on exam day — that is the deal.', ne: 'आज गलत, परीक्षा दिन सही — यही त सम्झौता हो।' },
  { en: 'Tricky one. The explanation is worth a second read.', ne: 'झुक्किने प्रश्न। व्याख्या दोस्रो पटक पढ्न लायक छ।' },
  { en: 'No worries — mistakes here are free.', ne: 'चिन्ता नलिनुहोस् — यहाँ गल्ती गर्नु नि:शुल्क छ।' },
  { en: 'That one stings a little, but it is now in your mistakes list to revise.', ne: 'यो अलि चित्त दुख्यो होला, तर अब यो तपाईंको गल्ती सूचीमा छ — दोहोर्याउनुहोस्।' },
  { en: 'Missed it — but every miss here is one less miss in the hall.', ne: 'छुट्यो — तर यहाँ छुटेको प्रत्येक प्रश्न हलमा छुट्ने सम्भावना घटाउँछ।' },
  { en: 'Not yet — the explanation below is your shortcut.', ne: 'अहिलेसम्म मिलेन — तलको व्याख्या तपाईंको छोटो बाटो हो।' },
  { en: 'Good try! The correct answer is a keeper — note it down.', ne: 'राम्रो प्रयास! सही उत्तर सम्झन लायक छ — टिप्नुहोस्।' },
  { en: 'That was a hard one. Even toppers miss these.', ne: 'त्यो गाह्रो प्रश्न थियो। टपरहरूले पनि यस्ता छुटाउँछन्।' },
  { en: 'Almost! One careful read and it will click.', ne: 'लगभग मिल्यो! एक पटक ध्यान दिएर पढ्नुहोस्, बुझिन्छ।' },
  { en: 'Wrong answer, right lesson. That is how toppers are made.', ne: 'गलत उत्तर, सही पाठ। यसरी नै टपर बन्छन्।' },
  { en: 'Do not rush past this one — it loves coming back in exams.', ne: 'यो प्रश्न छिटो नछोड्नुहोस् — परीक्षामा यो बारम्बार आउँछ।' },
  { en: 'A miss today is a mark saved tomorrow.', ne: 'आजको गल्ती भोलिको अंक जोगाउने हो।' },
  { en: 'Take a breath, read the explanation, try the next one.', ne: 'एक छिन सास फेर्नुहोस्, व्याख्या पढ्नुहोस्, अर्को प्रश्न प्रयास गर्नुहोस्।' },
  { en: 'This one caught you — now it cannot catch you twice.', ne: 'यो प्रश्नले तपाईंलाई छोप्यो — अब यसले दोस्रो पटक छोप्न सक्दैन।' },
  { en: 'So close! Your brain just filed this one away.', ne: 'धेरै नजिक! तपाईंको दिमागले यो भर्खरै सुरक्षित गर्यो।' },
  { en: 'Every wrong answer here is a free lesson.', ne: 'यहाँको प्रत्येक गलत उत्तर नि:शुल्क पाठ हो।' },
  { en: 'Keep your head up — the next one is yours.', ne: 'शिर उच्च राख्नुहोस् — अर्को प्रश्न तपाईंको हो।' },
  { en: 'That fact is tricky for everyone. Now you own it.', ne: 'यो तथ्य सबैका लागि झुक्किने खालको छ। अब यो तपाईंको भयो।' },
  { en: 'Mistakes are the revision list writing itself.', ne: 'गल्तीहरू आफैं दोहोर्याउने सूची बन्दै छन्।' },
  { en: 'You will get this one next time — it is already in your mistakes list.', ne: 'अर्को पटक यो मिलाउनुहुनेछ — यो तपाईंको गल्ती सूचीमा परिसक्यो।' }
];
const PASS_LINES = [
  { en: 'You cleared the cutoff — that is a real pass, not luck.', ne: 'तपाईंले कटअफ पार गर्नुभयो — यो साँच्चै पास हो, भाग्य होइन।' },
  { en: 'Cutoff beaten. Keep this form going.', ne: 'कटअफ पार भयो। यही फर्म कायम राख्नुहोस्।' },
  { en: 'Passed! The exam hall version of you says thanks.', ne: 'पास! परीक्षा हलमा बस्ने तपाईंले धन्यवाद भन्नेछन्।' },
  { en: 'That is a pass worth celebrating — briefly, then back to work.', ne: 'यो पास मनाउन लायक छ — छोटकरीमा, अनि फेरि कामतिर।' },
  { en: 'Cutoff cleared. The real paper is starting to look doable.', ne: 'कटअफ पार भयो। वास्तविक परीक्षा अब सम्भव देखिन थालेको छ।' }
];
const FAIL_LINES = [
  { en: 'Below the cutoff this time — the weak topics below are your revision list.', ne: 'यस पटक कटअफभन्दा तल — तलका कमजोर विषय तपाईंको दोहोर्याउने सूची हुन्।' },
  { en: 'Not yet — but every wrong answer here is one you will not repeat.', ne: 'अहिलेसम्म पुगेन — तर यहाँका प्रत्येक गलत उत्तर अब दोहोरिने छैनन्।' },
  { en: 'Keep going. A fail in practice is cheaper than a fail in the hall.', ne: 'अगाडि बढ्नुहोस्। अभ्यासमा असफल हुनु हलमा असफल हुनुभन्दा सस्तो छ।' },
  { en: 'The cutoff is close — one more focused week can close the gap.', ne: 'कटअफ नजिक छ — एक हप्ता केन्द्रित तयारीले दूरी घटाउन सक्छ।' },
  { en: 'Not a pass yet, but the score is honest — and honesty is where improvement starts.', ne: 'अहिलेसम्म पास होइन, तर अंक इमानदार छ — र सुधार इमानदारीबाटै सुरु हुन्छ।' }
];
// Last-used index per list, so the same line never repeats twice in a row.
const _lastLineIdx = {};
function pickLine(lines, key){
  if (!lines || !lines.length) return '';
  let idx = 0;
  if (lines.length > 1) {
    do { idx = Math.floor(Math.random() * lines.length); } while (key && _lastLineIdx[key] === idx);
    if (key) _lastLineIdx[key] = idx;
  }
  const e = lines[idx];
  if (typeof e === 'string') return e;
  return (lang === 'ne' && e.ne) ? e.ne : e.en;
}
// True when the user asked the OS/browser for reduced motion: animations,
// confetti, count-ups and smooth scrolling all switch to instant rendering.
function prefersReducedMotion(){
  try { return typeof window !== 'undefined' && !!window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
  catch (e) { return false; }
}

// Pure-CSS/JS confetti (no library): small coloured pieces falling through
// #confetti-layer. Only ever launched on a pass or a level-up.
let confettiT=null;
function launchConfetti(){
  if (prefersReducedMotion()) return; // reduced motion: no confetti, ever
  if (typeof document === 'undefined') return;
  const layer = document.getElementById('confetti-layer');
  if (!layer || typeof layer.appendChild !== 'function' || typeof document.createElement !== 'function') return;
  // A second celebration within the clear-timeout window must not let the
  // old timeout sweep the new pieces away early.
  if (confettiT) { clearTimeout(confettiT); confettiT = null; }
  const colors = ['#ea580c', '#f97316', '#22c55e', '#ef4444', '#fed7aa', '#facc15'];
  for (let i = 0; i < 48; i++) {
    const p = document.createElement('div');
    p.className = 'confetti-piece';
    p.style.left = (Math.random() * 100).toFixed(1) + '%';
    p.style.background = colors[i % colors.length];
    p.style.animationDelay = (Math.random() * 0.4).toFixed(2) + 's';
    p.style.animationDuration = (2 + Math.random() * 1.5).toFixed(2) + 's';
    layer.appendChild(p);
  }
  if (typeof setTimeout === 'function') confettiT = setTimeout(() => { layer.innerHTML = ''; confettiT = null; }, 4200);
}
// Glide a bar from a previous width to a new one (CSS transition does the
// work). In the Node test stubs requestAnimationFrame is absent, so the bar
// is simply set to its final width — no crash, no wrong value.
function animateWidth(el, fromPct, toPct){
  if (!el || !el.style) return;
  if (prefersReducedMotion() || typeof requestAnimationFrame !== 'function') { el.style.width = toPct + '%'; return; }
  el.style.width = fromPct + '%';
  requestAnimationFrame(() => { el.style.width = toPct + '%'; });
}

function showView(id){
  // Leaving a timed quiz abandons it: stop the countdown so it cannot
  // auto-submit while the user is on another view. The attempt is NOT
  // recorded (finishAttempt is never called for an abandoned quiz).
  if (id !== 'quiz' && id !== 'result') clearInterval(timerId);
  // A half-started "discuss this question" must not prefill the Hub when the
  // user opens Discuss on their own later — clear it on any other view.
  if (id !== 'discuss') pendingDiscuss = null;
  // Leaving the audio view stops narration so it never keeps talking on
  // another view (or after the tab is backgrounded).
  if (id !== 'audio') audioStop();
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  const el=document.getElementById('view-'+id); if(el) el.classList.add('active');
  // Active-state sync covers every [data-view] button no matter how it is
  // nested (plain nav, dropdown menu, mobile bar) — the selector is
  // deliberately not scoped to 'nav'.
  document.querySelectorAll('button[data-view]').forEach(b=>b.classList.toggle('active', b.dataset.view===id));
  // Dynamic <title>: brand first, then the English view name.
  if (typeof document !== 'undefined' && document){
    const vt = VIEW_TITLES[id];
    document.title = vt ? 'Outrank — ' + vt : 'Outrank';
  }
  window.scrollTo({top:0, behavior: prefersReducedMotion() ? 'auto' : 'smooth'}); if(id==='dashboard') renderDashboard(); if(id==='guide') renderGuide(); if(id==='review') renderReview();
  if(id==='mock') renderMockBest(); if(id==='home'){ renderWeekly(); renderFocusTimer(); renderFunFact(); renderQotd(); renderExamReminder(); renderFestivalCard(); if (typeof renderBirthdayCard === 'function') renderBirthdayCard(); renderHistoryOtd(); renderNextExamCard(); renderContinueStudying(); if (typeof renderBetaBanner === 'function') renderBetaBanner(); checkExamNotifications(); }
  if(id==='dashboard'){ renderNextExamCompact(); }
  if(id==='auth') renderAuth(); if(id==='profile') renderProfile(); if(id==='discuss') renderDiscuss();
  if(id==='submit') renderSubmit(); if(id==='moderate') renderModerate();
  if(id==='papers') renderPapers(); if(id==='notices') renderNotices();
  if(id==='funfacts') renderFunFacts();
  if(id==='notes') renderNotes(); if(id==='audio') renderAudio();
  if(id==='coverage') renderCoverage(); if(id==='print') renderPrint();
  if(id==='planner') renderPlanner(); if(id==='coach') renderCoach();
  if(id==='pyq') renderPYQ();
  if(id==='chat') renderChat(); if(id==='suggest') renderSuggest();
  if(id==='examdates') renderExamDates();
  if(id==='courses') renderCourses();
  if(id==='history') renderHistory();
  if(id==='today' && typeof renderToday === 'function') renderToday();
}
// Per-view <title> names (English view names are fine — the brand prefix
// stays constant). Unknown ids fall back to the bare brand.
const VIEW_TITLES = {
  home:'Home', practice:'Practice', quiz:'Quiz', result:'Result', mock:'Mock Exams',
  guide:'Exam Guide', dashboard:'Dashboard', review:'Bookmarks & Mistakes', flash:'Flashcards',
  search:'Search', auth:'Sign In', profile:'Profile', discuss:'Discussion Hub',
  submit:'Contribute a Question', moderate:'Review Queue', papers:'Old Papers', notices:'Notices',
  funfacts:'Fun Facts', chat:'Ask Ravi', suggest:'Suggest a Feature', coverage:'Syllabus Coverage',
  print:'Printable Paper', planner:'Study Planner', coach:'Guess Coach', pyq:'PYQ Heatmap',
  notes:'Revision Notes', audio:'Audio Revision', examdates:'Exam Dates',
  courses:'Courses', today:'My Day', history:'Dates to Remember'
};
/* ---- Production-polish UI helpers: skeletons, empty states, error states ---- */
// dataReady is false only while loadData() is actually fetching. In the Node
// test harnesses loadData() is either awaited (e2e — renders happen after it
// settles) or never called (unit — the flag stays true), so renders there
// behave exactly as before.
let dataReady = true;
// Skeleton placeholders (CSS .skel / .skel-line / .skel-card) for data-heavy
// views while their data is still arriving. Rendered synchronously on the
// next paint — no artificial delays, no "Loading…" text.
function skelCard(lines){
  let h = '<div class="skel-card" aria-hidden="true">';
  for (let i = 0; i < (lines == null ? 4 : lines); i++) h += '<div class="skel skel-line"></div>';
  return h + '</div>';
}
function skelBlock(n){
  let h = '<div class="skel-wrap">';
  for (let i = 0; i < (n || 2); i++) h += skelCard(4);
  return h + '</div>';
}
// Polished empty state: icon + headline + one-line explanation + optional
// CTA button. Pass already-bilingual strings (B('en','ne')).
function emptyState(icon, headline, blurb, ctaLabel, ctaOnclick){
  return '<div class="empty-state"><div class="empty-icon" aria-hidden="true">' + icon + '</div>' +
    '<h3>' + headline + '</h3><p class="muted">' + blurb + '</p>' +
    (ctaLabel ? '<p><button class="btn" onclick="' + ctaOnclick + '">' + ctaLabel + '</button></p>' : '') + '</div>';
}
// Friendly data-load failure with a retry button (retry = refetch everything
// and re-render the current view).
function errorState(headline, blurb){
  return '<div class="empty-state empty-error"><div class="empty-icon" aria-hidden="true">⚠️</div>' +
    '<h3>' + headline + '</h3><p class="muted">' + blurb + '</p>' +
    '<p><button class="btn" onclick="reloadData()">' + B('↻ Try again', '↻ पुनः प्रयास गर्नुहोस्') + '</button></p></div>';
}
function reloadData(){
  dataReady = false;
  const active = (typeof document !== 'undefined' && document.querySelector) ? document.querySelector('.view.active') : null;
  const id = active && active.id ? active.id.replace(/^view-/, '') : 'home';
  if (typeof loadData === 'function') loadData().then(function(){ showView(id); }).catch(function(){ dataReady = true; showView(id); });
  showView(id); // re-render immediately so skeletons show while refetching
}
function examById(id){ return EXAMS.find(e=>e.id===id); }
function cutoffFor(examId){ const e=examById(examId); return (e && e.prelim) ? e.prelim.pass : 45; }
// Negative-marking rate for a mock: prelim.negative stores the rate (0.2 = 20%
// on PSC entries, 0.25 on MECEE-BL), 0 where the exam has no negative marking,
// null where it is unverified. mockNegRate returns the stored rate.
// (Staff Nurse used to store 0.4 — absolute marks deducted per wrong 2-mark
// question — it now stores the 0.2 rate like every other exam.)
// MECEE-BL stores 0.25 (rate). Unverified or zero both mean: deduct nothing.
function mockNegRate(p){ if (p.negative === null || p.negative === 0) return 0; return p.negative; }

async function loadData(){
  dataReady = false; // data-heavy views render skeletons until this settles
  await loadConfig();
  try{
    const r=await fetch('data/exams.json'); EXAMS=await r.json();
  }catch(e){ EXAMS=[]; }
  QUESTIONS=[];
  // 106 files: fetch them in parallel, not one-by-one. The old sequential
  // loop cost one round-trip per file (106 round-trips on every load — seconds
  // on GitHub Pages). Promise.all preserves QUESTION_FILES order, and a
  // per-file catch keeps one bad file from losing the whole bank.
  // NOTE: scripts/build-bundle.py embeds this exact block (FETCH_BLOCK) —
  // keep the two in sync or the bundle build breaks.
  const _loaded=await Promise.all(QUESTION_FILES.map(f=>fetch('data/questions/'+f).then(r=>r.json()).catch(e=>{ console.warn('Could not load', f, e); return []; })));
  _loaded.forEach(arr=>{ QUESTIONS=QUESTIONS.concat(arr); });
  // Community-approved questions (approved in the Maintainer Review view) live
  // in localStorage in this static build and join the bank at startup, with a
  // "Community" badge. See docs/BACKEND.md for the server-side path.
  QUESTIONS=QUESTIONS.concat(communityApprovedQuestions());
  // Flag the transcribed real Previous Year questions (previous-year-*.json)
  // so the analytics views (PYQ heatmap, weight estimates) can use them as
  // ground truth. Must run before any analytics render.
  markPyqFlags();
  // Old papers + notices: same fetch pattern as exams/questions, with the
  // single-file bundle's embedded-data fallback (window.EMBEDDED_PAPERS /
  // window.EMBEDDED_NOTICES, set by scripts/build-bundle.py). Embedded data
  // is checked FIRST so the bundle never calls fetch() on file://.
  if (typeof window!=='undefined' && window.EMBEDDED_PAPERS) PAPERS = window.EMBEDDED_PAPERS.slice();
  else { try{ const r=await fetch('data/papers.json'); PAPERS=await r.json(); }catch(e){ PAPERS=[]; } }
  if (typeof window!=='undefined' && window.EMBEDDED_NOTICES) NOTICES = window.EMBEDDED_NOTICES.slice();
  else { try{ const r=await fetch('data/notices.json'); NOTICES=await r.json(); }catch(e){ NOTICES=[]; } }
  // Fun facts: same fetch pattern, with the single-file bundle's embedded-data
  // fallback (window.EMBEDDED_FUNFACTS, set by scripts/build-bundle.py).
  if (typeof window!=='undefined' && window.EMBEDDED_FUNFACTS) FUNFACTS = window.EMBEDDED_FUNFACTS.slice();
  else { try{ const r=await fetch('data/funfacts.json'); FUNFACTS=await r.json(); }catch(e){ FUNFACTS=[]; } }
  // Exam dates (data/exam-dates.json): verified upcoming exam/admit/deadline
  // dates in Bikram Sambat, with the single-file bundle's embedded-data
  // fallback (window.EMBEDDED_EXAMDATES, set by scripts/build-bundle.py).
  if (typeof window!=='undefined' && window.EMBEDDED_EXAMDATES) EXAMDATES = window.EMBEDDED_EXAMDATES.slice();
  else { try{ const r=await fetch('data/exam-dates.json'); EXAMDATES=await r.json(); }catch(e){ EXAMDATES=[]; } }
  // Festival wishes (data/festivals.json): verified Nepali festival dates
  // in Bikram Sambat, with the single-file bundle's embedded-data fallback
  // (window.EMBEDDED_FESTIVALS, set by scripts/build-bundle.py). Eid
  // al-Fitr and Bakr Eid are EXCLUDED from festivals.json by the user's
  // explicit instruction (2026-11-09) — every other Nepal festival is in.
  if (typeof window!=='undefined' && window.EMBEDDED_FESTIVALS) FESTIVALS = window.EMBEDDED_FESTIVALS.slice();
  else { try{ const r=await fetch('data/festivals.json'); FESTIVALS=await r.json(); }catch(e){ FESTIVALS=[]; } }
  // Historical events (data/historical-events.json): verified dates to
  // remember, with the single-file bundle's embedded-data fallback
  // (window.EMBEDDED_HISTORY, set by scripts/build-bundle.py). Entries
  // with day_bs null (AD-only or year-only) still load — they show in the
  // Dates view but cannot recur, so On This Day / My Day skip them.
  if (typeof window!=='undefined' && window.EMBEDDED_HISTORY) HISTORY = window.EMBEDDED_HISTORY.slice();
  else { try{ const r=await fetch('data/historical-events.json'); HISTORY=await r.json(); }catch(e){ HISTORY=[]; } }
  // Revision notes: one file per topic (data/notes/NOTES_FILES), fetched in
  // parallel like the question bank, with the single-file bundle's
  // embedded-data fallback (window.EMBEDDED_NOTES, set by
  // scripts/build-bundle.py). A failed note file must not break the rest:
  // failures resolve to null and are filtered out.
  if (typeof window!=='undefined' && window.EMBEDDED_NOTES) NOTES = window.EMBEDDED_NOTES.slice();
  else { try{ const _n=await Promise.all(NOTES_FILES.map(f=>fetch('data/notes/'+f).then(r=>r.json()).catch(e=>{ console.warn('Could not load note', f, e); return null; }))); NOTES=_n.filter(Boolean); }catch(e){ NOTES=[]; } }
  // Theory courses: one file per exam in data/courses/COURSE_FILES, with the
  // single-file bundle's embedded-data fallback (window.EMBEDDED_COURSES,
  // set by scripts/build-bundle.py). Failures resolve to null and filter out.
  if (typeof window!=='undefined' && window.EMBEDDED_COURSES) COURSES = window.EMBEDDED_COURSES.slice();
  else { try{ const _c=await Promise.all(COURSE_FILES.map(f=>fetch('data/courses/'+f).then(r=>r.json()).catch(e=>{ console.warn('Could not load course', f, e); return null; }))); COURSES=_c.filter(Boolean); }catch(e){ COURSES=[]; } }
  dataReady = true; // the fetch phase settled — views may render real content
  updateDemoBanner();
  const el=$('#q-count'); if(el) el.textContent = QUESTIONS.length ? QUESTIONS.length.toLocaleString() : '—';
  const ec=$('#exam-count'); if(ec) ec.textContent = EXAMS.length || '—';
  fillExamSelects(); renderHomeStats(); renderGuide(); renderTopics(); renderPapers(); renderNotices();
  renderWeekly(); renderFocusTimer(); renderFunFact(); renderMockBest(); renderMockTable(); renderQotd(); renderExamReminder(); renderFestivalCard(); renderHistoryOtd(); renderNextExamCard(); renderNextExamCompact(); renderContinueStudying(); if (typeof renderBetaBanner === 'function') renderBetaBanner(); checkExamNotifications();
  if(!QUESTIONS.length){
    const n=$('#load-note'); if(n) n.innerHTML='<p class="card" style="border-color:#ef4444">⚠️ Question bank did not load. This app loads its JSON files with <code>fetch()</code> — open it through a local server (<code>python3 -m http.server 8000</code>) or GitHub Pages, not by double-clicking the file. See README.</p>';
  }
}
function fillExamSelects(){
  // Rebuilding the selects used to wipe the user's choice: visiting the
  // Contribute view calls renderSubmit() → fillExamSelects(), and the
  // Practice/Mock exam silently reset to the first option. Snapshot each
  // select first and restore the choice afterwards when it still exists.
  // selectedIndex tells "never touched" (-1 / no options yet) apart from an
  // explicitly chosen empty value (the 🌐 mixed option): only the latter is
  // restored, so the default stays the first exam.
  const snap=id=>{ const s=document.getElementById(id); if(!s) return null; return {s, v:s.value, i:(typeof s.selectedIndex==='number')?s.selectedIndex:-1}; };
  const snaps=[snap('practice-exam'),snap('mock-exam'),snap('flash-exam'),snap('sub-exam'),snap('cov-exam'),snap('prt-exam'),snap('pla-exam'),snap('coa-exam'),snap('pyq-exam')].filter(Boolean);
  const allOpts=EXAMS.map(e=>`<option value="${e.id}">${esc(e.name)}</option>`).join('');
  // Guide-only exams (prelim: null) have no MCQ paper, but some DO have tagged
  // practice questions — only label an exam as having none when it truly has 0.
  const tagged={}; QUESTIONS.forEach(q=>(q.exam||[]).forEach(id=>tagged[id]=(tagged[id]||0)+1));
  // The empty-value option is "mixed practice" (the Daily/Surprise/Quick
  // modes are exam-less too); it is LAST so the default stays the first exam.
  const practiceOpts='<option value="">'+B('🌐 All exams (mixed)','🌐 सबै परीक्षा (मिश्रित)')+'</option>'+EXAMS.map(e=>`<option value="${e.id}">${esc(e.name)}${e.prelim?'':(tagged[e.id]?B(' — guide only',' — गाइड मात्र'):B(' — guide only, no practice questions',' — गाइड मात्र, अभ्यास प्रश्न छैनन्'))}</option>`).join('');
  // The mock select lists ONLY exams with a verified MCQ prelim — guide-only
  // exams (prelim: null) have no mock and must not appear here.
  const mockOpts=EXAMS.filter(e=>e.prelim).map(e=>`<option value="${e.id}">${esc(e.name)}</option>`).join('');
  const ps=document.getElementById('practice-exam'); if(ps) ps.innerHTML=practiceOpts;
  const ms=document.getElementById('mock-exam'); if(ms) ms.innerHTML=mockOpts;
  // Analytics views (features 1–5): prelim-only selects get the same mock
  // list (paper-exact patterns exist only for prelim exams); the planner's
  // custom-exam select accepts every exam.
  const mockIds=['cov-exam','prt-exam','coa-exam','pyq-exam'];
  mockIds.forEach(id=>{ const s=document.getElementById(id); if(s) s.innerHTML=mockOpts; });
  const ple=document.getElementById('pla-exam'); if(ple) ple.innerHTML='<option value="">—</option>'+allOpts;
  const ss=document.getElementById('sub-exam'); if(ss) ss.innerHTML=allOpts;
  const fs=document.getElementById('flash-exam'); if(fs) fs.innerHTML='<option value="">'+B('All exams (mixed)','सबै परीक्षा (मिश्रित)')+'</option>'+allOpts;
  snaps.forEach(({s,v,i})=>{ if(i===-1 && !v) return; for(const o of (s.options||[])){ if(o.value===v){ s.value=v; break; } } });
  const pp=document.getElementById('practice-pattern'); const upd=()=>{ const pe2=document.getElementById('practice-exam'); const ev=pe2?pe2.value:''; const e=ev?examById(ev):null; if(pp) pp.textContent=!ev?('🌐 '+B('Mixed practice','मिश्रित अभ्यास')+' — '+QUESTIONS.length.toLocaleString()+' '+B('questions from all exams, ~54s per question with the timer on.','सबै परीक्षाका प्रश्नहरू, टाइमर चल्दा प्रति प्रश्न ~५४ सेकेन्ड।')):e&&e.prelim?`${e.name}: ${e.prelim.questions} ${B('questions','प्रश्न')} × ${e.prelim.marksPerQ} ${B('mark(s)','अङ्क')}, ${e.prelim.timeMin==null?B('time unverified','समय अपुष्ट'):e.prelim.timeMin+' '+B('min','मिनेट')}, ${B('pass','पास')} ${e.prelim.pass}/${e.prelim.total}.`:B('Guide-only exam — no MCQ paper; practice draws from tagged questions only.','गाइड-मात्र परीक्षा — MCQ पेपर छैन; अभ्यास ट्याग गरिएका प्रश्नहरूबाट मात्र हुन्छ।'); }; const pe=document.getElementById('practice-exam'); if(pe) pe.addEventListener('change',()=>{ upd(); updatePracticeTopics(); }); upd(); updatePracticeTopics();
}
// Rebuild the Practice topic list from the topics that actually have questions
// tagged for the selected exam. The old global list let users pick impossible
// exam+topic combinations (e.g. Banking & Finance for Ayurveda BAMS, which has
// 18 questions all in one topic) that only failed at Start.
function updatePracticeTopics(){
  const sel=document.getElementById('practice-topic'); if(!sel) return;
  const exam=document.getElementById('practice-exam').value;
  const prev=sel.value;
  const counts={};
  QUESTIONS.forEach(q=>{ if(!exam||q.exam.includes(exam)) counts[q.topic]=(counts[q.topic]||0)+1; });
  const topics=Object.keys(counts).sort();
  const total=topics.reduce((n,t)=>n+counts[t],0);
  if(!topics.length){
    sel.innerHTML='<option value="">'+B('No questions tagged for this exam yet','यस परीक्षाका लागि अझै प्रश्न ट्याग गरिएको छैन')+'</option>';
  }else{
    sel.innerHTML=`<option value="">${B('All topics ('+total+')','सबै विषय ('+total+')')}</option>`+topics.map(t=>`<option value="${esc(t)}">${esc(t)} (${counts[t]})</option>`).join('');
  }
  // Keep the previous topic when it still exists for this exam; otherwise fall
  // back to All topics instead of a stale value that would match nothing.
  sel.value = topics.includes(prev) ? prev : '';
}
function renderHomeStats(){
  const t=$('#home-topics'); if(t) t.textContent = new Set(QUESTIONS.map(q=>q.topic)).size || '—';
  const d=$('#home-xp'); if(d) d.textContent = progress.xp;
  const s=$('#home-streak'); if(s) s.textContent = progress.streak;
  const sb=$('#speed-best'); if(sb){ const b=getSpeedBest(); sb.textContent = b ? `⚡ ${B('Best Speed Round:','उत्कृष्ट स्पिड राउन्ड:')} ${b.score}/${b.max} (${b.pct}%) ${B('on','मिति')} ${b.date}` : ''; }
}
function renderTopics(){
  const box=$('#topic-list'); if(!box) return;
  if(!dataReady){ box.innerHTML=skelBlock(2); return; }
  if(!QUESTIONS.length){ box.innerHTML=errorState(B('Topics could not be loaded','विषयहरू लोड हुन सकेनन्'), B('The question bank failed to load. Check your connection and try again.','प्रश्न बैंक लोड हुन असफल भयो। आफ्नो इन्टरनेट कनेक्सन जाँचेर पुनः प्रयास गर्नुहोस्।')); return; }
  const counts={}; QUESTIONS.forEach(q=>counts[q.topic]=(counts[q.topic]||0)+1);
  box.innerHTML=Object.entries(counts).sort((a,b)=>b[1]-a[1]).map(([t,n])=>{ const nt=noteByTopic(t); return `<div class="card"><strong>${esc(t)}</strong><div class="muted">${n} ${B('questions','प्रश्नहरू')}</div><button class="btn secondary" onclick="startPracticeTopic('${esc(t)}')">${B('Practice','अभ्यास')}</button>${nt?` <button class="btn secondary" onclick="openNote('${nt.slug}')">📖 ${B('Notes','नोटहरू')}</button>`:''}</div>`; }).join('');
}

/* ---------- Fun facts (data/funfacts.json, 300+ verified, bilingual) ---------- */
const FUNFACT_CATEGORIES = ['Nepal','World','Science','History','Constitution','Geography','Sports','Culture'];
function funFactText(f){ return (lang==='ne' && f.fact_ne) ? f.fact_ne : f.fact_en; }
// The daily fact is deterministic per calendar day (same seed as the daily
// challenge), so everyone sees the same fact on the same day.
function dailyFunFact(){
  if(!FUNFACTS.length) return null;
  const seed=todayStr(); let h=0; for(const ch of seed) h=(h*31+ch.charCodeAt(0))>>>0;
  return FUNFACTS[h % FUNFACTS.length];
}
function randomFunFact(cat){
  const pool = cat ? FUNFACTS.filter(f=>f.category===cat) : FUNFACTS;
  if(!pool.length) return null;
  return pool[Math.floor(Math.random()*pool.length)];
}
function funFactHtml(f){
  if(!f) return '';
  return `<p style="font-size:1.05rem">💡 ${esc(funFactText(f))}</p><p class="muted">${esc(f.category)} · Source: ${esc(f.source)}</p>`;
}
let funFactsShuffled=false;
function renderFunFacts(){
  const box=$('#funfact-box'); if(!box) return;
  if(!dataReady){ box.innerHTML=skelBlock(2); return; }
  if(!FUNFACTS.length){ box.innerHTML=errorState(B('Fun facts could not be loaded','रोचक तथ्यहरू लोड हुन सकेनन्'), B('The fun facts failed to load. Check your connection and try again.','रोचक तथ्यहरू लोड हुन असफल भए। आफ्नो इन्टरनेट कनेक्सन जाँचेर पुनः प्रयास गर्नुहोस्।')); const cnt=$('#funfact-count'); if(cnt) cnt.textContent=''; return; }
  const sel=document.getElementById('funfact-filter');
  if(sel){
    const cur=sel.value;
    sel.innerHTML='<option value="">All categories</option>'+FUNFACT_CATEGORIES.map(c=>`<option value="${esc(c)}">${esc(c)} (${FUNFACTS.filter(f=>f.category===c).length})</option>`).join('');
    if(FUNFACT_CATEGORIES.includes(cur)) sel.value=cur;
  }
  const f=sel?sel.value:'';
  const list0=FUNFACTS.filter(x=>!f||x.category===f);
  const list=funFactsShuffled?shuffle(list0):list0;
  const cnt=$('#funfact-count');
  if(cnt) cnt.textContent = list0.length+' fact(s)'+(f?' in '+f:'')+' of '+FUNFACTS.length+' total';
  box.innerHTML = list.map(x=>`<div class="card"><p>💡 ${esc(funFactText(x))}</p><p class="muted">${esc(x.category)} · Source: ${esc(x.source)}</p></div>`).join('') || errorState(B('Fun facts could not be loaded','रोचक तथ्यहरू लोड हुन सकेनन्'), B('The fun facts failed to load. Check your connection and try again.','रोचक तथ्यहरू लोड हुन असफल भए। आफ्नो इन्टरनेट कनेक्सन जाँचेर पुनः प्रयास गर्नुहोस्।'));
}
function setFunFactFilter(){ funFactsShuffled=false; renderFunFacts(); }
function shuffleFunFacts(){ funFactsShuffled=true; renderFunFacts(); }
function dismissFunFact(){ if(current) current._pendingFact=null; renderQuestion(); }

/* ---------- Practice ---------- */
// Shared "question bank has not loaded" alert for the practice / surprise /
// speed entry points — bilingual, and it says what to do about it.
function bankNotLoadedMsg(){ return B('The question bank has not loaded yet — open this app through a local server (e.g. python3 -m http.server) or GitHub Pages, then try again.','प्रश्न बैंक अझै लोड भएको छैन — यो एप लोकल सर्भर (जस्तै python3 -m http.server) वा GitHub Pages मार्फत खोल्नुहोस्, अनि पुनः प्रयास गर्नुहोस्।'); }
function startPracticeTopic(topic){
  // The topic must have questions tagged for the currently selected exam —
  // otherwise the user would land on an empty practice set. Say so plainly
  // instead of silently practicing something else.
  const exam=document.getElementById('practice-exam').value;
  if(topic && !QUESTIONS.some(q=>q.topic===topic && (!exam||q.exam.includes(exam)))){
    const name=(examById(exam)||{}).name||exam;
    alert(B(`No '${topic}' questions tagged for ${name} yet — try another exam, or pick a topic from the list.`,`'${topic}' का प्रश्न ${name} का लागि अझै ट्याग गरिएको छैन — अर्को परीक्षा प्रयास गर्नुहोस् वा सूचीबाट विषय छान्नुहोस्।`));
    return;
  }
  const sel=document.getElementById('practice-topic'); if(sel) sel.value=topic;
  showView('practice'); startPractice();
}
function filteredQuestions(){
  const exam=document.getElementById('practice-exam').value;
  const topic=document.getElementById('practice-topic').value;
  const diff=document.getElementById('practice-diff').value;
  let pool=QUESTIONS.filter(q=> (!topic||q.topic===topic) && (!diff||q.difficulty===diff) && (!exam||q.exam.includes(exam)));
  return pool;
}
function startPractice(){
  const count=parseInt(document.getElementById('practice-count').value,10)||10;
  const timerOn=document.getElementById('practice-timer').checked;
  const negOn=document.getElementById('practice-neg').checked;
  const exam=document.getElementById('practice-exam').value;
  let pool=shuffle(filteredQuestions());
  const qs=pool.slice(0, Math.min(count, pool.length)).map(q=>shuffleOptions(q));
  if(!qs.length){
    if(!QUESTIONS.length){ alert(bankNotLoadedMsg()); return; }
    const examObj=examById(exam);
    const topic=document.getElementById('practice-topic').value;
    const diff=document.getElementById('practice-diff').value;
    const bits=[examObj?examObj.name:exam, topic, diff].filter(Boolean).join(' · ');
    alert(B(`No questions match ${bits} — try another topic or difficulty.`,`${bits} सँग मिल्ने प्रश्न छैन — अर्को विषय वा कठिनाइ प्रयास गर्नुहोस्।`));
    return;
  }
  const examObj=examById(exam);
  const examNeg=examObj&&examObj.prelim ? mockNegRate(examObj.prelim) : 0.2;
  const examMarks=examObj&&examObj.prelim ? examObj.prelim.marksPerQ : null;
  const normQs=qs.map(q=> examMarks!=null ? {...q, marks:examMarks} : q);
  current={ mode:'practice', exam, questions:normQs, answers:Array(normQs.length).fill(null), idx:0, negOn: negOn && examNeg>0, negRate: negOn?examNeg:0, timerOn, startTime:Date.now(), perQ:[] };
  if(timerOn){
    const examObj2=examById(exam);
    const perQSecs=(examObj2&&examObj2.prelim&&examObj2.prelim.timeMin!=null) ? Math.round(examObj2.prelim.timeMin*60/examObj2.prelim.questions) : 54;
    timeLeft=normQs.length*perQSecs; startTimer(()=>finishAttempt(true));
  }
  showView('quiz'); renderQuestion();
}
function startTimer(onTimeout){
  clearInterval(timerId);
  timerId=setInterval(()=>{ timeLeft--; const t=$('#quiz-timer'); if(t) t.textContent=fmtTime(timeLeft);
    if(t && timeLeft<=300) t.classList.add('low');
    if(timeLeft<=0){ clearInterval(timerId); onTimeout(); } },1000);
}
function fmtTime(s){ s=Math.max(0,s); return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0'); }

function renderQuestion(){
  const c=current; const q=c.questions[c.idx];
  const box=$('#quiz-box'); const total=c.questions.length;
  const answered=c.answers.filter(a=>a!==null).length;
  // Time per question so far (average of the answered ones, in seconds).
  const times=c.perQ.filter(x=>x!=null);
  const pace=times.length? Math.round(times.reduce((a,b)=>a+b,0)/times.length/1000)+'s / Q' : '—';
  // "Take a break" nudge: every 20 answered questions in this session, until dismissed.
  const showBreak=answered>0 && answered%20===0 && c.breakShownAt!==answered;
  const examLabel = c.title ? esc(c.title) : esc(examById(c.exam)?.name||c.exam);
  const speedMode = c.mode==='speed';
  const mockMode = c.mode==='mock';
  const modeLabel = c.mode==='mock' ? B('Mock Exam','मक परीक्षा') : speedMode ? B('⚡ Speed Round','⚡ स्पिड राउन्ड') : B('Practice','अभ्यास');
  const qOfTotal = B('Question','प्रश्न')+' '+(c.idx+1)+' '+B('of','/')+' '+total;
  const marksLabel = q.marks+' '+B(q.marks>1?'marks':'mark','अङ्क');
  const negLabel = c.negOn ? `(−${Math.round(c.negRate*100)}% ${B('if wrong','गलत भएमा')})` : '';
  // Discussing navigates away from the quiz — in a timed mock that stops the
  // timer and silently abandons the attempt, so the button is hidden during
  // mocks (it stays available in practice and on the result review screen).
  const showDiscuss = !speedMode && !mockMode;
  const best = speedMode ? getSpeedBest() : null;
  // Practice only: after every 5th answered question a skippable fun fact
  // appears between questions. It never blocks answering — the question and
  // its Next button stay visible underneath, and dismissing just hides it.
  const factCard = c._pendingFact ? `<div class="card funfact-card"><h3>💡 Did you know?</h3>${funFactHtml(c._pendingFact)}<button class="btn secondary" onclick="dismissFunFact()">Continue →</button></div>` : '';
  box.innerHTML=`${factCard}
    <div class="card quiz-card${c.answers[c.idx]!==null?' answered':''}"><div class="muted">${modeLabel} · ${examLabel} · ${qOfTotal} · ${marksLabel} ${negLabel}</div>
    ${speedMode?`<p class="muted">${B(`⏱️ 60 seconds for all ${total} questions · +1 bonus for a correct answer in under 5s`,`⏱️ जम्मा ${total} प्रश्नका लागि ६० सेकेन्ड · ५ सेकेन्डभित्र सही उत्तरमा +१ बोनस`)}${best?` · ${B('Best speed score:','उत्कृष्ट स्पिड स्कोर:')} ${best.score}/${best.max} (${best.pct}%) ${B('on','मिति')} ${best.date}`:''}</p>`:''}
    <div class="session-bar" title="${qOfTotal}"><div style="width:${((c.idx+1)/total*100).toFixed(1)}%"></div></div>
    <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap"><span class="timer" id="quiz-timer">${c.timerOn?fmtTime(timeLeft):B('No timer','टाइमर छैन')}</span><span class="muted">⏱ ${pace}</span><span class="muted">${B('Answered','उत्तर दिइएको')} ${answered}/${total}</span></div>
    <div class="progress-bar"><div style="width:${(answered/total*100).toFixed(0)}%"></div></div>
    <h2 class="q-text" style="margin:14px 0">${esc(qText(q))}</h2>
    <div class="tag">${esc(q.topic)} · ${esc(q.subtopic||'')} · ${esc(q.difficulty)} ${communityBadge(q)}</div>
    ${qOpts(q).map((o,i)=>`<button class="opt ${c.answers[c.idx]===i?'selected':''}" data-i="${i}" style="animation-delay:${i*45}ms" onclick="answerOption(${i})">${String.fromCharCode(65+i)}. ${esc(o)}</button>`).join('')}
    <div id="feedback" aria-live="polite"></div>
    ${showBreak?`<div class="break-nudge" role="status">☕ <strong>${B('You have answered','तपाईंले')} ${answered} ${B('questions in this session.','प्रश्नको उत्तर दिनुभयो।')}</strong> ${B('Take a short break — stretch, drink some water, then come back fresh. Leaving this page abandons the session — it will not be scored.','छोटो ब्रेक लिनुहोस् — तन्किनुहोस्, पानी पिउनुहोस्, अनि ताजा भएर फर्कनुहोस्। यो पेज छोडेमा सत्र त्यागिन्छ — स्कोर हुँदैन।')}<br><button class="btn secondary" onclick="dismissBreak()">${B('Got it — keep going','बुझें — जारी राख्नुहोस्')}</button> <button class="btn secondary" onclick="takeABreak()">${B('Take a break','ब्रेक लिनुहोस्')}</button></div>`:''}
    <div style="margin-top:12px">
      ${speedMode?'':`<button class="btn secondary" onclick="prevQ()" ${c.idx===0?'disabled':''}>${B('← Previous','← अघिल्लो')}</button>`}
      <button class="btn secondary" onclick="skipQ()">${B('Skip','छोड्नुहोस्')}</button>
      ${speedMode?'':`<button class="btn secondary" onclick="bookmarkCurrent()">🔖 ${B('Bookmark','बुकमार्क')}</button>
      <button class="btn secondary" onclick="flagCurrent()">⚑ ${B('Report wrong','गलत रिपोर्ट')}</button>`}
      ${showDiscuss?`<button class="btn secondary" onclick="discussQuestion(current.questions[current.idx].id)">💬 ${B('Discuss this question','यो प्रश्न छलफल गर्नुहोस्')}</button>`:''}
      ${c.idx<total-1?`<button class="btn" onclick="nextQ()">${B('Next →','अर्को →')}</button>`:`<button class="btn green" onclick="finishAttempt(false)">${B('Finish &amp; See Result','सक्नुहोस् र नतिजा हेर्नुहोस्')}</button>`}
    </div></div>
    ${c.mode==='mock'?`<div class="card"><strong>${B('Question palette','प्रश्न प्यालेट')}</strong><div class="palette" ${c.questions.length>100?'style="max-height:220px;overflow-y:auto"':''}>${c.questions.map((_,i)=>`<button class="${c.answers[i]!==null?'answered':''} ${i===c.idx?'current':''}" onclick="jumpTo(${i})">${i+1}</button>`).join('')}</div></div>`:''}`;
  // Glide both bars from their previous widths instead of jumping.
  const bar=document.querySelector('#quiz-box .progress-bar>div');
  const sbar=document.querySelector('#quiz-box .session-bar>div');
  const pct=answered/total*100, spct=(c.idx+1)/total*100;
  if(bar) animateWidth(bar, c._lastBarPct!=null?c._lastBarPct:pct, pct);
  if(sbar) animateWidth(sbar, c._lastSessPct!=null?c._lastSessPct:spct, spct);
  c._lastBarPct=pct; c._lastSessPct=spct;
  if(c.mode==='practice' && c.answers[c.idx]!==null) showFeedback();
}
function dismissBreak(){
  if(!current) return;
  current.breakShownAt=current.answers.filter(a=>a!==null).length;
  renderQuestion();
}
// Leaving the quiz abandons the session (showView stops the timer and the
// attempt is never recorded) — say so before a timed session is thrown away.
function takeABreak(){
  if(current && current.timerOn && !confirm(B('Take a break? Leaving now abandons this timed session — it will not be scored.','ब्रेक लिने? अहिले छोडेमा यो समयबद्ध सत्र त्यागिन्छ — स्कोर हुँदैन।'))) return;
  showView('home');
}
function answerOption(i){
  const c=current; if(!c) return; const q=c.questions[c.idx];
  // Speed Round: no per-question feedback (it would eat the clock) — tap an
  // answer and move on instantly; the bonus is for correct answers < 5s.
  if(c.mode==='speed'){
    const elapsed=Date.now()-(c.qStart||c.startTime);
    c.perQ[c.idx]=elapsed; c.answers[c.idx]=i;
    if(c.idx<c.questions.length-1){ c.idx++; c.qStart=Date.now(); renderQuestion(); }
    else finishAttempt(false);
    return;
  }
  if(c.mode==='practice' && c.answers[c.idx]!==null) return; // lock after answering in practice
  c.answers[c.idx]=i; c.perQ[c.idx]=Date.now()- (c.qStart||c.startTime);
  // After every 5th question in practice (not mocks, not the last question),
  // queue a fun fact to show between questions — skippable, never blocking.
  if(c.mode==='practice' && (c.idx+1)%5===0 && c.idx<c.questions.length-1) c._pendingFact=randomFunFact();
  if(c.mode==='practice'){ showFeedback(); saveMistakeIfWrong(); }
  if(c.mode==='mock'){ saveMistakeIfWrong(); }
  renderQuestion();
}
function showFeedback(){
  const c=current, q=c.questions[c.idx], a=c.answers[c.idx]; const fb=document.getElementById('feedback'); if(!fb) return;
  const ok=a===q.answer;
  const line=ok?pickLine(PRAISE_LINES,'praise'):pickLine(TRY_AGAIN_LINES,'try');
  fb.innerHTML=`<div class="expl"><strong>${ok?B('✅ Correct!','✅ सही!'):B('❌ Wrong.','❌ गलत।')}</strong> ${B('Correct answer:','सही उत्तर:')} <strong>${String.fromCharCode(65+q.answer)}. ${esc(qOpts(q)[q.answer])}</strong><br>${esc(qExpl(q))}</div><div class="encourage">${esc(line)}</div>`;
  document.querySelectorAll('.opt').forEach(b=>{ const i=+b.dataset.i; b.disabled=true; if(i===q.answer) b.classList.add('correct'); else if(i===a) b.classList.add('wrong'); });
}
function saveMistakeIfWrong(){
  const c=current, q=c.questions[c.idx];
  if(c.answers[c.idx]!==q.answer && !progress.mistakes.includes(q.id)){ progress.mistakes.push(q.id); saveProgress(); }
}
function nextQ(){ if(current) current._pendingFact=null; if(current.idx<current.questions.length-1){ current.idx++; current.qStart=Date.now(); renderQuestion(); } }
function prevQ(){ if(current) current._pendingFact=null; if(current.idx>0){ current.idx--; renderQuestion(); } }
function skipQ(){ current.answers[current.idx]=null; if(current.idx<current.questions.length-1) nextQ(); else renderQuestion(); }
function jumpTo(i){ if(current) current._pendingFact=null; current.idx=i; renderQuestion(); }
function bookmarkCurrent(){ const id=current.questions[current.idx].id; if(!progress.bookmarks.includes(id)){ progress.bookmarks.push(id); saveProgress(); alert(B('Bookmarked ✓','बुकमार्क भयो ✓')); } else alert(B('Already bookmarked.','पहिले नै बुकमार्क गरिएको छ।')); }
function flagCurrent(){ openReportForm(current.questions[current.idx].id); }

function finishAttempt(timedOut){
  clearInterval(timerId); const c=current; if(!c) return;
  // One attempt = one record. Without this guard a double-tap on "Finish"
  // (or the timer expiring in the same instant as the last speed-round
  // answer) scored the attempt twice — double XP, double history entry.
  if(c._finished) return; c._finished=true;
  const res=scoreAttempt(c.answers, c.questions, c.negOn, c.negRate==null?0.2:c.negRate);
  // Speed Round bonus: +1 per correct answer given in under 5 seconds.
  // The bonus is added to the score (pct capped at 100) and recorded on
  // the attempt, so it counts toward XP and the saved best speed score.
  if(c.mode==='speed'){
    let bonus=0;
    c.questions.forEach((q,i)=>{ bonus+=speedBonusFor(c.perQ[i], c.answers[i]===q.answer); });
    res.speedBonus=bonus; res.score=Math.min(res.max, Math.round((res.score+bonus)*10)/10);
    res.pct=res.max?Math.min(100, Math.round((Math.max(res.score,0)/res.max)*1000)/10):0;
    const prevBest=getSpeedBest();
    if(!prevBest || res.score>prevBest.score) saveSpeedBest({score:res.score, max:res.max, pct:res.pct, bonus, date:todayStr()});
  }
  // Speed-round wrong answers join the Mistakes list, like practice/mock
  // wrong answers do — otherwise the Mistake Marathon could never drill
  // them. Skips (null) are not mistakes, same as practice mode.
  if(c.mode==='speed'){
    c.questions.forEach((q,i)=>{ if(c.answers[i]!==null && c.answers[i]!==q.answer && !progress.mistakes.includes(q.id)) progress.mistakes.push(q.id); });
  }
  // Pass/fail is judged on PERCENTAGE vs the exam's cutoff percentage, not on the
  // raw full-paper cutoff: a 10-question practice set (max 19–20) can never reach
  // 45/100, but a 100% practice set is a pass. For a full-length mock the two
  // are identical (e.g. Kharidar: 45% of 100 = 45).
  const examObj=examById(c.exam);
  const cutoffPct=(examObj && examObj.prelim)? Math.round(examObj.prelim.pass/examObj.prelim.total*100) : 45;
  const cutoff=cutoffFor(c.exam); const passed=res.pct>=cutoffPct;
  const secs=Math.round((Date.now()-c.startTime)/1000);
  const xp=c._dailyRepeat?0:xpFor(res.score, res.max); const oldLevel=progress.level; progress.xp+=xp; progress.level=levelFromXp(progress.xp); updateStreak();
  // Daily Challenge: the day counts as done only now, on finish — an
  // abandoned challenge (navigation away, closed tab) never reaches here,
  // so it does not burn the day's XP (see dailyChallenge).
  if(c._dailySeed){ progress.dailyDone=progress.dailyDone||{}; progress.dailyDone[c._dailySeed]=true; }
  const leveledUp=progress.level>oldLevel;
  const attempt={ date:new Date().toISOString(), mode:c.mode, exam:c.exam, total:c.questions.length, ...res, passed, cutoff, cutoffPct, secs, xp, timedOut:!!timedOut,
    // Per-question detail powers the analytics views (coverage, coach, PYQ
    // heatmap, planner rebalancing). Compact rows: t=topic, c=1 correct /
    // 0 wrong / -1 skipped, m=marks. Old attempts simply lack this field and
    // are handled gracefully by the analytics helpers.
    qdetail:c.questions.map((q,i)=>({t:q.topic||'General', c:c.answers[i]===q.answer?1:(c.answers[i]==null?-1:0), m:q.marks||1})) };
  progress.attempts.push(attempt); saveProgress();
  const weeklyMet = checkWeeklyGoal(); // first attempt that crosses this week's goal line
  // per-topic breakdown
  const byTopic={}; c.questions.forEach((q,i)=>{ const t=q.topic; byTopic[t]=byTopic[t]||{total:0,correct:0}; byTopic[t].total++; if(c.answers[i]===q.answer) byTopic[t].correct++; });
  const worst=Object.entries(byTopic).sort((a,b)=>(a[1].correct/a[1].total)-(b[1].correct/b[1].total)).slice(0,3);
  const best=Object.entries(byTopic).sort((a,b)=>(b[1].correct/b[1].total)-(a[1].correct/a[1].total)).slice(0,3);
  const wrongList=c.questions.map((q,i)=>({q, a:c.answers[i]})).filter(x=>x.a!==null && x.a!==x.q.answer);
  current._wrong=wrongList.map(x=>x.q); current._exam=c.exam; current._neg=c.negOn; current._negRate=c.negRate;
  // Stored so a language toggle on the result view can re-render it without
  // re-scoring (finishAttempt must run exactly once per attempt).
  current._res={res, cutoffPct, cutoff, passed, secs, xp, timedOut:!!timedOut, worst, best, wrongList, leveledUp, oldLevel, weeklyMet};
  renderResult();
  showView('result');
}
function renderResult(){
  const c=current; const r=c._res; if(!c||!r) return;
  const rf=randomFunFact();
  const {res, cutoffPct, cutoff, passed, secs, xp, timedOut, worst, best, wrongList, leveledUp, weeklyMet}=r;
  const examObj=examById(c.exam);
  const box=$('#result-box');
  // Score ring: circumference for r=52 is 2π·52 ≈ 326.7. The final offset is
  // written inline so the ring is correct even without animation; JS then
  // animates it from full (empty) when requestAnimationFrame exists.
  const CIRC=326.7, ringOff=(CIRC*(1-Math.max(0,Math.min(100,res.pct))/100)).toFixed(1);
  const cheer=passed?pickLine(PASS_LINES,'pass'):pickLine(FAIL_LINES,'fail');
  const speedBest=getSpeedBest();
  const fullTotal = examObj && examObj.prelim ? examObj.prelim.total : 100;
  // NMC MBBS only: the mock is the 130-MCQ part of a 180-mark paper (the 10
  // clinical scenario questions are not in this mock); pass is judged on
  // percentage, not on 90 raw marks. No other exam has total != max, so this
  // note must NOT fire for a merely short mock on another exam.
  const cutoffNote = (c.exam === 'nmc-mbbs' && examObj && examObj.prelim && examObj.prelim.total !== res.max) ? B(` (mock covers ${res.max} of ${examObj.prelim.total} marks — the 10 clinical scenario questions are not in this mock; pass is judged on percentage, not on ${cutoff} raw marks)`,` (मकमा ${examObj.prelim.total} मध्ये ${res.max} अङ्क मात्र — १० वटा क्लिनिकल सिनारियो प्रश्न मकमा छैनन्; पास प्रतिशतका आधारमा हुन्छ, ${cutoff} कच्चा अङ्कका आधारमा होइन)`) : '';
  const proxyNote = (c.exam==='mecee-bl') ? B(' — the real MECEE-BL pass is the 50th percentile (merit rank), not 50% marks; this is a rough proxy only',' — वास्तविक MECEE-BL पास ५०औँ पर्सेन्टाइल (मेरिट र्‍याङ्क) हो, ५०% अङ्क होइन; यो मोटामोटी अनुमान मात्र हो') : '';
  const negLine = !c.negOn ? B('Negative marking OFF — this exam has no negative marking.','नेगेटिभ मार्किङ बन्द — यो परीक्षामा नेगेटिभ मार्किङ छैन।')
    : B(`Negative marking ON (−${(c.negRate*(c.questions[0]?.marks||1)).toFixed(2).replace(/0$/,'')} per wrong question, ${Math.round(c.negRate*100)}%)`,`नेगेटिभ मार्किङ चालु (प्रति गलत प्रश्न −${(c.negRate*(c.questions[0]?.marks||1)).toFixed(2).replace(/0$/,'')}, ${Math.round(c.negRate*100)}%)`);
  box.innerHTML=`<div class="card" style="text-align:center">
    <div class="muted">${c.mode==='mock'?B('Mock Exam','मक परीक्षा'):B('Practice','अभ्यास')} · ${esc(c.title || examById(c.exam)?.name || B('Mixed practice','मिश्रित अभ्यास'))} ${timedOut?B('(time up — auto-submitted)','(समय सकियो — स्वतः बुझाइयो)'):''}</div>
    <div class="score-wrap">
      <svg class="score-ring" viewBox="0 0 120 120" width="148" height="148" aria-hidden="true">
        <circle class="ring-bg" cx="60" cy="60" r="52"></circle>
        <circle class="ring-fg ${passed?'':'fail-ring'}" cx="60" cy="60" r="52" data-off="${ringOff}" style="stroke-dashoffset:${ringOff}"></circle>
      </svg>
      <div class="score-center"><div class="result-big ${passed?'pass':'fail'}">${res.score} / ${res.max}</div><div class="muted">${res.pct}%</div></div>
    </div>
    <div><strong class="${passed?'pass':'fail'}">${passed?B('✅ PASS','✅ पास'):B('❌ FAIL','❌ फेल')}</strong> — ${B('cutoff for this exam is','यो परीक्षाको कटअफ')} ${cutoffPct}% (${cutoff}/${fullTotal} ${B('on the full paper','पूर्ण पेपरमा')})${cutoffNote}${proxyNote} &nbsp;·&nbsp; ${res.pct}%</div>
    <p>${B('Correct','सही')} ${res.correct} · ${B('Wrong','गलत')} ${res.wrong} · ${B('Skipped','छोडिएको')} ${res.skipped} · ${B('Time','समय')} ${fmtTime(secs)} (${Math.round(secs/Math.max(1,c.questions.length))}${B('s per question','सेकेन्ड/प्रश्न')}) · +${xp} XP · ${B('Level','लेभल')} ${progress.level} · 🔥 ${B('Streak','स्ट्रिक')} ${progress.streak} ${B('day(s)','दिन')}</p>
    ${c.mode==='speed'?`<p>${B('⚡ Speed Round bonus:','⚡ स्पिड राउन्ड बोनस:')} <strong>+${res.speedBonus||0}</strong> ${B('fast correct answer(s) under 5s','५ सेकेन्डभित्रका छिटो सही उत्तर')}${speedBest?` · ${B('Best speed score:','उत्कृष्ट स्पिड स्कोर:')} ${speedBest.score}/${speedBest.max} (${speedBest.pct}%) ${B('on','मिति')} ${speedBest.date}`:''}</p>`:''}
    ${leveledUp?`<div class="levelup-banner" role="status">${B('🎉 LEVEL UP! You are now Level '+progress.level+'!','🎉 लेभल अप! तपाईं अब लेभल '+progress.level+' मा हुनुहुन्छ!')}</div>`:''}
    ${weeklyMet?`<div class="levelup-banner gold" role="status">🏆 ${B('Weekly goal smashed! Weekly Champion badge earned.','साप्ताहिक लक्ष्य पूरा! Weekly Champion ब्याज प्राप्त भयो।')}</div>`:''}
    <p class="encourage" style="text-align:left">${esc(cheer)}</p>
    <p class="muted">${negLine}</p>
    <button class="btn" onclick="retryWrong()">${B('Retry wrong only ('+wrongList.length+')','गलत मात्र दोहोर्‍याउनुहोस् ('+wrongList.length+')')}</button>
    <button class="btn secondary" onclick="newRandomSet()">🔀 ${B('New random set','नयाँ र्‍यान्डम सेट')}</button>
    ${worst.length?`<button class="btn secondary" onclick="startPracticeTopic('${esc(worst[0][0])}')">📚 ${B('Practice weakest topic: ','कमजोर विषय अभ्यास: ')}${esc(worst[0][0])}</button>`:''}
    <button class="btn secondary" onclick="shareScore()">📋 ${B('Share my score','मेरो स्कोर सेयर गर्नुहोस्')}</button> <span id="share-status" class="muted" role="status"></span>
    <button class="btn secondary" onclick="showView('dashboard')">${B('View dashboard','ड्यासबोर्ड हेर्नुहोस्')}</button></div>
    ${rf?`<div class="card funfact-card"><h3>💡 ${B('Did you know?','के तपाईंलाई थाहा छ?')}</h3>${funFactHtml(rf)}</div>`:''}
    <div class="card"><h3>${B('Topic breakdown','विषय विश्लेषण')}</h3><p><strong>${B('Strongest:','सबल:')}</strong> ${best.map(([t,v])=>esc(t)+' '+v.correct+'/'+v.total).join(' · ')||'—'}</p><p><strong>${B('Weakest — revise these:','कमजोर — यी दोहोर्‍याउनुहोस्:')}</strong> ${worst.map(([t,v])=>esc(t)+' '+v.correct+'/'+v.total).join(' · ')||'—'}</p></div>
    <div class="card"><h3>${B('Wrong answers — review','गलत उत्तर — समीक्षा')}</h3>${wrongList.length? wrongList.map(({q,a})=>`<div style="margin-bottom:12px"><strong>${esc(qText(q))}</strong><br>${B('Your answer:','तपाईंको उत्तर:')} ${String.fromCharCode(65+a)}. ${esc(qOpts(q)[a])}<br>${B('Correct:','सही:')} <strong>${String.fromCharCode(65+q.answer)}. ${esc(qOpts(q)[q.answer])}</strong><br><span class="muted">${esc(qExpl(q))}</span><br><button class="btn secondary" onclick="discussQuestion('${esc(q.id)}')">💬 ${B('Discuss this question','यो प्रश्न छलफल गर्नुहोस्')}</button> <button class="btn secondary" onclick="openReportForm('${esc(q.id)}')">⚑ ${B('Report wrong question','गलत प्रश्न रिपोर्ट')}</button>${noteByTopic(q.topic)?` <button class="btn secondary" onclick="reviseTopic('${esc(q.topic)}')">📖 ${B('Revise this topic','यो विषय दोहोर्‍याउनुहोस्')}</button>`:''}</div>`).join(''):'<p>🎉 '+B('No wrong answers — perfect set!','गलत उत्तर छैन — उत्कृष्ट सेट!')+'</p>'}</div>`;
  // Animated score reveal: count the score up and sweep the ring in.
  // Everything is guarded — in the Node test stubs requestAnimationFrame is
  // absent, so the final values written in the HTML above simply stay.
  // Reduced motion also skips the animation and keeps the final values.
  if (typeof requestAnimationFrame === 'function' && !prefersReducedMotion()) {
    const scoreEl = document.querySelector('#result-box .result-big');
    if (scoreEl) {
      const target = res.score, max = res.max, t0 = Date.now();
      const tick = () => {
        const p = Math.min(1, (Date.now() - t0) / 800);
        const eased = 1 - Math.pow(1 - p, 3);
        scoreEl.textContent = (Math.round(target * eased * 10) / 10) + ' / ' + max;
        if (p < 1) requestAnimationFrame(tick);
      };
      scoreEl.textContent = '0 / ' + max;
      requestAnimationFrame(tick);
    }
    const ring = document.querySelector('#result-box .ring-fg');
    if (ring && ring.style) {
      const targetOff = parseFloat(ring.getAttribute('data-off') || '0');
      ring.style.strokeDashoffset = 326.7;
      requestAnimationFrame(() => { ring.style.strokeDashoffset = targetOff; });
    }
  }
  // Celebration only on a pass or a level-up — never on a fail.
  if (passed || leveledUp) launchConfetti();
}
function retryWrong(){
  const qs=(current._wrong||[]).map(q=>shuffleOptions(q));
  if(!qs.length){ alert(B('Nothing to retry!','दोहोर्‍याउन केही छैन!')); return; }
  current={ mode:'practice', exam:current._exam, questions:qs, answers:Array(qs.length).fill(null), idx:0, negOn:current._neg, negRate:current._negRate==null?0.2:current._negRate, timerOn:false, startTime:Date.now(), perQ:[] };
  showView('quiz'); renderQuestion();
}
function newRandomSet(){
  const s=document.getElementById('practice-exam');
  // Keep the finished exam — including the exam-less modes (Daily Challenge,
  // Surprise, Quick Quiz, Speed Round), which map to the 🌐 mixed option
  // (value ''), not to whatever the select happened to hold before.
  if(s && current) s.value=current.exam||'';
  showView('practice'); startPractice();
}

/* ---------- Mock exams ---------- */
// Topic-mix for the four prelims whose breakdown is a plain "Topic N Q + Topic M Q"
// count. Returns {topic: count} or null when the breakdown is not parseable
// (percentages, prose, or licence weight tables) — callers fall back to a
// uniform draw from the tagged pool.
function mockMixFor(e){
  const m={};
  if(e.id==='kharidar'){ m['Office Management & Public Service']=20; }
  else if(e.id==='nasu'){ m['IQ & Reasoning']=20; }
  else if(e.id==='section-officer'){ m['English']=20; }
  else if(e.id==='nrb-assistant'){ /* Mgmt/Acct+Econ/Banking are not topics; fall through */ return null; }
  else return null;
  return m;
}
function startMock(){
  const examId=document.getElementById('mock-exam').value; const e=examById(examId); if(!e){ alert(B('Exams not loaded yet — please wait a moment and try again.','परीक्षाहरू अझै लोड भएका छैनन् — केहीबेर पर्खेर पुनः प्रयास गर्नुहोस्।')); return; }
  // Guide-only exams have no MCQ prelim and must never start a mock. They are
  // hidden from the mock dropdown, but guard here too (e.g. startMockFor()).
  if(!e.prelim){ alert(e.name+B(' has no MCQ prelim paper — see its Exam Guide page instead. No mock can be started for it.',' को MCQ प्रिलिम पेपर छैन — बरु यसको Exam Guide पेज हेर्नुहोस्। यसका लागि मक सुरु गर्न सकिँदैन।')); return; }
  const p=e.prelim;
  const negRate=mockNegRate(p);
  // Mirror the real paper: use the exam's topic mix where possible, otherwise random from its tagged pool.
  let pool=QUESTIONS.filter(q=>q.exam.includes(examId));
  const tagged=pool.length;
  if(pool.length < p.questions) pool=QUESTIONS.slice();
  const mix=mockMixFor(e);
  let qs;
  if(mix){
    const rest=QUESTIONS.filter(q=>q.exam.includes(examId));
    const picked=[];
    for(const [topic,n] of Object.entries(mix)){
      picked.push(...shuffle(rest.filter(q=>q.topic===topic)).slice(0,n));
    }
    const used=new Set(picked.map(q=>q.id));
    picked.push(...shuffle(rest.filter(q=>!used.has(q.id))).slice(0, p.questions-picked.length));
    qs=shuffle(picked).map(q=>shuffleOptions({...q, marks:p.marksPerQ}));
  } else {
    qs=shuffle(pool).slice(0, p.questions).map(q=>shuffleOptions({...q, marks:p.marksPerQ}));
  }
  // timeMin null (e.g. TSC Teaching Licence — time limit unverified): run the mock
  // UNTIMED rather than starting a 0-second timer that would auto-submit instantly.
  const timed=p.timeMin!=null;
  current={ mode:'mock', exam:examId, questions:qs, answers:Array(qs.length).fill(null), idx:0, negOn:negRate>0, negRate, timerOn:timed, startTime:Date.now(), perQ:[] };
  if(timed){ timeLeft=p.timeMin*60; startTimer(()=>finishAttempt(true)); }
  showView('quiz'); renderQuestion();
  const negText=p.negative===null?B('negative marking unverified — NOT applied in this mock','नेगेटिभ मार्किङ अपुष्ट — यो मकमा लागू हुँदैन'):(p.negative===0?B('no negative marking','नेगेटिभ मार्किङ छैन'):Math.round(negRate*100)+B('% negative marking','% नेगेटिभ मार्किङ'));
  const timeText=timed?`${p.timeMin} ${B('minutes','मिनेट')}`:B('no time limit (time unverified — check the notice)','समय सीमा छैन (समय अपुष्ट — सूचना हेर्नुहोस्)');
  // Honesty guard for thin banks: if the tagged pool is smaller than the paper,
  // the mock silently draws from the whole bank (pre-existing fallback). Say so
  // instead of letting the student believe it mirrors the real paper.
  const thinText=tagged<p.questions?` ⚠️ ${B('Only '+tagged+' question'+(tagged===1?' is':'s are')+' tagged for '+e.name+' so far, so this mock also draws from the general bank — it does not mirror the real paper yet.','अहिलेसम्म '+e.name+' का लागि जम्मा '+tagged+' प्रश्न ट्याग गरिएको छ, त्यसैले यो मक सामान्य बैंकबाट पनि प्रश्न लिन्छ — यसले वास्तविक पेपरको प्रतिलिपि गर्दैन।')}`:'';
  alert(B(`Mock started: ${e.name} — ${p.questions} questions, ${timeText}, ${p.marksPerQ} mark${p.marksPerQ>1?'s':''} each, ${negText}, pass ${p.pass}. Good luck!`,`मक सुरु भयो: ${e.name} — ${p.questions} प्रश्न, ${timeText}, प्रति प्रश्न ${p.marksPerQ} अङ्क, ${negText}, पास ${p.pass}। शुभकामना!`)+thinText);
}

/* ---------- Daily challenge / Quick quiz / Flashcards ---------- */
function dailyChallenge(){
  const seed0=todayStr();
  const repeat0=!!(progress.dailyDone||{})[seed0];
  if(repeat0){ if(!confirm('You already did today’s Daily Challenge. Do it again for practice (no extra XP)?')) return; }
  const seed=todayStr(); let h=0; for(const ch of seed) h=(h*31+ch.charCodeAt(0))>>>0;
  const rand=()=>{ h=(h*1664525+1013904223)>>>0; return h/4294967296; };
  const qs=shuffle(QUESTIONS, rand).slice(0,10).map(q=>shuffleOptions(q, rand));
  current={ mode:'practice', exam:'', title:'🔥 Daily Challenge', questions:qs, answers:Array(qs.length).fill(null), idx:0, negOn:true, negRate:0.2, timerOn:false, startTime:Date.now(), perQ:[] };
  // The day is marked done only when the challenge is FINISHED (see
  // finishAttempt). Marking it here used to burn the day's XP if the user
  // navigated away or closed the tab mid-challenge — abandoning no longer
  // costs the day.
  if(repeat0) current._dailyRepeat=true;
  current._dailySeed=seed;
  showView('quiz'); renderQuestion();
}
function quickQuiz(){
  const qs=shuffle(QUESTIONS).slice(0,5).map(q=>shuffleOptions(q));
  current={ mode:'practice', exam:'', title:'⚡ Quick Quiz', questions:qs, answers:Array(qs.length).fill(null), idx:0, negOn:true, negRate:0.2, timerOn:false, startTime:Date.now(), perQ:[] };
  showView('quiz'); renderQuestion();
}
let flashIdx=0, flashQs=[];
function startFlashcards(){
  const fe=document.getElementById('flash-exam');
  const fExam=fe?fe.value:'';
  const fPool=fExam?QUESTIONS.filter(q=>q.exam.includes(fExam)):QUESTIONS;
  flashQs=shuffle(fPool.length?fPool:QUESTIONS).slice(0,20); flashIdx=0; progress.flashcardsSeen++; saveProgress(); renderFlash();
}
function renderFlash(){
  const q=flashQs[flashIdx]; if(!q){ $('#flash-box').innerHTML='<p>'+B('Done! 🎉','सकियो! 🎉')+'</p>'; return; }
  $('#flash-box').innerHTML=`<div class="card flash"><div class="tag">${esc(q.topic)} · ${flashIdx+1}/${flashQs.length}</div><p style="margin:14px 0">${esc(qText(q))}</p><button class="btn" onclick="revealFlash()">Reveal answer</button><div id="flash-ans"></div><div style="margin-top:14px"><button class="btn secondary" onclick="flashNext()">Next →</button></div></div>`;
}
function revealFlash(){ const q=flashQs[flashIdx]; document.getElementById('flash-ans').innerHTML=`<p><strong>${String.fromCharCode(65+q.answer)}. ${esc(qOpts(q)[q.answer])}</strong></p><p class="muted">${esc(qExpl(q))}</p>`; }
function flashNext(){ flashIdx++; renderFlash(); }

/* ---------- Review / Dashboard / Search / Guide ---------- */
// One-pass id → question map. renderReview / weakTopics used to call
// QUESTIONS.find() per bookmark/mistake — a linear scan of the 59k bank
// for every saved id.
function questionByIdMap(){
  const m=new Map(); QUESTIONS.forEach(q=>m.set(q.id,q)); return m;
}
function renderReview(){
  const byIdMap=questionByIdMap();
  const byId=id=>byIdMap.get(id);
  const bm=progress.bookmarks.map(byId).filter(Boolean);
  const mk=progress.mistakes.map(byId).filter(Boolean);
  const reviseBtn=q=>{ const n=noteByTopic(q.topic); return n?` <button class="btn secondary" onclick="reviseTopic('${esc(q.topic)}')">📖 ${B('Revise this topic','यो विषय दोहोर्‍याउनुहोस्')}</button>`:''; };
  const emptyBm=emptyState('🔖', B('No bookmarks yet','अझै बुकमार्क छैन'), B('Tap 🔖 on any question during practice to save it here for revision.','अभ्यासका क्रममा कुनै पनि प्रश्नमा 🔖 थिचेर दोहोर्‍याउन यहाँ सेभ गर्नुहोस्।'), B('Start practicing','अभ्यास सुरु गर्नुहोस्'), "showView('practice')");
  const emptyMk=emptyState('🎯', B('No mistakes recorded yet','अझै गल्ती रेकर्ड भएको छैन'), B('Wrong answers are saved here automatically when you practise — then drill them with the Mistake Marathon on Home.','अभ्यासमा गलत भएका उत्तर स्वतः यहाँ सेभ हुन्छन् — अनि Home को Mistake Marathon बाट तिनको अभ्यास गर्नुहोस्।'), B('Start practicing','अभ्यास सुरु गर्नुहोस्'), "showView('practice')");
  const list=(arr,empty,revise)=> arr.length? arr.map(q=>`<div class="card"><strong>${esc(qText(q))}</strong><br>${B('Answer:','उत्तर:')} <strong>${String.fromCharCode(65+q.answer)}. ${esc(qOpts(q)[q.answer])}</strong> <span class="muted">— ${esc(qExpl(q))}</span><br><span class="tag">${esc(q.topic)} · ${q.id}</span> ${communityBadge(q)}<br><button class="btn secondary" onclick="discussQuestion('${esc(q.id)}')">💬 ${B('Discuss this question','यो प्रश्न छलफल गर्नुहोस्')}</button> <button class="btn secondary" onclick="openReportForm('${esc(q.id)}')">⚑ ${B('Report wrong question','गलत प्रश्न रिपोर्ट')}</button>${revise?reviseBtn(q):''}</div>`).join('') : empty;
  $('#review-box').innerHTML=`<h3>🔖 ${B('Bookmarks','बुकमार्कहरू')} (${bm.length})</h3>${list(bm,emptyBm)}<h3>❌ ${B('Mistakes to revise','दोहोर्‍याउनुपर्ने गल्तीहरू')} (${mk.length})</h3>${list(mk,emptyMk,true)}<button class="btn secondary" onclick="if(confirm('${B('Clear all bookmarks and mistakes?','सबै बुकमार्क र गल्ती मेटाउने?')}')){progress.bookmarks=[];progress.mistakes=[];saveProgress();renderReview();}">${B('Clear bookmarks &amp; mistakes','बुकमार्क र गल्तीहरू मेटाउनुहोस्')}</button>`;
}
/* ---------- Revision notes (topic one-pagers) ---------- */
// One-pagers live in data/notes/*.json (one file per topic — see
// CONTRIBUTING.md "Revision notes"). noteByTopic matches a question's q.topic
// string exactly, so "📖 Revise this topic" always lands on the right page.
function noteBySlug(s){ return NOTES.find(n=>n.slug===s); }
function noteByTopic(t){ return NOTES.find(n=>n.topic===t); }
function noteTitle(n){ return (lang==='ne' && n.title_ne) ? n.title_ne : n.title_en; }
function noteBullet(b){ return (lang==='ne' && b.ne) ? b.ne : b.en; }
function noteQuestionCount(topic){ let n=0; for(const q of QUESTIONS){ if(q.topic===topic) n++; } return n; }
let notesSlug=null; // null = notes list; otherwise the open one-pager's slug
function renderNotes(missingTopic){
  const box=$('#notes-box'); if(!box) return;
  const n=notesSlug?noteBySlug(notesSlug):null;
  if(n){
    const bullets=n.bullets.map(b=>`<li>${esc(noteBullet(b))}</li>`).join('');
    box.innerHTML=`<div class="card"><p><button class="btn secondary" onclick="openNoteList()">← ${lang==='ne'?'सबै नोटहरू':'All notes'}</button></p>
      <h3>📖 ${esc(noteTitle(n))}</h3>
      <p class="muted">${esc(n.topic)} · ${n.bullets.length} ${lang==='ne'?'बुँदा':'key points'} · ${noteQuestionCount(n.topic).toLocaleString()} ${lang==='ne'?'प्रश्न':'questions'}${n.updated?` · ${lang==='ne'?'अद्यावधिक':'updated'} ${esc(n.updated)}`:''}</p>
      <ul class="note-bullets">${bullets}</ul>
      ${n.source_note?`<p class="muted">${esc(n.source_note)}</p>`:''}
      <p><button class="btn secondary" onclick="startPracticeTopic('${esc(n.topic)}')">✏️ ${lang==='ne'?'यो विषय अभ्यास गर्नुहोस्':'Practice this topic'}</button>
      <button class="btn secondary" onclick="showView('submit')">${lang==='ne'?'नोट सुधार्नुहोस् / थप्नुहोस्':'Improve / add a note'}</button></p></div>`;
    return;
  }
  const cards=NOTES.map(x=>`<div class="card"><strong>${esc(noteTitle(x))}</strong><div class="muted">${x.bullets.length} ${lang==='ne'?'बुँदा':'key points'} · ${noteQuestionCount(x.topic).toLocaleString()} ${lang==='ne'?'प्रश्न':'questions'}</div><button class="btn secondary" onclick="openNote('${esc(x.slug)}')">📖 ${lang==='ne'?'पढ्नुहोस्':'Read'}</button></div>`).join('');
  const missHtml=missingTopic?`<div class="card" style="border-color:#ea580c"><p>📝 ${lang==='ne'?'यस विषयको नोट अहिलेसम्म छैन':'No revision note for this topic yet'}: <strong>${esc(missingTopic)}</strong>.</p><p class="muted">${lang==='ne'?'तलका विषयका नोटहरू तयार छन्। नोट लेखेर योगदान गर्न चाहनुहुन्छ? CONTRIBUTING.md → “Revision notes” हेर्नुहोस्।':'Notes for the topics below are ready. Want to write one? See CONTRIBUTING.md → “Revision notes”.'}</p></div>`:'';
  if(!dataReady){ box.innerHTML=missHtml+skelBlock(3); return; }
  if(!NOTES.length){ box.innerHTML=missHtml+errorState(B('Revision notes could not be loaded','रिभिजन नोटहरू लोड हुन सकेनन्'), B('The notes failed to load. Check your connection and try again.','नोटहरू लोड हुन असफल भए। आफ्नो इन्टरनेट कनेक्सन जाँचेर पुनः प्रयास गर्नुहोस्।')); return; }
  box.innerHTML=`${missHtml}
  <div class="card"><p class="muted">${lang==='ne'?'हरेक विषयको एक-पृष्ठीय दोहोर्‍याउने नोट — मुख्य तथ्य, सूत्र, धारा र मिति।':'One-page revision notes per topic — key facts, formulas, articles and dates.'}</p></div>
  <div class="grid">${cards}</div>`;
}
function openNote(slug){ notesSlug=slug; showView('notes'); }
function openNoteList(){ notesSlug=null; showView('notes'); }
// "📖 Revise this topic" on wrong-answer review: jump to the note for the
// question's topic, or to the notes list with a "not yet written" hint.
function reviseTopic(topic){ const n=noteByTopic(topic); if(n){ notesSlug=n.slug; showView('notes'); } else { notesSlug=null; showView('notes'); renderNotes(topic); } }

/* ---------- Audio revision mode ---------- */
// Web Speech API (speechSynthesis) narration — fully offline, zero
// dependencies. Content: Q&A (question, pause, then answer), flashcards, or
// fun facts. Pause is implemented as cancel + resume-from-part (parts are
// short), which sidesteps the Chrome speechSynthesis.pause() quirks.
const AUDIO_RATE_KEY='loksewa_audio_rate';
let audioState=null;
function audioStateInit(){
  let rate=1; try{ const r=parseFloat(localStorage.getItem(AUDIO_RATE_KEY)); if(r>=0.5&&r<=2) rate=r; }catch(e){}
  audioState={ items:[], idx:0, partIdx:0, parts:[], playing:false, paused:false, src:'qa', rate:rate, voiceLang:'en-US', pauseTimer:null };
}
function audioSupported(){ return (typeof window!=='undefined') && ('speechSynthesis' in window) && (typeof SpeechSynthesisUtterance!=='undefined'); }
function audioAnswerLine(q){ return (lang==='ne'?'उत्तर: ':'Answer: ')+String.fromCharCode(65+q.answer)+'. '+qOpts(q)[q.answer]; }
function audioQaItems(){
  return shuffle(QUESTIONS).slice(0,20).map(q=>({ title:qText(q), parts:[ qText(q), 1200, audioAnswerLine(q) ] }));
}
function audioFlashItems(){
  return shuffle(QUESTIONS).slice(0,20).map(q=>({ title:qText(q), parts:[ qText(q), 800, audioAnswerLine(q)+(qExpl(q)?'. '+qExpl(q):'') ] }));
}
function audioFactItems(){
  return shuffle(FUNFACTS).slice(0,20).map(f=>({ title:funFactText(f), parts:[ funFactText(f) ] }));
}
function audioBuildItems(){
  if(!audioState) audioStateInit();
  audioState.items = audioState.src==='flash' ? audioFlashItems() : audioState.src==='facts' ? audioFactItems() : audioQaItems();
  audioState.idx=0;
}
function audioPickVoice(){
  try{
    const vs=speechSynthesis.getVoices()||[];
    const pref=audioState.voiceLang;
    return vs.find(v=>v.lang===pref) || vs.find(v=>v.lang&&v.lang.toLowerCase().indexOf(pref.slice(0,2).toLowerCase())===0) || vs.find(v=>v.default) || vs[0] || null;
  }catch(e){ return null; }
}
function audioCancelFlight(){
  try{ speechSynthesis.cancel(); }catch(e){}
  if(audioState&&audioState.pauseTimer){ clearTimeout(audioState.pauseTimer); audioState.pauseTimer=null; }
}
function audioSpeakPart(){
  const st=audioState; if(!st||!st.playing) return;
  if(st.partIdx>=st.parts.length){
    // Item done → next item; past the last item, stop.
    st.idx++;
    if(st.idx>=st.items.length){ audioStop(); renderAudio(); return; }
    audioPlayItem(); return;
  }
  const p=st.parts[st.partIdx];
  if(typeof p==='number'){ st.partIdx++; st.pauseTimer=setTimeout(audioSpeakPart,p); renderAudioStatus(); return; }
  try{
    const u=new SpeechSynthesisUtterance(p);
    u.rate=st.rate; u.lang=st.voiceLang;
    const v=audioPickVoice(); if(v) u.voice=v;
    u.onend=()=>{ if(!audioState||!audioState.playing) return; audioState.partIdx++; audioSpeakPart(); };
    u.onerror=()=>{ if(!audioState||!audioState.playing) return; audioState.partIdx++; audioSpeakPart(); };
    speechSynthesis.speak(u);
  }catch(e){ st.partIdx++; audioSpeakPart(); return; }
  renderAudioStatus();
}
function audioPlayItem(){
  const st=audioState; if(!st) return;
  const item=st.items[st.idx]; if(!item){ audioStop(); renderAudio(); return; }
  st.parts=item.parts||[]; st.partIdx=0; st.playing=true; st.paused=false;
  audioSpeakPart(); renderAudio();
}
function audioPlay(){
  if(!audioSupported()) return;
  if(!audioState) audioStateInit();
  const st=audioState;
  if(!st.items.length) audioBuildItems();
  if(!st.items.length){ renderAudio(); return; }
  st.idx=Math.min(st.idx, st.items.length-1);
  audioCancelFlight();
  if(st.paused){ st.paused=false; st.playing=true; } // resume: re-speak the paused part (parts are short)
  else { st.parts=(st.items[st.idx].parts||[]); st.partIdx=0; st.playing=true; }
  audioSpeakPart(); renderAudio();
}
function audioPause(){
  if(!audioState||!audioState.playing){ renderAudio(); return; }
  audioCancelFlight();
  audioState.playing=false; audioState.paused=true;
  renderAudio();
}
function audioStop(){
  audioCancelFlight();
  if(audioState){ audioState.playing=false; audioState.paused=false; audioState.idx=0; audioState.partIdx=0; audioState.parts=[]; }
}
function audioNext(){
  if(!audioState||!audioState.items.length) return;
  const st=audioState; audioCancelFlight(); st.playing=false; st.paused=false;
  st.idx=Math.min(st.idx+1, st.items.length-1); audioPlayItem();
}
function audioPrev(){
  if(!audioState||!audioState.items.length) return;
  const st=audioState; audioCancelFlight(); st.playing=false; st.paused=false;
  st.idx=Math.max(0, st.idx-1); audioPlayItem();
}
function audioNewSet(){ if(!audioState) audioStateInit(); audioCancelFlight(); audioState.playing=false; audioState.paused=false; audioBuildItems(); audioPlay(); }
function audioSetSource(s){ if(!audioState) audioStateInit(); if(['qa','flash','facts'].indexOf(s)<0) return; audioCancelFlight(); audioState.playing=false; audioState.paused=false; audioState.src=s; audioBuildItems(); renderAudio(); }
function audioSetRate(v){
  if(!audioState) audioStateInit();
  const r=Math.min(2,Math.max(0.5,parseFloat(v)||1)); audioState.rate=r;
  try{ localStorage.setItem(AUDIO_RATE_KEY,String(r)); }catch(e){}
  const el=document.getElementById('audio-rate-val'); if(el) el.textContent=String(Math.round(r*100)/100)+'×';
}
function audioSetVoiceLang(l){ if(!audioState) audioStateInit(); audioState.voiceLang=(l==='ne-NP')?'ne-NP':'en-US'; renderAudio(); }
function audioStatusText(){
  const st=audioState;
  if(!st||!st.items.length) return lang==='ne'?'तयार — Play थिच्नुहोस्':'Ready — press Play';
  return (lang==='ne'?'आइटम ':'Item ')+(st.idx+1)+' / '+st.items.length+(st.playing?(lang==='ne'?' · बजिरहेको':' · playing'):(st.paused?(lang==='ne'?' · रोकिएको':' · paused'):''));
}
function renderAudioStatus(){
  const el=document.getElementById('audio-status'); if(el) el.textContent=audioStatusText();
  const t=document.getElementById('audio-now'); if(t&&audioState&&audioState.items[audioState.idx]) t.textContent=audioState.items[audioState.idx].title;
}
function renderAudio(){
  const box=$('#audio-box'); if(!box) return;
  if(!audioSupported()){
    box.innerHTML=`<div class="card"><h3>🔇 ${lang==='ne'?'अडियो उपलब्ध छैन':'Audio not available'}</h3><p>${lang==='ne'?'अडियो दोहोर्‍याउन Web Speech API (speechSynthesis) चाहिन्छ, जुन यो ब्राउजरमा छैन। Chrome, Edge वा Safari प्रयास गर्नुहोस् — नोट र प्रश्नहरू सामान्य रूपमा चल्छन्।':'Audio revision needs the Web Speech API (speechSynthesis), which this browser does not support. Try Chrome, Edge or Safari — your notes and questions still work fine.'}</p><p><button class="btn secondary" onclick="showView('notes')">📖 ${lang==='ne'?'नोटहरू पढ्नुहोस्':'Read the notes instead'}</button></p></div>`;
    return;
  }
  if(!audioState) audioStateInit();
  const st=audioState;
  if(!st.items.length) audioBuildItems();
  const cur=st.items[st.idx];
  const srcOpts=[['qa',lang==='ne'?'प्रश्नोत्तर (प्रश्न → उत्तर)':'Q&A (question → pause → answer)'],['flash',lang==='ne'?'फ्ल्यासकार्ड':'Flashcards'],['facts',lang==='ne'?'रोचक तथ्य':'Fun facts']].map(([v,l])=>`<option value="${v}"${st.src===v?' selected':''}>${l}</option>`).join('');
  box.innerHTML=`<div class="card"><h3>🔊 ${lang==='ne'?'अडियो दोहोर्‍याइ':'Audio revision'}</h3>
  <p class="muted">${lang==='ne'?'फोन/ब्राउजरकै आवाजमा सुनिन्छ — इन्टरनेट चाहिँदैन। Play थिचेपछि पढ्न थाल्छ।':'Narrated with your device’s own voices — no internet needed. Press Play to start.'}</p>
  <label for="audio-src">${lang==='ne'?'सामग्री':'Content'}</label>
  <select id="audio-src" onchange="audioSetSource(this.value)">${srcOpts}</select>
  <div class="audio-controls">
    <button class="btn" onclick="audioPlay()">▶ ${lang==='ne'?'बजाउनुहोस्':'Play'}</button>
    <button class="btn secondary" onclick="audioPause()">⏸ ${lang==='ne'?'रोक्नुहोस्':'Pause'}</button>
    <button class="btn secondary" onclick="audioStop();renderAudio()">⏹ ${lang==='ne'?'बन्द':'Stop'}</button>
    <button class="btn secondary" onclick="audioPrev()">⏮ ${lang==='ne'?'अघिल्लो':'Prev'}</button>
    <button class="btn secondary" onclick="audioNext()">⏭ ${lang==='ne'?'अर्को':'Next'}</button>
    <button class="btn secondary" onclick="audioNewSet()">🔀 ${lang==='ne'?'नयाँ सेट':'New set'}</button>
  </div>
  <label for="audio-rate">${lang==='ne'?'गति':'Speed'} — <span id="audio-rate-val">${Math.round(st.rate*100)/100}×</span></label>
  <input type="range" id="audio-rate" min="0.5" max="2" step="0.25" value="${st.rate}" oninput="audioSetRate(this.value)">
  <label for="audio-voice">${lang==='ne'?'आवाजको भाषा':'Voice language'}</label>
  <select id="audio-voice" onchange="audioSetVoiceLang(this.value)">
    <option value="en-US"${st.voiceLang==='en-US'?' selected':''}>English (en-US)</option>
    <option value="ne-NP"${st.voiceLang==='ne-NP'?' selected':''}>नेपाली (ne-NP)</option>
  </select>
  <p class="muted">${lang==='ne'?'टिप: ne-NP आवाज धेरै डिभाइसमा हुँदैन — नभए अङ्ग्रेजी आवाजले पढ्छ।':'Tip: few devices ship an ne-NP voice — without one, the English voice reads the text.'}</p>
  <div class="card"><div class="muted" id="audio-status">${esc(audioStatusText())}</div><p class="audio-now" id="audio-now">${cur?esc(cur.title):''}</p></div>
  </div>`;
}

function renderDashboard(){
  const a=progress.attempts; const totalQ=a.reduce((s,x)=>s+x.total,0);
  const avg=a.length? (a.reduce((s,x)=>s+x.pct,0)/a.length).toFixed(1):'—';
  const passes=a.filter(x=>x.passed).length;
  const rec=personalRecords(progress);
  const recordsHtml=`<div class="card"><h3>🏆 Personal Records — just for you</h3>
    <p><strong>Longest streak:</strong> ${rec.longestStreak} day(s) · <strong>Total XP:</strong> ${rec.totalXp} · <strong>Total questions answered:</strong> ${rec.totalQuestions}</p>
    <p><strong>Best day:</strong> ${rec.bestDay? esc(rec.bestDay.date)+' — '+rec.bestDay.total+' questions' : 'No attempts yet — finish a practice set and your best day will show up here.'}</p>
    <p><strong>Best mock score per exam:</strong> ${rec.bestMocks.length? rec.bestMocks.map(b=>esc(b.examName)+' '+b.pct+'% ('+b.score+'/'+b.max+', '+b.date+')').join(' · ') : 'No mock attempts yet — your first mock score per exam becomes the record to beat.'}</p>
    <p><strong>Best Speed Round:</strong> ${rec.speedBest? rec.speedBest.score+'/'+rec.speedBest.max+' ('+rec.speedBest.pct+'%) on '+rec.speedBest.date : 'No Speed Round yet — try the 60-second round from Home.'}</p>
    <p class="muted">Personal only — no leaderboard, nothing leaves this device.</p></div>`;
  $('#dash-stats').innerHTML=`<div class="grid">
    <div class="card"><div class="stat">${progress.xp}</div>XP · Level ${progress.level}</div>
    <div class="card"><div class="stat">🔥 ${progress.streak}</div>day streak</div>
    <div class="card"><div class="stat">${a.length}</div>sessions · ${totalQ} questions</div>
    <div class="card"><div class="stat">${avg}%</div>average score · ${passes} passes</div></div>
    <div class="card"><strong>Badges:</strong> ${badges().length? badges().map(b=>`<span class="badge">${esc(b)}</span>`).join(''):B('No badges yet — finish your first practice set to earn one.','अझै ब्याज छैन — एउटा कमाउन पहिलो अभ्यास सेट पूरा गर्नुहोस्।')}</div>
    ${recordsHtml}
    <div class="card"><strong>Level ${progress.level} progress</strong><div class="muted">${progress.xp % 500} / 500 XP to Level ${progress.level + 1}</div><div class="progress-bar level-bar"><div style="width:${(progress.xp % 500) / 5}%"></div></div></div>
    <div class="card"><h3>${B('Recent attempts','हालका प्रयासहरू')}</h3>${a.length? [...a].reverse().slice(0,10).map(x=>`<div>${new Date(x.date).toLocaleDateString()} · ${esc(x.mode)} · ${esc(examById(x.exam)?.name||x.exam||'Mixed practice')} — <strong>${x.score}/${x.max}</strong> (${x.pct}%) ${x.passed?'✅ PASS':'❌ FAIL'} · ${x.correct}✓ ${x.wrong}✗ ${x.skipped}–</div>`).join(''):emptyState('📝', B('No attempts yet','अझै प्रयास छैन'), B('Your practice and mock sessions will appear here with scores and pass/fail.','तपाईंका अभ्यास र मक सत्रहरू स्कोर र पास/फेलसहित यहाँ देखिनेछन्।'), B('Start practicing','अभ्यास सुरु गर्नुहोस्'), "showView('practice')")}</div>
    <div class="card"><h3>${B('Score history','स्कोर इतिहास')}</h3><canvas id="chart" width="800" height="220"></canvas>${a.length?'':'<p style="margin-top:10px"><button class="btn" onclick="showView(\'practice\')">'+B('Start practicing','अभ्यास सुरु गर्नुहोस्')+'</button></p>'}</div>
    <div class="card" id="weekly-box-dash"></div>
    <div class="card" id="focus-timer-box-dash"></div>
    <button class="btn secondary" onclick="if(confirm('Reset ALL progress (XP, streak, history) AND sign out of the local profile? This cannot be undone.')){resetProgress();}">Reset progress</button>`;
  drawChart(); renderWeekly(); renderFocusTimer();
  const lb=document.querySelector('#dash-stats .level-bar>div');
  if(lb) animateWidth(lb, 0, (progress.xp % 500) / 5);
}
// Reset ALL progress — and really all of it. The device user_id is kept
// (so a fresh profile after reset is still the same device) and the
// name/email are cleared deliberately: the confirm text says this signs the
// local profile out. Two progress stores used to survive a reset because
// they live in their own localStorage keys, not on the progress object:
// the Best Speed Round (loksewa_speed_best_v1) and the Fact streak
// (loksewa_fact_streak_v1). Both are removed here now.
function resetProgress(){
  progress={user_id:progress.user_id,email:'',name:'',xp:0,level:1,streak:0,lastDay:'',attempts:[],bookmarks:[],mistakes:[],flashcardsSeen:0,dailyDone:{},qotdDone:{},weeklyTarget:70,weeklyGoalsMet:0,weeklyGoalMetWeek:'',funFactsSeen:[],focusSessions:0,focusMinutes:0};
  try{ localStorage.removeItem(SPEED_BEST_KEY); localStorage.removeItem(FACT_STREAK_KEY); }catch(e){}
  saveProgress(); updateDemoBanner(); renderDashboard();
}
function drawChart(){
  const c=document.getElementById('chart'); if(!c) return; const ctx=c.getContext('2d');
  const data=[...progress.attempts].slice(-20); ctx.clearRect(0,0,c.width,c.height);
  ctx.strokeStyle='#94a3b8'; ctx.beginPath(); ctx.moveTo(30,10); ctx.lineTo(30,190); ctx.lineTo(790,190); ctx.stroke();
  if(!data.length){ ctx.fillStyle='#94a3b8'; ctx.fillText('No data yet — finish a practice session and your score history appears here.', 40, 100); return; }
  data.forEach((x,i)=>{ const px=40+i*(740/Math.max(1,data.length-1||1)); const h=(x.pct/100)*160; ctx.fillStyle=x.passed?'#22c55e':'#ef4444'; ctx.fillRect(px-6, 190-h, 12, h); });
}
function searchHay(q){
  // Lazily cached lowercase haystack: rebuilding it for all 59,076
  // questions on every search cost ~160 ms per click. Cached on the
  // question object (never serialised — the bank is only read, never saved).
  if(!q._hay) q._hay=(q.question+' '+q.options.join(' ')+' '+(q.subtopic||'')+' '+(q.question_ne||'')+' '+((q.options_ne||[]).join(' '))+' '+(q.explanation||'')+' '+(q.explanation_ne||'')).toLowerCase();
  return q._hay;
}
function doSearch(){
  const rawTerm=(document.getElementById('search-input').value||'').trim();
  const term=rawTerm.toLowerCase();
  const topic=document.getElementById('search-topic').value;
  const all=QUESTIONS.filter(q=> (!topic||q.topic===topic) && (!term || searchHay(q).includes(term))); const res=all.slice(0,50);
  const noMatch=emptyState('🔎', B('No matches','कुनै मिल्दो भेटिएन'), B('Nothing in the question bank matched &ldquo;'+esc(rawTerm||topic)+'&rdquo;. Try fewer words, a different spelling, or browse by topic.','प्रश्न बैंकमा &ldquo;'+esc(rawTerm||topic)+'&rdquo; सँग मिल्ने केही भेटिएन। कम शब्द, फरक हिज्जे प्रयास गर्नुहोस् वा विषयअनुसार हेर्नुहोस्।'), B('Clear search','खोज मेटाउनुहोस्'), "document.getElementById('search-input').value='';doSearch()");
  $('#search-results').innerHTML=`<p class="muted">${B(all.length+' match(es) — showing '+res.length+'.', all.length+' वटा मिल्दो — '+res.length+' वटा देखाइँदै।')}</p>`+(res.length?res.map(q=>`<div class="card"><strong>${esc(qText(q))}</strong><br>${qOpts(q).map((o,i)=>`${String.fromCharCode(65+i)}. ${esc(o)}`).join(' &nbsp; ')}<br>${B('Answer:','उत्तर:')} <strong>${String.fromCharCode(65+q.answer)}</strong> <span class="muted">— ${esc(qExpl(q))}</span><br><span class="tag">${esc(q.topic)} · ${esc(q.difficulty)} · ${q.exam.join(', ')} · ${q.id}</span> ${communityBadge(q)}<br><button class="btn secondary" onclick="discussQuestion('${esc(q.id)}')">💬 ${B('Discuss this question','यो प्रश्न छलफल गर्नुहोस्')}</button> <button class="btn secondary" onclick="openReportForm('${esc(q.id)}')">⚑ ${B('Report wrong question','गलत प्रश्न रिपोर्ट')}</button></div>`).join(''):noMatch);
}
function filterGuide(term){
  const t=(term||'').toLowerCase();
  document.querySelectorAll('#guide-box .card').forEach(c=>{ c.style.display = (!t || c.textContent.toLowerCase().includes(t)) ? '' : 'none'; });
}
function showGuideFor(id){ showView('guide'); const el=document.getElementById('guide-'+id); if(el) el.scrollIntoView(); }
function renderGuide(){
  const box=$('#guide-box'); if(!box) return;
  if(!dataReady){ box.innerHTML=skelBlock(2); return; }
  if(!EXAMS.length){ box.innerHTML=errorState(B('Exam guide could not be loaded','परीक्षा गाइड लोड हुन सकेन'), B('The exam list failed to load. Check your connection and try again — the guide needs the exam data to render.','परीक्षा सूची लोड हुन असफल भयो। आफ्नो इन्टरनेट कनेक्सन जाँचेर पुनः प्रयास गर्नुहोस्।')); return; }
  const filterHtml=`<p><label for="guide-filter">${B('Find an exam','परीक्षा खोज्नुहोस्')}</label><input type="search" id="guide-filter" placeholder="${B('e.g. Kharidar, Nursing, Bar…','जस्तै: खरिदार, नर्सिङ, बार…')}" oninput="filterGuide(this.value)"></p>`;
  box.innerHTML=filterHtml+EXAMS.map(e=>{
    // Guide-only exams (prelim: null) have no MCQ paper: show the pattern as
    // "no mock" text instead of a prelim row, and no Start-mock button.
    // Negative marking is per-exam now: null = unverified, 0 = none, else 20%.
    const negTxt=p=>p.negative===null?'negative marking unverified':(p.negative===0?'no negative marking':Math.round(mockNegRate(p)*100)+'% negative marking');
    const prelimRow=e.prelim
      ? `<tr><td>Prelim / General</td><td>${e.prelim.questions} MCQ × ${e.prelim.marksPerQ} = ${e.prelim.total} marks, ${e.prelim.timeMin==null?'time not verified':e.prelim.timeMin+' min'}, pass ${e.prelim.pass}, ${negTxt(e.prelim)}. ${esc(e.prelim.breakdown)}</td></tr>`
      : `<tr><td>Prelim / General</td><td><strong>Guide only — no MCQ prelim.</strong> This exam has no verified MCQ prelim paper, so there is no mock for it. ${esc(e.main)}</td></tr>`;
    return `<div class="card" id="guide-${e.id}"><h3>${esc(e.name)} <span class="muted">(${esc(e.name_ne||'')})</span></h3>
    <p><strong>${esc(e.level)}</strong> · ${esc(e.body)} · Education: ${esc(e.education)} · Age: ${esc(e.age)}</p>
    <div class="table-wrap"><table><tr><th>Stage</th><th>Pattern</th></tr>
    ${prelimRow}
    <tr><td>Main / Written</td><td>${esc(e.main)}</td></tr>
    <tr><td>Final</td><td>${esc(e.final)}</td></tr></table></div>
    <p style="margin-top:8px"><strong>Syllabus:</strong> ${e.syllabus.map(esc).join(' · ')}</p>
    ${e.note?`<p class="muted">⚠️ ${esc(e.note)}</p>`:''}
    ${e.prelim?`<button class="btn" onclick="startMockFor('${e.id}')">Start ${esc(e.name)} mock</button>`:`<p class="muted">No mock available for this exam — guide only.</p>`}</div>`;
  }).join('');
}
/* ---------- Old Papers ---------- */
function paperExamName(p){ const e=examById(p.exam); return e ? e.name : p.exam; }
function renderPapers(){
  const box=$('#papers-box'); if(!box) return;
  if(!dataReady){ box.innerHTML=skelBlock(2); return; }
  if(!PAPERS.length){ box.innerHTML=errorState(B('Old papers could not be loaded','पुराना प्रश्नपत्र लोड हुन सकेनन्'), B('The papers list failed to load. Check your connection and try again.','प्रश्नपत्र सूची लोड हुन असफल भयो। आफ्नो इन्टरनेट कनेक्सन जाँचेर पुनः प्रयास गर्नुहोस्।')); return; }
  const sel=document.getElementById('papers-filter');
  if(sel){
    const exams=[...new Set(PAPERS.map(p=>p.exam))];
    const cur=sel.value;
    sel.innerHTML='<option value="">All exams</option>'+exams.map(id=>`<option value="${esc(id)}">${esc(examById(id)?.name||id)}</option>`).join('');
    if(exams.includes(cur)) sel.value=cur;
  }
  const f=sel ? sel.value : '';
  const list=PAPERS.filter(p=>!f||p.exam===f);
  const noMatchHtml=emptyState('🔎', B('No papers match this filter','यो फिल्टरसँग मिल्ने प्रश्नपत्र छैन'), B('Try a different exam, or clear the filter to see every paper.','अर्को परीक्षा प्रयास गर्नुहोस् वा सबै प्रश्नपत्र हेर्न फिल्टर हटाउनुहोस्।'), B('Clear filter','फिल्टर हटाउनुहोस्'), "document.getElementById('papers-filter').value='';renderPapers()");
  const groups={}; list.forEach(p=>{ (groups[p.exam]=groups[p.exam]||[]).push(p); });
  box.innerHTML=Object.entries(groups).map(([exam, ps])=>`<h3>${esc(examById(exam)?.name||exam)}</h3>`+ps.map(p=>{
    const meta=[p.date_bs?('📅 '+esc(p.date_bs)+(p.date_ad?' ('+esc(p.date_ad)+')':'')):null,
      p.questions?(p.questions+' MCQs'):null,
      p.marks!=null?(p.marks+' marks'):null,
      p.time_min!=null?(p.time_min+' min'):null,
      p.pass!=null?('pass '+p.pass):null].filter(Boolean).join(' · ');
    const viewerSrc=p.pdf_url||null;
    return `<div class="card"><h3>${esc(p.title)}${p.title_ne?` <span class="muted">(${esc(p.title_ne)})</span>`:''}</h3>
    <p class="muted">${esc(meta)||'Details on the source page'}</p>
    <p>${p.transcribed?'<span class="tag">✓ Transcribed — practice available</span>':'<span class="tag">📄 Scanned paper — read the original, not transcribed</span>'}</p>
    ${p.notes?`<p>${esc(p.notes)}</p>`:''}
    <p class="muted">Source: <a href="${esc(p.source_url)}" target="_blank" rel="noopener">${esc(p.source_name)}</a></p>
    <a class="btn" href="${esc(p.source_url)}" target="_blank" rel="noopener">Open Original ↗</a>
    ${p.pdf_url?`<button class="btn secondary" onclick="togglePaperView(this)">View Scanned</button>`:''}
    ${p.transcribed?`<button class="btn" onclick="practicePaper('${esc(p.id)}')">Practice these questions →</button>`:''}
    ${viewerSrc?`<div class="paper-viewer" hidden style="margin-top:12px"><iframe src="${esc(viewerSrc)}" style="width:100%;height:70vh;border:1px solid #444" title="Scanned paper: ${esc(p.title)}"></iframe>
    <p class="muted">If the preview does not load, the source blocks embedding — <a href="${esc(p.source_url)}" target="_blank" rel="noopener">open the original — scanned paper</a>.</p></div>`:`<p class="muted">Scanned paper — no embeddable PDF was verified for this one. Read it on the source site via "Open Original ↗" above.</p>`}
    </div>`;
  }).join('')).join('') || noMatchHtml;
}
function togglePaperView(btn){
  const card=btn.closest ? btn.closest('.card') : null;
  const v=card ? card.querySelector('.paper-viewer') : null;
  if(!v) return;
  v.hidden=!v.hidden;
  btn.textContent=v.hidden?'View Scanned':'Hide Scanned';
}
function practicePaper(id){
  const p=PAPERS.find(x=>x.id===id);
  if(!p){ alert(B('Paper not found.','प्रश्नपत्र भेटिएन।')); return; }
  // Transcribed questions carry the paper name + date in their source field
  // (e.g. "Previous Year — NaSu First Paper 2083-01-20"), not the paper id.
  // Match on the paper-name keyword + date: Kharidar First and Koshi share
  // the date 2083-01-26, so the keyword is what tells them apart.
  const key = p.id.includes('koshi') ? 'Koshi'
    : p.id.includes('nasu') ? 'NaSu'
    : p.id.includes('kharidar-first') ? 'Kharidar First'
    : p.id.includes('kharidar-pretest') ? 'Pretest' : null;
  // The date check is vacuous when the paper has no date_bs (''.includes('')
  // is always true), so an undated paper whose id contains a keyword (e.g.
  // 'nasu') would wrongly match another paper's transcribed questions.
  // Without a date the match cannot be trusted — treat it as not transcribed.
  if(!key || !p.date_bs){ alert(B('This paper has not been transcribed yet — use View Scanned to read the original.','यो प्रश्नपत्र अझै लिपिबद्ध गरिएको छैन — मूल पढ्न View Scanned प्रयोग गर्नुहोस्।')); return; }
  const pool=QUESTIONS.filter(q=>(q.source||'').includes(key) && (q.source||'').includes(p.date_bs));
  if(!pool.length){ alert(B('This paper has not been transcribed yet — use View Scanned to read the original.','यो प्रश्नपत्र अझै लिपिबद्ध गरिएको छैन — मूल पढ्न View Scanned प्रयोग गर्नुहोस्।')); return; }
  const qs=shuffle(pool).map(q=>shuffleOptions(q));
  current={ mode:'practice', exam:p.exam, questions:qs, answers:Array(qs.length).fill(null), idx:0, negOn:true, negRate:0.2, timerOn:false, startTime:Date.now(), perQ:[] };
  showView('quiz'); renderQuestion();
}

/* ---------- Notices ---------- */
const NOTICE_STATUS_LABEL={open:'Open', 'closing-soon':'Closing soon', closed:'Closed', unverified:'Unverified'};
// Effective status at render time: an open/closing-soon notice whose
// close_date has passed is shown Closed even though notices.json still
// carries its old status — the JSON is a snapshot, the date is the truth.
// today defaults to the real today; tests pass an explicit date.
function effectiveNoticeStatus(n, today){
  const t=today||new Date().toISOString().slice(0,10);
  return (n.close_date && n.close_date < t && (n.status==='open'||n.status==='closing-soon')) ? 'closed' : n.status;
}
function renderNotices(){
  const box=$('#notices-box'); if(!box) return;
  // Official "where to check" links are rendered here from a data array (not
  // static HTML, and never as a literal external-href string) so the page —
  // and the single-file bundle — stays free of external hrefs in its markup.
  const ol=document.getElementById('official-links');
  if(ol){
    const OFFICIAL=[
      ['Public Service Commission', 'https://psc.gov.np/', 'psc.gov.np'],
      ['PSC online applications', 'https://psconline1.psc.gov.np/', 'psconline1.psc.gov.np'],
      ['Teacher Service Commission', 'https://tsc.gov.np/', 'tsc.gov.np'],
      ['TSC online applications', 'https://online.tsc.gov.np/', 'online.tsc.gov.np'],
      ['Nepal Rastra Bank', 'https://www.nrb.org.np/', 'nrb.org.np'],
      ['Gandaki Province PSC', 'https://onlineppsc.gandaki.gov.np/', 'onlineppsc.gandaki.gov.np'],
      ['Lumbini Province PSC', 'https://ppsconline.lumbini.gov.np/', 'ppsconline.lumbini.gov.np'],
    ];
    const link=([label, url, text])=>`<a href="${esc(url)}" target="_blank" rel="noopener">${esc(text)}</a>`;
    ol.innerHTML='<h3>Where to check — official sites</h3>'
      + '<p class="muted">If a notice here is unverified or its deadline has passed, check the official source directly:</p><ul>'
      + OFFICIAL.map(([label, url, text])=>`<li>${esc(label)} — ${link([label, url, text])}</li>`).join('')
      + '</ul>';
  }
  const sc=document.getElementById('notices-scope'), bd=document.getElementById('notices-body'), st=document.getElementById('notices-status');
  if(!dataReady){ box.innerHTML=skelBlock(2); return; }
  if(bd){
    const bodies=[...new Set(NOTICES.map(n=>n.issuer).filter(Boolean))].sort();
    const cur=bd.value;
    bd.innerHTML='<option value="">All bodies</option>'+bodies.map(b=>`<option>${esc(b)}</option>`).join('');
    if(bodies.includes(cur)) bd.value=cur;
  }
  const fScope=sc?sc.value:'', fBody=bd?bd.value:'', fStatus=st?st.value:'';
  const today=new Date().toISOString().slice(0,10);
  const effStatus=n=>effectiveNoticeStatus(n, today);
  let list=NOTICES.filter(n=>(!fScope||n.scope===fScope)&&(!fBody||n.issuer===fBody)&&(!fStatus||effStatus(n)===fStatus));
  // Deadline order; notices without a verified deadline go last.
  list=list.slice().sort((a,b)=>{
    if(!a.close_date&&!b.close_date) return 0;
    if(!a.close_date) return 1; if(!b.close_date) return -1;
    return a.close_date<b.close_date?-1:(a.close_date>b.close_date?1:0);
  });
  const counts={open:0,'closing-soon':0,closed:0,unverified:0};
  NOTICES.forEach(n=>{ const s=effStatus(n); if(counts[s]!=null) counts[s]++; });
  // "Last checked" is the newest checked_date in the data, not a hardcoded
  // string — the old hardcoded 2026-10-26 kept showing after re-checks.
  const lastChecked=NOTICES.reduce((m,n)=>n.checked_date&&n.checked_date>m?n.checked_date:m,'');
  const head=`<p class="muted">${NOTICES.length} notice(s) — ${counts.open} open · ${counts['closing-soon']} closing soon · ${counts.closed} closed · ${counts.unverified} unverified. Last checked ${lastChecked||'—'}. Deadlines and post counts are only shown when a source reported them — never guessed.</p>`;
  if(!NOTICES.length){ box.innerHTML=head+errorState(B('Notices could not be loaded','सूचनाहरू लोड हुन सकेनन्'), B('The notices list failed to load. Check your connection and try again — or check the official sites listed below directly.','सूचना सूची लोड हुन असफल भयो। आफ्नो इन्टरनेट कनेक्सन जाँचेर पुनः प्रयास गर्नुहोस् — वा तलका आधिकारिक साइटहरूमा सिधै हेर्नुहोस्।')); return; }
  const noMatchHtml=emptyState('🔎', B('No notices match these filters','यी फिल्टरसँग मिल्ने सूचना छैन'), B('Try widening the filters — or clear them to see every notice.','फिल्टर फराकिलो बनाउनुहोस् — वा सबै सूचना हेर्न फिल्टर हटाउनुहोस्।'), B('Clear filters','फिल्टर हटाउनुहोस्'), 'clearNoticeFilters()');
  box.innerHTML=head+(list.length?list.map(n=>{
    const unverified=n.status==='unverified';
    const dates=[n.open_date?('Opens '+esc(n.open_date)):null, n.close_date?('Closes '+esc(n.close_date)):null].filter(Boolean).join(' · ')||'Dates not verified';
    return `<div class="card"><h3>${esc(n.title)}${n.title_ne?` <span class="muted">(${esc(n.title_ne)})</span>`:''}</h3>
    <p><span class="tag">${esc(NOTICE_STATUS_LABEL[effStatus(n)]||effStatus(n))}</span> <span class="tag">${esc(n.scope==='province'?'Province: '+n.province:'Nationwide')}</span> <span class="tag">${esc(n.issuer||'')}</span></p>
    <p>${esc(n.body||'')}</p>
    <p><strong>Posts:</strong> ${n.posts!=null?n.posts:'Not verified'} · <strong>Level:</strong> ${esc(n.level||'—')}</p>
    <p><strong>${esc(dates)}</strong></p>
    <p><strong>Fee:</strong> ${n.fee?esc(n.fee):'Not verified'}</p>
    ${unverified?'<p><strong>⚠️ Check official site — dates not verified (last checked '+esc(n.checked_date||'—')+').</strong></p>':''}
    <p class="muted">Source: <a href="${esc(n.source_url)}" target="_blank" rel="noopener">${esc(n.source_name)}</a> · Checked ${esc(n.checked_date)}</p>
    ${n.apply_url?`<a class="btn" href="${esc(n.apply_url)}" target="_blank" rel="noopener">Apply (official) ↗</a>`:'<p class="muted">No official apply link verified — see the source notice for how to apply.</p>'}
    </div>`;
  }).join(''):noMatchHtml);
}
function clearNoticeFilters(){
  const sc=document.getElementById('notices-scope'), bd=document.getElementById('notices-body'), st=document.getElementById('notices-status');
  if(sc) sc.value=''; if(bd) bd.value=''; if(st) st.value='';
  renderNotices();
}
function startMockFor(id){ const s=document.getElementById('mock-exam'); if(s) s.value=id; showView('mock'); startMock(); }

/* ================================================================
   v2 — Sign-in (demo), Discussion Hub, question submissions,
   moderation, report-wrong-question. All demo-mode storage is
   localStorage; the real backend is Supabase (docs/BACKEND.md).
   Nothing here sends data anywhere. First line of defence only:
   server-side review is the real gate.
   ================================================================ */

// ---- Config / demo mode ----
let CONFIG = null;
async function loadConfig(){
  // config.js is gitignored and created by the user from config.example.js.
  // Loaded with fetch (not a <script> tag) so its absence is silent in demo
  // mode instead of a console 404. The file only sets window.LOKSEWA_CONFIG.
  try{
    const r = await fetch('config.js');
    if (!r.ok) return;
    const t = await r.text();
    new Function(t)();
    if (typeof window !== 'undefined' && window.LOKSEWA_CONFIG) CONFIG = window.LOKSEWA_CONFIG;
  }catch(e){ /* demo mode — no config, no backend */ }
}
function isDemoMode(){ return !(CONFIG && CONFIG.SUPABASE_URL && CONFIG.SUPABASE_ANON_KEY); }
function updateDemoBanner(){
  const nb = document.getElementById('nav-auth-btn');
  if (nb) nb.textContent = (progress.name ? '👤 ' + progress.name.split(' ')[0] : 'Sign In');
}

// ---- Shared localStorage helpers ----
const LS_DISCUSS = 'loksewa_discussions_v1';
const LS_SUBMISSIONS = 'loksewa_submissions_v1';
const LS_APPROVED = 'loksewa_community_approved_v1';
const LS_REPORTS = 'loksewa_reports_v1';
const LS_MODLOG = 'loksewa_moderation_log_v1';
function lsGet(key, fallback){ try{ const v = JSON.parse(localStorage.getItem(key) || 'null'); return v == null ? fallback : v; }catch(e){ return fallback; } }
function lsSet(key, val){ try{ localStorage.setItem(key, JSON.stringify(val)); }catch(e){} }
function uid(prefix){ return prefix + '-' + Date.now().toString(36) + Math.floor(Math.random() * 1e6).toString(36); }
function nowIso(){ return new Date().toISOString(); }
function communityBadge(q){ return (q && q._community) ? '<span class="badge">Community</span>' : ''; }

/* ---------- Sign-in / Profile (demo mode) ---------- */
function isGmailAddress(email){ return /^[a-zA-Z0-9._%+-]+@gmail\.com$/i.test(String(email || '').trim()); }
function currentUserName(){ return progress.name || 'Guest'; }
function signInDemo(){
  const name = (document.getElementById('auth-name').value || '').trim();
  const email = (document.getElementById('auth-email').value || '').trim();
  const err = document.getElementById('auth-error');
  if (!name) { if (err) err.textContent = B('Please enter a display name.','कृपया देखिने नाम लेख्नुहोस्।'); return; }
  if (!isGmailAddress(email)) { if (err) err.textContent = B('Please enter a valid Gmail address (…@gmail.com). Only Gmail is accepted for sign-in.','कृपया मान्य Gmail ठेगाना लेख्नुहोस् (…@gmail.com)। साइन-इनका लागि Gmail मात्र स्वीकार गरिन्छ।'); return; }
  progress.name = name; progress.email = email.toLowerCase();
  if (!progress.user_id || progress.user_id.indexOf('local-') !== 0) progress.user_id = newLocalUserId();
  saveProgress();
  if (err) err.textContent = '';
  document.getElementById('auth-form').hidden = true;
  const ok = document.getElementById('auth-success');
  if (ok) { ok.hidden = false; ok.textContent = B('Signed in (local preview) as ','स्थानीय पूर्वावलोकनमा साइन इन: ') + name + ' — ' + progress.email + '. ' + B('Your profile is stored on this device only.','तपाईंको प्रोफाइल यो डिभाइसमा मात्र सेभ छ।'); }
  updateDemoBanner(); renderAuth();
}
function signOut(){
  progress.name = ''; progress.email = '';
  saveProgress(); updateDemoBanner(); renderAuth(); renderProfile();
}
function showAuthForm(){
  const f = document.getElementById('auth-form'); if (f) f.hidden = false;
  const ok = document.getElementById('auth-success'); if (ok) ok.hidden = true;
}
function renderAuth(){
  const box = document.getElementById('auth-box'); if (!box) return;
  updateDemoBanner();
  const signedIn = !!progress.name;
  box.innerHTML = `
    <p class="muted">Sign in keeps your XP, streak and bookmarks tied to a profile — and lets you post in the Discussion Hub and submit questions under your name.</p>
    ${signedIn ? `<div class="card"><p><strong>Signed in (local preview) as ${esc(progress.name)}</strong><br><span class="muted">${esc(progress.email)} · user_id ${esc(progress.user_id)}</span></p>
      <button class="btn secondary" onclick="showView('profile')">View profile</button>
      <button class="btn danger" onclick="signOut()">Sign out</button></div>`
    : `<div class="card"><button class="google-btn" onclick="showAuthForm()"><span class="g-logo">G</span> Sign in with Google / Gmail</button>
      <p class="muted" style="margin-top:10px">This is a local-preview sign-in: no Google account is contacted. Enter a display name and a Gmail address to create a profile on this device. Real Google sign-in arrives with Supabase — see <a href="docs/BACKEND.md">docs/BACKEND.md</a>.</p></div>`}
    <div class="card" id="auth-form" hidden>
      <h3>Sign in (local preview)</h3>
      <label for="auth-name">Display name</label><input type="text" id="auth-name" placeholder="e.g. Ravi Yadav" maxlength="60">
      <label for="auth-email">Gmail address</label><input type="text" id="auth-email" placeholder="you@gmail.com" maxlength="120" autocomplete="email">
      <p class="error-text" id="auth-error"></p>
      <button class="btn" onclick="signInDemo()">Create local profile</button>
      <p class="muted">Your progress is saved on this device in local preview — it will sync to your account once Supabase is connected.</p>
    </div>
    <div class="card" id="auth-success" hidden></div>`;
}
function weakTopics(){
  const counts = {};
  const byIdMap=questionByIdMap();
  progress.mistakes.forEach(id => { const q = byIdMap.get(id); if (q) counts[q.topic] = (counts[q.topic] || 0) + 1; });
  return Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 3);
}
function renderProfile(){
  const box = document.getElementById('profile-box'); if (!box) return;
  const a = progress.attempts;
  const totQ = a.reduce((s, x) => s + (x.total || 0), 0);
  const totC = a.reduce((s, x) => s + (x.correct || 0), 0);
  const acc = totQ ? (totC / totQ * 100).toFixed(1) : '—';
  const weak = weakTopics();
  box.innerHTML = `
    <div class="card"><h3>${esc(progress.name || B('Guest (not signed in)','अतिथि (साइन इन भएको छैन)'))}</h3>
    <p class="muted">${progress.email ? esc(progress.email) : B('No profile yet','अझै प्रोफाइल छैन')+' — <a href="#" onclick="showView(\'auth\');return false">'+B('sign in (local preview)','साइन इन (स्थानीय पूर्वावलोकन)')+'</a> '+B('to attach your progress to a name.','तपाईंको प्रगति नामसँग जोड्न।')}<br>user_id: ${esc(progress.user_id || '—')}</p>
    <p class="muted"><strong>${B('Local preview — profile stored on this device only.','स्थानीय पूर्वावलोकन — प्रोफाइल यो डिभाइसमा मात्र सेभ छ।')}</strong> ${B('Connect Supabase to enable real Google sign-in (see docs/BACKEND.md).','वास्तविक Google साइन-इनका लागि Supabase जोड्नुहोस् (docs/BACKEND.md हेर्नुहोस्)।')}</p></div>
    ${(typeof birthdayEditorHtml === 'function') ? birthdayEditorHtml() : ''}
    <div class="grid">
      <div class="card"><div class="stat">${progress.xp}</div>XP · ${B('Level','लेभल')} ${progress.level}</div>
      <div class="card"><div class="stat">🔥 ${progress.streak}</div>${B('day streak','दिनको स्ट्रिक')}</div>
      <div class="card"><div class="stat">${a.length}</div>${B('sessions','सत्र')} · ${totQ} ${B('questions','प्रश्नहरू')}</div>
      <div class="card"><div class="stat">${acc}%</div>${B('accuracy','शुद्धता')} (${totC}/${totQ} ${B('correct','सही')})</div>
    </div>
    <div class="card"><h3>${B('Weak topics (from your mistakes)','कमजोर विषयहरू (तपाईंका गल्तीबाट)')}</h3><p>${weak.length ? weak.map(([t, n]) => esc(t) + ' (' + n + ' ' + B(n > 1 ? 'mistakes' : 'mistake', 'गल्ती') + ')').join(' · ') : B('No mistakes recorded yet — answer a practice set and your weak topics will show up here.','अझै गल्ती रेकर्ड भएको छैन — अभ्यास सेट दिनुहोस् अनि तपाईंका कमजोर विषय यहाँ देखिनेछन्।')}</p></div>
    <div class="card"><h3>${B('Bookmarks &amp; mistakes','बुकमार्क र गल्तीहरू')}</h3><p>🔖 ${progress.bookmarks.length} ${B('bookmarked','बुकमार्क')} · ❌ ${progress.mistakes.length} ${B('mistakes to revise','दोहोर्‍याउनुपर्ने गल्ती')}</p>
    <button class="btn secondary" onclick="showView('review')">${B('Open Bookmarks &amp; Mistakes','बुकमार्क र गल्तीहरू खोल्नुहोस्')}</button></div>
    <div class="card"><p class="muted">Your progress is saved on this device (local preview) — it will sync to your account once Supabase is connected. Signing out keeps your XP and attempts on this device; it only removes the name and email from the profile.</p>
    ${progress.name ? '<button class="btn danger" onclick="signOut()">Sign out</button>' : ''}</div>`;
}

/* ---------- Discussion Hub ---------- */
function seedDiscussions(){
  const t = (id, exam, title, body, author, replies) => ({ id, exam, title, body, author, createdAt: '2026-10-26T08:00:00Z', upvotes: 0, replies: replies || [], reports: [] });
  return [
    t('DIS-001', 'kharidar', 'Kharidar prelim: is negative marking really 20%?', 'I keep hearing different numbers — some guides say 0.25 per wrong answer, some say 20%. Which one does the real Kharidar prelim use?', 'Guest aspirant', [{ author: 'Ravi (maintainer)', body: '20% — a wrong 2-mark question costs −0.4. That is the PSC rule the mocks here use. The 0.25 figure is from older papers / other exams.', createdAt: '2026-10-26T08:30:00Z' }]),
    t('DIS-002', 'nasu', 'NaSu Paper II — what should I study for the subjective paper?', 'Prelim is MCQ, but Paper II is descriptive. Any good sources for office procedure + report writing?', 'Guest aspirant', []),
    t('DIS-003', 'section-officer', 'Section Officer GK: how deep does Constitution 2072 go?', 'Do they ask article numbers, or just the big ideas (fundamental rights, federal structure)?', 'Guest aspirant', [{ author: 'Ravi (maintainer)', body: 'Both — article numbers for the famous ones (e.g. fundamental rights, Art. 17–33) and the structure for the rest. The Constitution topic in Practice covers the high-yield articles.', createdAt: '2026-10-26T09:00:00Z' }]),
    t('DIS-004', 'tsc-license', 'TSC licence exam pattern — is the time limit really unverified?', 'The guide says the licence time limit is unverified. Has anyone seen the official TSC notice?', 'Guest aspirant', []),
    t('DIS-005', 'nrb-assistant', 'NRB Assistant: management vs economics weightage?', 'The mock mixes both — which section carries more marks in the real paper?', 'Guest aspirant', []),
    t('DIS-006', 'nmc-mbbs', 'NMC licence: do the 10 CSQs count in the mock here?', 'The real MBBS licence has 130 MCQs + 10 clinical scenario questions. This mock only has the 130 — is that right?', 'Guest aspirant', [{ author: 'Ravi (maintainer)', body: 'Yes — the mock here is the MCQ part only (130/130, pass judged at 50% of the real 180 total). CSQs cannot be auto-marked yet, so they are noted on the guide card instead.', createdAt: '2026-10-26T09:15:00Z' }]),
    t('DIS-007', 'nnc-rn', 'Nursing licence (NLEN): no negative marking — confirmed?', 'I have heard there is no negative marking in the nursing licence. Can someone confirm from the NNC notice?', 'Guest aspirant', []),
    t('DIS-008', 'npc-pharmacy', 'Pharmacy licence: 50% in EACH subject or overall?', 'Some seniors say you need 50% in every subject, others say 50% overall. Which is it?', 'Guest aspirant', []),
    t('DIS-009', 'general', 'General doubts — ask anything about Lok Sewa prep', 'Stuck on a topic, confused by a pattern, or not sure which exam to target? Ask here.', 'Ravi (maintainer)', []),
  ];
}
function loadDiscussions(){
  const d = lsGet(LS_DISCUSS, null);
  if (d) return d;
  const seed = seedDiscussions();
  lsSet(LS_DISCUSS, seed);
  return seed;
}
function saveDiscussions(list){ lsSet(LS_DISCUSS, list); }
let pendingDiscuss = null; // {qid} set by discussQuestion() before opening the Hub
function discussQuestion(qid){
  const q = QUESTIONS.find(x => x.id === qid);
  pendingDiscuss = { qid, text: q ? qText(q) : '' };
  showView('discuss');
}
function postThread(){
  const title = (document.getElementById('dis-title').value || '').trim();
  const body = (document.getElementById('dis-body').value || '').trim();
  const exam = document.getElementById('dis-exam').value || 'general';
  const err = document.getElementById('dis-error');
  if (title.length < 8) { if (err) err.textContent = B('Please give your thread a title (at least 8 characters).','कृपया थ्रेडलाई शीर्षक दिनुहोस् (कम्तीमा ८ अक्षर)।'); return; }
  if (body.length < 10) { if (err) err.textContent = B('Please describe your doubt (at least 10 characters).','कृपया आफ्नो शङ्का वर्णन गर्नुहोस् (कम्तीमा १० अक्षर)।'); return; }
  const list = loadDiscussions();
  list.unshift({ id: uid('DIS'), exam, title, body, author: currentUserName(), createdAt: nowIso(), upvotes: 0, replies: [], reports: [] });
  saveDiscussions(list);
  document.getElementById('dis-title').value = ''; document.getElementById('dis-body').value = '';
  pendingDiscuss = null;
  renderDiscuss();
}
function postReply(threadId){
  const ta = document.getElementById('reply-' + threadId);
  const body = (ta && ta.value || '').trim();
  if (body.length < 2) { alert(B('Please write a reply first.','पहिले उत्तर लेख्नुहोस्।')); return; }
  const list = loadDiscussions();
  const th = list.find(x => x.id === threadId); if (!th) return;
  th.replies.push({ author: currentUserName(), body, createdAt: nowIso() });
  saveDiscussions(list); renderDiscuss();
}
function upvoteThread(threadId){
  const list = loadDiscussions();
  const th = list.find(x => x.id === threadId); if (!th) return;
  th.upvotes = (th.upvotes || 0) + 1;
  saveDiscussions(list); renderDiscuss();
}
function reportPost(threadId, replyIndex){
  const reason = prompt(B('Report this post — why? (spam / wrong info / abusive / other)','यो पोस्ट रिपोर्ट गर्नुहोस् — किन? (स्पाम / गलत जानकारी / अभद्र / अन्य)'));
  if (reason === null) return;
  const list = loadDiscussions();
  const th = list.find(x => x.id === threadId); if (!th) return;
  th.reports = th.reports || [];
  th.reports.push({ replyIndex: replyIndex == null ? null : replyIndex, reason: reason || 'no reason given', by: currentUserName(), at: nowIso() });
  saveDiscussions(list);
  alert(B('Thanks — the report is saved on this device (local preview) for the maintainer to review.','धन्यवाद — समीक्षकले हेर्नका लागि रिपोर्ट यो डिभाइसमा सेभ गरिएको छ (स्थानीय पूर्वावलोकन)।'));
  renderDiscuss();
}
function renderDiscuss(){
  const box = document.getElementById('discuss-box'); if (!box) return;
  const list = loadDiscussions();
  const examOpts = '<option value="general">'+B('General doubts','सामान्य शङ्काहरू')+'</option>' + EXAMS.map(e => `<option value="${e.id}">${esc(e.name)}</option>`).join('');
  let preTitle = '', preBody = '';
  if (pendingDiscuss) {
    preTitle = 'Question ' + pendingDiscuss.qid;
    preBody = 'Discussing question ' + pendingDiscuss.qid + (pendingDiscuss.text ? ': ' + pendingDiscuss.text : '') + '\n\nMy doubt: ';
  }
  const threadHtml = list.map(th => `
    <div class="card"><div class="muted">${esc(examById(th.exam)?.name || (th.exam === 'general' ? B('General doubts','सामान्य शङ्काहरू') : th.exam))} · ${B('by','—')} ${esc(th.author)} · ${esc((th.createdAt || '').slice(0, 10))} ${th.reports && th.reports.length ? '· ⚑ ' + th.reports.length + ' ' + B('report(s)','रिपोर्ट') : ''}</div>
    <h3 style="margin:6px 0">${esc(th.title)}</h3><p>${esc(th.body)}</p>
    <p><button class="btn secondary" onclick="upvoteThread('${th.id}')">▲ ${B('Upvote','मत दिनुहोस्')} (${th.upvotes || 0})</button>
    <button class="btn secondary" onclick="reportPost('${th.id}', null)">⚑ ${B('Report','रिपोर्ट')}</button></p>
    ${(th.replies || []).map((r, i) => `<div class="reply"><strong>${esc(r.author)}</strong> <span class="muted">${esc((r.createdAt || '').slice(0, 10))}</span><br>${esc(r.body)}<br><button class="btn secondary" onclick="reportPost('${th.id}', ${i})">⚑ ${B('Report','रिपोर्ट')}</button></div>`).join('')}
    <div style="margin-top:10px"><label for="reply-${th.id}">${B('Reply as','उत्तर दिने')}: ${esc(currentUserName())}${progress.name ? '' : ' ('+B('Guest','अतिथि')+' — '+B('sign in to post under your name','आफ्नो नाममा पोस्ट गर्न साइन इन गर्नुहोस्')+')'}</label>
    <textarea id="reply-${th.id}" rows="2" placeholder="${B('Write a helpful reply…','सहयोगी उत्तर लेख्नुहोस्…')}"></textarea>
    <button class="btn secondary" onclick="postReply('${th.id}')">${B('Reply','उत्तर दिनुहोस्')}</button></div></div>`).join('');
  box.innerHTML = `
    <p class="muted"><strong>${B('Local preview —','स्थानीय पूर्वावलोकन —')}</strong> ${B('posts are saved on this device only until the online backend is connected. With Supabase, threads sync across users in real time (see docs/BACKEND.md).','ब्याकएन्ड अनलाइन नजोडिएसम्म पोस्टहरू यो डिभाइसमा मात्र सेभ हुन्छन्। Supabase जोडिएपछि थ्रेडहरू प्रयोगकर्ताबीच रियल-टाइममा सिङ्क हुन्छन् (docs/BACKEND.md हेर्नुहोस्)।')} ${B('Posting as','पोस्ट गर्दै')}: <strong>${esc(currentUserName())}</strong>${progress.name ? '' : ' ('+B('Guest','अतिथि')+' — <a href="#" onclick="showView(\'auth\');return false">'+B('sign in','साइन इन')+'</a> '+B('to post under your name','आफ्नो नाममा पोस्ट गर्न')+')'}.</p>
    <div class="card"><h3>${B('Start a thread','थ्रेड सुरु गर्नुहोस्')}</h3>
      <label for="dis-exam">${B('Exam / topic','परीक्षा / विषय')}</label><select id="dis-exam">${examOpts}</select>
      <label for="dis-title">${B('Title','शीर्षक')}</label><input type="text" id="dis-title" maxlength="140" value="${esc(preTitle)}">
      <label for="dis-body">${B('Your question / doubt','तपाईंको प्रश्न / शङ्का')}</label><textarea id="dis-body" rows="4">${esc(preBody)}</textarea>
      <p class="error-text" id="dis-error"></p>
      <button class="btn" onclick="postThread()">${B('Post thread','थ्रेड पोस्ट गर्नुहोस्')}</button></div>
    <h3>${B('Threads','थ्रेडहरू')} (${list.length})</h3>${threadHtml || emptyState('💬', B('No threads yet','अझै थ्रेड छैन'), B('Start the first discussion — ask a doubt or share a tip with fellow aspirants.','पहिलो छलफल सुरु गर्नुहोस् — शङ्का सोध्नुहोस् वा साथी परीक्षार्थीसँग सुझाव बाँड्नुहोस्।'), B('Start a thread','थ्रेड सुरु गर्नुहोस्'), "document.getElementById('dis-title').focus()")}`;
}

/* ---------- Report a wrong question ---------- */
// Unified with the general report form (report.js): one form for
// bugs, wrong info and wrong questions. Falls back to the old modal only
// when report.js is not loaded.
function openReportForm(qid){
  if (typeof openIssueForm === 'function') { openIssueForm({ questionId: qid }); return; }
  const m = document.getElementById('modal'); const b = document.getElementById('modal-body');
  if (!m || !b) return;
  b.innerHTML = `<h3>Report wrong question — ${esc(qid)}</h3>
    <p class="muted">Reports are stored on this device (localStorage) in local preview for the maintainer to review. Once Supabase is connected they go to the shared moderation queue.</p>
    <label for="rep-reason">What is wrong?</label>
    <select id="rep-reason"><option value="wrong-answer">Wrong answer</option><option value="wrong-explanation">Wrong / misleading explanation</option><option value="typo">Typo or unclear wording</option><option value="outdated">Outdated fact</option><option value="duplicate">Duplicate of another question</option><option value="other">Other</option></select>
    <label for="rep-comment">Comment (what should it be? include a source if you can)</label>
    <textarea id="rep-comment" rows="3" placeholder="e.g. The correct answer is … because … (source: …)"></textarea>
    <p class="error-text" id="rep-error"></p>
    <button class="btn" onclick="submitReport('${esc(qid)}')">Submit report</button>
    <button class="btn secondary" onclick="closeModal()">Cancel</button>`;
  m.hidden = false;
}
function closeModal(){ const m = document.getElementById('modal'); if (m) m.hidden = true; }
document.addEventListener('keydown', e=>{ if(e.key==='Escape'){ const m=document.getElementById('modal'); if(m && !m.hidden) closeModal(); } });
document.addEventListener('click', e=>{ const m=document.getElementById('modal'); if(m && e.target===m) closeModal(); });
function submitReport(qid, reason, comment, type){
  // Called from the modal (reason/comment from the form) or directly by tests.
  // `type` is optional (unified form passes 'wrong-question'); stored so the
  // moderation view can label question reports like general ones.
  if (reason === undefined) {
    const r = document.getElementById('rep-reason'); reason = r ? r.value : 'other';
    const c = document.getElementById('rep-comment'); comment = c ? c.value.trim() : '';
  }
  if (!comment) { const e = document.getElementById('rep-error'); if (e) e.textContent = B('Please add a short comment — what is wrong and what should it be?','कृपया छोटो टिप्पणी थप्नुहोस् — के गलत छ र के हुनुपर्ने हो?'); return false; }
  const list = lsGet(LS_REPORTS, []);
  list.push({ id: uid('REP'), questionId: qid, reason, comment, by: currentUserName(), at: nowIso(), status: 'open', kind: 'question', type: type || 'wrong-question' });
  lsSet(LS_REPORTS, list);
  closeModal();
  return true;
}

/* ---------- Submit a question: validation, duplicates, spam, rate limit ---------- */
function normaliseText(s){
  return String(s || '').toLowerCase().replace(/[^\p{L}\p{N}\s]/gu, ' ').replace(/\s+/g, ' ').trim();
}
function tokenJaccard(a, b){
  return jaccardNorm(normaliseText(a), normaliseText(b));
}
// Jaccard similarity of two already-normalised strings (token sets).
// Split out so findDuplicate can reuse the cached normalised bank texts
// instead of re-normalising all 59,076 questions on every submission.
function jaccardNorm(nA, nB){
  const A = new Set(nA.split(' ').filter(Boolean));
  const B = new Set(nB.split(' ').filter(Boolean));
  if (!A.size || !B.size) return 0;
  let inter = 0; A.forEach(t => { if (B.has(t)) inter++; });
  return inter / (A.size + B.size - inter);
}
// Cache of normalised bank texts + an inverted token index, rebuilt only
// when the bank changes (keyed on length + first/last id — a community
// approval grows the bank by one, which invalidates it). Without this,
// findDuplicate re-ran normaliseText + token-Jaccard over the whole 59k
// bank per submit (~600–800 ms of dead button on every click).
let _dupCache={key:'', items:[], enIndex:null, neIndex:null};
function dupIndex(bank){
  const key=bank.length+'|'+(bank[0]&&bank[0].id||'')+'|'+(bank[bank.length-1]&&bank[bank.length-1].id||'');
  if(_dupCache.key!==key){
    const items=bank.map(q=>({q, nEn:normaliseText(q.question), nNe:q.question_ne?normaliseText(q.question_ne):''}));
    const buildIndex=field=>{
      const idx=new Map();
      items.forEach((it,i)=>{
        new Set(it[field].split(' ').filter(Boolean)).forEach(t=>{
          let list=idx.get(t); if(!list){ list=[]; idx.set(t,list); } list.push(i);
        });
      });
      return idx;
    };
    _dupCache={key, items, enIndex:buildIndex('nEn'), neIndex:buildIndex('nNe')};
  }
  return _dupCache;
}
// Item indices sharing enough tokens with the query that a Jaccard >= 0.8
// is still possible. Jaccard >= 0.8 needs shared >= (4/9)(a+b) > (4/9)a,
// where a is the query token count — so anything sharing fewer than
// floor(4a/9)+1 tokens can never be a near-duplicate and is skipped
// without computing Jaccard. (Exact matches are handled by the cheap
// string-equality loop in findDuplicate, not here.)
function _nearCandidates(cache, nQ, index){
  const toks=new Set(nQ.split(' ').filter(Boolean));
  const a=toks.size;
  if(!a) return [];
  const minShared=Math.floor(4*a/9)+1;
  const counts=new Map();
  toks.forEach(t=>{
    const list=index.get(t);
    if(list) list.forEach(i=>counts.set(i,(counts.get(i)||0)+1));
  });
  const out=[];
  counts.forEach((c,i)=>{ if(c>=minShared) out.push(i); });
  return out;
}
// Returns null (no duplicate), or {type:'exact'|'near', match:<question>, score}.
// Exact = normalised text identical; near = token-Jaccard >= 0.8 on EN or NE text.
function findDuplicate(qEn, qNe, bank){
  const nEn = normaliseText(qEn), nNe = normaliseText(qNe);
  const cache = dupIndex(bank || QUESTIONS);
  const items = cache.items;
  for (const it of items) {
    if (it.nEn === nEn || (nNe && it.nNe && it.nNe === nNe)) return { type: 'exact', match: it.q, score: 1 };
  }
  let best = null;
  const cand = new Set([..._nearCandidates(cache, nEn, cache.enIndex), ...(nNe ? _nearCandidates(cache, nNe, cache.neIndex) : [])]);
  cand.forEach(i => {
    const it = items[i];
    const s = Math.max(jaccardNorm(nEn, it.nEn), nNe && it.nNe ? jaccardNorm(nNe, it.nNe) : 0);
    if (s >= 0.8 && (!best || s > best.score)) best = { type: 'near', match: it.q, score: s };
  });
  return best;
}
function hasUrl(s){ return /(https?:\/\/|www\.)/i.test(String(s || '')); }
function repeatedChars(s){ return /(.)\1{4,}/.test(String(s || '')); }
function capsRatio(s){
  const letters = String(s || '').replace(/[^A-Za-z]/g, '');
  if (!letters.length) return 0;
  return letters.replace(/[^A-Z]/g, '').length / letters.length;
}
// Pure validation of a submission object. Returns {ok, errors[]}.
function validateSubmission(d){
  const errors = [];
  const need = (v, labelEn, labelNe) => { if (!String(v || '').trim()) errors.push(B(labelEn, labelNe) + B(' is required.',' आवश्यक छ।')); };
  need(d.exam, 'Exam', 'परीक्षा'); need(d.topic, 'Topic', 'विषय'); need(d.difficulty, 'Difficulty', 'कठिनाइ');
  need(d.question, 'Question (English)', 'प्रश्न (अङ्ग्रेजी)'); need(d.question_ne, 'Question (Nepali)', 'प्रश्न (नेपाली)');
  need(d.explanation, 'Explanation (English)', 'व्याख्या (अङ्ग्रेजी)'); need(d.explanation_ne, 'Explanation (Nepali)', 'व्याख्या (नेपाली)');
  need(d.source, 'Source', 'स्रोत'); need(d.contributor, 'Contributor name', 'योगदानकर्ताको नाम');
  if (!d.marks || ![1, 2].includes(+d.marks)) errors.push(B('Marks must be 1 or 2.','अङ्क १ वा २ हुनुपर्छ।'));
  if (String(d.question || '').trim().length < 15) errors.push(B('Question must be at least 15 characters.','प्रश्न कम्तीमा १५ अक्षरको हुनुपर्छ।'));
  if (hasUrl(d.question) || hasUrl(d.question_ne)) errors.push(B('Do not put links in the question text — the source field is the only place for links.','प्रश्न पाठमा लिङ्क नराख्नुहोस् — लिङ्कका लागि स्रोत फिल्ड मात्र हो।'));
  if (repeatedChars(d.question) || repeatedChars(d.question_ne)) errors.push(B('Question text contains repeated characters (e.g. "!!!!!") — please write normally.','प्रश्न पाठमा दोहोरिएका अक्षर छन् (जस्तै "!!!!!") — सामान्य रूपमा लेख्नुहोस्।'));
  if (capsRatio(d.question) > 0.5) errors.push(B('Question is mostly ALL CAPS — please write normally.','प्रश्न प्रायः सबै ठूलो अक्षरमा छ — सामान्य रूपमा लेख्नुहोस्।'));
  const checkOpts = (opts, labelEn, labelNe) => {
    if (!Array.isArray(opts) || opts.length !== 4) { errors.push(B(labelEn, labelNe) + B(': exactly 4 options are required.',': ठ्याक्कै ४ विकल्प आवश्यक छ।')); return; }
    const seen = new Set();
    opts.forEach((o, i) => {
      const t = String(o || '').trim();
      if (!t) errors.push(B(labelEn, labelNe) + ': ' + B('option ','विकल्प ') + String.fromCharCode(65 + i) + B(' is empty.',' खाली छ।'));
      const n = normaliseText(t);
      if (n && seen.has(n)) errors.push(B(labelEn, labelNe) + B(': options must all be different — two options say the same thing.',': सबै विकल्प फरक हुनुपर्छ — दुई विकल्प एउटै कुरा भन्छन्।'));
      seen.add(n);
    });
  };
  checkOpts(d.options, 'Options (English)', 'विकल्पहरू (अङ्ग्रेजी)');
  checkOpts(d.options_ne, 'Options (Nepali)', 'विकल्पहरू (नेपाली)');
  if (d.answer === null || d.answer === undefined || d.answer === '' || ![0, 1, 2, 3].includes(+d.answer)) errors.push(B('Correct answer must be A, B, C or D.','सही उत्तर A, B, C वा D हुनुपर्छ।'));
  return { ok: errors.length === 0, errors };
}
// Pure rate-limit check: max 5 submissions per hour per device.
// timestamps = array of submittedAt epoch-ms; now = epoch-ms (default Date.now()).
function rateLimitCheck(timestamps, now){
  const t = now || Date.now();
  const recent = (timestamps || []).filter(x => t - x < 3600e3);
  if (recent.length >= 5) {
    const oldest = Math.min.apply(null, recent);
    const minutesLeft = Math.ceil((oldest + 3600e3 - t) / 60000);
    return { allowed: false, minutesLeft, count: recent.length };
  }
  return { allowed: true, minutesLeft: 0, count: recent.length };
}
function readSubmissionForm(){
  const v = id => { const el = document.getElementById(id); return el ? el.value : ''; };
  const opts = lang => [0, 1, 2, 3].map(i => v('sub-opt-' + lang + '-' + i));
  return {
    exam: v('sub-exam'), topic: v('sub-topic').trim(), subtopic: v('sub-subtopic').trim(),
    difficulty: v('sub-diff'), marks: +v('sub-marks') || 2,
    question: v('sub-q-en').trim(), question_ne: v('sub-q-ne').trim(),
    options: opts('en'), options_ne: opts('ne'),
    answer: v('sub-answer') === '' ? null : +v('sub-answer'),
    explanation: v('sub-expl-en').trim(), explanation_ne: v('sub-expl-ne').trim(),
    source: v('sub-source').trim(), contributor: v('sub-name').trim() || currentUserName(),
  };
}
function validateSubmitLive(){
  const d = readSubmissionForm();
  const { errors } = validateSubmission(d);
  const box = document.getElementById('sub-errors');
  if (box) box.innerHTML = errors.length ? '<strong>Fix these before submitting:</strong><ul>' + errors.map(e => '<li>' + esc(e) + '</li>').join('') + '</ul>' : '<span class="pass">✓ Looks good so far — checks run again on submit.</span>';
  // The form changed, so a previously submitted question is no longer the
  // form's content: re-enable the submit button (submitQuestion disables
  // it after a successful submit to block double-clicks).
  const submitBtn = document.getElementById('sub-submit-btn');
  if (submitBtn) submitBtn.disabled = false;
  return errors;
}
function submitQuestion(){
  const d = readSubmissionForm();
  const box = document.getElementById('sub-errors');
  const { ok, errors } = validateSubmission(d);
  if (!ok) { if (box) box.innerHTML = '<strong>Cannot submit yet:</strong><ul>' + errors.map(e => '<li>' + esc(e) + '</li>').join('') + '</ul>'; return; }
  // Duplicate check against the full bank (exact + near-duplicate).
  const dup = findDuplicate(d.question, d.question_ne, QUESTIONS);
  if (dup) {
    const msg = dup.type === 'exact'
      ? 'This question already exists in the bank (' + dup.match.id + '). Please submit a different question.'
      : 'This looks like an existing question (' + dup.match.id + ', similarity ' + Math.round(dup.score * 100) + '%). Please check it and submit something different.';
    if (box) box.innerHTML = '<strong>Possible duplicate — not submitted.</strong><br>' + esc(msg);
    return;
  }
  // Spam: 3 identical submissions already in the queue.
  const queue = lsGet(LS_SUBMISSIONS, []);
  const same = queue.filter(s => normaliseText(s.question) === normaliseText(d.question)).length;
  if (same >= 3) { if (box) box.textContent = 'This exact question has already been submitted 3 times — it is in the review queue. Please submit something different.'; return; }
  // Double-submit guard: a second click (or a re-submit of the same text)
  // while an identical question is already pending must not queue a second
  // copy — the old code only stopped at 3 identical copies, so a double
  // click queued the question twice for the maintainer to review twice.
  const alreadyPending = queue.some(s => s.status === 'pending' && normaliseText(s.question) === normaliseText(d.question));
  if (alreadyPending) { if (box) box.textContent = 'This question is already in the review queue (pending) — it was submitted once already. Please submit something different.'; return; }
  // Rate limit: max 5 per hour per device.
  const rl = rateLimitCheck(queue.map(s => s.submittedAt), Date.now());
  if (!rl.allowed) { if (box) box.textContent = B('Rate limit: you have submitted 5 questions in the last hour. Please wait about ' + rl.minutesLeft + ' minute(s) and try again.','दर सीमा: पछिल्लो घण्टामा ५ प्रश्न पेस गरिसक्नुभयो। करिब ' + rl.minutesLeft + ' मिनेट पर्खेर पुनः प्रयास गर्नुहोस्।'); return; }
  queue.push({ id: uid('SUB'), status: 'pending', submittedAt: Date.now(), ...d });
  lsSet(LS_SUBMISSIONS, queue);
  const done = document.getElementById('sub-done');
  if (done) { done.hidden = false; done.textContent = 'Submitted for review — it will NOT go live instantly. A maintainer reviews every submission; first-time submissions never go live instantly. Thank you!'; }
  if (box) box.innerHTML = '';
  // Disable the submit button until the form changes again, so a double
  // click (or an impatient second tap) cannot queue the same question twice.
  // validateSubmitLive() re-enables it on the next edit.
  const submitBtn = document.getElementById('sub-submit-btn');
  if (submitBtn) submitBtn.disabled = true;
  renderSubmitCounts();
}
function submissionCounts(){
  const q = lsGet(LS_SUBMISSIONS, []);
  return { approved: q.filter(s => s.status === 'approved').length, rejected: q.filter(s => s.status === 'rejected').length, pending: q.filter(s => s.status === 'pending').length };
}
function renderSubmitCounts(){
  const c = submissionCounts();
  const el = document.getElementById('sub-counts');
  if (el) el.textContent = 'Public moderation log — approved ' + c.approved + ' · rejected ' + c.rejected + ' · pending ' + c.pending;
}
function copyTemplate(){
  const t = document.getElementById('sub-template');
  if (t && t.select) { t.select(); }
  try { if (navigator.clipboard) navigator.clipboard.writeText(t.value); } catch (e) {}
}
function renderSubmit(){
  const box = document.getElementById('submit-box'); if (!box) return;
  const c = submissionCounts();
  box.innerHTML = `
    <div class="card" style="border-color:#ea580c"><strong>⚠️ ${B('Reviewed before publishing.','प्रकाशनअघि समीक्षा हुन्छ।')}</strong> ${B('Submissions go through automatic checks (duplicate detection, spam heuristics, rate limit) <em>and</em> maintainer review. <strong>First-time submissions never go live instantly</strong> — Ravi Yadav approves or rejects every one. Contributors with 3+ approved questions and 0 rejections get faster review.','पेस गरिएका प्रश्न स्वचालित जाँच (डुप्लिकेट पहिचान, स्पाम नियम, दर सीमा) <em>र</em> समीक्षक समीक्षाबाट जान्छन्। <strong>पहिलो पेस कहिल्यै तुरुन्त लाइभ हुँदैन</strong> — रवि यादवले हरेक प्रश्न स्वीकृत वा अस्वीकृत गर्नुहुन्छ। ३+ स्वीकृत प्रश्न र ० अस्वीकृति भएका योगदानकर्ताको समीक्षा छिटो हुन्छ।')}</div>
    <p class="muted" id="sub-counts">Public moderation log — approved ${c.approved} · rejected ${c.rejected} · pending ${c.pending}</p>
    <div class="card"><h3>The exact format — copy this template</h3>
      <p class="muted">Every question must follow this JSON shape (the same schema as the bank). Nepali fields are required — the bank is 100% bilingual.</p>
      <textarea id="sub-template" rows="14" readonly>{
  "id": "COMM-000",
  "exam": ["kharidar", "nasu"],
  "topic": "Constitution &amp; Governance",
  "subtopic": "Fundamental Rights",
  "difficulty": "medium",
  "marks": 2,
  "question": "Which article of the Constitution of Nepal 2072 guarantees the right to freedom?",
  "question_ne": "नेपालको संविधान २०७२ को कुन धाराले स्वतन्त्रताको हकको ग्यारेन्टी गर्छ?",
  "options": ["Article 17", "Article 18", "Article 19", "Article 20"],
  "options_ne": ["धारा १७", "धारा १८", "धारा १९", "धारा २०"],
  "answer": 0,
  "explanation": "Article 17 guarantees the right to freedom.",
  "explanation_ne": "धारा १७ ले स्वतन्त्रताको हकको ग्यारेन्टी गर्छ।",
  "source": "Constitution of Nepal 2072, Part 3"
}</textarea>
      <button class="btn secondary" onclick="copyTemplate()">📋 Copy template</button>
      <p class="muted">Plain-text version: Question (EN + NE) · 4 options (EN + NE, all different) · correct answer (A–D) · explanation (EN + NE) · source (required — a URL or a book/article name).</p></div>
    <div class="card"><h3>Submit a question</h3>
      <p class="muted">Safety checks (first line of defence — server review is the real gate): duplicate detection against the full bank${QUESTIONS.length ? ' (' + QUESTIONS.length.toLocaleString() + ' questions)' : ''}, spam heuristics, max 5 submissions per hour per device. CAPTCHA is added when the backend is connected.</p>
      <label for="sub-exam">Exam</label><select id="sub-exam"></select>
      <label for="sub-topic">Topic</label><input type="text" id="sub-topic" placeholder="e.g. Constitution & Governance" oninput="validateSubmitLive()">
      <label for="sub-subtopic">Subtopic</label><input type="text" id="sub-subtopic" placeholder="e.g. Fundamental Rights" oninput="validateSubmitLive()">
      <label for="sub-diff">Difficulty</label><select id="sub-diff"><option value="easy">Easy</option><option value="medium" selected>Medium</option><option value="hard">Hard</option></select>
      <label for="sub-marks">Marks</label><select id="sub-marks"><option value="2" selected>2</option><option value="1">1</option></select>
      <label for="sub-q-en">Question (English) — at least 15 characters, no links here</label><textarea id="sub-q-en" rows="2" oninput="validateSubmitLive()"></textarea>
      <label for="sub-q-ne">Question (Nepali)</label><textarea id="sub-q-ne" rows="2" oninput="validateSubmitLive()"></textarea>
      <label>Options (English) — 4 different options</label>
      ${[0, 1, 2, 3].map(i => `<input type="text" id="sub-opt-en-${i}" placeholder="Option ${String.fromCharCode(65 + i)} (English)" oninput="validateSubmitLive()">`).join('')}
      <label>Options (Nepali) — 4 different options</label>
      ${[0, 1, 2, 3].map(i => `<input type="text" id="sub-opt-ne-${i}" placeholder="Option ${String.fromCharCode(65 + i)} (Nepali)" oninput="validateSubmitLive()">`).join('')}
      <label for="sub-answer">Correct answer</label><select id="sub-answer"><option value="">— choose —</option><option value="0">A</option><option value="1">B</option><option value="2">C</option><option value="3">D</option></select>
      <label for="sub-expl-en">Explanation (English)</label><textarea id="sub-expl-en" rows="2" oninput="validateSubmitLive()"></textarea>
      <label for="sub-expl-ne">Explanation (Nepali)</label><textarea id="sub-expl-ne" rows="2" oninput="validateSubmitLive()"></textarea>
      <label for="sub-source">Source (required — URL or book / article name)</label><input type="text" id="sub-source" placeholder="e.g. Constitution of Nepal 2072, Part 3 — or a URL" oninput="validateSubmitLive()">
      <label for="sub-name">Contributor name</label><input type="text" id="sub-name" placeholder="Your name (defaults to your profile name)" value="${esc(progress.name || '')}">
      <div class="card" style="margin-top:12px"><strong>CAPTCHA — added when the online backend is connected (hCaptcha/reCAPTCHA).</strong><br><span class="muted">In local preview there is no CAPTCHA; the rate limit (5/hour) and duplicate/spam checks run instead.</span></div>
      <div class="error-text" id="sub-errors"></div>
      <div class="card" id="sub-done" hidden></div>
      <button class="btn" id="sub-submit-btn" onclick="submitQuestion()">Submit for review</button>
      <p class="muted">Submitting as <strong>${esc(currentUserName())}</strong>. ${progress.name ? '' : '<a href="#" onclick="showView(\'auth\');return false">Sign in</a> to attach your name.'}</p>
      <p><a href="#" onclick="showView('moderate');return false">${B('Maintainer Review queue (preview)','समीक्षक समीक्षा कतार (पूर्वावलोकन)')}</a></p>
    </div>`;
  fillExamSelects();
}

/* ---------- Moderation queue ---------- */
function communityApprovedQuestions(){
  const list = lsGet(LS_APPROVED, []);
  return list.map(q => ({ ...q, _community: true }));
}
function nextCommunityId(){
  const n = lsGet(LS_APPROVED, []).length + 1;
  return 'COMM-' + String(n).padStart(3, '0');
}
function modLog(action, submissionId, reason){
  const log = lsGet(LS_MODLOG, []);
  log.push({ action, submissionId, by: 'Ravi Yadav (demo maintainer)', reason: reason || '', at: nowIso() });
  lsSet(LS_MODLOG, log);
}
function approveSubmission(subId){
  const queue = lsGet(LS_SUBMISSIONS, []);
  const sub = queue.find(s => s.id === subId);
  if (!sub || sub.status !== 'pending') return null;
  // Edit-before-approve: read the maintainer's edited fields if present.
  const ev = id => { const el = document.getElementById(id); return el ? el.value : null; };
  const qEn = ev('mod-q-' + subId); const qNe = ev('mod-qne-' + subId);
  const expl = ev('mod-expl-' + subId); const explNe = ev('mod-explne-' + subId);
  const ans = ev('mod-ans-' + subId);
  const opts = [0, 1, 2, 3].map(i => ev('mod-opt-' + subId + '-' + i));
  const optsNe = [0, 1, 2, 3].map(i => ev('mod-optne-' + subId + '-' + i));
  const q = {
    id: nextCommunityId(),
    exam: [sub.exam], topic: sub.topic, subtopic: sub.subtopic || '',
    difficulty: sub.difficulty, marks: sub.marks,
    question: (qEn !== null && qEn.trim()) ? qEn.trim() : sub.question,
    question_ne: (qNe !== null && qNe.trim()) ? qNe.trim() : sub.question_ne,
    options: opts.every(o => o !== null && o.trim()) ? opts.map(o => o.trim()) : sub.options,
    options_ne: optsNe.every(o => o !== null && o.trim()) ? optsNe.map(o => o.trim()) : sub.options_ne,
    answer: ans !== null && ans !== '' ? +ans : sub.answer,
    explanation: (expl !== null && expl.trim()) ? expl.trim() : sub.explanation,
    explanation_ne: (explNe !== null && explNe.trim()) ? explNe.trim() : sub.explanation_ne,
    source: 'Community: ' + (sub.contributor || 'anonymous') + ' — ' + sub.source,
  };
  const approved = lsGet(LS_APPROVED, []);
  approved.push(q); lsSet(LS_APPROVED, approved);
  sub.status = 'approved'; lsSet(LS_SUBMISSIONS, queue);
  modLog('approved', subId, '');
  // Join the live bank immediately so it appears in practice without a reload.
  QUESTIONS.push({ ...q, _community: true });
  const qc = document.getElementById('q-count'); if (qc) qc.textContent = QUESTIONS.length.toLocaleString();
  renderModerate(); renderSubmitCounts();
  return q;
}
function rejectSubmission(subId, reason){
  if (reason === undefined) {
    const el = document.getElementById('mod-reason-' + subId);
    reason = el ? el.value.trim() : '';
  }
  if (!reason) { alert('Please give a reason for the rejection — the contributor sees it.'); return false; }
  const queue = lsGet(LS_SUBMISSIONS, []);
  const sub = queue.find(s => s.id === subId);
  if (!sub || sub.status !== 'pending') return false;
  sub.status = 'rejected'; sub.rejectReason = reason;
  lsSet(LS_SUBMISSIONS, queue);
  modLog('rejected', subId, reason);
  renderModerate(); renderSubmitCounts();
  return true;
}
function downloadApproved(){
  const data = JSON.stringify(lsGet(LS_APPROVED, []), null, 2);
  const blob = new Blob([data], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'community-approved.json';
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}
function renderModerate(){
  const box = document.getElementById('moderate-box'); if (!box) return;
  const queue = lsGet(LS_SUBMISSIONS, []);
  const pending = queue.filter(s => s.status === 'pending');
  const reports = lsGet(LS_REPORTS, []).filter(r => r.status === 'open');
  const c = submissionCounts();
  box.innerHTML = `
    <div class="card"><strong>Maintainer preview — real authentication is required in production.</strong> In this static build anyone opening this page can approve or reject. With Supabase, this view is restricted to the maintainer role (Ravi Yadav, 08raviyadav) via Row Level Security — see docs/BACKEND.md.</div>
    <p class="muted">Public moderation log — approved ${c.approved} · rejected ${c.rejected} · pending ${c.pending} · open reports: ${reports.length}</p>
    <p class="muted">Trusted-contributor rule: contributors with 3+ approved questions and 0 rejections get faster review. First-time submissions never go live instantly.</p>
    <p><button class="btn secondary" onclick="downloadApproved()">⬇ Download approved questions (community-approved.json)</button>
    <span class="muted">Approved questions are stored in localStorage in local preview and loaded into the practice bank at startup with a “Community” badge. The download is the JSON to commit to <code>data/questions/community-approved.json</code>.</span></p>
    <h3>Pending submissions (${pending.length})</h3>
    ${pending.length ? pending.map(s => `<div class="card">
      <div class="muted">${esc(s.id)} · by ${esc(s.contributor || 'anonymous')} · ${esc((s.submittedAt ? new Date(s.submittedAt).toISOString() : '').slice(0, 10))} · ${esc(s.exam)} · ${esc(s.topic)} · ${esc(s.difficulty)} · ${s.marks} mark(s) · source: ${esc(s.source)}</div>
      <label>Question (EN) — editable before approve</label><textarea id="mod-q-${s.id}" rows="2">${esc(s.question)}</textarea>
      <label>Question (NE)</label><textarea id="mod-qne-${s.id}" rows="2">${esc(s.question_ne)}</textarea>
      <label>Options (EN)</label>${s.options.map((o, i) => `<input type="text" id="mod-opt-${s.id}-${i}" value="${esc(o)}">`).join('')}
      <label>Options (NE)</label>${s.options_ne.map((o, i) => `<input type="text" id="mod-optne-${s.id}-${i}" value="${esc(o)}">`).join('')}
      <label>Correct answer</label><select id="mod-ans-${s.id}">${[0, 1, 2, 3].map(i => `<option value="${i}" ${+s.answer === i ? 'selected' : ''}>${String.fromCharCode(65 + i)}</option>`).join('')}</select>
      <label>Explanation (EN)</label><textarea id="mod-expl-${s.id}" rows="2">${esc(s.explanation)}</textarea>
      <label>Explanation (NE)</label><textarea id="mod-explne-${s.id}" rows="2">${esc(s.explanation_ne)}</textarea>
      <div style="margin-top:10px"><button class="btn green" onclick="approveSubmission('${s.id}')">✓ Approve</button>
      <input type="text" id="mod-reason-${s.id}" placeholder="Rejection reason (required to reject)" style="max-width:320px">
      <button class="btn danger" onclick="rejectSubmission('${s.id}')">✕ Reject</button></div>
    </div>`).join('') : emptyState('📥', B('No pending submissions','कुनै पेन्डिङ पेस छैन'), B('Submitted questions appear here for review.','पेस गरिएका प्रश्नहरू समीक्षाका लागि यहाँ देखिन्छन्।'), B('Contribute a question','प्रश्न योगदान गर्नुहोस्'), "showView('submit')")}
    ${typeof renderReportsSection === 'function' ? renderReportsSection() : `<h3>Open wrong-question reports (${reports.length})</h3>${reports.length ? reports.map(r => `<div class="card"><strong>${esc(r.questionId)}</strong> — ${esc(r.reason)}<br>${esc(r.comment)}<br><span class="muted">by ${esc(r.by)} · ${esc((r.at || '').slice(0, 10))}</span></div>`).join('') : '<p class="muted">No open reports.</p>'}`}`;
}

/* ================= Feature 9 — Ask: on-device rule-based helper =================
   Zero dependencies, no API keys, no network calls. A keyword intent engine
   over a compact intent->response table (EN + NE).
   CRITICAL SAFETY RULE: it must NEVER invent exam facts. Factual-looking
   questions ("how many articles…", "who is…", "when was…") are caught by
   isFactualQuestion() FIRST and routed to practice topics / Search — the
   bot only restates the portal's own documented data (how practice, mocks,
   negative marking and cutoffs work; exam specs already verified in
   data/exams.json). */
const LS_CHAT = 'loksewa_chat_history_v1';
const CHAT_MAX_MSGS = 200; // cap stored history per device
function chatNorm(s){
  return String(s || '').toLowerCase()
    .replace(/[?!.,;:()[\]{}"'`~|\\/<>@#$%^&*=+—–-]/g, ' ')
    .replace(/[।॥]/g, ' ')
    .replace(/\s+/g, ' ').trim();
}
// Keyword -> real bank topic names (must match question topic strings).
const CHAT_TOPIC_KEYS = [
  { topic: 'Constitution & Governance', keys: ['constitution', 'samvidhan', 'संविधान', 'governance', 'fundamental right', 'मौलिक हक', 'federal', 'सङ्घीय'] },
  { topic: 'Nepal History', keys: ['history', 'इतिहास', 'unification', 'एकीकरण', 'malla', 'rana'] },
  { topic: 'Nepal Geography', keys: ['geography', 'भूगोल', 'everest', 'सगरमाथा', 'himalaya', 'river', 'नदी'] },
  { topic: 'Culture & Society', keys: ['culture', 'संस्कृति', 'festival', 'चाडपर्व'] },
  { topic: 'Maths & Numerical', keys: ['math', 'गणित', 'percentage', 'profit', 'interest', 'प्रतिशत'] },
  { topic: 'IQ & Reasoning', keys: ['iq', 'reasoning', 'series', 'coding', 'तर्क'] },
  { topic: 'English', keys: ['english', 'अङ्ग्रेजी', 'grammar'] },
  { topic: 'Nepali Language', keys: ['nepali language', 'नेपाली भाषा', 'व्याकरण'] },
  { topic: 'Computer & ICT', keys: ['computer', 'कम्प्युटर', 'ict', 'internet'] },
  { topic: 'Current Affairs', keys: ['current', 'समसामयिक', 'news', 'समाचार'] },
  { topic: 'Economy & Development', keys: ['economy', 'अर्थतन्त्र', 'budget', 'बजेट'] },
  { topic: 'Banking & Finance', keys: ['bank', 'बैंक', 'finance', 'loan', 'कर्जा'] },
  { topic: 'Office Management & Public Service', keys: ['office', 'कार्यालय', 'civil service', 'निजामती', 'filing'] },
  { topic: 'Education & Pedagogy', keys: ['education', 'शिक्षा', 'pedagogy', 'teaching'] },
  { topic: 'Science & Tech', keys: ['science', 'विज्ञान', 'physics', 'chemistry', 'biology'] },
  { topic: 'Law', keys: ['law', 'कानुन', 'court', 'अदालत', 'act '] },
  { topic: 'Health/Technical basics', keys: ['health', 'स्वास्थ्य', 'nurse', 'नर्स'] },
];
function chatTopicFor(t){
  for (const e of CHAT_TOPIC_KEYS) { if (e.keys.some(k => t.includes(k))) return e.topic; }
  return null;
}
function chatTopicStats(bank){
  const stats = { total: 0, topics: {} };
  (bank || QUESTIONS).forEach(q => { if (q && q.topic) { stats.topics[q.topic] = (stats.topics[q.topic] || 0) + 1; stats.total++; } });
  return stats;
}
// Factual-question guard: these patterns mean the user wants a FACT, which
// the bot must never answer from memory — route to topics / Search instead.
// Checked BEFORE every other intent (e.g. "how many articles in the
// constitution" contains the topic keyword "constitution").
const FACT_RES = [
  /how many/, /how much/, /\bwhich (article|schedule|part|chapter|year|province|district|amendment)\b/,
  /\bwho (is|was|were|are|has|invented|discovered|wrote|built|founded)\b/, /\bwho wrote\b/, /\bwho discovered\b/,
  /\bwhen (was|were|did|is)\b/, /\bwhere (is|was|are)\b/, /full form/, /abbreviation/, /stands for/,
  /\bcapital of\b/, /\b(largest|smallest|highest|longest|oldest|first|last) (river|mountain|district|lake|province|king|president|prime minister)\b/,
  /कति/, /कहिले/, /कहाँ/, /पूर्ण ?रूप/, /को (हुन्|थिए|छन्|हो)/, /कसले (लेखे|बनाए|पत्ता|स्थापना)/,
  /नेपालको (राजधानी|क्षेत्रफल|जनसंख्या)/,
];
function isFactualQuestion(t){ return FACT_RES.some(re => re.test(t)); }

// Compact intent -> response tables, both languages.
const CHAT_EN = {
  welcome: 'Namaste! 🙏 I\'m the on-device helper for Outrank — a rule-based assistant, not real AI. I can explain how to use this portal, find the right exam, mock and topics for you, and share study tips. I never invent exam facts: for factual questions I point you to practice topics instead. What would you like to know?',
  demo: 'Local preview —', demoText: 'chat history stays on this device only (localStorage).',
  helper: 'On-device helper — rule-based, not real AI',
  helperText: 'It runs entirely in your browser with no network calls and no API keys. It only knows this portal — it never invents exam facts; factual questions are routed to practice topics.',
  placeholder: 'Ask about the portal, exams, mocks, cutoffs…', send: 'Send', clear: 'Clear',
  chips: [
    { q: 'How do mocks work?', label: 'How do mocks work?' },
    { q: 'I want to prepare for Kharidar', label: 'Prepare for Kharidar' },
    { q: 'What is negative marking?', label: 'Negative marking?' },
    { q: 'Give me study tips', label: 'Study tips' },
  ],
  greeting: 'Namaste! 🙏 Ask me how to use the portal (practice, mocks, cutoffs), which exam to prepare for, or for study tips.',
  help: 'Here\'s what I can do:\n• Explain the portal — how practice, mocks, negative marking and cutoffs work\n• Find your exam — say "I want to prepare for Kharidar" and I\'ll point you to the right mock and topics\n• Share study tips — short and practical\n• Tell you where things are — Dashboard, Bookmarks, Old Papers, Notices…\nTap a suggestion below, or ask in your own words.',
  practice: 'Go to **Practice** → pick your exam (e.g. Kharidar) and a topic → **Start practice**. Every set shuffles both the question order and the option order — no two attempts are the same. Wrong answers are saved to **Bookmarks** automatically, and XP + streaks keep you going.',
  mock: 'Go to **Mock Exams** → choose your mock → **Start mock exam**. It\'s full-length and timed, auto-submits when time runs out, and your result is judged against the real cutoff. Answers are NOT revealed until you finish — just like the real exam hall. Use the question palette to jump between questions.',
  negative: 'PSC papers use 20% negative marking: a wrong 2-mark question costs −0.4, a wrong 1-mark question costs −0.2. Skipped questions cost 0. Licence papers (NNC / NHPC) have no negative marking — wrong answers cost nothing there.',
  cutoff: 'Your result is judged against the real cutoff for your exam: Kharidar / NaSu 45, Section Officer 45, TSC 50, NRB Assistant 40. The prelim is qualifying only — it doesn\'t add to your final merit.',
  tips: 'Five that actually work:\n• 20-minute blocks with 5-minute breaks — use the Focus Timer on Home.\n• Mix topics — alternate Constitution, GK, Maths and IQ so your brain stays awake.\n• Repeat at intervals — revisit a topic after 1 day, 3 days, then a week.\n• Test, don\'t just read — a 5-question Quick Quiz beats re-reading a chapter.\n• End on a win — finish each session with a topic you\'re good at.',
  xp: 'You earn XP from every attempt (score × 10), keep a daily streak by practicing each day, and collect badges — see your **Dashboard** for all of it.',
  daily: 'On **Home**: 🔥 Daily Challenge (10 Q), ⚡ Quick Quiz (5 Q), 🎲 Surprise me (10 Q), ⏱️ Speed Round (10 Q · 60 s) and 🏃 Mistake Marathon. No setup needed — just tap one.',
  thanks: 'You\'re welcome! Good luck with your preparation. 🙏',
  fallback: 'I\'m not sure about that — I only know this portal. Try the **Discussion Hub** for doubts, **Search** to find questions on a topic, or ask me about practice, mocks, cutoffs, or an exam like Kharidar.',
  where: {
    dashboard: 'Your **Dashboard** (Stats in the nav) shows XP, streaks, attempts, best mocks and personal records — all saved on this device.',
    bookmarks: '**Bookmarks & Mistakes** (Saved in the nav) — wrong answers land here automatically; bookmark any question to revise it later.',
    discuss: '**Discussion Hub** (Discuss in the nav) — ask doubts and reply to others. Local preview: threads stay on this device.',
    papers: '**Old Papers** — real previous-year papers, with 133 transcribed questions you can practice and the rest scanned with source links.',
    notices: '**Notices** — vacancy notices from PSC, TSC, NRB and others. Always confirm on the official site before applying.',
    search: 'Use **Search** for full-text search across the whole question bank.',
    flashcards: '**Flashcards** — 20 random questions, answer on reveal. Good for the bus or the last 10 minutes before bed.',
    funfacts: '**Fun Facts** — verified bilingual facts: one a day on Home, one after every 5th practice question.',
    profile: '**Profile** — your demo sign-in lives here. Everything is stored on this device only.',
    contribute: '**Contribute** — submit a question for review. First-time submissions never go live instantly; the maintainer reviews every one.',
  },
};
const CHAT_NE = {
  welcome: 'नमस्ते! 🙏 म Outrank को अन-डिभाइस सहायक हुँ — नियममा आधारित सहायक, वास्तविक AI होइन। म यो पोर्टल कसरी प्रयोग गर्ने भनेर बताउन सक्छु, तपाईंको परीक्षा, मक र विषय खोज्न सक्छु, अनि अध्ययन सुझाव दिन सक्छु। म तथ्य अनुमान गरेर उत्तर दिन्नँ — तथ्यात्मक प्रश्नमा अभ्यास विषयतर्फ पठाउँछु। के जान्न चाहनुहुन्छ?',
  demo: 'स्थानीय पूर्वावलोकन —', demoText: 'च्याट इतिहास यो डिभाइसमा मात्र रहन्छ (localStorage)।',
  helper: 'अन-डिभाइस सहायक — नियममा आधारित, वास्तविक AI होइन',
  helperText: 'यो तपाईंको ब्राउजरमै चल्छ — कुनै नेटवर्क कल छैन, कुनै API key छैन। यसले यो पोर्टल मात्र चिन्छ — तथ्य अनुमान गर्दैन; तथ्यात्मक प्रश्न अभ्यास विषयतर्फ पठाइन्छ।',
  placeholder: 'पोर्टल, परीक्षा, मक, कटअफबारे सोध्नुहोस्…', send: 'पठाउनुहोस्', clear: 'मेटाउनुहोस्',
  chips: [
    { q: 'मक कसरी काम गर्छ?', label: 'मक कसरी?' },
    { q: 'म खरिदारको तयारी गर्न चाहन्छु', label: 'खरिदार तयारी' },
    { q: 'नेगेटिभ मार्किङ के हो?', label: 'नेगेटिभ मार्किङ?' },
    { q: 'अध्ययन सुझाव दिनुहोस्', label: 'अध्ययन सुझाव' },
  ],
  greeting: 'नमस्ते! 🙏 पोर्टल कसरी प्रयोग गर्ने (अभ्यास, मक, कटअफ), कुन परीक्षाको तयारी गर्ने, वा अध्ययन सुझाव — जे सोध्नुहोस्।',
  help: 'म यी काम गर्न सक्छु:\n• पोर्टल बुझाउने — अभ्यास, मक, नेगेटिभ मार्किङ र कटअफ कसरी काम गर्छ\n• तपाईंको परीक्षा खोज्ने — "म खरिदारको तयारी गर्न चाहन्छु" भन्नुहोस्, सही मक र विषय देखाउँछु\n• अध्ययन सुझाव — छोटा र व्यावहारिक\n• कहाँ के छ — Dashboard, Bookmarks, Old Papers, Notices…\nतलको सुझाव थिच्नुहोस् वा आफ्नै शब्दमा सोध्नुहोस्।',
  practice: '**अभ्यास** ट्याबमा जानुहोस् → आफ्नो परीक्षा छान्नुहोस् (जस्तै खरिदार) र विषय छान्नुहोस् → **Start practice** थिच्नुहोस्। हरेक सेटमा प्रश्नको क्रम र विकल्पको क्रम दुवै फेरबदल हुन्छ — दुई प्रयास कहिल्यै उस्तै हुँदैनन्। गलत उत्तर स्वतः **Bookmarks** मा सेभ हुन्छन्, अनि XP र streak ले निरन्तरता दिन्छ।',
  mock: '**Mock Exams** मा जानुहोस् → आफ्नो मक छान्नुहोस् → **Start mock exam**। पूरा लम्बाइ, समयसहित — समय सकिएपछि स्वतः बुझाउँछ, अनि परिणाम वास्तविक कटअफसँग तुलना गरिन्छ। सकिन्जेल उत्तर देखिँदैन — वास्तविक परीक्षा हल जस्तै। प्रश्न प्यालेटबाट जुनसुकै प्रश्नमा जान सक्नुहुन्छ।',
  negative: 'PSC पेपरमा २०% नेगेटिभ मार्किङ हुन्छ: गलत २-अङ्के प्रश्नमा −०.४, गलत १-अङ्केमा −०.२। छोडेको प्रश्नमा ०। लाइसेन्स पेपर (NNC / NHPC) मा नेगेटिभ मार्किङ छैन।',
  cutoff: 'परिणाम तपाईंको परीक्षाको वास्तविक कटअफसँग तुलना गरिन्छ: खरिदार / नासु ४५, शाखा अधिकृत ४५, TSC ५०, NRB सहायक ४०। प्रिलिम क्वालिफाइङ मात्र हो — फाइनल मेरिटमा जोडिँदैन।',
  tips: 'काम लाग्ने पाँच सुझाव:\n• २०-मिनेटका ब्लक, ५-मिनेट ब्रेक — Home को Focus Timer प्रयोग गर्नुहोस्।\n• विषय मिसाउनुहोस् — संविधान, GK, गणित र IQ आलोपालो।\n• अन्तरालमा दोहोर्‍याउनुहोस् — १ दिन, ३ दिन, अनि हप्तापछि।\n• पढेर मात्र होइन, टेस्ट गरेर — ५ प्रश्नको Quick Quiz दोहोर्‍याएर पढ्नुभन्दा राम्रो।\n• जितमा सक्नुहोस् — आउने विषयबाट सत्र सक्नुहोस्।',
  xp: 'हरेक प्रयासबाट XP (स्कोर × १०), दैनिक अभ्यासले streak, अनि ब्याजहरू — सबै **Dashboard** मा हेर्नुहोस्।',
  daily: '**Home** मा: 🔥 Daily Challenge (10 प्रश्न), ⚡ Quick Quiz (5), 🎲 Surprise me (10), ⏱️ Speed Round (10 प्रश्न · ६० सेकेन्ड) र 🏃 Mistake Marathon। सेटअप चाहिँदैन — थिच्नुहोस् मात्र।',
  thanks: 'तपाईंलाई स्वागत छ! तयारीका लागि शुभकामना। 🙏',
  fallback: 'यसबारे म निश्चित छैन — म यो पोर्टल मात्र चिन्छु। शङ्काका लागि **Discussion Hub**, विषयका प्रश्न खोज्न **Search** प्रयोग गर्नुहोस्, वा अभ्यास, मक, कटअफ वा खरिदार जस्तो परीक्षाबारे सोध्नुहोस्।',
  where: {
    dashboard: '**Dashboard** (नेभमा Stats) — XP, streak, प्रयासहरू, उत्कृष्ट मक र रेकर्ड — सबै यो डिभाइसमा सेभ।',
    bookmarks: '**Bookmarks & Mistakes** (नेभमा Saved) — गलत उत्तर स्वतः यहाँ आउँछन्; कुनै पनि प्रश्न bookmark गरेर पछि दोहोर्‍याउन सक्नुहुन्छ।',
    discuss: '**Discussion Hub** (नेभमा Discuss) — शङ्का सोध्नुहोस्, अरूलाई उत्तर दिनुहोस्। स्थानीय पूर्वावलोकन: थ्रेड यो डिभाइसमा मात्र रहन्छन्।',
    papers: '**Old Papers** — वास्तविक पुराना प्रश्नपत्र; १३३ वटा ट्रान्स्क्राइब गरिएका प्रश्न अभ्यास गर्न मिल्छ, बाँकी स्रोत लिङ्कसहित स्क्यान गरिएका।',
    notices: '**Notices** — PSC, TSC, NRB लगायतका विज्ञापन। आवेदन गर्नुअघि आधिकारिक साइटमा पुष्टि गर्नुहोस्।',
    search: '**Search** बाट पूरै प्रश्न ब्याङ्कमा फुल-टेक्स्ट खोज गर्नुहोस्।',
    flashcards: '**Flashcards** — २० वटा र्‍यान्डम प्रश्न, उत्तर reveal गरेर हेर्ने। बसमा वा सुत्नुअघिको १० मिनेटका लागि उपयुक्त।',
    funfacts: '**Fun Facts** — प्रमाणित द्विभाषी तथ्य; Home मा दैनिक एउटा, अनि हरेक ५औँ अभ्यास प्रश्नपछि एउटा।',
    profile: '**Profile** — डेमो साइन-इन यहाँ छ। सबै कुरा यो डिभाइसमा मात्र सेभ हुन्छ।',
    contribute: '**Contribute** — समीक्षाका लागि प्रश्न पेस गर्नुहोस्। पहिलो पेस कहिल्यै तुरुन्त लाइभ हुँदैन; हरेक प्रश्न समीक्षा हुन्छ।',
  },
};
// Exam finder: specs only for the five prelims verified in data/exams.json
// (kharidar/nasu 50Q·45min·2 marks·pass 45; section-officer 100Q·90min·1 mark·pass 45;
// tsc-primary 50Q·60min·2 marks·pass 50; nrb-assistant 50Q·45min·2 marks·pass 40).
// Other exams point to the Exam Guide — no invented patterns.
const CHAT_EXAMS = [
  { id: 'kharidar', keys: ['kharidar', 'खरिदार'], name: { en: 'Kharidar', ne: 'खरिदार' }, spec: { q: 50, t: 45, m: 2, pass: 45 }, topics: ['Constitution & Governance', 'Office Management & Public Service', 'Current Affairs'] },
  { id: 'nasu', keys: ['nasu', 'nayab subba', 'nayab', 'नासु', 'नायब'], name: { en: 'Nayab Subba (NaSu)', ne: 'नायब सुब्बा (नासु)' }, spec: { q: 50, t: 45, m: 2, pass: 45 }, topics: ['Constitution & Governance', 'Office Management & Public Service', 'Current Affairs'] },
  { id: 'section-officer', keys: ['section officer', 'shakha adhikrit', 'शाखा अधिकृत'], name: { en: 'Section Officer', ne: 'शाखा अधिकृत' }, spec: { q: 100, t: 90, m: 1, pass: 45 }, topics: ['Constitution & Governance', 'Current Affairs', 'English'] },
  { id: 'tsc', keys: ['tsc', 'teacher', 'shikshak', 'शिक्षक'], name: { en: 'TSC (Teacher)', ne: 'शिक्षक सेवा (TSC)' }, spec: null, topics: ['Education & Pedagogy', 'Nepali Language', 'English'] },
  { id: 'nrb', keys: ['nrb', 'rastra bank', 'राष्ट्र बैंक'], name: { en: 'NRB', ne: 'नेपाल राष्ट्र बैंक (NRB)' }, spec: { q: 50, t: 45, m: 2, pass: 40 }, topics: ['Banking & Finance', 'Economy & Development', 'Current Affairs'] },
];
function chatTopicLine(topic, stats, ne){
  const n = stats && stats.topics ? stats.topics[topic] : 0;
  return n ? topic + ' (' + n.toLocaleString('en-US') + (ne ? ' प्रश्न' : ' Q') + ')' : topic;
}
// Pure: raw text + lang + stats -> {text, chips}. No DOM, no network.
function chatReply(raw, lang, stats){
  const ne = lang === 'ne';
  const L = ne ? CHAT_NE : CHAT_EN;
  const t = chatNorm(raw);
  const S = stats || { total: 0, topics: {} };
  const has = (...ws) => ws.some(w => t.includes(w));
  const word = w => new RegExp('(^| )' + w + '( |$)').test(t);
  if (!t) return { text: L.greeting, chips: L.chips };
  if (has('namaste', 'namaskar', 'नमस्ते') || word('hi') || word('hello') || word('hey') || word('hajur') || word('हजुर')) return { text: L.greeting, chips: L.chips };
  if (has('what can you do', 'who are you', 'help', 'के गर्न सक्छौ', 'मद्दत', 'about you', 'तपाईं को')) return { text: L.help, chips: L.chips };
  if (has('thank', 'धन्यवाद', 'dhanyabad')) return { text: L.thanks, chips: L.chips };
  // Where things are — checked BEFORE the fact guard: these keywords are
  // portal-specific nouns ("where is my dashboard") that can never be
  // syllabus facts, and the guard's "where is" pattern would swallow them.
  if (has('dashboard', 'ड्यासबोर्ड', 'stats', 'my progress', 'my score')) return { text: L.where.dashboard, chips: L.chips };
  if (has('bookmark', 'mistake', 'बुकमार्क', 'saved')) return { text: L.where.bookmarks, chips: L.chips };
  if (has('discuss', 'doubt', 'forum', 'छलफल', 'शङ्का')) return { text: L.where.discuss, chips: L.chips };
  if (has('old paper', 'previous year', 'past paper', 'पुराना प्रश्नपत्र', 'पुरानो पेपर')) return { text: L.where.papers, chips: L.chips };
  if (has('notice', 'vacancy', 'advertisement', 'विज्ञापन', 'सूचना', 'भ्याकेन्सी')) return { text: L.where.notices, chips: L.chips };
  if (has('search', 'खोज')) return { text: L.where.search, chips: L.chips };
  if (has('flashcard', 'फ्ल्यासकार्ड')) return { text: L.where.flashcards, chips: L.chips };
  if (has('fun fact', 'रोचक तथ्य')) return { text: L.where.funfacts, chips: L.chips };
  if (has('profile', 'sign in', 'login', 'प्रोफाइल', 'साइन इन')) return { text: L.where.profile, chips: L.chips };
  if (has('contribute', 'submit a question', 'योगदान')) return { text: L.where.contribute, chips: L.chips };
  // Portal-rule intents — also before the guard: "cutoff" / "negative" /
  // "mock" are portal nouns, never syllabus facts, and the answers restate
  // only the portal's own documented rules (never invented facts).
  if (has('cutoff', 'cut off', 'pass mark', 'कटअफ', 'उत्तीर्णाङ्क', 'पास मार्क')) return { text: L.cutoff, chips: L.chips };
  if (has('negative', 'नेगेटिभ')) return { text: L.negative, chips: L.chips };
  // 0. FACT GUARD — before every remaining intent. Never answer facts from memory.
  if (isFactualQuestion(t)) {
    const topic = chatTopicFor(t);
    const text = topic
      ? (ne ? 'म सम्झेर तथ्यात्मक उत्तर दिन्नँ — तथ्य अनुमान गर्दिनँ। 👉 **' + topic + '** अभ्यास गर्नुहोस् (' + (S.topics[topic] ? S.topics[topic].toLocaleString('en-US') + ' प्रश्न' : 'प्रश्नहरू') + ') — हरेक उत्तरसँग व्याख्या पाउनुहुन्छ।'
             : 'I don\'t answer factual questions from memory — I never invent exam facts. 👉 Practice **' + topic + '**' + (S.topics[topic] ? ' (' + S.topics[topic].toLocaleString('en-US') + ' questions)' : '') + ' — every answer comes with an explanation.')
      : (ne ? 'म सम्झेर तथ्यात्मक उत्तर दिन्नँ — तथ्य अनुमान गर्दिनँ। 👉 **Search** ट्याबमा त्यो विषय खोज्नुहोस् वा सम्बन्धित विषय अभ्यास गर्नुहोस् — हरेक उत्तरसँग व्याख्या पाउनुहुन्छ।'
            : 'I don\'t answer factual questions from memory — I never invent exam facts. 👉 Try the **Search** tab for that topic, or practice the related topic — every answer comes with an explanation.');
    return { text, chips: L.chips };
  }
  if (has('namaste', 'namaskar', 'नमस्ते') || word('hi') || word('hello') || word('hey') || word('hajur') || word('हजुर')) return { text: L.greeting, chips: L.chips };
  if (has('what can you do', 'who are you', 'help', 'के गर्न सक्छौ', 'मद्दत', 'about you', 'तपाईं को')) return { text: L.help, chips: L.chips };
  if (has('thank', 'धन्यवाद', 'dhanyabad')) return { text: L.thanks, chips: L.chips };
  // Exam finder — "I want to prepare for Kharidar" -> right exam, mock + topics.
  const exam = CHAT_EXAMS.find(e => e.keys.some(k => t.includes(k)));
  if (exam) {
    const nm = ne ? exam.name.ne : exam.name.en;
    const spec = exam.spec
      ? (ne ? ': ' + exam.spec.q + ' प्रश्न · ' + exam.spec.t + ' मिनेट · ' + exam.spec.m + ' अङ्क · पास ' + exam.spec.pass
             : ': ' + exam.spec.q + ' questions · ' + exam.spec.t + ' min · ' + exam.spec.m + ' marks each · pass ' + exam.spec.pass)
      : (ne ? ' (यसको ठ्याक्कै प्याटर्नका लागि Exam Guide हेर्नुहोस्)' : ' (see the Exam Guide for its exact pattern)');
    const topics = exam.topics.map(x => chatTopicLine(x, S, ne)).join(', ');
    const text = ne
      ? '**' + nm + '** को तयारी? **अभ्यास** मा गएर "' + nm + '" परीक्षा छान्नुहोस् — वा पूरा मक दिनुहोस्' + spec + '। धेरै सोधिने विषय: ' + topics + '। १० प्रश्नको अभ्यास सेटबाट सुरु गर्नुहोस्।'
      : 'Preparing for **' + nm + '**? Go to **Practice** and choose the "' + nm + '" exam — or run the full mock' + spec + '. High-yield topics: ' + topics + '. Start with a 10-question practice set.';
    return { text, chips: L.chips };
  }
  if (has('mock', 'मक')) return { text: L.mock, chips: L.chips };
  // Topic practice request — "practice constitution questions" etc.
  const topic = chatTopicFor(t);
  if (topic && has('practice', 'question', 'mock', 'prepare', 'preparation', 'tayari', 'तयारी', 'अभ्यास', 'प्रश्न')) {
    const n = S.topics[topic];
    const text = ne
      ? '**' + topic + '** अहिले नै अभ्यास गर्न सक्नुहुन्छ' + (n ? ' — ब्याङ्कमा ' + n.toLocaleString('en-US') + ' प्रश्न छन्' : '') + '। **अभ्यास** मा गएर विषय छान्नुहोस्। हरेक सेटमा प्रश्न र विकल्प फेरबदल हुन्छन्।'
      : 'You can practice **' + topic + '** right now' + (n ? ' — ' + n.toLocaleString('en-US') + ' questions in the bank' : '') + '. Go to **Practice**, pick the topic, and start. Every set shuffles questions and options.';
    return { text, chips: L.chips };
  }
  if (has('practice', 'अभ्यास', 'how do i start', 'getting started', 'कसरी सुरु', 'start practic')) return { text: L.practice, chips: L.chips };
  if (has('xp', 'streak', 'level', 'badge', 'ब्याज')) return { text: L.xp, chips: L.chips };
  if (has('daily challenge', 'speed round', 'quick quiz', 'surprise me', 'mistake marathon', 'डेली च्यालेन्ज')) return { text: L.daily, chips: L.chips };
  if (has('study tip', 'how to study', 'how should i study', 'अध्ययन', 'पढ्ने तरिका', 'tips for')) return { text: L.tips, chips: L.chips };
  return { text: L.fallback, chips: L.chips };
}
// History persistence (per device, like discussions).
function chatHistory(){ return lsGet(LS_CHAT, []); }
function saveChatHistory(h){ lsSet(LS_CHAT, (h || []).slice(-CHAT_MAX_MSGS)); }
function chatSend(text){
  const h = chatHistory();
  h.push({ role: 'user', text: String(text).slice(0, 500), t: nowIso() });
  const r = chatReply(text, lang, chatTopicStats());
  h.push({ role: 'bot', text: r.text, t: nowIso() });
  saveChatHistory(h);
  return r;
}
function sendChat(){
  const inp = document.getElementById('chat-input'); if (!inp) return;
  const v = (inp.value || '').trim(); if (!v) return;
  inp.value = '';
  const r = chatSend(v);
  renderChat(r);
}
function askChat(q){ const inp = document.getElementById('chat-input'); if (inp) inp.value = q; sendChat(); }
function clearChat(){ saveChatHistory([]); renderChat(); }
function renderChat(pending){
  const box = document.getElementById('chat-box'); if (!box) return;
  const ne = lang === 'ne';
  const L = ne ? CHAT_NE : CHAT_EN;
  const h = chatHistory();
  const msgs = h.length
    ? h.map(m => '<div class="chat-msg ' + (m.role === 'user' ? 'chat-user' : 'chat-bot') + '">' + (m.role === 'bot' ? '🤖 ' : '') + esc(m.text).replace(/\n/g, '<br>') + '</div>').join('')
    : '<div class="chat-msg chat-bot">🤖 ' + esc(L.welcome).replace(/\n/g, '<br>') + '</div>';
  const chips = (pending && pending.chips) || L.chips;
  box.innerHTML =
    '<p class="muted"><strong>' + esc(L.demo) + '</strong> ' + esc(L.demoText) + '</p>' +
    '<div class="card"><strong>🤖 ' + esc(L.helper) + '</strong><br><span class="muted">' + esc(L.helperText) + '</span></div>' +
    '<div class="chat-log" id="chat-log" role="log" aria-live="polite">' + msgs + '</div>' +
    '<div class="chat-chips">' + chips.map(c => '<button class="btn secondary chip" data-q="' + esc(c.q) + '" onclick="askChat(this.getAttribute(\'data-q\'))">' + esc(c.label) + '</button>').join('') + '</div>' +
    '<div class="chat-input-row"><input type="text" id="chat-input" maxlength="500" placeholder="' + esc(L.placeholder) + '" onkeydown="if(event.key===\'Enter\'){event.preventDefault();sendChat();}">' +
    '<button class="btn" onclick="sendChat()">' + esc(L.send) + '</button>' +
    '<button class="btn secondary" onclick="clearChat()">' + esc(L.clear) + '</button></div>';
  const log = document.getElementById('chat-log');
  if (log) log.scrollTop = log.scrollHeight;
}

/* ================= Feature 10 — Suggest a feature =================
   Same safety posture as Submit a Question: stored in localStorage only,
   shown in a public on-device list with upvotes, clearly labelled
   "Local preview — visible only on this device until the backend is connected."
   No network calls, nothing auto-published anywhere external.
   Spam guards: rate limit (5/hour, reused), min lengths, no links,
   no repeated-chars / ALL-CAPS, duplicate-title block, double-submit guard. */
const LS_SUGGEST = 'loksewa_suggestions_v1';
const SUG_CATS = [
  ['feature', 'New feature', 'नयाँ सुविधा'],
  ['topic', 'Topic request', 'विषय अनुरोध'],
  ['questions', 'Question set', 'प्रश्न सेट'],
  ['exam', 'New exam', 'नयाँ परीक्षा'],
  ['bug', 'Bug report', 'बग रिपोर्ट'],
  ['other', 'Other', 'अन्य'],
];
const SUG_EN = {
  demo: 'Local preview —', demoText: 'visible only on this device until the online backend is connected.',
  formTitle: 'Suggest a feature', title: 'Title', titlePh: 'e.g. Spaced-repetition reminders',
  desc: 'Description', descPh: 'What should it do, and why would it help aspirants? (min 20 characters)',
  cat: 'Category', submit: 'Submit suggestion', rateNote: 'Max 5 suggestions per hour per device.',
  listTitle: 'Community suggestions', by: 'by', upvote: 'Upvote', empty: 'No suggestions yet — be the first!',
  emptyBlurb: 'Ideas from aspirants shape what gets built next — tell us what would help your preparation.',
  emptyCta: 'Write a suggestion', seed: 'example',
  errTitle: 'Title is required.', errTitleShort: 'Title must be at least 8 characters.',
  errDesc: 'Description is required.', errDescShort: 'Description must be at least 20 characters — say what it should do and why.',
  errCat: 'Please pick a category.', errUrl: 'No links, please — describe the idea in words.',
  errRepeat: 'Please write normally (no repeated characters like "!!!!!").', errCaps: 'Please don\'t write in ALL CAPS.',
  errDup: 'This suggestion is already on the list — upvote it instead!',
  done: 'Thanks! Your suggestion is on the list below (this device only, until the backend is connected).',
};
const SUG_NE = {
  demo: 'स्थानीय पूर्वावलोकन —', demoText: 'ब्याकएन्ड अनलाइन नजोडिएसम्म यो डिभाइसमा मात्र देखिन्छ।',
  formTitle: 'सुविधा सुझाव दिनुहोस्', title: 'शीर्षक', titlePh: 'जस्तै: स्पेस्ड-रिपिटिसन रिमाइन्डर',
  desc: 'विवरण', descPh: 'यसले के गर्ने र परीक्षार्थीलाई किन सहयोगी हुन्छ? (कम्तीमा २० अक्षर)',
  cat: 'श्रेणी', submit: 'सुझाव पेस गर्नुहोस्', rateNote: 'प्रति डिभाइस प्रति घण्टा बढीमा ५ सुझाव।',
  listTitle: 'सामुदायिक सुझावहरू', by: '—', upvote: 'मत दिनुहोस्', empty: 'अझै कुनै सुझाव छैन — पहिलो बन्नुहोस्!',
  emptyBlurb: 'परीक्षार्थीका विचारले के बन्छ भन्ने तय गर्छ — तपाईंको तयारीलाई के सहयोगी हुन्छ भन्नुहोस्।',
  emptyCta: 'सुझाव लेख्नुहोस्', seed: 'उदाहरण',
  errTitle: 'शीर्षक आवश्यक छ।', errTitleShort: 'शीर्षक कम्तीमा ८ अक्षरको हुनुपर्छ।',
  errDesc: 'विवरण आवश्यक छ।', errDescShort: 'विवरण कम्तीमा २० अक्षरको हुनुपर्छ — के गर्ने र किन भन्नुहोस्।',
  errCat: 'श्रेणी छान्नुहोस्।', errUrl: 'लिङ्क नराख्नुहोस् — विचार शब्दमा वर्णन गर्नुहोस्।',
  errRepeat: 'सामान्य रूपमा लेख्नुहोस् (जस्तै "!!!!!" दोहोरिएको अक्षर नराख्नुहोस्)।', errCaps: 'सबै ठूलो अक्षरमा नलेख्नुहोस्।',
  errDup: 'यो सुझाव सूचीमा पहिले नै छ — मत दिनुहोस्!',
  done: 'धन्यवाद! तपाईंको सुझाव तलको सूचीमा छ (ब्याकएन्ड नजोडिएसम्म यो डिभाइसमा मात्र)।',
};
// Pure validation of a suggestion object. Returns {ok, errors[]}.
function validateSuggestion(d, lang){
  const L = lang === 'ne' ? SUG_NE : SUG_EN;
  const errors = [];
  const title = String(d.title || '').trim(), desc = String(d.description || '').trim();
  if (!title) errors.push(L.errTitle); else if (title.length < 8) errors.push(L.errTitleShort);
  if (!desc) errors.push(L.errDesc); else if (desc.length < 20) errors.push(L.errDescShort);
  if (!SUG_CATS.some(c => c[0] === d.category)) errors.push(L.errCat);
  if (hasUrl(title) || hasUrl(desc)) errors.push(L.errUrl);
  if (repeatedChars(title) || repeatedChars(desc)) errors.push(L.errRepeat);
  if (capsRatio(title) > 0.5) errors.push(L.errCaps);
  return { ok: errors.length === 0, errors };
}
function isDuplicateSuggestion(list, title){
  const n = normaliseText(title);
  return (list || []).some(s => normaliseText(s.title) === n);
}
function seedSuggestions(){
  const t = (id, category, title, description) => ({ id, category, title, description, by: 'Guest aspirant', at: '2026-10-31T08:00:00Z', upvotes: 0, voters: [], _seed: true });
  return [
    t('SUG-SEED-1', 'feature', 'Spaced-repetition reminders', 'A gentle nudge that resurfaces topics I keep getting wrong, on a 1-3-7 day schedule — so weak areas get revised automatically.'),
    t('SUG-SEED-2', 'exam', 'NEA (Nepal Electricity Authority) exam', 'NEA publishes technical + GK papers for its levels. A practice set for NEA aspirants would help engineering candidates.'),
    t('SUG-SEED-3', 'questions', 'Most-asked GK lightning round', 'A dedicated speed set of the most repeated PSC questions across 12 years of papers — the 80/20 facts for last-week revision.'),
  ];
}
function loadSuggestions(){
  const s = lsGet(LS_SUGGEST, null);
  if (s) return s;
  const seed = seedSuggestions();
  lsSet(LS_SUGGEST, seed);
  return seed;
}
function saveSuggestions(list){ lsSet(LS_SUGGEST, list); }
function voterId(){ return (typeof progress !== 'undefined' && progress.user_id) ? progress.user_id : 'guest'; }
function submitSuggestion(){
  const gv = id => { const el = document.getElementById(id); return el ? el.value : ''; };
  const err = document.getElementById('sug-error');
  const d = { title: gv('sug-title').trim(), description: gv('sug-desc').trim(), category: gv('sug-cat') };
  const { ok, errors } = validateSuggestion(d, lang);
  if (!ok) { if (err) err.innerHTML = '<ul>' + errors.map(e => '<li>' + esc(e) + '</li>').join('') + '</ul>'; return; }
  const list = loadSuggestions();
  if (isDuplicateSuggestion(list, d.title)) { if (err) err.textContent = (lang === 'ne' ? SUG_NE : SUG_EN).errDup; return; }
  // Rate limit: max 5 per hour per device (same rule as question submissions).
  const rl = rateLimitCheck(list.map(s => s.at).filter(Boolean).map(x => new Date(x).getTime()), Date.now());
  if (!rl.allowed) { if (err) err.textContent = B('Rate limit: 5 suggestions per hour. Please wait about ' + rl.minutesLeft + ' minute(s).','दर सीमा: प्रति घण्टा ५ सुझाव। करिब ' + rl.minutesLeft + ' मिनेट पर्खनुहोस्।'); return; }
  list.unshift({ id: uid('SUG'), category: d.category, title: d.title, description: d.description, by: currentUserName(), at: nowIso(), upvotes: 0, voters: [] });
  saveSuggestions(list);
  const done = document.getElementById('sug-done');
  if (done) { done.hidden = false; done.textContent = (lang === 'ne' ? SUG_NE : SUG_EN).done; }
  if (err) err.innerHTML = '';
  const te = document.getElementById('sug-title'), de = document.getElementById('sug-desc');
  if (te) te.value = ''; if (de) de.value = '';
  // Double-submit guard: disable until the form changes again.
  const btn = document.getElementById('sug-submit-btn');
  if (btn) btn.disabled = true;
  renderSuggest();
}
function upvoteSuggestion(id){
  const list = loadSuggestions();
  const s = list.find(x => x.id === id); if (!s) return;
  s.voters = s.voters || [];
  const v = voterId();
  const i = s.voters.indexOf(v);
  if (i >= 0) { s.voters.splice(i, 1); s.upvotes = Math.max(0, (s.upvotes || 1) - 1); }
  else { s.voters.push(v); s.upvotes = (s.upvotes || 0) + 1; }
  saveSuggestions(list);
  renderSuggest();
}
function renderSuggest(){
  const box = document.getElementById('suggest-box'); if (!box) return;
  const ne = lang === 'ne';
  const L = ne ? SUG_NE : SUG_EN;
  const list = loadSuggestions().slice().sort((a, b) => (b.upvotes || 0) - (a.upvotes || 0));
  const catLabel = c => { const f = SUG_CATS.find(x => x[0] === c); return f ? (ne ? f[2] : f[1]) : c; };
  const v = voterId();
  box.innerHTML =
    '<p class="muted"><strong>' + esc(L.demo) + '</strong> ' + esc(L.demoText) + '</p>' +
    '<div class="card"><h3>' + esc(L.formTitle) + '</h3>' +
    '<label for="sug-title">' + esc(L.title) + '</label><input type="text" id="sug-title" maxlength="120" placeholder="' + esc(L.titlePh) + '" oninput="var b=document.getElementById(\'sug-submit-btn\');if(b)b.disabled=false;">' +
    '<label for="sug-desc">' + esc(L.desc) + '</label><textarea id="sug-desc" rows="4" placeholder="' + esc(L.descPh) + '" oninput="var b=document.getElementById(\'sug-submit-btn\');if(b)b.disabled=false;"></textarea>' +
    '<label for="sug-cat">' + esc(L.cat) + '</label><select id="sug-cat">' + SUG_CATS.map(c => '<option value="' + c[0] + '">' + esc(ne ? c[2] : c[1]) + '</option>').join('') + '</select>' +
    '<p class="error-text" id="sug-error"></p>' +
    '<p class="pass" id="sug-done" hidden></p>' +
    '<p><button class="btn" id="sug-submit-btn" onclick="submitSuggestion()">' + esc(L.submit) + '</button> <span class="muted">' + esc(L.rateNote) + '</span></p></div>' +
    '<h3>' + esc(L.listTitle) + ' (' + list.length + ')</h3>' +
    (list.map(s =>
      '<div class="card"><div class="muted">' + esc(catLabel(s.category)) + ' · ' + esc(L.by) + ' ' + esc(s.by || 'Guest') + ' · ' + esc((s.at || '').slice(0, 10)) + (s._seed ? ' · 🌱 ' + esc(L.seed) : '') + '</div>' +
      '<h3 style="margin:6px 0">' + esc(s.title) + '</h3><p>' + esc(s.description) + '</p>' +
      '<p><button class="btn secondary" onclick="upvoteSuggestion(\'' + s.id + '\')">' + ((s.voters || []).includes(v) ? '▲' : '△') + ' ' + esc(L.upvote) + ' (' + (s.upvotes || 0) + ')</button></p></div>'
    ).join('') || emptyState('💡', L.empty, L.emptyBlurb, L.emptyCta, "document.getElementById('sug-title').focus()"));
}

document.addEventListener('DOMContentLoaded', ()=>{
  document.querySelectorAll('nav button[data-view]').forEach(b=>b.addEventListener('click',()=>showView(b.dataset.view)));
  // Nav "More" dropdown: click toggles, Escape closes, outside click closes.
  (function(){
    var btn=document.getElementById('nav-more-btn'), menu=document.getElementById('nav-more-menu');
    if(!btn||!menu) return;
    function setOpen(o){ btn.setAttribute('aria-expanded',o?'true':'false'); btn.classList.toggle('open',o); if(o){menu.removeAttribute('hidden');}else{menu.setAttribute('hidden','');} }
    btn.addEventListener('click',function(e){ e.stopPropagation(); setOpen(menu.hasAttribute('hidden')); });
    document.addEventListener('click',function(e){ if(!menu.hasAttribute('hidden')&&!e.target.closest('.nav-dropdown')) setOpen(false); });
    document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!menu.hasAttribute('hidden')){ setOpen(false); btn.focus(); } });
    menu.querySelectorAll('button[data-view]').forEach(function(b){ b.addEventListener('click',function(){ setOpen(false); }); });
  })();
  // Restore the saved theme (light is the default when nothing is saved).
  try{ const saved=localStorage.getItem(THEME_KEY); applyTheme(saved==='dark'?'dark':'light'); }catch(e){ applyTheme('light'); }
  const th=document.getElementById('theme-toggle'); if(th) th.addEventListener('click',toggleTheme);
  const lg=document.getElementById('lang-toggle'); if(lg){ lg.textContent = lang==='ne'?'NE · नेपाली':'EN · English'; lg.addEventListener('click',()=>setLang(lang==='ne'?'en':'ne')); }
  const topics=new Set(); // filled after load
  loadData().then(()=>{
    // Search keeps the global topic list (it is topic-only, no exam involved).
    // The Practice topic list is owned by updatePracticeTopics() and is
    // rebuilt per exam — do not overwrite it here with the global list.
    const st=document.getElementById('search-topic');
    const list=[...new Set(QUESTIONS.map(q=>q.topic))].sort();
    if(st) st.innerHTML='<option value="">All topics</option>'+list.map(t=>`<option>${esc(t)}</option>`).join('');
  });
});

/* ================================================================
   Analytics views 1–5 (2026-10-31): all frontend-only, localStorage
   backed, zero dependencies.
     1. Syllabus Coverage Tracker     → view-coverage / renderCoverage
     2. Printable mock + OMR sheet    → view-print    / renderPrint
     3. Deadline-driven study planner → view-planner  / renderPlanner
     4. Negative-marking guess coach  → view-coach    / renderCoach
     5. PYQ heatmap                   → view-pyq      / renderPYQ
   User-facing strings are bilingual: static headings use the inline
   "EN — NE" pattern; dynamic lines go through B(en, ne), which follows
   the lang toggle. Anything estimated is labelled as an estimate.
   ================================================================ */
// Bilingual line picker for dynamic strings.
function B(en, ne){ return lang==='ne' ? ne : en; }
function examName(e){ return (lang==='ne' && e && e.name_ne) ? e.name_ne : (e ? (e.name||'') : ''); }
function fmt1(n){ return String(Math.round(n*10)/10); }
// Flag the transcribed real Previous Year questions (previous-year-*.json
// tag source 'Previous Year — …') so the heatmap and the weight estimates
// can treat them as ground truth. Called once in loadData.
function markPyqFlags(){ QUESTIONS.forEach(q=>{ if(q.source && q.source.indexOf('Previous Year')===0) q._pyq=true; }); }
// How many bank questions carry each topic for one exam.
function topicsForExam(examId, bank){
  const counts={}; (bank||QUESTIONS).forEach(q=>{
    if((q.exam||[]).indexOf(examId)>=0){ const t=q.topic||'General'; counts[t]=(counts[t]||0)+1; }
  });
  return counts;
}
// Question topic → syllabus-section keywords. A topic maps to a syllabus
// section when any keyword appears in the section text (case-insensitive).
const TOPIC_SYLLABUS_KEYS={
  'Constitution & Governance':['constitution','governance','public administration','civil service'],
  'Nepal History':['history'], 'Nepal Geography':['geography'],
  'Culture & Society':['culture','society','social'],
  'Current Affairs':['current affairs'], 'GK & Current Affairs':['current affairs','general knowledge'],
  'Economy & Development':['econom','development','planning'], 'Economy':['econom'],
  'Banking & Finance':['bank','finance','nrb','management','accounting'],
  'Office Management & Public Service':['office','bost','record management','public management'],
  'Maths & Numerical':['math','numerical','aptitude','mental ability'], 'Mathematics':['math'],
  'IQ & Reasoning':['reasoning','mental ability','aptitude','mental agility','intelligence'],
  'IQ':['iq','mental agility'], 'English':['english'],
  'Nepali Language':['nepali'], 'Computer & ICT':['computer','ict','information technology'],
  'Science & Tech':['science','technology'], 'Physics':['physics'], 'Chemistry':['chemistry'],
  'Biology':['biology','zoology','botany','zoo'],
  'Education & Pedagogy':['education','pedagogy','teaching','curriculum'],
  'Law':['law','legal','constitution'], 'Health/Technical basics':['health','technical','nursing','medical'],
  'Foreign Service & Diplomacy':['foreign','diplomacy','international'],
  'Engineering Drawing':['engineering drawing','drawing']
};
function mapTopicToSyllabus(topic, sections){
  const keys=TOPIC_SYLLABUS_KEYS[topic]||[String(topic).toLowerCase()];
  const low=sections.map(s=>String(s).toLowerCase());
  for(let i=0;i<low.length;i++){ if(keys.some(k=>low[i].indexOf(k)>=0)) return i; }
  return -1;
}
// Paper-pattern section labels → question topics. Used to turn the
// prelim.breakdown string ("GK 30 Q + Basic Office Skills (BOST) 20 Q")
// into per-topic weights.
const BREAKDOWN_GROUPS={
  'general mental ability':['IQ & Reasoning','IQ'], 'mental agility':['IQ & Reasoning','IQ'],
  'general awareness':['Current Affairs','Nepal History','Nepal Geography','Culture & Society','Science & Tech','Economy & Development','Economy','Constitution & Governance'],
  'basic office skills':['Office Management & Public Service'], 'bost':['Office Management & Public Service'],
  'aptitude':['IQ & Reasoning','IQ','Maths & Numerical','Mathematics'],
  'computer gk':['Computer & ICT'], 'computer':['Computer & ICT'], 'ict':['Computer & ICT'],
  'mathematics':['Maths & Numerical','Mathematics'], 'maths':['Maths & Numerical','Mathematics'],
  'physics':['Physics'], 'chemistry':['Chemistry'],
  'zoology':['Biology'], 'botany':['Biology'], 'biology':['Biology'], 'zoo':['Biology'],
  'english':['English'], 'nepali':['Nepali Language'],
  'education':['Education & Pedagogy'], 'constitution':['Constitution & Governance'],
  'management':['Banking & Finance'], 'accounting':['Banking & Finance'],
  'economics':['Economy & Development','Economy'], 'banking':['Banking & Finance'],
  'gk':['Current Affairs','Nepal History','Nepal Geography','Culture & Society','Science & Tech','Economy & Development','Economy','Constitution & Governance']
};
function breakdownLabelTopics(label){
  const low=String(label).toLowerCase();
  const keys=Object.keys(BREAKDOWN_GROUPS).sort((a,b)=>b.length-a.length);
  for(const k of keys){ if(low.indexOf(k)>=0) return BREAKDOWN_GROUPS[k]; }
  return [];
}
// Estimate per-topic weightage for an exam from its prelim.breakdown text.
// Only trusted when the numbers in it sum to the paper's question count
// (truncated or prose breakdowns are rejected → null, no invented figures).
function parseBreakdownWeights(exam){
  const p=exam && exam.prelim; const bd=p && p.breakdown;
  if(!bd || !p.questions) return null;
  const parts=String(bd).split('+').map(s=>s.trim()).filter(Boolean);
  if(!parts.length) return null;
  const items=[];
  for(const part of parts){
    const m=part.match(/(\d+(?:\.\d+)?)\s*(%|percent)?/i);
    if(!m) return null;
    items.push({label:part, n:parseFloat(m[1]), pct:!!m[2]});
  }
  const usePct=items.every(i=>i.pct);
  const sum=items.reduce((a,i)=>a+i.n,0);
  if(usePct ? Math.abs(sum-100)>3 : Math.abs(sum-p.questions)>2) return null;
  const weights={}; let unmapped=0;
  for(const it of items){
    const share=usePct?it.n:(it.n/p.questions*100);
    const topics=breakdownLabelTopics(it.label);
    if(!topics.length){ unmapped+=share; continue; }
    const per=share/topics.length;
    topics.forEach(t=>{ weights[t]=(weights[t]||0)+per; });
  }
  if(!Object.keys(weights).length) return null;
  return {weights, unmapped, source:'breakdown'};
}
// Topic shares among the transcribed real PYQs for one exam.
function pyqTopicShares(examId, bank){
  const qs=(bank||QUESTIONS).filter(q=>q._pyq && (q.exam||[]).indexOf(examId)>=0);
  const counts={}; qs.forEach(q=>{ const t=q.topic||'General'; counts[t]=(counts[t]||0)+1; });
  const shares={}; Object.keys(counts).forEach(t=>{ shares[t]=counts[t]/qs.length*100; });
  return {shares, n:qs.length};
}
// Estimated topic weights for an exam: parsed paper pattern first, else the
// transcribed-PYQ shares (only with ≥20 PYQs), else nothing.
function examTopicWeights(examId, examObj, bank){
  const parsed=parseBreakdownWeights(examObj||examById(examId));
  if(parsed) return parsed;
  const pyq=pyqTopicShares(examId, bank);
  if(pyq.n>=20) return {weights:pyq.shares, unmapped:0, source:'pyq'};
  return {weights:null, unmapped:0, source:null};
}
// Per-topic practice stats from attempts that recorded qdetail (finishAttempt
// stores it since this feature landed; older attempts contribute only to the
// attempt-level totals below).
function practiceTopicStats(examId, attempts){
  const stats={};
  (attempts||[]).forEach(a=>{
    if(a.exam!==examId || !Array.isArray(a.qdetail)) return;
    a.qdetail.forEach(d=>{
      const t=d.t||'General';
      const s=stats[t]=stats[t]||{total:0,correct:0,wrong:0,skipped:0};
      s.total++;
      if(d.c===1) s.correct++; else if(d.c===-1) s.skipped++; else s.wrong++;
    });
  });
  return stats;
}
function attemptLevelTotals(examId, attempts){
  const t={attempts:0,total:0,correct:0,wrong:0,skipped:0,score:0,max:0};
  (attempts||[]).forEach(a=>{
    if(a.exam!==examId) return;
    t.attempts++; t.total+=a.total||0; t.correct+=a.correct||0; t.wrong+=a.wrong||0;
    t.skipped+=a.skipped||0; t.score+=a.score||0; t.max+=a.max||0;
  });
  return t;
}
// Expected marks per 1-mark question for three guess strategies under a
// negative-marking rate r (per-mark). Honest maths, not encouragement.
function guessEV(negRate){
  const r=negRate||0;
  return { blind:0.25-0.75*r, elim1:1/3-(2/3)*r, elim2:0.5-0.5*r };
}
function evVerdict(v){ return v>0.005?B('✅ worth it','✅ लायक'):v<-0.005?B('❌ avoid','❌ नगर्नुहोस्'):B('➖ neutral','➖ तटस्थ'); }
// "Marks left on the table" for one exam: negative-marking deductions on
// wrong guesses (exact, from history) vs skips in strong topics (a labelled
// heuristic: topic accuracy ≥70% on ≥5 attempted questions is the proxy for
// "likely knew it").
function coachStats(examId, attempts, examObj){
  const tot=attemptLevelTotals(examId, attempts);
  const perTopic=practiceTopicStats(examId, attempts);
  const negRate=(examObj && examObj.prelim) ? mockNegRate(examObj.prelim) : 0;
  const negUnknown=!(examObj && examObj.prelim) || examObj.prelim.negative==null;
  const avgMarks=tot.total?tot.max/tot.total:0;
  const negLost=tot.wrong*avgMarks*negRate;
  let strongSkips=0; const strongTopics=[];
  Object.keys(perTopic).forEach(t=>{
    const s=perTopic[t]; const att=s.correct+s.wrong;
    if(att>=5 && s.correct/att>=0.7 && s.skipped>0){ strongSkips+=s.skipped; strongTopics.push(t); }
  });
  const estSkipLoss=strongSkips*avgMarks*0.7;
  return Object.assign({}, tot, {avgMarks, negRate, negUnknown, negLost, strongSkips, strongTopics, estSkipLoss, ev:guessEV(negRate), perTopic});
}
function coachAdvice(st, exam){
  const A=[]; const negPct=Math.round(st.negRate*100);
  if(!st.attempts){
    A.push({en:'Attempt a practice set or mock for this exam first — the coach learns from your history.', ne:'पहिले यो परीक्षाका लागि अभ्यास वा मक दिनुहोस् — कोच तपाईंको इतिहासबाट सिक्छ।'});
    return A;
  }
  if(st.negUnknown){
    A.push({en:'Negative marking for this exam is unverified in our data — check the vacancy notice before trusting any guess maths below. When in doubt, skip blind guesses.', ne:'यो परीक्षाको नेगेटिभ मार्किङ हाम्रो डाटामा अपुष्ट छ — तलको अनुमान-गणितमा भर पर्नुअघि विज्ञापन हेर्नुहोस्। शङ्का लागे अन्धाधुन्ध अनुमान नगर्नुहोस्।'});
  }else if(st.negRate===0){
    A.push({en:'No negative marking in this exam — never leave a question blank. A guess can only help.', ne:'यो परीक्षामा नेगेटिभ मार्किङ छैन — कुनै प्रश्न खाली नछोड्नुहोस्। अनुमानले फाइदा मात्र गर्छ।'});
  }else if(st.ev.blind>0.005){
    A.push({en:`With ${negPct}% negative marking, a pure 1-in-4 guess still gains about +${st.ev.blind.toFixed(2)} marks per mark on average — but one bad guess costs ${(st.negRate*(st.avgMarks||1)).toFixed(2)} marks on a typical question here. Only guess blind when you are behind on time; otherwise eliminate at least one option first (expected +${st.ev.elim1.toFixed(2)} per mark).`, ne:`${negPct}% नेगेटिभ मार्किङमा शुद्ध १-मा-४ अनुमानले औसतमा प्रति अङ्क +${st.ev.blind.toFixed(2)} अङ्क फाइदा दिन्छ — तर एउटा गलत अनुमानले यहाँको सामान्य प्रश्नमा ${(st.negRate*(st.avgMarks||1)).toFixed(2)} अङ्क खर्च गर्छ। समयले पछाडि पार्दा मात्र अन्धाधुन्ध अनुमान गर्नुहोस्; नत्र कम्तीमा एउटा विकल्प हटाएर अनुमान गर्नुहोस् (अपेक्षित +${st.ev.elim1.toFixed(2)} प्रति अङ्क)।`});
  }else{
    A.push({en:`With ${negPct}% negative marking, blind 1-in-4 guesses lose marks on average (${st.ev.blind.toFixed(2)} per mark). Never guess blind — eliminate at least two options first (expected +${st.ev.elim2.toFixed(2)} per mark).`, ne:`${negPct}% नेगेटिभ मार्किङमा अन्धाधुन्ध १-मा-४ अनुमानले औसतमा अङ्क गुमाउँछ (${st.ev.blind.toFixed(2)} प्रति अङ्क)। कहिल्यै अन्धाधुन्ध अनुमान नगर्नुहोस् — कम्तीमा दुई विकल्प हटाएर मात्र अनुमान गर्नुहोस् (अपेक्षित +${st.ev.elim2.toFixed(2)} प्रति अङ्क)।`});
  }
  if(st.negLost>0.05) A.push({en:`Wrong guesses have cost you ${fmt1(st.negLost)} marks to negative marking across ${st.attempts} attempt(s). When torn between two options, mark the question and move on instead of forcing an answer.`, ne:`गलत अनुमानका कारण ${st.attempts} प्रयासमा नेगेटिभ मार्किङले तपाईंको ${fmt1(st.negLost)} अङ्क खाएको छ। दुई विकल्पबीच अलमलिँदा जबरजस्ती उत्तर नदिनुहोस् — प्रश्न चिह्न लगाएर अगाडि बढ्नुहोस्।`});
  if(st.strongSkips>0) A.push({en:`You skipped ${st.strongSkips} question(s) in topics where you score 70%+ — questions you likely knew. Heuristic estimate: ~${fmt1(st.estSkipLoss)} marks left on the table. Trust your preparation on strong topics.`, ne:`७०%+ स्कोर गर्ने विषयहरूमा तपाईंले ${st.strongSkips} प्रश्न छोड्नुभयो — जानेका प्रश्नहरू हुन सक्थे। अनुमानित हिसाब: ~${fmt1(st.estSkipLoss)} अङ्क टेबलमै छोडियो। बलिया विषयमा आफ्नो तयारीमा विश्वास गर्नुहोस्।`});
  const weak=Object.keys(st.perTopic).map(t=>({t, s:st.perTopic[t]}))
    .filter(x=>x.s.correct+x.s.wrong>=5)
    .sort((a,b)=>(a.s.correct/(a.s.correct+a.s.wrong))-(b.s.correct/(b.s.correct+b.s.wrong)))[0];
  if(weak) A.push({en:`Your weakest drilled topic is "${weak.t}" — drill it before your next mock.`, ne:`तपाईंको सबैभन्दा कमजोर अभ्यास गरिएको विषय "${weak.t}" हो — अर्को मकअघि यसको अभ्यास गर्नुहोस्।`, topic:weak.t});
  return A;
}
// Drill a topic for a specific exam: point the Practice view at that exam,
// then start the topic (startPracticeTopic guards empty exam+topic combos).
function drillTopic(examId, topic){
  const ps=document.getElementById('practice-exam');
  if(ps && examId) ps.value=examId;
  startPracticeTopic(topic);
}

/* ---------- Feature 1: Syllabus Coverage Tracker ---------- */
function renderCoverage(){
  const box=document.getElementById('cov-box'); if(!box) return;
  if(!dataReady){ box.innerHTML=skelBlock(2); return; }
  const examId=(document.getElementById('cov-exam')||{}).value||'';
  const e=examById(examId);
  if(!e){ box.innerHTML=emptyState('🎯', B('Choose an exam to see your coverage','कभरेज हेर्न परीक्षा छान्नुहोस्'), B('Pick an exam from the dropdown above — the tracker maps every syllabus section to bank topics and your own practice.','माथिको ड्रपडाउनबाट परीक्षा छान्नुहोस् — ट्र्याकरले हरेक पाठ्यक्रम खण्डलाई बैंक विषय र तपाईंको अभ्याससँग जोड्छ।')); return; }
  const counts=topicsForExam(examId);
  const topics=Object.keys(counts).sort((a,b)=>counts[b]-counts[a]);
  if(!topics.length){ box.innerHTML=`<div class="card"><h3>${esc(examName(e))}</h3></div>`+emptyState('📚', B('No questions tagged for this exam yet','यस परीक्षाका लागि अझै प्रश्न ट्याग गरिएको छैन'), B('The question bank has no questions tagged for this exam, so there is nothing to map yet. Practise the mixed bank in the meantime.','प्रश्न बैंकमा यस परीक्षाका लागि ट्याग गरिएका प्रश्न छैनन्, त्यसैले नक्सा बनाउन केही छैन। यसबीच मिश्रित बैंक अभ्यास गर्नुहोस्।'), B('Practise the mixed bank','मिश्रित बैंक अभ्यास गर्नुहोस्'), "showView('practice')"); return; }
  const stats=practiceTopicStats(examId, progress.attempts);
  const w=examTopicWeights(examId, e);
  const wLabel=w.source==='breakdown'?B('est. · paper pattern','अनुमान · पेपर ढाँचा'):w.source==='pyq'?B('est. · PYQ shares','अनुमान · PYQ हिस्सा'):'—';
  const totalBank=topics.reduce((a,t)=>a+counts[t],0);
  const touched=topics.filter(t=>(stats[t]||{total:0}).total>0);
  let h=`<div class="card"><h3>${esc(examName(e))}</h3>
  <p><span class="tag">${B('Topics touched','छोइएका विषयहरू')}: ${touched.length}/${topics.length}</span> <span class="tag">${B('Bank','बैंक')}: ${totalBank.toLocaleString()} ${B('questions','प्रश्नहरू')}</span> <span class="tag">${B('Weight','भार')}: ${wLabel}</span></p>`;
  if(!progress.attempts.some(a=>a.exam===examId && a.qdetail)) h+=`<p class="muted">ℹ️ ${B('Per-topic practice counts cover attempts recorded after this analytics update — older attempts still count in your totals.','प्रति-विषय अभ्यास गणनामा यो एनालिटिक्स अपडेटपछिका प्रयासहरू मात्र पर्छन् — पुराना प्रयासहरू तपाईंको कुल योगमा अझै गनिन्छन्।')}</p>`;
  h+=`<table class="tbl"><tr><th>${B('Topic','विषय')}</th><th>${B('Bank Qs','बैंक प्रश्न')}</th><th>${B('Practised','अभ्यास')}</th><th>${B('Accuracy','शुद्धता')}</th><th>${B('Est. weight','अनुमानित भार')}</th><th>${B('Status','स्थिति')}</th></tr>`;
  for(const t of topics){
    const s=stats[t]||{total:0,correct:0,wrong:0,skipped:0};
    const att=s.correct+s.wrong;
    const acc=att?Math.round(s.correct/att*100):null;
    const wt=w.weights&&w.weights[t]!=null?w.weights[t]:null;
    h+=`<tr><td>${esc(t)}</td><td>${counts[t].toLocaleString()}</td><td>${s.total}</td><td>${acc==null?'—':acc+'%'}</td><td>${wt==null?'—':wt.toFixed(1)+'%'}</td><td>${s.total?`✅ ${B('touched','छोइएको')}`:`<span class="tag">🆕 ${B('untouched','नछोइएको')}</span> <button class="btn secondary" onclick="drillTopic('${esc(examId)}','${esc(t)}')">${B('Practice','अभ्यास')}</button>`}</td></tr>`;
  }
  if(w.unmapped>0.5) h+=`<tr><td class="muted">${B('Other / unmapped pattern sections','अन्य / नमिलेका ढाँचा खण्डहरू')}</td><td>—</td><td>—</td><td>—</td><td>${w.unmapped.toFixed(1)}%</td><td><span class="tag">${B('est.','अनुमान')}</span></td></tr>`;
  h+=`</table></div>`;
  const sections=e.syllabus||[];
  if(sections.length){
    h+=`<div class="card"><h3>${B('Syllabus map','पाठ्यक्रम नक्सा')}</h3><p class="muted">${B('Which bank topics each syllabus section draws from (keyword-matched, approximate).','प्रत्येक पाठ्यक्रम खण्डले कुन बैंक विषयहरूबाट प्रश्न लिन्छ (किवर्ड मिलान, अनुमानित)।')}</p>`;
    sections.forEach((sec,idx)=>{
      const mapped=topics.filter(t=>mapTopicToSyllabus(t,sections)===idx);
      const doneN=mapped.filter(t=>(stats[t]||{total:0}).total>0).length;
      h+=`<p><strong>${esc(sec)}</strong><br><span class="muted">${mapped.length?mapped.map(esc).join(' · '):B('no bank topics matched','कुनै बैंक विषय मिलेन')} — ${doneN}/${mapped.length} ${B('touched','छोइएको')}</span></p>`;
    });
    h+=`</div>`;
  }
  box.innerHTML=h;
}

/* ---------- Feature 2: Printable mock papers with OMR sheet ---------- */
let printPaper=null; // {exam, qs:[shuffled questions], short, pool}
function renderPrint(){
  const box=document.getElementById('prt-box'); if(!box) return;
  if(!dataReady){ box.innerHTML=skelBlock(1); return; }
  const examId=(document.getElementById('prt-exam')||{}).value||'';
  if(printPaper && printPaper.exam!==examId) printPaper=null; // exam changed → old paper is stale
  box.innerHTML=printPaper ? renderPrintPaperHtml()
    : `<p class="muted">${B('Generates a paper-exact prelim: real question count, marks and time from the Exam Guide pattern, options shuffled. Print it, fill the OMR sheet, then check the answer key (last page).','पेपर-अनुरूप प्रिलिम बनाउँछ: परीक्षा गाइड ढाँचाअनुसार वास्तविक प्रश्न सङ्ख्या, अङ्क र समय, विकल्पहरू फेरबदल सहित। प्रिन्ट गर्नुहोस्, OMR पाना भर्नुहोस्, अनि उत्तर कुञ्जी (अन्तिम पाना) हेर्नुहोस्।')}</p>
       <button class="btn" onclick="generatePrintPaper()">${B('📝 Generate paper','📝 पेपर बनाउनुहोस्')}</button>`;
}
function generatePrintPaper(){
  const examId=(document.getElementById('prt-exam')||{}).value||'';
  const e=examById(examId);
  if(!e||!e.prelim) return;
  const pool=QUESTIONS.filter(q=>(q.exam||[]).indexOf(examId)>=0);
  const n=e.prelim.questions;
  const qs=shuffle(pool).slice(0,n).map(q=>shuffleOptions(q)); // shuffled options; key uses the remapped answer
  printPaper={exam:examId, qs, short:pool.length<n, pool:pool.length};
  renderPrint();
  window.scrollTo({top:0, behavior:'auto'});
}
function renderPrintPaperHtml(){
  const e=examById(printPaper.exam); const p=e.prelim; const qs=printPaper.qs;
  const letters=['A','B','C','D'];
  const negTxt=p.negative==null?B('unverified — check the notice','अपुष्ट — सूचना हेर्नुहोस्'):p.negative===0?B('none','छैन'):Math.round(p.negative*100)+'%';
  let h=`<div class="paper"><div class="no-print" style="margin-bottom:10px"><button class="btn" onclick="window.print()">${B('🖨️ Print paper','🖨️ पेपर प्रिन्ट गर्नुहोस्')}</button> <button class="btn secondary" onclick="printPaper=null;renderPrint()">${B('↺ New paper','↺ नयाँ पेपर')}</button></div>`;
  if(printPaper.short) h+=`<p class="no-print" style="border:1px solid #ea580c;border-radius:8px;padding:10px">⚠️ ${B(`The bank has only ${printPaper.pool} questions tagged for this exam — this paper is shortened to ${qs.length} questions.`,'यस परीक्षाका लागि बैंकमा जम्मा '+printPaper.pool+' प्रश्न मात्र छन् — यो पेपर '+qs.length+' प्रश्नमा छोट्याइएको छ।')}</p>`;
  h+=`<div class="paper-head"><h2>${esc(examName(e))} — ${B('Prelim Practice Paper','प्रिलिम अभ्यास पेपर')}</h2>
  <p><strong>${B('Questions','प्रश्नहरू')}:</strong> ${qs.length} × ${p.marksPerQ} ${B('marks','अङ्क')} = ${qs.length*p.marksPerQ} &nbsp;·&nbsp; <strong>${B('Time','समय')}:</strong> ${p.timeMin==null?B('unverified','अपुष्ट'):p.timeMin+' '+B('min','मिनेट')} &nbsp;·&nbsp; <strong>${B('Pass','उत्तीर्ण')}:</strong> ${p.pass}/${p.total} &nbsp;·&nbsp; <strong>${B('Negative marking','नेगेटिभ मार्किङ')}:</strong> ${negTxt}</p>
  <p>${B('Name','नाम')}: ____________________ &nbsp; ${B('Date','मिति')}: __________ &nbsp; ${B('Score','स्कोर')}: ______ / ${qs.length*p.marksPerQ}</p>
  <p class="muted">${B('Instructions: choose the single best answer for each question. Fill the OMR sheet as you go — one bubble per question.','निर्देशन: प्रत्येक प्रश्नको सबैभन्दा उपयुक्त एउटा उत्तर छान्नुहोस्। जाँदै गर्दा OMR पाना भर्नुहोस् — प्रति प्रश्न एउटा गोला।')}</p></div>
  <ol class="paper-qs">`+qs.map(q=>`<li><p>${esc(qText(q))}</p><ol type="A" class="paper-opts">${qOpts(q).map(o=>`<li>${esc(o)}</li>`).join('')}</ol></li>`).join('')+`</ol>
  <div class="omr-page"><h3>${B('OMR Answer Sheet','OMR उत्तर पाना')}</h3><p class="muted">${B('Fill one bubble per question. Do not tick more than one.','प्रत्येक प्रश्नका लागि एउटा गोला भर्नुहोस्। एउटाभन्दा बढी नछुनुहोस्।')}</p>
  <div class="omr-grid">`+qs.map((q,i)=>`<div class="omr-row"><span class="omr-n">${i+1}</span>${letters.map(L=>`<span class="bubble" title="${L}"></span>`).join('')}</div>`).join('')+`</div></div>
  <div class="key-page"><h3>${B('Answer Key — for the checker, not the candidate','उत्तर कुञ्जी — जाँचकर्ताका लागि, परीक्षार्थीका लागि होइन')}</h3>
  <table class="tbl key-table"><tr><th>#</th><th>${B('Answer','उत्तर')}</th><th>${B('Question ID','प्रश्न ID')}</th></tr>`+qs.map((q,i)=>`<tr><td>${i+1}</td><td><strong>${letters[q.answer]||'?'}</strong></td><td>${esc(q.id||'')}</td></tr>`).join('')+`</table></div></div>`;
  return h;
}

/* ---------- Feature 3: Deadline-driven study planner ---------- */
const PLANS_KEY='loksewa_plans_v1';
function loadPlans(){ try{ const p=JSON.parse(localStorage.getItem(PLANS_KEY)||'null'); return (p&&typeof p==='object')?p:{}; }catch(e){ return {}; } }
function savePlans(p){ try{ localStorage.setItem(PLANS_KEY, JSON.stringify(p)); }catch(e){} }
// Notices with verified deadlines, mapped to the exam they target. Notices
// whose exam has no prelim/question bank (or no mapping) are excluded.
const NOTICE_EXAM={
  'lumbini-health-8-2083':'health', 'nepal-police-asi-oa-2083':'police',
  'tsc-nimavi-2082':'tsc-lower-secondary', 'tsc-mavi-2082':'tsc-secondary',
  'nrb-contract-2083':'nrb-assistant', 'tsc-licence-2082-83':'tsc-license'
};
function planNotices(){
  return NOTICES.filter(n=>n.close_date && NOTICE_EXAM[n.id] && examById(NOTICE_EXAM[n.id]))
    .sort((a,b)=>a.close_date<b.close_date?-1:1);
}
function daysUntil(deadline, today){
  const t=today||new Date().toISOString().slice(0,10);
  if(!deadline) return 0;
  return Math.max(0, Math.ceil((new Date(deadline+'T00:00:00Z')-new Date(t+'T00:00:00Z'))/864e5));
}
// Build a daily plan: topics weighted by the paper's estimated pattern
// (paper pattern → PYQ shares → bank mix), split across daysLeft days.
function buildStudyPlan(examId, deadline, dailyTarget, bank){
  const counts=topicsForExam(examId, bank);
  const topics=Object.keys(counts).sort((a,b)=>counts[b]-counts[a]);
  const w=examTopicWeights(examId, examById(examId), bank);
  const totalBank=topics.reduce((a,t)=>a+counts[t],0)||1;
  const weight=t=>(w.weights&&w.weights[t]!=null)?w.weights[t]:counts[t]/totalBank*100;
  const totW=topics.reduce((a,t)=>a+weight(t),0)||1;
  const alloc=topics.map(t=>({topic:t, perDay:Math.max(1,Math.round(weight(t)/totW*dailyTarget))}));
  let sum=alloc.reduce((a,x)=>a+x.perDay,0), i=0;
  while(sum>dailyTarget && i<alloc.length*8){ const k=alloc[i%alloc.length]; if(k.perDay>1){ k.perDay--; sum--; } i++; }
  i=0; while(sum<dailyTarget && alloc.length){ alloc[i%alloc.length].perDay++; sum++; i++; }
  const daysLeft=daysUntil(deadline);
  return {exam:examId, deadline, dailyTarget, created:todayStr(), daysLeftAtCreate:daysLeft, alloc, weightSource:w.source, noticeId:null};
}
// Rebalance as the deadline approaches: remaining quota per topic (original
// quota minus what was actually practised since the plan started) spread
// over the days still left.
function rebalancePlan(plan){
  const daysLeft=Math.max(0, daysUntil(plan.deadline));
  const done=practiceTopicStats(plan.exam, (progress.attempts||[]).filter(a=>a.date && a.date.slice(0,10)>=plan.created));
  const totalDays=Math.max(1, plan.daysLeftAtCreate);
  return plan.alloc.map(a=>{
    const quota=a.perDay*totalDays;
    const practised=(done[a.topic]||{total:0}).total;
    const remaining=Math.max(0, quota-practised);
    return {topic:a.topic, perDay:a.perDay, quota, practised, remaining, perDayNow:Math.ceil(remaining/Math.max(1,daysLeft))};
  });
}
function currentPlanTarget(){
  const nsel=document.getElementById('pla-notice');
  if(nsel && nsel.value){
    const n=NOTICES.find(x=>x.id===nsel.value);
    if(n && NOTICE_EXAM[n.id]) return {exam:NOTICE_EXAM[n.id], deadline:n.close_date, noticeId:n.id};
  }
  const esel=document.getElementById('pla-exam'), d=document.getElementById('pla-date');
  return {exam:esel?esel.value:'', deadline:d?d.value:'', noticeId:null};
}
function generatePlan(){
  const t=currentPlanTarget();
  const dt=Math.max(5, Math.min(300, parseInt(((document.getElementById('pla-daily')||{}).value||'40'),10)||40));
  if(!t.exam){ alert(B('Choose a notice or an exam first.','पहिले सूचना वा परीक्षा छान्नुहोस्।')); return; }
  if(!t.deadline){ alert(B('Pick a deadline date.','अन्तिम मिति छान्नुहोस्।')); return; }
  const plans=loadPlans();
  const plan=buildStudyPlan(t.exam, t.deadline, dt);
  plan.noticeId=t.noticeId;
  plans[t.exam]=plan; savePlans(plans);
  renderPlanner();
}
function deletePlan(examId){
  if(!confirm(B('Delete this study plan?','यो अध्ययन योजना मेटाउने?'))) return;
  const plans=loadPlans(); delete plans[examId]; savePlans(plans);
  renderPlanner();
}
function showPlan(examId){
  const plans=loadPlans(); const p=plans[examId]; if(!p) return;
  const ns=document.getElementById('pla-notice');
  if(ns && p.noticeId && [...ns.options].some(o=>o.value===p.noticeId)){ ns.value=p.noticeId; }
  else{
    if(ns) ns.value='';
    const es=document.getElementById('pla-exam'); if(es) es.value=p.exam;
    const d=document.getElementById('pla-date'); if(d) d.value=p.deadline;
  }
  renderPlanner();
}
function renderPlanner(){
  const box=document.getElementById('pla-box'); if(!box) return;
  if(!dataReady){ box.innerHTML=skelBlock(2); return; }
  const ns=document.getElementById('pla-notice');
  if(ns){
    const prev=ns.value;
    ns.innerHTML='<option value="">'+esc(B('— choose a notice —','— सूचना छान्नुहोस् —'))+'</option>'
      +planNotices().map(n=>{ const ex=examById(NOTICE_EXAM[n.id]);
        return `<option value="${esc(n.id)}">${esc(n.title)} — ${B('closes','अन्तिम')} ${esc(n.close_date)} · ${esc(examName(ex))}</option>`; }).join('');
    if([...ns.options].some(o=>o.value===prev)) ns.value=prev;
  }
  const t=currentPlanTarget();
  const plans=loadPlans();
  const plan=t.exam?plans[t.exam]:null;
  let h='';
  if(plan) h+=renderPlanCard(plan);
  else h+=emptyState('🗓️', B('No study plan for this target yet','यो लक्ष्यका लागि अझै अध्ययन योजना छैन'), B('Pick a notice (or an exam + deadline) above and generate a day-by-day plan weighted by the real paper pattern.','माथि सूचना (वा परीक्षा + अन्तिम मिति) छानेर वास्तविक पेपर ढाँचाअनुसार तौल गरिएको दैनिक योजना बनाउनुहोस्।'), B('📝 Generate plan','📝 योजना बनाउनुहोस्'), 'generatePlan()');
  const others=Object.keys(plans).filter(k=>k!==t.exam);
  if(others.length){
    h+='<h3>'+B('Other saved plans','अन्य सुरक्षित योजनाहरू')+'</h3>'+others.map(k=>{
      const p=plans[k]; const ex=examById(k);
      return `<div class="card"><strong>${esc(examName(ex)||k)}</strong> <span class="muted">— ${B('deadline','अन्तिम मिति')} ${esc(p.deadline)} · ${daysUntil(p.deadline)} ${B('days left','दिन बाँकी')}</span> <button class="btn secondary" onclick="showPlan('${esc(k)}')">${B('View','हेर्नुहोस्')}</button></div>`;
    }).join('');
  }
  box.innerHTML=h;
}
function renderPlanCard(plan){
  const e=examById(plan.exam);
  const daysLeft=daysUntil(plan.deadline);
  const rows=rebalancePlan(plan);
  const today=rows.filter(r=>r.perDayNow>0);
  const wSrc=plan.weightSource==='breakdown'?B('paper pattern (est.)','पेपर ढाँचा (अनुमान)'):plan.weightSource==='pyq'?B('PYQ shares (est.)','PYQ हिस्सा (अनुमान)'):B('bank mix (est.)','बैंक मिश्रण (अनुमान)');
  let h=`<div class="card"><h3>🎯 ${esc(examName(e)||plan.exam)} — ${B('study plan','अध्ययन योजना')}</h3>
  <p><span class="tag">${B('Deadline','अन्तिम मिति')}: ${esc(plan.deadline)}</span> <span class="tag">${daysLeft} ${B('days left','दिन बाँकी')}</span> <span class="tag">${plan.dailyTarget} ${B('Q/day','प्रश्न/दिन')}</span> <span class="tag">${B('Topic weights','विषय भार')}: ${wSrc}</span></p>`;
  if(daysLeft===0) h+=`<p><strong>⚠️ ${B('Deadline reached or passed — revise strong topics and rest well. Good luck!','अन्तिम मिति आइपुग्यो वा बित्यो — बलिया विषय दोहोर्याउनुहोस् र आराम गर्नुहोस्। शुभकामना!')}</strong></p>`;
  if(plan.daysLeftAtCreate>=14) h+=`<p class="muted">📝 ${B('Sit a full mock every 7 days — start one from Mock Exams.','हरेक ७ दिनमा पूर्ण मक दिनुहोस् — Mock Exams बाट सुरु गर्नुहोस्।')}</p>`;
  h+=`<h4>${B("Today's tasks",'आजका कार्यहरू')}</h4>`;
  h+=today.length?'<ul class="plan-tasks">'+today.map(r=>`<li><button class="btn secondary" onclick="drillTopic('${esc(plan.exam)}','${esc(r.topic)}')">${esc(r.topic)} × ${r.perDayNow}</button> <span class="muted">${r.practised}/${r.quota} ${B('done','पूरा')}</span></li>`).join('')+'</ul>'
    :`<p class="muted">✅ ${B('All caught up — nothing left on today\u2019s list.','सबै सकियो — आजको सूचीमा केही बाँकी छैन।')}</p>`;
  h+=`<h4>${B('Full schedule — rebalanced daily from your actual practice','पूर्ण तालिका — तपाईंको वास्तविक अभ्यासबाट दैनिक पुनःसन्तुलित')}</h4>
  <table class="tbl"><tr><th>${B('Topic','विषय')}</th><th>${B('Planned / day','योजना / दिन')}</th><th>${B('Practised','अभ्यास')}</th><th>${B('Left','बाँकी')}</th><th>${B('Now / day','अब / दिन')}</th></tr>`
    +rows.map(r=>`<tr><td>${esc(r.topic)}</td><td>${r.perDay}</td><td>${r.practised}</td><td>${r.remaining}</td><td><strong>${r.perDayNow}</strong></td></tr>`).join('')+`</table>
  <button class="btn secondary" onclick="deletePlan('${esc(plan.exam)}')">${B('Delete plan','योजना मेटाउनुहोस्')}</button></div>`;
  return h;
}

/* ---------- Feature 4: Negative-marking guess-strategy coach ---------- */
function renderCoach(){
  const box=document.getElementById('coa-box'); if(!box) return;
  if(!dataReady){ box.innerHTML=skelBlock(2); return; }
  const examId=(document.getElementById('coa-exam')||{}).value||'';
  const e=examById(examId);
  if(!e){ box.innerHTML=emptyState('🎯', B('Choose an exam for coaching','कोचिङका लागि परीक्षा छान्नुहोस्'), B('Pick an exam from the dropdown above — the coach analyses your practice history for that exam.','माथिको ड्रपडाउनबाट परीक्षा छान्नुहोस् — कोचले त्यस परीक्षाका लागि तपाईंको अभ्यास इतिहास विश्लेषण गर्छ।')); return; }
  const st=coachStats(examId, progress.attempts, e);
  const negTxt=st.negUnknown?B('unverified','अपुष्ट'):st.negRate===0?B('none','छैन'):Math.round(st.negRate*100)+'%';
  let h=st.attempts?'':emptyState('📊', B('No attempts for this exam yet','यस परीक्षाका लागि अझै प्रयास छैन'), B('Sit a practice set or a mock first — then the coach computes your personal guess maths from your real answers.','पहिले अभ्यास सेट वा मक दिनुहोस् — अनि कोचले तपाईंका वास्तविक उत्तरबाट व्यक्तिगत अनुमान-गणित निकाल्नेछ।'), B('Start a mock','मक सुरु गर्नुहोस्'), "showView('mock')");
  h+=`<div class="card"><h3>🎯 ${esc(examName(e))}</h3>
  <p><span class="tag">${st.attempts} ${B('attempts','प्रयासहरू')}</span> <span class="tag">${st.total} ${B('questions','प्रश्नहरू')}</span> <span class="tag">✅ ${st.correct}</span> <span class="tag">❌ ${st.wrong}</span> <span class="tag">⏭️ ${st.skipped} ${B('skipped','छोडिएको')}</span> <span class="tag">${B('Negative','नेगेटिभ')}: ${negTxt}</span></p>`;
  if(st.attempts){
    h+=`<div class="grid">
    <div class="card"><strong>➖ ${B('Lost to negative marking','नेगेटिभ मार्किङमा गुमेको')}</strong><p class="big-num">${fmt1(st.negLost)}</p><p class="muted">${B('marks deducted for wrong guesses — already baked into your scores','गलत अनुमानमा काटिएको अङ्क — तपाईंको स्कोरमा पहिले नै परेको')}</p></div>
    <div class="card"><strong>⏭️ ${B('Left by skipping (heuristic)','छोडेर गुमाएको (अनुमानित)')}</strong><p class="big-num">~${fmt1(st.estSkipLoss)}</p><p class="muted">${B(`skipped in topics where you score 70%+ (${st.strongSkips} Q) — questions you likely knew`,'७०%+ स्कोर गर्ने विषयहरूमा छोडिएका ('+st.strongSkips+' प्रश्न) — जानेका हुन सक्ने प्रश्नहरू')}</p></div>
    </div>`;
  }
  h+=`<div class="card"><h4>${B('Guess maths for this exam','यो परीक्षाको अनुमान-गणित')}</h4>
  <p class="muted">${B('Expected marks per 1-mark question. Honest maths, not encouragement:','प्रति १-अङ्क प्रश्न अपेक्षित अङ्क। इमानदार गणित, हौसला होइन:')}</p>
  <table class="tbl"><tr><th>${B('Strategy','रणनीति')}</th><th>${B('Expected / mark','अपेक्षित / अङ्क')}</th><th>${B('Verdict','निष्कर्ष')}</th></tr>
  <tr><td>${B('Blind 1-in-4 guess','अन्धाधुन्ध १-मा-४ अनुमान')}</td><td>${st.ev.blind>=0?'+':''}${st.ev.blind.toFixed(3)}</td><td>${evVerdict(st.ev.blind)}</td></tr>
  <tr><td>${B('After eliminating 1 option','१ विकल्प हटाएपछि')}</td><td>+${st.ev.elim1.toFixed(3)}</td><td>${evVerdict(st.ev.elim1)}</td></tr>
  <tr><td>${B('After eliminating 2 options','२ विकल्प हटाएपछि')}</td><td>+${st.ev.elim2.toFixed(3)}</td><td>${evVerdict(st.ev.elim2)}</td></tr></table></div>`;
  h+=`<div class="card"><h4>${B("Coach's advice",'कोचको सल्लाह')}</h4><ul>`
    +coachAdvice(st,e).map(a=>`<li>${B(a.en,a.ne)}${a.topic?` <button class="btn secondary" onclick="drillTopic('${esc(examId)}','${esc(a.topic)}')">${B('Drill','अभ्यास')}</button>`:''}</li>`).join('')+`</ul>
  <p class="muted">⚠️ ${B('Heuristic — built from your practice history, not a prediction of the real paper.','अनुमानित — तपाईंको अभ्यास इतिहासबाट बनेको, वास्तविक पेपरको भविष्यवाणी होइन।')}</p></div>`;
  const trouble=Object.keys(st.perTopic).map(t=>({t, s:st.perTopic[t]})).filter(x=>x.s.wrong>0).sort((a,b)=>b.s.wrong-a.s.wrong).slice(0,8);
  if(trouble.length){
    h+=`<div class="card"><h4>${B('Where your wrong answers cluster','तपाईंका गलत उत्तरहरू कहाँ केन्द्रित छन्')}</h4>
    <table class="tbl"><tr><th>${B('Topic','विषय')}</th><th>❌</th><th>⏭️</th><th>${B('Accuracy','शुद्धता')}</th><th></th></tr>`
    +trouble.map(x=>{ const att=x.s.correct+x.s.wrong;
      return `<tr><td>${esc(x.t)}</td><td>${x.s.wrong}</td><td>${x.s.skipped}</td><td>${Math.round(x.s.correct/att*100)}%</td><td><button class="btn secondary" onclick="drillTopic('${esc(examId)}','${esc(x.t)}')">${B('Drill','अभ्यास')}</button></td></tr>`; }).join('')+`</table></div>`;
  }
  box.innerHTML=h;
}

/* ---------- Feature 5: PYQ heatmap ---------- */
function heatCell(text, frac, rgb){
  const a=Math.max(0.05, Math.min(0.85, frac||0)).toFixed(2);
  return `<td style="background:rgba(${rgb},${a})">${text}</td>`;
}
function renderPYQ(){
  const box=document.getElementById('pyq-box'); if(!box) return;
  if(!dataReady){ box.innerHTML=skelBlock(2); return; }
  const examId=(document.getElementById('pyq-exam')||{}).value||'';
  const e=examById(examId);
  if(!e){ box.innerHTML=emptyState('🔥', B('Choose an exam to see its PYQ map','PYQ नक्सा हेर्न परीक्षा छान्नुहोस्'), B('Pick an exam from the dropdown above — the heatmap shows which topics real papers asked most.','माथिको ड्रपडाउनबाट परीक्षा छान्नुहोस् — हिटम्यापले वास्तविक पेपरले कुन विषय बढी सोधेको देखाउँछ।')); return; }
  const pyq=pyqTopicShares(examId);
  const counts=topicsForExam(examId);
  const topics=Object.keys(counts).sort();
  if(!topics.length){ box.innerHTML=`<div class="card"><h3>🔥 ${esc(examName(e))}</h3></div>`+emptyState('📚', B('No bank coverage for this exam yet','यस परीक्षाका लागि बैंकमा अझै कभरेज छैन'), B('The question bank has no questions tagged for this exam, so there is no heatmap to draw yet.','प्रश्न बैंकमा यस परीक्षाका लागि ट्याग गरिएका प्रश्न छैनन्, त्यसैले हिटम्याप बनाउन केही छैन।'), B('Practise the mixed bank','मिश्रित बैंक अभ्यास गर्नुहोस्'), "showView('practice')"); return; }
  const totalBank=topics.reduce((a,t)=>a+counts[t],0);
  const stats=practiceTopicStats(examId, progress.attempts);
  const hasPyq=pyq.n>=5;
  let h=`<div class="card"><h3>🔥 ${esc(examName(e))}</h3>
  <p><span class="tag">${B('Transcribed PYQs','लिपिबद्ध PYQ')}: ${pyq.n}</span> <span class="tag">${B('Bank','बैंक')}: ${totalBank.toLocaleString()} ${B('Qs','प्रश्न')}</span></p>`;
  if(!hasPyq) h+=`<p class="muted">ℹ️ ${B(`No transcribed Previous Year questions for this exam yet — the bank's 133 transcribed PYQs cover Kharidar & NaSu. The table below still shows bank coverage vs your practice; transcribe a paper to grow this map.`,'यस परीक्षाका लागि अहिलेसम्म लिपिबद्ध पुराना प्रश्नहरू छैनन् — बैंकका १३३ लिपिबद्ध PYQ खरिदार र नासुका हुन्। तलको तालिकामा बैंक कभरेज र तपाईंको अभ्यास अझै देखिन्छ; यो नक्सा बढाउन पेपर लिपिबद्ध गर्नुहोस्।')}</p>`;
  else h+=`<p class="muted">${B(`Real-paper weight is the topic share across ${pyq.n} transcribed PYQs — an indicative sample, not the full paper. Red = heavily asked, blue = well covered in the bank, green = your accuracy.`,'वास्तविक-पेपर भार '+pyq.n+' लिपिबद्ध PYQ मा विषय हिस्सा हो — सङ्केतमूलक नमुना, पूर्ण पेपर होइन। रातो = धेरै सोधिएको, नीलो = बैंकमा राम्रो कभरेज, हरियो = तपाईंको शुद्धता।')}</p>`;
  const maxW=hasPyq?Math.max(...topics.map(t=>pyq.shares[t]||0),0.01):1;
  const maxB=Math.max(...topics.map(t=>counts[t]/totalBank),0.01);
  h+=`<table class="tbl"><tr><th>${B('Topic','विषय')}</th>${hasPyq?`<th>${B('Real-paper share','वास्तविक पेपर हिस्सा')}</th>`:''}<th>${B('Bank share','बैंक हिस्सा')}</th><th>${B('Your practice','तपाईंको अभ्यास')}</th><th>${B('Accuracy','शुद्धता')}</th></tr>`;
  const rows=topics.slice().sort((a,b)=>((pyq.shares[b]||0)-(pyq.shares[a]||0)));
  for(const t of rows){
    const s=stats[t]||{total:0,correct:0,wrong:0};
    const att=s.correct+s.wrong;
    const acc=att?Math.round(s.correct/att*100):null;
    h+=`<tr><td>${esc(t)}</td>`
      +(hasPyq?heatCell((pyq.shares[t]||0).toFixed(1)+'%', (pyq.shares[t]||0)/maxW, '220,60,60'):'')
      +heatCell((counts[t]/totalBank*100).toFixed(1)+'%', (counts[t]/totalBank)/maxB, '59,130,246')
      +`<td>${s.total}</td>`
      +heatCell(acc==null?'—':acc+'%', acc==null?0:acc/100, '34,197,94')
      +`</tr>`;
  }
  h+=`</table><p class="muted">${B('Read it as: red + low green = high-yield topic you are weak in — drill it. Red + low blue = the bank needs more questions here.','यसरी पढ्नुहोस्: रातो + कम हरियो = तपाईं कमजोर भएको उच्च-प्रतिफल विषय — अभ्यास गर्नुहोस्। रातो + कम नीलो = बैंकमा यहाँ थप प्रश्न चाहिन्छ।')}</p></div>`;
  box.innerHTML=h;
}

/* ---- Exam reminders (data/exam-dates.json) ---- */
// BS calendar anchor: 2026-10-31 AD (UTC) = 2083-07-14 BS (Kartik 14, 2083).
// All BS arithmetic is day-offsets from this anchor — no external calendar
// library, no guessing. Month lengths below are the VERIFIED 2083/2084 BS
// lengths (cross-checks: Baisakh 1 2083 = Apr 14 2026; Kartik 1 2083 =
// Oct 18 2026; Poush 1 2083 = Dec 16 2026 — govt 2083 holiday list, so
// Mangsir has 29 days and Poush 30; Magh 1 2083 = Jan 15 2027; Maha
// Shivaratri Falgun 11 2084 = Feb 23 2028, so Magh 2084 has 29 days and
// Falgun 30). CORRECTED 2026-11-09: the previous tables had Mangsir 30 /
// Poush 29 (2083) and Magh 30 / Falgun 29 (2084) — a one-day error inside
// Mangsir–Poush 2083 and Magh–Falgun 2084. If a later year is ever added,
// verify its lengths against the official patro first.
const BS_ANCHOR_AD = Date.UTC(2026, 9, 31); // 2026-10-31T00:00:00Z
const BS_MONTH_LEN = {
  2083: [31,32,31,32,31,30,30,29,30,29,30,30],
  2084: [31,32,31,32,31,30,30,30,29,29,30,31]
};
const BS_MONTH_EN = ['Baisakh','Jestha','Ashadh','Shrawan','Bhadra','Ashwin','Kartik','Mangsir','Poush','Magh','Falgun','Chaitra'];
const BS_MONTH_NE = ['बैशाख','जेठ','असार','साउन','भदौ','असोज','कात्तिक','मंसिर','पुस','माघ','फागुन','चैत'];

function bsParse(s){ const m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(s||''); return m?{y:+m[1],m:+m[2],d:+m[3]}:null; }
// Absolute day count since 2083-01-01. null on malformed/out-of-range input.
function bsAbsDay(s){
  const p=bsParse(s); if(!p) return null;
  const lens=BS_MONTH_LEN[p.y]; if(!lens) return null;
  if(p.m<1||p.m>12||p.d<1||p.d>lens[p.m-1]) return null;
  let n=0;
  for(let y=2083;y<p.y;y++){ const l=BS_MONTH_LEN[y]; if(!l) return null; n+=l.reduce((a,b)=>a+b,0); }
  for(let m=1;m<p.m;m++) n+=lens[m-1];
  return n+(p.d-1);
}
function bsFromAbs(n){
  for(let y=2083;y<=2100;y++){
    const lens=BS_MONTH_LEN[y]; if(!lens) return null;
    const yl=lens.reduce((a,b)=>a+b,0);
    if(n<yl){ let m=1; while(n>=lens[m-1]){ n-=lens[m-1]; m++; } return y+'-'+String(m).padStart(2,'0')+'-'+String(n+1).padStart(2,'0'); }
    n-=yl;
  }
  return null;
}
const BS_ANCHOR_ABS = bsAbsDay('2083-07-14'); // 200 — verified against both AD anchors
// Today's BS date (YYYY-MM-DD), derived from the anchor + elapsed AD days.
function bsToday(){
  const adDays=Math.floor(Date.now()/864e5)-Math.floor(BS_ANCHOR_AD/864e5);
  return bsFromAbs(BS_ANCHOR_ABS+adDays);
}
// Days from today (BS) until date_bs. Negative = past. null = bad input.
function bsDaysUntil(s){
  const a=bsAbsDay(s); if(a==null) return null;
  return a-bsAbsDay(bsToday());
}
function neDigits(s){ return String(s).replace(/\d/g,d=>'०१२३४५६७८९'[+d]); }
// "14 Kartik 2083" / "१४ कात्तिक २०८३"
function fmtBs(s){
  const p=bsParse(s); if(!p||p.m<1||p.m>12) return s||'';
  if(lang==='ne') return neDigits(p.d)+' '+BS_MONTH_NE[p.m-1]+' '+neDigits(p.y);
  return p.d+' '+BS_MONTH_EN[p.m-1]+' '+p.y;
}
// Countdown label: 0 → Today/आज, 1 → Tomorrow/भोलि, else "in N days".
function bsCountdown(d){
  if(d===0) return B('Today','आज');
  if(d===1) return B('Tomorrow','भोलि');
  return B('in '+d+' days', neDigits(d)+' दिनमा');
}

// Reminder storage (all on-device, versioned keys — no backend).
const REM_DISMISSED='loksewa_rem_dismissed_v1', REM_LIST='loksewa_reminders_v1',
      REM_NOTIFIED='loksewa_rem_notified_v1', REM_ASKED='loksewa_notif_asked_v1';
function remStore(k,fb){ try{ const v=JSON.parse(localStorage.getItem(k)); if(v==null) return fb; if(Array.isArray(fb)!==Array.isArray(v)) return fb; if(typeof v!==typeof fb) return fb; return v; }catch(e){ return fb; } }
function remSave(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)); }catch(e){} }
function upcomingExamDates(){
  const t=bsToday();
  return (EXAMDATES||[]).filter(e=>e&&e.date_bs&&e.date_bs>=t)
    .sort((a,b)=>a.date_bs<b.date_bs?-1:(a.date_bs>b.date_bs?1:0));
}
function examDateById(id){ return (EXAMDATES||[]).find(e=>e&&e.id===id); }

// Home hero banner: today → alert; ≤7 days → reminder; else nearest upcoming.
function renderExamReminder(){
  const box=document.getElementById('exam-reminder-banner'); if(!box) return;
  if(!dataReady){ box.innerHTML=''; return; }
  const dismissed=remStore(REM_DISMISSED,{});
  const up=upcomingExamDates().filter(e=>!dismissed[e.id]);
  if(!up.length){ box.innerHTML=''; return; }
  const e=up[0], d=bsDaysUntil(e.date_bs);
  const title=esc(lang==='ne'?(e.title_ne||e.title_en):(e.title_en||''));
  const ex=e.exam&&examById(e.exam)?e.exam:null;
  const goBtn=ex?` <button class="btn secondary rem-go" onclick="goPracticeExam('${esc(ex)}')">${B('Practice now','अहिले अभ्यास गर्नुहोस्')}</button>`:'';
  const xBtn=`<button class="rem-x" aria-label="${B('Dismiss','हटाउनुहोस्')}" onclick="dismissReminder('${esc(e.id)}')">×</button>`;
  let h='';
  if(d===0) h=`<div class="rem-banner rem-today" role="alert"><span>🔔 <strong>${title}</strong> — ${B('is today! Good luck.','आज छ! शुभकामना।')}</span>${goBtn}${xBtn}</div>`;
  else if(d>0&&d<=7) h=`<div class="rem-banner rem-soon" role="alert"><span>⏰ <strong>${title}</strong> — ${esc(bsCountdown(d))} · ${esc(fmtBs(e.date_bs))}</span>${goBtn}${xBtn}</div>`;
  else h=`<div class="rem-banner rem-next"><span>📅 ${B('Coming up','आगामी')}: <strong>${title}</strong> — ${esc(fmtBs(e.date_bs))}</span><span><button class="linklike" onclick="showView('examdates')">${B('See all dates','सबै मिति हेर्नुहोस्')}</button>${xBtn}</span></div>`;
  box.innerHTML=h;
}
function dismissReminder(id){ const d=remStore(REM_DISMISSED,{}); d[id]=true; remSave(REM_DISMISSED,d); renderExamReminder(); }
function goPracticeExam(id){
  const s=document.getElementById('practice-exam');
  if(s){ s.value=id; if(typeof updatePracticeTopics==='function'){ try{ updatePracticeTopics(); }catch(e){} } }
  showView('practice');
}
function goMockExam(id){
  const s=document.getElementById('mock-exam');
  if(s){ s.value=id; }
  showView('mock');
}

// Exam Dates view: chronological list, countdown chips, kind filter,
// per-exam "remind me" toggle, practice/mock links, official source links.
let examDateFilter='';
function remKindLabel(k){
  return k==='exam'?B('Exam','परीक्षा'):k==='admit'?B('Admit card','प्रवेशपत्र'):k==='deadline'?B('Deadline','अन्तिम मिति'):esc(k||'');
}
function remChip(d){
  if(d===0) return `<span class="chip chip-today">🔴 ${B('Today','आज')}</span>`;
  if(d===1) return `<span class="chip chip-soon">🟡 ${B('Tomorrow','भोलि')}</span>`;
  if(d<=7) return `<span class="chip chip-soon">🟡 ${esc(bsCountdown(d))}</span>`;
  return `<span class="chip">📅 ${esc(bsCountdown(d))}</span>`;
}
function renderExamDates(){
  const box=document.getElementById('examdates-box'); if(!box) return;
  if(!dataReady){ box.innerHTML=skelBlock(2); return; }
  const list=(EXAMDATES||[]).slice().sort((a,b)=>a.date_bs<b.date_bs?-1:(a.date_bs>b.date_bs?1:0));
  const t=bsToday();
  const kinds=[...new Set(list.map(e=>e.kind).filter(Boolean))];
  const f=examDateFilter;
  const shown=list.filter(e=>!f||e.kind===f);
  const reminded=remStore(REM_LIST,[]);
  // Polite one-time notification prompt: an inline button, never auto-asked.
  let notifHtml='';
  if(typeof Notification!=='undefined'&&Notification.permission==='default'&&!remStore(REM_ASKED,false)){
    notifHtml=`<p><button class="btn secondary" onclick="enableExamNotifications()">${B('🔔 Enable exam reminders','🔔 परीक्षा रिमाइन्डर सक्रिय गर्नुहोस्')}</button> <span class="muted">${B('Your browser will notify you when a saved exam is 3 days away. On-device only — nothing is uploaded.','सेभ गरिएको परीक्षा ३ दिन टाढा हुँदा ब्राउजरले सूचना दिनेछ। यन्त्रमै मात्र — केही अपलोड हुँदैन।')}</span></p>`;
  }
  let h=`<div class="card"><h2>📅 ${B('Exam dates','परीक्षा मितिहरू')}</h2>
  <p class="muted">${B('Verified exam dates, admit-card releases and application deadlines from official notices (PSC, TSC, NRB, MEC…). Dates are in Bikram Sambat — never guessed; every entry links its source.','आधिकारिक सूचनाहरूबाट प्रमाणित परीक्षा मिति, प्रवेशपत्र र आवेदन अन्तिम मिति (लोक सेवा, शिक्षक सेवा, राष्ट्र बैंक, चिकित्सा शिक्षा आयोग…)। मितिहरू विक्रम संवत्मा छन् — अनुमान गरिएको होइन; हरेक प्रविष्टिमा स्रोत लिङ्क छ।')}</p>${notifHtml}`;
  if(kinds.length>1){
    h+=`<p><label>${B('Show:','देखाउनुहोस्:')} <select id="ed-kind" onchange="examDateFilter=this.value;renderExamDates()">
    <option value="">${B('All','सबै')}</option>${kinds.map(k=>`<option value="${esc(k)}"${f===k?' selected':''}>${remKindLabel(k)}</option>`).join('')}</select></label></p>`;
  }
  if(!shown.length){
    h+=emptyState('📅', B('No dates yet','अहिले मिति छैन'), B('No verified upcoming dates in this list. Check the official sites linked in Notices.','यो सूचीमा प्रमाणित आगामी मिति छैन। सूचनामा लिङ्क गरिएका आधिकारिक साइट हेर्नुहोस्।'));
  }else{
    h+='<div class="ed-list">';
    for(const e of shown){
      const d=bsDaysUntil(e.date_bs);
      const title=esc(lang==='ne'?(e.title_ne||e.title_en):e.title_en);
      const past=d<0;
      const ex=e.exam&&examById(e.exam)?examById(e.exam):null;
      const isR=reminded.includes(e.id);
      h+=`<div class="card ed-row${past?' ed-past':''}">${past?`<span class="chip">✓ ${B('Done','सकियो')}</span>`:remChip(d)}
      <div class="ed-main"><strong>${title}</strong>
      <p class="muted">${esc(fmtBs(e.date_bs))} · ${remKindLabel(e.kind)}${e.source?` · <a href="${esc(e.source)}" target="_blank" rel="noopener">${B('Official source','आधिकारिक स्रोत')}</a>`:''}${e.confidence==='medium'?` · <span title="${B('Single-source: re-verify on the official site','एकल स्रोत: आधिकारिक साइटमा पुनःपुष्टि गर्नुहोस्')}">⚠️ ${B('re-verify','पुनःपुष्टि')}</span>`:''}</p>
      <p class="ed-actions">
      ${ex?`<button class="btn secondary" onclick="goPracticeExam('${esc(ex.id)}')">${B('Practice','अभ्यास')}</button>`:''}
      ${ex&&ex.prelim?` <button class="btn secondary" onclick="goMockExam('${esc(ex.id)}')">${B('Mock','मक')}</button>`:''}
      ${!past?` <button class="btn secondary${isR?' rem-on':''}" onclick="toggleExamReminder('${esc(e.id)}')">${isR?B('🔔 Reminding','🔔 रिमाइन्डर छ'):B('🔕 Remind me','🔕 सम्झाउनुहोस्')}</button>`:''}
      </p></div></div>`;
    }
    h+='</div>';
  }
  const lastV=(EXAMDATES||[]).reduce((m,e)=>e.verified&&e.verified>m?e.verified:m,'');
  h+=`<p class="muted">${B('Last verified','अन्तिम प्रमाणित')}: ${esc(lastV||'—')}. ${B('Exam boards reschedule — always confirm on the official site before travelling.','परीक्षा बोर्डले मिति सार्न सक्छ — यात्रा गर्नुअघि आधिकारिक साइटमा पुष्टि गर्नुहोस्।')}</p></div>`;
  box.innerHTML=h;
}
function toggleExamReminder(id){
  let r=remStore(REM_LIST,[]);
  r=r.includes(id)?r.filter(x=>x!==id):r.concat([id]);
  remSave(REM_LIST,r); renderExamDates(); renderExamReminder(); renderNextExamCard(); renderNextExamCompact();
}
function enableExamNotifications(){
  remSave(REM_ASKED,true);
  if(typeof Notification==='undefined') return;
  try{ Notification.requestPermission().then(()=>renderExamDates()).catch(()=>{}); }catch(e){}
}
// On-device reminder check: when the app opens and a saved exam is ≤3 days
// away (and today), fire one browser Notification per exam per day.
function checkExamNotifications(){
  if(typeof Notification==='undefined'||Notification.permission!=='granted') return;
  const reminded=remStore(REM_LIST,[]); if(!reminded.length) return;
  const today=bsToday();
  const done=remStore(REM_NOTIFIED,{});
  let changed=false;
  for(const id of reminded){
    const e=examDateById(id); if(!e) continue;
    const d=bsDaysUntil(e.date_bs);
    if(d==null||d<0||d>3) continue;
    if(done[id]===today) continue;
    const title=lang==='ne'?(e.title_ne||e.title_en):e.title_en;
    try{ new Notification('📅 '+title, { body: d===0?B('The exam is today! Good luck.','परीक्षा आज छ! शुभकामना।'):B('In '+d+' day'+(d>1?'s':'')+' — '+fmtBs(e.date_bs), neDigits(d)+' दिनमा — '+fmtBs(e.date_bs)), tag:'loksewa-rem-'+id }); }catch(err){}
    done[id]=today; changed=true;
  }
  if(changed) remSave(REM_NOTIFIED,done);
}

/* ---- "Next exam" live countdown card ---- */
// Countdown maths — pure and testable. The target is START-OF-DAY (00:00 UTC)
// on date_bs, derived from the SAME BS anchor as bsToday: no second calendar
// system, no guessing. Dates are day-granular so sub-day precision comes from
// the anchor offset alone.
function nxTargetMs(s){
  const abs=bsAbsDay(s); if(abs==null) return null;
  return BS_ANCHOR_AD + (abs-BS_ANCHOR_ABS)*864e5;
}
// Remaining time from nowMs until start-of-day on date_bs. Clamped at zero —
// never negative. Returns null on bad input.
function nxRemaining(s, nowMs){
  const t=nxTargetMs(s); if(t==null||nowMs==null) return null;
  let ms=t-nowMs; if(ms<0) ms=0;
  const d=Math.floor(ms/864e5); ms-=d*864e5;
  const h=Math.floor(ms/36e5);  ms-=h*36e5;
  const m=Math.floor(ms/6e4);   ms-=m*6e4;
  const sec=Math.floor(ms/1e3);
  return {d,h,m,s:sec};
}
function nxPad(n){ return String(n).padStart(2,'0'); }
// Pager list: upcoming exams within the next 30 days, nearest first.
function nxPagerList(){
  return upcomingExamDates().filter(e=>{ const d=bsDaysUntil(e.date_bs); return d!=null&&d>=0&&d<=30; });
}
// Card state: 'today' | 'near' (nearest within 30d) | 'far' (>30d out) | 'none'
function nxCardState(){
  const up=upcomingExamDates(); if(!up.length) return 'none';
  const d=bsDaysUntil(up[0].date_bs);
  if(d===0) return 'today';
  return (d!=null&&d<=30)?'near':'far';
}
// Pager position, keyed to the current list so it resets when dates change.
let nxIdx=0, nxListKey='';
function nxPick(list){
  const key=list.map(e=>e.id).join('|');
  if(key!==nxListKey){ nxListKey=key; nxIdx=0; }
  if(!list.length) return null;
  nxIdx=((nxIdx%list.length)+list.length)%list.length;
  return list[nxIdx];
}
function nxCycle(i){ nxIdx=i; renderNextExamCard(); renderNextExamCompact(); }

// One shared 1-second ticker for every countdown on the page. Skips work
// while the tab is hidden (document.hidden); also re-ticks on visibility
// change so the digits are fresh the moment the tab returns.
let nxTimer=null;
function nxTick(){
  if(typeof document==='undefined'||document.hidden) return;
  const now=Date.now();
  document.querySelectorAll('[data-nx-date]').forEach(el=>{
    const r=nxRemaining(el.getAttribute('data-nx-date'), now);
    if(!r) return;
    const set=(k,v)=>{ const n=el.querySelector('[data-nx-'+k+']'); if(n) n.textContent=v; };
    set('d', nxPad(r.d)); set('h', nxPad(r.h)); set('m', nxPad(r.m)); set('s', nxPad(r.s));
  });
}
function nxStartTicker(){
  if(nxTimer) return;
  nxTimer=setInterval(nxTick, 1000);
  if(typeof document!=='undefined'&&document.addEventListener){
    document.addEventListener('visibilitychange', ()=>{ if(!document.hidden) nxTick(); });
  }
}
function nxTitle(e){ return esc(lang==='ne'?(e.title_ne||e.title_en):(e.title_en||'')); }
function nxExamLink(e){
  const ex=e.exam&&examById(e.exam)?examById(e.exam):null;
  if(!ex) return '';
  let h=`<button class="btn secondary" onclick="goPracticeExam('${esc(ex.id)}')">${B('Practice now','अहिले अभ्यास गर्नुहोस्')}</button>`;
  if(ex.prelim) h+=` <button class="btn secondary" onclick="goMockExam('${esc(ex.id)}')">${B('Mock','मक')}</button>`;
  return h;
}
function nxRemindBtn(e){
  const isR=remStore(REM_LIST,[]).includes(e.id);
  return `<button class="btn secondary${isR?' rem-on':''}" onclick="toggleExamReminder('${esc(e.id)}')">${isR?B('🔔 Reminding','🔔 रिमाइन्डर छ'):B('🔕 Remind me','🔕 सम्झाउनुहोस्')}</button>`;
}
function nxDigitsHtml(dateBs, compact){
  return `<div class="nx-digits${compact?' nx-compact-digits':''}" data-nx-date="${esc(dateBs)}" role="timer" aria-label="${B('Countdown to exam','परीक्षासम्म बाँकी समय')}">
    <div><b data-nx-d>--</b><span>${B('days','दिन')}</span></div><i>:</i>
    <div><b data-nx-h>--</b><span>${B('hrs','घण्टा')}</span></div><i>:</i>
    <div><b data-nx-m>--</b><span>${B('min','मिनेट')}</span></div><i>:</i>
    <div><b data-nx-s>--</b><span>${B('sec','सेकेन्ड')}</span></div>
  </div>`;
}
// Pager dots: at most 7 visible — with 65+ exams inside 30 days a dot
// per exam fills the card with a row of rings. The window slides with
// the current index; the counter shows the true position.
function nxDotsHtml(list){
  if(list.length<=1) return '';
  const max=7;
  let start=0;
  if(list.length>max) start=Math.min(Math.max(nxIdx-3,0),list.length-max);
  const end=Math.min(start+max,list.length);
  let dots='';
  for(let i=start;i<end;i++){
    const x=list[i];
    dots+=`<button class="nx-dot${i===nxIdx?' on':''}" role="tab" aria-selected="${i===nxIdx}" aria-label="${esc(lang==='ne'?(x.title_ne||x.title_en):x.title_en)}" onclick="nxCycle(${i})"></button>`;
  }
  const counter=list.length>max?`<span class="nx-count muted">${nxIdx+1} / ${list.length}</span>`:'';
  return `<div class="nx-pager" role="tablist" aria-label="${B('Upcoming exams','आगामी परीक्षाहरू')}">${dots}${counter}</div>`;
}
// Full card: Home view, directly below the hero.
function renderNextExamCard(){
  const box=document.getElementById('next-exam-card'); if(!box) return;
  if(!dataReady){ box.innerHTML=''; return; }
  const state=nxCardState();
  if(state==='none'){ box.innerHTML=''; return; }
  nxStartTicker();
  const up=upcomingExamDates();
  const list=nxPagerList();
  const e=state==='far'?up[0]:nxPick(list);
  if(!e){ box.innerHTML=''; return; }
  const title=nxTitle(e), d=bsDaysUntil(e.date_bs);
  let inner='';
  if(state==='today'){
    inner=`<div class="nx-todaybig">🎯 ${B('Today!','आज!')}</div>
      <p class="muted">${B('The exam day is here — good luck.','परीक्षाको दिन आयो — शुभकामना।')}</p>`;
  }else{
    inner=nxDigitsHtml(e.date_bs,false);
  }
  const dots=nxDotsHtml(list);
  box.innerHTML=`<div class="nx-card nx-${state}">
    <div class="nx-head"><span class="nx-label">⏳ ${B('Next exam','अर्को परीक्षा')}</span>${d>0?`<span class="chip${d<=7?' chip-soon':''}">${d<=7?'🟡':'📅'} ${esc(bsCountdown(d))}</span>`:''}</div>
    <h3 class="nx-title">${title}</h3>
    ${inner}
    <p class="nx-date muted">${esc(fmtBs(e.date_bs))} · ${remKindLabel(e.kind)}${e.source?` · <a href="${esc(e.source)}" target="_blank" rel="noopener">${B('Official source','आधिकारिक स्रोत')}</a>`:''}${e.confidence==='medium'?` · ⚠️ ${B('re-verify','पुनःपुष्टि')}`:''}</p>
    ${dots}
    <div class="nx-actions">${nxExamLink(e)} ${nxRemindBtn(e)} <button class="btn secondary" onclick="showView('examdates')">${B('All dates','सबै मिति')}</button></div>
  </div>`;
  nxTick();
}
// Compact card: top of the Dashboard view.
function renderNextExamCompact(){
  const box=document.getElementById('next-exam-compact'); if(!box) return;
  if(!dataReady){ box.innerHTML=''; return; }
  const state=nxCardState();
  if(state==='none'||state==='far'){ box.innerHTML=''; return; }
  nxStartTicker();
  const e=nxPick(nxPagerList());
  if(!e){ box.innerHTML=''; return; }
  const body=bsDaysUntil(e.date_bs)===0
    ? `<strong>🎯 ${B('Today!','आज!')}</strong>`
    : nxDigitsHtml(e.date_bs,true);
  box.innerHTML=`<div class="card nx-compact"><span class="nx-label">⏳ ${B('Next exam','अर्को परीक्षा')}:</span> <strong>${nxTitle(e)}</strong> ${body} <span class="nx-compact-btn">${nxRemindBtn(e)}</span></div>`;
  nxTick();
}

/* ---- Festival wishes (data/festivals.json) ----
   Eid al-Fitr and Bakr Eid are EXCLUDED from festivals.json by the user's
   explicit instruction (2026-11-09) — every other Nepal festival is in.
   Windows are compared as zero-padded YYYY-MM-DD strings (lexicographic
   order == chronological order), so a window may end in 2085 (Bisket Jatra
   2028 ends 2085-01-05) even though BS_MONTH_LEN stops at 2084. Known gap:
   bsToday() is null once the year rolls to 2085, so the card cannot show
   during 2085-01-01→01-05 (14–18 Apr 2028) until the 2085 patro publishes
   and BS_MONTH_LEN gains that year. Dismissing a card hides it for the
   rest of that festival window. */
const FEST_DISMISSED='loksewa_festival_dismissed_v1';
function festById(id){ return (FESTIVALS||[]).find(f=>f&&f.id===id); }
// Festivals active today (start<=today<=end), earliest start first.
function festivalsToday(){
  const t=bsToday();
  return (FESTIVALS||[]).filter(f=>f&&f.start_bs&&f.end_bs&&f.start_bs<=t&&t<=f.end_bs)
    .sort((a,b)=>a.start_bs<b.start_bs?-1:(a.start_bs>b.start_bs?1:(a.id<b.id?-1:1)));
}
// Festivals starting tomorrow (bsDaysUntil(start)===1).
function festivalsTomorrow(){
  return (FESTIVALS||[]).filter(f=>f&&f.start_bs&&bsDaysUntil(f.start_bs)===1)
    .sort((a,b)=>a.start_bs<b.start_bs?-1:(a.start_bs>b.start_bs?1:(a.id<b.id?-1:1)));
}
// Next n festivals strictly after today.
function festivalsUpcoming(n){
  const t=bsToday();
  return (FESTIVALS||[]).filter(f=>f&&f.start_bs&&f.start_bs>t)
    .sort((a,b)=>a.start_bs<b.start_bs?-1:(a.start_bs>b.start_bs?1:(a.id<b.id?-1:1))).slice(0,n||3);
}
function festName(f){ return esc(lang==='ne'?(f.name_ne||f.name_en):(f.name_en||'')); }
function festGreeting(f){ return esc(lang==='ne'?(f.greeting_ne||f.greeting_en):(f.greeting_en||'')); }
function festDismissed(f){
  const d=remStore(FEST_DISMISSED,{});
  return d[f.id]===f.end_bs;
}
function dismissFestival(id){
  const f=festById(id); if(!f) return;
  const d=remStore(FEST_DISMISSED,{}); d[id]=f.end_bs; remSave(FEST_DISMISSED,d);
  renderFestivalCard();
}
function festConfetti(){
  if(prefersReducedMotion()) return '';
  const cols=['#ea580c','#ec4899','#22c55e','#3b82f6','#f97316','#fed7aa'];
  let s='';
  for(let i=0;i<12;i++){
    const left=(i*83)%100, delay=(i%6)*0.7, dur=5+(i%4), c=cols[i%cols.length], sz=6+(i%3)*3;
    s+=`<i class="fest-confetti-bit" style="left:${left}%;animation-delay:${delay}s;animation-duration:${dur}s;background:${c};width:${sz}px;height:${sz}px"></i>`;
  }
  return `<div class="fest-confetti" aria-hidden="true">${s}</div>`;
}
function renderFestivalCard(){
  const box=document.getElementById('festival-card'); if(!box) return;
  if(!dataReady){ box.innerHTML=''; return; }
  const active=festivalsToday().filter(f=>!festDismissed(f));
  const tom=festivalsTomorrow();
  if(active.length){
    const f=active[0];
    const rest=active.slice(1);
    const range=f.end_bs!==f.start_bs?`${esc(fmtBs(f.start_bs))} – ${esc(fmtBs(f.end_bs))}`:esc(fmtBs(f.start_bs));
    const also=rest.length?`<p class="fest-also">${B('Also today:','आज अरू पनि:')} ${rest.map(festName).join(', ')}</p>`:'';
    const up=festivalsUpcoming(3);
    const strip=up.length?`<div class="fest-strip">${up.map(u=>`<span class="chip">${esc(u.emoji||'🎉')} ${festName(u)} · ${esc(fmtBs(u.start_bs))}</span>`).join('')}</div>`:'';
    box.innerHTML=`<div class="fest-card" style="--fest:${esc(f.accent||'#ea580c')}">
      ${festConfetti()}
      <button class="rem-x fest-x" aria-label="${B('Dismiss','हटाउनुहोस्')}" onclick="dismissFestival('${esc(f.id)}')">×</button>
      <div class="fest-emoji">${esc(f.emoji||'🎉')}</div>
      <p class="fest-label">${B('Festival wishes','चाडपर्वको शुभकामना')}</p>
      <h3 class="fest-title">${B('Happy','शुभ')} ${festName(f)}!</h3>
      <p class="fest-greet">${festGreeting(f)}</p>
      <p class="fest-date muted">${range}${f.confidence==='medium'?` · ⚠️ ${B('re-verify','पुनःपुष्टि')}`:''}</p>
      ${also}
      ${strip}
    </div>`;
    return;
  }
  if(tom.length){
    const f=tom[0];
    const more=tom.length>1?` · +${tom.length-1} ${B('more','थप')}`:'';
    box.innerHTML=`<div class="fest-teaser"><span>${esc(f.emoji||'🎉')} ${B('Tomorrow:','भोलि:')} <strong>${festName(f)}</strong> · ${esc(fmtBs(f.start_bs))}${more}</span></div>`;
    return;
  }
  box.innerHTML='';
}

/* ================= Historical events / Dates to Remember =================
   Data: data/historical-events.json (95 verified entries, 2026-11-09 —
   see data/SOURCES.md §19 and scripts/historical-events-notes.md).
   Schema: {id, title_en, title_ne, day_bs ("MM-DD" | null),
   year_bs (int | null), date_ad ("YYYY-MM-DD" | null), category,
   summary_en, summary_ne, confidence ("high"|"medium"), sources[≥2]}.
   day_bs is set ONLY when a source explicitly gave the BS month/day.
   A few entries have BOTH year_bs and date_ad null (the year lives only
   in the title/summary text, e.g. Gorkha Kingdom founded 1559): they
   render gracefully (never "null"), sort last, and are excluded from
   On This Day, the My Day digest and quiz mode — there is no date to
   reveal. Entries with day_bs null but a year/date are likewise excluded
   from the recurring views (they cannot recur by BS day) but DO appear
   in the Dates view and in quiz mode (they have a date to reveal).
   BS day-32 rule: day_bs is month/day only, so validity is 1-32 — the
   same honest bound birthday.js uses (BS_MONTH_LEN covers 2083/2084
   only, so no exact month-length check is possible for most years). */
const HISTORY_CATEGORIES = ['nepal-history', 'world-history', 'nepal-institutions', 'constitution', 'international'];
const AD_MONTH_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const AD_MONTH_NE = ['जनवरी', 'फेब्रुअरी', 'मार्च', 'अप्रिल', 'मे', 'जुन', 'जुलाइ', 'अगस्ट', 'सेप्टेम्बर', 'अक्टोबर', 'नोभेम्बर', 'डिसेम्बर'];
function historyCategoryLabel(c){
  return c === 'nepal-history' ? B('Nepal History', 'नेपालको इतिहास')
    : c === 'world-history' ? B('World History', 'विश्व इतिहास')
    : c === 'nepal-institutions' ? B('Nepal Institutions', 'नेपालका संस्थाहरू')
    : c === 'constitution' ? B('Constitution', 'संविधान')
    : B('International', 'अन्तर्राष्ट्रिय');
}
function historyById(id){ return (HISTORY || []).find(e => e && e.id === id); }
// True when the entry has any date to show/reveal (BS day, BS year or AD).
function historyHasDate(e){ return !!(e && (e.day_bs || e.year_bs || e.date_ad)); }
// Display date, never "null": full BS date when day+year are known, BS
// month/day when the year is unknown, BS year alone, AD date alone, or ''
// when the year lives only in the title/summary text.
function historyDateLabel(e){
  if (!e) return '';
  if (e.day_bs && e.year_bs) return fmtBs(e.year_bs + '-' + e.day_bs);
  if (e.day_bs){
    const p = String(e.day_bs).split('-'); const m = +p[0], d = +p[1];
    if (m < 1 || m > 12 || !(d >= 1)) return '';
    return lang === 'ne' ? neDigits(d) + ' ' + BS_MONTH_NE[m - 1] : d + ' ' + BS_MONTH_EN[m - 1];
  }
  // BS year + exact AD date: show both (e.g. Everest — 2010 BS · 29 May
  // 1953). Either half alone would hide a date the student is asked for.
  const ad = e.date_ad ? historyAdLabel(e.date_ad) : '';
  if (e.year_bs && ad) return (lang === 'ne' ? neDigits(e.year_bs) : String(e.year_bs)) + ' BS · ' + ad;
  if (e.year_bs) return lang === 'ne' ? neDigits(e.year_bs) : String(e.year_bs);
  if (ad) return ad;
  return '';
}
// "4 March 1816" / "४ मार्च १८१६" — '' when the AD date is malformed.
function historyAdLabel(s){
  const p = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || '');
  if (!p) return '';
  const m = +p[2];
  if (m < 1 || m > 12) return '';
  return lang === 'ne'
    ? neDigits(+p[3]) + ' ' + AD_MONTH_NE[m - 1] + ' ' + neDigits(p[1])
    : (+p[3]) + ' ' + AD_MONTH_EN[m - 1] + ' ' + p[1];
}
// Chronological by BS month/day first, then BS year, then AD date, then
// dateless entries last (title tiebreak — deterministic, no crash on nulls).
function historySorted(list){
  const key = e => {
    if (e.day_bs) return [0, String(e.day_bs), e.title_en || ''];
    if (e.year_bs) return [1, String(e.year_bs).padStart(4, '0'), e.title_en || ''];
    if (e.date_ad) return [2, String(e.date_ad), e.title_en || ''];
    return [3, '', e.title_en || ''];
  };
  return (list || []).slice().sort((a, b) => {
    const ka = key(a), kb = key(b);
    if (ka[0] !== kb[0]) return ka[0] - kb[0];
    if (ka[1] !== kb[1]) return ka[1] < kb[1] ? -1 : 1;
    return ka[2] < kb[2] ? -1 : (ka[2] > kb[2] ? 1 : 0);
  });
}
// Events whose day_bs month/day matches todayBs (any year) — the recurring
// set for On This Day and the My Day digest. todayBs null → [].
function historyEventsToday(history, todayBs){
  const t = bsParse(todayBs || ''); if (!t) return [];
  const md = String(t.m).padStart(2, '0') + '-' + String(t.d).padStart(2, '0');
  return (history || []).filter(e => e && e.day_bs === md);
}
// Quiz pool: only entries with a date to reveal (dateless entries excluded).
function historyQuizPool(history){ return (history || []).filter(historyHasDate); }
function historyMatches(e, q){
  if (!q) return true;
  return [e.title_en, e.title_ne, e.summary_en, e.summary_ne].join(' ').toLowerCase().includes(q);
}
function historyTitle(e){ return esc(lang === 'ne' ? (e.title_ne || e.title_en) : (e.title_en || '')); }
function historySummary(e){ return esc(lang === 'ne' ? (e.summary_ne || e.summary_en) : (e.summary_en || '')); }
// One expandable row: date + title, tap to reveal the bilingual summary +
// sources. Dateless entries show a muted note instead of a date — never null.
function historyRowHtml(e){
  const date = historyDateLabel(e);
  const head = date
    ? `<strong>${esc(date)}</strong> — ${historyTitle(e)}`
    : `<span class="muted">${esc(B('Year in the summary below', 'वर्ष तलको सारांशमा छ'))}</span> — ${historyTitle(e)}`;
  const conf = e.confidence === 'medium' ? ` · ⚠️ ${B('re-verify', 'पुनःपुष्टि')}` : '';
  const srcs = Array.isArray(e.sources) && e.sources.length
    ? `<p class="muted">${B('Sources', 'स्रोतहरू')}: ${e.sources.map((s, i) => `<a href="${esc(s)}" target="_blank" rel="noopener">${i + 1}</a>`).join(' · ')}</p>` : '';
  return `<details class="card hist-row"><summary><span class="chip hist-badge">📜 ${esc(historyCategoryLabel(e.category))}</span> ${head}<span class="muted">${conf}</span></summary>
    <p>${historySummary(e)}</p>${srcs}</details>`;
}
// ---- "On This Day" card on Home (below the festival + birthday cards) ----
// Renders nothing when no historical event falls on today's BS month/day.
function renderHistoryOtd(){
  const box = document.getElementById('history-otd-card'); if (!box) return;
  if (!dataReady){ box.innerHTML = ''; return; }
  const today = bsToday(); if (!today){ box.innerHTML = ''; return; }
  const list = historyEventsToday(HISTORY, today);
  if (!list.length){ box.innerHTML = ''; return; }
  box.innerHTML = `<div class="card hist-otd"><h2>📜 ${B('On This Day', 'आजको दिनमा')}</h2>
    <p class="muted">${esc(fmtBs(today))} — ${B('on this day in history', 'इतिहासमा आजको दिन')}</p>
    <div class="hist-list">${list.map(historyRowHtml).join('')}</div>
    <p><button class="btn secondary" onclick="showView('history')">${B('All dates to remember →', 'सबै सम्झनुपर्ने मितिहरू →')}</button></p></div>`;
}
// ---- "Dates to Remember" view ----
let histFilter = '', histQuery = '';
let histQuizMode = false;
let histQuiz = { pool: [], idx: 0, revealed: false, correct: 0, missed: 0 };
function historyQuizState(){ return { mode: histQuizMode, pool: histQuiz.pool.slice(), idx: histQuiz.idx, revealed: histQuiz.revealed, correct: histQuiz.correct, missed: histQuiz.missed }; }
function historyQuizStart(pool){
  histQuiz = { pool: shuffle((pool || []).slice()), idx: 0, revealed: false, correct: 0, missed: 0 };
  histQuizMode = true;
}
function historyQuizReveal(){ if (histQuiz.pool.length) histQuiz.revealed = true; }
function historyQuizMark(gotIt){
  if (!histQuiz.revealed || !histQuiz.pool.length || histQuiz.idx >= histQuiz.pool.length) return;
  if (gotIt) histQuiz.correct++; else histQuiz.missed++;
  histQuiz.idx++; histQuiz.revealed = false;
}
function historyQuizReset(){ histQuiz = { pool: [], idx: 0, revealed: false, correct: 0, missed: 0 }; histQuizMode = false; }
function historyFiltered(){
  const q = (histQuery || '').trim().toLowerCase();
  return historySorted(HISTORY).filter(e => (!histFilter || e.category === histFilter) && historyMatches(e, q));
}
function renderHistory(){
  const box = document.getElementById('history-box'); if (!box) return;
  if (!dataReady){ box.innerHTML = skelBlock(2); return; }
  const catOpts = HISTORY_CATEGORIES.map(c =>
    `<option value="${esc(c)}"${histFilter === c ? ' selected' : ''}>${esc(historyCategoryLabel(c))} (${HISTORY.filter(e => e.category === c).length})</option>`).join('');
  const quizBtn = histQuizMode
    ? `<button class="btn secondary" onclick="historyQuizReset();renderHistory()">${B('← Back to list', '← सूचीमा फर्कनुहोस्')}</button>`
    : `<button class="btn" onclick="historyQuizStart(historyQuizPool(HISTORY));renderHistory()">🎴 ${B('Quiz me', 'मलाई प्रश्न गर्नुहोस्')}</button>`;
  box.innerHTML = `<div class="card"><h2>📜 ${B('Dates to Remember', 'इतिहासका मिति')}</h2>
    <p class="muted">${B('Verified historical dates for Lok Sewa GK — Nepal\'s history and constitutions, its institutions, and world history. Tap a row to read the story. Dates recur every year on their Bikram Sambat day.', 'लोक सेवा GK का लागि प्रमाणित ऐतिहासिक मितिहरू — नेपालको इतिहास र संविधान, संस्थाहरू र विश्व इतिहास। कथा पढ्न पङ्क्तिमा थिच्नुहोस्। मितिहरू हरेक वर्ष विक्रम संवत्कै दिन दोहोरिन्छन्।')}</p>
    <p class="muted">${HISTORY.length} ${B('dates', 'मितिहरू')} · ${B('verified against at least 2 sources each — see', 'प्रत्येक कम्तीमा २ स्रोतसँग प्रमाणित — हेर्नुहोस्')} <span class="mono">data/SOURCES.md §19</span></p>
    <label for="hist-search">${B('Search', 'खोज्नुहोस्')}</label>
    <input type="search" id="hist-search" placeholder="${esc(B('e.g. Constitution, Everest, Rana…', 'जस्तै संविधान, सगरमाथा, राणा…'))}" value="${esc(histQuery)}" oninput="histQuery=this.value;renderHistoryList()">
    <label for="hist-cat">${B('Category', 'श्रेणी')}</label>
    <select id="hist-cat" onchange="histFilter=this.value;renderHistoryList()"><option value="">${B('All categories', 'सबै श्रेणी')}</option>${catOpts}</select>
    <p>${quizBtn}</p></div>
    <div id="history-list"></div>`;
  renderHistoryList();
}
function renderHistoryList(){
  const listEl = document.getElementById('history-list'); if (!listEl) return;
  if (histQuizMode){
    const total = histQuiz.pool.length;
    if (!total){
      listEl.innerHTML = emptyState('🎴', B('Nothing to quiz yet', 'प्रश्न गर्न केही छैन'),
        B('No dated events are loaded, so there is nothing to quiz on.', 'मिति भएका घटना लोड भएका छैनन्, त्यसैले प्रश्न गर्न केही छैन।'));
      return;
    }
    if (histQuiz.idx >= total){
      listEl.innerHTML = `<div class="card hist-quiz"><h3>🎉 ${B('Quiz done!', 'क्विज सकियो!')}</h3>
        <p><strong>${histQuiz.correct} / ${total}</strong> ${B('correct', 'सही')} · ${histQuiz.missed} ${B('missed', 'छुट्यो')}</p>
        <p><button class="btn" onclick="historyQuizStart(historyQuizPool(HISTORY));renderHistory()">🔀 ${B('Quiz again', 'फेरि प्रश्न गर्नुहोस्')}</button>
        <button class="btn secondary" onclick="historyQuizReset();renderHistory()">${B('Back to list', 'सूचीमा फर्कनुहोस्')}</button></p></div>`;
      return;
    }
    const e = histQuiz.pool[histQuiz.idx];
    const date = historyDateLabel(e);
    listEl.innerHTML = `<div class="card hist-quiz"><p class="muted">${B('Question', 'प्रश्न')} ${histQuiz.idx + 1} / ${total} · ✓ ${histQuiz.correct} · ✗ ${histQuiz.missed}</p>
      <h3>${historyTitle(e)}</h3>
      <p class="muted">${esc(historyCategoryLabel(e.category))}</p>
      <p><strong>${B('When did this happen?', 'यो कहिले भयो?')}</strong></p>
      ${histQuiz.revealed
        ? `<p class="hist-answer">${esc(date)}</p><p>${historySummary(e)}</p>
           <p><button class="btn" onclick="historyQuizMark(true);renderHistoryList()">✅ ${B('Got it', 'मिल्यो')}</button>
           <button class="btn secondary" onclick="historyQuizMark(false);renderHistoryList()">❌ ${B('Missed it', 'छुट्यो')}</button></p>`
        : `<p><button class="btn" onclick="historyQuizReveal();renderHistoryList()">👁️ ${B('Reveal the date', 'मिति देखाउनुहोस्')}</button></p>`}
      <p><button class="btn secondary" onclick="historyQuizReset();renderHistoryList()">${B('Reset quiz', 'क्विज रिसेट गर्नुहोस्')}</button></p></div>`;
    return;
  }
  const list = historyFiltered();
  if (!list.length){
    listEl.innerHTML = emptyState('📜', B('No dates match', 'कुनै मिति मिलेन'),
      B('Try a different search or category.', 'अर्को खोजी वा श्रेणी प्रयास गर्नुहोस्।'));
    return;
  }
  listEl.innerHTML = `<p class="muted">${list.length} ${B(list.length > 1 ? 'dates' : 'date', 'मिति')}</p><div class="hist-list">${list.map(historyRowHtml).join('')}</div>`;
}

/* ================= Theory courses =================
   Chapter-wise bilingual theory (data/courses/*.json, listed in
   COURSE_FILES). Progress lives in localStorage under COURSE_PROG_KEY:
   {done:{chapterId:true}, last:{exam, chId, ts}}. Nothing here touches the
   network — pure local reading + deep-links into practice. */
const COURSE_PROG_KEY='loksewa_course_progress_v1';
// Course exam id (data/courses) -> practice-exam select value (exams.json).
const COURSE_EXAM_MAP={kharidar:'kharidar','nayab-subba':'nasu','section-officer':'section-officer'};
// Navigation state for the courses view (exam id / subject idx / chapter id).
let courseNav={exam:null,subject:-1,chapter:null};

// --- Pure helpers (exported for tests) ---
function courseByExam(id){ return (COURSES||[]).find(c=>c.exam===id)||null; }
function flattenCourseChapters(course){
  const out=[];
  (course.subjects||[]).forEach((s,si)=>(s.chapters||[]).forEach(ch=>out.push({subject:s,subjectIdx:si,ch})));
  return out;
}
function courseChapterById(course,id){ return flattenCourseChapters(course).find(x=>x.ch.id===id)||null; }
function calcCourseProgress(course,doneMap){
  const flat=flattenCourseChapters(course);
  const done=flat.filter(x=>doneMap&&doneMap[x.ch.id]).length;
  return {total:flat.length,done,pct:flat.length?Math.round(done/flat.length*100):0};
}
function subjectProgress(subject,doneMap){
  const total=(subject.chapters||[]).length;
  const done=(subject.chapters||[]).filter(ch=>doneMap&&doneMap[ch.id]).length;
  return {total,done,pct:total?Math.round(done/total*100):0};
}
// --- Progress store (localStorage) ---
function courseProgLoad(){ try{ const p=JSON.parse(localStorage.getItem(COURSE_PROG_KEY)||'{}'); return {done:(p&&p.done)||{},last:(p&&p.last)||null}; }catch(e){ return {done:{},last:null}; } }
function courseProgSave(p){ try{ localStorage.setItem(COURSE_PROG_KEY,JSON.stringify(p)); }catch(e){} }
function isChapterDone(id){ return !!courseProgLoad().done[id]; }
function setChapterDone(id,done){
  const p=courseProgLoad();
  if(done){ p.done[id]=true; } else { delete p.done[id]; }
  courseProgSave(p);
}
function ringSvg(pct,size){
  size=size||64; const r=(size-10)/2, c=2*Math.PI*r, off=c*(1-Math.max(0,Math.min(100,pct))/100);
  return `<svg class="ring" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" role="img" aria-label="${Math.round(pct)}% complete"><circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="var(--border)" stroke-width="8"/><circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="var(--accent)" stroke-width="8" stroke-linecap="round" stroke-dasharray="${c.toFixed(1)}" stroke-dashoffset="${off.toFixed(1)}" transform="rotate(-90 ${size/2} ${size/2})"/><text x="50%" y="50%" dy=".35em" text-anchor="middle" class="ring-txt">${Math.round(pct)}%</text></svg>`;
}
function courseBar(pct){
  return `<div class="course-bar" role="progressbar" aria-valuenow="${Math.round(pct)}" aria-valuemin="0" aria-valuemax="100"><span style="width:${Math.max(0,Math.min(100,pct))}%"></span></div>`;
}
function courseTitleOf(course){ return lang==='ne'?(course.exam_name_ne||course.exam_name_en):course.exam_name_en; }
function courseChTitle(ch){ return lang==='ne'?(ch.title_ne||ch.title_en):ch.title_en; }
function courseSubjName(s){ return lang==='ne'?(s.name_ne||s.name_en):s.name_en; }

// --- Courses view ---
function renderCourses(){
  const box=document.getElementById('courses-box'); if(!box) return;
  if(!dataReady){ box.innerHTML=`<p class="muted">${B('Loading courses…','पाठ्यक्रम लोड हुँदै…')}</p>`; return; }
  if(!COURSES.length){ box.innerHTML=`<div class="empty-state"><div class="empty-icon">📚</div><h3>${B('No courses yet','अझै पाठ्यक्रम छैन')}</h3><p class="muted">${B('Theory courses are on the way.','सैद्धान्तिक पाठ्यक्रमहरू आउँदैछन्।')}</p></div>`; return; }
  if(courseNav.chapter){ renderCourseChapter(box); return; }
  if(courseNav.exam){ renderCourseDetail(box); return; }
  // Exam picker.
  const prog=courseProgLoad();
  box.innerHTML=`<h2>📚 ${B('Theory Courses','सैद्धान्तिक पाठ्यक्रम')}</h2>
  <p class="muted">${B('Read the theory chapter by chapter, then jump straight into practice. Progress is saved on this device.','अध्यायअनुसार सिद्धान्त पढ्नुहोस्, अनि सिधै अभ्यासमा जानुहोस्। प्रगति यसै डिभाइसमा सेभ हुन्छ।')}</p>
  <div class="grid">${COURSES.map(c=>{
    const st=calcCourseProgress(c,prog.done);
    const conf=c.confidence==='medium'?` <span class="chip">⚠️ ${B('syllabus: re-verify','पाठ्यक्रम: पुनःपुष्टि')}</span>`:'';
    return `<div class="card course-card"><div class="course-card-top">${ringSvg(st.pct)}
      <div><strong>${esc(courseTitleOf(c))}</strong><p class="muted">${esc(lang==='ne'?'प्रथम पत्र — सिद्धान्त':'First Paper — Theory')}${conf}</p>
      <p class="muted">${st.done}/${st.total} ${B('chapters read','अध्याय पढियो')}</p></div></div>
      <button class="btn" onclick="openCourseExam('${esc(c.exam)}')">${st.done>0?B('Continue','जारी राख्नुहोस्'):B('Start studying','पढ्न सुरु गर्नुहोस्')}</button></div>`;
  }).join('')}</div>`;
}
function openCourseExam(examId){ courseNav={exam:examId,subject:-1,chapter:null}; renderCourses(); }
function toggleCourseSubject(si){ courseNav.subject=(courseNav.subject===si?-1:si); courseNav.chapter=null; renderCourses(); }
function renderCourseDetail(box){
  const course=courseByExam(courseNav.exam);
  if(!course){ courseNav={exam:null,subject:-1,chapter:null}; renderCourses(); return; }
  const prog=courseProgLoad();
  const st=calcCourseProgress(course,prog.done);
  const subjHtml=course.subjects.map((s,si)=>{
    const sp=subjectProgress(s,prog.done);
    const open=courseNav.subject===si;
    const rows=open?s.chapters.map(ch=>{
      const done=!!prog.done[ch.id];
      return `<button class="ch-row${done?' done':''}" onclick="openCourseChapter('${esc(ch.id)}')">
        <span class="ch-tick">${done?'✅':'⬜'}</span>
        <span class="ch-title">${esc(courseChTitle(ch))}</span>
        <span class="muted">${(ch.key_points||[]).length} ${B('key points','मुख्य बुँदा')}</span>
        <span class="ch-go">›</span></button>`;
    }).join(''):'';
    return `<div class="card subj-card"><button class="subj-head" onclick="toggleCourseSubject(${si})" aria-expanded="${open}">
      <span><strong>${esc(courseSubjName(s))}</strong> <span class="muted">${sp.done}/${sp.total}</span></span>
      <span class="subj-right">${courseBar(sp.pct)}<span class="subj-chev">${open?'▾':'▸'}</span></span></button>
      ${open?`<div class="ch-list">${rows}</div>`:''}</div>`;
  }).join('');
  box.innerHTML=`<button class="linklike" onclick="openCourseExam(null);courseNav={exam:null,subject:-1,chapter:null};renderCourses()">← ${B('All courses','सबै पाठ्यक्रम')}</button>
  <h2>${esc(courseTitleOf(course))}</h2>
  <p class="muted">${esc(lang==='ne'?(course.paper||''):'')||esc(course.paper||'')}</p>
  <div class="card"><div class="course-card-top">${ringSvg(st.pct,72)}<div><strong>${st.pct}% ${B('complete','पूरा')}</strong><p class="muted">${st.done}/${st.total} ${B('chapters','अध्याय')}</p></div></div>${courseBar(st.pct)}</div>
  ${subjHtml}`;
}
function openCourseChapter(chId){
  const course=courseByExam(courseNav.exam); if(!course) return;
  const found=courseChapterById(course,chId); if(!found) return;
  courseNav.chapter=chId; courseNav.subject=found.subjectIdx;
  const p=courseProgLoad(); p.last={exam:course.exam,chId,ts:Date.now()}; courseProgSave(p);
  renderCourses();
}
function renderCourseChapter(box){
  const course=courseByExam(courseNav.exam);
  const found=course?courseChapterById(course,courseNav.chapter):null;
  if(!found){ courseNav.chapter=null; renderCourses(); return; }
  const {subject,s,ch}=found;
  const flat=flattenCourseChapters(course);
  const idx=flat.findIndex(x=>x.ch.id===ch.id);
  const prev=flat[idx-1], next=flat[idx+1];
  const done=isChapterDone(ch.id);
  const theory=(lang==='ne'?(ch.theory_ne||ch.theory_en):(ch.theory_en||ch.theory_ne))||'';
  const paras=theory.split(/\n\s*\n/).map(p=>`<p>${esc(p.trim())}</p>`).join('');
  const kps=(ch.key_points||[]).map(k=>`<li>${esc(lang==='ne'?(k.ne||k.en):(k.en||k.ne))}</li>`).join('');
  const topics=(ch.linked_topics||[]).map(t=>`<button class="btn secondary btn-sm" onclick="practiceChapterTopic('${esc(t)}')">✏️ ${esc(t)}</button>`).join('');
  box.innerHTML=`<button class="linklike" onclick="courseNav.chapter=null;renderCourses()">← ${esc(courseSubjName(subject))}</button>
  <article class="chapter-reader">
    <p class="muted">${esc(courseTitleOf(course))} · ${esc(courseSubjName(subject))}</p>
    <h2>${esc(courseChTitle(ch))}</h2>
    <div class="chapter-body">${paras}</div>
    ${kps?`<div class="keypoints"><h3>⭐ ${B('Key points','मुख्य बुँदाहरू')}</h3><ul>${kps}</ul></div>`:''}
    ${topics?`<div class="chapter-practice"><h3>✏️ ${B('Practice this chapter','यो अध्याय अभ्यास गर्नुहोस्')}</h3><div class="chip-row">${topics}</div></div>`:''}
    <div class="chapter-actions">
      <button class="btn${done?' secondary':''}" onclick="toggleChapterRead()">${done?`✅ ${B('Read — mark unread','पढियो — नपढेको चिन्ह')}`:`📖 ${B('Mark as read','पढेको चिन्ह लगाउनुहोस्')}`}</button>
    </div>
    <nav class="chapter-nav">
      ${prev?`<button class="btn secondary" onclick="openCourseChapter('${esc(prev.ch.id)}')">← ${esc(courseChTitle(prev.ch))}</button>`:'<span></span>'}
      ${next?`<button class="btn secondary" onclick="openCourseChapter('${esc(next.ch.id)}')">${esc(courseChTitle(next.ch))} →</button>`:'<span></span>'}
    </nav>
  </article>`;
}
function toggleChapterRead(){
  const id=courseNav.chapter; if(!id) return;
  setChapterDone(id,!isChapterDone(id));
  renderCourses();
  renderContinueStudying();
}
function practiceChapterTopic(topic){
  const examId=COURSE_EXAM_MAP[courseNav.exam]||'';
  const sel=document.getElementById('practice-exam');
  if(sel&&examId) sel.value=examId;
  startPracticeTopic(topic);
}
// --- Home "Continue studying" card ---
function renderContinueStudying(){
  const box=document.getElementById('continue-studying-box'); if(!box) return;
  const p=courseProgLoad();
  const last=p.last;
  const course=last?courseByExam(last.exam):null;
  const found=course?courseChapterById(course,last.chId):null;
  if(!found){ box.hidden=true; box.innerHTML=''; return; }
  const st=calcCourseProgress(course,p.done);
  if(st.done>=st.total){ box.hidden=true; box.innerHTML=''; return; }
  box.hidden=false;
  box.innerHTML=`<div class="continue-flex"><div><strong>📚 ${B('Continue studying','पढाइ जारी राख्नुहोस्')}</strong>
    <p class="muted">${esc(courseTitleOf(course))} — ${esc(courseChTitle(found.ch))} · ${st.pct}% ${B('complete','पूरा')}</p></div>
    <button class="btn" onclick="courseNav={exam:'${esc(course.exam)}',subject:${found.subjectIdx},chapter:'${esc(found.ch.id)}'};showView('courses')">${B('Resume','सुरु गर्नुहोस्')}</button></div>`;
}

// Node exports (test harness): kept at the END of the file so every const
// above (incl. FOCUS_DURATIONS) is initialised before this object is built.
// An export placed near the top threw "Cannot access before initialization".
if (typeof module!=='undefined' && module.exports){ module.exports={shuffle,shuffleOptions,scoreAttempt,xpFor,qText,qOpts,qExpl,getLang,setLang,normaliseText,tokenJaccard,jaccardNorm,findDuplicate,validateSubmission,rateLimitCheck,isGmailAddress,communityBadge,seedDiscussions,weekStartStr,questionsThisWeek,weeklyProgress,personalBest,questionsInADay,pickSurprise,nextFocusMode,FOCUS_DURATIONS,badges,checkWeeklyGoal,funFactText,dailyFunFact,randomFunFact,PRAISE_LINES,TRY_AGAIN_LINES,PASS_LINES,FAIL_LINES,pickLine,prefersReducedMotion,recordFactVisit,getFactStreak,questionOfDay,speedBonusFor,mistakePool,longestStreak,bestDay,personalRecords,buildShareText,getSpeedBest,saveSpeedBest,SPEED_SECONDS,SPEED_COUNT,effectiveNoticeStatus,resetProgress,
chatReply,chatTopicFor,chatTopicStats,isFactualQuestion,chatHistory,saveChatHistory,chatSend,
validateSuggestion,isDuplicateSuggestion,loadSuggestions,saveSuggestions,upvoteSuggestion,LS_CHAT,LS_SUGGEST,CHAT_MAX_MSGS,B,examName,fmt1,markPyqFlags,topicsForExam,mapTopicToSyllabus,breakdownLabelTopics,parseBreakdownWeights,pyqTopicShares,examTopicWeights,practiceTopicStats,attemptLevelTotals,guessEV,evVerdict,coachStats,coachAdvice,drillTopic,renderCoverage,renderPrint,generatePrintPaper,renderPrintPaperHtml,renderPlanner,renderCoach,renderPYQ,heatCell,buildStudyPlan,daysUntil,rebalancePlan,loadPlans,savePlans,planNotices,currentPlanTarget,generatePlan,deletePlan,showPlan,renderPlanCard,NOTICE_EXAM,PLANS_KEY,TOPIC_SYLLABUS_KEYS,BREAKDOWN_GROUPS,
bsParse,bsAbsDay,bsFromAbs,BS_ANCHOR_ABS,bsToday,bsDaysUntil,neDigits,fmtBs,bsCountdown,upcomingExamDates,examDateById,renderExamReminder,dismissReminder,goPracticeExam,goMockExam,renderExamDates,toggleExamReminder,enableExamNotifications,checkExamNotifications,remStore,remSave,REM_DISMISSED,REM_LIST,REM_NOTIFIED,REM_ASKED,remKindLabel,remChip,nxTargetMs,nxRemaining,nxPad,nxPagerList,nxCardState,nxPick,nxCycle,renderNextExamCard,renderNextExamCompact,COURSE_FILES,COURSE_PROG_KEY,COURSE_EXAM_MAP,courseByExam,flattenCourseChapters,courseChapterById,calcCourseProgress,subjectProgress,
HISTORY_CATEGORIES,historyCategoryLabel,historyById,historyHasDate,historyDateLabel,historyAdLabel,historySorted,historyEventsToday,historyQuizPool,historyMatches,historyQuizStart,historyQuizReveal,historyQuizMark,historyQuizReset,historyQuizState,renderHistory,renderHistoryList,renderHistoryOtd}; }
