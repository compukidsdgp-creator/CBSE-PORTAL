"""WHY? — Why is the integral the AREA under a curve?  (Class 12 Maths · Integrals / Application of Integrals)"""
import numpy as np
from matplotlib.patches import Polygon, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = r"Why is $\int$ the AREA under a curve?"
TAGS = "Class 12 Maths"
BEATS = [
    ("hook",    "Why does integration give the area under a curve? Let's slice it up.",
                "Why does integration give the AREA under a curve? Let's slice it up.", 3.8),
    ("curve",   "Here's a curve, y equals f of x, from a to b. We want the area underneath it.",
                "A curve y = f(x) from a to b. We want the area underneath.", 4.2),
    ("rects",   "Fill it with rectangles. Each one has width delta x, and height f of x. Add up their areas.",
                "Fill it with rectangles: width Δx, height f(x). Add up their areas.", 5.2),
    ("thinner", "Thinner rectangles fit better. Eight. Sixteen. Sixty four. The gaps almost vanish.",
                "Thinner rectangles fit better: 8… 16… 64… the gaps almost vanish!", 5.4),
    ("limit",   "As the width shrinks towards zero, the sum becomes exact. That limit is the integral.",
                "As Δx → 0, the sum becomes EXACT. That limit is the integral.", 4.6),
    ("math",    "So the area equals the integral from a to b of f of x, d x.",
                "Area = ∫ from a to b of f(x) dx", 4.0),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """∫ WHY? — Why is the integral the AREA under a curve?

Fill the area under y = f(x) with rectangles (width Δx, height f(x)) and add them up 🟦🟦🟦
Make them thinner: 8 → 16 → 64… the gaps vanish
As Δx → 0 the sum becomes EXACT → that limit IS the integral ✨
Area = ∫ₐᵇ f(x) dx

Class 12 Integrals & Application of Integrals — finally see it. 🧠

💾 Save it · 📤 Share with your maths group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Calculus #Integration #Class12Maths #VisualMaths #BoardExam2027 #CBSE"""

A, B = 0.6, 4.6
f = lambda x: 0.9 + 0.55 * np.sin(1.1 * x) + 0.12 * x ** 2
XS = np.linspace(A, B, 4001)
EXACT = float(np.sum((f(XS[1:]) + f(XS[:-1])) / 2 * np.diff(XS)))
OX, OY = -2.6, -1.9            # where (0, 0) sits on screen
SX, SY = 1.15, 0.85            # screen scale


def P(x, y):
    return OX + x * SX, OY + y * SY


def riemann(n):
    dx = (B - A) / n
    xs = A + dx * np.arange(n)
    return xs, dx, float(np.sum(f(xs + dx / 2) * dx))


def draw(c):
    dax = c.area(0.0, -0.05, 7.4)
    aa = ease(c.phase("hook", 0.2, 0.7))
    x0, y0 = P(0, 0)
    dax.plot([x0 - 0.1, P(5.1, 0)[0]], [y0, y0], color=GREY, lw=2.5, alpha=aa, zorder=2)
    dax.plot([x0, x0], [y0 - 0.1, P(0, 5.0)[1]], color=GREY, lw=2.5, alpha=aa, zorder=2)

    ca = c.phase("curve", 0.05, 0.6)
    xx = np.linspace(0.2, 4.9, 400)
    if ca > 0:
        n = max(2, int(len(xx) * ca))
        pts = np.array([P(x, f(x)) for x in xx[:n]])
        dax.plot(pts[:, 0], pts[:, 1], color=WHITE, lw=4, zorder=6)
        la = ease(c.phase("curve", 0.4, 0.8))
        for xv, lab in ((A, "a"), (B, "b")):
            px, py = P(xv, f(xv))
            dax.plot([px, px], [y0, py], color=LTGREY, lw=2, ls=(0, (4, 3)), alpha=la, zorder=5)
            outline(dax.text(px, y0 - 0.35, lab, ha="center", fontsize=30, fontweight="bold", style="italic",
                             color=WHITE, alpha=la, zorder=7))
        outline(dax.text(*P(4.3, f(4.9) + 0.15), "y = f(x)", ha="center", fontsize=26, fontweight="bold",
                         color=LTGREY, alpha=la, zorder=7))
        fa = ease(c.phase("curve", 0.6, 0.95)) * (1 - ease(c.phase("rects", 0.0, 0.3)))
        if fa > 0:
            poly = [P(A, 0)] + [P(x, f(x)) for x in np.linspace(A, B, 120)] + [P(B, 0)]
            dax.add_patch(Polygon(poly, closed=True, facecolor=CYAN, edgecolor="none", alpha=0.35 * fa, zorder=3))

    # rectangles
    if c.at("rects"):
        n = 4
        if c.at("thinner"):
            tp = c.phase("thinner", 0.05, 0.85)
            n = [8, 16, 64][min(2, int(tp * 3))]
        if c.at("limit"):
            n = 200
        ra = ease(c.phase("rects", 0.1, 0.5))
        xs, dx, area = riemann(n)
        for k, xl in enumerate(xs):
            h = f(xl + dx / 2)
            p0 = P(xl, 0)
            col = CYAN if n >= 200 else (GOLD if k % 2 else "#d9a91f")
            dax.add_patch(Rectangle(p0, dx * SX, h * SY, facecolor=col, edgecolor=NAVY if n < 64 else "none",
                                    lw=1.2, alpha=0.8 * ra, zorder=4))
        if n == 4 and ra > 0.5:
            xl = xs[1]
            px, py = P(xl, 0)
            outline(dax.text(px + dx * SX / 2, py - 0.38, "Δx", ha="center", fontsize=24, fontweight="bold",
                             color=GOLD, zorder=8))
            outline(dax.text(px + dx * SX + 0.08, py + f(xl + dx / 2) * SY / 2, "f(x)", ha="left", va="center",
                             fontsize=22, fontweight="bold", color=GOLD, zorder=8))
        sa = ease(c.phase("rects", 0.4, 0.7)) * (1 - ease(c.phase("math", 0.0, 0.2)))
        if sa > 0:
            txt = f"n = {n}:  sum ≈ {area:.3f}" if n < 200 else f"Δx → 0:  area = {EXACT:.3f}"
            col = GREEN if n >= 200 else WHITE
            c.text(0.5, 0.385, txt, size=36, color=col, alpha=sa)
    c.steps([(r"Area $\approx \sum f(x)\,\Delta x$", 0.0, WHITE),
             (r"Area $= \int_{a}^{b} f(x)\,dx$", 0.35, GOLD)], ys=(0.360, 0.288))
