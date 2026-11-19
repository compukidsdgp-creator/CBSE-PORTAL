# Mock Zone rewrite — 15 genuinely different practice papers per subject

**Goal (owner, 19 Nov 2026):** the 15 practice papers on each Mock Zone subject page must not repeat questions;
at most a very few repeats. These pages get a lot of search traffic.

**In scope:** the 17 pages listed in `PRIORITY` in `mockzone_build.py`, worked in that order.
**Out of scope:** `cbse-class-10-ai-mock-papers.html` and `cbse-class-12-computer-science-mock-papers.html` (owner's decision),
and the frozen/locked files `resources/physics-xii-new.html`, `resources/ai-x.html`, `resources/cs-xii.html`.

## How it works
- A converted page keeps its layout and render code. Its pools live in `mockzone_bank/<page-stem>.json`
  (`{"page", "pools": {POOL: {"per_paper": k, "items": [...]}}}`) and `mockzone_build.py build` injects them between
  `/* MZ-POOLS:START */` and `/* MZ-POOLS:END */`.
- `buildPaper(n)` takes `mzPick(POOL, MZ_K.POOL, n)` = items `[n·k, (n+1)·k)`. So **items are written paper by paper**:
  to add Paper 2 you append exactly `k` new items to EVERY pool, in order. A pool with 15·k items = zero repeats.
- Reference page (already converted): `cbse-class-12-physics-mock-papers.html`.

## Converting a page (`action: convert`)
1. Read the page's script: which arrays are pools, how `buildPaper(n)` (or the page's equivalent) picks from them,
   and how many items one paper uses from each pool (= `k`).
2. If the pools are not next to each other, move them together first (no other code between them).
3. `python3 mockzone_build.py init <page> POOL:k POOL:k ...` (copies the pools into the bank and adds the markers).
4. Rewrite the page's paper builder so every pool is picked with `mzPick(POOL, MZ_K.POOL, n)`, keeping whatever the render
   code expects (same keys/shape). Pages that pick by `n % 3` or similar: same idea, one block per paper.
   If a pool currently holds more than one paper's worth, reorder its items so the first `k` form a sensible Paper 1, etc.
5. Verify (below) that Paper 1 renders exactly the same questions as before the conversion and there are no console errors.
6. Commit the conversion on its own: `mockzone: convert <page>`. Then continue writing papers for that page.

## Writing papers (`action: write`)
Each run writes **2 complete papers** (the next two paper numbers from `python3 mockzone_build.py next`).
A paper is complete only when every pool got its `k` new items. Never commit half a paper.

### Standard (non-negotiable)
- CBSE 2026–27 rationalised syllabus and the current board blueprint for that subject: same sections, marks, question types
  (MCQ, assertion–reason, VSA, SA, case-based, LA with internal OR) as Paper 1 of the page. Deleted topics never appear
  (e.g. Physics XII: communication systems, LED/photodiode/solar cell/Zener; Chemistry XII: solid state, surface chemistry,
  p-block, metallurgy, polymers, everyday chemistry; Biology XII: reproduction in organisms, food production, environmental
  issues; Maths X: frustum, conversion of solids). If unsure, check the official CBSE syllabus PDF on the web.
- **Each paper is a balanced full paper**: chapters spread by the CBSE unit weightage, not clustered; difficulty about
  30 % easy / 50 % moderate / 20 % hard; at least two competency/real-life (Indian context) questions.
- **Original** wording. Do not copy CBSE sample papers, PYQs, textbooks or websites. Do not reuse questions from
  `question-bank/` (those are the separate Mon/Wed/Fri PDF papers).
- **No repeats**, not even reworded: `mockzone_build.py check` rejects exact and near-duplicates across the whole bank;
  also avoid asking the same concept the same way as an earlier paper (vary the concept, data, context).
- Every answer correct and complete, with marking points for 2/3/4/5-mark answers. Compute every numerical in Python and give
  units. MCQs: exactly one correct option, plausible distractors, mix the answer letters across the paper.
  Assertion–reason: use the page's existing option wording.
- Same object fields as the existing items of that pool (look at item 0); keep `\n` line breaks the same way.
- Hindi / Bengali pages: correct, natural standard Hindi/Bengali in the right script, board-style.
- If you find an error in an existing item while working, fix it in the bank (mention it in the commit message).

## Verify before committing
1. `python3 mockzone_build.py check <page>` → OK (0 errors).
2. `python3 mockzone_build.py build <page>`.
3. `node tools/mock_overlap_audit.js /tmp/mz.json && python3 tools/mock_overlap_report.py /tmp/mz.json` — for your page the
   unique count must have grown by exactly the questions you added; the new papers share no question with any other paper.
4. Playwright (`require('playwright')`): open the page at 1280 px and devices['Pixel 5']; no console errors; click the tabs of
   the papers you wrote; every question and every "Show Answer" renders; no horizontal scroll on the phone.
5. Re-read every answer once more.

## Commit and push
Stage only `mockzone_bank/<page-stem>.json` and the page (plus `mockzone_build.py`/guide only if you fixed them).
Commit first line `mockzone: <Subject> papers <a>–<b> (<fresh>/15 fresh)`, blank line,
`Co-Authored-By: Claude <noreply@anthropic.com>`. `git pull --no-rebase`; if the bank changed upstream, re-run check + build;
then push (retry up to 4 times).
