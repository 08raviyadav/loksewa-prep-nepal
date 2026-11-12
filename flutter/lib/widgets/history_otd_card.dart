import 'package:flutter/material.dart';

import '../l10n/history_strings.dart';
import '../models/history.dart';
import '../theme/app_theme.dart';
import '../utils/bs_calendar.dart';
import 'app_scaffold.dart';
import 'history_event_row.dart';
import 'push_scope.dart';

/// "On This Day" card on Home — the Flutter port of the vanilla site's
/// renderHistoryOtd(). Shows the events whose BS month/day matches
/// today, any year. Renders NOTHING on a quiet day (no events today,
/// or the BS date can't be computed) — same as the web card.
///
/// [todayBsOverride] exists for tests (inject a BS date with a known
/// event instead of waiting for the real calendar).
class HistoryOtdCard extends StatelessWidget {
  final List<HistoricalEvent> events;
  final String? todayBsOverride;

  const HistoryOtdCard({super.key, required this.events, this.todayBsOverride});

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;
    final today = todayBsOverride ?? bsToday();
    if (today == null) return const SizedBox.shrink();
    final list = historyEventsToday(events, today);
    if (list.isEmpty) return const SizedBox.shrink();

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.s4),
      child: Card(
        margin: const EdgeInsets.only(bottom: AppSpacing.s3),
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.s4),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(s.historyOtdTitle, style: AppType.h2),
              const SizedBox(height: 4),
              Text(
                '${fmtBs(today, ne: ne)} — ${s.historyOtdSubtitle}',
                style: AppType.small.copyWith(color: AppColors.muted),
              ),
              const SizedBox(height: AppSpacing.s3),
              for (final e in historySorted(list)) HistoryEventRow(event: e),
              const SizedBox(height: AppSpacing.s2),
              OutlinedButton(
                onPressed: () => PushScope.of(context)?.onPush('/history'),
                child: Text(s.historyAllDatesBtn),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
