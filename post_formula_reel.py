#!/usr/bin/env python3
"""
post_formula_reel.py — CBSEMock Formula Flash Reel Auto-Publisher
──────────────────────────────────────────────────────────────────
Runs at 8 PM IST via GitHub Actions.
1. Picks a random topic NOT posted in the last 90 days
2. Generates the MP4 reel (vibrance v2 style, 1080×1920)
3. Uploads to Facebook Page + Instagram Reels via Graph API
4. Logs the result to formula-posts/reel_log.csv

Environment variables (GitHub Secrets):
  FB_PAGE_ID             — Facebook Page ID
  FB_PAGE_ACCESS_TOKEN   — Page Access Token
  INSTAGRAM_ACCOUNT_ID   — Instagram Business Account ID
  INSTAGRAM_ACCESS_TOKEN — Page Access Token (instagram_content_publish)
  GITHUB_REPOSITORY      — Set automatically by GitHub Actions
  GITHUB_REF_NAME        — Branch name (default: main)

Usage:
  python3 post_formula_reel.py               # Pick random topic & post
  python3 post_formula_reel.py --dry-run     # Preview without posting
  python3 post_formula_reel.py --topic em_induction  # Force a topic
  python3 post_formula_reel.py --status      # Show what has been posted
"""

import os
import sys
import csv
import json
import time
import random
import argparse
import tempfile
import subprocess
import shutil
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone, timedelta, date
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent
LOG_CSV   = REPO_ROOT / "formula-posts" / "reel_log.csv"
VIDEO_DIR = REPO_ROOT / "formula-posts" / "videos"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

# ── API config ────────────────────────────────────────────────────────────────
FB_API_BASE = "https://graph.facebook.com/v27.0"
PAGE_ID     = os.environ.get("FB_PAGE_ID", "1472735085918141")
FB_TOKEN    = os.environ.get("FB_PAGE_ACCESS_TOKEN", "")
IG_ACCT_ID  = os.environ.get("INSTAGRAM_ACCOUNT_ID", "17841480792360992")
IG_TOKEN    = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")

GH_REPO   = os.environ.get("GITHUB_REPOSITORY", "compukidsdgp-creator/CBSE-PORTAL")
GH_BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
GH_RAW    = f"https://raw.githubusercontent.com/{GH_REPO}/{GH_BRANCH}"
# jsdelivr CDN serves GitHub content with proper headers Instagram accepts for video
GH_CDN    = f"https://cdn.jsdelivr.net/gh/{GH_REPO}@{GH_BRANCH}"

IST = timezone(timedelta(hours=5, minutes=30))

def now_ist():
    return datetime.now(IST)

# ── Topic selection ────────────────────────────────────────────────────────────
def load_posted_topics(days: int = 90) -> set:
    """Return set of topic IDs posted in the last `days` days."""
    if not LOG_CSV.exists():
        return set()
    cutoff = now_ist().date() - timedelta(days=days)
    posted = set()
    with open(LOG_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                d = datetime.strptime(row["date_ist"], "%Y-%m-%d").date()
                if d >= cutoff:
                    posted.add(row["topic_id"])
            except (KeyError, ValueError):
                pass
    return posted

def pick_topic(force: str | None = None) -> tuple[str, dict]:
    """Return (topic_id, topic_data). Randomly picks from unposted topics."""
    from formula_topics_master import TOPICS

    if force:
        if force not in TOPICS:
            print(f"[ERROR] Unknown topic: {force}")
            print(f"Available: {', '.join(TOPICS.keys())}")
            sys.exit(1)
        return force, TOPICS[force]

    posted   = load_posted_topics(90)
    eligible = [t for t in TOPICS if t not in posted]

    if not eligible:
        # All topics posted recently — reset and use full list
        print("[INFO] All topics posted in last 90 days. Resetting pool.")
        eligible = list(TOPICS.keys())

    topic_id = random.choice(eligible)
    return topic_id, TOPICS[topic_id]

# ── Caption generator ─────────────────────────────────────────────────────────
SUBJECT_TAGS = {
    "Physics":     "#Physics #PhysicsFormulas",
    "Chemistry":   "#Chemistry #ChemFormulas",
    "Biology":     "#Biology #BioFormulas",
    "Mathematics": "#Maths #MathFormulas",
    "CS":          "#ComputerScience #CSFormulas",
}

def build_reel_caption(topic_id: str, data: dict, slot: str = "evening") -> str:
    subject  = data.get("subject", "CBSE")
    t1       = data.get("title_line1", "")
    t2       = data.get("title_line2", "")
    chapter  = data.get("chapter_tag", "CBSE Board")
    subj_tag = SUBJECT_TAGS.get(subject, f"#{subject}")
    extra    = data.get("hashtags", "")

    caption = f"""Evening Revision — Formula Flash!

{t1} {t2}
{chapter}

Watch all 5 key formulas with diagrams. Save this reel for quick revision before your board exam!

Full notes & practice tests (free) → cbsemock.org.in

{subj_tag} #FormulaFlash #CBSEMock #BoardRevision #BoardExam2027 #EveningStudy {extra}""".strip()

    return caption

# ── Reel generation ────────────────────────────────────────────────────────────
def generate_reel(topic_id: str, data: dict) -> Path:
    """Generate MP4 using generate_formula_reel_v2.py. Returns path."""
    script = REPO_ROOT / "generate_formula_reel_v2.py"
    out_path = VIDEO_DIR / f"{topic_id}_reel_v2.mp4"

    print(f"[INFO] Generating reel for '{topic_id}'…")
    result = subprocess.run(
        [sys.executable, str(script), "--topic", topic_id],
        capture_output=False,
        timeout=600,
    )
    if result.returncode != 0:
        print(f"[ERROR] Reel generation failed (exit {result.returncode})")
        sys.exit(1)

    if not out_path.exists():
        # Fallback: check for any v2 mp4 with this topic
        matches = list(VIDEO_DIR.glob(f"{topic_id}*.mp4"))
        if matches:
            out_path = matches[-1]
        else:
            print(f"[ERROR] Expected output not found: {out_path}")
            sys.exit(1)

    size_mb = out_path.stat().st_size / 1024 / 1024
    print(f"[INFO] Reel ready: {out_path.name}  ({size_mb:.1f} MB)")
    return out_path

# ── Upload helpers ─────────────────────────────────────────────────────────────
def _api_post(url: str, data: dict, dry_run: bool = False, label: str = "") -> dict:
    if dry_run:
        print(f"  [DRY-RUN] POST {url[:60]}")
        print(f"  Payload keys: {list(data.keys())}")
        return {"id": f"dry-run-{label}"}
    body = urllib.parse.urlencode(data).encode()
    req  = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"[API ERROR {e.code}] {err[:300]}")
        return {"error": err}

def _upload_video_fb(video_path: Path, caption: str, dry_run: bool) -> str | None:
    """
    Upload video to Facebook Page using chunked/resumable upload.
    Returns post ID or None on failure.
    """
    print(f"[FB] Uploading reel to Facebook Page {PAGE_ID}…")
    if not FB_TOKEN:
        print("[FB ERROR] FB_PAGE_ACCESS_TOKEN not set.")
        return None

    if dry_run:
        print(f"  [DRY-RUN] Would upload {video_path.name} ({video_path.stat().st_size/1e6:.1f} MB)")
        print(f"  Caption preview:\n{caption[:200]}…")
        return "dry-run-fb-reel"

    file_size = video_path.stat().st_size

    # Step 1 — Initialise upload session
    init_url  = f"{FB_API_BASE}/{PAGE_ID}/videos"
    init_data = {
        "upload_phase": "start",
        "file_size":    str(file_size),
        "access_token": FB_TOKEN,
    }
    init_resp = _api_post(init_url, init_data, label="fb-init")
    if "upload_session_id" not in init_resp:
        print(f"[FB ERROR] Init failed: {init_resp}")
        return None

    session_id  = init_resp["upload_session_id"]
    start_offset = int(init_resp.get("start_offset", 0))
    end_offset   = int(init_resp.get("end_offset",   file_size))
    print(f"[FB] Upload session {session_id} — transferring {file_size/1e6:.1f} MB…")

    # Step 2 — Transfer (single chunk; FB allows up to 1 GB in one chunk)
    transfer_url = f"{FB_API_BASE}/{PAGE_ID}/videos"
    with open(video_path, "rb") as fh:
        video_bytes = fh.read(end_offset - start_offset)

    boundary = "----CBSEMockBoundary"
    body_parts = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="upload_phase"\r\n\r\n'
        f"transfer\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="upload_session_id"\r\n\r\n'
        f"{session_id}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="start_offset"\r\n\r\n'
        f"{start_offset}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="access_token"\r\n\r\n'
        f"{FB_TOKEN}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="video_file_chunk"; filename="{video_path.name}"\r\n'
        f"Content-Type: video/mp4\r\n\r\n"
    ).encode() + video_bytes + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(transfer_url, data=body_parts, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            transfer_resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"[FB ERROR] Transfer: {e.code} {e.read().decode()[:300]}")
        return None

    # Step 3 — Finish
    finish_data = {
        "upload_phase":     "finish",
        "upload_session_id": session_id,
        "description":       caption,
        "access_token":      FB_TOKEN,
    }
    finish_resp = _api_post(init_url, finish_data, label="fb-finish")
    if "success" in finish_resp or "id" in finish_resp:
        vid_id = finish_resp.get("id", session_id)
        print(f"[FB OK] Video ID: {vid_id}")
        return vid_id
    else:
        print(f"[FB FAIL] Finish: {finish_resp}")
        return None

def _upload_reel_instagram(video_path: Path, caption: str, dry_run: bool) -> str | None:
    """
    Upload Reel to Instagram using the Reels publish flow.
    Returns media ID or None.
    """
    print(f"[IG] Uploading reel to Instagram account {IG_ACCT_ID}…")
    if not IG_TOKEN:
        print("[IG ERROR] INSTAGRAM_ACCESS_TOKEN not set.")
        return None

    if dry_run:
        print(f"  [DRY-RUN] Would upload {video_path.name} ({video_path.stat().st_size/1e6:.1f} MB)")
        return "dry-run-ig-reel"

    # Instagram Reels require a publicly accessible video URL.
    # We serve it via GitHub raw URL after the reel is committed to the repo.
    video_url = f"{GH_CDN}/formula-posts/videos/{video_path.name}"
    print(f"[IG] Using public URL: {video_url}")

    # Step 1 — Create container (Reels)
    container_url  = f"{FB_API_BASE}/{IG_ACCT_ID}/media"
    container_data = {
        "media_type":   "REELS",
        "video_url":    video_url,
        "caption":      caption,
        "share_to_feed": "true",
        "access_token": IG_TOKEN,
    }
    container = _api_post(container_url, container_data, label="ig-container")
    if "id" not in container:
        print(f"[IG FAIL] Container: {container}")
        return None

    container_id = container["id"]
    print(f"[IG] Container {container_id} — waiting for processing…")

    # Poll status (up to 90 s)
    for attempt in range(18):
        time.sleep(5)
        status_url = (
            f"{FB_API_BASE}/{container_id}"
            f"?fields=status_code,status&access_token={IG_TOKEN}"
        )
        try:
            with urllib.request.urlopen(status_url, timeout=15) as r:
                st = json.loads(r.read())
        except Exception:
            continue
        code = st.get("status_code", "")
        print(f"  status: {code}")
        if code == "FINISHED":
            break
        if code in ("ERROR", "EXPIRED"):
            print(f"[IG ERROR] Container failed: {st}")
            return None

    # Step 2 — Publish
    pub_url  = f"{FB_API_BASE}/{IG_ACCT_ID}/media_publish"
    pub_data = {"creation_id": container_id, "access_token": IG_TOKEN}
    pub = _api_post(pub_url, pub_data, label="ig-publish")
    if "id" in pub:
        print(f"[IG OK] Media ID: {pub['id']}")
        return pub["id"]
    else:
        print(f"[IG FAIL] Publish: {pub}")
        return None

# ── Logging ───────────────────────────────────────────────────────────────────
def log_reel(topic_id: str, subject: str, fb_id: str | None,
             ig_id: str | None, dry_run: bool):
    write_header = not LOG_CSV.exists()
    with open(LOG_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["date_ist", "time_ist", "topic_id", "subject",
                        "fb_video_id", "ig_media_id", "dry_run"])
        w.writerow([
            now_ist().strftime("%Y-%m-%d"),
            now_ist().strftime("%H:%M"),
            topic_id, subject,
            fb_id or "FAILED",
            ig_id or "FAILED",
            str(dry_run),
        ])

def show_status():
    from formula_topics_master import TOPICS
    posted = load_posted_topics(90)
    remaining = [t for t in TOPICS if t not in posted]
    print(f"\n── Reel log: {LOG_CSV} ──")
    if LOG_CSV.exists():
        with open(LOG_CSV, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        for r in rows[-10:]:
            print(f"  {r.get('date_ist','')} {r.get('topic_id','')} "
                  f"[{r.get('subject','')}] FB:{r.get('fb_video_id','')} IG:{r.get('ig_media_id','')}")
    print(f"\n── Topics remaining (not posted in 90 days): {len(remaining)}/{len(TOPICS)} ──")
    for t in remaining[:20]:
        print(f"  {t}")
    if len(remaining) > 20:
        print(f"  … and {len(remaining)-20} more")
    print()

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate & post Formula Flash reel")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--topic",   default=None, help="Force a specific topic ID")
    parser.add_argument("--status",  action="store_true")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    print(f"\n[INFO] Formula Reel poster — dry_run={args.dry_run}")
    print(f"[INFO] Time: {now_ist().strftime('%Y-%m-%d %H:%M IST')}")

    topic_id, data = pick_topic(args.topic)
    print(f"[INFO] Topic: {topic_id}  ({data['subject']} — {data['title_line1']} {data['title_line2']})")

    caption  = build_reel_caption(topic_id, data, slot="evening")
    print(f"\n── Caption preview ──\n{caption[:300]}\n────────────────────\n")

    # Generate reel (skipped on dry-run to save time)
    if args.dry_run:
        reel_path = VIDEO_DIR / f"{topic_id}_reel_v2.mp4"
        # Use existing file if available, else create a placeholder
        if not reel_path.exists():
            existing = list(VIDEO_DIR.glob("*.mp4"))
            reel_path = existing[0] if existing else reel_path
        print(f"[DRY-RUN] Would generate reel → {reel_path.name}")
    else:
        reel_path = generate_reel(topic_id, data)

    # Post to both platforms
    fb_id = _upload_video_fb(reel_path, caption, dry_run=args.dry_run)
    ig_id = _upload_reel_instagram(reel_path, caption, dry_run=args.dry_run)

    # Log
    log_reel(topic_id, data.get("subject", ""), fb_id, ig_id, args.dry_run)

    ok = bool(fb_id and ig_id)
    print(f"\n{'OK' if ok else 'PARTIAL/FAIL'}  FB: {fb_id or 'FAILED'}  |  IG: {ig_id or 'FAILED'}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
