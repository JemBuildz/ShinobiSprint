import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:super_dash/bamboo_village/twilight_game.dart';

/// Interactive Flutter view for Level 2: Twilight Bamboo Sanctuary
class TwilightSanctuaryView extends StatefulWidget {
  const TwilightSanctuaryView({super.key});

  @override
  State<TwilightSanctuaryView> createState() => _TwilightSanctuaryViewState();
}

class _TwilightSanctuaryViewState extends State<TwilightSanctuaryView> {
  late final TwilightSanctuaryGame _game;
  bool _debugHitboxes = false;
  int _orbsCollected = 0;

  @override
  void initState() {
    super.initState();
    _game = TwilightSanctuaryGame(
      onOrbsChanged: (orbs) {
        if (mounted) {
          setState(() {
            _orbsCollected = orbs;
          });
        }
      },
    );
  }

  void _toggleHitboxes() {
    setState(() {
      _debugHitboxes = !_debugHitboxes;
      _game.debugMode = _debugHitboxes;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0C101A),
      body: Stack(
        children: [
          Positioned.fill(
            child: GameWidget(
              game: _game,
            ),
          ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Row(
                children: [
                  if (Navigator.of(context).canPop())
                    IconButton.filledTonal(
                      onPressed: () => Navigator.of(context).pop(),
                      icon: const Icon(Icons.arrow_back),
                      tooltip: 'Back',
                    ),
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.black.withValues(alpha: 0.65),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: Colors.amber.withValues(alpha: 0.3),
                      ),
                    ),
                    child: const Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.nights_stay, color: Colors.amber, size: 18),
                        SizedBox(width: 6),
                        Text(
                          'Level 2: Twilight Sanctuary',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.black.withValues(alpha: 0.65),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: _orbsCollected == 4
                            ? Colors.greenAccent
                            : Colors.amber.withValues(alpha: 0.5),
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.stars_rounded,
                          color: _orbsCollected == 4
                              ? Colors.greenAccent
                              : Colors.amberAccent,
                          size: 18,
                        ),
                        const SizedBox(width: 6),
                        Text(
                          'Orbs: $_orbsCollected / 4',
                          style: TextStyle(
                            color: _orbsCollected == 4
                                ? Colors.greenAccent
                                : Colors.amberAccent,
                            fontWeight: FontWeight.bold,
                            fontSize: 13,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Spacer(),
                  ActionChip(
                    avatar: Icon(
                      _debugHitboxes ? Icons.visibility : Icons.visibility_off,
                      size: 16,
                      color:
                          _debugHitboxes ? Colors.cyanAccent : Colors.white70,
                    ),
                    label: Text(
                      _debugHitboxes ? 'Hitboxes ON' : 'Hitboxes OFF',
                      style: TextStyle(
                        color:
                            _debugHitboxes ? Colors.cyanAccent : Colors.white70,
                        fontSize: 12,
                      ),
                    ),
                    backgroundColor: Colors.black54,
                    side: BorderSide(
                      color:
                          _debugHitboxes ? Colors.cyanAccent : Colors.white24,
                    ),
                    onPressed: _toggleHitboxes,
                  ),
                  const SizedBox(width: 8),
                  IconButton.filled(
                    style: IconButton.styleFrom(
                      backgroundColor: Colors.amber.shade700,
                    ),
                    onPressed: () => _game.resetPlayer(),
                    icon: const Icon(Icons.refresh, color: Colors.black),
                    tooltip: 'Reset',
                  ),
                ],
              ),
            ),
          ),
          SafeArea(
            child: Align(
              alignment: Alignment.bottomLeft,
              child: Padding(
                padding:
                    const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    _TouchBtn(
                      icon: Icons.arrow_back,
                      label: 'A',
                      onDown: () => _game.player.moveLeft(),
                      onUp: () => _game.player.stopMoving(),
                    ),
                    const SizedBox(width: 12),
                    _TouchBtn(
                      icon: Icons.arrow_forward,
                      label: 'D',
                      onDown: () => _game.player.moveRight(),
                      onUp: () => _game.player.stopMoving(),
                    ),
                  ],
                ),
              ),
            ),
          ),
          SafeArea(
            child: Align(
              alignment: Alignment.bottomRight,
              child: Padding(
                padding:
                    const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    _TouchBtn(
                      icon: Icons.arrow_downward,
                      label: 'Drop',
                      color: Colors.orange.withValues(alpha: 0.8),
                      onDown: () => _game.player.dropDown(),
                      onUp: () {},
                    ),
                    const SizedBox(width: 12),
                    _TouchBtn(
                      icon: Icons.arrow_upward,
                      label: 'Jump',
                      color: Colors.green.withValues(alpha: 0.8),
                      onDown: () => _game.player.jump(),
                      onUp: () {},
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _TouchBtn extends StatelessWidget {
  const _TouchBtn({
    required this.icon,
    required this.label,
    required this.onDown,
    required this.onUp,
    this.color,
  });

  final IconData icon;
  final String label;
  final VoidCallback onDown;
  final VoidCallback onUp;
  final Color? color;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => onDown(),
      onTapUp: (_) => onUp(),
      onTapCancel: onUp,
      child: Container(
        width: 58,
        height: 58,
        decoration: BoxDecoration(
          color: color ?? Colors.white.withValues(alpha: 0.2),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.white30, width: 1.5),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: Colors.white, size: 24),
            Text(
              label,
              style: const TextStyle(
                color: Colors.white70,
                fontSize: 10,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
