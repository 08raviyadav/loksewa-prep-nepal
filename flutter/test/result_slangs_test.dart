// Funny result slangs (v1.0.8): band boundaries, both scripts, no empty
// lines, and the slang card on the result screen for perfect + low scores.
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:loksewa_vidyapeeth/engine/quiz_engine.dart';
import 'package:loksewa_vidyapeeth/gamification/result_slangs.dart';
import 'package:loksewa_vidyapeeth/l10n/app_strings.dart';
import 'package:loksewa_vidyapeeth/screens/quiz/result_screen.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/state/progress_store.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';

/// Devanagari block — a line is Devanagari if it holds at least one.
final _devanagari = RegExp(r'[\u0900-\u097F]');

QuizResult _result(double score, int max) => QuizResult(
      score: score,
      max: max,
      pct: max <= 0 ? 0 : score / max * 100,
      correct: score.round(),
      wrong: max - score.round(),
      skipped: 0,
      secs: 120,
      timedOut: false,
      perQuestion: const [],
      byTopic: const {},
      wrongList: const [],
    );

Future<void> _pumpResult(
  WidgetTester tester,
  QuizResult result, {
  bool nepali = false,
}) async {
  SharedPreferences.setMockInitialValues({});
  ProgressStore.resetForTest();
  final state = AppState();
  await state.init();
  if (nepali) await state.setLang(AppLang.ne);
  final store = await ProgressStore.instance;
  await tester.pumpWidget(
    AppStateScope(
      state: state,
      child: AnimatedBuilder(
        animation: state,
        builder: (context, _) => MaterialApp(
          theme: buildAppTheme(),
          home: ResultScreen(
            result: result,
            meta: const QuizMeta(
              examName: 'Kharidar',
              cutoff: 45,
              cutoffPct: 45,
              fullTotal: 100,
            ),
            config: const QuizConfig(questions: [], examId: 'kharidar'),
            summary: const AttemptSummary(
              passed: true,
              xp: 10,
              oldLevel: 1,
              newLevel: 1,
              leveledUp: false,
              weeklyMet: false,
            ),
            bank: const [],
            store: store,
          ),
        ),
      ),
    ),
  );
  await tester.pumpAndSettle();
}

/// The slang text currently shown in the result card.
Future<String> _shownSlang(WidgetTester tester) async {
  final card = find.byKey(const Key('result-slang-card'));
  await tester.scrollUntilVisible(
    card,
    300,
    scrollable: find.byType(Scrollable).first,
  );
  await tester.pumpAndSettle();
  final text = tester.widget<Text>(
    find.descendant(of: card, matching: find.byType(Text)),
  );
  return text.data ?? '';
}

void main() {
  group('result slang data', () {
    test('all 20 lines present, 4 + 4 + 4 + 8 per band', () {
      expect(perfectSlangs.length, 4);
      expect(goodSlangs.length, 4);
      expect(averageSlangs.length, 4);
      expect(lowSlangs.length, 8);
      expect(allResultSlangs.length, 20);
    });

    test('no empty line in either script', () {
      for (final s in allResultSlangs) {
        expect(s.roman.trim(), isNotEmpty);
        expect(s.nepali.trim(), isNotEmpty);
      }
    });

    test('roman lines hold no Devanagari, nepali lines hold Devanagari', () {
      for (final s in allResultSlangs) {
        expect(_devanagari.hasMatch(s.roman), isFalse, reason: s.roman);
        expect(_devanagari.hasMatch(s.nepali), isTrue, reason: s.nepali);
      }
    });

    test('text() returns the script matching the language flag', () {
      const s = ResultSlang(roman: 'Katxa tero Loksewa! 🔥', nepali: 'कट्छ तेरो लोकसेवा! 🔥');
      expect(s.text(false), 'Katxa tero Loksewa! 🔥');
      expect(s.text(true), 'कट्छ तेरो लोकसेवा! 🔥');
    });
  });

  group('slang band boundaries', () {
    void expectBand(double score, num total, List<ResultSlang> band) {
      // Several seeds: every pick must land in the expected band.
      for (var seed = 0; seed < 20; seed++) {
        expect(band, contains(pickResultSlang(score, total, Random(seed))));
      }
      expect(slangBandFor(score, total), same(band));
    }

    test('100% is perfect', () {
      expectBand(20, 20, perfectSlangs);
      expectBand(100, 100, perfectSlangs);
    });

    test('80–99% is good', () {
      expectBand(99, 100, goodSlangs);
      expectBand(80, 100, goodSlangs);
    });

    test('50–79% is average', () {
      expectBand(79, 100, averageSlangs);
      expectBand(50, 100, averageSlangs);
    });

    test('below 50% is low, including 0 and empty quizzes', () {
      expectBand(49, 100, lowSlangs);
      expectBand(0, 100, lowSlangs);
      expectBand(0, 0, lowSlangs);
    });
  });

  group('result screen slang card', () {
    testWidgets('perfect score shows a perfect-band slang in Roman', (
      WidgetTester tester,
    ) async {
      await _pumpResult(tester, _result(20, 20));
      final shown = await _shownSlang(tester);
      expect(
        perfectSlangs.map((s) => s.roman),
        contains(shown),
        reason: 'shown: $shown',
      );
    });

    testWidgets('low score shows a low-band slang in Roman', (
      WidgetTester tester,
    ) async {
      await _pumpResult(tester, _result(3, 20));
      final shown = await _shownSlang(tester);
      expect(
        lowSlangs.map((s) => s.roman),
        contains(shown),
        reason: 'shown: $shown',
      );
    });

    testWidgets('Nepali language shows a Devanagari slang', (
      WidgetTester tester,
    ) async {
      await _pumpResult(tester, _result(3, 20), nepali: true);
      final shown = await _shownSlang(tester);
      expect(
        lowSlangs.map((s) => s.nepali),
        contains(shown),
        reason: 'shown: $shown',
      );
      expect(_devanagari.hasMatch(shown), isTrue);
    });

    testWidgets('rebuild does not re-roll the slang', (
      WidgetTester tester,
    ) async {
      await _pumpResult(tester, _result(20, 20));
      final first = await _shownSlang(tester);
      await tester.pump();
      final second = await _shownSlang(tester);
      expect(second, first);
    });
  });
}
