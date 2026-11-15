import os
import numpy as np
from PIL import Image, ImageFilter

os.makedirs('assets/map/cutouts', exist_ok=True)
os.makedirs('assets/map/tiles', exist_ok=True)
os.makedirs('assets/map/objects', exist_ok=True)

concept = Image.open('assets/concept_art.jpg').convert('RGBA')

# -------------------------------------------------------------------------
# 1. EXTRACT TORII GATE (Daytime Vermilion & Nighttime)
# -------------------------------------------------------------------------
# In concept art, the red Torii gate is at:
# X: ~298 to 388, Y: ~372 to 455
torii_box = (296, 372, 390, 458)
torii_img = concept.crop(torii_box)
t_arr = np.array(torii_img, dtype=float)

# Background is pale teal/cream sky: R: 180..240, G: 210..245, B: 190..235
# Red gate has high R, low G, low B (R - G > 30 or R - B > 30), or dark wood/black base (R < 80, G < 80, B < 80)
r = t_arr[:, :, 0]
g = t_arr[:, :, 1]
b = t_arr[:, :, 2]

# Gate condition: strong red OR dark pillar base OR beam shadow
is_red = (r > 110) & (r > g + 25) & (r > b + 25)
is_dark_base = (r < 75) & (g < 75) & (b < 75) & (t_arr.shape[0] - np.indices(r.shape)[0] < 40)
is_wood_shadow = (r > 60) & (r < 140) & (g < 90) & (b < 80) & (r > g + 10)
is_gate = is_red | is_dark_base | is_wood_shadow

# Alpha mask creation with soft edge
alpha = np.zeros(r.shape, dtype=np.uint8)
alpha[is_gate] = 255

# Clean up small holes inside the beams using morphological closing
torii_alpha_img = Image.fromarray(alpha, mode='L')
torii_alpha_img = torii_alpha_img.filter(ImageFilter.MaxFilter(3))
torii_alpha_img = torii_alpha_img.filter(ImageFilter.MinFilter(3))
torii_alpha_img = torii_alpha_img.filter(ImageFilter.GaussianBlur(0.8))

torii_out = Image.new('RGBA', torii_img.size, (0, 0, 0, 0))
torii_out.paste(torii_img, (0, 0), torii_alpha_img)
torii_out.save('assets/map/cutouts/torii_gate.png')
print("Saved assets/map/cutouts/torii_gate.png", torii_out.size)

# -------------------------------------------------------------------------
# 2. EXTRACT LANTERNS (Standing Wooden Lantern & Stone Lantern)
# -------------------------------------------------------------------------
# In row 4 night: lantern post is at x: 735..785, y: 500..575
# In row 5 night: lantern post is at x: 415..455 in night_buildings_lamps or row 4
# Let's crop the standing glowing lantern in night_buildings_lamps:
# Coordinates in concept art:
# X: 720 to 765, Y: 505 to 580
lantern_box = (720, 502, 765, 582)
lantern_img = concept.crop(lantern_box)
l_arr = np.array(lantern_img, dtype=float)
lr = l_arr[:, :, 0]
lg = l_arr[:, :, 1]
lb = l_arr[:, :, 2]

# The glowing lantern has bright orange flame (R > 180, G > 90, B < 80)
# and dark cedar post/roof (R < 90, G < 60, B < 60)
# Background is dark misty violet (B > R or G ~ B, R < 70)
is_glow = (lr > 140) & (lg > 60) & (lb < 90)
is_post = (lr > 30) & (lr < 110) & (lg < 75) & (lb < 75) & (lr >= lb)
is_lantern = is_glow | is_post

l_alpha = np.zeros(lr.shape, dtype=np.uint8)
l_alpha[is_lantern] = 255
l_alpha_img = Image.fromarray(l_alpha, mode='L')
l_alpha_img = l_alpha_img.filter(ImageFilter.MaxFilter(3))
l_alpha_img = l_alpha_img.filter(ImageFilter.MinFilter(3))
l_alpha_img = l_alpha_img.filter(ImageFilter.GaussianBlur(0.7))

lantern_out = Image.new('RGBA', lantern_img.size, (0, 0, 0, 0))
lantern_out.paste(lantern_img, (0, 0), l_alpha_img)
lantern_out.save('assets/map/cutouts/lantern_standing_glowing.png')
print("Saved assets/map/cutouts/lantern_standing_glowing.png", lantern_out.size)

# Stone lantern from day layer (x: 200..235, y: 500..570)
stone_lantern_box = (200, 500, 238, 575)
stone_l_img = concept.crop(stone_lantern_box)
sl_arr = np.array(stone_l_img, dtype=float)
sl_r, sl_g, sl_b = sl_arr[:, :, 0], sl_arr[:, :, 1], sl_arr[:, :, 2]
is_stone_l = (sl_r > 130) & (sl_g > 60) | ((sl_r < 90) & (sl_g < 80) & (sl_b < 70))
sl_alpha = np.zeros(sl_r.shape, dtype=np.uint8)
sl_alpha[is_stone_l] = 255
sl_alpha_img = Image.fromarray(sl_alpha, mode='L').filter(ImageFilter.GaussianBlur(0.7))
stone_l_out = Image.new('RGBA', stone_l_img.size, (0, 0, 0, 0))
stone_l_out.paste(stone_l_img, (0, 0), sl_alpha_img)
stone_l_out.save('assets/map/cutouts/lantern_stone_day.png')
print("Saved assets/map/cutouts/lantern_stone_day.png", stone_l_out.size)

# -------------------------------------------------------------------------
# 3. EXTRACT PAGODA SHRINEL & JAPANESE TIMBER HOUSE
# -------------------------------------------------------------------------
# Pagoda in day row 3: X: 150..215, Y: 370..445
pagoda_box = (150, 368, 215, 445)
pagoda_img = concept.crop(pagoda_box)
p_arr = np.array(pagoda_img, dtype=float)
pr, pg, pb = p_arr[:, :, 0], p_arr[:, :, 1], p_arr[:, :, 2]
# Pagoda has dark timber and terra-cotta roofs (R > G, R < 140, G < 110)
is_pagoda = (pr > 50) & (pr < 150) & (pg < 115) & (pb < 100) & (pr > pg + 5)
p_alpha = np.zeros(pr.shape, dtype=np.uint8)
p_alpha[is_pagoda] = 255
p_alpha_img = Image.fromarray(p_alpha, mode='L')
p_alpha_img = p_alpha_img.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
pagoda_out = Image.new('RGBA', pagoda_img.size, (0, 0, 0, 0))
pagoda_out.paste(pagoda_img, (0, 0), p_alpha_img)
pagoda_out.save('assets/map/cutouts/pagoda_shrine.png')
print("Saved assets/map/cutouts/pagoda_shrine.png", pagoda_out.size)

# Japanese House in day row 4: X: 420..505, Y: 485..580
house_box = (420, 485, 508, 582)
house_img = concept.crop(house_box)
h_arr = np.array(house_img, dtype=float)
hr, hg, hb = h_arr[:, :, 0], h_arr[:, :, 1], h_arr[:, :, 2]
is_house = (hr > 40) & (hr < 160) & (hg < 120) & (hb < 105) | ((hr > 180) & (hg > 120) & (hb < 80)) # glowing windows
h_alpha = np.zeros(hr.shape, dtype=np.uint8)
h_alpha[is_house] = 255
h_alpha_img = Image.fromarray(h_alpha, mode='L').filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
house_out = Image.new('RGBA', house_img.size, (0, 0, 0, 0))
house_out.paste(house_img, (0, 0), h_alpha_img)
house_out.save('assets/map/cutouts/japanese_house.png')
print("Saved assets/map/cutouts/japanese_house.png", house_out.size)

# -------------------------------------------------------------------------
# 4. EXTRACT WOODEN BOARDWALK PLATFORM
# -------------------------------------------------------------------------
# Bridge planks in day row 5: X: 320..460, Y: 655..705
planks_box = (320, 655, 460, 705)
planks_img = concept.crop(planks_box)
w_arr = np.array(planks_img, dtype=float)
wr, wg, wb = w_arr[:, :, 0], w_arr[:, :, 1], w_arr[:, :, 2]
# Wood planks are cedar/reddish brown (R > 80, R > G + 15, R > B + 25)
is_planks = (wr > 75) & (wr > wg + 15) & (wr > wb + 20) & (wb < 90)
w_alpha = np.zeros(wr.shape, dtype=np.uint8)
w_alpha[is_planks] = 255
w_alpha_img = Image.fromarray(w_alpha, mode='L').filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
planks_out = Image.new('RGBA', planks_img.size, (0, 0, 0, 0))
planks_out.paste(planks_img, (0, 0), w_alpha_img)
planks_out.save('assets/map/cutouts/wooden_boardwalk_planks.png')
print("Saved assets/map/cutouts/wooden_boardwalk_planks.png", planks_out.size)
