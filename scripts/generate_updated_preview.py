import base64
import os

artifact_dir = r"C:\Users\User\.gemini\antigravity\brain\8d1fe0d7-a367-49a2-ba0b-1e27387c2271"

def to_b64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

cutouts = {
    "torii": to_b64("assets/map/cutouts/torii_gate.png"),
    "lantern": to_b64("assets/map/cutouts/lantern_post_glowing.png"),
    "pagoda": to_b64("assets/map/cutouts/pagoda_shrine.png"),
    "house": to_b64("assets/map/cutouts/japanese_shrine_house.png"),
    "bamboo": to_b64("assets/map/cutouts/bamboo_cluster.png"),
    "boardwalk": to_b64("assets/map/cutouts/wooden_boardwalk_platform.png"),
    "sky_night": to_b64("assets/images/backgrounds/farthest_sky.png"),
    "sky_day": to_b64("assets/images/backgrounds/day_farthest_sky.png"),
    "deep_night": to_b64("assets/images/backgrounds/deep_background.png"),
    "deep_day": to_b64("assets/images/backgrounds/day_deep_background.png"),
    "mid_night": to_b64("assets/images/backgrounds/mid_background.png"),
    "mid_day": to_b64("assets/images/backgrounds/day_mid_background.png"),
    "ninja_run": to_b64("assets/images/spritesheet_ninja_run.png"),
    "ninja_jump": to_b64("assets/images/spritesheet_ninja_jump.png"),
}

# Generate mobile_preview_card.html (compact inline embed)
card_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Shinobi Sprint - Tilemap Assets Live Preview</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{ margin: 0; background: #070B14; color: #FFF; font-family: ui-sans-serif, system-ui, sans-serif; }}
    canvas {{ display: block; }}
  </style>
</head>
<body class="p-3 bg-[#070B14] flex flex-col items-center">
  <div class="w-full max-w-2xl bg-[#0F172A] border border-[#C5A059]/40 rounded-xl overflow-hidden shadow-2xl">
    
    <!-- Header bar -->
    <div class="px-4 py-2.5 bg-[#090D1A] border-b border-amber-500/20 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse"></span>
        <span class="text-xs font-bold tracking-wider text-amber-300 uppercase">Shinobi Sprint • Tilemap Engine Preview</span>
      </div>
      <div class="flex items-center gap-2">
        <button id="themeToggle" class="px-2.5 py-1 text-[11px] font-semibold rounded bg-[#1E293B] border border-[#C5A059]/50 text-amber-200 hover:bg-amber-500/20 transition-colors">
          🌙 Night Mode
        </button>
        <span class="text-[11px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">60 FPS</span>
      </div>
    </div>

    <!-- Interactive Canvas Viewport -->
    <div class="relative w-full h-[320px] bg-[#090D1A] overflow-hidden select-none cursor-pointer" id="canvasContainer">
      <canvas id="stage" width="640" height="320" class="w-full h-full"></canvas>

      <!-- Jump banner prompt -->
      <div class="absolute bottom-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-black/75 border border-amber-500/30 text-[11px] font-bold text-amber-200 pointer-events-none backdrop-blur-sm">
        Tap / Spacebar to Jump onto Boardwalks
      </div>

      <!-- Real-time HUD -->
      <div class="absolute top-3 left-3 flex items-center gap-2 px-3 py-1 rounded-full bg-[#090D1A]/90 border border-[#C5A059]/40 text-xs font-bold text-[#FFB74D] backdrop-blur-md pointer-events-none">
        <span>🏆 SCORE:</span>
        <span id="scoreVal" class="font-mono text-white">0</span>
      </div>
    </div>

    <!-- Asset Inspector Footer -->
    <div class="p-3 bg-[#0A0E1A] border-t border-slate-800 text-[11px] text-slate-300 flex flex-wrap items-center justify-between gap-2">
      <div class="flex items-center gap-3">
        <span class="text-amber-400 font-semibold">Active Elements:</span>
        <span class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">⛩️ Torii Gate</span>
        <span class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">🏮 Glowing Lanterns</span>
        <span class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">🏯 Pagoda Shrine</span>
        <span class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">🪵 Boardwalk Platforms</span>
      </div>
      <div class="text-slate-400 font-mono text-[10px]">
        Leap Physics: Collision Active
      </div>
    </div>
  </div>

  <script>
    const canvas = document.getElementById('stage');
    const ctx = canvas.getContext('2d');
    const scoreVal = document.getElementById('scoreVal');
    const themeBtn = document.getElementById('themeToggle');

    let isNight = true;
    themeBtn.addEventListener('click', (e) => {{
      e.stopPropagation();
      isNight = !isNight;
      themeBtn.textContent = isNight ? '🌙 Night Mode' : '☀️ Day Mode';
    }});

    // Load Image Assets
    const assets = {{
      torii: new Image(),
      lantern: new Image(),
      pagoda: new Image(),
      house: new Image(),
      bamboo: new Image(),
      boardwalk: new Image(),
      sky_night: new Image(),
      sky_day: new Image(),
      deep_night: new Image(),
      deep_day: new Image(),
      mid_night: new Image(),
      mid_day: new Image(),
      ninja_run: new Image(),
      ninja_jump: new Image(),
    }};

    assets.torii.src = '{cutouts["torii"]}';
    assets.lantern.src = '{cutouts["lantern"]}';
    assets.pagoda.src = '{cutouts["pagoda"]}';
    assets.house.src = '{cutouts["house"]}';
    assets.bamboo.src = '{cutouts["bamboo"]}';
    assets.boardwalk.src = '{cutouts["boardwalk"]}';
    assets.sky_night.src = '{cutouts["sky_night"]}';
    assets.sky_day.src = '{cutouts["sky_day"]}';
    assets.deep_night.src = '{cutouts["deep_night"]}';
    assets.deep_day.src = '{cutouts["deep_day"]}';
    assets.mid_night.src = '{cutouts["mid_night"]}';
    assets.mid_day.src = '{cutouts["mid_day"]}';
    assets.ninja_run.src = '{cutouts["ninja_run"]}';
    assets.ninja_jump.src = '{cutouts["ninja_jump"]}';

    // Player state
    const player = {{
      x: 90,
      y: 200,
      vy: 0,
      width: 48,
      height: 48,
      groundY: 200,
      isGrounded: true,
      frame: 0,
      animTimer: 0
    }};

    // Platforms with Leap physics collision
    const platforms = [
      {{ x: 0, y: 248, w: 260, h: 72 }},
      {{ x: 310, y: 220, w: 220, h: 72 }},
      {{ x: 570, y: 190, w: 250, h: 72 }},
      {{ x: 860, y: 248, w: 300, h: 72 }},
    ];

    // Objects in world
    const worldObjects = [
      {{ type: 'pagoda', x: 180, y: 60, w: 100, h: 140, speed: 0.3 }},
      {{ type: 'house', x: 480, y: 100, w: 110, h: 100, speed: 0.4 }},
      {{ type: 'bamboo', x: 720, y: 90, w: 90, h: 110, speed: 0.5 }},
      {{ type: 'torii', x: 340, y: 95, w: 110, h: 105, speed: 1.0 }},
      {{ type: 'lantern', x: 40, y: 175, w: 28, h: 72, speed: 1.0 }},
      {{ type: 'lantern', x: 480, y: 150, w: 28, h: 70, speed: 1.0 }},
      {{ type: 'lantern', x: 780, y: 120, w: 28, h: 70, speed: 1.0 }},
    ];

    let worldScroll = 0;
    let score = 0;
    const scrollSpeed = 2.4;

    function jump() {{
      if (player.isGrounded) {{
        player.vy = -12;
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

      worldScroll += scrollSpeed;
      score = Math.floor(worldScroll / 5);
      scoreVal.textContent = score;

      // Physics update
      player.vy += 28 * dt; // gravity
      player.y += player.vy;

      // Platform collision
      let onPlatform = false;
      const playerFeet = player.y + player.height;
      const playerX = player.x;

      for (const p of platforms) {{
        const screenX = (p.x - worldScroll) % 1160;
        const normX = screenX < -p.w ? screenX + 1160 : screenX;
        if (playerX + player.width > normX && playerX < normX + p.w) {{
          if (playerFeet >= p.y && playerFeet <= p.y + 20 && player.vy >= 0) {{
            player.y = p.y - player.height;
            player.vy = 0;
            player.isGrounded = true;
            onPlatform = true;
            break;
          }}
        }}
      }}

      if (!onPlatform) {{
        player.isGrounded = false;
        if (player.y > 270) {{
          player.y = 200;
          player.vy = 0;
          player.isGrounded = true;
        }}
      }}

      // Animation frame
      player.animTimer += dt;
      if (player.animTimer > 0.08) {{
        player.frame = (player.frame + 1) % 6;
        player.animTimer = 0;
      }}

      // --- RENDERING ---
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // 1. Sky layer (0.0x stationary)
      const skyImg = isNight ? assets.sky_night : assets.sky_day;
      if (skyImg.complete && skyImg.naturalWidth > 0) {{
        ctx.drawImage(skyImg, 0, 0, canvas.width, canvas.height);
      }} else {{
        ctx.fillStyle = isNight ? '#0B1120' : '#88B0D0';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
      }}

      // 2. Mountains / Deep Background (0.25x)
      const deepImg = isNight ? assets.deep_night : assets.deep_day;
      if (deepImg.complete && deepImg.naturalWidth > 0) {{
        const dx = -(worldScroll * 0.25) % canvas.width;
        ctx.drawImage(deepImg, dx, 40, canvas.width, 220);
        ctx.drawImage(deepImg, dx + canvas.width, 40, canvas.width, 220);
      }}

      // 3. Midground Shrines & Trees (0.3x to 0.5x)
      for (const obj of worldObjects) {{
        if (obj.speed < 1.0) {{
          const ox = ((obj.x - worldScroll * obj.speed) % 960 + 960) % 960 - 100;
          let img = null;
          if (obj.type === 'pagoda') img = assets.pagoda;
          if (obj.type === 'house') img = assets.house;
          if (obj.type === 'bamboo') img = assets.bamboo;
          if (img && img.complete && img.naturalWidth > 0) {{
            ctx.drawImage(img, ox, obj.y, obj.w, obj.h);
          }}
        }}
      }}

      // 4. Wooden Boardwalk Platforms (1.0x)
      for (const p of platforms) {{
        const sx = ((p.x - worldScroll) % 1160 + 1160) % 1160 - 200;
        if (assets.boardwalk.complete && assets.boardwalk.naturalWidth > 0) {{
          ctx.drawImage(assets.boardwalk, sx, p.y - 4, p.w, p.h);
        }} else {{
          // Cedar wood fallback
          ctx.fillStyle = '#6E3C1B';
          ctx.fillRect(sx, p.y, p.w, p.h);
          ctx.fillStyle = '#A35E2D';
          ctx.fillRect(sx, p.y, p.w, 8);
        }}
      }}

      // 5. Foreground Props (Torii Gate & Lanterns at 1.0x)
      for (const obj of worldObjects) {{
        if (obj.speed === 1.0) {{
          const ox = ((obj.x - worldScroll) % 1160 + 1160) % 1160 - 150;
          let img = null;
          if (obj.type === 'torii') img = assets.torii;
          if (obj.type === 'lantern') img = assets.lantern;
          if (img && img.complete && img.naturalWidth > 0) {{
            ctx.drawImage(img, ox, obj.y, obj.w, obj.h);
          }}
        }}
      }}

      // 6. Ninja Player Sprite
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
      }} else {{
        ctx.fillStyle = '#E11D48';
        ctx.fillRect(player.x, player.y, player.width, player.height);
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
print("Updated mobile_preview_card.html successfully:", card_path)
