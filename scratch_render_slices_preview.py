import os
from PIL import Image, ImageDraw

sliced_dir = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/sliced_foes'
files = [
    # Category 1: Human Foes
    ('ashigaru.png', 'Ashigaru Spearman', 'Guard / Yari'),
    ('ronin.png', 'Masterless Ronin', 'Katana Duelist'),
    ('archer.png', 'Yumi-Ashi Archer', 'Composite Bow'),
    ('sumo.png', 'Sumo Rikishi', 'Heavy Roadblock'),
    
    # Category 2: Yokai Beasts
    ('oni.png', 'Blue Horned Oni', 'Ogre / Kanabo'),
    ('tengu.png', 'Crow Tengu', 'Winged Goblin'),
    ('tsuchigumo.png', 'Tsuchigumo', 'Cave Spider'),
    ('hitodama.png', 'Hitodama Wisps', 'Spirit Flame'),
    
    # Category 3: Cursed Stage Hazards
    ('karakasa_obake.png', 'Karakasa-Obake', 'Umbrella Yokai'),
    ('ancestral_katana.png', 'Ancestral Katana', 'Cursed Blade'),
    ('cursed_well.png', 'Cursed Well', 'Ghostly Well'),
    ('broken_stone_lantern.png', 'Broken Lantern', 'Purple Eye Toro'),
    
    # Category 4: Ninjas & Mystical
    ('ninja_blue_standing.png', 'Blue Shinobi', 'Hero / Mirror'),
    ('ninja_brown_prayer.png', 'Brown Shinobi', 'Earth Clan'),
    ('ninja_cyan_crouch.png', 'Cyan Shinobi', 'Wind Scout'),
    ('ninja_purple_kunoichi.png', 'Purple Kunoichi', 'Swift Assassin'),
    ('ninja_dark_infiltrator.png', 'Dark Shinobi', 'Night Clan'),
    ('ninja_ghostly.png', 'Ghostly Shinobi', 'Translucent Spirit'),
    ('kitsune_trio.png', 'Kitsune Trio', 'Multi-Tailed Spirit'),
    
    # Category 5: Effects & Projectiles
    ('shadow_portal.png', 'Shadow Portal', 'Spawn Void Vortex'),
    ('oni_rage_ofuda.png', 'Ofuda Talismans', 'Rage Seals'),
    ('tengu_gust.png', 'Tengu Gust', 'Wind Blast Spiral'),
    ('cursed_arrow.png', 'Cursed Arrow', 'Spectral Arrow'),
    ('smoke_cloud.png', 'Impact Cloud', 'Smoke Puff'),
    
    # Category 6: Collectibles
    ('magatama_cluster.png', 'Magatama Jewels', 'Sacred Pickups'),
    ('caltrops_cluster.png', 'Ninja Caltrops', 'Floor Spikes')
]

# Layout: 4 columns
cols = 4
rows = (len(files) + cols - 1) // cols
cell_w = 260
cell_h = 240
grid_w = cols * cell_w
grid_h = rows * cell_h + 85

# Dark slate presentation background
out = Image.new('RGBA', (grid_w, grid_h), (16, 22, 34, 255))
draw = ImageDraw.Draw(out)

# Header
draw.rectangle([0, 0, grid_w, 75], fill=(24, 34, 52, 255))
draw.text((25, 16), "TRANSPARENT SLICED ASSET PREVIEW (28 SLICES)", fill=(255, 215, 0, 255))
draw.text((25, 45), "Alpha cutout check against dark background to verify crisp silhouettes & zero white halos", fill=(170, 195, 230, 255))

# Checkerboard helper for checking transparency
check_size = 8
c1 = (22, 30, 46)
c2 = (28, 38, 58)

for idx, (fname, name, tag) in enumerate(files):
    r = idx // cols
    c = idx % cols
    x0 = c * cell_w
    y0 = 85 + r * cell_h
    
    # Card outline
    draw.rectangle([x0 + 8, y0 + 8, x0 + cell_w - 8, y0 + cell_h - 8], fill=(22, 30, 46, 255), outline=(42, 58, 86, 255), width=2)
    
    # Checkerboard area for sprite display
    chk_x0, chk_y0, chk_x1, chk_y1 = x0 + 16, y0 + 16, x0 + cell_w - 16, y0 + 155
    for cy in range(chk_y0, chk_y1, check_size):
        for cx in range(chk_x0, chk_x1, check_size):
            color = c1 if ((cx // check_size) + (cy // check_size)) % 2 == 0 else c2
            draw.rectangle([cx, cy, min(cx + check_size, chk_x1), min(cy + check_size, chk_y1)], fill=color)
            
    p = os.path.join(sliced_dir, fname)
    if os.path.exists(p):
        im = Image.open(p).convert('RGBA')
        scale = min((cell_w - 40) / im.width, 130 / im.height)
        nw = int(im.width * scale)
        nh = int(im.height * scale)
        im_scaled = im.resize((nw, nh), Image.Resampling.LANCZOS)
        
        im_x = x0 + (cell_w - nw) // 2
        im_y = y0 + 16 + (139 - nh) // 2
        out.paste(im_scaled, (im_x, im_y), im_scaled)
        
    draw.text((x0 + 16, y0 + 165), name, fill=(245, 248, 255, 255))
    draw.text((x0 + 16, y0 + 190), tag, fill=(120, 175, 240, 255))
    draw.text((x0 + 16, y0 + 212), fname, fill=(100, 120, 150, 255))

out_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/sliced_assets_transparent_preview.png'
out.save(out_path)
print(f'Saved preview to {out_path}')
