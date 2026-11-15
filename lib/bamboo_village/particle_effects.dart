import 'dart:math' as math;
import 'dart:ui';
import 'package:flame/components.dart';

/// Floating autumn leaf / pollen particle representation.
class LeafParticleData {
  /// Creates a [LeafParticleData] container.
  LeafParticleData({
    required this.x,
    required this.y,
    required this.speedX,
    required this.speedY,
    required this.rotation,
    required this.rotSpeed,
    required this.scale,
    required this.oscillationPhase,
  });

  /// Horizontal position
  double x;

  /// Vertical position
  double y;

  /// Horizontal velocity
  double speedX;

  /// Vertical velocity
  double speedY;

  /// Current angle of rotation
  double rotation;

  /// Angular velocity
  double rotSpeed;

  /// Scale factor
  double scale;

  /// Phase for sinusoidal wave oscillation
  double oscillationPhase;
}

/// Floating autumn leaf particle emitter creating ambient drifting foliage.
class MapleLeafParticleEmitter extends Component {
  /// Creates a [MapleLeafParticleEmitter].
  MapleLeafParticleEmitter({
    this.leafSprite,
    this.petalColor = const Color(0xCCE11D48),
  }) : super(priority: 2);

  /// Optional sprite representing an individual leaf.
  final Sprite? leafSprite;

  /// Primary color for procedural glowing leaf petals.
  final Color petalColor;

  /// Random number generator
  final math.Random random = math.Random();

  /// Active list of floating leaf particles
  final List<LeafParticleData> particles = [];

  @override
  void onLoad() {
    super.onLoad();
    for (var i = 0; i < 14; i++) {
      particles.add(
        LeafParticleData(
          x: random.nextDouble() * 1024,
          y: random.nextDouble() * 500,
          speedX: 20 + random.nextDouble() * 30,
          speedY: 12 + random.nextDouble() * 18,
          rotation: random.nextDouble() * math.pi * 2,
          rotSpeed: -1.0 + random.nextDouble() * 2.0,
          scale: 0.8 + random.nextDouble() * 0.4,
          oscillationPhase: random.nextDouble() * math.pi * 2,
        ),
      );
    }
  }

  @override
  void update(double dt) {
    super.update(dt);
    for (final p in particles) {
      p
        ..oscillationPhase += dt * 2.0
        ..x += (p.speedX + math.sin(p.oscillationPhase) * 12) * dt
        ..y += p.speedY * dt
        ..rotation += p.rotSpeed * dt;

      if (p.x > 1050) {
        p.x = -30;
      }
      if (p.y > 560) {
        p
          ..y = -20
          ..x = random.nextDouble() * 1024;
      }
    }
  }

  @override
  void render(Canvas canvas) {
    for (final p in particles) {
      canvas
        ..save()
        ..translate(p.x, p.y)
        ..rotate(p.rotation)
        ..scale(p.scale);

      if (leafSprite != null) {
        leafSprite!.render(
          canvas,
          size: Vector2(18, 22),
          anchor: Anchor.center,
        );
      } else {
        // Render smooth vector-drawn glowing maple/sakura petal
        final paint = Paint()
          ..color = petalColor
          ..style = PaintingStyle.fill;
        final rect = Rect.fromCenter(
          center: Offset.zero,
          width: 8,
          height: 14,
        );
        canvas.drawOval(rect, paint);
      }
      canvas.restore();
    }
  }
}

/// Floating sunlit pollen motes drifting in morning light.
class BambooPollenEmitter extends Component {
  /// Creates a [BambooPollenEmitter].
  BambooPollenEmitter({
    this.leafSprite,
    this.pollenColor = const Color(0xAAFEF08A),
  }) : super(priority: 2);

  /// Optional sprite for pollen
  final Sprite? leafSprite;

  /// Pollen color
  final Color pollenColor;

  /// Random number generator
  final math.Random random = math.Random();

  /// Active list of floating particles
  final List<LeafParticleData> particles = [];

  @override
  void onLoad() {
    super.onLoad();
    for (var i = 0; i < 14; i++) {
      particles.add(
        LeafParticleData(
          x: random.nextDouble() * 1024,
          y: random.nextDouble() * 500,
          speedX: 15 + random.nextDouble() * 25,
          speedY: 8 + random.nextDouble() * 16,
          rotation: random.nextDouble() * math.pi * 2,
          rotSpeed: -0.8 + random.nextDouble() * 1.6,
          scale: 0.6 + random.nextDouble() * 0.5,
          oscillationPhase: random.nextDouble() * math.pi * 2,
        ),
      );
    }
  }

  @override
  void update(double dt) {
    super.update(dt);
    for (final p in particles) {
      p
        ..oscillationPhase += dt * 1.8
        ..x += (p.speedX + math.sin(p.oscillationPhase) * 10) * dt
        ..y += p.speedY * dt
        ..rotation += p.rotSpeed * dt;

      if (p.x > 1050) {
        p.x = -20;
      }
      if (p.y > 560) {
        p
          ..y = -15
          ..x = random.nextDouble() * 1024;
      }
    }
  }

  @override
  void render(Canvas canvas) {
    for (final p in particles) {
      canvas
        ..save()
        ..translate(p.x, p.y)
        ..scale(p.scale);

      final paint = Paint()
        ..color = pollenColor
        ..style = PaintingStyle.fill;
      canvas
        ..drawCircle(Offset.zero, 3.5, paint)
        ..restore();
    }
  }
}

/// Data container for a rising mist vapor particle.
class MistParticleData {
  /// Creates a [MistParticleData].
  MistParticleData({
    required this.x,
    required this.y,
    required this.speedX,
    required this.speedY,
    required this.radius,
    required this.maxRadius,
    required this.lifetime,
    required this.maxLifetime,
    required this.phase,
  });

  /// Horizontal coordinate.
  double x;

  /// Vertical coordinate.
  double y;

  /// Horizontal drift velocity.
  double speedX;

  /// Vertical upward velocity.
  double speedY;

  /// Current particle radius.
  double radius;

  /// Target peak radius.
  double maxRadius;

  /// Elapsed alive time in seconds.
  double lifetime;

  /// Total lifespan in seconds.
  double maxLifetime;

  /// Sinusoidal sway phase.
  double phase;

  /// Normalized lifecycle progress from 0.0 to 1.0.
  double get progress => (lifetime / maxLifetime).clamp(0.0, 1.0);
}

/// Particle emitter simulating rising river gorge mist, waterfall splash vapor,
/// and atmospheric clouds billowing over water surfaces.
class WaterfallMistEmitter extends Component {
  /// Creates a [WaterfallMistEmitter].
  WaterfallMistEmitter({
    this.mistBounds = const Rect.fromLTWH(260, 480, 500, 90),
    this.particleCount = 22,
    this.baseColor = const Color(0x30A5E4F3),
    this.upwardSpeed = 22.0,
    super.priority = 2,
  });

  /// Bounding rectangle in world coordinates where mist generates.
  final Rect mistBounds;

  /// Number of simultaneous mist particles active.
  final int particleCount;

  /// Soft atmospheric tint for the mist clouds.
  final Color baseColor;

  /// Average upward drift velocity.
  final double upwardSpeed;

  /// Random generator.
  final math.Random random = math.Random();

  /// Active list of mist particles.
  final List<MistParticleData> particles = [];

  @override
  void onLoad() {
    super.onLoad();
    for (var i = 0; i < particleCount; i++) {
      particles.add(_spawnParticle(randomOffset: true));
    }
  }

  MistParticleData _spawnParticle({bool randomOffset = false}) {
    final maxLife = 3.0 + random.nextDouble() * 3.5;
    return MistParticleData(
      x: mistBounds.left + random.nextDouble() * mistBounds.width,
      y: randomOffset
          ? mistBounds.top + random.nextDouble() * mistBounds.height
          : mistBounds.bottom - random.nextDouble() * 15,
      speedX: -8.0 + random.nextDouble() * 16.0,
      speedY: upwardSpeed * (0.7 + random.nextDouble() * 0.6),
      radius: 12.0 + random.nextDouble() * 8.0,
      maxRadius: 28.0 + random.nextDouble() * 24.0,
      lifetime: randomOffset ? random.nextDouble() * maxLife : 0.0,
      maxLifetime: maxLife,
      phase: random.nextDouble() * math.pi * 2,
    );
  }

  @override
  void update(double dt) {
    super.update(dt);
    for (var i = 0; i < particles.length; i++) {
      final p = particles[i];
      if (p.lifetime + dt >= p.maxLifetime || p.y < mistBounds.top - 20) {
        particles[i] = _spawnParticle();
        continue;
      }

      p
        ..lifetime += dt
        ..phase += dt * 1.5
        ..x += (p.speedX + math.sin(p.phase) * 12.0) * dt
        ..y -= p.speedY * dt
        ..radius =
            10.0 + (p.maxRadius - 10.0) * math.sin(p.progress * math.pi);
    }
  }

  @override
  void render(Canvas canvas) {
    for (final p in particles) {
      final alphaFactor = math.sin(p.progress * math.pi);
      final baseAlpha = (baseColor.a * 255.0).round().clamp(0, 255);
      final currentAlpha = ((baseAlpha / 255.0) * alphaFactor * 255.0)
          .clamp(0.0, 255.0)
          .toInt();

      if (currentAlpha <= 0) continue;

      final paint = Paint()
        ..color = baseColor.withAlpha(currentAlpha)
        ..style = PaintingStyle.fill;

      canvas.drawCircle(Offset(p.x, p.y), p.radius, paint);
    }
  }
}

/// Data container for an expanding perspective surface ripple or foam cluster.
class RiverRippleData {
  /// Creates a [RiverRippleData].
  RiverRippleData({
    required this.x,
    required this.y,
    required this.width,
    required this.maxWidth,
    required this.height,
    required this.flowSpeed,
    required this.lifetime,
    required this.maxLifetime,
    required this.isFoamCluster,
  });

  /// Horizontal center coordinate.
  double x;

  /// Vertical center coordinate.
  double y;

  /// Current width.
  double width;

  /// Maximum expanded width.
  double maxWidth;

  /// Ellipse height for 2.5D perspective stretching.
  double height;

  /// Stream current velocity.
  double flowSpeed;

  /// Lifetime elapsed.
  double lifetime;

  /// Total lifespan.
  double maxLifetime;

  /// Whether this is a dense foam froth cluster or a wide ripple ring.
  bool isFoamCluster;

  /// Lifecycle progress from 0.0 to 1.0.
  double get progress => (lifetime / maxLifetime).clamp(0.0, 1.0);
}

/// Dynamic river surface emitter generating elliptical foam rings, ripples,
/// and rushing water surface wake crests along river streams.
class RiverFoamRippleEmitter extends Component {
  /// Creates a [RiverFoamRippleEmitter].
  RiverFoamRippleEmitter({
    this.riverBounds = const Rect.fromLTWH(260, 520, 500, 56),
    this.rippleCount = 26,
    this.foamColor = const Color(0x65E0F7FA),
    this.currentSpeed = 35.0,
    super.priority = 2,
  });

  /// Bounding rectangle in world coordinates encompassing the river surface.
  final Rect riverBounds;

  /// Number of active ripples.
  final int rippleCount;

  /// Foam tint.
  final Color foamColor;

  /// Stream current flow speed.
  final double currentSpeed;

  /// Random generator.
  final math.Random random = math.Random();

  /// Active list of surface ripples.
  final List<RiverRippleData> ripples = [];

  @override
  void onLoad() {
    super.onLoad();
    for (var i = 0; i < rippleCount; i++) {
      ripples.add(_spawnRipple(randomOffset: true));
    }
  }

  RiverRippleData _spawnRipple({bool randomOffset = false}) {
    final maxLife = 1.8 + random.nextDouble() * 2.2;
    final isFoam = random.nextBool();
    return RiverRippleData(
      x: randomOffset
          ? riverBounds.left + random.nextDouble() * riverBounds.width
          : riverBounds.left - random.nextDouble() * 40.0,
      y: riverBounds.top + random.nextDouble() * riverBounds.height,
      width: isFoam ? 8.0 : 12.0,
      maxWidth: isFoam
          ? 24.0 + random.nextDouble() * 16.0
          : 45.0 + random.nextDouble() * 35.0,
      height: isFoam
          ? 5.0 + random.nextDouble() * 4.0
          : 6.0 + random.nextDouble() * 5.0,
      flowSpeed: currentSpeed * (0.8 + random.nextDouble() * 0.4),
      lifetime: randomOffset ? random.nextDouble() * maxLife : 0.0,
      maxLifetime: maxLife,
      isFoamCluster: isFoam,
    );
  }

  @override
  void update(double dt) {
    super.update(dt);
    for (var i = 0; i < ripples.length; i++) {
      final r = ripples[i];
      if (r.lifetime + dt >= r.maxLifetime ||
          r.x > riverBounds.right + 30.0) {
        ripples[i] = _spawnRipple();
        continue;
      }

      r
        ..lifetime += dt
        ..x += r.flowSpeed * dt
        ..width += (r.maxWidth / r.maxLifetime) * dt;
    }
  }

  @override
  void render(Canvas canvas) {
    for (final r in ripples) {
      final alphaFactor = math.sin(r.progress * math.pi);
      final baseAlpha = (foamColor.a * 255.0).round().clamp(0, 255);
      final currentAlpha = ((baseAlpha / 255.0) * alphaFactor * 255.0)
          .clamp(0.0, 255.0)
          .toInt();

      if (currentAlpha <= 0) continue;

      if (r.isFoamCluster) {
        // Frothy foam cluster
        final paint = Paint()
          ..color = foamColor.withAlpha(currentAlpha)
          ..style = PaintingStyle.fill;
        final rect = Rect.fromCenter(
          center: Offset(r.x, r.y),
          width: r.width,
          height: r.height,
        );
        canvas.drawOval(rect, paint);
      } else {
        // Expanding concentric ripple crest
        final paint = Paint()
          ..color = foamColor.withAlpha((currentAlpha * 0.85).toInt())
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1.4;
        final rect = Rect.fromCenter(
          center: Offset(r.x, r.y),
          width: r.width,
          height: r.height,
        );
        canvas.drawOval(rect, paint);
      }
    }
  }
}
