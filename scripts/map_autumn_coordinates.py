from PIL import Image
import os

src_path = 'assets/autumn_maple/autumn_panoramic_clean_night.png'
im = Image.open(src_path)
print(f"Original size: {im.size}")

# Resize to standard game resolution 1024x576
im_1024 = im.resize((1024, 576), Image.Resampling.LANCZOS)
out_path = 'assets/images/level3_cinematic_stage_1024.png'
im_1024.save(out_path)
print(f"Saved {out_path} (1024x576)")

# Also copy to artifacts directory
art_dir = r'C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b'
im_1024.save(os.path.join(art_dir, 'level3_cinematic_stage_1024.png'))
print("Copied to artifacts")
