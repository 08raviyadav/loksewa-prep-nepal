/// Privacy Policy text (EN + NE), v1.0.2.
///
/// The same text is published as PRIVACY.md in the repo root — the
/// hosted copy the Play Store listing will point at. Keep both in sync
/// when the policy changes.
library;

class PrivacyStrings {
  final bool isNe;
  const PrivacyStrings(this.isNe);

  String t(String en, String ne) => isNe ? ne : en;

  String get lastUpdated =>
      t('Last updated: 12 November 2026', 'अन्तिम अपडेट: १२ नोभेम्बर २०२६');

  String get intro => t(
        'LokSewa Vidyapeeth is built to respect your privacy. In short: the app collects nothing about you, and everything you do in it stays on your phone.',
        'लोक सेवा विद्यापीठ तपाईंको गोपनीयताको सम्मान गर्न बनाइएको हो। छोटकरीमा: एपले तपाईंको बारेमा केही संकलन गर्दैन, र तपाईंले यसमा गर्ने सबै कुरा तपाईंको फोनमै रहन्छ।',
      );

  /// (title, body) pairs, in display order.
  List<(String, String)> get sections => [
        (
          t('What we collect', 'हामी के संकलन गर्छौं'),
          t(
            'Nothing. LokSewa Vidyapeeth has no accounts, no sign-in, no analytics, no advertising and no tracking. We do not collect your name, email, phone number, location or device identifiers.',
            'केही पनि होइन। लोक सेवा विद्यापीठमा खाता छैन, साइन-इन छैन, एनालिटिक्स छैन, विज्ञापन छैन र ट्र्याकिङ छैन। हामी तपाईंको नाम, इमेल, फोन नम्बर, स्थान वा डिभाइस विवरण संकलन गर्दैनौं।',
          ),
        ),
        (
          t('What stays on your phone', 'तपाईंको फोनमा के रहन्छ'),
          t(
            'Your progress, XP, streaks, bookmarks, reminders and community posts are stored only on your device. If you uninstall the app, that data is deleted with it. We have no server copy and cannot see it.',
            'तपाईंको प्रगति, XP, स्ट्रीक, बुकमार्क, रिमाइन्डर र सामुदायिक पोस्टहरू तपाईंको डिभाइसमै मात्र भण्डारण हुन्छन्। एप अनइन्स्टल गरेपछि त्यो डेटा पनि मेटिन्छ। हामीसँग सर्भरमा कुनै प्रतिलिपि छैन र हामी त्यो देख्न सक्दैनौं।',
          ),
        ),
        (
          t('Internet use', 'इन्टरनेट प्रयोग'),
          t(
            'The app works fully offline. It connects to the internet only when you ask it to: Check for updates (reads the latest release on GitHub), opening a link (your browser), or sharing (your phone\'s share sheet). The app itself sends no data anywhere.',
            'एप पूर्ण रूपमा अफलाइन काम गर्छ। तपाईंले भन्दा मात्र यो इन्टरनेटमा जोडिन्छ: अपडेट जाँच (GitHub मा पछिल्लो रिलिज पढ्छ), लिङ्क खोल्दा (तपाईंको ब्राउजर), वा सेयर गर्दा (फोनको सेयर सिट)। एप आफैंले कतै पनि डेटा पठाउँदैन।',
          ),
        ),
        (
          t('Reminders', 'रिमाइन्डर'),
          t(
            'Exam reminders are scheduled on your phone only. No reminder data leaves your device.',
            'परीक्षा रिमाइन्डरहरू तपाईंको फोनमै मात्र सेट हुन्छन्। रिमाइन्डर डेटा तपाईंको डिभाइसबाट बाहिर जाँदैन।',
          ),
        ),
        (
          t('Changes to this policy', 'नीतिमा परिवर्तन'),
          t(
            'If this policy changes, the new version will ship with an app update and be published at github.com/08raviyadav/loksewa-prep-nepal/blob/main/PRIVACY.md.',
            'यो नीति परिवर्तन भएमा नयाँ संस्करण एप अपडेटसँग आउँछ र github.com/08raviyadav/loksewa-prep-nepal/blob/main/PRIVACY.md मा प्रकाशित हुन्छ।',
          ),
        ),
        (
          t('Contact', 'सम्पर्क'),
          t(
            'Questions about this policy: open an issue at github.com/08raviyadav/loksewa-prep-nepal, or reach the developer at raviyadav.com.np.',
            'यो नीतिबारे प्रश्न छन् भने github.com/08raviyadav/loksewa-prep-nepal मा issue खोल्नुहोस् वा raviyadav.com.np मा विकासकर्तालाई सम्पर्क गर्नुहोस्।',
          ),
        ),
      ];
}
