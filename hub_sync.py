"""Make every LIVE chapter notes page impossible to miss.

On each subject notes page ("hub"):
  1. a 3D animated banner on the Home tab listing the chapter notes that are ready,
  2. a 3D "tap to open" card right under the chapter's own heading inside its tab,
  3. a small floating "Chapter notes" button that is always on screen.
On each chapter quiz page: the same card above the page's footer note.
Everything sits between marker comments, so re-running updates it instead of duplicating it.
Locked or owner-frozen pages are never touched.        python3 hub_sync.py
"""
import json
import re
from pathlib import Path

import syllabus
from notes_pages import load_chapters

ROOT = Path(__file__).resolve().parent
LOCKED = {"resources/physics-xii-new.html", "resources/ai-x.html", "resources/cs-xii.html"}  # locked or owner-frozen
PROGRESS = ROOT / "notes_content" / "progress.json"
STYLE_A, STYLE_B = "<!-- CHNOTES-STYLE -->", "<!-- /CHNOTES-STYLE -->"
BANNER_A, BANNER_B = "<!-- CHNOTES-BANNER -->", "<!-- /CHNOTES-BANNER -->"
FAB_A, FAB_B = "<!-- CHNOTES-FAB -->", "<!-- /CHNOTES-FAB -->"

CSS = """<style>
.chn3d{perspective:900px;margin:14px 0 20px}
.chn-card{position:relative;display:flex;align-items:center;gap:16px;padding:16px 18px;border-radius:18px;text-decoration:none!important;
 color:#fff!important;background:linear-gradient(135deg,#1f4a8a 0%,#0f2347 60%,#0b1a36 100%);border:2px solid #c9a227;overflow:hidden;
 box-shadow:0 10px 0 #091a33,0 18px 30px rgba(9,26,51,.35);transform:rotateX(8deg);transform-origin:50% 100%;
 animation:chnFloat 3.2s ease-in-out infinite;transition:transform .25s,box-shadow .25s}
.chn-card:hover,.chn-card:focus{transform:rotateX(0) translateY(-4px) scale(1.01);box-shadow:0 14px 0 #091a33,0 26px 40px rgba(9,26,51,.4),0 0 0 4px rgba(232,204,106,.55);animation-play-state:paused}
.chn-card:active{transform:translateY(6px);box-shadow:0 4px 0 #091a33}
.chn-card::after{content:'';position:absolute;inset:0;background:linear-gradient(110deg,transparent 35%,rgba(255,236,170,.32) 50%,transparent 65%);transform:translateX(-120%);animation:chnShine 3.6s ease-in-out infinite}
.chn-book{position:relative;flex:0 0 58px;height:46px;perspective:300px}
.chn-book i{position:absolute;top:0;width:29px;height:46px;background:#fff8e1;border:2px solid #c9a227;box-sizing:border-box}
.chn-book i.l{left:0;border-radius:6px 0 0 6px}.chn-book i.r{right:0;border-radius:0 6px 6px 0}
.chn-book i.p{right:0;border-radius:0 6px 6px 0;background:#ffe9a8;transform-origin:left center;animation:chnFlip 2.4s ease-in-out infinite}
.chn-book b{position:absolute;left:5px;right:5px;top:12px;height:2px;background:#c9a227;box-shadow:0 7px 0 #c9a227,0 14px 0 #c9a227;opacity:.55}
.chn-txt{flex:1;min-width:0;position:relative;z-index:1}
.chn-txt strong{display:block;font-size:1.06rem;line-height:1.25;color:#ffe4a0}
.chn-txt small{display:block;font-size:.82rem;color:#d3ddf1;margin-top:3px;line-height:1.35}
.chn-tap{position:relative;z-index:1;flex:0 0 auto;display:flex;align-items:center;gap:6px;background:#c9a227;color:#0f2347;font-weight:900;font-size:.78rem;letter-spacing:.05em;
 padding:9px 13px;border-radius:99px;box-shadow:0 0 0 0 rgba(232,204,106,.7);animation:chnPulse 1.8s infinite}
.chn-tap span{display:inline-block;animation:chnNudge 1s ease-in-out infinite}
.chn-banner{background:linear-gradient(135deg,#fff8e6,#fff);border:2px dashed #c9a227;border-radius:20px;padding:16px 16px 6px;margin:16px 0 22px}
.chn-banner h3{margin:0 0 4px;font-size:1.15rem;color:#0f2347;display:flex;align-items:center;gap:8px}
.chn-banner h3 em{font-style:normal;background:#e8452c;color:#fff;font-size:.7rem;font-weight:900;letter-spacing:.06em;padding:3px 8px;border-radius:99px;animation:chnPulse 1.8s infinite}
.chn-banner p{margin:0;color:#555;font-size:.9rem}
.chn-all{display:inline-block;margin:0 0 10px;font-weight:800;color:#1a3a6b!important;text-decoration:none!important;padding:6px 0}
.chn-fab{position:fixed;left:14px;bottom:18px;z-index:900;display:flex;align-items:center;gap:8px;padding:11px 15px;border-radius:99px;text-decoration:none!important;
 background:linear-gradient(135deg,#1f4a8a,#0f2347);color:#ffe4a0!important;font-weight:800;font-size:.85rem;border:2px solid #c9a227;
 box-shadow:0 6px 18px rgba(9,26,51,.4);animation:chnBob 2.6s ease-in-out infinite}
.chn-fab:hover{transform:translateY(-3px)}
@keyframes chnFloat{0%,100%{transform:rotateX(8deg) translateY(0)}50%{transform:rotateX(4deg) translateY(-4px)}}
@keyframes chnShine{0%,55%{transform:translateX(-120%)}85%,100%{transform:translateX(120%)}}
@keyframes chnFlip{0%,15%{transform:rotateY(0)}45%,60%{transform:rotateY(-170deg)}90%,100%{transform:rotateY(0)}}
@keyframes chnPulse{0%{box-shadow:0 0 0 0 rgba(232,204,106,.75)}70%{box-shadow:0 0 0 12px rgba(232,204,106,0)}100%{box-shadow:0 0 0 0 rgba(232,204,106,0)}}
@keyframes chnNudge{0%,100%{transform:translateX(0)}50%{transform:translateX(4px)}}
@keyframes chnBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@media(max-width:600px){.chn-card{flex-wrap:wrap;gap:12px}.chn-tap{width:100%;justify-content:center}.chn-fab{font-size:.8rem;padding:10px 13px}}
@media(prefers-reduced-motion:reduce){.chn-card,.chn-card::after,.chn-book i.p,.chn-tap,.chn-tap span,.chn-fab,.chn-banner h3 em{animation:none!important}.chn-card{transform:none}}
</style>"""


def card(href, title, sub):
    return (f'<div class="chn3d"><a class="chn-card" href="{href}" aria-label="Open the full chapter notes: {title}">'
            f'<span class="chn-book" aria-hidden="true"><i class="l"></i><i class="r"></i><i class="p"></i><b></b></span>'
            f'<span class="chn-txt"><strong>{title}</strong><small>{sub}</small></span>'
            f'<span class="chn-tap">TAP TO OPEN <span>➜</span></span></a></div>')


def cut(html, a, b):
    while a in html and b in html:
        i, j = html.index(a), html.index(b) + len(b)
        html = html[:i] + html[j:]
    return html


def norm(s):
    s = re.sub(r"<[^>]+>", " ", s).lower().replace("–", "-").replace("&amp;", "&")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def find_heading(html, title, number):
    """Position just after the chapter's heading in the hub, or None."""
    t = norm(title.split(": ", 1)[-1])
    best = None
    for m in re.finditer(r"<(h[234])\b[^>]*>(.*?)</\1>", html, re.S | re.I):
        txt = norm(m.group(2))
        if t and t in txt:
            score = 2 if re.search(rf"\bch(apter)?\s*{number}\b", txt) else 1
            if best is None or score > best[0]:
                best = (score, m.end())
    return best[1] if best else None


def block_end(html, start):
    """End index of the <div> element that opens at `start`."""
    depth, i = 0, start
    for m in re.finditer(r"<(/?)div\b[^>]*>", html[start:], re.I):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return start + m.end()
    return None


def banner_spot(html):
    m = re.search(r'<div class="hero">', html)
    if m:
        end = block_end(html, m.start())
        if end:
            return end
    m = re.search(r'<div class="sec-content">', html)
    return m.end() if m else None


def ensure_style(html):
    html = cut(html, STYLE_A, STYLE_B)
    old = re.search(r"<!-- CHNOTES-STYLE --><style>.*?</style>", html, re.S)     # first version (single line, no end mark)
    if old:
        html = html[:old.start()] + html[old.end():]
    html = re.sub(r"\n+</head>", "\n</head>", html, count=1)
    return html.replace("</head>", f"{STYLE_A}{CSS}{STYLE_B}</head>", 1)


def main():
    try:
        progress = json.loads(PROGRESS.read_text(encoding="utf-8"))
    except Exception:
        progress = {}
    subj = {s["key"]: s for s in syllabus.SUBJECTS}
    chapters = load_chapters()
    changed, missing = set(), []

    hubs = {}
    for s in syllabus.SUBJECTS:
        for h in s["hubs"]:
            if h not in LOCKED:
                hubs.setdefault(h, []).append(s["key"])

    for hub, keys in hubs.items():
        p = ROOT / hub
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        orig = html
        html = cut(html, BANNER_A, BANNER_B)
        html = cut(html, FAB_A, FAB_B)
        live = [c for c in chapters if f"class{c['class']}/{c['subject_slug']}" in keys]
        for ch in live:                                          # drop old per-chapter cards
            html = cut(html, f"<!-- CHNOTES:{ch['_id']} -->", f"<!-- /CHNOTES:{ch['_id']} -->")
        live = sorted([c for c in live if c.get("status") == "live"], key=lambda c: c["number"])
        if live:
            for ch in live:
                pos = find_heading(html, ch["title"], ch["number"])
                href = f"../notes/class-{ch['class']}/{ch['subject_slug']}/{ch['slug']}.html"
                if pos is None:
                    missing.append(f"{ch['title']} on {hub}")
                    continue
                html = (html[:pos] + f"<!-- CHNOTES:{ch['_id']} -->"
                        + card(href, f"📘 Full chapter notes: {ch['title']}",
                               "Concepts step by step, labelled diagrams, worked board questions and common mistakes")
                        + f"<!-- /CHNOTES:{ch['_id']} -->" + html[pos:])
                progress.setdefault(ch["_id"], {})["hub_linked"] = True
            c0 = live[0]
            index = f"../notes/class-{c0['class']}/{c0['subject_slug']}/"
            cards = "".join(card(f"../notes/class-{c['class']}/{c['subject_slug']}/{c['slug']}.html",
                                 f"Ch {c['number']}: {c['title']}", "Full notes · diagrams · worked board questions")
                            for c in live[:6])
            banner = (f'{BANNER_A}<div class="chn-banner"><h3>📘 Full chapter notes <em>NEW</em></h3>'
                      f'<p>Detailed, exam-ready notes for each chapter. Tap a card to open it.</p>{cards}'
                      f'<a class="chn-all" href="{index}">See all chapters ({len(live)} ready) →</a></div>{BANNER_B}')
            spot = banner_spot(html)
            if spot:
                html = html[:spot] + banner + html[spot:]
            fab = f'{FAB_A}<a class="chn-fab" href="{index}" aria-label="Open chapter notes">📘 Chapter notes</a>{FAB_B}'
            html = html.replace("</body>", fab + "</body>", 1)
            html = ensure_style(html)
        else:
            html = cut(html, STYLE_A, STYLE_B)
        if html != orig:
            p.write_text(html, encoding="utf-8")
            changed.add(hub)

    # the chapter quiz page (chapters/<quiz>.html) also points to the full notes
    quiz_of = {}
    for s_ in syllabus.SUBJECTS:
        for num, title, quiz in s_["chapters"]:
            if quiz:
                quiz_of.setdefault((s_["key"], num), quiz)
    for ch in chapters:
        quiz = quiz_of.get((f"class{ch['class']}/{ch['subject_slug']}", ch["number"]))
        p = ROOT / "chapters" / f"{quiz}.html" if quiz else None
        if not p or not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        orig = html
        a, b = f"<!-- CHNOTES:{ch['_id']} -->", f"<!-- /CHNOTES:{ch['_id']} -->"
        html = cut(html, a, b)
        if ch.get("status") == "live" and "<!-- STATIC-CONTENT:END -->" in html and '<p class="sc-meta">' in html:
            href = f"../notes/class-{ch['class']}/{ch['subject_slug']}/{ch['slug']}.html"
            blk = a + card(href, f"📘 Full chapter notes: {ch['title']}",
                           "Revise it properly first: concepts, labelled diagrams, worked board questions") + b
            k = html.rindex('<p class="sc-meta">', 0, html.index("<!-- STATIC-CONTENT:END -->"))
            html = html[:k] + blk + html[k:]
            # and once more at the top of the page content, so it is seen before the quiz starts
            m = re.search(r"<main[^>]*>", html) or re.search(r"<body[^>]*>", html)
            top = a.replace("CHNOTES:", "CHNOTES-TOP:")
            html = cut(html, top, top.replace("<!-- ", "<!-- /"))
            if m:
                html = (html[:m.end()] + top + '<div style="max-width:980px;margin:10px auto 0;padding:0 14px">'
                        + card(href, f"📘 Read the chapter notes first: {ch['title']}", "Tap to open the full notes, then take the quiz")
                        + "</div>" + top.replace("<!-- ", "<!-- /") + html[m.end():])
            html = ensure_style(html)
            progress.setdefault(ch["_id"], {})["quiz_linked"] = True
        if html != orig:
            p.write_text(html, encoding="utf-8")
            changed.add(str(p.relative_to(ROOT)))
    PROGRESS.write_text(json.dumps(progress, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[hub-sync] {len(changed)} pages updated")
    for m in missing:
        print(f"::warning::No chapter heading found for {m} — link it by hand")


if __name__ == "__main__":
    main()
