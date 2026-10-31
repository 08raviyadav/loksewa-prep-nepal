#!/usr/bin/env python3
"""High-confidence mismatch audit.
Flag only if the explanation's CONCLUDED value (last '= Rs? NUM' in the
explanation, or 'answer/is NUM' in the final sentence) equals a DIFFERENT
option than the marked one, and the marked option's value does NOT appear
as a concluded value in the final sentence.
Also flag explicit 'Option X is correct / answer is X' letter mismatches.
"""
import json, glob, re, sys

DEV = str.maketrans('०१२३४५६७८९', '0123456789')
def denum(s): return s.translate(DEV)
def parse_num(tok):
    tok = tok.replace(',', '').strip().rstrip('%')
    try: return float(tok) if '.' in tok else int(tok)
    except ValueError: return None

NUM = r'-?\d[\d,]*\.?\d*'
EQ_RE = re.compile(r'=\s*(?:Rs\.?|र[\u0941\u0942]\.?)?\s*(' + NUM + r')\s*(%|kg|cm|mm|m|km|years?|days?|hours?|minutes?)?', re.I)

def numeric_value(opt):
    s = denum(opt).strip()
    s2 = re.sub(r'^(Rs\.?|US\$|\$)\s*', '', s)
    s2 = re.sub(r'\s*(kg|km|m|cm|%|years?|days?|months?|hours?|minutes?|seconds?|MW|litres?|liters?|rupees?)$', '', s2, flags=re.I)
    s2 = s2.strip().rstrip('.')
    if re.fullmatch(r'-?\d[\d,]*\.?\d*', s2): return parse_num(s2)
    return None

def concluded_values(text):
    """Numbers that appear as results: after '=' or after is/are in final sentence."""
    t = denum(text)
    vals = []
    for m in EQ_RE.finditer(t):
        v = parse_num(m.group(1))
        if v is not None: vals.append(v)
    return vals

qs = []
for f in sorted(glob.glob('data/questions/*.json')):
    try: d = json.load(open(f))
    except Exception as e: print('BROKEN', f, e, file=sys.stderr); continue
    for q in d:
        q['_file'] = f.split('/')[-1]; qs.append(q)

print(f'Total: {len(qs)}', file=sys.stderr)
flagged = []
for q in qs:
    opts = q.get('options') or []
    ans = q.get('answer')
    if ans is None or not (0 <= ans < len(opts)):
        flagged.append({'id': q['id'], 'file': q['_file'], 'topic': q.get('topic'), 'reasons': ['BAD_ANSWER_INDEX'], 'question': q.get('question'), 'options': opts, 'answer': ans, 'explanation': q.get('explanation'), 'explanation_ne': q.get('explanation_ne')})
        continue
    marked_num = numeric_value(opts[ans])
    expl = q.get('explanation') or ''
    expl_ne = q.get('explanation_ne') or ''
    reasons = []
    # explicit option letter
    m = re.search(r'(?:correct answer is|answer is|answer:)\s*(?:option\s*)?\(?([A-D])\)?', expl, re.I) or \
        re.search(r'option\s+([A-D])\s+is\s+correct', expl, re.I)
    if m and ord(m.group(1).upper()) - 65 != ans:
        reasons.append(f"EXPL_NAMES_OPTION_{m.group(1).upper()}_BUT_KEY_IS_{chr(65+ans)}")
    # numeric conclusion
    if marked_num is not None:
        opt_nums = [numeric_value(o) for o in opts]
        # last '=' value in EN and NE
        for src, text in (('EN', expl), ('NE', expl_ne)):
            vals = concluded_values(text)
            if not vals: continue
            last = vals[-1]
            if last != marked_num and last in opt_nums:
                # check final sentence does not also conclude marked
                sents = re.split(r'(?<=[.!])\s+', text.strip())
                final = sents[-1] if sents else ''
                fvals = concluded_values(final)
                # also numbers after 'is/are' in final sentence
                for mm in re.finditer(r'(?:is|are|was|were)\s+(?:Rs\.?|रू\.?\s*)?(' + NUM + r')', denum(final), re.I):
                    v = parse_num(mm.group(1))
                    if v is not None: fvals.append(v)
                if marked_num not in fvals:
                    reasons.append(f"{src}_CONCLUDES_{last}_!=_MARKED_{marked_num} (matches option {chr(65+opt_nums.index(last))})")
                    break
        # 'answer is X' at very end
        m2 = re.search(r'(?:answer is|correct answer is)\s*(?:Rs\.?|रू\.?\s*)?(' + NUM + r')', denum(expl), re.I)
        if m2:
            v = parse_num(m2.group(1))
            if v is not None and v != marked_num and v in opt_nums:
                reasons.append(f"END_ANSWER_{v}_!=_MARKED_{marked_num}")
    if reasons:
        flagged.append({'id': q['id'], 'file': q['_file'], 'topic': q.get('topic'), 'subtopic': q.get('subtopic'),
                        'question': q.get('question'), 'options': opts, 'answer': ans,
                        'marked': opts[ans], 'explanation': expl, 'explanation_ne': expl_ne, 'reasons': reasons})

print(f'Flagged: {len(flagged)}', file=sys.stderr)
with open('/tmp/flags2.json', 'w') as f: json.dump(flagged, f, indent=2, ensure_ascii=False)
for fl in flagged:
    print(fl['id'], '|', fl['file'], '|', fl['topic'], '|', '; '.join(fl['reasons']))
    print('   Q:', fl['question'])
    print('   opts:', fl['options'], 'ans:', fl['answer'], 'marked:', fl.get('marked'))
    print('   expl:', fl['explanation'][:300])
