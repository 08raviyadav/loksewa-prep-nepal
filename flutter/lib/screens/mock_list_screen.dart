import 'package:flutter/material.dart';

import '../data/data_repository.dart';
import '../engine/exam_categories.dart';
import '../engine/mock_specs.dart';
import '../l10n/app_strings.dart';
import '../l10n/mock_strings.dart';
import '../models/models.dart';
import '../theme/app_theme.dart';
import '../widgets/app_scaffold.dart';
import 'mock_exam_screen.dart';

/// Mock Exams tab: pick an exam with a real paper pattern, see the
/// pattern, start the mock. Vanilla parity: only exams with a prelim
/// block offer mocks.
class MockListScreen extends StatefulWidget {
  final int navIndex;
  final ValueChanged<int> onNav;

  /// Exam preselected by a deep-link (Exam Dates screen).
  final Exam? initialExam;

  const MockListScreen({
    super.key,
    required this.navIndex,
    required this.onNav,
    this.initialExam,
  });

  @override
  State<MockListScreen> createState() => _MockListScreenState();
}

class _MockListScreenState extends State<MockListScreen> {
  late final Future<List<_MockEntry>> _entriesFuture;

  // Same organisation as the Practice picker (v1.0.1): 33 mocks as full
  // cards was ~10 screens of scrolling. Search + collapsible category
  // sections + one compact row per mock.
  final _searchCtrl = TextEditingController();
  String _query = '';
  final Set<String> _expanded = {};

  @override
  void initState() {
    super.initState();
    _entriesFuture = _load();
    if (widget.initialExam != null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _startMock(widget.initialExam!);
      });
    }
  }

  @override
  void dispose() {
    _searchCtrl.dispose();
    super.dispose();
  }

  Future<List<_MockEntry>> _load() async {
    final rows = await DataRepository().examRows();
    final out = <_MockEntry>[];
    for (final m in rows) {
      final prelim = m['prelim'];
      if (prelim == null) continue;
      final spec = MockSpec.fromPrelim(
        m['id'] as String,
        Map<String, dynamic>.from(prelim as Map),
      );
      out.add(
        _MockEntry(
          exam: Exam.fromJson(m),
          spec: spec,
        ),
      );
    }
    return out;
  }

  void _startMock(Exam exam) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => MockExamScreen(examId: exam.id),
      ),
    );
  }

  /// One-line pattern summary for the compact row, e.g.
  /// "50 Questions • 45 minutes • Pass 45/100 • 20% per wrong answer".
  /// The full detail lives in the bottom sheet, so a long line may
  /// ellipsize — nothing is lost.
  String _metaLine(MockSpec p, AppStrings s) {
    final time = p.timed ? s.minutesLabel(p.timeMin!) : s.untimedLine;
    final neg =
        p.negRate > 0 ? s.negPctLine((p.negRate * 100).round()) : s.negNoneLine;
    return '${p.questionCount} ${s.patternQuestions} • $time • '
        '${s.patternPass} ${p.cutoff}/${p.fullTotal} • $neg';
  }

  /// Full pattern detail as a bottom sheet: the v1.0.0 card content
  /// (name, pattern chips, big Start button), shown on demand instead
  /// of expanded for every mock at once.
  void _showDetails(_MockEntry e, bool ne) {
    final s = AppStateScope.of(context).strings;
    final p = e.spec;
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: AppRadius.lg),
      ),
      builder: (ctx) => Padding(
        padding: EdgeInsets.fromLTRB(
          AppSpacing.s4,
          AppSpacing.s3,
          AppSpacing.s4,
          AppSpacing.s4 + MediaQuery.of(ctx).viewPadding.bottom,
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: Container(
                width: 40,
                height: 4,
                decoration: BoxDecoration(
                  color: AppColors.of(context).borderSoft,
                  borderRadius: const BorderRadius.all(AppRadius.pill),
                ),
              ),
            ),
            const SizedBox(height: AppSpacing.s3),
            Text(e.exam.title(ne), style: AppType.h2),
            const SizedBox(height: AppSpacing.s3),
            Wrap(
              spacing: AppSpacing.s2,
              runSpacing: AppSpacing.s2,
              children: [
                _chip('${p.questionCount} ${s.patternQuestions}'),
                _chip(p.timed ? s.minutesLabel(p.timeMin!) : s.untimedLine),
                _chip('${s.patternPass} ${p.cutoff}/${p.fullTotal}'),
                _chip(p.negRate > 0
                    ? s.negPctLine((p.negRate * 100).round())
                    : s.negNoneLine,),
              ],
            ),
            const SizedBox(height: AppSpacing.s4),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                style: FilledButton.styleFrom(
                  minimumSize: const Size(0, AppSpacing.minTap),
                ),
                onPressed: () {
                  Navigator.of(ctx).pop();
                  _startMock(e.exam);
                },
                child: Text(s.startMockBtn),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;
    return AppScaffold(
      title: s.navMock,
      currentIndex: widget.navIndex,
      onNav: widget.onNav,
      body: FutureBuilder<List<_MockEntry>>(
        future: _entriesFuture,
        builder: (context, snap) {
          if (!snap.hasData) {
            return Center(
              child: CircularProgressIndicator(color: AppColors.of(context).accent),
            );
          }
          final entries = snap.data!;
          final query = _query;
          final matches = query.isEmpty
              ? entries
              : entries.where((e) => examMatchesQuery(e.exam, query)).toList();
          // Grouped view reuses the Practice picker's categories so both
          // tabs organise exams the same way.
          final grouped = <String, List<_MockEntry>>{};
          for (final e in entries) {
            grouped.putIfAbsent(categoryIdForExam(e.exam), () => []).add(e);
          }
          final groups = [
            for (final c in examCategories)
              if (grouped.containsKey(c.id)) (c, grouped[c.id]!),
          ];
          return ListView(
            padding: const EdgeInsets.all(AppSpacing.s4),
            children: [
              TextField(
                controller: _searchCtrl,
                decoration: InputDecoration(
                  hintText: s.searchExamsHint,
                  prefixIcon: const Icon(Icons.search),
                  suffixIcon: _query.isEmpty
                      ? null
                      : IconButton(
                          tooltip: s.clearSearch,
                          icon: const Icon(Icons.clear),
                          onPressed: () {
                            _searchCtrl.clear();
                            setState(() => _query = '');
                          },
                        ),
                  border: OutlineInputBorder(
                    borderRadius: AppRadius.mdAll,
                  ),
                ),
                textInputAction: TextInputAction.search,
                onChanged: (v) => setState(() => _query = v),
              ),
              const SizedBox(height: AppSpacing.s4),
              if (query.isNotEmpty && matches.isEmpty)
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: AppSpacing.s4),
                  child: Text(
                    s.noExamsFound,
                    style: AppType.small.copyWith(color: AppColors.of(context).muted),
                  ),
                ),
              if (query.isNotEmpty && matches.isNotEmpty)
                ...matches.map((e) => Padding(
                      padding: const EdgeInsets.only(bottom: AppSpacing.s2),
                      child: _mockRow(e, ne, s),
                    ),),
              if (query.isEmpty)
                ...groups.map((g) {
                  final (cat, list) = g;
                  final expanded = _expanded.contains(cat.id);
                  return Padding(
                    padding: const EdgeInsets.only(bottom: AppSpacing.s2),
                    child: Card(
                      margin: EdgeInsets.zero,
                      child: ExpansionTile(
                        key: ValueKey('mock_${cat.id}_$expanded'),
                        title: Text(
                          '${cat.title(ne)}  ·  ${list.length}',
                          style: AppType.h3,
                        ),
                        initiallyExpanded: expanded,
                        onExpansionChanged: (v) => setState(() {
                          if (v) {
                            _expanded.add(cat.id);
                          } else {
                            _expanded.remove(cat.id);
                          }
                        }),
                        children: [
                          for (final e in list)
                            Padding(
                              padding: const EdgeInsets.fromLTRB(AppSpacing.s3,
                                  0, AppSpacing.s3, AppSpacing.s2,),
                              child: _mockRow(e, ne, s),
                            ),
                        ],
                      ),
                    ),
                  );
                }),
            ],
          );
        },
      ),
    );
  }

  /// Compact mock row (v1.0.1): the old full card was ~230px each, so
  /// 33 mocks were ~10 screens of scrolling. One row per mock — name +
  /// one-line pattern summary + a small Start button — is ~72px. Tap
  /// the row for the full pattern detail sheet; Start jumps straight
  /// into the mock.
  Widget _mockRow(_MockEntry e, bool ne, AppStrings s) {
    return Card(
      margin: EdgeInsets.zero,
      child: InkWell(
        borderRadius: AppRadius.mdAll,
        onTap: () => _showDetails(e, ne),
        child: Padding(
          padding: const EdgeInsets.symmetric(
            horizontal: AppSpacing.s4,
            vertical: AppSpacing.s3,
          ),
          child: Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      e.exam.title(ne),
                      style: AppType.h3,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 2),
                    Text(
                      _metaLine(e.spec, s),
                      style: AppType.small.copyWith(color: AppColors.of(context).muted),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              const SizedBox(width: AppSpacing.s3),
              FilledButton(
                style: FilledButton.styleFrom(
                  minimumSize: const Size(0, 40),
                  padding:
                      const EdgeInsets.symmetric(horizontal: AppSpacing.s4),
                  visualDensity: VisualDensity.compact,
                ),
                onPressed: () => _startMock(e.exam),
                child: Text(s.startQuiz),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _chip(String label) => Chip(
        label: Text(label, style: AppType.small),
        visualDensity: VisualDensity.compact,
      );
}

class _MockEntry {
  final Exam exam;
  final MockSpec spec;
  _MockEntry({required this.exam, required this.spec});
}
