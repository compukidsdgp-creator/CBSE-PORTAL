#!/usr/bin/env python3
"""
post_formula_reel.py — CBSEMock Formula Flash Reel Auto-Publisher
──────────────────────────────────────────────────────────────────
Runs at 8 PM IST via GitHub Actions.
1. Picks the FIRST .mp4 (alphabetically) from formula-posts/videos/queue/
2. Uploads to Facebook Page + Instagram Reels via Graph API
3. Moves the file to formula-posts/videos/posted/
4. When queue is empty, moves all posted/ files back to queue/ (full circle)
5. Logs the result to formula-posts/reel_log.csv

Queue folder : formula-posts/videos/queue/
Posted folder: formula-posts/videos/posted/

Environment variables (GitHub Secrets):
  FB_PAGE_ID             — Facebook Page ID
  FB_PAGE_ACCESS_TOKEN   — Page Access Token
  INSTAGRAM_ACCOUNT_ID   — Instagram Business Account ID
  INSTAGRAM_ACCESS_TOKEN — Page Access Token (instagram_content_publish)
  GITHUB_REPOSITORY      — Set automatically by GitHub Actions
  GITHUB_REF_NAME        — Branch name (default: main)

Usage:
  python3 post_formula_reel.py               # Post next reel in queue
  python3 post_formula_reel.py --dry-run     # Preview without posting
  python3 post_formula_reel.py --status      # Show queue status
"""

import os
import sys
import csv
import json
import time
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
REPO_ROOT  = Path(__file__).parent
LOG_CSV    = REPO_ROOT / "formula-posts" / "reel_log.csv"
VIDEO_DIR  = REPO_ROOT / "formula-posts" / "videos"
QUEUE_DIR  = VIDEO_DIR / "queue"
POSTED_DIR = VIDEO_DIR / "posted"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)
POSTED_DIR.mkdir(parents=True, exist_ok=True)

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

# ── Queue helpers ──────────────────────────────────────────────────────────────
def next_reel() -> Path:
    """
    Return the first .mp4 (alphabetically) from queue/.
    If queue is empty, move all posted/ files back to queue/ (full circle reset)
    and return the first one.
    """
    queued = sorted(f for f in QUEUE_DIR.iterdir() if f.suffix.lower() == ".mp4")
    if not queued:
        posted = sorted(f for f in POSTED_DIR.iterdir() if f.suffix.lower() == ".mp4")
        if not posted:
            print("[SKIP] No reels in queue or posted. Add .mp4 files to formula-posts/videos/queue/")
            sys.exit(0)
        print(f"[INFO] Queue empty — full circle complete! Resetting {len(posted)} reels back to queue.")
        for f in posted:
            shutil.move(str(f), str(QUEUE_DIR / f.name))
        queued = sorted(f for f in QUEUE_DIR.iterdir() if f.suffix.lower() == ".mp4")
    return queued[0]

def move_to_posted(reel_path: Path) -> Path:
    dest = POSTED_DIR / reel_path.name
    shutil.move(str(reel_path), str(dest))
    return dest

def topic_from_filename(stem: str) -> str:
    """Derive a readable topic label from the filename stem."""
    # e.g. em_induction_reel_v2 → em induction, boolean_algebra_reel_v2 → boolean algebra
    name = stem.replace("_reel_v2", "").replace("_reel", "").replace("_", " ")
    return name.title()

# ── Caption generator ─────────────────────────────────────────────────────────
SUBJECT_TAGS = {
    "Physics":     "#Physics #PhysicsFormulas",
    "Chemistry":   "#Chemistry #ChemFormulas",
    "Biology":     "#Biology #BioFormulas",
    "Mathematics": "#Maths #MathFormulas",
    "CS":          "#ComputerScience #CSFormulas",
}

def build_reel_caption(topic_label: str) -> str:
    caption = (
        f"🎯 Evening Revision — Formula Flash!\n\n"
        f"📌 {topic_label}\n\n"
        f"Watch key formulas with animated diagrams. Save this reel for quick revision before your board exam!\n\n"
        f"🌐 Free notes & practice tests → https://cbsemock.org.in\n"
        f"📲 Join Telegram: t.me/cbsemockportal\n"
        f"👍 Facebook: cbsemock.org.in\n"
        f"📸 Instagram: @cbsemock\n\n"
        f"#FormulaFlash #CBSEMock #BoardRevision #BoardExam2027 #EveningStudy #CBSE2027 #CBSERevision"
    )
    return caption


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

    # Step 3 — Finish (description shown under FB Reel; URL in text is tappable on FB)
    finish_data = {
        "upload_phase":        "finish",
        "upload_session_id":    session_id,
        "description":          caption,
        "content_category":     "SCIENCE",
        "embeddable":           "true",
        "access_token":         FB_TOKEN,
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

    # Instagram Reels: use resumable upload (direct binary) so no public URL needed.
    file_size = video_path.stat().st_size

    # Step 1 — Initialise upload session
    init_url  = f"{FB_API_BASE}/{IG_ACCT_ID}/media"
    init_data = {
        "media_type":    "REELS",
        "caption":       caption,
        "share_to_feed": "true",
        "upload_type":   "resumable",
        "access_token":  IG_TOKEN,
    }
    print(f"[IG] Initialising resumable upload ({file_size/1e6:.1f} MB)…")
    init_resp = _api_post(init_url, init_data, label="ig-init")
    if "id" not in init_resp or "uri" not in init_resp:
        # Fallback: try video_url with raw GitHub (last resort)
        print(f"[IG] Resumable init failed: {init_resp} — trying video_url fallback")
        video_url = f"{GH_RAW}/formula-posts/videos/queue/{video_path.name}"
        fallback_data = {
            "media_type":    "REELS",
            "video_url":     video_url,
            "caption":       caption,
            "share_to_feed": "true",
            "access_token":  IG_TOKEN,
        }
        init_resp = _api_post(init_url, fallback_data, label="ig-container-fallback")
        if "id" not in init_resp:
            print(f"[IG FAIL] Container: {init_resp}")
            return None
        container_id = init_resp["id"]
    else:
        container_id = init_resp["id"]
        upload_uri   = init_resp["uri"]

        # Step 2 — Upload video bytes
        print(f"[IG] Uploading bytes to {upload_uri[:60]}…")
        with open(video_path, "rb") as vf:
            video_bytes = vf.read()
        upload_req = urllib.request.Request(
            upload_uri,
            data=video_bytes,
            method="POST",
        )
        upload_req.add_header("Authorization", f"OAuth {IG_TOKEN}")
        upload_req.add_header("Content-Type", "video/mp4")
        upload_req.add_header("Content-Length", str(file_size))
        upload_req.add_header("offset", "0")
        upload_req.add_header("file_size", str(file_size))
        upload_result = None
        for attempt in range(3):
            try:
                # Re-build request each retry (Request objects are single-use)
                upload_req2 = urllib.request.Request(upload_uri, data=video_bytes, method="POST")
                upload_req2.add_header("Authorization", f"OAuth {IG_TOKEN}")
                upload_req2.add_header("Content-Type", "video/mp4")
                upload_req2.add_header("Content-Length", str(file_size))
                upload_req2.add_header("offset", "0")
                upload_req2.add_header("file_size", str(file_size))
                with urllib.request.urlopen(upload_req2, timeout=180) as r:
                    upload_result = json.loads(r.read())
                    print(f"[IG] Upload result: {upload_result}")
                break
            except urllib.error.HTTPError as e:
                err = e.read().decode()
                print(f"[IG] Upload attempt {attempt+1} failed: {e.code}: {err[:200]}")
                if attempt == 2:
                    print(f"[IG ERROR] Upload failed after 3 attempts")
                    return None
                time.sleep(5)
        if upload_result is None:
            return None

    print(f"[IG] Container {container_id} — waiting for processing…")

    # Poll status (up to 120 s)
    for attempt in range(24):
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

    # Step 3 — Publish
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
def log_reel(filename: str, fb_id: str | None, ig_id: str | None, dry_run: bool):
    write_header = not LOG_CSV.exists()
    with open(LOG_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["date_ist", "time_ist", "filename", "fb_video_id", "ig_media_id", "dry_run"])
        w.writerow([
            now_ist().strftime("%Y-%m-%d"),
            now_ist().strftime("%H:%M"),
            filename,
            fb_id or "FAILED",
            ig_id or "FAILED",
            str(dry_run),
        ])

def show_status():
    queued = sorted(f.name for f in QUEUE_DIR.iterdir() if f.suffix.lower() == ".mp4")
    posted = sorted(f.name for f in POSTED_DIR.iterdir() if f.suffix.lower() == ".mp4")
    total  = len(queued) + len(posted)
    print(f"\n── Reel Queue ({len(queued)} remaining of {total} total) ──")
    for i, fn in enumerate(queued, 1):
        marker = "▶ NEXT" if i == 1 else f"  {i}."
        print(f"  {marker}  {fn}")
    print(f"\n── Posted ({len(posted)}) ──")
    for fn in posted[-10:]:
        print(f"  {fn}")
    if not queued:
        print("\n  ⚠️  Queue empty — will reset to full circle on next run.")
    print()

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Post next Formula Flash reel from queue")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--status",  action="store_true")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    print(f"\n[INFO] Formula Reel poster — dry_run={args.dry_run}")
    print(f"[INFO] Time: {now_ist().strftime('%Y-%m-%d %H:%M IST')}")

    reel_path   = next_reel()
    topic_label = topic_from_filename(reel_path.stem)
    caption     = build_reel_caption(topic_label)

    queued_count = len(list(QUEUE_DIR.glob("*.mp4")))
    print(f"[INFO] Next reel: {reel_path.name}  ({queued_count} in queue)")
    print(f"\n── Caption preview ──\n{caption[:300]}\n────────────────────\n")

    # Post to both platforms
    fb_id = _upload_video_fb(reel_path, caption, dry_run=args.dry_run)
    ig_id = _upload_reel_instagram(reel_path, caption, dry_run=args.dry_run)

    # Move to posted/ (even on dry-run so queue advances in test)
    if not args.dry_run:
        dest = move_to_posted(reel_path)
        print(f"[INFO] Moved to posted/: {dest.name}")
    else:
        print(f"[DRY-RUN] Would move {reel_path.name} → posted/")

    # Log
    log_reel(reel_path.name, fb_id, ig_id, args.dry_run)

    ok = bool(fb_id and ig_id)
    print(f"\n{'✅  Done' if ok else '⚠️  PARTIAL/FAIL'}  FB: {fb_id or 'FAILED'}  |  IG: {ig_id or 'FAILED'}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
