import os
from PIL import Image
import numpy as np

# Load backdrop (1376 x 768)
bg = Image.open('assets/autumn_maple/autumn_bg_clean_night.png').convert('RGBA')
w, h = bg.size
print(f'Backdrop size: {w}x{h}')

def extract_alpha(im, bg_color=(10, 20, 19), threshold=18, feather=15):
    rgba = im.convert('RGBA')
    arr = np.array(rgba, dtype=np.float32)
    dist = np.sqrt(np.sum((arr[:, :, :3] - bg_color)**2, axis=2))
    alpha = np.clip((dist - threshold) / feather, 0.0, 1.0)
    arr[:, :, 3] = alpha * 255.0
    res = Image.fromarray(arr.astype(np.uint8), mode='RGBA')
    bbox = res.getbbox()
    return res.crop(bbox) if bbox else res

# 1. Arched bridge
pack1 = Image.open('assets/autumn_maple/autumn_bridge_lanterns_pack1.png')
raw_bridge = pack1.crop((10, 18, 580, 215))
bridge_clean = extract_alpha(raw_bridge, bg_color=(10, 20, 19), threshold=16, feather=10)

# Scale bridge appropriately to span the river chasm
# Left bank top edge is around x=410, y=490; Right bank top edge is around x=1000, y=495
# River gap is from x=410 to x=1000 (about 590 px)
# Bridge width originally is 548px. Let's scale it to width ~ 600px
bridge_w = 600
bridge_h = int(bridge_clean.size[1] * (bridge_w / bridge_clean.size[0]))
bridge_scaled = bridge_clean.resize((bridge_w, bridge_h), Image.Resampling.LANCZOS)

# Position bridge across gap
bridge_x = 412
bridge_y = 350
bg.alpha_composite(bridge_scaled, (bridge_x, bridge_y))

# 2. Hanging Lanterns on bridge
raw_lantern = pack1.crop((495, 60, 580, 190))
lantern_clean = extract_alpha(raw_lantern, bg_color=(10, 20, 19), threshold=16, feather=10)
lantern_scaled = lantern_clean.resize((35, int(lantern_clean.size[1] * (35 / lantern_clean.size[0]))), Image.Resampling.LANCZOS)

# Place 3 lanterns along bridge arch
bg.alpha_composite(lantern_scaled, (bridge_x + 120, bridge_y + 110))
bg.alpha_composite(lantern_scaled, (bridge_x + 280, bridge_y + 70))
bg.alpha_composite(lantern_scaled, (bridge_x + 440, bridge_y + 110))

# 3. Kitsune Fox Statue on right stone terrace
pack_kitsune = Image.open('assets/autumn_maple/autumn_kitsune_statues_pack.png')
raw_fox = pack_kitsune.crop((25, 20, 190, 380))
fox_clean = extract_alpha(raw_fox, bg_color=(32, 35, 44), threshold=18, feather=12)
fox_scaled = fox_clean.resize((90, int(fox_clean.size[1] * (90 / fox_clean.size[0]))), Image.Resampling.LANCZOS)
# Place on right stone terrace (x ~ 1030, y ~ 370)
bg.alpha_composite(fox_scaled, (1040, 350))

# 4. Stone Toro Lantern on left bank
raw_toro = pack1.crop((465, 690, 560, 890))
toro_clean = extract_alpha(raw_toro, bg_color=(10, 20, 19), threshold=18, feather=10)
toro_scaled = toro_clean.resize((48, int(toro_clean.size[1] * (48 / toro_clean.size[0]))), Image.Resampling.LANCZOS)
bg.alpha_composite(toro_scaled, (360, 480))

# 5. Glowing Spirit Orbs
raw_orb = pack_kitsune.crop((785, 40, 860, 175))
orb_clean = extract_alpha(raw_orb, bg_color=(32, 35, 44), threshold=16, feather=8)
orb_scaled = orb_clean.resize((40, int(orb_clean.size[1] * (40 / orb_clean.size[0]))), Image.Resampling.LANCZOS)
bg.alpha_composite(orb_scaled, (690, 270))
bg.alpha_composite(orb_scaled, (850, 310))

# 6. Blue Chibi Ninja Player on bridge
if os.path.exists('assets/images/ninja_player_idle.png'):
    ninja = Image.open('assets/images/ninja_player_idle.png').convert('RGBA')
    ninja_scaled = ninja.resize((70, int(ninja.size[1] * (70 / ninja.size[0]))), Image.Resampling.LANCZOS)
    bg.alpha_composite(ninja_scaled, (bridge_x + 220, bridge_y + 40))

# Save composite
out_path = 'C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b/autumn_maple_composite_preview.png'
bg.save(out_path)
print(f'Saved composite to {out_path}')
