#!/usr/bin/env python3
"""
media_backup.py — copy every reel, image and caption to the owner's Google Drive ("CBSEMock Reels"), sorted into
series / language / class-subject folders ready for uploading to YouTube, and verify every file by MD5.

Each video gets a caption file next to it (same name, .txt) with a title and a description to paste into YouTube.
Runs on GitHub Actions with rclone; the Drive login is the RCLONE_DRIVE_TOKEN secret (scope drive.file: rclone only
sees the files it creates). Nothing is deleted from the repository here — removing posted media happens later and
only for files listed as verified in archive/backup_manifest.csv.

    python3 media_backup.py plan         print where every file would go (no upload; works without the token)
    python3 media_backup.py current      back up every media file now in the repository (queued + posted)
    python3 media_backup.py history      also recover media deleted from the repository but still in git history
    python3 media_backup.py status       counts from the manifest

Drive layout:
    CBSEMock Reels/
      1 WHY Series - English/<Class 10 Maths | Class 12 Science | AI | CS …>/
      2 WHY Series - Hindi/<same>/
      3 Formula Reels/<Class 12 Physics …>/
      4 Mistake Bank - English/<Class 10 Chemistry …>/      5 Mistake Bank - Hindi/<…>/
      6 Board Plan Campaign - English/<pillar>/             7 Board Plan Campaign - Hindi/<pillar>/
      8 Images/<Formula images/<subject> | Social images | Promo posters>/
      9 From history/<old folder>/      (reels recovered from git history)
"""
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
IST = timezone(timedelta(hours=5, minutes=30))
REMOTE = "gdrive:CBSEMock Reels"
MANIFEST = ROOT / "archive" / "backup_manifest.csv"
MEDIA = {".mp4", ".jpg", ".jpeg", ".png", ".webp"}
SAFE = lambda s: re.sub(r'[\\/:*?"<>|]+', "-", s).strip() or "Other"


def group(cls, cat):
    cat = {"Maths": "Maths", "CS": "CS", "AI": "AI"}.get(cat, cat)
    return SAFE(f"Class {cls} {cat}" if cls else cat)


# ── What goes where ──────────────────────────────────────────────────────────
def items():
    """[(repo_path, drive_path, caption_text|None)] for every media file in the repository."""
    out, seen = [], set()
    def add(path, drive, cap=None):
        p = Path(path)
        rel = str(p.relative_to(ROOT)) if p.is_absolute() else str(p)
        if rel in seen or not (ROOT / rel).is_file():
            return
        seen.add(rel)
        out.append((rel, drive, cap))

    import reels_page as R
    # WHY? English (queue + posted + backup + trig series) and Hindi
    why_cat = {}
    for w in R.why_items():
        mod = w["id"].split("-", 1)[1]
        why_cat[mod] = group(w["cls"], w["cat"])
    def why_mod_cap(mod):
        try:
            import importlib
            m = importlib.import_module(f"why_reels.{mod}")
            return m
        except Exception:
            return None
    def why_group(mod, m):
        if mod in why_cat:
            return why_cat[mod]
        tags = getattr(m, "TAGS", "") if m else ""
        c = re.search(r"Class (\d+)", tags)
        subj = tags.split()[-1] if tags else "Other"
        return group(c.group(1) if c else "", subj)
    for d in ("queue", "posted", "backup", "series"):
        for f in sorted((ROOT / "formula-posts/why" / d).glob("*.mp4")):
            mod = f.stem.split("why_", 1)[-1]
            m = why_mod_cap(mod)
            txt = f.with_suffix(".txt")
            desc = txt.read_text(encoding="utf-8").strip() if txt.exists() else (m.CAPTION.strip() if m and hasattr(m, "CAPTION") else "")
            title = re.sub(r"\$|\\\\|\\mathrm|[{}]", "", getattr(m, "TITLE", f.stem)) if m else f.stem
            folder = "1 WHY Series - English/" + ("Trig Series (Parts 2-4)" if d == "series" else why_group(mod, m))
            add(f, f"{folder}/{f.name}", f"TITLE: {title}\n\nDESCRIPTION:\n{desc}")
    for d in ("formula-posts/why/hindi", "formula-posts/why/hindi/posted"):
        for f in sorted((ROOT / d).glob("*_hi.mp4")):
            mod = f.stem[len("why_"):-len("_hi")]
            m = why_mod_cap(mod)
            hi = getattr(m, "HINDI", {}) if m else {}
            txt = f.with_suffix(".txt")
            desc = txt.read_text(encoding="utf-8").strip() if txt.exists() else hi.get("caption", "")
            add(f, f"2 WHY Series - Hindi/{why_group(mod, m)}/{f.name}", f"TITLE: {hi.get('title', f.stem)}\n\nDESCRIPTION:\n{desc}")
    # Formula reels
    import post_formula_reel as P
    for it in R.formula_items():
        f = ROOT / it["src"]
        add(f, f"3 Formula Reels/{group(it['cls'], it['cat'])}/{f.name}",
            f"TITLE: {it['title']} — Formula Flash\n\nDESCRIPTION:\n{P.build_reel_caption(it['title'])}")
    for f in sorted((ROOT / "formula-posts/videos").rglob("*.mp4")):
        add(f, f"3 Formula Reels/Other/{f.name}", f"TITLE: {P.topic_from_filename(f.stem)} — Formula Flash\n\nDESCRIPTION:\n"
            + P.build_reel_caption(P.topic_from_filename(f.stem)))
    # Mistake Bank
    try:
        import generate_mistake_reel as GM
        import mistake_bank as MB
        for r in GM.load_specs():
            badge = r.get("badge") or r["lang"].get("en", {}).get("badge", "")
            m = re.search(r"Class (\d+) · ([^·]+)", badge)
            grp = group(m.group(1), m.group(2).strip()) if m else "Other"
            for lang in r["lang"]:
                f = GM.video_path(r, lang)
                folder = "4 Mistake Bank - English" if lang == "en" else "5 Mistake Bank - Hindi"
                add(f, f"{folder}/{grp}/{f.name}", f"TITLE: Mistake Bank #{r['number']:02d} — {r['lang'][lang]['title']}\n\n"
                    f"DESCRIPTION:\n{MB.caption(r, lang)}")
    except Exception as e:
        print("[plan] mistake bank:", e)
    # Board Plan campaign
    try:
        import generate_hack_reel as GH
        import campaign_post as CP
        plan = {p["n"]: p for p in json.loads((GH.BASE / "plan.json").read_text(encoding="utf-8"))["reels"]}
        for r in GH.load_specs():
            pillar = SAFE(str(plan.get(r["n"], {}).get("pillar", "Other")).title())
            for lang in GH.langs(r):
                f = GH.video_path(r, lang)
                folder = "6 Board Plan Campaign - English" if lang == "en" else "7 Board Plan Campaign - Hindi"
                v = GH.view(r, lang)
                add(f, f"{folder}/{pillar}/{f.name}",
                    f"TITLE: {v.get('title') or plan.get(r['n'], {}).get('topic', f.stem)}\n\nDESCRIPTION:\n{CP.caption(r, 'facebook', lang)}")
    except Exception as e:
        print("[plan] campaign:", e)
    # Images
    for d in ("formula-posts/queue", "formula-posts/posted"):
        for f in sorted((ROOT / d).iterdir()) if (ROOT / d).exists() else []:
            if f.suffix.lower() in MEDIA:
                parts = f.stem.split("_")
                subj = parts[1] if len(parts) > 2 and not parts[1].isdigit() else "Other"
                add(f, f"8 Images/Formula images/{SAFE(subj)}/{f.name}")
    for d, name in (("social-images", "Social images"), ("promo-posters", "Promo posters"), ("campaign_reels/thumb", "Board Plan thumbnails")):
        for f in sorted((ROOT / d).rglob("*")) if (ROOT / d).exists() else []:
            if f.suffix.lower() in MEDIA:
                add(f, f"8 Images/{name}/{f.relative_to(ROOT / d)}")
    return out


def history_items(tmp):
    """Media deleted from the repository but still in git history: last version of each, written under tmp."""
    now = {r for r, _, _ in items()}
    log = subprocess.run(["git", "log", "--diff-filter=D", "--name-only", "--format=%H"], cwd=ROOT,
                         capture_output=True, text=True).stdout.splitlines()
    out, commit, seen = [], None, set()
    keep = ("formula-posts/", "mistake_reels/video", "campaign_reels/video", "social-images/", "promo-posters/")
    for line in log:
        if re.fullmatch(r"[0-9a-f]{40}", line):
            commit = line; continue
        f = line.strip()
        if not f or f in seen or f in now or Path(f).suffix.lower() != ".mp4" or not f.startswith(keep):
            continue
        seen.add(f)
        blob = subprocess.run(["git", "show", f"{commit}^:{f}"], cwd=ROOT, capture_output=True).stdout
        if not blob:
            continue
        dst = Path(tmp) / "hist" / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(blob)
        out.append((str(dst), f"9 From history/{SAFE(str(Path(f).parent).replace('/', ' - '))}/{Path(f).name}", None, f))
    return out


# ── Upload + verify ──────────────────────────────────────────────────────────
def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
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
    with open(MANIFEST, encoding="utf-8") as fh:
        return {r["repo_path"]: r for r in csv.DictReader(fh)}


def save_manifest(rows):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["repo_path", "drive_path", "bytes", "md5", "source", "backed_up_at"])
        w.writeheader()
        for k in sorted(rows):
            w.writerow(rows[k])


def upload(entries, conf, source):
    """entries: [(local_file, drive_path, caption|None, repo_key)]. Stage → rclone copy → verify by MD5."""
    done = manifest()
    todo = [e for e in entries if not (e[3] in done and done[e[3]]["drive_path"] == e[1] and done[e[3]]["md5"] == md5(e[0]))]
    print(f"[backup] {len(entries)} file(s) · {len(todo)} new or changed")
    if not todo:
        return {}, 0
    stage = Path(tempfile.mkdtemp(prefix="stage_"))
    want = {}
    for local, drive, cap, key in todo:
        dst = stage / drive
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(local, dst)
        except OSError:
            shutil.copy2(local, dst)
        want[drive] = (key, md5(local), Path(local).stat().st_size)
        if cap:
            t = dst.with_suffix(".txt")
            t.write_text(cap.strip() + "\n", encoding="utf-8")
            want[str(Path(drive).with_suffix(".txt"))] = (None, md5(t), t.stat().st_size)
    r = subprocess.run(["rclone", "--config", str(conf), "copy", str(stage), REMOTE, "--checksum",
                        "--transfers", "4", "--retries", "5", "--low-level-retries", "10", "--stats-one-line", "--stats", "60s"],
                       capture_output=True, text=True)
    print(r.stderr[-1500:])
    ls = subprocess.run(["rclone", "--config", str(conf), "lsjson", "-R", "--hash", "--files-only", REMOTE],
                        capture_output=True, text=True)
    remote = {e["Path"]: (e.get("Hashes") or {}).get("md5") for e in json.loads(ls.stdout or "[]")}
    rows, bad = {}, 0
    for drive, (key, h, size) in want.items():
        if remote.get(drive) == h:
            if key:
                rows[key] = {"repo_path": key, "drive_path": drive, "bytes": size, "md5": h, "source": source,
                             "backed_up_at": datetime.now(IST).isoformat(timespec="seconds")}
        else:
            bad += 1
            print(f"[backup] NOT VERIFIED: {drive}")
    shutil.rmtree(stage, ignore_errors=True)
    done.update(rows)
    save_manifest(done)
    return rows, bad


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
    if cmd == "plan":
        from collections import Counter
        it = items()
        for folder, n in sorted(Counter(str(Path(d).parent) for _, d, _ in it).items()):
            print(f"{n:4}  {folder}")
        print(f"{len(it)} files")
        sys.exit()
    conf = rclone_conf()
    ok, bad = upload([(str(ROOT / r), d, c, r) for r, d, c in items()], conf, "current")
    hist_ok, hist_bad = {}, 0
    if cmd == "history":
        with tempfile.TemporaryDirectory() as tmp:
            hist_ok, hist_bad = upload(history_items(tmp), conf, "history")
    m = manifest()
    gb = sum(int(r["bytes"]) for r in m.values()) / 1024 ** 3
    msg = (f"💾 CBSEMock Drive backup: {len(ok) + len(hist_ok)} new file(s) saved and verified"
           + (f" ({len(hist_ok)} recovered from history)" if cmd == "history" else "")
           + f". Total in Drive: {len(m)} files, {gb:.2f} GB — folder \"CBSEMock Reels\".")
    if bad or hist_bad:
        msg += f"\n⚠️ {bad + hist_bad} file(s) could not be verified — they stay in the repository; the next run retries."
    if ok or hist_ok or bad or hist_bad or cmd == "history":
        owner(msg)
    else:
        print(msg)
    sys.exit(1 if (bad or hist_bad) else 0)
