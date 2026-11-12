/// Question model — mirrors the vanilla bank's question JSON shape exactly
/// (see loksewa-prep-nepal/data/questions/*.json). `answer` is the index
/// of the correct option. `exam` lists exam ids this question is tagged for.
class Question {
  final String id;
  final List<String> exam;
  final String topic;
  final String subtopic;
  final String difficulty; // easy | medium | hard
  final int marks;
  final String question;
  final String questionNe;
  final List<String> options;
  final List<String> optionsNe;
  final int answer;
  final String explanation;
  final String explanationNe;
  final String source;

  const Question({
    required this.id,
    required this.exam,
    required this.topic,
    required this.subtopic,
    required this.difficulty,
    required this.marks,
    required this.question,
    required this.questionNe,
    required this.options,
    required this.optionsNe,
    required this.answer,
    required this.explanation,
    required this.explanationNe,
    required this.source,
  });

  factory Question.fromJson(Map<String, dynamic> j) => Question(
        id: j['id'] as String? ?? '',
        exam: (j['exam'] as List<dynamic>? ?? const [])
            .map((e) => e.toString())
            .toList(),
        topic: j['topic'] as String? ?? '',
        subtopic: j['subtopic'] as String? ?? '',
        difficulty: j['difficulty'] as String? ?? 'medium',
        marks: (j['marks'] as num?)?.toInt() ?? 1,
        question: j['question'] as String? ?? '',
        questionNe: j['question_ne'] as String? ?? '',
        options: (j['options'] as List<dynamic>? ?? const [])
            .map((e) => e.toString())
            .toList(),
        optionsNe: (j['options_ne'] as List<dynamic>? ?? const [])
            .map((e) => e.toString())
            .toList(),
        answer: (j['answer'] as num?)?.toInt() ?? 0,
        explanation: j['explanation'] as String? ?? '',
        explanationNe: j['explanation_ne'] as String? ?? '',
        source: j['source'] as String? ?? '',
      );

  String text(bool ne) => ne && questionNe.isNotEmpty ? questionNe : question;
  List<String> opts(bool ne) =>
      ne && optionsNe.length == options.length ? optionsNe : options;
  String explain(bool ne) =>
      ne && explanationNe.isNotEmpty ? explanationNe : explanation;
}

/// Exam model — mirrors data/exams.json (only the fields the app needs).
class Exam {
  final String id;
  final String name;
  final String nameNe;

  /// Recruiting body from exams.json (e.g. "Lok Sewa Aayog (PSC)").
  /// Drives the Practice picker's category grouping; '' when unknown.
  final String body;

  const Exam({
    required this.id,
    required this.name,
    required this.nameNe,
    this.body = '',
  });

  factory Exam.fromJson(Map<String, dynamic> j) => Exam(
        id: j['id'] as String? ?? '',
        name: j['name'] as String? ?? '',
        nameNe: j['name_ne'] as String? ?? '',
        body: j['body'] as String? ?? '',
      );

  String title(bool ne) => ne && nameNe.isNotEmpty ? nameNe : name;
}

/// Exam date — mirrors data/exam-dates.json. Dates are BS YYYY-MM-DD strings.
class ExamDate {
  final String id;
  final String exam; // exam id, matches Exam.id where possible
  final String kind; // exam | admit | deadline
  final String dateBs;
  final String titleEn;
  final String titleNe;
  final String source;
  final String confidence; // high | medium

  const ExamDate({
    required this.id,
    required this.exam,
    required this.kind,
    required this.dateBs,
    required this.titleEn,
    required this.titleNe,
    required this.source,
    required this.confidence,
  });

  factory ExamDate.fromJson(Map<String, dynamic> j) => ExamDate(
        id: j['id'] as String? ?? '',
        exam: j['exam'] as String? ?? '',
        kind: j['kind'] as String? ?? 'exam',
        dateBs: j['date_bs'] as String? ?? '',
        titleEn: j['title_en'] as String? ?? '',
        titleNe: j['title_ne'] as String? ?? '',
        source: j['source'] as String? ?? '',
        confidence: j['confidence'] as String? ?? 'medium',
      );

  String title(bool ne) => ne && titleNe.isNotEmpty ? titleNe : titleEn;
}

/// Course chapter — mirrors data/courses/*.json (framework-agnostic theory
/// content shared with the vanilla site).
class CourseChapter {
  final String id;
  final String titleEn;
  final String titleNe;
  final String theoryEn;
  final String theoryNe;
  final List<String> keyPointsEn;
  final List<String> keyPointsNe;
  final List<String> linkedTopics;

  const CourseChapter({
    required this.id,
    required this.titleEn,
    required this.titleNe,
    required this.theoryEn,
    required this.theoryNe,
    required this.keyPointsEn,
    required this.keyPointsNe,
    required this.linkedTopics,
  });

  factory CourseChapter.fromJson(Map<String, dynamic> j) => CourseChapter(
        id: j['id'] as String? ?? '',
        titleEn: j['title_en'] as String? ?? '',
        titleNe: j['title_ne'] as String? ?? '',
        theoryEn: j['theory_en'] as String? ?? '',
        theoryNe: j['theory_ne'] as String? ?? '',
        keyPointsEn: (j['key_points_en'] as List<dynamic>? ?? const [])
            .map((e) => e.toString())
            .toList(),
        keyPointsNe: (j['key_points_ne'] as List<dynamic>? ?? const [])
            .map((e) => e.toString())
            .toList(),
        linkedTopics: (j['linked_topics'] as List<dynamic>? ?? const [])
            .map((e) => e.toString())
            .toList(),
      );

  String title(bool ne) => ne && titleNe.isNotEmpty ? titleNe : titleEn;
  String theory(bool ne) => ne && theoryNe.isNotEmpty ? theoryNe : theoryEn;
  List<String> keyPoints(bool ne) =>
      ne && keyPointsNe.isNotEmpty ? keyPointsNe : keyPointsEn;
}
