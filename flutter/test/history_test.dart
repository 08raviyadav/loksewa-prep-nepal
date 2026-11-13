// Historical events / Dates to Remember tests.
// Pure-logic tests run without widgets; widget tests pump the real
// screen and the Home "On This Day" card against the bundled assets
// (rootBundle works under flutter_test).
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:loksewa_vidyapeeth/data/data_repository.dart';
import 'package:loksewa_vidyapeeth/l10n/app_strings.dart';
import 'package:loksewa_vidyapeeth/l10n/history_strings.dart';
import 'package:loksewa_vidyapeeth/models/history.dart';
import 'package:loksewa_vidyapeeth/screens/history_screen.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';
import 'package:loksewa_vidyapeeth/widgets/history_otd_card.dart';
import 'package:loksewa_vidyapeeth/widgets/push_scope.dart';

HistoricalEvent _e(
  String id, {
  String? dayBs,
  int? yearBs,
  String? dateAd,
  String category = 'nepal-history',
  String titleEn = '',
  String titleNe = '',
  String summaryEn = '',
  String summaryNe = '',
  String confidence = 'high',
}) =>
    HistoricalEvent(
      id: id,
      titleEn: titleEn.isEmpty ? '$id en' : titleEn,
      titleNe: titleNe.isEmpty ? '$id ne' : titleNe,
      dayBs: dayBs,
      yearBs: yearBs,
      dateAd: dateAd,
      category: category,
      summaryEn: summaryEn,
      summaryNe: summaryNe,
      confidence: confidence,
      sources: const ['https://example.com/a', 'https://example.com/b'],
    );

void main() {
  group('HistoricalEvent loader (bundled data)', () {
    test('parses 95 entries with a valid schema', () async {
      final events = await DataRepository().historicalEvents();
      expect(events, hasLength(95));
      for (final e in events) {
        expect(e.id, isNotEmpty);
        expect(e.titleEn, isNotEmpty, reason: e.id);
        expect(e.titleNe, isNotEmpty, reason: e.id);
        expect(historyCategories, contains(e.category), reason: e.id);
        expect(['high', 'medium'], contains(e.confidence), reason: e.id);
        // Vanilla rule: every entry verified against >= 2 sources.
        expect(e.sources.length, greaterThanOrEqualTo(2), reason: e.id);
        if (e.dayBs != null) {
          expect(e.dayBs, matches(RegExp(r'^\d{2}-\d{2}$')), reason: e.id);
        }
        if (e.dateAd != null) {
          expect(
            e.dateAd,
            matches(RegExp(r'^\d{4}-\d{2}-\d{2}$')),
            reason: e.id,
          );
        }
      }
    });

    test('category + shape counts match the web data', () async {
      final events = await DataRepository().historicalEvents();
      int cat(String c) => events.where((e) => e.category == c).length;
      expect(cat('nepal-history'), 35);
      expect(cat('world-history'), 14);
      expect(cat('nepal-institutions'), 17);
      expect(cat('constitution'), 13);
      expect(cat('international'), 16);
      // 19 entries carry a BS month/day and can recur; 76 do not.
      expect(events.where((e) => e.dayBs != null), hasLength(19));
      expect(events.where((e) => e.dayBs == null), hasLength(76));
      // 8 entries are dateless (year lives only in the text).
      expect(events.where((e) => !e.hasDate), hasLength(8));
      expect(events.where((e) => e.needsReverify), hasLength(41));
    });
  });

  group('historyDateLabel', () {
    test('day + year -> full BS date', () {
      final e = _e('x', dayBs: '09-06', yearBs: 1980);
      expect(historyDateLabel(e, ne: false), '6 Poush 1980');
      expect(historyDateLabel(e, ne: true), '६ पुस १९८०');
    });

    test('day only -> BS month/day', () {
      final e = _e('x', dayBs: '03-11');
      expect(historyDateLabel(e, ne: false), '11 Ashadh');
      expect(historyDateLabel(e, ne: true), '११ असार');
    });

    test('year + AD date -> both halves shown', () {
      final e = _e('x', yearBs: 1872, dateAd: '1816-03-04');
      expect(historyDateLabel(e, ne: false), '1872 BS · 4 March 1816');
      expect(historyDateLabel(e, ne: true), '१८७२ BS · ४ मार्च १८१६');
    });

    test('year only -> BS year', () {
      final e = _e('x', yearBs: 1779);
      expect(historyDateLabel(e, ne: false), '1779');
      expect(historyDateLabel(e, ne: true), '१७७९');
    });

    test('AD only -> AD date', () {
      final e = _e('x', dateAd: '1995-01-01');
      expect(historyDateLabel(e, ne: false), '1 January 1995');
      expect(historyDateLabel(e, ne: true), '१ जनवरी १९९५');
    });

    test('dateless -> empty string, never "null"', () {
      final e = _e('x');
      expect(historyDateLabel(e, ne: false), '');
      expect(historyDateLabel(e, ne: true), '');
    });

    test('malformed dates degrade to empty, never "null"', () {
      expect(historyAdLabel('not-a-date', ne: false), '');
      expect(historyAdLabel('2020-13-01', ne: false), '');
      expect(historyAdLabel(null, ne: false), '');
      expect(historyDateLabel(_e('x', dayBs: '13-99'), ne: false), '');
    });

    test('no entry in the bundled data ever renders "null"', () async {
      final events = await DataRepository().historicalEvents();
      for (final e in events) {
        for (final ne in [false, true]) {
          final label = historyDateLabel(e, ne: ne);
          expect(label.contains('null'), isFalse, reason: e.id);
          expect(label.contains('Null'), isFalse, reason: e.id);
        }
      }
    });
  });

  group('historySorted', () {
    test('day entries first by MM-DD, then year, then AD, dateless last', () {
      final input = [
        _e('dateless'),
        _e('ad', dateAd: '1995-01-01'),
        _e('day-b', dayBs: '03-01', yearBs: 2000),
        _e('year', yearBs: 1779),
        _e('day-a', dayBs: '01-12', yearBs: 2072),
      ];
      final out = historySorted(input);
      expect(out.map((e) => e.id), [
        'day-a',
        'day-b',
        'year',
        'ad',
        'dateless',
      ]);
      // Input not mutated in place.
      expect(input.first.id, 'dateless');
    });

    test(
      'bundled data starts with the Gorkha earthquake (Baisakh 12)',
      () async {
        final events = await DataRepository().historicalEvents();
        final sorted = historySorted(events);
        expect(sorted.first.id, 'gorkha-earthquake-2015');
        expect(sorted.first.dayBs, '01-12');
        // All 8 dateless entries sort last.
        expect(sorted.sublist(87).every((e) => !e.hasDate), isTrue);
      },
    );
  });

  group('historyEventsToday / historyDayValidInYear', () {
    test('matches by BS month/day, any year', () async {
      final events = await DataRepository().historicalEvents();
      final today = historyEventsToday(events, '2083-01-12');
      expect(today.map((e) => e.id), ['gorkha-earthquake-2015']);
      // Same month/day in a different year still matches (recurring).
      expect(historyEventsToday(events, '2084-01-12').map((e) => e.id), [
        'gorkha-earthquake-2015',
      ]);
    });

    test('a quiet day matches nothing', () async {
      final events = await DataRepository().historicalEvents();
      // No entry carries day_bs 07-26.
      expect(historyEventsToday(events, '2083-07-26'), isEmpty);
      expect(historyEventsToday(events, '2084-07-26'), isEmpty);
    });

    test('null day_bs never matches; bad today never matches', () {
      final dateless = _e('x', yearBs: 1779);
      expect(historyMatchesToday(dateless, '2083-01-12'), isFalse);
      final dated = _e('y', dayBs: '01-12', yearBs: 2072);
      expect(historyMatchesToday(dated, null), isFalse);
      expect(historyMatchesToday(dated, 'garbage'), isFalse);
      expect(historyMatchesToday(dated, '2083-01-13'), isFalse);
    });

    test('year-boundary: a day that does not exist never matches', () {
      // Mangsir 2083 has 29 days (corrected table); 2084 has 30.
      expect(historyDayValidInYear('08-30', 2083), isFalse);
      expect(historyDayValidInYear('08-30', 2084), isTrue);
      expect(historyDayValidInYear('08-29', 2083), isTrue);
      // Chaitra 2083 has 30 days; day 32 never exists.
      expect(historyDayValidInYear('12-32', 2083), isFalse);
      expect(historyDayValidInYear('12-32', 2084), isFalse);
      // Baisakh 31 exists in both years.
      expect(historyDayValidInYear('01-31', 2083), isTrue);
      expect(historyDayValidInYear('01-31', 2084), isTrue);
      // Malformed / null day_bs is never valid.
      expect(historyDayValidInYear(null, 2083), isFalse);
      expect(historyDayValidInYear('13-01', 2083), isFalse);
      expect(historyDayValidInYear('00-10', 2083), isFalse);
      // Years outside the corrected table fall back to the 1-32 bound.
      expect(historyDayValidInYear('08-30', 2090), isTrue);
      expect(historyDayValidInYear('08-33', 2090), isFalse);
    });

    test('Mangsir-30 entry recurs in 2084 but never in 2083', () {
      final e = _e('mangsir-30', dayBs: '08-30', yearBs: 2000);
      expect(historyMatchesToday(e, '2084-08-30'), isTrue);
      // 2083-08-30 is not a real day (Mangsir 2083 = 29d) — even
      // if the string is fed in, the matcher refuses it.
      expect(historyMatchesToday(e, '2083-08-30'), isFalse);
      expect(historyMatchesToday(e, '2083-08-29'), isFalse);
    });
  });

  group('historyQuizPool', () {
    test('only dated entries; the 8 dateless ones are excluded', () async {
      final events = await DataRepository().historicalEvents();
      final pool = historyQuizPool(events);
      expect(pool, hasLength(87));
      expect(pool.every((e) => e.hasDate), isTrue);
      expect(
        pool.map((e) => e.id),
        isNot(contains('gorkha-kingdom-founded-1559')),
      );
    });
  });

  group('historyMatches / historyFiltered', () {
    test('EN + NE search across titles and summaries', () async {
      final events = await DataRepository().historicalEvents();
      final everest = events.where((e) => historyMatches(e, 'everest'));
      expect(everest, hasLength(2));
      final constitution = events.where((e) => historyMatches(e, 'संविधान'));
      expect(constitution, isNotEmpty);
      expect(historyMatches(events.first, ''), isTrue);
      expect(historyMatches(events.first, '   '), isTrue);
    });

    test('category filter + search combine', () async {
      final events = await DataRepository().historicalEvents();
      final filtered = historyFiltered(
        events,
        category: 'constitution',
        query: '',
      );
      expect(filtered, hasLength(13));
      expect(filtered.every((e) => e.category == 'constitution'), isTrue);
      final none = historyFiltered(
        events,
        category: 'constitution',
        query: 'zzz-nope',
      );
      expect(none, isEmpty);
    });
  });

  group('history strings (EN/NE)', () {
    test('key copy bilingual', () {
      const en = AppStrings(AppLang.en);
      const ne = AppStrings(AppLang.ne);
      expect(en.historyTitle, 'Dates to Remember');
      expect(ne.historyTitle, 'इतिहासका मिति');
      expect(en.historyQuizMe, '🎴 Quiz me');
      expect(ne.historyQuizMe, '🎴 मलाई प्रश्न गर्नुहोस्');
      expect(en.historyYearInSummary, 'Year in the summary below');
      expect(ne.historyYearInSummary, 'वर्ष तलको सारांशमा छ');
      expect(en.historyCategory('constitution'), 'Constitution');
      expect(ne.historyCategory('constitution'), 'संविधान');
      expect(en.historyCategory('nepal-institutions'), 'Nepal Institutions');
      expect(ne.historyCategory('nepal-institutions'), 'नेपालका संस्थाहरू');
      expect(en.historyCategory('weird'), 'weird');
      expect(en.historyShownCount(1), '1 date');
      expect(en.historyShownCount(13), '13 dates');
      expect(ne.historyShownCount(13), '13 मिति');
    });
  });

  group('widget: HistoryScreen', () {
    /// Pumps the screen and waits until the FutureBuilder's data loads.
    /// Same pre-warm trick as exam_dates_test: asset loads via
    /// rootBundle don't flush under the test's fake-async clock.
    Future<AppState> pumpScreen(WidgetTester tester) async {
      SharedPreferences.setMockInitialValues({'loksewa_lang_v1': 'en'}); // English pinned (default is Nepali, v1.0.9)
      final state = AppState();
      await state.init();
      await tester.runAsync(() async {
        await DataRepository().historicalEvents();
      });
      await tester.pumpWidget(
        AnimatedBuilder(
          animation: state,
          builder: (context, _) => MaterialApp(
            home: AppStateScope(
              state: state,
              child: Builder(
                builder: (context) => HistoryScreen(navIndex: 0, onNav: (_) {}),
              ),
            ),
          ),
        ),
      );
      for (var i = 0; i < 20; i++) {
        await tester.pump(const Duration(milliseconds: 50));
        if (find.byType(CircularProgressIndicator).evaluate().isEmpty) break;
      }
      expect(find.byType(CircularProgressIndicator), findsNothing);
      return state;
    }

    testWidgets('renders header, first row, search + category chips', (
      tester,
    ) async {
      await pumpScreen(tester);
      expect(find.text('Dates to Remember'), findsOneWidget);
      expect(
        find.text('95 dates · verified against at least 2 sources each'),
        findsOneWidget,
      );
      // First sorted row: Gorkha earthquake, Baisakh 12, 2072.
      expect(find.textContaining('Gorkha earthquake of 2015'), findsOneWidget);
      expect(find.textContaining('12 Baisakh 2072'), findsOneWidget);
      expect(find.text('95 dates'), findsOneWidget);
      expect(find.text('All categories'), findsOneWidget);
      expect(find.text('Constitution (13)'), findsOneWidget);
      expect(find.text('Nepal History (35)'), findsOneWidget);
      expect(find.text('🎴 Quiz me'), findsOneWidget);
    });

    testWidgets('tapping a row expands the bilingual summary + sources', (
      tester,
    ) async {
      await pumpScreen(tester);
      expect(find.textContaining('magnitude 7.8 earthquake'), findsNothing);
      await tester.tap(find.textContaining('Gorkha earthquake of 2015'));
      await tester.pumpAndSettle();
      expect(find.textContaining('magnitude 7.8 earthquake'), findsOneWidget);
      expect(find.text('Sources:'), findsOneWidget);
    });

    testWidgets('dateless rows show the year note, never "null"', (
      tester,
    ) async {
      await pumpScreen(tester);
      // Gorkha Kingdom entry is dateless and sorts last — search for it.
      await tester.enterText(find.byType(TextField), 'Gorkha Kingdom');
      await tester.pumpAndSettle();
      expect(find.textContaining('Gorkha Kingdom founded'), findsOneWidget);
      expect(find.textContaining('Year in the summary below'), findsOneWidget);
      expect(find.textContaining('null'), findsNothing);
    });

    testWidgets('medium-confidence rows show the re-verify badge', (
      tester,
    ) async {
      await pumpScreen(tester);
      // High-confidence first row carries no badge…
      final highCard = find.ancestor(
        of: find.textContaining('Gorkha earthquake of 2015'),
        matching: find.byType(Card),
      );
      expect(
        find.descendant(of: highCard, matching: find.text('⚠️ re-verify')),
        findsNothing,
      );
      // …while a medium-confidence row does (scroll to it — small
      // steps: the list viewport is short and 400px jumps can skip
      // a lazily-built row entirely between checks).
      await tester.scrollUntilVisible(
        find.textContaining('Shreenath Battalion'),
        100,
        scrollable: find.descendant(
          of: find.byType(ListView),
          matching: find.byType(Scrollable),
        ),
      );
      await tester.pumpAndSettle();
      final medCard = find.ancestor(
        of: find.textContaining('Shreenath Battalion'),
        matching: find.byType(Card),
      );
      expect(
        find.descendant(of: medCard, matching: find.text('⚠️ re-verify')),
        findsOneWidget,
      );
    });

    testWidgets('search narrows the list', (tester) async {
      await pumpScreen(tester);
      await tester.enterText(find.byType(TextField), 'Everest');
      await tester.pumpAndSettle();
      expect(find.text('2 dates'), findsOneWidget);
      expect(
        find.textContaining('First ascent of Mount Everest'),
        findsOneWidget,
      );
      expect(find.textContaining('Gorkha earthquake of 2015'), findsNothing);
    });

    testWidgets('category filter narrows the list', (tester) async {
      await pumpScreen(tester);
      // The chip row scrolls horizontally; bring the chip into view
      // before tapping (it starts off the right edge).
      await tester.ensureVisible(find.text('Constitution (13)'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Constitution (13)'));
      await tester.pumpAndSettle();
      expect(find.text('13 dates'), findsOneWidget);
      expect(find.textContaining('Gorkha earthquake of 2015'), findsNothing);

      await tester.ensureVisible(find.text('All categories'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('All categories'));
      await tester.pumpAndSettle();
      expect(find.text('95 dates'), findsOneWidget);
    });

    testWidgets('empty search shows the no-match state', (tester) async {
      await pumpScreen(tester);
      await tester.enterText(find.byType(TextField), 'zzz-no-such-date');
      await tester.pumpAndSettle();
      expect(find.text('No dates match'), findsOneWidget);
      expect(find.text('Try a different search or category.'), findsOneWidget);
    });

    testWidgets('quiz mode: reveal, mark, running count, reset', (
      tester,
    ) async {
      await pumpScreen(tester);
      await tester.tap(find.text('🎴 Quiz me'));
      await tester.pumpAndSettle();
      expect(find.text('Question 1 / 87 · ✓ 0 · ✗ 0'), findsOneWidget);
      expect(find.text('When did this happen?'), findsOneWidget);
      expect(find.text('👁️ Reveal the date'), findsOneWidget);
      expect(find.text('✅ Got it'), findsNothing);

      // ensureVisible before each tap: the quiz card is taller than
      // the short test viewport, and the scroll offset persists
      // across questions, so buttons can sit above the fold.
      Future<void> tapVisible(String label) async {
        await tester.ensureVisible(find.text(label));
        await tester.pumpAndSettle();
        await tester.tap(find.text(label));
        await tester.pumpAndSettle();
      }

      await tapVisible('👁️ Reveal the date');
      expect(find.text('✅ Got it'), findsOneWidget);
      expect(find.text('❌ Missed it'), findsOneWidget);

      await tapVisible('✅ Got it');
      expect(find.text('Question 2 / 87 · ✓ 1 · ✗ 0'), findsOneWidget);

      await tapVisible('👁️ Reveal the date');
      await tapVisible('❌ Missed it');
      expect(find.text('Question 3 / 87 · ✓ 1 · ✗ 1'), findsOneWidget);

      await tapVisible('Reset quiz');
      expect(find.text('🎴 Quiz me'), findsOneWidget);
      expect(find.text('95 dates'), findsOneWidget);
    });
  });

  group('widget: HistoryOtdCard', () {
    Future<List<HistoricalEvent>> loadEvents(WidgetTester tester) async {
      var events = <HistoricalEvent>[];
      await tester.runAsync(() async {
        events = await DataRepository().historicalEvents();
      });
      return events;
    }

    Future<void> pumpCard(
      WidgetTester tester, {
      required List<HistoricalEvent> events,
      required String todayBs,
      ValueChanged<String>? onPush,
    }) async {
      SharedPreferences.setMockInitialValues({'loksewa_lang_v1': 'en'}); // English pinned (default is Nepali, v1.0.9)
      final state = AppState();
      await state.init();
      await tester.pumpWidget(
        AnimatedBuilder(
          animation: state,
          builder: (context, _) => MaterialApp(
            home: AppStateScope(
              state: state,
              child: PushScope(
                onPush: onPush ?? (_) {},
                child: Scaffold(
                  body: HistoryOtdCard(
                    events: events,
                    todayBsOverride: todayBs,
                  ),
                ),
              ),
            ),
          ),
        ),
      );
      await tester.pumpAndSettle();
    }

    testWidgets('shows today\'s events with a link to all dates', (
      tester,
    ) async {
      final events = await loadEvents(tester);
      String? pushed;
      await pumpCard(
        tester,
        events: events,
        todayBs: '2083-01-12',
        onPush: (r) => pushed = r,
      );
      expect(find.text('📜 On This Day'), findsOneWidget);
      expect(find.textContaining('Gorkha earthquake of 2015'), findsOneWidget);
      expect(find.textContaining('12 Baisakh 2083'), findsOneWidget);
      await tester.tap(find.text('All dates to remember →'));
      await tester.pumpAndSettle();
      expect(pushed, '/history');
    });

    testWidgets('renders nothing on a quiet day', (tester) async {
      final events = await loadEvents(tester);
      await pumpCard(tester, events: events, todayBs: '2083-07-26');
      expect(find.text('📜 On This Day'), findsNothing);
      expect(find.byType(Card), findsNothing);
    });
  });
}
