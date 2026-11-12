/// Mock-exam strings. Added ONLY as an extension on [AppStrings]
/// (never edit app_strings.dart) — every string bilingual EN/NE.
/// Copy tone follows the vanilla mock view (app.js `startMock`,
/// `renderMockTable`, `finishAttempt`).
library;

import 'app_strings.dart';

extension MockStrings on AppStrings {
  // --- mock intro (pattern summary card) ---
  String get mockIntroTitle => t('Mock exam', 'मक परीक्षा');
  String get patternTitle => t('Paper pattern', 'पेपर ढाँचा');
  String get patternQuestions => t('Questions', 'प्रश्नहरू');
  String get patternTime => t('Time', 'समय');
  String minutesLabel(int m) => t('$m minutes', '$m मिनेट');
  String get patternMarksPerQ => t('Marks per question', 'प्रति प्रश्न अंक');
  String get patternPass => t('Pass', 'पास');
  String get patternNegative => t('Negative marking', 'नेगेटिभ मार्किङ');
  String negPctLine(int pct) =>
      t('$pct% per wrong answer', 'प्रति गलत उत्तर $pct%');
  String get negNoneLine => t('None', 'छैन');
  String get negUnverifiedLine => t(
        'Unverified — not applied in this mock',
        'अपुष्ट — यो मकमा लागू हुँदैन',
      );
  String get untimedLine => t(
        'No time limit (time unverified — check the notice)',
        'समय सीमा छैन (समय अपुष्ट — सूचना हेर्नुहोस्)',
      );
  String get startMockBtn => t('Start mock exam', 'मक परीक्षा सुरु गर्नुहोस्');
  String thinBankWarning(int tagged, String examName) => t(
        'Only $tagged question(s) tagged for $examName so far, so this mock also draws from the general bank — it does not mirror the real paper yet.',
        'अहिलेसम्म $examName का लागि जम्मा $tagged प्रश्न ट्याग गरिएको छ, त्यसैले यो मक सामान्य बैंकबाट पनि प्रश्न लिन्छ — यसले वास्तविक पेपरको प्रतिलिपि गर्दैन।',
      );
  String get noMockAvailable => t(
        'No mock available for this exam — guide only. This exam has no verified MCQ prelim paper.',
        'यो परीक्षाका लागि मक उपलब्ध छैन — गाइड मात्र। यस परीक्षाको प्रमाणित MCQ प्रिलिम पेपर छैन।',
      );
  String get loadingMock =>
      t('Preparing your mock…', 'तपाईंको मक तयार हुँदैछ…');
  String get mockGoodLuck => t(
        'Answers stay hidden until you finish — just like the real exam hall. Good luck!',
        'तपाईंले सक्नुन्जेल उत्तरहरू लुकाइनेछन् — वास्तविक परीक्षा हल जस्तै। शुभकामना!',
      );

  // --- mock runner ---
  String mockRunnerTitle(String examName) =>
      t('$examName — mock', '$examName — मक');
  String get noTimerLabel => t('No timer', 'टाइमर छैन');
  String get timeUpAutoSubmitted =>
      t('Time up — auto-submitted', 'समय सकियो — स्वतः बुझाइयो');
  String get paletteTitle => t('Question palette', 'प्रश्न प्यालेट');
  String get legendAnswered => t('Answered', 'उत्तर दिइएको');
  String get legendCurrent => t('Current', 'हालको');
  String get legendFlagged => t('Flagged', 'फ्ल्याग गरिएको');
  String get legendUnanswered => t('Unanswered', 'अनुत्तरित');
  String get flagBtn => t('Flag', 'फ्ल्याग');
  String get unflagBtn => t('Unflag', 'फ्ल्याग हटाउनुहोस्');
  String get flaggedSnack =>
      t('Flagged for review ✓', 'समीक्षाका लागि फ्ल्याग भयो ✓');
  String get unflaggedSnack => t('Flag removed.', 'फ्ल्याग हटाइयो।');
  String answeredOf(int n, int total) =>
      t('Answered $n/$total', 'उत्तर $n/$total');

  // --- finish confirm ---
  String get finishMockTitle => t('Submit this mock?', 'यो मक बुझाउने?');
  String finishMockBody(int answered, int unanswered) => t(
        '$answered answered, $unanswered unanswered — unanswered questions score 0. Submit now?',
        '$answered उत्तर दिइयो, $unanswered अनुत्तरित — अनुत्तरित प्रश्नको ० अंक। अहिले बुझाउने?',
      );

  // --- abandon a timed session (back button) ---
  String get abandonMockTitle => t('Leave this mock?', 'यो मक छोड्ने?');
  String get abandonMockBody => t(
        'Leaving now abandons this timed session — it will not be scored.',
        'अहिले छोडेमा यो समयबद्ध सत्र त्यागिन्छ — स्कोर हुँदैन।',
      );
  String get leaveLabel => t('Leave', 'छोड्नुहोस्');
  String get stayLabel => t('Stay', 'बस्नुहोस्');
}
