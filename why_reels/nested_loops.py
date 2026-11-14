"""WHY? — How do nested loops work, and why do we use them?  (Class 11/12 Computer Science · Python)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY
from why_reels._codebox import code

TITLE = "How do NESTED loops work?"
TAGS = "Computer Science"
BEATS = [
    ("hook",   "A loop inside a loop sounds confusing. But it's just like a clock. Let's print a grid of stars.",
               "A loop INSIDE a loop? It's just like a CLOCK. Let's print a grid of stars.", 4.6),
    ("outer",  "The outer loop runs three times, once for each row.",
               "The OUTER loop runs 3 times — once per ROW.", 3.6),
    ("inner",  "For every single pass of the outer loop, the inner loop runs completely. Four stars, one for each column.",
               "For EVERY outer pass, the INNER loop runs completely: 4 stars, one per column.", 5.4),
    ("clock",  "Like a clock. The minute hand goes all the way round, for each step of the hour hand.",
               "Like a clock: the minute hand (inner) goes all the way round for each hour (outer).", 5.2),
    ("use",    "We use nested loops for patterns, multiplication tables, matrices, and comparing every pair of items.",
               "Used for PATTERNS, TABLES, MATRICES and comparing every PAIR of items.", 5.0),
    ("math",   "Total runs equals outer times inner. Three times four, twelve stars.",
               "Total runs = outer × inner = 3 × 4 = 12 stars", 3.8),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🔁 WHY? — How do NESTED loops work?

for i in range(3):        # outer: rows
    for j in range(4):    # inner: columns
        print("*", end=" ")
    print()

For EVERY pass of the outer loop, the inner loop runs completely 🕐
Like a clock: minute hand goes round once for each hour.

Total runs = outer × inner = 3 × 4 = 12 ⭐
Used for patterns, multiplication tables, matrices, comparing pairs.

Python — Computer Science, Class 11 & 12. 💻

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Python #NestedLoops #ComputerScience #Class12CS #Coding #CBSE"""

END_Y = 0.395
LINES = ["for i in range(3):", "    for j in range(4):", '        print("*", end=" ")', "    print()"]


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    ck = ease(c.phase("clock", 0.0, 0.2)) * (1 - ease(c.phase("use", 0.0, 0.2)))
    us = ease(c.phase("use", 0.0, 0.25)) * (1 - ease(c.phase("math", 0.0, 0.25)))
    main = 1 - max(ck, us)
    a0 = ease(c.phase("hook", 0.1, 0.4))
    # star counter: 12 steps across outer+inner beats
    prog = ease(c.phase("outer", 0.3, 1.0)) * 0.25 + ease(c.phase("inner", 0.0, 0.9)) * 0.75
    if c.at("math"):
        prog = 1.0
    k_done = int(prog * 12 + 1e-6)
    i_cur, j_cur = divmod(min(k_done, 11), 4)
    hl = None
    if c.at("outer") and k_done < 12:
        hl = 2 if c.at("inner") else 0
    if main > 0.01:
        code(dax, -3.2, 2.5, LINES, a0 * main, w=6.4, hl=hl, title="stars.py")
        # loop counters
        if c.at("outer"):
            ca = ease(c.phase("outer", 0.0, 0.3)) * main
            outline(dax.text(-3.1, -0.85, f"i = {i_cur}", ha="left", fontsize=26, color=PINK, fontweight="bold",
                             alpha=ca, zorder=8, family="DejaVu Sans Mono"))
            ja = ease(c.phase("inner", 0.0, 0.3)) * main
            outline(dax.text(-3.1, -1.55, f"j = {j_cur if k_done < 12 else 3}", ha="left", fontsize=26, color=CYAN,
                             fontweight="bold", alpha=ja, zorder=8, family="DejaVu Sans Mono"))
        # the star grid
        for k in range(12):
            r, q = divmod(k, 4)
            x, y = -0.1 + 0.68 * q, -0.75 - 0.66 * r
            done = k < k_done
            dax.add_patch(Circle((x, y), 0.27, facecolor="#13264d", edgecolor="#2a3d6b", lw=2, alpha=a0 * main * 0.8,
                                 zorder=5))
            if done:
                dax.text(x, y - 0.03, "★", ha="center", va="center", fontsize=28, color=GOLD, alpha=a0 * main, zorder=6,
                         family="DejaVu Sans")
        ra = ease(c.phase("outer", 0.2, 0.5)) * main
        for r in range(3):
            outline(dax.text(-0.6, -0.75 - 0.66 * r, f"row {r}", ha="right", va="center", fontsize=17, color=PINK,
                             fontweight="bold", alpha=ra, zorder=7))
    if ck > 0.01:
        dax.add_patch(Circle((0, 0.1), 2.0, facecolor="#0b1530", edgecolor=LTGREY, lw=4, alpha=ck, zorder=4))
        for h in range(12):
            ang = np.pi / 2 - h * np.pi / 6
            dax.plot([1.7 * np.cos(ang), 1.9 * np.cos(ang)], [0.1 + 1.7 * np.sin(ang), 0.1 + 1.9 * np.sin(ang)],
                     color=LTGREY, lw=3, alpha=ck, zorder=5)
        tt = c.phase("clock", 0.1, 1.0)
        ma_ = np.pi / 2 - tt * 2 * np.pi * 2
        ha_ = np.pi / 2 - (np.pi / 6) * (1 + tt * 2)
        dax.plot([0, 1.6 * np.cos(ma_)], [0.1, 0.1 + 1.6 * np.sin(ma_)], color=CYAN, lw=5, alpha=ck, zorder=6)
        dax.plot([0, 1.0 * np.cos(ha_)], [0.1, 0.1 + 1.0 * np.sin(ha_)], color=PINK, lw=8, alpha=ck, zorder=6)
        outline(dax.text(-2.4, 2.1, "hour = outer", ha="center", fontsize=21, color=PINK, fontweight="bold", alpha=ck, zorder=8))
        outline(dax.text(2.4, 2.1, "minute = inner", ha="center", fontsize=21, color=CYAN, fontweight="bold", alpha=ck, zorder=8))
    if us > 0.01:
        items = (("patterns", "*\n**\n***", GOLD), ("tables", "2×1\n2×2\n2×3", CYAN), ("matrices", "[1 2]\n[3 4]", GREEN),
                 ("pairs", "(a,b)\n(a,c)\n(b,c)", PINK))
        for k, (t, ex, col) in enumerate(items):
            x, y = -1.65 + 3.3 * (k % 2), 1.0 - 2.2 * (k // 2)
            a = us * ease(c.phase("use", 0.1 + 0.15 * k, 0.3 + 0.15 * k))
            dax.add_patch(FancyBboxPatch((x - 1.45, y - 0.95), 2.9, 1.9, boxstyle="round,pad=0,rounding_size=0.18",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=a, zorder=5))
            dax.text(x, y + 0.6, t, ha="center", va="center", fontsize=21, color=col, fontweight="bold", alpha=a, zorder=6)
            dax.text(x, y - 0.2, ex, ha="center", va="center", fontsize=15, color=WHITE, alpha=a, zorder=6,
                     family="DejaVu Sans Mono", linespacing=1.0)
    c.steps([("total runs = outer × inner", 0.0, WHITE),
             ("3 × 4 = 12 stars", 0.3, GOLD)], ys=(0.345, 0.285))
