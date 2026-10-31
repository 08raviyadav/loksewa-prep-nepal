#!/usr/bin/env python3
"""R10 generator 21: maths 5, big new parameter spaces (~6,000 candidates).
Decimal division, fraction x whole, fraction / fraction, mixed numbers,
net % change, SI find rate/time, CI half-yearly, average speed round trip,
pipes & cisterns, men-days, age after N years, notes/coins, CP from SP,
MP from SP, alligation, train crossing platform, boat downstream,
ratio simplification, proportion, direct/inverse proportion, calendar
2020-2023, days between dates, leap years, clock coincidence/opposite,
clock angles at arbitrary minutes, squares/cubes of decimals."""
import sys, random, math, datetime
from fractions import Fraction
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num, fmt

bank = Bank()
em = Emitter(bank, 'R10-MATH5')
rng = random.Random(71113)
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

# ---------- decimal division ----------
for _ in range(200):
    a = rng.choice([4.5, 6.3, 7.2, 8.4, 9.6, 10.5, 12.6, 15.0, 18.9, 21.0, 24.5, 27.3, 30.0, 36.0])
    b = rng.choice([1.5, 2.1, 2.4, 2.8, 3.2, 3.5, 4.2, 5.0, 6.3, 7.0])
    ans = round(a / b, 2)
    if abs(a / b - ans) > 0.001: continue
    if ans != int(ans) and abs(ans - round(ans, 1)) > 0.001: continue
    ans = int(ans) if ans == int(ans) else ans
    o = [fmt(ans), fmt(ans+1), fmt(ans-1), fmt(ans+2)]
    on = [dev_num(ans), dev_num(ans+1), dev_num(ans-1), dev_num(ans+2)]
    E('Decimals', 'medium', f'What is {a} divided by {b}?', f'{dev(a)} लाई {dev(b)} ले भाग गर्दा कति हुन्छ?',
      o, on, f'{a} / {b} = {ans}.', f'{dev(a)} / {dev(b)} = {dev_num(ans)}।')

# ---------- fraction x whole number ----------
for _ in range(150):
    a, b = rng.choice([(1,2),(1,3),(2,3),(1,4),(3,4),(2,5),(3,5),(1,6),(5,6),(3,8),(5,8),(2,7),(4,7)])
    n = rng.randint(4, 40)
    ans = Fraction(a, b) * n
    if ans.denominator != 1: continue
    ans = int(ans)
    o, on, _ = num_opts(ans, [ans+1, ans-1, ans+2, ans-2])
    E('Fractions', 'medium', f'What is {a}/{b} x {n}?', f'{dev(a)}/{dev(b)} x {dev(n)} कति हो?',
      o, on, f'{a}/{b} x {n} = {ans}.', f'{dev(a)}/{dev(b)} x {dev(n)} = {dev_num(ans)}।')

# ---------- fraction / fraction ----------
for _ in range(120):
    a = Fraction(rng.randint(1, 8), rng.randint(2, 8))
    b = Fraction(rng.randint(1, 8), rng.randint(2, 8))
    ans = a / b
    if ans.denominator != 1 and ans.numerator > 20: continue
    ans_s = f'{ans.numerator}/{ans.denominator}' if ans.denominator != 1 else str(ans.numerator)
    ans_n = dev(ans.numerator) + '/' + dev(ans.denominator) if ans.denominator != 1 else dev(ans.numerator)
    ds = [ans + Fraction(1, 4), ans - Fraction(1, 4), ans + Fraction(1, 2)]
    o = [ans_s] + [f'{x.numerator}/{x.denominator}' if x.denominator != 1 else str(x.numerator) for x in ds if x > 0][:3]
    on = [ans_n] + [dev(x.numerator) + '/' + dev(x.denominator) if x.denominator != 1 else dev(x.numerator) for x in ds if x > 0][:3]
    while len(o) < 4:
        o.append(f'{ans.numerator+len(o)}/{ans.denominator}'); on.append(dev(ans.numerator+len(o))+'/'+dev(ans.denominator))
    E('Fractions', 'hard', f'What is {a.numerator}/{a.denominator} divided by {b.numerator}/{b.denominator}?',
      f'{dev(a.numerator)}/{dev(a.denominator)} लाई {dev(b.numerator)}/{dev(b.denominator)} ले भाग गर्दा कति हुन्छ?',
      o, on, f'{a.numerator}/{a.denominator} / {b.numerator}/{b.denominator} = {ans_s}.', f'{dev(a.numerator)}/{dev(a.denominator)} / {dev(b.numerator)}/{dev(b.denominator)} = {ans_n}।')

# ---------- mixed numbers ----------
for _ in range(100):
    w1 = rng.randint(1, 9); f1 = Fraction(rng.randint(1, 5), rng.randint(2, 6))
    w2 = rng.randint(1, 9); f2 = Fraction(rng.randint(1, 5), rng.randint(2, 6))
    tot = w1 + f1 + w2 + f2
    if tot.denominator == 1: continue
    ans_s = f'{tot.numerator//tot.denominator} {tot.numerator%tot.denominator}/{tot.denominator}'
    ans_n = dev(tot.numerator//tot.denominator) + ' ' + dev(tot.numerator%tot.denominator) + '/' + dev(tot.denominator)
    ds = [tot + Fraction(1, 4), tot - Fraction(1, 4), tot + Fraction(1, 2)]
    def fmt_mix(x):
        if x.denominator == 1: return str(x.numerator)
        return f'{x.numerator//x.denominator} {x.numerator%x.denominator}/{x.denominator}'
    def fmt_mix_ne(x):
        if x.denominator == 1: return dev(x.numerator)
        return dev(x.numerator//x.denominator) + ' ' + dev(x.numerator%x.denominator) + '/' + dev(x.denominator)
    o = [ans_s] + [fmt_mix(x) for x in ds if x > 0][:3]
    on = [ans_n] + [fmt_mix_ne(x) for x in ds if x > 0][:3]
    while len(o) < 4:
        o.append(fmt_mix(tot + Fraction(len(o), 4))); on.append(fmt_mix_ne(tot + Fraction(len(o), 4)))
    E('Fractions', 'hard', f'What is {w1} {f1.numerator}/{f1.denominator} + {w2} {f2.numerator}/{f2.denominator}?',
      f'{dev(w1)} {dev(f1.numerator)}/{dev(f1.denominator)} + {dev(w2)} {dev(f2.numerator)}/{dev(f2.denominator)} कति हो?',
      o, on, f'The sum is {ans_s}.', f'योग {ans_n} हो।')

# ---------- net % change: increase then decrease ----------
for _ in range(150):
    p = rng.choice([10, 20, 25, 30, 40, 50])
    q = rng.choice([10, 20, 25, 30, 40, 50])
    net = (p - q - p*q/100)
    net = round(net, 2)
    if net == 0: continue
    ans = fmt(net)
    o = [f'{ans}%', f'{fmt(net+5)}%', f'{fmt(net-5)}%', f'{fmt(net+10)}%']
    on = [f'{dev_num(net)}%', f'{dev_num(net+5)}%', f'{dev_num(net-5)}%', f'{dev_num(net+10)}%']
    if net > 0:
        ans = fmt(net)
        o = [f'{ans}%', f'{fmt(net+5)}%', f'{fmt(net-5)}%', f'{fmt(net+10)}%']
        on = [f'{dev_num(net)}%', f'{dev_num(net+5)}%', f'{dev_num(net-5)}%', f'{dev_num(net+10)}%']
        E('Percentage', 'hard', f'A number is increased by {p}% and then decreased by {q}%. What is the net percentage change?',
          f'एउटा सङ्ख्या {dev(p)}% ले बढाइन्छ र त्यसपछि {dev(q)}% ले घटाइन्छ। खुद प्रतिशत परिवर्तन कति हुन्छ?',
          o, on, f'Net change = {p} - {q} - {p}x{q}/100 = {ans}%.', f'खुद परिवर्तन = {dev(p)} - {dev(q)} - {dev(p)}x{dev(q)}/१०० = {dev_num(net)}%।')
    else:
        dec = abs(net)
        o = [f'{fmt(dec)}%', f'{fmt(dec+5)}%', f'{fmt(dec-5)}%', f'{fmt(dec+10)}%']
        on = [f'{dev_num(dec)}%', f'{dev_num(dec+5)}%', f'{dev_num(dec-5)}%', f'{dev_num(dec+10)}%']
        E('Percentage', 'hard', f'A number is increased by {p}% and then decreased by {q}%. What is the net percentage decrease?',
          f'एउटा सङ्ख्या {dev(p)}% ले बढाइन्छ र त्यसपछि {dev(q)}% ले घटाइन्छ। खुद प्रतिशत कमी कति हुन्छ?',
          o, on, f'Net decrease = {q} + {p}x{q}/100 - {p} = {fmt(dec)}%.', f'खुद कमी = {dev(q)} + {dev(p)}x{dev(q)}/१०० - {dev(p)} = {dev_num(dec)}%।')

# ---------- SI find rate ----------
for _ in range(100):
    P = rng.choice([1000, 2000, 4000, 5000, 8000, 10000, 20000])
    T = rng.choice([2, 4, 5, 8, 10])
    R = rng.choice([5, 8, 10, 12, 15, 20])
    si = P * R * T // 100
    if P * R * T % 100: continue
    o, on, _ = num_opts(R, [R+1, R-1, R+2, R-2])
    E('Simple Interest', 'hard', f'What is the rate of interest if Rs {P} yields Rs {si} simple interest in {T} years?',
      f'रु {dev_num(P)} ले {dev(T)} वर्षमा रु {dev_num(si)} साधारण ब्याज दिन्छ भने ब्याज दर कति हो?',
      o, on, f'Rate = {si} x 100 / ({P} x {T}) = {R}%.', f'दर = {dev_num(si)} x १०० / ({dev_num(P)} x {dev(T)}) = {dev(R)}%।', exams=EXH)

# ---------- SI find time ----------
for _ in range(100):
    P = rng.choice([1000, 2000, 4000, 5000, 8000, 10000, 20000])
    R = rng.choice([5, 8, 10, 12, 15, 20])
    T = rng.choice([2, 4, 5, 8, 10])
    si = P * R * T // 100
    if P * R * T % 100: continue
    o, on, _ = num_opts(T, [T+1, T-1, T+2, T-2])
    E('Simple Interest', 'hard', f'In how many years will Rs {P} yield Rs {si} simple interest at {R}% per annum?',
      f'रु {dev_num(P)} ले {dev(R)}% वार्षिक दरमा रु {dev_num(si)} साधारण ब्याज कति वर्षमा दिन्छ?',
      o, on, f'Time = {si} x 100 / ({P} x {R}) = {T} years.', f'समय = {dev_num(si)} x १०० / ({dev_num(P)} x {dev(R)}) = {dev(T)} वर्ष।', exams=EXH)

# ---------- CI half-yearly ----------
for _ in range(60):
    P = rng.choice([4000, 8000, 16000, 20000, 40000, 80000])
    R = rng.choice([10, 20])
    # 1 year, half-yearly: 2 periods at R/2
    amt = P * (1 + R/200)**2
    if amt != int(amt): continue
    amt = int(amt)
    ci = amt - P
    o, on, _ = num_opts(ci, [ci+50, ci-50, ci+100, ci-100])
    E('Compound Interest', 'hard', f'What is the compound interest on Rs {P} at {R}% per annum for 1 year, compounded half-yearly?',
      f'रु {dev_num(P)} मा {dev(R)}% वार्षिक दरले १ वर्षको चक्रवृद्धि ब्याज कति हो, अर्धवार्षिक चक्रवृद्धि गर्दा?',
      o, on, f'Amount = {P} x (1 + {R}/200)^2 = {amt}; CI = {ci}.', f'मिश्रधन = {dev_num(P)} x (१ + {dev(R)}/२००)^२ = {dev_num(amt)}; चक्रवृद्धि ब्याज = {dev_num(ci)}।', exams=EXH)

# ---------- average speed round trip ----------
for _ in range(100):
    v1 = rng.choice([30, 40, 50, 60])
    v2 = rng.choice([30, 40, 50, 60, 80, 100])
    if v1 == v2: continue
    avg = 2*v1*v2/(v1+v2)
    if avg != int(avg): continue
    avg = int(avg)
    o, on, _ = num_opts(avg, [avg+5, avg-5, avg+10, avg-10])
    E('Speed & Distance', 'hard', f'A man goes from A to B at {v1} km/h and returns at {v2} km/h. What is his average speed for the whole journey?',
      f'एक मानिस A बाट B सम्म {dev(v1)} किमी/घण्टाको गतिमा जान्छ र {dev(v2)} किमी/घण्टाको गतिमा फर्कन्छ। पूरै यात्राको औसत गति कति हो?',
      o, on, f'Average speed = 2 x {v1} x {v2} / ({v1} + {v2}) = {avg} km/h.', f'औसत गति = २ x {dev(v1)} x {dev(v2)} / ({dev(v1)} + {dev(v2)}) = {dev(avg)} किमी/घण्टा।', exams=EXH)

# ---------- pipes & cisterns ----------
for _ in range(100):
    a, b = rng.choice([6, 8, 10, 12, 15, 20]), rng.choice([6, 8, 10, 12, 15, 20])
    if a == b: continue
    t = a*b/(a+b)
    if t != int(t): continue
    t = int(t)
    o, on, _ = num_opts(t, [t+1, t-1, t+2, t-2])
    E('Pipes & Cisterns', 'hard', f'Pipe A can fill a tank in {a} hours and pipe B in {b} hours. How long will they take together to fill the tank?',
      f'पाइप A ले ट्याङ्की {dev(a)} घण्टामा र पाइप B ले {dev(b)} घण्टामा भर्न सक्छ। सँगै ट्याङ्की भर्न कति समय लाग्छ?',
      o, on, f'Together: 1/{a} + 1/{b} = 1/{t}, so time = {t} hours.', f'सँगै: १/{dev(a)} + १/{dev(b)} = १/{dev(t)}, त्यसैले समय = {dev(t)} घण्टा।', exams=EXH)

# ---------- men-days ----------
for _ in range(100):
    m1 = rng.choice([10, 12, 15, 20, 24, 30])
    d1 = rng.choice([6, 8, 10, 12, 15, 20])
    m2 = rng.choice([8, 10, 12, 15, 20, 24, 30, 40])
    if m1*d1 % m2: continue
    d2 = m1*d1//m2
    o, on, _ = num_opts(d2, [d2+1, d2-1, d2+2, d2-2])
    E('Work & Time', 'hard', f'{m1} men can do a work in {d1} days. In how many days can {m2} men do the same work?',
      f'{dev(m1)} जनाले एउटा काम {dev(d1)} दिनमा गर्न सक्छन्। {dev(m2)} जनाले त्यही काम कति दिनमा गर्न सक्छन्?',
      o, on, f'{m1} x {d1} = {m2} x D, so D = {m1*d1}/{m2} = {d2} days.', f'{dev(m1)} x {dev(d1)} = {dev(m2)} x D, त्यसैले D = {dev_num(m1*d1)}/{dev(m2)} = {dev(d2)} दिन।', exams=EXH)

# ---------- age after N years ----------
for _ in range(120):
    age = rng.randint(8, 40)
    n = rng.choice([5, 10, 15, 20])
    ans = age + n
    o, on, _ = num_opts(ans, [ans+1, ans-1, ans+5, ans-5])
    E('Age Problems', 'easy', f'Ram is {age} years old now. How old will he be after {n} years?',
      f'राम अहिले {dev(age)} वर्षका छन्। {dev(n)} वर्षपछि उनी कति वर्षका हुनेछन्?',
      o, on, f'Age after {n} years = {age} + {n} = {ans}.', f'{dev(n)} वर्षपछिको उमेर = {dev(age)} + {dev(n)} = {dev_num(ans)}।')
for _ in range(120):
    age = rng.randint(15, 50)
    n = rng.choice([5, 10, 15, 20])
    if age - n <= 0: continue
    ans = age - n
    o, on, _ = num_opts(ans, [ans+1, ans-1, ans+5, ans-5])
    E('Age Problems', 'easy', f'Ram is {age} years old now. How old was he {n} years ago?',
      f'राम अहिले {dev(age)} वर्षका छन्। {dev(n)} वर्षअघि उनी कति वर्षका थिए?',
      o, on, f'Age {n} years ago = {age} - {n} = {ans}.', f'{dev(n)} वर्षअघिको उमेर = {dev(age)} - {dev(n)} = {dev_num(ans)}।')

# ---------- notes/coins ----------
for _ in range(100):
    n5 = rng.randint(2, 20)
    n10 = rng.randint(2, 20)
    total = 5*n5 + 10*n10
    o, on, _ = num_opts(total, [total+10, total-10, total+5, total-5])
    E('Money', 'easy', f'A boy has {n5} five-rupee notes and {n10} ten-rupee notes. How much money does he have?',
      f'एउटा केटासँग {dev(n5)} वटा पाँच रुपैयाँका नोट र {dev(n10)} वटा दस रुपैयाँका नोट छन्। उससँग कति पैसा छ?',
      o, on, f'Total = {n5} x 5 + {n10} x 10 = {total} rupees.', f'जम्मा = {dev(n5)} x ५ + {dev(n10)} x १० = {dev_num(total)} रुपैयाँ।')
for _ in range(100):
    total = rng.choice([50, 100, 150, 200, 250, 300, 500])
    n10 = rng.randint(1, total//10 - 1)
    rem = total - 10*n10
    if rem % 5: continue
    n5 = rem // 5
    o, on, _ = num_opts(n5, [n5+1, n5-1, n5+2, n5-2])
    E('Money', 'medium', f'A boy has Rs {total} in five-rupee and ten-rupee notes. If he has {n10} ten-rupee notes, how many five-rupee notes does he have?',
      f'एउटा केटासँग पाँच र दस रुपैयाँका नोट गरी रु {dev_num(total)} छ। उससँग {dev(n10)} वटा दस रुपैयाँका नोट छन् भने पाँच रुपैयाँका नोट कति छन्?',
      o, on, f'Value of ten-rupee notes = {n10} x 10 = {10*n10}. Remaining = {total} - {10*n10} = {rem}. Five-rupee notes = {rem}/5 = {n5}.',
      f'दस रुपैयाँका नोटको मूल्य = {dev(n10)} x १० = {dev_num(10*n10)}। बाँकी = {dev_num(total)} - {dev_num(10*n10)} = {dev_num(rem)}। पाँच रुपैयाँका नोट = {dev_num(rem)}/५ = {dev_num(n5)}।')

# ---------- CP from SP and profit% ----------
for _ in range(120):
    p = rng.choice([10, 20, 25, 50])
    cp = rng.choice([200, 400, 500, 800, 1000, 2000, 4000])
    sp = cp * (100+p)//100
    if cp * (100+p) % 100: continue
    o, on, _ = num_opts(cp, [cp+50, cp-50, cp+100, cp-100])
    E('Profit & Loss', 'hard', f'An article is sold for Rs {sp} at a profit of {p}%. What is its cost price?',
      f'एउटा सामान {dev(p)}% नाफामा रु {dev_num(sp)} मा बेचियो। त्यसको क्रय मूल्य कति हो?',
      o, on, f'CP = {sp} x 100 / (100 + {p}) = {cp}.', f'क्रय मूल्य = {dev_num(sp)} x १०० / (१०० + {dev(p)}) = {dev_num(cp)}।', exams=EXH)

# ---------- MP from SP and discount% ----------
for _ in range(120):
    d = rng.choice([10, 20, 25, 50])
    mp = rng.choice([400, 500, 800, 1000, 2000, 4000, 5000])
    sp = mp * (100-d)//100
    if mp * (100-d) % 100: continue
    o, on, _ = num_opts(mp, [mp+50, mp-50, mp+100, mp-100])
    E('Discount', 'hard', f'An article is sold for Rs {sp} after a discount of {d}%. What is its marked price?',
      f'एउटा सामान {dev(d)}% छुटपछि रु {dev_num(sp)} मा बेचियो। त्यसको अङ्कित मूल्य कति हो?',
      o, on, f'MP = {sp} x 100 / (100 - {d}) = {mp}.', f'अङ्कित मूल्य = {dev_num(sp)} x १०० / (१०० - {dev(d)}) = {dev_num(mp)}।', exams=EXH)

# ---------- alligation ----------
for _ in range(100):
    c1 = rng.choice([20, 30, 40, 50, 60])
    c2 = rng.choice([80, 90, 100, 120])
    m = rng.choice([40, 50, 60, 70])
    if not (c1 < m < c2): continue
    # ratio = (c2-m):(m-c1)
    r1, r2 = c2 - m, m - c1
    g = math.gcd(r1, r2)
    r1, r2 = r1//g, r2//g
    o = [f'{r1}:{r2}', f'{r2}:{r1}', f'{r1+1}:{r2}', f'{r1}:{r2+1}']
    on = [dev(r1)+':'+dev(r2), dev(r2)+':'+dev(r1), dev(r1+1)+':'+dev(r2), dev(r1)+':'+dev(r2+1)]
    E('Mixtures', 'hard', f'In what ratio should two solutions of strength {c1}% and {c2}% be mixed to get a {m}% solution?',
      f'{dev(c1)}% र {dev(c2)}% शक्तिका दुई घोललाई {dev(m)}% घोल बनाउन कुन अनुपातमा मिसाउनुपर्छ?',
      o, on, f'Ratio = ({c2} - {m}) : ({m} - {c1}) = {r1}:{r2}.', f'अनुपात = ({dev(c2)} - {dev(m)}) : ({dev(m)} - {dev(c1)}) = {dev(r1)}:{dev(r2)}।', exams=EXH)

# ---------- train crossing platform ----------
for _ in range(100):
    tl = rng.choice([120, 150, 180, 200, 240, 300])
    pl = rng.choice([120, 180, 240, 300, 360])
    speed = rng.choice([36, 54, 72, 90])
    ms = speed * 5 // 18
    t = (tl + pl) / ms
    if t != int(t): continue
    t = int(t)
    o, on, _ = num_opts(t, [t+2, t-2, t+5, t-5])
    E('Trains', 'hard', f'A train {tl} m long crosses a platform {pl} m long at {speed} km/h. How long does it take?',
      f'{dev(tl)} मिटर लामो रेलले {dev(pl)} मिटर लामो प्लेटफर्म {dev(speed)} किमी/घण्टाको गतिमा पार गर्न कति समय लाग्छ?',
      o, on, f'Time = ({tl} + {pl}) / {ms} = {t} seconds.', f'समय = ({dev(tl)} + {dev(pl)}) / {dev(ms)} = {dev(t)} सेकेन्ड।', exams=EXH)

# ---------- boat downstream ----------
for _ in range(100):
    v = rng.choice([8, 10, 12, 15, 20])
    u = rng.choice([2, 3, 4, 5])
    d = rng.choice([24, 30, 36, 40, 48, 60, 72, 90, 120])
    t = d / (v + u)
    if t != int(t): continue
    t = int(t)
    o, on, _ = num_opts(t, [t+1, t-1, t+2, t-2])
    E('Boats & Streams', 'hard', f'A boat goes {d} km downstream. If the speed of the boat in still water is {v} km/h and the speed of the stream is {u} km/h, how long does it take?',
      f'एउटा डुङ्गा {dev(d)} किमी धारसँगै जान्छ। स्थिर पानीमा डुङ्गाको गति {dev(v)} किमी/घण्टा र धारको गति {dev(u)} किमी/घण्टा भए कति समय लाग्छ?',
      o, on, f'Downstream speed = {v} + {u} = {v+u} km/h. Time = {d}/{v+u} = {t} hours.', f'धारसँगैको गति = {dev(v)} + {dev(u)} = {dev(v+u)} किमी/घण्टा। समय = {dev(d)}/{dev(v+u)} = {dev(t)} घण्टा।', exams=EXH)

# ---------- ratio simplification ----------
for _ in range(120):
    a = rng.randint(2, 30)
    b = rng.randint(2, 30)
    if a == b: continue
    g = math.gcd(a, b)
    if g == 1: continue
    ra, rb = a//g, b//g
    o = [f'{ra}:{rb}', f'{rb}:{ra}', f'{ra+1}:{rb}', f'{ra}:{rb+1}']
    on = [dev(ra)+':'+dev(rb), dev(rb)+':'+dev(ra), dev(ra+1)+':'+dev(rb), dev(ra)+':'+dev(rb+1)]
    E('Ratio & Proportion', 'medium', f'Simplify the ratio {a}:{b}.', f'{dev(a)}:{dev(b)} अनुपातलाई सरल बनाउनुहोस्।',
      o, on, f'{a}:{b} = {ra}:{rb}.', f'{dev(a)}:{dev(b)} = {dev(ra)}:{dev(rb)}।')

# ---------- proportion find x ----------
for _ in range(120):
    a, b = rng.randint(2, 12), rng.randint(2, 12)
    k = rng.randint(2, 9)
    c = a * k
    x = b * k
    o, on, _ = num_opts(x, [x+1, x-1, x+2, x-2])
    E('Ratio & Proportion', 'medium', f'If {a}:{b} = {c}:x, what is the value of x?', f'यदि {dev(a)}:{dev(b)} = {dev(c)}:x हो भने x को मान कति हो?',
      o, on, f'x = {b} x {c} / {a} = {x}.', f'x = {dev(b)} x {dev(c)} / {dev(a)} = {dev_num(x)}।')

# ---------- direct proportion ----------
for _ in range(100):
    price = rng.choice([10, 15, 20, 25, 30, 40, 50])
    n1 = rng.randint(2, 10)
    n2 = rng.randint(2, 10)
    if n1 == n2: continue
    cost1 = price * n1
    cost2 = price * n2
    o, on, _ = num_opts(cost2, [cost2+10, cost2-10, cost2+20, cost2-20])
    E('Ratio & Proportion', 'medium', f'If {n1} kg of rice costs Rs {cost1}, how much does {n2} kg cost?',
      f'यदि {dev(n1)} केजी चामलको मूल्य रु {dev_num(cost1)} हो भने {dev(n2)} केजीको मूल्य कति हो?',
      o, on, f'Cost of {n2} kg = {cost1} x {n2}/{n1} = {cost2}.', f'{dev(n2)} केजीको मूल्य = {dev_num(cost1)} x {dev(n2)}/{dev(n1)} = {dev_num(cost2)}।')

# ---------- inverse proportion ----------
for _ in range(100):
    speed = rng.choice([40, 50, 60, 80])
    time = rng.choice([2, 3, 4, 5])
    dist = speed * time
    s2 = rng.choice([40, 50, 60, 80, 100])
    if dist % s2: continue
    t2 = dist // s2
    o, on, _ = num_opts(t2, [t2+1, t2-1, t2+2, t2-2])
    E('Ratio & Proportion', 'hard', f'A car travels at {speed} km/h and reaches its destination in {time} hours. How long will it take at {s2} km/h?',
      f'एउटा कार {dev(speed)} किमी/घण्टाको गतिमा {dev(time)} घण्टामा गन्तव्यमा पुग्छ। {dev(s2)} किमी/घण्टाको गतिमा कति समय लाग्छ?',
      o, on, f'Distance = {speed} x {time} = {dist} km. Time = {dist}/{s2} = {t2} hours.', f'दूरी = {dev(speed)} x {dev(time)} = {dev_num(dist)} किमी। समय = {dev_num(dist)}/{dev(s2)} = {dev(t2)} घण्टा।', exams=EXH)

# ---------- calendar 2020-2023 ----------
start = datetime.date(2020, 1, 1)
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days_ne = ['सोमबार', 'मङ्गलबार', 'बुधबार', 'बिहीबार', 'शुक्रबार', 'शनिबार', 'आइतबार']
for _ in range(200):
    d = start + datetime.timedelta(days=rng.randint(0, 1450))
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

# ---------- days between dates ----------
for _ in range(100):
    d1 = datetime.date(rng.randint(2024, 2026), rng.randint(1, 12), rng.randint(1, 28))
    d2 = d1 + datetime.timedelta(days=rng.randint(5, 60))
    n = (d2 - d1).days
    o, on, _ = num_opts(n, [n+1, n-1, n+5, n-5])
    E('Calendar', 'medium', f'How many days are there between {d1.day} {d1.strftime("%B")} {d1.year} and {d2.day} {d2.strftime("%B")} {d2.year}?',
      f'{dev(d1.year)} {d1.strftime("%B")} {dev(d1.day)} र {dev(d2.year)} {d2.strftime("%B")} {dev(d2.day)} बीच कति दिन छन्?',
      o, on, f'The difference is {n} days.', f'अन्तर {dev_num(n)} दिन हो।')

# ---------- leap years ----------
for y in range(2000, 2101, 4):
    is_leap = (y % 4 == 0 and y % 100 != 0) or y % 400 == 0
    if not is_leap: continue
    o = [str(y)] + [str(y+1), str(y+2), str(y+3)]
    on = [dev_num(y), dev_num(y+1), dev_num(y+2), dev_num(y+3)]
    em.emit(EX, 'Maths & Numerical', 'Calendar', 'easy', 2,
            'Which of the following is a leap year?', 'निम्नमध्ये कुन अधिवर्ष (लीप वर्ष) हो?',
            o, on, 0, f'{y} is a leap year.', f'{dev_num(y)} अधिवर्ष हो।')
for y in [1900, 2100, 2200, 2300]:
    o = [str(y)] + [str(y+4), str(y+8), str(y+12)]
    on = [dev_num(y), dev_num(y+4), dev_num(y+8), dev_num(y+12)]
    # y is NOT a leap year (divisible by 100 but not by 400); the others are
    em.emit(EX, 'Maths & Numerical', 'Calendar', 'hard', 2,
            'Which of the following is NOT a leap year?', 'निम्नमध्ये कुन अधिवर्ष (लीप वर्ष) होइन?',
            o, on, 0, f'{y} is not a leap year because it is divisible by 100 but not by 400.',
            f'{dev_num(y)} अधिवर्ष होइन किनकि यो १०० ले भाग जान्छ तर ४०० ले जाँदैन।')

# ---------- clock coincidence / opposite ----------
for h in range(1, 12):
    # hands coincide at h: 60h/11 minutes
    m = 60*h/11
    mm = int(round(m))
    o, on, _ = num_opts(mm, [mm+1, mm-1, mm+5, mm-5])
    E('Clock', 'hard', f'At what time (approximately) do the hands of a clock coincide between {h} and {h+1} o\'clock?',
      f'घडीका सुईहरू {dev(h)} र {dev(h+1)} बजेको बीचमा लगभग कति बजे एकै ठाउँमा आउँछन्?',
      o, on, f'The hands coincide at about {h}:{mm:02d}.', f'सुईहरू लगभग {dev(h)}:{dev(f"{mm:02d}")} बजे एकै ठाउँमा आउँछन्।', exams=EXH)
    # hands opposite at h: (30h+180)*2/11 minutes
    m2 = (30*h + 180)*2/11
    mm2 = int(round(m2))
    if mm2 >= 60: continue
    o2, on2, _ = num_opts(mm2, [mm2+1, mm2-1, mm2+5, mm2-5])
    E('Clock', 'hard', f'At what time (approximately) are the hands of a clock opposite each other between {h} and {h+1} o\'clock?',
      f'घडीका सुईहरू {dev(h)} र {dev(h+1)} बजेको बीचमा लगभग कति बजे एकअर्काको विपरीत हुन्छन्?',
      o2, on2, f'The hands are opposite at about {h}:{mm2:02d}.', f'सुईहरू लगभग {dev(h)}:{dev(f"{mm2:02d}")} बजे एकअर्काको विपरीत हुन्छन्।', exams=EXH)

# ---------- clock angles at arbitrary minutes ----------
for _ in range(150):
    h = rng.randint(1, 12)
    m = rng.choice([1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 26, 27, 28, 29, 31, 32, 33, 34, 36, 37, 38, 39, 41, 42, 43, 44, 46, 47, 48, 49, 51, 52, 53, 54, 56, 57, 58, 59])
    ang = abs(30*h - 5.5*m)
    if ang > 180: ang = 360 - ang
    ang = round(ang, 1)
    o = [fmt(ang), fmt(ang+10), fmt(ang-10), fmt(ang+20)]
    on = [dev_num(ang), dev_num(ang+10), dev_num(ang-10), dev_num(ang+20)]
    E('Clock', 'hard', f'What is the angle between the hands of a clock at {h}:{m:02d}?', f'घडीमा {dev(h)}:{dev(f"{m:02d}")} बजे सुईहरूबीचको कोण कति हुन्छ?',
      o, on, f'Angle = |30 x {h} - 5.5 x {m}| = {fmt(ang)} degrees.', f'कोण = |३० x {dev(h)} - ५.५ x {dev(m)}| = {dev_num(ang)} डिग्री।', exams=EXH)

# ---------- squares/cubes of decimals ----------
for a in [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 0.5, 1.2, 1.4, 1.6, 1.8, 2.2, 2.4, 0.2, 0.4, 0.6, 0.8]:
    ans = round(a*a, 2)
    o = [fmt(ans), fmt(ans+1), fmt(ans-1), fmt(ans+0.5)]
    on = [dev_num(ans), dev_num(ans+1), dev_num(ans-1), dev_num(ans+0.5)]
    E('Squares & Cubes', 'medium', f'What is the square of {a}?', f'{dev(a)} को वर्ग कति हो?',
      o, on, f'{a} x {a} = {ans}.', f'{dev(a)} x {dev(a)} = {dev_num(ans)}।')
for a in [1.5, 2.5, 3.5, 0.5, 1.2, 2.2, 0.2, 0.4]:
    ans = round(a**3, 3)
    o = [fmt(ans), fmt(ans+1), fmt(ans-1), fmt(ans+0.5)]
    on = [dev_num(ans), dev_num(ans+1), dev_num(ans-1), dev_num(ans+0.5)]
    E('Squares & Cubes', 'hard', f'What is the cube of {a}?', f'{dev(a)} को घन कति हो?',
      o, on, f'{a}^3 = {ans}.', f'{dev(a)}^३ = {dev_num(ans)}।', exams=EXH)
for a in [0.25, 0.49, 0.64, 0.81, 1.44, 2.25, 6.25, 12.25]:
    r = round(math.sqrt(a), 2)
    o = [fmt(r), fmt(r+0.1), fmt(r-0.1), fmt(r+0.2)]
    on = [dev_num(r), dev_num(r+0.1), dev_num(r-0.1), dev_num(r+0.2)]
    E('Squares & Cubes', 'hard', f'What is the square root of {a}?', f'{dev(a)} को वर्गमूल कति हो?',
      o, on, f'The square root of {a} is {r}.', f'{dev(a)} को वर्गमूल {dev_num(r)} हो।', exams=EXH)

n = em.write('expansion-r10-maths5.json')
print('MATHS5 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
