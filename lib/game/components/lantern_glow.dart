import 'dart:math' as math;
import 'dart:ui';

import 'package:flame/components.dart';

/// A dynamic glowing lantern light effect for Shinobi Sprint.
///
/// Features warm amber flickering and pulsing luminance that illuminates the
/// surroundings at night and smoothly powers down during the daytime.
class LanternGlowComponent extends PositionComponent {
  /// Creates a [LanternGlowComponent].
  LanternGlowComponent({
    super.position,
    this.baseRadius = 24,
    this.pulseAmplitude = 4,
    this.pulseFrequency = 3,
    this.glowColor = const Color(0xFFFF9800),
    this.innerGlowColor = const Color(0xFFFFF3E0),
    this.isDaytime = false,
    super.priority = 10,
  }) : super(size: Vector2.all(baseRadius * 2), anchor: Anchor.center);

  /// The nominal radius of the outer warm light halo.
  final double baseRadius;

  /// The maximum deviation in radius during breathing pulse cycles.
  final double pulseAmplitude;

  /// Frequency of the breathing pulse in radians/second.
  final double pulseFrequency;

  /// The primary warm orange hue of the lantern light.
  final Color glowColor;

  /// The brighter core light color at the center of the flame.
  final Color innerGlowColor;

  /// Whether daytime mode is active. When true, the lantern glow is dimmed.
  bool isDaytime;

  double _elapsedTime = 0;
  double _flickerOffset = 0;

  /// The current intensity multiplier (1.0 at night, 0.0 during daytime).
  double get currentIntensity => isDaytime ? 0 : 1;

  /// The calculated dynamic outer radius including pulse and micro-flicker.
  double get currentRadius {
    if (isDaytime) return 0;
    final pulse = math.sin(_elapsedTime * pulseFrequency) * pulseAmplitude;
    return math.max(4, baseRadius + pulse + _flickerOffset);
  }

  @override
  void update(double dt) {
    super.update(dt);
    _elapsedTime += dt;
    // Micro-flicker simulation using pseudo-harmonic perturbation
    _flickerOffset = (math.sin(_elapsedTime * 17.3) * 0.7) +
        (math.cos(_elapsedTime * 29.1) * 0.5);
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    if (isDaytime) return;

    final radius = currentRadius;
    final center = Offset(size.x / 2, size.y / 2);

    // Outer soft atmospheric glow
    final outerPaint = Paint()
      ..shader = Gradient.radial(
        center,
        radius,
        [
          glowColor.withValues(alpha: 0.55),
          glowColor.withValues(alpha: 0.18),
          glowColor.withValues(alpha: 0),
        ],
        [0.0, 0.55, 1.0],
      )
      ..blendMode = BlendMode.plus;

    canvas.drawCircle(center, radius, outerPaint);

    // Inner bright core flame
    final innerPaint = Paint()
      ..shader = Gradient.radial(
        center,
        radius * 0.45,
        [
          innerGlowColor.withValues(alpha: 0.9),
          glowColor.withValues(alpha: 0.4),
          glowColor.withValues(alpha: 0),
        ],
        [0.0, 0.6, 1.0],
      )
      ..blendMode = BlendMode.plus;

    canvas.drawCircle(center, radius * 0.45, innerPaint);
  }
}
