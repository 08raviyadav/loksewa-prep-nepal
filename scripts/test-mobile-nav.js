/* Mobile navigation checks (2026-11-16): the hamburger menu, the mobile
   panel contents, the mock-table card layout, the bottom-nav scroll strip,
   and the toggle behaviour in a fake-DOM vm sandbox. Node, no deps.
   The Node sandbox can't do layout — these assert structure/behaviour, not
   pixels; the parent re-checks the real rendering in a browser.
   Usage: node scripts/test-mobile-nav.js */
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const css = fs.readFileSync(path.join(root, 'assets/css', 'style.css'), 'utf8');
const src = fs.readFileSync(path.join(root, 'assets/js', 'app.js'), 'utf8');

// --- 1. Hamburger button + mobile menu markup -------------------------
check('hamburger button exists with aria-controls + aria-expanded=false',
  html.includes('id="nav-toggle"') && html.includes('aria-controls="mobile-menu"') && html.includes('aria-expanded="false"'));
check('mobile menu panel exists, hidden by default', html.includes('id="mobile-menu"') && html.includes('class="mobile-menu" id="mobile-menu" hidden'));
const menuBlock = html.slice(html.indexOf('id="mobile-menu"'), html.indexOf('</header>'));
const mainViews = ['home', 'practice', 'mock', 'dashboard', 'auth', 'profile'];
const moreViews = ['coverage', 'planner', 'coach', 'pyq', 'notes', 'audio', 'funfacts',
  'guide', 'papers', 'notices', 'examdates', 'history', 'today', 'courses', 'print', 'search', 'review',
  'discuss', 'submit', 'suggest', 'chat', 'moderate'];
const missingMain = mainViews.filter(v => !menuBlock.includes(`data-view="${v}"`));
const missingMore = moreViews.filter(v => !menuBlock.includes(`data-view="${v}"`));
check('mobile menu lists all 6 main nav items', missingMain.length === 0, missingMain.join(', '));
check('mobile menu lists all 22 More items inline (no nested dropdown)', missingMore.length === 0, missingMore.join(', '));
check('mobile menu keeps the STUDY / RESOURCES / COMMUNITY group labels',
  menuBlock.includes('>Study<') && menuBlock.includes('>Resources<') && menuBlock.includes('>Community<'));
check('theme + language buttons live inside the mobile menu',
  menuBlock.includes('id="mobile-theme-toggle"') && menuBlock.includes('id="mobile-lang-toggle"'));
check('mobile Sign In button has its own id (no duplicate nav-auth-btn)',
  menuBlock.includes('id="mobile-auth-btn"') && (html.match(/id="nav-auth-btn"/g) || []).length === 1);
['nav-toggle', 'mobile-menu', 'mobile-theme-toggle', 'mobile-lang-toggle', 'mobile-auth-btn', 'ask-fab', 'mobile-header-theme-toggle', 'mobile-header-lang-toggle'].forEach(id => {
  check(`id "${id}" occurs exactly once in index.html`, (html.match(new RegExp(`id="${id}"`, 'g')) || []).length === 1);
});
check('Ask FAB exists, opens the chat view, labelled for screen readers',
  html.includes('id="ask-fab"') && html.includes(`onclick="showView('chat')"`) && html.includes('aria-label="Ask Ravi'));
check('compact theme + language icon buttons sit in the phone header, before the hamburger',
  html.includes('id="mobile-header-theme-toggle"') && html.includes('id="mobile-header-lang-toggle"') &&
  html.indexOf('id="mobile-header-theme-toggle"') < html.indexOf('id="nav-toggle"') &&
  html.indexOf('id="mobile-header-lang-toggle"') < html.indexOf('id="nav-toggle"'));
// Desktop nav + More dropdown untouched.
check('desktop More dropdown markup unchanged (button + 3-col menu still present)',
  html.includes('id="nav-more-btn"') && html.includes('id="nav-more-menu"') && html.includes('class="nav-dropdown"'));
check('every More item still exists in the desktop dropdown too (appears before the mobile menu in the document)',
  moreViews.every(v => html.indexOf(`data-view="${v}"`) !== -1 && html.indexOf(`data-view="${v}"`) < html.indexOf('id="mobile-menu"')));

// --- 2. CSS rules ------------------------------------------------------
check('hamburger hidden on desktop, shown at phone width',
  css.includes('.nav-toggle{display:none}') && css.includes('@media(max-width:768px)'));
check('desktop nav row + header buttons hide at ≤768px (header stays one row)',
  css.includes('.nav>nav{display:none}') && css.includes('.nav .head-btn{display:none}'));
check('mobile menu panel shows only when not [hidden] at ≤768px',
  css.includes('.mobile-menu:not([hidden]){display:block}'));
check('root-cause rule removed: header nav no longer gets overflow-x:auto',
  !css.includes('header nav{flex-wrap:nowrap;overflow-x:auto'));
check('mock table becomes labelled cards at ≤768px (all 6 column labels)',
  ['Mock', 'Questions', 'Time', 'Marks/Q', 'Pass', 'Negative'].every((label, i) =>
    css.includes(`#mock-pattern-table td:nth-child(${i + 1})::before{content:"${label}"}`)));
check('mock table card layout hides the header row + drops the 520px min-width',
  css.includes('#mock-pattern-table tr:first-child{display:none}') && css.includes('#mock-pattern-table table{min-width:0}'));
check('mock table card CSS is scoped to #mock-pattern-table (other tables untouched)',
  !css.includes('.table-wrap table{display:block}') && css.includes('#mock-pattern-table .table-wrap{overflow:visible}'));
check('bottom quick nav is a scroll-snap strip with readable labels',
  css.includes('scroll-snap-type:x proximity') && css.includes('.mobile-nav button span{font-size:.72rem'));
check('main clips horizontal overflow (no page-level sideways scroll)',
  css.includes('overflow-x:clip'));
check('Ask FAB is a fixed orange pill, hidden by .off, above the bottom bar on phones, never printed',
  css.includes('.ask-fab{') && css.includes('position:fixed') && css.includes('.ask-fab.off{display:none}') &&
  css.includes('.ask-fab{bottom:calc(80px + env(safe-area-inset-bottom,0px))}') && css.includes('#ask-fab,#confetti-layer'));
check('showView syncs the Ask FAB (hides it on the chat view itself)',
  src.includes('syncAskFab(false)') && src.includes('function syncAskFab'));
check('phone header icon buttons hidden on desktop, shown at ≤768px, theme button pushes the group right',
  css.includes('.head-icon-btn{display:none}') && css.includes('.head-icon-btn{') &&
  css.includes('#mobile-header-theme-toggle{margin-left:auto}'));
check('applyTheme / setLang sync the phone header icon buttons too',
  src.includes(`getElementById('mobile-header-theme-toggle')`) && src.includes(`getElementById('mobile-header-lang-toggle')`));

// --- 3. Behaviour in a fake-DOM vm sandbox -----------------------------
function fakeEl(id) {
  const attrs = new Map(), listeners = {}, cls = new Set();
  return {
    id, dataset: {}, textContent: '', _focused: false,
    getAttribute(n) { return attrs.has(n) ? attrs.get(n) : null; },
    setAttribute(n, v) { attrs.set(n, String(v)); },
    removeAttribute(n) { attrs.delete(n); },
    hasAttribute(n) { return attrs.has(n); },
    classList: {
      add(c) { cls.add(c); }, remove(c) { cls.delete(c); },
      toggle(c, f) { if (f === undefined) { cls.has(c) ? cls.delete(c) : cls.add(c); } else if (f) cls.add(c); else cls.delete(c); },
      contains(c) { return cls.has(c); }
    },
    addEventListener(t, fn) { (listeners[t] = listeners[t] || []).push(fn); },
    querySelectorAll() { return []; },
    focus() { this._focused = true; },
    closest() { return null; },
    _fire(t, ev) { (listeners[t] || []).forEach(fn => fn(ev || {})); },
    click() { this._fire('click', { stopPropagation() {} }); }
  };
}
const toggleBtn = fakeEl('nav-toggle');
toggleBtn.setAttribute('aria-expanded', 'false');
toggleBtn.setAttribute('aria-label', 'Open menu');
const menuEl = fakeEl('mobile-menu');
menuEl.setAttribute('hidden', '');
const practiceBtn = fakeEl('practice-btn');
practiceBtn.dataset.view = 'practice';
menuEl.querySelectorAll = () => [practiceBtn];
const mobileThemeBtn = fakeEl('mobile-theme-toggle');
const mobileLangBtn = fakeEl('mobile-lang-toggle');
const mobileAuthBtn = fakeEl('mobile-auth-btn');
const fabEl = fakeEl('ask-fab');
const chatViewEl = fakeEl('view-chat');
const headerThemeBtn = fakeEl('mobile-header-theme-toggle');
const headerLangBtn = fakeEl('mobile-header-lang-toggle');
const docListeners = {};
const sandbox = { module: { exports: {} },
  // Quiet console.warn: loadData() warns once per question file when fetch
  // throws in this sandbox (100+ lines of noise, all expected).
  console: { ...console, warn() {} },
  localStorage: { _s: {}, getItem(k) { return (k in this._s) ? this._s[k] : null; }, setItem(k, v) { this._s[k] = String(v); }, removeItem(k) { delete this._s[k]; } },
  document: {
    title: '',
    documentElement: { dataset: {} },
    addEventListener(t, fn) { (docListeners[t] = docListeners[t] || []).push(fn); },
    querySelector: () => null, querySelectorAll: () => [],
    getElementById(id) {
      return { 'nav-toggle': toggleBtn, 'mobile-menu': menuEl, 'mobile-theme-toggle': mobileThemeBtn,
        'mobile-lang-toggle': mobileLangBtn, 'mobile-auth-btn': mobileAuthBtn, 'ask-fab': fabEl,
        'view-chat': chatViewEl, 'mobile-header-theme-toggle': headerThemeBtn,
        'mobile-header-lang-toggle': headerLangBtn }[id] || null;
    }
  },
  window: { scrollTo: () => {} }, alert: () => {}, fetch: async () => { throw new Error('no fetch in test'); },
  scrollTo: () => {},
  setInterval: () => 0, clearInterval: () => {}, setTimeout: () => 0, clearTimeout: () => {} };
sandbox.window = sandbox;
vm.createContext(sandbox);
let unhandled = null;
process.on('unhandledRejection', e => { unhandled = e; });
try {
  vm.runInContext(src + '\nmodule.exports={setMobileMenuOpen,toggleMobileMenu,applyTheme,setLang,toggleTheme,showView,getLang,syncAskFab};', sandbox);
  check('app.js parses in the mobile-nav sandbox', true);
} catch (e) { check('app.js parses in the mobile-nav sandbox', false, e.message); process.exit(1); }
const exp = sandbox.module.exports;
const isOpen = () => !menuEl.hasAttribute('hidden') && toggleBtn.getAttribute('aria-expanded') === 'true';

check('initial state: menu hidden, toggle collapsed', !isOpen());
exp.toggleMobileMenu();
check('toggle opens: hidden removed, aria-expanded true, .open class, label flips to Close menu',
  isOpen() && toggleBtn.classList.contains('open') && toggleBtn.getAttribute('aria-label') === 'Close menu');
exp.toggleMobileMenu();
check('toggle again closes: hidden set, aria-expanded false, .open removed, label back to Open menu',
  !isOpen() && !toggleBtn.classList.contains('open') && toggleBtn.getAttribute('aria-label') === 'Open menu');
exp.setMobileMenuOpen(true);
check('setMobileMenuOpen(true) opens directly', isOpen());
exp.setMobileMenuOpen(false);
check('setMobileMenuOpen(false) closes directly', !isOpen());

// Fire the real DOMContentLoaded handler, then exercise the real wiring.
(async () => {
  (docListeners.DOMContentLoaded || []).forEach(fn => fn());
  // Let loadData() (fetch throws in this sandbox, all caught) settle.
  await new Promise(r => setTimeout(r, 50));
  check('DOMContentLoaded wiring registered document click + keydown handlers',
    (docListeners.click || []).length >= 1 && (docListeners.keydown || []).length >= 1);
  const fireDoc = (t, ev) => (docListeners[t] || []).forEach(fn => fn(ev));

  toggleBtn.click();
  check('clicking the hamburger opens the menu', isOpen());
  toggleBtn.click();
  check('clicking the hamburger again closes the menu', !isOpen());

  toggleBtn.click();
  fireDoc('keydown', { key: 'Escape' });
  check('Escape closes the menu and returns focus to the toggle', !isOpen() && toggleBtn._focused === true);

  toggleBtn.click();
  fireDoc('click', { target: { closest: () => null } });
  check('outside click closes the menu', !isOpen());

  toggleBtn.click();
  fireDoc('click', { target: { closest: () => ({}) } });
  check('click inside the menu keeps it open', isOpen());

  practiceBtn.click();
  check('tapping a menu item navigates (showView) and closes the menu', !isOpen());

  const fabHidden = () => fabEl.classList.contains('off');
  check('Ask FAB is visible on a normal view', !fabHidden());
  toggleBtn.click();
  check('opening the menu hides the Ask FAB', isOpen() && fabHidden());
  toggleBtn.click();
  check('closing the menu shows the Ask FAB again', !isOpen() && !fabHidden());
  chatViewEl.classList.add('active');
  exp.syncAskFab(false);
  check('Ask FAB hides while the chat view is active', fabHidden());
  chatViewEl.classList.remove('active');
  exp.syncAskFab(false);
  check('Ask FAB returns when leaving the chat view', !fabHidden());

  exp.applyTheme('dark');
  check('applyTheme syncs the mobile theme button label', mobileThemeBtn.textContent === '🌙 Dark');
  check('applyTheme syncs the phone header theme icon too', headerThemeBtn.textContent === '🌙');
  mobileThemeBtn.click();
  check('mobile theme button toggles back to light', mobileThemeBtn.textContent === '☀️ Light');

  exp.setLang('ne');
  check('setLang syncs the mobile language button label', mobileLangBtn.textContent === 'NE · नेपाली' && exp.getLang() === 'ne');
  check('setLang syncs the phone header language icon too', headerLangBtn.textContent === 'NE');
  mobileLangBtn.click();
  check('mobile language button switches back to English', mobileLangBtn.textContent === 'EN · English' && exp.getLang() === 'en');

  check('no unhandled rejection from init/loadData in the sandbox', unhandled === null, unhandled ? String(unhandled) : '');

  console.log(fail === 0 ? '\nAll mobile-nav checks passed.' : `\n${fail} check(s) FAILED.`);
  process.exit(fail ? 1 : 0);
})();
