from PIL import Image

def analyze_sheet(path):
    im = Image.open(path)
    print(f"\n--- {path} ({im.size}) ---")
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # Find bounding box of non-zero alpha
    bbox = im.getbbox()
    print(f"Total non-transparent bbox: {bbox}")

analyze_sheet('assets/map/tiles/tile_decorations_v01.png')
analyze_sheet('assets/map/tiles/tile_gate_v2.png')
analyze_sheet('assets/map/objects/tile_forest_trees_front_v02.png')
analyze_sheet('assets/map/objects/tile_forest_trees_back_v02.png')
