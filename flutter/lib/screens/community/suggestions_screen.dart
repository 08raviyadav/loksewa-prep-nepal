import 'package:flutter/material.dart';

import '../../l10n/app_strings.dart';
import '../../l10n/community_strings.dart';
import '../../state/community_store.dart';
import '../../widgets/app_scaffold.dart';

/// Suggestions (Milestone 6) — matches the vanilla site's Suggest tab:
/// suggestion form (title >= 8, description >= 20, category, no links),
/// local list sorted by upvotes desc, upvote TOGGLE via voters list,
/// spam guards (duplicate-title block, 5/hour rate limit), "local demo"
/// honesty banner. On-device with the vanilla-identical key
/// `loksewa_suggestions_v1`.
/// Route name for integration: [SuggestionsScreen.routeName].
class SuggestionsScreen extends StatefulWidget {
  static const routeName = '/community/suggestions';

  final CommunityStore store;
  final int navIndex;
  final ValueChanged<int> onNav;

  const SuggestionsScreen({
    super.key,
    required this.store,
    required this.navIndex,
    required this.onNav,
  });

  @override
  State<SuggestionsScreen> createState() => _SuggestionsScreenState();
}

class _SuggestionsScreenState extends State<SuggestionsScreen> {
  final _title = TextEditingController();
  final _desc = TextEditingController();
  String _category = 'feature';
  List<String> _errors = [];
  bool _done = false;
  bool _submitDisabled =
      false; // vanilla: disabled after submit until form changes

  @override
  void initState() {
    super.initState();
    widget.store.init();
    void reenable() {
      if (_submitDisabled) setState(() => _submitDisabled = false);
      if (_done) setState(() => _done = false);
    }

    _title.addListener(reenable);
    _desc.addListener(reenable);
  }

  @override
  void dispose() {
    _title.dispose();
    _desc.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    final s = AppStateScope.of(context).strings;
    final errors = await widget.store.addSuggestion(
      title: _title.text,
      description: _desc.text,
      category: _category,
      nepali: s.isNe,
    );
    if (!mounted) return;
    setState(() {
      _errors = errors;
      _done = errors.isEmpty;
      _submitDisabled = errors.isEmpty; // vanilla double-submit guard
    });
    if (errors.isEmpty) {
      _title.clear();
      _desc.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    return AppScaffold(
      title: s.suggestTitle,
      currentIndex: widget.navIndex,
      onNav: widget.onNav,
      body: ListenableBuilder(
        listenable: widget.store,
        builder: (context, _) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Card(
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
                      TextSpan(text: s.suggestLocalPreview),
                    ],
                  ),
                ),
              ),
            ),
            _formCard(s),
            const SizedBox(height: 8),
            Text(
              s.suggestionsCount(widget.store.suggestions.length),
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            if (widget.store.suggestions.isEmpty) _emptyState(s),
            ...widget.store.suggestions.map((x) => _suggestionCard(s, x)),
          ],
        ),
      ),
    );
  }

  Widget _formCard(AppStrings s) => Card(
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                s.suggestTitle,
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 8),
              TextField(
                controller: _title,
                maxLength: 120,
                decoration: InputDecoration(
                  labelText: s.suggestFormTitle,
                  hintText: s.suggestTitlePh,
                ),
              ),
              TextField(
                controller: _desc,
                maxLines: 4,
                decoration: InputDecoration(
                  labelText: s.suggestDescLabel,
                  hintText: s.suggestDescPh,
                ),
              ),
              const SizedBox(height: 8),
              DropdownButtonFormField<String>(
                initialValue: _category,
                decoration: InputDecoration(labelText: s.suggestCatLabel),
                items: suggestionCategories
                    .map(
                      (c) => DropdownMenuItem(
                        value: c[0],
                        child: Text(s.categoryLabel(c[0])),
                      ),
                    )
                    .toList(),
                onChanged: (v) => setState(() => _category = v ?? 'feature'),
              ),
              if (_errors.isNotEmpty) ...[
                const SizedBox(height: 8),
                ..._errors.map(
                  (e) => Text(
                    '• $e',
                    style:
                        TextStyle(color: Theme.of(context).colorScheme.error),
                  ),
                ),
              ],
              if (_done) ...[
                const SizedBox(height: 8),
                Text(
                  '✓ ${s.suggestDone}',
                  style: const TextStyle(color: Colors.green),
                ),
              ],
              const SizedBox(height: 8),
              FilledButton(
                onPressed: _submitDisabled ? null : _submit,
                child: Text(s.suggestSubmit),
              ),
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(
                  s.suggestRateNote,
                  style: Theme.of(context).textTheme.bodySmall,
                ),
              ),
            ],
          ),
        ),
      );

  Widget _suggestionCard(AppStrings s, Map<String, dynamic> x) {
    final voted = widget.store.hasVoted(x);
    final isSeed = x['_seed'] == true;
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '${s.categoryLabel(x['category'] ?? 'other')} · ${s.byLabel} ${x['by'] ?? 'Guest'} · ${(x['at'] ?? '').toString().substring(0, 10)}${isSeed ? ' · 🌱 ${s.exampleLabel}' : ''}',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 4),
            Text(
              x['title'] ?? '',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            Text(x['description'] ?? ''),
            const SizedBox(height: 8),
            OutlinedButton.icon(
              icon: Text(voted ? '▲' : '△'),
              label: Text('${s.upvote} (${x['upvotes'] ?? 0})'),
              style: voted
                  ? OutlinedButton.styleFrom(
                      foregroundColor: Theme.of(context).colorScheme.primary,
                    )
                  : null,
              onPressed: () => widget.store.upvoteSuggestion(x['id'] as String),
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
              const Text('💡', style: TextStyle(fontSize: 40)),
              const SizedBox(height: 8),
              Text(
                s.suggestEmpty,
                style: Theme.of(context).textTheme.titleMedium,
              ),
              Text(s.suggestEmptyBlurb, textAlign: TextAlign.center),
            ],
          ),
        ),
      );
}
