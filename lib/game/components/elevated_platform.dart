import 'dart:async';

import 'package:flame/components.dart';
import 'package:flutter/material.dart';

/// An elevated one-way platform (such as a cedar boardwalk bridge or pagoda
/// roof) that the ninja can jump through from below and land on from above.
class ElevatedPlatform extends PositionComponent with HasGameReference {
  /// Creates an [ElevatedPlatform].
  ElevatedPlatform({
    required super.position,
    required super.size,
    this.speed = 100.0,
    this.isOneWay = true,
    this.groundFloorY = 550.0,
    this.hasGroundPillars = false,
    super.priority = 1,
  });

  /// Horizontal scrolling speed in pixels/second.
  final double speed;

  /// Whether this platform allows jumping through from underneath.
  final bool isOneWay;

  /// The bottom ground Y level where foundation pillars anchor.
  final double groundFloorY;

  /// Whether vertical foundation pillars should extend to the ground.
  /// If `false`, the platform renders as a mid-air suspension platform
  /// with wooden angle brackets.
  final bool hasGroundPillars;

  Sprite? _platformSprite;

  /// Top Y coordinate where the ninja's feet contact the surface planks.
  double get surfaceY => position.y;

  /// Left X boundary of the platform.
  double get leftX => position.x;

  /// Right X boundary of the platform.
  double get rightX => position.x + size.x;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    try {
      final spriteAsset = hasGroundPillars
          ? 'cutouts/wooden_boardwalk_platform.png'
          : 'cutouts/wooden_midair_platform.png';
      _platformSprite = await game.loadSprite(spriteAsset);
    } catch (_) {
      // In headless test environments
    }
  }

  @override
  void update(double dt) {
    super.update(dt);
    position.x -= speed * dt;
    // Seamless wrapping forward when scrolled off screen
    if (position.x + size.x < -150) {
      position.x += 900;
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    // 1. Draw foundation support: grounded pillars firmly anchored to the floor
    // or feudal suspension angle brackets for mid-air platforms.
    if (hasGroundPillars) {
      final pillarPaint = Paint()
        ..color = const Color(0xFF1E140E)
        ..style = PaintingStyle.fill;
      final stonePlinthPaint = Paint()
        ..color = const Color(0xFF374151)
        ..style = PaintingStyle.fill;

      const pillarWidth = 12.0;
      final pillarHeight = (groundFloorY - (position.y + size.y)).clamp(
        0.0,
        600.0,
      );

      if (pillarHeight > 0) {
        // Left and right timber pillar legs extending all the way to ground
        canvas
          ..drawRect(
            Rect.fromLTWH(16, size.y - 2, pillarWidth, pillarHeight),
            pillarPaint,
          )
          ..drawRect(
            Rect.fromLTWH(size.x - 28, size.y - 2, pillarWidth, pillarHeight),
            pillarPaint,
          )
          ..drawRRect(
            RRect.fromRectAndRadius(
              Rect.fromLTWH(
                12,
                size.y - 2 + pillarHeight - 8,
                pillarWidth + 8,
                8,
              ),
              const Radius.circular(2),
            ),
            stonePlinthPaint,
          )
          ..drawRRect(
            RRect.fromRectAndRadius(
              Rect.fromLTWH(
                size.x - 32,
                size.y - 2 + pillarHeight - 8,
                pillarWidth + 8,
                8,
              ),
              const Radius.circular(2),
            ),
            stonePlinthPaint,
          );
      }
    } else {
      // Wooden angle brackets and suspension cables for mid-air platforms
      final bracketPaint = Paint()
        ..color = const Color(0xFF26140B)
        ..style = PaintingStyle.fill;
      final leftBracket = Path()
        ..moveTo(16, size.y - 4)
        ..lineTo(28, size.y - 4)
        ..lineTo(42, size.y + 16)
        ..lineTo(30, size.y + 16)
        ..close();
      final rightBracket = Path()
        ..moveTo(size.x - 28, size.y - 4)
        ..lineTo(size.x - 16, size.y - 4)
        ..lineTo(size.x - 30, size.y + 16)
        ..lineTo(size.x - 42, size.y + 16)
        ..close();
      final centerBracket = Path()
        ..moveTo(size.x / 2 - 8, size.y - 4)
        ..lineTo(size.x / 2 + 8, size.y - 4)
        ..lineTo(size.x / 2 + 14, size.y + 16)
        ..lineTo(size.x / 2 - 2, size.y + 16)
        ..close();

      canvas
        ..drawPath(leftBracket, bracketPaint)
        ..drawPath(rightBracket, bracketPaint)
        ..drawPath(centerBracket, bracketPaint);
    }

    // 2. Render platform top boardwalk planks
    if (_platformSprite != null) {
      _platformSprite!.render(canvas, size: size);
    } else {
      // Fallback wooden plank fill for testing
      final woodPaint = Paint()
        ..color = const Color(0xFF7A4A26)
        ..style = PaintingStyle.fill;
      canvas.drawRRect(
        RRect.fromRectAndRadius(
          Rect.fromLTWH(0, 0, size.x, size.y),
          const Radius.circular(4),
        ),
        woodPaint,
      );
    }
  }
}
