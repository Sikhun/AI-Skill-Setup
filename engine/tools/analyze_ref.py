"""Measure a reference video so an AI can analyse it (it cannot watch video directly).

Writes into OUTDIR:
  data.md               numbers: size, fps, duration, loudness, shot list with lengths, cut stats, audio hits per second,
                        how many hits land on a cut, pauses in the mix
  sheet-NN.jpg          a frame every 0.5 s (8 columns, time stamped)  -> pacing, typography, layout, safe zones
  shots.jpg             the middle frame of every shot                  -> composition, B-roll / prop placement
  cuts-NN.jpg           each cut at -0.20 / -0.10 / 0 / +0.10 / +0.20 s  -> transitions
  motion.jpg            first / middle / last frame of the 12 longest shots -> zooms, camera movement
Then look at every image and write the analysis (see engine/README.md, "Reference video").

Usage: python3 tools/analyze_ref.py example-output/ep01-socrates.mp4 analysis/ref-ep01
"""
import json, math, os, re, shutil, subprocess, sys, tempfile
import numpy as np

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
run = lambda a, **k: subprocess.run(a, capture_output=True, text=True, **k)
pr = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate", "-of", "json", src]).stdout)
dur = float(pr["format"]["duration"]); v = next(s for s in pr["streams"] if s["codec_type"] == "video")
fps = eval(v["r_frame_rate"]); W, H = v["width"], v["height"]

# ---- shots (scene change detection) ----
# frame-change score: share of pixels that changed a lot over 0.2 s (soft blur/dip/iris transitions defeat ffmpeg's scene filter)
FW, FH, FF = 54, 96, 15
fr = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", f"fps={FF},scale={FW}:{FH},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(fr, np.uint8).reshape(-1, FH, FW).astype(np.float32)
chg = np.zeros(len(fr)); chg[3:] = (np.abs(fr[3:] - fr[:-3]) > 25).mean((1, 2))
pk = [k / FF for k in range(2, len(chg) - 2) if chg[k] >= 0.2 and chg[k] == chg[max(0, k - 6):k + 7].max()]
cuts = [0.0]
for x in pk:
    if x - cuts[-1] > 0.6: cuts.append(round(x - 0.1, 2))  # peak sits ~0.1 s after the change
cuts.append(dur)
shots = [(cuts[i], cuts[i + 1]) for i in range(len(cuts) - 1)]
L = np.array([b - a for a, b in shots])

# ---- audio ----
ln = run(["ffmpeg", "-hide_banner", "-i", src, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
I = re.findall(r"I:\s+(-?[\d.]+) LUFS", ln)[-1]; TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", ln)[-1]
SR = 16000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-af", "highpass=f=1500", "-f", "f32le", "-"], capture_output=True).stdout
a = np.frombuffer(raw, dtype=np.float32)
hop = int(0.01 * SR); e = np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, mode="same"))[::hop]
base = np.convolve(e, np.ones(50) / 50, mode="same")
hits = [i * 0.01 for i in range(1, len(e) - 1) if e[i] > 2.2 * base[i] and e[i] > 0.02 and e[i] >= e[i - 1] and e[i] >= e[i + 1]]
hits = [h for k, h in enumerate(hits) if k == 0 or h - hits[k - 1] > 0.08]
on_cut = sum(1 for h in hits if min(abs(h - c) for c in cuts) < 0.15)
sil = run(["ffmpeg", "-hide_banner", "-i", src, "-af", "silencedetect=n=-45dB:d=0.25", "-f", "null", "-"]).stderr
pauses = re.findall(r"silence_duration: ([\d.]+)", sil)

# ---- images ----
T = tempfile.mkdtemp()
def grab(t, name, w=180, h=320, label=None):
    vf = f"scale={w}:{h}"
    if label: vf += f",drawtext=text='{label}':x=4:y=4:fontsize={max(12, w // 12)}:fontcolor=white:box=1:boxcolor=black@0.6"
    r = run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, min(dur - 0.05, t)):.3f}", "-i", src, "-frames:v", "1", "-vf", vf, os.path.join(T, name)])
    if r.returncode and label:  # drawtext needs a font; retry without the label
        grab(t, name, w, h, None)
def tile(pattern_files, cols, outname, w, h):
    files = sorted(pattern_files)
    for k, f in enumerate(files): os.rename(os.path.join(T, f), os.path.join(T, f"t{k:04d}.png"))
    rows = math.ceil(len(files) / cols)
    run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", os.path.join(T, "t%04d.png"), "-vf", f"tile={cols}x{rows}:padding=3:color=0x333333",
         "-frames:v", "1", "-q:v", "3", os.path.join(out, outname)])
    for f in os.listdir(T): os.remove(os.path.join(T, f))
imgs = []
ts = list(np.arange(0, dur, 0.5)); per = 48
for s in range(0, len(ts), per):
    for k, t in enumerate(ts[s:s + per]): grab(t, f"a{k:03d}.png", label=f"{t:.1f}s")
    n = f"sheet-{s // per + 1:02d}.jpg"; tile([f for f in os.listdir(T)], 8, n, 180, 320); imgs.append(n)
for k, (p, q) in enumerate(shots): grab((p + q) / 2, f"s{k:03d}.png", label=f"#{k + 1} {p:.1f}s")
tile(os.listdir(T), 8, "shots.jpg", 180, 320); imgs.append("shots.jpg")
cs = cuts[1:-1]
for s in range(0, len(cs), 8):
    for j, c in enumerate(cs[s:s + 8]):
        for i, d in enumerate((-0.2, -0.1, 0, 0.1, 0.2)): grab(c + d, f"c{j:02d}{i}.png", 144, 256, f"{c + d:.2f}" if i == 2 else None)
    n = f"cuts-{s // 8 + 1:02d}.jpg"; tile(os.listdir(T), 5, n, 144, 256); imgs.append(n)
longest = sorted(range(len(shots)), key=lambda k: -L[k])[:12]
for j, k in enumerate(sorted(longest)):
    p, q = shots[k]
    for i, t in enumerate((p + 0.15, (p + q) / 2, q - 0.15)): grab(t, f"m{j:02d}{i}.png", label=f"#{k + 1} {t:.1f}s" if i == 0 else None)
tile(os.listdir(T), 6, "motion.jpg", 180, 320); imgs.append("motion.jpg")
shutil.rmtree(T)

md = [f"# Reference data: {os.path.basename(src)}", "",
      f"- {W}x{H}, {fps:.2f} fps, {dur:.2f}s; loudness {I} LUFS, true peak {TP} dBFS",
      f"- shots: {len(shots)} (auto-detected big frame changes: tested at ~90% of real cuts found, ~25% of detections are big in-scene changes such as a full-screen prop; confirm on the sheets); average {L.mean():.2f}s, median {np.median(L):.2f}s, "
      f"shortest {L.min():.2f}s, longest {L.max():.2f}s; first cut at {cuts[1] if len(cuts) > 2 else dur:.2f}s",
      f"- audio hits (transients above 1.5 kHz, mostly SFX and consonants): {len(hits)} = {len(hits) / dur:.1f}/s; {on_cut} land within 0.15s of a cut "
      f"({100 * on_cut / max(1, len(cuts) - 2):.0f}% of cuts have a hit)",
      f"- pauses below -45 dB longer than 0.25s: {len(pauses)} ({', '.join(pauses[:10])}{'...' if len(pauses) > 10 else ''})", "",
      "## Shot list", "| # | start | end | length |", "|---|---|---|---|"]
md += [f"| {k + 1} | {p:.2f} | {q:.2f} | {q - p:.2f} |" for k, (p, q) in enumerate(shots)]
md += ["", "## Audio hits per 5 s", " ".join(f"{int(t)}s:{sum(1 for h in hits if t <= h < t + 5)}" for t in range(0, int(dur), 5)), "",
       "## Images", *[f"- {i}" for i in imgs]]
open(os.path.join(out, "data.md"), "w").write("\n".join(md) + "\n")
print(f"{len(shots)} shots, avg {L.mean():.2f}s, {len(hits)} audio hits, {I} LUFS -> {out}/data.md + {len(imgs)} images")
