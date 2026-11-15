import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/shinobi_sprint/models/shinobi_level.dart';
import 'package:super_dash/shinobi_sprint/models/shinobi_progress.dart';

void main() {
  group('Shinobi Campaign Architecture & Level Catalog', () {
    test('contains exactly 3 Worlds with 5 levels each (15 levels total)', () {
      expect(ShinobiWorld.values.length, equals(3));
      expect(ShinobiCampaign.allLevels.length, equals(15));

      for (final world in ShinobiWorld.values) {
        expect(world.levels.length, equals(5));
      }
    });

    test('World 1 (Dawn Village) matches user specifications', () {
      final w1 = ShinobiWorld.dawnVillage.levels;

      // Level 1-1: Tutorial — Collect 3 ground orbs, learn jump
      expect(w1[0].id, equals('1-1'));
      expect(w1[0].totalOrbs, equals(3));
      expect(w1[0].isTimeTrial, isFalse);

      // Level 1-2: Elevation — 6 orbs on rooftops, learn drop-through
      expect(w1[1].id, equals('1-2'));
      expect(w1[1].totalOrbs, equals(6));

      // Level 1-3: Time Trial — 6 orbs under 25 seconds
      expect(w1[2].id, equals('1-3'));
      expect(w1[2].totalOrbs, equals(6));
      expect(w1[2].isTimeTrial, isTrue);
      expect(w1[2].timeLimit, equals(25));

      // Level 1-4: Bridge Patrol — 2 foes
      expect(w1[3].id, equals('1-4'));
      expect(w1[3].hasFoes, isTrue);
      expect(w1[3].foesPositions.length, equals(2));

      // Level 1-5: Dawn Village Climax — 10 orbs
      expect(w1[4].id, equals('1-5'));
      expect(w1[4].totalOrbs, equals(10));
    });

    test(
      'World 2 (Twilight Sanctuary) has watchtower jumps & spike hazards',
      () {
        final w2 = ShinobiWorld.twilightSanctuary.levels;
        expect(w2.length, equals(5));
        expect(w2[0].hasSpikes, isTrue); // 2-1 has spikes
        expect(w2[1].totalOrbs, equals(6)); // 2-2 watchtower
        expect(w2[2].isTimeTrial, isTrue); // 2-3 double chasm dash
        expect(w2[4].totalOrbs, equals(8)); // 2-5 climax
      },
    );

    test('World 3 (Midnight Autumn) has shuriken hazards & finale', () {
      final w3 = ShinobiWorld.midnightAutumn.levels;
      expect(w3.length, equals(5));
      expect(w3[1].hasShurikens, isTrue); // 3-2 bridge traps
      expect(w3[2].isTimeTrial, isTrue); // 3-3 speed run
      expect(w3[2].timeLimit, equals(22)); // 22s
      expect(w3[4].isFinalLevel, isTrue); // 3-5 finale
    });

    test('level progression sequentially links from 1-1 to 3-5', () {
      var current = ShinobiCampaign.level1_1;
      var count = 1;

      while (current.nextLevel != null) {
        current = current.nextLevel!;
        count++;
      }

      expect(count, equals(15));
      expect(current.id, equals('3-5'));
      expect(current.isFinalLevel, isTrue);
    });

    test(
      'ShinobiProgressController unlocks next level and tracks stars',
      () async {
        final progress = ShinobiProgressController();

      expect(progress.isLevelUnlocked('1-1'), isTrue);
      expect(progress.isLevelUnlocked('1-2'), isFalse);
      expect(progress.totalStars, equals(0));

      await progress.recordLevelCompletion(
        level: ShinobiCampaign.level1_1,
        starsEarned: 3,
        timeElapsed: 12.5,
      );

      expect(progress.getStarsForLevel('1-1'), equals(3));
      expect(progress.totalStars, equals(3));
      expect(progress.isLevelUnlocked('1-2'), isTrue);
      expect(progress.getFastestTimeForLevel('1-1'), equals(12.5));
    });
  });
}
