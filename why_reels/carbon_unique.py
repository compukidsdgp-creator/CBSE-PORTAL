"""WHY? — Why does carbon form so many compounds?  (Class 10 Carbon and its Compounds)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does CARBON form millions of compounds?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",   "Scientists know millions of carbon compounds. More than all other elements put together. "
               "What makes carbon so special?",
               "MILLIONS of carbon compounds — more than all other elements combined! Why carbon?", 5.2),
    ("four",   "First, tetravalency. A carbon atom has four electrons to share, so it makes four bonds.",
               "TETRAVALENCY: carbon has 4 electrons to share → makes 4 bonds.", 4.8),
    ("chain",  "Second, catenation. Carbon atoms link to other carbon atoms, forming long chains.",
               "CATENATION: carbon links to carbon → long CHAINS.", 4.4),
    ("shapes", "These chains can be straight, branched, or even closed rings.",
               "Chains can be STRAIGHT, BRANCHED, or closed RINGS.", 3.8),
    ("strong", "And because carbon is so small, its bonds are very strong. The compounds stay stable.",
               "Carbon is SMALL → its bonds are STRONG → compounds stay stable.", 4.6),
    ("math",   "Four bonds, plus self linking, gives endless combinations.",
               "4 bonds + self-linking = endless combinations!", 3.6),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """⚫ WHY? — Why does CARBON form millions of compounds?

1️⃣ Tetravalency: 4 valence electrons → 4 covalent bonds
2️⃣ Catenation: carbon bonds to carbon → long chains 🔗
Straight ➖ branched 🌿 or rings ⭕
3️⃣ Small size → strong, stable bonds 💪

4 bonds + self-linking = endless combinations ♾️

Carbon and its Compounds — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Catenation #Tetravalency #Class10Science #CarbonCompounds #CBSE #BoardExams"""


def atom(dax, x, y, a, col=GOLD, lab="C", r=0.3, z=6):
    if a <= 0.01:
        return
    dax.add_patch(Circle((x, y), r, facecolor="#2b2b2b", edgecolor=col, lw=3, alpha=a, zorder=z))
    dax.text(x, y, lab, ha="center", va="center", fontsize=20 if r >= 0.3 else 13, color=col, fontweight="bold",
             alpha=a, zorder=z + 1)


def bond(dax, p, q, a, col=LTGREY):
    if a > 0.01:
        dax.plot([p[0], q[0]], [p[1], q[1]], color=col, lw=5, alpha=a, zorder=4)


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    # hook: a counter
    ha = ease(c.phase("hook", 0.05, 0.3)) * (1 - ease(c.phase("four", 0.0, 0.25)))
    if ha > 0.01:
        n = int(10_000_000 * ease(c.phase("hook", 0.1, 0.8)))
        outline(dax.text(0, 0.5, f"{n:,}+", ha="center", va="center", fontsize=58, color=GOLD, fontweight="bold",
                         alpha=ha, zorder=7))
        dax.text(0, -0.45, "known carbon compounds", ha="center", fontsize=24, color=LTGREY, alpha=ha, zorder=7,
                 fontweight="bold")
    # tetravalency
    fa = ease(c.phase("four", 0.0, 0.3)) * (1 - ease(c.phase("chain", 0.0, 0.25)))
    if fa > 0.01:
        atom(dax, 0, 0.1, fa, r=0.45)
        for k in range(4):
            ang = np.pi / 4 + k * np.pi / 2
            b = ease(c.phase("four", 0.25 + 0.12 * k, 0.4 + 0.12 * k)) * fa
            p, q = (0.45 * np.cos(ang), 0.1 + 0.45 * np.sin(ang)), (1.35 * np.cos(ang), 0.1 + 1.35 * np.sin(ang))
            bond(dax, p, q, b, CYAN)
            atom(dax, 1.6 * np.cos(ang), 0.1 + 1.6 * np.sin(ang), b, col=WHITE, lab="H", r=0.24)
        outline(dax.text(0, -2.1, "4 bonds", ha="center", fontsize=28, color=CYAN, fontweight="bold",
                         alpha=ease(c.phase("four", 0.7, 0.9)) * fa, zorder=8))
    # catenation: chain grows
    ca = ease(c.phase("chain", 0.0, 0.25)) * (1 - ease(c.phase("shapes", 0.0, 0.2)))
    if ca > 0.01:
        n = 1 + int(6 * ease(c.phase("chain", 0.1, 0.8)))
        xs = [-2.7 + 0.9 * k for k in range(7)]
        for k in range(n):
            y = 0.25 * (1 if k % 2 else -1)
            atom(dax, xs[k], y, ca)
            if k:
                bond(dax, (xs[k - 1], -y), (xs[k], y), ca)
        outline(dax.text(0, -1.4, "C–C–C–C… chains", ha="center", fontsize=26, color=GOLD, fontweight="bold",
                         alpha=ca, zorder=8))
    # shapes: straight, branched, ring
    sa = ease(c.phase("shapes", 0.0, 0.3)) * (1 - ease(c.phase("math", 0.0, 0.25)))
    if sa > 0.01:
        a1 = ease(c.phase("shapes", 0.05, 0.3)) * sa
        a2 = ease(c.phase("shapes", 0.3, 0.55)) * sa
        a3 = ease(c.phase("shapes", 0.55, 0.8)) * sa
        # straight (top)
        pts = [(-1.6 + 0.8 * k, 1.75) for k in range(5)]
        for k, p in enumerate(pts):
            atom(dax, *p, a1, r=0.25)
            if k:
                bond(dax, pts[k - 1], p, a1)
        outline(dax.text(-2.6, 1.75, "straight", ha="right", va="center", fontsize=19, color=LTGREY,
                         fontweight="bold", alpha=a1, zorder=8))
        # branched (bottom left)
        bp = [(-2.6, -0.6), (-1.8, -0.6), (-1.0, -0.6), (-1.8, 0.2), (-1.0, -1.4)]
        for p in bp:
            atom(dax, *p, a2, r=0.25)
        for i, j in ((0, 1), (1, 2), (1, 3), (2, 4)):
            bond(dax, bp[i], bp[j], a2)
        outline(dax.text(-1.8, -2.1, "branched", ha="center", fontsize=19, color=LTGREY, fontweight="bold",
                         alpha=a2, zorder=8))
        # ring (bottom right)
        rp = [(1.7 + 0.85 * np.cos(np.pi / 2 + k * np.pi / 3), -0.8 + 0.85 * np.sin(np.pi / 2 + k * np.pi / 3))
              for k in range(6)]
        for k, p in enumerate(rp):
            atom(dax, *p, a3, r=0.25)
            bond(dax, rp[k - 1], p, a3)
        outline(dax.text(1.7, -2.1, "ring", ha="center", fontsize=19, color=LTGREY, fontweight="bold", alpha=a3,
                         zorder=8))
        st = ease(c.phase("strong", 0.1, 0.4))
        if st > 0:
            outline(dax.text(1.7, 0.75, "small atom →\nstrong bonds", ha="center", va="center", fontsize=21,
                             color=GREEN, fontweight="bold", alpha=st * sa, zorder=9))
    ma = ease(c.phase("math", 0.0, 0.3))
    if ma > 0.01:
        for k, (s, col) in enumerate((("4 bonds", CYAN), ("+", WHITE), ("catenation", GOLD))):
            outline(dax.text(-2.1 + 2.1 * k, 0.3, s, ha="center", va="center", fontsize=30, color=col,
                             fontweight="bold", alpha=ma, zorder=8))
        outline(dax.text(0, -0.8, "= ∞ combinations", ha="center", fontsize=34, color=GREEN, fontweight="bold",
                         alpha=ease(c.phase("math", 0.3, 0.6)), zorder=8))
    c.steps([("tetravalency + catenation", 0.0, WHITE),
             ("millions of compounds", 0.3, GOLD)], ys=(0.345, 0.285))
