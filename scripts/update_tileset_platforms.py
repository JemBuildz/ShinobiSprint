import os
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

def update_all_platforms():
    img_path = 'assets/map/tiles/tile_forest_ground_v04.png'
    tsx_path = 'assets/map/tiles/tile_forest_ground_v04.tsx'
    
    # 1. Update TSX with class="Platform"
    with open(tsx_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add class="Platform" where type="Platform" is declared
    content = content.replace('type="Platform"', 'type="Platform" class="Platform"')
    content = content.replace('class="Platform" class="Platform"', 'class="Platform"')
    
    with open(tsx_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("TSX updated with class='Platform'")

    tileset = Image.open(img_path).convert('RGBA')
    midair = Image.open('assets/map/cutouts/boardwalk_elevated.png').convert('RGBA')
    
    # Scale midair to 3 * 64 = 192px wide, 54px high
    midair_3tile = midair.resize((192, 54), Image.Resampling.LANCZOS)
    
    tile_left = midair_3tile.crop((0, 0, 64, 54))
    tile_mid = midair_3tile.crop((64, 0, 128, 54))
    tile_right = midair_3tile.crop((128, 0, 192, 54))
    
    empty_cell = Image.new('RGBA', (64, 64), (0, 0, 0, 0))

    def paste_platform_triple(col_start, row):
        for c in range(3):
            tileset.paste(empty_cell, ((col_start + c) * 68, row * 68))
        tileset.paste(tile_left, (col_start * 68, row * 68), tile_left)
        tileset.paste(tile_mid, ((col_start + 1) * 68, row * 68), tile_mid)
        tileset.paste(tile_right, ((col_start + 2) * 68, row * 68), tile_right)

    # Row 1 platforms (Tiles 11, 12, 13 and 14, 15, 16)
    paste_platform_triple(0, 1)
    paste_platform_triple(3, 1)

    # Row 10 platforms (Tiles 110, 111, 112 / 113, 114, 115)
    paste_platform_triple(0, 10)
    paste_platform_triple(3, 10)

    # Tile 81 (Row 7, Col 4)
    tileset.paste(empty_cell, (4 * 68, 7 * 68))
    tileset.paste(tile_mid, (4 * 68, 7 * 68), tile_mid)

    # Continuous boardwalk ground in Row 3 (Tiles 33..37)
    continuous_deck = Image.open('assets/map/cutouts/boardwalk_continuous.png').convert('RGBA')
    deck_scaled = continuous_deck.resize((5 * 64, 64), Image.Resampling.LANCZOS)
    for i in range(5):
        crop = deck_scaled.crop((i * 64, 0, (i + 1) * 64, 64))
        gx = (i + 1) * 68
        gy = 3 * 68
        tileset.paste(crop, (gx, gy), crop)

    tileset.save(img_path)
    print("All platforms in tile_forest_ground_v04.png completely cleaned!")

if __name__ == '__main__':
    update_all_platforms()
