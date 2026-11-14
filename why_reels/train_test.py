"""WHY? — Why split data into TRAINING and TESTING sets?  (AI · Model Evaluation, Class 10 & 12)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why split data into TRAIN and TEST?"
TAGS = "AI · Model Evaluation"
BEATS = [
    ("hook",     "Why does every A I project split its data into a training set and a testing set? Think about exams.",
                 "Why does every AI project split data into TRAINING and TESTING? Think about exams.", 4.6),
    ("memorise", "Imagine a student who sees the exact exam questions beforehand. They score one hundred percent. "
                 "But did they learn?",
                 "A student sees the exact exam questions beforehand → 100%! But did they LEARN?", 5.6),
    ("newq",     "Give them new questions, and the score crashes.",
                 "Give them NEW questions… and the score crashes.", 3.4),
    ("ai",       "An A I can cheat the same way. It can memorise its training data. That's called overfitting.",
                 "An AI can cheat the same way — memorising its training data. That's OVERFITTING.", 5.0),
    ("split",    "So we split the data. Eighty percent to learn from, and twenty percent locked away for testing.",
                 "So we split the data: 80% to learn from, 20% locked away for testing.", 5.0),
    ("test",     "The test set checks whether the A I really learned, using data it has never seen.",
                 "The test set checks if the AI really learned — on data it has NEVER seen.", 4.6),
    ("math",     "Train on one part. Test on the other. Never test on your training data.",
                 "Train on one part. Test on the other. Never test on training data!", 4.2),
    ("end",      "Follow C B S E Mock for more why videos.",
                 "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """📊 WHY? — Why split data into TRAINING and TESTING sets?

A student who sees the exam questions beforehand scores 100%… then crashes on new questions 📉
An AI can "memorise" its training data the same way — that's OVERFITTING 🤖
So we split: 80% to train 🏋️ · 20% locked away to test 🔒
The test set checks if the AI really learned — on data it has never seen ✅

A core AI concept for Class 10 & 12 (model evaluation). 🧠

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ArtificialIntelligence #MachineLearning #Overfitting #AIClass10 #AIClass12 #CBSE"""

NOLD = [True, True, True, True, True]
NNEW = [False, True, False, False, True]


def card(dax, x, y, lab, mark, a, col=CYAN):
    dax.add_patch(FancyBboxPatch((x - 0.62, y - 0.42), 1.24, 0.84, boxstyle="round,pad=0,rounding_size=0.12",
                                 facecolor="#13264d", edgecolor=col, lw=2.5, alpha=a, zorder=5))
    dax.text(x - 0.22, y, lab, ha="center", va="center", fontsize=22, fontweight="bold", color=WHITE, alpha=a, zorder=6)
    if mark is not None:
        dax.text(x + 0.33, y, "✓" if mark else "✗", ha="center", va="center", fontsize=28, fontweight="bold",
                 color=GREEN if mark else PINK, alpha=a, zorder=6)


def draw(c):
    dax = c.area(0.0, 0.0, 7.6)
    # 1) exam with leaked questions
    ex_a = 1 - ease(c.phase("ai", 0.0, 0.25))
    if ex_a > 0 and c.at("memorise"):
        newp = ease(c.phase("newq", 0.0, 0.4))
        for k in range(5):
            a = ease(c.phase("memorise", 0.1 + k * 0.08, 0.25 + k * 0.08)) * ex_a
            if a <= 0:
                continue
            x = -2.8 + k * 1.4
            if newp < 0.5:
                mk = NOLD[k] if c.phase("memorise", 0.5, 0.7) > 0 else None
                card(dax, x, 1.2, f"Q{k + 1}", mk, a * (1 - 2 * newp))
            else:
                mk = NNEW[k] if c.phase("newq", 0.45, 0.7) > 0 else None
                card(dax, x, 1.2, f"Q{k + 6}", mk, a * (2 * newp - 1), col=PURPLE)
        lab = "seen-before questions" if newp < 0.5 else "NEW questions"
        outline(dax.text(0, 2.15, lab, ha="center", fontsize=26, fontweight="bold",
                         color=LTGREY if newp < 0.5 else PURPLE, alpha=ex_a, zorder=7))
        sc = 100 if c.phase("newq", 0.45, 0.7) == 0 else 40
        sa = ease(c.phase("memorise", 0.55, 0.75)) * ex_a
        if sa > 0:
            col = GREEN if sc == 100 else PINK
            outline(dax.text(0, -0.4, f"score: {sc}%", ha="center", fontsize=54, fontweight="bold", color=col,
                             alpha=sa, zorder=7))
            if sc == 40:
                outline(dax.text(0, -1.35, "memorised, didn't learn", ha="center", fontsize=28, fontweight="bold",
                                 color=LTGREY, alpha=sa, zorder=7))

    # 2) the AI version: overfitting
    oa = ease(c.phase("ai", 0.2, 0.5)) * (1 - ease(c.phase("split", 0.0, 0.2)))
    if oa > 0:
        rng = np.random.default_rng(5)
        xs = np.linspace(-3, 3, 9)
        ys = 0.35 * xs + rng.normal(0, 0.55, 9)
        dax.scatter(xs, ys, s=180, color=CYAN, edgecolors=NAVY, linewidths=1.5, alpha=oa, zorder=6)
        from numpy.polynomial import polynomial as P
        cf = P.polyfit(xs, ys, 8)
        xx = np.linspace(-3.05, 3.05, 300)
        dax.plot(xx, np.clip(P.polyval(xx, cf), -2.6, 2.6), color=PINK, lw=4, alpha=oa, zorder=5)
        dax.plot(xx, 0.35 * xx, color=GREEN, lw=3, ls=(0, (6, 4)), alpha=oa * 0.8, zorder=4)
        outline(dax.text(-2.9, 2.2, "memorised (overfit)", ha="left", fontsize=24, fontweight="bold", color=PINK,
                         alpha=oa, zorder=7))
        outline(dax.text(2.9, -2.3, "real pattern", ha="right", fontsize=24, fontweight="bold", color=GREEN,
                         alpha=oa, zorder=7))

    # 3) split the data 80 / 20
    if c.at("split"):
        sp = ease(c.phase("split", 0.2, 0.6))
        n, cols = 50, 10
        for k in range(n):
            r, q = divmod(k, cols)
            test = k >= 40
            x = -3.55 + q * 0.62
            y = 1.7 - r * 0.62 - (sp * 0.75 if test else 0.0)
            a = ease(c.phase("split", 0.0 + k * 0.004, 0.15 + k * 0.004))
            col = (PURPLE if test and sp > 0.3 else CYAN)
            dax.add_patch(Rectangle((x - 0.25, y - 0.25), 0.5, 0.5, facecolor=col, edgecolor=NAVY, lw=1, alpha=a, zorder=5))
        la = ease(c.phase("split", 0.55, 0.8))
        if la > 0:
            outline(dax.text(2.5, 0.75, "80%\ntrain", ha="left", va="center", fontsize=25, fontweight="bold",
                             color=CYAN, alpha=la, zorder=7))
            outline(dax.text(2.5, -1.2, "20%\ntest", ha="left", va="center", fontsize=25,
                             fontweight="bold", color=PURPLE, alpha=la, zorder=7))
        ta = back_out(c.phase("test", 0.3, 0.6)) * (1 - ease(c.phase("math", 0.0, 0.2)))
        if ta > 0.01:
            c.pill(0.5, 0.385, 0.62 * min(1, ta), 0.056, GREEN, alpha=min(1, ta), dark="#06261a")
            c.text(0.5, 0.385, "test accuracy on unseen data: 92%", size=30, color=GREEN, alpha=min(1, ta))
    c.steps([("Training data → learn", 0.0, CYAN), ("Testing data → check", 0.2, PURPLE),
             ("Never test on training data!", 0.45, GOLD)], ys=(0.330, 0.282, 0.228))
