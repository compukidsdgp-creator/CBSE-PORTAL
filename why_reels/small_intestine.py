"""WHY? — Why is the small intestine so long?  (Class 10 Life Processes)"""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why is the small intestine SO LONG?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",   "Your small intestine is about six metres long. Taller than three people! Why does it need to be so long?",
               "Your small intestine is ~6 metres long — taller than 3 people! Why so LONG?", 5.0),
    ("job",    "It has two big jobs. Finish digesting the food, and absorb the nutrients into the blood.",
               "Two big jobs: FINISH digestion and ABSORB nutrients into the blood.", 4.6),
    ("time",   "A long tube means food moves slowly. More time to digest, more time to absorb.",
               "A long tube → food moves slowly → more TIME to digest and absorb.", 4.6),
    ("villi",  "Inside, the wall is covered with millions of tiny finger like villi. They hugely increase the surface area.",
               "Inside: millions of finger-like VILLI → HUGE surface area for absorption.", 5.4),
    ("diet",   "Grass eaters have even longer small intestines. Cellulose takes a long time to digest.",
               "Grass-eaters have even LONGER ones — cellulose takes a long time to digest.", 4.8),
    ("math",   "More length, more villi, means more absorption.",
               "More length + more villi = more absorption.", 3.4),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🌀 WHY? — Why is the small intestine SO long?

~6 metres coiled inside you — taller than 3 people! 📏

Its jobs: finish digestion + absorb nutrients into blood 🩸
✅ Long tube → food moves slowly → more time to digest & absorb
✅ Villi (tiny finger-like folds) → huge surface area

Herbivores have even longer small intestines — cellulose is slow to digest 🐄🌿

Life Processes: Nutrition — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #SmallIntestine #Villi #Class10Science #LifeProcesses #CBSE #BoardExams"""


def coil_path(n=600):
    """A coiled tube (packed zig-zag) inside a belly-sized box."""
    t = np.linspace(0, 1, n)
    rows = 6
    y = 1.3 - 2.6 * t
    x = 1.1 * np.sin(t * rows * np.pi)
    return x, y


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    vil = ease(c.phase("villi", 0.0, 0.25))
    dia = ease(c.phase("diet", 0.0, 0.25))
    main = (1 - vil)
    a0 = ease(c.phase("hook", 0.05, 0.3))
    if main > 0.01 and dia < 0.5:
        un = ease(c.phase("hook", 0.35, 0.85)) * (1 - ease(c.phase("job", 0.0, 0.3)))
        xc, yc = coil_path()
        xs = np.linspace(-3.0, 3.0, len(xc))
        x = lerp(xc, xs, un); y = lerp(yc, np.full_like(yc, 0.6), un)
        dax.plot(x, y, color="#f4a6b8", lw=16, alpha=a0 * main, zorder=4, solid_capstyle="round")
        dax.plot(x, y, color="#c75b7a", lw=4, alpha=a0 * main * 0.6, zorder=5)
        if un > 0.05:
            dax.add_patch(FancyArrowPatch((-3.0, -0.3), (3.0, -0.3), arrowstyle="<|-|>", mutation_scale=30, color=GOLD,
                                          lw=3, alpha=un * main, zorder=6))
            outline(dax.text(0, -0.75, "≈ 6 metres", ha="center", fontsize=30, color=GOLD, fontweight="bold",
                             alpha=un * main, zorder=7))
        ja = ease(c.phase("job", 0.2, 0.5)) * main
        if ja > 0:
            outline(dax.text(-1.6, 2.0, "digest", ha="center", fontsize=26, color=CYAN, fontweight="bold", alpha=ja, zorder=7))
            outline(dax.text(1.6, 2.0, "absorb", ha="center", fontsize=26, color=GREEN, fontweight="bold", alpha=ja, zorder=7))
        ta = ease(c.phase("time", 0.1, 0.4)) * main
        if ta > 0:
            # food particles moving slowly along the coil
            for k in range(8):
                f = (k / 8 + 0.03 * c.t) % 1.0
                i = int(f * (len(x) - 1))
                dax.add_patch(Circle((x[i], y[i]), 0.12, color=GOLD, alpha=ta, zorder=6))
            outline(dax.text(0, -2.3, "slow trip = more time", ha="center", fontsize=24, color=WHITE, fontweight="bold",
                             alpha=ta, zorder=7))
    if vil > 0.01 and dia < 0.99:
        va = vil * (1 - dia)
        # zoom on the wall: villi fingers growing, nutrients going into blood
        dax.add_patch(Rectangle((-3.2, -2.0), 6.4, 0.6, facecolor="#c75b7a", edgecolor="none", alpha=va, zorder=4))
        g = ease(c.phase("villi", 0.15, 0.6))
        for k in range(11):
            x0 = -2.9 + 0.58 * k
            h = 2.3 * g
            xs = np.linspace(-0.2, 0.2, 30)
            ys = -1.4 + h * np.sqrt(np.clip(1 - (xs / 0.2) ** 2, 0, 1)) ** 0.35
            dax.fill_between(x0 + xs, -1.4, ys, color="#f4a6b8", alpha=va, zorder=5, lw=0)
            dax.plot([x0, x0], [-1.4, -1.4 + h * 0.85], color="#e63946", lw=2, alpha=va * 0.8, zorder=6)
        na = ease(c.phase("villi", 0.5, 0.8)) * va
        for k in range(10):
            f = (k / 10 + 0.15 * c.t) % 1.0
            dax.add_patch(Circle((-2.6 + 0.55 * k, lerp(1.9, -1.0, f)), 0.09, color=GOLD, alpha=na * (1 - f * 0.6), zorder=7))
        outline(dax.text(0, 2.25, "villi = huge surface area", ha="center", fontsize=24, color=PINK, fontweight="bold",
                         alpha=va, zorder=8))
        outline(dax.text(2.2, -2.4, "into blood", ha="center", fontsize=19, color="#ff6b6b", fontweight="bold",
                         alpha=na, zorder=8))
    if dia > 0.01:
        da = dia * (1 - ease(c.phase("math", 0.0, 0.25)))
        for x, lab, L, col in ((-1.7, "humans\n(mixed diet)", 1.8, CYAN), (1.7, "cows\n(grass, cellulose)", 3.6, GREEN)):
            g = ease(c.phase("diet", 0.2, 0.7))
            dax.add_patch(Rectangle((x - 0.35, -1.8), 0.7, L * g, facecolor=col, edgecolor="none", alpha=da, zorder=5))
            outline(dax.text(x, -2.25, lab, ha="center", va="center", fontsize=19, color=col, fontweight="bold",
                             alpha=da, zorder=7))
        outline(dax.text(0, 2.35, "small intestine length", ha="center", fontsize=22, color=LTGREY, fontweight="bold",
                         alpha=da, zorder=7))
    ma = ease(c.phase("math", 0.0, 0.3))
    if ma > 0.01:
        for k, (s, col) in enumerate((("length", GOLD), ("+", WHITE), ("villi", PINK))):
            outline(dax.text(-2.0 + 2.0 * k, 0.6, s, ha="center", va="center", fontsize=36, color=col, fontweight="bold",
                             alpha=ma, zorder=8))
        outline(dax.text(0, -0.6, "= more absorption", ha="center", fontsize=34, color=GREEN, fontweight="bold",
                         alpha=ease(c.phase("math", 0.3, 0.6)), zorder=8))
    c.steps([("long + villi → more time & surface", 0.0, WHITE),
             ("maximum absorption", 0.3, GOLD)], ys=(0.345, 0.285))
