# Campaign reel #07 — Board FAQ — "Is NCERT enough?": the NCERT spots to finish before buying another guide.
# Guardrail (plan note): no "90% of questions are NCERT" / "lifted straight"; say board papers follow the NCERT syllabus closely.
REEL = {
    "n": 7,
    "id": "is-ncert-enough",
    "date": "2026-11-30",
    "pillar": "Board FAQ",
    "voice": "af_heart", "speed": 1.12,
    "dest": "study-zone/",
    "beats": [
        {"say": "Before another guide, check N C E R T.",
         "cap": "Before another guide, check NCERT.",
         "card": {"type": "title", "kicker": "CBSE BOARD FAQ", "big": "Before another guide, check NCERT."}},
        {"say": "In-text questions. Worked examples. Activity conclusions. Chapter-end exercises.",
         "card": {"type": "list", "title": "Don't skip these",
                  "items": ["In-text questions", "Worked examples", "Activity conclusions", "Chapter-end exercises"]}},
        {"say": "Finish these first. Then use N C E R T Exemplar for extra practice.",
         "cap": "Finish these first. Then use NCERT Exemplar for extra practice.",
         "card": {"type": "compare", "wrong": ["Guide first", "Shortcuts, but gaps in the basics."],
                  "right": ["NCERT first", "Textbook, then Exemplar practice."]}},
        {"say": "Board papers follow the N C E R T syllabus closely.",
         "cap": "Board papers follow the NCERT syllabus closely.",
         "card": {"type": "recap", "kicker": "WHY IT WORKS", "big": "Board papers follow the NCERT syllabus."}},
        {"say": "Explore chapter practice on CBSE Mock.",
         "cap": "Explore chapter practice on CBSEMock",
         "card": {"type": "end", "cta": "Explore chapter practice", "url": "cbsemock.org.in/study-zone"}},
    ],
    "caption": ("Is NCERT enough for the board exam? 📘\n\n"
                "Before another guide, finish: in-text questions, worked examples, activity conclusions and chapter-end exercises. Then NCERT Exemplar for extra practice.\n"
                "Board papers follow the NCERT syllabus closely.\n\n"
                "Chapter practice 👉 link in bio (cbsemock.org.in/go)"),
    "hashtags": ["#CBSE2027", "#BoardExam", "#NCERT", "#Class10", "#Class12"],
    # Hindi version — same cards, natural spoken Hindi (Indic Parler-TTS voice "rohit", made on GitHub Actions)
    "hi": {
        "voice": "rohit", "engine": "parler", "speed": 1.05,
        "beats": [
            {"say": "नई गाइड से पहले, एनसीईआरटी चेक करो।",
             "cap": "नई गाइड से पहले, NCERT चेक करो।",
             "card": {"type": "title", "kicker": "CBSE बोर्ड FAQ", "big": "नई गाइड से पहले, NCERT चेक करो।"}},
            {"say": "पाठ के बीच के सवाल। हल किए उदाहरण। एक्टिविटी के निष्कर्ष। चैप्टर के आखिर के सवाल।",
             "card": {"type": "list", "title": "इन्हें मत छोड़ो",
                      "items": ["पाठ के बीच के सवाल", "हल किए उदाहरण", "एक्टिविटी के निष्कर्ष", "चैप्टर के आखिर के सवाल"]}},
            {"say": "पहले ये पूरे करो। फिर एक्स्ट्रा प्रैक्टिस के लिए एनसीईआरटी एग्ज़ेम्प्लर।",
             "cap": "पहले ये पूरे करो। फिर एक्स्ट्रा प्रैक्टिस के लिए NCERT Exemplar।",
             "card": {"type": "compare", "wrong": ["पहले गाइड", "शॉर्टकट मिले, पर बेसिक्स कच्चे।"],
                      "right": ["पहले NCERT", "टेक्स्टबुक, फिर Exemplar प्रैक्टिस।"]}},
            {"say": "बोर्ड के पेपर एनसीईआरटी सिलेबस को करीब से फ़ॉलो करते हैं।",
             "cap": "बोर्ड के पेपर NCERT सिलेबस को करीब से फ़ॉलो करते हैं।",
             "card": {"type": "recap", "kicker": "क्यों?", "big": "बोर्ड पेपर NCERT सिलेबस पर चलते हैं।"}},
            {"say": "चैप्टर वाइज़ प्रैक्टिस देखो, सीबीएसई मॉक पर।",
             "cap": "चैप्टर-वाइज़ प्रैक्टिस देखो — CBSEMock पर",
             "card": {"type": "end", "cta": "चैप्टर-वाइज़ प्रैक्टिस देखो", "url": "cbsemock.org.in/study-zone"}},
        ],
        "caption": ("क्या बोर्ड के लिए NCERT काफ़ी है? 📘\n\n"
                    "नई गाइड से पहले पूरा करो: पाठ के बीच के सवाल, हल किए उदाहरण, एक्टिविटी के निष्कर्ष और चैप्टर के आखिर के सवाल। फिर NCERT Exemplar से एक्स्ट्रा प्रैक्टिस।\n"
                    "बोर्ड के पेपर NCERT सिलेबस को करीब से फ़ॉलो करते हैं।\n\n"
                    "चैप्टर-वाइज़ प्रैक्टिस 👉 link in bio (cbsemock.org.in/go)"),
        "hashtags": ["#CBSE2027", "#BoardExam", "#NCERT", "#CBSEHindi", "#Class10"],
    },
}
