/// Update checker tests (v1.0.2) — GitHub API responses are mocked.
library;

import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:loksewa_vidyapeeth/services/update_checker.dart';

http.Client _client({required int status, String? tag}) => MockClient(
      (request) async {
        expect(request.url.toString(), contains('api.github.com'));
        return http.Response(
          jsonEncode({'tag_name': tag}),
          status,
          headers: {'content-type': 'application/json'},
        );
      },
    );

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
}
