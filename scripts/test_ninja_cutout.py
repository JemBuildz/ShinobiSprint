import os
from PIL import Image
import numpy as np
from collections import deque

user_uploaded_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b\.user_uploaded"
ninja_path = os.path.join(user_uploaded_dir, "media_1791004147591.jpg")

im = Image.open(ninja_path).convert("RGBA")
arr = np.array(im)
h, w, _ = arr.shape

# Let's inspect the corner pixels to see checkerboard values
corners = [arr[0, 0, :3], arr[0, 20, :3], arr[0, 40, :3], arr[10, 10, :3]]
print("Sample background colors near top-left:", corners)

# The checkerboard consists of two shades of grey: e.g. white (~255 or ~204) and grey (~153 or ~178)
# Notice the background is purely achromatic (R ~ G ~ B) and light/mid grey, whereas the ninja has colored clothes (dark blue) or skin (warm tones) or black outlines.
# Let's check flood fill from border pixels:
# A pixel is background if it is connected to the border and its color is typical checkerboard (e.g. diff between R,G,B < 15 and either light ~200+ or mid ~150-180, or simply any flood fill that doesn't cross the black outline).
# Let's check min pixel intensity of ninja's outline: it's dark black (R<50, G<50, B<50).
# Flood fill from all 4 borders:
visited = np.zeros((h, w), dtype=bool)
q = deque()

# Add all border pixels to queue if they look like checkerboard
for y in range(h):
    for x in [0, w-1]:
        q.append((y, x))
        visited[y, x] = True
for x in range(w):
    for y in [0, h-1]:
        if not visited[y, x]:
            q.append((y, x))
            visited[y, x] = True

# Checkerboard is achromatic: |r-g| < 18, |g-b| < 18, |r-b| < 18, and brightness > 120
def is_bg(r, g, b):
    # Acheomatic check
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    if (max_c - min_c) <= 25 and min_c >= 110:
        return True
    return False

bg_mask = np.zeros((h, w), dtype=bool)

while q:
    y, x = q.popleft()
    r, g, b = arr[y, x, :3]
    if is_bg(r, g, b):
        bg_mask[y, x] = True
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))

print(f"Total background pixels found: {np.sum(bg_mask)} out of {h*w} ({np.sum(bg_mask)/(h*w)*100:.1f}%)")

# Apply alpha
arr[bg_mask, 3] = 0

# Crop to bounding box of non-transparent pixels
non_bg = np.where(~bg_mask)
ymin, ymax = np.min(non_bg[0]), np.max(non_bg[0])
xmin, xmax = np.min(non_bg[1]), np.max(non_bg[1])
print(f"Ninja bounds: y=[{ymin}, {ymax}], x=[{xmin}, {xmax}], size=({xmax-xmin}, {ymax-ymin})")

out_im = Image.fromarray(arr).crop((xmin, ymin, xmax+1, ymax+1))
out_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "character_ninja.png")
out_im.save(out_path)
print("Saved character_ninja.png:", out_path, "Size:", out_im.size)
