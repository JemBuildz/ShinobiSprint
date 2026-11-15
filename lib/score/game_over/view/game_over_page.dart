import 'package:app_ui/app_ui.dart';
import 'package:flow_builder/flow_builder.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:intl/intl.dart';
import 'package:super_dash/game/game.dart';
import 'package:super_dash/game_intro/game_intro.dart';
import 'package:super_dash/gen/assets.gen.dart';
import 'package:super_dash/l10n/l10n.dart';
import 'package:super_dash/score/score.dart';
import 'package:super_dash/ui/theme/app_theme.dart';
import 'package:super_dash/utils/utils.dart';

class GameOverPage extends StatelessWidget {
  const GameOverPage({super.key});

  static Page<void> page() {
    return const MaterialPage(
      child: GameOverPage(),
    );
  }

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    final textTheme = Theme.of(context).textTheme;
    const titleColor = AppTheme.parchmentGold;

    return PageWithBackground(
      background: const GameBackground(),
      child: DecoratedBox(
        decoration: BoxDecoration(
          image: DecorationImage(
            image: Assets.images.gameOverBg.provider(),
            fit: BoxFit.cover,
            alignment:
                isDesktop ? const Alignment(0, -.5) : Alignment.topCenter,
          ),
        ),
        child: Column(
          children: [
            const Spacer(flex: 15),
            Text(
              l10n.gameOver,
              style: textTheme.headlineMedium?.copyWith(
                color: titleColor,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              l10n.betterLuckNextTime,
              style: textTheme.bodyLarge?.copyWith(
                color: titleColor,
              ),
            ),
            const Spacer(flex: 4),
            Text(
              l10n.totalScore,
              style: textTheme.bodyLarge?.copyWith(
                color: titleColor,
                fontWeight: FontWeight.bold,
              ),
            ),
            const Spacer(flex: 2),
            const _ScoreWidget(),
            const Spacer(flex: 4),
            GameElevatedButton(
              label: l10n.submitScore,
              gradient: AppTheme.lacquerButtonGradient,
              onPressed: () {
                context.read<ScoreBloc>().add(const ScoreSubmitted());
              },
            ),
            const Spacer(flex: 3),
            GameElevatedButton.icon(
              label: l10n.playAgain,
              icon: const Icon(Icons.refresh, size: 16),
              onPressed: context.flow<ScoreState>().complete,
              gradient: AppTheme.lanternFlameGradient,
            ),
            const Spacer(flex: 40),
            const BottomBar(),
            const SizedBox(height: 16),
          ],
        ),
      ),
    );
  }
}

class _ScoreWidget extends StatelessWidget {
  const _ScoreWidget();

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    final textTheme = Theme.of(context).textTheme;
    final score = context.select((ScoreBloc bloc) => bloc.score);

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
      decoration: BoxDecoration(
        gradient: AppTheme.woodPlaqueGradient,
        borderRadius: BorderRadius.circular(100),
        border: Border.all(
          color: AppTheme.antiqueGold,
          width: 1.5,
        ),
        boxShadow: const [
          BoxShadow(
            color: Colors.black54,
            blurRadius: 10,
            offset: Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Assets.images.trophy.image(width: 40, height: 40),
          const SizedBox(width: 8),
          RichText(
            text: TextSpan(
              style: textTheme.headlineMedium?.copyWith(
                color: AppTheme.goldLeaf,
                fontWeight: FontWeight.bold,
              ),
              children: [
                TextSpan(text: '${formatScore(score)} '),
                TextSpan(
                  text: l10n.pts,
                  style: const TextStyle(
                    fontSize: 24,
                    color: AppTheme.parchmentCream,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  String formatScore(int score) {
    final formatter = NumberFormat('#,###');
    return formatter.format(score);
  }
}
