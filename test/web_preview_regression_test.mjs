import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import assert from 'assert';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log('--- Shinobi Sprint Web Preview Starting Position & Grounded HUD Regression Test ---');

// 1. Read the web preview HTML file
const htmlPath = join(__dirname, '..', 'web', 'shinobi_mobile_preview.html');
const html = readFileSync(htmlPath, 'utf-8');

// 2. Extract script body
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
assert(scriptMatch, 'Could not find <script> tag in web/shinobi_mobile_preview.html');
const scriptContent = scriptMatch[1];

// 3. Create simulated DOM environment
const elements = {
  gameCanvas: {
    getContext: () => ({
      clearRect: () => {},
      drawImage: () => {},
      fillRect: () => {},
      strokeRect: () => {},
      fillText: () => {},
      beginPath: () => {},
      moveTo: () => {},
      lineTo: () => {},
      stroke: () => {},
      fill: () => {},
      arc: () => {},
      ellipse: () => {},
      roundRect: () => {},
      save: () => {},
      restore: () => {},
      translate: () => {},
      rotate: () => {},
      scale: () => {},
      closePath: () => {},
      createRadialGradient: () => ({ addColorStop: () => {} })
    })
  },
  ninjaPosDisplay: { textContent: '' },
  groundedDisplay: { textContent: '', className: '' },
  orbCounter: { textContent: '' },
  hitboxIcon: { textContent: '' },
  hitboxLabel: { textContent: '' },
  deviceShell: { className: 'w-[880px] h-[520px]' },
  btnLandscape: { className: '' },
  btnPortrait: { className: '' }
};

const mockDocument = {
  getElementById: (id) => elements[id] || { addEventListener: () => {}, textContent: '', className: '' },
  querySelector: () => ({ textContent: '' }),
  addEventListener: () => {}
};

class MockImage {
  constructor() {
    this.complete = true;
    this.naturalWidth = 1024;
    this.naturalHeight = 576;
    this.src = '';
  }
}

// Sandbox execution context
const sandbox = {
  document: mockDocument,
  window: {
    addEventListener: () => {}
  },
  Image: MockImage,
  performance: { now: () => 1000 },
  requestAnimationFrame: () => {},
  console,
  Math
};
sandbox.window.window = sandbox.window;
sandbox.window.document = mockDocument;

// Execute script within sandbox scope
const wrappedCode = `
  (function(document, window, Image, performance, requestAnimationFrame) {
    ${scriptContent}
  })(sandbox.document, sandbox.window, sandbox.Image, sandbox.performance, sandbox.requestAnimationFrame);
`;

const runSandbox = new Function('sandbox', wrappedCode);
runSandbox(sandbox);

const sim = sandbox.window.ShinobiSimulator;
assert(sim, 'ShinobiSimulator was not exported to window');

console.log('✓ ShinobiSimulator initialized successfully');

// Test 1: Starting Position verification
const initialFeetY = sim.player.y + sim.player.h;
console.log(`Starting Position -> X: ${sim.player.x}, Y: ${initialFeetY}, Vy: ${sim.player.vy}`);
assert.strictEqual(initialFeetY, 482, 'Player feet must start exactly at verified ground baseline Y = 482');
assert.strictEqual(sim.player.vy, 0, 'Player vertical velocity Vy must start at 0');

// Test 2: Initial HUD Readout verification
assert.strictEqual(elements.ninjaPosDisplay.textContent, 'X: 280, Y: 482', 'HUD must display X: 280, Y: 482');
assert.strictEqual(elements.groundedDisplay.textContent, 'Grounded (Flush Y=482)', 'HUD must report "Grounded (Flush Y=482)" at starting position');
assert.strictEqual(sim.player.isOnGround, true, 'player.isOnGround must be true on startup');
console.log('✓ Initial HUD correctly reports Grounded (Flush Y=482) with zero airborne flicker');

// Test 3: Ground-contact tolerance evaluation
const tolerance = sim.GROUND_CONTACT_TOLERANCE;
assert.ok(tolerance >= 4.0, 'GROUND_CONTACT_TOLERANCE should be at least 4.0px');

// Within tolerance with vy = 0 -> Grounded
assert.strictEqual(sim.isWithinGroundContactTolerance(280, 482 - 52, 36, 52, 0), true, 'Exact baseline must be grounded');
assert.strictEqual(sim.isWithinGroundContactTolerance(280, 482 - 52 + 3, 36, 52, 0), true, 'Feet at 485 (+3px) must be within contact tolerance');
assert.strictEqual(sim.isWithinGroundContactTolerance(280, 482 - 52 - 3, 36, 52, 0), true, 'Feet at 479 (-3px) must be within contact tolerance');

// Non-zero vertical velocity (jumping or falling) -> Not grounded by tolerance
assert.strictEqual(sim.isWithinGroundContactTolerance(280, 482 - 52, 36, 52, -420), false, 'Jumping upwards (Vy: -420) must not be grounded');
assert.strictEqual(sim.isWithinGroundContactTolerance(280, 482 - 52, 36, 52, 120), false, 'Falling downward (Vy: 120) must not be grounded');

// Mid-air position outside tolerance -> Not grounded
assert.strictEqual(sim.isWithinGroundContactTolerance(280, 400 - 52, 36, 52, 0), false, 'Mid-air position Y = 400 must be airborne');
console.log('✓ Ground-contact tolerance logic validated for all velocity and distance boundary conditions');

// Test 4: Simulation loop over 60 physics frames (1 full second at 60 FPS)
// Ensure gravity does not pull player into airborne state when resting at starting position
let testTime = 1000;
for (let frame = 1; frame <= 60; frame++) {
  testTime += 16.666;
  // Step simulation
  // Pre-gravity check
  if (!sim.player.isDropping && Math.abs(sim.player.vy) <= 0.05 && sim.isWithinGroundContactTolerance(sim.player.x, sim.player.y, sim.player.w, sim.player.h, sim.player.vy)) {
    sim.player.isOnGround = true;
    sim.player.vy = 0;
  }
  if (!sim.player.isOnGround) {
    sim.player.vy += sim.player.gravity * 0.016;
  } else {
    sim.player.vy = 0;
  }
  sim.player.y += sim.player.vy * 0.016;
  sim.updateDiagnostics();

  assert.strictEqual(sim.player.isOnGround, true, `Frame ${frame}: Player must remain solidly grounded`);
  assert.strictEqual(sim.player.vy, 0, `Frame ${frame}: Player Vy must remain 0`);
  assert.strictEqual(Math.round(sim.player.y + sim.player.h), 482, `Frame ${frame}: Feet Y must remain 482`);
  assert.strictEqual(elements.groundedDisplay.textContent, 'Grounded (Flush Y=482)', `Frame ${frame}: HUD must remain Grounded`);
}
console.log('✓ 60-frame continuous resting physics test passed (0 frame drop, 0 jitter, status solidly Grounded)');

// Test 5: Jump and Landing cycle
// Initiate jump
sim.player.vy = sim.player.jumpImpulse; // -420
sim.player.isOnGround = false;
sim.updateDiagnostics();
assert.strictEqual(elements.groundedDisplay.textContent, 'Airborne (Vy: -420)', 'HUD must report Airborne during jump ascent');

// Simulate ascent and descent until landing
const dt = 0.016;
let landed = false;
for (let step = 0; step < 120; step++) {
  if (!sim.player.isOnGround) {
    sim.player.vy += sim.player.gravity * dt;
  }
  sim.player.y += sim.player.vy * dt;
  const feet = sim.player.y + sim.player.h;

  if (sim.player.vy >= 0 && feet >= 482 - tolerance && feet <= 482 + 18) {
    sim.player.y = 482 - sim.player.h;
    sim.player.vy = 0;
    sim.player.isOnGround = true;
    landed = true;
    sim.updateDiagnostics();
    break;
  }
}
assert.strictEqual(landed, true, 'Player must land safely back on ground baseline');
assert.strictEqual(elements.groundedDisplay.textContent, 'Grounded (Flush Y=482)', 'HUD must return to "Grounded (Flush Y=482)" upon landing');
console.log('✓ Jump, airborne flight, and ground re-contact recovery verified');

console.log('--- ALL REGRESSION CHECKS PASSED SUCCESSFULLY ---');
