/// Dashboard — Flutter port of vanilla `renderDashboard`
/// (loksewa-prep-nepal/assets/js/app.js).
///
/// Shows: level ring + XP bar + streak header, stat grid, badges, weekly
/// goal, weak-topic analysis, personal records, Daily Challenge / Quick
/// Quiz entry cards, recent attempts, and a score-history chart.
///
/// ## Deep-link conventions (integration contract)
///
/// The dashboard does not own quiz routing. It emits [PracticeDeepLink]
/// intents through [onDeepLink]; the host (RootNav / main.dart) routes them:
///
/// - `PracticeDeepLink.dailyChallenge(seed)` — vanilla `dailyChallenge`.
///   `seed` is the UTC `yyyy-MM-dd` string (see `dailySeed()`). The quiz
///   milestone should rebuild vanilla's exact set with
///   `SeededRandom(seed)` (in `gamification/analytics.dart`):
///   shuffle the bank with the seeded RNG, take 10, shuffle each
///   question's options with the same RNG — the Flutter set then matches
///   vanilla's question set for the day. Marks `dailyDone[seed]` on
///   finish (vanilla `finishAttempt`), and shows the repeat confirm on a
///   second run of the same day ("no extra XP") — that UI lives with the
///   quiz milestone.
/// - `PracticeDeepLink.quickQuiz()` — vanilla `quickQuiz`: 5 random
///   questions, practice mode, negOn=true, negRate=0.2.
/// - `PracticeDeepLink.topicPractice(topic)` — vanilla
///   `startPracticeTopic(topic)`: practice view pre-filtered to `topic`
///   (default count 10). Warns "no questions tagged" when the bank has
///   none for the topic instead of silently practicing something else.
library;

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../data/data_repository.dart';
import '../gamification/analytics.dart';
import '../l10n/dashboard_strings.dart';
import '../state/progress_store.dart';
import '../theme/app_theme.dart';
import '../widgets/app_scaffold.dart';
import '../widgets/stat_card.dart';

/// A practice-launch intent emitted by the dashboard.
enum PracticeDeepLinkKind { dailyChallenge, quickQuiz, topicPractice }

class PracticeDeepLink {
  final PracticeDeepLinkKind kind;
  final String? topic; // topicPractice
  final String? seed; // dailyChallenge: vanilla seed string (yyyy-MM-dd UTC)
  final int count; // vanilla question counts: 10 daily, 5 quick, 10 topic

  const PracticeDeepLink._({
    required this.kind,
    this.topic,
    this.seed,
    required this.count,
  });

  factory PracticeDeepLink.dailyChallenge({required String seed}) =>
      PracticeDeepLink._(
        kind: PracticeDeepLinkKind.dailyChallenge,
        seed: seed,
        count: 10,
      );

  factory PracticeDeepLink.quickQuiz() =>
      const PracticeDeepLink._(kind: PracticeDeepLinkKind.quickQuiz, count: 5);

  factory PracticeDeepLink.topicPractice(String topic) => PracticeDeepLink._(
        kind: PracticeDeepLinkKind.topicPractice,
        topic: topic,
        count: 10,
      );
}

class DashboardScreen extends StatefulWidget {
  final int navIndex;
  final ValueChanged<int> onNav;
  final void Function(PracticeDeepLink) onDeepLink;

  const DashboardScreen({
    super.key,
    required this.navIndex,
    required this.onNav,
    required this.onDeepLink,
  });

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashData {
  final ProgressStore store;
  final Map<String, String> examNames;
  final Map<String, dynamic>? speedBest;
  _DashData({required this.store, required this.examNames, this.speedBest});
}

class _DashboardScreenState extends State<DashboardScreen> {
  late final Future<_DashData> _future;

  @override
  void initState() {
    super.initState();
    _future = _load();
  }

  Future<_DashData> _load() async {
    final store = await ProgressStore.instance;
    final exams = await DataRepository().exams();
    final prefs = await SharedPreferences.getInstance();
    Map<String, dynamic>? speedBest;
    // Vanilla SPEED_BEST_KEY ('loksewa_speed_best_v1') lives in its own
    // localStorage key, outside the progress object — same here.
    final rawSpeed = prefs.getString('loksewa_speed_best_v1');
    if (rawSpeed != null) {
      try {
        speedBest = Map<String, dynamic>.from(json.decode(rawSpeed) as Map);
      } catch (_) {}
    }
    return _DashData(
      store: store,
      examNames: {for (final e in exams) e.id: e.name},
      speedBest: speedBest,
    );
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    return AppScaffold(
      title: s.navDashboard,
      currentIndex: widget.navIndex,
      onNav: widget.onNav,
      body: FutureBuilder<_DashData>(
        future: _future,
        builder: (context, snap) {
          if (!snap.hasData) {
            return const Center(
              child: Padding(
                padding: EdgeInsets.all(AppSpacing.s12),
                child: CircularProgressIndicator(color: AppColors.accent),
              ),
            );
          }
          return _DashboardBody(
            data: snap.data!,
            onNav: widget.onNav,
            onDeepLink: widget.onDeepLink,
          );
        },
      ),
    );
  }
}

class _DashboardBody extends StatelessWidget {
  final _DashData data;
  final ValueChanged<int> onNav;
  final void Function(PracticeDeepLink) onDeepLink;

  const _DashboardBody({
    required this.data,
    required this.onNav,
    required this.onDeepLink,
  });

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final store = data.store;
    final attempts = store.attempts;
    final stats = attemptStats(attempts);
    final badges = store.badges();
    final week = weeklyProgress(attempts, store.weeklyTarget);
    final weak = weakTopics(attempts);
    final records = personalRecords(
      attempts,
      xp: store.xp,
      currentStreak: store.streak,
      speedBest: data.speedBest,
    );

    return ListView(
      padding: const EdgeInsets.all(AppSpacing.s4),
      children: [
        _HeaderCard(store: store),
        const SizedBox(height: AppSpacing.s4),
        // Stat grid — vanilla #dash-stats .grid (2x2 on phones).
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          mainAxisSpacing: AppSpacing.s3,
          crossAxisSpacing: AppSpacing.s3,
          childAspectRatio: 1.9,
          children: [
            StatCard(
              value: '${store.xp}',
              label: 'XP · ${s.dashLevel} ${store.level}',
            ),
            StatCard(value: '🔥 ${store.streak}', label: s.dashDayStreak),
            StatCard(
              value: '${stats.totalAttempts}',
              label:
                  '${s.dashSessions} · ${stats.totalQuestions} ${s.dashQuestions}',
            ),
            StatCard(
              value: '${stats.avgPct}%',
              label: '${s.dashAverageScore} · ${stats.passes} ${s.dashPasses}',
            ),
          ],
        ),
        const SizedBox(height: AppSpacing.s4),
        // Level progress — vanilla "Level N progress" card.
        ProgressCard(
          title: s.dashLevelProgress(store.level),
          subtitle: s.xpToNext(store.xp % 500, store.level + 1),
          progress: (store.xp % 500) / 500,
        ),
        const SizedBox(height: AppSpacing.s4),
        _BadgesCard(badges: badges),
        const SizedBox(height: AppSpacing.s4),
        _WeeklyCard(week: week, goalsMet: store.weeklyGoalsMet),
        const SizedBox(height: AppSpacing.s4),
        _WeakTopicsCard(
          weak: weak,
          onPractice: (topic) =>
              onDeepLink(PracticeDeepLink.topicPractice(topic)),
        ),
        const SizedBox(height: AppSpacing.s4),
        _RecordsCard(records: records, examNames: data.examNames),
        const SizedBox(height: AppSpacing.s4),
        _EntryCards(onDeepLink: onDeepLink),
        const SizedBox(height: AppSpacing.s4),
        _RecentAttemptsCard(
          attempts: attempts,
          examNames: data.examNames,
          onStart: () => onNav(1),
        ),
        const SizedBox(height: AppSpacing.s4),
        _ScoreHistoryCard(attempts: attempts, onStart: () => onNav(1)),
        const SizedBox(height: AppSpacing.s8),
      ],
    );
  }
}

/// Header: level ring + XP bar + streak flame.
class _HeaderCard extends StatelessWidget {
  final ProgressStore store;
  const _HeaderCard({required this.store});

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final progress = (store.xp % 500) / 500;
    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s4),
        child: Row(
          children: [
            Stack(
              alignment: Alignment.center,
              children: [
                SizedBox(
                  width: 76,
                  height: 76,
                  child: CircularProgressIndicator(
                    value: progress,
                    strokeWidth: 8,
                    backgroundColor: AppColors.borderSoft,
                    valueColor: const AlwaysStoppedAnimation<Color>(
                      AppColors.accent,
                    ),
                  ),
                ),
                Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      '${(progress * 100).round()}%',
                      style: AppType.tiny.copyWith(fontWeight: FontWeight.w800),
                    ),
                    Text('Lv ${store.level}', style: AppType.small),
                  ],
                ),
              ],
            ),
            const SizedBox(width: AppSpacing.s4),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('${s.dashLevel} ${store.level}', style: AppType.h2),
                  Text(
                    '${store.xp} XP',
                    style: AppType.lead.copyWith(color: AppColors.accent),
                  ),
                  const SizedBox(height: AppSpacing.s1),
                  Text(
                    '🔥 ${store.streak} ${s.dashDayStreak}',
                    style: AppType.body,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _BadgesCard extends StatelessWidget {
  final List<String> badges;
  const _BadgesCard({required this.badges});

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s4),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('🏅 ${s.dashBadgesTitle}', style: AppType.h3),
            const SizedBox(height: AppSpacing.s2),
            if (badges.isEmpty)
              Text(
                s.dashNoBadges,
                style: AppType.body.copyWith(color: AppColors.muted),
              )
            else
              Wrap(
                spacing: AppSpacing.s2,
                runSpacing: AppSpacing.s2,
                children: badges
                    .map(
                      (b) => Chip(
                        label: Text(b, style: AppType.small),
                        backgroundColor: AppColors.accentSoft,
                        side: const BorderSide(color: AppColors.accentLine),
                      ),
                    )
                    .toList(),
              ),
          ],
        ),
      ),
    );
  }
}

class _WeeklyCard extends StatelessWidget {
  final WeekProgress week;
  final int goalsMet;
  const _WeeklyCard({required this.week, required this.goalsMet});

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final status = week.met ? s.dashGoalMet : s.dashPctThere(week.pct);
    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s4),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(s.dashWeeklyTitle, style: AppType.h3),
            const SizedBox(height: AppSpacing.s1),
            Text(
              '${s.dashWeeklyDone(week.done, week.target)} · ${s.dashWeekOf} ${week.weekStart} ${s.dashWeekRange}',
              style: AppType.small.copyWith(color: AppColors.muted),
            ),
            Text(status, style: AppType.small),
            const SizedBox(height: AppSpacing.s2),
            ClipRRect(
              borderRadius: AppRadius.smAll,
              child: LinearProgressIndicator(
                value: week.pct / 100,
                minHeight: 10,
                backgroundColor: AppColors.borderSoft,
                valueColor: AlwaysStoppedAnimation<Color>(
                  week.met ? AppColors.green : AppColors.accent,
                ),
              ),
            ),
            const SizedBox(height: AppSpacing.s2),
            Text(
              '${s.dashGoalsSmashed} $goalsMet',
              style: AppType.small.copyWith(color: AppColors.muted),
            ),
            // NOTE: vanilla also offers a weekly-target selector
            // (35/70/100/140). That needs a `setWeeklyTarget` mutator on
            // ProgressStore (milestone 1 owns that file); flagged for
            // integration rather than duplicating store logic here.
          ],
        ),
      ),
    );
  }
}

class _WeakTopicsCard extends StatelessWidget {
  final List<TopicAccuracy> weak;
  final void Function(String topic) onPractice;
  const _WeakTopicsCard({required this.weak, required this.onPractice});

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s4),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('🎯 ${s.dashWeakTitle}', style: AppType.h3),
            const SizedBox(height: AppSpacing.s2),
            if (weak.isEmpty)
              Text(
                s.dashNoWeak,
                style: AppType.body.copyWith(color: AppColors.muted),
              )
            else ...[
              for (final w in weak)
                Padding(
                  padding: const EdgeInsets.only(bottom: AppSpacing.s1),
                  child: Text(
                    '• ${s.dashWeakLine(w.topic, w.correct, w.total)}',
                    style: AppType.body,
                  ),
                ),
              const SizedBox(height: AppSpacing.s2),
              ElevatedButton(
                onPressed: () => onPractice(weak.first.topic),
                child: Text(s.dashPracticeWeakest(weak.first.topic)),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class _RecordsCard extends StatelessWidget {
  final PersonalRecords records;
  final Map<String, String> examNames;
  const _RecordsCard({required this.records, required this.examNames});

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final r = records;
    final bd = r.bestDay;
    final speed = r.speedBest;
    String examName(String id) => id.isEmpty ? '' : (examNames[id] ?? id);
    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s4),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(s.dashRecordsTitle, style: AppType.h3),
            const SizedBox(height: AppSpacing.s2),
            Text(
              '${s.dashLongestStreak}: ${r.longestStreakDays} ${s.dashDays} · '
              '${s.dashTotalXp}: ${r.totalXp} · '
              '${s.dashTotalQuestions}: ${r.totalQuestions}',
              style: AppType.body,
            ),
            const SizedBox(height: AppSpacing.s1),
            Text(
              '${s.dashBestDay}: ${bd != null ? '${bd.date} — ${bd.total} ${s.dashQuestions}' : s.dashNoBestDay}',
              style: AppType.body.copyWith(
                color: bd == null ? AppColors.muted : null,
              ),
            ),
            const SizedBox(height: AppSpacing.s1),
            Text(
              '${s.dashBestMocks}: ${r.bestMocks.isNotEmpty ? r.bestMocks.map((b) => '${examName(b.examId)} ${b.pct}% (${b.score}/${b.max}, ${b.date})').join(' · ') : s.dashNoMocks}',
              style: AppType.body.copyWith(
                color: r.bestMocks.isEmpty ? AppColors.muted : null,
              ),
            ),
            const SizedBox(height: AppSpacing.s1),
            Text(
              '${s.dashBestSpeed}: ${speed != null ? '${speed['score']}/${speed['max']} (${speed['pct']}%) ${s.dashOnDate} ${speed['date']}' : s.dashNoSpeed}',
              style: AppType.body.copyWith(
                color: speed == null ? AppColors.muted : null,
              ),
            ),
            const SizedBox(height: AppSpacing.s2),
            Text(
              s.dashPrivateNote,
              style: AppType.small.copyWith(color: AppColors.muted),
            ),
          ],
        ),
      ),
    );
  }
}

class _EntryCards extends StatelessWidget {
  final void Function(PracticeDeepLink) onDeepLink;
  const _EntryCards({required this.onDeepLink});

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Expanded(
          child: Card(
            margin: EdgeInsets.zero,
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.s4),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(s.dashDailyTitle, style: AppType.h3),
                  const SizedBox(height: AppSpacing.s1),
                  Text(
                    s.dashDailyBody,
                    style: AppType.small.copyWith(color: AppColors.muted),
                  ),
                  const SizedBox(height: AppSpacing.s3),
                  ElevatedButton(
                    onPressed: () => onDeepLink(
                      PracticeDeepLink.dailyChallenge(seed: dailySeed()),
                    ),
                    child: Text(s.dashStartChallenge),
                  ),
                ],
              ),
            ),
          ),
        ),
        const SizedBox(width: AppSpacing.s3),
        Expanded(
          child: Card(
            margin: EdgeInsets.zero,
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.s4),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(s.dashQuickTitle, style: AppType.h3),
                  const SizedBox(height: AppSpacing.s1),
                  Text(
                    s.dashQuickBody,
                    style: AppType.small.copyWith(color: AppColors.muted),
                  ),
                  const SizedBox(height: AppSpacing.s3),
                  ElevatedButton(
                    onPressed: () => onDeepLink(PracticeDeepLink.quickQuiz()),
                    child: Text(s.dashStartQuiz),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class _RecentAttemptsCard extends StatelessWidget {
  final List<Map<String, dynamic>> attempts;
  final Map<String, String> examNames;
  final VoidCallback onStart;
  const _RecentAttemptsCard({
    required this.attempts,
    required this.examNames,
    required this.onStart,
  });

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final recent = attempts.reversed.take(10).toList();
    String examName(String id) => id.isEmpty ? '' : (examNames[id] ?? id);
    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s4),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('📝 ${s.dashRecentTitle}', style: AppType.h3),
            const SizedBox(height: AppSpacing.s2),
            if (recent.isEmpty) ...[
              Text(
                s.dashNoAttemptsTitle,
                style: AppType.h3.copyWith(color: AppColors.accent),
              ),
              const SizedBox(height: AppSpacing.s1),
              Text(
                s.dashNoAttemptsBody,
                style: AppType.body.copyWith(color: AppColors.muted),
              ),
              const SizedBox(height: AppSpacing.s3),
              ElevatedButton(
                onPressed: onStart,
                child: Text(s.dashStartPracticing),
              ),
            ] else
              for (final a in recent)
                Padding(
                  padding: const EdgeInsets.only(bottom: AppSpacing.s2),
                  child: _AttemptRow(
                    attempt: a,
                    examLabel: examName(a['exam'] as String? ?? ''),
                  ),
                ),
          ],
        ),
      ),
    );
  }
}

class _AttemptRow extends StatelessWidget {
  final Map<String, dynamic> attempt;
  final String examLabel;
  const _AttemptRow({required this.attempt, required this.examLabel});

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final a = attempt;
    final date = (a['date'] as String? ?? '');
    final day = date.length >= 10 ? date.substring(0, 10) : date;
    final passed = a['passed'] == true;
    return RichText(
      text: TextSpan(
        style: AppType.small.copyWith(
          color: Theme.of(context).colorScheme.onSurface,
        ),
        children: [
          TextSpan(text: '$day · ${a['mode']}'),
          if (examLabel.isNotEmpty) TextSpan(text: ' · $examLabel'),
          TextSpan(
            text:
                ' — ${a['score']}/${a['max']} (${a['pct']}%) ${passed ? '✅ ${s.dashPass}' : '❌ ${s.dashFail}'}',
            style: const TextStyle(fontWeight: FontWeight.w700),
          ),
          TextSpan(
            text: ' · ${a['correct']}✓ ${a['wrong']}✗ ${a['skipped']}–',
            style: const TextStyle(color: AppColors.muted),
          ),
        ],
      ),
    );
  }
}

class _ScoreHistoryCard extends StatelessWidget {
  final List<Map<String, dynamic>> attempts;
  final VoidCallback onStart;
  const _ScoreHistoryCard({required this.attempts, required this.onStart});

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final data = attempts.length > 20
        ? attempts.sublist(attempts.length - 20)
        : attempts;
    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s4),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('📊 ${s.dashHistoryTitle}', style: AppType.h3),
            const SizedBox(height: AppSpacing.s2),
            if (data.isEmpty) ...[
              Text(
                s.dashNoHistory,
                style: AppType.body.copyWith(color: AppColors.muted),
              ),
              const SizedBox(height: AppSpacing.s3),
              ElevatedButton(
                onPressed: onStart,
                child: Text(s.dashStartPracticing),
              ),
            ] else
              SizedBox(
                height: 160,
                width: double.infinity,
                child: CustomPaint(painter: _ScoreChart(attempts: data)),
              ),
          ],
        ),
      ),
    );
  }
}

/// Vanilla `drawChart`: bar per attempt, green for pass / red for fail,
/// height = pct% of the plot area. Last 20 attempts.
class _ScoreChart extends CustomPainter {
  final List<Map<String, dynamic>> attempts;
  const _ScoreChart({required this.attempts});

  @override
  void paint(Canvas canvas, Size size) {
    final axis = Paint()
      ..color = AppColors.muted
      ..strokeWidth = 1;
    canvas.drawLine(
      Offset(0, size.height - 1),
      Offset(size.width, size.height - 1),
      axis,
    );
    if (attempts.isEmpty) return;
    final n = attempts.length;
    final bw = size.width / n;
    for (var i = 0; i < n; i++) {
      final a = attempts[i];
      final pct = ((a['pct'] as num?)?.toDouble() ?? 0).clamp(0.0, 100.0);
      final h = (pct / 100) * (size.height - 8);
      final bar = Paint()
        ..color = a['passed'] == true ? AppColors.green : AppColors.danger;
      canvas.drawRect(
        Rect.fromLTWH(i * bw + bw * 0.22, size.height - h, bw * 0.56, h),
        bar,
      );
    }
  }

  @override
  bool shouldRepaint(covariant _ScoreChart oldDelegate) =>
      oldDelegate.attempts != attempts;
}
