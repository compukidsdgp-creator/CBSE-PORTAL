"""WHY? — Why is debugging important, and how does it actually work?  (Class 11/12 Computer Science)"""
import numpy as np
from matplotlib.patches import Ellipse, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY
from why_reels._codebox import code

TITLE = "Why is DEBUGGING so important?"
TAGS = "Computer Science"
BEATS = [
    ("hook",   "In nineteen forty seven, engineers found a real moth stuck inside a computer. "
               "They taped it in their logbook as the first actual bug found!",
               "1947: engineers found a real MOTH stuck in a computer — 'first actual case of bug being found'!", 5.8),
    ("types",  "Today's bugs are mistakes in code. Three kinds. Syntax errors, runtime errors, and logical errors.",
               "Today's bugs: 3 kinds — SYNTAX, RUNTIME and LOGICAL errors.", 5.0),
    ("logic",  "Logical errors are the sneakiest. The program runs, but gives the wrong answer. "
               "Average of eighty and ninety shows one twenty five!",
               "LOGICAL errors are sneakiest: code runs but gives the WRONG answer — average of 80 & 90 = 125?!", 6.2),
    ("trace",  "Debugging means hunting step by step. Print the values, compare with what you expect, "
               "and find where they go wrong.",
               "DEBUG: go step by step — PRINT values, compare with what you EXPECT, find where it breaks.", 5.8),
    ("fix",    "Here, division happened before addition. Add brackets, run again. Eighty five. Fixed!",
               "Division happened BEFORE addition → add brackets → 85 ✓ Fixed!", 4.8),
    ("math",   "Reproduce, read, trace, fix, retest.",
               "Reproduce → Read → Trace → Fix → Retest", 3.6),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🐞 WHY? — Why is DEBUGGING so important, and how does it work?

1947: engineers found a real moth in a computer — "first actual case of bug being found" 🦋

3 kinds of errors:
❌ Syntax — breaks Python's grammar (missing colon)
💥 Runtime — crashes while running (divide by zero)
🤔 Logical — runs fine, wrong answer (the sneakiest!)

avg = a + b / 2   → 80 + 45 = 125 ❌
avg = (a + b) / 2 → 85 ✅

Debugging = Reproduce → Read → Trace (print values) → Fix → Retest 🔁

Errors & exceptions — Computer Science, Class 11 & 12. 💻

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Python #Debugging #ComputerScience #Class12CS #Coding #CBSE"""

BUGGY = ["a = 80", "b = 90", "avg = a + b / 2", "print(avg)"]
FIXED = ["a = 80", "b = 90", "avg = (a + b) / 2", "print(avg)"]


def moth(dax, x, y, a, s=1.0):
    for sx in (-1, 1):
        dax.add_patch(Ellipse((x + sx * 0.42 * s, y + 0.12 * s), 0.8 * s, 0.6 * s, angle=sx * 25, facecolor="#8a7a5c",
                              edgecolor=GOLD, lw=2, alpha=a, zorder=6))
    dax.add_patch(Ellipse((x, y), 0.18 * s, 0.75 * s, facecolor="#3b3020", edgecolor=GOLD, lw=2, alpha=a, zorder=7))
    for sx in (-1, 1):
        dax.plot([x, x + sx * 0.25 * s], [y + 0.35 * s, y + 0.62 * s], color=GOLD, lw=2, alpha=a, zorder=7)


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    ta = ease(c.phase("types", 0.0, 0.25))
    ha = ease(c.phase("hook", 0.05, 0.35)) * (1 - ta)
    if ha > 0.01:
        dax.add_patch(FancyBboxPatch((-2.4, -1.6), 4.8, 3.6, boxstyle="round,pad=0,rounding_size=0.12",
                                     facecolor="#efe6c8", edgecolor="#b8a874", lw=3, alpha=ha, zorder=4))
        for k in range(6):
            dax.plot([-2.1, 2.1], [1.4 - 0.5 * k, 1.4 - 0.5 * k], color="#b8a874", lw=1.5, alpha=ha * 0.7, zorder=5)
        dax.text(0, 1.65, "logbook · 9 Sep 1947", ha="center", fontsize=17, color="#5c4a1e", alpha=ha, zorder=6,
                 style="italic")
        moth(dax, 0, 0.3, ha * ease(c.phase("hook", 0.25, 0.5)), 1.4)
        dax.add_patch(FancyBboxPatch((-0.9, 0.0), 1.8, 0.35, boxstyle="square,pad=0", facecolor="#ffffff",
                                     edgecolor="none", alpha=ha * 0.45 * ease(c.phase("hook", 0.4, 0.6)), zorder=8))
        dax.text(0, -1.1, '"first actual case of bug being found"', ha="center", fontsize=15, color="#5c4a1e",
                 alpha=ha * ease(c.phase("hook", 0.5, 0.8)), zorder=6, style="italic")
    lg = ease(c.phase("logic", 0.0, 0.25))
    if ta > 0.01:
        t = ta * (1 - lg)
        items = (("SYNTAX", "if x > 5   ← missing :", PINK), ("RUNTIME", "10 / 0  → crash!", GOLD),
                 ("LOGICAL", "runs… wrong answer", PURPLE))
        for k, (n, ex, col) in enumerate(items):
            a = t * ease(c.phase("types", 0.15 + 0.2 * k, 0.35 + 0.2 * k))
            y = 1.6 - 1.4 * k
            dax.add_patch(FancyBboxPatch((-3.1, y - 0.55), 6.2, 1.1, boxstyle="round,pad=0,rounding_size=0.15",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=a, zorder=5))
            dax.text(-2.85, y, n, ha="left", va="center", fontsize=24, color=col, fontweight="bold", alpha=a, zorder=6)
            dax.text(-0.6, y, ex, ha="left", va="center", fontsize=17, color=WHITE, alpha=a, zorder=6,
                     family="DejaVu Sans Mono")
    if lg > 0.01:
        fx = ease(c.phase("fix", 0.1, 0.4))
        tr = ease(c.phase("trace", 0.1, 0.4))
        lines = FIXED if fx > 0.5 else BUGGY
        hl = 2 if c.at("trace") else None
        code(dax, -3.2, 2.45, lines, lg, hl=hl, hl_col=GREEN if fx > 0.5 else PINK, title="average.py")
        res = "85.0  ✓" if fx > 0.5 else "125.0  ✗"
        col = GREEN if fx > 0.5 else PINK
        dax.add_patch(FancyBboxPatch((-3.2, -0.95), 6.4, 0.85, boxstyle="round,pad=0,rounding_size=0.12",
                                     facecolor="#050b1a", edgecolor=col, lw=2.5, alpha=lg, zorder=5))
        dax.text(-3.0, -0.52, "output: " + res, ha="left", va="center", fontsize=22, color=col, alpha=lg, zorder=6,
                 family="DejaVu Sans Mono")
        if tr > 0 and fx < 0.5:
            outline(dax.text(0, -1.55, "b / 2 = 45  →  80 + 45 = 125", ha="center", fontsize=22, color=GOLD,
                             fontweight="bold", alpha=tr, zorder=8, family="DejaVu Sans Mono"))
            outline(dax.text(0, -2.1, "expected (80 + 90) / 2 = 85", ha="center", fontsize=22, color=CYAN,
                             fontweight="bold", alpha=ease(c.phase("trace", 0.5, 0.8)), zorder=8,
                             family="DejaVu Sans Mono"))
        if fx > 0.5:
            outline(dax.text(0, -1.7, "brackets → add first ✓", ha="center", fontsize=24, color=GREEN,
                             fontweight="bold", alpha=fx * (1 - ease(c.phase("end", 0.0, 0.2))), zorder=8))
    c.steps([("reproduce → read → trace", 0.0, WHITE),
             ("fix → retest", 0.3, GOLD)], ys=(0.345, 0.285))
