/// Update checker tests (v1.0.2) — GitHub API responses are mocked.
library;

import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:loksewa_vidyapeeth/services/update_checker.dart';

http.Client _client({required int status, String? tag, String? body}) =>
    MockClient(
      (request) async {
        expect(request.url.toString(), contains('api.github.com'));
        return http.Response(
          jsonEncode({'tag_name': tag, 'body': body}),
          status,
          headers: {'content-type': 'application/json'},
        );
      },
    );

// Realistic release body, as written by the release workflow.
const _releaseBody = '''Signed release APK for Outrank v1.0.14 (Android).

What's new: **27 new exam dates** — PLSC Batch 03, TSC NiMaVi,
NRB deadline and RBB papers across four provinces. The update
check now shows what's new in the new version.

Install: download **app-release.apk**, open it on your phone and
allow "install unknown apps" if asked. No sign-in needed.
Installs over v1.0.13 as an update (same signature).

Bundled data: 109 exam dates, 47 exams, 64,689 questions,
63 festivals, 95 historical dates. No login, no ads, no tracking.''';

void main() {
  group('version compare', () {
    test('major/minor/patch ordering', () {
      expect(UpdateChecker.compareVersions('1.0.2', '1.0.2'), 0);
      expect(UpdateChecker.compareVersions('1.0.3', '1.0.2'), greaterThan(0));
      expect(UpdateChecker.compareVersions('1.0.2', '1.0.3'), lessThan(0));
      expect(UpdateChecker.compareVersions('1.10.0', '1.9.9'), greaterThan(0));
      expect(UpdateChecker.compareVersions('2.0.0', '1.99.99'), greaterThan(0));
    });

    test('tag parsing', () {
      expect(UpdateChecker.versionFromTag('android-v1.0.2'), '1.0.2');
      expect(UpdateChecker.versionFromTag('v2.3.4'), '2.3.4');
      expect(UpdateChecker.versionFromTag('no-version-here'), isNull);
      expect(UpdateChecker.versionFromTag(null), isNull);
    });
  });

  group('check()', () {
    test('newer release -> update available', () async {
      final checker = UpdateChecker(
        client: _client(status: 200, tag: 'android-v1.0.3'),
        currentVersion: '1.0.2',
      );
      final result = await checker.check();
      expect(result.updateAvailable, isTrue);
      expect(result.latestVersion, '1.0.3');
      expect(result.downloadUrl, contains('app-release.apk'));
    });

    test('same release -> up to date', () async {
      final checker = UpdateChecker(
        client: _client(status: 200, tag: 'android-v1.0.2'),
        currentVersion: '1.0.2',
      );
      final result = await checker.check();
      expect(result.updateAvailable, isFalse);
      expect(result.latestVersion, '1.0.2');
    });

    test('older release tag -> up to date (dev build)', () async {
      final checker = UpdateChecker(
        client: _client(status: 200, tag: 'android-v1.0.1'),
        currentVersion: '1.0.2',
      );
      final result = await checker.check();
      expect(result.updateAvailable, isFalse);
    });

    test('GitHub error -> throws', () async {
      final checker = UpdateChecker(
        client: _client(status: 403, tag: 'android-v1.0.3'),
        currentVersion: '1.0.2',
      );
      await expectLater(
        checker.check(),
        throwsA(isA<UpdateCheckException>()),
      );
    });

    test('release without a version tag -> throws', () async {
      final checker = UpdateChecker(
        client: _client(status: 200, tag: null),
        currentVersion: '1.0.2',
      );
      await expectLater(
        checker.check(),
        throwsA(isA<UpdateCheckException>()),
      );
    });
  });

  group('release notes (v1.0.14)', () {
    test("extracts the What's new section only", () async {
      final checker = UpdateChecker(
        client: _client(
          status: 200,
          tag: 'android-v1.0.14',
          body: _releaseBody,
        ),
        currentVersion: '1.0.13',
      );
      final result = await checker.check();
      expect(result.updateAvailable, isTrue);
      final notes = result.releaseNotes;
      expect(notes, isNotNull);
      expect(notes, contains('27 new exam dates'));
      expect(notes, contains("shows what's new"));
      // The surrounding sections are not part of the notes, and the
      // markdown bold markers are stripped for plain-text display.
      expect(notes, isNot(contains('Signed release APK')));
      expect(notes, isNot(contains('Install:')));
      expect(notes, isNot(contains('Bundled data')));
      expect(notes, isNot(contains('**')));
    });

    test('no marker -> whole body, trimmed', () async {
      final checker = UpdateChecker(
        client: _client(
          status: 200,
          tag: 'android-v1.0.14',
          body: '  A short note with no sections.  ',
        ),
        currentVersion: '1.0.13',
      );
      final result = await checker.check();
      expect(result.releaseNotes, 'A short note with no sections.');
    });

    test('no body -> null notes (dialog shows a generic line)', () async {
      final checker = UpdateChecker(
        client: _client(status: 200, tag: 'android-v1.0.14'),
        currentVersion: '1.0.13',
      );
      final result = await checker.check();
      expect(result.releaseNotes, isNull);
    });

    test('empty body -> null notes', () {
      expect(UpdateChecker.extractWhatsNew(''), isNull);
      expect(UpdateChecker.extractWhatsNew('   '), isNull);
      expect(UpdateChecker.extractWhatsNew(null), isNull);
    });

    test('very long body is capped', () {
      final long = 'x' * 2000;
      final notes = UpdateChecker.extractWhatsNew(long);
      expect(notes, isNotNull);
      expect(notes!.length, 1501); // 1500 chars + ellipsis
      expect(notes.endsWith('…'), isTrue);
    });
  });
}
