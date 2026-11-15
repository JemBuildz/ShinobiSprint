from PIL import Image

torii_night = Image.open('scripts/night_torii_and_shrines.png')
w, h = torii_night.size
print("night torii size:", w, h)
# In night half:
torii_night.crop((200, 20, 360, 125)).save('scripts/night_sub_torii.png')

bldg_night = Image.open('scripts/night_buildings_lamps.png')
bldg_night.crop((130, 20, 230, 125)).save('scripts/night_sub_lantern_1.png')
bldg_night.crop((340, 20, 440, 125)).save('scripts/night_sub_lantern_2.png')

path_night = Image.open('scripts/night_path_planks.png')
path_night.crop((280, 50, 470, 140)).save('scripts/night_sub_wood_bridge.png')

print("Saved night test crops")
