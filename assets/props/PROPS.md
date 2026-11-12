# Vintage Sketch Prop Library

The props used in EP.01, ready to reuse. `props-sheet.jpg` shows everything at once, and `props-sheet.html` is the same sheet as live HTML.

## 1. SVG line props (`svg/props.js`)
These are sepia pencil props with red-chalk accents. Place one with `<div class="svg" data-svg="NAME" style="left:..;top:..;width:..;height:.."></div>`, and `props.js` fills it in. Animate with `draw(sel, t, dur, sound)`, which draws every path on (see `helpers.js`).

| name | looks like | good for |
|---|---|---|
| bub | speech bubble with "..." | people talking, dialogue |
| bubq | speech bubble with "?" | asking questions |
| qmark | big red-chalk "?" | doubt, open questions |
| heart | outlined heart | goodness, love, like button |
| scales | balance scales | justice, comparing two sides |
| check | red-chalk tick | "correct", certainty |
| magni | magnifying glass | examining, investigating |
| scroll | scroll + quill | writings, records, history |
| cup | kylix cup + red drop | poison, drinking, a verdict carried out |
| arrow | curved red-chalk arrow | influence, A leads to B |
| plus | circled "+" | follow button, adding |
| strike | red-chalk strike-through (stretchable) | crossing out a wrong belief |
| xmark | red-chalk X | wrong, rejected |
| timeline | dimensioned line with ticks | years, BC to today |
| laurel | laurel wreath | honour, legacy, an ending |
| circ | hand-drawn red circle | highlighting a word or number |

New props follow the same rules. Lines use `class="ink"` (sepia #3A2A1E, 5px, round caps, `filter="url(#rough)"`), accents use the `CH(width)` red chalk, and fills are only paper tones (#F7F0DF, #E6D6A8, #E2CC98).

## 2. Torn-paper frames (`torn-frames/<size>/f0-f2.png`)
Each frame is a sheet of paper with angular torn edges, lighting and a drop shadow. There are 3 boil frames that swap at 8 fps. The PNG size includes a 60px transparent margin on every side, so content should go inside `inset:60px`.

| size | PNG | used for |
|---|---|---|
| strip | 1000x420 | one-line question or headline cards |
| big | 880x680 | lists, charge sheets, long text |
| mid | 720x540 | a keyword plus a small caption |
| small | 540x460 | a number or short tag |
| tag | 500x340 | names (SOKRATES / PLATO) |
| sq | 440x440 | icons (heart, plus) |
| torn-card-420x340, torn-card-760x560 | | the styleboard versions |

In a video, call `card(id, kind, x, y, inner, rot, scale)` in `gen_body.py`. To make a new size, run `python3 tools/torn.py rect W H OUTDIR` from the skill folder.

## 3. CSS props (in `head.html`)
- `.seal` is a red wax seal with a rough edge. Put text in a `<span>` and use `stamp()` to bring it in.
- `.tape` is a piece of masking tape for taping cards down.

## 4. Related files
- The host is the Socrates statue, 5 poses, as torn stickers with 3 boil frames each, in `assets/host/socrates/`.
- The backdrops are `assets/backdrops/acropolis.svg` and `columns.svg`. Add them with `mix-blend-mode: multiply` at opacity 0.16-0.45.
