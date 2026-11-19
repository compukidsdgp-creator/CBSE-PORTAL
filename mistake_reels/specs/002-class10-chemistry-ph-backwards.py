# Mistake Bank #02 — generic "flip" scene.
PH_SVG = ('<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">'
          + "".join(f'<rect x="{30 + i * 60}" y="70" width="58" height="70" rx="8" fill="{c}"/>'
                    f'<text x="{59 + i * 60}" y="117" text-anchor="middle" font-size="30" font-weight="700" fill="{"#fff" if i < 4 or i > 9 else "#0f172a"}">{i}</text>'
                    for i, c in enumerate(["#b91c1c", "#dc2626", "#ef4444", "#f97316", "#fb923c", "#facc15", "#a3e635", "#22c55e",
                                           "#14b8a6", "#0ea5e9", "#3b82f6", "#4f46e5", "#7c3aed", "#9333ea", "#6b21a8"]))
          + '<path d="M149 40 v26 M329 40 v26" stroke="#0f172a" stroke-width="5"/>'
          '<text x="149" y="32" text-anchor="middle" font-size="30" font-weight="700" fill="#b91c1c">pH 2</text>'
          '<text x="329" y="32" text-anchor="middle" font-size="30" font-weight="700" fill="#c2410c">pH 5</text>'
          '<path d="M930 185 H40" stroke="#b91c1c" stroke-width="6" marker-end="url(#a)"/>'
          '<defs><marker id="a" markerWidth="10" markerHeight="10" refX="6" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#b91c1c"/></marker></defs>'
          '<text x="485" y="222" text-anchor="middle" font-size="28" font-weight="700" fill="#b91c1c">more acidic ←</text></svg>')

REEL = {
    "id": "class10-chemistry-ph-backwards",
    "number": 2,
    "subject_key": "class10/science", "chapter": 2, "chapter_title": "Acids, Bases and Salts",
    "notes": "notes/class-10/science/acids-bases-and-salts.html",
    "scene": {"type": "flip", "svg_wrong": PH_SVG},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Reading the pH scale backwards",
            "stamp": ("WRONG", "Lower pH = more acidic"),
            "rule": ("pH below 7 = acidic", "Lower the pH, stronger the acid"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "scene": {"q": "Which is more acidic: pH 2 or pH 5?", "wrong": "pH 5 — <s>because 5 is bigger</s>",
                      "right": "<mark>pH 2</mark> is more acidic: lower pH, more H⁺ ions",
                      "wrong_label": "What students write", "right_label": "Write this instead"},
            "beats": [
                ("intro", "Top board exam mistake, number two!", "Top board-exam mistakes · #2"),
                ("hook", "Reading the pH scale backwards!", "Reading the pH scale backwards!"),
                ("setup", "Which is more acidic, pH two or pH five?", "Which is more acidic: pH 2 or pH 5?"),
                ("wrong", "Many students say pH five, because five is bigger. Wrong!", "“pH 5, because 5 is bigger” — WRONG!"),
                ("right", "Lower pH means more hydrogen ions. So pH two is more acidic.", "Lower pH = more H⁺ ions → pH 2 is more acidic"),
                ("done", "Lower the pH, stronger the acid!", "Lower pH, stronger acid ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "pH स्केल को उल्टा पढ़ना",
            "stamp": ("गलत!", "कम pH = ज़्यादा एसिडिक"),
            "rule": ("pH 7 से कम = एसिडिक", "pH जितना कम, एसिड उतना तेज़"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "scene": {"q": "ज़्यादा एसिडिक कौन: pH 2 या pH 5?", "wrong": "pH 5 — <s>क्योंकि 5 बड़ा है</s>",
                      "right": "<mark>pH 2</mark> ज़्यादा एसिडिक: कम pH, ज़्यादा H⁺ आयन",
                      "wrong_label": "स्टूडेंट्स लिखते हैं", "right_label": "ऐसे लिखो"},
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर टू!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #2"),
                ("hook", "पी एच स्केल को उल्टा पढ़ना!", "pH स्केल को उल्टा पढ़ना!"),
                ("setup", "पी एच टू और पी एच फ़ाइव में, ज़्यादा एसिडिक कौन है?", "ज़्यादा एसिडिक कौन: pH 2 या pH 5?"),
                ("wrong", "बहुत से स्टूडेंट्स कहते हैं पी एच फ़ाइव, क्योंकि फ़ाइव बड़ा है। गलत!", "“pH 5, क्योंकि 5 बड़ा है” — गलत!"),
                ("right", "पी एच जितना कम, हाइड्रोजन आयन उतने ज़्यादा। इसलिए पी एच टू ज़्यादा एसिडिक है।", "कम pH = ज़्यादा H⁺ आयन → pH 2 ज़्यादा एसिडिक"),
                ("done", "याद रखो, पी एच कम, एसिड तेज़!", "pH कम, एसिड तेज़ ✓"),
            ],
        },
    },
}
