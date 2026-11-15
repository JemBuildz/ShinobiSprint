import 'package:flame/game.dart';
import 'package:flame/parallax.dart';
import 'package:flame_test/flame_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:super_dash/game/components/parallax_background.dart';
import 'package:super_dash/game/shinobi_sprint_game.dart';

class _MockParallax extends Mock implements Parallax {
  @override
  Vector2 baseVelocity = Vector2.zero();

  @override
  bool isSized = false;

  @override
  void resize(Vector2? size) {}
}

class _TestGame extends FlameGame {}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('ParallaxBackground', () {
    test('defines 5 core background layer asset names', () {
      expect(ParallaxBackground.layerAssetNames.length, equals(5));
      expect(
        ParallaxBackground.layerAssetNames,
        containsAllInOrder([
          'backgrounds/farthest_sky.png',
          'backgrounds/deep_background.png',
          'backgrounds/mid_background.png',
          'backgrounds/midground_lamps.png',
          'backgrounds/foreground_path.png',
        ]),
      );
    });

    test(
      'defaultLayers configures ascending baseVelocity with static moon',
      () {
      final layers = ParallaxBackground.defaultLayers;
      expect(layers.length, equals(5));

      // Layer 1: Farthest Sky/Moon (static moon)
      expect(layers[0].fileName, contains('farthest_sky'));
      expect(layers[0].velocityMultiplier.x, equals(0.0));

      // Layer 2: Deep Background
      expect(layers[1].fileName, contains('deep_background'));
      expect(layers[1].velocityMultiplier.x, equals(0.25));

      // Layer 3: Mid Background Trees/Gates (moderate speeds for torii gates)
      expect(layers[2].fileName, contains('mid_background'));
      expect(layers[2].velocityMultiplier.x, equals(0.5));

      // Layer 4: Midground Lamps
      expect(layers[3].fileName, contains('midground_lamps'));
      expect(layers[3].velocityMultiplier.x, equals(0.75));

      // Layer 5: Foreground Path (1.0x speed)
      expect(layers[4].fileName, contains('foreground_path'));
      expect(layers[4].velocityMultiplier.x, equals(1.0));

      // Verify strictly ascending order
      for (var i = 0; i < layers.length - 1; i++) {
        expect(
          layers[i].velocityMultiplier.x,
          lessThan(layers[i + 1].velocityMultiplier.x),
        );
      }
    });

    test('can be created with custom speed and custom baseVelocity', () {
      final customVelocity = Vector2(250, 0);
      final bg = ParallaxBackground<_TestGame>(
        baseVelocity: customVelocity,
      );

      expect(bg.baseVelocity, equals(customVelocity));
      expect(bg.priority, equals(-1));
    });

    test('baseVelocity setter updates velocity', () {
      final mockParallax = _MockParallax();
      final bg = ParallaxBackground<_TestGame>(
        parallax: mockParallax,
      )..baseVelocity = Vector2(150, 0);

      expect(bg.baseVelocity, equals(Vector2(150, 0)));
      expect(mockParallax.baseVelocity, equals(Vector2(150, 0)));
    });

    testWithGame<_TestGame>(
      'mounts successfully with mock parallax',
      _TestGame.new,
      (game) async {
        final mockParallax = _MockParallax();
        final bg = ParallaxBackground<_TestGame>(
          parallax: mockParallax,
        );

        await game.ensureAdd(bg);
        expect(bg.isMounted, isTrue);
      },
    );

    testWithGame<ShinobiSprintGame>(
      'ShinobiSprintGame mounts parallaxBackground in game tree',
      ShinobiSprintGame.new,
      (game) async {
        expect(game.parallaxBackground.isMounted, isTrue);
        expect(game.children.contains(game.parallaxBackground), isTrue);
        expect(game.parallaxBackground.priority, equals(-1));
      },
    );

    test('defines 5 day background layer asset names', () {
      expect(ParallaxBackground.dayLayerAssetNames.length, equals(5));
      expect(
        ParallaxBackground.dayLayerAssetNames,
        containsAllInOrder([
          'backgrounds/day_farthest_sky.png',
          'backgrounds/day_deep_background.png',
          'backgrounds/day_mid_background.png',
          'backgrounds/day_midground_lamps.png',
          'backgrounds/day_foreground_path.png',
        ]),
      );
    });

    test(
      'dayLayers preserves identical velocity multipliers as defaultLayers',
      () {
        final nightLayers = ParallaxBackground.defaultLayers;
        final dayLayers = ParallaxBackground.dayLayers;

        expect(dayLayers.length, equals(nightLayers.length));

        for (var i = 0; i < dayLayers.length; i++) {
          expect(
            dayLayers[i].velocityMultiplier,
            equals(nightLayers[i].velocityMultiplier),
          );
        }
      },
    );

    test(
      'layerConfigs toggles defaultLayers and dayLayers based on isDaytime',
      () {
        final bg = ParallaxBackground<_TestGame>();
        expect(bg.isDaytime, isFalse);
        expect(bg.layerConfigs, equals(ParallaxBackground.defaultLayers));

        bg.isDaytime = true;
        expect(bg.isDaytime, isTrue);
        expect(bg.layerConfigs, equals(ParallaxBackground.dayLayers));

        bg.isDaytime = false;
        expect(bg.layerConfigs, equals(ParallaxBackground.defaultLayers));
      },
    );

    test(
      'threeLayerHierarchy defines 3 distinct depth layers',
      () {
        final layers = ParallaxBackground.threeLayerHierarchy;
        expect(layers.length, equals(3));

        // Layer 3 (Far): Moon & Stars (static)
        expect(layers[0].fileName, contains('farthest_sky'));
        expect(layers[0].velocityMultiplier.x, equals(0.0));

        // Layer 2 (Mid): Pagoda & Distant Mountains (0.25x)
        expect(layers[1].fileName, contains('deep_background'));
        expect(layers[1].velocityMultiplier.x, equals(0.25));

        // Layer 1 (Near): Bamboo Trees (0.50x)
        expect(layers[2].fileName, contains('mid_background'));
        expect(layers[2].velocityMultiplier.x, equals(0.50));
      },
    );

    test(
      'layerConfigs uses 3-layer hierarchy when useThreeLayerDepth is true',
      () {
        final bg = ParallaxBackground<_TestGame>(useThreeLayerDepth: true);
        expect(
          bg.layerConfigs,
          equals(ParallaxBackground.threeLayerHierarchy),
        );

        bg.isDaytime = true;
        expect(
          bg.layerConfigs,
          equals(ParallaxBackground.threeLayerDayHierarchy),
        );
      },
    );
  });
}
