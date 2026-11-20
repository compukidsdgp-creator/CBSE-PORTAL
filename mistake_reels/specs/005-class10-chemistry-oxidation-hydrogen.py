# Mistake Bank #05 — generic "flip" scene.
def _box(x, y, w, txt, fill):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="70" rx="14" fill="{fill}"/>'
            f'<text x="{x + w / 2}" y="{y + 48}" text-anchor="middle" font-size="38" font-weight="700" fill="#fff">{txt}</text>')


def _arrow(x1, x2, y, col):
    return f'<path d="M{x1} {y} H{x2 - 14}" stroke="{col}" stroke-width="6"/><path d="M{x2 - 18} {y - 13} L{x2} {y} L{x2 - 18} {y + 13}z" fill="{col}"/>'


_BLUE, _RED, _GREY = "#2563eb", "#dc2626", "#475569"
# front: the question — which one is oxidised?
OX_SVG_WRONG = ('<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">'
                + _box(40, 30, 220, "MnO₂", _GREY) + _arrow(280, 460, 65, _GREY) + _box(480, 30, 240, "MnCl₂", _GREY)
                + _box(40, 130, 220, "4HCl", _GREY) + _arrow(280, 460, 165, _GREY) + _box(480, 130, 240, "Cl₂", _GREY)
                + '<text x="840" y="140" text-anchor="middle" font-size="110" font-weight="700" fill="#b91c1c">?</text></svg>')
# back: MnO₂ loses O (reduced), HCl loses H (oxidised)
OX_SVG_RIGHT = ('<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">'
                + _box(10, 30, 180, "MnO₂", _BLUE) + _arrow(200, 300, 65, _BLUE) + _box(310, 30, 180, "MnCl₂", _BLUE)
                + '<text x="510" y="80" font-size="40" font-weight="700" fill="#1d4ed8">loses O → reduced</text>'
                + _box(10, 130, 180, "4HCl", _RED) + _arrow(200, 300, 165, _RED) + _box(310, 130, 180, "Cl₂", _RED)
                + '<text x="510" y="180" font-size="40" font-weight="700" fill="#b91c1c">loses H → oxidised</text></svg>')

REEL = {
    "id": "class10-chemistry-oxidation-hydrogen",
    "number": 5,
    "subject_key": "class10/science", "chapter": 1, "chapter_title": "Chemical Reactions and Equations",
    "notes": "notes/class-10/science/chemical-reactions-and-equations.html",
    "scene": {"type": "flip", "svg_wrong": OX_SVG_WRONG, "svg_right": OX_SVG_RIGHT},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Oxidation only means oxygen",
            "stamp": ("WRONG", "Loss of hydrogen<br>is also oxidation"),
            "rule": ("Oxidation: gain of O or loss of H", "Reduction: loss of O or gain of H"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "scene": {"q": "MnO₂ + 4HCl → MnCl₂ + 2H₂O + Cl₂. Which substance is oxidised?",
                      "wrong": "<s>Nothing — HCl gains no oxygen</s>",
                      "right": "<mark>HCl</mark> is oxidised: it <mark>loses hydrogen</mark>",
                      "wrong_label": "What students write", "right_label": "Write this instead"},
            "beats": [
                ("intro", "Top board exam mistake, number five!", "Top board-exam mistakes · #5"),
                ("hook", "Thinking oxidation only means oxygen!", "Oxidation only means oxygen?"),
                ("setup", "Manganese dioxide plus hydrochloric acid. What is oxidised?", "MnO₂ + 4HCl → MnCl₂ + 2H₂O + Cl₂: what is oxidised?"),
                ("wrong", "Students say nothing, since H C L gains no oxygen. Wrong!", "“Nothing — HCl gains no oxygen” — WRONG!"),
                ("right", "Losing hydrogen is oxidation too. So H C L is oxidised.", "Loss of H = oxidation → HCl is oxidised"),
                ("done", "Lose hydrogen? Oxidised!", "HCl oxidised ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "ऑक्सीडेशन मतलब सिर्फ़ ऑक्सीजन?",
            "stamp": ("गलत!", "हाइड्रोजन खोना भी<br>ऑक्सीडेशन है"),
            "rule": ("ऑक्सीडेशन: O मिले या H जाए", "रिडक्शन: O जाए या H मिले"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "scene": {"q": "MnO₂ + 4HCl → MnCl₂ + 2H₂O + Cl₂. किसका ऑक्सीडेशन हुआ?",
                      "wrong": "<s>किसी का नहीं — HCl को ऑक्सीजन नहीं मिली</s>",
                      "right": "<mark>HCl</mark> ऑक्सीडाइज़ हुआ: उसने <mark>हाइड्रोजन खोई</mark>",
                      "wrong_label": "स्टूडेंट्स लिखते हैं", "right_label": "ऐसे लिखो"},
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर फ़ाइव!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #5"),
                ("hook", "ऑक्सीडेशन मतलब सिर्फ़ ऑक्सीजन? नहीं!", "ऑक्सीडेशन मतलब सिर्फ़ ऑक्सीजन?"),
                ("setup", "मैंगनीज़ डाइऑक्साइड प्लस हाइड्रोक्लोरिक एसिड। किसका ऑक्सीडेशन हुआ?", "MnO₂ + 4HCl → MnCl₂ + 2H₂O + Cl₂: किसका ऑक्सीडेशन?"),
                ("wrong", "स्टूडेंट्स कहते हैं किसी का नहीं, क्योंकि एच सी एल को ऑक्सीजन नहीं मिली। गलत!", "“किसी का नहीं” — गलत!"),
                ("right", "हाइड्रोजन खोना भी ऑक्सीडेशन है। एच सी एल ने हाइड्रोजन खोई, तो वो ऑक्सीडाइज़ हुआ।", "H खोना = ऑक्सीडेशन → HCl ऑक्सीडाइज़ हुआ"),
                ("done", "हाइड्रोजन गई? यानी ऑक्सीडेशन!", "HCl ऑक्सीडाइज़ ✓"),
            ],
        },
    },
}
