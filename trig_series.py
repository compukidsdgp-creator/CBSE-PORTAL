#!/usr/bin/env python3
"""
trig_series.py — the WHY? trigonometry series that follows the viral reel (Part 1: sin²θ + cos²θ = 1, 19 Nov 2026).

Each part takes over an existing slot on its date, so the total number of posts stays the same:
    Part 2 · Sat 21 Nov · 8 PM formula-reel slot   (formula reel skipped that evening)
    Part 3 · Sun 22 Nov · WHY? slot                 (the queued WHY? reel moves to the next WHY? day)
    Part 4 · Mon 23 Nov · 8 PM formula-reel slot

    python3 trig_series.py due formula|why     exit 0 if a part is due now in that slot (the workflow then posts it instead)
    python3 trig_series.py post formula|why [--dry-run]
    python3 trig_series.py teaser [--dry-run]  comment on Part 1: "Part 2 drops tomorrow at 8 PM" (owner pins it)
    python3 trig_series.py digest <part>       private Telegram list of the new part's comments (run ~1 h after posting)
    python3 trig_series.py status

After posting a part it also: comments on the new part ("Part N of the series… pin me"), comments on the previous
part ("Part N is out now"), and sends the owner a private Telegram note to pin the comment. Instagram/Facebook do
not allow pinning comments through their API, so pinning stays a one-tap job for the owner.
Saturday's run also re-posts the full Part 1 to Facebook (the original FB upload was cut off by the old upload bug).
"""
import json
import os
import shutil
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import post_formula_reel as P
import social_links as SL

ROOT = Path(__file__).parent
DIR = ROOT / "formula-posts" / "why" / "series"
STATE = DIR / "state.json"
IST = timezone(timedelta(hours=5, minutes=30))
P.LOG_CSV = ROOT / "formula-posts" / "why" / "why_log.csv"
FB_API = "https://graph.facebook.com/v27.0"

PART1 = {"part": 1, "file": ROOT / "formula-posts" / "why" / "posted" / "04_why_trig_identity.mp4",
         "ig": "18061669220800240", "fb": "1144091108104391", "title": "sin²θ + cos²θ = 1"}
PARTS = [
    {"part": 2, "module": "trig_sec", "date": "2026-11-21", "slot": "formula", "title": "1 + tan²θ = sec²θ",
     "next": "Part 3 tomorrow (Sun) at 5 PM: Why is sin 30° exactly ½?"},
    {"part": 3, "module": "sin30_half", "date": "2026-11-22", "slot": "why", "title": "sin 30° = ½",
     "next": "Part 4 tomorrow (Mon) at 8 PM: Why is elevation = depression?"},
    {"part": 4, "module": "elevation_depression", "date": "2026-11-23", "slot": "formula",
     "title": "angle of elevation = angle of depression", "next": ""},
]


def video(p):
    return DIR / f"why_{p['module']}.mp4"


def state():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save(st):
    STATE.write_text(json.dumps(st, indent=1) + "\n", encoding="utf-8")


def today():
    return datetime.now(IST).date().isoformat()


def due(slot):
    st = state()
    return next((p for p in PARTS if p["date"] == today() and p["slot"] == slot and str(p["part"]) not in st
                 and video(p).exists()), None)


def owner(text):
    tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("SEO_REPORT_CHAT_ID")
    if not (tok and chat):
        print("[owner]", text); return
    req = urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage",
                                 data=json.dumps({"chat_id": chat, "text": text, "disable_web_page_preview": True}).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=20)
    except Exception as e:
        print("[owner] telegram failed:", e)


def ig_comment(media_id, message, dry=False):
    """Comment on an Instagram post as the page (needs instagram_manage_comments)."""
    if dry or not media_id or str(media_id).startswith("dry"):
        print(f"[IG comment] (dry) on {media_id}: {message}"); return None
    tok = P.IG_TOKEN
    data = urllib.parse.urlencode({"message": message, "access_token": tok}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(f"{FB_API}/{media_id}/comments", data=data), timeout=30) as r:
            cid = json.load(r).get("id")
            print(f"[IG comment OK] {cid}")
            return cid
    except urllib.error.HTTPError as e:
        print(f"[IG comment FAILED] {e.code}: {e.read().decode()[:300]}")
        return None


def caption(p):
    import importlib
    return importlib.import_module(f"why_reels.{p['module']}").CAPTION.strip()


def post(slot, dry=False):
    p = due(slot)
    if not p:
        print(f"[series] nothing due in the {slot} slot today"); return False
    st = state()
    prev = PART1 if p["part"] == 2 else {**next(x for x in PARTS if x["part"] == p["part"] - 1), **st.get(str(p["part"] - 1), {})}
    # Saturday: full Part 1 on Facebook first (the original FB copy was cut off)
    if p["part"] == 2 and "1fb" not in st and PART1["file"].exists():
        cap1 = (ROOT / "formula-posts" / "why" / "posted" / "04_why_trig_identity.txt")
        c1 = cap1.read_text(encoding="utf-8").strip() if cap1.exists() else "📐 WHY? — Why is sin²θ + cos²θ = 1?"
        fb1 = P._upload_video_fb(PART1["file"], "🔁 Full version — Part 1 of the trig series\n\n" + c1, dry_run=dry)
        if fb1 and not dry:
            st["1fb"] = fb1; save(st)
    cap = caption(p)
    fb = P._upload_video_fb(video(p), cap, dry_run=dry)
    ig = P._upload_reel_instagram(video(p), SL.ig_caption(cap), dry_run=dry)
    P.log_reel(video(p).name, fb, ig, dry)
    if not (fb or ig):
        owner(f"⚠️ Trig series Part {p['part']} failed to post on both Facebook and Instagram — check the run.")
        return False
    pin = (f"📌 Part {p['part']} of the WHY? trig series. "
           f"{'Part 1' if p['part'] == 2 else 'Parts 1–' + str(p['part'] - 1)} on our profile 👆"
           + (f" · 🔔 {p['next']}" if p["next"] else " · Follow for more WHY? videos!"))
    ig_c = ig_comment(ig, pin, dry)
    fb_c = SL.post_fb_comment(fb, pin + "\n🌐 https://cbsemock.org.in", P.FB_TOKEN, dry_run=dry)
    nudge = f"🔥 Part {p['part']} is out now: Why is {p['title']}? Watch it on our profile 👆"
    ig_comment(prev.get("ig"), nudge, dry)
    SL.post_fb_comment(st.get("1fb") if p["part"] == 2 and st.get("1fb") else prev.get("fb"), nudge, P.FB_TOKEN, dry_run=dry)
    if not dry:
        st[str(p["part"])] = {"ig": ig, "fb": fb, "at": datetime.now(IST).isoformat(timespec="seconds")}
        save(st)
    owner(f"✅ Trig series Part {p['part']} is live (FB {'✓' if fb else '✗'} · IG {'✓' if ig else '✗'}).\n\n"
          f"📌 Please pin this comment (long-press it → Pin)."
          f"{'' if ig_c else ' Instagram: it could not be posted automatically — add it yourself.'}"
          f"{'' if fb_c else ' Facebook: it could not be posted automatically — add it yourself.'}\n\n{pin}\n\n"
          f"I'll send you the first comments in about an hour.")
    return True


def teaser(dry=False):
    st = state()
    if "teaser" in st:
        print("[series] teaser already posted"); return
    msg = "🔥 This blew up! Part 2 drops tomorrow (Sat) at 8 PM: Why is 1 + tan²θ = sec²θ? Follow so you don't miss it 🔔"
    ig_c = ig_comment(PART1["ig"], msg, dry)
    fb_c = SL.post_fb_comment(PART1["fb"], msg, P.FB_TOKEN, dry_run=dry)
    if not dry:
        st["teaser"] = {"ig": ig_c, "fb": fb_c}; save(st)
    owner("📌 Teaser comment posted on Part 1 (the viral reel). Please pin it on Instagram: long-press the comment → Pin.\n\n"
          + msg + ("" if ig_c else "\n\n(It could not be posted on Instagram automatically — please add it yourself.)"))


def digest(part):
    st = state().get(str(part)) or {}
    lines = []
    for kind, mid in (("Instagram", st.get("ig")), ("Facebook", st.get("fb"))):
        if not mid:
            continue
        tok = P.IG_TOKEN if kind == "Instagram" else P.FB_TOKEN
        fields = "text,username,like_count" if kind == "Instagram" else "message,from,like_count"
        try:
            q = urllib.parse.urlencode({"fields": fields, "limit": 50, "access_token": tok})
            with urllib.request.urlopen(f"{FB_API}/{mid}/comments?{q}", timeout=30) as r:
                data = json.load(r).get("data", [])
        except Exception as e:
            lines.append(f"{kind}: could not read comments ({str(e)[:80]})"); continue
        data = [d for d in data if not (d.get("text") or d.get("message") or "").startswith(("📌", "🔥"))]
        lines.append(f"— {kind}: {len(data)} comment(s)")
        for d in sorted(data, key=lambda d: -int(d.get("like_count", 0)))[:12]:
            who = d.get("username") or (d.get("from") or {}).get("name", "")
            lines.append(f"• {who}: {(d.get('text') or d.get('message') or '')[:160]}")
    owner(f"💬 Part {part} — first-hour comments. Reply to the top ones yourself (it helps reach):\n\n" + "\n".join(lines or ["No comments yet."]))


def status():
    st = state()
    for p in PARTS:
        print(f"Part {p['part']} {p['date']} {p['slot']:7} video={'yes' if video(p).exists() else 'NO'} posted={'yes' if str(p['part']) in st else 'no'}")


if __name__ == "__main__":
    a = sys.argv[1:] or ["status"]
    dry = "--dry-run" in a
    if a[0] == "due":
        sys.exit(0 if due(a[1]) else 1)
    elif a[0] == "post":
        sys.exit(0 if post(a[1], dry) else 1)
    elif a[0] == "teaser":
        teaser(dry)
    elif a[0] == "digest":
        digest(int(a[1]))
    else:
        status()
