import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

os.makedirs('assets/images/backgrounds', exist_ok=True)
W, H = 720, 1280

# -------------------------------------------------------------------------
# 1. UPGRADED DISTANT MOUNTAINS & MIST (assets/images/backgrounds/deep_background.png)
# -------------------------------------------------------------------------
# Dimensions: 720 x 800
mtn_w, mtn_h = 720, 800
mtn_img = Image.new('RGBA', (mtn_w, mtn_h), (0, 0, 0, 0))
mtn_draw = ImageDraw.Draw(mtn_img)

# Layer 1: Distant Misty Ridge (Dark blue-slate #162035)
x_vals = np.linspace(0, 4 * np.pi, mtn_w)
h_back = 240 + 60 * np.sin(x_vals * 0.9) + 35 * np.cos(x_vals * 2.3) + 18 * np.sin(x_vals * 4.1)

back_points = [(0, mtn_h)]
for x in range(mtn_w):
    back_points.append((x, int(h_back[x])))
back_points.append((mtn_w, mtn_h))
mtn_draw.polygon(back_points, fill=(22, 32, 54, 210))

# Soft moonlight rim highlight along the back ridge top
for x in range(mtn_w):
    ry = int(h_back[x])
    mtn_img.putpixel((x, ry), (65, 85, 130, 180))
    if ry + 1 < mtn_h:
        mtn_img.putpixel((x, ry + 1), (45, 62, 95, 200))

# Layer 2: Mid-Distant Mountain Ridge (#11182B)
h_mid = 340 + 75 * np.cos(x_vals * 1.2 + 1.4) + 40 * np.sin(x_vals * 2.8)
mid_points = [(0, mtn_h)]
for x in range(mtn_w):
    mid_points.append((x, int(h_mid[x])))
mid_points.append((mtn_w, mtn_h))
mtn_draw.polygon(mid_points, fill=(17, 24, 43, 240))

# Small pine tree silhouettes on the mid ridge
np.random.seed(101)
for i in range(45):
    tx = int(i * 16 + (i * 7) % 11) % mtn_w
    ty = int(h_mid[tx])
    th = int(12 + (i % 5) * 4)
    # Draw tiny triangular pine silhouette
    mtn_draw.polygon([
        (tx, ty - th),
        (tx - int(th * 0.35), ty + 2),
        (tx + int(th * 0.35), ty + 2),
    ], fill=(13, 19, 34, 255))

# Layer 3: Closer Valley Hills & Plateau (#0C1221)
h_front = 450 + 50 * np.sin(x_vals * 1.5 + 0.8) + 30 * np.cos(x_vals * 3.1)
front_points = [(0, mtn_h)]
for x in range(mtn_w):
    front_points.append((x, int(h_front[x])))
front_points.append((mtn_w, mtn_h))
mtn_draw.polygon(front_points, fill=(12, 18, 33, 255))

# Layer 4: Volumetric Mist & Valley Fog (rolling between ridges)
# Gradient mist at y: 320..420 and y: 550..800
mtn_arr = np.array(mtn_img, dtype=float)

# Mid-valley mist band (diffuse cyan-indigo moonlight fog)
y_coords, x_coords = np.indices((mtn_h, mtn_w))
mist_mask = np.exp(-((y_coords - 390) ** 2) / (2 * 45 ** 2))
mtn_arr[:, :, 0] += mist_mask * 30
mtn_arr[:, :, 1] += mist_mask * 42
mtn_arr[:, :, 2] += mist_mask * 70
mtn_arr[:, :, 3] = np.maximum(mtn_arr[:, :, 3], mist_mask * 140)

# Bottom valley mist fade (seamless transparent transition to foreground)
for y in range(600, mtn_h):
    fade = max(0.0, 1.0 - (y - 600) / 180.0)
    mtn_arr[y, :, 3] = mtn_arr[y, :, 3] * fade

mtn_arr = np.clip(mtn_arr, 0, 255).astype(np.uint8)
mtn_final = Image.fromarray(mtn_arr, mode='RGBA')
mtn_final = mtn_final.filter(ImageFilter.GaussianBlur(0.6))
mtn_final.save('assets/images/backgrounds/deep_background.png')
mtn_final.save('assets/images/backgrounds/night_deep_background.png')
print("Successfully generated scenic distant mountain & valley mist: deep_background.png")

# -------------------------------------------------------------------------
# 2. UPGRADED BAMBOO FOREST & ATMOSPHERE (mid_background.png)
# -------------------------------------------------------------------------
bam_w, bam_h = 720, 700
bam_img = Image.new('RGBA', (bam_w, bam_h), (0, 0, 0, 0))
b_draw = ImageDraw.Draw(bam_img)

# Deep bamboo layer (dark blue silhouettes)
for i in range(32):
    bx = (i * 23 + (i * 17) % 19) % bam_w
    bw = 5 + (i % 4)
    btop = 140 + (i * 29) % 120
    b_draw.rectangle([bx, btop, bx + bw, bam_h], fill=(14, 20, 32, 220))
    # Joints
    for jy in range(btop + 35, bam_h, 45):
        b_draw.line([bx - 1, jy, bx + bw + 1, jy], fill=(22, 32, 48, 240), width=2)
    # Leaves
    for ly in range(btop + 15, btop + 160, 40):
        b_draw.polygon([bx, ly, bx - 16, ly - 7, bx, ly - 12], fill=(16, 24, 38, 190))
        b_draw.polygon([bx + bw, ly, bx + bw + 18, ly - 5, bx + bw, ly - 10], fill=(16, 24, 38, 190))

# Closer bamboo layer (richer tone)
for i in range(18):
    bx = (i * 41 + 13) % bam_w
    bw = 7 + (i % 3)
    btop = 170 + (i * 37) % 100
    b_draw.rectangle([bx, btop, bx + bw, bam_h], fill=(10, 15, 26, 245))
    for jy in range(btop + 40, bam_h, 50):
        b_draw.line([bx - 2, jy, bx + bw + 2, jy], fill=(18, 26, 42, 255), width=3)
    for ly in range(btop + 20, btop + 180, 45):
        b_draw.polygon([bx, ly, bx - 22, ly - 9, bx, ly - 15], fill=(12, 18, 30, 220))
        b_draw.polygon([bx + bw, ly, bx + bw + 24, ly - 7, bx + bw, ly - 13], fill=(12, 18, 30, 220))

# Soft misty atmosphere across the bottom half
bam_arr = np.array(bam_img, dtype=float)
for y in range(480, bam_h):
    fade = max(0.0, 1.0 - (y - 480) / 200.0)
    bam_arr[y, :, 3] = bam_arr[y, :, 3] * fade

bam_arr = np.clip(bam_arr, 0, 255).astype(np.uint8)
bam_final = Image.fromarray(bam_arr, mode='RGBA')
bam_final.save('assets/images/backgrounds/mid_background.png')
bam_final.save('assets/images/backgrounds/night_mid_background.png')
print("Successfully generated lush bamboo forest & mist: mid_background.png")
