# Mistake Bank #10 — generic "flip" scene.
_INK = "#0f172a"


def _svg(body):
    return '<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">' + body + '</svg>'


def _jar(x, name, formula, col, mark):
    """A labelled jar, 380 wide, starting at x."""
    return (f'<rect x="{x + 40}" y="20" width="300" height="26" rx="8" fill="#94a3b8"/>'
            f'<rect x="{x}" y="46" width="380" height="176" rx="24" fill="#fff" stroke="{col}" stroke-width="6"/>'
            f'<text x="{x + 190}" y="104" text-anchor="middle" font-size="36" font-weight="800" fill="{_INK}">{name}</text>'
            f'<text x="{x + 190}" y="170" text-anchor="middle" font-size="40" font-weight="800" fill="{col}">{formula}</text>'
            f'<text x="{x + 350}" y="88" text-anchor="middle" font-size="40" font-weight="800" fill="{col}">{mark}</text>')


# front: formulas swapped (the mistake)
SODA_SVG_WRONG = _svg(_jar(40, "Baking soda", "Na₂CO₃", "#dc2626", "✕") + _jar(540, "Washing soda", "NaHCO₃", "#dc2626", "✕"))
# back: correct formulas
SODA_SVG_RIGHT = _svg(_jar(40, "Baking soda", "NaHCO₃", "#15803d", "✓") + _jar(540, "Washing soda", "Na₂CO₃·10H₂O", "#15803d", "✓"))

REEL = {
    "id": "class10-chemistry-baking-washing-soda",
    "number": 10,
    "subject_key": "class10/science", "chapter": 2, "chapter_title": "Acids, Bases and Salts",
    "notes": "notes/class-10/science/acids-bases-and-salts.html",
    "scene": {"type": "flip", "svg_wrong": SODA_SVG_WRONG, "svg_right": SODA_SVG_RIGHT},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Mixing up baking soda and washing soda",
            "stamp": ("WRONG", "The formulas<br>are swapped!"),
            "rule": ("Baking soda = NaHCO₃", "Washing soda = Na₂CO₃·10H₂O"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "scene": {"q": "Formulas of baking soda and washing soda?",
                      "wrong": "Baking soda <s>Na₂CO₃</s><br>Washing soda <s>NaHCO₃</s>",
                      "right": "Baking soda <mark>NaHCO₃</mark><br>Washing soda Na₂CO₃·10H₂O",
                      "wrong_label": "What students write", "right_label": "Write this instead"},
            "beats": [
                ("intro", "Top board exam mistake, number ten!", "Top board-exam mistakes · #10"),
                ("hook", "Swapping baking and washing soda!", "Swapping baking soda and washing soda!"),
                ("setup", "Write both formulas.", "Write both formulas"),
                ("wrong", "Baking soda, N A two C O three? Wrong!", "“Baking soda = Na₂CO₃” — WRONG!"),
                ("right", "Baking soda is N A H C O three. Washing soda, N A two C O three, ten H two O.",
                 "Baking soda NaHCO₃ · Washing soda Na₂CO₃·10H₂O"),
                ("done", "Baking soda is the hydrogencarbonate!", "Baking soda = sodium hydrogencarbonate ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "बेकिंग सोडा और वॉशिंग सोडा में कन्फ़्यूज़न",
            "stamp": ("गलत!", "फ़ॉर्मूले उल्टे<br>लिख दिए!"),
            "rule": ("बेकिंग सोडा = NaHCO₃", "वॉशिंग सोडा = Na₂CO₃·10H₂O"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "scene": {"q": "बेकिंग सोडा और वॉशिंग सोडा के फ़ॉर्मूले?",
                      "wrong": "बेकिंग सोडा <s>Na₂CO₃</s><br>वॉशिंग सोडा <s>NaHCO₃</s>",
                      "right": "बेकिंग सोडा <mark>NaHCO₃</mark><br>वॉशिंग सोडा Na₂CO₃·10H₂O",
                      "wrong_label": "स्टूडेंट्स लिखते हैं", "right_label": "ऐसे लिखो"},
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर टेन!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #10"),
                ("hook", "बेकिंग सोडा और वॉशिंग सोडा की अदला-बदली!", "बेकिंग सोडा और वॉशिंग सोडा की अदला-बदली!"),
                ("setup", "दोनों के फ़ॉर्मूले लिखो।", "दोनों के फ़ॉर्मूले लिखो"),
                ("wrong", "बेकिंग सोडा, एन ए टू सी ओ थ्री? गलत!", "“बेकिंग सोडा = Na₂CO₃” — गलत!"),
                ("right", "बेकिंग सोडा, एन ए एच सी ओ थ्री। वॉशिंग सोडा, एन ए टू सी ओ थ्री, टेन एच टू ओ।",
                 "बेकिंग सोडा NaHCO₃ · वॉशिंग सोडा Na₂CO₃·10H₂O"),
                ("done", "बेकिंग सोडा यानी सोडियम हाइड्रोजन कार्बोनेट!", "बेकिंग सोडा = सोडियम हाइड्रोजनकार्बोनेट ✓"),
            ],
        },
    },
}
