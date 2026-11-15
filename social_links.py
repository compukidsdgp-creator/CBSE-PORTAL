"""Topic-specific links for social posts.

Facebook: the caption stays as it is and the exact links (explainer / chapter quiz / mock papers) go in the
first comment, posted straight after the reel or card — a common way to share links without the post itself
carrying an outside link. Instagram: links in captions are not clickable, so the web-address lines become a
short "link in bio" line pointing at cbsemock.org.in/go/, which lists the latest posts with their links.

A failed comment never fails a post (it needs the page token's comment permission).
"""
import json
import re
import urllib.error
import urllib.parse
import urllib.request

from topic_links import SITE, why_links, formula_links

FB_API = "https://graph.facebook.com/v27.0"
GO_URL = "cbsemock.org.in/go"


def comment_text(links, topic=""):
    lines = []
    if links.get("learn"):
        lines.append(f"📘 Read the full explainer: {links['learn'][1]}")
    for t, u in links.get("chapters", [])[:1]:
        lines.append(f"📝 Practise {t.replace(' quiz', '')} (free quiz with answers): {u}")
    if links.get("portal"):
        lines.append(f"📄 {links['portal'][0]}: {links['portal'][1]}")
    if not lines:
        lines.append(f"🌐 Free notes & mock papers: {SITE}")
    head = f"🔗 {topic} — practise it now 👇" if topic else "🔗 Practise this topic 👇"
    return head + "\n" + "\n".join(lines)


def ig_caption(caption):
    """Swap web-address lines (not clickable on Instagram) for one 'link in bio' line."""
    out, done = [], False
    for line in caption.splitlines():
        if re.search(r"cbsemock\.org\.in|https?://", line) and not line.strip().startswith("#"):
            if not done:
                out.append(f"🔗 Practise this topic — link in bio ({GO_URL})")
                done = True
            continue
        out.append(line)
    return "\n".join(out)


def post_fb_comment(object_id, message, token, dry_run=False):
    if not object_id or str(object_id).startswith("dry-run") or dry_run:
        print(f"[FB comment] (dry run) on {object_id}:\n{message}")
        return None
    if not token:
        print("[FB comment] no token — skipped")
        return None
    data = urllib.parse.urlencode({"message": message, "access_token": token}).encode()
    targets = [str(object_id)]
    try:                                    # a reel's video id can't take comments — its post id can
        q = urllib.parse.urlencode({"fields": "post_id", "access_token": token})
        with urllib.request.urlopen(f"{FB_API}/{object_id}?{q}", timeout=20) as r:
            pid = json.load(r).get("post_id")
        if pid:
            targets.insert(0, pid if "_" in str(pid) else str(pid))
    except Exception:
        pass
    err = ""
    for t in targets:
        try:
            with urllib.request.urlopen(urllib.request.Request(f"{FB_API}/{t}/comments", data=data), timeout=30) as r:
                cid = json.load(r).get("id")
                print(f"[FB comment OK] {cid}")
                return cid
        except urllib.error.HTTPError as e:
            err = f"({e.code}): {e.read().decode()[:200]}"
        except Exception as e:
            err = str(e)
    print(f"::warning::Facebook link comment failed {err}")
    if "(#200)" in err:
        print("::warning::The Facebook page token needs the pages_manage_engagement permission for link comments.")
    return None


# ── resolvers for each kind of post ─────────────────────────────────────────
def links_for_why(filename):
    return why_links(filename)


def links_for_formula_reel(stem):
    """stem of a formula-reel queue file, e.g. 'electrostatics_coulomb_s_law_part_1'."""
    try:
        from formula_topics_master import TOPICS
        from generate_formula_reel_v3 import queue_name, class_label
        try:
            from formula_topics_feb import TOPICS_FEB
        except Exception:
            TOPICS_FEB = {}
        base = re.sub(r"_part_\d+$", "", stem)
        for tid, d in {**TOPICS, **TOPICS_FEB}.items():
            if tid in TOPICS and queue_name(tid, 1, 1)[:-4] == base or \
               re.sub(r"[^a-z0-9]+", "_", f"{d['title_line1']} {d['title_line2']}".lower()).strip("_") == base:
                cls = class_label(d.get("chapter_tag", "")).replace("Class ", "")
                return formula_links(d["subject"], f"{tid.replace('_', ' ')} {d['title_line1']} {d['title_line2']}", cls)
    except Exception as e:
        print(f"[links] formula reel lookup failed: {e}")
    return formula_links("", stem.replace("_", " "), "")


def links_for_formula_image(subject, topic, cls):
    name = {"maths": "Maths", "mathematics": "Maths", "cs": "CS", "computer": "CS", "ai": "AI"}.get(
        (subject or "").lower(), (subject or "").title())
    return formula_links(name, topic, (cls or "").replace("class", ""))
