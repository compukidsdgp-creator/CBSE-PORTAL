# Mistake Bank #01 — the locked reference reel (custom "molecules" scene).
REEL = {
    "id": "class10-chemistry-subscripts",
    "number": 1,
    "subject_key": "class10/science", "chapter": 1, "chapter_title": "Chemical Reactions and Equations",
    "notes": "notes/class-10/science/chemical-reactions-and-equations.html",
    "scene": {"type": "molecules"},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Changing subscripts to balance",
            "stamp": ("WRONG", "H₂O₂ is hydrogen peroxide,<br>not water!"),
            "rule": ("Subscripts = what it is", "Coefficients = how many"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "beats": [   # (key, narration, caption shown on screen)
                ("intro", "Top board exam mistake, number one!", "Top board-exam mistakes · #1"),
                ("hook", "Never change subscripts to balance!", "Never change subscripts to balance!"),
                ("setup", "H two, plus O two, gives H two O. Oxygen doesn't balance.", "H₂ + O₂ → H₂O … oxygen doesn't balance"),
                ("wrong", "Make it H two O two? Wrong! That's hydrogen peroxide.", "Make it H₂O₂? WRONG — that's hydrogen peroxide!"),
                ("right", "Change only coefficients. Two H two, plus O two, gives two H two O.", "Change only coefficients: 2H₂ + O₂ → 2H₂O"),
                ("done", "Now it's balanced!", "Balanced ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "बैलेंस करने के लिए subscript बदलना",
            "stamp": ("गलत!", "H₂O₂ हाइड्रोजन पेरोक्साइड है,<br>पानी नहीं!"),
            "rule": ("Subscript = पहचान (क्या है)", "Coefficient = संख्या (कितने)"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर वन!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #1"),
                ("hook", "बैलेंस करते समय सबस्क्रिप्ट कभी मत बदलो!", "बैलेंस के लिए subscript कभी मत बदलो!"),
                ("setup", "एच टू प्लस ओ टू से एच टू ओ बनता है। लेकिन ऑक्सीजन बैलेंस नहीं है।", "H₂ + O₂ → H₂O … ऑक्सीजन बैलेंस नहीं"),
                ("wrong", "तो क्या एच टू ओ टू बना दें? बिल्कुल गलत! ये तो हाइड्रोजन पेरोक्साइड है।", "H₂O₂ बना दिया? गलत — ये हाइड्रोजन पेरोक्साइड है!"),
                ("right", "सिर्फ़ आगे का नंबर बदलो। टू एच टू, प्लस ओ टू, टू एच टू ओ।", "सिर्फ़ आगे का नंबर (coefficient) बदलो: 2H₂ + O₂ → 2H₂O"),
                ("done", "अब बैलेंस्ड!", "बैलेंस ✓"),
            ],
        },
    },
}


# ── audio ────────────────────────────────────────────────────────────────────
def tone(freq, dur, vol=0.25, kind="sine", decay=8.0):
    t = np.arange(int(dur * SR)) / SR
    if kind == "buzz":
        w = np.sign(np.sin(2 * np.pi * freq * t)) * 0.5 + np.sin(2 * np.pi * freq * 1.5 * t) * 0.5
    elif kind == "sweep":
        f = np.linspace(freq, freq * 3, len(t))
        w = np.sin(2 * np.pi * np.cumsum(f) / SR)
    else:
        w = np.sin(2 * np.pi * freq * t)
    return (w * np.exp(-decay * t) * vol).astype(np.float32)


def sfx_at(track, t, clip):
    i = int(t * SR)
    j = min(len(track), i + len(clip))
    track[i:j] += clip[: j - i]
