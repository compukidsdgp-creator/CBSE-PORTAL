#!/usr/bin/env python3
"""Generate a canonical, recursive XML sitemap for CBSEMOCK.

Includes public HTML pages only, omits pages marked noindex (incl. redirect
stubs left at old URLs) and pages whose canonical points to a different URL,
and adds <lastmod> from the last git commit that touched each page.
Run from any working directory with Python 3 (needs full git history for
accurate dates: actions/checkout with fetch-depth: 0).
"""
from __future__ import annotations

import os
import re
import html
import subprocess
from pathlib import Path
from urllib.parse import quote

DOMAIN = "https://cbsemock.org.in"
BASE_DIR = Path(__file__).resolve().parent
EXCLUDED_DIRS = {".git", ".github", "node_modules", "__pycache__"}
EXCLUDED_NAME_RE = re.compile(r"(?:^|[-_.])(backup|draft|old|archive|temp|tmp)(?:[-_.]|$)", re.I)


def canonical_for(path: Path) -> str:
    rel = path.relative_to(BASE_DIR).as_posix()
    parts = rel.split("/")
    if parts[-1].lower() == "index.html":
        parts = parts[:-1]
        return DOMAIN + ("/" + "/".join(quote(p, safe="-._~()'") for p in parts) if parts else "") + "/"
    return DOMAIN + "/" + "/".join(quote(p, safe="-._~()'") for p in parts)


def is_indexable(path: Path) -> bool:
    rel_parts = path.relative_to(BASE_DIR).parts
    if any(part in EXCLUDED_DIRS for part in rel_parts):
        return False
    if EXCLUDED_NAME_RE.search(path.stem):
        return False
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    if re.search(r'<meta\b(?=[^>]*\bname=["\']robots["\'])[^>]*\bcontent=["\'][^"\']*noindex', content, re.I):
        return False
    if re.search(r'<meta\b[^>]*http-equiv=["\']refresh', content, re.I):
        return False
    m = re.search(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*\bhref=["\']([^"\']+)', content, re.I)
    if m and m.group(1).strip().rstrip("/") != canonical_for(path).rstrip("/"):
        return False                      # page declares another URL as the real one
    return True


def git_lastmod() -> dict[str, str]:
    """path -> YYYY-MM-DD of the newest commit touching it (one git call)."""
    try:
        out = subprocess.run(["git", "-c", "core.quotepath=off", "log", "--format=@%cs", "--name-only", "--", "*.html"],
                             cwd=BASE_DIR, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return {}
    dates, cur = {}, None
    for line in out.splitlines():
        if line.startswith("@"):
            cur = line[1:]
        elif line and cur:
            dates.setdefault(line, cur)
    return dates


def collect_urls() -> list[tuple[str, str]]:
    dates = git_lastmod()
    urls = {}
    for path in BASE_DIR.rglob("*.html"):
        if is_indexable(path):
            urls[canonical_for(path)] = dates.get(path.relative_to(BASE_DIR).as_posix(), "")
    # home first, then section hubs (…/), then pages
    return sorted(urls.items(), key=lambda kv: (kv[0] != DOMAIN + "/", not kv[0].endswith("/"), kv[0]))


def build_sitemap(urls: list[tuple[str, str]]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url, lastmod in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{html.escape(url)}</loc>")
        if lastmod:
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    urls = collect_urls()
    output = BASE_DIR / "sitemap.xml"
    output.write_text(build_sitemap(urls), encoding="utf-8")
    print(f"Written: {output} ({len(urls)} canonical URLs)")
