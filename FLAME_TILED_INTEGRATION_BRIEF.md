# Flame Tiled Integration Brief: Shinobi Sprint Architecture

**Attention: Flame Tiled Agent**  
**Project**: Shinobi Sprint (`super_dash_Remix`)  
**Context**: Hand-Painted Cinematic 2D Platformer Stages  
**Reference Document**: [`CINEMATIC_UNIFIED_PLATE_ARCHITECTURE.md`](./CINEMATIC_UNIFIED_PLATE_ARCHITECTURE.md)

---

## 1. Context: What We Built & Why

We recently unified all 3 canonical levels of Shinobi Sprint:
1. **Level 1: Bamboo Village** (Daytime - Morning Sun & Mt. Fuji) -> [`lib/bamboo_village/main_game.dart`](./lib/bamboo_village/main_game.dart)
2. **Level 2: Twilight Sanctuary** (Sunset - Grand Vermilion Torii Gate) -> [`lib/bamboo_village/twilight_game.dart`](./lib/bamboo_village/twilight_game.dart)
3. **Level 3: Autumn Maple Forest** (Midnight - Crescent Moon & River Bridge) -> [`lib/bamboo_village/autumn_maple_game.dart`](./lib/bamboo_village/autumn_maple_game.dart)

### Crucial Lesson from Visual Testing
Early attempts sliced the hand-painted concept artwork into modular square tile chunks and cut-out props. This caused:
- Severe **"sticker effect"** (props lacked ambient lighting and contact shadows).
- Broken architecture (Torii gate legs severed, disjointed rectangular dirt blocks).
- Camera-obscuring black vertical bars.

We migrated to the **Cinematic Unified-Plate Architecture** (used by *Ori and the Blind Forest*, *Rayman Legends*, and *Hollow Knight*):
- The entire hand-painted 1024x576 illustration remains whole as a **Priority 0 Master Plate** (`assets/images/levelX_cinematic_stage_1024.png`).
- Collision boundaries (`GroundBlockComponent`, one-way `PlatformComponent`) are **invisible physics components** mapped along the painted walkable terrain.
- Sprites are used **strictly** for dynamic entities: Chibi Blue Ninja (`character_ninja.png`), collectible Spirit Orbs (`prop_spirit_orb_clean.png`), spinning shurikens, and ambient particle emitters.

---

## 2. How Flame Tiled Should Integrate with This System

If you are training or implementing **Flame Tiled** (`package:flame_tiled` / Tiled `.tmx` maps), do **NOT** attempt to recreate the visuals with modular tile grid layers (`tilelayer`). Instead, use Tiled for its industry-standard **Object Layers** (`objectgroup`) over the master image plate!

### Recommended Tiled Workflow:
1. **Background Image Layer**:
   - Set the master plate as an `imagelayer` in Tiled (e.g. `assets/images/level1_cinematic_stage_1024.png`).
2. **Object Layer: Collision (`collisions`)**:
   - Place Rectangle or Polygon Objects matching the walkable surfaces:
     - `class: "ground"` -> solid ground (`GroundBlockComponent`)
     - `class: "platform"` -> one-way drop-through platform (`PlatformComponent`, allows `S + Space` drop)
3. **Object Layer: Entities (`entities`)**:
   - `class: "player_spawn"` -> Ninja starting coordinates `(x, y)`
   - `class: "spirit_orb"` -> Dynamic golden collectible orb
   - `class: "hazard_spikes"` -> Static bamboo spike obstacle
   - `class: "hazard_shuriken"` -> Rotating blade hazard
4. **Flame Tiled Loader**:
   - Load map via `TiledComponent.load('level1.tmx', Vector2.all(16))`
   - Iterate over `tiledComponent.tileMap.getLayer<ObjectGroup>('collisions')` and instantiate the corresponding Flame components.

---

## 3. Standard Collision & Physics Reference

### Physics Constants
- **Viewport**: Fixed 16:9 (`1024 x 576`)
- **Player Run Speed**: `180 px/s`
- **Player Jump Velocity**: `-420 px/s`
- **Gravity**: `980 px/s²` (terminal fall `650 px/s`)
- **Drop-Through Action**: `S + Space` (`dropTimer = 0.22s`)

### Master Stage Coordinates Summary

#### Level 1: Bamboo Village (`assets/images/level1_cinematic_stage_1024.png`)
- Left Ground: `(0, 490, 425, 86)`
- Lower Log Bridge: `(415, 490, 175, 16)` (one-way)
- Right Ground: `(575, 490, 449, 86)`
- Elevated Bamboo Table: `(420, 340, 160, 16)` (one-way)
- Right Cliff: `(850, 330, 174, 20)`
- Shack Roof: `(45, 220, 230, 16)`
- Dojo Roof: `(770, 220, 210, 16)`
- Orbs: `(160, 175)`, `(300, 440)`, `(500, 290)`, `(500, 440)`, `(930, 280)`, `(875, 175)`

#### Level 2: Twilight Sanctuary (`assets/images/level2_cinematic_stage_1024.png`)
- Left Ground: `(0, 490, 225, 86)`
- Left Rope Bridge: `(220, 502, 165, 16)` (one-way)
- Center Island: `(380, 490, 265, 86)`
- Right Rope Bridge: `(640, 502, 165, 16)` (one-way)
- Right Ramp: `(800, 490, 105, 16)`
- Right Plateau: `(900, 425, 124, 151)`
- Watchtowers: Left `y=250` & `y=195`; Right `y=250` & `y=195`
- Spike Hazard: `(55, 440, 70, 50)`
- Orbs: `(270, 160)`, `(300, 465)`, `(455, 440)`, `(512, 435)`, `(570, 440)`, `(720, 465)`, `(770, 160)`, `(950, 375)`

#### Level 3: Autumn Maple Forest (`assets/images/level3_cinematic_stage_1024.png`)
- Upper Cliff: `(0, 298, 120, 16)`
- Steps: `(120..240, 310..355)`
- Arched Footbridge: `(310, 375, 455, 18)` (one-way)
- Pagoda Terrace: `(765, 375, 259, 16)`
- River Canyon Banks: Left `(0, 468, 310, 108)`, Right `(740, 468, 284, 108)`
- Shuriken Hazard: `(575, 375, 36, 36)`
- Orbs: `(60, 245)`, `(370, 315)`, `(595, 260)`, `(595, 450)`, `(880, 315)`

---

## 4. Test & Verification
- Unit test suite: `flutter test test/bamboo_village_test.dart` (11/11 passing)
- Static analysis: `flutter analyze lib/bamboo_village` (0 issues)
- Interactive web previews: See `bamboo_village_mobile_preview.html`, `twilight_sanctuary_mobile_preview.html`, and `autumn_maple_mobile_preview.html`.
