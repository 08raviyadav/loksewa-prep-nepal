#!/usr/bin/env python3
"""R10 generator 9: Current Affairs 2025/2026 (~260). Facts verified by web
search on 2026-10-26: Nepal Gen Z transition (Oli resignation, Karki interim
government, 5 March 2026 election, RSP landslide, Balen Shah PM), FIFA World
Cup 2026 (Spain), T20 World Cup 2026 (India), 2025 Nobel Prizes, Pope Leo
XIV, Asia Cup 2025, Champions Trophy 2025, Women's World Cup 2025."""
import sys, random
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num

bank = Bank()
em = Emitter(bank, 'R10-CURR')
rng = random.Random(88009)
EX = ['kharidar', 'nasu', 'section-officer', 'provincial-psc', 'psc-service-groups', 'foreign-service', 'nrb-assistant', 'rbb', 'police', 'army', 'tsc-primary', 'tsc-secondary']

def fact(q, qn, a, an, d1, d1n, d2, d2n, d3, d3n, sub='Nepal Events 2025-26'):
    em.emit(EX, 'Current Affairs', sub, 'hard', 2, q, qn,
            [a, d1, d2, d3], [an, d1n, d2n, d3n], 0,
            f'The answer is {a}.', f'उत्तर {an} हो।')

# ---------------- Nepal 2025-26 ----------------
NEPAL = [
    ('On which date did Prime Minister KP Sharma Oli resign in 2025?', 'प्रधानमन्त्री केपी शर्मा ओलीले सन् २०२५ मा कुन मितिमा राजीनामा दिए?', '9 September 2025', '९ सेप्टेम्बर २०२५', '8 September 2025', '८ सेप्टेम्बर २०२५', '12 September 2025', '१२ सेप्टेम्बर २०२५', '10 September 2025', '१० सेप्टेम्बर २०२५'),
    ('What triggered the Gen Z protests of September 2025 in Nepal?', 'सन् २०२५ सेप्टेम्बरको जेन्जी आन्दोलन के कारणले सुरु भयो?', 'Ban on 26 social media platforms', '२६ वटा सामाजिक सञ्जाल प्लेटफर्ममाथि प्रतिबन्ध', 'Fuel price hike', 'इन्धनको मूल्यवृद्धि', 'Earthquake', 'भूकम्प', 'Border blockade', 'नाकाबन्दी'),
    ('On which date did the Gen Z protests begin in Nepal in 2025?', 'नेपालमा सन् २०२५ मा जेन्जी आन्दोलन कुन मितिबाट सुरु भयो?', '8 September 2025', '८ सेप्टेम्बर २०२५', '9 September 2025', '९ सेप्टेम्बर २०२५', '12 September 2025', '१२ सेप्टेम्बर २०२५', '1 September 2025', '१ सेप्टेम्बर २०२५'),
    ('Who became the interim Prime Minister of Nepal in September 2025?', 'सन् २०२५ सेप्टेम्बरमा नेपालको अन्तरिम प्रधानमन्त्री को बनिन्?', 'Sushila Karki', 'सुशीला कार्की', 'Bidya Devi Bhandari', 'विद्यादेवी भण्डारी', 'Sabita Bhandari', 'सबिता भण्डारी', 'Onsari Gharti Magar', 'ओनसरी घर्ती मगर'),
    ('On which date was Sushila Karki sworn in as interim Prime Minister?', 'सुशीला कार्कीले अन्तरिम प्रधानमन्त्रीको शपथ कुन मितिमा लिइन्?', '12 September 2025', '१२ सेप्टेम्बर २०२५', '9 September 2025', '९ सेप्टेम्बर २०२५', '8 September 2025', '८ सेप्टेम्बर २०२५', '5 March 2026', '५ मार्च २०२६'),
    ('Who was the first woman Prime Minister of Nepal?', 'नेपालकी पहिलो महिला प्रधानमन्त्री को हुन्?', 'Sushila Karki', 'सुशीला कार्की', 'Bidya Devi Bhandari', 'विद्यादेवी भण्डारी', 'Sahana Pradhan', 'सहाना प्रधान', 'Onsari Gharti Magar', 'ओनसरी घर्ती मगर'),
    ('On which date was the House of Representatives dissolved in 2025?', 'सन् २०२५ मा प्रतिनिधि सभा कुन मितिमा विघटन भयो?', '12 September 2025', '१२ सेप्टेम्बर २०२५', '9 September 2025', '९ सेप्टेम्बर २०२५', '8 September 2025', '८ सेप्टेम्बर २०२५', '5 March 2026', '५ मार्च २०२६'),
    ('When were fresh elections held in Nepal after the 2025 Gen Z protests?', 'सन् २०२५ को जेन्जी आन्दोलनपछि नेपालमा नयाँ निर्वाचन कहिले भयो?', '5 March 2026', '५ मार्च २०२६', '9 September 2025', '९ सेप्टेम्बर २०२५', '12 September 2025', '१२ सेप्टेम्बर २०२५', '27 March 2026', '२७ मार्च २०२६'),
    ('Which party won the 5 March 2026 general election in Nepal?', 'सन् २०२६ मार्च ५ को आम निर्वाचनमा नेपालमा कुन दल विजयी भयो?', 'Rastriya Swatantra Party (RSP)', 'राष्ट्रिय स्वतन्त्र पार्टी (रास्वपा)', 'Nepali Congress', 'नेपाली काङ्ग्रेस', 'CPN-UML', 'नेकपा (एमाले)', 'Maoist Centre', 'माओवादी केन्द्र'),
    ('How many seats did the Rastriya Swatantra Party win in the 2026 election?', 'सन् २०२६ को निर्वाचनमा राष्ट्रिय स्वतन्त्र पार्टीले कति सिट जित्यो?', '182 of 275', '२७५ मध्ये १८२', '89 of 275', '२७५ मध्ये ८९', '78 of 275', '२७५ मध्ये ७८', '25 of 275', '२७५ मध्ये २५'),
    ('Who became the Prime Minister of Nepal after the March 2026 election?', 'सन् २०२६ मार्चको निर्वाचनपछि नेपालको प्रधानमन्त्री को बने?', 'Balendra Shah (Balen Shah)', 'बालेन्द्र शाह (बालेन शाह)', 'KP Sharma Oli', 'केपी शर्मा ओली', 'Sher Bahadur Deuba', 'शेरबहादुर देउवा', 'Pushpa Kamal Dahal', 'पुष्पकमल दाहाल'),
    ('On which date did Balendra Shah become Prime Minister of Nepal?', 'बालेन्द्र शाह नेपालको प्रधानमन्त्री कुन मितिमा बने?', '27 March 2026', '२७ मार्च २०२६', '5 March 2026', '५ मार्च २०२६', '12 September 2025', '१२ सेप्टेम्बर २०२५', '9 September 2025', '९ सेप्टेम्बर २०२५'),
    ('How many seats did the Nepali Congress win in the 2026 election?', 'सन् २०२६ को निर्वाचनमा नेपाली काङ्ग्रेसले कति सिट जित्यो?', '38', '३८', '89', '८९', '25', '२५', '182', '१८२'),
    ('How many seats did CPN-UML win in the 2026 election?', 'सन् २०२६ को निर्वाचनमा नेकपा (एमाले) ले कति सिट जित्यो?', '25', '२५', '78', '७८', '38', '३८', '182', '१८२'),
    ('What was the approximate voter turnout in the March 2026 Nepal election?', 'सन् २०२६ मार्चको नेपाल निर्वाचनमा मतदाताको उपस्थिति लगभग कति थियो?', 'About 60%', 'लगभग ६०%', 'About 40%', 'लगभग ४०%', 'About 80%', 'लगभग ८०%', 'About 50%', 'लगभग ५०%'),
    ('Who was appointed the first woman Attorney General of Nepal in 2025?', 'सन् २०२५ मा नेपालकी पहिलो महिला महान्यायाधिवक्ता को नियुक्त भइन्?', 'Sabita Bhandari', 'सबिता भण्डारी', 'Sushila Karki', 'सुशीला कार्की', 'Bidya Devi Bhandari', 'विद्यादेवी भण्डारी', 'Onsari Gharti Magar', 'ओनसरी घर्ती मगर'),
    ('How long did the Sushila Karki interim government remain in office?', 'सुशीला कार्कीको अन्तरिम सरकार कति समय सत्तामा रह्यो?', '12 September 2025 to 27 March 2026', '१२ सेप्टेम्बर २०२५ देखि २७ मार्च २०२६', '9 September 2025 to 5 March 2026', '९ सेप्टेम्बर २०२५ देखि ५ मार्च २०२६', '12 September 2025 to 5 March 2026', '१२ सेप्टेम्बर २०२५ देखि ५ मार्च २०२६', '8 September 2025 to 27 March 2026', '८ सेप्टेम्बर २०२५ देखि २७ मार्च २०२६'),
    ('Who was the President of Nepal during the 2025 Gen Z protests?', 'सन् २०२५ को जेन्जी आन्दोलनका बेला नेपालका राष्ट्रपति को थिए?', 'Ram Chandra Poudel', 'रामचन्द्र पौडेल', 'Bidya Devi Bhandari', 'विद्यादेवी भण्डारी', 'Ram Baran Yadav', 'रामवरण यादव', 'Nanda Bahadur Pun', 'नन्दबहादुर पुन'),
    ('Who appointed Sushila Karki as interim Prime Minister?', 'सुशीला कार्कीलाई अन्तरिम प्रधानमन्त्री कसले नियुक्त गरे?', 'President Ram Chandra Poudel', 'राष्ट्रपति रामचन्द्र पौडेल', 'KP Sharma Oli', 'केपी शर्मा ओली', 'Chief Justice', 'प्रधानन्यायाधीश', 'Nepal Army chief', 'नेपाली सेनाका प्रमुख'),
    ('How many ministers (including the PM) were there in the Karki interim cabinet?', 'कार्की अन्तरिम मन्त्रिपरिषद्मा प्रधानमन्त्रीसहित कति मन्त्री थिए?', '11', '११', '15', '१५', '21', '२१', '25', '२५'),
    ('In which year was the Rastriya Swatantra Party founded?', 'राष्ट्रिय स्वतन्त्र पार्टी कुन वर्ष स्थापना भयो?', '2022', 'सन् २०२२', '2017', 'सन् २०१७', '2020', 'सन् २०२०', '2024', 'सन् २०२४'),
    ('Before becoming PM, Balendra Shah was the mayor of which city?', 'प्रधानमन्त्री बन्नुअघि बालेन्द्र शाह कुन सहरका मेयर थिए?', 'Kathmandu', 'काठमाडौँ', 'Pokhara', 'पोखरा', 'Biratnagar', 'विराटनगर', 'Lalitpur', 'ललितपुर'),
    ('Sushila Karki was the first woman to hold which post before becoming PM?', 'प्रधानमन्त्री बन्नुअघि सुशीला कार्की कुन पद सम्हाल्ने पहिलो महिला थिइन्?', 'Chief Justice of Nepal', 'नेपालकी प्रधानन्यायाधीश', 'President of Nepal', 'नेपालकी राष्ट्रपति', 'Speaker', 'सभामुख', 'Attorney General', 'महान्यायाधिवक्ता'),
    ('In which year did Sushila Karki serve as Chief Justice of Nepal?', 'सुशीला कार्की नेपालकी प्रधानन्यायाधीश कुन वर्ष थिइन्?', '2016-2017', 'सन् २०१६-२०१७', '2015-2016', 'सन् २०१५-२०१६', '2017-2018', 'सन् २०१७-२०१८', '2014-2015', 'सन् २०१४-२०१५'),
    ('What was the main demand of the Gen Z protests in Nepal in 2025?', 'सन् २०२५ मा नेपालको जेन्जी आन्दोलनको मुख्य माग के थियो?', 'End to corruption and nepotism', 'भ्रष्टाचार र नातावादको अन्त्य', 'Higher salaries', 'उच्च तलब', 'Free education', 'निःशुल्क शिक्षा', 'Cheaper fuel', 'सस्तो इन्धन'),
    ('How many social media platforms were banned before the September 2025 protests?', 'सन् २०२५ सेप्टेम्बरको आन्दोलनअघि कति सामाजिक सञ्जाल प्लेटफर्ममाथि प्रतिबन्ध लगाइएको थियो?', '26', '२६', '12', '१२', '18', '१८', '30', '३०'),
    ('In the 2026 election, Balendra Shah defeated KP Sharma Oli in whose constituency?', 'सन् २०२६ को निर्वाचनमा बालेन्द्र शाहले केपी शर्मा ओलीलाई कसको निर्वाचन क्षेत्रमा हराए?', "Oli's own constituency", 'ओलीकै निर्वाचन क्षेत्र', 'His own constituency', 'आफ्नै निर्वाचन क्षेत्र', 'Kathmandu-1', 'काठमाडौँ-१', 'Pokhara-1', 'पोखरा-१'),
    ('Which party did KP Sharma Oli lead when he resigned in 2025?', 'सन् २०२५ मा राजीनामा दिँदा केपी शर्मा ओलीले कुन दलको नेतृत्व गरेका थिए?', 'CPN-UML', 'नेकपा (एमाले)', 'Nepali Congress', 'नेपाली काङ्ग्रेस', 'Maoist Centre', 'माओवादी केन्द्र', 'RSP', 'रास्वपा'),
    ('How many seats are there in the House of Representatives of Nepal?', 'नेपालको प्रतिनिधि सभामा कति सिट छन्?', '275', '२७५', '165', '१६५', '110', '११०', '59', '५९'),
    ('How many seats are there in the National Assembly of Nepal?', 'नेपालको राष्ट्रिय सभामा कति सिट छन्?', '59', '५९', '275', '२७५', '165', '१६५', '110', '११०'),
]
for row in NEPAL:
    fact(*row)

# ---------------- World 2025-26 ----------------
WORLD = [
    ('Which country won the FIFA World Cup 2026?', 'सन् २०२६ को फिफा विश्वकप कुन देशले जित्यो?', 'Spain', 'स्पेन', 'Argentina', 'अर्जेन्टिना', 'France', 'फ्रान्स', 'Brazil', 'ब्राजिल'),
    ('Who did Spain beat in the final of the FIFA World Cup 2026?', 'सन् २०२६ को फिफा विश्वकपको फाइनलमा स्पेनले कसलाई हरायो?', 'Argentina', 'अर्जेन्टिना', 'France', 'फ्रान्स', 'England', 'इङ्ग्ल्यान्ड', 'Brazil', 'ब्राजिल'),
    ('What was the score in the FIFA World Cup 2026 final?', 'सन् २०२६ को फिफा विश्वकप फाइनलको स्कोर के थियो?', 'Spain 1-0 Argentina', 'स्पेन १-० अर्जेन्टिना', 'Spain 2-0 Argentina', 'स्पेन २-० अर्जेन्टिना', 'Spain 1-0 France', 'स्पेन १-० फ्रान्स', 'Argentina 1-0 Spain', 'अर्जेन्टिना १-० स्पेन'),
    ('On which date was the FIFA World Cup 2026 final played?', 'सन् २०२६ को फिफा विश्वकप फाइनल कुन मितिमा खेलियो?', '19 July 2026', '१९ जुलाई २०२६', '11 June 2026', '११ जुन २०२६', '28 June 2026', '२८ जुन २०२६', '15 July 2026', '१५ जुलाई २०२६'),
    ('Where was the FIFA World Cup 2026 final played?', 'सन् २०२६ को फिफा विश्वकप फाइनल कहाँ खेलियो?', 'MetLife Stadium, New York New Jersey', 'मेटलाइफ स्टेडियम, न्युयोर्क न्यु जर्सी', 'Wembley Stadium, London', 'वेम्बली स्टेडियम, लन्डन', 'Lusail Stadium, Qatar', 'लुसेल स्टेडियम, कतार', 'Maracana Stadium, Rio', 'माराकाना स्टेडियम, रियो'),
    ('Which countries co-hosted the FIFA World Cup 2026?', 'सन् २०२६ को फिफा विश्वकप कुन देशहरूले संयुक्त रूपमा आयोजना गरे?', 'USA, Canada and Mexico', 'अमेरिका, क्यानडा र मेक्सिको', 'USA and Mexico', 'अमेरिका र मेक्सिको', 'Canada and Mexico', 'क्यानडा र मेक्सिको', 'USA and Canada', 'अमेरिका र क्यानडा'),
    ('How many teams played in the FIFA World Cup 2026?', 'सन् २०२६ को फिफा विश्वकपमा कति टोलीले खेले?', '48', '४८', '32', '३२', '24', '२४', '16', '१६'),
    ('How many FIFA World Cup titles has Spain won (as of 2026)?', 'सन् २०२६ सम्म स्पेनले कति फिफा विश्वकप उपाधि जितेको छ?', '2', '२', '1', '१', '3', '३', '4', '४'),
    ('Who won the Golden Boot at the FIFA World Cup 2026?', 'सन् २०२६ को फिफा विश्वकपमा गोल्डेन बुट कसले जित्यो?', 'Kylian Mbappe', 'किलियन एमबाप्पे', 'Lionel Messi', 'लियोनल मेसी', 'Lamine Yamal', 'लामिन यमाल', 'Harry Kane', 'ह्यारी केन'),
    ('How many goals did Kylian Mbappe score at the FIFA World Cup 2026?', 'सन् २०२६ को फिफा विश्वकपमा किलियन एमबाप्पेले कति गोल गरे?', '10', '१०', '8', '८', '7', '७', '6', '६'),
    ('Who won the Golden Ball at the FIFA World Cup 2026?', 'सन् २०२६ को फिफा विश्वकपमा गोल्डेन बल कसले जित्यो?', 'Rodri', 'रोड्री', 'Lamine Yamal', 'लामिन यमाल', 'Kylian Mbappe', 'किलियन एमबाप्पे', 'Lionel Messi', 'लियोनल मेसी'),
    ('Who scored the winning goal in the FIFA World Cup 2026 final?', 'सन् २०२६ को फिफा विश्वकप फाइनलमा विजयी गोल कसले गरे?', 'Ferran Torres', 'फेरान टोरेस', 'Lamine Yamal', 'लामिन यमाल', 'Rodri', 'रोड्री', 'Nico Williams', 'निको विलियम्स'),
    ('Which country won the ICC T20 World Cup 2026?', 'सन् २०२६ को आईसीसी टी-२० विश्वकप कुन देशले जित्यो?', 'India', 'भारत', 'New Zealand', 'न्युजिल्यान्ड', 'Australia', 'अस्ट्रेलिया', 'England', 'इङ्ग्ल्यान्ड'),
    ('Who did India beat in the final of the T20 World Cup 2026?', 'सन् २०२६ को टी-२० विश्वकप फाइनलमा भारतले कसलाई हरायो?', 'New Zealand', 'न्युजिल्यान्ड', 'Australia', 'अस्ट्रेलिया', 'South Africa', 'दक्षिण अफ्रिका', 'England', 'इङ्ग्ल्यान्ड'),
    ('By how many runs did India win the T20 World Cup 2026 final?', 'सन् २०२६ को टी-२० विश्वकप फाइनलमा भारत कति रनले विजयी भयो?', '96 runs', '९६ रन', '7 runs', '७ रन', '5 wickets', '५ विकेट', '36 runs', '३६ रन'),
    ('On which date was the T20 World Cup 2026 final played?', 'सन् २०२६ को टी-२० विश्वकप फाइनल कुन मितिमा खेलियो?', '8 March 2026', '८ मार्च २०२६', '29 June 2024', '२९ जुन २०२४', '15 February 2026', '१५ फेब्रुअरी २०२६', '3 March 2026', '३ मार्च २०२६'),
    ('Where was the T20 World Cup 2026 final played?', 'सन् २०२६ को टी-२० विश्वकप फाइनल कहाँ खेलियो?', 'Narendra Modi Stadium, Ahmedabad', 'नरेन्द्र मोदी स्टेडियम, अहमदाबाद', 'Eden Gardens, Kolkata', 'इडेन गार्डेन्स, कोलकाता', 'Melbourne Cricket Ground', 'मेलबर्न क्रिकेट मैदान', 'Lord\'s, London', 'लर्ड्स, लन्डन'),
    ('Which countries co-hosted the T20 World Cup 2026?', 'सन् २०२६ को टी-२० विश्वकप कुन देशहरूले संयुक्त रूपमा आयोजना गरे?', 'India and Sri Lanka', 'भारत र श्रीलङ्का', 'India and Bangladesh', 'भारत र बङ्गलादेश', 'Australia and New Zealand', 'अस्ट्रेलिया र न्युजिल्यान्ड', 'West Indies and USA', 'वेस्ट इन्डिज र अमेरिका'),
    ('How many T20 World Cup titles has India won (as of 2026)?', 'सन् २०२६ सम्म भारतले कति टी-२० विश्वकप उपाधि जितेको छ?', '3', '३', '2', '२', '1', '१', '4', '४'),
    ('Who was the captain of India in the T20 World Cup 2026?', 'सन् २०२६ को टी-२० विश्वकपमा भारतका कप्तान को थिए?', 'Suryakumar Yadav', 'सूर्यकुमार यादव', 'Rohit Sharma', 'रोहित शर्मा', 'Virat Kohli', 'विराट कोहली', 'Hardik Pandya', 'हार्दिक पाण्ड्या'),
    ('Who was the Player of the Tournament in the T20 World Cup 2026?', 'सन् २०२६ को टी-२० विश्वकपमा प्लेयर अफ द टुर्नामेन्ट को भए?', 'Sanju Samson', 'सञ्जु सामसन', 'Jasprit Bumrah', 'जसप्रीत बुमराह', 'Suryakumar Yadav', 'सूर्यकुमार यादव', 'Sahibzada Farhan', 'साहिबजादा फरहान'),
    ('Who was the Player of the Final in the T20 World Cup 2026?', 'सन् २०२६ को टी-२० विश्वकप फाइनलमा प्लेयर अफ द फाइनल को भए?', 'Jasprit Bumrah', 'जसप्रीत बुमराह', 'Sanju Samson', 'सञ्जु सामसन', 'Suryakumar Yadav', 'सूर्यकुमार यादव', 'Varun Chakravarthy', 'वरुण चक्रवर्ती'),
    ('Which country won the ICC Champions Trophy 2025?', 'सन् २०२५ को आईसीसी च्याम्पियन्स ट्रफी कुन देशले जित्यो?', 'India', 'भारत', 'New Zealand', 'न्युजिल्यान्ड', 'Australia', 'अस्ट्रेलिया', 'South Africa', 'दक्षिण अफ्रिका'),
    ('Which country won the Asia Cup 2025?', 'सन् २०२५ को एसिया कप कुन देशले जित्यो?', 'India', 'भारत', 'Pakistan', 'पाकिस्तान', 'Sri Lanka', 'श्रीलङ्का', 'Bangladesh', 'बङ्गलादेश'),
    ('Which country won the Women\'s Cricket World Cup 2025?', 'सन् २०२५ को महिला क्रिकेट विश्वकप कुन देशले जित्यो?', 'India', 'भारत', 'South Africa', 'दक्षिण अफ्रिका', 'Australia', 'अस्ट्रेलिया', 'England', 'इङ्ग्ल्यान्ड'),
    ('Who won the Nobel Peace Prize 2025?', 'सन् २०२५ को नोबेल शान्ति पुरस्कार कसले जिते?', 'Maria Corina Machado', 'मारिया कोरिना माचाडो', 'Donald Trump', 'डोनाल्ड ट्रम्प', 'Antonio Guterres', 'एन्टोनियो गुटेरेस', 'Greta Thunberg', 'ग्रेटा थनबर्ग'),
    ('From which country is the 2025 Nobel Peace Prize winner Maria Corina Machado?', 'सन् २०२५ की नोबेल शान्ति पुरस्कार विजेता मारिया कोरिना माचाडो कुन देशकी हुन्?', 'Venezuela', 'भेनेजुएला', 'Colombia', 'कोलम्बिया', 'Brazil', 'ब्राजिल', 'Argentina', 'अर्जेन्टिना'),
    ('Who won the Nobel Prize in Literature 2025?', 'सन् २०२५ को साहित्य नोबेल पुरस्कार कसले जिते?', 'Laszlo Krasznahorkai', 'लास्लो क्रास्नाहोरकाई', 'Han Kang', 'हान काङ', 'Jon Fosse', 'जोन फोसे', 'Annie Ernaux', 'एनी एर्नो'),
    ('From which country is the 2025 Nobel Literature winner Laszlo Krasznahorkai?', 'सन् २०२५ का साहित्य नोबेल विजेता लास्लो क्रास्नाहोरकाई कुन देशका हुन्?', 'Hungary', 'हङ्गेरी', 'Poland', 'पोल्यान्ड', 'Austria', 'अस्ट्रिया', 'Romania', 'रोमानिया'),
    ('Who won the Nobel Prize in Physics 2025?', 'सन् २०२५ को भौतिकशास्त्र नोबेल पुरस्कार कसले जिते?', 'John Clarke, Michel Devoret and John Martinis', 'जोन क्लार्क, मिसेल डेभोरेट र जोन मार्टिनिस', 'Alain Aspect, John Clauser and Anton Zeilinger', 'एलेन एस्पेक्ट, जोन क्लाउजर र एन्टोन जाइलिङ्गर', 'Pierre Agostini, Ferenc Krausz and Anne L\'Huillier', 'पियरे एगोस्टिनी, फेरेन्क क्राउज र एनी लुइलियर', 'Syukuro Manabe, Klaus Hasselmann and Giorgio Parisi', 'स्युकुरो मानाबे, क्लाउस ह्यासेलम्यान र जर्जियो पारिसी'),
    ('Who won the Nobel Prize in Chemistry 2025?', 'सन् २०२५ को रसायनशास्त्र नोबेल पुरस्कार कसले जिते?', 'Susumu Kitagawa, Richard Robson and Omar Yaghi', 'सुसुमु कितागावा, रिचर्ड रोब्सन र ओमर याघी', 'Carolyn Bertozzi, Morten Meldal and Barry Sharpless', 'क्यारोलिन बर्टोजी, मोर्टेन मेल्डल र ब्यारी शार्पलेस', 'David MacMillan and Benjamin List', 'डेभिड म्याकमिलन र बेन्जामिन लिस्ट', 'Emmanuelle Charpentier and Jennifer Doudna', 'इमानुएल शार्पेन्टियर र जेनिफर डाउड्ना'),
    ('Who won the Nobel Prize in Medicine 2025?', 'सन् २०२५ को चिकित्सा नोबेल पुरस्कार कसले जिते?', 'Mary Brunkow, Fred Ramsdell and Shimon Sakaguchi', 'मेरी ब्रुन्को, फ्रेड राम्सडेल र सिमोन साकागुची', 'Katalin Kariko and Drew Weissman', 'क्याटलिन कारिको र ड्रु वाइस्म्यान', 'Svante Paabo', 'स्वान्ते पाबो', 'David Julius and Ardem Patapoutian', 'डेभिड जुलियस र आर्डेम पटापाउटियन'),
    ('Who won the Nobel Prize in Economics 2025?', 'सन् २०२५ को अर्थशास्त्र नोबेल पुरस्कार कसले जिते?', 'Joel Mokyr, Philippe Aghion and Peter Howitt', 'जोएल मोकिर, फिलिप एगियोन र पिटर होविट', 'Daron Acemoglu, Simon Johnson and James Robinson', 'डारोन एसेमोग्लु, साइमन जोन्सन र जेम्स रोबिन्सन', 'Ben Bernanke, Douglas Diamond and Philip Dybvig', 'बेन बर्नान्के, डग्लस डायमन्ड र फिलिप डिब्भिग', 'Claudia Goldin', 'क्लाउडिया गोल्डिन'),
    ('Who became the Pope in 2025 after Pope Francis died?', 'सन् २०२५ मा पोप फ्रान्सिसको मृत्युपछि पोप को बने?', 'Pope Leo XIV', 'पोप लियो चौधौँ', 'Pope Benedict XVI', 'पोप बेनेडिक्ट सोह्रौँ', 'Pope John Paul II', 'पोप जोन पल द्वितीय', 'Pope Francis II', 'पोप फ्रान्सिस द्वितीय'),
    ('What was the birth name of Pope Leo XIV?', 'पोप लियो चौधौँको जन्म नाम के थियो?', 'Robert Prevost', 'रोबर्ट प्रेभोस्ट', 'Jorge Bergoglio', 'जोर्ज बर्गोग्लियो', 'Joseph Ratzinger', 'जोसेफ रात्जिङ्गर', 'Karol Wojtyla', 'कारोल वोज्टिला'),
    ('Pope Leo XIV is the first pope from which country?', 'पोप लियो चौधौँ कुन देशका पहिलो पोप हुन्?', 'United States', 'संयुक्त राज्य अमेरिका', 'Italy', 'इटाली', 'Argentina', 'अर्जेन्टिना', 'Germany', 'जर्मनी'),
    ('In which month did Pope Francis die in 2025?', 'सन् २०२५ मा पोप फ्रान्सिस कुन महिनामा बिते?', 'April 2025', 'अप्रिल २०२५', 'January 2025', 'जनवरी २०२५', 'May 2025', 'मे २०२५', 'March 2025', 'मार्च २०२५'),
    ('Which cities hosted the Winter Olympics 2026?', 'सन् २०२६ को शीतकालीन ओलम्पिक कुन सहरहरूले आयोजना गरे?', 'Milan and Cortina, Italy', 'मिलान र कोर्टिना, इटाली', 'Beijing, China', 'बेइजिङ, चीन', 'Paris, France', 'पेरिस, फ्रान्स', 'Tokyo, Japan', 'टोकियो, जापान'),
    ('Which city hosted the Commonwealth Games 2026?', 'सन् २०२६ को राष्ट्रमण्डल खेलकुद कुन सहरले आयोजना गर्यो?', 'Glasgow, Scotland', 'ग्लासगो, स्कटल्यान्ड', 'Birmingham, England', 'बर्मिङ्घम, इङ्ग्ल्यान्ड', 'Gold Coast, Australia', 'गोल्ड कोस्ट, अस्ट्रेलिया', 'Delhi, India', 'दिल्ली, भारत'),
    ('Who is the Prime Minister of India (as of 2026)?', 'सन् २०२६ सम्म भारतका प्रधानमन्त्री को हुन्?', 'Narendra Modi', 'नरेन्द्र मोदी', 'Rahul Gandhi', 'राहुल गान्धी', 'Amit Shah', 'अमित शाह', 'Manmohan Singh', 'मनमोहन सिंह'),
    ('Who is the President of the United States (as of 2026)?', 'सन् २०२६ सम्म संयुक्त राज्य अमेरिकाका राष्ट्रपति को हुन्?', 'Donald Trump', 'डोनाल्ड ट्रम्प', 'Joe Biden', 'जो बाइडेन', 'Barack Obama', 'बराक ओबामा', 'Kamala Harris', 'कमला ह्यारिस'),
    ('In which year did Donald Trump begin his second term as US President?', 'डोनाल्ड ट्रम्पले अमेरिकी राष्ट्रपतिको दोस्रो कार्यकाल कुन वर्ष सुरु गरे?', '2025', 'सन् २०२५', '2021', 'सन् २०२१', '2017', 'सन् २०१७', '2024', 'सन् २०२४'),
    ('Which two countries fought a 12-day war in June 2025?', 'सन् २०२५ जुनमा कुन दुई देशबीच १२ दिने युद्ध भयो?', 'Israel and Iran', 'इजरायल र इरान', 'India and Pakistan', 'भारत र पाकिस्तान', 'Russia and Ukraine', 'रुस र युक्रेन', 'Thailand and Cambodia', 'थाइल्यान्ड र कम्बोडिया'),
    ('Which operation did India launch against Pakistan in May 2025?', 'सन् २०२५ मे मा भारतले पाकिस्तानविरुद्ध कुन अपरेसन सुरु गर्यो?', 'Operation Sindoor', 'अपरेसन सिन्दूर', 'Operation Vijay', 'अपरेसन विजय', 'Operation Meghdoot', 'अपरेसन मेघदूत', 'Operation Parakram', 'अपरेसन पराक्रम'),
    ('What is the population of Nepal according to the 2021 census?', 'सन् २०२१ को जनगणनाअनुसार नेपालको जनसङ्ख्या कति छ?', '29,164,578', '२९,१६४,५७८', '26,494,504', '२६,४९४,५०४', '30,000,000', '३०,०००,०००', '28,000,000', '२८,०००,०००'),
    ('Which is the most populous province of Nepal (2021 census)?', 'सन् २०२१ को जनगणनाअनुसार नेपालको सबैभन्दा धेरै जनसङ्ख्या भएको प्रदेश कुन हो?', 'Bagmati', 'बागमती', 'Madhesh', 'मधेश', 'Lumbini', 'लुम्बिनी', 'Koshi', 'कोशी'),
    ('Which is the least populous province of Nepal (2021 census)?', 'सन् २०२१ को जनगणनाअनुसार नेपालको सबैभन्दा कम जनसङ्ख्या भएको प्रदेश कुन हो?', 'Karnali', 'कर्णाली', 'Sudurpashchim', 'सुदूरपश्चिम', 'Gandaki', 'गण्डकी', 'Madhesh', 'मधेश'),
    ('What is the literacy rate of Nepal (2021 census)?', 'सन् २०२१ को जनगणनाअनुसार नेपालको साक्षरता दर कति छ?', '76.2%', '७६.२%', '65.9%', '६५.९%', '71.2%', '७१.२%', '81.5%', '८१.५%'),
    ('Which district is the most populous in Nepal (2021 census)?', 'सन् २०२१ को जनगणनाअनुसार नेपालको सबैभन्दा धेरै जनसङ्ख्या भएको जिल्ला कुन हो?', 'Kathmandu', 'काठमाडौँ', 'Morang', 'मोरङ', 'Rupandehi', 'रुपन्देही', 'Jhapa', 'झापा'),
    ('Which district is the least populous in Nepal (2021 census)?', 'सन् २०२१ को जनगणनाअनुसार नेपालको सबैभन्दा कम जनसङ्ख्या भएको जिल्ला कुन हो?', 'Manang', 'मनाङ', 'Dolpa', 'डोल्पा', 'Mugu', 'मुगु', 'Humla', 'हुम्ला'),
    ('What is the population growth rate of Nepal (2021 census)?', 'सन् २०२१ को जनगणनाअनुसार नेपालको जनसङ्ख्या वृद्धि दर कति छ?', '0.92% per year', 'प्रतिवर्ष ०.९२%', '1.35% per year', 'प्रतिवर्ष १.३५%', '1.8% per year', 'प्रतिवर्ष १.८%', '2.1% per year', 'प्रतिवर्ष २.१%'),
    ('What is the sex ratio of Nepal (2021 census)?', 'सन् २०२१ को जनगणनाअनुसार नेपालको लिङ्ग अनुपात कति छ?', '95.59 males per 100 females', 'प्रति १०० महिला ९५.५९ पुरुष', '100 males per 100 females', 'प्रति १०० महिला १०० पुरुष', '94.2 males per 100 females', 'प्रति १०० महिला ९४.२ पुरुष', '99.5 males per 100 females', 'प्रति १०० महिला ९९.५ पुरुष'),
    ('Which is the largest caste/ethnic group in Nepal (2021 census)?', 'सन् २०२१ को जनगणनाअनुसार नेपालको सबैभन्दा ठूलो जातीय समूह कुन हो?', 'Chhetri', 'क्षेत्री', 'Brahman-Hill', 'पहाडी ब्राह्मण', 'Magar', 'मगर', 'Tharu', 'थारू'),
    ('Which language is spoken by the most people in Nepal (2021 census)?', 'सन् २०२१ को जनगणनाअनुसार नेपालमा सबैभन्दा धेरै मानिसले बोल्ने भाषा कुन हो?', 'Nepali', 'नेपाली', 'Maithili', 'मैथिली', 'Bhojpuri', 'भोजपुरी', 'Tharu', 'थारू'),
    ('Which is the second most spoken language in Nepal (2021 census)?', 'सन् २०२१ को जनगणनाअनुसार नेपालमा दोस्रो धेरै बोलिने भाषा कुन हो?', 'Maithili', 'मैथिली', 'Bhojpuri', 'भोजपुरी', 'Tharu', 'थारू', 'Tamang', 'तामाङ'),
]
for row in WORLD:
    fact(*row, sub='World Events 2025-26')

n = em.write('expansion-r10-current.json')
print('CURRENT TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:10]:
    print('  REJ', r)
