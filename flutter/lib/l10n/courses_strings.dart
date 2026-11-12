/// Courses (theory) strings. Added ONLY as an extension on [AppStrings]
/// (never edit app_strings.dart) — every string bilingual EN/NE.
/// Copy matches the vanilla site's courses UI (assets/js/app.js,
/// "Theory courses" section).
library;

import 'app_strings.dart';

extension CoursesStrings on AppStrings {
  // --- exam picker ---
  String get coursesTitle => t('📚 Theory Courses', '📚 सैद्धान्तिक पाठ्यक्रम');
  String get coursesSubtitle => t(
        'Read the theory chapter by chapter, then jump straight into practice. Progress is saved on this device.',
        'अध्यायअनुसार सिद्धान्त पढ्नुहोस्, अनि सिधै अभ्यासमा जानुहोस्। प्रगति यसै डिभाइसमा सेभ हुन्छ।',
      );
  String get loadingCourses => t('Loading courses…', 'पाठ्यक्रम लोड हुँदै…');
  String get noCoursesYet => t('No courses yet', 'अझै पाठ्यक्रम छैन');
  String get coursesOnWay =>
      t('Theory courses are on the way.', 'सैद्धान्तिक पाठ्यक्रमहरू आउँदैछन्।');
  String get firstPaperTheory =>
      t('First Paper — Theory', 'प्रथम पत्र — सिद्धान्त');
  String chaptersRead(int n) => t('$n chapters read', '$n अध्याय पढियो');
  String get continueStudying => t('Continue', 'जारी राख्नुहोस्');
  String get startStudying => t('Start studying', 'पढ्न सुरु गर्नुहोस्');
  String get allCourses => t('All courses', 'सबै पाठ्यक्रम');
  String get syllabusReverify =>
      t('Re-verify syllabus', 'पाठ्यक्रम पुनःपुष्टि गर्नुहोस्');

  // --- subject / chapter list ---
  String get complete => t('complete', 'पूरा');
  String keyPointsCount(int n) => t('$n key points', '$n मुख्य बुँदा');
  String get chaptersLabel => t('chapters', 'अध्याय');

  // --- chapter reader ---
  String get keyPointsHeading => t('⭐ Key points', '⭐ मुख्य बुँदाहरू');
  String get practiceThisChapter =>
      t('✏️ Practice this chapter', '✏️ यो अध्याय अभ्यास गर्नुहोस्');
  String get markAsRead => t('📖 Mark as read', '📖 पढेको चिन्ह लगाउनुहोस्');
  String get readMarkUnread =>
      t('✅ Read — mark unread', '✅ पढियो — नपढेको चिन्ह');
  String get previousChapter => t('Previous', 'अघिल्लो');
  String get nextChapter => t('Next', 'अर्को');
  String get chapterNotFound => t('Chapter not found.', 'अध्याय भेटिएन।');

  // --- Home "Continue studying" card (integration hook for Home screen) ---
  String get continueStudyingTitle =>
      t('📚 Continue studying', '📚 पढाइ जारी राख्नुहोस्');
  String continueStudyingSub(String chapterTitle, int pct) =>
      t('$chapterTitle · $pct% complete', '$chapterTitle · $pct% पूरा');
  String get resume => t('Resume', 'सुरु गर्नुहोस्');
}
