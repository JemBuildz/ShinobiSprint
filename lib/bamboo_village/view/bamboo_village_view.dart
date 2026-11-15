import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:super_dash/bamboo_village/main_game.dart';

/// Flutter interactive test view for the Bamboo Village level
class BambooVillageView extends StatefulWidget {
  const BambooVillageView({super.key});

  @override
  State<BambooVillageView> createState() => _BambooVillageViewState();
}

class _BambooVillageViewState extends State<BambooVillageView> {
  late final MainGame _game;
  bool _debugHitboxes = false;

  @override
  void initState() {
    super.initState();
    _game = MainGame();
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
      backgroundColor: const Color(0xFF0E1A24),
      body: Stack(
        children: [
          // 1. The Flame Game Canvas
          Positioned.fill(
            child: GameWidget(
              game: _game,
            ),
          ),

          // 2. Top Navigation & Inspection Bar
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Row(
                children: [
                  // Back button (if navigator can pop)
                  if (Navigator.of(context).canPop())
                    IconButton.filledTonal(
                      onPressed: () => Navigator.of(context).pop(),
                      icon: const Icon(Icons.arrow_back),
                      tooltip: 'Back to Menu',
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
                      border: Border.all(color: Colors.white24),
                    ),
                    child: const Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.landscape, color: Colors.amber, size: 18),
                        SizedBox(width: 6),
                        Text(
                          'Bamboo Village Level Test',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Spacer(),

                  // Hitbox Debug Toggle
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

                  // Reset Player Button
                  IconButton.filled(
                    style: IconButton.styleFrom(
                      backgroundColor: Colors.amber.shade700,
                    ),
                    onPressed: () => _game.resetPlayer(),
                    icon: const Icon(Icons.refresh, color: Colors.black),
                    tooltip: 'Reset Ninja Position',
                  ),
                ],
              ),
            ),
          ),

          // 3. Center Guide Pill (Keyboard Instructions)
          SafeArea(
            child: Align(
              alignment: Alignment.bottomCenter,
              child: Padding(
                padding: const EdgeInsets.only(bottom: 24),
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 14,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.black.withValues(alpha: 0.6),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: Colors.white12),
                  ),
                  child: const Text(
                    'Move: [A]/[D] or ←/→  |  Jump: [Space]  |  '
                    'Drop: [S] + [Space]',
                    style: TextStyle(
                      color: Colors.white70,
                      fontSize: 12,
                      letterSpacing: 0.3,
                    ),
                  ),
                ),
              ),
            ),
          ),

          // 4. Bottom Left Touch D-Pad (Left / Right)
          SafeArea(
            child: Align(
              alignment: Alignment.bottomLeft,
              child: Padding(
                padding:
                    const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    _ControlButton(
                      icon: Icons.arrow_back,
                      label: 'A',
                      onDown: () => _game.player.moveLeft(),
                      onUp: () => _game.player.stopMoving(),
                    ),
                    const SizedBox(width: 12),
                    _ControlButton(
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

          // 5. Bottom Right Touch Action Buttons (Combat & Mobility)
          SafeArea(
            child: Align(
              alignment: Alignment.bottomRight,
              child: Padding(
                padding:
                    const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    _ControlButton(
                      icon: Icons.change_circle_outlined,
                      label: 'Star',
                      color: const Color(0xFF0284C7).withValues(alpha: 0.8),
                      onDown: () => _game.player.throwShuriken(),
                      onUp: () {},
                    ),
                    const SizedBox(width: 10),
                    _ControlButton(
                      icon: Icons.flash_on,
                      label: 'Slash',
                      color: const Color(0xFFDC2626).withValues(alpha: 0.8),
                      onDown: () => _game.player.attack(),
                      onUp: () {},
                    ),
                    const SizedBox(width: 10),
                    _ControlButton(
                      icon: Icons.arrow_downward,
                      label: 'Drop',
                      color: Colors.orange.withValues(alpha: 0.8),
                      onDown: () => _game.player.dropDown(),
                      onUp: () {},
                    ),
                    const SizedBox(width: 10),
                    _ControlButton(
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

class _ControlButton extends StatelessWidget {
  const _ControlButton({
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
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.3),
              blurRadius: 6,
              offset: const Offset(0, 3),
            ),
          ],
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
