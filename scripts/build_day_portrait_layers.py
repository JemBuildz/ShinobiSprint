import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

os.makedirs('assets/images/backgrounds', exist_ok=True)

W, H = 720, 1280

# -------------------------------------------------------------------------
# 1. GENERATE TRUE PORTRAIT DAY SKY & SUN (720 x 1280)
# -------------------------------------------------------------------------
sky = Image.new('RGBA', (W, H), (0, 0, 0, 255))
sky_arr = np.zeros((H, W, 4), dtype=np.uint8)

# Vertical daytime sky gradient:
# Deep azure (#3A86FF) -> Morning sky blue (#64B5F6) -> Warm sun haze (#FFF3E0)
for y in range(H):
    t = y / (H - 1)
    t_ease = t * t * (3 - 2 * t)
    r = int(58 * (1 - t_ease) + 254 * t_ease)
    g = int(134 * (1 - t_ease) + 243 * t_ease)
    b = int(255 * (1 - t_ease) + 224 * t_ease)
    sky_arr[y, :, 0] = r
    sky_arr[y, :, 1] = g
    sky_arr[y, :, 2] = b
    sky_arr[y, :, 3] = 255

sky_img = Image.fromarray(sky_arr, mode='RGBA')
draw_sky = ImageDraw.Draw(sky_img)

# Soft glowing sun (Upper Right)
sun_center_x = 560
sun_center_y = 220
sun_radius = 52

# Outer warm golden solar corona glow
glow_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_img)
for gr in range(sun_radius + 60, sun_radius, -3):
    alpha = int(35 * (1 - (gr - sun_radius) / 60))
    glow_draw.ellipse(
        (sun_center_x - gr, sun_center_y - gr, sun_center_x + gr, sun_center_y + gr),
        fill=(255, 240, 200, alpha)
    )
glow_img = glow_img.filter(ImageFilter.GaussianBlur(15))
sky_img = Image.alpha_composite(sky_img, glow_img)

# Crisp luminous sun disc
sun_mask = Image.new('L', (W, H), 0)
s_draw = ImageDraw.Draw(sun_mask)
s_draw.ellipse(
    (sun_center_x - sun_radius, sun_center_y - sun_radius,
     sun_center_x + sun_radius, sun_center_y + sun_radius),
    fill=255
)
sun_mask = sun_mask.filter(ImageFilter.GaussianBlur(1.0))
sun_surf = Image.new('RGBA', (W, H), (255, 255, 240, 255))
sky_img.paste(sun_surf, (0, 0), sun_mask)

# Soft morning cumulus clouds
cloud_draw = ImageDraw.Draw(sky_img)
np.random.seed(101)
for i in range(12):
    cx = (i * 70 + 40) % (W - 80)
    cy = 140 + (i * 37) % 280
    cw = 70 + (i % 4) * 25
    ch = 22 + (i % 3) * 8
    cloud_draw.ellipse([cx, cy, cx + cw, cy + ch], fill=(255, 255, 255, 140))
    cloud_draw.ellipse([cx + 15, cy - 8, cx + cw - 15, cy + ch], fill=(255, 255, 255, 170))

sky_img = sky_img.filter(ImageFilter.GaussianBlur(0.5))
sky_img.save('assets/images/backgrounds/day_farthest_sky.png')
print("Saved clean portrait daytime sky and sun: 720x1280")

# -------------------------------------------------------------------------
# 2. GENERATE DISTANT DAYTIME MOUNTAINS (720 x 800)
# -------------------------------------------------------------------------
mtn = Image.new('RGBA', (W, 800), (0, 0, 0, 0))
mtn_arr = np.zeros((800, W, 4), dtype=np.uint8)

x_vals = np.linspace(0, 4 * np.pi, W)
h_back = 280 + 70 * np.sin(x_vals * 0.8) + 40 * np.sin(x_vals * 2.1) + 20 * np.cos(x_vals * 3.7)

# Back mountain peaks (soft teal-slate #5B8296)
for x in range(W):
    top_y = int(h_back[x])
    for y in range(top_y, 800):
        fade = 1.0
        if y > 600:
            fade = max(0.0, 1.0 - (y - 600) / 180.0)
        mtn_arr[y, x, 0] = 78
        mtn_arr[y, x, 1] = 118
        mtn_arr[y, x, 2] = 138
        mtn_arr[y, x, 3] = int(220 * fade)

# Mid mountain peaks (closer, lush pine blue-green #3E6B65)
h_mid = 380 + 55 * np.cos(x_vals * 1.1 + 1.2) + 35 * np.sin(x_vals * 2.7)
for x in range(W):
    top_y = int(h_mid[x])
    for y in range(top_y, 800):
        fade = 1.0
        if y > 620:
            fade = max(0.0, 1.0 - (y - 620) / 160.0)
        mtn_arr[y, x, 0] = 52
        mtn_arr[y, x, 1] = 92
        mtn_arr[y, x, 2] = 88
        mtn_arr[y, x, 3] = int(245 * fade)

mtn_img = Image.fromarray(mtn_arr, mode='RGBA')
mtn_img = mtn_img.filter(ImageFilter.GaussianBlur(0.8))
mtn_img.save('assets/images/backgrounds/day_deep_background.png')
print("Saved daytime distant mountains: 720x800")

# -------------------------------------------------------------------------
# 3. GENERATE DAYTIME BAMBOO FOREST & MIST (720 x 700)
# -------------------------------------------------------------------------
bamboo_layer = Image.new('RGBA', (W, 700), (0, 0, 0, 0))
b_draw = ImageDraw.Draw(bamboo_layer)

for i in range(26):
    bx = (i * 28 + (i * 13) % 17) % W
    bw = 6 + (i % 3)
    by_top = 180 + (i * 23) % 100
    # Vibrant bamboo green (#2E7D32)
    b_draw.rectangle([bx, by_top, bx + bw, 700], fill=(46, 125, 50, 215))
    # Joints
    for jy in range(by_top + 40, 700, 50):
        b_draw.line([bx - 2, jy, bx + bw + 2, jy], fill=(56, 142, 60, 235), width=3)
    # Leaves clusters
    for ly in range(by_top + 20, by_top + 160, 45):
        b_draw.polygon([bx, ly, bx - 18, ly - 8, bx, ly - 14], fill=(76, 175, 80, 190))
        b_draw.polygon([bx + bw, ly, bx + bw + 20, ly - 6, bx + bw, ly - 12], fill=(76, 175, 80, 190))

b_arr = np.array(bamboo_layer)
for y in range(500, 700):
    fade = max(0.0, 1.0 - (y - 500) / 190.0)
    b_arr[y, :, 3] = (b_arr[y, :, 3].astype(float) * fade).astype(np.uint8)

bamboo_out = Image.fromarray(b_arr, mode='RGBA')
bamboo_out.save('assets/images/backgrounds/day_mid_background.png')
print("Saved daytime bamboo & morning mist layer: 720x700")
