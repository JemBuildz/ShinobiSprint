from PIL import Image
import os

images = [
    'assets/concept_art.jpg',
    'assets/images/concept_1_day.png',
    'assets/images/concept_2_night.png',
    'assets/images/concept_day_wide.png',
    'assets/images/concept_night_wide.png',
    'assets/images/wide_day_strip.png',
    'assets/images/wide_night_strip.png',
]

for img_path in images:
    if os.path.exists(img_path):
        im = Image.open(img_path)
        print(f"{img_path}: size={im.size}, mode={im.mode}")
