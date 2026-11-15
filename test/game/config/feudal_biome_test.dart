import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/game/config/feudal_biome.dart';

void main() {
  group('FeudalBiome', () {
    test('contains 8 distinct feudal biomes with valid properties', () {
      expect(FeudalBiome.values.length, equals(8));

      for (final biome in FeudalBiome.values) {
        expect(biome.title.isNotEmpty, isTrue);
        expect(biome.assetPrefix.isNotEmpty, isTrue);
        expect(biome.scenery.isNotEmpty, isTrue);
        expect(biome.foes.isNotEmpty, isTrue);
        expect(biome.dayAsset, contains('panoramic_biomes/'));
        expect(biome.nightAsset, contains('panoramic_biomes/'));
        expect(biome.getAsset(isDaytime: true), equals(biome.dayAsset));
        expect(biome.getAsset(isDaytime: false), equals(biome.nightAsset));
      }
    });

    test('bambooGrove has expected characteristics', () {
      const bamboo = FeudalBiome.bambooGrove;
      expect(bamboo.title, equals('Bamboo Grove'));
      expect(bamboo.dayAsset, equals('panoramic_biomes/bamboo_grove_day.png'));
      expect(
        bamboo.nightAsset,
        equals('panoramic_biomes/bamboo_grove_night.png'),
      );
    });
  });
}
