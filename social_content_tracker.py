#!/usr/bin/env python3
"""
social_content_tracker.py — Content Rotation Tracker for CBSE Mock Social Media
─────────────────────────────────────────────────────────────────────────────────
Manages a CSV tracker (social-posting-tracker.csv) with columns:
  content_type, title, url, telegram, facebook

Rules:
  - Never repeat a post until ALL items of that type are ticked
  - Once all ticked → reset that type's ticks and restart cycle
  - Picks the next un-ticked item in order

Content types tracked:
  1. quest        — Quest of the Day MCQ (daily)
  2. news         — CBSE news digest (daily)
  3. notes        — Subject notes pages (Class 9–12, one per day)
  4. practice_10  — Class 10 practice paper (one per day)
  5. practice_12  — Class 12 practice paper (one per day)
  6. lab          — Virtual lab highlight (daily, 221 labs, rotating)
  7. weekly_focus — Weekly focus topic (static for 7 days, then advances)

Usage (called by post_telegram.py and post_facebook.py):
  tracker = ContentTracker()
  item = tracker.get_next("notes")           # get next un-posted notes item
  tracker.mark_posted("notes", item, "telegram")  # mark as posted
  tracker.save()
"""

import csv
import os
import re
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT    = Path(__file__).parent
TRACKER_PATH = REPO_ROOT / "social-posting-tracker.csv"

PORTAL_BASE  = "https://cbsemock.org.in"

FIELDNAMES = ["content_type", "title", "url", "telegram", "facebook", "instagram"]

# ── Content catalogue ─────────────────────────────────────────────────────────
# Notes pages: class → list of (title, url)
NOTES_PAGES = [
    # Class 9
    ("Science Notes — Class 9",           f"{PORTAL_BASE}/resources/science-x.html"),
    ("Mathematics Notes — Class 9",       f"{PORTAL_BASE}/resources/maths-x.html"),
    ("Social Science Notes — Class 9",    f"{PORTAL_BASE}/resources/sst-x.html"),
    ("Hindi Course A Notes — Class 9",    f"{PORTAL_BASE}/resources/hindi-a-x.html"),
    ("English LL Notes — Class 9",        f"{PORTAL_BASE}/resources/english-ll-x.html"),
    ("AI Notes — Class 9/10",             f"{PORTAL_BASE}/resources/ai-x.html"),
    # Class 10
    ("Science Notes — Class 10",          f"{PORTAL_BASE}/resources/science-x.html"),
    ("Mathematics Standard Notes — Cl 10",f"{PORTAL_BASE}/resources/maths-x.html"),
    ("Mathematics Basic Notes — Class 10",f"{PORTAL_BASE}/resources/maths-basic-x.html"),
    ("Social Science Notes — Class 10",   f"{PORTAL_BASE}/resources/sst-x.html"),
    ("Hindi Course A Notes — Class 10",   f"{PORTAL_BASE}/resources/hindi-a-x.html"),
    ("English Communicative Notes — Cl10",f"{PORTAL_BASE}/resources/english-comm-x.html"),
    ("English LL Notes — Class 10",       f"{PORTAL_BASE}/resources/english-ll-x.html"),
    ("Computer Applications Notes — Cl10",f"{PORTAL_BASE}/resources/comp-app-x.html"),
    # Class 11 (linking study-zone)
    ("Physics Notes — Class 11",          f"{PORTAL_BASE}/study-zone/classes-11-12.html"),
    ("Chemistry Notes — Class 11",        f"{PORTAL_BASE}/study-zone/classes-11-12.html"),
    ("Mathematics Notes — Class 11",      f"{PORTAL_BASE}/study-zone/classes-11-12.html"),
    ("Biology Notes — Class 11",          f"{PORTAL_BASE}/study-zone/classes-11-12.html"),
    ("Accountancy Notes — Class 11",      f"{PORTAL_BASE}/study-zone/classes-11-12.html"),
    ("Economics Notes — Class 11",        f"{PORTAL_BASE}/study-zone/classes-11-12.html"),
    # Class 12
    ("Physics Notes — Class 12",          f"{PORTAL_BASE}/resources/physics-xii.html"),
    ("Chemistry Notes — Class 12",        f"{PORTAL_BASE}/resources/chemistry-xii.html"),
    ("Mathematics Notes — Class 12",      f"{PORTAL_BASE}/resources/maths-xii.html"),
    ("Biology Notes — Class 12",          f"{PORTAL_BASE}/resources/biology-xii.html"),
    ("Accountancy Notes — Class 12",      f"{PORTAL_BASE}/resources/accountancy-xii.html"),
    ("Economics Notes — Class 12",        f"{PORTAL_BASE}/resources/economics-xii.html"),
    ("Physics Notes — Class 12",          f"{PORTAL_BASE}/resources/physics-xii.html"),
    ("Computer Science Notes — Class 12", f"{PORTAL_BASE}/resources/cs-xii.html"),
    ("English Core Notes — Class 12",     f"{PORTAL_BASE}/resources/english-xii.html"),
    ("Business Studies Notes — Class 12", f"{PORTAL_BASE}/resources/business-xii.html"),
]

PRACTICE_10_PAGES = [
    ("Science Mock Test — Class 10",              f"{PORTAL_BASE}/Science%20Mock%20Tests%20_%20Class%2010%20CBSE.html"),
    ("Mathematics Standard Mock — Class 10",      f"{PORTAL_BASE}/Mathematics%20Standard%20Mock%20Tests%20_%20Class%2010%20CBSE.html"),
    ("Mathematics Basic Mock — Class 10",         f"{PORTAL_BASE}/Mathematics%20Basic%20Mock%20Tests%20_%20Class%2010%20CBSE.html"),
    ("Social Science Mock — Class 10",            f"{PORTAL_BASE}/Social%20Science%20Mock%20Tests%20_%20Class%2010%20CBSE.html"),
    ("English Communicative Mock — Class 10",     f"{PORTAL_BASE}/English%20Communicative%20Mock%20Tests%20_%20Class%2010%20CBSE.html"),
    ("English Language & Lit Mock — Class 10",    f"{PORTAL_BASE}/English%20Language%20%26%20Literature%20Mock%20Tests%20_%20Class%2010%20CBSE.html"),
    ("Hindi Course A Mock — Class 10",            f"{PORTAL_BASE}/Hindi%20Course%20A%20Class%2010%20CBSE.html"),
    ("Computer Applications Mock — Class 10",     f"{PORTAL_BASE}/Computer%20Applications%20Mock%20Tests%20_%20Class%2010%20CBSE.html"),
    ("AI Mock Papers — Class 10",                 f"{PORTAL_BASE}/CBSE%20Class%2010%20AI%20Mock%20Papers.html"),
]

def _discover_labs() -> list[tuple[str, str]]:
    """Auto-discover all virtual lab HTML files and return (title, url) list."""
    base    = REPO_ROOT / "virtual-labs"
    portal  = "https://cbsemock.org.in/virtual-labs"
    labs    = []
    if not base.exists():
        return labs
    for f in sorted(base.rglob("*.html")):
        if "index" in f.name or "ai-ml" in str(f):
            continue
        subject = f.parent.name.replace("-", " ").title()
        stem    = f.stem
        name    = re.sub(r"^\d+[-_]?", "", stem).replace("-", " ").replace("_", " ").title()
        title   = f"{name} — {subject} Lab"
        url     = f"{portal}/{f.relative_to(base)}"
        labs.append((title, url))
    return labs

LAB_PAGES = _discover_labs()

# Weekly focus topics — one per week, rotating
WEEKLY_FOCUS_TOPICS = [
    ("Mechanics & Motion",         "Newton's Laws, velocity, acceleration, projectile motion",           "https://cbsemock.org.in/resources/physics-xii.html"),
    ("Chemical Reactions",         "Types of reactions, balancing equations, redox, electrolysis",        "https://cbsemock.org.in/resources/chemistry-xii.html"),
    ("Cell Biology",               "Cell structure, division, osmosis, tissues",                          "https://cbsemock.org.in/resources/biology-xii.html"),
    ("Algebra & Calculus",         "Functions, differentiation, integration, matrices",                   "https://cbsemock.org.in/resources/maths-xii.html"),
    ("Electricity & Magnetism",    "Current, resistance, Ohm's law, electromagnetic induction",           "https://cbsemock.org.in/resources/physics-xii.html"),
    ("Organic Chemistry",          "Carbon compounds, hydrocarbons, functional groups, polymers",         "https://cbsemock.org.in/resources/chemistry-xii.html"),
    ("Genetics & Evolution",       "DNA, Mendel's laws, natural selection, biotechnology",                "https://cbsemock.org.in/resources/biology-xii.html"),
    ("Statistics & Probability",   "Mean, median, mode, probability, Bayes theorem",                     "https://cbsemock.org.in/resources/maths-xii.html"),
    ("Thermodynamics",             "Heat, entropy, laws of thermodynamics, specific heat",                "https://cbsemock.org.in/resources/physics-xii.html"),
    ("Electrochemistry",           "Galvanic cells, Nernst equation, electrolysis, corrosion",            "https://cbsemock.org.in/resources/chemistry-xii.html"),
    ("Human Physiology",           "Digestion, respiration, circulation, excretion, nervous system",      "https://cbsemock.org.in/resources/biology-xii.html"),
    ("Coordinate Geometry",        "Lines, circles, conic sections, 3D geometry, vectors",               "https://cbsemock.org.in/resources/maths-xii.html"),
    ("Optics & Waves",             "Reflection, refraction, lenses, wave optics, interference",           "https://cbsemock.org.in/resources/physics-xii.html"),
    ("Macroeconomics",             "GDP, inflation, fiscal policy, money supply, banking",                "https://cbsemock.org.in/resources/economics-xii.html"),
    ("Financial Accounting",       "Journal, ledger, trial balance, final accounts, ratios",              "https://cbsemock.org.in/resources/accountancy-xii.html"),
    ("Data Structures & Algorithms","Arrays, stacks, queues, sorting, searching, complexity",             "https://cbsemock.org.in/resources/cs-xii.html"),
    ("Social Science — History",   "Nationalism, colonial era, world wars, independence movement",        "https://cbsemock.org.in/resources/sst-x.html"),
    ("Environmental Science",      "Ecosystems, biodiversity, pollution, climate change, conservation",   "https://cbsemock.org.in/resources/biology-xii.html"),
    ("Business Studies",           "Management, marketing, finance, entrepreneurship, HRM",               "https://cbsemock.org.in/resources/business-xii.html"),
    ("AI & Machine Learning",      "Data types, supervised learning, neural networks, ethics",            "https://cbsemock.org.in/resources/ai-x.html"),
]

PRACTICE_12_PAGES = [
    ("Physics Board Prep — Class 12",             f"{PORTAL_BASE}/Physics%20XII%20Board%20Prep.html"),
    ("Chemistry Board Prep — Class 12",           f"{PORTAL_BASE}/Chemistry%20XII%20Board%20Prep.html"),
    ("Mathematics Board Prep — Class 12",         f"{PORTAL_BASE}/Mathematics%20XII%20Board%20Prep.html"),
    ("Biology Board Prep — Class 12",             f"{PORTAL_BASE}/Biology%20XII%20Board%20Prep.html"),
    ("English Core Practice — Class 12",          f"{PORTAL_BASE}/English%20Core%20XII.html"),
    ("English Elective Practice — Class 12",      f"{PORTAL_BASE}/English%20Elective%20001%20Class%2012%20Practice%20Papers.html"),
    ("Computer Science Mock — Class 12",          f"{PORTAL_BASE}/CBSE%20Class%20XII%20CS%20Mock%20Papers.html"),
    ("Informatics Practices Mock — Class 12",     f"{PORTAL_BASE}/Informatics%20Practices%20065%20Class%2012%20Practice%20Papers.html"),
    ("Physical Education Mock — Class 12",        f"{PORTAL_BASE}/Physical%20Education%20048%20Class%2012%20Practice%20Papers.html"),
    ("Bengali Practice — Class 12",              f"{PORTAL_BASE}/Bengali%20Class%2012%20Practice%20Papers.html"),
]


# ── Tracker ───────────────────────────────────────────────────────────────────
class ContentTracker:
    def __init__(self):
        self.rows = []
        self._load_or_init()

    def _load_or_init(self):
        if TRACKER_PATH.exists():
            with open(TRACKER_PATH, encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                self.rows = list(reader)
            # Backfill any missing columns (e.g. instagram added later)
            for row in self.rows:
                for col in FIELDNAMES:
                    if col not in row:
                        row[col] = ""
            # Add any new items that aren't tracked yet
            self._sync_catalogue()
        else:
            self._init_fresh()

    def _init_fresh(self):
        """Create tracker from scratch with all content items."""
        self.rows = []
        for title, url in NOTES_PAGES:
            self.rows.append({"content_type": "notes", "title": title,
                               "url": url, "telegram": "", "facebook": "", "instagram": ""})
        for title, url in PRACTICE_10_PAGES:
            self.rows.append({"content_type": "practice_10", "title": title,
                               "url": url, "telegram": "", "facebook": "", "instagram": ""})
        for title, url in PRACTICE_12_PAGES:
            self.rows.append({"content_type": "practice_12", "title": title,
                               "url": url, "telegram": "", "facebook": "", "instagram": ""})
        for title, url in LAB_PAGES:
            self.rows.append({"content_type": "lab", "title": title,
                               "url": url, "telegram": "", "facebook": "", "instagram": ""})
        for topic, desc, url in WEEKLY_FOCUS_TOPICS:
            self.rows.append({"content_type": "weekly_focus", "title": topic,
                               "url": url, "telegram": "", "facebook": "", "instagram": ""})
        self.save()
        print(f"[OK] Tracker initialised: {TRACKER_PATH.name}")
        print(f"     {len([r for r in self.rows if r['content_type']=='notes'])} notes")
        print(f"     {len([r for r in self.rows if r['content_type']=='practice_10'])} Class 10 papers")
        print(f"     {len([r for r in self.rows if r['content_type']=='practice_12'])} Class 12 papers")
        print(f"     {len([r for r in self.rows if r['content_type']=='lab'])} virtual labs")
        print(f"     {len([r for r in self.rows if r['content_type']=='weekly_focus'])} weekly focus topics")

    def _sync_catalogue(self):
        """Add new catalogue items that don't exist in the CSV yet."""
        existing = {(r["content_type"], r["title"]) for r in self.rows}
        added = 0
        for title, url in NOTES_PAGES:
            if ("notes", title) not in existing:
                self.rows.append({"content_type": "notes", "title": title,
                                   "url": url, "telegram": "", "facebook": "", "instagram": ""})
                added += 1
        for title, url in PRACTICE_10_PAGES:
            if ("practice_10", title) not in existing:
                self.rows.append({"content_type": "practice_10", "title": title,
                                   "url": url, "telegram": "", "facebook": "", "instagram": ""})
                added += 1
        for title, url in PRACTICE_12_PAGES:
            if ("practice_12", title) not in existing:
                self.rows.append({"content_type": "practice_12", "title": title,
                                   "url": url, "telegram": "", "facebook": "", "instagram": ""})
                added += 1
        for title, url in LAB_PAGES:
            if ("lab", title) not in existing:
                self.rows.append({"content_type": "lab", "title": title,
                                   "url": url, "telegram": "", "facebook": "", "instagram": ""})
                added += 1
        for topic, desc, url in WEEKLY_FOCUS_TOPICS:
            if ("weekly_focus", topic) not in existing:
                self.rows.append({"content_type": "weekly_focus", "title": topic,
                                   "url": url, "telegram": "", "facebook": "", "instagram": ""})
                added += 1
        if added:
            print(f"[SYNC] Added {added} new items to tracker.")
            self.save()

    def _rows_of_type(self, content_type: str) -> list[dict]:
        return [r for r in self.rows if r["content_type"] == content_type]

    def get_next(self, content_type: str, platform: str = "telegram") -> dict | None:
        """
        Return the next un-posted item for this content_type on this platform.
        If all are posted, reset all ticks for that type and return first item.
        """
        rows = self._rows_of_type(content_type)
        if not rows:
            return None

        # Find first un-ticked row
        for row in rows:
            if not row.get(platform, "").strip():
                return row

        # All ticked — reset and start over
        print(f"[RESET] All {content_type} items posted on {platform}. Starting new cycle.")
        for row in self.rows:
            if row["content_type"] == content_type:
                row[platform] = ""
        return rows[0]

    def get_weekly_focus(self, platform: str = "telegram") -> dict | None:
        """
        Return current week's focus topic. Same item for 7 days.
        Advances to the next un-ticked item on week boundary.
        A tick is set once per week (not daily) — marked on Monday.
        """
        rows = self._rows_of_type("weekly_focus")
        if not rows:
            return None

        # Find the current in-progress item (ticked within last 7 days)
        today = datetime.now(timezone.utc)
        for row in rows:
            tick = row.get(platform, "").strip()
            if tick.startswith("✓"):
                try:
                    tick_date = datetime.strptime(tick[2:], "%Y-%m-%d").replace(tzinfo=timezone.utc)
                    days_ago  = (today - tick_date).days
                    if days_ago < 7:
                        return row   # still within the week
                except ValueError:
                    pass

        # No active item — find next un-ticked
        for row in rows:
            if not row.get(platform, "").strip():
                return row

        # All done — reset
        print(f"[RESET] All weekly_focus topics done on {platform}. Restarting.")
        for row in self.rows:
            if row["content_type"] == "weekly_focus":
                row[platform] = ""
        return rows[0]

    def mark_posted(self, content_type: str, item: dict, platform: str):
        """Mark an item as posted on a platform with a timestamp tick."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        for row in self.rows:
            if (row["content_type"] == content_type and
                    row["title"] == item["title"]):
                row[platform] = f"✓ {now}"
                break

    def save(self):
        with open(TRACKER_PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(self.rows)

    def stats(self):
        """Print posting stats."""
        for ctype in ("notes", "practice_10", "practice_12", "lab", "weekly_focus"):
            rows = self._rows_of_type(ctype)
            tg_done = sum(1 for r in rows if r.get("telegram", "").strip())
            fb_done = sum(1 for r in rows if r.get("facebook", "").strip())
            print(f"  {ctype:14s}: {tg_done}/{len(rows)} Telegram  {fb_done}/{len(rows)} Facebook")


if __name__ == "__main__":
    # Initialise or show stats
    tracker = ContentTracker()
    print("\nCurrent posting stats:")
    tracker.stats()
    next_notes = tracker.get_next("notes")
    next_p10   = tracker.get_next("practice_10")
    next_p12   = tracker.get_next("practice_12")
    print(f"\nNext notes     : {next_notes['title'] if next_notes else 'None'}")
    print(f"Next practice 10: {next_p10['title'] if next_p10 else 'None'}")
    print(f"Next practice 12: {next_p12['title'] if next_p12 else 'None'}")
