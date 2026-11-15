import 'dart:async';
import 'dart:ui' as ui;

import 'package:flame/cache.dart';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/sprite.dart';
import 'package:flame/text.dart';
import 'package:flame_tiled/flame_tiled.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:leap/leap.dart';
import 'package:super_dash/audio/audio.dart';
import 'package:super_dash/game/game.dart';
import 'package:super_dash/score/score.dart';
import 'package:super_dash/ui/theme/app_theme.dart';

bool _tsxPackingFilter(Tileset tileset) {
  return !(tileset.source ?? '').startsWith('anim');
}

Paint _layerPaintFactory(double opacity) {
  return Paint()
    ..color = Color.fromRGBO(255, 255, 255, opacity)
    ..isAntiAlias = false;
}

class SuperDashGame extends LeapGame
    with TapDetector, HasKeyboardHandlerComponents {
  SuperDashGame({
    required this.gameBloc,
    required this.audioController,
    this.customBundle,
    this.inMapTester = false,
  }) : super(
          tileSize: 64,
          configuration: const LeapConfiguration(
            tiled: TiledOptions(
              atlasMaxX: 4048,
              atlasMaxY: 4048,
              tsxPackingFilter: _tsxPackingFilter,
              layerPaintFactory: _layerPaintFactory,
              atlasPackingSpacingX: 4,
              atlasPackingSpacingY: 4,
            ),
          ),
        );

  static final _cameraViewport = Vector2(592, 1024);
  static const prefix = 'assets/map/';
  static const _sections = [
    'flutter_runnergame_map_A.tmx',
    'flutter_runnergame_map_B.tmx',
    'flutter_runnergame_map_C.tmx',
  ];
  static const _sectionsBackgroundColor = [
    (AppTheme.nightSkyDarkest, AppTheme.mistyForestBlue),
    (Color(0xFF2C1654), Color(0xFF5E2B5A)),
    (Color(0xFF1F0B18), Color(0xFF4A1525)),
  ];
  static const _sectionsDayBackgroundColor = [
    (Color(0xFF87CEEB), Color(0xFFE0F7FA)),
    (Color(0xFFF39C12), Color(0xFFE67E22)),
    (Color(0xFF8B2500), Color(0xFFD35400)),
  ];

  final GameBloc gameBloc;
  final AssetBundle? customBundle;
  final AudioController audioController;
  final List<VoidCallback> _inputListener = [];

  late final SpriteSheet itemsSpritesheet;
  final bool inMapTester;

  bool _isDaytime = false;

  /// Whether daytime theme is active.
  bool get isDaytime => _isDaytime;
  set isDaytime(bool value) {
    if (_isDaytime != value) {
      _isDaytime = value;
      _setSectionBackground();
    }
  }

  /// Toggles between daytime and nighttime themes.
  void toggleDayNight() {
    isDaytime = !isDaytime;
  }

  GameState get state => gameBloc.state;

  Player? get player => world.firstChild<Player>();

  List<Tileset> get tilesets => leapMap.tiledMap.tileMap.map.tilesets;

  Tileset get itemsTileset {
    return tilesets.firstWhere(
      (tileset) => tileset.name == 'tile_items_v2',
    );
  }

  Tileset get enemiesTileset {
    return tilesets.firstWhere(
      (tileset) => tileset.name == 'tile_enemies_v2',
    );
  }

  void addInputListener(VoidCallback listener) {
    _inputListener.add(listener);
  }

  void removeInputListener(VoidCallback listener) {
    _inputListener.remove(listener);
  }

  void _triggerInputListeners() {
    for (final listener in _inputListener) {
      listener();
    }
  }

  @override
  void onTapDown(TapDownInfo info) {
    super.onTapDown(info);

    _triggerInputListeners();
    overlays.remove('tapToJump');
  }

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    if (inMapTester) {
      _addMapTesterFeatures();
    }

    if (kIsWeb && audioController.isMusicEnabled) {
      audioController.startMusic();
    }

    camera = CameraComponent.withFixedResolution(
      width: _cameraViewport.x,
      height: _cameraViewport.y,
    )..world = world;

    images = Images(
      prefix: prefix,
      bundle: customBundle,
    );

    itemsSpritesheet = SpriteSheet(
      image: await images.load('objects/tile_items_v2.png'),
      srcSize: Vector2.all(tileSize),
    );

    await loadWorldAndMap(
      images: images,
      prefix: prefix,
      bundle: customBundle,
      tiledMapPath: _sections.first,
    );
    _setSectionBackground();

    final player = Player(
      levelSize: leapMap.tiledMap.size.clone(),
      cameraViewport: _cameraViewport,
    );
    unawaited(
      world.addAll([player]),
    );

    await _addSpawners();
    _addTreeHouseFrontLayer();
    _addTreeHouseSign();

    add(
      KeyboardListenerComponent(
        keyDown: {
          LogicalKeyboardKey.space: (_) {
            _triggerInputListeners();
            overlays.remove('tapToJump');
            return false;
          },
          LogicalKeyboardKey.arrowUp: (_) {
            _triggerInputListeners();
            overlays.remove('tapToJump');
            return false;
          },
          LogicalKeyboardKey.keyX: (_) {
            player.katanaSlash();
            return false;
          },
          LogicalKeyboardKey.keyK: (_) {
            player.katanaSlash();
            return false;
          },
          LogicalKeyboardKey.keyZ: (_) {
            player.throwShuriken();
            return false;
          },
          LogicalKeyboardKey.keyJ: (_) {
            player.throwShuriken();
            return false;
          },
        },
        keyUp: {
          LogicalKeyboardKey.space: (_) {
            return false;
          },
          LogicalKeyboardKey.arrowUp: (_) {
            return false;
          },
        },
      ),
    );
  }

  void _addTreeHouseSign() {
    world.addAll([
      TreeSign(
        position: Vector2(
          448,
          1862,
        ),
      ),
      LanternGlowComponent(
        position: Vector2(448, 1840),
        baseRadius: 32,
        isDaytime: _isDaytime,
      ),
    ]);
  }

  void _addTreeHouseFrontLayer() {
    // Suppressed to avoid overlaying the legacy cartoon treehouse branch.
  }

  void _setSectionBackground() {
    final sectionIdx = state.currentSection.clamp(0, _sections.length - 1);
    final colors = _isDaytime
        ? _sectionsDayBackgroundColor[sectionIdx]
        : _sectionsBackgroundColor[sectionIdx];
    final backgroundContainer = Component();

    final gradient = RectangleComponent(
      size: size.clone(),
      paint: Paint()
        ..shader = ui.Gradient.linear(
          Offset.zero,
          Offset(size.x, size.y),
          [
            colors.$1,
            colors.$2,
          ],
        ),
    );
    backgroundContainer.add(gradient);

    final List<ParallaxLayerConfig> layers;
    if (sectionIdx == 1) {
      layers = [
        ParallaxLayerConfig(
          fileName: 'twilight_layer1_sky.png',
          velocityMultiplier: Vector2(0, 0),
        ),
        ParallaxLayerConfig(
          fileName: 'twilight_layer2_mountains.png',
          velocityMultiplier: Vector2(0.25, 0),
        ),
        ParallaxLayerConfig(
          fileName: 'twilight_layer3_grove.png',
          velocityMultiplier: Vector2(0.5, 0),
        ),
      ];
    } else if (sectionIdx == 2) {
      layers = [
        ParallaxLayerConfig(
          fileName: _isDaytime
              ? 'level3_layer1_autumn_sky.png'
              : 'autumn_backdrop_night.png',
          velocityMultiplier: Vector2(0, 0),
        ),
        ParallaxLayerConfig(
          fileName: 'autumn_bridge_arched.png',
          velocityMultiplier: Vector2(0.35, 0),
        ),
      ];
    } else {
      layers = _isDaytime
          ? ParallaxBackground.threeLayerDayHierarchy
          : ParallaxBackground.threeLayerHierarchy;
    }

    final parallax = ParallaxBackground<SuperDashGame>(
      layerConfigs: layers,
      isDaytime: _isDaytime,
      size: size.clone(),
      speed: 25,
    );
    backgroundContainer.add(parallax);

    camera.backdrop = backgroundContainer;
  }

  void gameOver() {
    gameBloc.add(const GameOver());
    // Removed since the result didn't ended up good.
    // Leaving in comment if we decide to bring it back.
    // audioController.stopBackgroundSfx();

    world.firstChild<Player>()?.removeFromParent();

    _resetEntities();

    Future<void>.delayed(
      const Duration(seconds: 1),
      () async {
        await loadWorldAndMap(
          images: images,
          prefix: prefix,
          bundle: customBundle,
          tiledMapPath: _sections.first,
        );
        if (isLastSection || isFirstSection) {
          _addTreeHouseFrontLayer();
        }

        if (isFirstSection) {
          _addTreeHouseSign();
        }
        final newPlayer = Player(
          levelSize: leapMap.tiledMap.size.clone(),
          cameraViewport: _cameraViewport,
        );
        await world.add(newPlayer);

        await newPlayer.mounted;
        await _addSpawners();
        overlays.add('tapToJump');
      },
    );

    if (buildContext != null) {
      final score = gameBloc.state.score;
      Navigator.of(buildContext!).push(
        ScorePage.route(score: score),
      );
    }
  }

  void _resetEntities() {
    children.whereType<ObjectGroupProximityBuilder<Player>>().forEach(
          (spawner) => spawner.removeFromParent(),
        );
    world.firstChild<TreeHouseFront>()?.removeFromParent();
    world.firstChild<TreeSign>()?.removeFromParent();
    world.children
        .whereType<LanternGlowComponent>()
        .forEach((element) => element.removeFromParent());

    try {
      leapMap.children
          .whereType<Enemy>()
          .forEach((enemy) => enemy.removeFromParent());
      leapMap.children
          .whereType<Item>()
          .forEach((enemy) => enemy.removeFromParent());
    } catch (_) {
      // LeapMap not loaded yet
    }
  }

  Future<void> _addSpawners() async {
    await addAll([
      ObjectGroupProximityBuilder<Player>(
        proximity: _cameraViewport.x * 1.5,
        tileLayerName: 'items',
        tileset: itemsTileset,
        componentBuilder: Item.new,
      ),
      ObjectGroupProximityBuilder<Player>(
        proximity: _cameraViewport.x * 1.5,
        tileLayerName: 'enemies',
        tileset: enemiesTileset,
        componentBuilder: Enemy.new,
      ),
    ]);
  }

  Future<void> _loadNewSection() async {
    final nextSection = _sections[state.currentSection];

    _resetEntities();

    try {
      await loadWorldAndMap(
        images: images,
        prefix: prefix,
        bundle: customBundle,
        tiledMapPath: nextSection,
      );
    } catch (_) {
      // Map loading handled in game loop or mocked
    }

    if (isFirstSection) {
      _addTreeHouseSign();
    }

    if (isLastSection || isFirstSection) {
      _addTreeHouseFrontLayer();
    }

    await _addSpawners();
  }

  @override
  void onMapUnload(LeapMap map) {
    player?.velocity.setZero();
  }

  @override
  void onMapLoaded(LeapMap map) {
    player?.loadSpawnPoint();
    player?.loadRespawnPoints();
    player?.walking = true;
    player?.spritePaintColor(Colors.white);
    player?.isPlayerTeleporting = false;

    // Suppress legacy cartoon forest and treehouse layers
    leapMap.tiledMap.tileMap.renderableLayers.removeWhere(
      (renderableLayer) =>
          renderableLayer.layer.name.startsWith('forest_') ||
          renderableLayer.layer.name.startsWith('treehouse_') ||
          renderableLayer.layer.name.contains('decorations'),
    );

    _setSectionBackground();
  }

  void sectionCleared() {
    if (isLastSection) {
      player?.spritePaintColor(Colors.transparent);
      player?.walking = false;
    }

    gameBloc
      ..add(GameScoreIncreased(by: 1000 * state.currentLevel))
      ..add(GameSectionCompleted(sectionCount: _sections.length));

    _loadNewSection();
  }

  bool get isLastSection => state.currentSection == _sections.length - 1;
  bool get isFirstSection => state.currentSection == 0;

  void addCameraDebugger() {
    if (descendants().whereType<CameraDebugger>().isEmpty) {
      final player = world.firstChild<Player>()!;

      final cameraDebugger = CameraDebugger(
        position: player.position.clone(),
      );
      world.add(cameraDebugger);

      final anchor = PlayerCameraAnchor(
        levelSize: leapMap.tiledMap.size.clone(),
        cameraViewport: _cameraViewport,
      );
      cameraDebugger.add(anchor);
      camera.follow(anchor);

      final proximityBuilders =
          descendants().whereType<ObjectGroupProximityBuilder<Player>>();
      for (final proximityBuilder in proximityBuilders) {
        proximityBuilder.currentReference = cameraDebugger;
      }

      player.removeFromParent();
    }
  }

  void toggleInvincibility() {
    player?.isPlayerInvincible = !(player?.isPlayerInvincible ?? false);
  }

  void teleportPlayerToEnd() {
    player?.x = leapMap.tiledMap.size.x - (player?.size.x ?? 0) * 10 * 4;
    if (state.currentSection == 2) {
      player?.y = (player?.y ?? 0) - (tileSize * 4);
    }
  }

  void showHitBoxes() {
    void show() {
      descendants()
          .whereType<PhysicalEntity>()
          .where(
            (element) =>
                element is Player || element is Item || element is Enemy,
          )
          .forEach((entity) => entity.debugMode = true);
    }

    show();
    add(
      TimerComponent(
        period: 1,
        repeat: true,
        onTick: show,
      ),
    );
  }

  void _addMapTesterFeatures() {
    add(FpsComponent());
    add(
      FpsTextComponent(
        position: Vector2(0, 0),
        textRenderer: TextPaint(
          style: const TextStyle(
            color: Colors.white,
            fontSize: 20,
          ),
        ),
      ),
    );
  }
}
