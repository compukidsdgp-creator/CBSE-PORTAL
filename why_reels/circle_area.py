"""WHY? #1 — Why is the area of a circle πr²?  (Class 10 Maths)"""
import math
import numpy as np
import matplotlib
from matplotlib.patches import Polygon, Circle
from why_kit import ease, lerp, outline, CYAN, GOLD, PINK, NAVY, LTGREY, WHITE

TITLE = r"Why is circle area $= \pi r^{2}$ ?"
TAGS = "Class 10 Maths"
BEATS = [
    ("hook",   "Why is the area of a circle, pi r squared? Let's see it, instead of memorising it.",
               "Why is the area of a circle πr²? Let's see it, instead of memorising it.", 4.0),
    ("radius", "Take a circle of radius r.", "Take a circle of radius r.", 2.6),
    ("rings",  "Slice it into thin rings, like the layers of an onion.",
               "Slice it into thin rings, like the layers of an onion.", 3.6),
    ("outer",  "The outermost ring is as long as the circumference. Two pi r.",
               "The outermost ring is as long as the circumference: 2πr.", 3.6),
    ("unroll", "Now cut every ring at the bottom, and straighten it out.",
               "Now cut every ring at the bottom… and straighten it out.", 5.2),
    ("tri",    "The strips stack up into a triangle. Its base is two pi r, and its height is r.",
               "The strips stack up into a triangle. Base 2πr, height r.", 4.2),
    ("math",   "Area of a triangle is half, base times height. Half of two pi r, times r, is pi r squared.",
               "Area = ½ × base × height = ½ × 2πr × r = πr²", 5.5),
    ("end",    "That's why. Follow C B S E Mock for more why videos.",
               "That's why! Follow @cbsemock for more WHY? videos.", 3.4),
]
CAPTION = """🤔 WHY? — Why is the area of a circle πr²?

Slice a circle into thin rings, unroll every ring… and they stack into a triangle! 🔺
Base = 2πr, height = r → Area = ½ × 2πr × r = πr² ✨

Don't just memorise the formula — see where it comes from. 👀

💾 Save this for revision · 📤 Share with a friend who still mugs up formulas

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #CircleArea #VisualMaths #Class10Maths #BoardExam2027 #CBSE #MathsTricks"""

N = 16


def ring_color(j):
    f = j / (N - 1)
    c0, c1 = np.array(matplotlib.colors.to_rgb(CYAN)), np.array(matplotlib.colors.to_rgb(GOLD))
    return tuple((c0 * (1 - f) + c1 * f) * (1.0 if j % 2 else 0.78))


def ring_polygon(r, curl, dr):
    """Band of radius r; curl 1 = closed ring, 0 = straight strip, cut at the bottom point (0, -r)."""
    L = 2 * math.pi * r
    s = np.linspace(-L / 2, L / 2, 140)
    if curl < 1e-4:
        x, y, nx, ny = s, np.zeros_like(s), np.zeros_like(s), np.ones_like(s)
    else:
        k = curl / r
        x, y = np.sin(k * s) / k, (1 - np.cos(k * s)) / k
        nx, ny = -np.sin(k * s), np.cos(k * s)
    h = dr * 0.46
    return np.vstack([np.c_[x - nx * h, -r + y - ny * h], np.c_[x + nx * h, -r + y + ny * h][::-1]])


def draw(c):
    zo = ease(c.phase("unroll", 0.10, 0.85))
    push = math.sin(math.pi * c.phase("outer")) * 0.18
    dax = c.area(0.0, lerp(0.0, -0.05, zo), lerp(3.05, 6.75, zo) - push)
    dr = 1.0 / N
    rings_on = c.phase("rings", 0.05, 0.85)
    outer_hl = c.phase("outer", 0.0, 0.25) * (1 - c.phase("unroll", 0.0, 0.15))

    if rings_on <= 0:
        d = ease(c.phase("hook", 0.15, 0.75))
        th = np.linspace(-math.pi / 2, -math.pi / 2 + 2 * math.pi * d, 200)
        dax.plot(np.cos(th), np.sin(th), color=CYAN, lw=4, solid_capstyle="round", zorder=5)
        dax.add_patch(Circle((0, 0), 1, facecolor=CYAN, edgecolor="none",
                             alpha=0.25 * c.phase("hook", 0.65, 1.0), zorder=2))
    else:
        for j in range(N):
            appear = ease(rings_on * N - (N - 1 - j))
            if appear <= 0:
                continue
            st = (N - 1 - j) / N * 0.55
            curl = 1 - ease((c.phase("unroll", 0.05, 0.95) - st) / 0.45)
            a = appear * (1 - 0.72 * outer_hl * (j != N - 1))
            dax.add_patch(Polygon(ring_polygon((j + 0.5) * dr, curl, dr), closed=True,
                                  facecolor=ring_color(j), edgecolor=NAVY, lw=0.6, alpha=a, zorder=3 + j / 100))
        if rings_on < 1:
            dax.add_patch(Circle((0, 0), 1, facecolor=CYAN, edgecolor=CYAN, lw=3,
                                 alpha=0.25 * (1 - rings_on), zorder=2))

    rp = c.phase("radius", 0.1, 0.6) * (1 - c.phase("unroll", 0.0, 0.12))
    if rp > 0:
        dax.plot([0, ease(rp)], [0, 0], color="white", lw=4, zorder=20, solid_capstyle="round")
        dax.plot([0], [0], "o", color="white", ms=10, zorder=21)
        if rp > 0.6:
            dax.text(0.5, 0.09, "r", color="white", fontsize=46, fontweight="bold", ha="center",
                     style="italic", zorder=22, alpha=min(1, (rp - 0.6) / 0.3))
    if outer_hl > 0.05:
        outline(dax.text(0.0, -1.32, r"length $= 2\pi r$", color=GOLD, fontsize=40, ha="center",
                         fontweight="bold", zorder=22, alpha=outer_hl))

    tp = ease(c.phase("tri", 0.0, 0.45))
    if tp > 0:
        bx, by = math.pi, -1.0
        tri = np.array([[-bx, by - dr / 2], [bx, by - dr / 2], [0, 0], [-bx, by - dr / 2]])
        pts = np.vstack([np.linspace(tri[k], tri[k + 1], 40) for k in range(3)])[:max(2, int(120 * tp))]
        dax.plot(pts[:, 0], pts[:, 1], color="white", lw=3.5, zorder=30)
        lp = c.phase("tri", 0.30, 0.70)
        if lp > 0:
            dax.annotate("", xy=(bx, by - 0.22), xytext=(-bx, by - 0.22),
                         arrowprops=dict(arrowstyle="<->", color=GOLD, lw=3), zorder=31)
            outline(dax.text(0, by - 0.62, r"base $= 2\pi r$", color=GOLD, fontsize=38, ha="center",
                             fontweight="bold", zorder=32, alpha=lp))
        hp = c.phase("tri", 0.55, 0.95)
        if hp > 0:
            dax.plot([0, 0], [by - dr / 2, 0], color=PINK, lw=3, ls=(0, (4, 3)), zorder=31, alpha=hp)
            outline(dax.annotate(r"height $= r$", xy=(0.04, -0.45), xytext=(1.45, -0.05), color=PINK,
                                 fontsize=36, ha="left", va="center", fontweight="bold", zorder=32, alpha=hp,
                                 arrowprops=dict(arrowstyle="-", color=PINK, lw=2, alpha=hp)))
    gp = ease(c.phase("tri", 0.15, 0.6))
    if gp > 0:
        for j in range(N):
            dax.add_patch(Polygon(ring_polygon((j + 0.5) * dr * 0.75, 1.0, dr * 0.75) + [0, 1.35], closed=True,
                                  facecolor=ring_color(j), edgecolor=NAVY, lw=0.4, alpha=gp, zorder=3))
        dax.text(1.05, 1.35, "same area,\nnew shape", color=LTGREY, fontsize=30, ha="left",
                 va="center", fontweight="bold", zorder=32, alpha=gp)
        dax.annotate("", xy=(0, 0.25), xytext=(0, 0.52), zorder=31,
                     arrowprops=dict(arrowstyle="-|>", color=LTGREY, lw=2.5, alpha=gp, mutation_scale=28))

    c.steps([(r"Area $= \frac{1}{2}\times$ base $\times$ height", 0.05, WHITE),
             (r"$= \frac{1}{2}\times 2\pi r \times r$", 0.40, CYAN),
             (r"$= \pi r^{2}$", 0.68, GOLD)])
