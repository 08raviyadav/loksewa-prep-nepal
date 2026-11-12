import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;

import '../engine/mock_specs.dart';
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

  Future<List<_MockEntry>> _load() async {
    final raw = await rootBundle.loadString('assets/data/exams.json');
    final decoded = json.decode(raw);
    final list = decoded is List ? decoded : decoded['exams'] as List;
    final out = <_MockEntry>[];
    for (final e in list) {
      final m = Map<String, dynamic>.from(e as Map);
      final prelim = m['prelim'];
      if (prelim == null) continue;
      final spec = MockSpec.fromPrelim(
        m['id'] as String,
        Map<String, dynamic>.from(prelim as Map),
      );
      out.add(_MockEntry(exam: Exam.fromJson(m), spec: spec));
    }
    return out;
  }

  void _startMock(Exam exam) {
    Navigator.of(
      context,
    ).push(MaterialPageRoute(builder: (_) => MockExamScreen(examId: exam.id)));
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
            return const Center(
              child: CircularProgressIndicator(color: AppColors.accent),
            );
          }
          final entries = snap.data!;
          return ListView.separated(
            padding: const EdgeInsets.all(AppSpacing.s4),
            itemCount: entries.length,
            separatorBuilder: (_, __) => const SizedBox(height: AppSpacing.s3),
            itemBuilder: (context, i) {
              final e = entries[i];
              final p = e.spec;
              return Card(
                child: InkWell(
                  borderRadius: AppRadius.mdAll,
                  onTap: () => _startMock(e.exam),
                  child: Padding(
                    padding: const EdgeInsets.all(AppSpacing.s4),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(e.exam.title(ne), style: AppType.h3),
                        const SizedBox(height: AppSpacing.s2),
                        Wrap(
                          spacing: AppSpacing.s2,
                          runSpacing: AppSpacing.s2,
                          children: [
                            _chip('${p.questionCount} ${s.patternQuestions}'),
                            _chip(
                              p.timed
                                  ? s.minutesLabel(p.timeMin!)
                                  : s.untimedLine,
                            ),
                            _chip(
                              '${s.patternPass} ${p.cutoff}/${p.fullTotal}',
                            ),
                            _chip(
                              p.negRate > 0
                                  ? s.negPctLine((p.negRate * 100).round())
                                  : s.negNoneLine,
                            ),
                          ],
                        ),
                        const SizedBox(height: AppSpacing.s3),
                        SizedBox(
                          width: double.infinity,
                          child: FilledButton(
                            style: FilledButton.styleFrom(
                              minimumSize: const Size(0, AppSpacing.minTap),
                            ),
                            onPressed: () => _startMock(e.exam),
                            child: Text(s.startMockBtn),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          );
        },
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
