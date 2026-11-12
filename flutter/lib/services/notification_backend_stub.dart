/// Web (and any non-`dart:io` platform) backend for [NotificationService].
///
/// Imported by notifications.dart via conditional import; never compiled on
/// Android/iOS/desktop.
library;

import 'notifications.dart';

/// Returns the no-op stub backend. Web keeps the in-app reminder banner
/// (the vanilla site's on-open check) instead of OS notifications.
NotificationService createService() => StubNotificationService();
