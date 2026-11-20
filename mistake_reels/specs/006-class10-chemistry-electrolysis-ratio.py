# Mistake Bank #06 — generic "flip" scene.
_H, _O = "#2563eb", "#dc2626"


def _bar(y, label, units, col, tag):
    """A gas-volume bar: `units` blocks of 240 px each."""
    out = f'<text x="20" y="{y + 50}" font-size="44" font-weight="700" fill="{col}">{label}</text>'
    for i in range(units):
        out += f'<rect x="{110 + i * 246}" y="{y}" width="240" height="76" rx="12" fill="{col}"/>'
    return out + f'<text x="{130 + units * 246}" y="{y + 52}" font-size="38" font-weight="700" fill="#0f172a">{tag}</text>'


def _svg(body):
    return '<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">' + body + '</svg>'


# front: equal volumes (the mistake)
EL_SVG_WRONG = _svg('<text x="20" y="34" font-size="34" font-weight="700" fill="#b91c1c">Gas volume — equal?</text>'
                    + _bar(46, "H₂", 2, _H, "?") + _bar(140, "O₂", 2, _O, "?"))
# back: hydrogen twice oxygen
EL_SVG_RIGHT = _svg('<text x="20" y="34" font-size="34" font-weight="700" fill="#15803d">2H₂O → 2H₂ + O₂ · H₂ : O₂ = 2 : 1</text>'
                    + _bar(46, "H₂", 2, _H, "2 (cathode)") + _bar(140, "O₂", 1, _O, "1 (anode)"))

REEL = {
    "id": "class10-chemistry-electrolysis-ratio",
    "number": 6,
    "subject_key": "class10/science", "chapter": 1, "chapter_title": "Chemical Reactions and Equations",
    "notes": "notes/class-10/science/chemical-reactions-and-equations.html",
    "scene": {"type": "flip", "svg_wrong": EL_SVG_WRONG, "svg_right": EL_SVG_RIGHT},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Wrong volume ratio in electrolysis",
            "stamp": ("WRONG", "Hydrogen is twice<br>the volume of oxygen"),
            "rule": ("2H₂O → 2H₂ + O₂", "H₂ : O₂ = 2 : 1 by volume"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "scene": {"q": "Electrolysis of water: compare the volumes of H₂ and O₂.",
                      "wrong": "<s>Equal volumes of H₂ and O₂</s>",
                      "right": "<mark>H₂ = 2 × O₂</mark> by volume",
                      "wrong_label": "What students write", "right_label": "Write this instead"},
            "beats": [
                ("intro", "Top board exam mistake, number six!", "Top board-exam mistakes · #6"),
                ("hook", "Getting electrolysis volumes wrong!", "Getting electrolysis volumes wrong!"),
                ("setup", "Electrolysis of water. How do the gas volumes compare?", "Electrolysis of water: compare the gas volumes"),
                ("wrong", "Equal volumes of hydrogen and oxygen? Wrong!", "“Equal volumes of H₂ and O₂” — WRONG!"),
                ("right", "Two H two O gives two H two plus O two. Twice as much hydrogen.", "2H₂O → 2H₂ + O₂ → twice as much H₂"),
                ("done", "Hydrogen to oxygen, two to one!", "H₂ : O₂ = 2 : 1 ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "इलेक्ट्रोलिसिस में गलत वॉल्यूम",
            "stamp": ("गलत!", "हाइड्रोजन का वॉल्यूम<br>ऑक्सीजन से दोगुना"),
            "rule": ("2H₂O → 2H₂ + O₂", "H₂ : O₂ = 2 : 1 (वॉल्यूम में)"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "scene": {"q": "पानी का इलेक्ट्रोलिसिस: H₂ और O₂ के वॉल्यूम की तुलना करो।",
                      "wrong": "<s>H₂ और O₂ बराबर वॉल्यूम में</s>",
                      "right": "<mark>H₂ = 2 × O₂</mark> (वॉल्यूम में)",
                      "wrong_label": "स्टूडेंट्स लिखते हैं", "right_label": "ऐसे लिखो"},
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर सिक्स!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #6"),
                ("hook", "इलेक्ट्रोलिसिस में गैस का वॉल्यूम गलत बताना!", "इलेक्ट्रोलिसिस में गलत वॉल्यूम!"),
                ("setup", "पानी के इलेक्ट्रोलिसिस में, दोनों गैसों का वॉल्यूम कैसा होता है?", "पानी का इलेक्ट्रोलिसिस: गैसों का वॉल्यूम?"),
                ("wrong", "हाइड्रोजन और ऑक्सीजन बराबर? गलत!", "“H₂ और O₂ बराबर” — गलत!"),
                ("right", "टू एच टू ओ से टू एच टू और ओ टू बनते हैं। हाइड्रोजन, ऑक्सीजन से दोगुनी।", "2H₂O → 2H₂ + O₂ → H₂ दोगुनी"),
                ("done", "हाइड्रोजन और ऑक्सीजन, दो और एक!", "H₂ : O₂ = 2 : 1 ✓"),
            ],
        },
    },
}
