# Flame 1.38.2 API & Architectural Reference

## 1. Game Lifecycle & Root Structure

In Flame 1.38.2, games inherit from `FlameGame`.

```dart
class MyFlameGame extends FlameGame 
    with HasCollisionDetection, HasKeyboardHandlerComponents {
  
  late final CameraComponent cameraComponent;
  final World world = World();

  @override
  Color backgroundColor() => const Color(0xFF0D0D1A);

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    // Configure viewport & resolution
    cameraComponent = CameraComponent.withFixedResolution(
      width: 1024,
      height: 576,
      world: world,
    );

    await addAll([world, cameraComponent]);
  }
}
```

---

## 2. Component System

### `HasGameReference<T>` vs Legacy `HasGameRef<T>`
Always use `HasGameReference`:
```dart
class NinjaPlayer extends PositionComponent with HasGameReference<MyFlameGame> {
  // Access via `game`, not `gameRef`
  void takeDamage() {
    game.audioController.playSfx('hit.mp3');
  }
}
```

### Component Hierarchy in Flame 1.38
* **World Components**: Added to `world.add(component)`. Coordinates are in world space.
* **HUD / UI Components**: Added to `cameraComponent.viewport.add(component)`. Coordinates are in screen/viewport space.
* **Camera Viewfinder**: Controls zoom, rotation, anchor, and target tracking:
  ```dart
  cameraComponent.follow(player, maxSpeed: 400);
  cameraComponent.viewfinder.zoom = 1.0;
  cameraComponent.viewfinder.anchor = Anchor.center;
  ```

---

## 3. Gestures & Input (1.38 Hit-Testing & Slop)

Flame 1.38 fixed hit testing across complex component trees and introduced touch-slop handling on `DragCallbacks`.

### Available Callback Mixins:
* `TapCallbacks`: `onTapDown(TapDownEvent)`, `onTapUp(TapUpEvent)`, `onTapCancel(TapCancelEvent)`, `onLongTapDown(TapDownEvent)`
* `DragCallbacks`: `onDragStart(DragStartEvent)`, `onDragUpdate(DragUpdateEvent)`, `onDragEnd(DragEndEvent)`, `onDragCancel(DragCancelEvent)`
* `DoubleTapCallbacks`: `onDoubleTapDown(DoubleTapDownEvent)`
* `PointerMoveCallbacks`: `onPointerMove(PointerMoveEvent)`
* `HoverCallbacks`: `onHoverEnter(PointerHoverInfo)`, `onHoverExit(PointerHoverInfo)`

Example:
```dart
class VirtualActionButton extends PositionComponent with TapCallbacks {
  final VoidCallback onTrigger;

  VirtualActionButton({required this.onTrigger, required Vector2 size}) 
      : super(size: size);

  @override
  void onTapDown(TapDownEvent event) {
    event.handled = true;
    onTrigger();
  }
}
```

---

## 4. Collision System

* The game must mix `HasCollisionDetection`.
* Components mix `CollisionCallbacks`.
* Hitboxes are added as children of `PositionComponent`:
  - `RectangleHitbox`
  - `CircleHitbox`
  - `PolygonHitbox`

```dart
class ShurikenHazard extends PositionComponent with CollisionCallbacks {
  @override
  Future<void> onLoad() async {
    await super.onLoad();
    add(CircleHitbox()..collisionType = CollisionType.passive);
  }

  @override
  void onCollisionStart(Set<Vector2> intersectionPoints, PositionComponent other) {
    super.onCollisionStart(intersectionPoints, other);
    if (other is NinjaPlayer) {
      other.defeat();
    }
  }
}
```

---

## 5. Tiled & Cinematic Master Plate Integration

When combining hand-painted plates with Flame Tiled:
1. Master Plate rendered as Priority 0 `SpriteComponent` or `ImageLayer`.
2. Tiled `.tmx` maps provide `ObjectGroup` geometry for:
   - Walkable ground (`GroundBlockComponent`)
   - One-way platforms (`PlatformComponent`)
   - Entity spawn markers (`player_spawn`, `spirit_orb`, `hazard`)
3. Load Tiled objects dynamically without modular grid slicing.
