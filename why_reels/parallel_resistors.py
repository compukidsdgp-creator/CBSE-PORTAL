"""WHY? — Why does adding a resistor in PARALLEL lower the resistance?  (Class 10 & 12 Physics)"""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why does PARALLEL lower resistance?"
TAGS = "Class 10 & 12 Physics"
BEATS = [
    ("hook",    "Add another resistor, and the total resistance goes down? Sounds wrong. Let's see why.",
                "Add another resistor and the total resistance goes DOWN? Sounds wrong. Let's see why.", 4.2),
    ("road",    "Think of current as cars on a road. One resistor is like one narrow road.",
                "Think of current as cars on a road. One resistor = one narrow road.", 4.4),
    ("second",  "Now add a second resistor, side by side. That's a parallel connection. A second road.",
                "Add a second resistor side by side — a parallel connection. A second road!", 4.6),
    ("flow",    "Cars now have two paths, so twice as many get through every second. More current, from the same battery.",
                "Two paths → twice as many cars per second. More current from the same battery.", 5.6),
    ("ohm",     "Same voltage, but double the current, means half the resistance. Because R equals V by I.",
                "Same voltage, double the current → half the resistance. R = V / I.", 5.0),
    ("formula", "That's why in parallel, one by R equals one by R one, plus one by R two. "
                "Two equal resistors give half the resistance.",
                "In parallel: 1/R = 1/R₁ + 1/R₂. Two equal resistors give HALF the resistance.", 6.0),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """⚡ WHY? — Why does adding a resistor in parallel LOWER the resistance?

Think of current as cars 🚗 and resistors as roads 🛣️
One road → 1 A. Add a second road side by side → 2 A from the same battery!
Same V, double I → R = V/I is HALVED. That's 1/R = 1/R₁ + 1/R₂ ✨

Class 10 Electricity & Class 12 Current Electricity — finally intuitive. 🧠

💾 Save it · 📤 Share with your physics group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Physics #Electricity #Class10Science #Class12Physics #BoardExam2027 #CBSE"""

XL, XR, YB = -3.6, 3.6, -2.7
END_Y = 0.398


def zigzag(dax, x0, x1, y, amp, color, alpha, lw=4):
    xs = np.linspace(x0, x1, 13)
    ys = y + np.array([0 if k in (0, 12) else (amp if k % 2 else -amp) for k in range(13)])
    dax.plot(xs, ys, color=color, lw=lw, alpha=alpha, zorder=6, solid_joinstyle="round")


def lane(dax, y, alpha, label, t, n_cars, speed):
    dax.plot([XL, -1.1], [y, y], color=LTGREY, lw=4, alpha=alpha, zorder=4)
    dax.plot([1.1, XR], [y, y], color=LTGREY, lw=4, alpha=alpha, zorder=4)
    zigzag(dax, -1.1, 1.1, y, 0.32, GOLD, alpha)
    outline(dax.text(0, y + 0.55, label, ha="center", fontsize=24, fontweight="bold", color=GOLD,
                     alpha=alpha, zorder=7))
    for q in range(n_cars):
        f = (t * speed + q / n_cars) % 1
        dax.add_patch(Circle((lerp(XL + 0.2, XR - 0.2, f), y), 0.13, color=CYAN, alpha=alpha, zorder=8))


def draw(c):
    dax = c.area(0.0, -0.6, 9.2)
    t = c.t
    two = ease(c.phase("second", 0.15, 0.6))
    ya = lerp(0.1, 0.95, two)         # first road moves up to make room
    yb = -0.95

    base = ease(c.phase("hook", 0.15, 0.6))
    # outer loop: left / right wires, bottom wire with the battery
    dax.plot([XL, XL], [ya, YB], color=LTGREY, lw=4, alpha=base, zorder=4)
    dax.plot([XR, XR], [ya, YB], color=LTGREY, lw=4, alpha=base, zorder=4)
    dax.plot([XL, -0.35], [YB, YB], color=LTGREY, lw=4, alpha=base, zorder=4)
    dax.plot([0.35, XR], [YB, YB], color=LTGREY, lw=4, alpha=base, zorder=4)
    dax.plot([-0.35, -0.35], [YB - 0.55, YB + 0.55], color=WHITE, lw=5, alpha=base, zorder=5)
    dax.plot([0.35, 0.35], [YB - 0.3, YB + 0.3], color=WHITE, lw=8, alpha=base, zorder=5)
    outline(dax.text(0, YB - 0.8, "battery  V = 6 V", ha="center", fontsize=22, fontweight="bold",
                     color=WHITE, alpha=base, zorder=7))

    moving = c.at("road")
    speed = 0.35
    lane(dax, ya, base, "R₁ = 6 Ω", t if moving else 0, 5 if moving else 0, speed)
    if two > 0:
        dax.plot([XL, XL], [ya, yb], color=LTGREY, lw=4, alpha=two, zorder=4)
        lane(dax, yb, two, "R₂ = 6 Ω", t if c.at("flow") else 0, 5 if c.at("flow") else 0, speed)

    # cars on the battery wire: twice as dense once both roads carry traffic
    if moving:
        n = 5 if not c.at("flow") else 10
        for q in range(n):
            f = (t * speed + q / n) % 1
            dax.add_patch(Circle((lerp(XR - 0.2, XL + 0.2, f), YB), 0.13, color=CYAN, alpha=0.9, zorder=8))

    # current meter
    if c.at("road"):
        ia = ease(c.phase("road", 0.3, 0.6))
        I = 2 if c.phase("flow", 0.25, 0.4) > 0 else 1
        col = GREEN if I == 2 else CYAN
        dax.add_patch(FancyBboxPatch((-1.55, 2.0), 3.1, 0.75, boxstyle="round,pad=0,rounding_size=0.18",
                                     facecolor="#0e1d3f", edgecolor=col, lw=3, alpha=ia, zorder=9))
        dax.text(0, 2.37, f"current  I = {I} A", ha="center", va="center", fontsize=28, fontweight="bold",
                 color=col, alpha=ia, zorder=10)
        if I == 2:
            pa = back_out(c.phase("flow", 0.25, 0.45))
            outline(dax.text(2.0, 2.37, "×2", ha="left", va="center", fontsize=38 * min(1, pa), fontweight="bold",
                             color=GREEN, zorder=10))

    # Ohm's law reasoning
    oa = ease(c.phase("ohm", 0.0, 0.25)) * (1 - ease(c.phase("formula", 0.0, 0.15)))
    if oa > 0:
        rows = [("V = 6 V  (same battery)", WHITE, 0.0), ("I = 1 A  →  2 A", GREEN, 0.25),
                (r"R = V / I :  6 Ω  →  3 Ω", GOLD, 0.5)]
        for k, (s, col, at) in enumerate(rows):
            a = ease(c.phase("ohm", at, at + 0.25)) * oa / max(oa, 1e-6) * oa
            c.text(0.5, 0.352 - k * 0.052, s, size=36 if col != GOLD else 40, color=col, alpha=a)
    c.steps([("1/R = 1/R₁ + 1/R₂", 0.0, WHITE),
             ("1/R = 1/6 + 1/6 = 1/3", 0.3, CYAN),
             ("R = 3 Ω  (half!)", 0.6, GOLD)], ys=(0.350, 0.295, 0.238), beat="formula")


HINDI = {
    "title": "पैरेलल में प्रतिरोध कम क्यों?",
    "end_text": "और WHY? वीडियो के लिए फ़ॉलो करें",
    "beats": {
        "hook":    ("एक और प्रतिरोधक जोड़ा, और कुल प्रतिरोध घट गया? अजीब लगता है। आइए समझें क्यों।",
                    "एक और प्रतिरोधक जोड़ा और कुल प्रतिरोध घट गया? अजीब लगता है। समझिए क्यों।"),
        "road":    ("विद्युत धारा को सड़क पर चलती कारें मानिए। एक प्रतिरोधक, यानी एक पतली सड़क।",
                    "धारा = सड़क पर चलती कारें। एक प्रतिरोधक = एक पतली सड़क।"),
        "second":  ("अब बगल में दूसरा प्रतिरोधक जोड़िए। यह पार्श्वक्रम संयोजन है। यानी दूसरी सड़क।",
                    "बगल में दूसरा प्रतिरोधक — पार्श्वक्रम (पैरेलल) संयोजन। दूसरी सड़क!"),
        "flow":    ("अब कारों के दो रास्ते हैं, तो हर सेकंड दोगुनी कारें निकलती हैं। उसी बैटरी से ज़्यादा धारा।",
                    "दो रास्ते → हर सेकंड दोगुनी कारें। उसी बैटरी से ज़्यादा धारा।"),
        "ohm":     ("वोल्टेज वही, पर धारा दोगुनी, यानी प्रतिरोध आधा। क्योंकि आर बराबर वी बटा आई।",
                    "वोल्टेज वही, धारा दोगुनी → प्रतिरोध आधा। R = V / I"),
        "formula": ("इसीलिए पैरेलल में, एक बटा आर, बराबर एक बटा आर एक, प्लस एक बटा आर दो।",
                    "पैरेलल में: 1/R = 1/R₁ + 1/R₂. दो बराबर प्रतिरोधक → आधा प्रतिरोध।"),
        "end":     ("और ऐसे ही व्हाई वीडियो के लिए सी बी एस ई मॉक को फ़ॉलो करें।",
                    "और WHY? वीडियो के लिए @cbsemock को फ़ॉलो करें"),
    },
    "caption": """⚡ WHY? (हिंदी) — पैरेलल (पार्श्वक्रम) में प्रतिरोधक जोड़ने पर प्रतिरोध कम क्यों होता है?

धारा को कारें 🚗 और प्रतिरोधकों को सड़कें 🛣️ मानिए
एक सड़क → 1 A. बगल में दूसरी सड़क जोड़िए → उसी बैटरी से 2 A!
V वही, I दोगुनी → R = V/I आधा हो गया। यही है 1/R = 1/R₁ + 1/R₂ ✨

कक्षा 10 विद्युत और कक्षा 12 विद्युत धारा — अब समझ में आएगा। 🧠

💾 सेव करें · 📤 अपने फ़िज़िक्स ग्रुप में शेयर करें

🌐 फ्री नोट्स और मॉक पेपर → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #HindiMedium #Physics #Electricity #Class10Science #Class12Physics #BoardExam2027""",
}
