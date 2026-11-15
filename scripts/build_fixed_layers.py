import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

os.makedirs('assets/images/backgrounds', exist_ok=True)
os.makedirs('assets/map/cutouts', exist_ok=True)

# -------------------------------------------------------------------------
# 1. GENERATE TRUE PORTRAIT SKY & MOON (NO STRETCHING, 1:1 CIRCULAR MOON)
# -------------------------------------------------------------------------
# Dimensions: 720 x 1280 (True mobile portrait HD)
W, H = 720, 1280

sky = Image.new('RGBA', (W, H), (0, 0, 0, 255))
sky_arr = np.zeros((H, W, 4), dtype=np.uint8)

# Vertical night gradient: #040711 (top) -> #090E1D (mid) -> #141C33 (bottom)
for y in range(H):
    t = y / (H - 1)
    # Smooth cubic ease
    t_ease = t * t * (3 - 2 * t)
    r = int(4 * (1 - t_ease) + 20 * t_ease)
    g = int(7 * (1 - t_ease) + 28 * t_ease)
    b = int(17 * (1 - t_ease) + 51 * t_ease)
    sky_arr[y, :, 0] = r
    sky_arr[y, :, 1] = g
    sky_arr[y, :, 2] = b
    sky_arr[y, :, 3] = 255

sky_img = Image.fromarray(sky_arr, mode='RGBA')
draw_sky = ImageDraw.Draw(sky_img)

# Twinkling stars (pseudo-random deterministic)
np.random.seed(42)
num_stars = 140
star_x = np.random.randint(20, W - 20, size=num_stars)
star_y = np.random.randint(30, int(H * 0.65), size=num_stars)
star_brightness = np.random.randint(140, 255, size=num_stars)
star_sizes = np.random.choice([1, 1, 1, 2, 2, 3], size=num_stars)

for x, y, b, sz in zip(star_x, star_y, star_brightness, star_sizes):
    col = (b, b, min(255, b + 20), b)
    if sz == 1:
        sky_img.putpixel((int(x), int(y)), col)
    else:
        draw_sky.ellipse((x - sz/2, y - sz/2, x + sz/2, y + sz/2), fill=col)

# Crescent Moon (Upper Left, perfectly circular aspect ratio 1:1)
moon_center_x = 160
moon_center_y = 220
moon_radius = 54

# Outer soft moonlight glow
glow_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_img)
for gr in range(moon_radius + 45, moon_radius, -3):
    alpha = int(22 * (1 - (gr - moon_radius) / 45))
    glow_draw.ellipse(
        (moon_center_x - gr, moon_center_y - gr, moon_center_x + gr, moon_center_y + gr),
        fill=(220, 235, 255, alpha)
    )
glow_img = glow_img.filter(ImageFilter.GaussianBlur(12))
sky_img = Image.alpha_composite(sky_img, glow_img)

# Crisp crescent moon
moon_mask = Image.new('L', (W, H), 0)
m_draw = ImageDraw.Draw(moon_mask)
# Outer circle
m_draw.ellipse(
    (moon_center_x - moon_radius, moon_center_y - moon_radius, 
     moon_center_x + moon_radius, moon_center_y + moon_radius),
    fill=255
)
# Inner shadow circle offsetting to create crescent
offset_x = 22
offset_y = -8
inner_radius = 48
m_draw.ellipse(
    (moon_center_x - inner_radius + offset_x, moon_center_y - inner_radius + offset_y,
     moon_center_x + inner_radius + offset_x, moon_center_y + inner_radius + offset_y),
    fill=0
)
moon_mask = moon_mask.filter(ImageFilter.GaussianBlur(0.6))

# Fill moon color: soft pale silver-white (#F1F5F9 to #E2E8F0)
moon_surf = Image.new('RGBA', (W, H), (245, 248, 255, 255))
sky_img.paste(moon_surf, (0, 0), moon_mask)

sky_img.save('assets/images/backgrounds/farthest_sky.png')
sky_img.save('assets/images/backgrounds/night_farthest_sky.png')
print("Saved clean portrait sky and 1:1 crescent moon: 720x1280")

# -------------------------------------------------------------------------
# 2. GENERATE DISTANT MOUNTAINS WITH SEAMLESS FOG FADE (NO HARSH CUT SEAM)
# -------------------------------------------------------------------------
# Canvas: 720 x 800
mtn = Image.new('RGBA', (W, 800), (0, 0, 0, 0))
mtn_arr = np.zeros((800, W, 4), dtype=np.uint8)

# Layer 1: Back mountain peaks (dark blue-slate #131B2E)
# Procedural ridge height
x_vals = np.linspace(0, 4 * np.pi, W)
h_back = 280 + 70 * np.sin(x_vals * 0.8) + 40 * np.sin(x_vals * 2.1) + 20 * np.cos(x_vals * 3.7)

for x in range(W):
    top_y = int(h_back[x])
    for y in range(top_y, 800):
        # Soft vertical alpha fade towards bottom
        fade = 1.0
        if y > 600:
            fade = max(0.0, 1.0 - (y - 600) / 180.0)
        mtn_arr[y, x, 0] = 16
        mtn_arr[y, x, 1] = 24
        mtn_arr[y, x, 2] = 42
        mtn_arr[y, x, 3] = int(220 * fade)

# Layer 2: Mid mountain peaks (closer, #0E1524)
h_mid = 380 + 55 * np.cos(x_vals * 1.1 + 1.2) + 35 * np.sin(x_vals * 2.7)
for x in range(W):
    top_y = int(h_mid[x])
    for y in range(top_y, 800):
        fade = 1.0
        if y > 620:
            fade = max(0.0, 1.0 - (y - 620) / 160.0)
        mtn_arr[y, x, 0] = 12
        mtn_arr[y, x, 1] = 18
        mtn_arr[y, x, 2] = 34
        mtn_arr[y, x, 3] = int(245 * fade)

mtn_img = Image.fromarray(mtn_arr, mode='RGBA')
mtn_img = mtn_img.filter(ImageFilter.GaussianBlur(0.8))
mtn_img.save('assets/images/backgrounds/deep_background.png')
mtn_img.save('assets/images/backgrounds/night_deep_background.png')
print("Saved blended distant mountains: 720x800 (seamless fog fade)")

# -------------------------------------------------------------------------
# 3. GENERATE BAMBOO FOREST & MIST (MIDGROUND LAYER)
# -------------------------------------------------------------------------
bamboo_layer = Image.new('RGBA', (W, 700), (0, 0, 0, 0))
b_draw = ImageDraw.Draw(bamboo_layer)

# Bamboo silhouette stalks across width
for i in range(26):
    bx = (i * 28 + (i * 13) % 17) % W
    bw = 6 + (i % 3)
    by_top = 180 + (i * 23) % 100
    # Stalk
    b_draw.rectangle([bx, by_top, bx + bw, 700], fill=(10, 16, 26, 210))
    # Joints
    for jy in range(by_top + 40, 700, 50):
        b_draw.line([bx - 2, jy, bx + bw + 2, jy], fill=(16, 24, 38, 230), width=3)
    # Leaves clusters
    for ly in range(by_top + 20, by_top + 160, 45):
        b_draw.polygon([bx, ly, bx - 18, ly - 8, bx, ly - 14], fill=(14, 22, 34, 180))
        b_draw.polygon([bx + bw, ly, bx + bw + 20, ly - 6, bx + bw, ly - 12], fill=(14, 22, 34, 180))

# Apply vertical fog fade to bamboo layer bottom
b_arr = np.array(bamboo_layer)
for y in range(500, 700):
    fade = max(0.0, 1.0 - (y - 500) / 190.0)
    b_arr[y, :, 3] = (b_arr[y, :, 3].astype(float) * fade).astype(np.uint8)

bamboo_out = Image.fromarray(b_arr, mode='RGBA')
bamboo_out.save('assets/images/backgrounds/mid_background.png')
bamboo_out.save('assets/images/backgrounds/night_mid_background.png')
print("Saved seamless midground bamboo & mist layer: 720x700")

# -------------------------------------------------------------------------
# 4. GENERATE CONTINUOUS FOREGROUND BOARDWALK GROUND TILE (748 x 816)
# -------------------------------------------------------------------------
# Replace tile_forest_ground_v04.png with solid continuous boardwalk structure
orig_ground = Image.open('assets/map/tiles/tile_forest_ground_v04.png').convert('RGBA')
orig_g_arr = np.array(orig_ground)
gh, gw = orig_g_arr.shape[:2]
g_alpha = orig_g_arr[:, :, 3]

# Create dark cedar boardwalk platform texture
cedar_arr = np.zeros_like(orig_g_arr)
y_idx, x_idx = np.indices((gh, gw))

# Vertical plank seams every 24px
seam_mask = (x_idx % 24 == 0) | (x_idx % 24 == 1)

# Polished cedar colors
# Top surface highlight: #B07442 (176, 116, 66)
# Mid wood plank: #754424 (117, 68, 36)
# Dark wood shadow / grain: #422413 (66, 36, 19)
# Deep timber frame: #27140B (39, 20, 11)

# Base dark cedar
cedar_arr[:, :, 0] = 72 + ((x_idx * 5 + y_idx * 3) % 15).astype(np.uint8)
cedar_arr[:, :, 1] = 42 + ((x_idx * 5 + y_idx * 3) % 11).astype(np.uint8)
cedar_arr[:, :, 2] = 24 + ((x_idx * 5 + y_idx * 3) % 7).astype(np.uint8)
cedar_arr[:, :, 3] = g_alpha

# Top 12px walking surface of platforms has warm golden-amber cedar plank finish
is_top_plank = (y_idx % 68 < 16) & (g_alpha > 100)
cedar_arr[is_top_plank, 0] = 168 + ((x_idx[is_top_plank] * 7) % 20).astype(np.uint8)
cedar_arr[is_top_plank, 1] = 104 + ((x_idx[is_top_plank] * 7) % 14).astype(np.uint8)
cedar_arr[is_top_plank, 2] = 56 + ((x_idx[is_top_plank] * 7) % 9).astype(np.uint8)

# Vertical dark plank seams
cedar_arr[seam_mask & (g_alpha > 0), 0] = 30
cedar_arr[seam_mask & (g_alpha > 0), 1] = 16
cedar_arr[seam_mask & (g_alpha > 0), 2] = 9

final_ground = Image.fromarray(cedar_arr, mode='RGBA')
final_ground.save('assets/map/tiles/tile_forest_ground_v04.png')
print("Saved polished cedar ground tileset: 748x816")
