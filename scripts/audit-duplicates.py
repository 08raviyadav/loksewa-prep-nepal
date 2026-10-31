#!/usr/bin/env python3
"""Audit + clean duplicates in the Lok Sewa Prep Nepal question bank.

Detects, across all data/questions/*.json:
  (a) exact duplicates    — normalised question text identical (EN or NE)
  (b) near-duplicates     — token-Jaccard >= 0.8 on the normalised stem (EN or NE)
  (c) same stem, options in a different order — (a)/(b) stem + identical
      option set but different option order
  (d) same fact asked two ways — content-token Jaccard >= 0.7 AND the
      same correct answer (loosely) AND >= 3 of 4 options shared

Plus a test-level category:
  (e) exact-text — the question text is identical after ONLY trim +
      lowercase, exactly as scripts/test-questions.js defines it. The
      test does NOT strip punctuation, so 'Choose the correct spelling.'
      vs 'Choose the correct spelling:' is NOT a test failure (and the
      two are different template drills anyway — content lives in the
      options). Only raw-identical stems are planned for removal.

Confident bar for the near families (learned 2026-10-27): 'near' and
'same-options-reordered' are only planned when BOTH jac_en >= 0.9 AND
content-Jaccard >= 0.9. Weaker matches are overwhelmingly false
positives in this bank: NE-Jaccard >= 0.8 fires on template drills whose
Nepali translations differ by one word ('January' vs 'May', 'assemble'
vs 'accumulate', letter-sum words NEPAL vs BRAVE), and the option-pool
generator reuses identical 4-option sets (and identical answers by
coincidence) across different problems. 'same-fact' pairs are reported
only, never planned — the same option-pool effect makes them unreliable
without human review.
Template-list families (odd-one-out, LCM, commutative drills) additionally
need DIRECT set-grouping: numbers_compatible's neighbour-context check
misses same-set copies listed in very different orders — see the
Round-10 dedupe notes in data/SELF-AUDIT-2026-10-26.md.

Precision guards are adapted from scripts/dedupe-check.py (same bank,
same lessons — stem similarity alone is NOT a duplicate signal here: the
bank is full of same-template drills differing by one key word, and of
same-scenario IQ sub-questions):
  * loose_same_correct is strict: same numeric value alone does NOT count,
    near-identical strings do NOT count ('25 years' vs '35 years').
  * numbers_compatible: if both stems carry numbers, the multisets must
    match and each number must share a neighbouring token.
  * tail_overlap: the last 3 content tokens of the stems must share one.
  * contrast_veto: a swapped contrast pair (men/women, primary/secondary,
    largest/smallest, ...) means a different question.
  * Greedy star clustering: a member is removed only if it pairs DIRECTLY
    with its keeper, never via a chain.

Usage:
  python3 scripts/audit-duplicates.py [--report PATH] [--plan PATH]
  python3 scripts/audit-duplicates.py --apply PLAN_JSON
      [--clean-files expansion-r10-english4.json,expansion-r10-maths8.json]

  Without --apply this only reports and writes a removal plan.
  --clean-files lists the files whose members are preferred for removal
  when a duplicate group spans files (the files being cleaned in this
  round); keepers are otherwise chosen by quality score.
  --apply removes the plan's ids and unions the removed questions' exam
  tags onto their keepers. JSON is written indent=2, no trailing newline
  (repo format).

Previous-Year questions (previous-year-2083.json) are protected: a PY
member is always the keeper and a non-PY duplicate of a PY question is
removed; within PY only exact duplicates may be removed.
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
    da = qa['_ctok_en'] - qb['_ctok_en']
    db = qb['_ctok_en'] - qa['_ctok_en']
    for x in da:
        for y in db:
            if frozenset((x, y)) in CONTRAST_PAIRS:
                return True
    return False


def tail_overlap(qa, qb):
    ta, tb = qa['_tail_en'], qb['_tail_en']
    if not ta or not tb:
        return True
    return bool(ta & tb)


def numbers_compatible(qa, qb):
    for fa, fb in (('_nums_en', '_nums_en'), ('_nums_ne', '_nums_ne')):
        oa, ob = qa[fa], qb[fb]
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


def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    return inter / len(a | b) if (a | b) else 0.0


def load():
    qs = []
    for f in sorted(glob.glob('data/questions/*.json')):
        base = os.path.basename(f)
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            print('BROKEN', f, e, file=sys.stderr)
            continue
        for i, q in enumerate(d):
            q['_file'] = base
            q['_idx'] = i
            q['_py'] = base == 'previous-year-2083.json' or '-2083-' in q['id']
            q['_norm_en'] = normalise(q.get('question'))
            q['_norm_ne'] = normalise(q.get('question_ne'))
            # Raw stem exactly as test-questions.js compares it:
            # trim + lowercase only, punctuation kept.
            q['_raw_en'] = (q.get('question') or '').strip().lower()
            q['_tok_en'] = tokens(q.get('question'))
            q['_tok_ne'] = tokens(q.get('question_ne'))
            q['_ctok_en'] = content_tokens(q.get('question'))
            q['_tail_en'] = set([t for t in normalise(q.get('question')).split()
                                 if t not in STOP][-3:])
            q['_nums_en'] = number_occurrences(q.get('question'))
            q['_nums_ne'] = number_occurrences(q.get('question_ne'))
            opts = q.get('options') or []
            q['_opt_norm'] = [normalise(o) for o in opts]
            q['_opt_set'] = frozenset(q['_opt_norm'])
            ans = q.get('answer')
            q['_correct'] = q['_opt_norm'][ans] if isinstance(ans, int) and 0 <= ans < len(q['_opt_norm']) else ''
            q['_correct_raw'] = opts[ans] if isinstance(ans, int) and 0 <= ans < len(opts) else ''
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
        plen = max(1, min(n, n - math.ceil(threshold * n) + 1))
        for t in toks[:plen]:
            for oj in index[t]:
                cand.add((min(oj, qi), max(oj, qi)))
            index[t].append(qi)
    return cand


def keeper_score(q):
    bilingual = bool(q.get('question_ne') and q.get('options_ne') and q.get('explanation_ne'))
    return (10000 if q['_py'] else 0) \
        + 100 * bilingual \
        + min(len(q.get('explanation') or ''), 200) \
        + 0.5 * min(len(q.get('explanation_ne') or ''), 200) \
        + 5 * len(q.get('exam') or []) \
        + (20 if not q['_file'].startswith('expansion-') else 0) \
        + min(len(q.get('question') or ''), 60)


def audit(qs):
    by_id = {q['id']: q for q in qs}
    id_counts = Counter(q['id'] for q in qs)
    dup_ids = {i: c for i, c in id_counts.items() if c > 1}

    pairs = {}

    def note(i, j, **kw):
        key = (min(i, j), max(i, j))
        pairs.setdefault(key, {}).update(kw)

    # (a) exact stems, EN and NE
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

    # (b) near stems, prefix-filtered, EN and NE
    for getter, field in ((lambda q: q['_tok_en'], 'en'), (lambda q: q['_tok_ne'], 'ne')):
        for i, j in prefix_candidates(qs, getter, 0.8):
            s = jaccard(getter(qs[i]), getter(qs[j]))
            if s >= 0.8:
                note(i, j, **{f'jac_{field}': round(s, 3)})

    # (d) candidates: shared 3-option subsets
    opt3 = defaultdict(list)
    for qi, q in enumerate(qs):
        opts = sorted(q['_opt_set'])
        if len(opts) == 4:
            for a in range(4):
                opt3[tuple(opts[:a] + opts[a + 1:])].append(qi)
    for key, idxs in opt3.items():
        if len(idxs) > 1:
            for a in range(len(idxs)):
                for b in range(a + 1, len(idxs)):
                    note(idxs[a], idxs[b], shared3opts=True)

    results, excluded, exact_text_only = [], [], []
    for (i, j), m in sorted(pairs.items()):
        a, b = qs[i], qs[j]
        exact = 'exact_field' in m
        near = False
        if 'jac_en' in m or 'jac_ne' in m:
            near = (m.get('jac_en', 0) >= 0.8 or m.get('jac_ne', 0) >= 0.8)
        same_opts = bool(a['_opt_set']) and a['_opt_set'] == b['_opt_set']
        order_differs = same_opts and a['_opt_norm'] != b['_opt_norm']
        shared_opts = len(a['_opt_set'] & b['_opt_set'])
        same_correct = bool(a['_correct']) and a['_correct'] == b['_correct']
        cjac = jaccard(a['_ctok_en'], b['_ctok_en'])
        # Cheap-first: only compute the expensive guards / loose-correct
        # check when a type is actually reachable for this pair.
        exact_en = m.get('exact_field') == '_norm_en'
        loose_correct = None

        def guards_ok():
            return numbers_compatible(a, b) and tail_overlap(a, b) and not contrast_veto(a, b)

        def loose_ok():
            nonlocal loose_correct
            if loose_correct is None:
                loose_correct = loose_same_correct(a['_correct_raw'], b['_correct_raw'])
            return loose_correct

        typ = None
        if exact and loose_ok() and guards_ok():
            typ = 'exact'
        elif near or (shared_opts >= 3 and cjac >= 0.7):
            jac_en = m['jac_en'] if 'jac_en' in m else jaccard(a['_tok_en'], b['_tok_en'])
            jac_ne = m['jac_ne'] if 'jac_ne' in m else jaccard(a['_tok_ne'], b['_tok_ne'])
            near = jac_en >= 0.8 or jac_ne >= 0.8
            # Confident bar (see module docstring): NE-near alone and
            # sub-0.9 content overlap are false-positive territory here.
            confident = jac_en >= 0.9 and cjac >= 0.9
            if confident and near and same_opts and order_differs and loose_ok() and guards_ok():
                typ = 'same-options-reordered'
            elif confident and near and loose_ok() and guards_ok():
                typ = 'near'
            elif loose_ok() and shared_opts >= 3 and cjac >= 0.7 and guards_ok():
                typ = 'same-fact'
        jac_en = m['jac_en'] if 'jac_en' in m else jaccard(a['_tok_en'], b['_tok_en'])
        jac_ne = m['jac_ne'] if 'jac_ne' in m else jaccard(a['_tok_ne'], b['_tok_ne'])
        # Only build the (large) record when this pair is actually kept.
        keep_rec = bool(typ) or (exact_en and typ != 'exact') or (exact and not loose_correct)
        if not keep_rec:
            continue
        rec = {
            'a': {'id': a['id'], 'file': a['_file'], 'topic': a.get('topic'),
                  'question': a.get('question'), 'options': a.get('options'),
                  'answer': a.get('answer'), 'correct': a['_correct'],
                  'py': a['_py'],
                  'bilingual': bool(a.get('question_ne') and a.get('options_ne') and a.get('explanation_ne'))},
            'b': {'id': b['id'], 'file': b['_file'], 'topic': b.get('topic'),
                  'question': b.get('question'), 'options': b.get('options'),
                  'answer': b.get('answer'), 'correct': b['_correct'],
                  'py': b['_py'],
                  'bilingual': bool(b.get('question_ne') and b.get('options_ne') and b.get('explanation_ne'))},
            'jac_en': round(jac_en, 3), 'jac_ne': round(jac_ne, 3),
            'content_jac_en': round(cjac, 3),
            'same_options': same_opts, 'order_differs': order_differs,
            'shared_options': shared_opts, 'same_correct': same_correct,
            'loose_correct': bool(loose_correct),
            'exact_field': m.get('exact_field'),
        }
        if typ:
            rec['type'] = typ
            results.append(rec)
        # Test-level: raw-identical EN stem (trim + lowercase only, as the
        # test defines it) regardless of keys — the test flags it, so it
        # must be removed/rewritten even when the two copies are both
        # valid (e.g. two valid translations of one Nepali word).
        if exact_en and a['_raw_en'] and a['_raw_en'] == b['_raw_en'] and not (typ == 'exact'):
            r2 = dict(rec)
            r2['type'] = 'exact-text'
            exact_text_only.append(r2)
        elif exact and not loose_correct:
            excluded.append(rec)
    return results, exact_text_only, excluded, dup_ids, by_id


def build_plan(results, exact_text_only, by_id, clean_files):
    """Star-clustering removal plan over semantic dups + exact-text pairs.
    'same-fact' pairs are report-only, never planned (option-pool effect)."""
    planned = [r for r in results if r['type'] != 'same-fact']
    report_only = [r for r in results if r['type'] == 'same-fact']
    all_pairs = planned + exact_text_only
    pair_adj = defaultdict(set)
    for r in all_pairs:
        pair_adj[r['a']['id']].add(r['b']['id'])
        pair_adj[r['b']['id']].add(r['a']['id'])
    parent = {i: i for i in by_id}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for r in all_pairs:
        union(r['a']['id'], r['b']['id'])
    groups = defaultdict(list)
    for r in all_pairs:
        groups[find(r['a']['id'])].append(r)
    group_list = []
    for root, rs in groups.items():
        ids = sorted({r['a']['id'] for r in rs} | {r['b']['id'] for r in rs})
        group_list.append({'ids': ids, 'pairs': rs})
    group_list.sort(key=lambda g: (len(g['ids']), g['ids']))

    def sort_key(q):
        # clean-file members sort AFTER non-clean members, so the keeper is
        # picked outside the files being cleaned when possible
        return (-keeper_score(q), 1 if q['_file'] in clean_files else 0, q['id'])

    plan_remove, plan_merge_tags, plan_groups, notes = [], {}, [], []
    for g in group_list:
        members = [by_id[i] for i in g['ids']]
        py_members = [q for q in members if q['_py']]
        types = sorted({r['type'] for r in g['pairs']})
        if py_members and len(py_members) == len(members):
            if set(types) <= {'exact'}:
                keep = max(members, key=lambda q: (keeper_score(q), q['id']))
                removed_here = [q['id'] for q in members if q is not keep]
                plan_remove += removed_here
                notes.append(f"{', '.join(removed_here)}: exact duplicate(s) of PY {keep['id']}")
                plan_groups.append({'ids': g['ids'], 'keeper': [keep['id']],
                                    'types': types, 'removed': removed_here})
            else:
                plan_groups.append({'ids': g['ids'], 'keeper': [], 'types': types, 'removed': []})
                notes.append(f"GROUP {', '.join(g['ids'])}: all PY, non-exact — KEEP ALL")
            continue
        remaining = sorted(members, key=sort_key)
        removed_here, keepers_here = [], []
        while remaining:
            keep = remaining.pop(0)
            keepers_here.append(keep['id'])
            direct = [q for q in remaining if q['id'] in pair_adj.get(keep['id'], set())]
            direct_removed = []
            for q in direct:
                if q['_py']:
                    continue
                removed_here.append(q['id'])
                direct_removed.append(q['id'])
                remaining.remove(q)
            extra = sorted({t for q in members if q['id'] in direct_removed
                            for t in (q.get('exam') or [])} - set(keep.get('exam') or []))
            if extra:
                plan_merge_tags[keep['id']] = sorted(set(plan_merge_tags.get(keep['id'], [])) | set(extra))
        plan_remove += removed_here
        plan_groups.append({'ids': g['ids'], 'keeper': keepers_here,
                            'types': types, 'removed': removed_here})
    return {'remove': sorted(set(plan_remove)), 'merge_tags': plan_merge_tags,
            'notes': notes, 'groups': plan_groups,
            'report_only_same_fact': [{'a': r['a']['id'], 'b': r['b']['id'],
                                        'a_file': r['a']['file'], 'b_file': r['b']['file'],
                                        'question_a': r['a']['question'],
                                        'question_b': r['b']['question']}
                                       for r in report_only]}


def apply_plan(plan):
    remove = set(plan.get('remove', []))
    merge_tags = plan.get('merge_tags', {})
    removed, missing = [], []
    for f in sorted(glob.glob('data/questions/*.json')):
        d = json.load(open(f, encoding='utf-8'))
        keep = [q for q in d if q['id'] not in remove]
        changed = False
        for q in keep:
            if q['id'] in merge_tags:
                ex = list(q.get('exam') or [])
                for t in merge_tags[q['id']]:
                    if t not in ex:
                        ex.append(t)
                if ex != q.get('exam'):
                    q['exam'] = ex
                    changed = True
                    print(f"  {q['id']}: exam tags += {merge_tags[q['id']]}")
        n = len(d) - len(keep)
        if n or changed:
            removed += [q['id'] for q in d if q['id'] in remove]
            json.dump(keep, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
            print(f'{f}: removed {n}')
    missing = sorted(remove - set(removed))
    print(f'Removed {len(removed)}')
    if missing:
        print(f'NOT FOUND (check ids): {missing}', file=sys.stderr)
    return removed, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', default='/tmp/audit-duplicates-report.json')
    ap.add_argument('--plan', default=None)
    ap.add_argument('--apply', default=None, help='plan JSON to apply')
    ap.add_argument('--clean-files', default='',
                    help='comma-separated filenames whose members are preferred for removal')
    args = ap.parse_args()

    if args.apply:
        plan = json.load(open(args.apply, encoding='utf-8'))
        apply_plan(plan)
        return

    qs = load()
    print(f'Total questions: {len(qs)}', file=sys.stderr)
    results, exact_text_only, excluded, dup_ids, by_id = audit(qs)
    clean_files = {p for p in args.clean_files.split(',') if p}
    plan = build_plan(results, exact_text_only, by_id, clean_files)
    by_type = Counter(r['type'] for r in results)
    print(f'Candidate duplicate pairs classified: {len(results)} by type: {dict(by_type)}')
    print(f'Exact-text-only pairs (test-level, keys differ): {len(exact_text_only)}')
    print(f'Excluded identical-stem/different-key pairs (kept): {len(excluded)}')
    print(f'Duplicate groups: {len(plan["groups"])}')
    print(f'Planned removals: {len(plan["remove"])} '
          f'(keepers gain exam tags: {len(plan["merge_tags"])}; '
          f'same-fact report-only: {len(plan["report_only_same_fact"])})')
    if dup_ids:
        print(f'DUPLICATE IDS: {dup_ids}')
    for g in plan['groups']:
        print(f"  GROUP {', '.join(g['ids'])} [{', '.join(g['types'])}] "
              f"keeper={g['keeper']} removed={g['removed']}")
    report = {'total': len(qs), 'by_type': dict(by_type),
              'duplicate_ids': dup_ids, 'pairs': results,
              'exact_text_only': exact_text_only,
              'excluded_identical_stem_different_key': excluded,
              'groups': plan['groups'], 'plan': plan}
    with open(args.report, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f'Report written to {args.report}', file=sys.stderr)
    plan_path = args.plan or args.report.replace('.json', '-plan.json')
    with open(plan_path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    print(f'Plan written to {plan_path}', file=sys.stderr)


if __name__ == '__main__':
    main()
