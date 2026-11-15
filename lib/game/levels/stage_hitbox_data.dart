import 'dart:ui';
import 'package:flame/components.dart';
import 'package:flutter/material.dart';
import 'package:super_dash/bamboo_village/platform_component.dart';

/// Collision surface classification for the Master Stage Plate Architecture.
enum StageSurfaceType {
  /// Solid ground terrain that blocks player vertical and lateral movement.
  solid,

  /// One-way jump-through and drop-through bridge platform.
  oneWay,

  /// Lethal hazard surface (chasm, spike pit, river torrent) triggering reset.
  hazard,
}

/// Coordinate mapping container with aspect-ratio scaling.
class StageCollisionBox {
  /// Creates a calibrated collision boundary.
  const StageCollisionBox({
    required this.x,
    required this.y,
    required this.w,
    required this.h,
    required this.type,
    this.id,
  });

  /// Canonical X coordinate on native 1024x576 standard plate.
  final double x;

  /// Canonical Y coordinate on native 1024x576 standard plate.
  final double y;

  /// Canonical width.
  final double w;

  /// Canonical height.
  final double h;

  /// Surface physics behavior.
  final StageSurfaceType type;

  /// Optional identifier for debug tracking.
  final String? id;

  /// Translates canonical 1024x576 box to absolute [Rect]
  /// scaled to [stageSize].
  Rect toRect([Vector2? stageSize]) {
    if (stageSize == null) return Rect.fromLTWH(x, y, w, h);
    final scaleX = stageSize.x / 1024.0;
    final scaleY = stageSize.y / 576.0;
    return Rect.fromLTWH(x * scaleX, y * scaleY, w * scaleX, h * scaleY);
  }
}

/// Linear slope ramp for stairs, bridges, and mountain inclines.
class StageSlopeRamp {
  /// Creates a calibrated slope ramp for stairs.
  const StageSlopeRamp({
    required this.startX,
    required this.startY,
    required this.endX,
    required this.endY,
    this.id,
  });

  /// Canonical starting X coordinate.
  final double startX;

  /// Canonical starting Y coordinate.
  final double startY;

  /// Canonical ending X coordinate.
  final double endX;

  /// Canonical ending Y coordinate.
  final double endY;

  /// Optional identifier for debug tracking.
  final String? id;
}

/// Master Stage Plate calibration registry.
class StageCalibrationData {
  /// Creates a stage configuration instance.
  const StageCalibrationData({
    required this.stageId,
    required this.title,
    required this.imageAsset,
    required this.hitboxes,
    required this.playerStart,
    required this.soulOrbs,
    required this.goalPortal,
    this.slopes,
  });

  /// Numerical stage index.
  final int stageId;

  /// Human-readable level title.
  final String title;

  /// Full hand-painted 16:9 master plate asset filename.
  final String imageAsset;

  /// Registered collision boxes.
  final List<StageCollisionBox> hitboxes;

  /// Starting spawn point for the player ninja.
  final Vector2 playerStart;

  /// Collectible spirit soul orb coordinates.
  final List<Vector2> soulOrbs;

  /// Level exit goal portal coordinate.
  final Vector2 goalPortal;

  /// Optional stair ramp and slope incline paths.
  final List<StageSlopeRamp>? slopes;

  /// Level 1: Daytime Torii Shrine Path (Opening Shrine)
  static final level1ToriiShrine = StageCalibrationData(
    stageId: 1,
    title: 'Daytime Torii Shrine Path',
    imageAsset: 'stage1_daytime_torii_shrine_1024.png',
    playerStart: Vector2(340, 298),
    soulOrbs: [
      Vector2(70, 220), // Left shrine porch
      Vector2(230, 290), // Left stairs
      Vector2(340, 310), // Cobblestone path
      Vector2(520, 290), // Midair leap over mountain chasm
      Vector2(795, 240), // Grand Torii staircase
      Vector2(960, 100), // Upper mountain temple pavilion
    ],
    goalPortal: Vector2(960, 150 - 52),
    slopes: const [
      // Left Shrine Staircase: Ramps up from bluff (315, 350)
      // to porch (140, 265)
      StageSlopeRamp(
        id: 'left_shrine_stairs',
        startX: 315,
        startY: 350,
        endX: 140,
        endY: 265,
      ),
      // Grand Torii Staircase: Ramps up from bluff (700, 350)
      // to temple (890, 150)
      StageSlopeRamp(
        id: 'grand_torii_stairs',
        startX: 700,
        startY: 350,
        endX: 890,
        endY: 150,
      ),
    ],
    hitboxes: const [
      // Left Mountain Bluff: Solid ground
      StageCollisionBox(
        id: 'left_mountain_bluff',
        x: 0,
        y: 350,
        w: 455,
        h: 226,
        type: StageSurfaceType.solid,
      ),
      // Left Shrine Pavilion Terrace: Porch landing
      StageCollisionBox(
        id: 'left_shrine_terrace',
        x: 0,
        y: 265,
        w: 140,
        h: 20,
        type: StageSurfaceType.solid,
      ),
      // Center Mountain Chasm Hazard: Lethal fall pit
      StageCollisionBox(
        id: 'center_chasm_hazard',
        x: 455,
        y: 520,
        w: 130,
        h: 56,
        type: StageSurfaceType.hazard,
      ),
      // Right Mountain Bluff: Solid ground
      StageCollisionBox(
        id: 'right_mountain_bluff',
        x: 585,
        y: 350,
        w: 439,
        h: 226,
        type: StageSurfaceType.solid,
      ),
      // Upper Mountain Temple Terrace: Mountain landing
      StageCollisionBox(
        id: 'upper_temple_terrace',
        x: 890,
        y: 150,
        w: 134,
        h: 20,
        type: StageSurfaceType.solid,
      ),
    ],
  );

  /// Level 3: Nighttime Autumn Maple Forest & Pagoda Bridge
  static final level1AutumnMaple = StageCalibrationData(
    stageId: 1,
    title: 'Nighttime Autumn Maple Forest & Pagoda Bridge',
    imageAsset: 'level3_cinematic_stage_1024.png',
    playerStart: Vector2(70, 418),
    soulOrbs: [
      Vector2(210, 370),
      Vector2(440, 335), // Bridge apex
      Vector2(580, 340),
      Vector2(830, 370),
    ],
    goalPortal: Vector2(980, 418),
    hitboxes: const [
      // Left Grassy Cliff: Solid terrain
      StageCollisionBox(
        id: 'left_grassy_cliff',
        x: 0,
        y: 418,
        w: 275,
        h: 158,
        type: StageSurfaceType.solid,
      ),
      // Arched Wooden Bridge: One-way drop-through surface
      StageCollisionBox(
        id: 'arched_wooden_bridge',
        x: 275,
        y: 395,
        w: 480,
        h: 24,
        type: StageSurfaceType.oneWay,
      ),
      // Right Pagoda Terrace: Solid terrain
      StageCollisionBox(
        id: 'right_pagoda_terrace',
        x: 755,
        y: 418,
        w: 269,
        h: 158,
        type: StageSurfaceType.solid,
      ),
      // River Mist Water Hazard: Lethal reset pit
      StageCollisionBox(
        id: 'river_mist_water_hazard',
        x: 280,
        y: 535,
        w: 470,
        h: 41,
        type: StageSurfaceType.hazard,
      ),
    ],
  );

  /// Level 2: Nighttime Waterfall Gorge & Suspended Bridges
  static final level2SunsetBamboo = StageCalibrationData(
    stageId: 2,
    title: 'Nighttime Waterfall Gorge & Suspended Bridges',
    imageAsset: 'level2_night_waterfall_stage_1024.png',
    playerStart: Vector2(70, 350 - 52),
    soulOrbs: [
      Vector2(140, 310),
      Vector2(335, 335), // Bridge 1
      Vector2(480, 310), // Center stone pier
      Vector2(640, 350), // Bridge 2
      Vector2(840, 340), // Right cliff
    ],
    goalPortal: Vector2(960, 380 - 52),
    hitboxes: const [
      // Left Cliff: Solid ground
      StageCollisionBox(
        id: 'left_cliff_terrace',
        x: 0,
        y: 350,
        w: 230,
        h: 226,
        type: StageSurfaceType.solid,
      ),
      // Suspended Bridge 1: One-way catenary bridge
      StageCollisionBox(
        id: 'suspended_bridge_1',
        x: 230,
        y: 365,
        w: 210,
        h: 20,
        type: StageSurfaceType.oneWay,
      ),
      // Center Stone Pier: Solid platform
      StageCollisionBox(
        id: 'center_stone_pier',
        x: 440,
        y: 350,
        w: 80,
        h: 226,
        type: StageSurfaceType.solid,
      ),
      // Suspended Bridge 2: One-way catenary bridge
      StageCollisionBox(
        id: 'suspended_bridge_2',
        x: 520,
        y: 380,
        w: 240,
        h: 20,
        type: StageSurfaceType.oneWay,
      ),
      // Right Cliff Terrace: Solid ground
      StageCollisionBox(
        id: 'right_cliff_terrace',
        x: 760,
        y: 380,
        w: 264,
        h: 196,
        type: StageSurfaceType.solid,
      ),
      // Upper Right Lookout Ledge: One-way platform
      StageCollisionBox(
        id: 'upper_right_lookout',
        x: 820,
        y: 240,
        w: 204,
        h: 20,
        type: StageSurfaceType.oneWay,
      ),
      // River Rapids Torrent Hazard: Lethal fall reset
      StageCollisionBox(
        id: 'river_rapids_hazard',
        x: 230,
        y: 520,
        w: 530,
        h: 56,
        type: StageSurfaceType.hazard,
      ),
    ],
  );

  /// Level 4: Cascading Waterfall & Wooden Arch Bridge
  static final waterfallBridge = StageCalibrationData(
    stageId: 4,
    title: 'Cascading Waterfall & Arch Bridge',
    imageAsset: 'stitch_waterfall_bridge_day_1024.png',
    playerStart: Vector2(100, 482 - 52),
    soulOrbs: [
      Vector2(200, 440),
      Vector2(512, 335), // Bridge center
      Vector2(850, 310), // Right cliff
      Vector2(880, 440),
    ],
    goalPortal: Vector2(960, 482 - 52),
    hitboxes: const [
      // Left Riverbank: Solid ground baseline
      StageCollisionBox(
        id: 'left_riverbank_ground',
        x: 0,
        y: 482,
        w: 420,
        h: 94,
        type: StageSurfaceType.solid,
      ),
      // Right Riverbank: Solid ground baseline
      StageCollisionBox(
        id: 'right_riverbank_ground',
        x: 580,
        y: 482,
        w: 444,
        h: 94,
        type: StageSurfaceType.solid,
      ),
      // River Rapids Torrent Hazard: Fall hazard
      StageCollisionBox(
        id: 'river_rapids_hazard',
        x: 420,
        y: 520,
        w: 160,
        h: 56,
        type: StageSurfaceType.hazard,
      ),
      // Left Mountain Cliff: Elevated one-way / solid ledge
      StageCollisionBox(
        id: 'left_cliff_ledge',
        x: 0,
        y: 350,
        w: 330,
        h: 20,
        type: StageSurfaceType.oneWay,
      ),
      // Suspended Wooden Arch Bridge
      StageCollisionBox(
        id: 'wooden_arch_bridge',
        x: 330,
        y: 375,
        w: 370,
        h: 18,
        type: StageSurfaceType.oneWay,
      ),
      // Right Teahouse Cliff: Elevated one-way ledge
      StageCollisionBox(
        id: 'right_cliff_ledge',
        x: 700,
        y: 350,
        w: 324,
        h: 20,
        type: StageSurfaceType.oneWay,
      ),
    ],
  );
}

/// Full Flame component that mounts the 100% whole hand-painted scene plate
/// in 1 GPU texture pass (Priority = 0) and spawns collision colliders.
class MasterStagePlateComponent extends PositionComponent {
  /// Creates a [MasterStagePlateComponent].
  MasterStagePlateComponent({
    required this.calibrationData,
    this.stageSprite,
    this.debugDrawHitboxes = false,
  }) : super(
          position: Vector2.zero(),
          size: Vector2(1024, 576),
          priority: 0,
        );

  /// Stage calibration and collision registry.
  final StageCalibrationData calibrationData;

  /// Hand-painted master scene plate texture.
  final Sprite? stageSprite;

  /// Debug overlay flag:
  /// - Green: Solid Ground
  /// - Amber: One-Way Drop-Through Bridge
  /// - Red: Lethal Hazard / Chasm
  bool debugDrawHitboxes;

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    // Spawn invisible collision components according to surface physics
    for (final box in calibrationData.hitboxes) {
      final pos = Vector2(box.x, box.y);
      final boxSize = Vector2(box.w, box.h);

      switch (box.type) {
        case StageSurfaceType.solid:
          await add(
            GroundBlockComponent(
              position: pos,
              size: boxSize,
            )..priority = 3,
          );
        case StageSurfaceType.oneWay:
          await add(
            PlatformComponent(
              position: pos,
              size: boxSize,
            )..priority = 3,
          );
        case StageSurfaceType.hazard:
          await add(
            SpikeHazardComponent(
              position: pos,
              size: boxSize,
            )..priority = 3,
          );
      }
    }

    // Spawn linear slope ramps for stairs and bridges
    if (calibrationData.slopes != null) {
      for (final slope in calibrationData.slopes!) {
        await add(
          SlopePlatformComponent(
            start: Vector2(slope.startX, slope.startY),
            end: Vector2(slope.endX, slope.endY),
          )..priority = 3,
        );
      }
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    // 1. Render single 100% whole master plate (1 GPU draw call)
    if (stageSprite != null) {
      stageSprite!.render(canvas, size: size);
    }

    // 2. Render debug hitbox visual overlays if enabled
    if (debugDrawHitboxes) {
      for (final box in calibrationData.hitboxes) {
        final rect = box.toRect(size);
        final Paint fillPaint;
        final Paint strokePaint;

        switch (box.type) {
          case StageSurfaceType.solid:
            fillPaint = Paint()
              ..color = const Color(0x6022C55E) // Green fill
              ..style = PaintingStyle.fill;
            strokePaint = Paint()
              ..color = const Color(0xFF22C55E)
              ..style = PaintingStyle.stroke
              ..strokeWidth = 2;
          case StageSurfaceType.oneWay:
            fillPaint = Paint()
              ..color = const Color(0x70F59E0B) // Amber fill
              ..style = PaintingStyle.fill;
            strokePaint = Paint()
              ..color = const Color(0xFFF59E0B)
              ..style = PaintingStyle.stroke
              ..strokeWidth = 2;
          case StageSurfaceType.hazard:
            fillPaint = Paint()
              ..color = const Color(0x80EF4444) // Red fill
              ..style = PaintingStyle.fill;
            strokePaint = Paint()
              ..color = const Color(0xFFEF4444)
              ..style = PaintingStyle.stroke
              ..strokeWidth = 2;
        }

        canvas
          ..drawRect(rect, fillPaint)
          ..drawRect(rect, strokePaint);
      }
    }
  }
}
