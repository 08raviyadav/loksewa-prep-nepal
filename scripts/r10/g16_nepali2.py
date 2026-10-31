#!/usr/bin/env python3
"""R10 generator 16: Nepali language 2 (~900). Second vocab list, BS months,
days, seasons, more ukhan-tukka, Nepali grammar (karak, sandhi, samas),
Nepali literature (authors & works)."""
import sys, random
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num

bank = Bank()
em = Emitter(bank, 'R10-NEP2')
rng = random.Random(71108)
EX = ['kharidar', 'nasu', 'section-officer', 'tsc-primary', 'tsc-secondary', 'tsc-lower-secondary', 'tsc-license', 'provincial-psc']

def E(sub, diff, q, qn, o, on, expl, expln, idx=0):
    em.emit(EX, 'Nepali Language', sub, diff, 2, q, qn, o, on, idx, expl, expln)

# ---------- second Nepali vocab ----------
# (word, meaning_ne, syn, ant, rel, unrel) — all Nepali
NP2 = [
    ('अनुकूल', 'अनुकूल', 'सहायक', 'प्रतिकूल', 'उपयुक्त', 'विपरीत'),
    ('अनुशासन', 'नियमपालन', 'नियम', 'अनुशासनहीनता', 'शिष्टाचार', 'अव्यवस्था'),
    ('अभिमान', 'घमण्ड', 'अहङ्कार', 'विनम्रता', 'गर्व', 'नम्रता'),
    ('अमूल्य', 'बहुमूल्य', 'मूल्यवान्', 'बेकामे', 'अनमोल', 'सस्तो'),
    ('अल्छी', 'काम नगर्ने', 'निष्क्रिय', 'मेहनती', 'सुस्त', 'परिश्रमी'),
    ('आकाश', 'गगन', 'नभ', 'पाताल', 'अम्बर', 'धरती'),
    ('आदर', 'सम्मान', 'मान', 'अनादर', 'इज्जत', 'अपमान'),
    ('आनन्द', 'खुसी', 'सुख', 'दुःख', 'हर्ष', 'शोक'),
    ('आलस्य', 'अल्छीपना', 'सुस्ती', 'परिश्रम', 'ढिलाइ', 'मेहनत'),
    ('आशा', 'उम्मेद', 'अपेक्षा', 'निराशा', 'भरोसा', 'हताशा'),
    ('इच्छा', 'चाहना', 'अभिलाषा', 'अनिच्छा', 'मनसाय', 'विरक्ति'),
    ('उत्साह', 'जोश', 'उमङ्ग', 'निराशा', 'उत्कण्ठा', 'उदासी'),
    ('उपकार', 'भलाइ', 'सहयोग', 'अपकार', 'हित', 'हानि'),
    ('ऋण', 'कर्जा', 'सापटी', 'धन', 'उधारो', 'नगद'),
    ('कठिन', 'गाह्रो', 'दुष्कर', 'सजिलो', 'कष्टकर', 'सरल'),
    ('कपट', 'छल', 'धोका', 'इमानदारी', 'जाल', 'सत्य'),
    ('करुणा', 'दया', 'ममता', 'क्रूरता', 'सहानुभूति', 'निर्दयता'),
    ('कृतज्ञ', 'आभारी', 'धन्य', 'कृतघ्न', 'ऋणी', 'अकृतज्ञ'),
    ('क्रोध', 'रिस', 'आक्रोश', 'शान्ति', 'कोप', 'धैर्य'),
    ('क्षमा', 'माफी', 'माफ', 'दण्ड', 'उदारता', 'सजाय'),
    ('खुसी', 'प्रसन्न', 'आनन्दित', 'दुःखी', 'हर्षित', 'उदास'),
    ('गर्व', 'अभिमान', 'घमण्ड', 'विनम्रता', 'अहङ्कार', 'नम्रता'),
    ('गम्भीर', 'गहन', 'गहिरो', 'हल्का', 'गम्भीरता', 'चञ्चल'),
    ('चतुर', 'बुद्धिमान्', 'चालाक', 'मूर्ख', 'होसियार', 'अज्ञानी'),
    ('जिज्ञासा', 'कौतूहल', 'उत्सुकता', 'उदासीनता', 'जान्न चाहनु', 'बेवास्ता'),
    ('ज्ञान', 'विद्या', 'बुद्धि', 'अज्ञान', 'जानकारी', 'मूर्खता'),
    ('त्याग', 'छोड्नु', 'बलिदान', 'लोभ', 'समर्पण', 'स्वार्थ'),
    ('दया', 'करुणा', 'ममता', 'क्रूरता', 'सहानुभूति', 'निर्दयता'),
    ('दुःख', 'पीडा', 'वेदना', 'सुख', 'कष्ट', 'आनन्द'),
    ('धैर्य', 'सहनशीलता', 'धीरज', 'अधीरता', 'सन्तोष', 'बेचैनी'),
    ('धन', 'सम्पत्ति', 'दौलत', 'गरिबी', 'ऐश्वर्य', 'दरिद्रता'),
    ('नम्र', 'विनम्र', 'शिष्ट', 'अहङ्कारी', 'विनयी', 'घमण्डी'),
    ('निराशा', 'हताशा', 'नैराश्य', 'आशा', 'उदासी', 'उत्साह'),
    ('निष्ठा', 'इमानदारी', 'सत्यनिष्ठा', 'बेइमानी', 'वफादारी', 'धोका'),
    ('परिश्रम', 'मेहनत', 'श्रम', 'आलस्य', 'उद्यम', 'सुस्ती'),
    ('परोपकार', 'भलाइ', 'सेवा', 'स्वार्थ', 'दान', 'लोभ'),
    ('प्रसन्न', 'खुसी', 'आनन्दित', 'दुःखी', 'हर्षित', 'उदास'),
    ('प्रेम', 'माया', 'स्नेह', 'घृणा', 'ममता', 'द्वेष'),
    ('बुद्धि', 'ज्ञान', 'विवेक', 'मूर्खता', 'समझ', 'अज्ञान'),
    ('भय', 'डर', 'त्रास', 'निर्भयता', 'आतङ्क', 'साहस'),
    ('भलाइ', 'हित', 'कल्याण', 'हानि', 'उपकार', 'अपकार'),
    ('ममता', 'स्नेह', 'दया', 'क्रूरता', 'वात्सल्य', 'निर्दयता'),
    ('माया', 'प्रेम', 'स्नेह', 'घृणा', 'ममता', 'द्वेष'),
    ('मूर्ख', 'अज्ञानी', 'बेवकुफ', 'बुद्धिमान्', 'मन्द', 'चतुर'),
    ('मेहनत', 'परिश्रम', 'श्रम', 'आलस्य', 'उद्यम', 'सुस्ती'),
    ('यश', 'कीर्ति', 'प्रसिद्धि', 'अपयश', 'ख्याति', 'बदनामी'),
    ('रिस', 'क्रोध', 'आक्रोश', 'शान्ति', 'कोप', 'धैर्य'),
    ('लोभ', 'लालच', 'लालसा', 'सन्तोष', 'तृष्णा', 'त्याग'),
    ('विनम्र', 'नम्र', 'शिष्ट', 'अहङ्कारी', 'विनयी', 'घमण्डी'),
    ('विवेक', 'बुद्धि', 'समझदारी', 'मूर्खता', 'विचार', 'अज्ञान'),
    ('शक्ति', 'बल', 'सामर्थ्य', 'कमजोरी', 'ताकत', 'दुर्बलता'),
    ('शान्ति', 'अमन', 'सुख', 'अशान्ति', 'चैन', 'उपद्रव'),
    ('शिष्ट', 'सभ्य', 'विनम्र', 'अशिष्ट', 'सुशील', 'असभ्य'),
    ('सत्य', 'साँचो', 'वास्तविकता', 'झूट', 'यथार्थ', 'असत्य'),
    ('सन्तोष', 'तृप्ति', 'सन्तुष्टि', 'असन्तोष', 'धैर्य', 'लोभ'),
    ('सफलता', 'विजय', 'सिद्धि', 'असफलता', 'जित', 'हार'),
    ('सहनशीलता', 'धैर्य', 'सहन', 'असहनशीलता', 'धीरज', 'अधीरता'),
    ('साहस', 'वीरता', 'हिम्मत', 'कायरता', 'निर्भयता', 'डर'),
    ('सुख', 'आनन्द', 'खुसी', 'दुःख', 'हर्ष', 'पीडा'),
    ('सुन्दर', 'राम्रो', 'मनोहर', 'कुरूप', 'सुहावना', 'भद्दा'),
    ('स्वार्थ', 'आफ्नो हित', 'लोभ', 'परोपकार', 'स्वहित', 'सेवा'),
    ('स्वास्थ्य', 'तन्दुरुस्ती', 'आरोग्य', 'रोग', 'निरोगिता', 'बिमारी'),
    ('हिम्मत', 'साहस', 'वीरता', 'कायरता', 'आँट', 'डर'),
]
for word, meaning, syn, ant, rel, unrel in NP2:
    if len({syn, ant, rel, unrel}) < 4: continue
    # synonym framing
    em.emit(EX, 'Nepali Language', 'Nepali Vocabulary', 'easy', 1,
            f'Choose the synonym of the Nepali word "{word}".',
            f'‘{word}’ शब्दको पर्यायवाची छान्नुहोस्।',
            [syn, ant, rel, unrel], [syn, ant, rel, unrel], 0,
            f'The synonym of "{word}" is "{syn}".', f'‘{word}’ को पर्यायवाची ‘{syn}’ हो।')
    # antonym framing
    em.emit(EX, 'Nepali Language', 'Nepali Vocabulary', 'easy', 1,
            f'Choose the antonym of the Nepali word "{word}".',
            f'‘{word}’ शब्दको विलोम छान्नुहोस्।',
            [ant, syn, rel, unrel], [ant, syn, rel, unrel], 0,
            f'The antonym of "{word}" is "{ant}".', f'‘{word}’ को विलोम ‘{ant}’ हो।')
    # meaning framing
    ds = rng.sample([m for (_, m, _, _, _, _) in NP2 if m != meaning], 3)
    em.emit(EX, 'Nepali Language', 'Nepali Vocabulary', 'medium', 2,
            f'What does the Nepali word "{word}" mean?',
            f'‘{word}’ शब्दको अर्थ के हो?',
            [meaning] + ds, [meaning] + ds, 0,
            f'"{word}" means "{meaning}".', f'‘{word}’ को अर्थ ‘{meaning}’ हो।')

# ---------- BS months ----------
BS_MONTHS = [('Baisakh', 'वैशाख', 31), ('Jestha', 'जेठ', 32), ('Ashadh', 'असार', 32),
             ('Shrawan', 'श्रावण', 31), ('Bhadra', 'भदौ', 31), ('Ashwin', 'असोज', 31),
             ('Kartik', 'कात्तिक', 30), ('Mangsir', 'मंसिर', 30), ('Poush', 'पुस', 30),
             ('Magh', 'माघ', 29), ('Falgun', 'फागुन', 30), ('Chaitra', 'चैत', 31)]
for i, (en, ne, days) in enumerate(BS_MONTHS):
    # build options manually (days as numbers)
    opts = [str(days)] + [str(x) for x in [30, 31, 29, 32] if x != days][:3]
    opts_ne = [dev_num(int(x)) for x in opts]
    E('Nepali Calendar', 'easy', f'How many days are there in the Nepali month of {en}?',
      f'नेपाली महिना {ne} मा कति दिन हुन्छ?', opts, opts_ne,
      f'{en} has {days} days.', f'{ne} महिनामा {dev(days)} दिन हुन्छ।')
    # order in year
    opts2 = [str(i+1)] + [str(x) for x in [i+2, i, i+3] if 1 <= x <= 12][:3]
    opts2_ne = [dev_num(int(x)) for x in opts2]
    while len(opts2) < 4:
        opts2.append(str((i+5) % 12 + 1)); opts2_ne.append(dev_num(int(opts2[-1])))
    E('Nepali Calendar', 'medium', f'Which month of the Nepali year is {en}?',
      f'{ne} नेपाली वर्षको कुन महिना हो?', opts2, opts2_ne,
      f'{en} is the {i+1}th month of the Nepali year.', f'{ne} नेपाली वर्षको {dev(i+1)}औँ महिना हो।')

# ---------- days of week ----------
DAYS = [('Sunday', 'आइतबार'), ('Monday', 'सोमबार'), ('Tuesday', 'मङ्गलबार'), ('Wednesday', 'बुधबार'),
        ('Thursday', 'बिहीबार'), ('Friday', 'शुक्रबार'), ('Saturday', 'शनिबार')]
def ord_en(n):
    if n == 1: return '1st'
    if n == 2: return '2nd'
    if n == 3: return '3rd'
    return f'{n}th'
for i, (en, ne) in enumerate(DAYS):
    opts = [en] + [x for x, _ in DAYS if x != en][:3]
    opts_ne = [dict(DAYS)[x] for x in opts]
    E('Nepali Calendar', 'easy', f'Which day is the {ord_en(i+1)} day of the Nepali week?',
      f'{ne} हप्ताको कुन बार हो?', opts, opts_ne,
      f'The {ord_en(i+1)} day of the week is {en}.', f'हप्ताको {dev(i+1)}औँ दिन {ne} हो।')
    # which day comes after
    nxt = DAYS[(i+1) % 7]
    opts2 = [nxt[0]] + [x for x, _ in DAYS if x != nxt[0]][:3]
    opts2_ne = [dict(DAYS)[x] for x in opts2]
    E('Nepali Calendar', 'easy', f'Which day comes after {en}?',
      f'{ne} पछि कुन बार आउँछ?', opts2, opts2_ne,
      f'{nxt[0]} comes after {en}.', f'{ne} पछि {nxt[1]} आउँछ।')

# ---------- seasons ----------
SEASONS = [('Spring', 'वसन्त'), ('Summer', 'ग्रीष्म'), ('Monsoon', 'वर्षा'), ('Autumn', 'शरद्'), ('Winter', 'हेमन्त'), ('Late Winter', 'शिशिर')]
for en, ne in SEASONS:
    opts = [en] + [x for x, _ in SEASONS if x != en][:3]
    opts_ne = [dict(SEASONS)[x] for x in opts]
    E('Nepali Calendar', 'easy', f'Which Nepali season is "{ne}" in English?',
      f'"{ne}" ऋतुलाई अङ्ग्रेजीमा के भनिन्छ?', opts, opts_ne,
      f'"{ne}" is "{en}" in English.', f'"{ne}" ऋतुलाई अङ्ग्रेजीमा "{en}" भनिन्छ।')

# ---------- more ukhan-tukka ----------
UKHAN = [
    ('आगो नभई धुवाँ उठ्दैन', 'कारणबिना परिणाम हुँदैन', 'No smoke without fire'),
    ('आफ्नो हात जगन्नाथ', 'आफ्नो काम आफैँ गर्नुपर्छ', 'Self-help is the best help'),
    ('इन्द्रेणी नदेखी पानी नपर्ला', 'सङ्केतबिना घटना हुँदैन', 'No rainbow without rain'),
    ('उखान नबुझी कुरा नबुझ्नु', 'उखानको अर्थ नबुझी कुरा नबुझ्नु', 'Do not judge without understanding'),
    ('काग कराउँदैमा बिहान हुँदैन', 'बाहिरी हल्लाले सत्य बदलिँदैन', 'A crow\'s caw does not make the morning'),
    ('काम कुरो एकातिर, कुम्लो बोकी ठिमीतिर', 'काम एउटा, कुरा अर्को', 'One thing said, another done'),
    ('खाली भाँडो धेरै बज्छ', 'अज्ञानी मानिस धेरै बोल्छ', 'Empty vessels make the most noise'),
    ('गाई काटे गौहत्या, बाघ मारे वीरता', 'कामअनुसार मूल्याङ्कन फरक हुन्छ', 'Judgement depends on the deed'),
    ('घरको बाघ वनको स्याल', 'घरमा वीर, बाहिर डरपोक', 'A tiger at home, a jackal outside'),
    ('चोरको खुट्टा काट्नु', 'चोरलाई सजाय दिनु', 'To punish a thief'),
    ('जसको जिउँदो, उसकै माटो', 'जसको शक्ति, उसकै अधिकार', 'Might is right'),
    ('जति माया त्यति घृणा', 'माया बढ्दै जाँदा घृणा पनि बढ्छ', 'Love and hate grow together'),
    ('झूटको खुट्टा हुँदैन', 'झूट लामो समय टिक्दैन', 'A lie has no legs'),
    ('टाउको दुखेको औषधि नाइटोमा', 'समस्या एउटा, उपचार अर्को', 'Wrong remedy for the problem'),
    ('ठूलो माछा सानो माछा खान्छ', 'बलियोले कमजोरलाई दबाउँछ', 'Big fish eat small fish'),
    ('ढुङ्गा हान्नेले हात दुखाउँछ', 'अरूलाई हानि गर्नेले आफैँ दुःख पाउँछ', 'Who throws stones hurts his own hand'),
    ('नाच्न नजान्ने आँगन टेढो', 'आफ्नो कमी अरूलाई दोष दिनु', 'A bad workman blames his tools'),
    ('पानीमा डुबेर मर्नु', 'सजिलो काममा असफल हुनु', 'To fail at an easy task'),
    ('बाँदरको हातमा नरिवल', 'अयोग्य व्यक्तिको हातमा बहुमूल्य कुरा', 'A coconut in a monkey\'s hand'),
    ('मुखमा राम राम, बगलमा छुरा', 'बाहिर मित्रता, भित्र शत्रुता', 'A smiling face with a hidden dagger'),
    ('रातो मुख, कालो मन', 'बाहिर राम्रो, भित्र खराब', 'Fair face, foul heart'),
    ('सुनको अण्डा दिने हाँस', 'धेरै लाभ दिने स्रोत', 'The goose that lays golden eggs'),
    ('हात्ती गयो, पुच्छर अड्कियो', 'ठूलो काम भयो, सानो बाँकी रह्यो', 'The elephant passed, the tail stuck'),
    ('अन्धाले अन्धालाई बाटो देखाउनु', 'अज्ञानीले अज्ञानीलाई सिकाउनु', 'The blind leading the blind'),
    ('आफ्नो गोरुको बाह्रै टक्का', 'आफ्नो कुरालाई मात्र सही ठान्नु', 'To think only one\'s own view is right'),
    ('कुकुरले हड्डी चपाउँछ', 'लोभीले जे पायो त्यही खान्छ', 'A dog chews the bone it gets'),
    ('गधालाई गुलियो के थाहा', 'अज्ञानीलाई राम्रो कुराको मूल्य थाहा हुँदैन', 'A donkey does not know sweetness'),
    ('घोडा चढ्नेले लड्नु पर्छ', 'ठूलो काम गर्नेले जोखिम लिनुपर्छ', 'Who rides a horse must fall'),
    ('चन्द्रमामा दाग', 'राम्रोमा पनि केही कमी हुन्छ', 'Even the moon has spots'),
    ('जो चोर, उसैको सोर', 'चोरले नै चोरीको आवाज गर्छ', 'The thief shouts the loudest'),
    ('डुब्नेलाई तिनकाको सहारा', 'सङ्कटमा सानो सहयोग पनि ठूलो हुन्छ', 'A drowning man clutches at a straw'),
    ('नौ डुबेसी माझी रुँदैन', 'अनुभवीले सानो विपत्तिमा आत्तिँदैन', 'An experienced boatman does not cry when the boat sinks'),
    ('पानी नपरी बाढी आउँदैन', 'कारणबिना घटना हुँदैन', 'No flood without rain'),
    ('बिरालोले मुसा समात्नु', 'कमजोरले बलियोलाई हराउनु', 'The cat catches the mouse'),
    ('भैंसी अगाडि बीन बजाउनु', 'अज्ञानीलाई ज्ञान दिनु व्यर्थ छ', 'To play the flute before a buffalo'),
    ('माछा माछा भ्यागुतो', 'सानो कुरालाई ठूलो बनाउनु', 'To make a mountain out of a molehill'),
    ('सर्पले सर्पको खुट्टा देख्छ', 'समान प्रकृतिका मानिसले एकअर्कालाई चिन्छन्', 'A snake sees another snake\'s feet'),
    ('हातमा लागेको सुन', 'हातमा परेको अवसर', 'Gold in hand'),
]
for ukhan, meaning, meaning_en in UKHAN:
    ds = rng.sample([m for (_, m, _) in UKHAN if m != meaning], 3)
    em.emit(EX, 'Nepali Language', 'Ukhan-Tukka', 'medium', 2,
            f'What does the Nepali proverb "{ukhan}" mean?',
            f'‘{ukhan}’ उखानको अर्थ के हो?',
            [meaning] + ds, [meaning] + ds, 0,
            f'"{ukhan}" means: {meaning}.', f'‘{ukhan}’ को अर्थ: {meaning} हो।')
    ds2 = rng.sample([u for (u, _, _) in UKHAN if u != ukhan], 3)
    em.emit(EX, 'Nepali Language', 'Ukhan-Tukka', 'hard', 2,
            f'Which Nepali proverb means "{meaning}"?',
            f'‘{meaning}’ भन्ने अर्थ भएको उखान कुन हो?',
            [ukhan] + ds2, [ukhan] + ds2, 0,
            f'The proverb is "{ukhan}".', f'उखान ‘{ukhan}’ हो।')

# ---------- Nepali grammar: karak ----------
KARAK = [
    ('कर्त्ता कारक', 'काम गर्ने व्यक्ति', 'Subject case'),
    ('कर्म कारक', 'कामको फल भोग्ने', 'Object case'),
    ('करण कारक', 'साधन बुझाउने', 'Instrumental case'),
    ('सम्प्रदान कारक', 'दान वा दिने भाव बुझाउने', 'Dative case'),
    ('अपादान कारक', 'छुट्टिने भाव बुझाउने', 'Ablative case'),
    ('सम्बन्ध कारक', 'सम्बन्ध बुझाउने', 'Genitive case'),
    ('अधिकरण कारक', 'स्थान वा समय बुझाउने', 'Locative case'),
    ('सम्बोधन कारक', 'बोलाउने भाव बुझाउने', 'Vocative case'),
]
for name, meaning, meaning_en in KARAK:
    ds = rng.sample([m for (_, m, _) in KARAK if m != meaning], 3)
    em.emit(EX, 'Nepali Language', 'Nepali Grammar', 'medium', 2,
            f'What does "{name}" indicate in Nepali grammar?',
            f'नेपाली व्याकरणमा ‘{name}’ ले के बुझाउँछ?',
            [meaning] + ds, [meaning] + ds, 0,
            f'"{name}" indicates {meaning_en.lower()}.', f'‘{name}’ ले {meaning} बुझाउँछ।')

# ---------- Nepali literature ----------
LIT = [
    ('Who wrote the Nepali novel "Muna Madan"?', 'नेपाली उपन्यास "मुनामदन" कसले लेखे?', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Lekhnath Paudyal', 'लेखनाथ पौड्याल', 'Bal Krishna Sama', 'बालकृष्ण सम'),
    ('Who is known as the "Adikavi" (first poet) of Nepali literature?', 'नेपाली साहित्यका "आदिकवि" भनेर कसलाई चिनिन्छ?', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Lekhnath Paudyal', 'लेखनाथ पौड्याल', 'Motiram Bhatta', 'मोतीराम भट्ट'),
    ('Who wrote the Nepali epic "Shakuntala"?', 'नेपाली महाकाव्य "शकुन्तला" कसले लेखे?', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Lekhnath Paudyal', 'लेखनाथ पौड्याल', 'Bal Krishna Sama', 'बालकृष्ण सम'),
    ('Who translated the Ramayana into Nepali?', 'रामायणलाई नेपालीमा कसले अनुवाद गरे?', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Motiram Bhatta', 'मोतीराम भट्ट', 'Lekhnath Paudyal', 'लेखनाथ पौड्याल'),
    ('Who is known as "Maha Kavi" of Nepali literature?', 'नेपाली साहित्यका "महाकवि" भनेर कसलाई चिनिन्छ?', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Lekhnath Paudyal', 'लेखनाथ पौड्याल', 'Bal Krishna Sama', 'बालकृष्ण सम'),
    ('Who wrote the Nepali novel "Seto Bagh"?', 'नेपाली उपन्यास "सेतो बाघ" कसले लेखे?', 'Diamond Shumsher Rana', 'डायमण्ड शमशेर राणा', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Parijat', 'पारिजात'),
    ('Who wrote the Nepali novel "Shirishko Phool"?', 'नेपाली उपन्यास "शिरीषको फूल" कसले लेखे?', 'Parijat', 'पारिजात', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Diamond Shumsher Rana', 'डायमण्ड शमशेर राणा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य'),
    ('Who wrote the Nepali novel "Palpasa Cafe"?', 'नेपाली उपन्यास "पल्पसा क्याफे" कसले लेखे?', 'Narayan Wagle', 'नारायण वाग्ले', 'Parijat', 'पारिजात', 'Diamond Shumsher Rana', 'डायमण्ड शमशेर राणा', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा'),
    ('Who wrote the Nepali novel "Karnali Blues"?', 'नेपाली उपन्यास "कर्णाली ब्लुज" कसले लेखे?', 'Buddhi Sagar', 'बुद्धिसागर', 'Narayan Wagle', 'नारायण वाग्ले', 'Parijat', 'पारिजात', 'Diamond Shumsher Rana', 'डायमण्ड शमशेर राणा'),
    ('Who wrote the Nepali novel "Radha"?', 'नेपाली उपन्यास "राधा" कसले लेखे?', 'Krishna Dharabasi', 'कृष्ण धाराबासी', 'Parijat', 'पारिजात', 'Buddhi Sagar', 'बुद्धिसागर', 'Narayan Wagle', 'नारायण वाग्ले'),
    ('Who wrote the Nepali play "Mukunda Indira"?', 'नेपाली नाटक "मुकुन्द इन्दिरा" कसले लेखे?', 'Bal Krishna Sama', 'बालकृष्ण सम', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Lekhnath Paudyal', 'लेखनाथ पौड्याल'),
    ('Who is known as the "Yug Kavi" of Nepali literature?', 'नेपाली साहित्यका "युगकवि" भनेर कसलाई चिनिन्छ?', 'Siddhicharan Shrestha', 'सिद्धिचरण श्रेष्ठ', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Lekhnath Paudyal', 'लेखनाथ पौड्याल'),
    ('Who wrote the Nepali poem "Pinjada ko Suga"?', 'नेपाली कविता "पिञ्जडाको सुगा" कसले लेखे?', 'Lekhnath Paudyal', 'लेखनाथ पौड्याल', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Bal Krishna Sama', 'बालकृष्ण सम'),
    ('Who is known as the "Kavi Shiromani" of Nepali literature?', 'नेपाली साहित्यका "कविशिरोमणि" भनेर कसलाई चिनिन्छ?', 'Lekhnath Paudyal', 'लेखनाथ पौड्याल', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Motiram Bhatta', 'मोतीराम भट्ट'),
    ('Who founded the "Sharada" magazine?', 'पत्रिका "शारदा" कसले स्थापना गरे?', 'Riddhi Bahadur Malla', 'ऋद्धिबहादुर मल्ल', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Motiram Bhatta', 'मोतीराम भट्ट'),
    ('Who wrote the first Nepali novel "Bir Charitra"?', 'पहिलो नेपाली उपन्यास "वीर चरित्र" कसले लेखे?', 'Girija Prasad Joshi', 'गिरिजाप्रसाद जोशी', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Diamond Shumsher Rana', 'डायमण्ड शमशेर राणा'),
    ('Who wrote the Nepali novel "Basanti"?', 'नेपाली उपन्यास "बसन्ती" कसले लेखे?', 'Diamond Shumsher Rana', 'डायमण्ड शमशेर राणा', 'Parijat', 'पारिजात', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य'),
    ('Who wrote the Nepali story collection "Naso"?', 'नेपाली कथा सङ्ग्रह "नासो" कसले लेखे?', 'Guru Prasad Mainali', 'गुरुप्रसाद मैनाली', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Parijat', 'पारिजात'),
    ('Who is known as the "Katha Samrat" of Nepali literature?', 'नेपाली साहित्यका "कथा सम्राट" भनेर कसलाई चिनिन्छ?', 'Guru Prasad Mainali', 'गुरुप्रसाद मैनाली', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Parijat', 'पारिजात'),
    ('Who wrote the Nepali novel "Sumnima"?', 'नेपाली उपन्यास "सुम्निमा" कसले लेखे?', 'Bishweshwar Prasad Koirala', 'विश्वेश्वरप्रसाद कोइराला', 'Parijat', 'पारिजात', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Diamond Shumsher Rana', 'डायमण्ड शमशेर राणा'),
    ('Who wrote the Nepali novel "Modiain"?', 'नेपाली उपन्यास "मोदिआइन" कसले लेखे?', 'Bishweshwar Prasad Koirala', 'विश्वेश्वरप्रसाद कोइराला', 'Parijat', 'पारिजात', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Diamond Shumsher Rana', 'डायमण्ड शमशेर राणा'),
    ('Who wrote the Nepali novel "Hitler ra Yahudi"?', 'नेपाली उपन्यास "हिटलर र यहुदी" कसले लेखे?', 'Bishweshwar Prasad Koirala', 'विश्वेश्वरप्रसाद कोइराला', 'Parijat', 'पारिजात', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Diamond Shumsher Rana', 'डायमण्ड शमशेर राणा'),
    ('Who wrote the Nepali novel "Tin Ghumti"?', 'नेपाली उपन्यास "तीन घुम्ती" कसले लेखे?', 'Bishweshwar Prasad Koirala', 'विश्वेश्वरप्रसाद कोइराला', 'Parijat', 'पारिजात', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Diamond Shumsher Rana', 'डायमण्ड शमशेर राणा'),
    ('Who wrote the Nepali novel "Narendra Dai"?', 'नेपाली उपन्यास "नरेन्द्र दाइ" कसले लेखे?', 'Bishweshwar Prasad Koirala', 'विश्वेश्वरप्रसाद कोइराला', 'Parijat', 'पारिजात', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Diamond Shumsher Rana', 'डायमण्ड शमशेर राणा'),
    ('Who wrote the Nepali essay "Laxmi Nibandha Sangraha"?', 'नेपाली निबन्ध "लक्ष्मी निबन्ध सङ्ग्रह" कसले लेखे?', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य', 'Lekhnath Paudyal', 'लेखनाथ पौड्याल', 'Bal Krishna Sama', 'बालकृष्ण सम'),
    ('Who is the author of the Nepali book "Jhola"?', 'नेपाली पुस्तक "झोला" का लेखक को हुन्?', 'Krishna Dharabasi', 'कृष्ण धाराबासी', 'Parijat', 'पारिजात', 'Buddhi Sagar', 'बुद्धिसागर', 'Narayan Wagle', 'नारायण वाग्ले'),
    ('Who is the author of the Nepali book "Aina Jhyal Ko Putali"?', 'नेपाली पुस्तक "ऐना झ्यालको पुतली" का लेखक को हुन्?', 'Indra Bahadur Rai', 'इन्द्रबहादुर राई', 'Parijat', 'पारिजात', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य'),
    ('Who is the author of the Nepali book "Aaja Ramita Chha"?', 'नेपाली पुस्तक "आज रमिता छ" का लेखक को हुन्?', 'Indra Bahadur Rai', 'इन्द्रबहादुर राई', 'Parijat', 'पारिजात', 'Laxmi Prasad Devkota', 'लक्ष्मीप्रसाद देवकोटा', 'Bhanubhakta Acharya', 'भानुभक्त आचार्य'),
    ('Who is the author of the Nepali book "Loo"?', 'नेपाली पुस्तक "लू" का लेखक को हुन्?', 'Nayan Raj Pandey', 'नयनराज पाण्डे', 'Parijat', 'पारिजात', 'Buddhi Sagar', 'बुद्धिसागर', 'Narayan Wagle', 'नारायण वाग्ले'),
    ('Who is the author of the Nepali book "Ular"?', 'नेपाली पुस्तक "उलार" का लेखक को हुन्?', 'Nayan Raj Pandey', 'नयनराज पाण्डे', 'Parijat', 'पारिजात', 'Buddhi Sagar', 'बुद्धिसागर', 'Narayan Wagle', 'नारायण वाग्ले'),
]
for q, qn, a, an, d1, d1n, d2, d2n, d3, d3n in LIT:
    E('Nepali Literature', 'medium', q, qn, [a, d1, d2, d3], [an, d1n, d2n, d3n],
      f'The answer is {a}.', f'उत्तर {an} हो।')

n = em.write('expansion-r10-nepali2.json')
print('NEPALI2 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
