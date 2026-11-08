#!/usr/bin/env python3
"""
post_afternoon.py — CBSE Mock Afternoon Engagement Session (2:00 PM IST)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Posts 3 items every afternoon to Telegram from the chapter MCQ pages:

  1. CHAPTER MCQ FLASH    — 1 question as a quiz poll + link to chapter page
  2. COMMON MISTAKES SPOT — Tricky question framed as "most students get this wrong"
  3. TEACHER'S EYE        — Key examiner tip extracted from chapter MCQ explanations

All content is dynamic — sourced from the 45 chapter HTML pages in /chapters/.
Rotation: round-robin across all 45 chapters, never repeating until all done.
Separate pointer file: afternoon-tracker.json

Environment variables (GitHub Secrets):
  TELEGRAM_BOT_TOKEN
  TELEGRAM_CHAT_ID

Usage:
  python3 post_afternoon.py              # post all 3
  python3 post_afternoon.py --dry-run    # preview without posting
  python3 post_afternoon.py --mode flash # only chapter flash
  python3 post_afternoon.py --mode mistakes
  python3 post_afternoon.py --mode teacher
"""

import os, sys, json, re, random, argparse, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone, date

# ── Config ────────────────────────────────────────────────────────────────────
REPO         = Path(__file__).parent
CHAPTERS_DIR = REPO / "chapters"
TRACKER_FILE = REPO / "afternoon-tracker.json"

TG_API_BASE  = "https://api.telegram.org/bot"
BOT_TOKEN    = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID      = os.environ.get("TELEGRAM_CHAT_ID", "")
PORTAL_BASE  = "https://cbsemock.org.in"

# ── Subject emoji map ─────────────────────────────────────────────────────────
EMOJI = {
    "physics": "⚛️", "chemistry": "🧪", "mathematics": "📐", "maths": "📐",
    "biology": "🌿", "science": "🔬", "english": "📖", "hindi": "📝",
    "computer": "💻", "artificial": "🤖", "ai": "🤖", "data": "📊",
    "network": "🌐", "database": "🗄️", "sql": "🗄️", "python": "🐍",
    "oop": "🏗️", "grammar": "✍️", "writing": "✏️", "footprint": "👣",
    "flight": "📖", "genetics": "🧬", "evolution": "🧬", "neural": "⚡",
    "machine": "🧠", "ecosystem": "🌍", "biotechnology": "🧫",
}

def get_emoji(text: str) -> str:
    t = text.lower()
    for k, v in EMOJI.items():
        if k in t:
            return v
    return "📚"

# ── Chapter page parser ───────────────────────────────────────────────────────
def parse_chapter(path: Path) -> dict | None:
    """Extract chapter info and all MCQs from a chapter HTML page."""
    text = path.read_text(encoding='utf-8')

    # Title
    t = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
    title = re.sub(r'<[^>]+>', '', t.group(1)).strip() if t else path.stem

    # Class + subject from badge
    badge = re.search(r'class="chapter-badge">(.*?)</span>', text, re.S)
    badge_text = badge.group(1).strip() if badge else ""
    cls_m = re.search(r'Class (\d+)', badge_text)
    cls = cls_m.group(1) if cls_m else "12"
    # Subject from badge: "Class 12 · Computer Science"
    subj_m = re.search(r'Class \d+ · (.+)', badge_text)
    subject = subj_m.group(1).strip() if subj_m else "CBSE"

    # Extract QUESTIONS JS array from the page
    qs_match = re.search(r'const QUESTIONS\s*=\s*(\[[\s\S]*?\]);', text)
    if not qs_match:
        return None

    try:
        qs_raw = qs_match.group(1)
        # JS uses unquoted object keys: {q:"...", opts:[...], ans:"B", exp:"..."}
        # Convert to valid JSON by quoting bare keys
        json_str = re.sub(r'(?<=[{,])\s*([a-zA-Z_]\w*)\s*:', r'"\1":', qs_raw)
        questions = json.loads(json_str)
    except Exception:
        return None

    return {
        "slug": path.stem,
        "title": title,
        "class": cls,
        "subject": subject,
        "url": f"{PORTAL_BASE}/chapters/{path.stem}.html",
        "questions": questions,
    }

def load_all_chapters() -> list[dict]:
    chapters = []
    for p in sorted(CHAPTERS_DIR.glob("*.html")):
        ch = parse_chapter(p)
        if ch and ch["questions"]:
            chapters.append(ch)
    return chapters

# ── Rotation tracker ──────────────────────────────────────────────────────────
def load_tracker() -> dict:
    if TRACKER_FILE.exists():
        return json.loads(TRACKER_FILE.read_text(encoding='utf-8'))
    return {
        "flash_idx": 0,
        "mistakes_idx": 0,
        "teacher_idx": 0,
        "flash_order": [],
        "mistakes_order": [],
        "teacher_order": [],
        "last_run": "",
    }

def save_tracker(t: dict):
    TRACKER_FILE.write_text(json.dumps(t, indent=2, ensure_ascii=False), encoding='utf-8')

def get_next_chapter(tracker: dict, key: str, chapters: list[dict], dry_run: bool) -> dict:
    """Get next chapter in rotation, shuffling order when list exhausted."""
    order_key = f"{key}_order"
    idx_key   = f"{key}_idx"

    slugs = [ch["slug"] for ch in chapters]
    slug_map = {ch["slug"]: ch for ch in chapters}

    # Rebuild order if empty or stale
    if not tracker.get(order_key) or \
       set(tracker[order_key]) != set(slugs):
        order = slugs[:]
        random.shuffle(order)
        tracker[order_key] = order
        tracker[idx_key] = 0

    idx = tracker.get(idx_key, 0)
    if idx >= len(tracker[order_key]):
        # Full cycle done — reshuffle
        order = slugs[:]
        random.shuffle(order)
        tracker[order_key] = order
        idx = 0

    slug = tracker[order_key][idx]
    if not dry_run:
        tracker[idx_key] = idx + 1

    return slug_map.get(slug, chapters[0])

# ── Telegram helpers ──────────────────────────────────────────────────────────
def tg_request(method: str, payload: dict, dry_run: bool = False) -> dict:
    if dry_run:
        print(f"\n[DRY RUN] Telegram.{method}:")
        body = json.dumps(payload, indent=2, ensure_ascii=False)
        print(body[:800])
        return {"ok": True, "result": {"message_id": 0}}

    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set.")
    url  = f"{TG_API_BASE}{BOT_TOKEN}/{method}"
    data = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(url, data=data,
                                  headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"Telegram {e.code}: {body}")

def tg_send(text: str, dry_run=False) -> dict:
    return tg_request("sendMessage", {
        "chat_id": CHAT_ID, "text": text,
        "parse_mode": "HTML", "disable_web_page_preview": False,
    }, dry_run)

def tg_poll(question: str, options: list, correct_idx: int,
            explanation: str = "", dry_run=False) -> dict:
    return tg_request("sendPoll", {
        "chat_id":           CHAT_ID,
        "question":          question[:300],
        "options":           [o[:100] for o in options[:4]],
        "type":              "quiz",
        "correct_option_id": correct_idx,
        "explanation":       explanation[:200] if explanation else "",
        "is_anonymous":      True,
        "open_period":       21600,   # 6 hours
    }, dry_run)

# ── Pick question strategies ──────────────────────────────────────────────────
def pick_random_q(chapter: dict) -> dict:
    return random.choice(chapter["questions"])

def pick_tricky_q(chapter: dict) -> dict:
    """
    'Common mistake' question: prefer questions whose explanation
    mentions words like 'common', 'mistake', 'confusion', 'often',
    'many students', 'important', 'note', 'remember'.
    Fall back to random if none match.
    """
    keywords = ["common", "often", "mistake", "confus", "note that",
                "remember", "many student", "careful", "trick", "trap",
                "important", "frequently", "exception"]
    scored = []
    for q in chapter["questions"]:
        exp = q.get("exp", "").lower()
        score = sum(1 for kw in keywords if kw in exp)
        scored.append((score, q))
    scored.sort(key=lambda x: -x[0])
    top = [q for s, q in scored if s == scored[0][0]]
    return random.choice(top)

def pick_teacher_q(chapter: dict) -> dict:
    """
    'Teacher's Eye' question: prefer questions whose explanation
    is long (more detail = more examiner-worthy) or mentions
    board exam specific language.
    """
    keywords = ["cbse", "board", "exam", "mark", "evaluat", "step",
                "formulat", "definition", "derivat", "proof", "diagram",
                "always", "never", "must", "compulsory", "2 mark", "3 mark",
                "5 mark", "in exam", "examiners"]
    scored = []
    for q in chapter["questions"]:
        exp = q.get("exp", "").lower()
        score = len(exp) // 20 + sum(2 for kw in keywords if kw in exp)
        scored.append((score, q))
    scored.sort(key=lambda x: -x[0])
    top = [q for s, q in scored if s == scored[0][0]]
    return random.choice(top)

# ── Post functions ────────────────────────────────────────────────────────────
LABELS = ["A", "B", "C", "D"]

def post_flash(chapter: dict, dry_run=False):
    """1. Chapter MCQ Flash — quiz poll + teaser text."""
    q    = pick_random_q(chapter)
    opts = q["opts"]
    ans  = q["ans"]
    exp  = q.get("exp", "")
    ci   = LABELS.index(ans) if ans in LABELS else 0
    emoji = get_emoji(chapter["subject"] + " " + chapter["title"])

    teaser = (
        f"⚡ <b>Chapter MCQ Flash</b>\n\n"
        f"{emoji} <b>{chapter['title']}</b>\n"
        f"📘 Class {chapter['class']} · {chapter['subject']}\n\n"
        f"🎯 Quick 6-hour poll — test yourself before the answer locks!\n\n"
        f"🔗 <a href='{chapter['url']}'>Practice full chapter (12 Qs) →</a>\n\n"
        f"#CBSE #Class{chapter['class']} #{chapter['subject'].replace(' ','')} "
        f"#ChapterMCQ #BoardExams2027"
    )
    tg_send(teaser, dry_run)
    result = tg_poll(
        question=q["q"],
        options=opts,
        correct_idx=ci,
        explanation=exp[:200],
        dry_run=dry_run,
    )
    mid = result.get("result", {}).get("message_id", "n/a")
    print(f"[OK] Flash posted: {chapter['title']} → msg {mid}")

def post_mistakes(chapter: dict, dry_run=False):
    """2. Common Mistakes Spotlight."""
    q     = pick_tricky_q(chapter)
    opts  = q["opts"]
    ans   = q["ans"]
    exp   = q.get("exp", "")
    ci    = LABELS.index(ans) if ans in LABELS else 0
    emoji = get_emoji(chapter["subject"] + " " + chapter["title"])

    # Build 'wrong trap' — the first wrong option text
    wrong_opts = [o for i, o in enumerate(opts) if LABELS[i] != ans]
    trap = wrong_opts[0] if wrong_opts else opts[0]

    teaser = (
        f"⚠️ <b>Common Mistakes Spotlight</b>\n\n"
        f"{emoji} <b>{chapter['title']}</b> — Class {chapter['class']}\n\n"
        f"🔴 <b>Most students pick the wrong answer here!</b>\n"
        f"❌ Common trap: <i>\"{trap}\"</i>\n\n"
        f"💡 Can you spot what's really correct?\n"
        f"👇 Answer in the poll and check the explanation!\n\n"
        f"📌 <a href='{chapter['url']}'>See all tricky Qs for this chapter →</a>\n\n"
        f"#CBSEMistakes #Class{chapter['class']} #ExamTips #BoardPrep2027"
    )
    tg_send(teaser, dry_run)
    result = tg_poll(
        question=f"⚠️ TRICKY: {q['q']}",
        options=opts,
        correct_idx=ci,
        explanation=f"💡 {exp[:190]}",
        dry_run=dry_run,
    )
    mid = result.get("result", {}).get("message_id", "n/a")
    print(f"[OK] Mistakes posted: {chapter['title']} → msg {mid}")

def post_teacher(chapter: dict, dry_run=False):
    """3. Teacher's Eye — examiner tip from explanation text."""
    q     = pick_teacher_q(chapter)
    exp   = q.get("exp", "")
    ans   = q["ans"]
    opts  = q["opts"]
    ci    = LABELS.index(ans) if ans in LABELS else 0
    emoji = get_emoji(chapter["subject"] + " " + chapter["title"])

    # Correct answer text
    correct_text = opts[ci] if ci < len(opts) else ans

    # Extract the core teaching point from explanation (first sentence)
    first_sentence = re.split(r'(?<=[.!?])\s', exp.strip())[0] if exp else ""
    # Truncate for display
    tip = first_sentence[:220] if first_sentence else exp[:220]

    teaser = (
        f"👩‍🏫 <b>Teacher's Eye</b>\n\n"
        f"{emoji} <b>{chapter['title']}</b> — Class {chapter['class']} {chapter['subject']}\n\n"
        f"🎓 <b>What examiners always look for:</b>\n\n"
        f"❓ <i>{q['q'][:200]}</i>\n\n"
        f"✅ <b>Correct answer: {correct_text}</b>\n\n"
        f"📝 <b>Examiner's explanation:</b>\n"
        f"<i>{tip}</i>\n\n"
        f"💡 Knowing the WHY is what separates 90+ scorers!\n\n"
        f"🔗 <a href='{chapter['url']}'>Master this chapter →</a>\n\n"
        f"#TeachersEye #CBSE #Class{chapter['class']} #ExaminerTips #BoardExams2027"
    )
    result = tg_send(teaser, dry_run)
    mid = result.get("result", {}).get("message_id", "n/a")
    print(f"[OK] Teacher's Eye posted: {chapter['title']} → msg {mid}")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="CBSE Mock afternoon engagement poster")
    parser.add_argument("--mode", default="all",
        choices=["all", "flash", "mistakes", "teacher"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"Afternoon Poster — mode={args.mode} dry_run={args.dry_run}")

    chapters = load_all_chapters()
    if not chapters:
        print("[ERROR] No chapter pages found in /chapters/")
        sys.exit(1)
    print(f"Loaded {len(chapters)} chapter pages")

    tracker = load_tracker()
    # Seed random with today's date for consistent picks within same day
    random.seed(int(date.today().strftime("%Y%m%d")))

    modes = ["flash", "mistakes", "teacher"] if args.mode == "all" else [args.mode]

    for mode in modes:
        print(f"\n── {mode} ──")
        chapter = get_next_chapter(tracker, mode, chapters, args.dry_run)
        print(f"   Chapter: {chapter['title']} (Class {chapter['class']} {chapter['subject']})")

        if mode == "flash":
            post_flash(chapter, args.dry_run)
        elif mode == "mistakes":
            post_mistakes(chapter, args.dry_run)
        elif mode == "teacher":
            post_teacher(chapter, args.dry_run)

    if not args.dry_run:
        tracker["last_run"] = datetime.now(timezone.utc).isoformat()
        save_tracker(tracker)
        print("\n[OK] Tracker saved.")

    print("\nDone.")

if __name__ == "__main__":
    main()
