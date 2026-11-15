import 'dart:ui' as ui;

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:sign_in_with_apple/sign_in_with_apple.dart';
import 'package:super_dash/ui/theme/app_theme.dart';

/// {@template auth_overlay}
/// Feudal Japan wooden ninja-themed authentication overlay for Shinobi Sprint.
/// Integrates Email/Password, Google Sign-In, and Apple Sign-In.
/// {@endtemplate}
class AuthOverlay extends StatefulWidget {
  /// {@macro auth_overlay}
  const AuthOverlay({
    super.key,
    this.game,
    this.onClose,
    this.onSignInSuccess,
    this.onSignInWithEmail,
    this.onSignInWithGoogle,
    this.onSignInWithApple,
    this.isDaytime = false,
  });

  /// The overlay key identifier in Flame's overlay map.
  static const String id = 'auth';

  /// Alternative overlay key name.
  static const String overlayKey = 'auth_overlay';

  /// Optional Flame game reference to dismiss overlay.
  final FlameGame? game;

  /// Whether the overlay is rendered with daytime sunlight parchment palette
  /// or night-time lantern cedar aesthetic.
  final bool isDaytime;

  /// Callback when the overlay is closed.
  final VoidCallback? onClose;

  /// Callback after a successful authentication.
  final VoidCallback? onSignInSuccess;

  /// Custom handler for email and password authentication.
  final Future<void> Function(String email, String password)?
      onSignInWithEmail;

  /// Custom handler for Google Sign-In.
  final Future<void> Function()? onSignInWithGoogle;

  /// Custom handler for Apple Sign-In.
  final Future<void> Function()? onSignInWithApple;

  @override
  State<AuthOverlay> createState() => _AuthOverlayState();
}

class _AuthOverlayState extends State<AuthOverlay> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _emailController;
  late final TextEditingController _passwordController;

  bool _obscurePassword = true;
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _emailController = TextEditingController();
    _passwordController = TextEditingController();
    try {
      widget.game?.pauseEngine();
    } catch (_) {}
  }

  @override
  void dispose() {
    try {
      widget.game?.resumeEngine();
    } catch (_) {}
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _dismissOverlay() {
    try {
      widget.game?.resumeEngine();
    } catch (_) {}
    if (widget.onClose != null) {
      widget.onClose!();
    } else if (widget.game != null) {
      widget.game!.overlays.remove(AuthOverlay.id);
      widget.game!.overlays.remove(AuthOverlay.overlayKey);
    }
  }

  Future<void> _handleEmailSignIn() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final email = _emailController.text.trim();
    final password = _passwordController.text;

    try {
      if (widget.onSignInWithEmail != null) {
        await widget.onSignInWithEmail!(email, password);
      } else {
        await FirebaseAuth.instance.signInWithEmailAndPassword(
          email: email,
          password: password,
        );
      }
      widget.onSignInSuccess?.call();
      _dismissOverlay();
    } on FirebaseAuthException catch (e) {
      setState(() {
        _errorMessage = e.message ?? 'Authentication failed.';
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'An unexpected error occurred. Please try again.';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _handleGoogleSignIn() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      if (widget.onSignInWithGoogle != null) {
        await widget.onSignInWithGoogle!();
      } else {
        final googleSignIn = GoogleSignIn();
        final googleUser = await googleSignIn.signIn();
        if (googleUser != null) {
          final googleAuth = await googleUser.authentication;
          final credential = GoogleAuthProvider.credential(
            accessToken: googleAuth.accessToken,
            idToken: googleAuth.idToken,
          );
          await FirebaseAuth.instance.signInWithCredential(credential);
        }
      }
      widget.onSignInSuccess?.call();
      _dismissOverlay();
    } on FirebaseAuthException catch (e) {
      setState(() {
        _errorMessage = e.message ?? 'Google Sign-In failed.';
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Google Sign-In was cancelled or failed.';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _handleAppleSignIn() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      if (widget.onSignInWithApple != null) {
        await widget.onSignInWithApple!();
      } else {
        final credential = await SignInWithApple.getAppleIDCredential(
          scopes: [
            AppleIDAuthorizationScopes.email,
            AppleIDAuthorizationScopes.fullName,
          ],
        );
        final oauthCredential = OAuthProvider('apple.com').credential(
          idToken: credential.identityToken,
          accessToken: credential.authorizationCode,
        );
        await FirebaseAuth.instance.signInWithCredential(oauthCredential);
      }
      widget.onSignInSuccess?.call();
      _dismissOverlay();
    } on FirebaseAuthException catch (e) {
      setState(() {
        _errorMessage = e.message ?? 'Apple Sign-In failed.';
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Apple Sign-In was cancelled or failed.';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Material(
      type: MaterialType.transparency,
      child: Center(
        child: BackdropFilter(
          filter: ui.ImageFilter.blur(sigmaX: 4, sigmaY: 4),
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 420),
              child: _WoodenPlaqueContainer(
              onClose: _dismissOverlay,
              isDaytime: widget.isDaytime,
              child: Form(
                key: _formKey,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const _NinjaHeaderBanner(),
                    const SizedBox(height: 16),
                    if (_errorMessage != null) ...[
                      _NinjaErrorBanner(message: _errorMessage!),
                      const SizedBox(height: 14),
                    ],
                    _FeudalTextField(
                      controller: _emailController,
                      label: 'Email Address',
                      hintText: 'ninja@shinobi.clan',
                      icon: Icons.alternate_email_rounded,
                      keyboardType: TextInputType.emailAddress,
                      enabled: !_isLoading,
                      validator: (value) {
                        if (value == null || value.trim().isEmpty) {
                          return 'Please enter your ninja scroll email';
                        }
                        if (!value.contains('@') || !value.contains('.')) {
                          return 'Enter a valid email address';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 14),
                    _FeudalTextField(
                      controller: _passwordController,
                      label: 'Password',
                      hintText: '••••••••',
                      icon: Icons.lock_outline_rounded,
                      obscureText: _obscurePassword,
                      enabled: !_isLoading,
                      trailing: IconButton(
                        icon: Icon(
                          _obscurePassword
                              ? Icons.visibility_off_outlined
                              : Icons.visibility_outlined,
                          color: const Color(0xFFC5A059),
                          size: 20,
                        ),
                        onPressed: () {
                          setState(() {
                            _obscurePassword = !_obscurePassword;
                          });
                        },
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter your shinobi secret key';
                        }
                        if (value.length < 6) {
                          return 'Password must be at least 6 characters';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 22),
                    _NinjaSignInButton(
                      label: 'SIGN IN',
                      isLoading: _isLoading,
                      onPressed: _isLoading ? null : _handleEmailSignIn,
                    ),
                    const SizedBox(height: 20),
                    const _FeudalDivider(text: 'OR JOIN CLAN VIA'),
                    const SizedBox(height: 16),
                    _SocialSignInButton(
                      label: 'Sign in with Google',
                      icon: const FaIcon(
                        FontAwesomeIcons.google,
                        color: Color(0xFFEA4335),
                        size: 18,
                      ),
                      backgroundColor: const Color(0xFF2A170B),
                      borderColor: const Color(0xFF8B5A2B),
                      textColor: const Color(0xFFFFF6E5),
                      enabled: !_isLoading,
                      onPressed: _handleGoogleSignIn,
                    ),
                    const SizedBox(height: 10),
                    _SocialSignInButton(
                      label: 'Sign in with Apple',
                      icon: const FaIcon(
                        FontAwesomeIcons.apple,
                        color: Colors.white,
                        size: 18,
                      ),
                      backgroundColor: const Color(0xFF140F0A),
                      borderColor: const Color(0xFF5D4037),
                      textColor: Colors.white,
                      enabled: !_isLoading,
                      onPressed: _handleAppleSignIn,
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    ),
    );
  }
}

/// A container with dark cedar wood grain framing and antique golden lacquer.
class _WoodenPlaqueContainer extends StatelessWidget {
  const _WoodenPlaqueContainer({
    required this.child,
    required this.onClose,
    this.isDaytime = false,
  });

  final Widget child;
  final VoidCallback onClose;
  final bool isDaytime;

  @override
  Widget build(BuildContext context) {
    return Material(
      type: MaterialType.transparency,
      child: Container(
        decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(18),
        gradient: isDaytime
            ? const LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [
                  Color(0xFF5D4037),
                  Color(0xFF4E342E),
                  Color(0xFF3E2723),
                ],
              )
            : AppTheme.woodPlaqueGradient,
        border: Border.all(
          color: AppTheme.antiqueGold,
          width: 2.5,
        ),
        boxShadow: [
          const BoxShadow(
            color: Colors.black87,
            blurRadius: 28,
            spreadRadius: 3,
            offset: Offset(0, 10),
          ),
          BoxShadow(
            color: isDaytime
                ? const Color(0x4DFFD54F) // sunlight gold aura
                : const Color(0x4DFF9800), // glowing lantern orange aura
            blurRadius: 14,
            spreadRadius: -1,
          ),
        ],
      ),
      child: Stack(
        children: [
          // Inner carved wood border bevel
          Positioned.fill(
            child: Container(
              margin: const EdgeInsets.all(5),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(14),
                border: Border.all(
                  color: const Color(0xFF5A3819),
                  width: 1.5,
                ),
              ),
            ),
          ),
          // Close button
          Positioned(
            top: 10,
            right: 10,
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: onClose,
                borderRadius: BorderRadius.circular(20),
                child: Container(
                  padding: const EdgeInsets.all(6),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: const Color(0xFF211107),
                    border: Border.all(
                      color: const Color(0xFFC5A059),
                      width: 1.2,
                    ),
                  ),
                  child: const Icon(
                    Icons.close,
                    color: Color(0xFFE5C158),
                    size: 18,
                  ),
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(22, 24, 22, 24),
            child: child,
          ),
        ],
      ),
    ),
  );
}
}

/// Header banner displaying the ninja emblem and Shinobi Sprint styling.
class _NinjaHeaderBanner extends StatelessWidget {
  const _NinjaHeaderBanner();

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Kanji emblem badge
        Container(
          width: 48,
          height: 48,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: const LinearGradient(
              colors: [
                Color(0xFF8B1E0F),
                Color(0xFF5A0808),
              ],
            ),
            border: Border.all(
              color: const Color(0xFFFFD54F),
              width: 2,
            ),
            boxShadow: const [
              BoxShadow(
                color: Color(0x66B71C1C),
                blurRadius: 10,
                offset: Offset(0, 3),
              ),
            ],
          ),
          child: const Text(
            '忍',
            style: TextStyle(
              color: Color(0xFFFFE082),
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        const SizedBox(height: 10),
        const Text(
          'SHINOBI SPRINT',
          textAlign: TextAlign.center,
          style: TextStyle(
            color: Color(0xFFFFDF7D),
            fontSize: 20,
            fontWeight: FontWeight.w900,
            letterSpacing: 3,
            shadows: [
              Shadow(
                blurRadius: 4,
                offset: Offset(1, 2),
              ),
            ],
          ),
        ),
        const SizedBox(height: 4),
        const Text(
          'CLAN AUTHENTICATION',
          textAlign: TextAlign.center,
          style: TextStyle(
            color: Color(0xFFD7BA89),
            fontSize: 11,
            fontWeight: FontWeight.w700,
            letterSpacing: 2.2,
          ),
        ),
        const SizedBox(height: 10),
        const Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              '❖ ──────── ✦ ──────── ❖',
              style: TextStyle(
                color: Color(0xFF9E783D),
                fontSize: 10,
                letterSpacing: 1.5,
              ),
            ),
          ],
        ),
      ],
    );
  }
}

/// Carved wooden slot input field matching feudal Japanese aesthetic.
class _FeudalTextField extends StatelessWidget {
  const _FeudalTextField({
    required this.controller,
    required this.label,
    required this.hintText,
    required this.icon,
    this.obscureText = false,
    this.trailing,
    this.validator,
    this.keyboardType,
    this.enabled = true,
  });

  final TextEditingController controller;
  final String label;
  final String hintText;
  final IconData icon;
  final bool obscureText;
  final Widget? trailing;
  final String? Function(String?)? validator;
  final TextInputType? keyboardType;
  final bool enabled;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(
              icon,
              size: 14,
              color: const Color(0xFFE5C158),
            ),
            const SizedBox(width: 6),
            Text(
              label.toUpperCase(),
              style: const TextStyle(
                color: Color(0xFFE6C687),
                fontSize: 11.5,
                fontWeight: FontWeight.w700,
                letterSpacing: 1.3,
              ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(10),
            color: const Color(0xFF1B0E06),
            boxShadow: const [
              BoxShadow(
                color: Colors.black54,
                blurRadius: 4,
                offset: Offset(0, 2),
              ),
            ],
          ),
          child: TextFormField(
            controller: controller,
            obscureText: obscureText,
            keyboardType: keyboardType,
            enabled: enabled,
            validator: validator,
            style: const TextStyle(
              color: Color(0xFFFFF8E7),
              fontSize: 14.5,
              fontWeight: FontWeight.w500,
            ),
            cursorColor: const Color(0xFFFFD54F),
            decoration: InputDecoration(
              isDense: true,
              hintText: hintText,
              hintStyle: const TextStyle(
                color: Color(0xFF826952),
                fontSize: 13.5,
              ),
              contentPadding: const EdgeInsets.symmetric(
                horizontal: 14,
                vertical: 13,
              ),
              suffixIcon: trailing,
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
                borderSide: const BorderSide(
                  color: Color(0xFF6B421E),
                  width: 1.4,
                ),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
                borderSide: const BorderSide(
                  color: AppTheme.lanternAmber,
                  width: 1.8,
                ),
              ),
              errorBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
                borderSide: const BorderSide(
                  color: Color(0xFFD32F2F),
                  width: 1.4,
                ),
              ),
              focusedErrorBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(10),
                borderSide: const BorderSide(
                  color: Color(0xFFFF5252),
                  width: 1.8,
                ),
              ),
              errorStyle: const TextStyle(
                color: Color(0xFFFF8A80),
                fontSize: 11,
              ),
            ),
          ),
        ),
      ],
    );
  }
}

/// Primary Japanese warrior lacquer-red "SIGN IN" button.
class _NinjaSignInButton extends StatelessWidget {
  const _NinjaSignInButton({
    required this.label,
    required this.isLoading,
    required this.onPressed,
  });

  final String label;
  final bool isLoading;
  final VoidCallback? onPressed;

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 48,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        gradient: LinearGradient(
          colors: onPressed != null
              ? const [
                  Color(0xFFB71C1C),
                  Color(0xFF8B0000),
                  Color(0xFF5A0808),
                ]
              : const [
                  Color(0xFF5C2B2B),
                  Color(0xFF421C1C),
                ],
        ),
        border: Border.all(
          color: onPressed != null
              ? const Color(0xFFFFD54F)
              : const Color(0xFF8A6D3B),
          width: 1.8,
        ),
        boxShadow: onPressed != null
            ? const [
                BoxShadow(
                  color: Color(0x66B71C1C),
                  blurRadius: 10,
                  offset: Offset(0, 3),
                ),
                BoxShadow(
                  color: Colors.black45,
                  blurRadius: 6,
                  offset: Offset(0, 2),
                ),
              ]
            : null,
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(12),
          onTap: onPressed,
          child: Center(
            child: isLoading
                ? const SizedBox(
                    width: 22,
                    height: 22,
                    child: CircularProgressIndicator(
                      strokeWidth: 2.4,
                      color: Color(0xFFFFD54F),
                    ),
                  )
                : Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(
                        Icons.local_fire_department_rounded,
                        color: Color(0xFFFFE082),
                        size: 20,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        label,
                        style: const TextStyle(
                          color: Color(0xFFFFFBF2),
                          fontSize: 15,
                          fontWeight: FontWeight.w900,
                          letterSpacing: 2.2,
                          shadows: [
                            Shadow(
                              blurRadius: 3,
                              offset: Offset(1, 1),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
          ),
        ),
      ),
    );
  }
}

/// Ninja-themed social button for Google and Apple sign-in.
class _SocialSignInButton extends StatelessWidget {
  const _SocialSignInButton({
    required this.label,
    required this.icon,
    required this.backgroundColor,
    required this.borderColor,
    required this.textColor,
    required this.enabled,
    required this.onPressed,
  });

  final String label;
  final Widget icon;
  final Color backgroundColor;
  final Color borderColor;
  final Color textColor;
  final bool enabled;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 44,
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(
          color: borderColor,
          width: 1.3,
        ),
        boxShadow: const [
          BoxShadow(
            color: Colors.black38,
            blurRadius: 4,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(10),
          onTap: enabled ? onPressed : null,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 14),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                icon,
                const SizedBox(width: 12),
                Text(
                  label,
                  style: TextStyle(
                    color: textColor,
                    fontSize: 13.5,
                    fontWeight: FontWeight.w600,
                    letterSpacing: 0.5,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

/// Feudal parchment style divider.
class _FeudalDivider extends StatelessWidget {
  const _FeudalDivider({required this.text});

  final String text;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        const Expanded(
          child: Divider(
            color: Color(0xFF6B4524),
            thickness: 1,
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 10),
          child: Text(
            text,
            style: const TextStyle(
              color: Color(0xFFAD8C63),
              fontSize: 10,
              fontWeight: FontWeight.w700,
              letterSpacing: 1.5,
            ),
          ),
        ),
        const Expanded(
          child: Divider(
            color: Color(0xFF6B4524),
            thickness: 1,
          ),
        ),
      ],
    );
  }
}

/// Scroll error banner in feudal aesthetic.
class _NinjaErrorBanner extends StatelessWidget {
  const _NinjaErrorBanner({required this.message});

  final String message;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFF451414),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(
          color: const Color(0xFFE57373),
          width: 1.2,
        ),
      ),
      child: Row(
        children: [
          const Icon(
            Icons.warning_amber_rounded,
            color: Color(0xFFFF8A80),
            size: 18,
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              message,
              style: const TextStyle(
                color: Color(0xFFFFCDD2),
                fontSize: 12,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
