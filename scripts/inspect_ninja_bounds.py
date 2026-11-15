from PIL import Image
import numpy as np

ninja = Image.open('assets/images/spritesheet_ninja_run.png')
print("Ninja run spritesheet size:", ninja.size)
# 6 frames horizontally
w_frame = ninja.width // 6
h_frame = ninja.height
print(f"Each frame: {w_frame}x{h_frame}")

for f in range(6):
    crop = ninja.crop((f * w_frame, 0, (f + 1) * w_frame, h_frame))
    bbox = crop.getbbox()
    print(f"Frame {f} content bbox: {bbox}")
