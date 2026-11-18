"""Quality gate for Weekly Knowledge Booster files. Exit code 1 if anything is wrong.
    python3 booster_check.py                      check every booster
    python3 booster_check.py booster_content/2026-11-30/class10_science.py
Checks: required fields, exact counts per type, answer keys (A/R letter, MCQ answer = one of the options),
every question has an answer and explanation, chapters match the plan's subject, no near-duplicates of
questions already in the question bank, the published papers, or any other booster.
"""
import json
import re
import sys
from pathlib import Path

import booster_plan as BP
from mock_bank import _norm

ROOT = Path(__file__).resolve().parent
BANK_FILE = {"class10/science": "class10_science", "class10/maths": "class10_maths", "class12/physics": "class12_physics",
             "class12/chemistry": "class12_chemistry", "class12/maths": "class12_maths", "class12/biology": "class12_biology"}
LEGACY = {"class10/science": "cl10_science", "class10/maths": "cl10_maths", "class12/physics": "cl12_physics",
          "class12/chemistry": "cl12_chemistry", "class12/maths": "cl12_maths", "class12/biology": "cl12_biology"}


def texts(b):
    """(label, text) for every question in a booster."""
    out = []
    for i, q in enumerate(b.get("ar", []), 1):
        out.append((f"AR{i}", f"{q.get('a', '')} {q.get('r', '')}"))
    for ci, c in enumerate(b.get("case", []), 1):
        for pi, p in enumerate(c.get("parts", []), 1):
            out.append((f"Case{ci}.{pi}", p.get("q", "")))
    for k in ("hots", "competency", "knowledge"):
        for i, q in enumerate(b.get(k, []), 1):
            out.append((f"{k}{i}", q.get("q", "")))
    return out


def existing(subject_key):
    pool = []
    f = ROOT / "question-bank" / f"{BANK_FILE.get(subject_key, '_')}.json"
    if f.exists():
        for q in json.loads(f.read_text(encoding="utf-8")).get("questions", []):
            pool.append((f"bank:{q.get('id')}", q.get("text", "")))
    try:
        from pyq_question_bank import QUESTION_BANKS
        for s in QUESTION_BANKS[LEGACY[subject_key]]["sections"]:
            for q in s["questions"]:
                pool.append((f"published:{q['id']}", q["text"]))
    except Exception:
        pass
    return pool


def similar(a, b):
    inter = len(a & b)
    return inter >= 6 and inter / max(1, min(len(a), len(b))) > 0.7


def check(b, others):
    p, sid = [], b.get("_id", "?")
    for k in ("subject_key", "subject", "class", "chapter_numbers", "chapters"):
        if not b.get(k):
            p.append(f"missing field {k}")
    if b.get("subject_key") not in BP.SUBJECTS:
        p.append(f"subject {b.get('subject_key')} is not in booster_plan.SUBJECTS")
    else:
        _, chs = BP.chapters_of(b["subject_key"])
        titles = {c["number"]: c["title"] for c in chs}
        for n, t in zip(b.get("chapter_numbers", []), b.get("chapters", [])):
            if titles.get(n) != t:
                p.append(f"chapter {n} should be titled '{titles.get(n)}', not '{t}'")
    C = BP.COUNTS
    for k in ("ar", "hots", "competency", "knowledge"):
        if len(b.get(k, [])) != C[k]:
            p.append(f"{k}: {len(b.get(k, []))} questions, need {C[k]}")
    if len(b.get("case", [])) != C["case"]:
        p.append(f"case: {len(b.get('case', []))} case studies, need {C['case']}")
    for ci, c in enumerate(b.get("case", []), 1):
        if len(c.get("passage", "")) < 250:
            p.append(f"Case{ci}: passage too short")
        if len(c.get("parts", [])) != C["case_parts"]:
            p.append(f"Case{ci}: {len(c.get('parts', []))} parts, need {C['case_parts']}")
    ars = [q.get("answer") for q in b.get("ar", [])]
    for i, q in enumerate(b.get("ar", []), 1):
        if q.get("answer") not in ("A", "B", "C", "D"):
            p.append(f"AR{i}: answer must be A/B/C/D")
        if len(q.get("why", "")) < 30:
            p.append(f"AR{i}: explanation too short")
    if len(b.get("ar", [])) >= 8 and len(set(ars)) < 3:
        p.append(f"AR answers too uniform ({ars}) — mix A/B/C/D")
    items = [(f"Case{ci}.{pi}", pt) for ci, c in enumerate(b.get("case", []), 1) for pi, pt in enumerate(c.get("parts", []), 1)]
    items += [(f"{k}{i}", q) for k in ("hots", "competency", "knowledge") for i, q in enumerate(b.get(k, []), 1)]
    for lab, q in items:
        if not q.get("q", "").strip():
            p.append(f"{lab}: empty question")
        if not str(q.get("answer", "")).strip():
            p.append(f"{lab}: no answer")
        if q.get("options"):
            o = q["options"]
            if len(o) != 4 or len({x.strip().lower() for x in o}) != 4:
                p.append(f"{lab}: needs 4 different options")
            m = re.match(r"\(([a-d])\)", str(q.get("answer", "")))
            if not m:
                p.append(f"{lab}: MCQ answer must start with (a)-(d)")
            elif o and o["abcd".index(m.group(1))].strip().lower() not in q["answer"].lower():
                p.append(f"{lab}: answer text does not match option ({m.group(1)})")
            if len(q.get("why", "")) < 20:
                p.append(f"{lab}: MCQ needs a short explanation")
    mine = texts(b)
    seen = []
    for lab, t in mine:
        sh = _norm(t)
        for olab, osh in seen:
            if similar(sh, osh):
                p.append(f"{lab}: repeats {olab} in the same booster")
        seen.append((lab, sh))
    for olab, ot in others:
        osh = _norm(ot)
        for lab, sh in [(l, _norm(t)) for l, t in mine]:
            if similar(sh, osh):
                p.append(f"{lab}: looks like a repeat of {olab}")
    return [f"{sid}: {x}" for x in p]


def main(paths):
    boosters = BP.load_boosters()
    if paths:
        want = {str(Path(x).resolve().relative_to(ROOT)) for x in paths}
        targets = [b for b in boosters if b["_src"] in want]
    else:
        targets = boosters
    problems = []
    for b in targets:
        others = existing(b.get("subject_key", ""))
        others += [(f"booster:{o['_id']}:{l}", t) for o in boosters if o["_id"] != b["_id"] and o.get("subject_key") == b.get("subject_key")
                   for l, t in texts(o)]
        problems += check(b, others)
    for x in problems:
        print("✗", x)
    print(f"[booster_check] {len(targets)} booster(s), {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
