import os
from PIL import Image
import numpy as np

user_uploaded_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b\.user_uploaded"
images_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"
out_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b"

# ==============================================================================
# 1. CLEAN DISTANT MOUNTAINS LAYER (media_1791006019634.png)
# ==============================================================================
# The mountain ridge line in media_1791006019634.png:
# Rows above the mountain ridge have the 16x16 checkerboard ([0,0,0] & [61,54,68]).
# Below the ridge, the artwork is solid purple silhouettes and mist!
m_img = Image.open(os.path.join(user_uploaded_dir, "media_1791006019634.png")).convert("RGBA")
m_arr = np.array(m_img)
h_m, w_m, _ = m_arr.shape

# For each column x, find where the mountain begins by scanning from bottom up:
# The mountain is solid from the bottom up to the silhouette edge.
# In the sky area above the mountain, pixels are either [0,0,0] or [61,54,68] (neutral grey/black).
# Mountain pixels have distinctive purple / silhouette hue: r > 10 or (not matching checkerboard).
# Let's detect the mountain silhouette edge per column:
ridge_y = np.zeros(w_m, dtype=int)
for x in range(w_m):
    # Scan from y=0 down to find the first pixel that is NOT checkerboard
    first_mountain = h_m - 1
    for y in range(0, h_m):
        r, g, b = m_arr[y, x, :3]
        # Check if checkerboard:
        # either very dark black (r<=10, g<=10, b<=10) or grey (50<=r<=75, 42<=g<=66, 56<=b<=80)
        is_bg = (r <= 12 and g <= 12 and b <= 12) or (abs(int(r)-61) <= 12 and abs(int(g)-54) <= 12 and abs(int(b)-68) <= 12)
        if not is_bg:
            first_mountain = y
            break
    ridge_y[x] = first_mountain

# Smooth the ridge slightly to remove 1px single-pixel noise
for x in range(1, w_m - 1):
    med = int(np.median([ridge_y[x-1], ridge_y[x], ridge_y[x+1]]))
    ridge_y[x] = med

# Create clean mask: everything above ridge_y[x] is transparent (0), everything at or below is opaque (255)
# Add a 2px soft anti-aliased edge
clean_m_arr = m_arr.copy()
for x in range(w_m):
    ry = ridge_y[x]
    clean_m_arr[:max(0, ry - 1), x, 3] = 0
    if ry > 0:
        clean_m_arr[ry - 1, x, 3] = 128
    clean_m_arr[ry:, x, 3] = 255

clean_mountains = Image.fromarray(clean_m_arr)
clean_mountains.save(os.path.join(images_dir, "level2_layer2_distant_mountains.png"))
print("Saved clean solid distant mountains (no holes!):", clean_mountains.size)

# ==============================================================================
# 2. CLEAN TORII GATE (media_1791006098523.jpg)
# ==============================================================================
im_props_raw = Image.open(os.path.join(user_uploaded_dir, "media_1791006098523.jpg")).convert("RGBA")
torii_raw = im_props_raw.crop((30, 40, 410, 540))
t_arr = np.array(torii_raw)

# The checkerboard in media_1791006098523.jpg is strictly neutral dark (R,G,B <= 46, |R-G|<=8, |G-B|<=8)
# The Torii gate has warm red/orange/wood colors:
# (R > G + 15 or R > 60 or max(R,G,B) > 52)
r_t, g_t, b_t = t_arr[:, :, 0], t_arr[:, :, 1], t_arr[:, :, 2]
diff_t = np.maximum(np.maximum(r_t, g_t), b_t) - np.minimum(np.minimum(r_t, g_t), b_t)
is_bg_t = (r_t <= 46) & (g_t <= 46) & (b_t <= 46) & (diff_t <= 10)

t_arr[is_bg_t, 3] = 0
clean_torii = Image.fromarray(t_arr)
bbox_t = clean_torii.getbbox()
if bbox_t:
    clean_torii = clean_torii.crop(bbox_t)
clean_torii.save(os.path.join(images_dir, "prop_grand_torii.png"))
print("Saved clean prop_grand_torii.png:", clean_torii.size)

# ==============================================================================
# 3. CLEAN STONE LANTERN
# ==============================================================================
lantern_raw = im_props_raw.crop((440, 70, 550, 255))
l_arr = np.array(lantern_raw)
r_l, g_l, b_l = l_arr[:, :, 0], l_arr[:, :, 1], l_arr[:, :, 2]
diff_l = np.maximum(np.maximum(r_l, g_l), b_l) - np.minimum(np.minimum(r_l, g_l), b_l)
is_bg_l = (r_l <= 46) & (g_l <= 46) & (b_l <= 46) & (diff_l <= 10)
l_arr[is_bg_l, 3] = 0
clean_lantern = Image.fromarray(l_arr)
bbox_l = clean_lantern.getbbox()
if bbox_l:
    clean_lantern = clean_lantern.crop(bbox_l)
clean_lantern.save(os.path.join(images_dir, "prop_stone_lantern_toro.png"))
print("Saved clean prop_stone_lantern_toro.png:", clean_lantern.size)

# ==============================================================================
# 4. CLEAN BAMBOO PLATFORMS & LOG BRIDGE
# ==============================================================================
im_plat_raw = Image.open(os.path.join(user_uploaded_dir, "media_1791006048526.jpg")).convert("RGBA")
# Bamboo platform: x=[20, 270], y=[580, 745]
p_crop = im_plat_raw.crop((20, 580, 270, 745))
p_arr = np.array(p_crop)
r_p, g_p, b_p = p_arr[:, :, 0], p_arr[:, :, 1], p_arr[:, :, 2]
diff_p = np.maximum(np.maximum(r_p, g_p), b_p) - np.minimum(np.minimum(r_p, g_p), b_p)
is_bg_p = (r_p <= 72) & (g_p <= 72) & (b_p <= 72) & (diff_p <= 12)
p_arr[is_bg_p, 3] = 0
clean_plat = Image.fromarray(p_arr)
bbox_p = clean_plat.getbbox()
if bbox_p:
    clean_plat = clean_plat.crop(bbox_p)
clean_plat.save(os.path.join(images_dir, "prop_bamboo_platform.png"))
print("Saved clean prop_bamboo_platform.png:", clean_plat.size)

# Log bridge: x=[280, 595], y=[580, 745]
b_crop = im_plat_raw.crop((280, 580, 595, 745))
b_arr = np.array(b_crop)
r_b, g_b, b_b = b_arr[:, :, 0], b_arr[:, :, 1], b_arr[:, :, 2]
diff_b = np.maximum(np.maximum(r_b, g_b), b_b) - np.minimum(np.minimum(r_b, g_b), b_b)
is_bg_b = (r_b <= 72) & (g_b <= 72) & (b_b <= 72) & (diff_b <= 12)
b_arr[is_bg_b, 3] = 0
clean_bridge = Image.fromarray(b_arr)
bbox_b = clean_bridge.getbbox()
if bbox_b:
    clean_bridge = clean_bridge.crop(bbox_b)
clean_bridge.save(os.path.join(images_dir, "prop_log_bridge.png"))
print("Saved clean prop_log_bridge.png:", clean_bridge.size)

# ==============================================================================
# 5. TEST COMPOSITE WITH NEW CLEAN ASSETS
# ==============================================================================
W, H = 1024, 576
canvas = Image.new("RGBA", (W, H), (12, 16, 26, 255))

# 1. Sky Sunset (Layer 1)
sky = Image.open(os.path.join(images_dir, "level2_layer1_sky_sunset.png")).convert("RGBA").resize((W, H))
canvas.paste(sky, (0, 0), sky)

# 2. Solid Mountains (Layer 2) - Clean silhouette, NO holes!
canvas.paste(clean_mountains, (0, 0), clean_mountains)

# 3. Ground Platforms (Left cliff & Right cliff)
root = Image.open(os.path.join(images_dir, "prop_root_block.png")).convert("RGBA")
canvas.paste(root.resize((320, 136)), (0, 440), root.resize((320, 136)))
canvas.paste(root.resize((320, 136)), (704, 440), root.resize((320, 136)))

# 4. Grand Torii Gate (At entrance on left cliff)
torii_scaled = clean_torii.resize((150, 200))
canvas.paste(torii_scaled, (50, 440 - 195), torii_scaled)

# 5. Stone Toro Lanterns
canvas.paste(clean_lantern.resize((42, 70)), (210, 440 - 68), clean_lantern.resize((42, 70)))
canvas.paste(clean_lantern.resize((42, 70)), (760, 440 - 68), clean_lantern.resize((42, 70)))

# 6. Elevated Bamboo Platform & Log Bridge across the central chasm
canvas.paste(clean_plat.resize((160, 80)), (260, 360), clean_plat.resize((160, 80)))
canvas.paste(clean_bridge.resize((175, 80)), (420, 360), clean_bridge.resize((175, 80)))
canvas.paste(clean_plat.resize((160, 80)), (595, 330), clean_plat.resize((160, 80)))

# 7. Ninja Player
ninja = Image.open(os.path.join(images_dir, "character_ninja.png")).convert("RGBA").resize((56, 58))
canvas.paste(ninja, (140, 440 - 58), ninja)

canvas.save(os.path.join(out_dir, "test_composite_v4.png"))
print("Saved perfect test composite v4 to", os.path.join(out_dir, "test_composite_v4.png"))
