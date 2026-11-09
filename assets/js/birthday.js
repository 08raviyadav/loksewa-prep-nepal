/* ---------- Birthday wishes + "My Day" digest ----------
   Own file (kept separate from app.js so the parallel festival-wishes work
   can land without clobbering). Uses app.js globals: B, esc, bsParse,
   bsToday, fmtBs, neDigits, BS_MONTH_EN, BS_MONTH_NE, BS_MONTH_LEN,
   examById, goPracticeExam, goMockExam, remKindLabel, remStore, remSave,
   dataReady, skelBlock, emptyState, launchConfetti, saveProgress,
   progress, showView. Loaded AFTER app.js (see index.html).

   Birthday storage: progress.birthday (BS 'YYYY-MM-DD' or ''), added by
   migrateProgress() in app.js — same local profile store as name/email
   (loksewa_progress_v1). On this device only, never uploaded.
   Dismiss store: loksewa_birthday_dismissed_v1 = {date_bs} for the day.
   Festivals (data/festivals.json) are read lazily and ONLY if the file
   exists — the digest degrades gracefully to exams + birthday alone.
   The festival-wishes agent owns data/festivals.json; this file never
   writes it. */
const BDAY_DISMISSED = 'loksewa_birthday_dismissed_v1';
const BDAY_MIN_YEAR = 2040, BDAY_MAX_YEAR = 2083;
let BIRTHDAY_FESTIVALS = null; // null = not tried yet; [] = absent/unreadable
let bdayConfettiDone = false;
let todayTab = 'today', todaySelYear = null, todaySelMonth = null;

/* ---- Pure helpers (exported for tests) ---- */
// BS day must be 1-32: every BS month is 29-32 days, and birth years can be
// any year 2040-2083 — but BS_MONTH_LEN only covers 2083/2084, so an exact
// month-length check is impossible for most birth years. 1-32 is the honest
// bound; a day that doesn't exist in a given year simply never matches.
function birthdayIsValid(s){
  const p = bsParse(s); if (!p) return false;
  if (p.y < BDAY_MIN_YEAR || p.y > BDAY_MAX_YEAR) return false;
  if (p.m < 1 || p.m > 12) return false;
  if (p.d < 1 || p.d > 32) return false;
  return true;
}
function birthdayIsToday(birthday, todayBs){
  const b = bsParse(birthday || ''), t = bsParse(todayBs || '');
  if (!b || !t) return false;
  return b.m === t.m && b.d === t.d;
}
// Age in BS years on todayBs. null when the birthday is unparseable or in
// the future. Explicit todayBs keeps this pure and testable.
function birthdayAge(birthday, todayBs){
  const b = bsParse(birthday || ''), t = bsParse(todayBs || '');
  if (!b || !t) return null;
  let age = t.y - b.y;
  if (t.m < b.m || (t.m === b.m && t.d < b.d)) age--;
  return age < 0 ? null : age;
}
// Last BS day of a month, or null when the year has no verified lengths.
function birthdayMonthLen(y, m){
  const lens = BS_MONTH_LEN[y]; if (!lens || m < 1 || m > 12) return null;
  return lens[m - 1];
}
// Normalise a festival entry to a {start, end} BS window (or null).
// Accepts start_bs/end_bs (festival spec) or a single date_bs.
function festivalWindow(f){
  if (!f) return null;
  if (f.start_bs && f.end_bs) return { start: f.start_bs, end: f.end_bs };
  if (f.date_bs) return { start: f.date_bs, end: f.date_bs };
  return null;
}
const BDAY_KIND_ORDER = { birthday: 0, exam: 1, deadline: 2, festival: 3 };
function bdaySortEvents(a, b){
  if (a.date_bs !== b.date_bs) return a.date_bs < b.date_bs ? -1 : 1;
  const ka = BDAY_KIND_ORDER[a.kind] ?? 9, kb = BDAY_KIND_ORDER[b.kind] ?? 9;
  if (ka !== kb) return ka - kb;
  return (a.title_en || '') < (b.title_en || '') ? -1 : 1;
}
// All digest events for one BS day. exams = EXAMDATES entries,
// festivals = festivals.json entries (or []), birthday = 'YYYY-MM-DD'|''.
function digestEventsForDay(exams, festivals, birthday, todayBs){
  const out = [];
  if (birthdayIsToday(birthday, todayBs)){
    const age = birthdayAge(birthday, todayBs);
    out.push({ kind: 'birthday', date_bs: todayBs,
      title_en: 'Your birthday' + (age === null ? '' : ' — you turn ' + age),
      title_ne: 'तपाईंको जन्मदिन' + (age === null ? '' : ' — ' + neDigits(age) + ' वर्ष') });
  }
  (exams || []).forEach(e => {
    if (!e || e.date_bs !== todayBs) return;
    out.push({ kind: e.kind === 'deadline' ? 'deadline' : 'exam', date_bs: e.date_bs,
      title_en: e.title_en || '', title_ne: e.title_ne || e.title_en || '',
      examId: e.exam || null, source: e.source || '', id: e.id || '' });
  });
  (festivals || []).forEach(f => {
    const w = festivalWindow(f); if (!w) return;
    if (w.start <= todayBs && todayBs <= w.end)
      out.push({ kind: 'festival', date_bs: todayBs,
        title_en: f.name_en || '', title_ne: f.name_ne || f.name_en || '' });
  });
  return out.sort(bdaySortEvents);
}
// All digest events in one BS month. Birthday included when the birth
// month/day falls inside the month (and the day exists in that month).
function digestEventsForMonth(exams, festivals, birthday, year, month){
  const len = birthdayMonthLen(year, month);
  if (len === null || month < 1 || month > 12) return [];
  const mm = String(month).padStart(2, '0');
  const start = year + '-' + mm + '-01', end = year + '-' + mm + '-' + String(len).padStart(2, '0');
  const out = [];
  const b = bsParse(birthday || '');
  if (b && b.m === month && b.d <= len){
    const d = year + '-' + mm + '-' + String(b.d).padStart(2, '0');
    const age = year - b.y;
    out.push({ kind: 'birthday', date_bs: d,
      title_en: 'Your birthday — you turn ' + age,
      title_ne: 'तपाईंको जन्मदिन — ' + neDigits(age) + ' वर्ष' });
  }
  (exams || []).forEach(e => {
    if (!e || !e.date_bs || e.date_bs < start || e.date_bs > end) return;
    out.push({ kind: e.kind === 'deadline' ? 'deadline' : 'exam', date_bs: e.date_bs,
      title_en: e.title_en || '', title_ne: e.title_ne || e.title_en || '',
      examId: e.exam || null, source: e.source || '', id: e.id || '' });
  });
  (festivals || []).forEach(f => {
    const w = festivalWindow(f); if (!w) return;
    if (w.start <= end && w.end >= start)
      out.push({ kind: 'festival', date_bs: w.start < start ? start : w.start,
        title_en: f.name_en || '', title_ne: f.name_ne || f.name_en || '' });
  });
  return out.sort(bdaySortEvents);
}
// Month-by-month summary for one BS year: counts per kind + birthday flag.
// Festivals count in their start month only (a window spanning two months
// is not double-counted). Returns [] when the year has no verified lengths.
function digestYearSummary(exams, festivals, birthday, year){
  const lens = BS_MONTH_LEN[year]; if (!lens) return [];
  const b = bsParse(birthday || '');
  const rows = [];
  for (let m = 1; m <= 12; m++){
    const mm = String(m).padStart(2, '0');
    const start = year + '-' + mm + '-01', end = year + '-' + mm + '-' + String(lens[m - 1]).padStart(2, '0');
    let ex = 0, dl = 0;
    (exams || []).forEach(e => {
      if (!e || !e.date_bs || e.date_bs < start || e.date_bs > end) return;
      if (e.kind === 'deadline') dl++; else ex++;
    });
    let fe = 0;
    (festivals || []).forEach(f => {
      const w = festivalWindow(f); if (!w) return;
      if (w.start >= start && w.start <= end) fe++;
    });
    rows.push({ month: m, exams: ex, deadlines: dl, festivals: fe,
      birthday: !!(b && b.m === m) });
  }
  return rows;
}

/* ---- Festivals (lazy, optional) ---- */
// The festival-wishes agent owns data/festivals.json. If it isn't there
// yet (or never lands), the digest simply shows exams + birthday.
function loadFestivalsForDigest(){
  if (BIRTHDAY_FESTIVALS !== null) return;
  BIRTHDAY_FESTIVALS = [];
  // Prefer the app.js FESTIVALS global (loaded by loadData() in both web
  // and single-file-bundle modes) — no extra fetch. Then the embedded
  // bundle data, then a direct fetch as a last resort.
  if (typeof FESTIVALS !== 'undefined' && Array.isArray(FESTIVALS) && FESTIVALS.length){
    BIRTHDAY_FESTIVALS = FESTIVALS.slice();
    return;
  }
  if (typeof window !== 'undefined' && Array.isArray(window.EMBEDDED_FESTIVALS)){
    BIRTHDAY_FESTIVALS = window.EMBEDDED_FESTIVALS.slice();
    return;
  }
  if (typeof fetch !== 'function') return;
  fetch('data/festivals.json').then(r => r.json()).then(arr => {
    BIRTHDAY_FESTIVALS = Array.isArray(arr) ? arr : [];
    const v = document.getElementById('view-today');
    if (v && v.classList && v.classList.contains('active')) renderToday();
  }).catch(() => { BIRTHDAY_FESTIVALS = []; });
}

/* ---- Birthday card on Home ---- */
function renderBirthdayCard(){
  const box = document.getElementById('birthday-card-box'); if (!box) return;
  const bd = (typeof progress !== 'undefined' && progress) ? (progress.birthday || '') : '';
  const today = bsToday();
  if (!bd || !birthdayIsToday(bd, today)){ box.innerHTML = ''; return; }
  const dismissed = remStore(BDAY_DISMISSED, {});
  if (dismissed && dismissed.date_bs === today){ box.innerHTML = ''; return; }
  const age = birthdayAge(bd, today);
  const name = esc((typeof progress !== 'undefined' && progress.name) || B('friend', 'साथी'));
  box.innerHTML = `<div class="bday-card" role="alert">
    <button class="bday-x" onclick="dismissBirthdayCard()" aria-label="${B('Dismiss', 'हटाउनुहोस्')}">✕</button>
    <div class="bday-cake" aria-hidden="true">🎂</div>
    <h2>${B('Happy Birthday, ', 'जन्मदिनको शुभकामना, ')}${name}! 🎉</h2>
    <p class="bday-age">${age === null ? '' : B('You turn ' + age + ' today!', 'आज तपाईं ' + neDigits(age) + ' वर्षको हुनुभयो!')}</p>
    <p class="muted">${B('May this year bring you the exam result you have worked for — and many more candles to count.', 'यो वर्ष तपाईंको मेहनतले चाहेको नतिजा ल्याओस् — जन्मदिनको धेरै धेरै शुभकामना!')}</p>
    <p><button class="btn secondary" onclick="showView('today')">${B('See your day →', 'आजको दिन हेर्नुहोस् →')}</button></p>
  </div>`;
  if (!bdayConfettiDone){
    bdayConfettiDone = true;
    if (typeof launchConfetti === 'function') launchConfetti();
  }
}
function dismissBirthdayCard(){
  remSave(BDAY_DISMISSED, { date_bs: bsToday() });
  renderBirthdayCard();
}

/* ---- Birthday editor in the Profile view ---- */
function birthdayEditorHtml(){
  const bd = (typeof progress !== 'undefined' && progress) ? (progress.birthday || '') : '';
  const cur = bsParse(bd);
  const years = [];
  for (let y = BDAY_MAX_YEAR; y >= BDAY_MIN_YEAR; y--) years.push(y);
  const months = BS_MONTH_EN.map((m, i) =>
    `<option value="${i + 1}"${cur && cur.m === i + 1 ? ' selected' : ''}>${lang === 'ne' ? BS_MONTH_NE[i] : m}</option>`).join('');
  const days = [];
  for (let d = 1; d <= 32; d++)
    days.push(`<option value="${d}"${cur && cur.d === d ? ' selected' : ''}>${lang === 'ne' ? neDigits(d) : d}</option>`);
  return `<div class="card"><h3>🎂 ${B('Birthday', 'जन्मदिन')}</h3>
  <p class="muted">${B('Add your Bikram Sambat birthday and we will wish you on the day — and show it in your My Day digest.', 'तपाईंको विक्रम संवत् जन्मदिन थप्नुहोस् — जन्मदिनमा हामी शुभकामना दिनेछौं र तपाईंको My Day मा देखाउनेछौं।')}</p>
  <p class="muted"><strong>${B('Stays on this device only — never uploaded.', 'यो डिभाइसमा मात्र रहन्छ — कहिल्यै अपलोड हुँदैन।')}</strong></p>
  <p>${B('Saved birthday', 'सेभ गरिएको जन्मदिन')}: <strong>${bd ? esc(fmtBs(bd)) : B('Not set', 'सेट गरिएको छैन')}</strong></p>
  <div class="bday-picker">
  <label>${B('Year', 'वर्ष')} <select id="bd-year">${years.map(y => `<option value="${y}"${cur && cur.y === y ? ' selected' : ''}>${lang === 'ne' ? neDigits(y) : y}</option>`).join('')}</select></label>
  <label>${B('Month', 'महिना')} <select id="bd-month">${months}</select></label>
  <label>${B('Day', 'गते')} <select id="bd-day">${days.join('')}</select></label>
  </div>
  <p class="error-text" id="bd-error"></p>
  <p><button class="btn" onclick="saveBirthdayFromProfile()">${B('Save birthday', 'जन्मदिन सेभ गर्नुहोस्')}</button>
  ${bd ? ` <button class="btn secondary" onclick="clearBirthdayFromProfile()">${B('Remove birthday', 'जन्मदिन हटाउनुहोस्')}</button>` : ''}</p>
  </div>`;
}
function saveBirthdayFromProfile(){
  const y = document.getElementById('bd-year'), m = document.getElementById('bd-month'), d = document.getElementById('bd-day');
  const err = document.getElementById('bd-error');
  const s = y.value + '-' + String(+m.value).padStart(2, '0') + '-' + String(+d.value).padStart(2, '0');
  if (!birthdayIsValid(s)){
    if (err) err.textContent = B('Please pick a valid BS date (year 2040–2083, month 1–12, day 1–32).', 'कृपया मान्य वि.सं. मिति छान्नुहोस् (वर्ष २०४०–२०८३, महिना १–१२, गते १–३२)।');
    return;
  }
  progress.birthday = s; saveProgress();
  if (err) err.textContent = '';
  renderProfile(); renderBirthdayCard();
}
function clearBirthdayFromProfile(){
  progress.birthday = ''; saveProgress();
  renderProfile(); renderBirthdayCard();
}

/* ---- "My Day" digest view ---- */
function bdayEventRow(e){
  const title = esc(lang === 'ne' ? (e.title_ne || e.title_en) : (e.title_en || ''));
  const chip = e.kind === 'birthday' ? `<span class="chip bday-badge">🎂 ${B('Birthday', 'जन्मदिन')}</span>`
    : e.kind === 'deadline' ? `<span class="chip chip-soon">⏰ ${remKindLabel('deadline')}</span>`
    : e.kind === 'festival' ? `<span class="chip chip-soon">🎉 ${B('Festival', 'चाडपर्व')}</span>`
    : `<span class="chip chip-today">📝 ${remKindLabel('exam')}</span>`;
  const ex = e.examId && typeof examById === 'function' ? examById(e.examId) : null;
  const acts = [];
  if (ex) acts.push(`<button class="btn secondary" onclick="goPracticeExam('${esc(ex.id)}')">${B('Practice', 'अभ्यास')}</button>`);
  if (ex && ex.prelim) acts.push(` <button class="btn secondary" onclick="goMockExam('${esc(ex.id)}')">${B('Mock', 'मक')}</button>`);
  if (e.source) acts.push(` <a class="btn secondary" href="${esc(e.source)}" target="_blank" rel="noopener">${B('Source', 'स्रोत')}</a>`);
  return `<div class="card today-event">${chip}
    <div class="today-main"><strong>${title}</strong>
    <p class="muted">${esc(fmtBs(e.date_bs))}${e.kind === 'birthday' ? '' : ' · ' + (e.kind === 'festival' ? B('Festival', 'चाडपर्व') : remKindLabel(e.kind))}</p>
    ${acts.length ? `<p class="ed-actions">${acts.join('')}</p>` : ''}</div></div>`;
}
function renderToday(){
  const box = document.getElementById('today-box'); if (!box) return;
  if (!dataReady){ box.innerHTML = skelBlock(2); return; }
  loadFestivalsForDigest();
  const t = bsToday(), tp = bsParse(t);
  if (todaySelYear === null){ todaySelYear = tp ? tp.y : 2083; }
  if (todaySelMonth === null){ todaySelMonth = tp ? tp.m : 7; }
  const bd = (typeof progress !== 'undefined' && progress) ? (progress.birthday || '') : '';
  const festivals = BIRTHDAY_FESTIVALS || [];
  const tabs = `<div class="today-tabs" role="tablist">
    <button class="today-tab${todayTab === 'today' ? ' active' : ''}" onclick="todayTab='today';renderToday()">${B('Today', 'आज')}</button>
    <button class="today-tab${todayTab === 'month' ? ' active' : ''}" onclick="todayTab='month';renderToday()">${B('Month', 'महिना')}</button>
    <button class="today-tab${todayTab === 'year' ? ' active' : ''}" onclick="todayTab='year';renderToday()">${B('Year', 'वर्ष')}</button>
  </div>`;
  let h = `<div class="card"><h2>🎂 ${B('My Day — what is happening when?', 'मेरो दिन — के कहिले हुँदैछ?')}</h2>
  <p class="muted">${B('Your exams, festivals, deadlines and birthday — today, this month, this year. All dates in Bikram Sambat.', 'तपाईंका परीक्षा, चाडपर्व, अन्तिम मिति र जन्मदिन — आज, यो महिना, यो वर्ष। सबै मिति विक्रम संवत्मा छन्।')}</p>${tabs}`;
  if (todayTab === 'today'){
    const events = digestEventsForDay(EXAMDATES, festivals, bd, t);
    h += `<p><strong>${esc(fmtBs(t))}</strong> · ${B('Today', 'आज')}</p>`;
    if (!events.length){
      h += emptyState('🌿', B('Quiet day — nothing scheduled', 'शान्त दिन — केही तय छैन'),
        B('No exam, festival, deadline or birthday today. A good day to get ahead on practice.', 'आज परीक्षा, चाडपर्व, अन्तिम मिति वा जन्मदिन छैन। अभ्यासमा अगाडि बढ्ने राम्रो दिन।'),
        B('Practice now', 'अहिले अभ्यास गर्नुहोस्'), "showView('practice')");
    } else {
      h += '<div class="today-list">' + events.map(bdayEventRow).join('') + '</div>';
    }
    if (!bd) h += `<p class="muted">${B('Tip: add your birthday in Profile and it will show up here on the day.', 'सुझाव: प्रोफाइलमा तपाईंको जन्मदिन थप्नुहोस् — जन्मदिनमा यो यहाँ देखिनेछ।')} <button class="linklike" onclick="showView('profile')">${B('Add birthday', 'जन्मदिन थप्नुहोस्')}</button></p>`;
  } else if (todayTab === 'month'){
    const years = Object.keys(BS_MONTH_LEN).map(Number);
    const yOpts = years.map(y => `<option value="${y}"${y === todaySelYear ? ' selected' : ''}>${lang === 'ne' ? neDigits(y) : y}</option>`).join('');
    const mOpts = BS_MONTH_EN.map((m, i) =>
      `<option value="${i + 1}"${i + 1 === todaySelMonth ? ' selected' : ''}>${lang === 'ne' ? BS_MONTH_NE[i] : m}</option>`).join('');
    h += `<p><label>${B('Year', 'वर्ष')} <select onchange="todaySelYear=+this.value;renderToday()">${yOpts}</select></label>
    <label>${B('Month', 'महिना')} <select onchange="todaySelMonth=+this.value;renderToday()">${mOpts}</select></label></p>`;
    const events = digestEventsForMonth(EXAMDATES, festivals, bd, todaySelYear, todaySelMonth);
    if (!events.length){
      h += emptyState('🗓️', B('Nothing this month', 'यो महिना केही छैन'),
        B('No exam, festival, deadline or birthday in this month.', 'यो महिनामा परीक्षा, चाडपर्व, अन्तिम मिति वा जन्मदिन छैन।'));
    } else {
      h += `<p class="muted">${events.length} ${B(events.length > 1 ? 'events' : 'event', 'कार्यक्रम')}</p><div class="today-list">` + events.map(bdayEventRow).join('') + '</div>';
    }
  } else {
    const years = Object.keys(BS_MONTH_LEN).map(Number);
    const yOpts = years.map(y => `<option value="${y}"${y === todaySelYear ? ' selected' : ''}>${lang === 'ne' ? neDigits(y) : y}</option>`).join('');
    h += `<p><label>${B('Year', 'वर्ष')} <select onchange="todaySelYear=+this.value;renderToday()">${yOpts}</select></label></p>`;
    const rows = digestYearSummary(EXAMDATES, festivals, bd, todaySelYear);
    if (!rows.length){
      h += emptyState('🗓️', B('Year not supported yet', 'यो वर्ष अझै समर्थित छैन'),
        B('The BS calendar here covers 2083–2084 only.', 'यहाँको वि.सं. पात्रोले २०८३–२०८४ मात्र समेट्छ।'));
    } else {
      h += '<div class="today-list">';
      rows.forEach(r => {
        const total = r.exams + r.deadlines + r.festivals;
        h += `<div class="card today-event"><div class="today-main"><strong>${lang === 'ne' ? BS_MONTH_NE[r.month - 1] : BS_MONTH_EN[r.month - 1]} ${lang === 'ne' ? neDigits(todaySelYear) : todaySelYear}</strong>
        <p class="muted">${total === 0 ? B('Nothing scheduled', 'केही तय छैन') :
          [r.exams ? r.exams + ' ' + B(r.exams > 1 ? 'exams' : 'exam', 'परीक्षा') : '',
           r.deadlines ? r.deadlines + ' ' + B(r.deadlines > 1 ? 'deadlines' : 'deadline', 'अन्तिम मिति') : '',
           r.festivals ? r.festivals + ' ' + B(r.festivals > 1 ? 'festivals' : 'festival', 'चाडपर्व') : ''].filter(Boolean).join(' · ')}</p>
        ${r.birthday ? `<p><span class="chip bday-badge">🎂 ${B('Your birthday month', 'तपाईंको जन्मदिनको महिना')}</span></p>` : ''}</div></div>`;
      });
      h += '</div>';
    }
  }
  h += `<p class="muted">${B('Exam boards reschedule — always confirm on the official site before travelling.', 'परीक्षा बोर्डले मिति सार्न सक्छ — यात्रा गर्नुअघि आधिकारिक साइटमा पुष्टि गर्नुहोस्।')}</p></div>`;
  box.innerHTML = h;
}
