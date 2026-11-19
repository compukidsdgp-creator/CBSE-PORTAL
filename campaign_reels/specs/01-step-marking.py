# Campaign reel #01 — Board FAQ — the reference spec for the 60-day "90+ Score Hack" campaign.
REEL = {
    "n": 1,
    "id": "step-marking",
    "date": "2026-11-20",
    "pillar": "Board FAQ",
    "voice": "af_heart", "speed": 1.12,
    "dest": "free-mock-papers/",
    "beats": [
        {"say": "Right answer, but still lost marks?",
         "card": {"type": "title", "kicker": "CBSE BOARD FAQ", "big": "Right answer. Still lost marks?"}},
        {"say": "Board marking schemes give marks for the steps, not just the final answer.",
         "card": {"type": "compare", "wrong": ["Answer only", "R = 6 Ω"],
                  "right": ["Steps shown", "R = V ÷ I = 12 V ÷ 2 A = 6 Ω"]}},
        {"say": "Write the formula. Substitute the values. Calculate. And always add the unit.",
         "card": {"type": "chain", "title": "V = 12 V, I = 2 A. Find R.",
                  "items": [["Formula", "R = V ÷ I"], ["Substitute", "R = 12 V ÷ 2 A"], ["Calculate + unit", "R = 6 Ω"]]}},
        {"say": "Even if the final answer slips, correct steps can still earn marks.",
         "card": {"type": "recap", "kicker": "REMEMBER", "big": "Every correct step can earn marks."}},
        {"say": "Practise step-wise solutions, free, on CBSE Mock.",
         "cap": "Practise step-wise solutions free on CBSEMock",
         "card": {"type": "end", "cta": "Practise step-wise solutions", "url": "cbsemock.org.in/free-mock-papers"}},
    ],
    "caption": ("Right answer… but still lost marks? 🤔\n\n"
                "CBSE marking schemes give marks for correct steps — not only the final answer.\n"
                "✍️ Formula → Substitute → Calculate → Unit\n\n"
                "Practise step-wise solutions free 👉 link in bio (cbsemock.org.in/go)"),
    "hashtags": ["#CBSE2027", "#BoardExam", "#StepMarking", "#Class10", "#Class12"],
    # Hindi version — same cards, natural spoken Hindi (Indic Parler-TTS voice "rohit", made on GitHub Actions)
    "hi": {
        "voice": "rohit", "engine": "parler", "speed": 1.05,
        "beats": [
            {"say": "सही जवाब लिखा, फिर भी नंबर कट गए?",
             "card": {"type": "title", "kicker": "CBSE बोर्ड FAQ", "big": "सही जवाब। फिर भी नंबर कटे?"}},
            {"say": "बोर्ड की मार्किंग स्कीम में सिर्फ़ फ़ाइनल आंसर के नहीं, सही स्टेप्स के भी नंबर मिलते हैं।",
             "cap": "मार्किंग स्कीम में सिर्फ़ फ़ाइनल आंसर नहीं, सही स्टेप्स के भी नंबर मिलते हैं",
             "card": {"type": "compare", "wrong": ["सिर्फ़ जवाब", "R = 6 Ω"],
                      "right": ["स्टेप्स के साथ", "R = V ÷ I = 12 V ÷ 2 A = 6 Ω"]}},
            {"say": "पहले फ़ॉर्मूला लिखो। फिर वैल्यू रखो। कैलकुलेट करो। और यूनिट ज़रूर लिखो।",
             "card": {"type": "chain", "title": "V = 12 V, I = 2 A. R ज्ञात करो।",
                      "items": [["फ़ॉर्मूला", "R = V ÷ I"], ["वैल्यू रखो", "R = 12 V ÷ 2 A"], ["हल + यूनिट", "R = 6 Ω"]]}},
            {"say": "फ़ाइनल आंसर में गलती हो जाए, तब भी सही स्टेप्स के नंबर मिल सकते हैं।",
             "card": {"type": "recap", "kicker": "याद रखो", "big": "हर सही स्टेप के नंबर मिल सकते हैं।"}},
            {"say": "स्टेप-वाइज़ सॉल्यूशन की प्रैक्टिस करो, बिल्कुल फ़्री, सीबीएसई मॉक पर।",
             "cap": "स्टेप-वाइज़ सॉल्यूशन की फ़्री प्रैक्टिस करो — CBSEMock",
             "card": {"type": "end", "cta": "स्टेप-वाइज़ प्रैक्टिस करो", "url": "cbsemock.org.in/free-mock-papers"}},
        ],
        "caption": ("सही जवाब… फिर भी नंबर कटे? 🤔\n\n"
                    "CBSE की मार्किंग स्कीम में सिर्फ़ फ़ाइनल आंसर नहीं, सही स्टेप्स के भी नंबर मिलते हैं।\n"
                    "✍️ फ़ॉर्मूला → वैल्यू → कैलकुलेशन → यूनिट\n\n"
                    "स्टेप-वाइज़ फ़्री प्रैक्टिस 👉 link in bio (cbsemock.org.in/go)"),
        "hashtags": ["#CBSE2027", "#BoardExam", "#StepMarking", "#CBSEHindi", "#Class10"],
    },
}
