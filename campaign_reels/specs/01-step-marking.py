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
}
