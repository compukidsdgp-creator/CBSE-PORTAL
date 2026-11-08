#!/usr/bin/env python3
"""
post_festival.py — CBSE Mock Festival & Occasion Greetings (Telegram)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Checks today's date against festivals.json and posts a beautiful
animated HTML greeting card to Telegram as a rich text message,
plus a study motivation tie-in.

Called from GitHub Actions daily (morning run checks for festivals).
If today is not a festival day, exits silently with code 0.

Usage:
  python3 post_festival.py              # auto-detect today
  python3 post_festival.py --dry-run    # preview without posting
  python3 post_festival.py --date 11-08 # force a specific date (MM-DD)
"""

import os, sys, json, argparse, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone, date

REPO          = Path(__file__).parent
FESTIVALS_FILE = REPO / "festivals.json"
BOT_TOKEN     = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID       = os.environ.get("TELEGRAM_CHAT_ID", "")
TG_API_BASE   = "https://api.telegram.org/bot"
PORTAL_URL    = "https://cbsemock.org.in"

# ── Greeting templates per festival ──────────────────────────────────────────
# Key = festival name (lowercase, stripped). Falls back to GENERIC.
GREETINGS = {
    "diwali": {
        "header": "🪔 Happy Diwali! 🪔",
        "lines": [
            "May the Festival of Lights brighten your path to success!",
            "✨ Just like a lamp dispels darkness, knowledge dispels doubt.",
            "Let this Diwali spark a new level of exam preparation! 🔥",
        ],
        "cta": "🎯 Use this festive break wisely — attempt a mock test today!",
        "anim": "🪔🎆✨🪔🎆✨🪔",
        "study_tip": "Board exams are just months away. Even 1 hour of focused revision today keeps the momentum going!",
    },
    "diwali (day 2)": {
        "header": "🪔 Diwali Day 2 — Keep the Light Burning! ✨",
        "lines": [
            "The celebrations continue — and so does your preparation! 💪",
            "Every question you practice today is a step toward your score.",
        ],
        "cta": "📚 Quick 10-minute chapter quiz → cbsemock.org.in",
        "anim": "✨🪔✨🪔✨🪔✨",
        "study_tip": "Short sessions on festival days > zero sessions. Try one chapter MCQ set!",
    },
    "new year": {
        "header": "🎉 Happy New Year 2027! 🎉",
        "lines": [
            "A brand new year — and Board Exams are closer than ever! 📅",
            "Make 2027 your BEST academic year yet.",
            "Start strong: revise one chapter today. 💪",
        ],
        "cta": "🗓️ New year, new goals — start with a mock test right now!",
        "anim": "🎆🎉🎊🎆🎉🎊🎆",
        "study_tip": "Students who revise in January score significantly higher in March boards. Start now!",
    },
    "republic day": {
        "header": "🇮🇳 Happy Republic Day! 🇮🇳",
        "lines": [
            "On this proud day, we celebrate our Constitution and our nation.",
            "Let's also celebrate the power of education — the greatest equaliser! 📚",
        ],
        "cta": "🎯 Honour the republic by investing in your future — attempt a mock test!",
        "anim": "🇮🇳🌸🇮🇳🌸🇮🇳",
        "study_tip": "Civics, History, Geography — SST students, today is a great day to revise! 📖",
    },
    "independence day": {
        "header": "🇮🇳 Happy Independence Day! 🇮🇳",
        "lines": [
            "75+ years of freedom, countless opportunities ahead!",
            "Education is the foundation of a free, strong nation. 🌟",
            "Make your future bright — your boards are your first step.",
        ],
        "cta": "🎯 Celebrate freedom by freeing yourself from exam stress — practice daily!",
        "anim": "🇮🇳🌸🎆🇮🇳🌸🎆🇮🇳",
        "study_tip": "Even on a holiday, 30 minutes of revision makes a difference. Try a mock paper today!",
    },
    "teachers' day": {
        "header": "👩‍🏫 Happy Teachers' Day! 🌸",
        "lines": [
            "Today we honour every teacher who shaped a student's life. 🙏",
            "To all the students — your teachers believe in you. Prove them right! 💪",
        ],
        "cta": "📚 The best way to thank your teacher: score your personal best in boards!",
        "anim": "🌸👩‍🏫📚🌸👩‍🏫📚🌸",
        "study_tip": "Drop a 'Thank You' to your favourite teacher today — and get back to revision! 😊",
    },
    "holi": {
        "header": "🌈 Happy Holi! 🌈",
        "lines": [
            "May your life be as colourful as Holi — and your marksheet even brighter! 😄",
            "Have fun with family and friends today! 🎉",
        ],
        "cta": "📖 Come back refreshed tomorrow for some serious board prep!",
        "anim": "🌈🎨🌸🌈🎨🌸🌈",
        "study_tip": "A well-rested, happy mind learns better. Enjoy today — revise tomorrow! 💪",
    },
    "christmas": {
        "header": "🎄 Merry Christmas! 🎄",
        "lines": [
            "Wishing you joy, warmth, and excellent scores in your board exams! 🎁",
            "May Santa bring you exactly what you need: confidence and clarity! 🌟",
        ],
        "cta": "🎯 Holiday season = less distraction. Perfect time for a full mock test!",
        "anim": "🎄🎁⭐🎄🎁⭐🎄",
        "study_tip": "December is the golden revision window before January unit tests. Use it! 📚",
    },
    "gandhi jayanti": {
        "header": "🕊️ Gandhi Jayanti — 2nd October 🇮🇳",
        "lines": [
            "\"Live as if you were to die tomorrow. Learn as if you were to live forever.\" — Mahatma Gandhi",
            "On Bapu's birthday, let's commit to learning with sincerity. 📚",
        ],
        "cta": "📖 Start a new chapter today — in books and in life!",
        "anim": "🕊️🇮🇳🌸🕊️🇮🇳🌸🕊️",
        "study_tip": "Gandhiji valued discipline and consistency. Apply that to your studies today!",
    },
    "dussehra": {
        "header": "🏹 Happy Dussehra! 🏹",
        "lines": [
            "On this day of victory of good over evil —",
            "Let knowledge conquer confusion, and hard work conquer fear! 💪",
        ],
        "cta": "🎯 Defeat your weak chapters today. Practice makes perfect!",
        "anim": "🏹🌟🏹🌟🏹🌟🏹",
        "study_tip": "Dussehra marks the start of the final exam prep sprint. 100 days to boards!",
    },
    "guru nanak jayanti": {
        "header": "🙏 Gurpurab Mubarak! 🙏",
        "lines": [
            "On Guru Nanak Dev Ji's Prakash Utsav — seek blessings of wisdom and knowledge.",
            "\"Nanak dukhia sab sansar\" — rise above all worries through learning! 📚",
        ],
        "cta": "📖 Dedicate a chapter today in the spirit of Seva and Siksha!",
        "anim": "🙏✨🌸🙏✨🌸🙏",
        "study_tip": "Guruji's teachings emphasise honest hard work. That's the only exam strategy that works!",
    },
}

GENERIC = {
    "header": "{emoji} {name}!",
    "lines": [
        "Warm wishes from the entire CBSE Mock team! 🎉",
        "May this occasion bring you joy, peace, and academic success! 📚",
    ],
    "cta": "🎯 Celebrate AND prepare — attempt a mock test today!",
    "anim": "{emoji}✨{emoji}✨{emoji}",
    "study_tip": "Festive days are great for a quick revision session. Keep the momentum going!",
}

# ── Study motivation tie-ins per month (for board countdown) ─────────────────
def board_countdown_line() -> str:
    today = date.today()
    # CBSE boards typically start around Feb 15
    board_start = date(today.year + (1 if today.month > 8 else 0), 2, 15)
    days = (board_start - today).days
    if days > 180:
        return f"📅 Board exams in ~{days} days — still time to build a strong foundation!"
    elif days > 90:
        return f"⏳ Board exams in {days} days — time to shift into focused revision mode!"
    elif days > 30:
        return f"🔥 Only {days} days to Board exams — every day counts now!"
    else:
        return f"🚨 Board exams in {days} days — stay calm, stay focused, trust your prep!"

# ── Telegram helpers ──────────────────────────────────────────────────────────
def tg_request(method: str, payload: dict, dry_run: bool = False) -> dict:
    if dry_run:
        print(f"\n[DRY RUN] Telegram.{method}:")
        print(json.dumps(payload, indent=2, ensure_ascii=False)[:1000])
        return {"ok": True, "result": {"message_id": 0}}
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set.")
    url  = f"{TG_API_BASE}{BOT_TOKEN}/{method}"
    data = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(url, data=data,
                                  headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Telegram {e.code}: {e.read().decode()}")

def tg_send(text: str, dry_run=False) -> dict:
    return tg_request("sendMessage", {
        "chat_id":    CHAT_ID,
        "text":       text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }, dry_run)

# ── Festival lookup ───────────────────────────────────────────────────────────
def get_today_festival(override_date: str | None = None) -> dict | None:
    data = json.loads(FESTIVALS_FILE.read_text(encoding="utf-8"))
    today = date.today()
    year  = str(today.year)
    mmdd  = override_date or today.strftime("%m-%d")

    return data.get(year, {}).get(mmdd)

# ── Build message ─────────────────────────────────────────────────────────────
def build_message(festival: dict) -> str:
    name  = festival["name"]
    emoji = festival["emoji"]
    key   = name.lower().strip()

    tmpl = GREETINGS.get(key, GENERIC)

    header = tmpl["header"].format(emoji=emoji, name=name)
    anim   = tmpl["anim"].format(emoji=emoji)
    lines  = "\n".join(f"  {l}" for l in tmpl["lines"])
    cta    = tmpl["cta"]
    tip    = tmpl["study_tip"]
    countdown = board_countdown_line()

    msg = (
        f"{anim}\n\n"
        f"<b>{header}</b>\n\n"
        f"{lines}\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📚 <b>Study Motivation:</b>\n"
        f"<i>{tip}</i>\n\n"
        f"⏱ {countdown}\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"{cta}\n\n"
        f"🔗 <a href='{PORTAL_URL}'>Practice at cbsemock.org.in →</a>\n\n"
        f"<i>— Team CBSE Mock 🎓</i>\n\n"
        f"#CBSEMock #{name.replace(' ','').replace('(','').replace(')','').replace('/','').replace('\'','')} "
        f"#BoardExams2027 #CBSEStudents #ExamPrep"
    )
    return msg

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="CBSE Mock festival greeting poster")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--date", help="Force date MM-DD (e.g. 11-08 for Diwali)")
    args = parser.parse_args()

    festival = get_today_festival(args.date)

    if not festival:
        mmdd = args.date or date.today().strftime("%m-%d")
        print(f"[INFO] No festival on {mmdd} — nothing to post.")
        sys.exit(0)

    print(f"[FESTIVAL] {festival['name']} {festival['emoji']} ({festival['type']})")

    msg = build_message(festival)
    result = tg_send(msg, dry_run=args.dry_run)
    mid = result.get("result", {}).get("message_id", "n/a")
    print(f"[OK] Festival post sent → msg {mid}")

if __name__ == "__main__":
    main()
