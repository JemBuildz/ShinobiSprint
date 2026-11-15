import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:super_dash/bamboo_village/autumn_maple_game.dart';
import 'package:super_dash/bamboo_village/main_game.dart';
import 'package:super_dash/bamboo_village/twilight_game.dart';

/// Represents canonical stages in Shinobi Sprint.
enum ShinobiStage {
  /// Stage 1: Morning dawn in the Bamboo Village.
  bambooVillage(
    id: 1,
    title: 'Stage 1: Bamboo Village',
    locationName: 'Bamboo Village',
    timeOfDay: 'Morning Dawn',
    description:
        'Leap across village rooftops, scale the bamboo platform, and cross '
        'the chasm bridge to gather 6 ancient spirit orbs.',
    totalOrbs: 6,
    themeColor: Color(0xFF10B981),
    accentColor: Color(0xFF34D399),
    icon: Icons.nature_people,
    assetPlate: 'stage1_torii_shrine_1024.png',
  ),

  /// Stage 2: Golden sunset at the Sacred Torii Shrine.
  twilightSanctuary(
    id: 2,
    title: 'Stage 2: Twilight Sanctuary',
    locationName: 'Twilight Sanctuary',
    timeOfDay: 'Golden Sunset',
    description:
        'Navigate sagging rope bridges, avoid deadly bamboo spikes, scale the '
        'watchtowers, and collect 8 sacred orbs under the Grand Torii Gate.',
    totalOrbs: 8,
    themeColor: Color(0xFFF59E0B),
    accentColor: Color(0xFFFBBF24),
    icon: Icons.wb_twilight,
    assetPlate: 'level2_cinematic_stage_1024.png',
  ),

  /// Stage 3: Midnight moon in the Autumn Maple Forest.
  autumnMaple(
    id: 3,
    title: 'Stage 3: Autumn Maple Forest',
    locationName: 'Autumn Maple Forest',
    timeOfDay: 'Midnight Moon',
    description:
        'Dash beneath the glowing crescent moon, cross the arched stone '
        'river bridge, dodge spinning shurikens, and collect 6 nocturnal '
        'spirit orbs.',
    totalOrbs: 6,
    themeColor: Color(0xFFE11D48),
    accentColor: Color(0xFFFB7185),
    icon: Icons.park,
    assetPlate: 'level3_cinematic_stage_1024.png',
  );

  const ShinobiStage({
    required this.id,
    required this.title,
    required this.locationName,
    required this.timeOfDay,
    required this.description,
    required this.totalOrbs,
    required this.themeColor,
    required this.accentColor,
    required this.icon,
    required this.assetPlate,
  });

  final int id;
  final String title;
  final String locationName;
  final String timeOfDay;
  final String description;
  final int totalOrbs;
  final Color themeColor;
  final Color accentColor;
  final IconData icon;
  final String assetPlate;

  /// The next sequential stage in the campaign progression, or null if final.
  ShinobiStage? get nextStage {
    switch (this) {
      case ShinobiStage.bambooVillage:
        return ShinobiStage.twilightSanctuary;
      case ShinobiStage.twilightSanctuary:
        return ShinobiStage.autumnMaple;
      case ShinobiStage.autumnMaple:
        return null;
    }
  }

  /// Whether this is the final boss/climax stage in the campaign.
  bool get isFinalStage => nextStage == null;

  /// Builds the corresponding FlameGame instance for this stage.
  FlameGame buildGame({
    void Function(int orbs)? onOrbsChanged,
    VoidCallback? onHazardHit,
  }) {
    switch (this) {
      case ShinobiStage.bambooVillage:
        return MainGame(
          onOrbsChanged: onOrbsChanged,
          onHazardHit: onHazardHit,
        );
      case ShinobiStage.twilightSanctuary:
        return TwilightSanctuaryGame(
          onOrbsChanged: onOrbsChanged,
          onHazardHit: onHazardHit,
        );
      case ShinobiStage.autumnMaple:
        return AutumnMapleGame(
          onOrbsChanged: onOrbsChanged,
          onHazardHit: onHazardHit,
        );
    }
  }
}
