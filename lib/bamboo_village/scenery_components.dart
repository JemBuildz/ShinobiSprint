import 'dart:math' as math;
import 'dart:ui';
import 'package:flame/components.dart';

/// Parallax background component providing multi-depth scrolling layers:
/// 1. Base layer: Bright sky with sunbeams and distant mountain silhouette
/// 2. Mid layer: Bamboo grove canopy scrolling at 0.2x player speed
/// 3. Scene Backdrop plate (`backdrop_bamboo.png`)
class BambooParallaxComponent extends PositionComponent {
  BambooParallaxComponent({
    required Vector2 size,
    this.backdropSprite,
  }) : super(
          position: Vector2.zero(),
          size: size,
        );

  final Sprite? backdropSprite;
  double _scrollOffset = 0;

  void updateScroll(double playerVelocityX, double dt) {
    // Scroll midground bamboo at 0.2x player speed
    _scrollOffset += playerVelocityX * 0.2 * dt;
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    // 1. Base Layer: Gradient sky & sunbeams
    final skyPaint = Paint()
      ..shader = Gradient.linear(
        Offset.zero,
        Offset(0, size.y * 0.6),
        [
          const Color(0xFF8ED2FF), // Bright azure sky
          const Color(0xFFD6EEFF), // Soft horizon mist
        ],
      );
    canvas.drawRect(Rect.fromLTWH(0, 0, size.x, size.y), skyPaint);

    // Sunbeams / Atmospheric golden glow
    final sunbeamPaint = Paint()
      ..shader = Gradient.radial(
        Offset(size.x * 0.5, size.y * 0.2),
        size.x * 0.45,
        [
          const Color(0x35FFF3D1),
          const Color(0x00FFFFFF),
        ],
      );
    canvas.drawRect(Rect.fromLTWH(0, 0, size.x, size.y * 0.7), sunbeamPaint);

    // Distant mountain silhouette (Mt. Fuji style peaks)
    final mountainPaint = Paint()..color = const Color(0x557B96A8);
    final mountainPath = Path()
      ..moveTo(0, size.y * 0.45)
      ..lineTo(size.x * 0.2, size.y * 0.35)
      ..lineTo(size.x * 0.35, size.y * 0.42)
      ..lineTo(size.x * 0.5, size.y * 0.25)
      ..lineTo(size.x * 0.65, size.y * 0.40)
      ..lineTo(size.x * 0.85, size.y * 0.32)
      ..lineTo(size.x, size.y * 0.44)
      ..lineTo(size.x, size.y)
      ..lineTo(0, size.y)
      ..close();
    canvas.drawPath(mountainPath, mountainPaint);

    // 2. Scene Backdrop Plate (waterfalls, canyon, atmospheric scenery)
    if (backdropSprite != null) {
      backdropSprite!.render(canvas, size: size);
    }

    // 3. Mid layer: Parallax Bamboo Grove Canopy (scrolling at 0.2x)
    _renderBambooCanopy(canvas);
  }

  void _renderBambooCanopy(Canvas canvas) {
    final canopyPaint = Paint()..color = const Color(0x40366835);
    final bambooStalkPaint = Paint()
      ..color = const Color(0x55254A24)
      ..strokeWidth = 5
      ..style = PaintingStyle.stroke;

    // Repeatable bamboo canopy silhouettes in the upper background
    const patternWidth = 320.0;
    final startX = -(_scrollOffset % patternWidth);

    for (var x = startX - patternWidth;
        x < size.x + patternWidth;
        x += patternWidth) {
      // Stalks
      canvas
        ..drawLine(
          Offset(x + 40, 0),
          Offset(x + 50, size.y * 0.35),
          bambooStalkPaint,
        )
        ..drawLine(
          Offset(x + 120, 0),
          Offset(x + 115, size.y * 0.38),
          bambooStalkPaint,
        )
        ..drawLine(
          Offset(x + 220, 0),
          Offset(x + 230, size.y * 0.32),
          bambooStalkPaint,
        )
        // Canopy foliage clusters
        ..drawCircle(Offset(x + 60, size.y * 0.08), 45, canopyPaint)
        ..drawCircle(Offset(x + 140, size.y * 0.06), 55, canopyPaint)
        ..drawCircle(Offset(x + 240, size.y * 0.10), 40, canopyPaint);
    }
  }
}

/// Central Pagoda Tower structure positioned behind the bridge in the canyon.
class PagodaComponent extends SpriteComponent {
  PagodaComponent({
    required Vector2 position,
    required Vector2 size,
    required Sprite sprite,
  }) : super(
          position: position,
          size: size,
          sprite: sprite,
          anchor: Anchor.bottomCenter,
          priority: 5,
        );
}

/// Left cliff wooden mossy shack.
class HutComponent extends SpriteComponent {
  HutComponent({
    required Vector2 position,
    required Vector2 size,
    required Sprite sprite,
  }) : super(
          position: position,
          size: size,
          sprite: sprite,
          anchor: Anchor.bottomLeft,
          priority: 6,
        );
}

/// Right cliff wooden Japanese dojo.
class DojoComponent extends SpriteComponent {
  DojoComponent({
    required Vector2 position,
    required Vector2 size,
    required Sprite sprite,
  }) : super(
          position: position,
          size: size,
          sprite: sprite,
          anchor: Anchor.bottomRight,
          priority: 6,
        );
}

/// Decorative glowing paper lantern with warm subtle pulse animation.
class DecorativeLanternComponent extends PositionComponent {
  DecorativeLanternComponent({
    required Vector2 position,
  }) : super(
          position: position,
          size: Vector2(16, 24),
          anchor: Anchor.topCenter,
          priority: 7,
        );

  double _timer = 0;

  @override
  void update(double dt) {
    super.update(dt);
    _timer += dt * 3.0;
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    final glowRadius = 14.0 + 3.0 * math.sin(_timer);

    final glowPaint = Paint()
      ..shader = Gradient.radial(
        Offset(size.x / 2, size.y / 2),
        glowRadius,
        [
          const Color(0xAAFFAA22),
          const Color(0x00FFAA22),
        ],
      );
    canvas.drawCircle(Offset(size.x / 2, size.y / 2), glowRadius, glowPaint);

    final lanternPaint = Paint()..color = const Color(0xFFFF9800);
    canvas.drawRRect(
      RRect.fromRectAndRadius(
        Rect.fromLTWH(2, 4, size.x - 4, size.y - 8),
        const Radius.circular(4),
      ),
      lanternPaint,
    );

    final trimPaint = Paint()..color = const Color(0xFF3E2723);
    canvas
      ..drawRect(Rect.fromLTWH(1, 2, size.x - 2, 3), trimPaint)
      ..drawRect(Rect.fromLTWH(1, size.y - 5, size.x - 2, 3), trimPaint);
  }
}

/// Composite Midground Environment assembling the pagoda, huts, lanterns,
/// and decorative background foliage.
class MidgroundEnvironment extends PositionComponent {
  MidgroundEnvironment({
    required this.pagodaSprite,
    this.hutSprite,
    this.dojoSprite,
  });

  final Sprite pagodaSprite;
  final Sprite? hutSprite;
  final Sprite? dojoSprite;

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    // Central multi-tier pagoda tower rising behind the canyon bridge
    add(
      PagodaComponent(
        position: Vector2(512, 395),
        size: Vector2(175, 345),
        sprite: pagodaSprite,
      ),
    );

    // Decorative lanterns around the pagoda and bridge entrances
    add(DecorativeLanternComponent(position: Vector2(460, 220)));
    add(DecorativeLanternComponent(position: Vector2(564, 220)));
    add(DecorativeLanternComponent(position: Vector2(300, 360)));
    add(DecorativeLanternComponent(position: Vector2(725, 360)));
  }
}
