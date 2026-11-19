#!/usr/bin/env python3
"""
fetch_news.py — the CBSE Newsroom page (news.html) for cbsemock.org.in.  LAYOUT LOCKED (approved 19 Nov 2026).

Pulls CBSE headlines from Google News RSS and renders the "CBSE Newsroom": masthead with board-exam countdown,
category tabs, red LATEST ticker, a Top Story card, a corkboard Bulletin Board (notes from news_bulletin.json),
a filterable Latest-updates grid, 3D buttons to the major zones, official sources and Telegram alerts.

Runs daily at 9:30 AM IST from .github/workflows/portal-automation.yml.
    python3 fetch_news.py                 fetch live and write news.html
    python3 fetch_news.py --from FILE     render from saved items (JSON list of {title, link, pub, source})
"""
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(ROOT, "news.html")
BULLETIN = os.path.join(ROOT, "news_bulletin.json")
IST = timezone(timedelta(hours=5, minutes=30))
E = html.escape

QUERIES = [
    "CBSE date sheet 2027",
    "CBSE board exam 2027",
    "CBSE circular 2026",
    "CBSE syllabus 2026-27",
    "CBSE admit card 2027",
    "CBSE practical exam 2027",
    "CBSE sample paper 2027",
]
PER_QUERY = 8
MAX_ITEMS = 18
MIN_ITEMS = 4          # fewer than this = feed failure; keep the existing page

# category: (label, colour, keywords) — first match wins
CATS = [
    ("datesheet", "Date Sheet", "#e11d48", r"date ?sheet|time ?table|exam dates?|schedule"),
    ("results", "Results", "#16a34a", r"\bresults?\b|toppers?|pass percentage|marksheet|re-?evaluation"),
    ("syllabus", "Syllabus", "#7c3aed", r"syllabus|curriculum|deleted|rationali[sz]ed|scheme of studies|ncert"),
    ("prep", "Exam Prep", "#0891b2", r"mcqs?|sample papers?|questions?|practice|mock|preparation|tips|study plan|pyqs?|marking scheme"),
    ("circulars", "Circulars", "#c2410c", r".*"),
]
CAT_INFO = {k: (lbl, col) for k, lbl, col, _ in CATS}

BUTTONS = [  # icon, title, subtitle, href, colour top, colour bottom
    ("📝", "Mock Zone", "Full papers · solutions", "mock-zone/", "#1d4ed8", "#0b2a6b"),
    ("📚", "Study Zone", "Notes · chapter quizzes", "study-zone/", "#0f766e", "#053b36"),
    ("🔬", "Virtual Labs", "Interactive experiments", "virtual-labs/", "#7c3aed", "#3b1878"),
    ("⚡", "Weekly Booster", "New every Monday", "booster/", "#c9a227", "#6b5200"),
    ("⚠️", "Mistake Bank", "Top board mistakes", "mistake-bank/", "#e11d48", "#7a0a26"),
    ("📐", "Formula Board", "All formulas", "formula-board/", "#0891b2", "#064a5c"),
]
SUBJECTS = r"english|physics|chemistry|biology|maths?|mathematics|science|social science|history|geography|economics|" \
           r"accountancy|business studies|computer science|political science|hindi|sanskrit|psychology|sociology|" \
           r"informatics practices|physical education|applied maths|artificial intelligence"


# ── Fetch ─────────────────────────────────────────────────────────────────────
def clean_title(title, source):
    t = title.strip()
    if source and t.endswith(" - " + source):
        t = t[: -len(source) - 3]
    t = re.sub(r"\s+[-–—|]\s*$", "", t)           # stray trailing dash
    return re.sub(r"\s+", " ", t).strip()


def fetch_items(query):
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (cbsemock news bot)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            tree = ET.parse(r)
    except Exception as e:
        print(f"  [skip] {query}: {e}")
        return []
    out = []
    for item in tree.findall(".//item")[:PER_QUERY]:
        src_el = item.find("source")
        if src_el is None:
            src_el = item.find("{https://news.google.com/rss}source")
        source = (src_el.text or "").strip() if src_el is not None else ""
        raw = item.findtext("title", "")
        if not source and " - " in raw:
            source = raw.rsplit(" - ", 1)[1].strip()
        out.append({"title": clean_title(raw, source), "link": item.findtext("link", "").strip(),
                    "pub": item.findtext("pubDate", "").strip(), "source": source or "News"})
    return out


# ── Prepare ───────────────────────────────────────────────────────────────────
def when(item):
    try:
        return parsedate_to_datetime(item["pub"]).astimezone(IST)
    except Exception:
        return None


def categorise(title):
    low = title.lower()
    for k, _, _, rx in CATS:
        if re.search(rx, low):
            return k
    return "circulars"


def klass(title):
    low = title.lower()
    c10 = bool(re.search(r"class\s*(10|x)\b|10th", low))
    c12 = bool(re.search(r"class\s*(12|xii)\b|12th", low))
    return "both" if c10 == c12 else ("10" if c10 else "12")


def prepare(raw, now):
    """Drop stale/irrelevant items, de-duplicate, cap near-identical series (e.g. 'Top 50 MCQs for <subject>')."""
    seen, series, out = set(), {}, []
    raw = [r for r in raw if r.get("title") and "cbse" in r["title"].lower()]
    raw.sort(key=lambda r: when(r) or datetime(2000, 1, 1, tzinfo=IST), reverse=True)
    for r in raw:
        d = when(r)
        if d and (now - d).days > 45:
            continue
        key = re.sub(r"[^a-z0-9 ]", "", r["title"].lower())[:70]
        if key in seen:
            continue
        seen.add(key)
        sk = re.sub(SUBJECTS, "#", r["title"].lower())
        sk = re.sub(r"[^a-z# ]", "", sk)[:60]
        if series.get(sk, 0) >= 2:
            continue
        series[sk] = series.get(sk, 0) + 1
        r = dict(r, cat=categorise(r["title"]), cls=klass(r["title"]), dt=d)
        out.append(r)
        if len(out) >= MAX_ITEMS:
            break
    return out


def pick_top(items, now):
    """Most recent date-sheet / results / circular story from the last 10 days; otherwise the newest item."""
    for cat in ("datesheet", "results", "circulars"):
        for it in items:
            if it["cat"] == cat and it["dt"] and (now - it["dt"]).days <= 10:
                return it
    return items[0]


def ago(d, now):
    if not d:
        return ""
    s = (now - d).total_seconds()
    if s < 3600:
        return f"{max(1, int(s // 60))} min ago"
    if s < 86400:
        h = int(s // 3600)
        return f"{h} hour{'s' if h > 1 else ''} ago"
    days = int(s // 86400)
    if days < 7:
        return "Yesterday" if days == 1 else f"{days} days ago"
    return d.strftime("%-d %b %Y")


def bulletin(today):
    try:
        cfg = json.load(open(BULLETIN, encoding="utf-8"))
    except Exception:
        cfg = {"notes": []}
    notes = [n for n in cfg.get("notes", []) if not n.get("until") or date.fromisoformat(n["until"]) >= today]
    try:
        sys.path.insert(0, ROOT)
        import booster_plan as BP
        first = BP.FIRST_MONDAY
        txt = (f"Starts Monday {first.day} {first.strftime('%b')} · 50+ questions per subject" if today < first
               else "A fresh set every Monday · 50+ questions per subject")
        notes.insert(1, {"title": "⚡ Weekly Knowledge Booster", "text": txt, "link": "booster/"})
    except Exception as e:
        print("  [bulletin] booster note skipped:", e)
    exam = date.fromisoformat(cfg.get("exam_date", "2027-02-16"))
    return notes[:4], exam


# ── Render ────────────────────────────────────────────────────────────────────
DEKS = {
    "datesheet": "Board exams begin on {exam}. Check the subject-wise schedule and plan your revision around it.",
    "results": "Check what's new on CBSE results and what it means for Class 10 and 12 students.",
    "syllabus": "What's changed in the CBSE syllabus and what it means for your preparation this year.",
    "prep": "Practise with these questions now — board exams begin on {exam}.",
    "circulars": "The latest from CBSE for Class 10 and 12 students and schools.",
}


def ext(link):
    return ' target="_blank" rel="noopener"' if link.startswith("http") else ""


def card(it, now):
    lbl, col = CAT_INFO[it["cat"]]
    src = E(it["source"])
    return (f'<a class="nc" href="{E(it["link"])}" target="_blank" rel="noopener nofollow" data-cat="{it["cat"]}" data-cls="{it["cls"]}">'
            f'<span class="chip" style="--c:{col}">{lbl.upper()}</span><h3>{E(it["title"])}</h3>'
            f'<div class="mt"><span><b>{src}</b> · {E(ago(it["dt"], now))}</span><span class="rd">Read ↗</span></div></a>')


def build_html(items, now):
    today = now.date()
    top = pick_top(items, now)
    rest = [i for i in items if i is not top]
    notes, exam = bulletin(today)
    days = max(0, (exam - today).days)
    tlbl, tcol = CAT_INFO[top["cat"]]
    used = [k for k, *_ in CATS if any(i["cat"] == k for i in items)]
    tabs = '<button class="on" data-f="all">Top News</button>' + "".join(
        f'<button data-f="{k}">{CAT_INFO[k][0]}</button>' for k in used)
    tick = "".join(f'<span><b style="color:{CAT_INFO[i["cat"]][1]}">●</b> {E(i["title"])}</span>' for i in items[:8])
    cards = "\n".join(card(i, now) for i in rest)
    notes_html = "".join(
        (f'<a class="nt" href="{E(n["link"])}"{ext(n["link"])}>' if n.get("link") else '<div class="nt">')
        + f'<b>{E(n["title"])}</b>{E(n.get("text", ""))}' + ("</a>" if n.get("link") else "</div>") for n in notes)
    b3 = "".join(f'<a class="b3" href="{h}" style="--a:{a};--b:{b}"><span class="ic" aria-hidden="true">{ic}</span>'
                 f'<span class="tx"><b>{t}</b><small>{s}</small></span><span class="ar" aria-hidden="true">→</span></a>'
                 for ic, t, s, h, a, b in BUTTONS)
    ld = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "CBSE Newsroom — Board Exam News & Updates",
                     "url": "https://cbsemock.org.in/news.html", "dateModified": now.isoformat(timespec="minutes"),
                     "isPartOf": {"@type": "WebSite", "name": "CBSEMock", "url": "https://cbsemock.org.in/"},
                     "mainEntity": {"@type": "ItemList", "itemListElement": [
                         {"@type": "ListItem", "position": n + 1, "name": i["title"], "url": i["link"]} for n, i in enumerate(items)]}},
                    ensure_ascii=False).replace("</", "<\\/")
    stamp = now.strftime("%A, %-d %B %Y · Updated %-I:%M %p IST")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CBSE News Today: Date Sheet 2027, Board Exam Updates &amp; Circulars | CBSE Newsroom</title>
<meta name="description" content="CBSE Newsroom: today's CBSE board exam news for Class 10 and 12 — 2027 date sheet, syllabus changes, circulars, admit cards and results, checked every day. Board exams begin 16 Feb 2027.">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://cbsemock.org.in/news.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CBSEMock">
<meta property="og:title" content="CBSE Newsroom — Board Exam News &amp; Date Sheet 2027">
<meta property="og:description" content="Today's CBSE news for Class 10 and 12: date sheet, syllabus, circulars and results. {days} days to board exams.">
<meta property="og:url" content="https://cbsemock.org.in/news.html">
<meta property="og:image" content="https://cbsemock.org.in/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="CBSE Newsroom — Board Exam News &amp; Date Sheet 2027">
<meta name="twitter:description" content="Today's CBSE news for Class 10 and 12.">
<meta name="twitter:image" content="https://cbsemock.org.in/og-image.jpg">
<script type="application/ld+json">{ld}</script>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2810600896966939" crossorigin="anonymous"></script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@600;700;800&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--navy:#0f2347;--navy2:#1a3a6b;--gold:#c9a227;--gold2:#e8cc6a;--red:#b91c1c;--bg:#f3f1ed;--card:#fff;--text:#14171f;--muted:#5d6472;--border:#e2ddd2}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font:16px/1.55 Inter,system-ui,-apple-system,'Segoe UI',sans-serif;background:var(--bg);color:var(--text)}}
a{{color:inherit;text-decoration:none}}
.nr-top{{background:var(--navy);color:#fff;font-size:.8rem}}.nr-in{{max-width:1180px;margin:0 auto;padding-left:18px;padding-right:18px}}
.nr-top .nr-in{{padding-top:8px;padding-bottom:8px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}}.nr-top b{{color:var(--gold2)}}
.mast{{background:#fffdf7;border-bottom:4px double var(--navy)}}.mast .nr-in{{padding-top:18px;padding-bottom:14px;display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap}}
.mast h1{{font:800 clamp(2rem,5vw,3.3rem)/1 'Crimson Pro',Georgia,serif;color:var(--navy);letter-spacing:-.5px}}.mast h1 em{{font-style:normal;color:var(--red)}}
.mast p{{color:var(--muted);font-size:.88rem;margin-top:6px}}
.cd{{display:flex;align-items:center;gap:12px;background:var(--navy);color:#fff;border-radius:14px;padding:10px 18px}}
.cd b{{font:800 2.1rem/1 'Crimson Pro',Georgia,serif;color:var(--gold2)}}.cd span{{font-size:.8rem;line-height:1.3}}.cd small{{opacity:.75}}
.tabs{{background:#fff;border-bottom:1px solid var(--border)}}.tabs .nr-in{{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none}}
.tabs button{{font:700 .88rem Inter,sans-serif;background:none;border:0;border-bottom:3px solid transparent;color:var(--muted);padding:13px 14px;white-space:nowrap;cursor:pointer}}
.tabs button.on,.tabs button:hover{{color:var(--navy);border-color:var(--red)}}
.tick{{background:var(--red);color:#fff;display:flex;align-items:center;overflow:hidden}}
.tick .lb{{position:relative;z-index:2;flex:0 0 auto;background:#7f1d1d;font:800 .78rem Inter,sans-serif;letter-spacing:.08em;padding:10px 14px;display:flex;gap:8px;align-items:center}}
.tick .lb i{{width:8px;height:8px;border-radius:50%;background:#fff;animation:nrb 1s infinite}}@keyframes nrb{{50%{{opacity:.2}}}}
.tick .tr{{display:flex;gap:44px;white-space:nowrap;font-size:.86rem;font-weight:600;padding-left:22px;animation:nrm 60s linear infinite}}@keyframes nrm{{to{{transform:translateX(-50%)}}}}
.tick:hover .tr{{animation-play-state:paused}}
.wrap{{max-width:1180px;margin:0 auto;padding:22px 18px 60px;display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:22px}}
.hero{{display:grid;grid-template-columns:1.25fr 1fr;gap:18px;margin-bottom:22px}}
.ts{{background:linear-gradient(160deg,var(--navy2),var(--navy));color:#fff;border-radius:20px;padding:24px 26px;position:relative;overflow:hidden;min-height:330px;display:flex;flex-direction:column;box-shadow:0 18px 40px rgba(15,35,71,.25);transition:transform .2s}}
.ts:hover{{transform:translateY(-3px)}}
.ts::before{{content:"";position:absolute;right:-60px;top:-60px;width:260px;height:260px;border-radius:50%;background:radial-gradient(rgba(232,204,106,.35),transparent 70%)}}
.ts .lbl{{display:flex;gap:8px;margin-bottom:auto;padding-bottom:18px;position:relative}}.ts .lbl span{{font:800 .72rem Inter,sans-serif;letter-spacing:.08em;padding:5px 10px;border-radius:6px}}
.ts h2{{font:700 clamp(1.6rem,3vw,2.3rem)/1.12 'Crimson Pro',Georgia,serif;margin-bottom:12px;position:relative}}
.ts .dek{{color:rgba(255,255,255,.85);font-size:.95rem;margin-bottom:14px;position:relative}}
.ts .mt{{font-size:.82rem;color:var(--gold2);display:flex;gap:14px;flex-wrap:wrap;position:relative}}
.bb{{background:#c8a271;background-image:radial-gradient(rgba(0,0,0,.08) 1px,transparent 1px),radial-gradient(rgba(255,255,255,.12) 1px,transparent 1px);background-size:7px 7px,11px 11px;border:10px solid #6b4423;border-radius:14px;padding:16px 14px 12px;box-shadow:inset 0 0 30px rgba(0,0,0,.25),0 14px 30px rgba(0,0,0,.2)}}
.bb h2{{font:800 .82rem Inter,sans-serif;letter-spacing:.12em;color:#fff;background:#6b4423;display:inline-block;padding:4px 10px;border-radius:6px;margin-bottom:10px}}
.nt{{display:block;position:relative;background:#fff8c4;padding:12px 12px 10px;margin:10px 4px;font-size:.84rem;line-height:1.35;color:#333;box-shadow:2px 6px 12px rgba(0,0,0,.25);transform:rotate(-1.2deg);transition:transform .2s}}
.nt:nth-of-type(2){{background:#d9f7e8;transform:rotate(1deg)}}.nt:nth-of-type(3){{background:#ffe1e6;transform:rotate(-.6deg)}}.nt:nth-of-type(4){{background:#dbeafe;transform:rotate(1.4deg)}}
a.nt:hover{{transform:rotate(0) scale(1.03)}}
.nt::before{{content:"";position:absolute;top:-7px;left:50%;width:14px;height:14px;margin-left:-7px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#ff8a8a,#b91c1c);box-shadow:0 2px 3px rgba(0,0,0,.4)}}
.nt b{{display:block;font-size:.9rem;color:#14171f}}
.qg{{display:none}}
.sec{{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin:6px 0 12px;border-bottom:2px solid var(--navy);padding-bottom:6px}}
.sec h2{{font:800 1.4rem 'Crimson Pro',Georgia,serif;color:var(--navy)}}.fl{{display:flex;gap:6px}}
.fl button{{font:800 .76rem Inter,sans-serif;padding:6px 12px;border-radius:99px;border:1.5px solid var(--border);background:#fff;color:var(--text);cursor:pointer}}.fl button.on{{background:var(--navy);color:#fff;border-color:var(--navy)}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}}
.nc{{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:16px;display:flex;flex-direction:column;gap:8px;transition:transform .2s,box-shadow .2s}}
.nc:hover{{transform:translateY(-4px);box-shadow:0 12px 26px rgba(15,35,71,.12)}}.nc[hidden]{{display:none}}
.chip{{align-self:flex-start;font:800 .66rem Inter,sans-serif;letter-spacing:.08em;color:var(--c);background:color-mix(in srgb,var(--c) 12%,#fff);padding:4px 8px;border-radius:6px}}
.nc h3{{font:700 1rem/1.32 Inter,sans-serif}}.nc .mt{{margin-top:auto;display:flex;justify-content:space-between;gap:8px;font-size:.76rem;color:var(--muted)}}.nc .mt b{{color:var(--text)}}.nc .rd{{color:#1d4ed8;font-weight:700;white-space:nowrap}}
.empty{{display:none;padding:30px;text-align:center;color:var(--muted);background:#fff;border-radius:16px;border:1px dashed var(--border)}}
.cta{{margin-top:22px;border-radius:18px;padding:20px 22px;background:linear-gradient(135deg,var(--navy),#3b0a16);color:#fff;display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}}
.cta b{{font:700 1.3rem 'Crimson Pro',Georgia,serif}}.cta p{{font-size:.86rem;opacity:.85}}
.cta a{{background:var(--gold2);color:var(--navy);font-weight:800;font-size:.86rem;padding:11px 18px;border-radius:99px;box-shadow:0 5px 0 #8a6d12;transition:transform .15s,box-shadow .15s}}.cta a:active{{transform:translateY(4px);box-shadow:0 1px 0 #8a6d12}}
aside .box{{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:16px;margin-bottom:16px}}
aside h2{{font:800 .8rem Inter,sans-serif;letter-spacing:.1em;color:var(--muted);margin-bottom:12px}}
.b3{{display:flex;align-items:center;gap:12px;padding:12px 14px;margin-bottom:12px;border-radius:16px;color:#fff;background:linear-gradient(160deg,var(--a),var(--b));
 box-shadow:0 6px 0 color-mix(in srgb,var(--b) 70%,#000),0 12px 22px rgba(0,0,0,.18);transition:transform .15s,box-shadow .15s}}
.b3:hover{{transform:translateY(-3px);box-shadow:0 9px 0 color-mix(in srgb,var(--b) 70%,#000),0 18px 28px rgba(0,0,0,.22)}}
.b3:active{{transform:translateY(5px);box-shadow:0 1px 0 color-mix(in srgb,var(--b) 70%,#000),0 4px 8px rgba(0,0,0,.15)}}
.b3 .ic{{flex:0 0 44px;height:44px;border-radius:12px;background:rgba(255,255,255,.18);display:flex;align-items:center;justify-content:center;font-size:1.35rem;box-shadow:inset 0 -3px 0 rgba(0,0,0,.15)}}
.b3 .tx{{flex:1;min-width:0}}.b3 b{{display:block;font-size:.98rem}}.b3 small{{font-size:.76rem;opacity:.85}}.b3 .ar{{font-weight:800;opacity:.8}}
.off a{{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--border);font-size:.86rem;font-weight:600}}.off a:last-child{{border:0}}.off a:hover{{color:#1d4ed8}}
aside .box.tg{{background:linear-gradient(135deg,#229ED9,#1b6fa3);color:#fff;border:0}}.tg h2{{color:#e0f2fe}}.tg p{{font-size:.88rem;margin-bottom:12px}}
.tg a{{display:inline-block;background:#fff;color:#1b6fa3;font-weight:800;font-size:.82rem;padding:9px 14px;border-radius:99px}}
.src{{font-size:.74rem;color:var(--muted);margin-top:16px}}
@media(max-width:980px){{.wrap{{grid-template-columns:minmax(0,1fr)}}.grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}aside{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}aside .box{{margin:0}}}}
@media(max-width:640px){{.nr-in,.wrap{{padding-left:16px;padding-right:16px}}.hero{{grid-template-columns:1fr}}.grid{{grid-template-columns:1fr}}aside{{display:block}}aside .box{{margin-bottom:16px}}
 .ts{{min-height:0;padding:20px}}.cd{{width:100%}}
 .qg{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:24px}}.qg .b3{{flex-direction:column;align-items:flex-start;gap:6px;margin:0;padding:12px}}
 .qg .b3 .ar,.qg .b3 small{{display:none}}.qg .b3 .ic{{flex:0 0 auto;width:38px;height:38px}}aside .explore{{display:none}}}}
@media(prefers-reduced-motion:reduce){{.tick .tr{{animation:none;overflow-x:auto}}.tick .lb i{{animation:none}}.b3,.nc,.ts,.nt{{transition:none}}}}
</style>
</head>
<body>
<div class="nr-top"><div class="nr-in"><span>📅 {E(stamp)}</span><span><b>CBSE</b>Mock Newsroom · Class 10 &amp; 12</span></div></div>
<header class="mast"><div class="nr-in"><div><h1>CBSE <em>Newsroom</em></h1><p>Board exam news, date sheets, syllabus changes and circulars — checked every day</p></div>
<div class="cd" aria-label="Days to board exams"><b id="nr-days">{days}</b><span>days to<br>Board Exams {exam.year}<br><small>from {exam.day} {exam.strftime('%b %Y')}</small></span></div></div></header>
<nav class="tabs" aria-label="News categories"><div class="nr-in" id="nr-tabs">{tabs}</div></nav>
<div class="tick" aria-label="Latest headlines"><div class="lb"><i></i>LATEST</div><div class="tr">{tick}<span aria-hidden="true"></span>{tick}</div></div>
<div class="wrap"><main>
<section class="hero">
 <a class="ts" href="{E(top["link"])}" target="_blank" rel="noopener nofollow"><div class="lbl"><span style="background:#e11d48">TOP STORY</span><span style="background:rgba(255,255,255,.15)">{tlbl.upper()}</span></div>
 <h2>{E(top["title"])}</h2><p class="dek">{E(DEKS[top["cat"]].format(exam=f"{exam.day} {exam.strftime('%B %Y')}"))}</p>
 <div class="mt"><span>{E(top["source"])} · {E(ago(top["dt"], now))}</span><span>Read the full story ↗</span></div></a>
 <div class="bb"><h2>📌 BULLETIN BOARD</h2>{notes_html}</div>
</section>
<div class="qg" aria-label="Explore CBSEMock">{b3}</div>
<div class="sec"><h2>Latest updates</h2><div class="fl" id="nr-cls"><button class="on" data-c="all">All</button><button data-c="10">Class 10</button><button data-c="12">Class 12</button></div></div>
<div class="grid" id="nr-grid">
{cards}
</div>
<div class="empty" id="nr-empty">No stories in this section today — check back tomorrow.</div>
<div class="cta"><div><b>Exams in {days} days. Practise like it's the real thing.</b><p>Free full-length CBSE mock papers with solutions — a new one every Mon, Wed &amp; Fri.</p></div><a href="free-mock-papers/">Get free mock papers →</a></div>
<p class="src">Headlines from publishers via Google News, refreshed daily at 9:30 AM IST. Always confirm dates on cbse.gov.in.</p>
</main>
<aside><div class="box explore"><h2>EXPLORE CBSEMOCK</h2>{b3}</div>
<div class="box off"><h2>OFFICIAL SOURCES</h2><a href="https://www.cbse.gov.in/" target="_blank" rel="noopener">cbse.gov.in <span>↗</span></a><a href="https://cbseacademic.nic.in/" target="_blank" rel="noopener">cbseacademic.nic.in (syllabus) <span>↗</span></a><a href="https://results.cbse.nic.in/" target="_blank" rel="noopener">results.cbse.nic.in <span>↗</span></a></div>
<div class="box tg"><h2>GET ALERTS</h2><p>Date sheet changes, circulars and free papers on Telegram.</p><a href="https://t.me/cbsemockportal" target="_blank" rel="noopener">Join @cbsemockportal →</a></div></aside>
</div>
<script>
(function(){{
 var ex=new Date('{exam.isoformat()}T00:00:00+05:30'),d=Math.max(0,Math.ceil((ex-Date.now())/864e5)),el=document.getElementById('nr-days');if(el)el.textContent=d;
 var cat='all',cls='all',cards=[].slice.call(document.querySelectorAll('#nr-grid .nc'));
 function apply(){{var n=0;cards.forEach(function(c){{var ok=(cat==='all'||c.dataset.cat===cat)&&(cls==='all'||c.dataset.cls===cls||c.dataset.cls==='both');c.hidden=!ok;if(ok)n++;}});
  document.getElementById('nr-empty').style.display=n?'none':'block';}}
 function group(id,attr,set){{var g=document.getElementById(id);g.addEventListener('click',function(e){{var b=e.target.closest('button');if(!b)return;
  [].forEach.call(g.querySelectorAll('button'),function(x){{x.classList.toggle('on',x===b);}});set(b.dataset[attr]);apply();}});}}
 group('nr-tabs','f',function(v){{cat=v;}});group('nr-cls','c',function(v){{cls=v;}});
}})();
</script>
<script src="portal-shell.js"></script>
</body>
</html>"""


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    now = datetime.now(IST)
    if "--from" in sys.argv:
        raw = json.load(open(sys.argv[sys.argv.index("--from") + 1], encoding="utf-8"))
        raw = [dict(r, title=clean_title(r["title"], r.get("source", ""))) for r in raw]
    else:
        print("Fetching CBSE news from Google News RSS...")
        raw = []
        for q in QUERIES:
            got = fetch_items(q)
            print(f"  {q}: {len(got)}")
            raw.extend(got)
    items = prepare(raw, now)
    print(f"  {len(items)} stories after filtering")
    if len(items) < MIN_ITEMS:
        print(f"Only {len(items)} stories — feed looks broken; keeping the existing news.html")
        sys.exit(0)
    page = build_html(items, now)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Written: {OUT_PATH} ({len(page):,} bytes)")
