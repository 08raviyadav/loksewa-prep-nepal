import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;

import 'data/data_repository.dart';
import 'engine/quiz_engine.dart';
import 'gamification/analytics.dart';
import 'l10n/dashboard_strings.dart';
import 'l10n/quiz_strings.dart';
import 'models/course.dart';
import 'models/models.dart';
import 'screens/community/discussion_screen.dart';
import 'screens/community/submit_question_screen.dart';
import 'screens/community/suggestions_screen.dart';
import 'screens/courses/chapter_reader_screen.dart';
import 'screens/courses/courses_screen.dart';
import 'screens/dashboard_screen.dart';
import 'screens/exam_dates_screen.dart';
import 'screens/history_screen.dart';
import 'screens/home_screen.dart';
import 'screens/mock_list_screen.dart';
import 'screens/practice_screen.dart';
import 'screens/quiz/quiz_screen.dart';
import 'services/reminder_scheduler.dart';
import 'state/app_state.dart';
import 'state/community_store.dart';
import 'state/course_progress_store.dart';
import 'state/progress_store.dart';
import 'theme/app_theme.dart';
import 'widgets/app_scaffold.dart';
import 'widgets/push_scope.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final appState = AppState();
  await appState.init();
  await ProgressStore.instance; // warm the progress store
  await rescheduleAll(); // M7: arm exam reminders + daily nudge (no-op on web)
  runApp(AppStateScope(state: appState, child: const VidyapeethApp()));
}

class VidyapeethApp extends StatefulWidget {
  const VidyapeethApp({super.key});

  @override
  State<VidyapeethApp> createState() => _VidyapeethAppState();
}

class _VidyapeethAppState extends State<VidyapeethApp> {
  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    return AnimatedBuilder(
      animation: state,
      builder: (context, _) => MaterialApp(
        title: 'LokSewa Vidyapeeth',
        debugShowCheckedModeBanner: false,
        theme: buildLightTheme(),
        darkTheme: buildDarkTheme(),
        themeMode: state.themeMode,
        home: const RootNav(),
      ),
    );
  }
}

/// Bottom-nav root: 0 Home, 1 Practice, 2 Mock Exams, 3 Dashboard.
/// Exam Dates / Courses / Community live behind the drawer and are
/// pushed as routes (vanilla parity).
class RootNav extends StatefulWidget {
  const RootNav({super.key});

  @override
  State<RootNav> createState() => _RootNavState();
}

class _RootNavState extends State<RootNav> {
  int _index = 0;
  Exam? _practiceExam;
  Exam? _mockExam;
  late final Future<_SharedData> _sharedFuture;

  @override
  void initState() {
    super.initState();
    _sharedFuture = _loadShared();
  }

  Future<_SharedData> _loadShared() async {
    final community = CommunityStore();
    await community.init();
    final courseStore = CourseProgressStore();
    await courseStore.load();
    final courses = await loadCourses();
    return _SharedData(
      community: community,
      courseStore: courseStore,
      courses: courses,
    );
  }

  void _go(int i) => setState(() {
        _index = i;
        if (i != 1) _practiceExam = null; // one-shot prefill
        if (i != 2) _mockExam = null;
      });

  void _popAndGo(int i) {
    Navigator.of(context).popUntil((r) => r.isFirst);
    _go(i);
  }

  /// Vanilla `startPracticeTopic`: immediate 10Q quiz on one topic.
  Future<void> _startTopicQuiz(String examId, String topic) async {
    final repo = DataRepository();
    final pool = await repo.questionsForExam(examId, topics: {topic});
    if (!mounted) return;
    final s = AppStateScope.of(context).strings;
    if (pool.isEmpty) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(s.noTopicQuestions(topic))));
      return;
    }
    final prelim = await _prelimFor(examId);
    final picked = (pool.toList()..shuffle()).take(10).toList();
    final negRate = _negRateFor(prelim);
    if (!mounted) return;
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => QuizScreen(
          config: QuizConfig(
            questions: picked,
            negOn: negRate > 0,
            negRate: negRate,
            examId: examId,
          ),
          meta: _metaFor(examId, prelim),
          bank: pool,
        ),
      ),
    );
  }

  /// Vanilla `dailyChallenge`: seeded 10Q from the whole bank.
  Future<void> _dailyChallenge() async {
    final store = await ProgressStore.instance;
    if (!mounted) return;
    final seed = dailySeed();
    final s = AppStateScope.of(context).strings;
    if (store.isDailyDone(seed)) {
      final again = await showDialog<bool>(
        context: context,
        builder: (ctx) => AlertDialog(
          title: Text(s.dailyDoneTitle),
          content: Text(s.dailyRepeatAsk),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(ctx, false),
              child: Text(s.cancel),
            ),
            FilledButton(
              onPressed: () => Navigator.pop(ctx, true),
              child: Text(s.dailyRepeatYes),
            ),
          ],
        ),
      );
      if (again != true || !mounted) return;
    }
    final repo = DataRepository();
    final all = await repo.allQuestions();
    if (!mounted) return;
    final rand = SeededRandom(seed);
    final shuffled = all.toList()
      ..sort((a, b) => rand.next().compareTo(rand.next()));
    final picked = shuffled.take(10).toList();
    if (!mounted) return;
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => QuizScreen(
          config: QuizConfig(
            questions: picked,
            negOn: true,
            negRate: 0.2,
            examId: '',
            dailySeed: seed,
          ),
          meta: const QuizMeta(
            examName: 'Daily Challenge',
            cutoff: 45,
            cutoffPct: 45,
            fullTotal: 100,
          ),
          bank: all,
        ),
      ),
    );
  }

  /// Vanilla `quickQuiz`: 5 random questions.
  Future<void> _quickQuiz() async {
    final repo = DataRepository();
    final all = await repo.allQuestions();
    if (!mounted) return;
    final picked = (all.toList()..shuffle()).take(5).toList();
    if (!mounted) return;
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => QuizScreen(
          config: QuizConfig(
            questions: picked,
            negOn: true,
            negRate: 0.2,
            examId: '',
          ),
          meta: const QuizMeta(
            examName: 'Quick Quiz',
            cutoff: 45,
            cutoffPct: 45,
            fullTotal: 100,
          ),
          bank: all,
        ),
      ),
    );
  }

  Future<Map<String, dynamic>?> _prelimFor(String examId) async {
    try {
      final raw = await rootBundle.loadString('assets/data/exams.json');
      final decoded = json.decode(raw);
      final list = decoded is List ? decoded : decoded['exams'] as List;
      for (final e in list) {
        final m = Map<String, dynamic>.from(e as Map);
        if (m['id'] == examId && m['prelim'] != null) {
          return Map<String, dynamic>.from(m['prelim'] as Map);
        }
      }
    } catch (_) {}
    return null;
  }

  double _negRateFor(Map<String, dynamic>? prelim) {
    if (prelim == null) return 0.2;
    final neg = prelim['negative'] as num?;
    if (neg == null || neg == 0) return 0;
    return neg.toDouble();
  }

  QuizMeta _metaFor(String examId, Map<String, dynamic>? prelim) {
    final pass = (prelim?['pass'] as num?)?.toInt() ?? 45;
    final total = (prelim?['total'] as num?)?.toInt() ?? 100;
    return QuizMeta(
      examName: examId,
      cutoff: pass,
      cutoffPct: prelim != null ? (pass / total * 100).round() : 45,
      fullTotal: total,
    );
  }

  /// Builds the drawer destination page for [route], or null for an
  /// unknown route.
  Widget? _pageFor(String route, _SharedData shared) {
    switch (route) {
      case ExamDatesScreen.routeName:
        return ExamDatesScreen(
          navIndex: 0,
          onNav: _popAndGo,
          onPracticeExam: (exam) {
            _practiceExam = exam;
            _popAndGo(1);
          },
          onMockExam: (exam) {
            _mockExam = exam;
            _popAndGo(2);
          },
        );
      case HistoryScreen.routeName:
        return HistoryScreen(navIndex: 0, onNav: _popAndGo);
      case '/courses':
        return CoursesScreen(
          store: shared.courseStore,
          courses: shared.courses,
        );
      case DiscussionScreen.routeName:
        return DiscussionScreen(
          store: shared.community,
          navIndex: 0,
          onNav: _popAndGo,
        );
      case SubmitQuestionScreen.routeName:
        return SubmitQuestionScreen(
          store: shared.community,
          navIndex: 0,
          onNav: _popAndGo,
        );
      case SuggestionsScreen.routeName:
        return SuggestionsScreen(
          store: shared.community,
          navIndex: 0,
          onNav: _popAndGo,
        );
    }
    return null;
  }

  /// Drawer navigation (v1.0.1 fix): every pushed drawer page is wrapped
  /// in its own PushScope. Before this, PushScope lived only above the
  /// home route, so on any pushed page the drawer's
  /// `PushScope.of(context)` returned null and every drawer tap silently
  /// did nothing but close the drawer — the first-opened drawer page
  /// appeared "stuck".
  ///
  /// Drawer taps from the home route push normally; taps from a pushed
  /// page replace it, so the stack stays shallow and system-back always
  /// returns home instead of walking back through every drawer page.
  void _push(String route, _SharedData shared, {bool replace = false}) {
    final page = _pageFor(route, shared);
    if (page == null) return;
    final nav = Navigator.of(context);
    final materialPage = MaterialPageRoute(
      settings: RouteSettings(name: route),
      builder: (_) => PushScope(
        onPush: (r) => _push(r, shared, replace: true),
        child: page,
      ),
    );
    if (replace) {
      nav.pushReplacement(materialPage);
    } else {
      nav.push(materialPage);
    }
  }

  void _resumeChapter(
    _SharedData shared, {
    required String courseExam,
    required String chapterId,
  }) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => ChapterReaderScreen(
          store: shared.courseStore,
          courses: shared.courses,
          exam: courseExam,
          chapterId: chapterId,
          onPracticeTopic: ({required courseExam, required topic}) {
            final examId = courseExamMap[courseExam];
            if (examId != null) _startTopicQuiz(examId, topic);
          },
        ),
      ),
    );
  }

  void _onDashboardLink(PracticeDeepLink link) {
    switch (link.kind) {
      case PracticeDeepLinkKind.dailyChallenge:
        _dailyChallenge();
      case PracticeDeepLinkKind.quickQuiz:
        _quickQuiz();
      case PracticeDeepLinkKind.topicPractice:
        _topicPractice(link.topic ?? '');
    }
  }

  Future<void> _topicPractice(String topic) async {
    if (topic.isEmpty) return;
    // Weakest topic is drilled against the user's most-used exam
    // (vanilla drills it against the current practice exam).
    final store = await ProgressStore.instance;
    String examId = 'kharidar';
    final counts = <String, int>{};
    for (final a in store.attempts) {
      final e = a['exam'] as String? ?? '';
      if (e.isNotEmpty) counts[e] = (counts[e] ?? 0) + 1;
    }
    if (counts.isNotEmpty) {
      examId = counts.entries.reduce((a, b) => a.value >= b.value ? a : b).key;
    }
    _startTopicQuiz(examId, topic);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<_SharedData>(
      future: _sharedFuture,
      builder: (context, snap) {
        final shared = snap.data;
        Widget body;
        switch (_index) {
          case 1:
            body = PracticeScreen(
              navIndex: _index,
              onNav: _go,
              initialExam: _practiceExam,
              onStart: (_) {},
            );
          case 2:
            body = MockListScreen(
              navIndex: _index,
              onNav: _go,
              initialExam: _mockExam,
            );
          case 3:
            body = DashboardScreen(
              navIndex: _index,
              onNav: _go,
              onDeepLink: _onDashboardLink,
            );
          default:
            body = HomeScreen(
              navIndex: _index,
              onNav: _go,
              onPracticeExam: (exam) {
                _practiceExam = exam;
                _go(1);
              },
              courseStore: shared?.courseStore,
              courses: shared?.courses ?? const [],
              onResumeChapter: shared == null
                  ? null
                  : ({required courseExam, required chapterId}) =>
                      _resumeChapter(
                        shared,
                        courseExam: courseExam,
                        chapterId: chapterId,
                      ),
            );
        }
        return PushScope(
          onPush: (route) {
            if (shared != null) _push(route, shared);
          },
          child: body,
        );
      },
    );
  }
}

class _SharedData {
  final CommunityStore community;
  final CourseProgressStore courseStore;
  final List<Course> courses;
  _SharedData({
    required this.community,
    required this.courseStore,
    required this.courses,
  });
}
