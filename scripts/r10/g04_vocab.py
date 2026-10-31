#!/usr/bin/env python3
"""R10 generator 4: English vocabulary (~1,900 from the curated word list).
Per word: synonym x2 framings, antonym x2 framings, meaning (EN->NE),
reverse meaning (NE->EN). Distractors for meaning questions come from the
global pool so Nepali glosses never collide."""
import sys, random
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num
from vocab_data import WORDS

bank = Bank()
em = Emitter(bank, 'R10-ENG')
rng = random.Random(33004)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'tsc-primary', 'tsc-secondary', 'foreign-service']

# validate rows: the 4 EN option words AND their NE glosses must be distinct
# (syn-set and ant-set separately), else the question is unusable
valid = []
for w in WORDS:
    en, ne, syn, syn_ne, ant, ant_ne, rel, rel_ne, unrel, unrel_ne = w
    ok_en = len({syn.lower(), ant.lower(), rel.lower(), unrel.lower()}) == 4
    ok_ne = len({syn_ne, ant_ne, rel_ne, unrel_ne}) == 4
    if ok_en and ok_ne:
        valid.append(w)
    else:
        print('SKIP row (dup option words/glosses):', en, file=sys.stderr)
print(f'Valid words: {len(valid)}/{len(WORDS)}', file=sys.stderr)

pool_ne = [(w[0], w[1]) for w in valid]  # (en, ne) for fallback distractors

def rand_ne_distractors(correct_ne, k=3):
    cands = [ne for (en2, ne) in pool_ne if ne != correct_ne]
    rng.shuffle(cands)
    out = []
    for c in cands:
        if c not in out:
            out.append(c)
        if len(out) == k:
            break
    return out

def rand_en_distractors(correct_en, k=3):
    cands = [(en2, ne) for (en2, ne) in pool_ne if en2 != correct_en]
    rng.shuffle(cands)
    out = []
    for p in cands:
        if p[0] not in [x[0] for x in out]:
            out.append(p)
        if len(out) == k:
            break
    return out

for w in valid:
    en, ne, syn, syn_ne, ant, ant_ne, rel, rel_ne, unrel, unrel_ne = w
    cap = en.capitalize()
    # ---- 1. synonym framing A
    em.emit(EX, 'English', 'Vocabulary', 'easy', 1,
            f'Choose the synonym of {en}.',
            f'‘{en}’ शब्दको पर्यायवाची (synonym) छान्नुहोस्।',
            [syn.capitalize(), ant.capitalize(), rel.capitalize(), unrel.capitalize()],
            [syn_ne, ant_ne, rel_ne, unrel_ne], 0,
            f"'{en}' means the same as '{syn}'.",
            f'‘{en}’ को अर्थ ‘{syn}’ हो।')
    # ---- 2. synonym framing B
    em.emit(EX, 'English', 'Vocabulary', 'medium', 1,
            f'Which word is closest in meaning to {en}?',
            f'‘{en}’ को अर्थसँग सबैभन्दा नजिकको शब्द कुन हो?',
            [syn.capitalize(), ant.capitalize(), rel.capitalize(), unrel.capitalize()],
            [syn_ne, ant_ne, rel_ne, unrel_ne], 0,
            f"Of the options, '{syn}' is closest in meaning to '{en}'.",
            f'विकल्पहरूमध्ये ‘{syn}’ को अर्थ ‘{en}’ सँग सबैभन्दा नजिक छ।')
    # ---- 3. antonym framing A
    em.emit(EX, 'English', 'Vocabulary', 'easy', 1,
            f'Choose the antonym of {en}.',
            f'‘{en}’ शब्दको विलोम (antonym) छान्नुहोस्।',
            [ant.capitalize(), syn.capitalize(), rel.capitalize(), unrel.capitalize()],
            [ant_ne, syn_ne, rel_ne, unrel_ne], 0,
            f"The opposite of '{en}' is '{ant}'.",
            f'‘{en}’ को विलोम ‘{ant}’ हो।')
    # ---- 4. antonym framing B
    em.emit(EX, 'English', 'Vocabulary', 'medium', 1,
            f'Which word is opposite in meaning to {en}?',
            f'‘{en}’ को अर्थको विपरीत शब्द कुन हो?',
            [ant.capitalize(), syn.capitalize(), rel.capitalize(), unrel.capitalize()],
            [ant_ne, syn_ne, rel_ne, unrel_ne], 0,
            f"Of the options, '{ant}' is opposite in meaning to '{en}'.",
            f'विकल्पहरूमध्ये ‘{ant}’ को अर्थ ‘{en}’ को विपरीत छ।')
    # ---- 5. meaning EN -> NE
    ds = rand_ne_distractors(ne, 3)
    em.emit(EX, 'English', 'Vocabulary', 'medium', 2,
            f"What does '{en}' mean?",
            f'‘{en}’ को अर्थ के हो?',
            [ne] + ds, [ne] + ds, 0,
            f"'{en}' means '{ne}' in Nepali.",
            f'‘{en}’ को नेपाली अर्थ ‘{ne}’ हो।')
    # ---- 6. reverse meaning NE -> EN
    ds = rand_en_distractors(en, 3)
    opts_en = [en] + [d[0] for d in ds]
    opts_ne = [ne] + [d[1] for d in ds]
    em.emit(EX, 'English', 'Vocabulary', 'hard', 2,
            f"Which English word means '{ne}'?",
            f'‘{ne}’ भन्ने अर्थ भएको अङ्ग्रेजी शब्द कुन हो?',
            opts_en, opts_ne, 0,
            f"'{en}' means '{ne}'.",
            f'‘{en}’ को अर्थ ‘{ne}’ हो।')

n = em.write('expansion-r10-english.json')
print('ENG TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:10]:
    print('  REJ', r)
