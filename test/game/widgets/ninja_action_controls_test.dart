import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/game/widgets/ninja_action_controls.dart';

void main() {
  group('NinjaActionControls', () {
    testWidgets('renders all controls and triggers callbacks', (tester) async {
      var jumpCount = 0;
      var slashCount = 0;
      var shurikenCount = 0;
      var toggleCount = 0;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: NinjaActionControls(
              onJump: () => jumpCount++,
              onSlash: () => slashCount++,
              onThrowShuriken: () => shurikenCount++,
              onToggleDayNight: () => toggleCount++,
            ),
          ),
        ),
      );

      expect(
        find.byKey(const Key('ninja_action_jump_button')),
        findsOneWidget,
      );
      expect(
        find.byKey(const Key('ninja_action_slash_button')),
        findsOneWidget,
      );
      expect(
        find.byKey(const Key('ninja_action_shuriken_button')),
        findsOneWidget,
      );
      expect(
        find.byKey(const Key('ninja_action_theme_toggle_button')),
        findsOneWidget,
      );

      // Nighttime icon
      expect(find.byIcon(Icons.nightlight_round), findsOneWidget);

      await tester.tap(find.byKey(const Key('ninja_action_jump_button')));
      await tester.pump();
      expect(jumpCount, equals(1));

      await tester.tap(find.byKey(const Key('ninja_action_slash_button')));
      await tester.pump();
      expect(slashCount, equals(1));

      await tester.tap(find.byKey(const Key('ninja_action_shuriken_button')));
      await tester.pump();
      expect(shurikenCount, equals(1));

      await tester.tap(
        find.byKey(const Key('ninja_action_theme_toggle_button')),
      );
      await tester.pump();
      expect(toggleCount, equals(1));
    });

    testWidgets('displays sun icon when isDaytime is true', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: NinjaActionControls(
              onToggleDayNight: () {},
              isDaytime: true,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.wb_sunny_rounded), findsOneWidget);
    });

    testWidgets('omits action buttons when callbacks are null', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: NinjaActionControls(),
          ),
        ),
      );

      expect(find.byKey(const Key('ninja_action_slash_button')), findsNothing);
      expect(
        find.byKey(const Key('ninja_action_shuriken_button')),
        findsNothing,
      );
      expect(
        find.byKey(const Key('ninja_action_theme_toggle_button')),
        findsNothing,
      );
    });
  });
}
