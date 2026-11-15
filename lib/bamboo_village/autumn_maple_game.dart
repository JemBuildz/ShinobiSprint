import 'dart:ui';
import 'package:flame/camera.dart';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:super_dash/bamboo_village/ninja_player.dart';
import 'package:super_dash/bamboo_village/particle_effects.dart';
import 'package:super_dash/bamboo_village/platform_component.dart';
import 'package:super_dash/game/components/feudal_foe.dart';
import 'package:super_dash/game/levels/stage_hitbox_data.dart';

/// Level 1: Nighttime Autumn Maple Forest & Pagoda Bridge Flame Game
///
/// Implemented using the Master Stage Plate Architecture:
/// - Single 100% whole hand-painted scene plate renders in 1 GPU texture pass.
/// - Calibrated invisible collision surfaces for grassy cliffs, arched wooden
///   bridge, right pagoda terrace, and river mist hazard pit.
/// - Dynamic entities: Blue Chibi Ninja, collectible soul orbs, and exit goal.
class AutumnMapleGame extends FlameGame
    with HasCollisionDetection, HasKeyboardHandlerComponents {
  /// Creates an [AutumnMapleGame].
  AutumnMapleGame({
    this.onOrbsChanged,
    this.onHazardHit,
    this.debugHitboxes = false,
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

  /// Debug hitbox display flag.
  bool debugHitboxes;

  /// Player entity component.
  late final NinjaPlayerComponent player;

  /// Master stage plate component mounting the 100% whole background plate.
  late final MasterStagePlateComponent masterPlate;

  /// Native stage width standard.
  static const double levelWidth = 1024;

  /// Native stage height standard.
  static const double levelHeight = 576;

  /// Collected orbs counter.
  int orbsCollected = 0;

  @override
  Color backgroundColor() => const Color(0xFF0A0F1A);

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
      StageCalibrationData.level1AutumnMaple.imageAsset,
    );
    final orbSprite = await loadSprite('prop_spirit_orb_clean.png');
    final ninjaAnims = await NinjaAnimations.load(this);

    // 3. Mount Master Stage Plate Component (Priority: 0, 1 GPU draw call)
    masterPlate = MasterStagePlateComponent(
      calibrationData: StageCalibrationData.level1AutumnMaple,
      stageSprite: stagePlateSprite,
      debugDrawHitboxes: debugHitboxes,
    );
    await world.add(masterPlate);

    // 3b. Mount River Water Foam, Gorge Mist, and Drifting Leaves
    await world.addAll([
      RiverFoamRippleEmitter(
        riverBounds: const Rect.fromLTWH(275, 520, 480, 56),
        currentSpeed: 42,
        rippleCount: 24,
      ),
      WaterfallMistEmitter(
        mistBounds: const Rect.fromLTWH(275, 480, 480, 90),
        baseColor: const Color(0x3076B9E8),
        particleCount: 20,
      ),
      MapleLeafParticleEmitter(),
    ]);

    // 4. Collectible Soul Orbs
    final orbsToSpawn = customOrbPositions ??
        StageCalibrationData.level1AutumnMaple.soulOrbs;
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

    // 5. Patrolling Feudal Foes (Tengu / Ronin)
    for (final pos in customFoePositions ?? const <Vector2>[]) {
      await world.add(
        FeudalFoe(
          foeType: FoeType.tengu,
          position: pos,
          speed: 55,
          onPlayerDefeated: onHazardHit ?? restart,
        )..priority = 4,
      );
    }

    // 6. Chibi Blue Ninja Player
    player = NinjaPlayerComponent(
      position: StageCalibrationData.level1AutumnMaple.playerStart,
      ninjaSprite: ninjaAnims.sprite,
      runAnimation: ninjaAnims.run,
      idleAnimation: ninjaAnims.idle,
      jumpAnimation: ninjaAnims.jump,
      attackAnimation: ninjaAnims.attack,
      deathAnimation: ninjaAnims.death,
      onHazardHit: onHazardHit ?? restart,
    )..priority = 5;
    await world.add(player);
  }

  /// Toggle visual debug hitboxes.
  void toggleHitboxes() {
    debugHitboxes = !debugHitboxes;
    masterPlate.debugDrawHitboxes = debugHitboxes;
  }

  /// Reset the player back to the calibrated start of the level.
  void restart() {
    player.reset(
      newPosition: StageCalibrationData.level1AutumnMaple.playerStart,
    );
  }
}
