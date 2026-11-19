#!/usr/bin/env python3
"""
mockzone_build.py — 15 genuinely different practice papers per Mock Zone subject page.

Each converted page keeps its own layout and render code, but its question pools live in a bank file
    mockzone_bank/<page-stem>.json   {"page": "...html", "pools": {"POOL": {"per_paper": k, "items": [...]}}}
and are injected between  /* MZ-POOLS:START */ … /* MZ-POOLS:END */  in the page's script.
Paper n (0–14) takes items [n·k, (n+1)·k) of every pool (mzPick), so a pool with 15·k items means
NO question appears in two papers. Until a pool is full, the missing papers wrap round (old behaviour).

Commands
  python3 mockzone_build.py init PAGE.html POOL:k [POOL:k ...]   one-time: copy a page's pools into a bank + add markers
  python3 mockzone_build.py build [PAGE ...]                     write banks into their pages
  python3 mockzone_build.py check [PAGE ...]                     duplicates / near-duplicates / shape errors (exit 1 on error)
  python3 mockzone_build.py status                               progress table: fresh papers per page
  python3 mockzone_build.py next                                 the page + paper the nightly run should write next
"""
import json
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BANK = ROOT / "mockzone_bank"
A, B = "/* MZ-POOLS:START */", "/* MZ-POOLS:END */"
PAPERS = 15
EXCLUDED = {"cbse-class-10-ai-mock-papers.html", "cbse-class-12-computer-science-mock-papers.html"}   # owner: leave as is
PRIORITY = [          # search demand first; AI X and CS XII are excluded by the owner
    "cbse-class-12-physics-mock-papers.html", "cbse-class-12-english-core-mock-papers.html",
    "cbse-class-12-chemistry-mock-papers.html", "cbse-class-12-maths-mock-papers.html",
    "cbse-class-12-biology-mock-papers.html", "cbse-class-10-science-mock-tests.html",
    "cbse-class-10-maths-standard-mock-tests.html", "cbse-class-10-social-science-mock-tests.html",
    "cbse-class-10-maths-basic-mock-tests.html", "cbse-class-10-english-language-literature-mock-tests.html",
    "cbse-class-10-english-communicative-mock-tests.html", "cbse-class-10-hindi-course-a-mock-tests.html",
    "cbse-class-10-computer-applications-mock-tests.html", "cbse-class-12-informatics-practices-practice-papers.html",
    "cbse-class-12-physical-education-practice-papers.html", "cbse-class-12-english-elective-practice-papers.html",
    "cbse-class-12-bengali-practice-papers.html",
]
NEAR = 0.82            # similarity above this between two question texts = near-duplicate

HELPER = """function mzPick(pool, k, n){ /* paper n gets its own block of k items; wraps only while the pool is short */
  const out=[], L=pool.length; for(let i=0;i<k;i++) out.push(pool[(n*k+i)%L]); return out; }"""


def bank_path(page):
    return BANK / (Path(page).stem + ".json")


def load(page):
    return json.loads(bank_path(page).read_text(encoding="utf-8"))


def banks(pages=None):
    out = sorted(BANK.glob("*.json"))
    if pages:
        want = {Path(p).stem for p in pages}
        out = [b for b in out if b.stem in want]
    return out


def js_block(bank):
    lines = [A]
    for name, pool in bank["pools"].items():
        arr = json.dumps(pool["items"], ensure_ascii=False, indent=0).replace("</", "<\\/")
        lines.append(f"const {name} = {arr};")
    lines.append("const MZ_K = " + json.dumps({n: p["per_paper"] for n, p in bank["pools"].items()}) + ";")
    lines.append(HELPER)
    lines.append(B)
    return "\n".join(lines)


def build(pages=None):
    for bf in banks(pages):
        bank = json.loads(bf.read_text(encoding="utf-8"))
        f = ROOT / bank["page"]
        s = f.read_text(encoding="utf-8")
        if A not in s:
            print(f"[mz] {bank['page']}: no markers — run init first"); continue
        new = re.sub(re.escape(A) + r".*?" + re.escape(B), lambda m: js_block(bank), s, count=1, flags=re.S)
        if new != s:
            f.write_text(new, encoding="utf-8")
        print(f"[mz] {bank['page']}: {'updated' if new != s else 'unchanged'}")


# ── checks ───────────────────────────────────────────────────────────────────
def text_of(item):
    if isinstance(item, str):
        return item
    parts = [str(item.get(k, "")) for k in ("q", "question", "text", "passage", "stem", "title", "orq")]
    t = " ".join(p for p in parts if p)
    return t or json.dumps(item, ensure_ascii=False)


def norm(t):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", t.lower())).strip()


def check_bank(bank):
    errs, warns = [], []
    seen = []                                   # (norm text, where)
    for name, pool in bank["pools"].items():
        items, k = pool["items"], pool["per_paper"]
        if not items:
            errs.append(f"{name}: empty pool"); continue
        keys0 = set(items[0].keys()) if isinstance(items[0], dict) else None
        for i, it in enumerate(items):
            where = f"{name}[{i}] (paper {i // k + 1})"
            if keys0 is not None:
                if not isinstance(it, dict):
                    errs.append(f"{where}: not an object"); continue
                missing = keys0 - set(it.keys())
                if missing:
                    errs.append(f"{where}: missing fields {sorted(missing)}")
                for fld, v in it.items():
                    if isinstance(v, str) and not v.strip():
                        errs.append(f"{where}: empty '{fld}'")
                if "opts" in it and "ans" in it and isinstance(it["opts"], list) and isinstance(it["ans"], str):
                    letters = [re.match(r"\s*\(?([A-Da-d])[\.\)]", o or "") for o in it["opts"]]
                    if all(letters) and it["ans"].strip()[:1].upper() not in {m.group(1).upper() for m in letters}:
                        errs.append(f"{where}: answer '{it['ans']}' is not one of the options")
            t = norm(text_of(it))
            for t2, w2 in seen:
                if t == t2:
                    errs.append(f"{where}: exact duplicate of {w2}"); break
                if abs(len(t) - len(t2)) < 0.3 * max(len(t), len(t2)) and SequenceMatcher(None, t, t2).ratio() > NEAR:
                    errs.append(f"{where}: near-duplicate of {w2}"); break
            seen.append((t, where))
        if len(items) > PAPERS * k:
            warns.append(f"{name}: {len(items)} items, only {PAPERS * k} are used")
    return errs, warns


def check(pages=None):
    bad = 0
    for bf in banks(pages):
        bank = json.loads(bf.read_text(encoding="utf-8"))
        errs, warns = check_bank(bank)
        for w in warns:
            print(f"  [warn] {bank['page']}: {w}")
        for e in errs:
            print(f"  [ERROR] {bank['page']}: {e}")
        bad += len(errs)
        print(f"[check] {bank['page']}: {'OK' if not errs else str(len(errs)) + ' error(s)'}")
    return bad


def fresh_papers(bank):
    return min(len(p["items"]) // p["per_paper"] for p in bank["pools"].values())


def status():
    print(f"{'page':58} {'fresh papers':>12}  pools short")
    for bf in banks():
        bank = json.loads(bf.read_text(encoding="utf-8"))
        short = [f"{n} {len(p['items'])}/{PAPERS * p['per_paper']}" for n, p in bank["pools"].items() if len(p["items"]) < PAPERS * p["per_paper"]]
        print(f"{bank['page']:58} {fresh_papers(bank):>8}/{PAPERS}  {', '.join(short) if short else '— complete'}")


def next_job():
    """The page tonight's run should work on, and what to do."""
    for page in PRIORITY:
        if not bank_path(page).exists():
            return {"page": page, "action": "convert", "next_paper": 2}
        bank = load(page)
        f = fresh_papers(bank)
        if f < PAPERS:
            return {"page": page, "action": "write", "next_paper": f + 1,
                    "need_per_paper": {n: p["per_paper"] for n, p in bank["pools"].items()}}
    return {"action": "none"}


# ── one-time conversion ──────────────────────────────────────────────────────
def extract_pools(page, names):
    js = r"""
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.route(/^https?:/,r=>r.abort());await p.goto('file://'+process.argv[1]);await p.waitForTimeout(300);
const r=await p.evaluate(ns=>{const o={};for(const n of ns)o[n]=eval(n);return o},JSON.parse(process.argv[2]));
console.log(JSON.stringify(r));await b.close()})();"""
    out = subprocess.run(["node", "-e", js, str(ROOT / page), json.dumps(names)], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def init(page, specs):
    if page in EXCLUDED:
        sys.exit(f"{page} is excluded from the Mock Zone rewrite")
    ks = {}
    for sp in specs:
        n, k = sp.split(":")
        ks[n] = int(k)
    pools = extract_pools(page, list(ks))
    bank = {"page": page, "pools": {n: {"per_paper": ks[n], "items": pools[n]} for n in ks}}
    BANK.mkdir(exist_ok=True)
    bank_path(page).write_text(json.dumps(bank, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    f = ROOT / page
    s = f.read_text(encoding="utf-8")
    if A not in s:
        # the pools must be contiguous: from the first pool declaration to the end of the last one
        starts = [re.search(rf"(?:const|let|var)\s+{n}\s*=\s*\[", s) for n in ks]
        if not all(starts):
            sys.exit("could not find every pool declaration")
        first = min(m.start() for m in starts)
        last = max(starts, key=lambda m: m.start())
        end = s.index("];", last.end()) + 2
        between = s[first:end]
        if re.search(r"^\s*(?:function\s+\w+\s*\(|(?:const|let|var)\s+\w+\s*=(?!\s*\[))", between, re.M):
            sys.exit("pools are not contiguous (code between them) — move them together first")
        s = s[:first] + js_block(bank) + s[end:]
        f.write_text(s, encoding="utf-8")
    print(f"[mz] {page}: bank written ({sum(len(p['items']) for p in bank['pools'].values())} items). "
          f"Now change buildPaper to use mzPick(POOL, MZ_K.POOL, n).")


if __name__ == "__main__":
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("status", [])
    if cmd == "init":
        init(args[0], args[1:])
    elif cmd == "build":
        build(args)
    elif cmd == "check":
        sys.exit(1 if check(args) else 0)
    elif cmd == "next":
        print(json.dumps(next_job(), indent=1))
    elif cmd == "status":
        status()
    else:
        sys.exit(__doc__)
