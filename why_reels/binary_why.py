"""WHY? — Why do computers use BINARY?  (Computer Science · Number systems / Data representation)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why do computers use BINARY?"
TAGS = "Computer Science"
BEATS = [
    ("hook",     "Why do computers think in zeros and ones, and not in our ten digits?",
                 "Why do computers think in 0s and 1s — not our 10 digits?", 3.6),
    ("switch",   "A chip holds billions of tiny switches called transistors. A switch is either off, or on. Zero, or one.",
                 "A chip has billions of tiny SWITCHES (transistors): OFF or ON = 0 or 1.", 5.6),
    ("reliable", "Two states are easy to tell apart, even when the signal is noisy. With ten levels, they'd blur together.",
                 "Two levels are easy to tell apart, even with noise. Ten levels would BLUR together.", 5.6),
    ("count",    "With three switches, you can count from zero to seven.",
                 "With 3 switches you can count from 0 to 7.", 4.6),
    ("byte",     "Eight switches make a byte. That's two hundred and fifty six patterns, enough for every letter. "
                 "Capital A is zero one zero zero zero zero zero one.",
                 "8 switches = 1 BYTE = 256 patterns. 'A' = 01000001 (65).", 6.6),
    ("math",     "n bits give two to the power n patterns.",
                 "n bits → 2ⁿ patterns.", 3.4),
    ("end",      "Follow C B S E Mock for more why videos.",
                 "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """💡 WHY? — Why do computers use BINARY?

A chip holds billions of tiny switches (transistors): OFF or ON → 0 or 1
Two levels are easy to tell apart even with electrical noise — ten levels would blur together ⚡
3 switches → count 0 to 7 · 8 switches = 1 byte = 256 patterns
'A' = 01000001 = 65 🔤
n bits → 2ⁿ patterns

Number systems & data representation — Computer Science basics. 🧠

💾 Save it · 📤 Share with your CS batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Binary #ComputerScience #NumberSystem #CSClass12 #Coding #CBSE"""


def bulb(dax, x, y, on, a, r=0.38, lab=True):
    if on:
        dax.add_patch(Circle((x, y), r * 1.6, color=GOLD, alpha=0.18 * a, zorder=4))
    dax.add_patch(Circle((x, y), r, facecolor=GOLD if on else "#1b2742", edgecolor=GOLD if on else GREY, lw=2.5,
                         alpha=a, zorder=5))
    if lab:
        dax.text(x, y - r - 0.32, "1" if on else "0", ha="center", va="center", fontsize=26, fontweight="bold",
                 color=GOLD if on else GREY, family="DejaVu Sans Mono", alpha=a, zorder=6)


def draw(c):
    dax = c.area(0.0, 0.0, 7.6)
    hk = ease(c.phase("hook", 0.15, 0.55)) * (1 - ease(c.phase("switch", 0.0, 0.2)))
    if hk > 0:
        rng = np.random.default_rng(int(c.t * 6))
        for r in range(5):
            row = "".join(str(int(v)) for v in rng.integers(0, 2, 12))
            dax.text(0, 2.0 - r * 0.95, " ".join(row), ha="center", va="center", fontsize=30, fontweight="bold",
                     color=GREEN, family="DejaVu Sans Mono", alpha=hk * (0.35 + 0.15 * r), zorder=4)
    # 1) one switch
    sw = ease(c.phase("switch", 0.1, 0.35)) * (1 - ease(c.phase("reliable", 0.0, 0.2)))
    if sw > 0:
        on = int(c.t * 1.2) % 2 == 1 and c.phase("switch", 0.35, 1) > 0
        bulb(dax, 0, 1.0, on, sw, r=0.75)
        outline(dax.text(0, -0.75, "ON = 1" if on else "OFF = 0", ha="center", fontsize=40, fontweight="bold",
                         color=GOLD if on else LTGREY, alpha=sw, zorder=7))
        outline(dax.text(0, 2.45, "transistor switch", ha="center", fontsize=24, fontweight="bold", color=CYAN, alpha=sw, zorder=7))

    # 2) noise: 2 levels vs 10 levels
    ra = ease(c.phase("reliable", 0.1, 0.4)) * (1 - ease(c.phase("count", 0.0, 0.2)))
    if ra > 0:
        rng = np.random.default_rng(int(c.t * 8))
        for side, (levels, x0, title, col) in enumerate([(2, -3.4, "2 levels: clear", GREEN), (10, 0.4, "10 levels: blurry", PINK)]):
            outline(dax.text(x0 + 1.5, 2.35, title, ha="center", fontsize=24, fontweight="bold", color=col, alpha=ra, zorder=7))
            seq = [1, 0, 1, 1, 0, 1, 0, 0] if levels == 2 else [7, 2, 5, 9, 3, 6, 1, 8]
            for k, v in enumerate(seq):
                h = (v / (levels - 1)) * 3.0 + rng.normal(0, 0.28)
                dax.add_patch(Rectangle((x0 + k * 0.38, -1.6), 0.3, max(0.05, h), facecolor=col, edgecolor="none",
                                        alpha=0.85 * ra, zorder=5))
            for L in range(levels):
                y = -1.6 + L / (levels - 1) * 3.0
                dax.plot([x0 - 0.1, x0 + 3.1], [y, y], color=LTGREY, lw=1, alpha=0.35 * ra, zorder=4)
        outline(dax.text(0.0, -2.25, "+ electrical noise", ha="center", fontsize=22, fontweight="bold", color=LTGREY,
                         alpha=ra, zorder=7))

    # 3) three bulbs counting 0..7
    ca = ease(c.phase("count", 0.05, 0.25)) * (1 - ease(c.phase("byte", 0.0, 0.2)))
    if ca > 0:
        n = min(7, int(c.phase("count", 0.2, 0.95) * 8))
        bits = [(n >> (2 - k)) & 1 for k in range(3)]
        for k in range(3):
            bulb(dax, -1.6 + k * 1.6, 1.3, bits[k] == 1, ca, r=0.55)
            dax.text(-1.6 + k * 1.6, 2.2, str(2 ** (2 - k)), ha="center", fontsize=20, color=LTGREY, alpha=ca, zorder=6)
        outline(dax.text(0, -0.8, f"{bits[0]}{bits[1]}{bits[2]}  =  {n}", ha="center", fontsize=46, fontweight="bold",
                         color=WHITE, family="DejaVu Sans Mono", alpha=ca, zorder=7))
        outline(dax.text(0, -1.9, "3 bits → 8 patterns (0 to 7)", ha="center", fontsize=24, fontweight="bold",
                         color=CYAN, alpha=ca, zorder=7))

    # 4) a byte = 'A'
    ba = ease(c.phase("byte", 0.05, 0.3))
    if ba > 0:
        bits = [0, 1, 0, 0, 0, 0, 0, 1]
        show = c.phase("byte", 0.45, 0.8)
        for k in range(8):
            on = bits[k] == 1 and show > k / 8
            bulb(dax, -3.15 + k * 0.9, 1.25, on, ba, r=0.32)
        outline(dax.text(0, 2.3, "1 byte = 8 bits = 256 patterns", ha="center", fontsize=26, fontweight="bold",
                         color=CYAN, alpha=ba, zorder=7))
        aa = back_out(c.phase("byte", 0.8, 0.95))
        if aa > 0.01:
            outline(dax.text(0, -0.85, "01000001 = 65 = 'A'", ha="center", fontsize=40 * min(1, aa), fontweight="bold",
                             color=GOLD, family="DejaVu Sans Mono", zorder=7))
    c.steps([(r"$n$ bits $\rightarrow 2^{n}$ patterns", 0.0, WHITE),
             (r"8 bits = 1 byte = $2^{8}$ = 256", 0.35, GOLD)], ys=(0.360, 0.290))
