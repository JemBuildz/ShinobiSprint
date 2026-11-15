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
}
