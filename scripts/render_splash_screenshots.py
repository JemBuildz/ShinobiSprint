import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

base_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix"
artifact_dir = r"C:\Users\User\.gemini\antigravity\brain\7fa3f8e5-8048-4e68-83e9-9dd5e4846bee"
os.makedirs(artifact_dir, exist_ok=True)

# 1. SCREENSHOT 1: Web Preload & Loading Splash Screen (1024 x 576)
def render_web_loading_splash():
    w, h = 1024, 576
    canvas = Image.new("RGBA", (w, h), (9, 13, 26, 255))
    
    # Background cover art
    cover_path = os.path.join(base_dir, "web", "ShinobiSprint_GameCover.png")
    if os.path.exists(cover_path):
        cover = Image.open(cover_path).convert("RGBA")
        cover = cover.resize((w, h), Image.Resampling.LANCZOS)
        canvas.paste(cover, (0, 0))
    
    # Dark cinematic scrim overlay
    scrim = Image.new("RGBA", (w, h), (9, 13, 26, 170))
    sdraw = ImageDraw.Draw(scrim)
    # Vignette gradients
    for y in range(80):
        alpha = int(220 * (1 - y / 80))
        sdraw.line([(0, y), (w, y)], fill=(9, 13, 26, alpha))
    for y in range(120):
        alpha = int(240 * (y / 120))
        sdraw.line([(0, h - 120 + y), (w, h - 120 + y)], fill=(9, 13, 26, alpha))
    canvas.paste(scrim, (0, 0), scrim)
    
    # Logo
    logo_path = os.path.join(base_dir, "assets", "images", "shinobi_sprint_logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_w = 460
        logo_h = int(logo.height * (logo_w / logo.width))
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        
        # Soft glow behind logo
        glow = Image.new("RGBA", (logo_w + 40, logo_h + 40), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)
        gdraw.ellipse([10, 10, logo_w + 30, logo_h + 30], fill=(251, 191, 36, 60))
        glow = glow.filter(ImageFilter.GaussianBlur(15))
        
        lx = (w - logo_w) // 2
        ly = (h - logo_h) // 2 - 40
        canvas.paste(glow, (lx - 20, ly - 20), glow)
        canvas.paste(logo, (lx, ly), logo)
    
    # Loading Progress Bar
    draw = ImageDraw.Draw(canvas)
    bar_w, bar_h = 380, 20
    bar_x = (w - bar_w) // 2
    bar_y = h - 90
    
    # Outer capsule border
    draw.rounded_rectangle([bar_x - 3, bar_y - 3, bar_x + bar_w + 3, bar_y + bar_h + 3], radius=12, fill=(9, 13, 26, 220), outline=(251, 191, 36, 180), width=2)
    # Fill progress (78%)
    prog_w = int(bar_w * 0.78)
    draw.rounded_rectangle([bar_x, bar_y, bar_x + prog_w, bar_y + bar_h], radius=10, fill=(16, 185, 129, 230))
    # Inner gold highlight
    draw.rounded_rectangle([bar_x + prog_w - 60, bar_y + 2, bar_x + prog_w - 2, bar_y + bar_h - 2], radius=8, fill=(251, 191, 36, 240))
    
    # Progress text
    text_label = "LOADING ASSETS & STAGES... 78%"
    draw.text(((w - len(text_label) * 8) // 2, bar_y - 28), text_label, fill=(251, 191, 36, 255))
    
    footer_text = "SHINOBI SPRINT - A 2D FEUDAL PLATFORMER BUILT WITH FLUTTER & FLAME"
    draw.text(((w - len(footer_text) * 6) // 2, h - 35), footer_text, fill=(180, 190, 210, 200))
    
    out_path = os.path.join(artifact_dir, "web_loading_splash_screenshot.png")
    canvas.save(out_path, format="PNG")
    print("Saved:", out_path)

# 2. SCREENSHOT 2: Mobile Portrait Sign-On Splash Screen (540 x 960)
def render_mobile_sign_on_splash():
    w, h = 540, 960
    canvas = Image.new("RGBA", (w, h), (13, 19, 34, 255))
    
    # Background artwork
    bg_path = os.path.join(base_dir, "assets", "images", "shinobi_sign_on_bg.png")
    if os.path.exists(bg_path):
        bg = Image.open(bg_path).convert("RGBA")
        bg = bg.resize((w, h), Image.Resampling.LANCZOS)
        canvas.paste(bg, (0, 0))
    
    # Cinematic Vignette overlays
    scrim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(scrim)
    # Top vignette
    for y in range(140):
        alpha = int(180 * (1 - y / 140))
        sdraw.line([(0, y), (w, y)], fill=(13, 19, 34, alpha))
    # Bottom dark tray scrim
    for y in range(320):
        alpha = int(245 * (y / 320))
        sdraw.line([(0, h - 320 + y), (w, h - 320 + y)], fill=(8, 14, 29, alpha))
    canvas.paste(scrim, (0, 0), scrim)
    
    # Sakura Petals
    random.seed(99)
    petal_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(petal_layer)
    for _ in range(24):
        px = random.uniform(20, w - 20)
        py = random.uniform(80, h - 80)
        pw = random.uniform(8, 14)
        ph = random.uniform(5, 9)
        palpha = int(random.uniform(90, 200))
        pdraw.ellipse([px - pw/2, py - ph/2, px + pw/2, py + ph/2], fill=(244, 114, 182, palpha))
    canvas.paste(petal_layer, (0, 0), petal_layer)
    
    # Logo
    logo_path = os.path.join(base_dir, "assets", "images", "shinobi_sprint_logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_w = 340
        logo_h = int(logo.height * (logo_w / logo.width))
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        lx = (w - logo_w) // 2
        ly = 130
        canvas.paste(logo, (lx, ly), logo)
    
    # Top Audio Button
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([w - 60, 40, w - 20, 80], radius=20, fill=(21, 27, 43, 200), outline=(255, 255, 255, 60), width=1)
    draw.text((w - 48, 52), "♫", fill=(255, 255, 255, 220))
    
    # Auth Buttons Tray
    btn_w, btn_h = 360, 48
    btn_x = (w - btn_w) // 2
    
    # Button 1: Google Sign In
    b1_y = h - 230
    draw.rounded_rectangle([btn_x, b1_y, btn_x + btn_w, b1_y + btn_h], radius=24, fill=(255, 255, 255, 255), outline=(220, 225, 235, 255), width=1)
    # Google text
    draw.text((btn_x + 95, b1_y + 14), "Sign in with Google", fill=(31, 41, 55, 255))
    draw.ellipse([btn_x + 60, b1_y + 14, btn_x + 80, b1_y + 34], fill=(66, 133, 244, 255))
    
    # Button 2: Apple Sign In
    b2_y = b1_y + 58
    draw.rounded_rectangle([btn_x, b2_y, btn_x + btn_w, b2_y + btn_h], radius=24, fill=(255, 255, 255, 255), outline=(220, 225, 235, 255), width=1)
    draw.text((btn_x + 98, b2_y + 14), "Sign in with Apple", fill=(31, 41, 55, 255))
    draw.ellipse([btn_x + 62, b2_y + 14, btn_x + 82, b2_y + 34], fill=(0, 0, 0, 255))
    
    # Button 3: Quick Guest Play
    b3_y = b2_y + 56
    guest_w = 170
    guest_x = (w - guest_w) // 2
    draw.rounded_rectangle([guest_x, b3_y, guest_x + guest_w, b3_y + 34], radius=17, fill=(36, 42, 58, 180), outline=(78, 222, 163, 140), width=1)
    draw.text((guest_x + 22, b3_y + 9), "PLAY AS GUEST  ➜", fill=(78, 222, 163, 255))
    
    out_path = os.path.join(artifact_dir, "mobile_sign_on_splash_screenshot.png")
    canvas.save(out_path, format="PNG")
    print("Saved:", out_path)

# 3. SCREENSHOT 3: Landscape Main Menu & Sign-On Screen (1024 x 576)
def render_landscape_sign_on_splash():
    w, h = 1024, 576
    canvas = Image.new("RGBA", (w, h), (13, 19, 34, 255))
    
    # Background artwork
    bg_path = os.path.join(base_dir, "assets", "images", "shinobi_sign_on_bg.png")
    if os.path.exists(bg_path):
        bg = Image.open(bg_path).convert("RGBA")
        # Center crop landscape
        target_w = 1024
        target_h = int(bg.height * (target_w / bg.width))
        bg = bg.resize((target_w, target_h), Image.Resampling.LANCZOS)
        # Crop middle vertical
        crop_y = (target_h - 576) // 2
        bg = bg.crop((0, crop_y, 1024, crop_y + 576))
        canvas.paste(bg, (0, 0))
        
    # Split Scrim: Darkened right panel for auth & menu
    scrim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(scrim)
    for x in range(480):
        alpha = int(240 * (x / 480))
        sdraw.line([(544 + x, 0), (544 + x, h)], fill=(8, 14, 29, alpha))
    canvas.paste(scrim, (0, 0), scrim)
    
    # Sakura Petals
    random.seed(55)
    petal_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(petal_layer)
    for _ in range(30):
        px = random.uniform(20, w - 20)
        py = random.uniform(20, h - 20)
        pw = random.uniform(8, 13)
        ph = random.uniform(5, 8)
        palpha = int(random.uniform(80, 180))
        pdraw.ellipse([px - pw/2, py - ph/2, px + pw/2, py + ph/2], fill=(244, 114, 182, palpha))
    canvas.paste(petal_layer, (0, 0), petal_layer)
    
    # Left Side: Giant Logo
    logo_path = os.path.join(base_dir, "assets", "images", "shinobi_sprint_logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_w = 460
        logo_h = int(logo.height * (logo_w / logo.width))
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        canvas.paste(logo, (50, 140), logo)
    
    draw = ImageDraw.Draw(canvas)
    draw.text((65, 340), "THE FEUDAL 2D ACTION PLATFORMER", fill=(251, 191, 36, 255))
    draw.text((65, 370), "Master the katana, sprint through cherry blossoms, and leap across sacred shrines.", fill=(187, 202, 191, 220))
    
    # Right Side: Card Menu Panel
    panel_x = 580
    panel_y = 70
    panel_w = 390
    panel_h = 440
    draw.rounded_rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], radius=24, fill=(21, 27, 43, 230), outline=(78, 222, 163, 100), width=2)
    
    # Card Header
    draw.text((panel_x + 30, panel_y + 30), "CLAN ENTRANCE", fill=(255, 255, 255, 255))
    draw.text((panel_x + 30, panel_y + 55), "Sign in to synchronize leaderboards & progress", fill=(187, 202, 191, 180))
    
    # Auth Buttons inside panel
    btn_w, btn_h = 330, 46
    bx = panel_x + 30
    
    # Google
    b1_y = panel_y + 105
    draw.rounded_rectangle([bx, b1_y, bx + btn_w, b1_y + btn_h], radius=23, fill=(255, 255, 255, 255), outline=(220, 225, 235, 255), width=1)
    draw.text((bx + 85, b1_y + 13), "Sign in with Google", fill=(31, 41, 55, 255))
    draw.ellipse([bx + 48, b1_y + 13, bx + 68, b1_y + 33], fill=(66, 133, 244, 255))
    
    # Apple
    b2_y = b1_y + 58
    draw.rounded_rectangle([bx, b2_y, bx + btn_w, b2_y + btn_h], radius=23, fill=(255, 255, 255, 255), outline=(220, 225, 235, 255), width=1)
    draw.text((bx + 88, b2_y + 13), "Sign in with Apple", fill=(31, 41, 55, 255))
    draw.ellipse([bx + 50, b2_y + 13, bx + 70, b2_y + 33], fill=(0, 0, 0, 255))
    
    # Guest
    b3_y = b2_y + 68
    draw.rounded_rectangle([bx, b3_y, bx + btn_w, b3_y + 48], radius=24, fill=(16, 185, 129, 230), outline=(110, 251, 190, 200), width=1)
    draw.text((bx + 85, b3_y + 14), "QUICK GUEST PLAY  ➜", fill=(0, 33, 19, 255))
    
    # Status footer
    draw.text((panel_x + 30, panel_y + 390), "SERVER: ASIA-NORTHEAST-1  •  ONLINE", fill=(110, 251, 190, 220))
    
    out_path = os.path.join(artifact_dir, "landscape_sign_on_splash_screenshot.png")
    canvas.save(out_path, format="PNG")
    print("Saved:", out_path)

# 4. SCREENSHOT 4: Shinobi Sprint Campaign Intro & Launch Screen (540 x 960)
def render_shinobi_intro_launch_splash():
    w, h = 540, 960
    canvas = Image.new("RGBA", (w, h), (13, 19, 34, 255))
    
    # Background artwork
    bg_path = os.path.join(base_dir, "assets", "images", "shinobi_sign_on_bg.png")
    if os.path.exists(bg_path):
        bg = Image.open(bg_path).convert("RGBA")
        bg = bg.resize((w, h), Image.Resampling.LANCZOS)
        canvas.paste(bg, (0, 0))
        
    # Vignettes
    scrim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(scrim)
    for y in range(160):
        alpha = int(180 * (1 - y / 160))
        sdraw.line([(0, y), (w, y)], fill=(13, 19, 34, alpha))
    for y in range(350):
        alpha = int(245 * (y / 350))
        sdraw.line([(0, h - 350 + y), (w, h - 350 + y)], fill=(8, 14, 29, alpha))
    canvas.paste(scrim, (0, 0), scrim)
    
    # Drifting Sakura Petals
    random.seed(77)
    petal_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(petal_layer)
    for _ in range(26):
        px = random.uniform(20, w - 20)
        py = random.uniform(60, h - 60)
        pw = random.uniform(8, 14)
        ph = random.uniform(5, 9)
        palpha = int(random.uniform(90, 210))
        pdraw.ellipse([px - pw/2, py - ph/2, px + pw/2, py + ph/2], fill=(244, 114, 182, palpha))
    canvas.paste(petal_layer, (0, 0), petal_layer)
    
    draw = ImageDraw.Draw(canvas)
    
    # Crest Badge: 忍 び ス プ リ ン ト
    badge_w, badge_h = 160, 28
    bx = (w - badge_w) // 2
    by = 95
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=14, fill=(225, 29, 72, 70), outline=(225, 29, 72, 160), width=1)
    draw.text((bx + 18, by + 6), "忍 び ス プ リ ン ト", fill=(253, 164, 175, 255))
    
    # Logo
    logo_path = os.path.join(base_dir, "assets", "images", "shinobi_sprint_logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_w = 340
        logo_h = int(logo.height * (logo_w / logo.width))
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        lx = (w - logo_w) // 2
        ly = by + 38
        canvas.paste(logo, (lx, ly), logo)
    
    # Gold divider
    div_w = 140
    div_x = (w - div_w) // 2
    div_y = ly + logo_h + 10
    draw.line([(div_x, div_y), (div_x + div_w, div_y)], fill=(245, 158, 11, 230), width=2)
    
    # Lore Description Box
    lore_y = div_y + 24
    draw.text((45, lore_y), "Sprint through feudal Japan as the Blue Chibi Ninja!", fill=(226, 232, 240, 255))
    draw.text((38, lore_y + 24), "Master the katana, collect ancient soul orbs, and leap", fill=(187, 202, 191, 220))
    draw.text((120, lore_y + 46), "across sacred mountain Torii shrines.", fill=(187, 202, 191, 220))
    
    # Buttons
    btn_w, btn_h = 360, 52
    btn_x = (w - btn_w) // 2
    
    # 1. Primary Action: PLAY SHINOBI SPRINT
    b1_y = lore_y + 110
    draw.rounded_rectangle([btn_x, b1_y, btn_x + btn_w, b1_y + btn_h], radius=26, fill=(16, 185, 129, 240), outline=(110, 251, 190, 255), width=2)
    draw.text((btn_x + 85, b1_y + 16), "▶  PLAY SHINOBI SPRINT", fill=(0, 33, 19, 255))
    
    # 2. Secondary Action: SELECT STAGES
    b2_y = b1_y + 64
    draw.rounded_rectangle([btn_x, b2_y, btn_x + btn_w, b2_y + btn_h], radius=26, fill=(67, 56, 202, 230), outline=(129, 140, 248, 220), width=2)
    draw.text((btn_x + 105, b2_y + 16), "☵  SELECT STAGES", fill=(255, 255, 255, 255))
    
    # Bottom HUD Circles: Audio, Leaderboard, Info, HowToPlay
    icons_y = b2_y + 85
    icons = ["♫", "🏆", "ℹ", "❓"]
    spacing = 64
    start_x = (w - (len(icons) * spacing)) // 2 + 10
    for idx, ic in enumerate(icons):
        ix = start_x + idx * spacing
        draw.ellipse([ix, icons_y, ix + 44, icons_y + 44], fill=(21, 27, 43, 210), outline=(255, 255, 255, 80), width=1)
        draw.text((ix + 16, icons_y + 12), ic, fill=(255, 255, 255, 220))
    
    out_path = os.path.join(artifact_dir, "shinobi_campaign_intro_splash_screenshot.png")
    canvas.save(out_path, format="PNG")
    print("Saved:", out_path)

if __name__ == "__main__":
    render_web_loading_splash()
    render_mobile_sign_on_splash()
    render_landscape_sign_on_splash()
    render_shinobi_intro_launch_splash()
    print("All splash screens rendered successfully!")
