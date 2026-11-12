# SETUP: install everything for this skill (for Claude Code to run)

> Reference copy of the detailed install steps. For this skill, follow `SETUP.md` for the order and use its Self-test, not the one below.

The user has only installed Claude Code and pasted a request like "อ่าน SETUP.md แล้วติดตั้งทุกอย่างให้หน่อย". Do the whole setup for them, step by step, talking to them in Thai (short, friendly, no jargon). They may not know what a terminal is.

## Rules
- Detect the OS first (`uname -s`; on Windows you are in PowerShell or Git Bash). Follow the matching section.
- Check before installing: skip anything already present (`command -v` / `Get-Command`). Never reinstall or upgrade what works.
- Run one step at a time, show the user what you are doing in one Thai sentence, and verify each step before moving on.
- Steps that need the user's password or an admin prompt (Homebrew's installer, UAC on Windows) cannot be typed by you. Tell the user exactly what will pop up and what to do (type their Mac login password and press Enter, or click "Yes"), or give them the single command to paste into Terminal themselves, then wait and re-check.
- If a command fails, read the error, fix it using the troubleshooting table, and retry once. If it still fails, explain in plain Thai what is wrong and what they can do.
- Do not change system security settings beyond what is listed here.
- When finished, tell the user in Thai: what was installed, where the test video is, and the exact sentence to type next time to make a video.

## macOS
1. Homebrew: `brew -v`. If missing, the installer needs the user's password, so ask them to paste this into Terminal and follow the prompts:
   `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   On Apple Silicon also run the two `eval "$(/opt/homebrew/bin/brew shellenv)"` lines the installer prints (add to `~/.zprofile`).
2. Tools: `brew install node git git-lfs ffmpeg python numpy` (only the missing ones; skip python/numpy if `python3 -c "import numpy"` already works), then `git lfs install`.
3. Check `ffprobe`: `which -a ffprobe`. If the first hit is not FFmpeg's (e.g. a script in `~/bin`), use `/opt/homebrew/bin/ffprobe` via `HYPERFRAMES_FFPROBE_PATH` in step 7.
4. HyperFrames plugin:
   `claude plugin marketplace add https://github.com/heygen-com/hyperframes.git`
   `claude plugin install hyperframes@hyperframes`
   (Always the https URL; the short `heygen-com/hyperframes` form fails with "Host key verification failed" on machines without GitHub SSH keys. If the clone fails on LFS files, step 2's `git lfs install` was skipped.)
5. Install this skill for every project: copy this whole `vintage-sketch-studio` folder to `~/.claude/skills/vintage-sketch-studio/` (skip if it is already running from there).
6. Fonts (optional, for editing the props by hand): copy `assets/fonts/*.ttf` to `~/Library/Fonts/`.
7. Self-test with the real pipeline (see "Self-test" below) in `~/Desktop/edit-video/video-test`. Prefix `npx hyperframes ...` with `HYPERFRAMES_FFPROBE_PATH=/opt/homebrew/bin/ffprobe` if step 3 found a wrong ffprobe.
8. Tell the user to restart Claude Code (or type `/reload-plugins`) so the HyperFrames and vintage-sketch-studio skills load.

## Windows 10 / 11
1. Tools with winget (each may show a UAC prompt; tell the user to click "Yes"):
   `winget install -e --id OpenJS.NodeJS.LTS`, `winget install -e --id Git.Git`, `winget install -e --id GitHub.GitLFS`, `winget install -e --id Gyan.FFmpeg`, `winget install -e --id Python.Python.3.12` (only the missing ones). If `winget` is missing, ask the user to update "App Installer" from the Microsoft Store.
2. New programs are not on PATH in the current shell. Ask the user to close and reopen Claude Code in a new PowerShell window, then continue from step 3 (re-read this file).
3. `git lfs install`; `python -m pip install numpy`; verify `node -v`, `ffmpeg -version`, `ffprobe -version`, `python -c "import numpy"`. (If `python` opens the Microsoft Store, use `py` instead.)
4. If PowerShell blocks `npx` scripts ("running scripts is disabled"): `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force`.
5. HyperFrames plugin: same two `claude plugin ...` commands as macOS step 4.
6. Install this skill: copy this folder to `$HOME\.claude\skills\vintage-sketch-studio\`.
7. Fonts (optional): copy `assets\fonts\*.ttf` into `$env:LOCALAPPDATA\Microsoft\Windows\Fonts\` and register them, or tell the user to right-click each .ttf → Install.
8. Self-test (see "Self-test" below) in `$HOME\Desktop\edit-video\video-test`, using `python` instead of `python3` and `$env:NOBED=1` instead of `NOBED=1`. If images fail to render: `$env:HYPERFRAMES_FFPROBE_PATH = (Get-Command ffprobe).Source`. On Windows always call `npx hyperframes ...` directly; `package.json` scripts with `VAR=value cmd` prefixes are macOS/Linux syntax.
9. Tell the user to restart Claude Code so the skills load.

## Self-test (both systems)
Builds a 7-second clip with the engine's starter scenes, the sample host and the bundled voice sample, so every part (Python tools, Chrome, HyperFrames, FFmpeg) is proven. `SKILL` = this skill's folder.
1. Make `video-test/` with `assets/audio`, `assets/host`, `renders`; copy `SKILL/engine/tools` → `tools/`, `SKILL/engine/src` → `src/`, `SKILL/engine/demo/script.txt` and `cuts.json` → the folder root, `SKILL/assets/fonts` → `assets/fonts/`, `SKILL/assets/music/bg-music.mp3` → `assets/audio/bg-music.mp3`, `SKILL/assets/host/socrates/*/*.png` → `assets/host/`, and write `package.json` = `{"name":"video-test","private":true}`.
2. `ffmpeg -y -i SKILL/engine/example-ep01/voiceover-ep01.mp3 -t 9 assets/audio/voiceover.mp3`
3. `python3 tools/tighten.py assets/audio/voiceover.mp3 assets/audio/derived/vo-tight.wav` (expect 5 phrases, ~7.4s; if the count differs, add or merge lines in script.txt and set the last number in cuts.json to the printed duration)
4. `python3 tools/words.py`, `python3 tools/build.py`, `python3 tools/cues.py` (downloads HyperFrames' Chrome the first time), `python3 tools/mix.py`, `npx hyperframes check` (only the expected warnings listed in `engine/README.md`), `npx hyperframes render -q draft -o renders/preview.mp4`, `python3 tools/contact.py renders/preview.mp4 renders/contact.jpg`. The render needs the soundtrack from mix.py, so keep this order.
5. Look at `renders/contact.jpg`: 4 scenes, Socrates host, Thai headlines, red folder scene, iris-out ending. Open `renders/preview.mp4` for the user.
6. Optional (better word timing, ~3 GB download, ask first): `npx hyperframes transcribe assets/audio/voiceover.mp3 -m large-v3 -l th` once installs whisper and the model that `tools/words.py` uses.

## Reference analysis (last step, both systems)
After the self-test passes, analyse the two reference clips exactly as `references/videos/README.md` says: run `engine/tools/analyze_ref.py` on each into `~/Desktop/edit-video/ref-analysis/` (Windows: `$HOME\Desktop\edit-video\ref-analysis\`), look at every image, and write `~/Desktop/edit-video/REFERENCE-ANALYSIS.md` with the 8 headings (pacing and cut frequency, typography and captions, motion graphics, B-roll/image placement, zooms and camera movement, transitions, sound-design rhythm, composition and safe zones). This is the user's standing brief: "These are the reference videos. Analyse them and keep this understanding for the next command." Give the user a short Thai summary (one line per heading), then stop and wait for their next instruction. Do not start a video on your own.

## Final message to the user (Thai, adapt the paths; send it together with the reference summary)
"ติดตั้งครบแล้วครับ ✓ … (list) คลิปทดสอบอยู่ที่ … วิเคราะห์คลิป reference แล้ว อยู่ที่ REFERENCE-ANALYSIS.md … ครั้งหน้าอยากทำคลิป ให้เปิด Claude Code ในโฟลเดอร์ edit-video แล้วพิมพ์ว่า: ใช้สกิล vintage-sketch-studio ทำคลิปจาก voiceover.mp3 ใช้ตัวละครในโฟลเดอร์ poses (ถ้ายังไม่มีบท พิมพ์ว่า: ช่วยเขียนบทคลิปสไตล์กระดาษสเก็ตช์เรื่อง ...)"
