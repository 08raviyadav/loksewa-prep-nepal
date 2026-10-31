#!/usr/bin/env python3
"""R10 generator 13: English grammar (~1,300). Prepositions (collocations),
articles, active/passive voice, direct/indirect speech, error spotting,
sentence correction, question tags. All templates curated from standard
PSC/TSC English grammar syllabus."""
import sys, random
sys.path.insert(0, 'scripts/r10')
from gen_common import Bank, Emitter, dev, dev_num

bank = Bank()
em = Emitter(bank, 'R10-GRAM')
rng = random.Random(71106)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'police', 'army', 'tsc-primary', 'tsc-secondary', 'tsc-lower-secondary']
PREPS = ['in', 'on', 'at', 'of', 'to', 'for', 'with', 'by', 'from', 'about']

def E(sub, diff, q, qn, o, on, expl, expln, idx=0):
    em.emit(EX, 'English', sub, diff, 2, q, qn, o, on, idx, expl, expln)

# ---------- preposition collocations ----------
COLL = [
    ('interested', 'in', 'रुचि राख्नु'), ('good', 'at', 'राम्रो हुनु'), ('afraid', 'of', 'डराउनु'),
    ('depend', 'on', 'निर्भर गर्नु'), ('look', 'after', 'हेरचाह गर्नु'), ('listen', 'to', 'सुन्नु'),
    ('believe', 'in', 'विश्वास गर्नु'), ('angry', 'with', 'रिसाउनु'), ('married', 'to', 'विवाह गर्नु'),
    ('proud', 'of', 'गर्व गर्नु'), ('fond', 'of', 'मन पराउनु'), ('aware', 'of', 'जानकार हुनु'),
    ('capable', 'of', 'सक्षम हुनु'), ('full', 'of', 'भरिएको'), ('tired', 'of', 'थाक्नु'),
    ('responsible', 'for', 'जिम्मेवार हुनु'), ('famous', 'for', 'प्रसिद्ध हुनु'), ('sorry', 'for', 'दुःखी हुनु'),
    ('grateful', 'to', 'कृतज्ञ हुनु'), ('kind', 'to', 'दयालु हुनु'), ('accustomed', 'to', 'बानी पर्नु'),
    ('addicted', 'to', 'लत लाग्नु'), ('similar', 'to', 'समान हुनु'), ('different', 'from', 'फरक हुनु'),
    ('suffer', 'from', 'पीडित हुनु'), ('die', 'of', 'मर्नु'), ('consist', 'of', 'बनेको हुनु'),
    ('agree', 'with', 'सहमत हुनु'), ('disagree', 'with', 'असहमत हुनु'), ('argue', 'with', 'बहस गर्नु'),
    ('complain', 'about', 'गुनासो गर्नु'), ('talk', 'about', 'कुरा गर्नु'), ('think', 'about', 'सोच्नु'),
    ('worry', 'about', 'चिन्ता गर्नु'), ('dream', 'of', 'सपना देख्नु'), ('arrive', 'at', 'पुग्नु'),
    ('arrive', 'in', 'पुग्नु'), ('look', 'for', 'खोज्नु'), ('wait', 'for', 'पर्खनु'),
    ('ask', 'for', 'माग्नु'), ('pay', 'for', 'तिर्नु'), ('apply', 'for', 'आवेदन दिनु'),
    ('belong', 'to', 'सम्बन्धित हुनु'), ('listen', 'to', 'सुन्नु'), ('speak', 'to', 'बोल्नु'),
    ('write', 'to', 'लेख्नु'), ('send', 'to', 'पठाउनु'), ('give', 'to', 'दिनु'),
    ('take care', 'of', 'हेरचाह गर्नु'), ('in charge', 'of', 'जिम्मेवार हुनु'), ('instead', 'of', 'सट्टामा'),
    ('because', 'of', 'कारणले'), ('in spite', 'of', 'तथापि'), ('in front', 'of', 'अगाडि'),
    ('next', 'to', 'छेउमा'), ('close', 'to', 'नजिक'), ('far', 'from', 'टाढा'),
    ('away', 'from', 'टाढा'), ('safe', 'from', 'सुरक्षित'), ('free', 'from', 'मुक्त'),
    ('escape', 'from', 'भाग्नु'), ('hide', 'from', 'लुक्नु'), ('protect', 'from', 'जोगाउनु'),
    ('prevent', 'from', 'रोक्नु'), ('stop', 'from', 'रोक्नु'), ('borrow', 'from', 'सापट लिनु'),
    ('lend', 'to', 'सापट दिनु'), ('borrow', 'from', 'सापट लिनु'), ('shout', 'at', 'कराउनु'),
    ('laugh', 'at', 'हाँस्नु'), ('smile', 'at', 'मुसुक्क हाँस्नु'), ('look', 'at', 'हेर्नु'),
    ('point', 'at', 'औँल्याउनु'), ('aim', 'at', 'लक्ष्य गर्नु'), ('arrive', 'at', 'पुग्नु'),
    ('good', 'at', 'राम्रो हुनु'), ('bad', 'at', 'नराम्रो हुनु'), ('clever', 'at', 'चतुर हुनु'),
    ('interested', 'in', 'रुचि राख्नु'), ('involved', 'in', 'संलग्न हुनु'), ('believe', 'in', 'विश्वास गर्नु'),
    ('succeed', 'in', 'सफल हुनु'), ('fail', 'in', 'असफल हुनु'), ('arrive', 'in', 'पुग्नु'),
    ('live', 'in', 'बस्नु'), ('born', 'in', 'जन्मिनु'), ('dressed', 'in', 'पहिरिनु'),
    ('write', 'in', 'लेख्नु'), ('read', 'in', 'पढ्नु'), ('speak', 'in', 'बोल्नु'),
]
seen_coll = set()
for word, prep, meaning in COLL:
    key = (word, prep)
    if key in seen_coll: continue
    seen_coll.add(key)
    ds = rng.sample([p for p in PREPS if p != prep], 3)
    o = [prep] + ds
    on = o[:]
    E('Prepositions', 'medium',
      f'Choose the correct preposition: She is {word} ___ music.',
      f'सही पूर्वसर्ग छान्नुहोस्: She is {word} ___ music।', o, on,
      f'The correct preposition after "{word}" is "{prep}".',
      f'"{word}" पछि सही पूर्वसर्ग "{prep}" हो।')
    ds2 = rng.sample([p for p in PREPS if p != prep], 3)
    o2 = [prep] + ds2
    on2 = o2[:]
    E('Prepositions', 'medium',
      f'Fill in the blank with the correct preposition: He is {word} ___ his work.',
      f'खाली ठाउँमा सही पूर्वसर्ग भर्नुहोस्: He is {word} ___ his work।', o2, on2,
      f'The correct preposition after "{word}" is "{prep}".',
      f'"{word}" पछि सही पूर्वसर्ग "{prep}" हो।')

# ---------- articles ----------
ART = [
    ('___ sun rises in the east.', 'The', 'सूर्य'), ('___ moon is beautiful tonight.', 'The', 'चन्द्रमा'),
    ('I saw ___ elephant at the zoo.', 'an', 'हात्ती'), ('She is ___ honest woman.', 'an', 'इमानदार महिला'),
    ('He is ___ university student.', 'a', 'विश्वविद्यालयका विद्यार्थी'), ('___ Ganga is a holy river.', 'The', 'गङ्गा'),
    ('Nepal is ___ beautiful country.', 'a', 'सुन्दर देश'), ('___ Himalayas are in Nepal.', 'The', 'हिमालय'),
    ('I bought ___ umbrella yesterday.', 'an', 'छाता'), ('___ hour ago, he left.', 'An', 'घण्टा'),
    ('She plays ___ piano very well.', 'the', 'पियानो'), ('He is ___ best student in the class.', 'the', 'उत्कृष्ट विद्यार्थी'),
    ('___ water is essential for life.', 'no article', 'पानी'), ('___ Mount Everest is the highest peak.', 'no article', 'सगरमाथा'),
    ('I go to school ___ bus.', 'by', 'बस'), ('He is ___ M.A. in English.', 'an', 'एमए'),
    ('___ earth revolves around the sun.', 'The', 'पृथ्वी'), ('She is ___ European.', 'a', 'युरोपेली'),
    ('___ one-eyed man was there.', 'A', 'एक आँखा भएको मानिस'), ('He is ___ honest man.', 'an', 'इमानदार मानिस'),
    ('___ rich should help the poor.', 'The', 'धनी'), ('___ honesty is the best policy.', 'no article', 'इमानदारी'),
    ('I have ___ headache.', 'a', 'टाउको दुखाइ'), ('___ Taj Mahal is in India.', 'The', 'ताजमहल'),
    ('She is ___ singer and ___ dancer.', 'a, a', 'गायिका र नर्तकी'), ('___ gold is a precious metal.', 'no article', 'सुन'),
    ('He went to ___ hospital yesterday.', 'the', 'अस्पताल'), ('___ Bible is a holy book.', 'The', 'बाइबल'),
    ('I saw ___ bird in the tree.', 'a', 'चरा'), ('___ apple a day keeps the doctor away.', 'An', 'स्याउ'),
    ('He is ___ engineer.', 'an', 'इन्जिनियर'), ('She is ___ honest person.', 'an', 'इमानदार व्यक्ति'),
    ('___ ink is black.', 'no article', 'मसी'), ('I read ___ Ramayana every day.', 'the', 'रामायण'),
]
ART_OPTS = ['a', 'an', 'the', 'no article']
for sent, correct, hint in ART:
    ds = [x for x in ART_OPTS if x.lower() != correct.lower()]
    if correct.lower() not in [x.lower() for x in ART_OPTS]:
        ds = ['a', 'an', 'the']
    o = [correct] + ds[:3]
    on = o[:]
    E('Articles', 'medium', f'Choose the correct article: {sent}',
      f'सही आर्टिकल छान्नुहोस्: {sent}', o, on,
      f'The correct article is "{correct}".', f'सही आर्टिकल "{correct}" हो।')

# ---------- active / passive voice ----------
VOICE = [
    ('Ram writes a letter.', 'A letter is written by Ram.', 'रामले पत्र लेख्छ'),
    ('She eats an apple.', 'An apple is eaten by her.', 'उसले स्याउ खान्छे'),
    ('They play football.', 'Football is played by them.', 'उनीहरू फुटबल खेल्छन्'),
    ('He reads a book.', 'A book is read by him.', 'उसले किताब पढ्छ'),
    ('The cat chased the mouse.', 'The mouse was chased by the cat.', 'बिरालोले मुसालाई खेद्यो'),
    ('She sang a song.', 'A song was sung by her.', 'उसले गीत गाइन्'),
    ('He bought a car.', 'A car was bought by him.', 'उसले कार किन्यो'),
    ('They built a house.', 'A house was built by them.', 'उनीहरूले घर बनाए'),
    ('Ram is writing a letter.', 'A letter is being written by Ram.', 'राम पत्र लेख्दैछ'),
    ('She is cooking food.', 'Food is being cooked by her.', 'उसले खाना पकाउँदैछे'),
    ('He has finished the work.', 'The work has been finished by him.', 'उसले काम सक्यो'),
    ('They have completed the task.', 'The task has been completed by them.', 'उनीहरूले काम पूरा गरे'),
    ('The teacher punished the student.', 'The student was punished by the teacher.', 'शिक्षकले विद्यार्थीलाई सजाय दिए'),
    ('She will help me.', 'I will be helped by her.', 'उसले मलाई सहयोग गर्नेछे'),
    ('He will write a book.', 'A book will be written by him.', 'उसले किताब लेख्नेछ'),
    ('Open the door.', 'Let the door be opened.', 'ढोका खोल्नुहोस्'),
    ('Close the window.', 'Let the window be closed.', 'झ्याल बन्द गर्नुहोस्'),
    ('Do the work.', 'Let the work be done.', 'काम गर्नुहोस्'),
    ('Bring a glass of water.', 'Let a glass of water be brought.', 'एक गिलास पानी ल्याउनुहोस्'),
    ('Nobody likes him.', 'He is liked by nobody.', 'कसैले उसलाई मन पराउँदैन'),
]
for active, passive, meaning in VOICE:
    ds = [active, passive.replace('is', 'was'), passive.replace('by', 'with')]
    ds = [x for x in ds if x != passive][:3]
    o = [passive] + ds
    on = o[:]
    E('Active & Passive Voice', 'medium', f'Choose the passive voice of: "{active}"',
      f'"{active}" को कर्मवाच्य छान्नुहोस्।', o, on,
      f'The passive voice is: {passive}.', f'कर्मवाच्य: {passive} हो।')
    ds2 = [passive, active, passive.replace('is', 'are')]
    ds2 = [x for x in ds2 if x != active][:3]
    o2 = [active] + ds2
    on2 = o2[:]
    E('Active & Passive Voice', 'medium', f'Choose the active voice of: "{passive}"',
      f'"{passive}" को कर्तृवाच्य छान्नुहोस्।', o2, on2,
      f'The active voice is: {active}.', f'कर्तृवाच्य: {active} हो।')

# ---------- direct / indirect speech ----------
SPEECH = [
    ('He said, "I am happy."', 'He said that he was happy.', 'उसले भन्यो, "म खुसी छु।"'),
    ('She said, "I will come tomorrow."', 'She said that she would come the next day.', 'उसले भनिन्, "म भोलि आउनेछु।"'),
    ('Ram said, "I am reading a book."', 'Ram said that he was reading a book.', 'रामले भन्यो, "म किताब पढ्दैछु।"'),
    ('He said, "I have finished my work."', 'He said that he had finished his work.', 'उसले भन्यो, "मैले मेरो काम सकें।"'),
    ('She said, "I went to school yesterday."', 'She said that she had gone to school the previous day.', 'उसले भनिन्, "म हिजो विद्यालय गएँ।"'),
    ('He said, "I can do it."', 'He said that he could do it.', 'उसले भन्यो, "म यो गर्न सक्छु।"'),
    ('She said, "I may come."', 'She said that she might come.', 'उसले भनिन्, "म आउन सक्छु।"'),
    ('He said, "I must go now."', 'He said that he had to go then.', 'उसले भन्यो, "म अहिले जानैपर्छ।"'),
    ('Ram said, "I am a student."', 'Ram said that he was a student.', 'रामले भन्यो, "म विद्यार्थी हुँ।"'),
    ('She said, "It is raining."', 'She said that it was raining.', 'उसले भनिन्, "पानी परिरहेको छ।"'),
    ('He said, "I was playing football."', 'He said that he had been playing football.', 'उसले भन्यो, "म फुटबल खेल्दै थिएँ।"'),
    ('She said, "I shall help you."', 'She said that she would help me.', 'उसले भनिन्, "म तिमीलाई सहयोग गर्नेछु।"'),
    ('He said, "I do not like tea."', 'He said that he did not like tea.', 'उसले भन्यो, "मलाई चिया मन पर्दैन।"'),
    ('She said, "I have been waiting for you."', 'She said that she had been waiting for me.', 'उसले भनिन्, "म तिमीलाई पर्खिरहेकी छु।"'),
    ('He said, "I will have finished by then."', 'He said that he would have finished by then.', 'उसले भन्यो, "म त्यतिबेलासम्म सक्नेछु।"'),
]
for direct, indirect, meaning in SPEECH:
    ds = [direct, indirect.replace('that', 'that that'), indirect.replace('was', 'is')]
    ds = [x for x in ds if x != indirect][:3]
    o = [indirect] + ds
    on = o[:]
    E('Direct & Indirect Speech', 'medium', f'Choose the indirect speech of: {direct}',
      f'{direct} को अप्रत्यक्ष कथन छान्नुहोस्।', o, on,
      f'The indirect speech is: {indirect}.', f'अप्रत्यक्ष कथन: {indirect} हो।')

# ---------- error spotting ----------
ERRORS = [
    ('He do not like tea.', 'He does not like tea.', 'do/does'),
    ('She go to school daily.', 'She goes to school daily.', 'go/goes'),
    ('They is playing football.', 'They are playing football.', 'is/are'),
    ('I has a pen.', 'I have a pen.', 'has/have'),
    ('He are a good boy.', 'He is a good boy.', 'are/is'),
    ('Ram and Shyam is friends.', 'Ram and Shyam are friends.', 'is/are'),
    ('Each of the boys are present.', 'Each of the boys is present.', 'are/is'),
    ('Neither of them were there.', 'Neither of them was there.', 'were/was'),
    ('One of my friends are coming.', 'One of my friends is coming.', 'are/is'),
    ('The number of students are fifty.', 'The number of students is fifty.', 'are/is'),
    ('She did not went to school.', 'She did not go to school.', 'went/go'),
    ('He did not ate rice.', 'He did not eat rice.', 'ate/eat'),
    ('I have went to Kathmandu.', 'I have gone to Kathmandu.', 'went/gone'),
    ('He has wrote a letter.', 'He has written a letter.', 'wrote/written'),
    ('She is more taller than me.', 'She is taller than me.', 'more taller/taller'),
    ('He is the most tallest boy.', 'He is the tallest boy.', 'most tallest/tallest'),
    ('This book is more better than that.', 'This book is better than that.', 'more better/better'),
    ('I am knowing him well.', 'I know him well.', 'am knowing/know'),
    ('She is having a car.', 'She has a car.', 'is having/has'),
    ('They are believing in God.', 'They believe in God.', 'are believing/believe'),
    ('He is senior than me.', 'He is senior to me.', 'than/to'),
    ('She is junior than him.', 'She is junior to him.', 'than/to'),
    ('I prefer tea than coffee.', 'I prefer tea to coffee.', 'than/to'),
    ('He is good in English.', 'He is good at English.', 'in/at'),
    ('She is interested on music.', 'She is interested in music.', 'on/in'),
    ('He depends in his father.', 'He depends on his father.', 'in/on'),
    ('I am afraid from dogs.', 'I am afraid of dogs.', 'from/of'),
    ('She is married with Ram.', 'She is married to Ram.', 'with/to'),
    ('He is angry on me.', 'He is angry with me.', 'on/with'),
    ('The teacher entered into the class.', 'The teacher entered the class.', 'into/(no preposition)'),
]
for wrong, right, note in ERRORS:
    ds = [wrong, right.replace('is', 'are'), right.replace('are', 'is')]
    ds = [x for x in ds if x != right][:3]
    o = [right] + ds
    on = o[:]
    E('Error Spotting', 'hard', f'Choose the correct sentence: (error in {note})',
      f'सही वाक्य छान्नुहोस्: (त्रुटि: {note})', o, on,
      f'The correct sentence is: {right}.', f'सही वाक्य: {right} हो।')

# ---------- question tags ----------
TAGS = [
    ('She is coming,', "isn't she", 'उनी आउँदैछिन्'), ('He is not coming,', 'is he', 'उनी आउँदैनन्'),
    ('They are playing,', "aren't they", 'उनीहरू खेल्दैछन्'), ('You are a student,', "aren't you", 'तिमी विद्यार्थी हौ'),
    ('Ram was there,', "wasn't he", 'राम त्यहाँ थियो'), ('She has finished,', "hasn't she", 'उसले सकिन्'),
    ('He can swim,', "can't he", 'उसले पौडिन सक्छ'), ('They will come,', "won't they", 'उनीहरू आउनेछन्'),
    ('She likes tea,', "doesn't she", 'उसलाई चिया मन पर्छ'), ('He goes to school,', "doesn't he", 'उसले विद्यालय जान्छ'),
    ('They went home,', "didn't they", 'उनीहरू घर गए'), ('You did it,', "didn't you", 'तिमीले यो गर्यौ'),
    ('I am right,', "aren't I", 'म सही छु'), ('Let us go,', 'shall we', 'जाऔँ'),
    ('She is not happy,', 'is she', 'उनी खुसी छैनन्'), ('He does not know,', 'does he', 'उसलाई थाहा छैन'),
    ('Open the door,', 'will you', 'ढोका खोल्नुहोस्'), ('Do not go,', 'will you', 'नजाऊ'),
    ('They have not come,', 'have they', 'उनीहरू आएका छैनन्'), ('Ram is a good boy,', "isn't he", 'राम राम्रो केटा हो'),
]
OPP = {"isn't she": 'is she', 'is he': "isn't he", "aren't they": 'are they', "aren't you": 'are you',
       "wasn't he": 'was he', "hasn't she": 'has she', "can't he": 'can he', "won't they": 'will they',
       "doesn't she": 'does she', "doesn't he": 'does he', "didn't they": 'did they', "didn't you": 'did you',
       "aren't I": 'am I', 'shall we': "shan't we", 'is she': "isn't she", 'does he': "doesn't he",
       'will you': "won't you", 'have they': "haven't they", "isn't he": 'is he'}
for stem, tag, meaning in TAGS:
    opp = OPP.get(tag, tag)
    cands = [opp, 'is it', 'do they', 'are we']
    ds = [x for x in cands if x.lower() != tag.lower()][:3]
    o = [tag] + ds
    on = o[:]
    E('Question Tags', 'medium', f'Choose the correct question tag: "{stem} ___?"',
      f'सही प्रश्न ट्याग छान्नुहोस्: "{stem} ___?"', o, on,
      f'The correct question tag is "{tag}".', f'सही प्रश्न ट्याग "{tag}" हो।')

n = em.write('expansion-r10-grammar.json')
print('GRAMMAR TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
