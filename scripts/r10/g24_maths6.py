#!/usr/bin/env python3
"""R10 generator 24: Maths 6 (~1,800). Fresh parameter spaces:
fractions-of-percent, weighted averages, 3-part ratios, efficiency work,
age ratios, mixture replacement, SI/CI difference, two-digit numbers,
consecutive sums, pipes, A-leaves work, calendar 2010-2019, clock right-angle."""
import sys, random, math, datetime
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num

bank = Bank()
em = Emitter(bank, 'R10-M6')
rng = random.Random(99173)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'tsc-primary', 'tsc-secondary', 'health', 'police', 'army']

def q_emit(ex, topic, diff, marks, q, qn, opts, optn, ans, exp, expn):
    em.emit(ex, 'Maths & Numerical', topic, diff, marks, q, qn, opts, optn, ans, exp, expn)

def num_opts(ans, lo, hi, step=1, n=3, ints=True):
    s = {ans}
    while len(s) < 4:
        v = rng.randrange(lo, hi+1, step) if ints else round(rng.uniform(lo, hi), 2)
        if v != ans and v > 0: s.add(v)
    o = list(s); rng.shuffle(o)
    return o, o.index(ans)

# ---------- % of a fraction of a number ----------
for _ in range(120):
    n = rng.choice([120, 160, 200, 240, 280, 300, 360, 400, 450, 480, 500, 600, 640, 720, 800, 900, 1000])
    a = rng.randrange(1, 9); b = rng.randrange(a+1, 10)
    if n % b: continue
    frac = a * n // b
    pct = rng.choice([10, 20, 25, 30, 40, 50, 60, 75, 80])
    if frac * pct % 100: continue
    ans = frac * pct // 100
    o, ai = num_opts(ans, max(1, ans-40), ans+40, 5)
    q_emit(EX, 'Percentages', 'medium', 1,
        f"What is {pct}% of {a}/{b} of {n}?", f"{n} को {a}/{b} को {pct}% कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"{a}/{b} of {n} = {frac}. {pct}% of {frac} = {frac} x {pct}/100 = {ans}.",
        f"{n} को {a}/{b} = {frac} हो। {frac} को {pct}% = {frac} × {pct}/१०० = {ans} हो।")

# ---------- weighted average of two groups ----------
for _ in range(100):
    n1 = rng.choice([10, 20, 25, 30, 40, 50])
    n2 = rng.choice([10, 20, 25, 30, 40, 50])
    a1 = rng.randrange(30, 90, 5); a2 = rng.randrange(30, 90, 5)
    if a1 == a2: continue
    tot = n1*a1 + n2*a2
    if tot % (n1+n2): continue
    ans = tot // (n1+n2)
    o, ai = num_opts(ans, max(1, ans-15), ans+15, 5)
    q_emit(EX, 'Averages', 'medium', 1,
        f"The average score of {n1} students is {a1} and of another {n2} students is {a2}. What is the average of all {n1+n2} students?",
        f"{n1} जना विद्यार्थीको औसत अङ्क {a1} र अन्य {n2} जनाको औसत {a2} छ। सबै {n1+n2} जनाको औसत कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Total = {n1}x{a1} + {n2}x{a2} = {tot}. Average = {tot}/{n1+n2} = {ans}.",
        f"जम्मा = {n1}×{a1} + {n2}×{a2} = {tot} हो। औसत = {tot}/{n1+n2} = {ans} हो।")

# ---------- 3-part ratio division ----------
for _ in range(100):
    r = [rng.randrange(1, 6) for _ in range(3)]
    if r[0] == r[1] == r[2]: continue
    tot_r = sum(r)
    unit = rng.choice([50, 100, 150, 200, 250, 300, 400, 500])
    total = tot_r * unit
    part = rng.randrange(3)
    ans = r[part] * unit
    names = ['A', 'B', 'C']
    o, ai = num_opts(ans, max(1, ans-200), ans+200, 50)
    q_emit(EX, 'Ratio & Proportion', 'medium', 1,
        f"Rs {total} is divided among A, B and C in the ratio {r[0]}:{r[1]}:{r[2]}. What is {names[part]}'s share?",
        f"रू {total} लाई A, B र C बीच {r[0]}:{r[1]}:{r[2]} को अनुपातमा बाँडियो। {names[part]} को हिस्सा कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Total parts = {tot_r}. One part = {total}/{tot_r} = {unit}. {names[part]}'s share = {r[part]}x{unit} = {ans}.",
        f"कुल भाग = {tot_r} हो। एक भाग = {total}/{tot_r} = {unit} हो। {names[part]} को हिस्सा = {r[part]}×{unit} = {ans} हो।")

# ---------- work efficiency: A is k times as efficient as B ----------
for _ in range(80):
    k = rng.choice([2, 3, 4])
    tb = rng.choice([12, 18, 24, 30, 36])
    # A alone takes tb/k days; together: 1/(1/ta + 1/tb)
    if tb % k: continue
    ta = tb // k
    together = (ta * tb) / (ta + tb)
    if together != int(together): continue
    ans = int(together)
    o, ai = num_opts(ans, max(1, ans-5), ans+5, 1)
    q_emit(EX, 'Work & Time', 'hard', 2,
        f"A is {k} times as efficient as B. B alone can finish a work in {tb} days. In how many days can A and B together finish it?",
        f"A, B भन्दा {k} गुणा बढी दक्ष छ। B एक्लैले एउटा काम {tb} दिनमा सक्न सक्छ। A र B सँगैले कति दिनमा सक्न सक्छन्?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"A alone takes {tb}/{k} = {ta} days. Together: 1/{ta} + 1/{tb} = {ta+tb}/{ta*tb} of work per day, so {ta*tb}/{ta+tb} = {ans} days.",
        f"A एक्लैले {tb}/{k} = {ta} दिन लिन्छ। सँगै: प्रतिदिन 1/{ta} + 1/{tb} = {ta+tb}/{ta*tb} काम, त्यसैले {ta*tb}/{ta+tb} = {ans} दिन।")

# ---------- age ratio now / after n years ----------
for _ in range(100):
    r1 = rng.randrange(2, 8); r2 = rng.randrange(1, r1)
    n = rng.choice([4, 5, 6, 8, 10])
    # after n years ratio becomes r1+? use: (r1*x + n) / (r2*x + n) = target ratio p:q
    # simpler: ages now are r1*x and r2*x; after n years their ratio is (r1x+n):(r2x+n)
    x = rng.randrange(3, 10)
    a_now = r1*x; b_now = r2*x
    a_f = a_now + n; b_f = b_now + n
    g = math.gcd(a_f, b_f)
    fa, fb = a_f//g, b_f//g
    # ask: ratio after n years
    opts = [f"{fa}:{fb}", f"{r1}:{r2}", f"{fa+1}:{fb}", f"{fa}:{fb+1}"]
    if len(set(opts)) < 4: continue
    o = opts[:]; rng.shuffle(o)
    q_emit(EX, 'Age Problems', 'medium', 1,
        f"The present ages of A and B are in the ratio {r1}:{r2}. If A is {a_now} years old now, what will be the ratio of their ages after {n} years?",
        f"A र B को अहिलेको उमेरको अनुपात {r1}:{r2} छ। यदि A अहिले {a_now} वर्षको छ भने {n} वर्षपछि उनीहरूको उमेरको अनुपात कति हुन्छ?",
        o, [dev(x) for x in o], o.index(f"{fa}:{fb}"),
        f"B's age now = {a_now}x{r2}/{r1} = {b_now}. After {n} years: A = {a_f}, B = {b_f}, ratio = {fa}:{fb}.",
        f"B को अहिलेको उमेर = {a_now}×{r2}/{r1} = {b_now} हो। {n} वर्षपछि: A = {a_f}, B = {b_f}, अनुपात = {fa}:{fb} हो।")

# ---------- mixture replacement ----------
for _ in range(80):
    tot = rng.choice([40, 50, 60, 80, 100])
    milk = rng.choice([30, 35, 40, 45, 50, 60, 70])
    if milk >= tot: continue
    rep = rng.choice([5, 10, 15, 20])
    if rep >= milk: continue
    # after replacing rep litres with water: milk = milk - rep*milk/tot
    new_milk = milk - rep*milk/tot
    if new_milk != int(new_milk): continue
    new_milk = int(new_milk)
    new_water = tot - new_milk
    g = math.gcd(new_milk, new_water)
    ans_str = f"{new_milk//g}:{new_water//g}"
    opts = [ans_str, f"{milk}:{tot-milk}", f"{new_milk}:{new_water+5}", f"{new_milk+5}:{new_water}"]
    if len(set(opts)) < 4: continue
    o = opts[:]; rng.shuffle(o)
    q_emit(EX, 'Mixtures & Alligation', 'hard', 2,
        f"A vessel contains {tot} litres of a mixture of milk and water in which milk is {milk} litres. {rep} litres of the mixture is taken out and replaced with water. What is the new ratio of milk to water?",
        f"एउटा भाँडामा {tot} लिटर दूध र पानीको मिश्रण छ, जसमा दूध {milk} लिटर छ। {rep} लिटर मिश्रण निकालेर पानी हालियो। दूध र पानीको नयाँ अनुपात कति हो?",
        o, [dev(x) for x in o], o.index(ans_str),
        f"Milk removed = {rep}x{milk}/{tot} = {rep*milk/tot:g} L. Milk left = {milk} - {rep*milk/tot:g} = {new_milk} L. Water = {tot} - {new_milk} = {new_water} L. Ratio = {ans_str}.",
        f"निकालिएको दूध = {rep}×{milk}/{tot} = {rep*milk/tot:g} लिटर। बाँकी दूध = {milk} - {rep*milk/tot:g} = {new_milk} लिटर। पानी = {tot} - {new_milk} = {new_water} लिटर। अनुपात = {ans_str} हो।")

# ---------- SI vs CI difference (2 years) ----------
for _ in range(80):
    p = rng.choice([1000, 2000, 4000, 5000, 8000, 10000, 20000])
    r = rng.choice([5, 10, 15, 20])
    diff = p * r * r / 10000
    if diff != int(diff): continue
    ans = int(diff)
    o, ai = num_opts(ans, max(1, ans-100), ans+100, 10)
    q_emit(EX, 'Interest', 'hard', 2,
        f"What is the difference between compound interest and simple interest on Rs {p} at {r}% per annum for 2 years?",
        f"रू {p} मा {r}% वार्षिक दरले २ वर्षको चक्रवृद्धि ब्याज र साधारण ब्याजबीचको फरक कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Difference = P x (R/100)^2 = {p} x ({r}/100)^2 = {ans}.",
        f"फरक = P × (R/१००)² = {p} × ({r}/१००)² = {ans} हो।")

# ---------- two-digit number: reverse digits ----------
for _ in range(80):
    a = rng.randrange(1, 10); b = rng.randrange(0, 10)
    if a == b or a < b: continue
    num = 10*a + b
    rev = 10*b + a
    diff = num - rev
    o, ai = num_opts(diff, max(1, diff-27), diff+27, 9)
    q_emit(EX, 'Number System', 'medium', 1,
        f"The sum of the digits of a two-digit number is {a+b} and the difference between the number and the number obtained by reversing its digits is {diff}. What is the number?",
        f"दुई अङ्कको सङ्ख्याको अङ्कहरूको योग {a+b} छ र सङ्ख्या र यसका अङ्कहरू उल्ट्याउँदा बन्ने सङ्ख्याबीचको फरक {diff} छ। सङ्ख्या कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Let the digits be {a} and {b}: number = {num}, reversed = {rev}, difference = {diff}.",
        f"अङ्कहरू {a} र {b} मान्दा: सङ्ख्या = {num}, उल्टो = {rev}, फरक = {diff} हो।")

# ---------- consecutive numbers sum ----------
for _ in range(80):
    start = rng.randrange(5, 60)
    k = rng.choice([3, 4, 5])
    s = sum(range(start, start+k))
    o, ai = num_opts(s, max(1, s-30), s+30, 1)
    q_emit(EX, 'Number System', 'easy', 1,
        f"What is the sum of {k} consecutive numbers starting from {start}?",
        f"{start} बाट सुरु हुने {k} वटा क्रमागत सङ्ख्याहरूको योग कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Sum = {start} + {start+1} + ... + {start+k-1} = {s}.",
        f"योग = {start} + {start+1} + ... + {start+k-1} = {s} हो।")

# ---------- pipes: fill + empty ----------
for _ in range(80):
    t1 = rng.choice([6, 8, 10, 12, 15, 20])
    t2 = rng.choice([12, 15, 20, 24, 30, 40])
    if t1 >= t2: continue
    net = 1/t1 - 1/t2
    total = 1/net
    if total != int(total): continue
    ans = int(total)
    o, ai = num_opts(ans, max(1, ans-10), ans+10, 1)
    q_emit(EX, 'Pipes & Cisterns', 'hard', 2,
        f"A pipe can fill a tank in {t1} hours and another pipe can empty it in {t2} hours. If both pipes are opened together, in how many hours will the tank be filled?",
        f"एउटा पाइपले ट्याङ्की {t1} घण्टामा भर्छ र अर्को पाइपले {t2} घण्टामा खाली गर्छ। दुवै पाइप सँगै खोल्दा ट्याङ्की कति घण्टामा भरिन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Net fill per hour = 1/{t1} - 1/{t2} = {t2-t1}/{t1*t2}. Time = {t1*t2}/{t2-t1} = {ans} hours.",
        f"प्रतिघण्टा शुद्ध भर्ने दर = 1/{t1} - 1/{t2} = {t2-t1}/{t1*t2} हो। समय = {t1*t2}/{t2-t1} = {ans} घण्टा हो।")

# ---------- A leaves after n days ----------
for _ in range(80):
    ta = rng.choice([10, 12, 15, 20, 30])
    tb = rng.choice([15, 20, 30, 40, 60])
    n = rng.choice([2, 3, 4, 5, 6])
    # work done by A+B in n days, remaining by B alone
    done = n * (1/ta + 1/tb)
    if done >= 1: continue
    rem = 1 - done
    days_b = rem * tb
    if days_b != int(days_b): continue
    ans = int(days_b)
    o, ai = num_opts(ans, max(1, ans-10), ans+10, 1)
    q_emit(EX, 'Work & Time', 'hard', 2,
        f"A and B together can finish a work in {ta} and {tb} days respectively if working alone. They work together for {n} days and then A leaves. In how many more days will B finish the remaining work?",
        f"A र B एक्लैले काम क्रमशः {ta} र {tb} दिनमा सक्न सक्छन्। उनीहरू {n} दिन सँगै काम गर्छन् र त्यसपछि A जान्छ। B ले बाँकी काम कति दिनमा सक्न सक्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Work done in {n} days = {n}x(1/{ta} + 1/{tb}) = {done:.3f}. Remaining = {1-done:.3f}. B needs {1-done:.3f}x{tb} = {ans} more days.",
        f"{n} दिनमा भएको काम = {n}×(1/{ta} + 1/{tb}) = {done:.3f} हो। बाँकी = {1-done:.3f} हो। B लाई {1-done:.3f}×{tb} = {ans} दिन थप चाहिन्छ।")

# ---------- calendar 2010-2019 ----------
for _ in range(120):
    y = rng.randrange(2010, 2020)
    m = rng.randrange(1, 13)
    d = rng.randrange(1, 29)
    dt = datetime.date(y, m, d)
    wd = dt.strftime('%A')
    ne_wd = {'Monday': 'सोमबार', 'Tuesday': 'मङ्गलबार', 'Wednesday': 'बुधबार', 'Thursday': 'बिहीबार', 'Friday': 'शुक्रबार', 'Saturday': 'शनिबार', 'Sunday': 'आइतबार'}[wd]
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    ne_m = ['जनवरी', 'फेब्रुअरी', 'मार्च', 'अप्रिल', 'मे', 'जुन', 'जुलाई', 'अगस्ट', 'सेप्टेम्बर', 'अक्टोबर', 'नोभेम्बर', 'डिसेम्बर'][m-1]
    others = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    others.remove(wd)
    rng.shuffle(others)
    opts = [wd] + others[:3]
    optn = [ne_wd] + [ne_wd]  # placeholder fixed below
    ne_map = {'Monday': 'सोमबार', 'Tuesday': 'मङ्गलबार', 'Wednesday': 'बुधबार', 'Thursday': 'बिहीबार', 'Friday': 'शुक्रबार', 'Saturday': 'शनिबार', 'Sunday': 'आइतबार'}
    optn = [ne_map[x] for x in opts]
    o = opts[:]; rng.shuffle(o)
    q_emit(EX, 'Calendar & Clock', 'medium', 1,
        f"What day of the week was {d} {months[m-1]} {y}?", f"{y} को {ne_m} {d} गते कुन बार थियो?",
        o, [ne_map[x] for x in o], o.index(wd),
        f"{d} {months[m-1]} {y} was a {wd}.", f"{y} को {ne_m} {d} गते {ne_wd} थियो।")

# ---------- clock: hands at right angle (approx times) ----------
for _ in range(60):
    h = rng.randrange(1, 12)
    # right angle approx at h:05 and h:38 roughly; use the "h:05" approx? Too imprecise.
    # Instead: angle between hands at h:00
    ang = 30 * h
    if ang > 180: ang = 360 - ang
    o, ai = num_opts(ang, 0, 180, 30)
    q_emit(EX, 'Calendar & Clock', 'easy', 1,
        f"What is the angle between the hands of a clock at {h} o'clock?",
        f"घडीमा {h} बज्दा सुईहरूबीचको कोण कति हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"At {h} o'clock the minute hand is at 12 and the hour hand is {h} hours ahead: angle = {h}x30 = {ang} degrees (taking the smaller angle).",
        f"{h} बज्दा मिनेटको सुई १२ मा र घण्टाको सुई {h} घण्टा अगाडि हुन्छ: कोण = {h}×३० = {ang} डिग्री (सानो कोण) हो।")

# ---------- average of first n multiples of k ----------
for _ in range(80):
    k = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    n = rng.choice([5, 10, 15, 20, 25, 30, 40, 50])
    ans = k * (n + 1) // 2
    if k * (n + 1) % 2: continue
    o, ai = num_opts(ans, max(1, ans-20), ans+20, 5)
    q_emit(EX, 'Averages', 'medium', 1,
        f"What is the average of the first {n} multiples of {k}?",
        f"{k} का पहिलो {n} वटा गुणनहरूको औसत कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Sum of first {n} multiples of {k} = {k}x{n}x{n+1}/2 = {k*n*(n+1)//2}. Average = {k*n*(n+1)//2}/{n} = {ans}.",
        f"{k} का पहिलो {n} गुणनहरूको योग = {k}×{n}×{n+1}/२ = {k*n*(n+1)//2} हो। औसत = {k*n*(n+1)//2}/{n} = {ans} हो।")

# ---------- trains: crossing a man (time) ----------
for _ in range(80):
    length = rng.choice([120, 150, 180, 200, 240, 270, 300, 360])
    speed = rng.choice([36, 45, 54, 60, 72, 90])
    t = length / (speed * 5/18)
    if t != int(t): continue
    ans = int(t)
    o, ai = num_opts(ans, max(1, ans-10), ans+10, 1)
    q_emit(EX, 'Trains', 'medium', 1,
        f"A train {length} m long runs at {speed} km/h. In how many seconds will it cross a man standing on the platform?",
        f"{length} मिटर लामो रेल {speed} किमी/घण्टाको गतिमा चल्छ। प्लेटफर्ममा उभिएको मानिसलाई पार गर्न कति सेकेन्ड लाग्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Speed = {speed}x5/18 = {speed*5/18:g} m/s. Time = {length}/{speed*5/18:g} = {ans} seconds.",
        f"गति = {speed}×५/१८ = {speed*5/18:g} मि/से हो। समय = {length}/{speed*5/18:g} = {ans} सेकेन्ड हो।")

# ---------- boats: downstream time ----------
for _ in range(80):
    vb = rng.choice([6, 8, 10, 12, 15])
    vc = rng.choice([2, 3, 4, 5])
    d = rng.choice([24, 30, 36, 40, 48, 60, 72])
    if d % (vb + vc): continue
    ans = d // (vb + vc)
    o, ai = num_opts(ans, max(1, ans-5), ans+5, 1)
    q_emit(EX, 'Boats & Streams', 'medium', 1,
        f"A boat's speed in still water is {vb} km/h and the stream's speed is {vc} km/h. How many hours will it take to travel {d} km downstream?",
        f"स्थिर पानीमा डुङ्गाको गति {vb} किमी/घण्टा र खोलाको गति {vc} किमी/घण्टा छ। {d} किमी तलतिर जान कति घण्टा लाग्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Downstream speed = {vb} + {vc} = {vb+vc} km/h. Time = {d}/{vb+vc} = {ans} hours.",
        f"तलतिरको गति = {vb} + {vc} = {vb+vc} किमी/घण्टा हो। समय = {d}/{vb+vc} = {ans} घण्टा हो।")

# ---------- SI find principal ----------
for _ in range(80):
    si = rng.choice([200, 300, 400, 500, 600, 800, 1000, 1200])
    r = rng.choice([4, 5, 8, 10, 12])
    t = rng.choice([2, 3, 4, 5])
    p = si * 100 / (r * t)
    if p != int(p): continue
    ans = int(p)
    o, ai = num_opts(ans, max(100, ans-1000), ans+1000, 100)
    q_emit(EX, 'Interest', 'medium', 1,
        f"The simple interest on a sum for {t} years at {r}% per annum is Rs {si}. What is the sum?",
        f"कुनै रकममा {t} वर्षको {r}% वार्षिक दरले साधारण ब्याज रू {si} हुन्छ। रकम कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"P = SI x 100 / (R x T) = {si}x100/({r}x{t}) = {ans}.",
        f"P = SI × १०० / (R × T) = {si}×१००/({r}×{t}) = {ans} हो।")

# ---------- rectangle perimeter with side ratio ----------
for _ in range(80):
    r1 = rng.randrange(1, 6); r2 = rng.randrange(1, 6)
    if r1 == r2: continue
    u = rng.choice([2, 3, 4, 5, 6, 8, 10])
    l, w = r1*u, r2*u
    per = 2*(l+w)
    o, ai = num_opts(per, max(1, per-20), per+20, 4)
    q_emit(EX, 'Geometry', 'easy', 1,
        f"The length and breadth of a rectangle are in the ratio {r1}:{r2} and are {l} cm and {w} cm respectively. What is its perimeter?",
        f"आयतको लम्बाइ र चौडाइको अनुपात {r1}:{r2} छ र क्रमशः {l} सेमी र {w} सेमी छन्। यसको परिमिति कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Perimeter = 2 x (length + breadth) = 2 x ({l} + {w}) = {per} cm.",
        f"परिमिति = २ × (लम्बाइ + चौडाइ) = २ × ({l} + {w}) = {per} सेमी हो।")

# ---------- series: x2+3, x3-2, +primes, alternating ----------
def series_block(gen, name, n=90):
    for _ in range(n):
        seq, ans = gen()
        if seq is None: continue
        disp = ', '.join(str(x) for x in seq)
        o, ai = num_opts(ans, max(0, ans-20), ans+20, 1)
        q_emit(EX, 'Number Series', 'medium', 1,
            f"What is the next number in the series: {disp}, ...?", f"श्रेणीको अर्को सङ्ख्या कति हो: {disp}, ...?",
            [str(x) for x in o], [dev_num(x) for x in o], ai,
            f"The series follows the {name} pattern. The next term is {ans}.",
            f"श्रेणीले {name} ढाँचा पछ्याउँछ। अर्को पद {ans} हो।")

def gen_x2p3():
    a = rng.randrange(2, 15); seq = [a]
    for _ in range(4): seq.append(seq[-1]*2 + 3)
    return seq, seq[-1]*2 + 3
def gen_x3m2():
    a = rng.randrange(3, 15); seq = [a]
    for _ in range(4): seq.append(seq[-1]*3 - 2)
    return seq, seq[-1]*3 - 2
def gen_plus_primes():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    a = rng.randrange(5, 30); seq = [a]; i = rng.randrange(0, 4)
    for k in range(4): seq.append(seq[-1] + primes[i+k])
    return seq, seq[-1] + primes[i+4]
def gen_alt():
    a = rng.randrange(10, 40); p = rng.choice([3, 4, 5, 6]); q = rng.choice([2, 3, 4])
    seq = [a]
    for k in range(4):
        seq.append(seq[-1] + p if k % 2 == 0 else seq[-1] - q)
    nxt = seq[-1] + p if len(seq) % 2 == 1 else seq[-1] - q
    return seq, nxt
series_block(gen_x2p3, 'multiply by 2 and add 3')
series_block(gen_x3m2, 'multiply by 3 and subtract 2')
series_block(gen_plus_primes, 'add consecutive prime numbers')
series_block(gen_alt, 'alternately add and subtract')

# ---------- percentage decrease with decimals ----------
for _ in range(80):
    n = rng.choice([200, 400, 500, 800, 1000, 1200, 2000])
    pct = rng.choice([12.5, 37.5, 62.5, 87.5])
    ans = int(n * pct / 100)
    if n * pct % 100: continue
    o, ai = num_opts(ans, max(1, ans-50), ans+50, 25)
    q_emit(EX, 'Percentages', 'medium', 1,
        f"What is {pct}% of {n}?", f"{n} को {pct}% कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"{pct}% of {n} = {n} x {pct}/100 = {ans}.",
        f"{n} को {pct}% = {n} × {pct}/१०० = {ans} हो।")

# ---------- discount: find MP ----------
for _ in range(80):
    sp = rng.choice([450, 540, 630, 720, 810, 900, 1080, 1200, 1350, 1800])
    d = rng.choice([10, 20, 25, 30, 40])
    mp = sp * 100 / (100 - d)
    if mp != int(mp): continue
    ans = int(mp)
    o, ai = num_opts(ans, max(100, ans-300), ans+300, 50)
    q_emit(EX, 'Profit & Loss', 'medium', 1,
        f"After a discount of {d}%, an article is sold for Rs {sp}. What was its marked price?",
        f"{d}% छुटपछि एउटा सामान रू {sp} मा बेचियो। यसको अङ्कित मूल्य कति थियो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"SP = MP x (100 - {d})/100. So MP = {sp}x100/{100-d} = {ans}.",
        f"SP = MP × (१०० - {d})/१०० हो। त्यसैले MP = {sp}×१००/{100-d} = {ans} हो।")

# ---------- average speed round trip ----------
for _ in range(80):
    v1 = rng.choice([30, 40, 50, 60])
    v2 = rng.choice([40, 50, 60, 80, 90])
    if v1 == v2: continue
    avg = 2*v1*v2/(v1+v2)
    if avg != int(avg): continue
    ans = int(avg)
    o, ai = num_opts(ans, max(1, ans-10), ans+10, 2)
    q_emit(EX, 'Speed, Distance & Time', 'medium', 1,
        f"A car goes from A to B at {v1} km/h and returns at {v2} km/h. What is its average speed for the whole journey?",
        f"एउटा कार A बाट B सम्म {v1} किमी/घण्टामा जान्छ र {v2} किमी/घण्टामा फर्कन्छ। सम्पूर्ण यात्राको औसत गति कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Average speed = 2 x {v1} x {v2} / ({v1} + {v2}) = {ans} km/h.",
        f"औसत गति = २ × {v1} × {v2} / ({v1} + {v2}) = {ans} किमी/घण्टा हो।")

# ---------- men-days: more men, fewer days ----------
for _ in range(80):
    m1 = rng.choice([10, 12, 15, 20, 25, 30])
    d1 = rng.choice([8, 10, 12, 15, 20, 24, 30])
    m2 = rng.choice([15, 20, 25, 30, 40, 50, 60])
    if m2 <= m1: continue
    d2 = m1 * d1 / m2
    if d2 != int(d2): continue
    ans = int(d2)
    o, ai = num_opts(ans, max(1, ans-5), ans+5, 1)
    q_emit(EX, 'Work & Time', 'easy', 1,
        f"{m1} men can finish a work in {d1} days. In how many days can {m2} men finish the same work?",
        f"{m1} जना मानिसले एउटा काम {d1} दिनमा सक्न सक्छन्। {m2} जनाले उही काम कति दिनमा सक्न सक्छन्?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Total work = {m1}x{d1} = {m1*d1} man-days. Days for {m2} men = {m1*d1}/{m2} = {ans}.",
        f"कुल काम = {m1}×{d1} = {m1*d1} मानिस-दिन हो। {m2} जनालाई लाग्ने दिन = {m1*d1}/{m2} = {ans} हो।")

n = em.write('expansion-r10-maths6.json')
print('MATHS6 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
