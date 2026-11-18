"""Weekly Knowledge Booster — which chapters each week covers.

Every Monday one booster per subject goes live: one chapter, 50 questions with model answers
(10 assertion–reason, 4 case studies × 4 parts, 10 HOTS, 10 competency-based, 10 knowledge).
Chapters are taken in syllabus order; when there are more chapters left than Mondays left before
the board exams, two chapters are paired in one booster so every chapter is covered in time.

Files: booster_content/<monday YYYY-MM-DD>/<class>_<subject>.py   (a BOOSTER dict)
    python3 booster_plan.py next      → JSON: the coming Monday, what to write, what is already written
    python3 booster_plan.py status    → coverage per subject
"""
import importlib.util
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import syllabus

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "booster_content"
FIRST_MONDAY = date(2026, 11, 30)
BOARDS_START = date(2027, 2, 15)          # last booster week ends before this Monday
# Subjects in the booster. Add a key here to include another subject from syllabus.py.
SUBJECTS = ["class10/science", "class10/maths", "class12/physics", "class12/chemistry"]
COUNTS = {"ar": 10, "case": 4, "case_parts": 4, "hots": 10, "competency": 10, "knowledge": 10}


def today_ist():
    return (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()


def file_key(subject_key):
    cls, subj = subject_key.split("/", 1)
    return f"{cls}_{subj.replace('-', '_')}"


def load_boosters():
    out = []
    for f in sorted(SRC.glob("*/*.py")):
        if f.name.startswith("_") or not re.match(r"\d{4}-\d{2}-\d{2}$", f.parent.name):
            continue
        spec = importlib.util.spec_from_file_location(f"bc_{f.parent.name}_{f.stem}".replace("-", "_"), f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        b = dict(m.BOOSTER)
        b["_src"] = str(f.relative_to(ROOT))
        b["_monday"] = f.parent.name
        b["_id"] = f"{f.parent.name}/{f.stem}"
        out.append(b)
    return out


def chapters_of(subject_key):
    s = next(x for x in syllabus.SUBJECTS if x["key"] == subject_key)
    out = []
    for num, title, quiz in s["chapters"]:
        slug = syllabus.slugify(title)
        if not re.match(r"^[a-z0-9-]+$", slug):
            slug = f"chapter-{num}"
        out.append({"number": num, "title": title, "slug": slug, "quiz": quiz})
    return s, out


def covered(boosters, subject_key):
    done = set()
    for b in boosters:
        if b.get("subject_key") == subject_key:
            done.update(b.get("chapter_numbers", []))
    return done


def next_monday(d=None):
    d = d or today_ist()
    m = d + timedelta(days=(7 - d.weekday()) % 7)
    if m == d and d.weekday() == 0:
        m = d + timedelta(days=7)                # on a Monday, the next booster is next week's
    return max(m, FIRST_MONDAY)


def mondays_left(monday):
    n, d = 0, monday
    while d < BOARDS_START:
        n += 1; d += timedelta(days=7)
    return max(n, 1)


def plan_for(monday, boosters=None):
    boosters = load_boosters() if boosters is None else boosters
    written = {b["subject_key"]: b for b in boosters if b["_monday"] == monday.isoformat()}
    weeks = mondays_left(monday)
    plan = []
    for key in SUBJECTS:
        s, chs = chapters_of(key)
        if key in written:
            b = written[key]
            plan.append({"subject_key": key, "subject": s["name"], "class": s["class"], "status": "written",
                         "file": b["_src"], "chapters": b.get("chapter_numbers", [])})
            continue
        done = covered([b for b in boosters if b["_monday"] < monday.isoformat()], key)
        left = [c for c in chs if c["number"] not in done]
        if not left:
            plan.append({"subject_key": key, "subject": s["name"], "class": s["class"], "status": "complete"})
            continue
        take = 2 if len(left) > weeks and len(left) >= 2 else 1
        pick = left[:take]
        plan.append({"subject_key": key, "subject": s["name"], "class": s["class"], "status": "to_write",
                     "file": f"booster_content/{monday.isoformat()}/{file_key(key)}.py",
                     "chapters": [c["number"] for c in pick], "titles": [c["title"] for c in pick],
                     "quiz": [c["quiz"] for c in pick if c["quiz"]], "chapters_left_after": len(left) - take,
                     "mondays_left_after": weeks - 1})
    return plan


def status():
    boosters = load_boosters()
    out = []
    for key in SUBJECTS:
        s, chs = chapters_of(key)
        done = covered(boosters, key)
        out.append({"subject_key": key, "subject": s["name"], "class": s["class"],
                    "chapters": [{"n": c["number"], "title": c["title"], "done": c["number"] in done} for c in chs]})
    return out


def admin_data():
    """Booster section of the admin tracker: every booster with its state, coverage per subject, and next week's plan."""
    try:
        appr = json.loads((SRC / "approvals.json").read_text(encoding="utf-8"))
    except Exception:
        appr = {}
    today = today_ist()
    boosters = load_boosters()
    items = []
    for b in boosters:
        a = appr.get(b["_id"], {})
        st = a.get("status", "draft")
        if st == "approved":
            st = "live" if today >= date.fromisoformat(b["_monday"]) else "scheduled"
        subj = b["subject_key"].split("/", 1)[1]
        n = len(b.get("ar", [])) + sum(len(c.get("parts", [])) for c in b.get("case", [])) + \
            sum(len(b.get(k, [])) for k in ("hots", "competency", "knowledge"))
        items.append({"id": b["_id"], "monday": b["_monday"], "subject": b.get("subject"), "class": b.get("class"),
                      "chapters": [f"{x}. {t}" for x, t in zip(b.get("chapter_numbers", []), b.get("chapters", []))],
                      "questions": n, "state": st, "note": a.get("note", ""),
                      "url": f"booster/{b['_monday']}/class-{b['class']}-{subj}.html"})
    nm = next_monday(today)
    return {"items": sorted(items, key=lambda x: (x["monday"], x["class"], x["subject"] or "")),
            "coverage": [{"subject": s["subject"], "class": s["class"], "done": sum(c["done"] for c in s["chapters"]),
                          "total": len(s["chapters"])} for s in status()],
            "next": {"monday": nm.isoformat(), "plan": plan_for(nm, boosters)}}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "next"
    if cmd == "next":
        m = next_monday()
        print(json.dumps({"monday": m.isoformat(), "plan": plan_for(m)}, indent=1, ensure_ascii=False))
    else:
        for s in status():
            print(f"{s['class']} {s['subject']:<30}", "".join("■" if c["done"] else "□" for c in s["chapters"]))
