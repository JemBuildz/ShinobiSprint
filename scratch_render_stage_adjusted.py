from PIL import Image

bg_path = 'assets/images/stage1_daytime_torii_shrine_1024.png'
bg = Image.open(bg_path).convert('RGBA')

hero_path = 'assets/images/character_ninja.png'
foes_dir = 'assets/images/foes'

hero = Image.open(hero_path).convert('RGBA')
ninja_h = 52
hero_w = int(hero.width * (ninja_h / hero.height))
hero_scaled = hero.resize((hero_w, ninja_h), Image.Resampling.LANCZOS)

# Newly adjusted proportions:
# Ashigaru: 48px
# Archer: 46px
# Oni: 54px
# Ronin: 54px
# Kitsune: 44px
entities = [
    ('hero', hero_scaled, 340, 350, 'bottom'),
    ('ashigaru.png', 48, 620, 350, 'bottom'),
    ('archer.png', 46, 80, 265, 'bottom'),
    ('ronin.png', 54, 480, 350, 'bottom'),
    ('kitsune.png', 44, 255, 350, 'bottom'),
    ('oni.png', 54, 920, 150, 'bottom'),
    ('hitodama.png', 40, 770, 260, 'center')
]

for item in entities:
    fname = item[0]
    val = item[1]
    x = item[2]
    y = item[3]
    anchor = item[4]
    
    if fname == 'hero':
        img = val
    else:
        raw = Image.open(f'{foes_dir}/{fname}').convert('RGBA')
        th = val
        scale = th / raw.height
        w = int(raw.width * scale)
        h = int(raw.height * scale)
        img = raw.resize((w, h), Image.Resampling.LANCZOS)
        
    w, h = img.size
    if anchor == 'bottom':
        px = x - w // 2
        py = y - h
    else:
        px = x - w // 2
        py = y - h // 2
        
    bg.paste(img, (px, py), img)

out_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stage1_adjusted_placement_preview.png'
bg.save(out_path)
print(f'Saved adjusted stage preview to {out_path}')
