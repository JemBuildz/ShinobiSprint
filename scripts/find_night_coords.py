from PIL import Image

nb = Image.open('scripts/night_buildings_lamps.png')
# size is (500, 131)
# Let's save 3 crops across the width
nb.crop((0, 0, 150, 131)).save('scripts/night_b_left.png')
nb.crop((120, 0, 300, 131)).save('scripts/night_b_mid.png')
nb.crop((280, 0, 500, 131)).save('scripts/night_b_right.png')

np = Image.open('scripts/night_path_planks.png')
# size is (500, 149)
np.crop((0, 0, 250, 149)).save('scripts/night_p_left.png')
np.crop((250, 0, 500, 149)).save('scripts/night_p_right.png')

print("Saved night slices")
