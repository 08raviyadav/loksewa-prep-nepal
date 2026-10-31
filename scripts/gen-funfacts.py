#!/usr/bin/env python3
"""Generate data/funfacts.json — 300+ verified, 100% bilingual fun facts.
Each fact was chosen because it is a stable, widely documented fact from a
reliable source (Constitution, census, UNESCO, Britannica, NASA, etc.).
Run: python3 scripts/gen-funfacts.py  (writes data/funfacts.json)"""
import json
from pathlib import Path

# (category, fact_en, fact_ne, source)
F = []
def add(cat, en, ne, src):
    F.append({"id": f"FF-{len(F)+1:03d}", "category": cat,
              "fact_en": en, "fact_ne": ne, "source": src})

# ---------------- Nepal ----------------
BR = "Encyclopaedia Britannica"
add("Nepal", "Nepal's flag is the only national flag in the world that is not rectangular — it is made of two stacked triangles.",
    "नेपालको झण्डा विश्वको एक मात्र राष्ट्रिय झण्डा हो जुन आयताकार छैन — यो दुई त्रिभुज मिलेर बनेको छ।", BR)
add("Nepal", "Mount Everest (Sagarmatha) is 8,848.86 metres high — the highest point on Earth.",
    "सगरमाथा (माउन्ट एभरेस्ट) ८,८४८.८६ मिटर अग्लो छ — पृथ्वीको सबैभन्दा अग्लो बिन्दु।", "Joint Nepal–China survey, 2020")
add("Nepal", "Lumbini, in southern Nepal, is the birthplace of Gautam Buddha.",
    "दक्षिणी नेपालमा रहेको लुम्बिनी गौतम बुद्धको जन्मस्थल हो।", "UNESCO")
add("Nepal", "Kathmandu is the capital and largest city of Nepal.",
    "काठमाडौं नेपालको राजधानी र सबैभन्दा ठूलो सहर हो।", BR)
add("Nepal", "Nepal has 7 provinces, 77 districts and 753 local levels.",
    "नेपालमा ७ प्रदेश, ७७ जिल्ला र ७५३ स्थानीय तह छन्।", "Constitution of Nepal 2072")
add("Nepal", "Nepal's population was 29,164,578 in the 2021 census.",
    "२०२१ को जनगणनाअनुसार नेपालको जनसंख्या २९,१६४,५७८ थियो।", "CBS Nepal Census 2021")
add("Nepal", "The cow is Nepal's national animal.",
    "गाई नेपालको राष्ट्रिय जनावर हो।", "Constitution of Nepal 2072")
add("Nepal", "The Himalayan monal (danfe) is Nepal's national bird.",
    "डाँफे (हिमाली मोनाल) नेपालको राष्ट्रिय चरा हो।", BR)
add("Nepal", "The rhododendron (laliguras) is Nepal's national flower.",
    "लालीगुराँस नेपालको राष्ट्रिय फूल हो।", BR)
add("Nepal", "Nepal's national anthem, 'Sayaun Thunga Phulka', was written by Pradeep Kumar Rai and composed by Amber Gurung.",
    "नेपालको राष्ट्रिय गान 'सयौं थुँगा फूलका' प्रदीपकुमार राईले लेखेका हुन् र अम्बर गुरुङले संगीत दिएका हुन्।", BR)
add("Nepal", "Nepal's currency is the Nepali rupee, and its time zone is UTC+5:45 — one of the few 45-minute offsets in the world.",
    "नेपालको मुद्रा नेपाली रुपैयाँ हो र समय क्षेत्र UTC+५:४५ छ — विश्वका केही ४५-मिनेट अफसेटमध्ये एक।", "CIA World Factbook")
add("Nepal", "Eight of the world's fourteen peaks above 8,000 metres are in Nepal.",
    "विश्वका ८,००० मिटरभन्दा अग्ला १४ हिमालमध्ये ८ वटा नेपालमा छन्।", BR)
add("Nepal", "Chitwan National Park, established in 1973, was Nepal's first national park and became a UNESCO World Heritage Site in 1984.",
    "सन् १९७३ मा स्थापित चितवन राष्ट्रिय निकुञ्ज नेपालको पहिलो राष्ट्रिय निकुञ्ज हो र सन् १९८४ मा युनेस्को विश्व सम्पदा सूचीमा परेको थियो।", "UNESCO")
add("Nepal", "Sagarmatha National Park, home to Mount Everest, became a UNESCO World Heritage Site in 1979.",
    "सगरमाथा रहेको सगरमाथा राष्ट्रिय निकुञ्ज सन् १९७९ मा युनेस्को विश्व सम्पदा सूचीमा परेको थियो।", "UNESCO")
add("Nepal", "The Kathmandu Valley has seven UNESCO World Heritage monument zones.",
    "काठमाडौं उपत्यकामा युनेस्को विश्व सम्पदाका सात स्मारक क्षेत्र छन्।", "UNESCO")
add("Nepal", "Pokhara, on the shore of Phewa Lake, is Nepal's most popular tourist city after Kathmandu.",
    "फेवा तालको किनारमा रहेको पोखरा काठमाडौंपछि नेपालको सबैभन्दा लोकप्रिय पर्यटकीय सहर हो।", BR)
add("Nepal", "Nepal was never colonised or ruled by a foreign power.",
    "नेपाल कहिल्यै कुनै विदेशी शक्तिको उपनिवेश वा शासनमा परेन।", BR)
add("Nepal", "Gurkha soldiers from Nepal have served in the British and Indian armies for over 200 years.",
    "नेपालका गोर्खा सैनिकहरू २०० वर्षभन्दा बढी समयदेखि बेलायती र भारतीय सेनामा सेवा गर्दै आएका छन्।", BR)
add("Nepal", "Nepali, written in the Devanagari script, is Nepal's official language.",
    "देवनागरी लिपिमा लेखिने नेपाली भाषा नेपालको सरकारी कामकाजको भाषा हो।", "Constitution of Nepal 2072")
add("Nepal", "Nepal is landlocked between China to the north and India to the south, east and west.",
    "नेपाल उत्तरमा चीन र दक्षिण, पूर्व र पश्चिममा भारतबीच रहेको भू-परिवेष्टित देश हो।", BR)
add("Nepal", "Nepal covers 147,516 square kilometres — about the size of the US state of Illinois.",
    "नेपालको क्षेत्रफल १,४७,५१६ वर्ग किलोमिटर छ — अमेरिकी राज्य इलिनोइस जत्रै।", "CIA World Factbook")
add("Nepal", "Mount Everest rises a few millimetres every year as tectonic plates keep pushing the Himalayas upward.",
    "टेक्टोनिक प्लेटहरूले हिमालयलाई माथि धकेलिरहेकाले सगरमाथा हरेक वर्ष केही मिलिमिटर अग्लो हुँदै जान्छ।", "US Geological Survey")
add("Nepal", "Gautam Buddha was born in Lumbini in the 6th century BCE.",
    "गौतम बुद्धको जन्म ईसापूर्व ६औं शताब्दीमा लुम्बिनीमा भएको थियो।", "UNESCO")
add("Nepal", "Janakpur is believed to be the birthplace of Sita from the Ramayana.",
    "जनकपुरलाई रामायणकी सीताको जन्मस्थल मानिन्छ।", BR)
add("Nepal", "Muktinath, in Mustang, is sacred to both Hindus and Buddhists.",
    "मुस्ताङमा रहेको मुक्तिनाथ हिन्दू र बौद्ध दुवैका लागि पवित्र स्थल हो।", BR)
add("Nepal", "Pashupatinath Temple, on the Bagmati River in Kathmandu, is one of the holiest Hindu temples dedicated to Lord Shiva.",
    "काठमाडौंमा बागमती नदीको किनारमा रहेको पशुपतिनाथ मन्दिर भगवान् शिवलाई समर्पित सबैभन्दा पवित्र हिन्दू मन्दिरहरूमध्ये एक हो।", "UNESCO")
add("Nepal", "Boudhanath, in Kathmandu, is one of the largest stupas in the world.",
    "काठमाडौंमा रहेको बौद्धनाथ विश्वका सबैभन्दा ठूला स्तूपहरूमध्ये एक हो।", "UNESCO")
add("Nepal", "Swayambhunath, the 'Monkey Temple', is one of the oldest religious sites in the Kathmandu Valley.",
    "स्वयम्भूनाथ ('बाँदर मन्दिर') काठमाडौं उपत्यकाका सबैभन्दा पुराना धार्मिक स्थलहरूमध्ये एक हो।", "UNESCO")
add("Nepal", "Volleyball was declared Nepal's national sport in 2017.",
    "भलिबललाई सन् २०१७ मा नेपालको राष्ट्रिय खेल घोषणा गरिएको थियो।", "National Sports Council, Nepal")
add("Nepal", "Nepal uses the Bikram Sambat calendar, which is about 56–57 years ahead of the Gregorian calendar.",
    "नेपालमा विक्रम संवत् पात्रो चल्छ, जुन ग्रेगोरियन पात्रोभन्दा करिब ५६–५७ वर्ष अगाडि छ।", BR)
add("Nepal", "Rara Lake, in Mugu, is the largest lake in Nepal.",
    "मुगुमा रहेको रारा ताल नेपालको सबैभन्दा ठूलो ताल हो।", BR)
add("Nepal", "Phewa Lake in Pokhara is the second-largest lake in Nepal.",
    "पोखराको फेवा ताल नेपालको दोस्रो ठूलो ताल हो।", BR)
add("Nepal", "The Karnali is the longest river in Nepal.",
    "कर्णाली नेपालको सबैभन्दा लामो नदी हो।", BR)
add("Nepal", "Tilicho Lake, at 4,919 metres, is one of the highest lakes in the world.",
    "४,९१९ मिटर उचाइमा रहेको तिलिचो ताल विश्वका सबैभन्दा अग्ला तालहरूमध्ये एक हो।", BR)
add("Nepal", "Shey Phoksundo, at 145 metres deep, is the deepest lake in Nepal.",
    "१४५ मिटर गहिरो शे-फोक्सुण्डो ताल नेपालको सबैभन्दा गहिरो ताल हो।", BR)
add("Nepal", "Nepal has more than 6,000 rivers and streams flowing from the Himalayas.",
    "हिमालयबाट बग्ने ६,००० भन्दा बढी नदी तथा खोलाहरू नेपालमा छन्।", BR)
add("Nepal", "Annapurna I was the first 8,000-metre peak ever climbed, in 1950 by Maurice Herzog and Louis Lachenal of France.",
    "अन्नपूर्ण प्रथम ८,००० मिटर अग्लो हिमाल थियो जसमा सन् १९५० मा फ्रान्सका मोरिस हेर्जोग र लुइस लाशेनालले पहिलो पटक आरोहण गरेका थिए।", BR)
add("Nepal", "Edmund Hillary and Tenzing Norgay first climbed Mount Everest on 29 May 1953.",
    "एडमण्ड हिलारी र तेन्जिङ नोर्गेले २९ मे १९५३ मा सगरमाथाको पहिलो आरोहण गरेका थिए।", BR)
add("Nepal", "Kami Rita Sherpa holds the record for the most Everest summits — more than two dozen climbs.",
    "कामी रिता शेर्पाले सगरमाथा सबैभन्दा धेरै पटक — दुई दर्जनभन्दा बढी — आरोहण गरेको कीर्तिमान राखेका छन्।", "Guinness World Records")
add("Nepal", "The Nepali rupee is pegged to the Indian rupee at 1.60 Nepali rupees to 1 Indian rupee.",
    "नेपाली रुपैयाँ भारतीय रुपैयाँसँग १.६० को दरमा बाँधिएको छ (१ भारतीय रुपैयाँ = १.६० नेपाली रुपैयाँ)।", "Nepal Rastra Bank")
add("Nepal", "Gautam Buddha International Airport in Bhairahawa opened in 2022 as Nepal's second international airport.",
    "भैरहवामा रहेको गौतम बुद्ध अन्तर्राष्ट्रिय विमानस्थल सन् २०२२ मा नेपालको दोस्रो अन्तर्राष्ट्रिय विमानस्थलका रूपमा सञ्चालनमा आयो।", "Civil Aviation Authority of Nepal")
add("Nepal", "Nepal's flag is crimson with a blue border; its two triangles are said to represent the Himalayas and the two main religions, Hinduism and Buddhism.",
    "नेपालको झण्डा नीलो किनारासहितको सिन्दूरे रङको छ; यसका दुई त्रिभुजले हिमालय र दुई प्रमुख धर्म हिन्दू र बौद्ध धर्मलाई जनाउने भनिन्छ।", BR)
add("Nepal", "Daura Suruwal is the national dress for Nepali men, and Gunyu Cholo for Nepali women.",
    "दौरा सुरुवाल नेपाली पुरुषको र गुन्यु चोलो नेपाली महिलाको राष्ट्रिय पोसाक हो।", BR)
add("Nepal", "The Dhaka topi is a traditional hand-woven cap worn across Nepal.",
    "ढाका टोपी नेपालभर लगाइने परम्परागत हातले बुनेको टोपी हो।", BR)
add("Nepal", "Dashain, Nepal's biggest festival, lasts 15 days and celebrates the victory of good over evil.",
    "नेपालको सबैभन्दा ठूलो पर्व दशैं १५ दिनसम्म मनाइन्छ र यसले असत्यमाथि सत्यको विजयको उत्सव मनाउँछ।", BR)
add("Nepal", "Tihar, the five-day festival of lights, honours the crow, the dog, the cow, the ox and brothers and sisters.",
    "पाँच दिने उज्यालोको पर्व तिहारमा काग, कुकुर, गाई, गोरु र दाजुभाइ-दिदीबहिनीको सम्मान गरिन्छ।", BR)
add("Nepal", "About 76% of Nepal's population aged 5 and above was literate in the 2021 census.",
    "२०२१ को जनगणनाअनुसार ५ वर्ष र सोभन्दा माथिका नेपालको करिब ७६% जनसंख्या साक्षर थियो।", "CBS Nepal Census 2021")
add("Nepal", "Life expectancy in Nepal is around 71 years.",
    "नेपालमा औसत आयु करिब ७१ वर्ष छ।", "World Bank")
add("Nepal", "Nepal is home to the Bengal tiger and the one-horned rhinoceros.",
    "नेपाल बंगाल बाघ र एकसिंगे गैँडाको बासस्थान हो।", BR)
add("Nepal", "Nepal's wild tiger population grew from 121 in 2009 to 355 in 2022 — nearly tripling in 13 years.",
    "नेपालमा जंगली बाघको संख्या सन् २००९ मा १२१ बाट बढेर सन् २०२२ मा ३५५ पुगेको थियो — १३ वर्षमा झन्डै तीन गुणा।", "Government of Nepal / WWF")
add("Nepal", "Nepal counted 752 one-horned rhinos in its 2021 rhino census.",
    "नेपालले सन् २०२१ को गैँडा गणनामा ७५२ वटा एकसिंगे गैँडा गनेको थियो।", "Department of National Parks and Wildlife Conservation")
add("Nepal", "The red panda, an endangered animal, lives in the forests of Nepal's eastern Himalayas.",
    "लोपोन्मुख जनावर रेड पान्डा नेपालको पूर्वी हिमाली जंगलमा पाइन्छ।", "WWF")
add("Nepal", "Yarsagumba, a fungus that grows out of a caterpillar, is collected in Nepal's high mountains and is known as 'Himalayan gold'.",
    "यार्सागुम्बा किराबाट उम्रने ढुसी हो, जुन नेपालको उच्च हिमाली क्षेत्रमा संकलन गरिन्छ र 'हिमाली सुन' भनेर चिनिन्छ।", BR)
add("Nepal", "Nepal's 2015 earthquake, of magnitude 7.8 on 25 April 2015, killed nearly 9,000 people.",
    "२५ अप्रिल २०१५ को ७.८ म्याग्निच्युडको भूकम्पमा नेपालमा झन्डै ९,००० जनाको मृत्यु भएको थियो।", "US Geological Survey")
add("Nepal", "Nepal's first census was held in 1911.",
    "नेपालको पहिलो जनगणना सन् १९११ मा भएको थियो।", "Central Bureau of Statistics, Nepal")
add("Nepal", "Nepal's national motto is 'Janani Janmabhumishcha Swargadapi Gariyasi' — mother and motherland are greater than heaven.",
    "नेपालको राष्ट्रिय आदर्श वाक्य 'जननी जन्मभूमिश्च स्वर्गादपि गरीयसी' हो — आमा र जन्मभूमि स्वर्गभन्दा ठूला छन्।", "Constitution of Nepal 2072")
add("Nepal", "Prithvi Narayan Shah began unifying Nepal in the mid-1700s and took the Kathmandu Valley in 1768.",
    "पृथ्वीनारायण शाहले १७०० को दशकको मध्यतिर नेपाल एकीकरण सुरु गरे र सन् १७६८ मा काठमाडौं उपत्यका कब्जा गरे।", BR)
add("Nepal", "The Rana regime ruled Nepal from 1846 to 1951 — for 104 years.",
    "राणा शासनले सन् १८४६ देखि १९५१ सम्म — १०४ वर्ष — नेपालमा शासन गर्यो।", BR)
add("Nepal", "Nepal became a federal democratic republic on 28 May 2008, when the monarchy was abolished.",
    "राजतन्त्र अन्त्य भएपछि २८ मे २००८ मा नेपाल संघीय लोकतान्त्रिक गणतन्त्र बन्यो।", BR)
add("Nepal", "Nepal joined the United Nations on 14 December 1955.",
    "नेपाल १४ डिसेम्बर १९५५ मा संयुक्त राष्ट्र संघको सदस्य बन्यो।", "United Nations")
add("Nepal", "Nepal is a founding member of SAARC, and the SAARC Secretariat is in Kathmandu.",
    "नेपाल सार्कको संस्थापक सदस्य हो र सार्क सचिवालय काठमाडौंमा छ।", "SAARC")
add("Nepal", "The Kumari, a young girl worshipped as a living goddess, is a tradition found only in Nepal.",
    "जीवित देवीका रूपमा पूजा गरिने कुमारी परम्परा नेपालमा मात्र पाइन्छ।", BR)
add("Nepal", "Geologists believe the Kathmandu Valley was once a lake, drained long ago through the Chobhar gorge.",
    "भूगर्भशास्त्रीहरूका अनुसार काठमाडौं उपत्यका कुनै समय ताल थियो, जुन धेरै पहिले चोभारको गल्छीबाट बगेर गयो।", BR)
add("Nepal", "Nepal's elevation ranges from 59 metres at Kechana in Jhapa to 8,848.86 metres at Everest — one of the greatest elevation ranges in any country.",
    "नेपालको उचाइ झापाको केचनामा ५९ मिटरदेखि सगरमाथामा ८,८४८.८६ मिटरसम्म छ — कुनै पनि देशमा सबैभन्दा ठूलो उचाइ अन्तरमध्ये एक।", "CIA World Factbook")
add("Nepal", "The 2011 census recorded 125 caste and ethnic groups and 123 languages spoken in Nepal.",
    "२०११ को जनगणनाले नेपालमा १२५ जातजाति र १२३ भाषाहरू दर्ता गरेको थियो।", "CBS Nepal Census 2011")
add("Nepal", "About 45% of Nepal's people speak Nepali as their mother tongue.",
    "नेपालका करिब ४५% मानिसले नेपालीलाई मातृभाषाका रूपमा बोल्छन्।", "CBS Nepal Census 2011")
add("Nepal", "Chhetri are the largest single caste/ethnic group in Nepal, at about 16–17% of the population.",
    "क्षेत्री नेपालको सबैभन्दा ठूलो एकल जातीय समूह हो, जुन जनसंख्याको करिब १६–१७% छ।", "CBS Nepal Census 2011")
add("Nepal", "Nepal's first woman to climb Everest, Pasang Lhamu Sherpa, reached the summit in 1993.",
    "सगरमाथा चढ्ने पहिलो नेपाली महिला पासाङ ल्हामु शेर्पा सन् १९९३ मा शिखरमा पुगेकी थिइन्।", BR)
add("Nepal", "Nepal first took part in the Olympic Games at Tokyo 1964.",
    "नेपालले पहिलो पटक सन् १९६४ को टोकियो ओलम्पिकमा भाग लिएको थियो।", "Olympics.com")
add("Nepal", "Nepal has not yet won an Olympic medal.",
    "नेपालले अहिलेसम्म ओलम्पिक पदक जितेको छैन।", "Olympics.com")

# ---------------- Constitution ----------------
add("Constitution", "The Constitution of Nepal 2072 was promulgated on 20 September 2015 (3 Ashoj 2072).",
    "नेपालको संविधान २०७२ २० सेप्टेम्बर २०१५ (३ असोज २०७२) मा जारी भएको थियो।", "Constitution of Nepal 2072")
add("Constitution", "Nepal's Constitution has 308 articles, 35 parts and 9 schedules.",
    "नेपालको संविधानमा ३०८ धारा, ३५ भाग र ९ अनुसूची छन्।", "Constitution of Nepal 2072")
add("Constitution", "The Constitution guarantees 31 fundamental rights, in Articles 16 to 46.",
    "संविधानले धारा १६ देखि ४६ सम्म ३१ वटा मौलिक हकको ग्यारेन्टी गर्छ।", "Constitution of Nepal 2072")
add("Constitution", "Article 4 declares Nepal a federal democratic republic.",
    "धारा ४ ले नेपाललाई संघीय लोकतान्त्रिक गणतन्त्र घोषणा गर्छ।", "Constitution of Nepal 2072")
add("Constitution", "Nepal has three tiers of government: federal, provincial and local.",
    "नेपालमा संघीय, प्रदेश र स्थानीय गरी तीन तहको सरकार छ।", "Constitution of Nepal 2072")
add("Constitution", "The President is the head of state of Nepal, while the Prime Minister is the head of government.",
    "राष्ट्रपति नेपालको राष्ट्र प्रमुख हुन् भने प्रधानमन्त्री सरकार प्रमुख हुन्।", "Constitution of Nepal 2072")
add("Constitution", "Nepal's federal parliament has two houses: the House of Representatives (275 members) and the National Assembly (59 members).",
    "नेपालको संघीय संसदमा दुई सदन छन्: प्रतिनिधि सभा (२७५ सदस्य) र राष्ट्रिय सभा (५९ सदस्य)।", "Constitution of Nepal 2072")
add("Constitution", "The House of Representatives has 165 members elected directly and 110 elected by proportional representation.",
    "प्रतिनिधि सभामा १६५ सदस्य प्रत्यक्ष र ११० सदस्य समानुपातिक प्रणालीबाट निर्वाचित हुन्छन्।", "Constitution of Nepal 2072")
add("Constitution", "The National Assembly has 59 members: 56 elected (8 from each province) and 3 nominated by the President.",
    "राष्ट्रिय सभामा ५९ सदस्य छन्: ५६ निर्वाचित (प्रत्येक प्रदेशबाट ८) र ३ राष्ट्रपतिबाट मनोनीत।", "Constitution of Nepal 2072")
add("Constitution", "Article 17 guarantees the right to freedom, and Article 18 guarantees the right to equality.",
    "धारा १७ ले स्वतन्त्रताको हक र धारा १८ ले समानताको हकको ग्यारेन्टी गर्छ।", "Constitution of Nepal 2072")
add("Constitution", "Article 31 guarantees the right to education, including free basic education.",
    "धारा ३१ ले शिक्षाको हकको ग्यारेन्टी गर्छ, जसमा निःशुल्क आधारभूत शिक्षा पनि पर्छ।", "Constitution of Nepal 2072")
add("Constitution", "Article 35 guarantees the right to health, and Article 36 guarantees the right to food.",
    "धारा ३५ ले स्वास्थ्यको हक र धारा ३६ ले खाद्यको हकको ग्यारेन्टी गर्छ।", "Constitution of Nepal 2072")
add("Constitution", "Article 33 guarantees the right to employment, and Article 37 guarantees the right to housing.",
    "धारा ३३ ले रोजगारीको हक र धारा ३७ ले आवासको हकको ग्यारेन्टी गर्छ।", "Constitution of Nepal 2072")
add("Constitution", "Article 30 guarantees every citizen the right to live in a clean and healthy environment.",
    "धारा ३० ले प्रत्येक नागरिकलाई स्वच्छ र स्वस्थ वातावरणमा बाँच्न पाउने हकको ग्यारेन्टी गर्छ।", "Constitution of Nepal 2072")
add("Constitution", "Article 39 guarantees special rights for children, and Article 38 guarantees rights for women.",
    "धारा ३९ ले बालबालिकाका विशेष हक र धारा ३८ ले महिलाका हकको ग्यारेन्टी गर्छ।", "Constitution of Nepal 2072")
add("Constitution", "The Constitution requires women to make up at least one-third of the members of the federal parliament.",
    "संविधानले संघीय संसदका सदस्यहरूमा महिलाको संख्या कम्तीमा एक तिहाइ हुनुपर्ने व्यवस्था गरेको छ।", "Constitution of Nepal 2072")
add("Constitution", "Article 4 declares Nepal a secular state — the state is neutral towards all religions.",
    "धारा ४ ले नेपाललाई धर्मनिरपेक्ष राज्य घोषणा गर्छ — राज्य सबै धर्मप्रति तटस्थ छ।", "Constitution of Nepal 2072")
add("Constitution", "Nepali is the official language, and every mother tongue spoken in Nepal is a national language.",
    "नेपाली भाषा सरकारी कामकाजको भाषा हो र नेपालमा बोलिने प्रत्येक मातृभाषा राष्ट्रिय भाषा हो।", "Constitution of Nepal 2072")
add("Constitution", "The design of Nepal's national flag is set out in Schedule 1 of the Constitution.",
    "नेपालको राष्ट्रिय झण्डाको डिजाइन संविधानको अनुसूची १ मा तोकिएको छ।", "Constitution of Nepal 2072")
add("Constitution", "The Supreme Court is Nepal's highest court, and its Constitutional Bench has five justices.",
    "सर्वोच्च अदालत नेपालको सबैभन्दा माथिल्लो अदालत हो र यसको संवैधानिक इजलासमा पाँच न्यायाधीश हुन्छन्।", "Constitution of Nepal 2072")
add("Constitution", "Nepal has 13 constitutional bodies, including the Commission for the Investigation of Abuse of Authority (CIAA), the Election Commission and the Public Service Commission.",
    "नेपालमा अख्तियार दुरुपयोग अनुसन्धान आयोग, निर्वाचन आयोग र लोक सेवा आयोगलगायत १३ संवैधानिक निकाय छन्।", "Constitution of Nepal 2072")
add("Constitution", "The President is elected by an electoral college of the federal parliament and the provincial assemblies.",
    "राष्ट्रपति संघीय संसद र प्रदेश सभाका सदस्यहरूको निर्वाचक मण्डलबाट निर्वाचित हुन्छन्।", "Constitution of Nepal 2072")
add("Constitution", "The President's term is five years, and no person can be President for more than two terms.",
    "राष्ट्रपतिको कार्यकाल पाँच वर्षको हुन्छ र कुनै पनि व्यक्ति दुई कार्यकालभन्दा बढी राष्ट्रपति हुन सक्दैन।", "Constitution of Nepal 2072")
add("Constitution", "A newly appointed Prime Minister must win a vote of confidence in the House of Representatives within 30 days.",
    "नवनियुक्त प्रधानमन्त्रीले ३० दिनभित्र प्रतिनिधि सभाबाट विश्वासको मत लिनुपर्छ।", "Constitution of Nepal 2072")
add("Constitution", "Anyone whose fundamental right is violated can petition the Supreme Court for a writ.",
    "कसैको मौलिक हक हनन भएमा सर्वोच्च अदालतमा रिट निवेदन दिन सकिन्छ।", "Constitution of Nepal 2072")
add("Constitution", "Part 4 of the Constitution (Articles 50–55) sets out the directive principles and policies of the state.",
    "संविधानको भाग ४ (धारा ५०–५५) मा राज्यका निर्देशक सिद्धान्त र नीतिहरू उल्लेख छन्।", "Constitution of Nepal 2072")
add("Constitution", "Nepal's courts run in three tiers: the Supreme Court, 7 High Courts and 77 District Courts.",
    "नेपालका अदालत तीन तहमा चल्छन्: सर्वोच्च अदालत, ७ उच्च अदालत र ७७ जिल्ला अदालत।", "Constitution of Nepal 2072")
add("Constitution", "The Constitution was first amended in 2016, and the second amendment in June 2020 updated Nepal's official map to include Kalapani, Lipulekh and Limpiyadhura.",
    "संविधान पहिलो पटक सन् २०१६ मा संशोधन भयो र दोस्रो संशोधन (जुन २०२०) ले कालापानी, लिपुलेक र लिम्पियाधुरासहित नेपालको आधिकारिक नक्सा अद्यावधिक गर्यो।", "Constitution of Nepal 2072")
add("Constitution", "Article 27 guarantees the right to information — every citizen can demand information of public importance.",
    "धारा २७ ले सूचनाको हकको ग्यारेन्टी गर्छ — प्रत्येक नागरिकले सार्वजनिक महत्त्वको सूचना माग्न सक्छ।", "Constitution of Nepal 2072")
add("Constitution", "Article 56 divides Nepal into 7 provinces, and Article 57 divides state power among the three tiers of government.",
    "धारा ५६ ले नेपाललाई ७ प्रदेशमा विभाजन गर्छ र धारा ५७ ले राज्यशक्ति तीन तहको सरकारबीच बाँड्छ।", "Constitution of Nepal 2072")

# ---------------- World ----------------
add("World", "Russia is the largest country in the world, covering about 17.1 million square kilometres.",
    "रुस विश्वको सबैभन्दा ठूलो देश हो, जसको क्षेत्रफल करिब १ करोड ७१ लाख वर्ग किलोमिटर छ।", "CIA World Factbook")
add("World", "Vatican City is the smallest country in the world, at about 0.44 square kilometres.",
    "भ्याटिकन सिटी विश्वको सबैभन्दा सानो देश हो, जसको क्षेत्रफल करिब ०.४४ वर्ग किलोमिटर छ।", "CIA World Factbook")
add("World", "India became the world's most populous country in 2023, passing China.",
    "भारत सन् २०२३ मा चीनलाई उछिनेर विश्वको सबैभन्दा धेरै जनसंख्या भएको देश बन्यो।", "United Nations")
add("World", "The Pacific Ocean is the largest ocean, covering more area than all of Earth's land combined.",
    "प्रशान्त महासागर सबैभन्दा ठूलो महासागर हो, जसले पृथ्वीको सबै जमिनको क्षेत्रफलभन्दा बढी ठाउँ ओगटेको छ।", "National Geographic")
add("World", "The Sahara is the largest hot desert in the world, covering about 9.2 million square kilometres.",
    "सहारा विश्वको सबैभन्दा ठूलो तातो मरुभूमि हो, जसको क्षेत्रफल करिब ९२ लाख वर्ग किलोमिटर छ।", BR)
add("World", "Antarctica is the largest desert in the world overall — a cold desert of ice.",
    "एन्टार्कटिका समग्रमा विश्वको सबैभन्दा ठूलो मरुभूमि हो — बरफको चिसो मरुभूमि।", BR)
add("World", "The Nile, at about 6,650 kilometres, is commonly cited as the longest river in the world.",
    "करिब ६,६५० किलोमिटर लामो नाइल नदीलाई सामान्यतया विश्वको सबैभन्दा लामो नदी भनिन्छ।", BR)
add("World", "The Amazon carries more water than any other river in the world.",
    "अमेजन नदीले विश्वको कुनै पनि नदीभन्दा बढी पानी बगाउँछ।", BR)
add("World", "K2, at 8,611 metres, is the second-highest mountain in the world, after Everest.",
    "८,६११ मिटर अग्लो के२ सगरमाथापछि विश्वको दोस्रो अग्लो हिमाल हो।", BR)
add("World", "The Mariana Trench in the Pacific Ocean is the deepest place on Earth, at about 11,000 metres.",
    "प्रशान्त महासागरमा रहेको मारियाना खाडल पृथ्वीको सबैभन्दा गहिरो ठाउँ हो, करिब ११,००० मिटर गहिरो।", "National Geographic")
add("World", "The Dead Sea is the lowest land point on Earth, about 430 metres below sea level.",
    "मृत सागर पृथ्वीको सबैभन्दा होचो जमिन हो, समुद्र सतहभन्दा करिब ४३० मिटर तल।", BR)
add("World", "The Great Wall of China is about 21,196 kilometres long — the longest wall in the world.",
    "चीनको ठूलो पर्खाल करिब २१,१९६ किलोमिटर लामो छ — विश्वको सबैभन्दा लामो पर्खाल।", "UNESCO")
add("World", "The Eiffel Tower in Paris was completed in 1889 and is 330 metres tall including its antennas.",
    "पेरिसमा रहेको आइफेल टावर सन् १८८९ मा सम्पन्न भयो र एन्टेनासहित ३३० मिटर अग्लो छ।", BR)
add("World", "The Statue of Liberty was a gift from France to the United States, unveiled in 1886.",
    "स्ट्याचु अफ लिबर्टी फ्रान्सले संयुक्त राज्य अमेरिकालाई दिएको उपहार थियो, जुन सन् १८८६ मा अनावरण गरियो।", BR)
add("World", "The Taj Mahal in India was built between 1632 and 1653 by Emperor Shah Jahan for his wife Mumtaz Mahal.",
    "भारतको ताजमहल सन् १६३२ देखि १६५३ बीच सम्राट शाहजहाँले आफ्नी पत्नी मुमताज महलको सम्झनामा बनाएका थिए।", "UNESCO")
add("World", "The Great Pyramid of Giza is the only one of the Seven Wonders of the Ancient World still standing.",
    "गिजाको ठूलो पिरामिड प्राचीन विश्वका सात आश्चर्यहरूमध्ये अझै उभिएको एक मात्र हो।", BR)
add("World", "The Colosseum in Rome was completed in 80 CE and could hold about 50,000 spectators.",
    "रोमको कोलोसियम इस्वी संवत् ८० मा सम्पन्न भएको थियो र यसमा करिब ५०,००० दर्शक अटाउँथे।", BR)
add("World", "Machu Picchu in Peru was built in the 15th century by the Inca emperor Pachacuti.",
    "पेरुको माचु पिचु १५औं शताब्दीमा इन्का सम्राट पाचाकुटीले बनाएका थिए।", "UNESCO")
add("World", "Angkor Wat in Cambodia is the largest religious monument in the world.",
    "कम्बोडियाको अंकोर वाट विश्वको सबैभन्दा ठूलो धार्मिक स्मारक हो।", "UNESCO")
add("World", "About 60% of the Amazon rainforest is in Brazil.",
    "अमेजन वर्षावनको करिब ६०% ब्राजिलमा छ।", BR)
add("World", "Australia is the world's smallest continent.",
    "अस्ट्रेलिया विश्वको सबैभन्दा सानो महादेश हो।", BR)
add("World", "Greenland is the world's largest island.",
    "ग्रिनल्याण्ड विश्वको सबैभन्दा ठूलो टापु हो।", BR)
add("World", "English is the most widely spoken language in the world, with about 1.5 billion speakers.",
    "अङ्ग्रेजी विश्वमा सबैभन्दा धेरै बोलिने भाषा हो, करिब १.५ अर्ब वक्ताहरूसहित।", "Ethnologue")
add("World", "Mandarin Chinese has the most native speakers of any language, at about 900 million.",
    "मन्डारिन चिनियाँ भाषाका सबैभन्दा धेरै मातृभाषी छन्, करिब ९० करोड।", "Ethnologue")
add("World", "The United Nations has 193 member states.",
    "संयुक्त राष्ट्र संघमा १९३ सदस्य राष्ट्र छन्।", "United Nations")
add("World", "Antarctica has no permanent residents — only researchers who stay temporarily.",
    "एन्टार्कटिकामा कुनै स्थायी बासिन्दा छैनन् — अस्थायी रूपमा बस्ने अनुसन्धानकर्ताहरू मात्र छन्।", BR)
add("World", "The Great Barrier Reef in Australia is the world's largest living structure, visible from space.",
    "अस्ट्रेलियाको ग्रेट ब्यारियर रिफ विश्वको सबैभन्दा ठूलो जीवित संरचना हो, जुन अन्तरिक्षबाट पनि देखिन्छ।", "UNESCO")
add("World", "Lake Baikal in Siberia is the deepest lake in the world, at 1,642 metres.",
    "साइबेरियाको बैकाल ताल विश्वको सबैभन्दा गहिरो ताल हो, १,६४२ मिटर गहिरो।", BR)
add("World", "The Caspian Sea is the world's largest lake by surface area.",
    "क्यास्पियन सागर सतह क्षेत्रफलका हिसाबले विश्वको सबैभन्दा ठूलो ताल हो।", BR)
add("World", "The Atacama Desert in Chile is the driest place on Earth — some parts have never recorded rain.",
    "चिलीको अटाकामा मरुभूमि पृथ्वीको सबैभन्दा सुक्खा ठाउँ हो — केही भागमा कहिल्यै वर्षा मापन गरिएको छैन।", BR)
add("World", "The hottest air temperature ever recorded was 56.7°C in Death Valley, California, in 1913.",
    "अहिलेसम्म मापन गरिएको सबैभन्दा उच्च तापक्रम सन् १९१३ मा क्यालिफोर्नियाको डेथ भ्यालीमा ५६.७° सेल्सियस थियो।", "World Meteorological Organization")
add("World", "The coldest temperature ever recorded was −89.2°C at Vostok Station in Antarctica in 1983.",
    "अहिलेसम्म मापन गरिएको सबैभन्दा चिसो तापक्रम सन् १९८३ मा एन्टार्कटिकाको भोस्तोक स्टेसनमा −८९.२° सेल्सियस थियो।", "World Meteorological Organization")
add("World", "Canada has the longest coastline of any country in the world.",
    "क्यानडाको समुद्री तट विश्वको कुनै पनि देशभन्दा लामो छ।", "CIA World Factbook")
add("World", "The Nile flows through 11 countries on its way to the Mediterranean Sea.",
    "नाइल नदी भूमध्यसागर पुग्नुअघि ११ देश हुँदै बग्छ।", BR)
add("World", "The Danube flows through 10 countries — more than any other river in the world.",
    "ड्यानुब नदी १० देश हुँदै बग्छ — विश्वको कुनै पनि नदीभन्दा बढी।", BR)
add("World", "The United States–Canada border, at 8,891 kilometres, is the longest international border in the world.",
    "८,८९१ किलोमिटर लामो अमेरिका–क्यानडा सीमा विश्वको सबैभन्दा लामो अन्तर्राष्ट्रिय सीमा हो।", "CIA World Factbook")
add("World", "The equator passes through 13 countries.",
    "भूमध्यरेखा १३ देश हुँदै जान्छ।", "National Geographic")
add("World", "The Maldives is the lowest-lying country in the world, with an average height of just 1.5 metres above sea level.",
    "माल्दिभ्स विश्वको सबैभन्दा होचो देश हो, समुद्र सतहभन्दा औसतमा मात्र १.५ मिटर अग्लो।", "CIA World Factbook")
add("World", "Monaco is the most densely populated country in the world.",
    "मोनाको विश्वको सबैभन्दा घना जनसंख्या भएको देश हो।", "World Bank")
add("World", "Mongolia is the least densely populated independent country in the world.",
    "मंगोलिया विश्वको सबैभन्दा कम जनघनत्व भएको स्वतन्त्र देश हो।", "World Bank")
add("World", "France has the most time zones of any country — 12, counting its overseas territories.",
    "फ्रान्सको सबैभन्दा धेरै समय क्षेत्र छ — समुद्रपार क्षेत्रसहित १२।", "CIA World Factbook")

# ---------------- Geography ----------------
add("Geography", "Kangchenjunga, on the Nepal–India border, is the third-highest mountain in the world at 8,586 metres.",
    "नेपाल–भारत सीमामा रहेको कञ्चनजंघा ८,५८६ मिटर अग्लो विश्वको तेस्रो अग्लो हिमाल हो।", BR)
add("Geography", "Mount Kilimanjaro in Tanzania is the highest mountain in Africa, at 5,895 metres.",
    "तान्जानियाको किलिमन्जारो ५,८९५ मिटर अग्लो अफ्रिकाको सबैभन्दा अग्लो हिमाल हो।", BR)
add("Geography", "Aconcagua in Argentina, at 6,961 metres, is the highest mountain in the Americas.",
    "अर्जेन्टिनाको अकोन्कागुआ ६,९६१ मिटर अग्लो अमेरिकाको सबैभन्दा अग्लो हिमाल हो।", BR)
add("Geography", "Mount Elbrus in Russia, at 5,642 metres, is the highest mountain in Europe.",
    "रुसको माउन्ट एल्ब्रस ५,६४२ मिटर अग्लो युरोपको सबैभन्दा अग्लो हिमाल हो।", BR)
add("Geography", "Denali in Alaska, at 6,190 metres, is the highest mountain in North America.",
    "अलास्काको डेनाली ६,१९० मिटर अग्लो उत्तर अमेरिकाको सबैभन्दा अग्लो हिमाल हो।", BR)
add("Geography", "The Yangtze, at about 6,300 kilometres, is the longest river in Asia.",
    "करिब ६,३०० किलोमिटर लामो याङ्त्से एसियाको सबैभन्दा लामो नदी हो।", BR)
add("Geography", "The Volga, at about 3,530 kilometres, is the longest river in Europe.",
    "करिब ३,५३० किलोमिटर लामो भोल्गा युरोपको सबैभन्दा लामो नदी हो।", BR)
add("Geography", "Victoria Falls, on the Zambia–Zimbabwe border, is the largest waterfall in the world by combined width and height.",
    "जाम्बिया–जिम्बाब्वे सीमामा रहेको भिक्टोरिया झरना चौडाइ र उचाइको संयोजनमा विश्वको सबैभन्दा ठूलो झरना हो।", "UNESCO")
add("Geography", "Angel Falls in Venezuela, at 979 metres, is the tallest waterfall in the world.",
    "भेनेजुएलाको एन्जल झरना ९७९ मिटर अग्लो विश्वको सबैभन्दा अग्लो झरना हो।", BR)
add("Geography", "Russia spans 11 time zones — more than any other country.",
    "रुस ११ समय क्षेत्रमा फैलिएको छ — कुनै पनि देशभन्दा बढी।", "CIA World Factbook")
add("Geography", "China spans five geographic time zones but uses a single time zone for the whole country.",
    "चीन पाँच भौगोलिक समय क्षेत्रमा फैलिएको छ तर पूरै देशमा एउटै समय क्षेत्र प्रयोग गर्छ।", BR)
add("Geography", "Mauna Kea in Hawaii is the tallest mountain on Earth from base to peak — about 10,200 metres, most of it underwater.",
    "हवाईको माउना केआ आधारदेखि शिखरसम्म पृथ्वीको सबैभन्दा अग्लो हिमाल हो — करिब १०,२०० मिटर, जसको धेरै भाग पानीमुनि छ।", "US Geological Survey")
add("Geography", "The Dead Sea is about ten times saltier than the ocean.",
    "मृत सागर समुद्रभन्दा करिब दश गुणा नुनिलो छ।", BR)
add("Geography", "The Amazon basin covers about 7 million square kilometres across nine countries.",
    "अमेजन बेसिन नौ देशमा फैलिएको करिब ७० लाख वर्ग किलोमिटर क्षेत्र ओगटेको छ।", BR)
add("Geography", "The Panama Canal opened in 1914, and the Suez Canal opened in 1869.",
    "पनामा नहर सन् १९१४ मा र स्वेज नहर सन् १८६९ मा खोलिएको थियो।", BR)
add("Geography", "The Strait of Gibraltar, separating Europe and Africa, is only about 13 kilometres wide at its narrowest point.",
    "युरोप र अफ्रिकालाई छुट्याउने जिब्राल्टर जलडमरूमध्य साँघुरो ठाउँमा मात्र करिब १३ किलोमिटर चौडा छ।", BR)
add("Geography", "Mount Kilimanjaro is a dormant volcano — it last erupted about 360,000 years ago.",
    "किलिमन्जारो एउटा सुप्त ज्वालामुखी हो — यो अन्तिम पटक करिब ३,६०,००० वर्षअघि विस्फोट भएको थियो।", "US Geological Survey")
add("Geography", "The Grand Canyon in Arizona is about 446 kilometres long and up to 1.8 kilometres deep.",
    "एरिजोनाको ग्रान्ड क्यान्यन करिब ४४६ किलोमिटर लामो र १.८ किलोमिटरसम्म गहिरो छ।", "US National Park Service")
add("Geography", "Lake Titicaca, on the Peru–Bolivia border at 3,812 metres, is the highest navigable lake in the world.",
    "पेरु–बोलिभिया सीमामा ३,८१२ मिटर उचाइमा रहेको टिटिकाका ताल विश्वको सबैभन्दा अग्लो नौवहनयोग्य ताल हो।", BR)
add("Geography", "The Danube is the second-longest river in Europe, after the Volga.",
    "ड्यानुब भोल्गापछि युरोपको दोस्रो लामो नदी हो।", BR)
add("Geography", "About 75% of the world's volcanoes are on the Pacific 'Ring of Fire'.",
    "विश्वका करिब ७५% ज्वालामुखी प्रशान्त 'रिङ अफ फायर' मा छन्।", "US Geological Survey")
add("Geography", "Mauna Loa in Hawaii is the largest shield volcano on Earth by volume.",
    "हवाईको माउना लोआ आयतनका हिसाबले पृथ्वीको सबैभन्दा ठूलो ढाल ज्वालामुखी हो।", "US Geological Survey")
add("Geography", "The Gobi Desert spans northern China and southern Mongolia.",
    "गोबी मरुभूमि उत्तरी चीन र दक्षिणी मंगोलियामा फैलिएको छ।", BR)
add("Geography", "There are about 1,500 potentially active volcanoes on land around the world.",
    "विश्वभर जमिनमा करिब १,५०० सम्भावित सक्रिय ज्वालामुखी छन्।", "Smithsonian Institution")
add("Geography", "The Sahara is almost the size of the United States.",
    "सहारा मरुभूमि झन्डै संयुक्त राज्य अमेरिकाजत्रै ठूलो छ।", "National Geographic")
add("Geography", "Iceland sits on the Mid-Atlantic Ridge, where the North American and Eurasian tectonic plates pull apart.",
    "आइसल्याण्ड मध्य-अटलान्टिक रिजमा छ, जहाँ उत्तर अमेरिकी र युरेसियाली टेक्टोनिक प्लेटहरू टाढा तानिन्छन्।", "US Geological Survey")
add("Geography", "The Nile Delta, where the Nile meets the Mediterranean, is one of the most fertile farming regions on Earth.",
    "नाइल नदी भूमध्यसागरमा मिसिने नाइल डेल्टा पृथ्वीका सबैभन्दा उर्वर कृषि क्षेत्रहरूमध्ये एक हो।", BR)
add("Geography", "Mount Everest is known as Sagarmatha in Nepali and Chomolungma in Tibetan.",
    "सगरमाथालाई नेपालीमा सगरमाथा र तिब्बतीमा चोमोलुङ्मा भनिन्छ।", BR)
add("Geography", "The Mississippi River is the longest river in North America, at about 3,766 kilometres.",
    "करिब ३,७६६ किलोमिटर लामो मिसिसिपी नदी उत्तर अमेरिकाको सबैभन्दा लामो नदी हो।", BR)
add("Geography", "The Murray–Darling is the longest river system in Australia.",
    "मरे–डार्लिङ अस्ट्रेलियाको सबैभन्दा लामो नदी प्रणाली हो।", BR)
add("Geography", "Africa is the second-largest continent in the world, after Asia.",
    "अफ्रिका एसियापछि विश्वको दोस्रो ठूलो महादेश हो।", BR)
add("Geography", "Asia is the largest continent, covering about 30% of Earth's land area.",
    "एसिया सबैभन्दा ठूलो महादेश हो, जसले पृथ्वीको जमिनको करिब ३०% ओगटेको छ।", BR)
add("Geography", "The island of Borneo is shared by three countries: Indonesia, Malaysia and Brunei.",
    "बोर्नियो टापु तीन देश — इन्डोनेसिया, मलेसिया र ब्रुनाई — ले बाँडेका छन्।", BR)
add("Geography", "The world's largest island, Greenland, is about 80% covered in ice.",
    "विश्वको सबैभन्दा ठूलो टापु ग्रिनल्याण्डको करिब ८०% भाग बरफले ढाकिएको छ।", "National Geographic")
add("Geography", "The driest inhabited place on Earth is Arica, in northern Chile.",
    "पृथ्वीको सबैभन्दा सुक्खा बसोबास भएको ठाउँ उत्तरी चिलीको एरिका हो।", BR)
add("Geography", "The Rhine flows from the Swiss Alps to the North Sea through six countries.",
    "राइन नदी स्विस आल्प्सबाट बगेर छ देश हुँदै उत्तरी सागरमा पुग्छ।", BR)
add("Geography", "Mount Fuji, Japan's highest mountain at 3,776 metres, last erupted in 1707.",
    "जापानको सबैभन्दा अग्लो हिमाल माउन्ट फुजी (३,७७६ मिटर) अन्तिम पटक सन् १७०७ मा विस्फोट भएको थियो।", BR)
add("Geography", "The Great Dividing Range runs for about 3,500 kilometres along Australia's east coast.",
    "ग्रेट डिभाइडिङ रेन्ज अस्ट्रेलियाको पूर्वी तटमा करिब ३,५०० किलोमिटरसम्म फैलिएको छ।", BR)
add("Geography", "The Antarctic ice sheet holds about 60% of the world's fresh water.",
    "एन्टार्कटिकाको बरफको चादरले विश्वको करिब ६०% ताजा पानी ओगटेको छ।", "NASA")
add("Geography", "The longest mountain range on Earth is not on land — the Mid-Atlantic Ridge runs for about 16,000 kilometres under the ocean.",
    "पृथ्वीको सबैभन्दा लामो पर्वत शृंखला जमिनमा छैन — मध्य-अटलान्टिक रिज समुद्रमुनि करिब १६,००० किलोमिटरसम्म फैलिएको छ।", "National Geographic")

# ---------------- Science ----------------
add("Science", "Water is made of two hydrogen atoms and one oxygen atom — H2O.",
    "पानी दुई हाइड्रोजन परमाणु र एक अक्सिजन परमाणु मिलेर बनेको हुन्छ — H2O।", BR)
add("Science", "At sea level, water boils at 100°C and freezes at 0°C.",
    "समुद्र सतहमा पानी १००° सेल्सियसमा उम्लन्छ र ०° सेल्सियसमा जम्छ।", BR)
add("Science", "Light travels at 299,792 kilometres per second in a vacuum — the fastest speed known.",
    "शून्यतामा प्रकाश प्रति सेकेन्ड २,९९,७९२ किलोमिटर गतिमा यात्रा गर्छ — थाहा भएको सबैभन्दा छिटो गति।", "NASA")
add("Science", "Earth takes about 365.25 days to orbit the Sun — which is why we add a leap day every four years.",
    "पृथ्वीलाई सूर्यको परिक्रमा गर्न करिब ३६५.२५ दिन लाग्छ — त्यसैले हरेक चार वर्षमा एक अतिरिक्त दिन थपिन्छ।", "NASA")
add("Science", "The Moon takes about 27.3 days to orbit the Earth.",
    "चन्द्रमालाई पृथ्वीको परिक्रमा गर्न करिब २७.३ दिन लाग्छ।", "NASA")
add("Science", "The Sun holds about 99.86% of all the mass in the solar system.",
    "सूर्यले सौर्यमण्डलको कुल द्रव्यमानको करिब ९९.८६% ओगटेको छ।", "NASA")
add("Science", "Sunlight takes about 8 minutes and 20 seconds to reach the Earth.",
    "सूर्यको प्रकाश पृथ्वीमा पुग्न करिब ८ मिनेट २० सेकेन्ड लाग्छ।", "NASA")
add("Science", "An adult human has 206 bones; a baby is born with about 300, some of which fuse together as it grows.",
    "वयस्क मानिसमा २०६ वटा हड्डी हुन्छन्; बच्चा करिब ३०० हड्डीसहित जन्मन्छ, जसमध्ये केही बढ्दै जाँदा जोडिन्छन्।", BR)
add("Science", "The human heart beats about 100,000 times every day.",
    "मानिसको मुटु हरेक दिन करिब १,००,००० पटक धड्कन्छ।", "British Heart Foundation")
add("Science", "The human brain contains about 86 billion neurons.",
    "मानिसको मस्तिष्कमा करिब ८६ अर्ब न्युरोन हुन्छन्।", "Nature (2016)")
add("Science", "The double-helix structure of DNA was discovered in 1953 by James Watson and Francis Crick.",
    "डीएनएको डबल-हेलिक्स संरचना सन् १९५३ मा जेम्स वाटसन र फ्रान्सिस क्रिकले पत्ता लगाएका थिए।", BR)
add("Science", "Gravity on Earth pulls objects down at about 9.8 metres per second squared.",
    "पृथ्वीमा गुरुत्वाकर्षणले वस्तुहरूलाई प्रति सेकेन्ड वर्ग करिब ९.८ मिटरको दरले तल तान्छ।", BR)
add("Science", "Albert Einstein published his famous equation E=mc² in 1905.",
    "अल्बर्ट आइन्स्टाइनले आफ्नो प्रसिद्ध समीकरण E=mc² सन् १९०५ मा प्रकाशित गरेका थिए।", BR)
add("Science", "The first vaccine was for smallpox, developed by Edward Jenner in 1796.",
    "पहिलो खोप बिफर (स्मलपक्स) का लागि थियो, जुन एडवर्ड जेनरले सन् १७९६ मा विकास गरेका थिए।", "World Health Organization")
add("Science", "Penicillin, the first widely used antibiotic, was discovered by Alexander Fleming in 1928.",
    "पहिलो व्यापक रूपमा प्रयोग गरिएको एन्टिबायोटिक पेनिसिलिन अलेक्ज्याण्डर फ्लेमिङले सन् १९२८ मा पत्ता लगाएका थिए।", BR)
add("Science", "Joseph Priestley isolated oxygen in 1774.",
    "जोसेफ प्रिस्टलीले सन् १७७४ मा अक्सिजन अलग गरेका थिए।", BR)
add("Science", "Dmitri Mendeleev published the first periodic table of the elements in 1869.",
    "दिमित्री मेन्डेलिभले सन् १८६९ मा तत्वहरूको पहिलो आवर्त सारणी प्रकाशित गरेका थिए।", BR)
add("Science", "Gold's chemical symbol is Au and its atomic number is 79.",
    "सुनको रासायनिक संकेत Au हो र यसको परमाणु संख्या ७९ हो।", BR)
add("Science", "Diamond is the hardest naturally occurring material on Earth.",
    "हीरा पृथ्वीमा पाइने सबैभन्दा कडा प्राकृतिक पदार्थ हो।", BR)
add("Science", "Sound travels at about 343 metres per second in air.",
    "हावामा ध्वनि प्रति सेकेन्ड करिब ३४३ मिटर गतिमा यात्रा गर्छ।", BR)
add("Science", "Absolute zero, the coldest possible temperature, is −273.15°C.",
    "सम्भव सबैभन्दा चिसो तापक्रम निरपेक्ष शून्य −२७३.१५° सेल्सियस हो।", BR)
add("Science", "Venus is the hottest planet in the solar system, with a surface temperature of about 464°C.",
    "शुक्र सौर्यमण्डलको सबैभन्दा तातो ग्रह हो, जसको सतहको तापक्रम करिब ४६४° सेल्सियस छ।", "NASA")
add("Science", "Mars is called the Red Planet because iron oxide (rust) on its surface gives it a red colour.",
    "मंगल ग्रहलाई रातो ग्रह भनिन्छ किनभने यसको सतहको आइरन अक्साइड (खिया) ले यसलाई रातो रंग दिन्छ।", "NASA")
add("Science", "Olympus Mons on Mars is the tallest volcano in the solar system, at about 22 kilometres high.",
    "मंगल ग्रहको ओलम्पस मोन्स सौर्यमण्डलको सबैभन्दा अग्लो ज्वालामुखी हो, करिब २२ किलोमिटर अग्लो।", "NASA")
add("Science", "Jupiter is the largest planet in the solar system.",
    "बृहस्पति सौर्यमण्डलको सबैभन्दा ठूलो ग्रह हो।", "NASA")
add("Science", "Saturn's rings are made mostly of ice and rock.",
    "शनिका छल्लाहरू मुख्यतया बरफ र चट्टानबाट बनेका छन्।", "NASA")
add("Science", "Neptune is the farthest planet from the Sun.",
    "नेप्च्युन सूर्यबाट सबैभन्दा टाढा रहेको ग्रह हो।", "NASA")
add("Science", "Pluto was reclassified as a dwarf planet in 2006.",
    "प्लुटोलाई सन् २००६ मा बौना ग्रहका रूपमा पुनः वर्गीकरण गरिएको थियो।", "International Astronomical Union")
add("Science", "The Milky Way galaxy contains roughly 100 to 400 billion stars.",
    "आकाशगंगा (मिल्की वे) मा करिब १०० देखि ४०० अर्ब ताराहरू छन्।", "NASA")
add("Science", "The Andromeda galaxy, our nearest large neighbour, is about 2.5 million light-years away.",
    "हाम्रो नजिकको ठूलो छिमेकी एन्ड्रोमेडा आकाशगंगा करिब २५ लाख प्रकाश-वर्ष टाढा छ।", "NASA")
add("Science", "The first image of a black hole was released in 2019, showing the black hole at the centre of galaxy M87.",
    "ब्ल्याक होलको पहिलो तस्बिर सन् २०१९ मा सार्वजनिक गरियो, जसमा M87 आकाशगंगाको केन्द्रमा रहेको ब्ल्याक होल देखाइएको थियो।", "Event Horizon Telescope Collaboration")
add("Science", "About 60% of the human body is water.",
    "मानव शरीरको करिब ६०% भाग पानी हो।", "US Geological Survey")
add("Science", "Red blood cells carry oxygen around the body using a protein called haemoglobin.",
    "राता रक्तकोषहरू हिमोग्लोबिन नामक प्रोटिन प्रयोग गरेर शरीरभरि अक्सिजन पुर्‍याउँछन्।", BR)
add("Science", "Plants make food by photosynthesis — using sunlight, water and carbon dioxide.",
    "बिरुवाहरूले सूर्यको प्रकाश, पानी र कार्बन डाइअक्साइड प्रयोग गरेर प्रकाश संश्लेषणबाट खाना बनाउँछन्।", BR)
add("Science", "Honey never spoils — pots of honey found in Egyptian tombs thousands of years old are still edible.",
    "मह कहिल्यै बिग्रिँदैन — हजारौं वर्ष पुराना इजिप्टका चिहानहरूमा भेटिएका मह अझै खान मिल्छ।", "Smithsonian Institution")
add("Science", "Bananas are slightly radioactive because they contain potassium-40.",
    "केरामा पोटासियम-४० हुने भएकाले यो अलिकति रेडियोधर्मी हुन्छ।", BR)
add("Science", "Lightning can be hotter than the surface of the Sun — reaching about 30,000 Kelvin.",
    "चट्याङ सूर्यको सतहभन्दा तातो हुन सक्छ — करिब ३०,००० केल्भिनसम्म पुग्छ।", "National Weather Service (USA)")
add("Science", "The Earth is not a perfect sphere — it bulges slightly at the equator.",
    "पृथ्वी पूर्ण गोलो छैन — यो भूमध्यरेखामा अलिकति फुलेको छ।", "NASA")
add("Science", "The Moon is drifting away from the Earth by about 3.8 centimetres every year.",
    "चन्द्रमा हरेक वर्ष पृथ्वीबाट करिब ३.८ सेन्टिमिटर टाढा सर्दै छ।", "NASA")
add("Science", "A day on Venus (243 Earth days) is longer than its year (225 Earth days).",
    "शुक्र ग्रहको एक दिन (२४३ पृथ्वी दिन) यसको एक वर्ष (२२५ पृथ्वी दिन) भन्दा लामो छ।", "NASA")
add("Science", "Mercury has the biggest temperature swings of any planet — from about −180°C at night to 430°C in the day.",
    "बुध ग्रहमा कुनै पनि ग्रहभन्दा ठूलो तापक्रम परिवर्तन हुन्छ — राति करिब −१८०° सेल्सियसदेखि दिनमा ४३०° सेल्सियससम्म।", "NASA")
add("Science", "Octopuses have three hearts.",
    "अक्टोपसका तीनवटा मुटु हुन्छन्।", "Smithsonian Institution")
add("Science", "The blue whale is the largest animal ever known to have lived on Earth.",
    "नीलो ह्वेल पृथ्वीमा बसेको थाहा भएका सबैभन्दा ठूलो जनावर हो।", BR)
add("Science", "The hummingbird is the only bird that can fly backwards.",
    "हमिङबर्ड पछाडि उड्न सक्ने एक मात्र चरा हो।", BR)
add("Science", "Sharks are older than trees — sharks appeared about 450 million years ago, trees about 350 million years ago.",
    "शार्कहरू रुखहरूभन्दा पुराना हुन् — शार्क करिब ४५ करोड वर्षअघि देखा परे, रुख करिब ३५ करोड वर्षअघि।", "Smithsonian Institution")
add("Science", "A teaspoon of neutron-star material would weigh about a billion tonnes.",
    "एक चम्चा न्युट्रोन तारा पदार्थको तौल करिब एक अर्ब टन हुन्छ।", "NASA")
add("Science", "Sound cannot travel in space because there is no air or other medium to carry it.",
    "अन्तरिक्षमा ध्वनि यात्रा गर्न सक्दैन किनभने त्यसलाई बोक्ने हावा वा अन्य माध्यम हुँदैन।", "NASA")
add("Science", "The first computer bug was a real moth, found taped into a logbook at Harvard in 1947.",
    "पहिलो कम्प्युटर बग वास्तविक पुतली थियो, जुन सन् १९४७ मा हार्वर्डमा लगबुकमा टाँसिएको भेटिएको थियो।", "Smithsonian Institution")
add("Science", "The World Wide Web was invented by Tim Berners-Lee in 1989.",
    "वर्ल्ड वाइड वेब टिम बर्नर्स-लीले सन् १९८९ मा आविष्कार गरेका थिए।", "CERN")
add("Science", "The first email was sent by Ray Tomlinson in 1971.",
    "पहिलो इमेल रे टमलिनसनले सन् १९७१ मा पठाएका थिए।", BR)
add("Science", "The human genome contains about 3 billion base pairs of DNA.",
    "मानव जिनोममा करिब ३ अर्ब डीएनए बेस जोडी हुन्छन्।", "National Human Genome Research Institute")

# ---------------- History ----------------
add("History", "The Second World War lasted from 1939 to 1945.",
    "दोस्रो विश्वयुद्ध सन् १९३९ देखि १९४५ सम्म चल्यो।", BR)
add("History", "The First World War lasted from 1914 to 1918.",
    "प्रथम विश्वयुद्ध सन् १९१४ देखि १९१८ सम्म चल्यो।", BR)
add("History", "Yuri Gagarin became the first human in space on 12 April 1961.",
    "युरी गागारिन १२ अप्रिल १९६१ मा अन्तरिक्षमा पुग्ने पहिलो मानिस बने।", "NASA")
add("History", "Apollo 11 landed the first humans on the Moon on 20 July 1969 — Neil Armstrong and Buzz Aldrin.",
    "अपोलो ११ ले २० जुलाई १९६९ मा चन्द्रमामा पहिलो मानिस — निल आर्मस्ट्रङ र बज एल्ड्रिन — अवतरण गरायो।", "NASA")
add("History", "Johannes Gutenberg's printing press, around 1440, made books affordable for the first time.",
    "जोहानेस गुटेनबर्गको छापाखाना (करिब १४४०) ले पहिलो पटक किताबहरू सस्तो बनायो।", BR)
add("History", "The Wright brothers made the first powered flight on 17 December 1903.",
    "राइट दाजुभाइले १७ डिसेम्बर १९०३ मा पहिलो इन्जिनयुक्त उडान गरे।", BR)
add("History", "The Titanic sank on 15 April 1912, on its first voyage from England to America.",
    "टाइटानिक १५ अप्रिल १९१२ मा इङ्गल्याण्डबाट अमेरिकाको आफ्नो पहिलो यात्रामा डुब्यो।", BR)
add("History", "The Berlin Wall fell on 9 November 1989, ending the division of Germany.",
    "बर्लिन पर्खाल ९ नोभेम्बर १९८९ मा ढल्यो, जसले जर्मनीको विभाजन अन्त्य गर्यो।", BR)
add("History", "The United Nations was founded on 24 October 1945.",
    "संयुक्त राष्ट्र संघको स्थापना २४ अक्टोबर १९४५ मा भएको थियो।", "United Nations")
add("History", "The Western Roman Empire fell in 476 CE.",
    "पश्चिमी रोमन साम्राज्य इस्वी संवत् ४७६ मा पतन भयो।", BR)
add("History", "The French Revolution began in 1789.",
    "फ्रान्सेली क्रान्ति सन् १७८९ मा सुरु भयो।", BR)
add("History", "The United States declared independence on 4 July 1776.",
    "संयुक्त राज्य अमेरिकाले ४ जुलाई १७७६ मा स्वतन्त्रता घोषणा गर्यो।", BR)
add("History", "India became independent from Britain on 15 August 1947.",
    "भारत १५ अगस्ट १९४७ मा बेलायतबाट स्वतन्त्र भयो।", BR)
add("History", "The first modern Olympic Games were held in Athens in 1896.",
    "पहिलो आधुनिक ओलम्पिक खेल सन् १८९६ मा एथेन्समा भएको थियो।", "Olympics.com")
add("History", "The wheel was invented in Mesopotamia around 3500 BCE.",
    "पाङ्ग्रा मेसोपोटामियामा करिब ईसापूर्व ३५०० मा आविष्कार भएको थियो।", BR)
add("History", "Paper was invented in China around 105 CE by Cai Lun.",
    "कागज चीनमा करिब इस्वी संवत् १०५ मा चाई लुनले आविष्कार गरेका थिए।", BR)
add("History", "Gunpowder was invented in China in the 9th century.",
    "बारुद चीनमा ९औं शताब्दीमा आविष्कार भएको थियो।", BR)
add("History", "Leonardo da Vinci painted the Mona Lisa in the early 1500s.",
    "लियोनार्दो दा भिन्चीले १५०० को दशकको सुरुमा मोना लिसा चित्र बनाएका थिए।", BR)
add("History", "William Shakespeare was born in 1564 and died in 1616.",
    "विलियम शेक्सपियरको जन्म सन् १५६४ मा भएको थियो र मृत्यु सन् १६१६ मा भयो।", BR)
add("History", "Albert Einstein was born in 1879 and died in 1955.",
    "अल्बर्ट आइन्स्टाइनको जन्म सन् १८७९ मा भएको थियो र मृत्यु सन् १९५५ मा भयो।", BR)
add("History", "The Black Death of 1347–1351 killed between 30% and 60% of Europe's population.",
    "सन् १३४७–१३५१ को कालो मृत्यु (ब्ल्याक डेथ) ले युरोपको ३०% देखि ६०% जनसंख्या मार्यो।", BR)
add("History", "The 1918–1920 influenza pandemic infected about one-third of the world's population.",
    "सन् १९१८–१९२० को इन्फ्लुएन्जा महामारीले विश्व जनसंख्याको करिब एक तिहाइ मानिसलाई संक्रमित गर्यो।", "World Health Organization")
add("History", "Smallpox was declared eradicated by the World Health Organization in 1980 — the first disease ever wiped out.",
    "बिफर (स्मलपक्स) लाई विश्व स्वास्थ्य संगठनले सन् १९८० मा उन्मूलन भएको घोषणा गर्यो — उन्मूलन भएको पहिलो रोग।", "World Health Organization")
add("History", "Alexander the Great died in 323 BCE at the age of 32.",
    "अलेक्ज्याण्डर महानको मृत्यु ईसापूर्व ३२३ मा ३२ वर्षको उमेरमा भयो।", BR)
add("History", "Cleopatra lived closer in time to the Moon landing than to the building of the Great Pyramid of Giza.",
    "क्लियोपेट्रा गिजाको ठूलो पिरामिड निर्माणको समयभन्दा चन्द्रमा अवतरणको समयको नजिक बाँचेकी थिइन्।", BR)
add("History", "Oxford University was teaching students from 1096 — before the Aztec capital was founded in 1325.",
    "अक्सफोर्ड विश्वविद्यालयले सन् १०९६ देखि विद्यार्थी पढाउँदै आएको छ — एज्टेक राजधानी स्थापना (१३२५) भन्दा पहिलेदेखि।", "University of Oxford")
add("History", "Nintendo was founded in 1889 — as a maker of hand-painted playing cards.",
    "निन्टेन्डो सन् १८८९ मा स्थापना भएको थियो — हातले रंगाइएका तास बनाउने कम्पनीका रूपमा।", BR)
add("History", "The Great Fire of London burned for four days in 1666.",
    "लन्डनको ठूलो आगलागी सन् १६६६ मा चार दिनसम्म जल्यो।", BR)
add("History", "The Rosetta Stone, found in 1799, let scholars finally read Egyptian hieroglyphs.",
    "सन् १७९९ मा भेटिएको रोजेटा ढुंगाले विद्वानहरूलाई अन्ततः इजिप्टको चित्रलिपि पढ्न सक्षम बनायो।", "British Museum")
add("History", "Democracy began in Athens around 508 BCE.",
    "लोकतन्त्र एथेन्समा करिब ईसापूर्व ५०८ मा सुरु भयो।", BR)
add("History", "The University of al-Qarawiyyin in Fez, Morocco, founded in 859 CE, is the oldest existing university in the world.",
    "मोरक्कोको फेजमा सन् ८५९ मा स्थापित अल-करावियिन विश्वविद्यालय विश्वको सबैभन्दा पुरानो अस्तित्वमा रहेको विश्वविद्यालय हो।", "UNESCO")
add("History", "The first telephone call was made by Alexander Graham Bell in 1876.",
    "पहिलो टेलिफोन कल अलेक्ज्याण्डर ग्राहम बेलले सन् १८७६ मा गरेका थिए।", BR)
add("History", "Karl Benz built the first practical automobile in 1885–86.",
    "कार्ल बेन्जले सन् १८८५–८६ मा पहिलो व्यावहारिक अटोमोबाइल बनाएका थिए।", BR)
add("History", "The compass was invented in China, first for fortune-telling and later for navigation.",
    "कम्पास चीनमा आविष्कार भएको थियो, पहिले भाग्य हेर्न र पछि दिशानिर्देशनका लागि।", BR)
add("History", "The first World Cup was held in 1930 in Uruguay, and Uruguay won it.",
    "पहिलो विश्वकप सन् १९३० मा उरुग्वेमा भएको थियो र उरुग्वेले जितेको थियो।", "FIFA")
add("History", "Humans began migrating out of Africa about 60,000–70,000 years ago.",
    "मानिसहरू करिब ६०,०००–७०,००० वर्षअघि अफ्रिकाबाट बाहिर सर्न थाले।", "Smithsonian Institution")
add("History", "The Eiffel Tower was first proposed for Barcelona, which rejected it, before Paris accepted it for the 1889 World's Fair.",
    "आइफेल टावर पहिले बार्सिलोनालाई प्रस्ताव गरिएको थियो, जसले अस्वीकार गर्यो, र त्यसपछि पेरिसले सन् १८८९ को विश्व मेलाका लागि स्वीकार गर्यो।", BR)
add("History", "The ancient Olympic Games began in 776 BCE in Olympia, Greece.",
    "प्राचीन ओलम्पिक खेलहरू ईसापूर्व ७७६ मा ग्रीसको ओलम्पियामा सुरु भएका थिए।", "Olympics.com")
add("History", "The oldest known musical instruments, flutes made from bone, are about 40,000 years old.",
    "सबैभन्दा पुराना ज्ञात वाद्ययन्त्रहरू, हड्डीबाट बनेका बाँसुरीहरू, करिब ४०,००० वर्ष पुराना छन्।", "University of Tübingen")
add("History", "The Library of Alexandria in Egypt was one of the largest libraries of the ancient world.",
    "इजिप्टको अलेक्जान्ड्रिया पुस्तकालय प्राचीन विश्वका सबैभन्दा ठूला पुस्तकालयहरूमध्ये एक थियो।", BR)

# ---------------- Sports ----------------
add("Sports", "The first modern Olympic Games were held in Athens in 1896, with 241 athletes from 14 nations.",
    "पहिलो आधुनिक ओलम्पिक खेल सन् १८९६ मा एथेन्समा भएको थियो, जसमा १४ राष्ट्रका २४१ खेलाडी सहभागी थिए।", "Olympics.com")
add("Sports", "Brazil has won the FIFA World Cup five times — more than any other country.",
    "ब्राजिलले फिफा विश्वकप पाँच पटक जितेको छ — कुनै पनि देशभन्दा बढी।", "FIFA")
add("Sports", "The first Cricket World Cup was held in 1975 in England, and the West Indies won it.",
    "पहिलो क्रिकेट विश्वकप सन् १९७५ मा इङ्गल्याण्डमा भएको थियो र वेस्ट इन्डिजले जितेको थियो।", "International Cricket Council")
add("Sports", "Nepal gained One Day International (ODI) status in cricket in 2018.",
    "नेपालले सन् २०१८ मा क्रिकेटमा एकदिवसीय अन्तर्राष्ट्रिय (ODI) मान्यता पायो।", "International Cricket Council")
add("Sports", "Sandeep Lamichhane became the first Nepali cricketer to play in the Indian Premier League, for Delhi Daredevils in 2018.",
    "सन्दीप लामिछाने इन्डियन प्रिमियर लिगमा खेल्ने पहिलो नेपाली क्रिकेटर बने — सन् २०१८ मा दिल्ली डेयरडेभिल्सबाट।", "International Cricket Council")
add("Sports", "Usain Bolt's 100-metre world record of 9.58 seconds was set in Berlin in 2009.",
    "उसैन बोल्टको १०० मिटर विश्व कीर्तिमान ९.५८ सेकेन्ड सन् २००९ मा बर्लिनमा बनेको थियो।", "World Athletics")
add("Sports", "A marathon is 42.195 kilometres long.",
    "म्याराथन ४२.१९५ किलोमिटर लामो हुन्छ।", "World Athletics")
add("Sports", "The Olympic rings represent the five inhabited continents: Africa, the Americas, Asia, Europe and Oceania.",
    "ओलम्पिकका पाँच छल्लाले पाँच बसोबास भएका महादेश — अफ्रिका, अमेरिका, एसिया, युरोप र ओसिनिया — लाई जनाउँछन्।", "Olympics.com")
add("Sports", "The first Tour de France cycle race was held in 1903.",
    "पहिलो टुर डि फ्रान्स साइकल दौड सन् १९०३ मा भएको थियो।", BR)
add("Sports", "Wimbledon, first played in 1877, is the oldest tennis tournament in the world.",
    "सन् १८७७ मा पहिलो पटक खेलिएको विम्बल्डन विश्वको सबैभन्दा पुरानो टेनिस प्रतियोगिता हो।", BR)
add("Sports", "The first Super Bowl was played in 1967.",
    "पहिलो सुपर बाउल सन् १९६७ मा खेलिएको थियो।", BR)
add("Sports", "Michael Phelps has won 23 Olympic gold medals — more than any other athlete.",
    "माइकल फेल्प्सले २३ ओलम्पिक स्वर्ण पदक जितेका छन् — कुनै पनि खेलाडीभन्दा बढी।", "Olympics.com")
add("Sports", "Football is the world's most popular sport, with about 3.5 billion fans.",
    "फुटबल विश्वको सबैभन्दा लोकप्रिय खेल हो, करिब ३.५ अर्ब समर्थकसहित।", "FIFA")
add("Sports", "Cricket is the second most popular sport in the world.",
    "क्रिकेट विश्वको दोस्रो सबैभन्दा लोकप्रिय खेल हो।", BR)
add("Sports", "The longest tennis match ever lasted 11 hours and 5 minutes — John Isner beat Nicolas Mahut at Wimbledon in 2010.",
    "अहिलेसम्मको सबैभन्दा लामो टेनिस खेल ११ घण्टा ५ मिनेट चल्यो — सन् २०१० को विम्बल्डनमा जोन इस्नरले निकोलस माहुटलाई हराए।", BR)
add("Sports", "The FIFA World Cup trophy weighs 6.175 kilograms and is made of 18-carat gold.",
    "फिफा विश्वकप ट्रफीको तौल ६.१७५ किलोग्राम छ र यो १८ क्यारेट सुनबाट बनेको छ।", "FIFA")
add("Sports", "The first Asian Games were held in New Delhi in 1951.",
    "पहिलो एसियाली खेलकुद सन् १९५१ मा नयाँ दिल्लीमा भएको थियो।", "Olympic Council of Asia")
add("Sports", "The Paralympic Games began in Rome in 1960.",
    "पारालिम्पिक खेलकुद सन् १९६० मा रोममा सुरु भएको थियो।", "International Paralympic Committee")
add("Sports", "The first Test cricket match was played in 1877 between Australia and England.",
    "पहिलो टेस्ट क्रिकेट खेल सन् १८७७ मा अस्ट्रेलिया र इङ्गल्याण्डबीच खेलिएको थियो।", "International Cricket Council")
add("Sports", "Sachin Tendulkar is the only cricketer to score 100 international centuries.",
    "सचिन तेन्दुलकर १०० अन्तर्राष्ट्रिय शतक बनाउने एक मात्र क्रिकेटर हुन्।", "International Cricket Council")
add("Sports", "Don Bradman's Test batting average of 99.94 is the highest in cricket history.",
    "डन ब्र्याडम्यानको टेस्ट ब्याटिङ औसत ९९.९४ क्रिकेट इतिहासकै सबैभन्दा उच्च हो।", "International Cricket Council")
add("Sports", "A football match lasts 90 minutes, split into two 45-minute halves.",
    "फुटबल खेल ९० मिनेटको हुन्छ, जुन दुई ४५-मिनेटको हाफमा बाँडिएको हुन्छ।", "FIFA")
add("Sports", "The highest individual score in a One Day International is 264, by Rohit Sharma in 2014.",
    "एकदिवसीय अन्तर्राष्ट्रियमा सबैभन्दा उच्च व्यक्तिगत स्कोर २६४ हो, जुन रोहित शर्माले सन् २०१४ मा बनाएका थिए।", "International Cricket Council")
add("Sports", "Junko Tabei of Japan became the first woman to climb Mount Everest, in 1975.",
    "जापानकी जुन्को ताबेई सन् १९७५ मा सगरमाथा चढ्ने पहिलो महिला बनिन्।", BR)
add("Sports", "Chess is recognised as a sport by the International Olympic Committee.",
    "चेसलाई अन्तर्राष्ट्रिय ओलम्पिक समितिले खेलका रूपमा मान्यता दिएको छ।", "International Olympic Committee")

# ---------------- Culture ----------------
add("Culture", "Diwali, the festival of lights, is celebrated by Hindus, Jains and Sikhs across South Asia and the world.",
    "उज्यालोको पर्व दीपावली दक्षिण एसिया र विश्वभर हिन्दू, जैन र सिखहरूले मनाउँछन्।", BR)
add("Culture", "Holi, the festival of colours, marks the arrival of spring in South Asia.",
    "रङहरूको पर्व होलीले दक्षिण एसियामा वसन्तको आगमनलाई चिनाउँछ।", BR)
add("Culture", "'Namaste' is a greeting that means 'I bow to you'.",
    "'नमस्ते' भनेको 'म तपाईंलाई नमन गर्छु' भन्ने अभिवादन हो।", BR)
add("Culture", "The Mona Lisa is kept in the Louvre museum in Paris.",
    "मोना लिसा पेरिसको लुभ्र संग्रहालयमा राखिएको छ।", BR)
add("Culture", "The Louvre in Paris is the most-visited museum in the world.",
    "पेरिसको लुभ्र विश्वको सबैभन्दा धेरै भ्रमण गरिने संग्रहालय हो।", BR)
add("Culture", "India makes more films per year than any other country in the world.",
    "भारतले विश्वको कुनै पनि देशभन्दा बढी फिल्म प्रतिवर्ष निर्माण गर्छ।", BR)
add("Culture", "The Bible is the most translated book in history, in more than 700 languages.",
    "बाइबल इतिहासकै सबैभन्दा धेरै अनुवाद गरिएको पुस्तक हो, ७०० भन्दा बढी भाषाहरूमा।", "United Bible Societies")
add("Culture", "The word 'robot' comes from the Czech word 'robota', meaning forced labour — first used in Karel Čapek's 1920 play.",
    "'रोबोट' शब्द चेक शब्द 'रोबोटा' बाट आएको हो, जसको अर्थ जबर्जस्ती श्रम हो — यो पहिलो पटक कारेल चापेकको सन् १९२० को नाटकमा प्रयोग भयो।", BR)
add("Culture", "The Eiffel Tower grows about 15 centimetres taller in summer as its iron expands in the heat.",
    "आइफेल टावर गर्मीमा फलाम फैलिने भएकाले गर्मीमा करिब १५ सेन्टिमिटर अग्लो हुन्छ।", BR)
add("Culture", "More than 7,000 languages are spoken in the world today.",
    "आज विश्वमा ७,००० भन्दा बढी भाषाहरू बोलिन्छन्।", "Ethnologue")
add("Culture", "Papua New Guinea has the most languages of any country — about 840.",
    "पापुआ न्यु गिनीमा कुनै पनि देशभन्दा बढी भाषा छन् — करिब ८४०।", "Ethnologue")
add("Culture", "Don Quixote, published in 1605, is often called the first modern novel.",
    "सन् १६०५ मा प्रकाशित डन क्विक्सोटलाई प्रायः पहिलो आधुनिक उपन्यास भनिन्छ।", BR)
add("Culture", "William Shakespeare is credited with adding more than 1,700 words to the English language.",
    "विलियम शेक्सपियरले अङ्ग्रेजी भाषामा १,७०० भन्दा बढी शब्द थपेको श्रेय पाउँछन्।", BR)
add("Culture", "The Kumbh Mela in India is the largest religious gathering in the world.",
    "भारतको कुम्भ मेला विश्वको सबैभन्दा ठूलो धार्मिक जमघट हो।", "UNESCO")
add("Culture", "The Nepali New Year falls in mid-April, on the first day of Baisakh.",
    "नेपाली नयाँ वर्ष अप्रिलको मध्यमा, बैशाख १ गते पर्छ।", BR)
add("Culture", "Dal Bhat — lentils and rice with vegetables — is the traditional everyday meal of Nepal.",
    "दाल भात — तरकारीसहित दाल र भात — नेपालको परम्परागत दैनिक खाना हो।", BR)
add("Culture", "Thangka painting, a traditional Buddhist art of Nepal and Tibet, is painted on cotton cloth.",
    "थाङ्का चित्रकला नेपाल र तिब्बतको परम्परागत बौद्ध कला हो, जुन कपासको कपडामा चित्रित गरिन्छ।", "UNESCO")
add("Culture", "'Dhanyabad' means 'thank you' in Nepali.",
    "'धन्यवाद' को अर्थ नेपालीमा 'thank you' हो।", BR)
add("Culture", "The Madal is a traditional double-headed drum of Nepal.",
    "मादल नेपालको परम्परागत दुई मुखे ढोल हो।", BR)
add("Culture", "The Sarangi is a traditional Nepali string instrument, played by the Gandharba community.",
    "सारंगी परम्परागत नेपाली तार वाद्ययन्त्र हो, जुन गन्धर्व समुदायले बजाउँछ।", BR)
add("Culture", "Indra Jatra, a festival of the Newar community, is celebrated in Kathmandu every September.",
    "नेवार समुदायको पर्व इन्द्रजात्रा हरेक सेप्टेम्बरमा काठमाडौंमा मनाइन्छ।", BR)
add("Culture", "Gai Jatra, the 'cow festival' of the Kathmandu Valley, honours family members who died in the past year.",
    "काठमाडौं उपत्यकाको 'गाईजात्रा' पर्वले पछिल्लो वर्षमा मृत्यु भएका परिवारका सदस्यहरूको सम्झना गर्छ।", BR)
add("Culture", "The word 'Sherpa' is both the name of an ethnic group of Nepal and a job title for Himalayan mountain guides.",
    "'शेर्पा' शब्द नेपालको एक जातीय समूहको नाम र हिमाली पर्वतारोहण गाइडको पेशागत नाम दुवै हो।", BR)
add("Culture", "Kite flying is a beloved part of Dashain in Nepal — the skies over Kathmandu fill with kites.",
    "चंगा उडाउनु नेपालमा दशैंको प्रिय अंग हो — काठमाडौंको आकाश चंगाले भरिन्छ।", BR)
add("Culture", "The Nepali language is written in the Devanagari script, the same script used for Hindi and Sanskrit.",
    "नेपाली भाषा देवनागरी लिपिमा लेखिन्छ, जुन हिन्दी र संस्कृतका लागि पनि प्रयोग हुने लिपि हो।", BR)

# ---------------- write out ----------------
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "funfacts.json"
OUT.write_text(json.dumps(F, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
from collections import Counter
counts = Counter(f["category"] for f in F)
print(f"total: {len(F)}")
for cat, n in sorted(counts.items()):
    print(f"  {cat}: {n}")
print(f"wrote {OUT}")
