import 'dart:async';

import 'package:flame/cache.dart';
import 'package:flame/components.dart';
import 'package:flame/game.dart';
import 'package:super_dash/game/entities/item.dart';
import 'package:super_dash/game/shinobi_sprint_game.dart';
import 'package:super_dash/game/super_dash_game.dart';

class ItemEffect extends SpriteAnimationComponent
    with HasGameReference<FlameGame> {
  ItemEffect({
    required this.type,
    super.position,
    super.animation,
  }) : super(removeOnFinish: true, priority: 22);

  final ItemType type;

  static final _mapImages = Images(prefix: 'assets/map/');

  @override
  FutureOr<void> onLoad() async {
    await super.onLoad();

    if (animation != null) {
      if (type == ItemType.sushi) {
        size = Vector2.all(192);
        anchor = Anchor.center;
      } else {
        size = Vector2.all(64);
      }
      return;
    }

    try {
      if (type == ItemType.sushi) {
        final img = await _mapImages.load('anim/spritesheet_fx_large.png');
        animation = SpriteAnimation.fromFrameData(
          img,
          SpriteAnimationData.sequenced(
            amount: 14,
            amountPerRow: 7,
            textureSize: Vector2.all(192),
            stepTime: .042,
            loop: false,
          ),
        );
        size = Vector2.all(192);
        anchor = Anchor.center;
      } else if (type == ItemType.goldenFeather) {
        final img = await _mapImages.load('anim/spritesheet_poof_orange.png');
        animation = SpriteAnimation.fromFrameData(
          img,
          SpriteAnimationData.sequenced(
            amount: 20,
            amountPerRow: 5,
            textureSize: Vector2.all(192),
            stepTime: .042,
            loop: false,
          ),
        );
        size = Vector2.all(192);
        anchor = Anchor.center;
      } else {
        final img = await _mapImages.load('anim/spritesheet_fx_small.png');
        animation = SpriteAnimation.fromFrameData(
          img,
          SpriteAnimationData.sequenced(
            amount: 9,
            amountPerRow: 3,
            textureSize: Vector2.all(64),
            stepTime: .042,
            loop: false,
          ),
        );
        size = Vector2.all(64);
      }
    } catch (_) {
      // In headless test environments, sprite assets may not be loaded.
      size = type == ItemType.sushi ? Vector2.all(192) : Vector2.all(64);
    }
  }

  @override
  void update(double dt) {
    super.update(dt);


    final currentGame = game;
    Vector2? targetPos;
    if (currentGame is SuperDashGame) {
      targetPos = currentGame.player?.position;
    } else if (currentGame is ShinobiSprintGame) {
      targetPos = currentGame.ninjaPlayer.position;
    }

    if (targetPos != null) {
      position = targetPos;
    }
  }
}
