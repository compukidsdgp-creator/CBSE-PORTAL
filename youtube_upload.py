#!/usr/bin/env python3
"""
youtube_upload.py — upload the planned YouTube Shorts, each scheduled to go public at its slot.

Plan:     youtube/plan.json      {date, time (IST), series, group, title, drive_path}  — one entry per Short
Done:     youtube/uploaded.json  {drive_path: {id, url, publish_at, uploaded_at}}
Source:   the full-quality original in Google Drive ("CBSEMock Reels/<drive_path>"), via rclone
Login:    YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (scope youtube.upload) — GitHub secrets

    python3 youtube_upload.py schedule [--hours 54] [--dry-run]   upload every planned Short due within the next N hours
    python3 youtube_upload.py extend                               add new reels (not yet in the plan) to the end of their lane
    python3 youtube_upload.py test                                 upload one PRIVATE test Short (not scheduled), print its link
    python3 youtube_upload.py status
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
IST = timezone(timedelta(hours=5, minutes=30))
PLAN, DONE = ROOT / "youtube" / "plan.json", ROOT / "youtube" / "uploaded.json"
LANE = {"Formula": "Formula", "WHY": "WHY"}          # everything else goes in the 1:30 PM "extra" lane
TAGS = ["CBSE", "CBSE board exam", "board exam 2027", "Class 10", "Class 12", "CBSEMock", "revision", "Shorts"]


def jload(p, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def jsave(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def owner(text):
    tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("SEO_REPORT_CHAT_ID")
    if tok and chat:
        try:
            urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage",
                                   data=json.dumps({"chat_id": chat, "text": text, "disable_web_page_preview": True}).encode(),
                                   headers={"Content-Type": "application/json"}), timeout=20)
        except Exception as e:
            print("[owner] telegram failed:", e)
    print(text)


# ── Descriptions (from the same captions as the Drive .txt files) ────────────
_caps = None


def description(drive_path):
    global _caps
    if _caps is None:
        import media_backup as MB
        _caps = {d: c for _, d, c in MB.items() if c}
    cap = _caps.get(drive_path, "")
    m = re.search(r"DESCRIPTION:\n(.*)", cap, re.S)
    body = (m.group(1) if m else cap).strip()
    body = body.replace("link in bio (cbsemock.org.in/go)", "https://cbsemock.org.in")
    if "#Shorts" not in body:
        body += "\n\n#Shorts"
    return body[:4900]


# ── Google auth + upload ─────────────────────────────────────────────────────
def access_token():
    need = ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN")
    if not all(os.environ.get(k) for k in need):
        sys.exit("YouTube secrets missing (YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN)")
    data = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"].strip(), "client_secret": os.environ["YT_CLIENT_SECRET"].strip(),
                                   "refresh_token": os.environ["YT_REFRESH_TOKEN"].strip(), "grant_type": "refresh_token"}).encode()
    try:
        with urllib.request.urlopen("https://oauth2.googleapis.com/token", data=data, timeout=30) as r:
            return json.load(r)["access_token"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]         # Google's error code only (no secrets in it)
        owner(f"⚠️ YouTube login failed: {body}\nThe YouTube refresh token / client secrets need to be checked.")
        sys.exit(f"token exchange failed: {body}")


def upload(token, video, title, desc, publish_at=None):
    """Resumable upload. publish_at (UTC datetime) → private until then, then public. None → private test."""
    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False, "embeddable": True}
    if publish_at:
        status["publishAt"] = publish_at.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    meta = {"snippet": {"title": title[:100], "description": desc, "tags": TAGS, "categoryId": "27",
                        "defaultLanguage": "hi" if re.search(r"[ऀ-ॿ]", title) else "en"},
            "status": status}
    size = video.stat().st_size
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=json.dumps(meta).encode(), method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    with urllib.request.urlopen(req, timeout=60) as r:
        loc = r.headers["Location"]
    put = urllib.request.Request(loc, data=video.read_bytes(), method="PUT",
                                 headers={"Content-Type": "video/mp4", "Content-Length": str(size)})
    with urllib.request.urlopen(put, timeout=600) as r:
        return json.load(r)


def fetch(drive_path, dst):
    import media_backup as MB
    conf = MB.rclone_conf()
    r = subprocess.run(["rclone", "--config", str(conf), "copyto", f"{MB.REMOTE}/{drive_path}", str(dst), "--retries", "5"],
                       capture_output=True, text=True)
    if r.returncode or not dst.exists():
        raise RuntimeError(f"could not fetch from Drive: {r.stderr[-300:]}")
    return dst


def when(e):
    return datetime.strptime(f"{e['date']} {e['time']}", "%Y-%m-%d %H:%M").replace(tzinfo=IST)


# ── Commands ─────────────────────────────────────────────────────────────────
def schedule(hours=54, dry=False):
    plan, done = jload(PLAN, {}).get("plan", []), jload(DONE, {})
    now = datetime.now(IST)
    due = [e for e in plan if e["drive_path"] not in done and e.get("status") != "skip"
           and now + timedelta(minutes=20) < when(e) <= now + timedelta(hours=hours)]
    late = [e for e in plan if e["drive_path"] not in done and e.get("status") != "skip" and when(e) <= now + timedelta(minutes=20)
            and when(e) > now - timedelta(days=3)]
    print(f"[yt] {len(due)} Short(s) to schedule in the next {hours} h · {len(late)} missed slot(s)")
    if not due and not late:
        return True
    token = None if dry else access_token()
    ok, bad, lines = 0, 0, []
    for e in late + due:
        pub = when(e) if e in due else None              # a missed slot goes public now (no publishAt in the past)
        print(f"[yt] {e['date']} {e['time']} {e['title']}")
        if dry:
            continue
        try:
            with tempfile.TemporaryDirectory() as tmp:
                v = fetch(e["drive_path"], Path(tmp) / Path(e["drive_path"]).name)
                if pub is None:
                    pub_utc = None
                    res = upload(token, v, e["title"], description(e["drive_path"]), None)
                    # make a missed one public straight away
                    upd = urllib.request.Request("https://www.googleapis.com/youtube/v3/videos?part=status", method="PUT",
                                                 data=json.dumps({"id": res["id"], "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}).encode(),
                                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
                    urllib.request.urlopen(upd, timeout=30)
                else:
                    pub_utc = pub.astimezone(timezone.utc)
                    res = upload(token, v, e["title"], description(e["drive_path"]), pub_utc)
            vid = res["id"]
            done[e["drive_path"]] = {"id": vid, "url": f"https://youtube.com/shorts/{vid}", "title": e["title"],
                                     "publish_at": (pub or datetime.now(IST)).isoformat(timespec="minutes"),
                                     "uploaded_at": datetime.now(IST).isoformat(timespec="seconds")}
            jsave(DONE, done)
            ok += 1
            lines.append(f"• {(pub or now):%a %d %b %I:%M %p} — {e['title']}\n  https://youtube.com/shorts/{vid}")
        except urllib.error.HTTPError as err:
            bad += 1
            body = err.read().decode()[:300]
            lines.append(f"• ⚠️ FAILED {e['title']} — {err.code} {body}")
            if "quotaExceeded" in body or "uploadLimitExceeded" in body:
                lines.append("  (YouTube's daily limit — the rest go in the next run)")
                break
        except Exception as err:
            bad += 1
            lines.append(f"• ⚠️ FAILED {e['title']} — {str(err)[:200]}")
    if ok or bad:
        head = f"▶️ YouTube: {ok} Short(s) uploaded and scheduled" + (f", {bad} FAILED" if bad else "")
        owner(head + "\n\n" + "\n".join(lines) + "\n\nTo change or stop one, open YouTube Studio → Content before its time.")
    return bad == 0


def extend():
    """Put new reels (in the Drive layout, not yet planned) at the end of their lane."""
    import media_backup as MB
    data = jload(PLAN, {})
    plan, slots = data.get("plan", []), data.get("slots", {"Formula": "07:30", "extra": "13:30", "WHY": "18:30"})
    have = {e["drive_path"] for e in plan}
    series_of = {"1": "WHY", "2": "WHY Hindi", "3": "Formula", "4": "Mistake Bank", "6": "Board Plan"}
    added = []
    first_day = (datetime.now(IST) + timedelta(days=2)).date()
    for rel, drive, cap in MB.items():
        if not rel.endswith(".mp4") or drive in have or drive[0] not in series_of or drive.startswith("9 "):
            continue
        s = series_of[drive[0]]
        lane = LANE.get(s, "extra")
        lane_dates = [datetime.fromisoformat(e["date"]).date() for e in plan if e["time"] == slots[lane]]
        day = max([first_day - timedelta(days=1)] + lane_dates) + timedelta(days=1)
        m = re.match(r"TITLE: (.*)", cap or "")
        t, grp = (m.group(1).strip() if m else Path(drive).stem), drive.split("/")[1]
        title = {"WHY": f"{t} | {grp} #Shorts", "WHY Hindi": f"{t} | {grp} (हिंदी) #Shorts",
                 "Formula": f"{t.replace(' — Formula Flash', '')} – Formula Revision | {grp} #Shorts",
                 "Mistake Bank": f"Board Exam Mistake: {t.split('—', 1)[-1].strip()} | {grp} #Shorts"}.get(s, f"{t} | CBSE Board Exam 2027 #Shorts")
        e = {"date": day.isoformat(), "time": slots[lane], "series": s, "group": grp,
             "title": title if len(title) <= 100 else title[:97] + "…", "drive_path": drive}
        plan.append(e); have.add(drive); added.append(e)
    plan.sort(key=lambda e: (e["date"], e["time"]))
    data["plan"] = plan
    jsave(PLAN, data)
    print(f"[yt] added {len(added)} new reel(s) to the plan")
    for e in added:
        print(f"  {e['date']} {e['time']} {e['title']}")
    return added


def test():
    plan = jload(PLAN, {}).get("plan", [])
    e = plan[0]
    token = access_token()
    with tempfile.TemporaryDirectory() as tmp:
        v = fetch(e["drive_path"], Path(tmp) / Path(e["drive_path"]).name)
        res = upload(token, v, "[TEST — please delete] " + e["title"], description(e["drive_path"]), None)
    owner(f"🧪 YouTube test upload worked (PRIVATE): https://youtube.com/shorts/{res['id']}\n"
          f"Check the title, description and that it shows as a Short, then delete it in YouTube Studio.")


def status():
    plan, done = jload(PLAN, {}).get("plan", []), jload(DONE, {})
    now = datetime.now(IST)
    nxt = next((e for e in plan if e["drive_path"] not in done and when(e) > now), None)
    print(f"plan: {len(plan)} Shorts · uploaded: {len(done)} · last planned day: {plan[-1]['date'] if plan else '—'}")
    print("next to upload:", f"{nxt['date']} {nxt['time']} {nxt['title']}" if nxt else "none")


if __name__ == "__main__":
    a = sys.argv[1:] or ["status"]
    if a[0] == "schedule":
        h = int(a[a.index("--hours") + 1]) if "--hours" in a else 54
        sys.exit(0 if schedule(h, "--dry-run" in a) else 1)
    elif a[0] == "extend":
        extend()
    elif a[0] == "test":
        test()
    else:
        status()
