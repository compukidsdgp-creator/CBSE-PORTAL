"""WHY? — Why is d/dx (x²) = 2x?  (Class 12 Maths · Derivatives)"""
import numpy as np
from matplotlib.patches import Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = r"Why is $\dfrac{d}{dx}\,x^{2} = 2x$ ?"
TAGS = "Class 12 Maths"
BEATS = [
    ("hook",   "Why is the derivative of x squared equal to two x? Picture a growing square.",
               "Why is the derivative of x² equal to 2x? Picture a growing square.", 4.0),
    ("square", "Take a square with side x. Its area is x squared.",
               "Take a square with side x. Its area is x².", 3.4),
    ("grow",   "Now grow each side by a tiny amount, d x.",
               "Grow each side by a tiny amount, dx…", 3.4),
    ("strips", "The extra area is two thin strips, each x times d x, plus a tiny corner, d x squared.",
               "Extra area = two thin strips (x · dx each) + a tiny corner (dx)².", 5.2),
    ("tiny",   "When d x is super tiny, that corner is so small that it vanishes.",
               "When dx is super tiny, the corner (dx)² becomes so small it vanishes.", 4.2),
    ("math",   "So the change in area is two x times d x. Divide by d x, and you get two x.",
               "Change in area ≈ 2x · dx. Divide by dx → 2x!", 4.8),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """📐 WHY? — Why is d/dx (x²) = 2x?

Take a square of side x → area x² 🟦
Grow each side by a tiny dx → the extra area is two strips (x·dx each) + a tiny corner (dx)²
As dx → 0, the corner vanishes → change in area ≈ 2x·dx
Divide by dx → d/dx (x²) = 2x ✨

Class 12 Derivatives — finally SEE where the formula comes from. 🧠

💾 Save it · 📤 Share with your maths group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Calculus #Derivatives #Class12Maths #VisualMaths #BoardExam2027 #CBSE"""

X = 2.6
OX, OY = -1.75, -1.75


def draw(c):
    dax = c.area(-0.1, -0.35, 6.4)
    sa = ease(c.phase("square", 0.0, 0.4))
    gw = ease(c.phase("grow", 0.1, 0.8))
    dx = 0.65 * gw
    dx = lerp(dx, 0.12, ease(c.phase("tiny", 0.1, 0.7)))

    # the original square
    if sa > 0:
        dax.add_patch(Rectangle((OX, OY), X * sa, X * sa, facecolor=CYAN, edgecolor=WHITE, lw=3, alpha=0.75, zorder=4))
        la = ease(c.phase("square", 0.3, 0.7))
        outline(dax.text(OX + X / 2, OY + X / 2, r"$x^{2}$", ha="center", va="center", fontsize=54, color=NAVY,
                         alpha=la, zorder=6), w=0)
        outline(dax.text(OX + X / 2, OY - 0.32, "x", ha="center", va="center", fontsize=34, style="italic",
                         fontweight="bold", color=WHITE, alpha=la, zorder=6))
        outline(dax.text(OX - 0.32, OY + X / 2, "x", ha="center", va="center", fontsize=34, style="italic",
                         fontweight="bold", color=WHITE, alpha=la, zorder=6))
    # strips + corner
    if gw > 0:
        st = ease(c.phase("strips", 0.0, 0.3)) if c.at("strips") else 0.0
        col_s = GREEN if st > 0 else GOLD
        dax.add_patch(Rectangle((OX + X, OY), dx, X, facecolor=col_s, edgecolor=WHITE, lw=2.5, alpha=0.85, zorder=4))
        dax.add_patch(Rectangle((OX, OY + X), X, dx, facecolor=col_s, edgecolor=WHITE, lw=2.5, alpha=0.85, zorder=4))
        dax.add_patch(Rectangle((OX + X, OY + X), dx, dx, facecolor=PINK if st > 0 else GOLD, edgecolor=WHITE,
                                lw=2.5, alpha=0.95, zorder=5))
        if c.phase("grow", 0.5, 0.9) > 0 and not c.at("tiny"):
            ga = ease(c.phase("grow", 0.5, 0.9))
            outline(dax.text(OX + X + dx / 2, OY - 0.32, "dx", ha="center", fontsize=26, fontweight="bold",
                             style="italic", color=GOLD, alpha=ga, zorder=6))
            outline(dax.text(OX - 0.4, OY + X + dx / 2, "dx", ha="center", va="center", fontsize=26,
                             fontweight="bold", style="italic", color=GOLD, alpha=ga, zorder=6))
        if st > 0:
            la = st * (1 - ease(c.phase("math", 0.0, 0.2)))
            outline(dax.text(OX + X + dx + 0.12, OY + X / 2, "x · dx", ha="left", va="center", fontsize=28,
                             fontweight="bold", color=GREEN, alpha=la, zorder=7))
            outline(dax.text(OX + X / 2, OY + X + dx + 0.3, "x · dx", ha="center", va="center", fontsize=28,
                             fontweight="bold", color=GREEN, alpha=la, zorder=7))
            ca = st * (1 - ease(c.phase("tiny", 0.5, 0.9)))
            if ca > 0:
                dax.annotate(r"$(dx)^{2}$", xy=(OX + X + dx / 2, OY + X + dx / 2), xytext=(OX + X + 0.9, OY + X + 1.0),
                             fontsize=28, fontweight="bold", color=PINK, alpha=ca, zorder=7,
                             arrowprops=dict(arrowstyle="-|>", color=PINK, lw=2.5, alpha=ca))
        ta = ease(c.phase("tiny", 0.4, 0.8)) * (1 - ease(c.phase("math", 0.0, 0.2)))
        if ta > 0:
            outline(dax.annotate("corner ≈ 0", xy=(OX + X + dx / 2, OY + X + dx / 2), xytext=(OX + X + 0.75, OY + X + 0.9),
                                 fontsize=28, fontweight="bold", color=PINK, alpha=ta, zorder=7,
                                 arrowprops=dict(arrowstyle="-|>", color=PINK, lw=2.5, alpha=ta)))
    eq = ease(c.phase("strips", 0.4, 0.75)) * (1 - ease(c.phase("math", 0.0, 0.2)))
    if eq > 0:
        c.text(0.5, 0.385, r"extra area $= 2\,x\,dx + (dx)^{2}$", size=38, color=WHITE, alpha=eq)
    c.steps([(r"$dA \approx 2x \, dx$", 0.0, WHITE),
             (r"$dA \,/\, dx \approx 2x$", 0.3, CYAN),
             (r"$\dfrac{d}{dx}\,x^{2} = 2x$", 0.55, GOLD)], ys=(0.372, 0.318, 0.250))
