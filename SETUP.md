# Setup (for the AI to run)

The user has installed Claude Code, opened this folder and typed something like "อ่าน SETUP.md แล้วติดตั้งทุกอย่างให้หน่อย". Do the whole setup for them, one step at a time, in their language, without jargon. Check before installing and skip anything that already works. `SETUP-guide.md` has the detailed Mac and Windows steps (password prompts, PATH, troubleshooting); follow it for steps 1-4.

1. **Claude Code + package manager.** Homebrew on Mac, winget on Windows.
2. **Tools.** `brew install node git git-lfs ffmpeg python` (Windows: winget Node.js, Git, Git LFS, FFmpeg, Python), then `git lfs install`.
3. **HyperFrames plugin.** `claude plugin marketplace add https://github.com/heygen-com/hyperframes.git`, then `claude plugin install hyperframes@hyperframes`. Check with `npx hyperframes doctor`, and run `npx hyperframes browser ensure` once.
4. **Python packages.** `python3 -m pip install numpy pillow`.
5. **Thai word timing (needed for Thai voice-overs).** `python3 -m pip install sherpa-onnx`. Download `sherpa-onnx-zipformer-thai-2024-06-20.tar.bz2` from https://github.com/k2-fsa/sherpa-onnx/releases (tag `asr-models`) and unpack it into `~/asr/`, so the folder `~/asr/sherpa-onnx-zipformer-thai-2024-06-20/` exists. (Another location works if you set `ASR_MODEL` to that folder.)
6. **Frame previews.** `npm i -g playwright && npx playwright install chromium`. `engine/tools/frames.js` finds Playwright on its own; to use another Chrome, set `CHROME=/path/to/chrome`.
7. **Install the skill itself** so every new Claude Code session knows this style without being told:
   - Mac: `mkdir -p ~/.claude/skills && cp -R <this folder> ~/.claude/skills/vintage-sketch-studio`
   - Windows: copy the folder to `%USERPROFILE%\.claude\skills\vintage-sketch-studio`

   Claude Code then loads `SKILL.md` automatically whenever the user asks for a video in this style, from any folder.
8. **Self-test** (below), then **finish**: read `SKILL.md`, `references/style-spec.md` and `assets/props/PROPS.md`, and tell the user in 5 short lines how videos in this style are cut (look, host, props, pacing and transitions, deliverables), so they can see the AI understood. Then say the setup is done, where the test video is, and the sentence to type next time: "ทำคลิปสไตล์ Vintage sketch จากเสียงนี้" with a voice-over attached.

## Self-test
Rebuild the example EP.01 with its own bundled voice-over (`<skill>` is this folder):
```
python3 <skill>/engine/new_video.py ~/Desktop/edit-video/video-test
cd ~/Desktop/edit-video/video-test
cp <skill>/engine/example-ep01/{cuts.json,script.txt,transcript.json,cover.html} .
cp <skill>/engine/example-ep01/gen_body.py tools/ && cp <skill>/engine/example-ep01/scenes.js src/
mkdir -p assets/audio/derived
ffmpeg -y -i <skill>/engine/example-ep01/voiceover-ep01.mp3 -ar 48000 assets/audio/derived/vo-final.wav
echo '{"audio":"assets/audio/derived/vo-final.wav","duration":59.22}' > tools/tight-map.json
python3 tools/gen_body.py && python3 tools/build.py && python3 tools/cues.py && python3 tools/mix.py
npx hyperframes render . -q draft -o renders/test.mp4
```
The result should be about 59 s long and look like `example-output/ep01-socrates.mp4`. Open it for the user. On Windows use `python` instead of `python3` and copy the files one by one.
