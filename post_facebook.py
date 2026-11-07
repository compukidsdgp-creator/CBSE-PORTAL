#!/usr/bin/env python3
"""
post_facebook.py — CBSE Mock Facebook Page Auto-Poster
───────────────────────────────────────────────────────
Posts daily content to the CBSEMock Facebook page:
  • Morning: Quest of the Day (MCQ from current month's question bank)
  • Evening: Top CBSE news headlines

Environment variables (set as GitHub Secrets):
  FB_PAGE_ID           — Facebook Page ID (61596243964780)
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
import random
import argparse
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
REPO_ROOT   = Path(__file__).parent
QUESTIONS_DIR = REPO_ROOT / "quest" / "data" / "questions"
CATALOGUE_PATH = REPO_ROOT / "quest" / "data" / "catalogue-entry.json"

FB_API_VERSION = "v27.0"
FB_API_BASE    = f"https://graph.facebook.com/{FB_API_VERSION}"

PAGE_ID    = os.environ.get("FB_PAGE_ID", "61596243964780")
PAGE_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN", "")

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
def main():
    parser = argparse.ArgumentParser(description="CBSE Mock Facebook auto-poster")
    parser.add_argument("--mode",    choices=["quest", "news", "both"], default="both")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"Facebook Auto-Poster — mode={args.mode} dry_run={args.dry_run}")
    print(f"Page ID: {PAGE_ID}")

    if args.mode in ("quest", "both"):
        print("\n── Quest of the Day ──")
        q = pick_question()
        if q:
            post_text = format_quest_post(q)
            result = fb_post(post_text, dry_run=args.dry_run)
            print(f"[OK] Quest posted: {result.get('id', 'n/a')}")
        else:
            print("[SKIP] No question available.")

    if args.mode in ("news", "both"):
        print("\n── News Digest ──")
        all_items = []
        for q in NEWS_QUERIES:
            all_items.extend(fetch_news_items(q))
        # Deduplicate
        seen, unique = set(), []
        for item in all_items:
            key = item["title"][:50].lower()
            if key not in seen:
                seen.add(key)
                unique.append(item)

        if unique:
            post_text = format_news_post(unique[:5])
            result = fb_post(post_text, dry_run=args.dry_run)
            print(f"[OK] News posted: {result.get('id', 'n/a')}")
        else:
            print("[SKIP] No news items fetched.")

    print("\nDone.")


if __name__ == "__main__":
    main()
