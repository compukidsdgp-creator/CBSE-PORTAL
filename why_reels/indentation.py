"""WHY? — Why is indentation so important in Python?  (Class 11/12 Computer Science · Python)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY
from why_reels._codebox import code

TITLE = "Why is INDENTATION so important in Python?"
TAGS = "Computer Science"
BEATS = [
    ("hook",   "In most languages, spaces at the start of a line are just decoration. In Python, they change what your program does!",
               "In most languages, leading spaces are decoration. In PYTHON they change what your code DOES!", 5.4),
    ("braces", "Languages like C and Java mark a block of code with curly brackets.",
               "C and Java mark a block with { curly brackets }.", 3.6),
    ("python", "Python has no brackets. The indentation itself tells Python which lines belong inside the if, the loop, or the function.",
               "Python has NO brackets: the INDENTATION itself says which lines are inside the if / loop / function.", 6.0),
    ("same",   "Look. Same three lines. Indent the last print, and it runs only when you pass.",
               "Same 3 lines: INDENT the last print → it runs only when you pass.", 4.4),
    ("diff",   "Un indent it, and it runs every time. One tab changes the logic!",
               "UN-indent it → it runs EVERY time. One tab changes the logic!", 4.0),
    ("error",  "And if the spaces don't line up, Python stops with an Indentation Error.",
               "Spaces don't line up? Python stops with an IndentationError.", 3.8),
    ("math",   "Use four spaces per level, and keep them consistent.",
               "Use 4 spaces per level — and keep them CONSISTENT.", 3.4),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """↹ WHY? — Why is INDENTATION so important in Python?

C / Java use { } to mark blocks.
Python has no brackets — the indentation IS the block! 🧱

if marks >= 33:
    print("Pass")
    print("Well done")   # inside → only when passing

if marks >= 33:
    print("Pass")
print("Well done")       # outside → runs every time

Misaligned spaces → IndentationError ❌
Rule: 4 spaces per level, always consistent ✅

Python basics — Computer Science, Class 11 & 12. 💻

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Python #Indentation #ComputerScience #Class12CS #Coding #CBSE"""

C_CODE = ["if (marks >= 33) {", '    printf("Pass");', "}"]
INSIDE = ["marks = 20", "if marks >= 33:", '    print("Pass")', '    print("Well done")']
OUTSIDE = ["marks = 20", "if marks >= 33:", '    print("Pass")', 'print("Well done")']
BAD = ["if marks >= 33:", '    print("Pass")', '  print("Well done")']


def out_box(dax, y, text, col, a):
    dax.add_patch(FancyBboxPatch((-3.2, y - 0.45), 6.4, 0.9, boxstyle="round,pad=0,rounding_size=0.12",
                                 facecolor="#050b1a", edgecolor=col, lw=2.5, alpha=a, zorder=5))
    dax.text(-3.0, y, "output: " + text, ha="left", va="center", fontsize=20, color=col, alpha=a, zorder=6,
             family="DejaVu Sans Mono")


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    sm = ease(c.phase("same", 0.0, 0.25))
    er = ease(c.phase("error", 0.0, 0.25))
    a0 = ease(c.phase("hook", 0.05, 0.35)) * (1 - sm)
    if a0 > 0.01:
        ca = max(ease(c.phase("hook", 0.45, 0.8)), ease(c.phase("braces", 0.0, 0.3))) * a0
        code(dax, -3.2, 2.45, C_CODE, ca, title="C / Java")
        if ca > 0:
            outline(dax.text(2.5, 1.35, "{ }", ha="center", va="center", fontsize=40, color=GOLD, fontweight="bold",
                             alpha=ca * (1 - ease(c.phase("python", 0.0, 0.3))), zorder=8))
        pa = ease(c.phase("python", 0.1, 0.4)) * a0
        code(dax, -3.2, 0.15, INSIDE[1:3], pa, title="Python", hl=1, hl_col=CYAN)
        if pa > 0:
            outline(dax.text(-2.75, -2.0, "↦ 4 spaces = inside the if", ha="left", fontsize=22, color=CYAN,
                             fontweight="bold", alpha=pa, zorder=8))
    if sm > 0.01:
        b = sm * (1 - er)
        df = ease(c.phase("diff", 0.0, 0.3))
        lines = OUTSIDE if df > 0.5 else INSIDE
        code(dax, -3.2, 2.45, lines, b, title="result.py", hl=3, hl_col=GOLD if df < 0.5 else PINK)
        out_box(dax, -1.35, "(nothing)" if df < 0.5 else "Well done", GREEN if df < 0.5 else PINK, b)
        outline(dax.text(0, -2.3, "inside → only if passed" if df < 0.5 else "outside → runs EVERY time",
                         ha="center", fontsize=23, color=GREEN if df < 0.5 else PINK, fontweight="bold", alpha=b, zorder=8))
    if er > 0.01:
        e = er * (1 - ease(c.phase("math", 0.0, 0.3)))
        code(dax, -3.2, 2.45, BAD, e, title="oops.py", hl=2, hl_col=PINK)
        out_box(dax, -0.6, "IndentationError", PINK, e)
        ma = ease(c.phase("math", 0.0, 0.35))
    ma = ease(c.phase("math", 0.0, 0.35))
    if ma > 0.01:
        for k in range(3):
            y = 1.6 - 0.9 * k
            dax.add_patch(FancyBboxPatch((-2.6 + 0.9 * k, y - 0.3), 3.6, 0.6, boxstyle="round,pad=0,rounding_size=0.1",
                                         facecolor="#13264d", edgecolor=CYAN, lw=2, alpha=ma, zorder=5))
            dax.text(-2.4 + 0.9 * k, y, f"level {k}", ha="left", va="center", fontsize=19, color=CYAN, fontweight="bold",
                     alpha=ma, zorder=6)
        outline(dax.text(0, -1.3, "+4 spaces per level", ha="center", fontsize=28, color=GOLD, fontweight="bold",
                         alpha=ma, zorder=8))
    c.steps([("indentation = the block", 0.0, WHITE),
             ("4 spaces, always consistent", 0.3, GOLD)], ys=(0.345, 0.285))
