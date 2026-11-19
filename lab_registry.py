"""Virtual-lab rebuild tracker: every lab in every subject, against the locked standard (virtual-labs/LAB_STANDARD.md).

States: legacy (old design) → draft (rebuilt, in virtual-labs/<subject>/_drafts/, awaiting approval)
        → changes (owner asked for changes) → live (approved; meets the standard).
    python3 lab_registry.py next      → JSON: what tonight's run should do
    python3 lab_registry.py status    → progress per subject
    python3 lab_registry.py claim <id> → mark a lab as being built (parallel nightly runs skip it for 8 h)
    python3 lab_registry.py queue     → rebuild (re)write labs_content/queue.json (board-practical labs first)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LABS = ROOT / "virtual-labs"
SRC = ROOT / "labs_content"
STANDARD_META = 'name="cbse-lab-standard"'
REFERENCE = "physics/convex-lens-focal-length.html"
SUBJECTS = [("physics", "Physics"), ("chemistry", "Chemistry"), ("biology", "Biology"),
            ("mathematics", "Mathematics"), ("computer-science", "Computer Science"), ("ai-ml", "AI / ML")]
# CBSE board-practical experiments first (Class 10 Science, Class 12 Physics/Chemistry/Biology, CS practical file, AI).
PRIORITY = {
    "physics": ["01-ohm-s-law", "03-parallel-circuit", "02-series-circuit", "14-refraction-through-a-glass-slab",
                "19-refraction-through-a-prism", "17-concave-mirror-image-formation", "15-convex-lens-image-formation",
                "23-simple-pendulum", "04-combination-of-resistors", "22-human-eye-and-defects-of-vision"],
    "chemistry": ["39-titration-and-endpoint", "02-ph-scale-explorer", "01-acid-base-indicator-lab", "08-types-of-chemical-reactions",
                  "06-displacement-reactions", "32-esterification-reaction", "33-soap-and-detergent-cleaning",
                  "17-rate-of-reaction-concentration", "18-rate-of-reaction-temperature", "40-organic-functional-group-identifier"],
    "biology": ["07-stomata-and-leaf-impressions", "12-cellular-respiration-in-germinating-seeds", "09-photosynthesis-starch-test",
                "22-mitosis-onion-root-tip", "25-pollen-germination-model", "34-dna-extraction-from-fruit",
                "37-quadrat-sampling-population-estimate", "39-water-quality-and-aquatic-ecosystem", "05-osmosis-with-potato-strips",
                "02-onion-peel-cell-study"],
    "mathematics": ["07-pythagoras-theorem-lab", "12-heights-distances-simulator", "03-pair-of-linear-equations-lab",
                    "16-cumulative-frequency-ogive-lab", "20-integration-area-under-curve-lab"],
    "computer-science": ["lab-55", "lab-50", "lab-52", "lab-53", "lab-54", "lab-71", "lab-74", "lab-75", "lab-76", "lab-77",
                         "lab-07", "lab-25", "lab-33"],
    "ai-ml": ["ai-data-exploration", "ai-lab-data-exploration-image-classifier", "ml-knn", "ai-confusion-matrix",
              "ml-linear-regression", "ml-decision-tree", "ai-train-test", "ai-nlp", "ai-computer-vision"],
}


def is_redirect(text):
    return 'http-equiv="refresh"' in text or "<title>Moved" in text


def title_of(text, fallback):
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    t = (m.group(1) if m else fallback).replace("&#x27;", "'").replace("&amp;", "&")
    t = re.sub(r"^CBSEMOCK \| |\s*[|·—-]\s*CBSEMOCK.*$|\s*Virtual Lab$|— Virtual Lab \| CBSEMock$", "", t, flags=re.I).strip()
    t = re.sub(r"^(Math(ematics)? Lab|Biology Lab|Lab) \d+\s*\|?\s*", "", t).strip(" |")
    return t or fallback


def approvals():
    try:
        return json.loads((SRC / "approvals.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def labs():
    appr = approvals()
    out = []
    for key, name in SUBJECTS:
        d = LABS / key
        for f in sorted(d.glob("*.html")):
            if f.name == "index.html":
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
            if is_redirect(text):
                continue
            lid = f"{key}/{f.stem}"
            draft = d / "_drafts" / f.name
            a = appr.get(lid, {})
            if STANDARD_META in text and not draft.exists():
                state = "live"
            elif draft.exists():
                state = "changes" if a.get("status") == "changes" else "draft"
            else:
                state = "legacy"
            src = draft if draft.exists() else f
            out.append({"id": lid, "subject_key": key, "subject": name, "file": f"virtual-labs/{key}/{f.name}",
                        "title": title_of(src.read_text(encoding="utf-8", errors="ignore"), f.stem.replace("-", " ").title()),
                        "state": state, "note": a.get("note", "") if state == "changes" else "",
                        "draft": f"virtual-labs/{key}/_drafts/{f.name}" if draft.exists() else "",
                        "url": f"virtual-labs/{key}/{'_drafts/' if draft.exists() else ''}{f.name}"})
    return out


def build_queue(items=None):
    items = items or labs()
    per = {}
    for key, _ in SUBJECTS:
        sub = [x for x in items if x["subject_key"] == key]
        pri = [f"{key}/{s}" for s in PRIORITY.get(key, []) if any(x["id"] == f"{key}/{s}" for x in sub)]
        rest = [x["id"] for x in sub if x["id"] not in pri]
        per[key] = pri + rest
    order = []
    # board-practical labs first, rotating subjects so every subject moves forward
    while any(per.values()):
        for key, _ in SUBJECTS:
            if per[key]:
                order.append(per[key].pop(0))
    (SRC / "queue.json").write_text(json.dumps(order, indent=1) + "\n", encoding="utf-8")
    return order


def queue():
    try:
        q = json.loads((SRC / "queue.json").read_text(encoding="utf-8"))
    except Exception:
        q = build_queue()
    known = {x["id"] for x in labs()}
    return [i for i in q if i in known] + sorted(known - set(q))


def claimed(hours=8):
    """Labs claimed by a nightly run in the last few hours (labs_content/claims.json), so parallel runs never collide."""
    import time
    try:
        c = json.loads((SRC / "claims.json").read_text(encoding="utf-8"))
    except Exception:
        return set()
    return {k for k, t in c.items() if time.time() - t < hours * 3600}


def claim(lab_id):
    import time
    try:
        c = json.loads((SRC / "claims.json").read_text(encoding="utf-8"))
    except Exception:
        c = {}
    c = {k: t for k, t in c.items() if time.time() - t < 48 * 3600}
    c[lab_id] = int(time.time())
    (SRC / "claims.json").write_text(json.dumps(c, indent=1) + "\n", encoding="utf-8")


def next_job():
    items = {x["id"]: x for x in labs()}
    rev = [x for x in items.values() if x["state"] == "changes" and x["id"] not in claimed()]
    if rev:
        x = rev[0]
        return {"action": "revise", **x}
    pending = [x for x in items.values() if x["state"] == "draft"]
    skip = claimed()                             # labs another run is building right now
    for i in queue():
        if i in skip:
            continue
        x = items[i]
        if x["state"] == "legacy":
            return {"action": "build", "drafts_waiting": len(pending), **x,
                    "draft_path": f"virtual-labs/{x['subject_key']}/_drafts/{Path(x['file']).name}"}
    return {"action": "none"}


def admin_data():
    items = labs()
    q = queue()
    pos = {i: n for n, i in enumerate(q)}
    subs = []
    for key, name in SUBJECTS:
        rows = [x for x in items if x["subject_key"] == key]
        rows.sort(key=lambda x: pos.get(x["id"], 9999))
        subs.append({"key": key, "name": name, "total": len(rows),
                     "live": sum(r["state"] == "live" for r in rows),
                     "draft": sum(r["state"] in ("draft", "changes") for r in rows), "rows": rows})
    tot = len(items)
    return {"subjects": subs, "totals": {"labs": tot, "live": sum(x["state"] == "live" for x in items),
                                         "draft": sum(x["state"] == "draft" for x in items),
                                         "changes": sum(x["state"] == "changes" for x in items),
                                         "legacy": sum(x["state"] == "legacy" for x in items)},
            "next": next_job(), "reference": f"virtual-labs/{REFERENCE}"}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "next"
    if cmd == "claim":
        claim(sys.argv[2]); print("claimed", sys.argv[2])
    elif cmd == "queue":
        print(len(build_queue()), "labs queued")
    elif cmd == "status":
        d = admin_data()
        for s in d["subjects"]:
            print(f"{s['name']:<18} {s['live']:>3} live  {s['draft']:>3} draft  / {s['total']}")
        print(d["totals"])
    else:
        print(json.dumps(next_job(), indent=1, ensure_ascii=False))
