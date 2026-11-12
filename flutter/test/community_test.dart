import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:loksewa_vidyapeeth/state/community_store.dart';

Map<String, dynamic> validSubmission() => {
      'exam': 'kharidar',
      'topic': 'Constitution & Governance',
      'subtopic': 'Fundamental Rights',
      'difficulty': 'medium',
      'marks': 2,
      'question':
          'Which article of the Constitution of Nepal 2072 guarantees the right to freedom?',
      'question_ne':
          'नेपालको संविधान २०७२ को कुन धाराले स्वतन्त्रताको हकको ग्यारेन्टी गर्छ?',
      'options': ['Article 17', 'Article 18', 'Article 19', 'Article 20'],
      'options_ne': ['धारा १७', 'धारा १८', 'धारा १९', 'धारा २०'],
      'answer': 0,
      'explanation': 'Article 17 guarantees the right to freedom.',
      'explanation_ne': 'धारा १७ ले स्वतन्त्रताको हकको ग्यारेन्टी गर्छ।',
      'source': 'Constitution of Nepal 2072, Part 3',
      'contributor': 'Test User',
    };

Future<CommunityStore> freshStore({String author = 'Test User'}) async {
  SharedPreferences.setMockInitialValues({});
  final store = CommunityStore(authorName: author, voterId: 'voter-1');
  await store.init();
  return store;
}

void main() {
  group('pure text helpers (vanilla semantics)', () {
    test('normaliseText lowercases, strips punctuation, collapses space', () {
      expect(normaliseText('  Hello,  WORLD!  '), 'hello world');
      // Devanagari vowel signs (\p{M}) are stripped, same as vanilla's JS
      // /[^\p{L}\p{N}\s]/gu — normalisation is only for comparison, not display.
      expect(normaliseText('कुन-धाराले?'), 'क न ध र ल');
      expect(normaliseText(null), '');
    });

    test('hasUrl', () {
      expect(hasUrl('see https://example.com'), isTrue);
      expect(hasUrl('visit www.example.com/x'), isTrue);
      expect(hasUrl('no links here'), isFalse);
    });

    test('repeatedChars needs 5+ in a row', () {
      expect(repeatedChars('wow!!!!!'), isTrue);
      expect(repeatedChars('wow!!!!'), isFalse);
    });

    test('capsRatio', () {
      expect(capsRatio(''), 0);
      expect(capsRatio('123'), 0);
      expect(capsRatio('ABC def'), 0.5);
      expect(capsRatio('ALL CAPS HERE'), 1.0);
    });

    test('jaccardNorm', () {
      expect(jaccardNorm('a b c', 'a b c'), 1.0);
      expect(jaccardNorm('a b c', 'a b x'), closeTo(0.5, 1e-9));
      expect(jaccardNorm('', 'a'), 0);
    });
  });

  group('findDuplicate', () {
    final bank = [
      {
        'id': 'Q-1',
        'question': 'Which article guarantees the right to freedom?',
      },
      {'id': 'Q-2', 'question': 'Who was the first king of Nepal?'},
    ];

    test('exact match (normalised)', () {
      final hit = findDuplicate(
        '  WHICH article guarantees the RIGHT to freedom? ',
        '',
        bank,
      );
      expect(hit, isNotNull);
      expect(hit!.type, 'exact');
      expect(hit.score, 1);
      expect(hit.match['id'], 'Q-1');
    });

    test('near match at >= 0.8 jaccard', () {
      // 7 shared / 10 tokens = 0.7: below threshold
      expect(
        findDuplicate(
          'Who was the very first great king of Nepal today',
          '',
          bank,
        ),
        isNull,
      );
      expect(
        findDuplicate(
          'Who was the first great king of Nepal in history',
          '',
          bank,
        ),
        isNull,
      );
      // same tokens, different order -> jaccard 1.0 but not an exact
      // normalised-string match -> near hit
      final hit = findDuplicate('king of Nepal was the first Who', '', bank);
      expect(hit, isNotNull);
      expect(hit!.type, 'near');
      expect(hit.score, 1.0);
      expect(hit.match['id'], 'Q-2');
    });

    test('no match', () {
      expect(findDuplicate('What is the capital of France?', '', bank), isNull);
    });
  });

  group('validateSubmission (vanilla checks)', () {
    test('valid submission passes', () {
      final v = validateSubmission(validSubmission());
      expect(v.ok, isTrue);
      expect(v.errors, isEmpty);
    });

    test('missing required fields', () {
      final d = validSubmission()..['topic'] = '  ';
      final v = validateSubmission(d);
      expect(v.ok, isFalse);
      expect(v.errors.any((e) => e.contains('Topic')), isTrue);
    });

    test('marks must be 1 or 2', () {
      final d = validSubmission()..['marks'] = 3;
      expect(validateSubmission(d).ok, isFalse);
    });

    test('question min length 15', () {
      final d = validSubmission()..['question'] = 'Too short?';
      final v = validateSubmission(d);
      expect(v.ok, isFalse);
      expect(v.errors.any((e) => e.contains('15 characters')), isTrue);
    });

    test('no links in question text', () {
      final d = validSubmission()
        ..['question'] =
            'Which article guarantees freedom? See https://x.example for more';
      expect(validateSubmission(d).ok, isFalse);
    });

    test('repeated chars rejected', () {
      final d = validSubmission()
        ..['question'] = 'Which article guarantees freedom!!!!! really?';
      expect(validateSubmission(d).ok, isFalse);
    });

    test('all caps rejected', () {
      final d = validSubmission()
        ..['question'] = 'WHICH ARTICLE GUARANTEES THE RIGHT TO FREEDOM NOW';
      final v = validateSubmission(d);
      expect(v.ok, isFalse);
      expect(v.errors.any((e) => e.contains('ALL CAPS')), isTrue);
    });

    test('exactly 4 options required', () {
      final d = validSubmission()..['options'] = ['A', 'B'];
      expect(validateSubmission(d).ok, isFalse);
    });

    test('empty option rejected', () {
      final d = validSubmission()
        ..['options'] = ['Article 17', '', 'Article 19', 'Article 20'];
      final v = validateSubmission(d);
      expect(v.ok, isFalse);
      expect(v.errors.any((e) => e.contains('option B')), isTrue);
    });

    test('duplicate options rejected (normalised)', () {
      final d = validSubmission()
        ..['options'] = [
          'Article 17',
          'article 17!',
          'Article 19',
          'Article 20',
        ];
      expect(validateSubmission(d).ok, isFalse);
    });

    test('answer must be 0-3', () {
      final d = validSubmission()..['answer'] = null;
      expect(validateSubmission(d).ok, isFalse);
      final d2 = validSubmission()..['answer'] = 4;
      expect(validateSubmission(d2).ok, isFalse);
    });

    test('Nepali errors when nepali=true', () {
      final d = validSubmission()..['topic'] = '';
      final v = validateSubmission(d, nepali: true);
      expect(v.errors.any((e) => e.contains('विषय')), isTrue);
    });
  });

  group('rateLimitCheck (vanilla: 5/hour)', () {
    test('under the limit is allowed', () {
      const now = 1000000000;
      final ts = List.generate(4, (i) => now - i * 1000);
      final r = rateLimitCheck(ts, nowMs: now);
      expect(r.allowed, isTrue);
      expect(r.count, 4);
    });

    test('5 within the hour is blocked with minutes left', () {
      const now = 1000000000;
      final ts = List.generate(5, (i) => now - i * 60 * 1000);
      final r = rateLimitCheck(ts, nowMs: now);
      expect(r.allowed, isFalse);
      expect(r.minutesLeft, greaterThan(0));
      expect(r.count, 5);
    });

    test('old timestamps fall out of the window', () {
      const now = 1000000000;
      final ts = List.generate(5, (_) => now - 2 * 3600 * 1000);
      final r = rateLimitCheck(ts, nowMs: now);
      expect(r.allowed, isTrue);
      expect(r.count, 0);
    });
  });

  group('validateSuggestion (vanilla checks)', () {
    final cats = suggestionCategories.map((c) => c[0]).toList();

    test('valid suggestion passes', () {
      final v = validateSuggestion(
        {
          'title': 'Spaced repetition reminders',
          'description': 'Resurface weak topics on a 1-3-7 day schedule.',
          'category': 'feature',
        },
        cats,
      );
      expect(v.ok, isTrue);
    });

    test('title min 8, description min 20', () {
      final v = validateSuggestion(
        {
          'title': 'Short',
          'description': 'too short',
          'category': 'bug',
        },
        cats,
      );
      expect(v.ok, isFalse);
      expect(v.errors.length, 2);
    });

    test('bad category rejected', () {
      final v = validateSuggestion(
        {
          'title': 'A fine title here',
          'description': 'A long enough description for testing.',
          'category': 'nope',
        },
        cats,
      );
      expect(v.errors.any((e) => e.contains('category')), isTrue);
    });

    test('links and repeated chars rejected', () {
      final v = validateSuggestion(
        {
          'title': 'See https://x.example now',
          'description': 'A long enough description for testing!!!!!!',
          'category': 'other',
        },
        cats,
      );
      expect(v.errors.length, 2);
    });

    test('isDuplicateSuggestion normalises titles', () {
      final list = [
        {'title': 'Spaced-repetition reminders!'},
      ];
      expect(
        isDuplicateSuggestion(list, 'spaced repetition reminders'),
        isTrue,
      );
      expect(isDuplicateSuggestion(list, 'Something else'), isFalse);
    });
  });

  group('CommunityStore discussions', () {
    test('seeds 9 vanilla threads on first run', () async {
      final store = await freshStore();
      expect(store.threads.length, 9);
      expect(store.threads.first['id'], 'DIS-001');
    });

    test('addThread validates (title>=8, body>=10) and prepends', () async {
      final store = await freshStore();
      expect(
        await store.addThread(exam: 'general', title: 'Short', body: 'x'),
        isNotEmpty,
      );
      final errs = await store.addThread(
        exam: 'kharidar',
        title: 'A proper title here',
        body: 'A body long enough.',
      );
      expect(errs, isEmpty);
      expect(store.threads.first['title'], 'A proper title here');
      expect(store.threads.first['author'], 'Test User');
    });

    test('addReply needs >= 2 chars', () async {
      final store = await freshStore();
      expect(await store.addReply('DIS-001', 'x', false), isNotNull);
      expect(
        await store.addReply('DIS-001', 'Good tip, thanks!', false),
        isNull,
      );
      final th = store.threadById('DIS-001')!;
      expect((th['replies'] as List).length, 2);
    });

    test('upvoteThread increments (vanilla semantics)', () async {
      final store = await freshStore();
      await store.upvoteThread('DIS-002');
      await store.upvoteThread('DIS-002');
      expect(store.threadById('DIS-002')!['upvotes'], 2);
    });

    test('reportPost records the report', () async {
      final store = await freshStore();
      await store.reportPost('DIS-003', 'spam', replyIndex: 0);
      final th = store.threadById('DIS-003')!;
      expect((th['reports'] as List).length, 1);
      expect((th['reports'] as List).first['reason'], 'spam');
    });

    test('threadsSorted top orders by upvotes', () async {
      final store = await freshStore();
      await store.upvoteThread('DIS-009');
      final top = store.threadsSorted('top');
      expect(top.first['id'], 'DIS-009');
      expect(store.threadsSorted('new').first['id'], 'DIS-001');
    });

    test('data persists across store instances (same key)', () async {
      final store = await freshStore();
      await store.addThread(
        exam: 'general',
        title: 'Persisted thread title',
        body: 'Long enough body.',
      );
      final prefs = await SharedPreferences.getInstance();
      expect(prefs.containsKey(kDiscussionsKey), isTrue);
      final store2 = CommunityStore();
      await store2.init();
      expect(store2.threads.first['title'], 'Persisted thread title');
    });
  });

  group('CommunityStore submit-a-question', () {
    test('valid submit lands in the review queue as pending', () async {
      final store = await freshStore();
      final out = await store.submitQuestion(validSubmission());
      expect(out.ok, isTrue);
      final c = store.submissionCounts();
      expect(c['pending'], 1);
      expect(c['approved'], 0);
      // Never live instantly: not in the approved list.
      expect(store.approvedQuestions, isEmpty);
    });

    test('invalid submit returns validation errors', () async {
      final store = await freshStore();
      final d = validSubmission()..['answer'] = null;
      final out = await store.submitQuestion(d);
      expect(out.ok, isFalse);
      expect(out.errors, isNotEmpty);
      expect(store.submissionCounts()['pending'], 0);
    });

    test('duplicate of a pending item is blocked', () async {
      final store = await freshStore();
      expect((await store.submitQuestion(validSubmission())).ok, isTrue);
      final out = await store.submitQuestion(validSubmission());
      expect(out.ok, isFalse);
      expect(out.blockedMessage, isNotNull);
    });

    test('three identical rejected items hit the spam guard', () async {
      final store = await freshStore();
      const q = 'Identical spam question, long enough text?';
      // Submit + reject the identical question 3 times (3 queue entries).
      for (var i = 0; i < 3; i++) {
        final d = validSubmission()..['question'] = q;
        final out = await store.submitQuestion(d);
        expect(out.ok, isTrue, reason: 'identical submit $i');
        final pending = store.pendingSubmissions;
        expect(pending.length, 1);
        await store.rejectSubmission(pending.first['id'] as String, 'dup');
      }
      // The 4th identical attempt trips the vanilla "already submitted 3
      // times" spam guard.
      final out = await store.submitQuestion(
        validSubmission()..['question'] = q,
      );
      expect(out.ok, isFalse);
      expect(out.blockedMessage, contains('3 times'));
    });

    test('double-submit of a pending item is blocked', () async {
      final store = await freshStore();
      expect((await store.submitQuestion(validSubmission())).ok, isTrue);
      // A second, near-identical-but-different-enough submission while the
      // first is pending must not queue twice.
      final d = validSubmission()
        ..['question'] =
            'Which article of the Constitution of Nepal 2072 guarantees the right to freedom??';
      final out = await store.submitQuestion(d);
      expect(out.ok, isFalse);
      expect(out.blockedMessage, contains('already in the review queue'));
    });

    test('rate limit: 6th submission within the hour blocked', () async {
      final store = await freshStore();
      for (var i = 0; i < 5; i++) {
        final d = validSubmission()
          ..['question'] = 'Rate limit test question number $i, long enough?';
        expect((await store.submitQuestion(d)).ok, isTrue);
      }
      final d = validSubmission()
        ..['question'] = 'Rate limit test question number 5, long enough?';
      final out = await store.submitQuestion(d);
      expect(out.ok, isFalse);
      expect(out.blockedMessage, contains('Rate limit'));
    });

    test('approve moves to approved list with COMM id', () async {
      final store = await freshStore();
      await store.submitQuestion(validSubmission());
      final id = store.pendingSubmissions.first['id'] as String;
      final q = await store.approveSubmission(id);
      expect(q, isNotNull);
      expect(q!['id'], 'COMM-001');
      expect(store.submissionCounts()['approved'], 1);
      expect(store.approvedQuestions.length, 1);
      expect(store.pendingSubmissions, isEmpty);
    });

    test('reject needs a reason and marks rejected', () async {
      final store = await freshStore();
      await store.submitQuestion(validSubmission());
      final id = store.pendingSubmissions.first['id'] as String;
      expect(await store.rejectSubmission(id, '  '), isFalse);
      expect(await store.rejectSubmission(id, 'Wrong answer'), isTrue);
      expect(store.submissionCounts()['rejected'], 1);
      expect(store.pendingSubmissions, isEmpty);
    });
  });

  group('CommunityStore suggestions', () {
    test('seeds 3 vanilla suggestions on first run', () async {
      final store = await freshStore();
      expect(store.suggestions.length, 3);
      expect(store.suggestions.first['_seed'], isTrue);
    });

    test('addSuggestion validates and prepends', () async {
      final store = await freshStore();
      expect(
        await store.addSuggestion(
          title: 'Short',
          description: 'x',
          category: 'feature',
        ),
        isNotEmpty,
      );
      final errs = await store.addSuggestion(
        title: 'Offline-first question packs',
        description: 'Let users download per-exam packs for offline practice.',
        category: 'feature',
      );
      expect(errs, isEmpty);
      expect(store.suggestions.length, 4);
    });

    test('duplicate title is blocked, upvote instead', () async {
      final store = await freshStore();
      final errs = await store.addSuggestion(
        title: 'spaced repetition reminders',
        description: 'A long enough description of the same idea.',
        category: 'feature',
      );
      expect(errs, isNotEmpty);
      expect(errs.first, contains('already on the list'));
    });

    test('upvote toggles via voters list', () async {
      final store = await freshStore();
      final id = store.suggestions.first['id'] as String;
      await store.upvoteSuggestion(id);
      expect(store.suggestions.first['upvotes'], 1);
      expect(store.hasVoted(store.suggestions.first), isTrue);
      await store.upvoteSuggestion(id);
      expect(store.suggestions.first['upvotes'], 0);
      expect(store.hasVoted(store.suggestions.first), isFalse);
    });

    test('suggestions sort by upvotes desc', () async {
      final store = await freshStore();
      await store.upvoteSuggestion('SUG-SEED-3');
      final first = store.suggestions.first;
      expect(first['id'], 'SUG-SEED-3');
      expect(first['upvotes'], 1);
    });

    test('rate limit: 6th suggestion within the hour blocked', () async {
      final store = await freshStore();
      for (var i = 0; i < 5; i++) {
        final errs = await store.addSuggestion(
          title: 'Suggestion number $i with length',
          description: 'A sufficiently long description for number $i.',
          category: 'feature',
        );
        expect(errs, isEmpty, reason: 'suggestion $i: $errs');
      }
      final errs = await store.addSuggestion(
        title: 'One more suggestion here',
        description: 'A sufficiently long description for the sixth.',
        category: 'feature',
      );
      expect(errs, isNotEmpty);
      expect(errs.first, contains('Rate limit'));
    });
  });
}
