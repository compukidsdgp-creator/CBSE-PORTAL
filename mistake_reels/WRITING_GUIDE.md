# Mistake Bank reels — writing guide (for the nightly writing run)

The locked references: `mistake_reels/specs/001-class10-chemistry-subscripts.py` (custom "molecules" scene) and
`mistake_reels/specs/002-class10-chemistry-ph-backwards.py` (generic "flip" scene — use this pattern).

## What to write
- Source: the `mistakes` rows of LIVE chapter notes (`python3 -c "from notes_pages import load_chapters; ..."`, status "live").
  Take them in chapter order; skip any already covered by a spec (compare `chapter` + topic). Never invent a mistake that is not in the notes.
- One spec = `mistake_reels/specs/NNN-<id>.py` (NNN = next number, 3 digits; id = class10-<subject>-<short-slug>).
- Revisions first: an entry with "status": "changes" in `mistake_reels/approvals.json` → apply the owner's note to that spec,
  delete its videos (`mistake_reels/video/NNN-*`) and its Hindi clips (`mistake_reels/voice/<id>/`) so they are remade, and remove the entry.

## Spec rules (copy 002 exactly in structure)
- `scene.type` = "flip". Per language: `q` (the question/context, short), `wrong` (what students write; wrap the wrong part in `<s>`),
  `right` (the fix; wrap the key words in `<mark>`), `wrong_label` / `right_label`.
- Optional `svg_wrong` / `svg_right`: a clean inline SVG (viewBox about 960×230, Poppins/Inter, no external images) that shows the idea
  (a scale, a strip, a mini diagram). Must be accurate; labels inside the viewBox.
- Beats, in this order: intro, hook, setup, wrong, right, done. Each = (key, narration, on-screen caption).
  - intro: "Top board exam mistake, number <N in words>!" / "बोर्ड एग्ज़ाम की टॉप गलती, नंबर <N in Hindi words>!"
  - English narration total ≤ 15 s at speed 1.15 (about 40 words over all beats). Short, punchy, spoken English.
  - Hindi: natural spoken Hindi in Devanagari (the voice reads Devanagari only — write English terms and symbols as they are spoken:
    "पी एच", "एच टू ओ", "हाइड्रोजन आयन"). Captions may use symbols (pH, H₂O). Keep it as short as the English.
  - The stamp's first word appears in the wrong caption ("WRONG" / "गलत").
- `rule`: two short lines to remember. `badge`: "Class 10 · <Subject> · Ch <n>". `cta` as in 002.
- Accuracy: every fact must match the chapter notes and NCERT; check it twice.

## Check before committing
1. `python3 -c "import generate_mistake_reel as G; print([r['id'] for r in G.load_specs()])"` lists your spec.
2. Preview the English version at 4–5 points: `python3 generate_mistake_reel.py <N> --lang en --preview 9 --out /tmp/p.jpg` and LOOK:
   text must fit the card (shorten if it wraps past 3 lines), the SVG must be clear.
3. Commit only the spec (and approvals.json for a revision). First line: `mistake: draft #NN <title>` (or `mistake: revise #NN …`).
   The workflow makes the Hindi voice, renders both videos and sends them to the owner.
