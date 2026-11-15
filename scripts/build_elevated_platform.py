import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 400, 70
im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)

# 1. Ornamental angled wooden cantilever braces at both ends
# Left bracket
draw.polygon([
    (24, 20),
    (24, 60),
    (38, 60),
    (54, 20)
], fill=(42, 24, 14, 255))
draw.polygon([
    (28, 24),
    (28, 56),
    (36, 56),
    (48, 24)
], fill=(62, 35, 20, 255))

# Right bracket
draw.polygon([
    (W - 24, 20),
    (W - 24, 60),
    (W - 38, 60),
    (W - 54, 20)
], fill=(42, 24, 14, 255))
draw.polygon([
    (W - 28, 24),
    (W - 28, 56),
    (W - 36, 56),
    (W - 48, 24)
], fill=(62, 35, 20, 255))

# Center support beam bracket
draw.polygon([
    (W // 2 - 16, 20),
    (W // 2 - 16, 52),
    (W // 2 + 16, 52),
    (W // 2 + 16, 20)
], fill=(42, 24, 14, 255))

# 2. Horizontal timber joist beam with Japanese lattice (y=16 to y=38)
draw.rectangle([10, 16, W - 10, 38], fill=(48, 28, 16, 255))
draw.line([(10, 17), (W - 10, 17)], fill=(82, 48, 28, 255), width=2)
draw.line([(10, 37), (W - 10, 37)], fill=(28, 16, 9, 255), width=2)

# Interlocking lattice insets
for lx in range(24, W - 30, 22):
    draw.rectangle([lx, 21, lx + 12, 32], fill=(30, 16, 10, 255))
    draw.rectangle([lx + 2, 23, lx + 10, 30], fill=(20, 10, 6, 255))

# 3. Top polished cedar plank deck (y=0 to y=18)
deck_arr = np.zeros((18, W, 4), dtype=np.uint8)
for x in range(W):
    grain = int(np.sin(x * 0.15) * 7 + np.cos(x * 0.5) * 5)
    is_seam = (x % 28 == 0) or (x % 28 == 1)
    
    for y in range(18):
        if is_seam:
            deck_arr[y, x] = [32, 18, 10, 255]
        else:
            if y < 3: # top golden highlight
                deck_arr[y, x] = [min(255, 205 + grain), min(255, 135 + grain), 72, 255]
            elif y < 12: # rich cedar
                deck_arr[y, x] = [min(255, 165 + grain), min(255, 98 + grain), 48, 255]
            else: # bottom bevel
                deck_arr[y, x] = [min(255, 115 + grain), min(255, 68 + grain), 32, 255]

deck_img = Image.fromarray(deck_arr, mode='RGBA')
im.paste(deck_img, (0, 0), deck_img)

im.save('assets/map/cutouts/boardwalk_elevated.png')
print("Successfully generated clean elevated platform: boardwalk_elevated.png (400x70)")
