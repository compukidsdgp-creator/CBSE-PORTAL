"""Link-in-bio page: cbsemock.org.in/go/

Instagram captions can't hold clickable links, so they say "link in bio" and the bio links here.
The page lists the most recent reels and formula cards posted to Instagram (newest first), each with
buttons to its explainer, chapter quiz and mock papers, plus the main sections of the site.

Rebuilt by the posting workflows and the daily portal job:   python3 go_page.py
"""
import csv
import html
import json
from pathlib import Path

from topic_links import SITE, why_links, formula_links

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "go"
E = html.escape
MAX_ITEMS = 12


def rel(url):
    return url.replace(SITE + "/", "../")


def read_csv(path):
    try:
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


def ok(row):
    return row.get("dry_run") != "True" and (row.get("ig_media_id") or "").isdigit()


def items():
    out = []
    # WHY? reels
    for r in read_csv(ROOT / "formula-posts/why/why_log.csv"):
        if not ok(r):
            continue
        name = r["filename"]
        stem = Path(name).stem
        num, slug = stem.split("_why_", 1) if "_why_" in stem else ("", stem)
        L = why_links(name)
        title = slug.replace("_", " ").capitalize()
        try:
            import importlib
            from topic_links import _why_module
            _, mod = _why_module(slug)
            if mod is not None:
                title = mod.CAPTION.strip().splitlines()[0].split("WHY? —", 1)[-1].strip()
        except Exception:
            pass
        th = f"why-reels/thumb/{num}-{slug}.jpg"
        out.append({"when": f"{r['date_ist']} {r['time_ist']}", "kind": "WHY? reel", "title": title,
                    "thumb": th if (ROOT / th).exists() else "", "watch": f"why-reels/#{num}-{slug}", "links": L})
    # Formula Flash reels
    import social_links as SL
    for r in read_csv(ROOT / "formula-posts/reel_log.csv"):
        if r.get("dry_run") is None:          # rows written by log_reel() have 6 columns under an older 7-column header
            r = {"date_ist": r["date_ist"], "time_ist": r["time_ist"], "topic_id": r["topic_id"],
                 "ig_media_id": r["fb_video_id"], "dry_run": r["ig_media_id"]}
        if not ok(r):
            continue
        stem = Path(r["topic_id"]).stem
        th = f"formula-reels/thumb/{stem}.jpg"
        title = stem.replace("_part_", " · Part ").replace("_", " ").title().replace("· Part", "· Part")
        out.append({"when": f"{r['date_ist']} {r['time_ist']}", "kind": "Formula reel", "title": title,
                    "thumb": th if (ROOT / th).exists() else "", "watch": f"formula-reels/#{stem}",
                    "links": SL.links_for_formula_reel(stem)})
    # Formula cards (images)
    try:
        from post_formula_image import parse_filename
        from formula_board_page import slugify
    except Exception:
        parse_filename = None
    for r in read_csv(ROOT / "formula-posts/post_log.csv"):
        if not ok(r) or parse_filename is None:
            continue
        stem = Path(r["filename"]).stem
        info = parse_filename(stem)
        th = f"formula-board/thumb/{slugify(stem)}.webp"
        when = r["timestamp_ist"].replace(" IST", "")
        out.append({"when": when, "kind": "Formula card", "title": info["topic"],
                    "thumb": th if (ROOT / th).exists() else "", "watch": "formula-board/",
                    "links": SL.links_for_formula_image(info["subject"], info["topic"], info["class"])})
    out.sort(key=lambda d: d["when"], reverse=True)
    seen, uniq = set(), []
    for d in out:
        if d["title"] not in seen:
            seen.add(d["title"])
            uniq.append(d)
    return uniq[:MAX_ITEMS]


CSS = """
:root{--navy:#1a3a6b;--navy2:#0f2347;--gold:#c9a227;--gold2:#e8cc6a;}
*{box-sizing:border-box;margin:0;padding:0}
body{font:15px/1.5 Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:linear-gradient(160deg,#1a3a6b,#0f2347 60%,#0b1a36);color:#fff;min-height:100vh}
.w{max-width:560px;margin:0 auto;padding:26px 16px 50px}
.hd{text-align:center;margin-bottom:20px}
.logo{width:76px;height:76px;border-radius:50%;background:#fff url(logo.png) center/cover;margin:0 auto 10px;border:3px solid var(--gold);box-shadow:0 0 0 6px rgba(201,162,39,.18)}
h1{font-family:'Crimson Pro',Georgia,serif;font-size:1.9rem;line-height:1.1}
h1 b{color:var(--gold2)}
.hd p{color:rgba(255,255,255,.75);font-size:.88rem;margin-top:6px}
.main{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:18px 0 26px}
.main a{display:flex;align-items:center;justify-content:center;gap:6px;min-height:52px;padding:10px;border-radius:14px;color:#fff;text-decoration:none;font-weight:700;font-size:.86rem;text-align:center;box-shadow:0 5px 0 rgba(0,0,0,.18);transition:transform .18s,box-shadow .18s,filter .18s}
.main a:hover{transform:translateY(-3px);filter:brightness(1.1);box-shadow:0 8px 0 rgba(0,0,0,.14),0 0 0 2px var(--gold2)}
.main a:nth-child(1){background:linear-gradient(135deg,#c0284f,#4a0e1f)}
.main a:nth-child(2){background:linear-gradient(135deg,#c99a06,#4a3700)}
.main a:nth-child(3){background:linear-gradient(135deg,#2b9a80,#12483e)}
.main a:nth-child(4){background:linear-gradient(135deg,#4f5bd5,#12154d)}
.main a:nth-child(5){background:linear-gradient(135deg,#1497b8,#073445)}
.main a:nth-child(6){background:linear-gradient(135deg,#229ED9,#0b5e8a)}
h2{font-family:'Crimson Pro',Georgia,serif;color:var(--gold2);font-size:1.35rem;margin:0 0 10px}
.it{display:flex;gap:12px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:16px;padding:10px;margin-bottom:12px}
.th{flex:0 0 74px;height:110px;border-radius:10px;background:#000 center/cover no-repeat;display:block}
.bd{flex:1;min-width:0}
.k{font-size:.75rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--gold2)}
.t{font-weight:700;font-size:.98rem;line-height:1.3;margin:3px 0 8px}
.bt{display:flex;flex-wrap:wrap;gap:6px}
.bt a{display:inline-block;padding:6px 11px;border-radius:99px;font-size:.76rem;font-weight:700;color:#fff;text-decoration:none;transition:transform .15s,filter .15s}
.bt a:hover{transform:translateY(-2px);filter:brightness(1.15)}
.bt .learn{background:linear-gradient(135deg,#c99a06,#7a5c00)}
.bt .notes{background:linear-gradient(135deg,#e8452c,#7a1a0c)}
.bt .quiz{background:linear-gradient(135deg,#2b9a80,#12483e)}
.bt .paper{background:linear-gradient(135deg,#3b6fb8,#0e2344)}
.bt .watch{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25)}
.ft{text-align:center;color:rgba(255,255,255,.6);font-size:.78rem;margin-top:24px}
.ft a{color:var(--gold2);display:inline-block;padding:6px 4px}
"""


def build():
    rows = []
    for d in items():
        L = d["links"]
        btn = []
        if L.get("notes"):
            btn.append(f'<a class="notes" href="{rel(L["notes"][1])}">📒 Chapter notes</a>')
        if L.get("learn"):
            btn.append(f'<a class="learn" href="{rel(L["learn"][1])}">📘 Explainer</a>')
        for t, u in L.get("chapters", [])[:1]:
            btn.append(f'<a class="quiz" href="{rel(u)}">📝 {E(t.replace(" quiz", ""))} quiz</a>')
        if L.get("portal"):
            btn.append(f'<a class="paper" href="{rel(L["portal"][1])}">📄 Mock papers</a>')
        btn.append(f'<a class="watch" href="../{d["watch"]}">' + ('🧮 View card' if d['kind'] == 'Formula card' else '▶ Watch') + '</a>')
        th = f'<a class="th" href="../{d["watch"]}" style="background-image:url(../{d["thumb"]})" aria-label="Open {E(d["title"])}"></a>' if d["thumb"] else ""
        rows.append(f'<div class="it">{th}<div class="bd"><div class="k">{E(d["kind"])}</div>'
                    f'<div class="t">{E(d["title"])}</div><div class="bt">{"".join(btn)}</div></div></div>')
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CBSEMock — links from our posts</title>
<meta name="description" content="Links for the latest CBSEMock reels and formula cards: explainers, chapter quizzes and free CBSE mock papers for Class 10 and 12.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{SITE}/go/">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@700&family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>
</head>
<body>
<main class="w">
<div class="hd"><div class="logo" role="img" aria-label="CBSEMock"></div>
<h1>CBSE<b>Mock</b></h1><p>Free CBSE Class 10 &amp; 12 practice — tap a post below for its quiz, explainer and mock papers.</p></div>
<nav class="main">
<a href="../free-mock-papers/">📄 Free pre-board papers</a>
<a href="../board-plan/">📅 60-Day Board Plan: a daily exam hack</a>
<a href="../mistake-bank/">⚠️ Mistake Bank: top board-exam mistakes</a>
<a href="../booster/">⚡ Weekly Knowledge Booster</a>
<a href="../learn/">📘 Learn: WHY? explainers</a>
<a href="../mock-zone/index.html">📝 Mock tests</a>
<a href="../formula-board/">🧮 Formula Board</a>
<a href="../why-reels/">🎬 All reels</a>
<a href="https://www.youtube.com/@CBSEMOCK?sub_confirmation=1" rel="noopener">▶️ YouTube: all our Shorts</a>
<a href="https://t.me/cbsemockportal" rel="noopener">✈️ Telegram channel</a>
</nav>
<h2>From our latest posts</h2>
{''.join(rows) or '<p>New posts appear here as they go out.</p>'}
<p class="ft"><a href="../index.html">cbsemock.org.in</a> · <a href="../about.html">About</a> · <a href="../privacy.html">Privacy</a></p>
</main>
</body>
</html>
"""
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(page, encoding="utf-8")
    print(f"[ok] go/: {len(rows)} recent posts")


if __name__ == "__main__":
    build()
    import favicon_tags                       # favicon links on the pages just written
    for _g in "go/*.html".split():
        for _f in sorted(favicon_tags.ROOT.glob(_g)):
            favicon_tags.add(_f)
