import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../l10n/app_strings.dart';

/// Global app state: language, exam reminders.
/// ChangeNotifier keeps it lean — no Riverpod/Bloc until the app earns it.
/// (v1.0.5: the theme toggle is gone — the app is white + orange only.)
class AppState extends ChangeNotifier {
  static const _kLang = 'loksewa_lang_v1';
  static const _kReminders = 'loksewa_reminders_v1';
  static const _kDismissed = 'loksewa_rem_dismissed_v1';

  AppLang _lang = AppLang.en;
  Set<String> _reminders = {};
  Set<String> _dismissed = {};
  bool _ready = false;

  AppLang get lang => _lang;
  Set<String> get reminders => _reminders;
  bool get ready => _ready;
  AppStrings get strings => AppStrings(_lang);

  bool get isNe => _lang == AppLang.ne;

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    _lang = AppLangX.fromCode(prefs.getString(_kLang));
    _reminders = prefs.getStringList(_kReminders)?.toSet() ?? {};
    _dismissed = prefs.getStringList(_kDismissed)?.toSet() ?? {};
    _ready = true;
    notifyListeners();
  }

  Future<void> setLang(AppLang lang) async {
    _lang = lang;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_kLang, lang.code);
    notifyListeners();
  }

  Future<void> toggleLang() =>
      setLang(_lang == AppLang.en ? AppLang.ne : AppLang.en);

  bool hasReminder(String examDateId) => _reminders.contains(examDateId);

  Future<void> toggleReminder(String examDateId) async {
    if (_reminders.contains(examDateId)) {
      _reminders.remove(examDateId);
    } else {
      _reminders.add(examDateId);
    }
    final prefs = await SharedPreferences.getInstance();
    await prefs.setStringList(_kReminders, _reminders.toList());
    notifyListeners();
  }

  bool isDismissed(String key) => _dismissed.contains(key);

  Future<void> dismiss(String key) async {
    _dismissed.add(key);
    final prefs = await SharedPreferences.getInstance();
    await prefs.setStringList(_kDismissed, _dismissed.toList());
    notifyListeners();
  }
}
