"""WHY? — Why does the sperm decide boy or girl?  (Class 10 Science · Heredity · Sex determination)"""
import math
from fractions import Fraction
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does the SPERM decide boy or girl?"
TAGS = "Class 10 Science"
PLAN_RANK = 4

# ── the biology, computed (NCERT Class 10, Heredity: sex determination in human beings) ──
PAIRS = 23                       # chromosome pairs in a human body cell
SEX_PAIRS = 1
AUTOSOME_PAIRS = PAIRS - SEX_PAIRS            # 22
MOTHER, FATHER = ("X", "X"), ("X", "Y")
EGGS, SPERMS = sorted(set(MOTHER)), sorted(set(FATHER))       # ['X'] and ['X', 'Y']
CHILDREN = ["".join(sorted(m + f)) for m in MOTHER for f in FATHER]   # each gamete equally likely
P_GIRL = Fraction(CHILDREN.count("XX"), len(CHILDREN))
P_BOY = Fraction(CHILDREN.count("XY"), len(CHILDREN))
assert AUTOSOME_PAIRS == 22 and EGGS == ["X"] and SPERMS == ["X", "Y"] and P_GIRL == P_BOY == Fraction(1, 2)
PCT = f"{int(P_GIRL * 100)}%"                 # "50%"

BEATS = [
    ("hook",   "Boy or girl? Why does the sperm decide it, and not the egg?",
               "Boy or girl? Why does the SPERM decide it, not the egg?", 3.6),
    ("pairs",  "We have twenty three chromosome pairs. Twenty two are alike in boys and girls.",
               f"We have {PAIRS} chromosome pairs. {AUTOSOME_PAIRS} are alike in boys & girls.", 4.2),
    ("sexpair", "One pair decides sex. Women are X X. Men are X Y. Y is shorter.",
               "ONE pair decides sex. Women: XX. Men: XY (Y is shorter).", 4.2),
    ("egg",    "An egg gets one of the pair. Mothers have only X, so every egg has X.",
               "A gamete gets ONE of the pair. Mother has only X → every egg has X.", 4.2),
    ("sperm",  "Fathers have X and Y. So half the sperm carry X, half carry Y.",
               "Father has X and Y → half the sperm carry X, half carry Y.", 3.8),
    ("cross",  "X sperm plus X egg gives a girl. Y sperm plus X egg gives a boy.",
               "X sperm + X egg = XX → girl.   Y sperm + X egg = XY → boy.", 4.4),
    ("chance", "Which sperm wins is pure chance, about fifty fifty. Nobody chooses it.",
               f"Which sperm wins is pure CHANCE — about {PCT} each. Nobody chooses it.", 4.2),
    ("math",   "The egg always gives X. The sperm's X or Y decides.",
               "Egg always gives X. The sperm's X or Y decides boy or girl.", 3.8),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
END_Y = 0.395
CAPTION = f"""🧬 WHY? — Why does the SPERM decide whether a baby is a boy or a girl?

Human cells: {PAIRS} pairs of chromosomes — {AUTOSOME_PAIRS} pairs are the same in boys & girls.
Just ONE pair decides sex: women XX, men XY (Y is shorter).

🥚 Every egg carries an X (mother has only X to give)
🔬 Sperm are of two kinds: half carry X, half carry Y
X + X = XX → girl 👧 · X + Y = XY → boy 👦
Which sperm reaches the egg is pure chance — about {PCT} each.

Heredity (sex determination) — Class 10 Science. 📘 A favourite board question!

💾 Save it · 📤 Share with your bio group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Heredity #SexDetermination #Chromosomes #Class10Science #CBSE #BoardExams"""

XC, YC = CYAN, GOLD          # X chromosome / Y chromosome colours
MX, FX = -2.0, 2.0           # mother / father x positions
PY = 1.75                    # parents row
GY = 0.05                    # gametes row
CY = -1.55                   # children row


def xchrom(dax, x, y, s, a, z=8, col=XC):
    """X chromosome: two long crossed arms."""
    for d in (-1, 1):
        t = math.radians(d * 22)
        dx, dy = 0.30 * s * math.sin(t), 0.30 * s * math.cos(t)
        dax.plot([x - dx, x + dx], [y - dy, y + dy], color=col, lw=9 * s, alpha=a, solid_capstyle="round", zorder=z)


def ychrom(dax, x, y, s, a, z=8, col=YC):
    """Y chromosome: visibly shorter."""
    dax.plot([x, x], [y - 0.17 * s, y + 0.02 * s], color=col, lw=9 * s, alpha=a, solid_capstyle="round", zorder=z)
    for d in (-1, 1):
        dax.plot([x, x + d * 0.10 * s], [y + 0.02 * s, y + 0.15 * s], color=col, lw=9 * s, alpha=a,
                 solid_capstyle="round", zorder=z)


def chroms(dax, x, y, pair, s, a, gap=0.32, z=8):
    xs = [x] if len(pair) == 1 else [x - gap * s, x + gap * s]
    for xx, ch in zip(xs, pair):
        (xchrom if ch == "X" else ychrom)(dax, xx, y, s, a, z)


def lab(dax, x, y, s, col, a, size=22, va="center", z=10):
    if a > 0.01:
        outline(dax.text(x, y, s, ha="center", va=va, fontsize=size, fontweight="bold", color=col, alpha=min(1, a),
                         zorder=z))


def sperm(dax, x, y, ch, a, t, z=7):
    dax.add_patch(Ellipse((x, y), 0.62, 0.46, facecolor="#13264d", edgecolor=WHITE, lw=2.5, alpha=a, zorder=z))
    tail = np.linspace(0, 0.5, 30)
    dax.plot(x + 0.31 + tail, y + 0.07 * np.sin(tail * 10 - t * 12), color=WHITE, lw=2.5, alpha=a, zorder=z - 1)
    (xchrom if ch == "X" else ychrom)(dax, x, y, 0.55, a, z + 1)


def egg(dax, x, y, a, r=0.42, z=7):
    dax.add_patch(Circle((x, y), r, facecolor="#2a1d3d", edgecolor=PURPLE, lw=3, alpha=a, zorder=z))
    xchrom(dax, x, y, 0.6, a, z + 1)


def arrow(dax, p, q, col, a, z=4, lw=2.6):
    if a > 0.01:
        dax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=22, color=col, lw=lw, alpha=min(1, a),
                                      shrinkA=0, shrinkB=0, zorder=z))


def draw(c):
    dax = c.area(0.0, 0.0, 7.6)
    t = c.t

    # 1) hook: a sperm swims to an egg — "boy or girl?"
    h_in = ease(c.phase("hook", 0.05, 0.3))
    h_out = 1 - ease(c.phase("pairs", 0.0, 0.2))
    ha = h_in * h_out
    if ha > 0.01:
        mv = ease(c.phase("hook", 0.1, 0.75))
        dax.add_patch(Circle((0.9, 0.4), 1.25, facecolor="#2a1d3d", edgecolor=PURPLE, lw=3, alpha=ha, zorder=3))
        sx = lerp(-3.2, -0.65, mv)
        dax.add_patch(Ellipse((sx, 0.4), 0.6, 0.4, color=WHITE, alpha=ha, zorder=6))
        tail = np.linspace(0, 1.3, 40)
        dax.plot(sx - 0.3 - tail, 0.4 + 0.1 * np.sin(tail * 9 - t * 12), color=WHITE, lw=3, alpha=ha, zorder=5)
        qa = back_out(c.phase("hook", 0.65, 0.95))
        if qa > 0.01:
            outline(dax.text(0.9, 0.4, "?", ha="center", va="center", fontsize=90 * min(1, qa), fontweight="bold",
                             color=GOLD, alpha=ha, zorder=9))
            lab(dax, 0.0, -1.75, "boy or girl?", WHITE, ha * min(1, qa), size=32)

    # 2) the 23 pairs — 22 alike, 1 sex pair
    g_in = ease(c.phase("pairs", 0.1, 0.45))
    g_out = 1 - ease(c.phase("sexpair", 0.45, 0.7))
    ga = g_in * g_out
    if ga > 0.01:
        cols = [CYAN, PINK, GREEN, PURPLE, "#ff9f43", LTGREY]
        for k in range(PAIRS):
            row, col = divmod(k, 6)
            n_in_row = min(6, PAIRS - row * 6)
            x = (col - (n_in_row - 1) / 2) * 1.05
            y = 1.85 - row * 0.95
            ak = ga * ease(c.phase("pairs", 0.1 + 0.015 * k, 0.25 + 0.015 * k))
            if k < AUTOSOME_PAIRS:
                hgt = 0.62 - 0.012 * k
                for d in (-1, 1):
                    dax.plot([x + d * 0.11, x + d * 0.11], [y - hgt / 2, y + hgt / 2], color=cols[k % 6], lw=8,
                             alpha=ak * (1 - 0.6 * ease(c.phase("sexpair", 0.0, 0.25))), solid_capstyle="round", zorder=6)
            else:
                sa = ease(c.phase("sexpair", 0.0, 0.25))
                dax.add_patch(FancyBboxPatch((x - 0.42, y - 0.45), 0.84, 0.9, boxstyle="round,pad=0,rounding_size=0.12",
                                             facecolor="none", edgecolor=GOLD, lw=3, alpha=ak * (0.4 + 0.6 * sa), zorder=5))
                xchrom(dax, x - 0.15, y, 0.85, ak)
                yy = ease(c.phase("sexpair", 0.3, 0.45))
                xchrom(dax, x + 0.15, y, 0.85, ak * (1 - yy))
                ychrom(dax, x + 0.15, y - 0.03, 0.85, ak * yy)
                lab(dax, x, y - 0.72, "sex pair", GOLD, ak * sa, size=24)
        lab(dax, 0.0, -2.25, f"{AUTOSOME_PAIRS} pairs: same in boys & girls", WHITE,
            ga * ease(c.phase("pairs", 0.6, 0.85)) * (1 - ease(c.phase("sexpair", 0.0, 0.2))), size=24)
        lab(dax, 0.0, -2.25, "women: XX     men: XY", GOLD, ga * ease(c.phase("sexpair", 0.2, 0.4)), size=28)

    # 3) the cross: parents → gametes → children
    pa = ease(c.phase("sexpair", 0.6, 0.85))
    if pa > 0.01:
        for x, pair, name in ((MX, MOTHER, "mother: XX"), (FX, FATHER, "father: XY")):
            dax.add_patch(Circle((x, PY), 0.62, facecolor="#13264d", edgecolor=WHITE, lw=3, alpha=pa, zorder=5))
            chroms(dax, x, PY + 0.03, pair, 0.85, pa)
            lab(dax, x, PY + 0.88, name, WHITE, pa, size=24)

    lab_off = 1 - ease(c.phase("cross", 0.0, 0.15))      # gamete labels make way for the cross arrows
    ea = ease(c.phase("egg", 0.15, 0.45))
    if ea > 0.01:
        for ex in (MX - 0.75, MX + 0.75):
            arrow(dax, (MX + (ex - MX) * 0.45, PY - 0.62), (ex, GY + 0.5), PURPLE, ea * 0.9)
            egg(dax, ex, GY, ea)
        lab(dax, MX, GY - 0.68, "every egg: X", PURPLE, ea * ease(c.phase("egg", 0.45, 0.7)) * lab_off, size=22)

    sa = ease(c.phase("sperm", 0.1, 0.45))
    if sa > 0.01:
        spx = {"X": FX - 1.1, "Y": FX + 0.6}
        for ch, sx in spx.items():
            arrow(dax, (FX + (sx - FX) * 0.35, PY - 0.62), (sx, GY + 0.36), WHITE, sa * 0.9)
            sperm(dax, sx, GY, ch, sa, t)
        lab(dax, FX, GY - 0.68, "sperm: X or Y", WHITE, sa * ease(c.phase("sperm", 0.45, 0.7)) * lab_off, size=22)

    # children
    kids = [("XX", -1.3, "girl", ("X", "X")), ("XY", 1.3, "boy", ("X", "Y"))]
    for i, (code, kx, name, pair) in enumerate(kids):
        at0 = 0.05 + 0.45 * i
        ka = ease(c.phase("cross", at0, at0 + 0.3))
        if ka <= 0.01:
            continue
        # the egg's X and the matching sperm meet
        arrow(dax, (MX + 0.75, GY - 0.45), (kx - 0.35, CY + 0.5), PURPLE, ka * 0.8)
        sx = FX - 1.1 if pair[1] == "X" else FX + 0.6
        arrow(dax, (sx, GY - 0.3), (kx + 0.35, CY + 0.5), XC if pair[1] == "X" else YC, ka * 0.9)
        dax.add_patch(Circle((kx, CY), 0.55, facecolor="#123b2c", edgecolor=GREEN, lw=3, alpha=ka, zorder=6))
        chroms(dax, kx, CY + 0.03, pair, 0.75, ka, gap=0.3)
        lab(dax, kx, CY - 0.82, f"{code} → {name}", GREEN, ka, size=24)

    # chance: 50 % badges, a highlight hopping between the two outcomes
    ca = ease(c.phase("chance", 0.05, 0.3))
    if ca > 0.01:
        for i, (code, kx, name, pair) in enumerate(kids):
            bx = kx + (-1.25 if i == 0 else 1.25)
            lab(dax, bx, CY, PCT, GOLD, ca, size=30)
        hop = 0 if int(c.phase("chance", 0.0, 1.0) * 7) % 2 == 0 else 1
        if not c.at("math"):
            dax.add_patch(Circle((kids[hop][1], CY), 0.68, facecolor="none", edgecolor=GOLD, lw=4,
                                 alpha=ca * 0.9, zorder=7))

    c.steps([("egg: always X · sperm: X or Y", 0.05, WHITE),
             ("the sperm's X or Y decides", 0.4, GOLD)], ys=(0.345, 0.285))


# ── Hindi version (posted in the 8 PM slot; voice: Indic Parler-TTS "rohit") ──
HINDI = {
    "title": "शुक्राणु से लिंग तय क्यों?",
    "end_text": "और WHY? वीडियो के लिए फ़ॉलो करें",
    "beats": {
        "hook":    ("लड़का या लड़की? यह अंडा नहीं, शुक्राणु क्यों तय करता है?",
                    "लड़का या लड़की? अंडा नहीं, शुक्राणु क्यों तय करता है?"),
        "pairs":   ("हममें गुणसूत्रों के तेईस जोड़े हैं। बाईस जोड़े लड़के और लड़की में एक जैसे हैं।",
                    f"गुणसूत्रों के {PAIRS} जोड़े। {AUTOSOME_PAIRS} जोड़े लड़के-लड़की में एक जैसे।"),
        "sexpair": ("एक जोड़ा लिंग तय करता है। स्त्री में एक्स एक्स, पुरुष में एक्स वाई। वाई छोटा है।",
                    "एक जोड़ा लिंग तय करता है। स्त्री: XX, पुरुष: XY (Y छोटा)"),
        "egg":     ("अंडे को जोड़े का एक गुणसूत्र मिलता है। माँ के पास केवल एक्स, तो हर अंडे में एक्स।",
                    "अंडे को जोड़े का एक ही गुणसूत्र। माँ के पास केवल X → हर अंडे में X"),
        "sperm":   ("पिता के पास एक्स और वाई दोनों हैं। तो आधे शुक्राणुओं में एक्स, आधे में वाई।",
                    "पिता के पास X और Y → आधे शुक्राणुओं में X, आधे में Y"),
        "cross":   ("एक्स शुक्राणु और एक्स अंडा, तो लड़की। वाई शुक्राणु और एक्स अंडा, तो लड़का।",
                    "X शुक्राणु + X अंडा = XX → लड़की · Y शुक्राणु + X अंडा = XY → लड़का"),
        "chance":  ("कौन सा शुक्राणु अंडे तक पहुँचे, यह बस संयोग है, लगभग आधा आधा। इसे कोई नहीं चुनता।",
                    f"कौन सा शुक्राणु पहुँचे, यह संयोग है — लगभग {PCT}-{PCT}। कोई चुनता नहीं।"),
        "math":    ("अंडा हमेशा एक्स देता है। फ़ैसला शुक्राणु का एक्स या वाई करता है।",
                    "अंडा हमेशा X देता है। शुक्राणु का X या Y लिंग तय करता है।"),
        "end":     ("और ऐसे ही व्हाई वीडियो के लिए सी बी एस ई मॉक को फ़ॉलो करें।",
                    "और WHY? वीडियो के लिए @cbsemock को फ़ॉलो करें"),
    },
    "caption": f"""🧬 WHY? (हिंदी) — बच्चा लड़का होगा या लड़की, यह शुक्राणु से क्यों तय होता है?

मानव कोशिका: गुणसूत्रों के {PAIRS} जोड़े — इनमें {AUTOSOME_PAIRS} जोड़े लड़के-लड़की में एक जैसे।
सिर्फ़ एक जोड़ा लिंग तय करता है: स्त्री XX, पुरुष XY (Y छोटा)।

🥚 हर अंडे में X होता है (माँ के पास देने को केवल X है)
🔬 शुक्राणु दो तरह के: आधे में X, आधे में Y
X + X = XX → लड़की 👧 · X + Y = XY → लड़का 👦
कौन सा शुक्राणु अंडे तक पहुँचे, यह संयोग है — लगभग {PCT}-{PCT}।

आनुवंशिकता (लिंग निर्धारण) — कक्षा 10 विज्ञान। 📘 बोर्ड का पसंदीदा प्रश्न!

💾 सेव करें · 📤 अपने बायो ग्रुप में शेयर करें

🌐 फ्री नोट्स और मॉक पेपर → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #HindiMedium #Class10Science #Heredity #BoardExam2027""",
}
