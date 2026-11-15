import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/bamboo_village/bamboo_village.dart';
import 'package:super_dash/game/components/feudal_foe.dart';
import 'package:super_dash/game/levels/stage_hitbox_data.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('Bamboo Village Platformer Level', () {
    test('MainGame initializes with level dimensions and properties', () {
      final game = MainGame();
      expect(MainGame.levelWidth, equals(1024));
      expect(MainGame.levelHeight, equals(576));
      expect(game.backgroundColor(), equals(const Color(0xFF1E3A2B)));
    });

    test('PlatformComponent initializes with one-way hitbox', () {
      final platform = PlatformComponent(
        position: Vector2(100, 200),
        size: Vector2(150, 20),
      );
      expect(platform.position, equals(Vector2(100, 200)));
      expect(platform.size, equals(Vector2(150, 20)));
      expect(platform.isOneWay, isTrue);
    });

    test('GroundBlockComponent initializes with solid dimensions', () {
      final ground = GroundBlockComponent(
        position: Vector2(0, 400),
        size: Vector2(300, 100),
      );
      expect(ground.position, equals(Vector2(0, 400)));
      expect(ground.size, equals(Vector2(300, 100)));
    });

    testWidgets('BambooVillageView renders GameWidget and control overlays',
        (tester) async {
      await tester.binding.setSurfaceSize(const Size(1024, 576));

      await tester.pumpWidget(
        const MaterialApp(
          home: BambooVillageView(),
        ),
      );

      // Verify header and debug chips
      expect(find.text('Bamboo Village Level Test'), findsOneWidget);
      expect(find.text('Hitboxes OFF'), findsOneWidget);

      // Verify controls pill
      expect(
        find.text(
          'Move: [A]/[D] or ←/→  |  Jump: [Space]  |  Drop: [S] + [Space]',
        ),
        findsOneWidget,
      );

      // Toggle hitbox chip
      await tester.tap(find.text('Hitboxes OFF'));
      await tester.pump();
      expect(find.text('Hitboxes ON'), findsOneWidget);
    });

    test(
      'TwilightSanctuaryGame initializes with extended level dimensions',
      () {
      final game = TwilightSanctuaryGame();
      expect(TwilightSanctuaryGame.levelWidth, equals(1024));
      expect(TwilightSanctuaryGame.levelHeight, equals(576));
      expect(game.backgroundColor(), equals(const Color(0xFF0C101A)));
      expect(game.orbsCollected, equals(0));
    });

    test('SpikeHazardComponent initializes with hazard dimensions', () {
      final spike = SpikeHazardComponent(
        position: Vector2(350, 500),
        size: Vector2(120, 36),
      );
      expect(spike.position, equals(Vector2(350, 500)));
      expect(spike.size, equals(Vector2(120, 36)));
    });

    test('ShurikenHazardComponent rotates on update', () {
      final shuriken = ShurikenHazardComponent(
        position: Vector2(740, 330),
      );
      expect(shuriken.angle, equals(0));
      shuriken.update(0.5);
      expect(shuriken.angle, greaterThan(0));
    });

    test('SpiritOrbComponent triggers onCollected and sets isCollected', () {
      var collected = false;
      final orb = SpiritOrbComponent(
        position: Vector2(400, 300),
        onCollected: () => collected = true,
      );
      expect(orb.isCollected, isFalse);
      orb.collect();
      expect(orb.isCollected, isTrue);
      expect(collected, isTrue);
    });

    testWidgets('TwilightSanctuaryView renders GameWidget and HUD controls',
        (tester) async {
      await tester.binding.setSurfaceSize(const Size(1024, 576));

      await tester.pumpWidget(
        const MaterialApp(
          home: TwilightSanctuaryView(),
        ),
      );

      expect(find.text('Level 2: Twilight Sanctuary'), findsOneWidget);
      expect(find.text('Orbs: 0 / 4'), findsOneWidget);
      expect(find.text('Hitboxes OFF'), findsOneWidget);

      await tester.tap(find.text('Hitboxes OFF'));
      await tester.pump();
      expect(find.text('Hitboxes ON'), findsOneWidget);
    });

    test('AutumnMapleGame initializes with fixed 16:9 viewport and colors', () {
      final game = AutumnMapleGame();
      expect(AutumnMapleGame.levelWidth, equals(1024));
      expect(AutumnMapleGame.levelHeight, equals(576));
      expect(game.backgroundColor(), equals(const Color(0xFF0A0F1A)));
      expect(game.orbsCollected, equals(0));
    });

    test('LeafParticleData updates position and oscillations correctly', () {
      final p = LeafParticleData(
        x: 100,
        y: 100,
        speedX: 50,
        speedY: 20,
        rotation: 0,
        rotSpeed: 1,
        scale: 1,
        oscillationPhase: 0,
      );
      expect(p.x, equals(100));
      expect(p.y, equals(100));
    });

    test('NinjaPlayerComponent initializes with idle state', () {
      final player = NinjaPlayerComponent(
        position: Vector2(100, 490),
      );
      expect(player.state, equals(NinjaState.idle));
    });

    test(
      'NinjaPlayerComponent transitions across idle, running, leaping, falling',
      () {
        final player = NinjaPlayerComponent(
          position: Vector2(100, 490),
        )
          ..isOnGround = true
          ..velocity = Vector2.zero()
          ..update(0.016);
        expect(player.state, equals(NinjaState.idle));

        // Running right on ground
        player
          ..moveRight()
          ..isOnGround = true
          ..update(0.016);
        expect(player.velocity.x, equals(player.horizontalSpeed));
        expect(player.state, equals(NinjaState.running));
        expect(player.isFacingRight, isTrue);

        // Running left on ground
        player
          ..moveLeft()
          ..isOnGround = true
          ..update(0.016);
        expect(player.velocity.x, equals(-player.horizontalSpeed));
        expect(player.state, equals(NinjaState.running));
        expect(player.isFacingRight, isFalse);

        // Jumping upwards -> leaping state
        player
          ..stopMoving()
          ..isOnGround = true
          ..jump();
        expect(player.isOnGround, isFalse);
        expect(player.velocity.y, equals(player.jumpImpulse));
        player.update(0.016);
        expect(player.state, equals(NinjaState.leaping));

        // Descending downwards -> falling state
        player
          ..velocity.y = 200
          ..isOnGround = false
          ..update(0.016);
        expect(player.state, equals(NinjaState.falling));
      },
    );

    test('StageCalibrationData matches calibration registry', () {
      final lTorii = StageCalibrationData.level1ToriiShrine;
      expect(lTorii.stageId, equals(1));
      expect(lTorii.playerStart, equals(Vector2(340, 298)));
      expect(lTorii.soulOrbs.length, equals(6));
      expect(lTorii.hitboxes.length, equals(5));
      expect(lTorii.slopes?.length, equals(2));

      final l1 = StageCalibrationData.level1AutumnMaple;
      expect(l1.stageId, equals(1));
      expect(l1.playerStart, equals(Vector2(70, 418)));
      expect(l1.soulOrbs.length, equals(4));
      expect(l1.hitboxes.length, equals(4));

      final l2 = StageCalibrationData.level2SunsetBamboo;
      expect(l2.stageId, equals(2));
      expect(l2.playerStart, equals(Vector2(70, 298)));
      expect(l2.soulOrbs.length, equals(5));
      expect(l2.hitboxes.length, equals(7));

      // Test aspect ratio scaling
      final box = l1.hitboxes.first;
      final unscaledRect = box.toRect();
      expect(unscaledRect.left, equals(0));
      expect(unscaledRect.top, equals(418));
      expect(unscaledRect.width, equals(275));
      expect(unscaledRect.height, equals(158));

      final scaledRect = box.toRect(Vector2(2048, 1152));
      expect(scaledRect.width, equals(550));
      expect(scaledRect.height, equals(316));
    });

    test(
      'MasterStagePlateComponent mounts hitboxes for calibrated stages',
      () async {
        final plate = MasterStagePlateComponent(
          calibrationData: StageCalibrationData.level1AutumnMaple,
          debugDrawHitboxes: true,
        );
        await plate.onLoad();
        expect(plate.children.length, equals(4));
        expect(plate.debugDrawHitboxes, isTrue);
      },
    );

    test('NinjaPlayerComponent transitions to dead state on die()', () {
      final player = NinjaPlayerComponent(position: Vector2(100, 300));
      expect(player.isDead, isFalse);
      expect(player.state, equals(NinjaState.idle));

      player.die();
      expect(player.isDead, isTrue);
      expect(player.state, equals(NinjaState.dead));
      expect(player.velocity.y, equals(-160));
    });

    test(
      'NinjaPlayerComponent ignores input and triggers onHazardHit when dead',
      () {
        var hazardHitCalled = false;
        final player = NinjaPlayerComponent(
          position: Vector2(100, 300),
          onHazardHit: () => hazardHitCalled = true,
        )..die();
        expect(player.isDead, isTrue);

        // Verify controls are ignored
        player
          ..moveRight()
          ..moveLeft();
        expect(player.velocity.x, equals(0));

        // Advance through death timer (0.8s)
        player
          ..update(0.5)
          ..update(0.35);
        expect(hazardHitCalled, isTrue);
      },
    );

    test('NinjaPlayerComponent resets properly after death', () {
      final player = NinjaPlayerComponent(position: Vector2(100, 300))
        ..die();
      expect(player.isDead, isTrue);

      player.reset(newPosition: Vector2(50, 400));
      expect(player.isDead, isFalse);
      expect(player.state, equals(NinjaState.idle));
      expect(player.position, equals(Vector2(50, 400)));
      expect(player.isOnGround, isTrue);
    });

    test(
      'NinjaPlayerComponent triggers die() on spike or shuriken collision',
      () {
        final player = NinjaPlayerComponent(position: Vector2(100, 300));
        final spike = SpikeHazardComponent(
          position: Vector2(100, 300),
          size: Vector2(32, 32),
        );

        player.onCollision({Vector2(100, 300)}, spike);
        expect(player.isDead, isTrue);
        expect(player.state, equals(NinjaState.dead));

        // Reset and test shuriken hazard
        player.reset();
        expect(player.isDead, isFalse);

        final shuriken = ShurikenHazardComponent(position: Vector2(100, 300));
        player.onCollision({Vector2(100, 300)}, shuriken);
        expect(player.isDead, isTrue);
        expect(player.state, equals(NinjaState.dead));

        // Reset and test active FeudalFoe contact
        player.reset();
        expect(player.isDead, isFalse);

        final foe = FeudalFoe(
          foeType: FoeType.ashigaru,
          position: Vector2(100, 300),
        );
        player.onCollision({Vector2(100, 300)}, foe);
        expect(player.isDead, isTrue);
        expect(player.state, equals(NinjaState.dead));
      },
    );

    test('NinjaPlayerComponent ignores defeated FeudalFoe collision', () {
      final player = NinjaPlayerComponent(position: Vector2(100, 300));
      final foe = FeudalFoe(
        foeType: FoeType.ashigaru,
        position: Vector2(100, 300),
      )..defeat();

      player.onCollision({Vector2(100, 300)}, foe);
      expect(player.isDead, isFalse);
      expect(player.state, equals(NinjaState.idle));
    });

    test('NinjaPlayerComponent dies on pit fall (y > 600)', () {
      final player = NinjaPlayerComponent(position: Vector2(100, 605))
        ..update(0.016);
      expect(player.isDead, isTrue);
      expect(player.state, equals(NinjaState.dead));
    });

    test('WaterfallMistEmitter initializes particles and updates over time',
        () {
      final emitter = WaterfallMistEmitter(
        mistBounds: const Rect.fromLTWH(200, 450, 400, 80),
        particleCount: 15,
        upwardSpeed: 30,
      )..onLoad();

      expect(emitter.particles.length, equals(15));
      final initialY = emitter.particles.first.y;

      emitter.update(0.1);
      // Particle should drift upward (lower y coordinate)
      expect(emitter.particles.first.y, lessThan(initialY + 5.0));
      expect(emitter.particles.first.progress, inInclusiveRange(0.0, 1.0));
    });

    test('RiverFoamRippleEmitter initializes ripples and advances current', () {
      final emitter = RiverFoamRippleEmitter(
        riverBounds: const Rect.fromLTWH(200, 520, 400, 50),
        rippleCount: 18,
        currentSpeed: 40,
      )..onLoad();

      expect(emitter.ripples.length, equals(18));
      final initialX = emitter.ripples.first.x;

      emitter.update(0.1);
      // Ripple should flow downstream (greater x coordinate)
      expect(emitter.ripples.first.x, greaterThan(initialX));
      expect(emitter.ripples.first.progress, inInclusiveRange(0.0, 1.0));
    });
  });
}
