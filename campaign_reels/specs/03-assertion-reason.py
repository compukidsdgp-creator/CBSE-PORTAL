# Campaign reel #03 — Beat the Timer — the Assertion–Reason check, with a verified mini-example.
# Standard CBSE options: (A) Both A and R are true and R is the correct explanation of A. (B) Both A and R are true
# but R is not the correct explanation of A. (C) A is true but R is false. (D) A is false but R is true.
# Example (Class 10 Real Numbers, 2026–27): A: √2 is irrational (true). R: Every prime number is odd (false: 2) → (C).
REEL = {
    "n": 3,
    "id": "assertion-reason",
    "date": "2026-11-24",
    "pillar": "Beat the Timer",
    "voice": "af_heart", "speed": 1.12,
    "dest": "mock-zone/",
    "beats": [
        {"say": "Assertion Reason in ten seconds?",
         "card": {"type": "title", "kicker": "BEAT THE TIMER", "big": "Assertion–Reason in 10 seconds?"}},
        {"say": "Test A alone, then R alone. Both true? Ask: A because R? Yes, A. No, B. One false? C or D.",
         "cap": "Test A alone, then R alone. Both true? Ask: “A because R”? Yes → A. No → B. One false? C or D.",
         "card": {"type": "chain", "title": "The 10-second check",
                  "items": [["Test A alone", "True or false?"], ["Test R alone", "True or false?"],
                            ["Both true", "“A because R” fits? A : B"], ["One false", "R false → C · A false → D"]]}},
        {"say": "Try this. A: root two is irrational. R: every prime number is odd.",
         "cap": "Try this. A: √2 is irrational. R: Every prime number is odd.",
         "hold": 1.3,
         "card": {"type": "quiz", "q": "A: √2 is irrational.  R: Every prime number is odd.",
                  "opts": ["Both true, R explains A", "Both true, R doesn't", "A true, R false", "A false, R true"],
                  "ans": 2}},
        {"say": "A is true. But two is prime and even, so R is false. Answer: C.",
         "card": {"type": "worked", "title": "Why (C)?",
                  "lines": [["A", "√2 is irrational ✓"], ["R", "2 is prime but even ✗"],
                            ["So", "A true, R false"], ["", "Answer: (C)"]]}},
        {"say": "Got it in ten seconds? Comment your option.",
         "card": {"type": "end", "cta": "Comment your option", "url": "cbsemock.org.in/mock-zone"}},
    ],
    "caption": ("Assertion–Reason in 10 seconds? ⏱️\n\n"
                "Test A alone → test R alone → both true? Read “A because R”. Fits → (A), not → (B). One false → (C) or (D).\n"
                "A: √2 is irrational. R: Every prime number is odd. Your option? 👇\n\n"
                "More practice 👉 link in bio (cbsemock.org.in/go)"),
    "hashtags": ["#CBSE2027", "#BoardExam", "#AssertionReason", "#Class10", "#ExamTips"],
    # Hindi version — same cards, natural spoken Hindi (Indic Parler-TTS voice "rohit", made on GitHub Actions)
    "hi": {
        "voice": "rohit", "engine": "parler", "speed": 1.05,
        "beats": [
            {"say": "असर्शन रीज़न, दस सेकंड में?",
             "card": {"type": "title", "kicker": "BEAT THE TIMER", "big": "Assertion–Reason, 10 सेकंड में?"}},
            {"say": "पहले ए चेक करो, फिर आर। दोनों सही? ए क्योंकि आर बने तो ए, वरना बी। एक गलत? सी या डी।",
             "cap": "पहले A चेक करो, फिर R। दोनों सही? “A क्योंकि R” बने → A, वरना B। एक गलत? C या D।",
             "card": {"type": "chain", "title": "10 सेकंड वाला चेक",
                      "items": [["सिर्फ़ A चेक करो", "सही या गलत?"], ["सिर्फ़ R चेक करो", "सही या गलत?"],
                                ["दोनों सही", "“A क्योंकि R” बने? A : B"], ["एक गलत", "R गलत → C · A गलत → D"]]}},
            {"say": "अब बताओ। ए: रूट टू अपरिमेय। आर: हर अभाज्य संख्या विषम है।",
             "cap": "अब बताओ। A: √2 अपरिमेय। R: हर अभाज्य संख्या विषम है।",
             "hold": 1.3,
             "card": {"type": "quiz", "q": "A: √2 अपरिमेय (irrational) है।  R: हर अभाज्य संख्या विषम होती है।",
                      "opts": ["दोनों सही, R कारण है", "दोनों सही, R कारण नहीं", "A सही, R गलत", "A गलत, R सही"],
                      "ans": 2}},
            {"say": "ए सही। पर दो अभाज्य और सम है, तो आर गलत। जवाब सी।",
             "card": {"type": "worked", "title": "(C) क्यों?",
                      "lines": [["A", "√2 अपरिमेय है ✓"], ["R", "2 अभाज्य है, पर सम ✗"],
                                ["तो", "A सही, R गलत"], ["", "जवाब: (C)"]]}},
            {"say": "दस सेकंड में? अपना ऑप्शन कमेंट करो।",
             "card": {"type": "end", "cta": "अपना ऑप्शन कमेंट करो", "url": "cbsemock.org.in/mock-zone"}},
        ],
        "caption": ("Assertion–Reason, 10 सेकंड में? ⏱️\n\n"
                    "पहले सिर्फ़ A → फिर सिर्फ़ R → दोनों सही? पढ़ो “A क्योंकि R”। बने → (A), न बने → (B)। एक गलत → (C) या (D)।\n"
                    "A: √2 अपरिमेय है। R: हर अभाज्य संख्या विषम होती है। तुम्हारा ऑप्शन? 👇\n\n"
                    "और प्रैक्टिस 👉 link in bio (cbsemock.org.in/go)"),
        "hashtags": ["#CBSE2027", "#BoardExam", "#AssertionReason", "#CBSEHindi", "#Class10"],
    },
}
