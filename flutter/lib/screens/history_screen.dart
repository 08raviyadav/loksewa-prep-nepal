/// Dates to Remember screen — the Flutter port of the vanilla site's
/// view-history (loksewa-prep-nepal/assets/js/app.js §"Historical
/// events / Dates to Remember"). Full list of data/historical-events.json
/// entries sorted by BS month/day (dateless last), EN/NE search +
/// category filter, expandable rows with bilingual summary + sources
/// + ⚠️ re-verify marks, and a "Quiz me" flashcard mode (title shown,
/// date hidden, Reveal, then Got it / Missed it with a running ✓/✗
/// count and Reset).
///
/// Deep-link convention (main.dart integration):
///   - [HistoryScreen.routeName] is '/history'.
///   - Reached from the drawer and from the Home "On This Day" card
///     via PushScope — the same route mechanism as Exam Dates.
library;

import 'package:flutter/material.dart';

import '../data/data_repository.dart';
import '../l10n/history_strings.dart';
import '../models/history.dart';
import '../theme/app_theme.dart';
import '../widgets/app_scaffold.dart';
import '../widgets/history_event_row.dart';

class HistoryScreen extends StatefulWidget {
  static const routeName = '/history';

  final int navIndex;
  final ValueChanged<int> onNav;

  const HistoryScreen({super.key, required this.navIndex, required this.onNav});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  String _categoryFilter = '';
  String _query = '';
  late final Future<List<HistoricalEvent>> _loadFuture;

  // Quiz state — mirrors vanilla's histQuiz {pool, idx, revealed,
  // correct, missed} + histQuizMode flag.
  bool _quizMode = false;
  List<HistoricalEvent> _quizPool = const [];
  int _quizIdx = 0;
  bool _quizRevealed = false;
  int _quizCorrect = 0;
  int _quizMissed = 0;

  @override
  void initState() {
    super.initState();
    _loadFuture = DataRepository().historicalEvents();
  }

  void _startQuiz(List<HistoricalEvent> all) {
    setState(() {
      _quizPool = historyQuizPool(all)..shuffle();
      _quizIdx = 0;
      _quizRevealed = false;
      _quizCorrect = 0;
      _quizMissed = 0;
      _quizMode = true;
    });
  }

  void _resetQuiz() {
    setState(() {
      _quizPool = const [];
      _quizIdx = 0;
      _quizRevealed = false;
      _quizCorrect = 0;
      _quizMissed = 0;
      _quizMode = false;
    });
  }

  void _reveal() {
    if (_quizPool.isEmpty) return;
    setState(() => _quizRevealed = true);
  }

  void _mark(bool gotIt) {
    if (!_quizRevealed || _quizPool.isEmpty || _quizIdx >= _quizPool.length) {
      return;
    }
    setState(() {
      if (gotIt) {
        _quizCorrect++;
      } else {
        _quizMissed++;
      }
      _quizIdx++;
      _quizRevealed = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final appState = AppStateScope.of(context);
    final s = appState.strings;
    return AppScaffold(
      title: s.historyTitle,
      currentIndex: widget.navIndex,
      onNav: widget.onNav,
      body: FutureBuilder<List<HistoricalEvent>>(
        future: _loadFuture,
        builder: (context, snap) {
          if (!snap.hasData) {
            return const Center(child: CircularProgressIndicator());
          }
          final all = snap.data!;
          final shown = historyFiltered(
            all,
            category: _categoryFilter,
            query: _query,
          );
          return Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 4),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(s.historyBlurb, style: AppType.small),
                    const SizedBox(height: 8),
                    Text(
                      s.historyCount(all.length),
                      style: AppType.small.copyWith(color: AppColors.of(context).muted),
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 4),
                child: TextField(
                  decoration: InputDecoration(
                    labelText: s.historySearchLabel,
                    hintText: s.historySearchHint,
                    prefixIcon: const Icon(Icons.search),
                    border: const OutlineInputBorder(),
                  ),
                  onChanged: (v) => setState(() => _query = v),
                ),
              ),
              _categoryRow(all),
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 4, 16, 8),
                child: Wrap(
                  spacing: 8,
                  children: [
                    if (_quizMode)
                      OutlinedButton(
                        onPressed: _resetQuiz,
                        child: Text(s.historyBackToList),
                      )
                    else
                      FilledButton(
                        onPressed: () => _startQuiz(all),
                        child: Text(s.historyQuizMe),
                      ),
                  ],
                ),
              ),
              Expanded(
                child: _quizMode
                    ? _QuizView(
                        pool: _quizPool,
                        idx: _quizIdx,
                        revealed: _quizRevealed,
                        correct: _quizCorrect,
                        missed: _quizMissed,
                        onReveal: _reveal,
                        onMark: _mark,
                        onReset: _resetQuiz,
                        onAgain: () => _startQuiz(all),
                      )
                    : shown.isEmpty
                        ? const _EmptyState()
                        : ListView.builder(
                            padding: const EdgeInsets.fromLTRB(16, 4, 16, 8),
                            itemCount: shown.length + 1,
                            itemBuilder: (context, i) {
                              if (i == 0) {
                                return Padding(
                                  padding: const EdgeInsets.only(bottom: 8),
                                  child: Text(
                                    s.historyShownCount(shown.length),
                                    style: AppType.small.copyWith(
                                      color: AppColors.of(context).muted,
                                    ),
                                  ),
                                );
                              }
                              return HistoryEventRow(event: shown[i - 1]);
                            },
                          ),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _categoryRow(List<HistoricalEvent> all) {
    final appState = AppStateScope.of(context);
    final s = appState.strings;
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          Text(s.historyCategoryLabel, style: AppType.small),
          const SizedBox(width: 8),
          ChoiceChip(
            label: Text(s.historyCategoryAll),
            selected: _categoryFilter.isEmpty,
            onSelected: (_) => setState(() => _categoryFilter = ''),
          ),
          for (final c in historyCategories) ...[
            const SizedBox(width: 8),
            ChoiceChip(
              label: Text(
                '${s.historyCategory(c)} '
                '(${all.where((e) => e.category == c).length})',
              ),
              selected: _categoryFilter == c,
              onSelected: (_) => setState(() => _categoryFilter = c),
            ),
          ],
        ],
      ),
    );
  }
}

class _EmptyState extends StatelessWidget {
  const _EmptyState();

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    // Scrollable: on short screens the header leaves little room for
    // this state, and a bare Column overflows (caught by widget tests).
    return SingleChildScrollView(
      child: Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text('📜', style: TextStyle(fontSize: 48)),
              const SizedBox(height: 12),
              Text(
                s.historyNoMatchTitle,
                style: AppType.h2,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              Text(
                s.historyNoMatchBody,
                style: AppType.body,
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

/// "Quiz me" flashcard mode — mirrors vanilla's renderHistoryList()
/// quiz branch: title shown, date hidden, Reveal, then Got it /
/// Missed it with a running ✓/✗ count and Reset. Dateless entries
/// never enter the pool (nothing to reveal).
class _QuizView extends StatelessWidget {
  final List<HistoricalEvent> pool;
  final int idx;
  final bool revealed;
  final int correct;
  final int missed;
  final VoidCallback onReveal;
  final ValueChanged<bool> onMark;
  final VoidCallback onReset;
  final VoidCallback onAgain;

  const _QuizView({
    required this.pool,
    required this.idx,
    required this.revealed,
    required this.correct,
    required this.missed,
    required this.onReveal,
    required this.onMark,
    required this.onReset,
    required this.onAgain,
  });

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;

    if (pool.isEmpty) {
      // Scrollable for the same short-screen reason as _EmptyState.
      return SingleChildScrollView(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text('🎴', style: TextStyle(fontSize: 48)),
                const SizedBox(height: 12),
                Text(
                  s.historyQuizEmptyTitle,
                  style: AppType.h2,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  s.historyQuizEmptyBody,
                  style: AppType.body,
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      );
    }

    if (idx >= pool.length) {
      return SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(s.historyQuizDoneTitle, style: AppType.h2),
                const SizedBox(height: 8),
                Text(
                  '$correct / ${pool.length} ${s.historyQuizCorrect} · '
                  '$missed ${s.historyQuizMissed}',
                  style: AppType.body,
                ),
                const SizedBox(height: 16),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    FilledButton(
                      onPressed: onAgain,
                      child: Text(s.historyQuizAgain),
                    ),
                    OutlinedButton(
                      onPressed: onReset,
                      child: Text(s.historyBackToList),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      );
    }

    final event = pool[idx];
    final date = historyDateLabel(event, ne: ne);
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                s.historyQuizProgress(idx + 1, pool.length, correct, missed),
                style: AppType.small.copyWith(color: AppColors.of(context).muted),
              ),
              const SizedBox(height: 12),
              Text(event.title(ne), style: AppType.h2),
              const SizedBox(height: 4),
              Text(
                s.historyCategory(event.category),
                style: AppType.small.copyWith(color: AppColors.of(context).muted),
              ),
              const SizedBox(height: 16),
              Text(s.historyQuizWhen, style: AppType.h3),
              const SizedBox(height: 12),
              if (revealed) ...[
                Text(date, style: AppType.h1),
                const SizedBox(height: 12),
                Text(event.summary(ne), style: AppType.body),
                const SizedBox(height: 16),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    FilledButton(
                      onPressed: () => onMark(true),
                      child: Text(s.historyQuizGotIt),
                    ),
                    OutlinedButton(
                      onPressed: () => onMark(false),
                      child: Text(s.historyQuizMissedIt),
                    ),
                  ],
                ),
              ] else
                FilledButton(
                  onPressed: onReveal,
                  child: Text(s.historyQuizReveal),
                ),
              const SizedBox(height: 16),
              OutlinedButton(
                onPressed: onReset,
                child: Text(s.historyQuizReset),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
