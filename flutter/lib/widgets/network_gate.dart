/// Network gate (v1.0.4): the app requires internet to open.
///
/// On launch a real HTTP probe (GET https://www.google.com/generate_204,
/// 5s timeout) decides whether the app shell shows. Offline shows a
/// full-screen "No internet" state with a Retry button and an automatic
/// re-probe every [retryInterval] until the connection comes back.
///
/// [checkInternet] is injectable so tests can fake the probe; it
/// defaults to the real [probeInternet].
library;

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../l10n/v104_strings.dart';
import '../theme/app_theme.dart';
import 'app_scaffold.dart';

/// Real reachability probe: Google's captive-portal check endpoint
/// answers 204 with an empty body when the path to the internet is
/// clear (a captive portal or proxy answers something else).
Future<bool> probeInternet() async {
  try {
    final res = await http
        .get(Uri.parse('https://www.google.com/generate_204'))
        .timeout(const Duration(seconds: 5));
    return res.statusCode == 204;
  } catch (_) {
    return false;
  }
}

class NetworkGate extends StatefulWidget {
  final Widget child;
  final Future<bool> Function()? checkInternet;
  final Duration retryInterval;

  const NetworkGate({
    super.key,
    required this.child,
    this.checkInternet,
    this.retryInterval = const Duration(seconds: 5),
  });

  @override
  State<NetworkGate> createState() => _NetworkGateState();
}

class _NetworkGateState extends State<NetworkGate> {
  bool? _online; // null = still checking
  Timer? _retryTimer;
  int _probeId = 0; // guards against overlapping probes

  @override
  void initState() {
    super.initState();
    _probe();
  }

  @override
  void dispose() {
    _retryTimer?.cancel();
    super.dispose();
  }

  Future<void> _probe() async {
    final id = ++_probeId;
    final check = widget.checkInternet ?? probeInternet;
    final ok = await check();
    if (!mounted || id != _probeId) return;
    setState(() => _online = ok);
    if (ok) {
      _retryTimer?.cancel();
      _retryTimer = null;
    } else {
      _retryTimer ??=
          Timer.periodic(widget.retryInterval, (_) => _probe());
    }
  }

  @override
  Widget build(BuildContext context) {
    final online = _online;
    if (online == true) return widget.child;
    if (online == null) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }
    final s = AppStateScope.of(context).strings;
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.s6),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(
                Icons.wifi_off_outlined,
                size: 72,
                color: AppColors.muted,
              ),
              const SizedBox(height: AppSpacing.s4),
              Text(
                s.noInternetTitle,
                style: AppType.h2,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: AppSpacing.s2),
              Text(
                s.noInternetBody,
                style: AppType.body,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: AppSpacing.s6),
              FilledButton.icon(
                onPressed: _probe,
                icon: const Icon(Icons.refresh),
                label: Text(s.retryLabel),
                style: FilledButton.styleFrom(
                  backgroundColor: AppColors.accent,
                  foregroundColor: AppColors.accentInk,
                  minimumSize: const Size(0, AppSpacing.minTap),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
