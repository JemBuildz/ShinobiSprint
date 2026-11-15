import 'package:app_ui/app_ui.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:super_dash/game/bloc/game_bloc.dart';
import 'package:super_dash/gen/assets.gen.dart';
import 'package:super_dash/l10n/l10n.dart';

import 'package:super_dash/ui/theme/app_theme.dart';

class ScoreLabel extends StatelessWidget {
  const ScoreLabel({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    final textTheme = Theme.of(context).textTheme;
    final score = context.select(
      (GameBloc bloc) => bloc.state.score,
    );

    return SafeArea(
      child: TraslucentBackground(
        shape: BoxShape.rectangle,
        borderRadius: BorderRadius.circular(30),
        border: Border.all(
          color: AppTheme.antiqueGold,
          width: 1.5,
        ),
        gradient: const [
          Color(0xF0090D1A), // deep night sky indigo
          Color(0xF01E293B), // mountain nocturnal blue
        ],
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          child: Row(
            children: [
              Assets.images.trophy.image(
                width: 36,
                height: 36,
              ),
              const SizedBox(width: 10),
              Text(
                l10n.gameScoreLabel(score),
                style: textTheme.titleLarge?.copyWith(
                  color: AppTheme.lanternCoreGlow,
                  fontWeight: FontWeight.bold,
                  shadows: const [
                    Shadow(
                      color: Color(0x99FFA726), // glowing lantern amber shadow
                      blurRadius: 8,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
