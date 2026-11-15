from PIL import Image, ImageDraw
import os

src_path = 'C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b/984c1def32624df0aee5933a82faac83.png'
im = Image.open(src_path)

# Resize to standard game 1024x576
im_1024 = im.resize((1024, 576), Image.Resampling.LANCZOS)
out_path = 'assets/images/level1_cinematic_stage_1024.png'
im_1024.save(out_path)
print(f"Saved {out_path} (1024x576)")

# Draw candidate surfaces on test image
test_im = im_1024.copy()
draw = ImageDraw.Draw(test_im)

# 1. Left Ground
# x: 0..425, y: 490
draw.line([(0, 490), (425, 490)], fill=(0, 255, 0, 255), width=3)

# 2. Right Ground
# x: 575..1024, y: 490
draw.line([(575, 490), (1024, 490)], fill=(0, 255, 0, 255), width=3)

# 3. Right Raised Cliff
# x: 870..1024, y: 330
draw.line([(870, 330), (1024, 330)], fill=(0, 255, 255, 255), width=3)

# 4. Central Wooden Bridge Platform spanning chasm (y: 420, x: 395..605)
draw.line([(395, 420), (605, 420)], fill=(255, 128, 0, 255), width=3)

# 5. Stepping Stone Pillar
# x: 290..350, y: 420
draw.line([(290, 420), (350, 420)], fill=(255, 255, 0, 255), width=3)

# 6. Left Hut Rooftop Ledge
# x: 45..280, y: 220
draw.line([(45, 220), (280, 220)], fill=(255, 0, 255, 255), width=3)

# 7. Right Dojo Rooftop Ledge
# x: 770..980, y: 220
draw.line([(770, 220), (980, 220)], fill=(255, 0, 255, 255), width=3)

art_path = r'C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b/bamboo_mapped_surfaces.png'
test_im.save(art_path)
print(f"Saved mapped surface visualization to {art_path}")
