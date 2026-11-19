"""60-day "90+ Score Hack" reel campaign — posting and owner notices.

    python3 campaign_post.py post [en|hi] [--dry-run]   post TODAY's reel (date in its spec): English 1:01 PM, Hindi 7:31 PM IST
    python3 campaign_post.py notify <video ...>   private Telegram preview of newly rendered reels (owner only)
    python3 campaign_post.py status               what is written / rendered / posted

One reel per weekday at 1:01 PM IST (cron-job.org → workflow_dispatch). A GitHub-cron fallback run is skipped when it
arrives more than 3 h late. Never posts twice on a day. If today's reel is missing, the owner gets a private alert.
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import generate_hack_reel as G

ROOT = Path(__file__).resolve().parent
IST = timezone(timedelta(hours=5, minutes=30))
POSTED = G.BASE / "posted.json"
PLAN = G.BASE / "plan.json"
SITE = "https://cbsemock.org.in"
SLOTS = {"en": (13, 1), "hi": (19, 31)}


def jload(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return {}


def link(r, source, lang="en"):
    return (f"{SITE}/{r.get('dest', '')}?utm_source={source}&utm_medium=reel&utm_campaign=90plus"
            f"&utm_content=day{r['n']:02d}{'' if lang == 'en' else '-' + lang}")


def caption(r, source, lang="en"):
    v = G.view(r, lang)
    cap = v["caption"]
    if source != "instagram":
        cap = cap.replace("link in bio (cbsemock.org.in/go)", link(r, source, lang))
    return cap + "\n\n" + " ".join(v.get("hashtags", []))


def owner_msg(text):
    import urllib.request
    tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("SEO_REPORT_CHAT_ID")
    if not (tok and chat):
        print("[owner]", text); return
    req = urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage",
                                 data=json.dumps({"chat_id": chat, "text": text, "parse_mode": "HTML",
                                                  "disable_web_page_preview": True}).encode(),
                                 headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=20)


def key(r, lang):
    return f"{r['n']:02d}-{r['id']}" + ("" if lang == "en" else f"/{lang}")


def post(lang="en", dry=False):
    now = datetime.now(IST)
    today = now.date().isoformat()
    posted = jload(POSTED)
    if any(v.get("at", "").startswith(today) and v.get("lang", "en") == lang for v in posted.values()):
        print(f"[campaign] {lang} reel already posted today"); return False
    if os.environ.get("SCHEDULED") == "1":
        h, m = SLOTS[lang]
        slot = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if not slot - timedelta(minutes=15) <= now <= slot + timedelta(hours=3):
            print(f"[campaign] scheduled run at {now:%H:%M} IST is outside the {h:02d}:{m:02d} slot — skipped"); return False
    if now.weekday() > 4:
        print("[campaign] weekend — no reel"); return False
    r = next((x for x in G.load_specs() if x["date"] == today), None)
    if r and lang not in G.langs(r):
        print(f"[campaign] reel has no {lang} version"); return False
    if not r or not G.video_path(r, lang).exists():
        plan = next((p for p in jload(PLAN).get("reels", []) if p["date"] == today), None)
        if plan:
            owner_msg(f"⚠️ <b>Campaign reel #{plan['n']:02d} ({plan['topic']}, {lang.upper()}) was not ready at its slot</b> — "
                      f"{'spec missing' if not r else 'video not rendered'}. Nothing was posted today.")
        print("[campaign] today's reel is not ready"); return False
    import post_formula_reel as P
    vid = G.video_path(r, lang)
    print(f"[campaign] posting #{r['n']:02d} {r['id']} ({lang})")
    fb = P._upload_video_fb(vid, caption(r, "facebook", lang), dry_run=dry)
    ig = P._upload_reel_instagram(vid, caption(r, "instagram", lang), dry_run=dry)
    tg = False
    if not dry:
        from tg_photo import send_video
        tg = send_video(vid, caption(r, "telegram", lang))
    if dry:
        return True
    if fb or ig or tg:
        posted[key(r, lang)] = {"at": now.isoformat(timespec="seconds"), "lang": lang, "fb": fb, "ig": ig, "tg": tg}
        POSTED.write_text(json.dumps(posted, indent=1) + "\n", encoding="utf-8")
        print(f"FB: {fb or 'FAILED'} | IG: {ig or 'FAILED'} | TG: {tg}")
        return True
    owner_msg(f"⚠️ Campaign reel #{r['n']:02d} ({lang}) failed on every platform — check the 'Campaign reel post' run.")
    return False


def notify(paths):
    """Send each newly rendered reel to the owner's private chat (preview; it posts automatically on its date)."""
    from tg_photo import send_video
    specs = {G.video_path(r, l).name: (r, l) for r in G.load_specs() for l in G.langs(r)}
    for p in paths:
        if Path(p).name not in specs:
            continue
        r, lang = specs[Path(p).name]
        d = datetime.fromisoformat(r["date"]).strftime("%a %-d %b")
        h, m = SLOTS[lang]
        send_video(Path(p), f"🎬 Campaign reel #{r['n']:02d} · {r['pillar']} · {'हिंदी' if lang == 'hi' else 'English'} — ready.\n"
                            f"Posts automatically {d}, {h % 12 or 12}:{m:02d} {'PM' if h >= 12 else 'AM'}.\n"
                            f"Want a change? Tell Claude before then.\n\n{G.view(r, lang)['caption'][:600]}",
                   chat=os.environ.get("SEO_REPORT_CHAT_ID"))


def status():
    posted, specs = jload(POSTED), {r["n"]: r for r in G.load_specs()}
    for p in jload(PLAN).get("reels", []):
        r = specs.get(p["n"])
        sts = []
        for lang in ("en", "hi"):
            st = ("—" if not r else "no-hi" if lang not in G.langs(r) else "posted" if key(r, lang) in posted
                  else "rendered" if G.video_path(r, lang).exists() else "written")
            sts.append(f"{lang}:{st:8}")
        print(f"#{p['n']:02d} {p['date']} {p['pillar']:15} {' '.join(sts)} {p['topic']}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "post":
        lang = next((a for a in sys.argv[2:] if a in ("en", "hi")), "en")
        post(lang, "--dry-run" in sys.argv)
    elif cmd == "notify":
        notify(sys.argv[2:])
    else:
        status()
