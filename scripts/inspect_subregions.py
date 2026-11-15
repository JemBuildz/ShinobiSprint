from PIL import Image

# Let's inspect day_torii_and_shrines.png (480x129)
# The torii gate is in the center-left: around x=200..320, y=30..125
torii_crop = Image.open('scripts/day_torii_and_shrines.png')
# Save test slices to find exact bounds
torii_crop.crop((240, 20, 350, 125)).save('scripts/sub_torii.png')
torii_crop.crop((110, 30, 210, 125)).save('scripts/sub_pagoda_1.png')
torii_crop.crop((380, 40, 480, 125)).save('scripts/sub_pagoda_2.png')

# Buildings & lamps (480x131)
bldg = Image.open('scripts/day_buildings_lamps.png')
bldg.crop((150, 20, 230, 125)).save('scripts/sub_lantern_1.png')
bldg.crop((360, 20, 450, 125)).save('scripts/sub_lantern_2.png')
bldg.crop((20, 10, 180, 125)).save('scripts/sub_house_1.png')
bldg.crop((250, 10, 475, 125)).save('scripts/sub_house_2.png')

# Paths & wooden planks (480x149)
path = Image.open('scripts/day_path_planks.png')
path.crop((160, 80, 280, 140)).save('scripts/sub_wood_plank_1.png')
path.crop((300, 75, 475, 145)).save('scripts/sub_wood_bridge.png')
path.crop((180, 10, 260, 120)).save('scripts/sub_path_lantern.png')

print("Saved test sub-crops")
