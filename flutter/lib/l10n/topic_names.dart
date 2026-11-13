/// Nepali names for the question bank's topics and difficulty labels
/// (v1.0.9).
///
/// Topic/difficulty strings come from the data in English; in Nepali
/// mode the quiz chips and the result screen's topic breakdown show
/// these translations instead. Unknown values fall back to the English
/// original — never a crash, never blank.
///
/// The map covers all 25 distinct `topic` values in the bank
/// (data/questions/*.json, counted 2026-11-13). If a new topic appears
/// in the data later it renders in English until it is added here.
library;

/// Nepali name per English topic string.
const Map<String, String> topicNamesNe = {
  'Banking & Finance': 'बैंकिङ तथा वित्त',
  'Biology': 'जीवविज्ञान',
  'Chemistry': 'रसायनशास्त्र',
  'Computer & ICT': 'कम्प्युटर तथा सूचना प्रविधि',
  'Constitution & Governance': 'संविधान तथा शासन',
  'Culture & Society': 'संस्कृति तथा समाज',
  'Current Affairs': 'समसामयिक घटना',
  'Economy': 'अर्थतन्त्र',
  'Economy & Development': 'अर्थतन्त्र तथा विकास',
  'Education & Pedagogy': 'शिक्षा तथा शिक्षणशास्त्र',
  'Engineering Drawing': 'इन्जिनियरिङ ड्रइङ',
  'English': 'अङ्ग्रेजी',
  'Foreign Service & Diplomacy': 'परराष्ट्र सेवा तथा कूटनीति',
  'Health/Technical basics': 'स्वास्थ्य/प्राविधिक आधारभूत',
  'IQ': 'आईक्यू',
  'IQ & Reasoning': 'आईक्यू तथा तर्कशक्ति',
  'Law': 'कानुन',
  'Mathematics': 'गणित',
  'Maths & Numerical': 'गणित तथा संख्यात्मक',
  'Nepal Geography': 'नेपालको भूगोल',
  'Nepal History': 'नेपालको इतिहास',
  'Nepali Language': 'नेपाली भाषा',
  'Office Management & Public Service': 'कार्यालय व्यवस्थापन तथा सार्वजनिक सेवा',
  'Physics': 'भौतिकशास्त्र',
  'Science & Tech': 'विज्ञान तथा प्रविधि',
};

/// Nepali label per difficulty value (easy | medium | hard).
const Map<String, String> difficultyNamesNe = {
  'easy': 'सजिलो',
  'medium': 'मध्यम',
  'hard': 'गाह्रो',
};

/// Display name for a topic: Nepali in Nepali mode, English otherwise.
/// Unmapped topics fall back to the English original.
String topicLabel(String topic, bool ne) =>
    ne ? (topicNamesNe[topic] ?? topic) : topic;

/// Display label for a difficulty: Nepali in Nepali mode, English
/// otherwise. Unknown values fall back to the raw value.
String difficultyLabel(String difficulty, bool ne) =>
    ne ? (difficultyNamesNe[difficulty] ?? difficulty) : difficulty;
