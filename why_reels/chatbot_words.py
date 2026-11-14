"""WHY? — How does a chatbot understand WORDS?  (AI · Natural Language Processing, Class 10 & 12)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "How does a chatbot understand WORDS?"
TAGS = "AI · NLP"
BEATS = [
    ("hook",    "How can a chatbot understand words, when computers only understand numbers?",
                "How can a chatbot understand WORDS when computers only understand NUMBERS?", 4.0),
    ("numbers", "First, every word is turned into a list of numbers, called an embedding.",
                "First, every word becomes a list of numbers — an EMBEDDING.", 4.0),
    ("map",     "Picture those numbers as points on a map. Words with similar meanings land close together.",
                "Picture them as points on a map: similar meanings land CLOSE together.", 5.0),
    ("arith",   "Even directions carry meaning. King, minus man, plus woman, lands right next to queen.",
                "Directions carry meaning: king − man + woman ≈ queen!", 5.2),
    ("predict", "When you type, the chatbot reads these numbers, spots patterns, and predicts the most likely next word.",
                "When you type, it reads the numbers, spots patterns and PREDICTS the next word.", 5.6),
    ("math",    "Words become numbers. Similar meanings sit close. Patterns predict the next word.",
                "Words → numbers · similar meanings sit close · patterns predict the next word", 4.6),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """💬 WHY? — How does a chatbot understand WORDS?

Computers only understand numbers 🔢
1️⃣ Every word becomes a list of numbers — an EMBEDDING
2️⃣ On this "meaning map", similar words sit close together (apple 🍎 near mango 🥭)
3️⃣ Directions carry meaning: king − man + woman ≈ queen 👑
4️⃣ The chatbot spots patterns and PREDICTS the most likely next word

Natural Language Processing (NLP) — AI syllabus, Class 10 & 12. 🧠

💾 Save it · 📤 Share with your AI batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ArtificialIntelligence #NLP #Chatbot #AIClass10 #AIClass12 #CBSE"""

WORDS = {
    "apple": (-2.6, 1.7, GREEN), "mango": (-2.0, 2.15, GREEN), "banana": (-2.9, 2.45, GREEN),
    "dog": (2.1, 1.9, CYAN), "cat": (2.7, 2.3, CYAN), "cow": (2.4, 1.4, CYAN),
    "exam": (-2.4, -1.0, GOLD), "marks": (-1.7, -1.5, GOLD), "teacher": (-2.9, -1.7, GOLD),
    "man": (0.6, -0.2, PURPLE), "woman": (1.7, -0.75, PURPLE), "king": (0.95, 0.75, PINK), "queen": (2.05, 0.2, PINK),
}


def draw(c):
    dax = c.area(0.0, 0.45, 7.6)
    # 1) words become numbers
    na = ease(c.phase("numbers", 0.0, 0.3)) * (1 - ease(c.phase("map", 0.0, 0.3)))
    if na > 0:
        rows = [("king", "[0.82, 0.31, −0.44, 0.67 …]", PINK), ("mango", "[−0.15, 0.93, 0.28, −0.51 …]", GREEN),
                ("exam", "[0.47, −0.62, 0.89, 0.12 …]", GOLD)]
        for k, (w, v, col) in enumerate(rows):
            a = ease(c.phase("numbers", 0.15 + k * 0.2, 0.35 + k * 0.2)) * na / max(na, 1e-6) * na
            y = 1.6 - k * 1.3
            dax.add_patch(FancyBboxPatch((-3.6, y - 0.38), 1.9, 0.76, boxstyle="round,pad=0,rounding_size=0.15",
                                         facecolor="#13264d", edgecolor=col, lw=2.5, alpha=a, zorder=5))
            dax.text(-2.65, y, w, ha="center", va="center", fontsize=26, fontweight="bold", color=col, alpha=a, zorder=6)
            dax.annotate("", xy=(-1.15, y), xytext=(-1.6, y), zorder=6,
                         arrowprops=dict(arrowstyle="-|>", color=WHITE, lw=2.5, alpha=a, mutation_scale=22))
            dax.text(-1.05, y, v, ha="left", va="center", fontsize=19, color=WHITE, family="DejaVu Sans Mono",
                     fontweight="bold", alpha=a, zorder=6)
    # 2) the meaning map
    mp = ease(c.phase("map", 0.15, 0.6))
    pr_fade = 1 - ease(c.phase("predict", 0.0, 0.25))
    if mp > 0 and pr_fade > 0:
        a0 = mp * pr_fade
        for gx in np.linspace(-3.6, 3.6, 9):
            dax.plot([gx, gx], [-2.3, 2.9], color="#1b2b4f", lw=1, alpha=a0, zorder=1)
        for gy in np.linspace(-2.3, 2.9, 7):
            dax.plot([-3.6, 3.6], [gy, gy], color="#1b2b4f", lw=1, alpha=a0, zorder=1)
        for k, (w, (x, y, col)) in enumerate(WORDS.items()):
            a = ease(c.phase("map", 0.15 + k * 0.04, 0.35 + k * 0.04)) * pr_fade
            if w in ("man", "woman", "king", "queen") and not c.at("arith"):
                a *= 0.35
            dax.add_patch(Circle((x, y), 0.1, color=col, alpha=a, zorder=5))
            outline(dax.text(x + 0.15, y + 0.15, w, ha="left", va="bottom", fontsize=22, fontweight="bold",
                             color=col, alpha=a, zorder=6))
        for (lab, x, y, col) in [("fruits", -2.5, 2.95, GREEN), ("animals", 2.4, 2.95, CYAN), ("school", -2.4, -2.2, GOLD)]:
            la = ease(c.phase("map", 0.6, 0.85)) * pr_fade
            outline(dax.text(x, y, lab, ha="center", fontsize=20, color=col, alpha=la * 0.8, zorder=6))
    # 3) king - man + woman ≈ queen
    if c.at("arith") and pr_fade > 0:
        ar = c.phase("arith", 0.1, 0.9)
        km = WORDS["king"]; mn = WORDS["man"]; wm = WORDS["woman"]; qn = WORDS["queen"]
        a1 = ease(ar * 2)
        dax.annotate("", xy=(wm[0], wm[1]), xytext=(mn[0], mn[1]), zorder=7,
                     arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=3.5, alpha=a1 * pr_fade, mutation_scale=24))
        a2 = ease(ar * 2 - 0.8)
        if a2 > 0:
            dax.annotate("", xy=(qn[0], qn[1]), xytext=(km[0], km[1]), zorder=7,
                         arrowprops=dict(arrowstyle="-|>", color=PINK, lw=3.5, alpha=a2 * pr_fade, mutation_scale=24))
            outline(dax.text(1.55, 1.15, "same direction!", ha="left", fontsize=20, fontweight="bold", color=PINK,
                             alpha=a2 * pr_fade, zorder=8))
        ea = ease(c.phase("arith", 0.55, 0.85)) * pr_fade
        if ea > 0:
            c.text(0.5, 0.385, "king − man + woman ≈ queen", size=40, color=PINK, alpha=ea)
    # 4) predict the next word
    if c.at("predict"):
        pa = ease(c.phase("predict", 0.15, 0.4)) * (1 - ease(c.phase("math", 0.0, 0.25)))
        dax.add_patch(FancyBboxPatch((-3.5, 1.5), 7.0, 1.0, boxstyle="round,pad=0,rounding_size=0.25",
                                     facecolor="#13264d", edgecolor=CYAN, lw=3, alpha=pa, zorder=5))
        dax.text(-3.2, 2.0, "The exam was really  ___", ha="left", va="center", fontsize=30, fontweight="bold",
                 color=WHITE, alpha=pa, zorder=6)
        opts = [("easy", 0.48, GREEN), ("tough", 0.31, GOLD), ("long", 0.14, CYAN), ("purple", 0.01, GREY)]
        for k, (w, p, col) in enumerate(opts):
            a = ease(c.phase("predict", 0.35 + k * 0.1, 0.55 + k * 0.1)) * (1 - ease(c.phase("math", 0.0, 0.25)))
            y = 0.6 - k * 0.78
            dax.text(-3.2, y, w, ha="left", va="center", fontsize=26, fontweight="bold", color=col, alpha=a, zorder=6)
            dax.add_patch(FancyBboxPatch((-1.4, y - 0.22), 4.4 * p / 0.48 * ease(min(1, a * 1.3)), 0.44,
                                         boxstyle="round,pad=0,rounding_size=0.1", facecolor=col, edgecolor="none",
                                         alpha=a, zorder=5))
            dax.text(-1.4 + 4.4 * p / 0.48 + 0.15, y, f"{int(p * 100)}%", ha="left", va="center", fontsize=22,
                     fontweight="bold", color=col, alpha=a, zorder=6)
    c.steps([("words → numbers (embeddings)", 0.0, WHITE), ("similar meaning → close together", 0.25, CYAN),
             ("patterns → predict the next word", 0.5, GOLD)], ys=(0.360, 0.305, 0.245))
