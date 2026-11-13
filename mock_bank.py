#!/usr/bin/env python3
"""
mock_bank.py — JSON question pool for the free mock papers
───────────────────────────────────────────────────────────
Guarantee: a question is used in ONE paper only. Nothing is recycled.

Files (all under question-bank/):
  class10_science.json, class10_maths.json,
  class12_physics.json, class12_chemistry.json,
  class12_maths.json,   class12_biology.json
      {"subject_key", "subject", "class", "max_marks", "time",
       "sections": [{"name", "title", "marks", "slots": [["MCQ", 7], ...]}],
       "questions": [{"id", "section", "type", "chapter", "text",
                      "options"?, "note"?, "answer"?}]}
  usage_log.json   which question went into which paper, and when
  calendar.json    the paper planned for each Monday / Wednesday / Friday

Commands:
  python3 mock_bank.py validate            check the pool (ids, answers, duplicates)
  python3 mock_bank.py stock               fresh papers left per subject
  python3 mock_bank.py plan --slots 6      assemble papers for the next 6 posting days
  python3 mock_bank.py preview --out DIR   build PDFs of all planned, unposted papers
"""
import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT      = Path(__file__).parent
BANK_DIR  = ROOT / "question-bank"
USAGE     = BANK_DIR / "usage_log.json"
CALENDAR  = BANK_DIR / "calendar.json"

SUBJECT_FILES = {
    "science10":   "class10_science.json",
    "maths10":     "class10_maths.json",
    "physics12":   "class12_physics.json",
    "chemistry12": "class12_chemistry.json",
    "maths12":     "class12_maths.json",
    "biology12":   "class12_biology.json",
}
ROTATION = {
    "class10": ["science10", "maths10"],
    "class12": ["physics12", "chemistry12", "maths12", "biology12"],
}
POST_WEEKDAYS = (0, 2, 4)            # Monday, Wednesday, Friday
TYPE_MARKS = {"MCQ": 1, "A/R": 1, "VSA": 2, "SA": 3, "CBQ": 4, "LA": 5}
IST = timezone(timedelta(hours=5, minutes=30))

AR_PREAMBLE = (
    "Questions {nums} consist of two statements: Assertion (A) and Reason (R). "
    "Select the appropriate option:\n"
    "(A) Both A and R are true and R is the correct explanation of A.\n"
    "(B) Both A and R are true, but R is not the correct explanation of A.\n"
    "(C) A is true, but R is false.\n"
    "(D) A is false, but R is true."
)


def today_ist() -> date:
    return datetime.now(IST).date()


# ── load / save ──────────────────────────────────────────────────────────────
def load_subject(subject_key: str) -> dict:
    return json.loads((BANK_DIR / SUBJECT_FILES[subject_key]).read_text(encoding="utf-8"))

def _load(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default

def _save(path: Path, data):
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

def load_usage() -> dict:
    return _load(USAGE, {})

def load_calendar() -> dict:
    return _load(CALENDAR, {})


# ── paper assembly ───────────────────────────────────────────────────────────
def _pick(candidates, count, chapter_load):
    """Pick `count` questions, spreading chapters as evenly as the pool allows."""
    chosen, pool = [], list(candidates)
    for _ in range(count):
        if not pool:
            return None
        pool.sort(key=lambda q: (chapter_load.get(q.get("chapter", ""), 0), q["id"]))
        q = pool.pop(0)
        chosen.append(q)
        chapter_load[q.get("chapter", "")] = chapter_load.get(q.get("chapter", ""), 0) + 1
    return chosen

def assemble(subject_key: str, used: set):
    """Return the question ids of one fresh paper, or None if the pool cannot supply it."""
    bank = load_subject(subject_key)
    fresh = [q for q in bank["questions"] if q["id"] not in used]
    ids, load = [], {}
    for sec in bank["sections"]:
        for qtype, count in sec["slots"]:
            cands = [q for q in fresh if q["section"] == sec["name"] and q["type"] == qtype]
            got = _pick(cands, count, load)
            if got is None:
                return None
            ids += [q["id"] for q in got]
    return ids

def papers_left(subject_key: str, used: set) -> int:
    used, n = set(used), 0
    while True:
        ids = assemble(subject_key, used)
        if ids is None:
            return n
        used |= set(ids); n += 1

def _markup(text: str) -> str:
    """Plain text -> reportlab paragraph markup (escape, keep line breaks)."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text.replace("\n", "<br/>")

def _for_pdf(q: dict) -> dict:
    out = dict(q, marks=TYPE_MARKS[q["type"]], text=_markup(q["text"]))
    if q.get("options"):
        out["options"] = [_markup(o) for o in q["options"]]
    if q.get("note"):
        out["note"] = _markup(q["note"])
    return out

def paper_sections(subject_key: str, question_ids: list, raw: bool = False):
    """(meta, sections-with-questions) ready for pyq_generator.build_pdf_from_paper."""
    bank = load_subject(subject_key)
    by_id = {q["id"]: q for q in bank["questions"]}
    missing = [i for i in question_ids if i not in by_id]
    if missing:
        raise KeyError(f"{subject_key}: questions missing from the bank: {missing[:5]}")
    wanted, sections, n = set(question_ids), [], 1
    for sec in bank["sections"]:
        qs = [(dict(by_id[i], marks=TYPE_MARKS[by_id[i]["type"]]) if raw else _for_pdf(by_id[i]))
              for i in question_ids if by_id[i]["section"] == sec["name"]]
        order = [t for t, _ in sec["slots"]]
        qs.sort(key=lambda q: order.index(q["type"]))
        ar = [n + k for k, q in enumerate(qs) if q["type"] == "A/R"]
        if ar and not raw:
            nums = " & ".join(str(x) for x in ar) if len(ar) <= 2 else f"{ar[0]} to {ar[-1]}"
            first = next(q for q in qs if q["type"] == "A/R")
            first["preamble"] = _markup(AR_PREAMBLE.format(nums=nums))
        n += len(qs)
        sections.append({"name": sec["name"], "title": sec["title"],
                         "marks": sec["marks"], "questions": qs})
    assert sum(len(s["questions"]) for s in sections) == len(wanted)
    meta = {k: bank[k] for k in ("subject", "class", "max_marks", "time")}
    meta["sections"] = sections
    return meta, sections


# ── calendar ─────────────────────────────────────────────────────────────────
def next_slot_dates(start: date, n: int, taken: set):
    out, d = [], start
    while len(out) < n:
        if d.weekday() in POST_WEEKDAYS and d.isoformat() not in taken:
            out.append(d)
        d += timedelta(days=1)
    return out

def plan(slots: int, start: date = None, verbose=True) -> int:
    """Assemble papers for the next `slots` posting days. Returns how many were planned."""
    cal, usage = load_calendar(), load_usage()
    used = set(usage)
    start = start or max([today_ist()] + [date.fromisoformat(d) + timedelta(days=1) for d in cal])
    done = 0
    for d in next_slot_dates(start, slots, set(cal)):
        idx = len(cal)                      # rotation position = number of slots so far
        entry, ok = {}, True
        for cls, subjects in ROTATION.items():
            sk = subjects[idx % len(subjects)]
            ids = assemble(sk, used)
            if ids is None:
                if verbose:
                    print(f"[STOP] {d}: not enough unused {sk} questions for a full paper.")
                ok = False; break
            n_prev = sum(1 for e in cal.values() if e[cls]["subject_key"] == sk)
            entry[cls] = {"subject_key": sk, "paper_id": f"{sk}-P{n_prev + 1:02d}",
                          "question_ids": ids, "posted": False}
        if not ok:
            break
        for cls, e in entry.items():
            for qid in e["question_ids"]:
                usage[qid] = {"paper": e["paper_id"], "date": d.isoformat()}
            used |= set(e["question_ids"])
        cal[d.isoformat()] = entry
        done += 1
        if verbose:
            print(f"[PLAN] {d} {d.strftime('%a')}: {entry['class10']['paper_id']} + {entry['class12']['paper_id']}")
    _save(CALENDAR, dict(sorted(cal.items()))); _save(USAGE, usage)
    return done

def entry_for(d: date):
    return load_calendar().get(d.isoformat())

def mark_posted(d: date, cls: str):
    cal = load_calendar()
    cal[d.isoformat()][cls]["posted"] = True
    cal[d.isoformat()][cls]["posted_at"] = datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")
    _save(CALENDAR, cal)

def unposted_days() -> int:
    t = today_ist().isoformat()
    return sum(1 for d, e in load_calendar().items()
               if d >= t and not all(e[c]["posted"] for c in ROTATION))


# ── validation ───────────────────────────────────────────────────────────────
def _norm(text: str) -> set:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {" ".join(words[i:i + 3]) for i in range(max(1, len(words) - 2))}

def validate(verbose=True) -> list:
    problems, seen_ids = [], {}
    legacy = {}
    try:
        from pyq_question_bank import QUESTION_BANKS
        lk = {"science10": "cl10_science", "maths10": "cl10_maths", "physics12": "cl12_physics",
              "chemistry12": "cl12_chemistry", "maths12": "cl12_maths", "biology12": "cl12_biology"}
        for sk, bk in lk.items():
            legacy[sk] = [(q["id"], q["text"]) for s in QUESTION_BANKS[bk]["sections"] for q in s["questions"]]
    except Exception as e:                                   # legacy bank is optional
        problems.append(f"could not load already-published bank for duplicate check: {e}")
    for sk in SUBJECT_FILES:
        try:
            bank = load_subject(sk)
        except Exception as e:
            problems.append(f"{sk}: cannot read file ({e})"); continue
        secs = {s["name"]: s for s in bank["sections"]}
        total = sum(TYPE_MARKS[t] * c for s in bank["sections"] for t, c in s["slots"])
        if total != bank["max_marks"]:
            problems.append(f"{sk}: blueprint adds up to {total}, not {bank['max_marks']}")
        for s in bank["sections"]:
            sm = sum(TYPE_MARKS[t] * c for t, c in s["slots"])
            if sm != s["marks"]:
                problems.append(f"{sk} {s['name']}: slots add up to {sm}, section says {s['marks']}")
        shingles = [(f"published:{i}", _norm(t)) for i, t in legacy.get(sk, [])]
        for q in bank["questions"]:
            qid = q.get("id", "?")
            if qid in seen_ids:
                problems.append(f"{sk}: duplicate id {qid}")
            seen_ids[qid] = sk
            if q.get("section") not in secs:
                problems.append(f"{qid}: unknown section {q.get('section')}")
            if q.get("type") not in TYPE_MARKS:
                problems.append(f"{qid}: unknown type {q.get('type')}")
            elif q.get("section") in secs and q["type"] not in [t for t, _ in secs[q["section"]]["slots"]]:
                problems.append(f"{qid}: type {q['type']} not used in {q['section']}")
            if not q.get("text", "").strip():
                problems.append(f"{qid}: empty text")
            if not q.get("chapter"):
                problems.append(f"{qid}: no chapter")
            if q.get("type") == "MCQ":
                opts = q.get("options", [])
                if len(opts) != 4 or [o[:3] for o in opts] != ["(A)", "(B)", "(C)", "(D)"]:
                    problems.append(f"{qid}: MCQ needs options (A)-(D)")
                if len({o[3:].strip().lower() for o in opts}) != len(opts):
                    problems.append(f"{qid}: two options are identical")
            if q.get("type") in ("MCQ", "A/R") and q.get("answer") not in ("(A)", "(B)", "(C)", "(D)"):
                problems.append(f"{qid}: answer must be (A)/(B)/(C)/(D)")
            if q.get("type") == "A/R" and not ("Assertion (A):" in q.get("text", "") and "Reason (R):" in q.get("text", "")):
                problems.append(f"{qid}: A/R text must contain 'Assertion (A):' and 'Reason (R):'")
            sh = _norm(q.get("text", ""))
            for other, osh in shingles:
                inter = len(sh & osh)
                if inter >= 6 and inter / max(1, min(len(sh), len(osh))) > 0.7:
                    problems.append(f"{qid}: looks like a repeat of {other}")
            shingles.append((qid, sh))
    usage = load_usage()
    for qid in usage:
        if qid not in seen_ids:
            problems.append(f"usage log refers to a question that is no longer in the bank: {qid}")
    if verbose:
        print("\n".join(problems) if problems else "Pool is clean: no problems found.")
    return problems

def stock(verbose=True) -> dict:
    used, out = set(load_usage()), {}
    for sk in SUBJECT_FILES:
        bank = load_subject(sk)
        out[sk] = {"questions": len(bank["questions"]),
                   "used": sum(1 for q in bank["questions"] if q["id"] in used),
                   "fresh_papers": papers_left(sk, used)}
        if verbose:
            o = out[sk]
            print(f"{sk:12s} {o['questions']:4d} questions, {o['used']:4d} used, {o['fresh_papers']:2d} fresh papers left")
    if verbose:
        print(f"Posting days planned and not yet posted: {unposted_days()}")
    return out


def need(days: int = 6, verbose=True) -> dict:
    """
    What must be written so that `days` future paper days are planned.
    Returns {subject_key: {"papers": n, "short": {(section, type): count}}}.
    """
    cal, used = load_calendar(), set(load_usage())
    t = today_ist().isoformat()
    planned_ahead = sum(1 for d_ in cal if d_ > t)
    missing_days = max(0, days - planned_ahead)
    want = {}
    for i in range(missing_days):
        for subjects in ROTATION.values():
            sk = subjects[(len(cal) + i) % len(subjects)]
            want[sk] = want.get(sk, 0) + 1
    out = {}
    for sk, papers in want.items():
        bank = load_subject(sk)
        short = {}
        for sec in bank["sections"]:
            for qtype, count in sec["slots"]:
                have = sum(1 for q in bank["questions"]
                           if q["id"] not in used and q["section"] == sec["name"] and q["type"] == qtype)
                if papers * count > have:
                    short[(sec["name"], qtype)] = papers * count - have
        out[sk] = {"papers": papers, "short": short}
    if verbose:
        print(f"Paper days planned after today: {planned_ahead}. Target: {days}. Days still to plan: {missing_days}.")
        for sk, o in out.items():
            print(f"{sk}: {o['papers']} more paper(s) needed.")
            for (sec, qtype), n in o["short"].items():
                print(f"    write {n:3d} x {qtype:4s} for {sec}")
            if not o["short"]:
                print("    enough unused questions already in the pool")
        if not out:
            print("Nothing to write: the calendar already covers the target.")
        else:
            print(f"After adding the questions run: python3 mock_bank.py plan --slots {missing_days}")
    return out


def main():
    ap = argparse.ArgumentParser(description="Mock paper question pool")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate"); sub.add_parser("stock")
    p = sub.add_parser("plan"); p.add_argument("--slots", type=int, default=6); p.add_argument("--start")
    v = sub.add_parser("preview"); v.add_argument("--out", required=True)
    n = sub.add_parser("need"); n.add_argument("--days", type=int, default=6)
    a = ap.parse_args()
    if a.cmd == "validate":
        sys.exit(1 if validate() else 0)
    if a.cmd == "stock":
        stock()
    if a.cmd == "need":
        need(a.days)
    if a.cmd == "plan":
        if validate(verbose=False):
            validate(); sys.exit("Fix the problems above before planning.")
        plan(a.slots, date.fromisoformat(a.start) if a.start else None)
    if a.cmd == "preview":
        from mock_paper_pdf import build_mock_pdf
        out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
        for d, e in load_calendar().items():
            if d < today_ist().isoformat():
                continue
            for cls in ROTATION:
                if e[cls]["posted"]:
                    continue
                meta, _ = paper_sections(e[cls]["subject_key"], e[cls]["question_ids"], raw=True)
                pd_ = date.fromisoformat(d).strftime("%d %B %Y")
                f = out / f"{e[cls]['subject_key']}_{d}.pdf"
                build_mock_pdf(meta, str(f), pd_, paper_id=e[cls]["paper_id"])
                print(f"[PDF] {f}")


if __name__ == "__main__":
    main()
