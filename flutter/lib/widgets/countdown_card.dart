import 'dart:async';

import 'package:flutter/material.dart';

import '../models/models.dart';
import '../theme/app_theme.dart';
import '../utils/bs_calendar.dart';
import '../utils/countdown.dart';
import 'app_scaffold.dart';

/// "Next exam" live countdown card — the second reminder display type.
///
/// Mirrors the vanilla site's #next-exam-card: big ticking DD:HH:MM:SS,
/// swipeable pager over the 30-day window (swipe left/right or tap the
/// dots), today/near/far states, remind toggle.
class CountdownCard extends StatefulWidget {
  final List<ExamDate> dates;
  final void Function(ExamDate date)? onPractice;

  const CountdownCard({super.key, required this.dates, this.onPractice});

  @override
  State<CountdownCard> createState() => _CountdownCardState();
}

class _CountdownCardState extends State<CountdownCard> {
  Timer? _timer;
  int _pagerIndex = 0;
  int _slideDir = 1; // +1 swiped to next exam, -1 to previous
  double _dragDx = 0;
  DateTime _now = DateTime.now().toUtc();
  final ScrollController _dotsController = ScrollController();

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (!mounted) return;
      setState(() => _now = DateTime.now().toUtc());
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _dotsController.dispose();
    super.dispose();
  }

  /// Switches the shown exam (swipe or dot tap), clamped to the pager.
  void _setPage(int i, int dir, int count) {
    if (count <= 0) return;
    final next = i.clamp(0, count - 1);
    if (next == _pagerIndex) return;
    setState(() {
      _pagerIndex = next;
      _slideDir = dir;
    });
    _scrollDotsToActive();
  }

  /// Keeps the active dot visible when the dots row scrolls.
  void _scrollDotsToActive() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!_dotsController.hasClients) return;
      final pos = _dotsController.position;
      final target =
          (_pagerIndex * _PagerDots.dotHit + _PagerDots.dotHit / 2 - pos.viewportDimension / 2)
              .clamp(0.0, pos.maxScrollExtent);
      _dotsController.jumpTo(target);
    });
  }

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    final ne = state.isNe;

    final pager = nxPagerList(widget.dates);
    final nearest = nxPickNearest(widget.dates);
    if (nearest == null) return const SizedBox.shrink();

    final shown =
        pager.isEmpty ? nearest : pager[_pagerIndex.clamp(0, pager.length - 1)];
    final daysUntil = bsDaysUntil(shown.dateBs);
    final cardState = nxCardState(daysUntil);
    if (cardState == CountdownState.none) return const SizedBox.shrink();

    final targetMs = nxTargetMs(shown.dateBs);
    final remaining = nxRemaining(
      targetMs,
      nowUtcMs: _now.millisecondsSinceEpoch,
    );
    final parts = splitDuration(remaining);

    final isToday = cardState == CountdownState.today;
    final isFar = cardState == CountdownState.far;

    // Swipe left/right through the upcoming exams. A horizontal drag
    // wins the gesture arena over the home list's vertical scroll, so
    // swiping the card pages it while scrolling the page still works.
    // Distance (>60px) or a quick flick (>300px/s) both turn the page.
    return GestureDetector(
      onHorizontalDragUpdate: (d) => _dragDx += d.delta.dx,
      onHorizontalDragEnd: (d) {
        final v = d.velocity.pixelsPerSecond.dx;
        if (_dragDx < -60 || v < -300) {
          _setPage(_pagerIndex + 1, 1, pager.length);
        } else if (_dragDx > 60 || v > 300) {
          _setPage(_pagerIndex - 1, -1, pager.length);
        }
        _dragDx = 0;
      },
      onHorizontalDragCancel: () => _dragDx = 0,
      child: Card(
        margin: const EdgeInsets.all(AppSpacing.s4),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: AppRadius.lgAll,
            gradient: isFar
                ? null
                : const LinearGradient(
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                    colors: [Color(0xFF3B2F0B), Color(0xFF1E1B4B)],
                  ),
            border: Border.all(
              color: isFar ? AppColors.border : AppColors.accentLine,
              width: 1.5,
            ),
          ),
          padding: const EdgeInsets.all(AppSpacing.s5),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              AnimatedSwitcher(
                duration: const Duration(milliseconds: 250),
                transitionBuilder: (child, animation) {
                  final slide = Tween<Offset>(
                    begin: Offset(_slideDir * 0.25, 0),
                    end: Offset.zero,
                  ).animate(animation);
                  return SlideTransition(
                    position: slide,
                    child: FadeTransition(
                      opacity: animation,
                      child: child,
                    ),
                  );
                },
                child: Column(
                  key: ValueKey(_pagerIndex),
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(
                          Icons.alarm,
                          color: AppColors.accent,
                          size: 20,
                        ),
                        const SizedBox(width: AppSpacing.s2),
                        Text(
                          s.nextExam,
                          style:
                              AppType.small.copyWith(color: AppColors.muted),
                        ),
                        const Spacer(),
                        _KindChip(
                          kind: shown.kind,
                          label: s.examKindLabel(shown.kind),
                        ),
                      ],
                    ),
                    const SizedBox(height: AppSpacing.s2),
                    Text(
                      shown.title(ne),
                      style: AppType.h2,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    Text(
                      fmtBs(shown.dateBs, ne: ne),
                      style: AppType.small.copyWith(color: AppColors.muted),
                    ),
                    const SizedBox(height: AppSpacing.s4),
                    if (isToday)
                      Text(
                        s.todayBang,
                        style: AppType.display.copyWith(
                          color: AppColors.accent,
                        ),
                      )
                    else
                      _Digits(parts: parts, ne: ne),
                  ],
                ),
              ),
              const SizedBox(height: AppSpacing.s4),
              if (pager.length > 1)
                _PagerDots(
                  count: pager.length,
                  index: _pagerIndex.clamp(0, pager.length - 1),
                  controller: _dotsController,
                  onTap: (i) => _setPage(
                    i,
                    i > _pagerIndex ? 1 : -1,
                    pager.length,
                  ),
                ),
            Row(
              children: [
                // Expanded so the buttons share the width instead of
                // overflowing on narrow screens / large text sizes.
                Expanded(
                  child: FilledButton.icon(
                    onPressed: widget.onPractice == null
                        ? null
                        : () => widget.onPractice!(shown),
                    icon: const Icon(Icons.play_arrow, size: 18),
                    label: Text(s.practiceNow),
                    style: FilledButton.styleFrom(
                      backgroundColor: AppColors.accent,
                      foregroundColor: AppColors.accentInk,
                      minimumSize: const Size(44, 44),
                    ),
                  ),
                ),
                const SizedBox(width: AppSpacing.s3),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () => state.toggleReminder(shown.id),
                    icon: Icon(
                      state.hasReminder(shown.id)
                          ? Icons.notifications_active
                          : Icons.notifications_none,
                      size: 18,
                    ),
                    label: Text(
                      state.hasReminder(shown.id) ? s.remindOn : s.remindOff,
                    ),
                    style: OutlinedButton.styleFrom(
                      minimumSize: const Size(44, 44),
                      side: const BorderSide(color: AppColors.accentLine),
                    ),
                  ),
                ),
              ],
            ),
            if (shown.confidence == 'medium') ...[
              const SizedBox(height: AppSpacing.s2),
              Text(
                s.reverifyNote,
                style: AppType.tiny.copyWith(color: AppColors.accent),
              ),
            ],
          ],
        ),
      ),
    ),
    );
  }
}

class _KindChip extends StatelessWidget {
  final String kind;
  final String label;
  const _KindChip({required this.kind, required this.label});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.s3,
        vertical: AppSpacing.s1,
      ),
      decoration: BoxDecoration(
        color: AppColors.accentSoft,
        borderRadius: const BorderRadius.all(AppRadius.pill),
        border: Border.all(color: AppColors.accentLine),
      ),
      child: Text(
        label,
        style: AppType.tiny.copyWith(
          color: AppColors.accent,
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }
}

class _Digits extends StatelessWidget {
  final ({String dd, String hh, String mm, String ss}) parts;
  final bool ne;
  const _Digits({required this.parts, required this.ne});

  @override
  Widget build(BuildContext context) {
    // One row, always: each unit gets an equal share and the digits
    // scale down rather than wrapping (the old Wrap dropped "sec" onto
    // a second row on phone widths).
    Widget digit(String v, String label) => Expanded(
          child: Column(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.s2,
                  vertical: AppSpacing.s2,
                ),
                decoration: BoxDecoration(
                  color: Colors.black.withValues(alpha: 0.35),
                  borderRadius: AppRadius.mdAll,
                  border: Border.all(color: AppColors.borderSoft),
                ),
                child: FittedBox(
                  fit: BoxFit.scaleDown,
                  child: Text(
                    ne ? neDigits(v) : v,
                    style: AppType.countdownDigit.copyWith(
                      color: AppColors.accent,
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 2),
              Text(label, style: AppType.tiny.copyWith(color: AppColors.muted)),
            ],
          ),
        );
    Widget sep() => const Padding(
          padding: EdgeInsets.symmetric(horizontal: 2),
          child: Text(':', style: AppType.countdownDigit),
        );
    return Row(
      children: [
        digit(parts.dd, ne ? 'दिन' : 'days'),
        sep(),
        digit(parts.hh, ne ? 'घण्टा' : 'hrs'),
        sep(),
        digit(parts.mm, ne ? 'मिनेट' : 'min'),
        sep(),
        digit(parts.ss, ne ? 'सेकेन्ड' : 'sec'),
      ],
    );
  }
}

class _PagerDots extends StatelessWidget {
  /// Tap-target width per dot. The old 44px targets overflowed the
  /// card once there were 8+ exams in the window (dots ran off the
  /// right edge); 32px fits 9 dots, and beyond that the row scrolls.
  static const double dotHit = 32;

  final int count;
  final int index;
  final ValueChanged<int> onTap;
  final ScrollController controller;
  const _PagerDots({
    required this.count,
    required this.index,
    required this.onTap,
    required this.controller,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppSpacing.s3),
      child: LayoutBuilder(
        builder: (context, constraints) {
          final fits = count * dotHit <= constraints.maxWidth;
          return SingleChildScrollView(
            controller: controller,
            scrollDirection: Axis.horizontal,
            // When the dots fit, the row must not claim horizontal
            // drags — otherwise a swipe starting on the dots scrolls
            // this row instead of paging the card.
            physics: fits ? const NeverScrollableScrollPhysics() : null,
            child: SizedBox(
              // Center the dots when they fit; let them scroll when not.
              width: fits ? constraints.maxWidth : null,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(
                  count,
                  (i) => GestureDetector(
                    onTap: () => onTap(i),
                    child: Container(
                      width: dotHit,
                      height: dotHit,
                      alignment: Alignment.center,
                      child: Container(
                        width: i == index ? 22 : 8,
                        height: 8,
                        decoration: BoxDecoration(
                          borderRadius:
                              const BorderRadius.all(AppRadius.pill),
                          color:
                              i == index ? AppColors.accent : AppColors.faint,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
