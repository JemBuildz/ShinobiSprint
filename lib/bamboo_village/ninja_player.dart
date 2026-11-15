import 'dart:ui';
import 'package:flame/collisions.dart';
import 'package:flame/components.dart';
import 'package:flame/game.dart';
import 'package:flame/sprite.dart';
import 'package:flutter/services.dart';
import 'package:super_dash/bamboo_village/platform_component.dart';
import 'package:super_dash/game/components/feudal_foe.dart';
import 'package:super_dash/game/components/katana_slash.dart';
import 'package:super_dash/game/components/shuriken_projectile.dart';

enum NinjaState { idle, running, leaping, falling, attacking, dead }

/// Official character animations, sliced from `clean_chibi_ninja.png`
/// into 128x128 frame strips.
class NinjaAnimations {
  const NinjaAnimations({
    required this.sprite,
    required this.idle,
    required this.run,
    required this.jump,
    required this.attack,
    required this.death,
  });

  final Sprite sprite;
  final SpriteAnimation idle;
  final SpriteAnimation run;
  final SpriteAnimation jump;
  final SpriteAnimation attack;
  final SpriteAnimation death;

  /// Loads all ninja animations through the given game's image cache.
  static Future<NinjaAnimations> load(FlameGame game) async {
    final frame = Vector2.all(128);
    Future<SpriteAnimation> strip(
      String file,
      int amount,
      double stepTime, {
      bool loop = true,
    }) =>
        game.loadSpriteAnimation(
          file,
          SpriteAnimationData.sequenced(
            amount: amount,
            stepTime: stepTime,
            textureSize: frame,
            loop: loop,
          ),
        );

    return NinjaAnimations(
      sprite: await game.loadSprite('character_ninja.png'),
      idle: await strip('spritesheet_ninja_idle.png', 4, 0.16),
      run: await strip('spritesheet_ninja_run.png', 5, 0.08),
      jump: await strip('spritesheet_ninja_jump.png', 4, 0.12, loop: false),
      attack:
          await strip('spritesheet_ninja_attack.png', 4, 0.07, loop: false),
      death: await strip('spritesheet_ninja_death.png', 4, 0.15, loop: false),
    );
  }
}

/// Player Entity: Chibi Blue Shinobi Ninja
/// Physics parameters configured strictly per prompt:
/// - Horizontal velocity: 180 px/s
/// - Jump impulse: -420 px/s
/// - Gravity: 980 px/s²
class NinjaPlayerComponent extends PositionComponent
    with CollisionCallbacks, KeyboardHandler, HasGameRef {
  NinjaPlayerComponent({
    required Vector2 position,
    this.ninjaSprite,
    this.runAnimation,
    this.idleAnimation,
    this.jumpAnimation,
    this.attackAnimation,
    this.deathAnimation,
    this.onHazardHit,
  })  : _runTicker = runAnimation?.createTicker(),
        _idleTicker = idleAnimation?.createTicker(),
        _jumpTicker = jumpAnimation?.createTicker(),
        _attackTicker = attackAnimation?.createTicker(),
        _deathTicker = deathAnimation?.createTicker(),
        super(
          position: position,
          size: Vector2(36, 52),
          anchor: Anchor.bottomCenter,
          priority: 10,
        );

  final Sprite? ninjaSprite;
  SpriteAnimation? runAnimation;
  SpriteAnimation? idleAnimation;
  SpriteAnimation? jumpAnimation;
  SpriteAnimation? attackAnimation;
  SpriteAnimation? deathAnimation;

  SpriteAnimationTicker? _runTicker;
  SpriteAnimationTicker? _idleTicker;
  SpriteAnimationTicker? _jumpTicker;
  SpriteAnimationTicker? _attackTicker;
  SpriteAnimationTicker? _deathTicker;

  bool isAttacking = false;
  double _attackTimer = 0;

  bool isDead = false;
  double _deathTimer = 0;

  /// Current visual & behavioral animation state.
  NinjaState state = NinjaState.idle;

  /// Optional callback invoked when hitting a hazard or falling into a pit.
  final VoidCallback? onHazardHit;

  // Physics constants per specification
  final double horizontalSpeed = 180; // 180 px/s
  final double jumpImpulse = -420;    // -420 px/s
  final double gravity = 980;        // 980 px/s²

  // Dynamic state
  Vector2 velocity = Vector2.zero();
  bool _isOnGround = false;
  bool _hadGroundCollision = false;
  int _groundGraceFrames = 0;
  SlopePlatformComponent? _currentSlope;

  bool get isOnGround => _isOnGround;
  set isOnGround(bool value) {
    _isOnGround = value;
    if (value) {
      _hadGroundCollision = true;
      _groundGraceFrames = 0;
    }
  }

  bool isFacingRight = true;
  bool isDroppingThrough = false;
  double _dropTimer = 0;

  // Input state
  int _horizontalInput = 0;

  late final RectangleHitbox _hitbox;

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    // Decoupled physical hitbox fitting ninja torso & legs tightly
    _hitbox = RectangleHitbox(
      position: Vector2.zero(),
      size: size,
    );
    add(_hitbox);

    // Auto-load animations via gameRef if not injected via constructor
    if (runAnimation == null) {
      try {
        runAnimation = await gameRef.loadSpriteAnimation(
          'spritesheet_ninja_run.png',
          SpriteAnimationData.sequenced(
            amount: 5,
            stepTime: 0.08,
            textureSize: Vector2(128, 128),
          ),
        );
        _runTicker = runAnimation?.createTicker();
      } catch (_) {}
    }

    if (idleAnimation == null) {
      try {
        idleAnimation = await gameRef.loadSpriteAnimation(
          'spritesheet_ninja_idle.png',
          SpriteAnimationData.sequenced(
            amount: 4,
            stepTime: 0.16,
            textureSize: Vector2(128, 128),
          ),
        );
        _idleTicker = idleAnimation?.createTicker();
      } catch (_) {}
    }

    if (jumpAnimation == null) {
      try {
        jumpAnimation = await gameRef.loadSpriteAnimation(
          'spritesheet_ninja_jump.png',
          SpriteAnimationData.sequenced(
            amount: 4,
            stepTime: 0.12,
            textureSize: Vector2(128, 128),
            loop: false,
          ),
        );
        _jumpTicker = jumpAnimation?.createTicker();
      } catch (_) {}
    }

    if (attackAnimation == null) {
      try {
        attackAnimation = await gameRef.loadSpriteAnimation(
          'spritesheet_ninja_attack.png',
          SpriteAnimationData.sequenced(
            amount: 4,
            stepTime: 0.08,
            textureSize: Vector2(128, 128),
            loop: false,
          ),
        );
        _attackTicker = attackAnimation?.createTicker();
      } catch (_) {}
    }

    if (deathAnimation == null) {
      try {
        deathAnimation = await gameRef.loadSpriteAnimation(
          'spritesheet_ninja_death.png',
          SpriteAnimationData.sequenced(
            amount: 4,
            stepTime: 0.15,
            textureSize: Vector2(128, 128),
            loop: false,
          ),
        );
        _deathTicker = deathAnimation?.createTicker();
      } catch (_) {}
    }
  }

  @override
  bool onKeyEvent(KeyEvent event, Set<LogicalKeyboardKey> keysPressed) {
    if (isDead) return true;

    _horizontalInput = 0;
    if (keysPressed.contains(LogicalKeyboardKey.keyA) ||
        keysPressed.contains(LogicalKeyboardKey.arrowLeft)) {
      _horizontalInput -= 1;
    }
    if (keysPressed.contains(LogicalKeyboardKey.keyD) ||
        keysPressed.contains(LogicalKeyboardKey.arrowRight)) {
      _horizontalInput += 1;
    }

    final isDownPressed = keysPressed.contains(LogicalKeyboardKey.keyS) ||
        keysPressed.contains(LogicalKeyboardKey.arrowDown);
    final isJumpPressed = keysPressed.contains(LogicalKeyboardKey.space) ||
        keysPressed.contains(LogicalKeyboardKey.keyW) ||
        keysPressed.contains(LogicalKeyboardKey.arrowUp);

    if (isDownPressed && isJumpPressed) {
      dropDown();
    } else if (isJumpPressed) {
      if (event is KeyDownEvent) {
        jump();
      }
    }

    if (keysPressed.contains(LogicalKeyboardKey.keyJ) &&
        event is KeyDownEvent) {
      attack();
    }

    if (keysPressed.contains(LogicalKeyboardKey.keyK) &&
        event is KeyDownEvent) {
      throwShuriken();
    }

    return true;
  }

  // Virtual control hooks for mobile touch & web UI
  void moveLeft() {
    if (isDead) return;
    _horizontalInput = -1;
  }

  void moveRight() {
    if (isDead) return;
    _horizontalInput = 1;
  }

  void stopMoving() {
    if (isDead) return;
    _horizontalInput = 0;
  }

  void jump() {
    if (isDead) return;
    if (isOnGround) {
      velocity.y = jumpImpulse;
      _isOnGround = false;
      _hadGroundCollision = false;
      _currentSlope = null;
      _jumpTicker?.reset();
    }
  }

  void dropDown() {
    if (isDead) return;
    isDroppingThrough = true;
    _dropTimer = 0.28; // Drop through duration
    _isOnGround = false;
    _hadGroundCollision = false;
    _currentSlope = null;
  }

  /// Performs a melee katana slash strike with forward arc effect.
  void attack() {
    if (isDead || isAttacking) return;
    isAttacking = true;
    _attackTimer = 0.28;
    state = NinjaState.attacking;
    _attackTicker?.reset();

    if (parent != null) {
      final slashPos = position + Vector2(isFacingRight ? 16 : -52, -48);
      final slash = KatanaSlash(
        position: slashPos,
        isFacingRight: isFacingRight,
      );
      parent!.add(slash);
    }
  }

  /// Throws a rapidly spinning shuriken projectile in the facing direction.
  void throwShuriken() {
    if (isDead) return;
    if (parent != null) {
      final shurikenPos = position + Vector2(isFacingRight ? 24 : -24, -28);
      final projVelocity = Vector2(isFacingRight ? 650 : -650, 0);
      final proj = ShurikenProjectile(
        position: shurikenPos,
        velocity: projVelocity,
      );
      parent!.add(proj);
    }
  }

  /// Triggers defeat animation, halts controls, and initiates death state.
  void die() {
    if (isDead) return;
    isDead = true;
    state = NinjaState.dead;
    velocity = Vector2(0, -160);
    _horizontalInput = 0;
    _currentSlope = null;
    _deathTicker?.reset();
    _deathTimer = 0.8;
  }

  /// Resets the ninja entity state back to full health and active inputs.
  void reset({Vector2? newPosition}) {
    isDead = false;
    _deathTimer = 0;
    isAttacking = false;
    _attackTimer = 0;
    isDroppingThrough = false;
    _dropTimer = 0;
    _horizontalInput = 0;
    _currentSlope = null;
    state = NinjaState.idle;
    velocity = Vector2.zero();
    if (newPosition != null) {
      position = newPosition.clone();
    }
    _isOnGround = true;
    _deathTicker?.reset();
    _idleTicker?.reset();
  }

  @override
  void update(double dt) {
    super.update(dt);

    if (isDead) {
      _deathTimer -= dt;
      _deathTicker?.update(dt);
      velocity.y += gravity * dt;
      position.y += velocity.y * dt;
      if (_deathTimer <= 0) {
        onHazardHit?.call();
      }
      return;
    }

    if (isDroppingThrough) {
      _dropTimer -= dt;
      if (_dropTimer <= 0) {
        isDroppingThrough = false;
      }
    }

    if (isAttacking) {
      _attackTimer -= dt;
      if (_attackTimer <= 0) {
        isAttacking = false;
      }
      _attackTicker?.update(dt);
    }

    // Apply horizontal input
    velocity.x = _horizontalInput * horizontalSpeed;

    // Flip sprite depending on horizontal movement
    if (velocity.x > 0 && !isFacingRight) {
      isFacingRight = true;
    } else if (velocity.x < 0 && isFacingRight) {
      isFacingRight = false;
    }

    // Edge-fall check with grace frames to prevent 1-frame sub-pixel
    // ground drop oscillation:
    if (_isOnGround && !_hadGroundCollision && !isDroppingThrough) {
      _groundGraceFrames++;
      if (_groundGraceFrames > 2) {
        _isOnGround = false;
      }
    } else if (_hadGroundCollision) {
      _groundGraceFrames = 0;
    }
    _hadGroundCollision = false;

    // Apply gravity only when truly airborne
    if (!_isOnGround) {
      velocity.y += gravity * dt;
    } else {
      velocity.y = 0;
    }

    // Update position
    position
      ..x += velocity.x * dt
      ..y += velocity.y * dt;

    // Smooth slope ramp adherence for stairs and inclines
    if (_isOnGround && _currentSlope != null) {
      if (_currentSlope!.containsX(position.x)) {
        final rampY = _currentSlope!.getYAt(position.x);
        position.y = rampY.roundToDouble();
        velocity.y = 0;
      } else {
        _currentSlope = null;
      }
    }

    // Pixel snapping when standing still on the ground:
    // Snaps coordinates to whole numbers to eliminate sub-pixel jitter.
    if (_isOnGround && _horizontalInput == 0) {
      velocity.x = 0;
      velocity.y = 0;
      position.x = position.x.roundToDouble();
      position.y = position.y.roundToDouble();
    }

    // Update animation state and advance the appropriate ticker
    if (isAttacking) {
      state = NinjaState.attacking;
    } else if (!_isOnGround) {
      if (velocity.y < 0) {
        state = NinjaState.leaping;
      } else {
        state = NinjaState.falling;
      }
      _jumpTicker?.update(dt);
    } else if (velocity.x.abs() > 10) {
      state = NinjaState.running;
      _runTicker?.update(dt);
    } else {
      state = NinjaState.idle;
      _idleTicker?.update(dt);
    }

    // Leaping aesthetic rotation when in mid-air
    if (!_isOnGround) {
      final leapAngle =
          (velocity.y < 0 ? -0.12 : 0.08) * (isFacingRight ? 1 : -1);
      angle = leapAngle;
    } else {
      angle = 0;
    }

    // World floor safeguard
    if (position.y > 600) {
      die();
    }
  }

  @override
  void onCollision(Set<Vector2> intersectionPoints, PositionComponent other) {
    super.onCollision(intersectionPoints, other);

    if (isDead) return;

    final playerBottom = position.y;
    final playerLeft = position.x - size.x / 2 + 6;
    final playerRight = position.x + size.x / 2 - 6;

    if (other is SpiritOrbComponent) {
      other.collect();
    } else if (other is SpikeHazardComponent ||
        other is ShurikenHazardComponent ||
        (other is FeudalFoe && !other.isDefeated)) {
      die();
    } else if (other is SlopePlatformComponent) {
      // Continuous diagonal slope ramp for stairs
      if (velocity.y >= 0 && !isDroppingThrough) {
        final rampY = other.getYAt(position.x);
        if (playerBottom <= rampY + 22 && playerBottom >= rampY - 20) {
          position.y = rampY.roundToDouble();
          velocity.y = 0;
          isOnGround = true;
          _currentSlope = other;
        }
      }
    } else if (other is PlatformComponent) {
      // One-way jump-through platform logic:
      if (velocity.y >= 0 && !isDroppingThrough) {
        final platformTop = other.absolutePosition.y;
        if (playerBottom <= platformTop + 18 &&
            playerBottom >= platformTop - 14) {
          position.y = platformTop.roundToDouble();
          velocity.y = 0;
          isOnGround = true;
        }
      }
    } else if (other is GroundBlockComponent || other is StonePillarComponent) {
      // Solid obstacle collision
      final otherTop = other.absolutePosition.y;
      final otherLeft = other.absolutePosition.x;
      final otherRight = otherLeft + other.size.x;

      // Vertical landing
      if (velocity.y >= 0 &&
          playerBottom <= otherTop + 18 &&
          playerBottom >= otherTop - 12 &&
          playerRight > otherLeft + 2 &&
          playerLeft < otherRight - 2) {
        position.y = otherTop.roundToDouble();
        velocity.y = 0;
        isOnGround = true;
      }
    }
  }

  @override
  void render(Canvas canvas) {
    // 1. Soft grounded contact shadow beneath the ninja's feet
    // Positioned directly at (0, 0) for seamless ground contact
    if (_isOnGround) {
      final shadowPaint = Paint()
        ..color = const Color(0x66000000)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 2);
      canvas.drawOval(
        Rect.fromCenter(
          center: Offset.zero,
          width: 28,
          height: 6,
        ),
        shadowPaint,
      );
    }

    canvas.save();
    if (!isFacingRight) {
      canvas.scale(-1, 1);
    }

    Sprite? spriteToRender;
    if (isDead) {
      spriteToRender = _deathTicker?.getSprite() ?? ninjaSprite;
    } else if (isAttacking) {
      spriteToRender = _attackTicker?.getSprite() ?? ninjaSprite;
    } else if (!isOnGround) {
      spriteToRender = _jumpTicker?.getSprite() ?? ninjaSprite;
    } else if (velocity.x.abs() > 10) {
      spriteToRender = _runTicker?.getSprite() ?? ninjaSprite;
    } else {
      spriteToRender = _idleTicker?.getSprite() ?? ninjaSprite;
    }

    if (spriteToRender != null) {
      // Bilinear filtering and exact ground-aligned pixel snapping.
      // The 128x128 sprite rendered at 64x64 has feet at y = 61px down.
      // Offset by -61.0px so the feet land PRECISELY at y = 0 with 0px float!
      final paint = Paint()
        ..filterQuality = FilterQuality.medium
        ..isAntiAlias = true;

      const visualWidth = 64.0;
      const visualHeight = 64.0;
      final drawX = (-visualWidth / 2).roundToDouble();
      const drawY = -61.0;

      spriteToRender.render(
        canvas,
        position: Vector2(drawX, drawY),
        size: Vector2(visualWidth, visualHeight),
        overridePaint: paint,
      );
    }
    canvas.restore();
  }
}
