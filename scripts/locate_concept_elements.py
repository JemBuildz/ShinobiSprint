from PIL import Image

im = Image.open('assets/concept_art.jpg')
w, h = im.size
print(f"Concept art dimensions: {w}x{h}")

# In concept_art.jpg:
# Header is at top: ~0..88 px
# Left half: Daytime assets (x: ~30..510)
# Right half: Nighttime assets (x: ~515..1015)
# Row 1 (Sky): y ~89..209
# Row 2 (Mountains): y ~210..338
# Row 3 (Bamboo / Torii / Pagodas): y ~339..468
# Row 4 (Buildings / Lanterns / Rocks): y ~469..600
# Row 5 (Paths / Bridges / Streams): y ~601..750

crops = {
    'day_torii_and_shrines': (30, 339, 510, 468),
    'night_torii_and_shrines': (515, 339, 1015, 468),
    'day_buildings_lamps': (30, 469, 510, 600),
    'night_buildings_lamps': (515, 469, 1015, 600),
    'day_path_planks': (30, 601, 510, 750),
    'night_path_planks': (515, 601, 1015, 750),
}

for name, box in crops.items():
    crop = im.crop(box)
    crop.save(f'scripts/{name}.png')
    print(f"Saved scripts/{name}.png: {crop.size}")
