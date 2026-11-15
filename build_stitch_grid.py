from PIL import Image, ImageDraw
import os
import json

manifest_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stitch_scenes/manifest.json'
with open(manifest_path, 'r', encoding='utf-8') as f:
    scenes = json.load(f)

cols = 2
rows = 5
thumb_w = 640
thumb_h = 360
margin = 20
header_h = 90

total_w = cols * thumb_w + (cols + 1) * margin
total_h = header_h + rows * thumb_h + (rows + 1) * margin

canvas = Image.new('RGB', (total_w, total_h), (10, 14, 23))
draw = ImageDraw.Draw(canvas)

# Header
draw.rectangle([(0, 0), (total_w, header_h)], fill=(16, 22, 36))
draw.text((margin, 20), 'STITCH 2D GAME SCENE CATALOG (PROJECT: SHINOBI SPRINT)', fill=(255, 215, 0))
draw.text((margin, 52), '10 Environmental Panoramic Stage Plates & Biomes in Stitch Library', fill=(160, 185, 215))

for i, s in enumerate(scenes[:10]):
    c = i % cols
    r = i // cols
    x = margin + c * (thumb_w + margin)
    y = header_h + margin + r * (thumb_h + margin)
    
    img_path = s.get('local_file', '')
    if os.path.exists(img_path):
        try:
            im = Image.open(img_path).convert('RGB')
            im = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            canvas.paste(im, (x, y))
        except Exception as e:
            print(f'Error pasting {img_path}: {e}')
    
    # Border
    draw.rectangle([(x, y), (x + thumb_w, y + thumb_h)], outline=(50, 70, 95), width=2)
    
    # Tag banner
    banner_h = 36
    draw.rectangle([(x, y), (x + thumb_w, y + banner_h)], fill=(10, 14, 22))
    label = f"{i+1}. {s['category'].upper()}"
    draw.text((x + 12, y + 10), label, fill=(255, 255, 255))

out_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stitch_scenes_catalog_grid.png'
canvas.save(out_path)
print('Grid saved to:', out_path)
