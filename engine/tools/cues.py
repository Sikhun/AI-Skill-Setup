"""Dump the SFX cue list that index.html records while building its timeline (cue(t, name, gain)) -> tools/cues.json
Re-run after every change to index.html timing, then run mix.py.
Uses the headless Chrome that HyperFrames downloads (~/.cache/hyperframes/chrome; fetched with `npx hyperframes browser ensure` if missing), or $CHROME.
Usage: python3 tools/cues.py
"""
import glob, html, json, os, re, subprocess, sys, pathlib

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ch = os.environ.get("CHROME")
if not ch:
    pats = ["~/.cache/hyperframes/chrome/**/chrome-headless-shell", "~/.cache/hyperframes/chrome/**/chrome-headless-shell.exe",
            "~/.cache/ms-playwright/**/chrome-headless-shell", "/opt/pw-browsers/**/chrome-headless-shell"]
    hits = [h for p in pats for h in glob.glob(os.path.expanduser(p), recursive=True) if os.path.isfile(h)]
    ch = hits[0] if hits else None
if not ch:  # let HyperFrames find or download its Chrome
    npx = "npx.cmd" if os.name == "nt" else "npx"
    subprocess.run([npx, "--yes", "hyperframes", "browser", "ensure"], capture_output=True)
    r = subprocess.run([npx, "--yes", "hyperframes", "browser", "path"], capture_output=True, text=True)
    lines = [l.strip() for l in r.stdout.splitlines() if l.strip()]
    ch = lines[-1] if lines and os.path.isfile(lines[-1]) else None
if not ch: sys.exit("headless Chrome not found: run `npx hyperframes browser ensure`, or set CHROME=/path/to/chrome")

s = open(os.path.join(R, "index.html"), encoding="utf-8").read()
s = s.replace("</body>", '<pre id="cuesout"></pre><script>document.getElementById("cuesout").textContent=JSON.stringify(window.__sfxCues||null)</script></body>')
tmp = os.path.join(R, "_cues_tmp.html"); open(tmp, "w", encoding="utf-8").write(s)
try:
    dom = subprocess.run([ch, "--headless", "--disable-gpu", "--no-sandbox", "--virtual-time-budget=6000", "--dump-dom",
                          pathlib.Path(tmp).as_uri()], capture_output=True, text=True, encoding="utf-8", timeout=120).stdout
finally:
    os.remove(tmp)
m = re.search(r'<pre id="cuesout">(.*?)</pre>', dom, re.S)
c = json.loads(html.unescape(m.group(1))) if m and m.group(1).strip() else None
if not c: sys.exit("no cues found: open index.html in a browser and check the console for a script error (often a W() word not found or a missing #id)")
json.dump(sorted(c), open(os.path.join(R, "tools", "cues.json"), "w"))
names = {}
for _, n, _ in c: names[n] = names.get(n, 0) + 1
print(len(c), "cues ->", "tools/cues.json", dict(sorted(names.items())))
