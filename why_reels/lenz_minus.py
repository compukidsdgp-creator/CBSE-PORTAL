"""WHY? — Why does Lenz's law put a MINUS sign in ε = −dΦ/dt?  (Class 12 Physics · Electromagnetic Induction)
Follows NCERT Class 12 Physics, Ch. 6 (Lenz's law and conservation of energy, Fig. 6.6): a bar magnet's N pole pushed
towards a coil makes the coil's near face a N pole, which repels the magnet; with the opposite sign the magnet would be
pulled in and speed up on its own — a perpetual-motion machine, which violates conservation of energy."""
import math
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, ORANGE, NAVY, WHITE, LTGREY, GREY

TITLE = r"Why the MINUS in $\varepsilon = -\dfrac{d\Phi}{dt}$ ?"
TAGS = "Class 12 Physics"
PLAN_RANK = 3
END_Y = 0.252
BEATS = [
    ("hook",     "Why is there a minus sign in Faraday's law? One magnet explains it.",
                 "Why the MINUS sign in ε = −dΦ/dt? One magnet explains it.", 3.6),
    ("push",     "Push a magnet's north pole into a coil. The flux rises, and a current flows.",
                 "Push a magnet's N pole towards a coil → flux Φ increases → current flows.", 4.6),
    ("oppose",   "That current makes the coil's near face a north pole. It repels the magnet.",
                 "The current makes the coil's near face a N pole → it REPELS the magnet.", 4.2),
    ("work",     "So you must push harder. Your work becomes the bulb's electrical energy.",
                 "You must push HARDER → your work becomes the bulb's electrical energy.", 4.6),
    ("whatif",   "Now imagine a plus sign. The near face turns south, and pulls the magnet in.",
                 "Now imagine a PLUS sign: near face = S → it PULLS the magnet in.", 4.4),
    ("runaway",  "It speeds up, the current grows, the pull grows. Energy from nothing!",
                 "Speeds up → more current → stronger pull → energy from NOTHING!", 4.6),
    ("never",    "That breaks conservation of energy. So the induced current must oppose the change.",
                 "Impossible: it breaks CONSERVATION OF ENERGY. The induced current must OPPOSE the change.", 5.0),
    ("math",     "That opposition is the minus sign. This is Lenz's law.",
                 "That opposition IS the minus sign → Lenz's law: ε = −dΦ/dt", 4.0),
    ("end",      "Follow C B S E Mock for more why videos.",
                 "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧲 WHY? — Why is there a MINUS sign in ε = −dΦ/dt?

Push a magnet's N pole towards a coil → flux increases → current flows ⚡
The coil's near face becomes N → it REPELS the magnet
So you must push → your work becomes the bulb's electrical energy 💡

🤔 With a PLUS sign the coil would PULL the magnet in…
faster magnet → more current → stronger pull → energy from nothing ❌
That breaks conservation of energy!

✅ Lenz's law: the induced current always OPPOSES the change in flux — that's the minus sign.
Electromagnetic Induction — Class 12 Physics. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #LenzsLaw #ElectromagneticInduction #Class12Physics #BoardExam2027 #CBSE #Physics"""

# ── geometry (drawing units; c.area(0, 0, 7) shows x −3.5…3.5, y −2.64…2.64) ──
MAG_L = 1.8                                   # magnet length; xn = position of its N face
XN_FAR, XN_NEAR, XN_PUSHED = -1.35, -0.55, -0.30
TURNS = [0.75, 1.10, 1.45, 1.80]              # coil turns (x), radius RC
RC = 0.85
BULB = (1.275, -1.80)
RAYS = np.radians(np.linspace(-56, 56, 9))    # field lines fan out from the N face


def through(xn):
    """How many of the drawn field lines pass through the coil's first turn (computed, not typed)."""
    d = TURNS[0] - xn
    return int(sum(abs(d * math.tan(a)) < RC for a in RAYS))


N_FAR, N_NEAR = through(XN_FAR), through(XN_NEAR)
assert N_NEAR > N_FAR                         # closer magnet → more flux through the coil


def arrow(dax, p, q, col, a, lw=5, z=9, ms=34):
    dax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, color=col, lw=lw, alpha=a, zorder=z))


def label(dax, x, y, s, col, a, size=22, ha="center", va="center"):
    if a > 0.01:
        outline(dax.text(x, y, s, color=col, fontsize=size, fontweight="bold", ha=ha, va=va, alpha=min(1, a), zorder=11))


def magnet_x(c):
    """N-face position and speed (for the bulb) at this frame."""
    if c.at("whatif"):
        if c.at("never"):
            return XN_FAR + (XN_PUSHED - XN_FAR) * 1.0, 0.0
        p = c.phase("runaway", 0.0, 0.85)
        x = XN_FAR + (XN_PUSHED - XN_FAR) * p ** 2.2          # accelerates on its own
        return x, 2.2 * p ** 1.2
    p1 = ease(c.phase("push", 0.15, 0.85))
    p2 = ease(c.phase("work", 0.05, 0.9))
    x = XN_FAR + (XN_NEAR - XN_FAR) * p1 + (XN_PUSHED - XN_NEAR) * p2
    moving = (0.15 < c.phase("push") < 0.85) or (0.05 < c.phase("work") < 0.9)
    return x, (1.0 if moving else 0.0)


def draw(c):
    dax = c.area(0.0, 0.05, 7.0)
    t = c.t
    a0 = ease(c.phase("hook", 0.05, 0.4))
    alt = c.at("whatif") and not c.at("math")              # the imaginary "plus sign" world
    back = ease(c.phase("whatif", 0.0, 0.2)) if alt else 0.0
    xn, speed = magnet_x(c)
    if c.at("math"):
        xn, speed = XN_PUSHED, 0.0

    # tint + tag for the imaginary world
    if alt:
        dax.add_patch(FancyBboxPatch((-3.4, -2.45), 6.8, 4.95, boxstyle="round,pad=0,rounding_size=0.25",
                                     facecolor=PINK, edgecolor=PINK, lw=3, alpha=0.08 * back, zorder=0))
        label(dax, 0, 2.2, r"IMAGINE:  $\varepsilon = +\,d\Phi/dt$", PINK, back, size=24)

    # field lines from the N face
    fa = ease(c.phase("hook", 0.3, 0.8))
    n_in = 0
    for a in RAYS:
        L = min((2.6 - xn) / math.cos(a), 2.0 / max(1e-6, abs(math.sin(a))))   # stay inside the picture
        x2, y2 = xn + L * math.cos(a), L * math.sin(a)
        hit = abs((TURNS[0] - xn) * math.tan(a)) < RC
        n_in += hit
        col = GOLD if (hit and c.at("push")) else CYAN
        dax.plot([xn, x2], [0, y2], color=col, lw=2.6 if hit else 2, alpha=fa * (0.9 if hit else 0.45), zorder=2)

    # coil (back halves, then magnet, then front halves)
    cop = "#e08a3c"
    for x in TURNS:
        dax.add_patch(Ellipse((x, 0), 0.34, 2 * RC, facecolor="none", edgecolor=cop, lw=5, alpha=a0, zorder=3))
    dax.plot([TURNS[0], TURNS[-1]], [RC, RC], color=cop, lw=2, alpha=a0 * 0.5, zorder=3)
    dax.plot([TURNS[0], TURNS[-1]], [-RC, -RC], color=cop, lw=2, alpha=a0 * 0.5, zorder=3)
    # leads to the bulb
    dax.plot([TURNS[0], TURNS[0], BULB[0] - 0.12], [-RC, BULB[1], BULB[1]], color=LTGREY, lw=2.5, alpha=a0, zorder=3)
    dax.plot([TURNS[-1], TURNS[-1], BULB[0] + 0.12], [-RC, BULB[1], BULB[1]], color=LTGREY, lw=2.5, alpha=a0, zorder=3)
    glow = min(1.0, speed) if c.at("push") else 0.0
    if alt and c.at("runaway"):
        glow = min(1.6, speed)
    if glow > 0.02:
        flick = 0.85 + 0.15 * math.sin(t * 23)
        for r, al in ((0.75, 0.10), (0.5, 0.22), (0.32, 0.45)):
            dax.add_patch(Circle(BULB, r * (0.6 + 0.5 * glow), color=GOLD, alpha=min(0.9, al * glow * flick), zorder=4,
                                clip_on=False))
    dax.add_patch(Circle(BULB, 0.2, facecolor=GOLD if glow > 0.05 else "#2a3550", edgecolor=WHITE, lw=2,
                         alpha=a0, zorder=5))

    # bar magnet: S (blue) on the left, N (red) facing the coil
    dax.add_patch(FancyBboxPatch((xn - MAG_L, -0.32), MAG_L / 2, 0.64, boxstyle="round,pad=0,rounding_size=0.06",
                                 facecolor="#3a7bd5", edgecolor="none", alpha=a0, zorder=6))
    dax.add_patch(FancyBboxPatch((xn - MAG_L / 2, -0.32), MAG_L / 2, 0.64, boxstyle="round,pad=0,rounding_size=0.06",
                                 facecolor="#e2475b", edgecolor="none", alpha=a0, zorder=6))
    dax.text(xn - 0.75 * MAG_L, 0, "S", color=WHITE, fontsize=28, fontweight="bold", ha="center", va="center", alpha=a0, zorder=7)
    dax.text(xn - 0.25 * MAG_L, 0, "N", color=WHITE, fontsize=28, fontweight="bold", ha="center", va="center", alpha=a0, zorder=7)

    # push: motion arrow + flux read-out
    pa = ease(c.phase("push", 0.05, 0.3)) * (1 - ease(c.phase("oppose", 0.0, 0.2)))
    if pa > 0:
        arrow(dax, (xn - 1.3, 0.75), (xn - 0.1, 0.75), WHITE, pa, lw=4)
        label(dax, xn - 0.7, 1.15, "push in", WHITE, pa, size=21)
    fx = ease(c.phase("push", 0.3, 0.6)) * (1 - ease(c.phase("whatif", 0.0, 0.15)))
    if c.at("math"):
        fx = 0
    label(dax, 1.275, 1.45, f"Φ ↑  ({n_in} of {len(RAYS)} lines in)", GOLD, fx, size=20)

    # the coil's near face becomes a pole
    real = c.at("oppose") and not alt
    if real:
        ra = ease(c.phase("oppose", 0.05, 0.35)) if not c.at("work") else 1.0
        dax.add_patch(Circle((TURNS[0] - 0.42, 0), 0.26, facecolor="#e2475b", edgecolor=WHITE, lw=2, alpha=ra, zorder=10))
        dax.text(TURNS[0] - 0.42, 0, "N", color=WHITE, fontsize=24, fontweight="bold", ha="center", va="center",
                 alpha=ra, zorder=11)
        label(dax, 0.1, -1.25, "near face = N", PINK, ra * (1 - ease(c.phase("work", 0.0, 0.2))) if not c.at("math") else 0,
              size=20)
        rp = ease(c.phase("oppose", 0.35, 0.7)) if not c.at("work") else 1.0
        arrow(dax, (xn - 0.15, -0.75), (xn - 1.35, -0.75), PINK, rp, lw=5)
        label(dax, xn - 0.75, -1.15, "repels", PINK, rp, size=21)
    wk = ease(c.phase("work", 0.05, 0.3)) * (1 - ease(c.phase("whatif", 0.0, 0.15)))
    if wk > 0 and not c.at("math"):
        arrow(dax, (xn - MAG_L - 1.0, 0), (xn - MAG_L - 0.08, 0), GOLD, wk, lw=6)
        label(dax, xn - MAG_L - 0.55, 0.45, "your push", GOLD, wk, size=20)
        label(dax, BULB[0] - 1.9, BULB[1], "work → light", GOLD, ease(c.phase("work", 0.4, 0.7)), size=21)

    # the imaginary world: near face S, pulls the magnet in
    if alt:
        sa = ease(c.phase("whatif", 0.25, 0.55)) if not c.at("runaway") else 1.0
        dax.add_patch(Circle((TURNS[0] - 0.42, 0), 0.26, facecolor="#3a7bd5", edgecolor=WHITE, lw=2, alpha=sa, zorder=10))
        dax.text(TURNS[0] - 0.42, 0, "S", color=WHITE, fontsize=24, fontweight="bold", ha="center", va="center",
                 alpha=sa, zorder=11)
        pl = ease(c.phase("whatif", 0.55, 0.85)) if not c.at("runaway") else 1.0
        arrow(dax, (xn - 1.35, -0.75), (xn - 0.1, -0.75), GREEN, pl, lw=5)
        label(dax, xn - 0.75, -1.15, "pulls in", GREEN, pl, size=21)
        ru = ease(c.phase("runaway", 0.2, 0.5)) * (1 - ease(c.phase("never", 0.0, 0.2)))
        label(dax, -1.6, 1.45, "faster → brighter\n→ faster …", GOLD, ru, size=20)
        nv = ease(c.phase("never", 0.05, 0.3))
        if nv > 0:
            k = back_out(nv)
            for s in (1, -1):
                dax.plot([-2.2 * k, 2.2 * k], [-1.6 * k * s, 1.6 * k * s], color="#ff3b5c", lw=12, alpha=min(1, nv),
                         zorder=12, solid_capstyle="round")
            label(dax, 0, -2.15, "energy from nothing = IMPOSSIBLE", "#ff6b81", ease(c.phase("never", 0.25, 0.5)), size=21)

    # the real law again, with the opposition highlighted
    if c.at("math"):
        ma = ease(c.phase("math", 0.0, 0.3))
        dax.add_patch(Circle((TURNS[0] - 0.42, 0), 0.26, facecolor="#e2475b", edgecolor=WHITE, lw=2, alpha=ma, zorder=10))
        dax.text(TURNS[0] - 0.42, 0, "N", color=WHITE, fontsize=24, fontweight="bold", ha="center", va="center",
                 alpha=ma, zorder=11)
        arrow(dax, (xn - 0.15, -0.75), (xn - 1.35, -0.75), PINK, ma, lw=5)
        label(dax, xn - 0.75, -1.15, "opposes", PINK, ma, size=21)
        label(dax, 0, 2.2, "LENZ'S LAW", GOLD, ma, size=28)

    c.steps([("induced current OPPOSES the change", 0.05, WHITE),
             (r"$\varepsilon = -\frac{d\Phi}{dt}$", 0.4, GOLD)], ys=(0.378, 0.318))


# ── Hindi version (posted in the 8 PM slot; voice: Indic Parler-TTS "rohit") ──
HINDI = {
    "title": "ε = −dΦ/dt में माइनस क्यों?",
    "end_text": "और WHY? वीडियो के लिए फ़ॉलो करें",
    "beats": {
        "hook":    ("फैराडे के नियम में माइनस चिह्न क्यों होता है? एक चुंबक से समझिए।",
                    "यह माइनस चिह्न क्यों? एक चुंबक से समझिए।"),
        "push":    ("दंड चुंबक का उत्तरी ध्रुव कुंडली की ओर धकेलिए। फ्लक्स बढ़ता है, और धारा बहने लगती है।",
                    "N ध्रुव को कुंडली की ओर धकेलिए → फ्लक्स Φ बढ़ता है → धारा बहती है"),
        "oppose":  ("धारा कुंडली के पास वाले सिरे को उत्तरी ध्रुव बना देती है, जो चुंबक को दूर धकेलता है।",
                    "पास वाला सिरा N ध्रुव बनता है → चुंबक को प्रतिकर्षित करता है"),
        "work":    ("इसलिए ज़ोर लगाकर धकेलना पड़ता है। यही कार्य बल्ब की विद्युत ऊर्जा बनता है।",
                    "आपको ज़ोर लगाना पड़ता है → यही कार्य बल्ब की विद्युत ऊर्जा बनता है"),
        "whatif":  ("अब मान लीजिए, माइनस की जगह प्लस होता। तब पास वाला सिरा दक्षिणी ध्रुव बनकर चुंबक को खींच लेता।",
                    "मान लीजिए प्लस होता: पास वाला सिरा = S → चुंबक को खींचता"),
        "runaway": ("चुंबक तेज़ होता, धारा बढ़ती, खिंचाव बढ़ता। बिना कुछ किए, अनंत ऊर्जा!",
                    "चुंबक तेज़ → धारा ज़्यादा → खिंचाव ज़्यादा → मुफ़्त में अनंत ऊर्जा!"),
        "never":   ("यह ऊर्जा संरक्षण के नियम को तोड़ देता। इसलिए प्रेरित धारा को परिवर्तन का विरोध करना ही होगा।",
                    "असंभव: यह ऊर्जा संरक्षण तोड़ता। प्रेरित धारा परिवर्तन का विरोध करती है"),
        "math":    ("यही विरोध है वह माइनस चिह्न। यही है लेंज़ का नियम।",
                    "यही विरोध = माइनस चिह्न → लेंज़ का नियम: ε = −dΦ/dt"),
        "end":     ("और ऐसे ही व्हाई वीडियो के लिए सी बी एस ई मॉक को फ़ॉलो करें।",
                    "और WHY? वीडियो के लिए @cbsemock को फ़ॉलो करें"),
    },
    "caption": """🧲 WHY? (हिंदी) — ε = −dΦ/dt में माइनस चिह्न क्यों होता है?

दंड चुंबक का N ध्रुव कुंडली की ओर धकेलिए → फ्लक्स बढ़ता है → धारा बहती है ⚡
कुंडली का पास वाला सिरा N ध्रुव बनता है → चुंबक को प्रतिकर्षित करता है
इसलिए धकेलने में ज़ोर लगता है → आपका कार्य बल्ब की विद्युत ऊर्जा बनता है 💡

🤔 अगर प्लस होता, तो कुंडली चुंबक को खींचती…
चुंबक तेज़ → धारा ज़्यादा → खिंचाव ज़्यादा → बिना कुछ किए ऊर्जा ❌
यह ऊर्जा संरक्षण के नियम के विरुद्ध है!

✅ लेंज़ का नियम: प्रेरित धारा हमेशा फ्लक्स के परिवर्तन का विरोध करती है — यही है माइनस चिह्न।
वैद्युतचुंबकीय प्रेरण — कक्षा 12 भौतिकी। 📘

💾 सेव करें · 📤 अपने दोस्तों के साथ शेयर करें

🌐 फ्री नोट्स और मॉक पेपर → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #HindiMedium #Class12Physics #LenzsLaw #BoardExam2027""",
}
