#!/usr/bin/env python3
"""R10 generator 11: more computed maths (~3,200). Fractions, squares/cubes,
LCM/HCF of 3, AP/GP, divisor counts, primes, SI with months, CI variants,
unit conversions, relative speed, 3-part ratios, missing-number averages,
two-transaction profit/loss, successive discounts, age equations, mixtures,
efficiency work, more series, remainders, BODMAS decimals."""
import sys, random, math, datetime
from fractions import Fraction
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
em = Emitter(bank, 'R10-MATH3')
rng = random.Random(71103)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'police', 'army', 'tsc-primary', 'tsc-secondary']
EXH = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'csit-entrance', 'ioe-entrance', 'mecee-bl']

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

def Eh(sub, diff, q, qn, o, on, expl, expln):
    em.emit(EXH, 'Maths & Numerical', sub, diff, 2, q, qn, o, on, 0, expl, expln)

# ---------- fractions of a number ----------
for _ in range(120):
    a, b = rng.choice([(1,2),(1,3),(2,3),(1,4),(3,4),(1,5),(2,5),(3,5),(4,5),(1,6),(5,6),(1,8),(3,8),(5,8),(7,8),(2,7),(3,7),(1,10),(3,10),(7,10),(9,10)])
    n = b * rng.randint(3, 60)
    ans = a * n // b
    o, on, _ = num_opts(ans, [ans+1, ans-1, ans+a, ans+2*a, ans-2])
    E('Fractions', 'easy', f'What is {a}/{b} of {n}?', f'{n} को {dev(a)}/{dev(b)} कति हो?',
      o, on, f'{a}/{b} of {n} = {n} x {a}/{b} = {ans}.', f'{n} को {dev(a)}/{dev(b)} = {dev(n)} x {dev(a)}/{dev(b)} = {dev_num(ans)}।')

# ---------- fraction addition/subtraction (like denominators) ----------
for _ in range(80):
    b = rng.randint(3, 12)
    a1, a2 = rng.randint(1, b-1), rng.randint(1, b-1)
    if rng.random() < 0.5:
        num = a1 + a2
        if num >= b: continue
        f = Fraction(num, b)
        ans = f'{f.numerator}/{f.denominator}' if f.denominator != 1 else str(f.numerator)
        an = dev(f.numerator) + '/' + dev(f.denominator) if f.denominator != 1 else dev(f.numerator)
        d = [f'{x}/{b}' for x in (num+1, num-1, num+2) if 0 < x < b]
        o = [ans] + d[:3]
        on = [an] + [dev(x)+'/'+dev(b) for x in (num+1, num-1, num+2) if 0 < x < b][:3]
        while len(o) < 4:
            o.append(f'{num+len(o)}/{b}'); on.append(dev(num+len(o))+'/'+dev(b))
        E('Fractions', 'easy', f'What is {a1}/{b} + {a2}/{b}?', f'{dev(a1)}/{dev(b)} + {dev(a2)}/{dev(b)} कति हो?',
          o, on, f'{a1}/{b} + {a2}/{b} = {num}/{b} = {ans}.', f'{dev(a1)}/{dev(b)} + {dev(a2)}/{dev(b)} = {dev(num)}/{dev(b)} = {an}।')
    else:
        if a1 <= a2: continue
        num = a1 - a2
        f = Fraction(num, b)
        ans = f'{f.numerator}/{f.denominator}' if f.denominator != 1 else str(f.numerator)
        an = dev(f.numerator) + '/' + dev(f.denominator) if f.denominator != 1 else dev(f.numerator)
        d = [f'{x}/{b}' for x in (num+1, num-1, num+2) if 0 < x < b]
        o = [ans] + d[:3]
        on = [an] + [dev(x)+'/'+dev(b) for x in (num+1, num-1, num+2) if 0 < x < b][:3]
        while len(o) < 4:
            o.append(f'{num+len(o)}/{b}'); on.append(dev(num+len(o))+'/'+dev(b))
        E('Fractions', 'easy', f'What is {a1}/{b} - {a2}/{b}?', f'{dev(a1)}/{dev(b)} - {dev(a2)}/{dev(b)} कति हो?',
          o, on, f'{a1}/{b} - {a2}/{b} = {num}/{b} = {ans}.', f'{dev(a1)}/{dev(b)} - {dev(a2)}/{dev(b)} = {dev(num)}/{dev(b)} = {an}।')

# ---------- fraction -> percent / percent -> fraction ----------
for _ in range(60):
    p = rng.choice([5, 10, 12.5, 20, 25, 30, 40, 50, 60, 75, 80, 90])
    if rng.random() < 0.5:
        f = Fraction(p).limit_denominator(20) / 100
        ans = f'{f.numerator}/{f.denominator}'
        an = dev(f.numerator) + '/' + dev(f.denominator)
        o = [ans, f'{f.numerator+1}/{f.denominator}', f'{f.numerator}/{f.denominator+1}', f'{f.denominator}/{f.numerator}']
        on = [an, dev(f.numerator+1)+'/'+dev(f.denominator), dev(f.numerator)+'/'+dev(f.denominator+1), dev(f.denominator)+'/'+dev(f.numerator)]
        E('Fractions', 'medium', f'Express {p}% as a fraction in lowest terms.', f'{dev(p)}% लाई न्यूनतम भिन्नमा व्यक्त गर्नुहोस्।',
          o, on, f'{p}% = {p}/100 = {ans}.', f'{dev(p)}% = {dev(p)}/१०० = {an}।')
    else:
        f = Fraction(rng.choice([1,2,3,4,5,6,7,8,9]), rng.choice([2,4,5,8,10,20,25,50]))
        pct = f * 100
        ans = fmt(pct) if pct.denominator == 1 else f'{pct.numerator}/{pct.denominator}'
        an = dev_num(pct) if pct.denominator == 1 else dev(pct.numerator)+'/'+dev(pct.denominator)
        d = [pct+10, pct-10, pct+5, pct-5]
        o = [f'{ans}%'] + [f'{fmt(x)}%' for x in d[:3]]
        on = [f'{an}%'] + [f'{dev_num(x)}%' for x in d[:3]]
        E('Fractions', 'medium', f'Express {f.numerator}/{f.denominator} as a percentage.', f'{dev(f.numerator)}/{dev(f.denominator)} लाई प्रतिशतमा व्यक्त गर्नुहोस्।',
          o, on, f'{f.numerator}/{f.denominator} x 100 = {ans}%.', f'{dev(f.numerator)}/{dev(f.denominator)} x १०० = {an}%।')

# ---------- squares 31-100, cubes 11-30, square roots ----------
for n in range(31, 101):
    ans = n*n
    o, on, _ = num_opts(ans, [ans+n, ans-n, ans+100, ans-100])
    E('Squares & Cubes', 'easy', f'What is {n} squared?', f'{dev(n)} को वर्ग कति हो?',
      o, on, f'{n} x {n} = {ans}.', f'{dev(n)} x {dev(n)} = {dev_num(ans)}।')
for n in range(11, 31):
    ans = n**3
    o, on, _ = num_opts(ans, [ans+n*n, ans-n*n, ans+100, ans-100])
    E('Squares & Cubes', 'medium', f'What is the cube of {n}?', f'{dev(n)} को घन कति हो?',
      o, on, f'{n}^3 = {n} x {n} x {n} = {ans}.', f'{dev(n)}^३ = {dev(n)} x {dev(n)} x {dev(n)} = {dev_num(ans)}।')
for n in range(21, 101, 2):
    sq = n*n
    o, on, _ = num_opts(n, [n+1, n-1, n+2, n-2])
    E('Squares & Cubes', 'easy', f'What is the square root of {sq}?', f'{dev_num(sq)} को वर्गमूल कति हो?',
      o, on, f'The square root of {sq} = {n} because {n} x {n} = {sq}.', f'{dev_num(sq)} को वर्गमूल = {dev(n)} किनकि {dev(n)} x {dev(n)} = {dev_num(sq)}।')

# ---------- LCM / HCF of 3 numbers ----------
for _ in range(120):
    a, b, c = rng.randint(2, 15), rng.randint(2, 15), rng.randint(2, 15)
    if len({a, b, c}) < 3: continue
    if rng.random() < 0.5:
        ans = math.lcm(a, b, c)
        o, on, _ = num_opts(ans, [ans+a, ans-a, ans*2, ans//2 if ans % 2 == 0 else ans+b])
        E('HCF & LCM', 'medium', f'What is the LCM of {a}, {b} and {c}?', f'{dev(a)}, {dev(b)} र {dev(c)} को लस कति हो?',
          o, on, f'LCM({a}, {b}, {c}) = {ans}.', f'लस ({dev(a)}, {dev(b)}, {dev(c)}) = {dev_num(ans)}।')
    else:
        ans = math.gcd(math.gcd(a, b), c)
        o, on, _ = num_opts(ans, [ans+1, ans+2, ans*2, ans+3])
        E('HCF & LCM', 'medium', f'What is the HCF of {a}, {b} and {c}?', f'{dev(a)}, {dev(b)} र {dev(c)} को मस कति हो?',
          o, on, f'HCF({a}, {b}, {c}) = {ans}.', f'मस ({dev(a)}, {dev(b)}, {dev(c)}) = {dev_num(ans)}।')

# ---------- AP: nth term and sum ----------
for _ in range(120):
    a, d = rng.randint(1, 20), rng.randint(1, 10)
    n = rng.randint(5, 30)
    if rng.random() < 0.5:
        ans = a + (n-1)*d
        o, on, _ = num_opts(ans, [ans+d, ans-d, ans+1, ans-1])
        E('Sequences', 'medium', f'In an arithmetic sequence, the first term is {a} and the common difference is {d}. What is the {ord_s(n)} term?', f'एउटा समान्तर श्रेणीमा पहिलो पद {dev(a)} र साझा अन्तर {dev(d)} छ। {dev(n)}औँ पद कति हो?',
          o, on, f'Term {n} = {a} + ({n}-1) x {d} = {ans}.', f'{dev(n)}औँ पद = {dev(a)} + ({dev(n)}-१) x {dev(d)} = {dev_num(ans)}।')
    else:
        ans = n*(2*a + (n-1)*d)//2
        o, on, _ = num_opts(ans, [ans+a, ans-a, ans+d, ans-d])
        E('Sequences', 'hard', f'What is the sum of the first {n} terms of the arithmetic sequence {a}, {a+d}, {a+2*d}, ...?', f'समान्तर श्रेणी {dev(a)}, {dev(a+d)}, {dev(a+2*d)}, ... का पहिलो {dev(n)} पदहरूको योग कति हो?',
          o, on, f'Sum = {n}/2 x [2 x {a} + ({n}-1) x {d}] = {ans}.', f'योग = {dev(n)}/२ x [२ x {dev(a)} + ({dev(n)}-१) x {dev(d)}] = {dev_num(ans)}।')

# ---------- sum of first n naturals / squares / cubes ----------
for n in range(11, 61):
    ans = n*(n+1)//2
    o, on, _ = num_opts(ans, [ans+n, ans-n, ans+10, ans-10])
    E('Sequences', 'easy', f'What is the sum of the first {n} natural numbers?', f'पहिलो {dev(n)} वटा प्राकृतिक सङ्ख्याहरूको योग कति हो?',
      o, on, f'Sum = {n} x {n+1} / 2 = {ans}.', f'योग = {dev(n)} x {dev(n+1)} / २ = {dev_num(ans)}।')
for n in range(6, 26):
    ans = n*(n+1)*(2*n+1)//6
    o, on, _ = num_opts(ans, [ans+n, ans-n, ans+10, ans-10])
    E('Sequences', 'hard', f'What is the sum of the squares of the first {n} natural numbers?', f'पहिलो {dev(n)} वटा प्राकृतिक सङ्ख्याहरूको वर्गहरूको योग कति हो?',
      o, on, f'Sum of squares = {n} x {n+1} x {2*n+1} / 6 = {ans}.', f'वर्गहरूको योग = {dev(n)} x {dev(n+1)} x {dev(2*n+1)} / ६ = {dev_num(ans)}।')
for n in range(5, 16):
    ans = (n*(n+1)//2)**2
    o, on, _ = num_opts(ans, [ans+n, ans-n, ans+100, ans-100])
    E('Sequences', 'hard', f'What is the sum of the cubes of the first {n} natural numbers?', f'पहिलो {dev(n)} वटा प्राकृतिक सङ्ख्याहरूको घनहरूको योग कति हो?',
      o, on, f'Sum of cubes = ({n} x {n+1} / 2)^2 = {ans}.', f'घनहरूको योग = ({dev(n)} x {dev(n+1)} / २)^२ = {dev_num(ans)}।')

# ---------- divisor count ----------
def ndiv(n):
    c, i = 0, 1
    while i*i <= n:
        if n % i == 0:
            c += 2 if i*i != n else 1
        i += 1
    return c
for n in range(12, 121):
    ans = ndiv(n)
    o, on, _ = num_opts(ans, [ans+1, ans-1, ans+2, ans-2])
    E('Number Theory', 'medium', f'How many divisors does {n} have?', f'{dev(n)} का कति भाजक छन्?',
      o, on, f'The divisors of {n} are {ndiv(n)} in number = {ans}.', f'{dev(n)} का भाजकहरूको सङ्ख्या = {dev_num(ans)}।')

# ---------- prime identification ----------
def is_prime(n):
    if n < 2: return False
    i = 2
    while i*i <= n:
        if n % i == 0: return False
        i += 1
    return True
primes = [n for n in range(11, 200) if is_prime(n)]
comps = [n for n in range(11, 200) if not is_prime(n)]
for _ in range(80):
    p = rng.choice(primes)
    ds = rng.sample(comps, 3)
    o = [str(p)] + [str(x) for x in ds]
    on = [dev_num(p)] + [dev_num(x) for x in ds]
    rng.shuffle(o)
    # rebuild NE to match shuffled order
    on = [dev_num(int(x)) for x in o]
    idx = o.index(str(p))
    em.emit(EX, 'Maths & Numerical', 'Number Theory', 'easy', 2,
            'Which of the following is a prime number?', 'निम्नमध्ये कुन अभाज्य सङ्ख्या हो?',
            o, on, idx, f'{p} is a prime number; the others are composite. The answer is {p}.',
            f'{dev_num(p)} अभाज्य सङ्ख्या हो; अरू भाज्य छन्। उत्तर {dev_num(p)} हो।')

# ---------- SI with months ----------
for _ in range(100):
    P = rng.choice([1000, 2000, 4000, 5000, 8000, 10000, 12000, 15000, 20000, 25000])
    R = rng.choice([4, 5, 6, 8, 10, 12, 15, 20])
    m = rng.choice([3, 6, 9, 18, 30])
    ans = P * R * m // (100*12)
    if P * R * m % 1200: continue
    o, on, _ = num_opts(ans, [ans+10, ans-10, ans+50, ans-50])
    E('Simple Interest', 'medium', f'What is the simple interest on Rs {P} at {R}% per annum for {m} months?', f'रु {dev_num(P)} मा {dev(R)}% वार्षिक दरले {dev(m)} महिनाको साधारण ब्याज कति हो?',
      o, on, f'SI = {P} x {R} x {m}/12 / 100 = {ans}.', f'साधारण ब्याज = {dev_num(P)} x {dev(R)} x {dev(m)}/१२ / १०० = {dev_num(ans)}।')

# ---------- CI 2 years ----------
for _ in range(80):
    P = rng.choice([1000, 2000, 4000, 5000, 8000, 10000, 20000, 25000, 40000, 50000])
    R = rng.choice([5, 10, 20, 25])
    amt = P * (1 + R/100)**2
    if amt != int(amt): continue
    amt = int(amt)
    ci = amt - P
    if rng.random() < 0.5:
        o, on, _ = num_opts(ci, [ci+50, ci-50, ci+100, ci-100])
        E('Compound Interest', 'hard', f'What is the compound interest on Rs {P} at {R}% per annum for 2 years?', f'रु {dev_num(P)} मा {dev(R)}% वार्षिक दरले २ वर्षको चक्रवृद्धि ब्याज कति हो?',
          o, on, f'Amount = {P} x (1 + {R}/100)^2 = {amt}; CI = {amt} - {P} = {ci}.', f'मिश्रधन = {dev_num(P)} x (१ + {dev(R)}/१००)^२ = {dev_num(amt)}; चक्रवृद्धि ब्याज = {dev_num(amt)} - {dev_num(P)} = {dev_num(ci)}।')
    else:
        o, on, _ = num_opts(amt, [amt+100, amt-100, amt+500, amt-500])
        E('Compound Interest', 'hard', f'What is the amount after 2 years on Rs {P} at {R}% compound interest per annum?', f'रु {dev_num(P)} मा {dev(R)}% वार्षिक चक्रवृद्धि ब्याज दरले २ वर्षपछिको मिश्रधन कति हो?',
          o, on, f'Amount = {P} x (1 + {R}/100)^2 = {amt}.', f'मिश्रधन = {dev_num(P)} x (१ + {dev(R)}/१००)^२ = {dev_num(amt)}।')

# ---------- unit conversions ----------
CONV = []
for kmh in [18, 36, 54, 72, 90, 108, 126, 144]:
    CONV.append((f'Convert {kmh} km/h into m/s.', f'{dev(kmh)} किमी/घण्टालाई मिटर/सेकेन्डमा बदल्नुहोस्।', kmh*5//18, f'{kmh} x 5/18 = {kmh*5//18} m/s.'))
for ms in [5, 10, 15, 20, 25, 30, 40]:
    CONV.append((f'Convert {ms} m/s into km/h.', f'{dev(ms)} मिटर/सेकेन्डलाई किमी/घण्टामा बदल्नुहोस्।', ms*18//5, f'{ms} x 18/5 = {ms*18//5} km/h.'))
for kg in [2, 3, 5, 7, 12, 25, 40]:
    CONV.append((f'How many grams are there in {kg} kg?', f'{dev(kg)} किलोग्राममा कति ग्राम हुन्छ?', kg*1000, f'{kg} kg = {kg} x 1000 = {kg*1000} g.'))
for m in [3, 5, 8, 12, 25]:
    CONV.append((f'How many centimetres are there in {m} m?', f'{dev(m)} मिटरमा कति सेन्टिमिटर हुन्छ?', m*100, f'{m} m = {m} x 100 = {m*100} cm.'))
for h in [2, 3, 5, 8, 12, 24]:
    CONV.append((f'How many minutes are there in {h} hours?', f'{dev(h)} घण्टामा कति मिनेट हुन्छ?', h*60, f'{h} hours = {h} x 60 = {h*60} minutes.'))
for d in [2, 3, 5, 7, 10, 15, 30]:
    CONV.append((f'How many hours are there in {d} days?', f'{dev(d)} दिनमा कति घण्टा हुन्छ?', d*24, f'{d} days = {d} x 24 = {d*24} hours.'))
for q in [2, 5, 10, 25]:
    CONV.append((f'How many kilograms are there in {q} quintals?', f'{dev(q)} क्विन्टलमा कति किलोग्राम हुन्छ?', q*100, f'{q} quintals = {q} x 100 = {q*100} kg.'))
for t in [1, 2, 5, 10]:
    CONV.append((f'How many kilograms are there in {t} tonne(s)?', f'{dev(t)} टनमा कति किलोग्राम हुन्छ?', t*1000, f'{t} tonne = {t} x 1000 = {t*1000} kg.'))
for l in [2, 3, 5, 8, 12]:
    CONV.append((f'How many millilitres are there in {l} litres?', f'{dev(l)} लिटरमा कति मिलिलिटर हुन्छ?', l*1000, f'{l} litres = {l} x 1000 = {l*1000} ml.'))
for q, qn, ans, expl in CONV:
    o, on, _ = num_opts(ans, [ans+10, ans-10, ans*2, ans//2 if ans % 2 == 0 else ans+100])
    E('Unit Conversion', 'easy', q, qn, o, on, expl, f'उत्तर {dev_num(ans)} हो। {dev(expl)}')

# ---------- relative speed: trains crossing each other ----------
for _ in range(60):
    l1, l2 = rng.choice([100, 120, 150, 180, 200, 240, 300]), rng.choice([100, 120, 150, 180, 200, 240, 300])
    v1, v2 = rng.choice([36, 54, 72, 90]), rng.choice([36, 54, 72, 90])
    s1, s2 = v1*5//18, v2*5//18
    total = (l1+l2) / (s1+s2)
    if total != int(total): continue
    total = int(total)
    o, on, _ = num_opts(total, [total+2, total-2, total+5, total-5])
    E('Trains', 'hard', f'Two trains of lengths {l1} m and {l2} m run towards each other at {v1} km/h and {v2} km/h. In how many seconds do they cross each other?', f'{dev(l1)} मिटर र {dev(l2)} मिटर लम्बाइका दुई रेल {dev(v1)} किमी/घण्टा र {dev(v2)} किमी/घण्टाको गतिमा एकअर्कातर्फ दौडिरहेका छन्। तिनीहरूले एकअर्कालाई पार गर्न कति सेकेन्ड लाग्छ?',
      o, on, f'Relative speed = {v1} + {v2} = {v1+v2} km/h = {(v1+v2)*5//18} m/s. Time = ({l1} + {l2}) / {(v1+v2)*5//18} = {total} seconds.', f'सापेक्ष गति = {dev(v1)} + {dev(v2)} = {dev(v1+v2)} किमी/घण्टा = {dev((v1+v2)*5//18)} मिटर/सेकेन्ड। समय = ({dev(l1)} + {dev(l2)}) / {dev((v1+v2)*5//18)} = {dev(total)} सेकेन्ड।')

# ---------- 3-part ratios ----------
for _ in range(80):
    a, b, c = rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 6)
    if len({a, b, c}) < 2: continue
    tot = rng.randint(5, 30) * (a+b+c)
    share = tot * rng.choice([a, b, c]) // (a+b+c)
    part = rng.choice(['first', 'second', 'third'])
    idx = {'first': a, 'second': b, 'third': c}[part]
    share = tot * idx // (a+b+c)
    o, on, _ = num_opts(share, [share+10, share-10, share+20, share-20])
    E('Ratio & Proportion', 'medium', f'Divide Rs {tot} in the ratio {a}:{b}:{c}. What is the {part} share?', f'रु {dev_num(tot)} लाई {dev(a)}:{dev(b)}:{dev(c)} को अनुपातमा बाँड्नुहोस्। {part} भाग कति हो?',
      o, on, f'{part} share = {tot} x {idx}/{a+b+c} = {share}.', f'{part} भाग = {dev_num(tot)} x {dev(idx)}/{dev(a+b+c)} = {dev_num(share)}।')

# ---------- average with missing number ----------
for _ in range(80):
    n = rng.randint(4, 8)
    avg = rng.randint(10, 60)
    tot = n * avg
    known = [rng.randint(5, 90) for _ in range(n-1)]
    missing = tot - sum(known)
    if missing <= 0 or missing > 150: continue
    o, on, _ = num_opts(missing, [missing+5, missing-5, missing+10, missing-10])
    E('Averages', 'medium', f'The average of {n} numbers is {avg}. The sum of {n-1} of them is {sum(known)}. What is the remaining number?', f'{dev(n)} वटा सङ्ख्याहरूको औसत {dev(avg)} छ। तीमध्ये {dev(n-1)} वटाको योग {dev_num(sum(known))} छ। बाँकी सङ्ख्या कति हो?',
      o, on, f'Total = {n} x {avg} = {tot}. Missing number = {tot} - {sum(known)} = {missing}.', f'जम्मा = {dev(n)} x {dev(avg)} = {dev_num(tot)}। हराएको सङ्ख्या = {dev_num(tot)} - {dev_num(sum(known))} = {dev_num(missing)}।')

# ---------- two-transaction profit/loss ----------
for _ in range(60):
    cp1 = rng.choice([100, 200, 400, 500, 800, 1000])
    p1 = rng.choice([10, 20, 25])
    sp1 = cp1 * (100+p1)//100
    cp2 = rng.choice([100, 200, 400, 500, 800, 1000])
    l2 = rng.choice([10, 20, 25])
    sp2 = cp2 * (100-l2)//100
    net = (sp1+sp2) - (cp1+cp2)
    if net >= 0:
        q = f'A man sells one article for Rs {sp1} (bought for Rs {cp1}) and another for Rs {sp2} (bought for Rs {cp2}). What is his overall profit?'
        qn = f'एक व्यक्तिले एउटा सामान रु {dev_num(sp1)} मा बेच्छ (रु {dev_num(cp1)} मा किनेको) र अर्को रु {dev_num(sp2)} मा बेच्छ (रु {dev_num(cp2)} मा किनेको)। उसको समग्र नाफा कति हो?'
        ans = net
    else:
        q = f'A man sells one article for Rs {sp1} (bought for Rs {cp1}) and another for Rs {sp2} (bought for Rs {cp2}). What is his overall loss?'
        qn = f'एक व्यक्तिले एउटा सामान रु {dev_num(sp1)} मा बेच्छ (रु {dev_num(cp1)} मा किनेको) र अर्को रु {dev_num(sp2)} मा बेच्छ (रु {dev_num(cp2)} मा किनेको)। उसको समग्र घाटा कति हो?'
        ans = -net
    o, on, _ = num_opts(ans, [ans+20, ans-20, ans+50, ans-50])
    E('Profit & Loss', 'hard', q, qn, o, on,
      f'Total CP = {cp1+cp2}, total SP = {sp1+sp2}. Difference = {ans}.',
      f'कुल क्रय मूल्य = {dev_num(cp1+cp2)}, कुल विक्रय मूल्य = {dev_num(sp1+sp2)}। अन्तर = {dev_num(ans)}।')

# ---------- successive discounts ----------
for _ in range(60):
    mp = rng.choice([500, 1000, 2000, 4000, 5000, 10000])
    d1 = rng.choice([10, 20, 25, 50])
    d2 = rng.choice([10, 20, 25, 50])
    after1 = mp * (100-d1)//100
    sp = after1 * (100-d2)//100
    if after1 * (100-d2) % 100: continue
    o, on, _ = num_opts(sp, [sp+50, sp-50, sp+100, sp-100])
    E('Discount', 'hard', f'What is the selling price of an article marked Rs {mp} after successive discounts of {d1}% and {d2}%?', f'रु {dev_num(mp)} अङ्कित मूल्य भएको सामानमा {dev(d1)}% र {dev(d2)}% को क्रमिक छुटपछि विक्रय मूल्य कति हो?',
      o, on, f'After {d1}% discount: {mp} x {100-d1}/100 = {after1}. After {d2}% discount: {after1} x {100-d2}/100 = {sp}.', f'{dev(d1)}% छुटपछि: {dev_num(mp)} x {dev(100-d1)}/१०० = {dev_num(after1)}। {dev(d2)}% छुटपछि: {dev_num(after1)} x {dev(100-d2)}/१०० = {dev_num(sp)}।')

# ---------- age equations ----------
for _ in range(80):
    k = rng.choice([2, 3, 4, 5])
    son = rng.randint(4, 15)
    father = k * son
    if rng.random() < 0.5:
        o, on, _ = num_opts(father, [father+5, father-5, father+10, father-10])
        E('Age Problems', 'medium', f'A father is {k} times as old as his son. If the son is {son} years old, how old is the father?', f'बुबा छोराभन्दा {dev(k)} गुणा बूढा छन्। छोरा {dev(son)} वर्षको छ भने बुबा कति वर्षका छन्?',
          o, on, f'Father\'s age = {k} x {son} = {father}.', f'बुबाको उमेर = {dev(k)} x {dev(son)} = {dev(father)}।')
    else:
        s = father + son
        o, on, _ = num_opts(son, [son+2, son-2, son+5, son-5])
        E('Age Problems', 'medium', f'A father is {k} times as old as his son. The sum of their ages is {s}. How old is the son?', f'बुबा छोराभन्दा {dev(k)} गुणा बूढा छन्। उनीहरूको उमेरको योग {dev(s)} छ। छोरा कति वर्षको छ?',
          o, on, f'Let the son\'s age be x. Then {k}x + x = {s}, so {k+1}x = {s}, x = {son}.', f'छोराको उमेर x मानौँ। {dev(k)}x + x = {dev(s)}, त्यसैले {dev(k+1)}x = {dev(s)}, x = {dev(son)}।')

# ---------- mixtures: milk-water ----------
for _ in range(60):
    milk = rng.choice([20, 30, 40, 50, 60])
    water = rng.choice([5, 10, 15, 20])
    total = milk + water
    pct = milk * 100 // total
    if milk * 100 % total: continue
    o, on, _ = num_opts(pct, [pct+5, pct-5, pct+10, pct-10])
    E('Mixtures', 'medium', f'A mixture contains {milk} litres of milk and {water} litres of water. What is the percentage of milk in the mixture?', f'एउटा मिश्रणमा {dev(milk)} लिटर दूध र {dev(water)} लिटर पानी छ। मिश्रणमा दूधको प्रतिशत कति हो?',
      o, on, f'Total = {milk} + {water} = {total} litres. Milk % = {milk}/{total} x 100 = {pct}%.', f'जम्मा = {dev(milk)} + {dev(water)} = {dev(total)} लिटर। दूध % = {dev(milk)}/{dev(total)} x १०० = {dev(pct)}%।')

# ---------- work efficiency ----------
for _ in range(60):
    t = rng.choice([6, 8, 10, 12, 15, 20, 24, 30])
    k = rng.choice([2, 3])
    # A is k times as efficient as B; A alone takes t days; together?
    together = t * k // (k+1) if (t*k) % (k+1) == 0 else None
    if together is None: continue
    o, on, _ = num_opts(together, [together+1, together-1, together+2, together-2])
    E('Work & Time', 'hard', f'A is {k} times as efficient as B. A alone can finish a work in {t} days. In how many days can A and B together finish the work?', f'A, B भन्दा {dev(k)} गुणा बढी दक्ष छ। A एक्लैले एउटा काम {dev(t)} दिनमा सक्न सक्छ। A र B मिलेर त्यो काम कति दिनमा सक्न सक्छन्?',
      o, on, f'B alone takes {k*t} days. Together: 1/{t} + 1/{k*t} = {k+1}/{k*t}, so time = {together} days.', f'B एक्लैले {dev(k*t)} दिन लिन्छ। सँगै: १/{dev(t)} + १/{dev(k*t)} = {dev(k+1)}/{dev(k*t)}, त्यसैले समय = {dev(together)} दिन।')

# ---------- more series: n^2+-n, x2+-1, x3+-2, Fibonacci-like ----------
def series_q(seq, nxt, sub):
    s = ', '.join(str(x) for x in seq)
    sn = ', '.join(dev_num(x) for x in seq)
    o, on, _ = num_opts(nxt, [nxt+1, nxt-1, nxt+2, nxt-2])
    E('Number Series', 'hard', f'What is the next number in the series: {s}, ...?', f'श्रेणी {sn}, ... मा अर्को सङ्ख्या कति हो?',
      o, on, f'The next term is {nxt}.', f'अर्को पद {dev_num(nxt)} हो।')
for n0 in range(2, 12):
    seq = [i*i + i for i in range(n0, n0+4)]
    series_q(seq, (n0+4)*(n0+4) + (n0+4), 'Number Series')
    seq = [i*i - i for i in range(n0, n0+4)]
    series_q(seq, (n0+4)*(n0+4) - (n0+4), 'Number Series')
for n0 in [3, 5, 7, 11, 13]:
    seq = [n0]
    for _ in range(3): seq.append(seq[-1]*2 + 1)
    series_q(seq, seq[-1]*2 + 1, 'Number Series')
    seq = [n0]
    for _ in range(3): seq.append(seq[-1]*3 - 2)
    series_q(seq, seq[-1]*3 - 2, 'Number Series')
for a, b in [(2, 3), (3, 5), (5, 8), (1, 4), (4, 7)]:
    seq = [a, b]
    for _ in range(3): seq.append(seq[-1] + seq[-2])
    series_q(seq, seq[-1] + seq[-2], 'Number Series')

# ---------- remainders: smallest number leaving remainder ----------
for _ in range(60):
    d = rng.randint(3, 12)
    r = rng.randint(1, d-1)
    q = rng.randint(2, 9)
    n = d*q + r
    o, on, _ = num_opts(n, [n+1, n-1, n+d, n-d])
    E('Remainders', 'medium', f'What is the smallest number which, when divided by {d}, leaves a remainder of {r} and a quotient of {q}?', f'{dev(d)} ले भाग गर्दा {dev(r)} शेष र {dev(q)} भागफल आउने सबैभन्दा सानो सङ्ख्या कुन हो?',
      o, on, f'Number = divisor x quotient + remainder = {d} x {q} + {r} = {n}.', f'सङ्ख्या = भाजक x भागफल + शेष = {dev(d)} x {dev(q)} + {dev(r)} = {dev_num(n)}।')

# ---------- BODMAS with decimals ----------
for _ in range(60):
    a = rng.choice([1.5, 2.5, 3.5, 4.5, 0.5, 2.25, 1.25])
    b = rng.choice([2, 3, 4, 5])
    c = rng.choice([1.5, 2.5, 0.5, 3.5])
    ans = a * b + c
    ans = round(ans, 2)
    o = [fmt(ans), fmt(ans+1), fmt(ans-1), fmt(ans+0.5)]
    on = [dev_num(ans), dev_num(ans+1), dev_num(ans-1), dev_num(ans+0.5)]
    E('BODMAS', 'medium', f'What is {a} x {b} + {c}?', f'{dev(a)} x {dev(b)} + {dev(c)} कति हो?',
      o, on, f'{a} x {b} + {c} = {a*b} + {c} = {ans}.', f'{dev(a)} x {dev(b)} + {dev(c)} = {dev(a*b)} + {dev(c)} = {dev_num(ans)}।')

# ---------- more calendar dates 2027-2035 ----------
start = datetime.date(2027, 1, 1)
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days_ne = ['सोमबार', 'मङ्गलबार', 'बुधबार', 'बिहीबार', 'शुक्रबार', 'शनिबार', 'आइतबार']
for _ in range(200):
    d = start + datetime.timedelta(days=rng.randint(0, 2900))
    wd = d.weekday()
    correct = days[wd]
    ds = [x for x in days if x != correct]
    rng.shuffle(ds)
    o = [correct] + ds[:3]
    on = [days_ne[wd]] + [days_ne[days.index(x)] for x in ds[:3]]
    em.emit(EX, 'Maths & Numerical', 'Calendar', 'medium', 2,
            f'What day of the week was {d.day} {d.strftime("%B")} {d.year}?',
            f'{dev(d.year)} {d.strftime("%B")} {dev(d.day)} कुन बार थियो?',
            o, on, 0, f'{d.day} {d.strftime("%B")} {d.year} was a {correct}.',
            f'{dev(d.year)} {d.strftime("%B")} {dev(d.day)} {days_ne[wd]} थियो।')

# ---------- clock angles at 5-min marks ----------
for h in range(1, 13):
    for m in range(0, 60, 5):
        if h == 12 and m == 0: continue
        ang = abs(30*h - 5.5*m)
        if ang > 180: ang = 360 - ang
        ang = int(ang) if ang == int(ang) else ang
        o, on, _ = num_opts(ang, [ang+15, ang-15, ang+30, ang-30])
        E('Clock', 'hard', f'What is the angle between the hands of a clock at {h}:{m:02d}?', f'घडीमा {dev(h)}:{dev(f"{m:02d}")} बजे सुईहरूबीचको कोण कति हुन्छ?',
          o, on, f'Angle = |30 x {h} - 5.5 x {m}| = {ang} degrees.', f'कोण = |३० x {dev(h)} - ५.५ x {dev(m)}| = {dev_num(ang)} डिग्री।')

n = em.write('expansion-r10-maths3.json')
print('MATHS3 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
