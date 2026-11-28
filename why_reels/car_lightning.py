"""WHY? — Why is a car a safe place in a lightning storm?  (Class 12 Physics · Electrostatic Potential and Capacitance)
Follows NCERT Class 12 Physics Part I, Ch. 2, 'Electrostatics of conductors': E = 0 inside a conductor, charge resides
on the outer surface, and the field inside a charge-free cavity of a conductor is zero — electrostatic shielding.
Framing fixed from the plan title ('the SAFEST place'): a hard-topped metal car is a SAFE place (a Faraday cage);
it is not claimed to be safer than every building. The rubber-tyre explanation is a myth and is called out as one."""
import math
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Polygon
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, ORANGE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why is a CAR safe in LIGHTNING?"
TAGS = "Class 12 Physics"
PLAN_RANK = 5
END_Y = 0.252
BEATS = [
    ("hook",   "Lightning hits a car, but the people inside are safe. Why?",
               "Lightning hits a car… but the people inside are SAFE. Why?", 3.8),
    ("myth",   "Rubber tyres? No! The bolt just crossed kilometres of air.",
               "The rubber tyres? NO — the bolt just crossed KILOMETRES of air!", 4.4),
    ("shell",  "The real hero is the metal body, a hollow conductor around you.",
               "The real hero: the METAL body — a hollow conductor around you.", 4.0),
    ("strike", "When lightning strikes, charge spreads over the outer surface.",
               "Lightning strikes → charge spreads over the OUTER surface.", 4.2),
    ("flow",   "It races around the outside, and jumps to the ground.",
               "It races AROUND the outside → and jumps to the ground.", 4.0),
    ("gauss",  "Field in the metal is zero, so Gauss's law leaves no charge inside. The cabin feels no field.",
               "E = 0 in the metal → Gauss's law: no charge inside → E = 0 in the cabin.", 5.2),
    ("shield", "This is electrostatic shielding, a Faraday cage. Keep windows shut, hands off metal.",
               "Electrostatic SHIELDING: a Faraday cage. Windows shut, hands off metal.", 5.0),
    ("math",   "Field inside a hollow conductor is zero. A favourite board question.",
               "Inside a hollow conductor, E = 0 → a favourite board question!", 4.0),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """⚡ WHY? — Why is a car a SAFE place when lightning strikes?

❌ Not the rubber tyres — the bolt has just crossed kilometres of air!
✅ The METAL body is a hollow conductor around you.

Lightning hits → charge spreads over the OUTER surface → flows around the body → jumps to the ground 🌩️
E = 0 inside the metal → Gauss's law: no charge on the inside → E = 0 in the cabin.

That's electrostatic shielding — the car is a Faraday cage. 🚗
(Hard metal roof only · windows shut · don't touch metal parts.)

Electrostatics of Conductors — Class 12 Physics. 📘

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Electrostatics #FaradayCage #GaussLaw #Class12Physics #BoardExam2027 #CBSE"""

# ── geometry (drawing units; c.area(0, 0, 7) shows x −3.5…3.5, y −2.64…2.64) ──
GROUND = -1.92
STRIKE = (0.05, 0.55)                                  # where the bolt hits the roof
BODY = np.array([STRIKE, (0.75, 0.55), (1.30, -0.22), (2.20, -0.32), (2.55, -0.55), (2.55, -1.30),
                 (-2.55, -1.30), (-2.55, -0.45), (-1.80, -0.25), (-1.15, 0.55)])   # starts at the strike point
WIN_F = [(0.18, 0.40), (0.62, 0.40), (1.02, -0.20), (0.18, -0.20)]
WIN_R = [(-0.08, 0.40), (-1.03, 0.40), (-1.52, -0.20), (-0.08, -0.20)]
WHEELS = [(-1.55, -1.42), (1.55, -1.42)]
R_WHEEL = 0.45
BOLT = [(0.55, 2.05), (0.15, 1.65), (0.50, 1.35), (0.0, 0.95), (0.25, 0.80), STRIKE]
CLOUD = [(-0.6, 2.25, 0.48), (0.05, 2.38, 0.58), (0.75, 2.30, 0.52), (1.35, 2.18, 0.40), (-1.05, 2.12, 0.36)]

SEG = np.r_[0, np.cumsum(np.hypot(*np.diff(np.vstack([BODY, BODY[:1]]), axis=0).T))]
PERIM = SEG[-1]


def on_body(u):
    """Point on the car's outline at signed fraction u ∈ [−0.5, 0.5] of the perimeter from the strike point."""
    s = (u % 1.0) * PERIM
    i = min(int(np.searchsorted(SEG, s, side="right")) - 1, len(BODY) - 1)
    p, q = BODY[i], BODY[(i + 1) % len(BODY)]
    f = (s - SEG[i]) / max(1e-9, SEG[i + 1] - SEG[i])
    return p + (q - p) * f


EXIT = on_body(0.5)                                    # the point opposite the strike: where charge leaves
assert abs(EXIT[1] - (-1.30)) < 1e-9 and abs(EXIT[0]) < 1.0, EXIT    # it lies on the underside, between the wheels
N_Q = 30


def shrink(pts, k=0.86, cy=-0.38):
    """The outline scaled towards the cabin centre: a Gaussian surface drawn just inside the metal."""
    c = np.array([0.0, cy])
    return c + (np.asarray(pts) - c) * k


def arrow(dax, p, q, col, a, lw=4, z=9, ms=26):
    if a > 0.01:
        dax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, color=col, lw=lw, alpha=min(1, a), zorder=z))


def label(dax, x, y, s, col, a, size=22, ha="center", va="center"):
    if a > 0.01:
        outline(dax.text(x, y, s, color=col, fontsize=size, fontweight="bold", ha=ha, va=va, alpha=min(1, a), zorder=12))


def bolt(dax, pts, a, t, lw=7):
    if a <= 0.01:
        return
    xs, ys = zip(*pts)
    fl = 0.75 + 0.25 * math.sin(t * 41)
    dax.plot(xs, ys, color=GOLD, lw=lw * 2.4, alpha=0.25 * a * fl, zorder=7, solid_joinstyle="miter")
    dax.plot(xs, ys, color="#fff6c8", lw=lw, alpha=a * fl, zorder=8, solid_joinstyle="miter")


def draw(c):
    dax = c.area(0.0, 0.10, 7.0)
    t = c.t
    a0 = ease(c.phase("hook", 0.05, 0.35))

    # storm cloud + ground
    for x, y, r in CLOUD:
        dax.add_patch(Circle((x, y), r, color="#3a4766", alpha=a0, zorder=2))
    dax.plot([-3.4, 3.4], [GROUND, GROUND], color="#6b5a3a", lw=5, alpha=a0, zorder=2)

    # the bolt: hits in the hook, flashes again during strike / flow
    hb = ease(c.phase("hook", 0.15, 0.4)) * (1 - ease(c.phase("hook", 0.75, 1.0)))
    sb = ease(c.phase("strike", 0.0, 0.15)) * (1 - ease(c.phase("flow", 0.6, 0.9)))
    bolt(dax, BOLT, max(hb, sb), t)

    # car body (metal shell), windows, wheels, passenger
    shell = ease(c.phase("shell", 0.05, 0.4))
    metal = "#8090a8"
    dax.add_patch(Polygon(BODY, closed=True, facecolor="#24324f", edgecolor="none", alpha=a0, zorder=3))
    for w in (WIN_F, WIN_R):
        dax.add_patch(Polygon(w, closed=True, facecolor="#0d1a33", edgecolor="#5a6f96", lw=2, alpha=a0, zorder=4))
    pulse = 0.6 + 0.4 * math.sin(t * 6) if (c.at("shell") and not c.at("strike")) else 1.0
    edge_col = CYAN if c.at("shell") else metal
    dax.add_patch(Polygon(BODY, closed=True, facecolor="none", edgecolor=edge_col,
                          lw=6 + 4 * shell * (pulse if not c.at("strike") else 0.6), alpha=a0, zorder=6))
    # passenger (head + shoulders) behind the front window
    dax.add_patch(Circle((0.45, 0.05), 0.20, color="#f2c28b", alpha=a0, zorder=5))
    dax.add_patch(Ellipse((0.45, -0.38), 0.62, 0.44, color="#e2475b", alpha=a0, zorder=5))

    myth = ease(c.phase("myth", 0.05, 0.3)) * (1 - ease(c.phase("shell", 0.0, 0.2)))
    for (wx, wy) in WHEELS:
        dax.add_patch(Circle((wx, wy), R_WHEEL, color="#141a26", alpha=a0, zorder=6))
        dax.add_patch(Circle((wx, wy), R_WHEEL, facecolor="none", edgecolor="#ff3b5c", lw=6, alpha=a0 * myth, zorder=7))
        dax.add_patch(Circle((wx, wy), 0.18, color="#7d889c", alpha=a0, zorder=7))

    # beat 2: the tyre myth, against the km of air
    if myth > 0.01:
        label(dax, 0, -2.35, "rubber tyres?", "#ff6b81", myth, size=24)
        xs = ease(c.phase("myth", 0.3, 0.5))
        for (wx, wy) in WHEELS:
            k = 0.32 * back_out(xs)
            for s in (1, -1):
                dax.plot([wx - k, wx + k], [wy - s * k, wy + s * k], color="#ff3b5c", lw=7, alpha=myth * min(1, xs),
                         zorder=8, solid_capstyle="round")
        ka = ease(c.phase("myth", 0.5, 0.75))
        arrow(dax, (-2.85, 1.85), (-2.85, GROUND + 0.05), GOLD, myth * ka, lw=3)
        arrow(dax, (-2.85, GROUND + 0.05), (-2.85, 1.85), GOLD, myth * ka, lw=3)
        label(dax, -2.0, 1.25, "kilometres\nof air", GOLD, myth * ka, size=21)
        label(dax, 2.05, 1.25, "a few cm\nof rubber?", "#ff6b81", myth * ka, size=21)

    sh = ease(c.phase("shell", 0.3, 0.6)) * (1 - ease(c.phase("strike", 0.0, 0.2)))
    label(dax, -1.9, 1.15, "metal shell =\nhollow conductor", CYAN, sh, size=21)

    # beats 4–5: charge on the OUTER surface, flowing round to the ground
    if c.at("strike") and not c.at("math"):
        spread = ease(c.phase("strike", 0.1, 0.8))
        fade = 1 - ease(c.phase("gauss", 0.55, 0.85))
        flow = c.phase("flow", 0.0, 1.0) if c.at("flow") else 0.0
        for k in range(N_Q):
            u0 = (k + 0.5) / N_Q - 0.5                 # −0.5 … 0.5 around the shell
            if abs(u0) > 0.5 * spread:
                continue
            u = u0
            if c.at("flow"):                         # drift away from the strike towards the exit point
                d = (abs(u0) + 0.35 * (t - c.beat("flow")["start"])) % 0.5
                u = math.copysign(d, u0)
            p = on_body(u)
            n = p - np.array([0.0, -0.38])
            p = p + 0.10 * n / max(1e-9, np.hypot(*n))                   # just OUTSIDE the metal
            dax.add_patch(Circle(p, 0.075, color=GOLD, alpha=fade, zorder=9))
        label(dax, 1.95, 1.15, "charge stays\nOUTSIDE", GOLD,
              ease(c.phase("strike", 0.35, 0.65)) * (1 - ease(c.phase("gauss", 0.0, 0.2))), size=21)
        if c.at("flow") and not c.at("gauss"):
            jp = ease(c.phase("flow", 0.25, 0.45))
            jag = [tuple(EXIT), (EXIT[0] + 0.12, -1.48), (EXIT[0] - 0.10, -1.66), (EXIT[0] + 0.08, -1.80), (EXIT[0], GROUND)]
            bolt(dax, jag, jp, t, lw=5)
            label(dax, 0, -2.35, "→ to the ground", GOLD, jp, size=22)

    # beat 6: field outside, none inside; Gaussian surface in the metal
    ga = ease(c.phase("gauss", 0.0, 0.3)) * (1 - ease(c.phase("end", 0.0, 0.3)))
    if ga > 0.01:
        for x in (-3.15, -2.75, 2.75, 3.15):
            arrow(dax, (x, 1.75), (x, GROUND + 0.08), PINK, ga * 0.9, lw=3, ms=22)
        for x in (-0.95, 0.05, 0.65):
            top = 0.55 if x > -1.1 else 0.0
            arrow(dax, (x, 1.75), (x, top + 0.12), PINK, ga * 0.9, lw=3, ms=22)
        label(dax, -2.95, 2.15, "E outside", PINK, ga, size=20)
        gs = ease(c.phase("gauss", 0.2, 0.5))
        if gs > 0.01:
            pts = shrink(BODY)
            xs, ys = np.r_[pts[:, 0], pts[0, 0]], np.r_[pts[:, 1], pts[0, 1]]
            dax.plot(xs, ys, color=WHITE, lw=2.5, ls=(0, (4, 3)), alpha=gs * ga * 0.9, zorder=10)
        ea = ease(c.phase("gauss", 0.45, 0.75)) * (1 - ease(c.phase("shield", 0.0, 0.2)))
        label(dax, 1.55, -0.85, "q inside = 0", WHITE, ea, size=20)
        za = ease(c.phase("gauss", 0.6, 0.9))
        if za > 0.01:
            outline(dax.text(-1.05, -0.72, "E = 0", color=GREEN, fontsize=30, fontweight="bold", ha="center",
                             va="center", alpha=za * ga, zorder=12), w=7)

    # beat 7: shielding / Faraday cage + safety tips
    fa = ease(c.phase("shield", 0.05, 0.3)) * (1 - ease(c.phase("math", 0.0, 0.2)))
    label(dax, 0, -2.35, "FARADAY CAGE", CYAN, fa, size=26)
    ta = ease(c.phase("shield", 0.45, 0.7)) * (1 - ease(c.phase("math", 0.0, 0.2)))
    label(dax, 1.95, 1.15, "windows shut\nhands off metal", WHITE, ta, size=20)

    # beat 8: the result
    ma = ease(c.phase("math", 0.0, 0.3)) * (1 - ease(c.phase("end", 0.0, 0.3)))
    label(dax, 0, -2.35, "SAFE INSIDE", GREEN, ma, size=28)

    c.steps([("charge on the OUTER surface only", 0.0, WHITE),
             ("hollow conductor: E inside = 0", 0.25, GOLD)], ys=(0.372, 0.312), beat="gauss")


# ── Hindi version (posted in the 8 PM slot; voice: Indic Parler-TTS "rohit") ──
HINDI = {
    "title": "तड़ित में कार सुरक्षित क्यों?",
    "end_text": "और WHY? वीडियो के लिए फ़ॉलो करें",
    "beats": {
        "hook":   ("कार पर बिजली गिरती है, पर अंदर बैठे लोग सुरक्षित रहते हैं। क्यों?",
                   "कार पर बिजली गिरी… फिर भी अंदर लोग सुरक्षित! क्यों?"),
        "myth":   ("रबर के टायर? नहीं! बिजली तो कई किलोमीटर हवा पार करके आई है।",
                   "रबर के टायर? नहीं — बिजली कई किलोमीटर हवा पार करके आई है!"),
        "shell":  ("असली रक्षक है धातु का ढाँचा, आपके चारों ओर एक खोखला चालक।",
                   "असली रक्षक: धातु का ढाँचा — चारों ओर एक खोखला चालक"),
        "strike": ("बिजली गिरते ही आवेश धातु की बाहरी सतह पर फैल जाता है।",
                   "बिजली गिरी → आवेश धातु की बाहरी सतह पर फैलता है"),
        "flow":   ("यह ढाँचे के बाहर-बाहर दौड़ता है, और ज़मीन में चला जाता है।",
                   "आवेश बाहर-बाहर दौड़ता है → और ज़मीन में चला जाता है"),
        "gauss":  ("धातु में क्षेत्र शून्य है, तो गाउस नियम से अंदर आवेश नहीं। केबिन में क्षेत्र नहीं।",
                   "धातु में E = 0 → गाउस नियम: अंदर आवेश नहीं → केबिन में E = 0"),
        "shield": ("इसे स्थिरवैद्युत परिरक्षण कहते हैं। कार एक फैराडे पिंजरा है। खिड़कियाँ बंद, धातु को न छुएँ।",
                   "स्थिरवैद्युत परिरक्षण = फैराडे पिंजरा"),
        "math":   ("खोखले चालक के अंदर विद्युत क्षेत्र शून्य होता है। बोर्ड का पसंदीदा प्रश्न।",
                   "खोखले चालक के अंदर E = 0 → बोर्ड का पसंदीदा प्रश्न!"),
        "end":    ("और ऐसे ही व्हाई वीडियो के लिए सी बी एस ई मॉक को फ़ॉलो करें।",
                   "और WHY? वीडियो के लिए @cbsemock को फ़ॉलो करें"),
    },
    "caption": """⚡ WHY? (हिंदी) — बिजली गिरने पर कार के अंदर हम सुरक्षित क्यों रहते हैं?

❌ रबर के टायर नहीं — बिजली तो कई किलोमीटर हवा पार करके आई है!
✅ कार का धातु का ढाँचा आपके चारों ओर एक खोखला चालक है।

बिजली गिरी → आवेश बाहरी सतह पर फैलता है → ढाँचे के बाहर-बाहर बहकर ज़मीन में चला जाता है 🌩️
धातु में E = 0 → गाउस का नियम: अंदर की सतह पर आवेश नहीं → केबिन में E = 0

यही है स्थिरवैद्युत परिरक्षण — कार एक फैराडे पिंजरा है। 🚗
(सिर्फ़ धातु की छत वाली कार · खिड़कियाँ बंद · धातु के हिस्से न छुएँ)

चालकों की स्थिरवैद्युतिकी — कक्षा 12 भौतिकी। 📘

💾 सेव करें · 📤 अपने दोस्तों के साथ शेयर करें

🌐 फ्री नोट्स और मॉक पेपर → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #HindiMedium #Class12Physics #FaradayCage #BoardExam2027""",
}
