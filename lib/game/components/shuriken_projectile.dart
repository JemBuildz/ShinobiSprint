import 'dart:async';

import 'package:flame/components.dart';
import 'package:flutter/material.dart';
import 'package:super_dash/game/components/feudal_foe.dart';
import 'package:super_dash/game/entities/enemy.dart';

/// A flying, rapidly spinning shuriken projectile thrown by the ninja.
class ShurikenProjectile extends PositionComponent with HasGameReference {
  /// Creates a [ShurikenProjectile].
  ShurikenProjectile({
    required Vector2 position,
    Vector2? velocity,
    this.rotationSpeed = 24.0,
    this.maxTravelDistance = 900.0,
    this.damage = 1,
    Vector2? size,
  })  : velocity = velocity ?? Vector2(650, 0),
        _initialX = position.x,
        super(
          position: position,
          size: size ?? Vector2.all(28),
          anchor: Anchor.center,
          priority: 3,
        );

  /// Velocity vector of the flying projectile.
  final Vector2 velocity;

  /// Angular rotation speed in radians per second.
  final double rotationSpeed;

  /// Maximum distance the shuriken will travel before auto-removal.
  final double maxTravelDistance;

  /// Damage dealt on impact.
  final int damage;

  final double _initialX;

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    try {
      final shurikenImage = game.images.containsKey('shuriken_spin.png')
          ? game.images.fromCache('shuriken_spin.png')
          : await game.images.load('shuriken_spin.png');
      final animation = SpriteAnimation.fromFrameData(
        shurikenImage,
        SpriteAnimationData.sequenced(
          amount: 8,
          stepTime: 0.04,
          textureSize: Vector2(64, 64),
        ),
      );

      final spriteComp = SpriteAnimationComponent(
        animation: animation,
        size: size,
        anchor: Anchor.center,
        position: size / 2,
      );
      add(spriteComp);
    } catch (_) {
      // Fallback custom procedural rendering if running headless
    }
  }

  @override
  void update(double dt) {
    super.update(dt);

    position += velocity * dt;
    angle += rotationSpeed * dt;

    if (parent != null) {
      final myRect = toRect();
      for (final enemy in parent!.children.whereType<Enemy>()) {
        if (myRect.overlaps(enemy.toRect())) {
          enemy.removeFromParent();
          removeFromParent();
          return;
        }
      }
      for (final foe in parent!.children.whereType<FeudalFoe>()) {
        if (myRect.overlaps(foe.toRect())) {
          foe.removeFromParent();
          removeFromParent();
          return;
        }
      }
    }

    if ((position.x - _initialX).abs() >= maxTravelDistance) {
      removeFromParent();
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    // Fallback metallic 4-point throwing star if sprite not loaded
    if (children.isEmpty) {
      final paint = Paint()..color = const Color(0xFFDCDCDC);
      final center = Offset(size.x / 2, size.y / 2);
      final r = size.x / 2;
      canvas.drawCircle(center, r * 0.35, paint);
      for (var i = 0; i < 4; i++) {
        final path = Path()
          ..moveTo(center.dx, center.dy)
          ..lineTo(center.dx + r, center.dy)
          ..lineTo(center.dx + r * 0.3, center.dy + r * 0.3)
          ..close();
        canvas
          ..save()
          ..translate(center.dx, center.dy)
          ..rotate(i * 1.5708)
          ..translate(-center.dx, -center.dy)
          ..drawPath(path, paint)
          ..restore();
      }
    }
  }
}
