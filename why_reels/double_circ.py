"""WHY? — Why is double circulation more efficient than single circulation?  (Class 10 Life Processes)"""
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does blood pass the heart TWICE?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",    "In one trip around your body, your blood passes through the heart twice. Why not just once, like in fish?",
                "In ONE trip round the body, your blood passes the heart TWICE. Why not once, like fish?", 5.0),
    ("single",  "In a fish, the heart pumps blood to the gills, then straight on to the body. "
                "After squeezing through the gills, the pressure drops. Blood reaches the body slowly.",
                "FISH: heart → gills → body. After the gills, pressure DROPS — blood reaches the body slowly.", 6.4),
    ("double",  "In us, the heart sends blood to the lungs, gets it back, and pumps it again to the body. Two loops!",
                "US: heart → lungs → heart → body → heart. TWO loops!", 4.8),
    ("pressure", "The second pump restores high pressure, so oxygen rich blood rushes to every part of the body.",
                 "The SECOND pump restores high pressure → oxygen-rich blood rushes everywhere.", 4.8),
    ("separate", "And four chambers keep oxygen rich and oxygen poor blood completely separate. No mixing.",
                 "And 4 chambers keep oxygen-rich and oxygen-poor blood SEPARATE — no mixing.", 4.8),
    ("need",    "Birds and mammals need this. Keeping a warm body temperature takes a lot of energy, so a lot of oxygen.",
                "Birds & mammals need it: keeping the body WARM takes lots of energy → lots of oxygen.", 5.2),
    ("math",    "Two pumps, no mixing, more oxygen, more energy.",
                "Two pumps + no mixing = more oxygen = more energy.", 3.6),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """❤️ WHY? — Why is DOUBLE circulation better than single?

🐟 Fish (single): heart → gills → body → heart
Pressure drops after the gills → slow supply to the body

🧍 Humans (double): heart → lungs → heart → body → heart
✅ second pump restores high pressure
✅ 4 chambers keep oxygenated & deoxygenated blood separate

Warm-blooded birds & mammals need lots of energy → lots of oxygen 🔥

Life Processes: Transportation — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #DoubleCirculation #Heart #Class10Science #LifeProcesses #CBSE #BoardExams"""

RED, BLUE = "#e63946", "#3a86ff"


def loop_pts(cx, cy, rx, ry, n=200):
    th = np.linspace(0, 2 * np.pi, n)
    return cx + rx * np.cos(th), cy + ry * np.sin(th)


def organ(dax, x, y, w, h, lab, col, a):
    dax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.2",
                                 facecolor="#13264d", edgecolor=col, lw=3, alpha=a, zorder=6))
    dax.text(x, y, lab, ha="center", va="center", fontsize=20, color=col, fontweight="bold", alpha=a, zorder=7)


def heart(dax, x, y, a, s=1.0, four=False):
    dax.add_patch(Circle((x, y), 0.45 * s, facecolor="#5c1a24", edgecolor=PINK, lw=3, alpha=a, zorder=7))
    if four:
        dax.plot([x - 0.45 * s, x + 0.45 * s], [y, y], color=PINK, lw=2, alpha=a, zorder=8)
        dax.plot([x, x], [y - 0.45 * s, y + 0.45 * s], color=PINK, lw=2, alpha=a, zorder=8)
        dax.add_patch(Circle((x - 0.2 * s, y + 0.2 * s), 0.08, color=BLUE, alpha=a, zorder=9))
        dax.add_patch(Circle((x + 0.2 * s, y + 0.2 * s), 0.08, color=RED, alpha=a, zorder=9))


def dots(dax, xs, ys, t, a, cols, n=14, speed=0.12, slow=None):
    L = len(xs)
    for k in range(n):
        f = (k / n + speed * t) % 1.0
        if slow:      # slow down after a point
            f = f if f < slow else slow + (f - slow) * 0.55
        i = int(f * (L - 1)) % L
        dax.add_patch(Circle((xs[i], ys[i]), 0.1, color=cols(f), alpha=a, zorder=6))


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    t = c.t
    a0 = ease(c.phase("hook", 0.05, 0.35))
    db = ease(c.phase("double", 0.0, 0.25))
    nd = ease(c.phase("need", 0.0, 0.25))
    ma = ease(c.phase("math", 0.0, 0.3))
    si = a0 * (1 - db)
    if si > 0.01:
        xs, ys = loop_pts(0, 0.2, 2.4, 1.6)
        dax.plot(xs, ys, color=LTGREY, lw=3, alpha=si * 0.5, zorder=4)
        heart(dax, 0, -1.4, si)
        organ(dax, 0, 1.8, 1.8, 0.7, "gills", CYAN, si)
        organ(dax, 2.4, 0.2, 1.4, 0.7, "body", GOLD, si)
        sa = ease(c.phase("single", 0.1, 0.4))
        if sa > 0:
            # anticlockwise from heart (bottom) → gills (top) via left, then body (right), back to heart
            order = np.r_[np.arange(150, 200), np.arange(0, 150)][::-1]
            px, py = xs[order], ys[order]
            dots(dax, px, py, t, si * sa, lambda f: RED if 0.25 < f < 0.85 else BLUE, n=12, speed=0.1)
            outline(dax.text(-2.2, 2.3, "1 pump", ha="center", fontsize=22, color=PINK, fontweight="bold",
                             alpha=si * sa, zorder=8))
            outline(dax.text(1.9, -1.6, "pressure drops ↓", ha="center", fontsize=21, color=PINK, fontweight="bold",
                             alpha=si * ease(c.phase("single", 0.5, 0.8)), zorder=8))
        outline(dax.text(-2.3, -1.6, "FISH", ha="center", fontsize=26, color=CYAN, fontweight="bold", alpha=si, zorder=8))
    dd = db * (1 - nd)
    if dd > 0.01:
        four = ease(c.phase("separate", 0.1, 0.4)) > 0.5
        x1, y1 = loop_pts(0, 1.1, 1.6, 0.9)      # lung loop (top)
        x2, y2 = loop_pts(0, -1.0, 2.3, 1.1)     # body loop (bottom)
        dax.plot(x1, y1, color=LTGREY, lw=3, alpha=dd * 0.5, zorder=4)
        dax.plot(x2, y2, color=LTGREY, lw=3, alpha=dd * 0.5, zorder=4)
        heart(dax, 0, 0.15, dd, 1.15, four)
        organ(dax, 0, 2.2, 1.7, 0.6, "lungs", CYAN, dd)
        organ(dax, 0, -2.25, 1.7, 0.6, "body", GOLD, dd)
        dots(dax, x1, y1, t, dd, lambda f: RED if f < 0.5 else BLUE, n=10, speed=0.16)
        dots(dax, x2, y2, t, dd, lambda f: BLUE if f < 0.5 else RED, n=12, speed=0.16)
        outline(dax.text(-2.35, 1.6, "loop 1", ha="center", fontsize=21, color=CYAN, fontweight="bold", alpha=dd, zorder=8))
        outline(dax.text(-2.75, -0.2, "loop 2", ha="center", fontsize=21, color=GOLD, fontweight="bold", alpha=dd, zorder=8))
        pa = ease(c.phase("pressure", 0.1, 0.4)) * (1 - ease(c.phase("separate", 0.0, 0.2)))
        if pa > 0:
            outline(dax.text(2.0, 0.15, "2nd pump:\nHIGH pressure", ha="center", va="center", fontsize=20, color=PINK,
                             fontweight="bold", alpha=dd * pa, zorder=8))
        sa = ease(c.phase("separate", 0.2, 0.5))
        if sa > 0:
            outline(dax.text(2.05, 0.15, "4 chambers:\nno mixing", ha="center", va="center", fontsize=20, color=GREEN,
                             fontweight="bold", alpha=dd * sa, zorder=8))
    if nd > 0.01:
        n = nd * (1 - ma)
        for k, (lab, col) in enumerate((("birds", CYAN), ("mammals", GOLD))):
            dax.add_patch(FancyBboxPatch((-2.9 + 3.0 * k, -0.2), 2.8, 1.4, boxstyle="round,pad=0,rounding_size=0.2",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=n, zorder=6))
            dax.text(-1.5 + 3.0 * k, 0.5, lab, ha="center", va="center", fontsize=26, color=col, fontweight="bold",
                     alpha=n, zorder=7)
        outline(dax.text(0, 1.9, "warm body = 37 °C", ha="center", fontsize=28, color=PINK, fontweight="bold", alpha=n, zorder=8))
        outline(dax.text(0, -1.0, "needs lots of energy → lots of O₂", ha="center", fontsize=22, color=WHITE,
                         fontweight="bold", alpha=n * ease(c.phase("need", 0.4, 0.7)), zorder=8))
    if ma > 0.01:
        for k, (s, col) in enumerate((("2 pumps", PINK), ("no mixing", GREEN), ("more O₂ → more energy", GOLD))):
            outline(dax.text(0, 1.4 - 1.1 * k, s, ha="center", fontsize=32, color=col, fontweight="bold",
                             alpha=ma * ease(c.phase("math", 0.1 * k, 0.3 + 0.1 * k)), zorder=8))
    c.steps([("blood passes the heart twice", 0.0, WHITE),
             ("high pressure + no mixing", 0.3, GOLD)], ys=(0.345, 0.285))
