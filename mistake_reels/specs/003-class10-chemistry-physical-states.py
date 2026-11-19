# Mistake Bank #03 — generic "flip" scene.
_CHIPS = [("(s)", "solid", "#2563eb"), ("(l)", "liquid", "#0891b2"), ("(g)", "gas", "#7c3aed"), ("(aq)", "aqueous", "#16a34a")]
STATES_SVG = ('<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">'
              + "".join(f'<rect x="{12 + i * 237}" y="30" width="221" height="170" rx="22" fill="{c}"/>'
                        f'<text x="{122 + i * 237}" y="112" text-anchor="middle" font-size="62" font-weight="700" fill="#fff">{s}</text>'
                        f'<text x="{122 + i * 237}" y="166" text-anchor="middle" font-size="32" font-weight="700" fill="#fff">{w}</text>'
                        for i, (s, w, c) in enumerate(_CHIPS))
              + '</svg>')
_G = '<span style="color:#16a34a">'

REEL = {
    "id": "class10-chemistry-physical-states",
    "number": 3,
    "subject_key": "class10/science", "chapter": 1, "chapter_title": "Chemical Reactions and Equations",
    "notes": "notes/class-10/science/chemical-reactions-and-equations.html",
    "scene": {"type": "flip", "svg_right": STATES_SVG},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Leaving out physical states",
            "stamp": ("WRONG", "States were asked —<br>no states, marks lost!"),
            "rule": ("Write (s), (l), (g), (aq)", "after every formula"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "scene": {"q": "Zinc + dilute sulphuric acid: write the equation with states",
                      "wrong": "Zn + H₂SO₄ → ZnSO₄ + H₂<br><s>no states</s>",
                      "right": f"<mark>Add states:</mark> Zn{_G}(s)</span> + H₂SO₄{_G}(aq)</span> → ZnSO₄{_G}(aq)</span> + H₂{_G}(g)</span>",
                      "wrong_label": "What students write", "right_label": "Write this instead"},
            "beats": [
                ("intro", "Top board exam mistake, number three!", "Top board-exam mistakes · #3"),
                ("hook", "Leaving out physical states!", "Leaving out physical states!"),
                ("setup", "The question says: write the equation with states.", "Write the equation with physical states"),
                ("wrong", "You write no states at all? Wrong! Marks lost.", "No (s), (aq), (g)? WRONG — marks lost!"),
                ("right", "S for solid, L for liquid, G for gas, A Q for aqueous.", "(s) solid · (l) liquid · (g) gas · (aq) aqueous"),
                ("done", "States in brackets, every time!", "States in brackets ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "फ़िज़िकल स्टेट्स छोड़ देना",
            "stamp": ("गलत!", "स्टेट्स पूछे थे —<br>नहीं लिखे, नंबर कटे!"),
            "rule": ("(s), (l), (g), (aq) लिखो", "हर फ़ॉर्मूले के बाद"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "scene": {"q": "ज़िंक + तनु सल्फ़्यूरिक एसिड: स्टेट्स के साथ इक्वेशन लिखो",
                      "wrong": "Zn + H₂SO₄ → ZnSO₄ + H₂<br><s>कोई स्टेट नहीं</s>",
                      "right": f"<mark>स्टेट्स जोड़ो:</mark> Zn{_G}(s)</span> + H₂SO₄{_G}(aq)</span> → ZnSO₄{_G}(aq)</span> + H₂{_G}(g)</span>",
                      "wrong_label": "स्टूडेंट्स लिखते हैं", "right_label": "ऐसे लिखो"},
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर थ्री!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #3"),
                ("hook", "फ़िज़िकल स्टेट्स लिखना भूल जाना!", "फ़िज़िकल स्टेट्स भूल जाना!"),
                ("setup", "सवाल कहता है, स्टेट्स के साथ इक्वेशन लिखो।", "स्टेट्स के साथ इक्वेशन लिखो"),
                ("wrong", "और आपने स्टेट्स लिखे ही नहीं? गलत! नंबर कट गए।", "स्टेट्स नहीं लिखे? गलत — नंबर कटे!"),
                ("right", "एस यानी सॉलिड, एल लिक्विड, जी गैस, और ए क्यू यानी एक्वियस।", "(s) सॉलिड · (l) लिक्विड · (g) गैस · (aq) एक्वियस"),
                ("done", "हर बार, ब्रैकेट में स्टेट!", "ब्रैकेट में स्टेट ✓"),
            ],
        },
    },
}
