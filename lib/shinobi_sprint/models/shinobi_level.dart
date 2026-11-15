import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:super_dash/bamboo_village/autumn_maple_game.dart';
import 'package:super_dash/bamboo_village/main_game.dart';
import 'package:super_dash/bamboo_village/twilight_game.dart';

/// Represents the three overarching Acts/Worlds in Shinobi Sprint.
enum ShinobiWorld {
  /// World 1: Fresh morning sunlight in the Bamboo Village.
  dawnVillage(
    worldId: 1,
    title: 'Act I: Dawn Village',
    locationName: 'Bamboo Village',
    timeOfDay: 'Morning Dawn',
    themeColor: Color(0xFF10B981),
    accentColor: Color(0xFF34D399),
    icon: Icons.wb_sunny,
    assetPlate: 'stage1_torii_shrine_1024.png',
    description:
        'Master the fundamentals: leaping over chasms, rooftop drop-throughs, '
        'rapid time trials, and combat against bridge patrols.',
  ),

  /// World 2: Golden sunset at the Sacred Torii Shrine.
  twilightSanctuary(
    worldId: 2,
    title: 'Act II: Twilight Sanctuary',
    locationName: 'Twilight Sanctuary',
    timeOfDay: 'Golden Sunset',
    themeColor: Color(0xFFF59E0B),
    accentColor: Color(0xFFFBBF24),
    icon: Icons.wb_twilight,
    assetPlate: 'level2_cinematic_stage_1024.png',
    description:
        'High-elevation peril: sagging rope bridges, treacherous punji spikes, '
        'watchtower ascents, and high-stakes canyon crossings.',
  ),

  /// World 3: Midnight moon in the Autumn Maple Forest.
  midnightAutumn(
    worldId: 3,
    title: 'Act III: Midnight Autumn',
    locationName: 'Autumn Maple Forest',
    timeOfDay: 'Midnight Moon',
    themeColor: Color(0xFFE11D48),
    accentColor: Color(0xFFFB7185),
    icon: Icons.nights_stay,
    assetPlate: 'level3_cinematic_stage_1024.png',
    description:
        'The ultimate ninja trials: spinning shuriken hazards, narrow river '
        'bridge sprints under the crescent moon, and the final shrine trial.',
  );

  const ShinobiWorld({
    required this.worldId,
    required this.title,
    required this.locationName,
    required this.timeOfDay,
    required this.themeColor,
    required this.accentColor,
    required this.icon,
    required this.assetPlate,
    required this.description,
  });

  final int worldId;
  final String title;
  final String locationName;
  final String timeOfDay;
  final Color themeColor;
  final Color accentColor;
  final IconData icon;
  final String assetPlate;
  final String description;

  /// Returns the 5 levels corresponding to this world.
  List<ShinobiLevel> get levels =>
      ShinobiCampaign.allLevels.where((l) => l.world == this).toList();
}

/// Represents an individual handcrafted level in the campaign.
class ShinobiLevel {
  const ShinobiLevel({
    required this.id,
    required this.world,
    required this.levelNumber,
    required this.title,
    required this.subtitle,
    required this.description,
    required this.orbPositions,
    required this.star1Objective,
    required this.star2Objective,
    required this.star3Objective,
    this.timeLimit,
    this.hasSpikes = false,
    this.spikePositions = const [],
    this.hasShurikens = false,
    this.shurikenPositions = const [],
    this.hasFoes = false,
    this.foesPositions = const [],
  });

  /// Unique alphanumeric level identifier (e.g., '1-1', '2-3', '3-5').
  final String id;

  /// The parent world.
  final ShinobiWorld world;

  /// The level index within the world (1 to 5).
  final int levelNumber;

  /// Full level display name.
  final String title;

  /// Short tactical category (e.g. 'Tutorial', 'Time Trial', 'Elevation').
  final String subtitle;

  /// Gameplay briefing.
  final String description;

  /// Precise coordinates where spirit orbs spawn.
  final List<Vector2> orbPositions;

  /// Star 1 requirement (typically basic completion).
  final String star1Objective;

  /// Star 2 requirement (all collectibles or enemies).
  final String star2Objective;

  /// Star 3 requirement (time trial or zero damage).
  final String star3Objective;

  /// Optional countdown timer in seconds.
  final int? timeLimit;

  /// Whether deadly spikes are active.
  final bool hasSpikes;
  final List<Vector2> spikePositions;

  /// Whether spinning shuriken hazards are active.
  final bool hasShurikens;
  final List<Vector2> shurikenPositions;

  /// Whether enemy foes are patrolling.
  final bool hasFoes;
  final List<Vector2> foesPositions;

  /// Total number of spirit orbs required.
  int get totalOrbs => orbPositions.length;

  /// Whether this level has an active countdown timer.
  bool get isTimeTrial => timeLimit != null;

  /// Formatted stage tag e.g. "LEVEL 1-3".
  String get tag => 'LEVEL $id';

  /// Builds the corresponding [FlameGame] configured for this level.
  FlameGame buildGame({
    void Function(int orbs)? onOrbsChanged,
    VoidCallback? onHazardHit,
  }) {
    switch (world) {
      case ShinobiWorld.dawnVillage:
        return MainGame(
          onOrbsChanged: onOrbsChanged,
          onHazardHit: onHazardHit,
          customOrbPositions: orbPositions,
          customFoePositions: foesPositions,
        );
      case ShinobiWorld.twilightSanctuary:
        return TwilightSanctuaryGame(
          onOrbsChanged: onOrbsChanged,
          onHazardHit: onHazardHit,
          customOrbPositions: orbPositions,
          customFoePositions: foesPositions,
        );
      case ShinobiWorld.midnightAutumn:
        return AutumnMapleGame(
          onOrbsChanged: onOrbsChanged,
          onHazardHit: onHazardHit,
          customOrbPositions: orbPositions,
          customFoePositions: foesPositions,
        );
    }
  }

  /// Returns the next sequential level in the 15-level campaign.
  ShinobiLevel? get nextLevel {
    final idx = ShinobiCampaign.allLevels.indexWhere((l) => l.id == id);
    if (idx >= 0 && idx < ShinobiCampaign.allLevels.length - 1) {
      return ShinobiCampaign.allLevels[idx + 1];
    }
    return null;
  }

  /// Whether this is the final campaign finale level (3-5).
  bool get isFinalLevel => nextLevel == null;
}

/// Definitive 15-level campaign catalog for Shinobi Sprint across 3 Acts.
class ShinobiCampaign {
  // ---------------------------------------------------------------------------
  // WORLD 1: DAWN VILLAGE (Levels 1-1 to 1-5)
  // ---------------------------------------------------------------------------

  /// Level 1-1: Tutorial — Collect 3 ground orbs, learn jump.
  static final level1_1 = ShinobiLevel(
    id: '1-1',
    world: ShinobiWorld.dawnVillage,
    levelNumber: 1,
    title: 'Tutorial: Jump Training',
    subtitle: 'Movement & Jump',
    description:
        'Leap across the village path and bridge to collect 3 ground '
        'spirit orbs. Master basic jump momentum.',
    star1Objective: 'Reach the right village bank',
    star2Objective: 'Collect all 3 spirit orbs',
    star3Objective: 'Complete without falling into the chasm',
    orbPositions: [
      Vector2(200, 440),
      Vector2(500, 440),
      Vector2(750, 440),
    ],
  );

  /// Level 1-2: Elevation — 6 orbs on rooftops, learn drop-through (S+Space).
  static final level1_2 = ShinobiLevel(
    id: '1-2',
    world: ShinobiWorld.dawnVillage,
    levelNumber: 2,
    title: 'Elevation: Rooftop Run',
    subtitle: 'Rooftops & Drop-Through',
    description:
        'Scale the wooden shack, leap onto the elevated bamboo platform, and '
        'reach the dojo rooftop. Use S+Space to drop through platforms.',
    star1Objective: 'Collect 4 orbs and clear the stage',
    star2Objective: 'Collect all 6 rooftop orbs',
    star3Objective: 'Drop through both elevated platforms cleanly',
    orbPositions: [
      Vector2(160, 175), // Left shack roof
      Vector2(230, 175), // Left shack ridge
      Vector2(460, 290), // Center elevated bamboo platform
      Vector2(540, 290), // Center elevated bamboo platform
      Vector2(850, 175), // Right dojo roof
      Vector2(930, 175), // Right dojo ridge
    ],
  );

  /// Level 1-3: Time Trial — Collect all 6 orbs under 25 seconds.
  static final level1_3 = ShinobiLevel(
    id: '1-3',
    world: ShinobiWorld.dawnVillage,
    levelNumber: 3,
    title: 'Time Trial: Dawn Sprint',
    subtitle: 'High-Velocity Speedrun',
    description:
        'The sun is rising fast! Dash across both rooftops and the lower '
        'bridge to gather all 6 orbs before the 25-second timer expires.',
    star1Objective: 'Gather 6 orbs before time runs out',
    star2Objective: 'Finish with 5+ seconds remaining',
    star3Objective: 'Finish under 18 seconds',
    timeLimit: 25,
    orbPositions: [
      Vector2(160, 175),
      Vector2(320, 440),
      Vector2(500, 290),
      Vector2(500, 440),
      Vector2(750, 440),
      Vector2(875, 175),
    ],
  );

  /// Level 1-4: Shuriken Target Challenge — 2 ninja foes on lower bridge.
  static final level1_4 = ShinobiLevel(
    id: '1-4',
    world: ShinobiWorld.dawnVillage,
    levelNumber: 4,
    title: 'Bridge Patrol Ambush',
    subtitle: 'Combat & Evasion',
    description:
        'Two Ashigaru guards patrol the chasm bridge and right village '
        'grounds. Evade their spears or strike them with shurikens.',
    star1Objective: 'Collect 4 orbs safely',
    star2Objective: 'Cross the bridge without taking damage',
    star3Objective: 'Complete in under 20 seconds',
    hasFoes: true,
    foesPositions: [
      Vector2(480, 490),
      Vector2(750, 490),
    ],
    orbPositions: [
      Vector2(250, 440),
      Vector2(500, 440),
      Vector2(650, 440),
      Vector2(850, 280),
    ],
  );

  /// Level 1-5 (World 1 Climax): Clean run with 10 orbs and no missed jumps.
  static final level1_5 = ShinobiLevel(
    id: '1-5',
    world: ShinobiWorld.dawnVillage,
    levelNumber: 5,
    title: 'Dawn Village Climax',
    subtitle: 'Act I Master Trial',
    description:
        'The ultimate trial of the Dawn Village. Complete an acrobatic run '
        'collecting all 10 spirit orbs scattered from rooftops to the bridge.',
    star1Objective: 'Collect all 10 spirit orbs',
    star2Objective: 'Flawless run with zero resets',
    star3Objective: 'Complete in under 30 seconds',
    timeLimit: 35,
    orbPositions: [
      Vector2(120, 175),
      Vector2(200, 175),
      Vector2(280, 440),
      Vector2(420, 440),
      Vector2(500, 290),
      Vector2(580, 440),
      Vector2(720, 440),
      Vector2(820, 175),
      Vector2(920, 175),
      Vector2(950, 280),
    ],
  );

  // ---------------------------------------------------------------------------
  // WORLD 2: TWILIGHT SANCTUARY (Levels 2-1 to 2-5)
  // ---------------------------------------------------------------------------

  /// Level 2-1: Sanctuary Gates — Cross rope bridge & dodge spike trap.
  static final level2_1 = ShinobiLevel(
    id: '2-1',
    world: ShinobiWorld.twilightSanctuary,
    levelNumber: 1,
    title: 'Sanctuary Gates',
    subtitle: 'Rope Bridge & Spikes',
    description:
        'Enter the Twilight Sanctuary. Leap over the entrance punji spike trap '
        'and navigate the sagging western rope bridge to gather 4 sacred orbs.',
    star1Objective: 'Cross the western bridge safely',
    star2Objective: 'Collect all 4 spirit orbs',
    star3Objective: 'Zero spike trap damage',
    hasSpikes: true,
    orbPositions: [
      Vector2(200, 370),
      Vector2(330, 395),
      Vector2(500, 375),
      Vector2(850, 370),
    ],
  );

  /// Level 2-2: Watchtower Ascent — Reaching elevated watchtower lookouts.
  static final level2_2 = ShinobiLevel(
    id: '2-2',
    world: ShinobiWorld.twilightSanctuary,
    levelNumber: 2,
    title: 'Watchtower Ascent',
    subtitle: 'Vertical Aerial Leap',
    description:
        'Scale the soaring watchtower lookout beams flanking the Grand Torii '
        'Gate to gather 6 high-altitude soul orbs.',
    star1Objective: 'Collect 4 orbs and reach the eastern ridge',
    star2Objective: 'Collect all 6 elevated orbs',
    star3Objective: 'Reach the highest watchtower roof beam',
    orbPositions: [
      Vector2(260, 210), // Left watchtower mid
      Vector2(270, 155), // Left watchtower top
      Vector2(500, 375), // Center island
      Vector2(760, 210), // Right watchtower mid
      Vector2(770, 155), // Right watchtower top
      Vector2(920, 370), // Eastern ridge
    ],
  );

  /// Level 2-3: Double Chasm Dash — Cross both sagging bridges under 28s.
  static final level2_3 = ShinobiLevel(
    id: '2-3',
    world: ShinobiWorld.twilightSanctuary,
    levelNumber: 3,
    title: 'Double Chasm Dash',
    subtitle: '28-Second Speed Sprint',
    description:
        'Dash across the sagging western and eastern rope bridges under golden '
        'sunset. Collect 6 orbs before the 28-second timer runs out.',
    star1Objective: 'Cross to the eastern gate in time',
    star2Objective: 'Collect all 6 orbs',
    star3Objective: 'Finish under 20 seconds',
    timeLimit: 28,
    orbPositions: [
      Vector2(200, 370),
      Vector2(330, 395),
      Vector2(480, 375),
      Vector2(530, 375),
      Vector2(680, 395),
      Vector2(850, 370),
    ],
  );

  /// Level 2-4: Punji Stake Gauntlet — Multiple traps across the sanctuary.
  static final level2_4 = ShinobiLevel(
    id: '2-4',
    world: ShinobiWorld.twilightSanctuary,
    levelNumber: 4,
    title: 'Punji Stake Gauntlet',
    subtitle: 'Hazard Evasion',
    description:
        'Dangerous ground spike traps line the sanctuary approach. Time your '
        'jumps precisely across the center lantern island to collect 6 orbs.',
    star1Objective: 'Clear the gauntlet alive',
    star2Objective: 'Collect all 6 orbs',
    star3Objective: 'Zero hazard strikes',
    hasSpikes: true,
    hasFoes: true,
    foesPositions: [
      Vector2(500, 375),
    ],
    orbPositions: [
      Vector2(180, 370),
      Vector2(300, 395),
      Vector2(450, 375),
      Vector2(550, 375),
      Vector2(700, 395),
      Vector2(900, 370),
    ],
  );

  /// Level 2-5: Twilight Climax — Full sanctuary mastery.
  static final level2_5 = ShinobiLevel(
    id: '2-5',
    world: ShinobiWorld.twilightSanctuary,
    levelNumber: 5,
    title: 'Twilight Climax',
    subtitle: 'Act II Master Trial',
    description:
        'Master the entire Sacred Sanctuary under the setting sun. Scale both '
        'watchtowers, brave the rope bridges, and gather all 8 sacred orbs.',
    star1Objective: 'Collect all 8 sacred orbs',
    star2Objective: 'Flawless run with zero falls',
    star3Objective: 'Finish in under 26 seconds',
    hasSpikes: true,
    timeLimit: 32,
    orbPositions: [
      Vector2(270, 160),
      Vector2(300, 465),
      Vector2(455, 440),
      Vector2(512, 435),
      Vector2(570, 440),
      Vector2(720, 465),
      Vector2(770, 160),
      Vector2(950, 375),
    ],
  );

  // ---------------------------------------------------------------------------
  // WORLD 3: MIDNIGHT AUTUMN (Levels 3-1 to 3-5)
  // ---------------------------------------------------------------------------

  /// Level 3-1: Midnight Pagoda Arrival.
  static final level3_1 = ShinobiLevel(
    id: '3-1',
    world: ShinobiWorld.midnightAutumn,
    levelNumber: 1,
    title: 'Midnight Pagoda Arrival',
    subtitle: 'Moonlit Approach',
    description:
        'Dash beneath the glowing crescent moon, cross the rocky river canyon '
        'ledges, and gather 4 moonlight orbs before reaching the bridge.',
    star1Objective: 'Reach the arched bridge',
    star2Objective: 'Collect all 4 moonlight orbs',
    star3Objective: 'Finish under 16 seconds',
    orbPositions: [
      Vector2(210, 370),
      Vector2(360, 350),
      Vector2(520, 340),
      Vector2(830, 370),
    ],
  );

  /// Level 3-2: Arched Bridge Traps — Spinning shuriken hazards.
  static final level3_2 = ShinobiLevel(
    id: '3-2',
    world: ShinobiWorld.midnightAutumn,
    levelNumber: 2,
    title: 'Arched Bridge Traps',
    subtitle: 'Shuriken Evasion',
    description:
        'Spinning blades orbit the arched stone river bridge! Time your leaps '
        'to dodge rotating shurikens while collecting 5 soul orbs.',
    star1Objective: 'Cross the bridge safely',
    star2Objective: 'Collect all 5 soul orbs',
    star3Objective: 'Zero shuriken contact',
    hasShurikens: true,
    orbPositions: [
      Vector2(210, 370),
      Vector2(380, 340),
      Vector2(500, 335),
      Vector2(620, 340),
      Vector2(830, 370),
    ],
  );

  /// Level 3-3: Midnight Speed Run — 22-second bridge sprint.
  static final level3_3 = ShinobiLevel(
    id: '3-3',
    world: ShinobiWorld.midnightAutumn,
    levelNumber: 3,
    title: 'Midnight Speed Run',
    subtitle: '22-Second Moon Sprint',
    description:
        'Sprint at full velocity from the western cliffs across the bridge to '
        'the pagoda terrace under 22 seconds with all 6 orbs.',
    star1Objective: 'Reach the pagoda terrace in time',
    star2Objective: 'Collect all 6 orbs',
    star3Objective: 'Finish under 17 seconds',
    timeLimit: 22,
    orbPositions: [
      Vector2(150, 380),
      Vector2(300, 360),
      Vector2(450, 335),
      Vector2(580, 335),
      Vector2(720, 360),
      Vector2(860, 380),
    ],
  );

  /// Level 3-4: Shadow Patrols — River canyon & terrace guards.
  static final level3_4 = ShinobiLevel(
    id: '3-4',
    world: ShinobiWorld.midnightAutumn,
    levelNumber: 4,
    title: 'Shadow Patrols',
    subtitle: 'Stealth & Elimination',
    description:
        'Elite shadow guards watch the pagoda terrace. Slip past or defeat '
        'them with katana slashes while securing 6 nocturnal orbs.',
    star1Objective: 'Clear the terrace safely',
    star2Objective: 'Collect all 6 orbs',
    star3Objective: 'Finish in under 20 seconds',
    hasFoes: true,
    foesPositions: [
      Vector2(500, 335),
      Vector2(780, 370),
    ],
    orbPositions: [
      Vector2(200, 370),
      Vector2(350, 350),
      Vector2(480, 335),
      Vector2(620, 340),
      Vector2(780, 370),
      Vector2(920, 370),
    ],
  );

  /// Level 3-5: The Final Shinobi Trial — Grand Campaign Finale.
  static final level3_5 = ShinobiLevel(
    id: '3-5',
    world: ShinobiWorld.midnightAutumn,
    levelNumber: 5,
    title: 'The Final Shinobi Trial',
    subtitle: 'Grand Campaign Climax',
    description:
        'The ultimate test of a master shinobi. Navigate spinning shurikens, '
        'chasms, and collect all 8 ancient orbs to reach the sacred shrine!',
    star1Objective: 'Complete the Final Trial and save the realm',
    star2Objective: 'Collect all 8 sacred orbs',
    star3Objective: 'Flawless run with zero hits in under 25s',
    hasShurikens: true,
    timeLimit: 30,
    orbPositions: [
      Vector2(120, 380),
      Vector2(240, 360),
      Vector2(360, 345),
      Vector2(480, 335),
      Vector2(560, 335),
      Vector2(660, 345),
      Vector2(780, 360),
      Vector2(920, 380),
    ],
  );

  /// Master ordered list of all 15 levels across the 3 Worlds.
  static final List<ShinobiLevel> allLevels = [
    // World 1 (Dawn Village)
    level1_1,
    level1_2,
    level1_3,
    level1_4,
    level1_5,
    // World 2 (Twilight Sanctuary)
    level2_1,
    level2_2,
    level2_3,
    level2_4,
    level2_5,
    // World 3 (Midnight Autumn)
    level3_1,
    level3_2,
    level3_3,
    level3_4,
    level3_5,
  ];

  /// Look up a level by its unique ID (e.g. '1-3').
  static ShinobiLevel? getById(String id) {
    try {
      return allLevels.firstWhere((l) => l.id == id);
    } catch (_) {
      return null;
    }
  }
}
