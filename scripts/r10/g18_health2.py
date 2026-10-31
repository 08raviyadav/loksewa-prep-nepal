#!/usr/bin/env python3
"""R10 generator 18: more medical facts (~800). Drug uses, disease organisms
& symptoms, normal lab values, first aid, nutrition, anatomy part 2,
public health programmes of Nepal."""
import sys, random
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter

bank = Bank()
em = Emitter(bank, 'R10-HEALTH2')
rng = random.Random(71110)

def F(exams, topic, sub, q, qn, a, an, d1, d1n, d2, d2n, d3, d3n):
    em.emit(exams, topic, sub, 'medium', 2, q, qn, [a, d1, d2, d3], [an, d1n, d2n, d3n], 0,
            f'The answer is {a}.', f'उत्तर {an} हो।')

HEALTH_EX = ['nmc-mbbs','nmc-bds','nhpc-ha','nhpc-lab','nhpc-public-health','nnc-rn','staff-nurse-psc','midwifery-nlem','npc-pharmacy','nhpc-ayurveda','nhpc-dental','nhpc-physio','nhpc-radio','nhpc-optometry','health']

# ---------------- normal values ----------------
VALS = [
    ('What is the normal body temperature?', 'सामान्य शरीरको तापक्रम कति हुन्छ?', '37°C (98.6°F)', '३७°से (९८.६°फा)', '36°C (96.8°F)', '३६°से (९६.८°फा)', '38°C (100.4°F)', '३८°से (१००.४°फा)', '39°C (102.2°F)', '३९°से (१०२.२°फा)'),
    ('What is the normal resting heart rate for an adult?', 'वयस्कको सामान्य विश्राम मुटुको धड्कन दर कति हुन्छ?', '60-100 beats per minute', 'प्रति मिनेट ६०-१०० धड्कन', '40-60 beats per minute', 'प्रति मिनेट ४०-६० धड्कन', '100-120 beats per minute', 'प्रति मिनेट १००-१२० धड्कन', '120-140 beats per minute', 'प्रति मिनेट १२०-१४० धड्कन'),
    ('What is the normal respiratory rate for an adult?', 'वयस्कको सामान्य श्वासप्रश्वास दर कति हुन्छ?', '12-20 breaths per minute', 'प्रति मिनेट १२-२० श्वास', '8-12 breaths per minute', 'प्रति मिनेट ८-१२ श्वास', '20-30 breaths per minute', 'प्रति मिनेट २०-३० श्वास', '30-40 breaths per minute', 'प्रति मिनेट ३०-४० श्वास'),
    ('What is the normal blood pressure for an adult?', 'वयस्कको सामान्य रक्तचाप कति हुन्छ?', '120/80 mmHg', '१२०/८० मिमिHg', '140/90 mmHg', '१४०/९० मिमिHg', '100/60 mmHg', '१००/६० मिमिHg', '160/100 mmHg', '१६०/१०० मिमिHg'),
    ('What is the normal fasting blood sugar level?', 'सामान्य खाली पेटको रगतमा चिनीको मात्रा कति हुन्छ?', '70-100 mg/dL', '७०-१०० मिग्रा/डिएल', '100-125 mg/dL', '१००-१२५ मिग्रा/डिएल', '126-150 mg/dL', '१२६-१५० मिग्रा/डिएल', '50-70 mg/dL', '५०-७० मिग्रा/डिएल'),
    ('What is the normal haemoglobin level for an adult man?', 'वयस्क पुरुषको सामान्य हिमोग्लोबिन मात्रा कति हुन्छ?', '13.5-17.5 g/dL', '१३.५-१७.५ ग्रा/डिएल', '12-15.5 g/dL', '१२-१५.५ ग्रा/डिएल', '10-12 g/dL', '१०-१२ ग्रा/डिएल', '18-20 g/dL', '१८-२० ग्रा/डिएल'),
    ('What is the normal haemoglobin level for an adult woman?', 'वयस्क महिलाको सामान्य हिमोग्लोबिन मात्रा कति हुन्छ?', '12-15.5 g/dL', '१२-१५.५ ग्रा/डिएल', '13.5-17.5 g/dL', '१३.५-१७.५ ग्रा/डिएल', '10-12 g/dL', '१०-१२ ग्रा/डिएल', '16-18 g/dL', '१६-१८ ग्रा/डिएल'),
    ('What is the normal platelet count?', 'सामान्य प्लेटलेट सङ्ख्या कति हुन्छ?', '150,000-400,000 per microlitre', 'प्रति माइक्रोलिटर १,५०,०००-४,००,०००', '50,000-100,000 per microlitre', 'प्रति माइक्रोलिटर ५०,०००-१,००,०००', '400,000-600,000 per microlitre', 'प्रति माइक्रोलिटर ४,००,०००-६,००,०००', '100,000-150,000 per microlitre', 'प्रति माइक्रोलिटर १,००,०००-१,५०,०००'),
    ('What is the normal total WBC count?', 'सामान्य कुल श्वेत रक्तकोशिका सङ्ख्या कति हुन्छ?', '4,000-11,000 per microlitre', 'प्रति माइक्रोलिटर ४,०००-११,०००', '1,000-4,000 per microlitre', 'प्रति माइक्रोलिटर १,०००-४,०००', '11,000-15,000 per microlitre', 'प्रति माइक्रोलिटर ११,०००-१५,०००', '15,000-20,000 per microlitre', 'प्रति माइक्रोलिटर १५,०००-२०,०००'),
    ('What is the normal total RBC count for an adult man?', 'वयस्क पुरुषको सामान्य कुल रातो रक्तकोशिका सङ्ख्या कति हुन्छ?', '4.5-5.5 million per microlitre', 'प्रति माइक्रोलिटर ४.५-५.५ मिलियन', '3.5-4.5 million per microlitre', 'प्रति माइक्रोलिटर ३.५-४.५ मिलियन', '5.5-6.5 million per microlitre', 'प्रति माइक्रोलिटर ५.५-६.५ मिलियन', '2.5-3.5 million per microlitre', 'प्रति माइक्रोलिटर २.५-३.५ मिलियन'),
    ('What is the normal serum sodium level?', 'सामान्य सीरम सोडियम मात्रा कति हुन्छ?', '135-145 mEq/L', '१३५-१४५ मिक्वि/लि', '120-130 mEq/L', '१२०-१३० मिक्वि/लि', '145-155 mEq/L', '१४५-१५५ मिक्वि/लि', '110-120 mEq/L', '११०-१२० मिक्वि/लि'),
    ('What is the normal serum potassium level?', 'सामान्य सीरम पोटासियम मात्रा कति हुन्छ?', '3.5-5.0 mEq/L', '३.५-५.० मिक्वि/लि', '2.5-3.5 mEq/L', '२.५-३.५ मिक्वि/लि', '5.0-6.0 mEq/L', '५.०-६.० मिक्वि/लि', '6.0-7.0 mEq/L', '६.०-७.० मिक्वि/लि'),
    ('What is the normal serum calcium level?', 'सामान्य सीरम क्याल्सियम मात्रा कति हुन्छ?', '8.5-10.5 mg/dL', '८.५-१०.५ मिग्रा/डिएल', '6.5-8.5 mg/dL', '६.५-८.५ मिग्रा/डिएल', '10.5-12.5 mg/dL', '१०.५-१२.५ मिग्रा/डिएल', '5.5-7.5 mg/dL', '५.५-७.५ मिग्रा/डिएल'),
    ('What is the normal blood pH?', 'सामान्य रगतको pH कति हुन्छ?', '7.35-7.45', '७.३५-७.४५', '7.0-7.2', '७.०-७.२', '7.45-7.6', '७.४५-७.६', '6.8-7.0', '६.८-७.०'),
    ('What is the normal urine pH?', 'सामान्य पिसाबको pH कति हुन्छ?', '4.5-8.0', '४.५-८.०', '7.35-7.45', '७.३५-७.४५', '1.0-2.0', '१.०-२.०', '8.0-9.0', '८.०-९.०'),
    ('What is the normal total cholesterol level?', 'सामान्य कुल कोलेस्टेरोल मात्रा कति हुन्छ?', 'Less than 200 mg/dL', '२०० मिग्रा/डिएल भन्दा कम', '200-240 mg/dL', '२००-२४० मिग्रा/डिएल', 'More than 240 mg/dL', '२४० मिग्रा/डिएल भन्दा बढी', 'Less than 100 mg/dL', '१०० मिग्रा/डिएल भन्दा कम'),
    ('What is the normal duration of pregnancy?', 'सामान्य गर्भावस्थाको अवधि कति हुन्छ?', '40 weeks', '४० हप्ता', '36 weeks', '३६ हप्ता', '42 weeks', '४२ हप्ता', '38 weeks', '३८ हप्ता'),
    ('What is the normal birth weight of a newborn?', 'नवजात शिशुको सामान्य जन्म तौल कति हुन्छ?', '2.5-4.0 kg', '२.५-४.० केजी', '1.5-2.5 kg', '१.५-२.५ केजी', '4.0-5.0 kg', '४.०-५.० केजी', '1.0-2.0 kg', '१.०-२.० केजी'),
    ('At what age do babies usually start walking?', 'शिशुहरू सामान्यतया कुन उमेरमा हिँड्न थाल्छन्?', '12 months', '१२ महिना', '6 months', '६ महिना', '18 months', '१८ महिना', '24 months', '२४ महिना'),
    ('At what age do babies usually start speaking first words?', 'शिशुहरू सामान्यतया कुन उमेरमा पहिलो शब्द बोल्न थाल्छन्?', '12 months', '१२ महिना', '6 months', '६ महिना', '18 months', '१८ महिना', '24 months', '२४ महिना'),
]
for r in VALS:
    F(HEALTH_EX, 'Health/Technical basics', 'Normal Values', *r)

# ---------------- drug uses ----------------
DRUGS = [
    ('Paracetamol is used as a/an', 'प्यारासिटामोल के रूपमा प्रयोग गरिन्छ?', 'Antipyretic and analgesic', 'ज्वरो घटाउने र दुखाइ कम गर्ने', 'Antibiotic', 'एन्टिबायोटिक', 'Antacid', 'एन्टासिड', 'Antihistamine', 'एन्टिहिस्टामिन'),
    ('Amoxicillin is a type of', 'एमोक्सिसिलिन कुन प्रकारको औषधि हो?', 'Antibiotic', 'एन्टिबायोटिक', 'Antipyretic', 'ज्वरो घटाउने', 'Antacid', 'एन्टासिड', 'Antiviral', 'एन्टिभाइरल'),
    ('ORS stands for', 'ORS को पूरा रूप के हो?', 'Oral Rehydration Salts', 'ओरल रिहाइड्रेसन साल्ट्स', 'Oral Rehydration Solution', 'ओरल रिहाइड्रेसन सोलुसन', 'Oral Recovery Salts', 'ओरल रिकभरी साल्ट्स', 'Oral Rehydration Syrup', 'ओरल रिहाइड्रेसन सिरप'),
    ('ORS is used to treat', 'ORS के उपचार गर्न प्रयोग गरिन्छ?', 'Dehydration due to diarrhoea', 'झाडापखलाको कारणले भएको निर्जलीकरण', 'Fever', 'ज्वरो', 'Cough', 'खोकी', 'Malaria', 'मलेरिया'),
    ('Which drug is used to treat malaria?', 'मलेरिया उपचार गर्न कुन औषधि प्रयोग गरिन्छ?', 'Chloroquine', 'क्लोरोक्विन', 'Paracetamol', 'प्यारासिटामोल', 'Amoxicillin', 'एमोक्सिसिलिन', 'Omeprazole', 'ओमेप्राजोल'),
    ('Which drug is used to treat tuberculosis?', 'क्षयरोग उपचार गर्न कुन औषधि प्रयोग गरिन्छ?', 'Isoniazid', 'आइसोनियाजिड', 'Paracetamol', 'प्यारासिटामोल', 'Chloroquine', 'क्लोरोक्विन', 'Omeprazole', 'ओमेप्राजोल'),
    ('Which drug is used to reduce stomach acid?', 'पेटको एसिड घटाउन कुन औषधि प्रयोग गरिन्छ?', 'Omeprazole', 'ओमेप्राजोल', 'Paracetamol', 'प्यारासिटामोल', 'Amoxicillin', 'एमोक्सिसिलिन', 'Chloroquine', 'क्लोरोक्विन'),
    ('Which drug is used to treat allergy?', 'एलर्जी उपचार गर्न कुन औषधि प्रयोग गरिन्छ?', 'Cetirizine', 'सेटिरिजिन', 'Paracetamol', 'प्यारासिटामोल', 'Omeprazole', 'ओमेप्राजोल', 'Amoxicillin', 'एमोक्सिसिलिन'),
    ('Which drug is used to treat diabetes?', 'मधुमेह उपचार गर्न कुन औषधि प्रयोग गरिन्छ?', 'Metformin', 'मेटफर्मिन', 'Paracetamol', 'प्यारासिटामोल', 'Omeprazole', 'ओमेप्राजोल', 'Cetirizine', 'सेटिरिजिन'),
    ('Which drug is used to treat high blood pressure?', 'उच्च रक्तचाप उपचार गर्न कुन औषधि प्रयोग गरिन्छ?', 'Amlodipine', 'एम्लोडिपिन', 'Paracetamol', 'प्यारासिटामोल', 'Metformin', 'मेटफर्मिन', 'Omeprazole', 'ओमेप्राजोल'),
    ('Which drug is used as a painkiller?', 'दुखाइ कम गर्न कुन औषधि प्रयोग गरिन्छ?', 'Ibuprofen', 'आइबुप्रोफेन', 'Omeprazole', 'ओमेप्राजोल', 'Cetirizine', 'सेटिरिजिन', 'Metformin', 'मेटफर्मिन'),
    ('Which drug is used to treat worm infestation?', 'जुकाको सङ्क्रमण उपचार गर्न कुन औषधि प्रयोग गरिन्छ?', 'Albendazole', 'अल्बेन्डाजोल', 'Paracetamol', 'प्यारासिटामोल', 'Amoxicillin', 'एमोक्सिसिलिन', 'Chloroquine', 'क्लोरोक्विन'),
    ('Which drug is used to treat fungal infection?', 'ढुसी सङ्क्रमण उपचार गर्न कुन औषधि प्रयोग गरिन्छ?', 'Fluconazole', 'फ्लुकोनाजोल', 'Amoxicillin', 'एमोक्सिसिलिन', 'Paracetamol', 'प्यारासिटामोल', 'Cetirizine', 'सेटिरिजिन'),
    ('Which drug is used to treat HIV?', 'एचआईभी उपचार गर्न कुन औषधि प्रयोग गरिन्छ?', 'Antiretroviral drugs', 'एन्टिरेट्रोभाइरल औषधि', 'Antibiotics', 'एन्टिबायोटिक', 'Antipyretics', 'ज्वरो घटाउने औषधि', 'Antacids', 'एन्टासिड'),
    ('Which vaccine is given to prevent tuberculosis?', 'क्षयरोग रोक्न कुन खोप दिइन्छ?', 'BCG', 'बीसीजी', 'DPT', 'डीपीटी', 'Measles', 'दादुरा', 'Polio', 'पोलियो'),
    ('Which vaccine is given to prevent measles?', 'दादुरा रोक्न कुन खोप दिइन्छ?', 'Measles vaccine', 'दादुरा खोप', 'BCG', 'बीसीजी', 'DPT', 'डीपीटी', 'Polio', 'पोलियो'),
    ('Which vaccine is given to prevent polio?', 'पोलियो रोक्न कुन खोप दिइन्छ?', 'OPV/IPV', 'ओपीभी/आईपीभी', 'BCG', 'बीसीजी', 'DPT', 'डीपीटी', 'Measles', 'दादुरा'),
    ('Which vaccine is given to prevent hepatitis B?', 'हेपाटाइटिस बी रोक्न कुन खोप दिइन्छ?', 'Hepatitis B vaccine', 'हेपाटाइटिस बी खोप', 'BCG', 'बीसीजी', 'DPT', 'डीपीटी', 'Measles', 'दादुरा'),
    ('Which vaccine is given at birth in Nepal?', 'नेपालमा जन्मँदा कुन खोप दिइन्छ?', 'BCG and OPV-0', 'बीसीजी र ओपीभी-०', 'DPT', 'डीपीटी', 'Measles', 'दादुरा', 'JE', 'जेई'),
    ('What is the full form of DPT?', 'DPT को पूरा रूप के हो?', 'Diphtheria, Pertussis and Tetanus', 'डिप्थेरिया, पर्टुसिस र टिटानस', 'Diphtheria, Polio and Tetanus', 'डिप्थेरिया, पोलियो र टिटानस', 'Diarrhoea, Pertussis and Tetanus', 'झाडापखला, पर्टुसिस र टिटानस', 'Diphtheria, Pneumonia and Tetanus', 'डिप्थेरिया, निमोनिया र टिटानस'),
    ('What is the full form of BCG?', 'BCG को पूरा रूप के हो?', 'Bacillus Calmette-Guerin', 'ब्यासिलस काल्मेट-गुएरिन', 'Bacillus Calmette-Guillain', 'ब्यासिलस काल्मेट-गुइलेन', 'Bacterial Calmette-Guerin', 'ब्याक्टेरियल काल्मेट-गुएरिन', 'Bacillus Cholera-Guerin', 'ब्यासिलस कोलेरा-गुएरिन'),
    ('What is the full form of OPV?', 'OPV को पूरा रूप के हो?', 'Oral Polio Vaccine', 'ओरल पोलियो खोप', 'Oral Pneumonia Vaccine', 'ओरल निमोनिया खोप', 'Oral Pertussis Vaccine', 'ओरल पर्टुसिस खोप', 'Oral Polio Virus', 'ओरल पोलियो भाइरस'),
    ('What is the full form of IPV?', 'IPV को पूरा रूप के हो?', 'Inactivated Polio Vaccine', 'इनएक्टिभेटेड पोलियो खोप', 'Injectable Polio Vaccine', 'इन्जेक्टेबल पोलियो खोप', 'Inactivated Pneumonia Vaccine', 'इनएक्टिभेटेड निमोनिया खोप', 'Injectable Pertussis Vaccine', 'इन्जेक्टेबल पर्टुसिस खोप'),
    ('What is the full form of TT?', 'TT को पूरा रूप के हो?', 'Tetanus Toxoid', 'टिटानस टक्सोइड', 'Tetanus Treatment', 'टिटानस उपचार', 'Tetanus Tablet', 'टिटानस ट्याब्लेट', 'Tetanus Test', 'टिटानस परीक्षण'),
    ('What is the full form of JE?', 'JE को पूरा रूप के हो?', 'Japanese Encephalitis', 'जापानी इन्सेफलाइटिस', 'Joint Encephalitis', 'जोइन्ट इन्सेफलाइटिस', 'Japanese Enteritis', 'जापानी इन्टराइटिस', 'Juvenile Encephalitis', 'जुभेनाइल इन्सेफलाइटिस'),
    ('What is the full form of MR?', 'MR को पूरा रूप के हो?', 'Measles-Rubella', 'दादुरा-रुबेला', 'Measles-Rabies', 'दादुरा-रेबिज', 'Malaria-Rubella', 'मलेरिया-रुबेला', 'Measles-Rickets', 'दादुरा-रिकेट्स'),
    ('What is the full form of Td?', 'Td को पूरा रूप के हो?', 'Tetanus-diphtheria', 'टिटानस-डिप्थेरिया', 'Tetanus-diarrhoea', 'टिटानस-झाडापखला', 'Tetanus-dengue', 'टिटानस-डेङ्गु', 'Tetanus-diabetes', 'टिटानस-मधुमेह'),
]
for r in DRUGS:
    F(HEALTH_EX, 'Health/Technical basics', 'Drugs & Vaccines', *r)

# ---------------- diseases & symptoms ----------------
DIS = [
    ('Which disease is characterised by high blood sugar?', 'कुन रोगमा रगतमा चिनीको मात्रा बढ्छ?', 'Diabetes mellitus', 'मधुमेह', 'Hypertension', 'उच्च रक्तचाप', 'Anaemia', 'रक्तअल्पता', 'Hypothyroidism', 'हाइपोथाइराइडिज्म'),
    ('Which disease is characterised by high blood pressure?', 'कुन रोगमा रक्तचाप बढ्छ?', 'Hypertension', 'उच्च रक्तचाप', 'Diabetes mellitus', 'मधुमेह', 'Anaemia', 'रक्तअल्पता', 'Asthma', 'दमा'),
    ('Which disease is characterised by low haemoglobin?', 'कुन रोगमा हिमोग्लोबिन कम हुन्छ?', 'Anaemia', 'रक्तअल्पता', 'Diabetes mellitus', 'मधुमेह', 'Hypertension', 'उच्च रक्तचाप', 'Asthma', 'दमा'),
    ('Which disease is characterised by difficulty in breathing and wheezing?', 'कुन रोगमा सास फेर्न गाह्रो हुन्छ र घरघराहट हुन्छ?', 'Asthma', 'दमा', 'Diabetes mellitus', 'मधुमेह', 'Hypertension', 'उच्च रक्तचाप', 'Anaemia', 'रक्तअल्पता'),
    ('Which disease is caused by the deficiency of iodine?', 'आयोडिनको कमीले कुन रोग लाग्छ?', 'Goitre', 'गलगाँड', 'Anaemia', 'रक्तअल्पता', 'Rickets', 'रिकेट्स', 'Scurvy', 'स्कर्भी'),
    ('Which disease is caused by the deficiency of iron?', 'फलामको कमीले कुन रोग लाग्छ?', 'Anaemia', 'रक्तअल्पता', 'Goitre', 'गलगाँड', 'Rickets', 'रिकेट्स', 'Scurvy', 'स्कर्भी'),
    ('Which disease is caused by the deficiency of vitamin D?', 'भिटामिन डीको कमीले कुन रोग लाग्छ?', 'Rickets', 'रिकेट्स', 'Scurvy', 'स्कर्भी', 'Beriberi', 'बेरीबेरी', 'Goitre', 'गलगाँड'),
    ('Which disease is caused by the deficiency of vitamin C?', 'भिटामिन सीको कमीले कुन रोग लाग्छ?', 'Scurvy', 'स्कर्भी', 'Rickets', 'रिकेट्स', 'Beriberi', 'बेरीबेरी', 'Anaemia', 'रक्तअल्पता'),
    ('Which disease is caused by the deficiency of vitamin B1?', 'भिटामिन बी१ को कमीले कुन रोग लाग्छ?', 'Beriberi', 'बेरीबेरी', 'Scurvy', 'स्कर्भी', 'Rickets', 'रिकेट्स', 'Pellagra', 'पेलाग्रा'),
    ('Which disease is caused by the deficiency of vitamin B3 (niacin)?', 'भिटामिन बी३ (नियासिन) को कमीले कुन रोग लाग्छ?', 'Pellagra', 'पेलाग्रा', 'Beriberi', 'बेरीबेरी', 'Scurvy', 'स्कर्भी', 'Rickets', 'रिकेट्स'),
    ('Which disease is caused by the deficiency of vitamin A?', 'भिटामिन ए को कमीले कुन रोग लाग्छ?', 'Night blindness', 'रतन्धो', 'Scurvy', 'स्कर्भी', 'Rickets', 'रिकेट्स', 'Beriberi', 'बेरीबेरी'),
    ('Which disease is transmitted by the bite of a dog?', 'कुकुरको टोकाइले कुन रोग सर्छ?', 'Rabies', 'रेबिज', 'Malaria', 'मलेरिया', 'Dengue', 'डेङ्गु', 'Cholera', 'हैजा'),
    ('Which disease is transmitted through contaminated water?', 'दूषित पानीबाट कुन रोग सर्छ?', 'Cholera', 'हैजा', 'Rabies', 'रेबिज', 'Malaria', 'मलेरिया', 'AIDS', 'एड्स'),
    ('Which disease is transmitted through sexual contact?', 'यौन सम्पर्कबाट कुन रोग सर्छ?', 'AIDS', 'एड्स', 'Cholera', 'हैजा', 'Malaria', 'मलेरिया', 'Rabies', 'रेबिज'),
    ('Which disease is transmitted through air (droplets)?', 'हावाबाट (थुकका छिटा) कुन रोग सर्छ?', 'Tuberculosis', 'क्षयरोग', 'Cholera', 'हैजा', 'Malaria', 'मलेरिया', 'AIDS', 'एड्स'),
    ('Which disease is caused by the bite of a sandfly?', 'बालुवा झिँगाको टोकाइले कुन रोग लाग्छ?', 'Kala-azar', 'कालाजार', 'Malaria', 'मलेरिया', 'Dengue', 'डेङ्गु', 'Filaria', 'फाइलेरिया'),
    ('Which disease is caused by the bite of a Culex mosquito?', 'क्युलेक्स लामखुट्टेको टोकाइले कुन रोग लाग्छ?', 'Filaria', 'फाइलेरिया', 'Malaria', 'मलेरिया', 'Dengue', 'डेङ्गु', 'Kala-azar', 'कालाजार'),
    ('Which disease is known as the "white plague"?', 'कुन रोगलाई "सेतो महामारी" भनिन्छ?', 'Tuberculosis', 'क्षयरोग', 'Cholera', 'हैजा', 'Malaria', 'मलेरिया', 'Leprosy', 'कुष्ठरोग'),
    ('Which disease is known as Hansen\'s disease?', 'कुन रोगलाई हेन्सेन रोग भनिन्छ?', 'Leprosy', 'कुष्ठरोग', 'Tuberculosis', 'क्षयरोग', 'Cholera', 'हैजा', 'Malaria', 'मलेरिया'),
    ('Which disease is known as "lockjaw"?', 'कुन रोगलाई "बङ्गारा बन्द हुने रोग" भनिन्छ?', 'Tetanus', 'टिटानस', 'Rabies', 'रेबिज', 'Diphtheria', 'डिप्थेरिया', 'Pertussis', 'पर्टुसिस'),
    ('Which disease is known as "whooping cough"?', 'कुन रोगलाई "लहरे खोकी" भनिन्छ?', 'Pertussis', 'पर्टुसिस', 'Tetanus', 'टिटानस', 'Diphtheria', 'डिप्थेरिया', 'Tuberculosis', 'क्षयरोग'),
    ('Which disease is known as "black death"?', 'कुन रोगलाई "कालो मृत्यु" भनिन्छ?', 'Plague', 'प्लेग', 'Cholera', 'हैजा', 'Malaria', 'मलेरिया', 'Smallpox', 'बिफर'),
    ('Which disease has been eradicated from the world?', 'कुन रोग विश्वबाट उन्मूलन भएको छ?', 'Smallpox', 'बिफर', 'Polio', 'पोलियो', 'Measles', 'दादुरा', 'Malaria', 'मलेरिया'),
    ('In which year was smallpox declared eradicated?', 'बिफर उन्मूलन भएको कुन वर्ष घोषणा गरियो?', '1980', 'सन् १९८०', '1978', 'सन् १९७८', '1985', 'सन् १९८५', '1990', 'सन् १९९०'),
    ('Which disease is caused by the Ebola virus?', 'इबोला भाइरसले कुन रोग गराउँछ?', 'Ebola virus disease', 'इबोला भाइरस रोग', 'AIDS', 'एड्स', 'Dengue', 'डेङ्गु', 'Malaria', 'मलेरिया'),
    ('Which disease is caused by the Zika virus?', 'जिका भाइरसले कुन रोग गराउँछ?', 'Zika virus disease', 'जिका भाइरस रोग', 'Dengue', 'डेङ्गु', 'Malaria', 'मलेरिया', 'Chikungunya', 'चिकुनगुनिया'),
    ('Which disease is caused by the Nipah virus?', 'निपाह भाइरसले कुन रोग गराउँछ?', 'Nipah virus infection', 'निपाह भाइरस सङ्क्रमण', 'Rabies', 'रेबिज', 'Dengue', 'डेङ्गु', 'Malaria', 'मलेरिया'),
    ('Which disease is caused by the H1N1 virus?', 'H1N1 भाइरसले कुन रोग गराउँछ?', 'Swine flu', 'स्वाइन फ्लु', 'Bird flu', 'बर्ड फ्लु', 'Dengue', 'डेङ्गु', 'Malaria', 'मलेरिया'),
    ('Which disease is caused by the H5N1 virus?', 'H5N1 भाइरसले कुन रोग गराउँछ?', 'Bird flu', 'बर्ड फ्लु', 'Swine flu', 'स्वाइन फ्लु', 'Dengue', 'डेङ्गु', 'Malaria', 'मलेरिया'),
    ('Which disease is caused by the SARS-CoV-2 virus?', 'SARS-CoV-2 भाइरसले कुन रोग गराउँछ?', 'COVID-19', 'कोभिड-१९', 'SARS', 'सार्स', 'MERS', 'मर्स', 'Influenza', 'इन्फ्लुएन्जा'),
    ('In which year was COVID-19 declared a pandemic by the WHO?', 'विश्व स्वास्थ्य सङ्गठनले कोभिड-१९ लाई महामारी कुन वर्ष घोषणा गर्यो?', '2020', 'सन् २०२०', '2019', 'सन् २०१९', '2021', 'सन् २०२१', '2022', 'सन् २०२२'),
    ('Which disease is caused by the deficiency of protein?', 'प्रोटिनको कमीले कुन रोग लाग्छ?', 'Kwashiorkor', 'क्वासियोरकर', 'Marasmus', 'मरास्मस', 'Rickets', 'रिकेट्स', 'Scurvy', 'स्कर्भी'),
    ('Which disease is caused by the deficiency of protein and calories?', 'प्रोटिन र क्यालोरीको कमीले कुन रोग लाग्छ?', 'Marasmus', 'मरास्मस', 'Kwashiorkor', 'क्वासियोरकर', 'Rickets', 'रिकेट्स', 'Scurvy', 'स्कर्भी'),
    ('Which disease is characterised by a swollen belly and oedema in children?', 'कुन रोगमा बालबालिकाको पेट फुल्छ र सुन्निन्छ?', 'Kwashiorkor', 'क्वासियोरकर', 'Marasmus', 'मरास्मस', 'Rickets', 'रिकेट्स', 'Anaemia', 'रक्तअल्पता'),
    ('Which disease is characterised by severe wasting in children?', 'कुन रोगमा बालबालिका अत्यन्त दुब्लाउँछन्?', 'Marasmus', 'मरास्मस', 'Kwashiorkor', 'क्वासियोरकर', 'Rickets', 'रिकेट्स', 'Scurvy', 'स्कर्भी'),
]
for r in DIS:
    F(HEALTH_EX, 'Health/Technical basics', 'Diseases', *r)

# ---------------- first aid ----------------
FA = [
    ('What is the first aid for a burn?', 'पोलेकोमा प्राथमिक उपचार के हो?', 'Cool the burn with running water', 'बगिरहेको पानीले पोलेको ठाउँ चिसो पार्नु', 'Apply ice directly', 'सिधै बरफ लगाउनु', 'Apply toothpaste', 'टुथपेस्ट लगाउनु', 'Cover with a blanket', 'कम्बलले छोप्नु'),
    ('What is the first aid for a snake bite?', 'सर्पले टोकेकोमा प्राथमिक उपचार के हो?', 'Keep the victim calm and immobilise the limb', 'पीडितलाई शान्त राख्नु र अङ्ग नचलाउनु', 'Suck out the venom', 'विष चुस्नु', 'Apply a tight tourniquet', 'कडा बाँध्नु', 'Cut the wound', 'घाउ काट्नु'),
    ('What is the first aid for a nosebleed?', 'नाकबाट रगत बगेकोमा प्राथमिक उपचार के हो?', 'Pinch the soft part of the nose and lean forward', 'नाकको नरम भाग थिच्नु र अगाडि झुक्नु', 'Lean the head back', 'टाउको पछाडि ढल्काउनु', 'Blow the nose hard', 'नाक जोडले पुछ्नु', 'Lie flat', 'सिधा सुत्नु'),
    ('What is the first aid for choking?', 'निसास्सिएकोमा प्राथमिक उपचार के हो?', 'Perform the Heimlich manoeuvre', 'हेमलिच युक्ति गर्नु', 'Give water to drink', 'पानी पिउन दिनु', 'Pat the back hard', 'पिठ्युँमा जोडले थपथपाउनु', 'Lie the person down', 'व्यक्तिलाई सुताउनु'),
    ('What is the first aid for a fracture?', 'हाड भाँचिएकोमा प्राथमिक उपचार के हो?', 'Immobilise the limb with a splint', 'स्प्लिन्टले अङ्ग स्थिर पार्नु', 'Move the limb to check', 'जाँच्न अङ्ग चलाउनु', 'Massage the area', 'ठाउँ मसाज गर्नु', 'Apply heat', 'तातो लगाउनु'),
    ('What is the first aid for a person who has fainted?', 'बेहोस भएको व्यक्तिको प्राथमिक उपचार के हो?', 'Lay the person on their back and raise the legs', 'व्यक्तिलाई पिठ्युँ फर्काएर सुताउनु र खुट्टा उठाउनु', 'Give water immediately', 'तुरुन्त पानी दिनु', 'Shake the person', 'व्यक्तिलाई हल्लाउनु', 'Stand the person up', 'व्यक्तिलाई उभ्याउनु'),
    ('What is the full form of CPR?', 'CPR को पूरा रूप के हो?', 'Cardiopulmonary Resuscitation', 'कार्डियोपल्मोनरी रिससिटेसन', 'Cardiac Pulmonary Rescue', 'कार्डियाक पल्मोनरी रेस्क्यु', 'Cardio Pulmonary Recovery', 'कार्डियो पल्मोनरी रिकभरी', 'Central Pulmonary Resuscitation', 'सेन्ट्रल पल्मोनरी रिससिटेसन'),
    ('What is the ratio of chest compressions to rescue breaths in CPR for adults?', 'वयस्कमा CPR मा छाती थिच्ने र श्वास दिने अनुपात कति हुन्छ?', '30:2', '३०:२', '15:2', '१५:२', '30:1', '३०:१', '15:1', '१५:१'),
    ('How deep should chest compressions be in adult CPR?', 'वयस्क CPR मा छाती कति गहिरो थिच्नुपर्छ?', '5-6 cm', '५-६ सेमी', '2-3 cm', '२-३ सेमी', '8-10 cm', '८-१० सेमी', '1-2 cm', '१-२ सेमी'),
    ('How fast should chest compressions be in CPR?', 'CPR मा छाती कति छिटो थिच्नुपर्छ?', '100-120 per minute', 'प्रति मिनेट १००-१२०', '60-80 per minute', 'प्रति मिनेट ६०-८०', '140-160 per minute', 'प्रति मिनेट १४०-१६०', '80-100 per minute', 'प्रति मिनेट ८०-१००'),
    ('What is the first aid for a dog bite?', 'कुकुरले टोकेकोमा प्राथमिक उपचार के हो?', 'Wash the wound with soap and water', 'घाउ साबुनपानीले धुनु', 'Apply chilli powder', 'खुर्सानीको धुलो लगाउनु', 'Cover with mud', 'माटोले छोप्नु', 'Tie a tight band', 'कडा बाँध्नु'),
    ('What is the first aid for an electric shock?', 'विद्युत् झट्का लागेकोमा प्राथमिक उपचार के हो?', 'Switch off the power before touching the victim', 'पीडितलाई छुनुअघि बिजुली बन्द गर्नु', 'Pull the victim with bare hands', 'खाली हातले पीडितलाई तान्नु', 'Pour water on the victim', 'पीडितमाथि पानी खन्याउनु', 'Give the victim water', 'पीडितलाई पानी दिनु'),
    ('What is the first aid for a person who has swallowed poison?', 'विष निलेको व्यक्तिको प्राथमिक उपचार के हो?', 'Do not induce vomiting; seek medical help immediately', 'बान्ता नगराउनु; तुरुन्त चिकित्सा सहायता खोज्नु', 'Give milk to drink', 'दूध पिउन दिनु', 'Induce vomiting immediately', 'तुरुन्त बान्ता गराउनु', 'Give alcohol to drink', 'रक्सी पिउन दिनु'),
    ('What is the first aid for a heat stroke?', 'तातो हावा (हीट स्ट्रोक) लागेकोमा प्राथमिक उपचार के हो?', 'Move the person to a cool place and cool the body', 'व्यक्तिलाई चिसो ठाउँमा लैजानु र शरीर चिसो पार्नु', 'Give hot tea', 'तातो चिया दिनु', 'Cover with a blanket', 'कम्बलले छोप्नु', 'Give alcohol', 'रक्सी दिनु'),
    ('What is the first aid for hypothermia?', 'हाइपोथर्मिया (शरीर चिसो) भएकोमा प्राथमिक उपचार के हो?', 'Warm the person gradually with blankets', 'कम्बलले बिस्तारै व्यक्तिलाई न्यानो पार्नु', 'Give a cold bath', 'चिसो पानीले नुहाउनु', 'Give alcohol', 'रक्सी दिनु', 'Rub the skin with snow', 'हिउँले छाला रगड्नु'),
]
for r in FA:
    F(HEALTH_EX, 'Health/Technical basics', 'First Aid', *r)

# ---------------- nutrition ----------------
NUT = [
    ('Which food is the richest source of vitamin C?', 'भिटामिन सीको सबैभन्दा धनी स्रोत कुन खाना हो?', 'Amla (Indian gooseberry)', 'अमला', 'Banana', 'केरा', 'Rice', 'चामल', 'Potato', 'आलु'),
    ('Which food is the richest source of iron?', 'फलामको सबैभन्दा धनी स्रोत कुन खाना हो?', 'Green leafy vegetables', 'हरियो सागपात', 'Rice', 'चामल', 'Banana', 'केरा', 'Milk', 'दूध'),
    ('Which food is the richest source of calcium?', 'क्याल्सियमको सबैभन्दा धनी स्रोत कुन खाना हो?', 'Milk and dairy products', 'दूध र दुग्धजन्य पदार्थ', 'Rice', 'चामल', 'Banana', 'केरा', 'Potato', 'आलु'),
    ('Which food is the richest source of protein?', 'प्रोटिनको सबैभन्दा धनी स्रोत कुन खाना हो?', 'Egg', 'अण्डा', 'Rice', 'चामल', 'Banana', 'केरा', 'Potato', 'आलु'),
    ('Which food is the richest source of vitamin A?', 'भिटामिन ए को सबैभन्दा धनी स्रोत कुन खाना हो?', 'Carrot', 'गाजर', 'Rice', 'चामल', 'Banana', 'केरा', 'Potato', 'आलु'),
    ('Which food is the richest source of vitamin B12?', 'भिटामिन बी१२ को सबैभन्दा धनी स्रोत कुन खाना हो?', 'Meat and animal products', 'मासु र जनावरजन्य पदार्थ', 'Rice', 'चामल', 'Banana', 'केरा', 'Potato', 'आलु'),
    ('Which nutrient is the main source of energy?', 'ऊर्जाको मुख्य स्रोत कुन पोषक तत्व हो?', 'Carbohydrate', 'कार्बोहाइड्रेट', 'Protein', 'प्रोटिन', 'Vitamin', 'भिटामिन', 'Mineral', 'खनिज'),
    ('Which nutrient is needed for body building?', 'शरीर निर्माणका लागि कुन पोषक तत्व चाहिन्छ?', 'Protein', 'प्रोटिन', 'Carbohydrate', 'कार्बोहाइड्रेट', 'Fat', 'बोसो', 'Vitamin', 'भिटामिन'),
    ('How many calories does 1 gram of carbohydrate provide?', '१ ग्राम कार्बोहाइड्रेटले कति क्यालोरी दिन्छ?', '4 kcal', '४ किलोक्यालोरी', '9 kcal', '९ किलोक्यालोरी', '7 kcal', '७ किलोक्यालोरी', '2 kcal', '२ किलोक्यालोरी'),
    ('How many calories does 1 gram of protein provide?', '१ ग्राम प्रोटिनले कति क्यालोरी दिन्छ?', '4 kcal', '४ किलोक्यालोरी', '9 kcal', '९ किलोक्यालोरी', '7 kcal', '७ किलोक्यालोरी', '2 kcal', '२ किलोक्यालोरी'),
    ('How many calories does 1 gram of fat provide?', '१ ग्राम बोसोले कति क्यालोरी दिन्छ?', '9 kcal', '९ किलोक्यालोरी', '4 kcal', '४ किलोक्यालोरी', '7 kcal', '७ किलोक्यालोरी', '2 kcal', '२ किलोक्यालोरी'),
    ('How many calories does 1 gram of alcohol provide?', '१ ग्राम अल्कोहलले कति क्यालोरी दिन्छ?', '7 kcal', '७ किलोक्यालोरी', '4 kcal', '४ किलोक्यालोरी', '9 kcal', '९ किलोक्यालोरी', '2 kcal', '२ किलोक्यालोरी'),
    ('Which is the main source of iodine in the diet?', 'आहारमा आयोडिनको मुख्य स्रोत के हो?', 'Iodised salt', 'आयोडिनयुक्त नुन', 'Rice', 'चामल', 'Milk', 'दूध', 'Banana', 'केरा'),
    ('Which is the main source of vitamin D?', 'भिटामिन डी को मुख्य स्रोत के हो?', 'Sunlight', 'सूर्यको प्रकाश', 'Rice', 'चामल', 'Banana', 'केरा', 'Potato', 'आलु'),
    ('Which vitamin is also known as ascorbic acid?', 'कुन भिटामिनलाई एस्कर्बिक एसिड पनि भनिन्छ?', 'Vitamin C', 'भिटामिन सी', 'Vitamin A', 'भिटामिन ए', 'Vitamin D', 'भिटामिन डी', 'Vitamin B', 'भिटामिन बी'),
    ('Which vitamin is also known as retinol?', 'कुन भिटामिनलाई रेटिनोल पनि भनिन्छ?', 'Vitamin A', 'भिटामिन ए', 'Vitamin C', 'भिटामिन सी', 'Vitamin D', 'भिटामिन डी', 'Vitamin B', 'भिटामिन बी'),
    ('Which vitamin is also known as thiamine?', 'कुन भिटामिनलाई थायमिन पनि भनिन्छ?', 'Vitamin B1', 'भिटामिन बी१', 'Vitamin B2', 'भिटामिन बी२', 'Vitamin C', 'भिटामिन सी', 'Vitamin D', 'भिटामिन डी'),
    ('Which vitamin is also known as riboflavin?', 'कुन भिटामिनलाई राइबोफ्लेभिन पनि भनिन्छ?', 'Vitamin B2', 'भिटामिन बी२', 'Vitamin B1', 'भिटामिन बी१', 'Vitamin C', 'भिटामिन सी', 'Vitamin D', 'भिटामिन डी'),
    ('Which vitamin is also known as cobalamin?', 'कुन भिटामिनलाई कोबालामिन पनि भनिन्छ?', 'Vitamin B12', 'भिटामिन बी१२', 'Vitamin B1', 'भिटामिन बी१', 'Vitamin B2', 'भिटामिन बी२', 'Vitamin C', 'भिटामिन सी'),
    ('Which vitamin is also known as calciferol?', 'कुन भिटामिनलाई क्याल्सिफेरोल पनि भनिन्छ?', 'Vitamin D', 'भिटामिन डी', 'Vitamin A', 'भिटामिन ए', 'Vitamin C', 'भिटामिन सी', 'Vitamin B', 'भिटामिन बी'),
    ('Which vitamin is also known as phylloquinone?', 'कुन भिटामिनलाई फिलोक्विनोन पनि भनिन्छ?', 'Vitamin K', 'भिटामिन के', 'Vitamin A', 'भिटामिन ए', 'Vitamin C', 'भिटामिन सी', 'Vitamin D', 'भिटामिन डी'),
    ('Which vitamin is also known as tocopherol?', 'कुन भिटामिनलाई टोकोफेरोल पनि भनिन्छ?', 'Vitamin E', 'भिटामिन ई', 'Vitamin A', 'भिटामिन ए', 'Vitamin C', 'भिटामिन सी', 'Vitamin D', 'भिटामिन डी'),
    ('Which vitamin is also known as niacin?', 'कुन भिटामिनलाई नियासिन पनि भनिन्छ?', 'Vitamin B3', 'भिटामिन बी३', 'Vitamin B1', 'भिटामिन बी१', 'Vitamin B2', 'भिटामिन बी२', 'Vitamin C', 'भिटामिन सी'),
    ('Which vitamin is also known as folic acid?', 'कुन भिटामिनलाई फोलिक एसिड पनि भनिन्छ?', 'Vitamin B9', 'भिटामिन बी९', 'Vitamin B1', 'भिटामिन बी१', 'Vitamin B2', 'भिटामिन बी२', 'Vitamin C', 'भिटामिन सी'),
    ('Which vitamin is also known as biotin?', 'कुन भिटामिनलाई बायोटिन पनि भनिन्छ?', 'Vitamin B7', 'भिटामिन बी७', 'Vitamin B1', 'भिटामिन बी१', 'Vitamin B2', 'भिटामिन बी२', 'Vitamin C', 'भिटामिन सी'),
]
for r in NUT:
    F(HEALTH_EX, 'Health/Technical basics', 'Nutrition', *r)

# ---------------- Nepal public health ----------------
NPH = [
    ('In which year was the National Health Policy of Nepal first adopted?', 'नेपालको राष्ट्रिय स्वास्थ्य नीति पहिलोपटक कुन वर्ष अपनाइयो?', '1991', 'सन् १९९१', '1990', 'सन् १९९०', '1995', 'सन् १९९५', '2000', 'सन् २०००'),
    ('In which year was the National Health Policy 2019 adopted?', 'राष्ट्रिय स्वास्थ्य नीति २०१९ कुन वर्ष अपनाइयो?', '2019', 'सन् २०१९', '2017', 'सन् २०१७', '2020', 'सन् २०२०', '2015', 'सन् २०१५'),
    ('What is the full form of HMIS?', 'HMIS को पूरा रूप के हो?', 'Health Management Information System', 'स्वास्थ्य व्यवस्थापन सूचना प्रणाली', 'Health Monitoring Information System', 'स्वास्थ्य अनुगमन सूचना प्रणाली', 'Hospital Management Information System', 'अस्पताल व्यवस्थापन सूचना प्रणाली', 'Health Management Index System', 'स्वास्थ्य व्यवस्थापन सूचक प्रणाली'),
    ('What is the full form of FCHV?', 'FCHV को पूरा रूप के हो?', 'Female Community Health Volunteer', 'महिला सामुदायिक स्वास्थ्य स्वयंसेविका', 'Female Community Health Visitor', 'महिला सामुदायिक स्वास्थ्य आगन्तुक', 'Family Community Health Volunteer', 'परिवार सामुदायिक स्वास्थ्य स्वयंसेविका', 'Female Child Health Volunteer', 'महिला बाल स्वास्थ्य स्वयंसेविका'),
    ('In which year was the FCHV programme started in Nepal?', 'नेपालमा महिला सामुदायिक स्वास्थ्य स्वयंसेविका कार्यक्रम कुन वर्ष सुरु भयो?', '1988', 'सन् १९८८', '1980', 'सन् १९८०', '1990', 'सन् १९९०', '1995', 'सन् १९९५'),
    ('What is the full form of EPI?', 'EPI को पूरा रूप के हो?', 'Expanded Programme on Immunization', 'विस्तारित खोप कार्यक्रम', 'Extended Programme on Immunization', 'विस्तारित खोप कार्यक्रम', 'Expanded Programme on Infection', 'विस्तारित सङ्क्रमण कार्यक्रम', 'Essential Programme on Immunization', 'आवश्यक खोप कार्यक्रम'),
    ('In which year was EPI started in Nepal?', 'नेपालमा विस्तारित खोप कार्यक्रम कुन वर्ष सुरु भयो?', '1979', 'सन् १९७९', '1975', 'सन् १९७५', '1980', 'सन् १९८०', '1985', 'सन् १९८५'),
    ('What is the full form of NHEICC?', 'NHEICC को पूरा रूप के हो?', 'National Health Education, Information and Communication Centre', 'राष्ट्रिय स्वास्थ्य शिक्षा, सूचना तथा सञ्चार केन्द्र', 'National Health Education and Information Communication Centre', 'राष्ट्रिय स्वास्थ्य शिक्षा तथा सूचना सञ्चार केन्द्र', 'Nepal Health Education Information Communication Centre', 'नेपाल स्वास्थ्य शिक्षा सूचना सञ्चार केन्द्र', 'National Health Education Information Centre', 'राष्ट्रिय स्वास्थ्य शिक्षा सूचना केन्द्र'),
    ('What is the full form of DoHS?', 'DoHS को पूरा रूप के हो?', 'Department of Health Services', 'स्वास्थ्य सेवा विभाग', 'Department of Health Science', 'स्वास्थ्य विज्ञान विभाग', 'Directorate of Health Services', 'स्वास्थ्य सेवा निर्देशनालय', 'Department of Hospital Services', 'अस्पताल सेवा विभाग'),
    ('What is the full form of MoHP?', 'MoHP को पूरा रूप के हो?', 'Ministry of Health and Population', 'स्वास्थ्य तथा जनसङ्ख्या मन्त्रालय', 'Ministry of Health and Planning', 'स्वास्थ्य तथा योजना मन्त्रालय', 'Ministry of Hospital and Population', 'अस्पताल तथा जनसङ्ख्या मन्त्रालय', 'Ministry of Health and Pharmacy', 'स्वास्थ्य तथा औषधि मन्त्रालय'),
    ('What is the full form of NHRC in Nepal health?', 'नेपाल स्वास्थ्यमा NHRC को पूरा रूप के हो?', 'Nepal Health Research Council', 'नेपाल स्वास्थ्य अनुसन्धान परिषद्', 'National Health Research Council', 'राष्ट्रिय स्वास्थ्य अनुसन्धान परिषद्', 'Nepal Hospital Research Council', 'नेपाल अस्पताल अनुसन्धान परिषद्', 'National Hospital Research Council', 'राष्ट्रिय अस्पताल अनुसन्धान परिषद्'),
    ('In which year was the Nepal Health Research Council established?', 'नेपाल स्वास्थ्य अनुसन्धान परिषद् कुन वर्ष स्थापना भयो?', '1991', 'सन् १९९१', '1990', 'सन् १९९०', '1995', 'सन् १९९५', '2000', 'सन् २०००'),
    ('What is the full form of NTC in Nepal health?', 'नेपाल स्वास्थ्यमा NTC को पूरा रूप के हो?', 'National Tuberculosis Centre', 'राष्ट्रिय क्षयरोग केन्द्र', 'National Treatment Centre', 'राष्ट्रिय उपचार केन्द्र', 'Nepal Tuberculosis Centre', 'नेपाल क्षयरोग केन्द्र', 'National Trauma Centre', 'राष्ट्रिय आघात केन्द्र'),
    ('What is the full form of NPHL?', 'NPHL को पूरा रूप के हो?', 'National Public Health Laboratory', 'राष्ट्रिय जनस्वास्थ्य प्रयोगशाला', 'National Public Health Library', 'राष्ट्रिय जनस्वास्थ्य पुस्तकालय', 'Nepal Public Health Laboratory', 'नेपाल जनस्वास्थ्य प्रयोगशाला', 'National Population Health Laboratory', 'राष्ट्रिय जनसङ्ख्या स्वास्थ्य प्रयोगशाला'),
    ('What is the full form of EDCD?', 'EDCD को पूरा रूप के हो?', 'Epidemiology and Disease Control Division', 'महामारी तथा रोग नियन्त्रण महाशाखा', 'Epidemiology and Disease Control Department', 'महामारी तथा रोग नियन्त्रण विभाग', 'Epidemic and Disease Control Division', 'महामारी तथा रोग नियन्त्रण महाशाखा', 'Epidemiology and Drug Control Division', 'महामारी तथा औषधि नियन्त्रण महाशाखा'),
    ('What is the full form of NTCC?', 'NTCC को पूरा रूप के हो?', 'National Tuberculosis Control Centre', 'राष्ट्रिय क्षयरोग नियन्त्रण केन्द्र', 'National Treatment Control Centre', 'राष्ट्रिय उपचार नियन्त्रण केन्द्र', 'Nepal Tuberculosis Control Centre', 'नेपाल क्षयरोग नियन्त्रण केन्द्र', 'National Trauma Control Centre', 'राष्ट्रिय आघात नियन्त्रण केन्द्र'),
    ('What is the full form of NCASC?', 'NCASC को पूरा रूप के हो?', 'National Centre for AIDS and STD Control', 'राष्ट्रिय एड्स तथा यौनरोग नियन्त्रण केन्द्र', 'National Centre for AIDS and STI Control', 'राष्ट्रिय एड्स तथा यौनरोग नियन्त्रण केन्द्र', 'Nepal Centre for AIDS and STD Control', 'नेपाल एड्स तथा यौनरोग नियन्त्रण केन्द्र', 'National Centre for AIDS Control', 'राष्ट्रिय एड्स नियन्त्रण केन्द्र'),
    ('What is the full form of LMBI?', 'LMBI को पूरा रूप के हो?', 'Leprosy Mission Nepal', 'कुष्ठरोग मिसन नेपाल', 'Leprosy Mission Bangladesh', 'कुष्ठरोग मिसन बङ्गलादेश', 'Leprosy Medical Board of India', 'कुष्ठरोग चिकित्सा बोर्ड भारत', 'Leprosy Mission International', 'कुष्ठरोग मिसन इन्टरनेसनल'),
    ('What is the full form of CBIMCI?', 'CBIMCI को पूरा रूप के हो?', 'Community-Based Integrated Management of Childhood Illness', 'समुदायमा आधारित बालरोग एकीकृत व्यवस्थापन', 'Community-Based Integrated Management of Child Infection', 'समुदायमा आधारित बाल सङ्क्रमण एकीकृत व्यवस्थापन', 'Community-Based Immunization Management of Childhood Illness', 'समुदायमा आधारित बालरोग खोप व्यवस्थापन', 'Community-Based Integrated Management of Child Injury', 'समुदायमा आधारित बाल चोट एकीकृत व्यवस्थापन'),
    ('What is the full form of IMCI?', 'IMCI को पूरा रूप के हो?', 'Integrated Management of Childhood Illness', 'बालरोग एकीकृत व्यवस्थापन', 'Integrated Management of Child Infection', 'बाल सङ्क्रमण एकीकृत व्यवस्थापन', 'Immunization Management of Childhood Illness', 'बालरोग खोप व्यवस्थापन', 'Integrated Management of Child Injury', 'बाल चोट एकीकृत व्यवस्थापन'),
    ('What is the full form of SBA?', 'SBA को पूरा रूप के हो?', 'Skilled Birth Attendant', 'दक्ष प्रसूति सेवाप्रदायक', 'Skilled Birth Assistant', 'दक्ष प्रसूति सहायक', 'Safe Birth Attendant', 'सुरक्षित प्रसूति सेवाप्रदायक', 'Skilled Baby Attendant', 'दक्ष शिशु सेवाप्रदायक'),
    ('What is the full form of ANC?', 'ANC को पूरा रूप के हो?', 'Antenatal Care', 'गर्भावस्थाको हेरचाह', 'Antenatal Clinic', 'गर्भावस्था क्लिनिक', 'After Natal Care', 'प्रसवपछिको हेरचाह', 'Antenatal Checkup', 'गर्भावस्था जाँच'),
    ('What is the full form of PNC?', 'PNC को पूरा रूप के हो?', 'Postnatal Care', 'प्रसवपछिको हेरचाह', 'Postnatal Clinic', 'प्रसवपछिको क्लिनिक', 'Prenatal Care', 'प्रसवपूर्व हेरचाह', 'Postnatal Checkup', 'प्रसवपछिको जाँच'),
    ('How many ANC visits are recommended by the WHO?', 'विश्व स्वास्थ्य सङ्गठनले कति ANC भ्रमण सिफारिस गर्छ?', '8', '८', '4', '४', '6', '६', '10', '१०'),
    ('What is the full form of FP?', 'FP को पूरा रूप के हो?', 'Family Planning', 'परिवार नियोजन', 'Family Programme', 'परिवार कार्यक्रम', 'Female Planning', 'महिला नियोजन', 'Family Protection', 'परिवार सुरक्षा'),
    ('What is the full form of IUCD?', 'IUCD को पूरा रूप के हो?', 'Intrauterine Contraceptive Device', 'गर्भाशयभित्रको गर्भनिरोधक साधन', 'Intrauterine Contraceptive Drug', 'गर्भाशयभित्रको गर्भनिरोधक औषधि', 'Internal Uterine Contraceptive Device', 'आन्तरिक गर्भाशय गर्भनिरोधक साधन', 'Intrauterine Contraception Device', 'गर्भाशयभित्रको गर्भनिरोध साधन'),
    ('What is the full form of DMPA?', 'DMPA को पूरा रूप के हो?', 'Depot Medroxyprogesterone Acetate', 'डिपो मेड्रोक्सीप्रोजेस्टेरोन एसिटेट', 'Depot Medroxyprogesterone Acid', 'डिपो मेड्रोक्सीप्रोजेस्टेरोन एसिड', 'Depot Medroxyprogesterone Agent', 'डिपो मेड्रोक्सीप्रोजेस्टेरोन एजेन्ट', 'Depot Medroxyprogesterone Antibiotic', 'डिपो मेड्रोक्सीप्रोजेस्टेरोन एन्टिबायोटिक'),
    ('What is the full form of OCP?', 'OCP को पूरा रूप के हो?', 'Oral Contraceptive Pill', 'मुखबाट खाने गर्भनिरोधक चक्की', 'Oral Contraceptive Programme', 'मुखबाट खाने गर्भनिरोधक कार्यक्रम', 'Oral Contraceptive Powder', 'मुखबाट खाने गर्भनिरोधक धुलो', 'Oral Contraceptive Patch', 'मुखबाट खाने गर्भनिरोधक प्याच'),
    ('What is the full form of ECP?', 'ECP को पूरा रूप के हो?', 'Emergency Contraceptive Pill', 'आपत्कालीन गर्भनिरोधक चक्की', 'Emergency Contraceptive Programme', 'आपत्कालीन गर्भनिरोधक कार्यक्रम', 'Emergency Contraceptive Powder', 'आपत्कालीन गर्भनिरोधक धुलो', 'Emergency Contraceptive Patch', 'आपत्कालीन गर्भनिरोधक प्याच'),
    ('What is the full form of VSC?', 'VSC को पूरा रूप के हो?', 'Voluntary Surgical Contraception', 'स्वेच्छिक शल्य गर्भनिरोध', 'Voluntary Surgical Contraceptive', 'स्वेच्छिक शल्य गर्भनिरोधक', 'Voluntary Sterilization Contraception', 'स्वेच्छिक बन्ध्याकरण गर्भनिरोध', 'Voluntary Surgical Care', 'स्वेच्छिक शल्य हेरचाह'),
]
for r in NPH:
    F(HEALTH_EX, 'Health/Technical basics', 'Nepal Public Health', *r)

n = em.write('expansion-r10-health2.json')
print('HEALTH2 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
