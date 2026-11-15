import os
from PIL import Image
import numpy as np

user_uploaded_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b\.user_uploaded"
p = os.path.join(user_uploaded_dir, "media_1791006019634.png")
im = Image.open(p)
print("Mode:", im.mode, "Size:", im.size)
arr = np.array(im)
if arr.shape[2] == 4:
    print("Min alpha:", np.min(arr[:, :, 3]), "Max alpha:", np.max(arr[:, :, 3]))
    print("Does it already have alpha?", np.any(arr[:, :, 3] < 255))
