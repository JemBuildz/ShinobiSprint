import 'dart:async';
import 'dart:ui';

import 'package:flame/components.dart';
import 'package:flutter/foundation.dart';
import 'package:super_dash/game/components/elevated_platform.dart';
import 'package:super_dash/game/components/katana_slash.dart';
import 'package:super_dash/game/components/ninja_item.dart';
import 'package:super_dash/game/components/shuriken_projectile.dart';
import 'package:super_dash/game/shinobi_sprint_game.dart';

/// Available states and animation mappings for [NinjaPlayer].
enum NinjaState {
  /// Running along the ground.
  running,

  /// In the air leaping or falling.
  jumping,

  /// Performing a katana slash strike.
  attacking,
}

/// A temporary visual effect spawned when the ninja jumps.
class NinjaJumpEffect extends PositionComponent {
  /// Creates a [NinjaJumpEffect] at the specified [position].
  NinjaJumpEffect({
    required Vector2 position,
    this.lifetime = 0.4,
  }) : super(position: position, size: Vector2(32, 16));

  /// How long the effect lasts before auto-removal.
  final double lifetime;
  double _elapsed = 0;

  @override
  void update(double dt) {
    super.update(dt);
    _elapsed += dt;
    if (_elapsed >= lifetime) {
      removeFromParent();
    }
  }
}

/// The interactive Ninja player character for Shinobi Sprint.
class NinjaPlayer extends SpriteAnimationGroupComponent<NinjaState>
    with HasGameReference {
  /// Creates a new [NinjaPlayer] instance.
  NinjaPlayer({
    super.position,
    Vector2? size,
    this.groundY,
    this.floorBaselineY,
    this.footOffset = 2.0,
    this.horizontalHitboxInset = 17.0,
    this.topHitboxInset = 11.0,
    this.gravity = 1200,
    this.jumpVelocity = -600,
    this.onItemCollected,
    super.animations,
  }) : super(
          size: size ?? Vector2.all(64),
        );

  /// Callback triggered when this player collects a [NinjaItem].
  final void Function(NinjaItem item)? onItemCollected;

  /// Downward gravitational acceleration in pixels/s^2.
  final double gravity;

  /// Upward impulse velocity applied when jumping.
  final double jumpVelocity;

  /// Calibrated foot baseline offset from the sprite frame bottom in pixels.
  /// Matches spritesheet content baseline (y=62 of 64px frame).
  final double footOffset;

  /// Horizontal inset from the frame edges to the actual physical body hitbox.
  /// The 64px sprite has ~17px margins, centering a ~30px ninja silhouette.
  final double horizontalHitboxInset;

  /// Top inset from the frame top to the ninja's head.
  final double topHitboxInset;

  /// The left coordinate of the physical body hitbox.
  double get hitboxLeft => position.x + horizontalHitboxInset;

  /// The right coordinate of the physical body hitbox.
  double get hitboxRight => position.x + size.x - horizontalHitboxInset;

  /// The width of the physical body hitbox.
  double get hitboxWidth => size.x - (horizontalHitboxInset * 2);

  /// The physical bounding rectangle of the character body.
  Rect get physicalHitbox => Rect.fromLTWH(
        hitboxLeft,
        position.y + topHitboxInset,
        hitboxWidth,
        size.y - topHitboxInset - footOffset,
      );

  /// The Y coordinate representing the current platform or ground level.
  double? groundY;

  /// The continuous solid floor baseline below which the player never falls,
  /// guaranteeing the ninja never falls off the screen or into an abyss.
  double? floorBaselineY;

  /// Calculates the Y coordinate where the ninja's feet contact the ground.
  double get footPositionY => position.y + size.y - footOffset;

  /// Velocity vector of the player character.
  Vector2 velocity = Vector2.zero();

  /// Vertical velocity of the character.
  double get verticalVelocity => velocity.y;
  set verticalVelocity(double value) => velocity.y = value;

  /// Active temporary jump effects spawned by this player.
  final List<Component> _temporaryJumpEffects = [];

  /// Visible list of temporary jump effects for testing and verification.
  @visibleForTesting
  List<Component> get temporaryJumpEffects =>
      List.unmodifiable(_temporaryJumpEffects);

  /// Active katana slashes spawned by this player.
  final List<KatanaSlash> _activeSlashes = [];

  /// Active katana slashes visible for testing.
  @visibleForTesting
  List<KatanaSlash> get activeSlashes => List.unmodifiable(_activeSlashes);

  /// Active shuriken projectiles spawned by this player.
  final List<ShurikenProjectile> _activeShurikens = [];

  /// Active shuriken projectiles visible for testing.
  @visibleForTesting
  List<ShurikenProjectile> get activeShurikens =>
      List.unmodifiable(_activeShurikens);

  /// How long the katana slash animation and hitbox remains active.
  double attackDuration = 0.28;
  double _attackTimer = 0;

  /// Whether the ninja is currently performing an attack.
  bool get isAttacking => current == NinjaState.attacking;

  /// The active elevated platform the player is currently standing on, if any.
  ElevatedPlatform? currentPlatform;

  /// Whether the ninja is currently in the air jumping.
  bool get isJumping =>
      current == NinjaState.jumping ||
      (groundY != null && position.y < groundY!);

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    if (animations == null || animations!.isEmpty) {
      final runImage = await game.images.load('spritesheet_ninja_run.png');
      final jumpImage = await game.images.load(
        'spritesheet_ninja_jump.png',
      );
      final attackImage = await game.images.load(
        'spritesheet_ninja_attack.png',
      );

      final runAnimation = SpriteAnimation.fromFrameData(
        runImage,
        SpriteAnimationData.sequenced(
          amount: 5,
          stepTime: 0.1,
          textureSize: Vector2(64, 64),
        ),
      );

      final jumpAnimation = SpriteAnimation.fromFrameData(
        jumpImage,
        SpriteAnimationData.sequenced(
          amount: 4,
          stepTime: 0.12,
          textureSize: Vector2(64, 64),
          loop: false,
        ),
      );

      final attackAnimation = SpriteAnimation.fromFrameData(
        attackImage,
        SpriteAnimationData.sequenced(
          amount: 4,
          stepTime: 0.07,
          textureSize: Vector2(64, 64),
          loop: false,
        ),
      );

      animations = {
        NinjaState.running: runAnimation,
        NinjaState.jumping: jumpAnimation,
        NinjaState.attacking: attackAnimation,
      };
    }

    current ??= NinjaState.running;
    groundY ??= position.y;
    floorBaselineY ??= groundY;
  }

  /// Triggers the jump logic, applying upward velocity to the ninja character.
  void jump() {
    velocity.y = jumpVelocity;
    current = NinjaState.jumping;
    currentPlatform = null;
    animationTicker?.reset();

    // Spawn a temporary jump effect
    final effect = NinjaJumpEffect(position: position.clone());
    _temporaryJumpEffects.add(effect);
    parent?.add(effect);
  }

  /// Triggers a melee katana strike, spawning a slash arc and dealing damage.
  void katanaSlash() {
    attack();
  }

  /// Performs a katana attack in the current movement direction.
  void attack() {
    current = NinjaState.attacking;
    animationTicker?.reset();
    _attackTimer = 0.0;

    // Spawn a katana slash arc slightly in front of the ninja
    final slash = KatanaSlash(
      position: Vector2(
        position.x + size.x * 0.5,
        position.y + (size.y - 56) * 0.5,
      ),
    );
    _activeSlashes.add(slash);
    parent?.add(slash);
  }

  /// Throws a rapidly spinning shuriken projectile forward.
  ShurikenProjectile throwShuriken({Vector2? velocity}) {
    final projectile = ShurikenProjectile(
      position: Vector2(
        position.x + size.x * 0.85,
        position.y + size.y * 0.45,
      ),
      velocity: velocity,
    );
    _activeShurikens.add(projectile);
    parent?.add(projectile);
    return projectile;
  }

  @override
  void update(double dt) {
    super.update(dt);

    // Handle attack timer completion and transition back to running or jumping
    if (isAttacking) {
      _attackTimer += dt;
      if (_attackTimer >= attackDuration) {
        _attackTimer = 0.0;
        final currentGround = groundY;
        if (currentGround != null && position.y < currentGround) {
          current = NinjaState.jumping;
        } else {
          current = NinjaState.running;
        }
      }
    }

    // Apply downward gravitational acceleration when airborne
    if (isJumping) {
      velocity.y += gravity * dt;
    }

    // Vertical velocity variable tracking character physics
    final verticalVelocity = velocity.y;
    this.verticalVelocity = verticalVelocity;

    // Update physical location over time inside the game loop
    position += velocity * dt;

    // Check one-way elevated platforms when descending
    if (velocity.y >= 0) {
      final platforms = game.children.whereType<ElevatedPlatform>();
      final playerLeft = hitboxLeft;
      final playerRight = hitboxRight;
      final feetY = footPositionY;

      ElevatedPlatform? landed;
      for (final p in platforms) {
        if (playerRight > p.leftX && playerLeft < p.rightX) {
          if (feetY >= p.surfaceY - 4 && feetY <= p.surfaceY + 18) {
            landed = p;
            break;
          }
        }
      }

      if (landed != null) {
        currentPlatform = landed;
        position.y = landed.surfaceY - (size.y - footOffset);
        groundY = position.y;
        velocity.y = 0;
        if (current != NinjaState.running) {
          current = NinjaState.running;
        }
      } else if (currentPlatform != null) {
        if (playerRight <= currentPlatform!.leftX ||
            playerLeft >= currentPlatform!.rightX) {
          currentPlatform = null;
          groundY = floorBaselineY;
        }
      }
    }

    // Handle ground landing and safety baseline against falling off screen
    final currentGround = groundY;
    final floorLimit = floorBaselineY ?? currentGround;

    if (floorLimit != null && position.y > floorLimit) {
      // Safety: Never fall below continuous boardwalk floor baseline
      position.y = floorLimit;
      groundY = floorLimit;
      currentPlatform = null;
      velocity.y = 0;
      if (current != NinjaState.running) {
        current = NinjaState.running;
      }
    } else if (currentGround != null && position.y >= currentGround) {
      position.y = currentGround;
      velocity.y = 0;
      if (current != NinjaState.running) {
        current = NinjaState.running;
      }
    }

    // Check collectible item pickups
    _updateItemPickups();
  }

  void _updateItemPickups() {
    final game = findGame();
    if (game == null) return;

    final items = game.children.whereType<NinjaItem>();
    if (items.isEmpty) return;

    final playerRect = physicalHitbox;
    for (final item in items) {
      if (item.isCollected) continue;
      if (playerRect.overlaps(item.toRect())) {
        item.collect();
        onItemCollected?.call(item);
        if (game is ShinobiSprintGame) {
          game.onItemCollected(item);
        }
      }
    }
  }

  @override
  void onRemove() {
    // Facilitate necessary cleanup and dispose of temporary jump effects
    // and combat effects.
    for (final effect in _temporaryJumpEffects) {
      if (effect.isMounted) {
        effect.removeFromParent();
      }
    }
    _temporaryJumpEffects.clear();

    for (final slash in _activeSlashes) {
      if (slash.isMounted) {
        slash.removeFromParent();
      }
    }
    _activeSlashes.clear();

    for (final shuriken in _activeShurikens) {
      if (shuriken.isMounted) {
        shuriken.removeFromParent();
      }
    }
    _activeShurikens.clear();

    super.onRemove();
  }
}
