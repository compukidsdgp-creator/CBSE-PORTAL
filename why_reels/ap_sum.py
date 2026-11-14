"""WHY? — Why is the AP sum n/2 (first + last)?  (Class 10 Maths · Arithmetic Progressions)"""
import math
import numpy as np
from matplotlib.patches import Polygon, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = r"Why is $S_n = \dfrac{n}{2}(a + l)$ ?"
TAGS = "Class 10 Maths"
BEATS = [
    ("hook",   "Why is the sum of an A P, n by two, times first plus last? There's a beautiful picture behind it.",
               "Why is the AP sum n/2 × (first + last)? There's a beautiful picture behind it.", 4.6),
    ("stairs", "Take the A P one, two, three, up to six. Draw each number as a column of blocks. A staircase!",
               "Take the AP 1, 2, 3 … 6. Draw each number as a column of blocks — a staircase!", 5.4),
    ("copy",   "Now make a copy, flip it upside down, and fit it on top.",
               "Make a copy, flip it upside down, and fit it on top…", 4.4),
    ("rect",   "Together they make a perfect rectangle. Six columns, each seven blocks tall. "
               "That's first plus last.",
               "A perfect rectangle! 6 columns, each 7 blocks tall — that's first + last (1 + 6).", 5.4),
    ("half",   "The rectangle has six times seven, forty two blocks. Our staircase is exactly half. Twenty one.",
               "Rectangle = 6 × 7 = 42 blocks. Our staircase is exactly HALF: 21.", 5.0),
    ("math",   "So the sum of n terms is n by two, times the first term plus the last term.",
               "So the sum of n terms: Sₙ = n/2 × (first + last).", 4.4),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """➕ WHY? — Why is the AP sum Sₙ = n/2 (a + l)?

Draw 1, 2, 3 … 6 as columns of blocks → a staircase 🪜
Copy it, flip it, fit it on top → a perfect 6 × 7 rectangle! ▭
Rectangle = 42 blocks → the staircase is HALF = 21 ✨
So Sₙ = n/2 × (first + last)

Class 10 Arithmetic Progressions — the picture you'll never forget. 🧠

💾 Save it · 📤 Share with your maths group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ArithmeticProgression #Class10Maths #VisualMaths #BoardExam2027 #CBSE #MathsTricks"""

N = 6
U = 0.56
X0, Y0 = -N * U / 2, -2.25
C = np.array([N / 2, (N + 1) / 2])       # centre of the 6 x 7 rectangle, in block units


def block(dax, cx, cy, th, face, alpha, z=5):
    """A unit block centred at (cx, cy) block-units, rotated by th."""
    h = 0.46
    corners = np.array([[-h, -h], [h, -h], [h, h], [-h, h]])
    R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    pts = (corners @ R.T + [cx, cy]) * U + [X0, Y0]
    dax.add_patch(Polygon(pts, closed=True, facecolor=face, edgecolor=NAVY, lw=1.5, alpha=alpha, zorder=z))


def draw(c):
    dax = c.area(0.0, -0.55, 6.6)
    fade_end = 1 - ease(c.phase("end", 0.0, 0.2))
    # original staircase, column by column
    for i in range(N):
        a = ease(c.phase("stairs", 0.15 + i * 0.12, 0.3 + i * 0.12))
        if a <= 0:
            continue
        dim = 1 - 0.0 * c.at("half")
        for j in range(i + 1):
            block(dax, i + 0.5, j + 0.5 - (1 - a) * 0.6, 0.0, CYAN, a)
        outline(dax.text(X0 + (i + 0.5) * U, Y0 - 0.32, str(i + 1), ha="center", va="center", fontsize=24,
                         fontweight="bold", color=CYAN, alpha=a * (1 - ease(c.phase("rect", 0.0, 0.2))), zorder=8))

    # flipped copy swings over the top (180° about the rectangle's centre)
    cp = c.phase("copy", 0.05, 0.9)
    if cp > 0:
        th = math.pi * ease(cp)
        R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        lift = math.sin(math.pi * ease(cp)) * 0.9          # a little arc so it doesn't clip through
        for i in range(N):
            for j in range(i + 1):
                p = np.array([i + 0.5, j + 0.5])
                q = C + R @ (p - C)
                block(dax, q[0] + lift, q[1], th, GOLD, min(1, cp * 4), z=6)

    # rectangle outline + dimensions
    ra = ease(c.phase("rect", 0.0, 0.3))
    if ra > 0:
        dax.add_patch(Rectangle((X0, Y0), N * U, (N + 1) * U, fill=False, edgecolor=WHITE, lw=4, alpha=ra, zorder=9))
        dax.annotate("", xy=(X0 + N * U, Y0 - 0.35), xytext=(X0, Y0 - 0.35), zorder=9,
                     arrowprops=dict(arrowstyle="<->", color=PINK, lw=3, alpha=ra))
        outline(dax.text(0, Y0 - 0.68, "n = 6 columns", ha="center", fontsize=26, fontweight="bold", color=PINK,
                         alpha=ra * fade_end, zorder=9))
        hx = X0 + N * U + 0.35
        dax.annotate("", xy=(hx, Y0 + (N + 1) * U), xytext=(hx, Y0), zorder=9,
                     arrowprops=dict(arrowstyle="<->", color=GREEN, lw=3, alpha=ra))
        outline(dax.text(hx + 0.2, Y0 + (N + 1) * U / 2, "1 + 6\n= 7", ha="left", va="center", fontsize=26,
                         fontweight="bold", color=GREEN, alpha=ra, zorder=9))
    ha = ease(c.phase("half", 0.1, 0.4))
    if ha > 0:
        c.text(0.5, 0.345, "rectangle = 6 × 7 = 42   →   staircase = 42 ÷ 2 = 21", size=32, color=WHITE,
               alpha=ha * (1 - ease(c.phase("math", 0.0, 0.2))), max_w=0.92)
    c.steps([(r"$S = \frac{6}{2} \times (1 + 6) = 21$", 0.0, CYAN),
             (r"$S_n = \dfrac{n}{2}\,(a + l)$", 0.35, GOLD)], ys=(0.360, 0.290))
