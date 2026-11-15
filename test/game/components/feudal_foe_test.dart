import 'package:flame/game.dart';
import 'package:flame_test/flame_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/game/components/feudal_foe.dart';
import 'package:super_dash/game/components/katana_slash.dart';
import 'package:super_dash/game/components/shuriken_projectile.dart';

class _TestGame extends FlameGame {}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('FeudalFoe', () {
    test(
      'initializes with expected default size and asset path for Ashigaru',
      () {
        final foe = FeudalFoe(
          foeType: FoeType.ashigaru,
          position: Vector2(300, 500),
        );

        expect(foe.foeType, equals(FoeType.ashigaru));
        expect(foe.size, equals(Vector2(74, 64)));
        expect(foe.assetPath, equals('foes/ashigaru.png'));
        expect(foe.isDefeated, isFalse);
      },
    );

    test('initializes with expected properties for Hitodama and Karakasa', () {
      final hitodama = FeudalFoe(
        foeType: FoeType.hitodama,
        position: Vector2(200, 300),
      );
      final karakasa = FeudalFoe(
        foeType: FoeType.karakasa,
        position: Vector2(250, 400),
      );

      expect(hitodama.foeType, equals(FoeType.hitodama));
      expect(hitodama.assetPath, equals('foes/hitodama.png'));

      expect(karakasa.foeType, equals(FoeType.karakasa));
      expect(karakasa.assetPath, equals('foes/karakasa.png'));
    });

    test('updates horizontal patrol position for Ashigaru', () {
      final foe = FeudalFoe(
        foeType: FoeType.ashigaru,
        position: Vector2(300, 500),
        speed: 50,
        patrolRange: 20,
      )..update(0.1);

      // Moves left initially: 300 - 50 * 0.1 = 295
      expect(foe.position.x, closeTo(295, 0.001));
    });

    test('defeat() marks foe as defeated and removes from parent', () {
      final foe = FeudalFoe(
        foeType: FoeType.ronin,
        position: Vector2(100, 100),
      );

      expect(foe.isDefeated, isFalse);
      foe.defeat();
      expect(foe.isDefeated, isTrue);
    });

    testWithGame<_TestGame>(
      'mounts in Flame game tree successfully',
      _TestGame.new,
      (game) async {
        final foe = FeudalFoe(
          foeType: FoeType.oni,
          position: Vector2(100, 200),
        );

        await game.ensureAdd(foe);
        expect(foe.isMounted, isTrue);
      },
    );

    testWithGame<_TestGame>(
      'KatanaSlash collision defeats foe',
      _TestGame.new,
      (game) async {
        final foe = FeudalFoe(
          foeType: FoeType.ashigaru,
          position: Vector2(100, 100),
        );
        final slash = KatanaSlash(
          position: Vector2(100, 100),
        );

        await game.ensureAdd(foe);
        expect(foe.isDefeated, isFalse);

        foe.onCollision({Vector2(100, 100)}, slash);
        expect(foe.isDefeated, isTrue);
      },
    );

    testWithGame<_TestGame>(
      'ShurikenProjectile collision defeats foe',
      _TestGame.new,
      (game) async {
        final foe = FeudalFoe(
          foeType: FoeType.ronin,
          position: Vector2(150, 150),
        );
        final shuriken = ShurikenProjectile(
          position: Vector2(150, 150),
          velocity: Vector2(300, 0),
        );

        await game.ensureAdd(foe);
        expect(foe.isDefeated, isFalse);

        foe.onCollision({Vector2(150, 150)}, shuriken);
        expect(foe.isDefeated, isTrue);
      },
    );
  });
}
