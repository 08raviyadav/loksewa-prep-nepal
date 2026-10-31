#!/usr/bin/env python3
"""Dedupe sweep for Lok Sewa Prep Nepal question bank.

Detects, across all data/questions/*.json:
  (a) exact duplicates   — normalised question text identical (EN or NE)
  (b) near-duplicates    — token-Jaccard >= 0.8 on the normalised stem (EN or NE)
  (c) same stem, options in a different order — (a)/(b) stem + identical
      option set (as a set) but different option order
  (d) same fact asked two ways, same correct answer — content-token
      Jaccard >= 0.5 (stopwords stripped) AND the same normalised correct
      answer AND >= 3 of 4 options shared (option-set Jaccard >= 0.5)

Normalisation (mirrors assets/js/app.js normaliseText/tokenJaccard, plus
digit handling): lowercase, Devanagari/Arabic-Indic digits -> Arabic,
sub/superscript digits -> Arabic, punctuation -> space, collapse whitespace.

Precision guards (learned from sampling: stem similarity alone is NOT a
duplicate signal in this bank — it is full of same-template items that
differ by one key word, e.g. primary vs secondary prevention, and of
same-scenario IQ sub-questions):
  * loose_same_correct is strict: same numeric value alone does NOT count
    (two different drills can share an answer), near-identical strings do
    NOT count ('25 years' vs '35 years', 'Article 21' vs 'Article 22').
  * numbers_compatible: if both stems carry numbers, the multisets must
    match and each number must share a neighbouring token, so '2 A / 6 ohm'
    vs '2 ohm / 6 A' (swapped roles) is a different problem.
  * tail_overlap: the last 3 content tokens of the stems must share one,
    so same-scenario different sub-questions are not merged.
  * NE-exact alone does NOT count: template stems share one generic Nepali
    translation while testing different words; NE-exact needs the same
    correct answer or >= 2 shared options as well.
  * Greedy star clustering: a member is removed only if it pairs DIRECTLY
    with its keeper, never via a chain.

Candidate generation uses exact prefix filtering (no false negatives for
the Jaccard threshold): tokens are ordered by global document frequency
(rarest first); two sets with Jaccard >= t must share a token in their
prefixes of length n - ceil(t*n) + 1. Type (d) candidates additionally come
from blocking on shared 3-option subsets.

Usage:
  python3 scripts/dedupe-check.py [--report PATH] [--apply REMOVALS_JSON]
  --report: write full JSON report (default /tmp/dedupe-report.json)
  --apply:  JSON file {"remove": ["ID", ...], "reword": [{"id": ..., ...}]}
            (not used by default — removals are decided by a human from the
            report, then applied). Without --apply this only reports.

Previous-Year 2083 questions (data/questions/previous-year-2083.json) are
flagged in the report but must NOT be removed unless they are exact
duplicates of each other; a bank question duplicating a PY question loses.
"""
import json, glob, math, re, sys, unicodedata
from collections import Counter, defaultdict

DEV = str.maketrans('०१२३४५६७८९٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
SUB = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')

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
    return set(normalise(s).split()) if normalise(s) else set()

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
    """'Five years' -> '5 years'; also strips parentheticals for comparison."""
    toks = normalise(s).split()
    return ' '.join(NUMWORDS.get(t, t) for t in toks)

def strip_paren(s):
    # strip parentheticals BEFORE normalise() removes the parens themselves
    return normalise(re.sub(r'\([^()]*\)', ' ', str(s) if s else ''))

def parse_leading_num(s):
    m = re.match(r'-?\d[\d,]*\.?\d*', normalise(s).strip())
    if not m:
        return None
    try:
        return float(m.group(0).replace(',', ''))
    except ValueError:
        return None

def loose_same_correct(a, b, correct_df=None):
    """Same correct answer allowing different wording of the same fact:
    '5 years' vs 'Five years', '1 Shrawan' vs '16 July (1 Shrawan)',
    'Laliguras (Rhododendron)' vs 'Rhododendron (Lali Gurans)'.
    Deliberately STRICT: numeric equality alone does NOT count (two
    different drills can share an answer, e.g. two SI problems both = 3000),
    and near-identical strings do NOT count ('25 years' vs '35 years',
    'Article 21' vs 'Article 22' are different answers)."""
    if not a or not b:
        return False
    na, nb = normalise(a), normalise(b)
    if na == nb:
        return True
    # same string modulo spaces/punctuation: 'Hard-working' vs 'Hardworking'
    if na.replace(' ', '') == nb.replace(' ', ''):
        return True
    ca, cb = numword_norm(strip_paren(a)), numword_norm(strip_paren(b))
    if ca and ca == cb:
        return True
    ta, tb = set(numword_norm(a).split()), set(numword_norm(b).split())
    if ta and tb and (ta <= tb or tb <= ta):
        # ...but not when the ONLY extra tokens are numbers: '13 July 2025'
        # vs 'July 2025', 'CnH2n' vs 'CnH2n+2' (tokenised as {cnh2n, 2}),
        # '6 years' vs '6-7 years' are different answers. '1 Shrawan' vs
        # '16 July (1 Shrawan)' still passes: the extra tokens include the
        # non-numeric 'july'.
        small, big = (ta, tb) if ta <= tb else (tb, ta)
        extra = big - small
        if not extra or any(not t.replace('.', '', 1).isdigit() for t in extra):
            return True
    # NOTE (2026-10-26): there used to be a 'shared RARE token' rule here
    # ('rhododendron' in both flower answers). It was RETIRED: a shared
    # headword is not the distinguishing fact — it matched 'pituitary' in
    # anterior vs posterior pituitary, 'hypertext' in HTML vs HTTP,
    # 'portable' in PDF vs PNG, 'quadrant' in first- vs third-angle
    # projection, 'cholesterol' in HDL ('good') vs LDL ('bad'), and
    # 'chemical' in Au (gold) vs O3 (ozone). Six questions were wrongly
    # removed by it and restored (see SELF-AUDIT dedupe section). The
    # flower case it was written for (Danphe/Danfe, Laliguras/Rhododendron)
    # is covered by the transliteration rule below instead.
    # single-token transliteration variants, also after stripping
    # parentheticals: 'danphe' vs 'danfe (himalayan monal)' -> core 'danfe'
    import difflib
    ca_toks, cb_toks = ca.split(), cb.split()
    if len(ca_toks) == 1 and len(cb_toks) == 1:
        x, y = ca_toks[0], cb_toks[0]
        if (len(x) >= 4 and len(y) >= 4 and not x.isdigit() and not y.isdigit()
                and x[:3] == y[:3]
                and difflib.SequenceMatcher(None, x, y).ratio() >= 0.7):
            return True
    # single-token transliteration variants: same >=3-letter prefix,
    # e.g. 'danphe' vs 'danfe'
    if len(ta) == 1 and len(tb) == 1:
        x, y = next(iter(ta)), next(iter(tb))
        if (len(x) >= 4 and len(y) >= 4 and not x.isdigit() and not y.isdigit()
                and x[:3] == y[:3]):
            if difflib.SequenceMatcher(None, x, y).ratio() >= 0.7:
                return True
    return False

NUM_RE = re.compile(r'-?\d[\d,]*\.?\d*')

def number_occurrences(text):
    """Ordered [(value, prev_token, next_token)] for numbers in a stem."""
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

# Word pairs whose swap changes the question (not a rewording): men/women,
# civil/criminal, primary/secondary ... If one stem has X where the other
# has Y for any pair here, the pair is NOT a duplicate. Deliberately
# excludes near-synonym swaps that ARE rewordings (largest/longest,
# founded/established, celebrated/observed, guarantees/deals).
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

def contrast_veto(qa, qb):
    """True when the stems swap a contrast pair (different question)."""
    da = content_tokens(qa.get('question')) - content_tokens(qb.get('question'))
    db = content_tokens(qb.get('question')) - content_tokens(qa.get('question'))
    for x in da:
        for y in db:
            if frozenset((x, y)) in CONTRAST_PAIRS:
                return True
    return False

def tail_overlap(qa, qb):
    """Do the two stems end by asking the same thing? The last 3 content
    tokens must share >= 1 token. This separates genuine rewordings
    ('What is the pH of human blood?' / '... value of normal human blood?')
    from same-scenario different sub-questions ('Who sits in the middle?'
    vs 'Who sits immediately to the left of D?') and same-template items
    ('... right to housing?' vs '... rights of consumers?')."""
    def tail(q):
        toks = [t for t in normalise(q.get('question')).split() if t not in STOP]
        return set(toks[-3:])
    ta, tb = tail(qa), tail(qb)
    if not ta or not tb:
        return True
    return bool(ta & tb)

def numbers_compatible(qa, qb):
    """Veto for numeric drills: if BOTH stems carry numbers, the number
    multisets must match AND each number must appear in a matching context
    (same preceding or following token) — so '2 A / 6 ohm' vs '2 ohm / 6 A'
    (same numbers, swapped roles = a different problem) is NOT a duplicate,
    while a genuine rewording ('for 5 years' -> 'in 5 years') still passes.
    One-sided numbers (number in stem vs in options) do not veto."""
    for field in ('question', 'question_ne'):
        oa, ob = number_occurrences(qa.get(field)), number_occurrences(qb.get(field))
        if not oa or not ob:
            continue
        va = sorted(v for v, _, _ in oa)
        vb = sorted(v for v, _, _ in ob)
        if va != vb:
            return False
        # greedy context match, by value
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

def content_tokens(s):
    return tokens(s) - STOP

def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    return inter / len(a | b) if (a | b) else 0.0

def load(exclude_prefixes=()):
    qs = []
    for f in sorted(glob.glob('data/questions/*.json')):
        base = f.split('/')[-1]
        if any(base.startswith(p) for p in exclude_prefixes):
            continue  # parallel writers' files: not part of this sweep
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            print('BROKEN', f, e, file=sys.stderr)
            continue
        for i, q in enumerate(d):
            q['_file'] = f.split('/')[-1]
            q['_idx'] = i
            q['_py'] = q['_file'] == 'previous-year-2083.json' or '-2083-' in q['id']
            q['_r8'] = q['_file'].startswith(('expansion-r8-', 'expansion-r10-'))
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
            qs.append(q)
    return qs

def prefix_candidates(qs, tok_getter, threshold):
    """Exact prefix-filter candidate pairs for Jaccard >= threshold."""
    df = Counter()
    for q in qs:
        for t in tok_getter(q):
            df[t] += 1
    order = {t: i for i, t in enumerate(sorted(df, key=lambda t: (df[t], t)))}
    index = defaultdict(list)
    cand = set()
    for qi, q in enumerate(qs):
        toks = sorted(tok_getter(q), key=lambda t: order[t])
        n = len(toks)
        if n == 0:
            continue
        plen = n - math.ceil(threshold * n) + 1
        plen = max(1, min(n, plen))
        for t in toks[:plen]:
            for oj in index[t]:
                cand.add((min(oj, qi), max(oj, qi)))
            index[t].append(qi)
    return cand

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', default='/tmp/dedupe-report.json')
    ap.add_argument('--exclude', default='',
                    help='comma-separated filename prefixes to skip entirely '
                         '(parallel writers\' files, e.g. expansion-r8-,expansion-r10-)')
    ap.add_argument('--apply', default=None,
                    help='JSON {"remove": [ids...]} — apply removals after human review')
    args = ap.parse_args()

    qs = load([p for p in args.exclude.split(',') if p])
    print(f'Total questions: {len(qs)}', file=sys.stderr)
    by_id = {q['id']: q for q in qs}
    # document frequency of tokens across CORRECT answers (for the rare-token rule)
    correct_df = Counter()
    for q in qs:
        for t in set(numword_norm(q['_correct']).split()):
            correct_df[t] += 1

    # ---- duplicate ids (sanity) ----
    id_counts = Counter(q['id'] for q in qs)
    dup_ids = {i: c for i, c in id_counts.items() if c > 1}
    if dup_ids:
        print(f'DUPLICATE IDS: {dup_ids}', file=sys.stderr)

    pairs = {}  # (i,j) -> dict of metrics

    def note(i, j, **kw):
        key = (min(i, j), max(i, j))
        pairs.setdefault(key, {}).update(kw)

    # ---- (a) exact stems ----
    for field in ('_norm_en', '_norm_ne'):
        groups = defaultdict(list)
        for qi, q in enumerate(qs):
            if q[field]:
                groups[q[field]].append(qi)
        for norm, idxs in groups.items():
            if len(idxs) > 1:
                for a in range(len(idxs)):
                    for b in range(a + 1, len(idxs)):
                        note(idxs[a], idxs[b], exact_field=field)

    # ---- (b) near stems, prefix-filtered, EN and NE ----
    for getter, field in ((lambda q: q['_tok_en'], 'en'), (lambda q: q['_tok_ne'], 'ne')):
        for i, j in prefix_candidates(qs, getter, 0.8):
            s = jaccard(getter(qs[i]), getter(qs[j]))
            if s >= 0.8:
                note(i, j, **{f'jac_{field}': round(s, 3)})

    # ---- (d) candidates: shared 3-option subsets ----
    opt3 = defaultdict(list)
    for qi, q in enumerate(qs):
        opts = sorted(q['_opt_set'])
        if len(opts) == 4:
            for a in range(4):
                key = tuple(opts[:a] + opts[a + 1:])
                opt3[key].append(qi)
    for key, idxs in opt3.items():
        if len(idxs) > 1:
            for a in range(len(idxs)):
                for b in range(a + 1, len(idxs)):
                    note(idxs[a], idxs[b], shared3opts=True)

    # ---- classify (STRICT: stem similarity alone is NOT a duplicate —
    # this bank is full of distinct questions differing by one key word,
    # e.g. primary vs secondary prevention, different dates/numbers) ----
    results = []
    excluded = []  # identical stems, different keys: template stems / key conflicts
    for (i, j), m in sorted(pairs.items()):
        a, b = qs[i], qs[j]
        jac_en = m.get('jac_en', jaccard(a['_tok_en'], b['_tok_en']))
        jac_ne = m.get('jac_ne', jaccard(a['_tok_ne'], b['_tok_ne']))
        exact = 'exact_field' in m
        near = jac_en >= 0.8 or jac_ne >= 0.8
        same_opts = bool(a['_opt_set']) and a['_opt_set'] == b['_opt_set']
        order_differs = same_opts and a['_opt_norm'] != b['_opt_norm']
        opt_jac = jaccard(a['_opt_set'], b['_opt_set'])
        shared_opts = len(a['_opt_set'] & b['_opt_set'])
        same_correct = bool(a['_correct']) and a['_correct'] == b['_correct']
        loose_correct = loose_same_correct(a.get('options', [])[a['answer']] if isinstance(a.get('answer'), int) and 0 <= a['answer'] < len(a.get('options', [])) else '',
                                           b.get('options', [])[b['answer']] if isinstance(b.get('answer'), int) and 0 <= b['answer'] < len(b.get('options', [])) else '',
                                           correct_df)
        cjac = jaccard(a['_ctok_en'], b['_ctok_en'])
        nums_ok = numbers_compatible(a, b)
        tail_ok = tail_overlap(a, b)
        veto = contrast_veto(a, b)
        typ = None
        # S1: identical normalised stem = the same question — EXCEPT when
        # the stem is a generic template whose content lives in the options
        # ('Choose the correct spelling.' for Beautiful vs Necessary,
        # 'Choose the synonym of generous.' with Liberal vs Charitable as
        # the key). So even EN-exact needs the same correct answer.
        # Same-option-set pairs with DIFFERENT correct answers are
        # different questions (computer generations, Class A vs D banks,
        # Ozone vs Environment Day) or a key conflict — never auto-removed.
        exact_en = m.get('exact_field') == '_norm_en'
        exact_ne_only = exact and not exact_en
        if exact and nums_ok and tail_ok and loose_correct and not veto:
            typ = 'exact'
        elif near and same_opts and order_differs and loose_correct and nums_ok and tail_ok and not veto:
            typ = 'same-options-reordered'
        elif near and loose_correct and nums_ok and tail_ok and not veto:
            typ = 'near'
        elif loose_correct and shared_opts >= 3 and cjac >= 0.7 and nums_ok and tail_ok and not veto:
            typ = 'same-fact'
        else:
            # Not a duplicate — but an identical stem with a different key
            # is either a template stem (content lives in the options:
            # spelling/synonym drills) or a key conflict. Record for the
            # audit log; never auto-remove.
            if exact and not loose_correct:
                excluded.append({
                    'a': {'id': a['id'], 'file': a['_file'], 'question': a.get('question'),
                          'options': a.get('options'), 'answer': a.get('answer')},
                    'b': {'id': b['id'], 'file': b['_file'], 'question': b.get('question'),
                          'options': b.get('options'), 'answer': b.get('answer')},
                    'jac_en': round(jac_en, 3), 'jac_ne': round(jac_ne, 3),
                    'exact_field': m.get('exact_field')})
            continue  # distinct question (e.g. one key word differs)
        results.append({
            'type': typ,
            'a': {'id': a['id'], 'file': a['_file'], 'topic': a.get('topic'),
                  'question': a.get('question'), 'options': a.get('options'),
                  'answer': a.get('answer'), 'correct': a['_correct'],
                  'py': a['_py'], 'r8': a['_r8'], 'bilingual': bool(a.get('question_ne') and a.get('options_ne') and a.get('explanation_ne'))},
            'b': {'id': b['id'], 'file': b['_file'], 'topic': b.get('topic'),
                  'question': b.get('question'), 'options': b.get('options'),
                  'answer': b.get('answer'), 'correct': b['_correct'],
                  'py': b['_py'], 'r8': b['_r8'], 'bilingual': bool(b.get('question_ne') and b.get('options_ne') and b.get('explanation_ne'))},
            'jac_en': round(jac_en, 3), 'jac_ne': round(jac_ne, 3),
            'content_jac_en': round(cjac, 3),
            'same_options': same_opts, 'order_differs': order_differs,
            'shared_options': shared_opts, 'same_correct': same_correct,
            'loose_correct': loose_correct,
            'key_differs': exact and not loose_correct,
            'exact_field': m.get('exact_field'),
        })

    # connected components (dup groups) over classified pairs
    parent = list(range(len(qs)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry: parent[rx] = ry
    id2idx = {q['id']: i for i, q in enumerate(qs)}
    for r in results:
        union(id2idx[r['a']['id']], id2idx[r['b']['id']])
    groups = defaultdict(list)
    for r in results:
        groups[find(id2idx[r['a']['id']])].append(r)
    group_list = []
    for root, rs in groups.items():
        ids = sorted({r['a']['id'] for r in rs} | {r['b']['id'] for r in rs})
        group_list.append({'ids': ids, 'pairs': rs})
    group_list.sort(key=lambda g: (len(g['ids']), g['ids']))

    # ---- keeper suggestion per group + removal plan ----
    # PY questions are protected: a PY member is always the keeper, and a
    # non-PY duplicate of a PY question is removed. Within PY, only exact
    # duplicates of each other may be removed (task rule).
    def keeper_score(q):
        bilingual = bool(q.get('question_ne') and q.get('options_ne') and q.get('explanation_ne'))
        return (10000 if q['_py'] else 0) \
            + 100 * bilingual \
            + min(len(q.get('explanation') or ''), 200) \
            + 0.5 * min(len(q.get('explanation_ne') or ''), 200) \
            + 5 * len(q.get('exam') or []) \
            + (20 if not q['_file'].startswith('expansion-') else 0) \
            + min(len(q.get('question') or ''), 60)

    # Greedy STAR clustering (not union-find collapse): a member is removed
    # only if it pairs DIRECTLY with the keeper — a chain A~B~C where A≁C
    # keeps both A and C. This bounds the damage from any residual chaining
    # (e.g. same-option-set families).
    pair_adj = defaultdict(set)  # id -> set of directly-paired ids
    for r in results:
        # R8 files are being written in parallel by other writers: pairs
        # involving an R8 question are DEFERRED (reported, never planned
        # for removal) — this sweep only removes from the pre-R8 bank.
        if r['a'].get('r8') or r['b'].get('r8'):
            continue
        pair_adj[r['a']['id']].add(r['b']['id'])
        pair_adj[r['b']['id']].add(r['a']['id'])

    plan_remove, plan_merge_tags, plan_notes = [], {}, []
    plan_groups = []
    for g in group_list:
        members = [by_id[i] for i in g['ids']]
        py_members = [q for q in members if q['_py']]
        types = {r['type'] for r in g['pairs']}
        if py_members and len(py_members) == len(members):
            # all-PY group: only exact dups may go, keep one
            if types <= {'exact'}:
                keep = max(members, key=lambda q: (keeper_score(q), q['id']))
                removed_here = [q['id'] for q in members if q is not keep]
                plan_remove += removed_here
                plan_notes.append(f"{', '.join(removed_here)}: exact duplicate(s) of PY {keep['id']}")
                plan_groups.append({'ids': g['ids'], 'keeper': keep['id'],
                                    'types': sorted(types), 'removed': removed_here})
            else:
                plan_groups.append({'ids': g['ids'], 'keeper': None,
                                    'types': sorted(types), 'removed': []})
                plan_notes.append(f"GROUP {', '.join(g['ids'])}: all PY, non-exact — KEEP ALL")
            continue
        remaining = sorted(members, key=lambda q: (-keeper_score(q), q['id']))
        removed_here = []
        keepers_here = []
        while remaining:
            keep = remaining.pop(0)
            keepers_here.append(keep['id'])
            direct = [q for q in remaining if q['id'] in pair_adj.get(keep['id'], set())]
            direct_removed = []
            for q in direct:
                if q['_py']:
                    continue  # a non-PY keeper never removes a PY question
                removed_here.append(q['id'])
                direct_removed.append(q['id'])
                remaining.remove(q)
            extra_tags = sorted({t for q in members if q['id'] in direct_removed for t in (q.get('exam') or [])} - set(keep.get('exam') or []))
            if extra_tags:
                plan_merge_tags[keep['id']] = sorted(set(plan_merge_tags.get(keep['id'], [])) | set(extra_tags))
        plan_remove += removed_here
        plan_groups.append({'ids': g['ids'], 'keeper': keepers_here,
                            'types': sorted(types), 'removed': removed_here})
    plan = {'remove': sorted(set(plan_remove)), 'merge_tags': plan_merge_tags,
            'notes': plan_notes,
            'groups': plan_groups}
    plan_path = args.report.replace('.json', '-plan.json')
    with open(plan_path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    print(f'Suggested removals: {len(plan_remove)} (keepers keep exam-tag union: {len(plan_merge_tags)} keepers gain tags)')
    print(f'Plan written to {plan_path}', file=sys.stderr)

    by_type = Counter(r['type'] for r in results)
    print(f'Candidate pairs examined: {len(pairs)}')
    print(f'Classified duplicate pairs: {len(results)}  by type: {dict(by_type)}')
    print(f'Duplicate groups (connected components): {len(group_list)}')
    print(f'Questions involved: {len({i for g in group_list for i in g["ids"]})}')
    if dup_ids:
        print(f'DUPLICATE IDS: {dup_ids}')
    for g in group_list:
        types = sorted({r['type'] for r in g['pairs']})
        print(f"  GROUP {', '.join(g['ids'])}  [{', '.join(types)}]")
        for r in g['pairs']:
            print(f"    {r['type']}: {r['a']['id']} ({r['a']['file']}) vs {r['b']['id']} ({r['b']['file']}) "
                  f"jac_en={r['jac_en']} jac_ne={r['jac_ne']} cjac={r['content_jac_en']} "
                  f"same_opts={r['same_options']} order_diff={r['order_differs']} same_correct={r['same_correct']}")
            print(f"      A: {r['a']['question']}")
            print(f"      B: {r['b']['question']}")

    report = {'total': len(qs), 'by_type': dict(by_type),
              'duplicate_ids': dup_ids, 'pairs': results, 'groups': group_list,
              'excluded_identical_stem_different_key': excluded,
              'deferred_r8_pairs': [r for r in results if r['a'].get('r8') or r['b'].get('r8')],
              'r8_total': sum(1 for q in qs if q['_r8'])}
    print(f"R8 questions present (parallel writers, untouched): {sum(1 for q in qs if q['_r8'])}; "
          f"R8-involved duplicate pairs deferred: {len(report['deferred_r8_pairs'])}")
    print(f'Excluded identical-stem/different-key pairs (template stems or key conflicts, kept): {len(excluded)}')
    with open(args.report, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f'Report written to {args.report}', file=sys.stderr)

    if args.apply:
        plan = json.load(open(args.apply, encoding='utf-8'))
        remove = set(plan.get('remove', []))
        merge_tags = plan.get('merge_tags', {})
        removed, missing = [], []
        for f in sorted(glob.glob('data/questions/*.json')):
            if f.split('/')[-1].startswith(('expansion-r8-', 'expansion-r10-')):
                continue  # parallel writers' files: never touch
            d = json.load(open(f, encoding='utf-8'))
            keep = [q for q in d if q['id'] not in remove]
            for q in keep:
                if q['id'] in merge_tags:
                    ex = list(q.get('exam') or [])
                    for t in merge_tags[q['id']]:
                        if t not in ex:
                            ex.append(t)
                    q['exam'] = ex
                    print(f"  {q['id']}: exam tags += {merge_tags[q['id']]}")
            n = len(d) - len(keep)
            if n or any(q['id'] in merge_tags for q in keep):
                removed += [q['id'] for q in d if q['id'] in remove]
                # match repo format: indent=2, NO trailing newline
                json.dump(keep, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
                print(f'{f}: removed {n}')
        missing = sorted(remove - set(removed))
        print(f'Removed {len(removed)}: {removed}')
        if missing:
            print(f'NOT FOUND (check ids): {missing}', file=sys.stderr)

if __name__ == '__main__':
    main()
