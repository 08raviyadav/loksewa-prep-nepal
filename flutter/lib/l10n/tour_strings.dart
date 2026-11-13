/// v1.0.7 strings: first-launch guided tour. Extension on [AppStrings]
/// (per the milestone convention — app_strings.dart stays untouched).
library;

import 'app_strings.dart';

extension TourStrings on AppStrings {
  // --- shared tour chrome ---
  String get tourSkip => t('Skip', 'छोड्नुहोस्');
  String get tourNext => t('Next', 'अर्को');
  String get tourTapHint =>
      t('Tap the highlighted button', 'हाइलाइट भएको बटन थिच्नुहोस्');
  String get tourReplayTitle =>
      t('How to use the app', 'एप कसरी प्रयोग गर्ने');

  // --- step 1: Daily Challenge card ---
  String get tourDailyTitle => t('Daily Challenge', 'दैनिक चुनौती');
  String get tourDailyBody => t(
        'Start here every day — a fresh 10-question challenge.',
        'हरेक दिन यहाँबाट सुरु गर्नुहोस् — नयाँ १० प्रश्नको चुनौती।',
      );

  // --- step 2: Dashboard tab ---
  String get tourDashboardTitle => t('Your Dashboard', 'तपाईंको ड्यासबोर्ड');
  String get tourDashboardBody => t(
        'Track your XP, streak and badges here.',
        'यहाँ XP, स्ट्रिक र ब्याजहरू हेर्नुहोस्।',
      );

  // --- step 3: Practice tab (tap) ---
  String get tourPracticeTitle => t('Practice', 'अभ्यास');
  String get tourPracticeBody => t(
        'Tap Practice to study any exam.',
        'परीक्षा अभ्यास गर्न अभ्यास ट्याब थिच्नुहोस्।',
      );

  // --- step 4: first exam category (tap) ---
  String get tourCategoryTitle => t('Pick a category', 'श्रेणी छान्नुहोस्');
  String get tourCategoryBody => t(
        'Tap a category to see its exams.',
        'परीक्षाहरू हेर्न श्रेणी थिच्नुहोस्।',
      );

  // --- step 5: first exam chip (tap) ---
  String get tourExamTitle => t('Pick your exam', 'परीक्षा छान्नुहोस्');
  String get tourExamBody => t(
        'Tap an exam to practise it.',
        'अभ्यास गर्न परीक्षा थिच्नुहोस्।',
      );

  // --- step 6: first topic chip (tap) ---
  String get tourTopicTitle => t('Pick a topic', 'विषय छान्नुहोस्');
  String get tourTopicBody => t(
        'Choose a topic to practise.',
        'अभ्यास गर्न विषय थिच्नुहोस्।',
      );

  // --- step 7: Start button (tap) ---
  String get tourStartTitle => t('Start the quiz', 'क्विज सुरु गर्नुहोस्');
  String get tourStartBody => t(
        'Tap Start to begin the quiz.',
        'क्विज सुरु गर्न यो बटन थिच्नुहोस्।',
      );
}
