"""WHY? — Why can 99% accuracy still be a BAD model?  (AI · Evaluation / Confusion Matrix, Class 10 & 12)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why can 99% accuracy be BAD?"
TAGS = "AI · Evaluation"
BEATS = [
    ("hook",   "An A I with ninety nine percent accuracy sounds amazing. But it might be useless. Here's why.",
               "An AI with 99% accuracy sounds amazing… but it might be USELESS. Here's why.", 4.4),
    ("data",   "Imagine detecting a rare disease. Out of a hundred people, only one is sick.",
               "Detecting a rare disease: out of 100 people, only ONE is sick.", 4.0),
    ("lazy",   "A lazy model just says healthy, for everyone.",
               "A lazy model just says 'healthy' — for EVERYONE.", 3.4),
    ("score",  "It's right ninety nine times out of a hundred. Ninety nine percent accuracy! "
               "But it missed the one person who actually needed help.",
               "Right 99 times out of 100 → 99% accuracy! But it MISSED the one person who needed help.", 6.0),
    ("matrix", "That's why we use a confusion matrix. It shows exactly what was caught, and what was missed.",
               "That's why we use a CONFUSION MATRIX — what was caught, and what was missed.", 5.0),
    ("recall", "Recall asks: out of the sick people, how many did we catch? Here, zero percent.",
               "RECALL: of the sick people, how many did we catch? Here: 0%!", 4.6),
    ("math",   "So never trust accuracy alone. Check recall and precision too.",
               "Never trust accuracy alone — check recall & precision too.", 3.8),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🎯 WHY? — Why can 99% accuracy still be a BAD AI model?

Rare disease: 1 sick person out of 100 🧑‍⚕️
A lazy model says "healthy" for everyone → right 99 times → 99% accuracy! 🤩
…but it missed the ONE person who needed help ❌

Confusion matrix → Recall = 0 / 1 = 0% 😱
Lesson: never trust accuracy alone — check recall & precision.

Model evaluation — AI syllabus, Class 10 & 12. 🧠

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ArtificialIntelligence #ConfusionMatrix #ModelEvaluation #AIClass10 #AIClass12 #CBSE"""

SICK = 37                      # index of the one sick person in the 10x10 grid


def gxy(k):
    r, q = divmod(k, 10)
    return -2.7 + q * 0.6, 2.2 - r * 0.52


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    g_a = ease(c.phase("data", 0.0, 0.5)) * (1 - ease(c.phase("matrix", 0.0, 0.25)))
    if g_a > 0:
        lazy = ease(c.phase("lazy", 0.2, 0.6))
        for k in range(100):
            x, y = gxy(k)
            sick = k == SICK
            col = PINK if sick else GREEN
            a = ease((g_a * 110 - k) / 10)
            dax.add_patch(Circle((x, y), 0.17, color=col, alpha=a * g_a, zorder=5))
            if lazy > 0:
                dax.text(x, y - 0.005, "✓", ha="center", va="center", fontsize=12, fontweight="bold",
                         color=NAVY, alpha=lazy * g_a, zorder=6)
        if c.phase("data", 0.5, 0.8) > 0:
            sx, sy = gxy(SICK)
            ma = ease(c.phase("data", 0.5, 0.8)) * g_a
            dax.annotate("1 sick", xy=(sx + 0.12, sy + 0.14), xytext=(sx + 0.9, sy + 0.95), color=PINK, fontsize=26,
                         fontweight="bold", alpha=ma, zorder=8, ha="center",
                         arrowprops=dict(arrowstyle="-|>", color=PINK, lw=2.5, alpha=ma))
        sc = back_out(c.phase("score", 0.0, 0.25)) * (1 - ease(c.phase("matrix", 0.0, 0.25)))
        if sc > 0.01:
            c.pill(0.5, 0.385, 0.48 * min(1, sc), 0.064, GREEN, alpha=min(1, sc), dark="#06261a")
            c.text(0.5, 0.385, "accuracy = 99%", size=44, color=GREEN, alpha=min(1, sc))
        mi = ease(c.phase("score", 0.45, 0.7)) * g_a
        if mi > 0:
            sx, sy = gxy(SICK)
            dax.add_patch(Circle((sx, sy), 0.36, fill=False, edgecolor=PINK, lw=4, alpha=mi, zorder=7))
            c.text(0.5, 0.325, "✗  missed the one sick person", size=32, color=PINK, alpha=mi)

    # confusion matrix
    if c.at("matrix"):
        ma = ease(c.phase("matrix", 0.15, 0.5))
        cells = [("caught\n(TP)", "0", 0, 0, PINK), ("missed\n(FN)", "1", 1, 0, PINK),
                 ("false alarm\n(FP)", "0", 0, 1, GOLD), ("correct\nhealthy (TN)", "99", 1, 1, GREEN)]
        for k, (lab, v, col_i, row_i, col) in enumerate(cells):
            a = ease(c.phase("matrix", 0.2 + k * 0.12, 0.4 + k * 0.12))
            x0, y0 = -1.75 + col_i * 2.05, 0.35 - row_i * 1.75
            hl = 1.0
            if c.at("recall") and row_i == 0:
                hl = 1.0
            dax.add_patch(FancyBboxPatch((x0, y0), 1.9, 1.6, boxstyle="round,pad=0,rounding_size=0.15",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=a, zorder=5))
            dax.text(x0 + 0.95, y0 + 1.0, v, ha="center", va="center", fontsize=40, fontweight="bold", color=col,
                     alpha=a, zorder=6)
            dax.text(x0 + 0.95, y0 + 0.38, lab, ha="center", va="center", fontsize=17, color=LTGREY, alpha=a, zorder=6)
        outline(dax.text(-2.3, 1.15, "sick", ha="right", va="center", fontsize=24, fontweight="bold", color=PINK,
                         alpha=ma, zorder=6))
        outline(dax.text(-2.3, -0.6, "healthy", ha="right", va="center", fontsize=24, fontweight="bold", color=GREEN,
                         alpha=ma, zorder=6))
        outline(dax.text(0.2, 2.25, "predicted: sick | healthy", ha="center", fontsize=22, fontweight="bold",
                         color=LTGREY, alpha=ma, zorder=6))
        if c.at("recall"):
            ra = ease(c.phase("recall", 0.15, 0.4))
            dax.add_patch(FancyBboxPatch((-1.9, 0.2), 4.1, 1.9, boxstyle="round,pad=0,rounding_size=0.2",
                                         fill=False, edgecolor=WHITE, lw=3.5, ls=(0, (5, 3)), alpha=ra, zorder=7))
            rr = back_out(c.phase("recall", 0.35, 0.6))
            if rr > 0.01:
                c.pill(0.5, 0.385, 0.56 * min(1, rr), 0.062, PINK, alpha=min(1, rr) * (1 - ease(c.phase("math", 0.0, 0.2))),
                       dark="#2a0716")
                c.text(0.5, 0.385, "recall = 0 / 1 = 0%", size=40, color=PINK,
                       alpha=min(1, rr) * (1 - ease(c.phase("math", 0.0, 0.2))))
    c.steps([("accuracy 99%  ≠  good model", 0.0, WHITE),
             ("check recall & precision", 0.3, GOLD)], ys=(0.345, 0.285))
