import os
from PIL import Image, ImageDraw

src_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stitch_character_assets/ShinobiSprint_Game_Characters_2048.png'
im = Image.open(src_path).convert('RGBA')
W, H = im.size # 2048, 2048

# Coordinates for all elements on the 2048x2048 canvas
# (name, [left, top, right, bottom], category)
elements = [
    # A) Human Enemies
    ('ashigaru', [100, 160, 520, 500], 'Human Enemy'),
    ('ronin', [270, 500, 480, 800], 'Human Enemy'),
    ('archer', [240, 800, 520, 1100], 'Human Enemy'),
    ('sumo', [260, 1100, 540, 1340], 'Human Enemy'),
    
    # B) Yokai Beasts
    ('oni', [820, 170, 1100, 500], 'Yokai Beast'),
    ('tengu', [820, 510, 1150, 810], 'Yokai Beast'),
    ('tsuchigumo', [820, 830, 1160, 1070], 'Yokai Beast'),
    ('hitodama', [830, 1070, 1140, 1330], 'Yokai Beast'),
    
    # C) Cursed Props
    ('karakasa_obake', [1360, 180, 1660, 500], 'Cursed Prop'),
    ('ancestral_katana', [1320, 580, 1700, 770], 'Cursed Prop'),
    ('cursed_well', [1350, 820, 1660, 1070], 'Cursed Prop'),
    ('broken_stone_lantern', [1370, 1080, 1610, 1340], 'Cursed Prop'),
    
    # Column next to C: Ninjas
    ('ninja_blue_standing', [1750, 190, 1930, 450], 'Ninja Variant'),
    ('ninja_brown_prayer', [1750, 460, 1930, 710], 'Ninja Variant'),
    ('ninja_cyan_crouch', [1750, 710, 1930, 910], 'Ninja Variant'),
    ('ninja_purple_kunoichi', [1730, 910, 1960, 1140], 'Ninja Variant'),
    ('ninja_dark_infiltrator', [1750, 1140, 1950, 1370], 'Ninja Variant'),
    
    # D) Mystical Foes
    ('ninja_blue_alt', [100, 1450, 300, 1720], 'Mystical Foe'),
    ('ninja_ghostly', [330, 1450, 530, 1720], 'Mystical Foe'),
    ('ninja_purple_alt', [100, 1730, 280, 1980], 'Mystical Foe'),
    ('kitsune_trio', [320, 1730, 600, 1980], 'Mystical Foe'),
    
    # E) Enemy Effect Sprites
    ('shadow_portal', [950, 1440, 1220, 1660], 'Effect Sprite'),
    ('oni_rage_ofuda', [740, 1720, 990, 1890], 'Effect Sprite'),
    ('tengu_gust', [980, 1680, 1210, 1840], 'Effect Sprite'),
    ('smoke_cloud', [1210, 1700, 1410, 1860], 'Effect Sprite'),
    ('cursed_arrow', [970, 1870, 1230, 1990], 'Effect Sprite'),
    
    # F) Mystical Items
    ('magatama_cluster', [1640, 1460, 1900, 1660], 'Mystical Item'),
    ('caltrops_cluster', [1660, 1780, 1900, 1940], 'Mystical Item')
]

# Create debug overlay to verify bounding boxes
debug_img = im.copy()
draw = ImageDraw.Draw(debug_img)

for name, box, cat in elements:
    draw.rectangle(box, outline=(255, 0, 0, 255), width=4)
    draw.text((box[0] + 5, box[1] + 5), name, fill=(255, 255, 0, 255))

debug_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/slice_boxes_verification.png'
debug_img.save(debug_path)
print(f'Verification image saved to {debug_path}')
