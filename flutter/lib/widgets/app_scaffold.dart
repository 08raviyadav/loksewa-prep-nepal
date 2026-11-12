import 'package:flutter/material.dart';

import '../l10n/community_strings.dart';
import '../l10n/history_strings.dart';
import '../state/app_state.dart';
import '../theme/app_theme.dart';
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

  const AppScaffold({
    super.key,
    required this.title,
    required this.body,
    required this.currentIndex,
    required this.onNav,
    this.actions,
    this.floatingActionButton,
  });

  @override
  Widget build(BuildContext context) {
    // AppState is provided above MaterialApp via a simple InheritedWidget
    // (see main.dart) to avoid extra dependencies in Phase 1.
    final state = AppStateScope.of(context);
    final s = state.strings;
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
        actions: [
          // EN / NE toggle
          TextButton(
            onPressed: state.toggleLang,
            style: TextButton.styleFrom(minimumSize: const Size(44, 44)),
            child: Text(
              state.isNe ? 'EN' : 'NE',
              style: const TextStyle(
                color: AppColors.accent,
                fontWeight: FontWeight.w800,
              ),
            ),
          ),
          IconButton(
            tooltip: s.navMore,
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
    Navigator.pop(context); // close the drawer first
    PushScope.of(context)?.onPush(route);
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
            decoration: const BoxDecoration(gradient: AppColors.heroGradient),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                Text(
                  'लोक सेवा विद्यापीठ',
                  style: AppType.h2.copyWith(color: Colors.white),
                ),
                Text(
                  'LOKSEWA VIDYAPEETH',
                  style: AppType.small.copyWith(color: AppColors.accent),
                ),
              ],
            ),
          ),
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
            title: Text(s.footerCredit),
            subtitle: const Text('github.com/08raviyadav · MIT'),
          ),
        ],
      ),
    );
  }
}

/// Minimal InheritedWidget provider for AppState (no extra packages).
class AppStateScope extends InheritedWidget {
  final AppState state;
  const AppStateScope({super.key, required this.state, required super.child});

  static AppState of(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<AppStateScope>();
    assert(scope != null, 'AppStateScope not found above this widget');
    return scope!.state;
  }

  @override
  bool updateShouldNotify(AppStateScope oldWidget) => true;
}
