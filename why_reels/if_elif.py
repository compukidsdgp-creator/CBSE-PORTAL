"""WHY? — Why do we need elif instead of many separate ifs?  (Class 11/12 Computer Science · Python)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY
from why_reels._codebox import code

TITLE = "Why do we need ELIF, not just many IFs?"
TAGS = "Computer Science"
BEATS = [
    ("hook",   "Let's grade a student who scored ninety five. Using three separate if statements. Watch what happens.",
               "Grade a student who scored 95… using 3 separate IFs. Watch!", 4.2),
    ("ifs",    "Every if is checked on its own. Ninety five is at least ninety, so grade A. "
               "It's also at least seventy five, so grade B. And at least fifty, so grade C!",
               "Each IF is checked on its own: 95 ≥ 90 → A … 95 ≥ 75 → B … 95 ≥ 50 → C!", 6.6),
    ("bug",    "Three grades for one student. That's a bug.",
               "THREE grades for one student. That's a BUG!", 3.4),
    ("elif",   "With if, elif, else, Python checks from the top, and stops at the first condition that's true.",
               "With if / elif / else, Python checks from the TOP and STOPS at the first true one.", 5.2),
    ("fix",    "Ninety five matches the first check, gets an A, and the rest are skipped. One answer. Faster too.",
               "95 matches the first → A. The rest are SKIPPED. One answer — and faster.", 5.0),
    ("math",   "Use elif when only one choice should win.",
               "Use ELIF when only ONE choice should win.", 3.2),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🔀 WHY? — Why do we need ELIF instead of many separate IFs?

marks = 95
if marks >= 90: print("A")
if marks >= 75: print("B")
if marks >= 50: print("C")
➡️ prints A, B AND C 😱 (each if is checked separately)

if marks >= 90:   print("A")
elif marks >= 75: print("B")
elif marks >= 50: print("C")
else:             print("Fail")
➡️ prints only A ✅ — stops at the first true condition (and skips the rest)

Conditional statements — Computer Science, Class 11 & 12. 💻

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Python #IfElse #ComputerScience #Class12CS #Coding #CBSE"""

IFS = ["marks = 95", 'if marks >= 90: print("A")', 'if marks >= 75: print("B")', 'if marks >= 50: print("C")']
ELIF = ["marks = 95", 'if marks >= 90:   print("A")', 'elif marks >= 75: print("B")', 'elif marks >= 50: print("C")',
        'else:             print("Fail")']


def out(dax, y, s, col, a):
    dax.add_patch(FancyBboxPatch((-3.2, y - 0.45), 6.4, 0.9, boxstyle="round,pad=0,rounding_size=0.12",
                                 facecolor="#050b1a", edgecolor=col, lw=2.5, alpha=a, zorder=5))
    dax.text(-3.0, y, "output: " + s, ha="left", va="center", fontsize=22, color=col, alpha=a, zorder=6,
             family="DejaVu Sans Mono")


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    el = ease(c.phase("elif", 0.0, 0.25))
    a0 = ease(c.phase("hook", 0.1, 0.4)) * (1 - el)
    if a0 > 0.01:
        step = c.phase("ifs", 0.1, 0.9)
        k = int(step * 3) if c.at("ifs") else -1
        hl = 1 + min(k, 2) if 0 <= k else None
        code(dax, -3.2, 2.45, IFS, a0, hl=hl, hl_col=PINK, w=6.4, size=24)
        printed = "".join(g + " " for i, g in enumerate("ABC") if c.at("ifs") and step * 3 > i + 0.4)
        if c.at("bug"):
            printed = "A B C"
        out(dax, -0.5, printed or "…", PINK if c.at("bug") else WHITE, a0 * ease(c.phase("ifs", 0.0, 0.2)))
        ba = ease(c.phase("bug", 0.1, 0.4)) * (1 - el)
        if ba > 0:
            outline(dax.text(0, -1.65, "3 grades for 1 student ✗", ha="center", fontsize=26, color=PINK,
                             fontweight="bold", alpha=ba, zorder=8))
    if el > 0.01:
        e = el
        fx = ease(c.phase("fix", 0.1, 0.4))
        hl = 1 if c.at("fix") else None
        code(dax, -3.2, 2.45, ELIF, e, hl=hl, hl_col=GREEN, w=6.4, size=24)
        if fx > 0:
            for k in range(3):
                y = 2.45 - 0.32 - (2 + k) * 0.5
                dax.plot([-3.0, 3.0], [y, y], color=GREY, lw=2.5, alpha=fx * 0.9, zorder=7)
        out(dax, -1.0, "A" if fx > 0.3 else "…", GREEN if fx > 0.3 else WHITE, e * ease(c.phase("elif", 0.4, 0.7)))
        sa = ease(c.phase("elif", 0.3, 0.6)) * (1 - fx)
        if sa > 0:
            outline(dax.text(0, -2.05, "top → down, STOP at first true", ha="center", fontsize=23, color=CYAN,
                             fontweight="bold", alpha=sa, zorder=8))
        if fx > 0:
            outline(dax.text(0, -2.05, "one answer ✓", ha="center", fontsize=26, color=GREEN,
                             fontweight="bold", alpha=fx * (1 - ease(c.phase("end", 0.0, 0.2))), zorder=8))
    c.steps([("separate ifs: ALL true ones run", 0.0, WHITE),
             ("elif: only the FIRST true one", 0.3, GOLD)], ys=(0.345, 0.285))
