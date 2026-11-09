#!/usr/bin/env python3
"""Generate data/festivals.json — verified Nepali festival dates + greetings.

EID EXCLUSION (user instruction, 2026-11-09): Eid al-Fitr and Bakr Eid
(Eid al-Adha) are NOT included in this file, by explicit user request.
Every other festival celebrated in Nepal is included.

Dates verified 2026-11-09 against Nepali patro sources (primary: ashesh.com.np
full patro, 2083 Kartik–Chaitra + 2084 Baishakh–Chaitra; second sources per row
in the research notes). Rules: never guess a date — unverifiable dates are
excluded, not carried from another year. Confidence: high = 2+ sources agree;
medium = single reputable source (ashesh patro) — those entries should be
re-verified against the Government of Nepal holiday list when it publishes.

BS month lengths (corrected 2026-11-09, see assets/js/app.js):
  2083: [31,32,31,32,31,30,30,29,30,29,30,30]  (Mangsir 29, Poush 30)
  2084: [31,32,31,32,31,30,30,30,29,29,30,31]  (Magh 29, Falgun 30)
Today (2026-11-09) = Kartik 23, 2083 = Gai Tihar day.

Usage: python3 scripts/gen-festivals.py  (writes data/festivals.json)
Verify with: python3 -m py_compile scripts/gen-festivals.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ASH = "https://www.ashesh.com.np/nepali-calendar/?year={y}&month={m}"

def src(y, m):
    return ASH.format(y=y, m=m)

# (id, name_en, name_ne, start_bs, end_bs, emoji, accent, confidence, source, greeting_en, greeting_ne)
F = [
 # ---- Tihar 2083 (in progress right now: 7–11 Nov 2026) ----
 ("tihar-kaag-2026", "Kaag Tihar", "काग तिहार", "2083-07-21", "2083-07-21", "🐦", "#f97316", "high", src(2083, "Kartik"),
  "Happy Kaag Tihar! The crow, messenger of good news, is honoured today — may it bring glad tidings to your home.",
  "काग तिहारको शुभकामना! शुभ समाचारको दूत कागलाई सम्मान गरिने आजको दिन तपाईंको घरमा सुखद खबर आओस्।"),
 ("tihar-kukur-2026", "Kukur Tihar", "कुकुर तिहार", "2083-07-22", "2083-07-22", "🐕", "#f97316", "high", src(2083, "Kartik"),
  "Happy Kukur Tihar! Today we honour the loyal dog — may loyalty and friendship fill your life.",
  "कुकुर तिहारको शुभकामना! वफादार कुकुरलाई सम्मान गरिने आजको दिन तपाईंको जीवनमा वफादारी र मित्रता भरियोस्।"),
 ("tihar-laxmi-puja-2026", "Laxmi Puja", "लक्ष्मी पूजा", "2083-07-22", "2083-07-22", "✨", "#f59e0b", "high", src(2083, "Kartik"),
  "Happy Laxmi Puja! May Goddess Laxmi bless your home with light, wealth and happiness.",
  "लक्ष्मी पूजाको शुभकामना! लक्ष्मी माताले तपाईंको घरमा उज्यालो, समृद्धि र सुखशान्ति प्रदान गरून्।"),
 ("tihar-gai-2026", "Gai Tihar", "गाइतिहार", "2083-07-23", "2083-07-23", "🐄", "#f97316", "high", src(2083, "Kartik"),
  "Happy Gai Tihar! May the gentle cow's blessings bring peace and prosperity to your family.",
  "गाइतिहारको शुभकामना! गाईको आशीर्वादले तपाईंको परिवारमा शान्ति र समृद्धि ल्याओस्।"),
 ("tihar-govardhan-2026", "Govardhan Puja / Mha Puja", "गोवर्द्धन पूजा", "2083-07-24", "2083-07-24", "🏔️", "#f97316", "high", src(2083, "Kartik"),
  "Happy Govardhan Puja and Mha Puja! A day to honour yourself and the hills that protect us.",
  "गोवर्द्धन पूजा तथा म्हः पूजाको शुभकामना! आफूलाई र हामीलाई जोगाउने पहाडलाई सम्मान गर्ने दिन।"),
 ("tihar-bhai-tika-2026", "Bhai Tika", "भाइटीका", "2083-07-25", "2083-07-25", "👫", "#f97316", "high", src(2083, "Kartik"),
  "Happy Bhai Tika! May the bond between brothers and sisters grow stronger with every tika.",
  "भाइटीकाको शुभकामना! दाजुभाइ–दिदीबहिनीको माया र बन्धन हरेक टीकासँगै अझ गहिरो होस्।"),
 # ---- Late 2083 ----
 ("chhath-2026", "Chhath Parva", "छठपर्व", "2083-07-27", "2083-07-29", "🌞", "#ea580c", "high", src(2083, "Kartik"),
  "Happy Chhath! May the Sun God bless you with health, energy and a bright future.",
  "छठपर्वको शुभकामना! सूर्य देवले तपाईंलाई स्वास्थ्य, ऊर्जा र उज्यालो भविष्य प्रदान गरून्।"),
 ("udhauli-yomari-punhi-2026", "Udhauli (Yomari Punhi)", "उधौली पर्व (योमरी पुन्ही)", "2083-09-09", "2083-09-09", "🌾", "#65a30d", "medium", src(2083, "Poush"),
  "Happy Udhauli! As the Kirat community moves downhill for winter, may the harvest bring joy to every home.",
  "उधौली पर्वको शुभकामना! जाडोका लागि तल झर्ने किरात समुदायको यो पर्वमा बालीले हरेक घरमा खुशी ल्याओस्।"),
 ("christmas-2026", "Christmas", "क्रिसमस", "2083-09-10", "2083-09-10", "🎄", "#16a34a", "high", src(2083, "Poush"),
  "Merry Christmas! May your day be full of warmth, kindness and time with loved ones.",
  "क्रिसमसको शुभकामना! तपाईंको दिन न्यानोपन, दया र प्रियजनसँगको समयले भरियोस्।"),
 ("tamu-lhosar-2026", "Tamu Lhosar", "तमु ल्होसार", "2083-09-15", "2083-09-15", "🎉", "#7c3aed", "high", src(2083, "Poush"),
  "Happy Tamu Lhosar! The Gurung New Year — may the new cycle bring health and happiness.",
  "तमु ल्होसारको शुभकामना! गुरुङ नयाँ वर्ष — नयाँ चक्रले स्वास्थ्य र खुशी ल्याओस्।"),
 ("english-new-year-2027", "English New Year", "अङ्ग्रेजी नयाँ वर्ष", "2083-09-17", "2083-09-17", "🎆", "#f59e0b", "high", src(2083, "Poush"),
  "Happy New Year! A fresh year, fresh goals — may 2027 bring you success in every exam.",
  "अङ्ग्रेजी नयाँ वर्षको शुभकामना! नयाँ वर्ष, नयाँ लक्ष्य — २०२७ ले तपाईंलाई हरेक परीक्षामा सफलता देओस्।"),
 ("tol-lhosar-2027-01", "Tol Lhosar", "तोल ल्होसार", "2083-09-24", "2083-09-24", "🎉", "#7c3aed", "medium", src(2083, "Poush"),
  "Happy Tol Lhosar! New Year greetings to the Tol community and all who celebrate.",
  "तोल ल्होसारको शुभकामना! तोल समुदाय तथा मनाउने सबैलाई नयाँ वर्षको शुभकामना।"),
 ("maghe-sankranti-2027", "Maghe Sankranti (Maghi)", "माघे संक्रान्ति (माघी पर्व)", "2083-10-01", "2083-10-01", "🌞", "#f59e0b", "high", src(2083, "Magh"),
  "Happy Maghe Sankranti! May the winter sun warm your home and sweet til bring sweetness to your year.",
  "माघे संक्रान्तिको शुभकामना! जाडोको घामले तपाईंको घर न्यानो बनाओस् र तिलको मिठासले वर्ष मिठो होस्।"),
 ("sonam-lhosar-2027", "Sonam Lhosar", "सोनाम ल्होसार", "2083-10-24", "2083-10-24", "🎉", "#7c3aed", "high", src(2083, "Magh"),
  "Happy Sonam Lhosar! The Tamang New Year — may it bring peace, prosperity and new beginnings.",
  "सोनाम ल्होसारको शुभकामना! तामाङ नयाँ वर्ष — शान्ति, समृद्धि र नयाँ सुरुवात ल्याओस्।"),
 ("saraswati-puja-2027", "Saraswati Puja (Shree Panchami)", "सरस्वती पूजा (श्री पञ्चमी)", "2083-10-28", "2083-10-28", "📚", "#fbbf24", "high", src(2083, "Magh"),
  "Happy Saraswati Puja! May the goddess of learning bless your studies and sharpen your mind.",
  "सरस्वती पूजाको शुभकामना! विद्याकी देवीले तपाईंको अध्ययनमा आशीर्वाद दिऊन् र मन तीक्ष्ण बनाऊन्।"),
 ("maha-shivaratri-2027", "Maha Shivaratri", "महाशिवरात्रि", "2083-11-22", "2083-11-22", "🌙", "#6366f1", "high", src(2083, "Falgun"),
  "Happy Maha Shivaratri! May Lord Shiva bless you with strength, focus and calm on the great night.",
  "महाशिवरात्रिको शुभकामना! महादेवले तपाईंलाई शक्ति, एकाग्रता र शान्ति प्रदान गरून्।"),
 ("gyalpo-lhosar-2027", "Gyalpo Lhosar", "ग्याल्पो ल्होसार", "2083-11-25", "2083-11-25", "🎉", "#7c3aed", "high", src(2083, "Falgun"),
  "Happy Gyalpo Lhosar! The Sherpa New Year — may the new year bring joy and good fortune.",
  "ग्याल्पो ल्होसारको शुभकामना! शेर्पा नयाँ वर्ष — नयाँ वर्षले खुशी र सौभाग्य ल्याओस्।"),
 ("holi-hills-2027", "Holi — Hills (Fagu Purnima)", "पहाडमा होली (फागुपूर्णिमा)", "2083-12-07", "2083-12-07", "🎨", "#ec4899", "high", src(2083, "Chaitra"),
  "Happy Holi! May your life fill with the colours of joy, friendship and new beginnings.",
  "होलीको शुभकामना! तपाईंको जीवन खुशी, मित्रता र नयाँ सुरुवातका रङले भरियोस्।"),
 ("holi-terai-2027", "Holi — Terai", "तराईमा होली", "2083-12-08", "2083-12-08", "🎨", "#ec4899", "high", src(2083, "Chaitra"),
  "Happy Holi! May your life fill with the colours of joy, friendship and new beginnings.",
  "होलीको शुभकामना! तपाईंको जीवन खुशी, मित्रता र नयाँ सुरुवातका रङले भरियोस्।"),
 ("ghode-jatra-2027", "Ghode Jatra", "घोडेजात्रा", "2083-12-23", "2083-12-23", "🐎", "#92400e", "medium", src(2083, "Chaitra"),
  "Happy Ghode Jatra! The ancient horse festival of the Valley — may it bring courage and speed to your dreams.",
  "घोडेजात्राको शुभकामना! उपत्यकाको प्राचीन घोडा जात्रा — यसले तपाईंका सपनामा साहस र गति ल्याओस्।"),
 ("bisket-jatra-2027", "Bisket Jatra", "बिस्का जात्रा", "2083-12-27", "2084-01-05", "🎉", "#dc2626", "medium", src(2083, "Chaitra"),
  "Happy Bisket Jatra! Bhaktapur's great chariot festival — may the new year roll in with joy and energy.",
  "बिस्का जात्राको शुभकामना! भक्तपुरको महान् रथ जात्रा — नयाँ वर्ष खुशी र ऊर्जासहित आओस्।"),
 # ---- 2084, Baisakh–Ashwin ----
 ("nepali-new-year-2027", "Nepali New Year", "नेपाली नयाँ वर्ष", "2084-01-01", "2084-01-01", "🎆", "#f59e0b", "high", src(2084, "Baishakh"),
  "Happy Nepali New Year! 2084 — a fresh year of goals, growth and new chances. May it be your best year yet.",
  "नेपाली नयाँ वर्षको शुभकामना! २०८४ — लक्ष्य, विकास र नयाँ अवसरहरूको नयाँ वर्ष। यो तपाईंको सबैभन्दा राम्रो वर्ष होस्।"),
 ("chaite-dashain-2027", "Chaite Dashain", "चैते दशैँ", "2084-01-01", "2084-01-01", "🌸", "#dc2626", "medium", src(2084, "Baishakh"),
  "Happy Chaite Dashain! The spring Dashain — may it bring renewal, strength and blessings to your family.",
  "चैते दशैँको शुभकामना! वसन्तको दशैँ — यसले तपाईंको परिवारमा नवीकरण, शक्ति र आशीर्वाद ल्याओस्।"),
 ("ram-navami-2027", "Ram Navami", "रामनवमी", "2084-01-02", "2084-01-02", "🌸", "#f59e0b", "medium", src(2084, "Baishakh"),
  "Happy Ram Navami! May Lord Ram bless you with courage, truth and righteousness.",
  "रामनवमीको शुभकामना! भगवान् रामले तपाईंलाई साहस, सत्य र धर्म प्रदान गरून्।"),
 ("buddha-jayanti-2027", "Buddha Jayanti", "बुद्ध जयन्ती", "2084-02-06", "2084-02-06", "🌸", "#f59e0b", "high", src(2084, "Jestha"),
  "Happy Buddha Jayanti! May the Buddha's light of peace and wisdom guide your path.",
  "बुद्ध जयन्तीको शुभकामना! बुद्धको शान्ति र ज्ञानको उज्यालोले तपाईंको बाटो देखाओस्।"),
 ("ubhauli-2027", "Ubhauli", "उभौली पर्व", "2084-02-06", "2084-02-06", "🌾", "#65a30d", "medium", src(2084, "Jestha"),
  "Happy Ubhauli! As the Kirat community moves uphill for summer, may the season bring growth and joy.",
  "उभौली पर्वको शुभकामना! गर्मीका लागि माथि उक्लने किरात समुदायको यो पर्वले वृद्धि र खुशी ल्याओस्।"),
 ("nag-panchami-2027", "Nag Panchami", "नाग पञ्चमी", "2084-04-21", "2084-04-21", "🐍", "#16a34a", "medium", src(2084, "Shrawan"),
  "Happy Nag Panchami! May the serpent deities protect your home and family.",
  "नाग पञ्चमीको शुभकामना! नाग देवताले तपाईंको घर र परिवारको रक्षा गरून्।"),
 ("janai-purnima-2027", "Janai Purnima (Raksha Bandhan)", "जनै पूर्णिमा", "2084-04-32", "2084-04-32", "🧵", "#f59e0b", "medium", src(2084, "Shrawan"),
  "Happy Janai Purnima! A day of renewal and protection — may the sacred thread guard you through the year.",
  "जनै पूर्णिमाको शुभकामना! नवीकरण र रक्षाको दिन — पवित्र जनैले वर्षभरि तपाईंको रक्षा गरोस्।"),
 ("gai-jatra-2027", "Gai Jatra", "गाईजात्रा", "2084-05-01", "2084-05-01", "🐄", "#f97316", "medium", src(2084, "Bhadra"),
  "Happy Gai Jatra! The festival of laughter through tears — may it bring lightness and remembrance.",
  "गाईजात्राको शुभकामना! आँसुबीचको हाँसोको पर्व — यसले हलुकापन र सम्झना ल्याओस्।"),
 ("krishna-janmashtami-2027", "Krishna Janmashtami", "श्रीकृष्ण जन्माष्टमी", "2084-05-08", "2084-05-08", "🎶", "#3b82f6", "medium", src(2084, "Bhadra"),
  "Happy Krishna Janmashtami! May Lord Krishna's flute fill your life with melody and joy.",
  "श्रीकृष्ण जन्माष्टमीको शुभकामना! भगवान् श्रीकृष्णको बाँसुरीले तपाईंको जीवनमा सुमधुरता र खुशी भरिदेओस्।"),
 ("haritalika-teej-2027", "Haritalika Teej", "हरितालिका (तीज)", "2084-05-17", "2084-05-17", "🌸", "#dc2626", "medium", src(2084, "Bhadra"),
  "Happy Haritalika Teej! May the fast of devotion bless married life and every wish of the heart.",
  "हरितालिका तीजको शुभकामना! भक्तिको व्रतले वैवाहिक जीवन र मनका हरेक इच्छा पूरा गरोस्।"),
 ("rishi-panchami-2027", "Rishi Panchami", "ऋषि पञ्चमी", "2084-05-19", "2084-05-19", "🌿", "#65a30d", "medium", src(2084, "Bhadra"),
  "Happy Rishi Panchami! A day of cleansing and respect for the sages — may it bring purity and peace.",
  "ऋषि पञ्चमीको शुभकामना! ऋषिहरूको सम्मान र शुद्धिको दिन — यसले पवित्रता र शान्ति ल्याओस्।"),
 ("indra-jatra-2027", "Indra Jatra", "इन्द्रजात्रा", "2084-05-28", "2084-05-28", "🌧️", "#0ea5e9", "medium", src(2084, "Bhadra"),
  "Happy Indra Jatra! The Valley's great festival of the rain god — may it bring rain, harvest and joy.",
  "इन्द्रजात्राको शुभकामना! वर्षाका देवताको उपत्यकाको महान् पर्व — यसले वर्षा, बाली र खुशी ल्याओस्।"),
 ("jitiya-2027", "Jitiya", "जितिया पर्व", "2084-06-06", "2084-06-06", "🌙", "#7c3aed", "medium", src(2084, "Ashwin"),
  "Happy Jitiya! May the mothers' fast bless their children with long life and health.",
  "जितिया पर्वको शुभकामना! आमाहरूको व्रतले सन्तानलाई दीर्घायु र स्वास्थ्य प्रदान गरोस्।"),
 ("dashain-ghatasthapana-2027", "Ghatasthapana (Dashain Day 1)", "घटस्थापना", "2084-06-13", "2084-06-13", "🌸", "#dc2626", "medium", src(2084, "Ashwin"),
  "Happy Ghatasthapana! Dashain begins — the sacred jamara is sown, and nine nights of blessings begin.",
  "घटस्थापनाको शुभकामना! दशैँ सुरु भयो — पवित्र जमरा रोपियो, नौ रातका आशीर्वाद सुरु भए।"),
 ("dashain-phulpati-2027", "Phulpati", "फूलपाती", "2084-06-19", "2084-06-19", "💐", "#dc2626", "medium", src(2084, "Ashwin"),
  "Happy Phulpati! The flowers of Dashain arrive — may the festival fill your home with joy.",
  "फूलपातीको शुभकामना! दशैँका फूलहरू आए — यस पर्वले तपाईंको घर खुशीले भरियोस्।"),
 ("dashain-maha-ashtami-2027", "Maha Ashtami", "महाष्टमी", "2084-06-20", "2084-06-21", "✨", "#dc2626", "medium", src(2084, "Ashwin"),
  "Happy Maha Ashtami! On this powerful night of Dashain, may the goddess bless you with strength.",
  "महाष्टमीको शुभकामना! दशैँको यस शक्तिशाली रातमा देवीले तपाईंलाई शक्ति प्रदान गरून्।"),
 ("dashain-maha-navami-2027", "Maha Navami", "महानवमी", "2084-06-22", "2084-06-22", "✨", "#dc2626", "high", src(2084, "Ashwin"),
  "Happy Maha Navami! The ninth night of Dashain — may it bring victory over every obstacle.",
  "महानवमीको शुभकामना! दशैँको नवौं रात — यसले हरेक बाधामाथि विजय ल्याओस्।"),
 ("dashain-vijaya-dashami-2027", "Vijaya Dashami", "विजया दशमी", "2084-06-23", "2084-06-23", "🎉", "#dc2626", "high", src(2084, "Ashwin"),
  "Happy Vijaya Dashami! The day of victory and tika — may elders' blessings guide you to success.",
  "विजया दशमीको शुभकामना! विजय र टीकाको दिन — अग्रजहरूको आशीर्वादले तपाईंलाई सफलता दिलाओस्।"),
 ("dashain-kojagrat-purnima-2027", "Kojagrat Purnima", "कोजाग्रत पूर्णिमा", "2084-06-28", "2084-06-28", "🌕", "#f59e0b", "high", src(2084, "Ashwin"),
  "Happy Kojagrat Purnima! The full-moon night of Dashain — may Laxmi's blessings stay with you all year.",
  "कोजाग्रत पूर्णिमाको शुभकामना! दशैँको पूर्णिमाको रात — लक्ष्मीको आशीर्वाद वर्षभरि तपाईंसँग रहोस्।"),

 # ---- Tihar 2084 + late 2084 ----
 ("tihar-kaag-2027", "Kaag Tihar", "काग तिहार", "2084-07-10", "2084-07-10", "🐦", "#f97316", "high", src(2084, "Kartik"),
  "Happy Kaag Tihar! The crow, messenger of good news, is honoured today — may it bring glad tidings to your home.",
  "काग तिहारको शुभकामना! शुभ समाचारको दूत कागलाई सम्मान गरिने आजको दिन तपाईंको घरमा सुखद खबर आओस्।"),
 ("tihar-kukur-2027", "Kukur Tihar", "कुकुर तिहार", "2084-07-11", "2084-07-11", "🐕", "#f97316", "high", src(2084, "Kartik"),
  "Happy Kukur Tihar! Today we honour the loyal dog — may loyalty and friendship fill your life.",
  "कुकुर तिहारको शुभकामना! वफादार कुकुरलाई सम्मान गरिने आजको दिन तपाईंको जीवनमा वफादारी र मित्रता भरियोस्।"),
 ("tihar-laxmi-puja-2027", "Laxmi Puja", "लक्ष्मी पूजा", "2084-07-12", "2084-07-12", "✨", "#f59e0b", "high", src(2084, "Kartik"),
  "Happy Laxmi Puja! May Goddess Laxmi bless your home with light, wealth and happiness.",
  "लक्ष्मी पूजाको शुभकामना! लक्ष्मी माताले तपाईंको घरमा उज्यालो, समृद्धि र सुखशान्ति प्रदान गरून्।"),
 ("tihar-gai-2027", "Gai Tihar", "गाइतिहार", "2084-07-12", "2084-07-12", "🐄", "#f97316", "high", src(2084, "Kartik"),
  "Happy Gai Tihar! May the gentle cow's blessings bring peace and prosperity to your family.",
  "गाइतिहारको शुभकामना! गाईको आशीर्वादले तपाईंको परिवारमा शान्ति र समृद्धि ल्याओस्।"),
 ("tihar-govardhan-2027", "Govardhan Puja / Mha Puja", "गोवर्द्धन पूजा", "2084-07-13", "2084-07-13", "🏔️", "#f97316", "high", src(2084, "Kartik"),
  "Happy Govardhan Puja and Mha Puja! A day to honour yourself and the hills that protect us.",
  "गोवर्द्धन पूजा तथा म्हः पूजाको शुभकामना! आफूलाई र हामीलाई जोगाउने पहाडलाई सम्मान गर्ने दिन।"),
 ("tihar-bhai-tika-2027", "Bhai Tika", "भाइटीका", "2084-07-14", "2084-07-14", "👫", "#f97316", "high", src(2084, "Kartik"),
  "Happy Bhai Tika! May the bond between brothers and sisters grow stronger with every tika.",
  "भाइटीकाको शुभकामना! दाजुभाइ–दिदीबहिनीको माया र बन्धन हरेक टीकासँगै अझ गहिरो होस्।"),
 ("chhath-2027", "Chhath Parva", "छठपर्व", "2084-07-16", "2084-07-18", "🌞", "#ea580c", "medium", src(2084, "Kartik"),
  "Happy Chhath! May the Sun God bless you with health, energy and a bright future.",
  "छठपर्वको शुभकामना! सूर्य देवले तपाईंलाई स्वास्थ्य, ऊर्जा र उज्यालो भविष्य प्रदान गरून्।"),
 ("udhauli-yomari-punhi-2027", "Udhauli (Yomari Punhi)", "उधौली पर्व (योमरी पुन्ही)", "2084-08-27", "2084-08-27", "🌾", "#65a30d", "medium", src(2084, "Mangsir"),
  "Happy Udhauli! As the Kirat community moves downhill for winter, may the harvest bring joy to every home.",
  "उधौली पर्वको शुभकामना! जाडोका लागि तल झर्ने किरात समुदायको यो पर्वमा बालीले हरेक घरमा खुशी ल्याओस्।"),
 ("christmas-2027", "Christmas", "क्रिसमस", "2084-09-09", "2084-09-09", "🎄", "#16a34a", "high", src(2084, "Poush"),
  "Merry Christmas! May your day be full of warmth, kindness and time with loved ones.",
  "क्रिसमसको शुभकामना! तपाईंको दिन न्यानोपन, दया र प्रियजनसँगको समयले भरियोस्।"),
 ("tol-lhosar-2027-12", "Tol Lhosar", "तोल ल्होसार", "2084-09-12", "2084-09-12", "🎉", "#7c3aed", "medium", src(2084, "Poush"),
  "Happy Tol Lhosar! New Year greetings to the Tol community and all who celebrate.",
  "तोल ल्होसारको शुभकामना! तोल समुदाय तथा मनाउने सबैलाई नयाँ वर्षको शुभकामना।"),
 ("tamu-lhosar-2027", "Tamu Lhosar", "तमु ल्होसार", "2084-09-15", "2084-09-15", "🎉", "#7c3aed", "medium", src(2084, "Poush"),
  "Happy Tamu Lhosar! The Gurung New Year — may the new cycle bring health and happiness.",
  "तमु ल्होसारको शुभकामना! गुरुङ नयाँ वर्ष — नयाँ चक्रले स्वास्थ्य र खुशी ल्याओस्।"),
 ("english-new-year-2028", "English New Year", "अङ्ग्रेजी नयाँ वर्ष", "2084-09-16", "2084-09-16", "🎆", "#f59e0b", "high", src(2084, "Poush"),
  "Happy New Year! A fresh year, fresh goals — may 2028 bring you success in every exam.",
  "अङ्ग्रेजी नयाँ वर्षको शुभकामना! नयाँ वर्ष, नयाँ लक्ष्य — २०२८ ले तपाईंलाई हरेक परीक्षामा सफलता देओस्।"),
 ("maghe-sankranti-2028", "Maghe Sankranti (Maghi)", "माघे संक्रान्ति (माघी पर्व)", "2084-10-01", "2084-10-01", "🌞", "#f59e0b", "medium", src(2084, "Magh"),
  "Happy Maghe Sankranti! May the winter sun warm your home and sweet til bring sweetness to your year.",
  "माघे संक्रान्तिको शुभकामना! जाडोको घामले तपाईंको घर न्यानो बनाओस् र तिलको मिठासले वर्ष मिठो होस्।"),
 ("sonam-lhosar-2028", "Sonam Lhosar", "सोनाम ल्होसार", "2084-10-13", "2084-10-13", "🎉", "#7c3aed", "medium", src(2084, "Magh"),
  "Happy Sonam Lhosar! The Tamang New Year — may it bring peace, prosperity and new beginnings.",
  "सोनाम ल्होसारको शुभकामना! तामाङ नयाँ वर्ष — शान्ति, समृद्धि र नयाँ सुरुवात ल्याओस्।"),
 ("saraswati-puja-2028", "Saraswati Puja (Shree Panchami)", "सरस्वती पूजा (श्री पञ्चमी)", "2084-10-18", "2084-10-18", "📚", "#fbbf24", "medium", src(2084, "Magh"),
  "Happy Saraswati Puja! May the goddess of learning bless your studies and sharpen your mind.",
  "सरस्वती पूजाको शुभकामना! विद्याकी देवीले तपाईंको अध्ययनमा आशीर्वाद दिऊन् र मन तीक्ष्ण बनाऊन्।"),
 ("maha-shivaratri-2028", "Maha Shivaratri", "महाशिवरात्रि", "2084-11-11", "2084-11-11", "🌙", "#6366f1", "high", src(2084, "Falgun"),
  "Happy Maha Shivaratri! May Lord Shiva bless you with strength, focus and calm on the great night.",
  "महाशिवरात्रिको शुभकामना! महादेवले तपाईंलाई शक्ति, एकाग्रता र शान्ति प्रदान गरून्।"),
 ("gyalpo-lhosar-2028", "Gyalpo Lhosar", "ग्याल्पो ल्होसार", "2084-11-14", "2084-11-14", "🎉", "#7c3aed", "medium", src(2084, "Falgun"),
  "Happy Gyalpo Lhosar! The Sherpa New Year — may the new year bring joy and good fortune.",
  "ग्याल्पो ल्होसारको शुभकामना! शेर्पा नयाँ वर्ष — नयाँ वर्षले खुशी र सौभाग्य ल्याओस्।"),
 ("holi-hills-2028", "Holi — Hills (Fagu Purnima)", "पहाडमा होली (फागुपूर्णिमा)", "2084-11-27", "2084-11-27", "🎨", "#ec4899", "high", src(2084, "Falgun"),
  "Happy Holi! May your life fill with the colours of joy, friendship and new beginnings.",
  "होलीको शुभकामना! तपाईंको जीवन खुशी, मित्रता र नयाँ सुरुवातका रङले भरियोस्।"),
 ("holi-terai-2028", "Holi — Terai", "तराईमा होली", "2084-11-28", "2084-11-28", "🎨", "#ec4899", "high", src(2084, "Falgun"),
  "Happy Holi! May your life fill with the colours of joy, friendship and new beginnings.",
  "होलीको शुभकामना! तपाईंको जीवन खुशी, मित्रता र नयाँ सुरुवातका रङले भरियोस्।"),
 ("ghode-jatra-2028", "Ghode Jatra", "घोडेजात्रा", "2084-12-13", "2084-12-13", "🐎", "#92400e", "medium", src(2084, "Chaitra"),
  "Happy Ghode Jatra! The ancient horse festival of the Valley — may it bring courage and speed to your dreams.",
  "घोडेजात्राको शुभकामना! उपत्यकाको प्राचीन घोडा जात्रा — यसले तपाईंका सपनामा साहस र गति ल्याओस्।"),
 ("chaite-dashain-2028", "Chaite Dashain", "चैते दशैँ", "2084-12-21", "2084-12-21", "🌸", "#dc2626", "medium", src(2084, "Chaitra"),
  "Happy Chaite Dashain! The spring Dashain — may it bring renewal, strength and blessings to your family.",
  "चैते दशैँको शुभकामना! वसन्तको दशैँ — यसले तपाईंको परिवारमा नवीकरण, शक्ति र आशीर्वाद ल्याओस्।"),
 ("ram-navami-2028", "Ram Navami", "रामनवमी", "2084-12-22", "2084-12-22", "🌸", "#f59e0b", "medium", src(2084, "Chaitra"),
  "Happy Ram Navami! May Lord Ram bless you with courage, truth and righteousness.",
  "रामनवमीको शुभकामना! भगवान् रामले तपाईंलाई साहस, सत्य र धर्म प्रदान गरून्।"),
 ("bisket-jatra-2028", "Bisket Jatra", "बिस्का जात्रा", "2084-12-28", "2085-01-05", "🎉", "#dc2626", "medium",
  "https://www.swotahtravel.com/blogs/all-you-need-to-know-about-bisket-jatra",
  "Happy Bisket Jatra! Bhaktapur's great chariot festival — may the new year roll in with joy and energy.",
  "बिस्का जात्राको शुभकामना! भक्तपुरको महान् रथ जात्रा — नयाँ वर्ष खुशी र ऊर्जासहित आओस्।"),
]

KEYS = ["id", "name_en", "name_ne", "start_bs", "end_bs", "emoji", "accent",
        "confidence", "source", "greeting_en", "greeting_ne"]


def main() -> int:
    out = []
    seen = set()
    for row in F:
        assert len(row) == len(KEYS), f"bad row: {row[0]}"
        d = dict(zip(KEYS, row))
        assert d["id"] not in seen, f"duplicate id {d['id']}"
        seen.add(d["id"])
        assert d["start_bs"] <= d["end_bs"], f"bad window {d['id']}"
        assert d["confidence"] in ("high", "medium"), f"bad confidence {d['id']}"
        assert d["emoji"] and d["accent"].startswith("#"), f"bad style {d['id']}"
        assert d["greeting_en"] and d["greeting_ne"], f"missing greeting {d['id']}"
        # Eid exclusion guard — the file must never contain Eid entries.
        low = (d["id"] + d["name_en"] + d["name_ne"]).lower()
        assert "eid" not in low and "bakr" not in low and "bakra" not in low, \
            f"Eid entry slipped in: {d['id']}"
        d["verified"] = "2026-11-09"
        out.append(d)
    out.sort(key=lambda e: (e["start_bs"], e["id"]))
    target = ROOT / "data" / "festivals.json"
    target.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")
    print(f"wrote {target} — {len(out)} festivals "
          f"({sum(1 for e in out if e['confidence']=='high')} high, "
          f"{sum(1 for e in out if e['confidence']=='medium')} medium)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
