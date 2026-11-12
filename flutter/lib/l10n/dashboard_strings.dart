import 'app_strings.dart';

/// Dashboard strings. Lives as an extension on [AppStrings] (per the
/// milestone convention: other milestones' `app_strings.dart` is untouched).
extension DashboardStrings on AppStrings {
  // --- header ---
  String get dashLevel => t('Level', 'लेभल');
  String dashLevelProgress(int n) => t('Level $n progress', 'लेभल $n प्रगति');
  String xpToNext(int rest, int nextLevel) => t(
        '$rest / 500 XP to Level $nextLevel',
        '$rest / ५०० XP, लेभल $nextLevel तर्फ',
      );
  String get dashDayStreak => t('day streak', 'दिनको स्ट्रिक');

  // --- stat row ---
  String get dashSessions => t('sessions', 'सत्र');
  String get dashAverageScore => t('average score', 'औसत स्कोर');
  String get dashPasses => t('passes', 'पास');

  // --- badges ---
  String get dashBadgesTitle => t('Badges', 'ब्याजहरू');
  String get dashNoBadges => t(
        'No badges yet — finish your first practice set to earn one.',
        'अझै ब्याज छैन — एउटा कमाउन पहिलो अभ्यास सेट पूरा गर्नुहोस्।',
      );

  // --- personal records ---
  String get dashRecordsTitle => t(
        '🏆 Personal Records — just for you',
        '🏆 व्यक्तिगत रेकर्ड — तपाईंका लागि',
      );
  String get dashLongestStreak => t('Longest streak', 'सबैभन्दा लामो स्ट्रिक');
  String get dashDays => t('day(s)', 'दिन');
  String get dashTotalXp => t('Total XP', 'कुल XP');
  String get dashTotalQuestions =>
      t('Total questions answered', 'जवाफ दिएका कुल प्रश्नहरू');
  String get dashBestDay => t('Best day', 'उत्कृष्ट दिन');
  String get dashQuestions => t('questions', 'प्रश्नहरू');
  String get dashNoBestDay => t(
        'No attempts yet — finish a practice set and your best day will show up here.',
        'अझै प्रयास छैन — अभ्यास सेट पूरा गर्नुहोस्, तपाईंको उत्कृष्ट दिन यहाँ देखिनेछ।',
      );
  String get dashBestMocks =>
      t('Best mock score per exam', 'प्रति परीक्षा उत्कृष्ट मक स्कोर');
  String get dashNoMocks => t(
        'No mock attempts yet — your first mock score per exam becomes the record to beat.',
        'अझै मक प्रयास छैन — प्रति परीक्षाको पहिलो मक स्कोर नै तोड्नुपर्ने रेकर्ड बन्छ।',
      );
  String get dashBestSpeed => t('Best Speed Round', 'उत्कृष्ट स्पिड राउन्ड');
  String get dashNoSpeed => t(
        'No Speed Round yet — try the 60-second round from Home.',
        'अझै स्पिड राउन्ड छैन — होमबाट ६०-सेकेन्ड राउन्ड प्रयास गर्नुहोस्।',
      );
  String get dashOnDate => t('on', 'मिति');
  String get dashPrivateNote => t(
        'Personal only — no leaderboard, nothing leaves this device.',
        'व्यक्तिगत मात्र — लिडरबोर्ड छैन, यो डिभाइसबाट केही बाहिर जाँदैन।',
      );

  // --- weekly challenge ---
  String get dashWeeklyTitle => t('🎯 Weekly Challenge', '🎯 साप्ताहिक चुनौती');
  String dashWeeklyDone(int done, int target) =>
      t('$done / $target questions', '$done / $target प्रश्नहरू');
  String get dashWeekOf => t('Week of', 'हप्ता');
  String get dashWeekRange => t('(Mon–Sun)', '(सोम–आइत)');
  String get dashGoalMet => t(
        '✅ Goal met — Weekly Champion badge earned!',
        '✅ लक्ष्य पूरा — Weekly Champion ब्याज प्राप्त भयो!',
      );
  String dashPctThere(int pct) =>
      t('$pct% there — keep going!', '$pct% पुग्यो — जारी राख्नुहोस्!');
  String get dashGoalsSmashed => t(
        '🏆 Weekly goals smashed so far:',
        '🏆 अहिलेसम्म पूरा भएका साप्ताहिक लक्ष्य:',
      );

  // --- weak topics ---
  String get dashWeakTitle =>
      t('Weak topics — revise these', 'कमजोर विषयहरू — यी दोहोर्‍याउनुहोस्');
  String dashWeakLine(String topic, int correct, int total) =>
      t('$topic — $correct/$total correct', '$topic — $correct/$total सही');
  String get dashNoWeak => t(
        'No mistakes recorded yet — answer a practice set and your weak topics will show up here.',
        'अझै गल्ती रेकर्ड भएको छैन — अभ्यास सेट दिनुहोस् अनि तपाईंका कमजोर विषय यहाँ देखिनेछन्।',
      );
  String dashPracticeWeakest(String topic) =>
      t('📚 Practice weakest topic: $topic', '📚 कमजोर विषय अभ्यास: $topic');

  // --- entry cards ---
  String get dashDailyTitle => t('🔥 Daily Challenge', '🔥 दैनिक चुनौती');
  String get dashDailyBody => t(
        '10 seeded questions — the same set for everyone, new every day.',
        '१० वटा सिडेड प्रश्नहरू — सबैका लागि एउटै सेट, हरेक दिन नयाँ।',
      );
  String get dashStartChallenge =>
      t("Start today's challenge", 'आजको चुनौती सुरु गर्नुहोस्');
  String get dashQuickTitle => t('⚡ Quick Quiz', '⚡ क्विक क्विज');
  String get dashQuickBody => t(
        '5 random questions — a fast warm-up.',
        '५ वटा अनियमित प्रश्न — छिटो वार्म-अप।',
      );
  String get dashStartQuiz =>
      t('Start quick quiz', 'क्विक क्विज सुरु गर्नुहोस्');

  // --- recent attempts ---
  String get dashRecentTitle => t('Recent attempts', 'हालका प्रयासहरू');
  String get dashNoAttemptsTitle => t('No attempts yet', 'अझै प्रयास छैन');
  String get dashNoAttemptsBody => t(
        'Your practice and mock sessions will appear here with scores and pass/fail.',
        'तपाईंका अभ्यास र मक सत्रहरू स्कोर र पास/फेलसहित यहाँ देखिनेछन्।',
      );
  String get dashStartPracticing =>
      t('Start practicing', 'अभ्यास सुरु गर्नुहोस्');
  String get dashPass => t('PASS', 'पास');
  String get dashFail => t('FAIL', 'फेल');
  String get dashCorrect => t('Correct', 'सही');
  String get dashWrong => t('Wrong', 'गलत');
  String get dashSkipped => t('Skipped', 'छोडिएको');

  // --- score history ---
  String get dashHistoryTitle => t('Score history', 'स्कोर इतिहास');
  String get dashNoHistory => t(
        'No data yet — finish a practice session and your score history appears here.',
        'अझै डेटा छैन — अभ्यास सत्र पूरा गर्नुहोस्, तपाईंको स्कोर इतिहास यहाँ देखिनेछ।',
      );

  // --- deep-link dialogs (wired in main.dart) ---
  String get dailyDoneTitle => t('Already done today', 'आज सकिसक्नुभयो');
  String get dailyRepeatAsk => t(
        'You already finished today\'s Daily Challenge. Do it again for practice (no extra XP)?',
        'तपाईंले आजको दैनिक चुनौती सकिसक्नुभयो। अभ्यासका लागि फेरि गर्ने (थप XP छैन)?',
      );
  String get dailyRepeatYes => t('Practice again', 'फेरि अभ्यास');
  String noTopicQuestions(String topic) => t(
        'No "$topic" questions found — try another topic.',
        '"$topic" का प्रश्न भेटिएनन् — अर्को विषय प्रयास गर्नुहोस्।',
      );
}
