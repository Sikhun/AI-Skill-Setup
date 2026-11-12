"""Word timings for every phrase of the tightened VO -> transcript.json

Needs script.txt in the video folder: the exact spoken text, ONE LINE PER PHRASE, in the same order and count
as the phrases tighten.py printed (a phrase = speech between two pauses). Edit line breaks until the counts match.
ElevenLabs tags in [brackets] are removed; the "[ทำเสียงชู่]" shh sound usually becomes its own phrase: put it on its own line.

With whisper-cli (whisper.cpp) installed it gets per-token times for each phrase; without it, or when the
recognised text differs from the line, W() later falls back to the word's position inside the phrase (still close).

Usage: python3 tools/words.py [--lang th|en]
Model: $WHISPER_MODEL, else the first ggml-*.bin in ~/.cache/hyperframes/whisper/models/ (large-v3 preferred).
First time: `npx hyperframes transcribe assets/audio/voiceover.mp3 -m large-v3 -l th` installs whisper-cli and the model (~3 GB).
"""
import argparse, glob, json, os, shutil, subprocess, tempfile

ap = argparse.ArgumentParser(); ap.add_argument("--lang", default="th"); a = ap.parse_args()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tm = json.load(open(os.path.join(ROOT, "tools", "tight-map.json")))
import re
def clean(l):  # ElevenLabs audio tags like [ทำเสียงชู่] are not words; a tag-only phrase is the shh sound itself
    t = re.sub(r"\[[^\]]*\]", "", l).replace("...", " ").replace("…", " ").strip()
    return t if t else ("ชู่ว์" if "ชู่" in l else l.strip("[] "))
lines = [clean(l) for l in open(os.path.join(ROOT, "script.txt"), encoding="utf-8") if l.strip()]
P = tm["phrases"]
if len(lines) != len(P):
    print(f"MISMATCH: script.txt has {len(lines)} lines but the VO has {len(P)} phrases.")
    for i in range(max(len(lines), len(P))):
        t = f"{P[i]['start']:6.2f}-{P[i]['end']:6.2f}" if i < len(P) else "      -      "
        print(f"  {i + 1:>3} {t}  {lines[i] if i < len(lines) else '(no line)'}")
    raise SystemExit("Fix script.txt line breaks (merge lines spoken without a pause, split where there is one), "
                     "or re-run tighten.py with a different --min-silence, then run this again.")

wc = shutil.which("whisper-cli") or shutil.which("whisper-cpp")
if not wc:  # runtime that `npx hyperframes transcribe` installs
    hits = [h for h in glob.glob(os.path.expanduser("~/.cache/hyperframes/whisper/**/whisper-cli*"), recursive=True) if os.path.isfile(h)]
    wc = hits[0] if hits else None
model = os.environ.get("WHISPER_MODEL")
if not model:
    ms = sorted(glob.glob(os.path.expanduser("~/.cache/hyperframes/whisper/models/ggml-*.bin")), key=lambda m: ("large-v3" not in m, m))
    model = ms[0] if ms else None
if not (wc and model): print("whisper-cli or model not found: using in-phrase position for word times (fine for most edits).")

S = tempfile.mkdtemp(); out = []
for ph, txt in zip(P, lines):
    a0, b = max(0, ph["start"] - 0.08), ph["end"]; toks = []
    if wc and model:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(ROOT, tm["audio"]), "-ss", str(a0), "-to", str(b + 0.08),
                        "-ar", "16000", "-ac", "1", f"{S}/w.wav"], check=True)
        subprocess.run([wc, "-m", model, "-l", a.lang, "-f", f"{S}/w.wav", "-np", "-ojf", "-of", f"{S}/w"], capture_output=True)
        try:
            d = json.loads(open(f"{S}/w.json", "rb").read().decode("utf-8", "surrogateescape")); acc = b""
            for seg in d["transcription"]:
                for t in seg["tokens"]:
                    if t["text"].startswith("[_"): continue
                    acc += t["text"].encode("utf-8", "surrogateescape")
                    toks.append([round(a0 + t["offsets"]["from"] / 1000, 3), acc.decode("utf-8", "ignore").strip()])
        except Exception as e:
            print("  whisper failed on phrase", ph["n"], e)
    asr = toks[-1][1] if toks else ""
    out.append({"n": ph["n"], "start": ph["start"], "end": ph["end"], "text": txt, "asr": asr, "tokens": toks})
    print(f"{ph['n']:>3} {ph['start']:6.2f} {txt} | {asr}")
json.dump({"audio": tm["audio"], "phrases": out}, open(os.path.join(ROOT, "transcript.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("-> transcript.json")
