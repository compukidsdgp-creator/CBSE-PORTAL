# Mistake Bank #08 — generic "flip" scene.
_ACID, _WATER, _INK = "#f59e0b", "#60a5fa", "#0f172a"


def _svg(body):
    return '<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">' + body + '</svg>'


def _beaker(liquid, label, col):
    """A beaker (x 380–580, rim y 70, base y 222) filled from y 130 with `col`."""
    return (f'<path d="M386 132 V214 Q386 222 394 222 H566 Q574 222 574 214 V132 Z" fill="{col}" opacity=".85"/>'
            '<path d="M372 70 H386 V214 Q386 222 394 222 H566 Q574 222 574 214 V70" fill="none" stroke="#334155" stroke-width="6" stroke-linejoin="round"/>'
            f'<text x="480" y="186" text-anchor="middle" font-size="30" font-weight="700" fill="{_INK}">{label}</text>')


# front: water poured into concentrated acid (the mistake)
ACID_SVG_WRONG = _svg(
    _beaker("acid", "conc. acid", _ACID)
    + '<path d="M250 20 C330 20 420 40 450 128" fill="none" stroke="#2563eb" stroke-width="12" stroke-linecap="round"/>'
    '<text x="150" y="34" text-anchor="middle" font-size="32" font-weight="700" fill="#2563eb">water</text>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#dc2626"/>' for x, y, r in
              [(420, 52, 8), (452, 34, 10), (500, 44, 9), (536, 26, 7), (560, 56, 8), (404, 24, 6)])
    + '<text x="760" y="110" text-anchor="middle" font-size="38" font-weight="800" fill="#dc2626">SPLASH!</text>'
    '<text x="760" y="154" text-anchor="middle" font-size="28" font-weight="700" fill="#b91c1c">sudden heat</text>')

# back: acid added slowly to water, with stirring
ACID_SVG_RIGHT = _svg(
    _beaker("water", "water", _WATER)
    + '<path d="M250 20 C330 20 420 40 450 128" fill="none" stroke="#f59e0b" stroke-width="5" stroke-linecap="round"/>'
    '<text x="150" y="34" text-anchor="middle" font-size="32" font-weight="700" fill="#b45309">acid</text>'
    '<path d="M610 18 L552 212" stroke="#94a3b8" stroke-width="9" stroke-linecap="round"/>'
    '<text x="770" y="110" text-anchor="middle" font-size="34" font-weight="800" fill="#15803d">slowly</text>'
    '<text x="770" y="154" text-anchor="middle" font-size="30" font-weight="700" fill="#15803d">+ keep stirring</text>')

REEL = {
    "id": "class10-chemistry-acid-to-water",
    "number": 8,
    "subject_key": "class10/science", "chapter": 2, "chapter_title": "Acids, Bases and Salts",
    "notes": "notes/class-10/science/acids-bases-and-salts.html",
    "scene": {"type": "flip", "svg_wrong": ACID_SVG_WRONG, "svg_right": ACID_SVG_RIGHT},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Adding water to concentrated acid",
            "stamp": ("WRONG", "It can splash out<br>and burn you!"),
            "rule": ("Add acid to water", "Never water to acid!"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "scene": {"q": "How do you dilute a concentrated acid?",
                      "wrong": "<s>Pour water into the acid</s>",
                      "right": "Add <mark>acid slowly to water</mark>, with constant stirring",
                      "wrong_label": "What students write", "right_label": "Write this instead"},
            "beats": [
                ("intro", "Top board exam mistake, number eight!", "Top board-exam mistakes · #8"),
                ("hook", "Adding water to concentrated acid!", "Adding water to concentrated acid!"),
                ("setup", "How do you dilute a concentrated acid?", "How do you dilute a concentrated acid?"),
                ("wrong", "Pour water into the acid? Wrong! It can splash out.", "“Pour water into the acid” — WRONG!"),
                ("right", "It's highly exothermic. Add acid slowly to water, stirring all the time.", "Highly exothermic → add acid slowly to water, stir"),
                ("done", "Always add acid to water!", "Acid → water ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "कंसन्ट्रेटेड एसिड में पानी डालना",
            "stamp": ("गलत!", "मिश्रण उछलकर<br>जला सकता है!"),
            "rule": ("एसिड को पानी में डालो", "पानी को एसिड में कभी नहीं!"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "scene": {"q": "कंसन्ट्रेटेड एसिड को डाइल्यूट कैसे करते हैं?",
                      "wrong": "<s>एसिड में पानी डालो</s>",
                      "right": "<mark>एसिड को धीरे-धीरे पानी में</mark> डालो, लगातार हिलाते हुए",
                      "wrong_label": "स्टूडेंट्स लिखते हैं", "right_label": "ऐसे लिखो"},
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर एट!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #8"),
                ("hook", "कंसन्ट्रेटेड एसिड में पानी डालना!", "कंसन्ट्रेटेड एसिड में पानी डालना!"),
                ("setup", "कंसन्ट्रेटेड एसिड को डाइल्यूट कैसे करते हैं?", "कंसन्ट्रेटेड एसिड को डाइल्यूट कैसे करें?"),
                ("wrong", "एसिड में पानी डाल दिया? गलत! मिश्रण उछलकर बाहर आ सकता है।", "“एसिड में पानी डालो” — गलत!"),
                ("right", "ये बहुत एक्सोथर्मिक है। एसिड को धीरे-धीरे पानी में डालो, और लगातार हिलाओ।", "बहुत एक्सोथर्मिक → एसिड धीरे-धीरे पानी में, हिलाते रहो"),
                ("done", "हमेशा एसिड को पानी में डालो!", "एसिड → पानी ✓"),
            ],
        },
    },
}
