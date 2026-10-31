#!/usr/bin/env python3
"""R10 generator 19: more computed maths 4 (~3,500). Percentages of big
numbers, averages of ranges, ratio word problems with names, trains (new
speeds), 3-worker work, SI/CI new values, number series new patterns,
calendar 2036-2045, HCF/LCM pairs new ranges, decimal multiplication,
area/volume, profit/loss with two items, partnership, boats with distance."""
import sys, random, math, datetime
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num, fmt

bank = Bank()
em = Emitter(bank, 'R10-MATH4')
rng = random.Random(71111)
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

def E(sub, diff, q, qn, o, on, expl, expln, exams=EX):
    em.emit(exams, 'Maths & Numerical', sub, diff, 2, q, qn, o, on, 0, expl, expln)

NAMES = ['Ram', 'Hari', 'Sita', 'Gita', 'Shyam', 'Rita', 'Mohan', 'Sarita', 'Binod', 'Sunita']
NAMES_NE = ['राम', 'हरि', 'सीता', 'गीता', 'श्याम', 'रिता', 'मोहन', 'सरिता', 'बिनोद', 'सुनिता']

# ---------- percentages of big numbers ----------
for _ in range(300):
    p = rng.choice([5, 8, 10, 12, 15, 18, 20, 25, 30, 35, 40, 45, 50, 60, 65, 70, 75, 80, 85, 90, 95])
    n = rng.choice([120, 150, 200, 250, 300, 400, 500, 600, 800, 1000, 1200, 1500, 2000, 2500, 4000, 5000])
    ans = p * n // 100
    if p * n % 100: continue
    o, on, _ = num_opts(ans, [ans+10, ans-10, ans+50, ans-50])
    E('Percentage', 'easy', f'What is {p}% of {n}?', f'{dev(n)} को {dev(p)}% कति हो?',
      o, on, f'{p}% of {n} = {n} x {p}/100 = {ans}.', f'{dev(n)} को {dev(p)}% = {dev(n)} x {dev(p)}/१०० = {dev_num(ans)}।')

# ---------- find the number from % ----------
for _ in range(150):
    p = rng.choice([10, 20, 25, 40, 50, 60, 75, 80])
    part = rng.choice([20, 40, 50, 60, 80, 100, 120, 150, 200, 240, 300, 400])
    whole = part * 100 // p
    if part * 100 % p: continue
    o, on, _ = num_opts(whole, [whole+10, whole-10, whole+50, whole-50])
    E('Percentage', 'medium', f'{p}% of a number is {part}. What is the number?', f'एउटा सङ्ख्याको {dev(p)}% भनेको {dev(part)} हो। त्यो सङ्ख्या कति हो?',
      o, on, f'Number = {part} x 100 / {p} = {whole}.', f'सङ्ख्या = {dev(part)} x १०० / {dev(p)} = {dev_num(whole)}।')

# ---------- A as % of B ----------
for _ in range(150):
    b = rng.choice([200, 250, 400, 500, 800, 1000, 2000])
    p = rng.choice([10, 20, 25, 40, 50, 60, 75, 80, 90])
    a = b * p // 100
    if b * p % 100: continue
    o, on, _ = num_opts(p, [p+5, p-5, p+10, p-10])
    E('Percentage', 'medium', f'{a} is what percent of {b}?', f'{dev(a)} भनेको {dev(b)} को कति प्रतिशत हो?',
      o, on, f'{a}/{b} x 100 = {p}%.', f'{dev(a)}/{dev(b)} x १०० = {dev(p)}%।')

# ---------- averages of ranges ----------
for n in range(11, 51):
    # average of first n even numbers = n+1
    ans = n + 1
    o, on, _ = num_opts(ans, [ans+1, ans-1, ans+2, ans-2])
    E('Averages', 'medium', f'What is the average of the first {n} even numbers?', f'पहिलो {dev(n)} वटा जोर सङ्ख्याहरूको औसत कति हो?',
      o, on, f'Average of first {n} even numbers = {n} + 1 = {ans}.', f'पहिलो {dev(n)} वटा जोर सङ्ख्याहरूको औसत = {dev(n)} + १ = {dev_num(ans)}।')
for n in range(11, 51):
    # average of first n odd numbers = n
    ans = n
    o, on, _ = num_opts(ans, [ans+1, ans-1, ans+2, ans-2])
    E('Averages', 'medium', f'What is the average of the first {n} odd numbers?', f'पहिलो {dev(n)} वटा विजोर सङ्ख्याहरूको औसत कति हो?',
      o, on, f'Average of first {n} odd numbers = {n}.', f'पहिलो {dev(n)} वटा विजोर सङ्ख्याहरूको औसत = {dev_num(ans)}।')
for _ in range(100):
    a = rng.randint(2, 50)
    n = rng.randint(4, 12)
    # average of n consecutive numbers starting at a = a + (n-1)/2
    s = sum(range(a, a+n))
    ans = s // n
    if s % n: continue
    o, on, _ = num_opts(ans, [ans+1, ans-1, ans+2, ans-2])
    E('Averages', 'medium', f'What is the average of {a}, {a+1}, ..., {a+n-1}?', f'{dev(a)}, {dev(a+1)}, ..., {dev(a+n-1)} को औसत कति हो?',
      o, on, f'Sum = {s}, count = {n}, average = {s}/{n} = {ans}.', f'योग = {dev_num(s)}, सङ्ख्या = {dev(n)}, औसत = {dev_num(s)}/{dev(n)} = {dev_num(ans)}।')

# ---------- ratio word problems with names ----------
for _ in range(200):
    n1, n2 = rng.sample(NAMES, 2)
    n1n, n2n = NAMES_NE[NAMES.index(n1)], NAMES_NE[NAMES.index(n2)]
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    if a == b: continue
    tot = rng.randint(5, 25) * (a+b)
    share = tot * a // (a+b)
    o, on, _ = num_opts(share, [share+10, share-10, share+20, share-20])
    E('Ratio & Proportion', 'medium', f'{n1} and {n2} divide Rs {tot} in the ratio {a}:{b}. How much does {n1} get?',
      f'{n1n} र {n2n} ले रु {dev_num(tot)} लाई {dev(a)}:{dev(b)} को अनुपातमा बाँड्छन्। {n1n} ले कति पाउँछ?',
      o, on, f'{n1}\'s share = {tot} x {a}/{a+b} = {share}.', f'{n1n} को भाग = {dev_num(tot)} x {dev(a)}/{dev(a+b)} = {dev_num(share)}।')

# ---------- trains: new speeds/lengths ----------
for _ in range(150):
    length = rng.choice([120, 150, 180, 200, 240, 270, 300, 360, 400, 450])
    speed = rng.choice([36, 45, 54, 63, 72, 81, 90, 108])
    ms = speed * 5 // 18
    t = length / ms
    if t != int(t): continue
    t = int(t)
    o, on, _ = num_opts(t, [t+2, t-2, t+5, t-5])
    E('Trains', 'medium', f'A train of length {length} m runs at {speed} km/h. How long does it take to cross a pole?',
      f'{dev(length)} मिटर लामो रेल {dev(speed)} किमी/घण्टाको गतिमा दौडिरहेको छ। खम्बा पार गर्न कति समय लाग्छ?',
      o, on, f'Speed = {speed} km/h = {ms} m/s. Time = {length}/{ms} = {t} seconds.', f'गति = {dev(speed)} किमी/घण्टा = {dev(ms)} मिटर/सेकेन्ड। समय = {dev(length)}/{dev(ms)} = {dev(t)} सेकेन्ड।')

# ---------- 3-worker work ----------
for _ in range(150):
    a, b, c = rng.randint(4, 20), rng.randint(4, 20), rng.randint(4, 20)
    if len({a, b, c}) < 3: continue
    rate = 1/a + 1/b + 1/c
    t = 1 / rate
    if abs(t - round(t)) > 0.001: continue
    t = int(round(t))
    o, on, _ = num_opts(t, [t+1, t-1, t+2, t-2])
    E('Work & Time', 'hard', f'A can do a work in {a} days, B in {b} days and C in {c} days. In how many days can they together finish the work?',
      f'A ले एउटा काम {dev(a)} दिनमा, B ले {dev(b)} दिनमा र C ले {dev(c)} दिनमा गर्न सक्छन्। उनीहरू मिलेर त्यो काम कति दिनमा सक्न सक्छन्?',
      o, on, f'Combined rate = 1/{a} + 1/{b} + 1/{c} = 1/{t}, so time = {t} days.', f'संयुक्त दर = १/{dev(a)} + १/{dev(b)} + १/{dev(c)} = १/{dev(t)}, त्यसैले समय = {dev(t)} दिन।')

# ---------- SI new values ----------
for _ in range(150):
    P = rng.choice([1500, 2500, 3000, 3500, 4500, 6000, 7000, 9000, 11000, 13000, 18000, 22000, 30000, 35000, 45000, 60000])
    R = rng.choice([3, 4, 6, 7, 8, 9, 11, 12, 14, 16, 18])
    T = rng.choice([2, 3, 4, 5, 6, 8])
    si = P * R * T // 100
    if P * R * T % 100: continue
    o, on, _ = num_opts(si, [si+50, si-50, si+100, si-100])
    E('Simple Interest', 'medium', f'What is the simple interest on Rs {P} at {R}% per annum for {T} years?',
      f'रु {dev_num(P)} मा {dev(R)}% वार्षिक दरले {dev(T)} वर्षको साधारण ब्याज कति हो?',
      o, on, f'SI = {P} x {R} x {T} / 100 = {si}.', f'साधारण ब्याज = {dev_num(P)} x {dev(R)} x {dev(T)} / १०० = {dev_num(si)}।')

# ---------- CI 3 years (rate 10/20) ----------
for _ in range(60):
    P = rng.choice([1000, 2000, 5000, 10000, 20000, 40000, 50000, 80000, 100000])
    R = rng.choice([10, 20])
    amt = P * (1 + R/100)**3
    if amt != int(amt): continue
    amt = int(amt)
    ci = amt - P
    o, on, _ = num_opts(ci, [ci+100, ci-100, ci+500, ci-500])
    E('Compound Interest', 'hard', f'What is the compound interest on Rs {P} at {R}% per annum for 3 years?',
      f'रु {dev_num(P)} मा {dev(R)}% वार्षिक दरले ३ वर्षको चक्रवृद्धि ब्याज कति हो?',
      o, on, f'Amount = {P} x (1 + {R}/100)^3 = {amt}; CI = {amt} - {P} = {ci}.', f'मिश्रधन = {dev_num(P)} x (१ + {dev(R)}/१००)^३ = {dev_num(amt)}; चक्रवृद्धि ब्याज = {dev_num(amt)} - {dev_num(P)} = {dev_num(ci)}।', exams=EXH)

# ---------- number series new patterns ----------
def series_q(seq, nxt):
    s = ', '.join(str(x) for x in seq)
    sn = ', '.join(dev_num(x) for x in seq)
    o, on, _ = num_opts(nxt, [nxt+1, nxt-1, nxt+2, nxt-2])
    E('Number Series', 'hard', f'What is the next number in the series: {s}, ...?', f'श्रेणी {sn}, ... मा अर्को सङ्ख्या कति हो?',
      o, on, f'The next term is {nxt}.', f'अर्को पद {dev_num(nxt)} हो।')
for n0 in range(2, 16):
    seq = [i*i*i + i for i in range(n0, n0+4)]
    series_q(seq, (n0+4)**3 + (n0+4))
    seq = [i*i*i - i for i in range(n0, n0+4)]
    series_q(seq, (n0+4)**3 - (n0+4))
for n0 in [2, 3, 4, 5]:
    seq = [n0]
    for _ in range(3): seq.append(seq[-1]*2 - 1)
    series_q(seq, seq[-1]*2 - 1)
    seq = [n0]
    for _ in range(3): seq.append(seq[-1]*3 + 1)
    series_q(seq, seq[-1]*3 + 1)
for n0 in range(3, 20):
    seq = [n0, n0+2, n0+6, n0+12]
    series_q(seq, n0+20)
for n0 in range(2, 12):
    seq = [2**i + n0 for i in range(4)]
    series_q(seq, 2**4 + n0)

# ---------- calendar 2036-2045 ----------
start = datetime.date(2036, 1, 1)
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days_ne = ['सोमबार', 'मङ्गलबार', 'बुधबार', 'बिहीबार', 'शुक्रबार', 'शनिबार', 'आइतबार']
for _ in range(200):
    d = start + datetime.timedelta(days=rng.randint(0, 3600))
    wd = d.weekday()
    correct = days[wd]
    ds = [x for x in days if x != correct]
    rng.shuffle(ds)
    o = [correct] + ds[:3]
    on = [days_ne[wd]] + [days_ne[days.index(x)] for x in ds[:3]]
    em.emit(EX, 'Maths & Numerical', 'Calendar', 'medium', 2,
            f'What day of the week will {d.day} {d.strftime("%B")} {d.year} be?',
            f'{dev(d.year)} {d.strftime("%B")} {dev(d.day)} कुन बार पर्नेछ?',
            o, on, 0, f'{d.day} {d.strftime("%B")} {d.year} will be a {correct}.',
            f'{dev(d.year)} {d.strftime("%B")} {dev(d.day)} {days_ne[wd]} पर्नेछ।')

# ---------- HCF/LCM pairs new ranges ----------
for _ in range(200):
    a, b = rng.randint(16, 60), rng.randint(16, 60)
    if a == b: continue
    if rng.random() < 0.5:
        ans = math.lcm(a, b)
        o, on, _ = num_opts(ans, [ans+a, ans-a, ans*2, ans//2 if ans % 2 == 0 else ans+b])
        E('HCF & LCM', 'medium', f'What is the LCM of {a} and {b}?', f'{dev(a)} र {dev(b)} को लस कति हो?',
          o, on, f'LCM({a}, {b}) = {ans}.', f'लस ({dev(a)}, {dev(b)}) = {dev_num(ans)}।')
    else:
        ans = math.gcd(a, b)
        o, on, _ = num_opts(ans, [ans+1, ans+2, ans*2, ans+3])
        E('HCF & LCM', 'medium', f'What is the HCF of {a} and {b}?', f'{dev(a)} र {dev(b)} को मस कति हो?',
          o, on, f'HCF({a}, {b}) = {ans}.', f'मस ({dev(a)}, {dev(b)}) = {dev_num(ans)}।')

# ---------- decimal multiplication ----------
for _ in range(150):
    a = rng.choice([1.5, 2.5, 3.5, 4.5, 0.5, 1.25, 2.25, 0.25, 0.75, 1.75, 3.25])
    b = rng.choice([2, 3, 4, 5, 6, 8, 10, 12, 20])
    ans = round(a * b, 2)
    o = [fmt(ans), fmt(ans+1), fmt(ans-1), fmt(round(ans+0.5, 2))]
    on = [dev_num(ans), dev_num(ans+1), dev_num(ans-1), dev_num(round(ans+0.5, 2))]
    E('Decimals', 'medium', f'What is {a} x {b}?', f'{dev(a)} x {dev(b)} कति हो?',
      o, on, f'{a} x {b} = {ans}.', f'{dev(a)} x {dev(b)} = {dev_num(ans)}।')

# ---------- area / volume ----------
for _ in range(80):
    l, w = rng.randint(3, 30), rng.randint(3, 30)
    ans = l * w
    o, on, _ = num_opts(ans, [ans+l, ans-l, ans+w, ans-w])
    E('Area & Volume', 'easy', f'What is the area of a rectangle {l} m long and {w} m wide?', f'{dev(l)} मिटर लामो र {dev(w)} मिटर चौडा आयतको क्षेत्रफल कति हो?',
      o, on, f'Area = {l} x {w} = {ans} sq m.', f'क्षेत्रफल = {dev(l)} x {dev(w)} = {dev_num(ans)} वर्ग मिटर।')
for _ in range(80):
    s = rng.randint(2, 20)
    ans = s**3
    o, on, _ = num_opts(ans, [ans+s, ans-s, ans+10, ans-10])
    E('Area & Volume', 'medium', f'What is the volume of a cube with side {s} cm?', f'{dev(s)} सेमी भुजा भएको घनको आयतन कति हो?',
      o, on, f'Volume = {s}^3 = {ans} cubic cm.', f'आयतन = {dev(s)}^३ = {dev_num(ans)} घन सेमी।')
for _ in range(80):
    r = rng.choice([7, 14, 21, 28, 35])
    ans = 22 * r * r // 7
    o, on, _ = num_opts(ans, [ans+10, ans-10, ans+100, ans-100])
    E('Area & Volume', 'medium', f'What is the area of a circle with radius {r} cm? (Use pi = 22/7)', f'{dev(r)} सेमी अर्धव्यास भएको वृत्तको क्षेत्रफल कति हो? (pi = २२/७ प्रयोग गर्नुहोस्)',
      o, on, f'Area = 22/7 x {r} x {r} = {ans} sq cm.', f'क्षेत्रफल = २२/७ x {dev(r)} x {dev(r)} = {dev_num(ans)} वर्ग सेमी।')
for _ in range(60):
    l, w, h = rng.randint(2, 12), rng.randint(2, 12), rng.randint(2, 12)
    ans = l * w * h
    o, on, _ = num_opts(ans, [ans+10, ans-10, ans+20, ans-20])
    E('Area & Volume', 'medium', f'What is the volume of a cuboid {l} cm long, {w} cm wide and {h} cm high?', f'{dev(l)} सेमी लामो, {dev(w)} सेमी चौडा र {dev(h)} सेमी अग्लो घनाभको आयतन कति हो?',
      o, on, f'Volume = {l} x {w} x {h} = {ans} cubic cm.', f'आयतन = {dev(l)} x {dev(w)} x {dev(h)} = {dev_num(ans)} घन सेमी।')

# ---------- profit/loss with two items (same CP) ----------
for _ in range(100):
    cp = rng.choice([200, 400, 500, 800, 1000, 2000])
    p = rng.choice([10, 20, 25])
    l = rng.choice([10, 20, 25])
    sp1 = cp * (100+p)//100
    sp2 = cp * (100-l)//100
    if p == l:
        net = 0
        q = f'A man buys two articles for Rs {cp} each. He sells one at a profit of {p}% and the other at a loss of {l}%. What is his overall profit or loss?'
        qn = f'एक व्यक्तिले दुई सामान रु {dev_num(cp)} मा किन्छ। एउटा {dev(p)}% नाफामा र अर्को {dev(l)}% घाटामा बेच्छ। उसको समग्र नाफा वा घाटा कति हो?'
        o = ['No profit, no loss', f'Profit of Rs {cp*p//100}', f'Loss of Rs {cp*p//100}', f'Profit of Rs {cp*2*p//100}']
        on = ['न नाफा, न घाटा', f'रु {dev_num(cp*p//100)} नाफा', f'रु {dev_num(cp*p//100)} घाटा', f'रु {dev_num(cp*2*p//100)} नाफा']
        em.emit(EX, 'Maths & Numerical', 'Profit & Loss', 'hard', 2, q, qn, o, on, 0,
                'The profit and loss cancel out. The answer is no profit, no loss.',
                'नाफा र घाटा रद्द हुन्छन्। उत्तर: न नाफा, न घाटा।')
    else:
        net = sp1 + sp2 - 2*cp
        if net > 0:
            q = f'A man buys two articles for Rs {cp} each. He sells one at a profit of {p}% and the other at a loss of {l}%. What is his overall profit?'
            qn = f'एक व्यक्तिले दुई सामान रु {dev_num(cp)} मा किन्छ। एउटा {dev(p)}% नाफामा र अर्को {dev(l)}% घाटामा बेच्छ। उसको समग्र नाफा कति हो?'
            ans = net
        else:
            q = f'A man buys two articles for Rs {cp} each. He sells one at a profit of {p}% and the other at a loss of {l}%. What is his overall loss?'
            qn = f'एक व्यक्तिले दुई सामान रु {dev_num(cp)} मा किन्छ। एउटा {dev(p)}% नाफामा र अर्को {dev(l)}% घाटामा बेच्छ। उसको समग्र घाटा कति हो?'
            ans = -net
        o, on, _ = num_opts(ans, [ans+20, ans-20, ans+50, ans-50])
        E('Profit & Loss', 'hard', q, qn, o, on,
          f'Total CP = {2*cp}, total SP = {sp1+sp2}. Difference = {ans}.',
          f'कुल क्रय मूल्य = {dev_num(2*cp)}, कुल विक्रय मूल्य = {dev_num(sp1+sp2)}। अन्तर = {dev_num(ans)}।')

# ---------- partnership ----------
for _ in range(100):
    c1 = rng.choice([2000, 4000, 5000, 8000, 10000])
    c2 = rng.choice([3000, 4000, 6000, 8000, 12000])
    t1 = rng.choice([6, 12])
    t2 = rng.choice([6, 12])
    # profit share proportional to capital x time
    p1 = c1 * t1
    p2 = c2 * t2
    tot = rng.choice([7000, 14000, 21000, 28000, 35000])
    # make tot divisible by (p1+p2)/gcd
    g = math.gcd(p1, p2)
    unit = (p1 + p2) // g
    if tot % unit: continue
    share1 = tot * p1 // (p1 + p2)
    o, on, _ = num_opts(share1, [share1+500, share1-500, share1+1000, share1-1000])
    E('Partnership', 'hard', f'A invests Rs {c1} for {t1} months and B invests Rs {c2} for {t2} months. If the total profit is Rs {tot}, what is A\'s share?',
      f'A ले रु {dev_num(c1)} {dev(t1)} महिनाका लागि र B ले रु {dev_num(c2)} {dev(t2)} महिनाका लागि लगानी गर्छन्। कुल नाफा रु {dev_num(tot)} भए A को भाग कति हो?',
      o, on, f'Profit ratio = {c1}x{t1} : {c2}x{t2} = {p1}:{p2}. A\'s share = {tot} x {p1}/{p1+p2} = {share1}.',
      f'नाफा अनुपात = {dev_num(c1)}x{dev(t1)} : {dev_num(c2)}x{dev(t2)} = {dev_num(p1)}:{dev_num(p2)}। A को भाग = {dev_num(tot)} x {dev_num(p1)}/{dev_num(p1+p2)} = {dev_num(share1)}।', exams=EXH)

# ---------- boats with distance ----------
for _ in range(100):
    v = rng.choice([6, 8, 10, 12, 15])
    u = rng.choice([2, 3, 4, 5])
    if u >= v: continue
    d = rng.choice([24, 30, 36, 40, 48, 60, 72, 90, 120])
    t = d / (v - u)
    if t != int(t): continue
    t = int(t)
    o, on, _ = num_opts(t, [t+1, t-1, t+2, t-2])
    E('Boats & Streams', 'hard', f'A boat goes {d} km upstream. If the speed of the boat in still water is {v} km/h and the speed of the stream is {u} km/h, how long does it take?',
      f'एउटा डुङ्गा {dev(d)} किमी उल्टो धारमा जान्छ। स्थिर पानीमा डुङ्गाको गति {dev(v)} किमी/घण्टा र धारको गति {dev(u)} किमी/घण्टा भए कति समय लाग्छ?',
      o, on, f'Upstream speed = {v} - {u} = {v-u} km/h. Time = {d}/{v-u} = {t} hours.', f'उल्टो धारको गति = {dev(v)} - {dev(u)} = {dev(v-u)} किमी/घण्टा। समय = {dev(d)}/{dev(v-u)} = {dev(t)} घण्टा।', exams=EXH)

n = em.write('expansion-r10-maths4.json')
print('MATHS4 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
