import base64
import os

images_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"
artifact_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b"
os.makedirs(artifact_dir, exist_ok=True)

assets = {
    "ninja": "character_ninja.png",
    "sky": "twilight_layer1_sky.png",
    "mountains": "twilight_layer2_mountains.png",
    "grove": "twilight_layer3_grove.png",
    "fireflies": "twilight_layer4_fireflies.png",
    "platform": "prop_bamboo_platform.png",
    "bridge": "prop_log_bridge.png",
    "block": "tile_autumn_block.png",
    "slope": "tile_autumn_slope.png",
    "torii": "prop_grand_torii.png",
    "lantern": "prop_stone_lantern_toro.png",
    "chimes": "prop_wind_chimes.png",
    "spikes": "hazard_bamboo_spikes.png",
    "shuriken": "hazard_shuriken.png",
    "orb": "item_spirit_orb.png",
}

b64_assets = {}
for key, filename in assets.items():
    p = os.path.join(images_dir, filename)
    if os.path.exists(p):
        with open(p, "rb") as f:
            b64_assets[key] = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
        print(f"Encoded {key}: {len(b64_assets[key])} chars")
    else:
        print(f"MISSING {p}")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Level 2: Twilight Bamboo Sanctuary - Mobile Preview</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{
      user-select: none;
      -webkit-user-select: none;
      touch-action: manipulation;
    }}
    .phone-shadow {{
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.8), 0 0 0 12px #181f2a, 0 0 0 14px #2b3544;
    }}
    .dynamic-island {{
      width: 90px;
      height: 24px;
      background: #000;
      border-radius: 20px;
      position: absolute;
      top: 8px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 50;
    }}
    canvas {{
      image-rendering: -webkit-optimize-contrast;
      image-rendering: crisp-edges;
    }}
    .ctrl-btn {{
      transition: transform 0.08s ease, filter 0.08s ease;
      touch-action: none;
    }}
    .ctrl-btn:active {{
      transform: scale(0.92);
      filter: brightness(1.25);
    }}
  </style>
</head>
<body class="bg-[#080c14] text-white min-h-screen flex flex-col items-center justify-center p-3 font-sans">

  <!-- Top Tool Header -->
  <header class="w-full max-w-4xl flex items-center justify-between mb-3 px-2">
    <div class="flex items-center gap-2">
      <span class="inline-block w-3 h-3 rounded-full bg-amber-400 animate-pulse"></span>
      <h1 class="text-sm md:text-base font-semibold text-amber-200">Level 2: Twilight Bamboo Sanctuary</h1>
    </div>
    <div class="flex items-center gap-2 text-xs">
      <button id="toggleHitboxesBtn" class="px-2.5 py-1 rounded bg-gray-800 hover:bg-gray-700 border border-gray-600 text-gray-300 font-mono transition">
        Hitboxes: <span id="hitboxStatus" class="text-gray-400 font-bold">OFF</span>
      </button>
      <button id="resetBtn" class="px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white font-medium transition flex items-center gap-1">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        Reset
      </button>
      <button id="orientationBtn" class="px-2.5 py-1 rounded bg-gray-800 hover:bg-gray-700 border border-gray-600 text-gray-300 font-medium transition">
        📱 Rotate
      </button>
    </div>
  </header>

  <!-- Mobile Device Container -->
  <main id="deviceWrapper" class="relative transition-all duration-300">
    <div id="phoneFrame" class="phone-shadow relative bg-[#0e131d] rounded-[36px] overflow-hidden border border-gray-700/50 flex flex-col" style="width: 780px; height: 430px;">
      
      <!-- Phone Top Status Bar -->
      <div class="w-full h-8 flex items-center justify-between px-6 text-[11px] font-mono text-gray-400 select-none z-40 bg-black/40 backdrop-blur-sm">
        <span id="clockText">18:45</span>
        <div class="dynamic-island"></div>
        <div class="flex items-center gap-2">
          <span>5G</span>
          <span class="inline-block w-4 h-2 border border-gray-400 rounded-sm p-[1px]"><span class="block w-full h-full bg-amber-400 rounded-xs"></span></span>
        </div>
      </div>

      <!-- Main Game Canvas Container -->
      <div class="relative flex-1 w-full h-full overflow-hidden bg-[#0c101a]">
        <canvas id="gameCanvas" width="1024" height="576" class="w-full h-full object-contain"></canvas>

        <!-- On-Screen Virtual Controls Overlay (Mobile D-Pad & Action Buttons) -->
        <div class="absolute inset-0 pointer-events-none flex flex-col justify-between p-4 z-30">
          
          <!-- Top In-Game Bar -->
          <div class="flex items-center justify-between pointer-events-auto">
            <div class="bg-black/60 backdrop-blur px-3 py-1 rounded-full border border-white/10 text-[11px] text-gray-300 flex items-center gap-3 font-mono">
              <span>FPS: <b id="fpsText" class="text-emerald-400">60</b></span>
              <span>Orbs: <b id="scoreText" class="text-amber-400">0 / 4</b></span>
              <span>Pos: <b id="posText" class="text-cyan-300">140, 420</b></span>
            </div>
            <div class="bg-black/60 backdrop-blur px-3 py-1 rounded-full border border-amber-400/30 text-[11px] text-amber-300 flex items-center gap-1.5">
              <span>🏮</span>
              <span>Sanctuary Dusk</span>
            </div>
          </div>

          <!-- Bottom Touch Controls -->
          <div class="flex items-end justify-between pointer-events-auto pb-1">
            
            <!-- Left / Right Touch D-Pad -->
            <div class="flex items-center gap-3">
              <button id="btnLeft" class="ctrl-btn w-14 h-14 rounded-2xl bg-white/15 active:bg-white/30 backdrop-blur border border-white/20 flex flex-col items-center justify-center text-white shadow-lg">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"/></svg>
                <span class="text-[10px] font-bold text-gray-300">A</span>
              </button>
              <button id="btnRight" class="ctrl-btn w-14 h-14 rounded-2xl bg-white/15 active:bg-white/30 backdrop-blur border border-white/20 flex flex-col items-center justify-center text-white shadow-lg">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"/></svg>
                <span class="text-[10px] font-bold text-gray-300">D</span>
              </button>
            </div>

            <!-- Keyboard Instructions Pill -->
            <div class="hidden md:flex bg-black/70 backdrop-blur-md border border-white/10 px-3.5 py-1.5 rounded-full text-[11px] text-gray-300 items-center gap-2 shadow-lg">
              <span class="text-amber-400 font-bold">Controls:</span>
              <span>[A]/[D] Run</span>
              <span class="text-gray-500">•</span>
              <span>[Space] Jump</span>
              <span class="text-gray-500">•</span>
              <span>[S]+[Space] Drop</span>
            </div>

            <!-- Drop / Jump Buttons -->
            <div class="flex items-center gap-3">
              <button id="btnDrop" class="ctrl-btn w-14 h-14 rounded-2xl bg-amber-500/25 active:bg-amber-500/50 backdrop-blur border border-amber-400/40 flex flex-col items-center justify-center text-amber-200 shadow-lg">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 14l-7 7m0 0l-7-7m7 7V3"/></svg>
                <span class="text-[10px] font-bold text-amber-300">DROP</span>
              </button>
              <button id="btnJump" class="ctrl-btn w-14 h-14 rounded-2xl bg-emerald-500/30 active:bg-emerald-500/60 backdrop-blur border border-emerald-400/50 flex flex-col items-center justify-center text-emerald-200 shadow-lg">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 10l7-7m0 0l7 7m-7-7v18"/></svg>
                <span class="text-[10px] font-bold text-emerald-300">JUMP</span>
              </button>
            </div>

          </div>

        </div>

      </div>

      <!-- Phone Bottom Home Indicator -->
      <div class="w-full h-4 bg-black/40 flex items-center justify-center">
        <div class="w-28 h-1 bg-white/40 rounded-full"></div>
      </div>

    </div>
  </main>

  <footer class="mt-3 text-xs text-gray-400 text-center">
    Level 2 Parallax Layers: <span class="text-amber-300">Sunset Sky (0.0x)</span> • <span class="text-amber-300">Distant Mountains (0.15x)</span> • <span class="text-amber-300">Midground Grove (0.35x)</span> • <span class="text-amber-300">Foreground Fireflies (1.3x)</span>
  </footer>

  <script>
    // Asset image dictionary
    const assetSources = {{
      ninja: "{b64_assets['ninja']}",
      sky: "{b64_assets['sky']}",
      mountains: "{b64_assets['mountains']}",
      grove: "{b64_assets['grove']}",
      fireflies: "{b64_assets['fireflies']}",
      platform: "{b64_assets['platform']}",
      bridge: "{b64_assets['bridge']}",
      block: "{b64_assets['block']}",
      slope: "{b64_assets['slope']}",
      torii: "{b64_assets['torii']}",
      lantern: "{b64_assets['lantern']}",
      chimes: "{b64_assets['chimes']}",
      spikes: "{b64_assets['spikes']}",
      shuriken: "{b64_assets['shuriken']}",
      orb: "{b64_assets['orb']}"
    }};

    const images = {{}};
    let assetsLoaded = 0;
    const totalAssets = Object.keys(assetSources).length;

    for (const [key, src] of Object.entries(assetSources)) {{
      const img = new Image();
      img.onload = () => {{
        assetsLoaded++;
        if (assetsLoaded === totalAssets) initGame();
      }};
      img.src = src;
      images[key] = img;
    }}

    // Canvas setup
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const LEVEL_WIDTH = 1024;
    const LEVEL_HEIGHT = 576;

    // Hitbox visualization state
    let showHitboxes = false;
    document.getElementById('toggleHitboxesBtn').addEventListener('click', () => {{
      showHitboxes = !showHitboxes;
      document.getElementById('hitboxStatus').textContent = showHitboxes ? 'ON' : 'OFF';
      document.getElementById('hitboxStatus').className = showHitboxes ? 'text-emerald-400 font-bold' : 'text-gray-400 font-bold';
    }});

    // Orientation toggle
    let isLandscape = true;
    document.getElementById('orientationBtn').addEventListener('click', () => {{
      isLandscape = !isLandscape;
      const frame = document.getElementById('phoneFrame');
      if (isLandscape) {{
        frame.style.width = '780px';
        frame.style.height = '430px';
      }} else {{
        frame.style.width = '390px';
        frame.style.height = '680px';
      }}
    }});

    // Clock
    function updateClock() {{
      const now = new Date();
      document.getElementById('clockText').textContent = 
        now.getHours().toString().padStart(2, '0') + ':' + 
        now.getMinutes().toString().padStart(2, '0');
    }}
    setInterval(updateClock, 1000);
    updateClock();

    // Physics parameters
    const PLAYER_SPEED = 180;      // 180 px/s
    const JUMP_IMPULSE = -420;     // -420 px/s
    const GRAVITY = 980;           // 980 px/s²

    // Player state
    const player = {{
      x: 140,
      y: 430,
      width: 56,
      height: 58,
      vx: 0,
      vy: 0,
      isOnGround: false,
      isFacingRight: true,
      isDropping: false,
      dropTimer: 0,
      angle: 0
    }};

    // Orbs & Score
    let score = 0;
    const spiritOrbs = [
      {{ x: 260, y: 340, collected: false }},
      {{ x: 480, y: 280, collected: false }},
      {{ x: 680, y: 310, collected: false }},
      {{ x: 880, y: 380, collected: false }}
    ];

    function resetPlayer() {{
      player.x = 140;
      player.y = 430;
      player.vx = 0;
      player.vy = 0;
      player.isOnGround = true;
      player.isFacingRight = true;
      player.isDropping = false;
      score = 0;
      for (const orb of spiritOrbs) orb.collected = false;
      document.getElementById('scoreText').textContent = '0 / 4';
    }}
    document.getElementById('resetBtn').addEventListener('click', resetPlayer);

    // Platforms & Solid Colliders
    // Solid ground
    const solidBlocks = [
      {{ x: 0, y: 440, w: 260, h: 136, type: 'ground' }},
      {{ x: 740, y: 440, w: 284, h: 136, type: 'ground' }},
      // Central stepping ground rock
      {{ x: 440, y: 450, w: 140, h: 126, type: 'ground' }}
    ];

    // Elevated one-way platforms
    const oneWayPlatforms = [
      // Left ground walk surface
      {{ x: 0, y: 440, w: 260, h: 14 }},
      // Center ground walk surface
      {{ x: 440, y: 450, w: 140, h: 14 }},
      // Right ground walk surface
      {{ x: 740, y: 440, w: 284, h: 14 }},

      // Elevated bamboo platform 1 (Left high)
      {{ x: 230, y: 360, w: 130, h: 12 }},
      // Log suspension bridge (spanning to center)
      {{ x: 340, y: 340, w: 120, h: 12 }},
      // Elevated bamboo platform 2 (Center high)
      {{ x: 570, y: 320, w: 140, h: 12 }},
      // Elevated bamboo platform 3 (Right mid)
      {{ x: 700, y: 380, w: 110, h: 12 }}
    ];

    // Hazards
    const hazards = [
      // Bamboo spikes in pit 1
      {{ x: 275, y: 490, w: 75, h: 80, type: 'spikes' }},
      // Bamboo spikes in pit 2
      {{ x: 645, y: 490, w: 75, h: 80, type: 'spikes' }},
      // Spinning shuriken patrolling vertically
      {{ x: 505, y: 310, w: 32, h: 32, type: 'shuriken', baseY: 310, speed: 2.5 }}
    ];

    // Floating fireflies particles simulation
    const ambientFireflies = [];
    for (let i = 0; i < 28; i++) {{
      ambientFireflies.push({{
        x: Math.random() * LEVEL_WIDTH,
        y: 100 + Math.random() * 400,
        radius: 1.5 + Math.random() * 2.5,
        speedX: (Math.random() - 0.5) * 20,
        speedY: (Math.random() - 0.5) * 15,
        phase: Math.random() * Math.PI * 2
      }});
    }}

    // Inputs
    const input = {{ left: false, right: false }};
    window.addEventListener('keydown', (e) => {{
      if (e.code === 'KeyA' || e.code === 'ArrowLeft') input.left = true;
      if (e.code === 'KeyD' || e.code === 'ArrowRight') input.right = true;
      
      const isDown = e.code === 'KeyS' || e.code === 'ArrowDown';
      const isJump = e.code === 'Space' || e.code === 'KeyW' || e.code === 'ArrowUp';

      if (isDown && isJump) {{
        triggerDrop();
      }} else if (isJump) {{
        triggerJump();
      }}
    }});

    window.addEventListener('keyup', (e) => {{
      if (e.code === 'KeyA' || e.code === 'ArrowLeft') input.left = false;
      if (e.code === 'KeyD' || e.code === 'ArrowRight') input.right = false;
    }});

    function setupTouchBtn(btnId, onStart, onEnd) {{
      const el = document.getElementById(btnId);
      const start = (e) => {{ e.preventDefault(); onStart(); }};
      const end = (e) => {{ e.preventDefault(); onEnd && onEnd(); }};
      el.addEventListener('mousedown', start);
      el.addEventListener('mouseup', end);
      el.addEventListener('mouseleave', end);
      el.addEventListener('touchstart', start, {{ passive: false }});
      el.addEventListener('touchend', end, {{ passive: false }});
      el.addEventListener('touchcancel', end, {{ passive: false }});
    }}

    setupTouchBtn('btnLeft', () => input.left = true, () => input.left = false);
    setupTouchBtn('btnRight', () => input.right = true, () => input.right = false);
    setupTouchBtn('btnJump', () => triggerJump());
    setupTouchBtn('btnDrop', () => triggerDrop());

    function triggerJump() {{
      if (player.isOnGround) {{
        player.vy = JUMP_IMPULSE;
        player.isOnGround = false;
      }}
    }}

    function triggerDrop() {{
      player.isDropping = true;
      player.dropTimer = 0.28;
      player.isOnGround = false;
    }}

    let cameraX = LEVEL_WIDTH / 2;
    let lastTime = performance.now();
    let frameCount = 0;
    let fpsTimer = 0;
    let shurikenAngle = 0;

    function initGame() {{
      requestAnimationFrame(gameLoop);
    }}

    function gameLoop(now) {{
      const dt = Math.min((now - lastTime) / 1000, 0.05);
      lastTime = now;

      frameCount++;
      fpsTimer += dt;
      if (fpsTimer >= 0.5) {{
        document.getElementById('fpsText').textContent = Math.round(frameCount / fpsTimer);
        frameCount = 0;
        fpsTimer = 0;
      }}

      shurikenAngle += dt * 8.0;

      update(dt);
      render(now);

      requestAnimationFrame(gameLoop);
    }}

    function update(dt) {{
      if (player.isDropping) {{
        player.dropTimer -= dt;
        if (player.dropTimer <= 0) player.isDropping = false;
      }}

      player.vx = 0;
      if (input.left) player.vx -= PLAYER_SPEED;
      if (input.right) player.vx += PLAYER_SPEED;

      if (player.vx > 0) player.isFacingRight = true;
      if (player.vx < 0) player.isFacingRight = false;

      player.vy += GRAVITY * dt;
      player.x += player.vx * dt;
      player.y += player.vy * dt;

      if (player.vy !== 0) player.isOnGround = false;

      const playerBottom = player.y;
      const playerLeft = player.x - player.width / 2 + 10;
      const playerRight = player.x + player.width / 2 - 10;

      // 1. One-way platforms collision
      if (player.vy >= 0 && !player.isDropping) {{
        for (const plat of oneWayPlatforms) {{
          if (playerRight >= plat.x && playerLeft <= plat.x + plat.w) {{
            if (playerBottom >= plat.y - 4 && playerBottom <= plat.y + 16) {{
              player.y = plat.y;
              player.vy = 0;
              player.isOnGround = true;
              break;
            }}
          }}
        }}
      }}

      // 2. Solid obstacle collision
      for (const block of solidBlocks) {{
        const bTop = block.y;
        const bBottom = block.y + block.h;
        const bLeft = block.x;
        const bRight = block.x + block.w;

        if (playerRight >= bLeft && playerLeft <= bRight) {{
          if (player.vy >= 0 && playerBottom >= bTop - 4 && playerBottom <= bTop + 16) {{
            player.y = bTop;
            player.vy = 0;
            player.isOnGround = true;
          }}
        }}

        if (playerBottom > bTop + 14 && playerBottom < bBottom + 30) {{
          if (player.vx > 0 && playerRight >= bLeft && playerLeft < bLeft) {{
            player.x = bLeft - (player.width / 2 - 10);
          }} else if (player.vx < 0 && playerLeft <= bRight && playerRight > bRight) {{
            player.x = bRight + (player.width / 2 - 10);
          }}
        }}
      }}

      // 3. Orbs collection
      for (const orb of spiritOrbs) {{
        if (!orb.collected) {{
          const dx = player.x - orb.x;
          const dy = (player.y - player.height / 2) - orb.y;
          if (Math.hypot(dx, dy) < 32) {{
            orb.collected = true;
            score++;
            document.getElementById('scoreText').textContent = score + ' / ' + spiritOrbs.length;
          }}
        }}
      }}

      // 4. Hazards collision
      for (const h of hazards) {{
        let hX = h.x;
        let hY = h.y;
        if (h.type === 'shuriken') {{
          hY = h.baseY + Math.sin(performance.now() / 400 * h.speed) * 45;
          h.currentY = hY;
        }}
        if (playerRight >= hX && playerLeft <= hX + h.w &&
            playerBottom >= hY && playerBottom - player.height <= hY + h.h) {{
          // Hit hazard! Respawn
          resetPlayer();
          break;
        }}
      }}

      // Ambient fireflies animation
      for (const ff of ambientFireflies) {{
        ff.x += ff.speedX * dt;
        ff.y += ff.speedY * dt;
        if (ff.x < 0) ff.x = LEVEL_WIDTH;
        if (ff.x > LEVEL_WIDTH) ff.x = 0;
        if (ff.y < 80) ff.y = 500;
        if (ff.y > 520) ff.y = 100;
      }}

      // Mid-air angle
      if (!player.isOnGround) {{
        player.angle = (player.vy < 0 ? -0.12 : 0.08) * (player.isFacingRight ? 1 : -1);
      }} else {{
        player.angle = 0;
      }}

      if (player.y > 600) resetPlayer();

      // Camera horizontal tracking with deadzone
      const deltaX = player.x - cameraX;
      const deadzone = 45;
      if (Math.abs(deltaX) > deadzone) {{
        cameraX += (deltaX - Math.sign(deltaX) * deadzone) * 4.5 * dt;
      }}
      cameraX = Math.max(LEVEL_WIDTH / 2 - 40, Math.min(LEVEL_WIDTH / 2 + 40, cameraX));

      document.getElementById('posText').textContent = `${{Math.round(player.x)}}, ${{Math.round(player.y)}}`;
    }}

    function render(now) {{
      ctx.clearRect(0, 0, LEVEL_WIDTH, LEVEL_HEIGHT);

      const offsetX = LEVEL_WIDTH / 2 - cameraX;

      // ==========================================
      // LAYER 1: SKY & SUNSET CELESTIAL (0.0x - Fixed horizon)
      // ==========================================
      if (images.sky) {{
        ctx.drawImage(images.sky, 0, 0, LEVEL_WIDTH, LEVEL_HEIGHT);
      }}

      // Camera-moved layers:
      ctx.save();
      ctx.translate(offsetX, 0);

      // ==========================================
      // LAYER 2: DISTANT MOUNTAINS & MIST (0.15x parallax)
      // ==========================================
      if (images.mountains) {{
        const p2X = (cameraX - LEVEL_WIDTH / 2) * 0.15;
        ctx.drawImage(images.mountains, -p2X, 0, LEVEL_WIDTH, LEVEL_HEIGHT);
      }}

      // ==========================================
      // LAYER 3: MIDGROUND BAMBOO GROVE (0.35x parallax)
      // ==========================================
      if (images.grove) {{
        const p3X = (cameraX - LEVEL_WIDTH / 2) * 0.35;
        ctx.drawImage(images.grove, -p3X, 60, LEVEL_WIDTH, LEVEL_HEIGHT - 60);
      }}

      // ==========================================
      // LAYER 4: GAMEPLAY WORLD & PLATFORMS (1.0x speed)
      // ==========================================
      
      // Autumn terrain ground blocks
      if (images.block) {{
        ctx.drawImage(images.block, 0, 440, 260, 136);
        ctx.drawImage(images.block, 440, 450, 140, 126);
        ctx.drawImage(images.block, 740, 440, 284, 136);
      }}

      // Grand Torii Gate at entrance (Left)
      if (images.torii) {{
        ctx.drawImage(images.torii, 40, 440 - 240, 180, 245);
      }}

      // Stone Toro Lanterns with warm flame flicker
      if (images.lantern) {{
        const glow1 = 12 + 3 * Math.sin(now / 180);
        drawToroGlow(ctx, 235, 410, glow1);
        ctx.drawImage(images.lantern, 215, 380, 40, 65);

        const glow2 = 12 + 3 * Math.sin((now + 600) / 190);
        drawToroGlow(ctx, 775, 410, glow2);
        ctx.drawImage(images.lantern, 755, 380, 40, 65);
      }}

      // Hanging Wind Chimes Furin on platforms
      if (images.chimes) {{
        ctx.drawImage(images.chimes, 240, 360, 32, 70);
        ctx.drawImage(images.chimes, 675, 320, 32, 70);
      }}

      // Elevated Bamboo Platforms
      if (images.platform) {{
        // High platform 1
        ctx.drawImage(images.platform, 230, 360, 130, 75);
        // High platform 2
        ctx.drawImage(images.platform, 570, 320, 140, 80);
        // Mid platform 3
        ctx.drawImage(images.platform, 700, 380, 110, 65);
      }}

      // Log suspension bridge
      if (images.bridge) {{
        ctx.drawImage(images.bridge, 340, 340, 120, 75);
      }}

      // Bamboo Spike Hazards
      if (images.spikes) {{
        ctx.drawImage(images.spikes, 275, 490, 75, 80);
        ctx.drawImage(images.spikes, 645, 490, 75, 80);
      }}

      // Spinning Shuriken Hazard
      if (images.shuriken) {{
        const sh = hazards[2];
        const sY = sh.currentY || 310;
        ctx.save();
        ctx.translate(sh.x + 16, sY + 16);
        ctx.rotate(shurikenAngle);
        ctx.drawImage(images.shuriken, -16, -16, 32, 32);
        ctx.restore();
      }}

      // Collectible Spirit Orbs
      if (images.orb) {{
        for (let i = 0; i < spiritOrbs.length; i++) {{
          const orb = spiritOrbs[i];
          if (!orb.collected) {{
            const bobY = orb.y + Math.sin((now + i * 800) / 250) * 4;
            // Draw orb outer warm halo
            const halo = ctx.createRadialGradient(orb.x, bobY, 2, orb.x, bobY, 18);
            halo.addColorStop(0, 'rgba(255, 215, 64, 0.7)');
            halo.addColorStop(1, 'rgba(255, 215, 64, 0)');
            ctx.fillStyle = halo;
            ctx.beginPath();
            ctx.arc(orb.x, bobY, 18, 0, Math.PI * 2);
            ctx.fill();

            ctx.drawImage(images.orb, orb.x - 12, bobY - 15, 24, 30);
          }}
        }}
      }}

      // Ninja Player Entity
      ctx.save();
      ctx.translate(player.x, player.y);
      ctx.rotate(player.angle);

      if (!player.isFacingRight) {{
        ctx.scale(-1, 1);
      }}

      if (images.ninja) {{
        ctx.drawImage(images.ninja, -player.width / 2, -player.height, player.width, player.height);
      }}
      ctx.restore();

      // ==========================================
      // LAYER 5: FOREGROUND BAMBOO & FIREFLIES (1.3x speed)
      // ==========================================
      if (images.fireflies) {{
        const p5X = (cameraX - LEVEL_WIDTH / 2) * 0.3;
        ctx.drawImage(images.fireflies, -p5X, 0, LEVEL_WIDTH, LEVEL_HEIGHT);
      }}

      // Dynamic ambient floating fireflies
      for (const ff of ambientFireflies) {{
        const alpha = 0.4 + 0.4 * Math.sin(now / 300 + ff.phase);
        ctx.fillStyle = `rgba(255, 215, 90, ${{alpha}})`;
        ctx.beginPath();
        ctx.arc(ff.x, ff.y, ff.radius, 0, Math.PI * 2);
        ctx.fill();
      }}

      // ==========================================
      // HITBOX DEBUG OVERLAY
      // ==========================================
      if (showHitboxes) {{
        // Solid blocks (Cyan)
        ctx.strokeStyle = '#00f7ff';
        ctx.lineWidth = 2;
        for (const block of solidBlocks) {{
          ctx.strokeRect(block.x, block.y, block.w, block.h);
        }}

        // One-way platforms (Emerald)
        ctx.strokeStyle = '#00ff88';
        ctx.lineWidth = 2.5;
        for (const plat of oneWayPlatforms) {{
          ctx.beginPath();
          ctx.moveTo(plat.x, plat.y);
          ctx.lineTo(plat.x + plat.w, plat.y);
          ctx.stroke();
        }}

        // Hazards (Red)
        ctx.strokeStyle = '#ff0044';
        ctx.lineWidth = 2;
        for (const h of hazards) {{
          const hy = h.type === 'shuriken' ? (h.currentY || 310) : h.y;
          ctx.strokeRect(h.x, hy, h.w, h.h);
        }}

        // Orbs (Yellow)
        ctx.strokeStyle = '#ffd700';
        for (const orb of spiritOrbs) {{
          if (!orb.collected) {{
            ctx.strokeRect(orb.x - 12, orb.y - 12, 24, 24);
          }}
        }}

        // Player hitbox (Amber/Pink)
        ctx.strokeStyle = player.isOnGround ? '#ffaa00' : '#ff3366';
        ctx.lineWidth = 2;
        ctx.strokeRect(player.x - player.width / 2 + 10, player.y - player.height + 8, player.width - 20, player.height - 10);
      }}

      ctx.restore();
    }}

    function drawToroGlow(c, x, y, r) {{
      const grad = c.createRadialGradient(x, y, 2, x, y, r);
      grad.addColorStop(0, 'rgba(255, 180, 40, 0.75)');
      grad.addColorStop(1, 'rgba(255, 180, 40, 0)');
      c.fillStyle = grad;
      c.beginPath();
      c.arc(x, y, r, 0, Math.PI * 2);
      c.fill();
    }}
  </script>
</body>
</html>'''

out_file = os.path.join(artifact_dir, "twilight_sanctuary_mobile_preview.html")
with open(out_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated standalone Twilight mobile preview artifact: {out_file} (size: {len(html_content)} bytes)")
