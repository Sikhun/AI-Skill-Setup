---
name: vintage-sketch-studio
description: Make vertical (1080x1920) faceless explainer videos in a sepia pencil "Vintage sketch on aged paper" style from a voice-over, with a marble-statue host shown as a boiling torn-paper cut-out, torn-paper prop cards and red-chalk line props. Use for philosophy / history / educational storytelling clips (คลิปสเก็ตช์กระดาษเก่า, คลิปโสเครตีส, ทำคลิปจากเสียงพากย์สไตล์กระดาษสเก็ตช์), reusing its prop library, or making new torn-paper props, hosts and covers.
---

# Vintage Sketch Studio

This skill turns one voice-over into a fast faceless explainer. The canvas is aged cream paper with Acropolis and column sketches in sepia pencil. A marble statue host (Socrates by default, 5 poses) sits in the lower 42% as a torn-paper cut-out whose edge "boils" (3 frames at 8 fps, stop-motion). Keywords type in word by word in the top zone, and props prove each line: torn-paper cards and red-chalk drawings. The editing system (beat per phrase, hook, sub-beats, SFX on every hit) is engineered for high-retention vertical storytelling.

Example output: `example-output/ep01-socrates.mp4` ("โสเครตีสคือใคร", Thai, 59 s, 17 scenes) with `contact-sheet.jpg` and 2 covers.

## Start here
| user wants | do |
|---|---|
| install on a new machine | `SETUP.md` |
| a video from a voice-over | the Workflow below |
| to reuse or browse props | `assets/props/PROPS.md` + `props-sheet.jpg` (props in this skill MAY be reused) |
| a new torn-paper card size or a new host | `tools/torn.py` (see "Making new paper") |
| covers only | `engine/example-ep01/cover.html` (2 variants, screenshot at 1080x1920) |

Reply in the user's language. Users are not technical: name files exactly, run commands yourself, and deliver previews they can open, not paths.

## Bundle layout
- `references/style-spec.md` is the full visual spec: palette (paper #EFE4CC, ink #3A2A1E, soft #7A5C43, sanguine #A8432A, gold #B08A3E), fonts, the host torn-edge rule (angular faceted edge about 24px wide, lit rim, depth shadow), layout zones and labels. It is the default, so change only what the user asks.
- `assets/styleboard/` has 3 sample frames as HTML/PNG plus `boil-preview.mp4`. Copy these classes rather than reinventing the look.
- `assets/props/` is the prop library: `svg/props.js` (16 line props), `torn-frames/<size>/f0-f2.png` (6 card sizes), `PROPS.md` and `props-sheet.jpg`. Reuse these freely and add new props in the same style.
- `assets/host/socrates/<pose>/f0-f2.png` holds the 900px boil stickers for 01-thinking, 02-questioning, 03-explaining, 04-skeptical and 05-surprised. `socrates-originals/` has the source images. Anyone who received this skill may use the Socrates host in their own videos.
- `assets/backdrops/` has `acropolis.svg` and `columns.svg`. They are original code-drawn sketches and `tools/backdrops.py` regenerates them.
- `assets/fonts/` has Chonburi (Thai headlines), Trirong 400/700 (Thai text), Playfair Display 700/900 (Latin labels and numbers) and Special Elite (Latin notes), all SIL OFL.
- `assets/music/bg-music.mp3` is the channel's background track. It is always the music bed unless the user names another song.
- `engine/` holds the pipeline:
  - `engine/new_video.py` creates a video folder.
  - `engine/tools/` has the tested scripts.
  - `engine/src/` has the composition parts: head.html for CSS, helpers.js for animation and transitions, props.js, and scenes.js for the EP.01 timeline.
  - `engine/example-ep01/` is the complete EP.01 source (gen_body.py, scenes.js, cuts.json, script.txt, transcript.json, cover.html, and its tightened voice-over `voiceover-ep01.mp3`). Copy its patterns.

## Workflow
1. **New folder.** Run `python3 engine/new_video.py <workdir>/video-N <voiceover.mp3>`. Check which video-N numbers already exist, and never write into an old video's folder. Keep the original VO untouched; all edits go to copies in `assets/audio/derived/`.
2. **Tighten.** Always cut dead air and long pauses so the clip feels tight and fast. Run `ffmpeg -i assets/audio/voiceover.mp3 -af atempo=1.07 assets/audio/derived/vo-fast.wav`, then `python3 tools/tighten.py assets/audio/derived/vo-fast.wav assets/audio/derived/vo-tight.wav --gap 0.15 --long 0.24`. Pause trimming alone gives only about 8%. Tell the user the speed-up and the old and new length. `tighten.py` always rewrites `tools/tight-map.json`, so copy it before tightening a second file (for example a replacement outro), and splice with ffmpeg `atrim` + `concat`.
3. **Script and word times.** Write `script.txt` with one line per phrase in the order `tighten.py` printed, so the line count matches the phrase count. Run `python3 tools/words.py` to get `transcript.json`. For Thai, use `tools/words_zip.py` to get exact per-character times with the sherpa-onnx Thai zipformer (`pip install sherpa-onnx`, model `sherpa-onnx-zipformer-thai-2024-06-20` from the k2-fsa GitHub releases, unpacked into `~/asr/`, or set `ASR_MODEL` to its folder). `tools/asr_phrases.py` prints what each phrase sounds like. Words the recogniser could not hear clearly go on screen as your best guess, and you list them for the user to check.
4. **Plan scenes.** Use one scene per 1-3 phrases, about 15-25 scenes per minute. Write `cuts.json` (`{"cuts":[0, ..., DURATION]}`, with cuts slightly before each phrase start). Per scene, plan a headline split (a small `.s` lead line plus a big `.h` keyword, red `.r` on the key word), one or two props, a host pose that matches the meaning, and a sub-beat every 0.5-1.5 s (swap the text block, draw a prop, stamp a seal, change the pose).
5. **Build the body.** Edit the SCENES in `tools/gen_body.py` with the helpers `card()` (torn-paper card), `host(n, side, [(pose, mirror)])`, `svg()`, `w(n, text, word, cls)` (word typed on its spoken time) and `bd()` (backdrop). Then run `python3 tools/gen_body.py`.
6. **Timeline.** Edit `src/scenes.js` and copy the per-scene blocks from the example.
   - Transitions are tSmudge, tPage, tPencil, tErase, tInk, tSlow and tFlash. Vary them and never use the same one twice in a row.
   - The host uses `hIn` / `hPose`.
   - The other building blocks are `card`, `sv` (draw-on), `swap`, `stamp`, `count`, `shake` and `flash`.
   - Every hit calls `cue(t, sfx, gain)`.
   - Keep the global boil line `tl.set("#root",{attr:{"data-f":k%3}},k/8)`, because it drives every torn edge.
7. **Build and preview.** Run `python3 tools/build.py`, then `node tools/frames.js preview.jpg t1 t2 ...` (it needs Playwright: `npm i -g playwright && npx playwright install chromium`, or set `CHROME=/path/to/chrome`). Look at every frame and check that the text is readable, that nothing is clipped by the torn margin (keep text 50px inside a card), and that the host never covers the text.
8. **Sound.** Run `python3 tools/cues.py`, then `python3 tools/mix.py` (VO +7 dB, bg-music ducked under the VO, synthesized SFX, mastered to about -13 LUFS). Run `NOBED=1 python3 tools/mix.py` for the no-music track.
9. **Render.** Copy `index.html` and `assets/` to a local temporary folder (rendering on a network or cloud folder is slow) and run `npx hyperframes render <dir> -o final.mp4`. For the no-music version, change `soundtrack.wav` to `soundtrack-nomusic.wav` in a second copy's index.html and render again. Make `-small` versions with ffmpeg at about 3 Mbps for chat delivery, and a contact sheet with `tools/contact.py`.
10. **Covers.** Always make 2 covers (1080x1920) with `cover.html`. Variant 1 is the hook headline with the questioning host; variant 2 is a bolder curiosity headline with a dark page and a seal. Also give 2-3 alternative headlines and a post caption with hashtags.

## Making new paper
- New card size: from `tools/`, run `python3 torn.py rect W H OUTDIR`. It writes f0-f2 with a 60px pad, then you add the size to `CARD` in gen_body.py.
- New host: give each pose a transparent PNG on a consistent canvas, then run `python3 torn.py host pose.png OUTDIR` to get 3 boil frames with an angular torn edge, lit rim and shadow. Never redraw or alter a user's character.

## Style rules
- Use torn-paper edges that are angular (straight facets), thin, and have depth. Do not use round or fluffy edges.
- The setting is classical architecture (Parthenon, Acropolis, columns).
- Keep all text in the classic fonts listed above.
- The style is original. Do not use logos or characters from other brands.
- Deliver the music version, the no-music version, 2 covers and a contact sheet every time.
