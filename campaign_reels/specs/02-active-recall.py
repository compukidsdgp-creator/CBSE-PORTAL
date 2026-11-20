# Campaign reel #02 — 90+ Score Hack — active recall instead of rereading.
REEL = {
    "n": 2,
    "id": "active-recall",
    "date": "2026-11-23",
    "pillar": "90+ Score Hack",
    "voice": "af_heart", "speed": 1.12,
    "dest": "study-zone/",
    "beats": [
        {"say": "Stop rereading. Start recalling.",
         "card": {"type": "title", "kicker": "90+ SCORE HACK", "big": "Stop rereading. Start recalling."}},
        {"say": "Rereading makes pages feel familiar. Recalling shows what you really know.",
         "card": {"type": "compare", "wrong": ["Rereading", "Pages feel familiar. Gaps stay hidden."],
                  "right": ["Recalling", "Pull it from memory. See your gaps."]}},
        {"say": "Read for five minutes. Close the book. Write everything you remember. Then check what you missed.",
         "card": {"type": "chain", "title": "The recall loop",
                  "items": [["Read", "5 minutes"], ["Close the book", "No peeking"],
                            ["Write", "Everything you remember"], ["Check", "What did you miss?"]]}},
        {"say": "Whatever you missed is exactly what to revise next.",
         "card": {"type": "recap", "kicker": "REMEMBER", "big": "Your gaps = your next revision."}},
        {"say": "Save this, and try it tonight. More study tips on CBSE Mock.",
         "cap": "Save this and try it tonight. More study tips on CBSEMock",
         "card": {"type": "end", "cta": "Save this and try it tonight", "url": "cbsemock.org.in/study-zone"}},
    ],
    "caption": ("Still rereading the same chapter again and again? 📖\n\n"
                "Try active recall instead: Read 5 min → close the book → write everything you remember → check what you missed.\n"
                "Whatever you missed = your next revision.\n\n"
                "More study tips 👉 link in bio (cbsemock.org.in/go)"),
    "hashtags": ["#CBSE2027", "#BoardExam", "#ActiveRecall", "#StudyTips", "#Class10"],
    # Hindi version — same cards, natural spoken Hindi (Indic Parler-TTS voice "rohit", made on GitHub Actions)
    "hi": {
        "voice": "rohit", "engine": "parler", "speed": 1.05,
        "beats": [
            {"say": "बार-बार पढ़ना बंद करो। याद करके लिखना शुरू करो।",
             "card": {"type": "title", "kicker": "90+ स्कोर हैक", "big": "दोबारा पढ़ना छोड़ो। याद करके लिखो।"}},
            {"say": "दोबारा पढ़ने से पेज जाने-पहचाने लगते हैं। याद करके लिखने से पता चलता है कि असल में कितना आता है।",
             "card": {"type": "compare", "wrong": ["बार-बार पढ़ना", "पेज जाने-पहचाने लगते हैं। कमियाँ छिपी रहती हैं।"],
                      "right": ["याद करके लिखना", "दिमाग़ से निकालो। कमियाँ साफ़ दिखेंगी।"]}},
            {"say": "पाँच मिनट पढ़ो। किताब बंद करो। जितना याद है, सब लिखो। फिर चेक करो क्या छूट गया।",
             "card": {"type": "chain", "title": "रिकॉल का तरीका",
                      "items": [["पढ़ो", "5 मिनट"], ["किताब बंद", "झाँकना मना है"],
                                ["लिखो", "जितना याद है, सब"], ["चेक करो", "क्या छूट गया?"]]}},
            {"say": "जो छूट गया, वही तुम्हारा अगला रिवीज़न है।",
             "card": {"type": "recap", "kicker": "याद रखो", "big": "जो छूटा = अगला रिवीज़न।"}},
            {"say": "इसे सेव करो, और आज रात ही ट्राई करो। और स्टडी टिप्स सीबीएसई मॉक पर।",
             "cap": "इसे सेव करो और आज रात ट्राई करो — और टिप्स CBSEMock पर",
             "card": {"type": "end", "cta": "सेव करो, आज रात ट्राई करो", "url": "cbsemock.org.in/study-zone"}},
        ],
        "caption": ("एक ही चैप्टर बार-बार पढ़ रहे हो? 📖\n\n"
                    "एक्टिव रिकॉल ट्राई करो: 5 मिनट पढ़ो → किताब बंद → जितना याद है लिखो → चेक करो क्या छूटा।\n"
                    "जो छूटा = तुम्हारा अगला रिवीज़न।\n\n"
                    "और स्टडी टिप्स 👉 link in bio (cbsemock.org.in/go)"),
        "hashtags": ["#CBSE2027", "#BoardExam", "#ActiveRecall", "#CBSEHindi", "#StudyTips"],
    },
}
