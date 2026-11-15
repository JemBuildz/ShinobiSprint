import 'dart:math' as math;
import 'dart:ui';
import 'package:flame/collisions.dart';
import 'package:flame/components.dart';

/// Modular ground terrain block with static solid collision.
class GroundBlockComponent extends PositionComponent with CollisionCallbacks {
  GroundBlockComponent({
    required Vector2 position,
    required Vector2 size,
    this.sprite,
  }) : super(
          position: position,
          size: size,
          anchor: Anchor.topLeft,
        );

  final Sprite? sprite;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    // Solid static hitbox for ground collision
    add(
      RectangleHitbox(
        collisionType: CollisionType.passive,
      ),
    );
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    if (sprite != null) {
      sprite!.render(canvas, size: Vector2(size.x, math.min(size.y, 146)));
    }
  }
}

/// Elevated platform with one-way jump-through hitbox.
/// The player can jump through this platform from underneath,
/// and stands firmly on top when falling down.
class PlatformComponent extends PositionComponent with CollisionCallbacks {
  PlatformComponent({
    required Vector2 position,
    required Vector2 size,
    this.sprite,
    this.isOneWay = true,
  }) : super(
          position: position,
          size: size,
          anchor: Anchor.topLeft,
        );

  final Sprite? sprite;
  final bool isOneWay;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    // One-way passive platform hitbox
    add(
      RectangleHitbox(
        position: Vector2.zero(),
        size: Vector2(size.x, isOneWay ? 14 : size.y),
        collisionType: CollisionType.passive,
      ),
    );
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    if (sprite != null) {
      sprite!.render(canvas, size: size);
    }
  }
}

/// Mossy stone pillar acting as a solid terrain obstacle.
class StonePillarComponent extends PositionComponent with CollisionCallbacks {
  StonePillarComponent({
    required Vector2 position,
    required Vector2 size,
    this.sprite,
  }) : super(
          position: position,
          size: size,
          anchor: Anchor.topLeft,
        );

  final Sprite? sprite;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    add(
      RectangleHitbox(
        collisionType: CollisionType.passive,
      ),
    );
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    if (sprite != null) {
      sprite!.render(canvas, size: size);
    }
  }
}

/// Continuous diagonal collision ramp for stairs and hillside slopes.
/// Allows the ninja to smoothly ascend and descend stairs without crashing
/// into individual step edges or needing manual jumps.
class SlopePlatformComponent extends PositionComponent
    with CollisionCallbacks {
  SlopePlatformComponent({
    required this.start,
    required this.end,
    this.thickness = 18.0,
  }) : super(
          position: Vector2(
            math.min(start.x, end.x),
            math.min(start.y, end.y),
          ),
          size: Vector2(
            (end.x - start.x).abs().clamp(1.0, double.infinity),
            (end.y - start.y).abs().clamp(1.0, double.infinity),
          ),
          priority: 3,
        );

  final Vector2 start;
  final Vector2 end;
  final double thickness;

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    // Polygon ramp hitbox covering the diagonal incline
    final localP1 = start - position;
    final localP2 = end - position;
    final localP3 = Vector2(localP2.x, localP2.y + thickness);
    final localP4 = Vector2(localP1.x, localP1.y + thickness);

    add(
      PolygonHitbox(
        [localP1, localP2, localP3, localP4],
        collisionType: CollisionType.passive,
      ),
    );
  }

  /// Calculates the expected ground Y coordinate for a given global X.
  double getYAt(double globalX) {
    if (end.x == start.x) return start.y;
    final t = ((globalX - start.x) / (end.x - start.x)).clamp(0.0, 1.0);
    return start.y + (end.y - start.y) * t;
  }

  /// Whether the given global X falls within this slope's span.
  bool containsX(double globalX) {
    final minX = math.min(start.x, end.x);
    final maxX = math.max(start.x, end.x);
    return globalX >= minX - 4 && globalX <= maxX + 4;
  }
}

/// Arched wooden rope suspension bridge replicating the reference image.
/// Uses segmented one-way platform hitboxes along the curve so the player
/// walks smoothly across the arched sag of the bridge.
class ArchedBridgeComponent extends PositionComponent {
  ArchedBridgeComponent({
    required Vector2 position,
    required Vector2 size,
    required this.bridgeSprite,
  }) : super(
          position: position,
          size: size,
          anchor: Anchor.topLeft,
        );

  final Sprite bridgeSprite;

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    // The bridge spans [position.x, position.x + size.x].
    // We add segmented one-way platform colliders following the catenary curve
    // of the wooden planks shown in the reference image.
    const segments = 10;
    final segWidth = size.x / segments;

    // Sag offsets along the bridge: higher at ends, dipping in the center
    final sagOffsets = <double>[
      size.y * 0.48, // left post
      size.y * 0.54,
      size.y * 0.60,
      size.y * 0.64,
      size.y * 0.66, // lowest point (center)
      size.y * 0.66,
      size.y * 0.64,
      size.y * 0.60,
      size.y * 0.54,
      size.y * 0.48, // right post
    ];

    for (var i = 0; i < segments; i++) {
      final segX = i * segWidth;
      final segY = sagOffsets[i];

      add(
        PlatformComponent(
          position: Vector2(segX, segY),
          size: Vector2(segWidth, 12),
        ),
      );
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    bridgeSprite.render(canvas, size: size);
  }
}

/// Collectible golden spirit orb.
class SpiritOrbComponent extends PositionComponent with CollisionCallbacks {
  SpiritOrbComponent({
    required Vector2 position,
    this.sprite,
    this.onCollected,
  }) : super(
          position: position,
          size: Vector2(32, 32),
          anchor: Anchor.center,
          priority: 8,
        );

  final Sprite? sprite;
  final VoidCallback? onCollected;
  bool isCollected = false;
  double _elapsed = 0;
  late final double _baseY;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    _baseY = position.y;
    add(
      CircleHitbox(
        radius: 14,
        position: Vector2(2, 2),
        collisionType: CollisionType.passive,
      ),
    );
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (!isCollected) {
      _elapsed += dt * 3.5;
      position.y = _baseY + math.sin(_elapsed) * 4;
    }
  }

  void collect() {
    if (isCollected) return;
    isCollected = true;
    onCollected?.call();
    removeFromParent();
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    if (sprite != null && !isCollected) {
      sprite!.render(canvas, size: size);
    }
  }
}

/// Deadly ground bamboo spikes hazard.
class SpikeHazardComponent extends PositionComponent with CollisionCallbacks {
  SpikeHazardComponent({
    required Vector2 position,
    required Vector2 size,
    this.sprite,
  }) : super(
          position: position,
          size: size,
          anchor: Anchor.topLeft,
          priority: 3,
        );

  final Sprite? sprite;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    add(RectangleHitbox(collisionType: CollisionType.passive));
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    if (sprite != null) {
      sprite!.render(canvas, size: size);
    }
  }
}

/// Deadly spinning shuriken hazard.
class ShurikenHazardComponent extends PositionComponent
    with CollisionCallbacks {
  ShurikenHazardComponent({
    required Vector2 position,
    this.sprite,
    this.rotationSpeed = 8.0,
  }) : super(
          position: position,
          size: Vector2(36, 36),
          anchor: Anchor.center,
          priority: 7,
        );

  final Sprite? sprite;
  final double rotationSpeed;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    add(
      CircleHitbox(
        radius: 16,
        position: Vector2(2, 2),
        collisionType: CollisionType.passive,
      ),
    );
  }

  @override
  void update(double dt) {
    super.update(dt);
    angle += rotationSpeed * dt;
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    if (sprite != null) {
      sprite!.render(canvas, size: size);
    }
  }
}
