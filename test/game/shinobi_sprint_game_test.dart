import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/sprite.dart';
import 'package:flame_test/flame_test.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:super_dash/game/components/elevated_platform.dart';
import 'package:super_dash/game/components/ninja_player.dart';
import 'package:super_dash/game/shinobi_sprint_game.dart';

class _MockSpriteAnimation extends Mock implements SpriteAnimation {
  @override
  SpriteAnimationTicker createTicker() => _MockSpriteAnimationTicker();
}

class _MockSpriteAnimationTicker extends Mock
    implements SpriteAnimationTicker {
  @override
  void reset() {}
}

class _MockKeyDownEvent extends Mock implements KeyDownEvent {
  @override
  String toString({DiagnosticLevel minLevel = DiagnosticLevel.info}) {
    return '';
  }
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('ShinobiSprintGame', () {
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

    NinjaPlayer createPlayer() {
      return NinjaPlayer(
        position: Vector2(100, 300),
        groundY: 300,
        animations: testAnimations,
      );
    }

    testWithGame(
      'initializes with ninjaPlayer',
      () => ShinobiSprintGame(ninjaPlayer: createPlayer()),
      (game) async {
        expect(game.ninjaPlayer.isMounted, isTrue);
        expect(game.ninjaPlayer.current, equals(NinjaState.running));
      },
    );

    testWithGame(
      'mounts continuous boardwalk ground and calibrates ninja feet on '
      'baseline',
      ShinobiSprintGame.new,
      (game) async {
        expect(game.boardwalkGround.isMounted, isTrue);
        expect(
          game.boardwalkGround.position.y,
          equals(ShinobiSprintGame.defaultBaseGroundY),
        );
        expect(game.ninjaPlayer.isMounted, isTrue);
        expect(
          game.ninjaPlayer.footPositionY,
          equals(ShinobiSprintGame.defaultBaseGroundY),
        );
      },
    );

    testWithGame(
      'mounts elevated one-way platforms in game tree',
      ShinobiSprintGame.new,
      (game) async {
        final platforms = game.children.whereType<ElevatedPlatform>();
        expect(platforms.length, equals(3));
        expect(platforms.every((p) => p.isMounted), isTrue);
      },
    );

    testWithGame(
      'onTapDown triggers ninja jump',
      () => ShinobiSprintGame(ninjaPlayer: createPlayer()),
      (game) async {
        expect(game.ninjaPlayer.isJumping, isFalse);

        final tapInfo = TapDownInfo.fromDetails(
          game,
          TapDownDetails(),
        );

        game.onTapDown(tapInfo);

        expect(game.ninjaPlayer.isJumping, isTrue);
        expect(game.ninjaPlayer.verticalVelocity, equals(-600));
        expect(game.ninjaPlayer.current, equals(NinjaState.jumping));
      },
    );

    testWithGame(
      'onKeyEvent with Space triggers ninja jump',
      () => ShinobiSprintGame(ninjaPlayer: createPlayer()),
      (game) async {
        expect(game.ninjaPlayer.isJumping, isFalse);

        final event = _MockKeyDownEvent();
        when(() => event.logicalKey).thenReturn(LogicalKeyboardKey.space);

        final result = game.onKeyEvent(event, {LogicalKeyboardKey.space});

        expect(result, equals(KeyEventResult.handled));
        expect(game.ninjaPlayer.isJumping, isTrue);
        expect(game.ninjaPlayer.verticalVelocity, equals(-600));
      },
    );

    testWithGame(
      'onKeyEvent with ArrowUp triggers ninja jump',
      () => ShinobiSprintGame(ninjaPlayer: createPlayer()),
      (game) async {
        expect(game.ninjaPlayer.isJumping, isFalse);

        final event = _MockKeyDownEvent();
        when(() => event.logicalKey).thenReturn(LogicalKeyboardKey.arrowUp);

        final result = game.onKeyEvent(event, {LogicalKeyboardKey.arrowUp});

        expect(result, equals(KeyEventResult.handled));
        expect(game.ninjaPlayer.isJumping, isTrue);
        expect(game.ninjaPlayer.verticalVelocity, equals(-600));
      },
    );

    testWithGame(
      'defaults to nighttime and switches to daytime with integrated assets',
      () => ShinobiSprintGame(ninjaPlayer: createPlayer()),
      (game) async {
        // Defaults to night
        expect(game.isDaytime, isFalse);
        expect(
          game.activeIntegratedAsset,
          equals('backgrounds/wide_night_strip.png'),
        );
        expect(game.parallaxBackground.isDaytime, isFalse);

        // Switch to daytime
        game.isDaytime = true;
        expect(game.isDaytime, isTrue);
        expect(
          game.activeIntegratedAsset,
          equals('backgrounds/wide_day_strip.png'),
        );
        expect(game.parallaxBackground.isDaytime, isTrue);

        // Toggle back to night
        game.toggleDayNight();
        expect(game.isDaytime, isFalse);
        expect(
          game.activeIntegratedAsset,
          equals('backgrounds/wide_night_strip.png'),
        );
        expect(game.parallaxBackground.isDaytime, isFalse);

        // Switch back to day via setter
        game.isDaytime = true;
        expect(game.isDaytime, isTrue);
        expect(
          game.activeIntegratedAsset,
          equals('backgrounds/wide_day_strip.png'),
        );
      },
    );

    testWithGame(
      'initializes with isDaytime: true',
      () => ShinobiSprintGame(
        ninjaPlayer: createPlayer(),
        isDaytime: true,
      ),
      (game) async {
        expect(game.isDaytime, isTrue);
        expect(
          game.activeIntegratedAsset,
          equals('backgrounds/wide_day_strip.png'),
        );
        expect(game.parallaxBackground.isDaytime, isTrue);
      },
    );

    testWithGame(
      'depthLayers preserves velocity multipliers across state transitions',
      () => ShinobiSprintGame(ninjaPlayer: createPlayer()),
      (game) async {
        const expectedMultipliers = [0, 0.25, 0.5, 0.75, 1];

        for (var i = 0; i < game.depthLayers.length; i++) {
          expect(
            game.depthLayers[i].velocityMultiplier,
            equals(expectedMultipliers[i]),
          );
        }

        // Switch to daytime
        game.isDaytime = true;
        for (var i = 0; i < game.depthLayers.length; i++) {
          expect(
            game.depthLayers[i].velocityMultiplier,
            equals(expectedMultipliers[i]),
          );
        }
      },
    );
  });
}
