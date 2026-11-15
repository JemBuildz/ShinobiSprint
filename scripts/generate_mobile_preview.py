import base64
import os

images_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"
artifact_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b"
os.makedirs(artifact_dir, exist_ok=True)

assets = {
    "ninja": "character_ninja.png",
    "backdrop": "backdrop_bamboo.png",
    "pagoda": "prop_pagoda.png",
    "bridge": "prop_rope_bridge.png",
    "hut": "prop_hut_left.png",
    "dojo": "prop_dojo_right.png",
    "pillar": "prop_stone_pillar.png",
    "root_block": "prop_root_block.png",
}

b64_assets = {}
for key, filename in assets.items():
    p = os.path.join(images_dir, filename)
    if os.path.exists(p):
        with open(p, "rb") as f:
            b64_assets[key] = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
        print(f"Encoded {key}: {len(b64_assets[key])} chars")
    else:
        print(f"Missing {p}!")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bamboo Village 2D Platformer - Mobile Preview</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{
      user-select: none;
      -webkit-user-select: none;
      touch-action: manipulation;
    }}
    .phone-shadow {{
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7), 0 0 0 12px #1f2937, 0 0 0 14px #374151;
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
      transition: transform 0.08s ease, background-color 0.08s ease;
      touch-action: none;
    }}
    .ctrl-btn:active {{
      transform: scale(0.92);
      filter: brightness(1.2);
    }}
  </style>
</head>
<body class="bg-[#0b0f17] text-white min-h-screen flex flex-col items-center justify-center p-3 font-sans">

  <!-- Top Tool Header -->
  <header class="w-full max-w-4xl flex items-center justify-between mb-3 px-2">
    <div class="flex items-center gap-2">
      <span class="inline-block w-3 h-3 rounded-full bg-emerald-400 animate-pulse"></span>
      <h1 class="text-sm md:text-base font-semibold text-gray-200">Bamboo Village (Flame 1.18.0 Mobile Test)</h1>
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
    <div id="phoneFrame" class="phone-shadow relative bg-[#0e1a24] rounded-[36px] overflow-hidden border border-gray-700/50 flex flex-col" style="width: 780px; height: 430px;">
      
      <!-- Phone Top Status Bar -->
      <div class="w-full h-8 flex items-center justify-between px-6 text-[11px] font-mono text-gray-400 select-none z-40 bg-black/40 backdrop-blur-sm">
        <span id="clockText">9:41</span>
        <div class="dynamic-island"></div>
        <div class="flex items-center gap-2">
          <span>5G</span>
          <span class="inline-block w-4 h-2 border border-gray-400 rounded-sm p-[1px]"><span class="block w-full h-full bg-white rounded-xs"></span></span>
        </div>
      </div>

      <!-- Main Game Canvas Container -->
      <div class="relative flex-1 w-full h-full overflow-hidden bg-[#0e1a24]">
        <canvas id="gameCanvas" width="1024" height="576" class="w-full h-full object-contain"></canvas>

        <!-- On-Screen Virtual Controls Overlay (Mobile D-Pad & Action Buttons) -->
        <div class="absolute inset-0 pointer-events-none flex flex-col justify-between p-4 z-30">
          
          <!-- Top In-Game Bar -->
          <div class="flex items-center justify-between pointer-events-auto">
            <div class="bg-black/60 backdrop-blur px-3 py-1 rounded-full border border-white/10 text-[11px] text-gray-300 flex items-center gap-3 font-mono">
              <span>FPS: <b id="fpsText" class="text-emerald-400">60</b></span>
              <span>Vel: <b id="velText" class="text-amber-300">0, 0</b></span>
              <span>Pos: <b id="posText" class="text-cyan-300">210, 410</b></span>
            </div>
            <div class="bg-black/60 backdrop-blur px-3 py-1 rounded-full border border-white/10 text-[11px] text-amber-200">
              Bamboo Village
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
              <span>[A]/[D] Move</span>
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
    Replicating daytime bamboo village reference composition with Flame physics (<span class="text-amber-300">180px/s</span> speed, <span class="text-amber-300">-420px/s</span> jump, <span class="text-amber-300">980px/s²</span> gravity).
  </footer>

  <script>
    // Asset image cache
    const assetSources = {{
      ninja: "{b64_assets['ninja']}",
      backdrop: "{b64_assets['backdrop']}",
      pagoda: "{b64_assets['pagoda']}",
      bridge: "{b64_assets['bridge']}",
      hut: "{b64_assets['hut']}",
      dojo: "{b64_assets['dojo']}",
      pillar: "{b64_assets['pillar']}",
      root_block: "{b64_assets['root_block']}"
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

    // Clock updater
    function updateClock() {{
      const now = new Date();
      document.getElementById('clockText').textContent = 
        now.getHours().toString().padStart(2, '0') + ':' + 
        now.getMinutes().toString().padStart(2, '0');
    }}
    setInterval(updateClock, 1000);
    updateClock();

    // Game Physics Parameters (Flame Engine Spec)
    const PLAYER_SPEED = 180;      // 180 px/s
    const JUMP_IMPULSE = -420;     // -420 px/s
    const GRAVITY = 980;           // 980 px/s²

    // Player Entity state
    const player = {{
      x: 210,
      y: 410,
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

    // Reset player
    function resetPlayer() {{
      player.x = 210;
      player.y = 410;
      player.vx = 0;
      player.vy = 0;
      player.isOnGround = true;
      player.isFacingRight = true;
      player.isDropping = false;
    }}
    document.getElementById('resetBtn').addEventListener('click', resetPlayer);

    // Collision Platforms definitions
    // 1. Solid Ground root blocks & cliff ledges
    const solidBlocks = [
      {{ x: 0, y: 440, w: 310, h: 136, type: 'ground' }},
      {{ x: 714, y: 440, w: 310, h: 136, type: 'ground' }},
      // Bridge support stone pillars
      {{ x: 295, y: 418, w: 48, h: 120, type: 'pillar' }},
      {{ x: 680, y: 418, w: 48, h: 120, type: 'pillar' }},
      // Stepping river pillars
      {{ x: 430, y: 488, w: 46, h: 60, type: 'stepping' }},
      {{ x: 550, y: 496, w: 46, h: 52, type: 'stepping' }}
    ];

    // 2. One-Way Jump-Through Platforms
    const oneWayPlatforms = [
      // Left cliff top walk surface
      {{ x: 0, y: 420, w: 310, h: 16 }},
      // Right cliff top walk surface
      {{ x: 714, y: 420, w: 310, h: 16 }},
    ];

    // Arched Bridge catenary segments (10 segments following the rope sag)
    const bridgeX = 290;
    const bridgeY = 360;
    const bridgeW = 444;
    const bridgeH = 96;
    const bridgeSegments = 10;
    const segW = bridgeW / bridgeSegments;
    const sagRatios = [0.48, 0.54, 0.60, 0.64, 0.66, 0.66, 0.64, 0.60, 0.54, 0.48];

    for (let i = 0; i < bridgeSegments; i++) {{
      oneWayPlatforms.push({{
        x: bridgeX + i * segW,
        y: bridgeY + sagRatios[i] * bridgeH,
        w: segW,
        h: 12,
        isBridge: true
      }});
    }}

    // Input state
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

    // Touch controls handlers
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

    // Parallax scroll variable
    let parallaxScrollX = 0;
    let cameraX = LEVEL_WIDTH / 2;
    let lastTime = performance.now();
    let frameCount = 0;
    let fpsTimer = 0;

    function initGame() {{
      requestAnimationFrame(gameLoop);
    }}

    function gameLoop(now) {{
      const dt = Math.min((now - lastTime) / 1000, 0.05);
      lastTime = now;

      // Update FPS
      frameCount++;
      fpsTimer += dt;
      if (fpsTimer >= 0.5) {{
        document.getElementById('fpsText').textContent = Math.round(frameCount / fpsTimer);
        frameCount = 0;
        fpsTimer = 0;
      }}

      update(dt);
      render();

      requestAnimationFrame(gameLoop);
    }}

    function update(dt) {{
      // Drop through timer
      if (player.isDropping) {{
        player.dropTimer -= dt;
        if (player.dropTimer <= 0) player.isDropping = false;
      }}

      // Horizontal velocity
      player.vx = 0;
      if (input.left) player.vx -= PLAYER_SPEED;
      if (input.right) player.vx += PLAYER_SPEED;

      if (player.vx > 0) player.isFacingRight = true;
      if (player.vx < 0) player.isFacingRight = false;

      // Parallax update (0.2x player speed)
      parallaxScrollX += player.vx * 0.2 * dt;

      // Gravity
      player.vy += GRAVITY * dt;

      // Apply movement
      player.x += player.vx * dt;
      player.y += player.vy * dt;

      // Reset ground state before collision evaluation
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

      // 2. Solid obstacle collision (ground blocks & stone pillars)
      for (const block of solidBlocks) {{
        const bTop = block.y;
        const bBottom = block.y + block.h;
        const bLeft = block.x;
        const bRight = block.x + block.w;

        // Landing from above
        if (playerRight >= bLeft && playerLeft <= bRight) {{
          if (player.vy >= 0 && playerBottom >= bTop - 4 && playerBottom <= bTop + 16) {{
            player.y = bTop;
            player.vy = 0;
            player.isOnGround = true;
          }}
        }}

        // Side collision
        if (playerBottom > bTop + 14 && playerBottom < bBottom + 30) {{
          if (player.vx > 0 && playerRight >= bLeft && playerLeft < bLeft) {{
            player.x = bLeft - (player.width / 2 - 10);
          }} else if (player.vx < 0 && playerLeft <= bRight && playerRight > bRight) {{
            player.x = bRight + (player.width / 2 - 10);
          }}
        }}
      }}

      // Mid-air leaping angle
      if (!player.isOnGround) {{
        player.angle = (player.vy < 0 ? -0.12 : 0.08) * (player.isFacingRight ? 1 : -1);
      }} else {{
        player.angle = 0;
      }}

      // Pit floor safeguard
      if (player.y > 600) {{
        resetPlayer();
      }}

      // Camera horizontal deadzone
      const deltaX = player.x - cameraX;
      const deadzone = 45;
      if (Math.abs(deltaX) > deadzone) {{
        const shift = deltaX - Math.sign(deltaX) * deadzone;
        cameraX += shift * 4.5 * dt;
      }}
      cameraX = Math.max(LEVEL_WIDTH / 2 - 40, Math.min(LEVEL_WIDTH / 2 + 40, cameraX));

      // Update HUD telemetry
      document.getElementById('velText').textContent = `${{Math.round(player.vx)}}, ${{Math.round(player.vy)}}`;
      document.getElementById('posText').textContent = `${{Math.round(player.x)}}, ${{Math.round(player.y)}}`;
    }}

    function render() {{
      ctx.clearRect(0, 0, LEVEL_WIDTH, LEVEL_HEIGHT);

      // Camera transform offset
      const offsetX = LEVEL_WIDTH / 2 - cameraX;
      ctx.save();
      ctx.translate(offsetX, 0);

      // --- 1. Parallax Sky Base Layer ---
      const skyGrad = ctx.createLinearGradient(0, 0, 0, LEVEL_HEIGHT * 0.6);
      skyGrad.addColorStop(0, '#8ED2FF');
      skyGrad.addColorStop(1, '#D6EEFF');
      ctx.fillStyle = skyGrad;
      ctx.fillRect(-offsetX, 0, LEVEL_WIDTH, LEVEL_HEIGHT);

      // Sunbeams / radial warm glow
      const sunGrad = ctx.createRadialGradient(LEVEL_WIDTH * 0.5, LEVEL_HEIGHT * 0.2, 20, LEVEL_WIDTH * 0.5, LEVEL_HEIGHT * 0.2, LEVEL_WIDTH * 0.45);
      sunGrad.addColorStop(0, 'rgba(255, 243, 209, 0.35)');
      sunGrad.addColorStop(1, 'rgba(255, 255, 255, 0)');
      ctx.fillStyle = sunGrad;
      ctx.fillRect(-offsetX, 0, LEVEL_WIDTH, LEVEL_HEIGHT * 0.7);

      // Distant Mt. Fuji silhouette
      ctx.fillStyle = 'rgba(123, 150, 168, 0.45)';
      ctx.beginPath();
      ctx.moveTo(-offsetX, LEVEL_HEIGHT * 0.45);
      ctx.lineTo(LEVEL_WIDTH * 0.2, LEVEL_HEIGHT * 0.35);
      ctx.lineTo(LEVEL_WIDTH * 0.35, LEVEL_HEIGHT * 0.42);
      ctx.lineTo(LEVEL_WIDTH * 0.5, LEVEL_HEIGHT * 0.25);
      ctx.lineTo(LEVEL_WIDTH * 0.65, LEVEL_HEIGHT * 0.40);
      ctx.lineTo(LEVEL_WIDTH * 0.85, LEVEL_HEIGHT * 0.32);
      ctx.lineTo(LEVEL_WIDTH + offsetX, LEVEL_HEIGHT * 0.44);
      ctx.lineTo(LEVEL_WIDTH + offsetX, LEVEL_HEIGHT);
      ctx.lineTo(-offsetX, LEVEL_HEIGHT);
      ctx.closePath();
      ctx.fill();

      // --- 2. Backdrop Plate (Waterfalls, Cliffs, Scenic Plate) ---
      if (images.backdrop) {{
        ctx.drawImage(images.backdrop, 0, 0, LEVEL_WIDTH, LEVEL_HEIGHT);
      }}

      // --- 3. Parallax Bamboo Canopy (0.2x scrolling) ---
      const patternW = 320;
      const startX = -(parallaxScrollX % patternW) - patternW;
      ctx.fillStyle = 'rgba(54, 104, 53, 0.28)';
      ctx.strokeStyle = 'rgba(37, 74, 36, 0.35)';
      ctx.lineWidth = 5;

      for (let x = startX; x < LEVEL_WIDTH + patternW * 2; x += patternW) {{
        ctx.beginPath();
        ctx.moveTo(x + 40, 0); ctx.lineTo(x + 50, LEVEL_HEIGHT * 0.35);
        ctx.moveTo(x + 120, 0); ctx.lineTo(x + 115, LEVEL_HEIGHT * 0.38);
        ctx.moveTo(x + 220, 0); ctx.lineTo(x + 230, LEVEL_HEIGHT * 0.32);
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(x + 60, LEVEL_HEIGHT * 0.08, 45, 0, Math.PI * 2);
        ctx.arc(x + 140, LEVEL_HEIGHT * 0.06, 55, 0, Math.PI * 2);
        ctx.arc(x + 240, LEVEL_HEIGHT * 0.10, 40, 0, Math.PI * 2);
        ctx.fill();
      }}

      // --- 4. Midground Structures ---
      // Pagoda tower centered behind the bridge
      if (images.pagoda) {{
        ctx.drawImage(images.pagoda, 512 - 87, 395 - 345, 175, 345);
      }}

      // Glowing paper lanterns
      const nowMs = performance.now();
      drawLantern(ctx, 460, 220, nowMs);
      drawLantern(ctx, 564, 220, nowMs + 500);
      drawLantern(ctx, 300, 360, nowMs + 1000);
      drawLantern(ctx, 725, 360, nowMs + 1500);

      // --- 5. Bridge & Platforms ---
      // Stone support pillars
      if (images.pillar) {{
        ctx.drawImage(images.pillar, 295, 418, 48, 120);
        ctx.drawImage(images.pillar, 680, 418, 48, 120);
        ctx.drawImage(images.pillar, 430, 488, 46, 60);
        ctx.drawImage(images.pillar, 550, 496, 46, 52);
      }}

      // Arched wooden rope suspension bridge
      if (images.bridge) {{
        ctx.drawImage(images.bridge, bridgeX, bridgeY, bridgeW, bridgeH);
      }}

      // Ground Root blocks
      if (images.root_block) {{
        ctx.drawImage(images.root_block, 0, 440, 310, 136);
        ctx.drawImage(images.root_block, 714, 440, 310, 136);
      }}

      // --- 6. Ninja Player Entity ---
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

      // --- 7. Debug Hitbox Overlay ---
      if (showHitboxes) {{
        // Solid blocks (cyan)
        ctx.strokeStyle = '#00f7ff';
        ctx.lineWidth = 2;
        for (const block of solidBlocks) {{
          ctx.strokeRect(block.x, block.y, block.w, block.h);
        }}

        // One-way platforms (emerald green)
        ctx.strokeStyle = '#00ff88';
        ctx.lineWidth = 2.5;
        for (const plat of oneWayPlatforms) {{
          ctx.beginPath();
          ctx.moveTo(plat.x, plat.y);
          ctx.lineTo(plat.x + plat.w, plat.y);
          ctx.stroke();
        }}

        // Player hitbox (amber / red)
        ctx.strokeStyle = player.isOnGround ? '#ffaa00' : '#ff3366';
        ctx.lineWidth = 2;
        ctx.strokeRect(player.x - player.width / 2 + 10, player.y - player.height + 8, player.width - 20, player.height - 10);
      }}

      ctx.restore();
    }}

    function drawLantern(c, x, y, time) {{
      const glowR = 14 + 3 * Math.sin(time / 200);
      const radGrad = c.createRadialGradient(x, y, 2, x, y, glowR);
      radGrad.addColorStop(0, 'rgba(255, 170, 34, 0.7)');
      radGrad.addColorStop(1, 'rgba(255, 170, 34, 0)');
      c.fillStyle = radGrad;
      c.beginPath();
      c.arc(x, y, glowR, 0, Math.PI * 2);
      c.fill();

      c.fillStyle = '#ff9800';
      c.fillRect(x - 5, y - 8, 10, 16);
      c.fillStyle = '#3e2723';
      c.fillRect(x - 6, y - 10, 12, 3);
      c.fillRect(x - 6, y + 7, 12, 3);
    }}
  </script>
</body>
</html>'''

out_file = os.path.join(artifact_dir, "bamboo_village_mobile_preview.html")
with open(out_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated standalone mobile preview artifact: {out_file} (size: {len(html_content)} bytes)")
