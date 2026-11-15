"""WHY? — Why does a charge moving parallel to a magnetic field feel no force?  (Class 12 Moving Charges & Magnetism)"""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why NO force on a charge moving ALONG B?"
TAGS = "Class 12 Physics"
BEATS = [
    ("hook",    "A moving charge in a magnetic field usually gets pushed sideways. But move it along the field, and nothing happens! Why?",
                "A moving charge in a magnetic field gets pushed… but ALONG the field: NOTHING! Why?", 5.6),
    ("perp",    "Fire a proton straight across the field lines. It feels the biggest force, and curves into a circle.",
                "Fire it ACROSS the field (θ = 90°): maximum force → it curves into a circle.", 5.0),
    ("formula", "The force is q v B sine theta, where theta is the angle between the velocity and the field.",
                "Magnetic force: F = q v B sin θ  (θ = angle between v and B)", 4.6),
    ("para",    "Now fire it along the field lines. Theta is zero, and sine zero is zero. No force at all. It goes straight.",
                "ALONG the field: θ = 0°, sin 0° = 0 → F = 0 → it goes STRAIGHT.", 5.4),
    ("idea",    "A magnetic field only pushes on the part of the motion that cuts across it. Moving along it, you cut no field lines.",
                "B only pushes the part of motion that CUTS ACROSS it. Moving along → cuts nothing.", 5.4),
    ("helix",   "At an in between angle, the across part makes a circle, the along part carries on. A helix!",
                "In between? Across part → circle, along part → straight… together a HELIX!", 4.8),
    ("math",    "F equals q v B sine theta. Theta zero, no force. Theta ninety, maximum force.",
                "F = qvB sin θ:  θ = 0° → F = 0,  θ = 90° → F max", 4.4),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧲 WHY? — Why does a charge moving PARALLEL to a magnetic field feel NO force?

F = q v B sin θ   (θ = angle between velocity and field)

➡️ Across the field (θ = 90°): maximum force → circular path ⭕
➡️ Along the field (θ = 0°): sin 0 = 0 → NO force → straight line
➡️ In between: circle + straight motion = HELIX 🌀

A magnetic field only pushes the part of motion that cuts across it.

Moving Charges and Magnetism — Class 12 Physics. 📗

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #LorentzForce #MovingCharges #Class12Physics #Magnetism #JEE #CBSE"""


def field(dax, a):
    for y in np.linspace(-2.0, 2.0, 6):
        dax.plot([-3.3, 3.3], [y, y], color=CYAN, lw=2, alpha=a * 0.45, zorder=2)
        dax.add_patch(FancyArrowPatch((2.6, y), (2.95, y), arrowstyle="-|>", mutation_scale=22, color=CYAN, lw=2,
                                      alpha=a * 0.6, zorder=2))
    outline(dax.text(3.25, 2.35, "B →", ha="right", fontsize=24, color=CYAN, fontweight="bold", alpha=a, zorder=6))


def proton(dax, x, y, a, col=PINK):
    dax.add_patch(Circle((x, y), 0.2, facecolor=col, edgecolor=WHITE, lw=2, alpha=a, zorder=8))
    dax.text(x, y, "+", ha="center", va="center", fontsize=18, color=NAVY, fontweight="bold", alpha=a, zorder=9)


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    a0 = ease(c.phase("hook", 0.05, 0.35))
    pe = ease(c.phase("perp", 0.0, 0.2)) * (1 - ease(c.phase("formula", 0.0, 0.2)))
    field(dax, a0 * (1 - ease(c.phase("math", 0.0, 0.3))) * (1 - pe))
    if pe > 0.01:          # for the perpendicular case, show B pointing INTO the page (⊗ grid)
        for gx in np.linspace(-3.0, 3.0, 7):
            for gy in np.linspace(-1.9, 2.1, 5):
                dax.text(gx, gy, "×", ha="center", va="center", fontsize=28, color=CYAN, alpha=pe * 0.8, zorder=2)
        outline(dax.text(3.25, 2.35, "B into page", ha="right", fontsize=20, color=CYAN, fontweight="bold",
                         alpha=pe, zorder=6))
    fo = ease(c.phase("formula", 0.05, 0.35)) * (1 - ease(c.phase("para", 0.0, 0.2)))
    pa = ease(c.phase("para", 0.0, 0.2)) * (1 - ease(c.phase("helix", 0.0, 0.2)))
    he = ease(c.phase("helix", 0.0, 0.25)) * (1 - ease(c.phase("math", 0.0, 0.3)))
    if pe > 0.01:
        # perpendicular: B is drawn in-plane, so show the circle the proton makes (force ⟂ both)
        f = c.phase("perp", 0.15, 1.0)
        th = np.linspace(0, 2 * np.pi * f, 100)
        R = 1.25
        xs, ys = R * np.sin(th), 0.2 - R + R * np.cos(th) + R - 0.0
        xs, ys = R * np.sin(th), 0.2 + R * np.cos(th) - 0
        dax.plot(xs, ys - 0.0, color=PINK, lw=3, alpha=pe, zorder=6)
        proton(dax, xs[-1], ys[-1], pe)
        outline(dax.text(0, -1.6, "v across B → circle", ha="center", fontsize=21, color=PINK,
                         fontweight="bold", alpha=pe, zorder=8))
        outline(dax.text(0, 0.2, "F max", ha="center", va="center", fontsize=26, color=GOLD, fontweight="bold",
                         alpha=pe * ease(c.phase("perp", 0.4, 0.6)), zorder=8))
    if fo > 0.01:
        outline(dax.text(0, 0.6, r"$F = q\,v\,B\,\sin\theta$", ha="center", va="center", fontsize=52, color=GOLD,
                         alpha=fo, zorder=8))
        outline(dax.text(0, -0.7, "θ = angle between v and B", ha="center", fontsize=23, color=LTGREY,
                         fontweight="bold", alpha=fo, zorder=8))
    if pa > 0.01:
        f = ease(c.phase("para", 0.1, 0.9))
        x = lerp(-2.8, 2.6, f)
        dax.plot([-2.8, x], [0.35, 0.35], color=GREEN, lw=3, alpha=pa, zorder=6, ls=(0, (4, 3)))
        proton(dax, x, 0.35, pa, GREEN)
        dax.add_patch(FancyArrowPatch((x + 0.25, 0.35), (x + 0.9, 0.35), arrowstyle="-|>", mutation_scale=26,
                                      color=GREEN, lw=4, alpha=pa, zorder=7))
        outline(dax.text(0, 1.25, "θ = 0°  →  sin 0° = 0", ha="center", fontsize=26, color=WHITE, fontweight="bold",
                         alpha=pa, zorder=8))
        outline(dax.text(0, -0.65, "F = 0 → straight line", ha="center", fontsize=28, color=GREEN, fontweight="bold",
                         alpha=pa * ease(c.phase("para", 0.4, 0.7)), zorder=8))
        ia = ease(c.phase("idea", 0.1, 0.4))
        if ia > 0:
            outline(dax.text(0, -1.5, "cuts NO field lines", ha="center", fontsize=24, color=CYAN, fontweight="bold",
                             alpha=ia * pa, zorder=8))
    if he > 0.01:
        f = ease(c.phase("helix", 0.1, 0.95))
        tt = np.linspace(0, 8 * np.pi * f, 300)
        xs = -2.9 + 5.4 * tt / (8 * np.pi)
        ys = 0.3 + 0.75 * np.sin(tt)
        zs = np.cos(tt)
        front = zs > 0
        dax.plot(xs, ys, color=PURPLE, lw=2, alpha=he * 0.35, zorder=5)
        dax.plot(np.where(front, xs, np.nan), np.where(front, ys, np.nan), color=PURPLE, lw=4, alpha=he, zorder=6)
        if len(xs):
            proton(dax, xs[-1], ys[-1], he, PURPLE)
        outline(dax.text(0, -1.5, "across → circle  +  along → straight", ha="center", fontsize=21, color=WHITE,
                         fontweight="bold", alpha=he, zorder=8))
        outline(dax.text(0, 1.7, "HELIX", ha="center", fontsize=32, color=PURPLE, fontweight="bold", alpha=he, zorder=8))
    ma = ease(c.phase("math", 0.0, 0.35))
    if ma > 0.01:
        outline(dax.text(0, 1.1, r"$F = qvB\sin\theta$", ha="center", va="center", fontsize=50, color=GOLD,
                         alpha=ma, zorder=8))
        outline(dax.text(-1.5, -0.6, "θ = 0°\nF = 0", ha="center", va="center", fontsize=28, color=GREEN,
                         fontweight="bold", alpha=ma, zorder=8))
        outline(dax.text(1.5, -0.6, "θ = 90°\nF max", ha="center", va="center", fontsize=28, color=PINK,
                         fontweight="bold", alpha=ma, zorder=8))
    c.steps([("$F = qvB\\sin\\theta$", 0.0, WHITE),
             ("along B (θ = 0°) → no force", 0.3, GOLD)], ys=(0.345, 0.285))
