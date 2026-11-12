/// Pure dashboard analytics — no Flutter imports, fully unit-testable.
///
/// Mirrors the vanilla site's helpers (loksewa-prep-nepal/assets/js/app.js):
/// `dailyChallenge` seeding, `weekStartStr` / `questionsThisWeek` /
/// `weeklyProgress`, the per-attempt `worst` topic sort in `finishAttempt`,
/// and `personalRecords` (`longestStreak`, `bestDay`, `personalBest`).
///
/// All functions take plain data (attempt maps in the vanilla JSON shape,
/// i.e. what [ProgressStore] persists under `loksewa_progress_v1`), so the
/// ProgressStore stays the single source of truth — this file only derives.
library;

/// Today's UTC date as `yyyy-MM-dd` — vanilla `todayStr()`, and the
/// Daily Challenge seed. The day is marked done only when the challenge is
/// finished (see vanilla `dailyChallenge` + `finishAttempt`).
String dailySeed([DateTime? now]) =>
    (now ?? DateTime.now()).toUtc().toIso8601String().substring(0, 10);

/// Vanilla `dailyChallenge` seed hash:
/// `for (const ch of seed) h = (h * 31 + ch.charCodeAt(0)) >>> 0`.
int seedHash(String seed) {
  var h = 0;
  for (final unit in seed.codeUnits) {
    h = ((h * 31) + unit) & 0xFFFFFFFF;
  }
  return h;
}

/// Vanilla `dailyChallenge` RNG: `h = (h * 1664525 + 1013904223) >>> 0`
/// per call, returning `h / 4294967296`. Same sequence as the vanilla site
/// for the same seed, so the Flutter daily set matches vanilla's.
class SeededRandom {
  int _h;
  SeededRandom(String seed) : _h = seedHash(seed);
  double next() {
    _h = ((_h * 1664525) + 1013904223) & 0xFFFFFFFF;
    return _h / 4294967296.0;
  }
}

/// Per-topic accuracy aggregated from attempt `qdetail` rows.
class TopicAccuracy {
  final String topic;
  final int total; // answered only — skips are not evidence
  final int correct;
  double get accuracy => total == 0 ? 0 : correct / total;
  double get accuracyPct => accuracy * 100;

  const TopicAccuracy({
    required this.topic,
    required this.total,
    required this.correct,
  });
}

/// Weakest topics across all attempts' `qdetail` (vanilla `finishAttempt`
/// sorts topics by `correct/total` ascending and shows the worst 3).
///
/// Vanilla applies no minimum-evidence threshold, so neither do we:
/// every topic with at least [minAnswered] answered questions is evidence
/// ([minAnswered] defaults to 1, matching vanilla). Skipped questions are
/// excluded, mirroring vanilla's qdetail semantics (c=-1 is "not evidence").
List<TopicAccuracy> weakTopics(
  List<Map<String, dynamic>> attempts, {
  int topN = 3,
  int minAnswered = 1,
}) {
  final total = <String, int>{};
  final correct = <String, int>{};
  for (final a in attempts) {
    final qd = a['qdetail'];
    if (qd is! List) continue;
    for (final row in qd) {
      if (row is! Map) continue;
      final t = row['t']?.toString() ?? 'General';
      final c = (row['c'] as num?)?.toInt() ?? -1;
      if (c != 0 && c != 1) continue; // skipped / unknown: not evidence
      total[t] = (total[t] ?? 0) + 1;
      if (c == 1) correct[t] = (correct[t] ?? 0) + 1;
    }
  }
  final list = total.entries
      .where((e) => e.value >= minAnswered)
      .map(
        (e) => TopicAccuracy(
          topic: e.key,
          total: e.value,
          correct: correct[e.key] ?? 0,
        ),
      )
      .toList();
  list.sort((a, b) => a.accuracy.compareTo(b.accuracy));
  return list.take(topN).toList();
}

/// Monday (UTC) of the week containing [d] — vanilla `weekStartStr`.
String mondayOfWeek([DateTime? d]) {
  final t = (d ?? DateTime.now()).toUtc();
  final diff = (t.weekday + 6) % 7; // days since Monday
  final monday = DateTime.utc(t.year, t.month, t.day - diff);
  return monday.toIso8601String().substring(0, 10);
}

/// Questions answered in the Mon–Sun week — vanilla `questionsThisWeek`.
int questionsThisWeek(List<Map<String, dynamic>> attempts, {DateTime? now}) {
  final start = mondayOfWeek(now);
  final end = DateTime.parse('${start}T00:00:00Z')
      .add(const Duration(days: 7))
      .toIso8601String()
      .substring(0, 10);
  var sum = 0;
  for (final a in attempts) {
    final d = (a['date'] as String? ?? '');
    final day = d.length >= 10 ? d.substring(0, 10) : d;
    if (day.compareTo(start) >= 0 && day.compareTo(end) < 0) {
      sum += (a['total'] as num?)?.toInt() ?? 0;
    }
  }
  return sum;
}

/// Vanilla `weeklyProgress`: `{target, done, pct, weekStart, met}`.
/// `pct` caps at 100 like vanilla (`Math.min(100, …)`).
class WeekProgress {
  final int target;
  final int done;
  final int pct;
  final String weekStart;
  final bool met;

  const WeekProgress({
    required this.target,
    required this.done,
    required this.pct,
    required this.weekStart,
    required this.met,
  });
}

WeekProgress weeklyProgress(
  List<Map<String, dynamic>> attempts,
  int weeklyTarget, {
  DateTime? now,
}) {
  final target =
      weeklyTarget <= 0 ? 70 : weeklyTarget; // vanilla: p.weeklyTarget || 70
  final done = questionsThisWeek(attempts, now: now);
  final start = mondayOfWeek(now);
  final pct = (done / target * 100).round().clamp(0, 100);
  return WeekProgress(
    target: target,
    done: done,
    pct: pct,
    weekStart: start,
    met: done >= target,
  );
}

/// The single best day (most questions), or null when no attempts.
/// Vanilla `bestDay` — ties keep the earliest day.
class BestDay {
  final String date; // yyyy-MM-dd (UTC)
  final int total;
  const BestDay({required this.date, required this.total});
}

BestDay? bestDay(List<Map<String, dynamic>> attempts) {
  final per = <String, int>{};
  for (final a in attempts) {
    final d = (a['date'] as String? ?? '');
    final day = d.length >= 10 ? d.substring(0, 10) : d;
    if (day.isEmpty) continue;
    per[day] = (per[day] ?? 0) + ((a['total'] as num?)?.toInt() ?? 0);
  }
  BestDay? bd;
  for (final e in per.entries) {
    if (bd == null || e.value > bd.total) {
      bd = BestDay(date: e.key, total: e.value);
    }
  }
  return bd;
}

/// Best mock result for one exam — vanilla `personalBest`
/// (highest pct; ties keep the earliest attempt).
class MockBest {
  final String examId;
  final int pct;
  final num score;
  final num max;
  final String date; // yyyy-MM-dd (UTC)
  const MockBest({
    required this.examId,
    required this.pct,
    required this.score,
    required this.max,
    required this.date,
  });
}

List<MockBest> bestMocksPerExam(List<Map<String, dynamic>> attempts) {
  final byExam = <String, List<Map<String, dynamic>>>{};
  for (final a in attempts) {
    if (a['mode'] != 'mock') continue;
    final examId =
        (a['exam'] as String? ?? '').isEmpty ? '' : a['exam'] as String;
    byExam.putIfAbsent(examId, () => []).add(a);
  }
  final out = <MockBest>[];
  for (final e in byExam.entries) {
    var best = e.value.first;
    for (final a in e.value) {
      if (((a['pct'] as num?)?.toInt() ?? 0) >
          ((best['pct'] as num?)?.toInt() ?? 0)) {
        best = a;
      }
    }
    out.add(
      MockBest(
        examId: e.key,
        pct: (best['pct'] as num?)?.toInt() ?? 0,
        score: best['score'] as num? ?? 0,
        max: best['max'] as num? ?? 0,
        date: ((best['date'] as String? ?? '').length >= 10
            ? (best['date'] as String).substring(0, 10)
            : ''),
      ),
    );
  }
  return out;
}

/// Longest run of consecutive calendar days with at least one attempt,
/// also counting the live streak (vanilla `longestStreak`).
int longestStreak(
  List<Map<String, dynamic>> attempts, [
  int currentStreak = 0,
]) {
  final days = <String>{};
  for (final a in attempts) {
    final d = (a['date'] as String? ?? '');
    if (d.length >= 10) days.add(d.substring(0, 10));
  }
  final sorted = days.toList()..sort();
  var best = 0, run = 0;
  String? prev;
  for (final d in sorted) {
    final cur = DateTime.parse('${d}T00:00:00Z');
    final isNextDay = prev != null &&
        cur.difference(DateTime.parse('${prev}T00:00:00Z')) ==
            const Duration(days: 1);
    run = isNextDay ? run + 1 : 1;
    prev = d;
    if (run > best) best = run;
  }
  return best > currentStreak ? best : currentStreak;
}

/// Everything the Personal Records card needs — vanilla `personalRecords`.
/// [speedBest] is read by the caller from the separate vanilla key
/// `loksewa_speed_best_v1` (it is not part of the progress object).
class PersonalRecords {
  final int longestStreakDays;
  final int totalXp;
  final int totalQuestions;
  final int totalAttempts;
  final BestDay? bestDay;
  final List<MockBest> bestMocks;
  final Map<String, dynamic>? speedBest;

  const PersonalRecords({
    required this.longestStreakDays,
    required this.totalXp,
    required this.totalQuestions,
    required this.totalAttempts,
    required this.bestDay,
    required this.bestMocks,
    this.speedBest,
  });
}

PersonalRecords personalRecords(
  List<Map<String, dynamic>> attempts, {
  required int xp,
  int currentStreak = 0,
  Map<String, dynamic>? speedBest,
}) {
  return PersonalRecords(
    longestStreakDays: longestStreak(attempts, currentStreak),
    totalXp: xp,
    totalQuestions: attempts.fold(
      0,
      (s, a) => s + ((a['total'] as num?)?.toInt() ?? 0),
    ),
    totalAttempts: attempts.length,
    bestDay: bestDay(attempts),
    bestMocks: bestMocksPerExam(attempts),
    speedBest: speedBest,
  );
}

/// Dashboard stat row — vanilla `renderDashboard` stats:
/// avg = mean of per-attempt pct (one decimal, '—' when empty),
/// passes = attempts with passed=true.
class AttemptStats {
  final int totalQuestions;
  final int totalAttempts;
  final String avgPct; // e.g. '73.5' or '—'
  final int passes;
  const AttemptStats({
    required this.totalQuestions,
    required this.totalAttempts,
    required this.avgPct,
    required this.passes,
  });
}

AttemptStats attemptStats(List<Map<String, dynamic>> attempts) {
  final totalQ = attempts.fold(
    0,
    (s, a) => s + ((a['total'] as num?)?.toInt() ?? 0),
  );
  final passes = attempts.where((a) => a['passed'] == true).length;
  final avg = attempts.isEmpty
      ? '—'
      : (attempts.fold<double>(
                0,
                (s, a) => s + ((a['pct'] as num?)?.toDouble() ?? 0),
              ) /
              attempts.length)
          .toStringAsFixed(1);
  return AttemptStats(
    totalQuestions: totalQ,
    totalAttempts: attempts.length,
    avgPct: avg,
    passes: passes,
  );
}
