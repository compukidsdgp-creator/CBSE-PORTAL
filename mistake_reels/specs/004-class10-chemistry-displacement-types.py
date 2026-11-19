# Mistake Bank #04 — generic "flip" scene.
def _tile(x, y, txt, fill):
    return (f'<rect x="{x}" y="{y}" width="80" height="68" rx="12" fill="{fill}"/>'
            f'<text x="{x + 40}" y="{y + 48}" text-anchor="middle" font-size="38" font-weight="700" fill="#fff">{txt}</text>')


def _op(x, y, s):
    return f'<text x="{x}" y="{y + 49}" text-anchor="middle" font-size="42" font-weight="700" fill="#0f172a">{s}</text>'


def _row(y, groups):
    """groups: list of tile-groups (each a list of (letter, colour)); '+' between reactants/products, '→' in the middle."""
    out, x = "", 52
    for i, g in enumerate(groups):
        if i:
            out += _op(x + 30, y, "→" if i == len(groups) // 2 else "+"); x += 60
        for t, c in g:
            out += _tile(x, y, t, c); x += 84
    return out


_A, _B, _C, _D = "#2563eb", "#ea580c", "#16a34a", "#9333ea"
DISP_SVG = ('<svg viewBox="0 0 960 230" xmlns="http://www.w3.org/2000/svg" font-family="Poppins,Inter,sans-serif">'
            '<text x="52" y="30" font-size="30" font-weight="700" fill="#15803d">Displacement: element + compound</text>'
            + _row(42, [[("A", _A)], [("B", _B), ("C", _C)], [("A", _A), ("C", _C)], [("B", _B)]])
            + '<text x="52" y="146" font-size="30" font-weight="700" fill="#b91c1c">Double displacement: compound + compound</text>'
            + _row(158, [[("A", _A), ("B", _B)], [("C", _C), ("D", _D)], [("A", _A), ("D", _D)], [("C", _C), ("B", _B)]])
            + '</svg>')

REEL = {
    "id": "class10-chemistry-displacement-types",
    "number": 4,
    "subject_key": "class10/science", "chapter": 1, "chapter_title": "Chemical Reactions and Equations",
    "notes": "notes/class-10/science/chemical-reactions-and-equations.html",
    "scene": {"type": "flip", "svg_wrong": DISP_SVG},
    "lang": {
        "en": {
            "voice": "af_heart", "speed": 1.15,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("TOP BOARD EXAM", "MISTAKES"),
            "title": "Mixing up displacement types",
            "stamp": ("WRONG", "Fe + CuSO₄ is a<br>displacement reaction"),
            "rule": ("Element swaps in: displacement", "Ions swap: double displacement"),
            "cta": "📒 Full Mistake Bank · cbsemock.org.in",
            "scene": {"q": "Fe + CuSO₄ → FeSO₄ + Cu. Which type of reaction?",
                      "wrong": "<s>Double displacement</s>",
                      "right": "<mark>Displacement</mark>: iron pushes copper out of its compound",
                      "wrong_label": "What students write", "right_label": "Write this instead"},
            "beats": [
                ("intro", "Top board exam mistake, number four!", "Top board-exam mistakes · #4"),
                ("hook", "Mixing up displacement types!", "Mixing up displacement types!"),
                ("setup", "Iron plus copper sulphate. Which type of reaction?", "Fe + CuSO₄ → FeSO₄ + Cu: which type?"),
                ("wrong", "Double displacement? Wrong!", "“Double displacement” — WRONG!"),
                ("right", "One element swaps places: displacement. Two compounds swapping ions: double.", "Element swaps → displacement · Ions swap → double"),
                ("done", "Element pushes in? Displacement!", "Displacement ✓"),
            ],
        },
        "hi": {
            "voice": "rohit", "engine": "parler", "speed": 1.08,
            "badge": "Class 10 · Chemistry · Ch 1",
            "intro": ("बोर्ड एग्ज़ाम की", "टॉप गलतियाँ"),
            "title": "डिस्प्लेसमेंट के टाइप में कन्फ़्यूज़न",
            "stamp": ("गलत!", "Fe + CuSO₄ डिस्प्लेसमेंट<br>रिएक्शन है"),
            "rule": ("एलिमेंट जगह ले: डिस्प्लेसमेंट", "आयन बदलें: डबल डिस्प्लेसमेंट"),
            "cta": "📒 पूरा Mistake Bank · cbsemock.org.in",
            "scene": {"q": "Fe + CuSO₄ → FeSO₄ + Cu. ये कौन सा रिएक्शन है?",
                      "wrong": "<s>डबल डिस्प्लेसमेंट</s>",
                      "right": "<mark>डिस्प्लेसमेंट</mark>: आयरन ने कॉपर को कंपाउंड से बाहर निकाला",
                      "wrong_label": "स्टूडेंट्स लिखते हैं", "right_label": "ऐसे लिखो"},
            "beats": [
                ("intro", "बोर्ड एग्ज़ाम की टॉप गलती, नंबर फ़ोर!", "बोर्ड एग्ज़ाम की टॉप गलतियाँ · #4"),
                ("hook", "डिस्प्लेसमेंट के टाइप में कन्फ़्यूज़न!", "डिस्प्लेसमेंट के टाइप में कन्फ़्यूज़न!"),
                ("setup", "आयरन प्लस कॉपर सल्फ़ेट। ये कौन सा रिएक्शन है?", "Fe + CuSO₄ → FeSO₄ + Cu: कौन सा टाइप?"),
                ("wrong", "डबल डिस्प्लेसमेंट? गलत!", "“डबल डिस्प्लेसमेंट” — गलत!"),
                ("right", "एक एलिमेंट जगह बदले, तो डिस्प्लेसमेंट। दो कंपाउंड आयन बदलें, तो डबल।", "एलिमेंट जगह ले → डिस्प्लेसमेंट · आयन बदलें → डबल"),
                ("done", "एलिमेंट ने जगह ली? यानी डिस्प्लेसमेंट!", "डिस्प्लेसमेंट ✓"),
            ],
        },
    },
}
