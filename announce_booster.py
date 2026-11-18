"""Announce live Weekly Knowledge Boosters on Telegram, Facebook and Instagram — once per booster.
    python3 announce_booster.py --render            booster/posters/<id>.jpg for live boosters not yet announced
    python3 announce_booster.py --post [--dry-run]  post them, then mark them in booster_content/progress.json
Telegram (public channel) and Facebook carry the link; Instagram says "link in bio".
"""
import argparse
import json
import os
import textwrap
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import booster_plan as BP
from booster_pages import approvals, is_live, rel_path, BP_texts

ROOT = Path(__file__).resolve().parent
PROGRESS = BP.SRC / "progress.json"
POSTERS = ROOT / "booster" / "posters"
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


def pending():
    pr, appr = progress(), approvals()
    return [b for b in BP.load_boosters() if is_live(b, appr) and not pr.get(b["_id"], {}).get("announced")]


def poster_path(b):
    return POSTERS / (b["_id"].replace("/", "-") + ".jpg")


def url(b):
    return f"{SITE}/{rel_path(b)}"


def render(b):
    W, H = 1080, 1350
    im = Image.new("RGB", (W, H), "#0f2347")
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(31 - 16 * t), int(74 - 39 * t), int(138 - 67 * t)))
    d.ellipse((760, -260, 1340, 320), outline=(201, 162, 39), width=3)
    d.ellipse((840, -180, 1260, 240), outline=(120, 140, 190), width=2)
    gold, white, navy = (232, 204, 106), (255, 255, 255), (15, 35, 71)
    tag = f"CLASS {b['class']} {b['subject'].upper()}"
    tw = d.textlength(tag, font=font("Inter-Bold.otf", 30))
    d.rounded_rectangle((70, 80, 70 + tw + 60, 146), 33, fill=(201, 162, 39))
    d.text((100, 113), tag, font=font("Inter-Bold.otf", 30), fill=navy, anchor="lm")
    # lightning bolt
    d.polygon([(905, 330), (820, 500), (885, 500), (845, 650), (960, 450), (895, 450), (945, 330)], fill=(232, 204, 106))
    d.text((72, 205), "WEEKLY KNOWLEDGE", font=font("Inter-Bold.otf", 52), fill=gold)
    d.text((72, 265), "BOOSTER", font=font("Poppins-Bold.ttf", 120), fill=white)
    d.text((74, 420), f"Week of {date.fromisoformat(b['_monday']):%d %B %Y}".replace(" 0", " "), font=font("Inter-Regular.otf", 38), fill=(205, 216, 238))
    y = 500
    for n, t in zip(b["chapter_numbers"], b["chapters"]):
        for i, line in enumerate(textwrap.wrap(f"Ch {n}: {t}", 26)[:2]):
            d.text((72, y), line, font=font("Inter-Bold.otf", 46), fill=white)
            y += 58
        y += 12
    feats = [(f"{len(b.get('ar', []))}", "Assertion–Reason"), (f"{len(b.get('case', []))}", "Case studies"),
             (f"{len(b.get('hots', []))}", "HOTS"), (f"{len(b.get('competency', []))}", "Competency-based"),
             (f"{len(b.get('knowledge', []))}", "Knowledge check")]
    fy = max(y + 30, 760)
    for i, (num, lab) in enumerate(feats):
        x = 72 + (i % 2) * 470
        yy = fy + (i // 2) * 92
        d.rounded_rectangle((x, yy, x + 440, yy + 74), 18, fill=(28, 58, 110), outline=(201, 162, 39), width=2)
        d.text((x + 50, yy + 37), num, font=font("Poppins-Bold.ttf", 40), fill=gold, anchor="mm")
        d.text((x + 96, yy + 37), lab, font=font("Inter-Bold.otf", 32), fill=white, anchor="lm")
    d.rounded_rectangle((70, 1130, W - 70, 1240), 55, fill=(201, 162, 39))
    d.text((W // 2, 1185), f"{len(BP_texts(b))} QUESTIONS + ANSWERS · FREE", font=font("Inter-Bold.otf", 40), fill=navy, anchor="mm")
    d.text((W // 2, 1290), "cbsemock.org.in", font=font("Inter-Bold.otf", 34), fill=(255, 228, 160), anchor="mm")
    POSTERS.mkdir(parents=True, exist_ok=True)
    im.save(poster_path(b), quality=90, optimize=True)
    return poster_path(b)


def captions(b):
    ch = " + ".join(f"Ch {n}: {t}" for n, t in zip(b["chapter_numbers"], b["chapters"]))
    head = f"⚡ Weekly Knowledge Booster — Class {b['class']} {b['subject']}\n{ch}"
    body = (f"✅ {len(b.get('ar', []))} Assertion–Reason\n✅ {len(b.get('case', []))} case studies\n✅ {len(b.get('hots', []))} HOTS\n"
            f"✅ {len(b.get('competency', []))} competency-based\n✅ {len(b.get('knowledge', []))} knowledge questions\n"
            f"All with model answers — practise online or print.\n")
    tags = f"#CBSE #Class{b['class']} #{b['subject'].replace(' ', '')} #BoardExam2027 #CBSEMock"
    tg = f"{head}\n\n{body}\n👉 Practise free: {url(b)}\n\n{tags}"
    ig = f"{head}\n\n{body}\n🔗 Link in bio (cbsemock.org.in/go)\n\n{tags}"
    return tg, tg, ig


def post(b, dry):
    import post_formula_image as P
    img = f"{GH_RAW}/{poster_path(b).relative_to(ROOT).as_posix()}"
    tg, fb, ig = captions(b)
    ok = False
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if dry:
        print("[TG dry-run]", tg[:160])
    elif token and chat:
        try:
            data = urllib.parse.urlencode({"chat_id": chat, "photo": img, "caption": tg[:1024]}).encode()
            with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendPhoto", data=data, timeout=30) as r:
                ok = json.load(r).get("ok", False)
                print("[TG] posted")
        except Exception as e:
            print(f"::warning::Telegram post failed: {e}")
    ok = bool(P.post_to_facebook(img, fb, dry_run=dry)) or ok
    ok = bool(P.post_to_instagram(img, ig, dry_run=dry)) or ok
    return ok


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--render", action="store_true")
    a.add_argument("--post", action="store_true")
    a.add_argument("--dry-run", action="store_true")
    a.add_argument("--all", action="store_true", help="render posters for every booster (preview)")
    a = a.parse_args()
    todo = BP.load_boosters() if a.all else pending()
    if not todo:
        print("[announce] nothing new to announce"); return
    if a.render:
        for b in todo:
            print("[announce] poster", render(b).relative_to(ROOT))
    if a.post:
        pr = progress()
        for b in todo:
            if not poster_path(b).exists():
                render(b)
            if post(b, a.dry_run) and not a.dry_run:
                pr.setdefault(b["_id"], {})["announced"] = True
        if not a.dry_run:
            PROGRESS.write_text(json.dumps(pr, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
