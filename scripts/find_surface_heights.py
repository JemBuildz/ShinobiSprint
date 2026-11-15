from PIL import Image, ImageDraw

im = Image.open('assets/images/level3_cinematic_stage_1024.png').convert('RGBA')
draw = ImageDraw.Draw(im)

# Let's map candidate collision surfaces on 1024x576:
# 1. Left upper stone ledge
# x: 0..120, y: 298
draw.line([(0, 298), (120, 298)], fill=(0, 255, 255, 255), width=3)

# 2. Sloped plank ramp down to bank
# from (120, 310) to (310, 420)
draw.line([(120, 310), (310, 420)], fill=(0, 255, 128, 255), width=3)

# 3. Left bank grass floor
# x: 0..310, y: 468
draw.line([(0, 468), (310, 468)], fill=(0, 255, 0, 255), width=3)

# 4. Left stone pier holding bridge
# x: 310..430, y: 375
draw.line([(310, 375), (430, 375)], fill=(255, 255, 0, 255), width=3)

# 5. Arched wooden bridge walkway (segmented arc)
# Incline up: (430, 375) -> (510, 335)
draw.line([(430, 375), (510, 335)], fill=(255, 128, 0, 255), width=3)
# Arch crest center: (510, 335) -> (680, 335)
draw.line([(510, 335), (680, 335)], fill=(255, 64, 0, 255), width=3)
# Decline down: (680, 335) -> (760, 375)
draw.line([(680, 335), (760, 375)], fill=(255, 128, 0, 255), width=3)

# 6. Right stone bank & shrine terrace
# x: 760..1024, y: 375
draw.line([(760, 375), (1024, 375)], fill=(255, 255, 0, 255), width=3)

# 7. Right lower grass bank
# x: 740..1024, y: 468
draw.line([(740, 468), (1024, 468)], fill=(0, 255, 0, 255), width=3)

test_out = r'C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b/autumn_mapped_surfaces.png'
im.save(test_out)
print(f"Saved test surface map to {test_out}")
