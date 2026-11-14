"""WHY? — Why do we use lists when we already have variables?  (Class 11/12 Computer Science · Python)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY
from why_reels._codebox import code

TITLE = "Why use a LIST when we have variables?"
TAGS = "Computer Science"
BEATS = [
    ("hook",   "You need to store the marks of forty students. Forty variables? m one, m two, m three, all the way to m forty?",
               "Store marks of 40 students… 40 variables? m1, m2, m3 … m40?!", 5.0),
    ("pain",   "Now find the average. You'd have to type all forty names. And if a new student joins, you change the code.",
               "Average? Type all 40 names! New student joins? Change the code!", 4.8),
    ("list",   "A list stores all of them under one name. Each value has a position, called an index, starting from zero.",
               "A LIST stores them all under ONE name — each has an INDEX, starting from 0.", 5.4),
    ("loop",   "Now one line does the job. Sum of marks, divided by length of marks. Forty students or four thousand.",
               "Now ONE line: sum(marks) / len(marks) — 40 students or 4000!", 5.0),
    ("grow",   "A new student? Just append. The list grows by itself.",
               "New student? marks.append(…) — the list GROWS by itself.", 3.8),
    ("math",   "One name, many values. Loop once, handle all.",
               "One name, many values. Loop once, handle ALL.", 3.4),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """📋 WHY? — Why use a LIST when we already have variables?

40 students → m1, m2, m3 … m40? 😵
Average = (m1 + m2 + … + m40) / 40 — and change the code for every new student!

marks = [78, 92, 65, 88, …]   # ONE name, many values
marks[0] → 78   (index starts at 0)
avg = sum(marks) / len(marks)   # works for 40 or 4000
marks.append(71)   # new student joins ✅

Lists in Python — Computer Science, Class 11 & 12. 💻

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Python #Lists #ComputerScience #Class12CS #Coding #CBSE"""

VALS = [78, 92, 65, 88, 71, 95]


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    la = ease(c.phase("list", 0.0, 0.3))
    a0 = ease(c.phase("hook", 0.05, 0.3)) * (1 - la)
    if a0 > 0.01:
        n = int(3 + 37 * ease(c.phase("hook", 0.2, 0.9)))
        for k in range(min(n, 40)):
            r, q = divmod(k, 5)
            x, y = -3.3 + 1.32 * q, 2.3 - 0.52 * r
            dax.text(x, y, f"m{k + 1} = {VALS[k % 6]}", ha="left", va="center", fontsize=17, color=PINK if k > 2 else WHITE,
                     alpha=a0, zorder=6, family="DejaVu Sans Mono")
        pa = ease(c.phase("pain", 0.1, 0.4)) * (1 - la)
        if pa > 0:
            dax.add_patch(FancyBboxPatch((-3.2, -2.45), 6.4, 0.9, boxstyle="round,pad=0,rounding_size=0.12",
                                         facecolor="#2a0716", edgecolor=PINK, lw=3, alpha=pa, zorder=7))
            dax.text(0, -2.0, "avg = (m1 + m2 + … + m40) / 40", ha="center", va="center", fontsize=20, color=PINK,
                     alpha=pa, zorder=8, family="DejaVu Sans Mono")
    if la > 0.01:
        lb = la * (1 - ease(c.phase("math", 0.0, 0.3)))
        grow = ease(c.phase("grow", 0.2, 0.6))
        n = 6 if grow < 0.5 else 7
        vals = VALS + [83]
        outline(dax.text(-3.1, 2.15, "marks =", ha="left", va="center", fontsize=26, color=CYAN, fontweight="bold",
                         alpha=lb, zorder=8, family="DejaVu Sans Mono"))
        bw = 0.86
        for k in range(n):
            x = -3.0 + bw * k
            a = lb * (ease(c.phase("list", 0.15 + 0.08 * k, 0.3 + 0.08 * k)) if k < 6 else back_out(grow * 2 - 1))
            a = max(0, min(1, a))
            col = GREEN if k == 6 else GOLD
            dax.add_patch(FancyBboxPatch((x, 0.75), bw - 0.08, 0.85, boxstyle="round,pad=0,rounding_size=0.08",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=a, zorder=5))
            dax.text(x + (bw - 0.08) / 2, 1.18, str(vals[k]), ha="center", va="center", fontsize=22, color=WHITE,
                     fontweight="bold", alpha=a, zorder=6)
            dax.text(x + (bw - 0.08) / 2, 0.45, str(k), ha="center", va="center", fontsize=17, color=CYAN, alpha=a,
                     zorder=6, family="DejaVu Sans Mono")
        ia = ease(c.phase("list", 0.7, 0.95)) * lb
        outline(dax.text(-3.1, -0.05, "index →  marks[0] = 78", ha="left", va="center", fontsize=21, color=CYAN,
                         fontweight="bold", alpha=ia * (1 - ease(c.phase("loop", 0.0, 0.2))), zorder=8,
                         family="DejaVu Sans Mono"))
        lp = ease(c.phase("loop", 0.1, 0.4)) * (1 - ease(c.phase("grow", 0.0, 0.2)))
        code(dax, -3.2, 0.2, ["avg = sum(marks) / len(marks)"], lp * lb, title="one line")
        if lp > 0:
            outline(dax.text(0, -1.75, "40 or 4000 students — same line", ha="center", fontsize=22, color=GREEN,
                             fontweight="bold", alpha=lp * lb, zorder=8))
        ga = ease(c.phase("grow", 0.05, 0.3)) * lb
        code(dax, -3.2, 0.2, ["marks.append(83)"], ga, title="new student", hl=0, hl_col=GREEN)
    ma = ease(c.phase("math", 0.0, 0.35))
    if ma > 0.01:
        outline(dax.text(0, 0.8, "one name", ha="center", fontsize=40, color=CYAN, fontweight="bold", alpha=ma, zorder=8))
        outline(dax.text(0, -0.3, "many values", ha="center", fontsize=40, color=GOLD, fontweight="bold",
                         alpha=ease(c.phase("math", 0.25, 0.55)), zorder=8))
    c.steps([("one name, many values", 0.0, WHITE),
             ("loop once, handle all", 0.3, GOLD)], ys=(0.345, 0.285))
