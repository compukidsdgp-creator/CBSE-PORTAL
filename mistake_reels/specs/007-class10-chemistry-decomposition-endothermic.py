# Mistake Bank #07 — generic "flip" scene.
_RED, _GRN, _INK = "#dc2626", "#15803d", "#0f172a"


def _svg(body):
    return ('<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">'
            '<defs><marker id="hr" viewBox="0 0 10 10" markerUnits="userSpaceOnUse" markerWidth="30" markerHeight="30" refX="6" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#dc2626"/></marker>'
            '<marker id="hg" viewBox="0 0 10 10" markerUnits="userSpaceOnUse" markerWidth="30" markerHeight="30" refX="6" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#15803d"/></marker></defs>'
            + body + '</svg>')


def _box(col):
    return (f'<rect x="205" y="60" width="550" height="100" rx="18" fill="#fff" stroke="{col}" stroke-width="5"/>'
            f'<text x="480" y="124" text-anchor="middle" font-size="44" font-weight="700" fill="{_INK}">CaCO₃ → CaO + CO₂</text>')


# front: heat drawn going OUT (the mistake)
DEC_SVG_WRONG = _svg(_box(_RED)
                     + '<path d="M200 110 H55" stroke="#dc2626" stroke-width="7" marker-end="url(#hr)"/>'
                     '<path d="M760 110 H905" stroke="#dc2626" stroke-width="7" marker-end="url(#hr)"/>'
                     '<text x="115" y="80" text-anchor="middle" font-size="30" font-weight="700" fill="#dc2626">heat out?</text>'
                     '<text x="845" y="80" text-anchor="middle" font-size="30" font-weight="700" fill="#dc2626">heat out?</text>'
                     '<text x="480" y="212" text-anchor="middle" font-size="32" font-weight="700" fill="#b91c1c">“exothermic” ✗</text>')
# back: heat goes IN from the flame
DEC_SVG_RIGHT = _svg(_box(_GRN)
                     + '<path d="M25 110 H190" stroke="#15803d" stroke-width="7" marker-end="url(#hg)"/>'
                     '<path d="M935 110 H770" stroke="#15803d" stroke-width="7" marker-end="url(#hg)"/>'
                     '<text x="115" y="80" text-anchor="middle" font-size="30" font-weight="700" fill="#15803d">heat in</text>'
                     '<text x="845" y="80" text-anchor="middle" font-size="30" font-weight="700" fill="#15803d">heat in</text>'
                     '<path d="M480 228 C452 206 462 188 474 172 C476 190 492 194 490 176 C506 196 510 214 480 228z" fill="#f97316"/>'
                     '<text x="640" y="212" text-anchor="middle" font-size="32" font-weight="700" fill="#15803d">endothermic ✓</text>')

REEL = {
    "id": "class10-chemistry-decomposition-endothermic",
    "number": 7,
    "subject_key": "class10/science", "chapter": 1, "chapter_title": "Chemical Reactions and Equations",
    "notes": "notes/class-10/science/chemical-reactions-and-equations.html",
    "scene": {"type": "flip", "svg_wrong": DEC_SVG_WRONG, "svg_right": DEC_SVG_RIGHT},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Calling all decomposition exothermic",
            "stamp": ("WRONG", "Decomposition usually<br>absorbs heat"),
            "rule": ("Decomposition needs energy", "Usually endothermic"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "scene": {"q": "CaCO₃ → CaO + CO₂ on heating. Exothermic or endothermic?",
                      "wrong": "<s>Exothermic — it releases heat</s>",
                      "right": "<mark>Endothermic</mark>: it absorbs heat to break bonds",
                      "wrong_label": "What students write", "right_label": "Write this instead"},
            "beats": [
                ("intro", "Top board exam mistake, number seven!", "Top board-exam mistakes · #7"),
                ("hook", "Calling decomposition exothermic!", "Calling decomposition exothermic!"),
                ("setup", "Heating limestone gives quicklime and carbon dioxide. Exo or endo?", "Heating CaCO₃ → CaO + CO₂: exo or endo?"),
                ("wrong", "Students write exothermic, heat released. Wrong!", "“Exothermic — heat released” — WRONG!"),
                ("right", "Breaking bonds needs energy. It takes in heat, so it's endothermic.", "Breaking bonds needs energy → endothermic"),
                ("done", "Most decompositions are endothermic!", "Decomposition: usually endothermic ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "डीकम्पोज़िशन को एक्सोथर्मिक बताना",
            "stamp": ("गलत!", "डीकम्पोज़िशन में आमतौर पर<br>हीट ली जाती है"),
            "rule": ("डीकम्पोज़िशन में एनर्जी लगती है", "आमतौर पर एंडोथर्मिक"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "scene": {"q": "CaCO₃ → CaO + CO₂ (गरम करने पर)। एक्सोथर्मिक या एंडोथर्मिक?",
                      "wrong": "<s>एक्सोथर्मिक — हीट निकलती है</s>",
                      "right": "<mark>एंडोथर्मिक</mark>: बॉन्ड तोड़ने के लिए हीट लेता है",
                      "wrong_label": "स्टूडेंट्स लिखते हैं", "right_label": "ऐसे लिखो"},
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर सेवन!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #7"),
                ("hook", "डीकम्पोज़िशन को एक्सोथर्मिक बताना!", "डीकम्पोज़िशन को एक्सोथर्मिक बताना!"),
                ("setup", "लाइमस्टोन गरम करने पर क्विकलाइम और कार्बन डाइऑक्साइड बनते हैं। एक्सो या एंडो?", "CaCO₃ → CaO + CO₂ (गरम करने पर): एक्सो या एंडो?"),
                ("wrong", "स्टूडेंट्स लिखते हैं एक्सोथर्मिक, हीट निकलती है। गलत!", "“एक्सोथर्मिक — हीट निकलती है” — गलत!"),
                ("right", "बॉन्ड तोड़ने में एनर्जी लगती है। हीट अंदर जाती है, यानी एंडोथर्मिक।", "बॉन्ड तोड़ने में एनर्जी → एंडोथर्मिक"),
                ("done", "ज़्यादातर डीकम्पोज़िशन एंडोथर्मिक होते हैं!", "डीकम्पोज़िशन: आमतौर पर एंडोथर्मिक ✓"),
            ],
        },
    },
}
