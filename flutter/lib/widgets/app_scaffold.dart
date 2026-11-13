import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:package_info_plus/package_info_plus.dart';
import 'package:share_plus/share_plus.dart';
import 'package:url_launcher/url_launcher.dart';

import '../l10n/community_strings.dart';
import '../l10n/examdates_strings.dart';
import '../l10n/history_strings.dart';
import '../l10n/tour_strings.dart';
import '../l10n/v104_strings.dart';
import '../onboarding/tour.dart';
import '../services/update_checker.dart';
import '../state/app_state.dart';
import '../theme/app_theme.dart';
import 'drawer_calendar.dart';
import 'push_scope.dart';

/// Shared app chrome: app bar (title + EN/NE toggle + theme toggle),
/// bottom navigation, and navigation drawer. Keeps every screen consistent.
class AppScaffold extends StatelessWidget {
  final String title;
  final Widget body;
  final int currentIndex;
  final ValueChanged<int> onNav;
  final List<Widget>? actions;
  final Widget? floatingActionButton;

  /// Tour key for the bottom navigation bar (v1.0.7). Passed only by
  /// the four tab screens — one tab screen is mounted at a time, so
  /// the GlobalKey never duplicates. Pushed drawer pages don't pass it.
  final Key? bottomNavKey;

  /// Tour key for the EN/NE language button (v1.0.9). Passed only by
  /// the Home screen — the tour's language step runs there, and
  /// attaching the same GlobalKey from every pushed page would
  /// duplicate it.
  final Key? langToggleKey;

  const AppScaffold({
    super.key,
    required this.title,
    required this.body,
    required this.currentIndex,
    required this.onNav,
    this.actions,
    this.floatingActionButton,
    this.bottomNavKey,
    this.langToggleKey,
  });

  @override
  Widget build(BuildContext context) {
    // AppState is provided above MaterialApp via a simple InheritedWidget
    // (see main.dart) to avoid extra dependencies in Phase 1.
    final state = AppStateScope.of(context);
    final s = state.strings;
    // Tour step 2 (v1.0.9): the language button is a tour target. Its
    // tap really switches the language AND advances the tour; the
    // registered action lets the tooltip's Next button do the same.
    // Registration is idempotent (map overwrite), so re-registering on
    // every build is harmless.
    final tour = TourScope.of(context);
    tour?.registerAction('langToggle', () {
      state.toggleLang();
      tour.advanceIfOn('langToggle');
    });
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
        actions: [
          // Dark / light toggle (v1.0.6: dark mode is back; light is
          // the default).
          IconButton(
            icon: Icon(
              state.themeMode == ThemeMode.dark
                  ? Icons.light_mode_outlined
                  : Icons.dark_mode_outlined,
            ),
            onPressed: () => state.setThemeMode(
              state.themeMode == ThemeMode.dark
                  ? ThemeMode.light
                  : ThemeMode.dark,
            ),
          ),
          // EN / NE toggle
          TextButton(
            key: langToggleKey,
            onPressed: () {
              state.toggleLang();
              tour?.advanceIfOn('langToggle');
            },
            style: TextButton.styleFrom(minimumSize: const Size(44, 44)),
            child: Text(
              state.isNe ? 'EN' : 'NE',
              style: TextStyle(
                color: AppColors.of(context).accent,
                fontWeight: FontWeight.w800,
              ),
            ),
          ),
          ...?actions,
        ],
      ),
      drawer: _AppDrawer(onNav: onNav),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: AppSpacing.maxWidth),
          child: body,
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        key: bottomNavKey,
        currentIndex: currentIndex,
        onTap: onNav,
        type: BottomNavigationBarType.fixed,
        items: [
          BottomNavigationBarItem(
            icon: const Icon(Icons.home_outlined),
            label: s.navHome,
          ),
          BottomNavigationBarItem(
            icon: const Icon(Icons.quiz_outlined),
            label: s.navPractice,
          ),
          BottomNavigationBarItem(
            icon: const Icon(Icons.timer_outlined),
            label: s.navMock,
          ),
          BottomNavigationBarItem(
            icon: const Icon(Icons.dashboard_outlined),
            label: s.navDashboard,
          ),
        ],
      ),
      floatingActionButton: floatingActionButton,
    );
  }
}

class _AppDrawer extends StatelessWidget {
  final ValueChanged<int> onNav;
  const _AppDrawer({required this.onNav});

  void _push(BuildContext context, String route) {
    // Read the current route before popping: tapping the page you're
    // already on just closes the drawer instead of rebuilding the page.
    final current = ModalRoute.of(context)?.settings.name;
    Navigator.pop(context); // close the drawer first
    if (current == route) return;
    PushScope.of(context)?.onPush(route);
  }

  /// Opens an external link (GitHub, website) in the browser. Closes
  /// the drawer first; shows a snackbar if the device can't open it.
  ///
  /// The snackbar uses the Navigator's context, not the drawer's: the
  /// drawer unmounts on pop, so its own context is dead by the time
  /// the launch result comes back.
  Future<void> _openLink(BuildContext context, String url) async {
    final rootContext = Navigator.of(context).context;
    Navigator.pop(context); // close the drawer first
    final ok = await launchUrl(
      Uri.parse(url),
      mode: LaunchMode.externalApplication,
    );
    if (!ok && rootContext.mounted) {
      final s = AppStateScope.of(rootContext).strings;
      ScaffoldMessenger.of(rootContext).showSnackBar(
        SnackBar(content: Text(s.openLinkFailed)),
      );
    }
  }

  /// Shares [text] via the system share sheet (app link / invite).
  Future<void> _shareText(BuildContext context, String text) async {
    Navigator.pop(context); // close the drawer first
    try {
      await SharePlus.instance.share(ShareParams(text: text));
    } catch (_) {
      // The share sheet basically never fails on Android; if it does,
      // there is nothing useful to show — the user just taps again.
    }
  }

  /// Replays the first-launch tour (v1.0.7): closes the drawer, returns
  /// to the Home tab, then restarts the tour from step 1 once the home
  /// screen has settled.
  void _replayTour(BuildContext context) {
    final rootContext = Navigator.of(context).context;
    Navigator.pop(context); // close the drawer first
    Navigator.of(rootContext).popUntil((r) => r.isFirst);
    onNav(0);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Future<void>.delayed(const Duration(milliseconds: 600), () {
        if (rootContext.mounted) {
          TourScope.of(rootContext)?.replay();
        }
      });
    });
  }

  /// Manual update check: asks GitHub for the latest release, compares
  /// it with the installed version, and offers the APK download.
  Future<void> _checkForUpdates(BuildContext context) async {
    final rootContext = Navigator.of(context).context;
    final s = AppStateScope.of(context).strings;
    Navigator.pop(context); // close the drawer first
    // Loading dialog (back button disabled while the check runs, so
    // the dismiss-pop below always targets this dialog, never a page).
    showDialog<void>(
      context: rootContext,
      barrierDismissible: false,
      builder: (_) => PopScope(
        canPop: false,
        child: AlertDialog(
          content: Row(
            children: [
              const CircularProgressIndicator(),
              const SizedBox(width: AppSpacing.s4),
              Expanded(child: Text(s.checkingForUpdates)),
            ],
          ),
        ),
      ),
    );
    try {
      final info = await PackageInfo.fromPlatform();
      final result = await UpdateChecker(
        client: http.Client(),
        currentVersion: info.version,
      ).check();
      if (!rootContext.mounted) return;
      Navigator.of(rootContext).pop(); // dismiss loading
      if (result.updateAvailable) {
        final downloadIt = await showDialog<bool>(
          context: rootContext,
          builder: (_) => AlertDialog(
            title: Text(s.updateAvailable),
            content: Text(s.updateAvailableBody(result.latestVersion)),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(rootContext, false),
                child: Text(s.later),
              ),
              FilledButton(
                onPressed: () => Navigator.pop(rootContext, true),
                child: Text(s.download),
              ),
            ],
          ),
        );
        if (downloadIt == true && rootContext.mounted) {
          await launchUrl(
            Uri.parse(result.downloadUrl),
            mode: LaunchMode.externalApplication,
          );
        }
      } else {
        await showDialog<void>(
          context: rootContext,
          builder: (_) => AlertDialog(
            title: Text(s.upToDate),
            content: Text(s.upToDateBody),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(rootContext),
                child: Text(s.closeBtn),
              ),
            ],
          ),
        );
      }
    } catch (_) {
      if (rootContext.mounted) {
        Navigator.of(rootContext).pop(); // dismiss loading
        ScaffoldMessenger.of(rootContext).showSnackBar(
          SnackBar(content: Text(s.checkFailed)),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: BoxDecoration(
              color: AppColors.of(context).card,
              border: Border(
                bottom: BorderSide(color: AppColors.of(context).borderSoft),
              ),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: AppColors.of(context).accent,
                  ),
                  alignment: Alignment.center,
                  child: Text(
                    'O',
                    style: AppType.h2.copyWith(
                      color: AppColors.of(context).accentInk,
                    ),
                  ),
                ),
                const SizedBox(width: AppSpacing.s3),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        'Outrank',
                        style: AppType.h2.copyWith(
                          color: AppColors.of(context).text,
                        ),
                      ),
                      Text(
                        'LOK SEWA EXAM PREP',
                        style: AppType.small.copyWith(
                          color: AppColors.of(context).accent,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          // Live calendar (v1.0.3): AD date in English, BS date in
          // Nepali, with a ticking clock.
          const DrawerCalendar(),
          ListTile(
            leading: const Icon(Icons.calendar_month_outlined),
            title: Text(s.examDates),
            onTap: () => _push(context, '/exam-dates'),
          ),
          ListTile(
            leading: const Icon(Icons.menu_book_outlined),
            title: Text(s.courses),
            onTap: () => _push(context, '/courses'),
          ),
          ListTile(
            leading: const Icon(Icons.history_edu_outlined),
            title: Text(s.historyNav),
            onTap: () => _push(context, '/history'),
          ),
          ListTile(
            leading: const Icon(Icons.error_outline),
            title: Text(s.mistakesTitle),
            onTap: () => _push(context, '/mistakes'),
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.forum_outlined),
            title: Text(s.discussionTitle),
            onTap: () => _push(context, '/community/discussion'),
          ),
          ListTile(
            leading: const Icon(Icons.add_circle_outline),
            title: Text(s.submitTitle),
            onTap: () => _push(context, '/community/submit'),
          ),
          ListTile(
            leading: const Icon(Icons.lightbulb_outline),
            title: Text(s.suggestTitle),
            onTap: () => _push(context, '/community/suggestions'),
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.info_outline),
            title: Text(s.aboutTitle),
            onTap: () => _push(context, '/about'),
          ),
          ListTile(
            leading: const Icon(Icons.privacy_tip_outlined),
            title: Text(s.privacyTitle),
            onTap: () => _push(context, '/privacy'),
          ),
          ListTile(
            leading: const Icon(Icons.system_update_outlined),
            title: Text(s.checkUpdatesTitle),
            subtitle: const _CurrentVersionSubtitle(),
            onTap: () => _checkForUpdates(context),
          ),
          ListTile(
            leading: const Icon(Icons.share_outlined),
            title: Text(s.shareTitle),
            onTap: () => _shareText(context, s.shareMessage),
          ),
          ListTile(
            leading: const Icon(Icons.person_add_outlined),
            title: Text(s.inviteTitle),
            onTap: () => _shareText(context, s.inviteMessage),
          ),
          ListTile(
            leading: const Icon(Icons.school_outlined),
            title: Text(s.tourReplayTitle),
            onTap: () => _replayTour(context),
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.public_outlined),
            title: const Text('raviyadav.com.np'),
            subtitle: Text(s.websiteTitle),
            trailing: const Icon(Icons.open_in_new, size: 18),
            onTap: () => _openLink(context, 'https://raviyadav.com.np'),
          ),
          ListTile(
            leading: const Icon(Icons.code_outlined),
            title: Text(s.footerCredit),
            subtitle: const Text('github.com/08raviyadav · MIT'),
            trailing: const Icon(Icons.open_in_new, size: 18),
            onTap: () =>
                _openLink(context, 'https://github.com/08raviyadav'),
          ),
        ],
      ),
    );
  }
}

/// "Version 1.0.2" subtitle under Check for updates. Fetches once;
/// renders nothing if the platform lookup fails (e.g. in a test).
class _CurrentVersionSubtitle extends StatefulWidget {
  const _CurrentVersionSubtitle();

  @override
  State<_CurrentVersionSubtitle> createState() =>
      _CurrentVersionSubtitleState();
}

class _CurrentVersionSubtitleState extends State<_CurrentVersionSubtitle> {
  String? _version;

  @override
  void initState() {
    super.initState();
    PackageInfo.fromPlatform().then(
      (info) {
        if (mounted) setState(() => _version = info.version);
      },
      onError: (_) {},
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_version == null) return const SizedBox.shrink();
    final s = AppStateScope.of(context).strings;
    return Text('${s.versionLabel} $_version');
  }
}

/// Minimal provider for AppState (no extra packages).
///
/// v1.0.9 fix — the v1.0.8 language switcher "didn't work": tapping
/// EN/NE changed the stored preference but nothing on screen changed
/// until restart. Root cause: the old scope was a bare InheritedWidget
/// created once in main(), so it never rebuilt and never notified its
/// dependents; the only rebuild path was an AnimatedBuilder above
/// MaterialApp, and the route contents sit behind a `const` NetworkGate
/// so Flutter short-circuited the update. Now a StatefulWidget shell
/// listens to the AppState ChangeNotifier and rebuilds the inner
/// InheritedWidget on every change, so every dependent (screens, app
/// bar, drawer, tour tooltip) rebuilds when the language changes.
class AppStateScope extends StatefulWidget {
  final AppState state;
  final Widget child;
  const AppStateScope({
    super.key,
    required this.state,
    required this.child,
  });

  /// Depending lookup: the caller rebuilds when AppState notifies.
  static AppState of(BuildContext context) {
    final scope =
        context.dependOnInheritedWidgetOfExactType<_AppStateInherited>();
    assert(scope != null, 'AppStateScope not found above this widget');
    return scope!.state;
  }

  /// Non-depending lookup: safe in initState (no rebuild subscription).
  /// For one-shot reads, e.g. the language at quiz-start time.
  static AppState? maybeOf(BuildContext context) {
    final element =
        context.getElementForInheritedWidgetOfExactType<_AppStateInherited>();
    if (element == null) return null;
    return (element.widget as _AppStateInherited).state;
  }

  @override
  State<AppStateScope> createState() => _AppStateScopeState();
}

class _AppStateScopeState extends State<AppStateScope> {
  @override
  void initState() {
    super.initState();
    widget.state.addListener(_onStateChanged);
  }

  @override
  void didUpdateWidget(AppStateScope oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.state != widget.state) {
      oldWidget.state.removeListener(_onStateChanged);
      widget.state.addListener(_onStateChanged);
    }
  }

  @override
  void dispose() {
    widget.state.removeListener(_onStateChanged);
    super.dispose();
  }

  void _onStateChanged() => setState(() {});

  @override
  Widget build(BuildContext context) =>
      _AppStateInherited(state: widget.state, child: widget.child);
}

class _AppStateInherited extends InheritedWidget {
  final AppState state;
  const _AppStateInherited({required this.state, required super.child});

  // The state object never changes — the shell rebuilds this widget on
  // every notify, so always notify dependents.
  @override
  bool updateShouldNotify(_AppStateInherited oldWidget) => true;
}
