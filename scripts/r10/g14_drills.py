#!/usr/bin/env python3
"""R10 generator 14: high-volume computed drills (~3,000). Multiplication,
division, addition/subtraction, squares/cubes, roots, Roman numerals, Nepali
number words, days/months, time/length/weight/area conversions, fraction and
decimal arithmetic, LCM/HCF triples, sums, primes, divisibility, factors."""
import sys, random, math
from fractions import Fraction
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num, fmt

bank = Bank()
em = Emitter(bank, 'R10-DRILL')
rng = random.Random(71104)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'police', 'army', 'tsc-primary', 'tsc-secondary']

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

def E(sub, diff, q, qn, o, on, expl, expln):
    em.emit(EX, 'Maths & Numerical', sub, diff, 2, q, qn, o, on, 0, expl, expln)

# ---------- multiplication ----------
for _ in range(120):
    a, b = rng.randint(12, 99), rng.randint(2, 9)
    ans = a*b
    o, on, _ = num_opts(ans, [ans+b, ans-b, ans+10, ans-10])
    E('Multiplication', 'easy', f'What is {a} x {b}?', f'{dev(a)} x {dev(b)} कति हो?',
      o, on, f'{a} x {b} = {ans}.', f'{dev(a)} x {dev(b)} = {dev_num(ans)}।')
for _ in range(200):
    a, b = rng.randint(12, 99), rng.randint(11, 99)
    ans = a*b
    o, on, _ = num_opts(ans, [ans+b, ans-b, ans+100, ans-100])
    E('Multiplication', 'medium', f'What is {a} x {b}?', f'{dev(a)} x {dev(b)} कति हो?',
      o, on, f'{a} x {b} = {ans}.', f'{dev(a)} x {dev(b)} = {dev_num(ans)}।')
for _ in range(100):
    a, b = rng.randint(101, 999), rng.randint(2, 9)
    ans = a*b
    o, on, _ = num_opts(ans, [ans+b, ans-b, ans+100, ans-100])
    E('Multiplication', 'medium', f'What is {a} x {b}?', f'{dev(a)} x {dev(b)} कति हो?',
      o, on, f'{a} x {b} = {ans}.', f'{dev(a)} x {dev(b)} = {dev_num(ans)}।')

# ---------- division exact ----------
for _ in range(120):
    b = rng.randint(3, 25)
    q = rng.randint(11, 99)
    a = b*q
    o, on, _ = num_opts(q, [q+1, q-1, q+10, q-10])
    E('Division', 'easy', f'What is {a} divided by {b}?', f'{dev_num(a)} लाई {dev(b)} ले भाग गर्दा कति हुन्छ?',
      o, on, f'{a} / {b} = {q}.', f'{dev_num(a)} / {dev(b)} = {dev_num(q)}।')
# ---------- division with remainder ----------
for _ in range(120):
    b = rng.randint(3, 12)
    q = rng.randint(5, 40)
    r = rng.randint(1, b-1)
    a = b*q + r
    o, on, _ = num_opts(r, [r+1, r-1, r+2, b-r])
    E('Division', 'medium', f'What is the remainder when {a} is divided by {b}?', f'{dev_num(a)} लाई {dev(b)} ले भाग गर्दा शेष कति हुन्छ?',
      o, on, f'{a} = {b} x {q} + {r}, so the remainder is {r}.', f'{dev_num(a)} = {dev(b)} x {dev(q)} + {dev(r)}, त्यसैले शेष {dev(r)} हो।')

# ---------- addition / subtraction ----------
for _ in range(100):
    a, b = rng.randint(100, 999), rng.randint(100, 999)
    ans = a+b
    o, on, _ = num_opts(ans, [ans+10, ans-10, ans+100, ans-100])
    E('Addition & Subtraction', 'easy', f'What is {a} + {b}?', f'{dev_num(a)} + {dev_num(b)} कति हो?',
      o, on, f'{a} + {b} = {ans}.', f'{dev_num(a)} + {dev_num(b)} = {dev_num(ans)}।')
for _ in range(100):
    a, b = rng.randint(1000, 9999), rng.randint(100, 999)
    ans = a-b
    o, on, _ = num_opts(ans, [ans+10, ans-10, ans+100, ans-100])
    E('Addition & Subtraction', 'easy', f'What is {a} - {b}?', f'{dev_num(a)} - {dev_num(b)} कति हो?',
      o, on, f'{a} - {b} = {ans}.', f'{dev_num(a)} - {dev_num(b)} = {dev_num(ans)}।')

# ---------- squares 1-30 (already in g01? g01 had sqrt/cbrt; squares to 30 may overlap) ----------
for n in range(2, 31):
    ans = n*n
    o, on, _ = num_opts(ans, [ans+n, ans-n, ans+10, ans-10])
    E('Squares & Cubes', 'easy', f'What is the square of {n}?', f'{dev(n)} को वर्ग कति हो?',
      o, on, f'{n} x {n} = {ans}.', f'{dev(n)} x {dev(n)} = {dev_num(ans)}।')
for n in range(2, 11):
    ans = n**3
    o, on, _ = num_opts(ans, [ans+n, ans-n, ans+10, ans-10])
    E('Squares & Cubes', 'easy', f'What is the cube of {n}?', f'{dev(n)} को घन कति हो?',
      o, on, f'{n} x {n} x {n} = {ans}.', f'{dev(n)} x {dev(n)} x {dev(n)} = {dev_num(ans)}।')

# ---------- Roman numerals ----------
def to_roman(n):
    vals = [(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]
    out = ''
    for v, s in vals:
        while n >= v:
            out += s; n -= v
    return out
for n in range(1, 101):
    r = to_roman(n)
    ds = [to_roman(max(1, n+d)) for d in (1, -1, 5, 10) if to_roman(max(1, n+d)) != r]
    ds = list(dict.fromkeys(ds))[:3]
    o = [r] + ds
    on = [r] + ds  # Roman numerals stay Latin in NE
    while len(o) < 4:
        o.append(to_roman(n+len(o)+1)); on.append(o[-1])
    em.emit(EX, 'Maths & Numerical', 'Roman Numerals', 'medium', 2,
            f'What is {n} in Roman numerals?', f'{dev(n)} लाई रोमन अङ्कमा कसरी लेखिन्छ?',
            o, on, 0, f'{n} in Roman numerals is {r}.', f'{dev(n)} लाई रोमन अङ्कमा {r} लेखिन्छ।')
for n in [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 89, 94, 99, 40, 90, 50, 60, 70, 80, 100]:
    r = to_roman(n)
    ds = [n+1, n-1, n+5, n-5]
    o, on, _ = num_opts(n, ds)
    em.emit(EX, 'Maths & Numerical', 'Roman Numerals', 'medium', 2,
            f'What is {r} in Hindu-Arabic numerals?', f'रोमन अङ्क {r} को मान कति हो?',
            o, on, 0, f'{r} = {n}.', f'{r} = {dev_num(n)} हो।')

# ---------- Nepali number words 1-100 ----------
NP_NUM = ['एक','दुई','तीन','चार','पाँच','छ','सात','आठ','नौ','दस',
'एघार','बाह्र','तेह्र','चौध','पन्ध्र','सोह्र','सत्र','अठार','उन्नाइस','बीस',
'एक्काइस','बाइस','तेइस','चौबीस','पच्चीस','छब्बीस','सत्ताइस','अठ्ठाइस','उनन्तीस','तीस',
'एक्तीस','बत्तीस','तेत्तीस','चौंतीस','पैंतीस','छत्तीस','सैंतीस','अठ्तीस','उनन्चालीस','चालीस',
'एकचालीस','बयालीस','त्रिचालीस','चौवालीस','पैंतालीस','छयालीस','सच्चालीस','अठ्चालीस','उनन्चास','पचास',
'एकाउन्न','बाउन्न','त्रिपन्न','चौवन्न','पचपन्न','छपन्न','सन्ताउन्न','अन्ठाउन्न','उनन्साठी','साठी',
'एकसट्ठी','बयसट्ठी','त्रिसट्ठी','चौंसट्ठी','पैंसट्ठी','छयसट्ठी','सतसट्ठी','अठ्सट्ठी','उनन्सत्तरी','सत्तरी',
'एकहत्तर','बहत्तर','त्रिहत्तर','चौहत्तर','पचहत्तर','छयहत्तर','सतहत्तर','अठहत्तर','उनासी','असी',
'एकासी','बयासी','तिरासी','चौरासी','पचासी','छयासी','सतासी','अठासी','उनान्नब्बे','नब्बे',
'एकान्नब्बे','बयान्नब्बे','तिरान्नब्बे','चौरान्नब्बे','पचान्नब्बे','छयान्नब्बे','सतान्नब्बे','अठान्नब्बे','उनान्सय','सय']
for n in range(1, 101):
    w = NP_NUM[n-1]
    ds = [NP_NUM[(n-1+d) % 100] for d in (1, -1, 5, -5) if NP_NUM[(n-1+d) % 100] != w]
    ds = list(dict.fromkeys(ds))[:3]
    o = [w] + ds
    on = o[:]  # Nepali words are already Devanagari; EN options carry the Nepali word
    while len(o) < 4:
        o.append(NP_NUM[(n+len(o)) % 100]); on.append(o[-1])
    em.emit(EX, 'Nepali Language', 'Nepali Numbers', 'easy', 2,
            f'How is the number {n} written in Nepali words?', f'{dev(n)} लाई नेपाली शब्दमा कसरी लेखिन्छ?',
            o, on, 0, f'{n} is written as "{w}" in Nepali.', f'{dev(n)} लाई नेपालीमा "{w}" लेखिन्छ।')

# ---------- days in month / months ----------
MONTHS = [('January', 'जनवरी', 31), ('February', 'फेब्रुअरी', 28), ('March', 'मार्च', 31),
          ('April', 'अप्रिल', 30), ('May', 'मे', 31), ('June', 'जुन', 30),
          ('July', 'जुलाई', 31), ('August', 'अगस्ट', 31), ('September', 'सेप्टेम्बर', 30),
          ('October', 'अक्टोबर', 31), ('November', 'नोभेम्बर', 30), ('December', 'डिसेम्बर', 31)]
for name, name_ne, days in MONTHS:
    o, on, _ = num_opts(days, [30, 31, 28, 29])
    E('Calendar', 'easy', f'How many days are there in {name}?', f'{name_ne} महिनामा कति दिन हुन्छ?',
      o, on, f'{name} has {days} days.', f'{name_ne} महिनामा {dev(days)} दिन हुन्छ।')
for _ in range(20):
    m = rng.choice([m for m in MONTHS if m[2] == 30])
    o = [m[0]] + rng.sample([x[0] for x in MONTHS if x[2] != 30], 3)
    on = [m[1]] + [dict((x[0], x[1]) for x in MONTHS)[x] for x in o[1:]]
    em.emit(EX, 'Maths & Numerical', 'Calendar', 'easy', 2,
            'Which of the following months has 30 days?', 'निम्नमध्ये कुन महिनामा ३० दिन हुन्छ?',
            o, on, 0, f'{m[0]} has 30 days.', f'{m[1]} महिनामा ३० दिन हुन्छ।')

# ---------- time / length / weight / area conversions ----------
CONV = []
for h in [1, 2, 4, 6, 10, 12, 24, 48]:
    CONV.append((f'How many minutes are there in {h} hour(s)?', f'{dev(h)} घण्टामा कति मिनेट हुन्छ?', h*60))
for m in [30, 60, 90, 120, 180, 240, 360, 720]:
    CONV.append((f'How many seconds are there in {m} minutes?', f'{dev(m)} मिनेटमा कति सेकेन्ड हुन्छ?', m*60))
for w in [1, 2, 3, 4, 7, 14]:
    CONV.append((f'How many days are there in {w} week(s)?', f'{dev(w)} हप्तामा कति दिन हुन्छ?', w*7))
for km in [1, 2, 5, 10, 25, 50, 100]:
    CONV.append((f'How many metres are there in {km} km?', f'{dev(km)} किलोमिटरमा कति मिटर हुन्छ?', km*1000))
for cm in [1, 5, 10, 25, 50, 100, 250]:
    CONV.append((f'How many millimetres are there in {cm} cm?', f'{dev(cm)} सेन्टिमिटरमा कति मिलिमिटर हुन्छ?', cm*10))
for g in [1, 2, 5, 10, 50, 100, 500]:
    CONV.append((f'How many milligrams are there in {g} gram(s)?', f'{dev(g)} ग्राममा कति मिलिग्राम हुन्छ?', g*1000))
CONV.append(('How many square metres are there in 1 hectare?', '१ हेक्टरमा कति वर्ग मिटर हुन्छ?', 10000))
CONV.append(('How many square metres are there in 1 ropani (Nepal)?', '१ रोपनीमा कति वर्ग मिटर हुन्छ?', 508.74))
CONV.append(('How many square metres are there in 1 bigha (Nepal)?', '१ बिघामा कति वर्ग मिटर हुन्छ?', 6772.63))
CONV.append(('How many square metres are there in 1 anna (Nepal)?', '१ आनामा कति वर्ग मिटर हुन्छ?', 31.80))
CONV.append(('How many anna are there in 1 ropani?', '१ रोपनीमा कति आना हुन्छ?', 16))
CONV.append(('How many square feet are there in 1 ropani (approximately)?', '१ रोपनीमा लगभग कति वर्ग फिट हुन्छ?', 5476))
for q, qn, ans in CONV:
    o, on, _ = num_opts(ans, [ans+10, ans-10, ans*2, ans//2 if isinstance(ans, int) and ans % 2 == 0 else ans+100])
    E('Unit Conversion', 'easy', q, qn, o, on, f'The answer is {fmt(ans)}.', f'उत्तर {dev_num(ans)} हो।')

# ---------- fraction arithmetic ----------
for _ in range(80):
    a = Fraction(rng.randint(1, 9), rng.randint(2, 9))
    b = Fraction(rng.randint(1, 9), rng.randint(2, 9))
    if rng.random() < 0.5:
        ans = a + b
        op, opn = '+', '+'
    else:
        if a < b: a, b = b, a
        ans = a - b
        op, opn = '-', '-'
    ans_s = f'{ans.numerator}/{ans.denominator}' if ans.denominator != 1 else str(ans.numerator)
    ans_n = dev(ans.numerator) + '/' + dev(ans.denominator) if ans.denominator != 1 else dev(ans.numerator)
    ds = [ans + Fraction(1, 6), ans - Fraction(1, 6), ans + Fraction(1, 3)]
    o = [ans_s] + [f'{x.numerator}/{x.denominator}' if x.denominator != 1 else str(x.numerator) for x in ds if x > 0][:3]
    on = [ans_n] + [dev(x.numerator) + '/' + dev(x.denominator) if x.denominator != 1 else dev(x.numerator) for x in ds if x > 0][:3]
    while len(o) < 4:
        o.append(f'{ans.numerator+len(o)}/{ans.denominator}'); on.append(dev(ans.numerator+len(o))+'/'+dev(ans.denominator))
    E('Fractions', 'medium', f'What is {a.numerator}/{a.denominator} {op} {b.numerator}/{b.denominator}?',
      f'{dev(a.numerator)}/{dev(a.denominator)} {opn} {dev(b.numerator)}/{dev(b.denominator)} कति हो?',
      o, on, f'{a.numerator}/{a.denominator} {op} {b.numerator}/{b.denominator} = {ans_s}.', f'{dev(a.numerator)}/{dev(a.denominator)} {opn} {dev(b.numerator)}/{dev(b.denominator)} = {ans_n}।')

# ---------- decimal arithmetic ----------
for _ in range(60):
    a = round(rng.uniform(1, 50), 2)
    b = round(rng.uniform(1, 50), 2)
    if rng.random() < 0.5:
        ans = round(a + b, 2)
        o = [fmt(ans), fmt(ans+1), fmt(ans-1), fmt(ans+0.5)]
        on = [dev_num(ans), dev_num(ans+1), dev_num(ans-1), dev_num(ans+0.5)]
        E('Decimals', 'easy', f'What is {a} + {b}?', f'{dev(a)} + {dev(b)} कति हो?',
          o, on, f'{a} + {b} = {ans}.', f'{dev(a)} + {dev(b)} = {dev_num(ans)}।')
    else:
        if a < b: a, b = b, a
        ans = round(a - b, 2)
        o = [fmt(ans), fmt(ans+1), fmt(ans-1), fmt(ans+0.5)]
        on = [dev_num(ans), dev_num(ans+1), dev_num(ans-1), dev_num(ans+0.5)]
        E('Decimals', 'easy', f'What is {a} - {b}?', f'{dev(a)} - {dev(b)} कति हो?',
          o, on, f'{a} - {b} = {ans}.', f'{dev(a)} - {dev(b)} = {dev_num(ans)}।')

# ---------- LCM/HCF triples (new ranges) ----------
for _ in range(100):
    a, b, c = rng.randint(6, 20), rng.randint(6, 20), rng.randint(6, 20)
    if len({a, b, c}) < 3: continue
    if rng.random() < 0.5:
        ans = math.lcm(a, b, c)
        o, on, _ = num_opts(ans, [ans+a, ans-a, ans*2, ans//2 if ans % 2 == 0 else ans+b])
        E('HCF & LCM', 'medium', f'Find the LCM of {a}, {b} and {c}.', f'{dev(a)}, {dev(b)} र {dev(c)} को लस पत्ता लगाउनुहोस्।',
          o, on, f'LCM({a}, {b}, {c}) = {ans}.', f'लस ({dev(a)}, {dev(b)}, {dev(c)}) = {dev_num(ans)}।')
    else:
        ans = math.gcd(math.gcd(a, b), c)
        o, on, _ = num_opts(ans, [ans+1, ans+2, ans*2, ans+3])
        E('HCF & LCM', 'medium', f'Find the HCF of {a}, {b} and {c}.', f'{dev(a)}, {dev(b)} र {dev(c)} को मस पत्ता लगाउनुहोस्।',
          o, on, f'HCF({a}, {b}, {c}) = {ans}.', f'मस ({dev(a)}, {dev(b)}, {dev(c)}) = {dev_num(ans)}।')

# ---------- sums ----------
for n in range(61, 101):
    ans = n*(n+1)//2
    o, on, _ = num_opts(ans, [ans+n, ans-n, ans+10, ans-10])
    E('Sequences', 'easy', f'Find the sum of the first {n} natural numbers.', f'पहिलो {dev(n)} वटा प्राकृतिक सङ्ख्याहरूको योग पत्ता लगाउनुहोस्।',
      o, on, f'Sum = {n} x {n+1} / 2 = {ans}.', f'योग = {dev(n)} x {dev(n+1)} / २ = {dev_num(ans)}।')

# ---------- prime / composite / even / odd / divisible / multiple / factors ----------
def is_prime(n):
    if n < 2: return False
    i = 2
    while i*i <= n:
        if n % i == 0: return False
        i += 1
    return True
primes = [n for n in range(2, 200) if is_prime(n)]
comps = [n for n in range(2, 200) if not is_prime(n)]
for _ in range(60):
    p = rng.choice(primes)
    ds = rng.sample(comps, 3)
    o = [str(p)] + [str(x) for x in ds]
    rng.shuffle(o)
    on = [dev_num(int(x)) for x in o]
    idx = o.index(str(p))
    em.emit(EX, 'Maths & Numerical', 'Number Theory', 'easy', 2,
            'Which of the following numbers is prime?', 'निम्नमध्ये कुन सङ्ख्या अभाज्य हो?',
            o, on, idx, f'{p} is prime; the others are composite. The answer is {p}.',
            f'{dev_num(p)} अभाज्य हो; अरू भाज्य छन्। उत्तर {dev_num(p)} हो।')
for _ in range(40):
    c = rng.choice(comps)
    ds = rng.sample(primes, 3)
    o = [str(c)] + [str(x) for x in ds]
    rng.shuffle(o)
    on = [dev_num(int(x)) for x in o]
    idx = o.index(str(c))
    em.emit(EX, 'Maths & Numerical', 'Number Theory', 'easy', 2,
            'Which of the following numbers is composite?', 'निम्नमध्ये कुन सङ्ख्या भाज्य हो?',
            o, on, idx, f'{c} is composite; the others are prime. The answer is {c}.',
            f'{dev_num(c)} भाज्य हो; अरू अभाज्य छन्। उत्तर {dev_num(c)} हो।')
for _ in range(40):
    d = rng.choice([3, 4, 5, 6, 7, 8, 9, 11])
    m = d * rng.randint(2, 20)
    ds = [m+1, m+2, m+3]
    o = [str(m)] + [str(x) for x in ds]
    rng.shuffle(o)
    on = [dev_num(int(x)) for x in o]
    idx = o.index(str(m))
    em.emit(EX, 'Maths & Numerical', 'Number Theory', 'easy', 2,
            f'Which of the following numbers is divisible by {d}?', f'निम्नमध्ये कुन सङ्ख्या {dev(d)} ले भाग जान्छ?',
            o, on, idx, f'{m} / {d} = {m//d}, so {m} is divisible by {d}. The answer is {m}.',
            f'{dev_num(m)} / {dev(d)} = {dev_num(m//d)}, त्यसैले {dev_num(m)} {dev(d)} ले भाग जान्छ। उत्तर {dev_num(m)} हो।')
for _ in range(40):
    d = rng.choice([3, 5, 7, 9, 11, 13])
    m = d * rng.randint(2, 15)
    ds = [m+1, m+2, m+4]
    o = [str(m)] + [str(x) for x in ds]
    rng.shuffle(o)
    on = [dev_num(int(x)) for x in o]
    idx = o.index(str(m))
    em.emit(EX, 'Maths & Numerical', 'Number Theory', 'easy', 2,
            f'Which of the following is a multiple of {d}?', f'निम्नमध्ये कुन {dev(d)} को गुणन हो?',
            o, on, idx, f'{m} = {d} x {m//d}, so {m} is a multiple of {d}. The answer is {m}.',
            f'{dev_num(m)} = {dev(d)} x {dev_num(m//d)}, त्यसैले {dev_num(m)} {dev(d)} को गुणन हो। उत्तर {dev_num(m)} हो।')

def ndiv(n):
    c, i = 0, 1
    while i*i <= n:
        if n % i == 0:
            c += 2 if i*i != n else 1
        i += 1
    return c
for n in range(121, 201):
    ans = ndiv(n)
    o, on, _ = num_opts(ans, [ans+1, ans-1, ans+2, ans-2])
    E('Number Theory', 'medium', f'How many factors does {n} have?', f'{dev(n)} का कति गुणनखण्ड छन्?',
      o, on, f'The number of factors of {n} is {ans}.', f'{dev(n)} का गुणनखण्डहरूको सङ्ख्या {dev_num(ans)} हो।')

# ---------- percentages with decimals ----------
for _ in range(80):
    p = rng.choice([2.5, 5, 7.5, 12.5, 15, 17.5, 22.5, 27.5, 32.5, 37.5, 45, 55, 65, 85, 95])
    n = rng.choice([40, 80, 120, 160, 200, 240, 400, 800])
    ans = p * n / 100
    if ans != int(ans): continue
    ans = int(ans)
    o, on, _ = num_opts(ans, [ans+5, ans-5, ans+10, ans-10])
    E('Percentage', 'medium', f'What is {p}% of {n}?', f'{dev(n)} को {dev(p)}% कति हो?',
      o, on, f'{p}% of {n} = {n} x {p}/100 = {ans}.', f'{dev(n)} को {dev(p)}% = {dev(n)} x {dev(p)}/१०० = {dev_num(ans)}।')

n = em.write('expansion-r10-drills.json')
print('DRILLS TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
