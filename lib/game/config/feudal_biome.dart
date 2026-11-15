import 'package:super_dash/game/components/feudal_foe.dart';
import 'package:super_dash/game/components/scenery_element.dart';

/// The 8 distinct Feudal Biome Themes extracted from the master environment
/// sheets.
enum FeudalBiome {
  /// Dense vertical bamboo stalks with dappled golden sun or moonlit lanterns.
  bambooGrove(
    title: 'Bamboo Grove',
    assetPrefix: 'bamboo_grove',
    scenery: [
      SceneryType.bambooCluster,
      SceneryType.lanternPost,
      SceneryType.stoneWell,
    ],
    foes: [FoeType.ronin, FoeType.karakasa, FoeType.hitodama],
  ),

  /// Craggy alpine cliffs and highland shrines.
  mountainPass(
    title: 'Mountain Pass',
    assetPrefix: 'mountain_pass',
    scenery: [
      SceneryType.pagoda,
      SceneryType.mossyRocks,
      SceneryType.jizoStatue,
    ],
    foes: [FoeType.tengu, FoeType.archer, FoeType.oni],
  ),

  /// Shaded pine and cedar woodland trail with roadside Jizo statues.
  forestRoad(
    title: 'Forest Road',
    assetPrefix: 'forest_road',
    scenery: [
      SceneryType.jizoStatue,
      SceneryType.sakuraTree,
      SceneryType.roadsideShrine,
    ],
    foes: [FoeType.ashigaru, FoeType.tsuchigumo, FoeType.ronin],
  ),

  /// Sacred path lined with vermilion Torii gates.
  toriiGateTrail(
    title: 'Torii Gate Trail',
    assetPrefix: 'torii_gate',
    scenery: [
      SceneryType.toriiGate,
      SceneryType.lanternPost,
      SceneryType.komainuStatue,
    ],
    foes: [FoeType.ashigaru, FoeType.oni, FoeType.brokenLantern],
  ),

  /// Rushing mountain river crossed by an arched wooden bridge (Taiko-bashi).
  riverCrossing(
    title: 'River Crossing',
    assetPrefix: 'river_crossing',
    scenery: [
      SceneryType.archedBridge,
      SceneryType.willowTree,
      SceneryType.mossyRocks,
    ],
    foes: [FoeType.karakasa, FoeType.hitodama, FoeType.cursedWell],
  ),

  /// Traditional village market street with timber shops and lanterns.
  villageStreet(
    title: 'Village Street',
    assetPrefix: 'village_street',
    scenery: [
      SceneryType.shrineHouse,
      SceneryType.marketStall,
      SceneryType.teaTable,
      SceneryType.bellTower,
    ],
    foes: [FoeType.sumo, FoeType.ronin, FoeType.ashigaru],
  ),

  /// Seaside fishing port with moored sampans and wooden piers.
  shorelineHarbor(
    title: 'Shoreline & Harbor',
    assetPrefix: 'shoreline_harbor',
    scenery: [
      SceneryType.watchtower,
      SceneryType.boardwalkPlatform,
      SceneryType.stoneWell,
    ],
    foes: [FoeType.archer, FoeType.sumo, FoeType.oni],
  ),

  /// Subterranean cavern entrance with glowing crystals and rocky arches.
  caveEntrance(
    title: 'Cave Entrance',
    assetPrefix: 'cave_entrance',
    scenery: [
      SceneryType.mossyRocks,
      SceneryType.weaponRack,
      SceneryType.stoneWell,
    ],
    foes: [FoeType.tsuchigumo, FoeType.cursedWell, FoeType.ancestralKatana],
  );

  const FeudalBiome({
    required this.title,
    required this.assetPrefix,
    required this.scenery,
    required this.foes,
  });

  /// User-facing biome title.
  final String title;

  /// Filename prefix in `assets/images/panoramic_biomes/`.
  final String assetPrefix;

  /// Representative scenery element types for this environment.
  final List<SceneryType> scenery;

  /// Representative foes / obstacles inhabiting this biome.
  final List<FoeType> foes;

  /// Relative path to daytime panoramic strip.
  String get dayAsset => 'panoramic_biomes/${assetPrefix}_day.png';

  /// Relative path to nighttime panoramic strip.
  String get nightAsset => 'panoramic_biomes/${assetPrefix}_night.png';

  /// Resolves the asset based on daytime/nighttime state.
  String getAsset({required bool isDaytime}) =>
      isDaytime ? dayAsset : nightAsset;
}
