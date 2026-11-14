"""WHY? — Why is the slope ZERO at a maximum or minimum?  (Class 12 Maths · Application of Derivatives)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = r"Why is $\dfrac{dy}{dx} = 0$ at a peak?"
TAGS = "Class 12 Maths"
BEATS = [
    ("hook",   "Why is the slope zero at the top of a hill, and at the bottom of a valley? Watch the tangent.",
               "Why is the slope ZERO at the top of a hill and the bottom of a valley? Watch the tangent.", 4.4),
    ("curve",  "Here's a curve, y equals x cubed minus three x. It has a peak, and a valley.",
               "Here's a curve: y = x³ − 3x. It has a peak and a valley.", 4.2),
    ("climb",  "Slide a tangent line along it. Going uphill, the slope is positive.",
               "Slide a tangent along it. Going uphill, the slope is POSITIVE.", 3.8),
    ("peak",   "At the very top, the tangent goes perfectly flat. The slope is zero.",
               "At the very top, the tangent goes perfectly flat: slope = 0.", 3.8),
    ("down",   "Then, going downhill, the slope turns negative.",
               "Going downhill, the slope turns NEGATIVE.", 3.2),
    ("valley", "At the bottom of the valley, it's flat again. Zero.",
               "At the bottom of the valley, flat again: slope = 0.", 3.4),
    ("math",   "So to find peaks and valleys, set d y by d x equal to zero. "
               "Three x squared minus three equals zero, so x equals plus or minus one.",
               "To find peaks and valleys, set dy/dx = 0: 3x² − 3 = 0 → x = ±1", 6.4),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """📈 WHY? — Why is dy/dx = 0 at a maximum or minimum?

Slide a tangent along a curve:
⬆️ uphill → slope positive
⛰️ at the peak → tangent is FLAT → slope = 0
⬇️ downhill → slope negative
🏞️ at the valley → flat again → slope = 0

That's why we solve dy/dx = 0 to find maxima & minima! (y = x³ − 3x → x = ±1)

A must-know idea for Class 12 Application of Derivatives. 🧠

💾 Save it · 📤 Share with your maths group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Calculus #Derivatives #MaximaMinima #Class12Maths #BoardExam2027 #CBSE"""

SY = 0.8                              # vertical squash so the curve fits the frame
f = lambda x: x ** 3 - 3 * x
df = lambda x: 3 * x ** 2 - 3


def point_x(c):
    x = -2.0
    x = lerp(x, -1.3, ease(c.phase("climb", 0.1, 0.9)))
    x = lerp(x, -1.0, ease(c.phase("peak", 0.0, 0.4)))
    x = lerp(x, 0.55, ease(c.phase("down", 0.05, 0.95)))
    x = lerp(x, 1.0, ease(c.phase("valley", 0.0, 0.45)))
    return x


def draw(c):
    dax = c.area(0.0, 0.0, 6.2)
    ca = c.phase("curve", 0.05, 0.6)
    ax_a = ease(c.phase("hook", 0.2, 0.7))
    dax.plot([-2.6, 2.6], [0, 0], color=GREY, lw=2, alpha=ax_a, zorder=1)
    dax.plot([0, 0], [-2.2, 2.2], color=GREY, lw=2, alpha=ax_a, zorder=1)
    if ca > 0:
        xs = np.linspace(-2.05, lerp(-2.05, 2.05, ca), 300)
        dax.plot(xs, SY * f(xs), color=WHITE, lw=4, zorder=3, solid_capstyle="round")
        la = ease(c.phase("curve", 0.5, 0.8))
        outline(dax.text(1.75, 1.85, r"$y = x^{3} - 3x$", color=LTGREY, fontsize=28, ha="center",
                         alpha=la * (1 - ease(c.phase("math", 0.0, 0.2))), zorder=5))

    # marks for peak / valley once reached
    for name, x0, lab, col, dy in [("peak", -1.0, "MAX", PINK, 0.42), ("valley", 1.0, "MIN", GREEN, 0.0)]:
        a = back_out(c.phase(name, 0.35, 0.6))
        if a > 0:
            y0 = SY * f(x0)
            dax.plot([x0, x0], [0, y0], color=col, lw=2, ls=(0, (4, 3)), alpha=min(1, a) * 0.8, zorder=2)
            lx = x0 if dy else x0 + 0.95
            dax.add_patch(FancyBboxPatch((lx - 0.36, y0 + dy - 0.17), 0.72, 0.34,
                                         boxstyle="round,pad=0,rounding_size=0.08", facecolor=NAVY,
                                         edgecolor=col, lw=2.5, alpha=min(1, a), zorder=7))
            dax.text(lx, y0 + dy, lab, ha="center", va="center", fontsize=22, fontweight="bold", color=col,
                     alpha=min(1, a), zorder=8)
            dax.text(x0, -0.22 if x0 < 0 else 0.22, f"x = {x0:+.0f}".replace("+", ""), ha="center",
                     va="center", fontsize=20, color=col, alpha=min(1, a), zorder=8)

    # sliding tangent
    if c.at("climb") and not c.at("math"):
        ta = ease(c.phase("climb", 0.0, 0.15))
        x = point_x(c)
        y, m = SY * f(x), df(x)
        flat = abs(m) < 0.12
        col = GOLD if flat else (GREEN if m > 0 else PINK)
        L = 0.85
        dxl = L / np.sqrt(1 + (SY * m) ** 2)
        dax.plot([x - dxl, x + dxl], [y - SY * m * dxl, y + SY * m * dxl], color=col, lw=5, alpha=ta, zorder=6,
                 solid_capstyle="round")
        dax.add_patch(Circle((x, y), 0.07, color=GOLD, alpha=ta, zorder=7))
        txt = "slope = 0" if flat else f"slope = {m:+.1f}"
        c.pill(0.5, 0.385, 0.44, 0.056, col, alpha=ta, dark="#0b1630")
        c.text(0.5, 0.385, txt, size=36, color=col, alpha=ta)

    if c.at("math"):
        ma = ease(c.phase("math", 0.0, 0.2))
        for x0, col in [(-1.0, PINK), (1.0, GREEN)]:
            y0 = SY * f(x0)
            dax.plot([x0 - 0.7, x0 + 0.7], [y0, y0], color=GOLD, lw=5, alpha=ma, zorder=6, solid_capstyle="round")
            dax.add_patch(Circle((x0, y0), 0.07, color=GOLD, alpha=ma, zorder=7))
    c.steps([(r"$\dfrac{dy}{dx} = 3x^{2} - 3$", 0.05, WHITE),
             (r"$3x^{2} - 3 = 0$", 0.35, CYAN),
             (r"$x = \pm 1$  → peak & valley", 0.62, GOLD)], ys=(0.360, 0.297, 0.240))
