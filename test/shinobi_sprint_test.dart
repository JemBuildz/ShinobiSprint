import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/bamboo_village/autumn_maple_game.dart';
import 'package:super_dash/bamboo_village/main_game.dart';
import 'package:super_dash/bamboo_village/twilight_game.dart';
import 'package:super_dash/shinobi_sprint/models/shinobi_level.dart';
import 'package:super_dash/shinobi_sprint/models/shinobi_stage.dart';
import 'package:super_dash/shinobi_sprint/view/shinobi_stage_select_page.dart';
import 'package:super_dash/shinobi_sprint/view/shinobi_stage_view.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('Shinobi Sprint Stage Progression & Architecture', () {
    test(
      'ShinobiStage enum contains all 3 canonical stages with valid metadata',
      () {
        expect(ShinobiStage.values.length, equals(3));

        // Stage 1: Bamboo Village
        const s1 = ShinobiStage.bambooVillage;
        expect(s1.id, equals(1));
        expect(s1.locationName, equals('Bamboo Village'));
        expect(s1.timeOfDay, equals('Morning Dawn'));
        expect(s1.totalOrbs, equals(6));
        expect(s1.nextStage, equals(ShinobiStage.twilightSanctuary));
        expect(s1.isFinalStage, isFalse);
        expect(s1.buildGame(), isA<MainGame>());

        // Stage 2: Twilight Sanctuary
        const s2 = ShinobiStage.twilightSanctuary;
        expect(s2.id, equals(2));
        expect(s2.locationName, equals('Twilight Sanctuary'));
        expect(s2.timeOfDay, equals('Golden Sunset'));
        expect(s2.totalOrbs, equals(8));
        expect(s2.nextStage, equals(ShinobiStage.autumnMaple));
        expect(s2.isFinalStage, isFalse);
        expect(s2.buildGame(), isA<TwilightSanctuaryGame>());

        // Stage 3: Autumn Maple Forest
        const s3 = ShinobiStage.autumnMaple;
        expect(s3.id, equals(3));
        expect(s3.locationName, equals('Autumn Maple Forest'));
        expect(s3.timeOfDay, equals('Midnight Moon'));
        expect(s3.totalOrbs, equals(6));
        expect(s3.nextStage, isNull);
        expect(s3.isFinalStage, isTrue);
        expect(s3.buildGame(), isA<AutumnMapleGame>());
      },
    );

    testWidgets(
      'ShinobiStageSelectPage renders all 3 Acts tabs and campaign header',
      (tester) async {
        await tester.binding.setSurfaceSize(const Size(1024, 768));

        await tester.pumpWidget(
          const MaterialApp(
            home: ShinobiStageSelectPage(),
          ),
        );

        // Verify Header & Total Campaign Stars
        expect(find.text('SHINOBI SPRINT'), findsOneWidget);
        expect(find.textContaining('45'), findsOneWidget);

        // Verify All 3 Acts Tabs
        expect(find.text('ACT I: DAWN'), findsOneWidget);
        expect(find.text('ACT II: TWILIGHT'), findsOneWidget);
        expect(find.text('ACT III: MIDNIGHT'), findsOneWidget);
      },
    );

    testWidgets(
      'ShinobiStageView renders HUD, orbs counter, and debug controls',
      (tester) async {
        await tester.binding.setSurfaceSize(const Size(1024, 576));

        await tester.pumpWidget(
          const MaterialApp(
            home: ShinobiStageView(),
          ),
        );

        // Verify Stage title
        expect(find.text('Stage 1: Bamboo Village'), findsOneWidget);

        // Verify initial orb count
        expect(find.text('0 / 6 ORBS'), findsOneWidget);

        // Verify Hitbox toggle button
        expect(find.byIcon(Icons.visibility_off_outlined), findsOneWidget);

        // Verify On-Screen Touch Control buttons
        expect(find.byIcon(Icons.arrow_upward), findsOneWidget);
        expect(find.text('DROP'), findsOneWidget);
        expect(find.text('SLASH'), findsOneWidget);
        expect(find.text('SHURIKEN'), findsOneWidget);

        // Tap Hitbox button to toggle
        await tester.tap(find.byIcon(Icons.visibility_off_outlined));
        await tester.pump();
        expect(find.byIcon(Icons.visibility), findsOneWidget);
      },
    );

    testWidgets(
      'ShinobiStageView can launch Stage 3 directly with 6 orbs target',
      (tester) async {
        await tester.binding.setSurfaceSize(const Size(1024, 576));

        await tester.pumpWidget(
          const MaterialApp(
            home: ShinobiStageView(
              initialStage: ShinobiStage.autumnMaple,
            ),
          ),
        );

        // Verify Stage 3 HUD
        expect(find.text('Stage 3: Autumn Maple Forest'), findsOneWidget);
        expect(find.text('0 / 6 ORBS'), findsOneWidget);
      },
    );

    test('ShinobiLevel.buildGame binds onHazardHit callback', () {
      var hitCount = 0;
      final game = ShinobiCampaign.level1_1.buildGame(
        onHazardHit: () => hitCount++,
      );
      expect(game, isA<MainGame>());
      final mainGame = game as MainGame;
      expect(mainGame.onHazardHit, isNotNull);
      mainGame.onHazardHit?.call();
      expect(hitCount, equals(1));
    });

    test('ShinobiStage.buildGame binds onHazardHit callback', () {
      var hitCount = 0;
      final game = ShinobiStage.twilightSanctuary.buildGame(
        onHazardHit: () => hitCount++,
      );
      expect(game, isA<TwilightSanctuaryGame>());
      final twGame = game as TwilightSanctuaryGame;
      expect(twGame.onHazardHit, isNotNull);
      twGame.onHazardHit?.call();
      expect(hitCount, equals(1));
    });
  });
}
