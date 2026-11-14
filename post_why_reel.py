#!/usr/bin/env python3
"""
post_why_reel.py — posts the next "WHY?" reel (Sunday + Wednesday 6:30 PM IST) to Facebook + Instagram.

Queue : formula-posts/why/queue/NN_why_<slug>.mp4   (+ optional NN_why_<slug>.txt = caption)
Posted: formula-posts/why/posted/
Reels are posted in file-name order and never recycled: when the queue is empty the run
stops with a warning so new WHY? reels can be added.

    python3 post_why_reel.py            # post the next one
    python3 post_why_reel.py --dry-run
    python3 post_why_reel.py --status
"""
import argparse
import shutil
import sys
from pathlib import Path

import post_formula_reel as P

ROOT = Path(__file__).parent
QUEUE = ROOT / "formula-posts" / "why" / "queue"
POSTED = ROOT / "formula-posts" / "why" / "posted"
QUEUE.mkdir(parents=True, exist_ok=True)
POSTED.mkdir(parents=True, exist_ok=True)
P.LOG_CSV = ROOT / "formula-posts" / "why" / "why_log.csv"


def default_caption(stem):
    title = stem.split("_why_", 1)[-1].replace("_", " ").strip().capitalize()
    return (f"🤔 WHY? — {title}\n\n"
            "Don't just memorise it — see why it works! 👀\n\n"
            "💾 Save this for revision · 📤 Share with your batchmates\n\n"
            "🌐 Free notes & mock papers → https://cbsemock.org.in\n"
            "📲 Telegram: t.me/cbsemockportal\n\n"
            "#WhySeries #CBSEMock #VisualMaths #ConceptClear #BoardExam2027 #CBSE")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    queued = sorted(QUEUE.glob("*.mp4"))
    if a.status:
        print("Queue:", [q.name for q in queued]); print("Posted:", sorted(p.name for p in POSTED.glob("*.mp4")))
        return
    if not queued:
        print("::warning::The WHY? queue is empty — add new WHY? reels to formula-posts/why/queue/")
        return
    reel = queued[0]
    txt = reel.with_suffix(".txt")
    caption = txt.read_text(encoding="utf-8").strip() if txt.exists() else default_caption(reel.stem)
    print(f"[WHY] {reel.name} ({len(queued)} in queue)\n{caption[:200]}\n")
    fb = P._upload_video_fb(reel, caption, dry_run=a.dry_run)
    ig = P._upload_reel_instagram(reel, caption, dry_run=a.dry_run)
    if not a.dry_run and (fb or ig):
        shutil.move(str(reel), str(POSTED / reel.name))
        if txt.exists():
            shutil.move(str(txt), str(POSTED / txt.name))
    P.log_reel(reel.name, fb, ig, a.dry_run)
    print(f"FB: {fb or 'FAILED'} | IG: {ig or 'FAILED'}")
    sys.exit(0 if (fb and ig) else 1)


if __name__ == "__main__":
    main()
