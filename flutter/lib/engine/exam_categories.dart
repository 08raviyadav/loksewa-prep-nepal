import '../models/models.dart';

/// Curated categories for the Practice exam picker.
///
/// 47 exams as one flat chip list meant endless scrolling to reach the
/// bottom (v1.0.0 feedback). The picker now shows one collapsible section
/// per category, so the whole list is ~8 headers + search.
///
/// Categories are keyed by exam id first (exact, stable), with a
/// recruiting-body keyword fallback so a future exam still lands in a
/// sensible group instead of vanishing. Anything unmatched goes to
/// "Other" — never dropped.
class ExamCategory {
  final String id;
  final String nameEn;
  final String nameNe;
  const ExamCategory(
      {required this.id, required this.nameEn, required this.nameNe,});

  String title(bool ne) => ne ? nameNe : nameEn;
}

const List<ExamCategory> examCategories = [
  ExamCategory(id: 'psc', nameEn: 'Lok Sewa (PSC)', nameNe: 'लोक सेवा (PSC)'),
  ExamCategory(
      id: 'tsc', nameEn: 'Teaching (TSC)', nameNe: 'शिक्षक सेवा (TSC)',),
  ExamCategory(id: 'banking', nameEn: 'Banking', nameNe: 'बैंकिङ'),
  ExamCategory(
      id: 'security', nameEn: 'Security Forces', nameNe: 'सुरक्षा निकाय',),
  ExamCategory(
      id: 'health', nameEn: 'Health Licences', nameNe: 'स्वास्थ्य लाइसेन्स',),
  ExamCategory(
      id: 'licence-entrance',
      nameEn: 'Licence & Entrance',
      nameNe: 'लाइसेन्स तथा प्रवेश परीक्षा',),
  ExamCategory(id: 'law', nameEn: 'Law & Justice', nameNe: 'कानून तथा न्याय'),
  ExamCategory(
      id: 'enterprise',
      nameEn: 'Public Enterprises',
      nameNe: 'सार्वजनिक संस्थान',),
  ExamCategory(id: 'other', nameEn: 'Other', nameNe: 'अन्य'),
];

ExamCategory categoryById(String id) => examCategories.firstWhere(
      (c) => c.id == id,
      orElse: () => examCategories.last,
    );

/// Exact id mapping for the 47 exams shipped in v1.0.0.
const Map<String, String> _categoryByExamId = {
  // Lok Sewa (PSC) — 14
  'kharidar': 'psc',
  'nasu': 'psc',
  'section-officer': 'psc',
  'health': 'psc',
  'engineering': 'psc',
  'deputy-secretary': 'psc',
  'sub-engineer': 'psc',
  'jta': 'psc',
  'ranger': 'psc',
  'computer-operator': 'psc',
  'foreign-service': 'psc',
  'psc-service-groups': 'psc',
  'staff-nurse-psc': 'psc',
  'provincial-psc': 'psc',
  // Teaching (TSC) — 4
  'tsc-primary': 'tsc',
  'tsc-secondary': 'tsc',
  'tsc-lower-secondary': 'tsc',
  'tsc-license': 'tsc',
  // Banking — 4
  'nrb-assistant': 'banking',
  'nrb-officer': 'banking',
  'rbb': 'banking',
  'rbb-senior-assistant': 'banking',
  // Security Forces — 2
  'police': 'security',
  'army': 'security',
  // Health Licences — 16
  'nhpc-ha': 'health',
  'nhpc-lab': 'health',
  'nhpc-radio': 'health',
  'nhpc-physio': 'health',
  'nhpc-public-health': 'health',
  'nhpc-optometry': 'health',
  'nhpc-dental': 'health',
  'nhpc-ayurveda': 'health',
  'nmc-mbbs': 'health',
  'nmc-bds': 'health',
  'nnc-rn': 'health',
  'midwifery-nlem': 'health',
  'anm-guide': 'health',
  'npc-pharmacy': 'health',
  'ayurveda-bams': 'health',
  'mecee-bl': 'health',
  // Licence & Entrance — 3
  'nec-licence': 'licence-entrance',
  'ioe-entrance': 'licence-entrance',
  'csit-entrance': 'licence-entrance',
  // Law & Justice — 2
  'judicial-service': 'law',
  'bar-council': 'law',
  // Public Enterprises — 2
  'nea': 'enterprise',
  'nepal-telecom': 'enterprise',
};

/// Category id for an exam: exact id map first, then a keyword pass over
/// the recruiting body, then 'other'. Never throws, never empty.
String categoryIdForExam(Exam exam) {
  final byId = _categoryByExamId[exam.id];
  if (byId != null) return byId;
  final b = exam.body.toLowerCase();
  if (b.contains('judicial') || b.contains('bar council')) return 'law';
  if (b.contains('teacher service')) return 'tsc';
  if (b.contains('police') || b.contains('army')) return 'security';
  if (b.contains('rastra bank') ||
      b.contains('banijya bank') ||
      b.contains('public banks')) {
    return 'banking';
  }
  if (b.contains('health') ||
      b.contains('medical') ||
      b.contains('nursing') ||
      b.contains('pharmacy') ||
      b.contains('ayurveda')) {
    return 'health';
  }
  if (b.contains('engineering council') ||
      b.contains('university') ||
      b.contains('institute')) {
    return 'licence-entrance';
  }
  if (b.contains('electricity') || b.contains('telecom')) {
    return 'enterprise';
  }
  if (b.contains('lok sewa') || b.contains('public service commission')) {
    return 'psc';
  }
  return 'other';
}

/// Groups [exams] into (category, exams) pairs in display order,
/// skipping empty categories. Every exam appears exactly once.
List<(ExamCategory, List<Exam>)> groupExams(List<Exam> exams) {
  final buckets = <String, List<Exam>>{};
  for (final e in exams) {
    buckets.putIfAbsent(categoryIdForExam(e), () => []).add(e);
  }
  return [
    for (final c in examCategories)
      if (buckets.containsKey(c.id)) (c, buckets[c.id]!),
  ];
}

/// Case-insensitive match against the EN name, NE name and id.
/// An empty query matches everything.
bool examMatchesQuery(Exam exam, String query) {
  final q = query.trim().toLowerCase();
  if (q.isEmpty) return true;
  return exam.name.toLowerCase().contains(q) ||
      exam.nameNe.toLowerCase().contains(q) ||
      exam.id.toLowerCase().contains(q);
}
