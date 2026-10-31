#!/usr/bin/env python3
"""R10 generator 31: final top-up (~850). Vocab list 6 (G-H words) + Maths 10.
Bank includes R10 (post-dedupe-removal), so no cross-dupes. Explanations
follow the audit lessons: no 'The answer is' phrasing; NE ends on the
marked value as the last '=' value."""
import sys, random, math, datetime
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num
from vocab_data import WORDS as WORDS1
from vocab_data2 import WORDS2

bank = Bank(exclude_prefix='ZZZ-NONE-')
rng = random.Random(313131)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'tsc-primary', 'tsc-secondary', 'police', 'army']

emv = Emitter(bank, 'R10-VOC6')
WORDS6 = [
    ('gain', 'लाभ', 'profit', 'नाफा', 'loss', 'नोक्सान', 'benefit', 'फाइदा', 'harm', 'हानि'),
    ('game', 'खेल', 'sport', 'खेलकुद', 'play', 'खेल', 'match', 'खेल', 'work', 'काम'),
    ('gap', 'अन्तर', 'space', 'ठाउँ', 'hole', 'प्वाल', 'difference', 'फरक', 'bridge', 'पुल'),
    ('garden', 'बगैँचा', 'park', 'पार्क', 'yard', 'आँगन', 'orchard', 'बगैँचा', 'field', 'खेत'),
    ('gather', 'जम्मा गर्नु', 'collect', 'सङ्कलन गर्नु', 'scatter', 'छरिनु', 'assemble', 'भेला हुनु', 'disperse', 'छरिनु'),
    ('general', 'सामान्य', 'common', 'साधारण', 'specific', 'विशिष्ट', 'ordinary', 'साधारण', 'particular', 'विशेष'),
    ('generous', 'उदार', 'kind', 'दयालु', 'selfish', 'स्वार्थी', 'charitable', 'दानशील', 'greedy', 'लोभी'),
    ('gentle', 'नम्र', 'mild', 'हल्का', 'harsh', 'कठोर', 'soft', 'नरम', 'rough', 'खस्रो'),
    ('gift', 'उपहार', 'present', 'उपहार', 'donation', 'दान', 'offering', 'भेटी', 'penalty', 'सजाय'),
    ('girl', 'केटी', 'maiden', 'कन्या', 'boy', 'केटा', 'woman', 'महिला', 'lady', 'महिला'),
    ('give', 'दिनु', 'offer', 'प्रस्ताव गर्नु', 'take', 'लिनु', 'grant', 'प्रदान गर्नु', 'receive', 'प्राप्त गर्नु'),
    ('glad', 'खुसी', 'happy', 'प्रसन्न', 'sad', 'दुःखी', 'pleased', 'खुसी', 'sorry', 'दुःखी'),
    ('glass', 'सिसा', 'mirror', 'ऐना', 'cup', 'कप', 'bottle', 'बोतल', 'window', 'झ्याल'),
    ('global', 'विश्वव्यापी', 'worldwide', 'विश्वभरि', 'local', 'स्थानीय', 'international', 'अन्तर्राष्ट्रिय', 'national', 'राष्ट्रिय'),
    ('glory', 'महिमा', 'fame', 'प्रसिद्धि', 'shame', 'लाज', 'honour', 'सम्मान', 'disgrace', 'अपमान'),
    ('goal', 'लक्ष्य', 'aim', 'उद्देश्य', 'target', 'निशाना', 'purpose', 'उद्देश्य', 'start', 'सुरु'),
    ('god', 'भगवान्', 'deity', 'देवता', 'divine', 'दिव्य', 'lord', 'प्रभु', 'devil', 'शैतान'),
    ('gold', 'सुन', 'aurum', 'सुन', 'metal', 'धातु', 'treasure', 'खजाना', 'silver', 'चाँदी'),
    ('good', 'राम्रो', 'fine', 'उत्तम', 'bad', 'खराब', 'excellent', 'उत्कृष्ट', 'poor', 'खराब'),
    ('govern', 'शासन गर्नु', 'rule', 'शासन गर्नु', 'obey', 'आज्ञा मान्नु', 'administer', 'प्रशासन गर्नु', 'serve', 'सेवा गर्नु'),
    ('grace', 'कृपा', 'favour', 'अनुग्रह', 'blessing', 'आशीर्वाद', 'disgrace', 'अपमान', 'charm', 'आकर्षण'),
    ('grade', 'श्रेणी', 'level', 'स्तर', 'rank', 'पद', 'mark', 'अङ्क', 'class', 'कक्षा'),
    ('grain', 'अन्न', 'cereal', 'अन्न', 'seed', 'बीउ', 'corn', 'मकै', 'rice', 'चामल'),
    ('grand', 'भव्य', 'magnificent', 'शानदार', 'humble', 'विनम्र', 'splendid', 'शानदार', 'ordinary', 'साधारण'),
    ('grant', 'अनुदान', 'award', 'पुरस्कार', 'subsidy', 'अनुदान', 'refuse', 'इन्कार गर्नु', 'gift', 'उपहार'),
    ('grape', 'अङ्गुर', 'fruit', 'फल', 'berry', 'बेरी', 'vine', 'लहरा', 'apple', 'स्याउ'),
    ('grasp', 'समात्नु', 'grip', 'पक्रनु', 'hold', 'समात्नु', 'release', 'छोड्नु', 'understand', 'बुझ्नु'),
    ('grass', 'घाँस', 'lawn', 'चउर', 'meadow', 'घाँसे मैदान', 'plant', 'बिरुवा', 'herb', 'जडीबुटी'),
    ('grateful', 'कृतज्ञ', 'thankful', 'धन्यवाद दिने', 'ungrateful', 'अकृतज्ञ', 'obliged', 'आभारी', 'thankless', 'अकृतज्ञ'),
    ('grave', 'गम्भीर', 'serious', 'गम्भीर', 'trivial', 'तुच्छ', 'solemn', 'गम्भीर', 'tomb', 'चिहान'),
    ('great', 'महान्', 'grand', 'भव्य', 'small', 'सानो', 'vast', 'विशाल', 'tiny', 'सानो'),
    ('green', 'हरियो', 'verdant', 'हरियो', 'lush', 'हरियो', 'ripe', 'पाकेको', 'yellow', 'पहेँलो'),
    ('greet', 'अभिवादन गर्नु', 'welcome', 'स्वागत गर्नु', 'ignore', 'बेवास्ता गर्नु', 'salute', 'सलाम गर्नु', 'farewell', 'बिदाइ'),
    ('grief', 'शोक', 'sorrow', 'दुःख', 'joy', 'खुसी', 'mourning', 'शोक', 'delight', 'खुसी'),
    ('ground', 'जमिन', 'earth', 'पृथ्वी', 'soil', 'माटो', 'floor', 'भुइँ', 'sky', 'आकाश'),
    ('group', 'समूह', 'team', 'टोली', 'bunch', 'गुच्छा', 'individual', 'व्यक्ति', 'crowd', 'भिड'),
    ('grow', 'बढ्नु', 'increase', 'वृद्धि हुनु', 'shrink', 'खुम्चिनु', 'develop', 'विकास हुनु', 'decline', 'घट्नु'),
    ('guard', 'रक्षक', 'protector', 'रक्षक', 'watchman', 'चौकीदार', 'defender', 'रक्षक', 'attacker', 'आक्रमणकारी'),
    ('guess', 'अनुमान', 'estimate', 'अनुमान', 'suppose', 'अनुमान गर्नु', 'know', 'जान्नु', 'calculate', 'हिसाब गर्नु'),
    ('guest', 'अतिथि', 'visitor', 'आगन्तुक', 'host', 'आतिथ्य गर्ने', 'stranger', 'अपरिचित', 'friend', 'साथी'),
    ('guide', 'मार्गदर्शक', 'leader', 'नेता', 'mentor', 'गुरु', 'manual', 'पुस्तिका', 'follower', 'अनुयायी'),
    ('guilty', 'दोषी', 'culpable', 'दोषी', 'innocent', 'निर्दोष', 'responsible', 'जिम्मेवार', 'blameless', 'निर्दोष'),
    ('habit', 'बानी', 'custom', 'चलन', 'practice', 'अभ्यास', 'routine', 'दिनचर्या', 'addiction', 'लत'),
    ('half', 'आधा', 'part', 'भाग', 'portion', 'हिस्सा', 'whole', 'पूरै', 'full', 'भरिएको'),
    ('hall', 'हल', 'auditorium', 'सभागृह', 'room', 'कोठा', 'chamber', 'कक्ष', 'corridor', 'गल्ली'),
    ('hand', 'हात', 'palm', 'हत्केला', 'finger', 'औँला', 'arm', 'पाखुरा', 'foot', 'खुट्टा'),
    ('handle', 'सम्हाल्नु', 'manage', 'व्यवस्थापन गर्नु', 'grip', 'समात्नु', 'mishandle', 'गलत तरिकाले सम्हाल्नु', 'hold', 'समात्नु'),
    ('handsome', 'सुन्दर', 'good-looking', 'राम्रो देखिने', 'ugly', 'कुरूप', 'attractive', 'आकर्षक', 'plain', 'साधारण'),
    ('hang', 'झुन्ड्याउनु', 'suspend', 'झुन्ड्याउनु', 'drop', 'खसाल्नु', 'dangle', 'झुन्डिनु', 'remove', 'हटाउनु'),
    ('happen', 'हुनु', 'occur', 'घट्नु', 'take place', 'हुनु', 'event', 'घटना', 'prevent', 'रोक्नु'),
    ('happy', 'खुसी', 'joyful', 'हर्षित', 'sad', 'दुःखी', 'glad', 'प्रसन्न', 'gloomy', 'उदास'),
    ('hard', 'कठिन', 'difficult', 'गाह्रो', 'easy', 'सजिलो', 'tough', 'कठोर', 'soft', 'नरम'),
    ('harm', 'हानि', 'injury', 'चोट', 'damage', 'क्षति', 'benefit', 'फाइदा', 'hurt', 'चोट पुर्‍याउनु'),
    ('harvest', 'फसल', 'crop', 'बाली', 'yield', 'उपज', 'gathering', 'सङ्कलन', 'sowing', 'रोपाइँ'),
    ('hate', 'घृणा गर्नु', 'despise', 'घृणा गर्नु', 'love', 'माया गर्नु', 'detest', 'घृणा गर्नु', 'adore', 'धेरै माया गर्नु'),
    ('head', 'टाउको', 'skull', 'खप्पर', 'chief', 'प्रमुख', 'brain', 'मस्तिष्क', 'foot', 'खुट्टा'),
    ('health', 'स्वास्थ्य', 'wellness', 'स्वास्थ्य', 'fitness', 'तन्दुरुस्ती', 'disease', 'रोग', 'illness', 'बिरामी'),
    ('hear', 'सुन्नु', 'listen', 'सुन्नु', 'perceive', 'बुझ्नु', 'ignore', 'बेवास्ता गर्नु', 'sound', 'ध्वनि'),
    ('heart', 'मुटु', 'core', 'केन्द्र', 'organ', 'अङ्ग', 'soul', 'आत्मा', 'mind', 'मन'),
    ('heat', 'तातो', 'warmth', 'न्यानोपन', 'cold', 'चिसो', 'fire', 'आगो', 'frost', 'तुसारो'),
    ('heaven', 'स्वर्ग', 'paradise', 'स्वर्ग', 'hell', 'नर्क', 'sky', 'आकाश', 'earth', 'पृथ्वी'),
    ('heavy', 'भारी', 'weighty', 'गह्रौँ', 'light', 'हल्का', 'dense', 'घना', 'thin', 'पातलो'),
    ('height', 'उचाइ', 'altitude', 'उचाइ', 'elevation', 'उचाइ', 'depth', 'गहिराइ', 'length', 'लम्बाइ'),
    ('help', 'मद्दत', 'aid', 'सहायता', 'support', 'समर्थन', 'hinder', 'बाधा पुर्‍याउनु', 'assist', 'सहयोग गर्नु'),
    ('hero', 'वीर', 'champion', 'विजेता', 'warrior', 'योद्धा', 'coward', 'कायर', 'villain', 'खलनायक'),
    ('hide', 'लुकाउनु', 'conceal', 'लुकाउनु', 'reveal', 'प्रकट गर्नु', 'cover', 'ढाक्नु', 'show', 'देखाउनु'),
    ('high', 'उच्च', 'tall', 'अग्लो', 'low', 'निम्न', 'lofty', 'उच्च', 'short', 'छोटो'),
    ('hill', 'पहाड', 'mound', 'ढिस्को', 'mountain', 'हिमाल', 'valley', 'उपत्यका', 'peak', 'चुचुरो'),
    ('hint', 'सङ्केत', 'clue', 'सुराग', 'suggestion', 'सुझाव', 'trace', 'चिन्ह', 'answer', 'उत्तर'),
    ('hire', 'भर्ना गर्नु', 'employ', 'रोजगारी दिनु', 'dismiss', 'बर्खास्त गर्नु', 'recruit', 'भर्ना गर्नु', 'fire', 'निकाल्नु'),
    ('history', 'इतिहास', 'past', 'विगत', 'chronicle', 'इतिहास', 'record', 'अभिलेख', 'future', 'भविष्य'),
    ('hit', 'हान्नु', 'strike', 'प्रहार गर्नु', 'beat', 'पिट्नु', 'miss', 'चुक्नु', 'smash', 'ठोक्नु'),
    ('hold', 'समात्नु', 'grasp', 'पक्रनु', 'release', 'छोड्नु', 'grip', 'समात्नु', 'drop', 'खसाल्नु'),
    ('hole', 'प्वाल', 'gap', 'अन्तर', 'pit', 'खाडल', 'opening', 'खुला ठाउँ', 'cavity', 'गुहा'),
    ('holiday', 'बिदा', 'vacation', 'छुट्टी', 'festival', 'पर्व', 'leave', 'बिदा', 'workday', 'कामको दिन'),
    ('holy', 'पवित्र', 'sacred', 'पवित्र', 'divine', 'दिव्य', 'unholy', 'अपवित्र', 'blessed', 'धन्य'),
    ('home', 'घर', 'house', 'घर', 'residence', 'निवास', 'dwelling', 'बासस्थान', 'office', 'कार्यालय'),
    ('honest', 'इमानदार', 'truthful', 'सत्यवादी', 'dishonest', 'बेइमान', 'sincere', 'निष्कपट', 'deceitful', 'धोकेबाज'),
    ('honour', 'सम्मान', 'respect', 'आदर', 'glory', 'महिमा', 'shame', 'लाज', 'dignity', 'गरिमा'),
    ('hope', 'आशा', 'expectation', 'अपेक्षा', 'desire', 'इच्छा', 'despair', 'निराशा', 'faith', 'विश्वास'),
    ('horse', 'घोडा', 'steed', 'घोडा', 'mare', 'घोडी', 'stallion', 'घोडा', 'pony', 'टट्टू'),
    ('hospital', 'अस्पताल', 'clinic', 'क्लिनिक', 'infirmary', 'अस्पताल', 'ward', 'वार्ड', 'dispensary', 'औषधालय'),
    ('host', 'आतिथ्य गर्ने', 'entertainer', 'मनोरञ्जनकर्ता', 'guest', 'अतिथि', 'owner', 'मालिक', 'anchor', 'सञ्चालक'),
    ('hot', 'तातो', 'warm', 'न्यानो', 'cold', 'चिसो', 'boiling', 'उम्लिरहेको', 'cool', 'चिसो'),
    ('hour', 'घण्टा', 'time', 'समय', 'minute', 'मिनेट', 'period', 'अवधि', 'day', 'दिन'),
    ('house', 'घर', 'dwelling', 'बासस्थान', 'home', 'घर', 'building', 'भवन', 'hut', 'झुपडी'),
    ('huge', 'विशाल', 'enormous', 'दानवाकार', 'tiny', 'सानो', 'immense', 'अत्यन्त ठूलो', 'small', 'सानो'),
    ('human', 'मानव', 'person', 'व्यक्ति', 'mortal', 'मानव', 'being', 'प्राणी', 'animal', 'जनावर'),
    ('humble', 'विनम्र', 'modest', 'विनीत', 'proud', 'गर्वित', 'meek', 'नम्र', 'arrogant', 'अहङ्कारी'),
    ('humour', 'हास्य', 'wit', 'बुद्धिमत्ता', 'comedy', 'कमेडी', 'seriousness', 'गम्भीरता', 'joke', 'चुट्किला'),
    ('hunger', 'भोक', 'appetite', 'भोक', 'starvation', 'अनिकाल', 'thirst', 'तृष्णा', 'satiety', 'तृप्ति'),
    ('hunt', 'सिकार', 'chase', 'पछ्याउनु', 'pursuit', 'पछ्याइ', 'search', 'खोज्नु', 'catch', 'समात्नु'),
    ('hurry', 'हतार', 'rush', 'हतार', 'haste', 'हतार', 'delay', 'ढिलाइ', 'speed', 'गति'),
    ('hurt', 'चोट पुर्‍याउनु', 'injure', 'घाइते बनाउनु', 'harm', 'हानि पुर्‍याउनु', 'heal', 'निको पार्नु', 'pain', 'दुखाइ'),
    ('husband', 'श्रीमान्', 'spouse', 'पति', 'partner', 'साझेदार', 'wife', 'श्रीमती', 'bachelor', 'अविवाहित'),
]
seen1 = {w[0] for w in WORDS1} | {w[0] for w in WORDS2}
valid = []
for w in WORDS6:
    if w[0] in seen1:
        print('SKIP dup word (list1/2):', w[0], file=sys.stderr); continue
    en, ne, syn, syn_ne, ant, ant_ne, rel, rel_ne, unrel, unrel_ne = w
    ok_en = len({syn.lower(), ant.lower(), rel.lower(), unrel.lower()}) == 4
    ok_ne = len({syn_ne, ant_ne, rel_ne, unrel_ne}) == 4
    if ok_en and ok_ne:
        valid.append(w)
    else:
        print('SKIP row (dup option words/glosses):', en, file=sys.stderr)
print(f'Valid words: {len(valid)}/{len(WORDS6)}', file=sys.stderr)

pool_ne = [(w[0], w[1]) for w in valid]
def rand_ne_distractors(correct_ne, k=3):
    cands = [ne for (en2, ne) in pool_ne if ne != correct_ne]
    rng.shuffle(cands)
    out = []
    for c in cands:
        if c not in out: out.append(c)
        if len(out) == k: break
    return out
def rand_en_distractors(correct_en, k=3):
    cands = [(en2, ne) for (en2, ne) in pool_ne if en2 != correct_en]
    rng.shuffle(cands)
    out = []
    for p in cands:
        if p[0] not in [x[0] for x in out]: out.append(p)
        if len(out) == k: break
    return out

for w in valid:
    en, ne, syn, syn_ne, ant, ant_ne, rel, rel_ne, unrel, unrel_ne = w
    emv.emit(EX, 'English', 'Vocabulary', 'easy', 1,
            f'Choose the synonym of {en}.', f'‘{en}’ शब्दको पर्यायवाची (synonym) छान्नुहोस्।',
            [syn.capitalize(), ant.capitalize(), rel.capitalize(), unrel.capitalize()],
            [syn_ne, ant_ne, rel_ne, unrel_ne], 0,
            f"'{en}' means the same as '{syn}'.", f'‘{en}’ को अर्थ ‘{syn}’ हो।')
    emv.emit(EX, 'English', 'Vocabulary', 'medium', 1,
            f'Which word is closest in meaning to {en}?', f'‘{en}’ को अर्थसँग सबैभन्दा नजिकको शब्द कुन हो?',
            [syn.capitalize(), ant.capitalize(), rel.capitalize(), unrel.capitalize()],
            [syn_ne, ant_ne, rel_ne, unrel_ne], 0,
            f"Of the options, '{syn}' is closest in meaning to '{en}'.",
            f'विकल्पहरूमध्ये ‘{syn}’ को अर्थ ‘{en}’ सँग सबैभन्दा नजिक छ।')
    emv.emit(EX, 'English', 'Vocabulary', 'easy', 1,
            f'Choose the antonym of {en}.', f'‘{en}’ शब्दको विलोम (antonym) छान्नुहोस्।',
            [ant.capitalize(), syn.capitalize(), rel.capitalize(), unrel.capitalize()],
            [ant_ne, syn_ne, rel_ne, unrel_ne], 0,
            f"The opposite of '{en}' is '{ant}'.", f'‘{en}’ को विलोम ‘{ant}’ हो।')
    emv.emit(EX, 'English', 'Vocabulary', 'medium', 1,
            f'Which word is opposite in meaning to {en}?', f'‘{en}’ को अर्थको विपरीत शब्द कुन हो?',
            [ant.capitalize(), syn.capitalize(), rel.capitalize(), unrel.capitalize()],
            [ant_ne, syn_ne, rel_ne, unrel_ne], 0,
            f"Of the options, '{ant}' is opposite in meaning to '{en}'.",
            f'विकल्पहरूमध्ये ‘{ant}’ को अर्थ ‘{en}’ को विपरीत छ।')
    ds = rand_ne_distractors(ne, 3)
    emv.emit(EX, 'English', 'Vocabulary', 'medium', 2,
            f"What does '{en}' mean?", f'‘{en}’ को अर्थ के हो?',
            [ne] + ds, [ne] + ds, 0,
            f"'{en}' means '{ne}' in Nepali.", f'‘{en}’ को नेपाली अर्थ ‘{ne}’ हो।')
    ds = rand_en_distractors(en, 3)
    opts_en = [en] + [d[0] for d in ds]
    opts_ne = [ne] + [d[1] for d in ds]
    emv.emit(EX, 'English', 'Vocabulary', 'hard', 2,
            f"Which English word means '{ne}'?", f'‘{ne}’ भन्ने अर्थ भएको अङ्ग्रेजी शब्द कुन हो?',
            opts_en, opts_ne, 0,
            f"'{en}' means '{ne}'.", f'‘{en}’ को अर्थ ‘{ne}’ हो।')
nv = emv.write('expansion-r10-vocab6.json')
print('VOCAB6 TOTAL:', nv, 'rejected:', len(emv.rejected))

# ================= MATHS 10 =================
emm = Emitter(bank, 'R10-M10')
def qm(topic, diff, marks, q, qn, opts, optn, ans, exp, expn):
    emm.emit(EX, 'Maths & Numerical', topic, diff, marks, q, qn, opts, optn, ans, exp, expn)
def num_opts(ans, lo, hi, step=1):
    s = {ans}
    while len(s) < 4:
        v = rng.randrange(lo, hi+1, step)
        if v != ans and v >= 0: s.add(v)
    o = list(s); rng.shuffle(o)
    return o, o.index(ans)

# what percent of X is Y?
for _ in range(100):
    whole = rng.choice([80, 100, 120, 150, 200, 240, 250, 300, 400, 500, 600, 800, 1000])
    pct = rng.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 90])
    part = whole * pct // 100
    if whole * pct % 100: continue
    o, ai = num_opts(pct, 1, 100, 5)
    qm('Percentages', 'easy', 1,
        f"What percent of {whole} is {part}?", f"{whole} को कति प्रतिशत {part} हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Percent = {part}/{whole} x 100 = {pct}%.",
        f"प्रतिशत = {part}/{whole} × १०० = {pct}% हो।")

# find missing number given average
for _ in range(80):
    a = rng.randrange(10, 90, 5); b = rng.randrange(10, 90, 5)
    avg = rng.randrange(20, 80, 5)
    c = 3 * avg - a - b
    if c <= 0 or c > 200: continue
    o, ai = num_opts(c, max(1, c-20), c+20, 5)
    qm('Averages', 'medium', 1,
        f"The average of three numbers is {avg}. Two of the numbers are {a} and {b}. What is the third number?",
        f"तीन वटा सङ्ख्याको औसत {avg} छ। दुई वटा सङ्ख्या {a} र {b} छन्। तेस्रो सङ्ख्या कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Sum = 3 x {avg} = {3*avg}. Third number = {3*avg} - {a} - {b} = {c}.",
        f"योग = ३ × {avg} = {3*avg} हो। तेस्रो सङ्ख्या = {3*avg} - {a} - {b} = {c} हो।")

# A's share is X, find total (ratio)
for _ in range(80):
    r1 = rng.randrange(1, 6); r2 = rng.randrange(1, 6)
    if r1 == r2: continue
    unit = rng.choice([50, 100, 150, 200, 250, 300])
    share = r1 * unit
    total = (r1 + r2) * unit
    o, ai = num_opts(total, max(100, total-400), total+400, 50)
    qm('Ratio & Proportion', 'medium', 1,
        f"A and B share money in the ratio {r1}:{r2}. If A's share is Rs {share}, what is the total amount shared?",
        f"A र B ले {r1}:{r2} को अनुपातमा पैसा बाँड्छन्। यदि A को हिस्सा रू {share} हो भने जम्मा रकम कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"One part = {share}/{r1} = {unit}. Total = ({r1} + {r2}) x {unit} = {total}.",
        f"एक भाग = {share}/{r1} = {unit} हो। जम्मा = ({r1} + {r2}) × {unit} = {total} हो।")

# A does 1/k of work in n days
for _ in range(60):
    k = rng.choice([2, 3, 4, 5])
    n = rng.choice([3, 4, 5, 6, 8, 10, 12])
    ans = k * n
    o, ai = num_opts(ans, max(1, ans-10), ans+10, 1)
    qm('Work & Time', 'easy', 1,
        f"A can do 1/{k} of a work in {n} days. In how many days can A finish the whole work?",
        f"A ले एउटा कामको 1/{k} भाग {n} दिनमा गर्न सक्छ। A ले पूरै काम कति दिनमा सक्न सक्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Whole work takes {k} x {n} = {ans} days.",
        f"पूरै काममा {k} × {n} = {ans} दिन लाग्छ।")

# trains: find length from time and speed
for _ in range(60):
    v = rng.choice([36, 45, 54, 60, 72, 90])
    t = rng.choice([5, 6, 8, 10, 12, 15, 20])
    L = v * 5/18 * t
    if L != int(L): continue
    ans = int(L)
    o, ai = num_opts(ans, max(10, ans-100), ans+100, 10)
    qm('Trains', 'medium', 1,
        f"A train running at {v} km/h crosses a pole in {t} seconds. What is the length of the train?",
        f"{v} किमी/घण्टाको गतिमा चलिरहेको रेलले एउटा खम्बा {t} सेकेन्डमा पार गर्छ। रेलको लम्बाइ कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Speed = {v}x5/18 = {v*5/18:g} m/s. Length = {v*5/18:g} x {t} = {ans} m.",
        f"गति = {v}×५/१८ = {v*5/18:g} मि/से हो। लम्बाइ = {v*5/18:g} × {t} = {ans} मिटर हो।")

# calendar 1970-1979
for _ in range(100):
    y = rng.randrange(1970, 1980)
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
    qm('Calendar & Clock', 'medium', 1,
        f"What day of the week was {d} {months[m-1]} {y}?", f"{y} को {ne_m} {d} गते कुन बार थियो?",
        o, [ne_map[x] for x in o], o.index(wd),
        f"{d} {months[m-1]} {y} was a {wd}.", f"{y} को {ne_m} {d} गते {ne_map[wd]} थियो।")

# series: +cubes of even numbers, x4+1
def series_block(gen, name, n=60):
    for _ in range(n):
        seq, ans = gen()
        if seq is None: continue
        disp = ', '.join(str(x) for x in seq)
        o, ai = num_opts(ans, max(0, ans-40), ans+40, 1)
        qm('Number Series', 'medium', 1,
            f"What is the next number in the series: {disp}, ...?", f"श्रेणीको अर्को सङ्ख्या कति हो: {disp}, ...?",
            [str(x) for x in o], [dev_num(x) for x in o], ai,
            f"The series follows the {name} pattern. The next term is {ans}.",
            f"श्रेणीले {name} ढाँचा पछ्याउँछ। अर्को पद {ans} हो।")
def g_even_cubes():
    a = rng.randrange(5, 40); s = [a]; i = rng.randrange(1, 3)
    ev = [2, 4, 6, 8, 10, 12, 14]
    for k in range(4): s.append(s[-1] + ev[i+k]**3)
    return s, s[-1] + ev[i+4]**3
def g_x4p1():
    a = rng.randrange(2, 10); s = [a]
    for _ in range(4): s.append(s[-1]*4 + 1)
    return s, s[-1]*4 + 1
series_block(g_even_cubes, 'add cubes of consecutive even numbers')
series_block(g_x4p1, 'multiply by 4 and add 1')

# fractions: multiply mixed numbers
for _ in range(60):
    w1 = rng.randrange(1, 5); a1, b1 = rng.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)])
    w2 = rng.randrange(1, 4); a2, b2 = rng.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)])
    n1 = w1 * b1 + a1; n2 = w2 * b2 + a2
    num = n1 * n2; den = b1 * b2
    g = math.gcd(num, den)
    ans_str = f"{num//g}/{den//g}" if den//g != 1 else str(num//g)
    opts = [ans_str, f"{num}/{den}", f"{num//g+1}/{den//g}", f"{num//g}/{den//g+1}"]
    if len(set(opts)) < 4: continue
    o = opts[:]; rng.shuffle(o)
    qm('Fractions', 'hard', 2,
        f"What is {w1} {a1}/{b1} x {w2} {a2}/{b2}?", f"{w1} {a1}/{b1} × {w2} {a2}/{b2} कति हो?",
        o, [dev(x) for x in o], o.index(ans_str),
        f"{w1} {a1}/{b1} = {n1}/{b1} and {w2} {a2}/{b2} = {n2}/{b2}. Product = {num}/{den} = {ans_str}.",
        f"{w1} {a1}/{b1} = {n1}/{b1} र {w2} {a2}/{b2} = {n2}/{b2} हो। गुणनफल = {num}/{den} = {ans_str} हो।")

# decimals: divide decimal by whole number
for _ in range(60):
    b = rng.choice([2, 4, 5, 8, 10])
    ans = rng.choice([1.2, 1.5, 2.4, 2.5, 3.6, 4.5, 0.6, 0.8, 1.8, 2.2, 3.3, 5.5, 6.4, 7.2])
    a = round(ans * b, 2)
    o = [ans, round(ans+1, 2), round(ans-1, 2), round(ans+2, 2)]
    o = [x for x in o if x > 0]
    if len(set(o)) < 4: continue
    rng.shuffle(o)
    qm('Decimals', 'medium', 1,
        f"What is {a} / {b}?", f"{a} ÷ {b} कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], o.index(ans),
        f"{a} / {b} = {ans}.", f"{a} ÷ {b} = {ans} हो।")

# clock: hands coincide (approx hour)
for _ in range(40):
    h = rng.randrange(1, 11)
    mins = round(h * 60 / 11)  # hands coincide ~5.45*h minutes past h
    ans_str = f"{h}:{mins:02d}"
    opts = [ans_str, f"{h}:00", f"{h}:30", f"{h+1}:00"]
    if len(set(opts)) < 4: continue
    o = opts[:]; rng.shuffle(o)
    qm('Calendar & Clock', 'hard', 2,
        f"Between {h} o'clock and {h+1} o'clock, the hands of a clock coincide once. At approximately what time (to the nearest minute) do they coincide?",
        f"{h} बजे र {h+1} बजेबीच घडीका सुईहरू एक पटक मिल्छन्। लगभग कति बजे मिल्छन् (निकटतम मिनेटमा)?",
        o, [dev(x) for x in o], o.index(ans_str),
        f"The hands coincide about {mins} minutes past {h}, i.e. at about {ans_str}.",
        f"सुईहरू {h} बजेर लगभग {mins} मिनेटमा मिल्छन्, अर्थात् लगभग {ans_str} मा।")
nm = emm.write('expansion-r10-maths10.json')
print('MATHS10 TOTAL:', nm, 'rejected:', len(emm.rejected))
print('G31 GRAND TOTAL:', nv + nm)
