import 'package:flame/game.dart';
import 'package:flame_test/flame_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/game/components/scenery_element.dart';
import 'package:super_dash/game/config/parallax_depth.dart';

class _TestGame extends FlameGame {}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('SceneryElement', () {
    test('initializes with expected default size and depth multipliers', () {
      final torii = SceneryElement(
        sceneryType: SceneryType.toriiGate,
        depthSlice: ParallaxDepthSlice.midSlice,
        position: Vector2(200, 300),
      );

      expect(torii.sceneryType, equals(SceneryType.toriiGate));
      expect(torii.depthSlice, equals(ParallaxDepthSlice.midSlice));
      expect(torii.size, equals(Vector2(120, 140)));
      expect(torii.velocityMultiplier, equals(0.5));
      expect(torii.scrollSpeed, equals(50));
      expect(torii.assetPath, equals('cutouts/torii_gate.png'));
    });

    test('velocity multipliers match all 5 depth hierarchy slices', () {
      final back = SceneryElement(
        sceneryType: SceneryType.pagoda,
        depthSlice: ParallaxDepthSlice.backSlice,
      );
      final midBack = SceneryElement(
        sceneryType: SceneryType.pagoda,
        depthSlice: ParallaxDepthSlice.midBackSlice,
      );
      final mid = SceneryElement(
        sceneryType: SceneryType.bambooCluster,
        depthSlice: ParallaxDepthSlice.midSlice,
      );
      final midFront = SceneryElement(
        sceneryType: SceneryType.lanternPost,
        depthSlice: ParallaxDepthSlice.midFrontSlice,
      );
      final front = SceneryElement(
        sceneryType: SceneryType.boardwalkPlatform,
        depthSlice: ParallaxDepthSlice.frontSlice,
      );

      expect(back.velocityMultiplier, equals(0));
      expect(midBack.velocityMultiplier, equals(0.25));
      expect(mid.velocityMultiplier, equals(0.5));
      expect(midFront.velocityMultiplier, equals(0.75));
      expect(front.velocityMultiplier, equals(1));
    });

    test('scrolls horizontally based on assigned velocity multiplier', () {
      final element = SceneryElement(
        sceneryType: SceneryType.lanternPost,
        depthSlice: ParallaxDepthSlice.midFrontSlice, // 0.75x
        position: Vector2(300, 200),
        baseSpeed: 200,
      );

      // scrollSpeed = 200 * 0.75 = 150 px/s
      expect(element.scrollSpeed, equals(150));

      element.update(0.1);
      // position.x -= 150 * 0.1 = 15
      expect(element.position.x, closeTo(285, 0.001));
    });

    test('lanternPost switches between glowing night and clean day asset', () {
      final lantern = SceneryElement(
        sceneryType: SceneryType.lanternPost,
        depthSlice: ParallaxDepthSlice.midSlice,
      );

      // Nighttime default
      expect(lantern.isDaytime, isFalse);
      expect(lantern.assetPath, equals('cutouts/lantern_post_glowing.png'));

      // Switch to daytime
      lantern.isDaytime = true;
      expect(lantern.isDaytime, isTrue);
      expect(lantern.assetPath, equals('cutouts/lantern_post_clean.png'));
    });

    testWithGame<_TestGame>(
      'mounts successfully in Flame game tree',
      _TestGame.new,
      (game) async {
        final element = SceneryElement(
          sceneryType: SceneryType.toriiGate,
          depthSlice: ParallaxDepthSlice.midBackSlice,
          position: Vector2(100, 300),
        );

        await game.ensureAdd(element);
        expect(element.isMounted, isTrue);
      },
    );

    testWithGame<_TestGame>(
      'lanternPost attaches LanternGlowComponent and forwards isDaytime',
      _TestGame.new,
      (game) async {
        final lantern = SceneryElement(
          sceneryType: SceneryType.lanternPost,
          depthSlice: ParallaxDepthSlice.midSlice,
          position: Vector2(100, 300),
        );

        await game.ensureAdd(lantern);
        expect(lantern.lanternGlow, isNotNull);
        expect(lantern.lanternGlow!.isMounted, isTrue);
        expect(lantern.lanternGlow!.isDaytime, isFalse);

        lantern.isDaytime = true;
        expect(lantern.lanternGlow!.isDaytime, isTrue);
      },
    );
  });
}
