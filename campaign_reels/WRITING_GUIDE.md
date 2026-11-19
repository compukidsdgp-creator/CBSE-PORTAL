# 60-day "90+ Score Hack" reel campaign — writing guide

The owner's plan (CBSEMock_60_Day_Reel_Campaign.xlsx), ranked and fact-checked, is `campaign_reels/plan.json`:
43 weekday reels, 20 Nov 2026 → 19 Jan 2027, one per weekday at **1:01 PM IST**. Each entry has the date, pillar,
topic, hook direction, brief, CTA, destination page and a **note with guardrails — the note always wins**.
Reels **publish automatically** on their date (owner decision), so every fact must be right before you commit.

Reference spec (format locked): `campaign_reels/specs/01-step-marking.py`. Renderer: `generate_hack_reel.py`.

## Spec format — `campaign_reels/specs/NN-<slug>.py`
`REEL = {"n", "id", "date", "pillar", "voice": "af_heart", "speed": 1.12, "dest", "beats": [...], "caption", "hashtags"}`
- `n`, `date`, `pillar`, `dest` exactly as in plan.json. `id` = short kebab slug of the topic.
- 4–6 beats. Each beat: `{"say": narration, "card": {...}}`, optional `"cap"` (caption text if it should differ from
  `say`, e.g. symbols) and `"hold"` (extra seconds after the narration).
- Beat 1 is always the **hook**: `title` card, ≤ 8 words on screen, said in the first 2.5 s. No logo intro.
- Last beat is always the **end** card: `{"type":"end","cta": one action ≤ 32 chars,"url": ≤ 34 chars}`. For long page
  names show `cbsemock.org.in` and name the page in `cta` (e.g. "Class 12 Maths mock papers").
- Total 16–24 s (renderer prints it). Narration ≈ 40–55 words in total. One idea per screen.

## Card types (text limits keep it readable on a phone)
| type | fields | limits |
|---|---|---|
| title | `kicker`, `big` | big ≤ 8 words |
| list | `title`, `items` (`numbered`: false for ✓) | ≤ 4 items, ≤ 5 words each |
| chain | `title`, `items`: [[label, detail], …] | ≤ 4 steps, detail ≤ 26 chars |
| compare | `wrong`: [label, body], `right`: [label, body] | body ≤ 60 chars |
| quiz | `q`, `opts` (4), `ans` (0–3) | q ≤ 90 chars, option ≤ 24 chars; add `"hold": 1.3` so the countdown + reveal play before the next beat; the next beat explains the answer |
| worked | `title`, `lines`: [[tag, text], …] (last line = highlighted final answer) | ≤ 5 lines, ≤ 28 chars |
| recap | `kicker`, `big` | ≤ 7 words |
| end | `cta`, `url` | see above |

Pillar rhythm: Score Hack = list/chain; Board FAQ = compare/recap; Beat the Timer = quiz or worked; Mistake Fix =
compare; Exam Rescue = chain/list. One CTA only.

## Accuracy (non-negotiable)
- Follow the plan's `note`. No guarantees: never "will come", "guaranteed", "+N marks", "90% of questions", fixed grace
  marks, or percentages you cannot source. Phrase strategies as strategies.
- Exam rules/weightage: verify on official CBSE pages (cbse.gov.in, cbseacademic.nic.in) or a reliable report with a date;
  mention the source in the commit message.
- Every number in a worked example or quiz: compute it in Python. Quiz: exactly one correct option, plausible distractors,
  2026–27 syllabus only (deleted topics never appear).
- Kokoro reads text literally: write `say` the way it should sound ("CBSE Mock", "R equals V divided by I", "6 ohms").
  Put symbols only in card text and `cap`.

## Caption
Hook question + one-line value + destination line ending exactly with `link in bio (cbsemock.org.in/go)` (the poster
swaps in a tracked link on Facebook/Telegram) + 3–5 hashtags in `hashtags` (always `#CBSE2027 #BoardExam` + topic tags).

## Check before committing
1. `python3 generate_hack_reel.py <n> --out /tmp/p.jpg --preview <one time inside every beat>` (it prints beat start times;
   run it twice: first to learn the times, then with a point in every beat) and LOOK at each frame: nothing cut off,
   no text overflowing its card, quiz reveal correct, end card URL on one line.
2. Total length 16–24 s.
3. Re-read every fact against the plan note and your sources.
Commit only the spec: first line `campaign: reel #NN <topic> (<date>)`, blank line, sources if any, blank line,
`Co-Authored-By: Claude <noreply@anthropic.com>`. `git pull --no-rebase`, push (retry up to 4 times). The repo workflow
renders the video and sends the owner a private preview; it posts itself on its date.
