/// Courses view — mirrors vanilla renderCourses()/renderCourseDetail()
/// (app.js "Theory courses" section).
///
/// Flow: exam picker cards (SVG-style progress rings) -> tap opens the course
/// detail (subject accordions with progress bars -> chapter list with
/// ✅/⬜ read ticks) -> tap opens ChapterReaderScreen.
library;

import 'package:flutter/material.dart';

import '../../l10n/app_strings.dart';
import '../../l10n/courses_strings.dart';
import '../../models/course.dart';
import '../../widgets/app_scaffold.dart';
import '../../state/course_progress_store.dart';
import 'chapter_reader_screen.dart';
import 'course_progress_ring.dart';

class CoursesScreen extends StatefulWidget {
  /// Store + data shared with the final integration (RootNav).
  final CourseProgressStore store;
  final List<Course> courses;

  const CoursesScreen({super.key, required this.store, required this.courses});

  @override
  State<CoursesScreen> createState() => _CoursesScreenState();
}

class _CoursesScreenState extends State<CoursesScreen> {
  /// Vanilla courseNav.exam — null = exam picker.
  String? _exam;

  /// Vanilla courseNav.subject — expanded accordion index, -1 = none.
  int _subject = -1;

  void _openChapter(Course course, String chapterId) {
    widget.store.markOpened(course.exam, chapterId);
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => ChapterReaderScreen(
          store: widget.store,
          courses: widget.courses,
          exam: course.exam,
          chapterId: chapterId,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStateScope.of(context).strings;
    final examId = _exam;
    if (examId == null) return _examPicker(context, s);
    final course = widget.courses.where((c) => c.exam == examId);
    if (course.isEmpty) {
      // Defensive — vanilla renderCourseDetail resets nav on missing course.
      _exam = null;
      return _examPicker(context, s);
    }
    return _courseDetail(context, s, course.first);
  }

  // --- Exam picker (vanilla renderCourses, exam list) ---
  Widget _examPicker(BuildContext context, AppStrings s) {
    return AnimatedBuilder(
      animation: widget.store,
      builder: (context, _) {
        if (widget.courses.isEmpty) {
          return Scaffold(
            appBar: AppBar(title: Text(s.coursesTitle)),
            body: Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Text('📚', style: TextStyle(fontSize: 48)),
                    const SizedBox(height: 12),
                    Text(
                      s.noCoursesYet,
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      s.coursesOnWay,
                      style: Theme.of(context).textTheme.bodySmall,
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            ),
          );
        }
        return Scaffold(
          appBar: AppBar(title: Text(s.coursesTitle)),
          body: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              Text(
                s.coursesSubtitle,
                style: Theme.of(context).textTheme.bodySmall,
              ),
              const SizedBox(height: 16),
              ...widget.courses.map((c) {
                final st = c.progress(widget.store.done);
                final isNe = s.isNe;
                final needsReverify = c.confidence == 'medium';
                return Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            CourseProgressRing(pct: st.pct),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    c.title(isNe),
                                    style:
                                        Theme.of(context).textTheme.titleMedium,
                                  ),
                                  Text(
                                    s.firstPaperTheory,
                                    style:
                                        Theme.of(context).textTheme.bodySmall,
                                  ),
                                  if (needsReverify)
                                    Padding(
                                      padding: const EdgeInsets.only(top: 4),
                                      child: Chip(
                                        label: Text(
                                          s.syllabusReverify,
                                          style: Theme.of(context)
                                              .textTheme
                                              .labelSmall,
                                        ),
                                        visualDensity: VisualDensity.compact,
                                      ),
                                    ),
                                  const SizedBox(height: 4),
                                  Text(
                                    s.chaptersRead(st.done),
                                    style:
                                        Theme.of(context).textTheme.bodySmall,
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        SizedBox(
                          width: double.infinity,
                          child: FilledButton(
                            onPressed: () => setState(() {
                              _exam = c.exam;
                              _subject = -1;
                            }),
                            child: Text(
                              st.done > 0
                                  ? s.continueStudying
                                  : s.startStudying,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              }),
            ],
          ),
        );
      },
    );
  }

  // --- Course detail (vanilla renderCourseDetail) ---
  Widget _courseDetail(BuildContext context, AppStrings s, Course course) {
    final isNe = s.isNe;
    return AnimatedBuilder(
      animation: widget.store,
      builder: (context, _) {
        final st = course.progress(widget.store.done);
        return Scaffold(
          appBar: AppBar(
            title: Text(course.title(isNe)),
            leading: IconButton(
              icon: const Icon(Icons.arrow_back),
              onPressed: () => setState(() {
                _exam = null;
                _subject = -1;
              }),
            ),
          ),
          body: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          CourseProgressRing(pct: st.pct, size: 72),
                          const SizedBox(width: 16),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                '${st.pct}% ${s.complete}',
                                style: Theme.of(context).textTheme.titleMedium,
                              ),
                              Text(
                                '${st.done}/${st.total} ${s.chaptersLabel}',
                                style: Theme.of(context).textTheme.bodySmall,
                              ),
                            ],
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(4),
                        child: LinearProgressIndicator(
                          value: st.total == 0 ? 0 : st.done / st.total,
                          minHeight: 8,
                          semanticsLabel: '${st.pct}% ${s.complete}',
                          semanticsValue: '${st.done}/${st.total}',
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 8),
              ...course.subjects.asMap().entries.map((entry) {
                final si = entry.key;
                final subj = entry.value;
                final sp = subj.progress(widget.store.done);
                final open = _subject == si;
                return Card(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: Column(
                    children: [
                      ListTile(
                        title: Text(
                          subj.name(isNe),
                          style: Theme.of(context).textTheme.titleSmall,
                        ),
                        subtitle: Text('${sp.done}/${sp.total}'),
                        trailing: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            SizedBox(
                              width: 72,
                              child: ClipRRect(
                                borderRadius: BorderRadius.circular(4),
                                child: LinearProgressIndicator(
                                  value: sp.total == 0 ? 0 : sp.done / sp.total,
                                  minHeight: 6,
                                ),
                              ),
                            ),
                            const SizedBox(width: 8),
                            Icon(open ? Icons.expand_less : Icons.expand_more),
                          ],
                        ),
                        onTap: () => setState(() => _subject = open ? -1 : si),
                      ),
                      if (open)
                        ...subj.chapters.map((ch) {
                          final chDone = widget.store.isDone(ch.id);
                          return ListTile(
                            leading: Text(chDone ? '✅' : '⬜'),
                            title: Text(ch.title(isNe)),
                            subtitle: Text(
                              s.keyPointsCount(ch.keyPoints.length),
                              style: Theme.of(context).textTheme.bodySmall,
                            ),
                            trailing: const Icon(Icons.chevron_right),
                            onTap: () => _openChapter(course, ch.id),
                          );
                        }),
                    ],
                  ),
                );
              }),
            ],
          ),
        );
      },
    );
  }
}
