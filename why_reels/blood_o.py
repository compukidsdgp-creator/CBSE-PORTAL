"""WHY? — Why is blood group O called the universal donor?  (Class 11/12 Biology · general science)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why is blood group O the UNIVERSAL DONOR?"
TAGS = "Biology"
BEATS = [
    ("hook",   "In an emergency, doctors can give O negative blood to almost anyone. Why is O so special?",
               "In emergencies, doctors give O-negative blood to almost ANYONE. Why is O special?", 4.8),
    ("markers", "Red blood cells carry markers called antigens. Group A has A markers, B has B, A B has both, "
                "and O has none.",
                "Red cells carry ANTIGEN markers: A has A, B has B, AB has both, O has NONE.", 6.0),
    ("guards", "Your plasma has antibodies that attack any marker you don't have.",
               "Your plasma has ANTIBODIES that attack any marker you DON'T have.", 4.0),
    ("clump",  "Give someone the wrong blood, and the antibodies grab the cells. They clump together. That's dangerous.",
               "Wrong blood → antibodies grab the cells → they CLUMP. Dangerous!", 5.0),
    ("o",      "O cells have no A or B markers. Nothing for the antibodies to attack. "
               "So O can be given to every group.",
               "O cells have NO A or B markers → nothing to attack → O can go to EVERY group.", 5.6),
    ("rh",     "There's also the Rh marker. O negative has none of them, so it's the true universal donor.",
               "There's also the Rh marker. O-NEGATIVE has none → the true universal donor.", 4.8),
    ("math",   "No markers, no attack. O negative, universal donor. A B positive, universal recipient.",
               "No markers → no attack. O− = universal DONOR · AB+ = universal RECIPIENT.", 5.0),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🩸 WHY? — Why is blood group O the universal donor?

Red blood cells carry markers (antigens):
🅰️ A → A markers · 🅱️ B → B markers · 🆎 AB → both · 🅾️ O → none

Plasma antibodies attack markers you don't have → wrong blood CLUMPS ⚠️

O cells have no A/B markers → nothing to attack → O can be given to every group ✅
With the Rh marker too: O-negative = true universal donor, AB-positive = universal recipient.

Human blood groups — Biology. 📗

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #BloodGroups #UniversalDonor #Biology #NEET #CBSE #BoardExams"""

RBC = "#d62839"
GROUPS = [("A", ["A"]), ("B", ["B"]), ("AB", ["A", "B"]), ("O", [])]


def cell(dax, x, y, r, marks, a, z=5):
    if a <= 0.01:
        return
    dax.add_patch(Circle((x, y), r, facecolor=RBC, edgecolor="#ff8fa3", lw=3, alpha=a, zorder=z))
    dax.add_patch(Circle((x, y), r * 0.45, facecolor="#a81d2e", edgecolor="none", alpha=a, zorder=z + 1))
    n = 6
    for k in range(n):
        if not marks:
            break
        m = marks[k % len(marks)]
        ang = k * 2 * np.pi / n + 0.3
        px, py = x + (r + 0.08) * np.cos(ang), y + (r + 0.08) * np.sin(ang)
        s = 0.13
        if m == "A":
            pts = [(px + s * np.cos(ang), py + s * np.sin(ang)),
                   (px + s * np.cos(ang + 2.2), py + s * np.sin(ang + 2.2)),
                   (px + s * np.cos(ang - 2.2), py + s * np.sin(ang - 2.2))]
            dax.add_patch(Polygon(pts, color=GOLD, alpha=a, zorder=z + 2))
        else:
            dax.add_patch(Rectangle((px - s * 0.75, py - s * 0.75), s * 1.5, s * 1.5, color=CYAN, alpha=a, zorder=z + 2))


def antibody(dax, x, y, ang, col, a, z=8):
    d = np.array([np.cos(ang), np.sin(ang)])
    n = np.array([-d[1], d[0]])
    base = np.array([x, y]); fork = base + d * 0.35
    dax.plot([base[0], fork[0]], [base[1], fork[1]], color=col, lw=4, alpha=a, zorder=z)
    for s in (-1, 1):
        tip = fork + d * 0.25 + n * s * 0.2
        dax.plot([fork[0], tip[0]], [fork[1], tip[1]], color=col, lw=4, alpha=a, zorder=z)


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    cl = ease(c.phase("clump", 0.0, 0.2))
    oa_ = ease(c.phase("o", 0.0, 0.2))
    ha = ease(c.phase("hook", 0.05, 0.35)) * (1 - ease(c.phase("markers", 0.0, 0.2)))
    if ha > 0.01:
        dax.add_patch(FancyBboxPatch((-0.9, -1.4), 1.8, 2.6, boxstyle="round,pad=0,rounding_size=0.25",
                                     facecolor="#3a0a12", edgecolor=RBC, lw=4, alpha=ha, zorder=5))
        dax.text(0, 0.0, "O−", ha="center", va="center", fontsize=54, color=WHITE, fontweight="bold", alpha=ha, zorder=6)
        outline(dax.text(0, 1.75, "emergency blood", ha="center", fontsize=24, color=GOLD, fontweight="bold",
                         alpha=ha, zorder=7))
    ma = ease(c.phase("markers", 0.0, 0.3)) * (1 - cl)
    if ma > 0.01:
        for k, (g, marks) in enumerate(GROUPS):
            x = -2.55 + 1.7 * k
            a = ma * ease(c.phase("markers", 0.1 + 0.18 * k, 0.3 + 0.18 * k))
            cell(dax, x, 0.5, 0.55, marks, a)
            outline(dax.text(x, -0.55, g, ha="center", fontsize=32, color=WHITE, fontweight="bold", alpha=a, zorder=8))
            outline(dax.text(x, -1.05, "none" if not marks else "+".join(marks), ha="center", fontsize=18,
                             color=LTGREY, fontweight="bold", alpha=a, zorder=8))
        ga = ease(c.phase("guards", 0.1, 0.5)) * ma
        if ga > 0:
            for k in range(7):
                antibody(dax, -2.8 + 0.95 * k, -2.0 + 0.1 * np.sin(c.t * 3 + k), np.pi / 2, PURPLE, ga)
            outline(dax.text(0, 1.75, "antibodies attack unknown markers", ha="center", fontsize=21, color=PURPLE,
                             fontweight="bold", alpha=ga, zorder=8))
    ca = cl * (1 - oa_)
    if ca > 0.01:
        g = ease(c.phase("clump", 0.2, 0.7))
        pos = [(-1.2, 0.8), (0.0, 1.1), (1.2, 0.7), (-0.6, -0.4), (0.7, -0.3), (0.0, -1.3)]
        for k, (x, y) in enumerate(pos):
            cx, cy = lerp(x * 1.6, x * 0.75, g), lerp(y * 1.4, y * 0.75, g)
            cell(dax, cx, cy, 0.42, ["A"], ca)
        for k in range(8):
            ang = k * np.pi / 4
            antibody(dax, 1.9 * np.cos(ang) * lerp(1.3, 1.0, g), 1.7 * np.sin(ang) * lerp(1.3, 1.0, g) * 0.8,
                     ang + np.pi, PURPLE, ca)
        outline(dax.text(0, 2.35, "A blood → B person: CLUMPING ⚠", ha="center", fontsize=22, color=PINK,
                         fontweight="bold", alpha=ca * ease(c.phase("clump", 0.4, 0.7)), zorder=9))
    if oa_ > 0.01:
        rh = ease(c.phase("rh", 0.0, 0.3))
        oo = oa_ * (1 - ease(c.phase("math", 0.0, 0.3)))
        cell(dax, -1.6, 0.4, 0.75, [], oo)
        outline(dax.text(-1.6, -0.75, "O" if rh < 0.5 else "O−", ha="center", fontsize=36, color=WHITE,
                         fontweight="bold", alpha=oo, zorder=8))
        for k in range(5):
            ang = k * 2 * np.pi / 5
            antibody(dax, -1.6 + 1.35 * np.cos(ang), 0.4 + 1.35 * np.sin(ang), ang + np.pi, PURPLE,
                     oo * 0.9)
        outline(dax.text(-1.6, 2.1, "nothing to attack", ha="center", fontsize=21, color=GREEN, fontweight="bold",
                         alpha=oo * ease(c.phase("o", 0.3, 0.6)), zorder=8))
        ta = ease(c.phase("o", 0.5, 0.8)) * oo
        for k, g in enumerate(("A", "B", "AB", "O")):
            y = 1.35 - 0.75 * k
            outline(dax.text(1.0, y, "→  " + g + "  ✓", ha="left", va="center", fontsize=26, color=GREEN,
                             fontweight="bold", alpha=ta, zorder=8))
        if rh > 0:
            outline(dax.text(0.3, -2.25, "no Rh marker either → O−", ha="center", fontsize=21, color=GOLD,
                             fontweight="bold", alpha=rh * oo, zorder=8))
    m = ease(c.phase("math", 0.0, 0.35))
    if m > 0.01:
        for x, s, sub, col in ((-1.6, "O−", "universal DONOR", GREEN), (1.6, "AB+", "universal RECIPIENT", CYAN)):
            dax.add_patch(FancyBboxPatch((x - 1.4, -0.9), 2.8, 2.2, boxstyle="round,pad=0,rounding_size=0.2",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=m, zorder=5))
            dax.text(x, 0.45, s, ha="center", va="center", fontsize=40, color=col, fontweight="bold", alpha=m, zorder=6)
            dax.text(x, -0.45, sub, ha="center", va="center", fontsize=17, color=LTGREY, fontweight="bold", alpha=m, zorder=6)
    c.steps([("no markers → no attack", 0.0, WHITE),
             ("O− = universal donor", 0.3, GOLD)], ys=(0.345, 0.285))
