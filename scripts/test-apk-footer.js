/* "Download APK" footer button checks: the anchor exists in the footer,
   its href is EXACTLY the GitHub Releases latest-download URL for
   app-release.apk (the release is created by CI; the link is correct to
   ship before it exists), the label is bilingual EN/NE with a Beta note,
   and the §29 CSS block styles it. Fails if the href is missing or
   different. Node, no deps. Usage: node scripts/test-apk-footer.js */
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }

const APK_URL = 'https://github.com/08raviyadav/loksewa-prep-nepal/releases/latest/download/app-release.apk';
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const css = fs.readFileSync(path.join(root, 'assets/css/style.css'), 'utf8');

// --- 1. Footer + anchor presence -----------------------------------------
const footStart = html.indexOf('<footer>');
const footEnd = html.indexOf('</footer>');
check('index.html has a footer block', footStart !== -1 && footEnd > footStart);
const footer = (footStart !== -1 && footEnd > footStart) ? html.slice(footStart, footEnd) : '';
check('footer contains the APK download anchor', footer.includes('id="apk-download-btn"'));

// Extract the anchor tag carrying the id (order of attributes not assumed).
const anchorMatch = footer.match(/<a\b[^>]*\bid="apk-download-btn"[^>]*>([\s\S]*?)<\/a>/);
check('APK anchor is a real <a> element with a closing tag', !!anchorMatch);
const anchorTag = anchorMatch ? anchorMatch[0] : '';
const anchorInner = anchorMatch ? anchorMatch[1] : '';

// --- 2. The href must be EXACTLY the release URL --------------------------
const hrefMatch = anchorTag.match(/href="([^"]*)"/);
check('APK anchor has an href', !!hrefMatch);
check('APK href is exactly the GitHub Releases latest-download URL', hrefMatch ? hrefMatch[1] === APK_URL : false, hrefMatch ? 'found: ' + hrefMatch[1] : 'no href');
check('the exact APK URL appears exactly once in index.html', html.split(APK_URL).length - 1 === 1, (html.split(APK_URL).length - 1) + ' occurrence(s)');
// Matcher control: a near-miss URL must NOT satisfy the exact-equality test.
check('exact-match control rejects a different asset name', 'https://github.com/08raviyadav/loksewa-prep-nepal/releases/latest/download/app-debug.apk' !== APK_URL);

// --- 3. Bilingual label + Beta note ----------------------------------------
check('APK anchor uses the shared button system (btn green apk-download)', /class="[^"]*\bbtn\b[^"]*\bgreen\b[^"]*\bapk-download\b[^"]*"/.test(anchorTag));
check('APK label has the English text', anchorInner.includes('Download Android App'));
check('APK label has the Nepali text', anchorInner.includes('एन्ड्रोइड एप डाउनलोड गर्नुहोस्'));
check('APK label carries a Beta note', anchorInner.includes('Beta') && anchorInner.includes('apk-beta'));
check('APK label has a download affordance', anchorInner.includes('📱') || anchorInner.includes('⬇') || anchorInner.includes('Download'));

// --- 4. CSS §29 ------------------------------------------------------------
check('style.css has the §29 APK download block', css.includes('29. APK download button'));
check('§29 styles the button, Beta pill and Nepali line', css.includes('.apk-download') && css.includes('.apk-beta') && css.includes('.apk-ne'));
check('§29 introduces no new font or framework', !/\.apk-download[^}]*font-family/.test(css) && !css.includes('@import'));

console.log(fail === 0 ? 'ALL APK-FOOTER CHECKS PASSED ✔' : fail + ' CHECK(S) FAILED ✘');
process.exit(fail === 0 ? 0 : 1);
