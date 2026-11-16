"""Link each LIVE chapter notes page from its subject notes page (the "hub"), inside that chapter's tab.

Finds the chapter's heading on the hub (e.g. "Ch 1: Chemical Reactions and Equations") and puts a
"Read the full chapter notes" button right under it, between <!-- CHNOTES:<id> --> markers so it is
updated, never duplicated. Locked hubs are never touched.      python3 hub_sync.py
"""
import json
import re
from pathlib import Path

import syllabus
from notes_pages import load_chapters

ROOT = Path(__file__).resolve().parent
LOCKED = {"resources/physics-xii-new.html"}
PROGRESS = ROOT / "notes_content" / "progress.json"
STYLE_MARK = "<!-- CHNOTES-STYLE -->"
STYLE = (STYLE_MARK + "<style>.chn-btn{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:10px 0 16px;"
         "padding:13px 18px;border-radius:14px;background:linear-gradient(135deg,#1a3a6b,#0f2347);color:#ffe4a0!important;"
         "text-decoration:none!important;font-weight:800;border:2px solid #c9a227;box-shadow:0 5px 0 rgba(10,28,54,.18);"
         "transition:transform .18s,box-shadow .18s}.chn-btn:hover{transform:translateY(-3px);box-shadow:0 9px 0 rgba(10,28,54,.14),"
         "0 0 0 3px #e8cc6a}.chn-btn small{display:block;font-weight:500;color:#cfd9ee;font-size:12px}.chn-btn span.arr{font-size:20px}</style>")


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


def main():
    try:
        progress = json.loads(PROGRESS.read_text(encoding="utf-8"))
    except Exception:
        progress = {}
    subj = {s["key"]: s for s in syllabus.SUBJECTS}
    changed, missing = set(), []
    for ch in load_chapters():
        key = f"class{ch['class']}/{ch['subject_slug']}"
        s = subj.get(key)
        if not s:
            continue
        rel = f"notes/class-{ch['class']}/{ch['subject_slug']}/{ch['slug']}.html"
        mark_a, mark_b = f"<!-- CHNOTES:{ch['_id']} -->", f"<!-- /CHNOTES:{ch['_id']} -->"
        for hub in s["hubs"]:
            if hub in LOCKED:
                continue
            p = ROOT / hub
            html = p.read_text(encoding="utf-8")
            if mark_a in html:                                   # drop the old button first
                html = html[:html.index(mark_a)] + html[html.index(mark_b) + len(mark_b):]
            if ch.get("status") == "live":
                pos = find_heading(html, ch["title"], ch["number"])
                if pos is None:
                    missing.append(f"{ch['title']} on {hub}")
                    continue
                href = "../" + rel                               # hubs live in resources/
                btn = (f'{mark_a}<a class="chn-btn" href="{href}"><span>📘 Read the full chapter notes'
                       f'<small>Concepts, labelled diagrams, worked board questions and common mistakes</small></span>'
                       f'<span class="arr">→</span></a>{mark_b}')
                html = html[:pos] + btn + html[pos:]
                if STYLE_MARK not in html:
                    html = html.replace("</head>", STYLE + "\n</head>", 1)
                progress.setdefault(ch["_id"], {})["hub_linked"] = True
            p.write_text(html, encoding="utf-8")
            changed.add(hub)
    PROGRESS.write_text(json.dumps(progress, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[hub-sync] {len(changed)} subject pages checked")
    for m in missing:
        print(f"::warning::No chapter heading found for {m} — link it by hand")


if __name__ == "__main__":
    main()
