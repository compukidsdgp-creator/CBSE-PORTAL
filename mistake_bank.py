"""Mistake Bank reels: review state, owner notifications, posting and the /mistake-bank/ page.

  python3 mistake_bank.py notify <video>...     private Telegram to the owner with each new draft video
  python3 mistake_bank.py post en|hi [--dry-run] post the oldest approved, unposted reel in that language
  python3 mistake_bank.py page                   rebuild mistake-bank/index.html
  python3 mistake_bank.py admin                  JSON for the admin tracker
Approvals: mistake_reels/approvals.json  {"<number>-<id>": {"status": "approved"|"changes", "note": ...}}
Posted:    mistake_reels/posted.json     {"<number>-<id>/<lang>": {"at":..., "ig": id, "fb": id, "ig_link": url}}
"""
import html as H
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import generate_mistake_reel as G

ROOT = Path(__file__).resolve().parent
DIR = ROOT / "mistake_reels"
SITE = "https://cbsemock.org.in"
GH_RAW = f"https://raw.githubusercontent.com/{os.environ.get('GITHUB_REPOSITORY', 'compukidsdgp-creator/CBSE-PORTAL')}/main"
E = H.escape
LANG_NAME = {"en": "English", "hi": "Hindi"}


def jload(name):
    try:
        return json.loads((DIR / name).read_text(encoding="utf-8"))
    except Exception:
        return {}


def jsave(name, d):
    (DIR / name).write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def key(r):
    return f"{r['number']:03d}-{r['id']}"


def state(r, appr=None):
    appr = jload("approvals.json") if appr is None else appr
    a = appr.get(key(r), {})
    have = all(G.video_path(r, l).exists() for l in r["lang"])
    if a.get("status") == "approved":
        return "approved"
    if a.get("status") == "changes":
        return "changes"
    return "draft" if have else "rendering"


def caption(r, lang):
    L = r["lang"][lang]
    beats = {k: c for k, _, c in L["beats"]}
    if lang == "hi":
        head = f"⚠️ Mistake Bank #{r['number']:02d} — {L['title']}"
        body = f"❌ {beats.get('wrong', '')}\n✅ {beats.get('right', '')}\n\n📌 {L['rule'][0]} · {L['rule'][1]}"
        tail = "🔗 पूरी Mistake Bank और चैप्टर नोट्स — link in bio (cbsemock.org.in/go)"
    else:
        head = f"⚠️ Mistake Bank #{r['number']:02d} — {L['title']}"
        body = f"❌ {beats.get('wrong', '')}\n✅ {beats.get('right', '')}\n\n📌 {L['rule'][0]} · {L['rule'][1]}"
        tail = "🔗 Full Mistake Bank + chapter notes — link in bio (cbsemock.org.in/go)"
    cls = r["subject_key"].split("/")[0].replace("class", "Class")
    tags = f"#CBSE #{cls} #BoardExam2027 #MistakeBank #CBSEMock #{L['badge'].split('·')[1].strip().replace(' ', '')}"
    return f"{head}\n\n{body}\n\n{tail}\n\n{tags}"


def notify(paths):
    from tg_photo import send_video
    chat = os.environ.get("SEO_REPORT_CHAT_ID")
    specs = {str(G.video_path(r, l).relative_to(ROOT)): (r, l) for r in G.load_specs() for l in r["lang"]}
    for p in paths:
        rel = str(Path(p).resolve().relative_to(ROOT)) if Path(p).is_absolute() else p
        if rel not in specs:
            continue
        r, l = specs[rel]
        cap = (f"🎬 Mistake Bank #{r['number']:02d} ({LANG_NAME[l]}) ready for review\n{r['lang'][l]['title']}\n\n"
               "Approve or request changes: https://cbsemock.org.in/admin/ → Content tracker → Mistake Bank reels")
        send_video(ROOT / rel, cap, chat=chat)


def post(lang, dry=False):
    import post_formula_reel as P
    appr, posted = jload("approvals.json"), jload("posted.json")
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist)
    if any(k.endswith("/" + lang) and datetime.fromisoformat(v["at"]).astimezone(ist).date() == now.date() for k, v in posted.items()):
        print(f"[mistake] a {lang} reel was already posted today — one per day"); return False
    if os.environ.get("SCHEDULED") == "1":       # GitHub cron can run hours late: never post far outside the slot
        h, m = POST_TIME[lang]
        slot = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if not slot - timedelta(minutes=15) <= now <= slot + timedelta(hours=3):
            print(f"[mistake] scheduled run arrived at {now:%H:%M} IST, outside the {h:02d}:{m:02d} slot — skipped"); return False
    for r in G.load_specs():
        k = f"{key(r)}/{lang}"
        if lang not in r["lang"] or k in posted or state(r, appr) != "approved" or not G.video_path(r, lang).exists():
            continue
        vid, cap = G.video_path(r, lang), caption(r, lang)
        print(f"[mistake] posting {k}\n{cap[:200]}")
        fb = P._upload_video_fb(vid, cap.replace("link in bio (cbsemock.org.in/go)", f"{SITE}/mistake-bank/"), dry_run=dry)
        ig = P._upload_reel_instagram(vid, cap, dry_run=dry)
        tg = False
        if not dry:
            from tg_photo import send_video
            tg = send_video(vid, cap.replace("link in bio (cbsemock.org.in/go)", f"{SITE}/mistake-bank/"))
        if dry:
            return True
        if fb or ig or tg:
            link = ""
            try:
                import urllib.request, urllib.parse
                if ig:
                    q = urllib.parse.urlencode({"fields": "permalink", "access_token": P.IG_TOKEN})
                    link = json.load(urllib.request.urlopen(f"{P.FB_API_BASE}/{ig}?{q}", timeout=20)).get("permalink", "")
            except Exception:
                pass
            posted[k] = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "fb": fb, "ig": ig, "tg": tg, "ig_link": link}
            jsave("posted.json", posted)
            print(f"FB: {fb or 'FAILED'} | IG: {ig or 'FAILED'} | TG: {tg}")
            return True
        print("::warning::all channels failed")
        return False
    print(f"[mistake] nothing approved to post in {lang}")
    return False


POST_TIME = {"en": (17, 31), "hi": (21, 1)}


def schedule():
    """Expected premiere time (IST) of each approved, unposted reel per language: one per day, in order."""
    appr, posted = jload("approvals.json"), jload("posted.json")
    now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    out = {}
    for lang, (h, m) in POST_TIME.items():
        slot = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if slot <= now:
            slot += timedelta(days=1)
        for r in G.load_specs():
            if lang in r["lang"] and state(r, appr) == "approved" and f"{key(r)}/{lang}" not in posted:
                out[f"{key(r)}/{lang}"] = slot
                slot += timedelta(days=1)
    return out


def when(dt):
    today = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()
    day = "today" if dt.date() == today else "tomorrow" if dt.date() == today + timedelta(days=1) else f"{dt:%a} {dt.day} {dt:%b}"
    return f"{day}, {dt.strftime('%I:%M %p').lstrip('0')}"


def page():
    posted, appr, sched = jload("posted.json"), jload("approvals.json"), schedule()
    rows = [r for r in G.load_specs()
            if state(r, appr) == "approved" or any(f"{key(r)}/{l}" in posted for l in r["lang"])]
    cards = ""
    for r in reversed(rows):                 # newest first
        L = r["lang"]["en"]
        beats = {k: c for k, _, c in L["beats"]}
        phones, btns = "", {}
        for l, label in (("hi", "हिंदी"), ("en", "English")):
            if l not in r["lang"]:
                continue
            info = posted.get(f"{key(r)}/{l}", {})
            th = G.thumb_path(r, l)
            img = f'style="background-image:url(../{th.relative_to(ROOT).as_posix()})"' if th.exists() else ""
            if info.get("ig_link"):
                phones += f'<a class="ph {l}" href="{E(info["ig_link"])}" target="_blank" rel="noopener" {img}><i>▶</i><b>{label}</b></a>'
                btns[l] = f'<a class="ig" href="{E(info["ig_link"])}" target="_blank" rel="noopener">▶ Watch in {label}</a>'
            else:
                at = sched.get(f"{key(r)}/{l}")
                phones += f'<span class="ph {l} soon" {img}><b>{label}</b></span>'
                btns[l] = f'<span class="soon">🕒 {label}: {"premieres " + when(at) if at else "coming soon"}</span>'
        btn = btns.get("en", "") + btns.get("hi", "")
        cards += (f'<article class="mb"><div class="stk">{phones}</div><div class="tx">'
                  f'<div class="hd"><span class="n">#{r["number"]:02d}</span><span>{E(L["badge"])}</span></div>'
                  f'<h2>{E(L["title"])}</h2><p class="w">❌ {E(beats.get("wrong", ""))}</p><p class="r">✅ {E(beats.get("right", ""))}</p>'
                  f'<p class="rule">📌 {E(L["rule"][0])} · {E(L["rule"][1])}</p><div class="bt">{btn}'
                  f'<a class="nt" href="../{E(r["notes"])}#mistakes">📒 All mistakes in this chapter</a></div></div></article>')
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mistake Bank — Top CBSE Board Exam Mistakes | CBSEMock</title>
<meta name="description" content="Short reels on the mistakes that cost marks in CBSE board exams: what students write, what to write instead, and the rule to remember. English and Hindi.">
<link rel="canonical" href="{SITE}/mistake-bank/">
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@700&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>
<style>
:root{{--bg:#f3f1ed;--card:#fff;--text:#1a1a1a;--muted:#5d5d5d;--border:#ddd8cc}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0d1117;--card:#161b22;--text:#e6edf3;--muted:#8b949e;--border:#30363d}}}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font:16px/1.6 Inter,system-ui,sans-serif;background:var(--bg);color:var(--text)}}
.hero{{background:linear-gradient(135deg,#7f1d1d,#0f2347 70%);color:#fff;padding:18px 18px 40px}}
.top{{max-width:1000px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}}.top a{{color:#fff;text-decoration:none;font-weight:800}}.top b{{color:#e8cc6a}}
.hin{{max-width:1000px;margin:0 auto;padding-top:20px}}.badge{{display:inline-block;background:#e11d48;padding:6px 14px;border-radius:99px;font-weight:800;font-size:.8rem;letter-spacing:.06em}}
h1{{font-family:'Crimson Pro',serif;font-size:clamp(2rem,5vw,2.8rem);margin:10px 0 6px}}.hin p{{color:rgba(255,255,255,.85);max-width:720px}}
main{{max-width:1000px;margin:-20px auto 0;padding:0 16px 60px;display:grid;grid-template-columns:1fr;gap:16px}}
.mb{{display:grid;grid-template-columns:230px 1fr;gap:18px;align-items:center}}
.stk{{position:relative;height:240px}}
.ph{{position:absolute;top:8px;width:118px;height:210px;border-radius:18px;border:5px solid #0b0f1a;background:#111 center/cover no-repeat;box-shadow:0 14px 26px rgba(0,0,0,.35);text-decoration:none;transition:transform .35s}}
.ph.hi{{left:92px;transform:rotate(8deg)}}.ph.en{{left:8px;transform:rotate(-6deg);z-index:2}}
.stk:hover .ph.en{{transform:rotate(-10deg) translateX(-6px)}}.stk:hover .ph.hi{{transform:rotate(12deg) translateX(8px)}}
.ph i{{position:absolute;left:50%;top:50%;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;background:rgba(255,255,255,.92);color:#e11d48;font-style:normal;display:flex;align-items:center;justify-content:center;padding-left:3px}}
.ph b{{position:absolute;left:8px;bottom:8px;background:#ffd23f;color:#0f2347;font-size:.72rem;padding:3px 8px;border-radius:99px}}
.ph.soon::after{{content:"SOON";position:absolute;right:6px;top:8px;background:#e11d48;color:#fff;font:800 .62rem Inter;padding:2px 6px;border-radius:6px}}
.bt .soon{{display:inline-flex;align-items:center;min-height:40px;padding:8px 14px;border-radius:99px;background:rgba(225,29,72,.1);color:#be123c;font-weight:700;font-size:.85rem}}
@media(max-width:620px){{.mb{{grid-template-columns:1fr}}.stk{{width:230px;margin:0 auto}}}}
.mb{{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:18px;box-shadow:0 8px 20px rgba(0,0,0,.06)}}
.hd{{display:flex;gap:10px;align-items:center;font-size:.8rem;color:var(--muted);font-weight:600}}.n{{background:#e11d48;color:#fff;border-radius:8px;padding:2px 8px;font-weight:800}}
.mb h2{{font-family:'Crimson Pro',serif;font-size:1.4rem;margin:8px 0}}.w{{color:#b91c1c}}.r{{color:#15803d;font-weight:600}}.rule{{font-size:.9rem;color:var(--muted);margin-top:6px}}
.bt{{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}}.bt a{{display:inline-flex;align-items:center;min-height:40px;padding:8px 14px;border-radius:99px;text-decoration:none;font-weight:700;font-size:.85rem}}
.ig{{background:linear-gradient(135deg,#e11d48,#7c3aed);color:#fff}}.nt{{background:#0f2347;color:#ffe4a0}}
.empty{{grid-column:1/-1;background:var(--card);border-radius:18px;padding:24px;text-align:center}}
footer{{text-align:center;padding:24px;font-size:.8rem;color:var(--muted)}}footer a{{color:inherit}}
</style></head><body>
<header class="hero"><div class="top"><a href="../index.html">CBSE<b>Mock</b></a><a href="../learn/">📘 Learn</a></div>
<div class="hin"><span class="badge">⚠ MISTAKE BANK</span><h1>Top board exam mistakes — fixed in 20 seconds</h1>
<p>Each reel shows what students write, why it loses marks, and what to write instead. New reels in English and Hindi.</p></div></header>
<main>{cards or '<div class="empty">The first Mistake Bank reels arrive soon.</div>'}</main>
<footer>&copy; 2026 CBSEMock.org.in · <a href="../about.html">About Us</a> · <a href="../privacy.html">Privacy Policy</a></footer>
</body></html>"""
    (ROOT / "mistake-bank").mkdir(exist_ok=True)
    (ROOT / "mistake-bank" / "index.html").write_text(doc, encoding="utf-8")
    print(f"[mistake] page: {len(rows)} reel(s)")


def admin():
    appr, posted = jload("approvals.json"), jload("posted.json")
    items = []
    for r in G.load_specs():
        st = state(r, appr)
        items.append({"id": key(r), "number": r["number"], "title": r["lang"]["en"]["title"], "badge": r["lang"]["en"]["badge"],
                      "state": st, "note": appr.get(key(r), {}).get("note", ""),
                      "videos": {l: f"{GH_RAW}/{G.video_path(r, l).relative_to(ROOT).as_posix()}" for l in r["lang"] if G.video_path(r, l).exists()},
                      "posted": [l for l in r["lang"] if f"{key(r)}/{l}" in posted]})
    return {"items": items}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "page"
    if cmd == "notify":
        notify(sys.argv[2:])
    elif cmd == "post":
        ok = post(sys.argv[2], "--dry-run" in sys.argv)
        page()
    elif cmd == "admin":
        print(json.dumps(admin(), indent=1, ensure_ascii=False))
    else:
        page()
