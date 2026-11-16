"""Favicon <link> tags for every page.  python3 favicon_tags.py [files...]  (no args = every site page).

Idempotent: pages that already carry the block are left alone. The locked Physics XII notes page is never touched.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOCKED = {"resources/physics-xii-new.html"}
MARK = "<!-- favicon -->"
TAGS = (MARK + '<link rel="icon" href="/favicon.ico" sizes="48x48">'
        '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">'
        '<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">'
        '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">'
        '<link rel="manifest" href="/site.webmanifest">')


def add(path):
    p = Path(path)
    rel = str(p.resolve().relative_to(ROOT)) if p.is_absolute() or (ROOT / p).exists() else str(p)
    if rel in LOCKED or not p.exists():
        return False
    s = p.read_text(encoding="utf-8", errors="ignore")
    if MARK in s or "</head>" not in s.lower() or 'http-equiv="refresh"' in s[:3000]:
        return False
    m = re.search(r'<meta[^>]+name=["\']?viewport[^>]*>', s, re.I)
    i = m.end() if m else re.search(r"</head>", s, re.I).start()
    p.write_text(s[:i] + TAGS + s[i:], encoding="utf-8")
    return True


if __name__ == "__main__":
    files = sys.argv[1:] or [f for f in subprocess.run(["git", "ls-files", "-z", "*.html"], cwd=ROOT,
                                                       capture_output=True, text=True).stdout.split("\0") if f]
    n = sum(add(ROOT / f if not Path(f).is_absolute() else f) for f in files)
    print(f"[favicon] tags added to {n} pages")
