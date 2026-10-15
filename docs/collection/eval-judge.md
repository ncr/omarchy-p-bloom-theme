# Wallpaper eval, judge layer

The deterministic eval (`tools/eval_wallpapers.py`) measures what geometry can: text centred in frames, leaders,
schema, widows, glyphs, repeated phrases. The judge layer is a model looking at the rendered blocks the way the owner
does, with his taste as the rubric. It finds what the numbers cannot: a label that names the wrong part, a joke that
falls flat, a block that is technically clean and still looks wrong.

## Run

1. Crops of every block, at 1:1 pixels, from the virtual sheet (the same renderer the release uses):

       systemd-run --user --wait --collect -p Nice=18 -p MemoryMax=4G --working-directory=$PWD \
         sh -c "python3 tools/eval_wallpapers.py --crops <dir> [--only ids] [--profile 16x9-2160p]"

   `<id>-sheet.png` is the whole sheet; `<id>-<block>.png` are main (view A with callouts), B, C, left_diagram,
   right_diagram, legend, notes, punchline, emblem, each with 32 px of context.
2. A reviewer model reads `~/.claude/skills/jacek-taste/SKILL.md`, this file, then the crops of each sheet:
   the whole sheet first (composition), then every block at 1:1 (detail).
3. Findings go to a JSON list (one file per run), one object per finding:

       {"id": "c042", "block": "main", "severity": "must" | "should" | "note",
        "rubric": "<rubric key below>", "where": "<the text or part, quoted>",
        "issue": "<one sentence>", "fix": "<one sentence>"}

   `must`: the owner would stop on it. `should`: he would notice on a second look. `note`: taste call, his decision.
4. The run is scored on the labelled cases in `docs/collection/eval-cases.json` whose `layer` is `judge`
   (every case must be found on the version it was written for). Every owner note about a wallpaper that this layer
   missed becomes a new labelled case.

## Rubric

Keys in brackets go into `rubric`.

- **[label-placement]** Labels sit beside what they name, never on it; a callout's dot lands on the part it names;
  leaders are short, nearly level, and do not cross each other or run across the drawing.
- **[text-in-frame]** Text inside a box, badge or bar is optically centred; small indices belong to their frame,
  not float above it; nothing touches a line.
- **[alignment]** Siblings share edges and baselines; columns line up; rhythm between rows is even.
- **[hierarchy]** One punchline per sheet; secondary text never competes with it; title, subtitle, caption in the
  series' schema; sizes and weights tell what matters.
- **[redundancy]** Nothing says what another block already says (callout vs notes vs legend vs diagram vs punchline);
  view captions name what the view shows, not the title again.
- **[voice]** Sincere optimism, dry warm humour from a real detail, never bragging, never a disclaimer; punchlines add a
  concrete human or physical detail; wording, units and spelling consistent (British, ×, −, subscripts).
- **[truth]** Plausible physics and mechanics; numbers agree across blocks; a label names a part that is visibly there.
- **[line-work]** No gaps, doubled strokes, stray ticks, halos, clipped shapes or low-resolution mush.
- **[composition]** Detailed up close, calm from afar; empty space intended; the top 3.5 % plain (a see-through bar
  sits there); nothing crowded against an edge; the sheet reads at a glance.
- **[series]** The same structure on every sheet (legend layout, notes, view captions, callout style).

## What the owner has already said (calibration)

- b03: "70 °C in a rectangle … very hard to look at because of the positioning of text in relation to the box
  (also the superscripts above the rect!)" — text-in-frame.
- Punchlines that only retell the legend were rewritten (b13 "…THE PLUME OVER THE MILL IS ONLY CLOUD") — redundancy;
  one that adds a name and a time was kept (b04 "AMARA, 9, KISUMU. SATURN. TUESDAY, 21:10.") — voice.
- One law stated in the notes, the MODEL row and the diagram is said three times — redundancy.
- c-sheets with a different legend layout from the b-sheets — series.
