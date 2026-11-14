"""WHY? — Why only 2 ATP without oxygen but 38 with it?  (Class 10 Life Processes: Respiration)"""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle, RegularPolygon
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why 2 ATP without oxygen, but 38 WITH it?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",    "One glucose gives just two A T P without oxygen. With oxygen, thirty eight! Same sugar. Why the huge difference?",
                "One glucose: 2 ATP without oxygen… 38 WITH oxygen! Same sugar — why?", 5.0),
    ("glyco",   "Both start the same way. In the cytoplasm, glucose splits into two pyruvate. That gives two A T P.",
                "Both start the same: in the CYTOPLASM, glucose → 2 pyruvate. That gives 2 ATP.", 5.4),
    ("noo2",    "Without oxygen, it stops there. Pyruvate becomes lactic acid in muscles, or alcohol in yeast. "
                "Most energy stays locked inside.",
                "No oxygen → it STOPS: lactic acid (muscles) or alcohol (yeast). Most energy stays LOCKED inside.", 6.2),
    ("o2",      "With oxygen, pyruvate goes into the mitochondria and is broken down completely, into carbon dioxide and water. "
                "Thirty six more A T P!",
                "With oxygen → MITOCHONDRIA break pyruvate down fully to CO₂ + H₂O → 36 MORE ATP!", 6.6),
    ("both",    "So why keep the anaerobic route? It's a quick backup. When you sprint and oxygen runs short, "
                "your muscles still get some energy.",
                "Why keep anaerobic? A quick BACKUP: when you sprint and oxygen runs short, muscles still get energy.", 6.4),
    ("math",    "Partial breakdown, two A T P. Complete breakdown, thirty eight A T P.",
                "Partial breakdown: 2 ATP.  Complete breakdown: 38 ATP.", 4.0),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """⚡ WHY? — Why only 2 ATP without oxygen but 38 with it?

Step 1 (both): glucose → 2 pyruvate in the cytoplasm → 2 ATP

❌ No oxygen: stops here → lactic acid (muscles) / ethanol + CO₂ (yeast)
Most energy stays locked inside 🔒

✅ With oxygen: pyruvate → mitochondria → fully broken down to CO₂ + H₂O → 36 more ATP!
Total 38 ATP 🔋

Why keep anaerobic respiration? A quick backup when oxygen runs short — like sprinting 🏃 (muscle cramps = lactic acid!)

Life Processes: Respiration — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Respiration #ATP #Mitochondria #Class10Science #CBSE #BoardExams"""


def battery(dax, x, y, a, n, col=GOLD, max_n=38):
    """A tall bar showing an ATP count."""
    h = 3.2 * n / max_n
    dax.add_patch(Rectangle((x - 0.45, -1.6), 0.9, 3.2, fill=False, edgecolor=LTGREY, lw=2, alpha=a * 0.6, zorder=4))
    dax.add_patch(Rectangle((x - 0.45, -1.6), 0.9, h, facecolor=col, edgecolor="none", alpha=a, zorder=5))
    outline(dax.text(x, -1.6 + h + 0.25, f"{n:.0f}", ha="center", fontsize=30, color=col, fontweight="bold", alpha=a,
                     zorder=7))


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    ba = ease(c.phase("both", 0.0, 0.25))
    main = 1 - ba
    ha = ease(c.phase("hook", 0.05, 0.35)) * (1 - ease(c.phase("glyco", 0.0, 0.25)))
    if ha > 0.01:
        battery(dax, -1.2, 0, ha, 2, PINK)
        battery(dax, 1.2, 0, ha, 38 * ease(c.phase("hook", 0.3, 0.8)), GREEN)
        outline(dax.text(-1.2, -2.05, "no O₂", ha="center", fontsize=22, color=PINK, fontweight="bold", alpha=ha, zorder=7))
        outline(dax.text(1.2, -2.05, "with O₂", ha="center", fontsize=22, color=GREEN, fontweight="bold", alpha=ha, zorder=7))
    ga = ease(c.phase("glyco", 0.0, 0.3)) * main
    if ga > 0.01:
        sp = ease(c.phase("glyco", 0.3, 0.7))
        # glucose hexagon splitting into two pyruvate triangles
        if sp < 0.99:
            dax.add_patch(RegularPolygon((0, 1.7), 6, radius=0.55, facecolor="#3a2a00", edgecolor=GOLD, lw=4,
                                         alpha=ga * (1 - sp), zorder=6))
            dax.text(0, 1.7, "glucose", ha="center", va="center", fontsize=16, color=GOLD, fontweight="bold",
                     alpha=ga * (1 - sp), zorder=7)
        for s in (-1, 1):
            x = s * 0.9 * sp
            dax.add_patch(RegularPolygon((x, 1.5), 3, radius=0.42, facecolor="#00313a", edgecolor=CYAN, lw=3,
                                         alpha=ga * sp, zorder=6))
        outline(dax.text(0, 0.85, "2 pyruvate  +  2 ATP", ha="center", fontsize=22, color=CYAN, fontweight="bold",
                         alpha=ga * sp, zorder=7))
        outline(dax.text(-2.4, 1.7, "cytoplasm", ha="center", fontsize=18, color=LTGREY, fontweight="bold",
                         alpha=ga, zorder=7))
        # two branches
        na = ease(c.phase("noo2", 0.0, 0.3)) * main
        if na > 0:
            dax.add_patch(FancyArrowPatch((-0.5, 0.55), (-1.8, -0.4), arrowstyle="-|>", mutation_scale=28, color=PINK,
                                          lw=4, alpha=na, zorder=5))
            dax.add_patch(FancyBboxPatch((-3.3, -1.75), 2.9, 1.25, boxstyle="round,pad=0,rounding_size=0.18",
                                         facecolor="#2a0716", edgecolor=PINK, lw=3, alpha=na, zorder=5))
            dax.text(-1.85, -0.9, "no O₂", ha="center", fontsize=20, color=PINK, fontweight="bold", alpha=na, zorder=6)
            dax.text(-1.85, -1.4, "lactic acid / alcohol", ha="center", fontsize=16, color=LTGREY, alpha=na, zorder=6)
            outline(dax.text(-1.85, -2.2, "total 2 ATP", ha="center", fontsize=22, color=PINK, fontweight="bold",
                             alpha=ease(c.phase("noo2", 0.4, 0.7)) * main, zorder=7))
        oa = ease(c.phase("o2", 0.0, 0.3)) * main
        if oa > 0:
            dax.add_patch(FancyArrowPatch((0.5, 0.55), (1.8, -0.4), arrowstyle="-|>", mutation_scale=28, color=GREEN,
                                          lw=4, alpha=oa, zorder=5))
            dax.add_patch(FancyBboxPatch((0.4, -1.75), 2.9, 1.25, boxstyle="round,pad=0,rounding_size=0.18",
                                         facecolor="#06261a", edgecolor=GREEN, lw=3, alpha=oa, zorder=5))
            dax.text(1.85, -0.9, "mitochondria", ha="center", fontsize=20, color=GREEN, fontweight="bold", alpha=oa, zorder=6)
            dax.text(1.85, -1.4, "→ CO₂ + H₂O", ha="center", fontsize=16, color=LTGREY, alpha=oa, zorder=6)
            n = 2 + 36 * ease(c.phase("o2", 0.4, 0.85))
            outline(dax.text(1.85, -2.2, f"total {n:.0f} ATP", ha="center", fontsize=22, color=GREEN, fontweight="bold",
                             alpha=oa, zorder=7))
    if ba > 0.01:
        bb = ba * (1 - ease(c.phase("math", 0.0, 0.3)))
        # sprinting: oxygen meter low, backup kicks in
        lvl = 1 - 0.75 * ease(c.phase("both", 0.2, 0.6))
        dax.add_patch(Rectangle((-2.6, -1.4), 0.7, 2.8, fill=False, edgecolor=CYAN, lw=3, alpha=bb, zorder=5))
        dax.add_patch(Rectangle((-2.6, -1.4), 0.7, 2.8 * lvl, facecolor=CYAN, edgecolor="none", alpha=bb * 0.8, zorder=4))
        outline(dax.text(-2.25, -1.85, "oxygen", ha="center", fontsize=19, color=CYAN, fontweight="bold", alpha=bb, zorder=7))
        ka = ease(c.phase("both", 0.5, 0.8)) * bb
        dax.add_patch(FancyBboxPatch((-0.9, -0.6), 3.9, 1.6, boxstyle="round,pad=0,rounding_size=0.2",
                                     facecolor="#2a0716", edgecolor=PINK, lw=3, alpha=ka, zorder=5))
        dax.text(1.05, 0.45, "backup: anaerobic", ha="center", fontsize=22, color=PINK, fontweight="bold", alpha=ka, zorder=6)
        dax.text(1.05, -0.15, "quick energy · lactic acid", ha="center", fontsize=17, color=LTGREY, alpha=ka, zorder=6)
        outline(dax.text(0.3, 2.1, "sprinting!", ha="center", fontsize=28, color=GOLD, fontweight="bold",
                         alpha=bb, zorder=7))
    ma = ease(c.phase("math", 0.0, 0.35))
    if ma > 0.01:
        battery(dax, -1.2, 0, ma, 2, PINK)
        battery(dax, 1.2, 0, ma, 38, GREEN)
        outline(dax.text(-1.2, -2.05, "partial", ha="center", fontsize=22, color=PINK, fontweight="bold", alpha=ma, zorder=7))
        outline(dax.text(1.2, -2.05, "complete", ha="center", fontsize=22, color=GREEN, fontweight="bold", alpha=ma, zorder=7))
    c.steps([("partial breakdown → 2 ATP", 0.0, WHITE),
             ("complete breakdown → 38 ATP", 0.3, GOLD)], ys=(0.345, 0.285))
