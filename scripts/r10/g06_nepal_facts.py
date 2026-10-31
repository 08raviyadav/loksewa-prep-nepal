#!/usr/bin/env python3
"""R10 generator 6: Nepal facts (~1,500). Districts (HQ/province/reverse),
mountains, rivers, lakes, parks, history dates, constitution articles,
festivals, firsts, symbols. All facts are standard, well-established GK."""
import sys, random
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num

bank = Bank()
em = Emitter(bank, 'R10-NPL')
rng = random.Random(55006)
EX_PSC = ['kharidar', 'nasu', 'section-officer', 'provincial-psc', 'psc-service-groups', 'nrb-assistant', 'rbb', 'police', 'army']
EX_ALL = EX_PSC + ['foreign-service', 'tsc-primary', 'tsc-secondary']

# (district_en, district_ne, hq_en, hq_ne, province_en, province_ne)
DISTRICTS = [
    ('Taplejung', 'ताप्लेजुङ', 'Phungling', 'फुङ्लिङ', 'Koshi', 'कोशी'),
    ('Panchthar', 'पाँचथर', 'Phidim', 'फिदिम', 'Koshi', 'कोशी'),
    ('Ilam', 'इलाम', 'Ilam', 'इलाम', 'Koshi', 'कोशी'),
    ('Jhapa', 'झापा', 'Bhadrapur', 'भद्रपुर', 'Koshi', 'कोशी'),
    ('Morang', 'मोरङ', 'Biratnagar', 'विराटनगर', 'Koshi', 'कोशी'),
    ('Sunsari', 'सुनसरी', 'Inaruwa', 'इनरुवा', 'Koshi', 'कोशी'),
    ('Dhankuta', 'धनकुटा', 'Dhankuta', 'धनकुटा', 'Koshi', 'कोशी'),
    ('Terhathum', 'तेह्रथुम', 'Myaglung', 'म्याङलुङ', 'Koshi', 'कोशी'),
    ('Sankhuwasabha', 'सङ्खुवासभा', 'Khandbari', 'खाँदबारी', 'Koshi', 'कोशी'),
    ('Bhojpur', 'भोजपुर', 'Bhojpur', 'भोजपुर', 'Koshi', 'कोशी'),
    ('Solukhumbu', 'सोलुखुम्बु', 'Salleri', 'सल्लेरी', 'Koshi', 'कोशी'),
    ('Okhaldhunga', 'ओखलढुङ्गा', 'Okhaldhunga', 'ओखलढुङ्गा', 'Koshi', 'कोशी'),
    ('Khotang', 'खोटाङ', 'Diktel', 'दिक्तेल', 'Koshi', 'कोशी'),
    ('Udayapur', 'उदयपुर', 'Gaighat', 'गाईघाट', 'Koshi', 'कोशी'),
    ('Saptari', 'सप्तरी', 'Rajbiraj', 'राजविराज', 'Madhesh', 'मधेश'),
    ('Siraha', 'सिरहा', 'Siraha', 'सिरहा', 'Madhesh', 'मधेश'),
    ('Dhanusha', 'धनुषा', 'Janakpur', 'जनकपुर', 'Madhesh', 'मधेश'),
    ('Mahottari', 'महोत्तरी', 'Jaleshwor', 'जलेश्वर', 'Madhesh', 'मधेश'),
    ('Sarlahi', 'सर्लाही', 'Malangwa', 'मलङ्गवा', 'Madhesh', 'मधेश'),
    ('Rautahat', 'रौतहट', 'Gaur', 'गौर', 'Madhesh', 'मधेश'),
    ('Bara', 'बारा', 'Kalaiya', 'कलैया', 'Madhesh', 'मधेश'),
    ('Parsa', 'पर्सा', 'Birgunj', 'वीरगञ्ज', 'Madhesh', 'मधेश'),
    ('Dolakha', 'दोलखा', 'Charikot', 'चरिकोट', 'Bagmati', 'बागमती'),
    ('Ramechhap', 'रामेछाप', 'Manthali', 'मन्थली', 'Bagmati', 'बागमती'),
    ('Sindhuli', 'सिन्धुली', 'Sindhulimadhi', 'सिन्धुलीमाढी', 'Bagmati', 'बागमती'),
    ('Kavrepalanchok', 'काभ्रेपलाञ्चोक', 'Dhulikhel', 'धुलिखेल', 'Bagmati', 'बागमती'),
    ('Sindhupalchok', 'सिन्धुपाल्चोक', 'Chautara', 'चौतारा', 'Bagmati', 'बागमती'),
    ('Rasuwa', 'रसुवा', 'Dhunche', 'धुन्चे', 'Bagmati', 'बागमती'),
    ('Nuwakot', 'नुवाकोट', 'Bidur', 'विदुर', 'Bagmati', 'बागमती'),
    ('Dhading', 'धादिङ', 'Dhadingbesi', 'धादिङबेँसी', 'Bagmati', 'बागमती'),
    ('Makwanpur', 'मकवानपुर', 'Hetauda', 'हेटौँडा', 'Bagmati', 'बागमती'),
    ('Chitwan', 'चितवन', 'Bharatpur', 'भरतपुर', 'Bagmati', 'बागमती'),
    ('Kathmandu', 'काठमाडौँ', 'Kathmandu', 'काठमाडौँ', 'Bagmati', 'बागमती'),
    ('Bhaktapur', 'भक्तपुर', 'Bhaktapur', 'भक्तपुर', 'Bagmati', 'बागमती'),
    ('Lalitpur', 'ललितपुर', 'Lalitpur', 'ललितपुर', 'Bagmati', 'बागमती'),
    ('Gorkha', 'गोरखा', 'Gorkha', 'गोरखा', 'Gandaki', 'गण्डकी'),
    ('Manang', 'मनाङ', 'Chame', 'चामे', 'Gandaki', 'गण्डकी'),
    ('Mustang', 'मुस्ताङ', 'Jomsom', 'जोमसोम', 'Gandaki', 'गण्डकी'),
    ('Myagdi', 'म्याग्दी', 'Beni', 'बेनी', 'Gandaki', 'गण्डकी'),
    ('Kaski', 'कास्की', 'Pokhara', 'पोखरा', 'Gandaki', 'गण्डकी'),
    ('Lamjung', 'लमजुङ', 'Besisahar', 'बेँसीसहर', 'Gandaki', 'गण्डकी'),
    ('Tanahun', 'तनहुँ', 'Damauli', 'दमौली', 'Gandaki', 'गण्डकी'),
    ('Nawalpur', 'नवलपुर', 'Kawasoti', 'कावासोती', 'Gandaki', 'गण्डकी'),
    ('Syangja', 'स्याङ्जा', 'Putalibazar', 'पुतलीबजार', 'Gandaki', 'गण्डकी'),
    ('Parbat', 'पर्वत', 'Kusma', 'कुश्मा', 'Gandaki', 'गण्डकी'),
    ('Baglung', 'बागलुङ', 'Baglung', 'बागलुङ', 'Gandaki', 'गण्डकी'),
    ('Rukum East', 'रुकुम पूर्व', 'Rukumkot', 'रुकुमकोट', 'Lumbini', 'लुम्बिनी'),
    ('Rolpa', 'रोल्पा', 'Liwang', 'लिवाङ', 'Lumbini', 'लुम्बिनी'),
    ('Pyuthan', 'प्युठान', 'Pyuthan', 'प्युठान', 'Lumbini', 'लुम्बिनी'),
    ('Gulmi', 'गुल्मी', 'Tamghas', 'तम्घास', 'Lumbini', 'लुम्बिनी'),
    ('Arghakhanchi', 'अर्घाखाँची', 'Sandhikharka', 'सन्धिखर्क', 'Lumbini', 'लुम्बिनी'),
    ('Palpa', 'पाल्पा', 'Tansen', 'तानसेन', 'Lumbini', 'लुम्बिनी'),
    ('Nawalparasi West', 'नवलपरासी पश्चिम', 'Parasi', 'परासी', 'Lumbini', 'लुम्बिनी'),
    ('Rupandehi', 'रुपन्देही', 'Siddharthanagar', 'सिद्धार्थनगर', 'Lumbini', 'लुम्बिनी'),
    ('Kapilvastu', 'कपिलवस्तु', 'Taulihawa', 'तौलिहवा', 'Lumbini', 'लुम्बिनी'),
    ('Dang', 'दाङ', 'Ghorahi', 'घोराही', 'Lumbini', 'लुम्बिनी'),
    ('Banke', 'बाँके', 'Nepalgunj', 'नेपालगञ्ज', 'Lumbini', 'लुम्बिनी'),
    ('Bardiya', 'बर्दिया', 'Gulariya', 'गुलरिया', 'Lumbini', 'लुम्बिनी'),
    ('Dolpa', 'डोल्पा', 'Dunai', 'दुनै', 'Karnali', 'कर्णाली'),
    ('Jumla', 'जुम्ला', 'Jumla', 'जुम्ला', 'Karnali', 'कर्णाली'),
    ('Kalikot', 'कालिकोट', 'Manma', 'मान्मा', 'Karnali', 'कर्णाली'),
    ('Mugu', 'मुगु', 'Gamgadhi', 'गमगढी', 'Karnali', 'कर्णाली'),
    ('Humla', 'हुम्ला', 'Simikot', 'सिमिकोट', 'Karnali', 'कर्णाली'),
    ('Rukum West', 'रुकुम पश्चिम', 'Musikot', 'मुसिकोट', 'Karnali', 'कर्णाली'),
    ('Jajarkot', 'जाजरकोट', 'Khalanga', 'खलङ्गा', 'Karnali', 'कर्णाली'),
    ('Dailekh', 'दैलेख', 'Dailekh', 'दैलेख', 'Karnali', 'कर्णाली'),
    ('Surkhet', 'सुर्खेत', 'Birendranagar', 'वीरेन्द्रनगर', 'Karnali', 'कर्णाली'),
    ('Salyan', 'सल्यान', 'Salyan', 'सल्यान', 'Karnali', 'कर्णाली'),
    ('Bajura', 'बाजुरा', 'Martadi', 'मार्टाडी', 'Sudurpashchim', 'सुदूरपश्चिम'),
    ('Bajhang', 'बझाङ', 'Chainpur', 'चैनपुर', 'Sudurpashchim', 'सुदूरपश्चिम'),
    ('Achham', 'अछाम', 'Mangalsen', 'मङ्गलसेन', 'Sudurpashchim', 'सुदूरपश्चिम'),
    ('Doti', 'डोटी', 'Dipayal', 'दिपायल', 'Sudurpashchim', 'सुदूरपश्चिम'),
    ('Kailali', 'कैलाली', 'Dhangadhi', 'धनगढी', 'Sudurpashchim', 'सुदूरपश्चिम'),
    ('Kanchanpur', 'कञ्चनपुर', 'Mahendranagar', 'महेन्द्रनगर', 'Sudurpashchim', 'सुदूरपश्चिम'),
    ('Dadeldhura', 'डडेल्धुरा', 'Dadeldhura', 'डडेल्धुरा', 'Sudurpashchim', 'सुदूरपश्चिम'),
    ('Baitadi', 'बैतडी', 'Baitadi', 'बैतडी', 'Sudurpashchim', 'सुदूरपश्चिम'),
    ('Darchula', 'दार्चुला', 'Darchula', 'दार्चुला', 'Sudurpashchim', 'सुदूरपश्चिम'),
]
assert len(DISTRICTS) == 77, len(DISTRICTS)
ALL_HQ = [(d[2], d[3]) for d in DISTRICTS]
ALL_DIST = [(d[0], d[1]) for d in DISTRICTS]
PROVS = [('Koshi', 'कोशी'), ('Madhesh', 'मधेश'), ('Bagmati', 'बागमती'), ('Gandaki', 'गण्डकी'),
         ('Lumbini', 'लुम्बिनी'), ('Karnali', 'कर्णाली'), ('Sudurpashchim', 'सुदूरपश्चिम')]

def pick3(pool, correct, key=lambda x: x[0]):
    cands = [x for x in pool if key(x) != key(correct)]
    rng.shuffle(cands)
    out = []
    for c in cands:
        if c[0] not in [o[0] for o in out]:
            out.append(c)
        if len(out) == 3:
            break
    return out

for (dn, dn_ne, hq, hq_ne, prov, prov_ne) in DISTRICTS:
    # HQ question
    ds = pick3(ALL_HQ, (hq, hq_ne))
    em.emit(EX_PSC, 'Nepal Geography', 'Provinces & Districts', 'easy', 2,
            f'What is the headquarters of {dn} district?',
            f'{dn_ne} जिल्लाको सदरमुकाम कुन हो?',
            [hq] + [d[0] for d in ds], [hq_ne] + [d[1] for d in ds], 0,
            f'{hq} is the headquarters of {dn} district in {prov} Province.',
            f'{hq_ne} {prov_ne} प्रदेशको {dn_ne} जिल्लाको सदरमुकाम हो।')
    # province question
    ds = pick3(PROVS, (prov, prov_ne))
    em.emit(EX_PSC, 'Nepal Geography', 'Provinces & Districts', 'easy', 2,
            f'{dn} district lies in which province of Nepal?',
            f'{dn_ne} जिल्ला नेपालको कुन प्रदेशमा पर्छ?',
            [prov] + [d[0] for d in ds], [prov_ne] + [d[1] for d in ds], 0,
            f'{dn} district lies in {prov} Province.',
            f'{dn_ne} जिल्ला {prov_ne} प्रदेशमा पर्छ।')
    # reverse HQ question
    ds = pick3(ALL_DIST, (dn, dn_ne))
    em.emit(EX_PSC, 'Nepal Geography', 'Provinces & Districts', 'medium', 2,
            f'{hq} is the headquarters of which district?',
            f'{hq_ne} कुन जिल्लाको सदरमुकाम हो?',
            [dn] + [d[0] for d in ds], [dn_ne] + [d[1] for d in ds], 0,
            f'{hq} is the headquarters of {dn} district.',
            f'{hq_ne} {dn_ne} जिल्लाको सदरमुकाम हो।')
    # which district is in province X (one correct among 4 districts)
    others = [d for d in DISTRICTS if d[4] != prov]
    rng.shuffle(others)
    wrong = others[:3]
    opts = [(dn, dn_ne)] + [(d[0], d[1]) for d in wrong]
    em.emit(EX_PSC, 'Nepal Geography', 'Provinces & Districts', 'medium', 2,
            f'Which of the following districts lies in {prov} Province?',
            f'तलका मध्ये कुन जिल्ला {prov_ne} प्रदेशमा पर्छ?',
            [o[0] for o in opts], [o[1] for o in opts], 0,
            f'{dn} district lies in {prov} Province; the others lie in different provinces.',
            f'{dn_ne} जिल्ला {prov_ne} प्रदेशमा पर्छ; अरू जिल्ला फरक प्रदेशमा पर्छन्।')

# ---------------- Mountains ----------------
MOUNTAINS = [
    ('Mount Everest', 'सगरमाथा', 8848, 'Mahalangur', 'महालङ्गुर'),
    ('Kanchenjunga', 'कञ्चनजङ्घा', 8586, 'Kanchenjunga', 'कञ्चनजङ्घा'),
    ('Lhotse', 'ल्होत्से', 8516, 'Mahalangur', 'महालङ्गुर'),
    ('Makalu', 'मकालु', 8485, 'Mahalangur', 'महालङ्गुर'),
    ('Cho Oyu', 'चो ओयू', 8188, 'Mahalangur', 'महालङ्गुर'),
    ('Dhaulagiri', 'धौलागिरी', 8167, 'Dhaulagiri', 'धौलागिरी'),
    ('Manaslu', 'मनास्लु', 8163, 'Manaslu', 'मनास्लु'),
    ('Annapurna I', 'अन्नपूर्ण प्रथम', 8091, 'Annapurna', 'अन्नपूर्ण'),
    ('Gyachung Kang', 'ग्याचुङ काङ', 7952, 'Mahalangur', 'महालङ्गुर'),
    ('Annapurna II', 'अन्नपूर्ण द्वितीय', 7937, 'Annapurna', 'अन्नपूर्ण'),
    ('Himalchuli', 'हिमालचुली', 7893, 'Manaslu', 'मनास्लु'),
    ('Nuptse', 'नुप्त्से', 7864, 'Mahalangur', 'महालङ्गुर'),
    ('Machhapuchhre', 'माछापुच्छ्रे', 6993, 'Annapurna', 'अन्नपूर्ण'),
    ('Ama Dablam', 'आमा दब्लम', 6812, 'Mahalangur', 'महालङ्गुर'),
]
for i, (mn, mn_ne, h, rng_en, rng_ne) in enumerate(MOUNTAINS):
    others = [m for m in MOUNTAINS if m[0] != mn]
    rng.shuffle(others)
    hs = [o[2] for o in others[:3]]
    em.emit(EX_ALL, 'Nepal Geography', 'Mountains', 'easy', 2,
            f'What is the height of {mn}?',
            f'{mn_ne} को उचाइ कति छ?',
            [f'{h} m', f'{hs[0]} m', f'{hs[1]} m', f'{hs[2]} m'],
            [f'{dev_num(h)} मिटर', f'{dev_num(hs[0])} मिटर', f'{dev_num(hs[1])} मिटर', f'{dev_num(hs[2])} मिटर'], 0,
            f'{mn} is {h} m high.',
            f'{mn_ne} {dev_num(h)} मिटर अग्लो छ।')
    em.emit(EX_ALL, 'Nepal Geography', 'Mountains', 'medium', 2,
            f'Which mountain is the {i + 1}{"st" if i == 0 else "nd" if i == 1 else "rd" if i == 2 else "th"} highest in Nepal?',
            f'नेपालको {dev_num(i + 1)}औँ अग्लो हिमाल कुन हो?',
            [mn] + [o[0] for o in others[:3]], [mn_ne] + [o[1] for o in others[:3]], 0,
            f'{mn} ({h} m) is the {i + 1}{"st" if i == 0 else "nd" if i == 1 else "rd" if i == 2 else "th"} highest mountain in Nepal.',
            f'{mn_ne} ({dev_num(h)} मिटर) नेपालको {dev_num(i + 1)}औँ अग्लो हिमाल हो।')
    em.emit(EX_ALL, 'Nepal Geography', 'Mountains', 'medium', 2,
            f'{mn} lies in which mountain range?',
            f'{mn_ne} कुन हिमशृङ्खलामा पर्छ?',
            [rng_en] + [o[3] for o in others[:3] if o[3] != rng_en][:3] if len({o[3] for o in others if o[3] != rng_en}) >= 3 else [rng_en, 'Mahalangur', 'Annapurna', 'Dhaulagiri'],
            [rng_ne] + [o[4] for o in others[:3] if o[4] != rng_ne][:3] if len({o[4] for o in others if o[4] != rng_ne}) >= 3 else [rng_ne, 'महालङ्गुर', 'अन्नपूर्ण', 'धौलागिरी'], 0,
            f'{mn} lies in the {rng_en} range.',
            f'{mn_ne} {rng_ne} हिमशृङ्खलामा पर्छ।')

# ---------------- Rivers ----------------
RIVERS = [
    ('Koshi', 'कोशी', 'Mahabharat range', 'महाभारत शृङ्खला', 'Ganges', 'गङ्गा'),
    ('Gandaki', 'गण्डकी', 'Himalayas', 'हिमालय', 'Ganges', 'गङ्गा'),
    ('Karnali', 'कर्णाली', 'Himalayas', 'हिमालय', 'Ganges', 'गङ्गा'),
    ('Bagmati', 'बागमती', 'Shivapuri', 'शिवपुरी', 'Ganges', 'गङ्गा'),
    ('Mahakali', 'महाकाली', 'Himalayas', 'हिमालय', 'Ganges', 'गङ्गा'),
    ('Rapti', 'राप्ती', 'Mahabharat range', 'महाभारत शृङ्खला', 'Ganges', 'गङ्गा'),
    ('Babai', 'बबई', 'Mahabharat range', 'महाभारत शृङ्खला', 'Ganges', 'गङ्गा'),
    ('Bheri', 'भेरी', 'Himalayas', 'हिमालय', 'Karnali', 'कर्णाली'),
    ('Seti', 'सेती', 'Himalayas', 'हिमालय', 'Karnali', 'कर्णाली'),
    ('Trishuli', 'त्रिशूली', 'Himalayas', 'हिमालय', 'Gandaki', 'गण्डकी'),
    ('Marsyangdi', 'मर्स्याङ्दी', 'Himalayas', 'हिमालय', 'Gandaki', 'गण्डकी'),
    ('Kali Gandaki', 'कालीगण्डकी', 'Himalayas', 'हिमालय', 'Gandaki', 'गण्डकी'),
    ('Sun Koshi', 'सुनकोशी', 'Himalayas', 'हिमालय', 'Koshi', 'कोशी'),
    ('Arun', 'अरुण', 'Himalayas', 'हिमालय', 'Koshi', 'कोशी'),
    ('Tamur', 'तमोर', 'Himalayas', 'हिमालय', 'Koshi', 'कोशी'),
    ('Mechi', 'मेची', 'Mahabharat range', 'महाभारत शृङ्खला', 'Ganges', 'गङ्गा'),
    ('Kankai', 'कन्काई', 'Mahabharat range', 'महाभारत शृङ्खला', 'Ganges', 'गङ्गा'),
    ('Kamala', 'कमला', 'Mahabharat range', 'महाभारत शृङ्खला', 'Ganges', 'गङ्गा'),
]
for (rn, rn_ne, origin, origin_ne, flows, flows_ne) in RIVERS:
    others = [r for r in RIVERS if r[0] != rn]
    rng.shuffle(others)
    em.emit(EX_ALL, 'Nepal Geography', 'Rivers', 'medium', 2,
            f'The {rn} river originates from which region?',
            f'{rn_ne} नदी कुन क्षेत्रबाट उत्पत्ति हुन्छ?',
            [origin] + [o[2] for o in others[:3]], [origin_ne] + [o[3] for o in others[:3]], 0,
            f'The {rn} river originates in the {origin}.',
            f'{rn_ne} नदी {origin_ne} बाट उत्पत्ति हुन्छ।')
    em.emit(EX_ALL, 'Nepal Geography', 'Rivers', 'medium', 2,
            f'The {rn} river is a tributary of which river?',
            f'{rn_ne} नदी कुन नदीको सहायक नदी हो?',
            [flows] + [o[4] for o in others[:3] if o[4] != flows][:3] if len({o[4] for o in others if o[4] != flows}) >= 3 else [flows, 'Ganges', 'Koshi', 'Gandaki'],
            [flows_ne] + [o[5] for o in others[:3] if o[5] != flows_ne][:3] if len({o[5] for o in others if o[5] != flows_ne}) >= 3 else [flows_ne, 'गङ्गा', 'कोशी', 'गण्डकी'], 0,
            f'The {rn} is a tributary of the {flows}.',
            f'{rn_ne} {flows_ne} नदीको सहायक नदी हो।')

# ---------------- Lakes ----------------
LAKES = [
    ('Rara', 'रारा', 'Mugu', 'मुगु', 2990),
    ('Phewa', 'फेवा', 'Kaski', 'कास्की', 742),
    ('Begnas', 'बेगनास', 'Kaski', 'कास्की', 650),
    ('Tilicho', 'तिलिचो', 'Manang', 'मनाङ', 4919),
    ('Gosaikunda', 'गोसाइँकुण्ड', 'Rasuwa', 'रसुवा', 4380),
    ('Shey Phoksundo', 'शे-फोक्सुण्डो', 'Dolpa', 'डोल्पा', 3611),
    ('Bishazari', 'बिसहजारी', 'Chitwan', 'चितवन', 286),
    ('Ghodaghodi', 'घोडाघोडी', 'Kailali', 'कैलाली', 205),
    ('Jagadishpur', 'जगदीशपुर', 'Kapilvastu', 'कपिलवस्तु', 197),
    ('Mai Pokhari', 'माई पोखरी', 'Ilam', 'इलाम', 2121),
]
for (ln, ln_ne, dist, dist_ne, alt) in LAKES:
    others = [l for l in LAKES if l[0] != ln]
    rng.shuffle(others)
    em.emit(EX_ALL, 'Nepal Geography', 'Lakes', 'medium', 2,
            f'{ln} Lake is located in which district?',
            f'{ln_ne} ताल कुन जिल्लामा छ?',
            [dist] + [o[2] for o in others[:3]], [dist_ne] + [o[3] for o in others[:3]], 0,
            f'{ln} Lake is in {dist} district.',
            f'{ln_ne} ताल {dist_ne} जिल्लामा छ।')
    em.emit(EX_ALL, 'Nepal Geography', 'Lakes', 'hard', 2,
            f'What is the approximate altitude of {ln} Lake?',
            f'{ln_ne} तालको अनुमानित उचाइ कति छ?',
            [f'{alt} m', f'{others[0][4]} m', f'{others[1][4]} m', f'{others[2][4]} m'],
            [f'{dev_num(alt)} मिटर', f'{dev_num(others[0][4])} मिटर', f'{dev_num(others[1][4])} मिटर', f'{dev_num(others[2][4])} मिटर'], 0,
            f'{ln} Lake lies at about {alt} m above sea level.',
            f'{ln_ne} ताल समुद्री सतहबाट करिब {dev_num(alt)} मिटर उचाइमा छ।')

# ---------------- National parks ----------------
PARKS = [
    ('Chitwan National Park', 'चितवन राष्ट्रिय निकुञ्ज', 1973, 'One-horned rhinoceros', 'एकसिङ्गे गैंडा'),
    ('Sagarmatha National Park', 'सगरमाथा राष्ट्रिय निकुञ्ज', 1976, 'Mount Everest', 'सगरमाथा'),
    ('Langtang National Park', 'लाङटाङ राष्ट्रिय निकुञ्ज', 1976, 'Red panda', 'रातो पाण्डा'),
    ('Rara National Park', 'रारा राष्ट्रिय निकुञ्ज', 1976, 'Rara Lake', 'रारा ताल'),
    ('Shey Phoksundo National Park', 'शे-फोक्सुण्डो राष्ट्रिय निकुञ्ज', 1984, 'Phoksundo Lake', 'फोक्सुण्डो ताल'),
    ('Bardia National Park', 'बर्दिया राष्ट्रिय निकुञ्ज', 1988, 'Bengal tiger', 'पाटे बाघ'),
    ('Khaptad National Park', 'खप्तड राष्ट्रिय निकुञ्ज', 1984, 'Khaptad plateau', 'खप्तड पठार'),
    ('Shuklaphanta National Park', 'शुक्लाफाँटा राष्ट्रिय निकुञ्ज', 1976, 'Swamp deer', 'बार्हसिङ्गा'),
    ('Parsa National Park', 'पर्सा राष्ट्रिय निकुञ्ज', 1984, 'Wild elephant', 'जङ्गली हात्ती'),
    ('Banke National Park', 'बाँके राष्ट्रिय निकुञ्ज', 2010, 'Bengal tiger', 'पाटे बाघ'),
    ('Shivapuri Nagarjun National Park', 'शिवपुरी नागार्जुन राष्ट्रिय निकुञ्ज', 2002, 'Watershed of Kathmandu', 'काठमाडौँको जलाधार'),
    ('Makalu Barun National Park', 'मकालु बरुण राष्ट्रिय निकुञ्ज', 1992, 'Makalu mountain', 'मकालु हिमाल'),
]
for (pn, pn_ne, yr, famous, famous_ne) in PARKS:
    others = [p for p in PARKS if p[0] != pn]
    rng.shuffle(others)
    em.emit(EX_ALL, 'Nepal Geography', 'National Parks', 'medium', 2,
            f'In which year was {pn} established?',
            f'{pn_ne} कुन वर्ष स्थापना भएको हो?',
            [str(yr), str(others[0][2]), str(others[1][2]), str(others[2][2])],
            [dev_num(yr), dev_num(others[0][2]), dev_num(others[1][2]), dev_num(others[2][2])], 0,
            f'{pn} was established in {yr}.',
            f'{pn_ne} {dev_num(yr)} मा स्थापना भएको हो।')
    em.emit(EX_ALL, 'Nepal Geography', 'National Parks', 'medium', 2,
            f'{pn} is famous for which of the following?',
            f'{pn_ne} तलका मध्ये केका लागि प्रसिद्ध छ?',
            [famous] + [o[3] for o in others[:3]], [famous_ne] + [o[4] for o in others[:3]], 0,
            f'{pn} is famous for the {famous}.',
            f'{pn_ne} {famous_ne} का लागि प्रसिद्ध छ।')

# ---------------- History events ----------------
EVENTS = [
    ('Unification of Nepal began', 'नेपाल एकीकरण सुरु भयो', 1743, 'Prithvi Narayan Shah', 'पृथ्वीनारायण शाह'),
    ('Battle of Kirtipur', 'कीर्तिपुरको युद्ध', 1767, 'Prithvi Narayan Shah', 'पृथ्वीनारायण शाह'),
    ('Kathmandu Valley conquered', 'काठमाडौँ उपत्यका विजय', 1768, 'Prithvi Narayan Shah', 'पृथ्वीनारायण शाह'),
    ('Anglo-Nepal War began', 'अङ्ग्रेज-नेपाल युद्ध सुरु भयो', 1814, 'British East India Company', 'ब्रिटिस इस्ट इन्डिया कम्पनी'),
    ('Treaty of Sugauli signed', 'सुगौली सन्धि भयो', 1816, 'Nepal and Britain', 'नेपाल र बेलायत'),
    ('Kot Parba (Kot Massacre)', 'कोत पर्व', 1846, 'Jung Bahadur Rana', 'जङ्गबहादुर राणा'),
    ('Rana regime began', 'राणा शासन सुरु भयो', 1846, 'Jung Bahadur Rana', 'जङ्गबहादुर राणा'),
    ('Nepal-Britain Treaty of Peace and Friendship', 'नेपाल-बेलायत शान्ति तथा मैत्री सन्धि', 1923, 'Nepal and Britain', 'नेपाल र बेलायत'),
    ('Rana regime ended', 'राणा शासन अन्त्य भयो', 1951, 'Democracy movement', 'प्रजातन्त्र आन्दोलन'),
    ('First general election held', 'पहिलो आम निर्वाचन भयो', 1959, 'BP Koirala became PM', 'बीपी कोइराला प्रधानमन्त्री बने'),
    ('King Mahendra dissolved parliament', 'राजा महेन्द्रले संसद विघटन गरे', 1960, 'Panchayat began', 'पञ्चायत सुरु भयो'),
    ('Panchayat system introduced', 'पञ्चायत व्यवस्था लागू भयो', 1962, 'King Mahendra', 'राजा महेन्द्र'),
    ('First Jana Andolan', 'पहिलो जनआन्दोलन', 1990, 'Democracy restored', 'प्रजातन्त्र पुनर्स्थापना भयो'),
    ('Nepal became a republic', 'नेपाल गणतन्त्र भयो', 2008, 'Constituent Assembly', 'संविधानसभा'),
    ('Constitution of Nepal promulgated', 'नेपालको संविधान जारी भयो', 2015, 'Constituent Assembly', 'संविधानसभा'),
    ('Gorkha earthquake', 'गोरखा भूकम्प', 2015, '7.8 magnitude', '७.८ म्याग्निच्युड'),
    ('Gen Z protests; PM Oli resigned', 'जेन्जी आन्दोलन; प्रधानमन्त्री ओलीले राजीनामा दिए', 2025, '9 September 2025', '९ सेप्टेम्बर २०२५'),
    ('Sushila Karki became interim PM', 'सुशीला कार्की अन्तरिम प्रधानमन्त्री भइन्', 2025, 'First woman PM of Nepal', 'नेपालकी पहिलो महिला प्रधानमन्त्री'),
    ('Lumbini declared birthplace of Buddha (UNESCO)', 'लुम्बिनी बुद्धको जन्मस्थल (युनेस्को)', 1997, 'World Heritage Site', 'विश्व सम्पदा स्थल'),
    ('Chitwan National Park became UNESCO site', 'चितवन राष्ट्रिय निकुञ्ज युनेस्को स्थल बन्यो', 1984, 'World Heritage Site', 'विश्व सम्पदा स्थल'),
    ('Kathmandu Valley became UNESCO site', 'काठमाडौँ उपत्यका युनेस्को स्थल बन्यो', 1979, 'World Heritage Site', 'विश्व सम्पदा स्थल'),
    ('First census of Nepal', 'नेपालको पहिलो जनगणना', 1911, 'Population counted', 'जनसङ्ख्या गणना'),
    ('Nepal joined the United Nations', 'नेपाल संयुक्त राष्ट्रसङ्घको सदस्य बन्यो', 1955, 'UN member', 'संयुक्त राष्ट्रसङ्घको सदस्य'),
    ('Nepal joined SAARC as founder', 'नेपाल सार्कको संस्थापक सदस्य बन्यो', 1985, 'SAARC founded in Dhaka', 'ढाकामा सार्क स्थापना'),
    ('Nepal Rastra Bank established', 'नेपाल राष्ट्र बैंक स्थापना भयो', 1956, 'Central bank', 'केन्द्रीय बैंक'),
    ('Tribhuvan University established', 'त्रिभुवन विश्वविद्यालय स्थापना भयो', 1959, 'First university of Nepal', 'नेपालको पहिलो विश्वविद्यालय'),
    ('Nepal Television began', 'नेपाल टेलिभिजन सुरु भयो', 1985, 'First TV channel', 'पहिलो टेलिभिजन च्यानल'),
    ('Radio Nepal began', 'रेडियो नेपाल सुरु भयो', 1951, 'First radio', 'पहिलो रेडियो'),
    ('First newspaper Gorkhapatra published', 'पहिलो पत्रिका गोरखापत्र प्रकाशित भयो', 1901, 'Oldest newspaper', 'सबैभन्दा पुरानो पत्रिका'),
    ('Nepal Airlines (then Royal Nepal Airlines) founded', 'नेपाल एयरलाइन्स स्थापना भयो', 1958, 'National flag carrier', 'राष्ट्रिय ध्वजावाहक'),
    ('Araniko Highway opened', 'अरनिको राजमार्ग खुल्यो', 1967, 'Kathmandu-Kodari road', 'काठमाडौँ-कोदारी सडक'),
    ('Mahendra Highway completed', 'महेन्द्र राजमार्ग पूरा भयो', 1996, 'East-west highway', 'पूर्व-पश्चिम राजमार्ग'),
    ('First democratic constitution (1948)', 'पहिलो प्रजातान्त्रिक संविधान (२००४)', 1948, 'Government of Nepal Act', 'नेपाल सरकारको वैधानिक कानुन'),
    ('Second Jana Andolan', 'दोस्रो जनआन्दोलन', 2006, 'Loktantra restored', 'लोकतन्त्र पुनर्स्थापना'),
    ('Comprehensive Peace Accord signed', 'विस्तृत शान्ति सम्झौता भयो', 2006, 'End of Maoist conflict', 'माओवादी द्वन्द्व अन्त्य'),
    ('First Constituent Assembly election', 'पहिलो संविधानसभा निर्वाचन', 2008, 'Maoists largest party', 'माओवादी सबैभन्दा ठूलो दल'),
    ('Second Constituent Assembly election', 'दोस्रो संविधानसभा निर्वाचन', 2013, 'NC largest party', 'नेपाली काङ्ग्रेस सबैभन्दा ठूलो दल'),
    ('Nepal adopted federal structure', 'नेपालले सङ्घीय संरचना अपनायो', 2015, '7 provinces', '७ प्रदेश'),
    ('First woman President of Nepal', 'नेपालकी पहिलो महिला राष्ट्रपति', 2015, 'Bidya Devi Bhandari', 'विद्यादेवी भण्डारी'),
    ('First woman Speaker of Nepal', 'नेपालकी पहिलो महिला सभामुख', 2015, 'Onsari Gharti Magar', 'ओनसरी घर्ती मगर'),
    ('First woman Chief Justice of Nepal', 'नेपालकी पहिलो महिला प्रधानन्यायाधीश', 2016, 'Sushila Karki', 'सुशीला कार्की'),
    ('Nepal hosted first SAARC summit', 'नेपालले पहिलो सार्क शिखर सम्मेलन आयोजना गर्यो', 1987, 'Kathmandu', 'काठमाडौँ'),
    ('Mt Everest first climbed', 'सगरमाथा पहिलो पटक आरोहण भयो', 1953, 'Hillary and Tenzing', 'हिलारी र तेन्जिङ'),
    ('First Nepali to climb Everest', 'सगरमाथा चढ्ने पहिलो नेपाली', 1953, 'Tenzing Norgay Sherpa', 'तेन्जिङ नोर्गे शेर्पा'),
    ('Nepal won first Olympic medal (taekwondo, demonstration)', 'नेपालले पहिलो ओलम्पिक पदक जित्यो (ताइक्वान्दो)', 1988, 'Bidhan Lama (bronze, demonstration)', 'विधान लामा (कांस्य, प्रदर्शन)'),
    ('Nepal cricket gained ODI status', 'नेपाल क्रिकेटले एकदिवसीय मान्यता पायो', 2018, 'ICC ODI status', 'आईसीसी एकदिवसीय मान्यता'),
    ('Nepal played first T20 World Cup', 'नेपालले पहिलो टी-२० विश्वकप खेल्यो', 2014, 'Bangladesh', 'बङ्गलादेश'),
    ('Nepal abolished monarchy', 'नेपालमा राजतन्त्र अन्त्य भयो', 2008, 'Constituent Assembly decision', 'संविधानसभाको निर्णय'),
    ('Nepal adopted new map (Kalapani-Lipulekh-Limpiyadhura)', 'नेपालले नयाँ नक्सा अपनायो (कालापानी-लिपुलेक-लिम्पियाधुरा)', 2020, 'Parliament approved', 'संसदले अनुमोदन गर्यो'),
    ('Nepal signed BRI framework with China', 'नेपालले चीनसँग बीआरआई सम्झौता गर्यो', 2017, 'Belt and Road Initiative', 'बेल्ट एन्ड रोड पहल'),
    ('Nepal-India Transit Treaty', 'नेपाल-भारत पारवहन सन्धि', 1991, 'Trade and transit', 'व्यापार तथा पारवहन'),
    ('Nepal-China Transit Agreement', 'नेपाल-चीन पारवहन सम्झौता', 2016, 'Third-country trade access', 'तेस्रो मुलुक व्यापार पहुँच'),
    ('First hydroelectric project Pharping', 'पहिलो जलविद्युत् आयोजना फर्पिङ', 1911, '500 kW', '५०० किलोवाट'),
    ('Kulekhani Hydropower completed', 'कुलेखानी जलविद्युत् सम्पन्न भयो', 1982, 'First reservoir project', 'पहिलो जलाशययुक्त आयोजना'),
    ('Upper Tamakoshi Hydropower completed', 'माथिल्लो तामाकोशी जलविद्युत् सम्पन्न भयो', 2021, '456 MW', '४५६ मेगावाट'),
    ('Nepal first exported electricity to India', 'नेपालले पहिलो पटक भारतमा विद्युत् निर्यात गर्यो', 2021, '39 MW', '३९ मेगावाट'),
    ('Nepal first exported electricity to Bangladesh', 'नेपालले पहिलो पटक बङ्गलादेशमा विद्युत् निर्यात गर्यो', 2024, '40 MW', '४० मेगावाट'),
    ('First population census after federalism', 'सङ्घीयतापछिको पहिलो जनगणना', 2021, '12th census', '१२औँ जनगणना'),
]
for (ev, ev_ne, yr, note, note_ne) in EVENTS:
    others = [e for e in EVENTS if e[0] != ev]
    rng.shuffle(others)
    yrs = [o[2] for o in others[:3]]
    em.emit(EX_ALL, 'Nepal History', 'Historical Events', 'medium', 2,
            f'In which year did the following event occur: {ev}?',
            f'तलको घटना कुन वर्ष भयो: {ev_ne}?',
            [str(yr), str(yrs[0]), str(yrs[1]), str(yrs[2])],
            [dev_num(yr), dev_num(yrs[0]), dev_num(yrs[1]), dev_num(yrs[2])], 0,
            f'{ev} occurred in {yr} ({note}).',
            f'{ev_ne} {dev_num(yr)} मा भयो ({note_ne})।')
    em.emit(EX_ALL, 'Nepal History', 'Historical Events', 'hard', 2,
            f'Which of the following events occurred in {yr}?',
            f'तलका मध्ये कुन घटना {dev_num(yr)} मा भयो?',
            [ev] + [o[0] for o in others[:3]], [ev_ne] + [o[1] for o in others[:3]], 0,
            f'{ev} occurred in {yr}.',
            f'{ev_ne} {dev_num(yr)} मा भयो।')

# ---------------- Constitution articles ----------------
ARTICLES = [
    (1, 'Constitution as the fundamental law', 'संविधान मूल कानून'),
    (2, 'Sovereignty and state authority', 'सार्वभौमसत्ता र राजकीय सत्ता'),
    (3, 'Nation', 'राष्ट्र'),
    (4, 'State of Nepal', 'नेपाल राज्य'),
    (5, 'National interest', 'राष्ट्रिय हित'),
    (6, 'Languages spoken in Nepal', 'नेपालमा बोलिने भाषा'),
    (7, 'Official language', 'सरकारी कामकाजको भाषा'),
    (8, 'National flag', 'राष्ट्रिय झण्डा'),
    (9, 'National anthem', 'राष्ट्रिय गान'),
    (10, 'Nepali citizen', 'नेपाली नागरिक'),
    (11, 'Nepali citizenship', 'नेपाली नागरिकता'),
    (12, 'Citizenship with identity of descent and gender', 'वंशज तथा लैङ्गिक पहिचानसहितको नागरिकता'),
    (13, 'Termination of citizenship', 'नागरिकताको समाप्ति'),
    (14, 'Non-resident Nepali citizenship', 'गैरआवासीय नेपाली नागरिकता'),
    (16, 'Right to live with dignity', 'सम्मानपूर्वक बाँच्न पाउने हक'),
    (17, 'Right to freedom', 'स्वतन्त्रताको हक'),
    (18, 'Right to equality', 'समानताको हक'),
    (19, 'Right to communication', 'सञ्चारको हक'),
    (20, 'Right relating to justice', 'न्यायसम्बन्धी हक'),
    (21, 'Right of victim of crime', 'अपराध पीडितको हक'),
    (22, 'Right against torture', 'यातना विरुद्धको हक'),
    (23, 'Right against preventive detention', 'निवारक नजरबन्द विरुद्धको हक'),
    (24, 'Right against untouchability and discrimination', 'छुवाछूत तथा भेदभाव विरुद्धको हक'),
    (25, 'Right relating to property', 'सम्पत्तिसम्बन्धी हक'),
    (26, 'Right to religious freedom', 'धार्मिक स्वतन्त्रताको हक'),
    (27, 'Right to information', 'सूचनाको हक'),
    (28, 'Right to privacy', 'गोपनीयताको हक'),
    (29, 'Right against exploitation', 'शोषण विरुद्धको हक'),
    (30, 'Right to clean environment', 'स्वच्छ वातावरणको हक'),
    (31, 'Right relating to education', 'शिक्षासम्बन्धी हक'),
    (32, 'Right to language and culture', 'भाषा तथा संस्कृतिको हक'),
    (33, 'Right to employment', 'रोजगारीको हक'),
    (34, 'Right relating to labour', 'श्रमसम्बन्धी हक'),
    (35, 'Right relating to health', 'स्वास्थ्यसम्बन्धी हक'),
    (36, 'Right relating to food', 'खाद्यसम्बन्धी हक'),
    (37, 'Right to housing', 'आवासको हक'),
    (38, 'Rights of women', 'महिलाको हक'),
    (39, 'Rights of the child', 'बालबालिकाको हक'),
    (40, 'Rights of Dalit', 'दलितको हक'),
    (41, 'Rights of senior citizens', 'ज्येष्ठ नागरिकको हक'),
    (42, 'Right to social justice', 'सामाजिक न्यायको हक'),
    (43, 'Right to social security', 'सामाजिक सुरक्षाको हक'),
    (44, 'Rights of the consumer', 'उपभोक्ताको हक'),
    (45, 'Right against exile', 'देश निकाला विरुद्धको हक'),
    (46, 'Right to constitutional remedies', 'संवैधानिक उपचारको हक'),
    (47, 'Implementation of fundamental rights', 'मौलिक हकको कार्यान्वयन'),
    (48, 'Duties of citizens', 'नागरिकको कर्तव्य'),
    (50, 'Directive principles', 'निर्देशक सिद्धान्त'),
    (51, 'Policies of the state', 'राज्यका नीतिहरू'),
    (52, 'Obligations of the state', 'राज्यको दायित्व'),
    (56, 'Structure of the state', 'राज्यको संरचना'),
    (57, 'Distribution of state power', 'राज्यशक्तिको बाँडफाँट'),
    (61, 'President', 'राष्ट्रपति'),
    (62, 'Election of the President', 'राष्ट्रपतिको निर्वाचन'),
    (64, 'Qualifications of the President', 'राष्ट्रपतिको योग्यता'),
    (67, 'Vice-President', 'उपराष्ट्रपति'),
    (74, 'Form of government', 'शासनको स्वरूप'),
    (75, 'Executive power', 'कार्यकारी अधिकार'),
    (76, 'Formation of Council of Ministers', 'मन्त्रिपरिषद् गठन'),
    (83, 'Federal Parliament', 'सङ्घीय संसद'),
    (84, 'House of Representatives', 'प्रतिनिधि सभा'),
    (86, 'National Assembly', 'राष्ट्रिय सभा'),
    (87, 'Qualifications of members', 'सदस्यको योग्यता'),
    (91, 'Speaker and Deputy Speaker', 'सभामुख र उपसभामुख'),
    (100, 'Vote of confidence', 'विश्वासको मत'),
    (100, 'Vote of no confidence', 'अविश्वासको प्रस्ताव'),
    (101, 'Provisions relating to impeachment', 'महाभियोगसम्बन्धी व्यवस्था'),
    (128, 'Supreme Court', 'सर्वोच्च अदालत'),
    (137, 'Constitutional Bench', 'संवैधानिक इजलास'),
    (129, 'Chief Justice and Justices', 'प्रधानन्यायाधीश र न्यायाधीशहरू'),
    (139, 'High Courts', 'उच्च अदालतहरू'),
    (148, 'District Courts', 'जिल्ला अदालतहरू'),
    (162, 'Provincial Executive', 'प्रदेश कार्यपालिका'),
    (175, 'Provincial Assembly', 'प्रदेश सभा'),
    (214, 'Local Executive', 'स्थानीय कार्यपालिका'),
    (221, 'Local Assembly', 'स्थानीय सभा'),
    (220, 'District Assembly', 'जिल्ला सभा'),
    (220, 'District Coordination Committee', 'जिल्ला समन्वय समिति'),
    (223, 'Composition of Municipal Assembly', 'नगर सभाको गठन'),
    (234, 'Inter-State Council', 'अन्तरराज्य परिषद्'),
    (245, 'Election Commission', 'निर्वाचन आयोग'),
    (238, 'Commission for Investigation of Abuse of Authority', 'अख्तियार दुरुपयोग अनुसन्धान आयोग'),
    (240, 'Auditor General', 'महालेखा परीक्षक'),
    (242, 'Public Service Commission', 'लोक सेवा आयोग'),
    (248, 'National Human Rights Commission', 'राष्ट्रिय मानव अधिकार आयोग'),
    (250, 'National Natural Resources and Fiscal Commission', 'राष्ट्रिय प्राकृतिक स्रोत तथा वित्त आयोग'),
    (252, 'National Women Commission', 'राष्ट्रिय महिला आयोग'),
    (255, 'National Dalit Commission', 'राष्ट्रिय दलित आयोग'),
    (258, 'National Inclusion Commission', 'राष्ट्रिय समावेशी आयोग'),
    (247, 'Assistance to the Election Commission', 'निर्वाचन आयोगलाई आवश्यक सहयोग'),
    (284, 'Constitutional Council', 'संवैधानिक परिषद्'),
    (153, 'Judicial Council', 'न्याय परिषद्'),
    (267, 'Nepal Army', 'नेपाली सेना'),
    (268, 'Nepal Police', 'नेपाल प्रहरी'),
    (268, 'Armed Police Force', 'सशस्त्र प्रहरी बल'),
    (266, 'National Security Council', 'राष्ट्रिय सुरक्षा परिषद्'),
    (274, 'Amendment of the Constitution', 'संविधान संशोधन'),
    (275, 'Referendum', 'जनमत सङ्ग्रह'),
    (276, 'Pardons', 'माफी'),
]
for (num, subj, subj_ne) in ARTICLES:
    others = [a for a in ARTICLES if a[0] != num]
    rng.shuffle(others)
    em.emit(EX_PSC, 'Constitution & Governance', 'Constitution Articles', 'medium', 2,
            f'Which article of the Constitution of Nepal (2072) deals with {subj}?',
            f'नेपालको संविधान (२०७२) को कुन धाराले {subj_ne} को व्यवस्था गर्छ?',
            [f'Article {num}', f'Article {others[0][0]}', f'Article {others[1][0]}', f'Article {others[2][0]}'],
            [f'धारा {dev_num(num)}', f'धारा {dev_num(others[0][0])}', f'धारा {dev_num(others[1][0])}', f'धारा {dev_num(others[2][0])}'], 0,
            f'Article {num} of the Constitution deals with {subj}.',
            f'संविधानको धारा {dev_num(num)} ले {subj_ne} को व्यवस्था गर्छ।')
    em.emit(EX_PSC, 'Constitution & Governance', 'Constitution Articles', 'hard', 2,
            f'What does Article {num} of the Constitution of Nepal (2072) provide?',
            f'नेपालको संविधान (२०७२) को धारा {dev_num(num)} ले के व्यवस्था गर्छ?',
            [subj] + [o[1] for o in others[:3]], [subj_ne] + [o[2] for o in others[:3]], 0,
            f'Article {num} provides for {subj}.',
            f'धारा {dev_num(num)} ले {subj_ne} को व्यवस्था गर्छ।')

# ---------------- Festivals ----------------
FESTIVALS = [
    ('Dashain', 'दशैँ', 'September-October', 'सेप्टेम्बर-अक्टोबर', 'Victory of good over evil', 'असत्यमाथि सत्यको विजय'),
    ('Tihar', 'तिहार', 'October-November', 'अक्टोबर-नोभेम्बर', 'Festival of lights', 'उज्यालोको पर्व'),
    ('Holi', 'होली', 'March', 'मार्च', 'Festival of colours', 'रङहरूको पर्व'),
    ('Teej', 'तीज', 'August-September', 'अगस्ट-सेप्टेम्बर', "Women's festival", 'महिलाहरूको पर्व'),
    ('Chhath', 'छठ', 'October-November', 'अक्टोबर-नोभेम्बर', 'Worship of the Sun', 'सूर्यको पूजा'),
    ('Buddha Jayanti', 'बुद्ध जयन्ती', 'May', 'मे', 'Birth of Gautam Buddha', 'गौतम बुद्धको जन्म'),
    ('Maghe Sankranti', 'माघे सङ्क्रान्ति', 'January', 'जनवरी', 'Winter solstice festival', 'शिशिर सङ्क्रान्तिको पर्व'),
    ('Janai Purnima', 'जनैपूर्णिमा', 'August', 'अगस्ट', 'Sacred thread festival', 'पवित्र धागोको पर्व'),
    ('Gai Jatra', 'गाईजात्रा', 'August-September', 'अगस्ट-सेप्टेम्बर', 'Festival of cows', 'गाईको पर्व'),
    ('Indra Jatra', 'इन्द्रजात्रा', 'September', 'सेप्टेम्बर', 'Festival of Indra', 'इन्द्रको पर्व'),
    ('Bisket Jatra', 'बिस्केट जात्रा', 'April', 'अप्रिल', 'New Year festival of Bhaktapur', 'भक्तपुरको नयाँ वर्ष पर्व'),
    ('Rato Machhindranath Jatra', 'रातो मच्छिन्द्रनाथ जात्रा', 'May-June', 'मे-जुन', 'Chariot festival of Patan', 'पाटनको रथयात्रा'),
    ('Losar', 'लोसार', 'February', 'फेब्रुअरी', 'Tibetan New Year', 'तिब्बती नयाँ वर्ष'),
    ('Tamang Losar', 'तामाङ लोसार', 'January-February', 'जनवरी-फेब्रुअरी', 'New Year of Tamang community', 'तामाङ समुदायको नयाँ वर्ष'),
    ('Maghi', 'माघी', 'January', 'जनवरी', 'New Year of Tharu community', 'थारू समुदायको नयाँ वर्ष'),
    ('Udhauli', 'उधौली', 'December', 'डिसेम्बर', 'Harvest festival of Kirat', 'किरातको फसल पर्व'),
    ('Ubhauli', 'उभौली', 'May', 'मे', 'Festival of Kirat', 'किरातको पर्व'),
    ('Shree Panchami', 'श्री पञ्चमी', 'January-February', 'जनवरी-फेब्रुअरी', 'Goddess Saraswati worship', 'देवी सरस्वतीको पूजा'),
    ('Shivaratri', 'शिवरात्री', 'February-March', 'फेब्रुअरी-मार्च', 'Night of Lord Shiva', 'भगवान शिवको रात'),
    ('Ram Nawami', 'राम नवमी', 'March-April', 'मार्च-अप्रिल', 'Birth of Lord Ram', 'भगवान रामको जन्म'),
    ('Krishna Janmashtami', 'कृष्ण जन्माष्टमी', 'August-September', 'अगस्ट-सेप्टेम्बर', 'Birth of Lord Krishna', 'भगवान कृष्णको जन्म'),
    ('Nag Panchami', 'नाग पञ्चमी', 'July-August', 'जुलाई-अगस्ट', 'Worship of serpents', 'नागको पूजा'),
    ('Rishi Panchami', 'ऋषि पञ्चमी', 'August-September', 'अगस्ट-सेप्टेम्बर', "Worship of sages", 'ऋषिहरूको पूजा'),
    ('Kushe Aunsi', "कुशे औँसी", 'August-September', 'अगस्ट-सेप्टेम्बर', "Father's Day", 'बुबाको मुख हेर्ने दिन'),
    ('Mata Tirtha Aunsi', 'माता तीर्थ औँसी', 'April-May', 'अप्रिल-मे', "Mother's Day", 'आमाको मुख हेर्ने दिन'),
    ('Guru Purnima', 'गुरु पूर्णिमा', 'July', 'जुलाई', "Teacher's Day", 'शिक्षक दिवस'),
    ('Saraswati Puja', 'सरस्वती पूजा', 'January-February', 'जनवरी-फेब्रुअरी', 'Goddess of learning', 'विद्याकी देवी'),
    ('Fulpati', 'फूलपाती', 'September-October', 'सेप्टेम्बर-अक्टोबर', 'Seventh day of Dashain', 'दशैँको सातौँ दिन'),
    ('Maha Ashtami', 'महाअष्टमी', 'September-October', 'सेप्टेम्बर-अक्टोबर', 'Eighth day of Dashain', 'दशैँको आठौँ दिन'),
    ('Maha Nawami', 'महानवमी', 'September-October', 'सेप्टेम्बर-अक्टोबर', 'Ninth day of Dashain', 'दशैँको नवौँ दिन'),
    ('Vijaya Dashami', 'विजया दशमी', 'September-October', 'सेप्टेम्बर-अक्टोबर', 'Tenth day of Dashain', 'दशैँको दशौँ दिन'),
    ('Kojagrat Purnima', 'कोजाग्रत पूर्णिमा', 'October', 'अक्टोबर', 'Last day of Dashain', 'दशैँको अन्तिम दिन'),
    ('Bhailo', 'भैलो', 'October-November', 'अक्टोबर-नोभेम्बर', 'Tihar song sung by girls', 'तिहारमा केटीहरूले गाउने गीत'),
    ('Deusi', 'देउसी', 'October-November', 'अक्टोबर-नोभेम्बर', 'Tihar song sung by boys', 'तिहारमा केटाहरूले गाउने गीत'),
    ('Laxmi Puja', 'लक्ष्मी पूजा', 'October-November', 'अक्टोबर-नोभेम्बर', 'Worship of Goddess Laxmi', 'देवी लक्ष्मीको पूजा'),
    ('Govardhan Puja', 'गोवर्धन पूजा', 'October-November', 'अक्टोबर-नोभेम्बर', 'Worship of Govardhan hill', 'गोवर्धन पर्वतको पूजा'),
    ('Bhai Tika', 'भाइटीका', 'October-November', 'अक्टोबर-नोभेम्बर', 'Festival of brothers and sisters', 'दाजुभाइ-दिदीबहिनीको पर्व'),
]
for (fn, fn_ne, when, when_ne, note, note_ne) in FESTIVALS:
    others = [f for f in FESTIVALS if f[0] != fn]
    rng.shuffle(others)
    em.emit(EX_ALL, 'Culture & Society', 'Festivals', 'easy', 2,
            f'When is {fn} celebrated?',
            f'{fn_ne} कहिले मनाइन्छ?',
            [when] + [o[2] for o in others[:3]], [when_ne] + [o[3] for o in others[:3]], 0,
            f'{fn} is celebrated in {when}.',
            f'{fn_ne} {when_ne} मा मनाइन्छ।')
    em.emit(EX_ALL, 'Culture & Society', 'Festivals', 'medium', 2,
            f'Which festival is known as {note}?',
            f'कुन पर्वलाई {note_ne} भनेर चिनिन्छ?',
            [fn] + [o[0] for o in others[:3]], [fn_ne] + [o[1] for o in others[:3]], 0,
            f'{fn} is known as {note}.',
            f'{fn_ne} लाई {note_ne} भनेर चिनिन्छ।')

# ---------------- Nepal firsts & symbols ----------------
FIRSTS = [
    ('first President of Nepal', 'नेपालका पहिलो राष्ट्रपति', 'Ram Baran Yadav', 'रामवरण यादव'),
    ('first Prime Minister of Nepal', 'नेपालका पहिलो प्रधानमन्त्री', 'Bhimsen Thapa', 'भीमसेन थापा'),
    ('first woman President of Nepal', 'नेपालकी पहिलो महिला राष्ट्रपति', 'Bidya Devi Bhandari', 'विद्यादेवी भण्डारी'),
    ('first woman Prime Minister of Nepal', 'नेपालकी पहिलो महिला प्रधानमन्त्री', 'Sushila Karki', 'सुशीला कार्की'),
    ('first woman Chief Justice of Nepal', 'नेपालकी पहिलो महिला प्रधानन्यायाधीश', 'Sushila Karki', 'सुशीला कार्की'),
    ('first woman Speaker of Nepal', 'नेपालकी पहिलो महिला सभामुख', 'Onsari Gharti Magar', 'ओनसरी घर्ती मगर'),
    ('first King of unified Nepal', 'एकीकृत नेपालका पहिलो राजा', 'Prithvi Narayan Shah', 'पृथ्वीनारायण शाह'),
    ('first Rana Prime Minister', 'पहिलो राणा प्रधानमन्त्री', 'Jung Bahadur Rana', 'जङ्गबहादुर राणा'),
    ('first elected Prime Minister', 'पहिलो निर्वाचित प्रधानमन्त्री', 'BP Koirala', 'बीपी कोइराला'),
    ('first Chief Justice of Nepal', 'नेपालका पहिलो प्रधानन्यायाधीश', 'Hari Prasad Pradhan', 'हरिप्रसाद प्रधान'),
    ('first Governor of Nepal Rastra Bank', 'नेपाल राष्ट्र बैंकका पहिलो गभर्नर', 'Himalaya Shumsher JBR', 'हिमालय शमशेर जबरा'),
    ('first Nepali to climb Mount Everest', 'सगरमाथा चढ्ने पहिलो नेपाली', 'Tenzing Norgay Sherpa', 'तेन्जिङ नोर्गे शेर्पा'),
    ('first woman to climb Mount Everest from Nepal', 'सगरमाथा चढ्ने पहिलो नेपाली महिला', 'Pasang Lhamu Sherpa', 'पासाङ ल्हामु शेर्पा'),
    ('first Nepali to summit all 14 eight-thousanders', '१४ वटै आठहजारी चुचुरा चढ्ने पहिलो नेपाली', 'Mingma Sherpa', 'मिङ्मा शेर्पा'),
    ('first newspaper of Nepal', 'नेपालको पहिलो पत्रिका', 'Gorkhapatra', 'गोरखापत्र'),
    ('first radio station of Nepal', 'नेपालको पहिलो रेडियो स्टेसन', 'Radio Nepal', 'रेडियो नेपाल'),
    ('first television channel of Nepal', 'नेपालको पहिलो टेलिभिजन च्यानल', 'Nepal Television', 'नेपाल टेलिभिजन'),
    ('first university of Nepal', 'नेपालको पहिलो विश्वविद्यालय', 'Tribhuvan University', 'त्रिभुवन विश्वविद्यालय'),
    ('first medical college of Nepal', 'नेपालको पहिलो मेडिकल कलेज', 'Institute of Medicine', 'चिकित्सा विज्ञान अध्ययन संस्थान'),
    ('first hydroelectric project of Nepal', 'नेपालको पहिलो जलविद्युत् आयोजना', 'Pharping', 'फर्पिङ'),
    ('first airport of Nepal', 'नेपालको पहिलो विमानस्थल', 'Tribhuvan International Airport', 'त्रिभुवन अन्तर्राष्ट्रिय विमानस्थल'),
    ('first airline of Nepal', 'नेपालको पहिलो एयरलाइन्स', 'Nepal Airlines', 'नेपाल एयरलाइन्स'),
    ('first bank of Nepal', 'नेपालको पहिलो बैंक', 'Nepal Bank Limited', 'नेपाल बैंक लिमिटेड'),
    ('first commercial bank of Nepal', 'नेपालको पहिलो वाणिज्य बैंक', 'Nepal Bank Limited', 'नेपाल बैंक लिमिटेड'),
    ('first development bank of Nepal', 'नेपालको पहिलो विकास बैंक', 'Nepal Industrial Development Corporation', 'नेपाल औद्योगिक विकास निगम'),
    ('first census of Nepal', 'नेपालको पहिलो जनगणना', '1911 AD', 'सन् १९११'),
    ('first National Assembly election', 'पहिलो राष्ट्रिय सभा निर्वाचन', '2018', 'सन् २०१८'),
    ('national animal of Nepal', 'नेपालको राष्ट्रिय जनावर', 'Cow', 'गाई'),
    ('national bird of Nepal', 'नेपालको राष्ट्रिय पन्छी', 'Danphe (Himalayan Monal)', 'डाँफे (हिमालयन मोनाल)'),
    ('national flower of Nepal', 'नेपालको राष्ट्रिय फूल', 'Laliguras (Rhododendron)', 'लालीगुराँस (रोडोडेन्ड्रन)'),
    ('national tree of Nepal', 'नेपालको राष्ट्रिय रुख', 'Laliguras (Rhododendron)', 'लालीगुराँस (रोडोडेन्ड्रन)'),
    ('national colour of Nepal', 'नेपालको राष्ट्रिय रङ', 'Crimson', 'सिम्रिक'),
    ('national sport of Nepal', 'नेपालको राष्ट्रिय खेल', 'Volleyball', 'भलिबल'),
    ('national language of Nepal', 'नेपालको राष्ट्रिय भाषा', 'Nepali', 'नेपाली'),
    ('national anthem of Nepal', 'नेपालको राष्ट्रिय गान', 'Sayaun Thunga Phool Ka', 'सयौँ थुङ्गा फूलका'),
    ('national flag shape of Nepal', 'नेपालको राष्ट्रिय झण्डाको आकार', 'Double-pennant (non-rectangular)', 'दोहोरो त्रिकोण (गैर-आयताकार)'),
    ('national motto of Nepal', 'नेपालको राष्ट्रिय आदर्श वाक्य', 'Janani Janmabhumishcha Swargadapi Gariyasi', 'जननी जन्मभूमिश्च स्वर्गादपि गरीयसी'),
    ('capital of Nepal', 'नेपालको राजधानी', 'Kathmandu', 'काठमाडौँ'),
    ('largest city of Nepal', 'नेपालको सबैभन्दा ठूलो सहर', 'Kathmandu', 'काठमाडौँ'),
    ('largest district of Nepal by area', 'क्षेत्रफलको हिसाबले नेपालको सबैभन्दा ठूलो जिल्ला', 'Dolpa', 'डोल्पा'),
    ('smallest district of Nepal by area', 'क्षेत्रफलको हिसाबले नेपालको सबैभन्दा सानो जिल्ला', 'Bhaktapur', 'भक्तपुर'),
    ('most populous district of Nepal', 'नेपालको सबैभन्दा धेरै जनसङ्ख्या भएको जिल्ला', 'Kathmandu', 'काठमाडौँ'),
    ('least populous district of Nepal', 'नेपालको सबैभन्दा कम जनसङ्ख्या भएको जिल्ला', 'Manang', 'मनाङ'),
    ('longest river of Nepal', 'नेपालको सबैभन्दा लामो नदी', 'Karnali', 'कर्णाली'),
    ('largest lake of Nepal', 'नेपालको सबैभन्दा ठूलो ताल', 'Rara', 'रारा'),
    ('highest lake of Nepal', 'नेपालको सबैभन्दा अग्लो ताल', 'Tilicho', 'तिलिचो'),
    ('deepest lake of Nepal', 'नेपालको सबैभन्दा गहिरो ताल', 'Shey Phoksundo', 'शे-फोक्सुण्डो'),
    ('longest highway of Nepal', 'नेपालको सबैभन्दा लामो राजमार्ग', 'Mahendra Highway', 'महेन्द्र राजमार्ग'),
    ('highest peak of Nepal', 'नेपालको सबैभन्दा अग्लो चुचुरो', 'Mount Everest', 'सगरमाथा'),
    ('oldest national park of Nepal', 'नेपालको सबैभन्दा पुरानो राष्ट्रिय निकुञ्ज', 'Chitwan National Park', 'चितवन राष्ट्रिय निकुञ्ज'),
    ('largest national park of Nepal', 'नेपालको सबैभन्दा ठूलो राष्ट्रिय निकुञ्ज', 'Shey Phoksundo National Park', 'शे-फोक्सुण्डो राष्ट्रिय निकुञ्ज'),
    ('smallest national park of Nepal', 'नेपालको सबैभन्दा सानो राष्ट्रिय निकुञ्ज', 'Shivapuri Nagarjun National Park', 'शिवपुरी नागार्जुन राष्ट्रिय निकुञ्ज'),
    ('first World Heritage Site of Nepal', 'नेपालको पहिलो विश्व सम्पदा स्थल', 'Kathmandu Valley', 'काठमाडौँ उपत्यका'),
    ('first Ramsar site of Nepal', 'नेपालको पहिलो रामसार स्थल', 'Koshi Tappu', 'कोशी टप्पु'),
]
for (q_en, q_ne, ans, ans_ne) in FIRSTS:
    others = [f for f in FIRSTS if f[0] != q_en]
    rng.shuffle(others)
    ds = [o[2] for o in others[:3]]
    dsn = [o[3] for o in others[:3]]
    if len({ans} | set(ds)) != 4 or len({ans_ne} | set(dsn)) != 4:
        continue
    em.emit(EX_ALL, 'Nepal Geography', 'Nepal Firsts & Symbols', 'easy', 2,
            f'Who/What is the {q_en}?',
            f'{q_ne} को हुन्/के हो?',
            [ans] + ds, [ans_ne] + dsn, 0,
            f'The {q_en} is {ans}.',
            f'{q_ne} {ans_ne} हो।')

n = em.write('expansion-r10-nepal-facts.json')
print('NEPAL FACTS TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:10]:
    print('  REJ', r)
