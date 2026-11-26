# Campaign reel #06 — 90+ Score Hack — keep a mistake notebook (wrong answer → why → correct method; 10-min review).
REEL = {
    "n": 6,
    "id": "mistake-notebook",
    "date": "2026-11-27",
    "pillar": "90+ Score Hack",
    "voice": "af_heart", "speed": 1.12,
    "dest": "mistake-bank/",
    "beats": [
        {"say": "Your wrong answers are your best notes.",
         "card": {"type": "title", "kicker": "90+ SCORE HACK", "big": "Your wrong answers are your best notes."}},
        {"say": "Don't just tick the right answer and move on. Write the mistake down.",
         "card": {"type": "compare", "wrong": ["Tick and move on", "Same mistake waits in the next test."],
                  "right": ["Write it down", "Every mistake becomes a lesson."]}},
        {"say": "One entry, three lines. The wrong answer. Why it was wrong. The correct method.",
         "card": {"type": "chain", "title": "One entry, three lines",
                  "items": [["Wrong answer", "What you wrote"], ["Why it was wrong", "The real reason"],
                            ["Correct method", "Step by step"]]}},
        {"say": "Then review the notebook for ten minutes before every study session.",
         "card": {"type": "recap", "kicker": "DAILY HABIT", "big": "10 minutes before every study session."}},
        {"say": "Start one today. Common board mistakes are on CBSE Mock.",
         "cap": "Start one today. Common board mistakes are on CBSEMock",
         "card": {"type": "end", "cta": "Start your notebook today", "url": "cbsemock.org.in/mistake-bank"}},
    ],
    "caption": ("Making the same mistakes again and again? 📓\n\n"
                "Keep a mistake notebook: wrong answer → why it was wrong → correct method.\n"
                "⏱️ Review it for 10 minutes before every study session.\n\n"
                "Common board mistakes 👉 link in bio (cbsemock.org.in/go)"),
    "hashtags": ["#CBSE2027", "#BoardExam", "#MistakeNotebook", "#StudyTips", "#Class10"],
    # Hindi version — same cards, natural spoken Hindi (Indic Parler-TTS voice "rohit", made on GitHub Actions)
    "hi": {
        "voice": "rohit", "engine": "parler", "speed": 1.05,
        "beats": [
            {"say": "तुम्हारे गलत जवाब ही तुम्हारे सबसे अच्छे नोट्स हैं।",
             "card": {"type": "title", "kicker": "90+ SCORE HACK", "big": "गलत जवाब ही सबसे अच्छे नोट्स हैं।"}},
            {"say": "सही जवाब पर टिक लगाकर आगे मत बढ़ो। अपनी गलती लिख लो।",
             "card": {"type": "compare", "wrong": ["टिक लगाया, आगे बढ़े", "वही गलती अगले टेस्ट में फिर।"],
                      "right": ["गलती लिख ली", "हर गलती एक सबक बन जाती है।"]}},
            {"say": "एक एंट्री, तीन लाइनें। गलत जवाब। वो गलत क्यों था। और सही तरीका।",
             "card": {"type": "chain", "title": "एक एंट्री, तीन लाइनें",
                      "items": [["गलत जवाब", "जो तुमने लिखा"], ["गलत क्यों था", "असली वजह"],
                                ["सही तरीका", "स्टेप बाय स्टेप"]]}},
            {"say": "फिर हर बार पढ़ाई शुरू करने से पहले, दस मिनट ये नोटबुक देखो।",
             "card": {"type": "recap", "kicker": "रोज़ की आदत", "big": "हर स्टडी सेशन से पहले 10 मिनट।"}},
            {"say": "आज ही शुरू करो। बोर्ड की आम गलतियाँ देखो, सीबीएसई मॉक पर।",
             "cap": "आज ही शुरू करो। बोर्ड की आम गलतियाँ — CBSEMock पर",
             "card": {"type": "end", "cta": "आज ही नोटबुक शुरू करो", "url": "cbsemock.org.in/mistake-bank"}},
        ],
        "caption": ("एक ही गलती बार-बार हो रही है? 📓\n\n"
                    "मिस्टेक नोटबुक बनाओ: गलत जवाब → गलत क्यों था → सही तरीका।\n"
                    "⏱️ हर स्टडी सेशन से पहले 10 मिनट इसे दोहराओ।\n\n"
                    "बोर्ड की आम गलतियाँ 👉 link in bio (cbsemock.org.in/go)"),
        "hashtags": ["#CBSE2027", "#BoardExam", "#MistakeNotebook", "#CBSEHindi", "#Class10"],
    },
}
