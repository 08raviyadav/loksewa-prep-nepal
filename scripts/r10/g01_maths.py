#!/usr/bin/env python3
"""R10 generator 1: computed Maths & Numerical drills (~5,000).
Every answer is computed by the script (exact arithmetic), so keys are
correct by construction. Explanations end on the answer as the last '='.
"""
import sys, random, math, datetime
from fractions import Fraction
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num, fmt

bank = Bank()
em = Emitter(bank, 'R10-MATH')
rng = random.Random(71001)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'police', 'army', 'tsc-primary', 'tsc-secondary']
EXH = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'csit-entrance', 'ioe-entrance', 'mecee-bl']

def opts4(correct, cands):
    """Return [correct, d1, d2, d3] distinct (formatted strings)."""
    out = [correct]
    for c in cands:
        if len(out) == 4:
            break
        if c not in out:
            out.append(c)
    # pad with deltas if short
    d = 1
    while len(out) < 4:
        for c in (correct + d, correct - d, correct + 10 * d, correct - 10 * d):
            if c not in out and c > 0:
                out.append(c)
                break
        d += 1
    return out

def num_opts(correct, cands):
    """Numeric options as strings (EN) + Devanagari (NE)."""
    o = opts4(correct, cands)
    return [fmt(x) for x in o], [dev_num(x) for x in o], 0

def rs_opts(correct, cands):
    o = opts4(correct, cands)
    return ['Rs ' + fmt(x) for x in o], ['रू ' + dev_num(x) for x in o], 0

# ---------------- 1. Percentage of a number ----------------
for pct in [5, 10, 12.5, 15, 20, 25, 30, 40, 45, 50, 60, 75, 80, 90]:
    for N in [40, 60, 80, 120, 160, 200, 240, 300, 400, 500, 600, 800, 1000, 1200, 1500, 2000]:
        v = N * pct / 100
        if v != int(v):
            continue
        v = int(v)
        oe, on, a = num_opts(v, [v + N // 10, v - N // 10, v + pct, v * 2, N - v, v + 20])
        em.emit(EX, 'Maths & Numerical', 'Percentage', 'easy' if pct in (10, 25, 50, 75) else 'medium', 2,
                f'What is {fmt(pct)}% of {N}?', f'{dev_num(N)} को {dev(fmt(pct))}% कति हो?',
                oe, on, a,
                f'{fmt(pct)}% of {N} = {N} x {fmt(pct)}/100 = {v}.',
                f'{dev_num(N)} को {dev(fmt(pct))}% = {dev_num(N)} × {dev(fmt(pct))}/१०० = {dev_num(v)}।')

# ---------------- 2. Percentage increase / decrease ----------------
for pct in [5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80]:
    for N in [80, 120, 200, 240, 300, 400, 500, 600, 800, 1000, 1200, 1500]:
        for up in (True, False):
            delta = N * pct / 100
            if delta != int(delta):
                continue
            v = int(N + delta) if up else int(N - delta)
            oe, on, a = num_opts(v, [N, int(N + delta) if not up else int(N - delta), v + int(delta), v - int(delta)])
            w = 'increased' if up else 'decreased'
            wn = 'बढाइयो' if up else 'घटाइयो'
            em.emit(EX, 'Maths & Numerical', 'Percentage', 'medium', 2,
                    f'What is {N} {w} by {fmt(pct)}%?', f'{dev_num(N)} लाई {dev(fmt(pct))}% ले {wn} भने कति हुन्छ?',
                    oe, on, a,
                    f'{fmt(pct)}% of {N} is {int(delta)}. {N} {w} by {fmt(pct)}% = {N} {"+" if up else "-"} {int(delta)} = {v}.',
                    f'{dev_num(N)} को {dev(fmt(pct))}% भनेको {dev_num(int(delta))} हो। {dev_num(N)} लाई {dev(fmt(pct))}% ले {wn} भने {dev_num(N)} {"+" if up else "−"} {dev_num(int(delta))} = {dev_num(v)} हुन्छ।')

# ---------------- 3. Find the number from a percentage ----------------
for pct in [5, 10, 20, 25, 30, 40, 50, 60, 75, 80]:
    for part in [20, 30, 40, 50, 60, 80, 90, 100, 120, 150, 200, 240, 300, 400]:
        whole = part * 100 / pct
        if whole != int(whole):
            continue
        whole = int(whole)
        oe, on, a = num_opts(whole, [part, whole + part, whole - part, whole * 2])
        em.emit(EX, 'Maths & Numerical', 'Percentage', 'medium', 2,
                f'{fmt(pct)}% of a number is {part}. What is the number?',
                f'कुनै सङ्ख्याको {dev(fmt(pct))}% भनेको {dev_num(part)} हो। त्यो सङ्ख्या कति हो?',
                oe, on, a,
                f'Let the number be x. {fmt(pct)}% of x = {part}, so x = {part} x 100/{fmt(pct)} = {whole}.',
                f'सङ्ख्या x मानौँ। x को {dev(fmt(pct))}% = {dev_num(part)} भएकाले x = {dev_num(part)} × १००/{dev(fmt(pct))} = {dev_num(whole)} हुन्छ।')

# ---------------- 4. A as a percentage of B ----------------
for a, b in [(25, 100), (30, 120), (45, 90), (60, 240), (75, 300), (18, 72), (24, 96), (35, 140),
             (40, 160), (50, 250), (80, 320), (90, 360), (15, 60), (12, 48), (36, 144), (48, 192),
             (70, 280), (55, 220), (65, 260), (85, 340), (95, 380), (27, 108), (33, 132), (44, 176)]:
    p = a * 100 / b
    if p != int(p):
        continue
    p = int(p)
    oe, on, aidx = num_opts(p, [p + 5, p - 5, p + 10, 100 - p])
    em.emit(EX, 'Maths & Numerical', 'Percentage', 'medium', 2,
            f'{a} is what percent of {b}?', f'{dev_num(a)} भनेको {dev_num(b)} को कति प्रतिशत हो?',
            [fmt(x) + '%' for x in oe], [dev_num(x) + '%' for x in on], aidx,
            f'{a}/{b} x 100 = {p}%.',
            f'{dev_num(a)}/{dev_num(b)} × १०० = {dev_num(p)}%।')

# ---------------- 5. Profit / loss percent ----------------
cases = []
for cp in [100, 200, 250, 400, 500, 800, 1000, 1200, 1500, 2000]:
    for pct in [5, 10, 15, 20, 25, 30, 40, 50]:
        sp = cp * (100 + pct) / 100
        if sp == int(sp):
            cases.append((cp, int(sp), pct, 'profit'))
        sp = cp * (100 - pct) / 100
        if sp == int(sp):
            cases.append((cp, int(sp), pct, 'loss'))
for cp, sp, pct, kind in cases:
    oe, on, a = num_opts(pct, [pct + 5, pct - 5, pct + 10, pct * 2])
    em.emit(EX, 'Maths & Numerical', 'Profit & Loss', 'medium', 2,
            f'A shopkeeper buys an article for Rs {cp} and sells it for Rs {sp}. What is the {kind} percent?',
            f'एक पसलेले रु {dev_num(cp)} मा किनेको सामान रु {dev_num(sp)} मा बेच्छ। {"नाफा" if kind == "profit" else "नोक्सान"} प्रतिशत कति हो?',
            [fmt(x) + '%' for x in oe], [dev_num(x) + '%' for x in on], a,
            f'{kind.capitalize()} = Rs {abs(sp - cp)}. {kind.capitalize()}% = {abs(sp - cp)}/{cp} x 100 = {pct}%.',
            f'{"नाफा" if kind == "profit" else "नोक्सान"} = रु {dev_num(abs(sp - cp))}। {"नाफा" if kind == "profit" else "नोक्सान"}% = {dev_num(abs(sp - cp))}/{dev_num(cp)} × १०० = {dev_num(pct)}%।')

# ---------------- 6. Profit / loss amount ----------------
for cp in [200, 400, 500, 600, 800, 1000, 1200, 1500, 2000, 2500]:
    for pct in [10, 20, 25, 30, 40, 50]:
        sp = cp * (100 + pct) // 100
        if cp * (100 + pct) % 100:
            continue
        oe, on, a = rs_opts(sp, [cp, sp + 100, sp - 100, cp + pct])
        em.emit(EX, 'Maths & Numerical', 'Profit & Loss', 'easy', 2,
                f'An article bought for Rs {cp} is sold at a profit of {pct}%. What is the selling price?',
                f'रु {dev_num(cp)} मा किनेको सामान {dev(fmt(pct))}% नाफामा बेच्दा बिक्री मूल्य कति हुन्छ?',
                oe, on, a,
                f'Profit = {pct}% of Rs {cp} = Rs {sp - cp}. Selling price = {cp} + {sp - cp} = Rs {sp}.',
                f'नाफा = रु {dev_num(cp)} को {dev(fmt(pct))}% = रु {dev_num(sp - cp)}। बिक्री मूल्य = {dev_num(cp)} + {dev_num(sp - cp)} = रु {dev_num(sp)}।')

# ---------------- 7. Simple interest ----------------
for P in [1000, 2000, 4000, 5000, 8000, 10000, 12000, 15000, 20000, 25000]:
    for R in [4, 5, 6, 8, 10, 12]:
        for T in [2, 3, 4, 5]:
            si = P * R * T // 100
            if P * R * T % 100:
                continue
            oe, on, a = rs_opts(si, [si + P // 10, si - P // 10, P * R // 100, si * 2])
            em.emit(EX, 'Maths & Numerical', 'Simple Interest', 'medium', 2,
                    f'Find the simple interest on Rs {P} at {R}% per annum for {T} years.',
                    f'रु {dev_num(P)} को {dev(fmt(R))}% वार्षिक ब्याजदरमा {dev_num(T)} वर्षको साधारण ब्याज कति हुन्छ?',
                    oe, on, a,
                    f'SI = P x R x T / 100 = {P} x {R} x {T} / 100 = Rs {si}.',
                    f'साधारण ब्याज = मूलधन × दर × समय / १०० = {dev_num(P)} × {dev(fmt(R))} × {dev_num(T)} / १०० = रु {dev_num(si)}।')

# ---------------- 8. Compound interest (2-3 years) ----------------
for P in [1000, 2000, 4000, 5000, 8000, 10000, 20000]:
    for R in [5, 10, 20]:
        for T in [2, 3]:
            amt = P * (1 + R / 100) ** T
            if abs(amt - round(amt)) > 0.01:
                continue
            amt = int(round(amt))
            ci = amt - P
            oe, on, a = rs_opts(ci, [ci + 100, ci - 100, P * R // 100, ci + P // 10])
            em.emit(EXH, 'Maths & Numerical', 'Compound Interest', 'hard', 2,
                    f'Find the compound interest on Rs {P} at {R}% per annum for {T} years.',
                    f'रु {dev_num(P)} को {dev(fmt(R))}% वार्षिक ब्याजदरमा {dev_num(T)} वर्षको चक्रवृद्धि ब्याज कति हुन्छ?',
                    oe, on, a,
                    f'Amount = {P} x (1 + {R}/100)^{T} = Rs {amt}. CI = {amt} - {P} = Rs {ci}.',
                    f'मिश्रधन = {dev_num(P)} × (१ + {dev(fmt(R))}/१००)^{dev_num(T)} = रु {dev_num(amt)}। चक्रवृद्धि ब्याज = {dev_num(amt)} − {dev_num(P)} = रु {dev_num(ci)}।')

# ---------------- 9. Speed / distance / time ----------------
for v in [20, 25, 30, 40, 45, 50, 60, 72, 80, 90]:
    for t in [2, 3, 4, 5, 6, 8]:
        d = v * t
        oe, on, a = num_opts(d, [d + v, d - v, d + 2 * v, v * (t + 1)])
        em.emit(EX, 'Maths & Numerical', 'Speed Distance Time', 'easy', 2,
                f'A vehicle travels at {v} km/h for {t} hours. How far does it travel?',
                f'एउटा सवारी {dev_num(v)} किमी/घण्टाको गतिमा {dev_num(t)} घण्टा चल्छ। यसले कति दूरी पार गर्छ?',
                [fmt(x) + ' km' for x in oe], [dev_num(x) + ' किमी' for x in on], a,
                f'Distance = speed x time = {v} x {t} = {d} km.',
                f'दूरी = गति × समय = {dev_num(v)} × {dev_num(t)} = {dev_num(d)} किमी।')
for d in [120, 150, 180, 200, 240, 300, 360, 400, 450, 600]:
    for v in [30, 40, 50, 60, 75, 80, 90, 100, 120]:
        if d % v:
            continue
        t = d // v
        oe, on, a = num_opts(t, [t + 1, t - 1 if t > 1 else t + 2, t + 2, t * 2])
        em.emit(EX, 'Maths & Numerical', 'Speed Distance Time', 'medium', 2,
                f'How long will it take to travel {d} km at a speed of {v} km/h?',
                f'{dev_num(v)} किमी/घण्टाको गतिमा {dev_num(d)} किमी यात्रा गर्न कति समय लाग्छ?',
                [fmt(x) + ' hours' for x in oe], [dev_num(x) + ' घण्टा' for x in on], a,
                f'Time = distance / speed = {d}/{v} = {t} hours.',
                f'समय = दूरी / गति = {dev_num(d)}/{dev_num(v)} = {dev_num(t)} घण्टा।')

# ---------------- 10. Average ----------------
for _ in range(220):
    n = rng.choice([3, 4, 5])
    base = rng.choice([10, 20, 25, 30, 40, 50, 60, 100])
    step = rng.choice([2, 4, 5, 10])
    nums = [base + i * step for i in range(n)]
    if rng.random() < 0.5:
        nums = [x + rng.choice([-3, -2, -1, 1, 2, 3]) for x in nums]
    s = sum(nums)
    if s % n:
        continue
    avg = s // n
    oe, on, a = num_opts(avg, [avg + step, avg - step, avg + 5, s // (n + 1) if (n + 1) else avg + 1])
    lst = ', '.join(str(x) for x in nums)
    lstn = ', '.join(dev_num(x) for x in nums)
    em.emit(EX, 'Maths & Numerical', 'Average', 'easy', 2,
            f'Find the average of {lst}.', f'{lstn} को औसत कति हो?',
            oe, on, a,
            f'Sum = {s}. Average = {s}/{n} = {avg}.',
            f'योगफल = {dev_num(s)}। औसत = {dev_num(s)}/{dev_num(n)} = {dev_num(avg)}।')

# ---------------- 11. Ratio division ----------------
for total in [120, 180, 240, 300, 360, 420, 480, 600, 720, 900, 1000, 1200]:
    for r1, r2 in [(1, 2), (2, 3), (3, 4), (1, 3), (2, 5), (3, 5), (4, 5), (1, 5), (2, 7), (3, 7), (5, 7)]:
        if total % (r1 + r2):
            continue
        part = total * r1 // (r1 + r2)
        oe, on, a = num_opts(part, [total - part, part + 10, part - 10, total // (r1 + r2)])
        em.emit(EX, 'Maths & Numerical', 'Ratio & Proportion', 'medium', 2,
                f'Rs {total} is divided between A and B in the ratio {r1}:{r2}. How much does A get?',
                f'रु {dev_num(total)} लाई A र B बीच {dev(r1)}:{dev(r2)} को अनुपातमा बाँड्दा A ले कति पाउँछ?',
                ['Rs ' + fmt(x) for x in oe], ['रू ' + dev_num(x) for x in on], a,
                f'Sum of ratio parts = {r1 + r2}. A gets {r1}/{r1 + r2} x {total} = Rs {part}.',
                f'अनुपातका भागहरूको योग = {dev_num(r1 + r2)}। A ले {dev(r1)}/{dev_num(r1 + r2)} × {dev_num(total)} = रु {dev_num(part)} पाउँछ।')

# ---------------- 12. Age problems ----------------
for mult in [2, 3, 4, 5, 6]:
    for son in [5, 6, 8, 10, 12, 15, 18, 20]:
        for after in [3, 5, 10]:
            father_now = mult * son
            father_after = father_now + after
            oe, on, a = num_opts(father_after, [father_now, father_after + mult, father_after - mult, son + after])
            em.emit(EX, 'Maths & Numerical', 'Age Problems', 'medium', 2,
                    f'A father is {mult} times as old as his son. If the son is {son} years old now, how old will the father be after {after} years?',
                    f'बुबा छोराको भन्दा {dev(mult)} गुणा जेठा छन्। छोरा अहिले {dev_num(son)} वर्षको छ भने {dev_num(after)} वर्षपछि बुबा कति वर्षका हुनेछन्?',
                    [fmt(x) + ' years' for x in oe], [dev_num(x) + ' वर्ष' for x in on], a,
                    f'Father is now {son} x {mult} = {father_now} years. After {after} years he will be {father_now} + {after} = {father_after} years.',
                    f'बुबा अहिले {dev_num(son)} × {dev(mult)} = {dev_num(father_now)} वर्षका छन्। {dev_num(after)} वर्षपछि उनी {dev_num(father_now)} + {dev_num(after)} = {dev_num(father_after)} वर्षका हुनेछन्।')

# ---------------- 13. HCF / LCM ----------------
pairs = set()
while len(pairs) < 160:
    a = rng.randint(2, 60)
    b = rng.randint(2, 60)
    if a == b:
        continue
    pairs.add((min(a, b), max(a, b)))
for a, b in sorted(pairs):
    g = math.gcd(a, b)
    l = a * b // g
    oe, on, ai = num_opts(g, [g + 1, g + 2, g * 2, a])
    em.emit(EXH, 'Maths & Numerical', 'HCF & LCM', 'medium', 1,
            f'Find the HCF of {a} and {b}.', f'{dev_num(a)} र {dev_num(b)} को मस (HCF) कति हो?',
            oe, on, ai,
            f'Factors of {a} and {b} share the greatest common factor {g}, so HCF = {g}.',
            f'{dev_num(a)} र {dev_num(b)} का साझा गुणनखण्डहरूमध्ये सबैभन्दा ठूलो {dev_num(g)} हो, त्यसैले मस = {dev_num(g)}।')
    oe, on, ai = num_opts(l, [l + a, l - a, l + b, a * b])
    em.emit(EXH, 'Maths & Numerical', 'HCF & LCM', 'medium', 1,
            f'Find the LCM of {a} and {b}.', f'{dev_num(a)} र {dev_num(b)} को लस (LCM) कति हो?',
            oe, on, ai,
            f'LCM = {a} x {b} / HCF = {a * b}/{g} = {l}.',
            f'लस = {dev_num(a)} × {dev_num(b)} / मस = {dev_num(a * b)}/{dev_num(g)} = {dev_num(l)}।')

# ---------------- 14. Square / cube roots ----------------
for n in range(4, 51):
    v = n * n
    oe, on, a = num_opts(n, [n + 1, n - 1, n + 2, n * 2])
    em.emit(EX, 'Maths & Numerical', 'Square Roots', 'easy', 1,
            f'What is the square root of {v}?', f'{dev_num(v)} को वर्गमूल कति हो?',
            oe, on, a,
            f'{n} x {n} = {v}, so the square root of {v} is {n}.',
            f'{dev_num(n)} × {dev_num(n)} = {dev_num(v)} भएकाले {dev_num(v)} को वर्गमूल {dev_num(n)} हो।')
for n in range(2, 16):
    v = n ** 3
    oe, on, a = num_opts(n, [n + 1, n - 1, n + 2, n * 2])
    em.emit(EX, 'Maths & Numerical', 'Square Roots', 'easy', 1,
            f'What is the cube root of {v}?', f'{dev_num(v)} को घनमूल कति हो?',
            oe, on, a,
            f'{n} x {n} x {n} = {v}, so the cube root of {v} is {n}.',
            f'{dev_num(n)} × {dev_num(n)} × {dev_num(n)} = {dev_num(v)} भएकाले {dev_num(v)} को घनमूल {dev_num(n)} हो।')

# ---------------- 15. Simplification (BODMAS) ----------------
for _ in range(420):
    a = rng.randint(3, 40)
    b = rng.randint(2, 15)
    c = rng.randint(2, 12)
    kind = rng.choice(['add_mul', 'sub_mul', 'mul_add_sub', 'div_add', 'mul_mul_add'])
    if kind == 'add_mul':
        v = a + b * c
        q, qn = f'{a} + {b} x {c} = ?', f'{dev_num(a)} + {dev_num(b)} × {dev_num(c)} = ?'
        ex = f'{b} x {c} = {b * c} first, then {a} + {b * c} = {v}.'
        exn = f'पहिले {dev_num(b)} × {dev_num(c)} = {dev_num(b * c)}, त्यसपछि {dev_num(a)} + {dev_num(b * c)} = {dev_num(v)}।'
    elif kind == 'sub_mul':
        v = a * b - c
        q, qn = f'{a} x {b} - {c} = ?', f'{dev_num(a)} × {dev_num(b)} − {dev_num(c)} = ?'
        ex = f'{a} x {b} = {a * b} first, then {a * b} - {c} = {v}.'
        exn = f'पहिले {dev_num(a)} × {dev_num(b)} = {dev_num(a * b)}, त्यसपछि {dev_num(a * b)} − {dev_num(c)} = {dev_num(v)}।'
    elif kind == 'mul_add_sub':
        v = a * b + c * 2 - 5
        q, qn = f'{a} x {b} + {c} x 2 - 5 = ?', f'{dev_num(a)} × {dev_num(b)} + {dev_num(c)} × २ − ५ = ?'
        ex = f'{a} x {b} = {a * b} and {c} x 2 = {c * 2}; {a * b} + {c * 2} - 5 = {v}.'
        exn = f'{dev_num(a)} × {dev_num(b)} = {dev_num(a * b)} र {dev_num(c)} × २ = {dev_num(c * 2)}; {dev_num(a * b)} + {dev_num(c * 2)} − ५ = {dev_num(v)}।'
    elif kind == 'div_add':
        d = rng.choice([2, 3, 4, 5, 6, 8, 10])
        a2 = d * rng.randint(3, 20)
        v = a2 // d + b
        q, qn = f'{a2} / {d} + {b} = ?', f'{dev_num(a2)} / {dev_num(d)} + {dev_num(b)} = ?'
        ex = f'{a2} / {d} = {a2 // d} first, then {a2 // d} + {b} = {v}.'
        exn = f'पहिले {dev_num(a2)} / {dev_num(d)} = {dev_num(a2 // d)}, त्यसपछि {dev_num(a2 // d)} + {dev_num(b)} = {dev_num(v)}।'
    else:
        v = a * b + c
        q, qn = f'{a} x {b} + {c} = ?', f'{dev_num(a)} × {dev_num(b)} + {dev_num(c)} = ?'
        ex = f'{a} x {b} = {a * b}, then {a * b} + {c} = {v}.'
        exn = f'{dev_num(a)} × {dev_num(b)} = {dev_num(a * b)}, त्यसपछि {dev_num(a * b)} + {dev_num(c)} = {dev_num(v)}।'
    oe, on, aidx = num_opts(v, [v + 1, v - 1, v + 10, v + b])
    em.emit(EX, 'Maths & Numerical', 'Simplification', 'easy', 1,
            f'What is the value of {q}', f'{qn} को मान कति हो?',
            oe, on, aidx, ex, exn)

# ---------------- 16. Work & time ----------------
for a in [4, 5, 6, 8, 10, 12, 15, 20]:
    for b in [4, 5, 6, 8, 10, 12, 15, 20, 30]:
        if a == b:
            continue
        t = Fraction(a * b, a + b)
        if t.denominator != 1:
            continue
        t = int(t)
        oe, on, ai = num_opts(t, [t + 1, t + 2, a, b])
        em.emit(EXH, 'Maths & Numerical', 'Work & Time', 'hard', 2,
                f'A can do a work in {a} days and B can do the same work in {b} days. In how many days can they finish the work together?',
                f'A ले एउटा काम {dev_num(a)} दिनमा र B ले त्यही काम {dev_num(b)} दिनमा सक्छन्। दुवै मिलेर काम कति दिनमा सकिन्छ?',
                [fmt(x) + ' days' for x in oe], [dev_num(x) + ' दिन' for x in on], ai,
                f'Together they do 1/{a} + 1/{b} = {a + b}/{a * b} of the work per day, so they need {a * b}/{a + b} = {t} days.',
                f'दुवैले प्रतिदिन १/{dev_num(a)} + १/{dev_num(b)} = {dev_num(a + b)}/{dev_num(a * b)} भाग काम गर्छन्, त्यसैले {dev_num(a * b)}/{dev_num(a + b)} = {dev_num(t)} दिन लाग्छ।')

# ---------------- 17. Area / perimeter ----------------
for L in [6, 8, 10, 12, 15, 20, 25, 30]:
    for W in [4, 5, 6, 8, 10, 12, 15]:
        area = L * W
        oe, on, a = num_opts(area, [area + L, area - L, 2 * (L + W), L * W + W])
        em.emit(EX, 'Maths & Numerical', 'Mensuration', 'easy', 2,
                f'Find the area of a rectangle {L} cm long and {W} cm wide.',
                f'लम्बाइ {dev_num(L)} सेमी र चौडाइ {dev_num(W)} सेमी भएको आयतको क्षेत्रफल कति हो?',
                [fmt(x) + ' sq cm' for x in oe], [dev_num(x) + ' वर्ग सेमी' for x in on], a,
                f'Area = length x breadth = {L} x {W} = {area} sq cm.',
                f'क्षेत्रफल = लम्बाइ × चौडाइ = {dev_num(L)} × {dev_num(W)} = {dev_num(area)} वर्ग सेमी।')
        per = 2 * (L + W)
        oe, on, a = num_opts(per, [per + 2, per - 2, L + W, area])
        em.emit(EX, 'Maths & Numerical', 'Mensuration', 'easy', 1,
                f'Find the perimeter of a rectangle {L} cm long and {W} cm wide.',
                f'लम्बाइ {dev_num(L)} सेमी र चौडाइ {dev_num(W)} सेमी भएको आयतको परिमिति कति हो?',
                [fmt(x) + ' cm' for x in oe], [dev_num(x) + ' सेमी' for x in on], a,
                f'Perimeter = 2 x (length + breadth) = 2 x ({L} + {W}) = {per} cm.',
                f'परिमिति = २ × (लम्बाइ + चौडाइ) = २ × ({dev_num(L)} + {dev_num(W)}) = {dev_num(per)} सेमी।')
for r in [7, 14, 21, 28, 35]:
    area = 22 * r * r // 7
    oe, on, a = num_opts(area, [area + 22, area - 22, 2 * 22 * r // 7, area + r])
    em.emit(EXH, 'Maths & Numerical', 'Mensuration', 'medium', 2,
            f'Find the area of a circle of radius {r} cm. (Use pi = 22/7)',
            f'अर्धव्यास {dev_num(r)} सेमी भएको वृत्तको क्षेत्रफल कति हो? (π = २२/७ लिनुहोस्)',
            [fmt(x) + ' sq cm' for x in oe], [dev_num(x) + ' वर्ग सेमी' for x in on], a,
            f'Area = pi x r^2 = 22/7 x {r} x {r} = {area} sq cm.',
            f'क्षेत्रफल = π × r² = २२/७ × {dev_num(r)} × {dev_num(r)} = {dev_num(area)} वर्ग सेमी।')

# ---------------- 18. Trains ----------------
for L in [120, 150, 180, 200, 240, 300]:
    for v in [36, 54, 72, 90]:
        # v km/h -> m/s = v*5/18; time = L / (v*5/18)
        t = Fraction(L * 18, v * 5)
        if t.denominator != 1:
            continue
        t = int(t)
        oe, on, ai = num_opts(t, [t + 2, t - 2, t + 5, L // 10])
        em.emit(EXH, 'Maths & Numerical', 'Trains', 'hard', 2,
                f'A train {L} m long runs at {v} km/h. How long will it take to cross a pole?',
                f'{dev_num(L)} मिटर लामो रेल {dev_num(v)} किमी/घण्टाको गतिमा चल्छ। खम्बा पार गर्न कति समय लाग्छ?',
                [fmt(x) + ' seconds' for x in oe], [dev_num(x) + ' सेकेन्ड' for x in on], ai,
                f'Speed = {v} x 5/18 = {v * 5 // 18} m/s. Time = {L}/{v * 5 // 18} = {t} seconds.',
                f'गति = {dev_num(v)} × ५/१८ = {dev_num(v * 5 // 18)} मी/से। समय = {dev_num(L)}/{dev_num(v * 5 // 18)} = {dev_num(t)} सेकेन्ड।')

# ---------------- 19. Discount ----------------
for mp in [200, 400, 500, 600, 800, 1000, 1200, 1500, 2000]:
    for d in [5, 10, 15, 20, 25, 30, 40, 50]:
        sp = mp * (100 - d) // 100
        if mp * (100 - d) % 100:
            continue
        oe, on, a = rs_opts(sp, [mp, sp + 50, sp - 50, mp - d])
        em.emit(EX, 'Maths & Numerical', 'Profit & Loss', 'easy', 2,
                f'The marked price of an article is Rs {mp}. It is sold at a discount of {d}%. What is the selling price?',
                f'एउटा सामानको अङ्कित मूल्य रु {dev_num(mp)} छ। {dev(fmt(d))}% छुटमा बेच्दा बिक्री मूल्य कति हुन्छ?',
                oe, on, a,
                f'Discount = {d}% of Rs {mp} = Rs {mp - sp}. Selling price = {mp} - {mp - sp} = Rs {sp}.',
                f'छुट = रु {dev_num(mp)} को {dev(fmt(d))}% = रु {dev_num(mp - sp)}। बिक्री मूल्य = {dev_num(mp)} − {dev_num(mp - sp)} = रु {dev_num(sp)}।')

# ---------------- 20. Number series ----------------
def series_q(kind, seq, nxt, expl_en, expl_ne):
    s = ', '.join(str(x) for x in seq) + ', ?'
    sn = ', '.join(dev_num(x) for x in seq) + ', ?'
    oe, on, a = num_opts(nxt, [nxt + 1, nxt - 1, nxt + 5, nxt * 2 if nxt else nxt + 10])
    em.emit(EXH, 'IQ & Reasoning', 'Number Series', 'hard', 2,
            f'Find the next number in the series: {s}',
            f'तलको श्रृङ्खलाको अर्को सङ्ख्या कुन हो? {sn}',
            oe, on, a, expl_en, expl_ne)

for _ in range(260):
    start = rng.randint(2, 30)
    step = rng.randint(2, 12)
    seq = [start + i * step for i in range(5)]
    nxt = start + 5 * step
    series_q('arith', seq, nxt,
             f'Each term increases by {step}: {seq[-1]} + {step} = {nxt}.',
             f'प्रत्येक पद {dev_num(step)} ले बढ्छ: {dev_num(seq[-1])} + {dev_num(step)} = {dev_num(nxt)}।')
for _ in range(120):
    start = rng.randint(2, 9)
    ratio = rng.choice([2, 3])
    seq = [start * ratio ** i for i in range(5)]
    if seq[-1] > 5000:
        continue
    nxt = start * ratio ** 5
    series_q('geo', seq, nxt,
             f'Each term is multiplied by {ratio}: {seq[-1]} x {ratio} = {nxt}.',
             f'प्रत्येक पद {dev_num(ratio)} ले गुणन हुन्छ: {dev_num(seq[-1])} × {dev_num(ratio)} = {dev_num(nxt)}।')
for _ in range(120):
    start = rng.randint(2, 12)
    seq = [(start + i) ** 2 for i in range(5)]
    nxt = (start + 5) ** 2
    series_q('sq', seq, nxt,
             f'The terms are squares: {start}^2, {start + 1}^2, ..., {start + 4}^2. Next is {start + 5}^2 = {nxt}.',
             f'यी पदहरू वर्ग हुन्: {dev(start)}², {dev(start + 1)}², ..., {dev(start + 4)}²। अर्को {dev(start + 5)}² = {dev_num(nxt)} हो।')
for _ in range(80):
    start = rng.randint(2, 7)
    seq = [(start + i) ** 3 for i in range(4)]
    nxt = (start + 4) ** 3
    series_q('cube', seq, nxt,
             f'The terms are cubes: {start}^3, {start + 1}^3, ..., {start + 3}^3. Next is {start + 4}^3 = {nxt}.',
             f'यी पदहरू घन हुन्: {dev(start)}³, {dev(start + 1)}³, ..., {dev(start + 3)}³। अर्को {dev(start + 4)}³ = {dev_num(nxt)} हो।')
# primes
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
for i in range(0, 14):
    seq = primes[i:i + 5]
    nxt = primes[i + 5]
    series_q('prime', seq, nxt,
             f'The terms are consecutive prime numbers. After {seq[-1]} comes {nxt}.',
             f'यी पदहरू क्रमागत अभाज्य सङ्ख्या हुन्। {dev_num(seq[-1])} पछि {dev_num(nxt)} आउँछ।')
# increasing differences
for _ in range(100):
    start = rng.randint(1, 15)
    d0 = rng.randint(1, 4)
    inc = rng.randint(1, 3)
    seq = [start]
    d = d0
    for _ in range(4):
        seq.append(seq[-1] + d)
        d += inc
    nxt = seq[-1] + d
    series_q('diff', seq, nxt,
             f'Differences increase by {inc} each time ({d0}, {d0 + inc}, ...). The next difference is {d}, so {seq[-1]} + {d} = {nxt}.',
             f'अन्तर हरेक पटक {dev_num(inc)} ले बढ्छ ({dev_num(d0)}, {dev_num(d0 + inc)}, ...)। अर्को अन्तर {dev_num(d)} हो, त्यसैले {dev_num(seq[-1])} + {dev_num(d)} = {dev_num(nxt)}।')

# ---------------- 21. Unit digit of powers ----------------
for base in range(2, 10):
    for exp in range(2, 31):
        cyc = []
        v = 1
        for _ in range(4):
            v = v * base % 10
            cyc.append(v)
        unit = cyc[(exp - 1) % 4]
        oe, on, a = num_opts(unit, [x for x in range(10) if x != unit][:3] if unit not in range(10) else [u for u in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] if u != unit])
        # pick 3 distractors deterministically
        ds = [u for u in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] if u != unit]
        rng.shuffle(ds)
        oe, on, a = num_opts(unit, ds[:3])
        em.emit(EXH, 'Maths & Numerical', 'Number System', 'hard', 2,
                f'What is the unit digit of {base}^{exp}?',
                f'{dev_num(base)}^{dev_num(exp)} को एकाइ अङ्क कति हो?',
                oe, on, a,
                f'The unit digits of powers of {base} repeat every 4: {", ".join(str(x) for x in cyc)}. {exp} mod 4 = {exp % 4}, so the unit digit is {unit}.',
                f'{dev_num(base)} का घातहरूको एकाइ अङ्क हरेक ४ मा दोहोरिन्छ: {", ".join(dev_num(x) for x in cyc)}। {dev_num(exp)} mod ४ = {dev_num(exp % 4)} भएकाले एकाइ अङ्क {dev_num(unit)} हो।')

# ---------------- 22. Calendar: day of the week ----------------
WD_EN = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
WD_NE = ['सोमबार', 'मंगलबार', 'बुधबार', 'बिहीबार', 'शुक्रबार', 'शनिबार', 'आइतबार']
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
MONTHS_NE = ['जनवरी', 'फेब्रुअरी', 'मार्च', 'अप्रिल', 'मे', 'जुन', 'जुलाई', 'अगस्ट', 'सेप्टेम्बर', 'अक्टोबर', 'नोभेम्बर', 'डिसेम्बर']
seen_dates = set()
for _ in range(240):
    y = rng.randint(2024, 2031)
    m = rng.randint(1, 12)
    d = rng.randint(1, 28)
    if (y, m, d) in seen_dates:
        continue
    seen_dates.add((y, m, d))
    wd = datetime.date(y, m, d).weekday()
    others = [x for x in range(7) if x != wd]
    rng.shuffle(others)
    dist = others[:3]
    opts_en = [WD_EN[wd]] + [WD_EN[x] for x in dist]
    opts_ne = [WD_NE[wd]] + [WD_NE[x] for x in dist]
    em.emit(EX, 'IQ & Reasoning', 'Calendar', 'medium', 2,
            f'What day of the week was {d} {MONTHS[m - 1]} {y}?',
            f'{dev_num(d)} {MONTHS_NE[m - 1]} {dev_num(y)} कुन बार थियो?',
            opts_en, opts_ne, 0,
            f'{d} {MONTHS[m - 1]} {y} was a {WD_EN[wd]}.',
            f'{dev_num(d)} {MONTHS_NE[m - 1]} {dev_num(y)} {WD_NE[wd]} थियो।')

# ---------------- 23. Clock angles ----------------
for h in range(1, 13):
    for m in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]:
        if h == 12 and m == 0:
            continue
        ang = abs(30 * h - 5.5 * m)
        if ang > 180:
            ang = 360 - ang
        if ang != int(ang):
            continue
        ang = int(ang)
        oe, on, a = num_opts(ang, [360 - ang if 360 - ang != ang else ang + 30, ang + 15, ang - 15 if ang > 15 else ang + 45])
        em.emit(EXH, 'IQ & Reasoning', 'Clock', 'hard', 2,
                f'What is the angle between the hands of a clock at {h}:{m:02d}?',
                f'घडीमा {dev_num(h)}:{dev(f"{m:02d}")} बजे सुईहरूबीचको कोण कति हुन्छ?',
                [fmt(x) + ' degrees' for x in oe], [dev_num(x) + ' डिग्री' for x in on], a,
                f'Angle = |30 x {h} - 5.5 x {m}| = {abs(30 * h - 5.5 * m)} degrees; the smaller angle is {ang} degrees.',
                f'कोण = |३० × {dev_num(h)} − ५.५ × {dev_num(m)}| = {dev_num(int(abs(30 * h - 5.5 * m)))} डिग्री; सानो कोण {dev_num(ang)} डिग्री हो।')

# ---------------- 24. Remainder / divisibility ----------------
for _ in range(160):
    a = rng.randint(50, 500)
    b = rng.randint(6, 40)
    r = a % b
    q = a // b
    oe, on, ai = num_opts(r, [r + 1, r - 1 if r > 0 else r + 2, b - r if b - r != r else r + 3, q])
    em.emit(EX, 'Maths & Numerical', 'Number System', 'medium', 1,
            f'What is the remainder when {a} is divided by {b}?',
            f'{dev_num(a)} लाई {dev_num(b)} ले भाग गर्दा शेष कति हुन्छ?',
            oe, on, ai,
            f'{a} = {b} x {q} + {r}, so the remainder is {r}.',
            f'{dev_num(a)} = {dev_num(b)} × {dev_num(q)} + {dev_num(r)} भएकाले शेष {dev_num(r)} हो।')

# ---------------- 25. Probability (dice / coins) ----------------
for n in [1, 2, 3]:
    for total in range(1, 7):
        pass
# dice: P(sum = s) with two dice
from fractions import Fraction as F
for s in range(2, 13):
    ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s)
    p = F(ways, 36)
    correct = f'{p.numerator}/{p.denominator}'
    distract = [f'{w}/36' for w in [ways + 1, ways - 1, 36 - ways] if 0 < w < 36]
    distract = [d for d in distract if d != correct]
    while len(distract) < 3:
        distract.append(f'{rng.randint(1, 11)}/36')
    opts_en = [correct] + distract[:3]
    opts_ne = opts_en[:]
    em.emit(EXH, 'Maths & Numerical', 'Probability', 'hard', 2,
            f'Two dice are thrown. What is the probability that the sum is {s}?',
            f'दुईवटा गोटी फाल्दा योगफल {dev_num(s)} आउने सम्भावना कति हो?',
            opts_en, opts_ne, 0,
            f'There are {ways} favourable outcomes out of 36, so the probability is {ways}/36 = {correct}.',
            f'३६ सम्भावनामध्ये {dev_num(ways)} वटा अनुकूल छन्, त्यसैले सम्भावना {dev_num(ways)}/३६ = {correct} हो।')

n = em.write('expansion-r10-maths.json')
print('MATHS TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:10]:
    print('  REJ', r)
