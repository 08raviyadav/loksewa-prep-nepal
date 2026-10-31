#!/usr/bin/env python3
"""R10 generator 29: Maths 8 top-up (~350). Fresh spaces: average of first n
multiples of 12/15/18/20, A+B/B+C/A+C combined work, trains crossing platform,
calendar 1990-1999, clock quarter-hour angles, series x5-4 / +prime squares,
HCF of 3, CP from SP+loss%, SI amount, 3-person age ratio, mixture add water."""
import sys, random, math, datetime
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num

bank = Bank()
em = Emitter(bank, 'R10-M8')
rng = random.Random(20261026)
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

# ---------- average of first n multiples of k (k=12,15,18,20) ----------
for _ in range(80):
    k = rng.choice([12, 15, 18, 20, 25, 30])
    n = rng.choice([4, 5, 6, 8, 10, 12, 15, 20])
    ans = k * (n + 1) // 2
    if k * (n + 1) % 2: continue
    o, ai = num_opts(ans, max(1, ans-30), ans+30, 5)
    q_emit('Averages', 'medium', 1,
        f"What is the average of the first {n} multiples of {k}?",
        f"{k} का पहिलो {n} वटा गुणनहरूको औसत कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Sum = {k}x{n}x{n+1}/2 = {k*n*(n+1)//2}. Average = {k*n*(n+1)//2}/{n} = {ans}.",
        f"योग = {k}×{n}×{n+1}/२ = {k*n*(n+1)//2} हो। औसत = {k*n*(n+1)//2}/{n} = {ans} हो।")

# ---------- A+B / B+C / A+C combined work ----------
SETS = [(12, 15, 20), (10, 15, 30), (8, 12, 24), (6, 10, 15), (20, 30, 60), (15, 20, 60), (12, 20, 30), (10, 20, 40), (9, 12, 36), (18, 24, 72)]
for _ in range(60):
    x, y, z = rng.choice(SETS)
    S = 1/x + 1/y + 1/z
    combined = S / 2
    # A alone: combined - 1/y ; B alone: combined - 1/z ; C alone: combined - 1/x
    rates = {'A': combined - 1/y, 'B': combined - 1/z, 'C': combined - 1/x}
    person = rng.choice(['A', 'B', 'C'])
    rate = rates[person]
    if rate <= 0: continue
    days = 1 / rate
    if abs(days - round(days)) > 1e-9: continue
    ans = int(round(days))
    o, ai = num_opts(ans, max(1, ans-15), ans+15, 5)
    q_emit('Work & Time', 'hard', 2,
        f"A and B together can finish a work in {x} days, B and C in {y} days, and A and C in {z} days. In how many days can {person} alone finish the work?",
        f"A र B सँगैले काम {x} दिनमा, B र C ले {y} दिनमा, र A र C ले {z} दिनमा सक्न सक्छन्। {person} एक्लैले काम कति दिनमा सक्न सक्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Combined rate of all three = (1/{x} + 1/{y} + 1/{z})/2 = {combined:.4f} per day. {person}'s rate = {combined:.4f} - {1/y if person=='A' else (1/z if person=='B' else 1/x):.4f} = {rate:.4f}. Days = 1/{rate:.4f} = {ans}.",
        f"तीनै जनाको संयुक्त दर = (1/{x} + 1/{y} + 1/{z})/२ = {combined:.4f} प्रतिदिन हो। {person} को दर = {combined:.4f} - {1/y if person=='A' else (1/z if person=='B' else 1/x):.4f} = {rate:.4f} हो। दिन = १/{rate:.4f} = {ans} हो।")

# ---------- trains crossing a platform ----------
for _ in range(80):
    L = rng.choice([120, 150, 180, 200, 240, 270, 300])
    P = rng.choice([180, 240, 300, 360, 420, 480])
    v = rng.choice([36, 45, 54, 60, 72, 90])
    t = (L + P) / (v * 5/18)
    if t != int(t): continue
    ans = int(t)
    o, ai = num_opts(ans, max(1, ans-10), ans+10, 1)
    q_emit('Trains', 'medium', 1,
        f"A train {L} m long running at {v} km/h crosses a platform {P} m long. How many seconds does it take?",
        f"{L} मिटर लामो रेल {v} किमी/घण्टाको गतिमा {P} मिटर लामो प्लेटफर्म पार गर्छ। कति सेकेन्ड लाग्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Speed = {v}x5/18 = {v*5/18:g} m/s. Distance = {L} + {P} = {L+P} m. Time = {L+P}/{v*5/18:g} = {ans} s.",
        f"गति = {v}×५/१८ = {v*5/18:g} मि/से हो। दूरी = {L} + {P} = {L+P} मिटर हो। समय = {L+P}/{v*5/18:g} = {ans} सेकेन्ड हो।")

# ---------- calendar 1990-1999 ----------
for _ in range(100):
    y = rng.randrange(1990, 2000)
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

# ---------- clock angles at quarter hours ----------
for _ in range(60):
    h = rng.randrange(1, 12)
    mm = rng.choice([15, 45])
    ang = abs(30*h + 0.5*mm - 6*mm)
    if ang > 180: ang = 360 - ang
    ang = int(ang)
    o, ai = num_opts(ang, 0, 180, 15)
    q_emit('Calendar & Clock', 'hard', 2,
        f"What is the angle between the hands of a clock at {h}:{mm}?",
        f"घडीमा {h}:{mm} बज्दा सुईहरूबीचको कोण कति हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Minute hand at {6*mm} deg. Hour hand at {30*h + 0.5*mm:g} deg. Smaller angle = {ang} degrees.",
        f"मिनेटको सुई {6*mm} डिग्रीमा छ। घण्टाको सुई {30*h + 0.5*mm:g} डिग्रीमा छ। सानो कोण = {ang} डिग्री हो।")

# ---------- series: x5-4, +prime squares ----------
def series_block(gen, name, n=70):
    for _ in range(n):
        seq, ans = gen()
        if seq is None: continue
        disp = ', '.join(str(x) for x in seq)
        o, ai = num_opts(ans, max(0, ans-40), ans+40, 1)
        q_emit('Number Series', 'medium', 1,
            f"What is the next number in the series: {disp}, ...?", f"श्रेणीको अर्को सङ्ख्या कति हो: {disp}, ...?",
            [str(x) for x in o], [dev_num(x) for x in o], ai,
            f"The series follows the {name} pattern. The next term is {ans}.",
            f"श्रेणीले {name} ढाँचा पछ्याउँछ। अर्को पद {ans} हो।")
def g_x5m4():
    a = rng.randrange(2, 8); s = [a]
    for _ in range(4): s.append(s[-1]*5 - 4)
    return s, s[-1]*5 - 4
def g_prime_sq():
    ps = [2, 3, 5, 7, 11, 13]
    a = rng.randrange(5, 30); s = [a]; i = rng.randrange(0, 2)
    for k in range(4): s.append(s[-1] + ps[i+k]**2)
    return s, s[-1] + ps[i+4]**2
series_block(g_x5m4, 'multiply by 5 and subtract 4')
series_block(g_prime_sq, 'add squares of consecutive primes')

# ---------- HCF of 3 numbers ----------
for _ in range(60):
    a = rng.randrange(12, 120); b = rng.randrange(12, 120); c = rng.randrange(12, 120)
    if len({a, b, c}) < 3: continue
    ans = math.gcd(math.gcd(a, b), c)
    if ans < 2: continue
    o, ai = num_opts(ans, 1, ans+12, 1)
    q_emit('HCF & LCM', 'medium', 1,
        f"What is the HCF of {a}, {b} and {c}?", f"{a}, {b} र {c} को मस कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"HCF of {a}, {b} and {c} = {ans}.", f"{a}, {b} र {c} को मस {ans} हो।")

# ---------- CP from SP and loss% ----------
for _ in range(80):
    cp = rng.choice([500, 800, 1000, 1200, 1500, 2000, 2500])
    loss = rng.choice([10, 20, 25])
    sp = cp * (100 - loss) // 100
    if cp * (100 - loss) % 100: continue
    o, ai = num_opts(cp, max(100, cp-400), cp+400, 100)
    q_emit('Profit & Loss', 'medium', 1,
        f"An article is sold for Rs {sp} at a loss of {loss}%. What was its cost price?",
        f"एउटा सामान {loss}% नोक्सानमा रू {sp} मा बेचियो। यसको लागत मूल्य कति थियो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"SP = CP x (100 - {loss})/100. So CP = {sp}x100/{100-loss} = {cp}.",
        f"SP = CP × (१०० - {loss})/१०० हो। त्यसैले CP = {sp}×१००/{100-loss} = {cp} हो।")

# ---------- SI amount after t years ----------
for _ in range(80):
    p = rng.choice([1000, 2000, 4000, 5000, 8000, 10000])
    r = rng.choice([5, 8, 10, 12])
    t = rng.choice([2, 3, 4, 5])
    si = p * r * t // 100
    if p * r * t % 100: continue
    ans = p + si
    o, ai = num_opts(ans, max(100, ans-1000), ans+1000, 100)
    q_emit('Interest', 'medium', 1,
        f"What is the amount after {t} years if Rs {p} is invested at {r}% simple interest per annum?",
        f"रू {p} लाई {r}% वार्षिक साधारण ब्याजमा लगानी गर्दा {t} वर्षपछि रकम कति हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"SI = {p}x{r}x{t}/100 = {si}. Amount = {p} + {si} = {ans}.",
        f"SI = {p}×{r}×{t}/१०० = {si} हो। रकम = {p} + {si} = {ans} हो।")

# ---------- 3-person age ratio ----------
for _ in range(60):
    r1, r2, r3 = rng.choice([(2, 3, 4), (1, 2, 3), (3, 4, 5), (2, 3, 5), (1, 3, 4)])
    u = rng.choice([3, 4, 5, 6, 7, 8])
    ages = [r1*u, r2*u, r3*u]
    person = rng.choice(['A', 'B', 'C'])
    ans = ages[['A', 'B', 'C'].index(person)]
    o, ai = num_opts(ans, max(1, ans-15), ans+15, 3)
    q_emit('Age Problems', 'medium', 1,
        f"The ages of A, B and C are in the ratio {r1}:{r2}:{r3}. If the sum of their ages is {sum(ages)}, how old is {person}?",
        f"A, B र C को उमेरको अनुपात {r1}:{r2}:{r3} छ। उनीहरूको उमेरको योग {sum(ages)} छ भने {person} कति वर्षको हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Total parts = {r1+r2+r3}. One part = {sum(ages)}/{r1+r2+r3} = {u}. {person}'s age = {ages[['A','B','C'].index(person)]//u}x{u} = {ans}.",
        f"कुल भाग = {r1+r2+r3} हो। एक भाग = {sum(ages)}/{r1+r2+r3} = {u} हो। {person} को उमेर = {ages[['A','B','C'].index(person)]//u}×{u} = {ans} हो।")

# ---------- mixture: add water, new ratio ----------
for _ in range(80):
    milk = rng.choice([20, 30, 40, 50, 60])
    water = rng.choice([10, 15, 20, 25, 30])
    add = rng.choice([5, 10, 15, 20])
    new_water = water + add
    g = math.gcd(milk, new_water)
    ans_str = f"{milk//g}:{new_water//g}"
    opts = [ans_str, f"{milk}:{water}", f"{milk//g+1}:{new_water//g}", f"{milk//g}:{new_water//g+1}"]
    if len(set(opts)) < 4: continue
    o = opts[:]; rng.shuffle(o)
    q_emit('Mixtures & Alligation', 'medium', 1,
        f"A mixture contains {milk} litres of milk and {water} litres of water. If {add} litres of water is added, what is the new ratio of milk to water?",
        f"एउटा मिश्रणमा {milk} लिटर दूध र {water} लिटर पानी छ। {add} लिटर पानी थप्दा दूध र पानीको नयाँ अनुपात कति हो?",
        o, [dev(x) for x in o], o.index(ans_str),
        f"New water = {water} + {add} = {new_water} L. Ratio = {milk}:{new_water} = {ans_str}.",
        f"नयाँ पानी = {water} + {add} = {new_water} लिटर हो। अनुपात = {milk}:{new_water} = {ans_str} हो।")

n = em.write('expansion-r10-maths8.json')
print('MATHS8 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
