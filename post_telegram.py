#!/usr/bin/env python3
"""
post_telegram.py — CBSE Mock Telegram Channel/Group Auto-Poster
────────────────────────────────────────────────────────────────
Posts daily content to the CBSE Mock Telegram channel or group:
  • Morning: Quest of the Day (MCQ with inline poll)
  • Evening: CBSE news digest

Environment variables (set as GitHub Secrets):
  TELEGRAM_BOT_TOKEN — Token from @BotFather
  TELEGRAM_CHAT_ID   — Channel (@cbsemock) or group chat ID (-100xxxxxxxxxx)

Usage:
  python3 post_telegram.py --mode quest    # Post Quest of the Day
  python3 post_telegram.py --mode news     # Post news digest
  python3 post_telegram.py --mode both     # Post both (default)
  python3 post_telegram.py --dry-run       # Preview without posting

Setup:
  1. Create bot via @BotFather → get TELEGRAM_BOT_TOKEN
  2. Add bot to your channel/group as Admin
  3. Get chat ID:
     - For channel: @yourchannel or -100xxxxxxxxxx
     - For group: forward a message to @userinfobot or run get_chat_id()
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
CATALOGUE_PATH = REPO_ROOT / "quest" / "data" / "catalogue-entry.json"

TG_API_BASE  = "https://api.telegram.org/bot"
BOT_TOKEN    = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID      = os.environ.get("TELEGRAM_CHAT_ID", "")

NEWS_QUERIES = [
    "CBSE board exam 2027",
    "CBSE date sheet 2027",
    "CBSE result 2026",
]

# ── Telegram API ──────────────────────────────────────────────────────────────
def tg_request(method: str, payload: dict, dry_run: bool = False) -> dict:
    """Make a Telegram Bot API request."""
    if dry_run:
        print(f"\n[DRY RUN] Telegram API: {method}")
        print(json.dumps(payload, indent=2, ensure_ascii=False)[:500])
        return {"ok": True, "result": {"message_id": 0}}

    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set. Add it to GitHub Secrets.")
    if not CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID not set. Add it to GitHub Secrets.")

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


def tg_send_message(text: str, dry_run: bool = False) -> dict:
    return tg_request("sendMessage", {
        "chat_id":    CHAT_ID,
        "text":       text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }, dry_run)


def tg_send_poll(question: str, options: list[str],
                 correct_option_idx: int, explanation: str = "",
                 dry_run: bool = False) -> dict:
    """Send a quiz-style poll (shows correct answer after voting)."""
    return tg_request("sendPoll", {
        "chat_id":             CHAT_ID,
        "question":            question[:300],
        "options":             [o[:100] for o in options[:10]],
        "type":                "quiz",
        "correct_option_id":   correct_option_idx,
        "explanation":         explanation[:200] if explanation else "",
        "is_anonymous":        True,
        "open_period":         86400,   # poll open for 24 hours
    }, dry_run)


# ── Quest of the Day ──────────────────────────────────────────────────────────
def pick_question() -> dict | None:
    """Pick a random MCQ from the current month's question bank."""
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
    """Post Quest of the Day as a Telegram quiz poll + context message."""
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

    # Build ordered options list
    if isinstance(options_raw, dict):
        keys    = sorted(options_raw.keys())
        options = [options_raw[k] for k in keys]
        try:
            correct_idx = keys.index(answer)
        except ValueError:
            correct_idx = 0
    elif isinstance(options_raw, list):
        options = options_raw
        correct_idx = 0
    else:
        print("[SKIP] Unrecognised options format.")
        return

    # Send context message first
    header = (
        f"🎯 <b>Quest of the Day</b>\n"
        f"📚 Class {cls} | {subject}\n"
        f"📖 Chapter: {chapter}\n\n"
        f"Test your knowledge — vote in the poll below! 👇\n\n"
        f"<i>Practice more → <a href='https://cbsemock.org.in'>cbsemock.org.in</a></i>"
    )
    tg_send_message(header, dry_run)

    # Send quiz poll
    poll_question = f"[Class {cls} {subject}] {question}"
    result = tg_send_poll(
        question=poll_question,
        options=options,
        correct_option_idx=correct_idx,
        explanation=explanation[:200] if explanation else f"Answer: {answer}",
        dry_run=dry_run,
    )
    print(f"[OK] Quest poll posted: message_id={result.get('result',{}).get('message_id','n/a')}")


# ── News Digest ───────────────────────────────────────────────────────────────
def fetch_news(query: str, max_items: int = 3) -> list[dict]:
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
        title = re.sub(r'\s+[-–]\s+[\w\s&\.]+$', '', title)
        items.append({"title": title, "link": link})
    return items


def post_news(dry_run: bool = False):
    """Post CBSE news digest."""
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
        lines += f"\n{i}. {item['title']}"
        if item.get("link"):
            lines += f"\n   <a href='{item['link']}'>Read more</a>"

    text = (
        f"📰 <b>CBSE News — {now}</b>\n"
        f"{lines}\n\n"
        f"🔗 <a href='https://cbsemock.org.in/news.html'>More updates at cbsemock.org.in</a>\n\n"
        f"#CBSE #BoardExam2027 #CBSENews"
    )

    result = tg_send_message(text, dry_run)
    print(f"[OK] News posted: message_id={result.get('result',{}).get('message_id','n/a')}")


# ── Helper: Get Chat ID ───────────────────────────────────────────────────────
def get_chat_id():
    """Print recent updates to find your chat ID."""
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
        msg = update.get("message") or update.get("channel_post", {})
        chat = msg.get("chat", {})
        print(f"Chat ID: {chat.get('id')}  Type: {chat.get('type')}  Title: {chat.get('title') or chat.get('username')}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="CBSE Mock Telegram auto-poster")
    parser.add_argument("--mode",        choices=["quest", "news", "both"], default="both")
    parser.add_argument("--dry-run",     action="store_true")
    parser.add_argument("--get-chat-id", action="store_true",
                        help="Print recent chat IDs to find your group/channel ID")
    args = parser.parse_args()

    if args.get_chat_id:
        get_chat_id()
        return

    print(f"Telegram Auto-Poster — mode={args.mode} dry_run={args.dry_run}")
    print(f"Chat ID: {CHAT_ID or '(not set)'}")

    if args.mode in ("quest", "both"):
        print("\n── Quest of the Day ──")
        post_quest(dry_run=args.dry_run)

    if args.mode in ("news", "both"):
        print("\n── News Digest ──")
        post_news(dry_run=args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
