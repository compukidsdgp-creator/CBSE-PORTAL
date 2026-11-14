"""WHY? — Why do we need both precision AND recall?  (AI · Evaluation, Class 10 & 12)"""
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why do we need BOTH precision and recall?"
TAGS = "AI · Evaluation"
BEATS = [
    ("hook",    "Imagine fishing in a pond full of fish and junk. Your A I is the net. How do you judge it?",
                "A pond with FISH and JUNK. Your AI is the net. How do you judge it?", 4.4),
    ("prec",    "Precision asks: of everything you caught, how much is actually fish?",
                "PRECISION: of everything you CAUGHT, how much is actually fish?", 4.2),
    ("rec",     "Recall asks: of all the fish in the pond, how many did you catch?",
                "RECALL: of ALL the fish in the pond, how many did you catch?", 4.0),
    ("wide",    "Throw a giant net. You catch every fish, so recall is perfect. But you also catch tons of junk. "
                "Precision is terrible.",
                "GIANT net: every fish caught → recall 100%! But tons of junk → precision LOW.", 6.0),
    ("narrow",  "Use a tiny net around one fish. Precision is perfect. But you missed most fish. Recall is terrible.",
                "TINY net: only fish → precision 100%! But most fish missed → recall LOW.", 5.4),
    ("both",    "Each number alone can be cheated. Together, they show the truth. The F one score combines both.",
                "Each number alone can be GAMED. Together they tell the truth — F1 score combines both.", 5.4),
    ("math",    "Precision equals T P over T P plus F P. Recall equals T P over T P plus F N.",
                "Precision = TP/(TP+FP)   Recall = TP/(TP+FN)", 4.4),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🎣 WHY? — Why do we need BOTH precision AND recall?

Pond with fish 🐟 and junk 🥫 — your AI is the net.

🎯 Precision: of everything caught, how much is fish? = TP/(TP+FP)
🔍 Recall: of all the fish, how many were caught? = TP/(TP+FN)

Giant net → recall 100%, precision terrible
Tiny net → precision 100%, recall terrible

Each alone can be gamed — together (F1 score) they tell the truth!

Model Evaluation — AI, Class 10 & 12. 🧠

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Precision #Recall #F1Score #ArtificialIntelligence #AIClass12 #CBSE"""

rng = np.random.default_rng(11)
PTS = np.c_[rng.uniform(-2.9, 2.9, 34), rng.uniform(-1.9, 1.7, 34)]
FISH = np.zeros(34, bool); FISH[[1, 4, 7, 9, 12, 15, 18, 22, 25, 30]] = True


def fish(dax, x, y, a, z=6):
    dax.add_patch(Ellipse((x, y), 0.42, 0.22, color=GOLD, alpha=a, zorder=z))
    dax.fill([x + 0.18, x + 0.34, x + 0.34], [y, y + 0.13, y - 0.13], color=GOLD, alpha=a, zorder=z)


def junk(dax, x, y, a, z=6):
    dax.add_patch(FancyBboxPatch((x - 0.12, y - 0.16), 0.24, 0.32, boxstyle="round,pad=0,rounding_size=0.04",
                                 facecolor=GREY, edgecolor=LTGREY, lw=1.5, alpha=a, zorder=z))


def bar(c, y, lab, val, col, a):
    c.text(0.17, y, lab, size=26, color=col, alpha=a, ha="left")
    c.pill(0.62, y, 0.40, 0.030, col, alpha=a * 0.5, fill_alpha=0.3)
    w = 0.40 * val
    if w > 0.01:
        c.pill(0.42 + w / 2, y, w, 0.030, col, alpha=a, fill_alpha=1.0, dark=col)
    c.text(0.89, y, f"{val * 100:.0f}%", size=24, color=col, alpha=a, ha="left")


def draw(c):
    dax = c.area(0.0, 0.1, 7.0)
    ma = ease(c.phase("math", 0.0, 0.3))
    a0 = ease(c.phase("hook", 0.05, 0.35)) * (1 - ma)
    if a0 > 0.01:
        dax.add_patch(Ellipse((0, -0.1), 6.6, 4.4, facecolor="#0d2c4a", edgecolor=CYAN, lw=3, alpha=a0, zorder=3))
        for (x, y), f in zip(PTS, FISH):
            (fish if f else junk)(dax, x, y, a0)
    # nets
    wide = ease(c.phase("wide", 0.05, 0.3)) * (1 - ease(c.phase("narrow", 0.0, 0.2)))
    narrow = ease(c.phase("narrow", 0.05, 0.3)) * (1 - ease(c.phase("both", 0.1, 0.3)))
    if wide > 0.01:
        dax.add_patch(Ellipse((0, -0.1), 6.2 * wide, 4.0 * wide, fill=False, edgecolor=WHITE, lw=4, ls=(0, (6, 4)),
                              alpha=a0 * wide, zorder=8))
    if narrow > 0.01:
        x, y = PTS[12]
        dax.add_patch(Circle((x, y), 0.45 * narrow, fill=False, edgecolor=WHITE, lw=4, ls=(0, (5, 3)),
                             alpha=a0 * narrow, zorder=8))
    pa = ease(c.phase("prec", 0.1, 0.4)) * (1 - ma)
    if pa > 0 and wide < 0.01 and narrow < 0.01:
        outline(dax.text(0, 2.45, "precision: caught → how many fish?", ha="center", fontsize=21, color=GREEN,
                         fontweight="bold", alpha=pa * (1 - ease(c.phase("rec", 0.0, 0.2))), zorder=9))
        outline(dax.text(0, 2.45, "recall: all fish → how many caught?", ha="center", fontsize=21, color=CYAN,
                         fontweight="bold", alpha=ease(c.phase("rec", 0.1, 0.35)), zorder=9))
    # score bars under the pond
    if wide > 0.01:
        bar(c, 0.383, "recall", 1.0, CYAN, wide)
        bar(c, 0.425, "precision", 10 / 34, GREEN, wide)
    if narrow > 0.01:
        bar(c, 0.383, "recall", 0.1, CYAN, narrow)
        bar(c, 0.425, "precision", 1.0, GREEN, narrow)
    ba = ease(c.phase("both", 0.2, 0.5)) * (1 - ma)
    if ba > 0.01:
        dax.add_patch(FancyBboxPatch((-2.0, -0.7), 4.0, 1.5, boxstyle="round,pad=0,rounding_size=0.2",
                                     facecolor="#13264d", edgecolor=GOLD, lw=3, alpha=ba, zorder=9))
        dax.text(0, 0.25, "F1 score", ha="center", va="center", fontsize=30, color=GOLD, fontweight="bold",
                 alpha=ba, zorder=10)
        dax.text(0, -0.3, "balances both", ha="center", va="center", fontsize=19, color=LTGREY, fontweight="bold",
                 alpha=ba, zorder=10)
    if ma > 0.01:
        outline(dax.text(0, 1.2, r"$Precision = \dfrac{TP}{TP+FP}$", ha="center", va="center", fontsize=40,
                         color=GREEN, alpha=ma, zorder=9))
        outline(dax.text(0, -0.6, r"$Recall = \dfrac{TP}{TP+FN}$", ha="center", va="center", fontsize=40,
                         color=CYAN, alpha=ease(c.phase("math", 0.3, 0.6)), zorder=9))
    c.steps([("one number alone can be gamed", 0.0, WHITE),
             ("check precision AND recall", 0.3, GOLD)], ys=(0.345, 0.285))
