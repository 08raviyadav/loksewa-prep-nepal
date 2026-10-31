#!/usr/bin/env python3
"""Shared helpers for Round-10 expansion generators (Lok Sewa Prep Nepal).

Rules enforced here:
- ids: R10-<FILE>-<NNNN>, unique across all R10 files (tracked in a registry).
- every question: EN + real Nepali (question_ne, options_ne[4], explanation_ne),
  Devanagari digits in _ne fields, 4 distinct options, answer 0-3, marks 1|2.
- explanations: the LAST '= value' in EN/NE must equal the marked answer
  (audit-answer-mismatch.py heuristic), so worked solutions end on the answer.
- in-generator dedupe vs the full bank: exact stem, token-Jaccard >= 0.8
  (with the numeric-drill veto from dedupe-check.py), same-fact check.
  The authoritative gate remains scripts/dedupe-check.py run at the end.
"""
import json, glob, math, random, re, sys, unicodedata
from collections import defaultdict

DEV = str.maketrans('0123456789', '०१२३४५६७८९')
ARAB = str.maketrans('०१२३४५६७८९', '0123456789')

def dev(x):
    """Arabic digits -> Devanagari digits (int/float/str)."""
    return str(x).translate(DEV)

def dev_num(x):
    """Format a number for Nepali text: Devanagari digits, no commas."""
    if isinstance(x, float) and x == int(x):
        x = int(x)
    return str(x).translate(DEV)

def fmt(x):
    """English number formatting: int if whole, else trimmed to 2dp."""
    if isinstance(x, float):
        if x == int(x):
            return str(int(x))
        return f"{x:.2f}".rstrip('0').rstrip('.')
    return str(x)

# ---------------------------------------------------------------- bank index
_NORM_RE = re.compile(r'[^\w\s]', re.UNICODE)
def normalise(s):
    if s is None:
        return ''
    s = str(s).translate(ARAB)
    s = unicodedata.normalize('NFKC', s).lower()
    s = _NORM_RE.sub(' ', s)
    return re.sub(r'\s+', ' ', s).strip()

STOP = set('''what which who whom whose when where why how is are was were be been being
am the a an of in on for to by from with and or not nor but if then than so as at
into over under between among through during before after above below out up down
choose select following correct statement statements option options given below
which of the following is are was were does do did can could should would may might
this that these those there here it its one two first second'''.split())

def tokens(s):
    return set(normalise(s).split()) if normalise(s) else set()

def content_tokens(s):
    return tokens(s) - STOP

def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

NUM_RE = re.compile(r'-?\d[\d,]*\.?\d*')
def number_occurrences(text):
    toks = normalise(text).split()
    out = []
    for i, t in enumerate(toks):
        if re.fullmatch(r'-?\d[\d,]*\.?\d*', t):
            try:
                v = float(t.replace(',', ''))
            except ValueError:
                continue
            out.append((v, toks[i-1] if i > 0 else '', toks[i+1] if i+1 < len(toks) else ''))
    return out

def numbers_compatible(qa, qb):
    for field in ('question', 'question_ne'):
        oa, ob = number_occurrences(qa.get(field)), number_occurrences(qb.get(field))
        if not oa or not ob:
            continue
        if sorted(v for v, _, _ in oa) != sorted(v for v, _, _ in ob):
            return False
        remaining = list(ob)
        for v, prev, nxt in oa:
            hit = None
            for k, (v2, p2, n2) in enumerate(remaining):
                if v2 == v and (p2 == prev or n2 == nxt):
                    hit = k
                    break
            if hit is None:
                return False
            remaining.pop(hit)
    return True

NUMWORDS = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
            'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13',
            'fourteen': '14', 'fifteen': '15', 'sixteen': '16',
            'seventeen': '17', 'eighteen': '18', 'nineteen': '19',
            'twenty': '20', 'thirty': '30', 'forty': '40', 'fifty': '50',
            'sixty': '60', 'seventy': '70', 'eighty': '80', 'ninety': '90',
            'hundred': '100', 'thousand': '1000'}

def numword_norm(s):
    toks = normalise(s).split()
    return ' '.join(NUMWORDS.get(t, t) for t in toks)

def strip_paren(s):
    return re.sub(r'\([^()]*\)', ' ', normalise(s)).strip()

def loose_same_correct(a, b):
    """Same correct answer allowing different wording of the same fact."""
    if not a or not b:
        return False
    na, nb = normalise(a), normalise(b)
    if na == nb:
        return True
    ca, cb = numword_norm(strip_paren(a)), numword_norm(strip_paren(b))
    if ca and ca == cb:
        return True
    ta, tb = set(numword_norm(a).split()), set(numword_norm(b).split())
    if ta and tb and (ta <= tb or tb <= ta):
        return True
    return False

class Bank:
    """Read-only index of the current bank (excluding R10 files)."""
    def __init__(self, exclude_prefix='R10-'):
        self.qs = []
        self.exact = set()          # normalised EN + NE stems
        self.tok_index = defaultdict(list)  # token -> [bank idx], rare tokens only
        self.by_id = {}
        raw = []
        for f in sorted(glob.glob('data/questions/*.json')):
            try:
                d = json.load(open(f, encoding='utf-8'))
            except Exception as e:
                print('BROKEN', f, e, file=sys.stderr)
                continue
            for q in d:
                if str(q.get('id', '')).startswith(exclude_prefix):
                    continue
                raw.append(q)
        from collections import Counter
        df = Counter()
        for q in raw:
            for t in tokens(q.get('question')) | tokens(q.get('question_ne')):
                df[t] += 1
        for q in raw:
            q = dict(q)
            q['_tok_en'] = tokens(q.get('question'))
            q['_tok_ne'] = tokens(q.get('question_ne'))
            q['_ctok_en'] = content_tokens(q.get('question'))
            opts = q.get('options') or []
            q['_opt_norm'] = [normalise(o) for o in opts]
            q['_opt_set'] = frozenset(q['_opt_norm'])
            ans = q.get('answer')
            q['_correct'] = q['_opt_norm'][ans] if isinstance(ans, int) and 0 <= ans < len(q['_opt_norm']) else ''
            self.qs.append(q)
            self.by_id[q['id']] = q
            for s in (normalise(q.get('question')), normalise(q.get('question_ne'))):
                if s:
                    self.exact.add(s)
            for t in q['_tok_en'] | q['_tok_ne']:
                if df[t] <= 400:  # rare-token index: Jaccard>=0.8 pairs share rare tokens
                    self.tok_index[t].append(len(self.qs) - 1)
        print(f'Bank index: {len(self.qs)} questions, {len(self.exact)} exact stems', file=sys.stderr)

    def check(self, q):
        """Return (is_dup, reason, bank_id) or (False, '', None)."""
        ne = normalise(q.get('question'))
        nn = normalise(q.get('question_ne'))
        if ne in self.exact or (nn and nn in self.exact):
            return True, 'exact-stem', None
        toks = tokens(q.get('question')) | tokens(q.get('question_ne'))
        cand = defaultdict(int)
        for t in toks:
            for i in self.tok_index.get(t, []):
                cand[i] += 1
        qtok_en = tokens(q.get('question'))
        qtok_ne = tokens(q.get('question_ne'))
        qctok = content_tokens(q.get('question'))
        qopts = frozenset(normalise(o) for o in (q.get('options') or []))
        ans = q.get('answer')
        qcorr = normalise((q.get('options') or [])[ans]) if isinstance(ans, int) and 0 <= ans < len(q.get('options') or []) else ''
        for i, shared in cand.items():
            if shared < 2:
                continue
            b = self.qs[i]
            je = jaccard(qtok_en, b['_tok_en'])
            jn = jaccard(qtok_ne, b['_tok_ne'])
            if (je >= 0.8 or jn >= 0.8):
                # mirror dedupe-check.py: near stem is a dup only with the
                # same correct answer (loose) or the same option set, and
                # only when the numeric-drill veto passes. A shared template
                # with a different tested word/answer is NOT a duplicate.
                same_opts = bool(qopts) and qopts == b['_opt_set']
                bcorr_raw = (b.get('options') or [])[b['answer']] if isinstance(b.get('answer'), int) and 0 <= b['answer'] < len(b.get('options') or []) else ''
                loose = loose_same_correct(qcorr, bcorr_raw)
                if (loose or same_opts) and numbers_compatible(q, b):
                    return True, f'near-jac en={je:.2f} ne={jn:.2f}', b['id']
            # same-fact: content Jaccard >= 0.7, same correct, >=3 shared options
            cj = jaccard(qctok, b['_ctok_en'])
            if cj >= 0.7 and qcorr and qcorr == b['_correct'] and len(qopts & b['_opt_set']) >= 3:
                if numbers_compatible(q, b):
                    return True, f'same-fact cjac={cj:.2f}', b['id']
        return False, '', None

# ---------------------------------------------------------------- registry
_REGISTRY = set()
def fresh_id(prefix, n):
    i = f'{prefix}-{n:04d}'
    assert i not in _REGISTRY, f'duplicate id {i}'
    _REGISTRY.add(i)
    return i

# ---------------------------------------------------------------- question builder
class Emitter:
    """Collects questions for one file; dedupes against bank + own batch."""
    def __init__(self, bank, prefix, start=1):
        self.bank = bank
        self.prefix = prefix
        self.n = start
        self.out = []
        self.seen_stems = set()
        self.rejected = []   # (reason, question)
        self.rng = random.Random(20261026)

    def emit(self, exam, topic, subtopic, difficulty, marks,
             q_en, q_ne, opts_en, opts_ne, ans_idx, expl_en, expl_ne,
             source='Original practice question — Lok Sewa Prep Nepal'):
        # validation: skip (don't crash) on malformed option sets
        if not (len(opts_en) == 4 and len(opts_ne) == 4):
            self.rejected.append(('bad-option-count', q_en))
            return None
        if not (0 <= ans_idx < 4):
            self.rejected.append(('bad-answer-index', q_en))
            return None
        if len(set(o.strip().lower() for o in opts_en)) != 4:
            self.rejected.append((f'dup-options-EN: {opts_en}', q_en))
            return None
        if len(set(o.strip().lower() for o in opts_ne)) != 4:
            self.rejected.append((f'dup-options-NE: {opts_ne}', q_en))
            return None
        if not (q_en and q_ne and expl_en and expl_ne):
            self.rejected.append(('missing-field', q_en))
            return None
        # shuffle option order (deterministic rng)
        order = list(range(4))
        self.rng.shuffle(order)
        o_en = [opts_en[i] for i in order]
        o_ne = [opts_ne[i] for i in order]
        a = order.index(ans_idx)
        q = {
            'id': fresh_id(self.prefix, self.n),
            'exam': list(exam),
            'topic': topic,
            'subtopic': subtopic,
            'difficulty': difficulty,
            'marks': marks,
            'question': q_en,
            'question_ne': q_ne,
            'options': o_en,
            'options_ne': o_ne,
            'answer': a,
            'explanation': expl_en,
            'explanation_ne': expl_ne,
            'source': source,
        }
        self.n += 1
        # own-batch exact check
        ns = normalise(q_en)
        if ns in self.seen_stems:
            self.rejected.append(('own-batch-exact', q_en))
            return None
        self.seen_stems.add(ns)
        # bank check
        dup, reason, bid = self.bank.check(q)
        if dup:
            self.rejected.append((f'bank:{reason}:{bid}', q_en))
            return None
        self.out.append(q)
        return q

    def write(self, filename):
        with open(f'data/questions/{filename}', 'w', encoding='utf-8') as f:
            json.dump(self.out, f, indent=2, ensure_ascii=False)
            f.write('\n')
        print(f'{filename}: wrote {len(self.out)} questions, rejected {len(self.rejected)}', file=sys.stderr)
        return len(self.out)
