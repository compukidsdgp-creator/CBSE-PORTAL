# Campaign reel #08 — Beat the Timer — case-study questions: read the questions before the passage.
REEL = {
    "n": 8,
    "id": "case-study-questions-first",
    "date": "2026-12-01",
    "pillar": "Beat the Timer",
    "voice": "af_heart", "speed": 1.12,
    "dest": "mock-zone/",
    "beats": [
        {"say": "Case study? Read the questions first.",
         "card": {"type": "title", "kicker": "BEAT THE TIMER", "big": "Case study? Read the questions first."}},
        {"say": "Passage first? You often read it twice. Questions first? You read once, with a target.",
         "card": {"type": "compare", "wrong": ["Passage first", "Read it all, then hunt again."],
                  "right": ["Questions first", "Read once, knowing what to find."]}},
        {"say": "Scan the questions. Read only for what they ask. Underline the data you need.",
         "card": {"type": "chain", "title": "The 3-step scan",
                  "items": [["Scan the questions", "What do they ask?"], ["Read the passage", "Hunt only for that"],
                            ["Underline the data", "Numbers, names, terms"]]}},
        {"say": "Know what you are hunting for before you start reading.",
         "card": {"type": "recap", "kicker": "REMEMBER", "big": "Know what you're hunting for."}},
        {"say": "Try competency questions on CBSE Mock.",
         "cap": "Try competency questions on CBSEMock",
         "card": {"type": "end", "cta": "Try competency questions", "url": "cbsemock.org.in/mock-zone"}},
    ],
    "caption": ("Case study questions eating your time? ⏱️\n\n"
                "Read the questions BEFORE the passage. Then read the passage hunting only for what they ask, and underline the data you need.\n"
                "Scan → Hunt → Underline\n\n"
                "Practise competency questions 👉 link in bio (cbsemock.org.in/go)"),
    "hashtags": ["#CBSE2027", "#BoardExam", "#CaseStudy", "#ExamTips", "#Class10"],
    # Hindi version — same cards, natural spoken Hindi (Indic Parler-TTS voice "rohit", made on GitHub Actions)
    "hi": {
        "voice": "rohit", "engine": "parler", "speed": 1.05,
        "beats": [
            {"say": "केस स्टडी? पहले सवाल पढ़ो।",
             "card": {"type": "title", "kicker": "BEAT THE TIMER", "big": "केस स्टडी? पहले सवाल पढ़ो।"}},
            {"say": "पहले पूरा पैसेज पढ़ा, तो अक्सर दोबारा पढ़ना पड़ता है। पहले सवाल पढ़े, तो एक बार में काम हो जाता है।",
             "card": {"type": "compare", "wrong": ["पहले पैसेज", "पूरा पढ़ा, फिर दोबारा ढूँढा।"],
                      "right": ["पहले सवाल", "एक बार पढ़ो, पता है क्या ढूँढना है।"]}},
            {"say": "सवालों पर नज़र डालो। पैसेज में सिर्फ़ वही ढूँढो जो पूछा है। ज़रूरी डेटा अंडरलाइन करो।",
             "card": {"type": "chain", "title": "3 स्टेप वाला स्कैन",
                      "items": [["सवाल स्कैन करो", "क्या पूछा है?"], ["पैसेज पढ़ो", "सिर्फ़ वही ढूँढो"],
                                ["डेटा अंडरलाइन करो", "नंबर, नाम, टर्म्स"]]}},
            {"say": "पढ़ना शुरू करने से पहले जान लो, तुम्हें ढूँढना क्या है।",
             "card": {"type": "recap", "kicker": "याद रखो", "big": "पहले जानो, ढूँढना क्या है।"}},
            {"say": "कॉम्पिटेंसी वाले सवाल ट्राई करो, सीबीएसई मॉक पर।",
             "cap": "कॉम्पिटेंसी वाले सवाल ट्राई करो — CBSEMock पर",
             "card": {"type": "end", "cta": "कॉम्पिटेंसी सवाल ट्राई करो", "url": "cbsemock.org.in/mock-zone"}},
        ],
        "caption": ("केस स्टडी में टाइम ज़्यादा लगता है? ⏱️\n\n"
                    "पैसेज से पहले सवाल पढ़ो। फिर पैसेज में सिर्फ़ वही ढूँढो जो पूछा है, और ज़रूरी डेटा अंडरलाइन करो।\n"
                    "स्कैन → ढूँढो → अंडरलाइन\n\n"
                    "कॉम्पिटेंसी सवालों की प्रैक्टिस 👉 link in bio (cbsemock.org.in/go)"),
        "hashtags": ["#CBSE2027", "#BoardExam", "#CaseStudy", "#CBSEHindi", "#Class10"],
    },
}
