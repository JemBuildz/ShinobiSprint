import base64
import os

artifact_dir = r"C:\Users\User\.gemini\antigravity\brain\8d1fe0d7-a367-49a2-ba0b-1e27387c2271"

def to_b64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

bgs = {
    "l1": to_b64("assets/images/backgrounds/farthest_sky.png"),
    "l2": to_b64("assets/images/backgrounds/deep_background.png"),
    "l3": to_b64("assets/images/backgrounds/mid_background.png"),
    "l4": to_b64("assets/images/backgrounds/midground_lamps.png"),
    "l5": to_b64("assets/images/backgrounds/foreground_path.png"),
}

ninja_run = to_b64("assets/images/spritesheet_ninja_run.png")
ninja_jump = to_b64("assets/images/spritesheet_ninja_jump.png")

template = """<!DOCTYPE html>
<html>
<head>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-2">
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-4 shadow-lg flex flex-col md:flex-row items-center gap-4 max-w-xl mx-auto">
    
    <!-- Mini Phone Screen -->
    <div class="relative w-[210px] h-[380px] bg-[#090D1A] rounded-[28px] border-4 border-slate-700/80 shadow-2xl overflow-hidden flex-shrink-0 cursor-pointer select-none" id="viewport">
      
      <!-- Top Notch -->
      <div class="absolute top-2 left-1/2 -translate-x-1/2 w-16 h-3.5 bg-black rounded-full z-30"></div>
      
      <!-- Canvas -->
      <canvas id="canvas" width="210" height="380" class="absolute inset-0 w-full h-full"></canvas>

      <!-- HUD Score -->
      <div class="absolute top-7 left-1/2 -translate-x-1/2 z-20 pointer-events-none">
        <div class="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-[#090D1A]/90 border border-[#C5A059] shadow-md backdrop-blur-sm">
          <span class="text-xs">🏆</span>
          <span class="text-[10px] text-[#E2C99B] font-bold">SCORE:</span>
          <span id="scoreVal" class="text-xs font-black text-[#FFB74D]">0</span>
        </div>
      </div>

      <!-- Jump Overlay Hint -->
      <div class="absolute bottom-5 left-1/2 -translate-x-1/2 z-20 pointer-events-none text-center">
        <div class="px-2.5 py-1 rounded-full bg-[#090D1A]/85 border border-[#C5A059] backdrop-blur-sm">
          <span class="text-[9px] font-bold text-[#FFF7ED] tracking-wider">TAP TO JUMP</span>
        </div>
      </div>
    </div>

    <!-- Info & Controls -->
    <div class="flex-1 flex flex-col justify-between h-[380px] py-1 text-left w-full">
      <div>
        <div class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-400 text-[10px] font-semibold uppercase tracking-wider mb-1.5">
          <span>⛩️ Shinobi Sprint Mobile Preview</span>
        </div>
        <h2 class="text-base font-black text-[var(--foreground)] tracking-wide">Night Forest Parallax</h2>
        <p class="text-[var(--muted-foreground)] text-xs mt-1 leading-relaxed">
          5-layer Flame parallax engine with static moon, ascending depth velocities, and nocturnal UI theme.
        </p>

        <!-- Layer Legend -->
        <div class="space-y-1.5 mt-3 text-[11px]">
          <div class="flex items-center justify-between p-1.5 rounded bg-[var(--background)] border border-[var(--border)]">
            <span class="text-slate-300 font-medium">1. Farthest Sky</span>
            <span class="text-emerald-400 font-mono text-[10px] font-bold">0.0x Static Moon</span>
          </div>
          <div class="flex items-center justify-between p-1.5 rounded bg-[var(--background)] border border-[var(--border)]">
            <span class="text-slate-300 font-medium">2. Deep Mountains</span>
            <span class="text-blue-400 font-mono text-[10px] font-bold">0.25x</span>
          </div>
          <div class="flex items-center justify-between p-1.5 rounded bg-[var(--background)] border border-[var(--border)]">
            <span class="text-slate-300 font-medium">3. Mid Bamboo</span>
            <span class="text-teal-400 font-mono text-[10px] font-bold">0.50x</span>
          </div>
          <div class="flex items-center justify-between p-1.5 rounded bg-[var(--background)] border border-[var(--border)]">
            <span class="text-slate-300 font-medium">4. Midground Lamps</span>
            <span class="text-amber-400 font-mono text-[10px] font-bold">0.75x</span>
          </div>
          <div class="flex items-center justify-between p-1.5 rounded bg-[var(--background)] border border-[var(--border)]">
            <span class="text-slate-300 font-medium">5. Foreground Path</span>
            <span class="text-orange-400 font-mono text-[10px] font-bold">1.00x</span>
          </div>
        </div>
      </div>

      <div class="space-y-2 mt-2">
        <button id="btnJump" class="w-full py-2 rounded-xl bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-500 hover:to-amber-400 text-black font-black text-xs tracking-wider shadow-md hover:shadow-amber-500/20 active:scale-95 transition-all">
          🥷 TAP TO JUMP (SPACE)
        </button>
        <p class="text-[10px] text-[var(--muted-foreground)] text-center">
          Click phone or press Space to leap over obstacles
        </p>
      </div>

    </div>

  </div>

  <script>
    const imgs = {
      l1: new Image(), l2: new Image(), l3: new Image(), l4: new Image(), l5: new Image(),
      run: new Image(), jump: new Image()
    };
    imgs.l1.src = "__L1__";
    imgs.l2.src = "__L2__";
    imgs.l3.src = "__L3__";
    imgs.l4.src = "__L4__";
    imgs.l5.src = "__L5__";
    imgs.run.src = "__NINJA_RUN__";
    imgs.jump.src = "__NINJA_JUMP__";

    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const speeds = [0.0, 0.25, 0.50, 0.75, 1.0];
    const offsets = [0, 0, 0, 0, 0];
    const baseSpeed = 100;

    const player = {
      x: 35, groundY: 285, y: 285, vy: 0, gravity: 900, jumpImpulse: -420,
      isJumping: false, frame: 0, frameTimer: 0
    };

    let score = 0, scoreAcc = 0;

    function jump() {
      if (!player.isJumping) {
        player.vy = player.jumpImpulse;
        player.isJumping = true;
        player.frame = 0;
      }
    }

    document.getElementById('viewport').addEventListener('click', jump);
    document.getElementById('btnJump').addEventListener('click', jump);
    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space') { e.preventDefault(); jump(); }
    });

    let last = performance.now();

    function drawLayer(img, offset) {
      if (!img.complete || img.naturalWidth === 0) return;
      const scale = canvas.height / img.naturalHeight;
      const w = img.naturalWidth * scale;
      const norm = (offset % w + w) % w;
      ctx.drawImage(img, -norm, 0, w, canvas.height);
      if (-norm + w < canvas.width) ctx.drawImage(img, -norm + w, 0, w, canvas.height);
    }

    function loop(now) {
      const dt = Math.min((now - last) / 1000, 0.1);
      last = now;

      ctx.fillStyle = '#090D1A';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      for (let i = 0; i < 5; i++) offsets[i] += baseSpeed * speeds[i] * dt;

      drawLayer(imgs.l1, offsets[0]);
      drawLayer(imgs.l2, offsets[1]);
      drawLayer(imgs.l3, offsets[2]);
      drawLayer(imgs.l4, offsets[3]);
      drawLayer(imgs.l5, offsets[4]);

      if (player.isJumping) {
        player.vy += player.gravity * dt;
        player.y += player.vy * dt;
        if (player.y >= player.groundY) {
          player.y = player.groundY;
          player.vy = 0;
          player.isJumping = false;
        }
      }

      player.frameTimer += dt;
      if (player.frameTimer >= 0.1) {
        player.frameTimer = 0;
        player.frame = (player.frame + 1) % (player.isJumping ? 4 : 5);
      }

      const spr = player.isJumping ? imgs.jump : imgs.run;
      if (spr.complete && spr.naturalWidth > 0) {
        ctx.drawImage(spr, player.frame * 64, 0, 64, 64, player.x, player.y - 45, 54, 54);
      }

      scoreAcc += dt * 8;
      if (scoreAcc >= 1) {
        score += Math.floor(scoreAcc);
        scoreAcc %= 1;
        document.getElementById('scoreVal').innerText = score;
      }

      requestAnimationFrame(loop);
    }

    requestAnimationFrame(loop);
  </script>
</body>
</html>"""

html = template.replace("__L1__", bgs["l1"])\
               .replace("__L2__", bgs["l2"])\
               .replace("__L3__", bgs["l3"])\
               .replace("__L4__", bgs["l4"])\
               .replace("__L5__", bgs["l5"])\
               .replace("__NINJA_RUN__", ninja_run)\
               .replace("__NINJA_JUMP__", ninja_jump)

out = os.path.join(artifact_dir, "mobile_preview_card.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: mobile_preview_card.html written")
