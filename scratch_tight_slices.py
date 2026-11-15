import os
from PIL import Image, ImageDraw

src_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stitch_character_assets/ShinobiSprint_Game_Characters_2048.png'
im = Image.open(src_path).convert('RGBA')

# Perfected coordinate boxes strictly around character art (avoiding any text labels)
elements = [
    # A) Human Enemies
    ('ashigaru', [70, 230, 500, 495], 'Human Enemy'),
    ('ronin', [275, 508, 465, 792], 'Human Enemy'),
    ('archer', [240, 815, 515, 1075], 'Human Enemy'),
    ('sumo', [260, 1105, 535, 1345], 'Human Enemy'),
    
    # B) Yokai Beasts
    ('oni', [830, 230, 1090, 495], 'Yokai Beast'),
    ('tengu', [825, 512, 1145, 808], 'Yokai Beast'),
    ('tsuchigumo', [820, 835, 1150, 1065], 'Yokai Beast'),
    ('hitodama', [835, 1075, 1140, 1325], 'Yokai Beast'),
    
    # C) Cursed Props
    ('karakasa_obake', [1365, 230, 1655, 495], 'Cursed Prop'),
    ('ancestral_katana', [1325, 590, 1690, 755], 'Cursed Prop'),
    ('cursed_well', [1355, 825, 1650, 1030], 'Cursed Prop'),
    ('broken_stone_lantern', [1375, 1080, 1600, 1325], 'Cursed Prop'),
    
    # Column next to C: Ninjas
    ('ninja_blue_standing', [1750, 200, 1930, 445], 'Ninja Variant'),
    ('ninja_brown_prayer', [1755, 460, 1935, 705], 'Ninja Variant'),
    ('ninja_cyan_crouch', [1755, 715, 1935, 905], 'Ninja Variant'),
    ('ninja_purple_kunoichi', [1735, 915, 1955, 1135], 'Ninja Variant'),
    ('ninja_dark_infiltrator', [1750, 1145, 1945, 1365], 'Ninja Variant'),
    
    # D) Mystical Foes
    ('ninja_blue_alt', [105, 1455, 295, 1715], 'Mystical Foe'),
    ('ninja_ghostly', [335, 1455, 525, 1715], 'Mystical Foe'),
    ('ninja_purple_alt', [105, 1735, 275, 1975], 'Mystical Foe'),
    ('kitsune_trio', [325, 1735, 595, 1975], 'Mystical Foe'),
    
    # E) Enemy Effect Sprites
    ('shadow_portal', [950, 1445, 1215, 1650], 'Effect Sprite'),
    ('oni_rage_ofuda', [745, 1720, 985, 1880], 'Effect Sprite'),
    ('tengu_gust', [985, 1685, 1205, 1840], 'Effect Sprite'),
    ('smoke_cloud', [1215, 1705, 1410, 1860], 'Effect Sprite'),
    ('cursed_arrow', [975, 1880, 1230, 1975], 'Effect Sprite'),
    
    # F) Mystical Items
    ('magatama_cluster', [1645, 1465, 1895, 1655], 'Mystical Item'),
    ('caltrops_cluster', [1660, 1795, 1895, 1935], 'Mystical Item')
]

debug_img = im.copy()
draw = ImageDraw.Draw(debug_img)

for name, box, cat in elements:
    draw.rectangle(box, outline=(0, 255, 0, 255), width=3)
    draw.text((box[0] + 3, box[1] + 3), name, fill=(255, 0, 0, 255))

debug_path = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/slice_boxes_tight.png'
debug_img.save(debug_path)
print('Tight verification saved!')
