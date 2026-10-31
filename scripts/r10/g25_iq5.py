#!/usr/bin/env python3
"""R10 generator 25: IQ 5 (~1,700). Fresh IQ spaces: prime/square-step letter
series, new number-series rules, reverse-alphabet coding, digit-sum odd-one-out,
3-step blood relations, 5-step directions, circular seating, syllogisms,
alphabet sums, new analogies."""
import sys, random, math
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num

def ord_s(n):
    """English ordinal suffix: 1st, 2nd, 3rd, 4th, 11th, 21st, 22nd, 23rd..."""
    n = int(n)
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


bank = Bank()
em = Emitter(bank, 'R10-IQ5')
rng = random.Random(424242)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'tsc-primary', 'tsc-secondary', 'police', 'army', 'health']

def q_emit(topic, diff, marks, q, qn, opts, optn, ans, exp, expn):
    em.emit(EX, 'IQ & Reasoning', topic, diff, marks, q, qn, opts, optn, ans, exp, expn)

L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def letter_opts(ans):
    s = {ans}
    while len(s) < 4:
        s.add(rng.choice(L))
    o = list(s); rng.shuffle(o)
    return o, o.index(ans)

def num_opts(ans, lo, hi, step=1):
    s = {ans}
    while len(s) < 4:
        v = rng.randrange(lo, hi+1, step)
        if v != ans and v >= 0: s.add(v)
    o = list(s); rng.shuffle(o)
    return o, o.index(ans)

# ---------- letter series: prime steps ----------
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
for _ in range(120):
    start = rng.randrange(0, 10)
    pi = rng.randrange(0, 4)
    seq = [start]
    for k in range(4):
        seq.append((seq[-1] + primes[pi+k]) % 26)
    nxt = (seq[-1] + primes[pi+4]) % 26
    letters = [L[i] for i in seq]
    ans = L[nxt]
    o, ai = letter_opts(ans)
    disp = ', '.join(letters)
    q_emit('Letter Series', 'hard', 2,
        f"What is the next letter in the series: {disp}, ...?", f"श्रेणीको अर्को अक्षर कुन हो: {disp}, ...?",
        o, o, ai,
        f"The letters advance by consecutive prime numbers: +{primes[pi]}, +{primes[pi+1]}, +{primes[pi+2]}, +{primes[pi+3]}, so next is +{primes[pi+4]} = {ans}.",
        f"अक्षरहरू क्रमागत अभाज्य सङ्ख्याले अगाडि बढ्छन्: +{primes[pi]}, +{primes[pi+1]}, +{primes[pi+2]}, +{primes[pi+3]}, त्यसैले अर्को +{primes[pi+4]} = {ans} हो।")

# ---------- letter series: square steps ----------
for _ in range(100):
    start = rng.randrange(0, 8)
    sq = [1, 4, 9, 16, 25]
    seq = [start]
    for k in range(4):
        seq.append((seq[-1] + sq[k]) % 26)
    nxt = (seq[-1] + sq[4]) % 26
    letters = [L[i] for i in seq]
    ans = L[nxt]
    o, ai = letter_opts(ans)
    disp = ', '.join(letters)
    q_emit('Letter Series', 'hard', 2,
        f"What is the next letter in the series: {disp}, ...?", f"श्रेणीको अर्को अक्षर कुन हो: {disp}, ...?",
        o, o, ai,
        f"The letters advance by square numbers: +1, +4, +9, +16, so next is +25 = {ans}.",
        f"अक्षरहरू वर्ग सङ्ख्याले अगाडि बढ्छन्: +१, +४, +९, +१६, त्यसैले अर्को +२५ = {ans} हो।")

# ---------- number series: x2-3, x3+2, +cubes, triangular ----------
def series_block(gen, name, n=90):
    for _ in range(n):
        seq, ans = gen()
        if seq is None: continue
        disp = ', '.join(str(x) for x in seq)
        o, ai = num_opts(ans, max(0, ans-30), ans+30, 1)
        q_emit('Number Series', 'medium', 1,
            f"What is the next number in the series: {disp}, ...?", f"श्रेणीको अर्को सङ्ख्या कति हो: {disp}, ...?",
            [str(x) for x in o], [dev_num(x) for x in o], ai,
            f"The series follows the {name} pattern. The next term is {ans}.",
            f"श्रेणीले {name} ढाँचा पछ्याउँछ। अर्को पद {ans} हो।")
def g_x2m3():
    a = rng.randrange(4, 20); s = [a]
    for _ in range(4): s.append(s[-1]*2 - 3)
    return s, s[-1]*2 - 3
def g_x3p2():
    a = rng.randrange(2, 12); s = [a]
    for _ in range(4): s.append(s[-1]*3 + 2)
    return s, s[-1]*3 + 2
def g_cubes():
    a = rng.randrange(2, 20); s = [a]; i = rng.randrange(1, 3)
    for k in range(4): s.append(s[-1] + (i+k)**3)
    return s, s[-1] + (i+4)**3
def g_tri():
    a = rng.randrange(1, 10); s = [a]; i = rng.randrange(1, 5)
    tri = [1, 3, 6, 10, 15, 21, 28, 36, 45]
    for k in range(4): s.append(s[-1] + tri[i+k])
    return s, s[-1] + tri[i+4]
def g_odd():
    a = rng.randrange(3, 30); s = [a]; i = rng.randrange(0, 5)
    odds = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    for k in range(4): s.append(s[-1] + odds[i+k])
    return s, s[-1] + odds[i+4]
series_block(g_x2m3, 'multiply by 2 and subtract 3')
series_block(g_x3p2, 'multiply by 3 and add 2')
series_block(g_cubes, 'add consecutive cubes')
series_block(g_tri, 'add consecutive triangular numbers')
series_block(g_odd, 'add consecutive odd numbers')

# ---------- coding: reverse alphabet (A=Z) ----------
REV = {L[i]: L[25-i] for i in range(26)}
WORDS = ['CAT', 'DOG', 'SUN', 'MOON', 'STAR', 'FISH', 'BIRD', 'BOOK', 'TREE', 'KING', 'LION', 'WOLF', 'BEAR', 'DUCK', 'FROG', 'GOAT', 'HORSE', 'MOUSE', 'SNAKE', 'TIGER', 'APPLE', 'MANGO', 'NEPAL', 'KATHMANDU', 'WATER', 'EARTH', 'FIRE', 'WIND', 'RAIN', 'CLOUD', 'RIVER', 'MOUNT', 'GREEN', 'BLACK', 'WHITE', 'BROWN', 'SMALL', 'LARGE', 'HAPPY', 'BRAVE', 'SMART', 'QUICK', 'SLOW', 'FAST', 'HIGH', 'LONG', 'SHORT', 'ROUND', 'SQUARE']
for w in WORDS:
    code = ''.join(REV[c] for c in w)
    others = [x for x in WORDS if x != w and len(x) == len(w)]
    rng.shuffle(others)
    ds = [''.join(REV[c] for c in x) for x in others[:3]]
    if code in ds: continue
    o = [code] + ds; rng.shuffle(o)
    q_emit('Coding-Decoding', 'medium', 1,
        f"In a code, A is written as Z, B as Y, C as X and so on (reverse alphabet). How is '{w}' written in that code?",
        f"एउटा कोडमा A लाई Z, B लाई Y, C लाई X आदि (उल्टो वर्णमाला) लेखिन्छ। '{w}' लाई उक्त कोडमा कसरी लेखिन्छ?",
        o, o, o.index(code),
        f"Each letter is replaced by its reverse-alphabet partner: {w} -> {code}.",
        f"प्रत्येक अक्षरलाई उल्टो वर्णमालाको जोडीले प्रतिस्थापन गरिन्छ: {w} -> {code} हो।")

# ---------- coding: sum of letter positions of a word ----------
for w in WORDS:
    s = sum(L.index(c)+1 for c in w)
    o, ai = num_opts(s, max(1, s-20), s+20, 1)
    q_emit('Coding-Decoding', 'medium', 1,
        f"If A=1, B=2, C=3, ... Z=26, what is the sum of the letter values of '{w}'?",
        f"यदि A=१, B=२, C=३, ... Z=२६ हो भने '{w}' का अक्षरहरूको मानको योग कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Sum = {' + '.join(str(L.index(c)+1) for c in w)} = {s}.",
        f"योग = {' + '.join(dev_num(L.index(c)+1) for c in w)} = {dev_num(s)} हो।")

# ---------- odd-one-out: digit sum ----------
for _ in range(100):
    base = rng.randrange(10, 99)
    ds = sum(int(c) for c in str(base))
    # pick 3 numbers with digit sum != ds, one with digit sum == ds? No: odd one out = the one whose digit sum differs
    cands = []
    attempts = 0
    while len(cands) < 3 and attempts < 200:
        attempts += 1
        v = rng.randrange(10, 99)
        if sum(int(c) for c in str(v)) == ds and v != base and v not in cands:
            cands.append(v)
    if len(cands) < 3: continue
    odd = None
    while odd is None:
        v = rng.randrange(10, 99)
        if sum(int(c) for c in str(v)) != ds:
            odd = v
    o = cands + [odd]; rng.shuffle(o)
    q_emit('Odd One Out', 'medium', 1,
        f"Which is the odd one out? {', '.join(str(x) for x in o)}",
        f"कुन फरक छ? {', '.join(dev_num(x) for x in o)}",
        [str(x) for x in o], [dev_num(x) for x in o], o.index(odd),
        f"All numbers except {odd} have digit sum {ds}. {odd} has digit sum {sum(int(c) for c in str(odd))}.",
        f"{odd} बाहेक सबै सङ्ख्याको अङ्क योग {ds} छ। {odd} को अङ्क योग {sum(int(c) for c in str(odd))} हो।")

# ---------- odd-one-out: perfect cubes ----------
for _ in range(60):
    cubes = [1, 8, 27, 64, 125, 216, 343, 512]
    chosen = rng.sample(cubes, 3)
    odd = rng.randrange(10, 500)
    while odd in cubes or int(round(odd ** (1/3))) ** 3 == odd:
        odd = rng.randrange(10, 500)
    o = chosen + [odd]; rng.shuffle(o)
    q_emit('Odd One Out', 'easy', 1,
        f"Which is the odd one out? {', '.join(str(x) for x in o)}",
        f"कुन फरक छ? {', '.join(dev_num(x) for x in o)}",
        [str(x) for x in o], [dev_num(x) for x in o], o.index(odd),
        f"{chosen[0]}, {chosen[1]} and {chosen[2]} are perfect cubes ({int(round(chosen[0]**(1/3)))}^3, {int(round(chosen[1]**(1/3)))}^3, {int(round(chosen[2]**(1/3)))}^3). {odd} is not a perfect cube.",
        f"{chosen[0]}, {chosen[1]} र {chosen[2]} पूर्ण घन हुन् ({int(round(chosen[0]**(1/3)))}^३, {int(round(chosen[1]**(1/3)))}^३, {int(round(chosen[2]**(1/3)))}^३)। {odd} पूर्ण घन होइन।")

# ---------- blood relations: 3-step ----------
NAMES_M = ['Ram', 'Hari', 'Sita', 'Gita', 'Ramesh', 'Suresh', 'Anita', 'Sunita', 'Bikash', 'Prakash', 'Maya', 'Laxmi', 'Krishna', 'Rita', 'Deepak', 'Nirmala']
REL3 = [
    ("{a} is the son of {b}. {b} is the brother of {c}. How is {a} related to {c}?", "{a}, {b} को छोरा हो। {b}, {c} को भाइ हो। {a}, {c} को के हो?", "Nephew", "भतिजा/भान्जा", ["Son", "Brother", "Cousin"]),
    ("{a} is the daughter of {b}. {b} is the sister of {c}. How is {a} related to {c}?", "{a}, {b} की छोरी हो। {b}, {c} की बहिनी हो। {a}, {c} को के हो?", "Niece", "भतिजी/भान्जी", ["Daughter", "Sister", "Cousin"]),
    ("{a} is the father of {b}. {b} is the mother of {c}. How is {a} related to {c}?", "{a}, {b} को बुबा हो। {b}, {c} की आमा हो। {a}, {c} को के हो?", "Maternal grandfather", "मावली हजुरबुबा", ["Father", "Grandfather", "Uncle"]),
    ("{a} is the mother of {b}. {b} is the father of {c}. How is {a} related to {c}?", "{a}, {b} की आमा हो। {b}, {c} को बुबा हो। {a}, {c} को के हो?", "Paternal grandmother", "पितातर्फकी हजुरआमा", ["Mother", "Grandmother", "Aunt"]),
    ("{a} is the brother of {b}. {b} is the father of {c}. How is {a} related to {c}?", "{a}, {b} को भाइ हो। {b}, {c} को बुबा हो। {a}, {c} को के हो?", "Uncle", "काका/मामा", ["Father", "Brother", "Grandfather"]),
    ("{a} is the sister of {b}. {b} is the mother of {c}. How is {a} related to {c}?", "{a}, {b} की बहिनी हो। {b}, {c} की आमा हो। {a}, {c} को के हो?", "Aunt", "फुपू/माइजू", ["Mother", "Sister", "Grandmother"]),
]
for _ in range(120):
    t, tn, ans, ansn, ds = rng.choice(REL3)
    a, b, c = rng.sample(NAMES_M, 3)
    q = t.format(a=a, b=b, c=c)
    qn = tn.format(a=a, b=b, c=c)
    dne = {'Son': 'छोरा', 'Brother': 'भाइ', 'Cousin': 'चचेरा भाइ/बहिनी', 'Daughter': 'छोरी', 'Sister': 'बहिनी', 'Father': 'बुबा', 'Grandfather': 'हजुरबुबा', 'Uncle': 'काका/मामा', 'Mother': 'आमा', 'Grandmother': 'हजुरआमा', 'Aunt': 'फुपू/माइजू', 'Nephew': 'भतिजा/भान्जा', 'Niece': 'भतिजी/भान्जी', 'Maternal grandfather': 'मावली हजुरबुबा', 'Paternal grandmother': 'पितातर्फकी हजुरआमा'}
    o = [ans] + ds; rng.shuffle(o)
    q_emit('Blood Relations', 'hard', 2, q, qn, o, [dne.get(x, x) for x in o], o.index(ans),
        f"From the chain: {a} is the {ans.lower()} of {c}.",
        f"शृङ्खलाबाट: {a}, {c} को {ansn} हो।")

# ---------- directions: 5-step walk, net displacement ----------
DIRS = [('north', 'उत्तर'), ('south', 'दक्षिण'), ('east', 'पूर्व'), ('west', 'पश्चिम')]
for _ in range(100):
    steps = []
    x = y = 0
    for _ in range(5):
        d, dn = rng.choice(DIRS)
        dist = rng.choice([2, 3, 4, 5, 6, 8, 10])
        steps.append((d, dn, dist))
        if d == 'north': y += dist
        elif d == 'south': y -= dist
        elif d == 'east': x += dist
        else: x -= dist
    if x == 0 and y == 0: continue
    # net direction
    if x == 0: net = 'north' if y > 0 else 'south'
    elif y == 0: net = 'east' if x > 0 else 'west'
    elif x > 0 and y > 0: net = 'north-east'
    elif x > 0 and y < 0: net = 'south-east'
    elif x < 0 and y > 0: net = 'north-west'
    else: net = 'south-west'
    ne_net = {'north': 'उत्तर', 'south': 'दक्षिण', 'east': 'पूर्व', 'west': 'पश्चिम', 'north-east': 'उत्तर-पूर्व', 'south-east': 'दक्षिण-पूर्व', 'north-west': 'उत्तर-पश्चिम', 'south-west': 'दक्षिण-पश्चिम'}[net]
    dist_net = round(math.hypot(x, y), 1)
    if dist_net != int(dist_net): continue
    dist_net = int(dist_net)
    desc = ', then '.join(f"{d} {dist} km" for d, dn, dist in steps)
    desc_ne = ', त्यसपछि '.join(f"{dn} {dev_num(dist)} किमी" for d, dn, dist in steps)
    opts = ['north', 'south', 'east', 'west', 'north-east', 'south-east', 'north-west', 'south-west']
    rng.shuffle(opts)
    opts = opts[:4]
    if net not in opts: opts[0] = net
    rng.shuffle(opts)
    ne_map = {'north': 'उत्तर', 'south': 'दक्षिण', 'east': 'पूर्व', 'west': 'पश्चिम', 'north-east': 'उत्तर-पूर्व', 'south-east': 'दक्षिण-पूर्व', 'north-west': 'उत्तर-पश्चिम', 'south-west': 'दक्षिण-पश्चिम'}
    q_emit('Direction Sense', 'hard', 2,
        f"A man walks {desc}. In which direction is he from his starting point?",
        f"एक जना मानिस {desc_ne} हिँड्छ। ऊ सुरुको बिन्दुबाट कुन दिशामा छ?",
        [o.capitalize() for o in opts], [ne_map[o] for o in opts], opts.index(net),
        f"Net displacement: east-west = {x} km, north-south = {y} km. He is {dist_net} km to the {net} of the start.",
        f"शुद्ध विस्थापन: पूर्व-पश्चिम = {dev_num(x)} किमी, उत्तर-दक्षिण = {dev_num(y)} किमी। ऊ सुरुको बिन्दुबाट {dev_num(dist_net)} किमी {ne_net} तर्फ छ।")

# ---------- ranking: two people ----------
for _ in range(80):
    n = rng.choice([20, 25, 30, 35, 40])
    r1 = rng.randrange(3, n-5)
    gap = rng.randrange(2, 8)
    r2 = r1 + gap
    if r2 > n: continue
    # person B's rank from the end
    ans = n - r2 + 1
    o, ai = num_opts(ans, 1, n, 1)
    q_emit('Ranking', 'medium', 1,
        f"In a row of {n} students, A is {ord_s(r1)} from the left and B is {gap} positions to the right of A. What is B's rank from the right?",
        f"{n} जना विद्यार्थीको लाइनमा A बायाँबाट {r1}औँ छ र B, A भन्दा {gap} स्थान दायाँ छ। B को दायाँबाट स्थान कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"B is {ord_s(r2)} from the left. From the right, B is {n} - {r2} + 1 = {ord_s(ans)}.",
        f"B बायाँबाट {r2}औँ छ। दायाँबाट B {n} - {r2} + १ = {ans}औँ हो।")

# ---------- circular seating: opposite ----------
for _ in range(60):
    n = rng.choice([6, 8, 10, 12])
    names = rng.sample(NAMES_M, n)
    # seats around circle, person at position 0; opposite is n/2
    pos = rng.randrange(n)
    opp = (pos + n//2) % n
    q_emit('Seating Arrangement', 'medium', 1,
        f"{n} people sit around a circular table at equal distances in the order: {', '.join(names)}. Who sits opposite {names[pos]}?",
        f"{n} जना मानिस गोलाकार टेबल वरिपरि समान दूरीमा यस क्रममा बस्छन्: {', '.join(names)}। {names[pos]} को विपरीत को बस्छ?",
        [names[opp], names[(pos+1) % n], names[(pos-1) % n], names[(pos+2) % n]],
        [names[opp], names[(pos+1) % n], names[(pos-1) % n], names[(pos+2) % n]], 0,
        f"In a circle of {n}, the person opposite {names[pos]} is {n//2} seats away: {names[opp]}.",
        f"{n} जनाको गोलाकारमा {names[pos]} को विपरीत {n//2} सिट टाढा {names[opp]} बस्छ।")

# ---------- syllogisms ----------
SYL = [
    ("All cats are animals. All animals are living beings. Which conclusion follows?", "सबै बिरालाहरू जनावर हुन्। सबै जनावरहरू जीवित प्राणी हुन्। कुन निष्कर्ष सही छ?", "All cats are living beings", "सबै बिरालाहरू जीवित प्राणी हुन्", ["Some cats are not animals", "No cat is a living being", "All living beings are cats"]),
    ("No bird is a fish. All eagles are birds. Which conclusion follows?", "कुनै पनि चरा माछा होइन। सबै चीलहरू चरा हुन्। कुन निष्कर्ष सही छ?", "No eagle is a fish", "कुनै पनि चील माछा होइन", ["Some eagles are fish", "All fish are birds", "No bird is an eagle"]),
    ("Some pens are books. All books are papers. Which conclusion follows?", "केही कलमहरू किताब हुन्। सबै किताबहरू कागज हुन्। कुन निष्कर्ष सही छ?", "Some pens are papers", "केही कलमहरू कागज हुन्", ["All pens are papers", "No pen is a paper", "All papers are pens"]),
    ("All doctors are educated. Some educated people are teachers. Which conclusion follows?", "सबै डाक्टरहरू शिक्षित छन्। केही शिक्षित मानिसहरू शिक्षक हुन्। कुन निष्कर्ष सही छ?", "Some teachers may be doctors", "केही शिक्षकहरू डाक्टर हुन सक्छन्", ["All doctors are teachers", "No doctor is a teacher", "All teachers are doctors"]),
    ("No student is lazy. Ram is a student. Which conclusion follows?", "कुनै पनि विद्यार्थी अल्छी छैन। राम विद्यार्थी हो। कुन निष्कर्ष सही छ?", "Ram is not lazy", "राम अल्छी छैन", ["Ram is lazy", "All students are Ram", "Ram is not a student"]),
    ("All roses are flowers. Some flowers are red. Which conclusion follows?", "सबै गुलाबहरू फूल हुन्। केही फूलहरू रातो छन्। कुन निष्कर्ष सही छ?", "Some roses may be red", "केही गुलाबहरू रातो हुन सक्छन्", ["All roses are red", "No rose is red", "All red things are roses"]),
]
for q, qn, ans, ansn, ds in SYL:
    for _ in range(6):
        o = [ans] + ds; rng.shuffle(o)
        q_emit('Syllogism', 'hard', 2, q, qn, o, [ansn if x == ans else x for x in o], o.index(ans),
            f"By syllogism, the valid conclusion is: {ans}.",
            f"तर्कशास्त्र अनुसार मान्य निष्कर्ष हो: {ansn}।")

# ---------- alphabet: sum of positions of two letters ----------
for _ in range(100):
    a, b = rng.sample(L, 2)
    s = (L.index(a)+1) + (L.index(b)+1)
    o, ai = num_opts(s, 2, 52, 1)
    q_emit('Alphabet Test', 'easy', 1,
        f"If A=1, B=2, ... Z=26, what is the sum of the positions of '{a}' and '{b}'?",
        f"यदि A=१, B=२, ... Z=२६ हो भने '{a}' र '{b}' को स्थानको योग कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"{a} = {L.index(a)+1} and {b} = {L.index(b)+1}. Sum = {s}.",
        f"{a} = {dev_num(L.index(a)+1)} र {b} = {dev_num(L.index(b)+1)} हो। योग = {dev_num(s)} हो।")

# ---------- alphabet: letter 2 steps before/after ----------
for _ in range(100):
    a = rng.choice(L)
    k = rng.choice([2, 3, 4])
    fwd = rng.random() < 0.5
    idx = L.index(a)
    ans_idx = (idx + k) % 26 if fwd else (idx - k) % 26
    ans = L[ans_idx]
    o, ai = letter_opts(ans)
    word = 'after' if fwd else 'before'
    word_ne = 'पछि' if fwd else 'अघि'
    q_emit('Alphabet Test', 'easy', 1,
        f"Which letter is {k} places {word} '{a}' in the English alphabet?",
        f"अङ्ग्रेजी वर्णमालामा '{a}' को {k} स्थान {word_ne} कुन अक्षर आउँछ?",
        o, o, ai,
        f"Counting {k} places {word} {a} gives {ans}.",
        f"{a} बाट {k} स्थान {word_ne} गन्दा {ans} आउँछ।")

# ---------- analogies: new pairs ----------
ANAL = [
    ('Cow', 'Calf', 'गाई', 'बाछो', 'Dog', 'Puppy', 'कुकुर', 'कुकुरको बच्चा', ['Horse', 'Foal', 'घोडा', 'बछेडो'], ['Cat', 'Kitten', 'बिरालो', 'बिरालोको बच्चा'], ['Goat', 'Kid', 'बाख्रा', 'पाठो']),
    ('Doctor', 'Patient', 'डाक्टर', 'बिरामी', 'Teacher', 'Student', 'शिक्षक', 'विद्यार्थी', ['Lawyer', 'Client', 'वकिल', 'मुवक्किल'], ['Cook', 'Food', 'भान्से', 'खाना'], ['Driver', 'Car', 'चालक', 'कार']),
    ('Pen', 'Write', 'कलम', 'लेख्नु', 'Knife', 'Cut', 'चक्कु', 'काट्नु', ['Book', 'Read', 'किताब', 'पढ्नु'], ['Spoon', 'Eat', 'चम्चा', 'खानु'], ['Hammer', 'Nail', 'हथौडा', 'किला']),
    ('Bird', 'Nest', 'चरा', 'गुँड', 'Bee', 'Hive', 'मौरी', 'घार', ['Dog', 'Kennel', 'कुकुर', 'कुकुरको घर'], ['Lion', 'Den', 'सिंह', 'गुफा'], ['Horse', 'Stable', 'घोडा', 'अस्तबल']),
    ('Water', 'Thirst', 'पानी', 'तृष्णा', 'Food', 'Hunger', 'खाना', 'भोक', ['Air', 'Breath', 'हावा', 'श्वास'], ['Sleep', 'Tiredness', 'निद्रा', 'थकान'], ['Light', 'Darkness', 'प्रकाश', 'अँधेरो']),
    ('King', 'Queen', 'राजा', 'रानी', 'Prince', 'Princess', 'राजकुमार', 'राजकुमारी', ['Man', 'Woman', 'पुरुष', 'महिला'], ['Father', 'Mother', 'बुबा', 'आमा'], ['Brother', 'Sister', 'भाइ', 'बहिनी']),
    ('Book', 'Author', 'किताब', 'लेखक', 'Song', 'Singer', 'गीत', 'गायक', ['Painting', 'Painter', 'चित्र', 'चित्रकार'], ['Poem', 'Poet', 'कविता', 'कवि'], ['House', 'Builder', 'घर', 'निर्माणकर्ता']),
    ('Eye', 'See', 'आँखा', 'देख्नु', 'Ear', 'Hear', 'कान', 'सुन्नु', ['Nose', 'Smell', 'नाक', 'सुँघ्नु'], ['Tongue', 'Taste', 'जिब्रो', 'स्वाद लिनु'], ['Hand', 'Touch', 'हात', 'छुनु']),
    ('Sun', 'Day', 'सूर्य', 'दिन', 'Moon', 'Night', 'चन्द्रमा', 'रात', ['Star', 'Sky', 'तारा', 'आकाश'], ['Rain', 'Cloud', 'वर्षा', 'बादल'], ['Fire', 'Heat', 'आगो', 'तातो']),
    ('Wheel', 'Car', 'पाङ्ग्रा', 'कार', 'Wing', 'Bird', 'पखेटा', 'चरा', ['Engine', 'Train', 'इन्जिन', 'रेल'], ['Sail', 'Boat', 'पाल', 'डुङ्गा'], ['Rudder', 'Ship', 'पतवार', 'जहाज']),
]
for a1, b1, a1n, b1n, a2, b2, a2n, b2n, d1, d2, d3 in ANAL:
    for _ in range(4):
        ds = [d1[1], d2[1], d3[1]]
        ds_ne = [d1[3], d2[3], d3[3]]
        o = [b2] + ds; rng.shuffle(o)
        on = []
        for x in o:
            if x == b2: on.append(b2n)
            elif x == d1[1]: on.append(d1[3])
            elif x == d2[1]: on.append(d2[3])
            else: on.append(d3[3])
        q_emit('Analogies', 'medium', 1,
            f"{a1} is to {b1} as {a2} is to ...?", f"{a1n} को {b1n} सँग जस्तो सम्बन्ध छ, {a2n} को ... सँग त्यस्तै सम्बन्ध छ?",
            o, on, o.index(b2),
            f"{a1} relates to {b1} as {a2} relates to {b2}.",
            f"{a1n} को {b1n} सँग जस्तो सम्बन्ध छ, {a2n} को {b2n} सँग त्यस्तै सम्बन्ध छ।")

n = em.write('expansion-r10-iq5.json')
print('IQ5 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
