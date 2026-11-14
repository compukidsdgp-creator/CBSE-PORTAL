"""WHY? — Why do we need data types (int, float, string, boolean)?  (Class 11/12 Computer Science · Python)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY
from why_reels._codebox import code

TITLE = "Why do we need DATA TYPES?"
TAGS = "Computer Science"
BEATS = [
    ("hook",   "Five plus five is ten. But in Python, quote five, plus quote five, gives fifty five! Why?",
               "5 + 5 = 10… but \"5\" + \"5\" = \"55\"?! Why?", 4.2),
    ("bits",   "Inside the computer, everything is just zeros and ones. The data type tells it what those bits mean.",
               "Inside, everything is 0s and 1s. The DATA TYPE tells the computer what they MEAN.", 5.2),
    ("four",   "Int for whole numbers. Float for decimals. String for text. And boolean for true or false.",
               "int: whole numbers · float: decimals · str: text · bool: True / False", 5.0),
    ("ops",    "The type decides what an operation does. Plus adds numbers, but joins strings. "
               "And a number plus a string? Type error!",
               "Type decides the operation: + ADDS numbers, JOINS strings… number + string → TypeError!", 6.0),
    ("input",  "That's why input always gives a string. To do maths, convert it with int.",
               "input() always gives a STRING → convert with int(input()) to do maths.", 4.6),
    ("math",   "Same bits, different type, different meaning.",
               "Same bits + different type = different meaning.", 3.4),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🔢 WHY? — Why do we need DATA TYPES?

5 + 5 = 10 ✅
"5" + "5" = "55" 😲

Inside, everything is 0s and 1s — the data type says what they MEAN.

int → whole numbers (17)
float → decimals (3.14)
str → text ("Hello")
bool → True / False

+ adds numbers, joins strings, and 5 + "5" → TypeError ❌
input() gives a string → use int(input()) for maths ✅

Data types in Python — Computer Science, Class 11 & 12. 💻

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Python #DataTypes #ComputerScience #Class12CS #Coding #CBSE"""


def chip(dax, x, y, w, h, top, sub, col, a, size=30):
    if a <= 0.01:
        return
    dax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.15",
                                 facecolor="#13264d", edgecolor=col, lw=3, alpha=a, zorder=5))
    dax.text(x, y + 0.18, top, ha="center", va="center", fontsize=size, color=col, fontweight="bold", alpha=a, zorder=6,
             family="DejaVu Sans Mono")
    dax.text(x, y - 0.35, sub, ha="center", va="center", fontsize=17, color=LTGREY, fontweight="bold", alpha=a, zorder=6)


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    bi = ease(c.phase("bits", 0.0, 0.25))
    ha = ease(c.phase("hook", 0.05, 0.3)) * (1 - bi)
    if ha > 0.01:
        outline(dax.text(0, 1.2, "5 + 5  =  10", ha="center", va="center", fontsize=40, color=GREEN, fontweight="bold",
                         alpha=ha, zorder=7, family="DejaVu Sans Mono"))
        outline(dax.text(0, -0.4, '"5" + "5" = "55"', ha="center", va="center", fontsize=40, color=PINK,
                         fontweight="bold", alpha=ha * ease(c.phase("hook", 0.35, 0.6)), zorder=7,
                         family="DejaVu Sans Mono"))
    fo = ease(c.phase("four", 0.0, 0.25))
    if bi > 0.01:
        b = bi * (1 - fo)
        outline(dax.text(0, 1.6, "01000001", ha="center", va="center", fontsize=44, color=WHITE, fontweight="bold",
                         alpha=b, zorder=7, family="DejaVu Sans Mono"))
        ma = ease(c.phase("bits", 0.4, 0.8)) * b
        for k, (s, sub, col) in enumerate((("65", "as int", CYAN), ('"A"', "as str", GOLD))):
            chip(dax, -1.5 + 3.0 * k, -0.4, 2.6, 1.5, s, sub, col, ma)
    op = ease(c.phase("ops", 0.0, 0.25))
    if fo > 0.01:
        f = fo * (1 - op)
        items = (("17", "int", CYAN), ("3.14", "float", GREEN), ('"Hi"', "str", GOLD), ("True", "bool", PINK))
        for k, (s, sub, col) in enumerate(items):
            a = f * ease(c.phase("four", 0.1 + 0.18 * k, 0.3 + 0.18 * k))
            chip(dax, -1.6 + 3.2 * (k % 2), 1.15 - 2.0 * (k // 2), 2.8, 1.6, s, sub, col, a)
    inp = ease(c.phase("input", 0.0, 0.25))
    if op > 0.01:
        o = op * (1 - inp)
        rows = (("5 + 5", "10", GREEN), ('"5" + "5"', '"55"', GOLD), ('5 + "5"', "TypeError", PINK))
        for k, (e, r, col) in enumerate(rows):
            a = o * ease(c.phase("ops", 0.1 + 0.25 * k, 0.3 + 0.25 * k))
            y = 1.6 - 1.3 * k
            dax.add_patch(FancyBboxPatch((-3.1, y - 0.5), 6.2, 1.0, boxstyle="round,pad=0,rounding_size=0.15",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=a, zorder=5))
            dax.text(-2.85, y, e, ha="left", va="center", fontsize=24, color=WHITE, alpha=a, zorder=6,
                     family="DejaVu Sans Mono")
            dax.text(2.85, y, "→ " + r, ha="right", va="center", fontsize=24, color=col, fontweight="bold", alpha=a,
                     zorder=6, family="DejaVu Sans Mono")
    if inp > 0.01:
        i = inp * (1 - ease(c.phase("math", 0.0, 0.3)))
        conv = ease(c.phase("input", 0.4, 0.7))
        lines = ['age = input("Age? ")', "print(age + 1)"] if conv < 0.5 else ['age = int(input("Age? "))', "print(age + 1)"]
        code(dax, -3.2, 2.2, lines, i, hl=0, hl_col=PINK if conv < 0.5 else GREEN)
        res = "TypeError ✗" if conv < 0.5 else "17  ✓"
        outline(dax.text(0, -0.55, "output: " + res, ha="center", fontsize=26, color=PINK if conv < 0.5 else GREEN,
                         fontweight="bold", alpha=i, zorder=8, family="DejaVu Sans Mono"))
    mm = ease(c.phase("math", 0.0, 0.35))
    if mm > 0.01:
        chip(dax, -1.5, 0.4, 2.6, 1.5, "65", "int", CYAN, mm)
        chip(dax, 1.5, 0.4, 2.6, 1.5, '"A"', "str", GOLD, mm)
        outline(dax.text(0, 1.75, "01000001", ha="center", fontsize=30, color=WHITE, fontweight="bold", alpha=mm,
                         zorder=7, family="DejaVu Sans Mono"))
    c.steps([("same bits + different type", 0.0, WHITE),
             ("= different meaning", 0.3, GOLD)], ys=(0.345, 0.285))
