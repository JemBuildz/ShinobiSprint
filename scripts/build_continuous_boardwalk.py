import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 512, 120
im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)

# 1. Timber pilings / posts every 128px
for px in range(0, W, 128):
    # Wooden vertical post (width 22px, from y=24 down to y=105)
    post_x = px + 16
    draw.rectangle([post_x, 24, post_x + 22, 105], fill=(42, 24, 14, 255))
    draw.rectangle([post_x + 2, 26, post_x + 6, 103], fill=(68, 38, 22, 255)) # highlight
    draw.rectangle([post_x + 16, 26, post_x + 20, 103], fill=(26, 14, 8, 255)) # shadow
    
    # Ornamental angled brace
    draw.polygon([
        (post_x - 14, 30),
        (post_x + 2, 48),
        (post_x + 2, 58),
        (post_x - 14, 40)
    ], fill=(36, 20, 12, 255))
    draw.polygon([
        (post_x + 36, 30),
        (post_x + 20, 48),
        (post_x + 20, 58),
        (post_x + 36, 40)
    ], fill=(36, 20, 12, 255))
    
    # Carved granite stone pedestal at post foot (y=98 to 118)
    draw.rectangle([post_x - 6, 98, post_x + 28, 118], fill=(55, 62, 72, 255))
    draw.rectangle([post_x - 4, 100, post_x + 26, 104], fill=(85, 95, 110, 255)) # stone rim highlight
    draw.rectangle([post_x - 6, 114, post_x + 28, 118], fill=(35, 40, 48, 255)) # stone shadow

# 2. Horizontal timber joist beam (y=20 to y=42)
draw.rectangle([0, 20, W, 42], fill=(48, 28, 16, 255))
draw.line([(0, 21), (W, 21)], fill=(78, 46, 26, 255), width=2)
draw.line([(0, 41), (W, 41)], fill=(28, 16, 9, 255), width=2)

# Ornamental lattice under-beam details
for lx in range(0, W, 16):
    draw.rectangle([lx + 6, 26, lx + 10, 36], fill=(32, 18, 10, 255))

# 3. Top walking deck planks (y=0 to y=22)
# Warm cedar tones: #D98236, #A6561F, #73340D
deck_arr = np.zeros((22, W, 4), dtype=np.uint8)
for x in range(W):
    # Wood grain variation
    grain = int(np.sin(x * 0.12) * 8 + np.cos(x * 0.45) * 6)
    
    # Plank seams every 32px
    is_seam = (x % 32 == 0) or (x % 32 == 1)
    
    for y in range(22):
        if is_seam:
            deck_arr[y, x] = [30, 16, 9, 255]
        else:
            if y < 4: # top bevel highlight
                deck_arr[y, x] = [min(255, 195 + grain), min(255, 125 + grain), 65, 255]
            elif y < 14: # mid cedar plank
                deck_arr[y, x] = [min(255, 155 + grain), min(255, 92 + grain), 45, 255]
            else: # bottom shadow
                deck_arr[y, x] = [min(255, 105 + grain), min(255, 62 + grain), 30, 255]

deck_img = Image.fromarray(deck_arr, mode='RGBA')
im.paste(deck_img, (0, 0), deck_img)

# Save continuous boardwalk platform asset
im.save('assets/map/cutouts/boardwalk_continuous.png')
print("Successfully generated continuous boardwalk deck: boardwalk_continuous.png (512x120)")
