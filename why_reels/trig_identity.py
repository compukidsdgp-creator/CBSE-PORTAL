"""WHY? — Why is sin²θ + cos²θ = 1?  (Class 10 Maths)"""
import math
import numpy as np
from matplotlib.patches import Polygon, Circle, Arc
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = r"Why is $\sin^{2}\theta + \cos^{2}\theta = 1$ ?"
TAGS = "Class 10 Maths"
BEATS = [
    ("hook",   "Why is sine squared plus cos squared always one? One picture explains it.",
               "Why is sin²θ + cos²θ always 1? One picture explains it.", 3.8),
    ("circle", "Draw a circle of radius one, and mark a point on it at angle theta.",
               "Draw a circle of radius 1 and mark a point on it at angle θ.", 4.0),
    ("tri",    "Drop a line straight down. You get a right angled triangle.",
               "Drop a line straight down. You get a right-angled triangle.", 3.6),
    ("sides",  "Its base is cos theta, its height is sine theta, and the slanted side is the radius, one.",
               "Base = cos θ, height = sin θ, and the slanted side is the radius = 1.", 5.0),
    ("pyth",   "Pythagoras says, base squared plus height squared equals the slanted side squared.",
               "Pythagoras: base² + height² = (slanted side)²", 4.4),
    ("move",   "Move the point anywhere. The triangle changes, but the slanted side is always one.",
               "Move the point anywhere: the triangle changes, but the slanted side is always 1.", 5.4),
    ("math",   "So cos squared theta plus sine squared theta equals one squared, which is one. For every angle.",
               "cos²θ + sin²θ = 1² = 1, for every angle θ.", 4.8),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """📐 WHY? — Why is sin²θ + cos²θ = 1?

Put a point on a circle of radius 1 and drop a line down…
Base = cos θ, height = sin θ, slanted side = 1 → Pythagoras does the rest! ✨
cos²θ + sin²θ = 1² = 1 — for EVERY angle.

The most important identity in Class 10 Trigonometry, finally makes sense. 🧠

💾 Save it · 📤 Share with your maths group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Trigonometry #Class10Maths #VisualMaths #BoardExam2027 #CBSE #MathsTricks"""


def angle(c):
    """θ in degrees: settles at 40°, then sweeps during 'move'."""
    th = lerp(0, 40, ease(c.phase("circle", 0.35, 0.85)))
    mp = c.phase("move", 0.05, 0.95)
    if mp > 0:
        th = 40 + 32 * math.sin(2 * math.pi * mp) + 0 * mp
        th = 40 + 35 * math.sin(math.pi * 2 * mp) * (1 - 0.0)
    return th


def draw(c):
    sq = ease(c.phase("pyth", 0.1, 0.6))
    dax = c.area(0.35 + 0.1 * sq, 0.05 - 0.25 * sq, lerp(3.2, 3.85, sq))
    hide = 1 - ease(c.phase("pyth", 0.45, 0.7))          # side labels make way for the square labels
    th = math.radians(angle(c))
    cx, sy = math.cos(th), math.sin(th)

    ca = ease(c.phase("hook", 0.15, 0.8))
    # axes + unit circle
    dax.plot([-1.25, 1.35], [0, 0], color=GREY, lw=2, alpha=ca, zorder=1)
    dax.plot([0, 0], [-1.25, 1.3], color=GREY, lw=2, alpha=ca, zorder=1)
    t = np.linspace(0, 2 * math.pi * ca, 200)
    dax.plot(np.cos(t), np.sin(t), color=CYAN, lw=3.5, alpha=0.9, zorder=2)

    pa = ease(c.phase("circle", 0.1, 0.4))
    if pa > 0:
        dax.plot([0, cx * pa], [0, sy * pa], color=WHITE, lw=4, zorder=6, solid_capstyle="round")
        dax.add_patch(Circle((cx, sy), 0.045, color=GOLD, alpha=pa, zorder=8))
        dax.add_patch(Arc((0, 0), 0.5, 0.5, theta1=0, theta2=math.degrees(th), color=GOLD, lw=3, alpha=pa, zorder=7))
        outline(dax.text(0.33 * math.cos(th / 2), 0.33 * math.sin(th / 2), r"$\theta$", color=GOLD,
                         fontsize=34, ha="center", va="center", alpha=pa, zorder=9))
    ta = ease(c.phase("tri", 0.1, 0.6))
    if ta > 0:
        dax.plot([cx, cx], [sy, sy - sy * ta], color=PINK, lw=4, zorder=6)
        if ta > 0.7:
            dax.add_patch(Polygon([[0, 0], [cx, 0], [cx, sy]], closed=True, facecolor=PURPLE,
                                  edgecolor="none", alpha=0.28 * (ta - 0.7) / 0.3, zorder=3))
            s = 0.08 * (1 if cx > 0 else -1)
            dax.plot([cx - s, cx - s, cx], [0, 0.08 * np.sign(sy), 0.08 * np.sign(sy)], color=WHITE, lw=2, zorder=6)
    la = ease(c.phase("sides", 0.0, 0.3)) * hide
    if la > 0:
        dax.plot([0, cx], [0, 0], color=GREEN, lw=5, alpha=max(la, 0.0), zorder=5)
        outline(dax.text(cx / 2, -0.13, r"$\cos\theta$", color=GREEN, fontsize=30, ha="center", va="top",
                         alpha=la, zorder=9))
    lb = ease(c.phase("sides", 0.25, 0.55)) * hide
    if lb > 0:
        outline(dax.text(cx + 0.08, sy / 2, r"$\sin\theta$", color=PINK, fontsize=30, ha="left", va="center",
                         alpha=lb, zorder=9))
    lc = ease(c.phase("sides", 0.5, 0.8))
    if lc > 0:
        outline(dax.text(cx / 2 - 0.12, sy / 2 + 0.1, "1", color=WHITE, fontsize=36, fontweight="bold",
                         ha="center", va="center", alpha=lc, zorder=9))

    # squares on the three sides
    if sq > 0:
        a = sq
        # square on the base (below the x axis)
        dax.add_patch(Polygon([[0, 0], [cx, 0], [cx, -abs(cx) * a], [0, -abs(cx) * a]], closed=True,
                              facecolor=GREEN, edgecolor=GREEN, alpha=0.35, lw=2, zorder=2))
        # square on the height (to the right of the vertical side)
        d = 1 if cx >= 0 else -1
        dax.add_patch(Polygon([[cx, 0], [cx + d * abs(sy) * a, 0], [cx + d * abs(sy) * a, sy], [cx, sy]], closed=True,
                              facecolor=PINK, edgecolor=PINK, alpha=0.35, lw=2, zorder=2))
        # square on the hypotenuse (outward, away from the triangle)
        nx, ny = -sy, cx                       # unit normal to the radius
        p0, p1 = np.array([0, 0]), np.array([cx, sy])
        q1, q0 = p1 + np.array([nx, ny]) * a, p0 + np.array([nx, ny]) * a
        dax.add_patch(Polygon([p0, p1, q1, q0], closed=True, facecolor=GOLD, edgecolor=GOLD, alpha=0.30,
                              lw=2, zorder=2))
        if c.phase("pyth", 0.5, 0.8) > 0:
            al = ease(c.phase("pyth", 0.5, 0.8))
            outline(dax.text(cx / 2, -abs(cx) / 2, r"$\cos^{2}\theta$", color=GREEN, fontsize=30, ha="center",
                             va="center", alpha=al, zorder=9))
            outline(dax.text(cx + d * abs(sy) / 2, sy / 2, r"$\sin^{2}\theta$", color=PINK, fontsize=24,
                             ha="center", va="center", alpha=al, zorder=9))
            mid = (p0 + q1) / 2
            outline(dax.text(mid[0], mid[1], r"$1^{2}$", color=GOLD, fontsize=32, ha="center", va="center",
                             alpha=al, zorder=9))

    # live read-out while the point moves
    if c.at("move") and not c.at("math"):
        ra = ease(c.phase("move", 0.0, 0.12))
        c.text(0.5, 0.455, rf"$\cos^2\theta + \sin^2\theta$ = {cx*cx:.2f} + {sy*sy:.2f} = {cx*cx + sy*sy:.2f}",
               size=34, color=WHITE, alpha=ra, max_w=0.9)
        c.text(0.5, 0.415, f"θ = {math.degrees(th):.0f}°", size=26, color=GOLD, alpha=ra)
    c.steps([(r"$\cos^{2}\theta + \sin^{2}\theta = 1^{2}$", 0.05, WHITE),
             (r"$\sin^{2}\theta + \cos^{2}\theta = 1$", 0.45, GOLD)], ys=(0.352, 0.290))
