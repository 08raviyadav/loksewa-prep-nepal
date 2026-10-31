#!/usr/bin/env python3
"""Add Nepali bilingual fields (question_ne / options_ne / explanation_ne) to the
Lok Sewa Prep Nepal question bank.

Method: Google Translate (gtx endpoint, no key) with protection tokens.
  * Date expressions (e.g. "20 September 2015", "Ashoj 3, 2072 BS") are replaced
    by ZZ<n>ZZ tokens before translation and restored afterwards as correct
    Nepali dates -- raw MT mangles months (Sept 20 -> Bhadra 20).
  * In English-grammar/vocabulary questions the English words ARE the content,
    so the question keeps the English sentence with a Nepali instruction, the
    options stay in English, and only the explanation is translated -- with the
    English keywords protected by ZZ tokens so they survive verbatim.
  * Maths/IQ series, coding and analogy questions likewise keep the English
    sequence/code/analogy and get a Nepali instruction; digits are normalised
    back to Arabic numerals in that file (Nepali maths papers use them, and
    the numeric options stay Arabic).
  * Nepali Language questions are already Devanagari: fields are copied.
  * Everything else (GK, constitution, office, banking, education, health,
    computer) is fully translated, option by option.

Usage:  python3 scripts/add-nepali.py data/questions/<file>.json [--dry-run]
Cache:  /tmp/ne_cache.json (MT results keyed by exact input text, so re-runs
        are free and resume after any interruption).
"""
import json, re, sys, os, time, random, urllib.request, urllib.parse, threading
from concurrent.futures import ThreadPoolExecutor

_cache_lock = threading.RLock()
_cache_dirty = [0]

def _save_cache():
    with _cache_lock:
        tmp = CACHE_PATH + '.tmp'
        json.dump(_cache, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False)
        os.replace(tmp, CACHE_PATH)
        _cache_dirty[0] = 0

CACHE_PATH = '/tmp/ne_cache.json'
DEV = '०१२३४५६७८९'
EN_MON = {'january': 'जनवरी', 'february': 'फेब्रुअरी', 'march': 'मार्च',
          'april': 'अप्रिल', 'may': 'मे', 'june': 'जुन', 'july': 'जुलाई',
          'august': 'अगस्ट', 'september': 'सेप्टेम्बर', 'october': 'अक्टोबर',
          'november': 'नोभेम्बर', 'december': 'डिसेम्बर'}
NP_MON = {'baisakh': 'बैशाख', 'jestha': 'जेठ', 'ashadh': 'असार',
          'shrawan': 'साउन', 'bhadra': 'भदौ', 'ashoj': 'असोज',
          'kartik': 'कार्तिक', 'mangsir': 'मंसिर', 'poush': 'पुस',
          'magh': 'माघ', 'falgun': 'फागुन', 'chaitra': 'चैत'}
EN_MON_RE = '|'.join(EN_MON)
NP_MON_RE = '|'.join(NP_MON)

def dev_digits(s):
    # NB: c in '0123456789' (not c.isdigit()): subscript digits like '₂'
    # (U+2082, in number-base / chemistry options) are isdigit()==True but
    # int('₂') raises ValueError and crashed a whole-file run (PDF expansion,
    # expansion-pdf-07.json, 2026-10-27). ASCII digits only here.
    return ''.join(DEV[int(c)] if c in '0123456789' else c for c in str(s))

def en_digits(s):
    return ''.join(str(DEV.index(c)) if c in DEV else c for c in str(s))

def has_dev(s):
    return bool(re.search(r'[\u0900-\u097F]', s or ''))

# ---------------- MT client (cached, threaded, retried) ----------------
_cache = {}
if os.path.exists(CACHE_PATH):
    try:
        _cache = json.load(open(CACHE_PATH, encoding='utf-8'))
    except Exception:
        _cache = {}

def _mt_one(text):
    with _cache_lock:
        if text in _cache:
            return _cache[text]
    url = ('https://translate.googleapis.com/translate_a/single?client=gtx'
           '&sl=en&tl=ne&dt=t&q=' + urllib.parse.quote(text))
    last = None
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as r:
                j = json.load(r)
            out = ''.join(c[0] for c in j[0] if c and c[0])
            if not out.strip():
                raise ValueError('empty translation')
            with _cache_lock:
                _cache[text] = out
                _cache_dirty[0] += 1
                if _cache_dirty[0] >= 25:
                    _save_cache()
            return out
        except Exception as e:
            last = e
            time.sleep(1.5 * (attempt + 1) + random.random())
    raise RuntimeError(f'MT failed for {text!r}: {last}')

def mt_batch(texts):
    """Translate a list of distinct strings (deduped via cache)."""
    todo = sorted({t for t in texts if t and t not in _cache})
    if todo:
        with ThreadPoolExecutor(max_workers=6) as ex:
            list(ex.map(_mt_one, todo))
        json.dump(_cache, open(CACHE_PATH, 'w', encoding='utf-8'),
                  ensure_ascii=False)
    return {t: _cache.get(t, t) for t in texts}

def mt(text):
    return _mt_one(text)

# ---------------- protection tokens ----------------
class Protector:
    """Replace sensitive spans with ZZ<n>ZZ tokens (MT leaves them intact),
    then restore them after translation."""
    def __init__(self):
        self.map = {}
        self.n = 0
    def add(self, value):
        tok = f'ZZ{self.n}ZZ'
        self.n += 1
        self.map[tok] = value
        return tok
    def restore(self, text):
        for tok, val in self.map.items():
            text = text.replace(tok, val)
        return text
    def leftover(self, text):
        return re.findall(r'ZZ\d+ZZ', text)

DATE_RES = [
    # 20 September 2015 / 3 Ashoj 2073 / Ashoj 3, 2072 BS
    (re.compile(r'\b(\d{1,2})\s+(' + EN_MON_RE + r')\s+(\d{4})\b', re.I),
     lambda m: f"{dev_digits(m.group(1))} {EN_MON[m.group(2).lower()]} {dev_digits(m.group(3))}"),
    (re.compile(r'\b(' + EN_MON_RE + r')\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b', re.I),
     lambda m: f"{dev_digits(m.group(2))} {EN_MON[m.group(1).lower()]} {dev_digits(m.group(3))}"),
    (re.compile(r'\b(\d{1,2})\s+(' + NP_MON_RE + r')\s+(\d{4})(\s+B\.?S\.?)?\b', re.I),
     lambda m: f"{dev_digits(m.group(1))} {NP_MON[m.group(2).lower()]} {dev_digits(m.group(3))}" + (' बि.सं.' if m.group(4) else '')),
    (re.compile(r'\b(' + NP_MON_RE + r')\s+(\d{1,2}),?\s+(\d{4})(\s+B\.?S\.?)?\b', re.I),
     lambda m: f"{NP_MON[m.group(1).lower()]} {dev_digits(m.group(2))}, {dev_digits(m.group(3))}" + (' बि.सं.' if m.group(4) else '')),
    (re.compile(r'\b(' + NP_MON_RE + r')\s+(\d{4})\b', re.I),
     lambda m: f"{NP_MON[m.group(1).lower()]} {dev_digits(m.group(2))}"),
]

def protect_dates(text, prot):
    for rx, fmt in DATE_RES:
        def repl(m, fmt=fmt):
            return prot.add(fmt(m))
        text = rx.sub(repl, text)
    return text

STOP = set('''the a an is are was were has have had will would be been being am do does did
can could shall should may might must to in on at of for with by from as and or but if when
while after before so then than not no it its this that these those there here one two
'''.split())
# Grammar explanations: the English words ARE the rule, so protect almost
# everything that appears in the question/options (incl. is/has/will/the/by/in
# when they are the answer word). Only true glue is excluded.
GRAMMAR_STOP = frozenset('''a an and or but when while after before so then than not no
this that these those there here'''.split())
GRAMMAR_PRONOUNS = ['he', 'she', 'it', 'they', 'we', 'you',
                    'his', 'her', 'their', 'him', 'us', 'them']

def protect_words(text, words, prot):
    """Protect whole-word occurrences of `words` (case-insensitive, longest first)."""
    for w in sorted({w for w in words if w and (len(w) >= 2 or w.isupper())}, key=len, reverse=True):
        rx = re.compile(r'\b' + re.escape(w) + r'\b', re.I)
        text = rx.sub(lambda m: prot.add(m.group(0)), text)
    return text

def words_of(*texts, stop=None):
    stop = STOP if stop is None else stop
    out = []
    for t in texts:
        out += re.findall(r"[A-Za-z][A-Za-z\-']*", t or '')
    return [w for w in out if w.lower() not in stop]

def clean_ne(s):
    s = re.sub(r'\s+([।?,])', r'\1', s or '')
    s = re.sub(r'\s{2,}', ' ', s).strip()
    return s

# ---------------- option keep-rules ----------------
def keep_option(o):
    o = o.strip()
    if re.fullmatch(r'[A-Z]{2,6}', o): return True            # CPU, RAM, H2O-ish codes
    if re.search(r'\b(Ctrl|Alt|Shift)\s*\+', o): return True  # Ctrl + C
    if re.fullmatch(r'\.[a-zA-Z]{2,4}', o): return True       # .pdf
    if len(o) == 1: return True                               # A, @, 5, क
    if re.fullmatch(r'[A-Z][a-z]?\d[A-Za-z0-9]*', o): return True  # H2O, CO2
    return False

# ---------------- per-question translation ----------------
def translate_q(q, flags):
    topic, sub = q.get('topic', ''), q.get('subtopic', '')
    question, options, expl = q['question'], q['options'], q['explanation']
    is_maths = q.get('topic') in ('IQ & Reasoning', 'Maths & Numerical')
    norm = (lambda s: en_digits(clean_ne(s))) if is_maths else clean_ne

    def tr_protected(text, extra_words=(), protect_letters=False):
        prot = Protector()
        text = text.replace('year(s)', 'year').replace('place(s)', 'place')
        text = protect_dates(text, prot)
        if protect_letters:
            # Protect single capital letters only when they are labels: two or
            # more distinct ones (A and B) or one repeated. A lone "A" is
            # usually the article ("A man walks...") and must be translated.
            letters = re.findall(r'\b[A-Z]\b', text)
            keep = {L for L in set(letters)
                    if len(set(letters)) >= 2 or letters.count(L) >= 2}
            text = re.sub(r'\b[A-Z]\b',
                          lambda m: prot.add(m.group(0)) if m.group(0) in keep else m.group(0),
                          text)
        if extra_words:
            text = protect_words(text, extra_words, prot)
        out = norm(prot.restore(mt(text)))
        left = prot.leftover(out)
        if left:
            flags.append(f"{q['id']}: leftover token {left} in {out[:80]!r}")
        return out

    def tr_plain(text):
        return tr_protected(text)

    q_ne = opts_ne = expl_ne = None

    if topic == 'Nepali Language':
        q_ne, opts_ne, expl_ne = question, list(options), expl

    elif topic == 'English':
        if sub == 'Grammar':
            if '___' in question or question.startswith('Fill in the blank:'):
                sent = re.sub(r'^Fill in the blank:\s*', '', question)
                q_ne = 'खाली ठाउँमा सही विकल्प छान्नुहोस्: ' + sent
            elif 'passive form' in question:
                sent = question.split(': ', 1)[1].rstrip('.')
                q_ne = 'सही passive रूप छान्नुहोस्: ' + sent + '।'
            elif 'indirect speech' in question:
                sent = question.split(' Choose the correct indirect speech.')[0]
                q_ne = 'सही indirect speech छान्नुहोस्: ' + sent
            elif question.startswith('Choose the correct sentence about '):
                about = question[len('Choose the correct sentence about '):].rstrip('.')
                q_ne = f'‘{about}’ बारे सही वाक्य छान्नुहोस्।'
            else:
                q_ne = 'सही उत्तर छान्नुहोस्: ' + question
            opts_ne = list(options)
            prot_words = words_of(*options, question, stop=GRAMMAR_STOP) + GRAMMAR_PRONOUNS
            expl_ne = tr_protected(expl, extra_words=prot_words)
        else:  # Vocabulary
            m = re.match(r"Choose the synonym of (\w+)\.", question)
            m2 = re.match(r"Choose the antonym of (\w+)\.", question)
            m3 = re.match(r"One word for: (.+)", question)
            m4 = re.match(r"What does the idiom '(.+)' mean\?", question)
            target = None
            if m:
                target = m.group(1); q_ne = f'‘{target}’ को पर्यायवाची शब्द छान्नुहोस्।'
            elif m2:
                target = m2.group(1); q_ne = f'‘{target}’ को विलोम शब्द छान्नुहोस्।'
            elif m3:
                q_ne = 'एक शब्दमा उत्तर दिनुहोस्: ' + m3.group(1)
            elif m4:
                target = m4.group(1); q_ne = f'‘{target}’ उखानको अर्थ के हो?'
            elif 'spelling' in question or 'spelt' in question:
                q_ne = 'सही हिज्जे (spelling) भएको शब्द छान्नुहोस्।'
            else:
                q_ne = 'सही उत्तर छान्नुहोस्: ' + question
                flags.append(f"{q['id']}: untemplated English vocab Q: {question!r}")
            if m4:
                opts_ne = [tr_plain(o) for o in options]
                expl_ne = tr_protected(expl, extra_words=[target])
            else:
                opts_ne = list(options)
                expl_ne = tr_protected(expl, extra_words=([target] if target else []) + words_of(*options))

    elif topic == 'Computer & ICT':
        q_ne = tr_plain(question)
        opts_ne = [o if keep_option(o) else tr_plain(o) for o in options]
        prot = Protector()
        e = protect_dates(expl, prot)
        e = re.sub(r'\b[A-Z]{2,}\b', lambda m: prot.add(m.group(0)), e)
        e = re.sub(r'\b(?:Ctrl|Alt|Shift)\s*\+\s*[A-Z0-9]\b',
                   lambda m: prot.add(m.group(0)), e)
        e = re.sub(r'\.[a-z]{2,4}\b', lambda m: prot.add(m.group(0)), e)
        expl_ne = clean_ne(prot.restore(mt(e)))

    elif is_maths:
        if sub == 'Number Series':
            seq = question.split(':', 1)[1].strip() if ':' in question else question
            q_ne = 'श्रेणीको अर्को सङ्ख्या पत्ता लगाउनुहोस्: ' + en_digits(seq)
            opts_ne = list(options)
            expl_ne = tr_protected(expl, protect_letters=True)
        elif sub == 'Letter Series':
            seq = question.split(':', 1)[1].strip() if ':' in question else question
            q_ne = 'श्रेणीको अर्को अक्षर पत्ता लगाउनुहोस्: ' + seq
            opts_ne = list(options)
            expl_ne = tr_protected(expl, protect_letters=True)
        elif sub == 'Coding-Decoding':
            q_ne = 'दिइएको कोड अनुसार उत्तर छान्नुहोस्: ' + question
            opts_ne = list(options)
            expl_ne = tr_protected(expl, protect_letters=True)
        elif sub == 'Analogy':
            q_ne = 'सादृश्य पत्ता लगाउनुहोस्: ' + question
            opts_ne = list(options)
            expl_ne = tr_protected(expl, protect_letters=True)
        elif sub == 'Odd One Out':
            lst = question.split(':', 1)[1].strip() if ':' in question else question
            q_ne = 'फरक पत्ता लगाउनुहोस्: ' + norm(mt(lst))
            opts_ne = [norm(mt(o)) for o in options]
            expl_ne = tr_protected(expl, protect_letters=True)
        elif sub == 'Verbal Reasoning':
            m = re.match(r"Which word is most similar in meaning to '(.+)'\?", question)
            m2 = re.match(r"Which word is the opposite of '(.+)'\?", question)
            m3 = re.match(r'Choose the word that does not belong to the group: (.+)', question)
            m4 = re.match(r"If '(.+)' is related to '(.+)', then '(.+)' is related to\?", question)
            m5 = re.match(r"Find the missing word: (.+)", question)
            m6 = re.match(r"Arrange in order of size from smallest to largest: (.+)\. Which comes second\?", question)
            m7 = question.strip() == 'Which is the largest?'
            m8 = re.match(r"Which number is different from the others: (.+)", question)
            if m:
                q_ne = f"‘{m.group(1)}’ सँग मिल्दोजुल्दो अर्थ भएको शब्द कुन हो?"
                opts_ne = list(options)
                expl_ne = tr_protected(expl, extra_words=[m.group(1)] + words_of(*options))
            elif m2:
                q_ne = f"‘{m2.group(1)}’ को विलोम शब्द कुन हो?"
                opts_ne = list(options)
                expl_ne = tr_protected(expl, extra_words=[m2.group(1)] + words_of(*options))
            elif m3:
                q_ne = 'समूहमा नमिल्ने शब्द छान्नुहोस्: ' + norm(mt(m3.group(1)))
                opts_ne = [norm(mt(o)) for o in options]
                expl_ne = tr_protected(expl, protect_letters=True)
            elif m4:
                q_ne = (f"यदि ‘{m4.group(1)}’ को सम्बन्ध ‘{m4.group(2)}’ सँग छ भने "
                        f"‘{m4.group(3)}’ को सम्बन्ध के सँग छ?")
                opts_ne = [norm(mt(o)) for o in options]
                expl_ne = tr_protected(expl, extra_words=list(m4.groups()))
            elif m5:
                q_ne = 'हराएको शब्द पत्ता लगाउनुहोस्: ' + m5.group(1)
                opts_ne = list(options)
                expl_ne = tr_protected(expl, protect_letters=True)
            elif m6:
                q_ne = ('आकार अनुसार सानोबाट ठूलो क्रममा मिलाउनुहोस्: '
                        + norm(mt(m6.group(1))) + '। दोस्रोमा कुन आउँछ?')
                opts_ne = [norm(mt(o)) for o in options]
                expl_ne = tr_protected(expl, protect_letters=True)
            elif m7:
                q_ne = 'सबैभन्दा ठूलो कुन हो?'
                opts_ne = [norm(mt(o)) for o in options]
                expl_ne = tr_protected(expl, protect_letters=True)
            elif m8:
                q_ne = 'अरूभन्दा फरक सङ्ख्या कुन हो: ' + m8.group(1)
                opts_ne = list(options)
                expl_ne = tr_protected(expl, protect_letters=True)
            else:
                q_ne = 'सादृश्य पत्ता लगाउनुहोस्: ' + question
                opts_ne = list(options)
                expl_ne = tr_protected(expl, protect_letters=True)
                flags.append(f"{q['id']}: untemplated verbal-reasoning Q: {question!r}")
        else:
            q_ne = tr_protected(question, protect_letters=True)
            opts_ne = [norm(mt(o)) if not keep_option(o) else o for o in options]
            expl_ne = tr_protected(expl, protect_letters=True)
    else:
        # GK / constitution / office / banking / education / health
        q_ne = tr_plain(question)
        opts_ne = [o if keep_option(o) else tr_plain(o) for o in options]
        expl_ne = tr_plain(expl)

    # ---- post-checks / fallbacks ----
    if not q_ne or not q_ne.strip():
        q_ne = question; flags.append(f"{q['id']}: empty question_ne, fell back to English")
    if not expl_ne or not expl_ne.strip():
        expl_ne = expl; flags.append(f"{q['id']}: empty explanation_ne, fell back to English")
    for i, o in enumerate(opts_ne):
        if not o or not str(o).strip():
            opts_ne[i] = options[i]
            flags.append(f"{q['id']}: empty option_ne[{i}], fell back to English")
    # ---- digit consistency (non-maths files): MT converts digits to Devanagari
    # inconsistently inside one 4-option set ("6" vs "११"). For options that
    # contain no Latin word, normalise any ASCII digits to Devanagari so each
    # set is uniform. Latin options (CPU, Ctrl + C, .pdf, H2O, UTC +5:45) and
    # kept English options are left alone.
    if not is_maths and topic != 'Nepali Language':
        for i, o in enumerate(opts_ne):
            s = str(o)
            if re.search(r'[A-Za-z]{2,}', s):
                continue
            if s == options[i] and re.search(r'[A-Za-z]', s):
                continue
            opts_ne[i] = ''.join(DEV[int(c)] if c in '0123456789' else c for c in s)
    seen = {}
    for i, o in enumerate(opts_ne):
        k = str(o).strip().lower()
        if k in seen:
            opts_ne[i] = options[i]
            flags.append(f"{q['id']}: duplicate option_ne {o!r} at [{i}] (also [{seen[k]}]), fell back to English")
        else:
            seen[k] = i
    return q_ne, opts_ne, expl_ne

# Manual corrections applied after MT (id -> {field: value}).
CORRECTIONS = {
    # Pre-existing mojibake in the English field ("कु���"); the Nepali copy is fixed.
    'NEP-027': {'question_ne': "'मैले उसलाई किताब दिएँ।' मा उसलाई कुन कारक हो?"},
    # MT rendered "Terms" (series terms) as "सर्तहरू" (conditions); correct is "पदहरू".
    'IQ-019': {'explanation_ne': 'पदहरू वर्ग हुन्: 3^2, 4^2, 5^2, 6^2, त्यसैले अर्को 7^2 = 49 हो।'},
    'IQ-017': {'explanation_ne': 'पदहरू वर्ग हुन्: 1^2, 2^2, 3^2, 4^2, त्यसैले अर्को 5^2 = 25 हो।'},
    'IQ-018': {'explanation_ne': 'पदहरू वर्ग हुन्: 2^2, 3^2, 4^2, 5^2, त्यसैले अर्को 6^2 = 36 हो।'},
    # MT scrambled the "i before e except after c" rule; keep the rule in English.
    'ENG-089': {'explanation_ne': "Receive मा ‘i before e except after c’ नियम लागू हुन्छ।"},
    # MT returned mojibake (U+FFFD) for "To fall asleep"; "feeling/emotion" collapsed to one word.
    'ENG-082': {'options_ne': ['परास्त हुने', 'खाना स्वाद गर्न', 'धूलो खाने', 'निदाउनु']},
    'ENG-083': {'options_ne': ['हतारमा', 'धेरै चिसो मौसममा', 'भावनाबिना', 'ज्वरो लिएर']},
    # MT rendered "stands for" literally as "खडा छ" (stands upright).
    'COMP-005': {'explanation_ne': 'RAM को पूरा रूप Random Access Memory हो।'},
    'COMP-046': {'explanation_ne': 'URL को पूरा रूप Uniform Resource Locator हो।'},
    'COMP-055': {'explanation_ne': 'PDF को पूरा रूप Portable Document Format हो।'},
}

# Hand-written Nepali explanations for the 54 English grammar questions.
# MT mangles these rule statements (answer words get translated away or the
# glue turns to nonsense), and the rules are short and formulaic, so the
# correct Nepali is written out here instead of machine-translated.
GRAMMAR_NE = {
    'ENG-001': 'Simple present मा he, she, it सँग क्रियामा -s थपिन्छ।',
    'ENG-002': 'Yesterday ले simple past देखाउँछ, त्यसैले क्रिया played हुन्छ।',
    'ENG-003': 'Now ले भइरहेको कार्य देखाउँछ, त्यसैले present continuous प्रयोग हुन्छ।',
    'ENG-004': 'Has पछि past participle lived आउँछ।',
    'ENG-005': 'सामान्य वैज्ञानिक तथ्यमा simple present प्रयोग हुन्छ; water सँग क्रियामा -s थपिन्छ।',
    'ENG-006': 'Look! ले अहिले भइरहेको कार्य देखाउँछ, त्यसैले is raining सही छ।',
    'ENG-007': 'Past continuous was watching ले कलले अवरुद्ध गरेको लामो कार्य वर्णन गर्छ।',
    'ENG-008': 'Has पछि past participle been आउँछ।',
    'ENG-009': 'Will पछि base form come आउँछ।',
    'ENG-010': 'By next year सम्म पूरा हुने कार्यका लागि future perfect प्रयोग हुन्छ।',
    'ENG-011': 'Neither ले एकवचन क्रिया लिन्छ, त्यसैले has सही छ।',
    'ENG-012': 'Each एकवचन हो, त्यसैले यसले has लिन्छ।',
    'ENG-013': 'One of ले एकवचन क्रिया लिन्छ, त्यसैले is सही छ।',
    'ENG-014': 'Physics एकवचन विषय हो, त्यसैले यसले is लिन्छ।',
    'ENG-015': 'News अगणित र एकवचन हो, त्यसैले यसले is लिन्छ।',
    'ENG-016': 'Bread and butter लाई एउटै वस्तु मानिन्छ, त्यसैले यसले is लिन्छ।',
    'ENG-017': 'Neither-nor मा क्रिया नजिकको कर्ता Shyam सँग मिल्छ; Shyam एकवचन भएकाले is हुन्छ।',
    'ENG-018': 'Team लाई एउटा एकाइ मान्दा एकवचन क्रिया is हुन्छ।',
    'ENG-019': 'The sun अद्वितीय छ, त्यसैले definite article the प्रयोग हुन्छ।',
    'ENG-020': 'An स्वर ध्वनिअघि प्रयोग हुन्छ; honest मौन h बाट सुरु हुन्छ।',
    'ENG-021': 'An स्वर ध्वनिअघि प्रयोग हुन्छ, जस्तै elephant।',
    'ENG-022': 'The वाद्ययन्त्र (musical instruments) सँग प्रयोग हुन्छ।',
    'ENG-023': 'University व्यञ्जन ध्वनि (yoo) बाट सुरु हुने भएकाले A प्रयोग हुन्छ।',
    'ENG-024': 'The नदीहरूका नामअघि प्रयोग हुन्छ।',
    'ENG-025': 'An स्वर ध्वनिअघि प्रयोग हुन्छ, जस्तै umbrella।',
    'ENG-026': 'An स्वर ध्वनिअघि प्रयोग हुन्छ, जस्तै apple।',
    'ENG-027': 'The superlative (best) अघि प्रयोग हुन्छ।',
    'ENG-028': 'सही collocation interested in हो।',
    'ENG-029': 'सही collocation good at हो।',
    'ENG-030': 'सही collocation afraid of हो।',
    'ENG-031': 'सही collocation depend on हो।',
    'ENG-032': 'In ठूलो ठाउँ, जस्तै शहरसँग प्रयोग हुन्छ।',
    'ENG-033': 'At सानो, निश्चित ठाउँ, जस्तै stationसँग प्रयोग हुन्छ।',
    'ENG-034': 'सही collocation fond of हो।',
    'ENG-035': 'By यातायातको साधनसँग article बिना प्रयोग हुन्छ।',
    'ENG-036': 'On हप्ताका दिनहरूसँग प्रयोग हुन्छ।',
    'ENG-037': 'In वर्षसँग प्रयोग हुन्छ।',
    'ENG-038': 'Wrote simple past हो, त्यसैले passive was written हुन्छ।',
    'ENG-039': 'Is singing present continuous हो, त्यसैले passive is being sung हुन्छ।',
    'ENG-040': 'Will build को passive will be built हुन्छ।',
    'ENG-041': 'Imperative को passive Let + be + past participle हुन्छ।',
    'ENG-042': 'Stole simple past हो, त्यसैले passive was stolen हुन्छ।',
    'ENG-043': 'Teaches simple present हो, त्यसैले passive is taught हुन्छ।',
    'ENG-044': 'Have completed present perfect हो, त्यसैले passive has been completed हुन्छ।',
    'ENG-045': 'Chased simple past हो, त्यसैले passive was chased हुन्छ।',
    'ENG-046': 'Indirect speech मा reporting verb भूतकालमा हुँदा am was मा बदलिन्छ।',
    'ENG-047': 'Indirect speech मा will would मा र tomorrow the next day मा बदलिन्छ।',
    'ENG-048': 'हो-होइन प्रश्न asked + if हुन्छ र प्रश्नको रूप कथनमा बदलिन्छ।',
    'ENG-049': 'Indirect speech मा have finished had finished मा बदलिन्छ।',
    'ENG-050': 'Indirect speech मा imperative told + to + base verb हुन्छ।',
    'ENG-051': 'Wh-question मा wh-word यथावत् रहन्छ र शब्दक्रम कथनको जस्तो हुन्छ, भूतकालमा।',
    'ENG-090': 'He सँग negative present simple doesn’t like हुन्छ।',
    'ENG-091': 'She सँग simple present मा goes हुन्छ।',
    'ENG-092': 'Since समयको बिन्दु (point in time), 2015 सँग प्रयोग हुन्छ।',
}
CORRECTIONS.update({k: {'explanation_ne': v} for k, v in GRAMMAR_NE.items()})

def process(path, dry_run=False):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    flags = []
    out = [None] * len(data)

    def work(item):
        i, q = item
        q_ne, opts_ne, expl_ne = translate_q(q, flags)
        for field, val in CORRECTIONS.get(q['id'], {}).items():
            if field == 'question_ne': q_ne = val
            elif field == 'options_ne': opts_ne = val
            elif field == 'explanation_ne': expl_ne = val
        nq = {}
        for k, v in q.items():
            if k in ('question_ne', 'options_ne', 'explanation_ne'):
                continue  # stale _ne fields from a previous run must not overwrite fresh ones
            nq[k] = v
            if k == 'question': nq['question_ne'] = q_ne
            elif k == 'options': nq['options_ne'] = opts_ne
            elif k == 'explanation': nq['explanation_ne'] = expl_ne
        out[i] = nq
        return q['id']

    with ThreadPoolExecutor(max_workers=6) as ex:
        done = list(ex.map(work, enumerate(data)))
    print(f'translated {len(done)} questions')
    # Coverage + QA
    total = len(out)
    full = sum(1 for q in out if q.get('question_ne') and q.get('options_ne')
               and len(q['options_ne']) == 4 and all(str(o).strip() for o in q['options_ne'])
               and q.get('explanation_ne'))
    dev_q = sum(1 for q in out if has_dev(q.get('question_ne', '')))
    print(f'{os.path.basename(path)}: {total} questions, bilingual {full} ({full*100//total}%), '
          f'Devanagari in question_ne: {dev_q}')
    if flags:
        print(f'FLAGS ({len(flags)}):')
        for fl in flags:
            print('  -', fl)
    if not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
            f.write('\n')
        json.load(open(path, encoding='utf-8'))  # validate
        print('written + JSON validated:', path)
    _save_cache()
    return out, flags

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: add-nepali.py data/questions/<file>.json [--dry-run]')
        sys.exit(2)
    process(sys.argv[1], dry_run='--dry-run' in sys.argv)
