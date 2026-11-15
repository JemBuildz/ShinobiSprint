import 'dart:ui';
import 'package:flame/camera.dart';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:super_dash/bamboo_village/ninja_player.dart';
import 'package:super_dash/bamboo_village/particle_effects.dart';
import 'package:super_dash/bamboo_village/platform_component.dart';
import 'package:super_dash/game/components/feudal_foe.dart';

/// Level 1: Daytime Bamboo Village Flame Game
///
/// Implemented using the Cinematic Unified-Plate Architecture:
/// - Hand-painted morning sunlit village with Mount Fuji and bamboo groves.
/// - Precision collision surfaces for left/right ground, lower chasm bridge,
///   elevated bamboo platform table, raised cliff, and dojo rooftops.
/// - Dynamic entities: Blue Chibi Ninja, collectible golden Spirit Orbs,
///   and floating sunlit bamboo pollen/leaf particles.
class MainGame extends FlameGame
    with HasCollisionDetection, HasKeyboardHandlerComponents {
  /// Creates a [MainGame].
  MainGame({
    this.onOrbsChanged,
    this.onHazardHit,
    this.customOrbPositions,
    this.customFoePositions,
  });

  /// Optional callback invoked whenever a spirit orb is collected.
  final void Function(int orbs)? onOrbsChanged;

  /// Optional callback invoked whenever the player is defeated by a hazard.
  final VoidCallback? onHazardHit;

  /// Optional custom orb positions for level-specific challenges.
  final List<Vector2>? customOrbPositions;

  /// Optional custom foe positions for patrol challenges.
  final List<Vector2>? customFoePositions;

  late final NinjaPlayerComponent player;

  static const double levelWidth = 1024;
  static const double levelHeight = 576;

  int orbsCollected = 0;

  @override
  Color backgroundColor() => const Color(0xFF1E3A2B);

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    // 1. Camera Viewport setup with fixed 16:9 resolution
    camera.viewport = FixedResolutionViewport(
      resolution: Vector2(levelWidth, levelHeight),
    );
    camera.viewfinder.anchor = Anchor.center;
    camera.viewfinder.position = Vector2(levelWidth / 2, levelHeight / 2);

    // 2. Load Sprites & Animations
    final stagePlateSprite = await loadSprite(
      'stage1_daytime_torii_shrine_1024.png',
    );
    final orbSprite = await loadSprite('prop_spirit_orb_clean.png');
    final ninjaSprite = await loadSprite('character_ninja.png');
    final runAnimation = await loadSpriteAnimation(
      'spritesheet_ninja_run.png',
      SpriteAnimationData.sequenced(
        amount: 5,
        stepTime: 0.08,
        textureSize: Vector2(128, 128),
      ),
    );
    final idleAnimation = await loadSpriteAnimation(
      'spritesheet_ninja_idle.png',
      SpriteAnimationData.sequenced(
        amount: 4,
        stepTime: 0.16,
        textureSize: Vector2(128, 128),
      ),
    );
    final jumpAnimation = await loadSpriteAnimation(
      'spritesheet_ninja_jump.png',
      SpriteAnimationData.sequenced(
        amount: 4,
        stepTime: 0.12,
        textureSize: Vector2(128, 128),
        loop: false,
      ),
    );
    final attackAnimation = await loadSpriteAnimation(
      'spritesheet_ninja_attack.png',
      SpriteAnimationData.sequenced(
        amount: 4,
        stepTime: 0.08,
        textureSize: Vector2(128, 128),
        loop: false,
      ),
    );
    final deathAnimation = await loadSpriteAnimation(
      'spritesheet_ninja_death.png',
      SpriteAnimationData.sequenced(
        amount: 4,
        stepTime: 0.15,
        textureSize: Vector2(128, 128),
        loop: false,
      ),
    );

    // 3. Cinematic Stage Plate (Priority: 0 - High Resolution Plate
    // with Bilinear Filtering)
    final stagePlate = SpriteComponent(
      sprite: stagePlateSprite,
      size: Vector2(levelWidth, levelHeight),
      position: Vector2.zero(),
      priority: 0,
      paint: Paint()
        ..filterQuality = FilterQuality.medium
        ..isAntiAlias = true,
    );
    await world.add(stagePlate);

    // 4. Mapped Architectural Collision Surfaces & Staircase Ramps
    // Left Mountain Bluff Ground (Solid, y = 350)
    final leftMountainBluff = GroundBlockComponent(
      position: Vector2(0, 350),
      size: Vector2(455, levelHeight - 350),
    )..priority = 3;
    await world.add(leftMountainBluff);

    // Right Mountain Bluff Ground (Solid, y = 350)
    final rightMountainBluff = GroundBlockComponent(
      position: Vector2(585, 350),
      size: Vector2(439, levelHeight - 350),
    )..priority = 3;
    await world.add(rightMountainBluff);

    // Center Mountain Chasm Lethal Hazard
    final chasmHazard = SpikeHazardComponent(
      position: Vector2(455, 520),
      size: Vector2(130, 56),
    )..priority = 3;
    await world.add(chasmHazard);

    // Left Hillside Shrine Terrace Porch
    final leftShrineTerrace = PlatformComponent(
      position: Vector2(0, 265),
      size: Vector2(140, 20),
    )..priority = 3;
    await world.add(leftShrineTerrace);

    // Left Shrine Staircase Ramp (Ramps from bluff y = 350 to porch y = 265)
    final leftStaircaseRamp = SlopePlatformComponent(
      start: Vector2(315, 350),
      end: Vector2(140, 265),
    );
    await world.add(leftStaircaseRamp);

    // Grand Torii Staircase Ramp (Ascends from bluff y = 350 to temple
    // terrace y = 150)
    final grandStaircaseRamp = SlopePlatformComponent(
      start: Vector2(700, 350),
      end: Vector2(890, 150),
    );
    await world.add(grandStaircaseRamp);

    // Upper Grand Shinto Shrine Terrace Landing
    final upperShrineTerrace = PlatformComponent(
      position: Vector2(890, 150),
      size: Vector2(134, 20),
    )..priority = 3;
    await world.add(upperShrineTerrace);

    // 5. Collectible Golden Spirit Orbs (Priority: 4)
    final orbsToSpawn = customOrbPositions ??
        [
          Vector2(70, 220), // Left shrine porch
          Vector2(230, 290), // Left stairs
          Vector2(340, 310), // Cobblestone path
          Vector2(520, 290), // Midair leap over mountain chasm
          Vector2(795, 240), // Ascending grand Torii staircase
          Vector2(960, 100), // Upper mountain temple pavilion
        ];

    for (final pos in orbsToSpawn) {
      final orb = SpiritOrbComponent(
        sprite: orbSprite,
        position: pos,
        onCollected: () {
          orbsCollected++;
          onOrbsChanged?.call(orbsCollected);
        },
      )..priority = 4;
      await world.add(orb);
    }

    // 6. Floating Sunlit Bamboo Pollen Particle System (Priority: 2)
    final leafEmitter = BambooPollenEmitter();
    await world.add(leafEmitter);

    // 7. Patrolling Feudal Foes (Ashigaru)
    final foesToSpawn = customFoePositions ?? [];
    for (final pos in foesToSpawn) {
      final foe = FeudalFoe(
        foeType: FoeType.ashigaru,
        position: pos,
        speed: 45,
        patrolRange: 50,
        onPlayerDefeated: onHazardHit ?? resetPlayer,
      )..priority = 4;
      await world.add(foe);
    }

    // 8. Chibi Blue Ninja Player (Priority: 5)
    // Spawns standing directly on the true ground baseline (x = 340, y = 350)
    player = NinjaPlayerComponent(
      position: Vector2(340, 350),
      ninjaSprite: ninjaSprite,
      runAnimation: runAnimation,
      idleAnimation: idleAnimation,
      jumpAnimation: jumpAnimation,
      attackAnimation: attackAnimation,
      deathAnimation: deathAnimation,
      onHazardHit: onHazardHit ?? resetPlayer,
    )..priority = 5;
    await world.add(player);
  }

  /// Reset the player back to the start of the level.
  void resetPlayer() {
    player.reset(newPosition: Vector2(340, 350));
  }
}
