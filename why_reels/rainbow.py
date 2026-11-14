"""WHY? — Why do we see a RAINBOW?  (Class 10 Science · Human Eye & the Colourful World)"""
import math
import numpy as np
from matplotlib.patches import Circle, Polygon, Arc, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why do we see a RAINBOW?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",  "Why does a rainbow appear after rain? Every raindrop is a tiny prism.",
              "Why does a rainbow appear after rain? Every raindrop is a tiny PRISM.", 3.8),
    ("prism", "Sunlight is a mix of colours. In glass or water, each colour bends by a different amount. "
              "Violet bends the most, red the least. This is dispersion.",
              "Each colour bends differently in glass or water: violet MOST, red LEAST — dispersion.", 6.4),
    ("drop",  "In a raindrop, light bends as it enters, reflects off the back, and bends again as it leaves. "
              "The colours fan out.",
              "In a raindrop: light bends going in → reflects off the back → bends coming out. Colours fan out!", 6.4),
    ("sky",   "Millions of drops at different heights send different colours to your eyes, painting the arc. "
              "Red on top, violet at the bottom.",
              "Millions of drops at different heights send different colours to you: red on top, violet below.", 6.0),
    ("rule",  "That's why you only see a rainbow with the sun behind you, and rain in front.",
              "You only see a rainbow with the SUN BEHIND you and RAIN IN FRONT.", 4.2),
    ("end",   "Follow C B S E Mock for more why videos.",
              "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🌈 WHY? — Why do we see a RAINBOW?

Every raindrop is a tiny prism 💧
1️⃣ Dispersion: each colour bends differently (violet most, red least)
2️⃣ Inside the drop: refraction → internal reflection → refraction again → colours fan out
3️⃣ Millions of drops at different heights send different colours to your eyes → the arc! (red on top, violet below)
☀️ Sun behind you, rain in front — that's the only way to see one.

Class 10 Science — Human Eye & the Colourful World. 🧠

💾 Save it · 📤 Share with your science group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Rainbow #Dispersion #Physics #Class10Science #BoardExam2027 #CBSE"""

END_Y = 0.392
COLS = ["#ff4b4b", "#ff9f43", "#ffd23f", "#3ddc97", "#2ad4ff", "#4f6bff", "#a98bff"]   # R → V


def draw(c):
    dax = c.area(0.0, 0.0, 7.6)
    # hook: a soft rainbow and one big raindrop
    hk = ease(c.phase("hook", 0.15, 0.6)) * (1 - ease(c.phase("prism", 0.0, 0.2)))
    if hk > 0:
        for k, col in enumerate(COLS):
            r = 2.9 - k * 0.16
            dax.add_patch(Arc((0, -1.6), 2 * r, 2 * r, theta1=0, theta2=180, color=col, lw=8, alpha=0.75 * hk, zorder=3))
        dax.add_patch(Circle((0, -0.6), 0.55, facecolor="#2a6fdb", edgecolor=WHITE, lw=2.5, alpha=0.6 * hk, zorder=4))
        outline(dax.text(0, -0.62, "?", ha="center", va="center", fontsize=40, fontweight="bold", color=WHITE,
                         alpha=hk, zorder=5))
    # 1) prism dispersion
    pa = ease(c.phase("prism", 0.0, 0.2)) * (1 - ease(c.phase("drop", 0.0, 0.2)))
    if pa > 0:
        tri = np.array([[0.0, 1.9], [-1.25, -0.6], [1.25, -0.6]])
        dax.add_patch(Polygon(tri, closed=True, facecolor=CYAN, edgecolor=WHITE, lw=2.5, alpha=0.25 * pa, zorder=3))
        rp = c.phase("prism", 0.15, 0.6)
        dax.plot([-3.6, lerp(-3.6, -0.62, min(1, rp * 2))], [0.2, lerp(0.2, 0.65, min(1, rp * 2))], color=WHITE, lw=7,
                 alpha=pa, zorder=5, solid_capstyle="round")
        if rp > 0.5:
            sp = ease((rp - 0.5) / 0.5)
            for k, col in enumerate(COLS):
                ang = math.radians(-12 - k * 3.2)
                x1, y1 = 0.62, 0.15 - k * 0.04
                dax.plot([-0.62, x1], [0.65, y1], color=col, lw=3, alpha=pa, zorder=5)
                dax.plot([x1, x1 + 3.2 * sp * math.cos(ang)], [y1, y1 + 3.2 * sp * math.sin(ang)], color=col, lw=5,
                         alpha=pa, zorder=5, solid_capstyle="round")
        la = ease(c.phase("prism", 0.65, 0.9)) * pa
        outline(dax.text(3.0, -0.35, "red", ha="center", fontsize=24, fontweight="bold", color=COLS[0], alpha=la, zorder=7))
        outline(dax.text(2.7, -2.0, "violet", ha="center", fontsize=24, fontweight="bold", color=COLS[6], alpha=la, zorder=7))
        outline(dax.text(-2.3, 1.0, "white light", ha="center", fontsize=24, fontweight="bold", color=WHITE, alpha=la, zorder=7))

    # 2) inside a raindrop
    da = ease(c.phase("drop", 0.0, 0.25)) * (1 - ease(c.phase("sky", 0.0, 0.2)))
    if da > 0:
        Rd = 1.75
        dax.add_patch(Circle((0.4, 0.2), Rd, facecolor="#2a6fdb", edgecolor=WHITE, lw=3, alpha=0.25 * da + 0.05, zorder=3))
        rp = c.phase("drop", 0.15, 0.85)
        # entry, back reflection, exit (schematic)
        p_in = (0.4 - Rd * 0.6, 0.2 + Rd * 0.8)
        p_back = (0.4 + Rd * 0.92, 0.2 - Rd * 0.38)
        dax.plot([-3.6, lerp(-3.6, p_in[0], min(1, rp * 3))], [p_in[1]] * 2, color=WHITE, lw=6, alpha=da, zorder=5)
        if rp > 0.33:
            f = min(1, (rp - 0.33) * 3)
            dax.plot([p_in[0], lerp(p_in[0], p_back[0], f)], [p_in[1], lerp(p_in[1], p_back[1], f)], color=WHITE, lw=4,
                     alpha=da, zorder=5)
        if rp > 0.66:
            f = (rp - 0.66) / 0.34
            for k, col in enumerate(COLS):
                ex = (0.4 - Rd * 0.55 + k * 0.05, 0.2 - Rd * 0.83 + k * 0.03)
                dax.plot([p_back[0], ex[0]], [p_back[1], ex[1]], color=col, lw=2.5, alpha=da, zorder=5)
                ang = math.radians(205 + k * 2.2)
                dax.plot([ex[0], ex[0] + 2.0 * f * math.cos(ang)], [ex[1], ex[1] + 2.0 * f * math.sin(ang)], color=col,
                         lw=4.5, alpha=da, zorder=5, solid_capstyle="round")
        la = ease(c.phase("drop", 0.2, 0.4))
        for txt, xy, xt, at in [("1. bends in", p_in, (-2.6, 2.3), 0.2), ("2. reflects", p_back, (2.6, 0.9), 0.45),
                                ("3. bends out", (0.4 - Rd * 0.5, 0.2 - Rd * 0.85), (-2.2, -2.2), 0.7)]:
            a = ease(c.phase("drop", at, at + 0.15)) * da
            if a > 0:
                dax.annotate(txt, xy=xy, xytext=xt, ha="center", fontsize=23, fontweight="bold", color=GOLD, alpha=a,
                             zorder=8, arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.2, alpha=a))

    # 3) the arc in the sky
    sa = ease(c.phase("sky", 0.05, 0.4))
    if sa > 0:
        dax.add_patch(Rectangle((-3.8, -2.85), 7.6, 0.75, facecolor="#1b3a2a", edgecolor="none", alpha=sa, zorder=2))
        grow = ease(c.phase("sky", 0.2, 0.8))
        for k, col in enumerate(COLS):
            r = 3.15 - k * 0.17
            dax.add_patch(Arc((0.6, -2.1), 2 * r, 2 * r, theta1=90 - 90 * grow, theta2=90 + 90 * grow, color=col,
                              lw=9, alpha=sa, zorder=3))
        ox, oy = 0.6, -2.1
        dax.add_patch(Circle((ox, oy + 0.42), 0.17, color=WHITE, alpha=sa, zorder=6))
        dax.plot([ox, ox], [oy + 0.25, oy - 0.25], color=WHITE, lw=5, alpha=sa, zorder=6)
        outline(dax.text(ox, oy - 0.55, "you", ha="center", fontsize=22, fontweight="bold", color=WHITE, alpha=sa, zorder=7))
        # rain streaks
        rng = np.random.default_rng(8)
        for k in range(40):
            x = rng.uniform(-3.6, 3.6); y = (rng.uniform(-1.8, 2.6) - c.t * 1.6) % 4.4 - 1.8
            dax.plot([x, x - 0.05], [y, y - 0.22], color="#9cc8ff", lw=1.5, alpha=0.5 * sa, zorder=4)
    ra = ease(c.phase("rule", 0.05, 0.35))
    if ra > 0:
        dax.add_patch(Circle((-3.2, 2.3), 0.42 * ra, color=GOLD, alpha=ra, zorder=7))
        outline(dax.text(-3.2, 1.6, "sun behind", ha="center", fontsize=20, fontweight="bold", color=GOLD, alpha=ra, zorder=8))
    c.steps([("sun behind you  +  rain in front", 0.25, CYAN),
             ("refraction + dispersion + reflection", 0.5, GOLD)], ys=(0.333, 0.272), beat="rule")
