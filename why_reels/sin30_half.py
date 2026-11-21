"""WHY? — Why is sin 30° exactly ½?  (Class 10 Maths) — Part 3 of the trig series."""
import math
from matplotlib.patches import Polygon, Arc
from why_kit import ease, lerp, outline, CYAN, GOLD, PINK, GREEN, PURPLE, WHITE, GREY

TITLE = r"Why is $\sin 30^{\circ} = \frac{1}{2}$ ?"
TAGS = "Class 10 Maths"
PART = "PART 3 · TRIG SERIES"
END_TEXT = "Watch Parts 1 & 2 on our profile"
END_Y = 0.228
BEATS = [
    ("hook",  "Why is sine thirty exactly one half? One triangle explains it.",
              "Why is sin 30° exactly ½? One triangle explains it.", 3.6),
    ("eq",    "Take an equilateral triangle with every side two. Every angle is sixty degrees.",
              "An equilateral triangle, every side 2. Every angle = 60°.", 4.4),
    ("drop",  "Drop a line from the top, straight down to the middle of the base.",
              "Drop a line from the top straight down to the middle.", 3.6),
    ("split", "It cuts the base into one and one, and the top angle into thirty and thirty.",
              "Base → 1 and 1. Top angle → 30° and 30°.", 4.4),
    ("sin",   "Look at one half. Opposite the thirty degree angle is one. The hypotenuse is two.",
              "In this right triangle: opposite 30° = 1, hypotenuse = 2.", 4.4),
    ("math",  "Sine is opposite over hypotenuse. One over two. Exactly a half, for every size of triangle.",
              "sin 30° = opposite ÷ hypotenuse = 1 ÷ 2 = ½", 4.6),
    ("bonus", "Bonus. The height is root three, so cos thirty is root three by two.",
              "Bonus: height = √(2² − 1²) = √3 → cos 30° = √3/2", 4.4),
    ("end",   "Watch parts one and two on our profile, and follow for part four tomorrow.",
              "Parts 1 & 2 are on our profile · Part 4 tomorrow!", 3.4),
]
CAPTION = """📐 WHY? Part 3 — Why is sin 30° exactly ½?

Take an equilateral triangle (all sides 2, all angles 60°) and cut it in half…
Opposite 30° = 1, hypotenuse = 2 → sin 30° = 1/2 ✨
Bonus: height = √3 → cos 30° = √3/2.

👉 Parts 1 & 2 (sin²θ + cos²θ = 1 · 1 + tan²θ = sec²θ) are on our profile.
🔔 Part 4 tomorrow: Why is the angle of elevation = angle of depression?

💾 Save it · 📤 Share with your maths group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Trigonometry #Class10Maths #VisualMaths #BoardExam2027 #CBSE #MathsTricks"""

R3 = math.sqrt(3)
A, B, C = (-1.0, 0.0), (1.0, 0.0), (0.0, R3)          # side 2
M = (0.0, 0.0)


def draw(c):
    zoom = ease(c.phase("sin", 0.0, 0.5))               # camera moves onto the right half
    dax = c.area(lerp(0.0, 0.40, zoom), lerp(0.85, 0.98, zoom), lerp(3.0, 2.75, zoom))
    tri = ease(c.phase("hook", 0.15, 0.9))
    if tri > 0:
        dax.add_patch(Polygon([A, B, C], closed=True, facecolor=CYAN, edgecolor=CYAN, lw=4,
                              alpha=0.12 * tri, zorder=2))
        dax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], color=CYAN, lw=4, alpha=tri, zorder=3)
    la = ease(c.phase("eq", 0.05, 0.4)) * (1 - ease(c.phase("split", 0.0, 0.25)))
    if la > 0:
        for (p, q), dx, dy in [((A, B), 0, -0.16), ((B, C), 0.2, 0.05), ((C, A), -0.2, 0.05)]:
            outline(dax.text((p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, "2", color=WHITE, fontsize=32,
                             fontweight="bold", ha="center", va="center", alpha=la, zorder=9))
    aa = ease(c.phase("eq", 0.45, 0.85)) * (1 - ease(c.phase("split", 0.0, 0.25)))
    if aa > 0:
        for (vx, vy), t1, t2, tx, ty in [(A, 0, 60, 0.32, 0.13), (B, 120, 180, -0.32, 0.13), (C, 240, 300, 0, -0.38)]:
            dax.add_patch(Arc((vx, vy), 0.42, 0.42, theta1=t1, theta2=t2, color=GOLD, lw=3, alpha=aa, zorder=6))
            outline(dax.text(vx + tx, vy + ty, "60°", color=GOLD, fontsize=24, ha="center", va="center", alpha=aa, zorder=9))
    da = ease(c.phase("drop", 0.1, 0.8))
    if da > 0:
        dax.plot([0, 0], [R3, R3 - R3 * da], color=PINK, lw=4, ls=(0, (7, 4)) if da < 1 else "-", zorder=5)
        if da >= 1:
            dax.plot([0.1, 0.1, 0], [0, 0.1, 0.1], color=WHITE, lw=2, zorder=6)
    sa = ease(c.phase("split", 0.1, 0.55))
    if sa > 0:
        outline(dax.text(-0.5, -0.16, "1", color=GREEN, fontsize=32, fontweight="bold", ha="center", va="center", alpha=sa, zorder=9))
        outline(dax.text(0.5, -0.16, "1", color=GREEN, fontsize=32, fontweight="bold", ha="center", va="center", alpha=sa, zorder=9))
        dax.plot([0, 1], [0, 0], color=GREEN, lw=5, alpha=sa, zorder=4)
    ta = ease(c.phase("split", 0.5, 0.9))
    if ta > 0:
        dax.add_patch(Arc(C, 0.6, 0.6, theta1=240, theta2=270, color=GOLD, lw=3, alpha=ta, zorder=6))
        dax.add_patch(Arc(C, 0.6, 0.6, theta1=270, theta2=300, color=ORANGE_SAFE, lw=3, alpha=ta, zorder=6))
        outline(dax.text(-0.13, R3 - 0.45, "30°", color=GOLD, fontsize=22, ha="center", va="center", alpha=ta, zorder=9))
        outline(dax.text(0.14, R3 - 0.45, "30°", color=GOLD, fontsize=22, ha="center", va="center", alpha=ta, zorder=9))
    ha = ease(c.phase("sin", 0.2, 0.6))
    if ha > 0:                                           # highlight the right half
        dax.add_patch(Polygon([M, B, C], closed=True, facecolor=GOLD, edgecolor="none", alpha=0.22 * ha, zorder=2))
        dax.plot([0, 1], [R3, 0], color=GOLD, lw=6, alpha=ha, zorder=5)
        outline(dax.text(0.62, 1.0, "2", color=GOLD, fontsize=36, fontweight="bold", ha="center", va="center", alpha=ha, zorder=9))
        outline(dax.text(0.5, 0.18, "opposite 30°", color=GREEN, fontsize=18, ha="center", va="center", alpha=ha, zorder=9))
    ba = ease(c.phase("bonus", 0.1, 0.5))
    if ba > 0:
        outline(dax.text(-0.12, R3 / 2, r"$\sqrt{3}$", color=PINK, fontsize=30, ha="right", va="center", alpha=ba, zorder=9))

    c.steps([(r"$\sin 30^{\circ} = \frac{\mathrm{opposite}}{\mathrm{hypotenuse}} = \frac{1}{2}$", 0.05, WHITE),
             (r"$\sin 30^{\circ} = \frac{1}{2}$", 0.5, GOLD)], ys=(0.352, 0.290))
    bb = ease(c.phase("bonus", 0.35, 0.6))
    if bb > 0 and not c.at("end"):
        c.text(0.5, 0.235, r"$\cos 30^{\circ} = \frac{\sqrt{3}}{2}$", size=34, color=PINK, alpha=bb)


ORANGE_SAFE = GOLD

# ── Hindi version (posted in the 8 PM slot; voice: Indic Parler-TTS "rohit") ──
HINDI = {
    "title": "sin 30° = ½ क्यों?",
    "part": "भाग 3 · त्रिकोणमिति सीरीज़",
    "end_text": "भाग 1 और 2 हमारी प्रोफ़ाइल पर देखें",
    "beats": {
        "hook":  ("साइन तीस डिग्री ठीक आधा क्यों होता है? एक त्रिभुज से समझिए।",
                  "sin 30° ठीक ½ क्यों? एक त्रिभुज से समझिए।"),
        "eq":    ("एक समबाहु त्रिभुज लीजिए, जिसकी हर भुजा दो है। हर कोण साठ डिग्री का है।",
                  "समबाहु त्रिभुज, हर भुजा 2. हर कोण = 60°"),
        "drop":  ("ऊपर के शीर्ष से, आधार के बीच तक सीधी रेखा नीचे गिराइए।",
                  "शीर्ष से आधार के बीच तक सीधी रेखा गिराइए।"),
        "split": ("यह आधार को एक और एक में, और ऊपर के कोण को तीस और तीस में बाँट देती है।",
                  "आधार → 1 और 1. ऊपर का कोण → 30° और 30°"),
        "sin":   ("एक आधे हिस्से को देखिए। तीस डिग्री के सामने की भुजा एक है, कर्ण दो है।",
                  "इस समकोण त्रिभुज में: 30° के सामने = 1, कर्ण = 2"),
        "math":  ("साइन यानी लंब बटा कर्ण। एक बटा दो। ठीक आधा, त्रिभुज चाहे जितना बड़ा हो।",
                  "sin 30° = लंब ÷ कर्ण = 1 ÷ 2 = ½"),
        "bonus": ("बोनस। ऊँचाई रूट तीन है, इसलिए कॉस तीस, रूट तीन बटा दो।",
                  "बोनस: ऊँचाई = √(2² − 1²) = √3 → cos 30° = √3/2"),
        "end":   ("भाग एक और दो हमारी प्रोफ़ाइल पर देखिए, और पूरी सीरीज़ के लिए फ़ॉलो कीजिए।",
                  "भाग 1 और 2 हमारी प्रोफ़ाइल पर · सीरीज़ के लिए फ़ॉलो करें"),
    },
    "caption": """📐 WHY? भाग 3 (हिंदी) — sin 30° ठीक ½ क्यों होता है?

एक समबाहु त्रिभुज लीजिए (सभी भुजाएँ 2, सभी कोण 60°) और उसे आधा काटिए…
30° के सामने की भुजा = 1, कर्ण = 2 → sin 30° = 1/2 ✨
बोनस: ऊँचाई = √3 → cos 30° = √3/2

👉 भाग 1 और 2 (sin²θ + cos²θ = 1 · 1 + tan²θ = sec²θ) हमारी प्रोफ़ाइल पर हैं।

💾 सेव करें · 📤 अपने मैथ्स ग्रुप में शेयर करें

🌐 फ्री नोट्स और मॉक पेपर → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #HindiMedium #Class10Maths #Trigonometry #BoardExam2027""",
}
