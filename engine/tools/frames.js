// Screenshot index.html at given times (fast preview without a full render). Usage: node tools/frames.js out.jpg t1 t2 ...  (tiles 4 per row, 270x480 each)
const path = require("path"), os = require("os"), { execFileSync } = require("child_process");
// Playwright: local or global install (npm i -g playwright). Browser: $CHROME, else Playwright's own Chromium.
let pw;
try {
  pw = require("playwright");
} catch (e) {
  try {
    pw = require(path.join(process.env.APPDATA || "", "npm", "node_modules", "playwright"));
  } catch (e2) {
    const g = execFileSync(process.platform === "win32" ? "npm.cmd" : "npm", ["root", "-g"], { shell: true }).toString().trim();
    pw = require(path.join(g, "playwright"));
  }
}
const { chromium } = pw;
(async () => {
  const out = process.argv[2], ts = process.argv.slice(3).map(Number);
  const b = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const errs = []; p.on("pageerror", (e) => errs.push(e.message));
  await p.goto("file://" + path.resolve(__dirname, "../index.html")); await p.waitForTimeout(800);
  if (errs.length) console.log("ERRORS:", errs);
  const files = [];
  for (const [i, t] of ts.entries()) {
    await p.evaluate((t) => { const tl = window.__timelines.main; tl.seek(t, false);
      document.querySelectorAll(".clip[data-start]").forEach((el) => { const s = +el.dataset.start, d = +el.dataset.duration; el.style.visibility = t >= s && t < s + d ? "visible" : "hidden"; }); }, t);
    await p.waitForTimeout(60);
    const f = path.join(os.tmpdir(), `fr_${i}.png`); await p.screenshot({ path: f }); files.push(f);
  }
  await b.close();
  const cols = 4, rows = Math.ceil(files.length / cols);
  execFileSync(process.platform === "win32" ? "python" : "python3", ["-c", `
import sys
from PIL import Image, ImageDraw
fs=sys.argv[3:]; c=int(sys.argv[1]); out=sys.argv[2]; r=(len(fs)+c-1)//c
im=Image.new("RGB",(360*c,640*r),"white")
for i,f in enumerate(fs): im.paste(Image.open(f).convert("RGB").resize((360,640)),((i%c)*360,(i//c)*640))
im.save(out,quality=85)`, String(cols), out, ...files]);
  console.log("->", out);
})();
