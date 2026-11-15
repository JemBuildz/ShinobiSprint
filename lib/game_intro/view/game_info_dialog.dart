import 'dart:ui';

import 'package:app_ui/app_ui.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:super_dash/constants/constants.dart';
import 'package:super_dash/l10n/l10n.dart';
import 'package:url_launcher/url_launcher_string.dart';

class GameInfoDialog extends StatelessWidget {
  const GameInfoDialog({super.key});

  static PageRoute<void> route() {
    return HeroDialogRoute(
      builder: (_) => BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 8, sigmaY: 8),
        child: const GameInfoDialog(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    final bodyStyle = AppTextStyles.bodyLarge;
    const highlightColor = Color(0xFF9CECCD);
    final linkStyle = AppTextStyles.bodyLarge.copyWith(
      color: highlightColor,
      decoration: TextDecoration.underline,
      decorationColor: highlightColor,
    );
    return AppDialog(
      border: Border.all(color: Colors.white24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const SizedBox(height: 24),
          Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
                decoration: BoxDecoration(
                  color: const Color(0xFFE11D48).withValues(alpha: 0.25),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(
                    color: const Color(0xFFE11D48).withValues(alpha: 0.6),
                  ),
                ),
                child: const Text(
                  '忍 び ス プ リ ン ト',
                  style: TextStyle(
                    color: Color(0xFFFDA4AF),
                    fontSize: 12,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 4,
                  ),
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'SHINOBI SPRINT',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                  fontWeight: FontWeight.w900,
                  letterSpacing: 2,
                ),
              ),
            ],
          ),
          const SizedBox(height: 32),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 32),
            child: Column(
              children: [
                Text(
                  'About Shinobi Sprint',
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
                const SizedBox(height: 24),
                RichText(
                  textAlign: TextAlign.center,
                  text: TextSpan(
                    style: bodyStyle,
                    children: [
                      TextSpan(text: l10n.learn),
                      TextSpan(
                        text: l10n.howWeBuiltSuperDash,
                        style: linkStyle,
                        recognizer: TapGestureRecognizer()
                          ..onTap = () => launchUrlString(Urls.howWeBuilt),
                      ),
                      TextSpan(
                        text: l10n.inFlutterAndGrabThe,
                      ),
                      TextSpan(
                        text: l10n.openSourceCode,
                        style: linkStyle,
                        recognizer: TapGestureRecognizer()
                          ..onTap = () => launchUrlString(Urls.githubRepo),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 24),
                Text(
                  l10n.otherLinks,
                  style: bodyStyle,
                ),
                const SizedBox(height: 16),
                RichText(
                  text: TextSpan(
                    text: l10n.flutterGames,
                    style: linkStyle,
                    recognizer: TapGestureRecognizer()
                      ..onTap = () => launchUrlString(Urls.flutterGames),
                  ),
                ),
                RichText(
                  text: TextSpan(
                    text: l10n.privacyPolicy,
                    style: linkStyle,
                    recognizer: TapGestureRecognizer()
                      ..onTap = () => launchUrlString(Urls.privacyPolicy),
                  ),
                ),
                RichText(
                  text: TextSpan(
                    text: l10n.termsOfService,
                    style: linkStyle,
                    recognizer: TapGestureRecognizer()
                      ..onTap = () => launchUrlString(Urls.termsOfService),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 40),
        ],
      ),
    );
  }
}
