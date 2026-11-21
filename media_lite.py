#!/usr/bin/env python3
"""
media_lite.py — after a reel or image has been POSTED and its Google Drive backup is VERIFIED, replace the file in the
repository with a light copy (480 px wide video, ~0.6 MB; JPEG ≤1080 px). Same path and name, so every page, player
and workflow keeps working, and nothing is re-rendered. The full-quality original stays in Drive.

Safety: a file is only replaced when archive/backup_manifest.csv has it with the SAME MD5 as the file in the repo
(i.e. exactly this file was backed up and checked). Replaced files are listed in archive/lite.csv.

    python3 media_lite.py run [--dry-run]     replace every eligible posted file
    python3 media_lite.py restore <path>...   bring full-quality originals back from Drive (needs RCLONE_DRIVE_TOKEN)
    python3 media_lite.py status
"""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
IST = timezone(timedelta(hours=5, minutes=30))
LITE = ROOT / "archive" / "lite.csv"
FIELDS = ["repo_path", "drive_path", "original_md5", "original_bytes", "lite_bytes", "at"]


def lite_rows():
    if not LITE.exists():
        return {}
    with open(LITE, encoding="utf-8") as f:
        return {r["repo_path"]: r for r in csv.DictReader(f)}


def save(rows):
    LITE.parent.mkdir(parents=True, exist_ok=True)
    with open(LITE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for k in sorted(rows):
            w.writerow(rows[k])


def posted_files():
    """Repository paths of media that has already been posted (the only files that may be made light)."""
    out = []
    for d, pat in (("formula-posts/videos/posted", "*.mp4"), ("formula-posts/why/posted", "*.mp4"),
                   ("formula-posts/why/hindi/posted", "*.mp4"), ("formula-posts/posted", "*.jpg"),
                   ("formula-posts/posted", "*.png")):
        out += [str(p.relative_to(ROOT)) for p in sorted((ROOT / d).glob(pat))]
    try:
        import trig_series as T
        st = T.state()
        out += [str(T.video(p).relative_to(ROOT)) for p in T.PARTS if str(p["part"]) in st and T.video(p).exists()]
    except Exception as e:
        print("[lite] trig series:", e)
    try:
        import generate_mistake_reel as GM
        posted = json.loads((ROOT / "mistake_reels/posted.json").read_text(encoding="utf-8"))
        for r in GM.load_specs():
            for lang in r["lang"]:
                if f"{r['number']:03d}-{r['id']}/{lang}" in posted:
                    out.append(str(GM.video_path(r, lang).relative_to(ROOT)))
    except Exception as e:
        print("[lite] mistake bank:", e)
    try:
        import generate_hack_reel as GH
        posted = json.loads((GH.BASE / "posted.json").read_text(encoding="utf-8"))
        for r in GH.load_specs():
            for lang in GH.langs(r):
                key = f"{r['n']:02d}-{r['id']}" + ("" if lang == "en" else f"/{lang}")
                if key in posted or (lang == "en" and r["id"] in posted):
                    out.append(str(GH.video_path(r, lang).relative_to(ROOT)))
    except Exception as e:
        print("[lite] campaign:", e)
    return [p for p in dict.fromkeys(out) if (ROOT / p).is_file()]


def make_lite(src, dst):
    if src.suffix.lower() == ".mp4":
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", "scale='min(480,iw)':-2", "-c:v", "libx264",
               "-preset", "veryfast", "-crf", "28", "-profile:v", "main", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", str(dst)]
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", "scale='min(1080,iw)':-2", "-q:v", "4", str(dst)]
    subprocess.run(cmd, check=True)


def run(dry=False):
    import media_backup as MB
    man, done = MB.manifest(), lite_rows()
    rows, saved, skipped = dict(done), 0, []
    for rel in posted_files():
        if rel in done:
            continue
        p = ROOT / rel
        m = man.get(rel)
        if not m or m["md5"] != MB.md5(p):
            skipped.append(rel); continue          # not (yet) backed up exactly as it is now
        tmp = Path(tempfile.mkdtemp()) / p.name
        try:
            make_lite(p, tmp)
        except subprocess.CalledProcessError as e:
            print(f"[lite] ffmpeg failed for {rel}: {e}"); continue
        before, after = p.stat().st_size, tmp.stat().st_size
        if after >= before * 0.8:                   # not worth it (already small)
            rows[rel] = {"repo_path": rel, "drive_path": m["drive_path"], "original_md5": m["md5"],
                         "original_bytes": before, "lite_bytes": before, "at": "kept (already small)"}
            continue
        print(f"[lite] {rel}: {before / 1e6:.1f} MB → {after / 1e6:.2f} MB")
        if not dry:
            shutil.move(str(tmp), str(p))
            rows[rel] = {"repo_path": rel, "drive_path": m["drive_path"], "original_md5": m["md5"],
                         "original_bytes": before, "lite_bytes": after, "at": datetime.now(IST).isoformat(timespec="seconds")}
        saved += before - after
    if not dry:
        save(rows)
    print(f"[lite] saved {saved / 1e6:.0f} MB · {len(skipped)} posted file(s) waiting for a verified backup")
    return saved


def restore(paths):
    """Download full-quality originals from Drive over their light copies."""
    import media_backup as MB
    rows = lite_rows()
    if not shutil.which("rclone"):
        subprocess.run("curl -fsSL https://rclone.org/install.sh | sudo bash", shell=True, check=False)
    conf = MB.rclone_conf()
    n = 0
    for rel in paths:
        rel = str(Path(rel).relative_to(ROOT)) if Path(rel).is_absolute() else rel
        r = rows.get(rel)
        if not r or r["lite_bytes"] == r["original_bytes"]:
            continue
        res = subprocess.run(["rclone", "--config", str(conf), "copyto", f"{MB.REMOTE}/{r['drive_path']}", str(ROOT / rel)])
        if res.returncode == 0 and MB.md5(ROOT / rel) == r["original_md5"]:
            rows.pop(rel); n += 1
        else:
            print(f"[lite] could not restore {rel} from Drive")
    save(rows)
    print(f"[lite] restored {n} original(s)")
    return n


def status():
    rows = lite_rows()
    real = [r for r in rows.values() if r["lite_bytes"] != r["original_bytes"]]
    saved = sum(int(r["original_bytes"]) - int(r["lite_bytes"]) for r in real)
    print(f"{len(real)} light copies in the repository · {saved / 1e6:.0f} MB saved · originals in Google Drive")


if __name__ == "__main__":
    a = sys.argv[1:] or ["status"]
    if a[0] == "run":
        run("--dry-run" in a)
    elif a[0] == "restore":
        restore(a[1:])
    else:
        status()
