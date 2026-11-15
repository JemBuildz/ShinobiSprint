import os
from PIL import Image, ImageDraw

bg_path = 'assets/images/stage1_daytime_torii_shrine_1024.png'
bg = Image.open(bg_path).convert('RGBA')

hero_path = 'assets/images/character_ninja.png'
hero_clean_path = 'assets/images/clean_chibi_ninja.png'
foes_dir = 'assets/images/foes'

hero = Image.open(hero_path).convert('RGBA')
# Target ninja height in game is 52px
ninja_h = 52
hero_w = int(hero.width * (ninja_h / hero.height))
hero_scaled = hero.resize((hero_w, ninja_h), Image.Resampling.LANCZOS)

# Spawn positions scaled to match ninja's 52px height proportion
# (filename, x, y, target_h, label)
# Ground cobblestones: Y = 350
# Shrine terrace: Y = 265
# Mountain temple: Y = 150
entities = [
    # Hero player (ORIGINAL CHARACTER)
    ('hero', hero_scaled, 340, 350, 'bottom', 'Player Ninja (Height: 52px)'),
    
    # Ashigaru: spear reaches out, body height = 52px
    ('ashigaru.png', None, 640, 350, 'bottom', 'Ashigaru (Body H: 52px)'),
    
    # Yumi-Ashi Archer on left shrine terrace
    ('archer.png', None, 80, 265, 'bottom', 'Archer (Height: 52px)'),
    
    # Masterless Ronin on courtyard
    ('ronin.png', None, 480, 350, 'bottom', 'Ronin (Height: 52px)'),
    
    # Kitsune Fox Spirit next to Fox Statue
    ('kitsune.png', None, 255, 350, 'bottom', 'Kitsune (Height: 46px)'),
    
    # Blue Oni on upper temple (slightly larger boss proportion: 64px)
    ('oni.png', None, 920, 150, 'bottom', 'Oni Boss (Height: 64px)'),
    
    # Hitodama Wisps floating mid-air
    ('hitodama.png', None, 770, 260, 'center', 'Hitodama (Height: 42px)')
]

draw = ImageDraw.Draw(bg)

for item in entities:
    fname = item[0]
    img = item[1]
    x = item[2]
    y = item[3]
    anchor = item[4]
    label = item[5]
    
    if img is None:
        p = os.path.join(foes_dir, fname)
        raw_im = Image.open(p).convert('RGBA')
        
        # Scale to match ninja height
        if fname == 'ashigaru.png':
            # Ashigaru has a long spear extending upwards, so scale based on soldier body (~52px)
            target_h = 56
        elif fname == 'oni.png':
            target_h = 64 # Brute ogre
        elif fname == 'kitsune.png':
            target_h = 44 # Small spirit foxes
        elif fname == 'hitodama.png':
            target_h = 40 # Spirit flame cluster
        else:
            target_h = 52 # Matched 1:1 with player ninja height
            
        scale = target_h / raw_im.height
        w = int(raw_im.width * scale)
        h = int(raw_im.height * scale)
        img = raw_im.resize((w, h), Image.Resampling.LANCZOS)
        
    w, h = img.size
    if anchor == 'bottom':
        px = x - w // 2
        py = y - h
    else:
        px = x - w // 2
        py = y - h // 2
        
    bg.paste(img, (px, py), img)

out_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/calibrated_size_enemy_preview.png'
bg.save(out_path)
print(f'Saved calibrated preview to {out_path}')
