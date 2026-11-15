import os
from PIL import Image
import numpy as np
from collections import deque

user_uploaded_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b\.user_uploaded"
images_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"

# --- 1. Clean Torii Gate ---
torii_src = os.path.join(user_uploaded_dir, "media_1791006098523.jpg")
im_p = Image.open(torii_src).convert("RGBA")
# Crop Torii Gate: x=[30, 410], y=[40, 540]
torii_crop = im_p.crop((30, 40, 410, 540))
arr_t = np.array(torii_crop)
h_t, w_t, _ = arr_t.shape

# Flood fill checkerboard from border
visited = np.zeros((h_t, w_t), dtype=bool)
q = deque()
for y in range(h_t):
    for x in [0, w_t-1]:
        q.append((y, x))
        visited[y, x] = True
for x in range(w_t):
    for y in [0, h_t-1]:
        if not visited[y, x]:
            q.append((y, x))
            visited[y, x] = True

bg_mask_t = np.zeros((h_t, w_t), dtype=bool)
while q:
    y, x = q.popleft()
    r, g, b = arr_t[y, x, :3]
    # Checkerboard is dark neutral (r,g,b <= 50, diff <= 15)
    if (max(r, g, b) - min(r, g, b) <= 15) and (max(r, g, b) <= 52):
        bg_mask_t[y, x] = True
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h_t and 0 <= nx < w_t and not visited[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))

arr_t[bg_mask_t, 3] = 0
clean_torii = Image.fromarray(arr_t)
# Crop to bbox
bbox_t = clean_torii.getbbox()
if bbox_t:
    clean_torii = clean_torii.crop(bbox_t)
clean_torii.save(os.path.join(images_dir, "prop_grand_torii.png"))
print("Saved clean prop_grand_torii.png:", clean_torii.size)

# --- 2. Clean Stone Lantern ---
lantern_crop = im_p.crop((440, 70, 550, 255))
arr_l = np.array(lantern_crop)
h_l, w_l, _ = arr_l.shape
visited_l = np.zeros((h_l, w_l), dtype=bool)
q_l = deque()
for y in range(h_l):
    for x in [0, w_l-1]:
        q_l.append((y, x))
        visited_l[y, x] = True
for x in range(w_l):
    for y in [0, h_l-1]:
        if not visited_l[y, x]:
            q_l.append((y, x))
            visited_l[y, x] = True

bg_mask_l = np.zeros((h_l, w_l), dtype=bool)
while q_l:
    y, x = q_l.popleft()
    r, g, b = arr_l[y, x, :3]
    if (max(r, g, b) - min(r, g, b) <= 15) and (max(r, g, b) <= 52):
        bg_mask_l[y, x] = True
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h_l and 0 <= nx < w_l and not visited_l[ny, nx]:
                visited_l[ny, nx] = True
                q_l.append((ny, nx))

arr_l[bg_mask_l, 3] = 0
clean_lantern = Image.fromarray(arr_l)
bbox_l = clean_lantern.getbbox()
if bbox_l:
    clean_lantern = clean_lantern.crop(bbox_l)
clean_lantern.save(os.path.join(images_dir, "prop_stone_lantern_toro.png"))
print("Saved clean prop_stone_lantern_toro.png:", clean_lantern.size)

# --- 3. Clean Bamboo Platforms ---
plat_src = os.path.join(user_uploaded_dir, "media_1791006048526.jpg")
im_plat_full = Image.open(plat_src).convert("RGBA")
# Bamboo platform: x=[20, 265], y=[580, 745]
plat_crop = im_plat_full.crop((20, 580, 265, 745))
arr_p = np.array(plat_crop)
h_p, w_p, _ = arr_p.shape
visited_p = np.zeros((h_p, w_p), dtype=bool)
q_p = deque()
for y in range(h_p):
    for x in [0, w_p-1]:
        q_p.append((y, x))
        visited_p[y, x] = True
for x in range(w_p):
    for y in [0, h_p-1]:
        if not visited_p[y, x]:
            q_p.append((y, x))
            visited_p[y, x] = True

bg_mask_p = np.zeros((h_p, w_p), dtype=bool)
while q_p:
    y, x = q_p.popleft()
    r, g, b = arr_p[y, x, :3]
    if (max(r, g, b) - min(r, g, b) <= 15) and (max(r, g, b) <= 75):
        bg_mask_p[y, x] = True
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h_p and 0 <= nx < w_p and not visited_p[ny, nx]:
                visited_p[ny, nx] = True
                q_p.append((ny, nx))

arr_p[bg_mask_p, 3] = 0
clean_plat = Image.fromarray(arr_p)
bbox_p = clean_plat.getbbox()
if bbox_p:
    clean_plat = clean_plat.crop(bbox_p)
clean_plat.save(os.path.join(images_dir, "prop_bamboo_platform.png"))
print("Saved clean prop_bamboo_platform.png:", clean_plat.size)

# --- 4. Clean Log Bridge ---
bridge_crop = im_plat_full.crop((280, 580, 595, 745))
arr_b = np.array(bridge_crop)
h_b, w_b, _ = arr_b.shape
visited_b = np.zeros((h_b, w_b), dtype=bool)
q_b = deque()
for y in range(h_b):
    for x in [0, w_b-1]:
        q_b.append((y, x))
        visited_b[y, x] = True
for x in range(w_b):
    for y in [0, h_b-1]:
        if not visited_b[y, x]:
            q_b.append((y, x))
            visited_b[y, x] = True

bg_mask_b = np.zeros((h_b, w_b), dtype=bool)
while q_b:
    y, x = q_b.popleft()
    r, g, b = arr_b[y, x, :3]
    if (max(r, g, b) - min(r, g, b) <= 15) and (max(r, g, b) <= 75):
        bg_mask_b[y, x] = True
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h_b and 0 <= nx < w_b and not visited_b[ny, nx]:
                visited_b[ny, nx] = True
                q_b.append((ny, nx))

arr_b[bg_mask_b, 3] = 0
clean_bridge = Image.fromarray(arr_b)
bbox_b = clean_bridge.getbbox()
if bbox_b:
    clean_bridge = clean_bridge.crop(bbox_b)
clean_bridge.save(os.path.join(images_dir, "prop_log_bridge.png"))
print("Saved clean prop_log_bridge.png:", clean_bridge.size)

# --- 5. Clean Layer 2 (Distant Mountains) ---
mountains_src = os.path.join(user_uploaded_dir, "media_1791006019634.png")
im_m = Image.open(mountains_src).convert("RGBA")
arr_m = np.array(im_m)
h_m, w_m, _ = arr_m.shape
# Top section has dark purple checkerboard
# Let's flood fill from top border down to mountain ridge
visited_m = np.zeros((h_m, w_m), dtype=bool)
q_m = deque()
for x in range(w_m):
    q_m.append((0, x))
    visited_m[0, x] = True

bg_mask_m = np.zeros((h_m, w_m), dtype=bool)
while q_m:
    y, x = q_m.popleft()
    r, g, b = arr_m[y, x, :3]
    # Check if checkerboard or very dark/neutral top
    # The mountains are purple (~[70, 50, 80] to [110, 85, 120])
    # The checkerboard is r <= 65, g <= 55, b <= 70
    if (r <= 65 and g <= 58 and b <= 72):
        bg_mask_m[y, x] = True
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h_m and 0 <= nx < w_m and not visited_m[ny, nx]:
                visited_m[ny, nx] = True
                q_m.append((ny, nx))

arr_m[bg_mask_m, 3] = 0
clean_mountains = Image.fromarray(arr_m)
clean_mountains.save(os.path.join(images_dir, "level2_layer2_distant_mountains.png"))
print("Saved clean level2_layer2_distant_mountains.png")

# --- 6. Clean Layer 3 (Midground Bamboo Grove) ---
# Let's cleanly crop off the jagged white top and bottom white bar:
grove_src = os.path.join(user_uploaded_dir, "media_1791006026555.png")
im_g = Image.open(grove_src).convert("RGBA")
arr_g = np.array(im_g)
# Row 75 to 495 has the actual gorgeous bamboo grove and watchtowers!
grove_cropped = im_g.crop((0, 75, 1024, 495))
# Let's add a soft vertical alpha feather at top (first 30px) and bottom (last 30px)
arr_gc = np.array(grove_cropped)
h_gc, w_gc, _ = arr_gc.shape
for y in range(30):
    arr_gc[y, :, 3] = int(255 * (y / 30.0))
for y in range(h_gc - 30, h_gc):
    arr_gc[y, :, 3] = int(255 * ((h_gc - 1 - y) / 30.0))
clean_grove = Image.fromarray(arr_gc)
clean_grove.save(os.path.join(images_dir, "level2_layer3_midground_bamboo.png"))
print("Saved clean level2_layer3_midground_bamboo.png:", clean_grove.size)

# --- 7. Clean Foreground Bamboo (Frame edges only) ---
ff_src = os.path.join(user_uploaded_dir, "media_1791006033724.jpg")
im_ff_raw = Image.open(ff_src).convert("RGBA")
# Crop ONLY the left bamboo stalk (x=[0, 220]) and right bamboo stalk (x=[820, 1024])
# so they act as side frame vignettes instead of blocking the whole center!
arr_ff_l = np.array(im_ff_raw.crop((0, 0, 240, 571)))
arr_ff_r = np.array(im_ff_raw.crop((800, 0, 1024, 571)))

def clean_stalk_side(arr_s):
    h_s, w_s, _ = arr_s.shape
    r, g, b = arr_s[:, :, 0], arr_s[:, :, 1], arr_s[:, :, 2]
    diff = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    # The checkerboard is neutral grey between 75 and 155
    # The stalks are very dark (r,g,b <= 50)
    is_checker = (diff <= 20) & (r >= 70) & (r <= 160)
    arr_s[is_checker, 3] = 0
    return Image.fromarray(arr_s)

clean_stalk_left = clean_stalk_side(arr_ff_l)
clean_stalk_left.save(os.path.join(images_dir, "prop_bamboo_stalk_left.png"))
clean_stalk_right = clean_stalk_side(arr_ff_r)
clean_stalk_right.save(os.path.join(images_dir, "prop_bamboo_stalk_right.png"))
print("Saved clean side bamboo stalks for foreground framing!")
