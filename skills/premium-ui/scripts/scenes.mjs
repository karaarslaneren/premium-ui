#!/usr/bin/env node
// premium-ui scene screenshots: scrolls a page in real time (headless Chrome over CDP) and
// captures one viewport per stop, so pinned / scrubbed scenes are seen the way a visitor sees
// them. Use it when there is no browser tool, or when the browser pane is hidden.
// snapshot.py's full-page shot can't show these pages: a tall window turns every 100vh scene huge.
//
// Usage (Node 22+, Chrome / Chromium / Edge installed; CHROME=/path overrides):
//   node scenes.mjs <url> [--out DIR] [--width 1440] [--height 900] [--stops auto|0,900,2400]
// A local file needs a server (python3 -m http.server) so module scripts and fonts load.
// Writes DIR/NN-<y>.png (default DIR: ./scenes) and prints {height, shots}.
import { spawn, execSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(`--${k}`); return i > -1 ? args[i + 1] : d; };
const url = args.find((a) => /^(https?|file):/.test(a));
if (!url) { console.error('usage: node scenes.mjs <url> [--out DIR] [--width 1440] [--height 900] [--stops auto|y1,y2]'); process.exit(2); }
const out = opt('out', 'scenes'), w = +opt('width', 1440), h = +opt('height', 900), stops = opt('stops', 'auto');

const which = (c) => { try { return execSync(`command -v ${c}`, { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(); } catch { return ''; } };
const chrome = [process.env.CHROME,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  ...['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'microsoft-edge'].map(which),
].find((p) => p && existsSync(p));
if (!chrome) { console.error('No Chrome/Chromium/Edge found; set CHROME=/path/to/browser'); process.exit(2); }

mkdirSync(out, { recursive: true });
const port = 9300 + Math.floor(Math.random() * 600);
const proc = spawn(chrome, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${mkdtempSync(join(tmpdir(), 'pui-'))}`, '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let ws, id = 0; const pending = new Map();
const send = (method, params = {}) => new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
const run = async (expression) => (await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true })).result?.value;

try {
  let target;
  for (let t = 0; t < 50 && !target; t++) { await sleep(200); try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((x) => x.type === 'page'); } catch {} }
  if (!target) throw new Error('Chrome did not open a debugging port');
  ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d.result); pending.delete(d.id); } };
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: w < 600 });
  await send('Page.enable');
  await send('Page.navigate', { url });
  await sleep(3500); // fonts, intro, first reveals
  const H = await run('document.documentElement.scrollHeight');
  const ys = stops === 'auto' ? Array.from({ length: Math.ceil(H / h) }, (_, i) => Math.min(i * h, H - h)) : stops.split(',').map(Number);
  let n = 0;
  for (const y of [...new Set(ys)]) {
    // scroll in steps so scroll-linked code (ScrollTrigger, Lenis, observers) sees the path, then let it settle
    await run(`(async()=>{const a=scrollY,b=${y};for(let i=1;i<=12;i++){scrollTo(0,a+(b-a)*i/12);await new Promise(r=>setTimeout(r,40));}})()`);
    await sleep(1400);
    const { data } = await send('Page.captureScreenshot', { format: 'png' });
    writeFileSync(join(out, `${String(++n).padStart(2, '0')}-${y}.png`), Buffer.from(data, 'base64'));
  }
  console.log(JSON.stringify({ height: H, shots: n, out }));
} finally { try { ws?.close(); } catch {} proc.kill(); }
