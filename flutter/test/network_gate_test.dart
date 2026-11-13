/// Network gate tests (v1.0.4) — the app requires internet to open.
/// The probe is faked via the injected [checkInternet]; the real probe
/// (google.com/generate_204) is not hit from tests.
library;

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:loksewa_vidyapeeth/state/app_state.dart';
import 'package:loksewa_vidyapeeth/theme/app_theme.dart';
import 'package:loksewa_vidyapeeth/widgets/app_scaffold.dart';
import 'package:loksewa_vidyapeeth/widgets/network_gate.dart';
import 'package:shared_preferences/shared_preferences.dart';

Future<void> _pumpGate(
  WidgetTester tester, {
  required Future<bool> Function() checkInternet,
}) async {
  SharedPreferences.setMockInitialValues({});
  final state = AppState();
  await state.init();
  await tester.pumpWidget(
    AppStateScope(
      state: state,
      child: MaterialApp(
        theme: buildAppTheme(),
        home: NetworkGate(
          checkInternet: checkInternet,
          child: const Text('APP SHOWN'),
        ),
      ),
    ),
  );
  await tester.pump();
}

void main() {
  group('network gate', () {
    testWidgets('shows the app when online', (tester) async {
      await _pumpGate(tester, checkInternet: () async => true);
      await tester.pump();
      expect(find.text('APP SHOWN'), findsOneWidget);
      expect(find.text('No internet connection'), findsNothing);
    });

    testWidgets('shows the offline screen when offline', (tester) async {
      await _pumpGate(tester, checkInternet: () async => false);
      await tester.pump();
      expect(find.text('APP SHOWN'), findsNothing);
      expect(find.text('No internet connection'), findsOneWidget);
      expect(find.text('Retry'), findsOneWidget);
    });

    testWidgets('Retry re-probes and opens the app once online',
        (tester) async {
      var online = false;
      await _pumpGate(tester, checkInternet: () async => online);
      await tester.pump();
      expect(find.text('No internet connection'), findsOneWidget);
      online = true;
      await tester.tap(find.text('Retry'));
      await tester.pump();
      expect(find.text('APP SHOWN'), findsOneWidget);
    });

    testWidgets('auto-retries every 5 seconds while offline',
        (tester) async {
      var calls = 0;
      await _pumpGate(
        tester,
        checkInternet: () async => ++calls >= 2,
      );
      await tester.pump();
      expect(find.text('No internet connection'), findsOneWidget);
      // The periodic timer fires on fake pumps; the second probe
      // succeeds and the app opens without any tap.
      await tester.pump(const Duration(seconds: 5));
      await tester.pump();
      expect(find.text('APP SHOWN'), findsOneWidget);
    });
  });
}
