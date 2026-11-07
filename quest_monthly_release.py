#!/usr/bin/env python3
"""
quest_monthly_release.py — Automated monthly Quest data publisher
──────────────────────────────────────────────────────────────────
Runs on the 1st of each month (via GitHub Actions cron) to:
  1. Find the current month's folder in quest-bank/future-releases/
  2. Copy its questions/ files into quest/data/questions/
  3. Replace quest/data/catalogue-entry.json with the month's catalogue
  4. Commit and push

GitHub Actions setup (add to .github/workflows/quest-release.yml):
──────────────────────────────────────────────────────────────────
  name: Monthly Quest Release
  on:
    schedule:
      - cron: '0 1 1 * *'   # 1st of every month at 01:00 UTC (6:30 AM IST)
    workflow_dispatch:       # allow manual trigger from GitHub UI
  jobs:
    release:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Run release script
          run: python3 quest_monthly_release.py
        - name: Commit and push
          run: |
            git config user.name  "quest-release-bot"
            git config user.email "bot@cbsemock.org.in"
            git add quest/data/
            git diff --cached --quiet || git commit -m "chore: quest release $(date +%B\\ %Y)"
            git push

Usage locally (dry-run preview):
  python3 quest_monthly_release.py --dry-run

Force a specific month (for testing):
  python3 quest_monthly_release.py --month 2027-01
"""

import os
import sys
import json
import shutil
import argparse
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
REPO_ROOT   = Path(__file__).parent
FUTURE_DIR  = REPO_ROOT / "quest-bank" / "future-releases"
LIVE_DIR    = REPO_ROOT / "quest" / "data"
LIVE_Q_DIR  = LIVE_DIR / "questions"

# ── Month → folder name mapping ────────────────────────────────────────────────
MONTH_FOLDERS = {
    1:  "january",
    2:  "february",
    3:  "march",
    4:  "april",
    5:  "may",
    6:  "june",
    7:  "july",
    8:  "august",
    9:  "september",
    10: "october",
    11: "november",
    12: "december",
}


def find_release_folder(year: int, month: int) -> Path | None:
    """Return the future-release folder for the given year/month, or None."""
    folder_name = f"{year:04d}-{month:02d}-{MONTH_FOLDERS[month]}"
    path = FUTURE_DIR / folder_name
    return path if path.is_dir() else None


def load_catalogue(folder: Path) -> dict:
    catalogue_path = folder / "catalogue-entry.json"
    if not catalogue_path.exists():
        raise FileNotFoundError(f"catalogue-entry.json not found in {folder}")
    with open(catalogue_path, encoding="utf-8") as f:
        return json.load(f)


def run_release(year: int, month: int, dry_run: bool = False) -> bool:
    month_name = MONTH_FOLDERS[month].capitalize()
    print(f"\n── Quest Monthly Release ──────────────────────────")
    print(f"   Target  : {month_name} {year}")
    print(f"   Dry run : {dry_run}")

    release_folder = find_release_folder(year, month)
    if release_folder is None:
        print(f"\n[SKIP] No future-release folder found for {year}-{month:02d}.")
        print(f"       Expected: {FUTURE_DIR / (str(year)+'-'+f'{month:02d}-'+MONTH_FOLDERS[month])}")
        return False

    print(f"\n[OK] Release folder: {release_folder.name}")

    catalogue = load_catalogue(release_folder)
    print(f"[OK] Catalogue loaded: {catalogue.get('release')} — {len(catalogue.get('quests', []))} quests")

    src_q_dir = release_folder / "questions"
    if not src_q_dir.is_dir():
        print(f"[ERROR] questions/ subfolder not found in {release_folder}")
        return False

    question_files = sorted(src_q_dir.iterdir())
    print(f"[OK] Question files : {len(question_files)} files in questions/")

    if dry_run:
        print("\n── Dry-run summary (no files written) ──────────────")
        print(f"   Would copy {len(question_files)} question files → quest/data/questions/")
        print(f"   Would replace quest/data/catalogue-entry.json")
        print(f"   Quests in catalogue:")
        for q in catalogue.get("quests", []):
            print(f"     [{q['class_group']}] {q['subject']}")
        return True

    # ── Copy question files ──────────────────────────────────────────────────
    LIVE_Q_DIR.mkdir(parents=True, exist_ok=True)
    copied = 0
    for src_file in question_files:
        dest_file = LIVE_Q_DIR / src_file.name
        shutil.copy2(src_file, dest_file)
        copied += 1
    print(f"[OK] Copied {copied} files → quest/data/questions/")

    # ── Write catalogue-entry.json ───────────────────────────────────────────
    catalogue["published_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    catalogue["status"] = "published"

    catalogue_dest = LIVE_DIR / "catalogue-entry.json"
    with open(catalogue_dest, "w", encoding="utf-8") as f:
        json.dump(catalogue, f, indent=2, ensure_ascii=False)
    print(f"[OK] catalogue-entry.json updated → {month_name} {year}")

    print(f"\n── Release complete ──────────────────────────────────")
    print(f"   {copied} question files published")
    print(f"   {len(catalogue.get('quests', []))} quests now live")
    print(f"   Commit and push handled by GitHub Actions (or run git manually)\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="CBSE Quest monthly release publisher")
    parser.add_argument("--dry-run",  action="store_true", help="Preview only, do not write files")
    parser.add_argument("--month",    type=str, default=None,
                        help="Force a specific month: YYYY-MM (e.g. 2027-01)")
    args = parser.parse_args()

    if args.month:
        try:
            year, month = [int(x) for x in args.month.split("-")]
        except ValueError:
            print(f"[ERROR] --month must be YYYY-MM, got: {args.month}")
            sys.exit(1)
    else:
        now = datetime.now(timezone.utc)
        year, month = now.year, now.month

    success = run_release(year, month, dry_run=args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
