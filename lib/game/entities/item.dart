import 'dart:async';

import 'package:flame/components.dart';
import 'package:flame/effects.dart';
import 'package:flame_tiled/flame_tiled.dart';
import 'package:flutter/material.dart';
import 'package:leap/leap.dart';
import 'package:super_dash/game/super_dash_game.dart';

enum ItemType {
  shuriken(10),
  sushi(1000),
  magatama(500),
  ofuda(250),
  goldenFeather(0);

  const ItemType(this.points);

  final int points;

  /// Backwards compatibility aliases
  static const ItemType acorn = shuriken;
  static const ItemType egg = sushi;

  static ItemType fromType(String? type) {
    if (type == 'Sushi' || type == 'Egg') {
      return ItemType.sushi;
    } else if (type == 'Magatama') {
      return ItemType.magatama;
    } else if (type == 'Ofuda') {
      return ItemType.ofuda;
    } else if (type == 'Feather' || type == 'GoldenFeather') {
      return ItemType.goldenFeather;
    } else if (type == 'Shuriken' || type == 'Acorn') {
      return ItemType.shuriken;
    }
    return ItemType.shuriken;
  }
}

class Item extends PhysicalEntity<SuperDashGame> {
  Item({
    required this.tiledObject,
  }) : super(static: true, collisionType: CollisionType.standard);

  late final ItemType type;
  late final TiledObject tiledObject;

  @override
  int get priority => 2;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    type = ItemType.fromType(
      (tiledObject.properties.byName['Type'] as StringProperty?)?.value,
    );

    size = Vector2.all(gameRef.tileSize);
    position = Vector2(tiledObject.x, tiledObject.y);

    if (type == ItemType.sushi) {
      final sushiAnimation = await gameRef.loadSpriteAnimation(
        'anim/spritesheet_item_sushi.png',
        SpriteAnimationData.sequenced(
          amount: 48,
          amountPerRow: 8,
          textureSize: Vector2.all(gameRef.tileSize),
          stepTime: .042,
        ),
      );
      add(
        SpriteAnimationComponent(
          animation: sushiAnimation,
          size: size,
        ),
      );
    } else if (type == ItemType.shuriken) {
      final shurikenAnimation = await gameRef.loadSpriteAnimation(
        'anim/spritesheet_item_shuriken.png',
        SpriteAnimationData.sequenced(
          amount: 48,
          amountPerRow: 8,
          textureSize: Vector2.all(gameRef.tileSize),
          stepTime: .042,
        ),
      );
      add(
        SpriteAnimationComponent(
          animation: shurikenAnimation,
          size: size,
        ),
      );
    } else if (type == ItemType.goldenFeather) {
      final featherAnimation = await gameRef.loadSpriteAnimation(
        'anim/spritesheet_item_feather.png',
        SpriteAnimationData.sequenced(
          amount: 30,
          amountPerRow: 6,
          textureSize: Vector2.all(gameRef.tileSize),
          stepTime: .042,
        ),
      );
      add(
        SpriteAnimationComponent(
          animation: featherAnimation,
          size: size,
        ),
      );
    } else {
      add(
        SpriteComponent(
          size: size,
          sprite: gameRef.itemsSpritesheet.getSpriteById(
            (tiledObject.gid ?? 0) - gameRef.itemsTileset.firstGid!,
          ),
          children: [
            SequenceEffect(
              [
                MoveEffect.by(
                  -Vector2(0, gameRef.tileSize / 2),
                  CurvedEffectController(.8, Curves.easeIn),
                ),
                MoveEffect.by(
                  Vector2(0, gameRef.tileSize / 2),
                  CurvedEffectController(.8, Curves.easeOut),
                ),
              ],
              infinite: true,
            ),
          ],
        ),
      );
    }
  }
}

/// Collectible Shuriken component (formerly Acorn).
class Shuriken extends Item {
  Shuriken({required super.tiledObject});
}

/// Collectible Sushi component (formerly Egg).
class Sushi extends Item {
  Sushi({required super.tiledObject});
}

/// Backwards compatibility aliases
typedef Acorn = Shuriken;
typedef Egg = Sushi;
