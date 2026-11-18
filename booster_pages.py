"""Weekly Knowledge Booster pages: booster/<monday>/<class>-<subject>.html + booster/index.html.

A booster goes live when it is approved in the admin panel (booster_content/approvals.json) AND its
Monday (IST) has arrived; until then it is a hidden draft (noindex, unlinked).
    python3 booster_pages.py
"""
import html
import json
import re
from datetime import date
from pathlib import Path

import booster_plan as BP

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "booster"
SITE = "https://cbsemock.org.in"
E = html.escape
AR_KEY = [("A", "Both A and R are true, and R is the correct explanation of A."),
          ("B", "Both A and R are true, but R is not the correct explanation of A."),
          ("C", "A is true, but R is false."),
          ("D", "A is false, but R is true.")]
SHORT = {"ar": "Assertion–Reason", "case": "Case studies", "hots": "HOTS", "competency": "Competency", "knowledge": "Knowledge"}
SECTIONS = [("ar", "Assertion and Reasoning", "Read both statements and choose the correct option from the key."),
            ("case", "Case Studies", "Read each passage and answer the questions that follow."),
            ("hots", "HOTS — Higher Order Thinking", "Think it through before you open the answer."),
            ("competency", "Competency-Based Questions", "Apply the idea to a real situation."),
            ("knowledge", "Knowledge Check", "Quick recall: one or two lines each.")]


def approvals():
    try:
        return json.loads((BP.SRC / "approvals.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def is_live(b, appr=None):
    appr = approvals() if appr is None else appr
    return appr.get(b["_id"], {}).get("status") == "approved" and BP.today_ist() >= date.fromisoformat(b["_monday"])


def rel_path(b):
    subj = b["subject_key"].split("/", 1)[1]
    return f"booster/{b['_monday']}/class-{b['class']}-{subj}.html"


def BP_texts(b):
    return [1 for _ in b.get("ar", [])] + [1 for c in b.get("case", []) for _ in c.get("parts", [])] + \
        [1 for k in ("hots", "competency", "knowledge") for _ in b.get(k, [])]


def nice(d):
    d = date.fromisoformat(d)
    return f"{d.day} {d:%B %Y}"


CSS = """
:root{--navy:#1a3a6b;--navy2:#0f2347;--gold:#c9a227;--gold2:#e8cc6a;--bg:#f3f1ed;--card:#fff;--text:#1a1a1a;--muted:#5d5d5d;--border:#ddd8cc;--code:#f1eee6;--grd:linear-gradient(135deg,#1a3a6b 0%,#0f2347 100%)}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--card:#161b22;--text:#e6edf3;--muted:#8b949e;--border:#30363d;--code:#1f2630}}
*{box-sizing:border-box;margin:0;padding:0}
body{font:16px/1.7 Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text)}
h1,h2{font-family:'Crimson Pro',Georgia,serif}
.hero{background:var(--grd);color:#fff;padding:0 20px 44px;position:relative;overflow:hidden}
.hero::after{content:'';position:absolute;width:380px;height:380px;right:-140px;top:-160px;border-radius:50%;background:radial-gradient(circle,rgba(232,204,106,.25),transparent 70%)}
.hero>*{position:relative;z-index:1}
.topbar{max-width:980px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.12)}
.brand{color:#fff;text-decoration:none;font-weight:800}.brand b{color:var(--gold2)}
.nb{color:#fff;text-decoration:none;font-size:.8rem;font-weight:600;padding:7px 13px;border-radius:99px;border:1px solid rgba(255,255,255,.28);transition:all .18s}
.nb:hover{background:var(--gold);color:var(--navy2);border-color:var(--gold)}
.hero-in{max-width:980px;margin:0 auto;padding-top:22px}
.crumb{font-size:.8rem;color:rgba(255,255,255,.72);margin-bottom:10px}.crumb a{color:var(--gold2);text-decoration:none;display:inline-block;padding:5px 0}
.badge{display:inline-flex;align-items:center;gap:8px;background:var(--gold);color:var(--navy2);border-radius:20px;padding:5px 16px;font-size:.78rem;font-weight:800;letter-spacing:.05em;text-transform:uppercase;margin-bottom:12px}
h1{font-size:clamp(1.8rem,4.2vw,2.6rem);line-height:1.15;margin-bottom:10px}
.meta{display:flex;flex-wrap:wrap;gap:8px;font-size:.8rem}.chip{padding:4px 12px;border-radius:99px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2)}
.draft{max-width:980px;margin:16px auto 0;background:#fff4d6;color:#6b4e00;border:1.5px dashed #c9a227;border-radius:12px;padding:10px 14px;font-size:.88rem;font-weight:600;overflow-wrap:anywhere}
.wrap{max-width:980px;margin:0 auto;padding:0 20px 70px}
.bar{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:var(--card);border:1px solid var(--border);border-radius:14px;padding:10px 12px;margin:-24px 0 22px;box-shadow:0 10px 26px rgba(15,35,71,.12)}
.bar a.jump{font-size:.8rem;font-weight:700;color:var(--navy);text-decoration:none;padding:7px 11px;border-radius:99px;background:var(--code)}
.bar a.jump:hover{background:var(--gold2)}
.bar .sp{flex:1}
.btn{border:0;cursor:pointer;font:inherit;font-size:.82rem;font-weight:800;padding:9px 14px;border-radius:99px;transition:transform .15s,box-shadow .15s}
.btn.gold{background:var(--gold);color:var(--navy2)}.btn.navy{background:var(--grd);color:#ffe4a0}
.btn:hover{transform:translateY(-2px);box-shadow:0 6px 14px rgba(15,35,71,.2)}
section{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:22px 24px;margin:0 0 22px}
section>h2{font-size:1.6rem;color:var(--navy);display:flex;align-items:center;gap:10px;line-height:1.2}
section>h2 .n{font-family:Inter,sans-serif;font-size:.78rem;font-weight:800;background:var(--grd);color:var(--gold2);padding:4px 10px;border-radius:99px}
section>p.lead{color:var(--muted);margin:4px 0 14px}
@media(prefers-color-scheme:dark){section>h2,.bar a.jump{color:var(--gold2)}}
.key{background:var(--code);border-radius:12px;padding:10px 14px;margin:0 0 14px;font-size:.9rem}.key b{color:var(--navy)}
.q{border:1.5px solid var(--border);border-radius:14px;padding:14px 16px;margin:12px 0;break-inside:avoid}
.q .qh{display:flex;gap:12px}
.q .num{flex:0 0 32px;height:32px;border-radius:50%;background:var(--grd);color:var(--gold2);font-weight:800;font-size:.85rem;display:flex;align-items:center;justify-content:center}
.q .body{flex:1;min-width:0}
.q .body p{margin:0 0 6px}
.q .lbl{font-weight:800;color:var(--navy)}
.opts{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;margin:8px 0 4px}
.opts li{padding:6px 10px;border-radius:10px;background:var(--code)}
@media(max-width:640px){.opts{grid-template-columns:1fr}
 .bar{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;border-radius:12px;padding:8px;margin:-22px -4px 18px}
 .bar::-webkit-scrollbar{display:none}.bar>*{flex:0 0 auto}.bar .sp{display:none}
 .wrap{padding:0 12px 60px}section{padding:18px 14px;border-radius:16px}.case{padding:12px 10px}.case .passage{padding:10px 12px}
 .q{padding:12px}.q .qh{gap:10px}.q .num{flex-basis:28px;height:28px;font-size:.78rem}}
html{scroll-padding-top:84px}
.reveal{margin-top:8px;font-size:.8rem;font-weight:800;color:var(--navy);background:none;border:1.5px solid var(--gold);border-radius:99px;padding:6px 14px;cursor:pointer}
.reveal:hover{background:var(--gold2)}
.ans{display:none;margin-top:10px;background:rgba(35,125,105,.08);border-left:4px solid #237d69;border-radius:8px;padding:10px 12px}
.ans.on{display:block}.ans b.k{color:#237d69}
.case{border:2px solid var(--gold);border-radius:16px;padding:16px 18px;margin:14px 0}
.case h3{font-family:'Crimson Pro',Georgia,serif;font-size:1.25rem;color:var(--navy);margin-bottom:6px}
.case .passage{background:var(--code);border-radius:12px;padding:12px 14px;margin-bottom:6px}
.case .q{margin:10px 0 0}
.links{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.links a{display:flex;justify-content:space-between;align-items:center;min-height:54px;padding:12px 16px;border-radius:14px;color:#fff;text-decoration:none;font-weight:700;background:linear-gradient(135deg,#3b6fb8,#0f2347);box-shadow:0 5px 0 rgba(10,28,54,.18);transition:transform .2s}
.links a::after{content:'→';color:var(--gold2)}.links a:hover{transform:translateY(-3px)}
.links li:nth-child(2) a{background:linear-gradient(135deg,#2b9a80,#12483e)}.links li:nth-child(3) a{background:linear-gradient(135deg,#8b6bc2,#392653)}
footer{text-align:center;padding:26px 16px;font-size:.8rem;color:rgba(255,255,255,.7);background:var(--grd)}
footer a{color:var(--gold2);text-decoration:none;display:inline-block;padding:6px 4px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.card{display:block;text-decoration:none;color:#fff;border-radius:16px;padding:16px;background:linear-gradient(145deg,#3b6fb8,#0e2344);box-shadow:0 8px 0 rgba(10,28,54,.16);transition:transform .2s}
.card:hover{transform:translateY(-5px)}.card small{color:#ffe4a0;font-weight:800;letter-spacing:.05em;font-size:.72rem}.card b{display:block;font-family:'Crimson Pro',serif;font-size:1.3rem;margin:4px 0}
@media print{.hero,.bar,footer,.links,.reveal,.draft{display:none!important}body{background:#fff;color:#000;font-size:12pt}
 section{border:0;padding:0;margin:0 0 14pt}.ans{display:block!important;background:none;border-left:2px solid #999}
 body.print-q .ans{display:none!important}.q{border:1px solid #bbb}}
"""

JS = """<script>
document.querySelectorAll('.reveal').forEach(function(b){b.addEventListener('click',function(){
  var a=b.nextElementSibling;var on=a.classList.toggle('on');b.textContent=on?'Hide answer':'Show answer';});});
var all=false;document.getElementById('toggleAll').addEventListener('click',function(){all=!all;
  document.querySelectorAll('.ans').forEach(function(a){a.classList.toggle('on',all)});
  document.querySelectorAll('.reveal').forEach(function(b){b.textContent=all?'Hide answer':'Show answer'});
  this.textContent=all?'Hide all answers':'Show all answers';});
document.getElementById('printQ').addEventListener('click',function(){document.body.classList.add('print-q');window.print();setTimeout(function(){document.body.classList.remove('print-q')},500);});
document.getElementById('printA').addEventListener('click',function(){document.body.classList.remove('print-q');window.print();});
</script>"""


def opts_html(opts):
    return '<ul class="opts">' + "".join(f"<li><b>({chr(97 + i)})</b> {E(o)}</li>" for i, o in enumerate(opts)) + "</ul>"


def qcard(n, body, answer_html):
    return (f'<div class="q"><div class="qh"><span class="num">{n}</span><div class="body">{body}'
            f'<button class="reveal" type="button">Show answer</button><div class="ans">{answer_html}</div></div></div></div>')


def render_sections(b):
    out, n = [], 0
    for key, title, lead in SECTIONS:
        items = b.get(key, [])
        cnt = len(items) if key != "case" else sum(len(c["parts"]) for c in items)
        inner = ""
        if key == "ar":
            inner += '<div class="key"><b>Key:</b> ' + " ".join(f"<b>({k})</b> {E(t)}" for k, t in AR_KEY) + "</div>"
            for it in items:
                n += 1
                body = f'<p><span class="lbl">Assertion (A):</span> {E(it["a"])}</p><p><span class="lbl">Reason (R):</span> {E(it["r"])}</p>'
                inner += qcard(n, body, f'<b class="k">Answer: ({it["answer"]})</b> — {E(it["why"])}')
        elif key == "case":
            for ci, c in enumerate(items, 1):
                parts = ""
                for pi, pt in enumerate(c["parts"]):
                    n += 1
                    body = f"<p>{E(pt['q'])}</p>" + (opts_html(pt["options"]) if pt.get("options") else "")
                    ans = f'<b class="k">Answer: {E(pt["answer"])}</b>' + (f" — {E(pt['why'])}" if pt.get("why") else "")
                    parts += qcard(n, body, ans)
                inner += (f'<div class="case"><h3>Case {ci}: {E(c["title"])}</h3><div class="passage">{E(c["passage"])}</div>{parts}</div>')
        else:
            for it in items:
                n += 1
                body = f"<p>{E(it['q'])}</p>" + (opts_html(it["options"]) if it.get("options") else "")
                ans = f'<b class="k">Answer:</b> {E(it["answer"])}' + (f"<br>{E(it['why'])}" if it.get("why") else "")
                inner += qcard(n, body, ans)
        out.append(f'<section id="{key}"><h2>{E(title)} <span class="n">{cnt}</span></h2><p class="lead">{E(lead)}</p>{inner}</section>')
    return "".join(out), n


def head(title, desc, url, robots, ld):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@600;700&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>
</head>"""


def practice_links(b, up):
    links = []
    try:
        from notes_pages import load_chapters
        subj = b["subject_key"].split("/", 1)[1]
        for c in load_chapters():
            if c.get("status") == "live" and c["class"] == b["class"] and c["subject_slug"] == subj and c["number"] in b["chapter_numbers"]:
                links.append((f"📒 Chapter notes: {c['title']}", f"{up}notes/class-{c['class']}/{subj}/{c['slug']}.html"))
    except Exception:
        pass
    _, chs = BP.chapters_of(b["subject_key"])
    for c in chs:
        if c["number"] in b["chapter_numbers"] and c["quiz"] and (ROOT / f"chapters/{c['quiz']}.html").exists():
            links.append((f"📝 Chapter quiz: {c['title']}", f"{up}chapters/{c['quiz']}.html"))
    portal = {"class10/science": "cbse-class-10-science-mock-tests.html", "class10/maths": "cbse-class-10-maths-standard-mock-tests.html",
              "class12/physics": "cbse-class-12-physics-mock-papers.html", "class12/chemistry": "cbse-class-12-chemistry-mock-papers.html",
              "class12/maths": "cbse-class-12-maths-mock-papers.html", "class12/biology": "cbse-class-12-biology-mock-papers.html",
              "class10/social-science": "cbse-class-10-social-science-mock-tests.html"}.get(b["subject_key"])
    if portal:
        links.append(("📄 Full mock papers", up + portal))
    return links


def page(b, live):
    rel = rel_path(b)
    url = f"{SITE}/{rel}"
    up = "../../"
    chapters = " & ".join(f"Ch {n}: {t}" for n, t in zip(b["chapter_numbers"], b["chapters"]))
    title = f"Weekly Knowledge Booster — Class {b['class']} {b['subject']} — {', '.join(b['chapters'])} | CBSEMock"
    n_q = len(BP_texts(b))
    desc = (f"{n_q} CBSE board-style questions with answers for Class {b['class']} {b['subject']} ({', '.join(b['chapters'])}): "
            f"assertion–reason, case studies, HOTS, competency-based and knowledge questions.")
    secs, total = render_sections(b)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "LearningResource", "@id": url + "#booster", "name": f"Weekly Knowledge Booster: Class {b['class']} {b['subject']} — {', '.join(b['chapters'])}",
         "url": url, "description": desc, "educationalLevel": f"Class {b['class']}", "inLanguage": "en-IN",
         "learningResourceType": ["Practice Questions", "Question Bank"], "isAccessibleForFree": True,
         "teaches": b["chapters"], "datePublished": b["_monday"],
         "provider": {"@type": "Organization", "@id": SITE + "/#organization", "name": "CBSEMOCK", "url": SITE + "/"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Weekly Knowledge Booster", "item": SITE + "/booster/"},
            {"@type": "ListItem", "position": 3, "name": f"Class {b['class']} {b['subject']}", "item": url}]}]}
    robots = "" if live else '<meta name="robots" content="noindex, nofollow">'
    draft = "" if live else (f'<div class="draft">Draft preview — hidden from Google and not linked from the site. '
                             f'It goes live on Monday {nice(b["_monday"])} once approved in the admin panel. (Source: {E(b["_src"])})</div>')
    jumps = "".join(f'<a class="jump" href="#{k}">{SHORT[k]}</a>' for k, t, _ in SECTIONS)
    links = "".join(f'<li><a href="{h}">{E(l)}</a></li>' for l, h in practice_links(b, up))
    body = f"""
<body>
<header class="hero">
<div class="topbar"><a class="brand" href="{up}index.html">CBSE<b>Mock</b></a><a class="nb" href="../">⚡ All boosters</a></div>
<div class="hero-in"><nav class="crumb"><a href="{up}index.html">Home</a> › <a href="../">Weekly Knowledge Booster</a> › Class {b['class']} {E(b['subject'])}</nav>
<span class="badge">⚡ Weekly Knowledge Booster · week of {nice(b['_monday'])}</span>
<h1>Class {b['class']} {E(b['subject'])}: {E(chapters)}</h1>
<div class="meta"><span class="chip">{total} questions with answers</span><span class="chip">CBSE 2026–27 pattern</span><span class="chip">Reviewed by subject teachers</span></div></div>
{draft}
</header>
<main class="wrap">
<div class="bar">{jumps}<span class="sp"></span><button class="btn gold" id="toggleAll" type="button">Show all answers</button><button class="btn navy" id="printQ" type="button">Print questions</button><button class="btn navy" id="printA" type="button">Print with answers</button></div>
{secs}
<section><h2>Keep going</h2><ul class="links">{links}</ul></section>
</main>
<footer>&copy; 2026 CBSEMock.org.in · <a href="{up}about.html">About Us</a> · <a href="{up}privacy.html">Privacy Policy</a> · <a href="{up}contact.html">Contact</a></footer>
{JS}
</body>
</html>
"""
    return rel, head(title, desc, url, robots, ld) + body


def index(live):
    url = SITE + "/booster/"
    by_week = {}
    for b in live:
        by_week.setdefault(b["_monday"], []).append(b)
    weeks = ""
    for m in sorted(by_week, reverse=True):
        cards = "".join(f'<a class="card" href="{b["_monday"]}/{rel_path(b).rsplit("/", 1)[1]}"><small>CLASS {b["class"]} · {E(b["subject"].upper())}</small>'
                        f'<b>{E(" & ".join(b["chapters"]))}</b><span>{len(BP_texts(b))} questions with answers →</span></a>' for b in by_week[m])
        weeks += f'<section><h2>Week of {nice(m)}</h2><div class="grid">{cards}</div></section>'
    desc = "Every Monday: 50+ CBSE board-style questions with answers per subject — assertion–reason, case studies, HOTS, competency-based and knowledge questions."
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Weekly Knowledge Booster", "url": url, "description": desc,
          "isPartOf": {"@id": SITE + "/#website"}}
    robots = "" if live else '<meta name="robots" content="noindex, follow">'
    doc = head("Weekly Knowledge Booster — CBSE Class 10 & 12 | CBSEMock", desc, url, robots, ld) + f"""
<body>
<header class="hero"><div class="topbar"><a class="brand" href="../index.html">CBSE<b>Mock</b></a><a class="nb" href="../learn/">📘 Learn</a></div>
<div class="hero-in"><nav class="crumb"><a href="../index.html">Home</a> › Weekly Knowledge Booster</nav>
<span class="badge">⚡ New every Monday</span><h1>Weekly Knowledge Booster</h1>
<p style="color:rgba(255,255,255,.85);max-width:720px">One chapter per subject each week: 10 assertion–reason, 4 case studies, 10 HOTS, 10 competency-based and 10 knowledge questions, all with model answers. Practise online or print it.</p></div></header>
<main class="wrap" style="padding-top:26px">{weeks or '<section><h2>The first boosters arrive on Monday 30 November 2026</h2><p class="lead">Class 10 Science, Class 10 Maths, Class 12 Physics and Class 12 Chemistry.</p></section>'}</main>
<footer>&copy; 2026 CBSEMock.org.in · <a href="../about.html">About Us</a> · <a href="../privacy.html">Privacy Policy</a> · <a href="../contact.html">Contact</a></footer>
</body></html>
"""
    (OUT / "index.html").write_text(doc, encoding="utf-8")


def main():
    appr = approvals()
    boosters = BP.load_boosters()
    live = []
    OUT.mkdir(exist_ok=True)
    for b in boosters:
        is_l = is_live(b, appr)
        rel, doc = page(b, is_l)
        (ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / rel).write_text(doc, encoding="utf-8")
        print(f"[booster] {'live ' if is_l else 'DRAFT'} {rel}")
        if is_l:
            live.append(b)
    index(live)
    print(f"[booster] {len(boosters)} boosters, {len(live)} live")


if __name__ == "__main__":
    main()
    import favicon_tags
    for _f in sorted(OUT.glob("**/*.html")):
        favicon_tags.add(_f)
