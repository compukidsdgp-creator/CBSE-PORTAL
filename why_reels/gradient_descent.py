"""WHY? — Why does gradient descent move opposite to the gradient? (loss function + learning)  (AI · Class 12)"""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does AI learning go AGAINST the gradient?"
TAGS = "AI · Neural Networks"
BEATS = [
    ("hook",    "How does an A I learn from its mistakes? It walks downhill, on a hill made of its own errors.",
                "How does an AI learn from mistakes? It walks DOWNHILL on a hill of its own errors.", 4.8),
    ("loss",    "First, the loss function. It's a single number that says how wrong the predictions are. Big loss, bad model.",
                "LOSS FUNCTION: one number for how WRONG the predictions are. Big loss = bad model.", 5.4),
    ("valley",  "Plot the loss for every value of a weight. You get a valley. Training means finding the bottom.",
                "Plot loss vs a weight → a VALLEY. Training = find the BOTTOM.", 4.6),
    ("grad",    "The gradient is the slope. It always points uphill, the direction where loss grows fastest.",
                "The GRADIENT is the slope — it points UPHILL, where loss grows fastest.", 4.6),
    ("step",    "So we step the opposite way, downhill. New weight equals old weight, minus learning rate times gradient. Step after step.",
                "So step the OPPOSITE way: w_new = w − η × gradient. Step after step…", 6.0),
    ("lr",      "The learning rate is the step size. Too big, and you overshoot. Too small, and it takes forever.",
                "LEARNING RATE = step size: too big → overshoot, too small → forever.", 4.8),
    ("math",    "Gradient points uphill. Minus gradient goes downhill, to lower loss.",
                "Gradient ↑ uphill.  −Gradient ↓ downhill → lower loss.", 3.8),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """⛰️ WHY? — Why does gradient descent move OPPOSITE to the gradient?

📉 Loss function = one number for how wrong the model is
Plot loss vs a weight → a valley. Training = reach the bottom.

↗️ Gradient = slope → points UPHILL (loss increases fastest)
↘️ So step the OPPOSITE way: w_new = w − η × gradient
η (learning rate) = step size: too big overshoots, too small is slow

AI / Neural Networks — Class 12. 🤖

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #GradientDescent #LossFunction #MachineLearning #ArtificialIntelligence #AIClass12 #CBSE"""

W = np.linspace(-3, 3, 300)


def L(w):
    return 0.32 * (w - 0.4) ** 2 - 1.6


def dL(w):
    return 0.64 * (w - 0.4)


def path(w0, eta, n):
    ws = [w0]
    for _ in range(n):
        ws.append(ws[-1] - eta * dL(ws[-1]))
    return ws


def ball(dax, w, a, col=GOLD):
    dax.add_patch(Circle((w, L(w) + 0.2), 0.2, facecolor=col, edgecolor=WHITE, lw=2, alpha=a, zorder=8))


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    a0 = ease(c.phase("hook", 0.05, 0.35))
    ma = ease(c.phase("math", 0.0, 0.3))
    lo = ease(c.phase("loss", 0.0, 0.25)) * (1 - ease(c.phase("valley", 0.0, 0.25)))
    if lo > 0.01:
        # predictions vs truth: error bars
        xs = np.linspace(-2.6, 2.6, 7)
        truth = 0.5 * xs
        pred = truth + np.array([0.9, -0.7, 1.1, -0.5, 0.8, -1.0, 0.6])
        dax.plot(xs, truth, color=GREEN, lw=3, alpha=lo, zorder=5)
        for x, tr, p in zip(xs, truth, pred):
            dax.plot([x, x], [tr, p], color=PINK, lw=3, alpha=lo, zorder=5)
            dax.add_patch(Circle((x, p), 0.13, color=GOLD, alpha=lo, zorder=6))
        outline(dax.text(0, 2.2, "loss = total error", ha="center", fontsize=28, color=PINK, fontweight="bold", alpha=lo, zorder=8))
        outline(dax.text(-2.6, -2.0, "— truth", ha="left", fontsize=19, color=GREEN, fontweight="bold", alpha=lo, zorder=8))
        outline(dax.text(0.2, -2.0, "● prediction", ha="left", fontsize=19, color=GOLD, fontweight="bold", alpha=lo, zorder=8))
    va = (ease(c.phase("valley", 0.0, 0.3)) + a0 * (1 - ease(c.phase("loss", 0.0, 0.2)))) * (1 - ma)
    va = min(1, va) * (1 - lo)
    if va > 0.01:
        dax.plot(W, L(W), color=CYAN, lw=4, alpha=va, zorder=5)
        dax.plot([-3.1, 3.1], [-2.05, -2.05], color=GREY, lw=2, alpha=va * 0.6, zorder=3)
        outline(dax.text(3.1, -2.4, "weight w", ha="right", fontsize=18, color=LTGREY, fontweight="bold", alpha=va, zorder=8))
        outline(dax.text(-3.1, 2.3, "loss", ha="left", fontsize=20, color=LTGREY, fontweight="bold", alpha=va, zorder=8))
        if c.at("valley") and not c.at("grad"):
            outline(dax.text(0.4, -1.95, "★ goal", ha="center", fontsize=22, color=GREEN, fontweight="bold",
                             alpha=va * ease(c.phase("valley", 0.4, 0.7)), zorder=8))
        w0 = -2.0
        if c.at("grad") and not c.at("step"):
            ball(dax, w0, va)
            g = dL(w0)
            # tangent line + uphill arrow
            tx = np.array([w0 - 0.8, w0 + 0.8])
            dax.plot(tx, L(w0) + g * (tx - w0), color=PINK, lw=3, alpha=va, zorder=6)
            ga = ease(c.phase("grad", 0.3, 0.6))
            dax.add_patch(FancyArrowPatch((w0, L(w0) + 0.2), (w0 - 0.7, L(w0) + 0.2 + 0.7 * abs(g)), arrowstyle="-|>",
                                          mutation_scale=28, color=PINK, lw=4, alpha=va * ga, zorder=9))
            outline(dax.text(w0 + 0.45, L(w0) + 0.55, "gradient\n= uphill", ha="left", va="center", fontsize=21,
                             color=PINK, fontweight="bold", alpha=va * ga, zorder=9))
        if c.at("step") and not c.at("lr"):
            ws = path(w0, 1.0, 10)
            k = int(ease(c.phase("step", 0.1, 0.95)) * 10)
            for i in range(k):
                dax.add_patch(FancyArrowPatch((ws[i], L(ws[i]) + 0.45), (ws[i + 1], L(ws[i + 1]) + 0.45), arrowstyle="-|>",
                                              mutation_scale=18, color=GREEN, lw=2.5, alpha=va, zorder=7))
            ball(dax, ws[k], va, GREEN)
            outline(dax.text(0.4, 1.9, "w − η · gradient", ha="center", fontsize=26, color=GREEN, fontweight="bold",
                             alpha=va, zorder=9, family="DejaVu Sans Mono"))
        if c.at("lr"):
            big = path(-2.4, 2.9, 6)
            small = path(-2.4, 0.15, 6)
            kb = int(ease(c.phase("lr", 0.1, 0.5)) * 6)
            for i in range(kb):
                dax.plot([big[i], big[i + 1]], [L(big[i]) + 0.3, L(big[i + 1]) + 0.3], color=PINK, lw=2.5, alpha=va, zorder=7)
            ball(dax, big[kb], va, PINK)
            ks = int(ease(c.phase("lr", 0.5, 0.95)) * 6)
            for i in range(ks):
                dax.plot([small[i], small[i + 1]], [L(small[i]) + 0.3, L(small[i + 1]) + 0.3], color=GOLD, lw=2.5,
                         alpha=va, zorder=7)
            if c.phase("lr", 0.5, 1) > 0:
                ball(dax, small[ks], va, GOLD)
            outline(dax.text(-1.7, 2.3, "η big → overshoot", ha="center", fontsize=21, color=PINK, fontweight="bold",
                             alpha=va, zorder=9))
            outline(dax.text(1.7, 1.6, "η small → slow", ha="center", fontsize=21, color=GOLD, fontweight="bold",
                             alpha=va * ease(c.phase("lr", 0.5, 0.7)), zorder=9))
    if ma > 0.01:
        outline(dax.text(0, 0.9, "gradient → uphill", ha="center", fontsize=34, color=PINK, fontweight="bold", alpha=ma, zorder=8))
        outline(dax.text(0, -0.3, "−gradient → downhill", ha="center", fontsize=34, color=GREEN, fontweight="bold",
                         alpha=ease(c.phase("math", 0.3, 0.6)), zorder=8))
    c.steps([("$w_{new} = w - \\eta \\cdot \\nabla L$", 0.0, WHITE),
             ("step against the gradient", 0.3, GOLD)], ys=(0.345, 0.285))
