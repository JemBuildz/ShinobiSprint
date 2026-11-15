import 'package:flame/components.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/game/config/parallax_depth.dart';

void main() {
  group('ParallaxDepthConfig & ParallaxLayerInfo', () {
    test('defines 5 depth layers adhering to image_29 Panel 3 hierarchy', () {
      const layers = ParallaxDepthConfig.layers;
      expect(layers.length, equals(5));

      // 1. BACK SLICE
      final back = layers[0];
      expect(back.slice, equals(ParallaxDepthSlice.backSlice));
      expect(back.name, equals('BACK SLICE'));
      expect(back.mapping, equals('Moonlight Sky/Distant Mountains'));
      expect(back.depthCategory, equals('Infinite/Stationary'));
      expect(back.velocityMultiplier, equals(0));
      expect(back.velocityMultiplierVector, equals(Vector2(0, 0)));

      // 2. MID-BACK SLICE
      final midBack = layers[1];
      expect(midBack.slice, equals(ParallaxDepthSlice.midBackSlice));
      expect(midBack.name, equals('MID-BACK SLICE'));
      expect(midBack.mapping, equals('Distant Pagodas/Pagoda Groupings'));
      expect(midBack.depthCategory, equals('Slow'));
      expect(midBack.velocityMultiplier, equals(0.25));
      expect(midBack.velocityMultiplierVector, equals(Vector2(0.25, 0)));

      // 3. MID SLICE
      final mid = layers[2];
      expect(mid.slice, equals(ParallaxDepthSlice.midSlice));
      expect(mid.name, equals('MID SLICE'));
      expect(mid.mapping, equals('Lantern Posts/Bamboo Forest elements'));
      expect(mid.depthCategory, equals('Moderate'));
      expect(mid.velocityMultiplier, equals(0.5));
      expect(mid.velocityMultiplierVector, equals(Vector2(0.5, 0)));

      // 4. MID-FRONT SLICE
      final midFront = layers[3];
      expect(midFront.slice, equals(ParallaxDepthSlice.midFrontSlice));
      expect(midFront.name, equals('MID-FRONT SLICE'));
      expect(midFront.mapping, equals('Wooden Bridge/Main Path/Rocks'));
      expect(midFront.depthCategory, equals('Medium'));
      expect(midFront.velocityMultiplier, equals(0.75));
      expect(midFront.velocityMultiplierVector, equals(Vector2(0.75, 0)));

      // 5. FRONT SLICE
      final front = layers[4];
      expect(front.slice, equals(ParallaxDepthSlice.frontSlice));
      expect(front.name, equals('FRONT SLICE'));
      expect(front.mapping, equals('Foreground Pond/River'));
      expect(front.depthCategory, equals('Player Relative'));
      expect(front.velocityMultiplier, equals(1));
      expect(front.velocityMultiplierVector, equals(Vector2(1, 0)));
    });

    test('velocity multipliers are strictly ascending for depth illusion', () {
      const layers = ParallaxDepthConfig.layers;
      for (var i = 0; i < layers.length - 1; i++) {
        expect(
          layers[i].velocityMultiplier,
          lessThan(layers[i + 1].velocityMultiplier),
        );
      }
    });

    test('integrated wide assets resolve properly for day and night', () {
      expect(
        ParallaxDepthConfig.getIntegratedWideAsset(isDaytime: true),
        equals(ParallaxDepthConfig.dayWideAsset),
      );
      expect(
        ParallaxDepthConfig.getIntegratedWideAsset(isDaytime: false),
        equals(ParallaxDepthConfig.nightWideAsset),
      );
      expect(
        ParallaxDepthConfig.getIntegratedAsset(isDaytime: true),
        equals(ParallaxDepthConfig.dayWideAsset),
      );
      expect(
        ParallaxDepthConfig.getIntegratedAsset(isDaytime: false),
        equals(ParallaxDepthConfig.nightWideAsset),
      );
    });

    test(
      'toLayerConfigs preserves velocity rules identically across day/night',
      () {
        final nightConfigs =
            ParallaxDepthConfig.toLayerConfigs(isDaytime: false);
        final dayConfigs = ParallaxDepthConfig.toLayerConfigs(isDaytime: true);

        expect(nightConfigs.length, equals(5));
        expect(dayConfigs.length, equals(5));

        for (var i = 0; i < 5; i++) {
          expect(
            dayConfigs[i].velocityMultiplier,
            equals(nightConfigs[i].velocityMultiplier),
          );
          expect(
            dayConfigs[i].fileName,
            isNot(equals(nightConfigs[i].fileName)),
          );
          expect(dayConfigs[i].fileName, contains('day_'));
        }
      },
    );
  });
}
