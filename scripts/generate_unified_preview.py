import base64
import os

images_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"
artifact_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b"

assets = {
    "ninja": "character_ninja.png",
    "l2_sky": "level2_layer1_sky_sunset.png",
    "l2_mountains": "level2_layer2_distant_mountains.png",
    "l2_grove": "level2_layer3_midground_bamboo.png",
    "l2_foreground": "level2_layer5_foreground_blur.png",
    "l2_platform": "prop_bamboo_platform.png",
    "l2_bridge": "prop_log_bridge.png",
    "l2_raft": "prop_bamboo_raft.png",
    "l2_block": "prop_autumn_ground.png",
    "l2_torii": "prop_grand_torii.png",
    "l2_lantern": "prop_stone_lantern_toro.png",
    "l2_spikes": "prop_bamboo_spikes.png",
    "l2_shuriken": "prop_ninja_shuriken.png",
    "l2_orb": "prop_spirit_orb_clean.png",
    "l1_bg": "backdrop_bamboo.png",
    "l1_pagoda": "prop_pagoda.png",
    "l1_bridge": "prop_rope_bridge.png",
    "l1_root": "prop_root_block.png",
    "l1_pillar": "prop_stone_pillar.png",
}

b64_assets = {}
for key, filename in assets.items():
    p = os.path.join(images_dir, filename)
    if os.path.exists(p):
        with open(p, "rb") as f:
            b64_assets[key] = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
        print(f"Loaded {key}: {len(b64_assets[key])} chars")
    else:
        print(f"Missing {p}!")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Level 2: Twilight Bamboo Sanctuary - Web Preview</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {{
      user-select: none;
      -webkit-user-select: none;
      touch-action: manipulation;
    }}
    .phone-shadow {{
      box-shadow: 0 30px 70px -15px rgba(0, 0, 0, 0.85), 0 0 0 12px #141b26, 0 0 0 14px #263244;
    }}
    .dynamic-island {{
      width: 90px;
      height: 24px;
      background: #000;
      border-radius: 20px;
    }}
    .ctrl-btn {{
      transition: all 0.08s cubic-bezier(0.2, 0.8, 0.2, 1);
    }}
    .ctrl-btn:active, .ctrl-btn.active {{
      transform: scale(0.92);
      filter: brightness(1.3);
    }}
    canvas {{
      image-rendering: auto;
    }}
    .toast {{
      animation: fadeInOut 2.5s forwards ease-in-out;
    }}
    @keyframes fadeInOut {{
      0% {{ opacity: 0; transform: translateY(10px); }}
      15% {{ opacity: 1; transform: translateY(0); }}
      85% {{ opacity: 1; transform: translateY(0); }}
      100% {{ opacity: 0; transform: translateY(-10px); }}
    }}
  </style>
</head>
<body class="bg-[#070a10] text-white min-h-screen flex flex-col items-center justify-center p-3 font-sans">

  <!-- Top Tool Header -->
  <header class="w-full max-w-4xl flex items-center justify-between mb-3 px-2">
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-2">
        <span class="inline-block w-3 h-3 rounded-full bg-amber-400 animate-pulse"></span>
        <h1 class="text-sm md:text-base font-semibold text-amber-100" id="stageTitle">Level 2: Twilight Sanctuary</h1>
      </div>
      <!-- Level Switcher -->
      <div class="bg-gray-900 border border-gray-700 rounded-lg p-0.5 flex text-xs">
        <button id="lvl2Btn" class="px-2.5 py-1 rounded font-medium bg-amber-600 text-white transition">Level 2 (Twilight)</button>
        <button id="lvl1Btn" class="px-2.5 py-1 rounded font-medium text-gray-400 hover:text-white transition">Level 1 (Daytime)</button>
      </div>
    </div>
    
    <div class="flex items-center gap-2 text-xs">
      <!-- Edit Mode Toggle -->
      <button id="editModeBtn" class="px-2.5 py-1 rounded bg-indigo-700 hover:bg-indigo-600 text-white font-medium transition flex items-center gap-1 shadow-sm">
        <span id="editIcon">🛠️</span> <span id="editStatus">Edit Layout</span>
      </button>
      <button id="exportLayoutBtn" class="hidden px-2.5 py-1 rounded bg-emerald-600 hover:bg-emerald-500 text-white font-medium transition flex items-center gap-1 shadow-sm">
        📋 Copy Coordinates
      </button>

      <button id="soundBtn" class="px-2.5 py-1 rounded bg-gray-800 hover:bg-gray-700 border border-gray-600 text-gray-300 font-medium transition flex items-center gap-1">
        <span id="soundIcon">🔊</span> <span id="soundStatus">SFX ON</span>
      </button>
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
    <div id="phoneFrame" class="phone-shadow relative bg-[#0b0f17] rounded-[36px] overflow-hidden border border-gray-700/50 flex flex-col" style="width: 780px; height: 430px;">
      
      <!-- Phone Top Status Bar -->
      <div class="w-full h-8 flex items-center justify-between px-6 text-[11px] font-mono text-gray-400 select-none z-40 bg-black/40 backdrop-blur-sm">
        <span id="clockText">19:15</span>
        <div class="dynamic-island"></div>
        <div class="flex items-center gap-2">
          <span>5G</span>
          <span class="inline-block w-4 h-2 border border-gray-400 rounded-sm p-[1px]"><span class="block w-full h-full bg-amber-400 rounded-xs"></span></span>
        </div>
      </div>

      <!-- Main Game Canvas Container -->
      <div class="relative flex-1 w-full h-full overflow-hidden bg-[#0a0e16]" id="canvasContainer" tabindex="0">
        <canvas id="gameCanvas" width="1024" height="576" class="w-full h-full object-contain cursor-pointer"></canvas>

        <!-- Toast Notification -->
        <div id="toast" class="hidden absolute top-14 left-1/2 -translate-x-1/2 bg-emerald-600/90 text-white px-4 py-1.5 rounded-full text-xs font-semibold backdrop-blur shadow-xl z-50 pointer-events-none toast">
          Coordinates copied to clipboard!
        </div>

        <!-- Edit Mode Banner -->
        <div id="editBanner" class="hidden absolute top-12 left-4 right-4 bg-indigo-900/80 border border-indigo-500/40 backdrop-blur-md px-3.5 py-1.5 rounded-xl text-xs flex items-center justify-between z-30 shadow-xl pointer-events-auto">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-indigo-400 animate-ping"></span>
            <span class="text-indigo-200 font-medium">🎯 <b>Edit Mode:</b> Click & drag any platform, Torii gate, lantern, or hazard to place it.</span>
          </div>
          <div id="selectionInfo" class="font-mono text-[11px] text-amber-300 bg-black/40 px-2 py-0.5 rounded">
            Click an object to select & move
          </div>
        </div>

        <!-- On-Screen Virtual Controls Overlay -->
        <div id="controlsOverlay" class="absolute inset-0 pointer-events-none flex flex-col justify-between p-4 z-30">
          
          <!-- Top In-Game Bar -->
          <div class="flex items-center justify-between pointer-events-auto">
            <div class="bg-black/60 backdrop-blur px-3 py-1 rounded-full border border-white/10 text-[11px] text-gray-300 flex items-center gap-3 font-mono">
              <span>FPS: <b id="fpsText" class="text-emerald-400">60</b></span>
              <span id="scoreDisplay">Orbs: <b id="scoreText" class="text-amber-400">0 / 4</b></span>
              <span>Pos: <b id="posText" class="text-cyan-300">130, 440</b></span>
            </div>
            <div id="envPill" class="bg-black/60 backdrop-blur px-3 py-1 rounded-full border border-amber-400/30 text-[11px] text-amber-300 flex items-center gap-1.5">
              <span>🏮</span>
              <span id="envName">Twilight Sanctuary</span>
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

            <!-- Controls Pill -->
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
    </div>
  </main>

  <!-- Interactive Controls Guide -->
  <footer class="mt-3 text-center text-gray-400 text-xs flex flex-wrap items-center justify-center gap-4">
    <div class="flex items-center gap-1.5">
      <span class="px-1.5 py-0.5 rounded bg-gray-800 border border-gray-700 text-gray-200 font-mono">A</span>
      <span class="px-1.5 py-0.5 rounded bg-gray-800 border border-gray-700 text-gray-200 font-mono">D</span>
      <span>or Arrow keys to Run (180 px/s)</span>
    </div>
    <div class="flex items-center gap-1.5">
      <span class="px-1.5 py-0.5 rounded bg-gray-800 border border-gray-700 text-gray-200 font-mono">Space</span>
      <span>Jump (-420 px/s)</span>
    </div>
    <div class="flex items-center gap-1.5">
      <span class="px-1.5 py-0.5 rounded bg-gray-800 border border-gray-700 text-gray-200 font-mono">S + Space</span>
      <span>Drop through bridges</span>
    </div>
  </footer>

  <script>
    // Web Audio Synthesizer
    let audioCtx = null;
    let soundEnabled = true;

    function getAudioContext() {{
      if (!audioCtx) {{
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }}
      if (audioCtx.state === 'suspended') {{
        audioCtx.resume();
      }}
      return audioCtx;
    }}

    function playSound(type) {{
      if (!soundEnabled) return;
      try {{
        const ctx = getAudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        const t = ctx.currentTime;

        if (type === 'jump') {{
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(260, t);
          osc.frequency.exponentialRampToValueAtTime(540, t + 0.12);
          gain.gain.setValueAtTime(0.2, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.12);
          osc.start(t);
          osc.stop(t + 0.12);
        }} else if (type === 'land') {{
          osc.type = 'sine';
          osc.frequency.setValueAtTime(110, t);
          osc.frequency.exponentialRampToValueAtTime(50, t + 0.07);
          gain.gain.setValueAtTime(0.25, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.07);
          osc.start(t);
          osc.stop(t + 0.07);
        }} else if (type === 'orb') {{
          osc.type = 'sine';
          osc.frequency.setValueAtTime(580, t);
          osc.frequency.setValueAtTime(880, t + 0.04);
          gain.gain.setValueAtTime(0.25, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.15);
          osc.start(t);
          osc.stop(t + 0.15);
        }} else if (type === 'hit') {{
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(160, t);
          osc.frequency.exponentialRampToValueAtTime(50, t + 0.22);
          gain.gain.setValueAtTime(0.25, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.22);
          osc.start(t);
          osc.stop(t + 0.22);
        }}
      }} catch (e) {{}}
    }}

    document.getElementById('soundBtn').addEventListener('click', () => {{
      soundEnabled = !soundEnabled;
      document.getElementById('soundIcon').textContent = soundEnabled ? '🔊' : '🔇';
      document.getElementById('soundStatus').textContent = soundEnabled ? 'SFX ON' : 'SFX OFF';
    }});

    const assetSources = {{
      ninja: "{b64_assets['ninja']}",
      l2_sky: "{b64_assets['l2_sky']}",
      l2_mountains: "{b64_assets['l2_mountains']}",
      l2_grove: "{b64_assets['l2_grove']}",
      l2_foreground: "{b64_assets['l2_foreground']}",
      l2_platform: "{b64_assets['l2_platform']}",
      l2_bridge: "{b64_assets['l2_bridge']}",
      l2_raft: "{b64_assets['l2_raft']}",
      l2_block: "{b64_assets['l2_block']}",
      l2_torii: "{b64_assets['l2_torii']}",
      l2_lantern: "{b64_assets['l2_lantern']}",
      l2_spikes: "{b64_assets['l2_spikes']}",
      l2_shuriken: "{b64_assets['l2_shuriken']}",
      l2_orb: "{b64_assets['l2_orb']}",
      l1_bg: "{b64_assets['l1_bg']}",
      l1_pagoda: "{b64_assets['l1_pagoda']}",
      l1_bridge: "{b64_assets['l1_bridge']}",
      l1_root: "{b64_assets['l1_root']}",
      l1_pillar: "{b64_assets['l1_pillar']}"
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

    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const LEVEL_WIDTH = 1024;
    const LEVEL_HEIGHT = 576;

    let currentLevel = 2; // Default to Level 2 (Twilight Sanctuary)

    // Level Switcher Buttons
    document.getElementById('lvl1Btn').addEventListener('click', () => setLevel(1));
    document.getElementById('lvl2Btn').addEventListener('click', () => setLevel(2));

    function setLevel(lvl) {{
      currentLevel = lvl;
      if (lvl === 1) {{
        document.getElementById('lvl1Btn').className = 'px-2.5 py-1 rounded font-medium bg-amber-600 text-white transition';
        document.getElementById('lvl2Btn').className = 'px-2.5 py-1 rounded font-medium text-gray-400 hover:text-white transition';
        document.getElementById('stageTitle').textContent = 'Level 1: Daytime Bamboo Village';
        document.getElementById('envName').textContent = 'Daytime Village';
        document.getElementById('scoreDisplay').style.display = 'none';
      }} else {{
        document.getElementById('lvl2Btn').className = 'px-2.5 py-1 rounded font-medium bg-amber-600 text-white transition';
        document.getElementById('lvl1Btn').className = 'px-2.5 py-1 rounded font-medium text-gray-400 hover:text-white transition';
        document.getElementById('stageTitle').textContent = 'Level 2: Twilight Sanctuary';
        document.getElementById('envName').textContent = 'Twilight Sanctuary';
        document.getElementById('scoreDisplay').style.display = 'inline';
      }}
      resetPlayer();
    }}

    // Hitbox visualization
    let showHitboxes = false;
    document.getElementById('toggleHitboxesBtn').addEventListener('click', () => {{
      showHitboxes = !showHitboxes;
      document.getElementById('hitboxStatus').textContent = showHitboxes ? 'ON' : 'OFF';
      document.getElementById('hitboxStatus').className = showHitboxes ? 'text-emerald-400 font-bold' : 'text-gray-400 font-bold';
    }});

    // Phone orientation
    let isLandscape = true;
    document.getElementById('orientationBtn').addEventListener('click', () => {{
      isLandscape = !isLandscape;
      const frame = document.getElementById('phoneFrame');
      if (isLandscape) {{
        frame.style.width = '780px';
        frame.style.height = '430px';
      }} else {{
        frame.style.width = '420px';
        frame.style.height = '680px';
      }}
    }});

    // Exact Flame physics parameters:
    const PLAYER_SPEED = 180;
    const JUMP_IMPULSE = -420;
    const GRAVITY = 980;

    const player = {{
      x: 130,
      y: 440,
      width: 56,
      height: 58,
      vx: 0,
      vy: 0,
      isOnGround: true,
      isFacingRight: true,
      isDropping: false,
      dropTimer: 0,
      angle: 0,
      wasOnGround: false
    }};

    // Level 2 Interactive Layout Objects (Draggable in Edit Mode)
    const stageObjects = [
      {{ id: 'torii', name: 'Grand Torii Gate', x: 45, y: 248, w: 150, h: 195, type: 'prop' }},
      {{ id: 'lantern_l', name: 'Left Lantern', x: 215, y: 378, w: 44, h: 62, type: 'prop' }},
      {{ id: 'bridge1', name: 'Bridge 1', x: 286, y: 435, w: 184, h: 80, type: 'platform' }},
      {{ id: 'platform', name: 'Center Platform', x: 470, y: 415, w: 164, h: 85, type: 'platform' }},
      {{ id: 'bridge2', name: 'Bridge 2', x: 634, y: 435, w: 165, h: 80, type: 'platform' }},
      {{ id: 'lantern_r', name: 'Right Lantern', x: 810, y: 378, w: 44, h: 62, type: 'prop' }},
      {{ id: 'spikes1', name: 'Spikes Left', x: 310, y: 530, w: 135, h: 46, type: 'hazard' }},
      {{ id: 'spikes2', name: 'Spikes Right', x: 650, y: 530, w: 135, h: 46, type: 'hazard' }},
      {{ id: 'shuriken', name: 'Shuriken', x: 550, y: 280, w: 36, h: 36, type: 'hazard', baseY: 280, speed: 2.2 }},
      {{ id: 'orb1', name: 'Spirit Orb 1', x: 375, y: 360, w: 24, h: 24, type: 'orb', collected: false }},
      {{ id: 'orb2', name: 'Spirit Orb 2', x: 550, y: 330, w: 24, h: 24, type: 'orb', collected: false }},
      {{ id: 'orb3', name: 'Spirit Orb 3', x: 715, y: 360, w: 24, h: 24, type: 'orb', collected: false }},
      {{ id: 'orb4', name: 'Spirit Orb 4', x: 910, y: 380, w: 24, h: 24, type: 'orb', collected: false }}
    ];

    // Colliders definitions for Level 2 (Generated dynamically from stageObjects)
    function getL2SolidBlocks() {{
      return [
        {{ x: 0, y: 440, w: 286, h: 136, type: 'ground' }},
        {{ x: 799, y: 440, w: 225, h: 136, type: 'ground' }}
      ];
    }}

    function getL2OneWayPlatforms() {{
      const b1 = stageObjects.find(o => o.id === 'bridge1');
      const cp = stageObjects.find(o => o.id === 'platform');
      const b2 = stageObjects.find(o => o.id === 'bridge2');
      return [
        {{ x: 0, y: 440, w: 286, h: 16 }},
        {{ x: 799, y: 440, w: 225, h: 16 }},
        {{ x: b1.x, y: b1.y, w: b1.w, h: 16 }},
        {{ x: cp.x, y: cp.y, w: cp.w, h: 16 }},
        {{ x: b2.x, y: b2.y, w: b2.w, h: 16 }}
      ];
    }}

    function getL2Hazards() {{
      const s1 = stageObjects.find(o => o.id === 'spikes1');
      const s2 = stageObjects.find(o => o.id === 'spikes2');
      const sh = stageObjects.find(o => o.id === 'shuriken');
      return [
        {{ x: s1.x, y: s1.y, w: s1.w, h: s1.h, type: 'spikes' }},
        {{ x: s2.x, y: s2.y, w: s2.w, h: s2.h, type: 'spikes' }},
        {{ x: sh.x, y: sh.y, w: sh.w, h: sh.h, type: 'shuriken', baseY: sh.baseY || sh.y, speed: 2.2 }}
      ];
    }}

    let score = 0;

    function resetPlayer() {{
      if (currentLevel === 2) {{
        player.x = 130;
        player.y = 440;
      }} else {{
        player.x = 210;
        player.y = 410;
      }}
      player.vx = 0;
      player.vy = 0;
      player.isOnGround = true;
      player.isFacingRight = true;
      player.isDropping = false;
      score = 0;
      for (const obj of stageObjects) {{
        if (obj.type === 'orb') obj.collected = false;
      }}
      document.getElementById('scoreText').textContent = '0 / 4';
    }}
    document.getElementById('resetBtn').addEventListener('click', resetPlayer);

    // Colliders definitions for Level 1 (Daytime Bamboo Village)
    const l1_solidBlocks = [
      {{ x: 0, y: 440, w: 310, h: 136, type: 'ground' }},
      {{ x: 714, y: 440, w: 310, h: 136, type: 'ground' }},
      {{ x: 295, y: 418, w: 48, h: 120, type: 'pillar' }},
      {{ x: 680, y: 418, w: 48, h: 120, type: 'pillar' }},
      {{ x: 430, y: 488, w: 46, h: 60, type: 'stepping' }},
      {{ x: 550, y: 496, w: 46, h: 52, type: 'stepping' }}
    ];

    const l1_oneWayPlatforms = [
      {{ x: 0, y: 420, w: 310, h: 16 }},
      {{ x: 714, y: 420, w: 310, h: 16 }}
    ];
    for (let i = 0; i < 10; i++) {{
      const sY = [0.48, 0.54, 0.60, 0.64, 0.66, 0.66, 0.64, 0.60, 0.54, 0.48][i];
      l1_oneWayPlatforms.push({{
        x: 290 + i * 44.4,
        y: 360 + sY * 96,
        w: 44.4,
        h: 12
      }});
    }}

    // Ambient floating fireflies
    const ambientFireflies = [];
    for (let i = 0; i < 30; i++) {{
      ambientFireflies.push({{
        x: Math.random() * LEVEL_WIDTH,
        y: 80 + Math.random() * 420,
        radius: 1.5 + Math.random() * 2.5,
        speedX: (Math.random() - 0.5) * 18,
        speedY: (Math.random() - 0.5) * 12,
        phase: Math.random() * Math.PI * 2
      }});
    }}

    // Flame Parallax scroll state (accumulated offsets per layer)
    const parallaxOffsets = [0, 0, 0, 0];
    const BASE_VELOCITY = 20; // 20 px/s
    const MULTIPLIER_DELTA = 1.8;

    // Level Editor Interactive State
    let isEditMode = false;
    let selectedObject = null;
    let dragOffsetX = 0;
    let dragOffsetY = 0;

    const editBtn = document.getElementById('editModeBtn');
    const exportBtn = document.getElementById('exportLayoutBtn');
    const editBanner = document.getElementById('editBanner');
    const selectionInfo = document.getElementById('selectionInfo');

    editBtn.addEventListener('click', () => {{
      isEditMode = !isEditMode;
      if (isEditMode) {{
        editBtn.className = 'px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white font-medium transition flex items-center gap-1 shadow-sm';
        document.getElementById('editStatus').textContent = 'Play Test';
        document.getElementById('editIcon').textContent = '▶️';
        exportBtn.classList.remove('hidden');
        editBanner.classList.remove('hidden');
        document.getElementById('controlsOverlay').classList.add('pointer-events-none');
      }} else {{
        editBtn.className = 'px-2.5 py-1 rounded bg-indigo-700 hover:bg-indigo-600 text-white font-medium transition flex items-center gap-1 shadow-sm';
        document.getElementById('editStatus').textContent = 'Edit Layout';
        document.getElementById('editIcon').textContent = '🛠️';
        exportBtn.classList.add('hidden');
        editBanner.classList.add('hidden');
        selectedObject = null;
        resetPlayer();
      }}
    }});

    exportBtn.addEventListener('click', () => {{
      const layoutData = stageObjects.map(o => ({{
        id: o.id,
        name: o.name,
        x: Math.round(o.x),
        y: Math.round(o.y),
        width: o.w,
        height: o.h
      }}));
      const jsonStr = JSON.stringify(layoutData, null, 2);
      navigator.clipboard.writeText(jsonStr).then(() => {{
        const toast = document.getElementById('toast');
        toast.classList.remove('hidden');
        setTimeout(() => toast.classList.add('hidden'), 2500);
      }});
    }});

    function getCanvasCoords(e) {{
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      return {{
        x: (clientX - rect.left) * scaleX,
        y: (clientY - rect.top) * scaleY
      }};
    }}

    function onPointerDown(e) {{
      if (!isEditMode || currentLevel !== 2) return;
      const pt = getCanvasCoords(e);
      // Check objects in reverse render order
      for (let i = stageObjects.length - 1; i >= 0; i--) {{
        const o = stageObjects[i];
        if (pt.x >= o.x && pt.x <= o.x + o.w && pt.y >= o.y && pt.y <= o.y + o.h) {{
          selectedObject = o;
          dragOffsetX = pt.x - o.x;
          dragOffsetY = pt.y - o.y;
          selectionInfo.textContent = `${{o.name}}: X=${{Math.round(o.x)}}, Y=${{Math.round(o.y)}}`;
          break;
        }}
      }}
    }}

    function onPointerMove(e) {{
      if (!isEditMode || currentLevel !== 2) return;
      if (selectedObject) {{
        const pt = getCanvasCoords(e);
        selectedObject.x = Math.round(pt.x - dragOffsetX);
        selectedObject.y = Math.round(pt.y - dragOffsetY);
        if (selectedObject.id === 'shuriken') {{
          selectedObject.baseY = selectedObject.y;
        }}
        selectionInfo.textContent = `${{selectedObject.name}}: X=${{selectedObject.x}}, Y=${{selectedObject.y}}`;
      }}
    }}

    function onPointerUp() {{
      selectedObject = null;
    }}

    canvas.addEventListener('mousedown', onPointerDown);
    window.addEventListener('mousemove', onPointerMove);
    window.addEventListener('mouseup', onPointerUp);

    canvas.addEventListener('touchstart', onPointerDown, {{ passive: false }});
    window.addEventListener('touchmove', onPointerMove, {{ passive: false }});
    window.addEventListener('touchend', onPointerUp, {{ passive: false }});

    // Keyboard Controls
    const input = {{ left: false, right: false }};
    window.addEventListener('keydown', (e) => {{
      if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'KeyA', 'KeyD', 'KeyW', 'KeyS'].includes(e.code)) {{
        e.preventDefault();
      }}
      if (e.code === 'KeyA' || e.code === 'ArrowLeft') {{
        input.left = true;
        document.getElementById('btnLeft').classList.add('active');
      }}
      if (e.code === 'KeyD' || e.code === 'ArrowRight') {{
        input.right = true;
        document.getElementById('btnRight').classList.add('active');
      }}
      const isDrop = (e.code === 'KeyS' || e.code === 'ArrowDown') && (e.code === 'Space' || input.jumpHeld);
      const isJump = e.code === 'Space' || e.code === 'KeyW' || e.code === 'ArrowUp';
      if (e.code === 'KeyS' || e.code === 'ArrowDown') {{
        document.getElementById('btnDrop').classList.add('active');
      }}
      if (isDrop) {{
        triggerDrop();
      }} else if (isJump) {{
        triggerJump();
        document.getElementById('btnJump').classList.add('active');
      }}
    }});

    window.addEventListener('keyup', (e) => {{
      if (e.code === 'KeyA' || e.code === 'ArrowLeft') {{
        input.left = false;
        document.getElementById('btnLeft').classList.remove('active');
      }}
      if (e.code === 'KeyD' || e.code === 'ArrowRight') {{
        input.right = false;
        document.getElementById('btnRight').classList.remove('active');
      }}
      if (e.code === 'Space' || e.code === 'KeyW' || e.code === 'ArrowUp') {{
        document.getElementById('btnJump').classList.remove('active');
      }}
      if (e.code === 'KeyS' || e.code === 'ArrowDown') {{
        document.getElementById('btnDrop').classList.remove('active');
      }}
    }});

    function setupTouchBtn(btnId, onStart, onEnd) {{
      const el = document.getElementById(btnId);
      const start = (e) => {{
        e.preventDefault();
        el.classList.add('active');
        onStart();
      }};
      const end = (e) => {{
        e.preventDefault();
        el.classList.remove('active');
        onEnd && onEnd();
      }};
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
      if (isEditMode) return;
      if (player.isOnGround) {{
        player.vy = JUMP_IMPULSE;
        player.isOnGround = false;
        playSound('jump');
      }}
    }}

    function triggerDrop() {{
      if (isEditMode) return;
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

      if (!isEditMode) {{
        update(dt);
      }}
      render(now);

      requestAnimationFrame(gameLoop);
    }}

    function update(dt) {{
      player.wasOnGround = player.isOnGround;

      if (player.isDropping) {{
        player.dropTimer -= dt;
        if (player.dropTimer <= 0) player.isDropping = false;
      }}

      player.vx = 0;
      if (input.left) player.vx -= PLAYER_SPEED;
      if (input.right) player.vx += PLAYER_SPEED;

      if (player.vx > 0) player.isFacingRight = true;
      if (player.vx < 0) player.isFacingRight = false;

      // Update Flame Parallax scroll offsets
      const effectiveBaseVel = BASE_VELOCITY + player.vx * 0.35;
      for (let i = 0; i < 4; i++) {{
        const layerSpeed = effectiveBaseVel * Math.pow(MULTIPLIER_DELTA, i);
        parallaxOffsets[i] = (parallaxOffsets[i] + layerSpeed * dt) % LEVEL_WIDTH;
        if (parallaxOffsets[i] < 0) parallaxOffsets[i] += LEVEL_WIDTH;
      }}

      player.vy += GRAVITY * dt;
      player.x += player.vx * dt;
      player.y += player.vy * dt;

      if (player.vy !== 0) player.isOnGround = false;

      const playerBottom = player.y;
      const playerLeft = player.x - player.width / 2 + 10;
      const playerRight = player.x + player.width / 2 - 10;

      const solidBlocks = currentLevel === 2 ? getL2SolidBlocks() : l1_solidBlocks;
      const oneWayPlatforms = currentLevel === 2 ? getL2OneWayPlatforms() : l1_oneWayPlatforms;
      const hazards = currentLevel === 2 ? getL2Hazards() : [];

      // 1. One-way platforms
      if (player.vy >= 0 && !player.isDropping) {{
        for (const plat of oneWayPlatforms) {{
          if (playerRight >= plat.x && playerLeft <= plat.x + plat.w) {{
            if (playerBottom >= plat.y - 4 && playerBottom <= plat.y + 16) {{
              player.y = plat.y;
              player.vy = 0;
              player.isOnGround = true;
              if (!player.wasOnGround) playSound('land');
              break;
            }}
          }}
        }}
      }}

      // 2. Solid blocks
      for (const block of solidBlocks) {{
        const bTop = block.y;
        const bBottom = block.y + block.h;
        const bLeft = block.x;
        const bRight = block.x + block.w;

        if (playerRight >= bLeft && playerLeft <= bRight) {{
          if (player.y - player.height < bBottom && player.y > bTop) {{
            // Side collision
            if (player.vx > 0 && player.x < bLeft) {{
              player.x = bLeft - player.width / 2 + 10;
              player.vx = 0;
            }} else if (player.vx < 0 && player.x > bRight) {{
              player.x = bRight + player.width / 2 - 10;
              player.vx = 0;
            }}
          }}
        }}
      }}

      // Level 2 Collectibles & Hazards
      if (currentLevel === 2) {{
        for (const obj of stageObjects) {{
          if (obj.type === 'orb' && !obj.collected) {{
            const dist = Math.hypot(player.x - obj.x, (player.y - player.height / 2) - obj.y);
            if (dist < 38) {{
              obj.collected = true;
              score++;
              document.getElementById('scoreText').textContent = `${{score}} / 4`;
              playSound('orb');
            }}
          }}
        }}

        for (const h of hazards) {{
          let hX = h.x;
          let hY = h.y;
          if (h.type === 'shuriken') {{
            hY = h.baseY + Math.sin(performance.now() / 400 * h.speed) * 45;
            h.currentY = hY;
          }}
          if (playerRight >= hX && playerLeft <= hX + h.w &&
              playerBottom >= hY && playerBottom - player.height <= hY + h.h) {{
            playSound('hit');
            resetPlayer();
            break;
          }}
        }}
      }}

      // Fireflies
      for (const ff of ambientFireflies) {{
        ff.x += ff.speedX * dt;
        ff.y += ff.speedY * dt;
        if (ff.x < 0) ff.x = LEVEL_WIDTH;
        if (ff.x > LEVEL_WIDTH) ff.x = 0;
        if (ff.y < 80) ff.y = 500;
        if (ff.y > 520) ff.y = 100;
      }}

      if (!player.isOnGround) {{
        player.angle = (player.vy < 0 ? -0.12 : 0.08) * (player.isFacingRight ? 1 : -1);
      }} else {{
        player.angle = 0;
      }}

      if (player.y > 600) {{
        playSound('hit');
        resetPlayer();
      }}

      // Camera horizontal deadzone
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

      if (currentLevel === 2) {{
        renderLevel2(now);
      }} else {{
        renderLevel1(now);
      }}
    }}

    // ==========================================
    // RENDER LEVEL 2: TWILIGHT SANCTUARY
    // ==========================================
    function renderLevel2(now) {{
      const offsetX = LEVEL_WIDTH / 2 - cameraX;

      function drawParallaxLayer(img, offset, y = 0, h = LEVEL_HEIGHT) {{
        if (!img) return;
        const x = -(offset % LEVEL_WIDTH);
        ctx.drawImage(img, x, y, LEVEL_WIDTH, h);
        if (x + LEVEL_WIDTH < LEVEL_WIDTH) {{
          ctx.drawImage(img, x + LEVEL_WIDTH, y, LEVEL_WIDTH, h);
        }}
        if (x > 0) {{
          ctx.drawImage(img, x - LEVEL_WIDTH, y, LEVEL_WIDTH, h);
        }}
      }}

      // Layer 1: Sky Sunset (0.05x speed)
      drawParallaxLayer(images.l2_sky, parallaxOffsets[0]);

      // Layer 2: Distant Mountains & Mist (0.15x speed)
      drawParallaxLayer(images.l2_mountains, parallaxOffsets[1]);

      // Layer 3: Midground Bamboo Grove Silhouette (0.35x speed)
      drawParallaxLayer(images.l2_grove, parallaxOffsets[2]);

      // --- Stage Platforms & Props (1.0x with camera offset) ---
      ctx.save();
      ctx.translate(offsetX, 0);

      // 1. Autumn Ground Blocks (left & right cliffs) with deep solid bedrock fill
      if (images.l2_block) {{
        ctx.fillStyle = '#1a120b';
        ctx.fillRect(0, 440, 286, LEVEL_HEIGHT - 440);
        ctx.fillRect(799, 440, 225, LEVEL_HEIGHT - 440);

        ctx.drawImage(images.l2_block, 0, 440, 286, 146);
        ctx.drawImage(images.l2_block, 799, 440, 225, 146);
      }}

      // Look up objects by id from stageObjects:
      const torii = stageObjects.find(o => o.id === 'torii');
      const lanternL = stageObjects.find(o => o.id === 'lantern_l');
      const lanternR = stageObjects.find(o => o.id === 'lantern_r');
      const bridge1 = stageObjects.find(o => o.id === 'bridge1');
      const centerPlat = stageObjects.find(o => o.id === 'platform');
      const bridge2 = stageObjects.find(o => o.id === 'bridge2');
      const spikes1 = stageObjects.find(o => o.id === 'spikes1');
      const spikes2 = stageObjects.find(o => o.id === 'spikes2');
      const shurikenObj = stageObjects.find(o => o.id === 'shuriken');

      // 2. Grand Torii Gate
      if (images.l2_torii && torii) {{
        ctx.drawImage(images.l2_torii, torii.x, torii.y, torii.w, torii.h);
      }}

      // 3. Stone Toro Lanterns
      if (images.l2_lantern) {{
        if (lanternL) {{
          drawLanternGlow(ctx, lanternL.x + lanternL.w / 2, lanternL.y + lanternL.h / 2, 18 + 4 * Math.sin(now / 180));
          ctx.drawImage(images.l2_lantern, lanternL.x, lanternL.y, lanternL.w, lanternL.h);
        }}
        if (lanternR) {{
          drawLanternGlow(ctx, lanternR.x + lanternR.w / 2, lanternR.y + lanternR.h / 2, 18 + 4 * Math.sin((now + 600) / 190));
          ctx.drawImage(images.l2_lantern, lanternR.x, lanternR.y, lanternR.w, lanternR.h);
        }}
      }}

      // 4. Suspended Bamboo Bridge 1
      if (images.l2_bridge && bridge1) {{
        ctx.drawImage(images.l2_bridge, bridge1.x, bridge1.y, bridge1.w, bridge1.h);
      }}

      // 5. Center Stepping Platform
      if (images.l2_platform && centerPlat) {{
        ctx.drawImage(images.l2_platform, centerPlat.x, centerPlat.y, centerPlat.w, centerPlat.h);
      }}

      // 6. Suspended Bamboo Bridge 2
      if (images.l2_bridge && bridge2) {{
        ctx.drawImage(images.l2_bridge, bridge2.x, bridge2.y, bridge2.w, bridge2.h);
      }}

      // 7. Hazards: Bamboo Spikes
      if (images.l2_spikes) {{
        if (spikes1) ctx.drawImage(images.l2_spikes, spikes1.x, spikes1.y, spikes1.w, spikes1.h);
        if (spikes2) ctx.drawImage(images.l2_spikes, spikes2.x, spikes2.y, spikes2.w, spikes2.h);
      }}

      // 8. Spinning Shuriken Hazard
      if (images.l2_shuriken && shurikenObj) {{
        const sY = isEditMode ? shurikenObj.y : (shurikenObj.baseY + Math.sin(performance.now() / 400 * shurikenObj.speed) * 45);
        ctx.save();
        ctx.translate(shurikenObj.x + shurikenObj.w / 2, sY + shurikenObj.h / 2);
        ctx.rotate(shurikenAngle);
        ctx.drawImage(images.l2_shuriken, -shurikenObj.w / 2, -shurikenObj.h / 2, shurikenObj.w, shurikenObj.h);
        ctx.restore();
      }}

      // 9. Glowing Spirit Orbs
      if (images.l2_orb) {{
        for (const obj of stageObjects) {{
          if (obj.type === 'orb' && !obj.collected) {{
            const bobY = isEditMode ? obj.y : (obj.y + Math.sin((now + obj.x * 3) / 250) * 4);
            const halo = ctx.createRadialGradient(obj.x + 12, bobY + 12, 2, obj.x + 12, bobY + 12, 20);
            halo.addColorStop(0, 'rgba(255, 220, 60, 0.85)');
            halo.addColorStop(0.5, 'rgba(255, 180, 40, 0.4)');
            halo.addColorStop(1, 'rgba(255, 160, 20, 0)');
            ctx.fillStyle = halo;
            ctx.beginPath();
            ctx.arc(obj.x + 12, bobY + 12, 20, 0, Math.PI * 2);
            ctx.fill();

            ctx.drawImage(images.l2_orb, obj.x, bobY, obj.w, obj.h);
          }}
        }}
      }}

      // 10. Ninja Player
      renderNinja();

      // Hitboxes
      if (showHitboxes || isEditMode) {{
        renderHitboxes(getL2OneWayPlatforms(), getL2SolidBlocks(), getL2Hazards());
      }}

      // In Edit Mode, draw selection highlights around objects
      if (isEditMode) {{
        for (const o of stageObjects) {{
          const isSel = selectedObject && selectedObject.id === o.id;
          ctx.strokeStyle = isSel ? '#f59e0b' : 'rgba(56, 189, 248, 0.5)';
          ctx.lineWidth = isSel ? 2 : 1;
          ctx.strokeRect(o.x, o.y, o.w, o.h);

          // Name label
          ctx.fillStyle = isSel ? '#f59e0b' : 'rgba(14, 165, 233, 0.9)';
          ctx.font = '10px monospace';
          ctx.fillText(o.name, o.x, o.y - 4);
        }}
      }}

      ctx.restore();

      // Layer 5: Foreground Fireflies (1.30x speed)
      drawParallaxLayer(images.l2_foreground, parallaxOffsets[3]);

      // Ambient Animated Fireflies
      for (const ff of ambientFireflies) {{
        const alpha = 0.4 + 0.4 * Math.sin(now / 300 + ff.phase);
        ctx.fillStyle = `rgba(255, 225, 110, ${{alpha}})`;
        ctx.beginPath();
        ctx.arc(ff.x, ff.y, ff.radius, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = `rgba(255, 200, 60, ${{alpha * 0.35}})`;
        ctx.beginPath();
        ctx.arc(ff.x, ff.y, ff.radius * 2.8, 0, Math.PI * 2);
        ctx.fill();
      }}
    }}

    function drawLanternGlow(c, x, y, radius) {{
      const glow = c.createRadialGradient(x, y, 2, x, y, radius * 2.5);
      glow.addColorStop(0, 'rgba(255, 210, 80, 0.7)');
      glow.addColorStop(0.4, 'rgba(255, 160, 40, 0.3)');
      glow.addColorStop(1, 'rgba(255, 120, 20, 0)');
      c.fillStyle = glow;
      c.beginPath();
      c.arc(x, y, radius * 2.5, 0, Math.PI * 2);
      c.fill();
    }}

    // ==========================================
    // RENDER LEVEL 1: DAYTIME BAMBOO VILLAGE
    // ==========================================
    function renderLevel1(now) {{
      const offsetX = LEVEL_WIDTH / 2 - cameraX;

      // 1. Daytime Backdrop
      if (images.l1_bg) {{
        ctx.drawImage(images.l1_bg, 0, 0, LEVEL_WIDTH, LEVEL_HEIGHT);
      }}

      ctx.save();
      ctx.translate(offsetX, 0);

      // 2. Pagoda Shrines
      if (images.l1_pagoda) {{
        ctx.drawImage(images.l1_pagoda, 40, 440 - 245, 175, 245);
        ctx.drawImage(images.l1_pagoda, 800, 440 - 245, 175, 245);
      }}

      // 3. Ground Blocks
      if (images.l1_root) {{
        ctx.drawImage(images.l1_root, 0, 440, 310, 136);
        ctx.drawImage(images.l1_root, 714, 440, 310, 136);
      }}

      // 4. Stepping Stones
      if (images.l1_pillar) {{
        ctx.drawImage(images.l1_pillar, 295, 418, 48, 120);
        ctx.drawImage(images.l1_pillar, 680, 418, 48, 120);
        ctx.drawImage(images.l1_pillar, 430, 488, 46, 60);
        ctx.drawImage(images.l1_pillar, 550, 496, 46, 52);
      }}

      // 5. Bamboo Suspension Bridge
      if (images.l1_bridge) {{
        ctx.drawImage(images.l1_bridge, 290, 360, 444, 96);
      }}

      // 6. Ninja Player
      renderNinja();

      // Hitboxes
      if (showHitboxes) {{
        renderHitboxes(l1_oneWayPlatforms, l1_solidBlocks, []);
      }}

      ctx.restore();
    }}

    function renderNinja() {{
      ctx.save();
      ctx.translate(player.x, player.y - player.height / 2);
      ctx.rotate(player.angle);
      if (!player.isFacingRight) ctx.scale(-1, 1);

      // Drop shadow on ground
      if (player.isOnGround) {{
        ctx.fillStyle = 'rgba(0, 0, 0, 0.35)';
        ctx.beginPath();
        ctx.ellipse(0, player.height / 2 - 2, 16, 4, 0, 0, Math.PI * 2);
        ctx.fill();
      }}

      // Sprite: Ninja idle/run
      if (images.ninja) {{
        const isMoving = Math.abs(player.vx) > 10;
        const bounce = isMoving ? Math.sin(performance.now() / 60) * 2 : Math.sin(performance.now() / 400) * 1;
        ctx.drawImage(
          images.ninja,
          -player.width / 2,
          -player.height / 2 + bounce,
          player.width,
          player.height
        );
      }} else {{
        ctx.fillStyle = '#223344';
        ctx.fillRect(-18, -player.height / 2, 36, player.height);
      }}

      ctx.restore();
    }}

    function renderHitboxes(oneWayPlats, solidBlocks, hazards) {{
      ctx.lineWidth = 1.5;

      // Solid blocks: Orange
      ctx.strokeStyle = '#f97316';
      ctx.fillStyle = 'rgba(249, 115, 22, 0.15)';
      for (const b of solidBlocks) {{
        ctx.strokeRect(b.x, b.y, b.w, b.h);
        ctx.fillRect(b.x, b.y, b.w, b.h);
      }}

      // One-way platforms: Green
      ctx.strokeStyle = '#10b981';
      ctx.fillStyle = 'rgba(16, 185, 129, 0.15)';
      for (const p of oneWayPlats) {{
        ctx.strokeRect(p.x, p.y, p.w, p.h);
        ctx.fillRect(p.x, p.y, p.w, p.h);
      }}

      // Hazards: Red
      ctx.strokeStyle = '#ef4444';
      ctx.fillStyle = 'rgba(239, 68, 68, 0.2)';
      for (const h of hazards) {{
        const hY = h.currentY !== undefined ? h.currentY : h.y;
        ctx.strokeRect(h.x, hY, h.w, h.h);
        ctx.fillRect(h.x, hY, h.w, h.h);
      }}

      // Player box: Cyan
      ctx.strokeStyle = '#06b6d4';
      ctx.fillStyle = 'rgba(6, 182, 212, 0.2)';
      ctx.strokeRect(player.x - player.width / 2, player.y - player.height, player.width, player.height);
      ctx.fillRect(player.x - player.width / 2, player.y - player.height, player.width, player.height);
    }}

  </script>
</body>
</html>
'''

# Write to preview HTML files
p1 = os.path.join(artifact_dir, "twilight_sanctuary_mobile_preview.html")
with open(p1, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Saved {p1} ({len(html_content)} bytes)")

p2 = os.path.join(artifact_dir, "bamboo_village_mobile_preview.html")
with open(p2, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Saved {p2} ({len(html_content)} bytes)")
