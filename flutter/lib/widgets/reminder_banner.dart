import 'package:flutter/material.dart';

import '../models/models.dart';
import '../theme/app_theme.dart';
import '../utils/bs_calendar.dart';
import 'app_scaffold.dart';

/// Home hero reminder banner — the first reminder display type.
/// Shows when an exam is today or within 7 days; dismissible per item.
/// Mirrors the vanilla site's hero banner (dismissal key:
/// `loksewa_rem_dismissed_v1`, same localStorage key name for parity).
class ReminderBanner extends StatelessWidget {
  final List<ExamDate> dates;
  const ReminderBanner({super.key, required this.dates});

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;

    ExamDate? pick;
    int? pickDays;
    for (final d in dates) {
      final days = bsDaysUntil(d.dateBs);
      if (days == null || days < 0 || days > 7) continue;
      if (state.isDismissed('banner:${d.id}')) continue;
      if (pickDays == null || days < pickDays) {
        pick = d;
        pickDays = days;
      }
    }
    if (pick == null || pickDays == null) return const SizedBox.shrink();
    final exam = pick;

    final label = pickDays == 0
        ? '\ud83d\udd14 ${exam.title(ne)} — ${s.todayBang}'
        : '\u23f0 ${exam.title(ne)} — ${bsCountdownLabel(pickDays, ne: ne)}';

    return Container(
      margin: const EdgeInsets.fromLTRB(
        AppSpacing.s4,
        AppSpacing.s4,
        AppSpacing.s4,
        0,
      ),
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.s4,
        vertical: AppSpacing.s3,
      ),
      decoration: BoxDecoration(
        color: AppColors.of(context).accentSoft,
        borderRadius: AppRadius.mdAll,
        border: Border.all(color: AppColors.of(context).accentLine),
      ),
      child: Row(
        children: [
          Expanded(
            child: Text(
              label,
              style: AppType.body.copyWith(fontWeight: FontWeight.w600),
            ),
          ),
          IconButton(
            tooltip: 'Dismiss',
            icon: const Icon(Icons.close, size: 20),
            constraints: const BoxConstraints(minWidth: 44, minHeight: 44),
            onPressed: () => state.dismiss('banner:${exam.id}'),
          ),
        ],
      ),
    );
  }
}
