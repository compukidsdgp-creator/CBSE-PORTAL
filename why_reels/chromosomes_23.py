"""WHY? — Why do egg and sperm have only 23 chromosomes?  (Class 10 & 12 Biology · Reproduction)"""
import math
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Ellipse
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why do egg & sperm have only 23 chromosomes?"
TAGS = "Class 10 & 12 Biology"
BEATS = [
    ("hook",   "Your body cells have forty six chromosomes. So why do egg and sperm cells have only twenty three?",
               "Body cells have 46 chromosomes. So why do egg and sperm have only 23?", 4.8),
    ("cell",   "A normal human cell holds forty six chromosomes, arranged in twenty three pairs.",
               "A normal human cell: 46 chromosomes in 23 PAIRS.", 4.0),
    ("problem","If egg and sperm also had forty six, the baby would get ninety two. The next generation, one eighty four! Far too many.",
               "If egg and sperm had 46 each → baby gets 92 → next generation 184! Far too many.", 6.0),
    ("meiosis","So gametes are made by meiosis, a special division that halves the number. One chromosome from each pair.",
               "So gametes are made by MEIOSIS — it halves the number: one from each pair.", 5.6),
    ("fert",   "When sperm meets egg, twenty three plus twenty three makes forty six again. Balance restored!",
               "Sperm (23) + egg (23) = 46 again. Balance restored!", 4.8),
    ("math",   "Gametes are haploid, with n equals twenty three. The zygote is diploid, with two n equals forty six.",
               "Gametes: n = 23 (haploid) · Zygote: 2n = 46 (diploid)", 5.0),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧬 WHY? — Why do egg & sperm have only 23 chromosomes?

Body cells: 46 chromosomes in 23 pairs
If gametes had 46 → baby 92 → next generation 184! 😵
So gametes are made by MEIOSIS — it halves the number (one from each pair)
Sperm 23 + egg 23 = 46 again ✅ balance restored

Gametes: n = 23 (haploid) · Zygote: 2n = 46 (diploid)
Class 10 & 12 Biology — Reproduction. 🧠

💾 Save it · 📤 Share with your bio group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Biology #Meiosis #Chromosomes #Class10Science #Class12Biology #CBSE"""

PAIR_COLS = [CYAN, PINK, GOLD, GREEN, PURPLE, "#ff9f43"]
END_Y = 0.395


def chrom(dax, x, y, col, a, s=1.0, ang=0.0, z=6):
    """An X-shaped chromosome."""
    for d in (-1, 1):
        t = math.radians(ang + d * 18)
        dx, dy = 0.28 * s * math.sin(t), 0.28 * s * math.cos(t)
        dax.plot([x - dx, x + dx], [y - dy, y + dy], color=col, lw=6 * s, alpha=a, solid_capstyle="round", zorder=z)


def cell(dax, x, y, r, a, pairs, z=4, label=None, lab_col=WHITE, single=False, rot=0.0):
    dax.add_patch(Circle((x, y), r, facecolor="#13264d", edgecolor=CYAN, lw=3, alpha=a, zorder=z))
    n = len(pairs)
    for k, col in enumerate(pairs):
        ang = 2 * math.pi * k / n + rot
        rr = r * 0.52
        px, py = x + rr * math.cos(ang), y + rr * math.sin(ang)
        chrom(dax, px - (0 if single else 0.13 * r), py, col, a, s=r / 1.3, ang=15 * k, z=z + 1)
        if not single:
            chrom(dax, px + 0.13 * r, py, col, a, s=r / 1.3, ang=-15 * k, z=z + 1)
    if label:
        outline(dax.text(x, y - r - 0.35, label, ha="center", fontsize=24, fontweight="bold", color=lab_col, alpha=a,
                         zorder=z + 3))


def draw(c):
    dax = c.area(0.0, 0.0, 7.6)
    # 1) a body cell with pairs
    ca = ease(c.phase("cell", 0.0, 0.35)) * (1 - ease(c.phase("problem", 0.0, 0.2)))
    ha = ease(c.phase("hook", 0.2, 0.6)) * (1 - ease(c.phase("problem", 0.0, 0.2)))
    if max(ca, ha) > 0:
        cell(dax, 0, 0.5, 1.85, max(ca, ha), PAIR_COLS, label="body cell: 46 (23 pairs)")
        if ca > 0:
            outline(dax.text(2.4, 2.1, "pairs ✓", ha="center", fontsize=24, fontweight="bold", color=GOLD, alpha=ca, zorder=8))
    # 2) the doubling problem
    pa = ease(c.phase("problem", 0.1, 0.35)) * (1 - ease(c.phase("meiosis", 0.0, 0.2)))
    if pa > 0:
        vals = [("46 + 46", "92", 0.15), ("92 + 92", "184", 0.5)]
        for k, (s, v, at) in enumerate(vals):
            a = ease(c.phase("problem", at, at + 0.2)) * pa
            if a > 0:
                y = 1.5 - k * 1.7
                outline(dax.text(-0.4, y, s, ha="right", va="center", fontsize=38, fontweight="bold", color=WHITE,
                                 alpha=a, zorder=7))
                outline(dax.text(0.2, y, "→ " + v, ha="left", va="center", fontsize=48, fontweight="bold",
                                 color=PINK, alpha=a, zorder=7))
                outline(dax.text(0, y - 0.65, ["baby", "next generation"][k], ha="center", fontsize=22, color=LTGREY,
                                 alpha=a, zorder=7))
        xa = back_out(c.phase("problem", 0.75, 0.95))
        if xa > 0.01:
            outline(dax.text(0, -2.35, "✗ too many!", ha="center", fontsize=34 * min(1, xa), fontweight="bold",
                             color=PINK, zorder=8))
    # 3) meiosis: one cell → four cells with half
    ma = ease(c.phase("meiosis", 0.05, 0.3)) * (1 - ease(c.phase("fert", 0.0, 0.2)))
    if ma > 0:
        sp = ease(c.phase("meiosis", 0.3, 0.8))
        if sp < 0.05:
            cell(dax, 0, 0.5, 1.5, ma, PAIR_COLS, label="46")
        else:
            for k in range(4):
                ang = math.radians(45 + 90 * k)
                x, y = 2.0 * sp * math.cos(ang), 0.5 + 1.55 * sp * math.sin(ang)
                cell(dax, x, y, 0.9, ma, PAIR_COLS, single=True, label="23", lab_col=GOLD, rot=k * 0.4)
            outline(dax.text(0, 0.5, "meiosis", ha="center", va="center", fontsize=26, fontweight="bold", color=CYAN,
                             alpha=ma * ease(c.phase("meiosis", 0.6, 0.9)), zorder=9))
    # 4) fertilisation
    fa = ease(c.phase("fert", 0.05, 0.3))
    if fa > 0:
        mv = ease(c.phase("fert", 0.2, 0.6))
        egg_x = 0.9
        dax.add_patch(Circle((egg_x, 0.6), 1.4, facecolor="#2a1d3d", edgecolor=PINK, lw=3, alpha=fa, zorder=3))
        outline(dax.text(egg_x, 2.25, "egg: 23", ha="center", fontsize=26, fontweight="bold", color=PINK, alpha=fa, zorder=8))
        sx = lerp(-3.3, egg_x - 1.35, mv)
        dax.add_patch(Ellipse((sx, 0.6), 0.6, 0.38, color=CYAN, alpha=fa, zorder=6))
        tail = np.linspace(0, 1.4, 40)
        dax.plot(sx - 0.3 - tail, 0.6 + 0.12 * np.sin(tail * 9 - c.t * 12), color=CYAN, lw=3, alpha=fa, zorder=5)
        outline(dax.text(sx - 0.6, 1.25, "sperm: 23", ha="center", fontsize=24, fontweight="bold", color=CYAN,
                         alpha=fa * (1 - mv * 0.6), zorder=8))
        za = back_out(c.phase("fert", 0.6, 0.85))
        if za > 0.01:
            outline(dax.text(egg_x, 0.6, "46", ha="center", va="center", fontsize=60 * min(1, za), fontweight="bold",
                             color=GREEN, zorder=9))
            outline(dax.text(egg_x, -1.15, "zygote ✓", ha="center", fontsize=28, fontweight="bold", color=GREEN,
                             alpha=min(1, za), zorder=9))
    c.steps([("gametes: n = 23 (haploid)", 0.05, CYAN), ("zygote: 2n = 46 (diploid)", 0.4, GOLD)], ys=(0.345, 0.282))
