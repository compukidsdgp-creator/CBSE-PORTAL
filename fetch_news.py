#!/usr/bin/env python3
"""
fetch_news.py — CBSE News Auto-Updater for cbsemock.org.in
─────────────────────────────────────────────────────────────
Run daily (cron / GitHub Actions) to pull fresh CBSE news from
Google News RSS and write news.html into the Portal folder.

GitHub Actions cron (add to .github/workflows/news.yml):
  schedule:
    - cron: '0 4 * * *'   # 9:30 AM IST daily
  steps:
    - uses: actions/checkout@v4
    - run: python3 fetch_news.py
    - run: git config user.name "cbse-news-bot" && git config user.email "bot@cbsemock.org.in"
    - run: git add news.html && git diff --cached --quiet || git commit -m "chore: daily news update" && git push

Usage locally:
  python3 fetch_news.py
"""

import urllib.request
import xml.etree.ElementTree as ET
import html
import os
import re
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────
QUERIES = [
    "CBSE board exam 2027",
    "CBSE date sheet 2027",
    "CBSE curriculum and syllabus 2026-27",
    "CBSE Class 10 Class 12 result 2026",
    "CBSE circular notification 2026",
]
MAX_ITEMS = 15
OUT_PATH = os.path.join(os.path.dirname(__file__), "news.html")

# ── Fetch RSS ─────────────────────────────────────────────────────────────────
def fetch_items(query: str) -> list[dict]:
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            tree = ET.parse(r)
    except Exception as e:
        print(f"  [skip] {query}: {e}")
        return []
    items = []
    for item in tree.findall(".//item")[:5]:
        title = item.findtext("title", "").strip()
        link  = item.findtext("link", "").strip()
        pub   = item.findtext("pubDate", "").strip()
        src_el = item.find("{https://news.google.com/rss}source")
        source = src_el.text if src_el is not None else "Google News"
        # clean title (remove source suffix " - Publisher")
        title = re.sub(r'\s+[-–]\s+[\w\s&\.]+$', '', title)
        items.append({"title": title, "link": link, "pub": pub, "source": source})
    return items

# ── De-duplicate by title ─────────────────────────────────────────────────────
def dedupe(all_items):
    seen, out = set(), []
    for item in all_items:
        key = item["title"][:60].lower()
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out[:MAX_ITEMS]

# ── Render HTML ───────────────────────────────────────────────────────────────
def news_card(item: dict, idx: int) -> str:
    t = html.escape(item["title"])
    s = html.escape(item["source"])
    p = item["pub"][:16] if item["pub"] else ""
    l = html.escape(item["link"])
    badge = "🔴 New" if idx < 3 else "📰"
    return f"""<article class="news-item">
  <span class="news-badge">{badge}</span>
  <a class="news-title" href="{l}" target="_blank" rel="noopener">{t}</a>
  <div class="news-meta">{s} · {p}</div>
</article>"""

def build_html(items: list[dict]) -> str:
    now = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    cards = "\n".join(news_card(it, i) for i, it in enumerate(items))
    count = len(items)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CBSE News &amp; Updates 2026-27 | Board Exam Notifications</title>
<meta name="description" content="Latest CBSE board exam news, official notifications, 2027 datesheet updates, syllabus announcements and education updates for Class 10 and Class 12 students.">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://cbsemock.org.in/news.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CBSE Board Exam Hub">
<meta property="og:title" content="CBSE News &amp; Updates 2026-27">
<meta property="og:description" content="Latest CBSE board exam news, official notifications, datesheet updates and education announcements.">
<meta property="og:url" content="https://cbsemock.org.in/news.html">
<meta property="og:image" content="https://cbsemock.org.in/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="CBSE News &amp; Updates 2026-27">
<meta name="twitter:description" content="Latest CBSE board exam news and official notifications.">
<meta name="twitter:image" content="https://cbsemock.org.in/og-image.jpg">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CollectionPage","name":"CBSE News & Updates","description":"Latest CBSE board exam news, official notifications, datesheet updates and education announcements.","url":"https://cbsemock.org.in/news.html","isPartOf":{{"@type":"WebSite","name":"CBSE Board Exam Hub","url":"https://cbsemock.org.in/"}}}}
</script>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G9HPDB24Y7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-G9HPDB24Y7');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2810600896966939" crossorigin="anonymous"></script>
<style>
:root{{
  --navy:#0d1b2a;--teal:#00b4d8;--gold:#c9a227;
  --bg:#f4f6f8;--card:#fff;--border:#dde3ea;
  --text:#1a202c;--muted:#64748b;
  font-family:'Segoe UI',system-ui,sans-serif;
}}
@media(prefers-color-scheme:dark){{
  :root{{--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--muted:#8b949e;}}
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);padding:0 16px 40px}}
.news-nav{{display:flex;flex-wrap:wrap;gap:9px;align-items:center;padding:12px 16px;margin:0 -16px 18px;background:#142b4f;border-bottom:2px solid var(--gold)}}
.news-nav a{{color:#fff;text-decoration:none;font-size:.84rem;font-weight:650;padding:7px 11px;border-radius:7px}}
.news-nav a:hover,.news-nav a[aria-current="page"]{{background:#c9a227;color:#142b4f}}
.news-header{{
  background:var(--navy);color:#fff;padding:18px 20px;
  border-radius:0 0 12px 12px;margin-bottom:24px;
  display:flex;align-items:center;gap:12px;
}}
.news-header h1{{font-size:1.1rem;flex:1}}
.news-updated{{font-size:.72rem;color:#94a3b8}}
.news-item{{
  background:var(--card);border:1px solid var(--border);
  border-radius:10px;padding:14px 16px;margin-bottom:12px;
  transition:box-shadow .2s;
}}
.news-item:hover{{box-shadow:0 4px 16px rgba(0,0,0,.1)}}
.news-badge{{font-size:.7rem;font-weight:700;margin-bottom:6px;display:block}}
.news-title{{
  color:var(--teal);font-size:.92rem;font-weight:600;
  line-height:1.45;text-decoration:none;display:block;margin-bottom:6px;
}}
.news-title:hover{{text-decoration:underline}}
.news-meta{{font-size:.75rem;color:var(--muted)}}
.news-footer{{text-align:center;font-size:.75rem;color:var(--muted);margin-top:20px}}
</style>
</head>
<body>
<nav class="news-nav" aria-label="Main navigation">
  <a href="/">⌂ Home</a>
  <a href="/news.html" aria-current="page">📰 News &amp; Updates</a>
  <a href="/mock-zone/">Mock Zone</a>
  <a href="/study-zone/">Study Zone</a>
  <a href="/virtual-labs/">Virtual Labs</a>
</nav>
<div class="news-header">
  <div>
    <h1>📰 CBSE News &amp; Updates</h1>
    <div class="news-updated">Auto-updated: {now} · {count} items</div>
  </div>
</div>
{cards}
<div class="news-footer">
  Powered by Google News RSS · cbsemock.org.in<br>
  <a href="/" style="color:var(--teal)">← Back to Portal</a>
</div>
<script src="portal-shell.js"></script>
</body>
</html>"""

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import urllib.parse
    print("Fetching CBSE news from Google News RSS...")
    all_items = []
    for q in QUERIES:
        print(f"  Query: {q}")
        all_items.extend(fetch_items(q))
    items = dedupe(all_items)
    print(f"  {len(items)} unique items after deduplication")
    html_content = build_html(items)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Written: {OUT_PATH} ({len(html_content):,} bytes)")
    print("Done. Commit news.html to trigger GitHub Pages update.")
