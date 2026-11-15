---
name: flame-engine
description: Comprehensive architecture, APIs, and modern development standards for the Flame Game Engine (v1.38.x+). Use when building games, components, behaviors, gestures/events, cameras, collisions, or migrating legacy Flame code.
metadata:
  version: "1.38.2"
  category: GameDevelopment
---

# Flame Game Engine (1.38.x) Development Guide

This guide establishes the architecture and best practices for developing games using **Flame 1.38.x** in Flutter/Dart, based on the [Flame 1.38.2 Documentation](https://pub.dev/documentation/flame/1.38.2/).

---

## 1. Core Architecture: World & Camera System

Flame 1.38 uses the modern **CameraComponent + World** paradigm (replacing the legacy `Camera` and direct root component rendering).

### Standard Game Structure
```dart
class MyGame extends FlameGame with HasCollisionDetection {
  late final CameraComponent cameraComponent;
  final World world = World();

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    // 1. Set up camera with the world
    cameraComponent = CameraComponent.withFixedResolution(
      width: 640,
      height: 360,
      world: world,
    );

    // 2. Add both to the game root
    await addAll([world, cameraComponent]);

    // 3. Add world components to the world (NOT directly to the game root)
    await world.add(Player());
  }
}
```

* **Game Elements**: Placed inside `world` (players, enemies, terrain, items).
* **HUD & UI**: Placed inside `cameraComponent.viewport` (scores, health bars, virtual joysticks).
* **Viewports & Viewfinders**: Use `cameraComponent.viewfinder` for zoom, rotation, and anchors; use `cameraComponent.follow(target)` for tracking.

---

## 2. Component Referencing: `HasGameReference`

> **BREAKING / MODERN PATTERN:** In Flame 1.38+, **never** use `HasGameRef<T>`. Use **`HasGameReference<T>`**.

* `HasGameRef` is deprecated and causes subtle memory leaks.
* `HasGameReference<T>` provides typed access to the game via `game` (instead of `gameRef`).

```dart
// ❌ Deprecated:
class MyItem extends PositionComponent with HasGameRef<MyGame> {
  void doSomething() {
    print(gameRef.size);
  }
}

// ✅ Modern (1.38+):
class MyItem extends PositionComponent with HasGameReference<MyGame> {
  void doSomething() {
    print(game.size);
  }
}
```

---

## 3. Input & Event Handling (Flame 1.38.x Updates)

Flame 1.38 refactored `GestureDetectorBuilder` and hit-testing:
* Input callbacks on components (`TapCallbacks`, `DragCallbacks`, `DoubleTapCallbacks`) require that the game or components include the relevant callback mixins.
* Hit-testing correctly traces scene-graph transformations and respects touch-slop on drags to avoid accidental clicks/jitter on touch screens.

### Modern Input Mixins
* **Component-Level Taps**: Mix `TapCallbacks` onto `PositionComponent` and implement `onTapDown`, `onTapUp`, `onTapCancel`.
* **Component-Level Drags**: Mix `DragCallbacks` onto `PositionComponent` and implement `onDragStart`, `onDragUpdate`, `onDragEnd`.
* **Keyboard Handling**: Add `HasKeyboardHandlerComponents` to `FlameGame`, and mix `KeyboardHandler` on target components (or use `KeyboardListenerComponent`).

```dart
class InteractiveButton extends PositionComponent with TapCallbacks {
  @override
  void onTapDown(TapDownEvent event) {
    // React to tap down
    event.handled = true; // Mark event handled if it shouldn't bubble
  }

  @override
  void onTapUp(TapUpEvent event) {
    // Action triggered
  }
}
```

---

## 4. Collision Detection

Always use `HasCollisionDetection` on `FlameGame`:

```dart
class MyGame extends FlameGame with HasCollisionDetection { ... }
```

In components:
* Mix `CollisionCallbacks` onto `PositionComponent`.
* Attach hitboxes (`RectangleHitbox`, `CircleHitbox`, or `PolygonHitbox`).
* Override `onCollisionStart`, `onCollision`, or `onCollisionEnd`.

```dart
class Obstacle extends PositionComponent with CollisionCallbacks {
  @override
  Future<void> onLoad() async {
    await super.onLoad();
    add(RectangleHitbox());
  }

  @override
  void onCollisionStart(
    Set<Vector2> intersectionPoints,
    PositionComponent other,
  ) {
    super.onCollisionStart(intersectionPoints, other);
    if (other is Player) {
      // Handle player hit
    }
  }
}
```

---

## 5. Behavior-Driven Design (`flame_behaviors`)

When using `flame_behaviors` (as in Super Dash):
* **Entities**: Extend `Entity` (which is a `PositionComponent`).
* **Behaviors**: Extend `Behavior<EntityT>`.
* Keep game logic out of raw components; place logic into composable, testable behaviors.

```dart
class Player extends Entity with HasGameReference<SuperDashGame> {
  Player() : super(behaviors: [PlayerMovementBehavior(), JumpBehavior()]);
}

class PlayerMovementBehavior extends Behavior<Player> {
  @override
  void update(double dt) {
    super.update(dt);
    // Entity physics/position updates
    parent.position.x += 100 * dt;
  }
}
```

---

## 6. Performance & Lifecycle Optimization

* **Component Pooling / Removal**: Use `removeFromParent()` cleanly.
* **Sprite & Image Caching**: Preload assets via `images.load()` or `game.images.loadAll()` in `onLoad()`.
* **Delta Time (`dt`)**: Always multiply continuous movement/transformations by `dt`.
* **Avoid unnecessary object allocation in `update(double dt)` or `render(Canvas canvas)`**: Reuse vectors and paints instead of instantiating new objects each frame.
