"""WHY? — Why does a confusion matrix have four boxes?  (AI · Evaluation, Class 10 & 12)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does a confusion matrix have FOUR boxes?"
TAGS = "AI · Evaluation"
BEATS = [
    ("hook",   "Every confusion matrix has exactly four boxes. Not three, not five. Let's see why, with a spam filter.",
               "Every confusion matrix has exactly FOUR boxes. Why? Let's use a SPAM filter.", 4.8),
    ("twoq",   "Each email gives two answers. What did the model say? Spam or not. And what was it really? Spam or not.",
               "Each email has TWO answers: what the model SAID, and what it REALLY was.", 5.4),
    ("grid",   "Two answers, each yes or no. Two times two, that's four possible outcomes.",
               "Two answers × yes/no each = 2 × 2 = FOUR outcomes.", 4.2),
    ("right",  "True positive: spam, caught. True negative: a normal email, delivered. Both correct.",
               "TRUE POSITIVE: spam caught ✓  TRUE NEGATIVE: normal email delivered ✓", 5.0),
    ("wrong",  "False positive: a normal email sent to spam. A false alarm. False negative: spam that slipped through. A miss.",
               "FALSE POSITIVE: good email sent to spam (false alarm). FALSE NEGATIVE: spam got through (miss).", 6.4),
    ("cost",   "The two mistakes cost different things. That's why we count them separately.",
               "The two mistakes cost DIFFERENT things — so we count them separately.", 4.2),
    ("math",   "Predicted, times actual. Two by two equals four boxes.",
               "Predicted × Actual: 2 × 2 = 4 boxes (TP, TN, FP, FN).", 3.8),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧮 WHY? — Why does a confusion matrix have FOUR boxes?

Spam filter example 📧
Each email → 2 questions: what did the model SAY? what was it REALLY?
2 answers × yes/no = 2 × 2 = 4 outcomes

✅ TP: spam caught
✅ TN: normal email delivered
⚠️ FP: normal email sent to spam (false alarm)
❌ FN: spam slipped through (miss)

Different mistakes, different costs — so we count them separately!

Model Evaluation — AI, Class 10 & 12. 🧠

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ConfusionMatrix #ArtificialIntelligence #AIClass10 #AIClass12 #MachineLearning #CBSE"""

CELLS = [  # (col, row, short, long, color, beat)
    (0, 0, "TP", "spam caught", GREEN, "right"),
    (1, 1, "TN", "email delivered", GREEN, "right"),
    (1, 0, "FN", "spam got through", PINK, "wrong"),
    (0, 1, "FP", "email → spam", GOLD, "wrong"),
]


def env(dax, x, y, a, spam, w=0.9):
    if a <= 0.01:
        return
    col = PINK if spam else CYAN
    dax.add_patch(FancyBboxPatch((x - w / 2, y - w * 0.32), w, w * 0.64, boxstyle="round,pad=0,rounding_size=0.06",
                                 facecolor="#13264d", edgecolor=col, lw=3, alpha=a, zorder=6))
    dax.plot([x - w / 2, x, x + w / 2], [y + w * 0.32, y - 0.02, y + w * 0.32], color=col, lw=3, alpha=a, zorder=7)
    if spam:
        dax.text(x, y - w * 0.15, "SPAM", ha="center", va="center", fontsize=11, color=PINK, fontweight="bold",
                 alpha=a, zorder=7)


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    ga = ease(c.phase("grid", 0.0, 0.3))
    ha = ease(c.phase("hook", 0.05, 0.35)) * (1 - ga)
    if ha > 0.01:
        env(dax, -0.9, 0.3, ha, False, 1.6)
        env(dax, 0.9, 0.3, ha * ease(c.phase("hook", 0.3, 0.6)), True, 1.6)
        q = ease(c.phase("twoq", 0.1, 0.4)) * (1 - ga)
        if q > 0:
            outline(dax.text(0, 1.75, "model said: spam?", ha="center", fontsize=24, color=CYAN, fontweight="bold",
                             alpha=q, zorder=8))
            outline(dax.text(0, -1.25, "really was: spam?", ha="center", fontsize=24, color=GOLD, fontweight="bold",
                             alpha=ease(c.phase("twoq", 0.5, 0.8)) * (1 - ga), zorder=8))
    if ga > 0.01:
        ca = ga * (1 - ease(c.phase("math", 0.0, 0.0001)) * 0)
        outline(dax.text(0.35, 2.4, "model PREDICTED", ha="center", fontsize=20, color=CYAN, fontweight="bold",
                         alpha=ga, zorder=8))
        for k, s in enumerate(("spam", "not spam")):
            outline(dax.text(-0.75 + 2.2 * k, 2.0, s, ha="center", fontsize=19, color=CYAN, fontweight="bold",
                             alpha=ga, zorder=8))
        outline(dax.text(-3.15, 0.0, "ACTUAL", ha="center", va="center", fontsize=20, color=GOLD, fontweight="bold",
                         rotation=90, alpha=ga, zorder=8))
        for k, s in enumerate(("spam", "not\nspam")):
            outline(dax.text(-2.4, 0.95 - 2.0 * k, s, ha="center", va="center", fontsize=19, color=GOLD,
                             fontweight="bold", alpha=ga, zorder=8))
        for col, row, short, long, colr, bt in CELLS:
            x0, y0 = -1.8 + col * 2.2, 0.05 - row * 2.0
            a = ga * ease(c.phase("grid", 0.3 + 0.1 * (col + 2 * row), 0.5 + 0.1 * (col + 2 * row)))
            reveal = ease(c.phase(bt, 0.1 + (0.4 if short in ("FN", "TN") else 0.0), 0.35 + (0.4 if short in ("FN", "TN") else 0.0)))
            dax.add_patch(FancyBboxPatch((x0, y0), 2.05, 1.8, boxstyle="round,pad=0,rounding_size=0.15",
                                         facecolor="#13264d", edgecolor=colr if reveal > 0 else LTGREY, lw=3.5,
                                         alpha=a, zorder=5))
            if reveal <= 0:
                dax.text(x0 + 1.02, y0 + 0.9, "?", ha="center", va="center", fontsize=36, color=LTGREY,
                         fontweight="bold", alpha=a, zorder=6)
            else:
                dax.text(x0 + 1.02, y0 + 1.15, short, ha="center", va="center", fontsize=38, color=colr,
                         fontweight="bold", alpha=a * reveal, zorder=6)
                dax.text(x0 + 1.02, y0 + 0.45, long, ha="center", va="center", fontsize=16, color=LTGREY,
                         fontweight="bold", alpha=a * reveal, zorder=6)
        cs = ease(c.phase("cost", 0.1, 0.4))
        if cs > 0:
            outline(dax.text(0.35, -2.35, "miss ≠ false alarm", ha="center", fontsize=24, color=WHITE,
                             fontweight="bold", alpha=cs * (1 - ease(c.phase("end", 0.0, 0.2))), zorder=8))
    c.steps([("predicted × actual  =  2 × 2", 0.0, WHITE),
             ("4 boxes: TP · TN · FP · FN", 0.3, GOLD)], ys=(0.345, 0.285))
