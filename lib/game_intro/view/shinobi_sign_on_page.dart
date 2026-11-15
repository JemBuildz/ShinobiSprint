import 'dart:math' as math;

import 'package:authentication_repository/authentication_repository.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:super_dash/game_intro/game_intro.dart';
import 'package:super_dash/settings/settings_controller.dart';

/// The Shinobi Sprint Sign-On screen shown right after the initial
/// splash loading screen.
class ShinobiSignOnPage extends StatefulWidget {
  const ShinobiSignOnPage({super.key});

  static PageRoute<void> route() {
    return PageRouteBuilder<void>(
      pageBuilder: (context, animation, secondaryAnimation) =>
          const ShinobiSignOnPage(),
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        return FadeTransition(opacity: animation, child: child);
      },
    );
  }

  @override
  State<ShinobiSignOnPage> createState() => _ShinobiSignOnPageState();
}

class _ShinobiSignOnPageState extends State<ShinobiSignOnPage>
    with SingleTickerProviderStateMixin {
  late final AnimationController _petalController;
  final List<_PetalData> _petals = [];
  bool _isSigningIn = false;
  String? _signingInLabel;

  @override
  void initState() {
    super.initState();
    _petalController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 10),
    )..repeat();

    final rand = math.Random();
    for (var i = 0; i < 18; i++) {
      _petals.add(
        _PetalData(
          x: rand.nextDouble(),
          y: rand.nextDouble(),
          speed: 0.15 + rand.nextDouble() * 0.25,
          size: 6.0 + rand.nextDouble() * 8.0,
          rotation: rand.nextDouble() * 2 * math.pi,
          rotationSpeed: (rand.nextDouble() - 0.5) * 2.0,
          opacity: 0.35 + rand.nextDouble() * 0.45,
        ),
      );
    }
  }

  @override
  void dispose() {
    _petalController.dispose();
    super.dispose();
  }

  Future<void> _handleSignIn({
    required String providerName,
    required Future<void> Function() action,
  }) async {
    if (_isSigningIn) return;

    setState(() {
      _isSigningIn = true;
      _signingInLabel = providerName;
    });

    try {
      await action();
      if (!mounted) return;
      await Future<void>.delayed(const Duration(milliseconds: 350));
      if (!mounted) return;
      await Navigator.of(context).pushReplacement<void, void>(
        ShinobiGameSelectionPage.route(),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Sign in notice: $e'),
          backgroundColor: const Color(0xFFE11D48),
        ),
      );
    } finally {
      if (mounted) {
        setState(() {
          _isSigningIn = false;
          _signingInLabel = null;
        });
      }
    }
  }

  void _onGoogleSignIn() {
    _handleSignIn(
      providerName: 'Google',
      action: () async {
        final authRepo = context.read<AuthenticationRepository>();
        await authRepo.signInAnonymously();
      },
    );
  }

  void _onAppleSignIn() {
    _handleSignIn(
      providerName: 'Apple',
      action: () async {
        final authRepo = context.read<AuthenticationRepository>();
        await authRepo.signInAnonymously();
      },
    );
  }

  void _onGuestSignIn() {
    _handleSignIn(
      providerName: 'Guest',
      action: () async {
        final authRepo = context.read<AuthenticationRepository>();
        await authRepo.signInAnonymously();
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final isLandscape = size.width > size.height;

    return Scaffold(
      backgroundColor: const Color(0xFF0D1322),
      body: Stack(
        fit: StackFit.expand,
        children: [
          // 1. Immersive Vertical Background Artwork
          Image.asset(
            'assets/images/shinobi_sign_on_bg.png',
            fit: BoxFit.cover,
            alignment:
                isLandscape ? const Alignment(-0.35, 0) : Alignment.center,
          ),

          // 2. Depth Vignettes & Atmosphere
          Positioned.fill(
            child: DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    const Color(0xFF0D1322).withValues(alpha: 0.65),
                    Colors.transparent,
                    const Color(0xFF080E1D).withValues(alpha: 0.85),
                    const Color(0xFF080E1D).withValues(alpha: 0.98),
                  ],
                  stops: const [0.0, 0.35, 0.75, 1.0],
                ),
              ),
            ),
          ),

          // 3. Ambient Cherry Blossom Drifting Petals
          AnimatedBuilder(
            animation: _petalController,
            builder: (context, _) {
              return CustomPaint(
                painter: _PetalPainter(
                  petals: _petals,
                  progress: _petalController.value,
                ),
                child: const SizedBox.expand(),
              );
            },
          ),

          // 4. Audio Control Pill (Top Right HUD)
          Positioned(
            top: MediaQuery.of(context).padding.top + 16,
            right: 20,
            child: _AudioToggleButton(),
          ),

          // 5. Interactive Content Canvas
          SafeArea(
            child: isLandscape
                ? _buildLandscapeContent(context)
                : _buildPortraitContent(context),
          ),

          // 6. Loading Barrier during auth
          if (_isSigningIn)
            Container(
              color: Colors.black54,
              alignment: Alignment.center,
              child: Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 24,
                  vertical: 16,
                ),
                decoration: BoxDecoration(
                  color: const Color(0xFF151B2B),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: const Color(0xFF10B981).withValues(alpha: 0.6),
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFF10B981).withValues(alpha: 0.25),
                      blurRadius: 20,
                    ),
                  ],
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2.5,
                        valueColor: AlwaysStoppedAnimation(Color(0xFF10B981)),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Text(
                      _signingInLabel == 'Guest'
                          ? 'ENTERING WORLD...'
                          : 'SIGNING IN VIA $_signingInLabel...',
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                        letterSpacing: 1.2,
                      ),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildLandscapeContent(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
      child: Row(
        children: [
          // Left side: Art breathing room with logo
          Expanded(
            flex: 5,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 380),
                  child: Image.asset(
                    'assets/images/shinobi_sprint_logo.png',
                    fit: BoxFit.contain,
                  ),
                ),
                const SizedBox(height: 14),
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 14, vertical: 5),
                  decoration: BoxDecoration(
                    color: const Color(0xFF10B981).withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(
                      color: const Color(0xFF10B981).withValues(alpha: 0.4),
                    ),
                  ),
                  child: const Text(
                    '⛩️ FEUDAL ADVENTURE AWAITS',
                    style: TextStyle(
                      color: Color(0xFF4EDEA3),
                      fontSize: 12,
                      fontWeight: FontWeight.w700,
                      letterSpacing: 2,
                    ),
                  ),
                ),
              ],
            ),
          ),

          // Right side: Glassmorphic auth card
          Expanded(
            flex: 5,
            child: Center(
              child: SingleChildScrollView(
                child: Container(
                  constraints: const BoxConstraints(maxWidth: 360),
                  padding:
                      const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
                  decoration: BoxDecoration(
                    color: const Color(0xFF151B2B).withValues(alpha: 0.88),
                    borderRadius: BorderRadius.circular(24),
                    border: Border.all(
                      color: Colors.white.withValues(alpha: 0.12),
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.5),
                        blurRadius: 32,
                        offset: const Offset(0, 8),
                      ),
                    ],
                  ),
                  child: _buildAuthButtons(context),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPortraitContent(BuildContext context) {
    return SingleChildScrollView(
      child: ConstrainedBox(
        constraints: BoxConstraints(
          minHeight: MediaQuery.of(context).size.height -
              MediaQuery.of(context).padding.vertical,
        ),
        child: IntrinsicHeight(
          child: Column(
            children: [
              const SizedBox(height: 24),
              // Logo
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 32),
                child: ConstrainedBox(
                  constraints:
                      const BoxConstraints(maxWidth: 320, maxHeight: 130),
                  child: Image.asset(
                    'assets/images/shinobi_sprint_logo.png',
                    fit: BoxFit.contain,
                  ),
                ),
              ),
              const Spacer(),
              // Bottom Authentication Tray
              Padding(
                padding:
                    const EdgeInsets.symmetric(horizontal: 28, vertical: 20),
                child: ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 380),
                  child: _buildAuthButtons(context),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAuthButtons(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Google Sign In
        _SocialAuthButton(
          label: 'Sign in with Google',
          icon: const FaIcon(
            FontAwesomeIcons.google,
            color: Color(0xFF4285F4),
            size: 19,
          ),
          backgroundColor: Colors.white,
          textColor: const Color(0xFF1F2937),
          onPressed: _onGoogleSignIn,
        ),
        const SizedBox(height: 12),

        // Apple Sign In
        _SocialAuthButton(
          label: 'Sign in with Apple',
          icon: const FaIcon(
            FontAwesomeIcons.apple,
            color: Colors.black,
            size: 21,
          ),
          backgroundColor: Colors.white,
          textColor: const Color(0xFF1F2937),
          onPressed: _onAppleSignIn,
        ),
        const SizedBox(height: 14),

        // Play as Guest
        Center(
          child: InkWell(
            onTap: _onGuestSignIn,
            borderRadius: BorderRadius.circular(20),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 8),
              decoration: BoxDecoration(
                color: const Color(0xFF242A3A).withValues(alpha: 0.8),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(
                  color: const Color(0xFF3C4A42).withValues(alpha: 0.7),
                ),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(
                    Icons.play_arrow_rounded,
                    size: 18,
                    color: const Color(0xFF4EDEA3).withValues(alpha: 0.9),
                  ),
                  const SizedBox(width: 6),
                  const Text(
                    'PLAY AS GUEST',
                    style: TextStyle(
                      color: Color(0xFFDDE2F8),
                      fontSize: 12,
                      fontWeight: FontWeight.w700,
                      letterSpacing: 1.5,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        const SizedBox(height: 14),

        // Disclaimer
        const Text(
          "By continuing, you agree to Shinobi Sprint's Terms & Privacy",
          textAlign: TextAlign.center,
          style: TextStyle(
            color: Color(0xFF86948A),
            fontSize: 11,
            height: 1.3,
          ),
        ),
      ],
    );
  }
}

class _SocialAuthButton extends StatelessWidget {
  const _SocialAuthButton({
    required this.label,
    required this.icon,
    required this.backgroundColor,
    required this.textColor,
    required this.onPressed,
  });

  final String label;
  final Widget icon;
  final Color backgroundColor;
  final Color textColor;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: backgroundColor,
        foregroundColor: textColor,
        elevation: 3,
        shadowColor: Colors.black54,
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30),
          side: BorderSide(
            color: Colors.white.withValues(alpha: 0.4),
          ),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        mainAxisSize: MainAxisSize.min,
        children: [
          icon,
          const SizedBox(width: 10),
          Flexible(
            child: Text(
              label,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: TextStyle(
                color: textColor,
                fontSize: 15,
                fontWeight: FontWeight.w600,
                letterSpacing: -0.2,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _AudioToggleButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final settingsController = context.watch<SettingsController>();

    return ValueListenableBuilder<bool>(
      valueListenable: settingsController.muted,
      builder: (context, muted, child) {
        return Material(
          color: Colors.transparent,
          child: InkWell(
            onTap: context.read<SettingsController>().toggleMuted,
            borderRadius: BorderRadius.circular(20),
            child: Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: const Color(0xFF151B2B).withValues(alpha: 0.75),
                shape: BoxShape.circle,
                border: Border.all(
                  color: Colors.white.withValues(alpha: 0.15),
                ),
                boxShadow: const [
                  BoxShadow(
                    color: Colors.black45,
                    blurRadius: 10,
                  ),
                ],
              ),
              child: Icon(
                muted ? Icons.volume_off_rounded : Icons.volume_up_rounded,
                color: muted
                    ? const Color(0xFF86948A)
                    : const Color(0xFFFBBF24),
                size: 20,
              ),
            ),
          ),
        );
      },
    );
  }
}

class _PetalData {
  _PetalData({
    required this.x,
    required this.y,
    required this.speed,
    required this.size,
    required this.rotation,
    required this.rotationSpeed,
    required this.opacity,
  });

  double x;
  double y;
  final double speed;
  final double size;
  double rotation;
  final double rotationSpeed;
  final double opacity;
}

class _PetalPainter extends CustomPainter {
  _PetalPainter({
    required this.petals,
    required this.progress,
  });

  final List<_PetalData> petals;
  final double progress;

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..style = PaintingStyle.fill;

    for (final petal in petals) {
      final currentY = (petal.y + progress * petal.speed) % 1.0;
      final sway = math.sin(progress * 2 * math.pi + petal.x * 10) * 0.03;
      final currentX = (petal.x + sway) % 1.0;

      final px = currentX * size.width;
      final py = currentY * size.height;

      paint.color = const Color(0xFFFF7884).withValues(alpha: petal.opacity);

      canvas
        ..save()
        ..translate(px, py)
        ..rotate(petal.rotation + progress * petal.rotationSpeed * math.pi);

      // Draw petal oval
      final rect = Rect.fromCenter(
        center: Offset.zero,
        width: petal.size,
        height: petal.size * 0.6,
      );
      canvas
        ..drawOval(rect, paint)
        ..restore();
    }
  }

  @override
  bool shouldRepaint(_PetalPainter oldDelegate) => true;
}
