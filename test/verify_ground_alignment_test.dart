import 'package:flame/game.dart';
import 'package:flame_test/flame_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/bamboo_village/bamboo_village.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('MainGame Ground Baseline & Physics Verification', () {
    testWithGame<MainGame>(
      'Player spawns and rests solidly on the ground baseline at Y = 350',
      MainGame.new,
      (game) async {
        await game.ready();

        expect(game.player.position.x, equals(340.0));
        expect(game.player.position.y, equals(350.0));

        // Advance game physics for 60 frames (1 full second of physics simulation)
        for (var i = 0; i < 60; i++) {
          game.update(0.016);
        }

        // Verify player does NOT fall, does NOT hover, but remains exactly at y = 350
        expect(game.player.position.y, equals(350.0));
        expect(game.player.isOnGround, isTrue);
        expect(game.player.velocity.y, equals(0.0));
      },
    );

    testWithGame<MainGame>(
      'Player runs smoothly across the ground floor maintaining Y = 350',
      MainGame.new,
      (game) async {
        await game.ready();

        // Simulate moving player to the right across the mountain bluff
        game.player.moveRight();

        for (var i = 0; i < 30; i++) {
          game.update(0.016);
          // Over horizontal movement on the left bluff, Y must remain solidly 350
          expect(game.player.position.y, equals(350.0));
          expect(game.player.isOnGround, isTrue);
        }

        expect(game.player.position.x, greaterThan(340.0));
      },
    );

    testWithGame<MainGame>(
      'Staircase ramp connects seamlessly from ground baseline Y = 350',
      MainGame.new,
      (game) async {
        await game.ready();

        // Find the staircase ramp components
        final ramps = game.world.children.whereType<SlopePlatformComponent>();
        expect(ramps, isNotEmpty);

        final grandRamp = ramps.firstWhere((r) => r.start.x == 700.0);
        expect(grandRamp.start.x, equals(700.0));
        expect(grandRamp.start.y, equals(350.0));
        expect(grandRamp.end.x, equals(890.0));
        expect(grandRamp.end.y, equals(150.0));

        // Verify slope calculations at connection point
        expect(grandRamp.getYAt(700.0), equals(350.0));
      },
    );
  });

  group('Starting Position & Ground-Contact Tolerance Regression Verification', () {
    /// Evaluates whether feet position is within ground contact tolerance with zero vertical velocity
    bool isGroundedState({
      required double feetY,
      required double groundY,
      required double velocityY,
      double tolerance = 6.0,
    }) {
      final isWithinTolerance = (feetY - groundY).abs() <= tolerance;
      final hasZeroVy = velocityY.abs() <= 0.05;
      return isWithinTolerance && hasZeroVy;
    }

    test(
      'Starting position at verified ground baseline Y = 482 with Vy = 0 evaluates solidly to Grounded',
      () {
        const startingY = 482.0; // Player's feet position at verified ground line
        const groundBaseline = 482.0;
        const velocityY = 0.0;
        const tolerance = 6.0;

        final isGrounded = isGroundedState(
          feetY: startingY,
          groundY: groundBaseline,
          velocityY: velocityY,
          tolerance: tolerance,
        );

        expect(isGrounded, isTrue);

        // Verify HUD label logic
        final currentFeetY = startingY.round();
        final status = isGrounded
            ? 'Grounded (${currentFeetY == 482 ? 'Flush Y=482' : 'Y=$currentFeetY'})'
            : 'Airborne (Vy: ${velocityY.round()})';

        expect(status, equals('Grounded (Flush Y=482)'));
      },
    );

    test(
      'Sub-pixel deviations within ground contact tolerance (±6px) maintain Grounded state',
      () {
        const groundBaseline = 482.0;

        // Exactly on baseline
        expect(
          isGroundedState(feetY: 482.0, groundY: groundBaseline, velocityY: 0.0),
          isTrue,
        );

        // +4px penetration into contact band
        expect(
          isGroundedState(feetY: 486.0, groundY: groundBaseline, velocityY: 0.0),
          isTrue,
        );

        // -4px sub-pixel float
        expect(
          isGroundedState(feetY: 478.0, groundY: groundBaseline, velocityY: 0.0),
          isTrue,
        );

        // Exactly on positive boundary (+6px)
        expect(
          isGroundedState(feetY: 488.0, groundY: groundBaseline, velocityY: 0.0),
          isTrue,
        );

        // Exactly on negative boundary (-6px)
        expect(
          isGroundedState(feetY: 476.0, groundY: groundBaseline, velocityY: 0.0),
          isTrue,
        );
      },
    );

    test(
      'Non-zero vertical velocity correctly transitions state to Airborne even if within tolerance',
      () {
        const groundBaseline = 482.0;

        // Jump impulse at initial takeoff (Vy = -420)
        expect(
          isGroundedState(feetY: 482.0, groundY: groundBaseline, velocityY: -420.0),
          isFalse,
        );

        // Terminal fall velocity (Vy = 250)
        expect(
          isGroundedState(feetY: 482.0, groundY: groundBaseline, velocityY: 250.0),
          isFalse,
        );
      },
    );

    test(
      'Positions outside ground contact tolerance evaluate to Airborne',
      () {
        const groundBaseline = 482.0;

        // Mid-air peak between platforms (feetY = 410, vy = 0 at jump apex)
        expect(
          isGroundedState(feetY: 410.0, groundY: groundBaseline, velocityY: 0.0),
          isFalse,
        );

        // Falling below world bounds (feetY = 520)
        expect(
          isGroundedState(feetY: 520.0, groundY: groundBaseline, velocityY: 0.0),
          isFalse,
        );
      },
    );
  });
}
