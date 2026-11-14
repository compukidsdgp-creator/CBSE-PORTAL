"""WHY? — Why do we BALANCE chemical equations?  (Class 10 Chemical Reactions)"""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why do we BALANCE chemical equations?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",   "Why can't we just write hydrogen plus oxygen gives water, and stop? Why balance it?",
               "Why not just write H₂ + O₂ → H₂O and stop? Why BALANCE it?", 4.2),
    ("unbal",  "Look at the atoms. Two hydrogen and two oxygen on the left.",
               "Count the atoms. LEFT: 2 hydrogen, 2 oxygen.", 3.8),
    ("count",  "But on the right, only one oxygen. Where did the other oxygen atom go? It can't just vanish!",
               "RIGHT: only 1 oxygen! Where did the other one go? It can't just VANISH!", 5.0),
    ("law",    "The law of conservation of mass says atoms are never created or destroyed in a reaction. "
               "They only rearrange.",
               "Law of Conservation of Mass: atoms are never created or destroyed — only REARRANGED.", 5.6),
    ("fix",    "So we balance. Two H two plus O two gives two H two O. Now four hydrogen and two oxygen on each side.",
               "Balance it: 2H₂ + O₂ → 2H₂O. Now 4 H and 2 O on EACH side ✓", 5.6),
    ("math",   "Atoms in equals atoms out. So mass of reactants equals mass of products.",
               "Atoms in = atoms out → mass of reactants = mass of products.", 4.2),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """⚖️ WHY? — Why do we BALANCE chemical equations?

H₂ + O₂ → H₂O 🤔
Left: 2 H, 2 O · Right: 2 H, 1 O → an oxygen atom "vanished"?! ❌

Law of Conservation of Mass: atoms are never created or destroyed — only rearranged 🔄

Balanced ✅: 2H₂ + O₂ → 2H₂O (4 H and 2 O on each side)
Atoms in = atoms out → mass in = mass out.

Chemical Reactions and Equations — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #BalancingEquations #ConservationOfMass #Class10Science #Chemistry #CBSE #BoardExams"""

H_COL, O_COL = WHITE, PINK


def h2(dax, x, y, a, z=6):
    for dx in (-0.2, 0.2):
        dax.add_patch(Circle((x + dx, y), 0.2, facecolor=H_COL, edgecolor=NAVY, lw=2, alpha=a, zorder=z))


def o2(dax, x, y, a, z=6):
    for dx in (-0.27, 0.27):
        dax.add_patch(Circle((x + dx, y), 0.3, facecolor=O_COL, edgecolor=NAVY, lw=2, alpha=a, zorder=z))


def h2o(dax, x, y, a, z=6):
    dax.add_patch(Circle((x, y), 0.3, facecolor=O_COL, edgecolor=NAVY, lw=2, alpha=a, zorder=z))
    for dx in (-0.3, 0.3):
        dax.add_patch(Circle((x + dx, y - 0.25), 0.19, facecolor=H_COL, edgecolor=NAVY, lw=2, alpha=a, zorder=z + 1))


def tally(dax, x, y, h, o, a, ok=None):
    col = WHITE if ok is None else (GREEN if ok else PINK)
    outline(dax.text(x, y, f"H: {h}   O: {o}", ha="center", fontsize=24, color=col, fontweight="bold", alpha=a, zorder=8))


def draw(c):
    dax = c.area(0.0, 0.1, 7.0)
    a0 = ease(c.phase("hook", 0.1, 0.45))
    fx = ease(c.phase("fix", 0.0, 0.3))
    law = ease(c.phase("law", 0.0, 0.25)) * (1 - fx)
    arr_a = a0
    dax.add_patch(FancyArrowPatch((-0.45, 0.9), (0.55, 0.9), arrowstyle="-|>", mutation_scale=34, color=GOLD, lw=4,
                                  alpha=arr_a, zorder=5))
    # unbalanced version
    ua = a0 * (1 - fx)
    if ua > 0.01:
        h2(dax, -2.8, 0.9, ua); outline(dax.text(-2.1, 0.9, "+", ha="center", va="center", fontsize=34, color=WHITE,
                                                 fontweight="bold", alpha=ua, zorder=7))
        o2(dax, -1.25, 0.9, ua)
        vanish = ease(c.phase("count", 0.4, 0.8))
        h2o(dax, 1.6, 0.95, ua)
        # the "missing" oxygen, a ghost with a question mark
        if vanish > 0:
            dax.add_patch(Circle((2.75, 0.95), 0.3, fill=False, edgecolor=PINK, lw=3, ls=(0, (4, 3)), alpha=vanish * ua,
                                 zorder=6))
            outline(dax.text(2.75, 0.95, "?", ha="center", va="center", fontsize=30, color=PINK, fontweight="bold",
                             alpha=vanish * ua, zorder=7))
        ta = ease(c.phase("unbal", 0.2, 0.6)) * ua
        tally(dax, -2.0, -0.1, 2, 2, ta)
        tb = ease(c.phase("count", 0.1, 0.4)) * ua
        tally(dax, 1.75, -0.1, 2, 1, tb, ok=False)
        if tb > 0:
            outline(dax.text(0, -0.85, "1 oxygen atom missing!", ha="center", fontsize=24, color=PINK,
                             fontweight="bold", alpha=tb * (1 - law), zorder=8))
    if law > 0.01:
        dax.add_patch(FancyBboxPatch((-3.0, -2.35), 6.0, 1.35, boxstyle="round,pad=0,rounding_size=0.2",
                                     facecolor="#13264d", edgecolor=GOLD, lw=3, alpha=law, zorder=6))
        outline(dax.text(0, -1.45, "Conservation of Mass", ha="center", va="center", fontsize=26, color=GOLD,
                         fontweight="bold", alpha=law, zorder=7))
        dax.text(0, -1.95, "atoms are never created or destroyed", ha="center", va="center", fontsize=20,
                 color=LTGREY, alpha=law, zorder=7)
    if fx > 0.01:
        outline(dax.text(-3.35, 1.7, "2", ha="center", va="center", fontsize=36, color=GOLD, fontweight="bold",
                         alpha=fx, zorder=7))
        h2(dax, -2.8, 1.25, fx); h2(dax, -2.8, 0.55, fx)
        outline(dax.text(-2.1, 0.9, "+", ha="center", va="center", fontsize=34, color=WHITE, fontweight="bold",
                         alpha=fx, zorder=7))
        o2(dax, -1.25, 0.9, fx)
        outline(dax.text(0.95, 1.75, "2", ha="center", va="center", fontsize=36, color=GOLD, fontweight="bold",
                         alpha=fx, zorder=7))
        h2o(dax, 1.75, 1.35, fx); h2o(dax, 1.75, 0.45, fx)
        tt = ease(c.phase("fix", 0.4, 0.7))
        tally(dax, -2.0, -0.35, 4, 2, tt, ok=True)
        tally(dax, 1.75, -0.35, 4, 2, tt, ok=True)
        outline(dax.text(0, -1.25, "$2H_2 + O_2 \\rightarrow 2H_2O$", ha="center", fontsize=34, color=WHITE,
                         alpha=tt, zorder=8))
    c.steps([("atoms in  =  atoms out", 0.0, WHITE),
             ("mass of reactants = mass of products", 0.3, GOLD)], ys=(0.345, 0.285))
