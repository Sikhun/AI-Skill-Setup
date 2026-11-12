"""Build index.html from the parts in src/ + cuts.json + transcript.json.

src/head.html   <head> + all CSS (style system)        src/body.html  <body> + scenes (<section id="s01">...) using @S01 @D01 @K01 ... and @DUR; no </body>
src/props.js    optional: SVG ink props (data-svg) as plain JS     src/helpers.js animation + transition helpers (do not edit per video)
src/scenes.js   the per-scene timeline (uses W/T/P word timings and the cut list C); build.py adds the <script> wrapper and the ending
cuts.json       {"cuts": [0, 2.4, 4.8, ..., DURATION]}  scene n runs cuts[n-1]..cuts[n] (tight-VO seconds)

Each scene clip gets a +-0.45s window around its cut so transitions can overlap; neighbouring scenes alternate tracks 1/2.
Usage: python3 tools/build.py   (NOBED=1 -> index.html uses soundtrack-nomusic.wav, for the no-music render)
"""
import json, os, re

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = lambda f: open(os.path.join(R, "src", f), encoding="utf-8").read() if os.path.exists(os.path.join(R, "src", f)) else ""
NORM = r"[\s\"'.,!?…ๆ+]"
norm = lambda s: re.sub(NORM, "", s)

C = json.load(open(os.path.join(R, "cuts.json")))["cuts"]
tr = json.load(open(os.path.join(R, "transcript.json"), encoding="utf-8"))
DUR = round(C[-1], 2)

W = '''        const PH = /*PH*/[]/*/PH*/;
        const norm = (s) => s.replace(/[\\s"'.,!?…ๆ+]/g, "");
        const cursor = {};
        // W(n, word): spoken time of `word` inside phrase n (1-based). Repeated calls walk forward through the phrase.
        function W(n, word) {
          const p = PH[n - 1]; if (!p) return null; const target = norm(word); const from = cursor[n] || 0;
          let pos = p[2].indexOf(target, from); if (pos < 0) pos = p[2].indexOf(target); if (pos < 0) return null;
          cursor[n] = pos + target.length;
          if (p[3]) { for (const [t, len] of p[4]) if (len > pos) return t; }
          return p[0] + (p[1] - p[0]) * (pos / p[2].length);
        }

'''
END = """
        window.__sfxCues = cues;
        window.__timelines = window.__timelines || {};
        window.__timelines["main"] = tl;
        tl.seek(0);
      })();
    </script>
  </body>
</html>
"""
script = "    <script>\n      (function () {\n" + src("props.js") + "\n" + W + src("helpers.js") + "\n" + src("scenes.js") + END
s = src("head.html") + src("body.html") + script

nsc = len(C) - 1
for n in range(1, nsc + 1):
    a = max(0, C[n - 1] - 0.45); b = min(DUR, C[n] + 0.45)
    s = s.replace(f"@S{n:02d}", f"{a:.2f}").replace(f"@D{n:02d}", f"{b - a:.2f}").replace(f"@K{n:02d}", str(1 + (n + 1) % 2))
s = s.replace("@DUR", str(DUR)).replace("@CUTS", ", ".join(f"{c:.2f}" for c in C)).replace("@NSCENES", str(nsc))
left = re.findall(r"@[A-Z]+\d*", s)
if left: raise SystemExit(f"unfilled placeholders {sorted(set(left))[:8]}: body.html has more scenes than cuts.json, or a typo")

ph = []
for p in tr["phrases"]:
    tx = norm(p["text"]); ok = bool(p["tokens"]) and norm(p["asr"]) == tx
    ph.append([p["start"], p["end"], tx, ok, [[t, len(norm(x))] for t, x in p["tokens"]] if ok else []])
s = re.sub(r"/\*PH\*/.*?/\*/PH\*/", lambda m: "/*PH*/" + json.dumps(ph, ensure_ascii=False, separators=(",", ":")) + "/*/PH*/", s, flags=re.S)
if os.environ.get("NOBED"): s = s.replace("assets/audio/derived/soundtrack.wav", "assets/audio/derived/soundtrack-nomusic.wav")
open(os.path.join(R, "index.html"), "w", encoding="utf-8").write(s)
print(f"index.html: {nsc} scenes, {DUR}s, {len(ph)} phrases ({sum(p[3] for p in ph)} with exact word times)")
