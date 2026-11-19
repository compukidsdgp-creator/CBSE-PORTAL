"""Floating share buttons on every shareable page.  python3 share_tags.py [files...]  (no args = every site page).

Adds <script src="/share-fab.js" defer></script> before </body> on public pages that do not already have share buttons.
Idempotent. Skips locked/frozen pages, drafts, noindex pages, redirects, admin and link-in-bio pages.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOCKED = {"resources/physics-xii-new.html", "resources/physics-xii-new-backup.html", "resources/ai-x.html", "resources/cs-xii.html"}  # locked or owner-frozen
SKIP_DIRS = ("admin/", "go/", "ads/", "tts-samples/", "promo-posters/", "social-images/", "mistake_reels/",
             "why_reels/", "assets/", "tools/", "node_modules/")
FROZEN_SUBJECT_TITLES = re.compile(r"Class 10 Artific|Class 12 Compute")   # owner-frozen subjects
TAG = '<script src="/share-fab.js" defer></script>'


def add(path):
    p = Path(path)
    try:
        rel = p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return False
    if rel in LOCKED or rel.startswith(SKIP_DIRS) or "/_drafts/" in rel or not p.exists():
        return False
    s = p.read_text(encoding="utf-8", errors="ignore")
    low = s.lower()
    if ("share-fab" in s or "</body>" not in low or 'http-equiv="refresh"' in low[:3000]
            or re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', s[:6000], re.I)
            or re.search(r'^google[0-9a-f]+\.html$', p.name)):
        return False
    title = re.search(r"<title>([^<]*)", s, re.I)
    if title and FROZEN_SUBJECT_TITLES.search(title.group(1)):
        return False
    i = low.rfind("</body>")
    p.write_text(s[:i] + TAG + "\n" + s[i:], encoding="utf-8")
    return True


if __name__ == "__main__":
    files = sys.argv[1:] or [f for f in subprocess.run(["git", "ls-files", "-z", "*.html"], cwd=ROOT,
                                                       capture_output=True, text=True).stdout.split("\0") if f]
    n = sum(add(ROOT / f if not Path(f).is_absolute() else f) for f in files)
    print(f"[share] buttons added to {n} pages")
