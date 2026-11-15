import os
from PIL import Image

images_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"
out_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b"

W, H = 1024, 576
canvas = Image.new("RGBA", (W, H), (12, 16, 26, 255))

# 1. Sky
sky = Image.open(os.path.join(images_dir, "level2_layer1_sky_sunset.png")).convert("RGBA").resize((W, H))
canvas.paste(sky, (0, 0), sky)

# 2. Distant Mountains
mountains = Image.open(os.path.join(images_dir, "level2_layer2_distant_mountains.png")).convert("RGBA").resize((W, H))
canvas.paste(mountains, (0, 0), mountains)

# 3. Midground Grove (positioned lower so mountains and sky are visible!)
# The grove should be positioned at the horizon around y = 140..576
grove = Image.open(os.path.join(images_dir, "level2_layer3_midground_bamboo.png")).convert("RGBA")
# Resize grove width to W and height to ~380
grove_scaled = grove.resize((W, 360))
canvas.paste(grove_scaled, (0, H - 360), grove_scaled)

# 4. Ground Blocks (autumn terrain)
block = Image.open(os.path.join(images_dir, "tile_autumn_block.png")).convert("RGBA")
# Paste ground blocks across bottom
for x in range(0, 320, 100):
    canvas.paste(block.resize((110, 130)), (x, 446), block.resize((110, 130)))
for x in range(700, 1024, 100):
    canvas.paste(block.resize((110, 130)), (x, 446), block.resize((110, 130)))

# 5. Grand Torii Gate (scaled appropriately)
torii = Image.open(os.path.join(images_dir, "prop_grand_torii.png")).convert("RGBA")
torii_scaled = torii.resize((140, 185))
canvas.paste(torii_scaled, (50, 446 - 180), torii_scaled)

# 6. Stone Lanterns
lantern = Image.open(os.path.join(images_dir, "prop_stone_lantern_toro.png")).convert("RGBA").resize((38, 64))
canvas.paste(lantern, (200, 446 - 60), lantern)
canvas.paste(lantern, (760, 446 - 60), lantern)

# 7. Elevated Bamboo Platform & Bridge
plat = Image.open(os.path.join(images_dir, "prop_bamboo_platform.png")).convert("RGBA").resize((160, 80))
canvas.paste(plat, (280, 350), plat)
canvas.paste(plat, (600, 310), plat)

bridge = Image.open(os.path.join(images_dir, "prop_log_bridge.png")).convert("RGBA").resize((180, 80))
canvas.paste(bridge, (430, 340), bridge)

# 8. Ninja Player
ninja = Image.open(os.path.join(images_dir, "character_ninja.png")).convert("RGBA").resize((56, 58))
canvas.paste(ninja, (150, 446 - 58), ninja)

# 9. Foreground Stalks (subtle, framing edges)
fg = Image.open(os.path.join(images_dir, "level2_layer5_foreground_blur.png")).convert("RGBA").resize((W, H))
# Paste with slight opacity or as framing
canvas.paste(fg, (0, 0), fg)

canvas.save(os.path.join(out_dir, "test_composite.png"))
print("Saved test composite to", os.path.join(out_dir, "test_composite.png"))
