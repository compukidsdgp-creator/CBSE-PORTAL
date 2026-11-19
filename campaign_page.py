"""60-Day Board Plan on the website: the page board-plan/index.html and the home-page strip
(<!-- BOARDPLAN-STRIP:START/END -->, just above the Mistake Bank strip). Idempotent; run after every post/render.
    python3 campaign_page.py
"""
import html as H
import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import generate_hack_reel as G

ROOT = Path(__file__).resolve().parent
SITE = "https://cbsemock.org.in"
IST = timezone(timedelta(hours=5, minutes=30))
A, B = "<!-- BOARDPLAN-STRIP:START -->", "<!-- BOARDPLAN-STRIP:END -->"
E = H.escape
EXAM = "2027-02-16"
COL = {"90+ Score Hack": "#ffd23f", "Board FAQ": "#5eead4", "Beat the Timer": "#ff7a45", "Mistake Fix": "#ff5470",
       "Exam Rescue": "#a78bfa"}
ICON = {"free-mock-papers/": "📄 Free mock papers", "mock-zone/": "📝 Mock Zone", "study-zone/": "📚 Study Zone",
        "formula-board/": "🧮 Formula Board", "mistake-bank/": "⚠️ Mistake Bank", "weekly-focus/": "🎯 Weekly Focus"}


def jload(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return {}


def state():
    plan = jload(G.BASE / "plan.json").get("reels", [])
    posted = jload(G.BASE / "posted.json")
    specs = {r["n"]: r for r in G.load_specs()}
    today = datetime.now(IST).date()
    rows = []
    for p in plan:
        r = specs.get(p["n"])
        live = {l: bool(r and f"{r['n']:02d}-{r['id']}" + ("" if l == "en" else f"/{l}") in posted) for l in ("en", "hi")}
        rows.append({**p, "spec": r, "live": live, "d": date.fromisoformat(p["date"])})
    done = [x for x in rows if x["live"]["en"] or x["live"]["hi"]]
    cur = done[-1] if done else rows[0]
    upcoming = [x for x in rows if x["d"] > cur["d"]][:4]
    return rows, done, cur, upcoming, today


def dest_label(d):
    if d in ICON:
        return ICON[d]
    m = re.match(r"cbse-class-(\d+)-(.+?)-(mock-papers|mock-tests|practice-papers)\.html", d)
    if m:
        return f"📝 Class {m.group(1)} {m.group(2).replace('-', ' ').title()} mock papers"
    return "📚 Practise on CBSEMock"


def fmt(d):
    return d.strftime("%a %-d %b")


# ── home strip ───────────────────────────────────────────────────────────────
def strip():
    rows, done, cur, upcoming, today = state()
    r = cur["spec"]
    started = bool(done)
    thumb = G.thumb_path(r).relative_to(ROOT).as_posix() if r and G.thumb_path(r).exists() else ""
    when = "TODAY" if cur["d"] == today else ("STARTS " + fmt(cur["d"]).upper() if not started else fmt(cur["d"]).upper())
    nxt = "".join(f'<div class="bp-t" style="--c:{COL[x["pillar"]]}"><small>{fmt(x["d"])}</small><b>{E(x["topic"])}</b>'
                  f'<i>{E(x["pillar"])}</i></div>' for x in upcoming)
    head = (f"{'TODAY' if cur['d'] == today else 'LATEST'} · {cur['pillar'].upper()}" if started
            else f"STARTS {fmt(cur['d']).upper()} · 1 PM")
    day_txt = f"Day {cur['n']} of {len(rows)}" if started else f"{len(rows)} reels · starts {fmt(rows[0]['d'])}"
    pct = 100 * (len(done) / len(rows)) if rows else 0
    return f"""{A}
<style>
.bp{{max-width:1100px;margin:26px auto 10px;padding:0 20px}}
.bp-box{{border-radius:22px;padding:24px 26px;color:#fff;background:radial-gradient(600px 300px at 15% 0%,rgba(94,234,212,.18),transparent 60%),linear-gradient(135deg,#071426,#0f2347 60%,#14325f);
 border:2px solid #5eead4;box-shadow:0 10px 26px rgba(15,35,71,.25);display:grid;grid-template-columns:230px 1fr;gap:26px;align-items:center}}
.bp-ph{{position:relative;display:block;width:210px;height:373px;border-radius:26px;padding:7px;background:#0b0f1a;box-shadow:0 22px 40px rgba(0,0,0,.5),0 0 0 2px rgba(255,255,255,.18) inset;
 transform:perspective(900px) rotateY(10deg) rotateX(4deg);transition:transform .35s;text-decoration:none}}
.bp-ph:hover,.bp-ph:focus-visible{{transform:none}}
.bp-ph .sc{{position:absolute;inset:7px;border-radius:20px;background:#111 center/cover no-repeat}}
.bp-ph .pl{{position:absolute;left:50%;top:50%;width:62px;height:62px;margin:-31px 0 0 -31px;border-radius:50%;background:rgba(255,255,255,.92);color:#0f766e;display:flex;align-items:center;justify-content:center;font-size:26px;padding-left:4px}}
.bp-ph .lv{{position:absolute;left:14px;bottom:16px;background:#e11d48;color:#fff;font:800 .7rem Inter,sans-serif;letter-spacing:.08em;padding:5px 10px;border-radius:99px}}
.bp-lang{{display:flex;gap:6px;margin-top:12px;justify-content:center}}
.bp-lang a{{font:800 .76rem Inter,sans-serif;padding:8px 13px;border-radius:99px;border:1.5px solid rgba(255,255,255,.3);color:#fff;text-decoration:none;min-height:36px}}
.bp-lang a:first-child{{background:#5eead4;color:#062a26;border-color:#5eead4}}
.bp-tag{{display:inline-flex;gap:8px;align-items:center;font:800 .74rem Inter,sans-serif;letter-spacing:.1em;color:#062a26;background:#5eead4;padding:6px 12px;border-radius:99px}}
.bp h2{{font-family:'Crimson Pro',serif;font-size:clamp(1.5rem,3vw,2rem);line-height:1.15;margin:10px 0 4px;color:#fff}}
.bp p{{color:rgba(255,255,255,.84);font-size:.92rem;margin:0 0 12px}}
.bp-bar{{display:flex;align-items:center;gap:12px;font:700 .82rem Inter,sans-serif;color:#a7f3e8;margin:4px 0 16px;flex-wrap:wrap}}
.bp-bar div{{flex:1 1 120px;height:10px;border-radius:10px;background:rgba(255,255,255,.12);overflow:hidden}}
.bp-bar i{{display:block;height:100%;width:{pct:.1f}%;min-width:10px;background:linear-gradient(90deg,#5eead4,#ffd23f)}}
.bp-now{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.15);border-radius:16px;padding:12px 14px;margin-bottom:14px}}
.bp-now small{{color:#ffd23f;font:800 .72rem Inter,sans-serif;letter-spacing:.08em}}.bp-now b{{display:block;font-size:1.05rem;margin-top:2px}}
.bp-up{{font:800 .72rem Inter,sans-serif;letter-spacing:.1em;color:rgba(255,255,255,.6);margin-bottom:8px}}
.bp-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px}}
.bp-t{{border-radius:14px;padding:10px 12px;background:rgba(255,255,255,.05);border-left:4px solid var(--c)}}.bp-t small{{font:700 .72rem Inter,sans-serif;color:rgba(255,255,255,.65)}}
.bp-t b{{display:block;font-size:.86rem;line-height:1.25;margin:3px 0}}.bp-t i{{font-style:normal;font:800 .64rem Inter,sans-serif;letter-spacing:.06em;color:var(--c);text-transform:uppercase}}
.bp-cta{{display:inline-flex;min-height:44px;align-items:center;padding:10px 20px;border-radius:99px;background:#ffd23f;color:#0f2347;font-weight:800;font-size:.82rem;text-decoration:none;box-shadow:0 5px 0 #8a6d00;transition:transform .15s,box-shadow .15s}}
.bp-cta:active{{transform:translateY(4px);box-shadow:0 1px 0 #8a6d00}}
@media(max-width:760px){{.bp{{padding:0 14px}}.bp-box{{grid-template-columns:1fr;padding:20px}}.bp-ph{{margin:0 auto;width:180px;height:320px}}.bp-row{{grid-template-columns:1fr 1fr}}.bp-cta{{width:100%;justify-content:center}}}}
@media(prefers-reduced-motion:reduce){{.bp-ph{{transform:none;transition:none}}}}
</style>
<section class="bp" aria-label="60-Day Board Plan reels"><div class="bp-box">
<div><a class="bp-ph" href="board-plan/#day{cur['n']:02d}" aria-label="Watch: {E(cur['topic'])}"><span class="sc"{f' style="background-image:url({thumb})"' if thumb else ''}></span><span class="pl" aria-hidden="true">▶</span><span class="lv">{E(when)}</span></a>
<div class="bp-lang"><a href="board-plan/#day{cur['n']:02d}">English</a><a href="board-plan/?lang=hi#day{cur['n']:02d}" lang="hi">हिंदी</a></div></div>
<div><span class="bp-tag">📅 60-DAY BOARD PLAN</span>
<h2>One 20-second exam hack every weekday</h2>
<p>Answer-writing, revision and exam-day strategy for Class 10 &amp; 12 — a new reel at 1 PM, in Hindi at 7:30 PM, until the boards.</p>
<div class="bp-bar"><span>{day_txt}</span><div><i></i></div><span class="bp-cd" data-exam="{EXAM}"></span></div>
<div class="bp-now"><small>{E(head)}</small><b>{E(cur['topic'])}: {E(cur['hook'])}</b></div>
{f'<div class="bp-up">COMING UP</div><div class="bp-row">{nxt}</div>' if nxt else ''}
<a class="bp-cta" href="board-plan/">WATCH THE FULL PLAN →</a></div>
</div></section>
<script>(function(){{var e=document.querySelector('.bp-cd');if(!e)return;var d=Math.ceil((new Date(e.dataset.exam+'T00:00:00+05:30')-Date.now())/864e5);e.textContent=d>0?'Boards in '+d+' days':'Boards are on — all the best!';}})();</script>
{B}"""


def home():
    f = ROOT / "index.html"
    s = f.read_text(encoding="utf-8")
    o = s
    s = re.sub(re.escape(A) + r".*?" + re.escape(B) + r"\n\n", "", s, flags=re.S)
    anchor = "<!-- MISTAKE-STRIP:START -->" if "<!-- MISTAKE-STRIP:START -->" in s else "<!-- LEARN-STRIP:START -->"
    if anchor in s:
        s = s.replace(anchor, strip() + "\n\n" + anchor, 1)
    if s != o:
        f.write_text(s, encoding="utf-8")
    print(f"[board-plan] home {'updated' if s != o else 'unchanged'}")


# ── the page ─────────────────────────────────────────────────────────────────
def page():
    rows, done, cur, upcoming, today = state()
    cards = ""
    for x in reversed(done):
        r = x["spec"]
        live = x["live"]
        col = COL[x["pillar"]]
        vids = ""
        for l in ("en", "hi"):
            if live[l] and G.video_path(r, l).exists():
                th = G.thumb_path(r, l)
                vids += (f'<video class="v v-{l}" controls preload="none" playsinline '
                         f'{f"poster=../{th.relative_to(ROOT).as_posix()}" if th.exists() else ""} '
                         f'src="../{G.video_path(r, l).relative_to(ROOT).as_posix()}"></video>')
        tabs = "".join(f'<button type="button" data-l="{l}"{" lang=hi" if l == "hi" else ""}>{label}</button>'
                       for l, label in (("en", "English"), ("hi", "हिंदी")) if live[l])
        cards += (f'<article class="rc" id="day{x["n"]:02d}" data-p="{E(x["pillar"])}" style="--c:{col}">'
                  f'<div class="vw">{vids}</div><div class="tx"><div class="hd"><span class="n">#{x["n"]:02d}</span>'
                  f'<span class="pl">{E(x["pillar"])}</span><span class="dt">{fmt(x["d"])}</span></div>'
                  f'<h2>{E(x["topic"])}</h2><p class="hk">“{E(x["hook"])}”</p><p>{E(x["brief"])}</p>'
                  f'<div class="lg">{tabs}</div><a class="go" href="../{E(x["dest"])}">{E(dest_label(x["dest"]))} →</a></div></article>')
    later = [x for x in rows if not (x["live"]["en"] or x["live"]["hi"])]
    if not done:
        cards += ('<div class="first">🎬 The first reel premieres <b>' + fmt(rows[0]["d"]) +
                  ' at 1 PM</b> (Hindi at 7:30 PM). Every reel will appear here to watch, with a link to practise.</div>')
    if later:
        cards += '<section class="up" aria-label="Coming up"><h3>Coming up</h3>' + "".join(
            f'<div class="ur" id="day{x["n"]:02d}" data-p="{E(x["pillar"])}" style="--c:{COL[x["pillar"]]}"><span class="ud">{fmt(x["d"])}</span>'
            f'<span class="ut"><b>{E(x["topic"])}</b><i>{E(x["pillar"])}</i></span><span aria-hidden="true">🔒</span></div>' for x in later[:5])
        if len(later) > 5:
            cards += f'<p class="more">+ {len(later) - 5} more reels until {fmt(rows[-1]["d"])}, then the boards.</p>'
        cards += '</section>'
    pills = "".join(f'<button type="button" data-f="{E(p)}" style="--c:{c}">{E(p)}</button>' for p, c in COL.items())
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>60-Day Board Plan — Daily CBSE Exam Hacks (Reels) | CBSEMock</title>
<meta name="description" content="One 20-second CBSE board-exam hack every weekday until the 2027 boards: step marking, answer presentation, revision methods, time management and exam-day strategy. English and Hindi.">
<link rel="canonical" href="{SITE}/board-plan/">
<meta property="og:title" content="60-Day Board Plan — Daily CBSE Exam Hacks"><meta property="og:url" content="{SITE}/board-plan/">
<meta property="og:description" content="A 20-second board-exam hack every weekday until the boards. English + Hindi."><meta property="og:image" content="{SITE}/og-image.jpg">
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@700&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2810600896966939" crossorigin="anonymous"></script>
<style>
:root{{--bg:#f3f1ed;--card:#fff;--text:#16181d;--muted:#5d6472;--border:#ddd8cc}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0d1117;--card:#161b22;--text:#e6edf3;--muted:#8b949e;--border:#30363d}}}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font:16px/1.6 Inter,system-ui,sans-serif;background:var(--bg);color:var(--text)}}
.hero{{background:radial-gradient(600px 300px at 15% 0%,rgba(94,234,212,.2),transparent 60%),linear-gradient(135deg,#071426,#0f2347 60%,#14325f);color:#fff;padding:18px 16px 46px}}
.top{{max-width:1000px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}}.top a{{color:#fff;text-decoration:none;font-weight:800}}.top b{{color:#e8cc6a}}
.hin{{max-width:1000px;margin:0 auto;padding-top:22px}}.tag{{display:inline-block;background:#5eead4;color:#062a26;padding:6px 14px;border-radius:99px;font-weight:800;font-size:.78rem;letter-spacing:.08em}}
h1{{font-family:'Crimson Pro',serif;font-size:clamp(2rem,5vw,2.8rem);line-height:1.1;margin:12px 0 8px}}.hin p{{color:rgba(255,255,255,.86);max-width:720px}}
.bar{{display:flex;gap:12px;align-items:center;margin-top:16px;font-weight:700;font-size:.85rem;color:#a7f3e8;flex-wrap:wrap}}.bar div{{flex:1 1 140px;height:10px;border-radius:10px;background:rgba(255,255,255,.14);overflow:hidden}}
.bar i{{display:block;height:100%;width:{100 * len(done) / max(1, len(rows)):.1f}%;min-width:10px;background:linear-gradient(90deg,#5eead4,#ffd23f)}}
.fl{{max-width:1000px;margin:-22px auto 14px;padding:0 16px;display:flex;gap:8px;overflow-x:auto;scrollbar-width:none}}
.fl button{{flex:0 0 auto;font:800 .78rem Inter,sans-serif;padding:9px 14px;min-height:40px;border-radius:99px;border:2px solid var(--c,#0f2347);background:var(--card);color:var(--text);cursor:pointer}}
.fl button.on{{background:var(--c,#0f2347);color:#071426}}.fl button[data-f=all]{{--c:#0f2347}}.fl button[data-f=all].on{{color:#fff}}
main{{max-width:1000px;margin:0 auto;padding:0 16px 60px;display:grid;gap:16px}}
.rc{{display:grid;grid-template-columns:220px 1fr;gap:20px;background:var(--card);border:1px solid var(--border);border-left:6px solid var(--c);border-radius:18px;padding:16px;box-shadow:0 8px 20px rgba(0,0,0,.06);scroll-margin-top:16px}}
.vw video{{width:100%;aspect-ratio:9/16;border-radius:14px;background:#000;display:block}}
.hd{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:.8rem;color:var(--muted);font-weight:700}}.n{{background:#0f2347;color:#fff;border-radius:8px;padding:2px 8px}}
.pl{{color:var(--c);filter:brightness(.8);text-transform:uppercase;letter-spacing:.05em}}
.rc h2{{font-family:'Crimson Pro',serif;font-size:1.45rem;line-height:1.2;margin:8px 0 4px}}.hk{{font-weight:700;margin-bottom:6px}}.rc p{{font-size:.94rem}}
.lg{{display:flex;gap:8px;margin:12px 0 10px}}.lg button{{font:800 .8rem Inter,sans-serif;padding:8px 14px;min-height:40px;border-radius:99px;border:2px solid var(--border);background:transparent;color:var(--text);cursor:pointer}}
.lg button.on{{background:#0f2347;color:#fff;border-color:#0f2347}}
.go{{display:inline-flex;align-items:center;min-height:44px;padding:10px 16px;border-radius:99px;background:#ffd23f;color:#0f2347;font-weight:800;font-size:.86rem;text-decoration:none;box-shadow:0 4px 0 #8a6d00}}
.first{{background:var(--card);border:1px dashed var(--border);border-radius:18px;padding:20px;text-align:center}}
.up{{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:16px}}.up h3{{font-family:'Crimson Pro',serif;font-size:1.3rem;margin-bottom:8px}}
.ur{{display:flex;align-items:center;gap:14px;padding:10px 4px;border-bottom:1px solid var(--border);border-left:4px solid var(--c);padding-left:12px;margin-bottom:6px}}
.ud{{flex:0 0 92px;font-weight:800;font-size:.82rem;color:var(--muted)}}.ut{{flex:1}}.ut b{{display:block;font-size:.95rem}}.ut i{{font-style:normal;font-size:.72rem;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--c);filter:brightness(.8)}}
.more{{font-size:.85rem;color:var(--muted);margin-top:8px}}
@media(max-width:640px){{.rc{{grid-template-columns:1fr}}.vw{{max-width:280px;margin:0 auto}}}}
footer{{text-align:center;padding:24px;font-size:.8rem;color:var(--muted)}}footer a{{color:inherit}}
</style></head><body>
<header class="hero"><div class="top"><a href="../index.html">CBSE<b>Mock</b></a><a href="../mistake-bank/">⚠️ Mistake Bank</a></div>
<div class="hin"><span class="tag">📅 60-DAY BOARD PLAN</span><h1>One 20-second exam hack every weekday</h1>
<p>Step marking, answer presentation, revision methods, time management and exam-day strategy for CBSE Class 10 &amp; 12 — a new reel every weekday at 1 PM (Hindi at 7:30 PM) until the 2027 boards. Watch, then practise on the linked page.</p>
<div class="bar"><span>{len(done)} of {len(rows)} reels out</span><div><i></i></div><span id="cd"></span></div></div></header>
<div class="fl" id="fl"><button type="button" class="on" data-f="all">All</button>{pills}</div>
<main id="list">{cards}</main>
<footer><a href="../index.html">Home</a> · <a href="../free-mock-papers/">Free mock papers</a> · <a href="../mistake-bank/">Mistake Bank</a> · <a href="../learn/">Learn</a></footer>
<script>
(function(){{
 var d=Math.ceil((new Date('{EXAM}T00:00:00+05:30')-Date.now())/864e5);document.getElementById('cd').textContent=d>0?'Boards in '+d+' days':'Boards are on — all the best!';
 var pref=(new URLSearchParams(location.search).get('lang')==='hi')?'hi':'en';
 document.querySelectorAll('.rc').forEach(function(c){{var bs=c.querySelectorAll('.lg button');if(!bs.length)return;
  function show(l){{if(!c.querySelector('.v-'+l))l=bs[0].dataset.l;c.querySelectorAll('video').forEach(function(v){{var on=v.classList.contains('v-'+l);v.style.display=on?'block':'none';if(!on)v.pause();}});
   bs.forEach(function(b){{b.classList.toggle('on',b.dataset.l===l);}});}}
  bs.forEach(function(b){{b.addEventListener('click',function(){{show(b.dataset.l);}});}});show(pref);}});
 var fl=document.getElementById('fl');fl.addEventListener('click',function(e){{var b=e.target.closest('button');if(!b)return;
  [].forEach.call(fl.children,function(x){{x.classList.toggle('on',x===b);}});
  document.querySelectorAll('.rc,.ur').forEach(function(c){{c.hidden=!(b.dataset.f==='all'||c.dataset.p===b.dataset.f);}});}});
 document.querySelectorAll('video').forEach(function(v){{v.addEventListener('play',function(){{try{{gtag('event','board_plan_play',{{item_id:v.closest('.rc').id}})}}catch(x){{}}}},{{once:true}});}});
}})();
</script>
</body></html>"""
    out = ROOT / "board-plan" / "index.html"
    out.parent.mkdir(exist_ok=True)
    old = out.read_text(encoding="utf-8") if out.exists() else ""
    if doc != old:
        out.write_text(doc, encoding="utf-8")
    print(f"[board-plan] page {'updated' if doc != old else 'unchanged'} ({len(done)} live, {len(rows)} planned)")


if __name__ == "__main__":
    page()
    home()
