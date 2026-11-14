"""WHY? — Why does a plane mirror flip left-right but not upside down?  (Class 10 Light)"""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, PathPatch, Rectangle
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import Affine2D
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does a mirror flip LEFT-RIGHT, not UP-DOWN?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",   "A mirror swaps your left and right. But it never turns you upside down. Why not?",
               "A mirror swaps left and right… but never turns you UPSIDE DOWN. Why not?", 4.4),
    ("points", "A plane mirror sends every point straight back. A point in front appears the same distance behind.",
               "A plane mirror sends every point STRAIGHT BACK: same distance in front and behind.", 5.2),
    ("updown", "So the top stays at the top, and the bottom stays at the bottom. Nothing flips vertically.",
               "So TOP stays top, BOTTOM stays bottom. Nothing flips vertically.", 4.6),
    ("depth",  "What really flips is front and back. Your image faces you. We just describe that as left and right. "
               "That's lateral inversion.",
               "What REALLY flips is front ↔ back. We call it left-right: LATERAL INVERSION.", 6.0),
    ("ambul",  "That's why AMBULANCE is written backwards on the front, so drivers can read it in their mirrors.",
               "That's why AMBULANCE is written backwards — drivers read it right in their mirrors!", 5.4),
    ("math",   "Image distance equals object distance. Upright, same size, laterally inverted.",
               "Image distance = object distance. Upright, same size, laterally inverted.", 4.4),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🪞 WHY? — Why does a mirror flip left-right but NOT upside down?

A plane mirror sends every point straight back ↔️
Top stays top, bottom stays bottom ⬆️⬇️
What really flips is FRONT ↔ BACK — we just call it left-right: lateral inversion 🔄

That's why 🚑 AMBULANCE is written backwards — drivers read it in their mirrors!

Plane mirror image: virtual, upright, same size, image distance = object distance.

Light: Reflection — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #LateralInversion #PlaneMirror #Class10Science #Light #CBSE #BoardExams"""

FP = FontProperties(family="Inter", weight="bold")


def glyph(dax, s, x, y, size, col, a, flip=False, z=6):
    tp = TextPath((0, 0), s, size=size, prop=FP)
    bb = tp.get_extents()
    tr = Affine2D().translate(-(bb.x0 + bb.width / 2), -(bb.y0 + bb.height / 2))
    if flip:
        tr = tr.scale(-1, 1)
    tr = tr.translate(x, y)
    dax.add_patch(PathPatch(tr.transform_path(tp), facecolor=col, edgecolor="none", alpha=a, zorder=z))


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    amb = ease(c.phase("ambul", 0.0, 0.25))
    main = 1 - amb
    ma = ease(c.phase("hook", 0.05, 0.4)) * main
    if ma > 0.01:
        # mirror
        dax.add_patch(Rectangle((-0.06, -2.1), 0.12, 4.2, color=CYAN, alpha=ma, zorder=5))
        for y in np.linspace(-2.0, 2.0, 15):
            dax.plot([0.06, 0.26], [y, y - 0.18], color=CYAN, lw=2, alpha=ma * 0.5, zorder=4)
        outline(dax.text(0, 2.3, "mirror", ha="center", fontsize=20, color=CYAN, fontweight="bold", alpha=ma, zorder=6))
        # object: a big "F" (asymmetric, shows flips clearly)
        glyph(dax, "F", -1.8, 0.0, 3.4, GOLD, ma)
        ia = ease(c.phase("hook", 0.4, 0.8)) * main
        glyph(dax, "F", 1.8, 0.0, 3.4, GOLD, ia * 0.55, flip=True)
        outline(dax.text(-1.8, -2.1, "object", ha="center", fontsize=19, color=GOLD, fontweight="bold",
                         alpha=ma, zorder=6))
        outline(dax.text(1.8, -2.1, "image", ha="center", fontsize=19, color=GOLD, fontweight="bold",
                         alpha=ia, zorder=6))
        # points sent straight back
        pa = ease(c.phase("points", 0.1, 0.6)) * main
        if pa > 0:
            for y, col in ((1.25, GREEN), (0.15, PURPLE), (-1.25, PINK)):
                x_obj = -1.8 - 0.55 if y > -1 else -1.8 - 0.55
                dax.add_patch(Circle((x_obj, y), 0.13, color=col, alpha=pa, zorder=8))
                dax.add_patch(Circle((-x_obj, y), 0.13, color=col, alpha=pa, zorder=8))
                dax.plot([x_obj, -0.06], [y, y], color=col, lw=2.5, alpha=pa, zorder=7)
                dax.plot([0.06, -x_obj], [y, y], color=col, lw=2.5, alpha=pa * 0.8, ls=(0, (4, 3)), zorder=7)
            da = ease(c.phase("points", 0.5, 0.8)) * main
            outline(dax.text(-1.2, 1.9, "d", ha="center", fontsize=26, color=WHITE, fontweight="bold", alpha=da,
                             zorder=9, style="italic"))
            outline(dax.text(1.2, 1.9, "d", ha="center", fontsize=26, color=WHITE, fontweight="bold", alpha=da,
                             zorder=9, style="italic"))
        ua = ease(c.phase("updown", 0.1, 0.5)) * main
        if ua > 0:
            outline(dax.text(-3.2, 1.25, "top", ha="left", va="center", fontsize=20, color=GREEN, fontweight="bold",
                             alpha=ua, zorder=9))
            outline(dax.text(3.2, 1.25, "top", ha="right", va="center", fontsize=20, color=GREEN, fontweight="bold",
                             alpha=ua, zorder=9))
            outline(dax.text(-3.2, -1.25, "bottom", ha="left", va="center", fontsize=20, color=PINK,
                             fontweight="bold", alpha=ua, zorder=9))
            outline(dax.text(3.2, -1.25, "bottom", ha="right", va="center", fontsize=20, color=PINK,
                             fontweight="bold", alpha=ua, zorder=9))
        dp = ease(c.phase("depth", 0.15, 0.5)) * main
        if dp > 0:
            dax.add_patch(FancyArrowPatch((-0.9, -0.55), (0.9, -0.55), arrowstyle="<|-|>", mutation_scale=30,
                                          color=WHITE, lw=4, alpha=dp, zorder=9))
            outline(dax.text(0, -0.95, "front ↔ back", ha="center", fontsize=22, color=WHITE, fontweight="bold",
                             alpha=dp, zorder=9))
    if amb > 0.01:
        # ambulance bonnet with mirrored word, and its reflection reading correctly
        dax.add_patch(Rectangle((-3.0, 0.65), 6.0, 1.5, facecolor="#f4f4f4", edgecolor=PINK, lw=4, alpha=amb, zorder=4))
        glyph(dax, "AMBULANCE", 0, 1.4, 0.9, "#d62839", amb, flip=True)
        outline(dax.text(0, 2.4, "written on the ambulance", ha="center", fontsize=20, color=LTGREY,
                         fontweight="bold", alpha=amb, zorder=6))
        ra = ease(c.phase("ambul", 0.4, 0.7))
        dax.add_patch(Rectangle((-3.0, -1.8), 6.0, 1.5, facecolor="#13264d", edgecolor=CYAN, lw=4, alpha=ra, zorder=4))
        glyph(dax, "AMBULANCE", 0, -1.05, 0.9, WHITE, ra)
        outline(dax.text(0, -0.05, "seen in the driver's mirror ✓", ha="center", fontsize=20, color=CYAN,
                         fontweight="bold", alpha=ra, zorder=6))
    c.steps([("image distance  =  object distance", 0.0, WHITE),
             ("upright · same size · laterally inverted", 0.3, GOLD)], ys=(0.345, 0.285))
