import 'package:firebase_auth/firebase_auth.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:super_dash/ui/overlays/auth_overlay.dart';
import 'package:super_dash/ui/theme/app_theme.dart';

/// {@template clan_auth_badge}
/// HUD profile badge displaying the ninja's clan authentication status.
/// Tapping the badge opens the feudal [AuthOverlay].
/// {@endtemplate}
class ClanAuthBadge extends StatelessWidget {
  /// {@macro clan_auth_badge}
  const ClanAuthBadge({
    super.key,
    this.game,
    this.onTap,
    this.auth,
  });

  /// Optional Flame game reference to trigger overlay display.
  final FlameGame? game;

  /// Optional custom callback when tapped.
  final VoidCallback? onTap;

  /// Optional FirebaseAuth instance for testing.
  final FirebaseAuth? auth;

  void _handleTap(BuildContext context) {
    if (onTap != null) {
      onTap!();
    } else if (game != null) {
      game!.overlays.add(AuthOverlay.id);
    } else {
      showDialog<void>(
        context: context,
        barrierColor: Colors.black54,
        builder: (ctx) => AuthOverlay(
          onClose: () => Navigator.of(ctx).pop(),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    Stream<User?>? authStream;
    try {
      final firebaseAuth = auth ?? FirebaseAuth.instance;
      authStream = firebaseAuth.authStateChanges();
    } catch (_) {
      authStream = const Stream.empty();
    }

    return StreamBuilder<User?>(
      stream: authStream,
      builder: (context, snapshot) {
        final user = snapshot.data;
        final isAuthenticated = user != null && !user.isAnonymous;
        final displayName = isAuthenticated
            ? (user.displayName ??
                user.email?.split('@').first ??
                'Shinobi')
            : 'GUEST CLAN';

        return Material(
          color: Colors.transparent,
          child: InkWell(
            onTap: () => _handleTap(context),
            borderRadius: BorderRadius.circular(24),
            child: Container(
              padding: const EdgeInsets.symmetric(
                horizontal: 12,
                vertical: 6,
              ),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(24),
                gradient: const LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    Color(0xF0090D1A),
                    Color(0xF01E293B),
                  ],
                ),
                border: Border.all(
                  color: AppTheme.antiqueGold,
                  width: 1.4,
                ),
                boxShadow: const [
                  BoxShadow(
                    color: Colors.black45,
                    blurRadius: 8,
                    offset: Offset(0, 2),
                  ),
                  BoxShadow(
                    color: Color(0x33FFA726),
                    blurRadius: 6,
                    spreadRadius: -1,
                  ),
                ],
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                    width: 20,
                    height: 20,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      gradient: LinearGradient(
                        colors: isAuthenticated
                            ? const [
                                AppTheme.lacquerRed,
                                AppTheme.lacquerCrimson,
                              ]
                            : const [
                                Color(0xFF4A3425),
                                Color(0xFF2C1E15),
                              ],
                      ),
                      border: Border.all(
                        color: isAuthenticated
                            ? AppTheme.goldLeaf
                            : AppTheme.antiqueGold,
                      ),
                    ),
                    child: Text(
                      isAuthenticated ? '忍' : '？',
                      style: const TextStyle(
                        color: AppTheme.goldLeaf,
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    displayName.toUpperCase(),
                    style: const TextStyle(
                      color: AppTheme.parchmentCream,
                      fontSize: 11,
                      fontWeight: FontWeight.w700,
                      letterSpacing: 1.1,
                      shadows: [
                        Shadow(
                          color: Color(0x80FFA726),
                          blurRadius: 4,
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 4),
                  Icon(
                    isAuthenticated
                        ? Icons.verified_user_rounded
                        : Icons.login_rounded,
                    color: isAuthenticated
                        ? AppTheme.goldLeaf
                        : AppTheme.lanternAmber,
                    size: 14,
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
