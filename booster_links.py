"""Interlink the Weekly Knowledge Booster across the site (idempotent marker blocks).

  index.html               zone card in "Learning Zones" + "This week's booster" strip + footer link
  cbse-class-*.html        subject portal → this subject's latest live booster
  chapters/<quiz>.html     chapter quiz → the booster that covers that chapter
  resources/<hub>.html     inside each chapter tab → the booster for that chapter (never the locked pages)
  notes chapter pages      via booster_for_chapter(), used by notes_pages.py in "Practise this chapter"
Only LIVE boosters are linked from content pages; before the first one goes live the home page shows a teaser.
    python3 booster_links.py
"""
import html as H
import re
from datetime import date
from pathlib import Path

import booster_plan as BP
from booster_pages import approvals, is_live, rel_path, BP_texts

ROOT = Path(__file__).resolve().parent
LOCKED = {"resources/physics-xii-new.html", "resources/ai-x.html", "resources/cs-xii.html"}
PORTAL = {"class10/science": "cbse-class-10-science-mock-tests.html",
          "class10/maths": ["cbse-class-10-maths-standard-mock-tests.html", "cbse-class-10-maths-basic-mock-tests.html"],
          "class12/physics": "cbse-class-12-physics-mock-papers.html", "class12/chemistry": "cbse-class-12-chemistry-mock-papers.html",
          "class12/maths": "cbse-class-12-maths-mock-papers.html", "class12/biology": "cbse-class-12-biology-mock-papers.html"}
E = H.escape


def nice(d):
    d = date.fromisoformat(d)
    return f"{d.day} {d:%b}"


def live_boosters():
    appr = approvals()
    return sorted([b for b in BP.load_boosters() if is_live(b, appr)], key=lambda b: b["_monday"])


def booster_for_chapter(subject_key, number):
    """Latest live booster covering this chapter → (relative path from site root, booster) or None."""
    hits = [b for b in live_boosters() if b["subject_key"] == subject_key and number in b.get("chapter_numbers", [])]
    return (rel_path(hits[-1]), hits[-1]) if hits else None


def cut(s, a, b):
    while a in s and b in s:
        i, j = s.index(a), s.index(b, s.index(a)) + len(b)
        s = s[:i] + s[j:]
    return s


CARD_CSS = """<style id="wkb-css">.wkb{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:14px 0;padding:14px 16px;border-radius:16px;text-decoration:none;color:#fff;
background:linear-gradient(135deg,#1a3a6b,#0f2347);border:2px solid #c9a227;box-shadow:0 6px 0 rgba(10,28,54,.18);transition:transform .2s,box-shadow .2s;font-family:Inter,system-ui,sans-serif}
.wkb:hover{transform:translateY(-3px);box-shadow:0 10px 0 rgba(10,28,54,.14),0 0 0 3px rgba(232,204,106,.45)}
.wkb .z{flex:0 0 46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;background:#c9a227;color:#0f2347;animation:wkbz 1.8s ease-in-out infinite}
.wkb .t{flex:1 1 220px;min-width:0}.wkb .t b{display:block;font-size:1rem;line-height:1.3;color:#ffe4a0}.wkb .t small{display:block;font-size:.84rem;color:rgba(255,255,255,.82);margin-top:2px}
.wkb .go{flex:0 0 auto;background:#c9a227;color:#0f2347;font-weight:800;font-size:.8rem;letter-spacing:.04em;padding:10px 14px;border-radius:99px;min-height:40px;display:inline-flex;align-items:center}
@keyframes wkbz{50%{transform:scale(1.08) rotate(-6deg)}}
@media(max-width:600px){.wkb .go{width:100%;justify-content:center}}
@media(prefers-reduced-motion:reduce){.wkb .z{animation:none}.wkb{transition:none}}</style>"""


def card(href, title, sub):
    return (f'<a class="wkb" href="{href}"><span class="z" aria-hidden="true">⚡</span>'
            f'<span class="t"><b>{E(title)}</b><small>{E(sub)}</small></span><span class="go">PRACTISE NOW →</span></a>')


def with_css(s):
    if 'id="wkb-css"' not in s:
        s = s.replace("</head>", CARD_CSS + "\n</head>", 1)
    return s


def drop_css(s):
    return re.sub(r'<style id="wkb-css">.*?</style>\n?', "", s, flags=re.S)


def sub_line(b):
    return (f"{len(BP_texts(b))} questions with answers · assertion–reason, case studies, HOTS, competency, "
            f"knowledge · week of {nice(b['_monday'])}")


# ── home page ───────────────────────────────────────────────────────────────
ZA, ZB = "<!-- BOOSTER-ZONE -->", "<!-- /BOOSTER-ZONE -->"
SA, SB = "<!-- BOOSTER-STRIP:START -->", "<!-- BOOSTER-STRIP:END -->"
FA, FB = "<!-- BOOSTER-FOOT -->", "<!-- /BOOSTER-FOOT -->"


def home(live):
    f = ROOT / "index.html"
    s = f.read_text(encoding="utf-8")
    o = s
    s = re.sub(re.escape(ZA) + r".*?" + re.escape(ZB) + r"\n[ \t]*", "", s, flags=re.S)
    s = re.sub(re.escape(SA) + r".*?" + re.escape(SB) + r"\n\n", "", s, flags=re.S)
    s = re.sub(r" ?" + re.escape(FA) + r".*?" + re.escape(FB), "", s, flags=re.S)
    zone = (f'{ZA}<style>.wkz{{grid-column:1/-1;display:flex;align-items:center;flex-wrap:wrap;gap:10px 20px;padding:18px 22px;border-radius:18px;'
            f'text-decoration:none;color:#fff;background:linear-gradient(120deg,#1f4a86,#0b1d3a 62%,#3a2c00);border:2px solid #c9a227;'
            f'box-shadow:0 8px 0 rgba(10,28,54,.16),0 15px 26px rgba(10,28,54,.18);transition:transform .2s,box-shadow .2s;position:relative;overflow:hidden}}'
            f'.wkz:hover{{transform:translateY(-5px);box-shadow:0 12px 0 rgba(10,28,54,.13),0 22px 32px rgba(10,28,54,.26),0 0 0 3px #e8cc6a}}'
            f'.wkz i{{font-style:normal;font-size:2.3rem;line-height:1;animation:wkzb 1.8s ease-in-out infinite}}@keyframes wkzb{{50%{{transform:scale(1.1) rotate(-8deg)}}}}'
            f'.wkz b{{font-family:"Crimson Pro",serif;font-size:1.45rem;line-height:1.15}}.wkz b em{{font-family:Inter,sans-serif;font-style:normal;display:inline-block;'
            f'vertical-align:middle;background:#ffd600;color:#0f2347;font-size:.62rem;font-weight:800;letter-spacing:.04em;border-radius:10px;padding:3px 9px;margin-left:6px}}'
            f'.wkz span{{flex:1 1 300px;font-size:.88rem;color:rgba(255,255,255,.86)}}.wkz u{{text-decoration:none;background:#c9a227;color:#0f2347;font-weight:800;'
            f'font-size:.8rem;letter-spacing:.04em;padding:10px 16px;border-radius:99px;white-space:nowrap}}'
            f'@media(max-width:600px){{.wkz{{padding:16px}}.wkz u{{width:100%;text-align:center}}}}@media(prefers-reduced-motion:reduce){{.wkz i{{animation:none}}}}</style>'
            f'<a class="wkz" href="booster/"><i aria-hidden="true">⚡</i><b>Weekly Knowledge Booster<em>EVERY MONDAY</em></b>'
            f'<span>50+ board-style questions with model answers for each subject: assertion–reason, case studies, HOTS, competency-based and knowledge.</span>'
            f'<u>OPEN BOOSTER →</u></a>{ZB}')
    i = s.index('<div class="zone-launch-grid"')
    j = s.index("</div>", i)                          # end of the grid: the zone card goes last
    s = s[:j] + zone + "\n  " + s[j:]
    if live:
        last = live[-1]["_monday"]
        week = [b for b in live if b["_monday"] == last]
        cards = "".join(
            f'<a class="wkh-card" href="{rel_path(b)}"><small>CLASS {b["class"]} · {E(b["subject"].upper())}</small>'
            f'<b>{E(" & ".join(b["chapters"]))}</b><span>{len(BP_texts(b))} questions + answers →</span></a>' for b in week)
        head = f"⚡ This week’s Knowledge Booster <em>week of {nice(last)}</em>"
        lead = "One chapter per subject, every Monday: assertion–reason, case studies, HOTS, competency-based and knowledge questions with model answers."
    else:
        plan = BP.plan_for(BP.FIRST_MONDAY)
        cards = "".join(f'<a class="wkh-card soon" href="booster/"><small>CLASS {p["class"]} · {E(p["subject"].upper())}</small>'
                        f'<b>{E(" & ".join(p.get("titles", [])) or "Coming soon")}</b><span>Live Monday {nice(BP.FIRST_MONDAY.isoformat())}</span></a>'
                        for p in plan)
        head = f"⚡ Weekly Knowledge Booster <em>starts Monday {nice(BP.FIRST_MONDAY.isoformat())}</em>"
        lead = "Every Monday until the boards: 50+ board-style questions with model answers for each subject — assertion–reason, case studies, HOTS, competency-based and knowledge."
    strip = f"""{SA}
<style>
.wkh{{max-width:1100px;margin:26px auto 10px;padding:0 20px}}
.wkh-box{{border-radius:22px;padding:20px;background:linear-gradient(135deg,#1a3a6b,#0f2347);border:2px solid #c9a227;box-shadow:0 10px 26px rgba(15,35,71,.25);color:#fff}}
.wkh-head{{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:14px}}
.wkh-head h2{{font-family:'Crimson Pro',serif;color:#ffe4a0;font-size:clamp(1.4rem,2.8vw,1.85rem);margin:0}}
.wkh-head h2 em{{font-family:Inter,sans-serif;font-style:normal;font-size:.5em;font-weight:800;letter-spacing:.06em;text-transform:uppercase;background:#c9a227;color:#0f2347;padding:4px 10px;border-radius:99px;vertical-align:middle;margin-left:6px;white-space:nowrap}}
.wkh-head p{{color:rgba(255,255,255,.82);font-size:.88rem;margin:4px 0 0;max-width:720px}}
.wkh-all{{display:inline-flex;align-items:center;min-height:40px;padding:9px 18px;border-radius:99px;background:#c9a227;color:#0f2347;font-weight:800;font-size:.8rem;text-decoration:none;transition:transform .2s}}
.wkh-all:hover{{transform:translateY(-3px)}}
.wkh-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}}
.wkh-card{{display:flex;flex-direction:column;gap:4px;padding:14px;border-radius:16px;text-decoration:none;color:#fff;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);transition:transform .2s,background .2s}}
.wkh-card:hover{{transform:translateY(-4px);background:rgba(232,204,106,.16)}}
.wkh-card small{{font-size:.75rem;font-weight:800;letter-spacing:.06em;color:#e8cc6a}}.wkh-card b{{font-family:'Crimson Pro',serif;font-size:1.15rem;line-height:1.2}}
.wkh-card span{{margin-top:auto;font-size:.8rem;font-weight:700;color:#ffe4a0}}
@media(max-width:860px){{.wkh-grid{{grid-template-columns:1fr 1fr}}}}@media(max-width:520px){{.wkh{{padding:0 14px}}.wkh-grid{{grid-template-columns:1fr}}}}
</style>
<section class="wkh" aria-label="Weekly Knowledge Booster"><div class="wkh-box">
<div class="wkh-head"><div><h2>{head}</h2><p>{lead}</p></div><a class="wkh-all" href="booster/">ALL BOOSTERS →</a></div>
<div class="wkh-grid">{cards}</div></div></section>
{SB}"""
    if "<!-- LEARN-STRIP:START -->" in s:
        s = s.replace("<!-- LEARN-STRIP:START -->", strip + "\n\n<!-- LEARN-STRIP:START -->", 1)
    else:
        k = s.index("</section>", s.index('<div class="zone-launch-grid"')) + len("</section>")
        s = s[:k] + "\n\n" + strip + s[k:]
    s = s.replace('<a href="learn/" style="color:inherit;opacity:.7;text-decoration:none;margin:0 8px;">Learn</a> |',
                  '<a href="learn/" style="color:inherit;opacity:.7;text-decoration:none;margin:0 8px;">Learn</a> | '
                  f'{FA}<a href="booster/" style="color:inherit;opacity:.7;text-decoration:none;margin:0 8px;">Weekly Booster</a> |{FB}', 1)
    if s != o:
        f.write_text(s, encoding="utf-8")
        return 1
    return 0


# ── content pages ───────────────────────────────────────────────────────────
def portals(live):
    n = 0
    for key, files in PORTAL.items():
        for rel in ([files] if isinstance(files, str) else files):
            f = ROOT / rel
            if not f.exists() or rel in LOCKED:
                continue
            s = f.read_text(encoding="utf-8")
            o = s
            a, b = "<!-- BOOSTER-PORTAL -->", "<!-- /BOOSTER-PORTAL -->"
            s = cut(s, a, b)
            mine = [x for x in live if x["subject_key"] == key]
            if mine:
                x = mine[-1]
                blk = (f'{a}<div style="max-width:1100px;margin:10px auto 0;padding:0 14px">'
                       + card(rel_path(x), f"⚡ This week’s Knowledge Booster: {' & '.join(x['chapters'])}", sub_line(x))
                       + f"</div>{b}")
                m = re.search(r"</header>", s)
                if m:
                    s = s[:m.end()] + blk + s[m.end():]
                s = with_css(s)
            elif "wkb" not in s.replace('id="wkb-css"', ""):
                s = drop_css(s)
            if s != o:
                f.write_text(s, encoding="utf-8")
                n += 1
    return n


def quizzes(live):
    n = 0
    for s_ in BP.SUBJECTS:
        subj, chs = BP.chapters_of(s_)
        for c in chs:
            if not c["quiz"]:
                continue
            f = ROOT / "chapters" / f"{c['quiz']}.html"
            if not f.exists():
                continue
            s = f.read_text(encoding="utf-8")
            o = s
            a, b = f"<!-- BOOSTER-QUIZ:{s_}/{c['number']} -->", f"<!-- /BOOSTER-QUIZ:{s_}/{c['number']} -->"
            s = cut(s, a, b)
            hit = [x for x in live if x["subject_key"] == s_ and c["number"] in x["chapter_numbers"]]
            if hit:
                x = hit[-1]
                blk = (f'{a}<div style="max-width:980px;margin:10px auto 0;padding:0 14px">'
                       + card("../" + rel_path(x), f"⚡ Weekly Knowledge Booster: {c['title']}", sub_line(x)) + f"</div>{b}")
                top_end = re.search(r"<!-- /CHNOTES-TOP:[^>]*-->", s)
                m = top_end or re.search(r"<main[^>]*>", s) or re.search(r"<body[^>]*>", s)
                s = s[:m.end()] + blk + s[m.end():]
                s = with_css(s)
            if s != o:
                f.write_text(s, encoding="utf-8")
                n += 1
    return n


def hubs(live):
    from hub_sync import find_heading
    import syllabus
    n = 0
    for s_ in syllabus.SUBJECTS:
        if s_["key"] not in BP.SUBJECTS:
            continue
        for hub in s_["hubs"]:
            f = ROOT / hub
            if hub in LOCKED or not f.exists():
                continue
            s = f.read_text(encoding="utf-8")
            o = s
            for num, title, _ in s_["chapters"]:
                a, b = f"<!-- BOOSTER-HUB:{s_['key']}/{num} -->", f"<!-- /BOOSTER-HUB:{s_['key']}/{num} -->"
                s = cut(s, a, b)
                hit = [x for x in live if x["subject_key"] == s_["key"] and num in x["chapter_numbers"]]
                if not hit:
                    continue
                pos = find_heading(s, title, num)
                if pos is None:
                    continue
                # after the chapter-notes card if there is one, so notes come first
                end_notes = re.compile(r"<!-- /CHNOTES:[^>]*-->")
                m = end_notes.match(s, pos) or (end_notes.search(s, pos, pos + 6000))
                at = m.end() if m else pos
                x = hit[-1]
                s = (s[:at] + a + card("../" + rel_path(x), f"⚡ Weekly Knowledge Booster: {title}", sub_line(x)) + b + s[at:])
            if "BOOSTER-HUB:" in s:
                s = with_css(s)
            if s != o:
                f.write_text(s, encoding="utf-8")
                n += 1
    return n


def main():
    live = live_boosters()
    print(f"[booster-links] {len(live)} live booster(s)")
    print(f"[booster-links] home {home(live)} · portals {portals(live)} · quizzes {quizzes(live)} · hubs {hubs(live)} page(s) updated")


if __name__ == "__main__":
    main()
