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

/// Level 2: Sunset Bamboo Forest & Torii Ridge Flame Game
///
/// Implemented using the Master Stage Plate Architecture:
/// - Single 100% whole hand-painted scene plate renders in 1 GPU texture pass.
/// - Calibrated invisible collision surfaces for entrance Torii platform,
///   spike trap hazard, suspended bridges, center stone lantern platform,
///   sanctuary ridge slope, and bottom chasm pit.
/// - Dynamic entities: Blue Chibi Ninja, collectible soul orbs, and exit goal.
class TwilightSanctuaryGame extends FlameGame
    with HasCollisionDetection, HasKeyboardHandlerComponents {
  /// Creates a [TwilightSanctuaryGame].
  TwilightSanctuaryGame({
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
  Color backgroundColor() => const Color(0xFF0C101A);

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
      StageCalibrationData.level2SunsetBamboo.imageAsset,
    );
    final ninjaAnims = await NinjaAnimations.load(this);
    final orbSprite = await loadSprite('prop_spirit_orb_clean.png');

    // 3. Mount Master Stage Plate Component (Priority: 0, 1 GPU draw call)
    masterPlate = MasterStagePlateComponent(
      calibrationData: StageCalibrationData.level2SunsetBamboo,
      stageSprite: stagePlateSprite,
      debugDrawHitboxes: debugHitboxes,
    );
    await world.add(masterPlate);

    // 3b. Waterfall Gorge Mist & River Rapids Foam
    await world.addAll([
      RiverFoamRippleEmitter(
        riverBounds: const Rect.fromLTWH(220, 510, 540, 66),
        currentSpeed: 55,
      ),
      WaterfallMistEmitter(
        mistBounds: const Rect.fromLTWH(220, 460, 540, 100),
        baseColor: const Color(0x35E0F7FA),
        particleCount: 24,
        upwardSpeed: 28,
      ),
    ]);

    // 4. Collectible Soul Orbs
    final orbsToSpawn = customOrbPositions ??
        StageCalibrationData.level2SunsetBamboo.soulOrbs;
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

    // 5. Patrolling Feudal Foes (Ronin)
    for (final pos in customFoePositions ?? const <Vector2>[]) {
      await world.add(
        FeudalFoe(
          foeType: FoeType.ronin,
          position: pos,
          speed: 50,
          patrolRange: 55,
        )..priority = 4,
      );
    }

    // 6. Chibi Blue Ninja Player
    player = NinjaPlayerComponent(
      position: StageCalibrationData.level2SunsetBamboo.playerStart,
      ninjaSprite: ninjaAnims.sprite,
      runAnimation: ninjaAnims.run,
      idleAnimation: ninjaAnims.idle,
      jumpAnimation: ninjaAnims.jump,
      attackAnimation: ninjaAnims.attack,
      deathAnimation: ninjaAnims.death,
      onHazardHit: onHazardHit ?? resetPlayer,
    )..priority = 5;
    await world.add(player);
  }

  /// Toggle visual debug hitboxes.
  void toggleHitboxes() {
    debugHitboxes = !debugHitboxes;
    masterPlate.debugDrawHitboxes = debugHitboxes;
  }

  /// Reset the player cleanly back to the level start.
  void resetPlayer() {
    player.reset(
      newPosition: StageCalibrationData.level2SunsetBamboo.playerStart,
    );
  }
}
