"""Exit 0 and print "yes" if this workflow already had a SUCCESSFUL run today (India time), else print "no".

Used as a guard so a scheduled post can be triggered from more than one place (GitHub's own
schedule, which is often late or skipped, plus an external scheduler) without ever posting twice.

    python3 already_posted_today.py weekly-promo.yml
Needs GITHUB_TOKEN (actions: read) and GITHUB_REPOSITORY in the environment.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))


def main():
    wf = sys.argv[1]
    repo = os.environ.get("GITHUB_REPOSITORY", "compukidsdgp-creator/CBSE-PORTAL")
    token = os.environ.get("GITHUB_TOKEN", "")
    midnight_ist = datetime.now(IST).replace(hour=0, minute=0, second=0, microsecond=0)
    since = midnight_ist.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = (f"https://api.github.com/repos/{repo}/actions/workflows/{wf}/runs"
           f"?status=success&per_page=5&created=%3E%3D{since}")
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               **({"Authorization": f"Bearer {token}"} if token else {})})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            runs = json.load(r).get("workflow_runs", [])
    except Exception as e:                      # never block a post because the check itself failed
        print("no")
        print(f"[guard] could not check earlier runs: {e}", file=sys.stderr)
        return
    me = os.environ.get("GITHUB_RUN_ID", "")
    done = [r for r in runs if str(r.get("id")) != me]
    print("yes" if done else "no")
    if done:
        print(f"[guard] {wf} already succeeded today at {done[0].get('created_at')} — skipping", file=sys.stderr)


if __name__ == "__main__":
    main()
