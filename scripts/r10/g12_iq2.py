#!/usr/bin/env python3
"""R10 generator 12: more IQ & Reasoning (~2,500). Letter series variants,
mixed number-letter series, coding (Caesar shifts), odd-one-out words,
word formation/anagrams, mirror & water images, 3-step blood relations,
3-step directions, ranking, seating, syllogisms, alphabet positions."""
import sys, random
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
em = Emitter(bank, 'R10-IQ2')
rng = random.Random(71105)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'police', 'army', 'tsc-primary', 'tsc-secondary']
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHA_NE = ['ए','बी','सी','डी','ई','एफ','जी','एच','आई','जे','के','एल','एम','एन','ओ','पी','क्यू','आर','एस','टी','यू','भी','डब्ल्यू','एक्स','वाई','जेड']

def letter_opts(correct):
    ds = [c for c in ALPHA if c != correct]
    rng.shuffle(ds)
    o = [correct] + ds[:3]
    on = [ALPHA_NE[ALPHA.index(c)] for c in o]
    return o, on

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

def E(sub, diff, q, qn, o, on, expl, expln, idx=0):
    em.emit(EX, 'IQ & Reasoning', sub, diff, 2, q, qn, o, on, idx, expl, expln)

# ---------- letter series: increasing differences ----------
for start in range(0, 20):
    diff = rng.choice([1, 2, 3])
    seq = [ALPHA[start]]
    d = diff
    for _ in range(3):
        seq.append(ALPHA[(ALPHA.index(seq[-1]) + d) % 26])
        d += 1
    nxt = ALPHA[(ALPHA.index(seq[-1]) + d) % 26]
    s = ', '.join(seq)
    o, on = letter_opts(nxt)
    E('Letter Series', 'hard', f'What is the next letter in the series: {s}, ...?',
      f'श्रेणी {s}, ... मा अर्को अक्षर कुन हो?', o, on,
      f'The differences increase by 1 each time, so the next letter is {nxt}.',
      f'अन्तरहरू प्रत्येक पटक १ ले बढ्छन्, त्यसैले अर्को अक्षर {nxt} हो।')

# ---------- letter series: skip-2 / skip-3 ----------
for start in range(0, 10):
    for step in (2, 3, 4):
        seq = [ALPHA[(start + i*step) % 26] for i in range(4)]
        nxt = ALPHA[(start + 4*step) % 26]
        s = ', '.join(seq)
        o, on = letter_opts(nxt)
        E('Letter Series', 'medium', f'What is the next letter in the series: {s}, ...?',
          f'श्रेणी {s}, ... मा अर्को अक्षर कुन हो?', o, on,
          f'Each letter is {step} places after the previous one, so the next letter is {nxt}.',
          f'प्रत्येक अक्षर अघिल्लोभन्दा {dev(step)} स्थान पछि छ, त्यसैले अर्को अक्षर {nxt} हो।')

# ---------- mixed number-letter series ----------
for start in range(0, 10):
    # letters step 1, numbers double
    seq = []
    for i in range(4):
        seq.append(f'{ALPHA[(start+i) % 26]}{2**i}')
    nxt = f'{ALPHA[(start+4) % 26]}{2**4}'
    s = ', '.join(seq)
    ds = [f'{ALPHA[(start+4) % 26]}{x}' for x in (8, 32, 4)]
    o = [nxt] + ds
    on = o[:]
    E('Mixed Series', 'hard', f'What is the next term in the series: {s}, ...?',
      f'श्रेणी {s}, ... मा अर्को पद कुन हो?', o, on,
      f'The letters advance by 1 and the numbers double, so the next term is {nxt}.',
      f'अक्षरहरू १ ले अगाडि बढ्छन् र सङ्ख्याहरू दोब्बर हुन्छन्, त्यसैले अर्को पद {nxt} हो।')
    # letters step 2, numbers +3
    seq = []
    for i in range(4):
        seq.append(f'{ALPHA[(start+2*i) % 26]}{3+3*i}')
    nxt = f'{ALPHA[(start+8) % 26]}{15}'
    s = ', '.join(seq)
    ds = [f'{ALPHA[(start+8) % 26]}{x}' for x in (12, 18, 9)]
    o = [nxt] + ds
    on = o[:]
    E('Mixed Series', 'hard', f'What is the next term in the series: {s}, ...?',
      f'श्रेणी {s}, ... मा अर्को पद कुन हो?', o, on,
      f'The letters advance by 2 and the numbers increase by 3, so the next term is {nxt}.',
      f'अक्षरहरू २ ले अगाडि बढ्छन् र सङ्ख्याहरू ३ ले बढ्छन्, त्यसैले अर्को पद {nxt} हो।')

# ---------- coding: Caesar shifts ----------
WORDS = ['NEPAL','KATHMANDU','POKHARA','BIRATNAGAR','LUMBINI','JANAKPUR','DHARAN','BUTWAL',
         'SCHOOL','TEACHER','STUDENT','BOOK','PEN','TABLE','CHAIR','HOUSE','WATER','RIVER',
         'MOUNTAIN','FOREST','ANIMAL','TIGER','ELEPHANT','MONKEY','BIRD','FISH','FLOWER',
         'GARDEN','MARKET','BRIDGE','ROAD','TRAIN','PLANE','MOBILE','COMPUTER','KEYBOARD',
         'FRIEND','FAMILY','MOTHER','FATHER','SISTER','BROTHER','UNCLE','AUNT','KING','QUEEN',
         'DOCTOR','NURSE','POLICE','SOLDIER','FARMER','DRIVER','COOK','SINGER','DANCER','WRITER',
         'HAPPY','BRAVE','HONEST','KIND','STRONG','QUICK','BRIGHT','GENTLE','SIMPLE','NOBLE',
         'APPLE','MANGO','BANANA','ORANGE','GRAPE','LEMON','POTATO','TOMATO','ONION','GARLIC',
         'SUMMER','WINTER','SPRING','AUTUMN','MORNING','EVENING','NIGHT','TODAY','MONDAY','FRIDAY',
         'GOLD','SILVER','IRON','COPPER','STONE','SAND','FIRE','EARTH','WIND','RAIN','SNOW','CLOUD',
         'MUSIC','SONG','DANCE','STORY','POEM','NOVEL','FILM','GAME','SPORT','CRICKET','FOOTBALL',
         'HEALTH','WEALTH','POWER','PEACE','TRUTH','LIGHT','DARK','DREAM','HOPE','FAITH','LOVE','LIFE']
def caesar(w, s):
    return ''.join(ALPHA[(ALPHA.index(c)+s) % 26] for c in w)
for w in WORDS:
    for s in (1, 2, 3):
        code = caesar(w, s)
        # decode framing: given w1 -> c1 with shift s, decode c2 = code of another word
        w2 = rng.choice([x for x in WORDS if x != w])
        c2 = caesar(w2, s)
        ds = rng.sample([x for x in WORDS if x not in (w, w2)], 3)
        o = [w2] + ds
        on = o[:]
        E('Coding', 'medium', f'In a certain code, {w} is written as {code}. Which word is written as {c2} in the same code?',
          f'एउटा कोडमा {w} लाई {code} लेखिन्छ। त्यही कोडमा {c2} भनेर कुन शब्द लेखिन्छ?', o, on,
          f'Each letter is shifted forward by {s}, so {c2} stands for {w2}.',
          f'प्रत्येक अक्षर {dev(s)} ले अगाडि सारिन्छ, त्यसैले {c2} भनेको {w2} हो।')
# coding: apply same shift to a new word
for _ in range(150):
    w1, w2 = rng.sample(WORDS, 2)
    s = rng.choice([1, 2, 3, 4])
    c1, c2 = caesar(w1, s), caesar(w2, s)
    ds = [caesar(w2, s+1), caesar(w2, s-1), caesar(w2, s+2)]
    o = [c2] + ds
    on = o[:]
    E('Coding', 'hard', f'If {w1} is coded as {c1}, what is the code for {w2}?',
      f'यदि {w1} लाई {c1} भनेर कोड गरिन्छ भने {w2} को कोड के हो?', o, on,
      f'Each letter is shifted forward by {s}, so {w2} becomes {c2}.',
      f'प्रत्येक अक्षर {dev(s)} ले अगाडि सारिन्छ, त्यसैले {w2} {c2} हुन्छ।')
# coding: reverse (decode framing)
for w in WORDS[:60]:
    code = w[::-1]
    w2 = rng.choice([x for x in WORDS if x != w])
    c2 = w2[::-1]
    ds = rng.sample([x for x in WORDS if x not in (w, w2)], 3)
    o = [w2] + ds
    on = o[:]
    E('Coding', 'medium', f'In a certain code, {w} is written as {code}. Which word is written as {c2} in the same code?',
      f'एउटा कोडमा {w} लाई {code} लेखिन्छ। त्यही कोडमा {c2} भनेर कुन शब्द लेखिन्छ?', o, on,
      f'The letters are reversed, so {c2} stands for {w2}.',
      f'अक्षरहरू उल्टाइन्छन्, त्यसैले {c2} भनेको {w2} हो।')

# ---------- odd one out: words ----------
CATS = [
    ('Apple', 'Mango', 'Banana', 'Potato', 'fruits', 'फलफूल'),
    ('Tiger', 'Lion', 'Elephant', 'Eagle', 'animals', 'जनावर'),
    ('Red', 'Blue', 'Green', 'Circle', 'colours', 'रङ'),
    ('Car', 'Bus', 'Train', 'Chair', 'vehicles', 'सवारी साधन'),
    ('Doctor', 'Teacher', 'Farmer', 'Hospital', 'professions', 'पेशा'),
    ('January', 'February', 'March', 'Monday', 'months', 'महिना'),
    ('Monday', 'Tuesday', 'Wednesday', 'January', 'days', 'बार'),
    ('Guitar', 'Piano', 'Violin', 'Football', 'musical instruments', 'वाद्ययन्त्र'),
    ('Nepal', 'India', 'China', 'Kathmandu', 'countries', 'देश'),
    ('Gold', 'Silver', 'Iron', 'Wood', 'metals', 'धातु'),
    ('Rose', 'Lotus', 'Sunflower', 'Mango', 'flowers', 'फूल'),
    ('Pen', 'Pencil', 'Eraser', 'Book', 'writing tools', 'लेखन सामग्री'),
    ('Hand', 'Leg', 'Eye', 'Shirt', 'body parts', 'शरीरका अङ्ग'),
    ('Rice', 'Wheat', 'Maize', 'Milk', 'grains', 'अन्न'),
    ('Cricket', 'Football', 'Hockey', 'Chess', 'outdoor games', 'बाहिरी खेल'),
    ('Dog', 'Cat', 'Cow', 'Snake', 'domestic animals', 'घरपालुवा जनावर'),
    ('Book', 'Novel', 'Poem', 'Pen', 'reading material', 'पठन सामग्री'),
    ('Sun', 'Moon', 'Star', 'Earth', 'celestial bodies', 'खगोलीय पिण्ड'),
    ('Summer', 'Winter', 'Spring', 'Rain', 'seasons', 'ऋतु'),
    ('Hammer', 'Saw', 'Drill', 'Nail', 'tools', 'औजार'),
]
CATS_NE = {'Apple':'स्याउ','Mango':'आँप','Banana':'केरा','Potato':'आलु','Tiger':'बाघ','Lion':'सिंह','Elephant':'हात्ती','Eagle':'चील',
           'Red':'रातो','Blue':'निलो','Green':'हरियो','Circle':'वृत्त','Car':'कार','Bus':'बस','Train':'रेल','Chair':'कुर्सी',
           'Doctor':'डाक्टर','Teacher':'शिक्षक','Farmer':'किसान','Hospital':'अस्पताल','January':'जनवरी','February':'फेब्रुअरी',
           'March':'मार्च','Monday':'सोमबार','Tuesday':'मङ्गलबार','Wednesday':'बुधबार','Guitar':'गितार','Piano':'पियानो',
           'Violin':'भायोलिन','Football':'फुटबल','Nepal':'नेपाल','India':'भारत','China':'चीन','Kathmandu':'काठमाडौँ',
           'Gold':'सुन','Silver':'चाँदी','Iron':'फलाम','Wood':'काठ','Rose':'गुलाफ','Lotus':'कमल','Sunflower':'सूर्यमुखी',
           'Pen':'कलम','Pencil':'पेन्सिल','Eraser':'इरेजर','Book':'किताब','Hand':'हात','Leg':'खुट्टा','Eye':'आँखा','Shirt':'सर्ट',
           'Rice':'धान','Wheat':'गहुँ','Maize':'मकै','Milk':'दूध','Cricket':'क्रिकेट','Hockey':'हकी','Chess':'चेस',
           'Dog':'कुकुर','Cat':'बिरालो','Cow':'गाई','Snake':'सर्प','Novel':'उपन्यास','Poem':'कविता','Sun':'सूर्य','Moon':'चन्द्रमा',
           'Star':'तारा','Earth':'पृथ्वी','Summer':'गर्मी','Winter':'जाडो','Spring':'वसन्त','Rain':'वर्षा','Hammer':'हथौडा',
           'Saw':'आरा','Drill':'ड्रिल','Nail':'किला'}
for a, b, c, odd, cat, cat_ne in CATS:
    o = [a, b, c, odd]
    rng.shuffle(o)
    on = [CATS_NE[x] for x in o]
    idx = o.index(odd)
    E('Odd One Out', 'easy', f'Which is the odd one out: {a}, {b}, {c}, {odd}?',
      f'निम्नमध्ये फरक कुन हो: {CATS_NE[a]}, {CATS_NE[b]}, {CATS_NE[c]}, {CATS_NE[odd]}?', o, on,
      f'{odd} is the odd one out; the others are {cat}.', f'{CATS_NE[odd]} फरक हो; अरू {cat_ne} हुन्।', idx=idx)
    # reverse framing: which belongs
    o2 = [odd, a, b, c]
    rng.shuffle(o2)
    on2 = [CATS_NE[x] for x in o2]
    idx2 = o2.index(odd)
    E('Odd One Out', 'easy', f'Which one does NOT belong to the group of {cat}?',
      f'कुन {cat_ne} को समूहमा पर्दैन?', o2, on2,
      f'{odd} does not belong; the others are {cat}.', f'{CATS_NE[odd]} पर्दैन; अरू {cat_ne} हुन्।', idx=idx2)

# ---------- anagrams / word formation ----------
ANAGRAMS = [('LISTEN','SILENT'), ('EARTH','HEART'), ('ACT','CAT'), ('TEA','EAT'), ('STOP','TOPS'),
            ('POST','SPOT'), ('CARE','RACE'), ('LIVE','EVIL'), ('DOG','GOD'), ('NIGHT','THING'),
            ('ANGEL','GLEAN'), ('MALE','MEAL'), ('LATE','TALE'), ('RATE','TEAR'), ('STAR','RATS'),
            ('PEAR','REAP'), ('BEAR','BARE'), ('DEAR','READ'), ('FEAR','FARE'), ('NEAR','EARN'),
            ('LEAD','DEAL'), ('ROSE','SORE'), ('LOSE','SOLE'), ('NOTE','TONE'), ('STONE','TONES'),
            ('MATE','MEAT'), ('TEAM','MEAT'), ('LION','LOIN'), ('PAST','PATS'), ('TRAP','PART'),
            ('PALE','LEAP'), ('PLEA','LEAP'), ('DIAL','LAID'), ('FIRE','RIFE'), ('TIER','RITE'),
            ('TIRED','TRIED'), ('DIRE','RIDE'), ('SIDE','DIES'), ('TIDE','DIET'), ('EDIT','DIET'),
            ('TIME','MITE'), ('ITEM','MITE'), ('EMIT','MITE'), ('SITE','TIES'), ('FIST','FITS'),
            ('SIFT','FIST'), ('LIST','SILT'), ('SLIT','LIST'), ('COAT','TACO'), ('ROPE','PORE'),
            ('STOP','POST'), ('SPOT','TOPS'), ('MEAL','LAME'), ('TALE','LATE'), ('TEAR','RATE'),
            ('RATS','STAR'), ('REAP','PEAR'), ('BARE','BEAR'), ('READ','DEAR'), ('FARE','FEAR'),
            ('EARN','NEAR'), ('DEAL','LEAD'), ('SORE','ROSE'), ('SOLE','LOSE'), ('TONE','NOTE'),
            ('TONES','STONE'), ('MEAT','MATE'), ('LOIN','LION'), ('PATS','PAST'), ('PART','TRAP'),
            ('LEAP','PALE'), ('LAID','DIAL'), ('RIFE','FIRE'), ('RITE','TIER'), ('TRIED','TIRED'),
            ('RIDE','DIRE'), ('DIES','SIDE'), ('DIET','TIDE'), ('MITE','TIME'), ('TIES','SITE'),
            ('FITS','FIST'), ('SILT','LIST'), ('TACO','COAT'), ('PORE','ROPE')]
seen_pairs = set()
for w1, w2 in ANAGRAMS:
    key = tuple(sorted([w1, w2]))
    if key in seen_pairs: continue
    seen_pairs.add(key)
    # framing 1: which word can be formed from the letters of w1?
    # distractors are non-words (reversals/rotations), so w2 is the only real word
    ds = [w2[::-1], w1[1:] + w1[0], w2[:-1] + w2[0]]
    ds = [x for x in ds if x != w2 and x != w1][:3]
    if len(ds) < 3: continue
    o = [w2] + ds
    on = o[:]
    E('Word Formation', 'medium', f'Which word can be formed using all the letters of "{w1}"?',
      f'"{w1}" का सबै अक्षर प्रयोग गरेर कुन शब्द बनाउन सकिन्छ?', o, on,
      f'"{w2}" uses exactly the letters of "{w1}".', f'"{w2}" मा "{w1}" का ठ्याक्कै अक्षरहरू प्रयोग भएका छन्।')
    # framing 2: unscramble (distractors are non-words, never w1)
    scr = list(w2)
    rng.shuffle(scr)
    scr_s = ''.join(scr)
    if scr_s in (w2, w1):
        scr_s = w2[1:] + w2[0]
    ds2 = [w2[::-1], w2[1:] + w2[0], scr_s]
    ds2 = [x for x in ds2 if x != w2][:3]
    if len(ds2) < 3: continue
    o2 = [w2] + ds2
    on2 = o2[:]
    E('Word Formation', 'medium', f'Unscramble the letters "{scr_s}" to form a meaningful word.',
      f'"{scr_s}" अक्षरहरूलाई मिलाएर अर्थपूर्ण शब्द बनाउनुहोस्।', o2, on2,
      f'The letters rearrange to "{w2}".', f'अक्षरहरू मिलाएर "{w2}" बन्छ।')

# ---------- mirror / water images ----------
MIRROR_SAME = ['H', 'I', 'O', 'X']
WATER_SAME = ['B', 'C', 'D', 'E', 'H', 'I', 'K', 'O', 'X']
for _ in range(30):
    c = rng.choice(MIRROR_SAME)
    ds = rng.sample([x for x in ALPHA if x not in MIRROR_SAME], 3)
    o = [c] + ds
    rng.shuffle(o)
    on = [ALPHA_NE[ALPHA.index(x)] for x in o]
    idx = o.index(c)
    E('Mirror & Water Images', 'medium', 'Which letter looks the same in a mirror?',
      'ऐनामा कुन अक्षर उस्तै देखिन्छ?', o, on,
      f'{c} is symmetrical in a mirror. The answer is {c}.', f'{c} ऐनामा सममित हुन्छ। उत्तर {c} हो।', idx=idx)
for _ in range(30):
    c = rng.choice(WATER_SAME)
    ds = rng.sample([x for x in ALPHA if x not in WATER_SAME], 3)
    o = [c] + ds
    rng.shuffle(o)
    on = [ALPHA_NE[ALPHA.index(x)] for x in o]
    idx = o.index(c)
    E('Mirror & Water Images', 'medium', 'Which letter looks the same in its water image?',
      'पानीमा बनेको प्रतिबिम्बमा कुन अक्षर उस्तै देखिन्छ?', o, on,
      f'{c} looks the same in its water image. The answer is {c}.', f'{c} पानीको प्रतिबिम्बमा उस्तै देखिन्छ। उत्तर {c} हो।', idx=idx)

# ---------- 3-step blood relations ----------
REL = [
    ('A is the father of B. B is the mother of C. How is A related to C?', 'A, B का बुबा हुन्। B, C की आमा हुन्। A, C का के हुन्?', 'Maternal grandfather', 'मावली हजुरबुबा', 'Paternal grandfather', 'पितृ हजुरबुबा', 'Father', 'बुबा', 'Uncle', 'काका'),
    ('A is the mother of B. B is the father of C. How is A related to C?', 'A, B की आमा हुन्। B, C का बुबा हुन्। A, C की के हुन्?', 'Paternal grandmother', 'पितृ हजुरआमा', 'Maternal grandmother', 'मावली हजुरआमा', 'Mother', 'आमा', 'Aunt', 'फुपू'),
    ('A is the brother of B. B is the sister of C. How is A related to C?', 'A, B का दाजु हुन्। B, C की दिदी हुन्। A, C का के हुन्?', 'Brother', 'दाजु/भाइ', 'Sister', 'दिदी/बहिनी', 'Father', 'बुबा', 'Uncle', 'काका'),
    ('A is the son of B. B is the brother of C. How is A related to C?', 'A, B का छोरा हुन्। B, C का भाइ हुन्। A, C का के हुन्?', 'Nephew', 'भतिजा/भान्जा', 'Son', 'छोरा', 'Brother', 'भाइ', 'Grandson', 'नाति'),
    ('A is the daughter of B. B is the sister of C. How is A related to C?', 'A, B की छोरी हुन्। B, C की बहिनी हुन्। A, C की के हुन्?', 'Niece', 'भतिजी/भान्जी', 'Daughter', 'छोरी', 'Sister', 'बहिनी', 'Granddaughter', 'नातिनी'),
    ('A is the husband of B. B is the mother of C. How is A related to C?', 'A, B का श्रीमान् हुन्। B, C की आमा हुन्। A, C का के हुन्?', 'Father', 'बुबा', 'Uncle', 'काका', 'Grandfather', 'हजुरबुबा', 'Brother', 'दाजु'),
    ('A is the wife of B. B is the son of C. How is A related to C?', 'A, B की श्रीमती हुन्। B, C का छोरा हुन्। A, C की के हुन्?', 'Daughter-in-law', 'बुहारी', 'Daughter', 'छोरी', 'Sister', 'बहिनी', 'Niece', 'भतिजी'),
    ('A is the father of B. B is the brother of C. How is A related to C?', 'A, B का बुबा हुन्। B, C का भाइ हुन्। A, C का के हुन्?', 'Father', 'बुबा', 'Uncle', 'काका', 'Grandfather', 'हजुरबुबा', 'Brother', 'दाजु'),
    ('A is the mother of B. B is the sister of C. How is A related to C?', 'A, B की आमा हुन्। B, C की दिदी हुन्। A, C की के हुन्?', 'Mother', 'आमा', 'Aunt', 'फुपू', 'Grandmother', 'हजुरआमा', 'Sister', 'दिदी'),
    ('A is the grandfather of B. B is the father of C. How is A related to C?', 'A, B का हजुरबुबा हुन्। B, C का बुबा हुन्। A, C का के हुन्?', 'Great-grandfather', 'जिजुबाजे', 'Grandfather', 'हजुरबुबा', 'Father', 'बुबा', 'Uncle', 'काका'),
]
for q, qn, a, an, d1, d1n, d2, d2n, d3, d3n in REL:
    E('Blood Relations', 'hard', q, qn, [a, d1, d2, d3], [an, d1n, d2n, d3n],
      f'The answer is {a}.', f'उत्तर {an} हो।')

# ---------- 3-step directions with distance ----------
for _ in range(90):
    d1 = rng.choice([3, 4, 5, 6, 8, 10])
    d2 = rng.choice([3, 4, 5, 6, 8, 10])
    d3 = rng.choice([3, 4, 5, 6, 8, 10])
    pattern = rng.choice(['N-E-S', 'N-W-S', 'S-E-N', 'S-W-N', 'E-N-W', 'E-S-W', 'W-N-E', 'W-S-E'])
    dirs = pattern.split('-')
    # net displacement: first and third are opposite, so net = second direction distance
    net_dir = {'N': 'north', 'S': 'south', 'E': 'east', 'W': 'west'}[dirs[1]]
    net_dir_ne = {'N': 'उत्तर', 'S': 'दक्षिण', 'E': 'पूर्व', 'W': 'पश्चिम'}[dirs[1]]
    dist = d2
    o, on, _ = num_opts(dist, [dist+2, dist-2, dist+5, dist-5])
    dir_full = {'N': 'north', 'S': 'south', 'E': 'east', 'W': 'west'}
    dir_ne = {'N': 'उत्तर', 'S': 'दक्षिण', 'E': 'पूर्व', 'W': 'पश्चिम'}
    E('Direction Sense', 'hard',
      f'A man walks {d1} km {dir_full[dirs[0]]}, then {d2} km {dir_full[dirs[1]]}, then {d3} km {dir_full[dirs[2]]}. How far is he from his starting point?',
      f'एक मानिस {dev(d1)} किमी {dir_ne[dirs[0]]} हिँड्छ, त्यसपछि {dev(d2)} किमी {dir_ne[dirs[1]]} हिँड्छ, त्यसपछि {dev(d3)} किमी {dir_ne[dirs[2]]} हिँड्छ। उनी सुरुको बिन्दुबाट कति टाढा छन्?',
      o, on,
      f'The {dir_full[dirs[0]]} and {dir_full[dirs[2]]} walks cancel out, leaving {d2} km {net_dir}. The answer is {dist} km.',
      f'{dir_ne[dirs[0]]} र {dir_ne[dirs[2]]} का हिँडाइहरू रद्द हुन्छन्, {dev(d2)} किमी {net_dir_ne} बाँकी रहन्छ। उत्तर {dev_num(dist)} किमी हो।')

# ---------- ranking with two people ----------
for _ in range(90):
    total = rng.choice([30, 40, 50, 60])
    left = rng.randint(5, total//2)
    right = rng.randint(5, total//2)
    between = total - left - right
    if between < 0: continue
    o, on, _ = num_opts(between, [between+2, between-2, between+5, between-5])
    E('Ranking', 'hard',
      f'In a row of {total} students, Ram is {ord_s(left)} from the left and Hari is {ord_s(right)} from the right. How many students are between them?',
      f'{dev(total)} विद्यार्थीको लाइनमा राम बायाँबाट {dev(left)}औँ र हरि दायाँबाट {dev(right)}औँ छन्। उनीहरूबीच कति विद्यार्थी छन्?',
      o, on,
      f'Students between them = {total} - {left} - {right} = {between}.',
      f'उनीहरूबीचका विद्यार्थी = {dev(total)} - {dev(left)} - {dev(right)} = {dev_num(between)}।')

# ---------- seating: position from other end ----------
for _ in range(60):
    total = rng.randint(7, 15)
    pos = rng.randint(2, total-1)
    other = total - pos + 1
    o, on, _ = num_opts(other, [other+1, other-1, other+2, other-2])
    E('Seating Arrangement', 'medium',
      f'A sits {ord_s(pos)} from the left in a row of {total} people. What is A\'s position from the right?',
      f'{dev(total)} जनाको लाइनमा A बायाँबाट {dev(pos)}औँ स्थानमा बस्छ। A दायाँबाट कुन स्थानमा छ?',
      o, on,
      f'Position from the right = {total} - {pos} + 1 = {other}.',
      f'दायाँबाट स्थान = {dev(total)} - {dev(pos)} + १ = {dev(other)}।')

# ---------- syllogisms ----------
SYL = [
    ('All cats are animals. All animals are living beings. Which conclusion follows?', 'सबै बिरालाहरू जनावर हुन्। सबै जनावरहरू जीवित प्राणी हुन्। कुन निष्कर्ष निस्कन्छ?', 'All cats are living beings', 'सबै बिरालाहरू जीवित प्राणी हुन्', 'Some cats are not living beings', 'केही बिरालाहरू जीवित प्राणी होइनन्', 'No cat is a living being', 'कुनै बिरालो जीवित प्राणी होइन', 'All living beings are cats', 'सबै जीवित प्राणी बिरालाहरू हुन्'),
    ('All roses are flowers. All flowers are plants. Which conclusion follows?', 'सबै गुलाफ फूल हुन्। सबै फूल बिरुवा हुन्। कुन निष्कर्ष निस्कन्छ?', 'All roses are plants', 'सबै गुलाफ बिरुवा हुन्', 'Some roses are not plants', 'केही गुलाफ बिरुवा होइनन्', 'No rose is a plant', 'कुनै गुलाफ बिरुवा होइन', 'All plants are roses', 'सबै बिरुवा गुलाफ हुन्'),
    ('All pens are books. All books are papers. Which conclusion follows?', 'सबै कलम किताब हुन्। सबै किताब कागज हुन्। कुन निष्कर्ष निस्कन्छ?', 'All pens are papers', 'सबै कलम कागज हुन्', 'Some pens are not papers', 'केही कलम कागज होइनन्', 'No pen is a paper', 'कुनै कलम कागज होइन', 'All papers are pens', 'सबै कागज कलम हुन्'),
    ('All dogs are mammals. All mammals are animals. Which conclusion follows?', 'सबै कुकुर स्तनधारी हुन्। सबै स्तनधारी जनावर हुन्। कुन निष्कर्ष निस्कन्छ?', 'All dogs are animals', 'सबै कुकुर जनावर हुन्', 'Some dogs are not animals', 'केही कुकुर जनावर होइनन्', 'No dog is an animal', 'कुनै कुकुर जनावर होइन', 'All animals are dogs', 'सबै जनावर कुकुर हुन्'),
    ('All students are learners. All learners are humans. Which conclusion follows?', 'सबै विद्यार्थी सिकारु हुन्। सबै सिकारु मानव हुन्। कुन निष्कर्ष निस्कन्छ?', 'All students are humans', 'सबै विद्यार्थी मानव हुन्', 'Some students are not humans', 'केही विद्यार्थी मानव होइनन्', 'No student is a human', 'कुनै विद्यार्थी मानव होइन', 'All humans are students', 'सबै मानव विद्यार्थी हुन्'),
    ('All squares are rectangles. All rectangles are quadrilaterals. Which conclusion follows?', 'सबै वर्ग आयत हुन्। सबै आयत चतुर्भुज हुन्। कुन निष्कर्ष निस्कन्छ?', 'All squares are quadrilaterals', 'सबै वर्ग चतुर्भुज हुन्', 'Some squares are not quadrilaterals', 'केही वर्ग चतुर्भुज होइनन्', 'No square is a quadrilateral', 'कुनै वर्ग चतुर्भुज होइन', 'All quadrilaterals are squares', 'सबै चतुर्भुज वर्ग हुन्'),
    ('All metals are elements. All elements are matter. Which conclusion follows?', 'सबै धातु तत्व हुन्। सबै तत्व पदार्थ हुन्। कुन निष्कर्ष निस्कन्छ?', 'All metals are matter', 'सबै धातु पदार्थ हुन्', 'Some metals are not matter', 'केही धातु पदार्थ होइनन्', 'No metal is matter', 'कुनै धातु पदार्थ होइन', 'All matter is metal', 'सबै पदार्थ धातु हुन्'),
    ('All birds are animals. All animals need food. Which conclusion follows?', 'सबै चरा जनावर हुन्। सबै जनावरलाई खाना चाहिन्छ। कुन निष्कर्ष निस्कन्छ?', 'All birds need food', 'सबै चरालाई खाना चाहिन्छ', 'Some birds do not need food', 'केही चरालाई खाना चाहिँदैन', 'No bird needs food', 'कुनै चरालाई खाना चाहिँदैन', 'All that need food are birds', 'खाना चाहिने सबै चरा हुन्'),
]
for q, qn, a, an, d1, d1n, d2, d2n, d3, d3n in SYL:
    E('Syllogism', 'hard', q, qn, [a, d1, d2, d3], [an, d1n, d2n, d3n],
      f'The conclusion that follows is: {a}.', f'निस्कने निष्कर्ष: {an}।')

# ---------- alphabet positions ----------
for _ in range(80):
    n = rng.randint(3, 20)
    m = rng.randint(2, 10)
    pos = n + m
    if pos > 26: continue
    c = ALPHA[pos-1]
    o, on = letter_opts(c)
    E('Alphabet Positions', 'medium',
      f'Which letter is {ord_s(m)} to the right of the {ord_s(n)} letter from the left in the English alphabet?',
      f'अङ्ग्रेजी वर्णमालामा बायाँबाट {dev(n)}औँ अक्षरको दायाँतर्फ {dev(m)}औँ अक्षर कुन हो?', o, on,
      f'The {ord_s(n)} letter from the left is {ALPHA[n-1]}; {m} places to its right is {c}.',
      f'बायाँबाट {dev(n)}औँ अक्षर {ALPHA[n-1]} हो; त्यसको दायाँ {dev(m)} स्थानमा {c} छ।')
for _ in range(40):
    a, b = rng.randint(1, 26), rng.randint(1, 26)
    if a == b: continue
    n = abs(a - b) - 1
    o, on, _ = num_opts(n, [n+1, n-1, n+2, n-2])
    E('Alphabet Positions', 'medium',
      f'How many letters are there between {ALPHA[a-1]} and {ALPHA[b-1]} in the English alphabet?',
      f'अङ्ग्रेजी वर्णमालामा {ALPHA[a-1]} र {ALPHA[b-1]} बीच कति अक्षर छन्?', o, on,
      f'There are {n} letters between {ALPHA[a-1]} and {ALPHA[b-1]}.',
      f'{ALPHA[a-1]} र {ALPHA[b-1]} बीच {dev(n)} वटा अक्षर छन्।')

# ---------- reverse alphabet positions ----------
for _ in range(40):
    n = rng.randint(1, 26)
    c = ALPHA[26-n]
    o, on = letter_opts(c)
    E('Alphabet Positions', 'medium',
      f'Which letter is {ord_s(n)} from the right in the English alphabet?',
      f'अङ्ग्रेजी वर्णमालामा दायाँबाट {dev(n)}औँ अक्षर कुन हो?', o, on,
      f'The {ord_s(n)} letter from the right is {c}.', f'दायाँबाट {dev(n)}औँ अक्षर {c} हो।')

n = em.write('expansion-r10-iq2.json')
print('IQ2 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
