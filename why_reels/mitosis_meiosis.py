"""WHY? — Why does mitosis make identical cells but meiosis makes variation?  (Class 10 How do Organisms Reproduce)"""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why is MITOSIS a copy but MEIOSIS a shuffle?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",    "Your skin cells are perfect copies of each other. But no two of your egg or sperm cells are the same. Why?",
                "Skin cells are perfect COPIES… but no two egg or sperm cells are the SAME. Why?", 5.0),
    ("mitosis", "Mitosis copies every chromosome, then splits once. Two cells, identical to the parent. Perfect for growth and repair.",
                "MITOSIS: copy every chromosome, split ONCE → 2 IDENTICAL cells. For growth & repair.", 6.0),
    ("meiosis", "Meiosis splits twice. Four cells, each with only half the chromosomes, one from each pair.",
                "MEIOSIS: split TWICE → 4 cells, each with HALF the chromosomes (one from each pair).", 5.4),
    ("shuffle", "Which one of each pair goes where is random. And paired chromosomes swap pieces, called crossing over. "
                "So every cell is a new mix.",
                "Which one of each pair goes where is RANDOM, and pairs SWAP pieces (crossing over) → every cell is a new mix.", 6.6),
    ("why",     "Variation means some offspring may survive when the environment changes.",
                "VARIATION: some offspring may survive when the environment changes.", 4.0),
    ("math",    "Mitosis, two n to two n, identical. Meiosis, two n to n, varied.",
                "Mitosis: 2n → 2n, identical.  Meiosis: 2n → n, varied.", 4.2),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧬 WHY? — Why does MITOSIS make identical cells but MEIOSIS makes variation?

Mitosis 🪞: copy every chromosome → split once → 2 identical cells (2n → 2n)
➡️ growth, repair

Meiosis 🎲: split twice → 4 cells with half the chromosomes (2n → n)
➡️ random sorting of each pair + crossing over (pairs swap pieces)
➡️ every gamete is a new mix!

Variation helps a species survive when the environment changes 🌍

How do Organisms Reproduce / Heredity — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Mitosis #Meiosis #Variation #Class10Science #Heredity #CBSE"""

A1, A2, B1, B2 = PINK, CYAN, "#ff9f43", "#5b8cff"   # pair A (long), pair B (short): mum's vs dad's


def chrom(dax, x, y, L, col, a, col2=None, frac=0.5, z=7):
    """A chromosome bar; optional second colour for the crossed-over tip."""
    if a <= 0.01:
        return
    dax.plot([x, x], [y - L / 2, y + L / 2], color=col, lw=9, alpha=a, zorder=z, solid_capstyle="round")
    if col2:
        dax.plot([x, x], [y + L / 2 - L * frac, y + L / 2], color=col2, lw=9, alpha=a, zorder=z + 0.1,
                 solid_capstyle="round")


def cell(dax, x, y, r, a, chroms, z=5):
    if a <= 0.01:
        return
    dax.add_patch(Circle((x, y), r, facecolor="#123a2a", edgecolor=GREEN, lw=3, alpha=a, zorder=z))
    n = len(chroms)
    for i, (L, col, col2) in enumerate(chroms):
        cx = x + (i - (n - 1) / 2) * min(0.28, 1.3 * r / max(n, 1))
        chrom(dax, cx, y, L * r / 0.9, col, a, col2)


PARENT = [(0.9, A1, None), (0.9, A2, None), (0.5, B1, None), (0.5, B2, None)]


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    a0 = ease(c.phase("hook", 0.05, 0.35))
    me = ease(c.phase("meiosis", 0.0, 0.25))
    wy = ease(c.phase("why", 0.0, 0.25))
    ma = ease(c.phase("math", 0.0, 0.3))
    mi = a0 * (1 - me)
    if mi > 0.01:
        sp = ease(c.phase("mitosis", 0.2, 0.7))
        if sp < 0.99:
            cell(dax, 0, 1.2, 0.9, mi * (1 - sp), PARENT)
        for s in (-1, 1):
            cell(dax, s * lerp(0, 1.5, sp), lerp(1.2, -0.5, sp), 0.8, mi * sp, PARENT)
        if sp > 0:
            outline(dax.text(0, -1.75, "2 identical cells", ha="center", fontsize=26, color=GREEN, fontweight="bold",
                             alpha=mi * sp, zorder=9))
            outline(dax.text(0, 2.45, "MITOSIS = copy", ha="center", fontsize=26, color=WHITE, fontweight="bold",
                             alpha=mi * sp, zorder=9))
    if me > 0.01:
        m = me * (1 - wy)
        sp = ease(c.phase("meiosis", 0.2, 0.8))
        sh = ease(c.phase("shuffle", 0.2, 0.6))
        cell(dax, 0, 1.75, 0.6, m * (1 - 0.6 * sp), PARENT)
        gametes = [[(0.9, A1, A2 if sh > 0.5 else None), (0.5, B1, None)],
                   [(0.9, A2, A1 if sh > 0.5 else None), (0.5, B2, None)],
                   [(0.9, A1, None), (0.5, B2, B1 if sh > 0.5 else None)],
                   [(0.9, A2, None), (0.5, B1, None)]]
        for k, g in enumerate(gametes):
            x = -2.55 + 1.7 * k
            dax.add_patch(FancyArrowPatch((0, 1.1), (x, 0.25), arrowstyle="-|>", mutation_scale=18, color=LTGREY, lw=2,
                                          alpha=m * sp * 0.6, zorder=4))
            cell(dax, x, -0.45, 0.65, m * ease(c.phase("meiosis", 0.4 + 0.08 * k, 0.6 + 0.08 * k)), g)
        outline(dax.text(0, -1.5, "4 cells · half the chromosomes", ha="center", fontsize=23, color=GOLD,
                         fontweight="bold", alpha=m * sp * (1 - ease(c.phase("shuffle", 0.0, 0.15))), zorder=9))
        if c.phase("shuffle", 0.15, 0.3) > 0:
            outline(dax.text(0, -1.5, "random sort + crossing over", ha="center", fontsize=23, color=PINK,
                             fontweight="bold", alpha=m * sh, zorder=9))
            outline(dax.text(0, -2.05, "every cell different!", ha="center", fontsize=23, color=WHITE,
                             fontweight="bold", alpha=m * sh, zorder=9))
    if wy > 0.01:
        w = wy * (1 - ma)
        rng = np.random.default_rng(6)
        cols = [PINK, CYAN, GOLD, GREEN, PURPLE, "#ff9f43"]
        hot = ease(c.phase("why", 0.3, 0.7))
        for k in range(12):
            x, y = -2.5 + 1.0 * (k % 6), 1.3 - 1.4 * (k // 6)
            col = cols[rng.integers(0, 6)]
            surv = (k % 3 == 0)
            dax.add_patch(Circle((x, y), 0.35, facecolor=col, edgecolor=WHITE, lw=2,
                                 alpha=w * (1 if surv or hot < 0.5 else 0.2), zorder=6))
        outline(dax.text(0, -1.4, "change comes → some still survive", ha="center", fontsize=22, color=GREEN,
                         fontweight="bold", alpha=w * hot, zorder=9))
        outline(dax.text(0, 2.35, "variety = survival", ha="center", fontsize=26, color=GOLD, fontweight="bold",
                         alpha=w, zorder=9))
    if ma > 0.01:
        outline(dax.text(0, 0.9, "mitosis: 2n → 2n (copy)", ha="center", fontsize=32, color=GREEN, fontweight="bold",
                         alpha=ma, zorder=9))
        outline(dax.text(0, -0.3, "meiosis: 2n → n (shuffle)", ha="center", fontsize=32, color=PINK, fontweight="bold",
                         alpha=ease(c.phase("math", 0.3, 0.6)), zorder=9))
    c.steps([("mitosis: identical copies", 0.0, WHITE),
             ("meiosis: half + shuffled", 0.3, GOLD)], ys=(0.345, 0.285))
