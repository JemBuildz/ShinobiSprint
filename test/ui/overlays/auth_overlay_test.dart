import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:super_dash/ui/overlays/auth_overlay.dart';

class _TestGame extends FlameGame {}

void main() {
  group('AuthOverlay', () {
    testWidgets('renders all widgets with wooden ninja aesthetic',
        (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: AuthOverlay(),
          ),
        ),
      );

      expect(find.text('SHINOBI SPRINT'), findsOneWidget);
      expect(find.text('CLAN AUTHENTICATION'), findsOneWidget);
      expect(find.text('忍'), findsOneWidget);
      expect(find.text('EMAIL ADDRESS'), findsOneWidget);
      expect(find.text('PASSWORD'), findsOneWidget);
      expect(find.text('SIGN IN'), findsOneWidget);
      expect(find.text('Sign in with Google'), findsOneWidget);
      expect(find.text('Sign in with Apple'), findsOneWidget);
      expect(find.byType(FaIcon), findsNWidgets(2));
    });

    testWidgets('obscureText toggles when visibility icon is tapped',
        (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: AuthOverlay(),
          ),
        ),
      );

      final passwordFieldFinder = find.byWidgetPredicate(
        (widget) =>
            widget is TextField &&
            widget.decoration?.hintText == '••••••••' &&
            widget.obscureText == true,
      );
      expect(passwordFieldFinder, findsOneWidget);

      await tester.tap(find.byIcon(Icons.visibility_off_outlined));
      await tester.pump();

      final revealedPasswordFieldFinder = find.byWidgetPredicate(
        (widget) =>
            widget is TextField &&
            widget.decoration?.hintText == '••••••••' &&
            widget.obscureText == false,
      );
      expect(revealedPasswordFieldFinder, findsOneWidget);
    });

    testWidgets('validates empty email and password on SIGN IN tap',
        (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: AuthOverlay(),
          ),
        ),
      );

      await tester.tap(find.text('SIGN IN'));
      await tester.pumpAndSettle();

      expect(
        find.text('Please enter your ninja scroll email'),
        findsOneWidget,
      );
      expect(
        find.text('Please enter your shinobi secret key'),
        findsOneWidget,
      );
    });

    testWidgets(
        'calls onSignInWithEmail and onSignInSuccess on successful sign in',
        (tester) async {
      var emailSubmitted = '';
      var passwordSubmitted = '';
      var successCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AuthOverlay(
              onSignInWithEmail: (email, password) async {
                emailSubmitted = email;
                passwordSubmitted = password;
              },
              onSignInSuccess: () {
                successCalled = true;
              },
            ),
          ),
        ),
      );

      final emailField = find.widgetWithText(
        TextFormField,
        'ninja@shinobi.clan',
      );
      final passwordField = find.widgetWithText(
        TextFormField,
        '••••••••',
      );

      await tester.enterText(emailField, 'master@shinobi.clan');
      await tester.enterText(passwordField, 'katanaPassword123');

      await tester.tap(find.text('SIGN IN'));
      await tester.pumpAndSettle();

      expect(emailSubmitted, equals('master@shinobi.clan'));
      expect(passwordSubmitted, equals('katanaPassword123'));
      expect(successCalled, isTrue);
    });

    testWidgets('calls onSignInWithGoogle when Google button is tapped',
        (tester) async {
      var googleCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AuthOverlay(
              onSignInWithGoogle: () async {
                googleCalled = true;
              },
            ),
          ),
        ),
      );

      await tester.tap(find.text('Sign in with Google'));
      await tester.pumpAndSettle();

      expect(googleCalled, isTrue);
    });

    testWidgets('calls onSignInWithApple when Apple button is tapped',
        (tester) async {
      var appleCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AuthOverlay(
              onSignInWithApple: () async {
                appleCalled = true;
              },
            ),
          ),
        ),
      );

      await tester.tap(find.text('Sign in with Apple'));
      await tester.pumpAndSettle();

      expect(appleCalled, isTrue);
    });

    testWidgets('calls onClose when close button is tapped', (tester) async {
      var closeCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AuthOverlay(
              onClose: () {
                closeCalled = true;
              },
            ),
          ),
        ),
      );

      await tester.tap(find.byIcon(Icons.close));
      await tester.pumpAndSettle();

      expect(closeCalled, isTrue);
    });

    testWidgets('displays error message banner when sign in throws error',
        (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AuthOverlay(
              onSignInWithEmail: (email, password) async {
                throw Exception('Invalid clan credentials');
              },
            ),
          ),
        ),
      );

      final emailField = find.widgetWithText(
        TextFormField,
        'ninja@shinobi.clan',
      );
      final passwordField = find.widgetWithText(
        TextFormField,
        '••••••••',
      );

      await tester.enterText(emailField, 'ninja@shinobi.clan');
      await tester.enterText(passwordField, 'wrongSecretKey');

      await tester.tap(find.text('SIGN IN'));
      await tester.pumpAndSettle();

      expect(
        find.text('An unexpected error occurred. Please try again.'),
        findsOneWidget,
      );
    });

    testWidgets('dismisses overlay via Flame game if provided',
        (tester) async {
      final game = _TestGame();
      game.overlays.addEntry(
        AuthOverlay.id,
        (context, game) => const SizedBox(),
      );
      game.overlays.addEntry(
        AuthOverlay.overlayKey,
        (context, game) => const SizedBox(),
      );
      game.overlays.add(AuthOverlay.id);
      expect(game.overlays.isActive(AuthOverlay.id), isTrue);

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AuthOverlay(game: game),
          ),
        ),
      );

      await tester.tap(find.byIcon(Icons.close));
      await tester.pumpAndSettle();

      expect(game.overlays.isActive(AuthOverlay.id), isFalse);
      expect(AuthOverlay.id, equals('auth'));
      expect(AuthOverlay.overlayKey, equals('auth_overlay'));
    });
  });
}
