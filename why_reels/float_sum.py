"""WHY? — Why is 0.1 + 0.2 ≠ 0.3 in Python?  (Computer Science, Class 12)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = r"Why is 0.1 + 0.2 $\neq$ 0.3 in Python?"
TAGS = "Class 12 Computer Science"
BEATS = [
    ("hook",   "Type point one plus point two in Python. The answer is not point three! Why?",
               "Type 0.1 + 0.2 in Python. The answer is NOT 0.3! Why?", 4.6),
    ("binary", "Computers store every number in binary, using only zeros and ones.",
               "Computers store every number in binary — only 0s and 1s.", 3.6),
    ("third",  "In decimal, one third never ends. Point three three three, forever.",
               "In decimal, 1/3 never ends: 0.333333… forever.", 3.8),
    ("tenth",  "In binary, one tenth has the same problem. It repeats forever.",
               "In binary, 1/10 has the SAME problem: 0.000110011001100… forever.", 4.2),
    ("cut",    "The computer must cut it off after fifty two bits, so it stores a number that is very slightly off.",
               "Python cuts it off after 52 bits, so it stores a number that's very slightly off.", 5.4),
    ("add",    "Add two slightly-off numbers, and the tiny errors add up and show.",
               "Add two slightly-off numbers and the tiny errors show up.", 4.4),
    ("fix",    "So never compare decimals with double equals. Round them, or use math dot is close.",
               "So never compare floats with ==. Use round() or math.isclose().", 5.0),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🐍 WHY? — Why does 0.1 + 0.2 give 0.30000000000000004 in Python?

Computers store numbers in binary (0s and 1s).
1/10 in binary never ends: 0.000110011001100… ♾️
Python cuts it after 52 bits → a tiny error → it shows up when you add! 😮

✅ Fix: round(0.1 + 0.2, 2) == 0.3  or  math.isclose(0.1 + 0.2, 0.3)

A classic CS Class 12 viva / interview question! 🧠

💾 Save it · 📤 Share with your coding friends

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Python #ComputerScience #CSClass12 #Coding #FloatingPoint #CBSE"""

MONO = "DejaVu Sans Mono"
END_Y = 0.305


def terminal(dax, x, y, w, h, alpha, title="Python"):
    dax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.18",
                                 facecolor="#0b1222", edgecolor="#3a4a6b", lw=2.5, alpha=alpha, zorder=5))
    dax.add_patch(FancyBboxPatch((x, y + h - 0.55), w, 0.55, boxstyle="round,pad=0,rounding_size=0.18",
                                 facecolor="#1b2742", edgecolor="none", alpha=alpha, zorder=6))
    for k, col in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        dax.plot([x + 0.35 + k * 0.32], [y + h - 0.27], "o", color=col, ms=11, alpha=alpha, zorder=7)
    dax.text(x + w / 2, y + h - 0.27, title, ha="center", va="center", fontsize=17, color=LTGREY,
             alpha=alpha, zorder=7)


def typed(s, f):
    n = int(len(s) * max(0.0, min(1.0, f)))
    return s[:n]


def mono(dax, x, y, s, col, size=30, alpha=1.0, ha="left"):
    dax.text(x, y, s, ha=ha, va="center", fontsize=size, color=col, family=MONO, fontweight="bold",
             alpha=alpha, zorder=8)


def draw(c):
    dax = c.area(0.0, -0.45, 8.8, box=[0.0, 0.25, 1.0, 0.57])

    # 1) the surprise in a terminal (stays at the top, shrinks a little later)
    ta = ease(c.phase("hook", 0.0, 0.15))
    small = ease(c.phase("binary", 0.0, 0.4))
    if not c.at("fix"):
        y0 = lerp(-0.6, 1.55, small)
        h = lerp(3.0, 1.9, small)
        terminal(dax, -4.2, y0, 8.4, h, ta)
        cmd = typed(">>> 0.1 + 0.2", c.phase("hook", 0.05, 0.35))
        mono(dax, -3.9, y0 + h - 1.0, cmd, WHITE, size=lerp(34, 26, small), alpha=ta)
        ra = c.phase("hook", 0.45, 0.6)
        if ra > 0:
            mono(dax, -3.9, y0 + h - lerp(1.85, 1.5, small), "0.30000000000000004", GOLD,
                 size=lerp(34, 26, small), alpha=ra)
        wa = back_out(c.phase("hook", 0.65, 0.85))
        if wa > 0 and small < 1:
            outline(dax.text(2.6, y0 + 0.35, "≠ 0.3 ?!", ha="center", fontsize=40 * min(1, wa), fontweight="bold",
                             color=PINK, alpha=(1 - small), zorder=9))

    # 2) binary basics
    ba = ease(c.phase("binary", 0.3, 0.7)) * (1 - ease(c.phase("third", 0.0, 0.25)))
    if ba > 0:
        rows = [("0.5", "0.1₂"), ("0.25", "0.01₂"), ("0.75", "0.11₂")]
        for k, (d, b) in enumerate(rows):
            y = 0.3 - k * 1.05
            mono(dax, -1.4, y, d, WHITE, 38, ba, ha="right")
            mono(dax, -0.9, y, "=", GREY, 38, ba)
            mono(dax, 0.0, y, b, CYAN, 38, ba)
        outline(dax.text(0, -3.0, "these end neatly ✓", ha="center", fontsize=32, color=GREEN, fontweight="bold",
                         alpha=ba, zorder=9))

    # 3) 1/3 in decimal never ends
    th = c.phase("third", 0.2, 1.0) * (1 - ease(c.phase("tenth", 0.0, 0.2)))
    if th > 0:
        digits = "0." + "3" * int(2 + 10 * c.phase("third", 0.2, 0.9))
        mono(dax, -4.0, -0.4, "1/3 =", WHITE, 36, ease(min(1, th * 3)))
        mono(dax, -1.9, -0.4, digits + "…", GOLD, 36, ease(min(1, th * 3)))
        outline(dax.text(0, -1.8, "decimal: never ends", ha="center", fontsize=32, color=LTGREY, fontweight="bold",
                         alpha=ease(min(1, th * 3)), zorder=9))

    # 4) 1/10 in binary never ends either
    tn = c.phase("tenth", 0.15, 1.0)
    if tn > 0 and not c.at("add"):
        bits = "0001100110011001100110011"
        n = int(4 + (len(bits) - 4) * min(1, c.phase("tenth", 0.15, 0.9) + c.phase("cut", 0, 1)))
        a = ease(min(1, tn * 3)) * (1 - ease(c.phase("add", 0.0, 0.2)))
        mono(dax, -4.0, -0.1, "0.1 =", WHITE, 34, a)
        shown = "0." + bits[:n]
        # wrap the long bit string over two lines
        mono(dax, -2.1, -0.1, shown[:14], CYAN, 34, a)
        if len(shown) > 14:
            mono(dax, -2.1, -0.95, shown[14:] + ("…" if not c.at("cut") else ""), CYAN, 34, a)
        outline(dax.text(0, -2.1, "binary: never ends either!", ha="center", fontsize=32, color=PINK,
                         fontweight="bold", alpha=a, zorder=9))

    # 5) cut after 52 bits
    cu = ease(c.phase("cut", 0.15, 0.5)) * (1 - ease(c.phase("add", 0.0, 0.2)))
    if cu > 0:
        dax.plot([2.75, 2.75], [-1.4, 0.4], color=GOLD, lw=4, ls=(0, (3, 2)), alpha=cu, zorder=9)
        outline(dax.text(2.75, 0.7, "✂ 52 bits", ha="center", fontsize=30, color=GOLD, fontweight="bold",
                         alpha=cu, zorder=9))
        sa = ease(c.phase("cut", 0.45, 0.8)) * (1 - ease(c.phase("add", 0.0, 0.2)))
        mono(dax, 0, -3.0, "stored: 0.10000000000000000555…", GOLD, 27, sa, ha="center")

    # 6) the errors add up
    if c.at("add") and not c.at("fix"):
        ad = c.phase("add", 0.1, 0.8)
        lines = [("  0.1000000000000000055511", WHITE, 0.0), ("+ 0.2000000000000000111022", WHITE, 0.25),
                 ("= 0.3000000000000000444089", GOLD, 0.55)]
        for k, (s, col, at) in enumerate(lines):
            a = ease((ad - at) / 0.2)
            if a > 0:
                mono(dax, -4.1, 0.1 - k * 1.05, s, col, 29, a)
        if ad > 0.5:
            dax.plot([-4.1, 4.1], [-1.53, -1.53], color=GREY, lw=2, alpha=ease((ad - 0.5) / 0.2), zorder=8)
        ea = ease(c.phase("add", 0.75, 0.95))
        if ea > 0:
            dax.annotate("tiny error!", xy=(3.6, -2.25), xytext=(1.6, -3.3), color=PINK, fontsize=30,
                         fontweight="bold", ha="center", alpha=ea, zorder=9,
                         arrowprops=dict(arrowstyle="-|>", color=PINK, lw=2.5, alpha=ea))

    # 7) the fix
    if c.at("fix"):
        fa = ease(c.phase("fix", 0.0, 0.2))
        terminal(dax, -4.2, -3.1, 8.4, 5.9, fa, title="Python — the right way")
        rows = [(">>> 0.1 + 0.2 == 0.3", WHITE, 0.05), ("False", PINK, 0.15),
                (">>> round(0.1 + 0.2, 2) == 0.3", WHITE, 0.3), ("True", GREEN, 0.45),
                (">>> math.isclose(0.1 + 0.2, 0.3)", WHITE, 0.55), ("True", GREEN, 0.7)]
        for k, (s, col, at) in enumerate(rows):
            a = c.phase("fix", at, at + 0.12)
            if a > 0:
                mono(dax, -3.95, 1.45 - k * 0.78, typed(s, a * 1.5), col, 25)
