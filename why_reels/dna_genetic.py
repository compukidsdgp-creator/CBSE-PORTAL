"""WHY? — Why is DNA the genetic material and not protein?  (Class 12 Molecular Basis of Inheritance)"""
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, RegularPolygon
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why is DNA the genetic material, not PROTEIN?"
TAGS = "Class 12 Biology"
BEATS = [
    ("hook",    "Chromosomes contain both DNA and protein. So which one actually carries the genes? "
                "Scientists once bet on protein!",
                "Chromosomes have BOTH DNA and protein. Which carries the genes? Many bet on PROTEIN!", 5.4),
    ("phage",   "In nineteen fifty two, Hershey and Chase used a virus that infects bacteria. "
                "It's just DNA inside a protein coat.",
                "1952, Hershey & Chase: a virus that infects bacteria — DNA inside a PROTEIN coat.", 5.6),
    ("label",   "They tagged the DNA with radioactive phosphorus, and the protein with radioactive sulphur.",
                "They tagged DNA with radioactive PHOSPHORUS, protein with radioactive SULPHUR.", 5.0),
    ("inject",  "The virus injected only its DNA into the bacteria. The protein coat stayed outside. "
                "Yet new viruses were made inside!",
                "Only the DNA went INTO the bacteria. The protein stayed OUTSIDE — yet new viruses formed!", 6.0),
    ("traits",  "DNA is also stable, copies itself accurately, and can change slowly by mutation. "
                "Perfect for carrying information.",
                "DNA is also STABLE, COPIES itself accurately and can MUTATE slowly — perfect for genes.", 5.8),
    ("math",    "Hershey and Chase proved it. DNA is the genetic material.",
                "Hershey & Chase (1952): DNA is the genetic material.", 3.8),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧬 WHY? — Why is DNA the genetic material and not protein?

Chromosomes contain both DNA and protein — which carries the genes? 🤔

Hershey & Chase, 1952 🧪
• Virus (bacteriophage) = DNA inside a protein coat
• DNA tagged with radioactive ³²P, protein with radioactive ³⁵S
• Only ³²P (DNA) entered the bacteria — the protein coat stayed outside ✅
• New viruses were made → DNA carries the instructions!

DNA is also stable, replicates accurately and can mutate slowly. 🔁

Molecular Basis of Inheritance — Class 12 Biology. 📗

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #DNA #HersheyChase #Class12Biology #MolecularBasisOfInheritance #NEET #CBSE"""


def phage(dax, x, y, a, dna_a=1.0, coat_col=PINK, dna_col=CYAN, empty=False):
    dax.add_patch(RegularPolygon((x, y), 6, radius=0.48, orientation=np.pi / 6, facecolor="#2a1530",
                                 edgecolor=coat_col, lw=3.5, alpha=a, zorder=6))
    if not empty:
        t = np.linspace(0, 4 * np.pi, 80)
        dax.plot(x + 0.25 * np.sin(t), y - 0.3 + 0.6 * t / (4 * np.pi), color=dna_col, lw=3, alpha=a * dna_a, zorder=7)
    dax.plot([x, x], [y - 0.48, y - 1.15], color=coat_col, lw=7, alpha=a, zorder=5)
    for s in (-1, 1):
        dax.plot([x, x + s * 0.45], [y - 1.15, y - 1.5], color=coat_col, lw=3, alpha=a, zorder=5)


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    a_hook = ease(c.phase("hook", 0.05, 0.3)) * (1 - ease(c.phase("phage", 0.0, 0.25)))
    if a_hook > 0.01:
        for x, s, col in ((-1.6, "DNA", CYAN), (1.6, "PROTEIN", PINK)):
            dax.add_patch(FancyBboxPatch((x - 1.3, -0.6), 2.6, 1.6, boxstyle="round,pad=0,rounding_size=0.2",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=a_hook, zorder=5))
            dax.text(x, 0.2, s, ha="center", va="center", fontsize=32, color=col, fontweight="bold", alpha=a_hook, zorder=6)
        outline(dax.text(0, 0.2, "vs", ha="center", va="center", fontsize=28, color=WHITE, fontweight="bold",
                         alpha=a_hook, zorder=7))
        outline(dax.text(0, -1.3, "which one carries genes?", ha="center", fontsize=24, color=GOLD, fontweight="bold",
                         alpha=a_hook * ease(c.phase("hook", 0.4, 0.7)), zorder=7))
    tr = ease(c.phase("traits", 0.0, 0.25))
    pa = ease(c.phase("phage", 0.0, 0.3)) * (1 - tr)
    if pa > 0.01:
        lab = ease(c.phase("label", 0.1, 0.45))
        inj = ease(c.phase("inject", 0.1, 0.6))
        # bacterium
        dax.add_patch(Ellipse((0.0, -1.6), 5.2, 1.6, facecolor="#1d3b2a", edgecolor=GREEN, lw=4, alpha=pa, zorder=4))
        outline(dax.text(-1.9, -1.6, "bacterium", ha="center", va="center", fontsize=19, color=GREEN, fontweight="bold",
                         alpha=pa, zorder=8))
        coat_col = PINK if lab == 0 else PINK
        phage(dax, 0.0, 0.85 - 0.0, pa, dna_a=1 - inj, empty=inj > 0.95)
        if lab > 0:
            outline(dax.text(-1.3, 1.25, "DNA: ³²P", ha="right", va="center", fontsize=22, color=CYAN, fontweight="bold",
                             alpha=lab * pa, zorder=8))
            outline(dax.text(1.3, 1.25, "protein: ³⁵S", ha="left", va="center", fontsize=22, color=PINK,
                             fontweight="bold", alpha=lab * pa, zorder=8))
            for k in range(6):            # radioactive sparkle
                ang = c.t * 2 + k
                dax.add_patch(Circle((0.75 * np.cos(ang), 0.85 + 0.75 * np.sin(ang)), 0.05, color=GOLD,
                                     alpha=0.7 * lab * pa * (1 - inj), zorder=8))
        if inj > 0:
            # DNA strand travelling down the tail and into the cell
            t = np.linspace(0, 4 * np.pi, 80)
            yy = lerp(0.6, -1.6, inj)
            dax.plot(0.3 * np.sin(t) * inj + 0.0, yy - 0.3 + 0.5 * t / (4 * np.pi), color=CYAN, lw=3, alpha=pa, zorder=7)
            na = ease(c.phase("inject", 0.6, 0.9)) * pa
            for x in (1.2, 1.9):
                phage(dax, x, -1.15, na * 0.9, coat_col=GOLD, dna_col=CYAN)
                pass
            outline(dax.text(0, 2.3, "only DNA went in ✓", ha="center", fontsize=24, color=CYAN, fontweight="bold",
                             alpha=ease(c.phase("inject", 0.3, 0.6)) * pa, zorder=9))
    if tr > 0.01:
        ta = tr * (1 - ease(c.phase("math", 0.0, 0.3)))
        items = (("stable", CYAN), ("copies accurately", GREEN), ("mutates slowly", PURPLE))
        for k, (s, col) in enumerate(items):
            a = ta * ease(c.phase("traits", 0.15 + 0.2 * k, 0.35 + 0.2 * k))
            y = 1.5 - 1.2 * k
            dax.add_patch(FancyBboxPatch((-2.4, y - 0.42), 4.8, 0.84, boxstyle="round,pad=0,rounding_size=0.2",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=a, zorder=5))
            dax.text(0, y, "✓ " + s, ha="center", va="center", fontsize=28, color=col, fontweight="bold", alpha=a, zorder=6)
    ma = ease(c.phase("math", 0.0, 0.35))
    if ma > 0.01:
        # DNA double helix
        t = np.linspace(-3.0, 3.0, 200)
        dax.plot(t, 0.55 * np.sin(t * 2.2 + c.t), color=CYAN, lw=5, alpha=ma, zorder=5)
        dax.plot(t, -0.55 * np.sin(t * 2.2 + c.t), color=PINK, lw=5, alpha=ma, zorder=5)
        for x in np.linspace(-2.8, 2.8, 15):
            yv = 0.55 * np.sin(x * 2.2 + c.t)
            dax.plot([x, x], [yv, -yv], color=LTGREY, lw=2, alpha=ma * 0.7, zorder=4)
    c.steps([("Hershey & Chase, 1952", 0.0, WHITE),
             ("DNA = genetic material", 0.3, GOLD)], ys=(0.345, 0.285))
