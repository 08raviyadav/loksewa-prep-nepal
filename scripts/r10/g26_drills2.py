#!/usr/bin/env python3
"""R10 generator 26: Drills 2 (~1,700). Fresh drill spaces: 3x2 multiplication,
4x1 multiplication, 3-digit division, squares 31-50, cubes 11-15, Roman 101-399,
Nepali number words 101-200, time/length/weight conversions, fraction of fraction,
decimal multiply/divide, LCM/HCF bigger pairs, sums 101-200, primes 100-200,
divisibility by 6/8/9/11, factor counts, small % values."""
import sys, random, math
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num

bank = Bank()
em = Emitter(bank, 'R10-DR2')
rng = random.Random(31337)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'tsc-primary', 'tsc-secondary']

def q_emit(topic, diff, marks, q, qn, opts, optn, ans, exp, expn):
    em.emit(EX, 'Maths & Numerical', topic, diff, marks, q, qn, opts, optn, ans, exp, expn)

def num_opts(ans, lo, hi, step=1):
    s = {ans}
    while len(s) < 4:
        v = rng.randrange(lo, hi+1, step)
        if v != ans and v >= 0: s.add(v)
    o = list(s); rng.shuffle(o)
    return o, o.index(ans)

def arith(q, qn, ans, exp, expn, topic='Arithmetic', diff='easy', marks=1, spread=10):
    o, ai = num_opts(ans, max(0, ans-spread), ans+spread, 1)
    q_emit(topic, diff, marks, q, qn, [str(x) for x in o], [dev_num(x) for x in o], ai, exp, expn)

# ---------- 3-digit x 2-digit multiplication ----------
for _ in range(120):
    a = rng.randrange(102, 999); b = rng.randrange(12, 99)
    ans = a * b
    arith(f"What is {a} x {b}?", f"{a} × {b} कति हो?", ans,
          f"{a} x {b} = {ans}.", f"{a} × {b} = {ans} हो।", spread=200)

# ---------- 4-digit x 1-digit ----------
for _ in range(80):
    a = rng.randrange(1002, 9999); b = rng.randrange(2, 10)
    ans = a * b
    arith(f"What is {a} x {b}?", f"{a} × {b} कति हो?", ans,
          f"{a} x {b} = {ans}.", f"{a} × {b} = {ans} हो।", spread=500)

# ---------- 3-digit division (exact) ----------
for _ in range(120):
    b = rng.randrange(3, 30)
    ans = rng.randrange(11, 90)
    a = b * ans
    if a < 100 or a > 999: continue
    arith(f"What is {a} / {b}?", f"{a} ÷ {b} कति हो?", ans,
          f"{a} / {b} = {ans}.", f"{a} ÷ {b} = {ans} हो।", spread=8)

# ---------- 3-digit addition/subtraction ----------
for _ in range(100):
    a = rng.randrange(101, 999); b = rng.randrange(101, 999)
    if rng.random() < 0.5:
        ans = a + b
        arith(f"What is {a} + {b}?", f"{a} + {b} कति हो?", ans,
              f"{a} + {b} = {ans}.", f"{a} + {b} = {ans} हो।", spread=50)
    else:
        if a < b: a, b = b, a
        ans = a - b
        arith(f"What is {a} - {b}?", f"{a} - {b} कति हो?", ans,
              f"{a} - {b} = {ans}.", f"{a} - {b} = {ans} हो।", spread=50)

# ---------- squares 31-50 ----------
for n in range(31, 51):
    for _ in range(4):
        ans = n * n
        o, ai = num_opts(ans, max(1, ans-100), ans+100, 10)
        q_emit('Squares & Cubes', 'medium', 1,
            f"What is the square of {n}?", f"{n} को वर्ग कति हो?",
            [str(x) for x in o], [dev_num(x) for x in o], ai,
            f"{n}^2 = {n} x {n} = {ans}.", f"{n}² = {n} × {n} = {ans} हो।")

# ---------- cubes 11-15 ----------
for n in range(11, 16):
    for _ in range(4):
        ans = n ** 3
        o, ai = num_opts(ans, max(1, ans-200), ans+200, 10)
        q_emit('Squares & Cubes', 'medium', 1,
            f"What is the cube of {n}?", f"{n} को घन कति हो?",
            [str(x) for x in o], [dev_num(x) for x in o], ai,
            f"{n}^3 = {n} x {n} x {n} = {ans}.", f"{n}³ = {n} × {n} × {n} = {ans} हो।")

# ---------- Roman numerals 101-399 ----------
def to_roman(n):
    vals = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    out = ''
    for v, s in vals:
        while n >= v:
            out += s; n -= v
    return out
for _ in range(100):
    n = rng.randrange(101, 400)
    r = to_roman(n)
    others = set()
    while len(others) < 3:
        m = rng.randrange(101, 400)
        if m != n: others.add(to_roman(m))
    o = [r] + list(others); rng.shuffle(o)
    q_emit('Roman Numerals', 'medium', 1,
        f"What is {n} in Roman numerals?", f"{n} लाई रोमन अङ्कमा कसरी लेखिन्छ?",
        o, o, o.index(r),
        f"{n} in Roman numerals is {r}.", f"{n} को रोमन अङ्क {r} हो।")
for _ in range(60):
    n = rng.randrange(101, 400)
    r = to_roman(n)
    others = set()
    while len(others) < 3:
        m = rng.randrange(101, 400)
        if m != n: others.add(m)
    o = [n] + list(others); rng.shuffle(o)
    q_emit('Roman Numerals', 'medium', 1,
        f"What is the value of the Roman numeral {r}?", f"रोमन अङ्क {r} को मान कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], o.index(n),
        f"The Roman numeral {r} equals {n}.", f"रोमन अङ्क {r} को मान {n} हो।")

# ---------- Nepali number words 101-200 ----------
NE_WORDS = {101: 'एक सय एक', 105: 'एक सय पाँच', 110: 'एक सय दस', 115: 'एक सय पन्ध्र', 120: 'एक सय बीस', 125: 'एक सय पच्चीस', 130: 'एक सय तीस', 140: 'एक सय चालीस', 150: 'एक सय पचास', 160: 'एक सय साठी', 170: 'एक सय सत्तरी', 180: 'एक सय असी', 190: 'एक सय नब्बे', 200: 'दुई सय', 111: 'एक सय एघार', 121: 'एक सय एक्काइस', 131: 'एक सय एक्तीस', 141: 'एक सय एकचालीस', 151: 'एक सय एकाउन्न', 161: 'एक सय एकसठ्ठी', 171: 'एक सय एकहत्तर', 181: 'एक सय एकासी', 191: 'एक सय एकानब्बे', 199: 'एक सय उनान्सय'}
for n, w in NE_WORDS.items():
    others = [x for x in NE_WORDS.values() if x != w]
    rng.shuffle(others)
    ds = others[:3]
    o = [w] + ds; rng.shuffle(o)
    q_emit('Nepali Numbers', 'easy', 1,
        f"How is {n} written in Nepali words?", f"{n} लाई नेपाली शब्दमा कसरी लेखिन्छ?",
        o, o, o.index(w),
        f"{n} in Nepali words is '{w}'.", f"{n} को नेपाली शब्द '{w}' हो।")

# ---------- time conversions ----------
for _ in range(60):
    h = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 24, 48])
    ans = h * 60
    o, ai = num_opts(ans, max(1, ans-60), ans+60, 30)
    q_emit('Units & Measurement', 'easy', 1,
        f"How many minutes are there in {h} hours?", f"{h} घण्टामा कति मिनेट हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"{h} hours = {h} x 60 = {ans} minutes.", f"{h} घण्टा = {h} × ६० = {ans} मिनेट हो।")
for _ in range(60):
    m = rng.choice([120, 180, 240, 300, 360, 480, 600, 720, 900, 1200])
    ans = m // 60
    o, ai = num_opts(ans, max(1, ans-5), ans+5, 1)
    q_emit('Units & Measurement', 'easy', 1,
        f"How many hours are there in {m} minutes?", f"{m} मिनेटमा कति घण्टा हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"{m} minutes = {m} / 60 = {ans} hours.", f"{m} मिनेट = {m} / ६० = {ans} घण्टा हो।")

# ---------- length conversions ----------
for _ in range(60):
    km = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20])
    ans = km * 1000
    o, ai = num_opts(ans, max(100, ans-1000), ans+1000, 500)
    q_emit('Units & Measurement', 'easy', 1,
        f"How many metres are there in {km} kilometres?", f"{km} किलोमिटरमा कति मिटर हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"{km} km = {km} x 1000 = {ans} m.", f"{km} किमी = {km} × १००० = {ans} मिटर हो।")
for _ in range(60):
    m = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 50])
    ans = m * 100
    o, ai = num_opts(ans, max(10, ans-100), ans+100, 50)
    q_emit('Units & Measurement', 'easy', 1,
        f"How many centimetres are there in {m} metres?", f"{m} मिटरमा कति सेन्टिमिटर हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"{m} m = {m} x 100 = {ans} cm.", f"{m} मिटर = {m} × १०० = {ans} सेमी हो।")

# ---------- weight conversions ----------
for _ in range(60):
    kg = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25])
    ans = kg * 1000
    o, ai = num_opts(ans, max(100, ans-1000), ans+1000, 500)
    q_emit('Units & Measurement', 'easy', 1,
        f"How many grams are there in {kg} kilograms?", f"{kg} किलोग्राममा कति ग्राम हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"{kg} kg = {kg} x 1000 = {ans} g.", f"{kg} किग्रा = {kg} × १००० = {ans} ग्राम हो।")
for _ in range(40):
    q = rng.choice([2, 3, 4, 5, 6, 8, 10])
    ans = q * 100
    o, ai = num_opts(ans, max(50, ans-100), ans+100, 50)
    q_emit('Units & Measurement', 'medium', 1,
        f"How many kilograms are there in {q} quintals?", f"{q} क्विन्टलमा कति किलोग्राम हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"1 quintal = 100 kg, so {q} quintals = {q} x 100 = {ans} kg.",
        f"१ क्विन्टल = १०० किग्रा हो, त्यसैले {q} क्विन्टल = {q} × १०० = {ans} किग्रा हो।")

# ---------- fraction of a fraction ----------
for _ in range(80):
    a, b = rng.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (1, 5), (4, 5)])
    c, d = rng.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)])
    n = rng.choice([60, 120, 180, 240, 300, 360, 480, 600])
    if n * a % b or (n * a // b) * c % d: continue
    ans = (n * a // b) * c // d
    o, ai = num_opts(ans, max(1, ans-20), ans+20, 5)
    q_emit('Fractions', 'medium', 1,
        f"What is {c}/{d} of {a}/{b} of {n}?", f"{n} को {a}/{b} को {c}/{d} कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"{a}/{b} of {n} = {n*a//b}. {c}/{d} of {n*a//b} = {ans}.",
        f"{n} को {a}/{b} = {n*a//b} हो। {n*a//b} को {c}/{d} = {ans} हो।")

# ---------- decimal multiplication ----------
for _ in range(80):
    a = rng.choice([1.2, 1.5, 2.4, 2.5, 3.6, 4.5, 0.6, 0.8, 1.8, 2.2, 3.3, 5.5])
    b = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    ans = round(a * b, 2)
    if ans != int(ans):
        o = [ans, round(ans+1, 2), round(ans-1, 2), round(ans+2, 2)]
        o = [x for x in o if x > 0]
        if len(set(o)) < 4: continue
        rng.shuffle(o)
        q_emit('Decimals', 'medium', 1,
            f"What is {a} x {b}?", f"{a} × {b} कति हो?",
            [str(x) for x in o], [dev_num(x) for x in o], o.index(ans),
            f"{a} x {b} = {ans}.", f"{a} × {b} = {ans} हो।")
    else:
        arith(f"What is {a} x {b}?", f"{a} × {b} कति हो?", int(ans),
              f"{a} x {b} = {ans}.", f"{a} × {b} = {ans} हो।", topic='Decimals', diff='medium', spread=5)

# ---------- LCM/HCF bigger pairs ----------
for _ in range(80):
    a = rng.randrange(12, 60); b = rng.randrange(12, 60)
    if a == b: continue
    ans = math.lcm(a, b)
    if ans > 600: continue
    o, ai = num_opts(ans, max(1, ans-60), ans+60, 6)
    q_emit('HCF & LCM', 'medium', 1,
        f"What is the LCM of {a} and {b}?", f"{a} र {b} को लस कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"LCM of {a} and {b} = {ans}.", f"{a} र {b} को लस {ans} हो।")
for _ in range(80):
    a = rng.randrange(24, 120); b = rng.randrange(24, 120)
    if a == b: continue
    ans = math.gcd(a, b)
    if ans < 2: continue
    o, ai = num_opts(ans, 1, ans+12, 1)
    q_emit('HCF & LCM', 'medium', 1,
        f"What is the HCF of {a} and {b}?", f"{a} र {b} को मस कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"HCF of {a} and {b} = {ans}.", f"{a} र {b} को मस {ans} हो।")

# ---------- sums 101-200 ----------
for _ in range(80):
    n = rng.randrange(101, 201)
    ans = n * (n + 1) // 2
    o, ai = num_opts(ans, max(1, ans-500), ans+500, 100)
    q_emit('Number System', 'medium', 1,
        f"What is the sum of the first {n} natural numbers?", f"पहिलो {n} वटा प्राकृतिक सङ्ख्याहरूको योग कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Sum = {n}x{n+1}/2 = {ans}.", f"योग = {n}×{n+1}/२ = {ans} हो।")

# ---------- primes 100-200: is it prime? ----------
PRIMES_100_200 = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
for p in PRIMES_100_200:
    for _ in range(3):
        others = [x for x in range(100, 201) if x not in PRIMES_100_200]
        rng.shuffle(others)
        ds = others[:3]
        o = [p] + ds; rng.shuffle(o)
        q_emit('Number System', 'medium', 1,
            f"Which of the following is a prime number?", f"तलकामध्ये कुन अभाज्य सङ्ख्या हो?",
            [str(x) for x in o], [dev_num(x) for x in o], o.index(p),
            f"{p} is a prime number (divisible only by 1 and itself).",
            f"{p} अभाज्य सङ्ख्या हो (१ र आफैँबाहेक अरूले भाग जाँदैन)।")

# ---------- divisibility by 6, 8, 9, 11 ----------
for d, rule in [(6, 'divisible by both 2 and 3'), (9, 'digit sum divisible by 9'), (8, 'last three digits divisible by 8'), (11, 'alternating digit sum difference divisible by 11')]:
    for _ in range(40):
        # pick a multiple of d in 100-999
        m = rng.randrange(100, 1000)
        m = (m // d) * d
        if m < 100: continue
        others = set()
        while len(others) < 3:
            v = rng.randrange(100, 1000)
            if v % d != 0: others.add(v)
        o = [m] + list(others); rng.shuffle(o)
        q_emit('Number System', 'medium', 1,
            f"Which of the following is divisible by {d}?", f"तलकामध्ये कुन {d} ले भाग जान्छ?",
            [str(x) for x in o], [dev_num(x) for x in o], o.index(m),
            f"{m} / {d} = {m//d}, so {m} is divisible by {d}.",
            f"{m} / {d} = {m//d} हो, त्यसैले {m}, {d} ले भाग जान्छ।")

# ---------- number of factors ----------
for _ in range(60):
    n = rng.choice([12, 16, 18, 20, 24, 30, 36, 40, 48, 60, 72, 80, 96, 100])
    facs = [i for i in range(1, n+1) if n % i == 0]
    ans = len(facs)
    o, ai = num_opts(ans, 2, ans+8, 1)
    q_emit('Number System', 'hard', 2,
        f"How many factors does {n} have?", f"{n} का कति वटा गुणनखण्ड (factors) छन्?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Factors of {n}: {', '.join(str(f) for f in facs)}. Count = {ans}.",
        f"{n} का गुणनखण्डहरू: {', '.join(dev_num(f) for f in facs)} हुन्। सङ्ख्या = {ans} हो।")

# ---------- small % values ----------
for _ in range(80):
    n = rng.choice([200, 400, 500, 600, 800, 1000, 1200, 2000, 4000])
    pct = rng.choice([1, 2, 2.5, 5, 7.5])
    ans = n * pct / 100
    if ans != int(ans): continue
    ans = int(ans)
    o, ai = num_opts(ans, max(1, ans-10), ans+10, 5)
    q_emit('Percentages', 'easy', 1,
        f"What is {pct}% of {n}?", f"{n} को {pct}% कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"{pct}% of {n} = {n} x {pct}/100 = {ans}.",
        f"{n} को {pct}% = {n} × {pct}/१०० = {ans} हो।")

n = em.write('expansion-r10-drills2.json')
print('DRILLS2 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
