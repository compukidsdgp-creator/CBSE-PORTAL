"""Build the admin dashboard data and seal it with the admin password.

Output: admin/data/vault.json — AES-256-GCM, key from PBKDF2-SHA256(ADMIN_PASSWORD).
Inside the vault: KPIs, queue runways, posting history, rotation progress, website traffic
(GA4 + Search Console when their secrets are set) and the GitHub token the admin panel uses
to save ad settings. Nothing readable is published; the page decrypts it in the browser.

Environment:
  ADMIN_PASSWORD               required to write the vault
  ADMIN_GH_TOKEN               fine-grained token (this repo: Contents + Actions read/write)
  GSC_SERVICE_ACCOUNT_JSON     optional — Search Console clicks / impressions / queries
  GSC_PROPERTY                 optional — "https://cbsemock.org.in/" (default, URL-prefix property) or "sc-domain:cbsemock.org.in"
  GA4_PROPERTY_ID              optional — numeric GA4 property id (same service account)
  GITHUB_TOKEN                 optional — counts promo / WHY? runs via the Actions API

  python3 build_admin_data.py [--plain out.json]   # --plain also writes unencrypted data (local preview only)
"""
import argparse
import base64
import csv
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IST = timezone(timedelta(hours=5, minutes=30))
TODAY = datetime.now(IST).date()
REPO = os.environ.get("GITHUB_REPOSITORY", "compukidsdgp-creator/CBSE-PORTAL")
HISTORY_DAYS = 45

# Weekly posting rhythm (for the "post cycle" chart). Times are IST.
SCHEDULE = [
    # day 0=Mon … 6=Sun, time, label, kind
    *[(d, "08:00", "Formula image", "image") for d in range(7)],
    *[(d, "20:00", "Formula image", "image") for d in range(7)],
    *[(d, "20:00", "Formula reel (voiced)", "reel") for d in range(7)],
    *[(d, "07:00", "Telegram: quiz · notes · papers · lab", "telegram") for d in range(7)],
    *[(d, "18:00", "Telegram: news digest", "telegram") for d in range(7)],
    *[(d, "15:00", "Mock papers (Class 10 + 12)", "paper") for d in (0, 2, 4)],
    *[(d, "18:30", "WHY? reel", "why") for d in (6, 2)],
    *[(d, "11:30", "Weekend promo", "promo") for d in (5, 6)],
    (0, "06:00", "Weekly Focus lesson", "focus"),
    (0, "06:30", "Weekly Booster goes live", "focus"),
    *[(d, "09:30", "Newsroom update", "telegram") for d in range(7)],
    *[(d, "13:01", "Board Plan reel (English)", "reel") for d in range(5)],
    *[(d, "19:31", "Board Plan reel (Hindi)", "reel") for d in range(5)],
    *[(d, "17:31", "Mistake Bank reel (English)", "reel") for d in range(7)],
    *[(d, "21:01", "Mistake Bank reel (Hindi)", "reel") for d in range(7)],
]


def sh(*args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True).stdout


def d(s):
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except Exception:
        return None


# ── Posting history ──────────────────────────────────────────────────────────
def events():
    ev = []                                             # (date, kind, label, platforms)
    # formula images
    p = ROOT / "formula-posts" / "post_log.csv"
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8")):
            if str(r.get("dry_run")).lower() == "true":
                continue
            ev.append((d(r["timestamp_ist"]), "image", Path(r["filename"]).stem, "FB · IG"))
    # formula reels
    p = ROOT / "formula-posts" / "reel_log.csv"
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8")):
            if str(r.get("dry_run")).lower() == "true" or "FAILED" in (r.get("fb_video_id") or ""):
                continue
            ev.append((d(r["date_ist"]), "reel", r.get("topic_id", ""), "FB · IG"))
    # WHY? reels
    p = ROOT / "formula-posts" / "why" / "why_log.csv"
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8")):
            if str(r.get("dry_run")).lower() == "true":
                continue
            day = r.get("date_ist") or r.get("timestamp_ist") or ""
            ev.append((d(day), "why", r.get("topic_id") or r.get("filename", ""), "FB · IG"))
    # mock papers
    p = ROOT / "question-bank" / "calendar.json"
    if p.exists():
        cal = json.loads(p.read_text(encoding="utf-8"))
        for day, slots in cal.items():
            for cls, info in slots.items():
                if isinstance(info, dict) and info.get("posted"):
                    ev.append((d(day), "paper", info.get("paper_id", cls), "TG · FB · IG"))
    # Telegram / FB / IG rotation items (notes, practice papers, labs, weekly focus)
    p = ROOT / "social-posting-tracker.csv"
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8")):
            seen = {}
            for plat in ("telegram", "facebook", "instagram"):
                m = re.search(r"(\d{4}-\d{2}-\d{2})", r.get(plat) or "")
                if m:
                    seen.setdefault(m.group(1), []).append({"telegram": "TG", "facebook": "FB", "instagram": "IG"}[plat])
            for day, plats in seen.items():
                ev.append((d(day), "rotation:" + r["content_type"], r["title"], " · ".join(plats)))
    return [e for e in ev if e[0]]


def workflow_runs(wf):
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("ADMIN_GH_TOKEN")
    if not tok:
        return []
    since = (TODAY - timedelta(days=HISTORY_DAYS)).isoformat()
    url = (f"https://api.github.com/repos/{REPO}/actions/workflows/{wf}/runs"
           f"?status=success&per_page=100&created=%3E%3D{since}")
    try:
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}",
                                                   "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            runs = json.load(r).get("workflow_runs", [])
        out = []
        for run in runs:
            t = datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).astimezone(IST)
            out.append(t.date())
        return out
    except Exception as e:
        print(f"[warn] could not read {wf} runs: {e}", file=sys.stderr)
        return []


# ── Queues / runway ──────────────────────────────────────────────────────────
def count(folder, exts):
    f = ROOT / folder
    return sum(1 for p in f.iterdir() if p.suffix.lower() in exts) if f.exists() else 0


def runway_date(n, days_of_week, per_day=1):
    """Date the queue runs out if `per_day` items go on each of `days_of_week`."""
    left, day = n, TODAY
    last = None
    while left > 0 and (day - TODAY).days < 800:
        if day.weekday() in days_of_week:
            left -= per_day
            last = day
        day += timedelta(days=1)
    return last.isoformat() if last else None


def queues():
    imgs = count("formula-posts/queue", {".jpg", ".jpeg", ".png"})
    reels = count("formula-posts/videos/queue", {".mp4"})
    why = count("formula-posts/why/queue", {".mp4"})
    cal = json.loads((ROOT / "question-bank" / "calendar.json").read_text(encoding="utf-8")) \
        if (ROOT / "question-bank" / "calendar.json").exists() else {}
    paper_days = sorted(day for day, s in cal.items()
                        if d(day) and d(day) >= TODAY and not all(isinstance(v, dict) and v.get("posted") for v in s.values()))
    return [
        {"name": "Formula images", "left": imgs, "rate": "2 a day", "until": runway_date(imgs, range(7), 2)},
        {"name": "Formula reels", "left": reels, "rate": "1 a day", "until": runway_date(reels, range(7), 1)},
        {"name": "WHY? reels", "left": why, "rate": "Sun + Wed", "until": runway_date(why, (6, 2), 1)},
        {"name": "Mock papers", "left": len(paper_days), "rate": "Mon · Wed · Fri", "until": paper_days[-1] if paper_days else None},
    ]


def rotation():
    p = ROOT / "social-posting-tracker.csv"
    out = defaultdict(lambda: {"total": 0, "telegram": 0, "facebook": 0, "instagram": 0})
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8")):
            o = out[r["content_type"]]
            o["total"] += 1
            for plat in ("telegram", "facebook", "instagram"):
                if (r.get(plat) or "").strip().startswith("✓"):
                    o[plat] += 1
    return dict(out)


# ── Website traffic (optional) ───────────────────────────────────────────────
def google_token(scope):
    raw = os.environ.get("GSC_SERVICE_ACCOUNT_JSON")
    if not raw:
        return None
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
        creds = service_account.Credentials.from_service_account_info(json.loads(raw), scopes=[scope])
        creds.refresh(Request())
        return creds.token
    except Exception as e:
        print(f"[warn] Google auth failed: {e}", file=sys.stderr)
        return None


def post_json(url, body, token):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def search_console():
    tok = google_token("https://www.googleapis.com/auth/webmasters.readonly")
    if not tok:
        return None
    prop = os.environ.get("GSC_PROPERTY") or "https://cbsemock.org.in/"
    base = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(prop, safe='')}/searchAnalytics/query"
    end = TODAY - timedelta(days=2)                     # Search Console lags ~2 days
    start = end - timedelta(days=27)
    try:
        daily = post_json(base, {"startDate": str(start), "endDate": str(end), "dimensions": ["date"]}, tok).get("rows", [])
        queries = post_json(base, {"startDate": str(start), "endDate": str(end), "dimensions": ["query"],
                                   "rowLimit": 15}, tok).get("rows", [])
        pages = post_json(base, {"startDate": str(start), "endDate": str(end), "dimensions": ["page"],
                                 "rowLimit": 200}, tok).get("rows", [])
    except Exception as e:
        print(f"[warn] Search Console query failed: {e}", file=sys.stderr)
        return {"error": str(e)[:200]}
    near = [p for p in pages if 4.5 <= p.get("position", 99) <= 15]
    near.sort(key=lambda p: -p.get("impressions", 0))
    return {
        "range": [str(start), str(end)],
        "daily": [{"date": r["keys"][0], "clicks": r["clicks"], "impressions": r["impressions"]} for r in daily],
        "queries": [{"q": r["keys"][0], "clicks": r["clicks"], "impressions": r["impressions"],
                     "position": round(r["position"], 1)} for r in queries],
        "near_top": [{"page": r["keys"][0].replace("https://cbsemock.org.in", "") or "/", "impressions": r["impressions"],
                      "position": round(r["position"], 1)} for r in near[:10]],
    }


def analytics():
    prop = os.environ.get("GA4_PROPERTY_ID")
    tok = google_token("https://www.googleapis.com/auth/analytics.readonly") if prop else None
    if not tok:
        return None
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport"
    try:
        daily = post_json(url, {"dateRanges": [{"startDate": "28daysAgo", "endDate": "today"}],
                                "dimensions": [{"name": "date"}],
                                "metrics": [{"name": "activeUsers"}, {"name": "screenPageViews"}, {"name": "sessions"}]}, tok)
        pages = post_json(url, {"dateRanges": [{"startDate": "28daysAgo", "endDate": "today"}],
                                "dimensions": [{"name": "pagePath"}], "metrics": [{"name": "screenPageViews"}],
                                "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}], "limit": 12}, tok)
        sources = post_json(url, {"dateRanges": [{"startDate": "28daysAgo", "endDate": "today"}],
                                  "dimensions": [{"name": "sessionDefaultChannelGroup"}], "metrics": [{"name": "sessions"}],
                                  "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}], "limit": 8}, tok)
    except Exception as e:
        print(f"[warn] GA4 query failed: {e}", file=sys.stderr)
        return {"error": str(e)[:200]}
    rows = sorted(daily.get("rows", []), key=lambda r: r["dimensionValues"][0]["value"])
    return {
        "daily": [{"date": f'{r["dimensionValues"][0]["value"][:4]}-{r["dimensionValues"][0]["value"][4:6]}-{r["dimensionValues"][0]["value"][6:]}',
                   "users": int(r["metricValues"][0]["value"]), "views": int(r["metricValues"][1]["value"]),
                   "sessions": int(r["metricValues"][2]["value"])} for r in rows],
        "pages": [{"path": r["dimensionValues"][0]["value"], "views": int(r["metricValues"][0]["value"])}
                  for r in pages.get("rows", [])],
        "sources": [{"name": r["dimensionValues"][0]["value"], "sessions": int(r["metricValues"][0]["value"])}
                    for r in sources.get("rows", [])],
    }


# ── Assemble ─────────────────────────────────────────────────────────────────
def build():
    ev = events()
    for day in workflow_runs("weekly-promo.yml"):
        ev.append((day, "promo", "Weekend promo", "TG · FB · IG"))
    start = TODAY - timedelta(days=HISTORY_DAYS - 1)
    by_day = defaultdict(Counter)
    for day, kind, _, _ in ev:
        if start <= day <= TODAY:
            by_day[day.isoformat()][kind.split(":")[0]] += 1
    days = [(start + timedelta(days=i)).isoformat() for i in range(HISTORY_DAYS)]
    kinds = ["image", "reel", "why", "paper", "promo", "rotation"]
    recent = sorted(ev, key=lambda e: e[0], reverse=True)[:25]
    last7 = sum(1 for e in ev if (TODAY - e[0]).days < 7)
    prev7 = sum(1 for e in ev if 7 <= (TODAY - e[0]).days < 14)
    ads = json.loads((ROOT / "ads-config.json").read_text(encoding="utf-8"))
    return {
        "generated_at": datetime.now(IST).strftime("%Y-%m-%d %H:%M IST"),
        "kpis": {"posts_7d": last7, "posts_prev_7d": prev7, "posts_total": len(ev),
                 "live_ads": sum(1 for s in ads.get("slots", {}).values() if s.get("active") and s.get("img"))},
        "history": {"days": days, "series": {k: [by_day[x][k] for x in days] for k in kinds}},
        "queues": queues(),
        "rotation": rotation(),
        "schedule": [{"day": a, "time": b, "label": c, "kind": k} for a, b, c, k in SCHEDULE],
        "recent": [{"date": e[0].isoformat(), "kind": e[1].split(":")[-1], "label": e[2], "where": e[3]} for e in recent],
        "search_console": search_console(),
        "analytics": analytics(),
        "tracker": tracker(),
        "booster": booster(),
        "labs": labs_tracker(),
        "mistakes": mistakes_tracker(),
        "mockzone": mockzone_tracker(),
        "campaign": campaign_tracker(),
        "pending": pending_work(),
        "gh_token": os.environ.get("ADMIN_GH_TOKEN", ""),
        "repo": REPO,
    }


def tracker():
    """Content Tracker: state of every syllabus chapter (notes page, hub link, quiz, reels, Learn)."""
    try:
        import content_tracker
        return content_tracker.build()
    except Exception as e:                       # never break the dashboard over the tracker
        print(f"[warn] content tracker: {e}")
        return None


def booster():
    """Weekly Knowledge Booster: drafts to approve, schedule and coverage."""
    try:
        import booster_plan
        return booster_plan.admin_data()
    except Exception as e:
        print(f"[warn] booster tracker: {e}")
        return None


def labs_tracker():
    """Virtual labs: rebuild progress against the locked lab standard."""
    try:
        import lab_registry
        return lab_registry.admin_data()
    except Exception as e:
        print(f"[warn] labs tracker: {e}")
        return None


def mockzone_tracker():
    """Mock Zone rewrite: fresh (repeat-free) papers per subject page, in the order the nightly runs work."""
    try:
        import mockzone_build as M
        rows = []
        for page in M.PRIORITY:
            name = page.replace("cbse-class-", "Class ").replace("-mock-papers.html", "").replace("-mock-tests.html", "") \
                .replace("-practice-papers.html", "").replace("-", " ")
            name = name[:9] + name[9:].title()
            if M.bank_path(page).exists():
                b = M.load(page)
                rows.append({"page": page, "name": name, "fresh": M.fresh_papers(b), "converted": True})
            else:
                rows.append({"page": page, "name": name, "fresh": 0, "converted": False})
        done = sum(r["fresh"] for r in rows)
        return {"rows": rows, "total": len(rows) * M.PAPERS, "fresh": done, "next": M.next_job()}
    except Exception as e:
        print(f"[warn] mockzone tracker: {e}")
        return None


def campaign_tracker():
    """60-day Board Plan reels: written / rendered / posted, English + Hindi."""
    try:
        import generate_hack_reel as G
        plan = json.loads((G.BASE / "plan.json").read_text(encoding="utf-8"))["reels"]
        posted = json.loads((G.BASE / "posted.json").read_text(encoding="utf-8")) if (G.BASE / "posted.json").exists() else {}
        specs = {r["n"]: r for r in G.load_specs()}
        rows = []
        for p in plan:
            r = specs.get(p["n"])
            st = {}
            for lang in ("en", "hi"):
                if not r:
                    st[lang] = "todo"
                elif lang not in G.langs(r):
                    st[lang] = "no-hindi"
                elif (f"{r['n']:02d}-{r['id']}" + ("" if lang == "en" else f"/{lang}")) in posted:
                    st[lang] = "posted"
                elif G.video_path(r, lang).exists():
                    st[lang] = "ready"
                else:
                    st[lang] = "rendering"
            rows.append({"n": p["n"], "date": p["date"], "pillar": p["pillar"], "topic": p["topic"], "en": st["en"], "hi": st["hi"]})
        return {"rows": rows}
    except Exception as e:
        print(f"[warn] campaign tracker: {e}")
        return None


def pending_work():
    """What each nightly writer has to do next — so 'no output last night' can be judged (idle vs. failed)."""
    out = {}
    try:
        import content_tracker
        nx = content_tracker.build().get("next")
        out["notes"] = (nx or {}).get("title") and f"{nx['action']}: {nx['title']}"
    except Exception:
        pass
    try:
        import mistake_bank
        waiting = [i for i in mistake_bank.admin()["items"] if i["state"] not in ("approved",)]
        out["mistake"] = f"{len(waiting)} waiting for review" + (" — needs new scripts" if len(waiting) < 3 else "")
    except Exception:
        pass
    try:
        import lab_registry
        nx = lab_registry.next_job() if hasattr(lab_registry, "next_job") else None
        out["labs"] = nx and f"{nx.get('action')}: {nx.get('id', '')}"
    except Exception:
        pass
    try:
        import mockzone_build as M
        nx = M.next_job()
        out["mockzone"] = nx["action"] != "none" and f"{nx['action']}: {nx['page']} paper {nx.get('next_paper')}"
    except Exception:
        pass
    return out


def mistakes_tracker():
    """Mistake Bank reels: drafts to approve (English + Hindi videos)."""
    try:
        import mistake_bank
        return mistake_bank.admin()
    except Exception as e:
        print(f"[warn] mistake tracker: {e}")
        return None


def seal(data, password):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    salt, iv = os.urandom(16), os.urandom(12)
    iters = 310000
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iters).derive(password.encode())
    ct = AESGCM(key).encrypt(iv, json.dumps(data, ensure_ascii=False).encode(), None)
    b = lambda x: base64.b64encode(x).decode()
    return {"v": 1, "kdf": "PBKDF2-SHA256", "iter": iters, "salt": b(salt), "iv": b(iv), "data": b(ct)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plain", help="also write the unencrypted data here (local preview only, never commit)")
    a = ap.parse_args()
    data = build()
    if a.plain:
        Path(a.plain).write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    pw = os.environ.get("ADMIN_PASSWORD")
    if not pw:
        print("[skip] ADMIN_PASSWORD not set — vault not written")
        return
    out = ROOT / "admin" / "data" / "vault.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(seal(data, pw)), encoding="utf-8")
    print(f"[ok] {out.relative_to(ROOT)} · {data['kpis']['posts_total']} posts logged · "
          f"GSC {'on' if data['search_console'] else 'off'} · GA4 {'on' if data['analytics'] else 'off'}")


if __name__ == "__main__":
    main()
