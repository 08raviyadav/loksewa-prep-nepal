/// Dashboard tests: pure analytics (weak topics, records, weekly Monday-UTC
/// boundary, daily seed derivation) + badge derivation from synthetic
/// progress via the real ProgressStore.
library;

import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:loksewa_vidyapeeth/gamification/analytics.dart';
import 'package:loksewa_vidyapeeth/state/progress_store.dart';

Map<String, dynamic> _attempt({
  required String date,
  required int total,
  required int pct,
  bool passed = false,
  String mode = 'practice',
  String exam = '',
  int correct = 0,
  int wrong = 0,
  int skipped = 0,
  List<Map<String, dynamic>>? qdetail,
}) =>
    {
      'date': date,
      'mode': mode,
      'exam': exam,
      'total': total,
      'score': 0,
      'max': total,
      'pct': pct,
      'correct': correct,
      'wrong': wrong,
      'skipped': skipped,
      'passed': passed,
      if (qdetail != null) 'qdetail': qdetail,
    };

Map<String, dynamic> _qd(String topic, int code) => {
      't': topic,
      'c': code,
      'm': 1,
    };

void main() {
  group('daily seed derivation (vanilla dailyChallenge)', () {
    test('dailySeed is the UTC yyyy-MM-dd string', () {
      expect(dailySeed(DateTime.utc(2026, 10, 31, 23, 59)), '2026-10-31');
      // 2026-11-01 04:44 +0545 (NPT) is still 2026-10-31 in UTC.
      expect(
        dailySeed(DateTime.parse('2026-11-01T04:44:00+05:45')),
        '2026-10-31',
      );
    });

    test('seedHash matches the vanilla h*31+charCode derivation', () {
      // Precomputed with the vanilla formula: h=(h*31+code)>>>0 per char.
      expect(seedHash('2026-10-31'), 1162559553);
    });

    test('SeededRandom is deterministic and vanilla-compatible', () {
      final a = SeededRandom('2026-10-31');
      final b = SeededRandom('2026-10-31');
      // First two outputs of the vanilla LCG (h*1664525+1013904223)>>>0 / 2^32.
      expect(a.next(), closeTo(0.01251391600817442, 1e-12));
      expect(a.next(), closeTo(0.9621114793699235, 1e-12));
      expect(b.next(), closeTo(0.01251391600817442, 1e-12));
      final c = SeededRandom('2026-11-01');
      expect(c.next(), isNot(closeTo(0.01251391600817442, 1e-12)));
      // Range sanity over a long run.
      final r = SeededRandom('2026-10-31');
      for (var i = 0; i < 1000; i++) {
        final v = r.next();
        expect(v, greaterThanOrEqualTo(0));
        expect(v, lessThan(1));
      }
    });
  });

  group('weakTopics (qdetail accuracy)', () {
    test('orders by accuracy ascending, skips excluded', () {
      final attempts = [
        _attempt(
          date: '2026-10-30T10:00:00Z',
          total: 10,
          pct: 50,
          qdetail: [
            _qd('Constitution', 1),
            _qd('Constitution', 0),
            _qd('Economy', 1),
            _qd('Economy', 1),
            _qd('Economy', 1),
            _qd('History', -1), // skipped: not evidence
            _qd('History', 0),
          ],
        ),
      ];
      final weak = weakTopics(attempts);
      expect(weak.map((w) => w.topic).toList(), [
        'History',
        'Constitution',
        'Economy',
      ]);
      expect(weak.first.accuracy, 0.0);
      expect(weak.first.total, 1); // the skip did not count
      expect(weak.last.accuracy, 1.0);
    });

    test('topN caps the list and minAnswered filters thin topics', () {
      final attempts = [
        _attempt(
          date: '2026-10-30T10:00:00Z',
          total: 6,
          pct: 50,
          qdetail: [
            _qd('A', 0),
            _qd('B', 1),
            _qd('B', 0),
            _qd('C', 0),
            _qd('C', 1),
            _qd('C', 1),
            _qd('D', 1),
          ],
        ),
      ];
      expect(weakTopics(attempts, topN: 2).map((w) => w.topic).toList(), [
        'A',
        'B',
      ]);
      // 'A' (1 answered) and 'D' (1 answered) drop out at minAnswered: 2.
      expect(
        weakTopics(attempts, minAnswered: 2).map((w) => w.topic).toList(),
        ['B', 'C'],
      );
    });

    test('attempts without qdetail are ignored gracefully', () {
      final attempts = [
        _attempt(date: '2026-10-30T10:00:00Z', total: 5, pct: 80),
      ];
      expect(weakTopics(attempts), isEmpty);
    });
  });

  group('weeklyProgress (Monday-UTC boundary)', () {
    // Week of 2026-10-26 (Mon) .. 2026-11-01 (Sun).
    test('Sunday attempt counts, next Monday does not', () {
      final sunday = _attempt(date: '2026-11-01T23:59:00Z', total: 20, pct: 70);
      final monday = _attempt(date: '2026-11-02T00:01:00Z', total: 20, pct: 70);
      final w = weeklyProgress(
        [sunday],
        70,
        now: DateTime.utc(2026, 10, 28, 12),
      );
      expect(w.done, 20);
      expect(w.pct, 29); // 20/70*100 = 28.57 -> 29
      expect(w.met, isFalse);
      expect(w.weekStart, '2026-10-26');

      final w2 = weeklyProgress(
        [monday],
        70,
        now: DateTime.utc(2026, 11, 2, 12),
      );
      expect(w2.done, 20);
      expect(w2.weekStart, '2026-11-02');

      // The Sunday attempt belongs to the old week from the new week's view.
      final w3 = weeklyProgress(
        [sunday],
        70,
        now: DateTime.utc(2026, 11, 2, 12),
      );
      expect(w3.done, 0);
    });

    test('pct caps at 100 and met flips at target', () {
      final attempts = List.generate(
        5,
        (i) => _attempt(date: '2026-10-27T10:0$i:00Z', total: 20, pct: 80),
      );
      final w = weeklyProgress(
        attempts,
        70,
        now: DateTime.utc(2026, 10, 28, 12),
      );
      expect(w.done, 100);
      expect(w.pct, 100);
      expect(w.met, isTrue);
    });

    test('empty week is 0%', () {
      final w = weeklyProgress([], 70, now: DateTime.utc(2026, 10, 28, 12));
      expect(w.done, 0);
      expect(w.pct, 0);
      expect(w.met, isFalse);
    });
  });

  group('personalRecords', () {
    test('longestStreak counts consecutive days, breaks on gaps', () {
      final attempts = [
        _attempt(date: '2026-10-26T10:00:00Z', total: 10, pct: 60),
        _attempt(date: '2026-10-27T10:00:00Z', total: 10, pct: 60),
        _attempt(date: '2026-10-28T10:00:00Z', total: 10, pct: 60),
        // gap on the 29th
        _attempt(date: '2026-10-30T10:00:00Z', total: 10, pct: 60),
      ];
      expect(longestStreak(attempts), 3);
      // Live streak (e.g. a QOTD-only day) also counts — vanilla behaviour.
      expect(longestStreak(attempts, 5), 5);
      expect(longestStreak([]), 0);
    });

    test('bestDay picks the day with most questions', () {
      final attempts = [
        _attempt(date: '2026-10-26T10:00:00Z', total: 10, pct: 60),
        _attempt(date: '2026-10-27T10:00:00Z', total: 30, pct: 60),
        _attempt(date: '2026-10-27T18:00:00Z', total: 15, pct: 60),
      ];
      final bd = bestDay(attempts)!;
      expect(bd.date, '2026-10-27');
      expect(bd.total, 45);
      expect(bestDay([]), isNull);
    });

    test('bestMocksPerExam picks the highest pct per exam', () {
      final attempts = [
        _attempt(
          date: '2026-10-26T10:00:00Z',
          total: 100,
          pct: 55,
          mode: 'mock',
          exam: 'kharidar',
        ),
        _attempt(
          date: '2026-10-27T10:00:00Z',
          total: 100,
          pct: 78,
          mode: 'mock',
          exam: 'kharidar',
        ),
        _attempt(
          date: '2026-10-28T10:00:00Z',
          total: 100,
          pct: 90,
          mode: 'mock',
          exam: 'nasu',
        ),
        _attempt(
          date: '2026-10-29T10:00:00Z',
          total: 10,
          pct: 100,
          mode: 'practice',
          exam: 'kharidar',
        ),
      ];
      final bests = bestMocksPerExam(attempts);
      expect(bests.length, 2);
      final kh = bests.firstWhere((b) => b.examId == 'kharidar');
      expect(kh.pct, 78); // the practice 100% does not count as a mock
      final na = bests.firstWhere((b) => b.examId == 'nasu');
      expect(na.pct, 90);
    });

    test('attemptStats: average is the mean pct, passes counted', () {
      final attempts = [
        _attempt(date: '2026-10-26T10:00:00Z', total: 10, pct: 60),
        _attempt(
          date: '2026-10-27T10:00:00Z',
          total: 20,
          pct: 90,
          passed: true,
        ),
      ];
      final st = attemptStats(attempts);
      expect(st.totalQuestions, 30);
      expect(st.totalAttempts, 2);
      expect(st.avgPct, '75.0');
      expect(st.passes, 1);
      expect(attemptStats([]).avgPct, '—');
    });
  });

  group('badges() from synthetic progress', () {
    testWidgets('fresh progress earns nothing; activity earns badges', (
      tester,
    ) async {
      TestWidgetsFlutterBinding.ensureInitialized();

      Future<ProgressStore> loadWith(Map<String, dynamic> p) async {
        ProgressStore.resetForTest();
        SharedPreferences.setMockInitialValues({kProgressKey: json.encode(p)});
        return ProgressStore.instance;
      }

      final fresh = await loadWith({});
      expect(fresh.badges(), isEmpty);

      final active = await loadWith({
        'xp': 1500,
        'streak': 7,
        'weeklyGoalsMet': 1,
        'funFactsSeen': List.generate(10, (i) => 'f$i'),
        'attempts': [
          _attempt(
            date: '2026-10-27T10:00:00Z',
            total: 10,
            pct: 100,
            passed: true,
            mode: 'mock',
            exam: 'kharidar',
          ),
        ],
      });
      final badges = active.badges();
      expect(badges, contains('First Practice'));
      expect(badges, contains('7-Day Streak'));
      expect(badges, contains('3-Day Streak'));
      expect(badges, contains('1000 XP'));
      expect(badges, contains('First Pass'));
      expect(badges, contains('Perfect Mock'));
      expect(badges, contains('Weekly Champion'));
      expect(badges, contains('Fact Explorer'));
      expect(badges, isNot(contains('10 Sessions')));
      expect(badges, isNot(contains('30-Day Streak')));
      expect(badges, isNot(contains('5000 XP')));

      final century = await loadWith({
        'attempts': [
          _attempt(date: '2026-10-27T10:00:00Z', total: 100, pct: 70),
        ],
      });
      expect(century.badges(), contains('Century Day'));
    });
  });
}
