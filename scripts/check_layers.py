import os
from PIL import Image

user_uploaded_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b\.user_uploaded"
images_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"

# Let's inspect the exact dimensions and transparency of all images
for name in [
    "level2_layer1_sky_sunset.png",
    "level2_layer2_distant_mountains.png",
    "level2_layer3_midground_bamboo.png",
    "level2_layer5_foreground_blur.png",
    "prop_grand_torii.png",
    "prop_bamboo_platform.png",
    "prop_log_bridge.png",
    "tile_autumn_block.png",
    "prop_stone_lantern_toro.png",
]:
    p = os.path.join(images_dir, name)
    if os.path.exists(p):
        im = Image.open(p)
        print(f"{name}: size={im.size}, mode={im.mode}")
