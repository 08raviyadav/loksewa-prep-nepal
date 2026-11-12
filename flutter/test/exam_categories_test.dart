/// Category mapping for the Practice picker / Mock list (v1.0.1).
///
/// The picker groups 47 exams into 8 collapsible sections. These tests
/// pin the split against the real bundled exams.json so a data change
/// that drops an exam into "Other" (or out of the list entirely) fails
/// loudly instead of silently hiding an exam from the user.
library;

import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/engine/exam_categories.dart';
import 'package:loksewa_vidyapeeth/models/models.dart';

Future<List<Exam>> _shippedExams() async {
  final raw = await rootBundle.loadString('assets/data/exams.json');
  final decoded = json.decode(raw);
  final list = decoded is List ? decoded : decoded['exams'] as List;
  return list
      .map((e) => Exam.fromJson(Map<String, dynamic>.from(e as Map)))
      .toList();
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('categoryIdForExam — the 47 shipped exams', () {
    test('every shipped exam lands in a real category, none in Other',
        () async {
      final exams = await _shippedExams();
      expect(exams, hasLength(47));
      for (final e in exams) {
        expect(categoryIdForExam(e), isNot('other'), reason: e.id);
      }
    });

    test('category sizes match the curated split', () async {
      final exams = await _shippedExams();
      final groups = groupExams(exams);
      final sizes = {for (final (c, l) in groups) c.id: l.length};
      expect(sizes, {
        'psc': 14,
        'tsc': 4,
        'banking': 4,
        'security': 2,
        'health': 16,
        'licence-entrance': 3,
        'law': 2,
        'enterprise': 2,
      });
    });
  });

  group('categoryIdForExam — fallback for future exams', () {
    test('recruiting-body keywords route unknown ids', () {
      Exam e(String body) =>
          Exam(id: 'future-exam', name: 'Future', nameNe: '', body: body);
      expect(categoryIdForExam(e('Teacher Service Commission')), 'tsc');
      expect(categoryIdForExam(e('Nepal Rastra Bank')), 'banking');
      expect(categoryIdForExam(e('Nepal Police HQ')), 'security');
      expect(categoryIdForExam(e('Nepal Medical Council')), 'health');
      expect(categoryIdForExam(e('Nepal Bar Council')), 'law');
      expect(categoryIdForExam(e('Nepal Electricity Authority')), 'enterprise');
      expect(categoryIdForExam(e('Tribhuvan University')), 'licence-entrance');
      expect(categoryIdForExam(e('Lok Sewa Aayog (PSC)')), 'psc');
      expect(categoryIdForExam(e('Some Brand-New Board')), 'other');
      expect(categoryIdForExam(e('')), 'other');
    });

    test('exact id mapping beats the body fallback', () {
      // Judicial Service's body mentions Lok Sewa, but the exam belongs
      // in Law & Justice.
      const e = Exam(
        id: 'judicial-service',
        name: 'Judicial Service (Nyaya Sewa)',
        nameNe: '',
        body: 'Lok Sewa Aayog (PSC) — recommends; Judicial Service Commission',
      );
      expect(categoryIdForExam(e), 'law');
    });
  });

  group('groupExams', () {
    test('every exam appears exactly once, groups in display order', () {
      final exams = [
        const Exam(id: 'kharidar', name: 'Kharidar', nameNe: ''),
        const Exam(id: 'tsc-primary', name: 'TSC', nameNe: ''),
        const Exam(id: 'nasu', name: 'NaSu', nameNe: ''),
      ];
      final groups = groupExams(exams);
      expect(groups.map((g) => g.$1.id), ['psc', 'tsc']);
      expect(groups[0].$2.map((e) => e.id), ['kharidar', 'nasu']);
      expect(groups[1].$2.map((e) => e.id), ['tsc-primary']);
    });

    test('empty categories are skipped', () {
      final groups = groupExams([
        const Exam(id: 'kharidar', name: 'Kharidar', nameNe: ''),
      ]);
      expect(groups, hasLength(1));
      expect(groups.single.$1.id, 'psc');
    });
  });

  group('examMatchesQuery', () {
    const e = Exam(
      id: 'tsc-primary',
      name: 'TSC — Primary Teacher',
      nameNe: 'शिक्षक सेवा — प्राथमिक शिक्षक',
    );

    test('empty query matches everything', () {
      expect(examMatchesQuery(e, ''), isTrue);
      expect(examMatchesQuery(e, '   '), isTrue);
    });

    test('matches EN name, NE name and id, case-insensitive', () {
      expect(examMatchesQuery(e, 'tsc'), isTrue);
      expect(examMatchesQuery(e, 'PRIMARY'), isTrue);
      expect(examMatchesQuery(e, 'प्राथमिक'), isTrue);
      expect(examMatchesQuery(e, 'tsc-primary'), isTrue);
      expect(examMatchesQuery(e, 'kharidar'), isFalse);
      expect(examMatchesQuery(e, 'zzz'), isFalse);
    });
  });
}
