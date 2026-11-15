from PIL import Image

# Load the stage background
bg_path = 'assets/images/stage1_daytime_torii_shrine_1024.png'
bg = Image.open(bg_path).convert('RGBA')

foes_dir = 'assets/images/foes'

# Stage size is 1024 x 576
# Ground cobblestone baseline is Y = 350
# Left shrine terrace landing is Y = 265
# Upper mountain temple landing is Y = 150

# Let's place:
# 1. Ashigaru Spearman on right cobblestones (X = 640, ground Y = 350)
# 2. Yumi-Ashi Archer on left shrine terrace (X = 80, landing Y = 265)
# 3. Kitsune multi-tail spirit next to Fox Statue (X = 270, ground Y = 350)
# 4. Shadow Portal hovering near Grand Torii arch (X = 770, mid-air Y = 250)
# 5. Blue Horned Oni on upper temple terrace (X = 930, landing Y = 150)
# 6. Magatama collectible floating near Torii gate (X = 470, Y = 270)
# 7. Player Chibi Ninja standing on central courtyard (X = 350, ground Y = 350)

spawns = [
    ('ashigaru.png', 620, 350, 75, 'bottom'),
    ('archer.png', 75, 265, 65, 'bottom'),
    ('kitsune.png', 265, 350, 60, 'bottom'),
    ('shadow_portal.png', 760, 240, 65, 'center'),
    ('oni.png', 925, 150, 72, 'bottom'),
    ('magatama.png', 465, 270, 38, 'center'),
    ('ninja_blue.png', 340, 350, 52, 'bottom')
]

for fname, x, y, target_h, anchor in spawns:
    p = f'{foes_dir}/{fname}'
    im = Image.open(p).convert('RGBA')
    scale = target_h / im.height
    w = int(im.width * scale)
    h = int(im.height * scale)
    im_scaled = im.resize((w, h), Image.Resampling.LANCZOS)
    
    if anchor == 'bottom':
        paste_x = x - w // 2
        paste_y = y - h
    else: # center
        paste_x = x - w // 2
        paste_y = y - h // 2
        
    bg.paste(im_scaled, (paste_x, paste_y), im_scaled)

out_preview = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stage1_enemy_placement_preview.png'
bg.save(out_preview)
print(f'Stage placement preview saved to {out_preview}')
