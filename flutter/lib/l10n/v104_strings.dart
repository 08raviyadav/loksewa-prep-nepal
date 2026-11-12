/// v1.0.4 strings: network gate, Daily Challenge home card, Question of
/// the Day, My Mistakes, Invite friends. Extension on [AppStrings]
/// (per the milestone convention — app_strings.dart stays untouched).
library;

import 'app_strings.dart';

extension V104Strings on AppStrings {
  // --- network gate (v1.0.4) ---
  String get noInternetTitle => t('No internet connection', 'इन्टरनेट छैन');
  String get noInternetBody => t(
        'LokSewa Vidyapeeth needs an internet connection to open. Check your connection and try again.',
        'लोक सेवा विद्यापीठ खोल्न इन्टरनेट चाहिन्छ। तपाईंको इन्टरनेट जाँचेर फेरि प्रयास गर्नुहोस्।',
      );
  String get retryLabel => t('Retry', 'फेरि प्रयास');
  String get connectingLabel => t('Connecting…', 'जोडिँदै…');

  // --- daily challenge home card (v1.0.4) ---
  String get dailyCardBody => t(
        '10 questions, fresh every day — the same set for everyone.',
        '१० प्रश्न, हरेक दिन नयाँ — सबैका लागि एउटै सेट।',
      );
  String get dailyStart => t(
        "Start today's challenge",
        'आजको चुनौती सुरु गर्नुहोस्',
      );
  String get dailyDoneLabel => t('Done today ✓', 'आज सकियो ✓');

  // --- question of the day (v1.0.4) ---
  String get qotdTitle => t('Question of the Day', 'आजको प्रश्न');
  String get qotdBody =>
      t('One question, fresh every day.', 'एउटा प्रश्न, हरेक दिन नयाँ।');
  String get qotdAnswer => t('Answer it', 'उत्तर दिनुहोस्');
  String get qotdDoneLabel => t('Answered ✓', 'उत्तर दिइयो ✓');
  String get qotdTryAgain => t('Try again', 'फेरि प्रयास');

  // --- my mistakes (v1.0.4) ---
  String get mistakesTitle => t('My Mistakes', 'मेरा गल्तीहरू');
  String get mistakesEmptyTitle =>
      t('No mistakes yet', 'अहिलेसम्म कुनै गल्ती छैन');
  String get mistakesEmptyBody => t(
        'Questions you get wrong will appear here, grouped by exam. Answer one correctly in review and it leaves the list.',
        'तपाईंले गलत उत्तर दिनुभएका प्रश्नहरू यहाँ परीक्षाअनुसार देखिनेछन्। समीक्षामा सही उत्तर दिनुभयो भने त्यो सूचीबाट हट्छ।',
      );
  String mistakesCount(int n) =>
      t('$n mistake${n == 1 ? '' : 's'}', '$n गल्ती');
  String get mistakesRetryAll =>
      t('Retry all mistakes', 'सबै गल्ती दोहोर्याउनुहोस्');
  String mistakesRetrySample(int n) =>
      t('Retry $n random mistakes', '$n अनियमित गल्ती दोहोर्याउनुहोस्');
  String mistakesRetryExam(int n) =>
      t('Retry these $n', 'यी $n दोहोर्याउनुहोस्');
  String get mistakesReviewTitle => t('Mistake review', 'गल्ती समीक्षा');
  String get mistakesLoading =>
      t('Loading your mistakes…', 'गल्तीहरू लोड हुँदै…');
  String get mistakesCorrectAnswer => t('Correct answer', 'सही उत्तर');

  // --- invite friends (v1.0.4) ---
  String get inviteTitle => t('Invite friends', 'साथीहरूलाई निम्त्याउनुहोस्');
  String get inviteMessage => t(
        "I'm preparing for Lok Sewa exams with LokSewa Vidyapeeth — free practice questions, mock exams and exam dates. Join me!\n\nDownload: https://github.com/08raviyadav/loksewa-prep-nepal/releases/latest/download/app-release.apk",
        'म लोक सेवा विद्यापीठबाट लोक सेवा परीक्षाको तयारी गर्दैछु — निःशुल्क अभ्यास प्रश्न, मॉक परीक्षा र परीक्षा मिति। मसँग जोडिनुहोस्!\n\nडाउनलोड: https://github.com/08raviyadav/loksewa-prep-nepal/releases/latest/download/app-release.apk',
      );
}
