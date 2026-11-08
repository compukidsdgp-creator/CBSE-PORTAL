#!/usr/bin/env python3
"""
post_facebook.py — CBSE Mock Facebook Page Auto-Poster
───────────────────────────────────────────────────────
Posts daily content to the CBSEMock Facebook page:
  • Morning: Quest of the Day (MCQ from current month's question bank)
  • Evening: Top CBSE news headlines

Environment variables (set as GitHub Secrets):
  FB_PAGE_ID           — Facebook Page ID (1472735085918141)
  FB_PAGE_ACCESS_TOKEN — Never-expiring Page Access Token

Usage:
  python3 post_facebook.py --mode quest    # Post Quest of the Day
  python3 post_facebook.py --mode news     # Post news digest
  python3 post_facebook.py --mode both     # Post both (default)
  python3 post_facebook.py --dry-run       # Preview without posting
"""

import os
import sys
import json
import re
import random
import argparse
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, date
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
REPO_ROOT   = Path(__file__).parent
QUESTIONS_DIR = REPO_ROOT / "quest" / "data" / "questions"
CATALOGUE_PATH = REPO_ROOT / "quest" / "data" / "catalogue-entry.json"

FB_API_VERSION = "v27.0"
FB_API_BASE    = f"https://graph.facebook.com/{FB_API_VERSION}"

PAGE_ID    = os.environ.get("FB_PAGE_ID", "1472735085918141")
_RAW_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN", "")

def _resolve_page_token(raw_token: str, page_id: str) -> str:
    """If raw_token is a system user / user token, exchange it for a page token."""
    if not raw_token:
        return raw_token
    try:
        url = f"{FB_API_BASE}/{page_id}?fields=access_token&access_token={raw_token}"
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
            if "access_token" in data:
                print("[INFO] Resolved page token from system user token.")
                return data["access_token"]
    except Exception as e:
        print(f"[WARN] Could not resolve page token: {e} — using token as-is.")
    return raw_token

PAGE_TOKEN = _resolve_page_token(_RAW_TOKEN, PAGE_ID)

NEWS_QUERIES = [
    "CBSE board exam 2027",
    "CBSE date sheet 2027",
    "CBSE result 2026",
]

# ── Facebook API ──────────────────────────────────────────────────────────────
def fb_post(message: str, dry_run: bool = False) -> dict:
    """Post a message to the Facebook page."""
    if dry_run:
        print("\n[DRY RUN] Would post to Facebook:")
        print("─" * 60)
        print(message)
        print("─" * 60)
        return {"id": "dry_run_post_id"}

    if not PAGE_TOKEN:
        raise ValueError("FB_PAGE_ACCESS_TOKEN not set. Add it to GitHub Secrets.")

    url = f"{FB_API_BASE}/{PAGE_ID}/feed"
    data = urllib.parse.urlencode({
        "message": message,
        "access_token": PAGE_TOKEN,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"Facebook API error {e.code}: {body}")


# ── Quest of the Day ──────────────────────────────────────────────────────────
def pick_question() -> dict | None:
    """Pick a random MCQ from the current month's question bank."""
    if not QUESTIONS_DIR.exists():
        print("[SKIP] No questions directory found.")
        return None

    # Get all question files (not manifest files)
    q_files = [f for f in QUESTIONS_DIR.iterdir()
               if f.suffix == ".json" and "manifest" not in f.name]
    if not q_files:
        print("[SKIP] No question files found.")
        return None

    # Pick a random file, then a random question
    random.seed(datetime.now(timezone.utc).toordinal())  # consistent seed per day
    q_file = random.choice(q_files)
    with open(q_file, encoding="utf-8") as f:
        data = json.load(f)

    questions = data.get("questions", [])
    # Prefer medium difficulty MCQs
    mcqs = [q for q in questions if q.get("type") == "MCQ"]
    pool = mcqs if mcqs else questions
    if not pool:
        return None

    return random.choice(pool)


def format_quest_post(q: dict) -> str:
    """Format a question as a Facebook post."""
    subject  = q.get("subject", "CBSE")
    chapter  = q.get("chapter", "")
    question = q.get("question", "")
    options  = q.get("options", {})
    answer   = q.get("answer", "")
    explanation = q.get("explanation", "")
    cls      = q.get("class", "")

    # Format options
    opts_text = ""
    if isinstance(options, dict):
        for k, v in options.items():
            opts_text += f"\n  {k}) {v}"
    elif isinstance(options, list):
        for i, v in enumerate(options):
            letter = chr(65 + i)
            opts_text += f"\n  {letter}) {v}"

    # Answer reveal
    if isinstance(options, dict) and answer in options:
        answer_text = f"{answer}) {options[answer]}"
    else:
        answer_text = answer

    post = f"""🎯 Quest of the Day — Class {cls} {subject}

📚 Chapter: {chapter}

❓ {question}
{opts_text}

⬇️ Drop your answer in the comments!

✅ Answer (highlight to see): {answer_text}"""

    if explanation:
        post += f"\n\n💡 {explanation[:200]}"

    post += f"""

─────────────────
🔗 Practice more at cbsemock.org.in
#CBSE #BoardExams #Quest #MCQ #{subject.replace(' ','')} #Class{cls}"""

    return post


# ── News Digest ───────────────────────────────────────────────────────────────
def fetch_news_items(query: str, max_items: int = 3) -> list[dict]:
    """Fetch news from Google News RSS."""
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            tree = ET.parse(r)
    except Exception as e:
        print(f"  [skip news] {query}: {e}")
        return []

    items = []
    for item in tree.findall(".//item")[:max_items]:
        title = item.findtext("title", "").strip()
        link  = item.findtext("link", "").strip()
        import re
        title = re.sub(r'\s+[-–]\s+[\w\s&\.]+$', '', title)
        items.append({"title": title, "link": link})
    return items


def format_news_post(all_items: list[dict]) -> str:
    """Format news as a Facebook post."""
    now = datetime.now(timezone.utc).strftime("%d %b %Y")

    lines = ""
    for i, item in enumerate(all_items[:5], 1):
        lines += f"\n{i}. {item['title']}"

    post = f"""📰 CBSE News Update — {now}

Stay informed with the latest from CBSE Board:
{lines}

🔗 Read more at cbsemock.org.in/news.html

─────────────────
#CBSE #BoardExam2027 #CBSENews #Class10 #Class12 #StudyUpdate"""

    return post


# ── Main ──────────────────────────────────────────────────────────────────────
SUBJECT_EMOJI = {
    "physics": "⚛️", "chemistry": "🧪", "mathematics": "📐", "maths": "📐",
    "biology": "🌿", "science": "🔬", "social": "🌍", "english": "📖",
    "hindi": "📝", "accountancy": "📊", "economics": "📈", "business": "💼",
    "computer": "💻", "cs": "💻", "informatics": "🖥️", "ai": "🤖",
    "physical": "🏃", "bengali": "✍️",
}

def subject_emoji(title: str) -> str:
    t = title.lower()
    for k, v in SUBJECT_EMOJI.items():
        if k in t:
            return v
    return "📚"


def post_notes(tracker, dry_run: bool = False):
    item = tracker.get_next("notes", "facebook")
    if not item:
        print("[SKIP] No notes items.")
        return
    import re
    emoji   = subject_emoji(item["title"])
    cls_match = re.search(r'Class (\d+)', item["title"])
    cls_str = f"Class {cls_match.group(1)}" if cls_match else "CBSE"
    text = (
        f"{emoji} Study Notes — {item['title']}\n\n"
        f"📚 {cls_str} | CBSE Board 2026-27\n\n"
        f"✅ Chapter-wise notes\n"
        f"✅ Important definitions & formulas\n"
        f"✅ Previous year question patterns\n"
        f"✅ Quick revision points\n\n"
        f"🔗 Access Notes: {item['url']}\n\n"
        f"📌 Bookmark cbsemock.org.in for all subjects!\n\n"
        f"#CBSE #StudyNotes #{cls_str.replace(' ','')} #BoardExams2027"
    )
    result = fb_post(text, dry_run=dry_run)
    if not dry_run:
        tracker.mark_posted("notes", item, "facebook")
        tracker.save()
    print(f"[OK] Notes posted: {item['title']} → {result.get('id','n/a')}")


def post_practice(tracker, content_type: str, dry_run: bool = False):
    item = tracker.get_next(content_type, "facebook")
    if not item:
        print(f"[SKIP] No {content_type} items.")
        return
    cls   = "10" if content_type == "practice_10" else "12"
    emoji = subject_emoji(item["title"])
    text = (
        f"📝 Practice Paper — Class {cls}\n\n"
        f"{emoji} {item['title']}\n\n"
        f"🎯 Full-length CBSE pattern paper\n"
        f"⏱️ Time-bound practice\n"
        f"📊 Detailed answer key included\n"
        f"🏆 Score higher in Board Exams 2027\n\n"
        f"🔗 Start Practice: {item['url']}\n\n"
        f"💡 Tip: Attempt under exam conditions for best results!\n\n"
        f"#CBSE #Class{cls} #PracticePaper #MockTest #BoardExams2027"
    )
    result = fb_post(text, dry_run=dry_run)
    if not dry_run:
        tracker.mark_posted(content_type, item, "facebook")
        tracker.save()
    print(f"[OK] {content_type} posted: {item['title']} → {result.get('id','n/a')}")


# ── Festival greetings (mirrors post_festival.py logic, plain text for FB) ───
FESTIVALS_FILE = REPO_ROOT / "festivals.json"
PORTAL_URL     = "https://cbsemock.org.in"

def get_today_festival(override_date=None):
    if not FESTIVALS_FILE.exists():
        return None
    data = json.loads(FESTIVALS_FILE.read_text(encoding="utf-8"))
    today = date.today()
    year  = str(today.year)
    mmdd  = override_date or today.strftime("%m-%d")
    return data.get(year, {}).get(mmdd)

def board_countdown_line():
    today = date.today()
    board_start = date(today.year + (1 if today.month > 8 else 0), 2, 15)
    days = (board_start - today).days
    if days > 180:
        return f"📅 Board exams in ~{days} days — build a strong foundation now!"
    elif days > 90:
        return f"⏳ Board exams in {days} days — shift into focused revision mode!"
    elif days > 30:
        return f"🔥 Only {days} days to Board exams — every day counts!"
    else:
        return f"🚨 Board exams in {days} days — stay calm, stay focused!"

FESTIVAL_MSGS = {
    "diwali": ("🪔 Happy Diwali from CBSE Mock! 🪔\n\nMay the Festival of Lights brighten your path to success!\n✨ Just like a lamp dispels darkness, knowledge dispels doubt.\nLet this Diwali spark a new level of exam preparation! 🔥", "🎯 Use this festive break wisely — attempt a mock test today!"),
    "new year": ("🎉 Happy New Year from CBSE Mock! 🎉\n\nA brand new year — and Board Exams are closer than ever! 📅\nMake 2027 your BEST academic year yet.\nStart strong: revise one chapter today. 💪", "🗓️ New year, new goals — start with a mock test right now!"),
    "republic day": ("🇮🇳 Happy Republic Day from CBSE Mock! 🇮🇳\n\nOn this proud day, we celebrate our Constitution and our nation.\nLet's also celebrate the power of education — the greatest equaliser! 📚", "🎯 Honour the republic by investing in your future — attempt a mock test!"),
    "independence day": ("🇮🇳 Happy Independence Day from CBSE Mock! 🇮🇳\n\nEducation is the foundation of a free, strong nation. 🌟\nMake your future bright — your boards are your first step.", "🎯 Celebrate freedom by freeing yourself from exam stress — practice daily!"),
    "teachers' day": ("👩‍🏫 Happy Teachers' Day from CBSE Mock! 🌸\n\nToday we honour every teacher who shaped a student's life. 🙏\nTo all students — your teachers believe in you. Prove them right! 💪", "📚 The best way to thank your teacher: score your personal best in boards!"),
    "holi": ("🌈 Happy Holi from CBSE Mock! 🌈\n\nMay your life be as colourful as Holi — and your marksheet even brighter! 😄\nHave fun with family and friends today! 🎉", "📖 Come back refreshed tomorrow for some serious board prep!"),
    "christmas": ("🎄 Merry Christmas from CBSE Mock! 🎄\n\nWishing you joy, warmth, and excellent scores in your board exams! 🎁\nMay Santa bring confidence and clarity for your boards! 🌟", "🎯 Holiday season = less distraction. Perfect time for a full mock test!"),
    "dussehra": ("🏹 Happy Dussehra from CBSE Mock! 🏹\n\nLet knowledge conquer confusion, and hard work conquer fear! 💪\nOn this day of victory — defeat your weak chapters today.", "🎯 Dussehra marks the start of the final exam prep sprint. 100 days to boards!"),
    "gandhi jayanti": ("🕊️ Gandhi Jayanti — 2nd October 🇮🇳\n\n\"Live as if you were to die tomorrow. Learn as if you were to live forever.\"\n— Mahatma Gandhi\n\nOn Bapu's birthday, let's commit to learning with sincerity. 📚", "📖 Start a new chapter today — in books and in life!"),
    "guru nanak jayanti": ("🙏 Gurpurab Mubarak from CBSE Mock! 🙏\n\nOn Guru Nanak Dev Ji's Prakash Utsav — seek blessings of wisdom and knowledge.\nGuruji's teachings emphasise honest hard work. That's the only exam strategy that works!", "📖 Dedicate a chapter today in the spirit of Seva and Siksha!"),
}

def post_festival_fb(dry_run=False, override_date=None):
    festival = get_today_festival(override_date)
    if not festival:
        mmdd = override_date or date.today().strftime("%m-%d")
        print(f"[INFO] No festival on {mmdd} — skipping Facebook festival post.")
        return
    name  = festival["name"]
    emoji = festival["emoji"]
    key   = name.lower().strip()
    body, cta = FESTIVAL_MSGS.get(key, (
        f"{emoji} Happy {name} from CBSE Mock! {emoji}\n\nWarm wishes from our entire team! 🎉\nMay this occasion bring you joy, peace, and academic success! 📚",
        "🎯 Celebrate AND prepare — attempt a mock test today!"
    ))
    countdown = board_countdown_line()
    tag = name.replace(" ", "").replace("(", "").replace(")", "").replace("/", "").replace("'", "")
    msg = (
        f"{body}\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"{countdown}\n\n"
        f"{cta}\n\n"
        f"🔗 Practice at {PORTAL_URL}\n\n"
        f"— Team CBSE Mock 🎓\n\n"
        f"#CBSEMock #{tag} #BoardExams2027 #CBSEStudents #ExamPrep"
    )
    result = fb_post(msg, dry_run=dry_run)
    print(f"[OK] Festival post (FB): {name} → {result.get('id','n/a')}")


# ── Afternoon chapter posts (FB text version — no polls) ─────────────────────
CHAPTERS_DIR = REPO_ROOT / "chapters"
LABELS = ["A", "B", "C", "D"]
AFTERNOON_TRACKER = REPO_ROOT / "afternoon-tracker.json"

SUBJ_EMOJI = {
    "physics":"⚛️","chemistry":"🧪","mathematics":"📐","maths":"📐",
    "biology":"🌿","science":"🔬","english":"📖","hindi":"📝",
    "computer":"💻","artificial":"🤖","ai":"🤖","data":"📊",
    "network":"🌐","database":"🗄️","sql":"🗄️","python":"🐍",
    "oop":"🏗️","grammar":"✍️","writing":"✏️","neural":"⚡","machine":"🧠",
}

def get_subj_emoji(text):
    t = text.lower()
    for k, v in SUBJ_EMOJI.items():
        if k in t:
            return v
    return "📚"

def parse_chapter(path):
    text = path.read_text(encoding="utf-8")
    t = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
    title = re.sub(r'<[^>]+>', '', t.group(1)).strip() if t else path.stem
    badge = re.search(r'class="chapter-badge">(.*?)</span>', text, re.S)
    badge_text = badge.group(1).strip() if badge else ""
    cls_m = re.search(r'Class (\d+)', badge_text)
    cls = cls_m.group(1) if cls_m else "12"
    subj_m = re.search(r'Class \d+ · (.+)', badge_text)
    subject = subj_m.group(1).strip() if subj_m else "CBSE"
    qs_match = re.search(r'const QUESTIONS\s*=\s*(\[[\s\S]*?\]);', text)
    if not qs_match:
        return None
    try:
        json_str = re.sub(r'(?<=[{,])\s*([a-zA-Z_]\w*)\s*:', r'"\1":', qs_match.group(1))
        questions = json.loads(json_str)
    except Exception:
        return None
    return {"slug": path.stem, "title": title, "class": cls, "subject": subject,
            "url": f"{PORTAL_URL}/chapters/{path.stem}.html", "questions": questions}

def load_chapters():
    chapters = []
    for p in sorted(CHAPTERS_DIR.glob("*.html")):
        ch = parse_chapter(p)
        if ch and ch["questions"]:
            chapters.append(ch)
    return chapters

def get_afternoon_chapter(key, chapters):
    if not AFTERNOON_TRACKER.exists():
        return random.choice(chapters)
    tracker = json.loads(AFTERNOON_TRACKER.read_text(encoding="utf-8"))
    slugs = [ch["slug"] for ch in chapters]
    slug_map = {ch["slug"]: ch for ch in chapters}
    order_key = f"{key}_order"
    idx_key = f"{key}_idx"
    order = tracker.get(order_key, slugs)
    idx = tracker.get(idx_key, 0)
    if idx >= len(order):
        idx = 0
    slug = order[idx] if order else slugs[0]
    return slug_map.get(slug, chapters[0])

def post_afternoon_fb(dry_run=False):
    chapters = load_chapters()
    if not chapters:
        print("[SKIP] No chapter pages found.")
        return
    random.seed(int(date.today().strftime("%Y%m%d")))

    for key, label, pick_fn in [
        ("flash",    "⚡ Chapter MCQ Flash",          lambda ch: random.choice(ch["questions"])),
        ("mistakes", "⚠️ Common Mistakes Spotlight",  lambda ch: sorted(ch["questions"], key=lambda q: sum(1 for kw in ["common","mistake","confus","often","careful","trick","important"] if kw in q.get("exp","").lower()), reverse=True)[0]),
        ("teacher",  "👩‍🏫 Teacher's Eye",             lambda ch: sorted(ch["questions"], key=lambda q: len(q.get("exp","")), reverse=True)[0]),
    ]:
        ch = get_afternoon_chapter(key, chapters)
        q = pick_fn(ch)
        emoji = get_subj_emoji(ch["subject"] + " " + ch["title"])
        opts = q["opts"]
        ans  = q["ans"]
        ci   = LABELS.index(ans) if ans in LABELS else 0
        exp  = q.get("exp", "")
        correct_text = opts[ci] if ci < len(opts) else ans
        opts_text = "\n".join(f"  {LABELS[i]}) {o}" for i, o in enumerate(opts))

        if key == "flash":
            msg = (
                f"{label}\n\n"
                f"{emoji} {ch['title']} — Class {ch['class']} {ch['subject']}\n\n"
                f"❓ {q['q']}\n\n"
                f"{opts_text}\n\n"
                f"💡 Answer: {ans}) {correct_text}\n"
                f"📝 {exp[:250]}\n\n"
                f"🔗 Practice full chapter: {ch['url']}\n\n"
                f"#CBSE #Class{ch['class']} #{ch['subject'].replace(' ','')} #ChapterMCQ #BoardExams2027"
            )
        elif key == "mistakes":
            wrong_opts = [o for i, o in enumerate(opts) if LABELS[i] != ans]
            trap = wrong_opts[0] if wrong_opts else opts[0]
            msg = (
                f"{label}\n\n"
                f"{emoji} {ch['title']} — Class {ch['class']}\n\n"
                f"🔴 Most students pick the wrong answer here!\n"
                f"❌ Common trap: \"{trap}\"\n\n"
                f"❓ {q['q']}\n\n"
                f"{opts_text}\n\n"
                f"✅ Correct: {ans}) {correct_text}\n"
                f"💡 {exp[:220]}\n\n"
                f"🔗 {ch['url']}\n\n"
                f"#CBSEMistakes #Class{ch['class']} #ExamTips #BoardPrep2027"
            )
        else:  # teacher
            first_sent = re.split(r'(?<=[.!?])\s', exp.strip())[0] if exp else exp
            msg = (
                f"{label}\n\n"
                f"{emoji} {ch['title']} — Class {ch['class']} {ch['subject']}\n\n"
                f"🎓 What examiners always look for:\n\n"
                f"❓ {q['q'][:200]}\n\n"
                f"✅ Correct answer: {correct_text}\n\n"
                f"📝 Examiner's explanation:\n{first_sent[:250]}\n\n"
                f"💡 Knowing the WHY is what separates 90+ scorers!\n\n"
                f"🔗 {ch['url']}\n\n"
                f"#TeachersEye #CBSE #Class{ch['class']} #ExaminerTips #BoardExams2027"
            )
        result = fb_post(msg, dry_run=dry_run)
        print(f"[OK] FB afternoon/{key}: {ch['title']} → {result.get('id','n/a')}")


# ── Lab post (FB version) ─────────────────────────────────────────────────────
def post_lab_fb(tracker, dry_run=False):
    item = tracker.get_next("lab", "facebook")
    if not item:
        print("[SKIP] No lab items.")
        return
    text = (
        f"🧑‍🔬 Lab Activity of the Day\n\n"
        f"📌 {item.get('title','')}\n\n"
        f"{item.get('description','')}\n\n"
        f"🔗 {item.get('url', PORTAL_URL)}\n\n"
        f"#CBSELab #PracticalExam #BoardExams2027 #CBSEMock"
    )
    result = fb_post(text, dry_run=dry_run)
    if not dry_run:
        tracker.mark_posted("lab", item, "facebook")
        tracker.save()
    print(f"[OK] FB lab: {item.get('title','n/a')} → {result.get('id','n/a')}")


def main():
    parser = argparse.ArgumentParser(description="CBSE Mock Facebook auto-poster")
    parser.add_argument("--mode", default="morning",
        choices=["quest","news","notes","practice_10","practice_12","morning","lab_slot","afternoon","festival","evening","all"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--date", help="Force festival date MM-DD")
    args = parser.parse_args()

    sys.path.insert(0, str(REPO_ROOT))
    from social_content_tracker import ContentTracker
    tracker = ContentTracker()

    print(f"Facebook Auto-Poster — mode={args.mode} dry_run={args.dry_run}")
    print(f"Page ID: {PAGE_ID}")

    modes = {
        "morning":  ["festival", "quest", "notes", "practice_10", "practice_12"],
        "lab_slot": ["lab"],
        "afternoon":["afternoon"],
        "festival": ["festival"],
        "evening":  ["news"],
        "all":      ["festival", "quest", "news", "notes", "practice_10", "practice_12", "lab", "afternoon"],
    }
    run_modes = modes.get(args.mode, [args.mode])

    for m in run_modes:
        print(f"\n── {m} ──")
        if m == "quest":
            q = pick_question()
            if q:
                result = fb_post(format_quest_post(q), dry_run=args.dry_run)
                print(f"[OK] Quest posted: {result.get('id','n/a')}")
            else:
                print("[SKIP] No question available.")
        elif m == "news":
            all_items = []
            for q in NEWS_QUERIES:
                all_items.extend(fetch_news_items(q))
            seen, unique = set(), []
            for item in all_items:
                key = item["title"][:50].lower()
                if key not in seen:
                    seen.add(key)
                    unique.append(item)
            if unique:
                result = fb_post(format_news_post(unique[:5]), dry_run=args.dry_run)
                print(f"[OK] News posted: {result.get('id','n/a')}")
            else:
                print("[SKIP] No news items fetched.")
        elif m == "notes":
            post_notes(tracker, dry_run=args.dry_run)
        elif m == "practice_10":
            post_practice(tracker, "practice_10", dry_run=args.dry_run)
        elif m == "practice_12":
            post_practice(tracker, "practice_12", dry_run=args.dry_run)
        elif m == "festival":
            post_festival_fb(dry_run=args.dry_run, override_date=args.date)
        elif m == "afternoon":
            post_afternoon_fb(dry_run=args.dry_run)
        elif m == "lab":
            post_lab_fb(tracker, dry_run=args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
