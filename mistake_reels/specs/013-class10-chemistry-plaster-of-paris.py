# Mistake Bank #13 — generic "flip" scene.
_INK = "#0f172a"


def _svg(body):
    return '<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">' + body + '</svg>'


def _unit(x, y):
    """One CaSO₄ block."""
    return (f'<rect x="{x}" y="{y}" width="150" height="60" rx="12" fill="#e2e8f0" stroke="#475569" stroke-width="4"/>'
            f'<text x="{x + 75}" y="{y + 41}" text-anchor="middle" font-size="30" font-weight="800" fill="{_INK}">CaSO₄</text>')


def _drop(cx, cy):
    """One water molecule, drawn as a drop."""
    return (f'<path d="M{cx} {cy - 30} C{cx + 26} {cy} {cx + 22} {cy + 26} {cx} {cy + 26} '
            f'C{cx - 22} {cy + 26} {cx - 26} {cy} {cx} {cy - 30} Z" fill="#38bdf8" stroke="#0369a1" stroke-width="3"/>'
            f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" font-size="15" font-weight="800" fill="#fff">H₂O</text>')


# front: the mistake — two waters per CaSO₄ is gypsum, not Plaster of Paris
POP_SVG_WRONG = _svg(
    _unit(250, 60) + _drop(450, 90) + _drop(510, 90)
    + '<text x="680" y="110" text-anchor="middle" font-size="100" font-weight="800" fill="#dc2626">✕</text>'
    + '<text x="480" y="200" text-anchor="middle" font-size="34" font-weight="800" fill="#dc2626">CaSO₄·2H₂O = gypsum</text>'
)

# back: gypsum (2 waters each) → heat 373 K → PoP (one water shared by two CaSO₄)
POP_SVG_RIGHT = _svg(
    _unit(20, 34) + _drop(205, 64) + _drop(260, 64)
    + f'<text x="155" y="140" text-anchor="middle" font-size="28" font-weight="800" fill="{_INK}">gypsum</text>'
    + '<path d="M305 70 H395" stroke="#ea580c" stroke-width="6"/>'
    + '<path d="M392 58 L418 70 L392 82 Z" fill="#ea580c"/>'
    + '<text x="360" y="45" text-anchor="middle" font-size="26" font-weight="800" fill="#ea580c">373 K</text>'
    + _unit(440, 0) + _unit(440, 70) + _drop(640, 65)
    + '<path d="M600 30 H615 V100 H600" fill="none" stroke="#15803d" stroke-width="4"/>'
    + '<text x="545" y="166" text-anchor="middle" font-size="28" font-weight="800" fill="#15803d">Plaster of Paris</text>'
    + '<text x="545" y="212" text-anchor="middle" font-size="34" font-weight="800" fill="#15803d">CaSO₄·½H₂O</text>'
    + f'<text x="830" y="80" text-anchor="middle" font-size="28" font-weight="800" fill="{_INK}">½ water</text>'
    + f'<text x="830" y="116" text-anchor="middle" font-size="28" font-weight="800" fill="{_INK}">per CaSO₄</text>'
)

REEL = {
    "id": "class10-chemistry-plaster-of-paris",
    "number": 13,
    "subject_key": "class10/science", "chapter": 2, "chapter_title": "Acids, Bases and Salts",
    "notes": "notes/class-10/science/acids-bases-and-salts.html",
    "scene": {"type": "flip", "svg_wrong": POP_SVG_WRONG, "svg_right": POP_SVG_RIGHT},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Wrong formula of Plaster of Paris",
            "stamp": ("WRONG", "CaSO₄·2H₂O<br>is gypsum!"),
            "rule": ("Plaster of Paris = CaSO₄·½H₂O", "Gypsum = CaSO₄·2H₂O"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "scene": {"q": "Write the formula of Plaster of Paris.",
                      "wrong": "<s>CaSO₄·2H₂O</s> or <s>CaSO₄·H₂O</s>",
                      "right": "CaSO₄·<mark>½</mark>H₂O<br>(gypsum is CaSO₄·2H₂O)",
                      "wrong_label": "What students write", "right_label": "Write this instead"},
            "beats": [
                ("intro", "Top board exam mistake, number thirteen!", "Top board-exam mistakes · #13"),
                ("hook", "Wrong formula of Plaster of Paris!", "Wrong formula of Plaster of Paris!"),
                ("setup", "What is the formula of Plaster of Paris?", "Formula of Plaster of Paris?"),
                ("wrong", "Calcium sulphate with two waters? Wrong! That's gypsum.", "CaSO₄·2H₂O? WRONG — that's gypsum!"),
                ("right", "Heat gypsum at three seventy three kelvin. Plaster of Paris keeps only half a water.",
                 "Gypsum at 373 K → CaSO₄·½H₂O"),
                ("done", "Half, not two!", "½ H₂O ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "प्लास्टर ऑफ़ पेरिस का गलत फ़ॉर्मूला",
            "stamp": ("गलत!", "CaSO₄·2H₂O<br>तो जिप्सम है!"),
            "rule": ("प्लास्टर ऑफ़ पेरिस = CaSO₄·½H₂O", "जिप्सम = CaSO₄·2H₂O"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "scene": {"q": "प्लास्टर ऑफ़ पेरिस का फ़ॉर्मूला लिखो।",
                      "wrong": "<s>CaSO₄·2H₂O</s> या <s>CaSO₄·H₂O</s>",
                      "right": "CaSO₄·<mark>½</mark>H₂O<br>(जिप्सम है CaSO₄·2H₂O)",
                      "wrong_label": "स्टूडेंट्स लिखते हैं", "right_label": "ऐसे लिखो"},
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर थर्टीन!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #13"),
                ("hook", "प्लास्टर ऑफ़ पेरिस का गलत फ़ॉर्मूला!", "प्लास्टर ऑफ़ पेरिस का गलत फ़ॉर्मूला!"),
                ("setup", "प्लास्टर ऑफ़ पेरिस का फ़ॉर्मूला क्या है?", "प्लास्टर ऑफ़ पेरिस का फ़ॉर्मूला?"),
                ("wrong", "कैल्शियम सल्फ़ेट के साथ दो पानी? गलत! वो तो जिप्सम है।", "CaSO₄·2H₂O? गलत — वो जिप्सम है!"),
                ("right", "जिप्सम को तीन सौ तिहत्तर केल्विन पर गरम करो। प्लास्टर ऑफ़ पेरिस में बस आधा पानी बचता है।",
                 "जिप्सम, 373 K पर → CaSO₄·½H₂O"),
                ("done", "दो नहीं, आधा!", "½ H₂O ✓"),
            ],
        },
    },
}
