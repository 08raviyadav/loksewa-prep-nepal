/// Privacy Policy (v1.0.2) — the in-app copy of PRIVACY.md.
///
/// Reached from the drawer. The text lives in
/// lib/l10n/privacy_strings.dart (EN + NE); the same text is published
/// as PRIVACY.md in the repo root for the Play Store listing.
library;

import 'package:flutter/material.dart';

import '../l10n/privacy_strings.dart';
import '../theme/app_theme.dart';
import '../widgets/app_scaffold.dart';

class PrivacyScreen extends StatelessWidget {
  static const routeName = '/privacy';

  final int navIndex;
  final ValueChanged<int> onNav;

  const PrivacyScreen({
    super.key,
    required this.navIndex,
    required this.onNav,
  });

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final p = PrivacyStrings(state.isNe);
    return AppScaffold(
      title: s.privacyTitle,
      currentIndex: navIndex,
      onNav: onNav,
      body: ListView(
        padding: const EdgeInsets.all(AppSpacing.s4),
        children: [
          Text(
            p.lastUpdated,
            style: AppType.tiny.copyWith(color: AppColors.muted),
          ),
          const SizedBox(height: AppSpacing.s3),
          Text(p.intro, style: AppType.lead),
          const SizedBox(height: AppSpacing.s4),
          for (final (title, body) in p.sections) ...[
            Text(title, style: AppType.h3),
            const SizedBox(height: AppSpacing.s2),
            Text(body, style: AppType.body),
            const SizedBox(height: AppSpacing.s4),
          ],
        ],
      ),
    );
  }
}
