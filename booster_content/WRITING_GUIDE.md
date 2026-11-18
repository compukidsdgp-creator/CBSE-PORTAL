# Weekly Knowledge Booster — writing guide (for the scheduled writing run)

The model booster, approved by the owner, is `booster_content/2026-11-30/class10_science.py`.
Match its structure, depth, tone and accuracy exactly.

## What to write
1. Run `python3 booster_plan.py next`. It gives the coming Monday and, for each subject, either
   `written`, `complete` or `to_write` (with the file path, chapter numbers and titles).
2. **Revisions come first**: if `booster_content/approvals.json` has an entry with `"status": "changes"`,
   rewrite that booster following the owner's `note`, then remove nothing else. Commit message:
   `booster: revise Class <n> <Subject> — week of <d Mon>` and a line `Preview: <url>`.
3. Otherwise write at most **2** `to_write` boosters per night, in the order listed.
   Commit message: `booster: draft Class <n> <Subject> — week of <d Mon>` + `Preview: https://cbsemock.org.in/booster/<monday>/class-<n>-<subject>.html`.

## Contents of one booster (exact counts — `booster_check.py` enforces them)
| key | count | form |
|---|---|---|
| `ar` | 10 | `a`, `r`, `answer` (A/B/C/D, standard CBSE key), `why` |
| `case` | 4 case studies × 4 parts | `title`, `passage` (≥ 60 words, a real situation/experiment/data), `parts`: MCQ with 4 `options`, `answer` "(x) text", `why` |
| `hots` | 10 | `q`, `answer` — needs reasoning, not recall |
| `competency` | 10 | MCQ: `q`, 4 `options`, `answer` "(x) text", `why` — applying the idea to a real-life situation |
| `knowledge` | 10 | `q`, `answer` — one or two lines, definitions/equations/facts |

## Quality rules
- Strictly within the CBSE 2026–27 syllabus for that chapter (NCERT rationalised). Nothing from deleted portions.
- Every fact, equation, value and unit checked. Equations balanced; use Unicode sub/superscripts (H₂O, Fe³⁺, 10⁻³ m).
- Maths/Physics: every numerical answer worked to the final value with units; check arithmetic by running it in Python.
- A/R: mix the answers — at least three different letters, roughly 3–4 A, 2–3 B, 2 C, 1–2 D. The `why` says which statements are true and whether R explains A.
- MCQ distractors must be plausible (common misconceptions), never silly; exactly one correct option.
- Original wording. Don't copy NCERT exercise questions word for word; `booster_check.py` fails near-duplicates of the question bank and published papers.
- Indian context in case studies and competency questions (kitchen, farm, market, school lab, monsoon, cricket…).
- Plain, student-friendly English; short sentences.

## Before committing
```
python3 booster_check.py booster_content/<monday>/<file>.py   # must print 0 problem(s)
python3 booster_pages.py                                      # page renders
```
Commit only the booster file (`git add booster_content/<monday>/<file>.py`); the publish workflow builds the page.
Never touch `resources/physics-xii-new.html`, `resources/ai-x.html` or `resources/cs-xii.html`.
