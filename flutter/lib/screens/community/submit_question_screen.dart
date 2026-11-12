import 'package:flutter/material.dart';

import '../../l10n/app_strings.dart';
import '../../l10n/community_strings.dart';
import '../../state/community_store.dart';
import '../../widgets/app_scaffold.dart';
import '../../data/data_repository.dart';

/// Submit-a-Question (Milestone 6) — matches the vanilla site's Contribute view:
/// full bilingual form, vanilla `validateSubmission` checks, automatic spam
/// guards (duplicate, 3-identical-in-queue, double-submit, 5/hour rate limit).
///
/// First-time submissions NEVER go live instantly — accepted entries land in
/// the review queue (tab below) with status 'pending'. The queue tab is the
/// local-preview stand-in for the maintainer (approve/reject), exactly like
/// vanilla's moderation preview view; storage keys are vanilla-identical
/// (`loksewa_submissions_v1`, `loksewa_community_approved_v1`).
/// Route name for integration: [SubmitQuestionScreen.routeName].
class SubmitQuestionScreen extends StatefulWidget {
  static const routeName = '/community/submit';

  final CommunityStore store;
  final int navIndex;
  final ValueChanged<int> onNav;

  const SubmitQuestionScreen({
    super.key,
    required this.store,
    required this.navIndex,
    required this.onNav,
  });

  @override
  State<SubmitQuestionScreen> createState() => _SubmitQuestionScreenState();
}

class _SubmitQuestionScreenState extends State<SubmitQuestionScreen>
    with SingleTickerProviderStateMixin {
  late final TabController _tabs;

  // form controllers
  final _topic = TextEditingController();
  final _subtopic = TextEditingController();
  final _qEn = TextEditingController();
  final _qNe = TextEditingController();
  final _optEn = List.generate(4, (_) => TextEditingController());
  final _optNe = List.generate(4, (_) => TextEditingController());
  final _explEn = TextEditingController();
  final _explNe = TextEditingController();
  final _source = TextEditingController();

  String _exam = '';
  String _difficulty = 'medium';
  int _marks = 2;
  int _answer = -1;
  List<String> _errors = [];
  String? _blocked;
  bool _done = false;
  bool _submitDisabled =
      false; // vanilla: disabled after submit until form changes
  List<String> _examIds = const [];

  final _reasonCtrls = <String, TextEditingController>{};
  TextEditingController _reasonCtrl(String id) =>
      _reasonCtrls.putIfAbsent(id, TextEditingController.new);

  @override
  void initState() {
    super.initState();
    _tabs = TabController(length: 2, vsync: this);
    widget.store.init();
    DataRepository().exams().then((exams) {
      if (!mounted) return;
      setState(() {
        _examIds = exams.map((e) => e.id).toList();
        if (_examIds.isNotEmpty) _exam = _examIds.first;
      });
    }).catchError((_) {});
    // Vanilla: any edit re-enables the submit button.
    void reenable() {
      if (_submitDisabled) setState(() => _submitDisabled = false);
    }

    for (final c in [
      _topic,
      _subtopic,
      _qEn,
      _qNe,
      ..._optEn,
      ..._optNe,
      _explEn,
      _explNe,
      _source,
    ]) {
      c.addListener(reenable);
    }
  }

  @override
  void dispose() {
    _tabs.dispose();
    _topic.dispose();
    _subtopic.dispose();
    _qEn.dispose();
    _qNe.dispose();
    for (final c in [..._optEn, ..._optNe]) {
      c.dispose();
    }
    for (final c in _reasonCtrls.values) {
      c.dispose();
    }
    _explEn.dispose();
    _explNe.dispose();
    _source.dispose();
    super.dispose();
  }

  Map<String, dynamic> _formMap() => {
        'exam': _exam,
        'topic': _topic.text,
        'subtopic': _subtopic.text,
        'difficulty': _difficulty,
        'marks': _marks,
        'question': _qEn.text,
        'question_ne': _qNe.text,
        'options': _optEn.map((c) => c.text).toList(),
        'options_ne': _optNe.map((c) => c.text).toList(),
        'answer': _answer < 0 ? null : _answer,
        'explanation': _explEn.text,
        'explanation_ne': _explNe.text,
        'source': _source.text,
      };

  Future<void> _submit() async {
    final s = AppStateScope.of(context).strings;
    final outcome = await widget.store.submitQuestion(
      _formMap(),
      nepali: s.isNe,
    );
    if (!mounted) return;
    setState(() {
      _errors = outcome.errors;
      _blocked = outcome.blockedMessage;
      _done = outcome.ok;
      _submitDisabled = outcome.ok; // vanilla double-submit guard
      if (outcome.ok) _tabs.animateTo(1); // show the queue: pending, not live
    });
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    return AppScaffold(
      title: s.submitTitle,
      currentIndex: widget.navIndex,
      onNav: widget.onNav,
      body: Column(
        children: [
          TabBar(
            controller: _tabs,
            tabs: [
              Tab(text: s.submitTitle),
              Tab(text: s.reviewQueueTitle),
            ],
          ),
          Expanded(
            child: ListenableBuilder(
              listenable: widget.store,
              builder: (context, _) => TabBarView(
                controller: _tabs,
                children: [_formTab(s), _queueTab(s)],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ---------------- form tab ----------------

  Widget _formTab(AppStrings s) => ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            color: Colors.amber.shade900.withValues(alpha: 0.25),
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Text.rich(
                TextSpan(
                  children: [
                    TextSpan(
                      text: '${s.reviewBannerTitle} ',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    TextSpan(text: s.reviewBannerBody),
                  ],
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Text(
              _countsLine(s),
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Text(
                s.safetyNote,
                style: Theme.of(context).textTheme.bodySmall,
              ),
            ),
          ),
          const SizedBox(height: 8),
          _label(s.fExam),
          DropdownButtonFormField<String>(
            initialValue: _examIds.contains(_exam) ? _exam : null,
            items: _examIds
                .map((e) => DropdownMenuItem(value: e, child: Text(e)))
                .toList(),
            onChanged: (v) {
              setState(() => _exam = v ?? '');
              if (_submitDisabled) setState(() => _submitDisabled = false);
            },
          ),
          _field(_topic, s.fTopic),
          _field(_subtopic, s.fSubtopic),
          _label(s.fDifficulty),
          DropdownButtonFormField<String>(
            initialValue: _difficulty,
            items: const [
              'easy',
              'medium',
              'hard',
            ].map((d) => DropdownMenuItem(value: d, child: Text(d))).toList(),
            onChanged: (v) {
              setState(() => _difficulty = v ?? 'medium');
              if (_submitDisabled) setState(() => _submitDisabled = false);
            },
          ),
          _label(s.fMarks),
          DropdownButtonFormField<int>(
            initialValue: _marks,
            items: const [
              2,
              1,
            ]
                .map((m) => DropdownMenuItem(value: m, child: Text('$m')))
                .toList(),
            onChanged: (v) {
              setState(() => _marks = v ?? 2);
              if (_submitDisabled) setState(() => _submitDisabled = false);
            },
          ),
          _field(_qEn, s.fQuestionEn, maxLines: 3),
          _field(_qNe, s.fQuestionNe, maxLines: 3),
          _label(s.fOptionsEn),
          ...List.generate(
            4,
            (i) => Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: TextField(
                controller: _optEn[i],
                decoration: InputDecoration(
                  labelText: s.optionPh(String.fromCharCode(65 + i), s.isNe),
                ),
              ),
            ),
          ),
          _label(s.fOptionsNe),
          ...List.generate(
            4,
            (i) => Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: TextField(
                controller: _optNe[i],
                decoration: InputDecoration(
                  labelText: s.optionPh(String.fromCharCode(65 + i), s.isNe),
                ),
              ),
            ),
          ),
          _label(s.fAnswer),
          DropdownButtonFormField<int>(
            initialValue: _answer < 0 ? null : _answer,
            decoration: InputDecoration(hintText: s.fAnswerChoose),
            items: List.generate(
              4,
              (i) => DropdownMenuItem(
                value: i,
                child: Text(String.fromCharCode(65 + i)),
              ),
            ),
            onChanged: (v) {
              setState(() => _answer = v ?? -1);
              if (_submitDisabled) setState(() => _submitDisabled = false);
            },
          ),
          _field(_explEn, s.fExplanationEn, maxLines: 2),
          _field(_explNe, s.fExplanationNe, maxLines: 2),
          _field(_source, s.fSource),
          _label(s.fContributor),
          Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Text(
              widget.store.authorName,
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Text.rich(
                TextSpan(
                  children: [
                    const TextSpan(
                      text: 'CAPTCHA — ',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    TextSpan(
                      text: s.captchaNote,
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                  ],
                ),
              ),
            ),
          ),
          if (_errors.isNotEmpty) ...[
            const SizedBox(height: 8),
            Text(
              s.fixTheseInline,
              style: TextStyle(color: Theme.of(context).colorScheme.error),
            ),
            ..._errors.map(
              (e) => Text(
                '• $e',
                style: TextStyle(color: Theme.of(context).colorScheme.error),
              ),
            ),
          ],
          if (_blocked != null) ...[
            const SizedBox(height: 8),
            Text(
              _blocked!,
              style: TextStyle(color: Theme.of(context).colorScheme.error),
            ),
          ],
          if (_done) ...[
            const SizedBox(height: 8),
            Text(
              '✓ ${s.submitDone}',
              style: const TextStyle(color: Colors.green),
            ),
          ],
          const SizedBox(height: 8),
          FilledButton(
            onPressed: _submitDisabled ? null : _submit,
            child: Text(s.submitForReview),
          ),
          const SizedBox(height: 4),
          Text(
            '${s.submittingAs}: ${widget.store.authorName}',
            style: Theme.of(context).textTheme.bodySmall,
          ),
        ],
      );

  Widget _label(String text) => Padding(
        padding: const EdgeInsets.only(top: 12, bottom: 4),
        child: Text(text, style: const TextStyle(fontWeight: FontWeight.w600)),
      );

  Widget _field(TextEditingController c, String label, {int maxLines = 1}) =>
      Padding(
        padding: const EdgeInsets.only(bottom: 8),
        child: TextField(
          controller: c,
          maxLines: maxLines,
          decoration: InputDecoration(labelText: label),
        ),
      );

  String _countsLine(AppStrings s) {
    final c = widget.store.submissionCounts();
    return s.modLogLine(c['approved']!, c['rejected']!, c['pending']!);
  }

  // ---------------- review queue tab ----------------

  Widget _queueTab(AppStrings s) {
    final pending = widget.store.pendingSubmissions;
    final counts = widget.store.submissionCounts();
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Text(
              s.queuePreviewNote,
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 8),
          child: Text(
            s.modLogLine(
              counts['approved']!,
              counts['rejected']!,
              counts['pending']!,
            ),
          ),
        ),
        Text(
          '${s.mySubmissionsTitle} (${pending.length})',
          style: Theme.of(context).textTheme.titleMedium,
        ),
        const SizedBox(height: 8),
        if (pending.isEmpty)
          Card(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  const Text('📥', style: TextStyle(fontSize: 40)),
                  Text(
                    s.noPending,
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  Text(s.noPendingBlurb, textAlign: TextAlign.center),
                ],
              ),
            ),
          ),
        ...pending.map((sub) => _queueCard(s, sub)),
        const SizedBox(height: 16),
        Text(
          s.mySubmissionsTitle,
          style: Theme.of(context).textTheme.titleMedium,
        ),
        ...widget.store.submissions
            .where((x) => x['status'] != 'pending')
            .map((sub) => _historyCard(s, sub)),
      ],
    );
  }

  Widget _queueCard(AppStrings s, Map<String, dynamic> sub) {
    final id = sub['id'] as String;
    final reasonCtrl = _reasonCtrl(id);
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '$id · ${sub['contributor'] ?? 'anonymous'} · ${(sub['submittedAt'] != null ? DateTime.fromMillisecondsSinceEpoch((sub['submittedAt'] as num).toInt()).toIso8601String() : '').substring(0, 10)} · ${sub['exam']} · ${sub['topic']} · ${sub['difficulty']} · ${sub['marks']}',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 4),
            Text(
              sub['question'] ?? '',
              style: Theme.of(context).textTheme.titleSmall,
            ),
            Text(
              sub['question_ne'] ?? '',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            Text(
              '${s.fAnswer}: ${String.fromCharCode(65 + ((sub['answer'] ?? 0) as int))}',
            ),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                FilledButton.icon(
                  icon: const Text('✓'),
                  label: Text(s.approveBtn),
                  style: FilledButton.styleFrom(
                    backgroundColor: Colors.green.shade700,
                  ),
                  onPressed: () async {
                    await widget.store.approveSubmission(id);
                    if (mounted) setState(() {});
                  },
                ),
                SizedBox(
                  width: 220,
                  child: TextField(
                    controller: reasonCtrl,
                    decoration: InputDecoration(
                      hintText: s.rejectReasonPh,
                      isDense: true,
                    ),
                  ),
                ),
                OutlinedButton.icon(
                  icon: const Text('✕'),
                  label: Text(s.rejectBtn),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: Theme.of(context).colorScheme.error,
                  ),
                  onPressed: () async {
                    final ok = await widget.store.rejectSubmission(
                      id,
                      reasonCtrl.text,
                    );
                    if (!mounted) return;
                    if (!ok) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text(s.rejectReasonNeeded)),
                      );
                    } else {
                      setState(() {});
                    }
                  },
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _historyCard(AppStrings s, Map<String, dynamic> sub) {
    final approved = sub['status'] == 'approved';
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: ListTile(
        leading: Text(
          approved ? '✓' : '✕',
          style: TextStyle(
            color: approved ? Colors.green : Colors.red,
            fontSize: 20,
          ),
        ),
        title: Text(
          (sub['question'] ?? '').toString(),
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
        ),
        subtitle: Text(
          '${approved ? s.statusApproved : s.statusRejected}'
          '${sub['rejectReason'] != null ? ' — ${s.rejectReasonLine((sub['rejectReason']).toString())}' : ''}',
        ),
      ),
    );
  }
}
