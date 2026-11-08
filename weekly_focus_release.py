#!/usr/bin/env python3
"""
weekly_focus_release.py
-----------------------
Run every Monday via GitHub Actions cron.
Reads the current ISO week number, looks up the corresponding
weekly-focus/data/week_NN.json, copies it to
weekly-focus/weekly-focus.json, then commits and pushes.

Week rotation:
  - Weeks 1–19   → Jan–May 2027 (W01–W19)
  - Weeks 46–52  → Nov–Dec 2026 (W46–W52)
  - Any other ISO week uses modulo over the 26-file pool.
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.resolve()
DATA_DIR = REPO_ROOT / "weekly-focus" / "data"
LIVE_FILE = REPO_ROOT / "weekly-focus" / "weekly-focus.json"

# ── All available week numbers (sorted) ───────────────────────────────────────
AVAILABLE_WEEKS = sorted(
    int(p.stem.split("_")[1])
    for p in DATA_DIR.glob("week_*.json")
)

if not AVAILABLE_WEEKS:
    print("[ERROR] No week JSON files found in", DATA_DIR)
    sys.exit(1)


def get_target_week() -> int:
    """
    Return the week file number to publish today.

    Strategy: use the current ISO week number.  If that exact week
    file exists, use it.  Otherwise, pick from the pool using a
    circular index so the rotation never breaks.
    """
    iso_week = date.today().isocalendar()[1]   # 1–53

    if iso_week in AVAILABLE_WEEKS:
        return iso_week

    # Fallback: circular index over sorted available weeks
    idx = (iso_week - 1) % len(AVAILABLE_WEEKS)
    return AVAILABLE_WEEKS[idx]


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict, path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Written: {path}")


def git_commit_push(week_num: int) -> None:
    """Stage, commit and push the updated weekly-focus.json."""
    rel_live = str(LIVE_FILE.relative_to(REPO_ROOT))
    cmds = [
        ["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"],
        ["git", "config", "user.name",  "github-actions[bot]"],
        ["git", "add",    rel_live],
        ["git", "commit", "-m",
            f"chore: release weekly focus week {week_num:02d}\n\n"
            f"Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>\n"
            f"Claude-Session: https://claude.ai/code/session_01TuPQgyyjEsjE236cZyznix"],
        ["git", "push"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[WARN] {' '.join(cmd)} exited {result.returncode}: {result.stderr.strip()}")
        else:
            print(f"[OK]  {' '.join(cmd[:3])}")


def main() -> None:
    week_num = get_target_week()
    source_path = DATA_DIR / f"week_{week_num:02d}.json"

    print(f"[INFO] ISO week {date.today().isocalendar()[1]} → publishing week_{week_num:02d}.json")

    if not source_path.exists():
        print(f"[ERROR] Source file not found: {source_path}")
        sys.exit(1)

    # Load, validate, copy to live location
    data = load_json(source_path)
    actual_week = data.get("meta", {}).get("week", "?")
    subject = data.get("meta", {}).get("subject", "?")
    title   = data.get("hero", {}).get("title", "?")
    print(f"[INFO] Week {actual_week} · {subject} · {title}")

    save_json(data, LIVE_FILE)

    # Also update the SEO script if present (triggers portal SEO refresh)
    seo_script = REPO_ROOT / "update_weekly_focus_seo.py"
    if seo_script.exists():
        print(f"[INFO] Running SEO update script...")
        result = subprocess.run(
            [sys.executable, str(seo_script)],
            cwd=REPO_ROOT, capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"[OK]  SEO script completed")
        else:
            print(f"[WARN] SEO script: {result.stderr.strip()}")

    # Commit and push
    dry_run = os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes")
    if dry_run:
        print("[DRY RUN] Skipping git commit/push.")
    else:
        git_commit_push(week_num)

    print(f"[DONE] Weekly focus week {week_num:02d} released successfully.")


if __name__ == "__main__":
    main()
