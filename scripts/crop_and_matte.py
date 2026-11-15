from PIL import Image
import numpy as np

concept = Image.open('assets/concept_art.jpg').convert('RGB')

# Let's crop precise regions
crops = {
    'torii_gate_day': (285, 360, 395, 460),
    'torii_gate_night': (795, 360, 905, 460),
    'pagoda_shrine_day': (140, 365, 220, 445),
    'pagoda_shrine_night': (630, 365, 710, 445),
    'house_shrine_day': (400, 475, 510, 585),
    'house_shrine_night': (880, 475, 1010, 585),
    'lantern_post_day': (190, 480, 245, 585),
    'lantern_post_night': (800, 605, 875, 720),
    'boardwalk_planks_day': (315, 655, 470, 740),
    'boardwalk_planks_night': (740, 660, 890, 740),
    'bamboo_stalks_day': (55, 345, 135, 460),
    'bamboo_stalks_night': (525, 345, 615, 460),
}

for name, box in crops.items():
    c = concept.crop(box)
    c.save(f'scripts/{name}.png')
    print(f"Saved {name}: {c.size}")
