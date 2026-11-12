"""Premix the soundtrack: VO + synthesized noir-jazz bed + synthesized SFX, mastered to -13 LUFS / -1.5 dBTP.

VO  : the tightened VO from tools/tight-map.json ("audio"), +7 dB, gentle presence lift
Bed : the channel's background track (assets/audio/bg-music.mp3, looped with a crossfade if the video is longer), ducked -7 dB under the VO.
      MUSIC=/path/song.mp3 uses another file; MUSIC=synth uses the noir jazz synthesized here (D minor, 84 BPM swing).
SFX : all synthesized here (no third-party files), placed by tools/cues.json (python3 tools/cues.py)
Out : assets/audio/derived/soundtrack.wav (48 kHz stereo). NOBED=1 -> soundtrack-nomusic.wav (VO + SFX only)

Cue names: key paper slide stamp stampsoft thud pencil scratch stretch flick snap burn shh tick rise poof pour clink slap
           whoosh whoosh-low pop flash lampclick sparkle. Unknown names fall back to "pop".
Usage: python3 tools/cues.py && python3 tools/mix.py && NOBED=1 python3 tools/mix.py
       (Windows PowerShell: $env:NOBED=1; python tools/mix.py; Remove-Item Env:NOBED)
"""
import json, os, subprocess, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
DUR = json.load(open(os.path.join(ROOT, "cuts.json")))["cuts"][-1]
VO = json.load(open(os.path.join(ROOT, "tools", "tight-map.json")))["audio"]
N = int(DUR * SR)
rng = np.random.default_rng(9)


def dec(path, ch=1):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).copy()
    return a.reshape(-1, ch) if ch > 1 else a


def ff(x, af):
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af, "-f", "f32le", "-"],
                       input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    y = np.frombuffer(p, dtype=np.float32).copy()
    return np.pad(y, (0, max(0, len(x) - len(y))))[: len(x)]


def env(n, a=0.005, tau=0.3):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / tau)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def add(buf, x, t0, g=1.0):
    i = int(t0 * SR)
    if i >= len(buf) or i + len(x) <= 0: return
    if i < 0: x = x[-i:]; i = 0
    x = x[: len(buf) - i]; buf[i: i + len(x)] += g * x


def noise(d, tau, a=0.002):
    n = int(d * SR); return rng.standard_normal(n) * env(n, a, tau)

# ---------------- VO ----------------
vo = dec(os.path.join(ROOT, VO))
vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
vo = ff(vo, "highpass=f=70,equalizer=f=3000:t=q:w=1.2:g=2") * 10 ** (7 / 20)

# ---------------- music bed ----------------
# Default: the channel's own track at assets/audio/bg-music.mp3 (copied from the skill's assets/music/).
# $MUSIC=/path/song.mp3 picks another file; MUSIC=synth uses the synthesized noir jazz below instead.
def music_bed(path):
    m = dec(path, 2); L = len(m); xf = int(3 * SR)
    if L < N:  # loop with a 3 s crossfade
        out = m.copy()
        while len(out) < N:
            r = np.linspace(0, 1, xf)[:, None]
            out[-xf:] = out[-xf:] * (1 - r) + m[:xf] * r
            out = np.concatenate([out, m[xf:]])
        m = out
    return m[:N]

def synth_bed():
    BPM = 84; beat = 60 / BPM; bar = 4 * beat; sw = 0.62  # swing ratio for 8ths
    # Dm9 | Gm9 | Em7b5 | A7b9   (voicings as MIDI)
    chords = [[53, 57, 60, 64, 65], [55, 58, 62, 65, 69], [52, 55, 58, 62], [55, 58, 61, 64, 67]]
    roots = [38, 43, 40, 45]
    walks = [[38, 41, 45, 42], [43, 46, 50, 41], [40, 43, 46, 44], [45, 49, 52, 37]]


    def bass_note(f, d):
        n = int(d * SR); t = np.arange(n) / SR
        w = np.sin(2 * np.pi * f * t) + 0.55 * np.sin(4 * np.pi * f * t) * np.exp(-t / 0.18) + 0.25 * np.sin(6 * np.pi * f * t) * np.exp(-t / 0.09)
        w *= np.minimum(t / 0.006, 1) * np.exp(-t / 0.55)
        w[: int(0.03 * SR)] += noise(0.03, 0.008)[: int(0.03 * SR)] * 0.25  # finger thump
        return w


    def piano(f, d, amp):
        n = int(d * SR); t = np.arange(n) / SR
        w = sum(a * np.sin(2 * np.pi * f * k * (1 + 0.0004 * k * k) * t) * np.exp(-t / (1.6 / k)) for k, a in [(1, 1), (2, .45), (3, .18), (4, .08)])
        return amp * w * np.minimum(t / 0.004, 1)


    bass = np.zeros(N); keys = np.zeros(N); drums = np.zeros(N)
    nbars = int(DUR / bar) + 2
    comp = [[(0, 1.0)], [(1.5 + 0.0, 0.8), (3.0, 0.5)], [(0.62, 0.7), (2.5, 0.8)], [(0, 0.9), (2.62, 0.6)]]
    for b in range(nbars):
        t0 = 0.2 + b * bar; k = b % 4
        for q, m in enumerate(walks[k]):
            add(bass, bass_note(hz(m), beat * 1.1), t0 + q * beat, 0.5)
        for (bt, a) in comp[(b * 3) % 4]:
            for j, m in enumerate(chords[k]):
                add(keys, piano(hz(m), 2.2, 0.06 * a), t0 + bt * beat + j * 0.008)
        for q in range(4):  # brush swirl (continuous) + swung taps + backbeat slap
            sw_n = int(beat * SR); tt = np.arange(sw_n) / SR
            add(drums, rng.standard_normal(sw_n) * (0.35 + 0.65 * np.sin(np.pi * tt / beat) ** 2) * 0.018, t0 + q * beat)
            add(drums, noise(0.06, 0.02), t0 + q * beat, 0.05)
            add(drums, noise(0.05, 0.015), t0 + (q + sw) * beat, 0.035)
            if q in (1, 3): add(drums, noise(0.18, 0.06), t0 + q * beat, 0.11)
        if b % 2 == 0: add(drums, np.sin(2 * np.pi * 55 * np.arange(int(.3 * SR)) / SR) * env(int(.3 * SR), .003, .12), t0, 0.25)  # soft kick
    bass = ff(bass, "lowpass=f=900")
    drums = ff(drums, "highpass=f=1200,lowpass=f=9000")
    keys = ff(keys, "lowpass=f=3200,aecho=0.6:0.5:60|110:0.25|0.15")
    bed = bass + drums + keys
    return ff(bed, "acompressor=threshold=-20dB:ratio=2.5:attack=15:release=250")

MUSIC = os.environ.get("MUSIC") or os.path.join(ROOT, "assets/audio/bg-music.mp3")
if MUSIC != "synth" and not os.path.exists(MUSIC):
    raise SystemExit(f"music not found: {MUSIC}\nCopy the skill's assets/music/bg-music.mp3 to assets/audio/bg-music.mp3 (or set MUSIC=/path/to/song.mp3, or MUSIC=synth).")
t = np.arange(N) / SR
if MUSIC != "synth":
    bed = music_bed(MUSIC)
    bed *= 0.2 / (np.sqrt(np.mean(bed ** 2)) + 1e-9)  # same average level as the synth bed
    print("music:", MUSIC)
else:
    bed = synth_bed(); bed /= np.max(np.abs(bed)) + 1e-9
    bed = np.stack([bed, bed], 1); print("music: synthesized noir jazz")
bed *= (np.minimum(t / 0.6, 1) * np.clip((DUR - t) / 1.8, 0, 1))[:, None]
win = int(0.05 * SR)
e = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, mode="same"))
active = (e > 0.02).astype(float)
k = int(0.3 * SR); active = np.convolve(active, np.ones(k) / k, mode="same")
bed *= (10 ** (-7 * np.clip(active, 0, 1) / 20))[:, None]

# ---------------- SFX ----------------
def typewriter():
    n = int(0.09 * SR); tt = np.arange(n) / SR
    click = ff(noise(0.09, 0.004, 0.0003), "bandpass=f=3200:w=2500") * 1.4
    body = np.sin(2 * np.pi * (170 + rng.uniform(-15, 15)) * tt) * env(n, 0.001, 0.018) * 0.7
    ping = np.sin(2 * np.pi * 2350 * tt) * env(n, 0.001, 0.02) * 0.12
    return click + body + ping

def paper(d=0.28):
    x = ff(noise(d, 1.0, 0.0), "bandpass=f=3500:w=4000"); n = len(x); tt = np.arange(n) / SR
    return x * np.sin(np.pi * tt / d) ** 1.5

def thump(f0=70, g_noise=0.35):
    n = int(0.25 * SR); tt = np.arange(n) / SR
    body = np.sin(2 * np.pi * (f0 + 90 * np.exp(-tt * 40)) * tt) * env(n, 0.001, 0.07)
    return 0.9 * body + g_noise * ff(noise(0.25, 0.025), "bandpass=f=1800:w=1500")

def scratch(d=0.32, f=4200):
    x = ff(noise(d, 1.0, 0.0), f"bandpass=f={f}:w=2500"); n = len(x); tt = np.arange(n) / SR
    am = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 22 * tt + 3 * np.sin(2 * np.pi * 3 * tt)))
    return x * am * np.minimum(tt / 0.01, 1) * np.clip((d - tt) / 0.05, 0, 1)

def snap():
    n = int(0.12 * SR); tt = np.arange(n) / SR
    x = ff(noise(0.12, 0.006, 0.0002), "bandpass=f=2600:w=1800") * 2.2
    return x + np.sin(2 * np.pi * 900 * tt) * env(n, 0.0005, 0.01) * 0.3

def burn():
    x = ff(noise(0.5, 0.3, 0.05), "lowpass=f=2500") * 0.5
    cr = np.zeros(len(x)); idx = rng.choice(len(x), 70, replace=False); cr[idx] = rng.uniform(-1, 1, 70)
    return x + ff(cr, "highpass=f=1500") * 2

def sweep(f0, f1, d, amp=0.3):
    n = int(d * SR); tt = np.arange(n) / SR; f = f0 * (f1 / f0) ** (tt / d)
    return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / d)

def pour():
    out = np.zeros(int(0.7 * SR))
    for i in range(14):
        f = rng.uniform(300, 900); b = sweep(f, f * 1.8, 0.05, 0.3); add(out, b, i * 0.045)
    return ff(out, "lowpass=f=2500")

def clink():
    n = int(0.4 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2480 * tt) + 0.6 * np.sin(2 * np.pi * 3710 * tt) + 0.3 * np.sin(2 * np.pi * 5200 * tt)) * env(n, 0.001, 0.08) * 0.35

def tick():
    n = int(0.05 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * 1250 * tt) * env(n, 0.0005, 0.012)

synth = {"key": typewriter, "paper": paper, "slide": lambda: paper(0.4), "stamp": lambda: thump(65, 0.45), "stampsoft": lambda: thump(80, 0.25) * 0.6,
         "thud": lambda: thump(95, 0.1) * 0.7, "pencil": scratch, "scratch": lambda: scratch(0.08, 3800), "stretch": lambda: scratch(0.6, 1800) * 0.6,
         "flick": lambda: ff(noise(0.05, 0.012), "highpass=f=2000") * 0.8, "snap": snap, "burn": burn, "shh": lambda: ff(noise(0.5, 0.25, 0.08), "bandpass=f=6000:w=4000") * 0.6,
         "tick": tick, "rise": lambda: sweep(180, 720, 0.8, 0.25), "poof": lambda: ff(noise(0.45, 0.12, 0.01), "lowpass=f=1400"), "pour": pour, "clink": clink,
         "slap": lambda: thump(120, 0.8) * 0.8}
def whoosh(d=0.45, f0=600, f1=3800, amp=0.9):
    x = noise(d, 1.0, 0.0); n = len(x); tt = np.arange(n) / SR; out = np.zeros(n)
    for k in range(0, n, 2400):  # band sweep in blocks
        fc = f0 * (f1 / f0) ** (min(k, n - 1) / n)
        out[k:k + 2400] = ff(x[k:k + 2400], f"bandpass=f={fc:.0f}:w={fc * 0.8:.0f}")
    return amp * out * np.sin(np.pi * tt / d) ** 2

def pop():
    n = int(0.12 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * (380 + 900 * np.exp(-tt * 60)) * tt) * env(n, 0.001, 0.03)

def lampclick():
    n = int(0.08 * SR); tt = np.arange(n) / SR
    return ff(noise(0.08, 0.004, 0.0002), "bandpass=f=4200:w=3000") * 1.6 + np.sin(2 * np.pi * 1800 * tt) * env(n, 0.0005, 0.006) * 0.4

def sparkle():
    out = np.zeros(int(0.9 * SR))
    for i in range(9):
        f = hz(84 + [0, 4, 7, 12, 16, 19, 24, 19, 28][i]); n = int(0.35 * SR); tt = np.arange(n) / SR
        add(out, np.sin(2 * np.pi * f * tt) * env(n, 0.002, 0.08) * 0.35, i * 0.06)
    return out

def camflash():
    return pop() * 0.8 + sweep(5200, 7600, 0.12, 0.15)

synth.update({"whoosh": whoosh, "whoosh-low": lambda: ff(whoosh(0.6, 250, 1400, 1.2), "lowpass=f=1800"), "pop": pop, "flash": camflash,
              "lampclick": lampclick, "sparkle": sparkle, "frost": sparkle, "sprout": sparkle})
base_gain = {"key": 0.32, "paper": 0.22, "slide": 0.22, "stamp": 0.6, "stampsoft": 0.5, "thud": 0.4, "pencil": 0.18, "scratch": 0.14, "stretch": 0.16,
             "flick": 0.2, "snap": 0.75, "burn": 0.3, "shh": 0.12, "tick": 0.2, "rise": 0.35, "poof": 0.35, "pour": 0.4, "clink": 0.35, "slap": 0.5,
             "whoosh": 0.22, "whoosh-low": 0.28, "pop": 0.28, "lampclick": 0.45, "frost": 0.22, "sprout": 0.2, "flash": 0.3, "sparkle": 0.22}

# ---- Synth & Retro SFX Kit ----
def buzz():  # bulb/neon flicker hum
    d=0.35; n=int(d*SR); tt=np.arange(n)/SR
    hum=(np.sign(np.sin(2*np.pi*120*tt))*0.5+np.sin(2*np.pi*240*tt)*0.3)
    am=(rng.uniform(0,1,int(d*40)+1)>0.35).repeat(int(SR/40)+1)[:n]
    return ff(hum*am*np.minimum(tt/0.005,1)*np.clip((d-tt)/0.05,0,1),"lowpass=f=3000")*0.6
def static_():
    d=0.45; x=ff(noise(d,1.0,0.0),"highpass=f=900,lowpass=f=7000"); n=len(x); tt=np.arange(n)/SR
    am=0.6+0.4*np.sign(np.sin(2*np.pi*31*tt)); return x*am*np.sin(np.pi*tt/d)**0.5*0.8
def synthstab():  # detuned saw chord, 80s
    d=0.9; n=int(d*SR); tt=np.arange(n)/SR; y=np.zeros(n)
    for m in (50,57,62,65):
        for dt in (-0.12,0.12):
            f=hz(m+dt); y+=2*((tt*f)%1)-1
    y=ff(y/8,"lowpass=f=1800,aecho=0.6:0.4:180:0.35")
    return y*env(n,0.01,0.35)
def thunder():
    x=ff(noise(1.6,0.6,0.004),"lowpass=f=420")*2.2; n=len(x)
    cr=ff(noise(0.25,0.06,0.001),"bandpass=f=2500:w=2000")*0.8; x[:len(cr)]+=cr; return x
def beep():
    n=int(0.12*SR); tt=np.arange(n)/SR; return np.sign(np.sin(2*np.pi*2048*tt))*np.minimum(tt/0.002,1)*np.clip((0.12-tt)/0.01,0,1)*0.25
def click():
    n=int(0.06*SR); tt=np.arange(n)/SR; return ff(noise(0.06,0.004,0.0002),"bandpass=f=2500:w=2000")*1.5+np.sin(2*np.pi*700*tt)*env(n,0.0005,0.01)*0.4
def lock():
    out=np.zeros(int(0.5*SR)); add(out,click()*1.2,0); add(out,clink()*0.6,0.05); return out
def step():
    return thump(110,0.15)*0.5
def crt():
    d=0.5; n=int(d*SR); tt=np.arange(n)/SR; f=15600*(1-tt/d)+400
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*0.15+ff(noise(d,0.08,0.001),"lowpass=f=2000")*0.8)*np.clip((d-tt)/0.1,0,1)
def blip():
    n=int(0.07*SR); tt=np.arange(n)/SR; f=hz(84+int(rng.integers(0,5))*2)
    return (np.sin(2*np.pi*f*tt)+0.3*np.sign(np.sin(2*np.pi*f*tt)))*env(n,0.002,0.025)*0.5
synth.update({"blip":blip,"buzz":buzz,"static":static_,"synth":synthstab,"thunder":thunder,"beep":beep,"click":click,"lock":lock,"step":step,"crt":crt})
base_gain.update({"blip":0.14,"buzz":0.25,"static":0.2,"synth":0.35,"thunder":0.5,"beep":0.3,"click":0.4,"lock":0.45,"step":0.35,"crt":0.3})
# ---- Extended Transitions & UI SFX Kit ----
def rewind():  # tape rewind squeal: rising warble over hiss
    d=0.6; n=int(d*SR); tt=np.arange(n)/SR; f=600+2600*(tt/d)**1.5+120*np.sin(2*np.pi*23*tt)
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*0.18+ff(noise(d,1.0,0.0),"bandpass=f=3000:w=2500")*0.25)*np.sin(np.pi*tt/d)**0.6
def flipcard():
    out=np.zeros(int(0.15*SR)); add(out,ff(noise(0.09,0.02,0.002),"bandpass=f=2200:w=1800")*1.2,0); add(out,pop()*0.3,0); return out
def chord(ms, d=0.5, gap=0.07):
    out=np.zeros(int((d+gap*len(ms))*SR))
    for i,m in enumerate(ms):
        n=int(d*SR); tt=np.arange(n)/SR; f=hz(m)
        add(out,(np.sign(np.sin(2*np.pi*f*tt))*0.35+np.sin(2*np.pi*f*tt))*env(n,0.002,0.15)*0.4,i*gap)
    return out
def ding():
    n=int(0.7*SR); tt=np.arange(n)/SR
    return (np.sin(2*np.pi*1568*tt)+0.4*np.sin(2*np.pi*3136*tt))*env(n,0.001,0.22)*0.5
def wrong():
    n=int(0.45*SR); tt=np.arange(n)/SR
    return (np.sign(np.sin(2*np.pi*110*tt))+np.sign(np.sin(2*np.pi*116*tt)))*0.2*np.clip((0.45-tt)/0.05,0,1)*np.minimum(tt/0.005,1)
def ping():
    n=int(0.9*SR); tt=np.arange(n)/SR; x=np.sin(2*np.pi*1320*tt)*env(n,0.002,0.25)*0.5
    return ff(x,"aecho=0.6:0.5:180:0.3")
def tapestop():
    d=0.55; n=int(d*SR); tt=np.arange(n)/SR; f=420*(1-tt/d)**2+30
    return (np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*0.25+click()[:1].sum()*0)*np.clip((d-tt)/0.08,0,1)+np.pad(click()*1.4,(0,n-len(click())))
synth.update({"rewind":rewind,"flipcard":flipcard,"match":lambda: chord([72,76,79,84],0.45,0.06),"ding":ding,"wrong":wrong,"ping":ping,"tapestop":tapestop})
base_gain.update({"rewind":0.3,"flipcard":0.45,"match":0.3,"ding":0.3,"wrong":0.35,"ping":0.3,"tapestop":0.4})
VAR = {}
def get(name):
    name = name if name in synth else "pop"
    if name.startswith("whoosh"):  # slow to synthesize: make 3 variants once, rotate
        if name not in VAR: VAR[name] = [synth[name]() for _ in range(3)]
        return VAR[name][int(rng.integers(3))]
    return synth[name]()  # fresh each time (variation)

cues = json.load(open(os.path.join(ROOT, "tools/cues.json")))
sfx = np.zeros(N); last = {}; kept = 0
for t0, name, g in cues:
    if name in ("key","blip") and t0 - last.get(name, -9) < 0.09: continue
    if name.startswith("whoosh") and t0 - last.get("whoosh", -9) < 0.3: continue
    last[name] = t0
    if name.startswith("whoosh"): last["whoosh"] = t0
    add(sfx, get(name), max(0, t0), base_gain.get(name, 0.2) * g); kept += 1

# ---------------- mix + master ----------------
BEDG = 0.0 if os.environ.get("NOBED") else 0.3
st = np.stack([vo + sfx, vo + sfx], 1) + bed * BEDG
st /= max(1.0, np.max(np.abs(st)) / 0.95)
tmp = os.path.join(ROOT, "assets/audio/derived/_premaster.wav")
def wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    w = wave.open(path, "wb"); w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
wav(tmp, st)
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", "loudnorm=I=-13:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
js = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"loudnorm=I=-13:TP=-1.5:LRA=9:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
      f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
out = os.path.join(ROOT, "assets/audio/derived/soundtrack-nomusic.wav" if os.environ.get("NOBED") else "assets/audio/derived/soundtrack.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", af + ",aresample=48000", "-ar", "48000", "-c:a", "pcm_s16le", out], check=True)
os.remove(tmp)
print(f"cues kept {kept}/{len(cues)}; premaster I={js['input_i']} TP={js['input_tp']} -> {out}")
