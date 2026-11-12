/// Theory-course models — mirror the vanilla site's course JSON schema exactly
/// (loksewa-prep-nepal/data/courses/*.json). Vanilla pure helpers ported:
/// courseByExam, flattenCourseChapters, courseChapterById,
/// calcCourseProgress, subjectProgress (app.js "Theory courses" section).
library;

import 'dart:convert';

import 'package:flutter/services.dart';

/// Course exam id (data/courses) -> practice-exam select value (exams.json).
/// Same mapping as vanilla COURSE_EXAM_MAP (app.js: theory courses section).
const Map<String, String> courseExamMap = {
  'kharidar': 'kharidar',
  'nayab-subba': 'nasu',
  'section-officer': 'section-officer',
};

/// The bank-verified topic tags that chapter `linked_topics` may reference.
/// Must stay in sync with vanilla test-courses.js VERIFIED_TAGS.
const List<String> verifiedCourseTags = [
  'Health/Technical basics',
  'Education & Pedagogy',
  'Maths & Numerical',
  'IQ & Reasoning',
  'Constitution & Governance',
  'Computer & ICT',
  'Office Management & Public Service',
  'Banking & Finance',
  'Nepal History',
  'Nepal Geography',
  'Culture & Society',
  'Science & Tech',
  'Economy & Development',
  'Current Affairs',
  'English',
  'Nepali Language',
];

class KeyPoint {
  final String en;
  final String ne;

  const KeyPoint({required this.en, required this.ne});

  factory KeyPoint.fromJson(Map<String, dynamic> j) =>
      KeyPoint(en: j['en'] as String? ?? '', ne: j['ne'] as String? ?? '');

  String text(bool isNe) =>
      isNe ? (ne.isNotEmpty ? ne : en) : (en.isNotEmpty ? en : ne);
}

class Chapter {
  final String id;
  final String titleEn;
  final String titleNe;
  final String theoryEn;
  final String theoryNe;
  final List<KeyPoint> keyPoints;
  final List<String> linkedTopics;

  const Chapter({
    required this.id,
    required this.titleEn,
    required this.titleNe,
    required this.theoryEn,
    required this.theoryNe,
    required this.keyPoints,
    required this.linkedTopics,
  });

  factory Chapter.fromJson(Map<String, dynamic> j) => Chapter(
        id: j['id'] as String? ?? '',
        titleEn: j['title_en'] as String? ?? '',
        titleNe: j['title_ne'] as String? ?? '',
        theoryEn: j['theory_en'] as String? ?? '',
        theoryNe: j['theory_ne'] as String? ?? '',
        keyPoints: (j['key_points'] as List<dynamic>? ?? const [])
            .map((k) => KeyPoint.fromJson(k as Map<String, dynamic>))
            .toList(),
        linkedTopics: (j['linked_topics'] as List<dynamic>? ?? const [])
            .map((t) => t.toString())
            .toList(),
      );

  String title(bool isNe) => isNe
      ? (titleNe.isNotEmpty ? titleNe : titleEn)
      : (titleEn.isNotEmpty ? titleEn : titleNe);

  String theory(bool isNe) => isNe
      ? (theoryNe.isNotEmpty ? theoryNe : theoryEn)
      : (theoryEn.isNotEmpty ? theoryEn : theoryNe);

  /// Theory split into paragraphs, mirroring vanilla's `\n\s*\n` split in
  /// renderCourseChapter (app.js).
  List<String> paragraphs(bool isNe) => theory(isNe)
      .split(RegExp(r'\n\s*\n'))
      .map((p) => p.trim())
      .where((p) => p.isNotEmpty)
      .toList();

  /// Vanilla-style schema validation for one chapter. Returns a list of
  /// human-readable failures (empty = valid).
  List<String> validate(String expectedIdPrefix) {
    final errs = <String>[];
    if (id.isEmpty) errs.add('empty chapter id');
    if (!id.startsWith(expectedIdPrefix)) {
      errs.add('id "$id" does not start with "$expectedIdPrefix"');
    }
    if (titleEn.trim().isEmpty || titleNe.trim().isEmpty) {
      errs.add('$id: titles not bilingual');
    }
    final we = _words(theoryEn), wn = _words(theoryNe);
    if (we < 150 || we > 400) {
      errs.add('$id: theory_en $we words (need 150-400)');
    }
    if (wn < 150 || wn > 400) {
      errs.add('$id: theory_ne $wn words (need 150-400)');
    }
    if (RegExp(
      r'lorem|TODO|FIXME|xxx',
      caseSensitive: false,
    ).hasMatch('$theoryEn$theoryNe')) {
      errs.add('$id: placeholder text in theory');
    }
    if (keyPoints.length < 5 || keyPoints.length > 10) {
      errs.add('$id: ${keyPoints.length} key points (need 5-10)');
    }
    if (keyPoints.any((k) => k.en.trim().isEmpty || k.ne.trim().isEmpty)) {
      errs.add('$id: key points not bilingual');
    }
    if (linkedTopics.isEmpty) errs.add('$id: linked_topics empty');
    final badTags =
        linkedTopics.where((t) => !verifiedCourseTags.contains(t)).toList();
    if (badTags.isNotEmpty) {
      errs.add('$id: unverified tags: ${badTags.join(', ')}');
    }
    return errs;
  }

  static int _words(String s) =>
      s.split(RegExp(r'\s+')).where((w) => w.isNotEmpty).length;
}

class Subject {
  final String nameEn;
  final String nameNe;
  final double? weightMarks; // nullable, as in vanilla JSON
  final List<Chapter> chapters;

  const Subject({
    required this.nameEn,
    required this.nameNe,
    required this.weightMarks,
    required this.chapters,
  });

  factory Subject.fromJson(Map<String, dynamic> j) => Subject(
        nameEn: j['name_en'] as String? ?? '',
        nameNe: j['name_ne'] as String? ?? '',
        weightMarks: (j['weight_marks'] as num?)?.toDouble(),
        chapters: (j['chapters'] as List<dynamic>? ?? const [])
            .map((c) => Chapter.fromJson(c as Map<String, dynamic>))
            .toList(),
      );

  String name(bool isNe) => isNe
      ? (nameNe.isNotEmpty ? nameNe : nameEn)
      : (nameEn.isNotEmpty ? nameEn : nameNe);

  /// Vanilla subjectProgress (app.js).
  SubjectProgress progress(Set<String> done) {
    final total = chapters.length;
    final d = chapters.where((ch) => done.contains(ch.id)).length;
    return SubjectProgress(
      total: total,
      done: d,
      pct: total == 0 ? 0 : (d / total * 100).round(),
    );
  }
}

class Course {
  final String exam;
  final String examNameEn;
  final String examNameNe;
  final String paper;
  final String confidence; // 'high' | 'medium'
  final List<Subject> subjects;

  const Course({
    required this.exam,
    required this.examNameEn,
    required this.examNameNe,
    required this.paper,
    required this.confidence,
    required this.subjects,
  });

  factory Course.fromJson(Map<String, dynamic> j) => Course(
        exam: j['exam'] as String? ?? '',
        examNameEn: j['exam_name_en'] as String? ?? '',
        examNameNe: j['exam_name_ne'] as String? ?? '',
        paper: j['paper'] as String? ?? '',
        confidence: j['confidence'] as String? ?? '',
        subjects: (j['subjects'] as List<dynamic>? ?? const [])
            .map((s) => Subject.fromJson(s as Map<String, dynamic>))
            .toList(),
      );

  String title(bool isNe) =>
      isNe ? (examNameNe.isNotEmpty ? examNameNe : examNameEn) : examNameEn;

  /// All chapters with their owning subject — vanilla flattenCourseChapters.
  List<ChapterRef> flatten() {
    final out = <ChapterRef>[];
    for (var si = 0; si < subjects.length; si++) {
      for (final ch in subjects[si].chapters) {
        out.add(ChapterRef(subject: subjects[si], subjectIdx: si, chapter: ch));
      }
    }
    return out;
  }

  /// Vanilla courseChapterById.
  ChapterRef? chapterById(String id) {
    for (final ref in flatten()) {
      if (ref.chapter.id == id) return ref;
    }
    return null;
  }

  /// Vanilla calcCourseProgress.
  CourseProgress progress(Set<String> done) {
    final flat = flatten();
    final d = flat.where((r) => done.contains(r.chapter.id)).length;
    return CourseProgress(
      total: flat.length,
      done: d,
      pct: flat.isEmpty ? 0 : (d / flat.length * 100).round(),
    );
  }

  /// Vanilla-style schema validation. Returns failures (empty = valid).
  List<String> validate(String fileName) {
    final errs = <String>[];
    final tag = '$fileName:';
    if (exam != fileName.replaceAll('.json', '')) {
      errs.add('$tag exam "$exam" does not match filename');
    }
    if (subjects.isEmpty) errs.add('$tag no subjects');
    if (confidence != 'high' && confidence != 'medium') {
      errs.add('$tag confidence "$confidence" not high|medium');
    }
    final prefix = exam == 'nayab-subba'
        ? 'nasu'
        : (exam == 'section-officer' ? 'so' : 'kharidar');
    final seen = <String>{};
    for (final s in subjects) {
      if ((s.nameEn.isEmpty && s.nameNe.isEmpty) || s.chapters.isEmpty) {
        errs.add('$tag subject missing names or chapters: ${s.nameEn}');
      }
      for (final ch in s.chapters) {
        if (!seen.add(ch.id)) errs.add('$tag duplicate chapter id ${ch.id}');
        errs.addAll(ch.validate(prefix).map((e) => '$tag$e'));
      }
    }
    return errs;
  }

  static Course decode(String jsonStr) =>
      Course.fromJson(jsonDecode(jsonStr) as Map<String, dynamic>);
}

class ChapterRef {
  final Subject subject;
  final int subjectIdx;
  final Chapter chapter;

  const ChapterRef({
    required this.subject,
    required this.subjectIdx,
    required this.chapter,
  });
}

class CourseProgress {
  final int total;
  final int done;
  final int pct;

  const CourseProgress({
    required this.total,
    required this.done,
    required this.pct,
  });
}

class SubjectProgress {
  final int total;
  final int done;
  final int pct;

  const SubjectProgress({
    required this.total,
    required this.done,
    required this.pct,
  });
}

const List<String> courseFiles = [
  'kharidar.json',
  'nayab-subba.json',
  'section-officer.json',
];

/// Load all course files from the bundled assets.
Future<List<Course>> loadCourses() async {
  final out = <Course>[];
  for (final f in courseFiles) {
    try {
      final raw = await rootBundle.loadString('assets/data/courses/$f');
      out.add(Course.decode(raw));
    } catch (_) {
      // Same as vanilla: a missing/unparseable file is skipped with a warning.
      assert(() {
        // ignore: avoid_print
        print('Could not load course $f');
        return true;
      }());
    }
  }
  return out;
}
