import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/models/models.dart';
import 'package:loksewa_vidyapeeth/utils/countdown.dart';

ExamDate _d(String id, String dateBs) => ExamDate(
      id: id,
      exam: 'kharidar',
      kind: 'exam',
      dateBs: dateBs,
      titleEn: id,
      titleNe: id,
      source: 'https://example.com',
      confidence: 'high',
    );

/// nowUtcMs for 2026-10-31T00:00:00Z == anchor day start.
const _anchorMs = 20757 * 86400000;

void main() {
  group('nxTargetMs', () {
    test('exam tomorrow targets start of that day', () {
      final t = nxTargetMs('2083-07-15', nowUtcMs: _anchorMs);
      expect(t, _anchorMs + 86400000);
    });
    test('bad date returns null', () {
      expect(nxTargetMs('garbage', nowUtcMs: _anchorMs), isNull);
    });
  });

  group('nxRemaining', () {
    test('clamps negative to zero (never negative digits)', () {
      final r = nxRemaining(_anchorMs - 1000, nowUtcMs: _anchorMs);
      expect(r, Duration.zero);
    });
    test('null target is zero', () {
      expect(nxRemaining(null, nowUtcMs: _anchorMs), Duration.zero);
    });
    test('future target returns positive duration', () {
      final r = nxRemaining(_anchorMs + 90000, nowUtcMs: _anchorMs);
      expect(r.inSeconds, 90);
    });
  });

  group('nxPagerList', () {
    final dates = [
      _d('a', '2083-07-14'), // today
      _d('b', '2083-08-14'), // ~30d
      _d('c', '2083-07-10'), // past -> excluded
      _d('d', '2084-05-01'), // far -> excluded
      _d('e', '2083-07-20'), // 6d
    ];
    test('soonest first, past and far excluded', () {
      final list = nxPagerList(dates, nowUtcDay: 20757);
      expect(list.map((e) => e.id).toList(), ['a', 'e', 'b']);
    });
  });

  group('nxCardState', () {
    test('today/near/far/none', () {
      expect(nxCardState(0), CountdownState.today);
      expect(nxCardState(7), CountdownState.near);
      expect(nxCardState(30), CountdownState.near);
      expect(nxCardState(31), CountdownState.far);
      expect(nxCardState(null), CountdownState.none);
    });
  });

  group('nxPickNearest', () {
    test('picks soonest future exam', () {
      final dates = [_d('x', '2083-08-01'), _d('y', '2083-07-20')];
      expect(nxPickNearest(dates, nowUtcDay: 20757)!.id, 'y');
    });
    test('all past returns null', () {
      expect(nxPickNearest([_d('x', '2083-01-01')], nowUtcDay: 20757), isNull);
    });
  });

  group('splitDuration', () {
    test('splits DD:HH:MM:SS', () {
      final p = splitDuration(
        const Duration(days: 2, hours: 3, minutes: 4, seconds: 5),
      );
      expect((p.dd, p.hh, p.mm, p.ss), ('02', '03', '04', '05'));
    });
  });
}
