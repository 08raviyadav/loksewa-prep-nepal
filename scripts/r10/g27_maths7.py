#!/usr/bin/env python3
"""R10 generator 27: Maths 7 (~1,300). Fresh spaces: reverse % (find original),
average after add/remove, combined ratios A:B:C, two-speed time difference,
A+B+C work, SI find rate/time, CI amount, new series rules, calendar 2000-2009,
clock half-hour angles, HCF/LCM of 3, triangle/circle area, successive discounts,
father-son age, two-mixture combine, two trains crossing, upstream time,
sum of first n evens/odds, simplify fractions, decimal subtraction."""
import sys, random, math, datetime
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num

bank = Bank()
em = Emitter(bank, 'R10-M7')
rng = random.Random(777001)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'tsc-primary', 'tsc-secondary', 'health', 'police', 'army']

def q_emit(topic, diff, marks, q, qn, opts, optn, ans, exp, expn):
    em.emit(EX, 'Maths & Numerical', topic, diff, marks, q, qn, opts, optn, ans, exp, expn)

def num_opts(ans, lo, hi, step=1):
    s = {ans}
    while len(s) < 4:
        v = rng.randrange(lo, hi+1, step)
        if v != ans and v >= 0: s.add(v)
    o = list(s); rng.shuffle(o)
    return o, o.index(ans)

# ---------- reverse %: find original after increase ----------
for _ in range(100):
    orig = rng.choice([100, 200, 250, 400, 500, 800, 1000, 1200, 2000])
    pct = rng.choice([10, 20, 25, 50])
    new = orig * (100 + pct) // 100
    if orig * (100 + pct) % 100: continue
    o, ai = num_opts(orig, max(50, orig-200), orig+200, 50)
    q_emit('Percentages', 'medium', 1,
        f"After an increase of {pct}%, a number becomes {new}. What was the original number?",
        f"{pct}% ले बढेपछि एउटा सङ्ख्या {new} हुन्छ। मूल सङ्ख्या कति थियो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Original = {new} x 100 / {100+pct} = {orig}.",
        f"मूल सङ्ख्या = {new} × १०० / {100+pct} = {orig} हो।")

# ---------- reverse %: find original after decrease ----------
for _ in range(100):
    orig = rng.choice([100, 200, 250, 400, 500, 800, 1000, 1200, 2000])
    pct = rng.choice([10, 20, 25, 50])
    new = orig * (100 - pct) // 100
    if orig * (100 - pct) % 100: continue
    o, ai = num_opts(orig, max(50, orig-200), orig+200, 50)
    q_emit('Percentages', 'medium', 1,
        f"After a decrease of {pct}%, a number becomes {new}. What was the original number?",
        f"{pct}% ले घटेपछि एउटा सङ्ख्या {new} हुन्छ। मूल सङ्ख्या कति थियो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Original = {new} x 100 / {100-pct} = {orig}.",
        f"मूल सङ्ख्या = {new} × १०० / {100-pct} = {orig} हो।")

# ---------- average after adding a number ----------
for _ in range(100):
    n = rng.choice([4, 5, 6, 8, 10])
    avg = rng.randrange(20, 80, 5)
    add = rng.randrange(10, 100, 5)
    new_avg = (n * avg + add) / (n + 1)
    if new_avg != int(new_avg): continue
    ans = int(new_avg)
    o, ai = num_opts(ans, max(1, ans-15), ans+15, 5)
    q_emit('Averages', 'medium', 1,
        f"The average of {n} numbers is {avg}. If {add} is added to the list, what is the new average?",
        f"{n} वटा सङ्ख्याको औसत {avg} छ। सूचीमा {add} थप्दा नयाँ औसत कति हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Total = {n}x{avg} = {n*avg}. New total = {n*avg} + {add} = {n*avg+add}. New average = {n*avg+add}/{n+1} = {ans}.",
        f"जम्मा = {n}×{avg} = {n*avg} हो। नयाँ जम्मा = {n*avg} + {add} = {n*avg+add} हो। नयाँ औसत = {n*avg+add}/{n+1} = {ans} हो।")

# ---------- combined ratio A:B and B:C ----------
for _ in range(100):
    ab1, ab2 = rng.choice([(2, 3), (3, 4), (1, 2), (4, 5), (5, 6), (3, 5)])
    bc1, bc2 = rng.choice([(2, 3), (3, 4), (1, 2), (4, 5), (5, 6), (3, 5)])
    # A:B = ab1:ab2, B:C = bc1:bc2 -> A:B:C = ab1*bc1 : ab2*bc1 : ab2*bc2
    A = ab1 * bc1; B = ab2 * bc1; C = ab2 * bc2
    g = math.gcd(math.gcd(A, B), C)
    A, B, C = A//g, B//g, C//g
    which = rng.choice(['A', 'B', 'C'])
    val = {'A': A, 'B': B, 'C': C}[which]
    opts = [f"{A}:{B}:{C}", f"{ab1}:{ab2}:{bc2}", f"{A+1}:{B}:{C}", f"{A}:{B+1}:{C}"]
    if len(set(opts)) < 4: continue
    o = opts[:]; rng.shuffle(o)
    q_emit('Ratio & Proportion', 'medium', 1,
        f"If A:B = {ab1}:{ab2} and B:C = {bc1}:{bc2}, what is A:B:C?",
        f"यदि A:B = {ab1}:{ab2} र B:C = {bc1}:{bc2} हो भने A:B:C कति हो?",
        o, [dev(x) for x in o], o.index(f"{A}:{B}:{C}"),
        f"A:B:C = {ab1}x{bc1} : {ab2}x{bc1} : {ab2}x{bc2} = {A}:{B}:{C}.",
        f"A:B:C = {ab1}×{bc1} : {ab2}×{bc1} : {ab2}×{bc2} = {A}:{B}:{C} हो।")

# ---------- two speeds, time difference ----------
for _ in range(80):
    v1 = rng.choice([40, 50, 60, 80])
    v2 = rng.choice([50, 60, 80, 100])
    if v2 <= v1: continue
    d = rng.choice([120, 180, 240, 300, 360, 400, 480, 600])
    t1 = d / v1; t2 = d / v2
    diff = t1 - t2
    if diff != int(diff): continue
    ans = int(diff)
    o, ai = num_opts(ans, 1, ans+5, 1)
    q_emit('Speed, Distance & Time', 'hard', 2,
        f"A car travels {d} km. At {v1} km/h it takes longer than at {v2} km/h. How many hours longer does it take at the slower speed?",
        f"एउटा कार {d} किमी यात्रा गर्छ। {v1} किमी/घण्टामा {v2} किमी/घण्टा भन्दा बढी समय लाग्छ। ढिलो गतिमा कति घण्टा बढी लाग्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Time at {v1} km/h = {d}/{v1} = {t1:g} h. Time at {v2} km/h = {d}/{v2} = {t2:g} h. Difference = {ans} h.",
        f"{v1} किमी/घण्टामा समय = {d}/{v1} = {t1:g} घण्टा हो। {v2} किमी/घण्टामा समय = {d}/{v2} = {t2:g} घण्टा हो। फरक = {ans} घण्टा हो।")

# ---------- A+B+C work together ----------
for _ in range(80):
    ta = rng.choice([10, 12, 15, 20])
    tb = rng.choice([15, 20, 30])
    tc = rng.choice([20, 30, 40, 60])
    rate = 1/ta + 1/tb + 1/tc
    days = 1 / rate
    if abs(days - round(days)) > 1e-9: continue
    ans = int(round(days))
    o, ai = num_opts(ans, max(1, ans-5), ans+5, 1)
    q_emit('Work & Time', 'hard', 2,
        f"A, B and C can finish a work alone in {ta}, {tb} and {tc} days respectively. In how many days can they finish it together?",
        f"A, B र C एक्लैले काम क्रमशः {ta}, {tb} र {tc} दिनमा सक्न सक्छन्। सँगैले कति दिनमा सक्न सक्छन्?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Combined rate = 1/{ta} + 1/{tb} + 1/{tc} = {rate:.4f} per day. Days = 1/{rate:.4f} = {ans}.",
        f"संयुक्त दर = 1/{ta} + 1/{tb} + 1/{tc} = {rate:.4f} प्रतिदिन हो। दिन = १/{rate:.4f} = {ans} हो।")

# ---------- SI find rate ----------
for _ in range(80):
    p = rng.choice([1000, 2000, 4000, 5000, 8000, 10000])
    si = rng.choice([200, 400, 500, 600, 800, 1000, 1200, 1600])
    t = rng.choice([2, 4, 5, 8, 10])
    r = si * 100 / (p * t)
    if r != int(r): continue
    ans = int(r)
    o, ai = num_opts(ans, 1, ans+10, 1)
    q_emit('Interest', 'medium', 1,
        f"The simple interest on Rs {p} for {t} years is Rs {si}. What is the rate of interest per annum?",
        f"रू {p} मा {t} वर्षको साधारण ब्याज रू {si} हुन्छ। वार्षिक ब्याज दर कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"R = SI x 100 / (P x T) = {si}x100/({p}x{t}) = {ans}%.",
        f"R = SI × १०० / (P × T) = {si}×१००/({p}×{t}) = {ans}% हो।")

# ---------- SI find time ----------
for _ in range(80):
    p = rng.choice([1000, 2000, 4000, 5000, 8000, 10000])
    si = rng.choice([200, 400, 500, 600, 800, 1000, 1200, 1600])
    r = rng.choice([5, 8, 10, 12, 20])
    t = si * 100 / (p * r)
    if t != int(t): continue
    ans = int(t)
    o, ai = num_opts(ans, 1, ans+8, 1)
    q_emit('Interest', 'medium', 1,
        f"In how many years will Rs {p} earn Rs {si} as simple interest at {r}% per annum?",
        f"रू {p} ले {r}% वार्षिक दरले रू {si} साधारण ब्याज कमाउन कति वर्ष लाग्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"T = SI x 100 / (P x R) = {si}x100/({p}x{r}) = {ans} years.",
        f"T = SI × १०० / (P × R) = {si}×१००/({p}×{r}) = {ans} वर्ष हो।")

# ---------- CI amount after 2 years ----------
for _ in range(80):
    p = rng.choice([1000, 2000, 4000, 5000, 8000, 10000, 20000])
    r = rng.choice([5, 10, 20])
    amt = p * (1 + r/100) ** 2
    if amt != int(amt): continue
    ans = int(amt)
    o, ai = num_opts(ans, max(100, ans-1000), ans+1000, 100)
    q_emit('Interest', 'medium', 1,
        f"What is the amount after 2 years if Rs {p} is invested at {r}% compound interest per annum?",
        f"रू {p} लाई {r}% वार्षिक चक्रवृद्धि ब्याजमा लगानी गर्दा २ वर्षपछि रकम कति हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Amount = {p} x (1 + {r}/100)^2 = {p} x {(1+r/100)**2} = {ans}.",
        f"रकम = {p} × (१ + {r}/१००)² = {p} × {(1+r/100)**2} = {ans} हो।")

# ---------- series: n^2+2n, x4-3, +squares alternating, cubes descending ----------
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
def g_n2p2n():
    i = rng.randrange(1, 8)
    s = [k*k + 2*k for k in range(i, i+5)]
    return s, (i+5)*(i+5) + 2*(i+5)
def g_x4m3():
    a = rng.randrange(2, 10); s = [a]
    for _ in range(4): s.append(s[-1]*4 - 3)
    return s, s[-1]*4 - 3
def g_alt_sq():
    a = rng.randrange(5, 30); s = [a]
    for k in range(4):
        s.append(s[-1] + (k+1)**2 if k % 2 == 0 else s[-1] - (k+1))
    nxt = s[-1] + 25 if len(s) % 2 == 1 else s[-1] - 5
    return s, nxt
def g_cubes_desc():
    i = rng.randrange(6, 10)
    s = [k**3 for k in range(i, i-5, -1)]
    return s, (i-5)**3
series_block(g_n2p2n, 'n squared plus 2n')
series_block(g_x4m3, 'multiply by 4 and subtract 3')
series_block(g_alt_sq, 'alternately add squares and subtract')
series_block(g_cubes_desc, 'descending cubes')

# ---------- calendar 2000-2009 ----------
for _ in range(120):
    y = rng.randrange(2000, 2010)
    m = rng.randrange(1, 13)
    d = rng.randrange(1, 29)
    dt = datetime.date(y, m, d)
    wd = dt.strftime('%A')
    ne_map = {'Monday': 'सोमबार', 'Tuesday': 'मङ्गलबार', 'Wednesday': 'बुधबार', 'Thursday': 'बिहीबार', 'Friday': 'शुक्रबार', 'Saturday': 'शनिबार', 'Sunday': 'आइतबार'}
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    ne_m = ['जनवरी', 'फेब्रुअरी', 'मार्च', 'अप्रिल', 'मे', 'जुन', 'जुलाई', 'अगस्ट', 'सेप्टेम्बर', 'अक्टोबर', 'नोभेम्बर', 'डिसेम्बर'][m-1]
    others = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    others.remove(wd)
    rng.shuffle(others)
    opts = [wd] + others[:3]
    o = opts[:]; rng.shuffle(o)
    q_emit('Calendar & Clock', 'medium', 1,
        f"What day of the week was {d} {months[m-1]} {y}?", f"{y} को {ne_m} {d} गते कुन बार थियो?",
        o, [ne_map[x] for x in o], o.index(wd),
        f"{d} {months[m-1]} {y} was a {wd}.", f"{y} को {ne_m} {d} गते {ne_map[wd]} थियो।")

# ---------- clock angle at half hours ----------
for _ in range(60):
    h = rng.randrange(1, 12)
    # at h:30, minute hand at 6 (180 deg), hour hand at 30h + 15
    ang = abs(180 - (30*h + 15))
    if ang > 180: ang = 360 - ang
    o, ai = num_opts(ang, 0, 180, 15)
    q_emit('Calendar & Clock', 'hard', 2,
        f"What is the angle between the hands of a clock at {h}:30?",
        f"घडीमा {h}:३० बज्दा सुईहरूबीचको कोण कति हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Minute hand at 180 deg. Hour hand at {30*h+15} deg. Angle = |180 - {30*h+15}| = {ang} degrees (smaller angle).",
        f"मिनेटको सुई १८० डिग्रीमा छ। घण्टाको सुई {30*h+15} डिग्रीमा छ। कोण = |१८० - {30*h+15}| = {ang} डिग्री (सानो कोण) हो।")

# ---------- HCF/LCM of 3 numbers ----------
for _ in range(80):
    a = rng.randrange(4, 30); b = rng.randrange(4, 30); c = rng.randrange(4, 30)
    if len({a, b, c}) < 3: continue
    ans = math.lcm(math.lcm(a, b), c)
    if ans > 600: continue
    o, ai = num_opts(ans, max(1, ans-60), ans+60, 6)
    q_emit('HCF & LCM', 'hard', 2,
        f"What is the LCM of {a}, {b} and {c}?", f"{a}, {b} र {c} को लस कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"LCM of {a}, {b} and {c} = {ans}.", f"{a}, {b} र {c} को लस {ans} हो।")

# ---------- triangle area ----------
for _ in range(80):
    b = rng.choice([4, 6, 8, 10, 12, 14, 16, 20])
    h = rng.choice([3, 4, 5, 6, 8, 10, 12, 15])
    ans = b * h // 2
    if b * h % 2: continue
    o, ai = num_opts(ans, max(1, ans-20), ans+20, 5)
    q_emit('Geometry', 'easy', 1,
        f"What is the area of a triangle with base {b} cm and height {h} cm?",
        f"आधार {b} सेमी र उचाइ {h} सेमी भएको त्रिभुजको क्षेत्रफल कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Area = 1/2 x base x height = 1/2 x {b} x {h} = {ans} sq cm.",
        f"क्षेत्रफल = १/२ × आधार × उचाइ = १/२ × {b} × {h} = {ans} वर्ग सेमी हो।")

# ---------- circle circumference ----------
for _ in range(80):
    r = rng.choice([7, 14, 21, 28, 35])
    ans = 2 * 22 // 7 * r
    o, ai = num_opts(ans, max(1, ans-40), ans+40, 11)
    q_emit('Geometry', 'medium', 1,
        f"What is the circumference of a circle with radius {r} cm? (Use pi = 22/7)",
        f"त्रिज्या {r} सेमी भएको वृत्तको परिधि कति हो? (pi = २२/७ प्रयोग गर्नुहोस्)",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Circumference = 2 x pi x r = 2 x 22/7 x {r} = {ans} cm.",
        f"परिधि = २ × pi × r = २ × २२/७ × {r} = {ans} सेमी हो।")

# ---------- successive discounts: find SP ----------
for _ in range(80):
    mp = rng.choice([500, 800, 1000, 1200, 1500, 2000, 2500])
    d1 = rng.choice([10, 20])
    d2 = rng.choice([10, 20, 25])
    sp = mp * (100-d1)/100 * (100-d2)/100
    if sp != int(sp): continue
    ans = int(sp)
    o, ai = num_opts(ans, max(50, ans-200), ans+200, 50)
    q_emit('Profit & Loss', 'medium', 1,
        f"An article marked at Rs {mp} is sold after two successive discounts of {d1}% and {d2}%. What is the selling price?",
        f"रू {mp} अङ्कित मूल्य भएको सामान {d1}% र {d2}% को दुई क्रमिक छुटपछि बेचियो। बिक्री मूल्य कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"SP = {mp} x {100-d1}/100 x {100-d2}/100 = {ans}.",
        f"SP = {mp} × {100-d1}/१०० × {100-d2}/१०० = {ans} हो।")

# ---------- father-son age ----------
for _ in range(80):
    son = rng.randrange(5, 20)
    k = rng.choice([3, 4, 5])
    father = k * son
    n = rng.choice([5, 10])
    # after n years father is k2 times son? ask father's age after n years
    ans = father + n
    o, ai = num_opts(ans, max(1, ans-15), ans+15, 5)
    q_emit('Age Problems', 'medium', 1,
        f"A father is {k} times as old as his son. If the son is {son} years old now, how old will the father be after {n} years?",
        f"बुबा आफ्नो छोराभन्दा {k} गुणा जेठो छ। छोरा अहिले {son} वर्षको छ भने {n} वर्षपछि बुबा कति वर्षको हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Father's age now = {k}x{son} = {father}. After {n} years: {father} + {n} = {ans}.",
        f"बुबाको अहिलेको उमेर = {k}×{son} = {father} हो। {n} वर्षपछि: {father} + {n} = {ans} हो।")

# ---------- two mixtures combined ----------
for _ in range(80):
    m1 = rng.choice([20, 30, 40, 50])
    r1a, r1b = rng.choice([(1, 2), (2, 3), (3, 2), (1, 1)])
    m2 = rng.choice([20, 30, 40, 50])
    r2a, r2b = rng.choice([(1, 2), (2, 3), (3, 2), (1, 1)])
    a1 = m1 * r1a / (r1a + r1b); b1 = m1 - a1
    a2 = m2 * r2a / (r2a + r2b); b2 = m2 - a2
    if a1 != int(a1) or a2 != int(a2): continue
    A = int(a1 + a2); B = int(b1 + b2)
    g = math.gcd(A, B)
    ans_str = f"{A//g}:{B//g}"
    opts = [ans_str, f"{r1a}:{r1b}", f"{r2a}:{r2b}", f"{A}:{B+5}"]
    if len(set(opts)) < 4: continue
    o = opts[:]; rng.shuffle(o)
    q_emit('Mixtures & Alligation', 'hard', 2,
        f"Two mixtures of milk and water of {m1} litres (ratio {r1a}:{r1b}) and {m2} litres (ratio {r2a}:{r2b}) are mixed together. What is the ratio of milk to water in the new mixture?",
        f"दूध र पानीका दुई मिश्रणहरू {m1} लिटर (अनुपात {r1a}:{r1b}) र {m2} लिटर (अनुपात {r2a}:{r2b}) मिसाइयो। नयाँ मिश्रणमा दूध र पानीको अनुपात कति हो?",
        o, [dev(x) for x in o], o.index(ans_str),
        f"Milk = {int(a1)} + {int(a2)} = {A} L. Water = {int(b1)} + {int(b2)} = {B} L. Ratio = {ans_str}.",
        f"दूध = {int(a1)} + {int(a2)} = {A} लिटर हो। पानी = {int(b1)} + {int(b2)} = {B} लिटर हो। अनुपात = {ans_str} हो।")

# ---------- two trains crossing each other ----------
for _ in range(80):
    l1 = rng.choice([120, 150, 180, 200, 240])
    l2 = rng.choice([120, 150, 180, 200, 240])
    v1 = rng.choice([36, 45, 54])
    v2 = rng.choice([36, 45, 54, 72])
    rel = (v1 + v2) * 5/18
    t = (l1 + l2) / rel
    if t != int(t): continue
    ans = int(t)
    o, ai = num_opts(ans, max(1, ans-10), ans+10, 1)
    q_emit('Trains', 'hard', 2,
        f"Two trains of lengths {l1} m and {l2} m run towards each other at {v1} km/h and {v2} km/h. In how many seconds will they cross each other completely?",
        f"{l1} मिटर र {l2} मिटर लामा दुई रेलहरू {v1} किमी/घण्टा र {v2} किमी/घण्टाको गतिमा एकअर्कातर्फ चल्छन्। उनीहरूले एकअर्कालाई पूर्ण रूपमा पार गर्न कति सेकेन्ड लाग्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Relative speed = ({v1} + {v2}) x 5/18 = {rel:g} m/s. Total length = {l1+l2} m. Time = {l1+l2}/{rel:g} = {ans} s.",
        f"सापेक्ष गति = ({v1} + {v2}) × ५/१८ = {rel:g} मि/से हो। कुल लम्बाइ = {l1+l2} मिटर हो। समय = {l1+l2}/{rel:g} = {ans} सेकेन्ड हो।")

# ---------- boats upstream time ----------
for _ in range(80):
    vb = rng.choice([8, 10, 12, 15, 20])
    vc = rng.choice([2, 3, 4, 5])
    if vb <= vc: continue
    d = rng.choice([24, 30, 36, 40, 48, 60, 72, 90])
    if d % (vb - vc): continue
    ans = d // (vb - vc)
    o, ai = num_opts(ans, max(1, ans-5), ans+5, 1)
    q_emit('Boats & Streams', 'medium', 1,
        f"A boat's speed in still water is {vb} km/h and the stream's speed is {vc} km/h. How many hours will it take to travel {d} km upstream?",
        f"स्थिर पानीमा डुङ्गाको गति {vb} किमी/घण्टा र खोलाको गति {vc} किमी/घण्टा छ। {d} किमी माथितिर जान कति घण्टा लाग्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Upstream speed = {vb} - {vc} = {vb-vc} km/h. Time = {d}/{vb-vc} = {ans} hours.",
        f"माथितिरको गति = {vb} - {vc} = {vb-vc} किमी/घण्टा हो। समय = {d}/{vb-vc} = {ans} घण्टा हो।")

# ---------- sum of first n even numbers ----------
for _ in range(80):
    n = rng.randrange(5, 51)
    ans = n * (n + 1)
    o, ai = num_opts(ans, max(1, ans-100), ans+100, 10)
    q_emit('Number System', 'medium', 1,
        f"What is the sum of the first {n} even numbers?", f"पहिलो {n} वटा जोर सङ्ख्याहरूको योग कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Sum of first {n} even numbers = {n}x({n}+1) = {ans}.",
        f"पहिलो {n} वटा जोर सङ्ख्याको योग = {n}×({n}+१) = {ans} हो।")

# ---------- sum of first n odd numbers ----------
for _ in range(80):
    n = rng.randrange(5, 51)
    ans = n * n
    o, ai = num_opts(ans, max(1, ans-100), ans+100, 10)
    q_emit('Number System', 'medium', 1,
        f"What is the sum of the first {n} odd numbers?", f"पहिलो {n} वटा विजोर सङ्ख्याहरूको योग कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Sum of first {n} odd numbers = {n}^2 = {ans}.",
        f"पहिलो {n} वटा विजोर सङ्ख्याको योग = {n}² = {ans} हो।")

# ---------- simplify fractions ----------
for _ in range(100):
    a = rng.randrange(2, 13); b = rng.randrange(2, 13)
    n = rng.choice([2, 3, 4, 5, 6])
    num, den = a*n, b*n
    g = math.gcd(a, b)
    sa, sb = a//g, b//g
    ans_str = f"{sa}/{sb}"
    opts = [ans_str, f"{a}/{b}", f"{sa+1}/{sb}", f"{sa}/{sb+1}"]
    if len(set(opts)) < 4: continue
    o = opts[:]; rng.shuffle(o)
    q_emit('Fractions', 'easy', 1,
        f"What is {num}/{den} in its simplest form?", f"{num}/{den} को सरलतम रूप कति हो?",
        o, [dev(x) for x in o], o.index(ans_str),
        f"Divide numerator and denominator by their HCF {n*g}: {num}/{den} = {ans_str}.",
        f"अंश र हरलाई तिनीहरूको मस {n*g} ले भाग गर्दा: {num}/{den} = {ans_str} हो।")

# ---------- decimal subtraction ----------
for _ in range(80):
    a = rng.choice([5.5, 7.25, 8.4, 9.6, 10.75, 12.5, 15.25, 20.4])
    b = rng.choice([1.25, 2.5, 3.4, 4.6, 5.75, 6.2, 7.5])
    if a <= b: continue
    ans = round(a - b, 2)
    o = [ans, round(ans+1, 2), round(ans-1, 2), round(ans+2, 2)]
    o = [x for x in o if x > 0]
    if len(set(o)) < 4: continue
    rng.shuffle(o)
    q_emit('Decimals', 'easy', 1,
        f"What is {a} - {b}?", f"{a} - {b} कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], o.index(ans),
        f"{a} - {b} = {ans}.", f"{a} - {b} = {ans} हो।")

n = em.write('expansion-r10-maths7.json')
print('MATHS7 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
