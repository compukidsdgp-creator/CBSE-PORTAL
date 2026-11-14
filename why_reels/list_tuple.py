"""WHY? — Why can a LIST change but a TUPLE can't?  (Class 12 Computer Science · Python)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why can a LIST change but not a TUPLE?"
TAGS = "Class 12 Computer Science"
BEATS = [
    ("hook",  "In Python, why can you change a list, but not a tuple?",
              "In Python, why can you change a LIST but not a TUPLE?", 3.6),
    ("list",  "A list is like a whiteboard. Rub out an item, and write a new one.",
              "A list is like a whiteboard: rub out an item and write a new one.", 4.6),
    ("tuple", "A tuple is like a printed certificate. Once it's made, it cannot be edited. Python raises a type error.",
              "A tuple is like a printed certificate — once made, it can't be edited. TypeError!", 5.6),
    ("why",   "Lists are mutable, built to grow and change. Tuples are immutable, fixed the moment they're created.",
              "Lists are MUTABLE (built to change). Tuples are IMMUTABLE (fixed once created).", 5.6),
    ("use",   "So use tuples for data that must never change, like a date of birth, or map coordinates. "
              "They're also a little faster, and safer.",
              "Use tuples for data that must never change — date of birth, coordinates. Faster & safer!", 6.0),
    ("math",  "Square brackets make a list. Round brackets make a tuple.",
              "[ ] → list (mutable)   ( ) → tuple (immutable)", 3.8),
    ("end",   "Follow C B S E Mock for more why videos.",
              "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🐍 WHY? — Why can a LIST change but a TUPLE can't?

LIST = whiteboard 🧽 → marks[1] = 95 ✅ (mutable)
TUPLE = printed certificate 📜 → t[1] = 95 ❌ TypeError (immutable)

Use tuples for data that must never change — date of birth, map coordinates.
They're a little faster and safer too!
[ ] → list · ( ) → tuple

CS Class 12 Python — a guaranteed viva question. 🧠

💾 Save it · 📤 Share with your CS batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Python #ComputerScience #CSClass12 #Coding #PythonTips #CBSE"""

MONO = "DejaVu Sans Mono"


def cells(dax, x, y, vals, col, a, hl=None, hl_col=GOLD, cw=1.15):
    for k, v in enumerate(vals):
        face = "#3b2a00" if hl == k else "#13264d"
        dax.add_patch(FancyBboxPatch((x + k * (cw + 0.1), y - 0.42), cw, 0.84, boxstyle="round,pad=0,rounding_size=0.12",
                                     facecolor=face, edgecolor=hl_col if hl == k else col, lw=3, alpha=a, zorder=5))
        dax.text(x + k * (cw + 0.1) + cw / 2, y, str(v), ha="center", va="center", fontsize=30, fontweight="bold",
                 color=WHITE, alpha=a, zorder=6)
        dax.text(x + k * (cw + 0.1) + cw / 2, y - 0.7, f"[{k}]", ha="center", va="center", fontsize=18, color=LTGREY,
                 alpha=a, zorder=6, family=MONO)


def code(dax, x, y, s, col, a, size=26):
    dax.text(x, y, s, ha="left", va="center", fontsize=size, fontweight="bold", color=col, family=MONO, alpha=a, zorder=7)


def draw(c):
    dax = c.area(0.0, 0.0, 7.6)
    # LIST
    la = ease(c.phase("list", 0.0, 0.25))
    fade_top = 1 - ease(c.phase("use", 0.0, 0.2))
    if la > 0 and fade_top > 0:
        a = la * fade_top
        changed = c.phase("list", 0.55, 0.75) > 0
        code(dax, -3.5, 2.55, "marks = [90, 85, 72]", CYAN, a)
        cells(dax, -2.75, 1.55, [90, 95 if changed else 85, 72], CYAN, a, hl=1 if c.phase("list", 0.4, 0.5) > 0 else None,
              hl_col=GREEN if changed else GOLD)
        ca = ease(c.phase("list", 0.35, 0.55)) * fade_top
        code(dax, 1.25, 1.55, "marks[1] = 95", WHITE, ca, size=22)
        if changed:
            outline(dax.text(1.25, 1.0, "✓ changed!", ha="left", fontsize=26, fontweight="bold", color=GREEN,
                             alpha=ease(c.phase("list", 0.75, 0.9)) * fade_top, zorder=8))
    # TUPLE
    ta = ease(c.phase("tuple", 0.0, 0.25))
    if ta > 0 and fade_top > 0:
        a = ta * fade_top
        code(dax, -3.5, 0.15, "t = (90, 85, 72)", GOLD, a)
        cells(dax, -2.75, -0.85, [90, 85, 72], GOLD, a, hl=1 if c.phase("tuple", 0.35, 0.45) > 0 else None, hl_col=PINK)
        ca = ease(c.phase("tuple", 0.3, 0.5)) * fade_top
        code(dax, 1.25, -0.85, "t[1] = 95", WHITE, ca, size=22)
        ea = back_out(c.phase("tuple", 0.55, 0.75))
        if ea > 0.01:
            dax.add_patch(FancyBboxPatch((-3.55, -2.65), 7.1, 0.85, boxstyle="round,pad=0,rounding_size=0.15",
                                         facecolor="#2a0716", edgecolor=PINK, lw=3, alpha=min(1, ea) * fade_top, zorder=8))
            dax.text(0, -2.22, "TypeError: 'tuple' object does not\nsupport item assignment", ha="center", va="center",
                     fontsize=19, fontweight="bold", color=PINK, family=MONO, alpha=min(1, ea) * fade_top, zorder=9)
    # mutable / immutable labels
    wa = ease(c.phase("why", 0.1, 0.4)) * fade_top
    if wa > 0:
        outline(dax.text(3.6, 2.55, "MUTABLE", ha="right", fontsize=26, fontweight="bold", color=GREEN, alpha=wa, zorder=8))
        outline(dax.text(3.6, 0.15, "IMMUTABLE 🔒" if False else "IMMUTABLE (locked)", ha="right", fontsize=24,
                         fontweight="bold", color=PINK, alpha=ease(c.phase("why", 0.45, 0.75)) * fade_top, zorder=8))
    # uses for tuples
    if c.at("use"):
        ua = ease(c.phase("use", 0.15, 0.4))
        items = [("dob = (28, 2, 2008)", "date of birth"), ("loc = (22.57, 88.36)", "map coordinates"),
                 ("RGB = (255, 210, 0)", "a fixed colour")]
        for k, (s, lab) in enumerate(items):
            a = ease(c.phase("use", 0.15 + k * 0.2, 0.35 + k * 0.2))
            y = 1.9 - k * 1.35
            dax.add_patch(FancyBboxPatch((-3.55, y - 0.5), 7.1, 1.0, boxstyle="round,pad=0,rounding_size=0.18",
                                         facecolor="#13264d", edgecolor=GOLD, lw=2.5, alpha=a, zorder=5))
            code(dax, -3.3, y, s, GOLD, a, size=24)
            dax.text(3.35, y, lab, ha="right", va="center", fontsize=20, color=LTGREY, alpha=a, zorder=6)
        fa = ease(c.phase("use", 0.75, 0.95))
        if fa > 0:
            c.text(0.5, 0.385, "tuples: faster  •  safer  •  can be dict keys", size=30, color=CYAN,
                   alpha=fa * (1 - ease(c.phase("math", 0.0, 0.2))), max_w=0.92)
    c.steps([("[ ]  →  list  (mutable)", 0.0, CYAN), ("( )  →  tuple  (immutable)", 0.3, GOLD)], ys=(0.360, 0.290))
