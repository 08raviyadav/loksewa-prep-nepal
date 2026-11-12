/// Community strings. Added ONLY as an extension on [AppStrings]
/// (never edit app_strings.dart) — every string bilingual EN/NE.
///
/// Copy matches the vanilla site's discussion / submit / suggest sections
/// (loksewa-prep-nepal/assets/js/app.js) wherever the Flutter screen shows
/// the same message.
library;

import 'app_strings.dart';

extension CommunityStrings on AppStrings {
  // --- shared honesty copy ---
  String get communityLocalPreview => t(
        'Local preview — posts are saved on this device only until the online backend is connected.',
        'स्थानीय पूर्वावलोकन — ब्याकएन्ड अनलाइन नजोडिएसम्म पोस्टहरू यो डिभाइसमा मात्र सेभ हुन्छन्।',
      );

  String get suggestLocalPreview => t(
        'Local preview — visible only on this device until the online backend is connected.',
        'स्थानीय पूर्वावलोकन — ब्याकएन्ड अनलाइन नजोडिएसम्म यो डिभाइसमा मात्र देखिन्छ।',
      );

  String postingAs(String name) => '${t('Posting as', 'पोस्ट गर्दै')}: $name';

  // --- discussion hub ---
  String get discussionTitle => t('Discussion Hub', 'छलफल केन्द्र');
  String get startThread => t('Start a thread', 'थ्रेड सुरु गर्नुहोस्');
  String get examTopic => t('Exam / topic', 'परीक्षा / विषय');
  String get threadTitleLabel => t('Title', 'शीर्षक');
  String get threadBodyLabel =>
      t('Your question / doubt', 'तपाईंको प्रश्न / शङ्का');
  String get postThreadBtn => t('Post thread', 'थ्रेड पोस्ट गर्नुहोस्');
  String threadsCount(int n) => '${t('Threads', 'थ्रेडहरू')} ($n)';
  String get upvote => t('Upvote', 'मत दिनुहोस्');
  String get reportBtn => t('Report', 'रिपोर्ट');
  String get replyBtn => t('Reply', 'उत्तर दिनुहोस्');
  String replyAs(String name) => '${t('Reply as', 'उत्तर दिने')}: $name';
  String get replyPlaceholder =>
      t('Write a helpful reply…', 'सहयोगी उत्तर लेख्नुहोस्…');
  String get noThreads => t('No threads yet', 'अझै थ्रेड छैन');
  String get noThreadsBlurb => t(
        'Start the first discussion — ask a doubt or share a tip with fellow aspirants.',
        'पहिलो छलफल सुरु गर्नुहोस् — शङ्का सोध्नुहोस् वा साथी परीक्षार्थीसँग सुझाव बाँड्नुहोस्।',
      );
  String get sortNew => t('New', 'नयाँ');
  String get sortTop => t('Top', 'लोकप्रिय');
  String get generalDoubts => t('General doubts', 'सामान्य शङ्काहरू');
  String get byLabel => t('by', '—');

  // report dialog
  String get reportDialogTitle =>
      t('Report this post', 'यो पोस्ट रिपोर्ट गर्नुहोस्');
  String get reportWhy =>
      t('Why are you reporting it?', 'किन रिपोर्ट गर्दै हुनुहुन्छ?');
  String reportReason(String id) {
    switch (id) {
      case 'spam':
        return t('Spam', 'स्पाम');
      case 'wrong':
        return t('Wrong info', 'गलत जानकारी');
      case 'abusive':
        return t('Abusive', 'अभद्र');
      default:
        return t('Other', 'अन्य');
    }
  }

  String get reportThanks => t(
        'Thanks — the report is saved on this device (local preview) for the maintainer to review.',
        'धन्यवाद — समीक्षकले हेर्नका लागि रिपोर्ट यो डिभाइसमा सेभ गरिएको छ (स्थानीय पूर्वावलोकन)।',
      );
  String get cancelBtn => t('Cancel', 'रद्द गर्नुहोस्');
  String get submitBtn => t('Submit', 'पेस गर्नुहोस्');

  // --- submit a question ---
  String get submitTitle => t('Submit a question', 'प्रश्न पेस गर्नुहोस्');
  String get reviewBannerTitle =>
      t('Reviewed before publishing.', 'प्रकाशनअघि समीक्षा हुन्छ।');
  String get reviewBannerBody => t(
        'Submissions go through automatic checks (duplicate detection, spam heuristics, rate limit) and maintainer review. First-time submissions never go live instantly — every one is reviewed before it can appear.',
        'पेस गरिएका प्रश्न स्वचालित जाँच (डुप्लिकेट पहिचान, स्पाम नियम, दर सीमा) र समीक्षक समीक्षाबाट जान्छन्। पहिलो पेस कहिल्यै तुरुन्त लाइभ हुँदैन — हरेक प्रश्न लाइभ हुनुअघि समीक्षा हुन्छ।',
      );
  String modLogLine(int approved, int rejected, int pending) => t(
        'Public moderation log — approved $approved · rejected $rejected · pending $pending',
        'सार्वजनिक समीक्षा लग — स्वीकृत $approved · अस्वीकृत $rejected · पेन्डिङ $pending',
      );
  String get safetyNote => t(
        'Safety checks: duplicate detection, spam heuristics, max 5 submissions per hour per device. First-time submissions never go live instantly.',
        'सुरक्षा जाँच: डुप्लिकेट पहिचान, स्पाम नियम, प्रति डिभाइस प्रति घण्टा बढीमा ५ पेस। पहिलो पेस कहिल्यै तुरुन्त लाइभ हुँदैन।',
      );
  String get captchaNote => t(
        'CAPTCHA is added when the online backend is connected. In local preview the rate limit (5/hour) and duplicate/spam checks run instead.',
        'ब्याकएन्ड अनलाइन जडान हुँदा CAPTCHA थपिन्छ। स्थानीय पूर्वावलोकनमा दर सीमा (५/घण्टा) र डुप्लिकेट/स्पाम जाँच चल्छ।',
      );

  String get fExam => t('Exam', 'परीक्षा');
  String get fTopic => t('Topic', 'विषय');
  String get fSubtopic => t('Subtopic', 'उपविषय');
  String get fDifficulty => t('Difficulty', 'कठिनाइ');
  String get fMarks => t('Marks', 'अङ्क');
  String get fQuestionEn => t(
        'Question (English) — at least 15 characters, no links here',
        'प्रश्न (अङ्ग्रेजी) — कम्तीमा १५ अक्षर, यहाँ लिङ्क नराख्नुहोस्',
      );
  String get fQuestionNe => t('Question (Nepali)', 'प्रश्न (नेपाली)');
  String get fOptionsEn => t(
        'Options (English) — 4 different options',
        'विकल्पहरू (अङ्ग्रेजी) — ४ फरक विकल्प',
      );
  String get fOptionsNe => t(
        'Options (Nepali) — 4 different options',
        'विकल्पहरू (नेपाली) — ४ फरक विकल्प',
      );
  String optionPh(String letter, bool nepali) =>
      t('Option $letter (English)', 'विकल्प $letter (नेपाली)');
  String get fAnswer => t('Correct answer', 'सही उत्तर');
  String get fAnswerChoose => t('— choose —', '— छान्नुहोस् —');
  String get fExplanationEn =>
      t('Explanation (English)', 'व्याख्या (अङ्ग्रेजी)');
  String get fExplanationNe => t('Explanation (Nepali)', 'व्याख्या (नेपाली)');
  String get fSource => t(
        'Source (required — URL or book / article name)',
        'स्रोत (आवश्यक — URL वा पुस्तक / लेखको नाम)',
      );
  String get fContributor => t('Contributor name', 'योगदानकर्ताको नाम');

  String get submitForReview =>
      t('Submit for review', 'समीक्षाका लागि पेस गर्नुहोस्');
  String get submitDone => t(
        'Submitted for review — it will NOT go live instantly. A maintainer reviews every submission; first-time submissions never go live instantly. Thank you!',
        'समीक्षाका लागि पेस भयो — यो तुरुन्त लाइभ हुँदैन। हरेक पेस समीक्षा हुन्छ; पहिलो पेस कहिल्यै तुरुन्त लाइभ हुँदैन। धन्यवाद!',
      );
  String get submittingAs => t('Submitting as', 'पेस गर्दै');

  // review queue tab
  String get reviewQueueTitle => t('Review queue', 'समीक्षा कतार');
  String get mySubmissionsTitle => t('My submissions', 'मेरा पेसहरू');
  String get queuePreviewNote => t(
        'Maintainer preview — in this build the queue is the honest holding state: first-time submissions never go live instantly.',
        'समीक्षक पूर्वावलोकन — यो बिल्डमा कतार नै इमानदार होल्डिङ अवस्था हो: पहिलो पेस कहिल्यै तुरुन्त लाइभ हुँदैन।',
      );
  String get statusPending => t('Pending', 'पेन्डिङ');
  String get statusApproved => t('Approved', 'स्वीकृत');
  String get statusRejected => t('Rejected', 'अस्वीकृत');
  String get approveBtn => t('Approve', 'स्वीकृत गर्नुहोस्');
  String get rejectBtn => t('Reject', 'अस्वीकृत गर्नुहोस्');
  String get rejectReasonPh => t(
        'Rejection reason (required to reject)',
        'अस्वीकृति कारण (अस्वीकृत गर्न आवश्यक)',
      );
  String get rejectReasonNeeded => t(
        'Please give a reason for the rejection — the contributor sees it.',
        'कृपया अस्वीकृतिको कारण दिनुहोस् — योगदानकर्ताले हेर्छ।',
      );
  String get noPending => t('No pending submissions', 'कुनै पेन्डिङ पेस छैन');
  String get noPendingBlurb => t(
        'Submitted questions appear here for review.',
        'पेस गरिएका प्रश्नहरू समीक्षाका लागि यहाँ देखिन्छन्।',
      );
  String get noSubmissionsYet => t('No submissions yet', 'अझै कुनै पेस छैन');
  String rejectReasonLine(String reason) =>
      t('Rejected: ', 'अस्वीकृत: ') + reason;

  // --- suggestions ---
  String get suggestTitle => t('Suggest a feature', 'सुविधा सुझाव दिनुहोस्');
  String get suggestFormTitle => t('Title', 'शीर्षक');
  String get suggestTitlePh => t(
        'e.g. Spaced-repetition reminders',
        'जस्तै: स्पेस्ड-रिपिटिसन रिमाइन्डर',
      );
  String get suggestDescLabel => t('Description', 'विवरण');
  String get suggestDescPh => t(
        'What should it do, and why would it help aspirants? (min 20 characters)',
        'यसले के गर्ने र परीक्षार्थीलाई किन सहयोगी हुन्छ? (कम्तीमा २० अक्षर)',
      );
  String get suggestCatLabel => t('Category', 'श्रेणी');
  String get suggestSubmit => t('Submit suggestion', 'सुझाव पेस गर्नुहोस्');
  String get suggestRateNote => t(
        'Max 5 suggestions per hour per device.',
        'प्रति डिभाइस प्रति घण्टा बढीमा ५ सुझाव।',
      );
  String suggestionsCount(int n) =>
      '${t('Community suggestions', 'सामुदायिक सुझावहरू')} ($n)';
  String get suggestEmpty => t(
        'No suggestions yet — be the first!',
        'अझै कुनै सुझाव छैन — पहिलो बन्नुहोस्!',
      );
  String get suggestEmptyBlurb => t(
        'Ideas from aspirants shape what gets built next — tell us what would help your preparation.',
        'परीक्षार्थीका विचारले के बन्छ भन्ने तय गर्छ — तपाईंको तयारीलाई के सहयोगी हुन्छ भन्नुहोस्।',
      );
  String get suggestWriteCta => t('Write a suggestion', 'सुझाव लेख्नुहोस्');
  String get suggestDone => t(
        'Thanks! Your suggestion is on the list below (this device only, until the backend is connected).',
        'धन्यवाद! तपाईंको सुझाव तलको सूचीमा छ (ब्याकएन्ड नजोडिएसम्म यो डिभाइसमा मात्र)।',
      );
  String get exampleLabel => t('example', 'उदाहरण');

  String categoryLabel(String id) {
    switch (id) {
      case 'feature':
        return t('New feature', 'नयाँ सुविधा');
      case 'topic':
        return t('Topic request', 'विषय अनुरोध');
      case 'questions':
        return t('Question set', 'प्रश्न सेट');
      case 'exam':
        return t('New exam', 'नयाँ परीक्षा');
      case 'bug':
        return t('Bug report', 'बग रिपोर्ट');
      default:
        return t('Other', 'अन्य');
    }
  }

  // --- common ---
  String get fixThese =>
      t('Fix these before submitting:', 'पेस गर्नुअघि यी सच्याउनुहोस्:');
  String get fixTheseInline => t('Cannot submit yet:', 'अझै पेस गर्न सकिँदैन:');
}
