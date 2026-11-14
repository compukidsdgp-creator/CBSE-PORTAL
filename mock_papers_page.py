#!/usr/bin/env python3
"""
mock_papers_page.py — builds the "Free Mock Papers" section of the portal
──────────────────────────────────────────────────────────────────────────
Writes free-mock-papers/index.html: every paper already posted (newest first,
with a Download PDF button) plus the dates of the next few papers.

It is rebuilt automatically by post_pyq.py each time a paper is posted, so the
section never needs editing by hand.

    python3 mock_papers_page.py            # rebuild from question-bank/calendar.json
"""
import html
from datetime import date
from pathlib import Path

import mock_bank

ROOT     = Path(__file__).parent
OUT_DIR  = ROOT / "free-mock-papers"
OUT_FILE = OUT_DIR / "index.html"
SITE     = "https://cbsemock.org.in"

SUBJECTS = {
    "science10":   ("Science", "X"),
    "maths10":     ("Mathematics", "X"),
    "physics12":   ("Physics", "XII"),
    "chemistry12": ("Chemistry", "XII"),
    "maths12":     ("Mathematics", "XII"),
    "biology12":   ("Biology", "XII"),
}
MARKS = {"science10": 80, "maths10": 80, "maths12": 80, "physics12": 70, "chemistry12": 70, "biology12": 70}


def _set_no(paper_id: str) -> int:
    return int(paper_id.rsplit("P", 1)[-1])


def collect():
    """(posted papers newest first, upcoming paper days soonest first)."""
    cal = mock_bank.load_calendar()
    posted, upcoming = [], []
    for d in sorted(cal):
        for cls_key in ("class10", "class12"):
            e = cal[d][cls_key]
            subject, cls = SUBJECTS[e["subject_key"]]
            item = {"date": date.fromisoformat(d), "subject": subject, "cls": cls, "key": e["subject_key"],
                    "set": _set_no(e["paper_id"]), "pdf": f"../pyq-papers/{e['subject_key']}_{d}.pdf"}
            (posted if e.get("posted") else upcoming).append(item)
    posted.sort(key=lambda x: (x["date"], x["cls"]), reverse=True)
    return posted, upcoming


def _card(p):
    d = p["date"]
    return f"""
      <article class="paper" data-cls="{p['cls']}">
        <div class="paper-top"><span class="tag tag-{p['cls'].lower()}">Class {p['cls']}</span><span class="when">{d.strftime('%a, %d %b %Y')}</span></div>
        <h3>{html.escape(p['subject'])}</h3>
        <p class="meta">Practice Paper Set {p['set']} &middot; {MARKS[p['key']]} marks &middot; 3 hours</p>
        <a class="btn" href="{p['pdf']}" download>&#11015; Download PDF</a>
        <a class="view" href="{p['pdf']}" target="_blank" rel="noopener">Open in browser</a>
      </article>"""


def build() -> Path:
    posted, upcoming = collect()
    today = mock_bank.today_ist()
    upcoming = [u for u in upcoming if u["date"] >= today][:6]

    if posted:
        cards = "".join(_card(p) for p in posted)
        count_line = f"{len(posted)} paper{'s' if len(posted) != 1 else ''} so far &middot; a question is never repeated"
    else:
        first = upcoming[0]["date"].strftime("%A, %d %B") if upcoming else "soon"
        cards = f"""
      <div class="empty">
        <h3>The first papers arrive on {first} at 3:00 PM</h3>
        <p>Every Monday, Wednesday and Friday we add one new paper for Class X and one for Class XII. They will appear here as soon as they are published.</p>
      </div>"""
        count_line = "New series &middot; a question is never repeated"

    rows = "".join(
        f"<li><span>{u['date'].strftime('%a, %d %b')}</span><b>Class {u['cls']} {html.escape(u['subject'])}</b></li>"
        for u in upcoming) or "<li><span>To be announced</span><b>New papers every Mon, Wed &amp; Fri</b></li>"

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Free Mock Papers for Class 10 &amp; 12 — New Every Mon, Wed &amp; Fri | CBSEMock</title>
<meta name="description" content="Download free CBSE-pattern mock papers for Class 10 (Science, Maths) and Class 12 (Physics, Chemistry, Maths, Biology). A new paper every Monday, Wednesday and Friday — no question is ever repeated.">
<link rel="canonical" href="{SITE}/free-mock-papers/">
<meta property="og:title" content="Free Mock Papers — Class 10 &amp; 12 | CBSEMock">
<meta property="og:description" content="A new CBSE-pattern mock paper every Monday, Wednesday and Friday. Free PDF download.">
<meta property="og:url" content="{SITE}/free-mock-papers/">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2810600896966939" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>
<style>
:root{{--navy:#1a3a6b;--navy2:#0f2347;--gold:#c9a227;--gold2:#e8cc6a;--bg:#f3f1ed;--card:#fff;--border:#ddd8cc;--text:#1a1a1a;--muted:#666;--x:#b7791f;--xii:#0b7285}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--muted:#8b949e;--x:#e8cc6a;--xii:#66d9e8}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:'Inter',system-ui,Arial,sans-serif;line-height:1.5}}
a{{color:inherit}}
.top{{background:linear-gradient(135deg,#1a3a6b 0%,#0f2347 100%);color:#fff;padding:14px 16px}}
.top-in{{max-width:1040px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}}
.brand{{font-weight:700;font-size:1.05rem;text-decoration:none;color:#fff}}.brand b{{color:var(--gold2)}}
.back{{font-size:.82rem;text-decoration:none;border:1px solid rgba(255,255,255,.3);border-radius:20px;padding:5px 14px;color:#fff}}
.back:hover{{background:var(--gold);color:var(--navy2);border-color:var(--gold)}}
.hero{{background:linear-gradient(135deg,#1a3a6b 0%,#0f2347 100%);color:#fff;padding:26px 16px 34px;text-align:center}}
.hero h1{{font-family:'Crimson Pro',Georgia,serif;font-size:clamp(1.8rem,5vw,2.7rem);margin:0 0 8px;line-height:1.15}}
.hero h1 span{{color:var(--gold2)}}
.hero p{{margin:0 auto;max-width:640px;color:rgba(255,255,255,.85);font-size:.98rem}}
.days{{display:inline-flex;gap:8px;margin-top:16px;flex-wrap:wrap;justify-content:center}}
.days span{{background:var(--gold);color:var(--navy2);font-weight:700;font-size:.8rem;border-radius:20px;padding:5px 14px}}
.days em{{font-style:normal;color:rgba(255,255,255,.8);font-size:.85rem;align-self:center}}
main{{max-width:1040px;margin:0 auto;padding:22px 16px 40px}}
.bar{{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:16px}}
.bar small{{color:var(--muted);font-size:.85rem}}
.filters{{display:flex;gap:8px}}
.filters button{{font:inherit;font-size:.85rem;font-weight:600;border:1px solid var(--border);background:var(--card);color:var(--text);border-radius:20px;padding:6px 16px;cursor:pointer}}
.filters button.on{{background:var(--navy);color:#fff;border-color:var(--navy)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}}
.paper{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:6px}}
.paper-top{{display:flex;justify-content:space-between;align-items:center;gap:8px}}
.tag{{font-size:.72rem;font-weight:700;border-radius:12px;padding:3px 10px;color:#fff}}
.tag-x{{background:#b7791f}}.tag-xii{{background:#0b7285}}
.when{{font-size:.78rem;color:var(--muted)}}
.paper h3{{font-family:'Crimson Pro',Georgia,serif;font-size:1.5rem;margin:4px 0 0;line-height:1.15}}
.meta{{margin:0 0 8px;font-size:.82rem;color:var(--muted)}}
.btn{{display:block;text-align:center;background:var(--navy);color:#fff;font-weight:700;font-size:.9rem;text-decoration:none;border-radius:10px;padding:10px 12px;margin-top:auto}}
.btn:hover{{background:var(--gold);color:var(--navy2)}}
.view{{text-align:center;font-size:.78rem;color:var(--muted)}}
.empty{{grid-column:1/-1;background:var(--card);border:1px dashed var(--border);border-radius:14px;padding:28px 20px;text-align:center}}
.empty h3{{font-family:'Crimson Pro',Georgia,serif;font-size:1.4rem;margin:0 0 6px}}
.empty p{{margin:0 auto;max-width:520px;color:var(--muted);font-size:.92rem}}
.none{{display:none;color:var(--muted);text-align:center;padding:20px}}
.next{{margin-top:28px;background:var(--card);border:1px solid var(--border);border-radius:14px;padding:18px}}
.next h2{{font-family:'Crimson Pro',Georgia,serif;font-size:1.35rem;margin:0 0 10px}}
.next ul{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px 18px}}
.next li{{display:flex;gap:10px;font-size:.88rem;padding:5px 0;border-bottom:1px solid var(--border)}}
.next li span{{color:var(--muted);min-width:86px}}
.note{{margin-top:18px;font-size:.8rem;color:var(--muted);text-align:center}}
.tg{{display:inline-block;margin-top:14px;background:#229ED9;color:#fff;font-weight:700;font-size:.85rem;text-decoration:none;border-radius:30px;padding:8px 18px}}
footer{{text-align:center;font-size:.8rem;color:var(--muted);padding:18px 16px 28px}}
</style>
</head>
<body>
<div class="top"><div class="top-in">
  <a class="brand" href="../index.html">CBSE<b>MOCK</b>.org.in</a>
  <a class="back" href="../index.html">&larr; Hub</a>
</div></div>
<section class="hero">
  <h1>Free <span>Mock Papers</span></h1>
  <p>Full-length CBSE-pattern practice papers for Class X and Class XII, free to download as PDF. Every paper is new.</p>
  <div class="days"><em>New papers every</em><span>MON</span><span>WED</span><span>FRI</span><em>at 3 PM</em></div>
</section>
<main>
  <div class="bar">
    <small>{count_line}</small>
    <div class="filters" role="group" aria-label="Filter by class">
      <button class="on" data-f="all">All</button><button data-f="X">Class X</button><button data-f="XII">Class XII</button>
    </div>
  </div>
  <div class="grid" id="grid">{cards}
  </div>
  <p class="none" id="none">No papers for this class yet.</p>

  <section class="next">
    <h2>Coming next</h2>
    <ul>{rows}</ul>
  </section>

  <p class="note">These are practice papers prepared by CBSEMock.org.in on the CBSE pattern. They are not official CBSE question papers.<br>
    <a class="tg" href="https://t.me/cbsemockportal" target="_blank" rel="noopener">Get each new paper on Telegram</a></p>
</main>
<footer>&copy; CBSEMock.org.in &middot; <a href="../index.html">Home</a> &middot; <a href="../mock-zone/classes-9-10.html">Class IX-X Mock Zone</a> &middot; <a href="../mock-zone/classes-11-12.html">Class XI-XII Mock Zone</a></footer>
<script>
document.querySelectorAll('.filters button').forEach(function(b){{
  b.addEventListener('click',function(){{
    document.querySelectorAll('.filters button').forEach(function(x){{x.classList.remove('on')}});
    b.classList.add('on');
    var f=b.dataset.f,shown=0,cards=document.querySelectorAll('.paper');
    cards.forEach(function(c){{var ok=f==='all'||c.dataset.cls===f;c.style.display=ok?'':'none';if(ok)shown++;}});
    document.getElementById('none').style.display=(cards.length&&!shown)?'block':'none';
  }});
}});
</script>
</body>
</html>
"""
    OUT_DIR.mkdir(exist_ok=True)
    OUT_FILE.write_text(page, encoding="utf-8")
    return OUT_FILE


if __name__ == "__main__":
    print(f"Built {build()}")
