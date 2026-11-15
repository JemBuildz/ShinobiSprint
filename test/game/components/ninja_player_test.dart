import 'package:flame/components.dart';
import 'package:flame/game.dart';
import 'package:flame/sprite.dart';
import 'package:flame_test/flame_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:super_dash/game/components/elevated_platform.dart';
import 'package:super_dash/game/components/ninja_player.dart';

class _MockSpriteAnimation extends Mock implements SpriteAnimation {
  @override
  SpriteAnimationTicker createTicker() => _MockSpriteAnimationTicker();
}

class _MockSpriteAnimationTicker extends Mock
    implements SpriteAnimationTicker {
  @override
  void reset() {}
}

class _TestGame extends FlameGame {}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('NinjaPlayer', () {
    late _MockSpriteAnimation runAnimation;
    late _MockSpriteAnimation jumpAnimation;
    late Map<NinjaState, SpriteAnimation> testAnimations;

    setUp(() {
      runAnimation = _MockSpriteAnimation();
      jumpAnimation = _MockSpriteAnimation();
      testAnimations = {
        NinjaState.running: runAnimation,
        NinjaState.jumping: jumpAnimation,
      };
    });

    test('initializes with default values', () {
      final player = NinjaPlayer(
        position: Vector2(100, 200),
        groundY: 200,
        animations: testAnimations,
      );

      expect(player.position, equals(Vector2(100, 200)));
      expect(player.size, equals(Vector2.all(64)));
      expect(player.groundY, equals(200));
      expect(player.gravity, equals(1200));
      expect(player.jumpVelocity, equals(-600));
      expect(player.velocity, equals(Vector2.zero()));
      expect(player.verticalVelocity, equals(0));
      expect(player.isJumping, isFalse);
    });

    testWithGame(
      'starts in running state when added to game',
      _TestGame.new,
      (game) async {
        final player = NinjaPlayer(
          position: Vector2(100, 200),
          groundY: 200,
          animations: testAnimations,
        );

        await game.ensureAdd(player);

        expect(player.current, equals(NinjaState.running));
        expect(player.isJumping, isFalse);
      },
    );

    testWithGame(
      'jump applies upward velocity, updates state, and spawns jump effect',
      _TestGame.new,
      (game) async {
        final player = NinjaPlayer(
          position: Vector2(100, 200),
          groundY: 200,
          animations: testAnimations,
        );

        await game.ensureAdd(player);

        player.jump();

        expect(player.verticalVelocity, equals(-600));
        expect(player.current, equals(NinjaState.jumping));
        expect(player.isJumping, isTrue);
        expect(player.temporaryJumpEffects.length, equals(1));

        game.update(0);
        expect(game.children.whereType<NinjaJumpEffect>().length, equals(1));
      },
    );

    testWithGame(
      'update applies gravity and updates physical position over time',
      _TestGame.new,
      (game) async {
        final player = NinjaPlayer(
          position: Vector2(100, 200),
          groundY: 200,
          animations: testAnimations,
        );

        await game.ensureAdd(player);

        player
          ..jump()
          ..update(0.1);

        expect(player.verticalVelocity, equals(-480));
        expect(player.position.y, lessThan(200));
      },
    );

    testWithGame(
      'lands on ground, resets velocity, and transitions back to running',
      _TestGame.new,
      (game) async {
        final player = NinjaPlayer(
          position: Vector2(100, 200),
          groundY: 200,
          animations: testAnimations,
        );

        await game.ensureAdd(player);

        player.jump();
        expect(player.current, equals(NinjaState.jumping));

        player
          ..position.y = 190
          ..verticalVelocity = 500
          ..update(0.1);

        expect(player.position.y, equals(200));
        expect(player.verticalVelocity, equals(0));
        expect(player.current, equals(NinjaState.running));
        expect(player.isJumping, isFalse);
      },
    );

    testWithGame(
      'onRemove cleans up and disposes of temporary jump effects',
      _TestGame.new,
      (game) async {
        final player = NinjaPlayer(
          position: Vector2(100, 200),
          groundY: 200,
          animations: testAnimations,
        );

        await game.ensureAdd(player);
        player.jump();
        game.update(0);

        expect(player.temporaryJumpEffects.length, equals(1));
        final effect = player.temporaryJumpEffects.first;
        expect(effect.isMounted, isTrue);

        player.removeFromParent();
        game.update(0);

        expect(player.temporaryJumpEffects, isEmpty);
        expect(effect.isMounted, isFalse);
      },
    );

    testWithGame(
      'NinjaJumpEffect auto-removes after its lifetime',
      _TestGame.new,
      (game) async {
        final effect = NinjaJumpEffect(
          position: Vector2(50, 50),
          lifetime: 0.2,
        );

        await game.ensureAdd(effect);
        expect(effect.isMounted, isTrue);

        effect.update(0.1);
        expect(effect.isMounted, isTrue);

        effect.update(0.15);
        await game.ready();
        expect(effect.isMounted, isFalse);
      },
    );

    test('calibrates foot baseline offset for plank contact', () {
      final player = NinjaPlayer(
        position: Vector2(100, 200),
        groundY: 200,
        animations: testAnimations,
      );

      expect(player.footOffset, equals(2));
      // position.y (200) + size.y (64) - footOffset (2) = 262
      expect(player.footPositionY, equals(262));
    });

    testWithGame(
      'continuous floorBaselineY catches player and prevents falling',
      _TestGame.new,
      (game) async {
        final player = NinjaPlayer(
          position: Vector2(100, 100),
          groundY: 100,
          floorBaselineY: 300,
          animations: testAnimations,
        );

        await game.ensureAdd(player);

        // Simulate falling off high ledge (groundY removed or player passed it)
        player
          ..groundY = null
          ..position.y = 350
          ..verticalVelocity = 400
          ..update(0.1);

        // Player is safely caught on continuous floorBaselineY
        expect(player.position.y, equals(300));
        expect(player.verticalVelocity, equals(0));
        expect(player.current, equals(NinjaState.running));
        expect(player.isJumping, isFalse);
      },
    );

    testWithGame(
      'lands on top plank surface of elevated platform when falling',
      _TestGame.new,
      (game) async {
        final platform = ElevatedPlatform(
          position: Vector2(50, 200),
          size: Vector2(200, 48),
        );
        await game.ensureAdd(platform);

        final player = NinjaPlayer(
          position: Vector2(80, 130),
          groundY: 130,
          floorBaselineY: 550,
          animations: testAnimations,
        );
        await game.ensureAdd(player);

        player
          ..verticalVelocity = 100
          ..position.y = 138
          ..update(0.01);

        expect(player.currentPlatform, equals(platform));
        expect(player.position.y, equals(138));
        expect(player.verticalVelocity, equals(0));
        expect(player.current, equals(NinjaState.running));
      },
    );

    testWithGame(
      'walks off elevated platform and catches continuous floor baseline',
      _TestGame.new,
      (game) async {
        final platform = ElevatedPlatform(
          position: Vector2(50, 200),
          size: Vector2(100, 48),
        );
        await game.ensureAdd(platform);

        final player = NinjaPlayer(
          position: Vector2(80, 138),
          groundY: 138,
          floorBaselineY: 550,
          animations: testAnimations,
        );
        await game.ensureAdd(player);

        player
          ..verticalVelocity = 0
          ..update(0.01);
        expect(player.currentPlatform, equals(platform));

        player
          ..position.x = 160
          ..update(0.01);

        expect(player.currentPlatform, isNull);
        expect(player.groundY, equals(550));
      },
    );

    test('calibrated physical hitbox calculates accurate boundaries', () {
      final player = NinjaPlayer(
        position: Vector2(100, 200),
      );

      expect(player.hitboxLeft, equals(117));
      expect(player.hitboxRight, equals(147));
      expect(player.hitboxWidth, equals(30));
      expect(player.physicalHitbox.left, equals(117));
      expect(player.physicalHitbox.top, equals(211));
      expect(player.physicalHitbox.width, equals(30));
      expect(player.physicalHitbox.height, equals(51)); // 64 - 11 - 2
    });

    testWithGame(
      'departs platform precisely when body leaves edge without floating',
      _TestGame.new,
      (game) async {
        final platform = ElevatedPlatform(
          position: Vector2(100, 200),
          size: Vector2(100, 48), // X spans 100 to 200
        );
        await game.ensureAdd(platform);

        final player = NinjaPlayer(
          position: Vector2(120, 138), // hitboxLeft=137, hitboxRight=167
          groundY: 138,
          floorBaselineY: 550,
          animations: testAnimations,
        );
        await game.ensureAdd(player);

        player
          ..verticalVelocity = 0
          ..update(0.01);
        expect(player.currentPlatform, equals(platform));

        // Move player so body's left edge crosses platform right (x=200):
        // hitboxLeft = position.x + 17.
        // When position.x = 184, hitboxLeft = 201 > 200.
        player
          ..position.x = 184
          ..update(0.01);

        expect(player.currentPlatform, isNull);
        expect(player.groundY, equals(550));
      },
    );
  });
}
