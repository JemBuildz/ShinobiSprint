import os
import numpy as np
from PIL import Image

os.makedirs('assets/map/cutouts', exist_ok=True)
concept = Image.open('assets/concept_art.jpg').convert('RGB')
w_total, h_total = concept.size

# Coordinates in concept_art.jpg (1024x765):
# 1. Torii Gate (Vermilion Day):
# The red Torii gate in row 3 daytime: x: 280..380, y: 350..460
# 2. Torii Gate (Night):
# Row 3 nighttime: x: 790..890, y: 350..460
# 3. Pagoda Shrine (Day):
# Row 3 daytime left: x: 140..220, y: 350..460
# 4. Japanese House (Day):
# Row 4 daytime right: x: 400..510, y: 470..590
# 5. Glowing Lantern Post (Day & Night):
# Row 4 day lantern: x: 180..245, y: 480..590
# Row 4 night lantern: x: 690..760, y: 480..590
# Row 5 night lantern: x: 800..880, y: 605..720
# 6. Wooden Boardwalk Bridge / Planks:
# Row 5 day bridge: x: 310..470, y: 650..745
# Row 5 night bridge: x: 730..880, y: 655..745

print("Concept dimensions:", w_total, h_total)
