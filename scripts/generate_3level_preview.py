import base64
import os

images_dir = r"c:\Users\User\.gemini\antigravity\scratch\super_dash_Remix\assets\images"
artifact_dir = r"C:\Users\User\.gemini\antigravity\brain\b6c18e6e-846f-4320-a1a4-aab0dc148d2b"

assets = {
    # Ninja Player
    "ninja": "character_ninja.png",
    "ninja_run": "spritesheet_ninja_run.png",
    "ninja_idle": "spritesheet_ninja_idle.png",
    "ninja_jump": "spritesheet_ninja_jump.png",
    # Level 1: Bamboo Village (Cinematic Unified Plate)
    "l1_cinematic": "level1_cinematic_stage_1024.png",
    "l1_bg": "backdrop_bamboo.png",
    "l1_pagoda": "prop_pagoda.png",
    "l1_bridge": "prop_rope_bridge.png",
    "l1_root": "prop_root_block.png",
    "l1_pillar": "prop_stone_pillar.png",
    # Level 2: Twilight Sanctuary (Cinematic Unified Plate)
    "l2_cinematic": "level2_cinematic_stage_1024.png",
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
    # Level 3: Autumn Maple Forest (Cinematic Unified Plate)
    "l3_cinematic": "level3_cinematic_stage_1024.png",
    "l3_orb": "level3_prop_spirit_orb.png",
    "l3_leaf": "level3_prop_maple_leaf.png",
}

b64_assets = {}
for key, filename in assets.items():
    p = os.path.join(images_dir, filename)
    if os.path.exists(p):
        with open(p, "rb") as f:
            b64_assets[key] = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
        print(f"Loaded {key}: {len(b64_assets[key])} chars")
    else:
        print(f"WARNING: Missing {p}!")

def build_html(default_level=3):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shinobi Sprint - Cinematic 2D Platformer</title>
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
<body class="bg-slate-950 text-white min-h-screen flex flex-col items-center justify-center p-2 sm:p-4 font-sans select-none overflow-x-hidden">

  <!-- Header & Toolbar -->
  <header class="w-full max-w-5xl flex flex-wrap items-center justify-between gap-3 mb-2 px-2">
    <div class="flex items-center gap-3">
      <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-amber-600 via-rose-500 to-indigo-600 flex items-center justify-center font-bold text-lg shadow-lg shadow-amber-500/20">
        🥷
      </div>
      <div>
        <h1 class="text-base sm:text-lg font-bold tracking-tight text-gray-100 flex items-center gap-2">
          <span>Shinobi Sprint</span>
          <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Cinematic Plate Mode</span>
        </h1>
        <p class="text-xs text-gray-400">Hand-Painted Multi-Depth Environment & Dynamic Physics</p>
      </div>
    </div>

    <!-- Controls & Toggles -->
    <div class="flex items-center flex-wrap gap-2 text-xs">
      
      <!-- Stage Switcher Tabs -->
      <div class="bg-gray-900 border border-gray-700/80 rounded-xl p-1 flex items-center gap-1 shadow-inner">
        <button id="tabL1" onclick="switchStage(1)" class="px-2.5 py-1 rounded-lg font-medium transition text-gray-400 hover:text-white flex items-center gap-1.5">
          <span>🎋</span>
          <span class="hidden sm:inline">Bamboo Village</span>
          <span class="sm:hidden">L1</span>
        </button>
        <button id="tabL2" onclick="switchStage(2)" class="px-2.5 py-1 rounded-lg font-medium transition text-gray-400 hover:text-white flex items-center gap-1.5">
          <span>🏮</span>
          <span class="hidden sm:inline">Twilight Sanctuary</span>
          <span class="sm:hidden">L2</span>
        </button>
        <button id="tabL3" onclick="switchStage(3)" class="px-2.5 py-1 rounded-lg font-medium transition text-rose-300 bg-rose-500/20 border border-rose-500/40 flex items-center gap-1.5">
          <span>🍁</span>
          <span class="hidden sm:inline">Autumn Maple</span>
          <span class="sm:hidden">L3</span>
        </button>
      </div>

      <!-- Edit Layout Button -->
      <button id="btnEditLayout" onclick="toggleEditMode()" class="px-3 py-1.5 rounded-xl bg-purple-600/30 border border-purple-400/50 hover:bg-purple-600/50 text-purple-200 transition font-medium flex items-center gap-1.5 shadow">
        <span id="editIcon">🛠️</span>
        <span id="editText">Edit Hitboxes / Orbs</span>
      </button>

      <!-- Copy Coordinates Button -->
      <button id="btnCopyCoords" onclick="copyCoordinates()" class="hidden px-3 py-1.5 rounded-xl bg-amber-500/30 border border-amber-400/60 hover:bg-amber-500/50 text-amber-200 transition font-medium flex items-center gap-1.5 shadow">
        <span>📋</span>
        <span>Copy Coordinates</span>
      </button>

      <!-- Hitbox Toggle -->
      <button id="btnHitbox" onclick="toggleHitboxes()" class="px-3 py-1.5 rounded-xl bg-gray-800 border border-gray-700 hover:border-gray-500 text-gray-300 transition flex items-center gap-1.5 shadow">
        <span class="w-2 h-2 rounded-full bg-gray-500" id="hitboxDot"></span>
        <span id="hitboxText">Hitboxes OFF</span>
      </button>

      <!-- Sound Toggle -->
      <button id="btnSound" onclick="toggleSound()" class="p-1.5 rounded-xl bg-gray-800 border border-gray-700 hover:border-gray-500 text-gray-300 transition shadow">
        <span id="soundIcon">🔊</span>
      </button>

      <!-- Reset -->
      <button onclick="resetPlayer()" class="px-3 py-1.5 rounded-xl bg-red-950/40 border border-red-800/60 text-red-300 hover:bg-red-900/60 transition shadow">
        Reset
      </button>
    </div>
  </header>

  <!-- Mobile Viewport Container -->
  <main class="relative w-full max-w-[960px] flex justify-center items-center my-1">
    <div class="relative w-full aspect-[16/9] max-h-[540px] rounded-[36px] bg-[#0c101a] p-3 phone-shadow border border-white/10 flex flex-col overflow-hidden">
      
      <!-- Top Bezel / Dynamic Island -->
      <div class="absolute top-4 left-1/2 -translate-x-1/2 z-40 flex items-center justify-center pointer-events-none">
        <div class="dynamic-island flex items-center justify-between px-3">
          <div class="w-2.5 h-2.5 rounded-full bg-emerald-500/80 animate-pulse"></div>
          <div class="w-3 h-3 rounded-full bg-neutral-900 border border-white/20"></div>
        </div>
      </div>

      <!-- Canvas Wrapper -->
      <div class="relative w-full h-full rounded-[24px] overflow-hidden bg-black flex items-center justify-center">
        
        <canvas id="gameCanvas" width="1024" height="576" class="w-full h-full object-contain cursor-default"></canvas>

        <!-- Edit Mode Banner -->
        <div id="editBanner" class="hidden absolute top-3 left-4 right-4 z-40 bg-purple-950/80 border border-purple-500/50 backdrop-blur-md px-3 py-1.5 rounded-xl text-xs flex items-center justify-between shadow-2xl">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-purple-400 animate-ping"></span>
            <span class="text-purple-200 font-medium">🎯 <b>Edit Mode:</b> Click & drag any platform, bridge hitbox, or orb to adjust collision bounds.</span>
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
              <span id="scoreDisplay">Orbs: <b id="scoreText" class="text-amber-400">0 / 5</b></span>
              <span>Pos: <b id="posText" class="text-cyan-300">60, 298</b></span>
            </div>
            <div id="envPill" class="bg-black/60 backdrop-blur px-3 py-1 rounded-full border border-amber-400/30 text-[11px] text-amber-300 flex items-center gap-1.5">
              <span id="envIcon">🍁</span>
              <span id="envName">Autumn Maple Forest</span>
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
      <span>Drop through bridges & ramps</span>
    </div>
  </footer>

  <script>
    // Audio Synthesizer
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
          osc.frequency.exponentialRampToValueAtTime(540, t + 0.16);
          gain.gain.setValueAtTime(0.18, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.16);
          osc.start(t);
          osc.stop(t + 0.16);
        }} else if (type === 'orb') {{
          osc.type = 'sine';
          osc.frequency.setValueAtTime(523.25, t);
          osc.frequency.setValueAtTime(659.25, t + 0.08);
          osc.frequency.setValueAtTime(783.99, t + 0.16);
          osc.frequency.setValueAtTime(1046.50, t + 0.24);
          gain.gain.setValueAtTime(0.2, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.35);
          osc.start(t);
          osc.stop(t + 0.35);
        }} else if (type === 'drop') {{
          osc.type = 'sine';
          osc.frequency.setValueAtTime(320, t);
          osc.frequency.exponentialRampToValueAtTime(140, t + 0.14);
          gain.gain.setValueAtTime(0.18, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.14);
          osc.start(t);
          osc.stop(t + 0.14);
        }} else if (type === 'hit') {{
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(160, t);
          osc.frequency.exponentialRampToValueAtTime(60, t + 0.2);
          gain.gain.setValueAtTime(0.25, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.2);
          osc.start(t);
          osc.stop(t + 0.2);
        }}
      }} catch (e) {{}}
    }}

    function toggleSound() {{
      soundEnabled = !soundEnabled;
      document.getElementById('soundIcon').textContent = soundEnabled ? '🔊' : '🔇';
    }}

    // Sprites dictionary
    const imgData = {{
      ninja: "{b64_assets.get('ninja', '')}",
      l1_cinematic: "{b64_assets.get('l1_cinematic', '')}",
      l1_bg: "{b64_assets.get('l1_bg', '')}",
      l1_pagoda: "{b64_assets.get('l1_pagoda', '')}",
      l1_bridge: "{b64_assets.get('l1_bridge', '')}",
      l1_root: "{b64_assets.get('l1_root', '')}",
      l1_pillar: "{b64_assets.get('l1_pillar', '')}",
      l2_cinematic: "{b64_assets.get('l2_cinematic', '')}",
      l2_sky: "{b64_assets.get('l2_sky', '')}",
      l2_mountains: "{b64_assets.get('l2_mountains', '')}",
      l2_grove: "{b64_assets.get('l2_grove', '')}",
      l2_foreground: "{b64_assets.get('l2_foreground', '')}",
      l2_platform: "{b64_assets.get('l2_platform', '')}",
      l2_bridge: "{b64_assets.get('l2_bridge', '')}",
      l2_raft: "{b64_assets.get('l2_raft', '')}",
      l2_block: "{b64_assets.get('l2_block', '')}",
      l2_torii: "{b64_assets.get('l2_torii', '')}",
      l2_lantern: "{b64_assets.get('l2_lantern', '')}",
      l2_spikes: "{b64_assets.get('l2_spikes', '')}",
      l2_shuriken: "{b64_assets.get('l2_shuriken', '')}",
      l2_orb: "{b64_assets.get('l2_orb', '')}",
      l3_cinematic: "{b64_assets.get('l3_cinematic', '')}",
      l3_orb: "{b64_assets.get('l3_orb', '')}",
      l3_leaf: "{b64_assets.get('l3_leaf', '')}",
    }};

    const images = {{}};
    let imagesLoaded = 0;
    const totalImages = Object.keys(imgData).length;

    for (const [k, v] of Object.entries(imgData)) {{
      images[k] = new Image();
      images[k].onload = () => {{
        imagesLoaded++;
        if (imagesLoaded === totalImages) {{
          console.log("All sprites loaded!");
        }}
      }};
      images[k].src = v;
    }}

    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    let currentStage = {default_level};
    let showHitboxes = false;
    let editMode = false;
    let selectedObject = null;
    let dragOffsetX = 0;
    let dragOffsetY = 0;

    // Player State
    const player = {{
      x: 60,
      y: 298,
      vx: 0,
      vy: 0,
      w: 32,
      h: 48,
      isOnGround: true,
      facingRight: true,
      dropTimer: 0,
      runAnimTimer: 0,
      idleAnimTimer: 0,
      jumpAnimTimer: 0,
      frameIndex: 0,
    }};

    // Stage Layouts Data
    const stages = {{
      1: {{
        name: "Bamboo Village",
        icon: "🎋",
        spawn: {{ x: 100, y: 490 }},
        orbsTotal: 6,
        objects: [
          // Surface 1: Left Riverbank / Ground
          {{ id: "left_ground", type: "ground", x: 0, y: 490, w: 425, h: 86, color: "#1E3A2B" }},
          // Surface 2: Lower Log Bridge across Chasm (drop-through S+Space)
          {{ id: "lower_bridge", type: "platform", x: 415, y: 490, w: 175, h: 16, sprite: "l2_bridge" }},
          // Surface 3: Right Riverbank / Ground
          {{ id: "right_ground", type: "ground", x: 575, y: 490, w: 449, h: 86, color: "#1E3A2B" }},
          // Surface 4: Elevated Bamboo Platform Table (drop-through S+Space)
          {{ id: "upper_table", type: "platform", x: 420, y: 340, w: 160, h: 16, sprite: "l2_platform" }},
          // Surface 5: Right Raised Earth Cliff
          {{ id: "right_cliff", type: "platform", x: 850, y: 330, w: 174, h: 20 }},
          // Surface 6: Left Hut Rooftop
          {{ id: "left_roof", type: "platform", x: 45, y: 220, w: 230, h: 16 }},
          // Surface 7: Right Dojo Rooftop
          {{ id: "right_roof", type: "platform", x: 770, y: 220, w: 210, h: 16 }},
          // Collectible Golden Spirit Orbs
          {{ id: "orb1", type: "orb", x: 160, y: 175, r: 14, collected: false }},
          {{ id: "orb2", type: "orb", x: 300, y: 440, r: 14, collected: false }},
          {{ id: "orb3", type: "orb", x: 500, y: 290, r: 14, collected: false }},
          {{ id: "orb4", type: "orb", x: 500, y: 440, r: 14, collected: false }},
          {{ id: "orb5", type: "orb", x: 930, y: 280, r: 14, collected: false }},
          {{ id: "orb6", type: "orb", x: 875, y: 175, r: 14, collected: false }},
        ]
      }},
      2: {{
        name: "Twilight Sanctuary",
        icon: "🏮",
        spawn: {{ x: 160, y: 490 }},
        orbsTotal: 8,
        objects: [
          // Surface 1: Left Ground Bank
          {{ id: "left_ground", type: "ground", x: 0, y: 490, w: 225, h: 86, color: "#1A1024" }},
          // Surface 2: Left Sagging Rope Bridge (one-way drop-through)
          {{ id: "left_bridge", type: "platform", x: 220, y: 502, w: 165, h: 16 }},
          // Surface 3: Center Shrine Island Ground
          {{ id: "center_island", type: "ground", x: 380, y: 490, w: 265, h: 86, color: "#1A1024" }},
          // Surface 4: Right Sagging Rope Bridge (one-way drop-through)
          {{ id: "right_bridge", type: "platform", x: 640, y: 502, w: 165, h: 16 }},
          // Surface 5: Right Hill Ramp & Plateau
          {{ id: "right_ramp", type: "platform", x: 800, y: 490, w: 105, h: 16 }},
          {{ id: "right_plateau", type: "ground", x: 900, y: 425, w: 124, h: 151, color: "#1A1024" }},
          // Watchtowers: Left & Right Lookout Ledges
          {{ id: "watchtower_l_mid", type: "platform", x: 215, y: 250, w: 105, h: 16 }},
          {{ id: "watchtower_l_top", type: "platform", x: 225, y: 195, w: 85, h: 16 }},
          {{ id: "watchtower_r_mid", type: "platform", x: 715, y: 250, w: 105, h: 16 }},
          {{ id: "watchtower_r_top", type: "platform", x: 725, y: 195, w: 85, h: 16 }},
          // Left Spike Hazard
          {{ id: "spike_hazard", type: "hazard", x: 55, y: 440, w: 70, h: 50 }},
          // Collectible Golden Spirit Orbs
          {{ id: "orb1", type: "orb", x: 270, y: 160, r: 14, collected: false }},
          {{ id: "orb2", type: "orb", x: 300, y: 465, r: 14, collected: false }},
          {{ id: "orb3", type: "orb", x: 455, y: 440, r: 14, collected: false }},
          {{ id: "orb4", type: "orb", x: 512, y: 435, r: 14, collected: false }},
          {{ id: "orb5", type: "orb", x: 570, y: 440, r: 14, collected: false }},
          {{ id: "orb6", type: "orb", x: 720, y: 465, r: 14, collected: false }},
          {{ id: "orb7", type: "orb", x: 770, y: 160, r: 14, collected: false }},
          {{ id: "orb8", type: "orb", x: 950, y: 375, r: 14, collected: false }},
        ]
      }},
      3: {{
        name: "Autumn Maple Forest",
        icon: "🍁",
        spawn: {{ x: 60, y: 298 }},
        orbsTotal: 5,
        objects: [
          // Surface 1: Left Upper Ledge
          {{ id: "upper_ledge", type: "platform", x: 0, y: 298, w: 120, h: 16 }},
          // Surface 2: Sloped Ramp Steps
          {{ id: "ramp1", type: "platform", x: 120, y: 310, w: 40, h: 14 }},
          {{ id: "ramp2", type: "platform", x: 160, y: 325, w: 40, h: 14 }},
          {{ id: "ramp3", type: "platform", x: 200, y: 340, w: 40, h: 14 }},
          {{ id: "ramp4", type: "platform", x: 240, y: 355, w: 40, h: 14 }},
          {{ id: "ramp5", type: "platform", x: 280, y: 370, w: 30, h: 14 }},
          // Surface 3: Left Stone Pier
          {{ id: "pier_top", type: "platform", x: 310, y: 375, w: 120, h: 16 }},
          // Surface 4: Arched Bridge Walkway (Incline, Crest, Decline)
          {{ id: "bridge_incline", type: "platform", x: 430, y: 355, w: 70, h: 16 }},
          {{ id: "bridge_crest", type: "platform", x: 500, y: 335, w: 190, h: 16 }},
          {{ id: "bridge_decline", type: "platform", x: 690, y: 355, w: 75, h: 16 }},
          // Surface 5: Right Shrine Terrace
          {{ id: "right_terrace", type: "platform", x: 765, y: 375, w: 259, h: 16 }},
          // Surface 6: Lower Forest Banks
          {{ id: "lower_left", type: "ground", x: 0, y: 468, w: 310, h: 108, color: "#131A22" }},
          {{ id: "lower_right", type: "ground", x: 740, y: 468, w: 284, h: 108, color: "#131A22" }},
          // Dynamic Collectible Orbs
          {{ id: "orb1", type: "orb", x: 60, y: 245, r: 14, collected: false }},
          {{ id: "orb2", type: "orb", x: 370, y: 315, r: 14, collected: false }},
          {{ id: "orb3", type: "orb", x: 595, y: 260, r: 14, collected: false }},
          {{ id: "orb4", type: "orb", x: 595, y: 450, r: 14, collected: false }},
          {{ id: "orb5", type: "orb", x: 880, y: 315, r: 14, collected: false }},
          // River Hazard (Spinning Shuriken over mist)
          {{ id: "river_hazard", type: "hazard_spin", x: 575, y: 375, w: 36, h: 36, sprite: "l2_shuriken" }},
        ]
      }}
    }};

    // Floating Autumn Leaf Particles
    const leafParticles = [];
    for (let i = 0; i < 22; i++) {{
      leafParticles.push({{
        x: Math.random() * 1024,
        y: Math.random() * 500,
        vx: 30 + Math.random() * 40,
        vy: 18 + Math.random() * 25,
        rot: Math.random() * Math.PI * 2,
        vRot: (Math.random() - 0.5) * 2.5,
        phase: Math.random() * Math.PI * 2,
        scale: 0.35 + Math.random() * 0.35,
      }});
    }}

    // Controls Input State
    const keys = {{ left: false, right: false, jump: false, drop: false }};

    window.addEventListener('keydown', (e) => {{
      if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code)) {{
        e.preventDefault();
      }}
      if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = true;
      if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = true;
      if (e.code === 'KeyS' || e.code === 'ArrowDown') keys.drop = true;
      if (e.code === 'Space' || e.code === 'KeyW' || e.code === 'ArrowUp') {{
        keys.jump = true;
        handleJumpInput();
      }}
    }});

    window.addEventListener('keyup', (e) => {{
      if (e.code === 'KeyA' || e.code === 'ArrowLeft') keys.left = false;
      if (e.code === 'KeyD' || e.code === 'ArrowRight') keys.right = false;
      if (e.code === 'KeyS' || e.code === 'ArrowDown') keys.drop = false;
      if (e.code === 'Space' || e.code === 'KeyW' || e.code === 'ArrowUp') keys.jump = false;
    }});

    function handleJumpInput() {{
      if (keys.drop) {{
        player.dropTimer = 0.22;
        playSound('drop');
        return;
      }}
      if (player.isOnGround) {{
        player.vy = -420;
        player.isOnGround = false;
        playSound('jump');
      }}
    }}

    function bindTouch(btnId, keyName, isAction = false) {{
      const el = document.getElementById(btnId);
      if (!el) return;
      const start = (e) => {{
        e.preventDefault();
        el.classList.add('active');
        keys[keyName] = true;
        if (isAction && keyName === 'jump') handleJumpInput();
        if (isAction && keyName === 'drop') {{
          player.dropTimer = 0.22;
          playSound('drop');
        }}
      }};
      const end = (e) => {{
        e.preventDefault();
        el.classList.remove('active');
        keys[keyName] = false;
      }};
      el.addEventListener('touchstart', start, {{ passive: false }});
      el.addEventListener('touchend', end, {{ passive: false }});
      el.addEventListener('mousedown', start);
      el.addEventListener('mouseup', end);
      el.addEventListener('mouseleave', end);
    }}

    bindTouch('btnLeft', 'left');
    bindTouch('btnRight', 'right');
    bindTouch('btnJump', 'jump', true);
    bindTouch('btnDrop', 'drop', true);

    function switchStage(stageNum) {{
      currentStage = stageNum;
      document.getElementById('tabL1').className = stageNum === 1 ? 'px-2.5 py-1 rounded-lg font-medium transition text-emerald-300 bg-emerald-500/20 border border-emerald-500/40 flex items-center gap-1.5' : 'px-2.5 py-1 rounded-lg font-medium transition text-gray-400 hover:text-white flex items-center gap-1.5';
      document.getElementById('tabL2').className = stageNum === 2 ? 'px-2.5 py-1 rounded-lg font-medium transition text-amber-300 bg-amber-500/20 border border-amber-500/40 flex items-center gap-1.5' : 'px-2.5 py-1 rounded-lg font-medium transition text-gray-400 hover:text-white flex items-center gap-1.5';
      document.getElementById('tabL3').className = stageNum === 3 ? 'px-2.5 py-1 rounded-lg font-medium transition text-rose-300 bg-rose-500/20 border border-rose-500/40 flex items-center gap-1.5' : 'px-2.5 py-1 rounded-lg font-medium transition text-gray-400 hover:text-white flex items-center gap-1.5';

      const s = stages[stageNum];
      document.getElementById('envIcon').textContent = s.icon;
      document.getElementById('envName').textContent = s.name;
      
      // Reset orbs collected count
      for (const obj of s.objects) {{
        if (obj.type === 'orb') obj.collected = false;
      }}
      resetPlayer();
      updateScoreUI();
    }}

    function toggleHitboxes() {{
      showHitboxes = !showHitboxes;
      const dot = document.getElementById('hitboxDot');
      const txt = document.getElementById('hitboxText');
      if (showHitboxes) {{
        dot.className = 'w-2 h-2 rounded-full bg-emerald-400 animate-pulse';
        txt.textContent = 'Hitboxes ON';
      }} else {{
        dot.className = 'w-2 h-2 rounded-full bg-gray-500';
        txt.textContent = 'Hitboxes OFF';
      }}
    }}

    function toggleEditMode() {{
      editMode = !editMode;
      const banner = document.getElementById('editBanner');
      const copyBtn = document.getElementById('btnCopyCoords');
      const editBtn = document.getElementById('btnEditLayout');
      if (editMode) {{
        banner.classList.remove('hidden');
        copyBtn.classList.remove('hidden');
        editBtn.className = 'px-3 py-1.5 rounded-xl bg-purple-500 text-white font-medium flex items-center gap-1.5 shadow ring-2 ring-purple-400';
        canvas.style.cursor = 'grab';
      }} else {{
        banner.classList.add('hidden');
        copyBtn.classList.add('hidden');
        editBtn.className = 'px-3 py-1.5 rounded-xl bg-purple-600/30 border border-purple-400/50 hover:bg-purple-600/50 text-purple-200 transition font-medium flex items-center gap-1.5 shadow';
        canvas.style.cursor = 'default';
        selectedObject = null;
      }}
    }}

    function copyCoordinates() {{
      const st = stages[currentStage];
      const summary = st.objects.map(o => ({{
        id: o.id,
        type: o.type,
        x: Math.round(o.x),
        y: Math.round(o.y),
        w: o.w,
        h: o.h,
        sprite: o.sprite
      }}));
      const jsonStr = JSON.stringify(summary, null, 2);
      navigator.clipboard.writeText(jsonStr).then(() => {{
        showToast("📋 Coordinates copied to clipboard!");
      }}).catch(() => {{
        showToast("Coordinates logged to browser console!");
        console.log(jsonStr);
      }});
    }}

    function showToast(msg) {{
      const t = document.createElement('div');
      t.className = 'toast fixed bottom-6 left-1/2 -translate-x-1/2 z-50 bg-emerald-600 text-white text-xs px-4 py-2 rounded-xl shadow-2xl font-mono';
      t.textContent = msg;
      document.body.appendChild(t);
      setTimeout(() => t.remove(), 2600);
    }}

    function resetPlayer() {{
      const s = stages[currentStage];
      player.x = s.spawn.x;
      player.y = s.spawn.y;
      player.vx = 0;
      player.vy = 0;
      player.isOnGround = true;
      player.runAnimTimer = 0;
      player.idleAnimTimer = 0;
      player.jumpAnimTimer = 0;
    }}

    // Mouse / Touch Dragging in Edit Mode
    function getCanvasCoords(e) {{
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const clientX = e.clientX || (e.touches && e.touches[0].clientX);
      const clientY = e.clientY || (e.touches && e.touches[0].clientY);
      return {{
        x: (clientX - rect.left) * scaleX,
        y: (clientY - rect.top) * scaleY
      }};
    }}

    canvas.addEventListener('mousedown', (e) => {{
      if (!editMode) return;
      const pos = getCanvasCoords(e);
      const st = stages[currentStage];
      selectedObject = null;
      for (let i = st.objects.length - 1; i >= 0; i--) {{
        const o = st.objects[i];
        const w = o.w || o.r * 2 || 32;
        const h = o.h || o.r * 2 || 32;
        if (pos.x >= o.x && pos.x <= o.x + w && pos.y >= o.y && pos.y <= o.y + h) {{
          selectedObject = o;
          dragOffsetX = pos.x - o.x;
          dragOffsetY = pos.y - o.y;
          canvas.style.cursor = 'grabbing';
          document.getElementById('selectionInfo').textContent = `Selected: ${{o.id}} (${{Math.round(o.x)}}, ${{Math.round(o.y)}})`;
          break;
        }}
      }}
    }});

    window.addEventListener('mousemove', (e) => {{
      if (!editMode || !selectedObject) return;
      const pos = getCanvasCoords(e);
      selectedObject.x = Math.round(pos.x - dragOffsetX);
      selectedObject.y = Math.round(pos.y - dragOffsetY);
      document.getElementById('selectionInfo').textContent = `Selected: ${{selectedObject.id}} (${{selectedObject.x}}, ${{selectedObject.y}})`;
    }});

    window.addEventListener('mouseup', () => {{
      if (editMode && selectedObject) {{
        canvas.style.cursor = 'grab';
      }}
    }});

    function updateScoreUI() {{
      const st = stages[currentStage];
      const collected = st.objects.filter(o => o.type === 'orb' && o.collected).length;
      document.getElementById('scoreText').textContent = `${{collected}} / ${{st.orbsTotal}}`;
    }}

    // Physics & Render Loop
    let lastTime = performance.now();
    let frameCount = 0;
    let fpsTime = 0;
    let parallaxX = 0;
    let shurikenAngle = 0;
    let mistTime = 0;

    function gameLoop(time) {{
      const dt = Math.min((time - lastTime) / 1000, 0.05);
      lastTime = time;

      frameCount++;
      fpsTime += dt;
      if (fpsTime >= 0.5) {{
        document.getElementById('fpsText').textContent = Math.round(frameCount / fpsTime);
        frameCount = 0;
        fpsTime = 0;
      }}

      shurikenAngle += dt * 8.0;
      mistTime += dt;

      if (!editMode) {{
        updatePhysics(dt);
      }}

      render();
      requestAnimationFrame(gameLoop);
    }}

    function updatePhysics(dt) {{
      const speed = 180;
      const gravity = 980;

      if (keys.left) {{
        player.vx = -speed;
        player.facingRight = false;
      }} else if (keys.right) {{
        player.vx = speed;
        player.facingRight = true;
      }} else {{
        player.vx = 0;
      }}

      player.vy += gravity * dt;
      if (player.vy > 650) player.vy = 650;

      player.x += player.vx * dt;
      player.y += player.vy * dt;

      if (player.dropTimer > 0) {{
        player.dropTimer -= dt;
      }}

      if (player.x < 16) player.x = 16;
      if (player.x > 1024 - 16) player.x = 1024 - 16;

      player.isOnGround = false;
      const st = stages[currentStage];

      for (const obj of st.objects) {{
        if (obj.type === 'ground') {{
          if (player.x + 10 > obj.x && player.x - 10 < obj.x + obj.w) {{
            if (player.y >= obj.y && player.y - player.vy * dt <= obj.y + 16) {{
              player.y = obj.y;
              player.vy = 0;
              player.isOnGround = true;
            }}
          }}
        }} else if (obj.type === 'platform') {{
          if (player.dropTimer <= 0 && player.vy >= 0) {{
            if (player.x + 10 > obj.x && player.x - 10 < obj.x + obj.w) {{
              if (player.y >= obj.y && player.y - player.vy * dt <= obj.y + 16) {{
                player.y = obj.y;
                player.vy = 0;
                player.isOnGround = true;
              }}
            }}
          }}
        }} else if (obj.type === 'orb' && !obj.collected) {{
          const dx = player.x - obj.x;
          const dy = (player.y - 24) - obj.y;
          if (Math.hypot(dx, dy) < obj.r + 20) {{
            obj.collected = true;
            playSound('orb');
            updateScoreUI();
          }}
        }} else if (obj.type === 'hazard' || obj.type === 'hazard_spin') {{
          const hx = obj.x;
          const hy = obj.y;
          const hw = obj.w;
          const hh = obj.h;
          if (player.x + 10 > hx && player.x - 10 < hx + hw &&
              player.y > hy && player.y - 48 < hy + hh) {{
            playSound('hit');
            resetPlayer();
          }}
        }}
      }}

      // State-driven animation timer updates
      if (player.isOnGround) {{
        player.jumpAnimTimer = 0;
        if (Math.abs(player.vx) > 10) {{
          player.runAnimTimer += dt;
          player.idleAnimTimer = 0;
        }} else {{
          player.runAnimTimer = 0;
          player.idleAnimTimer += dt;
        }}
      }} else {{
        player.jumpAnimTimer += dt;
        player.runAnimTimer = 0;
        player.idleAnimTimer = 0;
      }}

      // Pit fall death
      if (player.y > 570) {{
        playSound('hit');
        resetPlayer();
      }}

      parallaxX += dt * 20;

      for (const p of leafParticles) {{
        p.phase += dt * 2.0;
        p.x += (p.vx + Math.sin(p.phase) * 15) * dt;
        p.y += p.vy * dt;
        p.rot += p.vRot * dt;
        if (p.x > 1050) p.x = -30;
        if (p.y > 560) {{
          p.y = -20;
          p.x = Math.random() * 1024;
        }}
      }}

      document.getElementById('posText').textContent = `${{Math.round(player.x)}}, ${{Math.round(player.y)}}`;
    }}

    function render() {{
      ctx.clearRect(0, 0, 1024, 576);

      if (currentStage === 1) {{
        renderStage1();
      }} else if (currentStage === 2) {{
        renderStage2();
      }} else if (currentStage === 3) {{
        renderStage3();
      }}

      renderPlayer();

      if (showHitboxes || editMode) {{
        renderHitboxes();
      }}
    }}

    // STAGE 1: Bamboo Village (CINEMATIC UNIFIED-PLATE ARCHITECTURE)
    function renderStage1() {{
      // 1. Hand-Painted Daytime Master Plate (Morning Sunlight & Mount Fuji)
      if (images.l1_cinematic && images.l1_cinematic.complete) {{
        ctx.drawImage(images.l1_cinematic, 0, 0, 1024, 576);
      }} else {{
        ctx.fillStyle = '#1E3A2B';
        ctx.fillRect(0, 0, 1024, 576);
      }}

      // 2. Chasm Crossing Sprites (Lower Log Bridge & Upper Bamboo Table Platform)
      if (images.l2_bridge && images.l2_bridge.complete) {{
        ctx.drawImage(images.l2_bridge, 415, 485, 175, 45);
      }}
      if (images.l2_platform && images.l2_platform.complete) {{
        ctx.drawImage(images.l2_platform, 420, 340, 160, 50);
      }}

      // 3. Floating Sunlit Bamboo Pollen/Leaves
      if (images.l3_leaf && images.l3_leaf.complete) {{
        for (const p of leafParticles) {{
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate(p.rot);
          ctx.scale(p.scale * 0.7, p.scale * 0.7);
          ctx.drawImage(images.l3_leaf, -15, -17, 30, 35);
          ctx.restore();
        }}
      }}

      // 4. Collectible Golden Spirit Orbs
      const st = stages[1];
      for (const obj of st.objects) {{
        if (obj.type === 'orb' && !obj.collected) {{
          renderSpiritOrb(obj.x, obj.y, obj.r, '#facc15');
        }}
      }}

      // 5. Morning Sun Ray Bloom effect from Mount Fuji
      renderLanternBloom(850, 140, 90, 'rgba(254, 240, 138, 0.22)');
      renderLanternBloom(850, 140, 180, 'rgba(253, 224, 71, 0.12)');
    }}

    // STAGE 2: Twilight Sanctuary (CINEMATIC UNIFIED-PLATE ARCHITECTURE)
    function renderStage2() {{
      // 1. Full Hand-Painted Sunset Master Plate (Setting Sun, Torii Gate & Watchtowers)
      if (images.l2_cinematic && images.l2_cinematic.complete) {{
        ctx.drawImage(images.l2_cinematic, 0, 0, 1024, 576);
      }} else {{
        ctx.fillStyle = '#0C101A';
        ctx.fillRect(0, 0, 1024, 576);
      }}

      // 2. Floating Sunset Dusk Embers/Leaves
      if (images.l3_leaf && images.l3_leaf.complete) {{
        for (const p of leafParticles) {{
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate(p.rot);
          ctx.scale(p.scale * 0.75, p.scale * 0.75);
          ctx.drawImage(images.l3_leaf, -15, -17, 30, 35);
          ctx.restore();
        }}
      }}

      // 3. Interactive Collectible Golden Spirit Orbs
      const st = stages[2];
      for (const obj of st.objects) {{
        if (obj.type === 'orb' && !obj.collected) {{
          renderSpiritOrb(obj.x, obj.y, obj.r, '#facc15');
        }}
      }}

      // 4. Atmospheric Sunset Light Blooms
      // Warm Lantern Blooms
      const pulse = 1.0 + Math.sin(mistTime * 2.5) * 0.08;
      renderLanternBloom(23, 470, 35 * pulse, 'rgba(251, 191, 36, 0.22)');
      renderLanternBloom(408, 470, 35 * pulse, 'rgba(251, 191, 36, 0.22)');
      renderLanternBloom(602, 470, 35 * pulse, 'rgba(251, 191, 36, 0.22)');

      // Radiant Sunset Disc Bloom
      renderLanternBloom(512, 280, 140, 'rgba(254, 215, 170, 0.15)');
      renderLanternBloom(512, 280, 220, 'rgba(251, 146, 60, 0.08)');
    }}

    // STAGE 3: Autumn Maple Forest (CINEMATIC UNIFIED-PLATE APPROACH)
    function renderStage3() {{
      // 1. Full Hand-Painted Stage Plate (Unified Lighting & Depth)
      if (images.l3_cinematic && images.l3_cinematic.complete) {{
        ctx.drawImage(images.l3_cinematic, 0, 0, 1024, 576);
      }} else {{
        ctx.fillStyle = '#0A0F1A';
        ctx.fillRect(0, 0, 1024, 576);
      }}

      // 2. Animated River Mist Flowing in the Canyon
      ctx.save();
      const mistGradient = ctx.createLinearGradient(0, 480, 0, 560);
      mistGradient.addColorStop(0, 'rgba(164, 219, 245, 0)');
      mistGradient.addColorStop(0.5, 'rgba(180, 230, 255, 0.12)');
      mistGradient.addColorStop(1, 'rgba(164, 219, 245, 0.25)');
      ctx.fillStyle = mistGradient;
      ctx.beginPath();
      // Wave curve across river chasm
      ctx.moveTo(310, 500);
      for (let x = 310; x <= 740; x += 30) {{
        const wave = Math.sin((x * 0.02) + mistTime * 1.5) * 8;
        ctx.lineTo(x, 500 + wave);
      }}
      ctx.lineTo(740, 576);
      ctx.lineTo(310, 576);
      ctx.closePath();
      ctx.fill();
      ctx.restore();

      // 3. Floating Autumn Momiji Leaves (Drifting with wind)
      if (images.l3_leaf && images.l3_leaf.complete) {{
        for (const p of leafParticles) {{
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate(p.rot);
          ctx.scale(p.scale, p.scale);
          ctx.drawImage(images.l3_leaf, -15, -17, 30, 35);
          ctx.restore();
        }}
      }}

      // 4. Interactive Stage Entities (Orbs & Hazards)
      const st = stages[3];
      for (const obj of st.objects) {{
        if (obj.type === 'orb' && !obj.collected) {{
          renderSpiritOrb(obj.x, obj.y, obj.r, '#2dd4bf');
        }} else if (obj.type === 'hazard_spin' && obj.sprite && images[obj.sprite]) {{
          ctx.save();
          ctx.translate(obj.x + obj.w / 2, obj.y + obj.h / 2);
          ctx.rotate(shurikenAngle);
          ctx.drawImage(images[obj.sprite], -obj.w / 2, -obj.h / 2, obj.w, obj.h);
          ctx.restore();
        }}
      }}

      // 5. Subtle Lantern Light Bloom (Additive pulsing atmosphere)
      const pulse = 1.0 + Math.sin(mistTime * 3) * 0.08;
      renderLanternBloom(360, 480, 40 * pulse, 'rgba(251, 191, 36, 0.18)');
      renderLanternBloom(485, 335, 30 * pulse, 'rgba(251, 146, 60, 0.15)');
      renderLanternBloom(605, 335, 30 * pulse, 'rgba(251, 146, 60, 0.15)');
      renderLanternBloom(725, 335, 30 * pulse, 'rgba(251, 146, 60, 0.15)');
    }}

    function renderLanternBloom(x, y, radius, color) {{
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      const glow = ctx.createRadialGradient(x, y, 0, x, y, radius);
      glow.addColorStop(0, color);
      glow.addColorStop(1, 'transparent');
      ctx.fillStyle = glow;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }}

    function renderSpiritOrb(x, y, r, color) {{
      ctx.save();
      const glow = ctx.createRadialGradient(x, y, 2, x, y, r * 2.2);
      glow.addColorStop(0, color);
      glow.addColorStop(0.4, color + '99');
      glow.addColorStop(1, 'transparent');
      ctx.fillStyle = glow;
      ctx.beginPath();
      ctx.arc(x, y, r * 2.2, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(x, y, r * 0.6, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }}

    function renderPlayer() {{
      ctx.save();
      ctx.translate(player.x, player.y);
      if (!player.facingRight) {{
        ctx.scale(-1, 1);
      }}

      if (!player.isOnGround) {{
        // Airborne: Jumping or Falling with dynamic leap tilt
        ctx.rotate(player.vy < 0 ? -0.08 : 0.06);
        if (images.ninja_jump && images.ninja_jump.complete) {{
          let jumpFrame = 1;
          if (player.vy < -200) {{
            jumpFrame = 0; // Launch / spring
          }} else if (player.vy < 0) {{
            jumpFrame = 1; // Ascending leap
          }} else if (player.vy < 150) {{
            jumpFrame = 2; // Mid-air crest
          }} else {{
            jumpFrame = 3; // Falling descent
          }}
          ctx.drawImage(images.ninja_jump, jumpFrame * 64, 0, 64, 64, -28, -54, 56, 56);
        }} else if (images.ninja && images.ninja.complete) {{
          ctx.drawImage(images.ninja, -28, -52, 56, 54);
        }} else {{
          renderFallbackPlayer();
        }}
      }} else if (Math.abs(player.vx) > 10) {{
        // Ground Running: 5-frame chibi ninja sprint cycle at 12 FPS
        if (images.ninja_run && images.ninja_run.complete) {{
          const frame = Math.floor(player.runAnimTimer * 12) % 5;
          ctx.drawImage(images.ninja_run, frame * 64, 0, 64, 64, -28, -54, 56, 56);
        }} else if (images.ninja && images.ninja.complete) {{
          const bounce = Math.sin(player.runAnimTimer * 16) * 2;
          ctx.drawImage(images.ninja, -28, -52 + bounce, 56, 54);
        }} else {{
          renderFallbackPlayer();
        }}
      }} else {{
        // Ground Idle: 4-frame breathing/blinking cycle at 4 FPS
        if (images.ninja_idle && images.ninja_idle.complete) {{
          const frame = Math.floor(player.idleAnimTimer * 4) % 4;
          ctx.drawImage(images.ninja_idle, frame * 64, 0, 64, 64, -28, -54, 56, 56);
        }} else if (images.ninja && images.ninja.complete) {{
          ctx.drawImage(images.ninja, -28, -52, 56, 54);
        }} else {{
          renderFallbackPlayer();
        }}
      }}

      ctx.restore();
    }}

    function renderFallbackPlayer() {{
      ctx.fillStyle = '#2563eb';
      ctx.fillRect(-16, -48, 32, 48);
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(player.facingRight ? 2 : -10, -38, 8, 6);
    }}

    function renderHitboxes() {{
      const st = stages[currentStage];
      ctx.save();
      ctx.lineWidth = 1.5;

      for (const obj of st.objects) {{
        const isSelected = (selectedObject === obj);
        if (obj.type === 'ground') {{
          ctx.strokeStyle = isSelected ? '#a855f7' : 'rgba(34, 197, 94, 0.85)';
          ctx.strokeRect(obj.x, obj.y, obj.w, obj.h);
        }} else if (obj.type === 'platform') {{
          ctx.strokeStyle = isSelected ? '#a855f7' : 'rgba(56, 189, 248, 0.85)';
          ctx.strokeRect(obj.x, obj.y, obj.w, obj.h);
        }} else if (obj.type === 'hazard' || obj.type === 'hazard_spin') {{
          ctx.strokeStyle = isSelected ? '#a855f7' : 'rgba(239, 68, 68, 0.9)';
          ctx.strokeRect(obj.x, obj.y, obj.w, obj.h);
        }} else if (obj.type === 'prop') {{
          ctx.strokeStyle = isSelected ? '#a855f7' : 'rgba(234, 179, 8, 0.6)';
          ctx.strokeRect(obj.x, obj.y, obj.w, obj.h);
        }} else if (obj.type === 'orb') {{
          ctx.strokeStyle = isSelected ? '#a855f7' : 'rgba(250, 204, 21, 0.9)';
          ctx.beginPath();
          ctx.arc(obj.x, obj.y, obj.r, 0, Math.PI * 2);
          ctx.stroke();
        }}

        if (editMode) {{
          ctx.fillStyle = isSelected ? '#facc15' : 'rgba(255,255,255,0.85)';
          ctx.font = '10px monospace';
          ctx.fillText(obj.id, obj.x + 4, obj.y + 12);
        }}
      }}

      ctx.strokeStyle = 'rgba(244, 63, 94, 0.9)';
      ctx.strokeRect(player.x - 16, player.y - 48, 32, 48);

      ctx.restore();
    }}

    switchStage({default_level});
    requestAnimationFrame(gameLoop);
  </script>
</body>
</html>
'''

files_to_generate = [
    ("autumn_maple_mobile_preview.html", 3),
    ("twilight_sanctuary_mobile_preview.html", 2),
    ("bamboo_village_mobile_preview.html", 1),
]

for filename, def_level in files_to_generate:
    out_path = os.path.join(artifact_dir, filename)
    content = build_html(default_level=def_level)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved {out_path} ({len(content)} bytes)")
