#!/usr/bin/env python3
"""R10 generator 3: more computed maths (~3,800). Median/mode/range, SI
variants (find P/R/T), trains crossing platforms, boats & streams, work with
3 workers, pipes, mixtures, ratio-age, geometry (triangle/square/volume/
circumference), percentage salary problems, partnership."""
import sys, random, math
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
em = Emitter(bank, 'R10-MATH2')
rng = random.Random(92003)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'police', 'army', 'tsc-primary', 'tsc-secondary']
EXH = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'csit-entrance', 'ioe-entrance', 'mecee-bl']

def num_opts(correct, cands):
    out = [correct]
    for c in cands:
        if len(out) == 4:
            break
        if c not in out and c is not None:
            out.append(c)
    d = 1
    while len(out) < 4:
        for c in (correct + d, correct - d, correct + 10 * d):
            if c not in out and c > 0:
                out.append(c)
                break
        d += 1
    return [fmt(x) for x in out], [dev_num(x) for x in out], 0

def rs_opts(correct, cands):
    o = num_opts(correct, cands)
    return ['Rs ' + x for x in o[0]], ['रू ' + x for x in o[1]], 0

# ---------------- 1. Median / mode / range of small data ----------------
for _ in range(300):
    n = rng.choice([5, 7, 9])
    nums = sorted(rng.sample(range(5, 99), n))
    med = nums[n // 2]
    oe, on, a = num_opts(med, [nums[0], nums[-1], sum(nums) // n, med + 2])
    lst = ', '.join(str(x) for x in nums)
    lstn = ', '.join(dev_num(x) for x in nums)
    em.emit(EX, 'Maths & Numerical', 'Statistics', 'medium', 2,
            f'Find the median of {lst}.', f'{lstn} को मध्यिका (median) कति हो?',
            oe, on, a,
            f'Arranged in order, the middle value of {n} numbers is the {ord_s(n // 2 + 1)} value, {med}.',
            f'क्रममा मिलाउँदा {dev_num(n)} वटा सङ्ख्यामध्ये बीचको {dev_num(n // 2 + 1)}औँ मान {dev_num(med)} हो।')
for _ in range(200):
    base = rng.sample(range(2, 40), 4)
    mode = rng.choice(base)
    nums = base + [mode, mode]
    rng.shuffle(nums)
    s = sum(nums)
    mean = s / len(nums)
    oe, on, a = num_opts(mode, [x for x in base if x != mode][:3])
    lst = ', '.join(str(x) for x in nums)
    lstn = ', '.join(dev_num(x) for x in nums)
    em.emit(EX, 'Maths & Numerical', 'Statistics', 'medium', 2,
            f'Find the mode of {lst}.', f'{lstn} को बहुलक (mode) कति हो?',
            oe, on, a,
            f'The value {mode} occurs most often (3 times), so the mode is {mode}.',
            f'{dev_num(mode)} सबैभन्दा धेरै पटक (३ पटक) आएको छ, त्यसैले बहुलक {dev_num(mode)} हो।')
for _ in range(200):
    nums = sorted(rng.sample(range(5, 120), rng.choice([5, 6, 7])))
    rg = nums[-1] - nums[0]
    oe, on, a = num_opts(rg, [nums[-1], nums[0], rg + 5, rg - 5])
    lst = ', '.join(str(x) for x in nums)
    lstn = ', '.join(dev_num(x) for x in nums)
    em.emit(EX, 'Maths & Numerical', 'Statistics', 'easy', 1,
            f'Find the range of {lst}.', f'{lstn} को परिसर (range) कति हो?',
            oe, on, a,
            f'Range = largest - smallest = {nums[-1]} - {nums[0]} = {rg}.',
            f'परिसर = सबैभन्दा ठूलो − सबैभन्दा सानो = {dev_num(nums[-1])} − {dev_num(nums[0])} = {dev_num(rg)}।')

# ---------------- 2. SI variants: find P, R, T ----------------
for P in [2000, 4000, 5000, 8000, 10000, 12000, 20000]:
    for R in [5, 8, 10, 12]:
        for T in [2, 3, 4, 5]:
            si = P * R * T // 100
            if P * R * T % 100:
                continue
            # find principal
            oe, on, a = rs_opts(P, [P + 1000, P - 1000, si, P + 500])
            em.emit(EX, 'Maths & Numerical', 'Simple Interest', 'hard', 2,
                    f'At {R}% per annum simple interest, Rs {si} interest is earned in {T} years. What was the principal?',
                    f'{dev(fmt(R))}% वार्षिक साधारण ब्याजमा {dev_num(T)} वर्षमा रु {dev_num(si)} ब्याज पाइयो। मूलधन कति थियो?',
                    oe, on, a,
                    f'P = SI x 100 / (R x T) = {si} x 100 / ({R} x {T}) = Rs {P}.',
                    f'मूलधन = ब्याज × १०० / (दर × समय) = {dev_num(si)} × १०० / ({dev(fmt(R))} × {dev_num(T)}) = रु {dev_num(P)}।')
            # find rate
            oe, on, a = num_opts(R, [R + 2, R - 2, R + 5, R * 2])
            em.emit(EX, 'Maths & Numerical', 'Simple Interest', 'hard', 2,
                    f'In how many percent per annum simple interest does Rs {P} earn Rs {si} interest in {T} years?',
                    f'रु {dev_num(P)} ले {dev_num(T)} वर्षमा रु {dev_num(si)} साधारण ब्याज पाउन ब्याजदर कति प्रतिशत हुनुपर्छ?',
                    [fmt(x) + '%' for x in oe], [dev_num(x) + '%' for x in on], a,
                    f'R = SI x 100 / (P x T) = {si} x 100 / ({P} x {T}) = {R}%.',
                    f'दर = ब्याज × १०० / (मूलधन × समय) = {dev_num(si)} × १०० / ({dev_num(P)} × {dev_num(T)}) = {dev(fmt(R))}%।')
            # find time
            oe, on, a = num_opts(T, [T + 1, T - 1, T + 2, T * 2])
            em.emit(EX, 'Maths & Numerical', 'Simple Interest', 'hard', 2,
                    f'In how many years does Rs {P} earn Rs {si} simple interest at {R}% per annum?',
                    f'रु {dev_num(P)} ले {dev(fmt(R))}% वार्षिक साधारण ब्याजमा रु {dev_num(si)} ब्याज पाउन कति वर्ष लाग्छ?',
                    [fmt(x) + ' years' for x in oe], [dev_num(x) + ' वर्ष' for x in on], a,
                    f'T = SI x 100 / (P x R) = {si} x 100 / ({P} x {R}) = {T} years.',
                    f'समय = ब्याज × १०० / (मूलधन × दर) = {dev_num(si)} × १०० / ({dev_num(P)} × {dev(fmt(R))}) = {dev_num(T)} वर्ष।')

# ---------------- 3. Trains crossing a platform ----------------
for L in [120, 150, 180, 200, 240]:
    for P in [180, 200, 240, 300, 360]:
        for v in [36, 54, 72, 90]:
            t = Fraction((L + P) * 18, v * 5)
            if t.denominator != 1:
                continue
            t = int(t)
            oe, on, a = num_opts(t, [t + 2, t - 2, t + 5, L // 10])
            em.emit(EXH, 'Maths & Numerical', 'Trains', 'hard', 2,
                    f'A train {L} m long running at {v} km/h crosses a {P} m long platform. How long does it take?',
                    f'{dev_num(L)} मिटर लामो रेल {dev_num(v)} किमी/घण्टाको गतिमा {dev_num(P)} मिटर लामो प्लेटफर्म पार गर्न कति समय लगाउँछ?',
                    [fmt(x) + ' seconds' for x in oe], [dev_num(x) + ' सेकेन्ड' for x in on], a,
                    f'Distance = {L} + {P} = {L + P} m. Speed = {v} x 5/18 = {v * 5 // 18} m/s. Time = {L + P}/{v * 5 // 18} = {t} seconds.',
                    f'दूरी = {dev_num(L)} + {dev_num(P)} = {dev_num(L + P)} मी। गति = {dev_num(v)} × ५/१८ = {dev_num(v * 5 // 18)} मी/से। समय = {dev_num(L + P)}/{dev_num(v * 5 // 18)} = {dev_num(t)} सेकेन्ड।')

# ---------------- 4. Boats & streams ----------------
for b in [8, 10, 12, 15, 18, 20]:
    for s in [2, 3, 4, 5, 6]:
        if b <= s:
            continue
        down = b + s
        up = b - s
        oe, on, a = num_opts(down, [b, up, down + 2, down - 2])
        em.emit(EXH, 'Maths & Numerical', 'Boats & Streams', 'hard', 2,
                f'A boat moves at {b} km/h in still water and the stream flows at {s} km/h. What is the downstream speed?',
                f'डुङ्गा स्थिर पानीमा {dev_num(b)} किमी/घण्टा र खोला {dev_num(s)} किमी/घण्टाको गतिमा बग्छ। बगावको दिशामा (downstream) गति कति हो?',
                [fmt(x) + ' km/h' for x in oe], [dev_num(x) + ' किमी/घण्टा' for x in on], a,
                f'Downstream speed = boat speed + stream speed = {b} + {s} = {down} km/h.',
                f'बगावको दिशामा गति = डुङ्गाको गति + खोलाको गति = {dev_num(b)} + {dev_num(s)} = {dev_num(down)} किमी/घण्टा।')
        oe, on, a = num_opts(up, [b, down, up + 2, up - 2])
        em.emit(EXH, 'Maths & Numerical', 'Boats & Streams', 'hard', 2,
                f'A boat moves at {b} km/h in still water and the stream flows at {s} km/h. What is the upstream speed?',
                f'डुङ्गा स्थिर पानीमा {dev_num(b)} किमी/घण्टा र खोला {dev_num(s)} किमी/घण्टाको गतिमा बग्छ। बगावको विपरीत दिशामा (upstream) गति कति हो?',
                [fmt(x) + ' km/h' for x in oe], [dev_num(x) + ' किमी/घण्टा' for x in on], a,
                f'Upstream speed = boat speed - stream speed = {b} - {s} = {up} km/h.',
                f'बगावको विपरीत दिशामा गति = डुङ्गाको गति − खोलाको गति = {dev_num(b)} − {dev_num(s)} = {dev_num(up)} किमी/घण्टा।')

# ---------------- 5. Work: 3 workers / pipes ----------------
for a, b, c in [(6, 12, 12), (4, 8, 8), (5, 10, 10), (3, 6, 6), (8, 16, 16), (10, 20, 20), (4, 6, 12), (6, 8, 24), (5, 15, 15), (3, 9, 9)]:
    t = Fraction(1, Fraction(1, a) + Fraction(1, b) + Fraction(1, c))
    if t.denominator != 1:
        continue
    t = int(t)
    oe, on, ai = num_opts(t, [t + 1, t + 2, a, b])
    em.emit(EXH, 'Maths & Numerical', 'Work & Time', 'hard', 2,
            f'A can do a work in {a} days, B in {b} days and C in {c} days. Working together, in how many days will they finish it?',
            f'A ले काम {dev_num(a)} दिनमा, B ले {dev_num(b)} दिनमा र C ले {dev_num(c)} दिनमा सक्छन्। तीनैजना मिलेर काम कति दिनमा सकिन्छ?',
            [fmt(x) + ' days' for x in oe], [dev_num(x) + ' दिन' for x in on], ai,
            f'Together they do 1/{a} + 1/{b} + 1/{c} = 1/{t} of the work per day, so they need {t} days.',
            f'तीनैजनाले प्रतिदिन १/{dev_num(a)} + १/{dev_num(b)} + १/{dev_num(c)} = १/{dev_num(t)} भाग काम गर्छन्, त्यसैले {dev_num(t)} दिन लाग्छ।')
# pipes: fill in a hrs, empty in b hrs -> net fill time
for a in [4, 6, 8, 10, 12]:
    for b in [6, 8, 12, 16, 20, 24]:
        if b <= a:
            continue
        t = Fraction(a * b, b - a)
        if t.denominator != 1:
            continue
        t = int(t)
        oe, on, ai = num_opts(t, [t + 2, t - 2, a + b, a])
        em.emit(EXH, 'Maths & Numerical', 'Work & Time', 'hard', 2,
                f'A pipe fills a tank in {a} hours and another pipe empties it in {b} hours. If both are opened together, in how many hours will the empty tank fill?',
                f'एउटा पाइपले ट्याङ्की {dev_num(a)} घण्टामा भर्छ र अर्को पाइपले {dev_num(b)} घण्टामा खाली गर्छ। दुवै एकैसाथ खोल्दा खाली ट्याङ्की कति घण्टामा भरिन्छ?',
                [fmt(x) + ' hours' for x in oe], [dev_num(x) + ' घण्टा' for x in on], ai,
                f'Net fill per hour = 1/{a} - 1/{b} = {b - a}/{a * b}, so the tank fills in {a * b}/{b - a} = {t} hours.',
                f'प्रतिघण्टा शुद्ध भराइ = १/{dev_num(a)} − १/{dev_num(b)} = {dev_num(b - a)}/{dev_num(a * b)} भएकाले ट्याङ्की {dev_num(a * b)}/{dev_num(b - a)} = {dev_num(t)} घण्टामा भरिन्छ।')

# ---------------- 6. Mixtures ----------------
for p1 in [20, 30, 40, 50, 60]:
    for p2 in [30, 40, 50, 60, 80]:
        if p1 == p2:
            continue
        for q1, q2 in [(1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)]:
            v = Fraction(p1 * q1 + p2 * q2, q1 + q2)
            if v.denominator != 1:
                continue
            v = int(v)
            oe, on, a = rs_opts(v, [p1, p2, v + 5, v - 5])
            em.emit(EXH, 'Maths & Numerical', 'Mixture & Alligation', 'hard', 2,
                    f'A mixture is made of {q1} kg of rice costing Rs {p1} per kg and {q2} kg costing Rs {p2} per kg. What is the cost of the mixture per kg?',
                    f'{dev_num(q1)} केजी रु {dev_num(p1)} प्रतिकेजीको चामल र {dev_num(q2)} केजी रु {dev_num(p2)} प्रतिकेजीको चामल मिसाइयो। मिश्रणको प्रतिकेजी मूल्य कति हो?',
                    oe, on, a,
                    f'Total cost = {q1} x {p1} + {q2} x {p2} = Rs {p1 * q1 + p2 * q2}. Total weight = {q1 + q2} kg. Cost per kg = {p1 * q1 + p2 * q2}/{q1 + q2} = Rs {v}.',
                    f'कुल मूल्य = {dev_num(q1)} × {dev_num(p1)} + {dev_num(q2)} × {dev_num(p2)} = रु {dev_num(p1 * q1 + p2 * q2)}। कुल तौल = {dev_num(q1 + q2)} केजी। प्रतिकेजी मूल्य = {dev_num(p1 * q1 + p2 * q2)}/{dev_num(q1 + q2)} = रु {dev_num(v)}।')

# ---------------- 7. Ratio of ages ----------------
for r1, r2 in [(2, 3), (3, 4), (4, 5), (3, 5), (5, 7), (2, 5), (5, 6), (4, 7)]:
    for s in [4, 5, 6, 8, 10]:
        a1, a2 = r1 * s, r2 * s
        for after in [4, 5, 6, 10]:
            b1, b2 = a1 + after, a2 + after
            oe, on, ai = num_opts(b1, [a1, b2, b1 + s, b1 - s])
            em.emit(EXH, 'Maths & Numerical', 'Age Problems', 'hard', 2,
                    f'The ratio of the ages of A and B is {r1}:{r2}. If A is {a1} years old now, how old will A be after {after} years?',
                    f'A र B को उमेरको अनुपात {dev(r1)}:{dev(r2)} छ। A अहिले {dev_num(a1)} वर्षका छन् भने {dev_num(after)} वर्षपछि A कति वर्षका हुनेछन्?',
                    [fmt(x) + ' years' for x in oe], [dev_num(x) + ' वर्ष' for x in on], ai,
                    f'A is {a1} years old now. After {after} years A will be {a1} + {after} = {b1} years old.',
                    f'A अहिले {dev_num(a1)} वर्षका छन्। {dev_num(after)} वर्षपछि A {dev_num(a1)} + {dev_num(after)} = {dev_num(b1)} वर्षका हुनेछन्।')

# ---------------- 8. Geometry ----------------
for base in [6, 8, 10, 12, 14, 16, 20]:
    for h in [4, 5, 6, 8, 10, 12]:
        area = base * h // 2
        if base * h % 2:
            continue
        oe, on, a = num_opts(area, [base * h, area + base, area - h, base + h])
        em.emit(EX, 'Maths & Numerical', 'Mensuration', 'easy', 2,
                f'Find the area of a triangle with base {base} cm and height {h} cm.',
                f'आधार {dev_num(base)} सेमी र उचाइ {dev_num(h)} सेमी भएको त्रिभुजको क्षेत्रफल कति हो?',
                [fmt(x) + ' sq cm' for x in oe], [dev_num(x) + ' वर्ग सेमी' for x in on], a,
                f'Area = 1/2 x base x height = 1/2 x {base} x {h} = {area} sq cm.',
                f'क्षेत्रफल = १/२ × आधार × उचाइ = १/२ × {dev_num(base)} × {dev_num(h)} = {dev_num(area)} वर्ग सेमी।')
for s in [4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25]:
    oe, on, a = num_opts(s * s, [s * s + s, s * 4, s * s - s, s * 3])
    em.emit(EX, 'Maths & Numerical', 'Mensuration', 'easy', 1,
            f'Find the area of a square with side {s} cm.',
            f'भुजा {dev_num(s)} सेमी भएको वर्गको क्षेत्रफल कति हो?',
            [fmt(x) + ' sq cm' for x in oe], [dev_num(x) + ' वर्ग सेमी' for x in on], a,
            f'Area = side x side = {s} x {s} = {s * s} sq cm.',
            f'क्षेत्रफल = भुजा × भुजा = {dev_num(s)} × {dev_num(s)} = {dev_num(s * s)} वर्ग सेमी।')
for s in [2, 3, 4, 5, 6, 8, 10]:
    v = s ** 3
    oe, on, a = num_opts(v, [v + s, v - s, s * s, 6 * s * s])
    em.emit(EX, 'Maths & Numerical', 'Mensuration', 'medium', 1,
            f'Find the volume of a cube with side {s} cm.',
            f'भुजा {dev_num(s)} सेमी भएको घनको आयतन कति हो?',
            [fmt(x) + ' cubic cm' for x in oe], [dev_num(x) + ' घन सेमी' for x in on], a,
            f'Volume = side^3 = {s}^3 = {v} cubic cm.',
            f'आयतन = भुजा³ = {dev_num(s)}³ = {dev_num(v)} घन सेमी।')
for r in [7, 14, 21, 28]:
    circ = 2 * 22 * r // 7
    oe, on, a = num_opts(circ, [circ + 22, circ - 22, 22 * r * r // 7, circ + r])
    em.emit(EX, 'Maths & Numerical', 'Mensuration', 'medium', 2,
            f'Find the circumference of a circle of radius {r} cm. (Use pi = 22/7)',
            f'अर्धव्यास {dev_num(r)} सेमी भएको वृत्तको परिधि कति हो? (π = २२/७ लिनुहोस्)',
            [fmt(x) + ' cm' for x in oe], [dev_num(x) + ' सेमी' for x in on], a,
            f'Circumference = 2 x pi x r = 2 x 22/7 x {r} = {circ} cm.',
            f'परिधि = २ × π × r = २ × २२/७ × {dev_num(r)} = {dev_num(circ)} सेमी।')

# ---------------- 9. Salary / expenditure / savings ----------------
for sal in [20000, 25000, 30000, 40000, 50000, 60000]:
    for pct in [10, 20, 25, 30, 40, 50, 60, 75, 80]:
        exp = sal * pct // 100
        if sal * pct % 100:
            continue
        sav = sal - exp
        oe, on, a = rs_opts(sav, [exp, sal, sav + 1000, sav - 1000])
        em.emit(EX, 'Maths & Numerical', 'Percentage', 'medium', 2,
                f'A man earns Rs {sal} per month and spends {pct}% of it. How much does he save per month?',
                f'एक व्यक्तिले महिनामा रु {dev_num(sal)} कमाउँछ र त्यसको {dev(fmt(pct))}% खर्च गर्छ। उसले महिनामा कति बचत गर्छ?',
                oe, on, a,
                f'Expenditure = {pct}% of Rs {sal} = Rs {exp}. Savings = {sal} - {exp} = Rs {sav}.',
                f'खर्च = रु {dev_num(sal)} को {dev(fmt(pct))}% = रु {dev_num(exp)}। बचत = {dev_num(sal)} − {dev_num(exp)} = रु {dev_num(sav)}।')

# ---------------- 10. Partnership ----------------
for c1, c2 in [(20000, 30000), (40000, 60000), (15000, 25000), (30000, 50000), (10000, 40000), (25000, 35000)]:
    for profit in [5000, 10000, 15000, 20000, 25000]:
        total = c1 + c2
        share = profit * c1 // total
        if profit * c1 % total:
            continue
        oe, on, a = rs_opts(share, [profit - share, profit, share + 1000, share - 1000])
        em.emit(EXH, 'Maths & Numerical', 'Partnership', 'hard', 2,
                f"A invests Rs {c1} and B invests Rs {c2} in a business. If the total profit is Rs {profit}, what is A's share?",
                f"A ले रु {dev_num(c1)} र B ले रु {dev_num(c2)} लगानी गरे। कुल नाफा रु {dev_num(profit)} भए A को हिस्सा कति हो?",
                oe, on, a,
                f'Profit is shared in the ratio {c1}:{c2} = {c1 // 10000}:{c2 // 10000}. A gets {c1}/{total} x {profit} = Rs {share}.',
                f'नाफा {dev_num(c1)}:{dev_num(c2)} को अनुपातमा बाँडिन्छ। A ले {dev_num(c1)}/{dev_num(total)} × {dev_num(profit)} = रु {dev_num(share)} पाउँछ।')

# ---------------- 11. Clock: time after interval ----------------
for h in range(1, 13):
    for m in [0, 15, 30, 45]:
        for add in [45, 90, 120, 150]:
            total_min = h * 60 + m + add
            nh = (total_min // 60) % 12
            if nh == 0:
                nh = 12
            nm = total_min % 60
            ans = f'{nh}:{nm:02d}'
            ds = []
            for da in [30, 60, -30]:
                tm = total_min + da
                hh = (tm // 60) % 12
                if hh == 0:
                    hh = 12
                mm = tm % 60
                ds.append(f'{hh}:{mm:02d}')
            opts = [ans] + [d for d in ds if d != ans][:3]
            while len(opts) < 4:
                opts.append(f'{(nh % 12) + 1}:{nm:02d}')
            optsn = [dev(x) for x in opts]
            em.emit(EX, 'IQ & Reasoning', 'Clock', 'easy', 1,
                    f'If it is {h}:{m:02d} now, what time will it be after {add} minutes?',
                    f'अहिले {dev_num(h)}:{dev(f"{m:02d}")} बजेको छ भने {dev_num(add)} मिनेटपछि कति बज्छ?',
                    opts, optsn, 0,
                    f'{h}:{m:02d} + {add} minutes = {ans}.',
                    f'{dev_num(h)}:{dev(f"{m:02d}")} + {dev_num(add)} मिनेट = {dev(ans)}।')

# ---------------- 12. Age equations ----------------
for diff in [4, 5, 6, 8, 10, 12]:
    for b in [8, 10, 12, 15, 18, 20, 24]:
        a = b + diff
        oe, on, ai = num_opts(a, [b, a + diff, a - diff, b + 2 * diff])
        em.emit(EX, 'Maths & Numerical', 'Age Problems', 'easy', 1,
                f'A is {diff} years older than B. If B is {b} years old, how old is A?',
                f'A, B भन्दा {dev_num(diff)} वर्ष जेठा छन्। B {dev_num(b)} वर्षको भए A कति वर्षका छन्?',
                [fmt(x) + ' years' for x in oe], [dev_num(x) + ' वर्ष' for x in on], ai,
                f'A = B + {diff} = {b} + {diff} = {a} years.',
                f'A = B + {dev_num(diff)} = {dev_num(b)} + {dev_num(diff)} = {dev_num(a)} वर्ष।')

n = em.write('expansion-r10-maths2.json')
print('MATHS2 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:10]:
    print('  REJ', r)
