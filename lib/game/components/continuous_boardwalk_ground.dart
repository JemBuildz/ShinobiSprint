import 'dart:async';

import 'package:flame/components.dart';
import 'package:flutter/widgets.dart';

/// A continuous solid boardwalk ground track spanning the bottom of the stage.
///
/// Ensures the ninja runs firmly on top of polished cedar wood planks and
/// guarantees the character never falls into an abyss.
class ContinuousBoardwalkGround extends PositionComponent
    with HasGameReference {
  /// Creates a [ContinuousBoardwalkGround].
  ContinuousBoardwalkGround({
    super.position,
    Vector2? size,
    this.speed = 100.0,
    super.priority = 0,
  }) : super(size: size ?? Vector2(1200, 110));

  /// Scroll speed matching the foreground parallax velocity.
  final double speed;

  Sprite? _planksSprite;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    try {
      _planksSprite = await game.loadSprite(
        'cutouts/boardwalk_continuous.png',
      );
    } catch (_) {
      try {
        _planksSprite = await game.loadSprite(
          'cutouts/wooden_boardwalk_platform.png',
        );
      } catch (_) {
        // In headless test environments asset bundle may not be loaded
      }
    }
  }

  @override
  void update(double dt) {
    super.update(dt);
    position.x -= speed * dt;
    // Seamless wrapping loop
    if (position.x <= -600) {
      position.x += 600;
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    if (_planksSprite != null) {
      const plankWidth = 160.0;
      final count = (size.x / plankWidth).ceil() + 2;
      for (var i = 0; i < count; i++) {
        _planksSprite!.render(
          canvas,
          position: Vector2(i * plankWidth, 0),
          size: Vector2(plankWidth, size.y),
        );
      }
    }
  }
}
