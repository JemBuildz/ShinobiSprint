import 'dart:async';

import 'package:flame/components.dart';
import 'package:super_dash/game/components/lantern_glow.dart';
import 'package:super_dash/game/config/parallax_depth.dart';

/// Available scenery types extracted from the concept art cutouts.
enum SceneryType {
  /// Grand wooden Torii Gate.
  toriiGate,

  /// Multi-tier Japanese pagoda shrine.
  pagoda,

  /// Traditional Japanese shrine house / village building.
  shrineHouse,

  /// Dense cluster of bamboo stalks.
  bambooCluster,

  /// Stone / timber lantern post.
  lanternPost,

  /// Elevated wooden boardwalk platform.
  boardwalkPlatform,

  /// Arched traditional wooden bridge (Taiko-bashi).
  archedBridge,

  /// Covered stone water well with gable roof.
  stoneWell,

  /// Flowering pink cherry blossom tree (Sakura).
  sakuraTree,

  /// Weeping willow tree.
  willowTree,

  /// Traditional tea ceremony table with teapot.
  teaTable,

  /// Katana and spear weapon rack.
  weaponRack,

  /// Protective roadside Jizo stone statue.
  jizoStatue,

  /// Guardian stone lion-dog (Komainu).
  komainuStatue,

  /// Village street market stall.
  marketStall,

  /// Temple belfry / bell tower (Shoro).
  bellTower,

  /// Wooden outpost watchtower.
  watchtower,

  /// Small roadside shrine (Hokora).
  roadsideShrine,

  /// Cluster of mossy boulders and river rocks.
  mossyRocks,
}

/// A scenery prop anchored in the Shinobi Sprint parallax world.
///
/// Moves horizontally according to the velocity multiplier of its assigned
/// depth layer slice.
class SceneryElement extends SpriteComponent with HasGameReference {
  /// Creates a [SceneryElement].
  SceneryElement({
    required this.sceneryType,
    required this.depthSlice,
    super.position,
    Vector2? size,
    super.anchor = Anchor.bottomLeft,
    int? priority,
    double baseSpeed = 100.0,
    bool isDaytime = false,
  })  : _baseSpeed = baseSpeed,
        _isDaytime = isDaytime,
        super(
          size: size ?? _defaultSizeFor(sceneryType),
          priority: priority ?? _defaultPriorityFor(sceneryType, depthSlice),
        );

  /// The visual type of this scenery prop.
  final SceneryType sceneryType;

  /// The depth slice this prop belongs to, determining its velocity multiplier.
  final ParallaxDepthSlice depthSlice;

  final double _baseSpeed;
  bool _isDaytime;
  LanternGlowComponent? _lanternGlow;

  /// The active attached lantern glow effect, if this element is a
  /// lantern post.
  LanternGlowComponent? get lanternGlow => _lanternGlow;

  /// Whether daytime mode is active for this scenery element.
  bool get isDaytime => _isDaytime;
  set isDaytime(bool value) {
    if (_isDaytime != value) {
      _isDaytime = value;
      _lanternGlow?.isDaytime = value;
      if (isMounted) {
        _updateSprite();
      }
    }
  }

  /// Calculates the velocity multiplier for this element based on depthSlice.
  double get velocityMultiplier {
    switch (depthSlice) {
      case ParallaxDepthSlice.backSlice:
        return 0;
      case ParallaxDepthSlice.midBackSlice:
        return 0.25;
      case ParallaxDepthSlice.midSlice:
        return 0.5;
      case ParallaxDepthSlice.midFrontSlice:
        return 0.75;
      case ParallaxDepthSlice.frontSlice:
        return 1;
    }
  }

  /// The horizontal scroll speed of this element in pixels/second.
  double get scrollSpeed => _baseSpeed * velocityMultiplier;

  static Vector2 _defaultSizeFor(SceneryType type) {
    switch (type) {
      case SceneryType.toriiGate:
        return Vector2(120, 140);
      case SceneryType.pagoda:
        return Vector2(130, 160);
      case SceneryType.shrineHouse:
        return Vector2(140, 120);
      case SceneryType.bambooCluster:
        return Vector2(80, 150);
      case SceneryType.lanternPost:
        return Vector2(36, 72);
      case SceneryType.boardwalkPlatform:
        return Vector2(160, 48);
      case SceneryType.archedBridge:
        return Vector2(140, 60);
      case SceneryType.stoneWell:
        return Vector2(60, 80);
      case SceneryType.sakuraTree:
        return Vector2(90, 105);
      case SceneryType.willowTree:
        return Vector2(85, 100);
      case SceneryType.teaTable:
        return Vector2(75, 55);
      case SceneryType.weaponRack:
        return Vector2(80, 70);
      case SceneryType.jizoStatue:
        return Vector2(35, 75);
      case SceneryType.komainuStatue:
        return Vector2(50, 65);
      case SceneryType.marketStall:
        return Vector2(90, 70);
      case SceneryType.bellTower:
        return Vector2(70, 65);
      case SceneryType.watchtower:
        return Vector2(65, 100);
      case SceneryType.roadsideShrine:
        return Vector2(55, 75);
      case SceneryType.mossyRocks:
        return Vector2(100, 70);
    }
  }

  static int _defaultPriorityFor(SceneryType type, ParallaxDepthSlice slice) {
    if (type == SceneryType.boardwalkPlatform) return 1;
    // Landmark decorations (Torii gate, Pagoda, Shrine, Bamboo) render
    // strictly in the background behind playable platforms (priority 1) and
    // the player (priority 2), preventing any clipping or visual overlap.
    if (type == SceneryType.toriiGate) return -2;
    switch (slice) {
      case ParallaxDepthSlice.backSlice:
        return -3;
      case ParallaxDepthSlice.midBackSlice:
        return -2;
      case ParallaxDepthSlice.midSlice:
      case ParallaxDepthSlice.midFrontSlice:
      case ParallaxDepthSlice.frontSlice:
        return -1;
    }
  }

  /// Returns the relative image path for this element.
  String get assetPath {
    switch (sceneryType) {
      case SceneryType.toriiGate:
        return 'cutouts/torii_gate.png';
      case SceneryType.pagoda:
        return 'cutouts/pagoda_shrine_grounded.png';
      case SceneryType.shrineHouse:
        return 'cutouts/japanese_shrine_house.png';
      case SceneryType.bambooCluster:
        return 'cutouts/bamboo_cluster.png';
      case SceneryType.lanternPost:
        return _isDaytime
            ? 'cutouts/lantern_post_clean.png'
            : 'cutouts/lantern_post_glowing.png';
      case SceneryType.boardwalkPlatform:
        return 'cutouts/wooden_boardwalk_platform.png';
      case SceneryType.archedBridge:
        return 'cutouts/arched_bridge.png';
      case SceneryType.stoneWell:
        return 'cutouts/stone_well.png';
      case SceneryType.sakuraTree:
        return 'cutouts/sakura_tree_1.png';
      case SceneryType.willowTree:
        return 'cutouts/willow_tree.png';
      case SceneryType.teaTable:
        return 'cutouts/tea_table.png';
      case SceneryType.weaponRack:
        return 'cutouts/weapon_rack.png';
      case SceneryType.jizoStatue:
        return 'cutouts/jizo_statue.png';
      case SceneryType.komainuStatue:
        return 'cutouts/komainu_statue.png';
      case SceneryType.marketStall:
        return 'cutouts/market_stall.png';
      case SceneryType.bellTower:
        return 'cutouts/bell_tower.png';
      case SceneryType.watchtower:
        return 'cutouts/watchtower.png';
      case SceneryType.roadsideShrine:
        return 'cutouts/roadside_shrine.png';
      case SceneryType.mossyRocks:
        return 'cutouts/mossy_rocks_1.png';
    }
  }

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    await _updateSprite();

    if (sceneryType == SceneryType.lanternPost) {
      _lanternGlow = LanternGlowComponent(
        position: Vector2(size.x / 2, size.y * 0.35),
        isDaytime: _isDaytime,
      );
      await add(_lanternGlow!);
    }
  }

  Future<void> _updateSprite() async {
    try {
      sprite = await game.loadSprite(assetPath);
    } catch (_) {
      // In headless test environments
    }
  }

  @override
  void update(double dt) {
    super.update(dt);
    // Scroll element leftwards according to its depth slice multiplier
    position.x -= scrollSpeed * dt;
  }
}
