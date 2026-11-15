/// Update-available dialog tests (v1.0.14): when an update is
/// available the dialog shows the new version's release notes; when the
/// release carries no notes, a generic line is shown instead. The
/// dialog takes a finished [UpdateCheckResult], so no HTTP is involved
/// here — the checker's parsing is covered by update_checker_test.dart.
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/l10n/app_strings.dart';
import 'package:loksewa_vidyapeeth/services/update_checker.dart';
import 'package:loksewa_vidyapeeth/widgets/update_available_dialog.dart';

void main() {
  const notes = '27 new exam dates across four provinces.';
  const withNotes = UpdateCheckResult(
    updateAvailable: true,
    latestVersion: '1.0.14',
    downloadUrl: 'https://example.invalid/app-release.apk',
    releaseNotes: notes,
  );
  const noNotes = UpdateCheckResult(
    updateAvailable: true,
    latestVersion: '1.0.14',
    downloadUrl: 'https://example.invalid/app-release.apk',
  );

  /// Pumps a page with a button that opens the dialog, then opens it.
  Future<void> openDialog(
    WidgetTester tester,
    UpdateCheckResult result,
    AppStrings strings,
  ) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Builder(
            builder: (context) => ElevatedButton(
              onPressed: () => showDialog<bool>(
                context: context,
                builder: (_) =>
                    UpdateAvailableDialog(result: result, strings: strings),
              ),
              child: const Text('open'),
            ),
          ),
        ),
      ),
    );
    await tester.tap(find.text('open'));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));
  }

  /// Opens the dialog, taps [buttonLabel], and returns the dialog's
  /// popped value.
  Future<bool?> openAndTap(
    WidgetTester tester, {
    required UpdateCheckResult result,
    required AppStrings strings,
    required String buttonLabel,
  }) async {
    bool? picked;
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Builder(
            builder: (context) => ElevatedButton(
              onPressed: () async {
                picked = await showDialog<bool>(
                  context: context,
                  builder: (_) => UpdateAvailableDialog(
                    result: result,
                    strings: strings,
                  ),
                );
              },
              child: const Text('open'),
            ),
          ),
        ),
      ),
    );
    await tester.tap(find.text('open'));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));
    await tester.tap(find.text(buttonLabel));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));
    return picked;
  }

  group('UpdateAvailableDialog', () {
    testWidgets('shows the release notes under What\'s new', (tester) async {
      await openDialog(tester, withNotes, const AppStrings(AppLang.en));
      expect(find.text('Update available'), findsOneWidget);
      expect(
        find.text('Version 1.0.14 is available. Download it now?'),
        findsOneWidget,
      );
      expect(find.text("What's new"), findsOneWidget);
      expect(find.text(notes), findsOneWidget);
    });

    testWidgets('shows the generic line when notes are absent',
        (tester) async {
      await openDialog(tester, noNotes, const AppStrings(AppLang.en));
      expect(find.text("What's new"), findsOneWidget);
      expect(
        find.text('No details available for this version.'),
        findsOneWidget,
      );
    });

    testWidgets('Download returns true, Later returns false',
        (tester) async {
      final download = await openAndTap(
        tester,
        result: withNotes,
        strings: const AppStrings(AppLang.en),
        buttonLabel: 'Download',
      );
      expect(download, isTrue);
      final later = await openAndTap(
        tester,
        result: withNotes,
        strings: const AppStrings(AppLang.en),
        buttonLabel: 'Later',
      );
      expect(later, isFalse);
    });

    testWidgets('Nepali chrome, notes stay in English', (tester) async {
      await openDialog(tester, withNotes, const AppStrings(AppLang.ne));
      expect(find.text('अपडेट उपलब्ध छ'), findsOneWidget);
      expect(find.text('नयाँ के छ'), findsOneWidget);
      expect(find.text(notes), findsOneWidget);
      expect(find.text('डाउनलोड'), findsOneWidget);
      expect(find.text('पछि'), findsOneWidget);
    });

    testWidgets('long notes scroll instead of overflowing',
        (tester) async {
      final longNotes = List.filled(60, 'A long release note line.').join(
        '\n',
      );
      final longResult = UpdateCheckResult(
        updateAvailable: true,
        latestVersion: '1.0.14',
        downloadUrl: 'https://example.invalid/app-release.apk',
        releaseNotes: longNotes,
      );
      await openDialog(tester, longResult, const AppStrings(AppLang.en));
      // The notes area is a scrollable: the first line is visible and
      // the dialog renders without overflow (no exception thrown).
      expect(find.textContaining('A long release note line.'), findsWidgets);
      await tester.drag(
        find.byType(SingleChildScrollView),
        const Offset(0, -200),
      );
      await tester.pump();
      expect(find.text("What's new"), findsOneWidget);
    });
  });
}
