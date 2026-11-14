"""WHY? — How does a NEURON in AI decide?  (AI · Neural Networks, Class 10 & 12)"""
import math
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "How does an AI NEURON decide?"
TAGS = "AI · Neural Networks"
BEATS = [
    ("hook",    "How does a single neuron in a neural network make a decision? It's simpler than you think.",
                "How does one neuron in a neural network decide? It's simpler than you think.", 4.0),
    ("inputs",  "Should I go out to play? It checks three inputs. Is it sunny? Are friends free? Is homework done?",
                "Should I go out to play? Three inputs: Sunny? Friends free? Homework done?", 5.2),
    ("weights", "Each input has a weight, which shows how much it matters. Homework matters the most.",
                "Each input has a WEIGHT — how much it matters. Homework matters most.", 4.4),
    ("sum",     "Multiply each input by its weight and add. Point four, plus point three, plus zero, is point seven.",
                "Multiply each input by its weight and add: 0.4 + 0.3 + 0 = 0.7", 5.2),
    ("fire",    "Point seven is below the threshold of one, so the neuron stays off. Stay home.",
                "0.7 is below the threshold of 1, so the neuron stays OFF. Stay home!", 4.2),
    ("flip",    "Finish the homework, and the total becomes one point three. It crosses the threshold, "
                "and the neuron fires. Go play!",
                "Finish the homework → total = 1.3. It crosses the threshold and the neuron FIRES. Go play!", 6.0),
    ("net",     "Training adjusts these weights. Connect thousands of neurons in layers, and you get a neural network.",
                "Training adjusts the weights. Thousands of neurons in layers = a neural network.", 5.6),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧠 WHY? — How does an AI neuron decide?

Inputs × weights → add them up → compare with a threshold → fire or not! ⚡
Sunny ✅ Friends ✅ Homework ❌ → 0.7 → stay home 🏠
Finish homework ✅ → 1.3 → GO PLAY! ⚽

That's a perceptron — the building block of every neural network in your AI syllabus (Class 10 & 12).

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ArtificialIntelligence #NeuralNetwork #Perceptron #AIClass10 #AIClass12 #CBSE"""

LABELS = ["Sunny?", "Friends free?", "Homework done?"]
W = [0.4, 0.3, 0.6]
YS = [2.5, 0.0, -2.5]
END_Y = 0.300
NX, NR = 1.4, 1.05


def draw(c):
    net = ease(c.phase("net", 0.05, 0.45))
    dax = c.area(lerp(0.3, 0.0, net), 0.0, lerp(9.8, 10.5, net))
    a_main = 1 - net
    x3 = 1 if c.phase("flip", 0.0, 0.25) > 0.5 else 0
    xs = [1, 1, x3]

    if a_main > 0:
        for k, (lab, y) in enumerate(zip(LABELS, YS)):
            ia = ease(c.phase("inputs", 0.15 + k * 0.2, 0.35 + k * 0.2)) * a_main
            if ia <= 0:
                continue
            on = xs[k] == 1
            col = GREEN if on else PINK
            dax.add_patch(FancyBboxPatch((-4.45, y - 0.6), 2.75, 1.2, boxstyle="round,pad=0,rounding_size=0.18",
                                         facecolor="#0e1d3f", edgecolor=col, lw=2.5, alpha=ia, zorder=5))
            dax.text(-3.07, y + 0.2, lab, ha="center", va="center", fontsize=24, fontweight="bold",
                     color=WHITE, alpha=ia, zorder=6)
            dax.text(-3.07, y - 0.28, ("yes  → 1" if on else "no  → 0"), ha="center", va="center",
                     fontsize=23, fontweight="bold", color=col, alpha=ia, zorder=6)
            # connection with thickness = weight
            wa = ease(c.phase("weights", 0.1 + k * 0.15, 0.4 + k * 0.15)) * a_main
            lw = 2 + 14 * W[k] * (wa if wa > 0 else 0)
            dax.plot([-1.8, NX - NR * 0.85], [y, y * 0.25], color=GOLD if wa > 0 else GREY, lw=lw if wa > 0 else 2,
                     alpha=max(ia * 0.5, wa), solid_capstyle="round", zorder=3)
            if wa > 0:
                mx, my = -0.55, y * 0.62
                outline(dax.text(mx, my + 0.32, f"w = {W[k]}", ha="center", fontsize=25, fontweight="bold",
                                 color=GOLD, alpha=wa, zorder=7))
            # signal dots flowing when the input is on
            if c.at("sum") and on:
                for q in range(3):
                    f = (c.t * 0.9 + q / 3 + k * 0.17) % 1
                    px, py = lerp(-1.8, NX - NR * 0.85, f), lerp(y, y * 0.25, f)
                    dax.add_patch(Circle((px, py), 0.08, color=CYAN, alpha=a_main * 0.9, zorder=4))

        # the neuron
        na = ease(c.phase("hook", 0.3, 0.8)) * a_main
        fired = c.phase("flip", 0.35, 0.55) > 0
        glow = ease(c.phase("flip", 0.35, 0.6)) * a_main
        for r, al in [(1.7, 0.10), (1.35, 0.18)]:
            if glow > 0:
                dax.add_patch(Circle((NX, 0), r, color=GREEN, alpha=al * glow, zorder=2))
        dax.add_patch(Circle((NX, 0), NR, facecolor=(GREEN if fired else "#16295a"), edgecolor=CYAN, lw=3.5,
                             alpha=na, zorder=6))
        dax.text(NX, 0.15, "Σ", ha="center", va="center", fontsize=46, color=NAVY if fired else WHITE,
                 alpha=na, zorder=7)
        dax.text(NX, -0.5, "neuron", ha="center", va="center", fontsize=16, color=NAVY if fired else LTGREY,
                 alpha=na, zorder=7)

        # running total
        total = sum(x * w for x, w in zip(xs, W))
        sa = ease(c.phase("sum", 0.25, 0.6)) * a_main
        if sa > 0:
            outline(dax.text(NX, -1.65, f"total = {total:.1f}", ha="center", fontsize=36, fontweight="bold",
                             color=WHITE, alpha=sa, zorder=8))
        # threshold + output
        oa = ease(c.phase("fire", 0.0, 0.3)) * a_main
        if oa > 0:
            outline(dax.text(NX, 1.55, "threshold = 1", ha="center", fontsize=27, fontweight="bold",
                             color=PURPLE, alpha=oa, zorder=8))
            dax.annotate("", xy=(4.3, 0), xytext=(NX + NR, 0), zorder=6,
                         arrowprops=dict(arrowstyle="-|>", color=GREEN if fired else GREY, lw=4,
                                         alpha=oa, mutation_scale=30))
            res, col = ("GO PLAY!", GREEN) if fired else ("stay home", PINK)
            dax.add_patch(FancyBboxPatch((2.75, -1.3), 2.25, 0.85, boxstyle="round,pad=0,rounding_size=0.15",
                                         facecolor="#0e1d3f", edgecolor=col, lw=2.5, alpha=oa, zorder=6))
            dax.text(3.875, -0.875, res, ha="center", va="center", fontsize=26, fontweight="bold", color=col,
                     alpha=oa, zorder=7)
            dax.text(3.875, 0.45, "output: " + ("1" if fired else "0"), ha="center", fontsize=24,
                     fontweight="bold", color=col, alpha=oa, zorder=7)

    # zoom out: a whole network
    if net > 0:
        layers = [3, 5, 5, 2]
        xs_l = [-4.0, -1.3, 1.4, 4.0]
        pos = [[(x, (j - (n - 1) / 2) * 1.25) for j in range(n)] for x, n in zip(xs_l, layers)]
        for L in range(3):
            for p in pos[L]:
                for q in pos[L + 1]:
                    dax.plot([p[0], q[0]], [p[1], q[1]], color=CYAN, lw=1.2, alpha=0.35 * net, zorder=2)
        # pulses travelling left to right
        f = (c.t * 0.6) % 1
        L = min(2, int(f * 3)); ff = f * 3 - L
        for p in pos[L]:
            for q in pos[L + 1][::2][:2]:
                dax.add_patch(Circle((lerp(p[0], q[0], ff), lerp(p[1], q[1], ff)), 0.07, color=GOLD,
                                     alpha=net * 0.9, zorder=4))
        for L, col in zip(range(4), [GREEN, CYAN, CYAN, PINK]):
            for p in pos[L]:
                dax.add_patch(Circle(p, 0.32, facecolor="#16295a", edgecolor=col, lw=2.5, alpha=net, zorder=5))
        for x, lab in zip(xs_l, ["input", "hidden", "hidden", "output"]):
            outline(dax.text(x, -3.45, lab, ha="center", fontsize=24, fontweight="bold", color=LTGREY,
                             alpha=net, zorder=6))

    # the rule, under the drawing
    ra = ease(c.phase("sum", 0.55, 0.8)) * (1 - ease(c.phase("net", 0.0, 0.2)))
    if ra > 0:
        c.text(0.5, 0.345, r"$z = w_1x_1 + w_2x_2 + w_3x_3$", size=40, color=WHITE, alpha=ra)
    fa = ease(c.phase("fire", 0.2, 0.5)) * (1 - ease(c.phase("net", 0.0, 0.2)))
    if fa > 0:
        c.pill(0.5, 0.285, 0.62, 0.056, GOLD, alpha=fa, dark="#2a2000")
        c.text(0.5, 0.285, "fires if  z ≥ threshold", size=38, color=GOLD, alpha=fa)
