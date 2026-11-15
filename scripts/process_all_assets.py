import os
from PIL import Image
import numpy as np

user_uploaded_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b\.user_uploaded"
images_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"
os.makedirs(images_dir, exist_ok=True)

# 1. backdrop_bamboo.png from media_1791003836740.jpg
bg_src = os.path.join(user_uploaded_dir, "media_1791003836740.jpg")
im_bg = Image.open(bg_src)
im_bg.save(os.path.join(images_dir, "backdrop_bamboo.png"))
print("Saved backdrop_bamboo.png")

# Function to remove white/near-white background
def remove_white_bg(src_path, threshold=245):
    im = Image.open(src_path).convert("RGBA")
    arr = np.array(im)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    # White or very light background
    mask = (r >= threshold) & (g >= threshold) & (b >= threshold)
    arr[mask, 3] = 0
    return Image.fromarray(arr)

# 2. props_structures.png from media_1791003847743.jpg
structures_src = os.path.join(user_uploaded_dir, "media_1791003847743.jpg")
im_struct = remove_white_bg(structures_src, threshold=248)
im_struct.save(os.path.join(images_dir, "props_structures.png"))
print("Saved props_structures.png")

# Also crop individual key elements from props_structures:
# Pagoda: center tower
# Hut left:
# Dojo right:
# Let's crop Pagoda from im_struct
w, h = im_struct.size
# Pagoda is centered around x=[350, 650], y=[40, 630]
pagoda = im_struct.crop((350, 45, 650, 635))
pagoda.save(os.path.join(images_dir, "prop_pagoda.png"))
print("Saved prop_pagoda.png", pagoda.size)

# Left mossy hut
hut_left = im_struct.crop((30, 250, 320, 620))
hut_left.save(os.path.join(images_dir, "prop_hut_left.png"))
print("Saved prop_hut_left.png", hut_left.size)

# Right dojo
dojo_right = im_struct.crop((660, 230, 980, 630))
dojo_right.save(os.path.join(images_dir, "prop_dojo_right.png"))
print("Saved prop_dojo_right.png", dojo_right.size)

# 3. props_platforms.png from media_1791003862025.jpg
platforms_src = os.path.join(user_uploaded_dir, "media_1791003862025.jpg")
im_plat = remove_white_bg(platforms_src, threshold=248)
im_plat.save(os.path.join(images_dir, "props_platforms.png"))
print("Saved props_platforms.png")

# Crop arched rope bridge:
# Rope bridge is at the top across x=[30, 960], y=[30, 220]
bridge = im_plat.crop((30, 30, 960, 220))
bridge.save(os.path.join(images_dir, "prop_rope_bridge.png"))
print("Saved prop_rope_bridge.png", bridge.size)

# Crop stone pillars:
pillar1 = im_plat.crop((330, 450, 430, 740))
pillar1.save(os.path.join(images_dir, "prop_stone_pillar.png"))
print("Saved prop_stone_pillar.png", pillar1.size)

# Crop root block platform:
root_block = im_plat.crop((525, 805, 845, 960) if h > 800 else (525, 600, 845, 730))
# Let's detect non-empty bounding box for bottom right root block
root_block_area = im_plat.crop((500, int(h * 0.75), 860, h))
bbox = root_block_area.getbbox()
if bbox:
    root_block = root_block_area.crop(bbox)
    root_block.save(os.path.join(images_dir, "prop_root_block.png"))
    print("Saved prop_root_block.png", root_block.size)

# 4. tileset_ground.png from media_1791003869353.jpg
tileset_src = os.path.join(user_uploaded_dir, "media_1791003869353.jpg")
im_tiles = remove_white_bg(tileset_src, threshold=248)
im_tiles.save(os.path.join(images_dir, "tileset_ground.png"))
print("Saved tileset_ground.png")

# Also crop modular 1x1, 2x1 ground tiles
ground_tile_1 = im_tiles.crop((145, 45, 255, 145))
ground_tile_1.save(os.path.join(images_dir, "tile_ground_1x1.png"))
print("Saved tile_ground_1x1.png", ground_tile_1.size)

ground_tile_2 = im_tiles.crop((380, 45, 500, 145))
ground_tile_2.save(os.path.join(images_dir, "tile_ground_2x1.png"))
print("Saved tile_ground_2x1.png", ground_tile_2.size)

print("All asset processing complete!")
