#!/usr/bin/env python3
"""PDF-extract dedupe for Lok Sewa Prep Nepal (2026-10-27).

Given data/pdf-extract-raw.json (questions extracted from a PDF by a
separate worker), check each PDF question against the CURRENT bank
(data/questions/*.json — 51,530 questions) and decide keep vs duplicate.

Checks (adapted from scripts/dedupe-check.py / audit-duplicates.py —
same normalisation and precision guards, because this bank is full of
same-template drills that differ by one key word):
  dup-exact  — normalised EN or NE stem identical to a bank question AND
               loose-same correct answer. An identical stem with a
               DIFFERENT key is a template stem / key conflict, NOT a dup:
               it is reported as dup-exact-key-conflict for human review.
  dup-near   — token-Jaccard >= 0.8 on the EN or NE stem, with the guards
               (numbers_compatible, tail_overlap, contrast_veto) and a
               loose-same correct answer.
  dup-near-key-conflict — near stem (>= 0.8) with guards passing but a
               DIFFERENT key: same question, conflicting answer. Human
               review — the PDF key may be wrong (this bank has had
               48%-wrong keys in one file) or the bank key may be.
  dup-options — near/exact stem AND the same 4-option set as a bank
               question, in a different order.
  dup-fact   — same fact asked two ways: content-token Jaccard >= 0.5
               AND loose-same correct answer AND >= 3 of 4 options
               shared. This status is ALWAYS "flag for human review" —
               the option-pool generator reuses identical option sets
               across different problems, so same-fact is never
               auto-decided (same rule as audit-duplicates.py).

Previous-Year 2083 protection: bank questions from
previous-year-2083.json are NEVER flagged for removal. This script only
ever reports PDF-side decisions; a match against a PY question means
the PDF copy is the duplicate (py_match: true in the decision record).
The bank is read-only — nothing here writes to data/questions/.

PDF input format: a JSON list of objects. Bank-schema records (id /
question / options / answer / ...) are used as-is. The real extractor
format is also accepted: pdf_num / topic / question / options /
pdf_answer / explanation / raw_text (pdf_num -> id "PDF-0001 ...",
pdf_answer -> answer; see normalise_record()). Objects without an id
or pdf_num get PDF-0001 etc.

Output: decisions JSON:
  {"meta": {...}, "decisions": [
     {"pdf_id", "pdf_index", "status", "match_bank_id",
      "match_bank_file", "py_match", "jac_en", "jac_ne",
      "content_jac", "same_options", "detail"}, ... ]}
Status values: keep, dup-exact, dup-near, dup-options, dup-fact,
dup-exact-key-conflict, dup-near-key-conflict.

Usage:
  python3 scripts/pdf-dedupe-2026-10-27.py [--pdf PATH] [--out PATH]
      [--bank-dir data/questions]
  --pdf: default data/pdf-extract-raw.json
  --out: default /tmp/pdf-dedupe-decisions.json

Run from the project root.
"""
import argparse
import difflib
import glob
import json
import math
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

DEV = str.maketrans('०१२३४५६७८९٠१२३४५६७८९', '01234567890123456789')
SUB = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')

# --- normalisation + guards (copied from scripts/dedupe-check.py) ---

def normalise(s):
    """Lowercase, digit-normalise, strip punctuation, collapse whitespace."""
    if s is None:
        return ''
    s = str(s).translate(DEV).translate(SUB).translate(SUP)
    s = unicodedata.normalize('NFKC', s).lower()
    s = re.sub(r'[^\w\s]', ' ', s, flags=re.UNICODE)
    s = s.replace('_', ' ')
    return re.sub(r'\s+', ' ', s).strip()

def tokens(s):
    n = normalise(s)
    return set(n.split()) if n else set()

STOP = set('''what which who whom whose when where why how is are was were be been being
am the a an of in on for to by from with and or not nor but if then than so as at
into over under between among through during before after above below out up down
choose select following correct statement statements option options given below
which of the following is are was were does do did can could should would may might
this that these those there here it its one two first second'''.split())

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
    return normalise(re.sub(r'\([^()]*\)', ' ', str(s) if s else ''))

def loose_same_correct(a, b):
    """Same correct answer allowing different wording of the same fact.
    STRICT: numeric equality alone does NOT count, near-identical strings
    do NOT count ('25 years' vs '35 years', 'Article 21' vs 'Article 22')."""
    if not a or not b:
        return False
    na, nb = normalise(a), normalise(b)
    if na == nb:
        return True
    if na.replace(' ', '') == nb.replace(' ', ''):
        return True
    ca, cb = numword_norm(strip_paren(a)), numword_norm(strip_paren(b))
    if ca and ca == cb:
        return True
    ta, tb = set(numword_norm(a).split()), set(numword_norm(b).split())
    if ta and tb and (ta <= tb or tb <= ta):
        small, big = (ta, tb) if ta <= tb else (tb, ta)
        extra = big - small
        if not extra or any(not t.replace('.', '', 1).isdigit() for t in extra):
            return True
    ca_toks, cb_toks = ca.split(), cb.split()
    if len(ca_toks) == 1 and len(cb_toks) == 1:
        x, y = ca_toks[0], cb_toks[0]
        if (len(x) >= 4 and len(y) >= 4 and not x.isdigit() and not y.isdigit()
                and x[:3] == y[:3]
                and difflib.SequenceMatcher(None, x, y).ratio() >= 0.7):
            return True
    if len(ta) == 1 and len(tb) == 1:
        x, y = next(iter(ta)), next(iter(tb))
        if (len(x) >= 4 and len(y) >= 4 and not x.isdigit() and not y.isdigit()
                and x[:3] == y[:3]):
            if difflib.SequenceMatcher(None, x, y).ratio() >= 0.7:
                return True
    return False

def number_occurrences(text):
    toks = normalise(text).split()
    out = []
    for i, t in enumerate(toks):
        if re.fullmatch(r'-?\d[\d,]*\.?\d*', t):
            try:
                v = float(t.replace(',', ''))
            except ValueError:
                continue
            out.append((v, toks[i - 1] if i > 0 else '', toks[i + 1] if i + 1 < len(toks) else ''))
    return out

CONTRAST_PAIRS = {
    frozenset(p) for p in [
        ('men', 'women'), ('male', 'female'), ('boy', 'girl'), ('man', 'woman'),
        ('civil', 'criminal'), ('primary', 'secondary'), ('first', 'last'),
        ('largest', 'smallest'), ('longest', 'shortest'), ('highest', 'lowest'),
        ('most', 'least'), ('before', 'after'), ('left', 'right'),
        ('upper', 'lower'), ('positive', 'negative'), ('acute', 'chronic'),
        ('direct', 'indirect'), ('internal', 'external'), ('public', 'private'),
        ('open', 'closed'), ('true', 'false'), ('increases', 'decreases'),
        ('rich', 'poor'), ('urban', 'rural'), ('young', 'old'), ('new', 'old'),
        ('fast', 'slow'), ('big', 'small'), ('hot', 'cold'), ('long', 'short'),
        ('high', 'low'), ('early', 'late'), ('easy', 'difficult'),
        ('simple', 'complex'), ('national', 'international'),
        ('domestic', 'foreign'), ('legal', 'illegal'), ('formal', 'informal'),
        ('active', 'passive'), ('strong', 'weak'), ('full', 'empty'),
        ('right', 'wrong'), ('correct', 'incorrect'), ('us', 'french'),
        ('hosted', 'won'), ('discovered', 'invented'),
    ]
}

def content_tokens(s):
    return tokens(s) - STOP

def contrast_veto(qa, qb):
    da = content_tokens(qa.get('question')) - content_tokens(qb.get('question'))
    db = content_tokens(qb.get('question')) - content_tokens(qa.get('question'))
    for x in da:
        for y in db:
            if frozenset((x, y)) in CONTRAST_PAIRS:
                return True
    return False

def tail_overlap(qa, qb):
    def tail(q):
        toks = [t for t in normalise(q.get('question')).split() if t not in STOP]
        return set(toks[-3:])
    ta, tb = tail(qa), tail(qb)
    if not ta or not tb:
        return True
    return bool(ta & tb)

def numbers_compatible(qa, qb):
    for field in ('question', 'question_ne'):
        oa, ob = number_occurrences(qa.get(field)), number_occurrences(qb.get(field))
        if not oa or not ob:
            continue
        va = sorted(v for v, _, _ in oa)
        vb = sorted(v for v, _, _ in ob)
        if va != vb:
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

def numbers_multiset_compatible(qa, qb):
    """Relaxed number check for the dup-fact (human-review) path: if BOTH
    stems carry numbers, the number multisets must match — but neighbour
    context is ignored, because rewordings move numbers ('Father is 30'
    vs 'Father 30'). Used ONLY where a human reads the result."""
    for field in ('question', 'question_ne'):
        oa, ob = number_occurrences(qa.get(field)), number_occurrences(qb.get(field))
        if not oa or not ob:
            continue
        if sorted(v for v, _, _ in oa) != sorted(v for v, _, _ in ob):
            return False
    return True

def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    return inter / len(a | b) if (a | b) else 0.0

# --- bank loading ---

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

def prep(q, fname, idx):
    q['_file'] = fname
    q['_idx'] = idx
    q['_py'] = fname == 'previous-year-2083.json' or '-2083-' in str(q.get('id', ''))
    q['_norm_en'] = normalise(q.get('question'))
    q['_norm_ne'] = normalise(q.get('question_ne'))
    q['_tok_en'] = tokens(q.get('question'))
    q['_tok_ne'] = tokens(q.get('question_ne'))
    q['_ctok_en'] = content_tokens(q.get('question'))
    opts = q.get('options') or []
    q['_opt_norm'] = [normalise(o) for o in opts]
    q['_opt_set'] = frozenset(q['_opt_norm'])
    ans = q.get('answer')
    q['_correct'] = q['_opt_norm'][ans] if isinstance(ans, int) and 0 <= ans < len(q['_opt_norm']) else ''
    q['_correct_raw'] = opts[ans] if isinstance(ans, int) and 0 <= ans < len(opts) else ''
    return q

def load_bank(bank_dir):
    qs = []
    for f in sorted(glob.glob(os.path.join(bank_dir, '*.json'))):
        base = os.path.basename(f)
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            print('BROKEN', f, e, file=sys.stderr)
            continue
        for i, q in enumerate(d):
            qs.append(prep(dict(q), base, i))
    return qs

# --- indices over the bank ---

class BankIndex:
    def __init__(self, qs):
        self.qs = qs
        self.exact_en = defaultdict(list)
        self.exact_ne = defaultdict(list)
        self.opt_set = defaultdict(list)
        self.opt3 = defaultdict(list)   # shared 3-option subsets -> bank idx
        self.correct_norm = defaultdict(list)
        for qi, q in enumerate(qs):
            if q['_norm_en']:
                self.exact_en[q['_norm_en']].append(qi)
            if q['_norm_ne']:
                self.exact_ne[q['_norm_ne']].append(qi)
            if q['_opt_set']:
                self.opt_set[q['_opt_set']].append(qi)
            opts = sorted(q['_opt_set'])
            if len(opts) == 4:
                for a in range(4):
                    self.opt3[tuple(opts[:a] + opts[a + 1:])].append(qi)
            if q['_correct']:
                self.correct_norm[q['_correct']].append(qi)
        # Prefix-filter index for Jaccard >= 0.8 (same method as
        # dedupe-check.py): tokens ordered by global DF, rarest first.
        df = Counter()
        for q in qs:
            for t in q['_tok_en']:
                df[t] += 1
            for t in q['_tok_ne']:
                df[t] += 1
        self.order = {t: i for i, t in enumerate(sorted(df, key=lambda t: (df[t], t)))}
        self.prefix_en = defaultdict(list)
        self.prefix_ne = defaultdict(list)
        for qi, q in enumerate(qs):
            for getter, index in ((lambda qq: qq['_tok_en'], self.prefix_en),
                                  (lambda qq: qq['_tok_ne'], self.prefix_ne)):
                toks = sorted(getter(q), key=lambda t: self.order.get(t, 1 << 30))
                n = len(toks)
                if n == 0:
                    continue
                plen = max(1, min(n, n - math.ceil(0.8 * n) + 1))
                for t in toks[:plen]:
                    index[t].append(qi)

    def near_candidates(self, pq, field):
        """Bank idxs that could have Jaccard >= 0.8 with pq on `field`."""
        getter = '_tok_en' if field == 'en' else '_tok_ne'
        index = self.prefix_en if field == 'en' else self.prefix_ne
        toks = sorted(pq[getter], key=lambda t: self.order.get(t, 1 << 30))
        n = len(toks)
        if n == 0:
            return set()
        plen = max(1, min(n, n - math.ceil(0.8 * n) + 1))
        out = set()
        for t in toks[:plen]:
            out.update(index.get(t, ()))
        return out

    def fact_candidates(self, pq):
        """Bank idxs sharing >= 3 options with pq, or the same correct
        answer (normalised). Used only for the dup-fact (human-review)
        check."""
        out = set()
        opts = sorted(pq['_opt_set'])
        if len(opts) == 4:
            for a in range(4):
                out.update(self.opt3.get(tuple(opts[:a] + opts[a + 1:]), ()))
        if pq['_correct']:
            out.update(self.correct_norm.get(pq['_correct'], ()))
        return out

# --- per-PDF-question classification ---

def classify(pq, idx):
    """Return (status, bank_q_or_None, metrics_dict)."""
    # (a) exact stems — check ALL bank questions sharing the stem: if ANY
    # has a loose-same correct answer this is a dup-exact; only if none
    # does is it a key conflict (the first candidate may be a different
    # template drill sharing the stem).
    conflict = None
    for field, mapping in (('_norm_en', idx.exact_en), ('_norm_ne', idx.exact_ne)):
        norm = pq[field]
        if not norm:
            continue
        for bi in mapping.get(norm, ()):
            bq = idx.qs[bi]
            if not numbers_compatible(pq, bq) or not tail_overlap(pq, bq) or contrast_veto(pq, bq):
                continue
            loose = loose_same_correct(pq['_correct_raw'], bq['_correct_raw'])
            metrics = {'jac_en': round(jaccard(pq['_tok_en'], bq['_tok_en']), 3),
                       'jac_ne': round(jaccard(pq['_tok_ne'], bq['_tok_ne']), 3),
                       'content_jac': round(jaccard(pq['_ctok_en'], bq['_ctok_en']), 3),
                       'same_options': bool(pq['_opt_set']) and pq['_opt_set'] == bq['_opt_set']}
            if loose:
                return 'dup-exact', bq, metrics
            if conflict is None:
                conflict = (bq, metrics)
    if conflict:
        # identical stem, different key: template stem or key conflict
        return 'dup-exact-key-conflict', conflict[0], conflict[1]
    # (b)/(c) near stems + same-options-reordered
    cand = idx.near_candidates(pq, 'en') | idx.near_candidates(pq, 'ne')
    best = None  # (score, status, bq, metrics)
    near_conflict = None  # (score, bq, metrics): near stem, different key
    for bi in cand:
        bq = idx.qs[bi]
        jac_en = jaccard(pq['_tok_en'], bq['_tok_en'])
        jac_ne = jaccard(pq['_tok_ne'], bq['_tok_ne'])
        if jac_en < 0.8 and jac_ne < 0.8:
            continue
        same_opts = bool(pq['_opt_set']) and pq['_opt_set'] == bq['_opt_set']
        order_differs = same_opts and pq['_opt_norm'] != bq['_opt_norm']
        if not (numbers_compatible(pq, bq) and tail_overlap(pq, bq)) or contrast_veto(pq, bq):
            continue
        metrics = {'jac_en': round(jac_en, 3), 'jac_ne': round(jac_ne, 3),
                   'content_jac': round(jaccard(pq['_ctok_en'], bq['_ctok_en']), 3),
                   'same_options': same_opts}
        loose = loose_same_correct(pq['_correct_raw'], bq['_correct_raw'])
        if not loose:
            # Near stem, conflicting key — same question, different answer.
            # Record the closest one; surfaced as dup-near-key-conflict
            # (human review) if no true duplicate is found.
            score = max(jac_en, jac_ne)
            if near_conflict is None or score > near_conflict[0]:
                near_conflict = (score, bq, metrics)
            continue
        status = 'dup-options' if (same_opts and order_differs) else 'dup-near'
        score = max(jac_en, jac_ne)
        if best is None or score > best[0]:
            best = (score, status, bq, metrics)
    if best:
        return best[1], best[2], best[3]
    if near_conflict:
        return 'dup-near-key-conflict', near_conflict[1], near_conflict[2]
    # (d) same-fact — human review only, never auto-decided. Guards are
    # deliberately RELAXED here vs (a)/(b): dup-fact false positives cost
    # one human read, false negatives lose a duplicate. So the tail check
    # is dropped (rewordings move the question word: '... lies in which
    # province?' vs 'In which province ... does ... lie?') and the number
    # check is multiset-only (rewordings move numbers next to different
    # words: 'Father is 30' vs 'Father 30'). contrast_veto stays: a
    # swapped contrast pair is a different question, not a rewording.
    best_fact = None
    for bi in idx.fact_candidates(pq):
        bq = idx.qs[bi]
        shared = len(pq['_opt_set'] & bq['_opt_set'])
        if shared < 3:
            continue
        cjac = jaccard(pq['_ctok_en'], bq['_ctok_en'])
        if cjac < 0.5:
            continue
        if not numbers_multiset_compatible(pq, bq) or contrast_veto(pq, bq):
            continue
        if not loose_same_correct(pq['_correct_raw'], bq['_correct_raw']):
            continue
        metrics = {'jac_en': round(jaccard(pq['_tok_en'], bq['_tok_en']), 3),
                   'jac_ne': round(jaccard(pq['_tok_ne'], bq['_tok_ne']), 3),
                   'content_jac': round(cjac, 3),
                   'same_options': bool(pq['_opt_set']) and pq['_opt_set'] == bq['_opt_set']}
        if best_fact is None or cjac > best_fact[0]:
            best_fact = (cjac, bq, metrics)
    if best_fact:
        return 'dup-fact', best_fact[1], best_fact[2]
    return 'keep', None, {'jac_en': 0.0, 'jac_ne': 0.0, 'content_jac': 0.0,
                          'same_options': False}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', default='data/pdf-extract-raw.json')
    ap.add_argument('--out', default='/tmp/pdf-dedupe-decisions.json')
    ap.add_argument('--bank-dir', default='data/questions')
    args = ap.parse_args()

    bank = load_bank(args.bank_dir)
    print(f'Bank: {len(bank)} questions '
          f'({sum(1 for q in bank if q["_py"])} Previous Year 2083)', file=sys.stderr)
    idx = BankIndex(bank)

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

    decisions = []
    by_status = Counter()
    for i, q in enumerate(raw):
        q = normalise_record(q)
        pq = prep(dict(q), 'pdf-extract', i)
        pq_id = q.get('id') or f'PDF-{i + 1:04d}'
        status, bq, metrics = classify(pq, idx)
        by_status[status] += 1
        dec = {'pdf_id': pq_id, 'pdf_index': i, 'status': status,
               'match_bank_id': bq['id'] if bq else None,
               'match_bank_file': bq['_file'] if bq else None,
               'py_match': bool(bq and bq['_py']),
               'jac_en': metrics['jac_en'], 'jac_ne': metrics['jac_ne'],
               'content_jac': metrics['content_jac'],
               'same_options': metrics['same_options'],
               'pdf_question': q.get('question'),
               'pdf_correct': pq['_correct_raw'],
               'bank_correct': bq['_correct_raw'] if bq else None}
        if status == 'dup-fact':
            dec['detail'] = ('same-fact candidate — HUMAN REVIEW required; '
                             'do not auto-drop (option-pool reuse makes this '
                             'unreliable without a human read)')
        elif status == 'dup-exact-key-conflict':
            dec['detail'] = ('identical stem but different key — template '
                             'stem or key conflict; HUMAN REVIEW required, '
                             'never auto-drop')
        elif status == 'dup-near-key-conflict':
            dec['detail'] = ('near-identical stem (>= 0.8 Jaccard) but a '
                             'different key — same question, conflicting '
                             'answer; HUMAN REVIEW required (PDF key may be '
                             'wrong, or the bank key may be)')
        elif bq and bq['_py']:
            dec['detail'] = ('match is a Previous Year 2083 question — the '
                             'bank copy is protected; the PDF copy is the '
                             'duplicate')
        decisions.append(dec)

    out = {'meta': {'bank_total': len(bank),
                    'py_total': sum(1 for q in bank if q['_py']),
                    'pdf_total': len(raw),
                    'by_status': dict(by_status),
                    'pdf_file': args.pdf,
                    'note': ('dup-fact and dup-exact-key-conflict are human-'
                             'review only. Previous Year 2083 bank questions '
                             'are never flagged for removal.')},
           'decisions': decisions}
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f'PDF questions: {len(raw)}  by status: {dict(by_status)}')
    print(f'Decisions written to {args.out}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
