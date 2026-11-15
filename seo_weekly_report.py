"""Weekly SEO report → Telegram (owner's chat).

Search Console, last 7 days vs the 7 before: clicks, impressions, average position,
top searches, biggest movers and pages ranking 5–15 ("almost on page 1").

Env: GSC_SERVICE_ACCOUNT_JSON, GSC_PROPERTY (optional), TELEGRAM_BOT_TOKEN,
     SEO_REPORT_CHAT_ID — the OWNER's private chat id. Never the public channel:
     the report is private, so it is skipped if this is not set.
     python3 seo_weekly_report.py [--dry-run]
"""
import argparse
import html
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import timedelta

import build_admin_data as B


def query(tok, prop, start, end, dims, limit=25):
    base = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(prop, safe='')}/searchAnalytics/query"
    return B.post_json(base, {"startDate": str(start), "endDate": str(end), "dimensions": dims, "rowLimit": limit}, tok).get("rows", [])


def totals(rows):
    c = sum(r["clicks"] for r in rows); i = sum(r["impressions"] for r in rows)
    pos = (sum(r["position"] * r["impressions"] for r in rows) / i) if i else 0
    return c, i, pos


def arrow(new, old, lower_is_better=False):
    if old == 0:
        return "🆕" if new else "–"
    ch = (new - old) / old * 100
    good = ch < 0 if lower_is_better else ch > 0
    return f"{'🟢' if good else '🔴'} {ch:+.0f}%"


def build_message():
    tok = B.google_token("https://www.googleapis.com/auth/webmasters.readonly")
    if not tok:
        return None, "Search Console is not connected (GSC_SERVICE_ACCOUNT_JSON missing or invalid)."
    prop = os.environ.get("GSC_PROPERTY") or "https://cbsemock.org.in/"
    end = B.TODAY - timedelta(days=2)
    start = end - timedelta(days=6)
    pend, pstart = start - timedelta(days=1), start - timedelta(days=7)
    cur = query(tok, prop, start, end, ["date"])
    prev = query(tok, prop, pstart, pend, ["date"])
    if not cur and not prev:
        return None, "Search Console has no data yet (new properties take a few days)."
    c, i, p = totals(cur)
    pc, pi, pp = totals(prev)
    q = query(tok, prop, start, end, ["query"], 10)
    pages = query(tok, prop, start, end, ["page"], 200)
    near = sorted([r for r in pages if 4.5 <= r["position"] <= 15], key=lambda r: -r["impressions"])[:5]
    top_pages = sorted(pages, key=lambda r: -r["clicks"])[:5]
    e = html.escape
    lines = [
        f"📈 <b>CBSEMock weekly SEO report</b>",
        f"<i>{start:%d %b} – {end:%d %b} vs previous week</i>",
        "",
        f"👆 Clicks: <b>{c:,}</b>  {arrow(c, pc)}",
        f"👀 Impressions: <b>{i:,}</b>  {arrow(i, pi)}",
        f"📍 Avg position: <b>{p:.1f}</b>  {arrow(p, pp, lower_is_better=True)}",
    ]
    if q:
        lines += ["", "🔎 <b>Top searches</b>"] + [f"• {e(r['keys'][0])} — {r['clicks']} clicks, pos {r['position']:.1f}" for r in q[:7]]
    if top_pages:
        lines += ["", "🏆 <b>Top pages</b>"] + [f"• {e(r['keys'][0].replace('https://cbsemock.org.in', '') or '/')} — {r['clicks']} clicks" for r in top_pages]
    if near:
        lines += ["", "🎯 <b>Almost on page 1</b> (improve these first)"] + [
            f"• {e(r['keys'][0].replace('https://cbsemock.org.in', '') or '/')} — pos {r['position']:.1f}, {r['impressions']} views" for r in near]
    lines += ["", "Full dashboard: https://cbsemock.org.in/admin/"]
    return "\n".join(lines), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    msg, problem = build_message()
    if problem:
        msg = f"📈 <b>CBSEMock weekly SEO report</b>\n\n{html.escape(problem)}"
    print(msg)
    if a.dry_run:
        return
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("SEO_REPORT_CHAT_ID")       # private chat only — never the public channel
    if not token or not chat:
        print("[skip] SEO_REPORT_CHAT_ID / TELEGRAM_BOT_TOKEN not set — report not sent"); return
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
                                 data=json.dumps({"chat_id": chat, "text": msg, "parse_mode": "HTML",
                                                  "disable_web_page_preview": True}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        print("[ok] sent" if json.load(r).get("ok") else "[warn] Telegram rejected the message")


if __name__ == "__main__":
    main()
