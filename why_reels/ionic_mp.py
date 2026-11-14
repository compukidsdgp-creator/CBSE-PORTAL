"""WHY? — Why do ionic compounds have high melting points but covalent compounds don't?  (Class 10 Metals / Carbon)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why do IONIC compounds melt so HIGH?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",    "Salt melts at eight hundred and one degrees. Wax melts at about sixty. Why such a huge gap?",
                "Salt melts at 801 °C. Wax melts at about 60 °C. Why such a HUGE gap?", 4.6),
    ("lattice", "Salt is ionic. It's a giant lattice of positive sodium ions and negative chloride ions.",
                "Salt is IONIC: a giant lattice of Na⁺ and Cl⁻ ions.", 4.6),
    ("pull",    "Every ion is pulled by the opposite charges all around it. These electrostatic forces are very strong.",
                "Every ion is pulled by opposite charges ALL AROUND it — very STRONG forces.", 5.2),
    ("heat",    "To melt it, you must break this whole network. That takes huge energy.",
                "To melt it, you must break the WHOLE network → huge energy needed.", 4.4),
    ("covalent", "Covalent compounds are made of separate molecules. The bonds inside are strong, "
                 "but the forces between molecules are weak. Little heat pulls them apart.",
                 "COVALENT compounds: separate molecules, held together only by WEAK forces → melt easily.", 6.4),
    ("math",    "Ionic, strong attraction, high melting point. Covalent, weak forces between molecules, low melting point.",
                "Ionic: strong attraction → HIGH m.p.  Covalent: weak forces → LOW m.p.", 5.2),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧂 WHY? — Why do ionic compounds melt so high but covalent ones don't?

Salt (NaCl) melts at 801 °C 🔥 · Wax melts at ~60 °C 🕯️

Ionic: a giant lattice of Na⁺ and Cl⁻ ➕➖
Every ion is pulled by opposite charges all around it → very strong forces 💪
Melting means breaking the whole network → lots of energy

Covalent: separate molecules held by WEAK forces between them → melt easily

Metals and Non-metals + Carbon Compounds — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #IonicCompounds #CovalentCompounds #Class10Science #Chemistry #CBSE #BoardExams"""

NA, CL = PURPLE, GREEN
END_Y = 0.398


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    cov = ease(c.phase("covalent", 0.0, 0.25))
    ha = ease(c.phase("hook", 0.05, 0.3)) * (1 - ease(c.phase("lattice", 0.0, 0.25)))
    if ha > 0.01:
        for x, name, t, col in ((-1.6, "salt", "801 °C", PINK), (1.6, "wax", "~60 °C", CYAN)):
            dax.add_patch(FancyBboxPatch((x - 1.3, -1.0), 2.6, 2.4, boxstyle="round,pad=0,rounding_size=0.2",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=ha, zorder=5))
            dax.text(x, 0.75, name, ha="center", fontsize=26, color=LTGREY, fontweight="bold", alpha=ha, zorder=6)
            dax.text(x, -0.15, t, ha="center", va="center", fontsize=38, color=col, fontweight="bold", alpha=ha, zorder=6)
    la = ease(c.phase("lattice", 0.05, 0.4)) * (1 - cov)
    if la > 0.01:
        sp = 0.72
        heat = ease(c.phase("heat", 0.2, 0.9))
        for i in range(-3, 4):
            for j in range(-3, 4):
                x, y = i * sp, j * sp * 0.95
                na = (i + j) % 2 == 0
                a = la * ease(c.phase("lattice", 0.05 + 0.02 * (i + j + 6), 0.25 + 0.02 * (i + j + 6)))
                jig = 0.05 * heat * np.sin(c.t * 25 + i * 3 + j * 7)
                col = NA if na else CL
                dax.add_patch(Circle((x + jig, y - jig), 0.22 if na else 0.3, facecolor=col, edgecolor=NAVY, lw=2,
                                     alpha=a, zorder=5))
                dax.text(x + jig, y - jig, "+" if na else "−", ha="center", va="center", fontsize=16, color=NAVY,
                         fontweight="bold", alpha=a, zorder=6)
        pa = ease(c.phase("pull", 0.1, 0.4))
        if pa > 0:
            cx, cy = 0, 0
            dax.add_patch(Circle((cx, cy), 0.42, fill=False, edgecolor=GOLD, lw=4, alpha=pa * la, zorder=7))
            for ang in np.arange(0, 2 * np.pi, np.pi / 2):
                dax.annotate("", xy=(0.3 * np.cos(ang), 0.3 * np.sin(ang)),
                             xytext=(sp * 0.95 * np.cos(ang), sp * 0.95 * np.sin(ang) * 0.95),
                             arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=3, alpha=pa * la), zorder=8)
            outline(dax.text(0, 2.45, "pulled from ALL sides", ha="center", fontsize=23, color=GOLD, fontweight="bold",
                             alpha=pa * la, zorder=8))
        hh = ease(c.phase("heat", 0.1, 0.4)) * la
        if hh > 0:
            outline(dax.text(0, -2.5, "needs ~801 °C to break", ha="center", fontsize=23, color=PINK,
                             fontweight="bold", alpha=hh, zorder=8))
    if cov > 0.01:
        sep = ease(c.phase("covalent", 0.5, 1.0))
        rng = np.random.default_rng(3)
        base = [(-2.2, 1.3), (-0.6, 1.6), (1.1, 1.2), (2.0, 1.75), (-1.6, -0.1), (0.3, 0.1), (1.9, -0.25),
                (-2.5, -1.5), (-0.7, -1.6), (1.2, -1.5)]
        for k, (x, y) in enumerate(base):
            dx, dy = rng.normal(0, 0.25, 2) * sep + 0.06 * np.sin(c.t * 5 + k)
            ang = rng.uniform(0, np.pi)
            p = (x + dx - 0.25 * np.cos(ang), y + dy - 0.25 * np.sin(ang))
            q = (x + dx + 0.25 * np.cos(ang), y + dy + 0.25 * np.sin(ang))
            dax.plot([p[0], q[0]], [p[1], q[1]], color=WHITE, lw=6, alpha=cov, zorder=5)
            dax.add_patch(Circle(p, 0.22, facecolor=CYAN, edgecolor=NAVY, lw=2, alpha=cov, zorder=6))
            dax.add_patch(Circle(q, 0.22, facecolor=CYAN, edgecolor=NAVY, lw=2, alpha=cov, zorder=6))
        outline(dax.text(0, 2.45, "strong bonds INSIDE molecules", ha="center", fontsize=22, color=CYAN,
                         fontweight="bold", alpha=cov, zorder=8))
        outline(dax.text(0, -2.3, "weak forces BETWEEN them → melt easily", ha="center", fontsize=22, color=GREEN,
                         fontweight="bold", alpha=ease(c.phase("covalent", 0.4, 0.7)), zorder=8))
    c.steps([("ionic: strong attraction → HIGH m.p.", 0.0, WHITE),
             ("covalent: weak forces → LOW m.p.", 0.3, GOLD)], ys=(0.345, 0.285))
