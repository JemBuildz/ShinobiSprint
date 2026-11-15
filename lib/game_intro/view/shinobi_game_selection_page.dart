import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:super_dash/game_intro/game_intro.dart';
import 'package:super_dash/leaderboard/leaderboard.dart';
import 'package:super_dash/settings/settings_controller.dart';
import 'package:super_dash/shinobi_sprint/shinobi_sprint.dart';

/// Screen 3: Official Shinobi Sprint Game Selection & Main Menu Screen.
/// Directly matches Stitch design "App Screen 3 Game Selection screen"
/// with landscape support, animated sakura petals, stage select,
/// campaign quick play, rankings, audio/settings, and clan status.
class ShinobiGameSelectionPage extends StatefulWidget {
  const ShinobiGameSelectionPage({super.key});

  static PageRoute<void> route() {
    return PageRouteBuilder<void>(
      pageBuilder: (context, animation, secondaryAnimation) =>
          const ShinobiGameSelectionPage(),
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        return FadeTransition(opacity: animation, child: child);
      },
    );
  }

  @override
  State<ShinobiGameSelectionPage> createState() =>
      _ShinobiGameSelectionPageState();
}

class _ShinobiGameSelectionPageState extends State<ShinobiGameSelectionPage>
    with SingleTickerProviderStateMixin {
  late final AnimationController _petalController;
  final List<_PetalData> _petals = [];

  @override
  void initState() {
    super.initState();
    _petalController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 12),
    )..repeat();

    final rand = math.Random();
    for (var i = 0; i < 16; i++) {
      _petals.add(
        _PetalData(
          x: rand.nextDouble(),
          y: rand.nextDouble(),
          speed: 0.12 + rand.nextDouble() * 0.22,
          size: 5 + rand.nextDouble() * 7.0,
          rotation: rand.nextDouble() * 2 * math.pi,
          rotationSpeed: (rand.nextDouble() - 0.5) * 2,
          opacity: 0.30 + rand.nextDouble() * 0.40,
        ),
      );
    }
  }

  @override
  void dispose() {
    _petalController.dispose();
    super.dispose();
  }

  void _onPlayCampaign() {
    Navigator.of(context).push(
      ShinobiStageView.route(),
    );
  }

  void _onStageSelect() {
    Navigator.of(context).push(
      ShinobiStageSelectPage.route(),
    );
  }

  void _onRankings() {
    Navigator.of(context).push(
      LeaderboardPage.route(),
    );
  }

  void _onInfo() {
    Navigator.of(context).push(
      GameInfoDialog.route(),
    );
  }

  void _onHowToPlay() {
    Navigator.of(context).push(
      GameInstructionsOverlay.route(),
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
          // 1. Background image (Waterfall Valley with Runner Ninja)
          Image.asset(
            'assets/images/shinobi_game_selection_bg.png',
            fit: BoxFit.cover,
            alignment:
                isLandscape ? const Alignment(0, 0.15) : Alignment.center,
          ),

          // 2. Cinematic vignette & lighting gradients
          Positioned.fill(
            child: DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    const Color(0xFF0D1322).withValues(alpha: 0.70),
                    Colors.transparent,
                    const Color(0xFF0D1322).withValues(alpha: 0.85),
                    const Color(0xFF080E1D).withValues(alpha: 0.95),
                  ],
                  stops: const [0, 0.28, 0.70, 1],
                ),
              ),
            ),
          ),

          // 3. Floating Sakura Petals
          AnimatedBuilder(
            animation: _petalController,
            builder: (context, _) {
              return CustomPaint(
                painter: _PetalPainter(
                  petals: _petals,
                  progress: _petalController.value,
                ),
              );
            },
          ),

          // 4. Safe Area UI
          SafeArea(
            child: isLandscape
                ? _buildLandscapeLayout(context)
                : _buildPortraitLayout(context),
          ),
        ],
      ),
    );
  }

  Widget _buildTopLogo({double maxWidth = 260}) {
    return ConstrainedBox(
      constraints: BoxConstraints(maxWidth: maxWidth),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Image.asset(
            'assets/images/shinobi_sprint_logo.png',
            fit: BoxFit.contain,
          ),
          const SizedBox(height: 4),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 2),
            decoration: BoxDecoration(
              color: const Color(0xFF10B981).withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: const Color(0xFF10B981).withValues(alpha: 0.4),
              ),
            ),
            child: const Text(
              'FLAME ENGINE 2D • CAMPAIGN SELECTION',
              style: TextStyle(
                color: Color(0xFF6FFBBE),
                fontSize: 9,
                fontWeight: FontWeight.w700,
                letterSpacing: 1.5,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStageSelectButton() {
    final progress = ShinobiProgressController.instance;
    return AnimatedBuilder(
      animation: progress,
      builder: (context, _) {
        final totalStars = progress.totalStars;
        final clearedCount = progress.levelStars.values
            .where((stars) => stars > 0)
            .length;

        return Material(
          color: Colors.transparent,
          borderRadius: BorderRadius.circular(14),
          child: InkWell(
            onTap: _onStageSelect,
            borderRadius: BorderRadius.circular(14),
            splashColor: const Color(0xFF10B981).withValues(alpha: 0.3),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
              decoration: BoxDecoration(
                color: const Color(0xFF151B2B).withValues(alpha: 0.85),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(
                  color: const Color(0xFF10B981).withValues(alpha: 0.35),
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha: 0.45),
                    blurRadius: 12,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Row(
                children: [
                  Container(
                    width: 44,
                    height: 44,
                    decoration: BoxDecoration(
                      color: const Color(0xFF242A3A),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(
                        color: const Color(0xFF10B981).withValues(alpha: 0.3),
                      ),
                    ),
                    child: const Icon(
                      Icons.map_rounded,
                      color: Color(0xFF4EDEA3),
                      size: 24,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Row(
                          children: [
                            const Text(
                              'STAGE SELECT',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 15,
                                fontWeight: FontWeight.w900,
                                letterSpacing: 0.5,
                              ),
                            ),
                            const SizedBox(width: 8),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 6,
                                vertical: 2,
                              ),
                              decoration: BoxDecoration(
                                color: const Color(0xFF10B981)
                                    .withValues(alpha: 0.25),
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: const Text(
                                'CHAPTER 1',
                                style: TextStyle(
                                  color: Color(0xFF4EDEA3),
                                  fontSize: 9,
                                  fontWeight: FontWeight.w800,
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 3),
                        Text(
                          '$clearedCount/15 Levels Cleared • '
                          '$totalStars/45 Stars Earned',
                          style: TextStyle(
                            color: Colors.white.withValues(alpha: 0.7),
                            fontSize: 11,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Icon(
                    Icons.arrow_forward_ios_rounded,
                    color: Color(0xFF86948A),
                    size: 16,
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildPlayCampaignButton() {
    return Material(
      color: Colors.transparent,
      borderRadius: BorderRadius.circular(14),
      child: InkWell(
        onTap: _onPlayCampaign,
        borderRadius: BorderRadius.circular(14),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          decoration: BoxDecoration(
            gradient: const LinearGradient(
              colors: [
                Color(0xFF059669),
                Color(0xFF10B981),
                Color(0xFF4EDEA3),
              ],
            ),
            borderRadius: BorderRadius.circular(14),
            boxShadow: [
              BoxShadow(
                color: const Color(0xFF10B981).withValues(alpha: 0.45),
                blurRadius: 18,
                offset: const Offset(0, 6),
              ),
            ],
          ),
          child: const Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.play_arrow_rounded,
                color: Color(0xFF003824),
                size: 26,
              ),
              SizedBox(width: 8),
              Text(
                'START RUN • LEVEL 1',
                style: TextStyle(
                  color: Color(0xFF003824),
                  fontSize: 15,
                  fontWeight: FontWeight.w900,
                  letterSpacing: 1,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildRankingsButton() {
    return Material(
      color: Colors.transparent,
      borderRadius: BorderRadius.circular(12),
      child: InkWell(
        onTap: _onRankings,
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
          decoration: BoxDecoration(
            color: const Color(0xFF151B2B).withValues(alpha: 0.8),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: Colors.white.withValues(alpha: 0.1),
            ),
          ),
          child: Row(
            children: [
              Container(
                width: 36,
                height: 36,
                decoration: BoxDecoration(
                  color: const Color(0xFF242A3A),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: const Icon(
                  Icons.military_tech_rounded,
                  color: Color(0xFFFACC15),
                  size: 20,
                ),
              ),
              const SizedBox(width: 8),
              const Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      'RANKINGS',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 12,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    Text(
                      '#42 Clan Rank',
                      style: TextStyle(
                        color: Color(0xFFFACC15),
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
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

  Widget _buildSettingsButton() {
    final settings = context.watch<SettingsController>();

    return ValueListenableBuilder<bool>(
      valueListenable: settings.muted,
      builder: (context, muted, _) {
        return Material(
          color: Colors.transparent,
          borderRadius: BorderRadius.circular(12),
          child: InkWell(
            onTap: () {
              context.read<SettingsController>().toggleMuted();
            },
            borderRadius: BorderRadius.circular(12),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              decoration: BoxDecoration(
                color: const Color(0xFF151B2B).withValues(alpha: 0.8),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: Colors.white.withValues(alpha: 0.1),
                ),
              ),
              child: Row(
                children: [
                  Container(
                    width: 36,
                    height: 36,
                    decoration: BoxDecoration(
                      color: const Color(0xFF242A3A),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Icon(
                      muted ? Icons.volume_off_rounded : Icons.tune_rounded,
                      color: muted
                          ? const Color(0xFFEF4444)
                          : const Color(0xFF4EDEA3),
                      size: 20,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Text(
                          'SETTINGS',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                        Text(
                          muted ? 'Muted' : 'Audio ON • 60 FPS',
                          style: TextStyle(
                            color: muted
                                ? const Color(0xFFEF4444)
                                : const Color(0xFFBBCAAF),
                            fontSize: 10,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildFooter() {
    return Padding(
      padding: const EdgeInsets.only(top: 8, bottom: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(
                  Icons.verified_rounded,
                  size: 13,
                  color: Color(0xFF86948A),
                ),
                const SizedBox(width: 4),
                Flexible(
                  child: Text(
                    'LOTUS SHADOW CLAN',
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(
                      color: Colors.white.withValues(alpha: 0.5),
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 8),
          Text(
            'V1.4.2 • FLAME ENGINE',
            style: TextStyle(
              color: Colors.white.withValues(alpha: 0.4),
              fontSize: 10,
              fontWeight: FontWeight.w600,
              letterSpacing: 0.8,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTopCornerActions() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          IconButton(
            icon: const Icon(
              Icons.arrow_back_ios_new_rounded,
              color: Colors.white,
              size: 20,
            ),
            onPressed: () => Navigator.of(context).pushReplacement(
              ShinobiSignOnPage.route(),
            ),
          ),
          Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              IconButton(
                icon: const Icon(
                  Icons.help_outline_rounded,
                  color: Colors.white,
                  size: 22,
                ),
                onPressed: _onHowToPlay,
              ),
              IconButton(
                icon: const Icon(
                  Icons.info_outline_rounded,
                  color: Colors.white,
                  size: 22,
                ),
                onPressed: _onInfo,
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildPortraitLayout(BuildContext context) {
    return Column(
      children: [
        _buildTopCornerActions(),
        const Spacer(),
        _buildTopLogo(maxWidth: 290),
        const Spacer(flex: 3),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              _buildPlayCampaignButton(),
              const SizedBox(height: 10),
              _buildStageSelectButton(),
              const SizedBox(height: 10),
              Row(
                children: [
                  Expanded(child: _buildRankingsButton()),
                  const SizedBox(width: 10),
                  Expanded(child: _buildSettingsButton()),
                ],
              ),
              const SizedBox(height: 10),
              _buildFooter(),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildLandscapeLayout(BuildContext context) {
    return Column(
      children: [
        _buildTopCornerActions(),
        Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 28),
            child: Row(
              children: [
                // Left Column: Logo & Branding
                Expanded(
                  flex: 5,
                  child: Center(
                    child: _buildTopLogo(maxWidth: 320),
                  ),
                ),
                const SizedBox(width: 24),
                // Right Column: Controls, Stages, Actions
                Expanded(
                  flex: 6,
                  child: SingleChildScrollView(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        _buildPlayCampaignButton(),
                        const SizedBox(height: 8),
                        _buildStageSelectButton(),
                        const SizedBox(height: 8),
                        Row(
                          children: [
                            Expanded(child: _buildRankingsButton()),
                            const SizedBox(width: 8),
                            Expanded(child: _buildSettingsButton()),
                          ],
                        ),
                        const SizedBox(height: 8),
                        _buildFooter(),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
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
  double speed;
  double size;
  double rotation;
  double rotationSpeed;
  double opacity;
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
      final currentX =
          (petal.x + math.sin(progress * 2 * math.pi + petal.y * 5) * 0.05) %
              1.0;

      final px = currentX * size.width;
      final py = currentY * size.height;

      paint.color = const Color(0xFFFFB7C5).withValues(alpha: petal.opacity);

      canvas
        ..save()
        ..translate(px, py)
        ..rotate(petal.rotation + progress * petal.rotationSpeed);

      final rect = Rect.fromCenter(
        center: Offset.zero,
        width: petal.size,
        height: petal.size * 1.6,
      );
      canvas
        ..drawOval(rect, paint)
        ..restore();
    }
  }

  @override
  bool shouldRepaint(covariant _PetalPainter oldDelegate) => true;
}
