/// Update-available dialog (v1.0.14): shows the new version's release
/// notes under a "What's new" heading, in a scrollable area so long
/// notes can't overflow the dialog. Notes come from the GitHub release
/// body as published (English); only the chrome is localised. When the
/// release carries no notes, a short generic line is shown instead —
/// the update flow never blocks on notes.
library;

import 'package:flutter/material.dart';

import '../l10n/app_strings.dart';
import '../services/update_checker.dart';
import '../theme/app_theme.dart';

class UpdateAvailableDialog extends StatelessWidget {
  final UpdateCheckResult result;
  final AppStrings strings;

  const UpdateAvailableDialog({
    super.key,
    required this.result,
    required this.strings,
  });

  @override
  Widget build(BuildContext context) {
    final s = strings;
    return AlertDialog(
      title: Text(s.updateAvailable),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(s.updateAvailableBody(result.latestVersion)),
          const SizedBox(height: AppSpacing.s3),
          Text(
            s.whatsNew,
            style: AppType.h3.copyWith(
              color: AppColors.of(context).text,
            ),
          ),
          const SizedBox(height: AppSpacing.s2),
          ConstrainedBox(
            constraints: const BoxConstraints(maxHeight: 220),
            child: SingleChildScrollView(
              child: Text(
                result.releaseNotes ?? s.updateNoNotes,
                style: AppType.body.copyWith(
                  color: AppColors.of(context).text,
                ),
              ),
            ),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context, false),
          child: Text(s.later),
        ),
        FilledButton(
          onPressed: () => Navigator.pop(context, true),
          child: Text(s.download),
        ),
      ],
    );
  }
}
