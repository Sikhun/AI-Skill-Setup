# Vintage Sketch Style Spec

The editing system is a fast faceless explainer (beat per phrase, keyword pop-ups, host in the lower part, SFX on every hit). The theme is a sepia pencil and ink architectural sketch of classical antiquity (Parthenon, Acropolis, columns) on aged cream paper. This spec is the default look; change only what the user asks.

## Editing system (unchanged)
Keyword pop-ups 1-4 words at y 17-36%, no running subtitles, host in lower 40-60%, scene change every 2-4s with a visual beat every ~1s, hook in first 2s, safe zones (bottom 20%, right 12%, top 8%), -13 LUFS master, 2 covers per video, bg-music.mp3 + a no-music version.

## Fonts (assets/fonts/)
| role | font |
|---|---|
| Thai headlines / keywords | **Chonburi** 84-120px (2nd line max ~84px for long phrases) |
| Prop / note text | **Trirong** 400/700 |
| Latin labels, Roman numerals | **Playfair Display** Bold (labels, letter-spaced) / Black (numerals I II III) |
| Latin margin notes, seal text | **Special Elite** (typewriter) / Playfair Black |

## Palette
paper #EFE4CC (centre #F4EBD6, edge #D8C39B) · sepia ink #3A2A1E · soft ink #7A5C43 · **sanguine (red chalk) accent #A8432A** (light #C4673F) for key highlights and accents · gold leaf #B08A3E for small ornaments only.

## Host
A marble Socrates-style statue, 5 half-body poses (1254px RGBA originals in assets/host/socrates-originals/): 01-thinking (hand on beard, looking up), 02-questioning (both palms up, shrug), 03-explaining (index finger up), 04-skeptical (arms crossed, side-eye), 05-surprised (palm up, hand on chest, shocked). Keep the photoreal marble as is; do not redraw.
Display rule: the host is always shown as a **torn-paper cut-out** with an ANGULAR outline (thin faceted polygon ~24px around the figure, top-left light: lit rim white, far rim grey, edge darkening, figure casts a small shadow on its paper, two-layer drop shadow, gaps between arm and head filled, straight torn segments with a small jagged grey-fibre rim; not a smooth contour-hugging edge) (cream paper rim with white torn fibres + soft brown drop shadow) whose edge **boils** stop-motion style: 3 re-torn frames looped at 8 fps (each held 3 frames @24fps), each frame also nudged ±2px / ±0.7°. Pre-rendered: assets/host/socrates/<pose>/f0-f2.png. Make new ones with tools/torn.py host IN.png OUTDIR.

## Torn-paper props
Every rectangular prop frame/card/page is a torn-paper card with the same boiling edge (tools/torn.py rect W H OUTDIR -> f0-f2.png; ready sizes in assets/props/torn-frames/). Text, chalk marks, seals and tape sit on top of the card and stay still while the edge boils.

## Props / pop elements (drawn as sketch lines, wobbly via SVG displacement filter)
- Torn-paper cards (see above) for the main point, comparisons, B-roll photos; masking tape and "fig. 1/2" labels
- Column/pediment line sketch only as background (not a prop frame)
- Sanguine chalk marks: strike-through, X, circle, underline, tick (drawn on with stroke animation)
- Sanguine wax seal ("SOPHIA", "ALETHEIA" = truth, "PSEUDOS" = false) instead of rubber stamp; thud on hit
- Olive/laurel wreath around the winner / correct answer
- Architect's dimension lines, compass arcs, ruler ticks for comparisons and numbers
- Roman numerals for lists; ornamental rule with gold diamond under chapter labels
- Backdrops (Athens): original code-drawn pencil sketches in assets/backdrops/ (tools/backdrops.py): acropolis.svg (Parthenon + small temple on the rock, hills, city, cypresses) and columns.svg (close-up Doric colonnade ruin). Use at 20-50% multiply behind host/hook. Labels in Latin letters with Greek words (LOGOS · I, seal SOPHIA): Playfair has no Greek glyphs.

## Texture
Paper fibre noise (multiply), large soft stains, burnt brown edge vignette, loose background scribbles (like the sample), optional line boil (re-seed the wobble filter at 8 fps) on props.

## Transitions
Pencil draw-on (lines draw, then hatch/fill fades in) = main · smudge blur dissolve · page turn / page slide · eraser wipe · ink-wash bleed (dip to sepia instead of dip to black) · 0.2-0.4s.

## SFX / music
Pencil scratch (draw-on), paper flip/slide, charcoal smear, chalk tap for marks, wax-seal thud, stone chisel tap on numerals, soft whoosh. Music: assets/music/bg-music.mp3 by default, plus a no-music render.

## Files
assets/styleboard/frames.html (3 sample frames, HTML/CSS ready to port to HyperFrames), frame-A/B/C.png, styleboard.jpg. Render: chrome --headless --screenshot --window-size=1080,6000 --virtual-time-budget=3000, then crop 1920px slices.

Preview of the boiling edge: assets/styleboard/boil-preview.mp4 (3 sample frames, 2.5s each).
