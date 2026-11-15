import 'dart:async';

import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:super_dash/audio/audio.dart';
import 'package:super_dash/game/bloc/game_bloc.dart';
import 'package:super_dash/game/components/continuous_boardwalk_ground.dart';
import 'package:super_dash/game/components/elevated_platform.dart';
import 'package:super_dash/game/components/feudal_foe.dart';
import 'package:super_dash/game/components/item_effect.dart';
import 'package:super_dash/game/components/ninja_item.dart';
import 'package:super_dash/game/components/ninja_player.dart';
import 'package:super_dash/game/components/parallax_background.dart';
import 'package:super_dash/game/components/scenery_element.dart';
import 'package:super_dash/game/config/feudal_biome.dart';
import 'package:super_dash/game/config/parallax_depth.dart';
import 'package:super_dash/game/entities/item.dart';

/// The game instance for Shinobi Sprint.
class ShinobiSprintGame extends FlameGame
    with TapDetector, KeyboardEvents, HasKeyboardHandlerComponents {
  /// Creates a [ShinobiSprintGame].
  ShinobiSprintGame({
    this.gameBloc,
    this.audioController,
    this.itemEffectFactory,
    this.customBundle,
    this.biome = FeudalBiome.bambooGrove,
    NinjaPlayer? ninjaPlayer,
    ParallaxBackground? parallaxBackground,
    bool isDaytime = false,
  })  : _isDaytime = isDaytime,
        _initialNinjaPlayer = ninjaPlayer,
        _initialParallaxBackground = parallaxBackground;

  /// The active [FeudalBiome] environment theme.
  final FeudalBiome biome;

  /// The active [GameBloc] to receive score updates.
  final GameBloc? gameBloc;

  /// The audio controller for playing sound effects.
  final AudioController? audioController;

  /// Optional factory for creating [ItemEffect] instances.
  final ItemEffect Function(ItemType type, Vector2 position)? itemEffectFactory;

  /// Custom asset bundle if provided.
  final AssetBundle? customBundle;

  final NinjaPlayer? _initialNinjaPlayer;
  final ParallaxBackground? _initialParallaxBackground;

  bool _isDaytime;

  /// Whether the game is rendered in daytime (true) or nighttime (false).
  bool get isDaytime => _isDaytime;
  set isDaytime(bool value) {
    if (_isDaytime != value) {
      _isDaytime = value;
      onDaytimeChanged();
    }
  }

  /// Toggles between daytime and nighttime themes.
  void toggleDayNight() {
    isDaytime = !isDaytime;
  }

  /// Returns the path of the active integrated wide background asset:
  /// Concept 1 (day, derived from image_27.png) or
  /// Concept 2 (night, image_28.png).
  String get activeIntegratedAsset =>
      ParallaxDepthConfig.getIntegratedWideAsset(isDaytime: isDaytime);

  /// Returns the formal 5-layer depth hierarchy defined in the
  /// image_29 pipeline.
  List<ParallaxLayerInfo> get depthLayers => ParallaxDepthConfig.layers;

  /// Handler for daytime state transitions.
  @protected
  @visibleForTesting
  void onDaytimeChanged() {
    if (isMounted) {
      parallaxBackground.isDaytime = _isDaytime;
      for (final child in children.whereType<SceneryElement>()) {
        child.isDaytime = _isDaytime;
      }
    }
  }

  /// Default base ground surface Y coordinate (matching 550px mobile baseline).
  static const double defaultBaseGroundY = 550;

  /// The active continuous boardwalk ground track.
  late final ContinuousBoardwalkGround boardwalkGround;

  /// The active [NinjaPlayer] component in the game.
  late final NinjaPlayer ninjaPlayer;

  /// The active [ParallaxBackground] component in the game.
  late final ParallaxBackground parallaxBackground;

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    // Step 1: Pre-load all required image assets asynchronously inside onLoad
    // to prevent one-time execution rendering delays or mid-game frame
    // stuttering.
    try {
      await images.loadAll([
        ...ParallaxBackground.layerAssetNames,
        ...ParallaxBackground.dayLayerAssetNames,
        ParallaxDepthConfig.dayWideAsset,
        ParallaxDepthConfig.nightWideAsset,
        ParallaxDepthConfig.concept1DayAsset,
        ParallaxDepthConfig.concept2NightAsset,
        'cutouts/torii_gate.png',
        'cutouts/pagoda_shrine_grounded.png',
        'cutouts/lantern_post_clean.png',
        'cutouts/lantern_post_glowing.png',
        'cutouts/boardwalk_continuous.png',
        'cutouts/boardwalk_elevated.png',
        'cutouts/wooden_boardwalk_platform.png',
        'cutouts/wooden_midair_platform.png',
        'cutouts/sakura_tree_1.png',
        'cutouts/stone_well.png',
        'cutouts/arched_bridge.png',
        'items/magatama_gem.png',
        'items/ofuda_talisman.png',
        'items/caltrops.png',
        'foes/ashigaru.png',
        'foes/ronin.png',
        'foes/archer.png',
        'foes/sumo.png',
        'foes/oni.png',
        'foes/tengu.png',
        'foes/hitodama.png',
        'foes/karakasa.png',
        'spritesheet_ninja_run.png',
        'spritesheet_ninja_jump.png',
        'spritesheet_ninja_attack.png',
        'shuriken_spin.png',
      ]);
    } catch (_) {
      // In headless test environments asset bundle may not be loaded
    }

    // Step 3: Mount completed parallax_background into main FlameGame tree.
    parallaxBackground = _initialParallaxBackground ??
        ParallaxBackground(
          isDaytime: _isDaytime,
          useThreeLayerDepth: true,
        );
    await add(parallaxBackground);

    // Mount continuous boardwalk ground track across the base of the stage.
    boardwalkGround = ContinuousBoardwalkGround(
      position: Vector2(0, defaultBaseGroundY),
    );
    await add(boardwalkGround);

    // Mount elevated one-way boardwalk platforms with proper support styles:
    // Upper-left and upper-right have grounded pillars anchored to the floor;
    // central upper platform is a dedicated mid-air suspension platform.
    final platforms = [
      ElevatedPlatform(
        position: Vector2(180, 440),
        size: Vector2(200, 56),
        hasGroundPillars: true,
      ),
      ElevatedPlatform(
        position: Vector2(440, 380),
        size: Vector2(220, 56),
      ),
      ElevatedPlatform(
        position: Vector2(740, 430),
        size: Vector2(210, 56),
        hasGroundPillars: true,
      ),
    ];
    for (final platform in platforms) {
      await add(platform);
    }

    // Mount grounded scenery props (Torii gate, pagoda, lanterns, sakura, well)
    final sceneryProps = [
      SceneryElement(
        sceneryType: SceneryType.pagoda,
        depthSlice: ParallaxDepthSlice.midBackSlice,
        position: Vector2(140, defaultBaseGroundY),
        size: Vector2(130, 180),
        isDaytime: _isDaytime,
      ),
      SceneryElement(
        sceneryType: SceneryType.toriiGate,
        depthSlice: ParallaxDepthSlice.frontSlice,
        position: Vector2(330, defaultBaseGroundY),
        size: Vector2(125, 155),
        isDaytime: _isDaytime,
      ),
      SceneryElement(
        sceneryType: SceneryType.sakuraTree,
        depthSlice: ParallaxDepthSlice.midSlice,
        position: Vector2(580, defaultBaseGroundY),
        isDaytime: _isDaytime,
      ),
      SceneryElement(
        sceneryType: SceneryType.stoneWell,
        depthSlice: ParallaxDepthSlice.midFrontSlice,
        position: Vector2(280, defaultBaseGroundY),
        isDaytime: _isDaytime,
      ),
      SceneryElement(
        sceneryType: SceneryType.lanternPost,
        depthSlice: ParallaxDepthSlice.frontSlice,
        position: Vector2(70, defaultBaseGroundY),
        size: Vector2(32, 80),
        isDaytime: _isDaytime,
      ),
      SceneryElement(
        sceneryType: SceneryType.lanternPost,
        depthSlice: ParallaxDepthSlice.frontSlice,
        position: Vector2(250, 440),
        size: Vector2(32, 80),
        isDaytime: _isDaytime,
      ),
      SceneryElement(
        sceneryType: SceneryType.lanternPost,
        depthSlice: ParallaxDepthSlice.frontSlice,
        position: Vector2(470, defaultBaseGroundY),
        size: Vector2(32, 80),
        isDaytime: _isDaytime,
      ),
    ];
    for (final prop in sceneryProps) {
      await add(prop);
    }

    // Mount Feudal Foes (patrolling Ashigaru spearman & floating Hitodama)
    final foes = [
      FeudalFoe(
        foeType: FoeType.ashigaru,
        position: Vector2(620, defaultBaseGroundY),
      ),
      FeudalFoe(
        foeType: FoeType.hitodama,
        position: Vector2(490, 310),
      ),
    ];
    for (final foe in foes) {
      await add(foe);
    }

    // Mount collectible sushi, shuriken, magatama, and ofuda items
    final collectibleItems = [
      NinjaItem.shuriken(position: Vector2(250, 370)),
      NinjaItem.sushi(position: Vector2(520, 310)),
      NinjaItem.magatama(position: Vector2(360, 360)),
      NinjaItem.ofuda(position: Vector2(660, 360)),
      NinjaItem.shuriken(position: Vector2(810, 360)),
    ];
    for (final item in collectibleItems) {
      await add(item);
    }

    const initialGroundY = defaultBaseGroundY - (64 - 2);
    ninjaPlayer = _initialNinjaPlayer ??
        NinjaPlayer(
          position: Vector2(100, initialGroundY),
          groundY: initialGroundY,
          floorBaselineY: initialGroundY,
        );

    await add(ninjaPlayer);
  }

  /// Called when the player collects a [NinjaItem].
  void onItemCollected(NinjaItem item) {
    final sfxToPlay = switch (item.type) {
      ItemType.shuriken || ItemType.ofuda => Sfx.shurikenPickup,
      ItemType.sushi ||
      ItemType.magatama ||
      ItemType.goldenFeather =>
        Sfx.sushiPickup,
    };
    audioController?.playSfx(sfxToPlay);

    gameBloc?.add(GameScoreIncreased(by: item.type.points));

    final effect = itemEffectFactory?.call(item.type, item.position.clone()) ??
        ItemEffect(
          type: item.type,
          position: item.position.clone(),
        );
    add(effect);
  }

  /// Triggers a katana slash on the active ninja player.
  void attack() {
    if (ninjaPlayer.isMounted) {
      ninjaPlayer.katanaSlash();
    }
  }

  /// Throws a shuriken projectile from the active ninja player.
  void throwShuriken() {
    if (ninjaPlayer.isMounted) {
      ninjaPlayer.throwShuriken();
    }
  }

  @override
  void onTapDown(TapDownInfo info) {
    super.onTapDown(info);
    if (ninjaPlayer.isMounted) {
      ninjaPlayer.jump();
    }
  }

  @override
  KeyEventResult onKeyEvent(
    KeyEvent event,
    Set<LogicalKeyboardKey> keysPressed,
  ) {
    if (event is KeyDownEvent) {
      if (event.logicalKey == LogicalKeyboardKey.space ||
          event.logicalKey == LogicalKeyboardKey.arrowUp ||
          event.logicalKey == LogicalKeyboardKey.keyW) {
        if (ninjaPlayer.isMounted) {
          ninjaPlayer.jump();
        }
        return KeyEventResult.handled;
      }
      if (event.logicalKey == LogicalKeyboardKey.keyX ||
          event.logicalKey == LogicalKeyboardKey.keyJ) {
        if (ninjaPlayer.isMounted) {
          ninjaPlayer.katanaSlash();
        }
        return KeyEventResult.handled;
      }
      if (event.logicalKey == LogicalKeyboardKey.keyC ||
          event.logicalKey == LogicalKeyboardKey.keyK) {
        if (ninjaPlayer.isMounted) {
          ninjaPlayer.throwShuriken();
        }
        return KeyEventResult.handled;
      }
    }
    return super.onKeyEvent(event, keysPressed);
  }
}
