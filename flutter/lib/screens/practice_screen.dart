import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../data/data_repository.dart';
import '../engine/exam_categories.dart';
import '../engine/quiz_engine.dart';
import '../l10n/quiz_strings.dart';
import '../models/models.dart';
import '../theme/app_theme.dart';
import '../widgets/app_scaffold.dart';
import 'quiz/quiz_screen.dart';

/// Practice setup: exam picker -> topic picker -> difficulty/count -> start.
/// Phase 1 ends at "start" (the quiz runner is Phase 2); it reports the
/// chosen config via [onStart] so wiring is ready.
class PracticeScreen extends StatefulWidget {
  final int navIndex;
  final ValueChanged<int> onNav;
  final Exam? initialExam;

  /// Pre-selected single topic (deep-links: "Practice this chapter",
  /// "Practice weakest topic"). Applied after topics load.
  final String? initialTopic;
  final void Function(PracticeConfig config) onStart;

  const PracticeScreen({
    super.key,
    required this.navIndex,
    required this.onNav,
    this.initialExam,
    this.initialTopic,
    required this.onStart,
  });

  @override
  State<PracticeScreen> createState() => _PracticeScreenState();
}

class PracticeConfig {
  final Exam exam;
  final List<String> topics;
  final String difficulty; // mixed | easy | medium | hard
  final int count;
  final bool timerOn;
  final bool negativeOn;
  const PracticeConfig({
    required this.exam,
    required this.topics,
    required this.difficulty,
    required this.count,
    this.timerOn = false,
    this.negativeOn = true,
  });
}

class _PracticeScreenState extends State<PracticeScreen> {
  late final Future<List<Exam>> _examsFuture;
  Exam? _exam;
  final Set<String> _topics = {};
  String _difficulty = 'mixed';
  int _count = 10;
  Map<String, int> _topicCounts = {};
  bool _topicsLoading = false;
  bool _timerOn = false;
  bool _negOn = true;
  Map<String, dynamic>? _prelim; // this exam's prelim table, if any

  // Exam-picker organisation (v1.0.1): 47 exams as one flat chip list
  // meant endless scrolling. The picker is now search + collapsible
  // category sections + a "Recent" row, so every exam is ≤2 taps away
  // and the initial view fits on one screen.
  final _searchCtrl = TextEditingController();
  String _query = '';
  final Set<String> _expanded = {};
  List<String> _recentIds = [];
  static const _kRecentKey = 'loksewa_recent_exams_v1';
  static const _kRecentMax = 4;

  // Full-bank index: topic counts without parsing 73MB of JSON.
  // (Phase 1 shipped one sample file; the index now covers all 131.)
  @override
  void initState() {
    super.initState();
    _examsFuture = DataRepository().exams();
    _exam = widget.initialExam;
    if (_exam != null) {
      _expanded.add(categoryIdForExam(_exam!));
      _loadTopics();
    }
    _loadRecent();
  }

  @override
  void dispose() {
    _searchCtrl.dispose();
    super.dispose();
  }

  Future<void> _loadRecent() async {
    final prefs = await SharedPreferences.getInstance();
    if (!mounted) return;
    setState(() => _recentIds = prefs.getStringList(_kRecentKey) ?? []);
  }

  Future<void> _saveRecent(String id) async {
    final next =
        [id, ..._recentIds.where((e) => e != id)].take(_kRecentMax).toList();
    setState(() => _recentIds = next);
    final prefs = await SharedPreferences.getInstance();
    await prefs.setStringList(_kRecentKey, next);
  }

  Future<void> _loadTopics() async {
    if (_exam == null) return;
    setState(() => _topicsLoading = true);
    final repo = DataRepository();
    final counts = await repo.topicCountsFor(_exam!.id);
    final prelim = await _prelimFor(_exam!.id);
    if (!mounted) return;
    setState(() {
      _topicCounts = counts;
      _topicsLoading = false;
      _prelim = prelim;
      final t = widget.initialTopic;
      if (t != null && counts.containsKey(t)) _topics.add(t);
    });
  }

  /// This exam's prelim row from assets/data/exams.json (null when the
  /// exam has no MCQ prelim). Vanilla: cutoffFor / mockNegRate / timer
  /// pace all read this table.
  Future<Map<String, dynamic>?> _prelimFor(String examId) async {
    try {
      final rows = await DataRepository().examRows();
      for (final m in rows) {
        if (m['id'] == examId) {
          final p = m['prelim'];
          return p == null ? null : Map<String, dynamic>.from(p as Map);
        }
      }
    } catch (_) {}
    return null;
  }

  /// Vanilla `mockNegRate`: null/0 = no deduction; otherwise the stored
  /// rate (0.2 on PSC entries, 0.25 on MECEE-BL). No prelim → 0.2 default.
  double _examNegRate() {
    final p = _prelim;
    if (p == null) return 0.2;
    final neg = p['negative'] as num?;
    if (neg == null || neg == 0) return 0;
    return neg.toDouble();
  }

  Question _withMarks(Question q, int marks) => Question(
        id: q.id,
        exam: q.exam,
        topic: q.topic,
        subtopic: q.subtopic,
        difficulty: q.difficulty,
        marks: marks,
        question: q.question,
        questionNe: q.questionNe,
        options: q.options,
        optionsNe: q.optionsNe,
        answer: q.answer,
        explanation: q.explanation,
        explanationNe: q.explanationNe,
        source: q.source,
      );

  /// Build the QuizConfig from the setup (vanilla `startPractice` logic)
  /// and push the QuizScreen — replaces the Phase 1 onStart snackbar.
  Future<void> _startQuiz() async {
    final exam = _exam;
    if (exam == null) return;
    final s = AppStateScope.of(context).strings;
    final repo = DataRepository();
    final pool = await repo.questionsForExam(
      exam.id,
      topics: _topics.isEmpty ? null : _topics,
      difficulty: _difficulty,
    );
    if (!mounted) return;
    if (pool.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(s.noMatch(exam.title(s.isNe)))),
      );
      return;
    }
    final prelim = _prelim;
    final examNeg = _examNegRate();
    final marksPerQ = prelim?['marksPerQ'] as num?;
    final picked = (pool.toList()..shuffle())
        .take(_count)
        .map(
          (q) => marksPerQ != null ? _withMarks(q, marksPerQ.toInt()) : q,
        )
        .toList();
    // Timer pace: prelim.timeMin spread over the full paper, else 54s/Q.
    final perQSecs = (prelim != null &&
            prelim['timeMin'] != null &&
            prelim['questions'] != null)
        ? ((prelim['timeMin'] as num) * 60 / (prelim['questions'] as num))
            .round()
        : 54;
    final negOn = _negOn && examNeg > 0;
    final config = QuizConfig(
      questions: picked,
      negOn: negOn,
      negRate: _negOn ? examNeg : 0,
      timerOn: _timerOn,
      timeLimitSecs: _timerOn ? picked.length * perQSecs : null,
      mode: 'practice',
      examId: exam.id,
    );
    final pass = (prelim?['pass'] as num?)?.toInt() ?? 45;
    final total = (prelim?['total'] as num?)?.toInt() ?? 100;
    final meta = QuizMeta(
      examName: exam.title(s.isNe),
      cutoff: pass,
      cutoffPct: prelim != null
          ? ((prelim['pass'] as num) / (prelim['total'] as num) * 100).round()
          : 45,
      fullTotal: total,
    );
    if (!mounted) return;
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => QuizScreen(config: config, meta: meta, bank: pool),
      ),
    );
  }

  void _pickExam(Exam e) {
    setState(() {
      _exam = e;
      _topics.clear();
      // Keep the picked exam's section open so the selection stays
      // visible when the search is cleared.
      _expanded.add(categoryIdForExam(e));
    });
    _saveRecent(e.id);
    _loadTopics();
  }

  Widget _examChips(List<Exam> exams, bool ne) => Wrap(
        spacing: AppSpacing.s2,
        runSpacing: AppSpacing.s2,
        children: exams
            .map(
              (e) => _ExamChip(
                exam: e,
                selected: _exam?.id == e.id,
                ne: ne,
                onTap: () => _pickExam(e),
              ),
            )
            .toList(),
      );

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;
    return AppScaffold(
      title: s.practiceTitle,
      currentIndex: widget.navIndex,
      onNav: widget.onNav,
      body: FutureBuilder<List<Exam>>(
        future: _examsFuture,
        builder: (context, snap) {
          if (!snap.hasData) {
            return Center(
              child: CircularProgressIndicator(color: AppColors.of(context).accent),
            );
          }
          final exams = snap.data!;
          final query = _query;
          final byId = {for (final e in exams) e.id: e};
          final recent = [
            for (final id in _recentIds)
              if (byId[id] != null) byId[id]!,
          ];
          final matches = query.isEmpty
              ? exams
              : exams.where((e) => examMatchesQuery(e, query)).toList();
          final groups = groupExams(exams);
          return ListView(
            padding: const EdgeInsets.all(AppSpacing.s4),
            children: [
              Text(s.chooseExam, style: AppType.h2),
              const SizedBox(height: AppSpacing.s3),
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
              if (query.isEmpty && recent.isNotEmpty) ...[
                const SizedBox(height: AppSpacing.s4),
                Text(s.recentExams, style: AppType.h3),
                const SizedBox(height: AppSpacing.s2),
                _examChips(recent, ne),
              ],
              const SizedBox(height: AppSpacing.s4),
              if (query.isNotEmpty)
                matches.isEmpty
                    ? Padding(
                        padding:
                            const EdgeInsets.symmetric(vertical: AppSpacing.s4),
                        child: Text(
                          s.noExamsFound,
                          style: AppType.small.copyWith(color: AppColors.of(context).muted),
                        ),
                      )
                    : _examChips(matches, ne)
              else
                ...groups.map((g) {
                  final (cat, list) = g;
                  final expanded = _expanded.contains(cat.id);
                  return Padding(
                    padding: const EdgeInsets.only(bottom: AppSpacing.s2),
                    child: Card(
                      margin: EdgeInsets.zero,
                      child: ExpansionTile(
                        // Key includes the expanded flag so a programmatic
                        // expand (picking from search / deep-link) rebuilds
                        // the tile open; user taps toggle via the callback.
                        key: ValueKey('cat_${cat.id}_$expanded'),
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
                          Padding(
                            padding: const EdgeInsets.fromLTRB(
                                AppSpacing.s4, 0, AppSpacing.s4, AppSpacing.s4,),
                            child: _examChips(list, ne),
                          ),
                        ],
                      ),
                    ),
                  );
                }),
              if (_exam != null) ...[
                const SizedBox(height: AppSpacing.s6),
                Text(s.chooseTopics, style: AppType.h2),
                const SizedBox(height: AppSpacing.s3),
                if (_topicsLoading)
                  LinearProgressIndicator(color: AppColors.of(context).accent)
                else if (_topicCounts.isEmpty)
                  Text(
                    s.loadingQuestions,
                    style: AppType.small.copyWith(color: AppColors.of(context).muted),
                  )
                else
                  Wrap(
                    spacing: AppSpacing.s2,
                    runSpacing: AppSpacing.s2,
                    children: _topicCounts.entries.map((en) {
                      final selected = _topics.contains(en.key);
                      return FilterChip(
                        selected: selected,
                        label: Text('${en.key} (${en.value})'),
                        onSelected: (_) => setState(() {
                          selected
                              ? _topics.remove(en.key)
                              : _topics.add(en.key);
                        }),
                      );
                    }).toList(),
                  ),
                const SizedBox(height: AppSpacing.s6),
                Text(s.chooseDifficulty, style: AppType.h2),
                const SizedBox(height: AppSpacing.s3),
                SegmentedButton<String>(
                  segments: [
                    ButtonSegment(value: 'mixed', label: Text(s.diffMixed)),
                    ButtonSegment(value: 'easy', label: Text(s.diffEasy)),
                    ButtonSegment(value: 'medium', label: Text(s.diffMedium)),
                    ButtonSegment(value: 'hard', label: Text(s.diffHard)),
                  ],
                  selected: {_difficulty},
                  onSelectionChanged: (v) =>
                      setState(() => _difficulty = v.first),
                ),
                const SizedBox(height: AppSpacing.s6),
                Text(s.chooseCount, style: AppType.h2),
                const SizedBox(height: AppSpacing.s3),
                SegmentedButton<int>(
                  segments: const [
                    ButtonSegment(value: 5, label: Text('5')),
                    ButtonSegment(value: 10, label: Text('10')),
                    ButtonSegment(value: 20, label: Text('20')),
                    ButtonSegment(value: 50, label: Text('50')),
                  ],
                  selected: {_count},
                  onSelectionChanged: (v) => setState(() => _count = v.first),
                ),
                const SizedBox(height: AppSpacing.s4),
                SwitchListTile(
                  value: _timerOn,
                  onChanged: (v) => setState(() => _timerOn = v),
                  title: Text(s.timerLabel),
                  subtitle: Text(s.timerHint),
                  contentPadding: EdgeInsets.zero,
                ),
                SwitchListTile(
                  value: _examNegRate() > 0 && _negOn,
                  onChanged: _examNegRate() > 0
                      ? (v) => setState(() => _negOn = v)
                      : null,
                  title: Text(s.negativeLabel),
                  subtitle: Text(
                    _examNegRate() > 0
                        ? s.negativeHint(
                            (_examNegRate() * 100).round().toString(),
                          )
                        : s.negOffLine,
                  ),
                  contentPadding: EdgeInsets.zero,
                ),
                const SizedBox(height: AppSpacing.s8),
                FilledButton(
                  onPressed: _topics.isEmpty ? null : _startQuiz,
                  style: FilledButton.styleFrom(
                    backgroundColor: AppColors.of(context).accent,
                    foregroundColor: AppColors.of(context).accentInk,
                    minimumSize: const Size(double.infinity, 56),
                    textStyle: AppType.h3,
                  ),
                  child: Text(s.startQuiz),
                ),
                const SizedBox(height: AppSpacing.s12),
              ],
            ],
          );
        },
      ),
    );
  }
}

class _ExamChip extends StatelessWidget {
  final Exam exam;
  final bool selected;
  final bool ne;
  final VoidCallback onTap;
  const _ExamChip({
    required this.exam,
    required this.selected,
    required this.ne,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    // Long names (e.g. "Deputy Secretary / Joint Secretary …") were
    // hard-clipped mid-word in v1.0.0. Cap the label width so the text
    // wraps onto a second line instead.
    final maxLabelWidth =
        MediaQuery.of(context).size.width - AppSpacing.s4 * 2 - 40;
    return ChoiceChip(
      label: ConstrainedBox(
        constraints: BoxConstraints(maxWidth: maxLabelWidth),
        child: Text(
          exam.title(ne),
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
          softWrap: true,
        ),
      ),
      selected: selected,
      onSelected: (_) => onTap(),
      selectedColor: AppColors.of(context).accentSoft,
      side: BorderSide(
        color: selected ? AppColors.of(context).accent : AppColors.of(context).borderSoft,
      ),
    );
  }
}
