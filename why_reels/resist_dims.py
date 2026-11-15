"""WHY? — Why does resistance increase with length but decrease with thickness?  (Class 10 Electricity)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why do LONG, THIN wires resist more?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",   "A longer wire has more resistance. A thicker wire has less. Why do length and thickness matter?",
               "Longer wire → MORE resistance. Thicker wire → LESS. Why?", 4.4),
    ("inside", "Inside a wire, electrons drift through a crowd of vibrating atoms, bumping into them all the way.",
               "Inside a wire, electrons drift through a crowd of atoms — BUMPING all the way.", 4.8),
    ("long",   "Double the length, and each electron has twice as far to travel, so twice the bumps. Resistance doubles.",
               "DOUBLE the length → twice as far → twice the bumps → resistance DOUBLES.", 5.0),
    ("thick",  "Double the area, and it's like opening a second lane. Twice as many electrons flow side by side. Resistance halves.",
               "DOUBLE the area → like a second LANE → twice the flow → resistance HALVES.", 5.4),
    ("rho",    "The material matters too. Copper lets electrons through easily. Nichrome doesn't. That's resistivity, rho.",
               "Material matters too: copper is easy, nichrome is hard. That's RESISTIVITY, ρ.", 5.0),
    ("math",   "So R equals rho L by A.",
               "R = ρ L / A", 3.0),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🔌 WHY? — Why does resistance go UP with length and DOWN with thickness?

Electrons drift through a crowd of vibrating atoms — bumping all the way 💥

📏 Double the length → twice the distance → twice the bumps → R doubles
⭕ Double the area → like an extra lane → twice the flow → R halves
🧪 Material matters: copper (low ρ) vs nichrome (high ρ)

R = ρL / A

Electricity — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Resistance #Resistivity #Class10Science #Electricity #CBSE #BoardExams"""

rng = np.random.default_rng(5)


def wire(dax, x0, y0, L, H, a, label=None, col=GOLD, n_e=6, t=0.0, speed=0.25):
    if a <= 0.01:
        return
    dax.add_patch(FancyBboxPatch((x0, y0 - H / 2), L, H, boxstyle="round,pad=0,rounding_size=0.12",
                                 facecolor="#1b2440", edgecolor=col, lw=3, alpha=a, zorder=4))
    # atoms
    nx, ny = max(2, int(L / 0.42)), max(1, int(H / 0.38))
    for i in range(nx):
        for j in range(ny):
            x = x0 + (i + 0.5) * L / nx + 0.03 * np.sin(t * 20 + i + j)
            y = y0 - H / 2 + (j + 0.5) * H / ny + 0.03 * np.cos(t * 23 + i * 2)
            dax.add_patch(Circle((x, y), 0.08, color=GREY, alpha=a * 0.8, zorder=5))
    # electrons drifting left → right
    for k in range(n_e):
        f = (k / n_e + speed * t / max(L, 0.5)) % 1.0
        y = y0 - H / 2 + H * ((k * 0.37) % 1.0 * 0.8 + 0.1)
        dax.add_patch(Circle((x0 + 0.1 + (L - 0.2) * f, y + 0.05 * np.sin(t * 15 + k)), 0.075, color=CYAN,
                             alpha=a, zorder=6))
    if label:
        outline(dax.text(x0 + L + 0.15, y0, label, ha="left", va="center", fontsize=22, color=col,
                         fontweight="bold", alpha=a, zorder=7))


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    t = c.t
    rh = ease(c.phase("rho", 0.0, 0.25))
    a0 = ease(c.phase("hook", 0.05, 0.35)) * (1 - rh)
    ins = ease(c.phase("inside", 0.0, 0.3))
    if a0 > 0.01:
        lo = ease(c.phase("long", 0.1, 0.5))
        th = ease(c.phase("thick", 0.1, 0.5))
        if lo < 0.01 and th < 0.01:
            # hook / inside: one wire, zoomed as we go inside
            H = lerp(0.35, 1.6, ins)
            wire(dax, -2.6, 0.4, 4.6, H, a0, t=t, n_e=int(lerp(0, 10, ins)), speed=0.25)
            if ins > 0.3:
                outline(dax.text(0, -1.0, "bump · bump · bump", ha="center", fontsize=26, color=PINK, fontweight="bold",
                                 alpha=a0 * ins, zorder=8))
        if lo > 0.01 and th < 0.01:
            wire(dax, -3.1, 1.5, 2.0, 0.7, lo * a0, label="L → R", col=GOLD, t=t, n_e=4)
            wire(dax, -3.1, 0.0, 4.0, 0.7, lo * a0, label="2L → 2R", col=PINK, t=t, n_e=4)
            outline(dax.text(0, -1.4, "twice the distance = twice the bumps", ha="center", fontsize=21, color=WHITE,
                             fontweight="bold", alpha=lo * a0 * (1 - th), zorder=8))
        if th > 0.01:
            wire(dax, -3.1, 1.75, 3.6, 0.6, th * a0, label="A → R", col=GOLD, t=t, n_e=4)
            wire(dax, -3.1, 0.15, 3.6, 1.2, th * a0, label="2A → R/2", col=GREEN, t=t, n_e=9)
            outline(dax.text(0, -1.4, "an extra lane = twice the flow", ha="center", fontsize=22, color=WHITE,
                             fontweight="bold", alpha=th * a0, zorder=8))
    if rh > 0.01:
        rr = rh * (1 - ease(c.phase("math", 0.0, 0.3)))
        for k, (name, rho, col, speed) in enumerate((("copper", "ρ low", CYAN, 0.6), ("nichrome", "ρ high", PINK, 0.12))):
            y = 1.3 - 2.0 * k
            wire(dax, -3.1, y, 3.6, 0.8, rr * ease(c.phase("rho", 0.15 + 0.25 * k, 0.4 + 0.25 * k)), col=col, t=t,
                 n_e=6, speed=speed)
            outline(dax.text(0.7, y + 0.15, name, ha="left", va="center", fontsize=24, color=col, fontweight="bold",
                             alpha=rr, zorder=8))
            outline(dax.text(0.7, y - 0.35, rho, ha="left", va="center", fontsize=20, color=LTGREY, fontweight="bold",
                             alpha=rr, zorder=8))
    ma = ease(c.phase("math", 0.0, 0.35))
    if ma > 0.01:
        outline(dax.text(0, 0.3, r"$R = \dfrac{\rho\,L}{A}$", ha="center", va="center", fontsize=60, color=GOLD,
                         alpha=ma, zorder=8))
    c.steps([("R ∝ length,  R ∝ 1 / area", 0.0, WHITE),
             ("$R = \\rho L / A$", 0.3, GOLD)], ys=(0.345, 0.285))
