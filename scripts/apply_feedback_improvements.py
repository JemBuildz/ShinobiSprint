import os
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

artifact_dir = r"C:\Users\User\.gemini\antigravity\brain\8d1fe0d7-a367-49a2-ba0b-1e27387c2271"

# -------------------------------------------------------------------------
# 1. CREATE DEDICATED MID-AIR SUSPENSION PLATFORM (BRACKETS / HANGING BEAMS)
# -------------------------------------------------------------------------
# Load original boardwalk cutout
boardwalk_orig = Image.open('assets/map/cutouts/wooden_boardwalk_platform.png').convert('RGBA')

# Crop just the top wood planks and horizontal truss beam (without bottom stone feet)
# boardwalk_clean size: (1254, 414). Stone feet are in the bottom ~120px.
# We crop the top plank deck and upper timber frame: (0, 0, 1254, 270)
deck = boardwalk_orig.crop((0, 0, 1254, 270))

# Create a clean mid-air platform with wooden angle brackets under the corners
mid_air_platform = Image.new('RGBA', (1254, 300), (0, 0, 0, 0))
mid_air_platform.paste(deck, (0, 0), deck)
draw_p = ImageDraw.Draw(mid_air_platform)

# Add heavy wooden support brackets angled back into wall/air underneath
# Left bracket
draw_p.polygon([(80, 240), (120, 240), (170, 290), (140, 290)], fill=(38, 20, 11, 255))
# Right bracket
draw_p.polygon([(1174, 240), (1134, 240), (1084, 290), (1114, 290)], fill=(38, 20, 11, 255))
# Center bracket
draw_p.polygon([(610, 240), (644, 240), (664, 290), (630, 290)], fill=(38, 20, 11, 255))

mid_air_platform.save('assets/map/cutouts/wooden_midair_platform.png')
print("Saved assets/map/cutouts/wooden_midair_platform.png (no floating stilt feet)")

# -------------------------------------------------------------------------
# 2. CREATE LAYER 2 (MID): DISTANT MOUNTAINS + MASSIVE DISTANT PAGODA (40% OPACITY + FOG)
# -------------------------------------------------------------------------
# Canvas: 720 x 800
W, H = 720, 800
layer2 = Image.new('RGBA', (W, H), (0, 0, 0, 0))

# Distant mountain ridge (dark misty indigo, 40% effective opacity: alpha ~100)
mtn_arr = np.zeros((H, W, 4), dtype=np.uint8)
x_vals = np.linspace(0, 4 * np.pi, W)
h_back = 240 + 75 * np.sin(x_vals * 0.9) + 35 * np.sin(x_vals * 2.3)

for x in range(W):
    top_y = int(h_back[x])
    for y in range(top_y, H):
        fade = 1.0
        if y > 520:
            fade = max(0.0, 1.0 - (y - 520) / 240.0)
        mtn_arr[y, x, 0] = 30
        mtn_arr[y, x, 1] = 42
        mtn_arr[y, x, 2] = 68
        # User requirement: Lower opacity to 40% (alpha ~ 102)
        mtn_arr[y, x, 3] = int(102 * fade)

layer2_mtn = Image.fromarray(mtn_arr, mode='RGBA').filter(ImageFilter.GaussianBlur(1.0))
layer2 = Image.alpha_composite(layer2, layer2_mtn)

# Now add a massive distant pagoda silhouette in Layer 2 (scaled down for proper perspective distance)
pagoda_orig = Image.open('assets/map/cutouts/pagoda_shrine.png').convert('RGBA')
# Scale pagoda to distant perspective size: ~180px tall
pagoda_aspect = pagoda_orig.width / pagoda_orig.height
p_dist_h = 240
p_dist_w = int(p_dist_h * pagoda_aspect)
pagoda_dist = pagoda_orig.resize((p_dist_w, p_dist_h), Image.Resampling.LANCZOS)

# Adjust pagoda to 40% opacity with atmospheric bluish night haze
p_arr = np.array(pagoda_dist, dtype=float)
# Blend pagoda color towards sky fog (#1E293B)
p_arr[:, :, 0] = p_arr[:, :, 0] * 0.4 + 30 * 0.6
p_arr[:, :, 1] = p_arr[:, :, 1] * 0.4 + 45 * 0.6
p_arr[:, :, 2] = p_arr[:, :, 2] * 0.4 + 75 * 0.6
p_arr[:, :, 3] = p_arr[:, :, 3] * 0.40 # 40% opacity

pagoda_hazed = Image.fromarray(p_arr.astype(np.uint8), mode='RGBA')
# Paste onto mountain ridge in Layer 2
layer2.paste(pagoda_hazed, (160, 220), pagoda_hazed)
layer2.save('assets/images/backgrounds/deep_background.png')
print("Saved Layer 2 (40% opacity distant mountains + massive distant pagoda)")

# -------------------------------------------------------------------------
# 3. CREATE LAYER 1 (NEAR): BAMBOO TREES AT 70% OPACITY (BEHIND PLATFORMS)
# -------------------------------------------------------------------------
bamboo_orig = Image.open('assets/map/cutouts/bamboo_cluster.png').convert('RGBA')
b_w, b_h = 720, 600
layer1 = Image.new('RGBA', (b_w, b_h), (0, 0, 0, 0))

# Paste repeating bamboo silhouettes at 70% opacity
# Resize bamboo clusters
b_aspect = bamboo_orig.width / bamboo_orig.height
b_scaled_h = 280
b_scaled_w = int(b_scaled_h * b_aspect)
b_scaled = bamboo_orig.resize((b_scaled_w, b_scaled_h), Image.Resampling.LANCZOS)

b_arr = np.array(b_scaled, dtype=float)
# Dark nocturnal green-blue hue
b_arr[:, :, 0] = b_arr[:, :, 0] * 0.5 + 15 * 0.5
b_arr[:, :, 1] = b_arr[:, :, 1] * 0.6 + 35 * 0.4
b_arr[:, :, 2] = b_arr[:, :, 2] * 0.6 + 50 * 0.4
# User requirement: 70% opacity
b_arr[:, :, 3] = b_arr[:, :, 3] * 0.70

b_hazed = Image.fromarray(b_arr.astype(np.uint8), mode='RGBA')

# Tile across Layer 1
for x_off in [10, 180, 360, 530]:
    layer1.paste(b_hazed, (x_off, 220), b_hazed)

# Also paste the red Torii gate in Layer 1 (BEHIND platforms, 75% opacity, landmark in midground)
torii_orig = Image.open('assets/map/cutouts/torii_gate.png').convert('RGBA')
t_h = 170
t_w = int(t_h * (torii_orig.width / torii_orig.height))
torii_bg = torii_orig.resize((t_w, t_h), Image.Resampling.LANCZOS)
t_arr = np.array(torii_bg, dtype=float)
t_arr[:, :, 3] = t_arr[:, :, 3] * 0.75 # Soft atmospheric depth
torii_hazed = Image.fromarray(t_arr.astype(np.uint8), mode='RGBA')
layer1.paste(torii_hazed, (330, 240), torii_hazed)

layer1.save('assets/images/backgrounds/mid_background.png')
print("Saved Layer 1 (70% opacity bamboo + background Torii landmark)")

print("Background layers separated and calibrated.")
