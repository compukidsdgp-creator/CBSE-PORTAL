"""WHY? — Why does time complexity matter more than just working code?  (Class 12 Computer Science)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY
from why_reels._codebox import code

TITLE = "Why does TIME COMPLEXITY matter?"
TAGS = "Computer Science"
BEATS = [
    ("hook",   "Two programs. Both correct. One finishes in a blink. The other takes hours. How?",
               "Two programs, both CORRECT. One finishes in a blink, the other takes HOURS. How?", 4.4),
    ("task",   "The task: check whether a list has any duplicate.",
               "Task: does a list have any DUPLICATE?", 3.2),
    ("slow",   "Program one compares every item with every other item. For n items, that's about n squared comparisons.",
               "Program 1 compares EVERY pair → about n² steps.", 5.0),
    ("fast",   "Program two remembers what it has seen, in a set. One pass. About n steps.",
               "Program 2 remembers what it's seen in a SET → one pass → about n steps.", 4.4),
    ("grow",   "With a million items, n squared is a trillion steps. Hours! n is a million steps. A hundredth of a second.",
               "1 million items: n² = 10¹² steps (HOURS!)  vs  n = 10⁶ steps (0.01 s).", 6.0),
    ("bigO",   "Time complexity tells you how the steps grow as the data grows. That's what decides if code scales.",
               "TIME COMPLEXITY: how steps GROW as data grows — it decides if code SCALES.", 5.0),
    ("math",   "Big O of n squared, versus big O of n. Working is not enough. It must scale.",
               "O(n²) vs O(n): working isn't enough — it must SCALE.", 4.0),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """⏱️ WHY? — Why does TIME COMPLEXITY matter more than just working code?

Task: does a list have a duplicate?

🐢 Compare every pair → ~n² steps → O(n²)
🚀 Remember seen items in a set → ~n steps → O(n)

For 1 million items:
n² = 10¹² steps → hours 😴
n = 10⁶ steps → 0.01 s ⚡

Time complexity = how the steps GROW as data grows. Working isn't enough — it must SCALE.

Algorithms — Computer Science. 💻

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #TimeComplexity #BigO #Algorithms #ComputerScience #Class12CS #CBSE"""

SLOW = ["for i in range(n):", "    for j in range(i+1, n):", "        if a[i] == a[j]:", "            return True"]
FAST = ["seen = set()", "for x in a:", "    if x in seen: return True", "    seen.add(x)"]


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    a0 = ease(c.phase("hook", 0.05, 0.35))
    ta = ease(c.phase("task", 0.0, 0.25))
    gr = ease(c.phase("grow", 0.0, 0.25))
    bo = ease(c.phase("bigO", 0.0, 0.25))
    ma = ease(c.phase("math", 0.0, 0.3))
    ha = a0 * (1 - ta)
    if ha > 0.01:
        for k, (lab, col, tm) in enumerate((("program 1", PINK, "3 hours"), ("program 2", GREEN, "0.01 s"))):
            dax.add_patch(FancyBboxPatch((-2.95 + 3.05 * k, -0.6), 2.85, 1.9, boxstyle="round,pad=0,rounding_size=0.2",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=ha, zorder=5))
            dax.text(-1.52 + 3.05 * k, 0.75, lab, ha="center", va="center", fontsize=21, color=LTGREY, fontweight="bold",
                     alpha=ha, zorder=6)
            dax.text(-1.52 + 3.05 * k, 0.0, tm, ha="center", va="center", fontsize=34, color=col, fontweight="bold",
                     alpha=ha * ease(c.phase("hook", 0.3 + 0.2 * k, 0.5 + 0.2 * k)), zorder=6)
        outline(dax.text(0, 1.95, "both correct ✓", ha="center", fontsize=26, color=WHITE, fontweight="bold", alpha=ha, zorder=8))
    cd = ta * (1 - gr)
    if cd > 0.01:
        if c.at("task") and not c.at("slow"):
            outline(dax.text(0, 1.5, "a = [7, 3, 9, 3, 5, …]", ha="center", fontsize=28, color=WHITE, fontweight="bold",
                             alpha=cd, zorder=8, family="DejaVu Sans Mono"))
            outline(dax.text(0, 0.3, "any duplicate?", ha="center", fontsize=32, color=GOLD, fontweight="bold",
                             alpha=cd, zorder=8))
        sl = ease(c.phase("slow", 0.0, 0.3)) * (1 - ease(c.phase("fast", 0.0, 0.2)))
        code(dax, -3.2, 2.45, SLOW, cd * sl, size=24, title="program 1", hl=1, hl_col=PINK)
        if sl > 0:
            outline(dax.text(0, -0.5, "every pair → ~n² steps", ha="center", fontsize=28, color=PINK, fontweight="bold",
                             alpha=cd * sl * ease(c.phase("slow", 0.4, 0.7)), zorder=8))
        fa = ease(c.phase("fast", 0.1, 0.4))
        code(dax, -3.2, 2.45, FAST, cd * fa, size=24, title="program 2", hl=2, hl_col=GREEN)
        if fa > 0:
            outline(dax.text(0, -0.5, "one pass → ~n steps", ha="center", fontsize=28, color=GREEN, fontweight="bold",
                             alpha=cd * fa * ease(c.phase("fast", 0.4, 0.7)), zorder=8))
    gg = gr * (1 - bo)
    if gg > 0.01:
        for k, (lab, steps, tm, col, frac) in enumerate((("n²", "10¹² steps", "≈ 3 hours", PINK, 1.0),
                                                         ("n", "10⁶ steps", "0.01 s", GREEN, 0.012))):
            y = 1.3 - 1.9 * k
            g = ease(c.phase("grow", 0.15 + 0.3 * k, 0.55 + 0.3 * k))
            dax.add_patch(Rectangle((-2.2, y - 0.3), 5.2, 0.6, fill=False, edgecolor=GREY, lw=2, alpha=gg, zorder=4))
            dax.add_patch(Rectangle((-2.2, y - 0.3), max(0.06, 5.2 * frac * g), 0.6, facecolor=col, edgecolor="none",
                                    alpha=gg, zorder=5))
            outline(dax.text(-2.4, y, lab, ha="right", va="center", fontsize=30, color=col, fontweight="bold", alpha=gg, zorder=8))
            outline(dax.text(-2.2, y - 0.6, f"{steps}  →  {tm}", ha="left", va="center", fontsize=21, color=WHITE,
                             fontweight="bold", alpha=gg * g, zorder=8))
        outline(dax.text(0, 2.3, "n = 1,000,000 items", ha="center", fontsize=24, color=GOLD, fontweight="bold",
                         alpha=gg, zorder=8))
    if bo > 0.01:
        b = bo * (1 - ma)
        x0, y0, Wd, Hd = -2.8, -1.9, 5.6, 3.9
        dax.plot([x0, x0 + Wd], [y0, y0], color=GREY, lw=2, alpha=b, zorder=4)
        dax.plot([x0, x0], [y0, y0 + Hd], color=GREY, lw=2, alpha=b, zorder=4)
        g = ease(c.phase("bigO", 0.1, 0.7))
        n = np.linspace(0, 1, 200)[: max(2, int(200 * g))]
        dax.plot(x0 + Wd * n, y0 + Hd * n ** 2, color=PINK, lw=4, alpha=b, zorder=5)
        dax.plot(x0 + Wd * n, y0 + Hd * 0.25 * n, color=GREEN, lw=4, alpha=b, zorder=5)
        outline(dax.text(x0 + Wd * 0.7, y0 + Hd * 0.75, "O(n²)", fontsize=28, color=PINK, fontweight="bold", alpha=b * g, zorder=8))
        outline(dax.text(x0 + Wd * 0.75, y0 + Hd * 0.3, "O(n)", fontsize=28, color=GREEN, fontweight="bold", alpha=b * g, zorder=8))
        outline(dax.text(x0 + Wd, y0 - 0.35, "data size n →", ha="right", fontsize=18, color=LTGREY, fontweight="bold",
                         alpha=b, zorder=8))
        outline(dax.text(x0 + 0.1, y0 + Hd + 0.15, "steps", ha="left", fontsize=18, color=LTGREY, fontweight="bold",
                         alpha=b, zorder=8))
    if ma > 0.01:
        outline(dax.text(0, 0.9, "O(n²)  vs  O(n)", ha="center", fontsize=44, color=GOLD, fontweight="bold", alpha=ma, zorder=8))
        outline(dax.text(0, -0.3, "it must SCALE", ha="center", fontsize=34, color=GREEN, fontweight="bold",
                         alpha=ease(c.phase("math", 0.3, 0.6)), zorder=8))
    c.steps([("correct code isn't enough", 0.0, WHITE),
             ("it must scale: O(n) beats O(n²)", 0.3, GOLD)], ys=(0.345, 0.285))
