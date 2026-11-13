// Milestone 3 — Exam Dates screen tests.
// Pure-logic tests run without widgets; widget tests pump the real screen
// against the bundled assets (rootBundle works under flutter_test) and a
// mock SharedPreferences store for the loksewa_reminders_v1 toggles.
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:plugin_platform_interface/plugin_platform_interface.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher_platform_interface/url_launcher_platform_interface.dart';

import 'package:loksewa_vidyapeeth/data/data_repository.dart';
import 'package:loksewa_vidyapeeth/l10n/app_strings.dart';
import 'package:loksewa_vidyapeeth/l10n/examdates_strings.dart';
import 'package:loksewa_vidyapeeth/models/models.dart';
import 'package:loksewa_vidyapeeth/screens/exam_dates_screen.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/utils/bs_calendar.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';

ExamDate _d(
  String id,
  String dateBs, {
  String exam = 'mecee-bl',
  String kind = 'exam',
}) =>
    ExamDate(
      id: id,
      exam: exam,
      kind: kind,
      dateBs: dateBs,
      titleEn: '$id en',
      titleNe: '$id ne',
      source: 'https://example.com',
      confidence: 'high',
    );

/// Records every URL the app tries to open, instead of leaving the
/// test. Set [result] false to simulate a device that can't open links.
class _FakeUrlLauncher extends Fake
    with MockPlatformInterfaceMixin
    implements UrlLauncherPlatform {
  final launched = <String>[];
  bool result = true;

  @override
  Future<bool> launchUrl(String url, LaunchOptions options) async {
    launched.add(url);
    return result;
  }
}

void main() {
  group('examDateChipKind', () {
    test('buckets match vanilla remChip thresholds', () {
      expect(examDateChipKind(null), ExamDateChipKind.past);
      expect(examDateChipKind(-3), ExamDateChipKind.past);
      expect(examDateChipKind(0), ExamDateChipKind.today);
      expect(examDateChipKind(1), ExamDateChipKind.tomorrow);
      expect(examDateChipKind(2), ExamDateChipKind.soon);
      expect(examDateChipKind(7), ExamDateChipKind.soon);
      expect(examDateChipKind(8), ExamDateChipKind.later);
      expect(examDateChipKind(120), ExamDateChipKind.later);
    });
  });

  group('sortExamDates', () {
    test('sorts chronologically by BS date string', () {
      final inOrder = [
        _d('c', '2083-08-16'),
        _d('a', '2083-07-15'),
        _d('b', '2083-07-27'),
      ];
      final out = sortExamDates(inOrder);
      expect(out.map((e) => e.id), ['a', 'b', 'c']);
      // input not mutated in place
      expect(inOrder.first.id, 'c');
    });
  });

  group('filterExamDatesByKind', () {
    final dates = [
      _d('e1', '2083-07-15', kind: 'exam'),
      _d('d1', '2083-07-16', kind: 'deadline'),
      _d('d2', '2083-07-17', kind: 'deadline'),
    ];
    test('empty filter returns all', () {
      expect(filterExamDatesByKind(dates, ''), hasLength(3));
    });
    test('kind filter keeps only matches', () {
      expect(filterExamDatesByKind(dates, 'deadline').map((e) => e.id), [
        'd1',
        'd2',
      ]);
      expect(filterExamDatesByKind(dates, 'exam').map((e) => e.id), ['e1']);
    });
    test('unknown kind yields empty', () {
      expect(filterExamDatesByKind(dates, 'admit'), isEmpty);
    });
  });

  group('examDateKinds', () {
    test('distinct kinds in first-seen order', () {
      final dates = [
        _d('e1', '2083-07-15', kind: 'exam'),
        _d('d1', '2083-07-16', kind: 'deadline'),
        _d('e2', '2083-07-17', kind: 'exam'),
      ];
      expect(examDateKinds(dates), ['exam', 'deadline']);
    });
  });

  group('examForExamDate', () {
    final exams = [
      const Exam(id: 'mecee-bl', name: 'MECEE-BL', nameNe: 'MECEE-BL'),
    ];
    test('mapped exam resolves', () {
      expect(
        examForExamDate(_d('x', '2083-07-15', exam: 'mecee-bl'), exams)?.id,
        'mecee-bl',
      );
    });
    test('empty exam id (vanilla null) -> no links', () {
      expect(examForExamDate(_d('x', '2083-07-15', exam: ''), exams), isNull);
    });
    test('unknown exam id -> no links', () {
      expect(
        examForExamDate(_d('x', '2083-07-15', exam: 'nope'), exams),
        isNull,
      );
    });
  });

  group('chip strings (EN/NE)', () {
    test('bilingual chip copy', () {
      const en = AppStrings(AppLang.en);
      const ne = AppStrings(AppLang.ne);
      expect(en.chipToday, '🔴 Today');
      expect(ne.chipToday, '🔴 आज');
      expect(en.chipTomorrow, '🟡 Tomorrow');
      expect(ne.chipTomorrow, '🟡 भोलि');
      expect(en.chipSoon(3), '🟡 in 3 days');
      expect(ne.chipSoon(3), '🟡 3 दिनमा');
      expect(en.chipLater(21), '📅 in 21 days');
      expect(ne.chipLater(21), '📅 21 दिनमा');
      expect(en.chipDone, '✓ Done');
      expect(ne.chipDone, '✓ सकियो');
    });

    test('kind labels bilingual, unknown kinds pass through', () {
      const en = AppStrings(AppLang.en);
      const ne = AppStrings(AppLang.ne);
      expect(en.kindLabel('exam'), 'Exam');
      expect(ne.kindLabel('exam'), 'परीक्षा');
      expect(en.kindLabel('admit'), 'Admit card');
      expect(ne.kindLabel('admit'), 'प्रवेशपत्र');
      expect(en.kindLabel('deadline'), 'Deadline');
      expect(ne.kindLabel('deadline'), 'अन्तिम मिति');
      expect(en.kindLabel('weird'), 'weird');
    });

    test('remind toggle copy bilingual', () {
      const en = AppStrings(AppLang.en);
      const ne = AppStrings(AppLang.ne);
      expect(en.remindMeBtn, '🔕 Remind me');
      expect(ne.remindMeBtn, '🔕 सम्झाउनुहोस्');
      expect(en.remindingBtn, '🔔 Reminding');
      expect(ne.remindingBtn, '🔔 रिमाइन्डर छ');
    });
  });

  group('mapping coverage against bundled data', () {
    test(
      'entries without practice/mock links are exactly the unmapped ones',
      () async {
        final repo = DataRepository();
        final exams = await repo.exams();
        final dates = await repo.examDates();
        expect(dates, hasLength(82));
        final unmapped = dates
            .where((d) => examForExamDate(d, exams) == null)
            .map((d) => d.id)
            .toList();
        // Vanilla logic: exam null/absent -> no links. The three NMC
        // special-exam entries carry exam:null in exam-dates.json.
        expect(
          unmapped,
          containsAll([
            'nmc-special-exam-application-deadline',
            'nmc-special-exam-day1',
            'nmc-special-exam-day2',
          ]),
        );
        // The newer RBB / PSC Saha Sachiv / forensic / CTEVT / NID
        // entries carry exam ids with no matching Exam in exams.json
        // yet (no practice pack), so they render without links too —
        // the same vanilla behaviour as the NMC rows.
        expect(unmapped, hasLength(61));
        final mapped = 82 - unmapped.length;
        expect(mapped, 21);
      },
    );

    test('medium-confidence entries carry the re-verify badge', () async {
      final dates = await DataRepository().examDates();
      final medium =
          dates.where((d) => d.confidence == 'medium').map((d) => d.id);
      // The 62 dates synced 2026-11-09 are single-source (medium);
      // the original 20 carried 8 medium entries.
      expect(medium, hasLength(70));
    });
  });

  group('widget: ExamDatesScreen', () {
    /// Pumps the screen and waits until the FutureBuilder's data loads.
    /// The repository cache is pre-warmed with real async first: asset
    /// loads via rootBundle don't flush under the test's fake-async
    /// clock, so without this the loading spinner never goes away.
    /// A plain pumpAndSettle also never settles while that spinner
    /// (an infinite animation) is on screen.
    Future<AppState> pumpScreen(
      WidgetTester tester, {
      void Function(Exam)? onPractice,
      void Function(Exam)? onMock,
      void Function(int)? onNav,
    }) async {
      SharedPreferences.setMockInitialValues({'loksewa_lang_v1': 'en'}); // English pinned (default is Nepali, v1.0.9)
      final state = AppState();
      await state.init();
      await tester.runAsync(() async {
        await DataRepository().exams();
        await DataRepository().examDates();
      });
      await tester.pumpWidget(
        // AnimatedBuilder mirrors main.dart: it rebuilds the subtree on
        // AppState.notifyListeners so AppStateScope dependents update.
        AnimatedBuilder(
          animation: state,
          builder: (context, _) => MaterialApp(
            home: AppStateScope(
              state: state,
              child: Builder(
                builder: (context) => ExamDatesScreen(
                  navIndex: 0,
                  onNav: onNav ?? (_) {},
                  onPracticeExam: onPractice ?? (_) {},
                  onMockExam: onMock ?? (_) {},
                ),
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

    testWidgets('renders rows, earliest first, with countdown chips', (
      tester,
    ) async {
      await pumpScreen(tester);
      // Earliest entry (2083-07-15) is the first row; its chip is
      // computed from the real clock (the old test hardcoded
      // "Tomorrow", which only held on the anchor date 2083-07-14).
      expect(find.text('MECEE-BL 2027 BDS entrance exam'), findsOneWidget);
      final daysUntil = bsDaysUntil('2083-07-15');
      final expectedChip = switch (examDateChipKind(daysUntil)) {
        ExamDateChipKind.today => '🔴 Today',
        ExamDateChipKind.tomorrow => '🟡 Tomorrow',
        ExamDateChipKind.soon => '🟡 in $daysUntil days',
        ExamDateChipKind.later => '📅 in $daysUntil days',
        ExamDateChipKind.past => '✓ Done',
      };
      final firstCard = find.ancestor(
        of: find.text('MECEE-BL 2027 BDS entrance exam'),
        matching: find.byType(Card),
      );
      expect(
        find.descendant(of: firstCard, matching: find.text(expectedChip)),
        findsOneWidget,
      );
      // A late entry exists in the list once scrolled into view.
      await tester.scrollUntilVisible(
        find.textContaining('NMCLE undergraduate'),
        400,
        scrollable: find.descendant(
          of: find.byType(ListView),
          matching: find.byType(Scrollable),
        ),
      );
      await tester.pumpAndSettle();
      expect(find.textContaining('NMCLE undergraduate'), findsOneWidget);
    });

    testWidgets('kind filter chips narrow the list', (tester) async {
      await pumpScreen(tester);
      // All + per-kind chips derived from the data (vanilla behaviour).
      expect(find.text('All'), findsOneWidget);
      expect(find.text('Exam'), findsOneWidget);
      expect(find.text('Deadline'), findsOneWidget);

      await tester.tap(find.text('Deadline'));
      await tester.pumpAndSettle();
      expect(find.text('MECEE-BL 2027 BDS entrance exam'), findsNothing);
      expect(find.textContaining('application deadline'), findsWidgets);

      await tester.tap(find.text('All'));
      await tester.pumpAndSettle();
      expect(find.text('MECEE-BL 2027 BDS entrance exam'), findsOneWidget);
    });

    testWidgets('medium-confidence rows show the re-verify badge', (
      tester,
    ) async {
      await pumpScreen(tester);
      // High-confidence first row carries no badge…
      final highCard = find.ancestor(
        of: find.text('MECEE-BL 2027 BDS entrance exam'),
        matching: find.byType(Card),
      );
      expect(
        find.descendant(of: highCard, matching: find.text('re-verify')),
        findsNothing,
      );
      // …while a medium-confidence row does (ListView builds lazily, so
      // scroll to it rather than counting all 8).
      await tester.scrollUntilVisible(
        find.textContaining('BAMS licensing exam'),
        400,
        scrollable: find.descendant(
          of: find.byType(ListView),
          matching: find.byType(Scrollable),
        ),
      );
      await tester.pumpAndSettle();
      final medCard = find.ancestor(
        of: find.textContaining('BAMS licensing exam'),
        matching: find.byType(Card),
      );
      expect(
        find.descendant(of: medCard, matching: find.text('re-verify')),
        findsOneWidget,
      );
    });

    testWidgets('remind-me toggle flips via the loksewa_reminders_v1 store', (
      tester,
    ) async {
      final state = await pumpScreen(tester);

      // The earliest rows are past now (no Remind button), so use a
      // far-future entry: NEC licence exam 4th cycle (2084-03-04).
      expect(state.hasReminder('nec-4th-cycle-exam-begins'), isFalse);
      await tester.scrollUntilVisible(
        find.text('NEC licence exam 4th cycle begins'),
        400,
        scrollable: find.descendant(
          of: find.byType(ListView),
          matching: find.byType(Scrollable),
        ),
      );
      await tester.pumpAndSettle();
      final card = find.ancestor(
        of: find.text('NEC licence exam 4th cycle begins'),
        matching: find.byType(Card),
      );
      await tester.tap(
        find.descendant(of: card, matching: find.text('🔕 Remind me')),
      );
      await tester.pumpAndSettle();
      expect(state.hasReminder('nec-4th-cycle-exam-begins'), isTrue);
      expect(
        find.descendant(of: card, matching: find.text('🔔 Reminding')),
        findsOneWidget,
      );
    });

    testWidgets('Practice button deep-links with the mapped exam', (
      tester,
    ) async {
      Exam? got;
      await pumpScreen(tester, onPractice: (e) => got = e);
      // First row (earliest date) maps to mecee-bl.
      await tester.tap(find.text('Practice').first);
      await tester.pumpAndSettle();
      expect(got?.id, 'mecee-bl');
    });

    testWidgets('unmapped rows show no Practice/Mock buttons', (tester) async {
      await pumpScreen(tester);
      // Mapped row (first card) carries both deep-link buttons.
      final mappedCard = find.ancestor(
        of: find.text('MECEE-BL 2027 BDS entrance exam'),
        matching: find.byType(Card),
      );
      expect(
        find.descendant(of: mappedCard, matching: find.text('Practice')),
        findsOneWidget,
      );
      expect(
        find.descendant(of: mappedCard, matching: find.text('Mock')),
        findsOneWidget,
      );
      // NMC special-exam rows (exam:null) carry neither — scroll to them.
      await tester.scrollUntilVisible(
        find.text('NMC Special Examination day 1'),
        400,
        scrollable: find.descendant(
          of: find.byType(ListView),
          matching: find.byType(Scrollable),
        ),
      );
      await tester.pumpAndSettle();
      final unmappedCard = find.ancestor(
        of: find.text('NMC Special Examination day 1'),
        matching: find.byType(Card),
      );
      expect(
        find.descendant(of: unmappedCard, matching: find.text('Practice')),
        findsNothing,
      );
      expect(
        find.descendant(of: unmappedCard, matching: find.text('Mock')),
        findsNothing,
      );
    });

    testWidgets('official-source button opens the link in the browser',
        (tester) async {
      // v1.0.2: the button now opens the URL directly instead of
      // showing the copyable-URL dialog (that dialog is only the
      // fallback when the browser can't open the link).
      final fake = _FakeUrlLauncher()..result = true;
      final real = UrlLauncherPlatform.instance;
      UrlLauncherPlatform.instance = fake;
      addTearDown(() => UrlLauncherPlatform.instance = real);
      await pumpScreen(tester);
      await tester.tap(find.text('Official source').first);
      await tester.pumpAndSettle();
      expect(fake.launched, ['https://entrance.mec.gov.np']);
      expect(find.text('https://entrance.mec.gov.np'), findsNothing);
    });

    testWidgets('official-source button falls back to the link dialog',
        (tester) async {
      // When the browser can't open the link, the old copyable-URL
      // dialog appears instead.
      final fake = _FakeUrlLauncher()..result = false;
      final real = UrlLauncherPlatform.instance;
      UrlLauncherPlatform.instance = fake;
      addTearDown(() => UrlLauncherPlatform.instance = real);
      await pumpScreen(tester);
      await tester.tap(find.text('Official source').first);
      await tester.pumpAndSettle();
      expect(find.text('https://entrance.mec.gov.np'), findsOneWidget);
      await tester.tap(find.text('Close'));
      await tester.pumpAndSettle();
    });
  });
}
