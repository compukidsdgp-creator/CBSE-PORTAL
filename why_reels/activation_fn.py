"""WHY? — Why do neural networks need activation functions?  (AI · Neural Networks, Class 10 & 12)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why do neural networks need ACTIVATION functions?"
TAGS = "AI · Neural Networks"
BEATS = [
    ("hook",   "A neuron multiplies and adds. So why do neural networks also need something called an activation function?",
               "A neuron multiplies and adds… so why do networks need an ACTIVATION FUNCTION?", 5.0),
    ("linear", "Multiply and add gives a straight line. y equals w x plus b.",
               "Multiply + add = a STRAIGHT LINE: y = wx + b", 3.8),
    ("stack",  "Stack ten such layers. A line of a line of a line is still just one line! All the layers collapse into one.",
               "Stack 10 such layers… a line of a line is STILL a line! They collapse into ONE.", 5.6),
    ("curve",  "But real data is curvy. Faces, voices, handwriting. A straight line can't fit it.",
               "But real data is CURVY — faces, voices, handwriting. A line can't fit it.", 4.6),
    ("relu",   "An activation function adds a bend. ReLU keeps positives, and turns negatives into zero. Now there's a kink.",
               "Activation adds a BEND: ReLU keeps positives, turns negatives to 0 → a KINK.", 5.4),
    ("fit",    "Combine many neurons, each with its own kink, and the network can bend to fit almost any curve.",
               "Many neurons, many kinks → the network can bend to fit almost ANY curve!", 5.0),
    ("math",   "No activation, one big line. With activation, curves.",
               "No activation → one big line. With activation → CURVES.", 3.6),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧠 WHY? — Why do neural networks need ACTIVATION FUNCTIONS?

A neuron does multiply + add → a straight line (y = wx + b) 📏
Stack 10 linear layers → still ONE straight line! (they collapse)

Real data is curvy — faces, voices, handwriting 〰️
Activation (e.g. ReLU: max(0, x)) adds a BEND
Many neurons × many bends → the network can fit almost any curve ✅

No activation = one big line. With activation = curves!

Neural Networks — AI, Class 10 & 12. 🤖

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #NeuralNetworks #ActivationFunction #ReLU #ArtificialIntelligence #AIClass12 #CBSE"""

X = np.linspace(-3, 3, 300)
TARGET = 0.9 * np.sin(1.3 * X) + 0.15 * X


def relu(z):
    return np.maximum(0, z)


def fit_relu(n):
    """Piecewise-linear interpolation of TARGET with n kinks — what n ReLU neurons can build."""
    knots = np.linspace(-3, 3, n + 1)
    return np.interp(X, knots, 0.9 * np.sin(1.3 * knots) + 0.15 * knots)


def axes(dax, a, y0=0.0):
    dax.plot([-3.2, 3.2], [y0, y0], color=GREY, lw=2, alpha=a, zorder=3)
    dax.plot([0, 0], [-2.2, 2.2], color=GREY, lw=2, alpha=a, zorder=3)


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    a0 = ease(c.phase("hook", 0.05, 0.35))
    ma = ease(c.phase("math", 0.0, 0.3))
    ha = a0 * (1 - ease(c.phase("linear", 0.0, 0.25)))
    if ha > 0.01:
        for k, (s, col) in enumerate((("×w", CYAN), ("+b", GOLD), ("f( )?", PINK))):
            dax.add_patch(FancyBboxPatch((-2.95 + 2.05 * k, -0.6), 1.8, 1.4, boxstyle="round,pad=0,rounding_size=0.2",
                                         facecolor="#13264d", edgecolor=col, lw=3,
                                         alpha=ha * ease(c.phase("hook", 0.15 + 0.2 * k, 0.35 + 0.2 * k)), zorder=5))
            dax.text(-2.05 + 2.05 * k, 0.1, s, ha="center", va="center", fontsize=36, color=col, fontweight="bold",
                     alpha=ha * ease(c.phase("hook", 0.15 + 0.2 * k, 0.35 + 0.2 * k)), zorder=6)
    gr = ease(c.phase("linear", 0.0, 0.3)) * (1 - ma)
    if gr > 0.01:
        axes(dax, gr * 0.7)
        cu = ease(c.phase("curve", 0.0, 0.3))
        rl = ease(c.phase("relu", 0.0, 0.25))
        if rl < 0.99:
            lin_a = gr * (1 - rl)
            st = ease(c.phase("stack", 0.1, 0.8))
            w = 0.5
            for k in range(1 + int(5 * st)):
                ww = w * (1.1 ** k) * (-1) ** k
                dax.plot(X, ww * X + 0.1 * k, color=CYAN, lw=3 if k == 0 else 2, alpha=lin_a * (1 if k == 0 else 0.5), zorder=5)
            outline(dax.text(-1.6, 1.9, "y = wx + b", ha="center", fontsize=26, color=CYAN, fontweight="bold",
                             alpha=lin_a * (1 - st), zorder=8, family="DejaVu Sans Mono"))
            if st > 0:
                outline(dax.text(0, 2.3, "10 layers → still a line", ha="center", fontsize=24, color=PINK,
                                 fontweight="bold", alpha=lin_a * st * (1 - cu), zorder=8))
            if cu > 0:
                dax.plot(X, TARGET, color=GOLD, lw=4, alpha=lin_a * cu, zorder=6)
                outline(dax.text(0, 2.3, "real data is curvy", ha="center", fontsize=24, color=GOLD, fontweight="bold",
                                 alpha=lin_a * cu, zorder=8))
        if rl > 0.01:
            fi = ease(c.phase("fit", 0.0, 0.3))
            if fi < 0.99:
                dax.plot(X, relu(X) * 0.7 - 0.0, color=PINK, lw=5, alpha=gr * rl * (1 - fi), zorder=6)
                outline(dax.text(-1.5, 1.6, "ReLU = max(0, x)", ha="center", fontsize=24, color=PINK, fontweight="bold",
                                 alpha=gr * rl * (1 - fi), zorder=8, family="DejaVu Sans Mono"))
                outline(dax.text(0.35, -0.45, "kink!", ha="left", fontsize=24, color=WHITE, fontweight="bold",
                                 alpha=gr * ease(c.phase("relu", 0.5, 0.8)) * (1 - fi), zorder=8))
            if fi > 0:
                dax.plot(X, TARGET, color=GOLD, lw=3, alpha=gr * fi * 0.6, zorder=5, ls=(0, (5, 4)))
                n = 2 + int(14 * ease(c.phase("fit", 0.15, 0.85)))
                dax.plot(X, fit_relu(n), color=GREEN, lw=4, alpha=gr * fi, zorder=6)
                outline(dax.text(0, 2.3, f"{n} neurons → {n} bends", ha="center", fontsize=24, color=GREEN,
                                 fontweight="bold", alpha=gr * fi, zorder=8))
    if ma > 0.01:
        outline(dax.text(0, 0.9, "no activation → one line", ha="center", fontsize=32, color=CYAN, fontweight="bold",
                         alpha=ma, zorder=8))
        outline(dax.text(0, -0.3, "activation → curves", ha="center", fontsize=32, color=GREEN, fontweight="bold",
                         alpha=ease(c.phase("math", 0.3, 0.6)), zorder=8))
    c.steps([("linear layers collapse into one", 0.0, WHITE),
             ("activation adds bends → curves", 0.3, GOLD)], ys=(0.345, 0.285))
