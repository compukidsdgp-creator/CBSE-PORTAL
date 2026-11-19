# CBSEMock Virtual Lab Standard — LOCKED (19 Nov 2026)

**Applies to every lab in every subject:** Physics, Chemistry, Biology, Mathematics, Computer Science and AI/ML.
**Locked by the owner on 19 Nov 2026.** No lab may go live unless it meets every rule below.
**Reference lab (the gold standard):** `virtual-labs/physics/convex-lens-focal-length.html`.
Open it and copy its shell; only the experiment itself changes from lab to lab.

This standard replaces all earlier lab standards, including `computer-science/V7_LOCKED_STANDARD.md`.
Those V7 rules are kept here where they still fit: real interaction, reset and challenge, keyboard access, and no fake execution.

---

## 1. Page shell (copy from the reference lab)
1. `<!DOCTYPE html>`, `lang="en"`, a viewport meta tag, a title in the form `<Experiment> — Virtual Lab | CBSEMock`, a meta description of 140–160 characters, a canonical link, the favicon block and the GA tag `G-G9HPDB24Y7`.
2. A `LearningResource` JSON-LD block with `learningResourceType: ["Simulation","Lab"]`, educationalLevel, `teaches` and the CBSEMOCK provider.
3. `<meta name="cbse-lab-standard" content="2026-11">`. A draft also carries `<meta name="robots" content="noindex, nofollow">` and, as the first element inside `<body>`, the draft bar
   `<div class="lab-draft" style="background:#fff4d6;color:#6b4e00;padding:8px 14px;font:600 14px Inter,sans-serif;text-align:center">Draft preview — waiting for approval in the admin panel</div>`.
   The publish workflow removes both. Don't use the class `lab-draft` for anything else.
4. The same fonts (Crimson Pro, Inter, JetBrains Mono), the same `:root` colour tokens with dark-mode overrides, and the same card, button and table styles.
5. External scripts may come only from cdnjs.cloudflare.com, cdn.jsdelivr.net/npm or unpkg, with an exact pinned version. Everything else is inline in one HTML file. No images are fetched from other sites; all art is inline SVG.

## 2. Header: design B, "lab scene" (locked)
- **Dark lab background:** the `hv hv-b` header uses the radial navy-to-black gradient.
- **Left column:** breadcrumb (Home › Virtual Labs › Subject › Lab) → eyebrow line (`Experiment · <apparatus>`) → H1, whose first line is gold gradient text (`.g1`) and whose second line is white (`.g2`) → a 1–2 sentence hook → chips (class and practical name, ⏱ time) → a gold call-to-action button that jumps to `#lab`.
- **Right column:** an inline SVG scene of **this experiment's own real apparatus**, drawn and lit realistically, with a subtle animation that shows what happens (light, flow, bubbles, colour change, data moving). Label the main parts in small caps.
- **Below both columns:** the 4-step strip (`.hsteps`) naming this lab's actual stages, for example *Set up → Take readings → Graph/analyse → Result & viva*.
- Respect `prefers-reduced-motion`. On phones the scene stacks under the text.

## 3. The lab environment (`<section class="lab" id="lab">`)
- **Step tabs** for the stages of the experiment, and a **task line** telling the student exactly what to do now.
- **A realistic working environment native to the concept** (see §6), not a slider-and-numbers toy. Apparatus can be dragged, and keyboard and fine-adjust buttons do the same job (±small and ±large steps, arrow keys). Touch works: the bench can scroll sideways on phones.
- **Real models only.** Outputs come from the actual law, equation, algorithm or chemistry, with realistic imperfections where the real lab has them (blur and depth of focus, meniscus, reaction time, noise, depth of field). Never fake a result.
- **The student does the measuring.** They read the instrument themselves: a zoomed scale, a burette meniscus, a stopwatch, a microscope field, program output. They then type the readings in. A "Show readings (helper)" switch exists, off by default.
- **Hidden unknown per session** where it makes sense (unknown focal length, unknown concentration, unknown resistor, unknown specimen), so answers can't be copied. "New sample" resets it.
- **Progress is saved** per viewer in `localStorage`, with every read and write wrapped in try/catch so the page still works without it.

### 3a. Mobile-first (every lab is used mostly on phones)
- **Phone widths:** the page works fully at 360 px and 390 px wide. The page itself never scrolls sideways. A wide apparatus (bench, circuit board, long table) sits in its own horizontal scroller (`overflow-x:auto`) with a "⟷ swipe" hint. The selected part scrolls into view automatically.
- **Tap targets:** every control is at least 40 × 40 px: buttons, chips, inputs, sliders, switches, and SVG hotspots such as terminals and knobs. Draw an invisible larger hit circle or rectangle around small SVG parts. Checkboxes are at least 22 px and sit inside a clickable label.
- **Text:** nothing is smaller than 12 px on a phone, including table headers, badges, pills and captions. Inputs use a 16 px font so iOS does not zoom in.
- **Layout:** panels stack in one column under 820 px. Zoomed views (scale magnifier, meter face, microscope field) stay big enough to read at 390 px. Nothing important hides behind the share buttons or a sticky bar.
- **Interaction:** no hover-only interactions. Dragging uses pointer events with `touch-action:none` on the draggable part only, so the page still scrolls, and every drag has a button or keyboard alternative.

## 4. Record, check, analyse
1. **Observation table** in the format of the CBSE practical file, with derived columns calculated live.
2. **"Check my table":** flags each misread value and any reading taken in the wrong condition (image not sharp, endpoint overshot, wrong focus), with a clear reason.
3. **Graph(s)** on canvas where the practical needs them, with the best-fit line or curve, the key construction marked (intercepts, slope, intersection) and the value read from it.
4. **Result card:** values from the table and from the graph. "Reveal actual value" and the percentage error are unlocked only after enough correct readings.

## 5. Teaching content (all required)
- Aim, Apparatus/materials, Theory with key equations, Procedure (numbered), Precautions, and Sources of error (or Limitations, for CS/AI/Maths).
- **Viva voce:** at least 8 questions with reveal answers, written the way examiners ask them.
- **"Keep going" links** to the matching chapter notes, quiz and mock papers, wherever those files exist.
- **Printable practical record** (`#record`, print CSS): the student's name/class/date lines, aim, apparatus, theory, their own table, their own graphs, result, precautions, sources of error and a teacher's signature line.
- All writing is CBSE 2026–27 syllabus-accurate, original and in plain student English, with Indian context where examples are needed.

## 6. What "realistic environment" means in each subject
| Subject | Environment | The student does |
|---|---|---|
| Physics | Optical or metre bench, circuit board with real-looking meters (needle with parallax), pendulum with a stopwatch, calorimeter, travelling microscope | Adjust the apparatus, read scales and meters, time oscillations |
| Chemistry | Lab bench with glassware: burette with meniscus, pipette, conical flask, test-tube rack, Bunsen burner, pH paper with a colour chart, gas jar | Add reagent drop by drop, watch colour or precipitate or effervescence develop over real time, read the burette, compare with the chart |
| Biology | Compound microscope (coarse and fine focus, 10×/40×, stage clips, light), slide preparation steps, dissection tray, potometer, quadrat field | Prepare and stain a slide, focus, count and identify, measure with an eyepiece scale, record drawings and labels |
| Mathematics | Graph paper, geometry box (ruler, protractor, compass), paper cutting/folding, clinometer, dice and coins | Construct and measure, verify the result, tabulate, compare with the formula |
| Computer Science | Editor + console with **real execution** of the student's code (Pyodide for Python, sql.js for SQL, both pinned from cdnjs or jsdelivr), and a memory/stack/file-pointer view that follows the run line by line | Write or complete code, run it, trace it, fix errors, match the expected output; record the output in a practical-file table |
| AI / ML | A real dataset in the page, a model actually trained in the browser (k-NN, decision tree, linear regression, a small neural net in plain JS), charts and a confusion matrix | Clean data, choose features, split train/test, train, evaluate, tune, and explain the result |

**CS/AI honesty rule (from V7):** never show code "running" unless it really runs in the page. If something can't really run, say plainly that it's a simulation.

**Retained CS reference features:** the Lab 07 logic-gate builder (gate palette, binary inputs, live output, truth table), the Lab 25 loop pattern studio (editable bounds, iteration trace) and the Lab 33 list memory studio (append/insert/update/delete/sort/reverse/search) must stay when those labs are rebuilt.

## 7. Quality gates (checked before a lab can be approved)
- `python3 lab_check.py <file>` prints 0 problems. It checks the structure in §1–§5.
- `node tools/lab_mobile_audit.js http://127.0.0.1:8765 audit.json <file>` reports `doc: 0`, no overflowing elements, no text under 12 px and no tap target under 32 px at both 360 and 390 px. The only exceptions are non-interactive labels and checkboxes inside a clickable label.
- Playwright: no console errors; the whole flow is done once (set up → readings → check → graph → result) with a correct answer.
- A screenshot of the header, the environment and the graphs, looked at on both desktop and phone.
- A subject check of every number, equation, reaction, label and code output.

## 8. Workflow
- **Same address:** a rebuilt lab keeps its file name, so links and the subject index stay valid. The draft is built at `virtual-labs/<subject>/_drafts/<file>` (noindex). When the owner approves it in Admin → Content tracker → Virtual labs, the publish workflow moves it into place, removes noindex and the draft bar, and refreshes the sitemap.
- **Speed:** three separate nightly runs (01:23, 03:11, 04:53 IST), one lab each. A run claims its lab first (`python3 lab_registry.py claim <id>`, pushed straight away), so two runs never build the same lab.
- **Older labs:** until a lab is rebuilt, `tools/lab_mobile.py` keeps the LAB-MOBILE layer on it (bigger tap targets, compact share buttons, text lifted to 12 px on phones).
- **Order:** board-practical experiments first (`labs_content/queue.json`), then the rest.
- **Locked pages:** the owner's locked pages are never touched: `resources/physics-xii-new.html`, `resources/ai-x.html`, `resources/cs-xii.html`. Each lab that has been approved and published is locked from then on, and changes only on the owner's request.
