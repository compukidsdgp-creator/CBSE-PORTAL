"""WHY? — Why is a cone's volume ⅓ of a cylinder's?  (Class 10 Maths · Surface Areas & Volumes)"""
import numpy as np
from matplotlib.patches import Polygon, Rectangle, Ellipse
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = r"Why is a cone $\dfrac{1}{3}$ of a cylinder?"
TAGS = "Class 10 Maths"
BEATS = [
    ("hook",  "Why is the volume of a cone exactly one third of a cylinder? Let's pour and see.",
              "Why is a cone's volume exactly ⅓ of a cylinder's? Let's pour and see!", 4.0),
    ("setup", "Take a cone and a cylinder, with the same base, and the same height.",
              "A cone and a cylinder with the SAME base and the SAME height.", 4.0),
    ("pour1", "Fill the cone with water, and pour it into the cylinder. It fills just one third.",
              "Fill the cone and pour it into the cylinder… just ONE THIRD full.", 5.0),
    ("pour2", "Fill it again, and pour. Two thirds.",
              "Again… two thirds.", 3.4),
    ("pour3", "And once more. Full! Exactly three cones fill one cylinder.",
              "Once more… FULL! Exactly 3 cones fill 1 cylinder.", 4.4),
    ("math",  "A cylinder holds pi r squared h. So a cone holds one third of pi r squared h.",
              "Cylinder = πr²h, so cone = ⅓ πr²h.", 4.6),
    ("end",   "Follow C B S E Mock for more why videos.",
              "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🍦 WHY? — Why is a cone's volume ⅓ of a cylinder's?

Same base, same height 📏
Fill the cone with water → pour into the cylinder → ⅓ full 💧
Again → ⅔ … once more → FULL! 3 cones = 1 cylinder ✨
So V(cone) = ⅓ πr²h

Class 10 Surface Areas & Volumes — the experiment that makes the formula stick. 🧠

💾 Save it · 📤 Share with your maths group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Volume #Cone #Cylinder #Class10Maths #VisualMaths #BoardExam2027 #CBSE"""

R, Hh = 1.05, 3.0
CX, YX = -1.75, 1.15                  # cone: apex at the bottom, rim at YX
SX, SB = 1.75, -1.85                  # cylinder centre x, base y
WATER = "#2a8cff"


def cone_level(v):
    """Water height in the (apex-down) cone for volume fraction v."""
    return Hh * max(0.0, v) ** (1 / 3)


def draw(c):
    dax = c.area(0.0, -0.1, 6.6)
    sa = ease(c.phase("setup", 0.0, 0.5))
    ap = YX - Hh
    pours = [c.phase(n, 0.15, 0.8) for n in ("pour1", "pour2", "pour3")]
    done = sum(ease(p) for p in pours)
    # cone fill: refills before each pour, drains while pouring
    cur = next((k for k, p in enumerate(pours) if 0 < p < 1), None)
    if cur is not None:
        cone_v = 1 - ease(pours[cur])
    else:
        nxt = sum(p >= 1 for p in pours)
        refill = ease(c.phase(["pour1", "pour2", "pour3", "math"][min(nxt, 3)], 0.0, 0.15)) if nxt < 3 else 0
        cone_v = refill if c.at("pour1") else 0
        if c.at("setup") and not c.at("pour1"):
            cone_v = ease(c.phase("setup", 0.6, 1.0))
    if sa > 0:
        # cone (apex down)
        L = cone_level(cone_v)
        if L > 0.01:
            w = R * L / Hh
            dax.add_patch(Polygon([[CX, ap], [CX - w, ap + L], [CX + w, ap + L]], closed=True, facecolor=WATER,
                                  edgecolor="none", alpha=0.85, zorder=3))
            dax.add_patch(Ellipse((CX, ap + L), 2 * w, 0.22 * w / R, facecolor="#6fb7ff", edgecolor="none",
                                  alpha=0.9, zorder=4))
        dax.plot([CX - R, CX, CX + R], [YX, ap, YX], color=WHITE, lw=3.5, alpha=sa, zorder=5)
        dax.add_patch(Ellipse((CX, YX), 2 * R, 0.25, fill=False, edgecolor=WHITE, lw=3, alpha=sa, zorder=5))
        # cylinder
        lvl = Hh * done / 3
        if lvl > 0.01:
            dax.add_patch(Rectangle((SX - R, SB), 2 * R, lvl, facecolor=WATER, edgecolor="none", alpha=0.85, zorder=3))
            dax.add_patch(Ellipse((SX, SB + lvl), 2 * R, 0.25, facecolor="#6fb7ff", edgecolor="none", alpha=0.9, zorder=4))
        dax.plot([SX - R, SX - R], [SB, SB + Hh], color=WHITE, lw=3.5, alpha=sa, zorder=5)
        dax.plot([SX + R, SX + R], [SB, SB + Hh], color=WHITE, lw=3.5, alpha=sa, zorder=5)
        dax.add_patch(Ellipse((SX, SB + Hh), 2 * R, 0.25, fill=False, edgecolor=WHITE, lw=3, alpha=sa, zorder=5))
        dax.add_patch(Ellipse((SX, SB), 2 * R, 0.25, fill=False, edgecolor=WHITE, lw=3, alpha=sa, zorder=2))
        # third marks
        for k in (1, 2):
            dax.plot([SX - R - 0.2, SX - R], [SB + Hh * k / 3] * 2, color=LTGREY, lw=2, alpha=sa, zorder=5)
            dax.text(SX - R - 0.28, SB + Hh * k / 3, f"{k}/3", ha="right", va="center", fontsize=20, color=LTGREY,
                     alpha=sa * (1 - ease(c.phase("setup", 0.25, 0.4)) * (1 - ease(c.phase("pour1", 0.0, 0.2)))), zorder=5)
        # same base / same height labels
        la = ease(c.phase("setup", 0.3, 0.7)) * (1 - ease(c.phase("pour1", 0.0, 0.2)))
        if la > 0:
            for x in (CX, SX):
                dax.annotate("", xy=(x + R, YX + 0.45 if x == CX else SB + Hh + 0.45),
                             xytext=(x - R, YX + 0.45 if x == CX else SB + Hh + 0.45), zorder=6,
                             arrowprops=dict(arrowstyle="<->", color=GOLD, lw=2.5, alpha=la))
            outline(dax.text(0, YX + 0.85, "same radius r", ha="center", fontsize=24, fontweight="bold", color=GOLD,
                             alpha=la, zorder=7))
            outline(dax.text(0, -0.35, "same\nheight h", ha="center", va="center", fontsize=24, fontweight="bold",
                             color=PINK, alpha=la, zorder=7))
        # pouring stream
        if cur is not None and 0.05 < pours[cur] < 0.95:
            xs = np.linspace(CX + R * 0.6, SX, 40)
            t_ = (xs - xs[0]) / (xs[-1] - xs[0])
            ys = YX + 0.2 + 0.9 * np.sin(np.pi * t_) - t_ * (YX + 0.2 - (SB + Hh * done / 3 + 0.1))
            dax.plot(xs, ys, color="#6fb7ff", lw=5, alpha=0.9, zorder=6, solid_capstyle="round")
        # count
        n_done = sum(p >= 0.8 for p in pours)
        if c.at("pour1"):
            outline(dax.text(SX, SB - 0.55, f"cones poured: {max(n_done, 0)} / 3", ha="center", fontsize=26,
                             fontweight="bold", color=CYAN, alpha=1 - ease(c.phase("end", 0.0, 0.2)), zorder=7))
        fa = back_out(c.phase("pour3", 0.75, 0.95))
        if fa > 0.01:
            c.pill(0.5, 0.385, 0.62 * min(1, fa), 0.058, GREEN, alpha=min(1, fa) * (1 - ease(c.phase("math", 0, 0.2))),
                   dark="#06261a")
            c.text(0.5, 0.385, "3 cones  =  1 cylinder", size=40, color=GREEN,
                   alpha=min(1, fa) * (1 - ease(c.phase("math", 0, 0.2))))
    c.steps([(r"cylinder $= \pi r^{2} h$", 0.0, WHITE),
             (r"cone $= \dfrac{1}{3}\,\pi r^{2} h$", 0.35, GOLD)], ys=(0.360, 0.282))
