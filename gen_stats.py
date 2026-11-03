#!/usr/bin/env python3
"""
gen_stats.py — Scans all portal HTML files and writes stats.json
                + updates the hero stat numbers in index.html automatically.

Run after adding any new portal:
  python3 gen_stats.py

GitHub Actions: trigger on push to main
  - run: python3 gen_stats.py
  - run: git add stats.json index.html && git diff --cached --quiet || git commit -m "chore: auto-update stats" && git push

What it counts:
  - Total HTML portal files (root + resources/)
  - Approximate question count (parses MCQ/SA/LA markers)
  - Last-updated date per file
  - Outputs stats.json for the JS countdown widget to consume
"""

import os, re, json
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(__file__)
RES_DIR  = os.path.join(BASE_DIR, "resources")

EXCLUDE = {"news.html", "sitemap.html"}  # not exam portals

def count_questions_in_file(path):
    """Rough count: MCQ options (A/B/C/D) blocks = 1 question each."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        # Count question markers: numbered items like (1) or Q1. or question blocks
        mcq   = len(re.findall(r'<li[^>]*>.*?\(A\)', text))
        sa_la = len(re.findall(r'class="[^"]*question[^"]*"', text))
        return max(mcq + sa_la, 0)
    except Exception:
        return 0

def scan_files():
    files = []
    for fname in os.listdir(BASE_DIR):
        if fname.endswith(".html") and fname not in EXCLUDE and not fname.startswith("."):
            files.append(("root", fname, os.path.join(BASE_DIR, fname)))
    if os.path.isdir(RES_DIR):
        for fname in os.listdir(RES_DIR):
            if fname.endswith(".html"):
                files.append(("resources", fname, os.path.join(RES_DIR, fname)))
    return files

def build_stats():
    files = scan_files()
    total_portals = len(files)
    total_q = 0
    subjects = []
    for folder, fname, path in sorted(files):
        q = count_questions_in_file(path)
        total_q += q
        mtime = datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc).strftime("%Y-%m-%d")
        subjects.append({"file": fname, "folder": folder, "questions": q, "updated": mtime})

    # Practice papers: each resources/ file has 5 units = 5 papers; root files = 1 each
    root_count = sum(1 for f in files if f[0] == "root")
    res_count  = sum(1 for f in files if f[0] == "resources")
    total_papers = root_count + res_count * 5

    stats = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_portals": total_portals,
        "total_papers": total_papers,
        "total_questions_approx": total_q,
        "subjects": subjects,
    }
    return stats

def update_index_stats(stats):
    idx = os.path.join(BASE_DIR, "index.html")
    with open(idx, encoding="utf-8") as f:
        html = f.read()

    def replace_stat(html, old_num, label, new_num):
        pattern = rf'(<div class="stat-num">){re.escape(str(old_num))}(</div><div class="stat-label">{re.escape(label)}</div>)'
        replacement = rf'\g<1>{new_num}\2'
        return re.sub(pattern, replacement, html)

    # Only update if numbers changed to avoid noisy commits
    portals_str = str(stats["total_portals"])
    papers_str  = str(stats["total_papers"]) + "+"

    html2 = re.sub(
        r'(<div class="stat-num">)\d+?(</div><div class="stat-label">Subjects</div>)',
        rf'\g<1>{portals_str}\2', html)
    html2 = re.sub(
        r'(<div class="stat-num">)[\d+]+(</div><div class="stat-label">Practice Papers</div>)',
        rf'\g<1>{papers_str}\2', html2)

    if html2 != html:
        with open(idx, "w", encoding="utf-8") as f:
            f.write(html2)
        print(f"  index.html updated → {portals_str} portals, {papers_str} papers")
    else:
        print("  index.html unchanged")

if __name__ == "__main__":
    print("Scanning portal files...")
    stats = build_stats()

    out = os.path.join(BASE_DIR, "stats.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"Written: {out}")
    print(f"  Portals : {stats['total_portals']}")
    print(f"  Papers  : {stats['total_papers']}")
    print(f"  ~Questions: {stats['total_questions_approx']}")

    update_index_stats(stats)
    print("Done.")
