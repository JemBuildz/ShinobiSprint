import os
import numpy as np
from PIL import Image

src_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stitch_character_assets/ShinobiSprint_Game_Characters_2048.png'
im = Image.open(src_path).convert('RGBA')

out_dir = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/sliced_foes'
os.makedirs(out_dir, exist_ok=True)

elements = [
    # A) Human Enemies
    ('ashigaru', [70, 230, 500, 495]),
    ('ronin', [275, 508, 465, 792]),
    ('archer', [240, 815, 515, 1075]),
    ('sumo', [260, 1105, 535, 1345]),
    
    # B) Yokai Beasts
    ('oni', [830, 230, 1090, 495]),
    ('tengu', [825, 512, 1145, 808]),
    ('tsuchigumo', [820, 835, 1150, 1065]),
    ('hitodama', [835, 1075, 1140, 1325]),
    
    # C) Cursed Props
    ('karakasa_obake', [1365, 230, 1655, 495]),
    ('ancestral_katana', [1325, 590, 1690, 755]),
    ('cursed_well', [1355, 825, 1650, 1030]),
    ('broken_stone_lantern', [1375, 1080, 1600, 1325]),
    
    # Ninjas
    ('ninja_blue_standing', [1750, 200, 1930, 445]),
    ('ninja_brown_prayer', [1755, 460, 1935, 705]),
    ('ninja_cyan_crouch', [1755, 715, 1935, 905]),
    ('ninja_purple_kunoichi', [1735, 915, 1955, 1135]),
    ('ninja_dark_infiltrator', [1750, 1145, 1945, 1365]),
    
    # D) Mystical Foes
    ('ninja_blue_alt', [105, 1455, 295, 1715]),
    ('ninja_ghostly', [335, 1455, 525, 1715]),
    ('ninja_purple_alt', [105, 1735, 275, 1975]),
    ('kitsune_trio', [325, 1735, 595, 1975]),
    
    # E) Effects
    ('shadow_portal', [950, 1445, 1215, 1650]),
    ('oni_rage_ofuda', [745, 1720, 985, 1880]),
    ('tengu_gust', [985, 1685, 1205, 1840]),
    ('smoke_cloud', [1215, 1705, 1410, 1860]),
    ('cursed_arrow', [975, 1880, 1230, 1975]),
    
    # F) Mystical Items
    ('magatama_cluster', [1645, 1465, 1895, 1655]),
    ('caltrops_cluster', [1660, 1795, 1895, 1935])
]

# Flood-fill or alpha threshold extraction
# The background is solid pure white RGB=(255, 255, 255).
for name, box in elements:
    cropped = im.crop(box)
    arr = np.array(cropped)
    
    # White background removal: pixels near pure white (> 248 on R,G,B) get alpha 0
    # Soft alpha feathering between 235 and 252
    r = arr[:, :, 0].astype(float)
    g = arr[:, :, 1].astype(float)
    b = arr[:, :, 2].astype(float)
    
    # Distance from white
    dist = np.maximum(255 - r, np.maximum(255 - g, 255 - b))
    
    # If dist > 20, completely opaque (255)
    # If dist < 4, completely transparent (0)
    # in between: smooth ramp
    alpha = np.clip((dist - 4) / 16.0 * 255.0, 0, 255).astype(np.uint8)
    
    # Keep original alpha if it had transparency
    arr[:, :, 3] = np.minimum(arr[:, :, 3], alpha)
    
    # Find true bounding box of non-transparent content
    non_empty = np.where(arr[:, :, 3] > 10)
    if len(non_empty[0]) > 0:
        ymin, ymax = non_empty[0].min(), non_empty[0].max() + 1
        xmin, xmax = non_empty[1].min(), non_empty[1].max() + 1
        trimmed_arr = arr[ymin:ymax, xmin:xmax]
    else:
        trimmed_arr = arr
        
    out_im = Image.fromarray(trimmed_arr, 'RGBA')
    out_path = os.path.join(out_dir, f'{name}.png')
    out_im.save(out_path)
    print(f'Sliced {name}: {out_im.size}')

print(f'All {len(elements)} assets sliced to {out_dir}!')
