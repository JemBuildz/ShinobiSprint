import os
import numpy as np
from PIL import Image

src_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stitch_character_assets/ShinobiSprint_Game_Characters_2048.png'
im = Image.open(src_path).convert('RGBA')
out_dir = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/sliced_foes'

# Fine-tuned to cut strictly below letterforms
precision_boxes = [
    # Y-min lowered enough to completely miss letters
    ('oni', [830, 246, 1090, 495]),
    ('tengu', [825, 542, 1145, 808]),
    ('tsuchigumo', [820, 868, 1150, 1065]),
    ('archer', [240, 865, 515, 1075]),
    ('sumo', [260, 1140, 535, 1345]),
    ('broken_stone_lantern', [1375, 1125, 1600, 1325]),
    ('ninja_ghostly', [335, 1455, 525, 1680]),
]

for name, box in precision_boxes:
    cropped = im.crop(box)
    arr = np.array(cropped)
    
    r = arr[:, :, 0].astype(float)
    g = arr[:, :, 1].astype(float)
    b = arr[:, :, 2].astype(float)
    
    dist = np.maximum(255 - r, np.maximum(255 - g, 255 - b))
    alpha = np.clip((dist - 4) / 16.0 * 255.0, 0, 255).astype(np.uint8)
    arr[:, :, 3] = np.minimum(arr[:, :, 3], alpha)
    
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
    print(f'Precision slice {name}: {out_im.size}')
