/// Checks GitHub for a newer LokSewa Vidyapeeth release (v1.0.2).
///
/// Reads the repo's latest release tag (e.g. `android-v1.0.2`) via the
/// public GitHub API — no auth, no data sent — and compares it with the
/// installed version. Manual checks only, so the unauthenticated
/// 60-requests-per-hour API limit is never a concern.
library;

import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;

class UpdateCheckException implements Exception {
  final String message;
  const UpdateCheckException(this.message);
  @override
  String toString() => 'UpdateCheckException: $message';
}

class UpdateCheckResult {
  final bool updateAvailable;
  final String latestVersion;
  final String downloadUrl;
  const UpdateCheckResult({
    required this.updateAvailable,
    required this.latestVersion,
    required this.downloadUrl,
  });
}

class UpdateChecker {
  static const String _latestReleaseUrl =
      'https://api.github.com/repos/08raviyadav/loksewa-prep-nepal/releases/latest';

  /// Always points at the newest release's APK.
  static const String apkDownloadUrl =
      'https://github.com/08raviyadav/loksewa-prep-nepal/releases/latest/download/app-release.apk';

  final http.Client client;
  final String currentVersion; // e.g. '1.0.2'

  const UpdateChecker({required this.client, required this.currentVersion});

  Future<UpdateCheckResult> check() async {
    http.Response res;
    try {
      res = await client
          .get(
            Uri.parse(_latestReleaseUrl),
            headers: const {'Accept': 'application/vnd.github+json'},
          )
          .timeout(const Duration(seconds: 15));
    } on TimeoutException {
      throw const UpdateCheckException('Timed out talking to GitHub.');
    }
    if (res.statusCode != 200) {
      throw UpdateCheckException('GitHub returned ${res.statusCode}.');
    }
    final body = jsonDecode(res.body) as Map<String, dynamic>;
    final latest = versionFromTag(body['tag_name'] as String?);
    if (latest == null) {
      throw const UpdateCheckException('Release has no version tag.');
    }
    return UpdateCheckResult(
      updateAvailable: compareVersions(latest, currentVersion) > 0,
      latestVersion: latest,
      downloadUrl: apkDownloadUrl,
    );
  }

  /// Pulls `1.0.2` out of tags like `android-v1.0.2` or `v1.0.2`.
  static String? versionFromTag(String? tag) {
    if (tag == null) return null;
    final m = RegExp(r'(\d+)\.(\d+)\.(\d+)').firstMatch(tag);
    return m == null ? null : '${m[1]}.${m[2]}.${m[3]}';
  }

  /// Compares dotted version strings: > 0 when [a] is newer than [b].
  static int compareVersions(String a, String b) {
    final pa = a.split('.').map(int.tryParse).toList();
    final pb = b.split('.').map(int.tryParse).toList();
    for (var i = 0; i < 3; i++) {
      final va = i < pa.length ? pa[i] ?? 0 : 0;
      final vb = i < pb.length ? pb[i] ?? 0 : 0;
      if (va != vb) return va.compareTo(vb);
    }
    return 0;
  }
}
