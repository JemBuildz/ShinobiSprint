import 'dart:async';
import 'dart:math' as math;
import 'dart:ui';

import 'package:flame/collisions.dart';
import 'package:flame/components.dart';
import 'package:super_dash/game/components/katana_slash.dart';
import 'package:super_dash/game/components/shuriken_projectile.dart';

/// Available Feudal Foes & Cursed Obstacle types.
enum FoeType {
  /// Armored spearmen with conical jingasa helmet.
  ashigaru,

  /// Wandering masterless samurai with katana.
  ronin,

  /// Samurai bowman firing cursed arrows.
  archer,

  /// Heavy immovable wrestler obstacle.
  sumo,

  /// Blue horned ogre with kanabo club.
  oni,

  /// Red-faced winged mountain crow-goblin.
  tengu,

  /// Earth spider crawling on ground.
  tsuchigumo,

  /// Floating mystical spirit wisps.
  hitodama,

  /// Cursed one-eyed hopping umbrella yokai.
  karakasa,

  /// Ancient mossy stone well with reaching ghostly hands.
  cursedWell,

  /// Demonic sword resting on purple aura stand.
  ancestralKatana,

  /// Collapsed stone lantern with glowing cursed eye.
  brokenLantern,

  /// Holy multi-tailed spirit fox guardian.
  kitsune,

  /// Translucent spiritual phantom ninja.
  ghostlyNinja,

  /// Dark swirling shadow void portal.
  shadowPortal,
}

/// An enemy or hazard obstacle in Shinobi Sprint.
class FeudalFoe extends SpriteComponent
    with HasGameReference, CollisionCallbacks {
  /// Creates a [FeudalFoe].
  FeudalFoe({
    required this.foeType,
    super.position,
    Vector2? size,
    super.anchor = Anchor.bottomLeft,
    this.speed = 40.0,
    this.patrolRange = 60.0,
    this.onPlayerDefeated,
  }) : super(
          size: size ?? defaultSizeFor(foeType),
          priority: 2,
        );

  /// The category of feudal foe or hazard.
  final FoeType foeType;

  /// Patrol speed in pixels per second.
  final double speed;

  /// Distance the foe wanders back and forth.
  final double patrolRange;

  /// Optional callback invoked when player collides with this hazard.
  final VoidCallback? onPlayerDefeated;

  double _startX = 0;
  double _time = 0;
  bool _movingLeft = true;
  bool _isDefeated = false;

  /// Whether this foe has been vanquished.
  bool get isDefeated => _isDefeated;

  /// Default bounding box size for each foe type.
  static Vector2 defaultSizeFor(FoeType type) {
    switch (type) {
      case FoeType.ashigaru:
        return Vector2(74, 64);
      case FoeType.ronin:
        return Vector2(52, 76);
      case FoeType.archer:
        return Vector2(64, 68);
      case FoeType.sumo:
        return Vector2(80, 66);
      case FoeType.oni:
        return Vector2(68, 84);
      case FoeType.tengu:
        return Vector2(76, 76);
      case FoeType.tsuchigumo:
        return Vector2(82, 58);
      case FoeType.hitodama:
        return Vector2(58, 48);
      case FoeType.karakasa:
        return Vector2(54, 62);
      case FoeType.cursedWell:
        return Vector2(70, 55);
      case FoeType.ancestralKatana:
        return Vector2(88, 48);
      case FoeType.brokenLantern:
        return Vector2(50, 55);
      case FoeType.kitsune:
        return Vector2(65, 60);
      case FoeType.ghostlyNinja:
        return Vector2(50, 68);
      case FoeType.shadowPortal:
        return Vector2(70, 55);
    }
  }

  /// Relative asset path for this foe's sprite.
  String get assetPath {
    switch (foeType) {
      case FoeType.ashigaru:
        return 'foes/ashigaru.png';
      case FoeType.ronin:
        return 'foes/ronin.png';
      case FoeType.archer:
        return 'foes/archer.png';
      case FoeType.sumo:
        return 'foes/sumo.png';
      case FoeType.oni:
        return 'foes/oni.png';
      case FoeType.tengu:
        return 'foes/tengu.png';
      case FoeType.tsuchigumo:
        return 'foes/tsuchigumo.png';
      case FoeType.hitodama:
        return 'foes/hitodama.png';
      case FoeType.karakasa:
        return 'foes/karakasa.png';
      case FoeType.cursedWell:
        return 'foes/cursed_well.png';
      case FoeType.ancestralKatana:
        return 'foes/ancestral_katana.png';
      case FoeType.brokenLantern:
        return 'foes/broken_lantern.png';
      case FoeType.kitsune:
        return 'foes/kitsune.png';
      case FoeType.ghostlyNinja:
        return 'foes/ninja_ghostly.png';
      case FoeType.shadowPortal:
        return 'foes/shadow_portal.png';
    }
  }

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    _startX = position.x;
    add(
      RectangleHitbox(
        position: Vector2(size.x * 0.1, size.y * 0.1),
        size: Vector2(size.x * 0.8, size.y * 0.8),
      ),
    );
    try {
      final img = await game.images.load(assetPath);
      sprite = Sprite(img);
    } catch (_) {
      // In headless test environments
    }
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (_isDefeated) return;

    _time += dt;

    switch (foeType) {
      case FoeType.hitodama:
        // Sine wave vertical floating motion
        position.y += math.sin(_time * 4) * 0.6;
      case FoeType.karakasa:
        // Hopping bouncing motion
        position.y += math.sin(_time * 6) * 1.0;
      case FoeType.ashigaru:
      case FoeType.ronin:
      case FoeType.tengu:
        // Horizontal patrol
        if (_movingLeft) {
          position.x -= speed * dt;
          if (position.x <= _startX - patrolRange) {
            _movingLeft = false;
          }
        } else {
          position.x += speed * dt;
          if (position.x >= _startX + patrolRange) {
            _movingLeft = true;
          }
        }
      case FoeType.archer:
      case FoeType.sumo:
      case FoeType.oni:
      case FoeType.tsuchigumo:
      case FoeType.cursedWell:
      case FoeType.ancestralKatana:
      case FoeType.brokenLantern:
      case FoeType.kitsune:
      case FoeType.ghostlyNinja:
      case FoeType.shadowPortal:
        // Static or custom behaviors
    }
  }

  @override
  void onCollision(Set<Vector2> intersectionPoints, PositionComponent other) {
    super.onCollision(intersectionPoints, other);
    if (_isDefeated) return;

    if (other is KatanaSlash || other is ShurikenProjectile) {
      defeat();
    }
  }

  @override
  void render(Canvas canvas) {
    canvas.save();
    if (!_movingLeft) {
      canvas
        ..scale(-1, 1)
        ..translate(-size.x, 0);
    }
    super.render(canvas);
    canvas.restore();
  }

  /// Vanquish this foe.
  void defeat() {
    if (_isDefeated) return;
    _isDefeated = true;
    removeFromParent();
  }
}
