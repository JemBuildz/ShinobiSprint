import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:super_dash/bamboo_village/autumn_maple_game.dart';

/// Interactive Flutter view for Level 3: Autumn Maple Forest
class AutumnMapleView extends StatefulWidget {
  const AutumnMapleView({super.key});

  @override
  State<AutumnMapleView> createState() => _AutumnMapleViewState();
}

class _AutumnMapleViewState extends State<AutumnMapleView> {
  late final AutumnMapleGame _game;
  bool _debugHitboxes = false;
  int _orbsCollected = 0;

  @override
  void initState() {
    super.initState();
    _game = AutumnMapleGame(
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
      backgroundColor: const Color(0xFF0A0F1A),
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
                      color: const Color(0xCC0E1524),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: const Color(0xFF8B2500),
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Text(
                          '🍁 LEVEL 3: AUTUMN MAPLE',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 0.8,
                          ),
                        ),
                        const SizedBox(width: 12),
                        const Text('🔮', style: TextStyle(fontSize: 14)),
                        const SizedBox(width: 4),
                        Text(
                          '$_orbsCollected/8',
                          style: const TextStyle(
                            color: Color(0xFFE0F7FA),
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Spacer(),
                  FilledButton.tonalIcon(
                    onPressed: _toggleHitboxes,
                    icon: Icon(
                      _debugHitboxes
                          ? Icons.visibility_off
                          : Icons.visibility,
                      size: 16,
                    ),
                    label: Text(
                      _debugHitboxes ? 'Hide Hitboxes' : 'Show Hitboxes',
                      style: const TextStyle(fontSize: 11),
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
}
