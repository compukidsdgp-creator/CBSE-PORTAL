"""WHY? — How does a dictionary find a key INSTANTLY?  (Class 12 Computer Science · Python dictionaries)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "How does a dictionary find keys INSTANTLY?"
TAGS = "Class 12 Computer Science"
BEATS = [
    ("hook",   "How does a Python dictionary find any key instantly, even among a million keys?",
               "How does a Python dictionary find ANY key instantly — even among a million?", 4.2),
    ("slow",   "Searching a list means checking the items one by one.",
               "Searching a list means checking items ONE BY ONE…", 3.6),
    ("hash",   "A dictionary is smarter. It uses a hash function, which turns the key into a number.",
               "A dictionary uses a HASH FUNCTION — it turns the key into a number.", 4.8),
    ("slot",   "That number tells Python exactly which slot to store it in.",
               "That number tells Python exactly which SLOT to use.", 3.6),
    ("lookup", "To find Riya later, hash it again. Same number, same slot. One step, no searching!",
               "To find 'Riya' later: hash it again → same number → same slot. ONE step!", 5.2),
    ("scale",  "That's why even with a million keys, a dictionary lookup takes about one step.",
               "Even with a million keys, a lookup takes about ONE step.", 4.4),
    ("math",   "In Python, marks square bracket Riya gives eighty eight, instantly.",
               "marks['Riya']  →  88   (instantly!)", 3.8),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🔑 WHY? — How does a Python dictionary find keys INSTANTLY?

A list: check items one by one 🐢
A dictionary: hash("Riya") → a number → that number picks the SLOT 🎯
Looking up again? Same hash → same slot → ONE step ⚡
Even with a million keys — about one step!

marks = {"Riya": 88}  →  marks["Riya"] → 88

CS Class 12 Python dictionaries — now you know the magic. 🧠

💾 Save it · 📤 Share with your CS batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Python #Dictionary #Hashing #ComputerScience #CSClass12 #CBSE"""

MONO = "DejaVu Sans Mono"
NAMES = [("Aman", 92), ("Riya", 88), ("Kabir", 75), ("Zoya", 81)]
NS = 8


def h(name):
    return sum(ord(ch) for ch in name) % NS


SLOTS = {h(n): (n, v) for n, v in NAMES}


def draw(c):
    dax = c.area(0.0, 0.0, 7.6)
    # 1) the slow way
    sa = ease(c.phase("slow", 0.0, 0.25)) * (1 - ease(c.phase("hash", 0.0, 0.2)))
    if sa > 0:
        names = ["Aman", "Kabir", "Zoya", "Dev", "Isha", "Riya"]
        p = c.phase("slow", 0.15, 0.95)
        cur = min(len(names) - 1, int(p * len(names)))
        for k, n in enumerate(names):
            x = -3.15 + k * 1.26
            col = GREEN if (k == cur and n == "Riya") else (GOLD if k == cur else (GREY if k < cur else CYAN))
            dax.add_patch(FancyBboxPatch((x - 0.58, 0.6), 1.16, 0.8, boxstyle="round,pad=0,rounding_size=0.12",
                                         facecolor="#13264d", edgecolor=col, lw=3, alpha=sa, zorder=5))
            dax.text(x, 1.0, n, ha="center", va="center", fontsize=20, fontweight="bold", color=WHITE, alpha=sa, zorder=6)
        outline(dax.text(-3.15 + cur * 1.26, 1.85, "▼", ha="center", fontsize=26, color=GOLD, alpha=sa, zorder=7))
        outline(dax.text(0, -0.4, f"checks: {cur + 1}", ha="center", fontsize=40, fontweight="bold", color=GOLD,
                         alpha=sa, zorder=7))
    # 2) hash table
    if c.at("hash"):
        ta = ease(c.phase("hash", 0.0, 0.3))
        sx, sy0, sh = 0.95, 2.0, 0.56
        for k in range(NS):
            y = sy0 - k * sh
            stored = None
            if k in SLOTS:
                n, v = SLOTS[k]
                idx = [nm for nm, _ in NAMES].index(n)
                show = c.phase("slot", 0.15 + idx * 0.15, 0.35 + idx * 0.15) > 0 if n != "Riya" else \
                    c.phase("slot", 0.1, 0.4) > 0
                if show:
                    stored = f'"{n}": {v}'
            hl = (k == h("Riya")) and (c.at("slot"))
            dax.add_patch(Rectangle((sx, y - sh / 2), 2.6, sh, facecolor="#1d3a6b" if hl else "#13264d",
                                    edgecolor=GREEN if hl and c.at("lookup") else (GOLD if hl else "#2b3f66"), lw=2.5 if hl else 1.5,
                                    alpha=ta, zorder=5))
            dax.text(sx - 0.2, y, str(k), ha="right", va="center", fontsize=20, color=LTGREY, family=MONO, alpha=ta,
                     zorder=6)
            if stored:
                dax.text(sx + 1.3, y, stored, ha="center", va="center", fontsize=19, fontweight="bold", color=WHITE,
                         family=MONO, alpha=ta, zorder=6)
        outline(dax.text(sx + 1.3, sy0 + 0.5, "slots", ha="center", fontsize=22, fontweight="bold", color=LTGREY,
                         alpha=ta, zorder=6))
        # hashing "Riya"
        key = "Riya"
        ka = ease(c.phase("hash", 0.25, 0.5))
        lk = c.at("lookup")
        dax.add_patch(FancyBboxPatch((-3.75, 0.9), 1.5, 0.8, boxstyle="round,pad=0,rounding_size=0.12", facecolor="#13264d",
                                     edgecolor=CYAN, lw=3, alpha=ka, zorder=5))
        dax.text(-3.0, 1.3, f'"{key}"', ha="center", va="center", fontsize=22, fontweight="bold", color=CYAN,
                 family=MONO, alpha=ka, zorder=6)
        fa = ease(c.phase("hash", 0.45, 0.7))
        dax.annotate("", xy=(-1.6, 1.3), xytext=(-2.2, 1.3), zorder=6,
                     arrowprops=dict(arrowstyle="-|>", color=WHITE, lw=3, alpha=fa, mutation_scale=24))
        dax.add_patch(FancyBboxPatch((-1.55, 0.85), 1.6, 0.9, boxstyle="round,pad=0,rounding_size=0.2", facecolor=PURPLE,
                                     edgecolor=WHITE, lw=2, alpha=fa, zorder=5))
        dax.text(-0.75, 1.3, "hash()", ha="center", va="center", fontsize=21, fontweight="bold", color=NAVY, family=MONO,
                 alpha=fa, zorder=6)
        na = back_out(c.phase("hash", 0.65, 0.9))
        if na > 0.01:
            outline(dax.text(-0.75, 0.25, f"→ {h(key)}", ha="center", va="center", fontsize=40 * min(1, na),
                             fontweight="bold", color=GOLD, zorder=7))
        pa = ease(c.phase("slot", 0.0, 0.4))
        if pa > 0:
            y = sy0 - h(key) * sh
            dax.annotate("", xy=(sx - 0.42, y), xytext=(-0.2, 0.2), zorder=7,
                         arrowprops=dict(arrowstyle="-|>", color=GREEN if lk else GOLD, lw=3.5, alpha=pa, mutation_scale=26,
                                         connectionstyle="arc3,rad=-0.2"))
        if lk:
            la = back_out(c.phase("lookup", 0.45, 0.7))
            if la > 0.01:
                c.pill(0.5, 0.385, 0.46 * min(1, la), 0.058, GREEN,
                       alpha=min(1, la) * (1 - ease(c.phase("scale", 0.0, 0.2))), dark="#06261a")
                c.text(0.5, 0.385, "found in 1 step!", size=38, color=GREEN,
                       alpha=min(1, la) * (1 - ease(c.phase("scale", 0.0, 0.2))))
    if c.at("scale"):
        sa2 = ease(c.phase("scale", 0.15, 0.45)) * (1 - ease(c.phase("math", 0.0, 0.2)))
        c.text(0.5, 0.385, "1,000,000 keys:  list ≈ 1,000,000 checks  •  dict ≈ 1", size=28, color=WHITE, alpha=sa2,
               max_w=0.94)
    if c.at("math"):
        rows = [('marks = {"Riya": 88, ...}', 0.05, LTGREY), ("marks['Riya']   # → 88", 0.35, GOLD)]
        for k, (s_, at, col) in enumerate(rows):
            a = ease(c.phase("math", at, at + 0.25))
            if a > 0:
                c.ax.text(0.5, 0.355 - k * 0.055, s_, ha="center", va="center", fontsize=32, color=col, family=MONO,
                          fontweight="bold", alpha=a, zorder=10, transform=c.ax.transAxes)
