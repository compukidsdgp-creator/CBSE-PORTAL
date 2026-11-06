#!/usr/bin/env python3
"""Refresh Weekly Focus SEO metadata from weekly-focus.json before sitemap generation."""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "weekly-focus" / "weekly-focus.json").read_text(encoding="utf-8"))
PAGE = ROOT / "weekly-focus" / "weekly-focus-prod.html"
source = PAGE.read_text(encoding="utf-8")

meta = DATA.get("meta", {})
hero = DATA.get("hero", {})
lesson = hero.get("title", "Weekly CBSE learning and revision")
subject = meta.get("subject", "CBSE")
level = meta.get("class", "Classes 10 and 12")
title = f"Weekly Focus: {lesson} | {level} {subject} | CBSEMock"
description = (
    f"Study {lesson} in this interactive CBSE {level} {subject} Weekly Focus lesson. "
    "Explore clear explanations, key revision points, board-style questions and an interactive quiz."
)
url = "https://cbsemock.org.in/weekly-focus/weekly-focus-prod.html"

def replace(pattern, replacement, text):
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.I | re.S)
    if count == 0:
        raise RuntimeError(f"Could not update expected SEO element: {pattern}")
    return updated

source = replace(r"<title>.*?</title>", f"<title>{escape(title)}</title>", source)
source = replace(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{escape(description, quote=True)}">', source)
source = replace(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{escape(title, quote=True)}">', source)
source = replace(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{escape(description, quote=True)}">', source)
source = replace(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{escape(title, quote=True)}">', source)
source = replace(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{escape(description, quote=True)}">', source)

# Keep the no-JavaScript summary aligned with the current lesson.
fallback = (
    '<noscript><main class="seo-fallback">'
    f'<h1>CBSE Weekly Focus: {escape(lesson)}</h1>'
    f'<p>{escape(hero.get("hook", ""))}</p>'
    f"<p>This week's focus is {escape(level)} {escape(subject)}, {escape(meta.get('chapter', ''))}. "
    'The lesson includes concept explanations, exam-focused revision points, board-style questions and an interactive quiz.</p>'
    '</main></noscript>'
)
source = re.sub(r'<noscript><main class="seo-fallback">.*?</main></noscript>', fallback, source, count=1, flags=re.S)
# Keep structured data synchronized with the current weekly lesson as well.
def sync_jsonld(match):
    payload = json.loads(match.group(1))
    graph = payload.get("@graph", [])
    for node in graph:
        if node.get("@type") == "WebPage":
            node["name"] = title
            node["description"] = description
        elif node.get("@type") == "LearningResource":
            node["description"] = description
    return '<script type="application/ld+json">\n' + json.dumps(payload, ensure_ascii=False, indent=2) + '\n</script>'

source, count = re.subn(
    r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
    sync_jsonld,
    source,
    count=1,
    flags=re.S
)
if count != 1:
    raise RuntimeError("Could not update Weekly Focus structured data")

PAGE.write_text(source, encoding="utf-8")
print(f"Updated Weekly Focus SEO: {title}")
