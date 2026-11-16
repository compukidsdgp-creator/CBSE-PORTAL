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

CAT_COLOR = {"Maths": "#3b6fb8", "AI": "#8b6bc2", "Computer Science": "#0e8aa8", "Physics": "#c18a45",
             "Chemistry": "#c0395f", "Biology": "#2b9a80", "Science": "#c18a45"}


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


IG_CACHE = OUT / "ig_links.json"
IG_PROFILE = "https://www.instagram.com/cbsemock/"


def ig_links():
    """{reel filename: instagram permalink} for WHY? reels already posted to Instagram.

    IDs come from formula-posts/why/why_log.csv; permalinks are looked up once with the Graph API
    (INSTAGRAM_ACCESS_TOKEN) and cached in learn/ig_links.json, so runs without the token keep them."""
    import csv, json, os, urllib.request, urllib.parse
    try:
        cache = json.loads(IG_CACHE.read_text())
    except Exception:
        cache = {}
    log = ROOT / "formula-posts/why/why_log.csv"
    token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")
    changed = False
    if log.exists():
        with open(log, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                mid, name = (row.get("ig_media_id") or "").strip(), row.get("filename", "")
                if row.get("dry_run") == "True" or not mid.isdigit() or name in cache or not token:
                    continue
                url = f"https://graph.facebook.com/v27.0/{mid}?" + urllib.parse.urlencode(
                    {"fields": "permalink", "access_token": token})
                try:
                    with urllib.request.urlopen(url, timeout=20) as r:
                        link = json.load(r).get("permalink", "")
                    if link.startswith("https://www.instagram.com/"):
                        cache[name] = link.split("?")[0]
                        changed = True
                except Exception as e:
                    print(f"[WARN] Instagram permalink for {name}: {e}")
    if changed:
        IG_CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True))
    return cache


def live_articles():
    arts = [a for a in ARTICLES if datetime.strptime(a["published"], "%Y-%m-%d").date() <= TODAY]
    return sorted(arts, key=lambda a: (a["published"], ARTICLES.index(a)), reverse=True)


CSS = """
:root{--navy:#1a3a6b;--navy2:#0f2347;--gold:#c9a227;--gold2:#e8cc6a;--bg:#f3f1ed;--card:#fff;--text:#1a1a1a;--muted:#5d5d5d;--border:#ddd8cc;--code:#f1eee6;
--grd:linear-gradient(135deg,#1a3a6b 0%,#0f2347 100%);}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--card:#161b22;--text:#e6edf3;--muted:#8b949e;--border:#30363d;--code:#1f2630;}}
*{box-sizing:border-box;margin:0;padding:0;}
body{font:16px/1.75 Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);}
.serif,h1,h2{font-family:'Crimson Pro',Georgia,serif;}
/* hero */
.hero{background:var(--grd);color:#fff;position:relative;overflow:hidden;padding:0 20px 34px;}
.hero::before{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/svg%3E");}
.hero::after{content:'';position:absolute;width:340px;height:340px;right:-120px;top:-140px;border-radius:50%;background:radial-gradient(circle,rgba(232,204,106,.22),transparent 70%);}
.hero>*{position:relative;z-index:1;}
.topbar{max-width:1040px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.12);}
.brand{color:#fff;text-decoration:none;font-weight:800;font-size:1.05rem;letter-spacing:.01em;}
.brand b{color:var(--gold2);}
.navbtns{display:flex;gap:8px;flex-wrap:wrap;}
.nb{color:#fff;text-decoration:none;font-size:.8rem;font-weight:600;padding:6px 13px;border-radius:99px;border:1px solid rgba(255,255,255,.28);transition:all .18s;}
.nb:hover{background:var(--gold);color:var(--navy2);border-color:var(--gold);transform:translateY(-2px);box-shadow:0 6px 16px rgba(201,162,39,.4);}
.hero-in{max-width:780px;margin:0 auto;padding-top:22px;}
.hero-in.wide{max-width:1040px;text-align:center;}
.crumb{font-size:.8rem;color:rgba(255,255,255,.7);margin-bottom:12px;}
.crumb a{color:var(--gold2);text-decoration:none;display:inline-block;padding:5px 0;}
.crumb a:hover{text-decoration:underline;}
h1{font-size:clamp(1.8rem,4.2vw,2.6rem);line-height:1.15;margin-bottom:14px;font-weight:700;}
h1 em{font-style:normal;color:var(--gold2);}
.badge{display:inline-block;background:var(--gold);color:var(--navy2);border-radius:20px;padding:4px 16px;font-size:.75rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;margin-bottom:14px;}
.meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:.8rem;}
.chip{padding:4px 12px;border-radius:99px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#fff;}
.pill{display:inline-block;padding:4px 12px;border-radius:99px;color:#fff;font-size:.75rem;font-weight:700;letter-spacing:.03em;}
.intro{color:rgba(255,255,255,.85);font-size:1rem;max-width:760px;margin:0 auto;}
/* page */
.wrap{max-width:780px;margin:0 auto;padding:0 20px 70px;}
.byline{display:flex;gap:12px;align-items:center;background:var(--card);border:1px solid var(--border);border-left:5px solid var(--gold);border-radius:14px;padding:13px 16px;margin:-20px 0 26px;position:relative;z-index:2;box-shadow:0 10px 26px rgba(15,35,71,.12);font-size:.9rem;}
.byline .av{flex:0 0 44px;height:44px;border-radius:50%;background:var(--grd);color:var(--gold2);display:flex;align-items:center;justify-content:center;font-weight:800;border:2px solid var(--gold);}
.byline small{color:var(--muted);display:block;line-height:1.45;}
.byline a{color:var(--navy);font-weight:600;}
.reel{float:right;width:250px;margin:4px 0 18px 26px;}
.reel video{width:100%;aspect-ratio:9/16;border-radius:16px;background:#000;display:block;border:3px solid var(--gold);box-shadow:0 0 0 6px rgba(201,162,39,.15),0 14px 30px rgba(15,35,71,.3);}
.igf{position:relative;width:100%;aspect-ratio:9/16;border-radius:16px;background:#000 center/cover no-repeat;cursor:pointer;border:3px solid var(--gold);box-shadow:0 0 0 6px rgba(201,162,39,.15),0 14px 30px rgba(15,35,71,.3);transition:transform .2s,box-shadow .2s;}
.igf:hover,.igf:focus{transform:translateY(-4px);box-shadow:0 0 0 6px rgba(201,162,39,.3),0 20px 36px rgba(15,35,71,.38);outline:none;}
.igplay{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:66px;height:66px;border-radius:50%;background:linear-gradient(45deg,#f9ce34,#ee2a7b,#6228d7);color:#fff;font-size:1.6rem;display:flex;align-items:center;justify-content:center;padding-left:5px;box-shadow:0 6px 20px rgba(0,0,0,.45);transition:transform .2s;}
.igf:hover .igplay{transform:translate(-50%,-50%) scale(1.12);}
.igbadge{position:absolute;left:50%;top:calc(50% + 46px);transform:translateX(-50%);white-space:nowrap;padding:3px 10px;border-radius:99px;background:rgba(0,0,0,.6);color:#fff;font-size:.75rem;font-weight:700;letter-spacing:.03em;}
.igbtn{display:block;margin-top:10px;text-align:center;padding:9px 12px;border-radius:12px;color:#fff;text-decoration:none;font-size:.8rem;font-weight:700;background:linear-gradient(45deg,#f9ce34,#ee2a7b,#6228d7);box-shadow:0 4px 12px rgba(238,42,123,.3);transition:transform .2s,box-shadow .2s;}
.igbtn:hover{transform:translateY(-3px);box-shadow:0 8px 20px rgba(238,42,123,.45);}
.reel .instagram-media{min-width:0!important;width:100%!important;margin:0!important;border-radius:14px!important;}
.reel p{font-size:.78rem;color:var(--muted);text-align:center;margin-top:8px;font-weight:600;}
article h2{font-size:1.55rem;margin:32px 0 10px;line-height:1.25;color:var(--navy);display:flex;align-items:center;gap:10px;}
article h2::before{content:'';flex:0 0 6px;height:24px;border-radius:3px;background:linear-gradient(180deg,var(--gold2),var(--gold));}
article p{margin:0 0 14px;}
article ul,article ol{margin:0 0 16px 22px;}
article li{margin:5px 0;}
article li::marker{color:var(--gold);font-weight:700;}
article b{color:var(--navy);}
article code{background:var(--code);padding:1px 6px;border-radius:5px;font-size:.9em;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;}
article pre{background:#0f2347;color:#e7e7f0;border-radius:12px;padding:14px 16px;overflow-x:auto;margin:0 0 18px;font-size:.85rem;line-height:1.55;clear:both;border-left:4px solid var(--gold);}
article pre code{background:none;padding:0;color:inherit;}
article table{border-collapse:collapse;width:100%;margin:0 0 18px;font-size:.92rem;clear:both;display:block;overflow-x:auto;border-radius:10px;}
article th,article td{border:1px solid var(--border);padding:8px 11px;text-align:left;}
article th{background:var(--navy);color:#fff;}
article tr:nth-child(odd) td{background:rgba(201,162,39,.06);}
@media(prefers-color-scheme:dark){article h2,article b,.byline a{color:var(--gold2);}}
/* boxes */
.box{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:22px 22px;margin:30px 0 0;clear:both;box-shadow:0 6px 18px rgba(15,35,71,.06);}
.box h2{font-size:1.45rem;margin:0 0 14px;color:var(--navy);}
@media(prefers-color-scheme:dark){.box h2{color:var(--gold2);}}
details{border:1.5px solid var(--border);border-radius:12px;padding:0;margin:10px 0;overflow:hidden;transition:border-color .18s,box-shadow .18s;}
details:hover{border-color:var(--gold);box-shadow:0 4px 14px rgba(201,162,39,.2);}
details[open]{border-color:var(--navy);}
summary{cursor:pointer;font-weight:600;padding:12px 16px;list-style:none;display:flex;gap:10px;align-items:flex-start;}
summary::-webkit-details-marker{display:none;}
summary::before{content:'Q';flex:0 0 24px;height:24px;border-radius:50%;background:var(--grd);color:var(--gold2);font-size:.75rem;font-weight:800;display:flex;align-items:center;justify-content:center;margin-top:2px;}
details[open] summary{background:linear-gradient(90deg,rgba(26,58,107,.08),transparent);}
details .ans{padding:4px 16px 14px 50px;color:var(--text);}
details .ans::before{content:'Answer: ';font-weight:700;color:#237d69;}
/* colourful link buttons */
.links{list-style:none;margin:0!important;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;}
.links a{--c1:#3b6fb8;--c2:#0f2347;position:relative;display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:58px;padding:12px 16px;border-radius:14px;text-decoration:none;color:#fff;font-weight:700;font-size:.9rem;line-height:1.35;background:linear-gradient(135deg,var(--c1),var(--c2));box-shadow:0 5px 0 rgba(10,28,54,.18),0 10px 18px rgba(10,28,54,.14);transition:transform .2s,box-shadow .2s,filter .2s;overflow:hidden;}
.links a::after{content:'→';flex:0 0 auto;width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,.18);display:flex;align-items:center;justify-content:center;color:var(--gold2);transition:transform .2s,background .2s,color .2s;}
.links a::before{content:'';position:absolute;inset:0;background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.25) 50%,transparent 70%);transform:translateX(-120%);transition:transform .55s;}
.links a:hover{transform:translateY(-4px);filter:saturate(1.15);box-shadow:0 9px 0 rgba(10,28,54,.14),0 18px 28px rgba(10,28,54,.24),0 0 0 3px var(--gold2);}
.links a:hover::before{transform:translateX(120%);}
.links a:hover::after{transform:translateX(4px);background:var(--gold);color:var(--navy2);}
.links li:nth-child(6n+1) a{--c1:#3b6fb8;--c2:#0f2347;}
.links li:nth-child(6n+2) a{--c1:#2b9a80;--c2:#12483e;}
.links li:nth-child(6n+3) a{--c1:#8b6bc2;--c2:#392653;}
.links li:nth-child(6n+4) a{--c1:#c18a45;--c2:#563318;}
.links li:nth-child(6n+5) a{--c1:#c0395f;--c2:#5a1228;}
.links li:nth-child(6n+6) a{--c1:#0e8aa8;--c2:#0b3d52;}
/* index cards */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px;margin-top:-22px;position:relative;z-index:2;}
.card{--c1:#3b6fb8;--c2:#0e2344;position:relative;display:flex;flex-direction:column;border-radius:18px;overflow:hidden;text-decoration:none;color:#fff;background:linear-gradient(145deg,var(--c1),var(--c2));border:1px solid rgba(255,255,255,.35);box-shadow:0 8px 0 rgba(10,28,54,.16),0 15px 26px rgba(10,28,54,.18),inset 0 1px 0 rgba(255,255,255,.35);transition:transform .22s,box-shadow .22s;}
.card:hover{transform:translateY(-7px) rotateX(2deg) rotateY(-1deg);box-shadow:0 13px 0 rgba(10,28,54,.13),0 25px 36px rgba(10,28,54,.26),0 0 0 3px var(--gold2);}
.card .th{aspect-ratio:16/10;background:#111 center 30%/cover no-repeat;position:relative;}
.card .th::after{content:'▶';position:absolute;right:12px;bottom:-18px;width:40px;height:40px;border-radius:50%;background:var(--gold);color:var(--navy2);display:flex;align-items:center;justify-content:center;font-size:.9rem;box-shadow:0 4px 12px rgba(0,0,0,.3);transition:transform .2s;}
.card:hover .th::after{transform:scale(1.15);}
.card .bd{padding:16px 16px 18px;display:flex;flex-direction:column;flex:1;}
.card .tag{display:inline-block;font-size:.75rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--gold2);}
.card b{display:block;font-family:'Crimson Pro',Georgia,serif;font-size:1.3rem;line-height:1.2;margin:6px 0 8px;}
.card span.d{font-size:.8rem;color:rgba(255,255,255,.82);line-height:1.5;}
.card .go{margin-top:auto;padding-top:14px;font-size:.75rem;font-weight:800;color:#ffe4a0;letter-spacing:.05em;}
.cat-Maths{--c1:#3b6fb8;--c2:#0e2344;}
.cat-AI{--c1:#8b6bc2;--c2:#392653;}
.cat-ComputerScience{--c1:#0e8aa8;--c2:#0b3d52;}
.cat-Physics,.cat-Science{--c1:#c18a45;--c2:#563318;}
.cat-Chemistry{--c1:#c0395f;--c2:#5a1228;}
.cat-Biology{--c1:#2b9a80;--c2:#12483e;}
footer{text-align:center;padding:26px 16px;font-size:.8rem;color:rgba(255,255,255,.7);background:var(--grd);margin-top:20px;}
footer a{color:var(--gold2);margin:0 2px;text-decoration:none;display:inline-block;padding:6px 4px;}
footer a:hover{text-decoration:underline;}
@media(max-width:640px){.reel{float:none;width:min(260px,72%);margin:0 auto 22px;}.navbtns .nb.hide-m{display:none;}.links{grid-template-columns:1fr;}}
"""

HEAD_TAGS = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2810600896966939" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>"""

FOOTER = """<footer>&copy; 2026 CBSEMock.org.in &nbsp;|&nbsp;
<a href="../about.html">About Us</a>|<a href="../privacy.html">Privacy Policy</a>|<a href="../terms.html">Terms of Use</a>|<a href="../contact.html">Contact</a>|<a href="../disclaimer.html">Disclaimer</a></footer>"""


IG_JS = """<script>
document.querySelectorAll('.igf').forEach(function(el){
  function go(){
    var u=el.getAttribute('data-ig'), b=document.createElement('blockquote');
    b.className='instagram-media'; b.setAttribute('data-instgrm-permalink',u+'?utm_source=ig_embed');
    b.setAttribute('data-instgrm-version','14'); b.innerHTML='<a href="'+u+'" target="_blank" rel="noopener">View this reel on Instagram</a>';
    el.replaceWith(b);
    if(window.instgrm){window.instgrm.Embeds.process();}
    else{var s=document.createElement('script');s.async=true;s.src='https://www.instagram.com/embed.js';document.body.appendChild(s);}
    try{gtag('event','ig_reel_play',{page_path:location.pathname});}catch(e){}
  }
  el.addEventListener('click',go);
  el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});
});
</script>"""


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
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@600;700&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ldjson, ensure_ascii=False)}</script>
{HEAD_TAGS}
</head>"""


def nice_date(s):
    d = datetime.strptime(s, "%Y-%m-%d")
    return f"{d.day} {d:%B %Y}"


def article_page(a, others, ig):
    url = f"{SITE}/learn/{a['slug']}.html"
    video, thumb = find_reel(a["reel"])
    ig_url = ig.get(Path(video).name, "") if video else ""
    color = CAT_COLOR.get(a["category"], "#2d6a4f")
    pub = a["published"]
    upd = a.get("updated", pub)
    words = len(re.sub(r"<[^>]+>", " ", a["body"]).split())
    author_name = a.get("author", AUTHOR)              # the article's real author / responsible editor
    author = {"@type": "Person", "name": author_name, "url": SITE + "/about.html"}
    author_role = a.get("author_role", AUTHOR_ROLE if author_name == AUTHOR else "Subject teacher, CBSEMock")
    author["jobTitle"] = author_role
    initials = "".join(w[0] for w in author_name.split()[:2]).upper()
    graph = [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": a["title"], "description": a["description"],
         "inLanguage": "en-IN", "isPartOf": {"@id": SITE + "/#website"}, "breadcrumb": {"@id": url + "#breadcrumb"},
         "datePublished": pub, "dateModified": upd,
         **({"primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}/{thumb}"}} if thumb else {})},
        {"@type": "Article", "@id": url + "#article", "headline": a["h1"], "description": a["description"], "url": url,
         "mainEntityOfPage": {"@id": url + "#webpage"}, "isPartOf": {"@id": SITE + "/learn/#collection"},
         "datePublished": pub, "dateModified": upd, "wordCount": words,
         "inLanguage": "en-IN", "articleSection": a["category"],
         "educationalLevel": "CBSE " + a["class_label"], "isAccessibleForFree": True,
         "author": author,
         "publisher": {"@type": "Organization", "@id": SITE + "/#organization", "name": "CBSEMOCK", "url": SITE + "/",
                       "logo": {"@type": "ImageObject", "url": SITE + "/og-image.jpg"}},
         **({"image": [f"{SITE}/{thumb}"]} if thumb else {}),
         **({"video": {"@id": url + "#video"}} if video else {})},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Learn", "item": SITE + "/learn/"},
            {"@type": "ListItem", "position": 3, "name": a["h1"], "item": url}]},
    ]
    if video:
        graph.append({"@type": "VideoObject", "@id": url + "#video", "name": a["h1"], "description": a["description"],
                      "thumbnailUrl": [f"{SITE}/{thumb}"] if thumb else [SITE + "/og-image.jpg"],
                      "uploadDate": pub + "T18:30:00+05:30", "contentUrl": f"{SITE}/{video}"})
    ld = {"@context": "https://schema.org", "@graph": graph}

    reel = ""
    if ig_url:
        bg = f' style="background-image:url(../{thumb})"' if thumb else ""
        reel = (f'<figure class="reel"><div class="igf" data-ig="{E(ig_url)}" role="button" tabindex="0" '
                f'aria-label="Play the reel on Instagram"{bg}><span class="igplay">▶</span>'
                f'<span class="igbadge">Instagram</span></div>'
                f'<a class="igbtn" href="{E(ig_url)}" target="_blank" rel="noopener">Watch &amp; follow on Instagram ↗</a></figure>')
    elif video:
        poster = f' poster="../{thumb}"' if thumb else ""
        reel = (f'<figure class="reel"><video controls playsinline preload="none"'
                f'{poster} src="../{video}" title="{E(a["h1"])}"></video>'
                f'<p>▶ Watch the WHY? reel</p></figure>')
    practice = "".join(f"<details><summary>{E(q)}</summary><p class=\"ans\">{E(ans)}</p></details>"
                       for q, ans in a.get("practice", []))
    related = "".join(f'<li><a href="../{h}">{E(l)}</a></li>' for l, h in a.get("related", []))
    related += '<li><a href="../why-reels/">All WHY? reels</a></li>'
    more = "".join(f'<li><a href="{o["slug"]}.html">{E(o["h1"])}</a></li>' for o in others[:4])

    body = f"""<body>
<header class="hero"><div class="topbar"><a class="brand" href="../index.html">CBSE<b>Mock</b></a><nav class="navbtns"><a class="nb" href="./">📘 Learn</a><a class="nb" href="../why-reels/">🤔 WHY? Reels</a><a class="nb hide-m" href="../free-mock-papers.html">📝 Mock Papers</a></nav></div>
<div class="hero-in"><nav class="crumb"><a href="../index.html">Home</a> › <a href="./">Learn</a> › {E(a['category'])}</nav>
<span class="badge">🤔 WHY? explainer</span>
<h1>{E(a['h1'])}</h1>
<div class="meta"><span class="pill" style="background:{color}">{E(a['category'])}</span><span class="chip">CBSE {E(a['class_label'])}</span><span class="chip">⏱ {a.get('read_min', 5)} min read</span><span class="chip">Updated {nice_date(upd)}</span></div></div>
</header>
<main class="wrap">
<article>
<div class="byline"><div class="av" aria-hidden="true">{E(initials)}</div><div><b>{E(author_name)}</b> · {E(author_role)}<small>{"20 years of teaching · " if author_name == AUTHOR else ""}Reviewed by subject teachers · <a href="../about.html">About us</a></small></div></div>
{reel}
{a['body'].strip()}
</article>
{f'<section class="box"><h2>Try it yourself</h2>{practice}</section>' if practice else ''}
<section class="box"><h2>Practise this topic</h2><ul class="links">{related}</ul></section>
{f'<section class="box"><h2>More WHY? explainers</h2><ul class="links">{more}</ul></section>' if more else ''}
</main>
{FOOTER}
{IG_JS if ig_url else ""}
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
        {"@type": "CollectionPage", "@id": url + "#collection", "name": "Learn — WHY? explainers", "url": url,
         "description": desc, "inLanguage": "en-IN", "isPartOf": {"@id": SITE + "/#website"},
         "publisher": {"@id": SITE + "/#organization"},
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/learn/{a['slug']}.html", "name": a["h1"]}
             for i, a in enumerate(arts)]}}]}
    cards = []
    for a in arts:
        _, thumb = find_reel(a["reel"])
        color = CAT_COLOR.get(a["category"], "#2d6a4f")
        bg = f' style="background-image:url(../{thumb})"' if thumb else ""
        cat = "cat-" + a["category"].replace(" ", "")
        cards.append(f'<a class="card {cat}" href="{a["slug"]}.html"><div class="th"{bg}></div><div class="bd">'
                     f'<span class="tag">{E(a["category"])} · CBSE {E(a["class_label"])}</span>'
                     f'<b>{E(a["h1"])}</b><span class="d">{E(a["description"])}</span>'
                     f'<span class="go">READ &amp; WATCH →</span></div></a>')
    body = f"""<body>
<header class="hero" style="padding-bottom:56px"><div class="topbar"><a class="brand" href="../index.html">CBSE<b>Mock</b></a><nav class="navbtns"><a class="nb" href="./">📘 Learn</a><a class="nb" href="../why-reels/">🤔 WHY? Reels</a><a class="nb hide-m" href="../free-mock-papers.html">📝 Mock Papers</a></nav></div>
<div class="hero-in wide"><nav class="crumb"><a href="../index.html">Home</a> › Learn</nav>
<span class="badge">📘 New every Sun &amp; Wed</span>
<h1>Learn: the <em>WHY?</em> behind CBSE concepts</h1>
<p class="intro">Board questions reward students who understand <i>why</i> a formula or idea works, not just what it says. Each explainer here takes one concept from the Class 10 or Class 12 syllabus, explains it step by step with a worked example and common mistakes, and ends with practice questions. Every article comes with a short WHY? reel. Written by {E(AUTHOR)} ({E(AUTHOR_ROLE)}) and reviewed by our subject teachers. New explainers are added every Sunday and Wednesday.</p></div>
</header>
<main class="wrap" style="max-width:1040px">
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


# ── cross-links: home-page strip + "explained" links on related chapter / portal pages ──────
GRAD = {"Maths": ("#3b6fb8", "#0e2344"), "AI": ("#8b6bc2", "#392653"), "Computer Science": ("#0e8aa8", "#0b3d52"),
        "Physics": ("#c18a45", "#563318"), "Science": ("#c18a45", "#563318"), "Chemistry": ("#c0395f", "#5a1228"),
        "Biology": ("#2b9a80", "#12483e")}
HS, HE = "<!-- LEARN-STRIP:START -->", "<!-- LEARN-STRIP:END -->"
LS, LE = "<!-- LEARN-LINKS:START -->", "<!-- LEARN-LINKS:END -->"
LOCKED = {"resources/physics-xii-new.html"}          # never modified


def home_strip(arts):
    cards = []
    for a in arts[:3]:
        _, thumb = find_reel(a["reel"])
        c1, c2 = GRAD.get(a["category"], GRAD["Maths"])
        img = f'<span class="lrn-th" style="background-image:url({thumb})"></span>' if thumb else ""
        cards.append(f'<a class="lrn-card" href="learn/{a["slug"]}.html" style="background:linear-gradient(145deg,{c1},{c2})">'
                     f'{img}<span class="lrn-bd"><span class="lrn-tag">{E(a["category"])} · CBSE {E(a["class_label"])}</span>'
                     f'<span class="lrn-t">{E(a["h1"])}</span><span class="lrn-go">READ &amp; WATCH →</span></span></a>')
    return f"""{HS}
<style>
.lrn{{max-width:1100px;margin:30px auto 10px;padding:0 20px;}}
.lrn-head{{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:14px;}}
.lrn-head h2{{font-family:'Crimson Pro',serif;color:var(--gold,#c9a227);font-size:clamp(1.45rem,2.8vw,1.85rem);margin:0;}}
.lrn-head p{{color:var(--muted,#666);font-size:.86rem;margin:2px 0 0;}}
.lrn-all{{display:inline-block;padding:9px 18px;border-radius:99px;background:linear-gradient(135deg,#1a3a6b,#0f2347);color:#ffe4a0;font-weight:800;font-size:.78rem;letter-spacing:.04em;text-decoration:none;border:1.5px solid #c9a227;transition:transform .18s,box-shadow .18s,background .18s;}}
.lrn-all:hover{{transform:translateY(-3px);background:#c9a227;color:#0f2347;box-shadow:0 8px 18px rgba(201,162,39,.45);}}
.lrn-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;}}
.lrn-card{{display:flex;border-radius:18px;overflow:hidden;text-decoration:none;color:#fff;min-height:150px;border:1px solid rgba(255,255,255,.35);box-shadow:0 8px 0 rgba(10,28,54,.16),0 15px 26px rgba(10,28,54,.18);transition:transform .22s,box-shadow .22s;}}
.lrn-card:hover{{transform:translateY(-6px);box-shadow:0 13px 0 rgba(10,28,54,.13),0 24px 34px rgba(10,28,54,.26),0 0 0 3px #e8cc6a;}}
.lrn-th{{flex:0 0 96px;background:#111 center 25%/cover no-repeat;}}
.lrn-bd{{display:flex;flex-direction:column;padding:14px 16px;}}
.lrn-tag{{font-size:.75rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#ffe4a0;}}
.lrn-t{{font-family:'Crimson Pro',serif;font-size:1.18rem;font-weight:700;line-height:1.2;margin:6px 0 10px;}}
.lrn-go{{margin-top:auto;font-size:.75rem;font-weight:800;color:#ffe4a0;letter-spacing:.05em;}}
@media(max-width:860px){{.lrn-grid{{grid-template-columns:1fr;}}.lrn-card{{min-height:120px;}}}}
</style>
<section class="lrn" aria-label="Latest Learn explainers">
<div class="lrn-head"><div><h2>📘 Learn: the WHY? behind CBSE concepts</h2><p>Short explainers with a reel, a worked example and practice questions — new every Sunday &amp; Wednesday.</p></div>
<a class="lrn-all" href="learn/">ALL EXPLAINERS →</a></div>
<div class="lrn-grid">{''.join(cards)}</div>
</section>
{HE}"""


def update_home(arts):
    f = ROOT / "index.html"
    s = f.read_text(encoding="utf-8")
    block = home_strip(arts)
    if HS in s:
        s = s[:s.index(HS)] + block + s[s.index(HE) + len(HE):]
    else:                                    # first run: right after the Learning Zones section
        i = s.index('<div class="zone-launch-grid"')
        j = s.index("</section>", i) + len("</section>")
        s = s[:j] + "\n\n" + block + s[j:]
    f.write_text(s, encoding="utf-8")


def update_backlinks(arts):
    """Add 'Explained simply' links to pages each live article points to (chapter quizzes / portals)."""
    want = {}
    for a in arts:
        for _, h in a.get("related", []):
            if h.endswith(".html") and (h.startswith("chapters/") or "/" not in h) and h not in LOCKED:
                want.setdefault(h, []).append(a)
    pages = set(want)
    for f in list(ROOT.glob("chapters/*.html")) + list(ROOT.glob("cbse-class-*.html")):
        rel = str(f.relative_to(ROOT))
        if rel not in LOCKED and LS in f.read_text(encoding="utf-8"):
            pages.add(rel)
    n = 0
    for rel in sorted(pages):
        f = ROOT / rel
        if not f.exists() or rel in LOCKED:
            continue
        s = f.read_text(encoding="utf-8")
        if LS in s:
            s = s[:s.index(LS)] + s[s.index(LE) + len(LE):].lstrip("\n")
        items = want.get(rel, [])
        if items:
            pre = "../" if rel.startswith("chapters/") else ""
            links = "".join(f'<li><a href="{pre}learn/{a["slug"]}.html">{E(a["h1"])}</a></li>' for a in items[:4])
            block = (f'{LS}\n<div class="sc-card lrn-x"><h2>📘 Explained simply</h2>'
                     f'<p style="margin-bottom:8px;color:var(--muted,#666)">Short WHY? explainers on ideas from this topic, each with a reel and practice questions.</p>'
                     f'<ul style="margin:0 0 0 18px;line-height:1.9;font-weight:600">{links}</ul>'
                     f'<p style="margin-top:8px"><a href="{pre}learn/" style="display:inline-block;padding:7px 16px;border-radius:99px;background:linear-gradient(135deg,#1a3a6b,#0f2347);color:#ffe4a0;font-weight:800;font-size:.8rem;text-decoration:none;border:1.5px solid #c9a227">All Learn explainers →</a></p></div>\n{LE}\n')
            if "<!-- STATIC-CONTENT:END -->" in s and '<p class="sc-meta">' in s:
                k = s.rindex('<p class="sc-meta">', 0, s.index("<!-- STATIC-CONTENT:END -->"))
                s = s[:k] + block + s[k:]
            else:
                print(f"[WARN] no static-content block in {rel}; skipped")
                continue
            n += 1
        f.write_text(s, encoding="utf-8")
    print(f"[ok] Learn links on {n} related pages")


def main():
    OUT.mkdir(exist_ok=True)
    arts = live_articles()
    ig = ig_links()
    keep = {"index.html"}
    for a in arts:
        others = [o for o in arts if o is not a]
        same = [o for o in others if o["category"] == a["category"]]
        others = same + [o for o in others if o not in same]
        (OUT / f"{a['slug']}.html").write_text(article_page(a, others, ig), encoding="utf-8")
        keep.add(f"{a['slug']}.html")
        v, _ = find_reel(a["reel"])
        if not v:
            print(f"[WARN] no reel video found for {a['slug']} ({a['reel']})")
    (OUT / "index.html").write_text(index_page(arts), encoding="utf-8")
    update_home(arts)
    update_backlinks(arts)
    for f in OUT.glob("*.html"):
        if f.name not in keep:
            f.unlink()
    pending = [a["slug"] for a in ARTICLES if a not in arts]
    print(f"[ok] learn/: {len(arts)} live articles" + (f", {len(pending)} scheduled" if pending else ""))


if __name__ == "__main__":
    main()
