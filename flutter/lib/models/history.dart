/// Historical event model + pure helpers — the Flutter port of the
/// vanilla site's "Historical events / Dates to Remember" section
/// (loksewa-prep-nepal/assets/js/app.js §"Historical events").
///
/// Data: assets/data/historical-events.json (95 verified entries).
/// Schema: {id, title_en, title_ne, day_bs ("MM-DD" | null),
/// year_bs (int | null), date_ad ("YYYY-MM-DD" | null), category,
/// summary_en, summary_ne, confidence ("high"|"medium"), sources[>=2]}.
/// day_bs is set ONLY when a source explicitly gave the BS month/day.
/// Entries with day_bs null do NOT recur in On This Day; dateless
/// entries (no day, year or AD date — the year lives only in the
/// title/summary text) are excluded from quiz mode too: there is no
/// date to reveal. Date labels never render "null".
///
/// One deliberate deviation from the web port: the web treats day_bs
/// validity as 1–32 (its BS table covers 2083/2084 only, so no exact
/// check is possible for most years). The Flutter matcher applies the
/// corrected month lengths for the year being matched: a day_bs day
/// that doesn't exist in that year's month never matches (e.g. a
/// Mangsir-30 entry never recurs in 2083, where Mangsir has 29 days,
/// but does recur in 2084). Years outside the table fall back to the
/// web's honest 1–32 bound.
library;

import '../utils/bs_calendar.dart';

/// Categories in the vanilla HISTORY_CATEGORIES order.
const historyCategories = [
  'nepal-history',
  'world-history',
  'nepal-institutions',
  'constitution',
  'international',
];

class HistoricalEvent {
  final String id;
  final String titleEn;
  final String titleNe;
  final String? dayBs; // "MM-DD" | null
  final int? yearBs;
  final String? dateAd; // "YYYY-MM-DD" | null
  final String category;
  final String summaryEn;
  final String summaryNe;
  final String confidence; // high | medium
  final List<String> sources;

  const HistoricalEvent({
    required this.id,
    required this.titleEn,
    required this.titleNe,
    required this.dayBs,
    required this.yearBs,
    required this.dateAd,
    required this.category,
    required this.summaryEn,
    required this.summaryNe,
    required this.confidence,
    required this.sources,
  });

  factory HistoricalEvent.fromJson(Map<String, dynamic> j) => HistoricalEvent(
        id: j['id'] as String? ?? '',
        titleEn: j['title_en'] as String? ?? '',
        titleNe: j['title_ne'] as String? ?? '',
        dayBs: j['day_bs'] as String?,
        yearBs: (j['year_bs'] as num?)?.toInt(),
        dateAd: j['date_ad'] as String?,
        category: j['category'] as String? ?? '',
        summaryEn: j['summary_en'] as String? ?? '',
        summaryNe: j['summary_ne'] as String? ?? '',
        confidence: j['confidence'] as String? ?? 'medium',
        sources: (j['sources'] as List<dynamic>? ?? const [])
            .map((e) => e.toString())
            .toList(),
      );

  String title(bool ne) => ne && titleNe.isNotEmpty ? titleNe : titleEn;
  String summary(bool ne) => ne && summaryNe.isNotEmpty ? summaryNe : summaryEn;

  /// True when the entry has any date to show/reveal (BS day, BS year
  /// or AD) — mirrors vanilla's historyHasDate().
  bool get hasDate => dayBs != null || yearBs != null || dateAd != null;

  bool get needsReverify => confidence == 'medium';
}

const List<String> _adMonthEn = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
];
const List<String> _adMonthNe = [
  'जनवरी',
  'फेब्रुअरी',
  'मार्च',
  'अप्रिल',
  'मे',
  'जुन',
  'जुलाइ',
  'अगस्ट',
  'सेप्टेम्बर',
  'अक्टोबर',
  'नोभेम्बर',
  'डिसेम्बर',
];

/// "4 March 1816" / "४ मार्च १८१६" — '' when the AD date is malformed.
/// Mirrors vanilla's historyAdLabel().
String historyAdLabel(String? s, {required bool ne}) {
  if (s == null) return '';
  final m = RegExp(r'^(\d{4})-(\d{2})-(\d{2})$').firstMatch(s);
  if (m == null) return '';
  final month = int.parse(m.group(2)!);
  if (month < 1 || month > 12) return '';
  final day = int.parse(m.group(3)!);
  if (ne) {
    return '${neDigits(day.toString())} ${_adMonthNe[month - 1]} '
        '${neDigits(m.group(1)!)}';
  }
  return '$day ${_adMonthEn[month - 1]} ${m.group(1)}';
}

/// Display date, never "null": full BS date when day+year are known,
/// BS month/day when the year is unknown, BS year alone, AD date
/// alone, BS year + AD date together, or '' when the year lives only
/// in the title/summary text. Mirrors vanilla's historyDateLabel().
String historyDateLabel(HistoricalEvent e, {required bool ne}) {
  final dayBs = e.dayBs;
  if (dayBs != null && e.yearBs != null) {
    return fmtBs('${e.yearBs}-$dayBs', ne: ne);
  }
  if (dayBs != null) {
    final parts = dayBs.split('-');
    if (parts.length != 2) return '';
    final m = int.tryParse(parts[0]);
    final d = int.tryParse(parts[1]);
    if (m == null || d == null || m < 1 || m > 12 || d < 1) return '';
    return ne
        ? '${neDigits(d.toString())} ${bsMonthNe[m - 1]}'
        : '$d ${bsMonthEn[m - 1]}';
  }
  // BS year + exact AD date: show both (e.g. Everest — 2010 BS ·
  // 29 May 1953). Either half alone would hide a date the student
  // is asked for.
  final ad = historyAdLabel(e.dateAd, ne: ne);
  final year = e.yearBs;
  if (year != null && ad.isNotEmpty) {
    return '${ne ? neDigits(year.toString()) : year} BS · $ad';
  }
  if (year != null) {
    return ne ? neDigits(year.toString()) : year.toString();
  }
  if (ad.isNotEmpty) return ad;
  return '';
}

/// True when [dayBs] ("MM-DD") is a real day in [year]'s BS calendar:
/// month 1–12, day within that month's corrected length when the year
/// is in the table, else the web's honest 1–32 bound. A day that
/// doesn't exist in that year's month (Mangsir 30 in 2083) is never
/// a matchable recurring date.
bool historyDayValidInYear(String? dayBs, int year) {
  if (dayBs == null) return false;
  final parts = dayBs.split('-');
  if (parts.length != 2) return false;
  final m = int.tryParse(parts[0]);
  final d = int.tryParse(parts[1]);
  if (m == null || d == null || m < 1 || m > 12 || d < 1) return false;
  final len = bsMonthLength(year, m);
  if (len != null) return d <= len;
  return d <= 32;
}

/// True when the entry's day_bs month/day matches [todayBs]
/// ("YYYY-MM-DD", any year) — the recurring set for On This Day.
/// Null day_bs never matches; a day that doesn't exist in today's
/// year/month never matches either. Null/malformed [todayBs] → false.
bool historyMatchesToday(HistoricalEvent e, String? todayBs) {
  final dayBs = e.dayBs;
  if (dayBs == null || todayBs == null) return false;
  final t = bsParse(todayBs);
  if (t == null) return false;
  if (!historyDayValidInYear(dayBs, t[0])) return false;
  final parts = dayBs.split('-');
  final m = int.parse(parts[0]);
  final d = int.parse(parts[1]);
  return m == t[1] && d == t[2];
}

/// Events whose day_bs month/day matches [todayBs] (any year).
/// Mirrors vanilla's historyEventsToday().
List<HistoricalEvent> historyEventsToday(
  List<HistoricalEvent> history,
  String? todayBs,
) {
  return history.where((e) => historyMatchesToday(e, todayBs)).toList();
}

/// Chronological by BS month/day first, then BS year, then AD date,
/// then dateless entries last (title tiebreak — deterministic, no
/// crash on nulls). Mirrors vanilla's historySorted().
List<HistoricalEvent> historySorted(List<HistoricalEvent> list) {
  int bucket(HistoricalEvent e) {
    if (e.dayBs != null) return 0;
    if (e.yearBs != null) return 1;
    if (e.dateAd != null) return 2;
    return 3;
  }

  String key(HistoricalEvent e) {
    if (e.dayBs != null) return e.dayBs!;
    if (e.yearBs != null) return e.yearBs.toString().padLeft(4, '0');
    if (e.dateAd != null) return e.dateAd!;
    return '';
  }

  final out = List<HistoricalEvent>.of(list);
  out.sort((a, b) {
    final ba = bucket(a);
    final bb = bucket(b);
    if (ba != bb) return ba - bb;
    final ka = key(a);
    final kb = key(b);
    if (ka != kb) return ka.compareTo(kb);
    return a.titleEn.compareTo(b.titleEn);
  });
  return out;
}

/// Quiz pool: only entries with a date to reveal (dateless entries
/// excluded). Mirrors vanilla's historyQuizPool().
List<HistoricalEvent> historyQuizPool(List<HistoricalEvent> history) =>
    history.where((e) => e.hasDate).toList();

/// EN/NE search across titles + summaries (case-insensitive).
/// Mirrors vanilla's historyMatches().
bool historyMatches(HistoricalEvent e, String query) {
  final q = query.trim().toLowerCase();
  if (q.isEmpty) return true;
  final haystack =
      '${e.titleEn} ${e.titleNe} ${e.summaryEn} ${e.summaryNe}'.toLowerCase();
  return haystack.contains(q);
}

/// Sorted list filtered by category ('' = all) and search query.
/// Mirrors vanilla's historyFiltered().
List<HistoricalEvent> historyFiltered(
  List<HistoricalEvent> history, {
  String category = '',
  String query = '',
}) {
  return historySorted(history)
      .where(
        (e) =>
            (category.isEmpty || e.category == category) &&
            historyMatches(e, query),
      )
      .toList();
}
