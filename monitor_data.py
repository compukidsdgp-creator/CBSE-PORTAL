"""Monitor panel data for the admin dashboard: stock run-out dates, token expiry, repository / GitHub Pages size,
Pages build health, Actions activity and an estimate of the website's monthly bandwidth.

GitHub limits that matter for a GitHub Pages site (docs.github.com, "GitHub Pages limits" / "Repository limits"):
  published site ≤ 1 GB · repository: recommended < 1 GB, strongly recommended < 5 GB · single file hard limit 100 MB
  (warning above 50 MB) · Pages bandwidth soft limit 100 GB / month · Pages builds soft limit 10 / hour.
GitHub does not publish a site's real bandwidth, so it is estimated from Google Analytics page views × page weight.

    python3 monitor_data.py            print the monitor JSON (local check)
    python3 monitor_data.py alert      Telegram the owner when an item turns red (state kept in admin/data/monitor_state.json)
"""
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IST = timezone(timedelta(hours=5, minutes=30))
TODAY = datetime.now(IST).date()
REPO = os.environ.get("GITHUB_REPOSITORY", "compukidsdgp-creator/CBSE-PORTAL")
GB = 1024 ** 3
MB = 1024 ** 2
LIMITS = {"site_gb": 1.0, "repo_soft_gb": 1.0, "repo_hard_gb": 5.0, "bandwidth_gb": 100.0, "builds_per_hour": 10,
          "file_warn_mb": 50, "file_max_mb": 100}


def level(frac, amber=0.7, red=0.9):
    return "red" if frac >= red else "amber" if frac >= amber else "green"


def _gh(path):
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("ADMIN_GH_TOKEN")
    if not tok:
        return None
    req = urllib.request.Request(f"https://api.github.com/{path}", headers={"Authorization": f"Bearer {tok}",
                                                                          "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.load(r)
    except Exception as e:
        print(f"[monitor] {path}: {e}", file=sys.stderr)
        return None


# ── Stock run-out ────────────────────────────────────────────────────────────
def _count(folder, exts):
    f = ROOT / folder
    return sum(1 for p in f.iterdir() if p.suffix.lower() in exts) if f.exists() else 0


def _runout(n, ok_day, start=None):
    """Last day an item posts if one goes out on every day where ok_day(day) is True."""
    day, last = start or TODAY, None
    while n > 0 and (day - TODAY).days < 1200:
        if ok_day(day):
            n -= 1
            last = day
        day += timedelta(days=1)
    return last.isoformat() if last else None


def stock():
    rows = []
    def add(name, left, rate, until, note="", red=7, amber=30):
        """red / amber: days of stock below which the row turns red / amber (writer-fed pipelines use small buffers)."""
        days = (datetime.fromisoformat(until).date() - TODAY).days if until else -1
        rows.append({"name": name, "left": left, "rate": rate, "until": until, "days": days, "note": note,
                     "level": "red" if days < red else "amber" if days < amber else "green"})
    try:
        import trig_series as T
        series = {(p["date"], p["slot"]) for p in T.PARTS if str(p["part"]) not in T.state()}
    except Exception:
        series = set()
    hindi_on = (ROOT / "formula-posts/why/hindi/ENABLED").exists()
    hi_day = lambda d: hindi_on and d.weekday() in (6, 2, 4)
    # Formula images: 8 AM + 8 PM every day → count slots
    imgs = _count("formula-posts/queue", {".jpg", ".jpeg", ".png"})
    now_h = datetime.now(IST).hour
    slots_today = 2 if now_h < 8 else 1 if now_h < 20 else 0
    left, day = imgs - slots_today, TODAY
    while left > 0:
        day += timedelta(days=1); left -= 2
    add("Formula images", imgs, "8 AM + 8 PM daily", day.isoformat() if imgs else None, "grows when you add images")
    reels = _count("formula-posts/videos/queue", {".mp4"})
    add("Formula reels", reels, "8 PM, except Hindi WHY? days" if hindi_on else "8 PM daily",
        _runout(reels, lambda d: not hi_day(d) and (d.isoformat(), "formula") not in series))
    why = _count("formula-posts/why/queue", {".mp4"}) + _count("formula-posts/why/backup", {".mp4"})
    add("WHY? reels (English)", why, "Sun · Wed · Fri 5 PM",
        _runout(why, lambda d: d.weekday() in (6, 2, 4) and (d.isoformat(), "why") not in series), "+1 backup reel written daily")
    try:
        import why_hindi as WH
        ready = sum(1 for n in WH.order() if WH.video(n).exists() and not WH.posted(n))
        add("WHY? reels (Hindi)", ready, "Sun · Wed · Fri 8 PM" if hindi_on else "paused",
            _runout(ready, hi_day) if hindi_on else None, "+~3 translated nightly", red=2, amber=5)
    except Exception as e:
        print("[monitor] hindi:", e, file=sys.stderr)
    try:
        import mistake_bank as MB_
        items = MB_.admin()["items"]
        ready = [i for i in items if i["state"] == "approved" and "en" not in i.get("posted", [])]
        waiting = sum(1 for i in items if i["state"] != "approved")
        add("Mistake Bank reels", len(ready), "daily · EN 5:31 PM + HI 9:01 PM", _runout(len(ready), lambda d: True),
            f"{waiting} draft(s) waiting for your approval" if waiting else "", red=2, amber=4)
    except Exception as e:
        print("[monitor] mistake:", e, file=sys.stderr)
    try:
        plan = json.loads((ROOT / "campaign_reels/plan.json").read_text(encoding="utf-8"))["reels"]
        posted = json.loads((ROOT / "campaign_reels/posted.json").read_text(encoding="utf-8"))
        written = {int(f.name[:2]) for f in (ROOT / "campaign_reels/specs").glob("[0-9][0-9]-*.py")}
        ready = [p for p in plan if p["n"] in written and p["date"] >= TODAY.isoformat()]
        last = max((p["date"] for p in ready), default=None)
        add("Board Plan reels (written ahead)", len(ready), "weekdays · EN 1:01 PM + HI 7:31 PM", last,
            f"campaign ends {plan[-1]['date']} · writer keeps 5 days ahead", red=1, amber=3)
    except Exception as e:
        print("[monitor] campaign:", e, file=sys.stderr)
    try:
        cal = json.loads((ROOT / "question-bank/calendar.json").read_text(encoding="utf-8"))
        days = sorted(d for d, s in cal.items() if d >= TODAY.isoformat()
                      and not all(isinstance(v, dict) and v.get("posted") for v in s.values()))
        add("Mock papers (Class 10 + 12)", len(days), "Mon · Wed · Fri 3 PM", days[-1] if days else None, "stock topped up every Saturday", red=5, amber=8)
    except Exception as e:
        print("[monitor] papers:", e, file=sys.stderr)
    return rows


# ── Tokens ───────────────────────────────────────────────────────────────────
def tokens():
    rows = []
    def when(ts):
        if not ts:
            return None, "never expires", "green"
        d = datetime.fromtimestamp(int(ts), timezone.utc).astimezone(IST).date()
        days = (d - TODAY).days
        return d.isoformat(), f"{days} days left", "red" if days < 14 else "amber" if days < 30 else "green"
    for env, label in (("FB_PAGE_ACCESS_TOKEN", "Facebook Page token"), ("INSTAGRAM_ACCESS_TOKEN", "Instagram token")):
        t = os.environ.get(env)
        if not t:
            continue
        try:
            q = urllib.parse.urlencode({"input_token": t, "access_token": t})
            d = json.load(urllib.request.urlopen(f"https://graph.facebook.com/v21.0/debug_token?{q}", timeout=25)).get("data", {})
        except Exception as e:
            rows.append({"name": label, "valid": False, "detail": str(e)[:80], "level": "red"}); continue
        exp, exp_txt, lv1 = when(d.get("expires_at") or None)
        dexp, dexp_txt, lv2 = when(d.get("data_access_expires_at") or None)
        lv = "red" if not d.get("is_valid") else max((lv1, lv2), key=["green", "amber", "red"].index)
        rows.append({"name": label, "valid": bool(d.get("is_valid")), "expires": exp, "detail":
                     f"token: {exp_txt} · data access until {dexp or '—'} ({dexp_txt})", "level": lv,
                     "fix": "Open CBSEMOCKAPP in the Meta developer dashboard (or make a new token in Graph API Explorer and update the GitHub secret)"})
    t = os.environ.get("HF_TOKEN")
    if t:
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request("https://huggingface.co/api/whoami-v2",
                                                                         headers={"Authorization": f"Bearer {t}"}), timeout=25))
            rows.append({"name": "Hugging Face token (Hindi voice)", "valid": True, "detail": "never expires", "level": "green"})
        except Exception as e:
            rows.append({"name": "Hugging Face token (Hindi voice)", "valid": False, "detail": str(e)[:80], "level": "red"})
    t = os.environ.get("TELEGRAM_BOT_TOKEN")
    if t:
        try:
            ok = json.load(urllib.request.urlopen(f"https://api.telegram.org/bot{t}/getMe", timeout=20)).get("ok")
        except Exception:
            ok = False
        rows.append({"name": "Telegram bot", "valid": ok, "detail": "never expires", "level": "green" if ok else "red"})
    t = os.environ.get("ADMIN_GH_TOKEN")
    if t:
        try:
            r = urllib.request.urlopen(urllib.request.Request("https://api.github.com/user", headers={"Authorization": f"Bearer {t}"}), timeout=20)
            exp = r.headers.get("github-authentication-token-expiration")
            if exp:
                e = datetime.strptime(exp.replace(" UTC", "").strip(), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                d_, txt, lv = when(e.timestamp())
            else:
                d_, txt, lv = None, "never expires", "green"
            rows.append({"name": "Admin panel GitHub token", "valid": True, "expires": d_, "detail": txt, "level": lv})
        except Exception as e:
            rows.append({"name": "Admin panel GitHub token", "valid": False, "detail": str(e)[:80], "level": "red"})
    if os.environ.get("GSC_SERVICE_ACCOUNT_JSON"):
        rows.append({"name": "Google service account (Search Console / GA4)", "valid": True,
                     "detail": "never expires (unless the key is deleted)", "level": "green"})
    return rows


# ── Repository / Pages size ──────────────────────────────────────────────────
def repo():
    files = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True).stdout.decode().split("\0")
    sizes, by_top, by_ext, big = 0, {}, {}, []
    for f in files:
        p = ROOT / f
        if not f or not p.is_file() or f.startswith(".github/"):
            continue
        s = p.stat().st_size
        sizes += s
        top = f.split("/")[0] if "/" in f else "(site root)"
        by_top[top] = by_top.get(top, 0) + s
        ext = p.suffix.lower() or "(none)"
        grp = "videos" if ext in (".mp4", ".mov", ".webm") else "audio" if ext in (".wav", ".mp3", ".ogg") else \
              "images" if ext in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg") else \
              "pages & code" if ext in (".html", ".js", ".css", ".json", ".py", ".md", ".txt", ".xml", ".csv") else \
              "PDFs" if ext == ".pdf" else "other"
        by_ext[grp] = by_ext.get(grp, 0) + s
        if s >= 20 * MB:
            big.append({"path": f, "mb": round(s / MB, 1)})
    api = _gh(f"repos/{REPO}") or {}
    repo_gb = round(api.get("size", 0) * 1024 / GB, 2) if api.get("size") else None
    site_gb = round(sizes / GB, 2)
    hist = None
    try:
        out = subprocess.run(["git", "count-objects", "-v"], cwd=ROOT, capture_output=True, text=True).stdout
        kb = sum(int(v) for k, v in (l.split(": ") for l in out.splitlines()) if k in ("size", "size-pack"))
        hist = round(kb * 1024 / GB, 2)
    except Exception:
        pass
    return {
        "site_gb": site_gb, "site_level": level(site_gb / LIMITS["site_gb"]),
        "repo_gb": repo_gb, "repo_level": level((repo_gb or site_gb) / LIMITS["repo_soft_gb"], 0.8, 1.0),
        "history_gb": hist,
        "by_folder": sorted(({"name": k, "mb": round(v / MB, 1)} for k, v in by_top.items()), key=lambda x: -x["mb"])[:10],
        "by_type": sorted(({"name": k, "mb": round(v / MB, 1)} for k, v in by_ext.items()), key=lambda x: -x["mb"]),
        "big_files": sorted(big, key=lambda x: -x["mb"])[:10],
        "files_over_50mb": sum(1 for b in big if b["mb"] >= LIMITS["file_warn_mb"]),
        "limits": LIMITS,
    }


# ── Pages builds + Actions ───────────────────────────────────────────────────
def builds():
    since = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    runs = (_gh(f"repos/{REPO}/actions/runs?per_page=100&created=%3E%3D{since}") or {}).get("workflow_runs", [])
    pages = [r for r in runs if r.get("name") == "pages build and deployment"]
    now = datetime.now(timezone.utc)
    ts = lambda r: datetime.strptime(r["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    per_hour = {}
    for r in pages:
        h = ts(r).strftime("%d %H")
        per_hour[h] = per_hour.get(h, 0) + 1
    peak = max(per_hour.values(), default=0)
    pfail = [r for r in pages if r.get("conclusion") == "failure"]
    last = pages[0] if pages else None
    other = [r for r in runs if r.get("name") != "pages build and deployment"]
    fails = [r for r in other if r.get("conclusion") == "failure"]
    return {
        "pages_24h": len(pages), "pages_peak_hour": peak, "pages_failed_24h": len(pfail),
        "pages_last": last and {"at": ts(last).astimezone(IST).strftime("%d %b %H:%M"), "result": last.get("conclusion") or last.get("status")},
        "pages_level": "red" if (last and last.get("conclusion") == "failure") else
                       "amber" if peak > LIMITS["builds_per_hour"] or pfail else "green",
        "actions_24h": len(other), "actions_failed_24h": len(fails),
        "actions_failed": [{"name": r["name"], "at": ts(r).astimezone(IST).strftime("%d %b %H:%M"), "url": r["html_url"]} for r in fails[:8]],
        "actions_level": "amber" if fails else "green",
        "minutes": "unlimited (public repository)",
    }


# ── Bandwidth estimate ───────────────────────────────────────────────────────
_weight_cache = {}


def page_weight(path):
    """Bytes a first-time visitor downloads from our own site for this page (HTML + local CSS/JS/images it references)."""
    rel = urllib.parse.unquote(path.split("?")[0]).lstrip("/")
    f = ROOT / rel
    if f.is_dir() or not rel:
        f = f / "index.html"
    if not f.exists() and (ROOT / (rel + ".html")).exists():
        f = ROOT / (rel + ".html")
    if not f.exists():
        return None
    if f in _weight_cache:
        return _weight_cache[f]
    html = f.read_text(encoding="utf-8", errors="ignore")
    total = f.stat().st_size
    for ref in set(re.findall(r'(?:src|href)=["\']([^"\'#?]+\.(?:css|js|png|jpe?g|webp|svg|gif))', html)):
        if ref.startswith(("http:", "https:", "//", "data:")):
            continue
        a = (ROOT / ref.lstrip("/")) if ref.startswith("/") else (f.parent / ref)
        try:
            total += a.resolve().stat().st_size
        except Exception:
            pass
    _weight_cache[f] = total
    return total


def bandwidth(analytics):
    if not analytics or not analytics.get("daily"):
        return {"level": "grey", "note": "Connect Google Analytics to estimate bandwidth."}
    views = sum(r["views"] for r in analytics["daily"])
    days = max(1, len(analytics["daily"]))
    tops = analytics.get("pages") or []
    w = [(p["views"], page_weight(p["path"])) for p in tops]
    w = [(v, b) for v, b in w if b]
    avg = sum(v * b for v, b in w) / max(1, sum(v for v, _ in w)) if w else 800 * 1024
    month_gb = views / days * 30 * avg / GB
    return {"views_28d": views, "avg_page_kb": round(avg / 1024), "month_gb": round(month_gb, 2),
            "level": level(month_gb / LIMITS["bandwidth_gb"], 0.5, 0.8),
            "note": "Estimate: page views × page weight (first visit, nothing cached). GitHub does not publish real Pages bandwidth."}


def build(analytics=None):
    out = {"generated_at": datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")}
    for k, fn in (("stock", stock), ("tokens", tokens), ("repo", repo), ("builds", builds)):
        try:
            out[k] = fn()
        except Exception as e:
            print(f"[monitor] {k}: {e}", file=sys.stderr)
            out[k] = None
    try:
        out["bandwidth"] = bandwidth(analytics)
    except Exception as e:
        out["bandwidth"] = {"level": "grey", "note": str(e)[:100]}
    return out


def red_items(m):
    items = []
    for s in m.get("stock") or []:
        if s["level"] == "red":
            items.append(f"Stock: {s['name']} runs out {s['until'] or 'now'}" + (f" — {s['note']}" if s.get("note") else ""))
    for t in m.get("tokens") or []:
        if t["level"] == "red":
            items.append(f"Token: {t['name']} — {t['detail']}")
    r = m.get("repo") or {}
    if r.get("site_level") == "red":
        items.append(f"Pages site size {r['site_gb']} GB (limit 1 GB)")
    if r.get("repo_level") == "red":
        items.append(f"Repository size {r.get('repo_gb')} GB (GitHub recommends under 1 GB)")
    if r.get("files_over_50mb"):
        items.append(f"{r['files_over_50mb']} file(s) over 50 MB (100 MB is the hard limit)")
    b = m.get("builds") or {}
    if b.get("pages_level") == "red":
        items.append("The last GitHub Pages build FAILED — the website is not updating")
    if (m.get("bandwidth") or {}).get("level") == "red":
        items.append(f"Estimated bandwidth {m['bandwidth']['month_gb']} GB/month (soft limit 100 GB)")
    return items


def alert(m):
    """Telegram the owner about red items that were not red at the last check."""
    state_f = ROOT / "admin" / "data" / "monitor_state.json"
    try:
        old = set(json.loads(state_f.read_text(encoding="utf-8")).get("red", []))
    except Exception:
        old = set()
    now = red_items(m)
    key = lambda s: s.split(" — ")[0].split(" runs out")[0].split(" (")[0]
    new = [s for s in now if key(s) not in {key(o) for o in old}]
    state_f.parent.mkdir(parents=True, exist_ok=True)
    state_f.write_text(json.dumps({"checked": m["generated_at"], "red": now}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("SEO_REPORT_CHAT_ID")
    if new and tok and chat:
        text = "🚨 CBSEMock monitor — needs attention:\n\n" + "\n".join("• " + s for s in new) + "\n\nDetails: admin panel → Monitor tab."
        urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage",
                               data=json.dumps({"chat_id": chat, "text": text}).encode(), headers={"Content-Type": "application/json"}), timeout=20)
    print(f"[monitor] red: {len(now)} · new alerts: {len(new)}")


if __name__ == "__main__":
    m = build()
    if sys.argv[1:] == ["alert"]:
        alert(m)
    else:
        print(json.dumps(m, indent=1, ensure_ascii=False))
