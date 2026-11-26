# Mistake Bank #11 — generic "flip" scene.
_INK = "#0f172a"


def _svg(body):
    return '<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">' + body + '</svg>'


def _bubbles(cx):
    return "".join(f'<circle cx="{cx + dx}" cy="{cy}" r="{r}" fill="#fff" stroke="#64748b" stroke-width="2"/>'
                   for dx, cy, r in ((-26, 170, 7), (26, 150, 6), (-24, 128, 5), (24, 110, 7), (-22, 92, 4)))


def _cell(left_gas, right_gas, col, mark, naoh):
    """Electrolysis of brine: anode (+) on the left, cathode (−) on the right; gas labels outside the tank."""
    body = (
        # wire + battery on top
        f'<path d="M342 40 V16 H455 M505 16 H618 V40" fill="none" stroke="{_INK}" stroke-width="4"/>'
        f'<path d="M455 2 V30 M470 8 V24" stroke="{_INK}" stroke-width="5"/>'
        f'<path d="M490 2 V30 M505 8 V24" stroke="{_INK}" stroke-width="5"/>'
        # tank with brine
        '<rect x="250" y="70" width="460" height="152" rx="14" fill="#e0f2fe" stroke="#475569" stroke-width="5"/>'
        '<text x="480" y="212" text-anchor="middle" font-size="24" font-weight="700" fill="#0369a1">brine (NaCl solution)</text>'
        # electrodes
        '<rect x="330" y="40" width="24" height="150" rx="5" fill="#334155"/>'
        '<rect x="606" y="40" width="24" height="150" rx="5" fill="#334155"/>'
        + _bubbles(342) + _bubbles(618) +
        # labels outside the tank
        f'<text x="125" y="70" text-anchor="middle" font-size="30" font-weight="800" fill="{_INK}">Anode (+)</text>'
        f'<text x="125" y="150" text-anchor="middle" font-size="56" font-weight="800" fill="{col}">{left_gas}</text>'
        f'<text x="835" y="70" text-anchor="middle" font-size="30" font-weight="800" fill="{_INK}">Cathode (−)</text>'
        f'<text x="835" y="150" text-anchor="middle" font-size="56" font-weight="800" fill="{col}">{right_gas}</text>'
        f'<text x="125" y="205" text-anchor="middle" font-size="40" font-weight="800" fill="{col}">{mark}</text>'
        f'<text x="835" y="205" text-anchor="middle" font-size="40" font-weight="800" fill="{col}">{mark}</text>'
    )
    if naoh:
        body += '<text x="535" y="140" text-anchor="middle" font-size="28" font-weight="800" fill="#15803d">NaOH</text>'
    return _svg(body)


# front: gases swapped (the mistake)
CELL_SVG_WRONG = _cell("H₂", "Cl₂", "#dc2626", "✕", False)
# back: correct products
CELL_SVG_RIGHT = _cell("Cl₂", "H₂", "#15803d", "✓", True)

REEL = {
    "id": "class10-chemistry-chlor-alkali-electrodes",
    "number": 11,
    "subject_key": "class10/science", "chapter": 2, "chapter_title": "Acids, Bases and Salts",
    "notes": "notes/class-10/science/acids-bases-and-salts.html",
    "scene": {"type": "flip", "svg_wrong": CELL_SVG_WRONG, "svg_right": CELL_SVG_RIGHT},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Wrong electrode products in chlor-alkali",
            "stamp": ("WRONG", "The gases<br>are swapped!"),
            "rule": ("Anode (+) → Cl₂", "Cathode (−) → H₂ + NaOH"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "scene": {"q": "Electrolysis of brine: what forms at each electrode?",
                      "wrong": "Anode <s>H₂</s> · Cathode <s>Cl₂</s>",
                      "right": "Anode <mark>Cl₂</mark> · Cathode H₂<br>NaOH near the cathode",
                      "wrong_label": "What students write", "right_label": "Write this instead"},
            "beats": [
                ("intro", "Top board exam mistake, number eleven!", "Top board-exam mistakes · #11"),
                ("hook", "Swapping the chlor-alkali gases!", "Swapping the chlor-alkali gases!"),
                ("setup", "Electrolyse brine. What forms where?", "Electrolysis of brine: what forms where?"),
                ("wrong", "Hydrogen at the anode, chlorine at the cathode? Wrong!", "“H₂ at anode, Cl₂ at cathode” — WRONG!"),
                ("right", "Chlorine at the anode. Hydrogen at the cathode, with sodium hydroxide near it.",
                 "Anode: Cl₂ · Cathode: H₂ · NaOH near the cathode"),
                ("done", "Chlorine at the anode!", "Cl₂ at the anode ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "क्लोर-अल्कली में इलेक्ट्रोड के प्रोडक्ट उल्टे",
            "stamp": ("गलत!", "गैसें उल्टी<br>लिख दीं!"),
            "rule": ("एनोड (+) → Cl₂", "कैथोड (−) → H₂ + NaOH"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "scene": {"q": "ब्राइन का इलेक्ट्रोलिसिस: किस इलेक्ट्रोड पर क्या बनता है?",
                      "wrong": "एनोड <s>H₂</s> · कैथोड <s>Cl₂</s>",
                      "right": "एनोड <mark>Cl₂</mark> · कैथोड H₂<br>NaOH कैथोड के पास",
                      "wrong_label": "स्टूडेंट्स लिखते हैं", "right_label": "ऐसे लिखो"},
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर इलेवन!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #11"),
                ("hook", "क्लोर-अल्कली में गैसों की अदला-बदली!", "क्लोर-अल्कली में गैसों की अदला-बदली!"),
                ("setup", "ब्राइन का इलेक्ट्रोलिसिस करो। कहाँ क्या बनता है?", "ब्राइन का इलेक्ट्रोलिसिस: कहाँ क्या बनता है?"),
                ("wrong", "एनोड पर हाइड्रोजन, कैथोड पर क्लोरीन? गलत!", "“एनोड पर H₂, कैथोड पर Cl₂” — गलत!"),
                ("right", "एनोड पर क्लोरीन। कैथोड पर हाइड्रोजन, और उसके पास सोडियम हाइड्रॉक्साइड।",
                 "एनोड: Cl₂ · कैथोड: H₂ · NaOH कैथोड के पास"),
                ("done", "क्लोरीन, एनोड पर!", "Cl₂ एनोड पर ✓"),
            ],
        },
    },
}
