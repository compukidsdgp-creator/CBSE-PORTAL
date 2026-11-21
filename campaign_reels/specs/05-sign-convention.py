# Campaign reel #05 — Mistake Fix — New Cartesian sign convention (Class 12 Physics, Ray Optics: mirror formula).
# Example (checked in Python): concave mirror, object 20 cm, f = 15 cm. 1/v + 1/u = 1/f.
# Signs first: u = −20, f = −15 → 1/v = −1/15 + 1/20 = −1/60 → v = −60 cm (real, in front of the mirror).
# No signs:    u = 20,  f = 15  → 1/v = 1/15 − 1/20 = +1/60 → v = +60 cm (wrong: says image behind the mirror).
REEL = {
    "n": 5,
    "id": "sign-convention",
    "date": "2026-11-26",
    "pillar": "Mistake Fix",
    "voice": "af_heart", "speed": 1.12,
    "dest": "cbse-class-12-physics-mock-papers.html",
    "beats": [
        {"say": "One wrong sign can ruin a whole numerical.",
         "card": {"type": "title", "kicker": "MISTAKE FIX · PHYSICS 12", "big": "One wrong sign ruins a numerical."}},
        {"say": "Measure from the pole. Along the incident light, plus. Against it, minus.",
         "cap": "Measure from the pole. Along incident light = +. Against it = −.",
         "card": {"type": "chain", "title": "New Cartesian sign convention",
                  "items": [["Measure from", "pole / optical centre"], ["Along incident light", "+ positive"],
                            ["Against incident light", "− negative"]]}},
        {"say": "Concave mirror, object 20 centimetres, f 15. No signs: v is plus 60. Wrong. Signs first: minus 60, a real image.",
         "cap": "Concave mirror, object 20 cm, f 15 cm. No signs: v = +60 ✗ Signs first: v = −60 cm, real ✓",
         "card": {"type": "compare", "wrong": ["No signs", "u = 20, f = 15 → v = +60 cm"],
                  "right": ["Signs first", "u = −20, f = −15 → v = −60 cm (real)"]}},
        {"say": "Signs on u, v and f before you substitute.",
         "card": {"type": "recap", "kicker": "LOCK IT IN", "big": "Signs on u, v, f first."}},
        {"say": "Practise Physics numericals on CBSE Mock.",
         "cap": "Practise Physics numericals on CBSEMock",
         "card": {"type": "end", "cta": "Practise Physics numericals", "url": "cbsemock.org.in"}},
    ],
    "caption": ("One wrong sign can ruin a whole numerical. 😬\n\n"
                "New Cartesian sign convention: measure from the pole/optical centre; along incident light = +, against = −.\n"
                "Concave mirror, object 20 cm, f = 15 cm → u = −20, f = −15 → v = −60 cm (real image).\n"
                "Put signs on u, v, f BEFORE substituting.\n\n"
                "Class 12 Physics mock papers 👉 link in bio (cbsemock.org.in/go)"),
    "hashtags": ["#CBSE2027", "#BoardExam", "#Class12Physics", "#RayOptics", "#Class12"],
    # Hindi version — same cards, natural spoken Hindi (Indic Parler-TTS voice "rohit", made on GitHub Actions)
    "hi": {
        "voice": "rohit", "engine": "parler", "speed": 1.05,
        "beats": [
            {"say": "एक गलत साइन, और पूरा न्यूमेरिकल बिगड़ जाता है।",
             "card": {"type": "title", "kicker": "मिस्टेक फ़िक्स · फ़िज़िक्स 12", "big": "एक गलत साइन, पूरा न्यूमेरिकल गलत।"}},
            {"say": "पोल से नापो। इंसिडेंट लाइट की दिशा में प्लस, उल्टी में माइनस।",
             "cap": "पोल से नापो। इंसिडेंट लाइट की दिशा में +, उल्टी में −",
             "card": {"type": "chain", "title": "न्यू कार्टेशियन साइन कन्वेंशन",
                      "items": [["यहाँ से नापो", "पोल / ऑप्टिकल सेंटर"], ["इंसिडेंट लाइट की दिशा", "+ पॉज़िटिव"],
                                ["उल्टी दिशा", "− नेगेटिव"]]}},
            {"say": "कॉन्केव मिरर, ऑब्जेक्ट बीस सेंटीमीटर, एफ़ पंद्रह। बिना साइन, वी प्लस साठ, गलत। पहले साइन, तो माइनस साठ, यानी रियल इमेज।",
             "cap": "कॉन्केव मिरर, ऑब्जेक्ट 20 cm, f = 15 cm। बिना साइन: v = +60 cm ✗ पहले साइन: v = −60 cm, रियल इमेज ✓",
             "card": {"type": "compare", "wrong": ["बिना साइन", "u = 20, f = 15 → v = +60 cm"],
                      "right": ["पहले साइन", "u = −20, f = −15 → v = −60 cm (रियल)"]}},
            {"say": "सब्स्टिट्यूट करने से पहले, यू, वी और एफ़ पर साइन लगाओ।",
             "card": {"type": "recap", "kicker": "पक्का कर लो", "big": "पहले u, v, f पर साइन।"}},
            {"say": "फ़िज़िक्स के न्यूमेरिकल की प्रैक्टिस करो, सीबीएसई मॉक पर।",
             "cap": "फ़िज़िक्स न्यूमेरिकल की प्रैक्टिस करो — CBSEMock",
             "card": {"type": "end", "cta": "फ़िज़िक्स न्यूमेरिकल प्रैक्टिस करो", "url": "cbsemock.org.in"}},
        ],
        "caption": ("एक गलत साइन, और पूरा न्यूमेरिकल गलत। 😬\n\n"
                    "न्यू कार्टेशियन साइन कन्वेंशन: हर दूरी पोल/ऑप्टिकल सेंटर से; इंसिडेंट लाइट की दिशा में +, उल्टी दिशा में −।\n"
                    "कॉन्केव मिरर, ऑब्जेक्ट 20 cm, f = 15 cm → u = −20, f = −15 → v = −60 cm (रियल इमेज)।\n"
                    "सब्स्टिट्यूट करने से पहले u, v, f पर साइन लगाओ।\n\n"
                    "क्लास 12 फ़िज़िक्स मॉक पेपर 👉 link in bio (cbsemock.org.in/go)"),
        "hashtags": ["#CBSE2027", "#BoardExam", "#Class12Physics", "#CBSEHindi", "#Class12"],
    },
}
