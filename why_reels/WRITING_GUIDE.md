# WHY? reels — writing guide (daily backup production)

The WHY? series is the channel's best performer on Facebook ("Why is sin²θ + cos²θ = 1?" reached 1.27 lakh plays,
"Why is circle area πr²?" ~6 k, while other formats get 50–300). Every new reel must keep that formula.

**Plan:** `formula-posts/why/plan.json` — the owner's 132-topic pool in priority order. `python3 why_backup.py next`
gives the topic to make. Entries with `skip` are never made; entries with `guard` carry a rule you must follow.
**Output:** `why_reels/<short_name>.py` with `PLAN_RANK = <rank>`, rendered into
`formula-posts/why/backup/<rank:03d>_why_<short_name>.mp4` + `.txt` caption. Posting takes the backup automatically
once the main queue (`formula-posts/why/queue/`) is empty.

## Reference reels (read 2–3 before writing)
`why_reels/trig_identity.py` (the viral one), `trig_sec.py`, `sin30_half.py`, `elevation_depression.py`,
`stomata_close.py`, `blue_sky.py`. Engine: `why_kit.py`.

## Module format
```python
TITLE = "Why is the sky RED at sunset?"     # or r"...$math$..."; ≤ 6 words + subject keyword in CAPS
TAGS = "Class 10 Science"
PLAN_RANK = 1
BEATS = [ (key, narration, on-screen caption, min_seconds), ... ]   # hook first, "end" last
CAPTION = """emoji WHY? — question … 3–6 short lines … chapter + class … save/share … site + Telegram … hashtags"""
def draw(c): ...                               # the animated picture
```
Optional: `END_TEXT` (end-card pill), `END_Y`, `PART` (series badge).
Drawing helpers (see the reference reels): `c.area(cx, cy, width)` gives the drawing axes; `c.phase(beat, a, b)`
0→1 progress inside a beat; `c.at(beat)`; `c.text(x, y, s, size, color, alpha)`; `c.steps([...], ys=...)` for the
equation steps at the bottom; `ease`, `lerp`, `outline`; colours CYAN GOLD PINK GREEN PURPLE WHITE GREY.

## Standard (non-negotiable)
- **One picture explains it.** The hook asks the question in ≤ 3 s; the animation builds the answer step by step; the
  last beats state the result and the board-exam use. 30–45 s total (the viral reel is 43 s). 7–9 beats.
- **Accuracy first.** CBSE 2026–27 rationalised syllabus; never animate deleted topics. Check every fact against NCERT;
  compute every number in Python. If a plan title's premise is wrong, fix the framing (say so in the commit) or skip
  it by adding `"skip"` with the reason to that plan entry.
- **No duplicates.** Before writing, read the TITLE of every module in `why_reels/` (60+ already exist). If the topic is
  already covered, add `"skip": "already made: <module>"` to the plan entry and take the next one.
- Narration: plain spoken English, ≤ 18 words per beat, written as it should sound (Kokoro reads it literally:
  "sine thirty", "H two O"). Symbols only in on-screen text.
- Layout: nothing overlaps the title, the badge area, the step lines or the end pill; labels ≥ 18 pt; everything
  inside the frame.
- Caption: same shape as `formula-posts/why/queue/68_why_stomata_close.txt`; ends with
  `🌐 Free notes & mock papers → https://cbsemock.org.in` and `📲 Telegram: t.me/cbsemockportal`, then 6–8 hashtags
  starting `#WhySeries #CBSEMock`.

## Check, render, commit
1. `python3 why_kit.py --reel <name> --preview /tmp/p` → LOOK at every still (2 per beat). Fix until clean.
2. `python3 why_backup.py render-missing` (renders into the backup, writes the caption .txt). Watch one or two frames
   of the final MP4 (`ffmpeg -ss <t> -i <mp4> -frames:v 1 /tmp/f.png`). Length 30–45 s.
3. Commit the module, `formula-posts/why/plan.json` (if you added skips) and the new backup .mp4 + .txt:
   first line `why: backup #<rank> <short title>`, blank line, `Co-Authored-By: Claude <noreply@anthropic.com>`.
   `git pull --no-rebase`, push (retry up to 4 times). A workflow sends the owner a private Telegram preview.
