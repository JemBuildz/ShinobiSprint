// ignore_for_file: prefer_const_constructors

import 'package:bloc_test/bloc_test.dart';
import 'package:flame/game.dart' hide Game;
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:super_dash/game/game.dart';
import 'package:super_dash/game_intro/game_intro.dart';
import 'package:super_dash/l10n/l10n.dart';
import 'package:super_dash/settings/settings.dart';

import '../../helpers/helpers.dart';

class _MockGameBloc extends MockBloc<GameEvent, GameState>
    implements GameBloc {}

class _MockSettingsController extends Mock implements SettingsController {}

void main() {
  late SettingsController settingsController;

  setUp(() {
    settingsController = _MockSettingsController();
    when(() => settingsController.muted).thenReturn(ValueNotifier(true));
  });

  group('Game', () {
    test('is routable', () {
      expect(Game.route(), isA<PageRoute<void>>());
    });

    testWidgets('renders GameView', (tester) async {
      await tester.pumpApp(
        Game(),
        settingsController: settingsController,
      );

      expect(find.byType(GameView), findsOneWidget);
    });
  });

  group('GameView', () {
    late GameBloc gameBloc;

    setUp(() => gameBloc = _MockGameBloc());

    Widget buildSubject() {
      return BlocProvider.value(
        value: gameBloc,
        child: const GameView(),
      );
    }

    testWidgets('renders score', (tester) async {
      when(() => gameBloc.state).thenReturn(GameState.initial());

      await tester.pumpApp(
        buildSubject(),
        settingsController: settingsController,
      );

      final context = tester.element(find.byType(ScoreLabel));

      expect(
        find.text(
          context.l10n.gameScoreLabel(gameBloc.state.score),
        ),
        findsOneWidget,
      );
    });

    testWidgets('renders TapToJumpOverlay initially', (tester) async {
      when(() => gameBloc.state).thenReturn(GameState.initial());

      await tester.pumpApp(
        BlocProvider.value(
          value: gameBloc,
          child: GameView(
            gameFactory: (_) => FlameGame(),
          ),
        ),
        settingsController: settingsController,
      );
      await tester.pump();
      await tester.pump();

      expect(find.byType(TapToJumpOverlay), findsOneWidget);
    });

    testWidgets('renders ClanAuthBadge and AudioButton', (tester) async {
      when(() => gameBloc.state).thenReturn(GameState.initial());

      await tester.pumpApp(
        buildSubject(),
        settingsController: settingsController,
      );

      expect(find.byType(AudioButton), findsOneWidget);
    });

    testWidgets('tapping TapToJumpOverlay removes overlay', (tester) async {
      when(() => gameBloc.state).thenReturn(GameState.initial());

      await tester.pumpApp(
        BlocProvider.value(
          value: gameBloc,
          child: GameView(
            gameFactory: (_) => FlameGame(),
          ),
        ),
        settingsController: settingsController,
      );
      await tester.pump();
      await tester.pump();

      expect(find.byType(TapToJumpOverlay), findsOneWidget);

      await tester.tap(find.byType(TapToJumpOverlay));
      await tester.pump();

      expect(find.byType(TapToJumpOverlay), findsNothing);
    });
  });
}
