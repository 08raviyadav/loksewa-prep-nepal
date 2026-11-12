import 'package:flutter/material.dart';

import '../../l10n/app_strings.dart';
import '../../l10n/community_strings.dart';
import '../../state/community_store.dart';
import '../../widgets/app_scaffold.dart';
import '../../data/data_repository.dart';

/// Discussion Hub (Milestone 6) — matches the vanilla site's Discuss view:
/// threads {id, exam, title, body, author, createdAt, upvotes, replies[]},
/// new-thread form (title >= 8, body >= 10), reply form (body >= 2),
/// upvote (vanilla increments — NOT a toggle), report, all on-device with
/// the vanilla-identical key `loksewa_discussions_v1`.
/// Route name for integration: [DiscussionScreen.routeName].
class DiscussionScreen extends StatefulWidget {
  static const routeName = '/community/discussion';

  final CommunityStore store;
  final int navIndex;
  final ValueChanged<int> onNav;

  const DiscussionScreen({
    super.key,
    required this.store,
    required this.navIndex,
    required this.onNav,
  });

  @override
  State<DiscussionScreen> createState() => _DiscussionScreenState();
}

class _DiscussionScreenState extends State<DiscussionScreen> {
  final _titleCtrl = TextEditingController();
  final _bodyCtrl = TextEditingController();
  final _replyCtrls = <String, TextEditingController>{};
  List<String> _formErrors = [];
  String _sort = 'new'; // 'new' | 'top'
  String _exam = 'general';
  List<String> _examIds = const ['general'];
  bool _submitted = false;

  @override
  void initState() {
    super.initState();
    widget.store.init();
    DataRepository().exams().then((exams) {
      if (!mounted) return;
      setState(() => _examIds = ['general', ...exams.map((e) => e.id)]);
    }).catchError((_) {});
  }

  @override
  void dispose() {
    _titleCtrl.dispose();
    _bodyCtrl.dispose();
    for (final c in _replyCtrls.values) {
      c.dispose();
    }
    super.dispose();
  }

  TextEditingController _replyCtrl(String id) =>
      _replyCtrls.putIfAbsent(id, TextEditingController.new);

  Future<void> _postThread() async {
    final s = AppStateScope.of(context).strings;
    final errors = await widget.store.addThread(
      exam: _exam,
      title: _titleCtrl.text,
      body: _bodyCtrl.text,
      nepali: s.isNe,
    );
    if (!mounted) return;
    setState(() {
      _formErrors = errors;
      _submitted = errors.isEmpty;
    });
    if (errors.isEmpty) {
      _titleCtrl.clear();
      _bodyCtrl.clear();
    }
  }

  Future<void> _postReply(String threadId) async {
    final s = AppStateScope.of(context).strings;
    final ctrl = _replyCtrl(threadId);
    final err = await widget.store.addReply(threadId, ctrl.text, s.isNe);
    if (!mounted) return;
    if (err != null) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(err)));
    } else {
      ctrl.clear();
      setState(() {});
    }
  }

  Future<void> _report(String threadId, {int? replyIndex}) async {
    final s = AppStateScope.of(context).strings;
    final reasons = ['spam', 'wrong', 'abusive', 'other'];
    String chosen = 'spam';
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setDlg) => AlertDialog(
          title: Text(s.reportDialogTitle),
          content: RadioGroup<String>(
            groupValue: chosen,
            onChanged: (v) => setDlg(() => chosen = v ?? 'spam'),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(s.reportWhy),
                const SizedBox(height: 8),
                ...reasons.map(
                  (r) => RadioListTile<String>(
                    title: Text(s.reportReason(r)),
                    value: r,
                    dense: true,
                    contentPadding: EdgeInsets.zero,
                  ),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(ctx, false),
              child: Text(s.cancelBtn),
            ),
            FilledButton(
              onPressed: () => Navigator.pop(ctx, true),
              child: Text(s.submitBtn),
            ),
          ],
        ),
      ),
    );
    if (ok != true || !mounted) return;
    await widget.store.reportPost(threadId, chosen, replyIndex: replyIndex);
    if (!mounted) return;
    ScaffoldMessenger.of(context)
        .showSnackBar(SnackBar(content: Text(s.reportThanks)));
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    return AppScaffold(
      title: s.discussionTitle,
      currentIndex: widget.navIndex,
      onNav: widget.onNav,
      body: ListenableBuilder(
        listenable: widget.store,
        builder: (context, _) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _demoBanner(s),
            _newThreadCard(s),
            const SizedBox(height: 8),
            _sortRow(s),
            ...widget.store.threadsSorted(_sort).map(_threadCard),
            if (widget.store.loaded && widget.store.threads.isEmpty)
              _emptyState(s),
          ],
        ),
      ),
    );
  }

  Widget _demoBanner(AppStrings s) => Card(
        color: Theme.of(context).colorScheme.surfaceContainerHighest,
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Text.rich(
            TextSpan(
              children: [
                const TextSpan(
                  text: 'ℹ️ ',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                TextSpan(text: s.communityLocalPreview),
                const TextSpan(text: '\n'),
                TextSpan(text: s.postingAs(widget.store.authorName)),
              ],
            ),
          ),
        ),
      );

  Widget _newThreadCard(AppStrings s) => Card(
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                s.startThread,
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 8),
              DropdownButtonFormField<String>(
                initialValue: _exam,
                decoration: InputDecoration(labelText: s.examTopic),
                items: _examIds
                    .map(
                      (e) => DropdownMenuItem(
                        value: e,
                        child: Text(e == 'general' ? s.generalDoubts : e),
                      ),
                    )
                    .toList(),
                onChanged: (v) => setState(() => _exam = v ?? 'general'),
              ),
              const SizedBox(height: 8),
              TextField(
                controller: _titleCtrl,
                maxLength: 140,
                decoration: InputDecoration(labelText: s.threadTitleLabel),
              ),
              TextField(
                controller: _bodyCtrl,
                maxLines: 4,
                decoration: InputDecoration(labelText: s.threadBodyLabel),
              ),
              if (_formErrors.isNotEmpty) ...[
                const SizedBox(height: 8),
                ..._formErrors.map(
                  (e) => Text(
                    '• $e',
                    style:
                        TextStyle(color: Theme.of(context).colorScheme.error),
                  ),
                ),
              ],
              if (_submitted) ...[
                const SizedBox(height: 8),
                const Text('✓', style: TextStyle(color: Colors.green)),
              ],
              const SizedBox(height: 8),
              FilledButton(
                onPressed: _postThread,
                child: Text(s.postThreadBtn),
              ),
            ],
          ),
        ),
      );

  Widget _sortRow(AppStrings s) => Row(
        children: [
          Text(
            s.threadsCount(widget.store.threads.length),
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const Spacer(),
          SegmentedButton<String>(
            segments: [
              ButtonSegment(value: 'new', label: Text(s.sortNew)),
              ButtonSegment(value: 'top', label: Text(s.sortTop)),
            ],
            selected: {_sort},
            onSelectionChanged: (v) => setState(() => _sort = v.first),
          ),
        ],
      );

  Widget _threadCard(Map<String, dynamic> th) {
    final s = AppStateScope.of(context).strings;
    final replies = (th['replies'] as List).cast<Map<String, dynamic>>();
    final reports = ((th['reports'] as List?) ?? const []).length;
    final id = th['id'] as String;
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '${th['exam'] == 'general' ? s.generalDoubts : th['exam']} · ${s.byLabel} ${th['author']} · ${(th['createdAt'] ?? '').toString().substring(0, 10)}${reports > 0 ? ' · ⚑ $reports' : ''}',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 4),
            Text(
              th['title'] ?? '',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            Text(th['body'] ?? ''),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              children: [
                OutlinedButton.icon(
                  icon: const Text('▲'),
                  label: Text('${s.upvote} (${th['upvotes'] ?? 0})'),
                  onPressed: () => widget.store.upvoteThread(id),
                ),
                OutlinedButton.icon(
                  icon: const Text('⚑'),
                  label: Text(s.reportBtn),
                  onPressed: () => _report(id),
                ),
              ],
            ),
            ...replies.asMap().entries.map((e) {
              final i = e.key, r = e.value;
              return Container(
                margin: const EdgeInsets.only(top: 8),
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Theme.of(context)
                      .colorScheme
                      .surfaceContainerHighest
                      .withValues(alpha: 0.5),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text.rich(
                      TextSpan(
                        children: [
                          TextSpan(
                            text: r['author'] ?? '',
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                          TextSpan(
                            text:
                                '  ${(r['createdAt'] ?? '').toString().substring(0, 10)}',
                            style: Theme.of(context).textTheme.bodySmall,
                          ),
                        ],
                      ),
                    ),
                    Text(r['body'] ?? ''),
                    Align(
                      alignment: Alignment.centerRight,
                      child: TextButton(
                        onPressed: () => _report(id, replyIndex: i),
                        child: Text('⚑ ${s.reportBtn}'),
                      ),
                    ),
                  ],
                ),
              );
            }),
            const SizedBox(height: 8),
            Text(s.replyAs(widget.store.authorName)),
            const SizedBox(height: 4),
            TextField(
              controller: _replyCtrl(id),
              maxLines: 2,
              decoration: InputDecoration(hintText: s.replyPlaceholder),
            ),
            const SizedBox(height: 4),
            Align(
              alignment: Alignment.centerRight,
              child: FilledButton.tonal(
                onPressed: () => _postReply(id),
                child: Text(s.replyBtn),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _emptyState(AppStrings s) => Card(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              const Text('💬', style: TextStyle(fontSize: 40)),
              const SizedBox(height: 8),
              Text(s.noThreads, style: Theme.of(context).textTheme.titleMedium),
              Text(s.noThreadsBlurb, textAlign: TextAlign.center),
            ],
          ),
        ),
      );
}
