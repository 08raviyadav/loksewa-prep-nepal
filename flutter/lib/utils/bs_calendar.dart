/// Bikram Sambat calendar engine — a direct Dart port of the vanilla site's
/// BS module (assets/js/app.js §"BS calendar"), including its honesty
/// comments. Month lengths corrected 2026-11-09 (same fix as the web app):
/// 2083 Mangsir = 29d, Poush = 30d; 2084 Magh = 29d, Falgun = 30d.
/// Evidence: Poush 1, 2083 = 16 Dec 2026 (Govt of Nepal 2083 holiday list);
/// Maha Shivaratri = Falgun 11, 2084 = 23 Feb 2028. The previous tables had
/// those two pairs swapped by one day.
///
/// Anchor: 2026-10-31 AD == 2083-07-14 BS (Kartik 14, 2083).
library;

const _anchorAdDay = 20757; // days since epoch for 2026-10-31 (UTC)
const _anchorBsAbs = 200; // bsAbsDay('2083-07-14')

const Map<int, List<int>> _bsMonthLen = {
  2083: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
  2084: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
};

const List<String> bsMonthEn = [
  'Baisakh',
  'Jestha',
  'Ashadh',
  'Shrawan',
  'Bhadra',
  'Ashwin',
  'Kartik',
  'Mangsir',
  'Poush',
  'Magh',
  'Falgun',
  'Chaitra',
];
const List<String> bsMonthNe = [
  'बैशाख',
  'जेठ',
  'असार',
  'साउन',
  'भदौ',
  'असोज',
  'कात्तिक',
  'मंसिर',
  'पुस',
  'माघ',
  'फागुन',
  'चैत',
];

final _bsRe = RegExp(r'^(\d{4})-(\d{2})-(\d{2})$');

/// Parse "YYYY-MM-DD" -> [y, m, d], or null.
List<int>? bsParse(String s) {
  final m = _bsRe.firstMatch(s);
  if (m == null) return null;
  return [
    int.parse(m.group(1)!),
    int.parse(m.group(2)!),
    int.parse(m.group(3)!),
  ];
}

/// Days in BS [month] of [year], or null when the year is outside the
/// corrected table (2083–2084) or the month is out of range.
/// Used by the recurring-date matcher (see models/history.dart): a
/// day that doesn't exist in that year's month never matches.
int? bsMonthLength(int year, int month) {
  final lens = _bsMonthLen[year];
  if (lens == null || month < 1 || month > 12) return null;
  return lens[month - 1];
}

/// Absolute day count since 2083-01-01. Null on malformed/out-of-range input.
int? bsAbsDay(String s) {
  final p = bsParse(s);
  if (p == null) return null;
  final lens = _bsMonthLen[p[0]];
  if (lens == null) return null;
  if (p[1] < 1 || p[1] > 12 || p[2] < 1 || p[2] > lens[p[1] - 1]) return null;
  var n = 0;
  for (var y = 2083; y < p[0]; y++) {
    final l = _bsMonthLen[y];
    if (l == null) return null;
    n += l.reduce((a, b) => a + b);
  }
  for (var m = 1; m < p[1]; m++) {
    n += lens[m - 1];
  }
  return n + (p[2] - 1);
}

String? bsFromAbs(int n) {
  for (var y = 2083; y <= 2100; y++) {
    final lens = _bsMonthLen[y];
    if (lens == null) return null;
    final yl = lens.reduce((a, b) => a + b);
    if (n < yl) {
      var m = 1;
      while (n >= lens[m - 1]) {
        n -= lens[m - 1];
        m++;
      }
      final mm = m.toString().padLeft(2, '0');
      final dd = (n + 1).toString().padLeft(2, '0');
      return '$y-$mm-$dd';
    }
    n -= yl;
  }
  return null;
}

/// Today's BS date (YYYY-MM-DD), derived from the anchor + elapsed AD days.
/// `nowUtcDay` is injectable for tests (days since epoch, UTC).
String? bsToday({int? nowUtcDay}) {
  final today =
      nowUtcDay ?? DateTime.now().toUtc().millisecondsSinceEpoch ~/ 86400000;
  return bsFromAbs(_anchorBsAbs + (today - _anchorAdDay));
}

/// Days from today (BS) until [dateBs]. Negative = past. Null = bad input.
int? bsDaysUntil(String dateBs, {int? nowUtcDay}) {
  final a = bsAbsDay(dateBs);
  final t = bsToday(nowUtcDay: nowUtcDay);
  if (a == null || t == null) return null;
  final b = bsAbsDay(t);
  if (b == null) return null;
  return a - b;
}

String neDigits(String s) => s.replaceAllMapped(
      RegExp(r'\d'),
      (m) => '०१२३४५६७८९'[int.parse(m.group(0)!)],
    );

/// "14 Kartik 2083" / "१४ कात्तिक २०८३"
String fmtBs(String s, {required bool ne}) {
  final p = bsParse(s);
  if (p == null || p[1] < 1 || p[1] > 12) return s;
  if (ne) {
    return '${neDigits(p[2].toString())} ${bsMonthNe[p[1] - 1]} ${neDigits(p[0].toString())}';
  }
  return '${p[2]} ${bsMonthEn[p[1] - 1]} ${p[0]}';
}

/// Countdown label: 0 -> Today/आज, 1 -> Tomorrow/भोलि, else "in N days".
String bsCountdownLabel(int d, {required bool ne}) {
  if (d == 0) return ne ? 'आज' : 'Today';
  if (d == 1) return ne ? 'भोलि' : 'Tomorrow';
  return ne ? '$d दिनमा' : 'in $d days';
}
