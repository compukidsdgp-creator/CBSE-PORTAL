"""Announce newly published chapter notes on Telegram, Facebook and Instagram — once per chapter.

Two steps, so Instagram can fetch the poster from GitHub after it is pushed:
    python3 announce_notes.py --render        make notes/posters/<id>.jpg for live chapters not yet announced
    python3 announce_notes.py --post [--dry-run]   post them, then mark them announced in notes_content/progress.json
Facebook: poster + caption, chapter link as the first comment. Instagram: caption says "link in bio".
Telegram: poster with the link in the caption (the public channel, TELEGRAM_CHAT_ID).
"""
import argparse
import json
import os
import textwrap
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from notes_pages import load_chapters

ROOT = Path(__file__).resolve().parent
PROGRESS = ROOT / "notes_content" / "progress.json"
POSTERS = ROOT / "notes" / "posters"
SITE = "https://cbsemock.org.in"
FONT = ROOT / "assets" / "fonts"
GH_RAW = f"https://raw.githubusercontent.com/{os.environ.get('GITHUB_REPOSITORY', 'compukidsdgp-creator/CBSE-PORTAL')}/main"


def font(name, size):
    try:
        return ImageFont.truetype(str(FONT / name), size)
    except Exception:
        return ImageFont.load_default()


def progress():
    try:
        return json.loads(PROGRESS.read_text(encoding="utf-8"))
    except Exception:
        return {}


CHANNELS = ("tg", "fb", "ig")


def missing_channels(entry):
    """Channels still to post. Older entries (no per-channel record) count as fully announced.
    A channel is retried on later runs up to 3 times."""
    if entry.get("announced") and "channels" not in entry:
        return []
    done = entry.get("channels", {})
    tries = entry.get("tries", 0)
    if tries >= 3:
        return []
    return [c for c in CHANNELS if not done.get(c)]


def pending():
    pr = progress()
    return [c for c in load_chapters() if c.get("status") == "live" and missing_channels(pr.get(c["_id"], {}))]


def poster_path(ch):
    return POSTERS / (ch["_id"].replace("/", "-") + ".jpg")


def chapter_url(ch):
    return f"{SITE}/notes/class-{ch['class']}/{ch['subject_slug']}/{ch['slug']}.html"


def render(ch):
    W, H = 1080, 1350
    im = Image.new("RGB", (W, H), "#0f2347")
    d = ImageDraw.Draw(im)
    for y in range(H):                                       # navy gradient
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(31 - 16 * t), int(74 - 39 * t), int(138 - 67 * t)))
    d.ellipse((760, -260, 1340, 320), outline=(201, 162, 39), width=3)
    d.ellipse((840, -180, 1260, 240), outline=(120, 140, 190), width=2)
    gold, cream, white = (232, 204, 106), (255, 228, 160), (255, 255, 255)
    d.rounded_rectangle((70, 80, 520, 146), 33, fill=(201, 162, 39))
    d.text((295, 113), f"NEW · CLASS {ch['class']} {ch['subject'].upper()}", font=font("Inter-Bold.otf", 30), fill=(15, 35, 71), anchor="mm")
    d.text((72, 210), "FULL CHAPTER NOTES", font=font("Inter-Bold.otf", 44), fill=gold)
    d.text((72, 268), f"Chapter {ch['number']}", font=font("Inter-Regular.otf", 40), fill=(205, 216, 238))
    y = 340
    for line in textwrap.wrap(ch["title"], 18)[:3]:
        d.text((70, y), line, font=font("Poppins-Bold.ttf", 92), fill=white)
        y += 108
    # 3D-ish open book
    bx, by = 650, 560
    d.polygon([(bx, by + 40), (bx + 180, by), (bx + 180, by + 230), (bx, by + 270)], fill=(255, 248, 225), outline=(201, 162, 39))
    d.polygon([(bx + 180, by), (bx + 360, by + 40), (bx + 360, by + 270), (bx + 180, by + 230)], fill=(255, 236, 180), outline=(201, 162, 39))
    for k in range(5):
        d.line([(bx + 25, by + 80 + k * 32), (bx + 160, by + 50 + k * 32)], fill=(201, 162, 39), width=4)
        d.line([(bx + 200, by + 50 + k * 32), (bx + 335, by + 80 + k * 32)], fill=(201, 162, 39), width=4)
    feats = ["Concepts step by step", f"{len(ch.get('diagrams', []))} labelled diagrams",
             f"{len(ch.get('worked', []))} worked board questions", "Common mistakes + quick revision"]
    fy = max(y + 40, 790)
    for f in feats:
        d.ellipse((72, fy + 10, 104, fy + 42), fill=(201, 162, 39))
        d.line([(80, fy + 26), (86, fy + 33), (97, fy + 18)], fill=(15, 35, 71), width=5)
        d.text((122, fy + 26), f, font=font("Inter-Bold.otf", 36), fill=white, anchor="lm")
        fy += 70
    d.rounded_rectangle((70, 1130, W - 70, 1240), 55, fill=(201, 162, 39))
    d.text((W // 2, 1185), "FREE · TAP THE LINK TO READ  →", font=font("Inter-Bold.otf", 40), fill=(15, 35, 71), anchor="mm")
    d.text((W // 2, 1290), "cbsemock.org.in", font=font("Inter-Bold.otf", 34), fill=cream, anchor="mm")
    POSTERS.mkdir(parents=True, exist_ok=True)
    im.save(poster_path(ch), quality=90, optimize=True)
    return poster_path(ch)


def captions(ch):
    url, n = chapter_url(ch), ch["number"]
    head = f"📘 NEW: Full chapter notes — Class {ch['class']} {ch['subject']}, Chapter {n}: {ch['title']}"
    body = (f"✅ Concepts explained step by step\n✅ {len(ch.get('diagrams', []))} labelled diagrams to learn\n"
            f"✅ {len(ch.get('worked', []))} worked board questions with model answers\n✅ Common mistakes + quick revision\n")
    tags = f"#CBSE #Class{ch['class']} #{ch['subject'].replace(' ', '')} #BoardExam2027 #CBSEMock"
    tg = f"{head}\n\n{body}\n👉 Read free: {url}\n\n{tags}"
    fb = f"{head}\n\n{body}\n👉 Read free: {url}\n\n{tags}"     # announcements carry the link itself
    ig = f"{head}\n\n{body}\n🔗 Link in bio (cbsemock.org.in/go)\n\n{tags}"
    return tg, fb, ig


def post(ch, dry, want=CHANNELS):
    import post_formula_image as P
    import social_links as SL
    from tg_photo import send_photo
    img_url = f"{GH_RAW}/{poster_path(ch).relative_to(ROOT).as_posix()}"
    tg, fb, ig = captions(ch)
    res = {}
    if "tg" in want:
        res["tg"] = True if dry else send_photo(poster_path(ch), tg)
        if dry:
            print("[TG dry-run]", tg[:120])
    if "fb" in want:
        fb_id = P.post_to_facebook(img_url, fb, dry_run=dry)
        res["fb"] = bool(fb_id)
        if fb_id:
            SL.post_fb_comment(fb_id, f"📘 Read the full chapter notes free: {chapter_url(ch)}", P.FB_TOKEN, dry_run=dry)
    if "ig" in want:
        res["ig"] = bool(P.post_to_instagram(img_url, ig, dry_run=dry))
    return res


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--render", action="store_true")
    a.add_argument("--post", action="store_true")
    a.add_argument("--dry-run", action="store_true")
    a = a.parse_args()
    todo = pending()
    if not todo:
        print("[announce] nothing new to announce"); return
    if a.render:
        for ch in todo:
            print("[announce] poster", render(ch).relative_to(ROOT))
    if a.post:
        pr = progress()
        for ch in todo:
            if not poster_path(ch).exists():
                render(ch)
            e = pr.setdefault(ch["_id"], {})
            want = missing_channels(e)
            res = post(ch, a.dry_run, want)
            if not a.dry_run:
                e.setdefault("channels", {}).update({k: True for k, v in res.items() if v})
                e["tries"] = e.get("tries", 0) + (0 if all(res.values()) else 1)
                e["announced"] = any(e["channels"].values())
                print(f"[announce] {ch['_id']}: {res}")
        if not a.dry_run:
            PROGRESS.write_text(json.dumps(pr, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
