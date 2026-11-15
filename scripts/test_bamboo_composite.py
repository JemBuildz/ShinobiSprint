from PIL import Image

# Load base 1024x576 cinematic plate
base = Image.open('assets/images/level1_cinematic_stage_1024.png').convert('RGBA')

# 1. Lower Bridge across the chasm at ground level
# Gap is x=420..580 (width ~160px) at y=490
bridge = Image.open('assets/images/prop_log_bridge.png').convert('RGBA')
bridge_scaled = bridge.resize((175, 45), Image.Resampling.LANCZOS)
base.alpha_composite(bridge_scaled, (415, 485))

# 2. Elevated Bamboo Table Platform
# Elevated route at x=430..570, y=340
platform = Image.open('assets/images/prop_bamboo_platform.png').convert('RGBA')
plat_scaled = platform.resize((160, 50), Image.Resampling.LANCZOS)
base.alpha_composite(plat_scaled, (420, 340))

# 3. Stepping Stone Pillar on Left of Gap
pillar = Image.open('assets/images/prop_stone_pillar.png').convert('RGBA')
pillar_scaled = pillar.resize((45, 90), Image.Resampling.LANCZOS)
base.alpha_composite(pillar_scaled, (320, 410))

# 4. Stepping Stone Pillar on Right of Gap
base.alpha_composite(pillar_scaled, (620, 410))

# 5. Blue Chibi Ninja Player leaping
ninja = Image.open('assets/images/character_ninja.png').convert('RGBA')
ninja_scaled = ninja.resize((56, 54), Image.Resampling.LANCZOS)
base.alpha_composite(ninja_scaled, (470, 290))

# 6. Golden Spirit Orbs
orb = Image.open('assets/images/prop_spirit_orb_clean.png').convert('RGBA')
orb_scaled = orb.resize((32, 32), Image.Resampling.LANCZOS)
base.alpha_composite(orb_scaled, (150, 180)) # on left hut roof
base.alpha_composite(orb_scaled, (340, 360)) # over left pillar
base.alpha_composite(orb_scaled, (500, 270)) # high above center platform
base.alpha_composite(orb_scaled, (640, 360)) # over right pillar
base.alpha_composite(orb_scaled, (930, 280)) # on right cliff

out_p = r'C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b/bamboo_cinematic_composite.png'
base.save(out_p)
print(f"Saved bamboo composite to {out_p}")
