import os
from PIL import Image

images_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"
out_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b"

W, H = 1024, 576
canvas = Image.new("RGBA", (W, H), (12, 16, 26, 255))

# 1. Sky Sunset (Layer 1)
sky = Image.open(os.path.join(images_dir, "level2_layer1_sky_sunset.png")).convert("RGBA").resize((W, H))
canvas.paste(sky, (0, 0), sky)

# 2. Distant Mountains (Layer 2)
mountains = Image.open(os.path.join(images_dir, "level2_layer2_distant_mountains.png")).convert("RGBA").resize((W, H))
canvas.paste(mountains, (0, 0), mountains)

# 3. Midground Bamboo Grove (Layer 3 - lowered to horizon)
grove = Image.open(os.path.join(images_dir, "level2_layer3_midground_bamboo.png")).convert("RGBA")
grove_scaled = grove.resize((W, 260))
canvas.paste(grove_scaled, (0, H - 260), grove_scaled)

# 4. Ground Blocks (Modular ground roots from props)
root = Image.open(os.path.join(images_dir, "prop_root_block.png")).convert("RGBA")
# Ground platforms
canvas.paste(root.resize((310, 136)), (0, 440), root.resize((310, 136)))
canvas.paste(root.resize((310, 136)), (714, 440), root.resize((310, 136)))

# 5. Grand Torii Gate (cleanly extracted!)
torii = Image.open(os.path.join(images_dir, "prop_grand_torii.png")).convert("RGBA")
torii_scaled = torii.resize((150, 200))
canvas.paste(torii_scaled, (40, 440 - 195), torii_scaled)

# 6. Stone Lanterns Toro (cleanly extracted!)
lantern = Image.open(os.path.join(images_dir, "prop_stone_lantern_toro.png")).convert("RGBA").resize((40, 68))
canvas.paste(lantern, (200, 440 - 65), lantern)
canvas.paste(lantern, (760, 440 - 65), lantern)

# 7. Elevated Bamboo Platforms (cleanly extracted!)
plat = Image.open(os.path.join(images_dir, "prop_bamboo_platform.png")).convert("RGBA").resize((150, 75))
canvas.paste(plat, (260, 360), plat)
canvas.paste(plat, (610, 330), plat)

bridge = Image.open(os.path.join(images_dir, "prop_log_bridge.png")).convert("RGBA").resize((160, 75))
canvas.paste(bridge, (430, 360), bridge)

# 8. Ninja Player
ninja = Image.open(os.path.join(images_dir, "character_ninja.png")).convert("RGBA").resize((56, 58))
canvas.paste(ninja, (140, 440 - 58), ninja)

# 9. Foreground Stalks (Side Vignettes ONLY - 100px width on sides, NOT covering player!)
stalk_l = Image.open(os.path.join(images_dir, "prop_bamboo_stalk_left.png")).convert("RGBA").resize((110, H))
stalk_r = Image.open(os.path.join(images_dir, "prop_bamboo_stalk_right.png")).convert("RGBA").resize((110, H))
canvas.paste(stalk_l, (0, 0), stalk_l)
canvas.paste(stalk_r, (W - 110, 0), stalk_r)

canvas.save(os.path.join(out_dir, "test_composite_v2.png"))
print("Saved clean composite v2!")
