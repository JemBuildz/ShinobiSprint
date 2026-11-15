import os
import glob
import numpy as np
from PIL import Image, ImageFilter

os.makedirs('assets/map/cutouts', exist_ok=True)
os.makedirs('assets/map/tiles', exist_ok=True)
os.makedirs('assets/map/objects', exist_ok=True)

artifact_dir = r'C:\Users\User\.gemini\antigravity\brain\8d1fe0d7-a367-49a2-ba0b-1e27387c2271'

def find_latest(pattern):
    files = glob.glob(os.path.join(artifact_dir, pattern))
    if not files:
        raise FileNotFoundError(f"No file matching {pattern}")
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

torii_path = find_latest('torii_gate_sprite_*.jpg')
lantern_path = find_latest('lantern_post_sprite_*.jpg')
pagoda_path = find_latest('pagoda_shrine_sprite_*.jpg')
boardwalk_path = find_latest('wooden_boardwalk_sprite_*.jpg')
house_path = find_latest('japanese_house_sprite_*.jpg')
bamboo_path = find_latest('bamboo_trees_sprite_*.jpg')

def clean_cutout(img_path, threshold=240, feather=0.7):
    im = Image.open(img_path).convert('RGB')
    arr = np.array(im, dtype=float)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    spread = max_c - min_c
    
    is_white = (min_c > threshold) & (spread < 20)
    alpha = np.ones(r.shape, dtype=float) * 255.0
    alpha[is_white] = 0.0
    
    edge_zone = (min_c >= 220) & (min_c <= 254) & (~is_white)
    if np.any(edge_zone):
        fade = (255.0 - min_c[edge_zone]) / 35.0
        alpha[edge_zone] = np.clip(fade * 255.0, 0, 255)
        
    alpha_img = Image.fromarray(alpha.astype(np.uint8), mode='L')
    if feather > 0:
        alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(feather))
        
    rgba = Image.new('RGBA', im.size, (0, 0, 0, 0))
    rgba.paste(im, (0, 0), alpha_img)
    
    bbox = rgba.getbbox()
    if bbox:
        m = 4
        bbox = (max(0, bbox[0]-m), max(0, bbox[1]-m), min(rgba.width, bbox[2]+m), min(rgba.height, bbox[3]+m))
        rgba = rgba.crop(bbox)
        
    return rgba

print("Extracting clean cutouts...")
torii = clean_cutout(torii_path, threshold=242)
torii.save('assets/map/cutouts/torii_gate.png')

lantern = clean_cutout(lantern_path, threshold=242)
lantern.save('assets/map/cutouts/lantern_post_glowing.png')

pagoda = clean_cutout(pagoda_path, threshold=240)
pagoda.save('assets/map/cutouts/pagoda_shrine.png')

house = clean_cutout(house_path, threshold=240)
house.save('assets/map/cutouts/japanese_shrine_house.png')

bamboo = clean_cutout(bamboo_path, threshold=240)
bamboo.save('assets/map/cutouts/bamboo_cluster.png')

boardwalk = clean_cutout(boardwalk_path, threshold=238)
boardwalk.save('assets/map/cutouts/wooden_boardwalk_platform.png')

print("All cutouts saved to assets/map/cutouts/")

# =========================================================================
# 1. BUILD tile_gate_v2.png (320 x 256)
# =========================================================================
# Super Dash uses a 320x256 image with 5 columns of 64px width
gate_canvas = Image.new('RGBA', (320, 256), (0, 0, 0, 0))
# Scale torii to fit 320x256 with margin
torii_aspect = torii.width / torii.height
gate_h = 248
gate_w = int(gate_h * torii_aspect)
if gate_w > 316:
    gate_w = 316
    gate_h = int(gate_w / torii_aspect)
torii_scaled = torii.resize((gate_w, gate_h), Image.Resampling.LANCZOS)
x_pos = (320 - gate_w) // 2
y_pos = 256 - gate_h
gate_canvas.paste(torii_scaled, (x_pos, y_pos), torii_scaled)
gate_canvas.save('assets/map/tiles/tile_gate_v2.png')
print("Updated assets/map/tiles/tile_gate_v2.png (320x256)")

# =========================================================================
# 2. BUILD tile_forest_trees_front_v02.png (588 x 324)
# =========================================================================
# 3 columns of 192 x 320 with 4px spacing
# Col 0: Pagoda Shrine (0..192)
# Col 1: Japanese Shrine House (196..388)
# Col 2: Bamboo Cluster (392..584)
trees_canvas = Image.new('RGBA', (588, 324), (0, 0, 0, 0))

def fit_in_box(img, max_w, max_h):
    aspect = img.width / img.height
    w = max_w
    h = int(w / aspect)
    if h > max_h:
        h = max_h
        w = int(h * aspect)
    return img.resize((w, h), Image.Resampling.LANCZOS)

# Col 0: Pagoda
pagoda_fit = fit_in_box(pagoda, 188, 318)
trees_canvas.paste(pagoda_fit, (2 + (188 - pagoda_fit.width)//2, 324 - pagoda_fit.height), pagoda_fit)

# Col 1: House
house_fit = fit_in_box(house, 188, 318)
trees_canvas.paste(house_fit, (196 + (188 - house_fit.width)//2, 324 - house_fit.height), house_fit)

# Col 2: Bamboo
bamboo_fit = fit_in_box(bamboo, 188, 318)
trees_canvas.paste(bamboo_fit, (392 + (188 - bamboo_fit.width)//2, 324 - bamboo_fit.height), bamboo_fit)

trees_canvas.save('assets/map/objects/tile_forest_trees_front_v02.png')
print("Updated assets/map/objects/tile_forest_trees_front_v02.png (588x324)")

# =========================================================================
# 3. BUILD tile_decorations_v01.png (660 x 204)
# =========================================================================
# 5 columns x 3 rows. Cell size: 128 x 64 with 4px spacing
# Row 0: Lanterns and props
# Row 1: Bamboo shoots / grass
# Row 2: Stone / pebbles
decor_canvas = Image.new('RGBA', (660, 204), (0, 0, 0, 0))

# Place glowing lanterns into decoration slots
lantern_cell = fit_in_box(lantern, 54, 60)
# Cell (0, 0): x=36, y=2
decor_canvas.paste(lantern_cell, (36, 64 - lantern_cell.height), lantern_cell)

# Cell (1, 0): x=168, y=2 (bamboo shoot)
bamboo_shoot = fit_in_box(bamboo, 60, 60)
decor_canvas.paste(bamboo_shoot, (168, 64 - bamboo_shoot.height), bamboo_shoot)

# Cell (2, 0): x=300 (second lantern variation)
decor_canvas.paste(lantern_cell, (300, 64 - lantern_cell.height), lantern_cell)

# Small bamboo sprigs in row 1
bamboo_small = fit_in_box(bamboo, 40, 48)
decor_canvas.paste(bamboo_small, (36, 68 + 64 - bamboo_small.height), bamboo_small)
decor_canvas.paste(bamboo_small, (168, 68 + 64 - bamboo_small.height), bamboo_small)
decor_canvas.paste(bamboo_small, (300, 68 + 64 - bamboo_small.height), bamboo_small)
decor_canvas.paste(bamboo_small, (432, 68 + 64 - bamboo_small.height), bamboo_small)

# Torii miniature prop in cell (4, 0)
torii_prop = fit_in_box(torii, 80, 60)
decor_canvas.paste(torii_prop, (554, 64 - torii_prop.height), torii_prop)

# Keep or blend original stone/pebble accents in row 2
orig_decor = Image.open('assets/map/tiles/tile_decorations_v01.png').convert('RGBA')
orig_row2 = orig_decor.crop((0, 136, 660, 204))
decor_canvas.paste(orig_row2, (0, 136), orig_row2)

decor_canvas.save('assets/map/tiles/tile_decorations_v01.png')
print("Updated assets/map/tiles/tile_decorations_v01.png (660x204)")

# =========================================================================
# 4. BUILD tile_forest_ground_v04.png (748 x 816) - WOODEN BOARDWALK
# =========================================================================
# We re-skin the ground tileset with wooden boardwalk textures:
# The top walking surfaces become dark cedar wooden planks with plank grain and seams.
# The body becomes sturdy charred cedar timber framing and stone pillars.
orig_ground = Image.open('assets/map/tiles/tile_forest_ground_v04.png').convert('RGBA')
g_arr = np.array(orig_ground)
orig_alpha = g_arr[:, :, 3]

# Create a rich wooden boardwalk texture
# Sample cedar colors:
# Highlight top wood: RGB(190, 120, 60)
# Mid wood plank: RGB(120, 65, 30)
# Dark wood grain / gaps: RGB(50, 25, 12)
# Shadow timber: RGB(35, 18, 10)
# Stone footing: RGB(70, 75, 80)

wood_sheet = np.zeros_like(g_arr)
h_g, w_g = orig_alpha.shape

# Generate procedural cedar plank horizontal pattern with vertical plank seams every 24px
y_coords, x_coords = np.indices((h_g, w_g))
# Plank vertical seams every 28px
is_seam = (x_coords % 28 == 0) | (x_coords % 28 == 1)

# Platform top edge detector (first 14px of any platform surface)
# We can find top surfaces by looking at original brightness and alpha
is_top_surface = (g_arr[:, :, 0] > 60) & (g_arr[:, :, 1] > 100) & (orig_alpha > 128)

# Wood tone:
# Base timber
wood_r = np.full((h_g, w_g), 68, dtype=np.uint8)
wood_g = np.full((h_g, w_g), 38, dtype=np.uint8)
wood_b = np.full((h_g, w_g), 22, dtype=np.uint8)

# Add wood grain noise
grain = ((x_coords * 3 + y_coords * 7) % 17).astype(np.uint8)
wood_r += grain
wood_g += (grain // 2)

# Top surface is warm glowing polished cedar planks
wood_r[is_top_surface] = 168 + (grain[is_top_surface] // 2)
wood_g[is_top_surface] = 98 + (grain[is_top_surface] // 3)
wood_b[is_top_surface] = 48

# Plank seams are dark charred cedar
wood_r[is_seam & (orig_alpha > 0)] = 32
wood_g[is_seam & (orig_alpha > 0)] = 18
wood_b[is_seam & (orig_alpha > 0)] = 10

# Bottom footing / foundation: if y in tile is near bottom of non-empty region
wood_sheet[:, :, 0] = wood_r
wood_sheet[:, :, 1] = wood_g
wood_sheet[:, :, 2] = wood_b
wood_sheet[:, :, 3] = orig_alpha

boardwalk_tileset = Image.fromarray(wood_sheet, mode='RGBA')
boardwalk_tileset.save('assets/map/tiles/tile_forest_ground_v04.png')
print("Updated assets/map/tiles/tile_forest_ground_v04.png (748x816)")

print("Successfully replaced Super Dash tilemap assets with Shinobi Sprint East Asian theme!")
