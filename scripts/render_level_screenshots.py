import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

base_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix"
images_dir = os.path.join(base_dir, "assets", "images")
artifact_dir = r"C:\Users\User\.gemini\antigravity\brain\7fa3f8e5-8048-4e68-83e9-9dd5e4846bee"
os.makedirs(artifact_dir, exist_ok=True)

# Load helper sprites
orb_img = Image.open(os.path.join(images_dir, "prop_spirit_orb_clean.png")).convert("RGBA")
orb_img = orb_img.resize((32, 32), Image.Resampling.LANCZOS)

# Create a glowing orb with aura
glow_orb = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_orb)
glow_draw.ellipse([4, 4, 44, 44], fill=(255, 215, 0, 80))
glow_draw.ellipse([8, 8, 40, 40], fill=(255, 230, 100, 140))
glow_orb = glow_orb.filter(ImageFilter.GaussianBlur(3))
glow_orb.paste(orb_img, (8, 8), orb_img)

# Ninja animation frames
ninja_run_sheet = Image.open(os.path.join(images_dir, "spritesheet_ninja_run.png")).convert("RGBA")
# Frame 1: (128, 0, 256, 128)
ninja_run_frame = ninja_run_sheet.crop((128, 0, 256, 128)).resize((64, 64), Image.Resampling.LANCZOS)

ninja_jump_sheet = Image.open(os.path.join(images_dir, "spritesheet_ninja_jump.png")).convert("RGBA")
# Frame 2: (256, 0, 384, 128)
ninja_jump_frame = ninja_jump_sheet.crop((256, 0, 384, 128)).resize((64, 64), Image.Resampling.LANCZOS)

ninja_attack_sheet = Image.open(os.path.join(images_dir, "spritesheet_ninja_attack.png")).convert("RGBA")
# Frame 2: (256, 0, 384, 128)
ninja_attack_frame = ninja_attack_sheet.crop((256, 0, 384, 128)).resize((68, 68), Image.Resampling.LANCZOS)

ninja_idle_sheet = Image.open(os.path.join(images_dir, "spritesheet_ninja_idle.png")).convert("RGBA")
ninja_idle_frame = ninja_idle_sheet.crop((0, 0, 128, 128)).resize((64, 64), Image.Resampling.LANCZOS)

# Foes
foe_dark = Image.open(os.path.join(images_dir, "foes", "ninja_dark.png")).convert("RGBA").resize((48, 70), Image.Resampling.LANCZOS)
foe_purple = Image.open(os.path.join(images_dir, "foes", "ninja_purple.png")).convert("RGBA").resize((52, 70), Image.Resampling.LANCZOS)
foe_brown = Image.open(os.path.join(images_dir, "foes", "ninja_brown.png")).convert("RGBA").resize((48, 70), Image.Resampling.LANCZOS)
foe_ghostly = Image.open(os.path.join(images_dir, "foes", "ninja_ghostly.png")).convert("RGBA").resize((48, 70), Image.Resampling.LANCZOS)

levels = [
    {
        "id": "level1_daytime_torii_shrine",
        "title": "STAGE 1: DAYTIME TORII SHRINE & BAMBOO GROVE",
        "subtitle": "Morning Sun & Mountain Pagoda Path",
        "stage_plate": "stage1_daytime_torii_shrine_1024.png",
        "player": {
            "sprite": ninja_run_frame,
            "pos": (310, 315)  # On the cobblestone mountain path
        },
        "foes": [
            {"sprite": foe_purple, "pos": (905, 105)}, # Top pagoda guard
            {"sprite": foe_brown, "pos": (160, 220)},   # Left temple veranda
        ],
        "orbs": [(70, 220), (230, 290), (340, 310), (520, 290), (795, 240), (960, 100)],
        "orbs_collected": 3,
        "score": "12,500"
    },
    {
        "id": "level2_twilight_sanctuary",
        "title": "STAGE 2: TWILIGHT BAMBOO SANCTUARY",
        "subtitle": "Golden Sunset & Grand Vermilion Torii Gate",
        "stage_plate": "level2_cinematic_stage_1024.png",
        "player": {
            "sprite": ninja_jump_frame,
            "pos": (270, 440)  # Mid-air leap across rope bridge
        },
        "foes": [
            {"sprite": foe_dark, "pos": (920, 375)},  # High eastern cliff under Torii
            {"sprite": foe_purple, "pos": (500, 440)}, # Center Torii shrine island
        ],
        "orbs": [(270, 160), (300, 465), (455, 440), (512, 435), (570, 440), (720, 465), (770, 160), (950, 375)],
        "orbs_collected": 5,
        "score": "24,800"
    },
    {
        "id": "level3_midnight_autumn_maple",
        "title": "STAGE 3: MIDNIGHT AUTUMN MAPLE FOREST",
        "subtitle": "Crescent Moon & Arched Pagoda River Bridge",
        "stage_plate": "level3_cinematic_stage_1024.png",
        "player": {
            "sprite": ninja_run_frame,
            "pos": (440, 345)  # Running across apex of arched wooden footbridge
        },
        "foes": [
            {"sprite": foe_ghostly, "pos": (780, 365)}, # Kitsune stone fox statue pagoda
            {"sprite": foe_dark, "pos": (140, 370)},    # Western approach cliff
        ],
        "orbs": [(210, 370), (440, 335), (580, 340), (830, 370)],
        "orbs_collected": 2,
        "score": "38,200"
    },
    {
        "id": "level4_night_waterfall_gorge",
        "title": "STAGE 4: NIGHTTIME WATERFALL GORGE",
        "subtitle": "Rushing Torrent & Suspended Catenary Bridges",
        "stage_plate": "level2_night_waterfall_stage_1024.png",
        "player": {
            "sprite": ninja_attack_frame,
            "pos": (470, 295)  # Katana air strike on center stone pier
        },
        "foes": [
            {"sprite": foe_dark, "pos": (850, 325)},    # Right cliff terrace
            {"sprite": foe_brown, "pos": (140, 300)},   # Left lookout terrace
        ],
        "orbs": [(140, 310), (335, 335), (480, 310), (640, 350), (840, 340)],
        "orbs_collected": 4,
        "score": "51,600"
    }
]

def draw_hud(draw, width, height, title, subtitle, score, orbs_collected, total_orbs):
    # Top HUD banner overlay
    banner_height = 58
    overlay = Image.new("RGBA", (width, banner_height), (12, 16, 26, 210))
    # Draw soft decorative border line
    draw_overlay = ImageDraw.Draw(overlay)
    draw_overlay.line([(0, banner_height - 1), (width, banner_height - 1)], fill=(218, 165, 32, 180), width=2)
    
    # We will paste overlay onto canvas in main routine

created_files = []

for lvl in levels:
    plate_path = os.path.join(images_dir, lvl["stage_plate"])
    stage_img = Image.open(plate_path).convert("RGBA")
    w, h = stage_img.size
    if (w, h) != (1024, 576):
        stage_img = stage_img.resize((1024, 576), Image.Resampling.LANCZOS)
    
    canvas = stage_img.copy()
    
    # 1. Place Soul Orbs
    for ox, oy in lvl["orbs"]:
        # center glow orb
        canvas.paste(glow_orb, (int(ox - 24), int(oy - 24)), glow_orb)

    # 1b. Render Water Effects (River Foam & Waterfall Mist) if level has water
    if "level3" in lvl["id"]:
        # River Foam Ripples & Froth
        water_layer = Image.new("RGBA", (1024, 576), (0, 0, 0, 0))
        wdraw = ImageDraw.Draw(water_layer)
        # Expanding concentric ripple crests and foam froth
        import random
        random.seed(42)
        for _ in range(22):
            rx = random.uniform(280, 740)
            ry = random.uniform(520, 560)
            rw = random.uniform(20, 55)
            rh = random.uniform(5, 11)
            alpha = int(random.uniform(70, 160))
            if random.random() < 0.5:
                # frothy foam cluster
                wdraw.ellipse([rx - rw/2, ry - rh/2, rx + rw/2, ry + rh/2], fill=(224, 247, 250, alpha))
            else:
                # concentric ripple ring
                wdraw.ellipse([rx - rw/2, ry - rh/2, rx + rw/2, ry + rh/2], outline=(200, 240, 255, alpha), width=2)
        
        # Rising gorge mist clouds
        for _ in range(16):
            mx = random.uniform(280, 740)
            my = random.uniform(480, 550)
            mr = random.uniform(20, 45)
            m_alpha = int(random.uniform(25, 65))
            wdraw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(130, 180, 255, m_alpha))
            
        water_layer = water_layer.filter(ImageFilter.GaussianBlur(2))
        canvas.paste(water_layer, (0, 0), water_layer)

    elif "level4" in lvl["id"]:
        # Waterfall Gorge Mist & River Rapids Foam
        water_layer = Image.new("RGBA", (1024, 576), (0, 0, 0, 0))
        wdraw = ImageDraw.Draw(water_layer)
        import random
        random.seed(108)
        # Dense rapids foam froth
        for _ in range(30):
            rx = random.uniform(225, 755)
            ry = random.uniform(500, 565)
            rw = random.uniform(25, 65)
            rh = random.uniform(6, 14)
            alpha = int(random.uniform(90, 190))
            if random.random() < 0.55:
                wdraw.ellipse([rx - rw/2, ry - rh/2, rx + rw/2, ry + rh/2], fill=(240, 255, 255, alpha))
            else:
                wdraw.ellipse([rx - rw/2, ry - rh/2, rx + rw/2, ry + rh/2], outline=(220, 250, 255, alpha), width=2)
        
        # Dense billowing waterfall spray mist
        for _ in range(22):
            mx = random.uniform(220, 750)
            my = random.uniform(450, 555)
            mr = random.uniform(25, 55)
            m_alpha = int(random.uniform(35, 80))
            wdraw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(180, 230, 255, m_alpha))
            
        water_layer = water_layer.filter(ImageFilter.GaussianBlur(3))
        canvas.paste(water_layer, (0, 0), water_layer)
    
    # 2. Place Foes
    for foe in lvl["foes"]:
        fs = foe["sprite"]
        fx, fy = foe["pos"]
        # Add slight shadow under foe
        shadow = Image.new("RGBA", (fs.width, 14), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(shadow)
        sdraw.ellipse([4, 2, fs.width - 4, 12], fill=(0, 0, 0, 130))
        shadow = shadow.filter(ImageFilter.GaussianBlur(2))
        canvas.paste(shadow, (int(fx), int(fy + fs.height - 8)), shadow)
        canvas.paste(fs, (int(fx), int(fy)), fs)
    
    # 3. Place Player
    ps = lvl["player"]["sprite"]
    px, py = lvl["player"]["pos"]
    # Shadow under player
    pshadow = Image.new("RGBA", (ps.width, 16), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(pshadow)
    pdraw.ellipse([8, 2, ps.width - 8, 14], fill=(0, 0, 0, 160))
    pshadow = pshadow.filter(ImageFilter.GaussianBlur(3))
    canvas.paste(pshadow, (int(px), int(py + ps.height - 10)), pshadow)
    canvas.paste(ps, (int(px), int(py)), ps)
    
    # 4. Composite HUD Overlay
    hud = Image.new("RGBA", (1024, 64), (10, 14, 24, 215))
    hdraw = ImageDraw.Draw(hud)
    # Golden divider line
    hdraw.line([(0, 63), (1024, 63)], fill=(218, 165, 32, 220), width=2)
    hdraw.line([(0, 61), (1024, 61)], fill=(255, 235, 140, 100), width=1)
    
    # Texts
    # Title
    hdraw.text((24, 10), lvl["title"], fill=(255, 255, 255))
    hdraw.text((24, 34), lvl["subtitle"].upper(), fill=(200, 180, 140))
    
    # Stats (Orbs & Score)
    hdraw.text((700, 12), f"SOUL ORBS: {lvl['orbs_collected']} / {len(lvl['orbs'])}", fill=(255, 215, 0))
    hdraw.text((700, 34), f"SCORE: {lvl['score']}", fill=(240, 240, 240))
    
    # Health hearts indicator
    hdraw.text((900, 12), "[HP: ♥♥♥♥]", fill=(255, 80, 80))
    hdraw.text((900, 34), "STAGE ACTIVE", fill=(100, 230, 130))
    
    canvas.paste(hud, (0, 0), hud)
    
    # Save to artifact dir
    out_path = os.path.join(artifact_dir, f"{lvl['id']}_screenshot.png")
    canvas.save(out_path, format="PNG")
    created_files.append(out_path)
    print(f"Generated: {out_path}")

print("All screenshots generated successfully!")
