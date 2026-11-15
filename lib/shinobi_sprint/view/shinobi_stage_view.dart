import 'dart:async';
import 'package:flame/game.dart' hide Route;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:super_dash/audio/audio.dart';
import 'package:super_dash/bamboo_village/autumn_maple_game.dart';
import 'package:super_dash/bamboo_village/main_game.dart';
import 'package:super_dash/bamboo_village/ninja_player.dart';
import 'package:super_dash/bamboo_village/twilight_game.dart';
import 'package:super_dash/shinobi_sprint/models/shinobi_level.dart';
import 'package:super_dash/shinobi_sprint/models/shinobi_progress.dart';
import 'package:super_dash/shinobi_sprint/models/shinobi_stage.dart';

/// Interactive Flutter View for playing any Shinobi Sprint stage or level
/// with live HUD, countdown timer for time trials, 3-star clear dialogs,
/// and sequential campaign level progression.
class ShinobiStageView extends StatefulWidget {
  const ShinobiStageView({
    this.initialLevel,
    this.initialStage,
    this.enableDebugHitboxes = false,
    super.key,
  });

  /// The initial level to launch (takes precedence if provided).
  final ShinobiLevel? initialLevel;

  /// Backwards-compatible stage launch.
  final ShinobiStage? initialStage;

  /// Whether hitboxes should be shown initially.
  final bool enableDebugHitboxes;

  /// Convenience route factory for a level.
  static MaterialPageRoute<void> route({
    ShinobiLevel? level,
    ShinobiStage? initialStage,
    bool enableDebugHitboxes = false,
  }) {
    final effectiveLevel =
        level ?? (initialStage == null ? ShinobiCampaign.level1_1 : null);
    return MaterialPageRoute<void>(
      builder: (_) => ShinobiStageView(
        initialLevel: effectiveLevel,
        initialStage: effectiveLevel == null ? initialStage : null,
        enableDebugHitboxes: enableDebugHitboxes,
      ),
    );
  }

  @override
  State<ShinobiStageView> createState() => _ShinobiStageViewState();
}

class _ShinobiStageViewState extends State<ShinobiStageView> {
  ShinobiLevel? _currentLevel;
  ShinobiStage? _currentLegacyStage;

  late FlameGame _game;
  int _orbsCollected = 0;
  late bool _debugHitboxes;
  bool _stageCleared = false;
  bool _isDefeated = false;

  Timer? _timer;
  int _remainingSeconds = 0;
  double _elapsedTime = 0;
  DateTime? _levelStartTime;

  @override
  void initState() {
    super.initState();
    _debugHitboxes = widget.enableDebugHitboxes;

    if (widget.initialLevel != null) {
      _currentLevel = widget.initialLevel;
      _initializeLevel(_currentLevel!);
    } else {
      _currentLegacyStage = widget.initialStage ?? ShinobiStage.bambooVillage;
      _initializeLegacyStage(_currentLegacyStage!);
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _initializeLevel(ShinobiLevel level) {
    _timer?.cancel();
    _orbsCollected = 0;
    _stageCleared = false;
    _isDefeated = false;
    _levelStartTime = DateTime.now();

    if (level.isTimeTrial) {
      _remainingSeconds = level.timeLimit!;
      _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
        if (!mounted || _stageCleared || _isDefeated) {
          timer.cancel();
          return;
        }
        setState(() {
          _remainingSeconds--;
          if (_remainingSeconds <= 0) {
            timer.cancel();
            _showTimeUpDialog();
          }
        });
      });
    }

    _game = level.buildGame(
      onOrbsChanged: (count) {
        if (!mounted) return;
        if (count > _orbsCollected) {
          try {
            context.read<AudioController>().playSfx(Sfx.shurikenPickup);
          } catch (_) {}
        }
        setState(() {
          _orbsCollected = count;
          if (_orbsCollected >= level.totalOrbs && !_stageCleared) {
            _stageCleared = true;
            _timer?.cancel();
            _onLevelCompleted();
          }
        });
      },
      onHazardHit: _onPlayerDefeated,
    );
    _game.debugMode = _debugHitboxes;
  }

  void _initializeLegacyStage(ShinobiStage stage) {
    _timer?.cancel();
    _orbsCollected = 0;
    _stageCleared = false;
    _isDefeated = false;
    _levelStartTime = DateTime.now();

    _game = stage.buildGame(
      onOrbsChanged: (count) {
        if (!mounted) return;
        if (count > _orbsCollected) {
          try {
            context.read<AudioController>().playSfx(Sfx.shurikenPickup);
          } catch (_) {}
        }
        setState(() {
          _orbsCollected = count;
          if (_orbsCollected >= stage.totalOrbs && !_stageCleared) {
            _stageCleared = true;
            _showLegacyStageClearDialog();
          }
        });
      },
      onHazardHit: _onPlayerDefeated,
    );
    _game.debugMode = _debugHitboxes;
  }

  void _restartCurrent() {
    setState(() {
      if (_currentLevel != null) {
        _initializeLevel(_currentLevel!);
      } else if (_currentLegacyStage != null) {
        _initializeLegacyStage(_currentLegacyStage!);
      }
    });
  }

  void _toggleHitboxes() {
    setState(() {
      _debugHitboxes = !_debugHitboxes;
      _game.debugMode = _debugHitboxes;
    });
  }

  NinjaPlayerComponent? _findNinjaPlayer() {
    try {
      if (_game is MainGame) {
        final g = _game as MainGame;
        return g.isLoaded ? g.player : null;
      } else if (_game is TwilightSanctuaryGame) {
        final g = _game as TwilightSanctuaryGame;
        return g.isLoaded ? g.player : null;
      } else if (_game is AutumnMapleGame) {
        final g = _game as AutumnMapleGame;
        return g.isLoaded ? g.player : null;
      }
    } catch (_) {}
    return null;
  }

  void _onLevelCompleted() {
    try {
      context.read<AudioController>().playSfx(Sfx.featherPowerup);
    } catch (_) {}

    final now = DateTime.now();
    _elapsedTime = _levelStartTime != null
        ? now.difference(_levelStartTime!).inMilliseconds / 1000.0
        : 0;

    var starsEarned = 1; // Star 1: Completion
    final level = _currentLevel!;

    // Star 2: All orbs collected
    if (_orbsCollected >= level.totalOrbs) {
      starsEarned++;
    }

    // Star 3: Par time or flawless
    if (level.isTimeTrial) {
      if (_remainingSeconds >= 3) {
        starsEarned++;
      }
    } else {
      if (_elapsedTime < 35.0) {
        starsEarned++;
      }
    }

    ShinobiProgressController.instance.recordLevelCompletion(
      level: level,
      starsEarned: starsEarned,
      timeElapsed: _elapsedTime,
    );

    _showLevelClearDialog(starsEarned);
  }

  void _onPlayerDefeated() {
    if (!mounted || _stageCleared || _isDefeated) return;
    _isDefeated = true;
    _timer?.cancel();
    try {
      HapticFeedback.heavyImpact();
      context.read<AudioController>().playSfx(Sfx.ninjaDefeat);
    } catch (_) {}
    _showDefeatDialog();
  }

  void _showDefeatDialog() {
    showDialog<void>(
      context: context,
      barrierDismissible: false,
      builder: (dialogContext) {
        return AlertDialog(
          backgroundColor: const Color(0xFF0F172A),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
            side: const BorderSide(color: Color(0xFFE11D48), width: 2),
          ),
          title: const Row(
            children: [
              Icon(
                Icons.warning_amber_rounded,
                color: Color(0xFFE11D48),
                size: 32,
              ),
              SizedBox(width: 10),
              Expanded(
                child: Text(
                  '無念 • SHINOBI FALLEN',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w900,
                    fontSize: 18,
                    letterSpacing: 1.2,
                  ),
                ),
              ),
            ],
          ),
          content: Text(
            'A shinobi fell to deadly spikes or treacherous depths! '
            'Calibrate your leaps, time your sword strikes, and try again.',
            style: TextStyle(
              color: Colors.grey.shade300,
              fontSize: 13,
              height: 1.4,
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(dialogContext).pop();
                Navigator.of(context).pop();
              },
              child: const Text(
                'STAGE SELECT',
                style: TextStyle(color: Colors.white70),
              ),
            ),
            ElevatedButton.icon(
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFFE11D48),
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 10,
                ),
              ),
              icon: const Icon(Icons.refresh, size: 18),
              onPressed: () {
                Navigator.of(dialogContext).pop();
                _restartCurrent();
              },
              label: const Text(
                'RETRY STAGE',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
            ),
          ],
        );
      },
    );
  }

  void _showTimeUpDialog() {
    showDialog<void>(
      context: context,
      barrierDismissible: false,
      builder: (dialogContext) {
        return AlertDialog(
          backgroundColor: const Color(0xFF0F172A),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
            side: const BorderSide(color: Color(0xFFEF4444), width: 2),
          ),
          title: const Row(
            children: [
              Icon(Icons.timer_off, color: Color(0xFFEF4444), size: 30),
              SizedBox(width: 10),
              Text(
                "TIME'S UP!",
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w900,
                  fontSize: 20,
                ),
              ),
            ],
          ),
          content: Text(
            'The timer expired before all orbs could be collected. '
            'Gather speed and leap faster on your next sprint!',
            style: TextStyle(color: Colors.grey.shade300, fontSize: 13),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(dialogContext).pop();
                Navigator.of(context).pop();
              },
              child: const Text(
                'STAGE SELECT',
                style: TextStyle(color: Colors.white70),
              ),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFFEF4444),
                foregroundColor: Colors.white,
              ),
              onPressed: () {
                Navigator.of(dialogContext).pop();
                _restartCurrent();
              },
              child: const Text('RETRY'),
            ),
          ],
        );
      },
    );
  }

  void _showLevelClearDialog(int starsEarned) {
    final level = _currentLevel!;
    final next = level.nextLevel;

    showDialog<void>(
      context: context,
      barrierDismissible: false,
      builder: (dialogContext) {
        return AlertDialog(
          backgroundColor: const Color(0xFF0F172A),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
            side: BorderSide(
              color: level.world.themeColor.withValues(alpha: 0.8),
              width: 2,
            ),
          ),
          title: Row(
            children: [
              Icon(
                Icons.stars,
                color: level.world.accentColor,
                size: 32,
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  level.isFinalLevel ? 'CAMPAIGN COMPLETE!' : 'LEVEL CLEARED!',
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w900,
                    fontSize: 20,
                  ),
                ),
              ),
            ],
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // 3 Stars display
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(3, (index) {
                  final filled = index < starsEarned;
                  return Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 6),
                    child: Icon(
                      filled ? Icons.star_rounded : Icons.star_outline_rounded,
                      color: filled
                          ? const Color(0xFFFBBF24)
                          : Colors.grey.shade700,
                      size: 40,
                    ),
                  );
                }),
              ),
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.05),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  children: [
                    _buildMetricRow('Level', level.title),
                    const SizedBox(height: 6),
                    _buildMetricRow(
                      'Orbs Collected',
                      '$_orbsCollected / ${level.totalOrbs}',
                    ),
                    _buildMetricRow(
                      'Time',
                      level.isTimeTrial
                          ? '${_elapsedTime.toStringAsFixed(1)}s '
                              '(Limit: ${level.timeLimit}s)'
                          : '${_elapsedTime.toStringAsFixed(1)}s',
                    ),
                  ],
                ),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(dialogContext).pop();
                Navigator.of(context).pop();
              },
              child: const Text('MAP', style: TextStyle(color: Colors.white70)),
            ),
            OutlinedButton(
              onPressed: () {
                Navigator.of(dialogContext).pop();
                _restartCurrent();
              },
              child: const Text('RETRY', style: TextStyle(color: Colors.white)),
            ),
            if (next != null)
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: level.world.themeColor,
                  foregroundColor: Colors.white,
                ),
                onPressed: () {
                  Navigator.of(dialogContext).pop();
                  setState(() {
                    _currentLevel = next;
                    _initializeLevel(next);
                  });
                },
                child: const Text('NEXT LEVEL'),
              ),
          ],
        );
      },
    );
  }

  void _showLegacyStageClearDialog() {
    try {
      context.read<AudioController>().playSfx(Sfx.featherPowerup);
    } catch (_) {}
    final next = _currentLegacyStage?.nextStage;
    showDialog<void>(
      context: context,
      barrierDismissible: false,
      builder: (dialogContext) {
        return AlertDialog(
          backgroundColor: const Color(0xFF0F172A),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
            side: BorderSide(
              color: _currentLegacyStage!.themeColor.withValues(alpha: 0.8),
              width: 2,
            ),
          ),
          title: Row(
            children: [
              Icon(
                Icons.stars,
                color: _currentLegacyStage!.accentColor,
                size: 32,
              ),
              const SizedBox(width: 10),
              Text(
                _currentLegacyStage!.isFinalStage
                    ? 'CAMPAIGN COMPLETE!'
                    : 'STAGE CLEARED!',
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w900,
                  fontSize: 20,
                ),
              ),
            ],
          ),
          content: Text(
            'All ${_currentLegacyStage!.totalOrbs} spirit orbs recovered!',
            style: const TextStyle(color: Colors.white70),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(dialogContext).pop();
                Navigator.of(context).pop();
              },
              child: const Text(
                'STAGE SELECT',
                style: TextStyle(color: Colors.white70),
              ),
            ),
            if (next != null)
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: _currentLegacyStage!.themeColor,
                  foregroundColor: Colors.white,
                ),
                onPressed: () {
                  Navigator.of(dialogContext).pop();
                  setState(() {
                    _currentLegacyStage = next;
                    _initializeLegacyStage(next);
                  });
                },
                child: const Text('NEXT STAGE'),
              ),
          ],
        );
      },
    );
  }

  Widget _buildMetricRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          label,
          style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 12),
        ),
        Text(
          value,
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
            fontSize: 12,
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final themeColor = _currentLevel?.world.themeColor ??
        _currentLegacyStage?.themeColor ??
        const Color(0xFF10B981);
    final accentColor = _currentLevel?.world.accentColor ??
        _currentLegacyStage?.accentColor ??
        const Color(0xFF34D399);

    final titleText = _currentLevel != null
        ? '${_currentLevel!.world.title} • ${_currentLevel!.tag}'
        : _currentLegacyStage?.title ?? 'SHINOBI SPRINT';

    final totalOrbs =
        _currentLevel?.totalOrbs ?? _currentLegacyStage?.totalOrbs ?? 6;

    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // 1. The Game Engine Canvas
          Positioned.fill(
            child: GameWidget(game: _game),
          ),

          // 2. Top HUD Bar
          Positioned(
            top: 16,
            left: 16,
            right: 16,
            child: Row(
              children: [
                // Back button
                IconButton(
                  icon: const Icon(Icons.arrow_back, color: Colors.white),
                  onPressed: () => Navigator.of(context).pop(),
                  tooltip: 'Exit to Stage Select',
                ),

                const SizedBox(width: 8),

                // Level Tag / Title
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.black54,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: themeColor.withValues(alpha: 0.6),
                    ),
                  ),
                  child: Text(
                    titleText,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 12,
                      fontWeight: FontWeight.w900,
                      letterSpacing: 0.5,
                    ),
                  ),
                ),

                const Spacer(),

                // Time Trial Countdown Badge (if active)
                if (_currentLevel?.isTimeTrial ?? false) ...[
                  Container(
                    margin: const EdgeInsets.only(right: 8),
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: _remainingSeconds <= 5
                          ? Colors.red.withValues(alpha: 0.8)
                          : Colors.black54,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: _remainingSeconds <= 5
                            ? Colors.redAccent
                            : Colors.amber,
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.timer, color: Colors.amber, size: 16),
                        const SizedBox(width: 6),
                        Text(
                          '${_remainingSeconds}s',
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 13,
                            fontWeight: FontWeight.w900,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],

                // Orbs Counter
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.black54,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: accentColor.withValues(alpha: 0.6),
                    ),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.circle, color: accentColor, size: 14),
                      const SizedBox(width: 8),
                      Text(
                        '$_orbsCollected / $totalOrbs ORBS',
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(width: 8),

                // Hitbox Toggle
                IconButton(
                  icon: Icon(
                    _debugHitboxes
                        ? Icons.visibility
                        : Icons.visibility_off_outlined,
                    color: _debugHitboxes ? accentColor : Colors.white60,
                  ),
                  onPressed: _toggleHitboxes,
                  tooltip: 'Toggle Collision Overlay',
                ),

                // Restart Stage
                IconButton(
                  icon: const Icon(Icons.refresh, color: Colors.white),
                  onPressed: _restartCurrent,
                  tooltip: 'Restart Level',
                ),
              ],
            ),
          ),

          // 3. Mobile Touch Virtual Controls:
          // Left: D-Pad, Right: Jump & Drop
          Positioned(
            left: 20,
            bottom: 20,
            child: Row(
              children: [
                _buildControlButton(
                  icon: Icons.arrow_left,
                  onTapDown: () => _findNinjaPlayer()?.moveLeft(),
                  onTapUp: () => _findNinjaPlayer()?.stopMoving(),
                ),
                const SizedBox(width: 12),
                _buildControlButton(
                  icon: Icons.arrow_right,
                  onTapDown: () => _findNinjaPlayer()?.moveRight(),
                  onTapUp: () => _findNinjaPlayer()?.stopMoving(),
                ),
              ],
            ),
          ),

          Positioned(
            right: 20,
            bottom: 20,
            child: Row(
              children: [
                _buildControlButton(
                  icon: Icons.change_circle_outlined,
                  label: 'SHURIKEN',
                  color: const Color(0xFF0284C7),
                  onTapDown: () {
                    HapticFeedback.lightImpact();
                    _findNinjaPlayer()?.throwShuriken();
                    try {
                      context
                          .read<AudioController>()
                          .playSfx(Sfx.shurikenThrow);
                    } catch (_) {}
                  },
                ),
                const SizedBox(width: 10),
                _buildControlButton(
                  icon: Icons.flash_on,
                  label: 'SLASH',
                  color: const Color(0xFFDC2626),
                  onTapDown: () {
                    HapticFeedback.mediumImpact();
                    _findNinjaPlayer()?.attack();
                    try {
                      context.read<AudioController>().playSfx(Sfx.katanaSlash);
                    } catch (_) {}
                  },
                ),
                const SizedBox(width: 10),
                _buildControlButton(
                  label: 'DROP',
                  onTapDown: () => _findNinjaPlayer()?.dropDown(),
                  color: Colors.amber.shade800,
                ),
                const SizedBox(width: 10),
                _buildControlButton(
                  icon: Icons.arrow_upward,
                  label: 'JUMP',
                  onTapDown: () => _findNinjaPlayer()?.jump(),
                  color: themeColor,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildControlButton({
    required VoidCallback onTapDown,
    IconData? icon,
    String? label,
    VoidCallback? onTapUp,
    Color? color,
  }) {
    return GestureDetector(
      onTapDown: (_) => onTapDown(),
      onTapUp: (_) => onTapUp?.call(),
      onTapCancel: () => onTapUp?.call(),
      child: Container(
        width: 60,
        height: 60,
        decoration: BoxDecoration(
          color: (color ?? Colors.black54).withValues(alpha: 0.6),
          shape: BoxShape.circle,
          border: Border.all(
            color: (color ?? Colors.white54).withValues(alpha: 0.8),
            width: 2,
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.4),
              blurRadius: 6,
              offset: const Offset(0, 3),
            ),
          ],
        ),
        child: Center(
          child: icon != null && label != null
              ? Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(icon, color: Colors.white, size: 20),
                    const SizedBox(height: 2),
                    Text(
                      label,
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 9,
                      ),
                    ),
                  ],
                )
              : icon != null
                  ? Icon(icon, color: Colors.white, size: 28)
                  : Text(
                      label ?? '',
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 11,
                      ),
                    ),
        ),
      ),
    );
  }
}
