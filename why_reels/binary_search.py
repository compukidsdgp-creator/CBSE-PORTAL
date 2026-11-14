"""WHY? — Why is binary search so fast?  (Computer Science, Class 12)"""
import math
import numpy as np
from matplotlib.patches import FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, NAVY, WHITE, LTGREY, GREY

TITLE = "Why is BINARY SEARCH so fast?"
TAGS = "Class 12 Computer Science"
BEATS = [
    ("hook",   "Why can binary search find one item among a thousand, in just ten steps?",
               "How can binary search find one item among 1000 in just 10 steps?", 4.0),
    ("linear", "Checking one by one, you might need all thousand tries.",
               "Checking one by one, you might need all 1000 tries.", 4.4),
    ("middle", "But if the list is sorted, jump straight to the middle.",
               "But if the list is SORTED, jump straight to the middle.", 3.4),
    ("half",   "Looking for forty one, and the middle is thirty one? Throw away the whole left half, in one step.",
               "Looking for 41, middle is 31? Throw away the whole left half in ONE step.", 5.2),
    ("repeat", "Repeat. Every step cuts what's left in half, until only the answer remains.",
               "Repeat. Every step cuts what's left in half… until only the answer remains.", 6.2),
    ("math",   "A thousand halves to one in about ten steps. That's log base two of n. "
               "A million items? Just twenty steps.",
               "1000 → 1 in about 10 halvings: steps ≈ log₂ n. A million items? Just 20 steps!", 6.4),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """💻 WHY? — Why is Binary Search so fast?

Linear search: check items one by one → up to 1000 tries 🐢
Binary search: open the middle, throw away half, repeat → about 10 tries ⚡
That's log₂ n — a million items in just 20 steps!

One of the favourite CS Class 12 topics — now you'll never forget why it works. 🧠

💾 Save it · 📤 Share with your CS batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ComputerScience #BinarySearch #Python #CSClass12 #CBSE #Coding"""

VALS = [3, 8, 12, 15, 19, 23, 27, 31, 34, 38, 41, 45, 50, 56, 63, 70]
N = len(VALS)
TARGET = 41
BW, GAP = 0.86, 0.10


def box_x(i):
    return (i - (N - 1) / 2) * (BW + GAP)


def search_steps():
    lo, hi, out = 0, N - 1, []
    while lo <= hi:
        mid = (lo + hi) // 2
        out.append((lo, hi, mid))
        if VALS[mid] == TARGET:
            break
        if VALS[mid] < TARGET:
            lo = mid + 1
        else:
            hi = mid - 1
    return out


STEPS = search_steps()          # [(lo, hi, mid), ...]  → 4 steps for 16 items


BH = 3.0


def draw_box(dax, i, y, face, edge, txt_col, alpha, scale=1.0):
    w, h = BW * scale, BH * scale
    dax.add_patch(FancyBboxPatch((box_x(i) - w / 2, y - h / 2), w, h,
                                 boxstyle="round,pad=0,rounding_size=0.12", facecolor=face,
                                 edgecolor=edge, lw=2.5, alpha=alpha, zorder=5))
    dax.text(box_x(i), y, str(VALS[i]), ha="center", va="center", fontsize=25 * scale, rotation=0,
             fontweight="bold", color=txt_col, alpha=alpha, zorder=6)


def draw(c):
    dax = c.area(0.0, -0.3, 16.4)
    y0 = 1.2

    # which boxes are still "alive", and which one is being looked at
    alive = np.ones(N, bool)
    look, found = None, False
    if c.at("middle"):
        look = STEPS[0][2]
    if c.at("half"):
        hp = c.phase("half", 0.35, 0.75)
        lo, hi, mid = STEPS[0]
        if hp > 0:
            alive[:mid + 1] = False
    rep_n = 0
    if c.at("repeat"):
        rp = c.phase("repeat", 0.0, 0.85)
        sub = STEPS[1:]
        k = min(len(sub) - 1, int(rp * len(sub)))
        rep_n = k + 1
        for s in STEPS[:k + 1]:
            lo, hi, mid = s
            alive[:lo] = False; alive[hi + 1:] = False
        lo, hi, mid = sub[k]
        alive[:lo] = False; alive[hi + 1:] = False
        look = mid
        within = rp * len(sub) - k
        if within > 0.55 and VALS[mid] != TARGET:
            if VALS[mid] < TARGET:
                alive[:mid + 1] = False
            else:
                alive[mid:] = False
        found = VALS[mid] == TARGET and within > 0.4
        if rp >= 1:
            found = True

    # linear scan pointer
    lin_i, lin_count = None, 0
    if c.at("linear") and not c.at("middle"):
        lp = c.phase("linear", 0.05, 0.95)
        lin_i = min(N - 1, int(lp * N))
        lin_count = int(lp * 1000)

    for i in range(N):
        dead_a = 1.0
        y = y0
        if not alive[i]:
            # fall and fade
            dead_a = 0.18
            y = y0 - 1.0
        face, edge, txt = "#13264d", CYAN, WHITE
        if lin_i is not None and i <= lin_i:
            face, edge = ("#3b2a00", GOLD) if i == lin_i else ("#0d1a35", GREY)
        if look == i:
            face, edge, txt = (GREEN, GREEN, NAVY) if found else (GOLD, GOLD, NAVY)
        a = ease(c.phase("hook", 0.1 + i * 0.02, 0.4 + i * 0.02))
        draw_box(dax, i, y, face, edge, txt, a * dead_a)
        if a > 0.5 and not c.at("math"):
            dax.text(box_x(i), (y0 if alive[i] else y) - 1.95, str(i), ha="center", fontsize=17,
                     color=LTGREY, alpha=0.6 * a * dead_a, zorder=6)

    # captions over the row
    if lin_i is not None:
        outline(dax.text(box_x(lin_i), y0 + 1.85, "▼", ha="center", fontsize=30, color=GOLD, zorder=8))
        outline(dax.text(0, -2.3, f"tries: {lin_count}", ha="center", fontsize=50, fontweight="bold",
                         color=GOLD, zorder=8))
        outline(dax.text(0, -3.4, "one by one…", ha="center", fontsize=34,
                         color=LTGREY, zorder=8))
    if look is not None and not c.at("math"):
        outline(dax.text(box_x(look), y0 + 1.85, "middle" if not found else "found!", ha="center",
                         fontsize=32, fontweight="bold", color=GREEN if found else GOLD, zorder=8))
    if c.at("half") and not c.at("repeat"):
        hp = ease(c.phase("half", 0.0, 0.3))
        outline(dax.text(0, -3.4, f"looking for {TARGET}:  {VALS[STEPS[0][2]]} < {TARGET}", ha="center",
                         fontsize=44, fontweight="bold", color=WHITE, alpha=hp, zorder=8))
        cut = ease(c.phase("half", 0.35, 0.75))
        if cut > 0:
            outline(dax.text(lerp(box_x(0), box_x(STEPS[0][2]), 0.5), y0 - 3.6, "✗ left half gone",
                             ha="center", fontsize=34, fontweight="bold", color=PINK, alpha=cut, zorder=8))
    if c.at("middle"):
        steps_done = 1 + rep_n
        a = 1 - ease(c.phase("math", 0.0, 0.15))
        if a > 0 and c.at("half"):
            c.pill(0.5, 0.475, 0.50, 0.056, CYAN, alpha=a, dark="#04182b")
            c.text(0.5, 0.475, f"steps: {steps_done}  (not 16!)" if found else f"steps: {steps_done}",
                   size=32, color=CYAN, alpha=a)

    # the halving chain
    if c.at("math"):
        chain = [1000, 500, 250, 125, 63, 32, 16, 8, 4, 2, 1]
        n_show = int(ease(c.phase("math", 0.05, 0.45)) * len(chain) + 0.999)
        for k, v in enumerate(chain[:n_show]):
            x = -7.5 + k * 1.5
            outline(dax.text(x, -2.4, str(v), ha="center", fontsize=21, fontweight="bold",
                             color=GOLD if v == 1 else WHITE, zorder=8))
            if k < n_show - 1:
                dax.annotate("", xy=(x + 1.05, -3.1), xytext=(x + 0.45, -3.1), zorder=8,
                             arrowprops=dict(arrowstyle="-|>", color=CYAN, lw=2, mutation_scale=16))
                dax.text(x + 0.75, -3.75, "÷2", ha="center", fontsize=16, color=CYAN, zorder=8)
        c.steps([("1000 → 1  in  10 halvings", 0.40, WHITE),
                 (r"steps $\approx \log_{2} n$", 0.55, GOLD),
                 ("1,000,000 items  →  only 20 steps", 0.72, CYAN)])
