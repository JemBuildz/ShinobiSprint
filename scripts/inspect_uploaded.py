import os
from PIL import Image
import numpy as np

user_uploaded_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b\.user_uploaded"
images = [
    "media_1791003813295.jpg", # Mockup reference
    "media_1791003836740.jpg", # Backdrop plate
    "media_1791003847743.jpg", # Props structures
    "media_1791003862025.jpg", # Platforms & bridge
    "media_1791003869353.jpg", # Tileset ground
    "media_1791004147591.jpg", # Character ninja (checkerboard bg)
]

for img_name in images:
    p = os.path.join(user_uploaded_dir, img_name)
    if os.path.exists(p):
        im = Image.open(p)
        print(f"{img_name}: size={im.size}, mode={im.mode}")
    else:
        print(f"{img_name}: NOT FOUND")
