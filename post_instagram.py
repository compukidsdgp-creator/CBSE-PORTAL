#!/usr/bin/env python3
"""
post_instagram.py — CBSE Mock Instagram Auto-Poster
─────────────────────────────────────────────────────
Posts daily content to the @cbsemock Instagram Business account
via the Instagram Graph API (image + caption).

Instagram requires a publicly accessible image URL for every post.
We serve branded images from the social-images/ folder in this repo
via GitHub raw URLs (12 design variants per post type, rotated daily).

Image types available (12 variants each):
  study_notes, practice_papers, virtual_lab, quest_zone,
  weekly_challenge, exam_tip, python_tip, ai_concept,
  answer_key, portal_overview
  plus: branded_poster_01, branded_poster_02

Environment variables (GitHub Secrets):
  INSTAGRAM_ACCOUNT_ID  — IG Business Account ID (17841480792360992)
  INSTAGRAM_ACCESS_TOKEN — Page Access Token with instagram_content_publish

Usage:
  python3 post_instagram.py --mode morning
  python3 post_instagram.py --mode notes
  python3 post_instagram.py --mode lab
  python3 post_instagram.py --mode promo_quest
  python3 post_instagram.py --dry-run
"""

import os
import sys
import json
import re
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone, date
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
REPO_ROOT    = Path(__file__).parent
IG_API_BASE  = "https://graph.facebook.com/v27.0"
PORTAL_URL   = "https://cbsemock.org.in"

IG_ACCOUNT_ID  = os.environ.get("INSTAGRAM_ACCOUNT_ID", "17841480792360992")
IG_ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")

# ── Branded image variants (GitHub raw URLs) ──────────────────────────────────
# 12 design variants per post type, served from social-images/ in this repo.
# Rotation: pick variant by (day_of_year % 12) so each day a fresh design.
_GITHUB_RAW = "https://raw.githubusercontent.com/compukidsdgp-creator/CBSE-PORTAL/main/social-images"

IMAGE_TYPES = [
    "study_notes", "practice_papers", "virtual_lab", "quest_zone",
    "weekly_challenge", "exam_tip", "python_tip", "ai_concept",
    "answer_key", "portal_overview",
]

# Build URLs dict: type -> [v01..v12]
BRANDED_IMAGES: dict[str, list[str]] = {
    t: [f"{_GITHUB_RAW}/{t}_v{i:02d}.jpg" for i in range(1, 13)]
    for t in IMAGE_TYPES
}
# Single-variant extras
BRANDED_IMAGES["branded_poster_01"] = [f"{_GITHUB_RAW}/branded_poster_01.jpg"]
BRANDED_IMAGES["branded_poster_02"] = [f"{_GITHUB_RAW}/branded_poster_02.jpg"]

def _day_variant(n: int = 12) -> int:
    """Return today's 0-based variant index (wraps over n variants)."""
    return date.today().timetuple().tm_yday % n

from promo_config import poster_url, month_name   # weekend promo posters

def get_image_url(title: str = "", post_type: str = "study_notes") -> str:
    """
    Return a branded image URL.
    post_type must be one of IMAGE_TYPES (or branded_poster_01/02).
    Falls back to study_notes if type is unknown.
    Rotates through 12 variants based on day-of-year.
    """
    variants = BRANDED_IMAGES.get(post_type) or BRANDED_IMAGES["study_notes"]
    idx = _day_variant(len(variants))
    return variants[idx]


# ── Instagram API helpers ─────────────────────────────────────────────────────
def ig_post(caption: str, image_url: str, dry_run: bool = False) -> dict:
    """
    Post an image + caption to Instagram via the Graph API.
    Two-step: 1) create media container, 2) publish it.
    """
    if dry_run:
        print(f"\n[DRY-RUN] Instagram post preview:")
        print(f"  Image: {image_url}")
        print(f"  Caption ({len(caption)} chars):\n{caption}\n")
        return {"id": "dry-run"}

    if not IG_ACCESS_TOKEN:
        print("[ERROR] INSTAGRAM_ACCESS_TOKEN not set.")
        return {}

    # Step 1: Create media container
    create_url = f"{IG_API_BASE}/{IG_ACCOUNT_ID}/media"
    payload = urllib.parse.urlencode({
        "image_url":   image_url,
        "caption":     caption,
        "access_token": IG_ACCESS_TOKEN,
    }).encode()

    try:
        with urllib.request.urlopen(create_url, data=payload, timeout=30) as r:
            container = json.loads(r.read())
    except urllib.error.HTTPError as e:
        err = json.loads(e.read())
        print(f"[ERROR] Media container creation failed: {err}")
        return {}

    container_id = container.get("id")
    if not container_id:
        print(f"[ERROR] No container ID returned: {container}")
        return {}

    print(f"[INFO] Media container created: {container_id}")

    # Step 1b: Poll until container status is FINISHED (up to 30s)
    status_url = (
        f"{IG_API_BASE}/{container_id}"
        f"?fields=status_code&access_token={IG_ACCESS_TOKEN}"
    )
    for attempt in range(6):
        time.sleep(5)
        try:
            with urllib.request.urlopen(status_url, timeout=15) as r:
                status_data = json.loads(r.read())
        except Exception as e:
            print(f"[WARN] Status check failed: {e}")
            continue
        status_code = status_data.get("status_code", "")
        print(f"[INFO] Container status ({attempt+1}): {status_code}")
        if status_code == "FINISHED":
            break
        if status_code == "ERROR":
            print(f"[ERROR] Container processing failed: {status_data}")
            return {}
    else:
        print("[WARN] Container not FINISHED after 30s — attempting publish anyway")

    # Step 2: Publish the container
    publish_url = f"{IG_API_BASE}/{IG_ACCOUNT_ID}/media_publish"
    publish_payload = urllib.parse.urlencode({
        "creation_id":  container_id,
        "access_token": IG_ACCESS_TOKEN,
    }).encode()

    try:
        with urllib.request.urlopen(publish_url, data=publish_payload, timeout=30) as r:
            result = json.loads(r.read())
            print(f"[OK] Instagram post published: {result.get('id','n/a')}")
            return result
    except urllib.error.HTTPError as e:
        err = json.loads(e.read())
        print(f"[ERROR] Publish failed: {err}")
        return {}


# ── Subject emoji helper ──────────────────────────────────────────────────────
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


# ── Post functions ────────────────────────────────────────────────────────────

def post_notes(tracker, dry_run=False):
    item = tracker.get_next("notes", "instagram")
    if not item:
        print("[SKIP] No notes items.")
        return
    emoji = subject_emoji(item["title"])
    cls_match = re.search(r'Class (\d+)', item["title"])
    cls_str = f"Class {cls_match.group(1)}" if cls_match else "CBSE"
    caption = (
        f"{emoji} Study Notes — {item['title']}\n\n"
        f"📚 {cls_str} | CBSE Board 2026-27\n\n"
        f"✅ Chapter-wise notes\n"
        f"✅ Important definitions & formulas\n"
        f"✅ Previous year question patterns\n"
        f"✅ Quick revision points\n\n"
        f"🔗 {item['url']}\n\n"
        f"📌 Bookmark cbsemock.org.in for all subjects!\n\n"
        f"#CBSE #StudyNotes #{cls_str.replace(' ','')} #BoardExams2027 #CBSEMock"
    )
    result = ig_post(caption, get_image_url(post_type="study_notes"), dry_run)
    if not dry_run and result.get("id"):
        tracker.mark_posted("notes", item, "instagram")
        tracker.save()
    print(f"[OK] IG Notes: {item['title']}")


def post_practice(tracker, content_type, dry_run=False):
    item = tracker.get_next(content_type, "instagram")
    if not item:
        print(f"[SKIP] No {content_type} items.")
        return
    cls = "10" if content_type == "practice_10" else "12"
    emoji = subject_emoji(item["title"])
    caption = (
        f"📝 Practice Paper — Class {cls}\n\n"
        f"{emoji} {item['title']}\n\n"
        f"🎯 Full-length CBSE pattern paper\n"
        f"⏱️ Time-bound practice\n"
        f"📊 Detailed answer key included\n"
        f"🏆 Score higher in Board Exams 2027\n\n"
        f"🔗 {item['url']}\n\n"
        f"💡 Attempt under exam conditions for best results!\n\n"
        f"#CBSE #Class{cls} #MockTest #PracticePaper #BoardExams2027 #CBSEMock"
    )
    result = ig_post(caption, get_image_url(post_type="practice_papers"), dry_run)
    if not dry_run and result.get("id"):
        tracker.mark_posted(content_type, item, "instagram")
        tracker.save()
    print(f"[OK] IG {content_type}: {item['title']}")


def post_lab(tracker, dry_run=False):
    item = tracker.get_next("lab", "instagram")
    if not item:
        print("[SKIP] No lab items.")
        return
    parts = item["title"].split(" — ")
    exp_name = parts[0].strip()
    subject = parts[1].replace(" Lab", "").strip() if len(parts) > 1 else "Science"
    caption = (
        f"🧪 Virtual Lab Highlight\n\n"
        f"🔬 {exp_name}\n"
        f"📋 Subject: {subject}\n\n"
        f"• Step-by-step interactive simulation\n"
        f"• Observe results in real time\n"
        f"• CBSE board exam relevance explained\n\n"
        f"🧑‍🔬 No lab equipment needed!\n\n"
        f"🔗 {item['url']}\n\n"
        f"#VirtualLab #CBSE #{subject.replace(' ','')} #HandsOn #BoardExams2027 #CBSEMock"
    )
    result = ig_post(caption, get_image_url(post_type="virtual_lab"), dry_run)
    if not dry_run and result.get("id"):
        tracker.mark_posted("lab", item, "instagram")
        tracker.save()
    print(f"[OK] IG Lab: {exp_name}")


def post_promo_quest(dry_run=False):
    caption = (
        "🏆 Have You Tried Our Monthly Quest?\n\n"
        "Every month — brand-new MCQ challenges for CBSE board prep!\n\n"
        "🎯 What's in a Quest?\n"
        "• High-difficulty MCQs — Class 10 & 12\n"
        "• New set every month\n"
        "• Instant score + answer explanations\n\n"
        "📲 How to Attempt:\n"
        "1️⃣ Open cbsemock.org.in/quest\n"
        "2️⃣ Select your subject\n"
        "3️⃣ Submit → see your score instantly!\n\n"
        f"🔥 {month_name()} Quest is LIVE NOW!\n\n"
        f"🔗 {PORTAL_URL}/quest/\n\n"
        "#Quest #CBSE #MCQ #BoardExams2027 #Class10 #Class12 #CBSEMock"
    )
    ig_post(caption, poster_url("promo_quest"), dry_run)
    print("[OK] IG Promo Quest")


def post_promo_mock(dry_run=False):
    caption = (
        "📝 15 Full-Length CBSE Board Mock Tests — FREE!\n\n"
        "The closest simulation to your actual board paper!\n\n"
        "✅ 15 complete practice papers per subject\n"
        "✅ Latest CBSE pattern\n"
        "✅ Detailed answer keys included\n"
        "✅ Class 10 & Class 12 core subjects\n\n"
        "📚 Subjects:\n"
        "🔵 Class 10: Science · Maths · SST · English · Hindi\n"
        "🟢 Class 12: Physics · Chemistry · Maths · Biology · CS\n\n"
        "💡 Attempt under real exam conditions — 3 hours!\n\n"
        f"🔗 {PORTAL_URL}\n\n"
        "#MockTest #CBSE #Class10 #Class12 #PracticePaper #BoardExams2027 #CBSEMock"
    )
    ig_post(caption, poster_url("promo_mock"), dry_run)
    print("[OK] IG Promo Mock")


def post_promo_lab(dry_run=False):
    caption = (
        "🧪 Practice Science Without a Lab!\n\n"
        "200+ interactive experiments on your screen 🖥️\n\n"
        "🌟 Physics · Chemistry · Biology · Maths\n"
        "🌟 Step-by-step simulation\n"
        "🌟 Real-time results\n"
        "🌟 Mapped to CBSE board exam questions\n\n"
        "🎯 Perfect for:\n"
        "• Home study without equipment\n"
        "• Last-minute practical revision\n"
        "• Visual learners\n\n"
        "🚀 No equipment. No mess. Pure learning!\n\n"
        f"🔗 {PORTAL_URL}/virtual-labs/\n\n"
        "#VirtualLab #CBSE #Science #Physics #Chemistry #Biology #BoardExams2027 #CBSEMock"
    )
    ig_post(caption, poster_url("promo_lab"), dry_run)
    print("[OK] IG Promo Lab")


def post_promo_notes(dry_run=False):
    caption = (
        "📖 Chapter-wise Study Notes — All CBSE Subjects!\n\n"
        "Everything you need to revise for boards in one place 🎯\n\n"
        "✏️ Chapter-wise breakdown\n"
        "✏️ Key definitions & formulas\n"
        "✏️ Previous year question patterns\n"
        "✏️ Quick-revision bullet points\n\n"
        "🗂️ Navigate from our Menu:\n"
        "🔹 Study Zone — Class 11 & 12\n"
        "🔹 Resources — All subjects\n"
        "🔹 Quick Revision — Formula sheets\n\n"
        "📚 Class 9, 10, 11 & 12 | All subjects\n\n"
        f"🔗 {PORTAL_URL}\n\n"
        "#StudyNotes #CBSE #Revision #BoardExams2027 #Class12 #Class10 #CBSEMock"
    )
    ig_post(caption, poster_url("promo_notes"), dry_run)
    print("[OK] IG Promo Notes")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="CBSE Mock Instagram auto-poster")
    parser.add_argument("--mode", default="morning",
        choices=["notes","practice_10","practice_12","lab","morning",
                 "promo_quest","promo_mock","promo_lab","promo_notes","all"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    sys.path.insert(0, str(REPO_ROOT))
    from social_content_tracker import ContentTracker
    tracker = ContentTracker()

    print(f"Instagram Auto-Poster — mode={args.mode} dry_run={args.dry_run}")
    print(f"IG Account ID: {IG_ACCOUNT_ID}")

    modes = {
        "morning": ["notes", "practice_10", "practice_12"],
        "all":     ["notes", "practice_10", "practice_12", "lab",
                    "promo_quest", "promo_mock", "promo_lab", "promo_notes"],
    }
    run_modes = modes.get(args.mode, [args.mode])

    for i, m in enumerate(run_modes):
        if i > 0 and not args.dry_run:
            print("[INFO] Waiting 10s before next post...")
            time.sleep(10)
        print(f"\n── {m} ──")
        if m == "notes":
            post_notes(tracker, dry_run=args.dry_run)
        elif m == "practice_10":
            post_practice(tracker, "practice_10", dry_run=args.dry_run)
        elif m == "practice_12":
            post_practice(tracker, "practice_12", dry_run=args.dry_run)
        elif m == "lab":
            post_lab(tracker, dry_run=args.dry_run)
        elif m == "promo_quest":
            post_promo_quest(dry_run=args.dry_run)
        elif m == "promo_mock":
            post_promo_mock(dry_run=args.dry_run)
        elif m == "promo_lab":
            post_promo_lab(dry_run=args.dry_run)
        elif m == "promo_notes":
            post_promo_notes(dry_run=args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()
