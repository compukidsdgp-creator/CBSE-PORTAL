# Campaign reel #09 — Board FAQ — value points: write distinct, numbered points instead of one long paragraph.
# Guardrail (plan note): phrase as a strategy, not a universal rule ("marking schemes list value points").
# Source: CBSE marking schemes' general instructions — "The Marking scheme carries only suggested value points for the answers"
# (e.g. cbseacademic.nic.in Class X Science MS).
REEL = {
    "n": 9,
    "id": "value-points",
    "date": "2026-12-02",
    "pillar": "Board FAQ",
    "voice": "af_heart", "speed": 1.12,
    "dest": "free-mock-papers/",
    "beats": [
        {"say": "Three marks? Write three clear points.",
         "card": {"type": "title", "kicker": "CBSE BOARD FAQ", "big": "3 marks? Write 3 clear points."}},
        {"say": "Board marking schemes list value points. Don't bury yours in one long paragraph.",
         "card": {"type": "compare", "wrong": ["One long paragraph", "Points buried. Easy to miss."],
                  "right": ["Numbered points", "Each point clear and easy to find."]}},
        {"say": "One idea per point. Start with the keyword. Leave space between points.",
         "card": {"type": "list", "title": "Write it like this",
                  "items": ["One idea per point", "Start with the keyword", "Space between points"]}},
        {"say": "Make every value point easy to find.",
         "card": {"type": "recap", "kicker": "REMEMBER", "big": "Make every point easy to find."}},
        {"say": "Read model answers on CBSE Mock.",
         "cap": "Read model answers on CBSEMock",
         "card": {"type": "end", "cta": "Read model answers", "url": "cbsemock.org.in/free-mock-papers"}},
    ],
    "caption": ("3-mark answer? Write 3 clear points. ✍️\n\n"
                "CBSE marking schemes list value points. Instead of one long paragraph, write distinct, numbered points — one idea each, keyword first.\n"
                "One idea → One point → Space\n\n"
                "Read model answers 👉 link in bio (cbsemock.org.in/go)"),
    "hashtags": ["#CBSE2027", "#BoardExam", "#AnswerWriting", "#Class10", "#Class12"],
    # Hindi version — same cards, natural spoken Hindi (Indic Parler-TTS voice "rohit", made on GitHub Actions)
    "hi": {
        "voice": "rohit", "engine": "parler", "speed": 1.05,
        "beats": [
            {"say": "तीन नंबर का सवाल? तीन साफ़ पॉइंट लिखो।",
             "card": {"type": "title", "kicker": "CBSE बोर्ड FAQ", "big": "3 नंबर? 3 साफ़ पॉइंट लिखो।"}},
            {"say": "बोर्ड की मार्किंग स्कीम में वैल्यू पॉइंट्स लिखे होते हैं। अपने पॉइंट्स एक लंबे पैराग्राफ़ में मत छिपाओ।",
             "card": {"type": "compare", "wrong": ["एक लंबा पैराग्राफ़", "पॉइंट्स छिप गए, छूट सकते हैं।"],
                      "right": ["नंबर वाले पॉइंट्स", "हर पॉइंट साफ़, आसानी से दिखे।"]}},
            {"say": "हर पॉइंट में एक बात। शुरुआत कीवर्ड से। पॉइंट्स के बीच जगह छोड़ो।",
             "card": {"type": "list", "title": "ऐसे लिखो",
                      "items": ["हर पॉइंट में एक बात", "शुरुआत कीवर्ड से", "पॉइंट्स के बीच जगह"]}},
            {"say": "हर वैल्यू पॉइंट ऐसा लिखो कि तुरंत दिख जाए।",
             "card": {"type": "recap", "kicker": "याद रखो", "big": "हर पॉइंट तुरंत दिखना चाहिए।"}},
            {"say": "मॉडल आंसर पढ़ो, सीबीएसई मॉक पर।",
             "cap": "मॉडल आंसर पढ़ो — CBSEMock पर",
             "card": {"type": "end", "cta": "मॉडल आंसर पढ़ो", "url": "cbsemock.org.in/free-mock-papers"}},
        ],
        "caption": ("3 नंबर का जवाब? 3 साफ़ पॉइंट लिखो। ✍️\n\n"
                    "CBSE की मार्किंग स्कीम में वैल्यू पॉइंट्स होते हैं। एक लंबे पैराग्राफ़ की जगह अलग-अलग, नंबर वाले पॉइंट्स लिखो — हर पॉइंट में एक बात, शुरुआत कीवर्ड से।\n"
                    "एक बात → एक पॉइंट → जगह\n\n"
                    "मॉडल आंसर पढ़ो 👉 link in bio (cbsemock.org.in/go)"),
        "hashtags": ["#CBSE2027", "#BoardExam", "#AnswerWriting", "#CBSEHindi", "#Class10"],
    },
}
