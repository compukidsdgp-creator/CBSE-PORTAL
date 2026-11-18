"""Structure gate for virtual labs against the locked standard (virtual-labs/LAB_STANDARD.md).
    python3 lab_check.py virtual-labs/physics/_drafts/01-ohm-s-law.html [--live]
Exit 1 on problems. --live also requires the page to be publishable (no noindex/draft bar).
Behaviour (console errors, mobile overflow, full run-through) is checked separately with Playwright.
"""
import re
import sys
from pathlib import Path

ALLOWED_SCRIPT_HOSTS = ("cdnjs.cloudflare.com", "cdn.jsdelivr.net/npm/", "unpkg.com", "www.googletagmanager.com")


def check(path, live=False):
    s = Path(path).read_text(encoding="utf-8")
    p = []

    def need(cond, msg):
        if not cond:
            p.append(msg)
    need(s.lstrip().lower().startswith("<!doctype html>"), "must start with <!DOCTYPE html>")
    need('<html lang="en"' in s, 'missing <html lang="en">')
    need('name="viewport"' in s, "missing viewport meta")
    need(re.search(r"<title>[^<]+— Virtual Lab \| CBSEMock</title>", s), "title must end with '— Virtual Lab | CBSEMock'")
    m = re.search(r'<meta name="description" content="([^"]+)"', s)
    need(m and 110 <= len(m.group(1)) <= 170, "meta description missing or not 110–170 characters")
    need('rel="canonical"' in s, "missing canonical link")
    need('name="cbse-lab-standard" content="2026-11"' in s, "missing <meta name=\"cbse-lab-standard\" content=\"2026-11\">")
    need('"LearningResource"' in s and '"Simulation"' in s, "missing LearningResource JSON-LD with Simulation type")
    need("G-G9HPDB24Y7" in s, "missing GA tag")
    need('rel="icon"' in s, "missing favicon block")
    # header B
    need('class="hero hv hv-b"' in s, "header must be design B: <header class=\"hero hv hv-b\">")
    need('class="sceneB"' in s, "header needs the inline SVG apparatus scene (svg.sceneB)")
    need('class="g1"' in s and 'class="g2"' in s, "H1 needs .g1 (gold line) and .g2 (white line)")
    need('class="hsteps"' in s and s.count("<li><b>") >= 4, "missing the 4-step strip (.hsteps)")
    need('href="#lab"' in s, "missing call-to-action button to #lab")
    need("prefers-reduced-motion" in s, "must respect prefers-reduced-motion")
    # environment + record
    need('<section class="lab" id="lab"' in s, 'missing <section class="lab" id="lab">')
    need('class="tab' in s and 'id="task"' in s, "missing step tabs and the task line (#task)")
    need(re.search(r"Show readings \(helper\)|helper", s), "missing the 'Show readings (helper)' switch")
    need("localStorage" in s and "try{" in s.replace(" ", ""), "progress must be saved with try/catch-wrapped localStorage")
    need(re.search(r"Observation table|Output table|Observation", s), "missing observation/record table")
    need(re.search(r"Check my", s), "missing 'Check my …' validation button")
    need(re.search(r">Result<", s), "missing Result section")
    for sec in ("Aim", "Apparatus|Materials|Requirements", "Theory", "Procedure", "Precautions|Limitations", "Sources of error|Limitations"):
        need(re.search(rf">\s*({sec})", s), f"missing teaching section: {sec}")
    need(re.search(r"Viva", s), "missing Viva voce section")
    viva = len(re.findall(r"\['[^']{8,}','[^']{8,}'\]", s)) + s.count('<details class="q">')
    need(viva >= 8, f"viva needs at least 8 questions (found {viva})")
    need('id="record"' in s and "@media print" in s and "Teacher" in s, "missing printable practical record (#record + print CSS + teacher signature)")
    need("Keep going" in s, "missing 'Keep going' links")
    for src in re.findall(r'<script[^>]+src="([^"]+)"', s):
        need(any(h in src for h in ALLOWED_SCRIPT_HOSTS), f"script from a host that is not allowed: {src}")
        if "googletagmanager" not in src:
            need(re.search(r"@\d+\.\d+(\.\d+)?|/\d+\.\d+\.\d+/", src), f"script version must be pinned: {src}")
    need(not re.search(r'<img[^>]+src="https?://', s), "no remote images: draw with inline SVG")
    if live:
        need("noindex" not in s, "live page must not be noindex")
        need('class="lab-draft"' not in s, "live page must not carry the draft bar")
    else:
        need("noindex" in s and 'class="lab-draft"' in s, "a draft must carry noindex and the draft bar (div.lab-draft)")
    return p


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    live = "--live" in sys.argv
    bad = 0
    for f in args:
        probs = check(f, live)
        for x in probs:
            print(f"✗ {f}: {x}")
        bad += len(probs)
        print(f"[lab_check] {f}: {len(probs)} problem(s)")
    sys.exit(1 if bad else 0)
