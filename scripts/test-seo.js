/* SEO basics + print watermark checks: robots/sitemap files, index.html meta +
   JSON-LD + analytics beacon, og-image PNG, printable mock watermark and
   attribution footer (rendered through the real renderPrintPaperHtml).
   Node, no deps. Usage: node scripts/test-seo.js */
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
let fail = 0;
function check(name, ok, extra = '') { console.log((ok ? 'PASS' : 'FAIL') + '  ' + name + (extra ? ' — ' + extra : '')); if (!ok) fail++; }
const CANON = 'https://08raviyadav.github.io/loksewa-prep-nepal/';

// 1. robots.txt
const robots = fs.readFileSync(path.join(root, 'robots.txt'), 'utf8');
check('robots.txt allows all', robots.includes('User-agent: *') && robots.includes('Allow: /'));
check('robots.txt points at the canonical sitemap', robots.includes('Sitemap: ' + CANON + 'sitemap.xml'));

// 2. sitemap.xml — well-formed single-URL sitemap
const sitemap = fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8');
check('sitemap.xml has XML declaration + urlset', sitemap.startsWith('<?xml') && sitemap.includes('<urlset') && sitemap.includes('</urlset>'));
let balanced = true;
for (const t of ['urlset', 'url', 'loc', 'lastmod']) {
  const open = (sitemap.match(new RegExp('<' + t + '[ >]', 'g')) || []).length;
  const close = (sitemap.match(new RegExp('</' + t + '>', 'g')) || []).length;
  if (open !== close || open === 0) balanced = false;
}
check('sitemap.xml tags balance (urlset/url/loc/lastmod)', balanced);
check('sitemap.xml lists the canonical homepage', sitemap.includes('<loc>' + CANON + '</loc>'));
check('sitemap.xml has a lastmod', /<lastmod>\d{4}-\d{2}-\d{2}<\/lastmod>/.test(sitemap));

// 3. index.html — canonical, JSON-LD, og/twitter image, keywords, beacon
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
check('index.html has the canonical link', html.includes('<link rel="canonical" href="' + CANON + '">'));
const ldMatch = html.match(/<script type="application\/ld\+json">\s*([\s\S]*?)\s*<\/script>/);
let ld = null;
try { ld = ldMatch && JSON.parse(ldMatch[1]); } catch (e) { ld = null; }
check('index.html has parseable JSON-LD', !!ld);
if (ld) {
  check('JSON-LD is a WebApplication named Outrank', ld['@type'] === 'WebApplication' && ld.name === 'Outrank', JSON.stringify({ t: ld['@type'], n: ld.name }));
  check('JSON-LD category is EducationalApplication', ld.applicationCategory === 'EducationalApplication');
  check('JSON-LD operatingSystem is Any', ld.operatingSystem === 'Any');
  check('JSON-LD is free (price 0)', ld.offers && ld.offers.price === '0');
  check('JSON-LD is bilingual (en + ne)', Array.isArray(ld.inLanguage) && ld.inLanguage.includes('en') && ld.inLanguage.includes('ne'));
  check('JSON-LD author is Ravi Yadav', ld.author && ld.author.name === 'Ravi Yadav');
}
check('index.html has absolute og:image', html.includes('<meta property="og:image" content="' + CANON + 'assets/og-image.png">'));
check('index.html has absolute twitter:image', html.includes('<meta name="twitter:image" content="' + CANON + 'assets/og-image.png">'));
const kw = (html.match(/<meta name="keywords" content="([^"]*)">/) || [])[1] || '';
check('keywords include Nepali + Roman search terms', kw.includes('लोक सेवा तयारी') && kw.includes('kharidar tayari') && kw.includes('psc nepal'), kw.slice(0, 60) + '…');
check('index.html has the Cloudflare beacon with a real 32-hex token', html.includes("src='https://static.cloudflareinsights.com/beacon.min.js'") && html.includes("type='module'") && /"token": "[0-9a-f]{32}"/.test(html) && !html.includes('__CLOUDFLARE_TOKEN__'));

// 4. og-image.png — valid PNG, 1200x630, sane size
const ogPath = path.join(root, 'assets/og-image.png');
const og = fs.readFileSync(ogPath);
const pngSig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
check('og-image.png has a valid PNG signature', og.slice(0, 8).equals(pngSig));
check('og-image.png is 1200x630', og.readUInt32BE(16) === 1200 && og.readUInt32BE(20) === 630, og.readUInt32BE(16) + 'x' + og.readUInt32BE(20));
check('og-image.png size is sane (5KB–1MB)', og.length > 5000 && og.length < 1000000, Math.round(og.length / 1024) + ' KB');

// 5. Printable mock — render the real paper and check watermark + attribution
const src = fs.readFileSync(path.join(root, 'assets/js/app.js'), 'utf8');
const sandbox = { module: { exports: {} }, console,
  localStorage: { _s: {}, getItem(k) { return (k in this._s) ? this._s[k] : null; }, setItem(k, v) { this._s[k] = String(v); }, removeItem(k) { delete this._s[k]; } },
  document: { addEventListener: () => {}, querySelector: () => null, querySelectorAll: () => [], getElementById: () => null },
  window: { scrollTo: () => {} }, alert: () => {}, fetch: async () => { throw new Error('no fetch in test'); },
  scrollTo: () => {},
  setInterval: () => 0, clearInterval: () => {}, setTimeout: () => 0, clearTimeout: () => {} };
sandbox.window = sandbox;
vm.createContext(sandbox);
try { vm.runInContext(src + '\nmodule.exports={renderPrintPaperHtml};', sandbox); check('app.js parses for print render', true); }
catch (e) { check('app.js parses for print render', false, e.message); process.exit(1); }
const { renderPrintPaperHtml } = sandbox.module.exports;
const runInApp = code => vm.runInContext(code, sandbox);
runInApp('EXAMS=[{id:"kharidar",name:"Kharidar",name_ne:"खरिदार",prelim:{questions:2,marksPerQ:2,timeMin:45,pass:45,total:100,negative:0.2}}]');
runInApp('printPaper={exam:"kharidar",qs:[{id:"Q1",question:"What is 2+2?",options:["3","4","5","6"],answer:1},{id:"Q2",question:"Capital of Nepal?",options:["Pokhara","Kathmandu","Biratnagar","Butwal"],answer:1}],short:false,pool:100}');
const paper = renderPrintPaperHtml();
check('paper still renders its questions', paper.includes('What is 2+2?') && paper.includes('Capital of Nepal?'));
check('paper still has the OMR sheet + answer key', paper.includes('omr-page') && paper.includes('key-page'));
check('paper has the print-watermark element', paper.includes('class="print-watermark"'));
check('watermark tiles 7 rows of the GitHub ID + brand', (paper.match(/class="wm-row"/g) || []).length === 7 && (paper.match(/08raviyadav • OUTRANK/g) || []).length === 28);
check('paper has the attribution footer', paper.includes('class="paper-attribution"'));
check('attribution has the Nepali line', paper.includes('यो पेपर Outrank बाट उत्पन्न गरिएको हो'));
check('attribution names the GitHub ID + copyright', paper.includes('github.com/08raviyadav') && paper.includes('© 2026 Ravi Yadav'));
check('attribution warns against redistribution', paper.includes('For personal practice only. Do not redistribute without credit.'));
check('attribution falls back to the canonical URL with no window.location', paper.includes(CANON));
// Live-origin path: with a location set, the footer uses it instead.
runInApp("location={origin:'https://example.test',pathname:'/x/'}");
check('attribution uses the live site origin when available', renderPrintPaperHtml().includes('https://example.test/x/'));

// 6. style.css — watermark hidden on screen, fixed + colour-forced in print
const css = fs.readFileSync(path.join(root, 'assets/css/style.css'), 'utf8');
check('style.css hides the watermark on screen', /\.print-watermark\{display:none\}/.test(css));
const printBlock = (css.match(/@media print\{([\s\S]*?)\n\}/) || [])[1] || '';
check('print CSS shows the watermark fixed (repeats every page)', printBlock.includes('.print-watermark') && printBlock.includes('position:fixed'));
check('print CSS forces the watermark colours to print', printBlock.includes('print-color-adjust:exact'));
check('print CSS rotates the watermark rows', printBlock.includes('rotate(-30deg)'));
check('print CSS keeps the paper-only rule', printBlock.includes('#view-print{display:block!important}'));

console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL SEO CHECKS PASSED ✔');
process.exit(fail ? 1 : 0);
