"""WHY? — Why does a convex lens FOCUS light?  (Class 10 Light · Class 12 Ray Optics)"""
import numpy as np
from matplotlib.patches import Circle, Polygon
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does a convex lens FOCUS light?"
TAGS = "Class 10 & 12 Physics"
BEATS = [
    ("hook",   "Why does a convex lens bring light together at one point? The secret is prisms.",
               "Why does a convex lens bring light to ONE point? The secret: prisms.", 4.0),
    ("prism",  "A prism bends light towards its thicker end, its base.",
               "A prism bends light towards its THICKER end — its base.", 3.8),
    ("stack",  "Now stack prisms like this. Thick in the middle, thin at the edges.",
               "Stack prisms like this: thick in the middle, thin at the edges.", 4.0),
    ("rays",   "Parallel rays come in. The top prism bends its ray down, the bottom one bends its ray up, "
               "and the middle ray goes straight through.",
               "Top prism bends its ray DOWN, bottom prism bends UP, the middle ray goes straight.", 6.2),
    ("focus",  "They all meet at a single point. The focus.",
               "They all meet at a single point — the FOCUS.", 3.4),
    ("smooth", "Make the prisms smoother and smoother, and you get a convex lens. "
               "Every ray bends just enough to reach the focus.",
               "Smooth the prisms → a convex lens. Every ray bends just enough to reach the focus.", 5.8),
    ("math",   "The distance from the lens to the focus is the focal length, f. And the power of a lens is one by f.",
               "Lens → focus distance = focal length f. Power P = 1/f (dioptre, f in metres).", 5.4),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🔍 WHY? — Why does a convex lens FOCUS light?

A prism bends light towards its thicker end 🔺
Stack prisms: thick in the middle, thin at the edges →
top ray bends DOWN, bottom ray bends UP, middle goes straight → they all meet at the FOCUS ✨
Smooth the prisms → a convex lens! Power P = 1/f

Class 10 Light & Class 12 Ray Optics — the picture that makes it click. 🧠

💾 Save it · 📤 Share with your physics group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Physics #ConvexLens #RayOptics #Class10Science #Class12Physics #CBSE"""

F = 3.0
X0 = -4.3
HW = 0.42                 # prism half-width


def prism(top):
    """Triangle with its base towards the axis (top=True: apex up)."""
    if top:
        return np.array([[0, 1.75], [-HW, 0.75], [HW, 0.75]])
    return np.array([[0, -1.75], [-HW, -0.75], [HW, -0.75]])


def lens_shape(h=1.9, bulge=0.55):
    t = np.linspace(-1, 1, 60)
    y = h * t
    x = bulge * (1 - t ** 2)
    return np.vstack([np.c_[x, y], np.c_[-x[::-1], y[::-1]]])


def ray(dax, h, p, col, lw=3.5, alpha=1.0, beyond=1.4):
    """Horizontal ray at height h, bent at x=0 towards the focus; p = drawn fraction 0..1."""
    if p <= 0:
        return
    pts = np.array([[X0, h], [0, h], [F, 0], [F + beyond, -h * beyond / F]])
    seg = np.cumsum([0] + [np.hypot(*(pts[k + 1] - pts[k])) for k in range(3)])
    L = seg[-1] * p
    out = [pts[0]]
    for k in range(3):
        if L >= seg[k + 1]:
            out.append(pts[k + 1])
        else:
            f = (L - seg[k]) / (seg[k + 1] - seg[k])
            out.append(pts[k] + (pts[k + 1] - pts[k]) * f)
            break
    out = np.array(out)
    dax.plot(out[:, 0], out[:, 1], color=col, lw=lw, alpha=alpha, zorder=6, solid_capstyle="round")


def draw(c):
    dax = c.area(-0.2, 0.0, 9.6)
    ax_a = ease(c.phase("hook", 0.2, 0.7))
    dax.plot([X0 - 0.3, 4.8], [0, 0], color=GREY, lw=1.8, ls=(0, (6, 4)), alpha=ax_a * 0.7, zorder=1)

    # 1) one prism bending one ray towards its base
    pa = ease(c.phase("prism", 0.0, 0.3)) * (1 - ease(c.phase("stack", 0.0, 0.25)))
    if pa > 0:
        tri = np.array([[0, 1.3], [-0.9, -0.9], [0.9, -0.9]])
        dax.add_patch(Polygon(tri, closed=True, facecolor=CYAN, edgecolor=WHITE, lw=2.5, alpha=0.3 * pa, zorder=3))
        rp = c.phase("prism", 0.25, 0.85)
        if rp > 0:
            pts = np.array([[-3.8, 0.6], [-0.5, 0.35], [0.5, 0.05], [3.6, -1.6]])
            n = max(2, int(len(pts) * 30 * rp))
            line = np.vstack([np.linspace(pts[k], pts[k + 1], 30) for k in range(3)])[:n]
            dax.plot(line[:, 0], line[:, 1], color=GOLD, lw=4, alpha=pa, zorder=6)
            if rp > 0.8:
                outline(dax.text(1.7, -1.75, "bends towards\nthe base", ha="center", fontsize=24, fontweight="bold",
                                 color=GOLD, alpha=pa, zorder=7))

    # 2) stacked prisms + slab
    sa = ease(c.phase("stack", 0.1, 0.6)) * (1 - ease(c.phase("smooth", 0.1, 0.6)))
    if sa > 0:
        for top in (True, False):
            dax.add_patch(Polygon(prism(top), closed=True, facecolor=CYAN, edgecolor=WHITE, lw=2.5,
                                  alpha=0.32 * sa + 0.05, zorder=3))
        dax.add_patch(Polygon([[-HW, -0.72], [HW, -0.72], [HW, 0.72], [-HW, 0.72]], closed=True, facecolor=CYAN,
                              edgecolor=WHITE, lw=2.5, alpha=0.32 * sa + 0.05, zorder=3))

    # 3) three rays through the prisms
    if c.at("rays") and not c.at("smooth"):
        for k, h in enumerate([1.25, 0.0, -1.25]):
            ray(dax, h, ease(c.phase("rays", 0.08 + k * 0.25, 0.4 + k * 0.25)), GOLD)
        for h, s, y in [(1.25, "bends down ↓", 2.05), (-1.25, "bends up ↑", -2.05)]:
            a = ease(c.phase("rays", 0.3 if h > 0 else 0.8, 0.45 if h > 0 else 0.95))
            if a > 0:
                outline(dax.text(1.6, y, s, ha="center", fontsize=24, fontweight="bold", color=GOLD, alpha=a, zorder=8))

    # 4) focus
    fa = back_out(c.phase("focus", 0.1, 0.4))
    if fa > 0:
        for r, al in [(0.35, 0.18), (0.2, 0.35)]:
            dax.add_patch(Circle((F, 0), r * min(1, fa), color=GOLD, alpha=al, zorder=7))
        dax.add_patch(Circle((F, 0), 0.08, color=WHITE, zorder=8))
        outline(dax.text(F, -0.5, "F  (focus)", ha="center", fontsize=26, fontweight="bold", color=GOLD,
                         alpha=min(1, fa), zorder=9))

    # 5) smooth lens with many rays
    la = ease(c.phase("smooth", 0.1, 0.6))
    if la > 0:
        dax.add_patch(Polygon(lens_shape(), closed=True, facecolor=CYAN, edgecolor=WHITE, lw=3, alpha=0.32 * la + 0.03,
                              zorder=3))
        for k, h in enumerate(np.linspace(-1.55, 1.55, 7)):
            ray(dax, h, ease(c.phase("smooth", 0.3 + k * 0.05, 0.65 + k * 0.05)),
                [CYAN, GREEN, GOLD, WHITE, GOLD, GREEN, CYAN][k], lw=3, alpha=0.95)
        if c.phase("smooth", 0.6, 0.8) > 0:
            outline(dax.text(0, 2.25, "convex lens", ha="center", fontsize=28, fontweight="bold", color=CYAN,
                             alpha=ease(c.phase("smooth", 0.6, 0.8)), zorder=9))

    # 6) focal length
    ma = ease(c.phase("math", 0.0, 0.3))
    if ma > 0:
        dax.annotate("", xy=(F, -1.2), xytext=(0, -1.2), zorder=9,
                     arrowprops=dict(arrowstyle="<->", color=PINK, lw=3, alpha=ma))
        outline(dax.text(F / 2, -1.6, "focal length  f", ha="center", fontsize=26, fontweight="bold", color=PINK,
                         alpha=ma, zorder=9))
    c.steps([("Power of a lens", 0.25, WHITE), (r"P = 1 / f", 0.45, GOLD),
             ("f in metres  →  P in dioptres (D)", 0.65, CYAN)], ys=(0.360, 0.300, 0.242))
