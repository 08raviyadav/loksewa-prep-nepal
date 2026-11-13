/// Hand-rolled EN/NE string tables.
///
/// The vanilla site uses a B(en, ne) helper + data-language attributes;
/// this is the same idea without intl codegen (keeps the build lean and
/// lets community translators edit one obvious file).
enum AppLang { en, ne }

extension AppLangX on AppLang {
  String get code => this == AppLang.en ? 'en' : 'ne';
  // v1.0.9: Nepali is the default — only an explicitly saved 'en'
  // picks English (a missing/unknown code means Nepali).
  static AppLang fromCode(String? code) =>
      code == 'en' ? AppLang.en : AppLang.ne;
}

class AppStrings {
  final AppLang lang;
  const AppStrings(this.lang);
  bool get isNe => lang == AppLang.ne;
  String t(String en, String ne) => isNe ? ne : en;

  // --- app chrome ---
  String get appName => t('LokSewa Vidyapeeth', 'लोक सेवा विद्यापीठ');
  String get tagline => t(
        'Nepal\u2019s Lok Sewa exams, mastered question by question.',
        'नेपालको लोक सेवा परीक्षा, प्रश्न-प्रश्न गर्दै मास्टर गर्नुहोस्।',
      );
  String get navHome => t('Home', 'होम');
  String get navPractice => t('Practice', 'अभ्यास');
  String get navMock => t('Mock Exams', 'मक परीक्षा');
  String get navDashboard => t('Dashboard', 'ड्यासबोर्ड');
  String get navMore => t('More', 'थप');
  String get examDates => t('Exam Dates', 'परीक्षा मितिहरू');
  String get courses => t('Courses', 'पाठ्यक्रम');

  // --- hero ---
  String get heroEyebrow => t('100% free \u00b7 Open source \u00b7 MIT',
      '१००% निःशुल्क \u00b7 ओपन सोर्स \u00b7 MIT',);
  String get heroTitle => t(
        'Nepal\u2019s Lok Sewa exams, mastered question by question.',
        'नेपालको लोक सेवा परीक्षा, प्रश्न-प्रश्न गर्दै।',
      );
  String get heroSubtitle => t(
        'Practice with randomised MCQs, timed mocks that copy the real paper, and a dashboard that shows exactly where you stand.',
        'अनियमित प्रश्नहरू, वास्तविक परीक्षा जस्तै टाइम्ड मक, र तपाईं कहाँ उभिनुभएको छ देखाउने ड्यासबोर्ड।',
      );
  String get startPracticing => t('Start practicing', 'अभ्यास सुरु गर्नुहोस्');
  String get takeMock => t('Take a mock exam', 'मक परीक्षा दिनुहोस्');
  String get questionsLabel => t('questions', 'प्रश्नहरू');
  String get examsLabel => t('exams', 'परीक्षाहरू');
  String get bilingualLabel => t('bilingual', 'द्विभाषिक');
  String get noLoginLabel => t('login needed', 'लगइन आवश्यक');
  String get trustRow => t(
        'Open source \u00b7 No login \u00b7 No ads \u00b7 No tracking',
        'ओपन सोर्स \u00b7 लगइन छैन \u00b7 विज्ञापन छैन \u00b7 ट्र्याकिङ छैन',
      );

  // --- countdown / reminders ---
  String get nextExam => t('Next exam', 'आगामी परीक्षा');
  String get today => t('Today', 'आज');
  String get tomorrow => t('Tomorrow', 'भोलि');
  String daysCount(int n) => t('in $n days', '$n दिनमा');
  String get todayBang => t('\ud83c\udfaf Today!', '\ud83c\udfaf आज!');
  String get practiceNow => t('Practice now', 'अहिले अभ्यास');
  String get remindMe =>
      t('\ud83d\udd14 Remind me', '\ud83d\udd14 सम्झाउनुहोस्');
  String get remindOn => t('Reminder on', 'रिमाइन्डर अन');
  String get remindOff => t('Remind me', 'सम्झाउनुहोस्');
  String get allDates => t('All dates', 'सबै मितिहरू');
  String get reverifyNote => t(
      'Re-verify on the official site before travelling.',
      'यात्रा गर्नुअघि आधिकारिक साइटमा पुनः पुष्टि गर्नुहोस्।',);
  String get kindExam => t('Exam', 'परीक्षा');
  String get kindAdmit => t('Admit card', 'प्रवेशपत्र');
  String get kindDeadline => t('Deadline', 'अन्तिम मिति');

  // --- practice setup ---
  String get practiceTitle => t('Practice', 'अभ्यास');
  String get chooseExam => t('Choose exam', 'परीक्षा छान्नुहोस्');
  String get searchExamsHint => t('Search exams…', 'परीक्षा खोज्नुहोस्…');
  String get recentExams => t('Recent', 'हालैका');
  String get clearSearch => t('Clear search', 'खोज खाली गर्नुहोस्');
  String get noExamsFound =>
      t('No exams match your search.', 'तपाईंको खोजसँग मिल्ने परीक्षा भेटिएन।');
  String get chooseTopics => t('Choose topics', 'विषय छान्नुहोस्');
  String get chooseDifficulty => t('Difficulty', 'कठिनाइ');
  String get chooseCount => t('Questions', 'प्रश्न संख्या');
  String get diffMixed => t('Mixed', 'मिश्रित');
  String get diffEasy => t('Easy', 'सजिलो');
  String get diffMedium => t('Medium', 'मध्यम');
  String get diffHard => t('Hard', 'गाह्रो');
  String get startQuiz => t('Start', 'सुरु गर्नुहोस्');
  String get loadingQuestions =>
      t('Loading questions\u2026', 'प्रश्नहरू लोड हुँदै\u2026');

  // --- footer ---
  String get footerCredit =>
      t('Created by Ravi Yadav', 'रवि यादव द्वारा निर्मित');
  String get websiteTitle => t('Website', 'वेबसाइट');
  String get openLinkFailed =>
      t("Couldn't open the link.", 'लिङ्क खोल्न सकिएन।');

  // --- about / privacy / share / updates (v1.0.2) ---
  String get aboutTitle => t('About this app', 'एपबारे');
  String get aboutTagline => t(
        'Free Lok Sewa exam preparation for Nepal — practice questions, mock exams, exam dates and reminders.',
        'नेपालका लागि निःशुल्क लोक सेवा परीक्षा तयारी — अभ्यास प्रश्न, मॉक परीक्षा, परीक्षा मिति र रिमाइन्डर।',
      );
  String get versionLabel => t('Version', 'संस्करण');
  String get madeInNepal => t('Made in Nepal', 'नेपालमा निर्मित');
  String get openSourceLicences =>
      t('Open-source licences', 'ओपन-सोर्स लाइसेन्स');
  String get dataSourcesTitle => t('Data sources', 'डेटा स्रोत');
  String get dataSourcesBody => t(
        'Exam dates come from Public Service Commission notices. Questions are original model questions, plus transcribed previous-year papers. Data is bundled with the app — no account needed to study. An internet connection is required to open the app.',
        'परीक्षा मितिहरू लोक सेवा आयोगका सूचनाबाट लिइएका हुन्। प्रश्नहरू मौलिक मोडेल प्रश्न र अघिल्ला वर्षका प्रश्नपत्रहरू हुन्। डेटा एपमै समावेश छ — पढ्न खाता चाहिँदैन। एप खोल्न इन्टरनेट चाहिन्छ।',
      );
  String get privacyTitle => t('Privacy Policy', 'गोपनीयता नीति');
  String get shareTitle => t('Share the app', 'एप सेयर गर्नुहोस्');
  String get checkUpdatesTitle => t('Check for updates', 'अपडेट जाँच गर्नुहोस्');
  String get checkingForUpdates =>
      t('Checking for updates…', 'अपडेट जाँच हुँदै…');
  String get upToDate => t('You are up to date', 'तपाईं अपडेट हुनुहुन्छ');
  String get upToDateBody =>
      t('You have the latest version.', 'तपाईंसँग पछिल्लो संस्करण छ।');
  String get updateAvailable => t('Update available', 'अपडेट उपलब्ध छ');
  String updateAvailableBody(String v) => t(
        'Version $v is available. Download it now?',
        'संस्करण $v उपलब्ध छ। अहिले डाउनलोड गर्ने?',
      );
  String get download => t('Download', 'डाउनलोड');
  String get later => t('Later', 'पछि');
  String get checkFailed => t(
        "Couldn't check for updates. Check your connection and try again.",
        'अपडेट जाँच्न सकिएन। इन्टरनेट जाँचेर फेरि प्रयास गर्नुहोस्।',
      );
  String get shareMessage => t(
        'LokSewa Vidyapeeth — free Lok Sewa exam prep: 47 exams, over 64,000 practice questions, mock exams and exam dates. No login, no ads.\n\nDownload: https://github.com/08raviyadav/loksewa-prep-nepal/releases/latest/download/app-release.apk',
        'लोक सेवा विद्यापीठ — निःशुल्क लोक सेवा परीक्षा तयारी: ४७ परीक्षा, ६४,००० भन्दा बढी अभ्यास प्रश्न, मॉक परीक्षा र परीक्षा मिति। खाता छैन, विज्ञापन छैन।\n\nडाउनलोड: https://github.com/08raviyadav/loksewa-prep-nepal/releases/latest/download/app-release.apk',
      );

  String examKindLabel(String kind) {
    switch (kind) {
      case 'admit':
        return kindAdmit;
      case 'deadline':
        return kindDeadline;
      default:
        return kindExam;
    }
  }
}
