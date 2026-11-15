import 'dart:math' as math;

import 'package:flame/components.dart';
import 'package:flutter/material.dart';
import 'package:super_dash/game/components/feudal_foe.dart';
import 'package:super_dash/game/entities/enemy.dart';

/// A visual and physical katana slash arc spawned during a ninja melee attack.
class KatanaSlash extends PositionComponent {
  /// Creates a [KatanaSlash] effect.
  KatanaSlash({
    required Vector2 position,
    this.slashDuration = 0.25,
    this.damage = 1,
    this.isFacingRight = true,
    Vector2? size,
  }) : super(
          position: position,
          size: size ?? Vector2(56, 56),
          priority: 3,
        );

  /// Duration of the slash effect in seconds.
  final double slashDuration;

  /// Damage dealt by this katana strike.
  final int damage;

  /// Direction the strike is facing.
  final bool isFacingRight;

  double _elapsed = 0;

  /// Progress of the slash from 0.0 to 1.0.
  double get progress => (_elapsed / slashDuration).clamp(0.0, 1.0);

  /// Whether the slash hitbox is currently active.
  bool get isActive => _elapsed < slashDuration;

  @override
  void update(double dt) {
    super.update(dt);
    _elapsed += dt;

    if (isActive && parent != null) {
      final myRect = toRect();
      for (final enemy in parent!.children.whereType<Enemy>()) {
        if (myRect.overlaps(enemy.toRect())) {
          enemy.removeFromParent();
        }
      }
      for (final foe in parent!.children.whereType<FeudalFoe>()) {
        if (myRect.overlaps(foe.toRect())) {
          foe.removeFromParent();
        }
      }
    }

    if (_elapsed >= slashDuration) {
      removeFromParent();
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    final t = progress;
    final alpha = (1.0 - t).clamp(0.0, 1.0);

    final startAngle = isFacingRight ? -math.pi * 0.45 : math.pi * 1.45;
    final sweepAngle = (isFacingRight ? math.pi * 0.85 : -math.pi * 0.85) * t;

    final center = Offset(size.x * (isFacingRight ? 0.25 : 0.75), size.y * 0.5);
    final radius = size.x * 0.65;
    final rect = Rect.fromCircle(center: center, radius: radius);

    // Outer luminous moonlight aura
    final auraPaint = Paint()
      ..color = const Color(0xFF64B5F6).withValues(alpha: alpha * 0.45)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 6.5
      ..strokeCap = StrokeCap.round
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 3);
    canvas.drawArc(rect, startAngle, sweepAngle, false, auraPaint);

    // Razor-sharp bright katana blade edge
    final bladePaint = Paint()
      ..color = Colors.white.withValues(alpha: alpha * 0.95)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.5
      ..strokeCap = StrokeCap.round;
    canvas.drawArc(rect, startAngle, sweepAngle, false, bladePaint);
  }
}
