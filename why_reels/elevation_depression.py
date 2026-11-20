"""WHY? — Why is the angle of elevation equal to the angle of depression?  (Class 10 Maths) — Part 4 of the trig series."""
import math
import numpy as np
from matplotlib.patches import Polygon, Arc, Circle, Rectangle, FancyBboxPatch
from why_kit import ease, lerp, outline, CYAN, GOLD, PINK, GREEN, PURPLE, WHITE, GREY

TITLE = "Why is elevation = depression?"
TAGS = "Class 10 Maths"
PART = "PART 4 · TRIG SERIES"
END_TEXT = "Watch the whole series on our profile"
BEATS = [
    ("hook",   "Why is the angle of depression always equal to the angle of elevation? One line explains it.",
               "Why is the angle of depression always = the angle of elevation? One line explains it.", 4.2),
    ("scene",  "A girl on top of a tower looks down at a car.",
               "A girl on top of a tower looks down at a car.", 3.4),
    ("dep",    "Her angle of depression is measured from her eye-level line, down to the car.",
               "Angle of depression: from her eye-level line, down to the car.", 4.2),
    ("elev",   "From the car, the angle of elevation is measured from the ground, up to her.",
               "Angle of elevation: from the ground, up to her.", 4.0),
    ("par",    "Her eye-level line and the ground are parallel. The line of sight cuts across both.",
               "Eye-level line ∥ ground. The line of sight cuts across both.", 4.4),
    ("alt",    "Parallel lines cut by a line make equal alternate angles. So the two angles are always equal.",
               "Parallel lines + a cutting line → equal alternate angles. So they're always equal!", 5.0),
    ("use",    "That's why, in heights and distances, you can put the same angle at the bottom of your triangle.",
               "So in heights & distances, the same angle goes at the bottom of your triangle.", 4.6),
    ("end",    "Watch the whole series on our profile, and follow for more.",
               "Watch the whole trig series on our profile!", 3.2),
]
CAPTION = """📐 WHY? Part 4 — Why is the angle of elevation = the angle of depression?

Her eye-level line is parallel to the ground, and the line of sight cuts across both…
Parallel lines + a cutting line → equal ALTERNATE angles ✨
That's why heights & distances questions put the same angle at the bottom of the triangle.

👉 Parts 1–3 (sin²θ + cos²θ = 1 · 1 + tan²θ = sec²θ · sin 30° = ½) are on our profile.

💾 Save it · 📤 Share with your maths group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Trigonometry #HeightsAndDistances #Class10Maths #VisualMaths #BoardExam2027 #CBSE"""

TX, TOP = -1.25, 1.55           # tower right edge x and eye height
CAR = 1.35                      # car x (line of sight ends at the car top)
CAR_Y = 0.12
ANG = math.degrees(math.atan2(TOP - CAR_Y, CAR - TX))


def draw(c):
    dax = c.area(0.02, 0.78, 3.95)
    sa = ease(c.phase("hook", 0.1, 0.8))
    dax.plot([-1.75, 1.85], [0, 0], color=GREEN, lw=4, alpha=sa, zorder=2)                # ground
    dax.add_patch(Rectangle((TX - 0.42, 0), 0.42, TOP - 0.18, facecolor="#33415f", edgecolor=GREY, lw=2, alpha=sa, zorder=2))
    for k in range(4):
        dax.add_patch(Rectangle((TX - 0.32, 0.18 + k * 0.32), 0.22, 0.16, facecolor="#ffd23f", alpha=0.35 * sa, zorder=3))
    pa = ease(c.phase("scene", 0.0, 0.5))
    if pa > 0:                                                                          # girl (stick figure) + car
        hx = TX - 0.12
        dax.add_patch(Circle((hx, TOP + 0.02), 0.07, color=PINK, alpha=pa, zorder=6))
        dax.plot([hx, hx], [TOP - 0.05, TOP - 0.18], color=PINK, lw=3, alpha=pa, zorder=6)
        dax.add_patch(FancyBboxPatch((CAR - 0.05, 0.04), 0.42, 0.13, boxstyle="round,pad=0.02",
                                     facecolor=CYAN, edgecolor="none", alpha=pa, zorder=5))
        dax.add_patch(FancyBboxPatch((CAR + 0.06, 0.15), 0.2, 0.08, boxstyle="round,pad=0.02",
                                     facecolor=CYAN, edgecolor="none", alpha=pa, zorder=5))
        for wx in (CAR + 0.05, CAR + 0.28):
            dax.add_patch(Circle((wx, 0.04), 0.05, color=WHITE, alpha=pa, zorder=6))
    la = ease(c.phase("scene", 0.4, 0.95))
    if la > 0:                                                                          # line of sight
        dax.plot([TX, TX + (CAR - TX) * la], [TOP, TOP + (CAR_Y - TOP) * la], color=WHITE, lw=3.5, zorder=4)
    ea = ease(c.phase("dep", 0.05, 0.4))
    if ea > 0:                                                                          # eye-level line
        dax.plot([TX, TX + 3.0 * ea], [TOP, TOP], color=GOLD, lw=3, ls=(0, (7, 4)), zorder=4)
    da = ease(c.phase("dep", 0.4, 0.8))
    if da > 0:
        dax.add_patch(Arc((TX, TOP), 0.9, 0.9, theta1=-ANG * da, theta2=0, color=GOLD, lw=4, zorder=7))
        outline(dax.text(TX + 0.62, TOP - 0.14, f"{ANG:.0f}°" if c.at("alt") else "θ", color=GOLD, fontsize=28,
                         ha="center", va="center", alpha=da, zorder=9))
        outline(dax.text(TX + 0.9, TOP + 0.15, "depression", color=GOLD, fontsize=24, ha="center", va="center", alpha=da, zorder=9))
    va = ease(c.phase("elev", 0.2, 0.65))
    if va > 0:
        dax.add_patch(Arc((CAR, CAR_Y), 0.9, 0.9, theta1=180 - ANG * va, theta2=180, color=PINK, lw=4, zorder=7))
        outline(dax.text(CAR - 0.62, CAR_Y + 0.14, f"{ANG:.0f}°" if c.at("alt") else "?", color=PINK, fontsize=28,
                         ha="center", va="center", alpha=va, zorder=9))
        outline(dax.text(CAR - 0.85, CAR_Y + 0.45, "elevation", color=PINK, fontsize=24, ha="center", va="center", alpha=va, zorder=9))
        dax.plot([CAR - 0.9, CAR], [CAR_Y, CAR_Y], color=PINK, lw=2.5, ls=(0, (5, 4)), alpha=va, zorder=4)
    pp = ease(c.phase("par", 0.2, 0.6))
    if pp > 0:                                                                          # parallel arrows
        for y in (TOP, CAR_Y):
            xm = 0.55 if y == TOP else -0.35
            dax.annotate("", xy=(xm + 0.18, y), xytext=(xm, y),
                         arrowprops=dict(arrowstyle="->,head_width=0.35,head_length=0.6", color=CYAN, lw=3, alpha=pp), zorder=8)
            dax.annotate("", xy=(xm + 0.30, y), xytext=(xm + 0.12, y),
                         arrowprops=dict(arrowstyle="->,head_width=0.35,head_length=0.6", color=CYAN, lw=3, alpha=pp), zorder=8)
    za = ease(c.phase("alt", 0.1, 0.45))
    if za > 0:                                                                          # the "Z" of alternate angles
        dax.plot([TX + 1.4, TX, CAR, CAR - 1.4], [TOP, TOP, CAR_Y, CAR_Y], color=PURPLE, lw=9, alpha=0.45 * za,
                 zorder=3, solid_capstyle="round")
        outline(dax.text(0.05, 0.98, "Z", color=PURPLE, fontsize=40, fontweight="bold", ha="center", va="center",
                         alpha=za, zorder=9))
    ua = ease(c.phase("use", 0.2, 0.6))
    if ua > 0:
        dax.add_patch(Polygon([[TX, 0], [TX, TOP], [CAR, CAR_Y]], closed=True, facecolor=GOLD, edgecolor="none",
                              alpha=0.15 * ua, zorder=1))
    c.steps([("angle of depression = angle of elevation", 0.1, WHITE),
             ("alternate angles are equal", 0.5, GOLD)], ys=(0.352, 0.290), beat="alt")
