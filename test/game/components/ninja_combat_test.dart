import 'package:flame/game.dart';
import 'package:flame_test/flame_test.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:super_dash/game/components/katana_slash.dart';
import 'package:super_dash/game/components/ninja_player.dart';
import 'package:super_dash/game/components/shuriken_projectile.dart';
import 'package:super_dash/game/shinobi_sprint_game.dart';

class _TestGame extends FlameGame {}

class _MockKeyDownEvent extends Mock implements KeyDownEvent {
  @override
  String toString({DiagnosticLevel minLevel = DiagnosticLevel.info}) =>
      super.toString();
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('KatanaSlash', () {
    testWithGame<_TestGame>(
      'advances progress and auto-removes after duration',
      _TestGame.new,
      (game) async {
        final slash = KatanaSlash(
          position: Vector2(100, 100),
          slashDuration: 0.2,
        );

        await game.ensureAdd(slash);
        expect(slash.isMounted, isTrue);
        expect(slash.isActive, isTrue);
        expect(slash.progress, equals(0.0));

        game.update(0.1);
        expect(slash.progress, closeTo(0.5, 0.01));
        expect(slash.isActive, isTrue);

        game.update(0.15);
        expect(slash.progress, equals(1.0));
        game.update(0);
        expect(slash.isMounted, isFalse);
      },
    );
  });

  group('ShurikenProjectile', () {
    testWithGame<_TestGame>(
      'travels forward with angular rotation and auto-removes at max distance',
      _TestGame.new,
      (game) async {
        final projectile = ShurikenProjectile(
          position: Vector2(50, 100),
          velocity: Vector2(500, 0),
          rotationSpeed: 10,
          maxTravelDistance: 200,
        );

        await game.ensureAdd(projectile);
        expect(projectile.isMounted, isTrue);

        game.update(0.1);
        expect(projectile.position.x, closeTo(100.0, 0.5));
        expect(projectile.angle, closeTo(1.0, 0.05));

        // Travel beyond 200 distance
        game
          ..update(0.4)
          ..update(0);
        expect(projectile.isMounted, isFalse);
      },
    );
  });

  group('NinjaPlayer Combat Actions', () {
    testWithGame<_TestGame>(
      'katanaSlash sets attacking state and spawns KatanaSlash',
      _TestGame.new,
      (game) async {
        final player = NinjaPlayer(
          position: Vector2(100, 200),
          groundY: 200,
        );

        await game.ensureAdd(player);

        player.katanaSlash();
        expect(player.current, equals(NinjaState.attacking));
        expect(player.isAttacking, isTrue);
        expect(player.activeSlashes.length, equals(1));

        game.update(0);
        expect(game.children.whereType<KatanaSlash>().length, equals(1));

        // After attack duration, transitions back to running
        game.update(player.attackDuration + 0.02);
        expect(player.isAttacking, isFalse);
        expect(player.current, equals(NinjaState.running));
      },
    );

    testWithGame<_TestGame>(
      'katanaSlash in mid-air returns to jumping after attack finishes',
      _TestGame.new,
      (game) async {
        final player = NinjaPlayer(
          position: Vector2(100, 100),
          groundY: 300,
        );

        await game.ensureAdd(player);
        player
          ..current = NinjaState.jumping
          ..katanaSlash();
        expect(player.isAttacking, isTrue);

        game.update(player.attackDuration + 0.02);
        expect(player.isAttacking, isFalse);
        expect(player.current, equals(NinjaState.jumping));
      },
    );

    testWithGame<_TestGame>(
      'throwShuriken spawns projectile in parent',
      _TestGame.new,
      (game) async {
        final player = NinjaPlayer(
          position: Vector2(100, 200),
          groundY: 200,
        );

        await game.ensureAdd(player);

        final shuriken = player.throwShuriken();
        expect(player.activeShurikens.contains(shuriken), isTrue);

        await game.ready();
        expect(game.children.whereType<ShurikenProjectile>().length, equals(1));
      },
    );
  });

  group('ShinobiSprintGame Combat Key Handling', () {
    testWithGame<ShinobiSprintGame>(
      'KeyX triggers katana slash',
      ShinobiSprintGame.new,
      (game) async {
        expect(game.ninjaPlayer.isAttacking, isFalse);

        final event = _MockKeyDownEvent();
        when(() => event.logicalKey).thenReturn(LogicalKeyboardKey.keyX);

        final result = game.onKeyEvent(event, {LogicalKeyboardKey.keyX});
        expect(result, equals(KeyEventResult.handled));
        expect(game.ninjaPlayer.isAttacking, isTrue);
      },
    );

    testWithGame<ShinobiSprintGame>(
      'KeyC triggers shuriken throw',
      ShinobiSprintGame.new,
      (game) async {
        final initialShurikens = game.ninjaPlayer.activeShurikens.length;

        final event = _MockKeyDownEvent();
        when(() => event.logicalKey).thenReturn(LogicalKeyboardKey.keyC);

        final result = game.onKeyEvent(event, {LogicalKeyboardKey.keyC});
        expect(result, equals(KeyEventResult.handled));
        expect(
          game.ninjaPlayer.activeShurikens.length,
          equals(initialShurikens + 1),
        );
      },
    );
  });
}
