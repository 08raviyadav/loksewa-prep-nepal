import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

import '../models/history.dart';
import '../models/models.dart';

/// Loads the bundled JSON data files with in-memory caching.
/// All data ships in assets/ — offline-first, zero network calls.
class DataRepository {
  static final DataRepository _instance = DataRepository._();
  factory DataRepository() => _instance;
  DataRepository._();

  List<Exam>? _exams;
  List<Map<String, dynamic>>? _examRows;
  List<ExamDate>? _examDates;
  List<HistoricalEvent>? _history;
  final Map<String, List<Question>> _questionFiles = {};
  Map<String, dynamic>? _qIndex;

  /// Raw decoded exams.json rows (prelim blocks included), parsed once
  /// and cached. Screens that need more than the Exam model (mock
  /// patterns, prelim tables) read this instead of re-parsing the file
  /// — exams.json was parsed in four places before v1.0.1.
  Future<List<Map<String, dynamic>>> examRows() async {
    if (_examRows != null) return _examRows!;
    final raw = await rootBundle.loadString('assets/data/exams.json');
    final decoded = json.decode(raw);
    final list = decoded is List ? decoded : decoded['exams'] as List;
    _examRows = list
        .map((e) => Map<String, dynamic>.from(e as Map))
        .toList();
    return _examRows!;
  }

  Future<List<Exam>> exams() async {
    if (_exams != null) return _exams!;
    final rows = await examRows();
    _exams = rows.map(Exam.fromJson).toList();
    return _exams!;
  }

  Future<List<ExamDate>> examDates() async {
    if (_examDates != null) return _examDates!;
    final raw = await rootBundle.loadString('assets/data/exam-dates.json');
    final decoded = json.decode(raw);
    final list = decoded is List ? decoded : decoded['dates'] as List;
    _examDates = list
        .map((e) => ExamDate.fromJson(Map<String, dynamic>.from(e as Map)))
        .toList();
    return _examDates!;
  }

  /// Historical events (assets/data/historical-events.json) — the
  /// 95 verified Dates to Remember entries.
  Future<List<HistoricalEvent>> historicalEvents() async {
    if (_history != null) return _history!;
    final raw = await rootBundle.loadString(
      'assets/data/historical-events.json',
    );
    final decoded = json.decode(raw) as List;
    _history = decoded
        .map(
          (e) => HistoricalEvent.fromJson(Map<String, dynamic>.from(e as Map)),
        )
        .toList();
    return _history!;
  }

  /// Loads one question file (e.g. 'constitution-governance-economy.json').
  /// Full bank ships as many files; screens load only what they need.
  Future<List<Question>> questions(String fileName) async {
    if (_questionFiles.containsKey(fileName)) return _questionFiles[fileName]!;
    final raw = await rootBundle.loadString('assets/data/questions/$fileName');
    final decoded = json.decode(raw) as List;
    final qs = decoded
        .map((e) => Question.fromJson(Map<String, dynamic>.from(e as Map)))
        .toList();
    _questionFiles[fileName] = qs;
    return qs;
  }

  /// Compact per-exam/per-file index (assets/data/question_index.json),
  /// generated from the 131 question files. Lets screens show topic
  /// counts without parsing 73MB of JSON.
  Future<Map<String, dynamic>> questionIndex() async {
    if (_qIndex != null) return _qIndex!;
    final raw = await rootBundle.loadString('assets/data/question_index.json');
    _qIndex = json.decode(raw) as Map<String, dynamic>;
    return _qIndex!;
  }

  /// Topic -> count for [examId], from the index (no file parsing).
  Future<Map<String, int>> topicCountsFor(String examId) async {
    final idx = await questionIndex();
    final exams = idx['exams'] as Map<String, dynamic>;
    final e = exams[examId] as Map<String, dynamic>?;
    if (e == null) return {};
    final topics = e['topics'] as Map<String, dynamic>;
    return topics.map((k, v) => MapEntry(k, (v as num).toInt()));
  }

  /// Total tagged questions for [examId], from the index.
  Future<int> questionCountFor(String examId) async {
    final idx = await questionIndex();
    final exams = idx['exams'] as Map<String, dynamic>;
    final e = exams[examId] as Map<String, dynamic>?;
    return ((e?['total'] as num?) ?? 0).toInt();
  }

  /// Loads only the files that contain questions for [examId], then
  /// filters by topics/difficulty. Files are cached in memory.
  Future<List<Question>> questionsForExam(
    String examId, {
    Set<String>? topics,
    String difficulty = 'mixed',
  }) async {
    final idx = await questionIndex();
    final files = idx['files'] as List;
    final wanted = <String>[];
    for (final f in files) {
      final m = f as Map<String, dynamic>;
      if ((m['exams'] as List).contains(examId)) {
        wanted.add(m['file'] as String);
      }
    }
    final out = <Question>[];
    for (final name in wanted) {
      final qs = await questions(name);
      for (final q in qs) {
        if (!q.exam.contains(examId)) continue;
        if (topics != null && topics.isNotEmpty && !topics.contains(q.topic)) {
          continue;
        }
        if (difficulty != 'mixed' && q.difficulty != difficulty) continue;
        out.add(q);
      }
    }
    return out;
  }

  /// Loads every question file in the index (cached per file).
  /// Heavy one-time cost — used by Daily Challenge / Quick Quiz, which
  /// draw from the whole bank like the vanilla site.
  Future<List<Question>> allQuestions() async {
    final idx = await questionIndex();
    final files = idx['files'] as List;
    final out = <Question>[];
    for (final f in files) {
      out.addAll(
        await questions((f as Map<String, dynamic>)['file'] as String),
      );
    }
    return out;
  }

  /// All distinct topic tags for [examId] across the loaded question files.
  /// Call after loading the needed files.
  Map<String, int> topicCounts(String examId) {
    final counts = <String, int>{};
    for (final qs in _questionFiles.values) {
      for (final q in qs) {
        if (q.exam.contains(examId)) {
          counts[q.topic] = (counts[q.topic] ?? 0) + 1;
        }
      }
    }
    return counts;
  }

  void clearCache() {
    _exams = null;
    _examDates = null;
    _history = null;
    _questionFiles.clear();
  }
}
