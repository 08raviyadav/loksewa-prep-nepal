/// Funny Nepali result slangs (v1.0.8): after every quiz / mock, the result
/// screen shows ONE random line from the band matching the score. Bilingual:
/// app language English -> Roman Nepali, Nepali -> Devanagari. Cool and
/// encouraging, never mean. Mom lines are labeled "Aama:" / "आमा:".
///
/// Copy is user-approved (see workspace `loksewa-result-slangs.md`) — do not
/// reword the lines; add new ones only with the user's approval.
library;

import 'dart:math';

/// One slang line in both scripts.
class ResultSlang {
  final String roman;
  final String nepali;
  const ResultSlang({required this.roman, required this.nepali});

  /// The line in the script matching the app language.
  String text(bool isNepali) => isNepali ? nepali : roman;
}

/// Perfect — 100%.
const perfectSlangs = <ResultSlang>[
  ResultSlang(
    roman: 'Katxa tero Loksewa! 🔥',
    nepali: 'कट्छ तेरो लोकसेवा! 🔥',
  ),
  ResultSlang(
    roman: 'Sarkari jagir pakka! 💪',
    nepali: 'सरकारी जागिर पक्का! 💪',
  ),
  ResultSlang(
    roman: 'Topper ho timi ta! 🏆',
    nepali: 'टपर हो तिमी त! 🏆',
  ),
  ResultSlang(
    roman: 'Yesto dimag, PSC le khojeko manche! 🧠',
    nepali: 'यस्तो दिमाग, PSC ले खोजेको मान्छे! 🧠',
  ),
];

/// Good — 80–99%.
const goodSlangs = <ResultSlang>[
  ResultSlang(
    roman: 'Ali ali matra baki, katxa! 💪',
    nepali: 'अलि अलि मात्र बाँकी, कट्छ! 💪',
  ),
  ResultSlang(
    roman: 'Damdar! Najikai chau! 👏',
    nepali: 'दमदार! नजिकै छौ! 👏',
  ),
  ResultSlang(
    roman: 'Gajjab! Keep it up! 🔥',
    nepali: 'गज्जब! Keep it up! 🔥',
  ),
  ResultSlang(
    roman: 'Ballai ballai pugyo, aba top garne! 🚀',
    nepali: 'बल्ल बल्ल पुग्यो, अब टप गर्ने! 🚀',
  ),
];

/// Average — 50–79%.
const averageSlangs = <ResultSlang>[
  ResultSlang(
    roman: 'Thikai cha, tara ajhai mehenat gara hai! 📚',
    nepali: 'ठिकै छ, तर अझै मेहनत गर है! 📚',
  ),
  ResultSlang(
    roman: 'Ramro suruwat, aba speed badhau! 🚀',
    nepali: 'राम्रो सुरुवात, अब स्पीड बढाऊ! 🚀',
  ),
  ResultSlang(
    roman: 'Hunchha, hunchha — ali ali gardai! 💪',
    nepali: 'हुन्छ, हुन्छ — अलि अलि गर्दै! 💪',
  ),
  ResultSlang(
    roman: 'Aama: "Ali dherai padheko bhaye top hunthyo ni!" 😄',
    nepali: 'आमा: "अलि धेरै पढेको भए टप हुन्थ्यो नि!" 😄',
  ),
];

/// Low — below 50%.
const lowSlangs = <ResultSlang>[
  ResultSlang(
    roman: 'Babu yo taal le hudaina! 😅',
    nepali: 'बाबु यो तालले हुँदैन! 😅',
  ),
  ResultSlang(
    roman: 'Diya tale adhyaro raixas bhai ta! 🪔',
    nepali: 'दियो तले अध्यारो रैछ भाइ त! 🪔',
  ),
  ResultSlang(
    roman: 'Coffee khau, kitab khol, feri try gara! ☕',
    nepali: 'कफी खाऊ, किताब खोल, फेरि ट्राई गर! ☕',
  ),
  ResultSlang(
    roman: 'Aaja chipliyau, bholi jitchau! 🌅',
    nepali: 'आज चिप्लियौ, भोलि जित्छौ! 🌅',
  ),
  ResultSlang(
    roman: 'Aama: "Aru chala TikTok, video herdai bas ani exam katxa tyo!" 😄',
    nepali: 'आमा: "अरू चला TikTok, भिडियो हेर्दै बस अनि एक्जाम कट्छ त्यो!" 😄',
  ),
  ResultSlang(
    roman: 'Aama: "Mobile matra chalauchas, kitab kahile kholne?" 📱',
    nepali: 'आमा: "मोबाइल मात्र चलाउँछस्, किताब कहिले खोल्ने?" 📱',
  ),
  ResultSlang(
    roman: 'Aama: "Chimeki ko chora le ta Lok Sewa pass gari sakyo!" 😄',
    nepali: 'आमा: "छिमेकीको छोराले त लोक सेवा पास गरिसक्यो!" 😄',
  ),
  ResultSlang(
    roman:
        'Padhna man lagdaina? Aaja dekhi suru gara, bholi dekhi hoina! 📚',
    nepali: 'पढ्न मन लाग्दैन? आज देखि सुरु गर, भोलि देखि होइन! 📚',
  ),
];

/// Every slang line, all bands (20 total).
const allResultSlangs = <ResultSlang>[
  ...perfectSlangs,
  ...goodSlangs,
  ...averageSlangs,
  ...lowSlangs,
];

/// The band a score falls in: 100% perfect, 80–99% good, 50–79% average,
/// below 50% low. `total <= 0` (no questions) counts as low.
List<ResultSlang> slangBandFor(double score, num total) {
  final pct = total <= 0 ? 0.0 : score / total * 100;
  if (pct >= 100) return perfectSlangs;
  if (pct >= 80) return goodSlangs;
  if (pct >= 50) return averageSlangs;
  return lowSlangs;
}

/// Picks ONE random line from the band matching [score] / [total].
/// Pass a seeded [Random] in tests for determinism.
ResultSlang pickResultSlang(double score, num total, [Random? random]) {
  final band = slangBandFor(score, total);
  return band[(random ?? Random()).nextInt(band.length)];
}

/// Convenience: the picked line in the script matching the app language
/// ([isNepali] true -> Devanagari, false -> Roman Nepali).
String pickResultSlangText(double score, num total, bool isNepali) =>
    pickResultSlang(score, total).text(isNepali);
