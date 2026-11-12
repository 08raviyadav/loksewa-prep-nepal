import 'package:flutter/material.dart';

/// LokSewa Vidyapeeth design system.
///
/// Ported 1:1 from the vanilla site's CSS custom properties
/// (loksewa-prep-nepal/assets/css/style.css §1 "Design tokens") so the
/// Flutter app and the web portal share one visual identity:
/// saffron brand family on deep indigo/slate, dark default + light theme,
/// 4px spacing rhythm, 44px minimum tap targets.
class AppColors {
  // --- dark (default) ---
  static const bg = Color(0xFF0F172A);
  static const bg2 = Color(0xFF16213A);
  static const card = Color(0xFF1E293B);
  static const card2 = Color(0xFF273449);
  static const text = Color(0xFFF1F5F9);
  static const muted = Color(0xFF94A3B8);
  static const faint = Color(0xFF64748B);
  static const border = Color(0xFF334155);
  static const borderSoft = Color(0xFF2A3A52);

  // --- light ---
  static const lightBg = Color(0xFFF1F5F9);
  static const lightBg2 = Color(0xFFFFFFFF);
  static const lightCard = Color(0xFFFFFFFF);
  static const lightCard2 = Color(0xFFEEF2F7);
  static const lightText = Color(0xFF0F172A);
  static const lightMuted = Color(0xFF475569);
  static const lightFaint = Color(0xFF94A3B8);

  // --- brand: saffron family (shared) ---
  static const accent = Color(0xFFF59E0B);
  static const accentStrong = Color(0xFFFBBF24);
  static const accentDeep = Color(0xFFB45309);
  static const accentInk = Color(0xFF1A1207);
  static const accentSoft = Color(0x21F59E0B); // ~13%
  static const accentLine = Color(0x61F59E0B); // ~38%

  // --- semantic (shared) ---
  static const green = Color(0xFF22C55E);
  static const greenSoft = Color(0x2122C55E);
  static const danger = Color(0xFFEF4444);
  static const dangerSoft = Color(0x1FEF4444);
  static const blue = Color(0xFF3B82F6);
  static const blueSoft = Color(0x293B82F6);
  static const indigo = Color(0xFF818CF8);

  static const heroGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF1E1B4B), Color(0xFF0F172A), Color(0xFF3B0764)],
  );
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

ThemeData buildDarkTheme() {
  final scheme = ColorScheme.fromSeed(
    seedColor: AppColors.accent,
    brightness: Brightness.dark,
    surface: AppColors.card,
  );
  return ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    scaffoldBackgroundColor: AppColors.bg,
    colorScheme: scheme.copyWith(
      primary: AppColors.accent,
      onPrimary: AppColors.accentInk,
      surface: AppColors.card,
      onSurface: AppColors.text,
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: AppColors.bg2,
      foregroundColor: AppColors.text,
      elevation: 0,
    ),
    cardTheme: CardThemeData(
      color: AppColors.card,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: AppRadius.mdAll,
        side: const BorderSide(color: AppColors.borderSoft),
      ),
    ),
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: AppColors.bg2,
      selectedItemColor: AppColors.accent,
      unselectedItemColor: AppColors.muted,
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
    ).apply(bodyColor: AppColors.text, displayColor: AppColors.text),
  );
}

ThemeData buildLightTheme() {
  final scheme = ColorScheme.fromSeed(
    seedColor: AppColors.accentDeep,
    brightness: Brightness.light,
    surface: AppColors.lightCard,
  );
  return ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    scaffoldBackgroundColor: AppColors.lightBg,
    colorScheme: scheme.copyWith(
      primary: AppColors.accentDeep,
      onPrimary: Colors.white,
      surface: AppColors.lightCard,
      onSurface: AppColors.lightText,
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: AppColors.lightBg2,
      foregroundColor: AppColors.lightText,
      elevation: 0,
    ),
    cardTheme: CardThemeData(
      color: AppColors.lightCard,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: AppRadius.mdAll,
        side: const BorderSide(color: Color(0xFFE2E8F0)),
      ),
    ),
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: AppColors.lightBg2,
      selectedItemColor: AppColors.accentDeep,
      unselectedItemColor: AppColors.lightMuted,
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
    ).apply(bodyColor: AppColors.lightText, displayColor: AppColors.lightText),
  );
}
