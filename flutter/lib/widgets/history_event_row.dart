import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';

import '../l10n/history_strings.dart';
import '../models/history.dart';
import '../theme/app_theme.dart';
import 'app_scaffold.dart';

/// One expandable history row — shared by the Dates to Remember screen
/// and the Home "On This Day" card. Mirrors the vanilla site's
/// historyRowHtml(): category chip, date + title (a muted note instead
/// of a date for dateless entries — never "null"), ⚠️ re-verify mark
/// for medium-confidence entries, tap to reveal the bilingual summary
/// + numbered sources.
class HistoryEventRow extends StatelessWidget {
  final HistoricalEvent event;

  const HistoryEventRow({super.key, required this.event});

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;
    final date = historyDateLabel(event, ne: ne);
    final muted =
        Theme.of(context).colorScheme.onSurface.withValues(alpha: 0.6);

    return Card(
      margin: const EdgeInsets.only(bottom: AppSpacing.s3),
      child: ExpansionTile(
        tilePadding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.s4,
          vertical: 2,
        ),
        childrenPadding: const EdgeInsets.fromLTRB(
          AppSpacing.s4,
          0,
          AppSpacing.s4,
          AppSpacing.s4,
        ),
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Wrap(
              spacing: 6,
              runSpacing: 4,
              crossAxisAlignment: WrapCrossAlignment.center,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: AppColors.accentSoft,
                    borderRadius: BorderRadius.circular(999),
                  ),
                  child: Text(
                    '📜 ${s.historyCategory(event.category)}',
                    style: AppType.small,
                  ),
                ),
                if (event.needsReverify)
                  Tooltip(
                    message: s.historyReverifyHint,
                    child: Text(s.historyReverify, style: AppType.small),
                  ),
              ],
            ),
            const SizedBox(height: 6),
            if (date.isNotEmpty)
              Text.rich(
                TextSpan(
                  children: [
                    TextSpan(
                      text: date,
                      style: const TextStyle(fontWeight: FontWeight.w700),
                    ),
                    TextSpan(text: ' — ${event.title(ne)}'),
                  ],
                ),
                style: AppType.h3,
              )
            else
              Text.rich(
                TextSpan(
                  children: [
                    TextSpan(
                      text: s.historyYearInSummary,
                      style: TextStyle(color: muted),
                    ),
                    TextSpan(text: ' — ${event.title(ne)}'),
                  ],
                ),
                style: AppType.h3,
              ),
          ],
        ),
        children: [
          Align(
            alignment: Alignment.centerLeft,
            child: Text(event.summary(ne), style: AppType.body),
          ),
          if (event.sources.isNotEmpty) ...[
            const SizedBox(height: 8),
            Align(
              alignment: Alignment.centerLeft,
              child: Wrap(
                crossAxisAlignment: WrapCrossAlignment.center,
                spacing: 6,
                children: [
                  Text('${s.historySources}:', style: AppType.small),
                  for (var i = 0; i < event.sources.length; i++)
                    TextButton(
                      style: TextButton.styleFrom(
                        padding: EdgeInsets.zero,
                        minimumSize: const Size(28, 28),
                        tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                      ),
                      onPressed: () =>
                          openHistorySource(context, event.sources[i]),
                      child: Text(
                        '${i + 1}',
                        style: AppType.small.copyWith(
                          decoration: TextDecoration.underline,
                        ),
                      ),
                    ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }
}

/// Source link: opens the URL in the browser. If the device can't open
/// it (launch fails or throws), falls back to the copyable-URL dialog
/// below.
Future<void> openHistorySource(BuildContext context, String url) async {
  bool ok = false;
  try {
    ok = await launchUrl(
      Uri.parse(url),
      mode: LaunchMode.externalApplication,
    );
  } catch (_) {
    ok = false;
  }
  if (!ok && context.mounted) {
    await _showHistorySourceDialog(context, url);
  }
}

/// Fallback for [openHistorySource]: the URL as selectable text with a
/// copy button, for devices that can't open the link.
Future<void> _showHistorySourceDialog(
  BuildContext context,
  String url,
) async {
  final s = AppStateScope.of(context).strings;
  await showDialog<void>(
    context: context,
    builder: (context) => AlertDialog(
      title: Text(s.historySourceTitle),
      content: SelectableText(url),
      actions: [
        TextButton(
          onPressed: () async {
            await Clipboard.setData(ClipboardData(text: url));
            if (context.mounted) {
              Navigator.of(context).pop();
              ScaffoldMessenger.of(context)
                  .showSnackBar(SnackBar(content: Text(s.historyLinkCopied)));
            }
          },
          child: Text(s.historyCopyLink),
        ),
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: Text(s.historyClose),
        ),
      ],
    ),
  );
}
