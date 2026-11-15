import 'package:flutter/material.dart';
import 'package:super_dash/l10n/l10n.dart';

import 'package:super_dash/ui/theme/app_theme.dart';

class TapToJumpOverlay extends StatelessWidget {
  const TapToJumpOverlay({super.key, this.onTap});

  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    final textTheme = Theme.of(context).textTheme;

    return SafeArea(
      child: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: onTap,
        child: Center(
          child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(30),
            gradient: const LinearGradient(
              colors: [
                Color(0xEE090D1A), // midnight indigo
                Color(0xEE1E293B), // mountain ridge nocturnal blue
              ],
            ),
            border: Border.all(
              color: AppTheme.antiqueGold,
              width: 1.8,
            ),
            boxShadow: const [
              BoxShadow(
                color: Colors.black54,
                blurRadius: 16,
                offset: Offset(0, 4),
              ),
              BoxShadow(
                color: Color(0x40FFA726), // warm lantern amber glow
                blurRadius: 10,
              ),
            ],
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            child: Text(
              l10n.tapToStart,
              style: textTheme.titleLarge?.copyWith(
                color: AppTheme.parchmentCream,
                fontWeight: FontWeight.bold,
                letterSpacing: 1.5,
                shadows: const [
                  Shadow(
                    color: Color(0x80FFB74D),
                    blurRadius: 8,
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    ),
  );
}
}
