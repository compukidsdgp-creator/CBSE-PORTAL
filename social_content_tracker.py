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

Usage (called by post_telegram.py and post_facebook.py):
  tracker = ContentTracker()
  item = tracker.get_next("notes")           # get next un-posted notes item
  tracker.mark_posted("notes", item, "telegram")  # mark as posted
  tracker.save()
"""

import csv
import os
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT    = Path(__file__).parent
TRACKER_PATH = REPO_ROOT / "social-posting-tracker.csv"

PORTAL_BASE  = "https://cbsemock.org.in"

FIELDNAMES = ["content_type", "title", "url", "telegram", "facebook"]

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
    ("Science Mock Test — Class 10",              f"{PORTAL_BASE}/Science Mock Tests _ Class 10 CBSE.html"),
    ("Mathematics Standard Mock — Class 10",      f"{PORTAL_BASE}/Mathematics Standard Mock Tests _ Class 10 CBSE.html"),
    ("Mathematics Basic Mock — Class 10",         f"{PORTAL_BASE}/Mathematics Basic Mock Tests _ Class 10 CBSE.html"),
    ("Social Science Mock — Class 10",            f"{PORTAL_BASE}/Social Science Mock Tests _ Class 10 CBSE.html"),
    ("English Communicative Mock — Class 10",     f"{PORTAL_BASE}/English Communicative Mock Tests _ Class 10 CBSE.html"),
    ("English Language & Lit Mock — Class 10",    f"{PORTAL_BASE}/English Language & Literature Mock Tests _ Class 10 CBSE.html"),
    ("Hindi Course A Mock — Class 10",            f"{PORTAL_BASE}/Hindi Course A Class 10 CBSE.html"),
    ("Computer Applications Mock — Class 10",     f"{PORTAL_BASE}/Computer Applications Mock Tests _ Class 10 CBSE.html"),
    ("AI Mock Papers — Class 10",                 f"{PORTAL_BASE}/CBSE Class 10 AI Mock Papers.html"),
]

PRACTICE_12_PAGES = [
    ("Physics Board Prep — Class 12",             f"{PORTAL_BASE}/Physics XII Board Prep.html"),
    ("Chemistry Board Prep — Class 12",           f"{PORTAL_BASE}/Chemistry XII Board Prep.html"),
    ("Mathematics Board Prep — Class 12",         f"{PORTAL_BASE}/Mathematics XII Board Prep.html"),
    ("Biology Board Prep — Class 12",             f"{PORTAL_BASE}/Biology XII Board Prep.html"),
    ("English Core Practice — Class 12",          f"{PORTAL_BASE}/English Core XII.html"),
    ("English Elective Practice — Class 12",      f"{PORTAL_BASE}/English Elective 001 Class 12 Practice Papers.html"),
    ("Computer Science Mock — Class 12",          f"{PORTAL_BASE}/CBSE Class XII CS Mock Papers.html"),
    ("Informatics Practices Mock — Class 12",     f"{PORTAL_BASE}/Informatics Practices 065 Class 12 Practice Papers.html"),
    ("Physical Education Mock — Class 12",        f"{PORTAL_BASE}/Physical Education 048 Class 12 Practice Papers.html"),
    ("Bengali Practice — Class 12",              f"{PORTAL_BASE}/Bengali Class 12 Practice Papers.html"),
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
            # Add any new items that aren't tracked yet
            self._sync_catalogue()
        else:
            self._init_fresh()

    def _init_fresh(self):
        """Create tracker from scratch with all content items."""
        self.rows = []
        for title, url in NOTES_PAGES:
            self.rows.append({"content_type": "notes", "title": title,
                               "url": url, "telegram": "", "facebook": ""})
        for title, url in PRACTICE_10_PAGES:
            self.rows.append({"content_type": "practice_10", "title": title,
                               "url": url, "telegram": "", "facebook": ""})
        for title, url in PRACTICE_12_PAGES:
            self.rows.append({"content_type": "practice_12", "title": title,
                               "url": url, "telegram": "", "facebook": ""})
        self.save()
        print(f"[OK] Tracker initialised: {TRACKER_PATH.name}")
        print(f"     {len([r for r in self.rows if r['content_type']=='notes'])} notes")
        print(f"     {len([r for r in self.rows if r['content_type']=='practice_10'])} Class 10 papers")
        print(f"     {len([r for r in self.rows if r['content_type']=='practice_12'])} Class 12 papers")

    def _sync_catalogue(self):
        """Add new catalogue items that don't exist in the CSV yet."""
        existing = {(r["content_type"], r["title"]) for r in self.rows}
        added = 0
        for title, url in NOTES_PAGES:
            if ("notes", title) not in existing:
                self.rows.append({"content_type": "notes", "title": title,
                                   "url": url, "telegram": "", "facebook": ""})
                added += 1
        for title, url in PRACTICE_10_PAGES:
            if ("practice_10", title) not in existing:
                self.rows.append({"content_type": "practice_10", "title": title,
                                   "url": url, "telegram": "", "facebook": ""})
                added += 1
        for title, url in PRACTICE_12_PAGES:
            if ("practice_12", title) not in existing:
                self.rows.append({"content_type": "practice_12", "title": title,
                                   "url": url, "telegram": "", "facebook": ""})
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
        for ctype in ("notes", "practice_10", "practice_12"):
            rows = self._rows_of_type(ctype)
            tg_done = sum(1 for r in rows if r.get("telegram", "").strip())
            fb_done = sum(1 for r in rows if r.get("facebook", "").strip())
            print(f"  {ctype:12s}: {tg_done}/{len(rows)} Telegram  {fb_done}/{len(rows)} Facebook")


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
