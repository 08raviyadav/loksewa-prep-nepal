/// Historical events / Dates to Remember strings. Added ONLY as an
/// extension on [AppStrings] (never edit app_strings.dart) — every
/// string bilingual EN/NE. Copy mirrors the vanilla site's historical
/// events section exactly (loksewa-prep-nepal/assets/js/app.js
/// §"Historical events / Dates to Remember").
library;

import 'app_strings.dart';

extension HistoryStrings on AppStrings {
  // --- nav + header ---
  String get historyNav => t('Dates to Remember', 'इतिहासका मिति');
  String get historyTitle => t('Dates to Remember', 'इतिहासका मिति');
  String get historyBlurb => t(
        'Verified historical dates for Lok Sewa GK — Nepal\'s history and constitutions, its institutions, and world history. Tap a row to read the story. Dates recur every year on their Bikram Sambat day.',
        'लोक सेवा GK का लागि प्रमाणित ऐतिहासिक मितिहरू — नेपालको इतिहास र संविधान, संस्थाहरू र विश्व इतिहास। कथा पढ्न पङ्क्तिमा थिच्नुहोस्। मितिहरू हरेक वर्ष विक्रम संवत्कै दिन दोहोरिन्छन्।',
      );
  String historyCount(int n) => t(
        '$n dates · verified against at least 2 sources each',
        '$n मितिहरू · प्रत्येक कम्तीमा २ स्रोतसँग प्रमाणित',
      );
  String historyShownCount(int n) =>
      t(n == 1 ? '1 date' : '$n dates', '$n मिति');

  // --- search + category filter ---
  String get historySearchLabel => t('Search', 'खोज्नुहोस्');
  String get historySearchHint =>
      t('e.g. Constitution, Everest, Rana…', 'जस्तै संविधान, सगरमाथा, राणा…');
  String get historyCategoryLabel => t('Category', 'श्रेणी');
  String get historyCategoryAll => t('All categories', 'सबै श्रेणी');
  String historyCategory(String c) => switch (c) {
        'nepal-history' => t('Nepal History', 'नेपालको इतिहास'),
        'world-history' => t('World History', 'विश्व इतिहास'),
        'nepal-institutions' => t('Nepal Institutions', 'नेपालका संस्थाहरू'),
        'constitution' => t('Constitution', 'संविधान'),
        'international' => t('International', 'अन्तर्राष्ट्रिय'),
        _ => c,
      };

  // --- rows ---
  String get historyYearInSummary =>
      t('Year in the summary below', 'वर्ष तलको सारांशमा छ');
  String get historySources => t('Sources', 'स्रोतहरू');
  String get historyReverify => t('⚠️ re-verify', '⚠️ पुनःपुष्टि');
  String get historyReverifyHint => t(
        'Medium confidence — re-verify before citing',
        'मध्यम विश्वसनीयता — उद्धृत गर्नुअघि पुनःपुष्टि गर्नुहोस्',
      );
  String get historySourceTitle => t('Source', 'स्रोत');
  String get historyCopyLink => t('Copy link', 'लिङ्क कपी गर्नुहोस्');
  String get historyLinkCopied => t('Link copied.', 'लिङ्क कपी भयो।');
  String get historyClose => t('Close', 'बन्द गर्नुहोस्');

  // --- empty state ---
  String get historyNoMatchTitle => t('No dates match', 'कुनै मिति मिलेन');
  String get historyNoMatchBody => t(
        'Try a different search or category.',
        'अर्को खोजी वा श्रेणी प्रयास गर्नुहोस्।',
      );

  // --- On This Day card (Home) ---
  String get historyOtdTitle => t('📜 On This Day', '📜 आजको दिनमा');
  String get historyOtdSubtitle =>
      t('on this day in history', 'इतिहासमा आजको दिन');
  String get historyAllDatesBtn =>
      t('All dates to remember →', 'सबै सम्झनुपर्ने मितिहरू →');

  // --- Quiz me ---
  String get historyQuizMe => t('🎴 Quiz me', '🎴 मलाई प्रश्न गर्नुहोस्');
  String get historyBackToList => t('← Back to list', '← सूचीमा फर्कनुहोस्');
  String get historyQuizEmptyTitle =>
      t('Nothing to quiz yet', 'प्रश्न गर्न केही छैन');
  String get historyQuizEmptyBody => t(
        'No dated events are loaded, so there is nothing to quiz on.',
        'मिति भएका घटना लोड भएका छैनन्, त्यसैले प्रश्न गर्न केही छैन।',
      );
  String get historyQuizDoneTitle => t('🎉 Quiz done!', '🎉 क्विज सकियो!');
  String get historyQuizCorrect => t('correct', 'सही');
  String get historyQuizMissed => t('missed', 'छुट्यो');
  String get historyQuizAgain => t('🔀 Quiz again', '🔀 फेरि प्रश्न गर्नुहोस्');
  String historyQuizProgress(int idx, int total, int correct, int missed) => t(
        'Question $idx / $total · ✓ $correct · ✗ $missed',
        'प्रश्न $idx / $total · ✓ $correct · ✗ $missed',
      );
  String get historyQuizWhen => t('When did this happen?', 'यो कहिले भयो?');
  String get historyQuizReveal =>
      t('👁️ Reveal the date', '👁️ मिति देखाउनुहोस्');
  String get historyQuizGotIt => t('✅ Got it', '✅ मिल्यो');
  String get historyQuizMissedIt => t('❌ Missed it', '❌ छुट्यो');
  String get historyQuizReset => t('Reset quiz', 'क्विज रिसेट गर्नुहोस्');
}
