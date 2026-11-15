"""WHY? — Why does reaction rate increase with temperature (collision theory)?  (Class 12 Chemical Kinetics)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why do reactions go FASTER when HOT?"
TAGS = "Class 12 Chemistry"
BEATS = [
    ("hook",   "Milk spoils faster in summer. Food cooks faster on high flame. Why does heat speed up reactions?",
               "Milk spoils faster in summer, food cooks faster on high flame. Why does HEAT speed reactions?", 5.0),
    ("collide", "For a reaction, molecules must collide. But most collisions just bounce off.",
                "To react, molecules must COLLIDE… but most collisions just bounce off.", 4.2),
    ("ea",     "Only collisions with enough energy, at least the activation energy, break bonds and react.",
               "Only collisions with ENOUGH energy (≥ activation energy, Ea) actually react.", 4.8),
    ("heat",   "Heat it up. Molecules move faster, so they collide more often, and much harder.",
               "Heat it: molecules move FASTER → collide more often, and HARDER.", 4.4),
    ("curve",  "The big effect: many more molecules now have energy above the activation energy. The shaded area grows a lot.",
               "Big effect: MANY more molecules now cross Ea — the shaded area grows a lot!", 5.6),
    ("rule",   "Roughly, every ten degree rise nearly doubles the rate.",
               "Rule of thumb: every 10 °C rise ≈ DOUBLES the rate.", 3.8),
    ("math",   "Higher temperature, more effective collisions, faster reaction.",
               "Higher T → more effective collisions → faster reaction.", 3.8),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🔥 WHY? — Why do reactions go FASTER at higher temperature?

Collision theory 💥
• Molecules must COLLIDE to react
• Only collisions with energy ≥ activation energy (Ea) are effective

Heat it up:
✅ molecules move faster → more collisions
✅ MANY more molecules cross Ea (the big effect!)

Rule of thumb: every 10 °C rise ≈ doubles the rate. (Milk spoils faster in summer 🥛)

Chemical Kinetics — Class 12 Chemistry. 📗

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #CollisionTheory #ChemicalKinetics #ActivationEnergy #Class12Chemistry #NEET #CBSE"""

rng = np.random.default_rng(4)
P0 = rng.uniform([-2.6, -1.2], [2.6, 2.0], (14, 2))
V0 = rng.normal(0, 1, (14, 2))


def box_pos(t, speed):
    p = P0 + V0 * speed * t
    lo, hi = np.array([-2.6, -1.2]), np.array([2.6, 2.0])
    span = hi - lo
    q = (p - lo) % (2 * span)
    q = np.where(q > span, 2 * span - q, q)
    return lo + q


def mb(E, T):
    return (E ** 0.5) * np.exp(-E / T) / (T ** 1.5)


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    t = c.t
    cu = ease(c.phase("curve", 0.0, 0.25))
    a0 = ease(c.phase("hook", 0.05, 0.35)) * (1 - cu)
    if a0 > 0.01:
        hot = ease(c.phase("heat", 0.1, 0.5))
        speed = lerp(0.35, 1.0, hot)
        dax.add_patch(Rectangle((-2.85, -1.45), 5.7, 3.7, fill=False, edgecolor=PINK if hot > 0.5 else CYAN, lw=4,
                                alpha=a0, zorder=4))
        pos = box_pos(t, speed)
        for k, (x, y) in enumerate(pos):
            dax.add_patch(Circle((x, y), 0.2, facecolor=GOLD if k % 2 else CYAN, edgecolor=NAVY, lw=2, alpha=a0, zorder=5))
        # flash where two are close
        hits = 0
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                if np.linalg.norm(pos[i] - pos[j]) < 0.45:
                    hits += 1
                    m = (pos[i] + pos[j]) / 2
                    eff = (hot > 0.5 and (i + j) % 2 == 0) or (i + j) % 5 == 0
                    dax.add_patch(Circle(m, 0.32, color=GREEN if eff else WHITE, alpha=a0 * 0.45, zorder=6))
        outline(dax.text(0, 2.45, ("HOT 🔥" if False else "HOT") if hot > 0.5 else "cool", ha="center", fontsize=24,
                         color=PINK if hot > 0.5 else CYAN, fontweight="bold", alpha=a0 * ease(c.phase("collide", 0.0, 0.3)),
                         zorder=8))
        ea = ease(c.phase("ea", 0.1, 0.4)) * (1 - ease(c.phase("heat", 0.0, 0.1)))
        if ea > 0:
            outline(dax.text(0, -1.95, "white = bounce · green = REACT", ha="center", fontsize=21, color=WHITE,
                             fontweight="bold", alpha=ea * a0, zorder=8))
        if c.phase("heat", 0.1, 0.3) > 0:
            outline(dax.text(0, -1.95, "faster · more often · harder", ha="center", fontsize=22, color=PINK,
                             fontweight="bold", alpha=hot * a0, zorder=8))
    if cu > 0.01:
        cc = cu * (1 - ease(c.phase("math", 0.0, 0.3)))
        x0, y0, W, H = -3.0, -1.6, 6.0, 3.6
        E = np.linspace(0.001, 6, 300)
        T1, T2 = 0.8, lerp(0.8, 1.3, ease(c.phase("curve", 0.2, 0.7)))
        s = H / (mb(E, 0.8).max() * 1.15)
        X = x0 + W * E / 6
        dax.plot([x0, x0 + W], [y0, y0], color=LTGREY, lw=2, alpha=cc, zorder=4)
        dax.plot([x0, x0], [y0, y0 + H], color=LTGREY, lw=2, alpha=cc, zorder=4)
        dax.plot(X, y0 + s * mb(E, T1), color=CYAN, lw=4, alpha=cc, zorder=5)
        dax.plot(X, y0 + s * mb(E, T2), color=PINK, lw=4, alpha=cc * ease(c.phase("curve", 0.15, 0.4)), zorder=5)
        Ea = 3.4
        xe = x0 + W * Ea / 6
        dax.plot([xe, xe], [y0, y0 + H * 0.85], color=GOLD, lw=3, ls=(0, (5, 4)), alpha=cc, zorder=5)
        outline(dax.text(xe, y0 + H * 0.9, "Ea", ha="center", fontsize=26, color=GOLD, fontweight="bold", alpha=cc, zorder=8))
        m = E >= Ea
        dax.fill_between(X[m], y0, y0 + s * mb(E[m], T1), color=CYAN, alpha=0.45 * cc, zorder=4, lw=0)
        dax.fill_between(X[m], y0, y0 + s * mb(E[m], T2), color=PINK, alpha=0.30 * cc * ease(c.phase("curve", 0.3, 0.6)),
                         zorder=3, lw=0)
        outline(dax.text(-1.6, 1.7, "cool", ha="center", fontsize=22, color=CYAN, fontweight="bold", alpha=cc, zorder=8))
        outline(dax.text(0.2, 0.6, "hot", ha="center", fontsize=22, color=PINK, fontweight="bold",
                         alpha=cc * ease(c.phase("curve", 0.3, 0.5)), zorder=8))
        outline(dax.text(x0 + W, y0 - 0.35, "energy →", ha="right", fontsize=18, color=LTGREY, fontweight="bold",
                         alpha=cc, zorder=8))
        ra = ease(c.phase("rule", 0.1, 0.4)) * cc
        if ra > 0:
            dax.add_patch(FancyBboxPatch((0.85, 0.15), 2.2, 1.0, boxstyle="round,pad=0,rounding_size=0.2",
                                         facecolor="#13264d", edgecolor=GOLD, lw=3, alpha=ra, zorder=9))
            dax.text(1.95, 0.65, "+10 °C ≈ ×2", ha="center", va="center", fontsize=26, color=GOLD, fontweight="bold",
                     alpha=ra, zorder=10)
    mm = ease(c.phase("math", 0.0, 0.35))
    if mm > 0.01:
        for k, (s_, col) in enumerate((("higher T", PINK), ("more effective collisions", GOLD), ("faster reaction", GREEN))):
            outline(dax.text(0, 1.4 - 1.1 * k, s_, ha="center", fontsize=30, color=col, fontweight="bold",
                             alpha=mm * ease(c.phase("math", 0.1 * k, 0.3 + 0.1 * k)), zorder=8))
    c.steps([("only collisions ≥ Ea react", 0.0, WHITE),
             ("hotter → many more cross Ea", 0.3, GOLD)], ys=(0.345, 0.285))
