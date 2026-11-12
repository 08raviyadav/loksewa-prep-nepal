/// Community (local/on-device): Discussion Hub, Submit-a-Question review
/// queue, and Suggestions — Milestone 6.
///
/// Vanilla reference: loksewa-prep-nepal/assets/js/app.js
/// (`LS_DISCUSS`, `LS_SUBMISSIONS`, `LS_APPROVED`, `LS_REPORTS`,
/// `LS_MODLOG`, `LS_SUGGEST`, `validateSubmission`, `rateLimitCheck`,
/// `validateSuggestion`, `isDuplicateSuggestion`, `findDuplicate`).
///
/// Everything is on-device via shared_preferences using the VANILLA-IDENTICAL
/// keys, so community data carries over between the vanilla site and this app
/// on web. The honest design rule is preserved: first-time submissions NEVER
/// go live instantly — they sit in the review queue until a maintainer
/// approves them (the in-app "Review queue" tab is the local-preview stand-in
/// for that, exactly like vanilla's moderation preview view). The Supabase
/// backend comes later.
library;

import 'dart:convert';
import 'dart:math';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Vanilla localStorage keys — must stay identical so data carries over.
const String kDiscussionsKey = 'loksewa_discussions_v1';
const String kSubmissionsKey = 'loksewa_submissions_v1';
const String kApprovedKey = 'loksewa_community_approved_v1';
const String kReportsKey = 'loksewa_reports_v1';
const String kModLogKey = 'loksewa_moderation_log_v1';
const String kSuggestionsKey = 'loksewa_suggestions_v1';

/// Duplicate-similarity threshold (vanilla `findDuplicate`: token-Jaccard >= 0.8).
const double kDuplicateThreshold = 0.8;

/// Spam guard: max 5 submissions/suggestions per hour per device (vanilla `rateLimitCheck`).
const int kRateLimitPerHour = 5;

/// Spam guard: an exact question already queued 3+ times is refused (vanilla).
const int kMaxIdenticalInQueue = 3;

// ---------------------------------------------------------------------------
// Pure helpers — vanilla `normaliseText`, `hasUrl`, `repeatedChars`,
// `capsRatio`, `jaccardNorm`.
// ---------------------------------------------------------------------------

/// Lowercase, strip punctuation, collapse whitespace (vanilla `normaliseText`).
String normaliseText(Object? s) => (s ?? '')
    .toString()
    .toLowerCase()
    .replaceAll(RegExp(r'[^\p{L}\p{N} ]', unicode: true), ' ')
    .replaceAll(RegExp(r'\s+'), ' ')
    .trim();

bool hasUrl(Object? s) => RegExp(
      r'(https?:\/\/|www\.)',
      caseSensitive: false,
    ).hasMatch((s ?? '').toString());

bool repeatedChars(Object? s) =>
    RegExp(r'(.)\1{4,}').hasMatch((s ?? '').toString());

/// Ratio of A-Z letters to all A-Z/a-z letters (vanilla `capsRatio`).
double capsRatio(Object? s) {
  final letters = (s ?? '').toString().replaceAll(RegExp(r'[^A-Za-z]'), '');
  if (letters.isEmpty) return 0;
  final caps = letters.replaceAll(RegExp(r'[^A-Z]'), '').length;
  return caps / letters.length;
}

/// Token-Jaccard of two ALREADY-normalised strings (vanilla `jaccardNorm`).
double jaccardNorm(String nA, String nB) {
  final a = nA.split(' ').where((t) => t.isNotEmpty).toSet();
  final b = nB.split(' ').where((t) => t.isNotEmpty).toSet();
  if (a.isEmpty || b.isEmpty) return 0;
  final inter = a.where(b.contains).length;
  return inter / (a.length + b.length - inter);
}

/// A duplicate hit against a question bank (vanilla `findDuplicate` result).
class DuplicateHit {
  final String type; // 'exact' | 'near'
  final double score;
  final Map<String, dynamic> match;
  const DuplicateHit({
    required this.type,
    required this.score,
    required this.match,
  });
}

/// Returns null (no duplicate), or a hit. Exact = normalised text identical;
/// near = token-Jaccard >= 0.8 on EN or NE text (vanilla semantics).
/// Each bank entry is a map with 'question' and optional 'question_ne'.
DuplicateHit? findDuplicate(
  String qEn,
  String qNe,
  List<Map<String, dynamic>> bank,
) {
  final nEn = normaliseText(qEn), nNe = normaliseText(qNe);
  DuplicateHit? best;
  for (final q in bank) {
    final bEn = normaliseText(q['question']);
    final bNe = normaliseText(q['question_ne']);
    if (bEn == nEn || (nNe.isNotEmpty && bNe.isNotEmpty && bNe == nNe)) {
      return DuplicateHit(type: 'exact', score: 1, match: q);
    }
    final s = max(
      jaccardNorm(nEn, bEn),
      nNe.isNotEmpty && bNe.isNotEmpty ? jaccardNorm(nNe, bNe) : 0.0,
    );
    if (s >= kDuplicateThreshold && (best == null || s > best.score)) {
      best = DuplicateHit(type: 'near', score: s, match: q);
    }
  }
  return best;
}

// ---------------------------------------------------------------------------
// Validation results
// ---------------------------------------------------------------------------

class ValidationResult {
  final bool ok;
  final List<String> errors;
  const ValidationResult({required this.ok, required this.errors});
}

/// Outcome of [CommunityStore.submitQuestion].
class SubmitOutcome {
  final bool ok;
  final List<String> errors; // validation errors
  final String? blockedMessage; // duplicate / spam / rate-limit block
  const SubmitOutcome({
    required this.ok,
    this.errors = const [],
    this.blockedMessage,
  });
}

/// Outcome of [CommunityStore.rateLimitCheck].
class RateLimitResult {
  final bool allowed;
  final int minutesLeft;
  final int count;
  const RateLimitResult({
    required this.allowed,
    required this.minutesLeft,
    required this.count,
  });
}

/// Pure rate-limit check: max [kRateLimitPerHour] per hour per device.
/// [timestampsMs] = epoch-ms list; [nowMs] injectable for tests
/// (vanilla `rateLimitCheck`).
RateLimitResult rateLimitCheck(List<int> timestampsMs, {int? nowMs}) {
  final t = nowMs ?? DateTime.now().millisecondsSinceEpoch;
  final recent = timestampsMs.where((x) => t - x < 3600 * 1000).toList();
  if (recent.length >= kRateLimitPerHour) {
    final oldest = recent.reduce(min);
    final minutesLeft = ((oldest + 3600 * 1000 - t) / 60000).ceil();
    return RateLimitResult(
      allowed: false,
      minutesLeft: minutesLeft,
      count: recent.length,
    );
  }
  return RateLimitResult(allowed: true, minutesLeft: 0, count: recent.length);
}

String _b(String en, String ne, bool nepali) => nepali ? ne : en;

/// Pure validation of a question submission (vanilla `validateSubmission`).
/// [d] keys: exam, topic, subtopic, difficulty, marks (int), question,
/// question_ne, options (List, 4), options_ne (List, 4), answer (0-3),
/// explanation, explanation_ne, source, contributor.
ValidationResult validateSubmission(
  Map<String, dynamic> d, {
  bool nepali = false,
}) {
  final errors = <String>[];
  void need(Object? v, String en, String ne) {
    if ((v ?? '').toString().trim().isEmpty) {
      errors.add(
        _b(en, ne, nepali) + _b(' is required.', ' आवश्यक छ।', nepali),
      );
    }
  }

  need(d['exam'], 'Exam', 'परीक्षा');
  need(d['topic'], 'Topic', 'विषय');
  need(d['difficulty'], 'Difficulty', 'कठिनाइ');
  need(d['question'], 'Question (English)', 'प्रश्न (अङ्ग्रेजी)');
  need(d['question_ne'], 'Question (Nepali)', 'प्रश्न (नेपाली)');
  need(d['explanation'], 'Explanation (English)', 'व्याख्या (अङ्ग्रेजी)');
  need(d['explanation_ne'], 'Explanation (Nepali)', 'व्याख्या (नेपाली)');
  need(d['source'], 'Source', 'स्रोत');
  need(d['contributor'], 'Contributor name', 'योगदानकर्ताको नाम');

  final marks = d['marks'];
  if (marks is! int || (marks != 1 && marks != 2)) {
    errors.add(_b('Marks must be 1 or 2.', 'अङ्क १ वा २ हुनुपर्छ।', nepali));
  }
  if ((d['question'] ?? '').toString().trim().length < 15) {
    errors.add(
      _b(
        'Question must be at least 15 characters.',
        'प्रश्न कम्तीमा १५ अक्षरको हुनुपर्छ।',
        nepali,
      ),
    );
  }
  if (hasUrl(d['question']) || hasUrl(d['question_ne'])) {
    errors.add(
      _b(
        'Do not put links in the question text — the source field is the only place for links.',
        'प्रश्न पाठमा लिङ्क नराख्नुहोस् — लिङ्कका लागि स्रोत फिल्ड मात्र हो।',
        nepali,
      ),
    );
  }
  if (repeatedChars(d['question']) || repeatedChars(d['question_ne'])) {
    errors.add(
      _b(
        'Question text contains repeated characters (e.g. "!!!!!") — please write normally.',
        'प्रश्न पाठमा दोहोरिएका अक्षर छन् (जस्तै "!!!!!") — सामान्य रूपमा लेख्नुहोस्।',
        nepali,
      ),
    );
  }
  if (capsRatio(d['question']) > 0.5) {
    errors.add(
      _b(
        'Question is mostly ALL CAPS — please write normally.',
        'प्रश्न प्रायः सबै ठूलो अक्षरमा छ — सामान्य रूपमा लेख्नुहोस्।',
        nepali,
      ),
    );
  }

  void checkOpts(Object? opts, String en, String ne) {
    final list = opts is List ? opts : const [];
    if (list.length != 4) {
      errors.add(
        _b(en, ne, nepali) +
            _b(
              ': exactly 4 options are required.',
              ': ठ्याक्कै ४ विकल्प आवश्यक छ।',
              nepali,
            ),
      );
      return;
    }
    final seen = <String>{};
    for (var i = 0; i < 4; i++) {
      final t = (list[i] ?? '').toString().trim();
      if (t.isEmpty) {
        errors.add(
          '${_b(en, ne, nepali)}: ${_b('option ', 'विकल्प ', nepali)}${String.fromCharCode(65 + i)}${_b(' is empty.', ' खाली छ।', nepali)}',
        );
      }
      final n = normaliseText(t);
      if (n.isNotEmpty && seen.contains(n)) {
        errors.add(
          _b(en, ne, nepali) +
              _b(
                ': options must all be different — two options say the same thing.',
                ': सबै विकल्प फरक हुनुपर्छ — दुई विकल्प एउटै कुरा भन्छन्।',
                nepali,
              ),
        );
      }
      seen.add(n);
    }
  }

  checkOpts(d['options'], 'Options (English)', 'विकल्पहरू (अङ्ग्रेजी)');
  checkOpts(d['options_ne'], 'Options (Nepali)', 'विकल्पहरू (नेपाली)');

  final answer = d['answer'];
  if (answer is! int || answer < 0 || answer > 3) {
    errors.add(
      _b(
        'Correct answer must be A, B, C or D.',
        'सही उत्तर A, B, C वा D हुनुपर्छ।',
        nepali,
      ),
    );
  }
  return ValidationResult(ok: errors.isEmpty, errors: errors);
}

/// Pure validation of a suggestion (vanilla `validateSuggestion`).
/// [d] keys: title, description, category. [categories] = valid ids.
ValidationResult validateSuggestion(
  Map<String, dynamic> d,
  List<String> categories, {
  bool nepali = false,
}) {
  final errors = <String>[];
  final title = (d['title'] ?? '').toString().trim();
  final desc = (d['description'] ?? '').toString().trim();
  if (title.isEmpty) {
    errors.add(_b('Title is required.', 'शीर्षक आवश्यक छ।', nepali));
  } else if (title.length < 8) {
    errors.add(
      _b(
        'Title must be at least 8 characters.',
        'शीर्षक कम्तीमा ८ अक्षरको हुनुपर्छ।',
        nepali,
      ),
    );
  }
  if (desc.isEmpty) {
    errors.add(_b('Description is required.', 'विवरण आवश्यक छ।', nepali));
  } else if (desc.length < 20) {
    errors.add(
      _b(
        'Description must be at least 20 characters — say what it should do and why.',
        'विवरण कम्तीमा २० अक्षरको हुनुपर्छ — के गर्ने र किन भन्नुहोस्।',
        nepali,
      ),
    );
  }
  if (!categories.contains(d['category'])) {
    errors.add(_b('Please pick a category.', 'श्रेणी छान्नुहोस्।', nepali));
  }
  if (hasUrl(title) || hasUrl(desc)) {
    errors.add(
      _b(
        'No links, please — describe the idea in words.',
        'लिङ्क नराख्नुहोस् — विचार शब्दमा वर्णन गर्नुहोस्।',
        nepali,
      ),
    );
  }
  if (repeatedChars(title) || repeatedChars(desc)) {
    errors.add(
      _b(
        'Please write normally (no repeated characters like "!!!!!").',
        'सामान्य रूपमा लेख्नुहोस् (जस्तै "!!!!!" दोहोरिएको अक्षर नराख्नुहोस्)।',
        nepali,
      ),
    );
  }
  if (capsRatio(title) > 0.5) {
    errors.add(
      _b(
        "Please don't write in ALL CAPS.",
        'सबै ठूलो अक्षरमा नलेख्नुहोस्।',
        nepali,
      ),
    );
  }
  return ValidationResult(ok: errors.isEmpty, errors: errors);
}

/// Duplicate-title check (vanilla `isDuplicateSuggestion`): normalised equality.
bool isDuplicateSuggestion(List<Map<String, dynamic>> list, String title) {
  final n = normaliseText(title);
  return list.any((s) => normaliseText(s['title']) == n);
}

/// Suggestion categories (vanilla `SUG_CATS`: id, EN, NE).
const List<List<String>> suggestionCategories = [
  ['feature', 'New feature', 'नयाँ सुविधा'],
  ['topic', 'Topic request', 'विषय अनुरोध'],
  ['questions', 'Question set', 'प्रश्न सेट'],
  ['exam', 'New exam', 'नयाँ परीक्षा'],
  ['bug', 'Bug report', 'बग रिपोर्ट'],
  ['other', 'Other', 'अन्य'],
];

String _uid(String prefix) {
  final rnd = Random();
  return '$prefix-${DateTime.now().millisecondsSinceEpoch.toRadixString(36)}'
      '${(rnd.nextDouble() * 1e6).floor().toRadixString(36)}';
}

String _nowIso() => DateTime.now().toUtc().toIso8601String();

// ---------------------------------------------------------------------------
// Seed data — vanilla `seedDiscussions()` / `seedSuggestions()` verbatim.
// ---------------------------------------------------------------------------

List<Map<String, dynamic>> _seedDiscussions() {
  Map<String, dynamic> t(
    String id,
    String exam,
    String title,
    String body,
    String author,
    List<Map<String, dynamic>> replies,
  ) {
    return {
      'id': id,
      'exam': exam,
      'title': title,
      'body': body,
      'author': author,
      'createdAt': '2026-10-26T08:00:00Z',
      'upvotes': 0,
      'replies': replies,
      'reports': <Map<String, dynamic>>[],
    };
  }

  Map<String, dynamic> r(String author, String body, String createdAt) => {
        'author': author,
        'body': body,
        'createdAt': createdAt,
      };

  return [
    t(
      'DIS-001',
      'kharidar',
      'Kharidar prelim: is negative marking really 20%?',
      'I keep hearing different numbers — some guides say 0.25 per wrong answer, some say 20%. Which one does the real Kharidar prelim use?',
      'Guest aspirant',
      [
        r(
          'Ravi (maintainer)',
          '20% — a wrong 2-mark question costs −0.4. That is the PSC rule the mocks here use. The 0.25 figure is from older papers / other exams.',
          '2026-10-26T08:30:00Z',
        ),
      ],
    ),
    t(
      'DIS-002',
      'nasu',
      'NaSu Paper II — what should I study for the subjective paper?',
      'Prelim is MCQ, but Paper II is descriptive. Any good sources for office procedure + report writing?',
      'Guest aspirant',
      [],
    ),
    t(
      'DIS-003',
      'section-officer',
      'Section Officer GK: how deep does Constitution 2072 go?',
      'Do they ask article numbers, or just the big ideas (fundamental rights, federal structure)?',
      'Guest aspirant',
      [
        r(
          'Ravi (maintainer)',
          'Both — article numbers for the famous ones (e.g. fundamental rights, Art. 17–33) and the structure for the rest. The Constitution topic in Practice covers the high-yield articles.',
          '2026-10-26T09:00:00Z',
        ),
      ],
    ),
    t(
      'DIS-004',
      'tsc-license',
      'TSC licence exam pattern — is the time limit really unverified?',
      'The guide says the licence time limit is unverified. Has anyone seen the official TSC notice?',
      'Guest aspirant',
      [],
    ),
    t(
      'DIS-005',
      'nrb-assistant',
      'NRB Assistant: management vs economics weightage?',
      'The mock mixes both — which section carries more marks in the real paper?',
      'Guest aspirant',
      [],
    ),
    t(
      'DIS-006',
      'nmc-mbbs',
      'NMC licence: do the 10 CSQs count in the mock here?',
      'The real MBBS licence has 130 MCQs + 10 clinical scenario questions. This mock only has the 130 — is that right?',
      'Guest aspirant',
      [
        r(
          'Ravi (maintainer)',
          'Yes — the mock here is the MCQ part only (130/130, pass judged at 50% of the real 180 total). CSQs cannot be auto-marked yet, so they are noted on the guide card instead.',
          '2026-10-26T09:15:00Z',
        ),
      ],
    ),
    t(
      'DIS-007',
      'nnc-rn',
      'Nursing licence (NLEN): no negative marking — confirmed?',
      'I have heard there is no negative marking in the nursing licence. Can someone confirm from the NNC notice?',
      'Guest aspirant',
      [],
    ),
    t(
      'DIS-008',
      'npc-pharmacy',
      'Pharmacy licence: 50% in EACH subject or overall?',
      'Some seniors say you need 50% in every subject, others say 50% overall. Which is it?',
      'Guest aspirant',
      [],
    ),
    t(
      'DIS-009',
      'general',
      'General doubts — ask anything about Lok Sewa prep',
      'Stuck on a topic, confused by a pattern, or not sure which exam to target? Ask here.',
      'Ravi (maintainer)',
      [],
    ),
  ];
}

List<Map<String, dynamic>> _seedSuggestions() {
  Map<String, dynamic> t(
    String id,
    String category,
    String title,
    String description,
  ) {
    return {
      'id': id,
      'category': category,
      'title': title,
      'description': description,
      'by': 'Guest aspirant',
      'at': '2026-10-31T08:00:00Z',
      'upvotes': 0,
      'voters': <String>[],
      '_seed': true,
    };
  }

  return [
    t(
      'SUG-SEED-1',
      'feature',
      'Spaced-repetition reminders',
      'A gentle nudge that resurfaces topics I keep getting wrong, on a 1-3-7 day schedule — so weak areas get revised automatically.',
    ),
    t(
      'SUG-SEED-2',
      'exam',
      'NEA (Nepal Electricity Authority) exam',
      'NEA publishes technical + GK papers for its levels. A practice set for NEA aspirants would help engineering candidates.',
    ),
    t(
      'SUG-SEED-3',
      'questions',
      'Most-asked GK lightning round',
      'A dedicated speed set of the most repeated PSC questions across 12 years of papers — the 80/20 facts for last-week revision.',
    ),
  ];
}

// ---------------------------------------------------------------------------
// Store
// ---------------------------------------------------------------------------

/// On-device community store. ChangeNotifier over shared_preferences using
/// the vanilla-identical keys. The local display name / voter id are injected
/// (default: Guest) — there is no real account yet (Supabase comes later).
class CommunityStore extends ChangeNotifier {
  /// Display name new threads/replies/submissions/suggestions are posted under.
  String authorName;

  /// Voter identity for suggestion upvote toggling (vanilla `voterId()`).
  String voterId;

  CommunityStore({this.authorName = 'Guest', this.voterId = 'guest'});

  List<Map<String, dynamic>> _threads = [];
  List<Map<String, dynamic>> _submissions = [];
  List<Map<String, dynamic>> _approved = [];
  List<Map<String, dynamic>> _suggestions = [];

  bool _loaded = false;
  bool get loaded => _loaded;

  Future<SharedPreferences> _prefs() => SharedPreferences.getInstance();

  List<Map<String, dynamic>> _decodeList(String? raw) {
    if (raw == null || raw.isEmpty) return [];
    try {
      final v = json.decode(raw);
      if (v is List) {
        return v.map((e) => Map<String, dynamic>.from(e as Map)).toList();
      }
    } catch (_) {}
    return [];
  }

  /// Loads everything, seeding first-run data exactly like vanilla
  /// (`loadDiscussions` / `loadSuggestions`).
  Future<void> init() async {
    final prefs = await _prefs();
    final d = prefs.getString(kDiscussionsKey);
    if (d == null) {
      _threads = _seedDiscussions();
      await prefs.setString(kDiscussionsKey, json.encode(_threads));
    } else {
      _threads = _decodeList(d);
    }
    _submissions = _decodeList(prefs.getString(kSubmissionsKey));
    _approved = _decodeList(prefs.getString(kApprovedKey));
    final s = prefs.getString(kSuggestionsKey);
    if (s == null) {
      _suggestions = _seedSuggestions();
      await prefs.setString(kSuggestionsKey, json.encode(_suggestions));
    } else {
      _suggestions = _decodeList(s);
    }
    _loaded = true;
    notifyListeners();
  }

  // ---------------- Discussion Hub ----------------

  /// Threads in newest-first order (vanilla `unshift`s new threads).
  List<Map<String, dynamic>> get threads => List.unmodifiable(_threads);

  /// Vanilla renders newest-first; the app additionally offers top (upvotes).
  List<Map<String, dynamic>> threadsSorted(String sort) {
    final list = List<Map<String, dynamic>>.from(_threads);
    if (sort == 'top') {
      list.sort(
        (a, b) =>
            ((b['upvotes'] ?? 0) as int).compareTo((a['upvotes'] ?? 0) as int),
      );
    }
    return list;
  }

  Map<String, dynamic>? threadById(String id) {
    for (final t in _threads) {
      if (t['id'] == id) return t;
    }
    return null;
  }

  /// Validates a new thread (vanilla `postThread`: title >= 8, body >= 10).
  /// Returns the error list (empty = ok).
  List<String> validateThread(String title, String body, bool nepali) {
    final errors = <String>[];
    if (title.trim().length < 8) {
      errors.add(
        nepali
            ? 'कृपया थ्रेडलाई शीर्षक दिनुहोस् (कम्तीमा ८ अक्षर)।'
            : 'Please give your thread a title (at least 8 characters).',
      );
    }
    if (body.trim().length < 10) {
      errors.add(
        nepali
            ? 'कृपया आफ्नो शङ्का वर्णन गर्नुहोस् (कम्तीमा १० अक्षर)।'
            : 'Please describe your doubt (at least 10 characters).',
      );
    }
    return errors;
  }

  Future<List<String>> addThread({
    required String exam,
    required String title,
    required String body,
    bool nepali = false,
  }) async {
    final errors = validateThread(title, body, nepali);
    if (errors.isNotEmpty) return errors;
    _threads.insert(0, {
      'id': _uid('DIS'),
      'exam': exam,
      'title': title.trim(),
      'body': body.trim(),
      'author': authorName,
      'createdAt': _nowIso(),
      'upvotes': 0,
      'replies': <Map<String, dynamic>>[],
      'reports': <Map<String, dynamic>>[],
    });
    await _save(kDiscussionsKey, _threads);
    notifyListeners();
    return const [];
  }

  /// Adds a reply (vanilla `postReply`: body >= 2 chars).
  /// Returns an error string, or null on success.
  Future<String?> addReply(String threadId, String body, bool nepali) async {
    if (body.trim().length < 2) {
      return nepali ? 'पहिले उत्तर लेख्नुहोस्।' : 'Please write a reply first.';
    }
    final th = threadById(threadId);
    if (th == null) return null;
    (th['replies'] as List).add({
      'author': authorName,
      'body': body.trim(),
      'createdAt': _nowIso(),
    });
    await _save(kDiscussionsKey, _threads);
    notifyListeners();
    return null;
  }

  /// Upvote a thread (vanilla `upvoteThread`: increments — NOT a toggle).
  Future<void> upvoteThread(String threadId) async {
    final th = threadById(threadId);
    if (th == null) return;
    th['upvotes'] = ((th['upvotes'] ?? 0) as int) + 1;
    await _save(kDiscussionsKey, _threads);
    notifyListeners();
  }

  /// Report a thread or one of its replies (vanilla `reportPost`).
  Future<void> reportPost(
    String threadId,
    String reason, {
    int? replyIndex,
  }) async {
    final th = threadById(threadId);
    if (th == null) return;
    (th['reports'] as List).add({
      'replyIndex': replyIndex,
      'reason': reason.trim().isEmpty ? 'no reason given' : reason.trim(),
      'by': authorName,
      'at': _nowIso(),
    });
    await _save(kDiscussionsKey, _threads);
    notifyListeners();
  }

  // ---------------- Submit-a-Question ----------------

  List<Map<String, dynamic>> get submissions => List.unmodifiable(_submissions);

  List<Map<String, dynamic>> get pendingSubmissions =>
      _submissions.where((s) => s['status'] == 'pending').toList();

  List<Map<String, dynamic>> get approvedQuestions =>
      List.unmodifiable(_approved);

  Map<String, int> submissionCounts() => {
        'approved': _submissions.where((s) => s['status'] == 'approved').length,
        'rejected': _submissions.where((s) => s['status'] == 'rejected').length,
        'pending': _submissions.where((s) => s['status'] == 'pending').length,
      };

  List<int> _submissionTimestamps() => _submissions
      .map((s) => (s['submittedAt'] as num?)?.toInt() ?? 0)
      .where((t) => t > 0)
      .toList();

  /// Submits a question: validation -> duplicate check (against local
  /// pending + approved items; the full-bank check runs server-side later) ->
  /// spam guards (3 identical in queue, double-submit of a pending item) ->
  /// rate limit (5/hour). On success the entry goes to the REVIEW QUEUE with
  /// status 'pending' — it never goes live instantly (vanilla `submitQuestion`).
  Future<SubmitOutcome> submitQuestion(
    Map<String, dynamic> d, {
    bool nepali = false,
  }) async {
    final v = validateSubmission(d, nepali: nepali);
    if (!v.ok) return SubmitOutcome(ok: false, errors: v.errors);

    final question = (d['question'] ?? '').toString().trim();
    final questionNe = (d['question_ne'] ?? '').toString().trim();

    // Duplicate check against the local bank: approved community questions
    // (vanilla checks the full QUESTIONS bank; pending items are NOT in the
    // bank — a pending re-submit is caught by the alreadyPending guard below).
    final dup = findDuplicate(question, questionNe, _approved);
    if (dup != null) {
      final msg = dup.type == 'exact'
          ? 'This question already exists (${dup.match['id']}). Please submit a different question.'
          : 'This looks like an existing question (${dup.match['id']}, similarity ${(dup.score * 100).round()}%). Please check it and submit something different.';
      return SubmitOutcome(ok: false, blockedMessage: msg);
    }

    // Spam: 3 identical submissions already in the queue.
    final same = _submissions
        .where((s) => normaliseText(s['question']) == normaliseText(question))
        .length;
    if (same >= kMaxIdenticalInQueue) {
      return const SubmitOutcome(
        ok: false,
        blockedMessage:
            'This exact question has already been submitted 3 times — it is in the review queue. Please submit something different.',
      );
    }
    // Double-submit guard: an identical pending item means the button was
    // double-tapped — do not queue a second copy (vanilla `alreadyPending`).
    final alreadyPending = _submissions.any(
      (s) =>
          s['status'] == 'pending' &&
          normaliseText(s['question']) == normaliseText(question),
    );
    if (alreadyPending) {
      return const SubmitOutcome(
        ok: false,
        blockedMessage:
            'This question is already in the review queue (pending) — it was submitted once already. Please submit something different.',
      );
    }

    // Rate limit: max 5 per hour per device.
    final rl = rateLimitCheck(_submissionTimestamps());
    if (!rl.allowed) {
      return SubmitOutcome(
        ok: false,
        blockedMessage: nepali
            ? 'दर सीमा: पछिल्लो घण्टामा ५ प्रश्न पेस गरिसक्नुभयो। करिब ${rl.minutesLeft} मिनेट पर्खेर पुनः प्रयास गर्नुहोस्।'
            : 'Rate limit: you have submitted 5 questions in the last hour. Please wait about ${rl.minutesLeft} minute(s) and try again.',
      );
    }

    _submissions.add({
      'id': _uid('SUB'),
      'status': 'pending',
      'submittedAt': DateTime.now().millisecondsSinceEpoch,
      'exam': d['exam'],
      'topic': (d['topic'] ?? '').toString().trim(),
      'subtopic': (d['subtopic'] ?? '').toString().trim(),
      'difficulty': d['difficulty'],
      'marks': d['marks'],
      'question': question,
      'question_ne': questionNe,
      'options': (d['options'] as List)
          .map((o) => (o ?? '').toString().trim())
          .toList(),
      'options_ne': (d['options_ne'] as List)
          .map((o) => (o ?? '').toString().trim())
          .toList(),
      'answer': d['answer'],
      'explanation': (d['explanation'] ?? '').toString().trim(),
      'explanation_ne': (d['explanation_ne'] ?? '').toString().trim(),
      'source': (d['source'] ?? '').toString().trim(),
      'contributor': authorName,
    });
    await _save(kSubmissionsKey, _submissions);
    notifyListeners();
    return const SubmitOutcome(ok: true);
  }

  String _nextCommunityId() {
    final n = _approved.length + 1;
    return 'COMM-${n.toString().padLeft(3, '0')}';
  }

  Future<void> _modLog(
    String action,
    String submissionId,
    String reason,
  ) async {
    final prefs = await _prefs();
    final log = _decodeList(prefs.getString(kModLogKey));
    log.add({
      'action': action,
      'submissionId': submissionId,
      'by': 'Ravi Yadav (demo maintainer)',
      'reason': reason,
      'at': _nowIso(),
    });
    await prefs.setString(kModLogKey, json.encode(log));
  }

  /// Approves a pending submission into `loksewa_community_approved_v1`
  /// (vanilla `approveSubmission`; the in-app review queue is the
  /// local-preview stand-in for the maintainer).
  Future<Map<String, dynamic>?> approveSubmission(String id) async {
    final idx = _submissions.indexWhere((s) => s['id'] == id);
    if (idx < 0) return null;
    final sub = _submissions[idx];
    if (sub['status'] != 'pending') return null;
    final q = {
      'id': _nextCommunityId(),
      'exam': [sub['exam']],
      'topic': sub['topic'],
      'subtopic': sub['subtopic'] ?? '',
      'difficulty': sub['difficulty'],
      'marks': sub['marks'],
      'question': sub['question'],
      'question_ne': sub['question_ne'],
      'options': sub['options'],
      'options_ne': sub['options_ne'],
      'answer': sub['answer'],
      'explanation': sub['explanation'],
      'explanation_ne': sub['explanation_ne'],
      'source':
          'Community: ${sub['contributor'] ?? 'anonymous'} — ${sub['source']}',
    };
    _approved.add(q);
    sub['status'] = 'approved';
    await _save(kApprovedKey, _approved);
    await _save(kSubmissionsKey, _submissions);
    await _modLog('approved', id, '');
    notifyListeners();
    return q;
  }

  /// Rejects a pending submission — a reason is required (vanilla `rejectSubmission`).
  Future<bool> rejectSubmission(String id, String reason) async {
    if (reason.trim().isEmpty) return false;
    final idx = _submissions.indexWhere((s) => s['id'] == id);
    if (idx < 0) return false;
    final sub = _submissions[idx];
    if (sub['status'] != 'pending') return false;
    sub['status'] = 'rejected';
    sub['rejectReason'] = reason.trim();
    await _save(kSubmissionsKey, _submissions);
    await _modLog('rejected', id, reason.trim());
    notifyListeners();
    return true;
  }

  // ---------------- Suggestions ----------------

  /// Suggestions sorted by upvotes desc (vanilla `renderSuggest`).
  List<Map<String, dynamic>> get suggestions {
    final list = List<Map<String, dynamic>>.from(_suggestions);
    list.sort(
      (a, b) =>
          ((b['upvotes'] ?? 0) as int).compareTo((a['upvotes'] ?? 0) as int),
    );
    return List.unmodifiable(list);
  }

  List<String> get categoryIds =>
      suggestionCategories.map((c) => c[0]).toList();

  /// Adds a suggestion: validation -> duplicate-title block -> rate limit
  /// (5/hour, same rule as submissions; vanilla `submitSuggestion`).
  /// Returns the error list (empty = ok).
  Future<List<String>> addSuggestion({
    required String title,
    required String description,
    required String category,
    bool nepali = false,
  }) async {
    final v = validateSuggestion(
      {'title': title, 'description': description, 'category': category},
      categoryIds,
      nepali: nepali,
    );
    if (!v.ok) return v.errors;
    if (isDuplicateSuggestion(_suggestions, title)) {
      return [
        nepali
            ? 'यो सुझाव सूचीमा पहिले नै छ — मत दिनुहोस्!'
            : 'This suggestion is already on the list — upvote it instead!',
      ];
    }
    final ts = _suggestions
        .map((s) => s['at'])
        .whereType<String>()
        .map((iso) => DateTime.tryParse(iso)?.millisecondsSinceEpoch ?? 0)
        .where((t) => t > 0)
        .toList();
    final rl = rateLimitCheck(ts);
    if (!rl.allowed) {
      return [
        nepali
            ? 'दर सीमा: प्रति घण्टा ५ सुझाव। करिब ${rl.minutesLeft} मिनेट पर्खनुहोस्।'
            : 'Rate limit: 5 suggestions per hour. Please wait about ${rl.minutesLeft} minute(s).',
      ];
    }
    _suggestions.insert(0, {
      'id': _uid('SUG'),
      'category': category,
      'title': title.trim(),
      'description': description.trim(),
      'by': authorName,
      'at': _nowIso(),
      'upvotes': 0,
      'voters': <String>[],
    });
    await _save(kSuggestionsKey, _suggestions);
    notifyListeners();
    return const [];
  }

  /// Upvote TOGGLE via the voters list (vanilla `upvoteSuggestion`).
  Future<void> upvoteSuggestion(String id) async {
    Map<String, dynamic>? s;
    for (final x in _suggestions) {
      if (x['id'] == id) {
        s = x;
        break;
      }
    }
    if (s == null) return;
    final voters = (s['voters'] as List).map((e) => e.toString()).toList();
    final i = voters.indexOf(voterId);
    if (i >= 0) {
      voters.removeAt(i);
      s['upvotes'] = max(0, ((s['upvotes'] ?? 1) as int) - 1);
    } else {
      voters.add(voterId);
      s['upvotes'] = ((s['upvotes'] ?? 0) as int) + 1;
    }
    s['voters'] = voters;
    await _save(kSuggestionsKey, _suggestions);
    notifyListeners();
  }

  /// Has this device's voter already upvoted [suggestion]?
  bool hasVoted(Map<String, dynamic> suggestion) =>
      ((suggestion['voters'] ?? []) as List)
          .map((e) => e.toString())
          .contains(voterId);

  // ---------------- persistence ----------------

  Future<void> _save(String key, List<Map<String, dynamic>> list) async {
    final prefs = await _prefs();
    await prefs.setString(key, json.encode(list));
  }
}
