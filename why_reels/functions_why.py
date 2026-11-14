"""WHY? — Why do we need functions instead of repeating code?  (Class 11/12 Computer Science · Python)"""
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY
from why_reels._codebox import code

TITLE = "Why write FUNCTIONS instead of repeating code?"
TAGS = "Computer Science"
BEATS = [
    ("hook",   "You need the area of three rectangles. So you copy and paste the same code three times. What could go wrong?",
               "Need 3 rectangle areas… so you copy-paste the same code 3 times. What could go wrong?", 5.2),
    ("bug",    "Find a bug, and you must fix it in three places. Miss one, and your program is wrong.",
               "Find a BUG → fix it in 3 places. Miss one → your program is wrong.", 4.4),
    ("define", "Instead, write it once, as a function, using def. Then call it whenever you need it.",
               "Instead: write it ONCE as a function with def… then CALL it whenever you need.", 4.8),
    ("params", "Parameters are the inputs. Each call can send different values, like length and breadth.",
               "PARAMETERS are the inputs — each call sends different values (l, b).", 4.6),
    ("ret",    "Return sends the answer back, so you can store it, print it, or use it in another calculation.",
               "RETURN sends the answer back — store it, print it, or use it again.", 4.6),
    ("math",   "Write once, use many times. Fix once, fixed everywhere.",
               "Write once, use many times. Fix once, fixed EVERYWHERE.", 3.6),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧩 WHY? — Why use FUNCTIONS instead of repeating code?

Copy-paste the same code 3 times… find a bug → fix it in 3 places 😩

def area(l, b):      # parameters = inputs
    return l * b     # return = sends answer back

a1 = area(4, 3)
a2 = area(5, 2)

✅ Write once, use many times
✅ Fix once, fixed everywhere
✅ Shorter, cleaner, easier to test

Functions in Python — Computer Science, Class 11 & 12. 💻

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Python #Functions #ComputerScience #Class12CS #Coding #CBSE"""

REPEAT = ["l = 4; b = 3", "print(l * b)", "l = 5; b = 2", "print(l * b)", "l = 6; b = 7", "print(l * b)"]
FUNC = ["def area(l, b):", "    return l * b", "", "a1 = area(4, 3)", "a2 = area(5, 2)", "print(a1 + a2)"]


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    df = ease(c.phase("define", 0.0, 0.3))
    a0 = ease(c.phase("hook", 0.05, 0.35)) * (1 - df)
    if a0 > 0.01:
        shown = 2 + 4 * ease(c.phase("hook", 0.3, 0.8))
        code(dax, -3.2, 2.45, REPEAT, a0, show=shown, title="copy-paste.py")
        ba = ease(c.phase("bug", 0.1, 0.4)) * (1 - df)
        if ba > 0:
            for k in range(3):
                y = 2.45 - 0.32 - 0.35 - (2 * k + 1) * 0.42
                dax.text(2.9, y, "✗", ha="center", va="center", fontsize=26, color=PINK, fontweight="bold",
                         alpha=ba * ease(c.phase("bug", 0.15 + 0.15 * k, 0.3 + 0.15 * k)), zorder=8)
            outline(dax.text(0, -1.9, "fix the bug 3 times?!", ha="center", fontsize=26, color=PINK, fontweight="bold",
                             alpha=ba, zorder=8))
    if df > 0.01:
        hl = None
        if c.at("params"):
            hl = 0
        if c.at("ret"):
            hl = 1
        code(dax, -3.2, 2.45, FUNC, df, show=1 + 5 * ease(c.phase("define", 0.2, 0.8)), hl=hl,
             title="functions.py")
        pa = ease(c.phase("params", 0.15, 0.45)) * (1 - ease(c.phase("ret", 0.0, 0.2)))
        if pa > 0:
            outline(dax.text(0.3, -1.75, "(l, b) = inputs", ha="center", fontsize=26, color=CYAN, fontweight="bold",
                             alpha=pa, zorder=8))
            outline(dax.text(0.3, -2.25, "area(4, 3) → l=4, b=3", ha="center", fontsize=21, color=LTGREY,
                             fontweight="bold", alpha=pa, zorder=8, family="DejaVu Sans Mono"))
        ra = ease(c.phase("ret", 0.15, 0.45)) * (1 - ease(c.phase("math", 0.0, 0.3)))
        if ra > 0:
            outline(dax.text(0.3, -1.75, "return → 12 comes back", ha="center", fontsize=26, color=GREEN,
                             fontweight="bold", alpha=ra, zorder=8))
            outline(dax.text(0.3, -2.25, "a1 = 12,  a2 = 10", ha="center", fontsize=21, color=LTGREY,
                             fontweight="bold", alpha=ra, zorder=8, family="DejaVu Sans Mono"))
        ma = ease(c.phase("math", 0.1, 0.4))
        if ma > 0:
            outline(dax.text(0.3, -1.9, "1 definition · many calls", ha="center", fontsize=26, color=GOLD,
                             fontweight="bold", alpha=ma, zorder=8))
    c.steps([("write once, use many times", 0.0, WHITE),
             ("fix once, fixed everywhere", 0.3, GOLD)], ys=(0.345, 0.285))
