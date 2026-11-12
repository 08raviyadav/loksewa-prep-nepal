import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;

import '../data/data_repository.dart';
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

  // Full-bank index: topic counts without parsing 73MB of JSON.
  // (Phase 1 shipped one sample file; the index now covers all 131.)
  @override
  void initState() {
    super.initState();
    _examsFuture = DataRepository().exams();
    _exam = widget.initialExam;
    if (_exam != null) _loadTopics();
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
      final raw = await rootBundle.loadString('assets/data/exams.json');
      final decoded = json.decode(raw);
      final list = decoded is List ? decoded : decoded['exams'] as List;
      for (final e in list) {
        final m = Map<String, dynamic>.from(e as Map);
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
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(s.noMatch(exam.title(s.isNe)))));
      return;
    }
    final prelim = _prelim;
    final examNeg = _examNegRate();
    final marksPerQ = prelim?['marksPerQ'] as num?;
    final picked = (pool.toList()..shuffle())
        .take(_count)
        .map((q) => marksPerQ != null ? _withMarks(q, marksPerQ.toInt()) : q)
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
    });
    _loadTopics();
  }

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
            return const Center(
              child: CircularProgressIndicator(color: AppColors.accent),
            );
          }
          final exams = snap.data!;
          return ListView(
            padding: const EdgeInsets.all(AppSpacing.s4),
            children: [
              Text(s.chooseExam, style: AppType.h2),
              const SizedBox(height: AppSpacing.s3),
              Wrap(
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
              ),
              if (_exam != null) ...[
                const SizedBox(height: AppSpacing.s6),
                Text(s.chooseTopics, style: AppType.h2),
                const SizedBox(height: AppSpacing.s3),
                if (_topicsLoading)
                  const LinearProgressIndicator(color: AppColors.accent)
                else if (_topicCounts.isEmpty)
                  Text(
                    s.loadingQuestions,
                    style: AppType.small.copyWith(color: AppColors.muted),
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
                    backgroundColor: AppColors.accent,
                    foregroundColor: AppColors.accentInk,
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
    return ChoiceChip(
      label: Text(exam.title(ne)),
      selected: selected,
      onSelected: (_) => onTap(),
      selectedColor: AppColors.accentSoft,
      side: BorderSide(
        color: selected ? AppColors.accent : AppColors.borderSoft,
      ),
    );
  }
}
