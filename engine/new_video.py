"""Create a fresh Vintage-sketch video folder from this skill.
Usage: python3 engine/new_video.py PATH/TO/video-N [VOICEOVER.mp3]
Copies tools/, src/, fonts, gsap, torn-paper frames, backdrops, the Socrates host stickers and the background music.
Never overwrites an existing folder.
"""
import os, shutil, sys

SK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) < 2:
    raise SystemExit(__doc__)
OUT = os.path.abspath(sys.argv[1])
if os.path.exists(OUT):
    raise SystemExit(f"{OUT} already exists: pick the next free video-N number")

cp = lambda a, b: shutil.copytree(os.path.join(SK, a), os.path.join(OUT, b))
cp("engine/tools", "tools")
cp("engine/src", "src")
cp("assets/fonts", "assets/fonts")
cp("engine/lib", "assets/lib")
cp("assets/props/torn-frames", "assets/props")
cp("assets/backdrops", "assets/bd")
cp("assets/host/socrates", "assets/host")
os.makedirs(os.path.join(OUT, "assets/audio/derived"))
os.makedirs(os.path.join(OUT, "renders/cover"))
shutil.copy(os.path.join(SK, "assets/music/bg-music.mp3"), os.path.join(OUT, "assets/audio/bg-music.mp3"))
shutil.copy(os.path.join(SK, "engine/example-ep01/cover.html"), os.path.join(OUT, "cover.html"))
with open(os.path.join(OUT, "package.json"), "w") as f:
    f.write('{"name": "%s", "private": true}\n' % os.path.basename(OUT))
if len(sys.argv) > 2:
    shutil.copy(sys.argv[2], os.path.join(OUT, "assets/audio/voiceover" + os.path.splitext(sys.argv[2])[1]))
print("created", OUT)
print("next: tools/tighten.py -> script.txt -> tools/words.py (or words_zip.py) -> edit tools/gen_body.py + src/scenes.js -> build -> cues -> mix -> render")
