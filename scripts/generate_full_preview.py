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

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shinobi Sprint - Tilemap Platformer Simulator</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen p-4 md:p-8 flex flex-col items-center justify-center font-sans antialiased">

  <div class="max-w-4xl w-full text-center mb-6">
    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-semibold uppercase tracking-wider mb-2">
      <span>✦ Authentic Feudal Japan Tilemap Architecture</span>
    </div>
    <h1 class="text-3xl md:text-4xl font-black text-amber-200 tracking-wider">SHINOBI SPRINT</h1>
    <p class="text-slate-400 text-sm mt-1">
      Live simulation showing isolated cutouts: Torii Gates, Glowing Lanterns, Pagoda Shrines & Wooden Boardwalk Platforms
    </p>
  </div>

  <div class="flex flex-col lg:flex-row items-center justify-center gap-8 max-w-5xl w-full">
    <!-- Phone Frame -->
    <div class="relative flex-shrink-0">
      <div class="w-[360px] h-[720px] bg-slate-900 rounded-[48px] p-3 shadow-2xl border-4 border-slate-700/80 ring-1 ring-amber-500/20 relative overflow-hidden flex flex-col">
        <div class="absolute top-5 left-1/2 -translate-x-1/2 w-28 h-5 bg-black rounded-full z-50 flex items-center justify-center gap-2">
          <div class="w-2.5 h-2.5 bg-slate-900 rounded-full border border-slate-800"></div>
          <div class="w-2 h-2 bg-indigo-950 rounded-full"></div>
        </div>

        <div class="relative w-full h-full bg-[#090D1A] rounded-[38px] overflow-hidden flex flex-col select-none">
          <div class="w-full pt-3 px-6 pb-1 flex justify-between items-center text-[11px] font-bold text-slate-300 z-40 bg-gradient-to-b from-black/60 to-transparent">
            <span>9:41</span>
            <div class="flex items-center gap-1.5">
              <span class="text-emerald-400">● 60 FPS</span>
            </div>
          </div>

          <div class="relative flex-1 w-full overflow-hidden cursor-pointer" id="gameViewport">
            <canvas id="stage" width="360" height="660" class="absolute inset-0 w-full h-full"></canvas>

            <div class="absolute top-10 left-1/2 -translate-x-1/2 z-30 pointer-events-none">
              <div class="flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-[#090D1A]/90 border border-[#C5A059] shadow-lg shadow-black/70 backdrop-blur-md">
                <span class="text-xl">🏆</span>
                <span class="text-xs text-[#E2C99B] font-semibold tracking-wider">SCORE:</span>
                <span id="scoreVal" class="text-base font-black text-[#FFB74D]">0</span>
              </div>
            </div>

            <div class="absolute bottom-16 left-1/2 -translate-x-1/2 z-30 pointer-events-none text-center">
              <div class="px-5 py-2 rounded-full bg-[#090D1A]/90 border border-[#C5A059] shadow-xl backdrop-blur-md">
                <span class="text-xs font-bold tracking-widest text-[#FFF7ED]">TAP SCREEN TO JUMP</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Controls & Inspector Sidebar -->
    <div class="flex flex-col gap-4 max-w-md w-full">
      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl">
        <h3 class="text-base font-bold text-amber-200 mb-3 flex items-center gap-2">
          <span>⚙️</span> Interactive Test Controls
        </h3>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-slate-300">Environment Theme:</span>
            <button id="themeToggle" class="px-4 py-1.5 rounded-lg bg-amber-500/20 border border-amber-500/40 text-amber-300 font-bold text-xs hover:bg-amber-500/30 transition-all">
              🌙 Night Mode
            </button>
          </div>
          <div>
            <div class="flex justify-between text-xs text-slate-400 mb-1">
              <span>Platform Speed:</span>
              <span id="speedLabel" class="font-mono text-amber-300">1.0x</span>
            </div>
            <input type="range" id="speedSlider" min="0.5" max="2.5" step="0.1" value="1.0" class="w-full accent-amber-500">
          </div>
        </div>
      </div>

      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl">
        <h3 class="text-base font-bold text-amber-200 mb-3 flex items-center gap-2">
          <span>📦</span> Active Tilemap Cutouts
        </h3>
        <div class="space-y-2 text-xs">
          <div class="p-2.5 rounded-xl bg-slate-800/60 border border-slate-700/50 flex items-center justify-between">
            <span class="font-medium text-amber-300">⛩️ Torii Gate (tile_gate_v2)</span>
            <span class="text-emerald-400 font-mono">320×256 Active</span>
          </div>
          <div class="p-2.5 rounded-xl bg-slate-800/60 border border-slate-700/50 flex items-center justify-between">
            <span class="font-medium text-amber-300">🏮 Glowing Lantern (tile_decorations)</span>
            <span class="text-emerald-400 font-mono">660×204 Active</span>
          </div>
          <div class="p-2.5 rounded-xl bg-slate-800/60 border border-slate-700/50 flex items-center justify-between">
            <span class="font-medium text-amber-300">🏯 Pagoda Shrine (tile_trees_front)</span>
            <span class="text-emerald-400 font-mono">588×324 Active</span>
          </div>
          <div class="p-2.5 rounded-xl bg-slate-800/60 border border-slate-700/50 flex items-center justify-between">
            <span class="font-medium text-amber-300">🪵 Boardwalk Planks (tile_ground_v04)</span>
            <span class="text-emerald-400 font-mono">748×816 Active</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const canvas = document.getElementById('stage');
    const ctx = canvas.getContext('2d');
    const scoreVal = document.getElementById('scoreVal');
    const themeBtn = document.getElementById('themeToggle');
    const speedSlider = document.getElementById('speedSlider');
    const speedLabel = document.getElementById('speedLabel');

    let isNight = true;
    let speedMult = 1.0;

    themeBtn.addEventListener('click', () => {{
      isNight = !isNight;
      themeBtn.textContent = isNight ? '🌙 Night Mode' : '☀️ Day Mode';
    }});

    speedSlider.addEventListener('input', (e) => {{
      speedMult = parseFloat(e.target.value);
      speedLabel.textContent = speedMult.toFixed(1) + 'x';
    }});

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

    const player = {{
      x: 60,
      y: 440,
      vy: 0,
      width: 56,
      height: 56,
      isGrounded: true,
      frame: 0,
      animTimer: 0
    }};

    const platforms = [
      {{ x: 0, y: 500, w: 240, h: 90 }},
      {{ x: 280, y: 460, w: 200, h: 90 }},
      {{ x: 520, y: 410, w: 220, h: 90 }},
      {{ x: 780, y: 500, w: 280, h: 90 }},
    ];

    const worldObjects = [
      {{ type: 'pagoda', x: 120, y: 180, w: 120, h: 180, speed: 0.25 }},
      {{ type: 'house', x: 380, y: 220, w: 140, h: 130, speed: 0.4 }},
      {{ type: 'bamboo', x: 560, y: 200, w: 110, h: 140, speed: 0.5 }},
      {{ type: 'torii', x: 320, y: 310, w: 130, h: 150, speed: 1.0 }},
      {{ type: 'lantern', x: 30, y: 410, w: 34, h: 90, speed: 1.0 }},
      {{ type: 'lantern', x: 440, y: 370, w: 34, h: 90, speed: 1.0 }},
      {{ type: 'lantern', x: 720, y: 320, w: 34, h: 90, speed: 1.0 }},
    ];

    let worldScroll = 0;

    function jump() {{
      if (player.isGrounded) {{
        player.vy = -13;
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

      worldScroll += 2.2 * speedMult;
      scoreVal.textContent = Math.floor(worldScroll / 5);

      player.vy += 28 * dt;
      player.y += player.vy;

      let onPlatform = false;
      const playerFeet = player.y + player.height;

      for (const p of platforms) {{
        const screenX = (p.x - worldScroll) % 1060;
        const normX = screenX < -p.w ? screenX + 1060 : screenX;
        if (player.x + player.width > normX && player.x < normX + p.w) {{
          if (playerFeet >= p.y && playerFeet <= p.y + 24 && player.vy >= 0) {{
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
        if (player.y > 540) {{
          player.y = 440;
          player.vy = 0;
          player.isGrounded = true;
        }}
      }}

      player.animTimer += dt;
      if (player.animTimer > 0.08) {{
        player.frame = (player.frame + 1) % 6;
        player.animTimer = 0;
      }}

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Sky
      const skyImg = isNight ? assets.sky_night : assets.sky_day;
      if (skyImg.complete && skyImg.naturalWidth > 0) {{
        ctx.drawImage(skyImg, 0, 0, canvas.width, canvas.height);
      }}

      // Deep mountains
      const deepImg = isNight ? assets.deep_night : assets.deep_day;
      if (deepImg.complete && deepImg.naturalWidth > 0) {{
        const dx = -(worldScroll * 0.2) % canvas.width;
        ctx.drawImage(deepImg, dx, 120, canvas.width, 360);
        ctx.drawImage(deepImg, dx + canvas.width, 120, canvas.width, 360);
      }}

      // Midground Shrines
      for (const obj of worldObjects) {{
        if (obj.speed < 1.0) {{
          const ox = ((obj.x - worldScroll * obj.speed) % 800 + 800) % 800 - 100;
          let img = null;
          if (obj.type === 'pagoda') img = assets.pagoda;
          if (obj.type === 'house') img = assets.house;
          if (obj.type === 'bamboo') img = assets.bamboo;
          if (img && img.complete && img.naturalWidth > 0) {{
            ctx.drawImage(img, ox, obj.y, obj.w, obj.h);
          }}
        }}
      }}

      // Boardwalk Platforms
      for (const p of platforms) {{
        const sx = ((p.x - worldScroll) % 1060 + 1060) % 1060 - 200;
        if (assets.boardwalk.complete && assets.boardwalk.naturalWidth > 0) {{
          ctx.drawImage(assets.boardwalk, sx, p.y - 6, p.w, p.h);
        }}
      }}

      // Foreground Torii & Lanterns
      for (const obj of worldObjects) {{
        if (obj.speed === 1.0) {{
          const ox = ((obj.x - worldScroll) % 1060 + 1060) % 1060 - 150;
          let img = null;
          if (obj.type === 'torii') img = assets.torii;
          if (obj.type === 'lantern') img = assets.lantern;
          if (img && img.complete && img.naturalWidth > 0) {{
            ctx.drawImage(img, ox, obj.y, obj.w, obj.h);
          }}
        }}
      }}

      // Ninja
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
    f.write(full_html)
print("Updated full mobile_preview.html successfully:", full_path)
