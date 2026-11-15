from PIL import Image, ImageDraw

base_dir = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stitch_character_assets'
files = [
    ('860dfea0.png', 'Stitch Asset 860dfea0', 'Armored Samurai Guards & Fortress Props'),
    ('09faf2b0.png', 'Stitch Asset 09faf2b0', 'Hitodama Ghost Wisps & Stone Kitsune Fox Statues'),
    ('2fc1f449.png', 'Stitch Asset 2fc1f449', 'Chibi Ninja Action Sprite Sheet (Run, Slash, Jump)'),
    ('ef032700.png', 'Stitch Asset ef032700', 'Isolated Chibi Shinobi Master Sprite')
]

w, h = 1200, 1000
out = Image.new('RGBA', (w, h), (20, 26, 40, 255))
draw = ImageDraw.Draw(out)

# Title
draw.rectangle([0, 0, w, 70], fill=(30, 42, 65, 255))
draw.text((25, 15), "STITCH PROJECT: CHARACTER & ENEMY SPRITE SHEETS", fill=(255, 215, 0, 255))
draw.text((25, 42), "Extracted from Stitch Project 'Shinobi Sprint' (projects/12274354107792210135)", fill=(180, 205, 240, 255))

# 2x2 grid
cell_w = 580
cell_h = 440

for idx, (fname, title, desc) in enumerate(files):
    r = idx // 2
    c = idx % 2
    x0 = 15 + c * (cell_w + 10)
    y0 = 85 + r * (cell_h + 10)
    
    draw.rectangle([x0, y0, x0 + cell_w, y0 + cell_h], fill=(28, 36, 54, 255), outline=(50, 70, 100, 255), width=2)
    
    im_path = f'{base_dir}/{fname}'
    im = Image.open(im_path).convert('RGBA')
    # Fit inside 550 x 340
    scale = min(540 / im.width, 340 / im.height)
    nw = int(im.width * scale)
    nh = int(im.height * scale)
    im_scaled = im.resize((nw, nh), Image.Resampling.LANCZOS)
    
    im_x = x0 + (cell_w - nw) // 2
    im_y = y0 + 10 + (340 - nh) // 2
    out.paste(im_scaled, (im_x, im_y), im_scaled)
    
    draw.text((x0 + 15, y0 + 365), title, fill=(255, 255, 255, 255))
    draw.text((x0 + 15, y0 + 395), desc, fill=(140, 185, 245, 255))

out_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stitch_character_spritesheets_overview.png'
out.save(out_path)
print(f'Stitch sheets overview saved to {out_path} ({out.size})')
