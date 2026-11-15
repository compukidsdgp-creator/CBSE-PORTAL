"""WHY? — Why do we use the right-hand thumb rule?  (Class 10 Magnetic Effects of Current)"""
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why use the RIGHT-HAND THUMB rule?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",   "A current carrying wire makes a magnetic field. But which way does it point? Here's why one simple hand rule beats memorising.",
               "A current makes a magnetic field… but WHICH WAY? Why one hand rule beats memorising.", 5.6),
    ("circles", "Sprinkle iron filings around the wire. The field forms closed circles around it.",
                "Iron filings show it: the field makes closed CIRCLES around the wire.", 4.4),
    ("flip",   "Reverse the current, and the circles reverse direction. So the field direction depends on the current.",
               "REVERSE the current → the circles REVERSE. Direction depends on the current.", 4.8),
    ("many",   "Wires point up, down, left, right, into the page. Memorising every case is impossible.",
               "Wires point up, down, left, right, into the page… memorising every case? Impossible.", 4.8),
    ("rule",   "So hold the wire in your right hand. Thumb along the current. Your curled fingers show the field direction. Works every time.",
               "Grip the wire in your RIGHT hand: THUMB = current, curled FINGERS = field. Works every time!", 6.0),
    ("math",   "One rule, every wire. Thumb, current. Fingers, field.",
               "One rule, every wire: thumb → current, fingers → field.", 3.8),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """👍 WHY? — Why use the RIGHT-HAND THUMB RULE?

A current-carrying wire makes a magnetic field in closed CIRCLES around it 🔄
Reverse the current → the circles reverse.

Wires can point in any direction — memorising every case is impossible 😵

✋ Grip the wire with your right hand:
👍 Thumb → direction of current
🤏 Curled fingers → direction of the magnetic field

One rule, every wire!

Magnetic Effects of Electric Current — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #RightHandThumbRule #Magnetism #Class10Science #CBSE #BoardExams"""


def loops(dax, cx, cy, up, a, t, n=3):
    """Field circles around a vertical wire, drawn as ellipses (perspective). up=True: current upward → anticlockwise from top."""
    for k, r in enumerate(np.linspace(0.6, 1.5, n)):
        dax.add_patch(Ellipse((cx, cy), 2 * r, 0.7 * r, fill=False, edgecolor=CYAN, lw=3, alpha=a * (1 - 0.2 * k), zorder=4))
        # moving arrow marker on the front edge
        ph = (t * 0.6 + k * 0.3) % 1.0
        ang = (-np.pi / 2 + (2 * np.pi * ph) * (1 if up else -1))
        x, y = cx + r * np.cos(ang), cy + 0.35 * r * np.sin(ang)
        d = 0.08 * (1 if up else -1)
        x2, y2 = cx + r * np.cos(ang + d / r * 3), cy + 0.35 * r * np.sin(ang + d / r * 3)
        dax.add_patch(FancyArrowPatch((x, y), (x2, y2), arrowstyle="-|>", mutation_scale=26, color=CYAN, lw=3,
                                      alpha=a, zorder=6))


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    t = c.t
    a0 = ease(c.phase("hook", 0.05, 0.35))
    ma_ = ease(c.phase("many", 0.0, 0.25))
    ru = ease(c.phase("rule", 0.0, 0.25))
    w = a0 * (1 - ma_) + ru * (1 - ease(c.phase("math", 0.0, 0.3)))
    up = not (c.at("flip") and not c.at("many")) or c.at("rule")
    if w > 0.01:
        # vertical wire
        dax.add_patch(Rectangle((-0.06, -2.2), 0.12, 4.4, color=GOLD, alpha=w, zorder=5))
        dax.add_patch(FancyArrowPatch((0.45, -0.9 if up else 0.9), (0.45, 0.9 if up else -0.9), arrowstyle="-|>",
                                      mutation_scale=30, color=GOLD, lw=4, alpha=w, zorder=6))
        outline(dax.text(0.7, 0.0, "I", ha="left", va="center", fontsize=30, color=GOLD, fontweight="bold", alpha=w,
                         zorder=7))
        ca = ease(c.phase("circles", 0.05, 0.4)) * (1 - ma_) + ru
        if ca > 0.01:
            loops(dax, 0, 0.2, up, min(1, ca) * w, t)
            # iron filings
            if c.at("circles") and not c.at("rule"):
                rng = np.random.default_rng(2)
                for k in range(70):
                    r = rng.uniform(0.5, 1.9); ang = rng.uniform(0, 2 * np.pi)
                    x, y = r * np.cos(ang), 0.2 + 0.35 * r * np.sin(ang)
                    da = 0.07
                    dax.plot([x - da * np.sin(ang), x + da * np.sin(ang)], [y + 0.35 * da * np.cos(ang), y - 0.35 * da * np.cos(ang)],
                             color=LTGREY, lw=2, alpha=ca * w * 0.6 * (1 - ru), zorder=3)
        if c.at("flip") and not c.at("many"):
            outline(dax.text(0, 2.35, "current reversed → field reversed", ha="center", fontsize=21, color=PINK,
                             fontweight="bold", alpha=ease(c.phase("flip", 0.2, 0.5)), zorder=8))
    if ma_ > 0.01:
        m = ma_ * (1 - ru)
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (0.7, 0.7), (-0.7, 0.7)]
        for k, (dx, dy) in enumerate(dirs):
            cx, cy = -2.0 + 2.0 * (k % 3), 1.2 - 2.0 * (k // 3)
            a = m * ease(c.phase("many", 0.05 + 0.1 * k, 0.2 + 0.1 * k))
            dax.add_patch(FancyArrowPatch((cx - 0.6 * dx, cy - 0.6 * dy), (cx + 0.6 * dx, cy + 0.6 * dy), arrowstyle="-|>",
                                          mutation_scale=26, color=GOLD, lw=5, alpha=a, zorder=5))
            outline(dax.text(cx + 0.55, cy - 0.55, "?", ha="center", va="center", fontsize=28, color=PINK,
                             fontweight="bold", alpha=a, zorder=6))
    if ru > 0.01:
        r = ru * (1 - ease(c.phase("math", 0.0, 0.3)))
        # stylised right hand gripping the wire: fist + thumb up
        fist_y = -0.2
        dax.add_patch(FancyBboxPatch((-0.75, fist_y - 0.55), 1.5, 1.1, boxstyle="round,pad=0,rounding_size=0.35",
                                     facecolor="#f2c9a0", edgecolor="#c48a5a", lw=3, alpha=r, zorder=7))
        for k in range(4):
            dax.plot([-0.65, 0.65], [fist_y - 0.4 + 0.27 * k, fist_y - 0.4 + 0.27 * k], color="#c48a5a", lw=2,
                     alpha=r, zorder=8)
        dax.add_patch(FancyBboxPatch((0.3, fist_y + 0.35), 0.32, 0.95, boxstyle="round,pad=0,rounding_size=0.15",
                                     facecolor="#f2c9a0", edgecolor="#c48a5a", lw=3, alpha=r, zorder=7))
        outline(dax.text(-2.2, 1.6, "THUMB = current", ha="center", fontsize=23, color=GOLD, fontweight="bold",
                         alpha=r * ease(c.phase("rule", 0.25, 0.5)), zorder=9))
        outline(dax.text(-2.2, -1.6, "FINGERS = field", ha="center", fontsize=23, color=CYAN, fontweight="bold",
                         alpha=r * ease(c.phase("rule", 0.5, 0.75)), zorder=9))
        outline(dax.text(2.3, -1.9, "RIGHT hand", ha="center", fontsize=22, color=WHITE, fontweight="bold",
                         alpha=r, zorder=9))
    mm = ease(c.phase("math", 0.0, 0.35))
    if mm > 0.01:
        outline(dax.text(0, 0.8, "thumb → current", ha="center", fontsize=40, color=GOLD, fontweight="bold", alpha=mm, zorder=8))
        outline(dax.text(0, -0.4, "fingers → field", ha="center", fontsize=40, color=CYAN, fontweight="bold",
                         alpha=ease(c.phase("math", 0.25, 0.55)), zorder=8))
    c.steps([("field = circles around the wire", 0.0, WHITE),
             ("right hand: thumb I, fingers B", 0.3, GOLD)], ys=(0.345, 0.285))
