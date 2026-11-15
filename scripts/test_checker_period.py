import os
from PIL import Image
import numpy as np

user_uploaded_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b\.user_uploaded"
images_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"
out_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b"

p = os.path.join(user_uploaded_dir, "media_1791006019634.png")
im = Image.open(p).convert("RGBA")
arr = np.array(im)
h, w, _ = arr.shape

# Let's inspect the checkerboard:
# In checkerboard, adjacent 16x16 blocks have massive difference in brightness:
# One block is dark (brightness ~6), one block is light (brightness ~55).
# So the difference between a pixel and 16px to its right is ~50!
# Whereas inside the mountains and mist, brightness is smooth!
# Let's compute local 16-pixel horizontal difference:
r, g, b = arr[:, :, 0].astype(float), arr[:, :, 1].astype(float), arr[:, :, 2].astype(float)
lum = 0.299 * r + 0.587 * g + 0.114 * b

# In the checkerboard area, lum fluctuates wildly every 16 pixels.
# Let's find the mountain boundary by detecting where the 16-pixel fluctuation stops!
diff16 = np.abs(lum[:, 16:] - lum[:, :-16])

# For each column x, find the lowest row y where diff16 is high (> 20)
# Below that row, it's 100% mountains!
mountain_top = np.zeros(w, dtype=int)
for x in range(w):
    # Check column x: find the last y from top to bottom where diff16 is > 18
    # Looking in x clamped to valid range
    cx = min(max(0, x - 8), diff16.shape[1] - 1)
    last_checker_y = 0
    for y in range(0, h):
        if diff16[y, cx] > 18:
            last_checker_y = y
    mountain_top[x] = min(h - 1, last_checker_y + 12)

print("Detected mountain top per column: min=", np.min(mountain_top), "max=", np.max(mountain_top), "median=", np.median(mountain_top))

# Create clean image:
clean_arr = arr.copy()
for x in range(w):
    clean_arr[:mountain_top[x], x, 3] = 0
    clean_arr[mountain_top[x]:, x, 3] = 255

clean_m = Image.fromarray(clean_arr)
clean_m.save(os.path.join(images_dir, "level2_layer2_distant_mountains.png"))
clean_m.save(os.path.join(out_dir, "isolated_mountains.png"))
print("Saved isolated_mountains.png!")
