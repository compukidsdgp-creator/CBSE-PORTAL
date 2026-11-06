#!/usr/bin/env python3
"""Generate a canonical, recursive XML sitemap for CBSEMOCK.

Includes public HTML pages only, follows each page's canonical URL, and omits
pages marked noindex. Run from any working directory with Python 3.
"""
from __future__ import annotations

import os
import re
import html
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
    return True


def collect_urls() -> list[str]:
    urls = []
    for path in BASE_DIR.rglob("*.html"):
        if is_indexable(path):
            urls.append(canonical_for(path))
    return sorted(set(urls))


def build_sitemap(urls: list[str]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in urls:
        lines.extend(["  <url>", f"    <loc>{html.escape(url)}</loc>", "  </url>"])
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    urls = collect_urls()
    output = BASE_DIR / "sitemap.xml"
    output.write_text(build_sitemap(urls), encoding="utf-8")
    print(f"Written: {output} ({len(urls)} canonical URLs)")
