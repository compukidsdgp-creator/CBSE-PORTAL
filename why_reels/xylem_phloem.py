"""WHY? — Why do plants need both xylem and phloem?  (Class 10 Life Processes: Transportation)"""
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why do plants need BOTH xylem and phloem?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",   "Plants have two separate transport pipes, xylem and phloem. Why not just one?",
               "Plants have TWO transport pipes — xylem and phloem. Why not just one?", 4.2),
    ("xylem",  "Xylem carries water and minerals from the roots, up to the leaves. Only upwards.",
               "XYLEM: water + minerals from ROOTS → up to the LEAVES. Only upwards.", 4.6),
    ("leaf",   "Leaves use that water to make food by photosynthesis. Now the food must reach every part of the plant.",
               "Leaves make FOOD by photosynthesis… now it must reach EVERY part.", 4.8),
    ("phloem", "Phloem carries this food, up to buds and fruits, and down to the roots. Both directions! "
               "This is called translocation.",
               "PHLOEM carries food UP to buds & fruits and DOWN to roots — TRANSLOCATION.", 5.8),
    ("why",    "Different materials, going in different directions. So the plant needs two separate pipelines.",
               "Different materials, different directions → TWO separate pipelines.", 4.4),
    ("math",   "Xylem, water, one way up. Phloem, food, up and down.",
               "Xylem: water, one way ↑.  Phloem: food, both ways ↕", 3.8),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🌱 WHY? — Why do plants need BOTH xylem and phloem?

💧 Xylem: water + minerals, roots → leaves (one way, UP)
🍃 Leaves make food by photosynthesis
🍬 Phloem: food from leaves → buds, fruits AND roots (UP and DOWN) — translocation

Different materials + different directions = two separate pipelines!

Life Processes: Transportation in Plants — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Xylem #Phloem #Translocation #Class10Science #CBSE #BoardExams"""

XW, XP = -0.32, 0.32          # xylem (left) and phloem (right) channels in the stem


def draw(c):
    dax = c.area(0.0, -0.2, 7.6)
    a0 = ease(c.phase("hook", 0.05, 0.35))
    # soil + roots
    dax.add_patch(Rectangle((-3.8, -2.25), 7.6, 0.45, facecolor="#3b2a1a", edgecolor="none", alpha=a0, zorder=2))
    for ang in (-0.9, -0.4, 0.4, 0.9):
        dax.plot([0, 1.1 * np.sin(ang)], [-1.8, -1.8 - 0.42 * np.cos(ang)], color="#c9a36a", lw=5, alpha=a0, zorder=3)
    # stem
    dax.add_patch(Rectangle((-0.65, -1.8), 1.3, 3.3, facecolor="#2f6b3a", edgecolor="#3ddc97", lw=2, alpha=a0, zorder=3))
    xa = ease(c.phase("xylem", 0.0, 0.3))
    pa = ease(c.phase("phloem", 0.0, 0.3))
    dax.add_patch(Rectangle((XW - 0.18, -1.8), 0.36, 3.3, facecolor="#123a5c", edgecolor=CYAN, lw=2,
                            alpha=max(0.15, xa) * a0, zorder=4))
    dax.add_patch(Rectangle((XP - 0.18, -1.8), 0.36, 3.3, facecolor="#4a2c0d", edgecolor=GOLD, lw=2,
                            alpha=max(0.15, pa) * a0, zorder=4))
    # leaves
    la = a0
    for side in (-1, 1):
        dax.add_patch(Ellipse((side * 1.35, 1.95), 1.9, 0.8, angle=side * 18, facecolor="#3ddc97", edgecolor="#1f8a5a",
                              lw=3, alpha=la, zorder=3))
    dax.add_patch(Circle((0, 2.25), 0.28, color=PINK, alpha=a0, zorder=4))      # bud / fruit
    sun = ease(c.phase("leaf", 0.1, 0.4))
    if sun > 0:
        dax.add_patch(Circle((2.85, 2.3), 0.35, color=GOLD, alpha=sun, zorder=3))
        for k in range(8):
            ang = k * np.pi / 4
            dax.plot([2.85 + 0.45 * np.cos(ang), 2.85 + 0.62 * np.cos(ang)],
                     [2.3 + 0.45 * np.sin(ang), 2.3 + 0.62 * np.sin(ang)], color=GOLD, lw=3, alpha=sun, zorder=3)
        outline(dax.text(-1.4, 2.6, "food made here", ha="center", fontsize=19, color=GREEN, fontweight="bold",
                         alpha=sun, zorder=8))
    # water going up the xylem
    if xa > 0:
        for k in range(7):
            f = (k / 7 + 0.18 * c.t) % 1.0
            dax.add_patch(Circle((XW, lerp(-1.75, 1.45, f)), 0.1, color=CYAN, alpha=xa, zorder=6))
        outline(dax.text(-0.9, 0.2, "XYLEM\nwater ↑", ha="right", va="center", fontsize=22, color=CYAN,
                         fontweight="bold", alpha=xa, zorder=8))
    # food going up AND down the phloem
    if pa > 0:
        for k in range(4):
            f = (k / 4 + 0.15 * c.t) % 1.0
            dax.add_patch(Circle((XP, lerp(1.45, -1.75, f)), 0.1, color=GOLD, alpha=pa, zorder=6))     # down
        tw = ease(c.phase("phloem", 0.35, 0.6))
        for k in range(3):
            f = (k / 3 + 0.15 * c.t) % 1.0
            dax.add_patch(Circle((XP, lerp(1.0, 2.0, f)), 0.1, color=GOLD, alpha=pa * tw, zorder=6))   # up to bud
        outline(dax.text(0.9, 0.2, "PHLOEM\nfood ↕", ha="left", va="center", fontsize=22, color=GOLD,
                         fontweight="bold", alpha=pa, zorder=8))
        outline(dax.text(0.55, 2.35, "to buds", ha="left", va="center", fontsize=18, color=PINK, fontweight="bold",
                         alpha=pa * tw, zorder=8))
        outline(dax.text(0.75, -1.5, "to roots", ha="left", va="center", fontsize=18, color="#e0b070", fontweight="bold",
                         alpha=pa * tw, zorder=8))
    c.steps([("xylem: water, one way ↑", 0.0, WHITE),
             ("phloem: food, both ways ↕", 0.3, GOLD)], ys=(0.345, 0.285))
