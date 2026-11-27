# Mistake Bank #12 — generic "flip" scene.
_INK = "#0f172a"


def _svg(body):
    return '<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">' + body + '</svg>'


def _tube(cx, fill, top_label, colour_label, label_col):
    """A test tube centred at cx: medium name above, liquid colour name below."""
    return (
        f'<text x="{cx}" y="32" text-anchor="middle" font-size="32" font-weight="800" fill="{_INK}">{top_label}</text>'
        f'<path d="M{cx - 32} 46 V150 a32 32 0 0 0 64 0 V46" fill="none" stroke="#475569" stroke-width="6"/>'
        f'<path d="M{cx - 28} 90 V150 a28 28 0 0 0 56 0 V90 Z" fill="{fill}"/>'
        f'<text x="{cx}" y="222" text-anchor="middle" font-size="30" font-weight="800" fill="{label_col}">{colour_label}</text>'
    )


def _name(cx, a, b):
    return (f'<text x="{cx}" y="105" text-anchor="middle" font-size="30" font-weight="800" fill="{_INK}">{a}</text>'
            f'<text x="{cx}" y="141" text-anchor="middle" font-size="30" font-weight="800" fill="{_INK}">{b}</text>')


# front: the mistake — phenolphthalein shown red in acid
IND_SVG_WRONG = _svg(
    _tube(330, "#dc2626", "acid", "red?", "#dc2626")
    + '<text x="560" y="120" text-anchor="middle" font-size="120" font-weight="800" fill="#dc2626">✕</text>'
    + f'<text x="560" y="190" text-anchor="middle" font-size="34" font-weight="800" fill="{_INK}">phenolphthalein</text>'
)

# back: the four correct colours
IND_SVG_RIGHT = _svg(
    _tube(90, "#f1f5f9", "acid", "colourless", "#475569")
    + _tube(230, "#ec4899", "base", "pink", "#db2777")
    + _name(355, "phenol-", "phthalein")
    + '<path d="M480 20 V220" stroke="#cbd5e1" stroke-width="3"/>'
    + _name(605, "methyl", "orange")
    + _tube(730, "#dc2626", "acid", "red", "#dc2626")
    + _tube(870, "#facc15", "base", "yellow", "#a16207")
)

REEL = {
    "id": "class10-chemistry-indicator-colours",
    "number": 12,
    "subject_key": "class10/science", "chapter": 2, "chapter_title": "Acids, Bases and Salts",
    "notes": "notes/class-10/science/acids-bases-and-salts.html",
    "scene": {"type": "flip", "svg_wrong": IND_SVG_WRONG, "svg_right": IND_SVG_RIGHT},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Wrong indicator colours",
            "stamp": ("WRONG", "Phenolphthalein is<br>colourless in acid!"),
            "rule": ("Phenolphthalein: pink only in base", "Methyl orange: red in acid"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "scene": {"q": "Phenolphthalein in acid: what colour?",
                      "wrong": "Phenolphthalein turns <s>red</s> in acid",
                      "right": "Phenolphthalein: <mark>colourless</mark> in acid, pink in base",
                      "wrong_label": "What students write", "right_label": "Write this instead"},
            "beats": [
                ("intro", "Top board exam mistake, number twelve!", "Top board-exam mistakes · #12"),
                ("hook", "Mixing up indicator colours!", "Mixing up indicator colours!"),
                ("setup", "What colour is phenolphthalein in acid?", "Phenolphthalein in acid: what colour?"),
                ("wrong", "Many students write red. Wrong!", "“Red in acid” — WRONG!"),
                ("right", "Phenolphthalein is colourless in acid, pink in base. Methyl orange is red in acid, yellow in base.",
                 "Phenolphthalein colourless/pink · methyl orange red/yellow"),
                ("done", "Learn both pairs!", "Both pairs ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 2",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "इंडिकेटर के गलत रंग",
            "stamp": ("गलत!", "एसिड में फ़िनॉलफ़्थेलिन<br>रंगहीन रहता है!"),
            "rule": ("फ़िनॉलफ़्थेलिन: सिर्फ़ बेस में गुलाबी", "मेथिल ऑरेंज: एसिड में लाल"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "scene": {"q": "एसिड में फ़िनॉलफ़्थेलिन का रंग?",
                      "wrong": "फ़िनॉलफ़्थेलिन एसिड में <s>लाल</s>",
                      "right": "फ़िनॉलफ़्थेलिन: एसिड में <mark>रंगहीन</mark>, बेस में गुलाबी",
                      "wrong_label": "स्टूडेंट्स लिखते हैं", "right_label": "ऐसे लिखो"},
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर ट्वेल्व!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #12"),
                ("hook", "इंडिकेटर के रंगों में गड़बड़!", "इंडिकेटर के रंगों में गड़बड़!"),
                ("setup", "एसिड में फ़िनॉलफ़्थेलिन का रंग क्या होता है?", "एसिड में फ़िनॉलफ़्थेलिन का रंग?"),
                ("wrong", "बहुत से स्टूडेंट्स लिखते हैं लाल। गलत!", "“एसिड में लाल” — गलत!"),
                ("right", "फ़िनॉलफ़्थेलिन एसिड में रंगहीन, बेस में गुलाबी। मेथिल ऑरेंज एसिड में लाल, बेस में पीला।",
                 "फ़िनॉलफ़्थेलिन रंगहीन/गुलाबी · मेथिल ऑरेंज लाल/पीला"),
                ("done", "दोनों जोड़ियाँ याद रखो!", "दोनों जोड़ियाँ ✓"),
            ],
        },
    },
}
