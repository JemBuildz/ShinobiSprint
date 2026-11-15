import os
from PIL import Image, ImageDraw, ImageFont

foes_dir = 'assets/images/foes'
files = [
    ('ashigaru.png', 'Ashigaru Spearman', 'Patrol Guard'),
    ('ronin.png', 'Masterless Ronin', 'Katana Duelist'),
    ('archer.png', 'Samurai Archer', 'Ranged Bow'),
    ('sumo.png', 'Sumo Wrestler', 'Heavy Obstacle'),
    ('oni.png', 'Blue Horned Oni', 'Ogre Brute'),
    ('tengu.png', 'Crow Tengu', 'Winged Goblin'),
    ('tsuchigumo.png', 'Tsuchigumo', 'Earth Spider'),
    ('hitodama.png', 'Hitodama Wisp', 'Ghost Spirit'),
    ('karakasa.png', 'Karakasa Kozou', 'Umbrella Yokai'),
    ('ninja_dark.png', 'Shadow Ninja', 'Dark Clan Infiltrator'),
    ('ninja_purple.png', 'Kunoichi / Violet', 'Swift Assassin'),
    ('ninja_brown.png', 'Earth Shinobi', 'Heavy Ninja'),
    ('ninja_cyan.png', 'Wind Shinobi', 'Agile Scout'),
    ('ninja_blue.png', 'Rival Shinobi', 'Mirror Foe'),
    ('ancestral_katana.png', 'Ancestral Katana', 'Cursed Relic Hazard'),
    ('cursed_well.png', 'Cursed Well', 'Reaching Hand Hazard'),
    ('broken_lantern.png', 'Broken Lantern', 'Cursed Eye Hazard')
]

# Grid layout: 4 columns
cols = 4
rows = (len(files) + cols - 1) // cols
cell_w = 260
cell_h = 240
grid_w = cols * cell_w
grid_h = rows * cell_h + 80

out_img = Image.new('RGBA', (grid_w, grid_h), (18, 24, 38, 255))
draw = ImageDraw.Draw(out_img)

# Title banner
draw.rectangle([0, 0, grid_w, 70], fill=(28, 38, 60, 255))
draw.text((20, 15), "SHINOBI SPRINT - FEUDAL FOE & ENEMY ROSTER CATALOG", fill=(255, 215, 0, 255))
draw.text((20, 42), "All 17 Active Foes, Rival Ninjas, Yokai & Cursed Hazards", fill=(180, 200, 230, 255))

for idx, (fname, name, role) in enumerate(files):
    r = idx // cols
    c = idx % cols
    x0 = c * cell_w
    y0 = 80 + r * cell_h
    
    # Cell background card
    draw.rectangle([x0 + 8, y0 + 8, x0 + cell_w - 8, y0 + cell_h - 8], fill=(26, 34, 52, 255), outline=(45, 60, 90, 255), width=2)
    
    p = os.path.join(foes_dir, fname)
    if os.path.exists(p):
        im = Image.open(p).convert('RGBA')
        # Scale to fit within 150x130 box keeping aspect
        scale = min(140 / im.width, 120 / im.height)
        new_w = int(im.width * scale)
        new_h = int(im.height * scale)
        im_scaled = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Center sprite in top area
        im_x = x0 + (cell_w - new_w) // 2
        im_y = y0 + 15 + (125 - new_h) // 2
        out_img.paste(im_scaled, (im_x, im_y), im_scaled)
    
    # Label
    draw.text((x0 + 15, y0 + 155), name, fill=(240, 245, 255, 255))
    draw.text((x0 + 15, y0 + 180), role, fill=(130, 175, 230, 255))
    draw.text((x0 + 15, y0 + 205), fname, fill=(100, 120, 150, 255))

out_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/shinobi_enemy_roster_catalog.png'
out_img.save(out_path)
print(f'Roster image saved to {out_path} ({out_img.size})')
