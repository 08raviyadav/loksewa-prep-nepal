#!/usr/bin/env python3
"""R10 generator 20: more IQ 3 (~3,000). Letter series 2-step patterns,
coding (reverse+shift), blood relations with names, direction with turns,
ranking variants, odd-one-out numbers (new sets), analogy pairs (new),
alphabet A=1 sums with new words, number-letter codes, letter pairs."""
import sys, random, math
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num, fmt

def ord_s(n):
    """English ordinal suffix: 1st, 2nd, 3rd, 4th, 11th, 21st, 22nd, 23rd..."""
    n = int(n)
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


bank = Bank()
em = Emitter(bank, 'R10-IQ3')
rng = random.Random(71112)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'police', 'army', 'tsc-primary', 'tsc-secondary']
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHA_NE = ['ए','बी','सी','डी','ई','एफ','जी','एच','आई','जे','के','एल','एम','एन','ओ','पी','क्यू','आर','एस','टी','यू','भी','डब्ल्यू','एक्स','वाई','जेड']

def opts4(correct, cands):
    out = [correct]
    for c in cands:
        if len(out) == 4: break
        if c not in out: out.append(c)
    d = 1
    while len(out) < 4:
        for c in (correct + d, correct - d, correct + 10*d, correct - 10*d):
            if c not in out and c > 0:
                out.append(c); break
        d += 1
    return out

def num_opts(correct, cands):
    o = opts4(correct, cands)
    return [fmt(x) for x in o], [dev_num(x) for x in o], 0

def letter_opts(correct):
    ds = [c for c in ALPHA if c != correct]
    rng.shuffle(ds)
    o = [correct] + ds[:3]
    on = [ALPHA_NE[ALPHA.index(c)] for c in o]
    return o, on

def E(sub, diff, q, qn, o, on, expl, expln, idx=0):
    em.emit(EX, 'IQ & Reasoning', sub, diff, 2, q, qn, o, on, idx, expl, expln)

# ---------- letter series: alternating two patterns ----------
for start in range(0, 15):
    s1, s2 = rng.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)])
    seq = [ALPHA[start]]
    for i in range(3):
        step = s1 if i % 2 == 0 else s2
        seq.append(ALPHA[(ALPHA.index(seq[-1]) + step) % 26])
    nxt = ALPHA[(ALPHA.index(seq[-1]) + (s1 if 3 % 2 == 0 else s2)) % 26]
    s = ', '.join(seq)
    o, on = letter_opts(nxt)
    E('Letter Series', 'hard', f'What is the next letter in the series: {s}, ...?',
      f'श्रेणी {s}, ... मा अर्को अक्षर कुन हो?', o, on,
      f'The steps alternate +{s1}, +{s2}, so the next letter is {nxt}.',
      f'चरणहरू +{dev(s1)}, +{dev(s2)} पालैपालो आउँछन्, त्यसैले अर्को अक्षर {nxt} हो।')

# ---------- letter series: vowel series ----------
VOWELS = ['A', 'E', 'I', 'O', 'U']
for start in range(0, 5):
    seq = [VOWELS[(start+i) % 5] for i in range(4)]
    nxt = VOWELS[(start+4) % 5]
    s = ', '.join(seq)
    o, on = letter_opts(nxt)
    E('Letter Series', 'medium', f'What is the next letter in the series: {s}, ...?',
      f'श्रेणी {s}, ... मा अर्को अक्षर कुन हो?', o, on,
      f'The vowels repeat in order, so the next letter is {nxt}.',
      f'स्वरहरू क्रममा दोहोरिन्छन्, त्यसैले अर्को अक्षर {nxt} हो।')

# ---------- letter series: reverse alphabet ----------
for start in range(20, 26):
    seq = [ALPHA[(start - i) % 26] for i in range(4)]
    nxt = ALPHA[(start - 4) % 26]
    s = ', '.join(seq)
    o, on = letter_opts(nxt)
    E('Letter Series', 'medium', f'What is the next letter in the series: {s}, ...?',
      f'श्रेणी {s}, ... मा अर्को अक्षर कुन हो?', o, on,
      f'The letters go backwards by 1, so the next letter is {nxt}.',
      f'अक्षरहरू १ ले पछाडि जान्छन्, त्यसैले अर्को अक्षर {nxt} हो।')

# ---------- coding: reverse + shift ----------
WORDS = ['NEPAL','KATHMANDU','POKHARA','SCHOOL','TEACHER','STUDENT','BOOK','HOUSE','WATER','RIVER',
         'MOUNTAIN','FOREST','TIGER','FLOWER','GARDEN','MARKET','BRIDGE','TRAIN','MOBILE','COMPUTER',
         'FRIEND','FAMILY','MOTHER','FATHER','DOCTOR','NURSE','POLICE','FARMER','DRIVER','SINGER',
         'HAPPY','BRAVE','HONEST','STRONG','APPLE','MANGO','BANANA','SUMMER','WINTER','MORNING',
         'GOLD','SILVER','IRON','FIRE','EARTH','MUSIC','STORY','POEM','GAME','SPORT','HEALTH','PEACE',
         'TRUTH','LIGHT','DREAM','HOPE','LOVE','LIFE','KING','QUEEN','UNCLE','AUNT','ROAD','PLANE']
def caesar(w, s):
    return ''.join(ALPHA[(ALPHA.index(c)+s) % 26] for c in w)
def rev_shift(w, s):
    return caesar(w[::-1], s)
for w in WORDS:
    for s in (1, 2):
        code = rev_shift(w, s)
        w2 = rng.choice([x for x in WORDS if x != w])
        c2 = rev_shift(w2, s)
        ds = rng.sample([x for x in WORDS if x not in (w, w2)], 3)
        o = [w2] + ds
        on = o[:]
        E('Coding', 'hard', f'In a certain code, {w} is written as {code}. Which word is written as {c2} in the same code?',
          f'एउटा कोडमा {w} लाई {code} लेखिन्छ। त्यही कोडमा {c2} भनेर कुन शब्द लेखिन्छ?', o, on,
          f'The letters are reversed and shifted by {s}, so {c2} stands for {w2}.',
          f'अक्षरहरू उल्टाइन्छन् र {dev(s)} ले सारिन्छन्, त्यसैले {c2} भनेको {w2} हो।')
# coding: A=1 sums with new words
def asum(w):
    return sum(ALPHA.index(c)+1 for c in w)
for w in WORDS:
    s = asum(w)
    ds = [s+5, s-5, s+10]
    o, on, _ = num_opts(s, ds)
    E('Coding', 'medium', f'If A = 1, B = 2, ..., Z = 26, what is the sum of the letters of the word "{w}"?',
      f'यदि A = १, B = २, ..., Z = २६ हो भने "{w}" शब्दका अक्षरहरूको योग कति हुन्छ?', o, on,
      f'The sum of the letters of "{w}" is {s}.', f'"{w}" शब्दका अक्षरहरूको योग {dev_num(s)} हो।')
# coding: number-letter code (A=1, word -> number of letters x sum)
for w in WORDS[:40]:
    s = asum(w)
    code = len(w) * s
    w2 = rng.choice([x for x in WORDS if x != w])
    s2 = asum(w2)
    code2 = len(w2) * s2
    o, on, _ = num_opts(code2, [code2+10, code2-10, code2+5, code2-5])
    E('Coding', 'hard', f'If the code of "{w}" is {code} (number of letters x sum of letter values), what is the code of "{w2}"?',
      f'यदि "{w}" को कोड {dev_num(code)} हो (अक्षर सङ्ख्या x अक्षर मानहरूको योग) भने "{w2}" को कोड के हो?', o, on,
      f'The code of "{w2}" is {len(w2)} x {s2} = {code2}.', f'"{w2}" को कोड {dev(len(w2))} x {dev_num(s2)} = {dev_num(code2)} हो।')

# ---------- blood relations with names ----------
NAMES_M = ['Ram', 'Hari', 'Shyam', 'Mohan', 'Binod', 'Suresh']
NAMES_F = ['Sita', 'Gita', 'Rita', 'Sarita', 'Sunita', 'Mina']
RELN = [
    ('{a} is the father of {b}. {b} is the mother of {c}. How is {a} related to {c}?', '{a} {b} का बुबा हुन्। {b} {c} की आमा हुन्। {a} {c} का के हुन्?', 'Maternal grandfather', 'मावली हजुरबुबा', 'Paternal grandfather', 'पितृ हजुरबुबा', 'Father', 'बुबा', 'Uncle', 'काका'),
    ('{a} is the mother of {b}. {b} is the father of {c}. How is {a} related to {c}?', '{a} {b} की आमा हुन्। {b} {c} का बुबा हुन्। {a} {c} की के हुन्?', 'Paternal grandmother', 'पितृ हजुरआमा', 'Maternal grandmother', 'मावली हजुरआमा', 'Mother', 'आमा', 'Aunt', 'फुपू'),
    ('{a} is the brother of {b}. {b} is the sister of {c}. How is {a} related to {c}?', '{a} {b} का दाजु हुन्। {b} {c} की दिदी हुन्। {a} {c} का के हुन्?', 'Brother', 'दाजु/भाइ', 'Sister', 'दिदी/बहिनी', 'Father', 'बुबा', 'Uncle', 'काका'),
    ('{a} is the son of {b}. {b} is the brother of {c}. How is {a} related to {c}?', '{a} {b} का छोरा हुन्। {b} {c} का भाइ हुन्। {a} {c} का के हुन्?', 'Nephew', 'भतिजा/भान्जा', 'Son', 'छोरा', 'Brother', 'भाइ', 'Grandson', 'नाति'),
    ('{a} is the daughter of {b}. {b} is the sister of {c}. How is {a} related to {c}?', '{a} {b} की छोरी हुन्। {b} {c} की बहिनी हुन्। {a} {c} की के हुन्?', 'Niece', 'भतिजी/भान्जी', 'Daughter', 'छोरी', 'Sister', 'बहिनी', 'Granddaughter', 'नातिनी'),
    ('{a} is the husband of {b}. {b} is the mother of {c}. How is {a} related to {c}?', '{a} {b} का श्रीमान् हुन्। {b} {c} की आमा हुन्। {a} {c} का के हुन्?', 'Father', 'बुबा', 'Uncle', 'काका', 'Grandfather', 'हजुरबुबा', 'Brother', 'दाजु'),
]
for _ in range(120):
    q, qn, a, an, d1, d1n, d2, d2n, d3, d3n = rng.choice(RELN)
    a_n, b_n, c_n = rng.sample(NAMES_M + NAMES_F, 3)
    q2 = q.format(a=a_n, b=b_n, c=c_n)
    qn2 = qn.format(a=a_n, b=b_n, c=c_n)
    E('Blood Relations', 'hard', q2, qn2, [a, d1, d2, d3], [an, d1n, d2n, d3n],
      f'The answer is {a}.', f'उत्तर {an} हो।')

# ---------- direction with turns ----------
for _ in range(150):
    # walk north, turn left/right, walk, turn, walk — net displacement computed
    d1 = rng.choice([2, 3, 4, 5, 6, 8, 10])
    d2 = rng.choice([2, 3, 4, 5, 6, 8, 10])
    d3 = rng.choice([2, 3, 4, 5, 6, 8, 10])
    # start facing north; turn left = west, turn right = east
    t1 = rng.choice(['left', 'right'])
    t2 = rng.choice(['left', 'right'])
    # positions: after first leg (north d1), second leg direction, third leg direction
    # facing north; left->west, right->east; then turn left/right from that heading
    dirs = {'north': (0, 1), 'south': (0, -1), 'east': (1, 0), 'west': (-1, 0)}
    left_of = {'north': 'west', 'west': 'south', 'south': 'east', 'east': 'north'}
    right_of = {'north': 'east', 'east': 'south', 'south': 'west', 'west': 'north'}
    h = 'north'
    x, y = 0, d1
    h = left_of[h] if t1 == 'left' else right_of[h]
    dx, dy = dirs[h]; x += dx*d2; y += dy*d2
    h = left_of[h] if t2 == 'left' else right_of[h]
    dx, dy = dirs[h]; x += dx*d3; y += dy*d3
    dist2 = x*x + y*y
    dist = int(math.isqrt(dist2))
    if dist*dist != dist2: continue
    o, on, _ = num_opts(dist, [dist+1, dist-1, dist+2, dist-2])
    t1n = 'बायाँ' if t1 == 'left' else 'दायाँ'
    t2n = 'बायाँ' if t2 == 'left' else 'दायाँ'
    E('Direction Sense', 'hard',
      f'A man faces north and walks {d1} km. He turns {t1} and walks {d2} km. He then turns {t2} and walks {d3} km. How far is he from his starting point?',
      f'एक मानिस उत्तर फर्केर {dev(d1)} किमी हिँड्छ। उनी {t1n} तर्फ मोडिएर {dev(d2)} किमी हिँड्छन्। त्यसपछि {t2n} तर्फ मोडिएर {dev(d3)} किमी हिँड्छन्। उनी सुरुको बिन्दुबाट कति टाढा छन्?',
      o, on,
      f'His final position is {dist} km from the start.', f'उनको अन्तिम स्थान सुरुबाट {dev_num(dist)} किमी टाढा छ।')

# ---------- ranking variants ----------
for _ in range(120):
    total = rng.choice([25, 30, 35, 40, 45, 50])
    pos = rng.randint(3, total-2)
    from_right = total - pos + 1
    if rng.random() < 0.5:
        o, on, _ = num_opts(from_right, [from_right+1, from_right-1, from_right+2, from_right-2])
        E('Ranking', 'medium', f'In a row of {total} students, Ram is {ord_s(pos)} from the left. What is his position from the right?',
          f'{dev(total)} विद्यार्थीको लाइनमा राम बायाँबाट {dev(pos)}औँ छन्। दायाँबाट उनको स्थान कुन हो?',
          o, on, f'Position from the right = {total} - {pos} + 1 = {from_right}.',
          f'दायाँबाट स्थान = {dev(total)} - {dev(pos)} + १ = {dev(from_right)}।')
    else:
        o, on, _ = num_opts(pos, [pos+1, pos-1, pos+2, pos-2])
        E('Ranking', 'medium', f'In a row of {total} students, Ram is {ord_s(from_right)} from the right. What is his position from the left?',
          f'{dev(total)} विद्यार्थीको लाइनमा राम दायाँबाट {dev(from_right)}औँ छन्। बायाँबाट उनको स्थान कुन हो?',
          o, on, f'Position from the left = {total} - {from_right} + 1 = {pos}.',
          f'बायाँबाट स्थान = {dev(total)} - {dev(from_right)} + १ = {dev(pos)}।')
for _ in range(60):
    total = rng.choice([30, 40, 50, 60])
    left = rng.randint(5, total//2)
    right = rng.randint(5, total//2)
    between = total - left - right
    if between < 0: continue
    # if two people swap positions
    o, on, _ = num_opts(between, [between+2, between-2, between+5, between-5])
    E('Ranking', 'hard', f'In a row of {total} students, A is {ord_s(left)} from the left and B is {ord_s(right)} from the right. If they swap positions, how many students are between them?',
      f'{dev(total)} विद्यार्थीको लाइनमा A बायाँबाट {dev(left)}औँ र B दायाँबाट {dev(right)}औँ छन्। उनीहरूले स्थान साटासाट गरे भने उनीहरूबीच कति विद्यार्थी छन्?',
      o, on, f'Students between them = {total} - {left} - {right} = {between}.',
      f'उनीहरूबीचका विद्यार्थी = {dev(total)} - {dev(left)} - {dev(right)} = {dev_num(between)}।')

# ---------- odd-one-out numbers: new sets ----------
for _ in range(100):
    base = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    k = rng.randint(2, 5)
    nums = [base*i for i in range(1, 5)]
    odd = base*k + rng.choice([1, 2, 3])
    if odd in nums: continue
    o = [str(x) for x in nums[:3]] + [str(odd)]
    rng.shuffle(o)
    on = [dev_num(int(x)) for x in o]
    idx = o.index(str(odd))
    E('Odd One Out', 'medium', f'Which is the odd one out: {", ".join(o)}?',
      f'निम्नमध्ये फरक कुन हो: {", ".join(on)}?', o, on,
      f'{odd} is the odd one out; the others are multiples of {base}.',
      f'{dev_num(odd)} फरक हो; अरू {dev(base)} का गुणन हुन्।', idx=idx)
for _ in range(100):
    # squares vs non-square
    sq = rng.choice([16, 25, 36, 49, 64, 81, 100, 121, 144])
    others = [sq+1, sq+2, sq-1]
    nums = [sq] + others
    rng.shuffle(nums)
    o = [str(x) for x in nums]
    on = [dev_num(x) for x in nums]
    idx = o.index(str(sq))
    E('Odd One Out', 'medium', f'Which is the odd one out: {", ".join(o)}?',
      f'निम्नमध्ये फरक कुन हो: {", ".join(on)}?', o, on,
      f'{sq} is a perfect square; the others are not.', f'{dev_num(sq)} पूर्ण वर्ग हो; अरू होइनन्।', idx=idx)
for _ in range(80):
    # primes vs composite
    p = rng.choice([11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47])
    comps = [p+1, p+3, p+5]
    nums = [p] + comps
    rng.shuffle(nums)
    o = [str(x) for x in nums]
    on = [dev_num(x) for x in nums]
    idx = o.index(str(p))
    E('Odd One Out', 'medium', f'Which is the odd one out: {", ".join(o)}?',
      f'निम्नमध्ये फरक कुन हो: {", ".join(on)}?', o, on,
      f'{p} is prime; the others are composite.', f'{dev_num(p)} अभाज्य हो; अरू भाज्य छन्।', idx=idx)

# ---------- analogy pairs (new) ----------
ANAL = [
    ('Book', 'Read', 'Pen', 'Write', 'किताब', 'पढ्नु', 'कलम', 'लेख्नु'),
    ('Bird', 'Fly', 'Fish', 'Swim', 'चरा', 'उड्नु', 'माछा', 'पौडिनु'),
    ('Sun', 'Day', 'Moon', 'Night', 'सूर्य', 'दिन', 'चन्द्रमा', 'रात'),
    ('Water', 'Thirst', 'Food', 'Hunger', 'पानी', 'तिर्खा', 'खाना', 'भोक'),
    ('Teacher', 'Teach', 'Doctor', 'Treat', 'शिक्षक', 'पढाउनु', 'डाक्टर', 'उपचार गर्नु'),
    ('Knife', 'Cut', 'Pen', 'Write', 'चक्कु', 'काट्नु', 'कलम', 'लेख्नु'),
    ('Car', 'Road', 'Ship', 'Sea', 'कार', 'सडक', 'जहाज', 'समुद्र'),
    ('Eye', 'See', 'Ear', 'Hear', 'आँखा', 'देख्नु', 'कान', 'सुन्नु'),
    ('Nose', 'Smell', 'Tongue', 'Taste', 'नाक', 'सुँघ्नु', 'जिब्रो', 'स्वाद लिनु'),
    ('Hand', 'Write', 'Leg', 'Walk', 'हात', 'लेख्नु', 'खुट्टा', 'हिँड्नु'),
    ('Cow', 'Milk', 'Hen', 'Egg', 'गाई', 'दूध', 'कुखुरा', 'अण्डा'),
    ('Bee', 'Honey', 'Cow', 'Milk', 'मौरी', 'मह', 'गाई', 'दूध'),
    ('King', 'Queen', 'Man', 'Woman', 'राजा', 'रानी', 'पुरुष', 'महिला'),
    ('Father', 'Son', 'Mother', 'Daughter', 'बुबा', 'छोरा', 'आमा', 'छोरी'),
    ('Winter', 'Cold', 'Summer', 'Hot', 'जाडो', 'चिसो', 'गर्मी', 'तातो'),
    ('Rain', 'Umbrella', 'Sun', 'Sunglasses', 'वर्षा', 'छाता', 'घाम', 'सनग्लास'),
    ('Wood', 'Furniture', 'Clay', 'Pot', 'काठ', 'फर्निचर', 'माटो', 'भाँडा'),
    ('Milk', 'Curd', 'Grape', 'Wine', 'दूध', 'दही', 'अङ्गुर', 'वाइन'),
    ('Seed', 'Plant', 'Egg', 'Bird', 'बीउ', 'बिरुवा', 'अण्डा', 'चरा'),
    ('Caterpillar', 'Butterfly', 'Tadpole', 'Frog', 'पुतलीको लार्भा', 'पुतली', 'भ्यागुतोको लार्भा', 'भ्यागुतो'),
]
for a, b, c, d, an, bn, cn, dn in ANAL:
    ds = rng.sample([x for x in ['Write', 'Read', 'Fly', 'Swim', 'Cut', 'See', 'Hear', 'Walk', 'Taste', 'Smell'] if x != d], 3)
    ds_ne = {'Write': 'लेख्नु', 'Read': 'पढ्नु', 'Fly': 'उड्नु', 'Swim': 'पौडिनु', 'Cut': 'काट्नु', 'See': 'देख्नु', 'Hear': 'सुन्नु', 'Walk': 'हिँड्नु', 'Taste': 'स्वाद लिनु', 'Smell': 'सुँघ्नु'}
    o = [d] + ds
    on = [dn] + [ds_ne[x] for x in ds]
    E('Analogies', 'medium', f'{a} is to {b} as {c} is to ___?',
      f'{an} को {bn} सँग जस्तो सम्बन्ध छ, {cn} को ___ सँग उस्तै सम्बन्ध छ?', o, on,
      f'As {a} is related to {b}, so {c} is related to {d}.', f'{an} को {bn} सँग जस्तो सम्बन्ध छ, {cn} को {dn} सँग उस्तै सम्बन्ध छ।')
    # reverse framing
    ds2 = rng.sample([x for x in ['Book', 'Pen', 'Bird', 'Fish', 'Sun', 'Moon', 'Teacher', 'Doctor', 'Knife', 'Car'] if x != c], 3)
    ds2_ne = {'Book': 'किताब', 'Pen': 'कलम', 'Bird': 'चरा', 'Fish': 'माछा', 'Sun': 'सूर्य', 'Moon': 'चन्द्रमा', 'Teacher': 'शिक्षक', 'Doctor': 'डाक्टर', 'Knife': 'चक्कु', 'Car': 'कार'}
    o2 = [c] + ds2
    on2 = [cn] + [ds2_ne[x] for x in ds2]
    E('Analogies', 'medium', f'{a} is to {b} as ___ is to {d}?',
      f'{an} को {bn} सँग जस्तो सम्बन्ध छ, ___ को {dn} सँग उस्तै सम्बन्ध छ?', o2, on2,
      f'As {a} is related to {b}, so {c} is related to {d}.', f'{an} को {bn} सँग जस्तो सम्बन्ध छ, {cn} को {dn} सँग उस्तै सम्बन्ध छ।')

# ---------- letter pairs: which letter comes after/before ----------
for _ in range(120):
    i = rng.randint(0, 24)
    c = ALPHA[i+1]
    o, on = letter_opts(c)
    E('Alphabet Positions', 'easy', f'Which letter comes immediately after {ALPHA[i]} in the English alphabet?',
      f'अङ्ग्रेजी वर्णमालामा {ALPHA[i]} पछि तुरुन्तै कुन अक्षर आउँछ?', o, on,
      f'{c} comes immediately after {ALPHA[i]}.', f'{ALPHA[i]} पछि तुरुन्तै {c} आउँछ।')
for _ in range(120):
    i = rng.randint(1, 25)
    c = ALPHA[i-1]
    o, on = letter_opts(c)
    E('Alphabet Positions', 'easy', f'Which letter comes immediately before {ALPHA[i]} in the English alphabet?',
      f'अङ्ग्रेजी वर्णमालामा {ALPHA[i]} अघि तुरुन्तै कुन अक्षर आउँछ?', o, on,
      f'{c} comes immediately before {ALPHA[i]}.', f'{ALPHA[i]} अघि तुरुन्तै {c} आउँछ।')

n = em.write('expansion-r10-iq3.json')
print('IQ3 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
