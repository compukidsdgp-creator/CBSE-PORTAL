#!/usr/bin/env python3
"""
media_backup.py — copy every reel, image and caption to the owner's Google Drive ("CBSEMock Reels") and verify it.

Runs on GitHub Actions with rclone; the Drive login is the RCLONE_DRIVE_TOKEN secret (scope drive.file: rclone only
sees the files it creates). Nothing is deleted from the repository here — deleting posted media comes later and only
for files this backup has verified (see archive/backup_manifest.csv).

    python3 media_backup.py current      back up every media file now in the repository (queued + posted)
    python3 media_backup.py history      also recover media that was deleted from the repository but is in git history
    python3 media_backup.py status       counts from the manifest
"""
import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IST = timezone(timedelta(hours=5, minutes=30))
REMOTE = "gdrive:CBSEMock Reels"
MANIFEST = ROOT / "archive" / "backup_manifest.csv"
EXTS = {".mp4", ".jpg", ".jpeg", ".png", ".webp", ".txt"}
# repository folder → Drive folder
MAP = [
    ("formula-posts/videos/posted", "Formula reels/posted"),
    ("formula-posts/videos/queue", "Formula reels/queue"),
    ("formula-posts/posted", "Formula images/posted"),
    ("formula-posts/queue", "Formula images/queue"),
    ("formula-posts/why/posted", "WHY English/posted"),
    ("formula-posts/why/queue", "WHY English/queue"),
    ("formula-posts/why/backup", "WHY English/backup"),
    ("formula-posts/why/series", "WHY English/trig series"),
    ("formula-posts/why/hindi/posted", "WHY Hindi/posted"),
    ("formula-posts/why/hindi", "WHY Hindi/ready"),
    ("mistake_reels/video", "Mistake Bank"),
    ("campaign_reels/video", "Board Plan campaign"),
    ("campaign_reels/thumb", "Board Plan campaign/thumbnails"),
    ("social-images", "Social images"),
    ("promo-posters", "Promo posters"),
]


def drive_folder(rel):
    """Drive folder for a repository path (longest matching prefix), or None if it is not backed up."""
    parent = str(Path(rel).parent)
    for src, dst in MAP:
        if parent == src:
            return dst
    return None


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rclone_conf():
    tok = os.environ.get("RCLONE_DRIVE_TOKEN")
    if not tok:
        sys.exit("RCLONE_DRIVE_TOKEN secret is missing")
    conf = Path(tempfile.gettempdir()) / "rclone.conf"
    conf.write_text(f"[gdrive]\ntype = drive\nscope = drive.file\ntoken = {tok.strip()}\n", encoding="utf-8")
    return conf


def manifest():
    if not MANIFEST.exists():
        return {}
    with open(MANIFEST, encoding="utf-8") as f:
        return {r["repo_path"]: r for r in csv.DictReader(f)}


def save_manifest(rows):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["repo_path", "drive_path", "bytes", "md5", "source", "backed_up_at"])
        w.writeheader()
        for k in sorted(rows):
            w.writerow(rows[k])


def current_files():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True).stdout.decode().split("\0")
    return [f for f in out if f and Path(f).suffix.lower() in EXTS and drive_folder(f) and (ROOT / f).is_file()
            and not Path(f).name.lower().startswith("readme")]


def history_files(tmp):
    """Media that was in the repository once but is gone now: last version of each deleted path, written to tmp."""
    now = set(current_files())
    log = subprocess.run(["git", "log", "--diff-filter=D", "--name-only", "--format=%H"], cwd=ROOT,
                         capture_output=True, text=True).stdout.splitlines()
    out, commit = [], None
    seen = set()
    for line in log:
        if len(line) == 40 and all(c in "0123456789abcdef" for c in line):
            commit = line; continue
        f = line.strip()
        if not f or f in seen or f in now or Path(f).suffix.lower() not in EXTS or not drive_folder(f):
            continue
        seen.add(f)
        blob = subprocess.run(["git", "show", f"{commit}^:{f}"], cwd=ROOT, capture_output=True).stdout
        if not blob:
            continue
        dst = Path(tmp) / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(blob)
        out.append(f)
    return out


def upload(files, base, conf, source):
    """Copy files (repository-relative, read from base) to Drive and verify each by MD5. Returns verified rows."""
    rows, done = {}, manifest()
    todo = [f for f in files if not (f in done and done[f]["md5"] == md5(Path(base) / f))]
    print(f"[backup] {len(files)} file(s) · {len(todo)} new or changed")
    by_folder = {}
    for f in todo:
        by_folder.setdefault(drive_folder(f), []).append(f)
    for folder, fs in by_folder.items():
        lst = Path(tempfile.gettempdir()) / "files.txt"
        src_dir = Path(base) / str(Path(fs[0]).parent)
        lst.write_text("\n".join(Path(f).name for f in fs) + "\n", encoding="utf-8")
        dst = f"{REMOTE}/{folder}" + ("" if source == "current" else "")
        r = subprocess.run(["rclone", "--config", str(conf), "copy", str(src_dir), dst, "--files-from", str(lst),
                            "--transfers", "4", "--retries", "5", "--low-level-retries", "10"], capture_output=True, text=True)
        if r.returncode:
            print(f"[backup] copy to {folder} failed: {r.stderr[-400:]}")
        # verify: Drive's own MD5 for every file must match ours
        ls = subprocess.run(["rclone", "--config", str(conf), "lsjson", "--hash", "--files-only", dst],
                            capture_output=True, text=True)
        remote = {e["Name"]: e for e in json.loads(ls.stdout or "[]")}
        for f in fs:
            local = md5(Path(base) / f)
            e = remote.get(Path(f).name)
            if e and (e.get("Hashes") or {}).get("md5") == local:
                rows[f] = {"repo_path": f, "drive_path": f"{folder}/{Path(f).name}", "bytes": (Path(base) / f).stat().st_size,
                           "md5": local, "source": source, "backed_up_at": datetime.now(IST).isoformat(timespec="seconds")}
            else:
                print(f"[backup] NOT VERIFIED: {f}")
    done.update(rows)
    save_manifest(done)
    return rows, len(todo) - len(rows)


def owner(text):
    tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("SEO_REPORT_CHAT_ID")
    if tok and chat:
        urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage",
                               data=json.dumps({"chat_id": chat, "text": text}).encode(), headers={"Content-Type": "application/json"}), timeout=20)
    print(text)


def status():
    m = manifest()
    gb = sum(int(r["bytes"]) for r in m.values()) / 1024 ** 3
    print(f"{len(m)} files backed up ({gb:.2f} GB) · {sum(1 for r in m.values() if r['source'] == 'history')} recovered from history")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        status(); sys.exit()
    conf = rclone_conf()
    ok, bad = upload(current_files(), ROOT, conf, "current")
    hist_ok, hist_bad = {}, 0
    if cmd == "history":
        with tempfile.TemporaryDirectory() as tmp:
            hist_ok, hist_bad = upload(history_files(tmp), tmp, conf, "history")
    m = manifest()
    gb = sum(int(r["bytes"]) for r in m.values()) / 1024 ** 3
    msg = (f"💾 CBSEMock Drive backup: {len(ok) + len(hist_ok)} new file(s) saved and verified"
           + (f" ({len(hist_ok)} recovered from history)" if cmd == "history" else "")
           + f". Total in Drive: {len(m)} files, {gb:.2f} GB.")
    if bad or hist_bad:
        msg += f"\n⚠️ {bad + hist_bad} file(s) could not be verified — they stay in the repository; the next run retries."
    if ok or hist_ok or bad or hist_bad or cmd == "history":
        owner(msg)
    else:
        print(msg)
    sys.exit(1 if (bad or hist_bad) else 0)
