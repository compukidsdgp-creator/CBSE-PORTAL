"""WHY? — How does a computer SEE an image?  (AI · Computer Vision, Class 10 & 12)"""
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Arc
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, NAVY, WHITE, LTGREY

TITLE = "How does a computer SEE an image?"
TAGS = "AI · Computer Vision"
BEATS = [
    ("hook",    "How does a computer see a picture? It doesn't see a smiley. It sees numbers.",
                "How does a computer see a picture? It doesn't see a smiley. It sees numbers.", 4.0),
    ("pixels",  "Zoom into any image, and it breaks into tiny squares called pixels.",
                "Zoom into any image and it breaks into tiny squares called pixels.", 3.6),
    ("numbers", "Each pixel is just a number. Zero is black, and two fifty five is white.",
                "Each pixel is just a number: 0 is black, 255 is white.", 4.2),
    ("rgb",     "A colour pixel stores three numbers. Red, green and blue.",
                "A colour pixel stores three numbers: Red, Green and Blue.", 3.8),
    ("filter",  "To find shapes, the computer slides a small filter across the numbers.",
                "To find shapes, the computer slides a small filter across the numbers.", 4.6),
    ("edges",   "Wherever the numbers jump sharply, it marks an edge.",
                "Wherever the numbers jump sharply, it marks an edge.", 3.4),
    ("layers",  "Layer after layer, edges become shapes, and shapes become a face. That's computer vision.",
                "Layer by layer: edges → shapes → a face. That's computer vision!", 5.6),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🤖 WHY? — How does a computer SEE an image?

A computer never sees a face… it sees a grid of numbers! 🔢
Pixels → numbers (0 = black, 255 = white) → filters find edges → layers find shapes → "FACE ✅"

That's the idea behind Computer Vision in your AI syllabus (Class 10 & 12). 🧠

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ArtificialIntelligence #ComputerVision #AIClass10 #AIClass12 #CBSE #LearnAI"""

N = 12                       # pixels per side
CELL = 0.5
HALF = N * CELL / 2
BOX = [0.0, 0.375, 1.0, 0.47]


def _hires(n=240):
    """A yellow smiley (RGB 0..1) on navy."""
    y, x = np.mgrid[0:n, 0:n] / (n - 1) * 2 - 1
    img = np.zeros((n, n, 3)); img[:] = (0.06, 0.10, 0.25)
    face = x ** 2 + y ** 2 < 0.80 ** 2
    img[face] = (1.0, 0.82, 0.10)
    for ex in (-0.32, 0.32):
        img[(x - ex) ** 2 + (y + 0.25) ** 2 < 0.13 ** 2] = (0.18, 0.10, 0.02)
    r = np.sqrt(x ** 2 + (y + 0.02) ** 2)
    mouth = (np.abs(r - 0.47) < 0.08) & (y > 0.12)
    img[mouth & face] = (0.18, 0.10, 0.02)
    return img


HI = _hires()
LO = HI.reshape(N, 240 // N, N, 240 // N, 3).mean(axis=(1, 3))          # 12x12 colour pixels
GRAY = (LO @ np.array([0.299, 0.587, 0.114]))                            # 0..1
VAL = np.round(GRAY * 255).astype(int)
gx = np.zeros_like(GRAY); gy = np.zeros_like(GRAY)
gx[:, 1:-1] = GRAY[:, 2:] - GRAY[:, :-2]
gy[1:-1, :] = GRAY[2:, :] - GRAY[:-2, :]
EDGE = np.hypot(gx, gy) > 0.35


def cell_xy(i, j):
    """Centre of pixel row i, column j (row 0 at the top)."""
    return -HALF + (j + 0.5) * CELL, HALF - (i + 0.5) * CELL


def draw(c):
    zoom = ease(c.phase("pixels", 0.0, 0.7))
    out = ease(c.phase("layers", 0.0, 0.25))
    dax = c.area(0.0, 0.0, lerp(7.9, 7.2, zoom) + 2.6 * out, box=BOX)
    ext = (-HALF, HALF, -HALF, HALF)

    if not c.at("layers") or out < 1:
        a_main = 1 - out
        # 1) smooth picture → pixels
        pix = c.phase("pixels", 0.15, 0.75)
        if pix < 1:
            dax.imshow(HI, extent=ext, zorder=2, alpha=a_main * (1 - pix), interpolation="bilinear")
        gray_mix = ease(c.phase("numbers", 0.0, 0.4)) * (1 - ease(c.phase("rgb", 0.0, 0.35)))
        if c.at("filter"):
            gray_mix = 1.0
        rgb_lo = LO * (1 - gray_mix) + np.repeat(GRAY[:, :, None], 3, axis=2) * gray_mix
        if c.at("filter"):
            rgb_lo = rgb_lo * (1 - 0.55 * ease(c.phase("filter", 0, 0.2)))
        if pix > 0:
            dax.imshow(rgb_lo, extent=ext, zorder=3, alpha=a_main * pix, interpolation="nearest")
            for k in range(N + 1):
                v = -HALF + k * CELL
                dax.plot([v, v], [-HALF, HALF], color=NAVY, lw=1.6, alpha=0.9 * pix * a_main, zorder=4)
                dax.plot([-HALF, HALF], [v, v], color=NAVY, lw=1.6, alpha=0.9 * pix * a_main, zorder=4)
        # 2) numbers in the cells
        na = ease(c.phase("numbers", 0.25, 0.6)) * (1 - 0.65 * ease(c.phase("rgb", 0.0, 0.3)))
        if c.at("filter"):
            na = 0.55
        na *= a_main
        if na > 0.02:
            for i in range(N):
                for j in range(N):
                    x, y = cell_xy(i, j)
                    dark = GRAY[i, j] * (1 - 0.55 * c.at("filter")) > 0.5
                    dax.text(x, y, str(VAL[i, j]), ha="center", va="center", fontsize=14,
                             fontweight="bold", color=NAVY if dark else WHITE, alpha=na, zorder=6)
        lp = c.phase("numbers", 0.55, 0.9) * (1 - c.phase("rgb", 0.0, 0.2))
        if lp > 0:
            for k, (txt, col, y) in enumerate([("0 = black", "#cfd8e8", -HALF - 0.45), ("255 = white", WHITE, -HALF - 0.95)]):
                outline(dax.text(0, y, txt, ha="center", fontsize=30, fontweight="bold", color=col, alpha=lp, zorder=8))
        # 3) one pixel splits into R, G, B
        rp = c.phase("rgb", 0.15, 0.55) * (1 - c.phase("filter", 0.0, 0.2))
        if rp > 0:
            i, j = 3, 5
            px, py = cell_xy(i, j)
            dax.add_patch(Rectangle((px - CELL / 2, py - CELL / 2), CELL, CELL, fill=False,
                                    edgecolor=GOLD, lw=4, zorder=9, alpha=rp))
            r, g, b = (np.round(LO[i, j] * 255)).astype(int)
            for k, (lab, v, col) in enumerate([("R", r, "#ff5a5a"), ("G", g, "#4ade80"), ("B", b, "#60a5fa")]):
                bx = lerp(px, -2.05 + k * 2.05, ease(rp))
                by = lerp(py, -HALF - 0.75, ease(rp))
                dax.add_patch(FancyBboxPatch((bx - 0.85, by - 0.36), 1.70, 0.72,
                                             boxstyle="round,pad=0.02,rounding_size=0.12", clip_on=False,
                                             facecolor=col, edgecolor=WHITE, lw=2, alpha=rp, zorder=10 + k))
                dax.text(bx, by, f"{lab} = {v}", ha="center", va="center", fontsize=26, fontweight="bold",
                         color=NAVY, alpha=rp, zorder=11 + k)
        # 4) sliding 3x3 filter, edges light up behind it
        fp = c.phase("filter", 0.15, 1.0)
        if c.at("filter") and fp > 0:
            steps = N * N
            pos = min(steps - 1, int(fp * steps))
            si, sj = divmod(pos, N)
            seen = np.zeros((N, N), bool)
            seen.flat[:pos + 1] = True
            for (i, j) in zip(*np.where(EDGE & seen)):
                x, y = cell_xy(i, j)
                dax.add_patch(Rectangle((x - CELL / 2, y - CELL / 2), CELL, CELL, facecolor=CYAN,
                                        edgecolor="none", alpha=0.85 * a_main, zorder=5))
            if fp < 1:
                x, y = cell_xy(si, sj)
                dax.add_patch(Rectangle((x - 1.5 * CELL, y - 1.5 * CELL), 3 * CELL, 3 * CELL, fill=False,
                                        edgecolor=GOLD, lw=5, zorder=12))
                outline(dax.text(x, y + 1.05 * CELL * 2, "3×3 filter", ha="center", fontsize=22,
                                 fontweight="bold", color=GOLD, zorder=13))
        ep = ease(c.phase("edges", 0.0, 0.5))
        if ep > 0:
            # everything but the edges fades away
            dax.add_patch(Rectangle((-HALF, -HALF), 2 * HALF, 2 * HALF, facecolor=NAVY, edgecolor="none",
                                    alpha=0.85 * ep * a_main, zorder=6.5))
            for (i, j) in zip(*np.where(EDGE)):
                x, y = cell_xy(i, j)
                dax.add_patch(Rectangle((x - CELL / 2, y - CELL / 2), CELL, CELL, facecolor=CYAN,
                                        edgecolor=NAVY, lw=1, alpha=ep * a_main, zorder=7))
            outline(dax.text(0, -HALF - 0.55, "edges found!", ha="center", fontsize=32, fontweight="bold",
                             color=CYAN, alpha=ep * a_main * (1 - out), zorder=8))

    # 5) layers: edges → shapes → face
    if c.at("layers"):
        xs = [-3.2, 0.0, 3.2]
        labels = ["edges", "shapes", "FACE!"]
        for k, x in enumerate(xs):
            a = back_out(c.phase("layers", 0.18 + k * 0.2, 0.36 + k * 0.2))
            if a <= 0:
                continue
            a = min(1, a)
            dax.add_patch(FancyBboxPatch((x - 1.3, -1.3), 2.6, 2.6, boxstyle="round,pad=0,rounding_size=0.25",
                                         facecolor="#0c1a3a", edgecolor=[CYAN, PINK, GREEN][k], lw=3,
                                         alpha=a, zorder=10))
            if k == 0:
                for (i, j) in zip(*np.where(EDGE)):
                    px, py = cell_xy(i, j)
                    dax.add_patch(Rectangle((x + px * 0.36 - 0.09, py * 0.36 - 0.09), 0.18, 0.18,
                                            facecolor=CYAN, edgecolor="none", alpha=a, zorder=11))
            elif k == 1:
                dax.add_patch(Circle((x, 0), 0.95, fill=False, edgecolor=PINK, lw=4, alpha=a, zorder=11))
                for ex in (-0.32, 0.32):
                    dax.add_patch(Circle((x + ex, 0.3), 0.14, fill=False, edgecolor=PINK, lw=3.5, alpha=a, zorder=11))
                dax.add_patch(Arc((x, 0.0), 1.0, 0.9, theta1=200, theta2=340, edgecolor=PINK, lw=4,
                                  alpha=a, zorder=11))
            else:
                dax.imshow(HI, extent=(x - 1.0, x + 1.0, -1.0, 1.0), zorder=11, alpha=a)
            outline(dax.text(x, -1.75, labels[k], ha="center", fontsize=30, fontweight="bold",
                             color=[CYAN, PINK, GREEN][k], alpha=a, zorder=12))
            if k < 2:
                ar = c.phase("layers", 0.30 + k * 0.2, 0.40 + k * 0.2)
                if ar > 0:
                    dax.annotate("", xy=(x + 1.95, 0), xytext=(x + 1.35, 0), zorder=12,
                                 arrowprops=dict(arrowstyle="-|>", color=WHITE, lw=3, alpha=ar, mutation_scale=30))
        fa = back_out(c.phase("layers", 0.78, 0.95))
        if fa > 0:
            c.pill(0.5, 0.345, 0.56 * min(1, fa), 0.056, GREEN, alpha=min(1, fa), dark="#06261a")
            c.text(0.5, 0.345, "Face detected  ✓  98%", size=34, color=GREEN, alpha=min(1, fa))
