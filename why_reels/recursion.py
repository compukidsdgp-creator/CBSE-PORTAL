"""WHY? — How does RECURSION know when to stop?  (Class 12 Computer Science · Functions)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "How does RECURSION know when to stop?"
TAGS = "Class 12 Computer Science"
BEATS = [
    ("hook",   "How can a function call itself, without going on forever? Let's trace factorial of four.",
               "How can a function call ITSELF without going on forever? Let's trace fact(4).", 4.4),
    ("code",   "Here's the function. If n is one, return one. Otherwise, return n times fact of n minus one.",
               "If n is 1, return 1. Otherwise return n × fact(n − 1).", 5.0),
    ("calls",  "Fact of four calls fact of three. Which calls fact of two. Which calls fact of one.",
               "fact(4) calls fact(3)… which calls fact(2)… which calls fact(1).", 5.4),
    ("base",   "Fact of one is the base case. It just returns one. No more calls. This is where it stops.",
               "fact(1) is the BASE CASE: it returns 1. No more calls — this is where it stops.", 5.2),
    ("unwind", "Now the answers travel back up. Two times one is two. Three times two is six. "
               "Four times six is twenty four.",
               "Answers travel back up: 2 × 1 = 2 → 3 × 2 = 6 → 4 × 6 = 24", 6.4),
    ("math",   "Every recursion needs a base case. Without one, it never stops, and Python raises a recursion error.",
               "Every recursion needs a base case — without it Python raises RecursionError.", 5.4),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🔁 WHY? — How does RECURSION know when to stop?

def fact(n):
    if n == 1: return 1        # base case 🛑
    return n * fact(n - 1)

fact(4) → fact(3) → fact(2) → fact(1) 🛑
then back up: 2 × 1 = 2 → 3 × 2 = 6 → 4 × 6 = 24 ✅

No base case = it never stops → RecursionError ❌
A CS Class 12 favourite — now you can SEE the call stack. 🧠

💾 Save it · 📤 Share with your CS batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Python #Recursion #ComputerScience #CSClass12 #Coding #CBSE"""

MONO = "DejaVu Sans Mono"
FW, FH = 6.4, 0.95
BASE_Y = -1.9
END_Y = 0.372
VALS = {1: 1, 2: 2, 3: 6, 4: 24}


def frame_y(level):           # level 0 = fact(4) at the bottom of the call stack
    return BASE_Y + level * (FH + 0.18)


def draw(c):
    dax = c.area(0.0, 0.1, 7.6)
    # code box (top), shrinks away once the calls begin
    ca = ease(c.phase("code", 0.0, 0.25)) * (1 - ease(c.phase("calls", 0.0, 0.2)))
    if ca > 0:
        dax.add_patch(FancyBboxPatch((-3.5, -1.6), 7.0, 3.6, boxstyle="round,pad=0,rounding_size=0.2",
                                     facecolor="#0b1222", edgecolor="#3a4a6b", lw=2.5, alpha=ca, zorder=5))
        lines = [("def fact(n):", WHITE), ("    if n == 1:", PINK), ("        return 1", PINK),
                 ("    return n * fact(n - 1)", CYAN)]
        for k, (s, col) in enumerate(lines):
            a = ease(c.phase("code", 0.1 + k * 0.15, 0.3 + k * 0.15)) * ca
            dax.text(-3.2, 1.35 - k * 0.85, s, ha="left", va="center", fontsize=28, color=col, family=MONO,
                     fontweight="bold", alpha=a, zorder=6)
        ba = ease(c.phase("code", 0.45, 0.65)) * ca
        if ba > 0:
            outline(dax.text(2.9, 0.1, "← base case", ha="right", fontsize=22, fontweight="bold", color=PINK,
                             alpha=ba, zorder=7))

    # call stack
    if c.at("calls"):
        outline(dax.text(0, BASE_Y - 0.9, "call stack", ha="center", fontsize=24, fontweight="bold", color=LTGREY,
                         alpha=ease(c.phase("calls", 0.0, 0.2)), zorder=7))
        for level, n in enumerate([4, 3, 2, 1]):
            a = ease(c.phase("calls", 0.05 + level * 0.25, 0.25 + level * 0.25))
            if a <= 0:
                continue
            # popping during unwind: fact(1) first
            pop_order = {1: 0, 2: 1, 3: 2, 4: 3}[n]
            pp = ease(c.phase("unwind", 0.05 + pop_order * 0.25, 0.25 + pop_order * 0.25))
            done = pp > 0.5
            y = frame_y(level) + (1 - a) * 0.8
            base = n == 1
            col = GOLD if base else CYAN
            if done:
                col = GREEN
            dax.add_patch(FancyBboxPatch((-FW / 2, y - FH / 2), FW, FH, boxstyle="round,pad=0,rounding_size=0.15",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=a, zorder=5 + level))
            if done:
                txt = f"fact({n}) = {VALS[n]}"
            elif base and c.at("base"):
                txt = "fact(1) → return 1"
            else:
                txt = f"fact({n}) = {n} × fact({n - 1})" if n > 1 else "fact(1) = ?"
            dax.text(0, y, txt, ha="center", va="center", fontsize=26, color=WHITE if not done else GREEN,
                     family=MONO, fontweight="bold", alpha=a, zorder=6 + level)
            # value travelling down to the caller
            if 0 < pp < 1 and n > 1:
                pass
            if n < 4 and 0.5 < pp:
                ta = ease((pp - 0.5) / 0.5)
                outline(dax.text(FW / 2 + 0.1, y - 0.55, f"↓ {VALS[n]}", ha="left", va="center", fontsize=24,
                                 fontweight="bold", color=GREEN, alpha=ta * (1 - c.phase("math", 0.0, 0.2)), zorder=9))
        sa = back_out(c.phase("base", 0.2, 0.45)) * (1 - ease(c.phase("unwind", 0.0, 0.15)))
        if sa > 0.01:
            outline(dax.text(0, frame_y(3) + 0.95, "🛑 STOP — base case" if False else "STOP: base case reached",
                             ha="center", fontsize=28 * min(1, sa), fontweight="bold", color=GOLD, zorder=9))
    c.steps([("base case  →  recursion stops", 0.05, CYAN),
             ("no base case  →  RecursionError", 0.35, PINK)], ys=(0.320, 0.268))
