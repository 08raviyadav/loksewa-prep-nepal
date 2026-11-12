/// Chapter reader — mirrors vanilla renderCourseChapter()
/// (app.js "Theory courses" section):
///
/// clean typography, EN/NE follows app language, key-points card,
/// per-topic "✏️ Practice this chapter" buttons that deep-link into practice
/// filtered by linked_topics, "Mark as read" toggle, prev/next chapter nav.
///
/// Also exposes [ContinueStudyingCard]: the reusable Home "📚 Continue
/// studying" card (vanilla renderContinueStudying()). Do NOT edit
/// home_screen.dart — instead drop this widget into the Home screen's list
/// at integration time; it hides itself when nothing is started or all is
/// done, exactly like vanilla.
library;

import 'package:flutter/material.dart';

import '../../l10n/courses_strings.dart';
import '../../models/course.dart';
import '../../widgets/app_scaffold.dart';
import '../../state/course_progress_store.dart';

/// Deep-link convention into Practice (final-integration hook):
/// when the user taps a linked topic, the chapter reader calls
/// [onPracticeTopic] with the course's exam id (as in data/courses, e.g.
/// 'nayab-subba') and the bank-verified topic string (e.g. 'Science & Tech').
/// The integrator (RootNav/main.dart) is responsible for:
///   1. mapping the course exam id to the practice-exam id via
///      [courseExamMap] — same mapping as vanilla COURSE_EXAM_MAP
///      (kharidar->kharidar, nayab-subba->nasu, section-officer->section-officer);
///   2. navigating to the Practice tab with that exam + the single topic
///      preselected, then starting the practice run — same effect as
///      vanilla's practiceChapterTopic()/startPracticeTopic(topic).
typedef OnPracticeTopic = void Function({
  required String courseExam,
  required String topic,
});

/// Resume callback convention for ContinueStudyingCard: open the given
/// course + chapter in the Courses flow — same effect as vanilla's
/// courseNav={exam,subject,chapter};showView('courses').
typedef OnResumeChapter = void Function({
  required String courseExam,
  required String chapterId,
});

class ChapterReaderScreen extends StatefulWidget {
  final CourseProgressStore store;
  final List<Course> courses;
  final String exam;
  final String chapterId;
  final OnPracticeTopic? onPracticeTopic;

  const ChapterReaderScreen({
    super.key,
    required this.store,
    required this.courses,
    required this.exam,
    required this.chapterId,
    this.onPracticeTopic,
  });

  @override
  State<ChapterReaderScreen> createState() => _ChapterReaderScreenState();
}

class _ChapterReaderScreenState extends State<ChapterReaderScreen> {
  Course? get _course {
    for (final c in widget.courses) {
      if (c.exam == widget.exam) return c;
    }
    return null;
  }

  @override
  void initState() {
    super.initState();
    // Vanilla openCourseChapter records last={exam, chId, ts} on open.
    widget.store.markOpened(widget.exam, widget.chapterId);
  }

  void _openChapter(String chapterId) {
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => ChapterReaderScreen(
          store: widget.store,
          courses: widget.courses,
          exam: widget.exam,
          chapterId: chapterId,
          onPracticeTopic: widget.onPracticeTopic,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final course = _course;
    final found = course?.chapterById(widget.chapterId);
    if (course == null || found == null) {
      return Scaffold(
        appBar: AppBar(),
        body: Center(child: Text(s.chapterNotFound)),
      );
    }
    final subject = found.subject;
    final ch = found.chapter;
    final flat = course.flatten();
    final idx = flat.indexWhere((r) => r.chapter.id == ch.id);
    final prev = idx > 0 ? flat[idx - 1] : null;
    final next = idx >= 0 && idx < flat.length - 1 ? flat[idx + 1] : null;
    final isNe = s.isNe;

    return AnimatedBuilder(
      animation: widget.store,
      builder: (context, _) {
        final done = widget.store.isDone(ch.id);
        return Scaffold(
          appBar: AppBar(
            title: Text(
              subject.name(isNe),
              style: Theme.of(context).textTheme.titleMedium,
            ),
          ),
          body: ListView(
            padding: const EdgeInsets.fromLTRB(20, 12, 20, 24),
            children: [
              Text(
                '${course.title(isNe)} · ${subject.name(isNe)}',
                style: Theme.of(context).textTheme.bodySmall,
              ),
              const SizedBox(height: 4),
              Text(
                ch.title(isNe),
                style: Theme.of(context)
                    .textTheme
                    .headlineSmall
                    ?.copyWith(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),
              // Theory body — clean typography, selectable like vanilla text.
              ...ch.paragraphs(isNe).map(
                    (p) => Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: SelectableText(
                        p,
                        style: Theme.of(context)
                            .textTheme
                            .bodyLarge
                            ?.copyWith(height: 1.6),
                      ),
                    ),
                  ),
              // Key points card — vanilla .keypoints box.
              if (ch.keyPoints.isNotEmpty)
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          s.keyPointsHeading,
                          style: Theme.of(context)
                              .textTheme
                              .titleMedium
                              ?.copyWith(fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        ...ch.keyPoints.map(
                          (k) => Padding(
                            padding: const EdgeInsets.only(bottom: 6),
                            child: Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text('• '),
                                Expanded(child: Text(k.text(isNe))),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              const SizedBox(height: 16),
              // Per-topic practice deep-links — vanilla .chapter-practice.
              if (ch.linkedTopics.isNotEmpty)
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      s.practiceThisChapter,
                      style: Theme.of(context)
                          .textTheme
                          .titleSmall
                          ?.copyWith(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: ch.linkedTopics.map((t) {
                        return OutlinedButton(
                          onPressed: widget.onPracticeTopic == null
                              ? null
                              : () => widget.onPracticeTopic!(
                                    courseExam: course.exam,
                                    topic: t,
                                  ),
                          child: Text('✏️ $t'),
                        );
                      }).toList(),
                    ),
                  ],
                ),
              const SizedBox(height: 16),
              // Mark as read toggle — vanilla toggleChapterRead().
              SizedBox(
                width: double.infinity,
                child: FilledButton.tonal(
                  onPressed: () => widget.store.toggle(ch.id),
                  child: Text(done ? s.readMarkUnread : s.markAsRead),
                ),
              ),
              const SizedBox(height: 24),
              // Prev/next nav.
              Row(
                children: [
                  Expanded(
                    child: prev == null
                        ? const SizedBox.shrink()
                        : OutlinedButton(
                            onPressed: () => _openChapter(prev.chapter.id),
                            child: Text(
                              '${s.previousChapter} ${prev.chapter.title(isNe)}',
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                  ),
                  if (prev != null && next != null) const SizedBox(width: 8),
                  Expanded(
                    child: next == null
                        ? const SizedBox.shrink()
                        : OutlinedButton(
                            onPressed: () => _openChapter(next.chapter.id),
                            child: Text(
                              '${next.chapter.title(isNe)} ${s.nextChapter}',
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                  ),
                ],
              ),
            ],
          ),
        );
      },
    );
  }
}

// --- Home "Continue studying" card (vanilla renderContinueStudying) ---

/// Drop-in Home card. Hidden (returns SizedBox.shrink) when there is no
/// resumable chapter (nothing started yet, last chapter deleted/unknown, or
/// every chapter in that course is marked read) — exactly vanilla's
/// renderContinueStudying visibility rules.
///
/// INTEGRATION NOTE for the parent agent: add this widget to HomeScreen's
/// content (e.g. under the hero) with the app's CourseProgressStore +
/// loaded courses; do NOT edit home_screen.dart in this milestone.
class ContinueStudyingCard extends StatelessWidget {
  final CourseProgressStore store;
  final List<Course> courses;
  final OnResumeChapter onResume;

  const ContinueStudyingCard({
    super.key,
    required this.store,
    required this.courses,
    required this.onResume,
  });

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    return AnimatedBuilder(
      animation: store,
      builder: (context, _) {
        final last = store.last;
        if (last == null) return const SizedBox.shrink();
        Course? course;
        for (final c in courses) {
          if (c.exam == last.exam) course = c;
        }
        final found = course?.chapterById(last.chapterId);
        if (course == null || found == null) return const SizedBox.shrink();
        final st = course.progress(store.done);
        // Local copies: `course`/`found` are captured by the button closure,
        // where null-promotion does not apply.
        final examId = course.exam;
        final chId = found.chapter.id;
        if (st.done >= st.total) return const SizedBox.shrink();

        return Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        s.continueStudyingTitle,
                        style: Theme.of(context)
                            .textTheme
                            .titleMedium
                            ?.copyWith(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        '${course.title(s.isNe)} — ${s.continueStudyingSub(found.chapter.title(s.isNe), st.pct)}',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                  ),
                ),
                FilledButton(
                  onPressed: () =>
                      onResume(courseExam: examId, chapterId: chId),
                  child: Text(s.resume),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
