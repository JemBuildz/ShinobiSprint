import os
from PIL import Image, ImageFilter
import numpy as np

os.makedirs('assets/images', exist_ok=True)

def clean_cutout(crop_im, bg_color, dist_thresh=20, feather=12):
    """Accurately keys out background with alpha feathering and despill."""
    rgba = crop_im.convert('RGBA')
    arr = np.array(rgba, dtype=np.float32)
    
    # Euclidean color distance
    diff = np.sqrt(np.sum((arr[:, :, :3] - bg_color)**2, axis=2))
    
    alpha = np.clip((diff - dist_thresh) / feather, 0.0, 1.0)
    
    # Despill: prevent dark background color bleeding into semi-transparent edge pixels
    for c in range(3):
        # Unblend against background
        arr[:, :, c] = np.clip((arr[:, :, c] - (1.0 - alpha) * bg_color[c]) / np.maximum(alpha, 0.05), 0.0, 255.0)
        
    arr[:, :, 3] = alpha * 255.0
    res = Image.fromarray(arr.astype(np.uint8), mode='RGBA')
    bbox = res.getbbox()
    return res.crop(bbox) if bbox else res

# 1. Background Backdrop: Level 3 Autumn Maple Forest
bg_img = Image.open('assets/autumn_maple/autumn_bg_clean_night.png')
# Standardize to 1024x576 for consistent Flame game resolution & parallax matching Level 1 & 2
bg_1024 = bg_img.resize((1024, 576), Image.Resampling.LANCZOS)
bg_1024.save('assets/images/level3_layer1_autumn_sky.png')
print('Saved level3_layer1_autumn_sky.png (1024x576)')

# 2. Arched Bridge
pack1 = Image.open('assets/autumn_maple/autumn_bridge_lanterns_pack1.png')
# Bridge 1 (arched bridge with top rail & deck planks)
raw_bridge = pack1.crop((10, 18, 580, 215))
bridge = clean_cutout(raw_bridge, bg_color=(10, 20, 19), dist_thresh=18, feather=10)
bridge.save('assets/images/level3_prop_bridge_arched.png')
print('Saved level3_prop_bridge_arched.png:', bridge.size)

# 3. Stone Pier Foundation
raw_pier = pack1.crop((595, 460, 800, 680))
pier = clean_cutout(raw_pier, bg_color=(10, 20, 19), dist_thresh=20, feather=10)
pier.save('assets/images/level3_prop_stone_pier.png')
print('Saved level3_prop_stone_pier.png:', pier.size)

# 4. Stone Toro Lantern
raw_toro = pack1.crop((465, 690, 560, 890))
toro = clean_cutout(raw_toro, bg_color=(10, 20, 19), dist_thresh=18, feather=10)
toro.save('assets/images/level3_prop_stone_toro.png')
print('Saved level3_prop_stone_toro.png:', toro.size)

# 5. Hanging Chochin Amber Lantern
raw_lantern = pack1.crop((495, 60, 580, 190))
lantern = clean_cutout(raw_lantern, bg_color=(10, 20, 19), dist_thresh=16, feather=10)
lantern.save('assets/images/level3_prop_lantern_chochin.png')
print('Saved level3_prop_lantern_chochin.png:', lantern.size)

# 6. Kitsune Fox Statue
pack_fox = Image.open('assets/autumn_maple/autumn_kitsune_statues_pack.png')
raw_fox = pack_fox.crop((25, 20, 190, 380))
fox = clean_cutout(raw_fox, bg_color=(32, 35, 44), dist_thresh=20, feather=12)
fox.save('assets/images/level3_prop_kitsune_statue.png')
print('Saved level3_prop_kitsune_statue.png:', fox.size)

# 7. Glowing Spirit Orb
raw_orb = pack_fox.crop((785, 40, 860, 175))
orb = clean_cutout(raw_orb, bg_color=(32, 35, 44), dist_thresh=16, feather=8)
orb.save('assets/images/level3_prop_spirit_orb.png')
print('Saved level3_prop_spirit_orb.png:', orb.size)

# 8. Single Falling Maple Leaf (for particle effects)
pack_flora = Image.open('assets/autumn_maple/autumn_flora_maple_trees_pack1.png')
raw_leaf = pack_flora.crop((910, 640, 975, 715))
leaf = clean_cutout(raw_leaf, bg_color=(14, 24, 26), dist_thresh=18, feather=8)
leaf.save('assets/images/level3_prop_maple_leaf.png')
print('Saved level3_prop_maple_leaf.png:', leaf.size)

# Copy all to brain artifact directory for inspection
art_dir = r'C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b'
import shutil
for f in [
    'level3_layer1_autumn_sky.png',
    'level3_prop_bridge_arched.png',
    'level3_prop_stone_pier.png',
    'level3_prop_stone_toro.png',
    'level3_prop_lantern_chochin.png',
    'level3_prop_kitsune_statue.png',
    'level3_prop_spirit_orb.png',
    'level3_prop_maple_leaf.png'
]:
    shutil.copy2(os.path.join('assets/images', f), os.path.join(art_dir, f))
    print(f'Copied {f} to artifacts')
