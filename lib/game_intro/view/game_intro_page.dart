import 'package:app_ui/app_ui.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:super_dash/constants/constants.dart';
import 'package:super_dash/game_intro/game_intro.dart';
import 'package:super_dash/l10n/l10n.dart';
import 'package:super_dash/shinobi_sprint/shinobi_sprint.dart';
import 'package:url_launcher/url_launcher.dart';

/// Shinobi Sprint Introduction and Launch Page.
class GameIntroPage extends StatefulWidget {
  const GameIntroPage({super.key});

  static PageRoute<void> route() {
    return PageRouteBuilder<void>(
      pageBuilder: (context, animation, secondaryAnimation) =>
          const GameIntroPage(),
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        return FadeTransition(opacity: animation, child: child);
      },
    );
  }

  @override
  State<GameIntroPage> createState() => _GameIntroPageState();
}

class _GameIntroPageState extends State<GameIntroPage> {
  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    precacheImage(
      const AssetImage('assets/images/shinobi_sign_on_bg.png'),
      context,
    );
    precacheImage(
      const AssetImage('assets/images/shinobi_sprint_logo.png'),
      context,
    );
  }

  void _onDownload() {
    final isAndroid = defaultTargetPlatform == TargetPlatform.android;
    launchUrl(Uri.parse(isAndroid ? Urls.playStoreLink : Urls.appStoreLink));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D1322),
      body: Stack(
        fit: StackFit.expand,
        children: [
          // 1. Feudal Japanese Panoramic Background Artwork
          Image.asset(
            'assets/images/shinobi_sign_on_bg.png',
            fit: BoxFit.cover,
          ),

          // 2. Cinematic Vignette Scrims
          Positioned.fill(
            child: DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    const Color(0xFF0D1322).withValues(alpha: 0.65),
                    const Color(0xFF080E1D).withValues(alpha: 0.85),
                    const Color(0xFF080E1D).withValues(alpha: 0.96),
                  ],
                  stops: const [0.0, 0.45, 1.0],
                ),
              ),
            ),
          ),

          // 3. Interactive Content
          SafeArea(
            child: isMobileWeb
                ? _MobileWebNotAvailableIntroPage(onDownload: _onDownload)
                : const _IntroPage(),
          ),
        ],
      ),
    );
  }

  bool get isMobileWeb =>
      kIsWeb &&
      (defaultTargetPlatform == TargetPlatform.android ||
          defaultTargetPlatform == TargetPlatform.iOS);
}

class _IntroPage extends StatelessWidget {
  const _IntroPage();

  @override
  Widget build(BuildContext context) {
    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 420),
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const SizedBox(height: 12),
              // Japanese Crest Badge
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
                    fontSize: 13,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 4,
                  ),
                ),
              ),
              const SizedBox(height: 14),

              // Official Shinobi Sprint Game Logo
              Image.asset(
                'assets/images/shinobi_sprint_logo.png',
                width: context.isSmall ? 280 : 350,
                fit: BoxFit.contain,
              ),

              const SizedBox(height: 10),
              Container(
                height: 2,
                width: 150,
                decoration: const BoxDecoration(
                  gradient: LinearGradient(
                    colors: [
                      Colors.transparent,
                      Color(0xFFF59E0B),
                      Colors.transparent,
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // Game Headline & Lore
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 20),
                child: Text(
                  'Sprint through feudal Japan as the Blue Chibi Ninja! '
                  'Master the katana, collect ancient spirit orbs, and '
                  'leap across sacred Torii shrines.',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Color(0xFFE2E8F0),
                    fontSize: 15,
                    fontWeight: FontWeight.w500,
                    height: 1.4,
                  ),
                ),
              ),
              const SizedBox(height: 28),

              // Primary Play Button
              GameElevatedButton.icon(
                label: 'PLAY SHINOBI SPRINT',
                icon: const Icon(
                  Icons.play_circle_fill,
                  color: Colors.white,
                  size: 22,
                ),
                gradient: const LinearGradient(
                  colors: [Color(0xFF059669), Color(0xFF10B981)],
                ),
                onPressed: () => Navigator.of(context).push(
                  ShinobiStageView.route(),
                ),
              ),
              const SizedBox(height: 12),

              // Secondary Stages Button
              GameElevatedButton.icon(
                label: 'SELECT STAGES',
                icon: const Icon(
                  Icons.map,
                  color: Colors.white,
                  size: 20,
                ),
                gradient: const LinearGradient(
                  colors: [Color(0xFF4338CA), Color(0xFF6366F1)],
                ),
                onPressed: () => Navigator.of(context).push(
                  ShinobiStageSelectPage.route(),
                ),
              ),
              const SizedBox(height: 28),

              // Bottom Control Bar
              const Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  AudioButton(),
                  LeaderboardButton(),
                  InfoButton(),
                  HowToPlayButton(),
                ],
              ),
              const SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }
}

class _MobileWebNotAvailableIntroPage extends StatelessWidget {
  const _MobileWebNotAvailableIntroPage({
    required this.onDownload,
  });

  final VoidCallback onDownload;

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    final theme = Theme.of(context);
    final textTheme = theme.textTheme;
    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 390),
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
          child: Column(
            children: [
              const SizedBox(height: 20),
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
                    fontSize: 13,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 4,
                  ),
                ),
              ),
              const SizedBox(height: 14),
              Image.asset(
                'assets/images/shinobi_sprint_logo.png',
                width: 290,
                fit: BoxFit.contain,
              ),
              const SizedBox(height: 40),
              Text(
                l10n.downloadAppMessage,
                textAlign: TextAlign.center,
                style: textTheme.headlineSmall?.copyWith(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 24),
              GameElevatedButton.icon(
                label: l10n.downloadAppLabel,
                icon: const Icon(
                  Icons.download,
                  color: Colors.white,
                ),
                gradient: const LinearGradient(
                  colors: [Color(0xFF059669), Color(0xFF10B981)],
                ),
                onPressed: onDownload,
              ),
              const SizedBox(height: 40),
              const BottomBar(),
              const SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }
}
