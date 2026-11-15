import base64
import json
import os

art_dir = r"C:\Users\User\.gemini\antigravity\brain\8549168d-c34b-4d73-ab24-be6264661fb8"

def to_b64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        ext = path.split(".")[-1]
        mime = "image/png" if ext == "png" else "image/jpeg"
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode("utf-8")

biome_names = [
    ("bamboo_grove", "Bamboo Grove"),
    ("mountain_pass", "Mountain Pass"),
    ("forest_road", "Forest Road"),
    ("torii_gate", "Torii Gate Trail"),
    ("river_crossing", "River Crossing"),
    ("village_street", "Village Street"),
    ("shoreline_harbor", "Shoreline & Harbor"),
    ("cave_entrance", "Cave Entrance")
]

biomes_dict = {}
for code, title in biome_names:
    biomes_dict[code] = {
        "title": title,
        "day": to_b64(f"assets/images/panoramic_biomes/{code}_day.png"),
        "night": to_b64(f"assets/images/panoramic_biomes/{code}_night.png")
    }

assets_dict = {
    "ashigaru": to_b64("assets/images/foes/ashigaru.png"),
    "hitodama": to_b64("assets/images/foes/hitodama.png"),
    "karakasa": to_b64("assets/images/foes/karakasa.png"),
    "oni": to_b64("assets/images/foes/oni.png"),
    "ronin": to_b64("assets/images/foes/ronin.png"),
    "tengu": to_b64("assets/images/foes/tengu.png"),
    "magatama": to_b64("assets/images/items/magatama_gem.png"),
    "ofuda": to_b64("assets/images/items/ofuda_talisman.png"),
    "caltrops": to_b64("assets/images/items/caltrops.png"),
    "sakura": to_b64("assets/images/cutouts/sakura_tree_1.png"),
    "stone_well": to_b64("assets/images/cutouts/stone_well.png"),
    "arched_bridge": to_b64("assets/images/cutouts/arched_bridge.png"),
    "torii": to_b64("assets/images/cutouts/torii_gate_sacred.png") or to_b64("assets/images/cutouts/torii_gate.png"),
    "pagoda": to_b64("assets/images/cutouts/pagoda_tall.png") or to_b64("assets/images/cutouts/pagoda_shrine_grounded.png"),
    "lantern_glowing": to_b64("assets/images/cutouts/lantern_post_glowing.png"),
    "lantern_clean": to_b64("assets/images/cutouts/lantern_post_clean.png"),
    "boardwalk": to_b64("assets/images/cutouts/boardwalk_continuous.png"),
    "platform": to_b64("assets/images/cutouts/wooden_boardwalk_platform.png"),
    "ninja_run": to_b64("assets/images/spritesheet_ninja_run.png"),
    "ninja_jump": to_b64("assets/images/spritesheet_ninja_jump.png"),
    "ninja_attack": to_b64("assets/images/spritesheet_ninja_attack.png"),
}

json_biomes = json.dumps(biomes_dict)
json_assets = json.dumps(assets_dict)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shinobi Sprint - Feudal World Playable Showcase</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 0.8; transform: scale(1); }}
      50% {{ opacity: 1; transform: scale(1.08); }}
    }}
    .pulse-glow {{ animation: pulseGlow 2.5s infinite ease-in-out; }}
    canvas {{ image-rendering: pixelated; }}
  </style>
</head>
<body class="bg-[#080d18] text-slate-100 min-h-screen flex flex-col items-center justify-center p-3 font-sans antialiased">

  <!-- Header -->
  <header class="max-w-4xl w-full text-center mb-4">
    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-semibold tracking-widest uppercase mb-1.5">
      <span>★ Live Feudal Environment & Foes Showcase ★</span>
    </div>
    <h1 class="text-3xl md:text-4xl font-extrabold text-amber-200 tracking-wider flex items-center justify-center gap-3">
      <span>⛩️</span> SHINOBI SPRINT <span>⚔️</span>
    </h1>
    <p class="text-slate-400 text-xs md:text-sm mt-1 max-w-xl mx-auto">
      Featuring 8 Panoramic Biomes, Feudal Foes (Ashigaru, Hitodama, Karakasa, Oni), Magatama & Ofuda Collectibles, and Ninja Combat!
    </p>
  </header>

  <!-- Main Container -->
  <div class="flex flex-col xl:flex-row items-center justify-center gap-6 max-w-6xl w-full">

    <!-- Phone Simulator Bezel -->
    <div class="relative flex-shrink-0">
      <div class="w-[360px] h-[660px] bg-slate-950 rounded-[44px] p-2.5 shadow-2xl border-4 border-slate-700/80 ring-2 ring-amber-500/30 relative overflow-hidden flex flex-col">
        
        <!-- Camera Notch -->
        <div class="absolute top-3 left-1/2 -translate-x-1/2 w-24 h-4 bg-black rounded-full z-50 flex items-center justify-center">
          <div class="w-2 h-2 rounded-full bg-slate-800"></div>
        </div>

        <!-- Canvas Container -->
        <div class="relative w-full h-full rounded-[36px] overflow-hidden bg-[#0a0f1d]">
          <canvas id="gameCanvas" width="360" height="660" class="w-full h-full block cursor-pointer"></canvas>

          <!-- On-screen Touch Controls -->
          <div class="absolute bottom-3 left-3 right-3 flex items-center justify-between pointer-events-none z-30">
            <div class="flex gap-2 pointer-events-auto">
              <button id="btnSlash" class="w-12 h-12 rounded-full bg-red-600/80 hover:bg-red-500 text-white font-bold text-xs flex items-center justify-center border-2 border-red-300 shadow-lg active:scale-95 transition-transform backdrop-blur-sm">
                ⚔️ Slash
              </button>
              <button id="btnShuriken" class="w-12 h-12 rounded-full bg-indigo-600/80 hover:bg-indigo-500 text-white font-bold text-xs flex items-center justify-center border-2 border-indigo-300 shadow-lg active:scale-95 transition-transform backdrop-blur-sm">
                🌀 Throw
              </button>
            </div>
            <button id="btnJump" class="pointer-events-auto px-5 h-12 rounded-full bg-amber-500/80 hover:bg-amber-400 text-slate-950 font-black text-sm flex items-center justify-center border-2 border-amber-200 shadow-lg active:scale-95 transition-transform backdrop-blur-sm">
              ⬆ JUMP
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Interactive Dashboard & Biome Controls -->
    <div class="flex-1 max-w-xl flex flex-col gap-4 bg-slate-900/80 border border-slate-700/80 p-5 rounded-2xl shadow-xl backdrop-blur-md">
      
      <!-- Quick Status Strip -->
      <div class="grid grid-cols-3 gap-2 text-center">
        <div class="bg-slate-800/90 border border-slate-700 p-2.5 rounded-xl">
          <span class="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">SCORE</span>
          <span id="uiScore" class="text-xl font-black text-amber-300">0</span>
        </div>
        <div class="bg-slate-800/90 border border-slate-700 p-2.5 rounded-xl">
          <span class="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">FOES SLAIN</span>
          <span id="uiFoes" class="text-xl font-black text-red-400">0</span>
        </div>
        <div class="bg-slate-800/90 border border-slate-700 p-2.5 rounded-xl">
          <span class="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">LIGHTING</span>
          <button id="uiToggleDay" class="mt-0.5 px-2 py-0.5 rounded-md text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40 hover:bg-amber-500/30 transition-colors">
            🌙 Night
          </button>
        </div>
      </div>

      <!-- Biome Switcher -->
      <div>
        <label class="text-xs font-bold uppercase tracking-wider text-amber-300 block mb-2">
          Select Feudal Biome (8 Environments)
        </label>
        <div id="biomeButtons" class="grid grid-cols-2 sm:grid-cols-4 gap-2">
          <!-- Buttons generated in JS -->
        </div>
      </div>

      <!-- Controls Guide -->
      <div class="bg-slate-950/80 border border-slate-800 p-3.5 rounded-xl text-xs space-y-1.5 text-slate-300">
        <div class="font-bold text-amber-200 text-sm mb-1">🎮 Controls & Combos:</div>
        <div class="flex justify-between border-b border-slate-800/80 pb-1">
          <span><kbd class="bg-slate-800 px-1.5 py-0.5 rounded text-amber-300">Space</kbd> or <kbd class="bg-slate-800 px-1.5 py-0.5 rounded">Tap</kbd></span>
          <span class="text-slate-400">Jump (Double Jump supported!)</span>
        </div>
        <div class="flex justify-between border-b border-slate-800/80 pb-1">
          <span><kbd class="bg-slate-800 px-1.5 py-0.5 rounded text-amber-300">Z</kbd> or <kbd class="bg-slate-800 px-1.5 py-0.5 rounded">J</kbd></span>
          <span class="text-slate-400">Katana Slash (Melee strike on Foes)</span>
        </div>
        <div class="flex justify-between border-b border-slate-800/80 pb-1">
          <span><kbd class="bg-slate-800 px-1.5 py-0.5 rounded text-amber-300">X</kbd> or <kbd class="bg-slate-800 px-1.5 py-0.5 rounded">K</kbd></span>
          <span class="text-slate-400">Shuriken Projectile Throw</span>
        </div>
        <div class="flex justify-between">
          <span><kbd class="bg-slate-800 px-1.5 py-0.5 rounded text-amber-300">D</kbd></span>
          <span class="text-slate-400">Toggle Day / Night</span>
        </div>
      </div>

      <!-- Lore & Items -->
      <div class="bg-amber-950/20 border border-amber-900/30 p-3 rounded-xl text-xs text-amber-200/90 leading-relaxed">
        <span class="font-bold text-amber-300">💠 Collectibles:</span>
        <span class="font-semibold text-cyan-300">Magatama Jewels (+500)</span> boost ancestral spirit;
        <span class="font-semibold text-yellow-300">Ofuda Talismans (+250)</span> ward against yokai;
        <span class="font-semibold text-emerald-300">Sushi (+1000)</span> restores vitality.
      </div>
    </div>
  </div>

  <script>
    const BIOMES = {json_biomes};
    const ASSETS = {json_assets};

    // Game State
    let currentBiome = 'bamboo_grove';
    let isDay = false;
    let score = 0;
    let foesSlain = 0;

    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const W = canvas.width;
    const H = canvas.height;
    const groundY = 530;

    // Preloaded Images Cache
    const imgCache = {{}};
    function preloadAll() {{
      for (const [k, v] of Object.entries(ASSETS)) {{
        if (v) {{
          const img = new Image();
          img.src = v;
          imgCache[k] = img;
        }}
      }}
      for (const [k, v] of Object.entries(BIOMES)) {{
        if (v.day) {{
          const imgDay = new Image();
          imgDay.src = v.day;
          imgCache[k + '_day'] = imgDay;
        }}
        if (v.night) {{
          const imgNight = new Image();
          imgNight.src = v.night;
          imgCache[k + '_night'] = imgNight;
        }}
      }}
    }}
    preloadAll();

    // Player State
    const player = {{
      x: 70,
      y: groundY - 58,
      w: 58,
      h: 58,
      vy: 0,
      gravity: 0.58,
      jumpForce: -13,
      jumpsRemaining: 2,
      isOnGround: true,
      state: 'run', // 'run', 'jump', 'attack'
      frame: 0,
      animTimer: 0,
      attackCooldown: 0,
    }};

    // Foes
    let foes = [
      {{ type: 'ashigaru', x: 260, y: groundY - 56, w: 56, h: 56, startX: 260, speed: 0.8, range: 45, alive: true }},
      {{ type: 'hitodama', x: 190, y: 340, w: 42, h: 42, baseVy: 340, t: 0, alive: true }},
      {{ type: 'karakasa', x: 310, y: groundY - 52, w: 46, h: 52, t: 0, alive: true }}
    ];

    // Collectibles
    let items = [
      {{ type: 'magatama', x: 140, y: 390, w: 32, h: 32, collected: false, t: 0 }},
      {{ type: 'ofuda', x: 230, y: 440, w: 30, h: 30, collected: false, t: 1 }},
      {{ type: 'magatama', x: 280, y: 360, w: 32, h: 32, collected: false, t: 2 }}
    ];

    // Shurikens
    let shurikens = [];

    // Floating text FX
    let floatTexts = [];

    // Platforms
    const platforms = [
      {{ x: 110, y: 430, w: 100, h: 22 }},
      {{ x: 220, y: 370, w: 110, h: 22 }}
    ];

    // Parallax scroll
    let bgScroll = 0;

    // Controls
    function jump() {{
      if (player.jumpsRemaining > 0) {{
        player.vy = player.jumpForce;
        player.jumpsRemaining--;
        player.isOnGround = false;
        player.state = 'jump';
      }}
    }}

    function slash() {{
      player.state = 'attack';
      player.attackCooldown = 18;

      // Check hit with foes in melee range
      const attackRange = 90;
      foes.forEach(f => {{
        if (f.alive && Math.abs((player.x + 30) - (f.x + f.w/2)) < attackRange && Math.abs(player.y - f.y) < 70) {{
          f.alive = false;
          foesSlain++;
          score += 200;
          updateHUD();
          floatTexts.push({{ text: 'SLASH! +200', x: f.x, y: f.y - 15, life: 35, color: '#f87171' }});
        }}
      }});
    }}

    function throwShuriken() {{
      shurikens.push({{
        x: player.x + 40,
        y: player.y + 25,
        vx: 8.5,
        rot: 0
      }});
    }}

    // Input listeners
    window.addEventListener('keydown', e => {{
      if (e.code === 'Space' || e.code === 'ArrowUp') {{ e.preventDefault(); jump(); }}
      if (e.code === 'KeyZ' || e.code === 'KeyJ') {{ e.preventDefault(); slash(); }}
      if (e.code === 'KeyX' || e.code === 'KeyK') {{ e.preventDefault(); throwShuriken(); }}
      if (e.code === 'KeyD') {{ toggleDayNight(); }}
    }});

    document.getElementById('btnJump').addEventListener('click', jump);
    document.getElementById('btnSlash').addEventListener('click', slash);
    document.getElementById('btnShuriken').addEventListener('click', throwShuriken);
    canvas.addEventListener('click', (e) => {{
      const rect = canvas.getBoundingClientRect();
      const clickY = (e.clientY - rect.top) * (canvas.height / rect.height);
      if (clickY < 480) jump();
    }});

    function toggleDayNight() {{
      isDay = !isDay;
      document.getElementById('uiToggleDay').innerText = isDay ? '☀️ Day' : '🌙 Night';
      document.getElementById('uiToggleDay').className = isDay 
        ? 'mt-0.5 px-2 py-0.5 rounded-md text-xs font-bold bg-amber-400/20 text-amber-200 border border-amber-400/40 hover:bg-amber-400/30'
        : 'mt-0.5 px-2 py-0.5 rounded-md text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 hover:bg-indigo-500/30';
    }}
    document.getElementById('uiToggleDay').addEventListener('click', toggleDayNight);

    function updateHUD() {{
      document.getElementById('uiScore').innerText = score;
      document.getElementById('uiFoes').innerText = foesSlain;
    }}

    // Render Biome Selector Buttons
    const btnContainer = document.getElementById('biomeButtons');
    Object.keys(BIOMES).forEach(bKey => {{
      const b = BIOMES[bKey];
      const btn = document.createElement('button');
      btn.className = `p-2 rounded-lg text-xs font-bold text-left border transition-all ${{
        bKey === currentBiome 
          ? 'bg-amber-500/20 border-amber-400 text-amber-200 ring-1 ring-amber-400' 
          : 'bg-slate-800/80 border-slate-700 text-slate-300 hover:bg-slate-800 hover:border-slate-500'
      }}`;
      btn.innerText = b.title;
      btn.addEventListener('click', () => {{
        currentBiome = bKey;
        resetBiomeFoes(bKey);
        Array.from(btnContainer.children).forEach(c => {{
          c.className = 'p-2 rounded-lg text-xs font-bold text-left border transition-all bg-slate-800/80 border-slate-700 text-slate-300 hover:bg-slate-800';
        }});
        btn.className = 'p-2 rounded-lg text-xs font-bold text-left border transition-all bg-amber-500/20 border-amber-400 text-amber-200 ring-1 ring-amber-400';
      }});
      btnContainer.appendChild(btn);
    }});

    function resetBiomeFoes(biome) {{
      if (biome === 'mountain_pass') {{
        foes = [
          {{ type: 'tengu', x: 270, y: groundY - 60, w: 56, h: 60, startX: 270, speed: 0.9, range: 40, alive: true }},
          {{ type: 'oni', x: 190, y: groundY - 65, w: 60, h: 65, startX: 190, speed: 0.4, range: 25, alive: true }}
        ];
      }} else if (biome === 'river_crossing') {{
        foes = [
          {{ type: 'karakasa', x: 260, y: groundY - 52, w: 46, h: 52, t: 0, alive: true }},
          {{ type: 'hitodama', x: 180, y: 350, w: 42, h: 42, baseVy: 350, t: 0, alive: true }}
        ];
      }} else {{
        foes = [
          {{ type: 'ashigaru', x: 260, y: groundY - 56, w: 56, h: 56, startX: 260, speed: 0.8, range: 45, alive: true }},
          {{ type: 'hitodama', x: 190, y: 340, w: 42, h: 42, baseVy: 340, t: 0, alive: true }},
          {{ type: 'karakasa', x: 310, y: groundY - 52, w: 46, h: 52, t: 0, alive: true }}
        ];
      }}
      items.forEach(it => it.collected = false);
    }}

    // MAIN GAME LOOP
    function update() {{
      // Background scroll
      bgScroll += 1.2;

      // Player Physics
      player.vy += player.gravity;
      player.y += player.vy;

      // Check platform collisions
      platforms.forEach(p => {{
        if (player.vy >= 0 &&
            player.x + player.w > p.x &&
            player.x < p.x + p.w &&
            player.y + player.h >= p.y &&
            player.y + player.h <= p.y + 16) {{
          player.y = p.y - player.h;
          player.vy = 0;
          player.isOnGround = true;
          player.jumpsRemaining = 2;
        }}
      }});

      // Floor collision
      if (player.y >= groundY - player.h) {{
        player.y = groundY - player.h;
        player.vy = 0;
        player.isOnGround = true;
        player.jumpsRemaining = 2;
      }}

      // Attack countdown
      if (player.attackCooldown > 0) {{
        player.attackCooldown--;
        if (player.attackCooldown === 0) {{
          player.state = player.isOnGround ? 'run' : 'jump';
        }}
      }} else {{
        if (player.isOnGround) player.state = 'run';
      }}

      // Animate player frames
      player.animTimer++;
      if (player.animTimer >= 5) {{
        player.animTimer = 0;
        player.frame = (player.frame + 1) % 8;
      }}

      // Update Foes
      foes.forEach(f => {{
        if (!f.alive) return;
        if (f.type === 'ashigaru' || f.type === 'tengu' || f.type === 'oni') {{
          f.x += f.speed;
          if (Math.abs(f.x - f.startX) > f.range) f.speed *= -1;
        }} else if (f.type === 'hitodama') {{
          f.t += 0.05;
          f.y = f.baseVy + Math.sin(f.t) * 22;
        }} else if (f.type === 'karakasa') {{
          f.t += 0.08;
          f.y = (groundY - f.h) - Math.abs(Math.sin(f.t)) * 40;
        }}
      }});

      // Update Shurikens
      for (let i = shurikens.length - 1; i >= 0; i--) {{
        const s = shurikens[i];
        s.x += s.vx;
        s.rot += 0.35;
        foes.forEach(f => {{
          if (f.alive && Math.abs(s.x - (f.x + f.w/2)) < f.w/2 && Math.abs(s.y - (f.y + f.h/2)) < f.h/2) {{
            f.alive = false;
            foesSlain++;
            score += 200;
            updateHUD();
            floatTexts.push({{ text: 'HIT! +200', x: f.x, y: f.y - 10, life: 30, color: '#a78bfa' }});
            shurikens.splice(i, 1);
          }}
        }});
        if (s.x > W + 40) shurikens.splice(i, 1);
      }}

      // Check Collectibles
      items.forEach(it => {{
        if (!it.collected) {{
          it.t += 0.06;
          const bobY = it.y + Math.sin(it.t) * 4;
          if (Math.abs(player.x + player.w/2 - (it.x + it.w/2)) < 30 &&
              Math.abs(player.y + player.h/2 - (bobY + it.h/2)) < 35) {{
            it.collected = true;
            const pts = it.type === 'magatama' ? 500 : 250;
            score += pts;
            updateHUD();
            floatTexts.push({{
              text: `+${{pts}} ${{it.type.toUpperCase()}}!`,
              x: it.x - 20,
              y: it.y - 15,
              life: 40,
              color: it.type === 'magatama' ? '#38bdf8' : '#facc15'
            }});
          }}
        }}
      }});

      // Floating Texts
      for (let i = floatTexts.length - 1; i >= 0; i--) {{
        const ft = floatTexts[i];
        ft.y -= 0.8;
        ft.life--;
        if (ft.life <= 0) floatTexts.splice(i, 1);
      }}
    }}

    function draw() {{
      ctx.clearRect(0, 0, W, H);

      // 1. Panoramic Biome Background
      const bgImgKey = currentBiome + (isDay ? '_day' : '_night');
      const bgImg = imgCache[bgImgKey];
      if (bgImg && bgImg.complete && bgImg.naturalWidth > 0) {{
        const scrollX = (bgScroll * 0.4) % W;
        ctx.drawImage(bgImg, -scrollX, 0, W, H);
        ctx.drawImage(bgImg, W - scrollX, 0, W, H);
      }} else {{
        const grad = ctx.createLinearGradient(0, 0, 0, H);
        if (isDay) {{
          grad.addColorStop(0, '#5888a5');
          grad.addColorStop(1, '#a8c2a8');
        }} else {{
          grad.addColorStop(0, '#060a14');
          grad.addColorStop(1, '#111d2e');
        }}
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, W, H);
      }}

      // 2. Parallax Midground Scenery (Pagoda & Torii)
      const pagodaImg = imgCache['pagoda'];
      if (pagodaImg && pagodaImg.complete) {{
        ctx.drawImage(pagodaImg, 20, groundY - 140, 95, 140);
      }}

      const sakuraImg = imgCache['sakura'];
      if (sakuraImg && sakuraImg.complete) {{
        ctx.drawImage(sakuraImg, 260, groundY - 110, 85, 110);
      }}

      const wellImg = imgCache['stone_well'];
      if (wellImg && wellImg.complete) {{
        ctx.drawImage(wellImg, 175, groundY - 60, 48, 60);
      }}

      // 3. Elevated Platforms
      const platImg = imgCache['platform'];
      platforms.forEach((p, idx) => {{
        if (platImg && platImg.complete) {{
          ctx.drawImage(platImg, p.x, p.y, p.w, p.h);
        }} else {{
          ctx.fillStyle = '#6b432a';
          ctx.fillRect(p.x, p.y, p.w, p.h);
        }}
        // Timber support pillar
        ctx.fillStyle = 'rgba(40, 24, 16, 0.7)';
        ctx.fillRect(p.x + 12, p.y + p.h, 6, groundY - (p.y + p.h));
        ctx.fillRect(p.x + p.w - 18, p.y + p.h, 6, groundY - (p.y + p.h));
      }});

      // 4. Collectibles
      items.forEach(it => {{
        if (!it.collected) {{
          const itemImg = imgCache[it.type];
          const bobY = it.y + Math.sin(it.t) * 4;
          if (itemImg && itemImg.complete) {{
            ctx.drawImage(itemImg, it.x, bobY, it.w, it.h);
          }} else {{
            ctx.fillStyle = it.type === 'magatama' ? '#38bdf8' : '#eab308';
            ctx.beginPath();
            ctx.arc(it.x + it.w/2, bobY + it.h/2, 12, 0, Math.PI * 2);
            ctx.fill();
          }}
        }}
      }});

      // 5. Continuous Boardwalk Floor
      const bwImg = imgCache['boardwalk'];
      if (bwImg && bwImg.complete) {{
        ctx.drawImage(bwImg, 0, groundY, W, 48);
      }} else {{
        ctx.fillStyle = isDay ? '#8a5a36' : '#3d2516';
        ctx.fillRect(0, groundY, W, 50);
        ctx.strokeStyle = '#2b1a10';
        ctx.lineWidth = 2;
        for (let x = 0; x < W; x += 36) {{
          ctx.beginPath();
          ctx.moveTo(x, groundY);
          ctx.lineTo(x, groundY + 50);
          ctx.stroke();
        }}
      }}

      // Lantern Posts with Glow
      const lanternImg = imgCache[isDay ? 'lantern_clean' : 'lantern_glowing'];
      if (lanternImg && lanternImg.complete) {{
        ctx.drawImage(lanternImg, 40, groundY - 68, 28, 68);
        ctx.drawImage(lanternImg, 310, groundY - 68, 28, 68);
        if (!isDay) {{
          const radial = ctx.createRadialGradient(54, groundY - 45, 2, 54, groundY - 45, 35);
          radial.addColorStop(0, 'rgba(251, 191, 36, 0.4)');
          radial.addColorStop(1, 'rgba(251, 191, 36, 0)');
          ctx.fillStyle = radial;
          ctx.beginPath();
          ctx.arc(54, groundY - 45, 35, 0, Math.PI * 2);
          ctx.fill();
        }}
      }}

      // 6. Feudal Foes
      foes.forEach(f => {{
        if (!f.alive) return;
        const foeImg = imgCache[f.type];
        if (foeImg && foeImg.complete) {{
          ctx.drawImage(foeImg, f.x, f.y, f.w, f.h);
        }} else {{
          ctx.fillStyle = '#dc2626';
          ctx.fillRect(f.x, f.y, f.w, f.h);
        }}
      }});

      // 7. Shurikens
      shurikens.forEach(s => {{
        ctx.save();
        ctx.translate(s.x, s.y);
        ctx.rotate(s.rot);
        ctx.fillStyle = '#94a3b8';
        ctx.beginPath();
        for (let i = 0; i < 4; i++) {{
          ctx.lineTo(0, -9);
          ctx.lineTo(3, -3);
          ctx.rotate(Math.PI / 2);
        }}
        ctx.closePath();
        ctx.fill();
        ctx.restore();
      }});

      // 8. Ninja Player
      let ninjaImg = imgCache['ninja_run'];
      let frameW = 64, frameH = 64;
      if (player.state === 'jump') ninjaImg = imgCache['ninja_jump'] || ninjaImg;
      if (player.state === 'attack') ninjaImg = imgCache['ninja_attack'] || ninjaImg;

      if (ninjaImg && ninjaImg.complete && ninjaImg.naturalWidth > 0) {{
        const frameIndex = player.state === 'run' ? player.frame : 0;
        ctx.drawImage(
          ninjaImg,
          frameIndex * frameW, 0, frameW, frameH,
          player.x, player.y, player.w, player.h
        );
      }} else {{
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(player.x, player.y, player.w, player.h);
        ctx.fillStyle = '#ef4444';
        ctx.fillRect(player.x + 8, player.y + 12, player.w - 16, 8);
      }}

      // Katana Slash Arc FX
      if (player.state === 'attack') {{
        ctx.strokeStyle = 'rgba(239, 68, 68, 0.85)';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(player.x + player.w + 10, player.y + player.h/2, 28, -Math.PI*0.4, Math.PI*0.4);
        ctx.stroke();
      }}

      // 9. Floating Text Effects
      floatTexts.forEach(ft => {{
        ctx.font = 'bold 12px sans-serif';
        ctx.fillStyle = ft.color;
        ctx.shadowColor = 'black';
        ctx.shadowBlur = 4;
        ctx.fillText(ft.text, ft.x, ft.y);
        ctx.shadowBlur = 0;
      }});

      // 10. Top HUD on Canvas
      ctx.fillStyle = 'rgba(15, 23, 42, 0.75)';
      ctx.roundRect(12, 14, 150, 32, 10);
      ctx.fill();
      ctx.strokeStyle = 'rgba(245, 158, 11, 0.4)';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      ctx.fillStyle = '#fef08a';
      ctx.font = 'bold 11px sans-serif';
      ctx.fillText(BIOMES[currentBiome].title.toUpperCase(), 22, 34);
    }}

    function loop() {{
      update();
      draw();
      requestAnimationFrame(loop);
    }}
    requestAnimationFrame(loop);
  </script>
</body>
</html>
"""

out_art = os.path.join(art_dir, "shinobi_sprint_game_showcase.html")
with open(out_art, "w", encoding="utf-8") as f:
    f.write(html_template)
print(f"Saved showcase to: {out_art}")

out_web = "web/game_showcase.html"
with open(out_web, "w", encoding="utf-8") as f:
    f.write(html_template)
print(f"Saved showcase to: {out_web}")
