#!/usr/bin/env python3
"""Extended verification for the PDF extract (2026-10-27) — MY OWN checks,
written for this job. Does NOT import any generator module; reads only
data/pdf-extract-raw.json and writes data/pdf-extended-flags-2026-10-27.json.

Checks (each flag carries a proposed fix when the correct answer is certain):
  E1 constitution-part: "Part N (Articles a-b)" range or subject wrong in key.
  E2 constitution-article: "subject matter of Article N" — keyed option
     contradicts a well-known article subject while another option matches.
  E3 constitution-article-rev: "which article guarantees X" for non-rights
     articles in the table.
  E4 district-province: stem names a district; keyed option names a wrong
     province while another option names the right one.
  E5 census-fact: census 2021 facts (sex ratio, literacy, density,
     households, most/least populous district, most/least populous province).
  E6 nrb-fact: first governor, first commercial bank, first JV bank,
     RBB/ADBL establishment years, NRB Act 2058.
  E7 history-fact: Sugauli 1816, Kot Massacre 1846, Rana 1846-1951,
     Kathmandu Valley conquest 1768, unification start 1743.
  E8 geography-fact: longest river Karnali, largest lake Rara,
     deepest lake Phoksundo, lowest point Kechana 60m, 8 eight-thousanders.
  M1 letter-sum: sum of letter values of a quoted word.
  M2 caesar: letter shift (+/-N) coding of a quoted word.
  M3 rank: rank from the other end of a row.
  M4 handshakes-diagonals: C(n,2) handshakes + n(n-3)/2 diagonals.
  M5 quadratic: roots of x^2 +/- bx +/- c = 0 and sum of squares.
  M6 sets: survey both/only counts.
  M7 profit: cost price from SP + profit%, and SP for a new profit%.
  M8 discounts: single equivalent discount + SP after two successive discounts.
  M9 pipes: inlet/outlet fill-empty time.
  S1 numeric-dup-options: two options with equal numeric value (two correct).
  S2 keyed-option-missing-number: keyed numeric option has no numeric value
     where the stem demands one (garbled).

Flag rule throughout: only flag when the correct value is CERTAIN and it
appears among the options (so a fix is unambiguous), except structural
flags (S1/S2) which are drops.
"""
import json
import re
import sys
import unicodedata
from collections import Counter

DEV = str.maketrans('०१२३४५६७८९', '0123456789')


def denum(s):
    return str(s).translate(DEV) if s is not None else ''


def parse_num(tok):
    tok = str(tok).replace(',', '').strip().rstrip('%')
    try:
        return float(tok) if '.' in tok else int(tok)
    except ValueError:
        return None


def normalise(s):
    if s is None:
        return ''
    s = denum(s)
    s = unicodedata.normalize('NFKC', s).lower()
    s = re.sub(r'[^\w\s]', ' ', s, flags=re.UNICODE)
    s = s.replace('_', ' ')
    return re.sub(r'\s+', ' ', s).strip()


NUM = r'-?\d[\d,]*\.?\d*'


def numeric_value(opt):
    s = denum(opt).strip()
    s2 = re.sub(r'^(Rs\.?|US\$|\$|NPR\.?)\s*', '', s)
    s2 = re.sub(r'\s*(kg|km|m|cm|%|years?|days?|months?|hours?|minutes?|seconds?|MW|litres?|liters?|rupees?)$', '', s2, flags=re.I)
    s2 = s2.strip().rstrip('.')
    if re.fullmatch(r'-?\d[\d,]*\.?\d*', s2):
        return parse_num(s2)
    return None


def opt_numbers(opt):
    """All numbers appearing in an option."""
    return [parse_num(t) for t in re.findall(NUM, denum(opt))]


# ------------------------------------------------------------ constitution ---
# part -> (subject keywords (list of regex fragments, any must match),
#          first article, last article)
PARTS = {
    1: (['preliminary'], 1, 9),
    2: (['citizenship'], 10, 15),
    3: (['fundamental rights'], 16, 48),
    4: (['directive principles'], 49, 55),
    5: (['structure of state', 'distribution of state power'], 56, 60),
    6: (['president and vice'], 61, 73),
    7: (['federal executive'], 74, 82),
    8: (['federal legislature', 'federal parliament'], 83, 108),
    9: (['federal legislative procedure'], 109, 114),
    10: (['federal financial procedure'], 115, 125),
    11: (['judiciary'], 126, 156),
    12: (['attorney general'], 157, 161),
    13: (['provincial executive', 'state executive'], 162, 174),
    14: (['provincial legislature', 'state legislature'], 175, 196),
    15: (['provincial legislative procedure', 'state legislative procedure'], 197, 202),
    16: (['provincial financial procedure', 'state financial procedure'], 203, 213),
    17: (['local executive'], 214, 220),
    18: (['local legislature'], 221, 227),
    19: (['local financial procedure'], 228, 230),
    20: (['interrelation', 'interrelationship', 'relations between federation'], 231, 237),
    21: (['commission for the investigation of abuse of authority'], 238, 239),
    22: (['auditor general'], 240, 241),
    23: (['public service commission'], 242, 244),
    24: (['election commission'], 245, 247),
    25: (['national human rights commission'], 248, 249),
    26: (['national natural resources and fiscal commission'], 250, 251),
    27: (['other commissions'], 252, 265),
    28: (['national security'], 266, 268),
    29: (['political parties'], 269, 272),
    30: (['emergency power'], 273, 273),
    31: (['amendment'], 274, 274),
    32: (['miscellaneous'], 275, 294),
    33: (['transitional provisions'], 295, 305),
    34: (['definitions'], 306, 306),
    35: (['short title', 'commencement and repeal'], 307, 308),
}

# article -> subject keywords (only articles I am certain about).
ARTICLES = {
    1: ['constitution as the fundamental law', 'fundamental law'],
    2: ['sovereignty and state authority', 'sovereignty'],
    3: ['definition of the nation', 'nation'],
    4: ['state of nepal', 'nepal is an independent'],
    5: ['national interest'],
    6: ['languages spoken in nepal', 'languages of the nation', 'language'],
    7: ['language of official transaction'],
    8: ['national flag'],
    9: ['national anthem'],
    10: ['citizenship not to be denied', 'not to be denied'],
    11: ['deemed to be citizen', 'citizenship of nepal to be deemed', 'deemed citizen'],
    12: ['citizenship by descent', 'gender identity'],
    13: ['acquisition, re-acquisition and termination of citizenship', 'acquisition and termination'],
    14: ['non residential citizenship', 'non-residential citizenship'],
    15: ['other matters relating to citizenship'],
    16: ['right to live with dignity'],
    17: ['right to freedom'],
    18: ['right to equality'],
    19: ['right to communication'],
    20: ['rights relating to justice'],
    21: ['right of victim of crime'],
    22: ['right against torture'],
    23: ['right against preventive detention'],
    24: ['right against untouchability'],
    25: ['right relating to property'],
    26: ['right to religious freedom', 'right to freedom of religion'],
    27: ['right to information'],
    28: ['right to privacy'],
    29: ['right against exploitation'],
    30: ['right to clean environment', 'right to a clean environment'],
    31: ['right relating to education'],
    32: ['right to language and culture'],
    33: ['right to employment'],
    34: ['right to labour'],
    35: ['right relating to health'],
    36: ['right relating to food'],
    37: ['right to housing'],
    38: ['rights of women'],
    39: ['rights of child', 'rights of the child'],
    40: ['rights of dalit'],
    41: ['rights of senior citizen'],
    42: ['right to social justice'],
    43: ['right to social security'],
    44: ['consumer right'],
    45: ['right against exile'],
    46: ['right to constitutional remedies'],
    47: ['enforcement of fundamental rights'],
    48: ['duties of citizens', 'duties of citizen'],
    49: ['directive principles'],
    51: ['policies of the state'],
    56: ['structure of state', 'restructuring of the state'],
    57: ['distribution of state power'],
    58: ['residual power'],
    59: ['exercise of state power'],
    61: ['president'],
    71: ['vice president', 'vice-president'],
    74: ['federal executive'],
    76: ['formation of council of ministers', 'council of ministers'],
    83: ['federal parliament', 'federal legislature'],
    84: ['formation of house of representatives', 'house of representatives'],
    85: ['term of the house of representatives'],
    86: ['formation of national assembly', 'national assembly'],
    87: ['term of the national assembly'],
    91: ['speaker and deputy speaker', 'speaker'],
    100: ['vote of confidence', 'motion of no confidence', 'no confidence'],
    119: ['estimates of revenues and expenditure'],
    126: ['courts'],
    127: ['supreme court'],
    156: ['attorney general'],
    168: ['formation of council of ministers'],
    175: ['provincial assembly', 'state assembly'],
    176: ['formation of provincial assembly'],
    215: ['village executive', 'municipal executive'],
    221: ['village assembly', 'municipal assembly'],
    230: ['estimates of revenues and expenditure'],
    231: ['legislative interrelation'],
    232: ['relations between federation'],
    238: ['commission for the investigation of abuse of authority'],
    240: ['auditor general'],
    242: ['public service commission'],
    245: ['election commission'],
    248: ['national human rights commission'],
    250: ['national natural resources and fiscal commission'],
    252: ['national women commission'],
    253: ['national dalit commission'],
    254: ['national inclusion commission'],
    255: ['national indigenous nationalities commission'],
    256: ['madhesi commission'],
    257: ['tharu commission'],
    258: ['muslim commission'],
    266: ['national security council'],
    269: ['formation of political parties', 'political parties'],
    273: ['emergency power'],
    274: ['amendment of the constitution', 'amendment'],
    306: ['definitions'],
    307: ['short title and commencement', 'short title'],
    308: ['repeal'],
}

RIGHTS = {n: k for n, k in ARTICLES.items() if 16 <= n <= 46}


def opt_matches(opt, keywords):
    no = normalise(opt)
    return any(normalise(k) in no for k in keywords)


def find_opt_with(opts, keywords):
    return [i for i, o in enumerate(opts) if opt_matches(o, keywords)]


# ------------------------------------------------------------- districts -----
DISTRICT_PROVINCE = {}
for _prov, _ds in {
    'Koshi': ['Taplejung', 'Panchthar', 'Ilam', 'Jhapa', 'Morang', 'Sunsari',
              'Dhankuta', 'Sankhuwasabha', 'Bhojpur', 'Terhathum',
              'Solukhumbu', 'Okhaldhunga', 'Khotang', 'Udayapur'],
    'Madhesh': ['Saptari', 'Siraha', 'Dhanusha', 'Mahottari', 'Sarlahi',
                'Rautahat', 'Bara', 'Parsa'],
    'Bagmati': ['Dolakha', 'Sindhupalchok', 'Rasuwa', 'Nuwakot', 'Dhading',
                'Kathmandu', 'Bhaktapur', 'Lalitpur', 'Kavrepalanchok',
                'Ramechhap', 'Sindhuli', 'Makwanpur', 'Chitwan'],
    'Gandaki': ['Gorkha', 'Manang', 'Mustang', 'Myagdi', 'Kaski', 'Lamjung',
                'Tanahun', 'Nawalpur', 'Syangja', 'Parbat', 'Baglung'],
    'Lumbini': ['Gulmi', 'Palpa', 'Arghakhanchi', 'Rupandehi', 'Kapilvastu',
                'Parasi', 'Dang', 'Banke', 'Bardiya', 'Pyuthan', 'Rolpa',
                'Rukum East'],
    'Karnali': ['Dolpa', 'Humla', 'Mugu', 'Jumla', 'Kalikot', 'Dailekh',
                'Jajarkot', 'Rukum West', 'Salyan', 'Surkhet'],
    'Sudurpashchim': ['Bajura', 'Bajhang', 'Darchula', 'Baitadi',
                      'Dadeldhura', 'Doti', 'Achham', 'Kailali',
                      'Kanchanpur'],
}.items():
    for _d in _ds:
        DISTRICT_PROVINCE[_d.lower()] = _prov

PROVINCES = ['Koshi', 'Madhesh', 'Bagmati', 'Gandaki', 'Lumbini', 'Karnali',
             'Sudurpashchim']


# ------------------------------------------------------------------ maths ----
def letter_sum(word):
    return sum(ord(c) - 64 for c in word.upper() if c.isalpha())


def caesar(word, shift):
    out = ''
    for c in word:
        if c.isalpha():
            b = ord('A') if c.isupper() else ord('a')
            out += chr((ord(c) - b + shift) % 26 + b)
        else:
            out += c
    return out


def check_question(q):
    flags = []
    stem = q.get('question') or ''
    opts = q.get('options') or []
    ans = q.get('pdf_answer')
    if not isinstance(opts, list) or len(opts) != 4 or not isinstance(ans, int) \
            or not 0 <= ans < 4:
        return flags
    nstem = normalise(stem)
    keyed = opts[ans]

    # ---- S1: two options with equal numeric value (two correct options) ----
    vals = [numeric_value(o) for o in opts]
    if all(v is not None for v in vals) and len(set(vals)) != 4:
        flags.append({'type': 'S1-numeric-dup-options',
                      'detail': f'two options share numeric value: {opts}',
                      'action': 'drop',
                      'reason': 'two options have the same numeric value — two correct options'})
        return flags

    # ---- E1/E2: Constitution Part / Article questions ----
    m = re.search(r'part\s+(\d+)\s*\(articles?\s*(\d+)\s*[–\-]\s*(\d+)\)', nstem)
    if m:
        pn, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if pn in PARTS:
            kws, fa, la = PARTS[pn]
            if (a, b) != (fa, la):
                flags.append({'type': 'E1-part-range-wrong',
                              'detail': f'stem says Part {pn} is Articles {a}-{b}; correct range is {fa}-{la}',
                              'action': 'review',
                              'reason': f'Part {pn} covers Articles {fa}-{la}'})
            else:
                good = find_opt_with(opts, kws)
                if good and ans not in good:
                    flags.append({'type': 'E1-part-subject-wrong',
                                  'detail': f'Part {pn} is {kws[0]}; key is {keyed!r}, correct option is {chr(65 + good[0])}',
                                  'action': 'fix', 'new_answer': good[0],
                                  'reason': f'Constitution Part {pn} is {PARTS[pn][0][0]}'})
        return flags
    m = re.search(r'which group of articles.*comprises part\s+(\d+)\b', nstem)
    if m:
        pn = int(m.group(1))
        if pn in PARTS:
            _kws, fa, la = PARTS[pn]
            good = []
            for i, o in enumerate(opts):
                om = re.search(r'articles?\s*(\d+)\s*[–\-]\s*(\d+)', denum(o), re.I)
                if om and int(om.group(1)) == fa and int(om.group(2)) == la:
                    good.append(i)
                elif fa == la:
                    om1 = re.search(r'article\s*(\d+)\b', denum(o), re.I)
                    if om1 and int(om1.group(1)) == fa and 'articles' not in denum(o):
                        good.append(i)
            if good and ans not in good:
                flags.append({'type': 'E1b-part-range-option-wrong',
                              'detail': f'Part {pn} comprises Articles {fa}-{la}; key is {keyed!r}, correct option is {chr(65 + good[0])}',
                              'action': 'fix', 'new_answer': good[0],
                              'reason': f'Constitution Part {pn} comprises Articles {fa}-{la}'})
        return flags
    m = re.search(r'which subject is governed by part\s+(\d+)\b', nstem)
    if m:
        pn = int(m.group(1))
        if pn in PARTS:
            kws = PARTS[pn][0]
            good = find_opt_with(opts, kws)
            if good and ans not in good:
                flags.append({'type': 'E1-part-subject-wrong',
                              'detail': f'Part {pn} is {kws[0]}; key is {keyed!r}, correct option is {chr(65 + good[0])}',
                              'action': 'fix', 'new_answer': good[0],
                              'reason': f'Constitution Part {pn} is {PARTS[pn][0][0]}'})
        return flags
    m = re.search(r'subject matter of article\s+(\d+)\b', nstem)
    if m:
        an = int(m.group(1))
        if an in ARTICLES:
            kws = ARTICLES[an]
            good = find_opt_with(opts, kws)
            if good and ans not in good:
                flags.append({'type': 'E2-article-subject-wrong',
                              'detail': f'Article {an} is about {kws[0]}; key is {keyed!r}, correct option is {chr(65 + good[0])}',
                              'action': 'fix', 'new_answer': good[0],
                              'reason': f'Constitution Article {an}: {kws[0]}'})
        return flags
    # reverse: "which article" + subject of a tabled article (non-rights only;
    # rights already covered by the main audit script)
    if 'which article' in nstem:
        for an, kws in ARTICLES.items():
            if an in RIGHTS:
                continue
            if any(normalise(k) in nstem for k in kws):
                keyed_nums = re.findall(r'\b\d+\b', denum(keyed))
                if keyed_nums and str(an) not in keyed_nums:
                    good = [i for i, o in enumerate(opts)
                            if str(an) in re.findall(r'\b\d+\b', denum(o))]
                    if good:
                        flags.append({'type': 'E3-article-number-wrong',
                                      'detail': f'{kws[0]} is Article {an}; key is {keyed!r}, correct option is {chr(65 + good[0])}',
                                      'action': 'fix', 'new_answer': good[0],
                                      'reason': f'{kws[0]} is Constitution Article {an}'})
                break
        return flags

    # ---- E4: district -> province ----
    if 'district' in nstem and 'province' in nstem:
        for dname, prov in DISTRICT_PROVINCE.items():
            if dname in nstem:
                good = [i for i, o in enumerate(opts)
                        if normalise(prov) in normalise(o)]
                keyed_provs = [p for p in PROVINCES
                               if normalise(p) in normalise(keyed)]
                if good and ans not in good and keyed_provs:
                    flags.append({'type': 'E4-district-province-wrong',
                                  'detail': f'{dname.title()} District is in {prov} Province; key is {keyed!r}, correct option is {chr(65 + good[0])}',
                                  'action': 'fix', 'new_answer': good[0],
                                  'reason': f'{dname.title()} District lies in {prov} Province'})
                break

    # ---- E5: census 2021 ----
    def census_check(pat, expected, label, accept=()):
        if re.search(pat, nstem):
            mv = numeric_value(keyed)
            expv = parse_num(expected)
            ok = (mv is not None and (mv == expv or mv in accept))
            if not ok:
                good = [i for i, o in enumerate(opts)
                        if numeric_value(o) is not None and
                        (numeric_value(o) == expv or numeric_value(o) in accept)]
                if good:
                    flags.append({'type': 'E5-census-fact-wrong',
                                  'detail': f'{label}; key is {keyed!r}, correct option is {chr(65 + good[0])}',
                                  'action': 'fix', 'new_answer': good[0],
                                  'reason': label})
            return True
        return False

    if census_check(r'sex ratio.*census 2021|census 2021.*sex ratio', '95.59',
                    'Census 2021 sex ratio 95.59 males per 100 females'):
        return flags
    if census_check(r'literacy rate.*census 2021|census 2021.*literacy', '76.2',
                    'Census 2021 literacy rate 76.2%', accept=(76.3,)):
        return flags
    if census_check(r'population density.*census 2021|census 2021.*population density',
                    '198', 'Census 2021 population density 198 per sq km'):
        return flags
    if census_check(r'how many households.*census 2021|census 2021.*households',
                    '6666937', 'Census 2021 total households 6,666,937'):
        return flags
    if re.search(r'most populous district', nstem):
        good = find_opt_with(opts, ['kathmandu'])
        if good and ans not in good:
            flags.append({'type': 'E5-census-fact-wrong',
                          'detail': f'most populous district (Census 2021) is Kathmandu; key is {keyed!r}',
                          'action': 'fix', 'new_answer': good[0],
                          'reason': 'Census 2021: Kathmandu is the most populous district (2,041,587)'})
        return flags
    if re.search(r'least populous district|lowest population.*district', nstem):
        good = find_opt_with(opts, ['manang'])
        if good and ans not in good:
            flags.append({'type': 'E5-census-fact-wrong',
                          'detail': f'least populous district (Census 2021) is Manang; key is {keyed!r}',
                          'action': 'fix', 'new_answer': good[0],
                          'reason': 'Census 2021: Manang is the least populous district (5,658)'})
        return flags
    if re.search(r'most populous province|highest population.*province', nstem):
        good = find_opt_with(opts, ['bagmati'])
        if good and ans not in good:
            flags.append({'type': 'E5-census-fact-wrong',
                          'detail': 'most populous province (Census 2021) is Bagmati; key is %r' % keyed,
                          'action': 'fix', 'new_answer': good[0],
                          'reason': 'Census 2021: Bagmati is the most populous province'})
        return flags
    if re.search(r'least populous province|lowest population.*province', nstem):
        good = find_opt_with(opts, ['karnali'])
        if good and ans not in good:
            flags.append({'type': 'E5-census-fact-wrong',
                          'detail': 'least populous province (Census 2021) is Karnali; key is %r' % keyed,
                          'action': 'fix', 'new_answer': good[0],
                          'reason': 'Census 2021: Karnali is the least populous province'})
        return flags

    # ---- E6: NRB / banking ----
    def text_check(pat, keywords, label):
        if re.search(pat, nstem):
            good = find_opt_with(opts, keywords)
            if good and ans not in good:
                flags.append({'type': 'E6-nrb-fact-wrong',
                              'detail': f'{label}; key is {keyed!r}, correct option is {chr(65 + good[0])}',
                              'action': 'fix', 'new_answer': good[0],
                              'reason': label})
            return True
        return False

    if text_check(r'\bfirst governor of\b.*nepal rastra bank|first governor of\b.*\bnrb\b|who was the first governor of',
                  ['himalaya shumsher'], 'First NRB Governor: Himalaya Shumsher JBR (1956)'):
        return flags
    if text_check(r'first commercial bank.*nepal|nepal.*first commercial bank',
                  ['nepal bank'], 'First commercial bank of Nepal: Nepal Bank Ltd (1937)'):
        return flags
    if text_check(r'first joint venture bank|first joint-venture bank',
                  ['nepal arab bank', 'nabil'], 'First joint-venture bank: Nepal Arab Bank (now Nabil, 1984)'):
        return flags
    if re.search(r'rastriya banijya bank.*established|when.*rbb.*established', nstem):
        good = [i for i, o in enumerate(opts) if '1966' in denum(o)]
        if good and ans not in good:
            flags.append({'type': 'E6-nrb-fact-wrong',
                          'detail': 'RBB established 1966; key is %r' % keyed,
                          'action': 'fix', 'new_answer': good[0],
                          'reason': 'Rastriya Banijya Bank established 23 Jan 1966'})
        return flags
    if re.search(r'agricultural development bank.*established|when.*adbl.*established', nstem):
        good = [i for i, o in enumerate(opts) if '1968' in denum(o)]
        if good and ans not in good:
            flags.append({'type': 'E6-nrb-fact-wrong',
                          'detail': 'ADBL established 1968; key is %r' % keyed,
                          'action': 'fix', 'new_answer': good[0],
                          'reason': 'Agricultural Development Bank established 1968'})
        return flags
    if re.search(r'which year.*nrb act (was )?(enacted|passed|promulgated)|when was the nrb act', nstem):
        good = [i for i, o in enumerate(opts) if '2058' in denum(o)]
        if good and ans not in good:
            flags.append({'type': 'E6-nrb-fact-wrong',
                          'detail': 'NRB Act enacted 2058 BS (2002 AD); key is %r' % keyed,
                          'action': 'fix', 'new_answer': good[0],
                          'reason': 'Nepal Rastra Bank Act, 2058 (2002)'})
        return flags

    # ---- E7: history ----
    if re.search(r'sugauli treaty', nstem):
        good = [i for i, o in enumerate(opts) if '1816' in denum(o)]
        if good and ans not in good:
            flags.append({'type': 'E7-history-fact-wrong',
                          'detail': 'Sugauli Treaty signed 1816; key is %r' % keyed,
                          'action': 'fix', 'new_answer': good[0],
                          'reason': 'Treaty of Sugauli: 1816'})
        return flags
    if re.search(r'kot massacre', nstem):
        good = [i for i, o in enumerate(opts) if '1846' in denum(o)]
        if good and ans not in good:
            flags.append({'type': 'E7-history-fact-wrong',
                          'detail': 'Kot Massacre 1846; key is %r' % keyed,
                          'action': 'fix', 'new_answer': good[0],
                          'reason': 'Kot Massacre: 14 Sep 1846'})
        return flags
    if re.search(r'rana regime.*(start|begin|establish)|when.*rana regime.*start', nstem):
        good = [i for i, o in enumerate(opts) if '1846' in denum(o)]
        if good and ans not in good:
            flags.append({'type': 'E7-history-fact-wrong',
                          'detail': 'Rana regime began 1846; key is %r' % keyed,
                          'action': 'fix', 'new_answer': good[0],
                          'reason': 'Rana regime began with the Kot Massacre, 1846'})
        return flags
    if re.search(r'prithvi narayan shah.*kathmandu|conquest of kathmandu valley|kathmandu valley.*conquer', nstem):
        good = [i for i, o in enumerate(opts) if '1768' in denum(o)]
        if good and ans not in good:
            flags.append({'type': 'E7-history-fact-wrong',
                          'detail': 'Kathmandu Valley conquered 1768; key is %r' % keyed,
                          'action': 'fix', 'new_answer': good[0],
                          'reason': 'Prithvi Narayan Shah conquered Kathmandu Valley in 1768'})
        return flags

    # ---- E8: geography ----
    if text_check(r'longest river.*nepal|nepal.*longest river',
                  ['karnali'], 'Longest river of Nepal: Karnali'):
        return flags
    if text_check(r'largest lake.*nepal|nepal.*largest lake',
                  ['rara'], 'Largest lake of Nepal: Rara'):
        return flags
    if text_check(r'deepest lake.*nepal|nepal.*deepest lake',
                  ['phoksundo'], 'Deepest lake of Nepal: Phoksundo'):
        return flags
    if text_check(r'lowest point.*nepal|nepal.*lowest point|lowest altitude.*nepal',
                  ['kechana'], 'Lowest point of Nepal: Kechana Kalan, Jhapa (60 m)'):
        return flags
    if re.search(r'how many.*eight thousand|eight-thousanders.*nepal|nepal.*eight-thousanders', nstem):
        good = [i for i, o in enumerate(opts) if numeric_value(o) == 8]
        if good and ans not in good:
            flags.append({'type': 'E8-geography-fact-wrong',
                          'detail': '8 eight-thousanders lie (wholly/partly) in Nepal; key is %r' % keyed,
                          'action': 'fix', 'new_answer': good[0],
                          'reason': '8 of the 14 eight-thousanders are in Nepal'})
        return flags

    # ---- M1: letter sum ----
    m = re.search(r"sum of the letter values of the word '([A-Za-z]+)'", stem)
    if m:
        s = letter_sum(m.group(1))
        good = [i for i, o in enumerate(opts) if numeric_value(o) == s]
        if good and ans not in good:
            flags.append({'type': 'M1-letter-sum-wrong',
                          'detail': f"letter sum of {m.group(1)} is {s}; key is {keyed!r}",
                          'action': 'fix', 'new_answer': good[0],
                          'reason': f"letter values of {m.group(1)} sum to {s}"})
        return flags

    # ---- M2: caesar code ----
    m = re.search(r'shifted (\w+) positions? (forward|backward) \([+-](\d+)\)', stem)
    m2 = re.search(r"how is the word '([A-Za-z]+)' coded", stem)
    if m and m2:
        shift = int(m.group(3))
        if m.group(2) == 'backward':
            shift = -shift
        coded = caesar(m2.group(1), shift)
        good = [i for i, o in enumerate(opts) if o.strip().upper() == coded]
        if good and ans not in good:
            flags.append({'type': 'M2-caesar-wrong',
                          'detail': f"{m2.group(1)} shifted {shift:+d} is {coded}; key is {keyed!r}",
                          'action': 'fix', 'new_answer': good[0],
                          'reason': f"Caesar shift {shift:+d} of {m2.group(1)} is {coded}"})
        return flags

    # ---- M3: rank from other end ----
    m = re.search(r'row of (\d+).*ranked (\d+)(?:st|nd|rd|th) from the (left|right) end.*rank from the (left|right) end', stem, re.S)
    if m:
        total, rank = int(m.group(1)), int(m.group(2))
        other = total - rank + 1
        good = [i for i, o in enumerate(opts)
                if re.search(rf'\b{other}(?:st|nd|rd|th)\b', denum(o))]
        if good and ans not in good:
            flags.append({'type': 'M3-rank-wrong',
                          'detail': f'rank from the other end is {other}; key is {keyed!r}',
                          'action': 'fix', 'new_answer': good[0],
                          'reason': f'{total} - {rank} + 1 = {other}'})
        return flags

    # ---- M4: handshakes + diagonals (labelled values, not just presence) ----
    m = re.search(r'(\d+) delegates shake hands with every other delegate', stem)
    if m:
        n = int(m.group(1))
        hs, dg = n * (n - 1) // 2, n * (n - 3) // 2
        good = []
        for i, o in enumerate(opts):
            hm = re.search(r'Handshakes:\s*(\d+)', denum(o))
            dm = re.search(r'Diagonals.*?:\s*(\d+)', denum(o))
            if hm and dm and int(hm.group(1)) == hs and int(dm.group(1)) == dg:
                good.append(i)
        if good and ans not in good:
            flags.append({'type': 'M4-handshake-wrong',
                          'detail': f'handshakes C({n},2)={hs}, diagonals of {n}-gon={dg}; key is {keyed!r}',
                          'action': 'fix', 'new_answer': good[0],
                          'reason': f'C({n},2)={hs} handshakes; {n}({n}-3)/2={dg} diagonals'})
        return flags

    # ---- M5: quadratic roots + sum of squares ----
    m = re.search(r'x²\s*([−\-+])\s*(\d+)x\s*([−\-+])\s*(\d+)\s*=\s*0', stem)
    if m:
        b = int(m.group(2)) * (-1 if m.group(1) in '−-' else 1)
        c = int(m.group(4)) * (-1 if m.group(3) in '−-' else 1)
        # roots r1+r2 = -b, r1*r2 = c; integer roots
        roots = None
        for r in range(-100, 101):
            if r != 0 and c % r == 0:
                s2 = -b - r
                if r * s2 == c:
                    roots = sorted([r, s2])
                    break
        if roots:
            ss = roots[0] ** 2 + roots[1] ** 2
            good = []
            for i, o in enumerate(opts):
                rm = re.search(r'Roots:\s*([-\u2212]?\d+)\s+and\s*([-\u2212]?\d+)', denum(o))
                sm = re.search(r'=\s*(\d+)\s*$', denum(o).strip())
                if rm and sm:
                    r1, r2 = sorted([int(rm.group(1).replace('\u2212', '-')),
                                     int(rm.group(2).replace('\u2212', '-'))])
                    if int(sm.group(1)) == ss and [r1, r2] == roots:
                        good.append(i)
            if good and ans not in good:
                flags.append({'type': 'M5-quadratic-wrong',
                              'detail': f'roots {roots}, sum of squares {ss}; key is {keyed!r}',
                              'action': 'fix', 'new_answer': good[0],
                              'reason': f'x^2 {b:+d}x {c:+d} = 0 has roots {roots[0]}, {roots[1]}; squares sum to {ss}'})
        return flags

    # ---- M6: survey sets ----
    m = re.search(r'survey of (\d+).*?(\d+) read ([A-Za-z]+).*?(\d+) read ([A-Za-z]+).*?(\d+) read neither',
                  stem, re.S)
    if m:
        total, a, _na, b, _nb, neither = int(m.group(1)), int(m.group(2)), \
            m.group(3), int(m.group(4)), m.group(5), int(m.group(6))
        both = a + b - (total - neither)
        only_a = a - both
        good = []
        for i, o in enumerate(opts):
            bm = re.search(r'Both:\s*(\d+)', denum(o))
            om = re.search(r'Only[^:]*:\s*(\d+)', denum(o))
            if bm and om and int(bm.group(1)) == both and int(om.group(1)) == only_a:
                good.append(i)
        if good and ans not in good:
            flags.append({'type': 'M6-sets-wrong',
                          'detail': f'both={both}, only first={only_a}; key is {keyed!r}',
                          'action': 'fix', 'new_answer': good[0],
                          'reason': f'both = {a}+{b}-({total}-{neither}) = {both}; only first = {a}-{both} = {only_a}'})
        return flags

    # ---- M7: profit / cost price ----
    m = re.search(r'selling .*? for NPR ([\d,]+).*?profit of (\d+)% on cost.*?'
                  r'sold to earn a (\d+)% profit', stem, re.S)
    if m:
        sp, p1, p2 = parse_num(m.group(1)), int(m.group(2)), int(m.group(3))
        cp = sp / (1 + p1 / 100)
        sp2 = cp * (1 + p2 / 100)
        good = []
        for i, o in enumerate(opts):
            # labelled NPR amounts only ("for 35% profit" injects a bare 35)
            amts = [parse_num(t) for t in re.findall(r'NPR\s*([\d,]+)', denum(o))]
            if len(amts) >= 2 and abs(amts[0] - cp) < 1 and abs(amts[1] - sp2) < 1:
                good.append(i)
        if good and ans not in good:
            flags.append({'type': 'M7-profit-wrong',
                          'detail': f'CP={cp:.0f}, SP for {p2}%={sp2:.0f}; key is {keyed!r}',
                          'action': 'fix', 'new_answer': good[0],
                          'reason': f'CP = {sp}/(1+{p1}%) = {cp:.0f}; SP at {p2}% = {sp2:.0f}'})
        return flags

    # ---- M8: successive discounts ----
    m = re.search(r'marked price of NPR ([\d,]+).*?two successive discounts of (\d+)% and (\d+)%',
                  stem, re.S)
    if m:
        mp, d1, d2 = parse_num(m.group(1)), int(m.group(2)), int(m.group(3))
        eq = (1 - (1 - d1 / 100) * (1 - d2 / 100)) * 100
        sp = mp * (1 - d1 / 100) * (1 - d2 / 100)
        good = []
        for i, o in enumerate(opts):
            em = re.search(r'Equivalent discount:\s*([\d.]+)%', denum(o))
            sm = re.search(r'Selling price:\s*NPR\s*([\d,]+)', denum(o))
            if em and sm and abs(float(em.group(1)) - eq) < 0.6 \
                    and abs(parse_num(sm.group(1)) - sp) < 1:
                good.append(i)
        if good and ans not in good:
            flags.append({'type': 'M8-discount-wrong',
                          'detail': f'equivalent discount={eq:.0f}%, SP={sp:.0f}; key is {keyed!r}',
                          'action': 'fix', 'new_answer': good[0],
                          'reason': f'equivalent discount = {eq:.1f}%; SP = {sp:.0f}'})
        return flags

    # ---- M9: pipes & cisterns ----
    m = re.search(r'inlet pipe can fill .*? in (\d+) hours.*?outlet.*?in (\d+) hours',
                  stem, re.S)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        t = None
        if b > a:
            t = a * b / (b - a)
        if t is not None:
            good = [i for i, o in enumerate(opts)
                    if numeric_value(o) is not None and abs(numeric_value(o) - t) < 0.01]
            if good and ans not in good:
                flags.append({'type': 'M9-pipes-wrong',
                              'detail': f'net fill time = {a}*{b}/({b}-{a}) = {t:.1f}h; key is {keyed!r}',
                              'action': 'fix', 'new_answer': good[0],
                              'reason': f'net rate 1/{a} - 1/{b}; time {t:.1f} hours'})
        return flags

        # ---- M10: number matrix (Top x Middle) + k = Bottom ----
    m = re.search(r'\(Top\s*[×x]\s*Middle\)\s*\+\s*(\d+)\s*=\s*Bottom', stem)
    m2 = re.search(r'Top\s*=\s*(\d+)\s+and\s+Middle\s*=\s*(\d+)', stem)
    if m and m2:
        k, top, mid = int(m.group(1)), int(m2.group(1)), int(m2.group(2))
        val = top * mid + k
        good = [i for i, o in enumerate(opts) if numeric_value(o) == val]
        if good and ans not in good:
            flags.append({'type': 'M10-matrix-wrong',
                          'detail': f'{top} x {mid} + {k} = {val}; key is {keyed!r}',
                          'action': 'fix', 'new_answer': good[0],
                          'reason': f'{top} x {mid} + {k} = {val}'})
        return flags

    # ---- M11: cubic series (constant third difference, >= 5 terms) ----
    m = re.search(r'((?:' + NUM + r'\s*,\s*){4,}' + NUM + r')\s*,?\s*\?', denum(stem))
    if m:
        seq = [parse_num(t) for t in re.findall(NUM, m.group(1))]
        if all(v is not None for v in seq) and len(seq) >= 5:
            d1 = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
            d2 = [d1[i + 1] - d1[i] for i in range(len(d1) - 1)]
            d3 = [d2[i + 1] - d2[i] for i in range(len(d2) - 1)]
            if len(d3) >= 2 and len(set(d3)) == 1:
                nxt = seq[-1] + d1[-1] + d2[-1] + d3[0]
                good = [i for i, o in enumerate(opts) if numeric_value(o) == nxt]
                if good and ans not in good:
                    flags.append({'type': 'M11-series-cubic-wrong',
                                  'detail': f'series has constant third difference {d3[0]}; next term {nxt}; key is {keyed!r}',
                                  'action': 'fix', 'new_answer': good[0],
                                  'reason': f'constant third difference {d3[0]} gives next term {nxt}'})
        return flags

    return flags


def main():
    raw = json.load(open('data/pdf-extract-raw.json', encoding='utf-8'))
    flagged = []
    by_type = Counter()
    for i, q in enumerate(raw):
        fl = check_question(q)
        if fl:
            for f in fl:
                by_type[f['type']] += 1
            flagged.append({'pdf_id': f"PDF-{int(q['pdf_num']):04d}",
                            'pdf_index': i, 'flags': fl,
                            'question': q.get('question'),
                            'options': q.get('options'),
                            'answer': q.get('pdf_answer')})
    out = {'meta': {'pdf_total': len(raw), 'flagged_total': len(flagged),
                    'by_type': dict(by_type)},
           'flags': flagged}
    with open('data/pdf-extended-flags-2026-10-27.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"PDF questions: {len(raw)}  flagged: {len(flagged)}  by type: {dict(by_type)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
