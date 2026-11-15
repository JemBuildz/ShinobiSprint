import os
import glob
import numpy as np
from PIL import Image, ImageFilter

os.makedirs('assets/map/cutouts', exist_ok=True)

# Find the generated images in artifact directory
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

print("Found assets:")
print("Torii:", torii_path)
print("Lantern:", lantern_path)
print("Pagoda:", pagoda_path)
print("Boardwalk:", boardwalk_path)

def make_transparent_from_white(img_path, threshold=240, feather=0.7):
    """Converts a sprite on white background to a clean transparent RGBA PNG."""
    im = Image.open(img_path).convert('RGB')
    arr = np.array(im, dtype=float)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    
    # White background condition: all RGB channels very high and color is neutral
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    spread = max_c - min_c
    
    # Background is white or near-white with low saturation
    is_white = (min_c > threshold) & (spread < 20)
    
    # Generate alpha: 255 for sprite, 0 for white bg
    alpha = np.ones(r.shape, dtype=float) * 255.0
    alpha[is_white] = 0.0
    
    # Smooth transition for anti-aliasing near edges (220..250)
    edge_zone = (min_c >= 220) & (min_c <= 254) & (~is_white)
    if np.any(edge_zone):
        fade = (255.0 - min_c[edge_zone]) / 35.0
        alpha[edge_zone] = np.clip(fade * 255.0, 0, 255)
        
    alpha_img = Image.fromarray(alpha.astype(np.uint8), mode='L')
    if feather > 0:
        alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(feather))
        
    # Crop to bounding box of content
    rgba = Image.new('RGBA', im.size, (0, 0, 0, 0))
    rgba.paste(im, (0, 0), alpha_img)
    
    # Auto crop excess transparent border
    bbox = rgba.getbbox()
    if bbox:
        # Add 4px margin
        m = 4
        bbox = (max(0, bbox[0]-m), max(0, bbox[1]-m), min(rgba.width, bbox[2]+m), min(rgba.height, bbox[3]+m))
        rgba = rgba.crop(bbox)
        
    return rgba

# Process and save isolated cutouts
torii_clean = make_transparent_from_white(torii_path, threshold=242)
torii_clean.save('assets/map/cutouts/torii_gate_clean.png')
print("Saved assets/map/cutouts/torii_gate_clean.png", torii_clean.size)

lantern_clean = make_transparent_from_white(lantern_path, threshold=242)
lantern_clean.save('assets/map/cutouts/lantern_post_clean.png')
print("Saved assets/map/cutouts/lantern_post_clean.png", lantern_clean.size)

pagoda_clean = make_transparent_from_white(pagoda_path, threshold=240)
pagoda_clean.save('assets/map/cutouts/pagoda_shrine_clean.png')
print("Saved assets/map/cutouts/pagoda_shrine_clean.png", pagoda_clean.size)

boardwalk_clean = make_transparent_from_white(boardwalk_path, threshold=238)
boardwalk_clean.save('assets/map/cutouts/wooden_boardwalk_clean.png')
print("Saved assets/map/cutouts/wooden_boardwalk_clean.png", boardwalk_clean.size)
