import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:super_dash/shinobi_sprint/models/shinobi_level.dart';

/// Manages campaign progression, 3-star achievements, and records for
/// Shinobi Sprint.
class ShinobiProgressController extends ChangeNotifier {
  ShinobiProgressController({SharedPreferences? preferences})
      : _prefs = preferences {
    _loadProgress();
  }

  ShinobiProgressController._() : _prefs = null {
    _loadProgress();
  }

  static ShinobiProgressController? _instance;

  /// Singleton access instance.
  // ignore: prefer_constructors_over_static_methods
  static ShinobiProgressController get instance =>
      _instance ??= ShinobiProgressController._();

  final SharedPreferences? _prefs;

  final Map<String, int> _levelStars = {};
  final Map<String, int> _levelHighScores = {};
  final Map<String, double> _levelFastestTimes = {};
  final Set<String> _unlockedLevels = {'1-1'};

  /// Star ratings for all levels (0 to 3).
  Map<String, int> get levelStars => Map.unmodifiable(_levelStars);

  /// Total stars earned across the entire campaign (max 45).
  int get totalStars => _levelStars.values.fold(0, (sum, val) => sum + val);

  /// Maximum possible stars in the 15-level campaign.
  static const int maxCampaignStars = 45;

  /// Whether a specific level is unlocked.
  bool isLevelUnlocked(String levelId) {
    // Level 1-1 is always unlocked
    if (levelId == '1-1') return true;
    return _unlockedLevels.contains(levelId);
  }

  /// Returns stars earned for a specific level (0 to 3).
  int getStarsForLevel(String levelId) => _levelStars[levelId] ?? 0;

  /// Returns the fastest completion time for a level, or null if unrecorded.
  double? getFastestTimeForLevel(String levelId) => _levelFastestTimes[levelId];

  /// Records level completion, awards stars, and unlocks the next level.
  Future<void> recordLevelCompletion({
    required ShinobiLevel level,
    required int starsEarned,
    int? score,
    double? timeElapsed,
  }) async {
    final currentStars = _levelStars[level.id] ?? 0;
    if (starsEarned > currentStars) {
      _levelStars[level.id] = starsEarned.clamp(0, 3);
    }

    if (score != null) {
      final currentHigh = _levelHighScores[level.id] ?? 0;
      if (score > currentHigh) {
        _levelHighScores[level.id] = score;
      }
    }

    if (timeElapsed != null) {
      final currentBest = _levelFastestTimes[level.id];
      if (currentBest == null || timeElapsed < currentBest) {
        _levelFastestTimes[level.id] = timeElapsed;
      }
    }

    // Unlock the next sequential level
    final next = level.nextLevel;
    if (next != null) {
      _unlockedLevels.add(next.id);
    }

    notifyListeners();
    await _saveProgress();
  }

  void _loadProgress() {
    if (_prefs == null) return;
    try {
      for (final lvl in ShinobiCampaign.allLevels) {
        final stars = _prefs.getInt('shinobi_stars_${lvl.id}');
        if (stars != null) {
          _levelStars[lvl.id] = stars;
          _unlockedLevels.add(lvl.id);
          final next = lvl.nextLevel;
          if (next != null) {
            _unlockedLevels.add(next.id);
          }
        }

        final bestTime = _prefs.getDouble('shinobi_time_${lvl.id}');
        if (bestTime != null) {
          _levelFastestTimes[lvl.id] = bestTime;
        }

        final high = _prefs.getInt('shinobi_score_${lvl.id}');
        if (high != null) {
          _levelHighScores[lvl.id] = high;
        }
      }
    } catch (_) {}
  }

  Future<void> _saveProgress() async {
    if (_prefs == null) return;
    try {
      for (final entry in _levelStars.entries) {
        await _prefs.setInt('shinobi_stars_${entry.key}', entry.value);
      }
      for (final entry in _levelFastestTimes.entries) {
        await _prefs.setDouble('shinobi_time_${entry.key}', entry.value);
      }
      for (final entry in _levelHighScores.entries) {
        await _prefs.setInt('shinobi_score_${entry.key}', entry.value);
      }
    } catch (_) {}
  }
}
