import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:super_dash/ui/theme/app_theme.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('AppTheme', () {
    test('defines nocturnal dark blues palette', () {
      expect(AppTheme.nightSkyDarkest, equals(const Color(0xFF090D1A)));
      expect(AppTheme.nightSkyDeep, equals(const Color(0xFF0F172A)));
      expect(AppTheme.mountainRidgeBlue, equals(const Color(0xFF1E293B)));
      expect(AppTheme.mistyForestBlue, equals(const Color(0xFF2A3A4E)));
      expect(AppTheme.riverStreamBlue, equals(const Color(0xFF1B3B4B)));
    });

    test('defines glowing lantern oranges palette', () {
      expect(AppTheme.lanternCoreGlow, equals(const Color(0xFFFFB74D)));
      expect(AppTheme.lanternAmber, equals(const Color(0xFFFFA726)));
      expect(AppTheme.lanternEmber, equals(const Color(0xFFFF7043)));
      expect(AppTheme.lacquerRed, equals(const Color(0xFFB71C1C)));
    });

    test('defines wooden textures and antique gold palette', () {
      expect(AppTheme.woodDarkCedar, equals(const Color(0xFF1A0E08)));
      expect(AppTheme.woodTimber, equals(const Color(0xFF2A180E)));
      expect(AppTheme.antiqueGold, equals(const Color(0xFFC5A059)));
      expect(AppTheme.goldLeaf, equals(const Color(0xFFFFD54F)));
      expect(AppTheme.parchmentCream, equals(const Color(0xFFFFF7ED)));
    });

    test('provides functional gradients and decorations', () {
      expect(AppTheme.nightSkyGradient.colors.length, equals(3));
      expect(AppTheme.lanternFlameGradient.colors.length, equals(3));
      expect(AppTheme.woodenPlaqueDecoration.border, isNotNull);
      expect(AppTheme.hudContainerDecoration.borderRadius, isNotNull);
    });

    test('provides ThemeData configured for East Asian night aesthetic', () {
      final theme = AppTheme.theme;
      expect(theme.brightness, equals(Brightness.dark));
      expect(theme.scaffoldBackgroundColor, equals(AppTheme.nightSkyDarkest));
      expect(theme.primaryColor, equals(AppTheme.lanternAmber));
      expect(theme.colorScheme.primary, equals(AppTheme.lanternAmber));
      expect(theme.cardColor, equals(AppTheme.woodDarkCedar));
    });
  });
}
