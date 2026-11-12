/// Exam Dates screen strings. Added ONLY as an extension on [AppStrings]
/// (never edit app_strings.dart) — every string bilingual EN/NE.
/// Copy mirrors the vanilla site's renderExamDates exactly
/// (loksewa-prep-nepal/assets/js/app.js §"Exam dates": view-examdates).
library;

import 'app_strings.dart';

extension ExamDatesStrings on AppStrings {
  // --- header ---
  String get examDatesTitle => t('Exam dates', 'परीक्षा मितिहरू');
  String get examDatesBlurb => t(
        'Verified exam dates, admit-card releases and application deadlines from official notices (PSC, TSC, NRB, MEC…). Dates are in Bikram Sambat — never guessed; every entry links its source.',
        'आधिकारिक सूचनाहरूबाट प्रमाणित परीक्षा मिति, प्रवेशपत्र र आवेदन अन्तिम मिति (लोक सेवा, शिक्षक सेवा, राष्ट्र बैंक, चिकित्सा शिक्षा आयोग…)। मितिहरू विक्रम संवत्मा छन् — अनुमान गरिएको होइन; हरेक प्रविष्टिमा स्रोत लिङ्क छ।',
      );

  // --- kind filter ---
  String get showFilterLabel => t('Show:', 'देखाउनुहोस्:');
  String get kindAll => t('All', 'सबै');
  String kindLabel(String kind) => switch (kind) {
        'exam' => t('Exam', 'परीक्षा'),
        'admit' => t('Admit card', 'प्रवेशपत्र'),
        'deadline' => t('Deadline', 'अन्तिम मिति'),
        _ => kind,
      };

  // --- countdown chips (vanilla's remChip: 🔴 today, 🟡 ≤7d, 📅 later) ---
  String get chipToday => t('🔴 Today', '🔴 आज');
  String get chipTomorrow => t('🟡 Tomorrow', '🟡 भोलि');
  String chipSoon(int d) => t('🟡 in $d days', '🟡 $d दिनमा');
  String chipLater(int d) => t('📅 in $d days', '📅 $d दिनमा');
  String get chipDone => t('✓ Done', '✓ सकियो');

  // --- row actions ---
  String get practiceBtn => t('Practice', 'अभ्यास');
  String get mockBtn => t('Mock', 'मक');
  String get remindMeBtn => t('🔕 Remind me', '🔕 सम्झाउनुहोस्');
  String get remindingBtn => t('🔔 Reminding', '🔔 रिमाइन्डर छ');

  // --- official source + re-verify ---
  String get officialSource => t('Official source', 'आधिकारिक स्रोत');
  String get reverifyBadge => t('re-verify', 'पुनःपुष्टि');
  String get reverifyHint => t(
        'Single-source: re-verify on the official site',
        'एकल स्रोत: आधिकारिक साइटमा पुनःपुष्टि गर्नुहोस्',
      );
  String get sourceDialogTitle => t('Official source', 'आधिकारिक स्रोत');
  String get copyLink => t('Copy link', 'लिङ्क कपी गर्नुहोस्');
  String get linkCopied => t('Link copied.', 'लिङ्क कपी भयो।');
  String get closeBtn => t('Close', 'बन्द गर्नुहोस्');

  // --- empty state ---
  String get noDatesTitle => t('No dates yet', 'अहिले मिति छैन');
  String get noDatesBody => t(
        'No verified upcoming dates in this list. Check the official sites linked in Notices.',
        'यो सूचीमा प्रमाणित आगामी मिति छैन। सूचनामा लिङ्क गरिएका आधिकारिक साइट हेर्नुहोस्।',
      );

  // --- footer: the honesty note ---
  String get confirmNote => t(
        'Exam boards reschedule — always confirm on the official site before travelling.',
        'परीक्षा बोर्डले मिति सार्न सक्छ — यात्रा गर्नुअघि आधिकारिक साइटमा पुष्टि गर्नुहोस्।',
      );
}
