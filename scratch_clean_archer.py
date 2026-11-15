import os
import numpy as np
from PIL import Image

src_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stitch_character_assets/ShinobiSprint_Game_Characters_2048.png'
im = Image.open(src_path).convert('RGBA')
out_dir = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/sliced_foes'

# Archer: cut x-min=262, y-min=910 (removes the 'R' at top-left completely while keeping the quiver and bow)
cropped = im.crop([262, 910, 515, 1075])
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
out_path = os.path.join(out_dir, 'archer.png')
out_im.save(out_path)
print(f'Clean archer slice: {out_im.size}')
