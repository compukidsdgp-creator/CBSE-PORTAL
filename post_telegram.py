#!/usr/bin/env python3
"""
post_telegram.py — CBSE Mock Telegram Channel/Group Auto-Poster
────────────────────────────────────────────────────────────────
Posts 5 types of daily content to the CBSE Mock Telegram group/channel:
  1. quest        — Quest of the Day MCQ poll (7:00 AM IST)
  2. news         — CBSE news digest (6:00 PM IST)
  3. notes        — Subject notes page (rotating, no repeat until all done)
  4. practice_10  — Class 10 practice paper (rotating)
  5. practice_12  — Class 12 practice paper (rotating)

Environment variables (GitHub Secrets):
  TELEGRAM_BOT_TOKEN — Token from @BotFather
  TELEGRAM_CHAT_ID   — Channel (@cbsemock) or group chat ID (-100xxxxxxxxxx)

Usage:
  python3 post_telegram.py --mode quest
  python3 post_telegram.py --mode news
  python3 post_telegram.py --mode notes
  python3 post_telegram.py --mode practice_10
  python3 post_telegram.py --mode practice_12
  python3 post_telegram.py --mode morning    # quest + notes + practice_10 + practice_12
  python3 post_telegram.py --mode evening    # news
  python3 post_telegram.py --mode all        # everything
  python3 post_telegram.py --dry-run         # preview without posting
  python3 post_telegram.py --get-chat-id     # find your group/channel ID
"""

import os
import sys
import json
import random
import argparse
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import re
from datetime import datetime, timezone
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
REPO_ROOT      = Path(__file__).parent
QUESTIONS_DIR  = REPO_ROOT / "quest" / "data" / "questions"

TG_API_BASE  = "https://api.telegram.org/bot"
BOT_TOKEN    = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID      = os.environ.get("TELEGRAM_CHAT_ID", "")

NEWS_QUERIES = [
    "CBSE board exam 2027",
    "CBSE date sheet 2027",
    "CBSE result 2026",
]

# Subject emoji map
SUBJECT_EMOJI = {
    "physics": "⚛️", "chemistry": "🧪", "mathematics": "📐", "maths": "📐",
    "biology": "🌿", "science": "🔬", "social": "🌍", "history": "🏛️",
    "geography": "🗺️", "english": "📖", "hindi": "📝", "accountancy": "📊",
    "economics": "📈", "business": "💼", "computer": "💻", "cs": "💻",
    "informatics": "🖥️", "ai": "🤖", "physical": "🏃", "bengali": "✍️",
}

def subject_emoji(title: str) -> str:
    t = title.lower()
    for k, v in SUBJECT_EMOJI.items():
        if k in t:
            return v
    return "📚"


# ── Telegram API ──────────────────────────────────────────────────────────────
def tg_request(method: str, payload: dict, dry_run: bool = False) -> dict:
    if dry_run:
        print(f"\n[DRY RUN] Telegram.{method}:")
        print(json.dumps(payload, indent=2, ensure_ascii=False)[:600])
        return {"ok": True, "result": {"message_id": 0}}

    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set.")
    if not CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID not set.")

    url  = f"{TG_API_BASE}{BOT_TOKEN}/{method}"
    data = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(url, data=data,
                                   headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"Telegram API error {e.code}: {body}")


def tg_send(text: str, dry_run: bool = False) -> dict:
    return tg_request("sendMessage", {
        "chat_id":    CHAT_ID,
        "text":       text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }, dry_run)


def tg_poll(question: str, options: list, correct_idx: int,
            explanation: str = "", dry_run: bool = False) -> dict:
    return tg_request("sendPoll", {
        "chat_id":           CHAT_ID,
        "question":          question[:300],
        "options":           [o[:100] for o in options[:10]],
        "type":              "quiz",
        "correct_option_id": correct_idx,
        "explanation":       explanation[:200] if explanation else "",
        "is_anonymous":      True,
        "open_period":       86400,
    }, dry_run)


# ── 1. Quest of the Day ───────────────────────────────────────────────────────
def pick_question() -> dict | None:
    if not QUESTIONS_DIR.exists():
        return None
    q_files = [f for f in QUESTIONS_DIR.iterdir()
               if f.suffix == ".json" and "manifest" not in f.name]
    if not q_files:
        return None
    random.seed(datetime.now(timezone.utc).toordinal())
    q_file = random.choice(q_files)
    with open(q_file, encoding="utf-8") as f:
        data = json.load(f)
    questions = data.get("questions", [])
    mcqs = [q for q in questions if q.get("type") == "MCQ"
            and isinstance(q.get("options"), dict)
            and len(q["options"]) >= 2]
    pool = mcqs if mcqs else questions
    return random.choice(pool) if pool else None


def post_quest(dry_run: bool = False):
    q = pick_question()
    if not q:
        print("[SKIP] No question available.")
        return

    subject     = q.get("subject", "CBSE")
    chapter     = q.get("chapter", "")
    cls         = q.get("class", "")
    question    = q.get("question", "")
    options_raw = q.get("options", {})
    answer      = q.get("answer", "")
    explanation = q.get("explanation", "")
    difficulty  = q.get("difficulty", "Medium")
    emoji       = subject_emoji(subject)

    if isinstance(options_raw, dict):
        keys        = sorted(options_raw.keys())
        options     = [options_raw[k] for k in keys]
        correct_idx = keys.index(answer) if answer in keys else 0
    elif isinstance(options_raw, list):
        options     = options_raw
        correct_idx = 0
    else:
        print("[SKIP] Unrecognised options format.")
        return

    diff_stars = {"Easy": "⭐", "Medium": "⭐⭐", "Hard": "⭐⭐⭐"}.get(difficulty, "⭐⭐")

    header = (
        f"🎯 <b>Quest of the Day</b>\n\n"
        f"{emoji} <b>{subject}</b> | Class {cls}\n"
        f"📖 Chapter: {chapter}\n"
        f"🎚️ Difficulty: {diff_stars}\n\n"
        f"Test your knowledge — vote in the poll below! 👇\n\n"
        f"🔗 <a href='https://cbsemock.org.in/quest/'>More Quests</a> | "
        f"<a href='https://cbsemock.org.in'>cbsemock.org.in</a>"
    )
    tg_send(header, dry_run)

    result = tg_poll(
        question=f"[Class {cls} {subject}] {question}",
        options=options,
        correct_idx=correct_idx,
        explanation=explanation[:200] if explanation else f"Answer: {answer}",
        dry_run=dry_run,
    )
    print(f"[OK] Quest posted: {result.get('result',{}).get('message_id','n/a')}")


# ── 2. News Digest ────────────────────────────────────────────────────────────
def fetch_news(query: str, max_items: int = 3) -> list[dict]:
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            tree = ET.parse(r)
    except Exception as e:
        print(f"  [skip] {query}: {e}")
        return []
    items = []
    for item in tree.findall(".//item")[:max_items]:
        title = re.sub(r'\s+[-–]\s+[\w\s&\.]+$', '',
                       item.findtext("title", "").strip())
        link  = item.findtext("link", "").strip()
        items.append({"title": title, "link": link})
    return items


def post_news(dry_run: bool = False):
    all_items = []
    for q in NEWS_QUERIES:
        all_items.extend(fetch_news(q))
    seen, unique = set(), []
    for item in all_items:
        key = item["title"][:50].lower()
        if key not in seen:
            seen.add(key)
            unique.append(item)

    if not unique:
        print("[SKIP] No news fetched.")
        return

    now   = datetime.now(timezone.utc).strftime("%d %b %Y")
    lines = ""
    for i, item in enumerate(unique[:5], 1):
        lines += f"\n\n{i}. {item['title']}"
        if item.get("link"):
            lines += f"\n   📎 <a href='{item['link']}'>Read →</a>"

    text = (
        f"📰 <b>CBSE News Update — {now}</b>\n"
        f"{'─'*32}"
        f"{lines}\n\n"
        f"{'─'*32}\n"
        f"🔗 <a href='https://cbsemock.org.in/news.html'>Full news at cbsemock.org.in</a>\n\n"
        f"#CBSE #BoardExam2027 #CBSENews #Class10 #Class12"
    )
    result = tg_send(text, dry_run)
    print(f"[OK] News posted: {result.get('result',{}).get('message_id','n/a')}")


# ── 3. Subject Notes ──────────────────────────────────────────────────────────
def post_notes(tracker, dry_run: bool = False):
    item = tracker.get_next("notes", "telegram")
    if not item:
        print("[SKIP] No notes items in tracker.")
        return

    emoji = subject_emoji(item["title"])
    # Extract class number from title
    cls_match = re.search(r'Class (\d+)', item["title"])
    cls_str = f"Class {cls_match.group(1)}" if cls_match else "CBSE"

    text = (
        f"{emoji} <b>Study Notes — {item['title']}</b>\n\n"
        f"📚 <b>{cls_str} | CBSE Board 2026-27</b>\n\n"
        f"✅ Chapter-wise notes\n"
        f"✅ Important definitions & formulas\n"
        f"✅ Previous year question patterns\n"
        f"✅ Quick revision points\n\n"
        f"🔗 <a href='{item['url']}'>Access Notes Now →</a>\n\n"
        f"📌 Bookmark cbsemock.org.in for all subjects!\n\n"
        f"#CBSE #StudyNotes #{cls_str.replace(' ','')} #BoardExams2027"
    )
    result = tg_send(text, dry_run)
    if not dry_run:
        tracker.mark_posted("notes", item, "telegram")
        tracker.save()
    print(f"[OK] Notes posted: {item['title']} → msg {result.get('result',{}).get('message_id','n/a')}")


# ── 4 & 5. Practice Papers ────────────────────────────────────────────────────
def post_practice(tracker, content_type: str, dry_run: bool = False):
    item = tracker.get_next(content_type, "telegram")
    if not item:
        print(f"[SKIP] No {content_type} items in tracker.")
        return

    cls = "10" if content_type == "practice_10" else "12"
    emoji = subject_emoji(item["title"])

    text = (
        f"📝 <b>Practice Paper — Class {cls}</b>\n\n"
        f"{emoji} <b>{item['title']}</b>\n\n"
        f"🎯 Full-length CBSE pattern paper\n"
        f"⏱️ Time-bound practice\n"
        f"📊 Detailed answer key included\n"
        f"🏆 Score higher in Board Exams 2027\n\n"
        f"🔗 <a href='{item['url']}'>Start Practice Now →</a>\n\n"
        f"💡 Tip: Attempt under exam conditions for best results!\n\n"
        f"#CBSE #Class{cls} #PracticePaper #MockTest #BoardExams2027"
    )
    result = tg_send(text, dry_run)
    if not dry_run:
        tracker.mark_posted(content_type, item, "telegram")
        tracker.save()
    print(f"[OK] {content_type} posted: {item['title']} → msg {result.get('result',{}).get('message_id','n/a')}")


# ── 6. Virtual Lab Highlight ──────────────────────────────────────────────────
def post_lab(tracker, dry_run: bool = False):
    item = tracker.get_next("lab", "telegram")
    if not item:
        print("[SKIP] No lab items in tracker.")
        return

    # Parse subject from title: "Name — Subject Lab"
    parts   = item["title"].split(" — ")
    exp_name = parts[0].strip()
    subject  = parts[1].replace(" Lab", "").strip() if len(parts) > 1 else "Science"
    emoji    = subject_emoji(subject)

    text = (
        f"🧪 <b>Today's Hands-On Highlight</b>\n\n"
        f"{emoji} <b>{exp_name}</b>\n"
        f"📋 Subject: {subject}\n\n"
        f"🔬 What you'll explore:\n"
        f"• Step-by-step interactive simulation\n"
        f"• Observe results in real time\n"
        f"• Understand the concept behind the experiment\n"
        f"• CBSE board exam relevance explained\n\n"
        f"🧑‍🔬 Try it yourself — no lab equipment needed!\n\n"
        f"🔗 <a href='{item['url']}'>Open Virtual Lab →</a>\n\n"
        f"#VirtualLab #CBSE #{subject.replace(' ','')} #HandsOn #BoardExams2027"
    )
    result = tg_send(text, dry_run)
    if not dry_run:
        tracker.mark_posted("lab", item, "telegram")
        tracker.save()
    print(f"[OK] Lab posted: {exp_name} → msg {result.get('result',{}).get('message_id','n/a')}")


# ── 7. Weekly Focus ───────────────────────────────────────────────────────────
def post_weekly_focus(tracker, dry_run: bool = False):
    item = tracker.get_weekly_focus("telegram")
    if not item:
        print("[SKIP] No weekly focus items.")
        return

    # Get description from WEEKLY_FOCUS_TOPICS
    from social_content_tracker import WEEKLY_FOCUS_TOPICS
    desc = ""
    for topic, d, url in WEEKLY_FOCUS_TOPICS:
        if topic == item["title"]:
            desc = d
            break

    emoji = subject_emoji(item["title"])

    text = (
        f"📌 <b>Weekly Focus Area</b>\n\n"
        f"{emoji} <b>{item['title']}</b>\n\n"
        f"🎯 This week, master these key concepts:\n"
        f"<i>{desc}</i>\n\n"
        f"📅 Dedicate 30 minutes daily to this topic\n"
        f"📝 Solve 5 questions per concept\n"
        f"🔄 Revise on Sunday before next week's focus\n\n"
        f"🔗 <a href='{item['url']}'>Study Resources →</a>\n\n"
        f"💪 Consistency beats intensity — one week at a time!\n\n"
        f"#WeeklyFocus #CBSE #BoardExams2027 #StudyPlan #{item['title'].replace(' ','').replace('&','')[:20]}"
    )
    result = tg_send(text, dry_run)
    if not dry_run:
        tracker.mark_posted("weekly_focus", item, "telegram")
        tracker.save()
    print(f"[OK] Weekly focus posted: {item['title']} → msg {result.get('result',{}).get('message_id','n/a')}")


# ── Helper: Get Chat ID ───────────────────────────────────────────────────────
def get_chat_id():
    if not BOT_TOKEN:
        print("Set TELEGRAM_BOT_TOKEN first.")
        return
    url = f"{TG_API_BASE}{BOT_TOKEN}/getUpdates"
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.loads(r.read())
    if not data.get("result"):
        print("No updates yet. Send a message to your bot/group first, then run again.")
        return
    for update in data["result"][-5:]:
        msg  = update.get("message") or update.get("channel_post", {})
        chat = msg.get("chat", {})
        print(f"Chat ID: {chat.get('id')}  Type: {chat.get('type')}  "
              f"Title/User: {chat.get('title') or chat.get('username')}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="CBSE Mock Telegram auto-poster")
    parser.add_argument("--mode", default="morning",
        choices=["quest","news","notes","practice_10","practice_12","lab","weekly_focus","morning","lab_slot","evening","all"])
    parser.add_argument("--dry-run",     action="store_true")
    parser.add_argument("--get-chat-id", action="store_true")
    args = parser.parse_args()

    if args.get_chat_id:
        get_chat_id()
        return

    # Import tracker only when needed (avoids import error if file missing)
    from social_content_tracker import ContentTracker
    tracker = ContentTracker()

    print(f"Telegram Poster — mode={args.mode} dry_run={args.dry_run}")

    modes = {
        "morning": ["quest", "notes", "practice_10", "practice_12", "weekly_focus"],
        "lab_slot": ["lab"],
        "evening": ["news"],
        "all":     ["quest", "news", "notes", "practice_10", "practice_12", "lab", "weekly_focus"],
    }
    run_modes = modes.get(args.mode, [args.mode])

    for m in run_modes:
        print(f"\n── {m} ──")
        if m == "quest":
            post_quest(dry_run=args.dry_run)
        elif m == "news":
            post_news(dry_run=args.dry_run)
        elif m == "notes":
            post_notes(tracker, dry_run=args.dry_run)
        elif m == "practice_10":
            post_practice(tracker, "practice_10", dry_run=args.dry_run)
        elif m == "practice_12":
            post_practice(tracker, "practice_12", dry_run=args.dry_run)
        elif m == "lab":
            post_lab(tracker, dry_run=args.dry_run)
        elif m == "weekly_focus":
            post_weekly_focus(tracker, dry_run=args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
