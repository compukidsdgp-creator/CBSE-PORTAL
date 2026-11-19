"""Private Telegram message to the owner when new Mock Zone papers go live (publishing is direct; this is for spot-checks).

Compares the mockzone_bank/*.json files between two commits (env BEFORE, AFTER), works out which papers were added per page,
and sends the page link, the new paper numbers and two of the new questions with their answers.
Sends to SEO_REPORT_CHAT_ID only (never the public channel).
    BEFORE=<sha> AFTER=<sha> python3 notify_mockzone.py
"""
import html
import json
import os
import random
import re
import subprocess
import urllib.request

E = html.escape
token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("SEO_REPORT_CHAT_ID")
before, after = os.environ.get("BEFORE", "HEAD~1"), os.environ.get("AFTER", "HEAD")
PAPERS = 15


def show(rev, path):
    try:
        return json.loads(subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout)
    except Exception:
        return None


def fresh(bank):
    return min(len(p["items"]) // p["per_paper"] for p in bank["pools"].values()) if bank else 0


def plain(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", str(t))).strip()


def sample(bank, start):
    """Two random new items (with answers) from papers ≥ start."""
    out = []
    for name, p in bank["pools"].items():
        k = p["per_paper"]
        out += [(name, it) for it in p["items"][start * k:] if isinstance(it, dict)]
    picks = random.sample(out, min(2, len(out)))
    lines = []
    for name, it in picks:
        q = plain(it.get("q") or it.get("question") or it.get("text") or it.get("passage") or "")[:350]
        opts = " | ".join(plain(o) for o in it.get("opts", []))[:250]
        ans = plain(it.get("ans") or it.get("answer") or "")
        key = plain(it.get("key") or "")
        a = (ans + (" — " + key if key else ""))[:450]
        lines.append(f"<b>Q</b> {E(q)}" + (f"\n<i>{E(opts)}</i>" if opts else "") + f"\n<b>A</b> {E(a)}")
    return "\n\n".join(lines)


files = subprocess.run(["git", "diff", "--name-only", before, after, "--", "mockzone_bank/"],
                       capture_output=True, text=True).stdout.split()
msgs = []
for f in [x for x in files if x.endswith(".json")]:
    new, old = show(after, f), show(before, f)
    if not new:
        continue
    a, b = fresh(old), fresh(new)
    if b <= a:
        continue
    page = new["page"]
    papers = f"Paper {a + 1}" if b == a + 1 else f"Papers {a + 1}–{b}"
    title = re.sub(r"^cbse-class-(\d+)-(.*?)-(mock-papers|mock-tests|practice-papers)\.html$", r"Class \1 \2", page).replace("-", " ").title()
    msgs.append(f"📝 <b>Mock Zone: {E(title)} — {papers} now live</b> ({b}/{PAPERS} fresh)\n"
                f"https://cbsemock.org.in/{page}\n\n<b>Spot-check (2 random new questions):</b>\n{sample(new, a)}")

if not msgs:
    print("[notify-mockzone] nothing to send"); raise SystemExit
if not (token and chat):
    print("[notify-mockzone] dry run (no token):\n\n" + "\n\n---\n\n".join(msgs)); raise SystemExit
for text in msgs:
    text = text[:4000]
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
                                 data=json.dumps({"chat_id": chat, "text": text, "parse_mode": "HTML",
                                                  "disable_web_page_preview": True}).encode(),
                                 headers={"Content-Type": "application/json"})
    print("[notify-mockzone]", urllib.request.urlopen(req, timeout=20).read()[:60])
