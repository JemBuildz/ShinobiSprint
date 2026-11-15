import 'package:flutter/material.dart';
import 'package:super_dash/ui/theme/app_theme.dart';

/// Neo-feudal touch action controls providing mobile/touchscreen players
/// with responsive on-screen buttons for combat actions
/// (Katana Slash, Shuriken) and atmospheric day/night toggling.
class NinjaActionControls extends StatelessWidget {
  const NinjaActionControls({
    super.key,
    this.onJump,
    this.onSlash,
    this.onThrowShuriken,
    this.onToggleDayNight,
    this.isDaytime = false,
  });

  /// Callback when the Jump button is pressed.
  final VoidCallback? onJump;

  /// Callback when the Katana Slash button is pressed.
  final VoidCallback? onSlash;

  /// Callback when the Shuriken Throw button is pressed.
  final VoidCallback? onThrowShuriken;

  /// Callback when the Day/Night theme toggle is pressed.
  final VoidCallback? onToggleDayNight;

  /// Whether daytime mode is active.
  final bool isDaytime;

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            // Left Side: Day / Night Theme Toggle
            if (onToggleDayNight != null)
              _ThemeToggleButton(
                isDaytime: isDaytime,
                onPressed: onToggleDayNight!,
              )
            else
              const SizedBox.shrink(),

            // Right Side: Combat & Mobility (Jump, Shuriken, Slash)
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                if (onJump != null) ...[
                  _ActionButton(
                    key: const Key('ninja_action_jump_button'),
                    label: '▲',
                    subtitle: 'JUMP',
                    glowColor: AppTheme.goldLeaf,
                    borderColor: AppTheme.goldLeaf,
                    onPressed: onJump!,
                  ),
                  const SizedBox(width: 14),
                ],
                if (onThrowShuriken != null) ...[
                  _ActionButton(
                    key: const Key('ninja_action_shuriken_button'),
                    label: '✦',
                    subtitle: 'SHURIKEN',
                    glowColor: AppTheme.celestialCyan,
                    borderColor: AppTheme.celestialCyan,
                    onPressed: onThrowShuriken!,
                  ),
                  const SizedBox(width: 14),
                ],
                if (onSlash != null)
                  _ActionButton(
                    key: const Key('ninja_action_slash_button'),
                    label: '⚔',
                    subtitle: 'SLASH',
                    glowColor: AppTheme.lacquerRed,
                    borderColor: AppTheme.antiqueGold,
                    onPressed: onSlash!,
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _ActionButton extends StatelessWidget {
  const _ActionButton({
    required this.label,
    required this.subtitle,
    required this.glowColor,
    required this.borderColor,
    required this.onPressed,
    super.key,
  });

  final String label;
  final String subtitle;
  final Color glowColor;
  final Color borderColor;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => onPressed(),
      child: Container(
        width: 60,
        height: 60,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          gradient: const RadialGradient(
            colors: [
              Color(0xFA1E293B),
              Color(0xFA090D1A),
            ],
          ),
          border: Border.all(
            color: borderColor,
            width: 2,
          ),
          boxShadow: [
            BoxShadow(
              color: glowColor.withValues(alpha: 0.55),
              blurRadius: 10,
              spreadRadius: 1,
            ),
            const BoxShadow(
              color: Colors.black87,
              blurRadius: 6,
              offset: Offset(0, 3),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              label,
              style: TextStyle(
                color: borderColor,
                fontSize: 22,
                height: 1,
                fontWeight: FontWeight.bold,
                shadows: [
                  Shadow(
                    color: glowColor,
                    blurRadius: 8,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 2),
            Text(
              subtitle,
              style: const TextStyle(
                color: AppTheme.parchmentGold,
                fontSize: 8,
                letterSpacing: 0.8,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ThemeToggleButton extends StatelessWidget {
  const _ThemeToggleButton({
    required this.isDaytime,
    required this.onPressed,
  });

  final bool isDaytime;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      key: const Key('ninja_action_theme_toggle_button'),
      onTap: onPressed,
      child: Container(
        width: 44,
        height: 44,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: const Color(0xDD0F172A),
          border: Border.all(
            color: isDaytime ? AppTheme.goldLeaf : AppTheme.celestialCyan,
            width: 1.5,
          ),
          boxShadow: [
            BoxShadow(
              color: isDaytime
                  ? AppTheme.lanternAmber.withValues(alpha: 0.4)
                  : AppTheme.celestialCyan.withValues(alpha: 0.3),
              blurRadius: 8,
            ),
          ],
        ),
        child: Icon(
          isDaytime ? Icons.wb_sunny_rounded : Icons.nightlight_round,
          color: isDaytime ? AppTheme.goldLeaf : AppTheme.parchmentCream,
          size: 20,
        ),
      ),
    );
  }
}
