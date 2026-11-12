"""Contact sheet for review: 2 frames per scene (start+0.9s and end-0.25s) from a rendered MP4, 10 per row.
Usage: python3 tools/contact.py renders/preview.mp4 renders/contact-sheet.jpg
"""
import json, math, os, shutil, subprocess, sys, tempfile

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, out = sys.argv[1], sys.argv[2]
C = json.load(open(os.path.join(R, "cuts.json")))["cuts"]
times = []
for i in range(len(C) - 1):
    a, b = C[i] + 0.9, C[i + 1] - 0.25
    times += [round(min(a, b), 2), round(max(a, b), 2)]
font = next((f"assets/fonts/{f}" for f in ("PlayfairDisplay-Bold.ttf", "Trirong-Bold.ttf") if os.path.exists(os.path.join(R, "assets/fonts", f))), None)
T = tempfile.mkdtemp()
for i, t in enumerate(times):
    vf = "scale=216:384"
    if font: vf += f",drawtext=fontfile={font}:text='{i // 2 + 1}  {t}s':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", src, "-frames:v", "1", "-vf", vf, os.path.join(T, f"{i:03d}.png")], cwd=R, check=True)
rows = math.ceil(len(times) / 10)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", os.path.join(T, "%03d.png"), "-vf", f"tile=10x{rows}:padding=4:color=0x222222",
                "-frames:v", "1", "-q:v", "3", out], cwd=R, check=True)
shutil.rmtree(T); print(out, f"({len(C) - 1} scenes)")
