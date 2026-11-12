"""Tighten the pauses in a voice-over copy (the original is never touched).

Finds phrases with ffmpeg silencedetect, shortens every pause to GAP (default 0.17s);
pauses that were long in the original (>= LONG_IF, default 0.6s) become LONG (0.30s) so chapter breaks still breathe.
Writes the tightened WAV and tools/tight-map.json (phrase list with old and new times).

Usage (run from the video folder):
  python3 tools/tighten.py assets/audio/voiceover.mp3 assets/audio/derived/vo-tight.wav
Options: --gap 0.17 --long 0.30 --long-if 0.6 --noise -38 --min-silence 0.15
After it runs, check the phrase count it prints against script.txt (one line per phrase).
"""
import argparse, json, os, re, subprocess, wave
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--gap", type=float, default=0.17); ap.add_argument("--long", type=float, default=0.30)
ap.add_argument("--long-if", type=float, default=0.6); ap.add_argument("--noise", type=float, default=-38)
ap.add_argument("--min-silence", type=float, default=0.15)
a = ap.parse_args()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32).copy(); dur = len(x) / SR

log = subprocess.run(["ffmpeg", "-hide_banner", "-i", a.src, "-af", f"silencedetect=n={a.noise}dB:d={a.min_silence}", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
starts = [float(v) for v in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", log)]
sil = list(zip(starts, ends + [dur] * (len(starts) - len(ends))))
ph = []; s = 0.0
for (p, q) in sil:
    if p - s > 0.05: ph.append((round(s, 3), round(p, 3)))
    s = q
if dur - s > 0.05: ph.append((round(s, 3), round(dur, 3)))
if not ph: raise SystemExit("no speech found; try --noise -45")

keep = []; s = max(0.0, ph[0][0] - 0.08)
for k in range(len(ph) - 1):
    e, b = ph[k][1], ph[k + 1][0]; g = b - e
    tgt = a.long if g >= a.long_if else a.gap
    if g > tgt + 0.01:
        rm = g - tgt; mid = (e + b) / 2
        keep.append((s, mid - rm / 2)); s = mid + rm / 2
keep.append((s, min(dur, ph[-1][1] + 0.24)))

fade = int(0.006 * SR); out = []
for (p, q) in keep:
    seg = x[int(p * SR):int(q * SR)].copy()
    if len(seg) > 2 * fade:
        seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    out.append(seg)
y = np.concatenate(out)

def remap(t):
    o = 0.0
    for (p, q) in keep:
        if t <= q: return o + max(0, t - p)
        o += q - p
    return o

mp = [{"n": i + 1, "src_start": p, "src_end": q, "start": round(remap(p), 3), "end": round(remap(q), 3)} for i, (p, q) in enumerate(ph)]
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
json.dump({"source": a.src, "audio": a.out, "keep": keep, "phrases": mp, "duration": round(len(y) / SR, 3)},
          open(os.path.join(ROOT, "tools", "tight-map.json"), "w"), indent=1)
pcm = (np.clip(y, -1, 1) * 32767).astype("<i2")
w = wave.open(a.out, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print(f"{len(ph)} phrases; {dur:.2f}s -> {len(y) / SR:.2f}s ({100 * (1 - len(y) / SR / dur):.1f}% shorter)")
for p in mp: print(f"  {p['n']:>3}  {p['start']:7.2f} - {p['end']:7.2f}")
