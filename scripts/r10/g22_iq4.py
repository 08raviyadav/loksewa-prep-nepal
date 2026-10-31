#!/usr/bin/env python3
"""R10 generator 22: IQ 4, big new patterns (~5,000 candidates). Letter
series (constant steps, squares, cubes, primes, Fibonacci positions),
number series (x2+2, x3-1, +squares, +cubes, alternating, n^2+-1, n^3+-1,
triangular, pentagonal), coding (A=1 sums new words, reverse-alphabet,
shift+reverse new words), odd-one-out letters & numbers, direction 4-step,
blood relations 2-step with names, pointing-to-photograph, linear seating
from permutations, syllogisms (some/all forms), alphabet sums of pairs."""
import sys, random, math
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
em = Emitter(bank, 'R10-IQ4')
rng = random.Random(71114)
EX = ['kharidar', 'nasu', 'section-officer', 'nrb-assistant', 'rbb', 'police', 'army', 'tsc-primary', 'tsc-secondary']
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHA_NE = ['ए','बी','सी','डी','ई','एफ','जी','एच','आई','जे','के','एल','एम','एन','ओ','पी','क्यू','आर','एस','टी','यू','भी','डब्ल्यू','एक्स','वाई','जेड']

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

def letter_opts(correct):
    ds = [c for c in ALPHA if c != correct]
    rng.shuffle(ds)
    o = [correct] + ds[:3]
    on = [ALPHA_NE[ALPHA.index(c)] for c in o]
    return o, on

def E(sub, diff, q, qn, o, on, expl, expln, idx=0):
    em.emit(EX, 'IQ & Reasoning', sub, diff, 2, q, qn, o, on, idx, expl, expln)

def letter_series(positions, desc, desc_ne):
    seq = [ALPHA[(p-1) % 26] for p in positions[:4]]
    nxt = ALPHA[(positions[4]-1) % 26]
    s = ', '.join(seq)
    o, on = letter_opts(nxt)
    E('Letter Series', 'hard', f'What is the next letter in the series: {s}, ...?',
      f'श्रेणी {s}, ... मा अर्को अक्षर कुन हो?', o, on,
      f'The letters follow {desc}, so the next letter is {nxt}.',
      f'अक्षरहरू {desc_ne} अनुसार छन्, त्यसैले अर्को अक्षर {nxt} हो।')

# ---------- letter series: constant steps ----------
for step in (4, 5, 6, 7):
    for start in range(1, 10):
        pos = [start + step*i for i in range(5)]
        letter_series(pos, f'a constant step of +{step}', f'+{dev(step)} को स्थिर चरण')
# ---------- letter series: squares positions ----------
for start in range(0, 3):
    pos = [(start+i+1)**2 for i in range(5)]
    letter_series(pos, 'square-number positions (1, 4, 9, 16, 25)', 'वर्ग सङ्ख्या स्थानहरू (१, ४, ९, १६, २५)')
# ---------- letter series: prime positions ----------
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
for start in range(0, 5):
    pos = primes[start:start+5]
    letter_series(pos, 'prime-number positions', 'अभाज्य सङ्ख्या स्थानहरू')
# ---------- letter series: Fibonacci positions ----------
fib = [1, 2, 3, 5, 8, 13, 21]
for start in range(0, 3):
    pos = fib[start:start+5]
    letter_series(pos, 'Fibonacci positions', 'फिबोनाच्ची स्थानहरू')
# ---------- letter series: cubes ----------
for start in range(0, 2):
    pos = [(start+i+1)**3 for i in range(5)]
    letter_series(pos, 'cube-number positions (1, 8, 27)', 'घन सङ्ख्या स्थानहरू (१, ८, २७)')

# ---------- number series: new patterns ----------
def series_q(seq, nxt):
    s = ', '.join(str(x) for x in seq)
    sn = ', '.join(dev_num(x) for x in seq)
    o, on, _ = num_opts(nxt, [nxt+1, nxt-1, nxt+2, nxt-2])
    E('Number Series', 'hard', f'What is the next number in the series: {s}, ...?', f'श्रेणी {sn}, ... मा अर्को सङ्ख्या कति हो?',
      o, on, f'The next term is {nxt}.', f'अर्को पद {dev_num(nxt)} हो।')
for n0 in range(2, 10):
    seq = [n0]
    for _ in range(3): seq.append(seq[-1]*2 + 2)
    series_q(seq, seq[-1]*2 + 2)
    seq = [n0]
    for _ in range(3): seq.append(seq[-1]*3 - 1)
    series_q(seq, seq[-1]*3 - 1)
    seq = [n0]
    for _ in range(3): seq.append(seq[-1] + len(seq)**2)
    series_q(seq, seq[-1] + 16)
for n0 in range(1, 12):
    seq = [i*i + 1 for i in range(n0, n0+4)]
    series_q(seq, (n0+4)**2 + 1)
    seq = [i*i - 1 for i in range(n0, n0+4)]
    series_q(seq, (n0+4)**2 - 1)
    seq = [i**3 + 1 for i in range(n0, n0+4)]
    series_q(seq, (n0+4)**3 + 1)
    seq = [i**3 - 1 for i in range(n0, n0+4)]
    series_q(seq, (n0+4)**3 - 1)
for n0 in range(1, 8):
    # triangular numbers T_n = n(n+1)/2
    seq = [(n0+i)*(n0+i+1)//2 for i in range(4)]
    series_q(seq, (n0+4)*(n0+5)//2)
    # pentagonal numbers P_n = n(3n-1)/2
    seq = [(n0+i)*(3*(n0+i)-1)//2 for i in range(4)]
    series_q(seq, (n0+4)*(3*(n0+4)-1)//2)
for n0 in range(2, 15):
    seq = [n0]
    for i in range(3):
        seq.append(seq[-1] + (5 if i % 2 == 0 else 3))
    series_q(seq, seq[-1] + 3)
    seq = [n0]
    for i in range(3):
        seq.append(seq[-1] - (2 if i % 2 == 0 else 4))
    series_q(seq, seq[-1] - 4)

# ---------- coding: A=1 sums, new words ----------
WORDS2 = ['ABATE','ABHOR','ABIDE','ABORT','ABSORB','ABSTRACT','ACCEPT','ACCESS','ACCUSE','ACTION',
          'ADMIRE','ADVICE','AFFAIR','AFRAID','AGENCY','AGENDA','AGREE','ALARM','ALBUM','ALERT',
          'ALIKE','ALIVE','ALLOW','ALONE','ALONG','ALOUD','ALPHA','ALTAR','ALTER','AMAZE','AMBER',
          'AMEND','AMONG','AMOUNT','AMUSE','ANGEL','ANGER','ANGLE','ANGRY','ANIMAL','ANKLE','ANNOY',
          'ANSWER','ANTHEM','ANXIETY','APART','APPEAL','APPEAR','APPLE','APPLY','APRIL','ARCH','ARENA',
          'ARGUE','ARISE','ARMY','AROUND','ARREST','ARRIVE','ARROW','ARTICLE','ARTIST','ASHAMED',
          'ASIDE','ASLEEP','ASPECT','ASSIST','ASSUME','ASSURE','ATHLETE','ATTACK','ATTEMPT','ATTEND',
          'ATTITUDE','AUDIO','AUDIT','AUGUST','AUTHOR','AUTUMN','AVENUE','AVERAGE','AVOID','AWAKE',
          'AWARD','AWARE','AWFUL','AXIOM','BABY','BACHELOR','BACK','BADGE','BAKE','BALANCE','BALL',
          'BAND','BANK','BAR','BARE','BARGAIN','BARRIER','BASE','BASIC','BASKET','BATH','BATTLE',
          'BEACH','BEAK','BEAM','BEAN','BEAR','BEARD','BEAST','BEAT','BEAUTY','BECOME','BED','BEE',
          'BEEF','BEER','BEFORE','BEG','BEGIN','BEHAVE','BEHIND','BELIEF','BELL','BELONG','BELOW',
          'BELT','BENCH','BEND','BENEFIT','BERRY','BESIDE','BEST','BET','BETTER','BETWEEN','BEYOND',
          'BIBLE','BID','BIG','BILL','BIND','BIRD','BIRTH','BIT','BITE','BITTER','BLACK','BLADE',
          'BLAME','BLANK','BLAST','BLEED','BLESS','BLIND','BLOCK','BLOOD','BLOW','BLUE','BOARD',
          'BOAT','BODY','BOIL','BOLD','BOLT','BOMB','BOND','BONE','BOOK','BOOST','BOOT','BORDER',
          'BORE','BORN','BORROW','BOSS','BOTH','BOTTLE','BOTTOM','BOUGHT','BOUND','BOWL','BOX',
          'BOY','BRAIN','BRANCH','BRAND','BRAVE','BREAD','BREAK','BREATH','BREEZE','BRICK','BRIDE',
          'BRIDGE','BRIEF','BRIGHT','BRING','BROAD','BROKE','BROTHER','BROWN','BRUSH','BUBBLE',
          'BUCKET','BUDGET','BUILD','BULB','BULK','BULLET','BUNCH','BURDEN','BURN','BURST','BURY',
          'BUS','BUSH','BUSINESS','BUSY','BUTTER','BUTTON','BUY','BUYER','BYE','CABIN','CABLE',
          'CAKE','CALCULATE','CALENDAR','CALL','CALM','CAMEL','CAMERA','CAMP','CANAL','CANCEL',
          'CANCER','CANDIDATE','CANDLE','CANDY','CAPABLE','CAPACITY','CAPITAL','CAPTAIN','CAPTURE',
          'CAR','CARBON','CARD','CARE','CAREER','CAREFUL','CARPET','CARRY','CART','CASE','CASH',
          'CAST','CASTLE','CAT','CATCH','CATTLE','CAUSE','CEASE','CEILING','CELEBRATE','CELL',
          'CENTRE','CENTURY','CERTAIN','CHAIN','CHAIR','CHALK','CHANCE','CHANGE','CHANNEL','CHAOS',
          'CHAPTER','CHARGE','CHARITY','CHART','CHASE','CHEAP','CHECK','CHEESE','CHEF','CHEMICAL',
          'CHEST','CHICKEN','CHIEF','CHILD','CHILL','CHIP','CHOICE','CHOOSE','CHURCH','CIRCLE',
          'CITIZEN','CITY','CIVIL','CLAIM','CLASS','CLAUSE','CLEAN','CLEAR','CLERK','CLEVER',
          'CLICK','CLIENT','CLIMATE','CLIMB','CLOCK','CLOSE','CLOTH','CLOUD','CLUB','COACH',
          'COAL','COAST','CODE','COFFEE','COIN','COLD','COLLEGE','COLOUR','COMB','COME','COMFORT',
          'COMMAND','COMMENT','COMMON','COMPACT','COMPANY','COMPARE','COMPETE','COMPLETE','COMPLEX',
          'COMPOSE','CONCERT','CONCLUDE','CONDITION','CONFIRM','CONFLICT','CONGRESS','CONNECT',
          'CONSENT','CONSIDER','CONSIST','CONSTANT','CONTACT','CONTAIN','CONTENT','CONTEST',
          'CONTEXT','CONTRACT','CONTRAST','CONTROL','CONVERT','COOK','COOL','COPE','COPY','CORE',
          'CORN','CORNER','CORRECT','COST','COTTON','COUGH','COULD','COUNT','COUNTRY','COUNTY',
          'COUPLE','COURAGE','COURSE','COURT','COVER','CRACK','CRAFT','CRASH','CRAZY','CREAM',
          'CREATE','CREW','CRICKET','CRIME','CRISIS','CRITICAL','CROP','CROSS','CROWD','CRUCIAL',
          'CRUEL','CRY','CULTURE','CUP','CURE','CURIOUS','CURRENT','CURTAIN','CURVE','CUSTOM',
          'CUT','CYCLE','DAILY','DAIRY','DAMAGE','DANCE','DANGER','DARE','DARK','DATA','DATE',
          'DAUGHTER','DAWN','DEAD','DEAL','DEAR','DEATH','DEBATE','DEBT','DECADE','DECIDE','DECISION',
          'DECLARE','DEEP','DEER','DEFEAT','DEFENCE','DEFICIT','DEGREE','DELAY','DELIGHT','DEMAND',
          'DEMOCRACY','DENY','DEPEND','DEPOSIT','DEPTH','DERIVE','DESCRIBE','DESERT','DESIGN',
          'DESIRE','DESK','DESPITE','DESTROY','DETAIL','DETECT','DETERMINE','DEVELOP','DEVICE',
          'DEVOTE','DIAGRAM','DIAL','DIAMOND','DIARY','DICE','DIE','DIET','DIFFER','DIG','DINNER',
          'DIRECT','DIRTY','DISABLE','DISASTER','DISCIPLINE','DISCOUNT','DISCOVER','DISCUSS',
          'DISEASE','DISH','DISK','DISPLAY','DISTANCE','DISTINCT','DISTRICT','DIVIDE','DIVORCE',
          'DOCTOR','DOG','DOLL','DOMAIN','DONATE','DOOR','DOSE','DOUBLE','DOUBT','DOVE','DOWN',
          'DOZEN','DRAFT','DRAG','DRAIN','DRAMA','DRAW','DREAM','DRESS','DRIFT','DRILL','DRINK',
          'DRIVE','DROP','DROWN','DRUM','DRY','DUCK','DUE','DUST','DUTY','DWELL','EACH','EAGER',
          'EAGLE','EAR','EARLY','EARN','EARTH','EASE','EAST','EASY','EAT','ECHO','EDGE','EDIT',
          'EDUCATION','EFFECT','EFFORT','EGG','EITHER','ELBOW','ELDER','ELECT','ELEGANT','ELEMENT',
          'ELIGIBLE','ELSE','EMBARRASS','EMERGE','EMPHASIS','EMPLOY','EMPTY','ENABLE','ENCOURAGE',
          'END','ENEMY','ENERGY','ENGAGE','ENGINE','ENJOY','ENORMOUS','ENOUGH','ENSURE','ENTER',
          'ENTIRE','ENTRY','ENVIRONMENT','EPISODE','EQUAL','EQUIP','ERROR','ESCAPE','ESPECIALLY',
          'ESSAY','ESSENTIAL','ESTABLISH','ESTATE','ESTIMATE','ETHICS','EVEN','EVENING','EVENT',
          'EVERY','EVIDENCE','EVIL','EXACT','EXAM','EXAMPLE','EXCEED','EXCELLENT','EXCEPT','EXCESS',
          'EXCHANGE','EXCITE','EXCUSE','EXERCISE','EXHAUST','EXIST','EXIT','EXPAND','EXPECT',
          'EXPENSE','EXPERT','EXPLAIN','EXPLODE','EXPLORE','EXPORT','EXPOSE','EXPRESS','EXTEND',
          'EXTENT','EXTRA','EXTREME','EYE','FACE','FACT','FACTOR','FAIL','FAIR','FAITH','FALL',
          'FALSE','FAME','FAMILY','FAMOUS','FAN','FANCY','FAR','FARM','FASHION','FAST','FAT',
          'FATE','FATHER','FAULT','FAVOUR','FEAR','FEATURE','FEBRUARY','FEDERAL','FEE','FEED',
          'FEEL','FELLOW','FEMALE','FENCE','FESTIVAL','FEW','FICTION','FIELD','FIERCE','FIFTEEN',
          'FIFTH','FIFTY','FIGHT','FIGURE','FILE','FILL','FILM','FINAL','FINANCE','FIND','FINE',
          'FINGER','FINISH','FIRE','FIRM','FIRST','FISH','FIT','FIX','FLAG','FLAME','FLASH','FLAT',
          'FLAVOUR','FLEET','FLESH','FLIGHT','FLOAT','FLOOD','FLOOR','FLOUR','FLOW','FLOWER','FLUENT',
          'FLUID','FLY','FOCUS','FOG','FOLD','FOLK','FOLLOW','FOOD','FOOL','FOOT','FOR','FORCE',
          'FOREIGN','FOREST','FORGET','FORK','FORM','FORMAL','FORMER','FORTUNE','FORTY','FORWARD',
          'FOUND','FOUR','FRAME','FREE','FREEZE','FREQUENT','FRESH','FRIEND','FRONT','FROST',
          'FRUIT','FUEL','FULL','FUN','FUNCTION','FUND','FUNNY','FUR','FUTURE','GAIN','GAME',
          'GAP','GARDEN','GARLIC','GAS','GATE','GATHER','GAVE','GENERAL','GENTLE','GENTLEMAN',
          'GEOGRAPHY','GERM','GET','GIFT','GIRL','GIVE','GLAD','GLASS','GLEAM','GLIDE','GLOBAL',
          'GLORY','GLOVE','GOAL','GOAT','GOLD','GOLF','GOOD','GOVERN','GRACE','GRADE','GRAIN',
          'GRAMMAR','GRAND','GRANT','GRAPE','GRAPH','GRASP','GRASS','GRATEFUL','GRAVE','GREAT',
          'GREEN','GREET','GREY','GRIEF','GRILL','GRIP','GROAN','GROUP','GROW','GROWTH','GUARD',
          'GUESS','GUEST','GUIDE','GUILT','GUITAR','GULF','GUN','HABIT','HAIR','HALF','HALL',
          'HAND','HANDLE','HANG','HAPPY','HARBOR','HARD','HARM','HARVEST','HAT','HATE','HAUNT',
          'HAVE','HEAD','HEAL','HEALTH','HEAR','HEART','HEAT','HEAVEN','HEAVY','HEIGHT','HELD',
          'HELICOPTER','HELL','HELLO','HELP','HENCE','HERB','HERE','HERO','HIDE','HIGH','HILL',
          'HINT','HIRE','HISTORY','HIT','HOLD','HOLE','HOLIDAY','HOLLOW','HOLY','HOME','HONEST',
          'HONOR','HOOK','HOPE','HORIZON','HORN','HORSE','HOSPITAL','HOST','HOT','HOTEL','HOUR',
          'HOUSE','HOW','HUGE','HUMAN','HUMOUR','HUNGER','HUNT','HURRY','HURT','HUSBAND','HUT',
          'ICE','IDEA','IDEAL','IDENTIFY','IDLE','IF','IGNORE','ILL','IMAGE','IMAGINE','IMPACT',
          'IMPLY','IMPORT','IMPORTANT','IMPOSE','IMPROVE','INCH','INCOME','INDEED','INDEX','INDIA',
          'INDICATE','INDOOR','INDUSTRY','INFANT','INFLATION','INFLUENCE','INFORM','INJURY','INK',
          'INNER','INPUT','INSECT','INSIDE','INSIST','INSPECT','INSTANT','INSTEAD','INSTRUMENT',
          'INSULT','INTELLIGENT','INTEND','INTEREST','INTERNATIONAL','INTERNET','INTERPRET',
          'INTERRUPT','INTERVAL','INTERVIEW','INTRODUCE','INVENT','INVEST','INVITE','INVOLVE',
          'IRON','ISLAND','ISSUE','ITEM','ITSELF','JACKET','JAIL','JANUARY','JAZZ','JEALOUS',
          'JEANS','JEEP','JELLY','JEWEL','JOB','JOIN','JOINT','JOKE','JOURNAL','JOURNEY','JOY',
          'JUDGE','JUICE','JULY','JUMP','JUNE','JUNIOR','JURY','JUST','JUSTICE','KEEP','KEY',
          'KICK','KID','KILL','KIND','KING','KISS','KITCHEN','KNEE','KNIFE','KNOCK','KNOW',
          'KNOWLEDGE','LABOUR','LADDER','LADY','LAKE','LAMP','LAND','LANGUAGE','LAP','LARGE',
          'LAST','LATE','LAUGH','LAUNCH','LAW','LAWYER','LAY','LEAD','LEAF','LEAGUE','LEARN',
          'LEAST','LEATHER','LEAVE','LECTURE','LEFT','LEG','LEGAL','LEMON','LEND','LENGTH',
          'LESS','LESSON','LET','LETTER','LEVEL','LIBRARY','LICENSE','LIE','LIFE','LIFT','LIGHT',
          'LIKE','LIMIT','LINE','LINK','LION','LIP','LIQUID','LIST','LISTEN','LITERATURE','LITTLE',
          'LIVE','LOAD','LOAN','LOCAL','LOCK','LOGIC','LONELY','LONG','LOOK','LOOSE','LORD','LOSE',
          'LOSS','LOT','LOUD','LOVE','LOW','LOYAL','LUCK','LUGGAGE','LUNCH','LUNG','MACHINE',
          'MAD','MAGAZINE','MAGIC','MAIL','MAIN','MAJOR','MAKE','MALE','MALL','MAN','MANAGE',
          'MANNER','MANY','MAP','MARCH','MARGIN','MARK','MARKET','MARRIAGE','MARRY','MASK',
          'MASS','MASTER','MATCH','MATERIAL','MATH','MATTER','MAXIMUM','MAY','MAYOR','MEAL',
          'MEAN','MEASURE','MEAT','MEDIA','MEDICAL','MEDICINE','MEDIUM','MEET','MEETING','MEMBER',
          'MEMORY','MENTAL','MENTION','MENU','MERE','MESSAGE','METAL','METHOD','MIDDLE','MIGHT',
          'MILD','MILE','MILK','MIND','MINE','MINIMUM','MINISTER','MINOR','MINUTE','MIRROR','MISS',
          'MISTAKE','MIX','MOBILE','MODE','MODEL','MODERN','MODEST','MOMENT','MONDAY','MONEY',
          'MONITOR','MONKEY','MONTH','MOON','MORAL','MORE','MORNING','MOST','MOTHER','MOTION',
          'MOTOR','MOUNTAIN','MOUSE','MOUTH','MOVE','MOVIE','MUCH','MUD','MULTIPLE','MURDER',
          'MUSEUM','MUSIC','MUST','MUTUAL','MYSELF','MYSTERY','NAIL','NAME','NARROW','NATION',
          'NATIVE','NATURAL','NATURE','NAVY','NEAR','NEAT','NECESSARY','NECK','NEED','NEEDLE',
          'NEGATIVE','NEGLECT','NEIGHBOUR','NEITHER','NEPHEW','NERVE','NET','NETWORK','NEVER',
          'NEW','NEWS','NEXT','NICE','NIGHT','NINE','NO','NOBLE','NOBODY','NOD','NOISE','NONE',
          'NOON','NOR','NORMAL','NORTH','NOSE','NOTE','NOTHING','NOTICE','NOTION','NOVEL','NOW',
          'NUMBER','NURSE','NUT','OBJECT','OBLIGE','OBSERVE','OBTAIN','OBVIOUS','OCCASION','OCCUPY',
          'OCEAN','OCTOBER','ODD','OF','OFF','OFFER','OFFICE','OFFICER','OFFICIAL','OFTEN','OIL',
          'OLD','ON','ONCE','ONE','ONLY','ONTO','OPEN','OPERA','OPINION','OPPORTUNITY','OPPOSE',
          'OPTION','OR','ORAL','ORANGE','ORDER','ORDINARY','ORGAN','ORIGIN','OTHER','OUGHT','OUR',
          'OUT','OUTCOME','OUTDOOR','OUTER','OUTPUT','OUTSIDE','OVER','OVERCOME','OWE','OWN','OWNER',
          'OX','PACK','PAGE','PAIN','PAINT','PAIR','PALACE','PALE','PAN','PANEL','PANIC','PAPER',
          'PARADE','PARENT','PARK','PART','PARTICULAR','PARTNER','PARTY','PASS','PASSAGE','PASSENGER',
          'PASSION','PAST','PATH','PATIENCE','PATIENT','PATTERN','PAUSE','PAY','PEACE','PEAK','PEAR',
          'PEN','PENCIL','PEOPLE','PEPPER','PER','PERFECT','PERFORM','PERHAPS','PERIOD','PERMANENT',
          'PERMIT','PERSON','PERSONAL','PET','PHASE','PHONE','PHOTO','PHRASE','PHYSICAL','PIANO',
          'PICK','PICTURE','PIECE','PIG','PILE','PILOT','PIN','PINK','PIPE','PITCH','PITY','PLACE',
          'PLAIN','PLAN','PLANE','PLANET','PLANT','PLASTIC','PLATE','PLAY','PLEASANT','PLEASE',
          'PLEASURE','PLENTY','PLOT','PLUS','POCKET','POEM','POET','POINT','POLICE','POLICY',
          'POLITE','POLITICAL','POLLUTION','POOL','POOR','POPULAR','POPULATION','PORT','POSE',
          'POSITION','POSITIVE','POSSESS','POSSIBLE','POST','POT','POTATO','POUND','POUR','POVERTY',
          'POWDER','POWER','PRACTICAL','PRACTICE','PRAISE','PRAY','PRECISE','PREDICT','PREFER',
          'PREPARE','PRESENT','PRESIDENT','PRESS','PRESSURE','PRETTY','PREVENT','PRICE','PRIDE',
          'PRIEST','PRIMARY','PRIME','PRINCE','PRINCIPLE','PRINT','PRIOR','PRISON','PRIVATE',
          'PRIZE','PROBABLY','PROBLEM','PROCEED','PROCESS','PRODUCE','PROFESSION','PROFILE',
          'PROFIT','PROGRAM','PROGRESS','PROJECT','PROMISE','PROMPT','PROOF','PROPER','PROPERTY',
          'PROPOSE','PROTECT','PROUD','PROVE','PROVIDE','PUBLIC','PUBLISH','PULL','PULSE','PUMP',
          'PUNISH','PUPIL','PURCHASE','PURE','PURPOSE','PURSUE','PUSH','PUT','QUALITY','QUANTITY',
          'QUARTER','QUEEN','QUESTION','QUICK','QUIET','QUITE','RACE','RADIO','RAIL','RAIN','RAISE',
          'RANGE','RANK','RAPID','RARE','RATE','RATHER','RAW','REACH','READ','READY','REAL',
          'REALISE','REALLY','REASON','RECEIVE','RECENT','RECIPE','RECORD','RED','REDUCE','REFER',
          'REFLECT','REFORM','REFUSE','REGARD','REGION','REGULAR','REJECT','RELATE','RELATION',
          'RELAX','RELEASE','RELEVANT','RELIABLE','RELIEF','RELIGION','RELY','REMAIN','REMARK',
          'REMEMBER','REMIND','REMOTE','REMOVE','RENT','REPAIR','REPEAT','REPLACE','REPLY','REPORT',
          'REPRESENT','REQUEST','REQUIRE','RESCUE','RESEARCH','RESERVE','RESIST','RESOLVE','RESORT',
          'RESOURCE','RESPECT','RESPOND','REST','RESULT','RETAIL','RETIRE','RETURN','REVEAL',
          'REVIEW','REWARD','RICE','RICH','RIDE','RIDICULOUS','RIGHT','RING','RISE','RISK','RIVER',
          'ROAD','ROAR','ROAST','ROB','ROCK','ROLE','ROLL','ROOF','ROOM','ROOT','ROPE','ROSE',
          'ROUGH','ROUND','ROUTE','ROW','ROYAL','RUB','RUDE','RUIN','RULE','RUN','RURAL','RUSH',
          'SACRED','SACRIFICE','SAD','SAFE','SAIL','SALARY','SALE','SALT','SAME','SAMPLE','SAND',
          'SATISFY','SAVE','SAY','SCALE','SCAN','SCARE','SCENE','SCHEME','SCHOOL','SCIENCE','SCOPE',
          'SCORE','SEA','SEAL','SEARCH','SEASON','SEAT','SECOND','SECRET','SECTION','SECTOR','SECURE',
          'SEE','SEED','SEEK','SEEM','SELECT','SELF','SELL','SEND','SENIOR','SENSE','SENTENCE',
          'SEPARATE','SEPTEMBER','SERIES','SERIOUS','SERVE','SERVICE','SESSION','SET','SETTLE',
          'SEVEN','SEVERAL','SEVERE','SEW','SHADE','SHADOW','SHAKE','SHALL','SHAME','SHAPE','SHARE',
          'SHARP','SHAVE','SHE','SHEEP','SHEET','SHELF','SHELL','SHELTER','SHIFT','SHINE','SHIP',
          'SHIRT','SHOCK','SHOE','SHOOT','SHOP','SHORE','SHORT','SHOT','SHOULD','SHOULDER','SHOUT',
          'SHOW','SHOWER','SHUT','SHY','SICK','SIDE','SIGHT','SIGN','SIGNAL','SILENCE','SILK',
          'SILLY','SILVER','SIMILAR','SIMPLE','SINCE','SING','SINGLE','SINK','SIR','SISTER','SIT',
          'SITE','SITUATION','SIX','SIZE','SKILL','SKIN','SKIRT','SKY','SLEEP','SLICE','SLIDE',
          'SLIGHT','SLIM','SLIP','SLOPE','SLOW','SMALL','SMART','SMELL','SMILE','SMOKE','SMOOTH',
          'SNAKE','SNOW','SO','SOAP','SOCIAL','SOCIETY','SOCK','SOFT','SOIL','SOLDIER','SOLID',
          'SOLUTION','SOLVE','SOME','SON','SONG','SOON','SORRY','SORT','SOUL','SOUND','SOUP',
          'SOURCE','SOUTH','SPACE','SPARE','SPEAK','SPECIAL','SPEECH','SPEED','SPELL','SPEND',
          'SPIRIT','SPITE','SPLIT','SPOIL','SPOKE','SPORT','SPOT','SPREAD','SPRING','SQUARE','STAFF',
          'STAGE','STAIR','STAMP','STAND','STAR','START','STATE','STATION','STAY','STEADY','STEAL',
          'STEAM','STEEL','STEEP','STEER','STEP','STICK','STILL','STING','STOCK','STOMACH','STONE',
          'STOOD','STOP','STORE','STORM','STORY','STOVE','STRAIGHT','STRANGE','STRATEGY','STREAM',
          'STREET','STRENGTH','STRESS','STRETCH','STRICT','STRIKE','STRING','STRIP','STRONG',
          'STRUGGLE','STUDENT','STUDIO','STUDY','STUFF','STUPID','STYLE','SUBJECT','SUBMIT',
          'SUBSTANCE','SUBURB','SUCCEED','SUCCESS','SUCH','SUDDEN','SUFFER','SUGAR','SUGGEST',
          'SUIT','SUMMER','SUN','SUPER','SUPPLY','SUPPORT','SUPPOSE','SUPREME','SURE','SURFACE',
          'SURPRISE','SURROUND','SURVEY','SURVIVE','SUSPECT','SWALLOW','SWEAR','SWEAT','SWEEP',
          'SWEET','SWIM','SWING','SWITCH','SYMBOL','SYMPATHY','SYSTEM','TABLE','TAIL','TAKE','TALE',
          'TALK','TALL','TANK','TAP','TAPE','TARGET','TASK','TASTE','TAX','TEA','TEACH','TEAM',
          'TEAR','TECHNICAL','TEEN','TELEPHONE','TELEVISION','TELL','TEMPERATURE','TEMPLE','TEN',
          'TEND','TENT','TERM','TERRIBLE','TEST','THAN','THANK','THAT','THE','THEATRE','THEIR',
          'THEM','THEME','THEMSELVES','THEN','THEORY','THERE','THESE','THEY','THICK','THIN','THING',
          'THINK','THIRD','THIRSTY','THIRTEEN','THIRTY','THIS','THOROUGH','THOSE','THOUGH','THOUGHT',
          'THOUSAND','THREAD','THREAT','THREE','THROAT','THROUGH','THROW','THUMB','THURSDAY','THUS',
          'TICKET','TIDE','TIE','TIGHT','TILL','TIME','TIN','TINY','TIP','TIRED','TITLE','TO',
          'TOBACCO','TODAY','TOE','TOGETHER','TOILET','TOMATO','TOMORROW','TONE','TONGUE','TONIGHT',
          'TOO','TOOL','TOOTH','TOP','TOPIC','TOTAL','TOUCH','TOUGH','TOUR','TOWARD','TOWEL','TOWER',
          'TOWN','TOY','TRACE','TRACK','TRADE','TRADITION','TRAFFIC','TRAIN','TRANSFER','TRANSLATE',
          'TRANSPORT','TRAP','TRAVEL','TREAT','TREE','TREND','TRIAL','TRIBE','TRICK','TRIP','TROOP',
          'TROUBLE','TRUCK','TRUE','TRUST','TRUTH','TRY','TUBE','TUESDAY','TUNE','TURN','TWICE',
          'TWIN','TYPE','TYPICAL','UGLY','ULTIMATE','UNCLE','UNDER','UNDERSTAND','UNION','UNIT',
          'UNITED','UNIVERSE','UNIVERSITY','UNLESS','UNTIL','UP','UPON','UPPER','UPSET','URBAN',
          'URGE','USE','USED','USEFUL','USUAL','VACATION','VALLEY','VALUABLE','VALUE','VAN','VARIOUS',
          'VARY','VAST','VEGETABLE','VEHICLE','VENTURE','VERB','VERY','VESSEL','VETERAN','VICTIM',
          'VICTORY','VIDEO','VIEW','VILLAGE','VIOLENCE','VIRGIN','VIRTUE','VISIBLE','VISION','VISIT',
          'VISITOR','VITAL','VOICE','VOLUME','VOTE','VOYAGE','WAGE','WAIT','WAKE','WALK','WALL',
          'WANDER','WANT','WAR','WARM','WARN','WASH','WASTE','WATCH','WATER','WAVE','WAY','WE',
          'WEAK','WEALTH','WEAPON','WEAR','WEATHER','WEAVE','WEB','WEDDING','WEEK','WEEKEND','WEIGH',
          'WELCOME','WELL','WEST','WET','WHAT','WHEAT','WHEEL','WHEN','WHERE','WHETHER','WHICH',
          'WHILE','WHISPER','WHITE','WHO','WHOLE','WHOM','WHOSE','WHY','WIDE','WIDOW','WIFE','WILD',
          'WILL','WIN','WIND','WINDOW','WINE','WING','WINNER','WINTER','WIPE','WIRE','WISE','WISH',
          'WITH','WITHIN','WITHOUT','WITNESS','WOLF','WOMAN','WONDER','WOOD','WOOL','WORD','WORK',
          'WORLD','WORRY','WORTH','WOUND','WRAP','WRITE','WRITER','WRONG','YARD','YEAR','YELLOW',
          'YES','YESTERDAY','YET','YIELD','YOU','YOUNG','YOUR','YOUTH','ZERO','ZONE','ZOOM']
def asum(w):
    return sum(ALPHA.index(c)+1 for c in w)
for w in WORDS2:
    s = asum(w)
    o, on, _ = num_opts(s, [s+5, s-5, s+10, s-10])
    E('Coding', 'medium', f'If A = 1, B = 2, ..., Z = 26, what is the sum of the letters of the word "{w}"?',
      f'यदि A = १, B = २, ..., Z = २६ हो भने "{w}" शब्दका अक्षरहरूको योग कति हुन्छ?', o, on,
      f'The sum of the letters of "{w}" is {s}.', f'"{w}" शब्दका अक्षरहरूको योग {dev_num(s)} हो।')
# coding: reverse-alphabet (A<->Z)
def rev_alpha(w):
    return ''.join(ALPHA[25 - ALPHA.index(c)] for c in w)
for w in ['NEPAL','KATHMANDU','POKHARA','SCHOOL','BOOK','HOUSE','WATER','RIVER','TIGER','FLOWER',
          'GARDEN','MARKET','FRIEND','MOTHER','DOCTOR','HAPPY','BRAVE','APPLE','MANGO','GOLD',
          'SILVER','MUSIC','STORY','PEACE','TRUTH','LIGHT','DREAM','HOPE','LOVE','LIFE']:
    code = rev_alpha(w)
    w2 = rng.choice([x for x in ['NEPAL','SCHOOL','BOOK','HOUSE','WATER','TIGER','FLOWER','GARDEN','FRIEND','MOTHER','DOCTOR','HAPPY','APPLE','GOLD','MUSIC','STORY','PEACE','LIGHT','DREAM','LOVE'] if x != w])
    c2 = rev_alpha(w2)
    ds = rng.sample([x for x in ['NEPAL','SCHOOL','BOOK','HOUSE','WATER','TIGER','FLOWER','GARDEN','FRIEND','MOTHER','DOCTOR','HAPPY','APPLE','GOLD','MUSIC','STORY','PEACE','LIGHT','DREAM','LOVE'] if x not in (w, w2)], 3)
    o = [w2] + ds
    on = o[:]
    E('Coding', 'hard', f'In a certain code, {w} is written as {code}. Which word is written as {c2} in the same code?',
      f'एउटा कोडमा {w} लाई {code} लेखिन्छ। त्यही कोडमा {c2} भनेर कुन शब्द लेखिन्छ?', o, on,
      f'Each letter is replaced by its opposite in the alphabet (A<->Z), so {c2} stands for {w2}.',
      f'प्रत्येक अक्षरलाई वर्णमालामा विपरीत अक्षरले बदलिन्छ (A<->Z), त्यसैले {c2} भनेको {w2} हो।')

# ---------- odd-one-out letters ----------
VOW = ['A', 'E', 'I', 'O', 'U']
CONS = [c for c in ALPHA if c not in VOW]
for _ in range(60):
    v = rng.choice(VOW)
    ds = rng.sample(CONS, 3)
    o = [v] + ds
    rng.shuffle(o)
    on = [ALPHA_NE[ALPHA.index(x)] for x in o]
    idx = o.index(v)
    E('Odd One Out', 'easy', 'Which is the odd one out?', 'निम्नमध्ये फरक कुन हो?', o, on,
      f'{v} is a vowel; the others are consonants.', f'{v} स्वर हो; अरू व्यञ्जन हुन्।', idx=idx)
for _ in range(60):
    c = rng.choice(CONS)
    ds = rng.sample(VOW, 3)
    o = [c] + ds
    rng.shuffle(o)
    on = [ALPHA_NE[ALPHA.index(x)] for x in o]
    idx = o.index(c)
    E('Odd One Out', 'easy', 'Which is the odd one out?', 'निम्नमध्ये फरक कुन हो?', o, on,
      f'{c} is a consonant; the others are vowels.', f'{c} व्यञ्जन हो; अरू स्वर हुन्।', idx=idx)
# curved vs straight lines
CURVED = ['C', 'O', 'S', 'U']
STRAIGHT = ['A', 'E', 'F', 'H', 'I', 'K', 'L', 'M', 'N', 'T', 'V', 'W', 'X', 'Y', 'Z']
for _ in range(40):
    c = rng.choice(CURVED)
    ds = rng.sample(STRAIGHT, 3)
    o = [c] + ds
    rng.shuffle(o)
    on = [ALPHA_NE[ALPHA.index(x)] for x in o]
    idx = o.index(c)
    E('Odd One Out', 'medium', 'Which letter is made only of curved lines?', 'कुन अक्षर केवल घुमाउरो रेखाबाट बनेको छ?', o, on,
      f'{c} is made only of curved lines.', f'{c} केवल घुमाउरो रेखाबाट बनेको छ।', idx=idx)

# ---------- direction 4-step ----------
for _ in range(120):
    # walk in 4 directions with distances; net displacement via Pythagoras
    legs = []
    x, y = 0, 0
    for _ in range(4):
        d = rng.choice([3, 4, 5, 6, 8, 10, 12])
        direc = rng.choice(['north', 'south', 'east', 'west'])
        legs.append((d, direc))
        if direc == 'north': y += d
        elif direc == 'south': y -= d
        elif direc == 'east': x += d
        else: x -= d
    dist2 = x*x + y*y
    dist = int(math.isqrt(dist2))
    if dist*dist != dist2 or dist == 0: continue
    leg_s = '; '.join(f'{d} km {dir}' for d, dir in legs)
    DIR_NE = {'north': 'उत्तर', 'south': 'दक्षिण', 'east': 'पूर्व', 'west': 'पश्चिम'}
    leg_sn = '; '.join(f'{dev(d)} किमी {DIR_NE[dir]}' for d, dir in legs)
    o, on, _ = num_opts(dist, [dist+1, dist-1, dist+2, dist-2])
    E('Direction Sense', 'hard', f'A man walks: {leg_s}. How far is he from his starting point?',
      f'एक मानिस हिँड्छ: {leg_sn}। उनी सुरुको बिन्दुबाट कति टाढा छन्?',
      o, on, f'His net displacement is {dist} km from the start.', f'उनको खुद विस्थापन सुरुबाट {dev_num(dist)} किमी छ।')

# ---------- blood relations 2-step with names ----------
NAMES_M = ['Ram', 'Hari', 'Shyam', 'Mohan', 'Binod', 'Suresh', 'Ramesh', 'Dinesh']
NAMES_F = ['Sita', 'Gita', 'Rita', 'Sarita', 'Sunita', 'Mina', 'Kamala', 'Laxmi']
REL2 = [
    ('{a} is the father of {b}. How is {a} related to {b}?', '{a} {b} का बुबा हुन्। {a} {b} का के हुन्?', 'Father', 'बुबा', 'Uncle', 'काका', 'Brother', 'दाजु', 'Grandfather', 'हजुरबुबा'),
    ('{a} is the mother of {b}. How is {a} related to {b}?', '{a} {b} की आमा हुन्। {a} {b} की के हुन्?', 'Mother', 'आमा', 'Aunt', 'फुपू', 'Sister', 'दिदी', 'Grandmother', 'हजुरआमा'),
    ('{a} is the brother of {b}. How is {a} related to {b}?', '{a} {b} का भाइ हुन्। {a} {b} का के हुन्?', 'Brother', 'भाइ', 'Father', 'बुबा', 'Uncle', 'काका', 'Son', 'छोरा'),
    ('{a} is the sister of {b}. How is {a} related to {b}?', '{a} {b} की बहिनी हुन्। {a} {b} की के हुन्?', 'Sister', 'बहिनी', 'Mother', 'आमा', 'Aunt', 'फुपू', 'Daughter', 'छोरी'),
    ('{a} is the son of {b}. How is {a} related to {b}?', '{a} {b} का छोरा हुन्। {a} {b} का के हुन्?', 'Son', 'छोरा', 'Brother', 'भाइ', 'Nephew', 'भतिजा', 'Grandson', 'नाति'),
    ('{a} is the daughter of {b}. How is {a} related to {b}?', '{a} {b} की छोरी हुन्। {a} {b} की के हुन्?', 'Daughter', 'छोरी', 'Sister', 'बहिनी', 'Niece', 'भतिजी', 'Granddaughter', 'नातिनी'),
]
for _ in range(150):
    q, qn, a, an, d1, d1n, d2, d2n, d3, d3n = rng.choice(REL2)
    a_n, b_n = rng.sample(NAMES_M + NAMES_F, 2)
    E('Blood Relations', 'easy', q.format(a=a_n, b=b_n), qn.format(a=a_n, b=b_n),
      [a, d1, d2, d3], [an, d1n, d2n, d3n], f'The answer is {a}.', f'उत्तर {an} हो।')

# ---------- pointing to a photograph ----------
PHOTO = [
    ('Pointing to a photograph, Ram says, "She is the daughter of my father." Who is she?', 'एउटा तस्बिरतर्फ औँल्याउँदै राम भन्छन्, "उनी मेरो बुबाकी छोरी हुन्।" उनी को हुन्?', 'Sister', 'बहिनी', 'Mother', 'आमा', 'Daughter', 'छोरी', 'Aunt', 'फुपू'),
    ('Pointing to a photograph, Sita says, "He is the son of my mother." Who is he?', 'एउटा तस्बिरतर्फ औँल्याउँदै सीता भन्छिन्, "उनी मेरी आमाका छोरा हुन्।" उनी को हुन्?', 'Brother', 'भाइ', 'Father', 'बुबा', 'Son', 'छोरा', 'Uncle', 'काका'),
    ('Pointing to a photograph, Hari says, "He is my father\'s only son." Who is he?', 'एउटा तस्बिरतर्फ औँल्याउँदै हरि भन्छन्, "उनी मेरो बुबाका एक मात्र छोरा हुन्।" उनी को हुन्?', 'Hari himself', 'हरि आफैँ', 'Brother', 'भाइ', 'Father', 'बुबा', 'Son', 'छोरा'),
    ('Pointing to a photograph, Gita says, "She is my mother\'s only daughter." Who is she?', 'एउटा तस्बिरतर्फ औँल्याउँदै गीता भन्छिन्, "उनी मेरी आमाकी एक मात्र छोरी हुन्।" उनी को हुन्?', 'Gita herself', 'गीता आफैँ', 'Sister', 'बहिनी', 'Mother', 'आमा', 'Daughter', 'छोरी'),
    ('Pointing to a photograph, Ram says, "He is the brother of my wife." Who is he?', 'एउटा तस्बिरतर्फ औँल्याउँदै राम भन्छन्, "उनी मेरी श्रीमतीका भाइ हुन्।" उनी को हुन्?', 'Brother-in-law', 'ज्वाइँ/साला', 'Brother', 'भाइ', 'Father', 'बुबा', 'Uncle', 'काका'),
    ('Pointing to a photograph, Sita says, "She is the sister of my husband." Who is she?', 'एउटा तस्बिरतर्फ औँल्याउँदै सीता भन्छिन्, "उनी मेरो श्रीमान्की बहिनी हुन्।" उनी को हुन्?', 'Sister-in-law', 'नन्द/भाउजू', 'Sister', 'बहिनी', 'Mother', 'आमा', 'Aunt', 'फुपू'),
    ('Pointing to a photograph, Ram says, "He is the son of my grandfather." Who is he?', 'एउटा तस्बिरतर्फ औँल्याउँदै राम भन्छन्, "उनी मेरो हजुरबुबाका छोरा हुन्।" उनी को हुन्?', 'Father or uncle', 'बुबा वा काका', 'Brother', 'भाइ', 'Son', 'छोरा', 'Grandfather', 'हजुरबुबा'),
    ('Pointing to a photograph, Sita says, "She is the daughter of my grandmother." Who is she?', 'एउटा तस्बिरतर्फ औँल्याउँदै सीता भन्छिन्, "उनी मेरी हजुरआमाकी छोरी हुन्।" उनी को हुन्?', 'Mother or aunt', 'आमा वा फुपू', 'Sister', 'बहिनी', 'Daughter', 'छोरी', 'Grandmother', 'हजुरआमा'),
]
for q, qn, a, an, d1, d1n, d2, d2n, d3, d3n in PHOTO:
    E('Blood Relations', 'hard', q, qn, [a, d1, d2, d3], [an, d1n, d2n, d3n],
      f'The answer is {a}.', f'उत्तर {an} हो।')

# ---------- linear seating from permutations ----------
for _ in range(150):
    names = rng.sample(NAMES_M + NAMES_F, 5)
    pos = rng.randint(1, 5)
    person = names[pos-1]
    ds = [x for x in names if x != person]
    rng.shuffle(ds)
    o = [person] + ds[:3]
    on = o[:]
    E('Seating Arrangement', 'medium', f'{", ".join(names)} sit in a row from left to right. Who sits {ord_s(pos)} from the left?',
      f'{", ".join(names)} बायाँदेखि दायाँ लाइनमा बस्छन्। बायाँबाट {dev(pos)}औँ स्थानमा को बस्छ?',
      o, on, f'{person} sits {ord_s(pos)} from the left.', f'बायाँबाट {dev(pos)}औँ स्थानमा {person} बस्छ।')
    # position from right framing
    pos_r = 6 - pos
    o2 = [person] + ds[:3]
    on2 = o2[:]
    E('Seating Arrangement', 'medium', f'{", ".join(names)} sit in a row from left to right. Who sits {ord_s(pos_r)} from the right?',
      f'{", ".join(names)} बायाँदेखि दायाँ लाइनमा बस्छन्। दायाँबाट {dev(pos_r)}औँ स्थानमा को बस्छ?',
      o2, on2, f'{person} sits {ord_s(pos_r)} from the right.', f'दायाँबाट {dev(pos_r)}औँ स्थानमा {person} बस्छ।')

# ---------- syllogisms: some/all forms ----------
SYL2 = [
    ('Some cats are black. All black things are animals. Which conclusion follows?', 'केही बिरालाहरू काला छन्। सबै काला कुराहरू जनावर हुन्। कुन निष्कर्ष निस्कन्छ?', 'Some cats are animals', 'केही बिरालाहरू जनावर हुन्', 'All cats are black', 'सबै बिरालाहरू काला छन्', 'No cat is an animal', 'कुनै बिरालो जनावर होइन', 'All animals are cats', 'सबै जनावर बिरालाहरू हुन्'),
    ('Some students are girls. All girls are humans. Which conclusion follows?', 'केही विद्यार्थी केटीहरू हुन्। सबै केटीहरू मानव हुन्। कुन निष्कर्ष निस्कन्छ?', 'Some students are humans', 'केही विद्यार्थी मानव हुन्', 'All students are girls', 'सबै विद्यार्थी केटीहरू हुन्', 'No student is a human', 'कुनै विद्यार्थी मानव होइन', 'All humans are students', 'सबै मानव विद्यार्थी हुन्'),
    ('All pens are pencils. Some pencils are red. Which conclusion follows?', 'सबै कलम पेन्सिल हुन्। केही पेन्सिल रातो छन्। कुन निष्कर्ष निस्कन्छ?', 'Some pens may be red', 'केही कलम रातो हुन सक्छन्', 'All pens are red', 'सबै कलम रातो छन्', 'No pen is red', 'कुनै कलम रातो छैन', 'All red things are pens', 'सबै रातो कुरा कलम हुन्'),
    ('Some books are novels. All novels are stories. Which conclusion follows?', 'केही किताब उपन्यास हुन्। सबै उपन्यास कथा हुन्। कुन निष्कर्ष निस्कन्छ?', 'Some books are stories', 'केही किताब कथा हुन्', 'All books are novels', 'सबै किताब उपन्यास हुन्', 'No book is a story', 'कुनै किताब कथा होइन', 'All stories are books', 'सबै कथा किताब हुन्'),
    ('All dogs are animals. Some animals are pets. Which conclusion follows?', 'सबै कुकुर जनावर हुन्। केही जनावर घरपालुवा हुन्। कुन निष्कर्ष निस्कन्छ?', 'Some dogs may be pets', 'केही कुकुर घरपालुवा हुन सक्छन्', 'All dogs are pets', 'सबै कुकुर घरपालुवा हुन्', 'No dog is a pet', 'कुनै कुकुर घरपालुवा होइन', 'All pets are dogs', 'सबै घरपालुवा कुकुर हुन्'),
    ('No cat is a dog. All dogs are animals. Which conclusion follows?', 'कुनै बिरालो कुकुर होइन। सबै कुकुर जनावर हुन्। कुन निष्कर्ष निस्कन्छ?', 'No cat is a dog', 'कुनै बिरालो कुकुर होइन', 'All cats are animals', 'सबै बिरालाहरू जनावर हुन्', 'Some cats are dogs', 'केही बिरालाहरू कुकुर हुन्', 'All animals are cats', 'सबै जनावर बिरालाहरू हुन्'),
    ('Some roses are red. All red things are flowers. Which conclusion follows?', 'केही गुलाफ रातो छन्। सबै रातो कुराहरू फूल हुन्। कुन निष्कर्ष निस्कन्छ?', 'Some roses are flowers', 'केही गुलाफ फूल हुन्', 'All roses are red', 'सबै गुलाफ रातो छन्', 'No rose is a flower', 'कुनै गुलाफ फूल होइन', 'All flowers are roses', 'सबै फूल गुलाफ हुन्'),
    ('All metals are solids. Some solids are hard. Which conclusion follows?', 'सबै धातु ठोस हुन्। केही ठोस कडा छन्। कुन निष्कर्ष निस्कन्छ?', 'Some metals may be hard', 'केही धातु कडा हुन सक्छन्', 'All metals are hard', 'सबै धातु कडा छन्', 'No metal is hard', 'कुनै धातु कडा छैन', 'All hard things are metals', 'सबै कडा कुरा धातु हुन्'),
]
for q, qn, a, an, d1, d1n, d2, d2n, d3, d3n in SYL2:
    E('Syllogism', 'hard', q, qn, [a, d1, d2, d3], [an, d1n, d2n, d3n],
      f'The conclusion that follows is: {a}.', f'निस्कने निष्कर्ष: {an}।')

# ---------- alphabet sums of pairs ----------
for _ in range(100):
    i, j = rng.randint(0, 25), rng.randint(0, 25)
    s = (i+1) + (j+1)
    o, on, _ = num_opts(s, [s+1, s-1, s+2, s-2])
    E('Alphabet Positions', 'medium', f'If A = 1, B = 2, ..., Z = 26, what is the sum of the values of {ALPHA[i]} and {ALPHA[j]}?',
      f'यदि A = १, B = २, ..., Z = २६ हो भने {ALPHA[i]} र {ALPHA[j]} को मानहरूको योग कति हुन्छ?', o, on,
      f'{ALPHA[i]} = {i+1} and {ALPHA[j]} = {j+1}, so the sum is {s}.', f'{ALPHA[i]} = {dev(i+1)} र {ALPHA[j]} = {dev(j+1)}, त्यसैले योग {dev_num(s)} हो।')

n = em.write('expansion-r10-iq4.json')
print('IQ4 TOTAL:', n, 'rejected:', len(em.rejected))
for r in em.rejected[:8]:
    print('  REJ', r)
