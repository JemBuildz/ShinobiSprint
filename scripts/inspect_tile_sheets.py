from PIL import Image

targets = [
    'assets/map/objects/tile_forest_trees_front_v02.png',
    'assets/map/objects/tile_forest_trees_back_v02.png',
    'assets/map/tiles/tile_decorations_v01.png',
    'assets/map/tiles/tile_gate_v2.png',
    'assets/map/tiles/tile_forest_ground_v04.png',
]

for t in targets:
    try:
        im = Image.open(t)
        print(f"{t}: size={im.size}, mode={im.mode}")
    except Exception as e:
        print(f"Error {t}: {e}")
