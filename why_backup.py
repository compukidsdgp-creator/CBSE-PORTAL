#!/usr/bin/env python3
"""
why_backup.py — the WHY? reels backup queue, made from the owner's plan (formula-posts/why/plan.json).

A daily writer adds one reel module why_reels/<name>.py with PLAN_RANK = <rank>. The render workflow turns every such
module that has no video yet into formula-posts/why/backup/<rank:03d>_why_<name>.mp4 (+ .txt caption).
post_why_reel.py posts from formula-posts/why/queue/ first and, when that is empty, from the backup in rank order.

    python3 why_backup.py next            the plan entry the writer should make next (JSON)
    python3 why_backup.py render-missing  render every planned module without a video into the backup (prints new files)
    python3 why_backup.py status          counts: queue, backup, plan progress
"""
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WHY = ROOT / "formula-posts" / "why"
PLAN, BACKUP, QUEUE, POSTED = WHY / "plan.json", WHY / "backup", WHY / "queue", WHY / "posted"


def plan():
    return json.loads(PLAN.read_text(encoding="utf-8"))["reels"]


def modules():
    """{rank: module_name} for every why_reels module that declares PLAN_RANK."""
    out = {}
    for f in sorted((ROOT / "why_reels").glob("[a-z]*.py")):
        m = re.search(r"^PLAN_RANK\s*=\s*(\d+)", f.read_text(encoding="utf-8"), re.M)
        if m:
            out[int(m.group(1))] = f.stem
    return out


def has_video(name):
    return any(True for d in (BACKUP, QUEUE, POSTED) if d.exists() for _ in d.glob(f"*_why_{name}.mp4"))


def next_job():
    done = modules()
    for r in plan():
        if r.get("skip") or r["rank"] in done:
            continue
        return {"action": "write", **r}
    return {"action": "none"}


def render_missing():
    BACKUP.mkdir(parents=True, exist_ok=True)
    new = []
    for rank, name in sorted(modules().items()):
        if has_video(name):
            continue
        out = BACKUP / f"{rank:03d}_why_{name}.mp4"
        print(f"[backup] rendering #{rank} {name} …", flush=True)
        _cli(name, out)
        mod = importlib.import_module(f"why_reels.{name}")
        out.with_suffix(".txt").write_text(mod.CAPTION.strip() + "\n", encoding="utf-8")
        new.append(str(out.relative_to(ROOT)))
    print("\n".join(new) if new else "[backup] nothing to render")
    return new


def _cli(name, out):
    import subprocess
    subprocess.run([sys.executable, str(ROOT / "why_kit.py"), "--reel", name, "--out", str(out)], check=True)


def status():
    q = len(list(QUEUE.glob("*.mp4"))) if QUEUE.exists() else 0
    b = len(list(BACKUP.glob("*.mp4"))) if BACKUP.exists() else 0
    p = plan()
    todo = [r for r in p if not r.get("skip")]
    done = modules()
    print(f"queue: {q} reels · backup: {b} reels · plan: {len([r for r in todo if r['rank'] in done])}/{len(todo)} written "
          f"({len([r for r in p if r.get('skip')])} skipped)")
    nx = next_job()
    print("next:", f"#{nx['rank']} {nx['title']}" if nx["action"] == "write" else "none")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "next":
        print(json.dumps(next_job(), ensure_ascii=False, indent=1))
    elif cmd == "render-missing":
        render_missing()
    else:
        status()
