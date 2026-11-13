/// First-launch guided tour (v1.0.7, 8 steps since v1.0.9): an
/// interactive coachmark tour over the real UI.
///
/// Each step highlights one real widget — a dim scrim covers everything
/// except a hole over the target, so the target stays tappable. On
/// "tap" steps the user's tap on the real button performs the real
/// action (navigate, pick an exam, start the quiz) AND advances the
/// tour. Every step also has a Next button (v1.0.9): on tap steps Next
/// performs the step's action programmatically via the registered
/// action — the same handler the real tap uses — so the tour never
/// strands the user on a step with no way forward but Skip.
///
/// The tour runs once (SharedPreferences flag `loksewa_tour_done_v1`,
/// set on skip or completion) and can be replayed from the drawer
/// ("How to use the app").
///
/// Implementation notes:
/// * The dim is FOUR rectangles around the target (top/bottom/left/
///   right strips), not one layer with a hole — so nothing sits over
///   the target and taps reach the real button naturally. The strips
///   swallow taps elsewhere.
/// * Target rects come from GlobalKeys. If a target is not mounted when
///   its step becomes active (screen still loading, user navigated
///   away), the overlay waits ~5s of frames and then skips the step —
///   the tour never blocks the app and never crashes.
/// * The overlay lives in MaterialApp.builder, above the Navigator, so
///   it also covers pushed routes. It re-measures the target every
///   frame while active, so the highlight follows scrolling.
library;

import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../l10n/app_strings.dart';
import '../l10n/tour_strings.dart';
import '../theme/app_theme.dart';
import '../widgets/app_scaffold.dart';

/// Localised text for one tour step (resolved at build time so a
/// language switch mid-tour still shows the right language).
typedef TourText = String Function(AppStrings strings);

/// One coachmark step.
class TourStep {
  final String id;
  final TourText title;
  final TourText body;

  /// The widget to highlight.
  final GlobalKey targetKey;

  /// If set, the target is tab [tabIndex] of the bottom navigation bar
  /// (the bar's rect is split into 4 equal tabs — BottomNavigationBar
  /// with fixed type lays its items out evenly).
  final int? tabIndex;

  /// True when tapping the highlighted widget itself advances the tour
  /// (the widget's own handler calls [TourController.advanceIfOn]).
  /// False steps show a Next button instead.
  final bool advanceOnTap;

  const TourStep({
    required this.id,
    required this.title,
    required this.body,
    required this.targetKey,
    this.tabIndex,
    this.advanceOnTap = false,
  });
}

/// GlobalKeys for the tour's targets. Attached to the real widgets:
/// the Daily Challenge card, the app-bar language button (Home screen
/// only), the bottom navigation bar (tab screens only — one tab screen
/// is mounted at a time, so the key never duplicates), and the Practice
/// screen's first category tile, first exam chip, first topic chip and
/// Start button.
class TourKeys {
  static final GlobalKey dailyChallenge =
      GlobalKey(debugLabel: 'tour_daily');
  static final GlobalKey langToggle = GlobalKey(debugLabel: 'tour_lang');
  static final GlobalKey bottomNav = GlobalKey(debugLabel: 'tour_bottom_nav');
  static final GlobalKey firstCategory =
      GlobalKey(debugLabel: 'tour_category');
  static final GlobalKey firstExamChip = GlobalKey(debugLabel: 'tour_exam');
  static final GlobalKey firstTopicChip = GlobalKey(debugLabel: 'tour_topic');
  static final GlobalKey startButton = GlobalKey(debugLabel: 'tour_start');
}

/// The 8-step first-launch tour.
///
/// Why 8 and not 5: the Practice screen has no exam-detail sheet —
/// exams live in collapsed category sections and the Start button stays
/// disabled until a topic is picked. So the "select then start" leg
/// needs its own steps: category -> exam -> topic -> Start. Step 2
/// (v1.0.9) guides the language switcher.
List<TourStep> get defaultTourSteps => [
      TourStep(
        id: 'daily',
        title: (s) => s.tourDailyTitle,
        body: (s) => s.tourDailyBody,
        targetKey: TourKeys.dailyChallenge,
      ),
      TourStep(
        id: 'langToggle',
        title: (s) => s.tourLangTitle,
        body: (s) => s.tourLangBody,
        targetKey: TourKeys.langToggle,
        advanceOnTap: true,
      ),
      TourStep(
        id: 'dashboardTab',
        title: (s) => s.tourDashboardTitle,
        body: (s) => s.tourDashboardBody,
        targetKey: TourKeys.bottomNav,
        tabIndex: 3,
      ),
      TourStep(
        id: 'practiceTab',
        title: (s) => s.tourPracticeTitle,
        body: (s) => s.tourPracticeBody,
        targetKey: TourKeys.bottomNav,
        tabIndex: 1,
        advanceOnTap: true,
      ),
      TourStep(
        id: 'firstCategory',
        title: (s) => s.tourCategoryTitle,
        body: (s) => s.tourCategoryBody,
        targetKey: TourKeys.firstCategory,
        advanceOnTap: true,
      ),
      TourStep(
        id: 'firstExamChip',
        title: (s) => s.tourExamTitle,
        body: (s) => s.tourExamBody,
        targetKey: TourKeys.firstExamChip,
        advanceOnTap: true,
      ),
      TourStep(
        id: 'firstTopicChip',
        title: (s) => s.tourTopicTitle,
        body: (s) => s.tourTopicBody,
        targetKey: TourKeys.firstTopicChip,
        advanceOnTap: true,
      ),
      TourStep(
        id: 'startButton',
        title: (s) => s.tourStartTitle,
        body: (s) => s.tourStartBody,
        targetKey: TourKeys.startButton,
        advanceOnTap: true,
      ),
    ];

/// Tour state. Created once in [VidyapeethApp] and provided via
/// [TourScope]; screens reach it with `TourScope.of(context)` (null
/// when no scope is above — e.g. in tests that pump a bare screen).
class TourController extends ChangeNotifier {
  static const String doneKey = 'loksewa_tour_done_v1';

  final List<TourStep> steps;
  int _index = 0;
  bool _active = false;

  /// Step actions (v1.0.9): the real handlers the highlighted buttons
  /// use, registered by the owning screens (RootNav, PracticeScreen,
  /// AppScaffold) so the tooltip's Next button can perform a tap
  /// step's action programmatically. Registration is idempotent —
  /// screens re-register on every build.
  final Map<String, VoidCallback> _actions = {};

  TourController({List<TourStep>? steps})
      : steps = steps ?? defaultTourSteps;

  bool get isActive => _active;
  int get currentIndex => _index;
  int get stepCount => steps.length;
  TourStep? get currentStep =>
      _active && _index < steps.length ? steps[_index] : null;

  void registerAction(String stepId, VoidCallback action) {
    _actions[stepId] = action;
  }

  /// Runs the current step's registered action and returns true; false
  /// when no action is registered for the step (plain Next steps).
  /// The real handlers advance the tour via [advanceIfOn]; if the step
  /// is still current afterwards (a guarded handler), advance anyway
  /// so Next never leaves the tour stuck.
  bool performCurrentAction() {
    final step = currentStep;
    if (step == null) return false;
    final action = _actions[step.id];
    if (action == null) return false;
    action();
    if (currentStep?.id == step.id) next();
    return true;
  }

  static Future<bool> isTourDone() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(doneKey) ?? false;
  }

  /// Starts the tour from step 1, unless it was already completed or
  /// skipped (or is already running).
  Future<void> start() async {
    if (_active || steps.isEmpty) return;
    if (await isTourDone()) return;
    _active = true;
    _index = 0;
    notifyListeners();
  }

  /// Restarts the tour from step 1 (drawer replay): clears the done
  /// flag first so [start]'s guard doesn't block it.
  Future<void> replay() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(doneKey);
    _active = true;
    _index = 0;
    notifyListeners();
  }

  /// Moves to the next step; past the last step the tour completes.
  void next() {
    if (!_active) return;
    if (_index + 1 >= steps.length) {
      complete();
      return;
    }
    _index++;
    notifyListeners();
  }

  /// Advances only when the tour is currently on [stepId]. Called by
  /// the real widgets' own tap handlers, so a tap on the highlighted
  /// button performs its real action and moves the tour on.
  void advanceIfOn(String stepId) {
    if (!_active) return;
    if (currentStep?.id == stepId) next();
  }

  /// Ends the tour early (Skip button). Marks it done so it never
  /// auto-starts again.
  Future<void> skip() => complete();

  /// Ends the tour and marks it done.
  Future<void> complete() async {
    if (!_active) return;
    _active = false;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(doneKey, true);
  }
}

/// InheritedWidget provider for the [TourController]. The lookup does
/// NOT register a dependency (widgets listen to the controller itself),
/// so it is safe to call from event handlers and post-frame callbacks.
class TourScope extends InheritedWidget {
  final TourController controller;
  const TourScope({
    super.key,
    required this.controller,
    required super.child,
  });

  static TourController? of(BuildContext context) {
    final element =
        context.getElementForInheritedWidgetOfExactType<TourScope>();
    if (element == null) return null;
    return (element.widget as TourScope).controller;
  }

  @override
  bool updateShouldNotify(TourScope oldWidget) =>
      controller != oldWidget.controller;
}

/// The coachmark overlay: dim strips + highlight ring + tooltip card.
/// Renders nothing while the tour is inactive or the current step's
/// target is not (yet) on screen.
class TourOverlay extends StatefulWidget {
  const TourOverlay({super.key});

  @override
  State<TourOverlay> createState() => _TourOverlayState();
}

class _TourOverlayState extends State<TourOverlay>
    with SingleTickerProviderStateMixin {
  Rect? _targetRect;
  String? _stepId;
  int _missingFrames = 0;
  late final Ticker _ticker;
  TourController? _controller;

  /// Frames to wait for a missing target before skipping its step
  /// (~5s at 60fps). Covers async loads (exam list, topics) and the
  /// Practice screen's scroll-into-view; a target that never appears
  /// (user navigated away) is skipped instead of blocking the app.
  static const _maxMissingFrames = 300;

  @override
  void initState() {
    super.initState();
    // A Ticker (not a post-frame callback chain): post-frame callbacks
    // only run when something else schedules a frame, so a chain
    // stalls — the ticker fires every vsync while the tour is active.
    _ticker = createTicker(_onTick);
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final controller = TourScope.of(context);
    if (controller != _controller) {
      _controller?.removeListener(_onControllerChanged);
      _controller = controller;
      _controller?.addListener(_onControllerChanged);
      _onControllerChanged();
    }
  }

  @override
  void dispose() {
    _controller?.removeListener(_onControllerChanged);
    _ticker.dispose();
    super.dispose();
  }

  void _onControllerChanged() {
    final active = _controller?.currentStep != null;
    if (active) {
      if (!_ticker.isTicking) _ticker.start();
    } else if (_ticker.isTicking) {
      _ticker.stop();
    }
  }

  @override
  Widget build(BuildContext context) {
    final controller = TourScope.of(context);
    if (controller == null) return const SizedBox.shrink();
    return AnimatedBuilder(
      animation: controller,
      builder: (context, _) {
        final step = controller.currentStep;
        if (step == null) return const SizedBox.shrink();
        final rect = _targetRect;
        if (rect == null) return const SizedBox.shrink();
        return _buildOverlay(context, controller, step, rect);
      },
    );
  }

  /// Re-measures the target every frame while the tour is active, so
  /// the highlight follows scrolling and layout changes.
  void _onTick(Duration _) {
    if (!mounted) return;
    final controller = _controller;
    final step = controller?.currentStep;
    if (controller == null || step == null) return;
    if (_stepId != step.id) {
      _stepId = step.id;
      _missingFrames = 0;
      _targetRect = null;
    }
    final rect = _rectFor(step);
    if (rect == null) {
      _missingFrames++;
      if (_targetRect != null) {
        setState(() => _targetRect = null);
      }
      if (_missingFrames >= _maxMissingFrames) {
        controller.next();
      }
    } else {
      _missingFrames = 0;
      if (_targetRect != rect) {
        setState(() => _targetRect = rect);
      }
    }
  }

  /// The target's rect in screen coordinates, or null when it is not
  /// mounted (or fully off-screen). For bottom-nav steps the bar's
  /// rect is split into its 4 equal tabs.
  Rect? _rectFor(TourStep step) {
    final box =
        step.targetKey.currentContext?.findRenderObject() as RenderBox?;
    if (box == null || !box.hasSize) return null;
    var rect = box.localToGlobal(Offset.zero) & box.size;
    final tabIndex = step.tabIndex;
    if (tabIndex != null) {
      final tabWidth = rect.width / 4;
      rect = Rect.fromLTWH(
        rect.left + tabWidth * tabIndex,
        rect.top,
        tabWidth,
        rect.height,
      );
    }
    // Clamp to the visible screen so a half-off-screen target still
    // highlights the part the user can see.
    final size = MediaQuery.sizeOf(context);
    final clamped = rect.intersect(Offset.zero & size);
    if (clamped.isEmpty) return null;
    return clamped;
  }

  Widget _buildOverlay(
    BuildContext context,
    TourController controller,
    TourStep step,
    Rect rect,
  ) {
    final palette = AppColors.of(context);
    final size = MediaQuery.sizeOf(context);
    final ring = rect.inflate(4);
    return Stack(
      children: [
        // Dim strips — four rectangles around the target. Nothing sits
        // over the target itself, so taps reach the real button. The
        // strips swallow taps everywhere else.
        if (rect.top > 0)
          Positioned(
            left: 0,
            right: 0,
            top: 0,
            height: rect.top,
            child: _DimStrip(color: palette.scrim),
          ),
        if (rect.bottom < size.height)
          Positioned(
            left: 0,
            right: 0,
            top: rect.bottom,
            bottom: 0,
            child: _DimStrip(color: palette.scrim),
          ),
        if (rect.left > 0)
          Positioned(
            left: 0,
            top: rect.top,
            width: rect.left,
            height: rect.height,
            child: _DimStrip(color: palette.scrim),
          ),
        if (rect.right < size.width)
          Positioned(
            left: rect.right,
            top: rect.top,
            right: 0,
            height: rect.height,
            child: _DimStrip(color: palette.scrim),
          ),
        // Highlight ring around the target (ignores taps).
        Positioned.fromRect(
          rect: ring,
          child: IgnorePointer(
            child: Container(
              decoration: BoxDecoration(
                border: Border.all(color: palette.accent, width: 2.5),
                borderRadius: AppRadius.mdAll,
              ),
            ),
          ),
        ),
        // Tooltip card in the largest free strip (above or below).
        _TourTooltip(
          controller: controller,
          step: step,
          targetRect: rect,
          screenSize: size,
        ),
      ],
    );
  }
}

/// One dim strip: a solid scrim that absorbs taps.
class _DimStrip extends StatelessWidget {
  final Color color;
  const _DimStrip({required this.color});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {}, // swallow — only the highlighted target is tappable
      child: Container(color: color),
    );
  }
}

/// The tooltip card: title + body, step indicator, Skip, and a Next
/// button on EVERY step (v1.0.9 — on tap steps Next performs the
/// highlighted action). Tap steps also show a hint line above the
/// buttons. A small diamond points from the card toward the target.
class _TourTooltip extends StatelessWidget {
  final TourController controller;
  final TourStep step;
  final Rect targetRect;
  final Size screenSize;

  const _TourTooltip({
    required this.controller,
    required this.step,
    required this.targetRect,
    required this.screenSize,
  });

  @override
  Widget build(BuildContext context) {
    final palette = AppColors.of(context);
    final s = AppStateScope.of(context).strings;
    final spaceAbove = targetRect.top;
    final spaceBelow = screenSize.height - targetRect.bottom;
    final below = spaceBelow >= spaceAbove;

    const maxWidth = 360.0;
    const margin = 16.0;
    final width = math.min(screenSize.width - margin * 2, maxWidth);
    final centerX = targetRect.center.dx;
    final left =
        (centerX - width / 2).clamp(margin, screenSize.width - width - margin);

    // Diamond pointer: 12x12 rotated square, half sunk into the card's
    // edge, centred on the target (clamped inside the card).
    const diamond = 12.0;
    final diamondLeft = (centerX - diamond / 2).clamp(
      left + AppSpacing.s4,
      left + width - AppSpacing.s4 - diamond,
    );
    const gap = 16.0; // target edge -> card edge

    final card = Container(
      width: width,
      padding: const EdgeInsets.all(AppSpacing.s4),
      decoration: BoxDecoration(
        color: palette.card,
        borderRadius: AppRadius.lgAll,
        border: Border.all(color: palette.border),
        boxShadow: [
          BoxShadow(
            color: palette.scrim,
            blurRadius: 16,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  step.title(s),
                  style: AppType.h3.copyWith(color: palette.text),
                ),
              ),
              const SizedBox(width: AppSpacing.s2),
              Text(
                '${controller.currentIndex + 1} / ${controller.stepCount}',
                style: AppType.small.copyWith(color: palette.muted),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.s1),
          Text(
            step.body(s),
            style: AppType.body.copyWith(color: palette.text),
          ),
          if (step.advanceOnTap) ...[
            const SizedBox(height: AppSpacing.s2),
            Row(
              children: [
                Icon(
                  Icons.touch_app_outlined,
                  size: 18,
                  color: palette.accent,
                ),
                const SizedBox(width: AppSpacing.s1),
                Expanded(
                  child: Text(
                    s.tourTapHint,
                    style: AppType.small.copyWith(
                      color: palette.muted,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
          ],
          const SizedBox(height: AppSpacing.s3),
          Row(
            children: [
              TextButton(
                onPressed: controller.skip,
                child: Text(s.tourSkip),
              ),
              const Spacer(),
              FilledButton(
                // On tap steps Next performs the highlighted action
                // (same handler the real tap uses); on plain steps
                // there is no action, so it just advances.
                onPressed: () {
                  if (!controller.performCurrentAction()) {
                    controller.next();
                  }
                },
                style: FilledButton.styleFrom(
                  backgroundColor: palette.accent,
                  foregroundColor: palette.accentInk,
                  minimumSize: const Size(0, AppSpacing.minTap),
                ),
                child: Text(s.tourNext),
              ),
            ],
          ),
        ],
      ),
    );

    final pointer = Container(
      width: diamond,
      height: diamond,
      decoration: BoxDecoration(
        color: palette.card,
        borderRadius: const BorderRadius.all(Radius.circular(2)),
      ),
      transform: Matrix4.rotationZ(math.pi / 4),
    );

    // The inner Stack must fill the screen: positioned children don't
    // size a Stack, so an unfilled Stack would collapse to zero and
    // the card would land at the top-left.
    if (below) {
      return Positioned.fill(
        child: Stack(
          children: [
            Positioned(
              left: left,
              top: targetRect.bottom + gap,
              child: card,
            ),
            Positioned(
              left: diamondLeft,
              top: targetRect.bottom + gap - diamond / 2 - 2,
              child: pointer,
            ),
          ],
        ),
      );
    }
    return Positioned.fill(
      child: Stack(
        children: [
          Positioned(
            left: left,
            bottom: screenSize.height - targetRect.top + gap,
            child: card,
          ),
          Positioned(
            left: diamondLeft,
            bottom:
                screenSize.height - targetRect.top + gap - diamond / 2 - 2,
            child: pointer,
          ),
        ],
      ),
    );
  }
}
