"""Private Telegram message to the owner when the nightly run commits a new or revised chapter draft.

Reads the commit message (env MSG): first line "notes: draft <title>" or "notes: revise <title>",
and a line "Preview: <url>". Sends to SEO_REPORT_CHAT_ID only (never the public channel).
"""
import json
import os
import re
import urllib.request

token, chat, msg = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("SEO_REPORT_CHAT_ID"), os.environ.get("MSG", "")
lines = msg.splitlines() or [""]
if not (token and chat) or not re.match(r"(notes|booster|lab): (draft|revise)\b", lines[0]):
    print("[notify] nothing to send"); raise SystemExit
url = next((l.split("Preview: ", 1)[1].strip() for l in lines if l.startswith("Preview: ")), "")
booster = lines[0].startswith("booster:")
lab = lines[0].startswith("lab:")
rev = re.match(r"\w+: revise", lines[0])
kind = ("Revised lab" if rev else "New virtual lab draft") if lab else ("Revised booster" if rev else "New Weekly Knowledge Booster draft") if booster else ("Revised chapter" if rev else "New chapter draft")
title = re.sub(r"^\w+: (draft|revise)\s*", "", lines[0])
icon = "🔬" if lab else "⚡" if booster else "📘"
text = (f"{icon} <b>{kind} ready for review</b>\n{title}\n\n" + (f"Preview: {url}\n" if url else "")
        + "Approve or request changes in the admin panel → Content tracker"
        + (" → Weekly Knowledge Booster" if booster else " → Virtual labs" if lab else "") + ":\nhttps://cbsemock.org.in/admin/")
req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
                             data=json.dumps({"chat_id": chat, "text": text, "parse_mode": "HTML",
                                              "disable_web_page_preview": True}).encode(),
                             headers={"Content-Type": "application/json"})
print("[notify]", urllib.request.urlopen(req, timeout=20).read()[:60])
