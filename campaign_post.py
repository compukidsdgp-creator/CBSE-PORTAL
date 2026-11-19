"""60-day "90+ Score Hack" reel campaign — posting and owner notices.

    python3 campaign_post.py post [--dry-run]     post TODAY's reel (date in its spec) to Facebook, Instagram, Telegram
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
SLOT = (13, 1)


def jload(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return {}


def link(r, source):
    return f"{SITE}/{r.get('dest', '')}?utm_source={source}&utm_medium=reel&utm_campaign=90plus&utm_content=day{r['n']:02d}"


def caption(r, source):
    cap = r["caption"]
    if source != "instagram":
        cap = cap.replace("link in bio (cbsemock.org.in/go)", link(r, source))
    return cap + "\n\n" + " ".join(r.get("hashtags", []))


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


def post(dry=False):
    now = datetime.now(IST)
    today = now.date().isoformat()
    posted = jload(POSTED)
    if any(v.get("at", "").startswith(today) for v in posted.values()):
        print("[campaign] already posted today"); return False
    if os.environ.get("SCHEDULED") == "1":
        slot = now.replace(hour=SLOT[0], minute=SLOT[1], second=0, microsecond=0)
        if not slot - timedelta(minutes=15) <= now <= slot + timedelta(hours=3):
            print(f"[campaign] scheduled run at {now:%H:%M} IST is outside the 13:01 slot — skipped"); return False
    if now.weekday() > 4:
        print("[campaign] weekend — no reel"); return False
    r = next((x for x in G.load_specs() if x["date"] == today), None)
    if not r or not G.video_path(r).exists():
        plan = next((p for p in jload(PLAN).get("reels", []) if p["date"] == today), None)
        if plan:
            owner_msg(f"⚠️ <b>Campaign reel #{plan['n']:02d} ({plan['topic']}) was not ready at 1:01 PM</b> — "
                      f"{'spec missing' if not r else 'video not rendered'}. Nothing was posted today.")
        print("[campaign] today's reel is not ready"); return False
    import post_formula_reel as P
    vid = G.video_path(r)
    print(f"[campaign] posting #{r['n']:02d} {r['id']}")
    fb = P._upload_video_fb(vid, caption(r, "facebook"), dry_run=dry)
    ig = P._upload_reel_instagram(vid, caption(r, "instagram"), dry_run=dry)
    tg = False
    if not dry:
        from tg_photo import send_video
        tg = send_video(vid, caption(r, "telegram"))
    if dry:
        return True
    if fb or ig or tg:
        posted[f"{r['n']:02d}-{r['id']}"] = {"at": now.isoformat(timespec="seconds"), "fb": fb, "ig": ig, "tg": tg}
        POSTED.write_text(json.dumps(posted, indent=1) + "\n", encoding="utf-8")
        print(f"FB: {fb or 'FAILED'} | IG: {ig or 'FAILED'} | TG: {tg}")
        return True
    owner_msg(f"⚠️ Campaign reel #{r['n']:02d} failed on every platform — check the 'Campaign reel post' run.")
    return False


def notify(paths):
    """Send each newly rendered reel to the owner's private chat (preview; it posts automatically on its date)."""
    from tg_photo import send_video
    specs = {G.video_path(r).name: r for r in G.load_specs()}
    for p in paths:
        r = specs.get(Path(p).name)
        if not r:
            continue
        d = datetime.fromisoformat(r["date"]).strftime("%a %-d %b")
        send_video(Path(p), f"🎬 Campaign reel #{r['n']:02d} · {r['pillar']} — ready.\nPosts automatically {d}, 1:01 PM.\n"
                            f"Want a change? Tell Claude before then.\n\n{r['caption'][:600]}",
                   chat=os.environ.get("SEO_REPORT_CHAT_ID"))


def status():
    posted, specs = jload(POSTED), {r["n"]: r for r in G.load_specs()}
    for p in jload(PLAN).get("reels", []):
        r = specs.get(p["n"])
        st = ("posted" if r and f"{r['n']:02d}-{r['id']}" in posted else "rendered" if r and G.video_path(r).exists()
              else "written" if r else "—")
        print(f"#{p['n']:02d} {p['date']} {p['pillar']:15} {st:9} {p['topic']}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "post":
        post("--dry-run" in sys.argv)
    elif cmd == "notify":
        notify(sys.argv[2:])
    else:
        status()
