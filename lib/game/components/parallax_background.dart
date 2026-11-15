import 'dart:async';

import 'package:flame/cache.dart';
import 'package:flame/components.dart';
import 'package:flame/flame.dart';
import 'package:flame/game.dart';
import 'package:flame/parallax.dart';
import 'package:flutter/widgets.dart';

/// Configuration for an individual layer in [ParallaxBackground].
class ParallaxLayerConfig {
  /// Creates a configuration for a parallax layer.
  const ParallaxLayerConfig({
    required this.fileName,
    required this.velocityMultiplier,
    this.repeat = ImageRepeat.repeatX,
    this.alignment = Alignment.bottomLeft,
    this.fill = LayerFill.height,
  });

  /// The asset image path (relative to Flame's images prefix).
  final String fileName;

  /// Ascending velocity multiplier for depth perception.
  final Vector2 velocityMultiplier;

  /// How the image is repeated across the screen.
  final ImageRepeat repeat;

  /// Alignment of the image within the viewport.
  final Alignment alignment;

  /// How the image fills the screen.
  final LayerFill fill;
}

/// A deep, multi-layered parallax background component for Shinobi Sprint
/// utilizing Flame's [ParallaxComponent].
///
/// Features 5 distinct layers:
/// 1. Farthest Sky/Moon (0.1x velocity)
/// 2. Deep Background Castle (0.25x velocity)
/// 3. Mid Background Trees/Gates (0.5x velocity)
/// 4. Midground Lamps (0.75x velocity)
/// 5. Foreground Path (1.0x velocity)
class ParallaxBackground<T extends FlameGame> extends ParallaxComponent<T> {
  /// Creates a [ParallaxBackground] with ascending depth multipliers.
  ParallaxBackground({
    super.parallax,
    Vector2? baseVelocity,
    double speed = 100.0,
    List<ParallaxLayerConfig>? layerConfigs,
    bool isDaytime = false,
    bool useThreeLayerDepth = false,
    Images? images,
    super.priority = -1,
    super.position,
    super.size,
    super.scale,
    super.angle,
    super.anchor,
    super.key,
  })  : _isDaytime = isDaytime,
        _useThreeLayerDepth = useThreeLayerDepth,
        _baseVelocity = baseVelocity ?? Vector2(speed, 0),
        _customLayerConfigs = layerConfigs,
        _customImages = images;

  final Images? _customImages;

  Images get _effectiveImages =>
      _customImages ??
      (game.images.prefix == 'assets/images/' ? game.images : Flame.images);

  /// The 5 core background layer image asset filenames for night theme.
  static const List<String> layerAssetNames = [
    'backgrounds/farthest_sky.png',
    'backgrounds/deep_background.png',
    'backgrounds/mid_background.png',
    'backgrounds/midground_lamps.png',
    'backgrounds/foreground_path.png',
  ];

  /// The 5 core day background layer image asset filenames.
  static const List<String> dayLayerAssetNames = [
    'backgrounds/day_farthest_sky.png',
    'backgrounds/day_deep_background.png',
    'backgrounds/day_mid_background.png',
    'backgrounds/day_midground_lamps.png',
    'backgrounds/day_foreground_path.png',
  ];

  /// Legacy layer asset names for backwards compatibility.
  static const List<String> legacyLayerAssetNames = [
    'parallax/parallax_layer1_sky_moon.png',
    'parallax/parallax_layer2_castle.png',
    'parallax/parallax_layer3_trees_gates.png',
    'parallax/parallax_layer4_lamps.png',
    'parallax/parallax_layer5_path.png',
  ];

  /// Default 5 core layers with ascending baseVelocity multipliers,
  /// ensuring the moon remains static (0.0x) while foreground path moves 1.0x.
  static final List<ParallaxLayerConfig> defaultLayers = [
    ParallaxLayerConfig(
      fileName: 'backgrounds/farthest_sky.png',
      velocityMultiplier: Vector2(0, 0),
    ),
    ParallaxLayerConfig(
      fileName: 'backgrounds/deep_background.png',
      velocityMultiplier: Vector2(0.25, 0),
    ),
    ParallaxLayerConfig(
      fileName: 'backgrounds/mid_background.png',
      velocityMultiplier: Vector2(0.5, 0),
    ),
    ParallaxLayerConfig(
      fileName: 'backgrounds/midground_lamps.png',
      velocityMultiplier: Vector2(0.75, 0),
    ),
    ParallaxLayerConfig(
      fileName: 'backgrounds/foreground_path.png',
      velocityMultiplier: Vector2(1, 0),
    ),
  ];

  /// Daytime 5-Layer Parallax Depth Hierarchy matching identical velocities.
  static final List<ParallaxLayerConfig> dayLayers = [
    ParallaxLayerConfig(
      fileName: 'backgrounds/day_farthest_sky.png',
      velocityMultiplier: Vector2(0, 0),
    ),
    ParallaxLayerConfig(
      fileName: 'backgrounds/day_deep_background.png',
      velocityMultiplier: Vector2(0.25, 0),
    ),
    ParallaxLayerConfig(
      fileName: 'backgrounds/day_mid_background.png',
      velocityMultiplier: Vector2(0.5, 0),
    ),
    ParallaxLayerConfig(
      fileName: 'backgrounds/day_midground_lamps.png',
      velocityMultiplier: Vector2(0.75, 0),
    ),
    ParallaxLayerConfig(
      fileName: 'backgrounds/day_foreground_path.png',
      velocityMultiplier: Vector2(1, 0),
    ),
  ];

  /// Calibrated 3-Layer Parallax Depth Hierarchy for night theme:
  /// - LAYER 3 (Far - 0.0x): Moon & Stars (100% Opacity)
  /// - LAYER 2 (Mid - 0.25x): Pagoda & Distant Mountains (40% Opacity + Fog)
  /// - LAYER 1 (Near - 0.50x): Bamboo Trees (70% Opacity, behind platforms)
  static final List<ParallaxLayerConfig> threeLayerHierarchy = [
    ParallaxLayerConfig(
      fileName: 'backgrounds/farthest_sky.png',
      velocityMultiplier: Vector2(0, 0),
    ),
    ParallaxLayerConfig(
      fileName: 'backgrounds/deep_background.png',
      velocityMultiplier: Vector2(0.25, 0),
    ),
    ParallaxLayerConfig(
      fileName: 'backgrounds/mid_background.png',
      velocityMultiplier: Vector2(0.5, 0),
    ),
  ];

  /// Daytime 3-Layer Parallax Depth Hierarchy matching identical
  /// velocity ratios.
  static final List<ParallaxLayerConfig> threeLayerDayHierarchy = [
    ParallaxLayerConfig(
      fileName: 'backgrounds/day_farthest_sky.png',
      velocityMultiplier: Vector2(0, 0),
    ),
    ParallaxLayerConfig(
      fileName: 'backgrounds/day_deep_background.png',
      velocityMultiplier: Vector2(0.25, 0),
    ),
    ParallaxLayerConfig(
      fileName: 'backgrounds/day_mid_background.png',
      velocityMultiplier: Vector2(0.5, 0),
    ),
  ];

  bool _isDaytime;
  final bool _useThreeLayerDepth;
  final Vector2 _baseVelocity;
  final List<ParallaxLayerConfig>? _customLayerConfigs;

  /// Whether daytime mode is active.
  bool get isDaytime => _isDaytime;
  set isDaytime(bool value) {
    if (_isDaytime != value) {
      _isDaytime = value;
      if (isMounted) {
        reloadLayers();
      }
    }
  }

  /// Whether the calibrated 3-layer visual depth hierarchy is active.
  bool get useThreeLayerDepth => _useThreeLayerDepth;

  /// Reloads parallax layers according to current theme.
  Future<void> reloadLayers() async {
    final configs = layerConfigs;
    try {
      await _effectiveImages.loadAll(configs.map((c) => c.fileName).toList());
      final layers = await Future.wait(
        configs.map((config) async {
          return ParallaxLayer.load(
            ParallaxImageData(config.fileName),
            velocityMultiplier: config.velocityMultiplier,
            repeat: config.repeat,
            alignment: config.alignment,
            fill: config.fill,
            images: _effectiveImages,
          );
        }),
      );
      parallax = Parallax(
        layers,
        baseVelocity: _baseVelocity,
      );
    } catch (_) {
      // In headless test environments.
    }
  }

  /// The active base velocity for the background parallax layers.
  Vector2 get baseVelocity => parallax?.baseVelocity ?? _baseVelocity;
  set baseVelocity(Vector2 velocity) {
    _baseVelocity.setFrom(velocity);
    parallax?.baseVelocity.setFrom(velocity);
  }

  /// The list of active layer configurations.
  List<ParallaxLayerConfig> get layerConfigs {
    final custom = _customLayerConfigs;
    if (custom != null) return custom;
    if (_useThreeLayerDepth) {
      return _isDaytime ? threeLayerDayHierarchy : threeLayerHierarchy;
    }
    return _isDaytime ? dayLayers : defaultLayers;
  }

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    if (parallax == null) {
      final configs = layerConfigs;

      // Pre-load all required image assets asynchronously inside onLoad
      // to prevent one-time execution rendering delays or mid-game frame
      // stuttering.
      final imagePaths = configs.map((c) => c.fileName).toList();
      try {
        await _effectiveImages.loadAll(imagePaths);
      } catch (_) {
        // Fallback if running inside headless test environment without assets.
      }

      // Map each image to a specific layer and assign ascending baseVelocity.
      final layers = await Future.wait(
        configs.map((config) async {
          return ParallaxLayer.load(
            ParallaxImageData(config.fileName),
            velocityMultiplier: config.velocityMultiplier,
            repeat: config.repeat,
            alignment: config.alignment,
            fill: config.fill,
            images: _effectiveImages,
          );
        }),
      );

      parallax = Parallax(
        layers,
        baseVelocity: _baseVelocity,
      );
    }
  }
}
