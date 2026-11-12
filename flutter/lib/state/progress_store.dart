/// Progress store — ChangeNotifier over shared_preferences using the
/// VANILLA-IDENTICAL key `loksewa_progress_v1` and the identical JSON shape,
/// so web progress carries over between the vanilla site and this app.
///
/// Vanilla reference: loksewa-prep-nepal/assets/js/app.js
/// (`LS_KEY`, `loadProgress`/`migrateProgress`, `updateStreak`,
/// `xpFor`, `levelFromXp`, `checkWeeklyGoal`, `badges`).
library;

import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../engine/quiz_engine.dart';

/// Vanilla localStorage key — must stay identical so progress carries over.
const String kProgressKey = 'loksewa_progress_v1';

/// Vanilla report box key (Report button on a question).
const String kReportsKey = 'loksewa_reports_v1';

String _todayStr() => DateTime.now().toUtc().toIso8601String().substring(0, 10);

String _yesterdayStr() => DateTime.now()
    .toUtc()
    .subtract(const Duration(days: 1))
    .toIso8601String()
    .substring(0, 10);

/// Monday (UTC) of the week containing [d] — matches vanilla `weekStartStr`.
String weekStartStr([DateTime? d]) {
  final t = (d ?? DateTime.now()).toUtc();
  final diff = (t.weekday + 6) % 7; // days since Monday
  final monday = DateTime.utc(t.year, t.month, t.day - diff);
  return monday.toIso8601String().substring(0, 10);
}

int _levelFromXp(int xp) => xp ~/ 500 + 1;
int _xpFor(double score) => score <= 0 ? 0 : (score * 10).round();

/// Outcome summary returned by [ProgressStore.recordAttempt].
class AttemptSummary {
  final bool passed;
  final int xp;
  final int oldLevel;
  final int newLevel;
  final bool leveledUp;
  final bool weeklyMet;

  const AttemptSummary({
    required this.passed,
    required this.xp,
    required this.oldLevel,
    required this.newLevel,
    required this.leveledUp,
    required this.weeklyMet,
  });
}

class ProgressStore extends ChangeNotifier {
  static ProgressStore? _instance;

  /// Shared singleton — screens await this, then record attempts on it.
  static Future<ProgressStore> get instance async =>
      _instance ??= await ProgressStore._load();

  /// Test / reset hook.
  @visibleForTesting
  static void resetForTest() => _instance = null;

  Map<String, dynamic> _p = {};

  ProgressStore._();

  static Future<ProgressStore> _load() async {
    final store = ProgressStore._();
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(kProgressKey);
    Map<String, dynamic> p = {};
    if (raw != null) {
      try {
        p = Map<String, dynamic>.from(json.decode(raw) as Map);
      } catch (_) {
        p = {};
      }
    }
    store._p = _migrate(p);
    return store;
  }

  /// Vanilla `migrateProgress` — old progress migrates in place, nothing lost.
  static Map<String, dynamic> _migrate(Map<String, dynamic> p) {
    p['xp'] ??= 0;
    p['level'] ??= 1;
    p['streak'] ??= 0;
    p['lastDay'] ??= '';
    if (p['attempts'] is! List) p['attempts'] = [];
    if (p['bookmarks'] is! List) p['bookmarks'] = [];
    if (p['mistakes'] is! List) p['mistakes'] = [];
    p['flashcardsSeen'] ??= 0;
    if (p['dailyDone'] is! Map) p['dailyDone'] = {};
    if (p['qotdDone'] is! Map) p['qotdDone'] = {};
    p['weeklyTarget'] ??= 70;
    p['weeklyGoalsMet'] ??= 0;
    p['weeklyGoalMetWeek'] ??= '';
    if (p['funFactsSeen'] is! List) p['funFactsSeen'] = [];
    p['focusSessions'] ??= 0;
    p['focusMinutes'] ??= 0;
    return p;
  }

  Future<void> _save() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(kProgressKey, json.encode(_p));
    notifyListeners();
  }

  // --- reads ---
  int get xp => (_p['xp'] as num?)?.toInt() ?? 0;
  int get level => (_p['level'] as num?)?.toInt() ?? 1;
  int get streak => (_p['streak'] as num?)?.toInt() ?? 0;
  String get lastDay => _p['lastDay'] as String? ?? '';
  int get weeklyTarget => (_p['weeklyTarget'] as num?)?.toInt() ?? 70;
  int get weeklyGoalsMet => (_p['weeklyGoalsMet'] as num?)?.toInt() ?? 0;

  /// Vanilla weekly-target selector (35/70/100/140).
  Future<void> setWeeklyTarget(int target) async {
    _p['weeklyTarget'] = target;
    await _save();
  }

  /// Vanilla "Reset progress" — wipes everything after user confirmation.
  /// The caller must confirm; this just executes.
  Future<void> resetProgress() async {
    _p['xp'] = 0;
    _p['level'] = 1;
    _p['streak'] = 0;
    _p['lastDay'] = '';
    _p['attempts'] = [];
    _p['bookmarks'] = [];
    _p['mistakes'] = [];
    _p['flashcardsSeen'] = 0;
    _p['dailyDone'] = {};
    _p['qotdDone'] = {};
    _p['weeklyGoalsMet'] = 0;
    _p['weeklyGoalMetWeek'] = '';
    _p['funFactsSeen'] = [];
    _p['focusSessions'] = 0;
    _p['focusMinutes'] = 0;
    await _save();
  }

  /// Daily-challenge bookkeeping (vanilla `progress.dailyDone[seed]`).
  bool isDailyDone(String seed) {
    final d = _p['dailyDone'];
    return d is Map && d[seed] == true;
  }

  Future<void> markDailyDone(String seed) async {
    final d = (_p['dailyDone'] is Map)
        ? Map<String, dynamic>.from(_p['dailyDone'] as Map)
        : <String, dynamic>{};
    d[seed] = true;
    _p['dailyDone'] = d;
    await _save();
  }

  List<Map<String, dynamic>> get attempts => (_p['attempts'] as List)
      .map((a) => Map<String, dynamic>.from(a as Map))
      .toList();

  List<String> get bookmarks =>
      (_p['bookmarks'] as List).map((e) => e.toString()).toList();

  List<String> get mistakes =>
      (_p['mistakes'] as List).map((e) => e.toString()).toList();

  // --- streak (vanilla `updateStreak`) ---
  Future<void> updateStreak() async {
    final t = _todayStr();
    if (lastDay == t) return;
    final y = _yesterdayStr();
    _p['streak'] = (lastDay == y) ? streak + 1 : 1;
    _p['lastDay'] = t;
    await _save();
  }

  // --- weekly goal (vanilla `checkWeeklyGoal` / `weeklyProgress`) ---
  int _questionsThisWeek() {
    final start = weekStartStr();
    final end = DateTime.parse('${start}T00:00:00Z')
        .add(const Duration(days: 7))
        .toIso8601String()
        .substring(0, 10);
    var sum = 0;
    for (final a in attempts) {
      final d = (a['date'] as String? ?? '').substring(0, 10);
      if (d.compareTo(start) >= 0 && d.compareTo(end) < 0) {
        sum += (a['total'] as num?)?.toInt() ?? 0;
      }
    }
    return sum;
  }

  /// First attempt that crosses this week's goal line records it.
  /// Returns true when the Weekly Champion badge is earned now.
  Future<bool> checkWeeklyGoal() async {
    final start = weekStartStr();
    final done = _questionsThisWeek();
    final target = weeklyTarget;
    if (done >= target && _p['weeklyGoalMetWeek'] != start) {
      _p['weeklyGoalMetWeek'] = start;
      _p['weeklyGoalsMet'] = weeklyGoalsMet + 1;
      await _save();
      return true;
    }
    return false;
  }

  // --- mistakes & bookmarks ---
  /// Vanilla `saveMistakeIfWrong`: wrong answers join the list, skips never.
  Future<void> addMistake(String questionId) async {
    final m = mistakes;
    if (!m.contains(questionId)) {
      m.add(questionId);
      _p['mistakes'] = m;
      await _save();
    }
  }

  Future<void> removeMistake(String questionId) async {
    final m = mistakes;
    if (m.remove(questionId)) {
      _p['mistakes'] = m;
      await _save();
    }
  }

  /// Toggle a bookmark; returns true when it was added.
  Future<bool> toggleBookmark(String questionId) async {
    final b = bookmarks;
    final added = !b.contains(questionId);
    if (added) {
      b.add(questionId);
    } else {
      b.remove(questionId);
    }
    _p['bookmarks'] = b;
    await _save();
    return added;
  }

  bool isBookmarked(String questionId) => bookmarks.contains(questionId);

  /// Ids from [questionIds] still on the mistakes list — what "retry wrong
  /// only" should drill.
  List<String> retryWrongOnly(List<String> questionIds) {
    final m = mistakes.toSet();
    return questionIds.where(m.contains).toList();
  }

  /// Save a question report (vanilla `loksewa_reports_v1`).
  Future<void> reportQuestion(String questionId, String note) async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(kReportsKey);
    List<dynamic> list = [];
    if (raw != null) {
      try {
        list = List<dynamic>.from(json.decode(raw) as List);
      } catch (_) {}
    }
    list.add({
      'id': questionId,
      'note': note,
      'date': DateTime.now().toUtc().toIso8601String(),
      'status': 'pending',
    });
    await prefs.setString(kReportsKey, json.encode(list));
  }

  // --- attempts (vanilla `finishAttempt` bookkeeping) ---
  Future<AttemptSummary> recordAttempt({
    required QuizResult result,
    required String mode,
    required String examId,
    required int cutoff,
    required int cutoffPct,
    bool timedOut = false,
    bool noXp = false, // daily-challenge repeat: vanilla burns no XP
    String? dailySeed, // marks progress.dailyDone[seed] on finish
  }) async {
    final passed = passesCutoff(result.pct, cutoffPct);
    final xpGain = noXp ? 0 : _xpFor(result.score);
    final oldLevel = level;
    _p['xp'] = xp + xpGain;
    _p['level'] = _levelFromXp(xp + xpGain);

    final attempt = <String, dynamic>{
      'date': DateTime.now().toUtc().toIso8601String(),
      'mode': mode,
      'exam': examId,
      'total': result.perQuestion.length,
      'score': result.score,
      'max': result.max,
      'pct': result.pct,
      'correct': result.correct,
      'wrong': result.wrong,
      'skipped': result.skipped,
      'passed': passed,
      'cutoff': cutoff,
      'cutoffPct': cutoffPct,
      'secs': result.secs,
      'xp': xpGain,
      'timedOut': timedOut,
      // Compact per-question rows: t=topic, c=1 correct / 0 wrong /
      // -1 skipped, m=marks (vanilla qdetail).
      'qdetail': result.perQuestion
          .map((d) => {'t': d.topic, 'c': d.code, 'm': d.marks})
          .toList(),
    };
    (_p['attempts'] as List).add(attempt);

    // Wrong answers appended, skips not (idempotent with addMistake).
    final m = mistakes.toSet();
    var mistakesChanged = false;
    for (final w in result.wrongList) {
      if (m.add(w.view.question.id)) mistakesChanged = true;
    }
    if (mistakesChanged) _p['mistakes'] = m.toList();

    await _save();
    await updateStreak();
    if (dailySeed != null) await markDailyDone(dailySeed);
    final weeklyMet = await checkWeeklyGoal();
    return AttemptSummary(
      passed: passed,
      xp: xpGain,
      oldLevel: oldLevel,
      newLevel: level,
      leveledUp: level > oldLevel,
      weeklyMet: weeklyMet,
    );
  }

  /// Topic with the lowest correct ratio across all attempts' qdetail
  /// (skips excluded). Null when there is no answered data.
  String? weakestTopic() {
    final total = <String, int>{};
    final correct = <String, int>{};
    for (final a in attempts) {
      final qd = a['qdetail'];
      if (qd is! List) continue;
      for (final row in qd) {
        if (row is! Map) continue;
        final t = row['t']?.toString() ?? 'General';
        final c = (row['c'] as num?)?.toInt() ?? -1;
        if (c == -1) continue; // skipped: not evidence
        total[t] = (total[t] ?? 0) + 1;
        if (c == 1) correct[t] = (correct[t] ?? 0) + 1;
      }
    }
    String? weakest;
    var worstRatio = 2.0;
    total.forEach((t, n) {
      final ratio = (correct[t] ?? 0) / n;
      if (ratio < worstRatio) {
        worstRatio = ratio;
        weakest = t;
      }
    });
    return weakest;
  }

  /// Computed badges — vanilla `badges()` verbatim. UI display is
  /// Milestone 5's job; the computation lives here.
  List<String> badges() {
    final b = <String>[];
    final n = attempts.length;
    if (n >= 1) b.add('First Practice');
    if (n >= 10) b.add('10 Sessions');
    if (n >= 50) b.add('50 Sessions');
    if (streak >= 3) b.add('3-Day Streak');
    if (streak >= 7) b.add('7-Day Streak');
    if (streak >= 30) b.add('30-Day Streak');
    if (xp >= 1000) b.add('1000 XP');
    if (xp >= 5000) b.add('5000 XP');
    final passed = attempts.where((a) => a['passed'] == true).length;
    if (passed >= 1) b.add('First Pass');
    if (passed >= 5) b.add('5 Mock Passes');
    if (weeklyGoalsMet >= 1) b.add('Weekly Champion');
    if (_questionsInADay() >= 100) b.add('Century Day');
    if (attempts.any((a) => a['mode'] == 'mock' && (a['pct'] as num?) == 100)) {
      b.add('Perfect Mock');
    }
    final funFacts = _p['funFactsSeen'];
    if (funFacts is List && funFacts.length >= 10) b.add('Fact Explorer');
    return b;
  }

  int _questionsInADay() {
    final per = <String, int>{};
    for (final a in attempts) {
      final d = (a['date'] as String? ?? '');
      final day = d.length >= 10 ? d.substring(0, 10) : d;
      per[day] = (per[day] ?? 0) + ((a['total'] as num?)?.toInt() ?? 0);
    }
    var max = 0;
    for (final v in per.values) {
      if (v > max) max = v;
    }
    return max;
  }
}
