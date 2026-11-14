"""WHY? — Why does a STACK reverse things?  (Class 12 Computer Science · Data Structures)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does a STACK reverse things?"
TAGS = "Class 12 Computer Science"
BEATS = [
    ("hook",    "Why does a stack always give things back in reverse order? Think of a pile of plates.",
                "Why does a stack give things back in REVERSE order? Think of a pile of plates.", 4.2),
    ("push",    "Push puts a plate on top. Push A, then B, then C.",
                "PUSH puts a plate on top: push A… then B… then C.", 4.6),
    ("top",     "You can only reach the plate on top.",
                "You can only reach the plate on TOP.", 2.8),
    ("pop",     "Pop removes the top plate. So C comes out first, then B, then A.",
                "POP removes the top: C comes out first… then B… then A.", 5.2),
    ("reverse", "In went A, B, C. Out came C, B, A. Last in, first out. That's LIFO.",
                "In: A B C → Out: C B A. Last In, First Out = LIFO.", 4.8),
    ("uses",    "That's why stacks power the undo button, the back button, and reversing a string.",
                "That's why stacks power UNDO, the BACK button and reversing a string.", 4.8),
    ("math",    "In Python, push is append, and pop is pop.",
                "In Python: push → append(), pop → pop()", 4.0),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🥞 WHY? — Why does a STACK reverse things?

Think of a pile of plates 🍽️
PUSH A, B, C → only the TOP is reachable → POP gives C, B, A!
In: A B C → Out: C B A = Last In, First Out (LIFO) 🔁

Stacks power Undo (Ctrl+Z), the browser Back button and string reversal.
Python: push → append(), pop → pop()

A CS Class 12 Data Structures favourite — never forget LIFO again. 🧠

💾 Save it · 📤 Share with your CS batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ComputerScience #Stack #DataStructures #Python #CSClass12 #CBSE"""

ITEMS = [("A", CYAN), ("B", GOLD), ("C", PINK)]
SX, SY0, PW, PH = -1.4, -1.9, 2.4, 0.78      # stack container x, base y, plate size
OUT_X = [1.55, 2.75, 3.95]
LAB = (2.75, 2.2)                             # where push()/pop() labels appear
END_Y = 0.400


def plate(dax, x, y, lab, col, a, z=6, w=PW):
    dax.add_patch(FancyBboxPatch((x - w / 2, y - PH / 2), w, PH, boxstyle="round,pad=0,rounding_size=0.18",
                                 facecolor=col, edgecolor=WHITE, lw=2.5, alpha=a, zorder=z))
    dax.text(x, y, lab, ha="center", va="center", fontsize=34, fontweight="bold", color=NAVY, alpha=a, zorder=z + 1)


def slot_y(k):
    return SY0 + PH / 2 + 0.08 + k * (PH + 0.08)


def draw(c):
    dax = c.area(0.5, -0.1, 8.2)
    ca = ease(c.phase("hook", 0.2, 0.7))
    # container (open at the top)
    xl, xr, yt = SX - PW / 2 - 0.18, SX + PW / 2 + 0.18, slot_y(2) + PH / 2 + 0.6
    dax.plot([xl, xl, xr, xr], [yt, SY0, SY0, yt], color=LTGREY, lw=5, alpha=ca, zorder=4, solid_joinstyle="round")
    outline(dax.text(SX, SY0 - 0.45, "stack", ha="center", fontsize=26, fontweight="bold", color=LTGREY,
                     alpha=ca, zorder=5))

    pushed = [ease(c.phase("push", 0.05 + k * 0.3, 0.3 + k * 0.3)) for k in range(3)]
    popped = [ease(c.phase("pop", 0.08 + k * 0.3, 0.33 + k * 0.3)) for k in (2, 1, 0)]   # A, B, C order
    # popped[i] is progress for item i: C pops first
    pop_p = {2: ease(c.phase("pop", 0.08, 0.33)), 1: ease(c.phase("pop", 0.38, 0.63)),
             0: ease(c.phase("pop", 0.68, 0.93))}
    order_out = {2: 0, 1: 1, 0: 2}            # C → first slot of the output row
    for k, (lab, col) in enumerate(ITEMS):
        p = pushed[k]
        if p <= 0:
            continue
        x, y = SX, lerp(yt + 1.4, slot_y(k), p)
        q = pop_p[k]
        if q > 0:
            ox, oy = OUT_X[order_out[k]], 0.2
            mid = (SX + ox) / 2, yt + 0.6
            # arc out of the top
            x = (1 - q) ** 2 * SX + 2 * (1 - q) * q * mid[0] + q * q * ox
            y = (1 - q) ** 2 * slot_y(k) + 2 * (1 - q) * q * mid[1] + q * q * oy
        plate(dax, x, y, lab, col, min(1, p * 1.5), z=6 + k, w=lerp(PW, 1.05, ease(q)))

    # "push X" labels while pushing
    for k, (lab, col) in enumerate(ITEMS):
        a = c.phase("push", 0.05 + k * 0.3, 0.2 + k * 0.3) * (1 - c.phase("push", 0.3 + k * 0.3, 0.4 + k * 0.3))
        if 0 < a and not c.at("top"):
            outline(dax.text(*LAB, f"push({lab})", ha="center", fontsize=32, fontweight="bold",
                             color=col, family="DejaVu Sans Mono", alpha=min(1, a * 3), zorder=9))
    # top pointer
    ta = ease(c.phase("top", 0.1, 0.4)) * (1 - ease(c.phase("pop", 0.0, 0.1)))
    if ta > 0:
        dax.annotate("top", xy=(SX + PW / 2 + 0.25, slot_y(2)), xytext=(SX + PW / 2 + 1.4, slot_y(2)),
                     color=GOLD, fontsize=30, fontweight="bold", va="center", alpha=ta, zorder=9,
                     arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=3.5, alpha=ta, mutation_scale=28))
        outline(dax.text(SX + PW / 2 + 1.0, slot_y(0), "can't reach\nA or B", ha="left", va="center",
                         fontsize=22, color=LTGREY, alpha=ta, zorder=9))
    # pop labels + output row title
    if c.at("pop"):
        oa = ease(c.phase("pop", 0.0, 0.1))
        outline(dax.text(OUT_X[1], 0.95, "popped out:", ha="center", fontsize=26, fontweight="bold", color=LTGREY,
                         alpha=oa, zorder=9))
        for i, k in enumerate((2, 1, 0)):
            a = c.phase("pop", 0.08 + i * 0.3, 0.2 + i * 0.3) * (1 - c.phase("pop", 0.33 + i * 0.3, 0.4 + i * 0.3))
            if a > 0:
                outline(dax.text(*LAB, "pop()", ha="center", fontsize=32, fontweight="bold",
                                 color=ITEMS[k][1], family="DejaVu Sans Mono", alpha=min(1, a * 3), zorder=9))

    # IN vs OUT, then uses, then Python
    ra = ease(c.phase("reverse", 0.1, 0.4)) * (1 - ease(c.phase("uses", 0.0, 0.2)))
    if ra > 0:
        c.text(0.5, 0.400, "IN:  A  B  C      OUT:  C  B  A", size=38, color=WHITE, alpha=ra)
    la = back_out(c.phase("reverse", 0.5, 0.75)) * (1 - ease(c.phase("end", 0.0, 0.15)))
    if la > 0.01:
        y = lerp(0.340, 0.400, ease(c.phase("uses", 0.0, 0.25)))
        c.pill(0.5, y, 0.70 * min(1, la), 0.056, GOLD, alpha=min(1, la), dark="#2a2000")
        c.text(0.5, y, "LIFO: Last In, First Out", size=40, color=GOLD, alpha=min(1, la))
    if c.at("uses"):
        for k, s_ in enumerate(["↶  Undo (Ctrl + Z)", "←  Browser Back button", "'CBSE' → 'ESBC'"]):
            a = ease(c.phase("uses", 0.15 + k * 0.22, 0.35 + k * 0.22)) * (1 - ease(c.phase("math", 0.0, 0.2)))
            if a > 0:
                c.text(0.5, 0.338 - k * 0.044, s_, size=32, color=CYAN, alpha=a)
    if c.at("math"):
        rows = [("stack = []", 0.05, LTGREY), ("stack.append('A')   # push", 0.25, CYAN),
                ("stack.pop()         # → 'C'", 0.50, PINK)]
        for k, (s_, at, col) in enumerate(rows):
            a = ease(c.phase("math", at, at + 0.2))
            if a > 0:
                c.ax.text(0.5, 0.338 - k * 0.044, s_, ha="center", va="center", fontsize=30, color=col,
                          family="DejaVu Sans Mono", fontweight="bold", alpha=a, zorder=10,
                          transform=c.ax.transAxes)
