#!/usr/bin/env python3
"""
post_formula_image.py — CBSEMock Formula Flash Image Auto-Poster
─────────────────────────────────────────────────────────────────
Posts one Formula Flash image to Facebook Page + Instagram Business
account simultaneously, twice daily (8 AM IST / 8 PM IST).

Queue folder : formula-posts/queue/
Posted folder: formula-posts/posted/
Log CSV      : formula-posts/post_log.csv

Image naming convention (determines auto-caption):
  {subject}_{topic}_{class}.jpg   e.g. biology_photosynthesis_class10.jpg
  {subject}_{topic}.jpg           e.g. physics_em_induction.jpg

The script picks the FIRST file (alphabetically) from the queue,
posts it to both platforms, moves it to posted/, and logs the result.

Environment variables (GitHub Secrets):
  FB_PAGE_ID            — Facebook Page ID
  FB_PAGE_ACCESS_TOKEN  — Never-expiring Page Access Token
  INSTAGRAM_ACCOUNT_ID  — Instagram Business Account ID
  INSTAGRAM_ACCESS_TOKEN— Same Page Access Token (instagram_content_publish)
  GITHUB_REPOSITORY     — Set automatically by GitHub Actions (owner/repo)

Usage:
  python3 post_formula_image.py             # Post next image in queue
  python3 post_formula_image.py --dry-run   # Preview without posting
  python3 post_formula_image.py --status    # Show queue status
"""

import os
import sys
import csv
import json
import time
import shutil
import argparse
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
REPO_ROOT   = Path(__file__).parent
QUEUE_DIR   = REPO_ROOT / "formula-posts" / "queue"
POSTED_DIR  = REPO_ROOT / "formula-posts" / "posted"
LOG_CSV     = REPO_ROOT / "formula-posts" / "post_log.csv"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)
POSTED_DIR.mkdir(parents=True, exist_ok=True)

# ── API config ────────────────────────────────────────────────────────────────
FB_API_BASE = "https://graph.facebook.com/v27.0"
PAGE_ID     = os.environ.get("FB_PAGE_ID", "1472735085918141")
FB_TOKEN    = os.environ.get("FB_PAGE_ACCESS_TOKEN", "")
IG_ACCT_ID  = os.environ.get("INSTAGRAM_ACCOUNT_ID", "17841480792360992")
IG_TOKEN    = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")

# GitHub raw URL base — image must be publicly accessible for Instagram API
GH_REPO     = os.environ.get("GITHUB_REPOSITORY", "compukidsdgp-creator/CBSE-PORTAL")
GH_BRANCH   = os.environ.get("GITHUB_REF_NAME", "main")
GH_RAW_BASE = f"https://raw.githubusercontent.com/{GH_REPO}/{GH_BRANCH}"

# ── IST helper ────────────────────────────────────────────────────────────────
IST = timezone(timedelta(hours=5, minutes=30))

def now_ist() -> datetime:
    return datetime.now(IST)

def utc_now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

# ── Caption generator ─────────────────────────────────────────────────────────
SUBJECT_META = {
    "physics":      {"emoji": "⚡", "tag": "#Physics",      "pill": "Physics"},
    "chemistry":    {"emoji": "⚗️",  "tag": "#Chemistry",    "pill": "Chemistry"},
    "biology":      {"emoji": "🌿", "tag": "#Biology",      "pill": "Biology"},
    "maths":        {"emoji": "📐", "tag": "#Maths",        "pill": "Mathematics"},
    "mathematics":  {"emoji": "📐", "tag": "#Maths",        "pill": "Mathematics"},
    "cs":           {"emoji": "💻", "tag": "#ComputerScience","pill": "CS"},
    "computer":     {"emoji": "💻", "tag": "#ComputerScience","pill": "CS"},
    "english":      {"emoji": "📖", "tag": "#English",      "pill": "English"},
    "economics":    {"emoji": "📊", "tag": "#Economics",    "pill": "Economics"},
    "accountancy":  {"emoji": "🧾", "tag": "#Accountancy",  "pill": "Accounts"},
    "history":      {"emoji": "🏛️", "tag": "#History",      "pill": "History"},
    "geography":    {"emoji": "🌍", "tag": "#Geography",    "pill": "Geography"},
    "science":      {"emoji": "🔬", "tag": "#Science",      "pill": "Science"},
}

CLASS_HASHTAGS = {
    "class10": "#Class10 #CBSE10 #BoardExam2027",
    "class12": "#Class12 #CBSE12 #BoardExam2027",
    "class9":  "#Class9 #CBSE",
    "class11": "#Class11 #CBSE",
}

COMMON_TAGS = "#CBSEMock #FormulaFlash #CBSERevision #StudySmart #BoardPrep"

_NOISE_WORDS = {"formulaflash", "concept8", "neonyellow", "neon", "infographic",
                "poster", "guide", "study", "cbse", "card", "v2"}

def parse_filename(stem: str) -> dict:
    """
    Parse image filename stem into subject / topic / class.

    Works with any of:
      physics_em_induction_class12
      03_FormulaFlash_Chemistry_pH              (order prefix + style words are ignored)
      01b_Physics_Alternating_Current_class12
      Chemical Kinetics Class 12 Infographic    (spaces work too)
    The subject is the first recognised subject word anywhere in the name.
    """
    import re
    tokens = [t for t in re.split(r"[_\s\-]+", stem) if t]
    subject, class_part, topic_tokens = "", "", []
    k = 0
    while k < len(tokens):
        tok = tokens[k]; low = tok.lower()
        m = re.fullmatch(r"class(\d{1,2})", low)
        if m:
            class_part = f"class{m.group(1)}"
        elif low == "class" and k + 1 < len(tokens) and tokens[k + 1].isdigit():
            class_part = f"class{tokens[k + 1]}"; k += 1
        elif re.fullmatch(r"\d+[a-z]?", low) or low in _NOISE_WORDS:
            pass                                   # order prefix, part number, style word
        elif not subject and low in SUBJECT_META:
            subject = low
        else:
            topic_tokens.append(tok)
        k += 1

    words = []
    for tok in topic_tokens:
        w = tok.capitalize() if (tok.islower() and len(tok) > 3) else tok
        if not words or words[-1].lower() != w.lower():      # drop immediate repeats
            words.append(w)
    topic = " ".join(words) if words else "Formula Flash"
    return {"subject": subject or "cbse", "topic": topic, "class": class_part}

def build_caption(stem: str, slot: str = "morning") -> str:
    """Auto-generate a rich caption from the image filename."""
    info    = parse_filename(stem)
    subj    = info["subject"]
    topic   = info["topic"]
    cls     = info["class"]
    meta    = SUBJECT_META.get(subj, {"emoji": "📚", "tag": "#CBSE", "pill": "CBSE"})
    emoji   = meta["emoji"]
    subj_tag = meta["tag"]
    cls_tags = CLASS_HASHTAGS.get(cls, "#CBSE")
    subj_cap = meta["pill"]

    if slot == "morning":
        greeting = "Good morning! ☀️ Start your day with today's Formula Flash."
        cta = "Save this card & revise it tonight before bed! 🔖"
    else:
        greeting = "Evening revision time! 🌙 Lock in this formula before tomorrow."
        cta = "Screenshot & save — your tomorrow self will thank you! 💪"

    caption = f"""{emoji} Formula Flash — {subj_cap} | {topic}

{greeting}

🎯 Topic: {topic}
📚 Subject: {subj_cap}
{'🏫 ' + cls.replace('class','Class ') + ' · CBSE' if cls else '📋 CBSE Board'}

{cta}

🌐 Full revision portal → cbsemock.org.in
Practice tests, formula sheets, virtual labs — all free!

{subj_tag} {cls_tags} {COMMON_TAGS} #FormulaCard #{''.join(c for c in topic if c.isalnum())}"""

    return caption.strip()

# ── GitHub raw URL for image ───────────────────────────────────────────────────
def get_public_image_url(filename: str) -> str:
    """Return publicly accessible raw GitHub URL for the image."""
    return f"{GH_RAW_BASE}/formula-posts/queue/{urllib.parse.quote(filename)}"

# ── Facebook Graph API ────────────────────────────────────────────────────────
def _fb_api(endpoint: str, data: dict, dry_run: bool = False) -> dict:
    if dry_run:
        print(f"  [FB DRY-RUN] POST {endpoint}")
        print(f"  Payload: {json.dumps({k: v[:60]+'…' if isinstance(v,str) and len(v)>60 else v for k,v in data.items()}, indent=2)}")
        return {"id": "dry-run-fb"}

    url   = f"{FB_API_BASE}/{endpoint}"
    body  = urllib.parse.urlencode(data).encode()
    req   = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"[FB ERROR] {e.code}: {err}")
        return {"error": err}

def post_to_facebook(image_url: str, caption: str, dry_run: bool = False) -> str | None:
    """Post image+caption to Facebook Page. Returns post ID or None."""
    print(f"[FB] Posting image to Facebook Page {PAGE_ID}…")
    if not FB_TOKEN:
        print("[FB ERROR] FB_PAGE_ACCESS_TOKEN not set.")
        return None

    result = _fb_api(f"{PAGE_ID}/photos", {
        "url":          image_url,
        "caption":      caption,
        "access_token": FB_TOKEN,
    }, dry_run=dry_run)

    if "id" in result:
        post_id = result["id"]
        print(f"[FB OK] Post ID: {post_id}")
        return post_id
    else:
        print(f"[FB FAIL] {result}")
        return None

# ── Instagram Graph API ───────────────────────────────────────────────────────
def _ig_api(endpoint: str, data: dict, dry_run: bool = False) -> dict:
    if dry_run:
        print(f"  [IG DRY-RUN] POST {endpoint}")
        print(f"  Payload: {json.dumps({k: v[:60]+'…' if isinstance(v,str) and len(v)>60 else v for k,v in data.items()}, indent=2)}")
        return {"id": "dry-run-ig"}

    url  = f"{FB_API_BASE}/{endpoint}"
    body = urllib.parse.urlencode(data).encode()
    req  = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"[IG ERROR] {e.code}: {err}")
        return {"error": err}

def post_to_instagram(image_url: str, caption: str, dry_run: bool = False) -> str | None:
    """Post image+caption to Instagram Business. Returns media ID or None."""
    print(f"[IG] Creating media container on Instagram account {IG_ACCT_ID}…")
    if not IG_TOKEN:
        print("[IG ERROR] INSTAGRAM_ACCESS_TOKEN not set.")
        return None

    # Step 1: Create media container
    container = _ig_api(f"{IG_ACCT_ID}/media", {
        "image_url":    image_url,
        "caption":      caption,
        "access_token": IG_TOKEN,
    }, dry_run=dry_run)

    if "id" not in container:
        print(f"[IG FAIL] Container creation failed: {container}")
        return None

    container_id = container["id"]
    print(f"[IG] Container ID: {container_id}  — waiting 5s for processing…")
    if not dry_run:
        time.sleep(5)

    # Step 2: Publish container
    publish = _ig_api(f"{IG_ACCT_ID}/media_publish", {
        "creation_id":  container_id,
        "access_token": IG_TOKEN,
    }, dry_run=dry_run)

    if "id" in publish:
        media_id = publish["id"]
        print(f"[IG OK] Media ID: {media_id}")
        return media_id
    else:
        print(f"[IG FAIL] {publish}")
        return None

# ── Queue management ──────────────────────────────────────────────────────────
def get_next_image() -> Path | None:
    """Return the next image file from the queue (alphabetical order)."""
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    files = sorted(
        f for f in QUEUE_DIR.iterdir()
        if f.suffix.lower() in exts and not f.name.startswith(".")
    )
    return files[0] if files else None

def move_to_posted(img_path: Path) -> Path:
    dest = POSTED_DIR / img_path.name
    # Avoid collision — suffix with timestamp if already exists
    if dest.exists():
        ts   = now_ist().strftime("%Y%m%d_%H%M")
        dest = POSTED_DIR / f"{img_path.stem}_{ts}{img_path.suffix}"
    shutil.move(str(img_path), str(dest))
    return dest

def log_post(filename: str, slot: str, fb_id: str | None, ig_id: str | None,
             caption: str, dry_run: bool):
    """Append one row to the CSV log."""
    write_header = not LOG_CSV.exists()
    with open(LOG_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["timestamp_ist", "filename", "slot", "fb_post_id",
                        "ig_media_id", "dry_run", "caption_preview"])
        w.writerow([
            now_ist().strftime("%Y-%m-%d %H:%M IST"),
            filename,
            slot,
            fb_id or "FAILED",
            ig_id or "FAILED",
            str(dry_run),
            caption[:120].replace("\n", " "),
        ])

def show_status():
    """Print queue and log status."""
    exts   = {".jpg", ".jpeg", ".png", ".webp"}
    queued = sorted(f.name for f in QUEUE_DIR.iterdir()
                    if f.suffix.lower() in exts and not f.name.startswith("."))
    posted = sorted(f.name for f in POSTED_DIR.iterdir()
                    if f.suffix.lower() in exts and not f.name.startswith("."))

    print(f"\n── Queue ({len(queued)} images) ──")
    for i, fn in enumerate(queued, 1):
        print(f"  {i:3}. {fn}")
    if not queued:
        print("  (empty)")

    print(f"\n── Posted ({len(posted)} images) ──")
    for fn in posted[-5:]:
        print(f"  {fn}")
    if len(posted) > 5:
        print(f"  … and {len(posted)-5} more")

    # Days remaining at 2 posts/day
    days_left = len(queued) / 2
    print(f"\n── Coverage: ~{days_left:.0f} days at 2 posts/day "
          f"({len(queued)} images in queue) ──\n")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Post Formula Flash image to FB + Instagram")
    parser.add_argument("--dry-run",  action="store_true", help="Preview without posting")
    parser.add_argument("--slot",     default="auto",      help="morning | evening | auto")
    parser.add_argument("--status",   action="store_true", help="Show queue status and exit")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    # Determine slot from IST time if auto
    slot = args.slot
    if slot == "auto":
        hour = now_ist().hour
        slot = "morning" if hour < 14 else "evening"

    print(f"\n[INFO] Formula Flash poster — slot={slot}, dry_run={args.dry_run}")
    print(f"[INFO] Time: {now_ist().strftime('%Y-%m-%d %H:%M IST')} / {utc_now_str()}")

    img_path = get_next_image()
    if not img_path:
        print("[SKIP] No images in queue. Add images to formula-posts/queue/ and push.")
        sys.exit(0)

    print(f"[INFO] Next image: {img_path.name}")

    caption     = build_caption(img_path.stem, slot)
    image_url   = get_public_image_url(img_path.name)

    print(f"\n── Caption preview ──\n{caption}\n────────────────────")
    print(f"\n── Image URL ──\n{image_url}\n────────────────────\n")

    # Post to both platforms
    fb_id = post_to_facebook(image_url, caption, dry_run=args.dry_run)
    ig_id = post_to_instagram(image_url, caption, dry_run=args.dry_run)

    # Log result
    log_post(img_path.name, slot, fb_id, ig_id, caption, args.dry_run)

    # Move to posted/ (even on dry-run, so queue advances in test)
    if not args.dry_run:
        dest = move_to_posted(img_path)
        print(f"[INFO] Moved to posted/: {dest.name}")
    else:
        print(f"[DRY-RUN] Would move {img_path.name} → posted/")

    # Summary
    ok = bool(fb_id and ig_id)
    print(f"\n{'✅' if ok else '⚠️ '}  Done — FB: {fb_id or 'FAILED'}  |  IG: {ig_id or 'FAILED'}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
