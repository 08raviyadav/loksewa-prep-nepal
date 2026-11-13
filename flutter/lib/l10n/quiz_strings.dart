/// Quiz + result strings. Added ONLY as an extension on [AppStrings]
/// (never edit app_strings.dart) — every string bilingual EN/NE.
/// Encouragement lines are the vanilla site's exact copy
/// (loksewa-prep-nepal/assets/js/app.js: PRAISE/TRY_AGAIN/PASS/FAIL_LINES).
library;

import 'dart:math';

import 'app_strings.dart';

extension QuizStrings on AppStrings {
  // --- practice setup additions (timer / negative toggles) ---
  String get timerLabel => t('Timer', 'टाइमर');
  String get timerHint => t(
        'Real-paper pace, auto-submits at zero',
        'वास्तविक परीक्षा गति, समय सकिएपछि स्वतः बुझाइन्छ',
      );
  String get negativeLabel => t('Negative marking', 'नेगेटिभ मार्किङ');
  String negativeHint(String pct) =>
      t('−$pct% per wrong answer', 'प्रति गलत उत्तर −$pct%');

  // --- quiz screen ---
  String quizProgress(int i, int n) => t('Question $i of $n', 'प्रश्न $i / $n');
  String get skip => t('Skip', 'छोड्नुहोस्');
  String get bookmark => t('Bookmark', 'बुकमार्क');
  String get bookmarked => t('Bookmarked ✓', 'बुकमार्क भयो ✓');
  String get alreadyBookmarked =>
      t('Already bookmarked.', 'पहिले नै बुकमार्क गरिएको छ।');
  String get report => t('Report', 'रिपोर्ट');
  String get reportTitle =>
      t('Report this question', 'यो प्रश्न रिपोर्ट गर्नुहोस्');
  String get reportHint => t('What is wrong with it?', 'यसमा के गल्ती छ?');
  String get reportSaved => t(
        'Thanks — report saved for review.',
        'धन्यवाद — रिपोर्ट समीक्षाका लागि सुरक्षित भयो।',
      );
  String get cancel => t('Cancel', 'रद्द गर्नुहोस्');
  String get save => t('Save', 'सुरक्षित गर्नुहोस्');
  String get previous => t('Previous', 'अघिल्लो');
  String get next => t('Next', 'अर्को');
  String get finish => t('Finish', 'समाप्त गर्नुहोस्');
  String get finishTitle => t('Finish this set?', 'यो सेट समाप्त गर्ने?');
  String finishBody(int unanswered) => unanswered == 0
      ? t(
          'Submit your answers and see the result.',
          'उत्तर बुझाएर नतिजा हेर्नुहोस्।',
        )
      : t(
          '$unanswered question(s) unanswered — they score 0. Submit anyway?',
          '$unanswered प्रश्न अनुत्तरित — तिनको ० अंक। जे भए पनि बुझाउने?',
        );
  String get submit => t('Submit', 'बुझाउनुहोस्');
  String get correctFeedback => t('✅ Correct!', '✅ सही!');
  String get wrongFeedback => t('❌ Wrong.', '❌ गलत।');
  String get correctAnswerIs => t('Correct answer:', 'सही उत्तर:');
  String get explanationLabel => t('Explanation', 'व्याख्या');
  String get timeUpTitle =>
      t('Time up — auto-submitted', 'समय सकियो — स्वतः बुझाइयो');
  String get noQuestions => t('No questions to show.', 'देखाउने प्रश्न छैन।');
  String noMatch(String bits) => t(
        'No questions match $bits — try another topic or difficulty.',
        '$bits सँग मिल्ने प्रश्न छैन — अर्को विषय वा कठिनाइ प्रयास गर्नुहोस्।',
      );

  // --- result screen ---
  String get practiceMode => t('Practice', 'अभ्यास');
  String get mockMode => t('Mock Exam', 'मक परीक्षा');
  String get passLabel => t('✅ PASS', '✅ पास');
  String get failLabel => t('❌ FAIL', '❌ फेल');
  String cutoffLine(int cutoffPct, int cutoff, int fullTotal, double pct) => t(
        'cutoff for this exam is $cutoffPct% ($cutoff/$fullTotal on the full paper) · $pct%',
        'यो परीक्षाको कटअफ $cutoffPct% हो ($cutoff/$fullTotal पूर्ण पेपरमा) · $pct%',
      );
  String get correctCount => t('Correct', 'सही');
  String get wrongCount => t('Wrong', 'गलत');
  String get skippedCount => t('Skipped', 'छोडिएको');
  String get timeLabel => t('Time', 'समय');
  String perQuestionSecs(int s) => t('$s s per question', '$s सेकेन्ड/प्रश्न');
  String get xpLabel => t('XP', 'XP');
  String get levelLabel => t('Level', 'लेभल');
  String get streakLabel => t('Streak', 'स्ट्रिक');
  String get daysLabel => t('day(s)', 'दिन');
  String get negOffLine => t(
        'Negative marking OFF — this exam has no negative marking.',
        'नेगेटिभ मार्किङ बन्द — यो परीक्षामा नेगेटिभ मार्किङ छैन।',
      );
  String negOnLine(String perWrong, int pct) => t(
        'Negative marking ON (−$perWrong per wrong question, $pct%)',
        'नेगेटिभ मार्किङ चालु (प्रति गलत प्रश्न −$perWrong, $pct%)',
      );
  String retryWrong(int n) =>
      t('Retry wrong only ($n)', 'गलत मात्र दोहोर्‍याउनुहोस् ($n)');
  String get nothingToRetry => t('Nothing to retry!', 'दोहोर्‍याउन केही छैन!');
  String get backHome => t('Back home', 'होम जानुहोस्');
  String practiceWeakest(String topic) =>
      t('📚 Practice weakest topic: $topic', '📚 कमजोर विषय अभ्यास: $topic');
  String get levelUpBanner =>
      t('🎉 LEVEL UP! You are now Level ', '🎉 लेभल अप! तपाईं अब लेभल ');
  String get weeklyBanner => t(
        '🏆 Weekly goal smashed! Weekly Champion badge earned.',
        '🏆 साप्ताहिक लक्ष्य पूरा! Weekly Champion ब्याज प्राप्त भयो।',
      );
  String get strongestLabel => t('Strongest:', 'सबल:');
  String get weakestLabel =>
      t('Weakest — revise these:', 'कमजोर — यी दोहोर्‍याउनुहोस्:');
  String get topicBreakdown => t('Topic breakdown', 'विषय विश्लेषण');
  String get wrongReviewTitle =>
      t('Wrong answers — review', 'गलत उत्तर — समीक्षा');
  String get yourAnswer => t('Your answer:', 'तपाईंको उत्तर:');
  String get correctIs => t('Correct:', 'सही:');
  String get noWrongAnswers => t(
        '🎉 No wrong answers — perfect set!',
        '🎉 गलत उत्तर छैन — उत्कृष्ट सेट!',
      );
  String get discuss => t('💬 Discuss', '💬 छलफल');
  String get reviseTopic => t('📖 Revise', '📖 दोहोर्‍याउनुहोस्');

  // --- encouragement lines (vanilla exact copy; no line repeats twice) ---
  static final Map<String, int> _lastLineIdx = {};
  static final _rand = Random();

  String _pick(List<List<String>> lines, String key) {
    if (lines.isEmpty) return '';
    var idx = 0;
    if (lines.length > 1) {
      do {
        idx = _rand.nextInt(lines.length);
      } while (idx == _lastLineIdx[key]);
      _lastLineIdx[key] = idx;
    }
    final line = lines[idx];
    return isNe ? line[1] : line[0];
  }

  String praiseLine() => _pick(_praiseLines, 'praise');
  String tryAgainLine() => _pick(_tryAgainLines, 'try');
  String passLine() => _pick(_passLines, 'pass');
  String failLine() => _pick(_failLines, 'fail');

  static const List<List<String>> _praiseLines = [
    ['Nice — that one is staying with you.', 'राम्रो — यो कुरा मनमा बस्नेछ।'],
    ['Sharp! Keep the streak alive.', 'चुस्त! यो लय कायम राख्नुहोस्।'],
    [
      'Exactly right. On to the next one.',
      'ठ्याक्कै मिल्यो। अब अर्को प्रश्नतिर।',
    ],
    [
      'Well done — the revision is paying off.',
      'स्याबास — दोहोर्याएको मिहिनेतले फल दिइरहेको छ।',
    ],
    [
      'Correct! You are building real momentum.',
      'सही! तपाईं साँच्चै गति बनाउँदै हुनुहुन्छ।',
    ],
    ['Brilliant — that is a keeper.', 'उत्कृष्ट — यो कुरा सम्झन लायक छ।'],
    ['Yes! One more fact locked in.', 'हो! अर्को तथ्य पनि पक्का भयो।'],
    [
      'Superb — your hard work is showing.',
      'उत्तम — तपाईंको मिहिनेत देखिइरहेको छ।',
    ],
    [
      'That was textbook. Well played.',
      'त्यो त किताबी उत्तर भयो। राम्रो खेल्नुभयो।',
    ],
    [
      'Spot on! You knew that one cold.',
      'ठीक ठाउँमा! त्यो त तपाईंलाई पक्कै थाहा थियो।',
    ],
    [
      'Excellent — one step closer to the hall.',
      'उत्कृष्ट — परीक्षा हलतिर एक पाइला नजिक।',
    ],
    [
      'Great recall — that fact is yours now.',
      'राम्रो सम्झना — त्यो तथ्य अब तपाईंको भयो।',
    ],
    ['You are on fire today!', 'आज तपाईं त आगो बल्नुभएको छ!'],
    [
      'That is the kind of answer that passes exams.',
      'यस्तै उत्तरले परीक्षा पास गराउँछ।',
    ],
    [
      'Well remembered — revision done right.',
      'राम्रोसँग सम्झनुभयो — दोहोर्याइ सही तरिकाले भयो।',
    ],
    ['Clean and correct. Lovely work.', 'सफा र सही। राम्रो काम।'],
    [
      'Another one in the bag — keep going!',
      'अर्को पनि हातमा पर्यो — अगाडि बढ्नुहोस्!',
    ],
    [
      'Nailed it — that topic is yours.',
      'ठ्याक्कै मिलाउनुभयो — त्यो विषय अब तपाईंको हो।',
    ],
  ];

  static const List<List<String>> _tryAgainLines = [
    [
      'Not this one — but now you know it for the exam hall.',
      'यो मिलेन — तर अब परीक्षा हलका लागि थाहा भयो।',
    ],
    [
      'Close! Read the explanation slowly and it will stick.',
      'नजिक पुग्नुभयो! व्याख्या बिस्तारै पढ्नुहोस्, मनमा बस्छ।',
    ],
    [
      'Wrong today, right on exam day — that is the deal.',
      'आज गलत, परीक्षा दिन सही — यही त सम्झौता हो।',
    ],
    [
      'Tricky one. The explanation is worth a second read.',
      'झुक्किने प्रश्न। व्याख्या दोस्रो पटक पढ्न लायक छ।',
    ],
    [
      'No worries — mistakes here are free.',
      'चिन्ता नलिनुहोस् — यहाँ गल्ती गर्नु नि:शुल्क छ।',
    ],
    [
      'That one stings a little, but it is now in your mistakes list to revise.',
      'यो अलि चित्त दुख्यो होला, तर अब यो तपाईंको गल्ती सूचीमा छ — दोहोर्याउनुहोस्।',
    ],
    [
      'Missed it — but every miss here is one less miss in the hall.',
      'छुट्यो — तर यहाँ छुटेको प्रत्येक प्रश्न हलमा छुट्ने सम्भावना घटाउँछ।',
    ],
    [
      'Not yet — the explanation below is your shortcut.',
      'अहिलेसम्म मिलेन — तलको व्याख्या तपाईंको छोटो बाटो हो।',
    ],
    [
      'Good try! The correct answer is a keeper — note it down.',
      'राम्रो प्रयास! सही उत्तर सम्झन लायक छ — टिप्नुहोस्।',
    ],
    [
      'That was a hard one. Even toppers miss these.',
      'त्यो गाह्रो प्रश्न थियो। टपरहरूले पनि यस्ता छुटाउँछन्।',
    ],
    [
      'Almost! One careful read and it will click.',
      'लगभग मिल्यो! एक पटक ध्यान दिएर पढ्नुहोस्, बुझिन्छ।',
    ],
    [
      'Wrong answer, right lesson. That is how toppers are made.',
      'गलत उत्तर, सही पाठ। यसरी नै टपर बन्छन्।',
    ],
    [
      'A miss today is a mark saved tomorrow.',
      'आजको गल्ती भोलिको अंक जोगाउने हो।',
    ],
    [
      'This one caught you — now it cannot catch you twice.',
      'यो प्रश्नले तपाईंलाई छोप्यो — अब यसले दोस्रो पटक छोप्न सक्दैन।',
    ],
    [
      'So close! Your brain just filed this one away.',
      'धेरै नजिक! तपाईंको दिमागले यो भर्खरै सुरक्षित गर्यो।',
    ],
    [
      'Every wrong answer here is a free lesson.',
      'यहाँको प्रत्येक गलत उत्तर नि:शुल्क पाठ हो।',
    ],
    [
      'Keep your head up — the next one is yours.',
      'शिर उच्च राख्नुहोस् — अर्को प्रश्न तपाईंको हो।',
    ],
    [
      'Mistakes are the revision list writing itself.',
      'गल्तीहरू आफैं दोहोर्याउने सूची बन्दै छन्।',
    ],
  ];

  static const List<List<String>> _passLines = [
    [
      'You cleared the cutoff — that is a real pass, not luck.',
      'तपाईंले कटअफ पार गर्नुभयो — यो साँच्चै पास हो, भाग्य होइन।',
    ],
    [
      'Cutoff beaten. Keep this form going.',
      'कटअफ पार भयो। यही फर्म कायम राख्नुहोस्।',
    ],
    [
      'Passed! The exam hall version of you says thanks.',
      'पास! परीक्षा हलमा बस्ने तपाईंले धन्यवाद भन्नेछन्।',
    ],
    [
      'That is a pass worth celebrating — briefly, then back to work.',
      'यो पास मनाउन लायक छ — छोटकरीमा, अनि फेरि कामतिर।',
    ],
    [
      'Cutoff cleared. The real paper is starting to look doable.',
      'कटअफ पार भयो। वास्तविक परीक्षा अब सम्भव देखिन थालेको छ।',
    ],
  ];

  static const List<List<String>> _failLines = [
    [
      'Below the cutoff this time — the weak topics below are your revision list.',
      'यस पटक कटअफभन्दा तल — तलका कमजोर विषय तपाईंको दोहोर्याउने सूची हुन्।',
    ],
    [
      'Not yet — but every wrong answer here is one you will not repeat.',
      'अहिलेसम्म पुगेन — तर यहाँका प्रत्येक गलत उत्तर अब दोहोरिने छैनन्।',
    ],
    [
      'Keep going. A fail in practice is cheaper than a fail in the hall.',
      'अगाडि बढ्नुहोस्। अभ्यासमा असफल हुनु हलमा असफल हुनुभन्दा सस्तो छ।',
    ],
    [
      'The cutoff is close — one more focused week can close the gap.',
      'कटअफ नजिक छ — एक हप्ता केन्द्रित तयारीले दूरी घटाउन सक्छ।',
    ],
    [
      'Not a pass yet, but the score is honest — and honesty is where improvement starts.',
      'अहिलेसम्म पास होइन, तर अंक इमानदार छ — र सुधार इमानदारीबाटै सुरु हुन्छ।',
    ],
  ];

  // --- share score (v1.0.4) ---
  String get shareScoreTitle => t('Share score', 'स्कोर सेयर गर्नुहोस्');
  String shareScoreText(
    String score,
    String max,
    String pct,
    String exam,
  ) =>
      t(
        'I scored $score/$max ($pct%) on $exam in Outrank! 🎯\n\nFree Lok Sewa exam prep — download it here:\nhttps://github.com/08raviyadav/loksewa-prep-nepal/releases/latest/download/app-release.apk',
        'मैले Outrank मा $exam मा $score/$max ($pct%) ल्याएँ! 🎯\n\nनिःशुल्क लोक सेवा परीक्षा तयारी — यहाँबाट डाउनलोड गर्नुहोस्:\nhttps://github.com/08raviyadav/loksewa-prep-nepal/releases/latest/download/app-release.apk',
      );
}
