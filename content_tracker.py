"""Content Tracker data: the state of every chapter in syllabus.py, read straight from the repo.

Used by build_admin_data.py (the admin dashboard) and by the nightly drafting run to pick the next
chapter.        python3 content_tracker.py     (prints a summary and the next chapter in the queue)
"""
import glob
import json
import os
import re
from pathlib import Path

import syllabus

ROOT = Path(__file__).resolve().parent
APPROVALS = ROOT / "notes_content" / "approvals.json"
PROGRESS = ROOT / "notes_content" / "progress.json"


def _json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return {}


def notes_chapters():
    """{(class, subject_slug, slug): CHAPTER dict} from notes_content/."""
    from notes_pages import load_chapters
    out = {}
    for ch in load_chapters():
        out[(ch["class"], ch["subject_slug"], ch["slug"])] = ch
    return out


def chapter_id(key, slug):
    return f"{key}/{slug}"


def build():
    approvals, progress = _json(APPROVALS), _json(PROGRESS)
    notes = notes_chapters()
    hub_text = {}
    learn_rel = {}
    try:
        from learn_articles import ARTICLES
        for a in ARTICLES:
            for _, h in a.get("related", []):
                learn_rel.setdefault(h, []).append(a["slug"])
    except Exception:
        pass
    reels_by_quiz = {}
    try:
        from topic_links import why_links
        for f in glob.glob(str(ROOT / "formula-posts/why/*/*.mp4")):
            for _, u in why_links(os.path.basename(f))["chapters"]:
                q = u.rsplit("/", 1)[-1].replace(".html", "")
                reels_by_quiz[q] = reels_by_quiz.get(q, 0) + 1
    except Exception:
        pass

    subjects = []
    for s in syllabus.SUBJECTS:
        subj_slug = s["key"].split("/", 1)[1]
        rows = []
        for num, title, quiz in s["chapters"]:
            slug = syllabus.slugify(title)
            if not re.match(r"^[a-z0-9-]+$", slug):
                slug = f"chapter-{num}"
            cid = chapter_id(s["key"], slug)
            ch = notes.get((s["class"], subj_slug, slug))
            appr = approvals.get(cid, {})
            if ch is None:
                state = "todo"
            elif appr.get("status") == "approved" or ch.get("status") == "live":
                state = "live"
            elif appr.get("status") == "changes":
                state = "changes"
            else:
                state = "draft"
            url = f"notes/class-{s['class']}/{subj_slug}/{slug}.html"
            hub_linked = False
            for h in s["hubs"]:
                if h not in hub_text:
                    try:
                        hub_text[h] = (ROOT / h).read_text(encoding="utf-8", errors="ignore")
                    except Exception:
                        hub_text[h] = ""
                hub_linked = hub_linked or (url in hub_text[h])
            words = diagrams = worked = mistakes = revision = 0
            if ch:
                body = ch.get("glance", "") + "".join(b for _, b in ch.get("concepts", []))
                words = len(re.sub(r"<[^>]+>", " ", body).split())
                diagrams, worked = len(ch.get("diagrams", [])), len(ch.get("worked", []))
                mistakes, revision = len(ch.get("mistakes", [])), len(ch.get("revision", []))
            prog = progress.get(cid, {})
            rows.append({
                "id": cid, "n": num, "title": title, "state": state, "url": url if ch else "",
                "note": appr.get("note", ""), "words": words, "diagrams": diagrams, "worked": worked,
                "mistakes": mistakes, "revision": revision, "hub": hub_linked,
                "tools": prog.get("tools", []), "quiz": bool(quiz and (ROOT / f"chapters/{quiz}.html").exists()),
                "quiz_slug": quiz or "", "reels": reels_by_quiz.get(quiz, 0) if quiz else 0,
                "learn": len(learn_rel.get(f"chapters/{quiz}.html", [])) if quiz else 0,
                "updated": ch.get("updated", "") if ch else "",
            })
        done = sum(r["state"] == "live" for r in rows)
        subjects.append({"key": s["key"], "class": s["class"], "name": s["name"], "code": s["code"],
                         "verified": s.get("verified", False), "hub_locked": s.get("hub_locked", False),
                         "hubs": s["hubs"], "rows": rows, "live": done, "total": len(rows),
                         "drafts": sum(r["state"] in ("draft", "changes") for r in rows)})
    order = {k: i for i, k in enumerate(syllabus.QUEUE_ORDER)}
    subjects.sort(key=lambda x: order.get(x["key"], 99))
    allrows = [r for s in subjects for r in s["rows"]]
    return {"subjects": subjects,
            "totals": {"chapters": len(allrows), "live": sum(r["state"] == "live" for r in allrows),
                       "draft": sum(r["state"] == "draft" for r in allrows),
                       "changes": sum(r["state"] == "changes" for r in allrows),
                       "todo": sum(r["state"] == "todo" for r in allrows)},
            "next": next_up(subjects)}


def next_up(subjects):
    """What the nightly run should do next: fix a chapter with requested changes first, else draft the next new one."""
    for s in subjects:
        for r in s["rows"]:
            if r["state"] == "changes":
                return {"action": "revise", "subject": s["key"], "id": r["id"], "title": r["title"], "note": r["note"]}
    for s in subjects:
        for r in s["rows"]:
            if r["state"] == "todo":
                return {"action": "draft", "subject": s["key"], "id": r["id"], "title": r["title"], "n": r["n"]}
    return None


if __name__ == "__main__":
    t = build()
    print(json.dumps(t["totals"]), "\nnext:", t["next"])
    for s in t["subjects"]:
        print(f"  {s['class']} {s['name']:<32} {s['live']}/{s['total']} live, {s['drafts']} draft")
