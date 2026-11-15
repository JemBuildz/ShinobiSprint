import 'dart:async';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:super_dash/ui/overlays/auth_overlay.dart';
import 'package:super_dash/ui/widgets/clan_auth_badge.dart';

class _MockFirebaseAuth extends Mock implements FirebaseAuth {}

class _MockUser extends Mock implements User {}

class _TestGame extends FlameGame {}

void main() {
  group('ClanAuthBadge', () {
    late FirebaseAuth firebaseAuth;
    late StreamController<User?> authStateController;

    setUp(() {
      firebaseAuth = _MockFirebaseAuth();
      authStateController = StreamController<User?>.broadcast();
      when(() => firebaseAuth.authStateChanges())
          .thenAnswer((_) => authStateController.stream);
    });

    tearDown(() {
      authStateController.close();
    });

    testWidgets('renders GUEST CLAN when unauthenticated', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ClanAuthBadge(auth: firebaseAuth),
          ),
        ),
      );

      // Initially null or empty stream yields GUEST CLAN
      await tester.pump();

      expect(find.text('GUEST CLAN'), findsOneWidget);
      expect(find.text('？'), findsOneWidget);
      expect(find.byIcon(Icons.login_rounded), findsOneWidget);
    });

    testWidgets('renders authenticated user name and ninja badge',
        (tester) async {
      final user = _MockUser();
      when(() => user.isAnonymous).thenReturn(false);
      when(() => user.displayName).thenReturn('Hattori Hanzo');
      when(() => user.email).thenReturn('hanzo@shinobi.clan');

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ClanAuthBadge(auth: firebaseAuth),
          ),
        ),
      );

      authStateController.add(user);
      await tester.pump();

      expect(find.text('HATTORI HANZO'), findsOneWidget);
      expect(find.text('忍'), findsOneWidget);
      expect(find.byIcon(Icons.verified_user_rounded), findsOneWidget);
    });

    testWidgets('calls custom onTap callback when provided', (tester) async {
      var tapped = false;
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ClanAuthBadge(
              auth: firebaseAuth,
              onTap: () => tapped = true,
            ),
          ),
        ),
      );

      await tester.pump();
      await tester.tap(find.byType(ClanAuthBadge));
      expect(tapped, isTrue);
    });

    testWidgets('triggers game.overlays.add(AuthOverlay.id) when tapped',
        (tester) async {
      final game = _TestGame();
      game.overlays.addEntry(
        AuthOverlay.id,
        (context, game) => const SizedBox(),
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ClanAuthBadge(
              auth: firebaseAuth,
              game: game,
            ),
          ),
        ),
      );

      await tester.pump();
      expect(game.overlays.isActive(AuthOverlay.id), isFalse);

      await tester.tap(find.byType(ClanAuthBadge));
      expect(game.overlays.isActive(AuthOverlay.id), isTrue);
    });

    testWidgets('opens AuthOverlay dialog when tapped without game or onTap',
        (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ClanAuthBadge(auth: firebaseAuth),
          ),
        ),
      );

      await tester.pump();
      await tester.tap(find.byType(ClanAuthBadge));
      await tester.pumpAndSettle();

      expect(find.byType(AuthOverlay), findsOneWidget);
    });
  });
}
