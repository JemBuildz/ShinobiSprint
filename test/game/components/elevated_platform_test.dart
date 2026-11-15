import 'dart:ui';

import 'package:flame/game.dart';
import 'package:flame_test/flame_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/game/components/elevated_platform.dart';

class _TestGame extends FlameGame {}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('ElevatedPlatform', () {
    test('initializes with default mid-air bracket parameters', () {
      final platform = ElevatedPlatform(
        position: Vector2(100, 200),
        size: Vector2(150, 40),
      );

      expect(platform.position, equals(Vector2(100, 200)));
      expect(platform.size, equals(Vector2(150, 40)));
      expect(platform.surfaceY, equals(200.0));
      expect(platform.leftX, equals(100.0));
      expect(platform.rightX, equals(250.0));
      expect(platform.isOneWay, isTrue);
      expect(platform.hasGroundPillars, isFalse);
      expect(platform.groundFloorY, equals(550.0));
    });

    test('initializes with grounded pillars when specified', () {
      final platform = ElevatedPlatform(
        position: Vector2(150, 300),
        size: Vector2(180, 50),
        hasGroundPillars: true,
        groundFloorY: 500,
      );

      expect(platform.hasGroundPillars, isTrue);
      expect(platform.groundFloorY, equals(500.0));
    });

    test('updates horizontal position according to speed', () {
      final platform = ElevatedPlatform(
        position: Vector2(200, 100),
        size: Vector2(100, 30),
      )..update(0.5);

      expect(platform.position.x, equals(150.0));
    });

    test('wraps forward when scrolled far off screen', () {
      final platform = ElevatedPlatform(
        position: Vector2(-260, 100),
        size: Vector2(100, 30),
      )..update(0.1);

      expect(platform.position.x, greaterThan(0));
    });

    testWithGame<_TestGame>(
      'mounts and renders mid-air suspension platform without crash',
      _TestGame.new,
      (game) async {
        final platform = ElevatedPlatform(
          position: Vector2(50, 150),
          size: Vector2(120, 36),
        );

        await game.ensureAdd(platform);
        expect(platform.isMounted, isTrue);

        final recorder = PictureRecorder();
        final canvas = Canvas(recorder);
        expect(() => platform.render(canvas), returnsNormally);
      },
    );

    testWithGame<_TestGame>(
      'mounts and renders grounded platform with stone plinths without crash',
      _TestGame.new,
      (game) async {
        final platform = ElevatedPlatform(
          position: Vector2(50, 150),
          size: Vector2(120, 36),
          hasGroundPillars: true,
          groundFloorY: 400,
        );

        await game.ensureAdd(platform);
        expect(platform.isMounted, isTrue);

        final recorder = PictureRecorder();
        final canvas = Canvas(recorder);
        expect(() => platform.render(canvas), returnsNormally);
      },
    );
  });
}
