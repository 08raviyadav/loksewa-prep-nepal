#!/usr/bin/env python3
"""R10 generator 2: IQ & Reasoning (~5,500). Letter series, coding-decoding,
odd-one-out, alphabet positions, blood relations, direction sense, ranking,
seating, word analogies. All answers computed by the script."""
import sys, random
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
em = Emitter(bank, 'R10-IQ')
rng = random.Random(81002)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'police', 'army', 'tsc-primary', 'tsc-secondary']
EXH = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'csit-entrance', 'ioe-entrance']

def L(i):
    return chr(ord('A') + i % 26)

def letter_opts(correct, cands):
    out = [correct]
    for c in cands:
        if len(out) == 4:
            break
        if c not in out:
            out.append(c)
    while len(out) < 4:
        c = L(rng.randint(0, 25))
        if c not in out:
            out.append(c)
    return out, out, 0

# ---------------- 1. Letter series (step patterns) ----------------
for _ in range(700):
    start = rng.randint(0, 25)
    step = rng.choice([1, 2, 3, 4, 5])
    n = 5
    seq = [L(start + i * step) for i in range(n)]
    nxt = L(start + n * step)
    s = ', '.join(seq) + ', ?'
    opts, optsn, a = letter_opts(nxt, [L(start + n * step + 1), L(start + n * step - 1), L(start + n * step + 2), L(start + (n - 1) * step)])
    em.emit(EX, 'IQ & Reasoning', 'Letter Series', 'medium', 2,
            f'Find the next letter in the series: {s}',
            f'तलको अक्षर श्रृङ्खलाको अर्को अक्षर कुन हो? {s}',
            opts, optsn, a,
            f'Each letter moves {step} step(s) forward: {seq[-1]} + {step} = {nxt}.',
            f'प्रत्येक अक्षर {dev_num(step)} कदम अगाडि बढ्छ: {seq[-1]} + {dev_num(step)} = {nxt}।')
# alternating steps
for _ in range(300):
    start = rng.randint(0, 25)
    s1 = rng.randint(1, 4)
    s2 = rng.randint(1, 4)
    seq = [start]
    for i in range(4):
        seq.append(seq[-1] + (s1 if i % 2 == 0 else s2))
    letters = [L(x) for x in seq]
    nxt = L(seq[-1] + (s1 if 4 % 2 == 0 else s2))
    s = ', '.join(letters) + ', ?'
    opts, optsn, a = letter_opts(nxt, [L(seq[-1] + s1 + 1), L(seq[-1] + s2 - 1), L(seq[-1] + 1), L(seq[-1] + 3)])
    em.emit(EXH, 'IQ & Reasoning', 'Letter Series', 'hard', 2,
            f'Find the next letter in the series: {s}',
            f'तलको अक्षर श्रृङ्खलाको अर्को अक्षर कुन हो? {s}',
            opts, optsn, a,
            f'Steps alternate +{s1}, +{s2}: {letters[-1]} + {s1 if 4 % 2 == 0 else s2} = {nxt}.',
            f'कदम पालैपालो +{dev_num(s1)}, +{dev_num(s2)} हुन्छ: {letters[-1]} + {dev_num(s1 if 4 % 2 == 0 else s2)} = {nxt}।')
# reverse series
for _ in range(200):
    start = rng.randint(10, 25)
    step = rng.choice([1, 2, 3])
    seq = [L(start - i * step) for i in range(5)]
    nxt = L(start - 5 * step)
    s = ', '.join(seq) + ', ?'
    opts, optsn, a = letter_opts(nxt, [L(start - 5 * step + 1), L(start - 5 * step - 1), L(start - 4 * step), L(start - 5 * step + 2)])
    em.emit(EX, 'IQ & Reasoning', 'Letter Series', 'medium', 2,
            f'Find the next letter in the series: {s}',
            f'तलको अक्षर श्रृङ्खलाको अर्को अक्षर कुन हो? {s}',
            opts, optsn, a,
            f'Each letter moves {step} step(s) backward: {seq[-1]} - {step} = {nxt}.',
            f'प्रत्येक अक्षर {dev_num(step)} कदम पछाडि जान्छ: {seq[-1]} − {dev_num(step)} = {nxt}।')

# ---------------- 2. Coding: letter shift ----------------
WORDS = ['CAT', 'DOG', 'SUN', 'MOON', 'STAR', 'BOOK', 'TREE', 'FISH', 'BIRD', 'KING',
         'LION', 'TIGER', 'NEPAL', 'KATHMANDU', 'RIVER', 'MOUNT', 'LIGHT', 'WATER', 'EARTH', 'HEART',
         'TABLE', 'CHAIR', 'SCHOOL', 'TEACHER', 'STUDENT', 'MOTHER', 'FATHER', 'SISTER', 'BROTHER',
         'GOLD', 'SILVER', 'IRON', 'APPLE', 'MANGO', 'HOUSE', 'ROAD', 'BRIDGE', 'TEMPLE', 'MARKET',
         'POLICE', 'ARMY', 'DOCTOR', 'NURSE', 'PILOT', 'FARMER', 'WRITER', 'SINGER', 'DANCER', 'PLAYER']
for w in WORDS:
    for shift in [1, 2, 3, -1, -2]:
        coded = ''.join(L(ord(c) - 65 + shift) for c in w)
        # ask: code a second word with same shift
        w2 = rng.choice([x for x in WORDS if x != w])
        coded2 = ''.join(L(ord(c) - 65 + shift) for c in w2)
        ds = []
        for dshift in [shift + 1, shift - 1, shift + 2]:
            ds.append(''.join(L(ord(c) - 65 + dshift) for c in w2))
        opts, optsn, a = letter_opts(coded2, ds)
        direction = 'forward' if shift > 0 else 'backward'
        dn = 'अगाडि' if shift > 0 else 'पछाडि'
        em.emit(EX, 'IQ & Reasoning', 'Coding-Decoding', 'medium', 2,
                f'If {w} is coded as {coded}, how is {w2} coded?',
                f'यदि {w} लाई {coded} भनेर कोड गरियो भने {w2} लाई कसरी कोड गरिन्छ?',
                opts, optsn, a,
                f'Each letter shifts {abs(shift)} step(s) {direction}: {w2} becomes {coded2}.',
                f'प्रत्येक अक्षर {dev_num(abs(shift))} कदम {dn} सर्छ: {w2} बाट {coded2} हुन्छ।')

# ---------------- 3. Coding: A=1 ... Z=26 sums ----------------
for w in WORDS:
    val = sum(ord(c) - 64 for c in w)
    w2 = rng.choice([x for x in WORDS if x != w])
    v2 = sum(ord(c) - 64 for c in w2)
    ds = [v2 + len(w2), v2 - len(w2), v2 + 5, v2 * 2]
    opts = [str(v2)] + [str(d) for d in ds if d != v2 and d > 0][:3]
    while len(opts) < 4:
        opts.append(str(v2 + len(opts) + 3))
    optsn = [dev_num(x) for x in opts]
    em.emit(EX, 'IQ & Reasoning', 'Coding-Decoding', 'medium', 2,
            f'If {w} is coded as {val} (A=1, B=2, ..., Z=26), what is the code for {w2}?',
            f'यदि {w} लाई {dev_num(val)} भनेर कोड गरियो (A=१, B=२, ..., Z=२६) भने {w2} को कोड कति हो?',
            opts, optsn, 0,
            f'Add the letter values: {"+".join(str(ord(c) - 64) for c in w2)} = {v2}.',
            f'अक्षरहरूको मान जोड्नुहोस्: {"+".join(dev_num(ord(c) - 64) for c in w2)} = {dev_num(v2)}।')

# ---------------- 4. Odd one out (numbers) ----------------
def odd_q(nums, odd, reason_en, reason_ne, sub):
    opts = [str(x) for x in nums]
    optsn = [dev_num(x) for x in nums]
    em.emit(EX, 'IQ & Reasoning', 'Odd One Out', 'medium', 2,
            f'Find the odd one out: {", ".join(opts)}.',
            f'बेग्लै सङ्ख्या पत्ता लगाउनुहोस्: {", ".join(optsn)}।',
            opts, optsn, nums.index(odd),
            reason_en, reason_ne)
for _ in range(250):
    base = rng.choice([2, 3, 4, 5, 6, 7, 8, 10])
    mults = [base * i for i in rng.sample(range(2, 15), 3)]
    odd = rng.choice([x for x in range(11, 99) if x % base != 0])
    nums = mults + [odd]
    rng.shuffle(nums)
    odd_q(nums, odd,
          f'All the others are multiples of {base}; {odd} is not.',
          f'अरू सबै {dev_num(base)} का गुणन हुन्; {dev_num(odd)} होइन।', 'numbers')
for _ in range(200):
    sqs = [(n * n) for n in rng.sample(range(3, 16), 3)]
    odd = rng.choice([x for x in range(10, 99) if int(x ** 0.5) ** 2 != x])
    nums = sqs + [odd]
    rng.shuffle(nums)
    odd_q(nums, odd,
          f'All the others are perfect squares; {odd} is not.',
          f'अरू सबै पूर्ण वर्ग हुन्; {dev_num(odd)} होइन।', 'numbers')
for _ in range(150):
    evens = [2 * n for n in rng.sample(range(5, 40), 3)]
    odd = rng.choice([x for x in range(11, 99, 2)])
    nums = evens + [odd]
    rng.shuffle(nums)
    odd_q(nums, odd,
          f'All the others are even numbers; {odd} is odd.',
          f'अरू सबै जोर सङ्ख्या हुन्; {dev_num(odd)} बिजोर हो।', 'numbers')
for _ in range(150):
    pr = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    ps = rng.sample(pr, 3)
    odd = rng.choice([x for x in range(12, 60) if x not in pr])
    nums = ps + [odd]
    rng.shuffle(nums)
    odd_q(nums, odd,
          f'All the others are prime numbers; {odd} is not prime.',
          f'अरू सबै अभाज्य सङ्ख्या हुन्; {dev_num(odd)} अभाज्य होइन।', 'numbers')

# ---------------- 5. Alphabet positions ----------------
for _ in range(300):
    n = rng.randint(1, 26)
    letter = L(n - 1)
    frm = rng.choice(['left', 'right'])
    if frm == 'left':
        opts = [letter, L(n), L(n - 2), L(n + 1)]
        opts = [o for o in opts if o]
        opts = list(dict.fromkeys(opts))
        while len(opts) < 4:
            opts.append(L(rng.randint(0, 25)))
        em.emit(EX, 'IQ & Reasoning', 'Alphabet', 'easy', 1,
                f'Which letter is {n}{"st" if n == 1 else "nd" if n == 2 else "rd" if n == 3 else "th"} from the left in the English alphabet?',
                f'अङ्ग्रेजी वर्णमालामा बायाँबाट {dev_num(n)}औँ अक्षर कुन हो?',
                opts, opts, 0,
                f'Counting from the left, the {ord_s(n)} letter is {letter}.',
                f'बायाँबाट गन्दा {dev_num(n)}औँ अक्षर {letter} हो।')
    else:
        letter = L(26 - n)
        opts = [letter, L(26 - n - 1), L(26 - n + 1), L(26 - n - 2)]
        opts = [o for o in opts if o]
        opts = list(dict.fromkeys(opts))
        while len(opts) < 4:
            opts.append(L(rng.randint(0, 25)))
        em.emit(EX, 'IQ & Reasoning', 'Alphabet', 'easy', 1,
                f'Which letter is {n}{"st" if n == 1 else "nd" if n == 2 else "rd" if n == 3 else "th"} from the right in the English alphabet?',
                f'अङ्ग्रेजी वर्णमालामा दायाँबाट {dev_num(n)}औँ अक्षर कुन हो?',
                opts, opts, 0,
                f'Counting from the right, the {ord_s(n)} letter is {letter}.',
                f'दायाँबाट गन्दा {dev_num(n)}औँ अक्षर {letter} हो।')
# letter between two letters
for _ in range(200):
    a = rng.randint(0, 23)
    b = a + rng.choice([2, 3, 4])
    mid = L((a + b) // 2) if (a + b) % 2 == 0 else None
    if mid is None:
        continue
    opts = [mid, L(a + 1), L(b - 1), L(a)]
    opts = list(dict.fromkeys(opts))
    while len(opts) < 4:
        opts.append(L(rng.randint(0, 25)))
    em.emit(EX, 'IQ & Reasoning', 'Alphabet', 'medium', 1,
            f'Which letter is exactly in the middle of {L(a)} and {L(b)} in the English alphabet?',
            f'अङ्ग्रेजी वर्णमालामा {L(a)} र {L(b)} को ठीक बीचमा कुन अक्षर छ?',
            opts, opts, 0,
            f'The letter midway between {L(a)} and {L(b)} is {mid}.',
            f'{L(a)} र {L(b)} को बीचमा {mid} अक्षर पर्छ।')

# ---------------- 6. Blood relations ----------------
MALE = ['Ram', 'Hari', 'Shyam', 'Gopal', 'Binod', 'Suresh', 'Ramesh', 'Dipak', 'Anil', 'Kiran']
FEMALE = ['Sita', 'Gita', 'Maya', 'Rita', 'Sunita', 'Kamala', 'Laxmi', 'Nirmala', 'Pooja', 'Sapana']
for _ in range(260):
    kind = rng.choice(['son', 'daughter', 'brother', 'sister'])
    if kind in ('son', 'brother'):
        a = rng.choice(MALE)
    else:
        a = rng.choice(FEMALE)
    b = rng.choice(FEMALE)
    if kind == 'son':
        q = f'{a} is the son of {b}. How is {b} related to {a}?'
        qn = f'{a} {b} का छोरा हुन्। {b} {a} का को हुन्?'
        ans, ansn = 'Mother', 'आमा'
        ds, dsn = ['Sister', 'Aunt', 'Grandmother'], ['बहिनी', 'फुपू', 'हजुरआमा']
    elif kind == 'daughter':
        q = f'{a} is the daughter of {b}. How is {b} related to {a}?'
        qn = f'{a} {b} की छोरी हुन्। {b} {a} का को हुन्?'
        ans, ansn = 'Mother', 'आमा'
        ds, dsn = ['Sister', 'Aunt', 'Grandmother'], ['बहिनी', 'फुपू', 'हजुरआमा']
    elif kind == 'brother':
        q = f'{a} is the brother of {b}. How is {a} related to {b}?'
        qn = f'{a} {b} का भाइ हुन्। {a} {b} का को हुन्?'
        ans, ansn = 'Brother', 'भाइ'
        ds, dsn = ['Father', 'Uncle', 'Cousin'], ['बुबा', 'काका', 'काका-भाइ']
    else:
        q = f'{a} is the sister of {b}. How is {a} related to {b}?'
        qn = f'{a} {b} की बहिनी हुन्। {a} {b} का को हुन्?'
        ans, ansn = 'Sister', 'बहिनी'
        ds, dsn = ['Mother', 'Aunt', 'Cousin'], ['आमा', 'फुपू', 'काकी-बहिनी']
    opts = [ans] + ds
    optsn = [ansn] + dsn
    em.emit(EX, 'IQ & Reasoning', 'Blood Relations', 'easy', 1, q, qn, opts, optsn, 0,
            f'{ans} is the correct relation.',
            f'{ansn} सही सम्बन्ध हो।')
for _ in range(200):
    a = rng.choice(MALE)
    b = rng.choice(MALE)
    if a == b:
        continue
    q = f'{a} is the father of {b}. {b} is the brother of C. How is {a} related to C?'
    qn = f'{a} {b} का बुबा हुन्। {b} C का भाइ हुन्। {a} C का को हुन्?'
    opts = ['Father', 'Uncle', 'Grandfather', 'Brother']
    optsn = ['बुबा', 'काका', 'हजुरबुबा', 'भाइ']
    em.emit(EX, 'IQ & Reasoning', 'Blood Relations', 'medium', 2, q, qn, opts, optsn, 0,
            f'{a} is the father of {b}, and {b} is the brother of C, so {a} is also the father of C.',
            f'{a} {b} का बुबा हुन् र {b} C का भाइ हुन्, त्यसैले {a} C का पनि बुबा हुन्।')
for _ in range(150):
    a = rng.choice(FEMALE)
    b = rng.choice(MALE)
    q = f'{a} is the mother of {b}. {b} is the father of C. How is {a} related to C?'
    qn = f'{a} {b} की आमा हुन्। {b} C का बुबा हुन्। {a} C का को हुन्?'
    opts = ['Grandmother', 'Mother', 'Aunt', 'Sister']
    optsn = ['हजुरआमा', 'आमा', 'फुपू', 'बहिनी']
    em.emit(EX, 'IQ & Reasoning', 'Blood Relations', 'medium', 2, q, qn, opts, optsn, 0,
            f'{a} is the mother of {b} and {b} is the father of C, so {a} is the grandmother of C.',
            f'{a} {b} की आमा हुन् र {b} C का बुबा हुन्, त्यसैले {a} C की हजुरआमा हुन्।')

# ---------------- 7. Direction sense ----------------
DIRS = [('north', 'उत्तर'), ('south', 'दक्षिण'), ('east', 'पूर्व'), ('west', 'पश्चिम')]
for _ in range(300):
    d1, d1n = rng.choice(DIRS)
    dist1 = rng.choice([2, 3, 4, 5, 6, 8, 10])
    turn = rng.choice(['left', 'right'])
    turnn = 'बायाँ' if turn == 'left' else 'दायाँ'
    dist2 = rng.choice([2, 3, 4, 5, 6, 8, 10])
    # start facing d1, turn left/right -> new facing
    order = ['north', 'east', 'south', 'west']
    i = order.index(d1)
    j = (i - 1) % 4 if turn == 'left' else (i + 1) % 4
    d2 = order[j]
    d2n = dict(DIRS)[d2]
    # final position relative to start: displacement
    vec = {'north': (0, 1), 'south': (0, -1), 'east': (1, 0), 'west': (-1, 0)}
    x = vec[d1][0] * dist1 + vec[d2][0] * dist2
    y = vec[d1][1] * dist1 + vec[d2][1] * dist2
    if x == 0 and y == 0:
        continue
    if x > 0 and y > 0:
        final, finaln = 'north-east', 'उत्तर-पूर्व'
    elif x > 0 and y < 0:
        final, finaln = 'south-east', 'दक्षिण-पूर्व'
    elif x < 0 and y > 0:
        final, finaln = 'north-west', 'उत्तर-पश्चिम'
    elif x < 0 and y < 0:
        final, finaln = 'south-west', 'दक्षिण-पश्चिम'
    elif x > 0:
        final, finaln = 'east', 'पूर्व'
    elif x < 0:
        final, finaln = 'west', 'पश्चिम'
    elif y > 0:
        final, finaln = 'north', 'उत्तर'
    else:
        final, finaln = 'south', 'दक्षिण'
    others = [d for d in ['north', 'south', 'east', 'west', 'north-east', 'south-east', 'north-west', 'south-west'] if d != final]
    rng.shuffle(others)
    ds = others[:3]
    dsn = [dict(DIRS + [('north-east', 'उत्तर-पूर्व'), ('south-east', 'दक्षिण-पूर्व'), ('north-west', 'उत्तर-पश्चिम'), ('south-west', 'दक्षिण-पश्चिम')])[d] for d in ds]
    opts = [final] + ds
    optsn = [finaln] + dsn
    em.emit(EX, 'IQ & Reasoning', 'Direction Sense', 'medium', 2,
            f'A person walks {dist1} km towards the {d1}, then turns {turn} and walks {dist2} km. In which direction is he now from the starting point?',
            f'एक व्यक्ति {d1n} तर्फ {dev_num(dist1)} किमी हिँड्छ, त्यसपछि {turnn} मोडिएर {dev_num(dist2)} किमी हिँड्छ। ऊ सुरुको ठाउँबाट कुन दिशामा छ?',
            opts, optsn, 0,
            f'After walking {dist1} km {d1} and {dist2} km {d2}, the person is to the {final} of the starting point.',
            f'{dev_num(dist1)} किमी {d1n} र {dev_num(dist2)} किमी {d2n} हिँडेपछि व्यक्ति सुरुको ठाउँको {finaln} दिशामा छ।')

# ---------------- 8. Ranking ----------------
for _ in range(250):
    n = rng.randint(15, 40)
    pos = rng.randint(2, n - 1)
    from_end = n - pos + 1
    q = f'In a row of {n} students, Ram is {ord_s(pos)} from the left. What is his position from the right?'
    qn = f'{dev_num(n)} जना विद्यार्थीको लहरमा राम बायाँबाट {dev_num(pos)}औँ छन्। दायाँबाट उनको स्थान कति हो?'
    opts = [str(from_end), str(pos), str(from_end + 1), str(from_end - 1)]
    optsn = [dev_num(x) for x in opts]
    em.emit(EX, 'IQ & Reasoning', 'Ranking', 'medium', 2, q, qn, opts, optsn, 0,
            f'Position from the right = {n} - {pos} + 1 = {from_end}.',
            f'दायाँबाट स्थान = {dev_num(n)} − {dev_num(pos)} + १ = {dev_num(from_end)}।')

# ---------------- 9. Analogies (curated pairs) ----------------
PAIRS = [
    ('Doctor', 'Hospital', 'Teacher', 'School', 'डाक्टर', 'अस्पताल', 'शिक्षक', 'विद्यालय'),
    ('Bird', 'Nest', 'Bee', 'Hive', 'चरा', 'गुँड', 'माहुरी', 'घार'),
    ('Fish', 'Water', 'Bird', 'Air', 'माछा', 'पानी', 'चरा', 'हावा'),
    ('Book', 'Read', 'Pen', 'Write', 'पुस्तक', 'पढ्नु', 'कलम', 'लेख्नु'),
    ('Sun', 'Day', 'Moon', 'Night', 'सूर्य', 'दिन', 'चन्द्रमा', 'रात'),
    ('King', 'Palace', 'Farmer', 'Field', 'राजा', 'दरबार', 'किसान', 'खेत'),
    ('Cow', 'Milk', 'Hen', 'Egg', 'गाई', 'दूध', 'कुखुरा', 'अण्डा'),
    ('Knife', 'Cut', 'Needle', 'Sew', 'चक्कु', 'काट्नु', 'सियो', 'सिउनु'),
    ('Water', 'Thirst', 'Food', 'Hunger', 'पानी', 'तिर्खा', 'खाना', 'भोक'),
    ('Clock', 'Time', 'Thermometer', 'Temperature', 'घडी', 'समय', 'थर्मोमिटर', 'तापक्रम'),
    ('Author', 'Book', 'Painter', 'Painting', 'लेखक', 'पुस्तक', 'चित्रकार', 'चित्र'),
    ('Tailor', 'Cloth', 'Carpenter', 'Wood', 'दर्जी', 'कपडा', 'सिकर्मी', 'काठ'),
    ('Seed', 'Plant', 'Egg', 'Bird', 'बीउ', 'बिरुवा', 'अण्डा', 'चरा'),
    ('Lion', 'Den', 'Horse', 'Stable', 'सिंह', 'ओडार', 'घोडा', 'अस्तबल'),
    ('Spider', 'Web', 'Bird', 'Nest', 'माकुरा', 'जालो', 'चरा', 'गुँड'),
    ('Iron', 'Hard', 'Cotton', 'Soft', 'फलाम', 'कडा', 'कपास', 'नरम'),
    ('Rain', 'Umbrella', 'Sun', 'Sunglasses', 'वर्षा', 'छाता', 'घाम', 'चस्मा'),
    ('Shoes', 'Feet', 'Gloves', 'Hands', 'जुत्ता', 'खुट्टा', 'पन्जा', 'हात'),
    ('Teacher', 'Student', 'Doctor', 'Patient', 'शिक्षक', 'विद्यार्थी', 'डाक्टर', 'बिरामी'),
    ('Wheel', 'Car', 'Wing', 'Bird', 'पाङ्ग्रा', 'गाडी', 'पखेटा', 'चरा'),
]
DISTRACT_POOL = ['School', 'Hospital', 'River', 'Mountain', 'Book', 'Pen', 'Garden', 'Kitchen', 'Field', 'Stable', 'Nest', 'Hive', 'Water', 'Fire', 'Sky', 'Ground']
POOL_NE = {'School': 'विद्यालय', 'Hospital': 'अस्पताल', 'River': 'नदी', 'Mountain': 'पहाड', 'Book': 'पुस्तक', 'Pen': 'कलम', 'Garden': 'बगैँचा', 'Kitchen': 'भान्सा', 'Field': 'खेत', 'Stable': 'अस्तबल', 'Nest': 'गुँड', 'Hive': 'घार', 'Water': 'पानी', 'Fire': 'आगो', 'Sky': 'आकाश', 'Ground': 'मैदान'}
for (a, b, c, d, an, bn, cn, dn) in PAIRS:
    ds = [x for x in DISTRACT_POOL if x not in (b, d)]
    rng.shuffle(ds)
    ds = ds[:3]
    opts = [d] + ds
    optsn = [dn] + [POOL_NE[x] for x in ds]
    em.emit(EX, 'IQ & Reasoning', 'Analogies', 'easy', 1,
            f'{a} is to {b} as {c} is to ____.',
            f'{an} को {bn} सँग जस्तो सम्बन्ध छ, {cn} को ____ सँग त्यस्तै सम्बन्ध छ।',
            opts, optsn, 0,
            f'{a} is associated with {b}, just as {c} is associated with {d}.',
            f'{an} {bn} सँग सम्बन्धित छ, त्यसैगरी {cn} {dn} सँग सम्बन्धित छ।')
    # reverse direction
    ds2 = [x for x in DISTRACT_POOL if x not in (a, c)]
    rng.shuffle(ds2)
    ds2 = ds2[:3]
    opts = [c] + ds2
    optsn = [cn] + [POOL_NE[x] for x in ds2]
    em.emit(EX, 'IQ & Reasoning', 'Analogies', 'medium', 1,
            f'{b} is to {a} as {d} is to ____.',
            f'{bn} को {an} सँग जस्तो सम्बन्ध छ, {dn} को ____ सँग त्यस्तै सम्बन्ध छ।',
            opts, optsn, 0,
            f'{b} belongs to {a}, just as {d} belongs to {c}.',
            f'{bn} {an} को हो, त्यसैगरी {dn} {cn} को हो।')

# ---------------- 10. Seating (linear, computed) ----------------
for _ in range(200):
    n = rng.choice([5, 6, 7])
    names = ['A', 'B', 'C', 'D', 'E', 'F', 'G'][:n]
    order = names[:]
    rng.shuffle(order)
    pos = rng.randint(0, n - 1)
    who = order[pos]
    q = f'{n} people sit in a row in the order: {", ".join(order)} (left to right). Who is {pos + 1}{"st" if pos == 0 else "nd" if pos == 1 else "rd" if pos == 2 else "th"} from the left?'
    qn = f'{dev_num(n)} जना लहरमा यस क्रममा बसेका छन्: {", ".join(order)} (बायाँदेखि दायाँ)। बायाँबाट {dev_num(pos + 1)}औँ को हुन्?'
    ds = [x for x in names if x != who]
    rng.shuffle(ds)
    opts = [who] + ds[:3]
    em.emit(EX, 'IQ & Reasoning', 'Seating Arrangement', 'medium', 2, q, qn, opts, opts, 0,
            f'Counting from the left, position {pos + 1} is {who}.',
            f'बायाँबाट गन्दा {dev_num(pos + 1)}औँ स्थानमा {who} छन्।')
    # neighbour question
    if 0 < pos < n - 1:
        left, right = order[pos - 1], order[pos + 1]
        q2 = f'In the row {", ".join(order)} (left to right), who sits immediately to the right of {who}?'
        q2n = f'{", ".join(order)} (बायाँदेखि दायाँ) को लहरमा {who} को ठीक दायाँ को बसेको छ?'
        ds = [x for x in names if x != right]
        rng.shuffle(ds)
        opts = [right] + ds[:3]
        em.emit(EX, 'IQ & Reasoning', 'Seating Arrangement', 'medium', 2, q2, q2n, opts, opts, 0,
                f'Immediately to the right of {who} is {right}.',
                f'{who} को ठीक दायाँ {right} छन्।')

# ---------------- 11. Counting letters ----------------
for w in WORDS:
    for letter in set(w):
        cnt = w.count(letter)
        if cnt < 2:
            continue
        opts = [str(cnt), str(cnt + 1), str(cnt - 1), str(cnt + 2)]
        optsn = [dev_num(x) for x in opts]
        em.emit(EX, 'IQ & Reasoning', 'Counting', 'easy', 1,
                f'How many times does the letter {letter} appear in the word {w}?',
                f'{w} शब्दमा {letter} अक्षर कति पटक आएको छ?',
                opts, optsn, 0,
                f'The letter {letter} appears {cnt} times in {w}.',
                f'{letter} अक्षर {w} शब्दमा {dev_num(cnt)} पटक आएको छ।')

n = em.write('expansion-r10-iq.json')
print('IQ TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:10]:
    print('  REJ', r)
