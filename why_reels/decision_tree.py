"""WHY? — How does an AI DECISION TREE decide?  (AI · Modelling, Class 10 & 12)"""
from matplotlib.patches import FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "How does an AI DECISION TREE decide?"
TAGS = "AI · Modelling"
BEATS = [
    ("hook",     "How does a decision tree in A I make a choice? Like a game of twenty questions.",
                 "How does an AI decision tree make a choice? Like a game of 20 questions!", 4.0),
    ("question", "It asks one yes or no question at a time. First: is it raining?",
                 "It asks ONE yes/no question at a time. First: is it raining?", 4.0),
    ("branch",   "If yes, stay indoors. If no, ask another question. Is the homework done?",
                 "Yes → stay indoors. No → ask another: is the homework done?", 4.6),
    ("leaves",   "Every path ends in a final decision, called a leaf.",
                 "Every path ends in a final decision — a LEAF.", 3.4),
    ("example",  "Today it's sunny, and the homework is done. Follow the path. No, then yes. Play cricket!",
                 "Today: sunny ☀ and homework done ✓ → follow the path: No → Yes → PLAY CRICKET!", 5.4),
    ("learn",    "The A I builds this tree from data, picking the questions that split the examples best.",
                 "The AI builds the tree from DATA, picking the questions that split examples best.", 5.0),
    ("end",      "Follow C B S E Mock for more why videos.",
                 "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🌳 WHY? — How does an AI DECISION TREE decide?

Like a game of 20 questions — one yes/no question at a time:
❓ Raining? → Yes → stay indoors
❓ No → Homework done? → Yes → PLAY CRICKET 🏏 / No → study first 📚
Every path ends in a LEAF (the decision).

The AI builds the tree from data, choosing the questions that split the examples best.
AI modelling — Class 10 & 12. 🧠

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ArtificialIntelligence #DecisionTree #MachineLearning #AIClass10 #AIClass12 #CBSE"""

NODES = {
    "root": (0.2, 2.35, "Raining?", CYAN, False),
    "stay": (-1.95, 0.35, "Stay indoors", PURPLE, True),
    "hw":   (1.65, 0.35, "Homework done?", CYAN, False),
    "play": (0.45, -1.7, "Play cricket!", GREEN, True),
    "study": (2.85, -1.7, "Study first", GOLD, True),
}
EDGES = [("root", "stay", "Yes"), ("root", "hw", "No"), ("hw", "play", "Yes"), ("hw", "study", "No")]
PATH = {("root", "hw"), ("hw", "play")}
END_Y = 0.398


def box(dax, key, a, glow=False):
    x, y, lab, col, leaf = NODES[key]
    w = 2.35 if not leaf else 2.15
    dax.add_patch(FancyBboxPatch((x - w / 2, y - 0.45), w, 0.9,
                                 boxstyle=f"round,pad=0,rounding_size={0.42 if leaf else 0.12}",
                                 facecolor=col if glow else "#13264d", edgecolor=col, lw=3.5 if glow else 2.8,
                                 alpha=a, zorder=6))
    dax.text(x, y, lab, ha="center", va="center", fontsize=25, fontweight="bold", color=NAVY if glow else WHITE,
             alpha=a, zorder=7)


def draw(c):
    dax = c.area(0.45, 0.1, 7.3)
    show = {"root": c.phase("question", 0.05, 0.3),
            "stay": c.phase("branch", 0.05, 0.3), "hw": c.phase("branch", 0.35, 0.6),
            "play": c.phase("leaves", 0.05, 0.35), "study": c.phase("leaves", 0.25, 0.55)}
    ex = c.at("example")
    step = c.phase("example", 0.25, 0.85)
    lit = set()
    if ex:
        lit.add("root")
        if step > 0.3:
            lit.add("hw")
        if step > 0.75:
            lit.add("play")
    # edges
    for a_, b_, lab in EDGES:
        ea = ease(show[b_])
        if ea <= 0:
            continue
        x1, y1 = NODES[a_][:2]; x2, y2 = NODES[b_][:2]
        on = ex and (a_, b_) in PATH and ((a_ == "root" and step > 0.3) or (a_ == "hw" and step > 0.75))
        dim = ex and not on
        dax.plot([x1, lerp(x1, x2, ea)], [y1 - 0.45, lerp(y1 - 0.45, y2 + 0.45, ea)],
                 color=GREEN if on else LTGREY, lw=5 if on else 2.8, alpha=0.35 if dim else 1.0, zorder=3)
        if ea > 0.6:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            outline(dax.text(mx + (-0.35 if x2 < x1 else 0.35), my, lab, ha="center", va="center", fontsize=22,
                             fontweight="bold", color=GREEN if on else (PINK if lab == "Yes" else GOLD),
                             alpha=0.4 if dim else 1.0, zorder=8))
    for k in NODES:
        a = ease(show[k])
        if a > 0:
            box(dax, k, a * (0.45 if ex and k not in lit and k != "root" else 1.0), glow=k in lit)
    if c.phase("leaves", 0.5, 0.8) > 0 and not ex:
        la = ease(c.phase("leaves", 0.5, 0.8))
        outline(dax.text(-1.25, -1.7, "leaves →", ha="center", va="center", fontsize=24, fontweight="bold",
                         color=LTGREY, alpha=la, zorder=8))
    if ex:
        ea = ease(c.phase("example", 0.0, 0.2))
        outline(dax.text(-1.85, -1.75, "today:\nsunny ☀\nhomework ✓", ha="center", va="center", fontsize=23,
                         fontweight="bold", color=GOLD, alpha=ea * (1 - ease(c.phase("learn", 0.0, 0.2))), zorder=8))
        ra = back_out(c.phase("example", 0.8, 0.95)) * (1 - ease(c.phase("learn", 0.0, 0.2)))
        if ra > 0.01:
            c.pill(0.5, 0.385, 0.66 * min(1, ra), 0.058, GREEN, alpha=min(1, ra), dark="#06261a")
            c.text(0.5, 0.385, "decision: PLAY CRICKET!", size=34, color=GREEN, alpha=min(1, ra))
    c.steps([("root → questions → leaves", 0.1, CYAN),
             ("learns the best questions from data", 0.4, GOLD)], ys=(0.345, 0.285), beat="learn")
