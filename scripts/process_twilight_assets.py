import os
from PIL import Image
import numpy as np
from collections import deque

user_uploaded_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b\.user_uploaded"
images_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"
os.makedirs(images_dir, exist_ok=True)

# 1. Sky & Celestial Layer
sky_src = os.path.join(user_uploaded_dir, "media_1791006012788.png")
im_sky = Image.open(sky_src)
im_sky.save(os.path.join(images_dir, "twilight_layer1_sky.png"))
print("Saved twilight_layer1_sky.png:", im_sky.size)

# Helper function to remove dark checkerboard from outer boundary using flood fill
def remove_dark_checkerboard(src_path, max_diff=25, max_val=80):
    im = Image.open(src_path).convert("RGBA")
    arr = np.array(im)
    h, w, _ = arr.shape
    
    visited = np.zeros((h, w), dtype=bool)
    q = deque()
    
    # Push border pixels
    for y in range(h):
        for x in [0, w-1]:
            q.append((y, x))
            visited[y, x] = True
    for x in range(w):
        for y in [0, h-1]:
            if not visited[y, x]:
                q.append((y, x))
                visited[y, x] = True
                
    def is_checker(r, g, b):
        # Dark checkerboard has low brightness and is neutral
        return (max(r, g, b) - min(r, g, b) <= max_diff) and (max(r, g, b) <= max_val)

    bg_mask = np.zeros((h, w), dtype=bool)
    while q:
        y, x = q.popleft()
        r, g, b = arr[y, x, :3]
        if is_checker(r, g, b):
            bg_mask[y, x] = True
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                    visited[ny, nx] = True
                    q.append((ny, nx))
                    
    arr[bg_mask, 3] = 0
    return Image.fromarray(arr)

# 2. Distant Mountains Layer (media_1791006019634.png)
# The checkerboard is at the top sky section (r,g,b <= 75 and neutral)
mountains_src = os.path.join(user_uploaded_dir, "media_1791006019634.png")
im_mountains = remove_dark_checkerboard(mountains_src, max_diff=25, max_val=75)
im_mountains.save(os.path.join(images_dir, "twilight_layer2_mountains.png"))
print("Saved twilight_layer2_mountains.png")

# 3. Midground Grove Layer (media_1791006026555.png)
# Has white and black borders at top/bottom
grove_src = os.path.join(user_uploaded_dir, "media_1791006026555.png")
im_grove = Image.open(grove_src).convert("RGBA")
arr_grove = np.array(im_grove)
# Mask pure black/white outside areas at top and bottom
r, g, b = arr_grove[:, :, 0], arr_grove[:, :, 1], arr_grove[:, :, 2]
is_white = (r >= 250) & (g >= 250) & (b >= 250)
# Top black cutout:
y_indices = np.arange(arr_grove.shape[0])[:, None]
is_top_black = (y_indices < 100) & (r <= 10) & (g <= 10) & (b <= 10)
arr_grove[is_white | is_top_black, 3] = 0
im_grove_clean = Image.fromarray(arr_grove)
im_grove_clean.save(os.path.join(images_dir, "twilight_layer3_grove.png"))
print("Saved twilight_layer3_grove.png")

# 4. Foreground Bamboo & Fireflies (media_1791006033724.jpg)
# Dark/mid grey checkerboard (values ~90 to 145, neutral)
ff_src = os.path.join(user_uploaded_dir, "media_1791006033724.jpg")
im_ff = Image.open(ff_src).convert("RGBA")
arr_ff = np.array(im_ff)
h_ff, w_ff, _ = arr_ff.shape

# Fireflies are bright yellow/gold (R > 180, G > 140, B < 150)
# Bamboo stalks are dark silhouette (R < 35, G < 35, B < 35)
# Checkerboard is neutral grey between 75 and 150
r_ff, g_ff, b_ff = arr_ff[:, :, 0], arr_ff[:, :, 1], arr_ff[:, :, 2]
diff_ff = np.maximum(np.maximum(r_ff, g_ff), b_ff) - np.minimum(np.minimum(r_ff, g_ff), b_ff)
is_checker_ff = (diff_ff <= 18) & (r_ff >= 75) & (r_ff <= 155)
arr_ff[is_checker_ff, 3] = 0
im_ff_clean = Image.fromarray(arr_ff)
im_ff_clean.save(os.path.join(images_dir, "twilight_layer4_fireflies.png"))
print("Saved twilight_layer4_fireflies.png")

# 5. Platforms & Tiles Sheet (media_1791006048526.jpg)
plat_src = os.path.join(user_uploaded_dir, "media_1791006048526.jpg")
im_plat = remove_dark_checkerboard(plat_src, max_diff=25, max_val=85)
im_plat.save(os.path.join(images_dir, "twilight_props_platforms.png"))
print("Saved twilight_props_platforms.png")

# Crop specific platforms from sheet:
# Top-left bamboo platform: x=[20, 265], y=[570, 740] (approx)
# Let's inspect coordinates of top bamboo platform and bridge:
# Platform: x=[20, 260], y=[580, 740]
# Log rope bridge: x=[280, 580], y=[580, 740]
# Bamboo pole: x=[660, 700], y=[570, 960]
# Autumn ground cube: x=[610, 750], y=[25, 195]
# Autumn slope: x=[520, 740], y=[290, 520]

crop_bamboo_plat = im_plat.crop((20, 580, 270, 745))
crop_bamboo_plat.save(os.path.join(images_dir, "prop_bamboo_platform.png"))
print("Saved prop_bamboo_platform.png", crop_bamboo_plat.size)

crop_log_bridge = im_plat.crop((280, 580, 595, 745))
crop_log_bridge.save(os.path.join(images_dir, "prop_log_bridge.png"))
print("Saved prop_log_bridge.png", crop_log_bridge.size)

crop_autumn_block = im_plat.crop((610, 25, 755, 195))
crop_autumn_block.save(os.path.join(images_dir, "tile_autumn_block.png"))
print("Saved tile_autumn_block.png", crop_autumn_block.size)

crop_autumn_slope = im_plat.crop((520, 280, 740, 520))
crop_autumn_slope.save(os.path.join(images_dir, "tile_autumn_slope.png"))
print("Saved tile_autumn_slope.png", crop_autumn_slope.size)

# 6. Props & Hazards Sheet (media_1791006098523.jpg)
props_src = os.path.join(user_uploaded_dir, "media_1791006098523.jpg")
im_props = remove_dark_checkerboard(props_src, max_diff=25, max_val=60)
im_props.save(os.path.join(images_dir, "twilight_props_hazards.png"))
print("Saved twilight_props_hazards.png")

# Crop specific props & hazards:
# Grand Torii gate: x=[30, 410], y=[40, 540]
torii = im_props.crop((30, 40, 410, 540))
torii.save(os.path.join(images_dir, "prop_grand_torii.png"))
print("Saved prop_grand_torii.png", torii.size)

# Stone lantern Toro: x=[440, 550], y=[70, 255]
lantern = im_props.crop((440, 70, 550, 255))
lantern.save(os.path.join(images_dir, "prop_stone_lantern_toro.png"))
print("Saved prop_stone_lantern_toro.png", lantern.size)

# Bamboo wind chimes Furin: x=[770, 940], y=[60, 450]
chimes = im_props.crop((770, 60, 940, 450))
chimes.save(os.path.join(images_dir, "prop_wind_chimes.png"))
print("Saved prop_wind_chimes.png", chimes.size)

# Sharpened bamboo spikes: x=[50, 365], y=[630, 960]
spikes = im_props.crop((50, 630, 365, 960))
spikes.save(os.path.join(images_dir, "hazard_bamboo_spikes.png"))
print("Saved hazard_bamboo_spikes.png", spikes.size)

# Spinning shuriken: x=[440, 580], y=[640, 780]
shuriken = im_props.crop((440, 640, 580, 780))
shuriken.save(os.path.join(images_dir, "hazard_shuriken.png"))
print("Saved hazard_shuriken.png", shuriken.size)

# Glowing spirit orb: x=[830, 890], y=[750, 825]
orb = im_props.crop((830, 750, 890, 825))
orb.save(os.path.join(images_dir, "item_spirit_orb.png"))
print("Saved item_spirit_orb.png", orb.size)

print("All Twilight level assets extracted successfully!")
