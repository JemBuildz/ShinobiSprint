import 'package:app_ui/app_ui.dart';
import 'package:flutter/material.dart';

/// Unified design system and theme for Shinobi Sprint,
/// capturing the East Asian night-time forest aesthetic:
/// deep indigo skies, glowing lantern oranges, and rich cedar wood textures.
class AppTheme {
  const AppTheme._();

  // ---------------------------------------------------------------------------
  // Dark Blues & Nocturnal Palette (Extracted from Night Sky & Mountains)
  // ---------------------------------------------------------------------------

  /// The darkest night sky indigo, representing the deep celestial horizon.
  static const Color nightSkyDarkest = Color(0xFF090D1A);

  /// Deep midnight blue of the celestial sky and mountain silhouettes.
  static const Color nightSkyDeep = Color(0xFF0F172A);

  /// Mountain ridge nocturnal blue, visible in the distant pagoda silhouettes.
  static const Color mountainRidgeBlue = Color(0xFF1E293B);

  /// Misty bamboo forest blue-gray, reflecting ambient night fog.
  static const Color mistyForestBlue = Color(0xFF2A3A4E);

  /// Night-time river stream teal/cyan, catching lantern reflections.
  static const Color riverStreamBlue = Color(0xFF1B3B4B);

  /// Ethereal celestial nebula teal/cyan glowing near the crescent moon.
  static const Color celestialCyan = Color(0xFF38BDF8);

  // ---------------------------------------------------------------------------
  // Glowing Lantern Oranges & Flame Highlights
  // ---------------------------------------------------------------------------

  /// Radiant core incandescent flame glow inside stone lanterns.
  static const Color lanternCoreGlow = Color(0xFFFFB74D);

  /// Warm amber flame color radiating across wooden posts and paths.
  static const Color lanternAmber = Color(0xFFFFA726);

  /// Deep burning ember orange seen in the glowing lanterns.
  static const Color lanternEmber = Color(0xFFFF7043);

  /// Intense fiery orange for active triggers and glowing effects.
  static const Color lanternFire = Color(0xFFF97316);

  /// Warrior lacquer red used on banners, seals, and torii gates.
  static const Color lacquerRed = Color(0xFFB71C1C);

  /// Deep lacquer crimson for container borders and stamps.
  static const Color lacquerCrimson = Color(0xFF7F1D1D);

  // ---------------------------------------------------------------------------
  // Wooden Textures & Traditional Materials
  // ---------------------------------------------------------------------------

  /// Deep charred cedar wood grain (yakisugi), used for plaque backdrops.
  static const Color woodDarkCedar = Color(0xFF1A0E08);

  /// Aged Japanese timber/hinoki for card backgrounds and container bevels.
  static const Color woodTimber = Color(0xFF2A180E);

  /// Warm wooden plank brown, matching the foreground bridge walkway.
  static const Color woodPlank = Color(0xFF3E2314);

  /// Weathered wood edge accent and border trim.
  static const Color woodBevel = Color(0xFF5C361D);

  /// Antique golden brass lacquer used on ornamental corners and trims.
  static const Color antiqueGold = Color(0xFFC5A059);

  /// Polished yellow gold leaf for highlighted icons and emblems.
  static const Color goldLeaf = Color(0xFFFFD54F);

  /// Light cream parchment paper for legible text against dark surfaces.
  static const Color parchmentCream = Color(0xFFFFF7ED);

  /// Warm parchment golden-beige for subtitles and metadata labels.
  static const Color parchmentGold = Color(0xFFE2C99B);

  /// Muted sumi-ink ash for secondary descriptions.
  static const Color sumiInkMuted = Color(0xFF94A3B8);

  // ---------------------------------------------------------------------------
  // Gradients
  // ---------------------------------------------------------------------------

  /// Nocturnal linear gradient matching the night sky parallax layers.
  static const LinearGradient nightSkyGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [
      nightSkyDarkest,
      nightSkyDeep,
      mountainRidgeBlue,
    ],
  );

  /// Glowing lantern flame gradient for buttons and highlighted elements.
  static const LinearGradient lanternFlameGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      lanternCoreGlow,
      lanternAmber,
      lanternEmber,
    ],
  );

  /// Traditional warrior red lacquer gradient for primary action buttons.
  static const LinearGradient lacquerButtonGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [
      Color(0xFFB71C1C),
      Color(0xFF881313),
      Color(0xFF5A0808),
    ],
  );

  /// Rich dark cedar wood plaque gradient.
  static const LinearGradient woodPlaqueGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFF381F12),
      Color(0xFF26140A),
      Color(0xFF1A0D06),
    ],
  );

  /// HUD translucent night-blue acrylic gradient for game score and controls.
  static const LinearGradient hudGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xEE0F172A),
      Color(0xEE1E293B),
    ],
  );

  // ---------------------------------------------------------------------------
  // Pre-configured BoxDecorations
  // ---------------------------------------------------------------------------

  /// Carved cedar wood plaque decoration with antique gold border
  /// and deep shadow.
  static BoxDecoration get woodenPlaqueDecoration => BoxDecoration(
        borderRadius: BorderRadius.circular(18),
        gradient: woodPlaqueGradient,
        border: Border.all(
          color: antiqueGold,
          width: 2.2,
        ),
        boxShadow: const [
          BoxShadow(
            color: Colors.black87,
            blurRadius: 28,
            spreadRadius: 4,
            offset: Offset(0, 10),
          ),
          BoxShadow(
            color: Color(0x40FFA726),
            blurRadius: 10,
            spreadRadius: -2,
          ),
        ],
      );

  /// Translucent HUD pill container decoration with lantern glow accent.
  static BoxDecoration get hudContainerDecoration => BoxDecoration(
        borderRadius: BorderRadius.circular(30),
        gradient: hudGradient,
        border: Border.all(
          color: const Color(0xD9C5A059),
          width: 1.5,
        ),
        boxShadow: const [
          BoxShadow(
            color: Colors.black54,
            blurRadius: 12,
            offset: Offset(0, 4),
          ),
          BoxShadow(
            color: Color(0x33FFB74D),
            blurRadius: 6,
            spreadRadius: -1,
          ),
        ],
      );

  /// Glowing lantern circular button decoration.
  static BoxDecoration get lanternButtonDecoration => BoxDecoration(
        shape: BoxShape.circle,
        gradient: const RadialGradient(
          colors: [
            lanternCoreGlow,
            lanternAmber,
            woodTimber,
          ],
        ),
        border: Border.all(
          color: goldLeaf,
          width: 1.8,
        ),
        boxShadow: const [
          BoxShadow(
            color: Color(0x80FF7043),
            blurRadius: 12,
            spreadRadius: 2,
          ),
        ],
      );

  // ---------------------------------------------------------------------------
  // Flutter ThemeData Definition
  // ---------------------------------------------------------------------------

  /// The official ThemeData for Shinobi Sprint.
  static ThemeData get theme => ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: nightSkyDarkest,
        primaryColor: lanternAmber,
        colorScheme: const ColorScheme(
          brightness: Brightness.dark,
          primary: lanternAmber,
          onPrimary: Colors.black,
          secondary: goldLeaf,
          onSecondary: Colors.black,
          error: Color(0xFFEF4444),
          onError: Colors.white,
          surface: nightSkyDeep,
          onSurface: parchmentCream,
        ),
        textTheme: AppTextStyles.textTheme.apply(
          bodyColor: parchmentCream,
          displayColor: parchmentGold,
        ),
        cardColor: woodDarkCedar,
        dialogTheme: const DialogThemeData(
          backgroundColor: woodDarkCedar,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: lacquerRed,
            foregroundColor: parchmentCream,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
              side: const BorderSide(color: goldLeaf, width: 1.5),
            ),
          ),
        ),
      );

  /// Backwards-compatible alias for MaterialApp theme setup.
  static ThemeData get standard => theme;
}
