"""WHY? — Why is 1 + tan²θ = sec²θ?  (Class 10 Maths) — Part 2 of the trig series (same picture as Part 1)."""
import math
import numpy as np
from matplotlib.patches import Polygon, Circle, Arc
from why_kit import ease, lerp, outline, CYAN, GOLD, PINK, GREEN, PURPLE, WHITE, GREY

TITLE = r"Why is $1 + \tan^{2}\theta = \sec^{2}\theta$ ?"
TAGS = "Class 10 Maths"
PART = "PART 2 · TRIG SERIES"
END_TEXT = "Watch Part 1 on our profile"
END_Y = 0.418
BEATS = [
    ("hook",   "Part one: sine squared plus cos squared is one. Here is its twin.",
               "Part 1: sin²θ + cos²θ = 1. Here's its twin.", 3.6),
    ("circle", "Same circle of radius one. Same angle theta.",
               "Same circle of radius 1. Same angle θ.", 3.0),
    ("tangent", "Draw a line touching the circle on the right, and stretch the radius to meet it.",
               "Draw a line touching the circle on the right, and stretch the radius until it meets it.", 4.8),
    ("sides",  "The new triangle has base one. By similar triangles, its height is tan theta, and its long side is sec theta.",
               "Base = 1. By similar triangles, height = tan θ and the long side = sec θ.", 5.4),
    ("pyth",   "Pythagoras again. Base squared plus height squared equals the long side squared.",
               "Pythagoras: base² + height² = (long side)²", 4.2),
    ("move",   "Change the angle. The triangle stretches, but the rule never breaks.",
               "Change the angle: the triangle stretches, but the rule never breaks.", 4.8),
    ("math",   "So one plus tan squared theta equals sec squared theta. Same picture, one step further.",
               "1² + tan²θ = sec²θ → 1 + tan²θ = sec²θ", 4.6),
    ("end",    "Watch part one on our profile, and follow for part three tomorrow.",
               "Watch Part 1 on our profile · Part 3 tomorrow!", 3.4),
]
CAPTION = """📐 WHY? Part 2 — Why is 1 + tan²θ = sec²θ?

Same circle as Part 1 — just stretch the radius to the tangent line…
Base = 1, height = tan θ, long side = sec θ → Pythagoras does the rest! ✨
1 + tan²θ = sec²θ — for every angle (where tan θ is defined).

👉 Missed Part 1 (sin²θ + cos²θ = 1)? It's on our profile.
🔔 Part 3 tomorrow: Why is sin 30° exactly ½?

💾 Save it · 📤 Share with your maths group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Trigonometry #Class10Maths #VisualMaths #BoardExam2027 #CBSE #MathsTricks"""


def angle(c):
    th = lerp(0, 40, ease(c.phase("circle", 0.3, 0.9)))
    mp = c.phase("move", 0.05, 0.95)
    if mp > 0:
        th = 40 + 14 * math.sin(2 * math.pi * mp)          # 26°–54°: keeps the tangent point in frame
    return th


def draw(c):
    dax = c.area(0.30, 0.42, 3.15)
    th = math.radians(angle(c))
    cx, sy = math.cos(th), math.sin(th)
    t, s = math.tan(th), 1 / math.cos(th)

    ca = ease(c.phase("hook", 0.15, 0.8))
    dax.plot([-1.15, 1.75], [0, 0], color=GREY, lw=2, alpha=ca, zorder=1)
    dax.plot([0, 0], [-0.75, 1.65], color=GREY, lw=2, alpha=ca, zorder=1)
    tt = np.linspace(0, 2 * math.pi * ca, 200)
    dax.plot(np.cos(tt), np.sin(tt), color=CYAN, lw=3.5, alpha=0.9, zorder=2)

    pa = ease(c.phase("circle", 0.05, 0.4))
    if pa > 0:
        dax.plot([0, cx * pa], [0, sy * pa], color=WHITE, lw=4, zorder=6, solid_capstyle="round")
        dax.add_patch(Circle((cx, sy), 0.04, color=WHITE, alpha=pa, zorder=8))
        dax.add_patch(Arc((0, 0), 0.5, 0.5, theta1=0, theta2=math.degrees(th), color=GOLD, lw=3, alpha=pa, zorder=7))
        outline(dax.text(0.33 * math.cos(th / 2), 0.33 * math.sin(th / 2), r"$\theta$", color=GOLD,
                         fontsize=32, ha="center", va="center", alpha=pa, zorder=9))
        # Part 1's triangle, faint, for continuity
        dax.add_patch(Polygon([[0, 0], [cx, 0], [cx, sy]], closed=True, facecolor=PURPLE, edgecolor="none",
                              alpha=0.18 * pa, zorder=3))

    ga = ease(c.phase("tangent", 0.05, 0.45))
    if ga > 0:                                            # tangent line x = 1
        dax.plot([1, 1], [-0.7, -0.7 + 2.35 * ga], color=GREEN, lw=2.5, ls=(0, (6, 4)), zorder=4)
    ea = ease(c.phase("tangent", 0.45, 0.9))
    if ea > 0:                                            # radius stretched to the tangent line
        dax.plot([cx, cx + (1 - cx) * ea], [sy, sy + (t - sy) * ea], color=GOLD, lw=4.5, zorder=6, solid_capstyle="round")
    if c.at("sides") or ea >= 1:
        fa = ease(c.phase("sides", 0.0, 0.25)) if not c.at("pyth") else 1
        dax.add_patch(Polygon([[0, 0], [1, 0], [1, t]], closed=True, facecolor=GOLD, edgecolor="none",
                              alpha=0.20 * fa, zorder=3))
        dax.plot([0.92, 0.92, 1.0], [0, 0.08, 0.08], color=WHITE, lw=2, alpha=fa, zorder=6)
        dax.add_patch(Circle((1, t), 0.045, color=GOLD, alpha=1, zorder=8))
    la = ease(c.phase("sides", 0.05, 0.3))
    if la > 0:
        dax.plot([0, 1], [0, 0], color=CYAN, lw=5, alpha=la, zorder=5)
        outline(dax.text(0.5, -0.11, "1", color=CYAN, fontsize=34, fontweight="bold", ha="center", va="top", alpha=la, zorder=9))
    lb = ease(c.phase("sides", 0.3, 0.55))
    if lb > 0:
        dax.plot([1, 1], [0, t], color=PINK, lw=5, alpha=lb, zorder=5)
        outline(dax.text(1.08, t / 2, r"$\tan\theta$", color=PINK, fontsize=30, ha="left", va="center", alpha=lb, zorder=9))
    lc = ease(c.phase("sides", 0.55, 0.8))
    if lc > 0:
        outline(dax.text(0.42, t / 2 + 0.22, r"$\sec\theta$", color=GOLD, fontsize=30, ha="right", va="center",
                         alpha=lc, zorder=9, rotation=0))

    pa2 = ease(c.phase("pyth", 0.15, 0.6))
    if pa2 > 0 and not c.at("move"):
        c.text(0.5, 0.455, r"$1^{2} + \tan^{2}\theta = \sec^{2}\theta$", size=40, color=WHITE, alpha=pa2)
    if c.at("move") and not c.at("math"):
        ra = ease(c.phase("move", 0.0, 0.12))
        c.text(0.5, 0.455, rf"$1 + \tan^2\theta$ = 1 + {t*t:.2f} = {1 + t*t:.2f}   ·   $\sec^2\theta$ = {s*s:.2f}",
               size=30, color=WHITE, alpha=ra, max_w=0.92)
        c.text(0.5, 0.415, f"θ = {math.degrees(th):.0f}°", size=26, color=GOLD, alpha=ra)
    c.steps([(r"$1^{2} + \tan^{2}\theta = \sec^{2}\theta$", 0.05, WHITE),
             (r"$1 + \tan^{2}\theta = \sec^{2}\theta$", 0.45, GOLD)], ys=(0.352, 0.290))

# ── Hindi version (posted in the 8 PM slot; voice: Indic Parler-TTS "rohit") ──
HINDI = {
    "title": "1 + tan²θ = sec²θ क्यों?",
    "part": "भाग 2 · त्रिकोणमिति सीरीज़",
    "end_text": "भाग 1 हमारी प्रोफ़ाइल पर देखें",
    "beats": {
        "hook":    ("भाग एक में देखा, साइन स्क्वेयर्ड प्लस कॉस स्क्वेयर्ड एक होता है। अब उसका जुड़वाँ।",
                    "भाग 1: sin²θ + cos²θ = 1. अब उसका जुड़वाँ।"),
        "circle":  ("वही एक त्रिज्या वाला वृत्त। वही थीटा कोण।",
                    "वही त्रिज्या 1 का वृत्त। वही कोण θ।"),
        "tangent": ("दाईं ओर वृत्त को छूती हुई एक रेखा खींचिए, और त्रिज्या को बढ़ाकर उससे मिलाइए।",
                    "दाईं ओर स्पर्श रेखा खींचिए, त्रिज्या को बढ़ाकर उससे मिलाइए।"),
        "sides":   ("नए त्रिभुज का आधार एक है। समरूप त्रिभुजों से, ऊँचाई टैन थीटा और लंबी भुजा सेक थीटा।",
                    "आधार = 1. समरूप त्रिभुजों से: ऊँचाई = tan θ, लंबी भुजा = sec θ"),
        "pyth":    ("फिर से पाइथागोरस। आधार का वर्ग प्लस ऊँचाई का वर्ग, बराबर लंबी भुजा का वर्ग।",
                    "पाइथागोरस: आधार² + ऊँचाई² = (लंबी भुजा)²"),
        "move":    ("कोण बदलिए। त्रिभुज खिंचता है, पर नियम कभी नहीं टूटता।",
                    "कोण बदलिए: त्रिभुज खिंचता है, नियम नहीं टूटता।"),
        "math":    ("तो एक प्लस टैन स्क्वेयर्ड थीटा, बराबर सेक स्क्वेयर्ड थीटा। वही तस्वीर, एक कदम आगे।",
                    "1² + tan²θ = sec²θ → 1 + tan²θ = sec²θ"),
        "end":     ("भाग एक हमारी प्रोफ़ाइल पर देखिए, और पूरी सीरीज़ के लिए फ़ॉलो कीजिए।",
                    "भाग 1 हमारी प्रोफ़ाइल पर · पूरी सीरीज़ के लिए फ़ॉलो करें"),
    },
    "caption": """📐 WHY? भाग 2 (हिंदी) — 1 + tan²θ = sec²θ क्यों होता है?

भाग 1 वाला ही वृत्त — बस त्रिज्या को स्पर्श रेखा तक बढ़ाइए…
आधार = 1, ऊँचाई = tan θ, लंबी भुजा = sec θ → बाकी काम पाइथागोरस करता है! ✨
1 + tan²θ = sec²θ — हर कोण के लिए (जहाँ tan θ परिभाषित है)।

👉 भाग 1 (sin²θ + cos²θ = 1) हमारी प्रोफ़ाइल पर है।

💾 सेव करें · 📤 अपने मैथ्स ग्रुप में शेयर करें

🌐 फ्री नोट्स और मॉक पेपर → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #HindiMedium #Class10Maths #Trigonometry #BoardExam2027""",
}
