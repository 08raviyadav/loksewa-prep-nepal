/// Theme tests (v1.0.6) — dark mode is back. Light stays the default;
/// AppColors.of(context) resolves the palette for the active brightness.
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Captures the palette resolved in its own build context.
class _PaletteProbe extends StatelessWidget {
  final void Function(AppPalette palette) onPalette;
  const _PaletteProbe({required this.onPalette});

  @override
  Widget build(BuildContext context) {
    onPalette(AppColors.of(context));
    return const SizedBox.shrink();
  }
}

Future<AppPalette> _resolvePalette(
  WidgetTester tester, {
  required ThemeData theme,
}) async {
  var resolved = AppPalette.light;
  await tester.pumpWidget(
    MaterialApp(
      theme: theme,
      home: _PaletteProbe(onPalette: (p) => resolved = p),
    ),
  );
  await tester.pump();
  return resolved;
}

void main() {
  group('theme palettes', () {
    testWidgets('light theme resolves the light palette', (tester) async {
      final p = await _resolvePalette(tester, theme: buildAppTheme());
      expect(p.bg, AppPalette.light.bg);
      expect(p.text, AppPalette.light.text);
      expect(p.accent, AppPalette.light.accent);
      expect(p.bg, const Color(0xFFFFFFFF));
      expect(p.text, const Color(0xFF111827));
      expect(p.accent, const Color(0xFFEA580C));
      expect(p.accentInk, const Color(0xFFFFFFFF));
    });

    testWidgets('dark theme resolves the dark palette', (tester) async {
      final p = await _resolvePalette(tester, theme: buildDarkTheme());
      expect(p.bg, AppPalette.dark.bg);
      expect(p.text, AppPalette.dark.text);
      expect(p.accent, AppPalette.dark.accent);
      expect(p.bg, const Color(0xFF121212));
      expect(p.text, const Color(0xFFF5F5F4));
      expect(p.accent, const Color(0xFFF97316));
      expect(p.accentInk, const Color(0xFF1C0F00));
      // No navy / indigo / purple anywhere in the dark palette.
      expect(p.bg2, const Color(0xFF1E1E1E));
      expect(p.card, const Color(0xFF1E1E1E));
    });

    testWidgets('themeMode picks the palette (main.dart wiring)',
        (tester) async {
      AppPalette? resolved;
      await tester.pumpWidget(
        MaterialApp(
          theme: buildAppTheme(),
          darkTheme: buildDarkTheme(),
          themeMode: ThemeMode.dark,
          home: _PaletteProbe(onPalette: (p) => resolved = p),
        ),
      );
      await tester.pump();
      expect(resolved?.bg, AppPalette.dark.bg);

      await tester.pumpWidget(
        MaterialApp(
          theme: buildAppTheme(),
          darkTheme: buildDarkTheme(),
          themeMode: ThemeMode.light,
          home: _PaletteProbe(onPalette: (p) => resolved = p),
        ),
      );
      // MaterialApp animates between themes (AnimatedTheme) — advance
      // past the animation or Theme.of still returns the old theme.
      await tester.pump(const Duration(seconds: 1));
      expect(resolved?.bg, AppPalette.light.bg);
    });
  });

  group('AppState theme mode', () {
    test('defaults to light, setThemeMode flips it, preference persists',
        () async {
      SharedPreferences.setMockInitialValues({});
      final state = AppState();
      await state.init();
      expect(state.themeMode, ThemeMode.light);

      await state.setThemeMode(ThemeMode.dark);
      expect(state.themeMode, ThemeMode.dark);

      // A fresh AppState reads the saved preference back.
      final reloaded = AppState();
      await reloaded.init();
      expect(reloaded.themeMode, ThemeMode.dark);

      await reloaded.setThemeMode(ThemeMode.light);
      expect(reloaded.themeMode, ThemeMode.light);
    });
  });
}
