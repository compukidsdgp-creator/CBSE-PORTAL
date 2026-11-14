"""WHY? — Why does AI need SO MUCH data?  (AI · Data & Learning, Class 10 & 12)"""
import math
import numpy as np
from matplotlib.patches import Circle, Polygon, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does AI need SO MUCH data?"
TAGS = "AI · Data"
BEATS = [
    ("hook",  "Why does A I need thousands, even millions of examples, when a child learns from just a few?",
              "Why does AI need thousands of examples when a child learns from just a few?", 4.6),
    ("few",   "Show an A I only three cat photos, all orange. It learns that a cat is an orange blob.",
              "Show an AI only 3 cat photos — all orange. It learns: cat = orange blob.", 5.0),
    ("fail",  "Now show it a black cat. It has no idea.",
              "Now show it a BLACK cat… no idea!", 3.2),
    ("more",  "Give it thousands of examples. Every colour, every size, every angle.",
              "Give it THOUSANDS of examples — every colour, size and angle.", 4.4),
    ("learn", "Now it learns what really makes a cat. Ears, eyes, whiskers. Not just colour.",
              "Now it learns what REALLY makes a cat: ears, eyes, whiskers — not colour.", 4.8),
    ("curve", "More good data usually means better accuracy, until it slowly levels off.",
              "More good data → better accuracy (until it levels off).", 4.4),
    ("math",  "Few examples, it memorises. Many varied examples, it generalises.",
              "Few examples → it memorises. Many varied examples → it generalises.", 4.2),
    ("end",   "Follow C B S E Mock for more why videos.",
              "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🐱 WHY? — Why does AI need SO MUCH data?

Show an AI only 3 orange cats → it learns "cat = orange blob" 🟠
Show it a black cat → ❓ no idea!
Give it thousands of varied examples → it learns what REALLY makes a cat: ears, eyes, whiskers 👂👀
More good data → better accuracy (until it levels off) 📈

Few examples → memorise. Many varied examples → generalise.
AI syllabus (data & learning), Class 10 & 12. 🧠

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ArtificialIntelligence #MachineLearning #Data #AIClass10 #AIClass12 #CBSE"""

CATS = ["#ff9f43", "#2b2b2b", "#e8e8e8", "#8a6a4f", "#c9c9c9", "#ffcf8a", "#5b5b5b", "#d98c4a"]


def cat(dax, x, y, s, col, a, rot=0.0, z=6, feat=0.0):
    """Simple cat face: head, ears, eyes, whiskers."""
    cr, sr = math.cos(rot), math.sin(rot)
    P = lambda px, py: (x + s * (px * cr - py * sr), y + s * (px * sr + py * cr))
    edge = GOLD if feat > 0.5 else NAVY
    for sx in (-1, 1):
        dax.add_patch(Polygon([P(sx * 0.62, 0.45), P(sx * 0.95, 1.05), P(sx * 0.2, 0.78)], closed=True, facecolor=col,
                              edgecolor=edge, lw=1.5 + 2 * feat, alpha=a, zorder=z))
    dax.add_patch(Circle(P(0, 0), s * 0.85, facecolor=col, edgecolor=NAVY, lw=1.5, alpha=a, zorder=z))
    eye = "#3ddc97" if col != "#e8e8e8" else "#2a6fdb"
    for sx in (-1, 1):
        dax.add_patch(Circle(P(sx * 0.32, 0.12), s * 0.13, facecolor=eye, edgecolor=GOLD if feat > 0.5 else "none",
                             lw=2 * feat, alpha=a, zorder=z + 1))
    dax.add_patch(Polygon([P(-0.1, -0.12), P(0.1, -0.12), P(0, -0.25)], closed=True, facecolor=PINK, edgecolor="none",
                          alpha=a, zorder=z + 1))
    wc = GOLD if feat > 0.5 else LTGREY
    for sx in (-1, 1):
        for dy in (-0.18, -0.3):
            p0, p1 = P(sx * 0.2, dy), P(sx * 1.05, dy + 0.05 * (1 if dy > -0.25 else -1))
            dax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=wc, lw=1.2 + 1.5 * feat, alpha=a, zorder=z + 1)


def draw(c):
    dax = c.area(0.0, 0.0, 7.2)
    # 1) three orange cats
    fa = 1 - ease(c.phase("more", 0.0, 0.25))
    if c.at("few") and fa > 0:
        for k in range(3):
            a = ease(c.phase("few", 0.1 + k * 0.12, 0.3 + k * 0.12)) * fa
            cat(dax, -2.4 + k * 1.6, 1.35, 0.55, "#ff9f43", a)
        ra = ease(c.phase("few", 0.55, 0.85)) * fa
        if ra > 0:
            c.pill(0.5, 0.385, 0.52, 0.056, GOLD, alpha=ra, dark="#2a2000")
            c.text(0.5, 0.385, 'AI rule: "cat = orange"', size=34, color=GOLD, alpha=ra)
    if c.at("fail") and fa > 0:
        a = ease(c.phase("fail", 0.0, 0.3)) * fa
        cat(dax, 0.0, -0.9, 0.75, "#2b2b2b", a, rot=0.25)
        q = back_out(c.phase("fail", 0.3, 0.6))
        if q > 0:
            outline(dax.text(1.25, -0.6, "not orange…\nnot a cat? ✗", ha="left", va="center", fontsize=26 * min(1, q),
                             fontweight="bold", color=PINK, alpha=fa, zorder=9))
    # 2) thousands of varied examples
    if c.at("more"):
        ma = ease(c.phase("more", 0.1, 0.6)) * (1 - ease(c.phase("curve", 0.0, 0.25)))
        rng = np.random.default_rng(4)
        feat = ease(c.phase("learn", 0.2, 0.5))
        for k in range(40):
            r, q = divmod(k, 8)
            x, y = -2.8 + q * 0.8 + rng.uniform(-0.1, 0.1), 1.9 - r * 0.85 + rng.uniform(-0.08, 0.08)
            a = ease(c.phase("more", 0.1 + k * 0.012, 0.3 + k * 0.012)) * ma / max(ma, 1e-6) * ma
            cat(dax, x, y, rng.uniform(0.22, 0.3), CATS[k % len(CATS)], a, rot=rng.uniform(-0.6, 0.6), feat=feat)
        if c.at("learn"):
            la = ease(c.phase("learn", 0.3, 0.6)) * (1 - ease(c.phase("curve", 0.0, 0.25)))
            c.text(0.5, 0.385, "learns: ears ✓  eyes ✓  whiskers ✓", size=34, color=GOLD, alpha=la)
    # 3) accuracy vs data
    if c.at("curve"):
        ca = ease(c.phase("curve", 0.1, 0.4))
        dax.plot([-3.0, 3.0], [-1.45, -1.45], color=GREY, lw=2.5, alpha=ca, zorder=3)
        dax.plot([-3.0, -3.0], [-1.45, 2.2], color=GREY, lw=2.5, alpha=ca, zorder=3)
        p = c.phase("curve", 0.2, 0.9)
        xs = np.linspace(-3.0, lerp(-3.0, 3.0, p), 200)
        ys = -1.3 + 3.3 * (1 - np.exp(-(xs + 3.0) / 1.3))
        dax.plot(xs, ys, color=GREEN, lw=5, alpha=ca, zorder=4)
        outline(dax.text(0, -1.95, "amount of data →", ha="center", fontsize=24, fontweight="bold", color=LTGREY,
                         alpha=ca, zorder=5))
        outline(dax.text(-3.2, 0.25, "accuracy →", ha="center", va="center", rotation=90, fontsize=24, fontweight="bold",
                         color=LTGREY, alpha=ca, zorder=5))
        if p > 0.8:
            outline(dax.text(2.2, 2.2, "levels off", ha="center", fontsize=22, fontweight="bold", color=GOLD,
                             alpha=ease((p - 0.8) / 0.2), zorder=5))
    c.steps([("few examples → memorises", 0.0, PINK),
             ("many varied examples → generalises", 0.35, GOLD)], ys=(0.345, 0.285))
