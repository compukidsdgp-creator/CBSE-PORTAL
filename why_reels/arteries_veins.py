"""WHY? — Why do we need both arteries and veins?  (Class 10 Life Processes: Transportation)"""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle, Wedge
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why do we need BOTH arteries and veins?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",    "Why does your body need two kinds of blood vessels? Wouldn't one type of tube be simpler?",
                "Why TWO kinds of blood vessels? Wouldn't one type of tube be simpler?", 4.2),
    ("pump",    "Every heartbeat blasts blood out at high pressure. On the way back, the pressure is very low.",
                "Every heartbeat blasts blood OUT at HIGH pressure. On the way BACK, pressure is LOW.", 5.0),
    ("artery",  "Arteries carry blood away from the heart. They have thick, elastic, muscular walls to take the pressure surge. "
                "That's your pulse.",
                "ARTERIES carry blood AWAY: thick, elastic, muscular walls take the surge — that's your PULSE.", 6.0),
    ("vein",    "Veins bring blood back to the heart. Low pressure, so thin walls and a wide space inside. "
                "And valves, so blood can't flow backwards.",
                "VEINS bring blood BACK: low pressure → thin walls, wide space, and VALVES to stop backflow.", 6.0),
    ("cap",     "In between, tiny capillaries, just one cell thick, let oxygen and food pass into the cells.",
                "In between, tiny CAPILLARIES — one cell thick — swap oxygen and food with the cells.", 4.8),
    ("math",    "Different jobs, different pressures, different designs.",
                "Different jobs + different pressures = different designs.", 3.6),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """❤️ WHY? — Why do we need BOTH arteries and veins?

The heart blasts blood out at HIGH pressure; it comes back at LOW pressure.

🔴 Arteries (away from heart): thick, elastic, muscular walls → handle the surge (your pulse!)
🔵 Veins (back to heart): thin walls, wide lumen + VALVES to stop backflow
🟣 Capillaries: one cell thick → exchange of O₂, food and wastes

Different jobs, different pressures → different designs!

Life Processes: Transportation — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Arteries #Veins #Circulation #Class10Science #LifeProcesses #CBSE"""

RED, BLUE = "#e63946", "#3a86ff"


def section(dax, x, y, R, wall, col, a, label, sub):
    if a <= 0.01:
        return
    dax.add_patch(Circle((x, y), R, facecolor="#d98aa0", edgecolor="#a04a64", lw=2, alpha=a, zorder=5))
    dax.add_patch(Circle((x, y), R - wall, facecolor=col, edgecolor="#5c1a24", lw=2, alpha=a, zorder=6))
    outline(dax.text(x, y - R - 0.35, label, ha="center", fontsize=26, color=WHITE, fontweight="bold", alpha=a, zorder=8))
    outline(dax.text(x, y - R - 0.85, sub, ha="center", fontsize=18, color=LTGREY, fontweight="bold", alpha=a, zorder=8,
                     linespacing=1.1, va="top"))


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    t = c.t
    a0 = ease(c.phase("hook", 0.05, 0.35))
    cap = ease(c.phase("cap", 0.0, 0.25))
    ma = ease(c.phase("math", 0.0, 0.3))
    main = a0 * (1 - cap)
    hk = a0 * (1 - ease(c.phase("pump", 0.0, 0.2)))
    if hk > 0.01:      # hook: two different tubes, one question
        for x, col, lab in ((-1.5, RED, "artery"), (1.5, BLUE, "vein")):
            dax.add_patch(FancyBboxPatch((x - 0.45, -1.2), 0.9, 3.0, boxstyle="round,pad=0,rounding_size=0.4",
                                         facecolor=col, edgecolor="#d98aa0", lw=6 if col == RED else 2, alpha=hk, zorder=5))
            outline(dax.text(x, -1.65, lab, ha="center", fontsize=24, color=col, fontweight="bold", alpha=hk, zorder=8))
        outline(dax.text(0, 0.3, "?", ha="center", va="center", fontsize=60, color=WHITE, fontweight="bold",
                         alpha=hk * ease(c.phase("hook", 0.3, 0.6)), zorder=8))
    if main > 0.01:
        pu = ease(c.phase("pump", 0.05, 0.4))
        # pressure gauge bars (out vs back)
        if pu > 0 and not c.at("artery"):
            beat = 0.5 + 0.5 * np.sin(t * 7)
            for x, h, col, lab in ((-1.4, 2.6 * (0.75 + 0.25 * beat), RED, "out: HIGH"), (1.4, 0.6, BLUE, "back: LOW")):
                dax.add_patch(Rectangle((x - 0.4, -1.4), 0.8, 3.0, fill=False, edgecolor=LTGREY, lw=2, alpha=pu * main, zorder=4))
                dax.add_patch(Rectangle((x - 0.4, -1.4), 0.8, h, facecolor=col, edgecolor="none", alpha=pu * main, zorder=5))
                outline(dax.text(x, -1.85, lab, ha="center", fontsize=22, color=col, fontweight="bold", alpha=pu * main, zorder=8))
            outline(dax.text(0, 2.1, "blood pressure", ha="center", fontsize=22, color=LTGREY, fontweight="bold",
                             alpha=pu * main, zorder=8))
        ar = ease(c.phase("artery", 0.05, 0.35))
        if ar > 0:
            pulse = 1 + 0.05 * np.sin(t * 7) ** 8
            section(dax, -1.6, 0.9, 1.05 * pulse, 0.45, RED, ar * main, "artery", "thick elastic wall\nhigh pressure")
            ve = ease(c.phase("vein", 0.05, 0.35))
            if ve > 0:
                section(dax, 1.6, 0.9, 1.15, 0.13, BLUE, ve * main, "vein", "thin wall, wide space\n+ valves")
                # valve flaps
                for s in (-1, 1):
                    dax.add_patch(Polygon([(1.6 + s * 1.0, 1.2), (1.6 + s * 0.15, 0.6), (1.6 + s * 1.0, 0.8)],
                                          facecolor="#f1d4dc", edgecolor="#a04a64", lw=1.5, alpha=ve * main, zorder=7))
                # blood can only go one way
                fl = (t * 0.6) % 1.0
                dax.add_patch(Circle((1.6, lerp(0.0, 1.8, fl)), 0.12, color="#9fc3ff", alpha=ve * main, zorder=8))
    if cap > 0.01:
        cc = cap * (1 - ma)
        xs = np.linspace(-3.0, 3.0, 200)
        dax.plot(xs[:40], 0.3 + 0 * xs[:40], color=RED, lw=18, alpha=cc, zorder=4, solid_capstyle="round")
        dax.plot(xs[-40:], 0.3 + 0 * xs[-40:], color=BLUE, lw=18, alpha=cc, zorder=4, solid_capstyle="round")
        for k, amp in enumerate((-1.0, -0.4, 0.4, 1.0)):
            xx = np.linspace(-1.8, 1.8, 120)
            yy = 0.3 + amp * np.sin(np.pi * (xx + 1.8) / 3.6)
            col = [RED, "#b5559a", PURPLE, BLUE]
            for i in range(3):
                seg = slice(i * 40, (i + 1) * 40 + 1)
                dax.plot(xx[seg], yy[seg], color=[RED, PURPLE, BLUE][i], lw=4, alpha=cc, zorder=5)
        # O2 leaving into cells
        for k in range(8):
            f = (k / 8 + 0.3 * t) % 1.0
            x = -1.5 + 3.0 * (k / 8)
            dax.add_patch(Circle((x, lerp(1.0, 2.1, f)), 0.07, color=GOLD, alpha=cc * (1 - f), zorder=6))
        outline(dax.text(-2.6, -0.5, "artery", ha="center", fontsize=20, color=RED, fontweight="bold", alpha=cc, zorder=8))
        outline(dax.text(2.6, -0.5, "vein", ha="center", fontsize=20, color=BLUE, fontweight="bold", alpha=cc, zorder=8))
        outline(dax.text(0, -1.3, "capillaries: 1 cell thick", ha="center", fontsize=24, color=PURPLE, fontweight="bold",
                         alpha=cc, zorder=8))
        outline(dax.text(0, 2.35, "O₂ + food → cells", ha="center", fontsize=20, color=GOLD, fontweight="bold",
                         alpha=cc, zorder=8))
    if ma > 0.01:
        for k, (s, col) in enumerate((("artery: thick · high pressure", RED), ("vein: thin · valves", BLUE),
                                      ("capillary: exchange", PURPLE))):
            outline(dax.text(0, 1.4 - 1.0 * k, s, ha="center", fontsize=28, color=col, fontweight="bold",
                             alpha=ma * ease(c.phase("math", 0.1 * k, 0.3 + 0.1 * k)), zorder=8))
    c.steps([("arteries: away, high pressure", 0.0, WHITE),
             ("veins: back, low pressure + valves", 0.3, GOLD)], ys=(0.345, 0.285))
