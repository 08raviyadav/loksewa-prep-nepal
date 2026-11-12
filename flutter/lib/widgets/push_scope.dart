import 'package:flutter/material.dart';

/// Makes the drawer "More" push-handler available to [AppScaffold]'s
/// drawer. Provided by RootNav in main.dart; consumed in app_scaffold.dart.
class PushScope extends InheritedWidget {
  final ValueChanged<String> onPush;
  const PushScope({super.key, required this.onPush, required super.child});

  static PushScope? of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<PushScope>();

  @override
  bool updateShouldNotify(PushScope oldWidget) => oldWidget.onPush != onPush;
}
