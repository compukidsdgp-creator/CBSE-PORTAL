"""WHY? — Why do ionic compounds conduct only when molten or dissolved, not as solids?  (Class 10 Metals and Non-metals)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does SOLID salt NOT conduct electricity?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",   "Salt is made of charged ions. Yet a salt crystal doesn't conduct electricity. Melt it, or dissolve it, and suddenly it does! Why?",
               "Salt is made of charged IONS… yet solid salt won't conduct. Melt or dissolve it — it DOES! Why?", 6.0),
    ("need",   "Electric current needs charged particles that can move.",
               "Current needs charged particles that can MOVE.", 3.2),
    ("solid",  "In a solid crystal, every ion is locked in place by strong attractions. They can only vibrate. No flow, no current.",
               "SOLID: every ion is LOCKED in the lattice — it can only vibrate. No flow → no current.", 5.6),
    ("melt",   "Melt it, or dissolve it in water, and the lattice breaks apart. The ions are free to move.",
               "MELT it or DISSOLVE it → the lattice breaks → ions are FREE to move.", 4.6),
    ("flow",   "Connect a battery. Positive ions drift to the negative electrode, negative ions to the positive one. Current flows! The bulb glows.",
               "Battery on: + ions → cathode, − ions → anode. Current FLOWS — the bulb glows!", 6.0),
    ("math",   "Locked ions, no current. Free ions, current flows.",
               "Locked ions → no current. Free ions → current flows.", 3.6),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """⚡ WHY? — Why do ionic compounds conduct only when MOLTEN or DISSOLVED?

Current needs charged particles that can MOVE.

🧊 Solid: ions locked in the lattice — they only vibrate → no current ❌
🔥 Molten / 💧 dissolved: lattice breaks → ions move freely ✅
➕ ions → cathode (−) · ➖ ions → anode (+) → current flows, bulb glows 💡

Metals and Non-metals — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #IonicCompounds #Electrolysis #Class10Science #Chemistry #CBSE #BoardExams"""

NA, CL = PURPLE, GREEN
rng = np.random.default_rng(9)
FREE = rng.uniform([-2.2, -1.6], [2.2, 1.0], (24, 2))


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    t = c.t
    a0 = ease(c.phase("hook", 0.05, 0.35))
    melt = ease(c.phase("melt", 0.1, 0.7))
    flow = ease(c.phase("flow", 0.1, 0.4))
    ma = ease(c.phase("math", 0.0, 0.3))
    b = a0 * (1 - ma)
    # beaker + electrodes + bulb
    dax.plot([-2.7, -2.7, 2.7, 2.7], [1.5, -2.1, -2.1, 1.5], color=LTGREY, lw=4, alpha=b, zorder=6)
    if melt > 0:
        dax.add_patch(Rectangle((-2.65, -2.05), 5.3, 3.2, facecolor="#1d4e7a", edgecolor="none", alpha=b * 0.45 * melt, zorder=2))
    for x, s, col in ((-2.25, "−", CYAN), (2.25, "+", PINK)):
        dax.add_patch(Rectangle((x - 0.12, -1.8), 0.24, 3.6, color=GREY, alpha=b, zorder=7))
        outline(dax.text(x, 2.05, s, ha="center", va="center", fontsize=30, color=col, fontweight="bold", alpha=b, zorder=8))
    dax.plot([-2.25, -2.25, 2.25, 2.25], [1.8, 2.45, 2.45, 1.8], color=LTGREY, lw=3, alpha=b, zorder=5)
    glow = flow * b
    dax.add_patch(Circle((0, 2.45), 0.3, facecolor="#fff3b0" if glow > 0.3 else "#555", edgecolor=GOLD, lw=3,
                         alpha=b, zorder=8))
    for r, al in ((0.75, 0.12), (0.5, 0.25)):
        dax.add_patch(Circle((0, 2.45), r, color=GOLD, alpha=al * glow, zorder=7))
    # ions
    sp = 0.62
    k = 0
    for i in range(-3, 4):
        for j in range(-2, 2):
            na = (i + j) % 2 == 0
            lx, ly = i * sp, -0.35 + j * sp
            fx, fy = FREE[k % len(FREE)]
            k += 1
            x, y = lerp(lx, fx, melt), lerp(ly, fy, melt)
            # random wander when free, drift when battery on
            x += melt * 0.12 * np.sin(t * 2 + k)
            y += melt * 0.12 * np.cos(t * 1.7 + k * 2)
            if flow > 0:
                dirn = -1 if na else 1
                x = x + dirn * ((t * 0.5 + k * 0.13) % 1.0) * 0.9 * flow
                x = np.clip(x, -1.95, 1.95)
            vib = (1 - melt) * 0.04 * np.sin(t * 25 + k)
            col = NA if na else CL
            dax.add_patch(Circle((x + vib, y), 0.2 if na else 0.26, facecolor=col, edgecolor=NAVY, lw=2,
                                 alpha=b * ease(c.phase("hook", 0.2, 0.5)), zorder=5))
            dax.text(x + vib, y, "+" if na else "−", ha="center", va="center", fontsize=14, color=NAVY, fontweight="bold",
                     alpha=b * ease(c.phase("hook", 0.2, 0.5)), zorder=6)
    na_ = ease(c.phase("need", 0.1, 0.4)) * (1 - ease(c.phase("solid", 0.0, 0.2)))
    if na_ > 0:
        outline(dax.text(0, -2.45, "current = MOVING charges", ha="center", fontsize=23, color=GOLD, fontweight="bold",
                         alpha=na_ * b, zorder=9))
    sa = ease(c.phase("solid", 0.2, 0.5)) * (1 - ease(c.phase("melt", 0.0, 0.15)))
    if sa > 0:
        outline(dax.text(0, -2.45, "locked → only vibrate → no current", ha="center", fontsize=21, color=PINK,
                         fontweight="bold", alpha=sa * b, zorder=9))
    fr = ease(c.phase("melt", 0.2, 0.4)) * (1 - ease(c.phase("flow", 0.0, 0.12)))
    if fr > 0:
        outline(dax.text(0, -2.45, "free to move!", ha="center", fontsize=24, color=GREEN, fontweight="bold",
                         alpha=b * fr, zorder=9))
    if c.phase("flow", 0.12, 0.3) > 0:
        outline(dax.text(0, -2.45, "+ → (−)   and   − → (+)", ha="center", fontsize=23, color=WHITE, fontweight="bold",
                         alpha=b * flow, zorder=9))
    if ma > 0.01:
        outline(dax.text(0, 0.8, "locked ions → no current", ha="center", fontsize=30, color=PINK, fontweight="bold",
                         alpha=ma, zorder=9))
        outline(dax.text(0, -0.4, "free ions → current", ha="center", fontsize=30, color=GREEN, fontweight="bold",
                         alpha=ease(c.phase("math", 0.3, 0.6)), zorder=9))
    c.steps([("solid: ions locked → no current", 0.0, WHITE),
             ("molten / dissolved: ions move", 0.3, GOLD)], ys=(0.345, 0.285))
