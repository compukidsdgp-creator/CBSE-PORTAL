"""WHY? — Why does electric power have three formulas: VI, I²R and V²/R?  (Class 10 Electricity)"""
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does POWER have THREE formulas?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",   "Power is V I. But it's also I squared R. And V squared by R. Why three formulas? They're really one.",
               "P = VI… also I²R… also V²/R. Why THREE formulas? They're really ONE.", 5.0),
    ("base",   "Start with the basic one. Power equals voltage times current. Energy every second.",
               "Start here: P = V × I — energy used every second.", 4.2),
    ("ohm",    "Now bring in Ohm's law. V equals I R.",
               "Now bring in Ohm's law: V = I R", 3.2),
    ("sub1",   "Replace V with I R. Power becomes I times I R. That's I squared R.",
               "Replace V with IR → P = (IR) × I = I²R", 4.4),
    ("sub2",   "Or replace I with V by R. Power becomes V times V by R. That's V squared by R.",
               "Or replace I with V/R → P = V × (V/R) = V²/R", 4.6),
    ("choose", "Use the one that fits what you know. In series, current is the same, so use I squared R. "
               "In parallel, voltage is the same, so use V squared by R.",
               "SERIES (same I) → use I²R.  PARALLEL (same V) → use V²/R.", 6.4),
    ("math",   "Three formulas, one idea. Just Ohm's law, substituted.",
               "Three formulas, one idea: Ohm's law, substituted.", 3.6),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """⚡ WHY? — Why does power have THREE formulas?

Start with P = V × I (energy per second)
Ohm's law: V = I R
➡️ Replace V: P = (IR) × I = I²R
➡️ Replace I: P = V × (V/R) = V²/R

Which one to use? 🤔
🔗 Series (same current) → I²R
🔀 Parallel (same voltage) → V²/R

Three formulas, ONE idea. Electricity — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ElectricPower #OhmsLaw #Class10Science #Electricity #CBSE #BoardExams"""


def card(dax, x, y, w, h, s, col, a, size=40, sub=None):
    if a <= 0.01:
        return
    dax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.18",
                                 facecolor="#13264d", edgecolor=col, lw=3.5, alpha=min(1, a), zorder=5))
    dax.text(x, y + (0.12 if sub else 0), s, ha="center", va="center", fontsize=size, color=col,
             fontweight="bold", alpha=min(1, a), zorder=6)
    if sub:
        dax.text(x, y - 0.42, sub, ha="center", va="center", fontsize=17, color=LTGREY, alpha=min(1, a), zorder=6)


def arr(dax, p, q, col, a):
    if a > 0.01:
        dax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=30, color=col, lw=4, alpha=a, zorder=4))


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    ch = ease(c.phase("choose", 0.0, 0.25))
    ha = ease(c.phase("hook", 0.1, 0.4)) * (1 - ease(c.phase("base", 0.0, 0.2)))
    if ha > 0.01:
        for k, (s, col) in enumerate((("$VI$", GOLD), ("$I^2R$", GREEN), (r"$\frac{V^2}{R}$", PINK))):
            a = ha * ease(c.phase("hook", 0.15 + 0.15 * k, 0.35 + 0.15 * k))
            card(dax, -2.2 + 2.2 * k, 0.6, 1.8, 1.3, s, col, a, size=44)
            outline(dax.text(-2.2 + 2.2 * k, -0.45, "?", ha="center", fontsize=40, color=WHITE, fontweight="bold",
                             alpha=a, zorder=6))
    top = 1 - ch
    card(dax, -1.45, 1.55, 2.6, 1.25, "$P = VI$", GOLD, back_out(c.phase("base", 0.05, 0.4)) * top,
         sub="energy per second")
    card(dax, 1.55, 1.55, 2.4, 1.25, "$V = IR$", CYAN, back_out(c.phase("ohm", 0.05, 0.4)) * top, sub="Ohm's law")
    a1 = ease(c.phase("sub1", 0.0, 0.3)) * top
    arr(dax, (-1.45, 0.85), (-1.6, -0.55), GOLD, a1)
    arr(dax, (1.2, 0.85), (-0.9, -0.55), CYAN, a1)
    card(dax, -1.65, -1.3, 2.6, 1.25, "$P = I^2R$", GREEN, back_out(c.phase("sub1", 0.3, 0.6)) * top,
         sub="put V = IR")
    a2 = ease(c.phase("sub2", 0.0, 0.3)) * top
    arr(dax, (-0.4, 0.85), (1.3, -0.55), GOLD, a2)
    arr(dax, (1.9, 0.85), (1.9, -0.55), CYAN, a2)
    card(dax, 1.75, -1.3, 2.6, 1.25, r"$P = \frac{V^2}{R}$", PINK, back_out(c.phase("sub2", 0.3, 0.6)) * top,
         sub="put I = V/R")
    if ch > 0.01:
        # series: same current; parallel: same voltage
        sa = ease(c.phase("choose", 0.15, 0.45))
        dax.add_patch(FancyBboxPatch((-3.3, 0.25), 3.1, 2.1, boxstyle="round,pad=0,rounding_size=0.2",
                                     facecolor="#0e1d3d", edgecolor=GREEN, lw=3, alpha=sa, zorder=4))
        outline(dax.text(-1.75, 2.0, "SERIES", ha="center", fontsize=24, color=GREEN, fontweight="bold", alpha=sa, zorder=6))
        dax.plot([-3.0, -0.5], [1.15, 1.15], color=LTGREY, lw=3, alpha=sa, zorder=5)
        for x in (-2.35, -1.2):
            dax.add_patch(FancyBboxPatch((x - 0.3, 1.0), 0.6, 0.3, boxstyle="square,pad=0", facecolor=NAVY,
                                         edgecolor=GOLD, lw=3, alpha=sa, zorder=6))
        dax.text(-1.75, 0.6, "same  I  →  $I^2R$", ha="center", fontsize=22, color=WHITE, fontweight="bold",
                 alpha=sa, zorder=6)
        pa = ease(c.phase("choose", 0.5, 0.8))
        dax.add_patch(FancyBboxPatch((0.2, -1.95), 3.1, 2.1, boxstyle="round,pad=0,rounding_size=0.2",
                                     facecolor="#0e1d3d", edgecolor=PINK, lw=3, alpha=pa, zorder=4))
        outline(dax.text(1.75, -0.2, "PARALLEL", ha="center", fontsize=24, color=PINK, fontweight="bold", alpha=pa, zorder=6))
        for y in (-0.75, -1.25):
            dax.plot([0.6, 2.9], [y, y], color=LTGREY, lw=3, alpha=pa, zorder=5)
            dax.add_patch(FancyBboxPatch((1.45, y - 0.15), 0.6, 0.3, boxstyle="square,pad=0", facecolor=NAVY,
                                         edgecolor=GOLD, lw=3, alpha=pa, zorder=6))
        dax.plot([0.6, 0.6], [-1.25, -0.75], color=LTGREY, lw=3, alpha=pa, zorder=5)
        dax.plot([2.9, 2.9], [-1.25, -0.75], color=LTGREY, lw=3, alpha=pa, zorder=5)
        dax.text(1.75, -1.7, "same  V  →  $V^2/R$", ha="center", fontsize=22, color=WHITE, fontweight="bold",
                 alpha=pa, zorder=6)
    c.steps([("$P = VI = I^2R = V^2/R$", 0.0, WHITE),
             ("one idea: Ohm's law substituted", 0.3, GOLD)], ys=(0.345, 0.285))
