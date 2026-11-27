#!/usr/bin/env python3
"""
youtube_upload.py — upload the planned YouTube Shorts, each scheduled to go public at its slot.

Plan:     youtube/plan.json      {date, time (IST), series, group, title, drive_path}  — one entry per Short
Done:     youtube/uploaded.json  {drive_path: {id, url, publish_at, uploaded_at}}
Source:   the full-quality original in Google Drive ("CBSEMock Reels/<drive_path>"), via rclone
Login:    YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (scope youtube.upload) — GitHub secrets

    python3 youtube_upload.py schedule [--hours 54] [--dry-run]   upload every planned Short due within the next N hours
    python3 youtube_upload.py extend                               add new reels (not yet in the plan) to the end of their lane
    python3 youtube_upload.py playlists                            put uploaded Shorts into their class-wise playlists
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


# ── Playlists (class-wise) ───────────────────────────────────────────────────
PLAYLISTS_FILE = ROOT / "youtube" / "playlists.json"
PLAYLISTS = {   # key → (title, description)
    "c10-maths":   ("Class 10 Maths — CBSE Board Shorts", "Class 10 Maths in under a minute: WHY? explainers, formula revision and exam tips for the CBSE board exams. Free notes & mock papers: https://cbsemock.org.in"),
    "c10-science": ("Class 10 Science — CBSE Board Shorts", "Class 10 Science (Physics, Chemistry, Biology) in under a minute: WHY? explainers, formula revision and common board-exam mistakes. https://cbsemock.org.in"),
    "c10-ai":      ("Class 10 Artificial Intelligence — Shorts", "Class 10 AI (CBSE code 417) concepts explained simply. https://cbsemock.org.in"),
    "c12-physics": ("Class 12 Physics — CBSE Board Shorts", "Class 12 Physics in under a minute: WHY? explainers and formula revision for the CBSE board exams. https://cbsemock.org.in"),
    "c12-chemistry": ("Class 12 Chemistry — CBSE Board Shorts", "Class 12 Chemistry in under a minute: WHY? explainers and formula revision for the CBSE board exams. https://cbsemock.org.in"),
    "c12-maths":   ("Class 12 Maths — CBSE Board Shorts", "Class 12 Maths in under a minute: WHY? explainers and formula revision for the CBSE board exams. https://cbsemock.org.in"),
    "c12-biology": ("Class 12 Biology — CBSE Board Shorts", "Class 12 Biology in under a minute: WHY? explainers and formula revision for the CBSE board exams. https://cbsemock.org.in"),
    "c12-cs":      ("Class 12 Computer Science — Python Shorts", "Class 12 Computer Science and Python concepts explained in under a minute. https://cbsemock.org.in"),
    "why":         ("WHY? Series — Understand, Don't Memorise", "One concept, one picture, under a minute. Why is sin²θ + cos²θ = 1? Why is a circle's area πr²? CBSE Class 10 & 12 concepts explained so you never have to cram them. Free notes & mock papers: https://cbsemock.org.in"),
    "board-plan":  ("Board Exam Strategy 2027 — Shorts", "Smart CBSE board-exam strategy: step marking, time management, board FAQs and daily score hacks. https://cbsemock.org.in"),
    "hindi":       ("हिंदी में WHY? — CBSE Shorts (Hindi)", "CBSE कक्षा 10 और 12 के कॉन्सेप्ट हिंदी में, एक मिनट से कम में। फ्री नोट्स और मॉक पेपर: https://cbsemock.org.in"),
}


def playlist_keys(e):
    """Which class-wise playlists a planned Short belongs to."""
    g, t = e.get("group", ""), e.get("title", "").lower()
    keys = []
    if e.get("series") == "Board Plan":
        keys.append("board-plan")
    elif g == "Class 10 Maths":
        keys.append("c10-maths")
    elif g in ("Class 10 Science", "Class 10 Physics", "Class 10 Chemistry", "Class 10 Biology"):
        keys.append("c10-science")
    elif g == "AI":
        keys.append("c10-ai")
    elif g in ("Class 12 CS", "CS"):
        keys.append("c12-cs")
    elif g in ("Class 12 Physics", "Class 12 Chemistry", "Class 12 Maths", "Class 12 Biology"):
        keys.append("c12-" + g.split()[-1].lower())
    elif g in ("Class 12 Science", "Science"):   # WHY? reels tagged only "Science": decide by the topic
        if re.search(r"dna|gene|protein|blood|cell", t):
            keys.append("c12-biology")
        elif re.search(r"reaction|rate|mole|acid|bond", t):
            keys.append("c12-chemistry")
        else:
            keys.append("c12-physics")
    if e.get("series") == "WHY":
        keys.append("why")
    if e.get("series") == "WHY Hindi":
        keys.append("hindi")
    return keys


def _yt(token, method, path, body=None, params=None):
    q = urllib.parse.urlencode(params or {})
    req = urllib.request.Request(f"https://www.googleapis.com/youtube/v3/{path}?{q}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def playlist_id(token, key, cache):
    if key in cache:
        return cache[key]
    title, desc = PLAYLISTS[key]
    res = _yt(token, "POST", "playlists", {"snippet": {"title": title, "description": desc, "defaultLanguage": "hi" if key == "hindi" else "en"},
                                          "status": {"privacyStatus": "public"}}, {"part": "snippet,status"})
    cache[key] = res["id"]
    jsave(PLAYLISTS_FILE, cache)
    print(f"[yt] created playlist '{title}' → {res['id']}")
    return res["id"]


def add_to_playlists(token, plan=None, limit=60):
    """Put every uploaded Short into its class-wise playlists (idempotent; remembered in uploaded.json)."""
    plan = plan or jload(PLAN, {}).get("plan", [])
    done, cache = jload(DONE, {}), jload(PLAYLISTS_FILE, {})
    by_path = {e["drive_path"]: e for e in plan}
    n = 0
    for path, u in done.items():
        e = by_path.get(path)
        if not e:
            continue
        for key in playlist_keys(e):
            if key in u.get("playlists", []):
                continue
            if n >= limit:
                return n
            try:
                pid = playlist_id(token, key, cache)
                _yt(token, "POST", "playlistItems", {"snippet": {"playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": u["id"]}}},
                    {"part": "snippet"})
                u.setdefault("playlists", []).append(key)
                jsave(DONE, done)
                n += 1
            except urllib.error.HTTPError as err:
                body = err.read().decode()[:200]
                if "insufficient" in body.lower() or err.code == 403:
                    print("[yt] playlists need the broader YouTube permission — refresh token has upload-only scope; skipping")
                    return n
                print(f"[yt] playlist add failed for {path}: {err.code} {body}")
    print(f"[yt] {n} playlist entr{'y' if n == 1 else 'ies'} added")
    return n


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
    try:
        add_to_playlists(token)
    except Exception as err:
        print(f"[yt] playlists: {err}")
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
    elif a[0] == "playlists":
        add_to_playlists(access_token())
    else:
        status()
