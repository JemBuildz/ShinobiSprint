import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:super_dash/audio/audio.dart';
import 'package:super_dash/game/game.dart';
import 'package:super_dash/game_intro/game_intro.dart';
import 'package:super_dash/ui/overlays/auth_overlay.dart';
import 'package:super_dash/ui/widgets/clan_auth_badge.dart';

class Game extends StatelessWidget {
  const Game({super.key, this.gameFactory});

  final FlameGame Function(BuildContext context)? gameFactory;

  static PageRoute<void> route({
    FlameGame Function(BuildContext context)? gameFactory,
  }) {
    return PageRouteBuilder(
      pageBuilder: (_, __, ___) => Game(gameFactory: gameFactory),
    );
  }

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => GameBloc(),
      child: GameView(gameFactory: gameFactory),
    );
  }
}

class GameView extends StatelessWidget {
  const GameView({super.key, this.gameFactory});

  final FlameGame Function(BuildContext context)? gameFactory;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        alignment: Alignment.center,
        children: [
          GameWidget.controlled(
            loadingBuilder: (context) => const GameBackground(),
            backgroundBuilder: (context) => const GameBackground(),
            gameFactory: () =>
                gameFactory?.call(context) ??
                SuperDashGame(
                  gameBloc: context.read<GameBloc>(),
                  audioController: context.read<AudioController>(),
                ),
            overlayBuilderMap: {
              'tapToJump': (context, game) => TapToJumpOverlay(
                    onTap: () {
                      if (game is FlameGame) {
                        game.overlays.remove('tapToJump');
                      }
                      if (game is SuperDashGame &&
                          (game.player?.isMounted ?? false)) {
                        game.player?.walking = true;
                        game.player?.jumping = true;
                      } else if (game is ShinobiSprintGame &&
                          game.ninjaPlayer.isMounted) {
                        game.ninjaPlayer.jump();
                      }
                    },
                  ),
              'ninjaControls': (context, game) => NinjaActionControls(
                    isDaytime: (game is SuperDashGame && game.isDaytime) ||
                        (game is ShinobiSprintGame && game.isDaytime),
                    onJump: () {
                      if (game is SuperDashGame) {
                        if (game.player?.isMounted ?? false) {
                          if (!game.player!.walking) {
                            game.player!.walking = true;
                          } else if (game.player!.isOnGround) {
                            game.player!
                              ..jumpEffects()
                              ..jumping = true;
                          }
                        }
                      } else if (game is ShinobiSprintGame &&
                          game.ninjaPlayer.isMounted) {
                        game.ninjaPlayer.jump();
                      }
                    },
                    onSlash: () {
                      if (game is SuperDashGame) {
                        game.player?.katanaSlash();
                      } else if (game is ShinobiSprintGame) {
                        game.ninjaPlayer.katanaSlash();
                      }
                    },
                    onThrowShuriken: () {
                      if (game is SuperDashGame) {
                        game.player?.throwShuriken();
                      } else if (game is ShinobiSprintGame) {
                        game.ninjaPlayer.throwShuriken();
                      }
                    },
                    onToggleDayNight: () {
                      if (game is SuperDashGame) {
                        game.toggleDayNight();
                      } else if (game is ShinobiSprintGame) {
                        game.toggleDayNight();
                      }
                    },
                  ),
              AuthOverlay.id: (context, game) => AuthOverlay(
                    game: game is FlameGame ? game : null,
                    isDaytime: game is ShinobiSprintGame && game.isDaytime,
                  ),
              AuthOverlay.overlayKey: (context, game) => AuthOverlay(
                    game: game is FlameGame ? game : null,
                    isDaytime: game is ShinobiSprintGame && game.isDaytime,
                  ),
            },
            initialActiveOverlays: const ['tapToJump', 'ninjaControls'],
          ),
          const Positioned(
            top: 12,
            child: ScoreLabel(),
          ),
          const Positioned(
            top: 12,
            right: 16,
            child: SafeArea(
              child: ClanAuthBadge(),
            ),
          ),
          const Positioned(
            bottom: 12,
            child: SafeArea(child: AudioButton()),
          ),
        ],
      ),
    );
  }
}
