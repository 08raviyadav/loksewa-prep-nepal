import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/models/models.dart';

/// Validates the real bundled JSON files against the Dart models —
/// catches schema drift between the vanilla bank and the Flutter app.
void main() {
  group('bundled data files', () {
    test('exams.json parses to 47 exams', () {
      final raw = File('assets/data/exams.json').readAsStringSync();
      final decoded = json.decode(raw) as List;
      final exams = decoded
          .map((e) => Exam.fromJson(Map<String, dynamic>.from(e as Map)))
          .toList();
      expect(exams.length, 47);
      expect(exams.any((e) => e.id == 'kharidar'), isTrue);
      expect(exams.firstWhere((e) => e.id == 'kharidar').nameNe, 'खरिदार');
    });

    test('exam-dates.json parses with valid BS dates', () {
      final raw = File('assets/data/exam-dates.json').readAsStringSync();
      final decoded = json.decode(raw) as List;
      final dates = decoded
          .map((e) => ExamDate.fromJson(Map<String, dynamic>.from(e as Map)))
          .toList();
      expect(dates.length, 82);
      final bsRe = RegExp(r'^\d{4}-\d{2}-\d{2}$');
      for (final d in dates) {
        expect(bsRe.hasMatch(d.dateBs), isTrue, reason: d.id);
        expect(['exam', 'admit', 'deadline'], contains(d.kind));
        expect(['high', 'medium'], contains(d.confidence));
      }
    });

    test('sample question file parses with valid answer indices', () {
      final raw = File(
        'assets/data/questions/constitution-governance-economy.json',
      ).readAsStringSync();
      final decoded = json.decode(raw) as List;
      final qs = decoded
          .map((e) => Question.fromJson(Map<String, dynamic>.from(e as Map)))
          .toList();
      expect(qs.length, 215);
      for (final q in qs.take(50)) {
        expect(
          q.answer,
          inInclusiveRange(0, q.options.length - 1),
          reason: q.id,
        );
        expect(q.optionsNe.length, q.options.length, reason: q.id);
      }
    });
  });

  group('Question helpers', () {
    test('text/opts fall back to English when Nepali is empty', () {
      const q = Question(
        id: 'x',
        exam: ['kharidar'],
        topic: 't',
        subtopic: 's',
        difficulty: 'easy',
        marks: 2,
        question: 'EN?',
        questionNe: '',
        options: ['a', 'b'],
        optionsNe: [],
        answer: 0,
        explanation: 'EN exp',
        explanationNe: '',
        source: 'src',
      );
      expect(q.text(true), 'EN?');
      expect(q.opts(true), ['a', 'b']);
      expect(q.explain(true), 'EN exp');
    });
  });
}
