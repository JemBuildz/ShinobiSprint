from PIL import Image, ImageDraw

hero_path = 'assets/images/character_ninja.png'
foes_dir = 'assets/images/foes'

hero = Image.open(hero_path).convert('RGBA')
ninja_h = 52 # Baseline player height
hero_w = int(hero.width * (ninja_h / hero.height))
hero_scaled = hero.resize((hero_w, ninja_h), Image.Resampling.LANCZOS)

# Targets calibrated so human heads & bodies match the ninja:
# Ashigaru: reduced from 65px to 48px total height
# Yumi-Ashi Archer: reduced from 63px to 46px total height
# Blue Horned Oni: reduced from 68px to 54px total height
# Ronin, Sumo, Tengu, Karakasa, Kitsune left at user-approved sizes
foes = [
    ('hero', hero_scaled, 'Player (Hero)', 'Height: 52px (Baseline)'),
    ('ashigaru.png', 48, 'Ashigaru Spearman', 'Adjusted (H: 48px)'),
    ('ronin.png', 54, 'Masterless Ronin', 'Approved (H: 54px)'),
    ('archer.png', 46, 'Yumi-Ashi Archer', 'Adjusted (H: 46px)'),
    ('sumo.png', 52, 'Sumo Rikishi', 'Approved (H: 52px)'),
    ('oni.png', 54, 'Blue Horned Oni', 'Adjusted (H: 54px)'),
    ('tengu.png', 54, 'Crow Tengu', 'Approved (H: 54px)'),
    ('karakasa.png', 50, 'Karakasa-Obake', 'Approved (H: 50px)'),
    ('kitsune.png', 44, 'Kitsune Trio', 'Approved (H: 44px)')
]

cell_w = 120
cell_h = 160
total_w = len(foes) * cell_w
total_h = cell_h + 80

out = Image.new('RGBA', (total_w, total_h), (20, 26, 40, 255))
draw = ImageDraw.Draw(out)

# Header
draw.rectangle([0, 0, total_w, 60], fill=(28, 38, 60, 255))
draw.text((20, 12), "UPDATED SCALE CALIBRATION GUIDE (ADJUSTED ASHIGARU, ARCHER & ONI)", fill=(255, 215, 0, 255))
draw.text((20, 36), "Red line: 52px Player head line. Green line: Cobblestone walking ground (Y = 175).", fill=(170, 200, 240, 255))

ground_y = 175
head_y = ground_y - 52

# Guide lines
draw.line([0, ground_y, total_w, ground_y], fill=(80, 200, 80, 255), width=2)
draw.line([0, head_y, total_w, head_y], fill=(255, 70, 70, 255), width=1)

for idx, item in enumerate(foes):
    fname = item[0]
    target_val = item[1]
    name = item[2]
    spec = item[3]
    
    if fname == 'hero':
        img = target_val
    else:
        p = f'{foes_dir}/{fname}'
        raw = Image.open(p).convert('RGBA')
        th = target_val
        scale = th / raw.height
        w = int(raw.width * scale)
        h = int(raw.height * scale)
        img = raw.resize((w, h), Image.Resampling.LANCZOS)
        
    w, h = img.size
    cx = idx * cell_w + cell_w // 2
    px = cx - w // 2
    py = ground_y - h
    
    out.paste(img, (px, py), img)
    
    # Text labels
    color = (255, 220, 100, 255) if 'Adjusted' in spec else (240, 245, 255, 255)
    draw.text((idx * cell_w + 5, ground_y + 10), name, fill=color)
    draw.text((idx * cell_w + 5, ground_y + 32), spec, fill=(130, 170, 220, 255))

out_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/character_scale_alignment_guide_adjusted.png'
out.save(out_path)
print(f'Adjusted scale alignment guide saved to {out_path}')
