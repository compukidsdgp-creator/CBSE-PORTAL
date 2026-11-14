"""WHY? — Why is the focal length of a concave lens always negative?  (Class 10 Light)"""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Polygon
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why is a CONCAVE lens's focal length negative?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",    "Every concave lens has a negative focal length. Not sometimes. Always. Here's the reason.",
                "Every concave lens has a NEGATIVE focal length. Always. Here's why.", 4.2),
    ("diverge", "Send parallel rays into a concave lens. Instead of meeting, they spread out.",
                "Parallel rays into a concave lens… they SPREAD OUT (diverge).", 4.2),
    ("trace",   "Trace the spread rays backwards. They all seem to come from one point, on the same side as the light. "
                "That's the focus.",
                "Trace them BACKWARDS: they seem to come from one point — the FOCUS — on the light's side.", 6.0),
    ("sign",    "Sign convention: distances along the light's direction are positive. Against it, negative. "
                "The focus is behind the lens, against the light.",
                "Sign convention: ALONG the light = +, AGAINST it = −. This focus is against the light.", 6.2),
    ("convex",  "A convex lens is the opposite. Its rays really meet on the far side. So its focal length is positive.",
                "A CONVEX lens is the opposite: rays meet on the FAR side → focal length +.", 5.2),
    ("math",    "Concave lens, f is negative. Convex lens, f is positive.",
                "Concave: f < 0.  Convex: f > 0.", 3.6),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🔍 WHY? — Why is a concave lens's focal length ALWAYS negative?

Parallel rays → concave lens → they spread out (diverge) ↗️↘️
Trace them backwards → they seem to come from the focus F,
on the SAME side as the incoming light ⬅️

Sign convention 📏: along the light = +, against it = −
So f(concave) < 0 ❌   and   f(convex) > 0 ✅ (rays really meet on the far side)

Refraction of Light — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ConcaveLens #SignConvention #Class10Science #Light #CBSE #BoardExams"""

F = 1.5
YS = (1.2, 0.6, -0.6, -1.2)
END_Y = 0.40


def lens(dax, kind, a):
    t = np.linspace(-1, 1, 60)
    h = 1.8
    if kind == "concave":
        xl = -0.28 + 0.18 * (1 - t ** 2)
        xr = 0.28 - 0.18 * (1 - t ** 2)
    else:
        xl = -0.30 * (1 - t ** 2) - 0.02
        xr = 0.30 * (1 - t ** 2) + 0.02
    pts = np.r_[np.c_[xl, t * h], np.c_[xr[::-1], t[::-1] * h]]
    dax.add_patch(Polygon(pts, closed=True, facecolor=CYAN, edgecolor=CYAN, alpha=0.35 * a, lw=3, zorder=5))
    dax.plot(xl, t * h, color=CYAN, lw=3, alpha=a, zorder=6)
    dax.plot(xr, t * h, color=CYAN, lw=3, alpha=a, zorder=6)


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    cv = ease(c.phase("convex", 0.0, 0.3))
    base = ease(c.phase("hook", 0.05, 0.4))
    dax.plot([-3.4, 3.4], [0, 0], color=GREY, lw=2, alpha=base, zorder=2)
    dax.add_patch(Circle((0, 0), 0.06, color=WHITE, alpha=base, zorder=7))
    cc = base * (1 - cv)
    if cc > 0.01:
        lens(dax, "concave", cc)
        d = ease(c.phase("diverge", 0.1, 0.8))
        for y in YS:
            dax.plot([-3.3, -0.2], [y, y], color=GOLD, lw=3, alpha=cc * ease(c.phase("diverge", 0.0, 0.3)), zorder=4)
            if d > 0:
                L = 3.0 * d
                slope = y / F
                dax.plot([0.2, 0.2 + L], [y, y + slope * L], color=GOLD, lw=3, alpha=cc, zorder=4)
        tr = ease(c.phase("trace", 0.1, 0.6)) * cc
        if tr > 0:
            for y in YS:
                xe = lerp(0.2, -F, tr)
                dax.plot([0.2, xe], [y, y * (1 - (0.2 - xe) / (F + 0.2)) if True else 0], color=GOLD, lw=2.5,
                         ls=(0, (4, 3)), alpha=tr * 0.9, zorder=4)
            fa = ease(c.phase("trace", 0.5, 0.75)) * cc
            dax.add_patch(Circle((-F, 0), 0.13, color=PINK, alpha=fa, zorder=8))
            outline(dax.text(-F, -0.45, "F", ha="center", fontsize=30, color=PINK, fontweight="bold", alpha=fa, zorder=9))
        sa = ease(c.phase("sign", 0.1, 0.45)) * cc
        if sa > 0:
            dax.add_patch(FancyArrowPatch((-3.2, 2.15), (-1.4, 2.15), arrowstyle="-|>", mutation_scale=30, color=GREEN,
                                          lw=4, alpha=sa, zorder=8))
            outline(dax.text(-2.3, 2.35, "light → = +", ha="center", fontsize=21, color=GREEN, fontweight="bold",
                             alpha=sa, zorder=9))
            fb = ease(c.phase("sign", 0.5, 0.8)) * cc
            dax.add_patch(FancyArrowPatch((0, -1.8), (-F, -1.8), arrowstyle="-|>", mutation_scale=28, color=PINK,
                                          lw=4, alpha=fb, zorder=8))
            outline(dax.text(-F / 2, -2.2, "f = −1.5 (against light)", ha="center", fontsize=21, color=PINK,
                             fontweight="bold", alpha=fb, zorder=9))
    if cv > 0.01:
        lens(dax, "convex", cv)
        cvr = ease(c.phase("convex", 0.2, 0.7))
        for y in YS:
            dax.plot([-3.3, -0.1], [y, y], color=GOLD, lw=3, alpha=cv, zorder=4)
            xe = lerp(0.1, F + 1.2, cvr)
            dax.plot([0.1, xe], [y, y - y * (xe - 0.1) / (F - 0.1)], color=GOLD, lw=3, alpha=cv, zorder=4)
        fa = ease(c.phase("convex", 0.55, 0.8))
        dax.add_patch(Circle((F, 0), 0.13, color=GREEN, alpha=fa, zorder=8))
        outline(dax.text(F, 0.4, "F", ha="center", fontsize=30, color=GREEN, fontweight="bold", alpha=fa, zorder=9))
        dax.add_patch(FancyArrowPatch((0, -1.8), (F, -1.8), arrowstyle="-|>", mutation_scale=28, color=GREEN,
                                      lw=4, alpha=fa, zorder=8))
        outline(dax.text(F / 2 + 0.3, -2.2, "f = +1.5 (along light)", ha="center", fontsize=21, color=GREEN,
                         fontweight="bold", alpha=fa, zorder=9))
    c.steps([("concave (diverging):  f < 0", 0.0, WHITE),
             ("convex (converging):  f > 0", 0.3, GOLD)], ys=(0.345, 0.285))
