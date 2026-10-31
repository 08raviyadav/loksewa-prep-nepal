#!/usr/bin/env python3
"""PDF answer-key / structure audit for Lok Sewa Prep Nepal (2026-10-27).

Checks each question in data/pdf-extract-raw.json (produced by a separate
PDF-extraction worker) BEFORE it is integrated into the bank. The bank
itself is never touched; this script only reads the PDF file and writes a
flags JSON. The extractor format is accepted as-is (pdf_num -> id,
pdf_answer -> answer; see normalise_record()). Note the real extract
has NO exam, difficulty, marks, subtopic, source or _ne fields, its
explanation is usually null, and its options mix English + Devanagari
in one string ("Citizenship (नागरिकता)") — the integration worker must
supply the missing schema fields and decide how to split the bilingual
options.

(a) Re-derived answers where computable:
    - arithmetic: single-operation + - x * / % expressions, "X% of Y",
      square / cube / square-root of a number, in the stem. The computed
      value is compared with the keyed option's numeric value.
    - number series: a comma-separated sequence ending in "?" — tested
      against arithmetic, geometric, squares, cubes, primes, Fibonacci
      and +increasing-increment patterns. Only flagged when exactly one
      pattern fits AND its next term is among the options AND the key
      points elsewhere.
    - factual lookups against a small built-in FACTS table (Constitution
      article numbers, Census 2021, NRB dates, Nepal structural facts).
      ONLY facts the author is certain of are in the table; anything
      outside it is left for human review, never guessed.
(b) Explanation/key contradictions (adapted from
    scripts/audit-answer-mismatch.py): the explanation's concluded value
    ("= 10", "answer is 10", "Option B is correct") names a different
    option than the key, or the explanation's text contains the full text
    of a non-keyed option while not containing the keyed option's text
    (the HEAL2-182 pattern: explanation says BCG, key says Measles).
(c) Structural breakage: <4 or >4 options, empty option/question/
    explanation, answer index out of range or missing, duplicate options
    (exact, after stripping a trailing parenthetical — the
    test-questions.js rule — and after stripping "(alt)"), duplicate
    question text within the PDF file itself, missing id, options_ne
    count mismatch when _ne fields are present.

Output: flags JSON:
  {"meta": {...}, "flags": [
     {"pdf_id", "pdf_index", "flags": [{"type", "detail"}, ...],
      "question", "options", "answer"}, ... ]}
Only questions with >= 1 flag appear in "flags". A question with no
flags is clean (not listed).

Flag types:
  key-wrong-arithmetic, key-wrong-series, key-wrong-fact,
  explanation-contradicts-key, explanation-names-other-option,
  dup-options, dup-options-paren, dup-options-alt, options-count,
  empty-option, empty-question, empty-explanation, answer-out-of-range,
  missing-id, dup-question-in-pdf, options-ne-count, question-too-short

Usage:
  python3 scripts/pdf-audit-2026-10-27.py [--pdf PATH] [--out PATH]
  --pdf: default data/pdf-extract-raw.json
  --out: default /tmp/pdf-audit-flags.json

Run from the project root. Read-only on the bank and on app.js.
"""
import argparse
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
    """Leading numeric value of an option, or None if not numeric."""
    s = denum(opt).strip()
    s2 = re.sub(r'^(Rs\.?|US\$|\$)\s*', '', s)
    s2 = re.sub(r'\s*(kg|km|m|cm|%|years?|days?|months?|hours?|minutes?|seconds?|MW|litres?|liters?|rupees?)$', '', s2, flags=re.I)
    s2 = s2.strip().rstrip('.')
    if re.fullmatch(r'-?\d[\d,]*\.?\d*', s2):
        return parse_num(s2)
    return None

# ---------------------------------------------------------------- facts ---
# ONLY facts the author is certain of. Each entry: (regex on the normalised
# stem, expected value as it should appear in the correct option, label).
# Article-number facts: the stem must ask which article guarantees a right;
# the check is that the keyed option contains the expected article number
# and no other article number.
FACTS = [
    (r'how many articles.*constitution of nepal|constitution of nepal.*how many articles',
     '308', 'Constitution of Nepal 2015 has 308 articles'),
    (r'how many schedules.*constitution of nepal|constitution of nepal.*how many schedules',
     '9', 'Constitution of Nepal 2015 has 9 schedules'),
    (r'how many parts.*constitution of nepal|constitution of nepal.*how many parts',
     '35', 'Constitution of Nepal 2015 has 35 parts'),
    (r'when.*constitution of nepal.*promulgated|constitution.*promulgated.*2072|constitution.*came into force',
     '2072', 'Constitution of Nepal promulgated 2072 Ashoj 3 (20 Sep 2015)'),
    (r'total population.*census 2021|population of nepal.*census 2021|census 2021.*total population',
     '29164578', 'Census 2021 (2078) total population 29,164,578'),
    (r'population growth rate.*census 2021|census 2021.*growth rate',
     '0.92', 'Census 2021 annual population growth rate 0.92%'),
    (r'how many districts.*nepal|total.*districts of nepal',
     '77', 'Nepal has 77 districts'),
    (r'how many provinces.*nepal|total.*provinces of nepal',
     '7', 'Nepal has 7 provinces'),
    (r'how many local levels.*nepal|total.*local levels',
     '753', 'Nepal has 753 local levels'),
    (r'area of nepal|total area.*nepal',
     '147516', 'Nepal area 147,516 sq km'),
    (r'height of.*(mount everest|sagarmatha)|how high.*sagarmatha|height of sagarmatha',
     '8848.86', 'Sagarmatha / Everest height 8,848.86 m'),
    (r'how many members.*house of representatives|house of representatives.*how many members',
     '275', 'House of Representatives has 275 members'),
    (r'how many members.*national assembly|national assembly.*how many members',
     '59', 'National Assembly has 59 members'),
    (r'nepal rastra bank.*established|when.*nrb.*established|nrb.*founded',
     '1956', 'Nepal Rastra Bank established 26 April 1956 (2013 BS)'),
    (r'national bird of nepal',
     'danphe', 'National bird of Nepal is Danphe (Lophophorus)'),
    (r'national animal of nepal',
     'cow', 'National animal of Nepal is the cow'),
    (r'national flower of nepal',
     'rhododendron', 'National flower of Nepal is Rhododendron (Laliguras)'),
    (r'national anthem of nepal',
     'sayaun thunga phulka', 'National anthem is "Sayaun Thunga Phulka"'),
]

# Fundamental-rights article numbers (Constitution of Nepal 2015, Part 3).
# Only the unambiguous one-right-one-article mappings are listed.
ARTICLE_RIGHTS = [
    (r'right to live with dignity', '16'),
    (r'right to freedom', '17'),
    (r'right to equality', '18'),
    (r'right to communication', '19'),
    (r'rights? relating to justice', '20'),
    (r'right of victim of crime', '21'),
    (r'right against torture', '22'),
    (r'right against preventive detention', '23'),
    (r'right against untouchability', '24'),
    (r'right relating to property', '25'),
    (r'right to religious freedom', '26'),
    (r'right to information', '27'),
    (r'right to privacy', '28'),
    (r'right against exploitation', '29'),
    (r'right to (a )?clean environment', '30'),
    (r'right relating to education', '31'),
    (r'right to language and culture', '32'),
    (r'right to employment', '33'),
    (r'right to labour', '34'),
    (r'right relating to health', '35'),
    (r'right relating to food', '36'),
    (r'right to housing', '37'),
    (r'rights? of women', '38'),
    (r'rights? of (the )?child', '39'),
    (r'rights? of dalit', '40'),
    (r'rights? of senior citizens?', '41'),
    (r'right to social justice', '42'),
    (r'right to social security', '43'),
    (r'consumer.{0,5}right', '44'),
    (r'right against exile', '45'),
    (r'right to constitutional remedies', '46'),
]

# ------------------------------------------------------------- arithmetic ---
ARITH_RE = re.compile(
    r'(?P<a>' + NUM + r')\s*(?P<op>\+|-|×|x|\*|/|÷|%)\s*(?P<b>' + NUM + r')\s*(?:=|\?|$)')
PCT_OF_RE = re.compile(r'(?P<p>' + NUM + r')\s*%\s*of\s+(?P<b>' + NUM + r')')
SQUARE_RE = re.compile(r'square of\s+(' + NUM + r')')
CUBE_RE = re.compile(r'cube of\s+(' + NUM + r')')
SQRT_RE = re.compile(r'square root of\s+(' + NUM + r')')

def derive_arithmetic(stem):
    """Return the computed value, or None when the stem has no single
    unambiguous arithmetic expression."""
    s = denum(stem)
    m = PCT_OF_RE.search(s)
    if m:
        p, b = parse_num(m.group('p')), parse_num(m.group('b'))
        if p is not None and b is not None:
            return p * b / 100
    m = SQUARE_RE.search(s)
    if m:
        v = parse_num(m.group(1))
        return v * v if v is not None else None
    m = CUBE_RE.search(s)
    if m:
        v = parse_num(m.group(1))
        return v ** 3 if v is not None else None
    m = SQRT_RE.search(s)
    if m:
        v = parse_num(m.group(1))
        if v is not None and v >= 0:
            r = v ** 0.5
            return r if abs(r - round(r)) < 1e-9 else None
        return None
    # single binary operation only: reject stems with 3+ numbers (a series
    # or a word problem with several figures is not safely derivable)
    nums = re.findall(NUM, s)
    if len(nums) != 2:
        return None
    m = ARITH_RE.search(s)
    if not m:
        return None
    a, b = parse_num(m.group('a')), parse_num(m.group('b'))
    if a is None or b is None:
        return None
    op = m.group('op')
    try:
        if op == '+':
            return a + b
        if op == '-':
            return a - b
        if op in ('×', 'x', '*'):
            return a * b
        if op in ('/', '÷'):
            return a / b if b != 0 else None
        if op == '%':
            return a % b if b != 0 else None
    except (ZeroDivisionError, OverflowError):
        return None
    return None

# ---------------------------------------------------------------- series ---
def _is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def series_next(seq):
    """Return the unique next term if exactly one known pattern fits the
    whole sequence, else None."""
    if len(seq) < 3 or any(not float(v).is_integer() for v in seq):
        return None
    seq = [int(v) for v in seq]
    fits = []
    diffs = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
    if len(set(diffs)) == 1:
        fits.append(seq[-1] + diffs[0])                       # arithmetic
    if all(seq[i] != 0 for i in range(len(seq) - 1)):
        ratios = [seq[i + 1] / seq[i] for i in range(len(seq) - 1)]
        if len(set(ratios)) == 1 and ratios[0] == int(ratios[0]):
            fits.append(seq[-1] * int(ratios[0]))             # geometric
    if all(v == (i + 1) ** 2 for i, v in enumerate(seq)) or \
       all(seq[i] == (seq[0] ** 0.5 + i) ** 2 for i in range(len(seq))):
        pass
    sq = [round(v ** 0.5) for v in seq]
    if all(s * s == v for s, v in zip(sq, seq)) and \
       len(set(sq[i + 1] - sq[i] for i in range(len(sq) - 1))) == 1:
        fits.append((sq[-1] + (sq[1] - sq[0])) ** 2)           # squares
    cb = [round(v ** (1 / 3)) for v in seq]
    if all(c ** 3 == v for c, v in zip(cb, seq)) and \
       len(set(cb[i + 1] - cb[i] for i in range(len(cb) - 1))) == 1:
        fits.append((cb[-1] + (cb[1] - cb[0])) ** 3)           # cubes
    if all(_is_prime(v) for v in seq):
        primes = []
        n = seq[-1] + 1
        while len(primes) < 1:
            if _is_prime(n):
                primes.append(n)
            n += 1
        fits.append(primes[0])                                 # primes
    if len(seq) >= 3 and all(seq[i] == seq[i - 1] + seq[i - 2] for i in range(2, len(seq))):
        fits.append(seq[-1] + seq[-2])                         # Fibonacci-like
    if len(set(diffs)) > 1:
        dd = [diffs[i + 1] - diffs[i] for i in range(len(diffs) - 1)]
        if len(set(dd)) == 1:
            fits.append(seq[-1] + diffs[-1] + dd[0])           # +increasing increment
    fits = sorted(set(fits))
    return fits[0] if len(fits) == 1 else None

SERIES_RE = re.compile(r'((?:' + NUM + r'\s*,\s*){2,}' + NUM + r')\s*,?\s*\?')

def derive_series(stem):
    m = SERIES_RE.search(denum(stem))
    if not m:
        return None
    seq = [parse_num(t) for t in re.findall(NUM, m.group(1))]
    if any(v is None for v in seq):
        return None
    return series_next(seq)

# ------------------------------------------------- explanation contradictions ---
EQ_RE = re.compile(r'=\s*(?:Rs\.?|रू\.?\s*)?(' + NUM + r')\s*(%|kg|cm|mm|m|km|years?|days?|hours?|minutes?)?', re.I)

def concluded_values(text):
    vals = []
    for m in EQ_RE.finditer(denum(text)):
        v = parse_num(m.group(1))
        if v is not None:
            vals.append(v)
    return vals

def check_explanation(q, opts, ans, flags):
    expl = q.get('explanation') or ''
    expl_ne = q.get('explanation_ne') or ''
    if not expl.strip() and not expl_ne.strip():
        return
    # explicit option letter
    for text in (expl, expl_ne):
        m = re.search(r'(?:correct answer is|answer is|answer:)\s*(?:option\s*)?\(?([A-D])\)?', text, re.I) or \
            re.search(r'option\s+([A-D])\s+is\s+correct', text, re.I)
        if m and ord(m.group(1).upper()) - 65 != ans:
            flags.append({'type': 'explanation-names-other-option',
                          'detail': f"explanation names option {m.group(1).upper()} but key is {chr(65 + ans)}"})
            return
    # numeric conclusion: last '= NUM' in the explanation equals a
    # different option's value (adapted from audit-answer-mismatch.py)
    marked_num = numeric_value(opts[ans])
    if marked_num is not None:
        opt_nums = [numeric_value(o) for o in opts]
        for src, text in (('EN', expl), ('NE', expl_ne)):
            vals = concluded_values(text)
            if not vals:
                continue
            last = vals[-1]
            if last != marked_num and last in opt_nums:
                sents = re.split(r'(?<=[.!])\s+', text.strip())
                final = sents[-1] if sents else ''
                fvals = concluded_values(final)
                for mm in re.finditer(r'(?:is|are|was|were)\s+(?:Rs\.?|रू\.?\s*)?(' + NUM + r')', denum(final), re.I):
                    v = parse_num(mm.group(1))
                    if v is not None:
                        fvals.append(v)
                if marked_num not in fvals:
                    flags.append({'type': 'explanation-contradicts-key',
                                  'detail': f"{src} explanation concludes {last} "
                                            f"(option {chr(65 + opt_nums.index(last))}) "
                                            f"but key is {marked_num} (option {chr(65 + ans)})"})
                    return
    # text containment: explanation contains the full text of a non-keyed
    # option but NOT the keyed option's text (HEAL2-182 pattern).
    n_expl = normalise(expl) + ' ' + normalise(expl_ne)
    if len(n_expl.strip()) < 3:
        return
    keyed = normalise(opts[ans])
    mentioned = []
    for i, o in enumerate(opts):
        no = normalise(o)
        if len(no) >= 3 and no in n_expl:
            mentioned.append(i)
    if mentioned and ans not in mentioned and len(mentioned) == 1:
        flags.append({'type': 'explanation-contradicts-key',
                      'detail': f"explanation names option {chr(65 + mentioned[0])} "
                                f"({opts[mentioned[0]]!r}) but never mentions the keyed "
                                f"option {chr(65 + ans)} ({opts[ans]!r})"})

def normalise_record(q):
    """Map the PDF extractor's field names onto the bank schema.

    Real extract format (data/pdf-extract-raw.json, landed 2026-10-27):
    pdf_num / topic / question / options / pdf_answer / explanation /
    raw_text — no id, no answer, no exam/difficulty/marks/subtopic,
    no _ne fields, explanation usually null. Map pdf_num -> id
    (PDF-0001 ...) and pdf_answer -> answer; everything else passes
    through unchanged. Records that already use the bank schema
    (id / answer) are left alone."""
    q = dict(q)
    if q.get('id') is None and q.get('pdf_num') is not None:
        try:
            q['id'] = f"PDF-{int(q['pdf_num']):04d}"
        except (TypeError, ValueError):
            q['id'] = f"PDF-{q['pdf_num']}"
    if q.get('answer') is None and q.get('pdf_answer') is not None:
        q['answer'] = q['pdf_answer']
    return q

# ------------------------------------------------------------------ main ---
def audit_question(q, i, seen_qtexts):
    flags = []
    qid = q.get('id')
    if not qid:
        flags.append({'type': 'missing-id', 'detail': 'no id field'})
    stem = q.get('question') or ''
    if not stem or not str(stem).strip():
        flags.append({'type': 'empty-question', 'detail': 'question is empty'})
        return qid or f'PDF-{i + 1:04d}', flags
    if len(str(stem).strip()) < 8:
        flags.append({'type': 'question-too-short',
                      'detail': f'question is {len(str(stem).strip())} chars'})
    opts = q.get('options')
    ans = q.get('answer')
    if not isinstance(opts, list) or len(opts) != 4:
        flags.append({'type': 'options-count',
                      'detail': f'options is {opts if not isinstance(opts, list) else len(opts)} (must be exactly 4)'})
        return qid or f'PDF-{i + 1:04d}', flags
    if any(not o or not str(o).strip() for o in opts):
        flags.append({'type': 'empty-option',
                      'detail': f'options: {opts}'})
    if not isinstance(ans, int) or not 0 <= ans < 4:
        flags.append({'type': 'answer-out-of-range',
                      'detail': f'answer is {ans!r} (must be int 0-3)'})
        # without a valid key the key-dependent checks below cannot run
        return qid or f'PDF-{i + 1:04d}', flags
    # duplicate options
    low = [str(o).strip().lower() for o in opts]
    if len(set(low)) != 4:
        flags.append({'type': 'dup-options',
                      'detail': f'duplicate options (exact, case-insensitive): {opts}'})
    strip_paren = lambda o: re.sub(r'\s*\([^()]*\)\s*$', '', str(o).strip().lower())
    stripped = [strip_paren(o) for o in opts]
    if len(set(stripped)) != 4 and len(set(low)) == 4:
        flags.append({'type': 'dup-options-paren',
                      'detail': f'options duplicate after stripping trailing parenthetical: {opts}'})
    alt_stripped = [re.sub(r'\s*\(alt\)\s*$', '', str(o).strip().lower(), flags=re.I) for o in opts]
    if len(set(alt_stripped)) != 4 and len(set(low)) == 4:
        flags.append({'type': 'dup-options-alt',
                      'detail': f'options duplicate after stripping "(alt)": {opts}'})
    # duplicate question text within the PDF file
    nq = normalise(stem)
    if nq in seen_qtexts:
        flags.append({'type': 'dup-question-in-pdf',
                      'detail': f'identical normalised stem as PDF question {seen_qtexts[nq]}'})
    else:
        seen_qtexts[nq] = qid or f'PDF-{i + 1:04d}'
    # _ne fields: if any present, options_ne must be 4
    has_ne = q.get('question_ne') is not None or q.get('options_ne') is not None or q.get('explanation_ne') is not None
    if has_ne and (not isinstance(q.get('options_ne'), list) or len(q.get('options_ne') or []) != 4):
        flags.append({'type': 'options-ne-count',
                      'detail': 'some _ne fields present but options_ne is not 4 entries'})
    if not (q.get('explanation') or '').strip():
        flags.append({'type': 'empty-explanation',
                      'detail': 'explanation is empty'})
    # (a) re-derived answers
    derived = derive_arithmetic(stem)
    if derived is not None:
        marked = numeric_value(opts[ans])
        if marked is not None and abs(marked - derived) > 1e-9:
            flags.append({'type': 'key-wrong-arithmetic',
                          'detail': f'stem computes to {derived} but key is {marked} (option {chr(65 + ans)}: {opts[ans]!r})'})
    else:
        nxt = derive_series(stem)
        if nxt is not None:
            marked = numeric_value(opts[ans])
            opt_nums = [numeric_value(o) for o in opts]
            if nxt in opt_nums and marked is not None and marked != nxt:
                flags.append({'type': 'key-wrong-series',
                              'detail': f'series continues with {nxt} (option {chr(65 + opt_nums.index(nxt))}) '
                                        f'but key is {marked} (option {chr(65 + ans)})'})
    nstem = normalise(stem)
    # (a) fact table — only when the stem matches a fact pattern
    for pat, expected, label in FACTS:
        if re.search(pat, nstem):
            keyed = normalise(opts[ans])
            exp_norm = normalise(expected)
            if exp_norm.isdigit():
                # numeric fact: keyed option's numeric value must equal it
                marked = numeric_value(opts[ans])
                if marked is not None and marked != parse_num(expected):
                    flags.append({'type': 'key-wrong-fact',
                                  'detail': f'{label}; key is {marked} (option {chr(65 + ans)}: {opts[ans]!r})'})
            else:
                if exp_norm not in keyed:
                    # only flag when the expected value IS one of the options
                    # (otherwise the fact pattern may have misfired)
                    if any(exp_norm in normalise(o) for o in opts):
                        flags.append({'type': 'key-wrong-fact',
                                      'detail': f'{label}; key is {opts[ans]!r}'})
            break
    # article-number facts
    if 'article' in nstem and 'which article' in nstem:
        for pat, num in ARTICLE_RIGHTS:
            if re.search(pat, nstem):
                keyed_nums = re.findall(r'\b\d+\b', denum(opts[ans]))
                if keyed_nums and num not in keyed_nums:
                    opt_with = [chr(65 + k) for k, o in enumerate(opts)
                                if num in re.findall(r'\b\d+\b', denum(o))]
                    if opt_with:
                        flags.append({'type': 'key-wrong-fact',
                                      'detail': f'right in the stem is guaranteed by Article {num}; '
                                                f'key is option {chr(65 + ans)} ({opts[ans]!r}), '
                                                f'Article {num} is option {opt_with[0]}'})
                break
    # (b) explanation / key contradictions
    check_explanation(q, opts, ans, flags)
    return qid or f'PDF-{i + 1:04d}', flags

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', default='data/pdf-extract-raw.json')
    ap.add_argument('--out', default='/tmp/pdf-audit-flags.json')
    args = ap.parse_args()

    try:
        raw = json.load(open(args.pdf, encoding='utf-8'))
    except FileNotFoundError:
        print(f'ERROR: {args.pdf} not found (extract not landed yet)', file=sys.stderr)
        return 2
    if isinstance(raw, dict):
        raw = raw.get('questions', raw.get('items', []))
    if not isinstance(raw, list):
        print(f'ERROR: {args.pdf} is not a JSON list', file=sys.stderr)
        return 2

    seen_qtexts = {}
    flagged = []
    by_type = Counter()
    for i, q in enumerate(raw):
        q = normalise_record(q)
        qid, flags = audit_question(q, i, seen_qtexts)
        if flags:
            for fl in flags:
                by_type[fl['type']] += 1
            flagged.append({'pdf_id': qid, 'pdf_index': i, 'flags': flags,
                            'question': q.get('question'),
                            'options': q.get('options'),
                            'answer': q.get('answer')})
    out = {'meta': {'pdf_total': len(raw), 'flagged_total': len(flagged),
                    'by_type': dict(by_type), 'pdf_file': args.pdf,
                    'note': ('key-wrong-* flags are computed re-derivations, '
                             'not guesses — but every flag still needs a human '
                             'read before any key is changed.')},
           'flags': flagged}
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f'PDF questions: {len(raw)}  flagged: {len(flagged)}  by type: {dict(by_type)}')
    print(f'Flags written to {args.out}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
