/// Exam Dates screen — the Flutter port of the vanilla site's
/// view-examdates (loksewa-prep-nepal/assets/js/app.js §"Exam dates").
/// Chronological list of data/exam-dates.json entries with countdown
/// chips, kind filter, official-source links, ⚠️ re-verify badges,
/// Practice/Mock deep-links and per-row 🔔 Remind me toggles reusing
/// the loksewa_reminders_v1 store in AppState.
///
/// Deep-link convention (main.dart integration):
///   - [ExamDatesScreen.routeName] is '/exam-dates'.
///   - [onPracticeExam] fires with the mapped [Exam] when the row's
///     Practice button is tapped — the integrator opens the Practice
///     setup prefilled (HomeScreen's onPracticeExam is the model:
///     store as initialExam, go to nav index 1).
///   - [onMockExam] fires with the mapped [Exam] for the Mock button —
///     the integrator opens the Mock flow with that exam preselected.
library;

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';

import '../data/data_repository.dart';
import '../l10n/examdates_strings.dart';
import '../models/models.dart';
import '../theme/app_theme.dart';
import '../utils/bs_calendar.dart';
import '../widgets/app_scaffold.dart';

/// Countdown chip bucket — mirrors the vanilla site's remChip().
enum ExamDateChipKind { today, tomorrow, soon, later, past }

/// Bucket for a days-until value. Vanilla: d<0 → past ("✓ Done" chip),
/// 0 → today, 1 → tomorrow, 2..7 → soon (🟡), >7 → later (📅).
/// Null (unparseable date) behaves as past — no live countdown.
ExamDateChipKind examDateChipKind(int? daysUntil) {
  if (daysUntil == null || daysUntil < 0) return ExamDateChipKind.past;
  if (daysUntil == 0) return ExamDateChipKind.today;
  if (daysUntil == 1) return ExamDateChipKind.tomorrow;
  if (daysUntil <= 7) return ExamDateChipKind.soon;
  return ExamDateChipKind.later;
}

/// Chronological sort — mirrors vanilla's
/// `list.sort((a,b)=>a.date_bs<b.date_bs?-1:(a.date_bs>b.date_bs?1:0))`.
/// Zero-padded BS YYYY-MM-DD strings sort lexicographically.
List<ExamDate> sortExamDates(List<ExamDate> dates) {
  final out = List<ExamDate>.of(dates);
  out.sort((a, b) => a.dateBs.compareTo(b.dateBs));
  return out;
}

/// Kind filter — mirrors vanilla's `shown=list.filter(e=>!f||e.kind===f)`.
List<ExamDate> filterExamDatesByKind(List<ExamDate> dates, String kindFilter) {
  if (kindFilter.isEmpty) return List<ExamDate>.of(dates);
  return dates.where((e) => e.kind == kindFilter).toList();
}

/// Distinct kinds present in [dates], in first-seen order — mirrors
/// vanilla's `kinds=[...new Set(list.map(e=>e.kind).filter(Boolean))]`.
List<String> examDateKinds(List<ExamDate> dates) {
  final kinds = <String>[];
  for (final e in dates) {
    if (e.kind.isNotEmpty && !kinds.contains(e.kind)) kinds.add(e.kind);
  }
  return kinds;
}

/// Map an ExamDate to its Exam — mirrors vanilla's
/// `e.exam && examById(e.exam)`: no exam id, or no matching exam, → null
/// and the row shows no Practice/Mock buttons. (The NMC special-exam
/// entries carry exam:null, so they render without links — same as web.)
Exam? examForExamDate(ExamDate date, List<Exam> exams) {
  if (date.exam.isEmpty) return null;
  for (final e in exams) {
    if (e.id == date.exam) return e;
  }
  return null;
}

class ExamDatesScreen extends StatefulWidget {
  static const routeName = '/exam-dates';

  final int navIndex;
  final ValueChanged<int> onNav;

  /// Deep-link: Practice setup prefilled with the mapped exam.
  final ValueChanged<Exam> onPracticeExam;

  /// Deep-link: Mock flow with the mapped exam preselected.
  final ValueChanged<Exam> onMockExam;

  const ExamDatesScreen({
    super.key,
    required this.navIndex,
    required this.onNav,
    required this.onPracticeExam,
    required this.onMockExam,
  });

  @override
  State<ExamDatesScreen> createState() => _ExamDatesScreenState();
}

class _ExamDatesScreenState extends State<ExamDatesScreen> {
  String _kindFilter = '';
  late final Future<({List<Exam> exams, List<ExamDate> dates})> _loadFuture;

  @override
  void initState() {
    super.initState();
    _loadFuture = Future(() async {
      final repo = DataRepository();
      final exams = await repo.exams();
      final dates = await repo.examDates();
      return (exams: exams, dates: sortExamDates(dates));
    });
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateScope.of(context);
    final s = appState.strings;
    return AppScaffold(
      title: s.examDatesTitle,
      currentIndex: widget.navIndex,
      onNav: widget.onNav,
      body: FutureBuilder<({List<Exam> exams, List<ExamDate> dates})>(
        future: _loadFuture,
        builder: (context, snap) {
          if (!snap.hasData) {
            return const Center(child: CircularProgressIndicator());
          }
          final exams = snap.data!.exams;
          final dates = snap.data!.dates;
          final kinds = examDateKinds(dates);
          final shown = filterExamDatesByKind(dates, _kindFilter);
          return Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 4),
                child: Text(s.examDatesBlurb, style: AppType.small),
              ),
              if (kinds.length > 1) _filterRow(kinds),
              Expanded(
                child: shown.isEmpty
                    ? _EmptyState()
                    : ListView.builder(
                        padding: const EdgeInsets.fromLTRB(16, 8, 16, 8),
                        itemCount: shown.length + 1,
                        itemBuilder: (context, i) {
                          if (i == shown.length) {
                            return Padding(
                              padding: const EdgeInsets.symmetric(
                                vertical: 16,
                                horizontal: 4,
                              ),
                              child: Text(
                                s.confirmNote,
                                style: AppType.small.copyWith(
                                  color: Theme.of(context)
                                      .colorScheme
                                      .onSurface
                                      .withValues(alpha: 0.6),
                                ),
                              ),
                            );
                          }
                          return _ExamDateCard(
                            date: shown[i],
                            exam: examForExamDate(shown[i], exams),
                            onPracticeExam: widget.onPracticeExam,
                            onMockExam: widget.onMockExam,
                          );
                        },
                      ),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _filterRow(List<String> kinds) {
    final appState = AppStateScope.of(context);
    final s = appState.strings;
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          Text(s.showFilterLabel, style: AppType.small),
          const SizedBox(width: 8),
          ChoiceChip(
            label: Text(s.kindAll),
            selected: _kindFilter.isEmpty,
            onSelected: (_) => setState(() => _kindFilter = ''),
          ),
          for (final k in kinds) ...[
            const SizedBox(width: 8),
            ChoiceChip(
              label: Text(s.kindLabel(k)),
              selected: _kindFilter == k,
              onSelected: (_) => setState(() => _kindFilter = k),
            ),
          ],
        ],
      ),
    );
  }
}

class _ExamDateCard extends StatelessWidget {
  final ExamDate date;
  final Exam? exam;
  final ValueChanged<Exam> onPracticeExam;
  final ValueChanged<Exam> onMockExam;

  const _ExamDateCard({
    required this.date,
    required this.exam,
    required this.onPracticeExam,
    required this.onMockExam,
  });

  @override
  Widget build(BuildContext context) {
    final appState = AppStateScope.of(context);
    final s = appState.strings;
    final ne = appState.isNe;
    final daysUntil = bsDaysUntil(date.dateBs);
    final kind = examDateChipKind(daysUntil);
    final past = kind == ExamDateChipKind.past && daysUntil != null;
    final reminding = appState.hasReminder(date.id);

    final card = Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _CountdownChip(kind: kind, daysUntil: daysUntil ?? 0),
            const SizedBox(height: 8),
            Text(date.title(ne), style: AppType.h3),
            const SizedBox(height: 6),
            Wrap(
              crossAxisAlignment: WrapCrossAlignment.center,
              spacing: 6,
              runSpacing: 4,
              children: [
                Text(
                  '${fmtBs(date.dateBs, ne: ne)} · ${s.kindLabel(date.kind)}',
                  style: AppType.small,
                ),
                if (date.source.isNotEmpty)
                  TextButton(
                    style: TextButton.styleFrom(
                      padding: EdgeInsets.zero,
                      minimumSize: const Size(0, 28),
                      tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                    ),
                    onPressed: () => _openSource(context, date),
                    child: Text(
                      s.officialSource,
                      style: AppType.small.copyWith(
                        decoration: TextDecoration.underline,
                      ),
                    ),
                  ),
                if (date.confidence == 'medium')
                  Tooltip(
                    message: s.reverifyHint,
                    child: Text(s.reverifyBadge, style: AppType.small),
                  ),
              ],
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                // Local for closure capture (field promotion doesn't reach
                // closures). Vanilla gates Mock on ex.prelim; the Flutter
                // Exam model carries no prelim flag, so a mapped exam shows
                // both buttons (Milestone 3 spec: Practice + Mock per row).
                if (exam case final Exam ex) ...[
                  OutlinedButton(
                    onPressed: () => onPracticeExam(ex),
                    child: Text(s.practiceBtn),
                  ),
                  OutlinedButton(
                    onPressed: () => onMockExam(ex),
                    child: Text(s.mockBtn),
                  ),
                ],
                if (!past)
                  OutlinedButton(
                    style: OutlinedButton.styleFrom(
                      side: reminding
                          ? const BorderSide(color: AppColors.accent)
                          : null,
                    ),
                    onPressed: () => appState.toggleReminder(date.id),
                    child: Text(reminding ? s.remindingBtn : s.remindMeBtn),
                  ),
              ],
            ),
          ],
        ),
      ),
    );

    // Past rows render dimmed (vanilla's ed-past class).
    if (past) {
      return Opacity(opacity: 0.55, child: card);
    }
    return card;
  }
}

class _CountdownChip extends StatelessWidget {
  final ExamDateChipKind kind;
  final int daysUntil;

  const _CountdownChip({required this.kind, required this.daysUntil});

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final (label, bg) = switch (kind) {
      ExamDateChipKind.today => (s.chipToday, AppColors.dangerSoft),
      ExamDateChipKind.tomorrow => (s.chipTomorrow, AppColors.accentSoft),
      ExamDateChipKind.soon => (s.chipSoon(daysUntil), AppColors.accentSoft),
      ExamDateChipKind.later => (s.chipLater(daysUntil), AppColors.blueSoft),
      ExamDateChipKind.past => (s.chipDone, AppColors.greenSoft),
    };
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(label, style: AppType.small),
    );
  }
}

class _EmptyState extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('📅', style: TextStyle(fontSize: 48)),
            const SizedBox(height: 12),
            Text(
              s.noDatesTitle,
              style: AppType.h2,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            Text(
              s.noDatesBody,
              style: AppType.body,
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}

/// Official-source link: opens the URL in the browser. If the device
/// can't open it, falls back to the copyable-URL dialog below.
Future<void> _openSource(BuildContext context, ExamDate date) async {
  final ok = await launchUrl(
    Uri.parse(date.source),
    mode: LaunchMode.externalApplication,
  );
  if (!ok && context.mounted) {
    await _showSourceDialog(context, date);
  }
}

/// Fallback for [_openSource]: the URL as selectable text with a copy
/// button, for devices that can't open the link.
Future<void> _showSourceDialog(BuildContext context, ExamDate date) async {
  final s = AppStateScope.of(context).strings;
  await showDialog<void>(
    context: context,
    builder: (context) => AlertDialog(
      title: Text(s.sourceDialogTitle),
      content: SelectableText(date.source),
      actions: [
        TextButton(
          onPressed: () async {
            await Clipboard.setData(ClipboardData(text: date.source));
            if (context.mounted) {
              Navigator.of(context).pop();
              ScaffoldMessenger.of(context)
                  .showSnackBar(SnackBar(content: Text(s.linkCopied)));
            }
          },
          child: Text(s.copyLink),
        ),
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: Text(s.closeBtn),
        ),
      ],
    ),
  );
}
