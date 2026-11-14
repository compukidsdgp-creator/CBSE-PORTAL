"""WHY? — Why does a neural network need LAYERS?  (AI · Neural Networks / Deep Learning, Class 10 & 12)"""
import math
import numpy as np
from matplotlib.patches import Circle, Polygon
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does a neural network need LAYERS?"
TAGS = "AI · Deep Learning"
BEATS = [
    ("hook",    "Why do neural networks need so many layers? Because one neuron can only draw a straight line.",
                "Why so many layers? Because ONE neuron can only draw a straight line.", 4.4),
    ("data",    "Say we must separate the blue dots from the pink dots. The blue ones sit in the middle.",
                "Task: separate the blue dots from the pink dots. The blue ones sit in the middle.", 4.4),
    ("oneline", "A single neuron draws one straight line. However you turn it, it can't separate them.",
                "One neuron = one straight line. However you turn it, it can't separate them.", 5.2),
    ("more",    "Add a hidden layer of neurons. Each one draws its own line.",
                "Add a HIDDEN LAYER of neurons. Each one draws its own line.", 4.4),
    ("combine", "The next layer combines those lines, and they wrap around the blue dots. Separated!",
                "The next layer COMBINES the lines — they wrap around the blue dots. Separated!", 4.8),
    ("deep",    "Add more layers, and the boundary becomes a smooth curve. "
                "That's how deep learning handles faces, voices and much more.",
                "More layers → smooth, complex boundaries. That's how deep learning handles faces and voices.", 6.0),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧠 WHY? — Why does a neural network need LAYERS?

One neuron can only draw ONE straight line ➖
Blue dots in the middle, pink dots around them → no single line can split them ❌
A hidden layer draws many lines → the next layer combines them → they wrap around the blue dots ✅
More layers → smooth, complex shapes → faces, voices, language! 🎯

That's the idea behind DEEP learning — AI syllabus, Class 10 & 12.

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ArtificialIntelligence #DeepLearning #NeuralNetwork #AIClass10 #AIClass12 #CBSE"""

rng = np.random.default_rng(3)
_r_in = np.sqrt(rng.random(26)) * 0.75
_t_in = rng.random(26) * 2 * math.pi
BLUE = np.c_[_r_in * np.cos(_t_in), _r_in * np.sin(_t_in)]
_r_out = 1.35 + rng.random(34) * 0.5
_t_out = rng.random(34) * 2 * math.pi
PINKS = np.c_[_r_out * np.cos(_t_out), _r_out * np.sin(_t_out)]
R0 = 1.05                                   # where the boundary sits


def polygon(n, r=R0, rot=0.0):
    """Regular n-gon whose sides are tangent to a circle of radius r (each side = one neuron's line)."""
    ang = rot + (np.arange(n) + 0.5) * 2 * math.pi / n
    R = r / math.cos(math.pi / n)
    return np.c_[R * np.cos(ang), R * np.sin(ang)]


def tangent_line(theta, r=R0, L=2.6):
    nx, ny = math.cos(theta), math.sin(theta)
    px, py = r * nx, r * ny
    return [px - ny * L, px + ny * L], [py + nx * L, py - nx * L]


def draw(c):
    dax = c.area(0.0, -0.05, 5.4)
    da = ease(c.phase("data", 0.05, 0.5))
    if da > 0:
        dax.scatter(BLUE[:, 0], BLUE[:, 1], s=210, color=CYAN, edgecolors=NAVY, linewidths=1.5, alpha=da, zorder=6)
        dax.scatter(PINKS[:, 0], PINKS[:, 1], s=210, color=PINK, edgecolors=NAVY, linewidths=1.5, alpha=da, zorder=6)

    # one neuron = one straight line, swinging around and failing
    oa = c.phase("oneline", 0.05, 0.95) * (1 - ease(c.phase("more", 0.0, 0.2)))
    if oa > 0:
        th = 0.4 + oa * 2.6
        off = 0.3 * math.sin(oa * 7)
        nx, ny = math.cos(th), math.sin(th)
        px, py = off * nx, off * ny
        a = min(1, oa * 5) * (1 - ease(c.phase("more", 0.0, 0.2)))
        dax.plot([px - ny * 3, px + ny * 3], [py + nx * 3, py - nx * 3], color=GOLD, lw=5, alpha=a, zorder=7)
        wrong = sum((p[0] - px) * nx + (p[1] - py) * ny > 0 for p in BLUE) + \
            sum((p[0] - px) * nx + (p[1] - py) * ny < 0 for p in PINKS)
        wrong = min(wrong, len(BLUE) + len(PINKS) - wrong)
        c.pill(0.5, 0.385, 0.56, 0.056, PINK, alpha=a, dark="#2a0716")
        c.text(0.5, 0.385, f"✗  {wrong} dots on the wrong side", size=32, color=PINK, alpha=a)

    # hidden layer: several tangent lines; next layer combines them
    if c.at("more"):
        n = 3 if c.phase("more", 0.0, 0.55) < 1 else 6
        if c.at("combine"):
            n = 6
        for k in range(n):
            la = ease(c.phase("more", 0.1 + k * 0.08, 0.3 + k * 0.08)) if n == 3 else \
                ease(c.phase("more", 0.55 + (k - 3) * 0.1, 0.7 + (k - 3) * 0.1)) if k >= 3 else 1.0
            la *= 1 - ease(c.phase("deep", 0.0, 0.3))
            if la > 0:
                xs, ys = tangent_line((k + 0.5) * 2 * math.pi / n)
                dax.plot(xs, ys, color=GOLD, lw=3.5, alpha=la * 0.85, zorder=7)
        lab = "hidden layer: 3 neurons" if n == 3 else "hidden layer: 6 neurons"
        ha = ease(c.phase("more", 0.1, 0.3)) * (1 - ease(c.phase("combine", 0.0, 0.2)))
        c.text(0.5, 0.385, lab, size=32, color=GOLD, alpha=ha)

    cb = ease(c.phase("combine", 0.1, 0.55))
    if cb > 0:
        sm = ease(c.phase("deep", 0.1, 0.8))
        n = int(round(lerp(6, 60, sm)))
        poly = polygon(n, r=lerp(R0, 1.06, sm))
        dax.add_patch(Polygon(poly, closed=True, facecolor=CYAN, edgecolor=GREEN, lw=4, alpha=0.18 * cb, zorder=4))
        dax.add_patch(Polygon(poly, closed=True, fill=False, edgecolor=GREEN, lw=4.5, alpha=cb, zorder=8))
        ok = ease(c.phase("combine", 0.5, 0.75)) * (1 - ease(c.phase("deep", 0.0, 0.2)))
        if ok > 0:
            c.pill(0.5, 0.385, 0.42, 0.056, GREEN, alpha=ok, dark="#06261a")
            c.text(0.5, 0.385, "✓  all separated!", size=32, color=GREEN, alpha=ok)

    # deep: the layer stack, small, under the drawing
    if c.at("deep"):
        da2 = ease(c.phase("deep", 0.3, 0.6))
        for k, (s, col) in enumerate([("1 neuron → 1 straight line", WHITE), ("1 layer → corners", CYAN),
                                      ("many layers → any shape", GOLD)]):
            a = ease(c.phase("deep", 0.25 + k * 0.18, 0.45 + k * 0.18))
            if a > 0:
                if col == GOLD:
                    c.pill(0.5, 0.352 - k * 0.055, 0.66, 0.054, GOLD, alpha=a, dark="#2a2000")
                c.text(0.5, 0.352 - k * 0.055, s, size=36 if col != GOLD else 40, color=col, alpha=a)
