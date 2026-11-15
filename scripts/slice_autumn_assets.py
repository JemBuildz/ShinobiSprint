import os
from PIL import Image, ImageFilter
import numpy as np

os.makedirs('assets/images', exist_ok=True)

def remove_dark_bg(im_crop, bg_color=(10, 20, 19), threshold=22):
    """Cleanly converts dark slate background to transparent PNG with smooth edge antialiasing."""
    rgba = im_crop.convert('RGBA')
    data = np.array(rgba, dtype=np.float32)
    
    # Distance from bg_color
    diff = np.sqrt(
        (data[:, :, 0] - bg_color[0])**2 +
        (data[:, :, 1] - bg_color[1])**2 +
        (data[:, :, 2] - bg_color[2])**2
    )
    
    # Alpha mask: fully transparent if close to bg, fully opaque if far
    low = threshold
    high = threshold + 25
    alpha = np.clip((diff - low) / (high - low), 0.0, 1.0) * 255.0
    data[:, :, 3] = alpha
    
    res = Image.fromarray(data.astype(np.uint8), mode='RGBA')
    # Crop to non-transparent bounding box
    bbox = res.getbbox()
    if bbox:
        res = res.crop(bbox)
    return res

def remove_near_black(im_crop, threshold=20):
    rgba = im_crop.convert('RGBA')
    data = np.array(rgba, dtype=np.float32)
    luminance = np.max(data[:, :, :3], axis=2)
    low = threshold
    high = threshold + 20
    alpha = np.clip((luminance - low) / (high - low), 0.0, 1.0) * 255.0
    data[:, :, 3] = alpha
    res = Image.fromarray(data.astype(np.uint8), mode='RGBA')
    bbox = res.getbbox()
    if bbox:
        res = res.crop(bbox)
    return res

# 1. Bridge pack extraction (assets/autumn_maple/autumn_bridge_lanterns_pack1.png)
im_bridge = Image.open('assets/autumn_maple/autumn_bridge_lanterns_pack1.png')

# Arched Bridge (middle horizontal bridge with planks & railing)
crop_bridge = im_bridge.crop((20, 240, 640, 480))
bridge_clean = remove_dark_bg(crop_bridge, bg_color=(10, 20, 19), threshold=20)
bridge_clean.save('assets/images/autumn_bridge_arched.png')
print('Saved autumn_bridge_arched.png:', bridge_clean.size)

# Hanging Paper Lantern Chochin (single glowing lantern)
crop_lantern = im_bridge.crop((495, 60, 580, 190))
lantern_clean = remove_dark_bg(crop_lantern, bg_color=(10, 20, 19), threshold=18)
lantern_clean.save('assets/images/autumn_lantern_chochin.png')
print('Saved autumn_lantern_chochin.png:', lantern_clean.size)

# Stone Pier / Foundation (mossy stone wall block)
crop_pier = im_bridge.crop((595, 460, 800, 680))
pier_clean = remove_dark_bg(crop_pier, bg_color=(10, 20, 19), threshold=22)
pier_clean.save('assets/images/autumn_stone_pier.png')
print('Saved autumn_stone_pier.png:', pier_clean.size)

# Stone Toro Lantern on Pedestal
crop_toro = im_bridge.crop((465, 690, 560, 890))
toro_clean = remove_dark_bg(crop_toro, bg_color=(10, 20, 19), threshold=20)
toro_clean.save('assets/images/autumn_stone_toro.png')
print('Saved autumn_stone_toro.png:', toro_clean.size)

# 2. Kitsune Statues & Spirit Orbs (assets/autumn_maple/autumn_kitsune_statues_pack.png)
im_kitsune = Image.open('assets/autumn_maple/autumn_kitsune_statues_pack.png')

# Kitsune Fox Statue (left-facing on pedestal)
crop_fox = im_kitsune.crop((25, 20, 190, 380))
fox_clean = remove_dark_bg(crop_fox, bg_color=(32, 35, 44), threshold=22)
fox_clean.save('assets/images/autumn_kitsune_statue.png')
print('Saved autumn_kitsune_statue.png:', fox_clean.size)

# Cyan/Blue Spirit Flame Orb
crop_orb = im_kitsune.crop((785, 40, 860, 175))
orb_clean = remove_dark_bg(crop_orb, bg_color=(32, 35, 44), threshold=18)
orb_clean.save('assets/images/autumn_spirit_orb.png')
print('Saved autumn_spirit_orb.png:', orb_clean.size)

# Teal Spirit Lantern
crop_spirit_lantern = im_kitsune.crop((510, 35, 635, 380))
spirit_lantern_clean = remove_dark_bg(crop_spirit_lantern, bg_color=(32, 35, 44), threshold=20)
spirit_lantern_clean.save('assets/images/autumn_spirit_lantern.png')
print('Saved autumn_spirit_lantern.png:', spirit_lantern_clean.size)

# Stone Steps Platform
crop_steps = im_kitsune.crop((490, 595, 735, 795))
steps_clean = remove_dark_bg(crop_steps, bg_color=(32, 35, 44), threshold=22)
steps_clean.save('assets/images/autumn_stone_steps.png')
print('Saved autumn_stone_steps.png:', steps_clean.size)

# 3. Autumn Flora Pack (assets/autumn_maple/autumn_flora_maple_trees_pack1.png)
im_flora = Image.open('assets/autumn_maple/autumn_flora_maple_trees_pack1.png')

# Hanging Maple Branch with Red Leaves
crop_branch = im_flora.crop((695, 30, 840, 325))
branch_clean = remove_dark_bg(crop_branch, bg_color=(14, 24, 26), threshold=20)
branch_clean.save('assets/images/autumn_maple_branch.png')
print('Saved autumn_maple_branch.png:', branch_clean.size)

# Mossy River Boulder with fallen leaves
crop_rock = im_flora.crop((575, 830, 745, 975)) if im_flora.size[1] > 900 else im_flora.crop((575, 750, 745, 890))
rock_clean = remove_dark_bg(crop_rock, bg_color=(14, 24, 26), threshold=20)
rock_clean.save('assets/images/autumn_mossy_rock.png')
print('Saved autumn_mossy_rock.png:', rock_clean.size)

# Also save high-res backdrop
bg_pure = Image.open('assets/autumn_maple/autumn_parallax_bg_pure.png')
bg_pure.save('assets/images/autumn_backdrop_night.png')
print('Saved autumn_backdrop_night.png:', bg_pure.size)

# Copy extracted sprites to artifact dir for preview
art_dir = r'C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b'
import shutil
for f in ['autumn_bridge_arched.png', 'autumn_lantern_chochin.png', 'autumn_stone_pier.png', 'autumn_stone_toro.png', 'autumn_kitsune_statue.png', 'autumn_spirit_orb.png', 'autumn_spirit_lantern.png', 'autumn_stone_steps.png', 'autumn_maple_branch.png', 'autumn_mossy_rock.png', 'autumn_backdrop_night.png']:
    s = os.path.join('assets/images', f)
    d = os.path.join(art_dir, f)
    shutil.copy2(s, d)
    print(f'Copied {f} to artifacts')
