"""WHY? — Why does a current-carrying wire feel a FORCE in a magnetic field?  (Class 10 / 12 Magnetism)"""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does a wire feel a FORCE in a magnet?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",    "Put a wire carrying current between two magnets, and it jumps! Why does that happen?",
                "Put a current-carrying wire between magnets… and it JUMPS! Why?", 4.2),
    ("field",   "The magnet has its own field, running from north to south.",
                "The magnet has its own field, running from NORTH to SOUTH.", 3.6),
    ("circles", "The current makes a second field, in circles around the wire.",
                "The current makes a SECOND field — circles around the wire.", 3.8),
    ("combine", "Above the wire, the two fields point the same way and add up. Below, they oppose and cancel.",
                "ABOVE the wire the fields ADD. BELOW they CANCEL.", 5.0),
    ("push",    "Field lines act like stretched rubber bands. They push the wire from the strong side to the weak side.",
                "Field lines act like stretched rubber bands → they push the wire from STRONG to WEAK.", 5.4),
    ("fleming", "Fleming's left hand rule tells the direction. First finger, field. Second finger, current. Thumb, motion.",
                "Fleming's LEFT-HAND rule: First finger = Field, seCond = Current, thuMb = Motion.", 6.0),
    ("math",    "And the size of the force is B I L.",
                "Size of the force: F = B I L", 3.4),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧲 WHY? — Why does a current-carrying wire feel a FORCE in a magnetic field?

The magnet's field runs N → S ➡️
The current makes its own field in circles around the wire 🔄
Above the wire they ADD, below they CANCEL ➕➖
Field lines push the wire from strong → weak 💥

Direction = Fleming's Left-Hand Rule ✋
First finger → Field · seCond finger → Current · thuMb → Motion
Size: F = BIL

Magnetic Effects of Current — Class 10 · Moving Charges — Class 12. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #FlemingsLeftHandRule #Magnetism #Class10Science #Class12Physics #CBSE #BoardExams"""

LINES = [1.6, 1.0, 0.45, -0.45, -1.0, -1.6]


def arrow(dax, p, q, col, a, lw=4, z=6):
    dax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=34, color=col, lw=lw, alpha=a, zorder=z))


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    fl = ease(c.phase("fleming", 0.0, 0.25))
    main = 1 - fl
    if main > 0.01:
        ma = ease(c.phase("hook", 0.05, 0.4)) * main
        # magnets
        for x, lab, col in ((-3.1, "N", PINK), (2.6, "S", CYAN)):
            dax.add_patch(FancyBboxPatch((x, -2.0), 0.5, 4.0, boxstyle="round,pad=0,rounding_size=0.08",
                                         facecolor=col, edgecolor="none", alpha=ma * 0.85, zorder=4))
            dax.text(x + 0.25, 0, lab, ha="center", va="center", fontsize=34, fontweight="bold", color=NAVY,
                     alpha=ma, zorder=5)
        # wire, current into the page
        wa = ma
        jump = 0.35 * ease(c.phase("push", 0.35, 0.8)) + 0.12 * np.sin(c.t * 9) * ease(c.phase("hook", 0.4, 0.6)) \
            * (1 - ease(c.phase("field", 0, 0.3)))
        wy = -jump
        dax.add_patch(Circle((0, wy), 0.30, facecolor="#13264d", edgecolor=GOLD, lw=4, alpha=wa, zorder=8))
        dax.plot([-0.16, 0.16], [wy - 0.16, wy + 0.16], color=GOLD, lw=4, alpha=wa, zorder=9)
        dax.plot([-0.16, 0.16], [wy + 0.16, wy - 0.16], color=GOLD, lw=4, alpha=wa, zorder=9)
        outline(dax.text(-0.42, wy - 0.42, "current\ninto page", fontsize=17, color=GOLD, fontweight="bold", ha="right",
                         alpha=ease(c.phase("circles", 0.0, 0.3)) * main, zorder=9, va="top"))
        # magnet field lines (N → S), bending in "combine"
        fa = ease(c.phase("field", 0.1, 0.5)) * main
        cb = ease(c.phase("combine", 0.25, 0.7))
        if fa > 0:
            xs = np.linspace(-2.55, 2.55, 120)
            for y0 in LINES:
                if y0 > 0:     # crowd above the wire, bowing over it
                    y = y0 - cb * 0.22 * (y0) * np.exp(-xs ** 2 / 2.5) * 0 + cb * (0.55 - 0.18 * y0) * np.exp(-xs ** 2 / 1.2) * 0.6
                    y = y0 * (1 - 0.35 * cb * np.exp(-xs ** 2 / 2.0)) + cb * 0.55 * np.exp(-xs ** 2 / 0.9) * (1.7 - y0) / 1.7
                else:          # spread out below
                    y = y0 * (1 + 0.25 * cb * np.exp(-xs ** 2 / 2.0))
                dax.plot(xs, y, color=CYAN, lw=3, alpha=fa * 0.85, zorder=5)
                xm = 1.6
                ym = np.interp(xm, xs, y)
                arrow(dax, (xm - 0.2, ym), (xm + 0.12, ym), CYAN, fa, lw=3)
        # the wire's own circular field (clockwise for current into page)
        ca = ease(c.phase("circles", 0.15, 0.5)) * (1 - cb) * main
        if ca > 0:
            for r in (0.6, 0.95):
                th = np.linspace(0, 2 * np.pi, 90)
                dax.plot(r * np.cos(th), wy + r * np.sin(th), color=PURPLE, lw=3, alpha=ca, zorder=6)
                arrow(dax, (-0.15, wy + r), (0.12, wy + r), PURPLE, ca, lw=3)        # top → right
                arrow(dax, (0.15, wy - r), (-0.12, wy - r), PURPLE, ca, lw=3)        # bottom → left
        la = ease(c.phase("combine", 0.4, 0.75)) * main
        if la > 0:
            outline(dax.text(-1.5, 2.25, "fields ADD → strong", ha="center", fontsize=21, color=GREEN,
                             fontweight="bold", alpha=la, zorder=9))
            outline(dax.text(-1.5, -2.45, "fields CANCEL → weak", ha="center", fontsize=21, color=PINK,
                             fontweight="bold", alpha=la, zorder=9))
        pa = back_out(c.phase("push", 0.15, 0.5)) * main
        if pa > 0.01:
            arrow(dax, (0.0, wy - 0.4), (0.0, wy - 0.4 - 1.1 * min(1, pa)), GOLD, min(1, pa), lw=6, z=10)
            outline(dax.text(0.35, wy - 1.15, "F", fontsize=34, color=GOLD, fontweight="bold", alpha=min(1, pa),
                             zorder=10))
    # Fleming's left-hand rule: three perpendicular arrows
    if fl > 0.01:
        o = (-0.3, 0.2)
        a1 = ease(c.phase("fleming", 0.2, 0.4)); a2 = ease(c.phase("fleming", 0.4, 0.6))
        a3 = ease(c.phase("fleming", 0.6, 0.8))
        arrow(dax, o, (o[0] + 2.4, o[1]), CYAN, a1 * fl, lw=6)
        outline(dax.text(o[0] + 2.5, o[1] + 0.3, "First finger\nFIELD", fontsize=21, color=CYAN, fontweight="bold",
                         alpha=a1 * fl, zorder=9, ha="center", va="bottom"))
        arrow(dax, o, (o[0] - 1.5, o[1] + 1.25), GOLD, a2 * fl, lw=6)
        outline(dax.text(o[0] - 1.6, o[1] + 1.4, "seCond finger\nCURRENT (into page)", fontsize=20, color=GOLD,
                         fontweight="bold", alpha=a2 * fl, zorder=9, ha="center", va="bottom"))
        arrow(dax, o, (o[0], o[1] - 2.0), PINK, a3 * fl, lw=6)
        outline(dax.text(o[0] + 0.25, o[1] - 1.9, "thuMb\nMOTION (force)", fontsize=21, color=PINK, fontweight="bold",
                         alpha=a3 * fl, zorder=9, ha="left", va="center"))
        dax.add_patch(Circle(o, 0.12, color=WHITE, alpha=fl, zorder=10))
        outline(dax.text(0, 2.3, "LEFT hand · all three at 90°", ha="center", fontsize=22, color=WHITE,
                         fontweight="bold", alpha=a1 * fl, zorder=9))
    c.steps([("direction: Fleming's left-hand rule", 0.0, WHITE),
             ("$F = B\\,I\\,L$", 0.3, GOLD)], ys=(0.345, 0.285))
