import 'package:flame/components.dart';
import 'package:super_dash/game/components/parallax_background.dart';

/// The conceptual depth slices as defined in the image_29 pipeline (Panel 3).
enum ParallaxDepthSlice {
  /// Back slice: Moonlight Sky / Distant Mountains (0.0x velocity multiplier).
  backSlice,

  /// Mid-back slice: Distant Pagodas / Pagoda Groupings (0.25x velocity).
  midBackSlice,

  /// Mid slice: Lantern Posts / Bamboo Forest elements (0.5x velocity).
  midSlice,

  /// Mid-front slice: Wooden Bridge / Main Path / Rocks (0.75x velocity).
  midFrontSlice,

  /// Front slice: Foreground Pond / River (1.0x velocity multiplier).
  frontSlice,
}

/// A formal configuration structure for a parallax depth layer in
/// Shinobi Sprint.
///
/// Encapsulates depth perception rules, environmental asset mappings, and
/// horizontal velocity multipliers based on the image_29 conceptual diagram
/// (Panel 3).
class ParallaxLayerInfo {
  /// Creates a [ParallaxLayerInfo] configuration.
  const ParallaxLayerInfo({
    required this.slice,
    required this.name,
    required this.mapping,
    required this.depthCategory,
    required this.velocityMultiplier,
    this.dayAsset,
    this.nightAsset,
  });

  /// The conceptual depth slice identifier.
  final ParallaxDepthSlice slice;

  /// The formal layer slice name (e.g., 'BACK SLICE', 'MID-BACK SLICE').
  final String name;

  /// Visual and environmental mapping according to the reference diagram.
  final String mapping;

  /// The depth categorization (e.g., 'Infinite/Stationary', 'Slow',
  /// 'Moderate', 'Medium', 'Player Relative').
  final String depthCategory;

  /// The horizontal layer velocity multiplier relative to base speed.
  final double velocityMultiplier;

  /// Relative asset path for daytime theme.
  final String? dayAsset;

  /// Relative asset path for nighttime theme.
  final String? nightAsset;

  /// Returns a Flame-compatible 2D velocity multiplier vector.
  Vector2 get velocityMultiplierVector => Vector2(velocityMultiplier, 0);

  /// Resolves the asset filename depending on whether [isDaytime] is active.
  String getAsset({required bool isDaytime}) {
    if (isDaytime) {
      return dayAsset ?? nightAsset ?? '';
    }
    return nightAsset ?? dayAsset ?? '';
  }
}

/// The architectural depth and speed configuration for Shinobi Sprint.
///
/// Adheres strictly to the image_29 pipeline hierarchy:
/// - BACK SLICE: (Map: Moonlight Sky/Distant Mountains) -> Stationary (0.0x)
/// - MID-BACK SLICE: (Map: Distant Pagodas/Pagoda Groupings) -> Slow (0.25x)
/// - MID SLICE: (Map: Lantern Posts/Bamboo Forest elements) -> Moderate (0.5x)
/// - MID-FRONT SLICE: (Map: Wooden Bridge/Main Path/Rocks) -> Medium (0.75x)
/// - FRONT SLICE: (Map: Foreground Pond/River) -> Player Relative (1.0x)
class ParallaxDepthConfig {
  /// The integrated day wide asset (concept 1, derived from image_27.png).
  static const String dayWideAsset = 'backgrounds/wide_day_strip.png';

  /// The integrated night wide asset (concept 2, image_28.png).
  static const String nightWideAsset = 'backgrounds/wide_night_strip.png';

  /// Raw concept 1 day reference asset.
  static const String concept1DayAsset = 'backgrounds/concept_1_day.png';

  /// Raw concept 2 night reference asset.
  static const String concept2NightAsset = 'backgrounds/concept_2_night.png';

  /// BACK SLICE: Moonlight Sky / Distant Mountains (0.0x velocity multiplier).
  static const ParallaxLayerInfo backSlice = ParallaxLayerInfo(
    slice: ParallaxDepthSlice.backSlice,
    name: 'BACK SLICE',
    mapping: 'Moonlight Sky/Distant Mountains',
    depthCategory: 'Infinite/Stationary',
    velocityMultiplier: 0,
    dayAsset: 'backgrounds/day_farthest_sky.png',
    nightAsset: 'backgrounds/farthest_sky.png',
  );

  /// MID-BACK SLICE: Distant Pagodas / Pagoda Groupings (0.25x velocity).
  static const ParallaxLayerInfo midBackSlice = ParallaxLayerInfo(
    slice: ParallaxDepthSlice.midBackSlice,
    name: 'MID-BACK SLICE',
    mapping: 'Distant Pagodas/Pagoda Groupings',
    depthCategory: 'Slow',
    velocityMultiplier: 0.25,
    dayAsset: 'backgrounds/day_deep_background.png',
    nightAsset: 'backgrounds/deep_background.png',
  );

  /// MID SLICE: Lantern Posts / Bamboo Forest elements (0.5x velocity).
  static const ParallaxLayerInfo midSlice = ParallaxLayerInfo(
    slice: ParallaxDepthSlice.midSlice,
    name: 'MID SLICE',
    mapping: 'Lantern Posts/Bamboo Forest elements',
    depthCategory: 'Moderate',
    velocityMultiplier: 0.5,
    dayAsset: 'backgrounds/day_mid_background.png',
    nightAsset: 'backgrounds/mid_background.png',
  );

  /// MID-FRONT SLICE: Wooden Bridge / Main Path / Rocks (0.75x velocity).
  static const ParallaxLayerInfo midFrontSlice = ParallaxLayerInfo(
    slice: ParallaxDepthSlice.midFrontSlice,
    name: 'MID-FRONT SLICE',
    mapping: 'Wooden Bridge/Main Path/Rocks',
    depthCategory: 'Medium',
    velocityMultiplier: 0.75,
    dayAsset: 'backgrounds/day_midground_lamps.png',
    nightAsset: 'backgrounds/midground_lamps.png',
  );

  /// FRONT SLICE: Foreground Pond / River (1.0x velocity multiplier).
  static const ParallaxLayerInfo frontSlice = ParallaxLayerInfo(
    slice: ParallaxDepthSlice.frontSlice,
    name: 'FRONT SLICE',
    mapping: 'Foreground Pond/River',
    depthCategory: 'Player Relative',
    velocityMultiplier: 1,
    dayAsset: 'backgrounds/day_foreground_path.png',
    nightAsset: 'backgrounds/foreground_path.png',
  );

  /// The complete 5-layer depth hierarchy in descending distance order
  /// (back to front).
  static const List<ParallaxLayerInfo> layers = [
    backSlice,
    midBackSlice,
    midSlice,
    midFrontSlice,
    frontSlice,
  ];

  /// Returns the active integrated wide asset filename for [isDaytime].
  static String getIntegratedWideAsset({required bool isDaytime}) =>
      isDaytime ? dayWideAsset : nightWideAsset;

  /// Returns the active integrated wide asset filename for [isDaytime].
  static String getIntegratedAsset({required bool isDaytime}) =>
      getIntegratedWideAsset(isDaytime: isDaytime);

  /// Converts the depth hierarchy into Flame [ParallaxLayerConfig]s for
  /// [isDaytime], preserving constant velocity multiplier rules across themes.
  static List<ParallaxLayerConfig> toLayerConfigs({required bool isDaytime}) {
    return layers.map((layer) {
      return ParallaxLayerConfig(
        fileName: layer.getAsset(isDaytime: isDaytime),
        velocityMultiplier: layer.velocityMultiplierVector,
      );
    }).toList();
  }
}
