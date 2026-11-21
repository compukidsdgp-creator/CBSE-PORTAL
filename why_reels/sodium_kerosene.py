"""WHY? — Why is sodium stored in kerosene but phosphorus in water?  (Class 10 Science · Metals and Non-metals)"""
import math
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, ORANGE, NAVY, WHITE, LTGREY, GREY

# densities in g/cm³ at room temperature (sodium 0.968, white phosphorus 1.82, water 1.00, kerosene ~0.80)
RHO = {"Na": 0.968, "P": 1.82, "water": 1.00, "kerosene": 0.80}
NA_SINKS = RHO["Na"] > RHO["kerosene"]
P_SINKS = RHO["P"] > RHO["water"]
assert NA_SINKS and P_SINKS
NA_TXT = f"Na {RHO['Na']:.2f} > kerosene {RHO['kerosene']:.2f} g/cm³ → sinks"
P_TXT = f"P {RHO['P']:.2f} > water {RHO['water']:.2f} g/cm³ → sinks"

TITLE = "Why sodium in KEROSENE, phosphorus in WATER?"
TAGS = "Class 10 Science"
PLAN_RANK = 2
END_Y = 0.393
BEATS = [
    ("hook",    "Sodium is kept in kerosene, phosphorus in water. Why not the same liquid?",
                "Sodium → KEROSENE. Phosphorus → WATER. Why not the same liquid?", 4.2),
    ("air",     "Both are so reactive they catch fire in open air. So keep them away from oxygen.",
                "Both are so reactive they catch FIRE in open air → keep oxygen away!", 5.0),
    ("nawater", "But sodium reacts violently with water, giving hydrogen and so much heat that it can catch fire.",
                "Sodium + WATER: violent reaction → H₂ + heat → the H₂ can catch fire!", 5.6),
    ("kero",    "Kerosene has no water and doesn't react with sodium. Sodium sinks in it, away from air.",
                "Kerosene: no water, no reaction. Sodium SINKS in it, sealed from air.", 5.0),
    ("pwater",  "Phosphorus doesn't react with water, and doesn't dissolve in it.",
                "Phosphorus does NOT react with water, and does NOT dissolve in it.", 4.4),
    ("sinks",   "It is heavier than water, so it sinks. The water keeps the oxygen away.",
                "Heavier than water → it SINKS. The water keeps the OXYGEN away.", 4.4),
    ("math",    "Rule: store it under a liquid it can't react with. Kerosene for sodium, water for phosphorus.",
                "Rule: store it under a liquid it CAN'T react with.", 5.2),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🧪 WHY? — Why is sodium stored in KEROSENE but phosphorus in WATER?

Both are so reactive they catch fire in open air 🔥 → both must be kept away from oxygen.
Sodium + water → violent reaction: 2Na + 2H₂O → 2NaOH + H₂ + heat (the H₂ can catch fire!) ❌
So sodium goes under kerosene: no water, no reaction, and Na sinks in it ✅
Phosphorus does NOT react with water and doesn't dissolve in it → it sinks, and the water keeps O₂ away 💧

Rule: store it under a liquid it CAN'T react with.
Metals and Non-metals — Class 10 Science. 📘

💾 Save it · 📤 Share with your science group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Chemistry #MetalsAndNonMetals #Class10Science #BoardExam2027 #CBSE #ScienceFacts"""

# ── picture labels in the reel's language (the Hindi build sets lang = "hi" in why_kit's G) ──
HI_LABELS = {
    "kerosene": "केरोसिन", "water": "पानी", "open air → catches FIRE": "खुली हवा → आग!",
    "Na in water?": "Na पानी में?", "2Na + 2H₂O → 2NaOH + H₂ + heat": "2Na + 2H₂O → 2NaOH + H₂ + ऊष्मा", "H₂ + heat": "H₂ + ऊष्मा",
    NA_TXT: f"Na {RHO['Na']:.2f} > केरोसिन {RHO['kerosene']:.2f} g/cm³ → डूबता है",
    "no reaction · does not dissolve": "अभिक्रिया नहीं · घुलता नहीं",
    "liquid lid: O₂ can't reach": "द्रव का ढक्कन: O₂ नहीं पहुँचती",
    P_TXT: f"P {RHO['P']:.2f} > पानी {RHO['water']:.2f} g/cm³ → डूबता है",
    "no reaction · no air": "अभिक्रिया नहीं · हवा नहीं",
    "store it under a liquid it can't react with": "ऐसे द्रव में रखो जिससे अभिक्रिया न हो",
    "Na → kerosene  ·  P → water": "Na → केरोसिन  ·  P → पानी",
}


def _lang():
    import sys
    for name in ("__main__", "why_kit"):
        g = getattr(sys.modules.get(name), "G", None)
        if g and "lang" in g:
            return g["lang"]
    return "en"


def L(s):
    return HI_LABELS.get(s, s) if _lang() == "hi" else s


def _hindi_fonts():
    """Devanagari fallback after the house Latin font (matplotlib ≥ 3.11 shapes Devanagari)."""
    import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    from pathlib import Path
    f = Path(__file__).resolve().parent.parent / "assets" / "fonts" / "NotoSansDevanagari-Bold.ttf"
    if "CBSEMock Deva" not in {x.name for x in fm.fontManager.ttflist}:
        fm.fontManager.addfont(str(f))
    fam = list(plt.rcParams["font.family"])
    if "CBSEMock Deva" not in fam:
        plt.rcParams["font.family"] = fam[:1] + ["CBSEMock Deva"] + fam[1:]


LX, RX = -1.85, 1.85            # jar centres
JW, JB, JT = 2.3, -2.25, 0.35   # jar width, bottom, top
FULL = 0.0                      # liquid level when full
KERO = "#d9a441"
WATER = "#2a8fdb"
rng = np.random.default_rng(5)
O2 = np.c_[rng.uniform(-3.1, 3.1, 22), rng.uniform(0.8, 2.1, 22), rng.uniform(0, 1, 22)]


def jar(dax, x, a):
    if a <= 0:
        return
    xs = [x - JW / 2, x - JW / 2, x + JW / 2, x + JW / 2]
    ys = [JT, JB, JB, JT]
    dax.plot(xs, ys, color=LTGREY, lw=4, alpha=a, zorder=7, solid_joinstyle="round")


def liquid(dax, x, level, col, a):
    if a <= 0 or level <= JB:
        return
    dax.add_patch(Rectangle((x - JW / 2 + 0.05, JB + 0.04), JW - 0.1, level - JB - 0.04, facecolor=col,
                            edgecolor="none", alpha=0.42 * a, zorder=3))
    dax.plot([x - JW / 2 + 0.05, x + JW / 2 - 0.05], [level, level], color=col, lw=3, alpha=a, zorder=4)


def sodium(dax, x, y, a):
    dax.add_patch(FancyBboxPatch((x - 0.32, y), 0.64, 0.5, boxstyle="round,pad=0,rounding_size=0.06",
                                 facecolor="#c9ced6", edgecolor="#8a94a3", lw=2.5, alpha=a, zorder=5))
    outline(dax.text(x, y + 0.25, "Na", ha="center", va="center", fontsize=24, fontweight="bold", color=NAVY,
                     alpha=a, zorder=6), w=0)


def phos(dax, x, y, a):
    dax.add_patch(FancyBboxPatch((x - 0.45, y), 0.9, 0.36, boxstyle="round,pad=0,rounding_size=0.16",
                                 facecolor="#f3ecc8", edgecolor="#b9ad72", lw=2.5, alpha=a, zorder=5))
    outline(dax.text(x, y + 0.18, "P", ha="center", va="center", fontsize=24, fontweight="bold", color=NAVY,
                     alpha=a, zorder=6), w=0)


def flame(dax, x, y, s, a, t):
    if a <= 0:
        return
    f = 1 + 0.12 * math.sin(t * 17 + x * 3)
    for col, k in ((ORANGE, 1.0), (GOLD, 0.55)):
        h, w = 0.9 * s * k * f, 0.42 * s * k
        pts = [(x - w, y), (x - w * 0.6, y + h * 0.45), (x, y + h), (x + w * 0.6, y + h * 0.45), (x + w, y)]
        dax.add_patch(Polygon(pts, closed=True, facecolor=col, edgecolor="none", alpha=a, zorder=8))


def mark(dax, x, y, ok, a):
    if a <= 0:
        return
    if ok:
        dax.plot([x - 0.25, x - 0.05, x + 0.32], [y, y - 0.22, y + 0.3], color=GREEN, lw=7, alpha=a, zorder=9,
                 solid_capstyle="round", solid_joinstyle="round")
    else:
        for s in (1, -1):
            dax.plot([x - 0.25, x + 0.25], [y - 0.25 * s, y + 0.25 * s], color=PINK, lw=7, alpha=a, zorder=9,
                     solid_capstyle="round")


def label(dax, x, y, s, col, a, size=22):
    if a > 0:
        outline(dax.text(x, y, L(s), ha="center", va="center", fontsize=size, fontweight="bold", color=col,
                         alpha=a, zorder=10))


def draw(c):
    if _lang() == "hi":
        _hindi_fonts()
    dax = c.area(0.0, 0.1, 7.0)
    t = c.t
    a0 = ease(c.phase("hook", 0.0, 0.25))
    air = ease(c.phase("air", 0.0, 0.25))
    nw = ease(c.phase("nawater", 0.0, 0.3))
    ke = ease(c.phase("kero", 0.0, 0.35))
    pw = ease(c.phase("pwater", 0.0, 0.35))
    fin = ease(c.phase("math", 0.0, 0.3))

    jar(dax, LX, a0); jar(dax, RX, a0)
    na_y, p_y = JB + 0.08, JB + 0.08
    sodium(dax, LX, na_y, a0)
    phos(dax, RX, p_y, a0)

    # ── left jar: kerosene (hook) → empty (air) → water (what-if) → kerosene again ──
    if not c.at("air"):
        liquid(dax, LX, FULL, KERO, a0)
        liquid(dax, RX, FULL, WATER, a0)
        label(dax, LX, 0.85, "kerosene", KERO, a0)
        label(dax, RX, 0.85, "water", CYAN, a0)
        qa = ease(c.phase("hook", 0.45, 0.75))
        label(dax, 0, -0.9, "?", GOLD, qa, size=64)
    elif not c.at("nawater"):
        drain = 1 - air
        liquid(dax, LX, lerp(JB, FULL, drain), KERO, 1)
        liquid(dax, RX, lerp(JB, FULL, drain), WATER, 1)
        fa = ease(c.phase("air", 0.25, 0.5))
        flame(dax, LX, na_y + 0.5, 1.0, fa, t)
        flame(dax, RX, p_y + 0.36, 0.9, fa, t)
        for x, y, ph in O2:
            label(dax, x + 0.15 * math.sin(t * 2 + ph * 6), y + 0.1 * math.cos(t * 2.5 + ph * 6), "O₂", LTGREY,
                  fa * 0.9, size=18)
        label(dax, 0, 2.4, "open air → catches FIRE", ORANGE, ease(c.phase("air", 0.4, 0.65)), size=24)
    elif not c.at("kero"):
        # what if sodium were put in water?
        lvl = lerp(JB, FULL, ease(c.phase("nawater", 0.0, 0.3)))
        liquid(dax, LX, lvl, WATER, 1)
        rx = ease(c.phase("nawater", 0.25, 0.5))
        for k in range(14):
            f = (k / 14 + 0.9 * t) % 1.0
            bx = LX + 0.75 * math.sin(k * 2.3) * (0.3 + 0.7 * f)
            by = lerp(na_y + 0.5, lvl, f)
            dax.add_patch(Circle((bx, by), 0.06 + 0.05 * f, facecolor="none", edgecolor=WHITE, lw=1.8,
                                 alpha=rx * 0.9, zorder=6))
        flame(dax, LX, FULL, 1.1, ease(c.phase("nawater", 0.5, 0.7)), t)
        label(dax, LX, 1.75, "H₂ + heat", WHITE, rx, size=24)
        label(dax, LX, 2.3, "Na in water?", CYAN, nw, size=24)
        mark(dax, LX + 1.45, 2.3, False, ease(c.phase("nawater", 0.55, 0.75)))
        # the right jar waits, empty and dim
        liquid(dax, RX, JB, WATER, 0)
        ea = ease(c.phase("nawater", 0.3, 0.55))
        if ea > 0:
            c.text(0.5, 0.37, L("2Na + 2H₂O → 2NaOH + H₂ + heat"), size=34, color=PINK, alpha=ea, max_w=0.92)
    else:
        # left jar: kerosene, safe for good
        lvl_k = lerp(JB, FULL, ke) if not c.at("pwater") else FULL
        liquid(dax, LX, lvl_k, KERO, 1)
        ka = ke if not c.at("math") else 1
        label(dax, LX, 0.85, "kerosene", KERO, ka)
        mark(dax, LX, 1.6, True, ease(c.phase("kero", 0.4, 0.6)) if not c.at("pwater") else 1)
        if not c.at("pwater"):
            c.text(0.5, 0.37, L(NA_TXT), size=30, color=WHITE, alpha=ease(c.phase("kero", 0.45, 0.7)), max_w=0.92)
        # right jar: water
        if c.at("pwater"):
            lvl_w = lerp(JB, FULL, pw) if not c.at("sinks") else FULL
            liquid(dax, RX, lvl_w, WATER, 1)
            label(dax, RX, 0.85, "water", CYAN, pw if not c.at("sinks") else 1)
            if not c.at("sinks"):
                ta = ease(c.phase("pwater", 0.45, 0.7))
                c.text(0.5, 0.37, L("no reaction · does not dissolve"), size=30, color=CYAN, alpha=ta, max_w=0.92)
            mark(dax, RX, 1.6, True, ease(c.phase("pwater", 0.6, 0.8)) if not c.at("sinks") else 1)
        if c.at("sinks") and not c.at("math"):
            sa = ease(c.phase("sinks", 0.0, 0.25))
            # oxygen falls on both surfaces and bounces off
            for k, (x0, y0, ph) in enumerate(O2[:10]):
                x = (LX if k % 2 == 0 else RX) + (k // 2 - 2) * 0.44
                f = (k * 0.37 + 0.55 * t) % 1.0
                y = FULL + 0.14 + 0.42 * abs(1 - 2 * f)
                label(dax, x, y, "O₂", LTGREY, sa * 0.9, size=18)
            label(dax, 0, 2.4, "liquid lid: O₂ can't reach", WHITE, ease(c.phase("sinks", 0.15, 0.4)), size=24)
            c.text(0.5, 0.37, L(P_TXT), size=30, color=WHITE, alpha=ease(c.phase("sinks", 0.3, 0.55)), max_w=0.92)
        if c.at("math"):
            label(dax, 0, 2.4, "no reaction · no air", GREEN, fin, size=26)

    c.steps([(L("store it under a liquid it can't react with"), 0.05, WHITE),
             (L("Na → kerosene  ·  P → water"), 0.45, GOLD)], ys=(0.330, 0.270), beat="math")


# ── Hindi version (posted in the 8 PM slot; voice: Indic Parler-TTS "rohit") ──
HINDI = {
    "title": "Na केरोसिन, P पानी में क्यों?",
    "end_text": "और WHY? वीडियो के लिए फ़ॉलो करें",
    "beats": {
        "hook":    ("सोडियम को केरोसिन में रखते हैं, और फ़ॉस्फ़ोरस को पानी में। एक ही द्रव में क्यों नहीं?",
                    "सोडियम → केरोसिन, फ़ॉस्फ़ोरस → पानी। एक ही द्रव क्यों नहीं?"),
        "air":     ("दोनों इतने अभिक्रियाशील हैं कि हवा में आग पकड़ लेते हैं। इन्हें ऑक्सीजन से दूर रखना है।",
                    "दोनों खुली हवा में आग पकड़ लेते हैं → ऑक्सीजन से दूर रखो!"),
        "nawater": ("पर सोडियम पानी से तेज़ अभिक्रिया करता है। हाइड्रोजन और इतनी ऊष्मा बनती है कि आग लग जाए।",
                    "सोडियम + पानी: तीव्र अभिक्रिया → H₂ + ऊष्मा → आग लग सकती है!"),
        "kero":    ("केरोसिन में पानी नहीं होता, और यह सोडियम से अभिक्रिया नहीं करता। सोडियम इसमें डूबा रहता है।",
                    "केरोसिन: पानी नहीं, अभिक्रिया नहीं। सोडियम डूबा रहता है।"),
        "pwater":  ("फ़ॉस्फ़ोरस अलग है। यह पानी से अभिक्रिया नहीं करता, और पानी में घुलता भी नहीं।",
                    "फ़ॉस्फ़ोरस पानी से अभिक्रिया नहीं करता, घुलता भी नहीं।"),
        "sinks":   ("यह पानी से भारी है, इसलिए नीचे डूब जाता है। पानी ऑक्सीजन को इस तक पहुँचने नहीं देता।",
                    "पानी से भारी → डूब जाता है। पानी ऑक्सीजन को रोकता है।"),
        "math":    ("नियम: उसे ऐसे द्रव में रखो जिससे वह अभिक्रिया न करे। सोडियम केरोसिन में, फ़ॉस्फ़ोरस पानी में।",
                    "नियम: ऐसे द्रव में रखो जिससे अभिक्रिया न हो।"),
        "end":     ("और ऐसे ही व्हाई वीडियो के लिए सी बी एस ई मॉक को फ़ॉलो करें।",
                    "और WHY? वीडियो के लिए @cbsemock को फ़ॉलो करें"),
    },
    "caption": """🧪 WHY? (हिंदी) — सोडियम केरोसिन में और फ़ॉस्फ़ोरस पानी में क्यों रखा जाता है?

दोनों इतने अभिक्रियाशील हैं कि खुली हवा में आग पकड़ लेते हैं 🔥 → ऑक्सीजन से दूर रखना ज़रूरी।
सोडियम + पानी → तीव्र अभिक्रिया: 2Na + 2H₂O → 2NaOH + H₂ + ऊष्मा (H₂ आग पकड़ सकती है!) ❌
इसलिए सोडियम केरोसिन में: पानी नहीं, अभिक्रिया नहीं, और Na उसमें डूबा रहता है ✅
फ़ॉस्फ़ोरस पानी से अभिक्रिया नहीं करता, घुलता भी नहीं → डूबा रहता है, पानी O₂ को रोकता है 💧

नियम: ऐसे द्रव में रखो जिससे अभिक्रिया न हो।
धातु एवं अधातु — कक्षा 10 विज्ञान। 📘

💾 सेव करें · 📤 अपने साइंस ग्रुप में शेयर करें

🌐 फ्री नोट्स और मॉक पेपर → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #HindiMedium #Class10Science #MetalsAndNonMetals #BoardExam2027""",
}
