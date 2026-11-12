/// Course progress store — ChangeNotifier over shared_preferences using the
/// IDENTICAL key as the vanilla site: 'loksewa_course_progress_v1'
/// (app.js COURSE_PROG_KEY), same shape:
///   {done: {chapterId: true}, last: {exam, chId, ts}}
/// Note: vanilla uses a done-OBJECT keyed by id; here we use a Set<String>
/// internally and serialise back to the object shape so the stored JSON stays
/// byte-compatible with the vanilla site for users who open both.
library;

import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Must match vanilla's COURSE_PROG_KEY (app.js "Theory courses" section).
const String courseProgressKey = 'loksewa_course_progress_v1';

class LastRead {
  final String exam;
  final String chapterId;
  final int ts;

  const LastRead({
    required this.exam,
    required this.chapterId,
    required this.ts,
  });

  Map<String, dynamic> toJson() => {'exam': exam, 'chId': chapterId, 'ts': ts};

  factory LastRead.fromJson(Map<String, dynamic> j) => LastRead(
        exam: j['exam'] as String? ?? '',
        chapterId: j['chId'] as String? ?? '',
        ts: (j['ts'] as num?)?.toInt() ?? 0,
      );
}

class CourseProgressStore extends ChangeNotifier {
  final Set<String> done = {};
  LastRead? last;

  bool get isLoaded => _loaded;
  bool _loaded = false;

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    try {
      final raw = prefs.getString(courseProgressKey);
      if (raw != null && raw.isNotEmpty) {
        final p = jsonDecode(raw) as Map<String, dynamic>;
        final d = p['done'];
        if (d is Map<String, dynamic>) {
          done
            ..clear()
            ..addAll(d.entries.where((e) => e.value == true).map((e) => e.key));
        } else if (d is List) {
          // Defensive: accept the task-spec array shape too.
          done
            ..clear()
            ..addAll(d.map((e) => e.toString()));
        }
        final l = p['last'];
        last = l is Map<String, dynamic> ? LastRead.fromJson(l) : null;
      }
    } catch (_) {
      done.clear();
      last = null;
    }
    _loaded = true;
    notifyListeners();
  }

  Future<void> _save() async {
    final prefs = await SharedPreferences.getInstance();
    // Serialize done as {id: true} — the exact vanilla shape.
    await prefs.setString(
      courseProgressKey,
      jsonEncode({
        'done': {for (final id in done) id: true},
        'last': last?.toJson(),
      }),
    );
  }

  bool isDone(String chapterId) => done.contains(chapterId);

  /// Toggle read state — vanilla setChapterDone(id, !isChapterDone(id)).
  Future<void> toggle(String chapterId) async {
    if (done.contains(chapterId)) {
      done.remove(chapterId);
    } else {
      done.add(chapterId);
    }
    await _save();
    notifyListeners();
  }

  /// Record the last opened chapter — vanilla openCourseChapter's
  /// `p.last = {exam, chId, ts: Date.now()}`.
  Future<void> markOpened(String exam, String chapterId) async {
    last = LastRead(
      exam: exam,
      chapterId: chapterId,
      ts: DateTime.now().millisecondsSinceEpoch,
    );
    await _save();
    notifyListeners();
  }
}
