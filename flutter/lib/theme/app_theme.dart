import 'package:flutter/material.dart';

/// LokSewa Vidyapeeth design system.
///
/// Minimal white + orange (light, the default) and the same orange on
/// clean charcoal (dark), mirroring the web portal's tokens
/// (loksewa-prep-nepal/assets/css/style.css §1 "Design tokens") so the
/// Flutter app and the web portal share one visual identity. No navy,
/// no indigo, no purple, no gradients. 4px spacing rhythm, 44px
/// minimum tap targets.
///
/// Colors are theme-aware: widgets read them through
/// `AppColors.of(context)`, which returns the palette for the current
/// brightness. The theme builders use the palette consts directly.
class AppPalette {
  final Color bg;
  final Color bg2;
  final Color card;
  final Color card2;
  final Color text;
  final Color muted;
  final Color faint;
  final Color border;
  final Color borderSoft;
  final Color accent;
  final Color accentStrong;
  final Color accentDeep;
  final Color accentInk;
  final Color accentSoft;
  final Color accentLine;
  final Color green;
  final Color greenSoft;
  final Color danger;
  final Color dangerSoft;
  final Color blue;
  final Color blueSoft;

  /// Dim scrim behind coachmark tooltips (v1.0.7 tour). Same in both
  /// themes — a dark scrim reads the same over a light or dark screen.
  final Color scrim;

  const AppPalette({
    required this.bg,
    required this.bg2,
    required this.card,
    required this.card2,
    required this.text,
    required this.muted,
    required this.faint,
    required this.border,
    required this.borderSoft,
    required this.accent,
    required this.accentStrong,
    required this.accentDeep,
    required this.accentInk,
    required this.accentSoft,
    required this.accentLine,
    required this.green,
    required this.greenSoft,
    required this.danger,
    required this.dangerSoft,
    required this.blue,
    required this.blueSoft,
    required this.scrim,
  });

  /// Light (default): minimal white + orange.
  static const light = AppPalette(
    bg: Color(0xFFFFFFFF),
    bg2: Color(0xFFFFFFFF),
    card: Color(0xFFFFFFFF),
    card2: Color(0xFFF5F5F4),
    text: Color(0xFF111827),
    muted: Color(0xFF6B7280),
    faint: Color(0xFF9CA3AF),
    border: Color(0xFFE7E5E4),
    borderSoft: Color(0xFFF5F5F4),
    accent: Color(0xFFEA580C),
    accentStrong: Color(0xFFF97316),
    accentDeep: Color(0xFFC2410C),
    accentInk: Color(0xFFFFFFFF),
    accentSoft: Color(0x14EA580C), // ~8%
    accentLine: Color(0x59EA580C), // ~35%
    green: Color(0xFF16A34A),
    greenSoft: Color(0x1A16A34A),
    danger: Color(0xFFDC2626),
    dangerSoft: Color(0x14DC2626),
    blue: Color(0xFF2563EB),
    blueSoft: Color(0x142563EB),
    scrim: Color(0x99000000), // 60% black
  );

  /// Dark: the same orange on clean charcoal.
  static const dark = AppPalette(
    bg: Color(0xFF121212),
    bg2: Color(0xFF1E1E1E),
    card: Color(0xFF1E1E1E),
    card2: Color(0xFF2A2A2A),
    text: Color(0xFFF5F5F4),
    muted: Color(0xFFA3A3A3),
    faint: Color(0xFF737373),
    border: Color(0xFF333333),
    borderSoft: Color(0xFF262626),
    accent: Color(0xFFF97316),
    accentStrong: Color(0xFFFB923C),
    accentDeep: Color(0xFFFDBA74),
    accentInk: Color(0xFF1C0F00),
    accentSoft: Color(0x26F97316), // ~15%
    accentLine: Color(0x66F97316), // ~40%
    green: Color(0xFF22C55E),
    greenSoft: Color(0x2622C55E),
    danger: Color(0xFFEF4444),
    dangerSoft: Color(0x26EF4444),
    blue: Color(0xFF3B82F6),
    blueSoft: Color(0x293B82F6),
    scrim: Color(0x99000000), // 60% black
  );
}

class AppColors {
  /// The palette for the current theme brightness. Light is the
  /// default; dark resolves when the dark theme is active.
  static AppPalette of(BuildContext context) {
    return Theme.of(context).brightness == Brightness.dark
        ? AppPalette.dark
        : AppPalette.light;
  }
}

/// Spacing rhythm — 4px base, mirrors --sp-* tokens.
class AppSpacing {
  static const double s1 = 4;
  static const double s2 = 8;
  static const double s3 = 12;
  static const double s4 = 16;
  static const double s5 = 20;
  static const double s6 = 24;
  static const double s8 = 32;
  static const double s12 = 48;
  static const double maxWidth = 1100;
  static const double minTap = 44;
}

/// Radius scale — mirrors --radius-* tokens.
class AppRadius {
  static const sm = Radius.circular(8);
  static const md = Radius.circular(12);
  static const lg = Radius.circular(16);
  static const pill = Radius.circular(999);
  static BorderRadius get smAll => const BorderRadius.all(sm);
  static BorderRadius get mdAll => const BorderRadius.all(md);
  static BorderRadius get lgAll => const BorderRadius.all(lg);
}

/// Type scale. Devanagari needs generous line-height (>=1.5 for body),
/// mirroring --lh-* tokens.
class AppType {
  static const display = TextStyle(
    fontSize: 34,
    height: 1.25,
    fontWeight: FontWeight.w800,
  );
  static const h1 = TextStyle(
    fontSize: 26,
    height: 1.35,
    fontWeight: FontWeight.w700,
  );
  static const h2 = TextStyle(
    fontSize: 20,
    height: 1.35,
    fontWeight: FontWeight.w700,
  );
  static const h3 = TextStyle(
    fontSize: 17,
    height: 1.35,
    fontWeight: FontWeight.w600,
  );
  static const lead = TextStyle(fontSize: 17, height: 1.65);
  static const body = TextStyle(fontSize: 15, height: 1.65);
  static const small = TextStyle(fontSize: 13.5, height: 1.5);
  static const tiny = TextStyle(fontSize: 12, height: 1.4);
  static const countdownDigit = TextStyle(
    fontSize: 40,
    height: 1.1,
    fontWeight: FontWeight.w800,
    fontFeatures: [FontFeature.tabularFigures()],
  );
}

ThemeData buildAppTheme() {
  const p = AppPalette.light;
  final scheme = ColorScheme.fromSeed(
    seedColor: p.accent,
    brightness: Brightness.light,
    surface: p.card,
  );
  return ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    scaffoldBackgroundColor: p.bg,
    colorScheme: scheme.copyWith(
      primary: p.accent,
      onPrimary: p.accentInk,
      surface: p.card,
      onSurface: p.text,
    ),
    appBarTheme: AppBarTheme(
      backgroundColor: p.bg2,
      foregroundColor: p.text,
      elevation: 0,
    ),
    cardTheme: CardThemeData(
      color: p.card,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: AppRadius.mdAll,
        side: BorderSide(color: p.borderSoft),
      ),
    ),
    bottomNavigationBarTheme: BottomNavigationBarThemeData(
      backgroundColor: p.bg2,
      selectedItemColor: p.accentDeep,
      unselectedItemColor: p.muted,
    ),
    textTheme: const TextTheme(
      displayLarge: AppType.display,
      headlineMedium: AppType.h1,
      titleLarge: AppType.h2,
      titleMedium: AppType.h3,
      bodyLarge: AppType.lead,
      bodyMedium: AppType.body,
      bodySmall: AppType.small,
      labelSmall: AppType.tiny,
    ).apply(bodyColor: p.text, displayColor: p.text),
  );
}

ThemeData buildDarkTheme() {
  const p = AppPalette.dark;
  final scheme = ColorScheme.fromSeed(
    seedColor: p.accent,
    brightness: Brightness.dark,
    surface: p.card,
  );
  return ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    scaffoldBackgroundColor: p.bg,
    colorScheme: scheme.copyWith(
      primary: p.accent,
      onPrimary: p.accentInk,
      surface: p.card,
      onSurface: p.text,
    ),
    appBarTheme: AppBarTheme(
      backgroundColor: p.bg2,
      foregroundColor: p.text,
      elevation: 0,
    ),
    cardTheme: CardThemeData(
      color: p.card,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: AppRadius.mdAll,
        side: BorderSide(color: p.borderSoft),
      ),
    ),
    bottomNavigationBarTheme: BottomNavigationBarThemeData(
      backgroundColor: p.bg2,
      selectedItemColor: p.accentDeep,
      unselectedItemColor: p.muted,
    ),
    textTheme: const TextTheme(
      displayLarge: AppType.display,
      headlineMedium: AppType.h1,
      titleLarge: AppType.h2,
      titleMedium: AppType.h3,
      bodyLarge: AppType.lead,
      bodyMedium: AppType.body,
      bodySmall: AppType.small,
      labelSmall: AppType.tiny,
    ).apply(bodyColor: p.text, displayColor: p.text),
  );
}
