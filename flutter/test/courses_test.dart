/// Courses milestone tests:
///   1. JSON schema validation for all 3 bundled course files (mirrors
///      vanilla scripts/test-courses.js checks: schema, bilingual theory
///      word counts, key points, placeholder text, unique/prefixed ids).
///   2. linked_topics ⊆ verified bank tags (vanilla VERIFIED_TAGS).
///   3. Course progress store round-trip using the EXACT vanilla storage key
///      'loksewa_course_progress_v1' with the vanilla done-object shape.
///   4. Pure helpers: flatten/chapterById/courseProgress/subjectProgress
///      and paragraph splitting.
library;

import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/models/course.dart';
import 'package:loksewa_vidyapeeth/state/course_progress_store.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// The copied vanilla files must be what the tests validate.
const List<String> _courseFiles = [
  'kharidar.json',
  'nayab-subba.json',
  'section-officer.json',
];

List<Course> _loadAll() => _courseFiles
    .map(
      (f) => Course.decode(File('assets/data/courses/$f').readAsStringSync()),
    )
    .toList();

void main() {
  group('course JSON schema (vanilla test-courses.js checks)', () {
    test('all 3 course files exist in the Flutter asset bundle', () {
      for (final f in _courseFiles) {
        expect(File('assets/data/courses/$f').existsSync(), isTrue, reason: f);
      }
    });

    test('courseFiles constant lists exactly the bundled files', () {
      expect(courseFiles, equals(_courseFiles));
    });

    test('full schema validation passes for all 56 chapters', () {
      final courses = _loadAll();
      expect(courses.length, 3);
      final allErrs = <String>[];
      var totalChapters = 0;
      for (var i = 0; i < courses.length; i++) {
        final errs = courses[i].validate(_courseFiles[i]);
        allErrs.addAll(errs);
        totalChapters += courses[i].subjects.fold(
              0,
              (n, s) => n + s.chapters.length,
            );
      }
      expect(allErrs, isEmpty, reason: allErrs.take(10).join('\n'));
      expect(totalChapters, 56);
    });

    test('chapter ids are unique across all courses', () {
      final ids = _loadAll()
          .expand((c) => c.subjects)
          .expand((s) => s.chapters)
          .map((ch) => ch.id);
      final seen = <String>{};
      for (final id in ids) {
        expect(seen.add(id), isTrue, reason: 'duplicate id $id');
      }
    });

    test('chapter id prefixes match the exam (vanilla rule)', () {
      for (final c in _loadAll()) {
        final prefix = c.exam == 'nayab-subba'
            ? 'nasu'
            : (c.exam == 'section-officer' ? 'so' : 'kharidar');
        for (final ch in c.subjects.expand((s) => s.chapters)) {
          expect(
            ch.id.startsWith(prefix),
            isTrue,
            reason: '${ch.id} vs $prefix',
          );
        }
      }
    });
  });

  group('linked_topics are verified bank tags', () {
    test('every linked_topic is in verifiedCourseTags', () {
      final bad = <String>[];
      for (final c in _loadAll()) {
        for (final ch in c.subjects.expand((s) => s.chapters)) {
          for (final t in ch.linkedTopics) {
            if (!verifiedCourseTags.contains(t)) bad.add('${ch.id}: $t');
          }
        }
      }
      expect(bad, isEmpty, reason: bad.take(10).join('\n'));
    });

    test('verifiedCourseTags matches vanilla VERIFIED_TAGS exactly', () {
      const vanillaTags = [
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
      expect(Set.of(verifiedCourseTags), Set.of(vanillaTags));
    });

    test('courseExamMap matches vanilla COURSE_EXAM_MAP', () {
      expect(courseExamMap, {
        'kharidar': 'kharidar',
        'nayab-subba': 'nasu',
        'section-officer': 'section-officer',
      });
    });
  });

  group('pure progress helpers (vanilla ports)', () {
    late Course kharidar;
    setUpAll(() {
      kharidar = Course.decode(
        File('assets/data/courses/kharidar.json').readAsStringSync(),
      );
    });

    test('flatten covers all chapters with owning subjects', () {
      final flat = kharidar.flatten();
      expect(flat.length, 16);
      for (final r in flat) {
        expect(r.subject.chapters, contains(r.chapter));
      }
    });

    test('chapterById finds chapters; unknown id returns null', () {
      expect(kharidar.chapterById('kharidar-solar-system-earth'), isNotNull);
      expect(kharidar.chapterById('nope'), isNull);
    });

    test('calcCourseProgress equivalent math', () {
      final p0 = kharidar.progress(const {});
      expect(p0.total, 16);
      expect(p0.done, 0);
      expect(p0.pct, 0);
      final p2 = kharidar.progress({'kharidar-solar-system-earth'});
      expect(p2.done, 1);
      // Vanilla: Math.round(done/total*100)
      expect(p2.pct, (1 / 16 * 100).round());
    });

    test('subjectProgress equivalent math', () {
      final subj = kharidar.subjects.first;
      final done = subj.chapters.take(2).map((ch) => ch.id).toSet();
      final sp = subj.progress(done);
      expect(sp.total, subj.chapters.length);
      expect(sp.done, 2);
      expect(sp.pct, (2 / subj.chapters.length * 100).round());
    });

    test('paragraphs split on blank lines like vanilla', () {
      final ch = kharidar.chapterById('kharidar-solar-system-earth')!.chapter;
      final paras = ch.paragraphs(false);
      expect(paras.length, greaterThan(1));
      expect(paras.every((p) => p.isNotEmpty), isTrue);
    });

    test('bilingual fallbacks never empty when other lang exists', () {
      for (final c in _loadAll()) {
        for (final ch in c.subjects.expand((s) => s.chapters)) {
          expect(ch.title(false).isNotEmpty, isTrue, reason: ch.id);
          expect(ch.title(true).isNotEmpty, isTrue, reason: ch.id);
        }
      }
    });
  });

  group('course progress store — exact vanilla key', () {
    test('key is byte-identical to vanilla COURSE_PROG_KEY', () {
      expect(courseProgressKey, 'loksewa_course_progress_v1');
    });

    test(
      'round-trip uses the vanilla {done:{id:true},last:{exam,chId,ts}} shape',
      () async {
        SharedPreferences.setMockInitialValues({});
        final store = CourseProgressStore();
        await store.load();
        expect(store.done, isEmpty);
        expect(store.last, isNull);

        await store.toggle('kharidar-solar-system-earth');
        expect(store.isDone('kharidar-solar-system-earth'), isTrue);
        await store.markOpened('kharidar', 'kharidar-solar-system-earth');
        expect(store.last?.exam, 'kharidar');
        expect(store.last?.chapterId, 'kharidar-solar-system-earth');
        expect(store.last!.ts, greaterThan(0));

        // Inspect the RAW stored JSON — must match the vanilla site's shape.
        final prefs = await SharedPreferences.getInstance();
        final raw = prefs.getString('loksewa_course_progress_v1');
        expect(raw, isNotNull);
        final decoded = jsonDecode(raw!) as Map<String, dynamic>;
        expect(decoded['done'], {'kharidar-solar-system-earth': true});
        expect((decoded['last'] as Map)['exam'], 'kharidar');
        expect((decoded['last'] as Map)['chId'], 'kharidar-solar-system-earth');
        expect((decoded['last'] as Map)['ts'], isA<int>());

        // Reload from storage — state survives a restart.
        final store2 = CourseProgressStore();
        await store2.load();
        expect(store2.isDone('kharidar-solar-system-earth'), isTrue);
        expect(store2.last?.chapterId, 'kharidar-solar-system-earth');

        // Toggle off — vanilla setChapterDone(id, false) deletes the key.
        await store2.toggle('kharidar-solar-system-earth');
        expect(store2.isDone('kharidar-solar-system-earth'), isFalse);
        final raw2 = (await SharedPreferences.getInstance()).getString(
          courseProgressKey,
        )!;
        final decoded2 = jsonDecode(raw2) as Map<String, dynamic>;
        expect(
          (decoded2['done'] as Map).containsKey('kharidar-solar-system-earth'),
          isFalse,
        );
      },
    );

    test('corrupt storage degrades gracefully like vanilla', () async {
      SharedPreferences.setMockInitialValues({
        courseProgressKey: 'not-json{{{',
      });
      final store = CourseProgressStore();
      await store.load();
      expect(store.done, isEmpty);
      expect(store.last, isNull);
    });
  });
}
