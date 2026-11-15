"""Build the Learn section: /learn/index.html + one page per article in learn_articles.py.

An article goes live once its `published` date (IST) has arrived, so future articles can be
written ahead and roll out with the WHY? reels. Each page embeds its WHY? reel from wherever
the video currently lives (formula-posts/why/queue or /posted).

    python3 learn_pages.py            # writes learn/*.html, removes pages of unpublished articles
"""
import html
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from learn_articles import ARTICLES, AUTHOR, AUTHOR_ROLE

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "learn"
SITE = "https://cbsemock.org.in"
TODAY = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()
E = html.escape

CAT_COLOR = {"Maths": "#2d6a4f", "AI": "#6d28d9", "Computer Science": "#1d4ed8", "Physics": "#b45309",
             "Chemistry": "#be123c", "Biology": "#047857", "Science": "#b45309"}


def find_reel(mod):
    """-> (video path rel. to site root, thumb path rel. to site root) for WHY? module `mod`."""
    for folder in ("formula-posts/why/queue", "formula-posts/why/posted"):
        for f in sorted((ROOT / folder).glob(f"*_why_{mod}*.mp4")):
            m = re.match(r"(\d+)_why_(.+)\.mp4$", f.name)
            if not m or not (m.group(2) == mod or m.group(2).startswith(mod + "_")):
                continue
            th = ROOT / "why-reels/thumb" / f"{m.group(1)}-{m.group(2)}.jpg"
            return f"{folder}/{f.name}", (str(th.relative_to(ROOT)) if th.exists() else "")
    return "", ""


def live_articles():
    arts = [a for a in ARTICLES if datetime.strptime(a["published"], "%Y-%m-%d").date() <= TODAY]
    return sorted(arts, key=lambda a: (a["published"], ARTICLES.index(a)), reverse=True)


CSS = """
:root{--bg:#f8f7f4;--card:#fff;--text:#1a1a1a;--muted:#5f5f5f;--accent:#2d6a4f;--border:#e5e3df;--code:#f1f0ec;}
@media(prefers-color-scheme:dark){:root{--bg:#161616;--card:#222;--text:#eee;--muted:#a0a0a0;--border:#343434;--accent:#52b788;--code:#2b2b2b;}}
*{box-sizing:border-box;margin:0;padding:0;}
body{font:16px/1.75 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);}
header.top{background:#2d6a4f;color:#fff;padding:14px 20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;}
header.top a{color:#fff;text-decoration:none;font-size:.88rem;opacity:.88;}
header.top a:hover{opacity:1;}
.wrap{max-width:780px;margin:0 auto;padding:28px 20px 70px;}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:14px;}
.crumb a{color:var(--muted);}
h1{font-size:1.85rem;line-height:1.25;margin-bottom:12px;letter-spacing:-.01em;}
.meta{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;font-size:.86rem;color:var(--muted);margin-bottom:22px;}
.pill{display:inline-block;padding:2px 10px;border-radius:99px;color:#fff;font-size:.76rem;font-weight:600;letter-spacing:.02em;}
.byline{display:flex;gap:12px;align-items:center;border:1px solid var(--border);background:var(--card);border-radius:12px;padding:12px 14px;margin:0 0 24px;font-size:.9rem;}
.byline .av{flex:0 0 42px;height:42px;border-radius:50%;background:#2d6a4f;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;}
.byline small{color:var(--muted);display:block;line-height:1.45;}
.reel{float:right;width:250px;margin:4px 0 18px 26px;}
.reel video{width:100%;aspect-ratio:9/16;border-radius:14px;background:#000;display:block;box-shadow:0 6px 24px rgba(0,0,0,.18);}
.reel p{font-size:.78rem;color:var(--muted);text-align:center;margin-top:6px;line-height:1.4;}
article h2{font-size:1.25rem;margin:30px 0 10px;line-height:1.3;}
article p{margin:0 0 14px;}
article ul,article ol{margin:0 0 16px 22px;}
article li{margin:5px 0;}
article code{background:var(--code);padding:1px 6px;border-radius:5px;font-size:.9em;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;}
article pre{background:#1e1e2e;color:#e7e7f0;border-radius:10px;padding:14px 16px;overflow-x:auto;margin:0 0 18px;font-size:.85rem;line-height:1.55;clear:both;}
article pre code{background:none;padding:0;color:inherit;}
article table{border-collapse:collapse;width:100%;margin:0 0 18px;font-size:.92rem;clear:both;display:block;overflow-x:auto;}
article th,article td{border:1px solid var(--border);padding:7px 10px;text-align:left;}
article th{background:var(--code);}
.box{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px 22px;margin:30px 0 0;clear:both;}
.box h2{margin-top:0;font-size:1.12rem;}
details{border-top:1px solid var(--border);padding:10px 0;}
details:first-of-type{border-top:0;}
summary{cursor:pointer;font-weight:600;}
details .ans{margin-top:8px;color:var(--muted);}
.links{list-style:none;margin:0!important;display:grid;gap:8px;}
.links a{display:block;padding:10px 14px;border:1px solid var(--border);border-radius:10px;text-decoration:none;color:var(--text);}
.links a:hover{border-color:var(--accent);}
.links a::after{content:" →";color:var(--accent);}
a{color:var(--accent);}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;}
.card{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden;text-decoration:none;color:var(--text);transition:transform .15s,border-color .15s;}
.card:hover{transform:translateY(-2px);border-color:var(--accent);}
.card .th{aspect-ratio:16/10;background:#111 center/cover no-repeat;}
.card .bd{padding:12px 14px 16px;}
.card b{display:block;font-size:1rem;line-height:1.35;margin:6px 0;}
.card span.d{font-size:.84rem;color:var(--muted);line-height:1.5;}
.intro{color:var(--muted);font-size:1.02rem;margin-bottom:24px;}
footer{text-align:center;padding:26px 16px;font-size:.8rem;color:var(--muted);border-top:1px solid var(--border);}
footer a{color:var(--muted);margin:0 6px;}
@media(max-width:640px){h1{font-size:1.5rem;}.reel{float:none;width:min(260px,72%);margin:0 auto 22px;}}
"""

HEAD_TAGS = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2810600896966939" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>"""

FOOTER = """<footer>&copy; 2026 CBSEMock.org.in &nbsp;|&nbsp;
<a href="../about.html">About Us</a>|<a href="../privacy.html">Privacy Policy</a>|<a href="../terms.html">Terms of Use</a>|<a href="../contact.html">Contact</a>|<a href="../disclaimer.html">Disclaimer</a></footer>"""


def head(title, desc, url, ldjson, og_img="", og_type="article"):
    import json
    img = f'<meta property="og:image" content="{SITE}/{og_img}">' if og_img else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="{og_type}">
{img}
<meta name="twitter:card" content="summary_large_image">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ldjson, ensure_ascii=False)}</script>
{HEAD_TAGS}
</head>"""


def nice_date(s):
    d = datetime.strptime(s, "%Y-%m-%d")
    return f"{d.day} {d:%B %Y}"


def article_page(a, others):
    url = f"{SITE}/learn/{a['slug']}.html"
    video, thumb = find_reel(a["reel"])
    color = CAT_COLOR.get(a["category"], "#2d6a4f")
    pub = a["published"]
    upd = a.get("updated", pub)
    words = len(re.sub(r"<[^>]+>", " ", a["body"]).split())
    graph = [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Learn", "item": SITE + "/learn/"},
            {"@type": "ListItem", "position": 3, "name": a["h1"], "item": url}]},
        {"@type": "Article", "headline": a["h1"], "description": a["description"], "url": url,
         "mainEntityOfPage": url, "datePublished": pub, "dateModified": upd, "wordCount": words,
         "inLanguage": "en-IN", "articleSection": a["category"],
         "educationalLevel": "CBSE " + a["class_label"],
         "author": {"@type": "Person", "name": AUTHOR, "jobTitle": AUTHOR_ROLE, "url": SITE + "/about.html"},
         "publisher": {"@type": "EducationalOrganization", "name": "CBSE Mock", "url": SITE},
         **({"image": f"{SITE}/{thumb}"} if thumb else {})},
    ]
    if video:
        graph.append({"@type": "VideoObject", "name": a["h1"], "description": a["description"],
                      "thumbnailUrl": f"{SITE}/{thumb}" if thumb else f"{SITE}/logo.png",
                      "uploadDate": pub + "T18:30:00+05:30", "contentUrl": f"{SITE}/{video}",
                      "embedUrl": url})
    ld = {"@context": "https://schema.org", "@graph": graph}

    reel = ""
    if video:
        poster = f' poster="../{thumb}"' if thumb else ""
        reel = (f'<figure class="reel"><video controls playsinline preload="none"'
                f'{poster} src="../{video}" title="{E(a["h1"])}"></video>'
                f'<p>Watch: the short WHY? reel</p></figure>')
    practice = "".join(f"<details><summary>{E(q)}</summary><p class=\"ans\">{E(ans)}</p></details>"
                       for q, ans in a.get("practice", []))
    related = "".join(f'<li><a href="../{h}">{E(l)}</a></li>' for l, h in a.get("related", []))
    related += '<li><a href="../why-reels/">All WHY? reels</a></li>'
    more = "".join(f'<li><a href="{o["slug"]}.html">{E(o["h1"])}</a></li>' for o in others[:4])

    body = f"""<body>
<header class="top"><a href="../index.html">← CBSEMock.org.in</a><span style="opacity:.5">|</span><a href="./"><strong>Learn</strong></a></header>
<main class="wrap">
<nav class="crumb"><a href="../index.html">Home</a> › <a href="./">Learn</a> › {E(a['category'])}</nav>
<article>
<h1>{E(a['h1'])}</h1>
<div class="meta"><span class="pill" style="background:{color}">{E(a['category'])}</span><span>CBSE {E(a['class_label'])}</span><span>{a.get('read_min', 5)} min read</span><span>Updated {nice_date(upd)}</span></div>
<div class="byline"><div class="av" aria-hidden="true">BM</div><div><b>{E(AUTHOR)}</b> · {E(AUTHOR_ROLE)}<small>20 years of teaching · Reviewed by subject teachers · <a href="../about.html">About us</a></small></div></div>
{reel}
{a['body'].strip()}
</article>
{f'<section class="box"><h2>Try it yourself</h2>{practice}</section>' if practice else ''}
<section class="box"><h2>Practise this topic</h2><ul class="links">{related}</ul></section>
{f'<section class="box"><h2>More WHY? explainers</h2><ul class="links">{more}</ul></section>' if more else ''}
</main>
{FOOTER}
</body>
</html>
"""
    return head(a["title"] + " | CBSEMock", a["description"], url, ld, thumb) + "\n" + body


def index_page(arts):
    url = SITE + "/learn/"
    desc = ("Short, clear explainers for CBSE Class 10 and 12 — the ‘why’ behind formulas and concepts in Maths, "
            "Science, Computer Science and AI, each with a short reel and practice questions.")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Learn", "item": url}]},
        {"@type": "CollectionPage", "name": "Learn — WHY? explainers", "url": url, "description": desc,
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/learn/{a['slug']}.html", "name": a["h1"]}
             for i, a in enumerate(arts)]}}]}
    cards = []
    for a in arts:
        _, thumb = find_reel(a["reel"])
        color = CAT_COLOR.get(a["category"], "#2d6a4f")
        bg = f' style="background-image:url(../{thumb})"' if thumb else ""
        cards.append(f'<a class="card" href="{a["slug"]}.html"><div class="th"{bg}></div><div class="bd">'
                     f'<span class="pill" style="background:{color}">{E(a["category"])}</span> '
                     f'<span class="d">CBSE {E(a["class_label"])}</span>'
                     f'<b>{E(a["h1"])}</b><span class="d">{E(a["description"])}</span></div></a>')
    body = f"""<body>
<header class="top"><a href="../index.html">← CBSEMock.org.in</a><span style="opacity:.5">|</span><strong>Learn</strong></header>
<main class="wrap" style="max-width:1040px">
<nav class="crumb"><a href="../index.html">Home</a> › Learn</nav>
<h1>Learn: the WHY? behind CBSE concepts</h1>
<p class="intro">Board questions reward students who understand <i>why</i> a formula or idea works, not just what it says. Each explainer here takes one concept from the Class 10 or Class 12 syllabus, explains it step by step with a worked example and common mistakes, and ends with practice questions. Every article comes with a short WHY? reel. Written by {E(AUTHOR)} ({E(AUTHOR_ROLE)}) and reviewed by our subject teachers. New explainers are added every Sunday and Wednesday.</p>
<div class="grid">{''.join(cards)}</div>
<section class="box"><h2>Practise next</h2><ul class="links">
<li><a href="../free-mock-papers.html">Free CBSE mock papers</a></li>
<li><a href="../formula-board/">Formula Board — quick revision cards</a></li>
<li><a href="../why-reels/">All WHY? reels</a></li></ul></section>
</main>
{FOOTER}
</body>
</html>
"""
    return head("Learn — WHY? explainers for CBSE Class 10 & 12 | CBSEMock", desc, url, ld, og_type="website") + "\n" + body


def main():
    OUT.mkdir(exist_ok=True)
    arts = live_articles()
    keep = {"index.html"}
    for a in arts:
        others = [o for o in arts if o is not a]
        same = [o for o in others if o["category"] == a["category"]]
        others = same + [o for o in others if o not in same]
        (OUT / f"{a['slug']}.html").write_text(article_page(a, others), encoding="utf-8")
        keep.add(f"{a['slug']}.html")
        v, _ = find_reel(a["reel"])
        if not v:
            print(f"[WARN] no reel video found for {a['slug']} ({a['reel']})")
    (OUT / "index.html").write_text(index_page(arts), encoding="utf-8")
    for f in OUT.glob("*.html"):
        if f.name not in keep:
            f.unlink()
    pending = [a["slug"] for a in ARTICLES if a not in arts]
    print(f"[ok] learn/: {len(arts)} live articles" + (f", {len(pending)} scheduled" if pending else ""))


if __name__ == "__main__":
    main()
