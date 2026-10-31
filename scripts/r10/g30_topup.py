#!/usr/bin/env python3
"""R10 generator 30: top-up (~2,000). Vocab list 5 (C-F words), Maths 9,
IQ 6. Uses Bank(include R10) so cross-R10 duplicates are caught at
generation time. Lessons applied: explanations never start 'The answer is';
NE explanations end with the marked value as the last '=' value."""
import sys, random, math, datetime
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num
from vocab_data import WORDS as WORDS1
from vocab_data2 import WORDS2

def ord_s(n):
    """English ordinal suffix: 1st, 2nd, 3rd, 4th, 11th, 21st, 22nd, 23rd..."""
    n = int(n)
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


# include R10 files in the bank index this time (prefix that matches nothing)
bank = Bank(exclude_prefix='ZZZ-NONE-')
rng = random.Random(60606)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'tsc-primary', 'tsc-secondary', 'police', 'army', 'health']

# ================= VOCAB 5 =================
emv = Emitter(bank, 'R10-VOC5')
WORDS5 = [
    ('calm', 'शान्त', 'peaceful', 'शान्तिपूर्ण', 'agitated', 'उत्तेजित', 'serene', 'शान्त', 'noisy', 'कोलाहलपूर्ण'),
    ('candid', 'स्पष्टवादी', 'frank', 'खुला', 'secretive', 'गोप्य', 'honest', 'इमानदार', 'deceitful', 'धोकेबाज'),
    ('capable', 'सक्षम', 'able', 'योग्य', 'incapable', 'अक्षम', 'competent', 'दक्ष', 'helpless', 'असहाय'),
    ('careful', 'सावधान', 'cautious', 'सतर्क', 'careless', 'लापरवाह', 'attentive', 'ध्यान दिने', 'reckless', 'लापरवाह'),
    ('carry', 'बोक्नु', 'transport', 'ढुवानी गर्नु', 'drop', 'खसाल्नु', 'convey', 'पुर्‍याउनु', 'leave', 'छोड्नु'),
    ('catch', 'समात्नु', 'capture', 'पक्रनु', 'release', 'छोड्नु', 'seize', 'समात्नु', 'miss', 'छुटाउनु'),
    ('cause', 'कारण', 'reason', 'हेतु', 'effect', 'परिणाम', 'origin', 'उत्पत्ति', 'result', 'नतिजा'),
    ('cease', 'रोक्नु', 'stop', 'बन्द गर्नु', 'continue', 'जारी राख्नु', 'halt', 'रोक्नु', 'begin', 'सुरु गर्नु'),
    ('celebrate', 'मनाउनु', 'rejoice', 'खुसी मनाउनु', 'mourn', 'शोक गर्नु', 'observe', 'मनाउनु', 'ignore', 'बेवास्ता गर्नु'),
    ('certain', 'निश्चित', 'sure', 'पक्का', 'uncertain', 'अनिश्चित', 'definite', 'निश्चित', 'doubtful', 'शङ्कास्पद'),
    ('chance', 'अवसर', 'opportunity', 'मौका', 'certainty', 'निश्चितता', 'luck', 'भाग्य', 'fate', 'भाग्य'),
    ('change', 'परिवर्तन', 'alteration', 'बदलाव', 'stability', 'स्थिरता', 'shift', 'परिवर्तन', 'constancy', 'स्थिरता'),
    ('charge', 'शुल्क', 'fee', 'फि', 'free', 'निःशुल्क', 'cost', 'लागत', 'payment', 'भुक्तानी'),
    ('cheap', 'सस्तो', 'inexpensive', 'कम मूल्यको', 'expensive', 'महँगो', 'low-cost', 'सस्तो', 'dear', 'महँगो'),
    ('check', 'जाँच गर्नु', 'verify', 'प्रमाणित गर्नु', 'ignore', 'बेवास्ता गर्नु', 'inspect', 'निरीक्षण गर्नु', 'neglect', 'उपेक्षा गर्नु'),
    ('cheerful', 'प्रसन्न', 'happy', 'खुसी', 'gloomy', 'उदास', 'joyful', 'हर्षित', 'sad', 'दुःखी'),
    ('choice', 'छनोट', 'selection', 'चयन', 'rejection', 'अस्वीकार', 'option', 'विकल्प', 'compulsion', 'बाध्यता'),
    ('choose', 'छान्नु', 'select', 'चयन गर्नु', 'reject', 'अस्वीकार गर्नु', 'pick', 'छान्नु', 'refuse', 'इन्कार गर्नु'),
    ('circle', 'वृत्त', 'ring', 'घेरा', 'square', 'वर्ग', 'round', 'गोलो', 'line', 'रेखा'),
    ('citizen', 'नागरिक', 'resident', 'बासिन्दा', 'alien', 'विदेशी', 'subject', 'प्रजा', 'foreigner', 'विदेशी'),
    ('civil', 'नागरिक', 'civic', 'नागरिकसम्बन्धी', 'military', 'सैन्य', 'polite', 'शिष्ट', 'rude', 'अशिष्ट'),
    ('claim', 'दाबी गर्नु', 'assert', 'दाबी गर्नु', 'deny', 'अस्वीकार गर्नु', 'demand', 'माग गर्नु', 'surrender', 'आत्मसमर्पण गर्नु'),
    ('clean', 'सफा', 'tidy', 'व्यवस्थित', 'dirty', 'फोहोर', 'pure', 'शुद्ध', 'polluted', 'प्रदूषित'),
    ('clear', 'स्पष्ट', 'obvious', 'प्रस्ट', 'unclear', 'अस्पष्ट', 'transparent', 'पारदर्शी', 'vague', 'अस्पष्ट'),
    ('clever', 'चतुर', 'smart', 'बुद्धिमान्', 'foolish', 'मूर्ख', 'intelligent', 'बुद्धिमान्', 'dull', 'मन्द'),
    ('close', 'बन्द गर्नु', 'shut', 'बन्द गर्नु', 'open', 'खोल्नु', 'near', 'नजिक', 'far', 'टाढा'),
    ('cloth', 'कपडा', 'fabric', 'कपडा', 'material', 'सामग्री', 'garment', 'पोशाक', 'paper', 'कागज'),
    ('cloud', 'बादल', 'mist', 'कुहिरो', 'sky', 'आकाश', 'fog', 'हुस्सु', 'sun', 'सूर्य'),
    ('coach', 'प्रशिक्षक', 'trainer', 'तालिमकर्ता', 'player', 'खेलाडी', 'mentor', 'मार्गदर्शक', 'student', 'विद्यार्थी'),
    ('coast', 'तट', 'shore', 'किनार', 'beach', 'समुद्र तट', 'inland', 'भित्री भाग', 'cliff', 'चट्टान'),
    ('code', 'संहिता', 'law', 'कानुन', 'rule', 'नियम', 'cipher', 'गुप्त लेख', 'decode', 'गुप्त लेख खोल्नु'),
    ('coffee', 'कफी', 'beverage', 'पेय', 'tea', 'चिया', 'drink', 'पेय पदार्थ', 'milk', 'दूध'),
    ('cold', 'चिसो', 'chilly', 'जाडो', 'hot', 'तातो', 'cool', 'चिसो', 'warm', 'न्यानो'),
    ('collect', 'सङ्कलन गर्नु', 'gather', 'जम्मा गर्नु', 'scatter', 'छरिनु', 'accumulate', 'सङ्ग्रह गर्नु', 'distribute', 'वितरण गर्नु'),
    ('college', 'कलेज', 'institution', 'संस्था', 'school', 'विद्यालय', 'university', 'विश्वविद्यालय', 'academy', 'एकेडेमी'),
    ('colour', 'रङ', 'hue', 'रङ्ग', 'shade', 'छाया', 'tint', 'रङ', 'paint', 'पेन्ट'),
    ('come', 'आउनु', 'arrive', 'आइपुग्नु', 'go', 'जानु', 'reach', 'पुग्नु', 'leave', 'जानु'),
    ('comfort', 'आराम', 'ease', 'सुख', 'discomfort', 'असुविधा', 'relief', 'राहत', 'pain', 'दुखाइ'),
    ('command', 'आदेश', 'order', 'निर्देश', 'request', 'अनुरोध', 'directive', 'निर्देशन', 'plea', 'याचना'),
    ('common', 'सामान्य', 'ordinary', 'साधारण', 'rare', 'दुर्लभ', 'usual', 'सामान्य', 'unusual', 'असामान्य'),
    ('company', 'कम्पनी', 'firm', 'फर्म', 'business', 'व्यापार', 'corporation', 'निगम', 'individual', 'व्यक्ति'),
    ('compare', 'तुलना गर्नु', 'contrast', 'तुलना गर्नु', 'differ', 'फरक हुनु', 'match', 'मेल खानु', 'separate', 'छुट्याउनु'),
    ('compete', 'प्रतिस्पर्धा गर्नु', 'contest', 'प्रतियोगिता गर्नु', 'cooperate', 'सहयोग गर्नु', 'rival', 'प्रतिद्वन्द्वी', 'assist', 'सहयोग गर्नु'),
    ('complete', 'पूर्ण', 'finished', 'सम्पन्न', 'incomplete', 'अपूर्ण', 'total', 'कुल', 'partial', 'आंशिक'),
    ('complex', 'जटिल', 'complicated', 'कठिन', 'simple', 'सरल', 'intricate', 'जटिल', 'easy', 'सजिलो'),
    ('compose', 'रचना गर्नु', 'write', 'लेख्नु', 'destroy', 'नष्ट गर्नु', 'create', 'सिर्जना गर्नु', 'break', 'भाँच्नु'),
    ('concern', 'चिन्ता', 'worry', 'चिन्ता', 'unconcern', 'बेवास्ता', 'interest', 'रुचि', 'indifference', 'उदासीनता'),
    ('condition', 'अवस्था', 'state', 'स्थिति', 'situation', 'परिस्थिति', 'circumstance', 'परिस्थिति', 'health', 'स्वास्थ्य'),
    ('conduct', 'सञ्चालन गर्नु', 'manage', 'व्यवस्थापन गर्नु', 'misconduct', 'दुर्व्यवहार', 'lead', 'नेतृत्व गर्नु', 'follow', 'पछ्याउनु'),
    ('confirm', 'पुष्टि गर्नु', 'verify', 'प्रमाणित गर्नु', 'deny', 'अस्वीकार गर्नु', 'affirm', 'पुष्टि गर्नु', 'refute', 'खण्डन गर्नु'),
    ('conflict', 'द्वन्द्व', 'clash', 'टकराव', 'harmony', 'मेलमिलाप', 'dispute', 'विवाद', 'peace', 'शान्ति'),
    ('connect', 'जोड्नु', 'link', 'सम्पर्क गर्नु', 'disconnect', 'विच्छेद गर्नु', 'join', 'मिलाउनु', 'separate', 'छुट्याउनु'),
    ('consider', 'विचार गर्नु', 'think', 'सोच्नु', 'ignore', 'बेवास्ता गर्नु', 'ponder', 'मनन गर्नु', 'dismiss', 'खारेज गर्नु'),
    ('constant', 'स्थिर', 'steady', 'स्थिर', 'variable', 'परिवर्तनशील', 'fixed', 'निश्चित', 'changing', 'बदलिँदो'),
    ('construct', 'निर्माण गर्नु', 'build', 'बनाउनु', 'demolish', 'भत्काउनु', 'erect', 'खडा गर्नु', 'destroy', 'नष्ट गर्नु'),
    ('contain', 'समावेश गर्नु', 'include', 'समावेश गर्नु', 'exclude', 'बाहिर राख्नु', 'hold', 'समात्नु', 'release', 'छोड्नु'),
    ('content', 'सन्तुष्ट', 'satisfied', 'सन्तुष्ट', 'discontent', 'असन्तुष्ट', 'happy', 'खुसी', 'angry', 'रिसाएको'),
    ('continue', 'जारी राख्नु', 'proceed', 'अगाडि बढ्नु', 'stop', 'रोक्नु', 'persist', 'निरन्तर राख्नु', 'halt', 'रोक्नु'),
    ('control', 'नियन्त्रण', 'command', 'आदेश', 'freedom', 'स्वतन्त्रता', 'power', 'शक्ति', 'chaos', 'अव्यवस्था'),
    ('cook', 'पकाउनु', 'prepare', 'तयार गर्नु', 'bake', 'सेक्नु', 'boil', 'उमाल्नु', 'eat', 'खानु'),
    ('copy', 'प्रतिलिपि', 'duplicate', 'नक्कल', 'original', 'मौलिक', 'replica', 'प्रतिकृति', 'model', 'मोडेल'),
    ('correct', 'सही', 'right', 'ठीक', 'wrong', 'गलत', 'accurate', 'सटीक', 'false', 'झुटो'),
    ('cost', 'लागत', 'price', 'मूल्य', 'expense', 'खर्च', 'value', 'मूल्य', 'profit', 'नाफा'),
    ('cottage', 'कुटी', 'hut', 'झुपडी', 'house', 'घर', 'cabin', 'कुटी', 'palace', 'दरबार'),
    ('cotton', 'कपास', 'fibre', 'रेशा', 'silk', 'रेशम', 'wool', 'ऊन', 'nylon', 'नाइलन'),
    ('cough', 'खोकी', 'hack', 'खोक्नु', 'sneeze', 'हाच्छिउँ', 'cold', 'रुघा', 'fever', 'ज्वरो'),
    ('could', 'सक्नु', 'might', 'सक्छ', 'must', 'पर्छ', 'can', 'सक्छ', 'will', 'गर्नेछ'),
    ('council', 'परिषद्', 'committee', 'समिति', 'assembly', 'सभा', 'board', 'बोर्ड', 'member', 'सदस्य'),
    ('count', 'गन्नु', 'enumerate', 'गणना गर्नु', 'ignore', 'बेवास्ता गर्नु', 'calculate', 'हिसाब गर्नु', 'estimate', 'अनुमान गर्नु'),
    ('country', 'देश', 'nation', 'राष्ट्र', 'state', 'राज्य', 'land', 'भूमि', 'city', 'सहर'),
    ('courage', 'साहस', 'bravery', 'बहादुरी', 'cowardice', 'कायरता', 'valour', 'वीरता', 'fear', 'डर'),
    ('course', 'पाठ्यक्रम', 'curriculum', 'पाठ्यक्रम', 'subject', 'विषय', 'path', 'बाटो', 'lesson', 'पाठ'),
    ('court', 'अदालत', 'tribunal', 'न्यायाधिकरण', 'bench', 'बेन्च', 'judge', 'न्यायाधीश', 'prison', 'कारागार'),
    ('cover', 'ढाक्नु', 'conceal', 'लुकाउनु', 'uncover', 'खोल्नु', 'hide', 'लुकाउनु', 'reveal', 'प्रकट गर्नु'),
    ('crack', 'चर्किनु', 'split', 'फुट्नु', 'mend', 'मर्मत गर्नु', 'break', 'भाँच्नु', 'fix', 'ठीक गर्नु'),
    ('craft', 'शिल्प', 'skill', 'सीप', 'art', 'कला', 'trade', 'व्यापार', 'work', 'काम'),
    ('crash', 'दुर्घटना', 'collision', 'ठक्कर', 'accident', 'दुर्घटना', 'smash', 'ठोकिनु', 'safety', 'सुरक्षा'),
    ('create', 'सिर्जना गर्नु', 'make', 'बनाउनु', 'destroy', 'नष्ट गर्नु', 'produce', 'उत्पादन गर्नु', 'ruin', 'बिगार्नु'),
    ('credit', 'श्रेय', 'praise', 'प्रशंसा', 'blame', 'दोष', 'trust', 'विश्वास', 'debt', 'ऋण'),
    ('crime', 'अपराध', 'offence', 'कसुर', 'virtue', 'गुण', 'sin', 'पाप', 'law', 'कानुन'),
    ('crisis', 'सङ्कट', 'emergency', 'आपतकाल', 'stability', 'स्थिरता', 'danger', 'खतरा', 'safety', 'सुरक्षा'),
    ('critic', 'आलोचक', 'reviewer', 'समीक्षक', 'supporter', 'समर्थक', 'judge', 'न्यायाधीश', 'fan', 'प्रशंसक'),
    ('crop', 'बाली', 'harvest', 'फसल', 'yield', 'उपज', 'plant', 'बिरुवा', 'seed', 'बीउ'),
    ('cross', 'पार गर्नु', 'traverse', 'पार गर्नु', 'stay', 'बस्नु', 'pass', 'जानु', 'return', 'फर्कनु'),
    ('crowd', 'भिड', 'throng', 'हुल', 'group', 'समूह', 'assembly', 'सभा', 'individual', 'व्यक्ति'),
    ('cruel', 'क्रूर', 'merciless', 'निर्दयी', 'kind', 'दयालु', 'brutal', 'क्रूर', 'gentle', 'नम्र'),
    ('culture', 'संस्कृति', 'civilisation', 'सभ्यता', 'tradition', 'परम्परा', 'custom', 'चलन', 'nature', 'प्रकृति'),
    ('cure', 'उपचार', 'remedy', 'औषधि', 'disease', 'रोग', 'heal', 'निको पार्नु', 'harm', 'हानि'),
    ('curious', 'जिज्ञासु', 'inquisitive', 'जान्न उत्सुक', 'indifferent', 'उदासीन', 'eager', 'उत्सुक', 'bored', 'विरक्त'),
    ('current', 'हालको', 'present', 'वर्तमान', 'past', 'विगत', 'modern', 'आधुनिक', 'old', 'पुरानो'),
    ('custom', 'चलन', 'tradition', 'परम्परा', 'habit', 'बानी', 'practice', 'अभ्यास', 'innovation', 'नवीनता'),
    ('daily', 'दैनिक', 'everyday', 'प्रतिदिन', 'weekly', 'साप्ताहिक', 'regular', 'नियमित', 'rarely', 'विरलै'),
    ('damage', 'क्षति', 'harm', 'हानि', 'repair', 'मर्मत', 'injury', 'चोट', 'benefit', 'फाइदा'),
    ('dance', 'नाच', 'performance', 'प्रस्तुति', 'song', 'गीत', 'rhythm', 'लय', 'stillness', 'स्थिरता'),
    ('danger', 'खतरा', 'risk', 'जोखिम', 'safety', 'सुरक्षा', 'peril', 'खतरा', 'security', 'सुरक्षा'),
    ('dark', 'अँधेरो', 'dim', 'मधुरो', 'bright', 'उज्यालो', 'gloomy', 'अँध्यारो', 'light', 'प्रकाश'),
    ('data', 'तथ्याङ्क', 'information', 'जानकारी', 'facts', 'तथ्यहरू', 'figures', 'अङ्कहरू', 'opinion', 'विचार'),
    ('date', 'मिति', 'day', 'दिन', 'time', 'समय', 'appointment', 'भेटघाट', 'event', 'घटना'),
    ('daughter', 'छोरी', 'girl', 'केटी', 'son', 'छोरा', 'child', 'बालक', 'mother', 'आमा'),
    ('dawn', 'बिहान', 'sunrise', 'सूर्योदय', 'morning', 'बिहान', 'dusk', 'साँझ', 'night', 'रात'),
    ('dead', 'मृत', 'lifeless', 'निर्जीव', 'alive', 'जीवित', 'deceased', 'मृतक', 'living', 'बाँचिरहेको'),
    ('deal', 'सम्झौता', 'agreement', 'सहमति', 'bargain', 'सौदा', 'transaction', 'लेनदेन', 'dispute', 'विवाद'),
    ('dear', 'प्रिय', 'beloved', 'प्यारो', 'cheap', 'सस्तो', 'loved', 'मायालु', 'hated', 'घृणित'),
    ('death', 'मृत्यु', 'demise', 'निधन', 'birth', 'जन्म', 'end', 'अन्त्य', 'life', 'जीवन'),
    ('debate', 'वादविवाद', 'discussion', 'छलफल', 'argument', 'बहस', 'agreement', 'सहमति', 'talk', 'कुराकानी'),
    ('debt', 'ऋण', 'loan', 'सापटी', 'credit', 'उधारो', 'liability', 'दायित्व', 'asset', 'सम्पत्ति'),
    ('decade', 'दशक', 'ten years', 'दस वर्ष', 'year', 'वर्ष', 'period', 'अवधि', 'century', 'शताब्दी'),
    ('decide', 'निर्णय गर्नु', 'resolve', 'सङ्कल्प गर्नु', 'hesitate', 'हिचकिचाउनु', 'determine', 'निर्धारण गर्नु', 'delay', 'ढिलाइ गर्नु'),
    ('decision', 'निर्णय', 'verdict', 'फैसला', 'choice', 'छनोट', 'judgement', 'निर्णय', 'doubt', 'शङ्का'),
    ('declare', 'घोषणा गर्नु', 'announce', 'घोषणा गर्नु', 'conceal', 'लुकाउनु', 'proclaim', 'घोषणा गर्नु', 'hide', 'लुकाउनु'),
    ('decline', 'घट्नु', 'decrease', 'कम हुनु', 'increase', 'बढ्नु', 'fall', 'खस्नु', 'rise', 'उठ्नु'),
    ('deep', 'गहिरो', 'profound', 'गहन', 'shallow', 'उथलो', 'abyss', 'खाडल', 'surface', 'सतह'),
    ('defeat', 'हार', 'loss', 'पराजय', 'victory', 'विजय', 'failure', 'असफलता', 'triumph', 'विजय'),
    ('defend', 'रक्षा गर्नु', 'protect', 'जोगाउनु', 'attack', 'आक्रमण गर्नु', 'guard', 'रक्षा गर्नु', 'assault', 'हमला गर्नु'),
    ('define', 'परिभाषित गर्नु', 'explain', 'व्याख्या गर्नु', 'describe', 'वर्णन गर्नु', 'state', 'बताउनु', 'confuse', 'अलमल्याउनु'),
    ('degree', 'डिग्री', 'level', 'स्तर', 'grade', 'श्रेणी', 'extent', 'हद', 'unit', 'एकाइ'),
    ('delay', 'ढिलाइ', 'postponement', 'स्थगन', 'promptness', 'तत्परता', 'late', 'ढिलो', 'early', 'चाँडो'),
    ('delicate', 'नाजुक', 'fragile', 'भङ्गुर', 'strong', 'बलियो', 'fine', 'मसिनो', 'rough', 'खस्रो'),
    ('delight', 'खुसी', 'joy', 'आनन्द', 'sorrow', 'दुःख', 'pleasure', 'रमाइलो', 'grief', 'शोक'),
    ('deliver', 'पुर्‍याउनु', 'convey', 'पुर्‍याउनु', 'receive', 'प्राप्त गर्नु', 'send', 'पठाउनु', 'keep', 'राख्नु'),
    ('demand', 'माग', 'request', 'अनुरोध', 'supply', 'आपूर्ति', 'need', 'आवश्यकता', 'offer', 'प्रस्ताव'),
    ('democracy', 'लोकतन्त्र', 'republic', 'गणतन्त्र', 'freedom', 'स्वतन्त्रता', 'dictatorship', 'तानाशाही', 'rule', 'शासन'),
    ('depend', 'निर्भर हुनु', 'rely', 'भर पर्नु', 'independent', 'स्वतन्त्र', 'trust', 'विश्वास गर्नु', 'doubt', 'शङ्का गर्नु'),
    ('describe', 'वर्णन गर्नु', 'portray', 'चित्रण गर्नु', 'explain', 'व्याख्या गर्नु', 'depict', 'वर्णन गर्नु', 'hide', 'लुकाउनु'),
    ('desert', 'मरुभूमि', 'wasteland', 'उजाड', 'oasis', 'मरुद्यान', 'arid', 'सुक्खा', 'forest', 'जङ्गल'),
    ('design', 'डिजाइन', 'plan', 'योजना', 'pattern', 'ढाँचा', 'layout', 'विन्यास', 'build', 'निर्माण'),
    ('desire', 'इच्छा', 'wish', 'चाहना', 'longing', 'तृष्णा', 'aversion', 'घृणा', 'need', 'आवश्यकता'),
    ('desk', 'डेस्क', 'table', 'टेबल', 'counter', 'काउन्टर', 'workplace', 'कार्यस्थल', 'chair', 'कुर्सी'),
    ('despite', 'तथापि', 'although', 'यद्यपि', 'because', 'किनभने', 'notwithstanding', 'तथापि', 'therefore', 'त्यसैले'),
    ('detail', 'विवरण', 'particular', 'विशेष', 'summary', 'सारांश', 'fact', 'तथ्य', 'whole', 'पूरै'),
    ('develop', 'विकास गर्नु', 'grow', 'बढ्नु', 'decline', 'घट्नु', 'evolve', 'विकसित हुनु', 'shrink', 'खुम्चिनु'),
    ('device', 'यन्त्र', 'gadget', 'उपकरण', 'tool', 'औजार', 'machine', 'मेसिन', 'instrument', 'यन्त्र'),
    ('devote', 'समर्पित गर्नु', 'dedicate', 'अर्पण गर्नु', 'neglect', 'उपेक्षा गर्नु', 'commit', 'प्रतिबद्ध हुनु', 'abandon', 'त्याग्नु'),
    ('dialogue', 'संवाद', 'conversation', 'कुराकानी', 'monologue', 'एकल संवाद', 'discussion', 'छलफल', 'silence', 'मौनता'),
    ('diary', 'डायरी', 'journal', 'दैनिकी', 'notebook', 'नोटबुक', 'record', 'अभिलेख', 'book', 'किताब'),
    ('differ', 'फरक हुनु', 'vary', 'भिन्न हुनु', 'agree', 'सहमत हुनु', 'contrast', 'तुलना गर्नु', 'match', 'मेल खानु'),
    ('difficult', 'कठिन', 'hard', 'गाह्रो', 'easy', 'सजिलो', 'tough', 'कठोर', 'simple', 'सरल'),
    ('dig', 'खन्नु', 'excavate', 'उत्खनन गर्नु', 'bury', 'गाड्नु', 'shovel', 'बेल्चा', 'fill', 'भर्नु'),
    ('dinner', 'बेलुकाको खाना', 'supper', 'रातिको खाना', 'lunch', 'दिउँसोको खाना', 'meal', 'खाना', 'breakfast', 'बिहानको खाना'),
    ('direct', 'प्रत्यक्ष', 'straight', 'सिधा', 'indirect', 'अप्रत्यक्ष', 'immediate', 'तत्काल', 'roundabout', 'घुमाउरो'),
    ('direction', 'दिशा', 'way', 'बाटो', 'course', 'मार्ग', 'route', 'बाटो', 'guidance', 'मार्गदर्शन'),
    ('dirt', 'फोहोर', 'soil', 'माटो', 'mud', 'हिलो', 'cleanliness', 'सफाइ', 'dust', 'धुलो'),
    ('discover', 'पत्ता लगाउनु', 'find', 'फेला पार्नु', 'hide', 'लुकाउनु', 'uncover', 'खोज्नु', 'lose', 'गुमाउनु'),
    ('discuss', 'छलफल गर्नु', 'debate', 'वादविवाद गर्नु', 'talk', 'कुराकानी गर्नु', 'argue', 'बहस गर्नु', 'ignore', 'बेवास्ता गर्नु'),
    ('disease', 'रोग', 'illness', 'बिरामी', 'health', 'स्वास्थ्य', 'ailment', 'रोग', 'cure', 'उपचार'),
    ('display', 'प्रदर्शन', 'exhibit', 'प्रदर्शनी', 'show', 'देखाउनु', 'hide', 'लुकाउनु', 'conceal', 'लुकाउनु'),
    ('distance', 'दूरी', 'length', 'लम्बाइ', 'gap', 'अन्तर', 'nearness', 'नजिक', 'space', 'ठाउँ'),
    ('distant', 'टाढा', 'far', 'दूर', 'near', 'नजिक', 'remote', 'दुर्गम', 'close', 'नजिक'),
    ('divide', 'भाग गर्नु', 'split', 'विभाजन गर्नु', 'unite', 'एकताबद्ध गर्नु', 'separate', 'छुट्याउनु', 'join', 'जोड्नु'),
    ('doctor', 'डाक्टर', 'physician', 'चिकित्सक', 'patient', 'बिरामी', 'surgeon', 'शल्यक्रिया विशेषज्ञ', 'nurse', 'नर्स'),
    ('document', 'कागजात', 'record', 'अभिलेख', 'paper', 'कागज', 'file', 'फाइल', 'certificate', 'प्रमाणपत्र'),
    ('dollar', 'डलर', 'currency', 'मुद्रा', 'rupee', 'रुपियाँ', 'money', 'पैसा', 'coin', 'सिक्का'),
    ('door', 'ढोका', 'gate', 'गेट', 'entrance', 'प्रवेशद्वार', 'window', 'झ्याल', 'wall', 'पर्खाल'),
    ('double', 'दोब्बर', 'twice', 'दुई गुणा', 'single', 'एकल', 'duplicate', 'नक्कल', 'half', 'आधा'),
    ('doubt', 'शङ्का', 'suspicion', 'सन्देह', 'certainty', 'निश्चितता', 'uncertainty', 'अनिश्चितता', 'trust', 'विश्वास'),
    ('down', 'तल', 'below', 'मुनि', 'up', 'माथि', 'under', 'तल', 'above', 'माथि'),
    ('dozen', 'दर्जन', 'twelve', 'बाह्र', 'pair', 'जोडी', 'hundred', 'सय', 'unit', 'एकाइ'),
    ('draft', 'मस्यौदा', 'outline', 'रूपरेखा', 'plan', 'योजना', 'final', 'अन्तिम', 'sketch', 'खाका'),
    ('draw', 'कोर्नु', 'sketch', 'खाका कोर्नु', 'erase', 'मेट्नु', 'paint', 'रङ्ग गर्नु', 'write', 'लेख्नु'),
    ('dream', 'सपना', 'vision', 'दृष्टि', 'nightmare', 'दुःस्वप्न', 'fantasy', 'कल्पना', 'reality', 'वास्तविकता'),
    ('dress', 'पोशाक', 'attire', 'वस्त्र', 'clothes', 'लुगा', 'garment', 'पोशाक', 'uniform', 'पोशाक'),
    ('drink', 'पिउनु', 'sip', 'चुस्की लिनु', 'eat', 'खानु', 'swallow', 'निल्नु', 'taste', 'स्वाद लिनु'),
    ('drive', 'चलाउनु', 'operate', 'सञ्चालन गर्नु', 'steer', 'हाक्नु', 'ride', 'चढ्नु', 'walk', 'हिँड्नु'),
    ('drop', 'थोपा', 'bead', 'थोपा', 'fall', 'खस्नु', 'rise', 'उठ्नु', 'trickle', 'टपक्नु'),
    ('drum', 'ढोल', 'instrument', 'वाद्ययन्त्र', 'beat', 'ताल', 'music', 'सङ्गीत', 'flute', 'बाँसुरी'),
    ('dry', 'सुक्खा', 'arid', 'सुक्खा', 'wet', 'भिजेको', 'parched', 'सुकेको', 'moist', 'चिसो'),
    ('during', 'अवधिमा', 'while', 'जब', 'before', 'अघि', 'after', 'पछि', 'throughout', 'भरि'),
    ('duty', 'कर्तव्य', 'obligation', 'दायित्व', 'responsibility', 'जिम्मेवारी', 'right', 'अधिकार', 'freedom', 'स्वतन्त्रता'),
    ('each', 'प्रत्येक', 'every', 'हरेक', 'all', 'सबै', 'any', 'कुनै', 'none', 'कुनै पनि होइन'),
    ('eager', 'उत्सुक', 'keen', 'इच्छुक', 'reluctant', 'अनिच्छुक', 'enthusiastic', 'उत्साही', 'indifferent', 'उदासीन'),
    ('early', 'चाँडो', 'soon', 'चाँडै', 'late', 'ढिलो', 'prompt', 'तत्काल', 'delayed', 'ढिलाइ भएको'),
    ('earn', 'कमाउनु', 'gain', 'प्राप्त गर्नु', 'lose', 'गुमाउनु', 'acquire', 'प्राप्त गर्नु', 'spend', 'खर्च गर्नु'),
    ('earth', 'पृथ्वी', 'world', 'संसार', 'globe', 'गोलार्ध', 'soil', 'माटो', 'sky', 'आकाश'),
    ('east', 'पूर्व', 'orient', 'पूर्व', 'west', 'पश्चिम', 'north', 'उत्तर', 'south', 'दक्षिण'),
    ('easy', 'सजिलो', 'simple', 'सरल', 'difficult', 'कठिन', 'effortless', 'सहज', 'hard', 'गाह्रो'),
    ('eat', 'खानु', 'consume', 'उपभोग गर्नु', 'dine', 'खाना खानु', 'chew', 'चपाउनु', 'fast', 'व्रत बस्नु'),
    ('economy', 'अर्थतन्त्र', 'finance', 'वित्त', 'market', 'बजार', 'trade', 'व्यापार', 'wealth', 'धन'),
    ('edge', 'किनार', 'border', 'सीमा', 'margin', 'किनार', 'centre', 'केन्द्र', 'rim', 'किनार'),
    ('edit', 'सम्पादन गर्नु', 'revise', 'परिमार्जन गर्नु', 'write', 'लेख्नु', 'correct', 'सच्याउनु', 'publish', 'प्रकाशन गर्नु'),
    ('educate', 'शिक्षा दिनु', 'teach', 'पढाउनु', 'instruct', 'निर्देशन दिनु', 'train', 'तालिम दिनु', 'ignore', 'बेवास्ता गर्नु'),
    ('effect', 'प्रभाव', 'result', 'परिणाम', 'cause', 'कारण', 'impact', 'असर', 'outcome', 'नतिजा'),
    ('effort', 'प्रयास', 'attempt', 'कोसिस', 'endeavour', 'प्रयत्न', 'laziness', 'आलस्य', 'struggle', 'सङ्घर्ष'),
    ('either', 'कुनै एक', 'one', 'एक', 'neither', 'कुनै पनि होइन', 'both', 'दुवै', 'any', 'कुनै'),
    ('elder', 'जेठो', 'senior', 'वरिष्ठ', 'younger', 'कान्छो', 'older', 'बुढो', 'junior', 'कनिष्ठ'),
    ('elect', 'निर्वाचित गर्नु', 'choose', 'छान्नु', 'vote', 'मतदान गर्नु', 'appoint', 'नियुक्त गर्नु', 'reject', 'अस्वीकार गर्नु'),
    ('elegant', 'सुरुचिपूर्ण', 'graceful', 'सुन्दर', 'awkward', 'अप्ठ्यारो', 'stylish', 'फेसनेबल', 'plain', 'साधारण'),
    ('element', 'तत्त्व', 'component', 'अवयव', 'part', 'भाग', 'factor', 'कारक', 'whole', 'पूरै'),
    ('else', 'अन्यथा', 'otherwise', 'नत्र', 'also', 'पनि', 'besides', 'अतिरिक्त', 'moreover', 'यसबाहेक'),
    ('embrace', 'अँगाल्नु', 'hug', 'अँगालो हाल्नु', 'reject', 'अस्वीकार गर्नु', 'accept', 'स्वीकार्नु', 'push', 'धकेल्नु'),
    ('emerge', 'निस्कनु', 'appear', 'देखिनु', 'disappear', 'हराउनु', 'arise', 'उठ्नु', 'vanish', 'गायब हुनु'),
    ('emotion', 'भावना', 'feeling', 'अनुभूति', 'sentiment', 'भाव', 'passion', 'जोश', 'reason', 'तर्क'),
    ('empire', 'साम्राज्य', 'kingdom', 'राज्य', 'realm', 'राज्य', 'domain', 'क्षेत्र', 'republic', 'गणतन्त्र'),
    ('employ', 'रोजगारी दिनु', 'hire', 'भर्ना गर्नु', 'dismiss', 'बर्खास्त गर्नु', 'engage', 'संलग्न गर्नु', 'fire', 'निकाल्नु'),
    ('empty', 'खाली', 'vacant', 'रिक्त', 'full', 'भरिएको', 'blank', 'खाली', 'occupied', 'भरिएको'),
    ('enable', 'सक्षम बनाउनु', 'allow', 'अनुमति दिनु', 'prevent', 'रोक्नु', 'empower', 'सशक्त बनाउनु', 'disable', 'असक्षम बनाउनु'),
    ('encourage', 'प्रोत्साहन दिनु', 'inspire', 'प्रेरणा दिनु', 'discourage', 'निरुत्साहित गर्नु', 'motivate', 'उत्प्रेरित गर्नु', 'deter', 'रोक्नु'),
    ('end', 'अन्त्य', 'finish', 'समाप्ति', 'beginning', 'सुरुवात', 'conclusion', 'निष्कर्ष', 'start', 'सुरु'),
    ('enemy', 'शत्रु', 'foe', 'विरोधी', 'friend', 'मित्र', 'adversary', 'प्रतिद्वन्द्वी', 'ally', 'सहयोगी'),
    ('energy', 'ऊर्जा', 'power', 'शक्ति', 'force', 'बल', 'vitality', 'जीवनशक्ति', 'weakness', 'कमजोरी'),
    ('engage', 'संलग्न हुनु', 'involve', 'सामेल हुनु', 'disengage', 'अलग हुनु', 'participate', 'सहभागी हुनु', 'withdraw', 'फिर्ता लिनु'),
    ('engine', 'इन्जिन', 'motor', 'मोटर', 'machine', 'मेसिन', 'mechanism', 'यन्त्र', 'wheel', 'पाङ्ग्रा'),
    ('enjoy', 'रमाइलो गर्नु', 'relish', 'आनन्द लिनु', 'dislike', 'मन नपराउनु', 'delight', 'खुसी हुनु', 'suffer', 'पीडा भोग्नु'),
    ('enough', 'पर्याप्त', 'sufficient', 'पर्याप्त', 'insufficient', 'अपर्याप्त', 'ample', 'प्रशस्त', 'scarce', 'दुर्लभ'),
    ('ensure', 'सुनिश्चित गर्नु', 'guarantee', 'ग्यारेन्टी दिनु', 'assure', 'आश्वासन दिनु', 'risk', 'जोखिम', 'doubt', 'शङ्का गर्नु'),
    ('enter', 'प्रवेश गर्नु', 'arrive', 'आइपुग्नु', 'exit', 'निस्कनु', 'join', 'सामेल हुनु', 'leave', 'जानु'),
    ('entire', 'सम्पूर्ण', 'whole', 'पूरै', 'total', 'कुल', 'partial', 'आंशिक', 'complete', 'पूर्ण'),
    ('entrance', 'प्रवेशद्वार', 'entry', 'प्रवेश', 'exit', 'निकास', 'gate', 'गेट', 'door', 'ढोका'),
    ('entry', 'प्रविष्टि', 'record', 'अभिलेख', 'admission', 'प्रवेश', 'exit', 'निकास', 'note', 'टिप्पणी'),
    ('equal', 'बराबर', 'same', 'उस्तै', 'unequal', 'असमान', 'identical', 'एउटै', 'different', 'फरक'),
    ('error', 'त्रुटि', 'mistake', 'गल्ती', 'accuracy', 'शुद्धता', 'fault', 'दोष', 'correctness', 'सहीपन'),
    ('escape', 'भाग्नु', 'flee', 'भाग्नु', 'capture', 'समात्नु', 'evade', 'टार्नु', 'remain', 'बस्नु'),
    ('especially', 'विशेष गरी', 'particularly', 'विशेष रूपमा', 'generally', 'सामान्यतया', 'notably', 'उल्लेखनीय रूपमा', 'rarely', 'विरलै'),
    ('essay', 'निबन्ध', 'composition', 'रचना', 'article', 'लेख', 'paper', 'पत्र', 'story', 'कथा'),
    ('essential', 'आवश्यक', 'necessary', 'जरुरी', 'optional', 'वैकल्पिक', 'vital', 'अत्यावश्यक', 'unneeded', 'अनावश्यक'),
    ('establish', 'स्थापना गर्नु', 'found', 'स्थापना गर्नु', 'abolish', 'उन्मूलन गर्नु', 'create', 'सिर्जना गर्नु', 'destroy', 'नष्ट गर्नु'),
    ('estimate', 'अनुमान', 'guess', 'अनुमान', 'calculation', 'हिसाब', 'assessment', 'मूल्याङ्कन', 'fact', 'तथ्य'),
    ('even', 'सम', 'level', 'समतल', 'odd', 'विजोर', 'flat', 'समथर', 'uneven', 'असमतल'),
    ('evening', 'साँझ', 'dusk', 'साँझ', 'morning', 'बिहान', 'night', 'रात', 'afternoon', 'दिउँसो'),
    ('event', 'घटना', 'incident', 'घटना', 'occasion', 'अवसर', 'happening', 'घटना', 'accident', 'दुर्घटना'),
    ('every', 'हरेक', 'each', 'प्रत्येक', 'all', 'सबै', 'any', 'कुनै', 'none', 'कुनै पनि होइन'),
    ('evidence', 'प्रमाण', 'proof', 'प्रमाण', 'testimony', 'गवाही', 'clue', 'सुराग', 'doubt', 'शङ्का'),
    ('exact', 'ठ्याक्कै', 'precise', 'सटीक', 'approximate', 'लगभग', 'accurate', 'सही', 'vague', 'अस्पष्ट'),
    ('examine', 'जाँच गर्नु', 'inspect', 'निरीक्षण गर्नु', 'test', 'परीक्षण गर्नु', 'assess', 'मूल्याङ्कन गर्नु', 'ignore', 'बेवास्ता गर्नु'),
    ('example', 'उदाहरण', 'instance', 'उदाहरण', 'sample', 'नमुना', 'illustration', 'उदाहरण', 'model', 'मोडेल'),
    ('excellent', 'उत्कृष्ट', 'superb', 'उत्तम', 'poor', 'खराब', 'outstanding', 'असाधारण', 'mediocre', 'मध्यम'),
    ('except', 'बाहेक', 'excluding', 'बाहेक', 'including', 'सहित', 'besides', 'अतिरिक्त', 'apart', 'छुट्टै'),
    ('exchange', 'आदानप्रदान', 'swap', 'साट्नु', 'trade', 'व्यापार', 'barter', 'वस्तु विनिमय', 'keep', 'राख्नु'),
    ('excuse', 'बहाना', 'apology', 'माफी', 'reason', 'कारण', 'justification', 'औचित्य', 'blame', 'दोष'),
    ('exercise', 'व्यायाम', 'workout', 'कसरत', 'training', 'तालिम', 'rest', 'आराम', 'practice', 'अभ्यास'),
    ('exist', 'अस्तित्वमा हुनु', 'live', 'बाँच्नु', 'survive', 'बाँच्नु', 'vanish', 'गायब हुनु', 'occur', 'हुनु'),
    ('expand', 'विस्तार गर्नु', 'enlarge', 'ठूलो बनाउनु', 'contract', 'सङ्कुचित हुनु', 'grow', 'बढ्नु', 'shrink', 'खुम्चिनु'),
    ('expect', 'अपेक्षा गर्नु', 'anticipate', 'पूर्वानुमान गर्नु', 'await', 'पर्खनु', 'hope', 'आशा गर्नु', 'doubt', 'शङ्का गर्नु'),
    ('expense', 'खर्च', 'cost', 'लागत', 'expenditure', 'व्यय', 'income', 'आम्दानी', 'saving', 'बचत'),
    ('explain', 'व्याख्या गर्नु', 'clarify', 'स्पष्ट पार्नु', 'describe', 'वर्णन गर्नु', 'illustrate', 'उदाहरण दिनु', 'confuse', 'अलमल्याउनु'),
    ('explore', 'अन्वेषण गर्नु', 'investigate', 'अनुसन्धान गर्नु', 'discover', 'पत्ता लगाउनु', 'search', 'खोज्नु', 'ignore', 'बेवास्ता गर्नु'),
    ('express', 'व्यक्त गर्नु', 'convey', 'पुर्‍याउनु', 'state', 'बताउनु', 'voice', 'आवाज', 'hide', 'लुकाउनु'),
    ('extend', 'विस्तार गर्नु', 'lengthen', 'लम्ब्याउनु', 'shorten', 'छोटो पार्नु', 'prolong', 'लम्ब्याउनु', 'reduce', 'घटाउनु'),
    ('extra', 'थप', 'additional', 'अतिरिक्त', 'more', 'बढी', 'less', 'कम', 'spare', 'थप'),
    ('face', 'अनुहार', 'visage', 'मुख', 'countenance', 'अनुहार', 'expression', 'अभिव्यक्ति', 'back', 'पछाडि'),
    ('fact', 'तथ्य', 'truth', 'सत्य', 'reality', 'वास्तविकता', 'fiction', 'कल्पना', 'evidence', 'प्रमाण'),
    ('factor', 'कारक', 'element', 'तत्त्व', 'cause', 'कारण', 'component', 'अवयव', 'result', 'नतिजा'),
    ('fail', 'असफल हुनु', 'flunk', 'फेल हुनु', 'succeed', 'सफल हुनु', 'collapse', 'ढल्नु', 'triumph', 'विजय'),
    ('fair', 'निष्पक्ष', 'just', 'न्यायपूर्ण', 'unfair', 'अन्यायपूर्ण', 'impartial', 'तटस्थ', 'biased', 'पक्षपाती'),
    ('faith', 'विश्वास', 'belief', 'आस्था', 'trust', 'भरोसा', 'doubt', 'शङ्का', 'devotion', 'भक्ति'),
    ('fall', 'खस्नु', 'drop', 'झर्नु', 'rise', 'उठ्नु', 'tumble', 'लड्नु', 'climb', 'चढ्नु'),
    ('false', 'झुटो', 'untrue', 'असत्य', 'true', 'साँचो', 'fake', 'नक्कली', 'genuine', 'वास्तविक'),
    ('familiar', 'परिचित', 'known', 'चिनिएको', 'strange', 'अनौठो', 'acquainted', 'परिचित', 'unknown', 'अज्ञात'),
    ('family', 'परिवार', 'household', 'घरपरिवार', 'kin', 'नाता', 'relatives', 'आफन्तहरू', 'individual', 'व्यक्ति'),
    ('famous', 'प्रसिद्ध', 'renowned', 'प्रख्यात', 'unknown', 'अज्ञात', 'celebrated', 'प्रसिद्ध', 'obscure', 'अस्पष्ट'),
    ('far', 'टाढा', 'distant', 'दूर', 'near', 'नजिक', 'remote', 'दुर्गम', 'close', 'नजिक'),
    ('farm', 'खेत', 'field', 'खेतबारी', 'land', 'जमिन', 'estate', 'जागिर', 'garden', 'बगैँचा'),
    ('fast', 'छिटो', 'quick', 'द्रुत', 'slow', 'ढिलो', 'rapid', 'तीव्र', 'swift', 'छिटो'),
    ('fate', 'भाग्य', 'destiny', 'नियति', 'fortune', 'भाग्य', 'luck', 'भाग्य', 'choice', 'छनोट'),
    ('father', 'बुबा', 'dad', 'बुबा', 'parent', 'अभिभावक', 'mother', 'आमा', 'son', 'छोरा'),
    ('fear', 'डर', 'fright', 'त्रास', 'courage', 'साहस', 'terror', 'आतङ्क', 'bravery', 'बहादुरी'),
    ('feast', 'भोज', 'banquet', 'भोज', 'celebration', 'उत्सव', 'meal', 'खाना', 'fast', 'व्रत'),
    ('feature', 'विशेषता', 'characteristic', 'लक्षण', 'trait', 'गुण', 'aspect', 'पक्ष', 'detail', 'विवरण'),
    ('fee', 'शुल्क', 'charge', 'शुल्क', 'cost', 'लागत', 'payment', 'भुक्तानी', 'fine', 'जरिवाना'),
    ('feel', 'महसुस गर्नु', 'sense', 'अनुभव गर्नु', 'touch', 'छुनु', 'perceive', 'बुझ्नु', 'ignore', 'बेवास्ता गर्नु'),
    ('female', 'महिला', 'woman', 'स्त्री', 'male', 'पुरुष', 'girl', 'केटी', 'lady', 'महिला'),
    ('festival', 'पर्व', 'celebration', 'उत्सव', 'feast', 'भोज', 'holiday', 'बिदा', 'ceremony', 'समारोह'),
    ('fetch', 'ल्याउनु', 'bring', 'ल्याउनु', 'carry', 'बोक्नु', 'retrieve', 'ल्याउनु', 'send', 'पठाउनु'),
    ('few', 'थोरै', 'some', 'केही', 'many', 'धेरै', 'several', 'धेरै', 'none', 'कुनै पनि होइन'),
    ('field', 'खेत', 'ground', 'मैदान', 'area', 'क्षेत्र', 'plot', 'प्लट', 'court', 'अदालत'),
    ('fierce', 'उग्र', 'ferocious', 'क्रूर', 'gentle', 'नम्र', 'violent', 'हिंस्रक', 'calm', 'शान्त'),
    ('fight', 'लडाइँ', 'battle', 'युद्ध', 'combat', 'सङ्घर्ष', 'peace', 'शान्ति', 'struggle', 'सङ्घर्ष'),
    ('figure', 'आकृति', 'shape', 'आकार', 'form', 'रूप', 'number', 'सङ्ख्या', 'digit', 'अङ्क'),
    ('fill', 'भर्नु', 'occupy', 'ओगट्नु', 'empty', 'खाली गर्नु', 'load', 'बोझ्नु', 'pour', 'खन्याउनु'),
    ('film', 'फिल्म', 'movie', 'चलचित्र', 'cinema', 'सिनेमा', 'picture', 'तस्बिर', 'video', 'भिडियो'),
    ('final', 'अन्तिम', 'last', 'अन्तिम', 'first', 'पहिलो', 'ultimate', 'अन्तिम', 'initial', 'प्रारम्भिक'),
    ('find', 'फेला पार्नु', 'discover', 'पत्ता लगाउनु', 'lose', 'गुमाउनु', 'locate', 'पत्ता लगाउनु', 'miss', 'छुटाउनु'),
    ('fine', 'जरिवाना', 'penalty', 'सजाय', 'fee', 'शुल्क', 'punishment', 'दण्ड', 'reward', 'पुरस्कार'),
    ('finger', 'औँला', 'digit', 'औँला', 'thumb', 'बूढी औँला', 'toe', 'खुट्टाको औँला', 'hand', 'हात'),
    ('finish', 'समाप्त गर्नु', 'complete', 'पूरा गर्नु', 'begin', 'सुरु गर्नु', 'end', 'अन्त्य गर्नु', 'start', 'थाल्नु'),
    ('fire', 'आगो', 'flame', 'ज्वाला', 'blaze', 'आगो', 'water', 'पानी', 'smoke', 'धुवाँ'),
    ('firm', 'दृढ', 'solid', 'ठोस', 'weak', 'कमजोर', 'stable', 'स्थिर', 'loose', 'खुकुलो'),
    ('first', 'पहिलो', 'initial', 'प्रारम्भिक', 'last', 'अन्तिम', 'primary', 'प्राथमिक', 'final', 'अन्तिम'),
    ('fish', 'माछा', 'aquatic', 'जलीय', 'seafood', 'समुद्री खाना', 'catch', 'समात्नु', 'bird', 'चरा'),
    ('fit', 'उपयुक्त', 'suitable', 'योग्य', 'unfit', 'अयोग्य', 'appropriate', 'उपयुक्त', 'unsuitable', 'अनुपयुक्त'),
    ('fix', 'ठीक गर्नु', 'repair', 'मर्मत गर्नु', 'break', 'भाँच्नु', 'mend', 'मर्मत गर्नु', 'damage', 'क्षति पुर्‍याउनु'),
    ('flag', 'झण्डा', 'banner', 'झण्डा', 'ensign', 'निशान', 'standard', 'मानक', 'emblem', 'प्रतीक'),
    ('flame', 'ज्वाला', 'fire', 'आगो', 'blaze', 'आगो', 'spark', 'झिल्को', 'ash', 'खरानी'),
    ('flat', 'समथर', 'level', 'समतल', 'hilly', 'पहाडी', 'even', 'सम', 'rough', 'खस्रो'),
    ('flight', 'उडान', 'journey', 'यात्रा', 'voyage', 'यात्रा', 'landing', 'अवतरण', 'departure', 'प्रस्थान'),
    ('float', 'तैरिनु', 'drift', 'बहनु', 'sink', 'डुब्नु', 'swim', 'पौडिनु', 'drown', 'डुब्नु'),
    ('flood', 'बाढी', 'deluge', 'प्रलय', 'inundation', 'डुबान', 'drought', 'खडेरी', 'rain', 'वर्षा'),
    ('floor', 'भुइँ', 'ground', 'जमिन', 'storey', 'तल्ला', 'ceiling', 'छत', 'level', 'स्तर'),
    ('flour', 'पिठो', 'meal', 'पिठो', 'powder', 'धुलो', 'grain', 'अन्न', 'dough', 'आटा'),
    ('flow', 'बग्नु', 'stream', 'खोल्सा', 'current', 'धारा', 'stagnate', 'थामिनु', 'run', 'दौड्नु'),
    ('flower', 'फूल', 'bloom', 'फुल्नु', 'blossom', 'फूल', 'petal', 'पंखुडी', 'plant', 'बिरुवा'),
    ('fluent', 'प्रवाहपूर्ण', 'eloquent', 'वाक्पटु', 'hesitant', 'हिचकिचाउने', 'smooth', 'चिल्लो', 'broken', 'टुटेको'),
    ('fly', 'उड्नु', 'soar', 'उड्नु', 'land', 'अवतरण गर्नु', 'glide', 'तैरिनु', 'walk', 'हिँड्नु'),
    ('focus', 'ध्यान', 'concentration', 'एकाग्रता', 'attention', 'ध्यान', 'distraction', 'विचलन', 'centre', 'केन्द्र'),
    ('fog', 'कुहिरो', 'mist', 'कुहिरो', 'haze', 'धुम्म', 'clear', 'सफा', 'cloud', 'बादल'),
    ('fold', 'फोल्ड गर्नु', 'bend', 'मोड्नु', 'unfold', 'खोल्नु', 'crease', 'चाउरी', 'wrap', 'बेर्नु'),
    ('follow', 'पछ्याउनु', 'pursue', 'पछ्याउनु', 'lead', 'नेतृत्व गर्नु', 'obey', 'आज्ञा मान्नु', 'precede', 'अगाडि हुनु'),
    ('food', 'खाना', 'meal', 'भोजन', 'diet', 'आहार', 'nutrition', 'पोषण', 'hunger', 'भोक'),
    ('fool', 'मूर्ख', 'idiot', 'मूर्ख', 'wise', 'बुद्धिमान्', 'dolt', 'मूर्ख', 'genius', 'प्रतिभा'),
    ('foot', 'खुट्टा', 'feet', 'खुट्टाहरू', 'leg', 'खुट्टा', 'toe', 'खुट्टाको औँला', 'hand', 'हात'),
    ('forbid', 'निषेध गर्नु', 'prohibit', 'प्रतिबन्ध लगाउनु', 'allow', 'अनुमति दिनु', 'ban', 'प्रतिबन्ध', 'permit', 'अनुमति दिनु'),
    ('force', 'बल', 'power', 'शक्ति', 'strength', 'शक्ति', 'weakness', 'कमजोरी', 'energy', 'ऊर्जा'),
    ('foreign', 'विदेशी', 'alien', 'विदेशी', 'native', 'स्वदेशी', 'overseas', 'विदेश', 'domestic', 'स्वदेशी'),
    ('forest', 'जङ्गल', 'woods', 'वन', 'jungle', 'जङ्गल', 'grove', 'कुञ्ज', 'desert', 'मरुभूमि'),
    ('forget', 'बिर्सनु', 'neglect', 'उपेक्षा गर्नु', 'remember', 'सम्झनु', 'recall', 'स्मरण गर्नु', 'retain', 'राख्नु'),
    ('form', 'फारम', 'shape', 'आकार', 'structure', 'संरचना', 'format', 'ढाँचा', 'blank', 'खाली'),
    ('formal', 'औपचारिक', 'official', 'आधिकारिक', 'informal', 'अनौपचारिक', 'ceremonial', 'औपचारिक', 'casual', 'साधारण'),
    ('former', 'पूर्व', 'previous', 'अघिल्लो', 'latter', 'पछिल्लो', 'earlier', 'पहिलेको', 'current', 'हालको'),
    ('fortune', 'भाग्य', 'luck', 'भाग्य', 'wealth', 'धन', 'destiny', 'नियति', 'misfortune', 'दुर्भाग्य'),
    ('forward', 'अगाडि', 'ahead', 'अगाडि', 'backward', 'पछाडि', 'onward', 'अगाडि', 'behind', 'पछाडि'),
    ('found', 'स्थापना गर्नु', 'establish', 'स्थापना गर्नु', 'create', 'सिर्जना गर्नु', 'discover', 'पत्ता लगाउनु', 'abolish', 'उन्मूलन गर्नु'),
    ('free', 'निःशुल्क', 'gratis', 'निःशुल्क', 'paid', 'भुक्तानी गरिएको', 'liberated', 'मुक्त', 'bound', 'बाँधिएको'),
    ('freedom', 'स्वतन्त्रता', 'liberty', 'स्वाधीनता', 'slavery', 'दासत्व', 'independence', 'स्वतन्त्रता', 'captivity', 'कैद'),
    ('frequent', 'बारम्बार', 'often', 'प्रायः', 'rare', 'दुर्लभ', 'regular', 'नियमित', 'occasional', 'कहिलेकाहीँ'),
    ('fresh', 'ताजा', 'new', 'नयाँ', 'stale', 'बासी', 'recent', 'हालैको', 'old', 'पुरानो'),
    ('friend', 'साथी', 'companion', 'सहयात्री', 'enemy', 'शत्रु', 'mate', 'साथी', 'foe', 'विरोधी'),
    ('front', 'अगाडि', 'fore', 'अगाडि', 'back', 'पछाडि', 'face', 'अनुहार', 'rear', 'पछाडि'),
    ('fruit', 'फल', 'produce', 'उपज', 'berry', 'बेरी', 'vegetable', 'तरकारी', 'seed', 'बीउ'),
    ('full', 'भरिएको', 'complete', 'पूर्ण', 'empty', 'खाली', 'packed', 'भरिएको', 'vacant', 'रिक्त'),
    ('fun', 'रमाइलो', 'amusement', 'मनोरञ्जन', 'enjoyment', 'आनन्द', 'boredom', 'विरक्ति', 'pleasure', 'खुसी'),
    ('function', 'कार्य', 'role', 'भूमिका', 'purpose', 'उद्देश्य', 'duty', 'कर्तव्य', 'operation', 'सञ्चालन'),
    ('fund', 'कोष', 'finance', 'वित्त', 'money', 'पैसा', 'capital', 'पूँजी', 'budget', 'बजेट'),
    ('future', 'भविष्य', 'forthcoming', 'आगामी', 'past', 'विगत', 'present', 'वर्तमान', 'destiny', 'नियति'),
]
seen1 = {w[0] for w in WORDS1} | {w[0] for w in WORDS2}
valid = []
for w in WORDS5:
    if w[0] in seen1:
        print('SKIP dup word (list1/2):', w[0], file=sys.stderr); continue
    en, ne, syn, syn_ne, ant, ant_ne, rel, rel_ne, unrel, unrel_ne = w
    ok_en = len({syn.lower(), ant.lower(), rel.lower(), unrel.lower()}) == 4
    ok_ne = len({syn_ne, ant_ne, rel_ne, unrel_ne}) == 4
    if ok_en and ok_ne:
        valid.append(w)
    else:
        print('SKIP row (dup option words/glosses):', en, file=sys.stderr)
print(f'Valid words: {len(valid)}/{len(WORDS5)}', file=sys.stderr)

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
nv = emv.write('expansion-r10-vocab5.json')
print('VOCAB5 TOTAL:', nv, 'rejected:', len(emv.rejected))

# ================= MATHS 9 =================
emm = Emitter(bank, 'R10-M9')
def qm(topic, diff, marks, q, qn, opts, optn, ans, exp, expn):
    emm.emit(EX, 'Maths & Numerical', topic, diff, marks, q, qn, opts, optn, ans, exp, expn)
def num_opts(ans, lo, hi, step=1):
    s = {ans}
    while len(s) < 4:
        v = rng.randrange(lo, hi+1, step)
        if v != ans and v >= 0: s.add(v)
    o = list(s); rng.shuffle(o)
    return o, o.index(ans)

# % with 2.5 / 7.5 of 3-digit numbers
for _ in range(100):
    n = rng.choice([120, 240, 360, 480, 600, 720, 840, 960, 200, 400, 800, 1000, 1200, 1600, 2000])
    pct = rng.choice([2.5, 7.5, 12.5, 37.5])
    ans = n * pct / 100
    if ans != int(ans): continue
    ans = int(ans)
    o, ai = num_opts(ans, max(1, ans-20), ans+20, 5)
    qm('Percentages', 'medium', 1,
        f"What is {pct}% of {n}?", f"{n} को {pct}% कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"{pct}% of {n} = {n} x {pct}/100 = {ans}.",
        f"{n} को {pct}% = {n} × {pct}/१०० = {ans} हो।")

# average of consecutive range a..b
for _ in range(100):
    a = rng.randrange(5, 60); b = a + rng.choice([4, 6, 8, 10, 14, 19, 20, 24])
    ans = (a + b) / 2
    if ans != int(ans): continue
    ans = int(ans)
    o, ai = num_opts(ans, max(1, ans-15), ans+15, 1)
    qm('Averages', 'medium', 1,
        f"What is the average of all numbers from {a} to {b}?", f"{a} देखि {b} सम्मका सबै सङ्ख्याहरूको औसत कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Average of consecutive numbers from {a} to {b} = ({a} + {b})/2 = {ans}.",
        f"{a} देखि {b} सम्मका क्रमागत सङ्ख्याको औसत = ({a} + {b})/२ = {ans} हो।")

# 4-part ratio division
for _ in range(80):
    r = [rng.randrange(1, 6) for _ in range(4)]
    if len(set(r)) < 3: continue
    tot_r = sum(r)
    unit = rng.choice([50, 100, 150, 200, 250])
    total = tot_r * unit
    part = rng.randrange(4)
    ans = r[part] * unit
    names = ['A', 'B', 'C', 'D']
    o, ai = num_opts(ans, max(1, ans-200), ans+200, 50)
    qm('Ratio & Proportion', 'medium', 1,
        f"Rs {total} is divided among A, B, C and D in the ratio {r[0]}:{r[1]}:{r[2]}:{r[3]}. What is {names[part]}'s share?",
        f"रू {total} लाई A, B, C र D बीच {r[0]}:{r[1]}:{r[2]}:{r[3]} को अनुपातमा बाँडियो। {names[part]} को हिस्सा कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Total parts = {tot_r}. One part = {total}/{tot_r} = {unit}. {names[part]}'s share = {r[part]}x{unit} = {ans}.",
        f"कुल भाग = {tot_r} हो। एक भाग = {total}/{tot_r} = {unit} हो। {names[part]} को हिस्सा = {r[part]}×{unit} = {ans} हो।")

# effective speed with stops
for _ in range(60):
    v = rng.choice([40, 50, 60, 80])
    d = rng.choice([120, 160, 200, 240, 300, 400])
    stops = rng.choice([1, 2, 3])
    stop_min = rng.choice([10, 15, 20, 30])
    run_h = d / v
    total_h = run_h + stops * stop_min / 60
    eff = d / total_h
    if eff != int(eff): continue
    ans = int(eff)
    o, ai = num_opts(ans, max(1, ans-10), ans+10, 2)
    qm('Speed, Distance & Time', 'hard', 2,
        f"A bus runs at {v} km/h and covers {d} km, stopping {stops} time(s) for {stop_min} minutes each. What is its effective speed for the whole journey?",
        f"एउटा बस {v} किमी/घण्टाको गतिमा {d} किमी यात्रा गर्छ र {stops} पटक {stop_min} मिनेटका लागि रोकिन्छ। सम्पूर्ण यात्राको प्रभावकारी गति कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Running time = {d}/{v} = {run_h:g} h. Total time = {run_h:g} + {stops}x{stop_min}/60 = {total_h:g} h. Effective speed = {d}/{total_h:g} = {ans} km/h.",
        f"चल्ने समय = {d}/{v} = {run_h:g} घण्टा हो। कुल समय = {run_h:g} + {stops}×{stop_min}/६० = {total_h:g} घण्टा हो। प्रभावकारी गति = {d}/{total_h:g} = {ans} किमी/घण्टा हो।")

# 4 workers combined
SETS4 = [(10, 15, 20, 30), (6, 12, 18, 36), (12, 24, 36, 72), (8, 16, 24, 48), (5, 10, 20, 20), (15, 30, 45, 90)]
for _ in range(60):
    ts = rng.choice(SETS4)
    rate = sum(1/t for t in ts)
    days = 1 / rate
    if abs(days - round(days)) > 1e-9: continue
    ans = int(round(days))
    o, ai = num_opts(ans, max(1, ans-3), ans+3, 1)
    qm('Work & Time', 'hard', 2,
        f"Four workers can finish a work alone in {ts[0]}, {ts[1]}, {ts[2]} and {ts[3]} days respectively. In how many days can they finish it together?",
        f"चार जना कामदारले काम एक्लैले क्रमशः {ts[0]}, {ts[1]}, {ts[2]} र {ts[3]} दिनमा सक्न सक्छन्। सँगैले कति दिनमा सक्न सक्छन्?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Combined rate = 1/{ts[0]} + 1/{ts[1]} + 1/{ts[2]} + 1/{ts[3]} = {rate:.4f} per day. Days = 1/{rate:.4f} = {ans}.",
        f"संयुक्त दर = 1/{ts[0]} + 1/{ts[1]} + 1/{ts[2]} + 1/{ts[3]} = {rate:.4f} प्रतिदिन हो। दिन = १/{rate:.4f} = {ans} हो।")

# SI half-yearly rate
for _ in range(60):
    p = rng.choice([1000, 2000, 4000, 5000, 8000, 10000])
    si = rng.choice([100, 200, 300, 400, 500, 600, 800])
    t = rng.choice([1, 2, 3])
    r_half = si * 100 / (p * t * 2)
    if r_half != int(r_half): continue
    ans = int(r_half)
    o, ai = num_opts(ans, 1, ans+8, 1)
    qm('Interest', 'hard', 2,
        f"The simple interest on Rs {p} for {t} year(s) at a half-yearly rate is Rs {si}. What is the half-yearly rate of interest?",
        f"रू {p} मा {t} वर्षको अर्धवार्षिक दरले साधारण ब्याज रू {si} हुन्छ। अर्धवार्षिक ब्याज दर कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Rate per half-year = SI x 100 / (P x 2 x T) = {si}x100/({p}x2x{t}) = {ans}%.",
        f"प्रति अर्धवर्ष दर = SI × १०० / (P × २ × T) = {si}×१००/({p}×२×{t}) = {ans}% हो।")

# CI 3 years amount
for _ in range(60):
    p = rng.choice([1000, 2000, 4000, 5000, 8000, 10000])
    r = rng.choice([5, 10])
    amt = p * (1 + r/100) ** 3
    if abs(amt - round(amt)) > 1e-9: continue
    ans = int(round(amt))
    o, ai = num_opts(ans, max(100, ans-1000), ans+1000, 100)
    qm('Interest', 'hard', 2,
        f"What is the amount after 3 years if Rs {p} is invested at {r}% compound interest per annum?",
        f"रू {p} लाई {r}% वार्षिक चक्रवृद्धि ब्याजमा लगानी गर्दा ३ वर्षपछि रकम कति हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Amount = {p} x (1 + {r}/100)^3 = {p} x {(1+r/100)**3:.3f} = {ans}.",
        f"रकम = {p} × (१ + {r}/१००)³ = {p} × {(1+r/100)**3:.3f} = {ans} हो।")

# series: +squares of even numbers, x2+5, n^3-n
def series_block(gen, name, n=70):
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
def g_even_sq():
    a = rng.randrange(5, 40); s = [a]; i = rng.randrange(1, 4)
    ev = [2, 4, 6, 8, 10, 12, 14, 16]
    for k in range(4): s.append(s[-1] + ev[i+k]**2)
    return s, s[-1] + ev[i+4]**2
def g_x2p5():
    a = rng.randrange(2, 15); s = [a]
    for _ in range(4): s.append(s[-1]*2 + 5)
    return s, s[-1]*2 + 5
def g_n3mn():
    i = rng.randrange(2, 8)
    s = [k**3 - k for k in range(i, i+5)]
    return s, (i+5)**3 - (i+5)
series_block(g_even_sq, 'add squares of consecutive even numbers')
series_block(g_x2p5, 'multiply by 2 and add 5')
series_block(g_n3mn, 'n cubed minus n')

# calendar 1980-1989
for _ in range(100):
    y = rng.randrange(1980, 1990)
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

# clock angles at 10-min marks
for _ in range(60):
    h = rng.randrange(1, 12)
    mm = rng.choice([10, 20, 40, 50])
    ang = abs(30*h + 0.5*mm - 6*mm)
    if ang > 180: ang = 360 - ang
    ang = int(ang)
    o, ai = num_opts(ang, 0, 180, 5)
    qm('Calendar & Clock', 'hard', 2,
        f"What is the angle between the hands of a clock at {h}:{mm}?",
        f"घडीमा {h}:{mm} बज्दा सुईहरूबीचको कोण कति हुन्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Minute hand at {6*mm} deg. Hour hand at {30*h + 0.5*mm:g} deg. Smaller angle = {ang} degrees.",
        f"मिनेटको सुई {6*mm} डिग्रीमा छ। घण्टाको सुई {30*h + 0.5*mm:g} डिग्रीमा छ। सानो कोण = {ang} डिग्री हो।")

# HCF/LCM of 4 numbers
for _ in range(60):
    nums = [rng.randrange(4, 30) for _ in range(4)]
    if len(set(nums)) < 4: continue
    ans = math.lcm(math.lcm(nums[0], nums[1]), math.lcm(nums[2], nums[3]))
    if ans > 600: continue
    o, ai = num_opts(ans, max(1, ans-60), ans+60, 6)
    qm('HCF & LCM', 'hard', 2,
        f"What is the LCM of {nums[0]}, {nums[1]}, {nums[2]} and {nums[3]}?", f"{nums[0]}, {nums[1]}, {nums[2]} र {nums[3]} को लस कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"LCM of {nums[0]}, {nums[1]}, {nums[2]} and {nums[3]} = {ans}.",
        f"{nums[0]}, {nums[1]}, {nums[2]} र {nums[3]} को लस {ans} हो।")
for _ in range(60):
    nums = [rng.randrange(12, 120) for _ in range(4)]
    if len(set(nums)) < 4: continue
    ans = math.gcd(math.gcd(nums[0], nums[1]), math.gcd(nums[2], nums[3]))
    if ans < 2: continue
    o, ai = num_opts(ans, 1, ans+12, 1)
    qm('HCF & LCM', 'medium', 1,
        f"What is the HCF of {nums[0]}, {nums[1]}, {nums[2]} and {nums[3]}?", f"{nums[0]}, {nums[1]}, {nums[2]} र {nums[3]} को मस कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"HCF of {nums[0]}, {nums[1]}, {nums[2]} and {nums[3]} = {ans}.",
        f"{nums[0]}, {nums[1]}, {nums[2]} र {nums[3]} को मस {ans} हो।")

# area parallelogram / trapezium
for _ in range(60):
    b = rng.choice([6, 8, 10, 12, 14, 16, 20])
    h = rng.choice([4, 5, 6, 8, 10, 12])
    ans = b * h
    o, ai = num_opts(ans, max(1, ans-30), ans+30, 5)
    qm('Geometry', 'medium', 1,
        f"What is the area of a parallelogram with base {b} cm and height {h} cm?",
        f"आधार {b} सेमी र उचाइ {h} सेमी भएको समानान्तर चतुर्भुजको क्षेत्रफल कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Area = base x height = {b} x {h} = {ans} sq cm.",
        f"क्षेत्रफल = आधार × उचाइ = {b} × {h} = {ans} वर्ग सेमी हो।")
for _ in range(60):
    a = rng.choice([6, 8, 10, 12, 14])
    b = rng.choice([8, 10, 12, 14, 16, 18, 20])
    h = rng.choice([4, 5, 6, 8, 10])
    if (a + b) * h % 2: continue
    ans = (a + b) * h // 2
    o, ai = num_opts(ans, max(1, ans-30), ans+30, 5)
    qm('Geometry', 'hard', 2,
        f"What is the area of a trapezium with parallel sides {a} cm and {b} cm and height {h} cm?",
        f"समानान्तर भुजाहरू {a} सेमी र {b} सेमी र उचाइ {h} सेमी भएको समलम्ब चतुर्भुजको क्षेत्रफल कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Area = 1/2 x (sum of parallel sides) x height = 1/2 x ({a} + {b}) x {h} = {ans} sq cm.",
        f"क्षेत्रफल = १/२ × (समानान्तर भुजाहरूको योग) × उचाइ = १/२ × ({a} + {b}) × {h} = {ans} वर्ग सेमी हो।")

# profit/loss two items net
for _ in range(60):
    cp1 = rng.choice([500, 800, 1000, 1200])
    p1 = rng.choice([10, 20])
    cp2 = rng.choice([500, 800, 1000, 1200])
    l2 = rng.choice([10, 20])
    sp1 = cp1 * (100 + p1) // 100
    sp2 = cp2 * (100 - l2) // 100
    if cp1 * (100 + p1) % 100 or cp2 * (100 - l2) % 100: continue
    net = (sp1 + sp2) - (cp1 + cp2)
    if net == 0: continue
    kind = 'profit' if net > 0 else 'loss'
    kind_ne = 'नाफा' if net > 0 else 'नोक्सान'
    ans = abs(net)
    o, ai = num_opts(ans, max(1, ans-100), ans+100, 10)
    qm('Profit & Loss', 'hard', 2,
        f"One article costing Rs {cp1} is sold at a profit of {p1}% and another costing Rs {cp2} is sold at a loss of {l2}%. What is the net {kind} on the two articles together?",
        f"रू {cp1} पर्ने एउटा सामान {p1}% नाफामा र रू {cp2} पर्ने अर्को सामान {l2}% नोक्सानमा बेचियो। दुवै सामानमा जम्मा शुद्ध {kind_ne} कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"SP1 = {cp1}x{100+p1}/100 = {sp1}. SP2 = {cp2}x{100-l2}/100 = {sp2}. Total CP = {cp1+cp2}, total SP = {sp1+sp2}. Net {kind} = {ans}.",
        f"SP1 = {cp1}×{100+p1}/१०० = {sp1} हो। SP2 = {cp2}×{100-l2}/१०० = {sp2} हो। कुल CP = {cp1+cp2}, कुल SP = {sp1+sp2} हो। शुद्ध {kind_ne} = {ans} हो।")

# age 4 people ratio
for _ in range(60):
    r = [rng.randrange(1, 6) for _ in range(4)]
    if len(set(r)) < 3: continue
    u = rng.choice([3, 4, 5, 6, 7])
    ages = [x*u for x in r]
    person = rng.choice(['A', 'B', 'C', 'D'])
    ans = ages[['A', 'B', 'C', 'D'].index(person)]
    o, ai = num_opts(ans, max(1, ans-15), ans+15, 3)
    qm('Age Problems', 'medium', 1,
        f"The ages of A, B, C and D are in the ratio {r[0]}:{r[1]}:{r[2]}:{r[3]}. If the sum of their ages is {sum(ages)}, how old is {person}?",
        f"A, B, C र D को उमेरको अनुपात {r[0]}:{r[1]}:{r[2]}:{r[3]} छ। उनीहरूको उमेरको योग {sum(ages)} छ भने {person} कति वर्षको हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Total parts = {sum(r)}. One part = {sum(ages)}/{sum(r)} = {u}. {person}'s age = {r[['A','B','C','D'].index(person)]}x{u} = {ans}.",
        f"कुल भाग = {sum(r)} हो। एक भाग = {sum(ages)}/{sum(r)} = {u} हो। {person} को उमेर = {r[['A','B','C','D'].index(person)]}×{u} = {ans} हो।")

# mixture 3 ingredients
for _ in range(60):
    r = [rng.randrange(1, 5) for _ in range(3)]
    if len(set(r)) < 2: continue
    tot = sum(r)
    unit = rng.choice([10, 20, 30, 40, 50])
    total = tot * unit
    part = rng.randrange(3)
    ans = r[part] * unit
    names = ['milk', 'water', 'sugar']
    names_ne = ['दूध', 'पानी', 'चिनी']
    o, ai = num_opts(ans, max(1, ans-50), ans+50, 10)
    qm('Mixtures & Alligation', 'medium', 1,
        f"A mixture of {total} litres contains milk, water and sugar in the ratio {r[0]}:{r[1]}:{r[2]}. How many litres of {names[part]} does it contain?",
        f"{total} लिटरको मिश्रणमा दूध, पानी र चिनी {r[0]}:{r[1]}:{r[2]} को अनुपातमा छन्। यसमा {names_ne[part]} कति लिटर छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Total parts = {tot}. One part = {total}/{tot} = {unit}. {names[part].capitalize()} = {r[part]}x{unit} = {ans} litres.",
        f"कुल भाग = {tot} हो। एक भाग = {total}/{tot} = {unit} हो। {names_ne[part]} = {r[part]}×{unit} = {ans} लिटर हो।")

# trains same direction
for _ in range(60):
    l1 = rng.choice([120, 150, 180, 200, 240])
    l2 = rng.choice([120, 150, 180, 200, 240])
    v1 = rng.choice([72, 81, 90, 108])
    v2 = rng.choice([36, 45, 54, 63])
    if v1 <= v2: continue
    rel = (v1 - v2) * 5/18
    t = (l1 + l2) / rel
    if t != int(t): continue
    ans = int(t)
    o, ai = num_opts(ans, max(1, ans-15), ans+15, 1)
    qm('Trains', 'hard', 2,
        f"A {l1} m long train running at {v1} km/h overtakes a {l2} m long train running at {v2} km/h in the same direction. In how many seconds will the faster train cross the slower one completely?",
        f"{l1} मिटर लामो रेल {v1} किमी/घण्टाको गतिमा उही दिशामा {v2} किमी/घण्टामा चलिरहेको {l2} मिटर लामो रेललाई उछिन्छ। छिटो रेलले ढिलो रेललाई पूर्ण रूपमा पार गर्न कति सेकेन्ड लाग्छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Relative speed = ({v1} - {v2}) x 5/18 = {rel:g} m/s. Total length = {l1+l2} m. Time = {l1+l2}/{rel:g} = {ans} s.",
        f"सापेक्ष गति = ({v1} - {v2}) × ५/१८ = {rel:g} मि/से हो। कुल लम्बाइ = {l1+l2} मिटर हो। समय = {l1+l2}/{rel:g} = {ans} सेकेन्ड हो।")

# boats: still-water speed from upstream/downstream
for _ in range(60):
    up = rng.choice([4, 6, 8, 10])
    down = rng.choice([10, 12, 14, 16, 20])
    if down <= up: continue
    vb = (up + down) / 2
    if vb != int(vb): continue
    ans = int(vb)
    o, ai = num_opts(ans, max(1, ans-5), ans+5, 1)
    qm('Boats & Streams', 'hard', 2,
        f"A boat travels {up} km/h upstream and {down} km/h downstream. What is the speed of the boat in still water?",
        f"एउटा डुङ्गा माथितिर {up} किमी/घण्टा र तलतिर {down} किमी/घण्टाको गतिमा यात्रा गर्छ। स्थिर पानीमा डुङ्गाको गति कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Still-water speed = (upstream + downstream)/2 = ({up} + {down})/2 = {ans} km/h.",
        f"स्थिर पानीको गति = (माथितिर + तलतिर)/२ = ({up} + {down})/२ = {ans} किमी/घण्टा हो।")

# sum of first n cubes
for _ in range(60):
    n = rng.randrange(4, 21)
    ans = (n * (n + 1) // 2) ** 2
    o, ai = num_opts(ans, max(1, ans-200), ans+200, 50)
    qm('Number System', 'hard', 2,
        f"What is the sum of the cubes of the first {n} natural numbers?",
        f"पहिलो {n} वटा प्राकृतिक सङ्ख्याहरूको घनहरूको योग कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Sum of cubes = (n(n+1)/2)^2 = ({n}x{n+1}/2)^2 = {ans}.",
        f"घनहरूको योग = (n(n+१)/२)² = ({n}×{n+1}/२)² = {ans} हो।")

# fractions: add unlike fractions
for _ in range(80):
    a, b = rng.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5), (1, 6), (5, 6)])
    c, d = rng.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5)])
    if b == d: continue
    lcm = math.lcm(b, d)
    num = a * (lcm // b) + c * (lcm // d)
    g = math.gcd(num, lcm)
    ans_str = f"{num//g}/{lcm//g}" if lcm//g != 1 else str(num//g)
    opts = [ans_str, f"{num}/{lcm}", f"{(num+1)//g}/{(lcm)//g}" if (num+1)//g != num//g else f"{num//g+1}/{lcm//g}", f"{num//g}/{lcm//g+1}"]
    if len(set(opts)) < 4: continue
    o = opts[:]; rng.shuffle(o)
    qm('Fractions', 'medium', 1,
        f"What is {a}/{b} + {c}/{d}?", f"{a}/{b} + {c}/{d} कति हो?",
        o, [dev(x) for x in o], o.index(ans_str),
        f"{a}/{b} + {c}/{d} = {a*(lcm//b)}/{lcm} + {c*(lcm//d)}/{lcm} = {num}/{lcm} = {ans_str}.",
        f"{a}/{b} + {c}/{d} = {a*(lcm//b)}/{lcm} + {c*(lcm//d)}/{lcm} = {num}/{lcm} = {ans_str} हो।")

# decimals: multiply two decimals
for _ in range(80):
    a = rng.choice([1.2, 1.5, 2.4, 2.5, 3.6, 4.5, 0.6, 0.8, 1.8, 2.2, 3.3, 5.5, 0.4, 0.25, 1.25, 2.75])
    b = rng.choice([1.2, 1.5, 2.4, 2.5, 3.6, 4.5, 0.6, 0.8, 1.8, 2.2, 3.3, 5.5, 0.4, 0.25, 1.25, 2.75])
    ans = round(a * b, 4)
    o = [ans, round(ans+1, 2), round(ans-1, 2), round(ans+2, 2)]
    o = [x for x in o if x > 0]
    if len(set(o)) < 4: continue
    rng.shuffle(o)
    qm('Decimals', 'medium', 1,
        f"What is {a} x {b}?", f"{a} × {b} कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], o.index(ans),
        f"{a} x {b} = {ans}.", f"{a} × {b} = {ans} हो।")

# largest 3-digit number divisible by k / smallest 4-digit divisible by k
for _ in range(60):
    k = rng.choice([6, 7, 8, 9, 11, 12, 13, 15, 17, 19, 21, 23])
    ans = (999 // k) * k
    o, ai = num_opts(ans, max(100, ans-100), ans+100, k)
    qm('Number System', 'medium', 1,
        f"What is the largest 3-digit number divisible by {k}?", f"{k} ले भाग जाने सबैभन्दा ठूलो ३-अङ्कको सङ्ख्या कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"999 / {k} = {999//k} remainder {999%k}. Largest 3-digit multiple = {999//k} x {k} = {ans}.",
        f"९९९ / {k} = {999//k} शेष {999%k} हो। सबैभन्दा ठूलो ३-अङ्कको गुणन = {999//k} × {k} = {ans} हो।")
for _ in range(60):
    k = rng.choice([6, 7, 8, 9, 11, 12, 13, 15, 17, 19, 21, 23])
    ans = ((1000 + k - 1) // k) * k
    o, ai = num_opts(ans, max(100, ans-100), ans+100, k)
    qm('Number System', 'medium', 1,
        f"What is the smallest 4-digit number divisible by {k}?", f"{k} ले भाग जाने सबैभन्दा सानो ४-अङ्कको सङ्ख्या कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"1000 / {k} = {1000//k} remainder {1000%k}. Smallest 4-digit multiple = {(1000+k-1)//k} x {k} = {ans}.",
        f"१००० / {k} = {1000//k} शेष {1000%k} हो। सबैभन्दा सानो ४-अङ्कको गुणन = {(1000+k-1)//k} × {k} = {ans} हो।")
nm = emm.write('expansion-r10-maths9.json')
print('MATHS9 TOTAL:', nm, 'rejected:', len(emm.rejected))

# ================= IQ 6 =================
emi = Emitter(bank, 'R10-IQ6')
L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def qi(topic, diff, marks, q, qn, opts, optn, ans, exp, expn):
    emi.emit(EX, 'IQ & Reasoning', topic, diff, marks, q, qn, opts, optn, ans, exp, expn)
def letter_opts(ans):
    s = {ans}
    while len(s) < 4:
        s.add(rng.choice(L))
    o = list(s); rng.shuffle(o)
    return o, o.index(ans)

# vowel series
VOW = ['A', 'E', 'I', 'O', 'U']
for _ in range(60):
    start = rng.randrange(0, 3)
    seq = [VOW[(start + k) % 5] for k in range(4)]
    ans = VOW[(start + 4) % 5]
    o, ai = letter_opts(ans)
    disp = ', '.join(seq)
    qi('Letter Series', 'easy', 1,
        f"What is the next letter in the series: {disp}, ...?", f"श्रेणीको अर्को अक्षर कुन हो: {disp}, ...?",
        o, o, ai,
        f"The series cycles through the vowels A, E, I, O, U. After {seq[-1]} comes {ans}.",
        f"श्रेणीले स्वरहरू A, E, I, O, U लाई चक्रीय रूपमा दोहोर्‍याउँछ। {seq[-1]} पछि {ans} आउँछ।")
# consonant series (skip 2 consonants)
CONS = [c for c in L if c not in 'AEIOU']
for _ in range(80):
    start = rng.randrange(0, 15)
    seq = [CONS[(start + 3*k) % 21] for k in range(4)]
    ans = CONS[(start + 12) % 21]
    o, ai = letter_opts(ans)
    disp = ', '.join(seq)
    qi('Letter Series', 'medium', 1,
        f"What is the next letter in the series: {disp}, ...?", f"श्रेणीको अर्को अक्षर कुन हो: {disp}, ...?",
        o, o, ai,
        f"Counting consonants only, each step skips 2 consonants. After {seq[-1]} comes {ans}.",
        f"व्यञ्जनहरू मात्र गन्दा प्रत्येक चरणमा २ व्यञ्जन छोडिन्छ। {seq[-1]} पछि {ans} आउँछ।")

# number series: x3+5, +triangular descending, n^2-n
def series_block_i(gen, name, n=70):
    for _ in range(n):
        seq, ans = gen()
        if seq is None: continue
        disp = ', '.join(str(x) for x in seq)
        o, ai = num_opts(ans, max(0, ans-40), ans+40, 1)
        qi('Number Series', 'medium', 1,
            f"What is the next number in the series: {disp}, ...?", f"श्रेणीको अर्को सङ्ख्या कति हो: {disp}, ...?",
            [str(x) for x in o], [dev_num(x) for x in o], ai,
            f"The series follows the {name} pattern. The next term is {ans}.",
            f"श्रेणीले {name} ढाँचा पछ्याउँछ। अर्को पद {ans} हो।")
def g_x3p5():
    a = rng.randrange(2, 10); s = [a]
    for _ in range(4): s.append(s[-1]*3 + 5)
    return s, s[-1]*3 + 5
def g_tri_desc():
    tri = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
    a = rng.randrange(50, 150); s = [a]; i = rng.randrange(3, 6)
    for k in range(4): s.append(s[-1] - tri[i-k])
    return s, s[-1] - tri[i-4]
def g_n2mn():
    i = rng.randrange(3, 10)
    s = [k*k - k for k in range(i, i+5)]
    return s, (i+5)*(i+5) - (i+5)
series_block_i(g_x3p5, 'multiply by 3 and add 5')
series_block_i(g_tri_desc, 'subtract consecutive triangular numbers')
series_block_i(g_n2mn, 'n squared minus n')

# coding: Caesar +3 / -3
WORDS_C = ['CAT', 'DOG', 'SUN', 'MOON', 'STAR', 'FISH', 'BIRD', 'BOOK', 'TREE', 'KING', 'LION', 'WOLF', 'BEAR', 'DUCK', 'FROG', 'GOAT', 'APPLE', 'MANGO', 'NEPAL', 'WATER', 'EARTH', 'FIRE', 'WIND', 'RAIN', 'CLOUD', 'RIVER', 'GREEN', 'BLACK', 'WHITE', 'BROWN', 'SMALL', 'LARGE', 'HAPPY', 'BRAVE', 'SMART', 'QUICK', 'SLOW', 'FAST', 'HIGH', 'LONG']
for w in WORDS_C:
    shift = rng.choice([3, -3])
    code = ''.join(L[(L.index(c) + shift) % 26] for c in w)
    others = [x for x in WORDS_C if x != w and len(x) == len(w)]
    rng.shuffle(others)
    ds = [''.join(L[(L.index(c) + shift) % 26] for c in x) for x in others[:3]]
    if code in ds: continue
    o = [code] + ds; rng.shuffle(o)
    word = 'forward' if shift > 0 else 'backward'
    word_ne = 'अगाडि' if shift > 0 else 'पछाडि'
    qi('Coding-Decoding', 'medium', 1,
        f"In a code, each letter is shifted {abs(shift)} places {word} in the alphabet. How is '{w}' written in that code?",
        f"एउटा कोडमा प्रत्येक अक्षरलाई वर्णमालामा {abs(shift)} स्थान {word_ne} सारिन्छ। '{w}' लाई उक्त कोडमा कसरी लेखिन्छ?",
        o, o, o.index(code),
        f"Shifting each letter of {w} by {shift:+d} gives {code}.",
        f"{w} का प्रत्येक अक्षरलाई {shift:+d} ले सार्दा {code} हुन्छ।")

# odd-one-out: divisible by 7 / perfect squares
for _ in range(60):
    base = rng.choice([7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98])
    chosen = [base]
    while len(chosen) < 3:
        v = rng.choice([7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126])
        if v not in chosen: chosen.append(v)
    odd = rng.randrange(10, 130)
    while odd % 7 == 0:
        odd = rng.randrange(10, 130)
    o = chosen + [odd]; rng.shuffle(o)
    qi('Odd One Out', 'easy', 1,
        f"Which is the odd one out? {', '.join(str(x) for x in o)}",
        f"कुन फरक छ? {', '.join(dev_num(x) for x in o)}",
        [str(x) for x in o], [dev_num(x) for x in o], o.index(odd),
        f"{chosen[0]}, {chosen[1]} and {chosen[2]} are all divisible by 7. {odd} is not divisible by 7.",
        f"{chosen[0]}, {chosen[1]} र {chosen[2]} सबै ७ ले भाग जान्छन्। {odd}, ७ ले भाग जाँदैन।")
for _ in range(60):
    sqs = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225]
    chosen = rng.sample(sqs, 3)
    odd = rng.randrange(10, 230)
    while int(odd ** 0.5) ** 2 == odd:
        odd = rng.randrange(10, 230)
    o = chosen + [odd]; rng.shuffle(o)
    qi('Odd One Out', 'easy', 1,
        f"Which is the odd one out? {', '.join(str(x) for x in o)}",
        f"कुन फरक छ? {', '.join(dev_num(x) for x in o)}",
        [str(x) for x in o], [dev_num(x) for x in o], o.index(odd),
        f"{chosen[0]}, {chosen[1]} and {chosen[2]} are perfect squares. {odd} is not a perfect square.",
        f"{chosen[0]}, {chosen[1]} र {chosen[2]} पूर्ण वर्ग हुन्। {odd} पूर्ण वर्ग होइन।")

# blood relations: only son/daughter
NAMES = ['Ram', 'Hari', 'Sita', 'Gita', 'Ramesh', 'Suresh', 'Anita', 'Sunita', 'Bikash', 'Prakash', 'Maya', 'Laxmi', 'Krishna', 'Rita', 'Deepak', 'Nirmala']
REL2 = [
    ("{a} is the only son of {b}. How is {b} related to {a}?", "{a}, {b} को एक मात्र छोरा हो। {b}, {a} को के हो?", "Father or Mother", "बुबा वा आमा", ["Brother", "Uncle", "Grandfather"]),
    ("{a} is the only daughter of {b}. How is {b} related to {a}?", "{a}, {b} की एक मात्र छोरी हो। {b}, {a} को के हो?", "Father or Mother", "बुबा वा आमा", ["Sister", "Aunt", "Grandmother"]),
    ("{a} is the only brother of {b}. How is {a} related to {b}?", "{a}, {b} को एक मात्र भाइ हो। {a}, {b} को के हो?", "Brother", "भाइ", ["Father", "Uncle", "Son"]),
    ("{a} is the only sister of {b}. How is {a} related to {b}?", "{a}, {b} की एक मात्र बहिनी हो। {a}, {b} को के हो?", "Sister", "बहिनी", ["Mother", "Aunt", "Daughter"]),
]
for _ in range(80):
    t, tn, ans, ansn, ds = rng.choice(REL2)
    a, b = rng.sample(NAMES, 2)
    q = t.format(a=a, b=b)
    qn = tn.format(a=a, b=b)
    dne = {'Brother': 'भाइ', 'Uncle': 'काका/मामा', 'Grandfather': 'हजुरबुबा', 'Sister': 'बहिनी', 'Aunt': 'फुपू/माइजू', 'Grandmother': 'हजुरआमा', 'Father': 'बुबा', 'Son': 'छोरा', 'Mother': 'आमा', 'Daughter': 'छोरी', 'Father or Mother': 'बुबा वा आमा'}
    o = [ans] + ds; rng.shuffle(o)
    qi('Blood Relations', 'medium', 1, q, qn, o, [dne.get(x, x) for x in o], o.index(ans),
        f"From the relation given, {a} is the {ans.lower()} of {b}.",
        f"दिइएको सम्बन्धबाट {a}, {b} को {ansn} हो।")

# directions: 3-step Pythagorean net distance
for _ in range(80):
    # pick a 3-4-5 style walk: east a, north b, west c -> net displacement
    a = rng.choice([3, 6, 9, 12])
    b = rng.choice([4, 8, 12])
    c = rng.choice([0, 3, 6])
    x = a - c; y = b
    dist = math.hypot(x, y)
    if dist != int(dist): continue
    ans = int(dist)
    o, ai = num_opts(ans, max(1, ans-5), ans+5, 1)
    steps = f"east {a} km, then north {b} km" + (f", then west {c} km" if c else "")
    steps_ne = f"पूर्व {dev_num(a)} किमी, त्यसपछि उत्तर {dev_num(b)} किमी" + (f", त्यसपछि पश्चिम {dev_num(c)} किमी" if c else "")
    qi('Direction Sense', 'hard', 2,
        f"A man walks {steps}. How far is he from his starting point?",
        f"एक जना मानिस {steps_ne} हिँड्छ। ऊ सुरुको बिन्दुबाट कति टाढा छ?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"Net east = {a} - {c} = {x} km, net north = {b} km. Distance = sqrt({x}^2 + {b}^2) = sqrt({x*x + b*b}) = {ans} km.",
        f"शुद्ध पूर्व = {a} - {c} = {x} किमी, शुद्ध उत्तर = {b} किमी हो। दूरी = sqrt({x}² + {b}²) = sqrt({x*x + b*b}) = {ans} किमी हो।")

# ranking: from both ends, two people
for _ in range(60):
    n = rng.choice([20, 25, 30, 35, 40])
    r_left = rng.randrange(3, n-5)
    r_right = rng.randrange(3, n-5)
    if r_left + r_right >= n: continue
    # A is r_left from left; B is r_right from right; how many between them?
    pos_b_left = n - r_right + 1
    between = pos_b_left - r_left - 1
    if between < 0: continue
    o, ai = num_opts(between, 0, n, 1)
    qi('Ranking', 'hard', 2,
        f"In a row of {n} students, A is {ord_s(r_left)} from the left and B is {ord_s(r_right)} from the right. How many students are between A and B?",
        f"{n} जना विद्यार्थीको लाइनमा A बायाँबाट {r_left}औँ छ र B दायाँबाट {r_right}औँ छ। A र B बीच कति जना विद्यार्थी छन्?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"B is {ord_s(pos_b_left)} from the left. Students between A and B = {pos_b_left} - {r_left} - 1 = {between}.",
        f"B बायाँबाट {pos_b_left}औँ छ। A र B बीचका विद्यार्थी = {pos_b_left} - {r_left} - १ = {between} हो।")

# alphabet: reverse alphabet position (Z=1)
for _ in range(60):
    a = rng.choice(L)
    ans = 26 - L.index(a)
    o, ai = num_opts(ans, 1, 26, 1)
    qi('Alphabet Test', 'medium', 1,
        f"If Z=1, Y=2, X=3, ... A=26 (reverse alphabet), what is the position of '{a}'?",
        f"यदि Z=१, Y=२, X=३, ... A=२६ (उल्टो वर्णमाला) हो भने '{a}' को स्थान कति हो?",
        [str(x) for x in o], [dev_num(x) for x in o], ai,
        f"In reverse order, {a} is {ord_s(ans)} from Z.",
        f"उल्टो क्रममा {a}, Z बाट {ans}औँ हो।")
ni = emi.write('expansion-r10-iq6.json')
print('IQ6 TOTAL:', ni, 'rejected:', len(emi.rejected))
print('G30 GRAND TOTAL:', nv + nm + ni)
