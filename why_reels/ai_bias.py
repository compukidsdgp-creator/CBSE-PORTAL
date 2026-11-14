"""WHY? — Why can AI be BIASED?  (AI · Ethics, Class 10 & 12)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why can AI be BIASED?"
TAGS = "AI · Ethics"
BEATS = [
    ("hook",    "Can a computer be unfair? A I can be, and the reason might surprise you.",
                "Can a computer be unfair? AI can be — and the reason might surprise you.", 4.0),
    ("learn",   "An A I learns only from the examples we give it. Nothing else.",
                "An AI learns ONLY from the examples we give it. Nothing else.", 3.8),
    ("data",    "Imagine a hiring A I, trained on old records where almost everyone hired came from Group A.",
                "Imagine a hiring AI trained on old records where almost everyone hired was from Group A.", 5.2),
    ("pattern", "The A I spots the pattern, and quietly learns: Group A means good.",
                "The AI spots the pattern and quietly learns: Group A = good.", 4.2),
    ("unfair",  "Now a brilliant candidate from Group B applies, with top marks, and gets rejected. "
                "The A I simply copied the bias in its data.",
                "A brilliant Group B candidate with top marks applies… REJECTED. The AI copied the bias in its data.", 6.4),
    ("fix",     "The fix? Balanced data, testing for fairness, and humans checking important decisions.",
                "The fix: balanced data, fairness testing, and humans checking important decisions.", 5.4),
    ("math",    "Remember. Biased data in, biased decisions out. Fair A I needs fair data.",
                "Biased data in → biased decisions out. Fair AI needs fair data.", 4.4),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """⚖️ WHY? — Why can AI be BIASED?

An AI learns ONLY from the examples we give it.
Train a hiring AI on old records where almost everyone hired was from one group…
→ it learns "that group = good" → a brilliant candidate from another group gets rejected ❌

The fix ✅ balanced data · fairness testing · humans checking important decisions

Biased data in → biased decisions out. A key AI Ethics topic for Class 10 & 12. 🧠

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ArtificialIntelligence #AIEthics #AIBias #AIClass10 #AIClass12 #CBSE"""

COLS, ROWS = 4, 5
B_OLD = {7, 16}                                     # the only Group B people in the old data
B_NEW = {k for k in range(COLS * ROWS) if (k + k // COLS) % 2}   # balanced data
MX, MY = 2.35, 0.35
END_Y = 0.393                                 # the AI model box


def person(dax, x, y, col, alpha, s=1.0, z=6):
    dax.add_patch(Circle((x, y + 0.24 * s), 0.15 * s, color=col, alpha=alpha, zorder=z))
    dax.add_patch(FancyBboxPatch((x - 0.21 * s, y - 0.24 * s), 0.42 * s, 0.36 * s,
                                 boxstyle=f"round,pad=0,rounding_size={0.15 * s}", facecolor=col,
                                 edgecolor="none", alpha=alpha, zorder=z))


def grid_xy(k):
    r, cc = divmod(k, COLS)
    return -4.0 + cc * 0.78, 2.0 - r * 0.92


def draw(c):
    dax = c.area(-0.1, -0.15, 8.7)

    # the AI model box
    ma = ease(c.phase("hook", 0.3, 0.8))
    dax.add_patch(FancyBboxPatch((MX - 1.45, MY - 1.15), 2.9, 2.3, boxstyle="round,pad=0,rounding_size=0.3",
                                 facecolor="#13264d", edgecolor=CYAN, lw=3.5, alpha=ma, zorder=4))
    dax.text(MX, MY + 0.55, "AI model", ha="center", va="center", fontsize=28, fontweight="bold",
             color=WHITE, alpha=ma, zorder=5)

    # learning stream: example cards fly into the model
    la = c.phase("learn", 0.1, 1.0) * (1 - ease(c.phase("data", 0.0, 0.2)))
    if la > 0:
        for q in range(6):
            f = (la * 1.6 + q / 6) % 1
            x, y = lerp(-4.3, MX - 1.2, f), MY + 0.3 * np.sin(f * 6 + q)
            person(dax, x, y, CYAN if q % 3 else PURPLE, min(1, la * 3) * (1 - f * 0.4), 0.9)
        outline(dax.text(-2.0, -1.6, "examples (data)", ha="center", fontsize=26, fontweight="bold",
                         color=LTGREY, alpha=min(1, la * 3), zorder=7))

    # the old hiring records
    ga = ease(c.phase("data", 0.15, 0.5))
    if ga > 0:
        balance = ease(c.phase("fix", 0.1, 0.6))
        dim = 1 - 0.65 * ease(c.phase("unfair", 0.0, 0.2)) * (1 - balance)
        for k in range(COLS * ROWS):
            x, y = grid_xy(k)
            appear = ease((ga * (COLS * ROWS + 3) - k) / 3)
            b_old, b_new = k in B_OLD, k in B_NEW
            col = PURPLE if (b_new if balance > 0.5 else b_old) else CYAN
            person(dax, x, y, col, appear * dim, 0.95)
        title = "past hires" if balance < 0.5 else "balanced data"
        outline(dax.text(-2.83, 2.75, title, ha="center", fontsize=26, fontweight="bold",
                         color=GREEN if balance >= 0.5 else LTGREY, alpha=ga, zorder=7))
        for k, (lab, col) in enumerate([("Group A", CYAN), ("Group B", PURPLE)]):
            person(dax, -4.0 + k * 1.95, -2.55, col, ga, 0.7)
            dax.text(-3.72 + k * 1.95, -2.55, lab, ha="left", va="center", fontsize=21, fontweight="bold",
                     color=col, alpha=ga, zorder=7)

    # what the model learnt
    pa = ease(c.phase("pattern", 0.15, 0.5)) * (1 - ease(c.phase("fix", 0.2, 0.45)))
    if pa > 0:
        dax.annotate("", xy=(MX - 1.5, MY), xytext=(-1.35, MY), zorder=6,
                     arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=4, alpha=pa, mutation_scale=30))
        dax.text(MX, MY - 0.15, "Group A → ✓", ha="center", va="center", fontsize=24, fontweight="bold",
                 color=CYAN, alpha=pa, zorder=6)
        dax.text(MX, MY - 0.65, "Group B → ✗", ha="center", va="center", fontsize=24, fontweight="bold",
                 color=PINK, alpha=pa, zorder=6)
    fa = ease(c.phase("fix", 0.35, 0.6))
    if fa > 0:
        dax.text(MX, MY - 0.4, "skills → ✓", ha="center", va="center", fontsize=26, fontweight="bold",
                 color=GREEN, alpha=fa, zorder=6)

    # the brilliant Group B candidate
    ua = c.phase("unfair", 0.05, 1.0)
    if ua > 0:
        mv = ease(c.phase("unfair", 0.1, 0.45))
        x, y = lerp(-1.0, MX, mv), -1.98
        person(dax, x, y, PURPLE, 1.0, 1.5, z=9)
        outline(dax.text(x, y + 0.78, "★ top marks", ha="center", fontsize=22, fontweight="bold",
                         color=GOLD, zorder=10))
        ra = back_out(c.phase("unfair", 0.45, 0.6)) * (1 - ease(c.phase("math", 0.0, 0.25)))
        if ra > 0.01:
            hired = c.phase("fix", 0.5, 0.7) > 0
            col, txt = (GREEN, "HIRED ✓") if hired else (PINK, "REJECTED ✗")
            bw = 2.6 * min(1, ra)
            dax.add_patch(FancyBboxPatch((MX - bw / 2, -3.5), bw, 0.72, clip_on=False,
                                         boxstyle="round,pad=0,rounding_size=0.15", facecolor="#0e1d3f",
                                         edgecolor=col, lw=3, alpha=min(1, ra), zorder=10))
            dax.text(MX, -3.14, txt, ha="center", va="center", fontsize=24, fontweight="bold",
                     color=col, alpha=min(1, ra), zorder=11)
        ca = ease(c.phase("unfair", 0.7, 0.9)) * (1 - ease(c.phase("fix", 0.0, 0.2)))
        if ca > 0:
            outline(dax.text(MX, 2.15, "copied the bias!", ha="center", fontsize=30, fontweight="bold",
                             color=PINK, alpha=ca, zorder=10))

    # the fix checklist
    if c.at("fix"):
        for k, s in enumerate(["✓ balanced data", "✓ fairness testing", "✓ human review"]):
            a = ease(c.phase("fix", 0.15 + k * 0.2, 0.35 + k * 0.2)) * (1 - ease(c.phase("math", 0.0, 0.2)))
            if a > 0:
                c.text(0.5, 0.352 - k * 0.052, s, size=34, color=GREEN, alpha=a)
    c.steps([("Biased data in → biased decisions out", 0.05, WHITE),
             ("Fair AI needs fair data", 0.40, GOLD)], ys=(0.335, 0.275))
