import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/utils/bs_calendar.dart';

/// Anchor: 2026-10-31 AD == 2083-07-14 BS.
/// nowUtcDay for 2026-10-31 = 20757 (days since epoch, UTC).
const _anchorDay = 20757;

void main() {
  group('bsParse', () {
    test('parses valid dates', () {
      expect(bsParse('2083-07-14'), [2083, 7, 14]);
    });
    test('rejects malformed input', () {
      expect(bsParse(''), isNull);
      expect(bsParse('2083-7-14'), isNull);
      expect(bsParse('not-a-date'), isNull);
      expect(bsParse('2083-13-40'), [
        2083,
        13,
        40,
      ]); // parse ok, range checked later
    });
  });

  group('bsAbsDay', () {
    test('anchor is day 200 of 2083', () {
      expect(bsAbsDay('2083-07-14'), 200);
    });
    test('first day of year is 0', () {
      expect(bsAbsDay('2083-01-01'), 0);
    });
    test('rejects out-of-range day', () {
      // Kartik (month 7) 2083 has 30 days
      expect(bsAbsDay('2083-07-31'), isNull);
      expect(bsAbsDay('2083-07-30'), isNotNull);
    });
    test('rejects unknown year', () {
      expect(bsAbsDay('2082-01-01'), isNull);
    });
    test('corrected month lengths (2026-11-09)', () {
      // Mangsir 2083 = 29d, Poush 2083 = 30d (old tables had them swapped).
      expect(bsAbsDay('2083-08-29'), isNotNull);
      expect(bsAbsDay('2083-08-30'), isNull);
      expect(bsAbsDay('2083-09-30'), isNotNull);
      expect(bsAbsDay('2083-09-01'), 246);
      // Magh 2084 = 29d, Falgun 2084 = 30d (old tables had them swapped).
      expect(bsAbsDay('2084-10-29'), isNotNull);
      expect(bsAbsDay('2084-10-30'), isNull);
      expect(bsAbsDay('2084-11-30'), isNotNull);
      expect(bsAbsDay('2084-11-11'), 680); // Maha Shivaratri 2028
      // No 2085 table yet: Bisket Jatra 2028 ends 2085-01-05.
      expect(bsAbsDay('2085-01-05'), isNull);
    });
  });

  group('bsFromAbs round-trip', () {
    test('round-trips across month boundaries', () {
      for (final s in [
        '2083-01-01',
        '2083-07-14',
        '2083-12-30',
        '2084-01-15',
      ]) {
        expect(bsFromAbs(bsAbsDay(s)!), s);
      }
    });
  });

  group('bsToday', () {
    test('anchor day maps to 2083-07-14', () {
      expect(bsToday(nowUtcDay: _anchorDay), '2083-07-14');
    });
    test('next AD day maps to 2083-07-15', () {
      expect(bsToday(nowUtcDay: _anchorDay + 1), '2083-07-15');
    });
  });

  group('bsDaysUntil', () {
    test('exam tomorrow is 1', () {
      expect(bsDaysUntil('2083-07-15', nowUtcDay: _anchorDay), 1);
    });
    test('exam today is 0', () {
      expect(bsDaysUntil('2083-07-14', nowUtcDay: _anchorDay), 0);
    });
    test('past exam is negative', () {
      expect(bsDaysUntil('2083-07-10', nowUtcDay: _anchorDay), -4);
    });
    test('bad input is null', () {
      expect(bsDaysUntil('garbage', nowUtcDay: _anchorDay), isNull);
    });
  });

  group('fmtBs', () {
    test('english format', () {
      expect(fmtBs('2083-07-14', ne: false), '14 Kartik 2083');
    });
    test('nepali format', () {
      expect(fmtBs('2083-07-14', ne: true), '१४ कात्तिक २०८३');
    });
    test('bad input passes through', () {
      expect(fmtBs('nope', ne: false), 'nope');
    });
  });

  group('bsCountdownLabel', () {
    test('today/tomorrow/in-N-days', () {
      expect(bsCountdownLabel(0, ne: false), 'Today');
      expect(bsCountdownLabel(0, ne: true), 'आज');
      expect(bsCountdownLabel(1, ne: false), 'Tomorrow');
      expect(bsCountdownLabel(5, ne: false), 'in 5 days');
      expect(bsCountdownLabel(5, ne: true), '5 दिनमा');
    });
  });
}
