import 'package:flame_tiled/flame_tiled.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/game/entities/item.dart';

void main() {
  group('ItemType', () {
    test('points are properly configured', () {
      expect(ItemType.shuriken.points, equals(10));
      expect(ItemType.sushi.points, equals(1000));
      expect(ItemType.goldenFeather.points, equals(0));
    });

    test('backward-compatibility aliases point to shuriken and sushi', () {
      expect(ItemType.acorn, equals(ItemType.shuriken));
      expect(ItemType.egg, equals(ItemType.sushi));
    });

    test('fromType resolves Sushi and Egg correctly', () {
      expect(ItemType.fromType('Sushi'), equals(ItemType.sushi));
      expect(ItemType.fromType('Egg'), equals(ItemType.sushi));
    });

    test('fromType resolves Feather and GoldenFeather correctly', () {
      expect(ItemType.fromType('Feather'), equals(ItemType.goldenFeather));
      expect(
        ItemType.fromType('GoldenFeather'),
        equals(ItemType.goldenFeather),
      );
    });

    test('fromType resolves Shuriken, Acorn, or defaults correctly', () {
      expect(ItemType.fromType('Shuriken'), equals(ItemType.shuriken));
      expect(ItemType.fromType('Acorn'), equals(ItemType.shuriken));
      expect(ItemType.fromType(null), equals(ItemType.shuriken));
      expect(ItemType.fromType('Unknown'), equals(ItemType.shuriken));
    });
  });

  group('Collectible component classes', () {
    test('can instantiate Shuriken and Sushi', () {
      final tiledObject = TiledObject(id: 1, x: 10, y: 10);
      final shuriken = Shuriken(tiledObject: tiledObject);
      final sushi = Sushi(tiledObject: tiledObject);

      expect(shuriken, isA<Item>());
      expect(sushi, isA<Item>());
      expect(Acorn(tiledObject: tiledObject), isA<Shuriken>());
      expect(Egg(tiledObject: tiledObject), isA<Sushi>());
    });
  });
}
