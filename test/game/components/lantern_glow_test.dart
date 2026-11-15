import 'dart:ui';

import 'package:flame/game.dart';
import 'package:flame_test/flame_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/game/components/lantern_glow.dart';

class _TestGame extends FlameGame {}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('LanternGlowComponent', () {
    test('initializes with nominal radius and warm amber hue', () {
      final glow = LanternGlowComponent();

      expect(glow.baseRadius, equals(24));
      expect(glow.pulseAmplitude, equals(4));
      expect(glow.pulseFrequency, equals(3));
      expect(glow.glowColor, equals(const Color(0xFFFF9800)));
      expect(glow.innerGlowColor, equals(const Color(0xFFFFF3E0)));
      expect(glow.isDaytime, isFalse);
      expect(glow.currentIntensity, equals(1));
      expect(glow.currentRadius, greaterThan(0));
    });

    test('currentIntensity and radius update based on isDaytime', () {
      final glow = LanternGlowComponent();

      // Nighttime: fully active
      expect(glow.isDaytime, isFalse);
      expect(glow.currentIntensity, equals(1));
      expect(glow.currentRadius, greaterThan(0));

      // Daytime: powered down
      glow.isDaytime = true;
      expect(glow.isDaytime, isTrue);
      expect(glow.currentIntensity, equals(0));
      expect(glow.currentRadius, equals(0));
    });

    test('currentRadius pulses dynamically over time with micro-flicker', () {
      final glow = LanternGlowComponent(
        pulseAmplitude: 6,
        pulseFrequency: 2,
      );

      final r0 = glow.currentRadius;
      glow.update(0.3);
      final r1 = glow.currentRadius;

      expect(r0, isNot(equals(r1)));
      expect(r1, inInclusiveRange(16.0, 32.0));
    });

    testWithGame<_TestGame>(
      'mounts in Flame game tree and renders without error',
      _TestGame.new,
      (game) async {
        final glow = LanternGlowComponent(position: Vector2(100, 100));
        await game.ensureAdd(glow);

        expect(glow.isMounted, isTrue);

        final recorder = PictureRecorder();
        final canvas = Canvas(recorder);
        glow.render(canvas);
        final picture = recorder.endRecording();
        expect(picture, isNotNull);
      },
    );
  });
}
