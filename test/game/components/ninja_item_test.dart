import 'package:flame/game.dart';
import 'package:flame_test/flame_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:super_dash/audio/audio.dart';
import 'package:super_dash/game/bloc/game_bloc.dart';
import 'package:super_dash/game/components/item_effect.dart';
import 'package:super_dash/game/components/ninja_item.dart';
import 'package:super_dash/game/components/ninja_player.dart';
import 'package:super_dash/game/entities/item.dart';
import 'package:super_dash/game/shinobi_sprint_game.dart';

class _MockAudioController extends Mock implements AudioController {}

class _TestGame extends FlameGame {}

class _TestItemEffect extends ItemEffect {
  _TestItemEffect({required super.type, super.position});

  @override
  Future<void> onLoad() async {}
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() {
    registerFallbackValue(Sfx.jump);
  });

  group('NinjaItem', () {
    test('initializes sushi item with correct defaults and points', () {
      final item = NinjaItem.sushi(
        position: Vector2(100, 200),
      );

      expect(item.type, equals(ItemType.sushi));
      expect(item.type.points, equals(1000));
      expect(item.position, equals(Vector2(100, 200)));
      expect(item.size, equals(Vector2.all(64)));
      expect(item.isCollected, isFalse);
    });

    test('initializes shuriken item with correct defaults and points', () {
      final item = NinjaItem.shuriken(
        position: Vector2(150, 250),
      );

      expect(item.type, equals(ItemType.shuriken));
      expect(item.type.points, equals(10));
      expect(item.position, equals(Vector2(150, 250)));
      expect(item.size, equals(Vector2.all(64)));
      expect(item.isCollected, isFalse);
    });

    test('initializes magatama item with correct defaults and 500 points', () {
      final item = NinjaItem.magatama(
        position: Vector2(120, 220),
      );

      expect(item.type, equals(ItemType.magatama));
      expect(item.type.points, equals(500));
      expect(item.position, equals(Vector2(120, 220)));
      expect(item.isCollected, isFalse);
    });

    test('initializes ofuda item with correct defaults and 250 points', () {
      final item = NinjaItem.ofuda(
        position: Vector2(180, 280),
      );

      expect(item.type, equals(ItemType.ofuda));
      expect(item.type.points, equals(250));
      expect(item.position, equals(Vector2(180, 280)));
      expect(item.isCollected, isFalse);
    });

    testWithGame(
      'collect() marks item as collected and removes from parent',
      _TestGame.new,
      (game) async {
        final item = NinjaItem.shuriken(position: Vector2(10, 10));
        await game.add(item);
        await game.ready();

        expect(item.isMounted, isTrue);
        expect(item.isCollected, isFalse);

        item.collect();
        expect(item.isCollected, isTrue);

        game.update(0.1);
        expect(item.isMounted, isFalse);
      },
    );

    testWithGame(
      'NinjaPlayer collision collects NinjaItem and invokes onItemCollected',
      _TestGame.new,
      (game) async {
        NinjaItem? collected;
        final item = NinjaItem.sushi(position: Vector2(100, 100));
        final player = NinjaPlayer(
          position: Vector2(100, 100),
          groundY: 100,
          onItemCollected: (it) => collected = it,
        );

        await game.add(item);
        await game.add(player);
        await game.ready();

        expect(item.isCollected, isFalse);
        player.update(0.016);

        expect(item.isCollected, isTrue);
        expect(collected, equals(item));
      },
    );

    testWithGame(
      'Item pickup in ShinobiSprintGame increases GameBloc score, '
      'plays audio SFX, and spawns ItemEffect',
      () {
        final audio = _MockAudioController();
        when(() => audio.playSfx(any())).thenReturn(null);
        final gameBloc = GameBloc();

        return ShinobiSprintGame(
          audioController: audio,
          gameBloc: gameBloc,
          itemEffectFactory: (type, pos) => _TestItemEffect(
            type: type,
            position: pos,
          ),
        );
      },
      (game) async {
        await game.ready();

        final initialScore = game.gameBloc!.state.score;
        final sushiItem = NinjaItem.sushi(
          position: Vector2(100, game.ninjaPlayer.position.y),
        );
        await game.add(sushiItem);
        await game.ready();

        // Position ninja directly on sushi item
        game.ninjaPlayer.position = sushiItem.position.clone();
        game.update(0.016);
        await game.ready();
        await pumpEventQueue();

        expect(sushiItem.isCollected, isTrue);
        expect(game.gameBloc!.state.score, equals(initialScore + 1000));
        verify(() => game.audioController!.playSfx(Sfx.sushiPickup)).called(1);

        // Verify ItemEffect was added to the game
        expect(game.children.whereType<ItemEffect>().isNotEmpty, isTrue);
      },
    );

    testWithGame(
      'Shuriken pickup in ShinobiSprintGame adds 10 points and plays '
      'shuriken SFX',
      () {
        final audio = _MockAudioController();
        when(() => audio.playSfx(any())).thenReturn(null);
        final gameBloc = GameBloc();

        return ShinobiSprintGame(
          audioController: audio,
          gameBloc: gameBloc,
        );
      },
      (game) async {
        await game.ready();

        final initialScore = game.gameBloc!.state.score;
        final shurikenItem = NinjaItem.shuriken(
          position: Vector2(100, game.ninjaPlayer.position.y),
        );
        await game.add(shurikenItem);
        await game.ready();

        game.ninjaPlayer.position = shurikenItem.position.clone();
        game.update(0.016);
        await pumpEventQueue();

        expect(shurikenItem.isCollected, isTrue);
        expect(game.gameBloc!.state.score, equals(initialScore + 10));
        verify(
          () => game.audioController!.playSfx(Sfx.shurikenPickup),
        ).called(1);
      },
    );
  });
}
