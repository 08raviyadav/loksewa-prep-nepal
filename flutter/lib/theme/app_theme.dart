import 'package:flutter/material.dart';

/// LokSewa Vidyapeeth design system.
///
/// Minimal white + orange, mirroring the web portal's tokens
/// (loksewa-prep-nepal/assets/css/style.css §1 "Design tokens") so the
/// Flutter app and the web portal share one visual identity: white
/// surfaces, warm stone borders, one orange brand family. Single light
/// theme — no dark mode, no gradients. 4px spacing rhythm, 44px minimum
/// tap targets.
class AppColors {
  // --- surfaces ---
  static const bg = Color(0xFFFFFFFF);
  static const bg2 = Color(0xFFFFFFFF);
  static const card = Color(0xFFFFFFFF);
  static const card2 = Color(0xFFF5F5F4);
  static const text = Color(0xFF111827);
  static const muted = Color(0xFF6B7280);
  static const faint = Color(0xFF9CA3AF);
  static const border = Color(0xFFE7E5E4);
  static const borderSoft = Color(0xFFF5F5F4);

  // --- brand: orange family ---
  static const accent = Color(0xFFEA580C);
  static const accentStrong = Color(0xFFF97316);
  static const accentDeep = Color(0xFFC2410C);
  static const accentInk = Color(0xFFFFFFFF);
  static const accentSoft = Color(0x14EA580C); // ~8%
  static const accentLine = Color(0x59EA580C); // ~35%

  // --- semantic ---
  static const green = Color(0xFF16A34A);
  static const greenSoft = Color(0x1A16A34A);
  static const danger = Color(0xFFDC2626);
  static const dangerSoft = Color(0x14DC2626);
  // Blue is functional, not brand: exam-date "later" chips and the mock
  // palette's "current question" state.
  static const blue = Color(0xFF2563EB);
  static const blueSoft = Color(0x142563EB);
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
  final scheme = ColorScheme.fromSeed(
    seedColor: AppColors.accent,
    brightness: Brightness.light,
    surface: AppColors.card,
  );
  return ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
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
      selectedItemColor: AppColors.accentDeep,
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
