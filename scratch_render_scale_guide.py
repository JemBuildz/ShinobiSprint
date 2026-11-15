from PIL import Image, ImageDraw

hero_path = 'assets/images/character_ninja.png'
foes_dir = 'assets/images/foes'

hero = Image.open(hero_path).convert('RGBA')
ninja_h = 52 # Baseline player height

# Accurate scale targets so eyes/head/body line up directly with the ninja
# For wide sprites (archer with bow, ashigaru with horizontal spear), scale by human body height:
# ashigaru raw: (360, 250) -> helmet to toes is approx 200px of the 250px height. To make body 52px, total h = 52 * (250/200) = 65px
# archer raw: (253, 165) -> top knot to toes is ~135px. To make body 52px, total h = 52 * (165/135) = 63px
# ronin raw: (163, 280) -> top knot to toes is ~260px. total h = 56px
# sumo raw: (268, 205) -> head to feet is ~180px. total h = 59px
# oni raw: (234, 235) -> ogre brute is ~68px total
# tengu raw: (301, 238) -> wings/hat to feet is ~60px total
# karakasa raw: (259, 245) -> ~50px total
# kitsune raw: (257, 240) -> ~44px total

hero_w = int(hero.width * (ninja_h / hero.height))
hero_scaled = hero.resize((hero_w, ninja_h), Image.Resampling.LANCZOS)

foes = [
    ('hero', hero_scaled, 'Player (Hero)', 'Height: 52px (Baseline)'),
    ('ashigaru.png', 65, 'Ashigaru Spearman', 'Body matched to 52px'),
    ('ronin.png', 56, 'Masterless Ronin', 'Body matched to 52px'),
    ('archer.png', 63, 'Yumi-Ashi Archer', 'Body matched to 52px'),
    ('sumo.png', 59, 'Sumo Rikishi', 'Body matched to 52px'),
    ('oni.png', 68, 'Blue Horned Oni', 'Ogre Brute: 68px'),
    ('tengu.png', 60, 'Crow Tengu', 'Winged: 60px'),
    ('karakasa.png', 50, 'Karakasa-Obake', 'Umbrella: 50px'),
    ('kitsune.png', 44, 'Kitsune Trio', 'Spirits: 44px')
]

cell_w = 120
cell_h = 160
total_w = len(foes) * cell_w
total_h = cell_h + 80

out = Image.new('RGBA', (total_w, total_h), (20, 26, 40, 255))
draw = ImageDraw.Draw(out)

# Header
draw.rectangle([0, 0, total_w, 60], fill=(28, 38, 60, 255))
draw.text((20, 12), "1:1 CHARACTER SCALE CALIBRATION (ALIGNED TO 52px GROUND BASELINE)", fill=(255, 215, 0, 255))
draw.text((20, 36), "Red line indicates the 52px head level for human characters. Green line is cobblestone ground.", fill=(170, 200, 240, 255))

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
    draw.text((idx * cell_w + 5, ground_y + 10), name, fill=(240, 245, 255, 255))
    draw.text((idx * cell_w + 5, ground_y + 32), spec, fill=(130, 170, 220, 255))

out_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/character_scale_alignment_guide.png'
out.save(out_path)
print(f'Updated scale alignment guide saved to {out_path}')
