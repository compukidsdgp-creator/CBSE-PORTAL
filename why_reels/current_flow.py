"""WHY? — Why doesn't current get USED UP in a circuit?  (Class 10 Electricity)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why isn't current USED UP by a bulb?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",   "A bulb glows using current. So does less current come out of the bulb than goes in? No! Here's why.",
               "A bulb glows using current… so does LESS current come out? NO! Here's why.", 4.6),
    ("loop",   "A circuit is a closed loop. Electrons flow all the way round, from the battery, through the bulb, and back.",
               "A circuit is a CLOSED LOOP: electrons flow round — battery → bulb → back again.", 5.4),
    ("meters", "Put an ammeter before the bulb, and one after it. Both read exactly the same current.",
               "Ammeter BEFORE the bulb, ammeter AFTER it: both read the SAME current.", 4.6),
    ("energy", "Electrons can't disappear. What the bulb uses is their energy. They pass through with less energy, "
               "and the battery gives it back.",
               "Electrons can't vanish. The bulb uses their ENERGY — the battery gives it back.", 6.0),
    ("chain",  "Think of a bicycle chain. The chain is never used up. It just carries energy from the pedals to the wheel.",
               "Like a bicycle CHAIN: never used up — it just CARRIES energy from pedals to wheel.", 5.4),
    ("math",   "So current in equals current out. Energy is what gets used.",
               "Current in = current out. ENERGY is what gets used!", 3.8),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """💡 WHY? — Why doesn't a bulb "use up" current?

A circuit is a closed loop 🔁 — electrons go round and round.
Ammeter before the bulb = ammeter after the bulb ✅ (same current!)

What the bulb uses is ENERGY ⚡, not electrons.
Electrons leave the bulb with less energy — the battery tops them up 🔋

Think of a bicycle chain 🚲: the chain isn't used up, it CARRIES energy.

Electricity — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Electricity #Class10Science #ElectricCurrent #Physics #CBSE #BoardExams"""

X0, X1, Y0, Y1 = -2.4, 2.4, -1.5, 1.5
PER = 2 * (X1 - X0) + 2 * (Y1 - Y0)


def on_loop(s):
    """Point at arc length fraction s (0..1), clockwise from top-left corner."""
    d = (s % 1.0) * PER
    w, h = X1 - X0, Y1 - Y0
    if d < w:
        return X0 + d, Y1
    d -= w
    if d < h:
        return X1, Y1 - d
    d -= h
    if d < w:
        return X1 - d, Y0
    d -= w
    return X0, Y0 + d


def draw(c):
    dax = c.area(0.0, 0.05, 7.0)
    chain_a = ease(c.phase("chain", 0.0, 0.25)) * (1 - ease(c.phase("math", 0.0, 0.3)))
    ca = ease(c.phase("hook", 0.1, 0.5)) * (1 - chain_a)
    if ca > 0.01:
        dax.add_patch(Rectangle((X0, Y0), X1 - X0, Y1 - Y0, fill=False, edgecolor=LTGREY, lw=5, alpha=ca, zorder=3))
        # battery on the left side
        dax.add_patch(Rectangle((X0 - 0.3, -0.35), 0.6, 0.7, facecolor=NAVY, edgecolor="none", zorder=4, alpha=ca))
        dax.plot([X0 - 0.3, X0 + 0.3], [0.12, 0.12], color=GOLD, lw=6, alpha=ca, zorder=5)
        dax.plot([X0 - 0.17, X0 + 0.17], [-0.12, -0.12], color=GOLD, lw=10, alpha=ca, zorder=5)
        outline(dax.text(X0 + 0.42, 0.0, "battery", ha="left", va="center", fontsize=20, color=GOLD,
                         fontweight="bold", alpha=ca, zorder=6))
        # bulb on the top side
        glow = 0.5 + 0.5 * ease(c.phase("hook", 0.3, 0.8))
        for r, al in ((0.75, 0.10), (0.55, 0.18), (0.38, 0.35)):
            dax.add_patch(Circle((0, Y1), r, color=GOLD, alpha=al * glow * ca, zorder=4, lw=0))
        dax.add_patch(Circle((0, Y1), 0.28, facecolor="#fff3b0", edgecolor=GOLD, lw=3, alpha=ca, zorder=5))
        outline(dax.text(0, Y1 + 0.55, "bulb", ha="center", fontsize=20, color=GOLD, fontweight="bold",
                         alpha=ca, zorder=6))
        # electrons moving clockwise round the loop
        ea = ease(c.phase("loop", 0.15, 0.4)) * ca
        if ea > 0:
            energy_on = ease(c.phase("energy", 0.15, 0.4))
            speed = 0.06
            for k in range(22):
                s = (k / 22 + speed * c.t) % 1.0
                x, y = on_loop(s)
                # energy: bright from battery (s≈0.85..1 → left side) up to bulb (top middle s≈0.1), dim after
                after_bulb = 0.104 < s < 0.875
                col = GOLD if (not after_bulb or energy_on == 0) else lerp_col(energy_on)
                dax.add_patch(Circle((x, y), 0.11, color=col, alpha=ea, zorder=6, lw=0))
            outline(dax.text(-1.2, Y1 + 0.32, "e⁻ →", ha="center", fontsize=22, color=CYAN, fontweight="bold",
                             alpha=ea * (1 - energy_on), zorder=6))
        # two ammeters
        ma = back_out(c.phase("meters", 0.1, 0.45)) * ca
        if ma > 0.01:
            for x, lab in ((-1.25, "before"), (1.25, "after")):
                dax.add_patch(Circle((x, Y1), 0.36 * min(1, ma), facecolor="#13264d", edgecolor=CYAN, lw=3,
                                     alpha=min(1, ma), zorder=7))
                dax.text(x, Y1, "A", ha="center", va="center", fontsize=22, color=CYAN, fontweight="bold",
                         alpha=min(1, ma), zorder=8)
                ra = ease(c.phase("meters", 0.35, 0.6)) * ca
                outline(dax.text(x, Y1 - 0.75, f"{lab}\n0.5 A", ha="center", va="center", fontsize=22,
                                 color=GREEN, fontweight="bold", alpha=ra, zorder=8, linespacing=1.1))
        en = ease(c.phase("energy", 0.3, 0.6)) * ca
        if en > 0:
            outline(dax.text(1.25, -0.25, "same electrons,\nless energy", ha="center", va="center", fontsize=20,
                             color=PURPLE, fontweight="bold", alpha=en, zorder=8))
            outline(dax.text(-1.0, -0.95, "energy\ntopped up", ha="center", va="center", fontsize=20,
                             color=GOLD, fontweight="bold", alpha=en, zorder=8))
    # bicycle chain analogy
    if chain_a > 0.01:
        p1, p2 = (-1.6, -0.2), (1.7, -0.2)
        r1, r2 = 0.95, 0.55
        dax.add_patch(Circle(p1, r1, fill=False, edgecolor=GOLD, lw=5, alpha=chain_a, zorder=4))
        dax.add_patch(Circle(p2, r2, fill=False, edgecolor=CYAN, lw=5, alpha=chain_a, zorder=4))
        dax.plot([p1[0], p2[0]], [p1[1] + r1, p2[1] + r2], color=LTGREY, lw=4, alpha=chain_a, zorder=3)
        dax.plot([p1[0], p2[0]], [p1[1] - r1, p2[1] - r2], color=LTGREY, lw=4, alpha=chain_a, zorder=3)
        for k in range(14):
            f = (k / 14 + 0.08 * c.t) % 1.0
            if f < 0.5:
                g = f / 0.5
                x, y = lerp(p1[0], p2[0], g), lerp(p1[1] + r1, p2[1] + r2, g)
            else:
                g = (f - 0.5) / 0.5
                x, y = lerp(p2[0], p1[0], g), lerp(p2[1] - r2, p1[1] - r1, g)
            dax.add_patch(Circle((x, y), 0.09, color=WHITE, alpha=chain_a, zorder=5, lw=0))
        outline(dax.text(p1[0], p1[1], "pedals\n(battery)", ha="center", va="center", fontsize=19, color=GOLD,
                         fontweight="bold", alpha=chain_a, zorder=6))
        outline(dax.text(p2[0], p2[1] - 1.05, "wheel\n(bulb)", ha="center", va="center", fontsize=19, color=CYAN,
                         fontweight="bold", alpha=chain_a, zorder=6))
        outline(dax.text(0.05, 1.55, "chain = electrons: never used up", ha="center", fontsize=21, color=WHITE,
                         fontweight="bold", alpha=chain_a, zorder=6))
    c.steps([("current in  =  current out", 0.0, WHITE),
             ("ENERGY is what gets used", 0.3, GOLD)], ys=(0.345, 0.285))


def lerp_col(x):
    """Gold → dim purple as electrons lose energy."""
    from matplotlib.colors import to_rgb
    a, b = np.array(to_rgb(GOLD)), np.array(to_rgb("#6b5a9e"))
    return tuple(a + (b - a) * x)
