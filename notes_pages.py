"""Chapter notes pages: notes/class-<N>/<subject>/<chapter>.html, one page per chapter.

Content lives in notes_content/<class><N>_<subject>/<module>.py as a CHAPTER dict. A chapter with
status "draft" is a hidden preview (noindex, unlinked, out of the sitemap) until it is approved; "live"
publishes it normally.            python3 notes_pages.py            (builds every chapter)
"""
import html
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "notes_content"
OUT = ROOT / "notes"
SITE = "https://cbsemock.org.in"
E = html.escape
AUTHOR, AUTHOR_ROLE = "Biswarup Mukherjee", "Teaching Administrator, CBSEMock"


def load_chapters():
    try:
        approvals = json.loads((SRC / "approvals.json").read_text(encoding="utf-8"))
    except Exception:
        approvals = {}
    out = []
    for f in sorted(SRC.glob("*/*.py")):
        if f.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f"nc_{f.parent.name}_{f.stem}", f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        ch = dict(m.CHAPTER); ch["_src"] = str(f.relative_to(ROOT))
        ch["_id"] = f"class{ch['class']}/{ch['subject_slug']}/{ch['slug']}"
        appr = approvals.get(ch["_id"], {})
        if appr.get("status") == "approved":       # approved in the admin panel → publish
            ch["status"] = "live"
            ch["updated"] = max(ch.get("updated", ""), appr.get("at", "")[:10])
        out.append(ch)
    return out


CSS = """
:root{--navy:#1a3a6b;--navy2:#0f2347;--gold:#c9a227;--gold2:#e8cc6a;--bg:#f3f1ed;--card:#fff;--text:#1a1a1a;--muted:#5d5d5d;--border:#ddd8cc;--code:#f1eee6;--grd:linear-gradient(135deg,#1a3a6b 0%,#0f2347 100%);}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--card:#161b22;--text:#e6edf3;--muted:#8b949e;--border:#30363d;--code:#1f2630;}}
*{box-sizing:border-box;margin:0;padding:0}
body{font:16.5px/1.75 Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text)}
h1,h2,h3{font-family:'Crimson Pro',Georgia,serif}
.hero{background:var(--grd);color:#fff;position:relative;overflow:hidden;padding:0 20px 40px}
.hero::after{content:'';position:absolute;width:360px;height:360px;right:-130px;top:-150px;border-radius:50%;background:radial-gradient(circle,rgba(232,204,106,.22),transparent 70%)}
.hero>*{position:relative;z-index:1}
.topbar{max-width:1080px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.12)}
.brand{color:#fff;text-decoration:none;font-weight:800;font-size:1.05rem}.brand b{color:var(--gold2)}
.navbtns{display:flex;gap:8px;flex-wrap:wrap}
.nb{color:#fff;text-decoration:none;font-size:.8rem;font-weight:600;padding:7px 13px;border-radius:99px;border:1px solid rgba(255,255,255,.28);transition:all .18s}
.nb:hover{background:var(--gold);color:var(--navy2);border-color:var(--gold);transform:translateY(-2px)}
.hero-in{max-width:1080px;margin:0 auto;padding-top:22px}
.crumb{font-size:.8rem;color:rgba(255,255,255,.72);margin-bottom:12px}.crumb a{color:var(--gold2);text-decoration:none;display:inline-block;padding:5px 0}
.badge{display:inline-block;background:var(--gold);color:var(--navy2);border-radius:20px;padding:4px 16px;font-size:.75rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;margin-bottom:12px}
h1{font-size:clamp(1.9rem,4.4vw,2.8rem);line-height:1.12;margin-bottom:12px}
.meta{display:flex;flex-wrap:wrap;gap:8px;font-size:.8rem}
.chip{padding:4px 12px;border-radius:99px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2)}
.draft{max-width:1080px;margin:16px auto 0;overflow-wrap:anywhere;background:#fff4d6;color:#6b4e00;border:1.5px dashed #c9a227;border-radius:12px;padding:10px 14px;font-size:.88rem;font-weight:600}
.layout{max-width:1080px;margin:0 auto;padding:0 20px 70px;display:grid;grid-template-columns:230px minmax(0,1fr);gap:34px}
.toc{position:sticky;top:16px;align-self:start;margin-top:26px;background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px 14px 10px;font-size:.84rem}
.toc b{display:block;font-size:.75rem;letter-spacing:.06em;text-transform:uppercase;color:var(--gold);margin-bottom:6px}
.toc a{display:block;color:var(--text);text-decoration:none;padding:6px 8px;border-radius:8px;line-height:1.35}
.toc a:hover{background:rgba(201,162,39,.14);color:var(--navy)}
main{min-width:0}
.byline{display:flex;gap:12px;align-items:center;background:var(--card);border:1px solid var(--border);border-left:5px solid var(--gold);border-radius:14px;padding:13px 16px;margin:-22px 0 22px;position:relative;z-index:2;box-shadow:0 10px 26px rgba(15,35,71,.12);font-size:.9rem}
.byline .av{flex:0 0 44px;height:44px;border-radius:50%;background:var(--grd);color:var(--gold2);display:flex;align-items:center;justify-content:center;font-weight:800;border:2px solid var(--gold)}
.byline small{display:block;color:var(--muted);line-height:1.45}
section{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:24px 26px;margin:0 0 22px;box-shadow:0 6px 18px rgba(15,35,71,.05)}
section>h2{font-size:1.65rem;color:var(--navy);margin-bottom:12px;display:flex;align-items:center;gap:10px;line-height:1.2}
section>h2::before{content:'';flex:0 0 6px;height:26px;border-radius:3px;background:linear-gradient(180deg,var(--gold2),var(--gold))}
h3{font-size:1.32rem;color:var(--navy);margin:22px 0 8px;line-height:1.25}
h3:first-of-type{margin-top:4px}
@media(prefers-color-scheme:dark){section>h2,h3,b{color:var(--gold2)}}
p{margin:0 0 12px}ul,ol{margin:0 0 14px 22px}li{margin:5px 0}li::marker{color:var(--gold);font-weight:700}
b{color:var(--navy)}
.eq{font-family:'Cambria Math','STIX Two Math',Georgia,serif;font-size:1.12rem;background:var(--code);border-left:4px solid var(--gold);border-radius:8px;padding:9px 14px;margin:6px 0 14px;overflow-x:auto;white-space:nowrap}
.cond{font-size:.75rem;vertical-align:super;color:var(--muted);margin:0 2px}
figure.diag{margin:18px 0;background:#fff;border:1px solid var(--border);border-radius:14px;padding:12px}
figure.diag svg{width:100%;height:auto;display:block}
figure.diag figcaption{font-size:.88rem;color:#444;margin-top:6px;text-align:center}
table{border-collapse:collapse;width:100%;font-size:.93rem;display:block;overflow-x:auto}
th,td{border:1px solid var(--border);padding:9px 11px;text-align:left;vertical-align:top}
th{background:var(--navy);color:#fff;font-weight:700}
tr:nth-child(even) td{background:rgba(201,162,39,.06)}
td.f{font-family:'Cambria Math',Georgia,serif;white-space:nowrap}
.wk{border:1.5px solid var(--border);border-radius:14px;margin:12px 0;overflow:hidden}
.wk summary{cursor:pointer;list-style:none;padding:13px 16px;font-weight:700;display:flex;gap:10px}
.wk summary::-webkit-details-marker{display:none}
.wk summary::before{content:'Q';flex:0 0 26px;height:26px;border-radius:50%;background:var(--grd);color:var(--gold2);font-size:.8rem;display:flex;align-items:center;justify-content:center}
.wk[open]{border-color:var(--navy)}.wk:hover{border-color:var(--gold)}
.wk .body{padding:2px 18px 14px 52px}
.ans{background:rgba(35,125,105,.08);border-left:4px solid #237d69;border-radius:8px;padding:9px 12px}
.mist td:nth-child(2){color:#b42318}.mist td:nth-child(3){color:#237d69}
.rev{background:linear-gradient(135deg,#fffaf0,#fff);border:2px solid var(--gold)}
@media(prefers-color-scheme:dark){.rev{background:var(--card)}figure.diag figcaption{color:#444}}
.rev ol{columns:2;column-gap:30px}@media(max-width:760px){.rev ol{columns:1}}
.links{list-style:none;margin:0!important;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.links a{--c1:#3b6fb8;--c2:#0f2347;display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:56px;padding:12px 16px;border-radius:14px;text-decoration:none;color:#fff;font-weight:700;font-size:.9rem;background:linear-gradient(135deg,var(--c1),var(--c2));box-shadow:0 5px 0 rgba(10,28,54,.18);transition:transform .2s,box-shadow .2s}
.links a::after{content:'→';color:var(--gold2)}
.links a:hover{transform:translateY(-4px);box-shadow:0 9px 0 rgba(10,28,54,.14),0 0 0 3px var(--gold2)}
.links li:nth-child(4n+2) a{--c1:#2b9a80;--c2:#12483e}.links li:nth-child(4n+3) a{--c1:#8b6bc2;--c2:#392653}.links li:nth-child(4n+4) a{--c1:#c18a45;--c2:#563318}
footer{text-align:center;padding:26px 16px;font-size:.8rem;color:rgba(255,255,255,.7);background:var(--grd)}
footer a{color:var(--gold2);text-decoration:none;display:inline-block;padding:6px 4px}
@media(max-width:860px){.layout{grid-template-columns:1fr;gap:0}.toc{position:static;margin:0 0 18px}.byline{margin-top:-22px}section{padding:20px 18px}}
@media print{.hero,.toc,footer,.links,.draft{display:none}body{background:#fff}section{box-shadow:none;break-inside:avoid}}
"""


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def page(ch):
    cls, subj = ch["class"], ch["subject"]
    rel = f"notes/class-{cls}/{ch['subject_slug']}/{ch['slug']}.html"
    url = f"{SITE}/{rel}"
    up = "../../../"
    draft = ch.get("status") != "live"
    secs = [("glance", "At a glance"), ("concepts", "Concepts, step by step"), ("diagrams", "Diagrams to learn"),
            ("formulas", "Key equations and definitions"), ("worked", "Worked board questions"),
            ("mistakes", "Common mistakes"), ("revision", "Quick revision"), ("practise", "Practise this chapter")]
    toc = "".join(f'<a href="#{k}">{E(t)}</a>' for k, t in secs)
    concepts = "".join(f'<h3 id="{slugify(t)}">{E(t)}</h3>{b.strip()}' for t, b in ch["concepts"])
    diagrams = "".join(f'<figure class="diag" id="fig-{k}">{svg.strip()}<figcaption>Fig. {i + 1}: {E(cap)}</figcaption></figure>'
                       for i, (k, cap, svg) in enumerate(ch["diagrams"]))
    formulas = ("<table><tr><th>Type</th><th>General form</th><th>Example</th></tr>" +
                "".join(f"<tr><td><b>{E(a)}</b></td><td class=\"f\">{E(b)}</td><td class=\"f\">{E(c)}</td></tr>" for a, b, c in ch["formulas"])
                + "</table>")
    worked = "".join(f'<details class="wk"><summary>{E(q)}</summary><div class="body">{a.strip()}</div></details>' for q, a in ch["worked"])
    mistakes = ('<table class="mist"><tr><th>Mistake</th><th>What students write</th><th>Write this instead</th></tr>' +
                "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in ch["mistakes"]) + "</table>")
    revision = "<ol>" + "".join(f"<li>{E(x)}</li>" for x in ch["revision"]) + "</ol>"
    links = "".join(f'<li><a href="{up}{h}">{E(l)}</a></li>' for h, l in ch["practice"])
    words = len(re.sub(r"<[^>]+>", " ", ch["glance"] + "".join(b for _, b in ch["concepts"])).split())
    title = f"{ch['title']} Class {cls} Notes | CBSE {subj} Chapter {ch['number']}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article", "headline": f"{ch['title']} — Class {cls} {subj} notes",
         "description": ch["description"], "url": url, "mainEntityOfPage": url, "inLanguage": "en-IN",
         "datePublished": ch["updated"], "dateModified": ch["updated"], "wordCount": words,
         "educationalLevel": f"CBSE Class {cls}", "articleSection": subj, "isAccessibleForFree": True,
         "author": {"@type": "Person", "name": ch.get("author", AUTHOR), "url": SITE + "/about.html"},
         "publisher": {"@type": "Organization", "@id": SITE + "/#organization", "name": "CBSEMOCK", "url": SITE + "/",
                       "logo": {"@type": "ImageObject", "url": SITE + "/og-image.jpg"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": f"Class {cls} {subj} notes", "item": f"{SITE}/notes/class-{cls}/{ch['subject_slug']}/"},
            {"@type": "ListItem", "position": 3, "name": ch["title"], "item": url}]}]}
    robots = '<meta name="robots" content="noindex, nofollow">' if draft else ""
    draft_bar = (f'<div class="draft">Draft preview — hidden from Google and not linked from the site. '
                 f'Approve it in the admin panel to publish. (Source: {E(ch["_src"])})</div>') if draft else ""
    return rel, f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(ch['description'])}">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(ch['description'])}"><meta property="og:url" content="{url}"><meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@600;700&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{'' if draft else '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2810600896966939" crossorigin="anonymous"></script>'}
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>
</head>
<body>
<header class="hero">
<div class="topbar"><a class="brand" href="{up}index.html">CBSE<b>Mock</b></a><nav class="navbtns"><a class="nb" href="{up}cbse-class-{cls}-science-mock-tests.html">📝 Mock tests</a><a class="nb" href="{up}learn/">📘 Learn</a><a class="nb" href="{up}formula-board/">🧮 Formulas</a></nav></div>
<div class="hero-in"><nav class="crumb"><a href="{up}index.html">Home</a> › <a href="{up}study-zone/index.html">Notes</a> › <a href="./">Class {cls} {E(subj)} chapter notes</a></nav>
<span class="badge">Chapter {ch['number']} · Class {cls} {E(subj)}</span>
<h1>{E(ch['title'])}</h1>
<div class="meta"><span class="chip">{E(ch.get('unit', ''))}</span><span class="chip">CBSE 2026–27 syllabus</span><span class="chip">~{max(5, words // 200)} min read</span></div></div>
{draft_bar}
</header>
<div class="layout">
<nav class="toc" aria-label="On this page"><b>On this page</b>{toc}</nav>
<main>
<div class="byline"><div class="av" aria-hidden="true">BM</div><div><b>{E(ch.get('author', AUTHOR))}</b> · {E(AUTHOR_ROLE)}<small>Reviewed by subject teachers · Updated {E(ch['updated'])} · <a href="{up}about.html">About us</a></small></div></div>
<section id="glance"><h2>At a glance</h2>{ch['glance'].strip()}</section>
<section id="concepts"><h2>Concepts, step by step</h2>{concepts}</section>
<section id="diagrams"><h2>Diagrams to learn</h2><p>These are the figures most often asked to be drawn or labelled. Practise drawing them neatly with labels.</p>{diagrams}</section>
<section id="formulas"><h2>Key equations and definitions</h2>{formulas}</section>
<section id="worked"><h2>Worked board questions</h2><p>Try each question first, then open it to check the model answer.</p>{worked}</section>
<section id="mistakes"><h2>Common mistakes</h2>{mistakes}</section>
<section id="revision" class="rev"><h2>Quick revision</h2>{revision}</section>
<section id="practise"><h2>Practise this chapter</h2><ul class="links">{links}</ul></section>
</main>
</div>
<footer>&copy; 2026 CBSEMock.org.in · <a href="{up}about.html">About Us</a> · <a href="{up}privacy.html">Privacy Policy</a> · <a href="{up}terms.html">Terms of Use</a> · <a href="{up}contact.html">Contact</a></footer>
</body>
</html>
"""


def subject_index(key, chapters):
    """notes/class-N/<subject>/index.html: every syllabus chapter, linked once its notes are live."""
    import syllabus
    s = next((x for x in syllabus.SUBJECTS if x["key"] == key), None)
    if not s:
        return None
    cls, subj_slug = s["class"], key.split("/", 1)[1]
    live = {c["slug"]: c for c in chapters if c.get("status") == "live"}
    rel = f"notes/class-{cls}/{subj_slug}/index.html"
    url = f"{SITE}/notes/class-{cls}/{subj_slug}/"
    up = "../../../"
    items = []
    for num, title, _ in s["chapters"]:
        slug = syllabus.slugify(title)
        if not re.match(r"^[a-z0-9-]+$", slug):
            slug = f"chapter-{num}"
        if slug in live:
            items.append(f'<li><a class="chl live" href="{slug}.html"><span class="no">{num}</span><span>{E(title)}</span><b>Read →</b></a></li>')
        else:
            items.append(f'<li><div class="chl"><span class="no">{num}</span><span>{E(title)}</span><em>coming soon</em></div></li>')
    name = f"Class {cls} {s['name']}"
    hub = s["hubs"][0]
    desc = f"Chapter-wise CBSE {name} notes for 2026–27: concepts, labelled diagrams, worked board questions, common mistakes and quick revision."
    robots = "" if live else '<meta name="robots" content="noindex, follow">'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": f"{name} chapter notes", "url": url, "description": desc, "inLanguage": "en-IN",
         "isPartOf": {"@id": SITE + "/#website"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": f"{name} chapter notes", "item": url}]}]}
    extra = """
.chlist{list-style:none;margin:0!important;display:grid;gap:10px}
.chl{display:flex;align-items:center;gap:14px;padding:13px 16px;border:1.5px solid var(--border);border-radius:14px;background:var(--card);color:var(--muted);text-decoration:none}
.chl .no{flex:0 0 34px;height:34px;border-radius:50%;background:var(--code);display:flex;align-items:center;justify-content:center;font-weight:800;color:var(--navy)}
.chl span:nth-child(2){flex:1}.chl em{font-size:.8rem;font-style:normal}
a.chl.live{color:var(--text);border-color:var(--gold);transition:transform .18s,box-shadow .18s}
a.chl.live .no{background:var(--grd);color:var(--gold2)}a.chl.live b{color:var(--navy);white-space:nowrap}
a.chl.live:hover{transform:translateY(-3px);box-shadow:0 8px 20px rgba(15,35,71,.15),0 0 0 2px var(--gold2)}
.wrap1{max-width:860px;margin:0 auto;padding:26px 20px 70px}
"""
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(name)} Chapter-wise Notes 2026–27 | CBSEMock</title>
<meta name="description" content="{E(desc)}">
{robots}
<link rel="canonical" href="{url}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@600;700&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}{extra}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>
</head>
<body>
<header class="hero">
<div class="topbar"><a class="brand" href="{up}index.html">CBSE<b>Mock</b></a><nav class="navbtns"><a class="nb" href="{up}{hub}">📒 {E(s['name'])} notes page</a><a class="nb" href="{up}learn/">📘 Learn</a></nav></div>
<div class="hero-in"><nav class="crumb"><a href="{up}index.html">Home</a> › <a href="{up}study-zone/index.html">Notes</a> › {E(name)}</nav>
<span class="badge">CBSE 2026–27 syllabus</span>
<h1>{E(name)} — chapter notes</h1>
<div class="meta"><span class="chip">{len(live)} of {len(s['chapters'])} chapters ready</span><span class="chip">New chapters added regularly</span></div></div>
</header>
<main class="wrap1">
<section><h2>Chapters</h2><p>Each chapter has the concepts in order, labelled diagrams, worked board questions, common mistakes and a quick-revision box. For tests, flashcards and past-year questions, open the <a href="{up}{hub}">{E(s['name'])} notes page</a>.</p>
<ul class="chlist">{''.join(items)}</ul></section>
</main>
<footer>&copy; 2026 CBSEMock.org.in · <a href="{up}about.html">About Us</a> · <a href="{up}privacy.html">Privacy Policy</a> · <a href="{up}contact.html">Contact</a></footer>
</body>
</html>
"""
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    return rel


def main():
    n = 0
    chapters = load_chapters()
    for key in sorted({f"class{c['class']}/{c['subject_slug']}" for c in chapters}):
        rel = subject_index(key, [c for c in chapters if f"class{c['class']}/{c['subject_slug']}" == key])
        if rel:
            print(f"[notes] index {rel}")
    for ch in chapters:
        rel, doc = page(ch)
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(doc, encoding="utf-8")
        n += 1
        print(f"[notes] {'DRAFT' if ch.get('status') != 'live' else 'live '} {rel}")
    print(f"[notes] {n} chapter pages built")


if __name__ == "__main__":
    main()
    import favicon_tags
    for _f in sorted((ROOT / "notes").glob("**/*.html")):
        favicon_tags.add(_f)
