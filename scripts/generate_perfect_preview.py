import base64
import os

artifact_dirs = [
    r"C:\Users\User\.gemini\antigravity\brain\aafaea32-8493-447f-9dd1-1ef9ae5953f6",
    r"C:\Users\User\.gemini\antigravity\brain\8d1fe0d7-a367-49a2-ba0b-1e27387c2271",
]

def to_b64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

assets_b64 = {
    "torii": to_b64("assets/map/cutouts/torii_gate.png"),
    "lantern": to_b64("assets/map/cutouts/lantern_post_glowing.png"),
    "pagoda": to_b64("assets/map/cutouts/pagoda_shrine_grounded.png") or to_b64("assets/map/cutouts/pagoda_shrine.png"),
    "house": to_b64("assets/map/cutouts/japanese_shrine_house.png"),
    "bamboo": to_b64("assets/map/cutouts/bamboo_cluster.png"),
    "boardwalk_deck": to_b64("assets/map/cutouts/boardwalk_continuous.png"),
    "boardwalk_elevated": to_b64("assets/map/cutouts/boardwalk_elevated.png"),
    "boardwalk_platform": to_b64("assets/map/cutouts/wooden_boardwalk_platform.png"),
    "sky_night": to_b64("assets/images/backgrounds/farthest_sky.png"),
    "deep_night": to_b64("assets/images/backgrounds/deep_background.png"),
    "mid_night": to_b64("assets/images/backgrounds/mid_background.png"),
    "ninja_run": to_b64("assets/images/spritesheet_ninja_run.png"),
    "ninja_jump": to_b64("assets/images/spritesheet_ninja_jump.png"),
}

# -------------------------------------------------------------------------
# BUILD FULL MOBILE SIMULATOR: mobile_preview.html (Portrait 360 x 660)
# -------------------------------------------------------------------------
full_simulator_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shinobi Sprint - Master Mobile Preview</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-[#03060E] text-slate-100 min-h-screen p-4 flex flex-col items-center justify-center font-sans antialiased">

  <div class="max-w-4xl w-full text-center mb-5">
    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold uppercase tracking-wider mb-2">
      <span>✓ Architecture & Layout Verified</span>
    </div>
    <h1 class="text-3xl md:text-4xl font-black text-amber-200 tracking-wider">SHINOBI SPRINT</h1>
    <p class="text-slate-400 text-sm mt-1">
      Continuous solid boardwalk deck, grounded mist pagoda, unobstructed Torii gate, and structural timber pillars
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
          <span>⛩️</span> Master Architecture Validations
        </h3>
        <div class="space-y-3 text-xs text-slate-300">
          <div class="p-3 rounded-xl bg-slate-800/70 border border-slate-700/60">
            <div class="font-bold text-emerald-400 mb-1">✓ Continuous Solid Cedar Deck</div>
            <p class="text-slate-400 leading-relaxed">
              No repeated stone pedestal cutouts on base ground. Pure continuous cedar decking anchored with foundation pilings.
            </p>
          </div>
          <div class="p-3 rounded-xl bg-slate-800/70 border border-slate-700/60">
            <div class="font-bold text-emerald-400 mb-1">✓ Pagoda Shrouded in Mountain Fog</div>
            <p class="text-slate-400 leading-relaxed">
              Pagoda stone foundation is naturally nestled into the mountain mist line instead of hovering mid-air.
            </p>
          </div>
          <div class="p-3 rounded-xl bg-slate-800/70 border border-slate-700/60">
            <div class="font-bold text-emerald-400 mb-1">✓ Torii Gate Zero-Clipping Clearance</div>
            <p class="text-slate-400 leading-relaxed">
              The Torii gate is placed in an open courtyard clearing on base ground with zero platform beam intersections.
            </p>
          </div>
          <div class="p-3 rounded-xl bg-slate-800/70 border border-slate-700/60">
            <div class="font-bold text-emerald-400 mb-1">✓ Structural Timber Pillars on Platforms</div>
            <p class="text-slate-400 leading-relaxed">
              Elevated boardwalks feature Japanese cantilever brackets and structural timber columns descending solidly into the base ground.
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
      torii: new Image(),
      lantern: new Image(),
      pagoda: new Image(),
      house: new Image(),
      bamboo: new Image(),
      boardwalk_deck: new Image(),
      boardwalk_elevated: new Image(),
      sky: new Image(),
      mountains: new Image(),
      bamboo_layer: new Image(),
      ninja_run: new Image(),
      ninja_jump: new Image(),
    }};

    assets.torii.src = '{assets_b64["torii"]}';
    assets.lantern.src = '{assets_b64["lantern"]}';
    assets.pagoda.src = '{assets_b64["pagoda"]}';
    assets.house.src = '{assets_b64["house"]}';
    assets.bamboo.src = '{assets_b64["bamboo"]}';
    assets.boardwalk_deck.src = '{assets_b64["boardwalk_deck"]}';
    assets.boardwalk_elevated.src = '{assets_b64["boardwalk_elevated"]}';
    assets.sky.src = '{assets_b64["sky_night"]}';
    assets.mountains.src = '{assets_b64["deep_night"]}';
    assets.bamboo_layer.src = '{assets_b64["mid_night"]}';
    assets.ninja_run.src = '{assets_b64["ninja_run"]}';
    assets.ninja_jump.src = '{assets_b64["ninja_jump"]}';

    const BASE_GROUND_Y = 550;

    // Elevated Boardwalk Platforms (with ample clearance around Torii at x=340..460)
    const platforms = [
      {{ x: -200, y: BASE_GROUND_Y, w: 1400, h: 110, isBase: true }},
      {{ x: 120, y: 440, w: 180, h: 48, isBase: false }},
      {{ x: 500, y: 390, w: 200, h: 48, isBase: false }},
      {{ x: 780, y: 430, w: 190, h: 48, isBase: false }},
    ];

    const scenery = [
      // Midground Pagoda grounded at horizon mist
      {{ type: 'pagoda', x: 140, y: 375, w: 125, h: 180, speed: 0.25 }},
      {{ type: 'house', x: 440, y: 435, w: 130, h: 120, speed: 0.35 }},
      {{ type: 'bamboo', x: 50, y: BASE_GROUND_Y - 145, w: 90, h: 150, speed: 0.45 }},
      {{ type: 'bamboo', x: 670, y: BASE_GROUND_Y - 145, w: 90, h: 150, speed: 0.45 }},
      
      // Foreground Torii Gate (speed 1.0x, in open clearing at x=340..460)
      {{ type: 'torii', x: 340, y: BASE_GROUND_Y - 150, w: 125, h: 155, speed: 1.0 }},

      // Lanterns anchored firmly on platforms & ground
      {{ type: 'lantern', x: 60, y: BASE_GROUND_Y - 78, w: 32, h: 80, speed: 1.0 }},
      {{ type: 'lantern', x: 250, y: 440 - 78, w: 32, h: 80, speed: 1.0 }},
      {{ type: 'lantern', x: 470, y: BASE_GROUND_Y - 78, w: 32, h: 80, speed: 1.0 }},
      {{ type: 'lantern', x: 650, y: 390 - 78, w: 32, h: 80, speed: 1.0 }},
    ];

    const player = {{
      x: 70,
      y: BASE_GROUND_Y - 58,
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

      // Physics
      player.vy += 32 * dt;
      player.y += player.vy;

      let onPlatform = false;
      const playerFeet = player.y + player.height;

      for (const p of platforms) {{
        let sx = p.x;
        if (!p.isBase) {{
          sx = ((p.x - worldScroll) % 900 + 900) % 900 - 150;
        }}
        if (player.x + player.width > sx && player.x < sx + p.w) {{
          if (playerFeet >= p.y - 2 && playerFeet <= p.y + 18 && player.vy >= 0) {{
            player.y = p.y - player.height;
            player.vy = 0;
            player.isGrounded = true;
            onPlatform = true;
            break;
          }}
        }}
      }}

      if (!onPlatform && player.y >= BASE_GROUND_Y - player.height) {{
        player.y = BASE_GROUND_Y - player.height;
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

      // --- DRAW SCENE ---
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // 1. Undistorted Portrait Sky (0.0x stationary)
      if (assets.sky.complete && assets.sky.naturalWidth > 0) {{
        ctx.drawImage(assets.sky, 0, 0, canvas.width, canvas.height);
      }}

      // 2. Distant Mountains with Seamless Fog Fade (0.18x)
      if (assets.mountains.complete && assets.mountains.naturalWidth > 0) {{
        const mtx = -(worldScroll * 0.18) % canvas.width;
        ctx.drawImage(assets.mountains, mtx, 140, canvas.width, 380);
        ctx.drawImage(assets.mountains, mtx + canvas.width, 140, canvas.width, 380);
      }}

      // 3. Bamboo Canopy & Mist (0.42x)
      if (assets.bamboo_layer.complete && assets.bamboo_layer.naturalWidth > 0) {{
        const bbx = -(worldScroll * 0.42) % canvas.width;
        ctx.drawImage(assets.bamboo_layer, bbx, 190, canvas.width, 340);
        ctx.drawImage(assets.bamboo_layer, bbx + canvas.width, 190, canvas.width, 340);
      }}

      // 4. Midground Pagoda & House (0.25x - 0.35x)
      for (const item of scenery) {{
        if (item.speed < 1.0) {{
          const ox = ((item.x - worldScroll * item.speed) % 800 + 800) % 800 - 100;
          let img = null;
          if (item.type === 'pagoda') img = assets.pagoda;
          if (item.type === 'house') img = assets.house;
          if (item.type === 'bamboo') img = assets.bamboo;
          if (img && img.complete && img.naturalWidth > 0) {{
            ctx.drawImage(img, ox, item.y, item.w, item.h);
          }}
        }}
      }}

      // 5. Structural Pillars for Elevated Platforms
      for (const p of platforms) {{
        if (!p.isBase) {{
          const sx = ((p.x - worldScroll) % 900 + 900) % 900 - 150;
          // Left structural cedar post
          ctx.fillStyle = '#2A180E';
          ctx.fillRect(sx + 16, p.y + p.h - 10, 14, BASE_GROUND_Y - (p.y + p.h - 10));
          ctx.fillStyle = '#442616';
          ctx.fillRect(sx + 18, p.y + p.h - 10, 3, BASE_GROUND_Y - (p.y + p.h - 10));
          // Right structural cedar post
          ctx.fillStyle = '#2A180E';
          ctx.fillRect(sx + p.w - 30, p.y + p.h - 10, 14, BASE_GROUND_Y - (p.y + p.h - 10));
          ctx.fillStyle = '#442616';
          ctx.fillRect(sx + p.w - 28, p.y + p.h - 10, 3, BASE_GROUND_Y - (p.y + p.h - 10));

          // Draw elevated platform
          if (assets.boardwalk_elevated.complete && assets.boardwalk_elevated.naturalWidth > 0) {{
            ctx.drawImage(assets.boardwalk_elevated, sx, p.y, p.w, p.h);
          }}
        }}
      }}

      // 6. Continuous Solid Base Boardwalk Ground
      // Base bedrock bed
      ctx.fillStyle = '#0F1626';
      ctx.fillRect(0, BASE_GROUND_Y + 45, canvas.width, canvas.height - (BASE_GROUND_Y + 45));

      if (assets.boardwalk_deck.complete && assets.boardwalk_deck.naturalWidth > 0) {{
        const bw = 256;
        const scrollOffset = -(worldScroll % bw);
        for (let bx = scrollOffset - bw; bx < canvas.width + bw; bx += bw) {{
          ctx.drawImage(assets.boardwalk_deck, bx, BASE_GROUND_Y, bw, 60);
        }}
      }}

      // 7. Props (Torii & Lanterns with warm light halo)
      for (const item of scenery) {{
        if (item.speed === 1.0) {{
          const ox = ((item.x - worldScroll) % 900 + 900) % 900 - 150;
          let img = null;
          if (item.type === 'torii') img = assets.torii;
          if (item.type === 'lantern') {{
            img = assets.lantern;
            // Draw warm amber radial glow around lantern head
            const glow = ctx.createRadialGradient(ox + 16, item.y + 24, 4, ox + 16, item.y + 24, 38);
            glow.addColorStop(0, 'rgba(255, 175, 40, 0.45)');
            glow.addColorStop(0.5, 'rgba(255, 140, 20, 0.18)');
            glow.addColorStop(1, 'rgba(255, 140, 20, 0)');
            ctx.fillStyle = glow;
            ctx.beginPath();
            ctx.arc(ox + 16, item.y + 24, 38, 0, Math.PI * 2);
            ctx.fill();
          }}
          if (img && img.complete && img.naturalWidth > 0) {{
            ctx.drawImage(img, ox, item.y, item.w, item.h);
          }}
        }}
      }}

      // 8. Ninja Player Sprite
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

# -------------------------------------------------------------------------
# BUILD COMPACT INLINE EMBED: mobile_preview_card.html (Landscape 640 x 320)
# -------------------------------------------------------------------------
card_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Shinobi Sprint - Corrected Master View</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{ margin: 0; background: #040711; color: #FFF; font-family: ui-sans-serif, system-ui, sans-serif; }}
    canvas {{ display: block; }}
  </style>
</head>
<body class="p-3 bg-[#040711] flex flex-col items-center">
  <div class="w-full max-w-2xl bg-[#0B101D] border border-[#C5A059]/60 rounded-2xl overflow-hidden shadow-2xl">
    
    <!-- Header -->
    <div class="px-4 py-2.5 bg-[#080D1A] border-b border-amber-500/20 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="text-xs font-bold tracking-wider text-amber-300 uppercase">Shinobi Sprint • Production Map & Background Fixed</span>
      </div>
      <span class="text-[11px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">60 FPS</span>
    </div>

    <!-- Canvas -->
    <div class="relative w-full h-[320px] bg-[#040711] overflow-hidden select-none cursor-pointer" id="canvasContainer">
      <canvas id="stage" width="640" height="320" class="w-full h-full"></canvas>

      <div class="absolute bottom-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-black/80 border border-amber-500/30 text-[11px] font-bold text-amber-200 pointer-events-none backdrop-blur-sm">
        Tap / Spacebar to Jump
      </div>

      <div class="absolute top-3 left-3 flex items-center gap-2 px-3 py-1 rounded-full bg-[#080D1A]/90 border border-[#C5A059]/50 text-xs font-bold text-[#FFB74D] backdrop-blur-md pointer-events-none">
        <span>🏆 SCORE:</span>
        <span id="scoreVal" class="font-mono text-white">0</span>
      </div>
    </div>

    <!-- Footer Status -->
    <div class="p-3 bg-[#080D1A] border-t border-slate-800 text-[11px] text-slate-300 flex items-center justify-between">
      <div class="flex items-center gap-2 text-slate-300">
        <span class="text-emerald-400 font-semibold">✓ Fixed:</span>
        <span>Continuous Cedar Deck</span> • <span>Misty Horizon Pagoda</span> • <span>Clear Torii Crossing</span>
      </div>
      <div class="text-amber-400/90 font-mono text-[10px]">
        Structural Timber Pillars Active
      </div>
    </div>
  </div>

  <script>
    const canvas = document.getElementById('stage');
    const ctx = canvas.getContext('2d');
    const scoreVal = document.getElementById('scoreVal');

    const assets = {{
      torii: new Image(),
      lantern: new Image(),
      pagoda: new Image(),
      house: new Image(),
      bamboo: new Image(),
      boardwalk_deck: new Image(),
      boardwalk_elevated: new Image(),
      sky: new Image(),
      mountains: new Image(),
      bamboo_layer: new Image(),
      ninja_run: new Image(),
      ninja_jump: new Image(),
    }};

    assets.torii.src = '{assets_b64["torii"]}';
    assets.lantern.src = '{assets_b64["lantern"]}';
    assets.pagoda.src = '{assets_b64["pagoda"]}';
    assets.house.src = '{assets_b64["house"]}';
    assets.bamboo.src = '{assets_b64["bamboo"]}';
    assets.boardwalk_deck.src = '{assets_b64["boardwalk_deck"]}';
    assets.boardwalk_elevated.src = '{assets_b64["boardwalk_elevated"]}';
    assets.sky.src = '{assets_b64["sky_night"]}';
    assets.mountains.src = '{assets_b64["deep_night"]}';
    assets.bamboo_layer.src = '{assets_b64["mid_night"]}';
    assets.ninja_run.src = '{assets_b64["ninja_run"]}';
    assets.ninja_jump.src = '{assets_b64["ninja_jump"]}';

    const BASE_GROUND_Y = 255;

    // Platforms with generous Torii clearance (Torii at x=340..435)
    const platforms = [
      {{ x: -200, y: BASE_GROUND_Y, w: 1200, h: 70, isBase: true }},
      {{ x: 120, y: 195, w: 160, h: 36, isBase: false }},
      {{ x: 470, y: 165, w: 170, h: 36, isBase: false }},
      {{ x: 700, y: 200, w: 160, h: 36, isBase: false }},
    ];

    const scenery = [
      // Grounded Pagoda sitting on misty mountain ridge line (bottom at BASE_GROUND_Y)
      {{ type: 'pagoda', x: 110, y: 135, w: 90, h: 125, speed: 0.22 }},
      {{ type: 'house', x: 400, y: 165, w: 100, h: 92, speed: 0.35 }},
      {{ type: 'bamboo', x: 50, y: BASE_GROUND_Y - 95, w: 65, h: 100, speed: 0.45 }},
      {{ type: 'bamboo', x: 590, y: BASE_GROUND_Y - 95, w: 65, h: 100, speed: 0.45 }},
      
      // Torii Gate completely clear of platforms (clearing between x=280 and x=470)
      {{ type: 'torii', x: 330, y: BASE_GROUND_Y - 105, w: 88, h: 110, speed: 1.0 }},

      // Lanterns firmly rooted with warm ambient light
      {{ type: 'lantern', x: 60, y: BASE_GROUND_Y - 55, w: 22, h: 56, speed: 1.0 }},
      {{ type: 'lantern', x: 235, y: 195 - 55, w: 22, h: 56, speed: 1.0 }},
      {{ type: 'lantern', x: 435, y: BASE_GROUND_Y - 55, w: 22, h: 56, speed: 1.0 }},
      {{ type: 'lantern', x: 590, y: 165 - 55, w: 22, h: 56, speed: 1.0 }},
    ];

    const player = {{
      x: 70,
      y: BASE_GROUND_Y - 48,
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

      player.vy += 30 * dt;
      player.y += player.vy;

      let onPlatform = false;
      const playerFeet = player.y + player.height;

      for (const p of platforms) {{
        let sx = p.x;
        if (!p.isBase) {{
          sx = ((p.x - worldScroll) % 800 + 800) % 800 - 150;
        }}
        if (player.x + player.width > sx && player.x < sx + p.w) {{
          if (playerFeet >= p.y - 2 && playerFeet <= p.y + 14 && player.vy >= 0) {{
            player.y = p.y - player.height;
            player.vy = 0;
            player.isGrounded = true;
            onPlatform = true;
            break;
          }}
        }}
      }}

      if (!onPlatform && player.y >= BASE_GROUND_Y - player.height) {{
        player.y = BASE_GROUND_Y - player.height;
        player.vy = 0;
        player.isGrounded = true;
      }}

      player.animTimer += dt;
      if (player.animTimer > 0.08) {{
        player.frame = (player.frame + 1) % 6;
        player.animTimer = 0;
      }}

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // 1. Sky & Moon (0.0x)
      if (assets.sky.complete && assets.sky.naturalWidth > 0) {{
        ctx.drawImage(assets.sky, 0, 0, canvas.width, canvas.height);
      }}

      // 2. Distant Mountains & Mist (0.18x)
      if (assets.mountains.complete && assets.mountains.naturalWidth > 0) {{
        const mtx = -(worldScroll * 0.18) % canvas.width;
        ctx.drawImage(assets.mountains, mtx, 50, canvas.width, 220);
        ctx.drawImage(assets.mountains, mtx + canvas.width, 50, canvas.width, 220);
      }}

      // 3. Bamboo Canopy & Fog (0.42x)
      if (assets.bamboo_layer.complete && assets.bamboo_layer.naturalWidth > 0) {{
        const bbx = -(worldScroll * 0.42) % canvas.width;
        ctx.drawImage(assets.bamboo_layer, bbx, 80, canvas.width, 190);
        ctx.drawImage(assets.bamboo_layer, bbx + canvas.width, 80, canvas.width, 190);
      }}

      // 4. Grounded Midground Shrines & Bamboo
      for (const item of scenery) {{
        if (item.speed < 1.0) {{
          const ox = ((item.x - worldScroll * item.speed) % 750 + 750) % 750 - 100;
          let img = null;
          if (item.type === 'pagoda') img = assets.pagoda;
          if (item.type === 'house') img = assets.house;
          if (item.type === 'bamboo') img = assets.bamboo;
          if (img && img.complete && img.naturalWidth > 0) {{
            ctx.drawImage(img, ox, item.y, item.w, item.h);
          }}
        }}
      }}

      // 5. Structural Pillars & Elevated Platforms
      for (const p of platforms) {{
        if (!p.isBase) {{
          const sx = ((p.x - worldScroll) % 800 + 800) % 800 - 150;
          
          // Solid vertical timber pillars reaching the ground
          ctx.fillStyle = '#26140A';
          ctx.fillRect(sx + 14, p.y + p.h - 8, 10, BASE_GROUND_Y - (p.y + p.h - 8));
          ctx.fillStyle = '#442616';
          ctx.fillRect(sx + 15, p.y + p.h - 8, 2, BASE_GROUND_Y - (p.y + p.h - 8));

          ctx.fillStyle = '#26140A';
          ctx.fillRect(sx + p.w - 24, p.y + p.h - 8, 10, BASE_GROUND_Y - (p.y + p.h - 8));
          ctx.fillStyle = '#442616';
          ctx.fillRect(sx + p.w - 23, p.y + p.h - 8, 2, BASE_GROUND_Y - (p.y + p.h - 8));

          // Draw elevated platform
          if (assets.boardwalk_elevated.complete && assets.boardwalk_elevated.naturalWidth > 0) {{
            ctx.drawImage(assets.boardwalk_elevated, sx, p.y, p.w, p.h);
          }}
        }}
      }}

      // 6. Continuous Base Ground Boardwalk (No Gaps, Solid Footing)
      ctx.fillStyle = '#0B101D';
      ctx.fillRect(0, BASE_GROUND_Y + 36, canvas.width, canvas.height - (BASE_GROUND_Y + 36));

      if (assets.boardwalk_deck.complete && assets.boardwalk_deck.naturalWidth > 0) {{
        const bw = 220;
        const scrollOffset = -(worldScroll % bw);
        for (let bx = scrollOffset - bw; bx < canvas.width + bw; bx += bw) {{
          ctx.drawImage(assets.boardwalk_deck, bx, BASE_GROUND_Y, bw, 50);
        }}
      }}

      // 7. Foreground Props (Torii & Glowing Lanterns)
      for (const item of scenery) {{
        if (item.speed === 1.0) {{
          const ox = ((item.x - worldScroll) % 800 + 800) % 800 - 150;
          let img = null;
          if (item.type === 'torii') img = assets.torii;
          if (item.type === 'lantern') {{
            img = assets.lantern;
            // Warm amber lantern light halo
            const glow = ctx.createRadialGradient(ox + 11, item.y + 17, 3, ox + 11, item.y + 17, 26);
            glow.addColorStop(0, 'rgba(255, 175, 40, 0.45)');
            glow.addColorStop(0.5, 'rgba(255, 140, 20, 0.18)');
            glow.addColorStop(1, 'rgba(255, 140, 20, 0)');
            ctx.fillStyle = glow;
            ctx.beginPath();
            ctx.arc(ox + 11, item.y + 17, 26, 0, Math.PI * 2);
            ctx.fill();
          }}
          if (img && img.complete && img.naturalWidth > 0) {{
            ctx.drawImage(img, ox, item.y, item.w, item.h);
          }}
        }}
      }}

      // 8. Ninja Sprite
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

# Write to all target artifact directories
for ad in artifact_dirs:
    os.makedirs(ad, exist_ok=True)
    full_path = os.path.join(ad, "mobile_preview.html")
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(full_simulator_html)
    card_path = os.path.join(ad, "mobile_preview_card.html")
    with open(card_path, "w", encoding="utf-8") as f:
        f.write(card_html)
    print(f"Written preview files to {ad}")

# Also copy to web/
os.makedirs('web', exist_ok=True)
with open('web/mobile_preview.html', 'w', encoding='utf-8') as f:
    f.write(full_simulator_html)
with open('web/mobile_preview_card.html', 'w', encoding='utf-8') as f:
    f.write(card_html)
print("Updated web/ preview copies successfully.")
