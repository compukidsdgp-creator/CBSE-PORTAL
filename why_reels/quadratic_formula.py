"""WHY? — Where does the QUADRATIC FORMULA come from?  (Class 10 Maths · Quadratic Equations)"""
from matplotlib.patches import Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Where does the QUADRATIC FORMULA come from?"
TAGS = "Class 10 Maths"
BEATS = [
    ("hook",   "Where does the quadratic formula come from? It's a square, completed.",
               "Where does the quadratic formula come from? It's a SQUARE, completed!", 3.8),
    ("pieces", "Picture x squared as a square, and b x as a long rectangle.",
               "Picture x² as a square, and bx as a long rectangle.", 3.8),
    ("split",  "Cut the rectangle in half, and stick the two halves onto two sides of the square.",
               "Cut the rectangle in half and stick the halves onto two sides.", 4.4),
    ("corner", "A small corner is missing. Its area is b by two, squared. Add it, and you have a perfect square.",
               "A corner is missing: (b/2)². Add it → a PERFECT square!", 5.4),
    ("eq",     "So x squared plus b x, plus b by two squared, equals x plus b by two, all squared.",
               "x² + bx + (b/2)² = (x + b/2)²", 4.6),
    ("math",   "Take the square root, solve for x, and do the same for a x squared plus b x plus c. "
               "Out pops the quadratic formula.",
               "Square-root, solve for x (for ax² + bx + c = 0) → the quadratic formula!", 5.8),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🔲 WHY? — Where does the QUADRATIC FORMULA come from?

Picture x² as a square and bx as a rectangle
Cut the rectangle in half → stick the halves on two sides
A corner is missing: (b/2)² → add it → a PERFECT square ✨
x² + bx + (b/2)² = (x + b/2)²
Solve for x (for ax² + bx + c = 0) → x = (−b ± √(b² − 4ac)) / 2a

"Completing the square" — Class 10 Quadratic Equations, made visual. 🧠

💾 Save it · 📤 Share with your maths group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #QuadraticEquations #CompletingTheSquare #Class10Maths #VisualMaths #CBSE"""

X, Bv = 2.4, 1.6           # side x and length b (screen units)
OX, OY = -1.95, -1.6


def draw(c):
    dax = c.area(0.15, 0.0, 6.4)
    pa = ease(c.phase("pieces", 0.0, 0.4))
    sp = ease(c.phase("split", 0.1, 0.8))
    co = ease(c.phase("corner", 0.35, 0.65))
    h2 = Bv / 2
    if pa > 0:
        dax.add_patch(Rectangle((OX, OY), X, X, facecolor=CYAN, edgecolor=WHITE, lw=3, alpha=0.8 * pa, zorder=4))
        outline(dax.text(OX + X / 2, OY + X / 2, r"$x^{2}$", ha="center", va="center", fontsize=48, color=NAVY,
                         alpha=pa, zorder=6), w=0)
        outline(dax.text(OX + X / 2, OY - 0.32, "x", ha="center", fontsize=30, style="italic", fontweight="bold",
                         color=WHITE, alpha=pa, zorder=6))
        outline(dax.text(OX - 0.3, OY + X / 2, "x", ha="center", va="center", fontsize=30, style="italic",
                         fontweight="bold", color=WHITE, alpha=pa, zorder=6))
        # the bx rectangle: starts to the right of the square as one piece (b wide, x tall)
        # half 1 → right side of the square;  half 2 → rotates to the top of the square
        rx0 = OX + X + 0.5
        # half 1 (right side)
        x1 = lerp(rx0, OX + X, sp)
        dax.add_patch(Rectangle((x1, OY), h2, X, facecolor=GOLD, edgecolor=WHITE, lw=2.5, alpha=0.85 * pa, zorder=4))
        # half 2: from right of half 1 to the top of the square (rotated 90°)
        if sp < 0.5:
            x2 = rx0 + h2 + 0.0
            dax.add_patch(Rectangle((x2 + sp * 0.8, OY), h2, X, facecolor=GOLD, edgecolor=WHITE, lw=2.5,
                                    alpha=0.85 * pa, zorder=4))
        else:
            f = ease((sp - 0.5) / 0.5)
            w, hgt = lerp(h2, X, f), lerp(X, h2, f)
            xx = lerp(rx0 + h2 + 0.4, OX, f)
            yy = lerp(OY, OY + X, f)
            dax.add_patch(Rectangle((xx, yy), w, hgt, facecolor=GOLD, edgecolor=WHITE, lw=2.5, alpha=0.85 * pa, zorder=4))
        lab_a = pa * (1 - ease(c.phase("eq", 0.0, 0.2)))
        if sp < 0.1:
            outline(dax.text(rx0 + h2, OY + X / 2, "bx", ha="center", va="center", fontsize=34, fontweight="bold",
                             color=NAVY, alpha=pa, zorder=6), w=0)
            outline(dax.text(rx0 + h2, OY - 0.32, "b", ha="center", fontsize=30, style="italic", fontweight="bold",
                             color=GOLD, alpha=pa, zorder=6))
        elif sp >= 0.99:
            outline(dax.text(OX + X + h2 / 2, OY + X / 2, r"$\frac{b}{2}x$", ha="center", va="center", fontsize=28,
                             color=NAVY, alpha=lab_a, zorder=6), w=0)
            outline(dax.text(OX + X / 2, OY + X + h2 / 2, r"$\frac{b}{2}x$", ha="center", va="center", fontsize=28,
                             color=NAVY, alpha=lab_a, zorder=6), w=0)
            outline(dax.text(OX + X + h2 / 2, OY - 0.32, r"$\frac{b}{2}$", ha="center", fontsize=30, color=GOLD,
                             alpha=lab_a, zorder=6))
    # missing corner
    if c.at("corner"):
        ma = ease(c.phase("corner", 0.0, 0.25))
        cx0, cy0 = OX + X, OY + X
        if co < 1:
            dax.add_patch(Rectangle((cx0, cy0), h2, h2, fill=False, edgecolor=PINK, lw=3, ls=(0, (4, 3)), alpha=ma, zorder=5))
            outline(dax.text(cx0 + h2 + 0.15, cy0 + h2 + 0.15, "missing!", ha="left", fontsize=24, fontweight="bold",
                             color=PINK, alpha=ma * (1 - co), zorder=7))
        if co > 0:
            dax.add_patch(Rectangle((cx0 + (1 - co) * 0.9, cy0 + (1 - co) * 0.9), h2, h2, facecolor=PINK, edgecolor=WHITE,
                                    lw=2.5, alpha=co, zorder=5))
            outline(dax.text(cx0 + h2 / 2, cy0 + h2 / 2, r"$(\frac{b}{2})^{2}$", ha="center", va="center", fontsize=22,
                             color=NAVY, alpha=co, zorder=6), w=0)
        fa = ease(c.phase("corner", 0.7, 0.95))
        if fa > 0:
            S = X + h2
            dax.add_patch(Rectangle((OX, OY), S, S, fill=False, edgecolor=GREEN, lw=5, alpha=fa, zorder=7))
            outline(dax.text(OX + S + 0.2, OY + S / 2, r"$x + \frac{b}{2}$", ha="left", va="center", fontsize=30,
                             color=GREEN, alpha=fa, zorder=8))
    ea = ease(c.phase("eq", 0.1, 0.4)) * (1 - ease(c.phase("math", 0.0, 0.2)))
    if ea > 0:
        c.text(0.5, 0.385, r"$x^{2} + bx + (\frac{b}{2})^{2} = (x + \frac{b}{2})^{2}$", size=40, color=WHITE, alpha=ea)
    c.steps([(r"$(x + \frac{b}{2})^{2} = \frac{b^{2}}{4} - c$   (a = 1)", 0.05, CYAN),
             (r"$x = (-b \pm \sqrt{b^{2} - 4ac})\ /\ 2a$", 0.45, GOLD)], ys=(0.362, 0.290))
