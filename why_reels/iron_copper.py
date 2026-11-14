"""WHY? — Why does copper sulphate solution turn green when iron is dipped in it?  (Class 10 Chemical Reactions / Metals)"""
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does BLUE copper sulphate turn GREEN with iron?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",    "Drop an iron nail into blue copper sulphate solution. Wait a while, and the blue turns green! Why?",
                "Iron nail into BLUE copper sulphate… after a while it turns GREEN! Why?", 4.8),
    ("change",  "Two things happen. The solution turns pale green, and the nail gets a brown coating.",
                "Two changes: the solution turns pale GREEN, the nail gets a BROWN coating.", 4.6),
    ("why",     "Iron is more reactive than copper. It pushes copper out of the solution, and takes its place.",
                "Iron is MORE REACTIVE than copper → it pushes copper OUT and takes its place.", 5.2),
    ("result",  "The brown coating is copper metal. The green colour is iron sulphate.",
                "Brown coating = COPPER metal. Green colour = IRON SULPHATE.", 4.2),
    ("ladder",  "A more reactive metal always displaces a less reactive one. That's a displacement reaction.",
                "A MORE reactive metal displaces a LESS reactive one: DISPLACEMENT reaction.", 4.8),
    ("math",    "Iron plus copper sulphate gives iron sulphate plus copper.",
                "Fe + CuSO₄ → FeSO₄ + Cu", 3.6),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🔵➡️🟢 WHY? — Why does copper sulphate turn green when an iron nail is dipped in it?

Blue CuSO₄ solution + iron nail 🔩
✅ Solution turns pale green
✅ Nail gets a brown coating

Iron is MORE reactive than copper → it displaces copper 💪
Brown coating = copper metal · Green = iron sulphate

Fe + CuSO₄ → FeSO₄ + Cu (displacement reaction)

Chemical Reactions + Metals and Non-metals — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #DisplacementReaction #ReactivitySeries #Class10Science #Chemistry #CBSE #BoardExams"""

END_Y = 0.40
BLUE, PALE_GREEN = np.array(to_rgb("#1e7bd8")), np.array(to_rgb("#9be3a6"))
IRON, COPPER = np.array(to_rgb("#8a9099")), np.array(to_rgb("#b5651d"))


def draw(c):
    lad = ease(c.phase("ladder", 0.0, 0.3))
    main = 1 - lad
    dax = c.area(0.0, 0.0, 7.0)
    if main > 0.01:
        a0 = ease(c.phase("hook", 0.05, 0.35)) * main
        prog = ease(c.phase("hook", 0.6, 1.0)) * 0.3 + ease(c.phase("change", 0.0, 0.6)) * 0.7
        liquid = tuple(BLUE + (PALE_GREEN - BLUE) * prog)
        bx = -0.6
        # beaker
        dax.add_patch(Rectangle((bx - 1.3, -2.0), 2.6, 2.2, facecolor=liquid, edgecolor="none", alpha=0.85 * a0, zorder=3))
        dax.plot([bx - 1.35, bx - 1.35, bx + 1.35, bx + 1.35], [1.0, -2.05, -2.05, 1.0], color=LTGREY, lw=4,
                 alpha=a0, zorder=5)
        # nail dropping in
        drop = ease(c.phase("hook", 0.15, 0.45))
        ny = lerp(3.0, 0.0, drop)
        coat = ease(c.phase("change", 0.2, 0.8))
        ncol = tuple(IRON + (COPPER - IRON) * coat)
        dax.add_patch(Rectangle((bx - 0.09, ny - 1.6), 0.18, 2.3, facecolor=ncol, edgecolor="none", alpha=a0, zorder=6))
        dax.add_patch(Rectangle((bx - 0.3, ny + 0.65), 0.6, 0.14, facecolor=ncol, edgecolor="none", alpha=a0, zorder=6))
        dax.add_patch(Polygon([(bx - 0.09, ny - 1.6), (bx + 0.09, ny - 1.6), (bx, ny - 1.9)], color=ncol, alpha=a0, zorder=6))
        la = ease(c.phase("change", 0.4, 0.8)) * main
        outline(dax.text(bx + 1.6, -0.8, "pale green\nsolution", ha="left", va="center", fontsize=20, color=GREEN,
                         fontweight="bold", alpha=la, zorder=8))
        outline(dax.text(bx + 0.3, 0.75, "brown\ncoating", ha="left", va="center", fontsize=20, color="#e0914a",
                         fontweight="bold", alpha=la, zorder=8))
        # ions swapping
        wa = ease(c.phase("why", 0.1, 0.4)) * main * (1 - ease(c.phase("result", 0.0, 0.12)))
        if wa > 0:
            sw = ease(c.phase("why", 0.35, 0.9))
            for k in range(4):
                y = -0.4 - 0.4 * k
                # Cu2+ moving onto the nail, Fe2+ moving off
                xc = lerp(bx - 1.0 + 0.15 * (k % 2), bx - 0.2, sw)
                xf = lerp(bx + 0.1, bx + 0.95 - 0.15 * (k % 2), sw)
                dax.add_patch(Circle((xc, y), 0.14, color="#5ec3ff", alpha=wa, zorder=7))
                dax.text(xc, y, "Cu", ha="center", va="center", fontsize=10, color=NAVY, fontweight="bold", alpha=wa, zorder=8)
                dax.add_patch(Circle((xf, y - 0.2), 0.14, color=GREEN, alpha=wa * sw, zorder=7))
                dax.text(xf, y - 0.2, "Fe", ha="center", va="center", fontsize=10, color=NAVY, fontweight="bold",
                         alpha=wa * sw, zorder=8)
            outline(dax.text(bx + 1.6, 1.6, "Fe more reactive\nthan Cu", ha="left", va="center", fontsize=21,
                             color=GOLD, fontweight="bold", alpha=wa, zorder=8))
        ra = ease(c.phase("result", 0.15, 0.45)) * main
        if ra > 0:
            outline(dax.text(bx + 1.6, 1.6, "Cu  = brown coat\nFeSO₄ = green", ha="left", va="center", fontsize=21,
                             color=WHITE, fontweight="bold", alpha=ra, zorder=8))
    if lad > 0.01:
        metals = [("K", 0.95), ("Na", 0.9), ("Ca", 0.85), ("Mg", 0.8), ("Al", 0.75), ("Zn", 0.7), ("Fe", 0.65),
                  ("Pb", 0.6), ("Cu", 0.5), ("Ag", 0.45), ("Au", 0.4)]
        for k, (m, _) in enumerate(metals):
            y = 2.2 - 0.39 * k
            hl = m in ("Fe", "Cu")
            col = GREEN if m == "Fe" else ("#e0914a" if m == "Cu" else LTGREY)
            a = ease(c.phase("ladder", 0.05 + 0.03 * k, 0.2 + 0.03 * k))
            dax.add_patch(FancyBboxPatch((-1.0, y - 0.17), 2.0, 0.34, boxstyle="round,pad=0,rounding_size=0.08",
                                         facecolor="#13264d" if not hl else "#1f3a2e", edgecolor=col, lw=2.5 if hl else 1.5,
                                         alpha=a, zorder=5))
            dax.text(0, y, m, ha="center", va="center", fontsize=20, color=col, fontweight="bold", alpha=a, zorder=6)
        aa = ease(c.phase("ladder", 0.5, 0.8))
        outline(dax.text(1.3, 2.2, "more\nreactive ↑", ha="left", va="center", fontsize=20, color=GOLD,
                         fontweight="bold", alpha=aa, zorder=7))
        outline(dax.text(1.3, -0.15, "Fe is above Cu\n→ Fe displaces Cu", ha="left", va="center", fontsize=20,
                         color=GREEN, fontweight="bold", alpha=aa, zorder=7))
    c.steps([("$Fe + CuSO_4 \\rightarrow FeSO_4 + Cu$", 0.0, WHITE),
             ("more reactive displaces less reactive", 0.3, GOLD)], ys=(0.345, 0.285))
