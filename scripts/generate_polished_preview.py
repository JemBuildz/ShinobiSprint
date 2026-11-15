import base64
import os

artifact_dir = r"C:\Users\User\.gemini\antigravity\brain\8d1fe0d7-a367-49a2-ba0b-1e27387c2271"

def to_b64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

assets_b64 = {
    "sky_layer3": to_b64("assets/images/backgrounds/farthest_sky.png"),
    "mountains_layer2": to_b64("assets/images/backgrounds/deep_background.png"),
    "bamboo_layer1": to_b64("assets/images/backgrounds/mid_background.png"),
    "midair_platform": to_b64("assets/map/cutouts/wooden_midair_platform.png"),
    "boardwalk_ground": to_b64("assets/map/cutouts/wooden_boardwalk_platform.png"),
    "lantern": to_b64("assets/map/cutouts/lantern_post_glowing.png"),
    "ninja_run": to_b64("assets/images/spritesheet_ninja_run.png"),
    "ninja_jump": to_b64("assets/images/spritesheet_ninja_jump.png"),
}

# -------------------------------------------------------------------------
# GENERATE CARD: mobile_preview_card.html
# -------------------------------------------------------------------------
card_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Shinobi Sprint - 3-Layer Parallax & Collision Polished</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{ margin: 0; background: #050814; color: #FFF; font-family: ui-sans-serif, system-ui, sans-serif; }}
    canvas {{ display: block; }}
  </style>
</head>
<body class="p-3 bg-[#050814] flex flex-col items-center">
  <div class="w-full max-w-2xl bg-[#0D1527] border border-[#C5A059]/60 rounded-2xl overflow-hidden shadow-2xl">
    
    <!-- Top Bar -->
    <div class="px-4 py-2.5 bg-[#080D1A] border-b border-amber-500/20 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="text-xs font-bold tracking-wider text-amber-300 uppercase">Shinobi Sprint • 3-Layer Depth & Readability Polish</span>
      </div>
      <div class="flex items-center gap-2 text-[11px]">
        <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">60 FPS</span>
      </div>
    </div>

    <!-- Canvas Viewport -->
    <div class="relative w-full h-[320px] bg-[#040711] overflow-hidden select-none cursor-pointer" id="canvasContainer">
      <canvas id="stage" width="640" height="320" class="w-full h-full"></canvas>

      <!-- Action prompt -->
      <div class="absolute bottom-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-black/85 border border-amber-500/30 text-[11px] font-bold text-amber-200 pointer-events-none backdrop-blur-sm">
        Tap / Spacebar to Jump
      </div>

      <!-- Score HUD -->
      <div class="absolute top-3 left-3 flex items-center gap-2 px-3 py-1 rounded-full bg-[#080D1A]/90 border border-[#C5A059]/40 text-xs font-bold text-[#FFB74D] backdrop-blur-md pointer-events-none">
        <span>🏆 SCORE:</span>
        <span id="scoreVal" class="font-mono text-white">0</span>
      </div>
    </div>

    <!-- Inspector Legend -->
    <div class="p-3 bg-[#070B16] border-t border-slate-800 text-[11px] text-slate-300 flex flex-wrap items-center justify-between gap-2">
      <div class="flex items-center gap-2">
        <span class="text-amber-400 font-bold">3-Depth Hierarchy:</span>
        <span class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">L3: Moon (100%)</span>
        <span class="px-1.5 py-0.5 rounded bg-slate-800 text-blue-300">L2: Pagoda/Mtn (40% Fog)</span>
        <span class="px-1.5 py-0.5 rounded bg-slate-800 text-emerald-300">L1: Bamboo/Torii (70%)</span>
        <span class="px-1.5 py-0.5 rounded bg-slate-800 text-amber-300 font-semibold">FG: Boardwalk (100%)</span>
      </div>
      <div class="text-emerald-400 font-mono text-[10px]">
        No Floating Stilts • No Wall Traps
      </div>
    </div>
  </div>

  <script>
    const canvas = document.getElementById('stage');
    const ctx = canvas.getContext('2d');
    const scoreVal = document.getElementById('scoreVal');

    const assets = {{
      sky: new Image(),
      mountains: new Image(),
      bamboo: new Image(),
      midair: new Image(),
      boardwalk: new Image(),
      lantern: new Image(),
      ninja_run: new Image(),
      ninja_jump: new Image(),
    }};

    assets.sky.src = '{assets_b64["sky_layer3"]}';
    assets.mountains.src = '{assets_b64["mountains_layer2"]}';
    assets.bamboo.src = '{assets_b64["bamboo_layer1"]}';
    assets.midair.src = '{assets_b64["midair_platform"]}';
    assets.boardwalk.src = '{assets_b64["boardwalk_ground"]}';
    assets.lantern.src = '{assets_b64["lantern"]}';
    assets.ninja_run.src = '{assets_b64["ninja_run"]}';
    assets.ninja_jump.src = '{assets_b64["ninja_jump"]}';

    // GROUND BASELINE: Continuous main floor at y = 265 (No invisible wall traps!)
    const FLOOR_Y = 265;

    // Elevated Mid-Air Platforms (Equipped with clean wooden brackets, no floating stilt feet)
    const midAirPlatforms = [
      {{ x: 190, y: 190, w: 160, h: 36 }},
      {{ x: 420, y: 155, w: 170, h: 36 }},
      {{ x: 670, y: 185, w: 160, h: 36 }},
    ];

    // Lanterns firmly mounted
    const lanterns = [
      {{ x: 80, y: FLOOR_Y - 58, w: 22, h: 60 }},
      {{ x: 260, y: 190 - 58, w: 22, h: 60 }},
      {{ x: 500, y: 155 - 58, w: 22, h: 60 }},
      {{ x: 740, y: 185 - 58, w: 22, h: 60 }},
    ];

    // Player
    const player = {{
      x: 70,
      y: FLOOR_Y - 48,
      vy: 0,
      width: 40,
      height: 48,
      isGrounded: true,
      frame: 0,
      animTimer: 0
    }};

    let worldScroll = 0;

    function jump() {{
      if (player.isGrounded) {{
        player.vy = -12.5;
        player.isGrounded = false;
      }}
    }}

    window.addEventListener('keydown', (e) => {{
      if (e.code === 'Space' || e.key === ' ') {{
        e.preventDefault();
        jump();
      }}
    }});

    document.getElementById('canvasContainer').addEventListener('pointerdown', () => {{
      jump();
    }});

    let lastTime = performance.now();

    function render(now) {{
      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;

      worldScroll += 2.4;
      scoreVal.textContent = Math.floor(worldScroll / 5);

      // Physics
      player.vy += 32 * dt;
      player.y += player.vy;

      // Platform collision
      let onPlatform = false;
      const playerFeet = player.y + player.height;

      // 1. Check mid-air platforms
      for (const p of midAirPlatforms) {{
        const sx = ((p.x - worldScroll) % 850 + 850) % 850 - 150;
        if (player.x + player.width > sx && player.x < sx + p.w) {{
          // Land on top surface
          if (playerFeet >= p.y - 2 && playerFeet <= p.y + 14 && player.vy >= 0) {{
            player.y = p.y - player.height;
            player.vy = 0;
            player.isGrounded = true;
            onPlatform = true;
            break;
          }}
        }}
      }}

      // 2. Safe Continuous Ground (Never fall off screen, no invisible wall traps)
      if (!onPlatform && player.y >= FLOOR_Y - player.height) {{
        player.y = FLOOR_Y - player.height;
        player.vy = 0;
        player.isGrounded = true;
        onPlatform = true;
      }}

      // Animation
      player.animTimer += dt;
      if (player.animTimer > 0.08) {{
        player.frame = (player.frame + 1) % 6;
        player.animTimer = 0;
      }}

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // -------------------------------------------------------------
      // LAYER 3 (Far - 0.0x stationary): Moon & Stars (100% Opacity)
      // -------------------------------------------------------------
      if (assets.sky.complete && assets.sky.naturalWidth > 0) {{
        ctx.globalAlpha = 1.0;
        ctx.drawImage(assets.sky, 0, 0, canvas.width, canvas.height);
      }}

      // -------------------------------------------------------------
      // LAYER 2 (Mid - 0.25x): Pagoda & Distant Mountains (40% Opacity)
      // -------------------------------------------------------------
      if (assets.mountains.complete && assets.mountains.naturalWidth > 0) {{
        ctx.globalAlpha = 0.40; // User specified 40% opacity for atmospheric fog
        const mtx = -(worldScroll * 0.25) % canvas.width;
        ctx.drawImage(assets.mountains, mtx, 60, canvas.width, 220);
        ctx.drawImage(assets.mountains, mtx + canvas.width, 60, canvas.width, 220);
        ctx.globalAlpha = 1.0;
      }}

      // -------------------------------------------------------------
      // LAYER 1 (Near - 0.5x): Bamboo Trees & Torii in Grove (70% Opacity)
      // (Positioned strictly in the background so it never clips platforms)
      // -------------------------------------------------------------
      if (assets.bamboo.complete && assets.bamboo.naturalWidth > 0) {{
        ctx.globalAlpha = 0.70; // User specified 70% opacity
        const bbx = -(worldScroll * 0.50) % canvas.width;
        ctx.drawImage(assets.bamboo, bbx, 90, canvas.width, 180);
        ctx.drawImage(assets.bamboo, bbx + canvas.width, 90, canvas.width, 180);
        ctx.globalAlpha = 1.0;
      }}

      // -------------------------------------------------------------
      // FOREGROUND (1.0x): 100% Sharp Contrast Playable Platforms & Ninja
      // -------------------------------------------------------------
      ctx.globalAlpha = 1.0;

      // Draw Continuous Ground Boardwalk (Open sprint, no blocking side stone walls!)
      if (assets.boardwalk.complete && assets.boardwalk.naturalWidth > 0) {{
        const bw = 240;
        const scrollOffset = -(worldScroll % bw);
        for (let bx = scrollOffset - bw; bx < canvas.width + bw; bx += bw) {{
          ctx.drawImage(assets.boardwalk, bx, FLOOR_Y, bw, 60);
        }}
      }} else {{
        ctx.fillStyle = '#6E3C1B';
        ctx.fillRect(0, FLOOR_Y, canvas.width, 60);
      }}

      // Draw Mid-Air Platforms (Clean brackets, NO floating stilt feet!)
      for (const p of midAirPlatforms) {{
        const sx = ((p.x - worldScroll) % 850 + 850) % 850 - 150;
        if (assets.midair.complete && assets.midair.naturalWidth > 0) {{
          ctx.drawImage(assets.midair, sx, p.y, p.w, p.h);
        }} else {{
          ctx.fillStyle = '#8B4513';
          ctx.fillRect(sx, p.y, p.w, 14);
        }}
      }}

      // Draw Glowing Lanterns (Sitting squarely on platform surfaces)
      for (const l of lanterns) {{
        const lx = ((l.x - worldScroll) % 850 + 850) % 850 - 150;
        if (assets.lantern.complete && assets.lantern.naturalWidth > 0) {{
          ctx.drawImage(assets.lantern, lx, l.y, l.w, l.h);
        }}
      }}

      // Draw Ninja Player Sprite (Feet resting cleanly on top planks)
      const sprite = player.isGrounded ? assets.ninja_run : assets.ninja_jump;
      if (sprite.complete && sprite.naturalWidth > 0) {{
        const frameW = sprite.naturalWidth / 6;
        const frameH = sprite.naturalHeight;
        const frameIdx = player.isGrounded ? player.frame : 2;
        ctx.drawImage(
          sprite,
          frameIdx * frameW, 0, frameW, frameH,
          player.x, player.y, player.width, player.height
        );
      }}

      requestAnimationFrame(render);
    }}

    requestAnimationFrame(render);
  </script>
</body>
</html>
"""

card_path = os.path.join(artifact_dir, "mobile_preview_card.html")
with open(card_path, "w", encoding="utf-8") as f:
    f.write(card_html)
print("Updated mobile_preview_card.html with 3-layer depth and collision fixes")

# -------------------------------------------------------------------------
# GENERATE FULL SIMULATOR: mobile_preview.html
# -------------------------------------------------------------------------
full_simulator_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shinobi Sprint - 3-Layer Depth & Collision Polish</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen p-4 flex flex-col items-center justify-center font-sans antialiased">

  <div class="max-w-4xl w-full text-center mb-5">
    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold uppercase tracking-wider mb-2">
      <span>✓ 3-Layer Parallax & Collision Polished</span>
    </div>
    <h1 class="text-3xl md:text-4xl font-black text-amber-200 tracking-wider">SHINOBI SPRINT</h1>
    <p class="text-slate-400 text-sm mt-1">
      Mid-Air Bracket Platforms (No Floating Stilts) • 3-Layer Calibrated Opacities • Clear Running Surface (No Wall Traps)
    </p>
  </div>

  <div class="flex flex-col lg:flex-row items-center justify-center gap-8 max-w-5xl w-full">
    <!-- Phone Bezel -->
    <div class="relative flex-shrink-0">
      <div class="w-[360px] h-[720px] bg-slate-900 rounded-[48px] p-3 shadow-2xl border-4 border-slate-700/80 ring-1 ring-amber-500/20 relative overflow-hidden flex flex-col">
        
        <!-- Notch -->
        <div class="absolute top-5 left-1/2 -translate-x-1/2 w-28 h-5 bg-black rounded-full z-50 flex items-center justify-center gap-2">
          <div class="w-2.5 h-2.5 bg-slate-900 rounded-full border border-slate-800"></div>
          <div class="w-2 h-2 bg-indigo-950 rounded-full"></div>
        </div>

        <!-- Phone Display Screen -->
        <div class="relative w-full h-full bg-[#050814] rounded-[38px] overflow-hidden flex flex-col select-none">
          
          <!-- Status Bar -->
          <div class="w-full pt-3 px-6 pb-1 flex justify-between items-center text-[11px] font-bold text-slate-300 z-40 bg-gradient-to-b from-black/70 to-transparent">
            <span>9:41</span>
            <div class="flex items-center gap-2">
              <span class="text-emerald-400 font-mono">60 FPS</span>
              <div class="w-5 h-2.5 border border-slate-400 rounded-sm p-0.5 flex items-center">
                <div class="w-full h-full bg-emerald-400 rounded-2xs"></div>
              </div>
            </div>
          </div>

          <!-- Flame Parallax Game Canvas -->
          <div class="relative flex-1 w-full overflow-hidden cursor-pointer" id="gameViewport">
            <canvas id="stage" width="360" height="660" class="absolute inset-0 w-full h-full"></canvas>

            <!-- Top Score HUD -->
            <div class="absolute top-10 left-1/2 -translate-x-1/2 z-30 pointer-events-none">
              <div class="flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-[#090D1A]/90 border border-[#C5A059] shadow-lg shadow-black/80 backdrop-blur-md">
                <span class="text-lg">🏆</span>
                <span class="text-xs text-[#E2C99B] font-semibold tracking-wider">SCORE:</span>
                <span id="scoreVal" class="text-base font-black text-[#FFB74D]">0</span>
              </div>
            </div>

            <!-- Tap to Jump Prompt -->
            <div class="absolute bottom-6 left-1/2 -translate-x-1/2 z-30 pointer-events-none text-center">
              <div class="px-5 py-2 rounded-full bg-[#090D1A]/95 border border-[#C5A059] shadow-xl backdrop-blur-md">
                <span class="text-xs font-bold tracking-widest text-[#FFF7ED]">TAP SCREEN TO JUMP</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Inspector Sidebar -->
    <div class="flex flex-col gap-4 max-w-md w-full">
      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl">
        <h3 class="text-base font-bold text-amber-200 mb-3 flex items-center gap-2">
          <span>🎯</span> Verified Improvements
        </h3>
        <div class="space-y-3 text-xs text-slate-300">
          <div class="p-3 rounded-xl bg-slate-800/70 border border-slate-700/60">
            <div class="font-bold text-emerald-400 mb-1">1. Mid-Air Bracket Platforms (No Floating Stilts)</div>
            <p class="text-slate-400 leading-relaxed">
              Upper platforms now use dedicated hanging angle brackets rather than disconnected stilts or floating stone footings.
            </p>
          </div>
          <div class="p-3 rounded-xl bg-slate-800/70 border border-slate-700/60">
            <div class="font-bold text-emerald-400 mb-1">2. 3-Layer Parallax & Fog Calibration</div>
            <p class="text-slate-400 leading-relaxed">
              • <strong>Layer 3 (Far)</strong>: Moon & Stars (100% Opacity)<br>
              • <strong>Layer 2 (Mid)</strong>: Massive Pagoda & Mountains (40% Opacity + Blue Fog)<br>
              • <strong>Layer 1 (Near)</strong>: Bamboo & Torii Landmark (70% Opacity in Background)<br>
              • <strong>Foreground</strong>: 100% Crisp Platforms & Ninja
            </p>
          </div>
          <div class="p-3 rounded-xl bg-slate-800/70 border border-slate-700/60">
            <div class="font-bold text-emerald-400 mb-1">3. Gameplay Readability & No Wall Traps</div>
            <p class="text-slate-400 leading-relaxed">
              The continuous boardwalk floor runs without horizontal stone face obstacles. The Torii gate sits strictly in the background grove without overlapping playable platforms.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const canvas = document.getElementById('stage');
    const ctx = canvas.getContext('2d');
    const scoreVal = document.getElementById('scoreVal');

    const assets = {{
      sky: new Image(),
      mountains: new Image(),
      bamboo: new Image(),
      midair: new Image(),
      boardwalk: new Image(),
      lantern: new Image(),
      ninja_run: new Image(),
      ninja_jump: new Image(),
    }};

    assets.sky.src = '{assets_b64["sky_layer3"]}';
    assets.mountains.src = '{assets_b64["mountains_layer2"]}';
    assets.bamboo.src = '{assets_b64["bamboo_layer1"]}';
    assets.midair.src = '{assets_b64["midair_platform"]}';
    assets.boardwalk.src = '{assets_b64["boardwalk_ground"]}';
    assets.lantern.src = '{assets_b64["lantern"]}';
    assets.ninja_run.src = '{assets_b64["ninja_run"]}';
    assets.ninja_jump.src = '{assets_b64["ninja_jump"]}';

    const FLOOR_Y = 550;

    // Mid-air platforms with wooden brackets
    const midAirPlatforms = [
      {{ x: 180, y: 440, w: 200, h: 48 }},
      {{ x: 440, y: 380, w: 210, h: 48 }},
      {{ x: 730, y: 430, w: 200, h: 48 }},
    ];

    const lanterns = [
      {{ x: 70, y: FLOOR_Y - 82, w: 32, h: 84 }},
      {{ x: 260, y: 440 - 82, w: 32, h: 84 }},
      {{ x: 520, y: 380 - 82, w: 32, h: 84 }},
      {{ x: 810, y: 430 - 82, w: 32, h: 84 }},
    ];

    const player = {{
      x: 60,
      y: FLOOR_Y - 58,
      vy: 0,
      width: 50,
      height: 60,
      isGrounded: true,
      frame: 0,
      animTimer: 0
    }};

    let worldScroll = 0;

    function jump() {{
      if (player.isGrounded) {{
        player.vy = -14.5;
        player.isGrounded = false;
      }}
    }}

    window.addEventListener('keydown', (e) => {{
      if (e.code === 'Space' || e.key === ' ') {{
        e.preventDefault();
        jump();
      }}
    }});

    document.getElementById('gameViewport').addEventListener('pointerdown', () => {{
      jump();
    }});

    let lastTime = performance.now();

    function render(now) {{
      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;

      worldScroll += 2.4;
      scoreVal.textContent = Math.floor(worldScroll / 5);

      player.vy += 32 * dt;
      player.y += player.vy;

      let onPlatform = false;
      const playerFeet = player.y + player.height;

      // 1. Check mid-air platforms
      for (const p of midAirPlatforms) {{
        const sx = ((p.x - worldScroll) % 950 + 950) % 950 - 150;
        if (player.x + player.width > sx && player.x < sx + p.w) {{
          if (playerFeet >= p.y - 2 && playerFeet <= p.y + 16 && player.vy >= 0) {{
            player.y = p.y - player.height;
            player.vy = 0;
            player.isGrounded = true;
            onPlatform = true;
            break;
          }}
        }}
      }}

      // 2. Safe continuous ground
      if (!onPlatform && player.y >= FLOOR_Y - player.height) {{
        player.y = FLOOR_Y - player.height;
        player.vy = 0;
        player.isGrounded = true;
        onPlatform = true;
      }}

      player.animTimer += dt;
      if (player.animTimer > 0.08) {{
        player.frame = (player.frame + 1) % 6;
        player.animTimer = 0;
      }}

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // LAYER 3 (Far - 0.0x): Moon & Stars (100% Opacity)
      if (assets.sky.complete && assets.sky.naturalWidth > 0) {{
        ctx.globalAlpha = 1.0;
        ctx.drawImage(assets.sky, 0, 0, canvas.width, canvas.height);
      }}

      // LAYER 2 (Mid - 0.25x): Pagoda & Distant Mountains (40% Opacity)
      if (assets.mountains.complete && assets.mountains.naturalWidth > 0) {{
        ctx.globalAlpha = 0.40;
        const mtx = -(worldScroll * 0.25) % canvas.width;
        ctx.drawImage(assets.mountains, mtx, 140, canvas.width, 380);
        ctx.drawImage(assets.mountains, mtx + canvas.width, 140, canvas.width, 380);
        ctx.globalAlpha = 1.0;
      }}

      // LAYER 1 (Near - 0.5x): Bamboo & Torii Landmark in Grove (70% Opacity)
      // (Kept strictly in the background behind playable platforms)
      if (assets.bamboo.complete && assets.bamboo.naturalWidth > 0) {{
        ctx.globalAlpha = 0.70;
        const bbx = -(worldScroll * 0.50) % canvas.width;
        ctx.drawImage(assets.bamboo, bbx, 190, canvas.width, 340);
        ctx.drawImage(assets.bamboo, bbx + canvas.width, 190, canvas.width, 340);
        ctx.globalAlpha = 1.0;
      }}

      // FOREGROUND (1.0x): 100% Contrast Crisp Platforms & Ninja
      ctx.globalAlpha = 1.0;

      // Continuous ground boardwalk floor (no blocking walls!)
      if (assets.boardwalk.complete && assets.boardwalk.naturalWidth > 0) {{
        const bw = 320;
        const scrollOffset = -(worldScroll % bw);
        for (let bx = scrollOffset - bw; bx < canvas.width + bw; bx += bw) {{
          ctx.drawImage(assets.boardwalk, bx, FLOOR_Y, bw, 80);
        }}
      }}

      // Mid-Air Platforms with brackets (No floating stilt feet!)
      for (const p of midAirPlatforms) {{
        const sx = ((p.x - worldScroll) % 950 + 950) % 950 - 150;
        if (assets.midair.complete && assets.midair.naturalWidth > 0) {{
          ctx.drawImage(assets.midair, sx, p.y, p.w, p.h);
        }}
      }}

      // Glowing Lanterns
      for (const l of lanterns) {{
        const lx = ((l.x - worldScroll) % 950 + 950) % 950 - 150;
        if (assets.lantern.complete && assets.lantern.naturalWidth > 0) {{
          ctx.drawImage(assets.lantern, lx, l.y, l.w, l.h);
        }}
      }}

      // Ninja Player Sprite
      const sprite = player.isGrounded ? assets.ninja_run : assets.ninja_jump;
      if (sprite.complete && sprite.naturalWidth > 0) {{
        const frameW = sprite.naturalWidth / 6;
        const frameH = sprite.naturalHeight;
        const frameIdx = player.isGrounded ? player.frame : 2;
        ctx.drawImage(
          sprite,
          frameIdx * frameW, 0, frameW, frameH,
          player.x, player.y, player.width, player.height
        );
      }}

      requestAnimationFrame(render);
    }}

    requestAnimationFrame(render);
  </script>
</body>
</html>
"""

full_path = os.path.join(artifact_dir, "mobile_preview.html")
with open(full_path, "w", encoding="utf-8") as f:
    f.write(full_simulator_html)
print("Updated full mobile_preview.html successfully")
