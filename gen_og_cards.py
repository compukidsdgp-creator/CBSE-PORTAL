#!/usr/bin/env python3
"""
gen_og_cards.py — Injects/updates Open Graph + Twitter meta tags
into every resource HTML file so each subject page gets a unique
shareable preview card when shared on WhatsApp, Twitter, etc.

Run once after building new portals:
  python3 gen_og_cards.py

No external dependencies — pure stdlib.
"""

import os
import re

DOMAIN = "https://cbsemock.org.in"
BASE_DIR = os.path.dirname(__file__)
RES_DIR  = os.path.join(BASE_DIR, "resources")

# Subject-specific meta — file stem → (title, description, theme_color)
META = {
    "maths-x":       ("Maths X Practice Papers | CBSEMock",
                       "Class 10 Mathematics — Algebra, Geometry, Trigonometry, Statistics. 5 unit practice papers with solutions.",
                       "#0d4f8b"),
    "maths-basic-x": ("Maths Basic X Practice Papers | CBSEMock",
                       "Class 10 Maths Basic — Arithmetic, Mensuration, Data Handling. Simplified practice papers.",
                       "#0d4f8b"),
    "science-x":     ("Science X Practice Papers | CBSEMock",
                       "Class 10 Science — Physics, Chemistry, Biology. 13 chapters, CBSE pattern.",
                       "#2d6a4f"),
    "sst-x":         ("Social Science X Practice Papers | CBSEMock",
                       "Class 10 Social Science — History, Geography, Civics, Economics. CBSE board pattern.",
                       "#c9a227"),
    "english-ll-x":  ("English Lang & Lit X | CBSEMock",
                       "Class 10 English Language & Literature — First Flight, Footprints. CBSE practice papers.",
                       "#6b21a8"),
    "english-comm-x":("English Communicative X | CBSEMock",
                       "Class 10 English Communicative — Writing, Grammar, Comprehension. CBSE practice.",
                       "#6b21a8"),
    "hindi-a-x":     ("Hindi Course A X | CBSEMock",
                       "Class 10 Hindi Course A — Kshitij, Kritika, Sparsh. CBSE practice papers.",
                       "#c0392b"),
    "comp-app-x":    ("Computer Applications X | CBSEMock",
                       "Class 10 Computer Applications — HTML, CSS, Python basics. CBSE practice.",
                       "#00b4d8"),
    "ai-x":          ("AI Class X Practice Papers | CBSEMock",
                       "Class 10 Artificial Intelligence (Code 417) — Project Cycle, ML basics, Data. CBSE pattern.",
                       "#d97706"),
    "maths-xii":     ("Maths XII Practice Papers | CBSEMock",
                       "Class 12 Mathematics — Calculus, Matrices, Vectors, 3D Geometry, Probability. 5 unit papers.",
                       "#0d4f8b"),
    "physics-xii":   ("Physics XII Practice Papers | CBSEMock",
                       "Class 12 Physics — Electrostatics, Optics, Modern Physics. CBSE board practice.",
                       "#1a4a7c"),
    "chemistry-xii": ("Chemistry XII Practice Papers | CBSEMock",
                       "Class 12 Chemistry — Organic, Inorganic, Physical. CBSE board practice.",
                       "#5c1a5c"),
    "biology-xii":   ("Biology XII Practice Papers | CBSEMock",
                       "Class 12 Biology — Genetics, Evolution, Biotechnology, Ecology. CBSE practice.",
                       "#145214"),
    "english-xii":   ("English Core XII Practice Papers | CBSEMock",
                       "Class 12 English Core — Flamingo, Vistas, Writing. CBSE board practice.",
                       "#6b21a8"),
    "cs-xii":        ("Computer Science XII Practice Papers | CBSEMock",
                       "Class 12 Computer Science — Python OOP, SQL, Networking. CBSE board practice.",
                       "#1a4a7c"),
    "economics-xii": ("Economics XII Practice Papers | CBSEMock",
                       "Class 12 Economics — Micro & Macro, GDP, Money & Banking. CBSE board practice.",
                       "#7c5a0d"),
    "accountancy-xii":("Accountancy XII Practice Papers | CBSEMock",
                        "Class 12 Accountancy — Partnership, Company Accounts, Cash Flow. CBSE practice.",
                        "#7c1a1a"),
    "business-xii":  ("Business Studies XII Practice Papers | CBSEMock",
                       "Class 12 Business Studies — Management, Marketing, Consumer Protection. CBSE practice.",
                       "#2d5a1a"),
}

OG_TEMPLATE = """  <meta property="og:type"        content="website">
  <meta property="og:site_name"   content="CBSEMock.org.in">
  <meta property="og:url"         content="{url}">
  <meta property="og:title"       content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image"       content="https://cbsemock.org.in/og-image.jpg">
  <meta name="twitter:card"       content="summary_large_image">
  <meta name="twitter:title"      content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image"      content="https://cbsemock.org.in/og-image.jpg">
  <meta name="theme-color"        content="{color}">"""

def inject(path, stem):
    if stem not in META:
        print(f"  [skip] no meta for {stem}")
        return
    title, desc, color = META[stem]
    url = f"{DOMAIN}/resources/{stem}.html"
    og_block = OG_TEMPLATE.format(url=url, title=title, desc=desc, color=color)

    with open(path, encoding="utf-8") as f:
        html = f.read()

    # Remove existing OG/twitter/theme-color tags
    html = re.sub(r'\s*<meta\s+(property|name)="(og:|twitter:|theme-color)[^"]*"[^>]*>', '', html)

    # Inject after <head> or after charset meta
    if '<meta charset' in html:
        html = re.sub(r'(<meta charset[^>]+>)', r'\1\n' + og_block, html, count=1)
    elif '<head>' in html:
        html = html.replace('<head>', '<head>\n' + og_block, 1)
    else:
        print(f"  [warn] no <head> found in {stem}")
        return

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {stem}.html")

if __name__ == "__main__":
    print("Injecting OG meta tags into resource files...")
    for fname in sorted(os.listdir(RES_DIR)):
        if not fname.endswith(".html"):
            continue
        stem = fname[:-5]
        inject(os.path.join(RES_DIR, fname), stem)
    print("Done.")
