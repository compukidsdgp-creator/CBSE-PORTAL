# Mistake Bank #09 — generic "flip" scene.
_WATER, _INK = "#93c5fd", "#0f172a"


def _svg(body):
    return '<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">' + body + '</svg>'


# front: CuO in water — it does not dissolve, yet it is a base (the counter-example)
BA_SVG_WRONG = _svg(
    '<path d="M136 92 V206 Q136 214 144 214 H316 Q324 214 324 206 V92 Z" fill="' + _WATER + '" opacity=".8"/>'
    + "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#1f2937"/>' for x, y in
              [(160, 202), (180, 196), (200, 203), (222, 197), (244, 202), (266, 196), (288, 203), (306, 198),
               (190, 186), (234, 187), (278, 187)])
    + '<path d="M122 60 H136 V206 Q136 214 144 214 H316 Q324 214 324 206 V60" fill="none" stroke="#334155" stroke-width="6" stroke-linejoin="round"/>'
    '<text x="230" y="140" text-anchor="middle" font-size="30" font-weight="700" fill="' + _INK + '">water</text>'
    '<text x="230" y="40" text-anchor="middle" font-size="34" font-weight="800" fill="' + _INK + '">CuO</text>'
    '<text x="640" y="92" text-anchor="middle" font-size="34" font-weight="800" fill="#b91c1c">does not dissolve…</text>'
    '<text x="640" y="150" text-anchor="middle" font-size="34" font-weight="800" fill="#15803d">but it is still a base!</text>')

# back: Venn — alkalis are a small circle inside bases
BA_SVG_RIGHT = _svg(
    '<ellipse cx="480" cy="118" rx="440" ry="108" fill="#ede9fe" stroke="#7c3aed" stroke-width="5"/>'
    '<text x="190" y="88" text-anchor="middle" font-size="40" font-weight="800" fill="#6d28d9">BASES</text>'
    '<text x="190" y="140" text-anchor="middle" font-size="32" font-weight="700" fill="' + _INK + '">CuO, Cu(OH)₂</text>'
    '<text x="190" y="180" text-anchor="middle" font-size="30" font-weight="700" fill="#475569">insoluble</text>'
    '<ellipse cx="640" cy="118" rx="220" ry="84" fill="#dcfce7" stroke="#16a34a" stroke-width="5"/>'
    '<text x="640" y="90" text-anchor="middle" font-size="36" font-weight="800" fill="#15803d">ALKALIS</text>'
    '<text x="640" y="138" text-anchor="middle" font-size="30" font-weight="700" fill="#166534">dissolve in water</text>'
    '<text x="640" y="180" text-anchor="middle" font-size="32" font-weight="700" fill="' + _INK + '">NaOH, KOH</text>')

REEL = {
    "id": "class10-chemistry-bases-alkalis",
    "number": 9,
    "subject_key": "class10/science", "chapter": 2, "chapter_title": "Acids, Bases and Salts",
    "notes": "notes/class-10/science/acids-bases-and-salts.html",
    "scene": {"type": "flip", "svg_wrong": BA_SVG_WRONG, "svg_right": BA_SVG_RIGHT},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Treating all bases as alkalis",
            "stamp": ("WRONG", "Not every base<br>dissolves in water"),
            "rule": ("Alkali = soluble base", "Not every base is an alkali"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "scene": {"q": "Is every base an alkali?",
                      "wrong": "Yes — <s>every base dissolves in water</s>",
                      "right": "Only <mark>water-soluble bases</mark> are alkalis (NaOH, KOH)",
                      "wrong_label": "What students write", "right_label": "Write this instead"},
            "beats": [
                ("intro", "Top board exam mistake, number nine!", "Top board-exam mistakes · #9"),
                ("hook", "Calling every base an alkali!", "Calling every base an alkali!"),
                ("setup", "Is every base an alkali?", "Is every base an alkali?"),
                ("wrong", "Students say yes, every base dissolves. Wrong!", "“Every base dissolves in water” — WRONG!"),
                ("right", "Only bases that dissolve in water are alkalis.", "Only water-soluble bases are alkalis: NaOH, KOH"),
                ("done", "All alkalis are bases, but not all bases are alkalis!", "All alkalis are bases, not all bases are alkalis ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "हर बेस को एल्कली समझना",
            "stamp": ("गलत!", "हर बेस पानी में<br>नहीं घुलता"),
            "rule": ("एल्कली = घुलनशील बेस", "हर बेस एल्कली नहीं होता"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "scene": {"q": "क्या हर बेस एल्कली होता है?",
                      "wrong": "हाँ — <s>हर बेस पानी में घुलता है</s>",
                      "right": "सिर्फ़ <mark>पानी में घुलने वाले बेस</mark> एल्कली हैं (NaOH, KOH)",
                      "wrong_label": "स्टूडेंट्स लिखते हैं", "right_label": "ऐसे लिखो"},
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर नाइन!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #9"),
                ("hook", "हर बेस को एल्कली कहना!", "हर बेस को एल्कली कहना!"),
                ("setup", "क्या हर बेस एल्कली होता है?", "क्या हर बेस एल्कली होता है?"),
                ("wrong", "स्टूडेंट्स कहते हैं हाँ, हर बेस पानी में घुलता है। गलत!", "“हर बेस पानी में घुलता है” — गलत!"),
                ("right", "सिर्फ़ पानी में घुलने वाले बेस ही एल्कली होते हैं।", "सिर्फ़ पानी में घुलने वाले बेस एल्कली: NaOH, KOH"),
                ("done", "हर एल्कली बेस है, पर हर बेस एल्कली नहीं!", "हर एल्कली बेस है, हर बेस एल्कली नहीं ✓"),
            ],
        },
    },
}
