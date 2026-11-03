#!/usr/bin/env python3
"""
gen_sitemap.py — Auto-generates sitemap.xml for cbsemock.org.in
Run after any portal update, or via GitHub Actions on every push.

GitHub Actions usage (add to .github/workflows/sitemap.yml):
  on: [push]
  steps:
    - uses: actions/checkout@v4
    - run: python3 gen_sitemap.py
    - run: git config user.name "sitemap-bot" && git config user.email "bot@cbsemock.org.in"
    - run: git add sitemap.xml && git diff --cached --quiet || git commit -m "chore: update sitemap" && git push
"""

import os
from datetime import datetime, timezone

DOMAIN = "https://cbsemock.org.in"
BASE_DIR = os.path.dirname(__file__)

# Priority map: higher = more important for SEO
PRIORITY = {
    "index.html": ("1.0", "daily"),
    "news.html":  ("0.9", "daily"),
}
DEFAULT_PRIORITY = ("0.8", "weekly")

def collect_urls():
    urls = []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Root-level HTML files
    for fname in sorted(os.listdir(BASE_DIR)):
        if not fname.endswith(".html"):
            continue
        if fname.startswith("."):
            continue
        pri, freq = PRIORITY.get(fname, ("0.7", "weekly"))
        loc = f"{DOMAIN}/{fname}" if fname != "index.html" else DOMAIN + "/"
        urls.append((loc, today, freq, pri))

    # resources/ subfolder
    res_dir = os.path.join(BASE_DIR, "resources")
    if os.path.isdir(res_dir):
        for fname in sorted(os.listdir(res_dir)):
            if not fname.endswith(".html"):
                continue
            loc = f"{DOMAIN}/resources/{fname}"
            urls.append((loc, today, "monthly", "0.8"))

    return urls

def build_sitemap(urls):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, freq, pri in urls:
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{lastmod}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{pri}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    return "\n".join(lines)

if __name__ == "__main__":
    urls = collect_urls()
    xml = build_sitemap(urls)
    out = os.path.join(BASE_DIR, "sitemap.xml")
    with open(out, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"Written: {out}  ({len(urls)} URLs)")
