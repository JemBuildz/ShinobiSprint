import 'dart:async';

import 'package:flame/cache.dart';
import 'package:flame/components.dart';
import 'package:flame/effects.dart';
import 'package:flutter/animation.dart';
import 'package:super_dash/game/entities/item.dart';

/// A collectible item in Shinobi Sprint (Sushi or Shuriken).
class NinjaItem extends PositionComponent with HasGameReference {
  /// Creates a [NinjaItem] with the given [type] and [position].
  NinjaItem({
    required this.type,
    super.position,
    Vector2? size,
    this.enableBobbing = true,
    this.animation,
  }) : super(
          size: size ?? Vector2.all(64),
        );

  /// Convenience constructor for a Sushi collectible item (1000 pts).
  NinjaItem.sushi({
    Vector2? position,
    Vector2? size,
    bool enableBobbing = true,
    SpriteAnimation? animation,
  }) : this(
          type: ItemType.sushi,
          position: position,
          size: size,
          enableBobbing: enableBobbing,
          animation: animation,
        );

  /// Convenience constructor for a Shuriken collectible item (10 pts).
  NinjaItem.shuriken({
    Vector2? position,
    Vector2? size,
    bool enableBobbing = true,
    SpriteAnimation? animation,
  }) : this(
          type: ItemType.shuriken,
          position: position,
          size: size,
          enableBobbing: enableBobbing,
          animation: animation,
        );

  /// Convenience constructor for a Magatama gemstone collectible (500 pts).
  NinjaItem.magatama({
    Vector2? position,
    Vector2? size,
    bool enableBobbing = true,
    SpriteAnimation? animation,
  }) : this(
          type: ItemType.magatama,
          position: position,
          size: size,
          enableBobbing: enableBobbing,
          animation: animation,
        );

  /// Convenience constructor for an Ofuda talisman collectible (250 pts).
  NinjaItem.ofuda({
    Vector2? position,
    Vector2? size,
    bool enableBobbing = true,
    SpriteAnimation? animation,
  }) : this(
          type: ItemType.ofuda,
          position: position,
          size: size,
          enableBobbing: enableBobbing,
          animation: animation,
        );

  /// Optional preloaded [SpriteAnimation] to render.
  final SpriteAnimation? animation;

  /// The type of item (e.g. [ItemType.sushi] or [ItemType.shuriken]).
  final ItemType type;

  /// Whether to play a gentle vertical bobbing animation.
  final bool enableBobbing;

  /// Whether this item has already been collected.
  bool get isCollected => _isCollected;
  bool _isCollected = false;

  /// Animated sprite component displaying the item visual.
  SpriteAnimationComponent? animationComponent;

  static final _mapImages = Images(prefix: 'assets/map/');

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    if (animation != null) {
      final comp = SpriteAnimationComponent(
        animation: animation,
        size: size,
      );
      animationComponent = comp;
      await add(comp);
    } else if (type == ItemType.magatama || type == ItemType.ofuda) {
      try {
        final itemAsset = type == ItemType.magatama
            ? 'items/magatama_gem.png'
            : 'items/ofuda_talisman.png';
        final img = await game.images.load(itemAsset);
        final spriteComp = SpriteComponent(
          sprite: Sprite(img),
          size: size,
        );
        await add(spriteComp);
      } catch (_) {
        // In headless test environments
      }
    } else {
      try {
        final animationPath = type == ItemType.sushi
            ? 'anim/spritesheet_item_sushi.png'
            : 'anim/spritesheet_item_shuriken.png';

        final img = await _mapImages.load(animationPath);
        final anim = SpriteAnimation.fromFrameData(
          img,
          SpriteAnimationData.sequenced(
            amount: 48,
            amountPerRow: 8,
            textureSize: Vector2.all(64),
            stepTime: 0.042,
          ),
        );

        final comp = SpriteAnimationComponent(
          animation: anim,
          size: size,
        );
        animationComponent = comp;
        await add(comp);
      } catch (_) {
        // In headless test environments, sprite assets may not be loaded.
      }
    }

    if (enableBobbing) {
      add(
        SequenceEffect(
          [
            MoveEffect.by(
              Vector2(0, -6),
              CurvedEffectController(0.8, Curves.easeInOut),
            ),
            MoveEffect.by(
              Vector2(0, 6),
              CurvedEffectController(0.8, Curves.easeInOut),
            ),
          ],
          infinite: true,
        ),
      );
    }
  }

  /// Marks this item as collected and removes it from the game tree.
  void collect() {
    if (_isCollected) return;
    _isCollected = true;
    removeFromParent();
  }
}
