"""WHY? — Why is the stomach acidic but the small intestine basic?  (Class 10 Acids, Bases & Life Processes)"""
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle, Polygon
from matplotlib.colors import LinearSegmentedColormap
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why is the stomach ACIDIC but the intestine BASIC?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",   "Your stomach is full of acid. A few centimetres later, your intestine is basic. Why switch?",
               "Your stomach is full of ACID… a little further on, the intestine is BASIC. Why switch?", 4.8),
    ("stomach", "The stomach makes hydrochloric acid. p H about two. It kills germs in food, "
                "and lets the enzyme pepsin start digesting proteins.",
                "Stomach makes HCl → pH ≈ 2. It kills germs and lets PEPSIN digest proteins.", 6.0),
    ("problem", "But the enzymes of the small intestine can't work in acid. And acid would harm its lining.",
                "But intestine enzymes CAN'T work in acid — and acid would harm its lining.", 4.8),
    ("neutral", "So bile from the liver, and juice from the pancreas, pour in. They're basic, and neutralise the acid.",
                "Bile (liver) + pancreatic juice are BASIC → they NEUTRALISE the acid.", 5.4),
    ("enzyme", "Now the p H is about eight, perfect for trypsin and lipase to finish digestion. "
               "Every enzyme has its own favourite p H.",
               "Now pH ≈ 8: perfect for TRYPSIN & LIPASE. Every enzyme has its own favourite pH.", 6.0),
    ("math",   "Stomach, acidic, for pepsin. Intestine, basic, for trypsin and lipase.",
               "Stomach: acidic (pepsin). Intestine: basic (trypsin, lipase).", 4.4),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧪 WHY? — Why is the stomach ACIDIC but the small intestine BASIC?

Stomach 🟥 makes HCl → pH ≈ 2
✅ kills germs ✅ pepsin digests proteins in acid

Small intestine 🟪: its enzymes can't work in acid, and acid harms its lining
➡️ Bile (liver) + pancreatic juice are basic → neutralise the acid → pH ≈ 8
✅ trypsin & lipase finish digestion

Every enzyme has its favourite pH! 🎯

Acids, Bases & Salts + Life Processes — Class 10 Science. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #pH #Digestion #Class10Science #AcidsBasesSalts #CBSE #BoardExams"""

END_Y = 0.398
PH_CMAP = LinearSegmentedColormap.from_list("ph", ["#e63946", "#ff9f43", "#ffd23f", "#3ddc97", "#2ad4ff", "#5b4bd8", "#a98bff"])


def ph_x(ph):
    return -3.0 + 6.0 * ph / 14


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    a0 = ease(c.phase("hook", 0.05, 0.4))
    # pH scale
    grad = np.linspace(0, 1, 256)[None, :]
    dax.imshow(grad, extent=(-3.0, 3.0, 1.85, 2.2), cmap=PH_CMAP, aspect="auto", alpha=a0, zorder=3)
    for ph in (0, 7, 14):
        dax.text(ph_x(ph), 2.32, str(ph), ha="center", fontsize=18, color=LTGREY, alpha=a0, zorder=4, fontweight="bold")
    dax.text(-3.0, 1.62, "acid", ha="left", fontsize=17, color="#ff6b6b", alpha=a0, zorder=4, fontweight="bold")
    dax.text(3.0, 1.62, "base", ha="right", fontsize=17, color=PURPLE, alpha=a0, zorder=4, fontweight="bold")
    # stomach (left) and intestine (right)
    dax.add_patch(Ellipse((-1.7, -0.3), 2.3, 1.7, angle=-25, facecolor="#5c1a24", edgecolor="#ff6b6b", lw=4,
                          alpha=a0, zorder=4))
    outline(dax.text(-1.7, -0.3, "stomach", ha="center", va="center", fontsize=22, color=WHITE, fontweight="bold",
                     alpha=a0, zorder=6))
    xs = np.linspace(0.6, 3.1, 200)
    for k, y0 in enumerate((0.4, -0.4, -1.2)):
        ys = y0 + 0.18 * np.sin(xs * 6 + k)
        dax.plot(xs, ys, color=PURPLE, lw=14, alpha=a0 * 0.8, zorder=4, solid_capstyle="round")
    outline(dax.text(1.85, -1.95, "small intestine", ha="center", fontsize=22, color=WHITE, fontweight="bold",
                     alpha=a0, zorder=6))
    dax.plot([-0.55, 0.6], [-0.65, 0.4], color="#ff6b6b", lw=10, alpha=a0 * 0.7, zorder=3)
    # acid in stomach: bubbles + HCl
    sa = ease(c.phase("stomach", 0.1, 0.4))
    if sa > 0:
        for k in range(9):
            ang = k * 0.7 + c.t * 0.8
            dax.add_patch(Circle((-1.7 + 0.75 * np.cos(ang), -0.3 + 0.45 * np.sin(ang * 1.3)), 0.07, color="#ff9f9f",
                                 alpha=sa * 0.8, zorder=5))
        outline(dax.text(-1.7, -1.45, "HCl · pH ≈ 2", ha="center", fontsize=22, color="#ff6b6b", fontweight="bold",
                         alpha=sa, zorder=7))
        pa = ease(c.phase("stomach", 0.5, 0.8))
        outline(dax.text(-1.7, 0.95, "pepsin ✓", ha="center", fontsize=21, color=GOLD, fontweight="bold",
                         alpha=pa, zorder=7))
    # pointer on the scale
    pp = ease(c.phase("stomach", 0.1, 0.4))
    if pp > 0:
        ph = 2 + 6 * ease(c.phase("neutral", 0.3, 0.9))
        x = ph_x(ph)
        dax.add_patch(Polygon([(x, 1.82), (x - 0.15, 1.55), (x + 0.15, 1.55)], color=WHITE, alpha=pp, zorder=6))
        outline(dax.text(x, 1.25, f"pH {ph:.0f}", ha="center", fontsize=21, color=WHITE, fontweight="bold",
                         alpha=pp, zorder=7))
    pr = ease(c.phase("problem", 0.1, 0.4)) * (1 - ease(c.phase("neutral", 0.3, 0.6)))
    if pr > 0:
        outline(dax.text(1.85, 1.0, "enzymes ✗ in acid", ha="center", fontsize=21, color=PINK, fontweight="bold",
                         alpha=pr, zorder=7))
    na = ease(c.phase("neutral", 0.0, 0.35))
    if na > 0:
        for (x0, y0), lab in (((0.2, -2.3), "bile"), ((-0.6, -2.3), "pancreatic\njuice")):
            pass
        dax.add_patch(FancyArrowPatch((-0.2, -1.9), (0.75, -0.75), arrowstyle="-|>", mutation_scale=30, color=CYAN,
                                      lw=4, alpha=na, zorder=6))
        outline(dax.text(-0.35, -2.2, "bile + pancreatic juice (basic)", ha="center", fontsize=19, color=CYAN,
                         fontweight="bold", alpha=na, zorder=7))
    ea = ease(c.phase("enzyme", 0.1, 0.4))
    if ea > 0:
        outline(dax.text(1.85, 1.0, "trypsin · lipase ✓", ha="center", fontsize=21, color=GREEN, fontweight="bold",
                         alpha=ea, zorder=7))
    c.steps([("stomach: acidic → pepsin", 0.0, WHITE),
             ("intestine: basic → trypsin, lipase", 0.3, GOLD)], ys=(0.345, 0.285))
