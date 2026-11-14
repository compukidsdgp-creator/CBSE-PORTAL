#!/usr/bin/env python3
"""
CBSE Mock — Free Mock Paper Post

  python3 post_pyq.py --today            # Mon/Wed/Fri: Class 10 + Class 12 paper, never repeated
  python3 post_pyq.py --today --dry-run  # build everything, post nothing

Papers come from the JSON pool in question-bank/ (see mock_bank.py).

(Older description follows.)
CBSE Mock — PYQ Practice Paper Daily Post
Generates a branded cover image, commits the PDF to the repo,
and posts to Telegram + Facebook + Instagram.

Usage:
  python3 post_pyq.py --subject science10
  python3 post_pyq.py --subject physics12 --dry-run
"""

import os, sys, json, argparse, subprocess, textwrap
from datetime import date
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow not installed — pip install Pillow --break-system-packages")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("requests not installed — pip install requests --break-system-packages")
    sys.exit(1)

# ─── Paths ───────────────────────────────────────────────────────────────────

REPO_ROOT   = Path(__file__).parent
OUTPUT_DIR  = REPO_ROOT / "pyq-papers"
OUTPUT_DIR.mkdir(exist_ok=True)

# ─── Subject display names ────────────────────────────────────────────────────

SUBJECT_META = {
    "science10":   {"label": "Science", "class": "X",   "bank": "cl10_science"},
    "maths10":     {"label": "Mathematics", "class": "X",   "bank": "cl10_maths"},
    "physics12":   {"label": "Physics",  "class": "XII", "bank": "cl12_physics"},
    "maths12":     {"label": "Mathematics", "class": "XII", "bank": "cl12_maths"},
    "chemistry12": {"label": "Chemistry","class": "XII", "bank": "cl12_chemistry"},
    "biology12":   {"label": "Biology",  "class": "XII", "bank": "cl12_biology"},
}

# ─── Brand colours ───────────────────────────────────────────────────────────

BRAND_BLUE   = (21,  101, 192)   # #1565C0
BRAND_ORANGE = (230,  81,   0)   # #E65100
WHITE        = (255, 255, 255)
CREAM        = (255, 253, 231)
DARK_GREY    = ( 66,  66,  66)
GOLD         = (249, 168,  37)

# ─── Image generator ─────────────────────────────────────────────────────────

FONT_DIR   = REPO_ROOT / "assets" / "fonts"
LOGO_CIRCLE = REPO_ROOT / "formula-posts" / "_cbsemock_logo_circle.png"

# Top-half colour per class, so the two papers of the day are easy to tell apart
COVER_THEME = {
    "X":   {"top": (255, 214, 0),  "chip_text": (255, 214, 0)},    # yellow
    "XII": {"top": (0, 212, 255),  "chip_text": (0, 212, 255)},    # cyan
}

def build_cover_image(subject_key: str, paper_date: str, pdf_url: str) -> str:
    """Create the 1080x1080 'Bold Poster' cover (JPEG). Returns its path."""
    from PIL import ImageFilter
    meta    = SUBJECT_META[subject_key]
    cls     = meta["class"]
    subject = meta["label"].upper()
    theme   = COVER_THEME.get(cls, COVER_THEME["X"])
    TOP, NAVY, WHITE = theme["top"], (8, 20, 48), (255, 255, 255)
    BLUE, ORANGE = (21, 101, 192), (230, 81, 0)

    S = 2                                   # draw at 2x, shrink at the end for smooth edges
    W = H = 1080 * S

    def font(size, weight="Bold"):
        fallbacks = {"Bold": "DejaVuSans-Bold.ttf", "Medium": "DejaVuSans.ttf", "Regular": "DejaVuSans.ttf"}
        for path in (FONT_DIR / f"Poppins-{weight}.ttf",
                     Path("/usr/share/fonts/truetype/dejavu") / fallbacks[weight]):
            if path.exists():
                try:
                    return ImageFont.truetype(str(path), int(size * S))
                except Exception:
                    pass
        return ImageFont.load_default()

    def fit(text, size, max_w, weight="Bold"):
        f = font(size, weight)
        while f.getlength(text) > max_w * S and size > 12:
            size -= 2; f = font(size, weight)
        return f

    def P(*v):
        return tuple(int(x * S) for x in v)

    def txt(d, xy, s_, f, fill, anchor="la", stroke=0):
        d.text(P(*xy), s_, font=f, fill=fill, anchor=anchor,
               stroke_width=int(stroke * S), stroke_fill=fill)

    def rr(d, box, r, fill=None, outline=None, width=0):
        d.rounded_rectangle(P(*box), radius=int(r * S), fill=fill, outline=outline, width=int(width * S))

    img = Image.new("RGBA", (W, H), (*NAVY, 255))
    d = ImageDraw.Draw(img)
    d.polygon([P(0, 0), P(1080, 0), P(1080, 430), P(0, 540)], fill=TOP)
    d.polygon([P(0, 540), P(1080, 430), P(1080, 448), P(0, 558)], fill=WHITE)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse(P(520, 520, 1280, 1280), fill=(*BLUE, 90))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(170 * S)))
    d = ImageDraw.Draw(img)

    # ── Logo on a white disc (the logo's inside is see-through) + wordmark ────
    x = 44
    if LOGO_CIRCLE.exists():
        lg = Image.open(LOGO_CIRCLE).convert("RGBA").resize(P(120, 120), Image.LANCZOS)
        disc = Image.new("RGBA", lg.size, (0, 0, 0, 0))
        m = int(120 * S * 0.035)
        ImageDraw.Draw(disc).ellipse([m, m, lg.width - m, lg.height - m], fill=(255, 255, 255, 255))
        img.alpha_composite(disc, P(36, 18)); img.alpha_composite(lg, P(36, 18))
        d = ImageDraw.Draw(img); x = 168
    f = font(40)
    txt(d, (x, 78), "CBSE", f, NAVY, "lm"); x += f.getlength("CBSE") / S
    txt(d, (x, 78), "MOCK", f, BLUE, "lm"); x += f.getlength("MOCK") / S
    txt(d, (x + 4, 83), ".ORG.IN", font(24, "Medium"), NAVY, "lm")

    # ── Class chip ───────────────────────────────────────────────────────────
    f = font(28); w = f.getlength(f"CLASS {cls}") / S
    rr(d, (1036 - w - 44, 50, 1036, 106), 28, fill=NAVY)
    txt(d, (1036 - w / 2 - 22, 79), f"CLASS {cls}", f, theme["chip_text"], "mm")

    # ── Headline: the day's name, e.g. MONDAY'S FREE MOCK PAPER ──────────────
    from datetime import datetime as _dt
    try:
        weekday = _dt.strptime(paper_date, "%d %B %Y").strftime("%A")
    except ValueError:
        weekday = date.today().strftime("%A")
    line1 = f"{weekday.upper()}'S FREE"
    txt(d, (44, 192), line1, fit(line1, 132, 990), NAVY, "lm", stroke=2)
    txt(d, (44, 322), "MOCK PAPER", fit("MOCK PAPER", 132, 990), NAVY, "lm", stroke=2)

    # ── This week's papers strip: Mon / Wed / Fri, today's day highlighted ───
    f = font(23)
    lead = "THIS WEEK'S FREE MOCK PAPERS FOR CLASS X & XII"
    f = fit(lead, 23, 560)
    txt(d, (46, 421), lead, f, NAVY, "lm")
    px = 46 + f.getlength(lead) / S + 18
    for short in ("MON", "WED", "FRI"):
        on = weekday.upper().startswith(short)
        rr(d, (px, 400, px + 84, 442), 21, fill=NAVY if on else None, outline=NAVY, width=2.5)
        txt(d, (px + 42, 421), short, font(22), TOP if on else NAVY, "mm")
        px += 94

    # ── Badge, subject, date ─────────────────────────────────────────────────
    badge = "FREE PRE-BOARD PRACTICE PAPER"
    f = font(22); w = f.getlength(badge) / S
    rr(d, (44, 590, 44 + w + 40, 636), 23, outline=TOP, width=2)
    txt(d, (64, 614), badge, f, TOP, "lm")
    txt(d, (40, 714), subject, fit(subject, 130, 620), WHITE, "lm", stroke=1.5)
    txt(d, (44, 796), paper_date, font(28, "Medium"), TOP, "lm")

    # ── Question-paper illustration ──────────────────────────────────────────
    pw, ph = 250, 330
    sheet = Image.new("RGBA", P(pw + 40, ph + 40), (0, 0, 0, 0))
    shadow = Image.new("RGBA", sheet.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(P(32, 34, pw + 32, ph + 34), radius=16 * S, fill=(0, 0, 0, 110))
    sheet.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10 * S)))
    sd = ImageDraw.Draw(sheet)
    rr(sd, (20, 16, pw + 20, ph + 16), 16, fill=WHITE)
    rr(sd, (20, 16, pw + 20, 76), 16, fill=BLUE); sd.rectangle(P(20, 56, pw + 20, 76), fill=BLUE)
    txt(sd, (20 + pw / 2, 46), "MOCK PAPER", font(22), WHITE, "mm")
    y = 104
    for qn in range(3):
        sd.ellipse(P(40, y, 66, y + 26), fill=BLUE)
        txt(sd, (53, y + 13), str(qn + 1), font(14), WHITE, "mm")
        rr(sd, (78, y + 3, pw - 6, y + 13), 5, fill=(205, 214, 228))
        rr(sd, (78, y + 21, pw - 70 - qn * 18, y + 31), 5, fill=(225, 231, 240))
        for k in range(2):
            sd.ellipse(P(80 + k * 96, y + 44, 94 + k * 96, y + 58), outline=(150, 165, 185), width=2 * S)
            rr(sd, (100 + k * 96, y + 47, 156 + k * 96, y + 55), 4, fill=(225, 231, 240))
        y += 72
    rot = sheet.rotate(8, expand=True, resample=Image.BICUBIC)
    cx, cy = P(880, 680)
    img.alpha_composite(rot, (cx - rot.width // 2, cy - rot.height // 2))
    d = ImageDraw.Draw(img)

    # ── Supporting lines ─────────────────────────────────────────────────────
    l1 = "Get our Free Pre-Board Practice Paper"
    l2 = "Every Mon, Wed & Fri for Your Practice!  We are committed to your success."
    txt(d, (44, 846), l1, fit(l1, 30, 700), WHITE, "lm")
    txt(d, (44, 884), l2, fit(l2, 24, 990, "Medium"), (200, 215, 240), "lm")

    # ── Call to action ───────────────────────────────────────────────────────
    rr(d, (44, 918, 1036, 1046), 64, fill=WHITE)
    l3 = "Get today's paper link below  •  Also available on our Telegram channel"
    txt(d, (540, 944), l3, fit(l3, 20, 900, "Medium"), (70, 80, 100), "mm")
    txt(d, (540, 984), "www.cbsemock.org.in", font(40), BLUE, "mm")
    txt(d, (540, 1024), "New papers every MON, WED & FRI — absolutely FREE!", font(21), ORANGE, "mm")

    date_slug = date.today().strftime("%Y-%m-%d")
    img_path  = str(OUTPUT_DIR / f"cover_{subject_key}_{date_slug}.jpg")
    img.convert("RGB").resize((1080, 1080), Image.LANCZOS).save(img_path, "JPEG", quality=92, optimize=True)
    print(f"🖼️   Cover image: {img_path}")
    return img_path


# ─── Git commit + push PDF ────────────────────────────────────────────────────

def _set_git_remote():
    """Set authenticated remote URL using GH_TOKEN if available."""
    gh_token = os.getenv("GH_TOKEN", "")
    repo = os.getenv("GITHUB_REPOSITORY", "compukidsdgp-creator/CBSE-PORTAL")
    if gh_token:
        url = f"https://x-access-token:{gh_token}@github.com/{repo}.git"
        subprocess.run(
            ["git", "-C", str(REPO_ROOT), "remote", "set-url", "origin", url],
            capture_output=True
        )


def commit_pdf(pdf_path: str, subject_key: str, dry_run: bool = False):
    """Add the PDF to git and push so it's live at cbsemock.org.in/pyq-papers/."""
    rel_path = Path(pdf_path).relative_to(REPO_ROOT)
    if dry_run:
        print(f"[DRY] Would commit: {rel_path}")
        return

    _set_git_remote()
    cmds = [
        ["git", "-C", str(REPO_ROOT), "config", "user.name", "social-post-bot"],
        ["git", "-C", str(REPO_ROOT), "config", "user.email", "bot@cbsemock.org.in"],
        ["git", "-C", str(REPO_ROOT), "add", str(rel_path),
         "pyq-papers/question_log.json"],
        ["git", "-C", str(REPO_ROOT), "commit", "-m",
         f"feat: add {subject_key} practice paper {date.today()} [skip ci]\n\n"
         f"Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>\n"
         f"Claude-Session: https://claude.ai/code/session_01TuPQgyyjEsjE236cZyznix"],
        ["git", "-C", str(REPO_ROOT), "push"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 and "nothing to commit" not in result.stdout:
            print(f"  git warning: {result.stderr.strip()}")
    print(f"✅  PDF committed & pushed: {rel_path}")


# ─── Telegram post ────────────────────────────────────────────────────────────

def post_telegram(pdf_path: str, img_path: str,
                  subject_key: str, pdf_url: str,
                  paper_date: str, dry_run: bool):
    token   = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    meta    = SUBJECT_META[subject_key]

    caption = (
        f"📄 *Class {meta['class']} {meta['label']} — Pre\\-Board Practice Paper*\n"
        f"📅 Date: {paper_date}\n\n"
        f"🎯 Get our FREE pre\\-board mock papers every Monday, Wednesday and Friday\\!\n"
        f"We are committed to your success\\.\n\n"
        f"📥 *Download today's paper here:*\n"
        f"{pdf_url}\n\n"
        f"💡 More free resources: www\\.cbsemock\\.org\\.in\n"
        f"📲 Join our Telegram: t\\.me/cbsemockportal\n"
        f"👍 Follow on Facebook: cbsemock\\.org\\.in\n"
        f"📸 Follow on Instagram: @cbsemock\n\n"
        f"\\#CBSE \\#PreBoard \\#Class{meta['class']} \\#{''.join(meta['label'].split())} "
        f"\\#FreeStudyMaterial \\#CBSEMock"
    )

    if dry_run:
        print(f"[DRY] Telegram: would post cover image + caption for {subject_key}")
        print(f"      PDF URL: {pdf_url}")
        return

    if not token or not chat_id:
        print("⚠️  TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set — skipping Telegram")
        return

    # Send cover image with caption
    with open(img_path, "rb") as f:
        resp = requests.post(
            f"https://api.telegram.org/bot{token}/sendPhoto",
            data={"chat_id": chat_id, "caption": caption, "parse_mode": "MarkdownV2"},
            files={"photo": f},
            timeout=30,
        )
    if resp.status_code == 200:
        print("✅  Telegram: cover image posted")
    else:
        print(f"❌  Telegram image: {resp.status_code} {resp.text[:200]}")

    # Also send the actual PDF as a document
    with open(pdf_path, "rb") as f:
        resp2 = requests.post(
            f"https://api.telegram.org/bot{token}/sendDocument",
            data={"chat_id": chat_id,
                  "caption": f"📎 Direct PDF download — Class {meta['class']} {meta['label']}",
                  "parse_mode": "MarkdownV2"},
            files={"document": f},
            timeout=30,
        )
    if resp2.status_code == 200:
        print("✅  Telegram: PDF document posted")
    else:
        print(f"❌  Telegram PDF: {resp2.status_code} {resp2.text[:200]}")


# ─── Facebook post ────────────────────────────────────────────────────────────

def post_facebook(img_path: str, subject_key: str,
                  pdf_url: str, paper_date: str, dry_run: bool):
    page_id = os.getenv("FB_PAGE_ID", "")
    token   = os.getenv("FB_PAGE_ACCESS_TOKEN", "")
    meta    = SUBJECT_META[subject_key]

    message = (
        f"📄 Class {meta['class']} {meta['label']} — Pre-Board Practice Paper | {paper_date}\n\n"
        f"🎯 Get our FREE pre-board mock papers every Monday, Wednesday & Friday!\n"
        f"We are committed to your success. 💪\n\n"
        f"📥 Download today's paper:\n{pdf_url}\n\n"
        f"🌐 More free resources: www.cbsemock.org.in\n"
        f"📲 Join our Telegram for every new paper: https://t.me/cbsemockportal\n"
        f"📸 Follow on Instagram: https://www.instagram.com/cbsemock/\n\n"
        f"#CBSE #PreBoard #Class{meta['class']} #{meta['label'].replace(' ','')} "
        f"#FreeStudyMaterial #CBSEExam #StudyWithUs #CBSEMock"
    )

    if dry_run:
        print(f"[DRY] Facebook: would post cover image with message for {subject_key}")
        return

    if not page_id or not token:
        print("⚠️  FB_PAGE_ID / FB_PAGE_ACCESS_TOKEN not set — skipping Facebook")
        return

    # Upload image to FB and post
    with open(img_path, "rb") as f:
        resp = requests.post(
            f"https://graph.facebook.com/v19.0/{page_id}/photos",
            data={"message": message, "access_token": token},
            files={"source": f},
            timeout=30,
        )
    if resp.status_code == 200:
        print("✅  Facebook: photo post successful")
    else:
        print(f"❌  Facebook: {resp.status_code} {resp.text[:300]}")


# ─── Instagram post ───────────────────────────────────────────────────────────

def post_instagram(img_path: str, subject_key: str,
                   pdf_url: str, paper_date: str, dry_run: bool, bio_url: str = None):
    ig_id  = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
    token  = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    meta   = SUBJECT_META[subject_key]

    # Instagram needs a public URL for the image — use GitHub raw URL
    repo = os.getenv("GITHUB_REPOSITORY", "compukidsdgp-creator/CBSE-PORTAL")
    branch = os.getenv("GITHUB_REF_NAME", "main")
    img_filename = Path(img_path).name
    ig_img_url = f"https://raw.githubusercontent.com/{repo}/{branch}/pyq-papers/{img_filename}"

    caption = (
        f"📄 Class {meta['class']} {meta['label']} Practice Paper — {paper_date}\n\n"
        f"🎯 FREE Pre-Board Mock Papers — every Mon, Wed & Fri!\n"
        f"We are committed to your success 💪\n\n"
        f"🔗 Bio link updated to today's paper — tap it to download!\n"
        f"🌐 www.cbsemock.org.in\n"
        f"📲 Telegram: t.me/cbsemockportal\n"
        f"👍 Facebook: facebook.com/cbsemock\n\n"
        f"#CBSE #PreBoard #Class{meta['class']} #{meta['label'].replace(' ','')} "
        f"#FreeStudyMaterial #CBSEExam #StudyWithUs #CBSEMock #BoardExam"
    )

    if dry_run:
        print(f"[DRY] Instagram: would update bio link to {bio_url or pdf_url} and post {img_filename}")
        return

    if not ig_id or not token:
        print("⚠️  INSTAGRAM_ACCOUNT_ID / INSTAGRAM_ACCESS_TOKEN not set — skipping Instagram")
        return

    # Step 0: update Instagram bio link to today's paper URL
    rb = requests.post(
        f"https://graph.facebook.com/v19.0/{ig_id}",
        data={"website": bio_url or pdf_url, "access_token": token},
        timeout=30,
    )
    if rb.status_code == 200:
        print(f"✅  Instagram: bio link updated → {pdf_url}")
    else:
        print(f"⚠️  Instagram bio update: {rb.status_code} {rb.text[:200]}")

    # Step 1: create media container
    r1 = requests.post(
        f"https://graph.facebook.com/v19.0/{ig_id}/media",
        data={"image_url": ig_img_url, "caption": caption, "access_token": token},
        timeout=30,
    )
    if r1.status_code != 200:
        print(f"❌  Instagram container: {r1.status_code} {r1.text[:300]}")
        return
    container_id = r1.json().get("id")

    # Step 2: publish
    r2 = requests.post(
        f"https://graph.facebook.com/v19.0/{ig_id}/media_publish",
        data={"creation_id": container_id, "access_token": token},
        timeout=30,
    )
    if r2.status_code == 200:
        print("✅  Instagram: post published")
    else:
        print(f"❌  Instagram publish: {r2.status_code} {r2.text[:300]}")


# ─── Main ─────────────────────────────────────────────────────────────────────

TODAY_PAGE_URL = "https://cbsemock.org.in/pyq-papers/today.html"

def _git_commit_push(paths, message, dry_run):
    if dry_run:
        print(f"[DRY] Would commit: {', '.join(str(p) for p in paths)}")
        return
    _set_git_remote()
    for cmd in (["config", "user.name", "social-post-bot"],
                ["config", "user.email", "bot@cbsemock.org.in"],
                ["add", *[str(p) for p in paths]],
                ["commit", "-m", message + " [skip ci]"],
                ["pull", "--rebase", "--autostash", "origin", os.getenv("GITHUB_REF_NAME", "main")],
                ["push", "origin", "HEAD:" + os.getenv("GITHUB_REF_NAME", "main")]):
        r = subprocess.run(["git", "-C", str(REPO_ROOT), *cmd], capture_output=True, text=True)
        if r.returncode != 0 and "nothing to commit" not in r.stdout:
            print(f"  git warning ({cmd[0]}): {r.stderr.strip()[:200]}")


def _write_today_page(papers, paper_date):
    """One page that links to both of today's papers (used for the Instagram bio link)."""
    rows = "".join(
        f'<a class="b" href="{u}">Class {SUBJECT_META[k]["class"]} {SUBJECT_META[k]["label"]}'
        f'<span>Download PDF</span></a>' for k, u in papers)
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Today's Free Mock Papers | CBSEMock</title>
<style>body{{margin:0;font-family:system-ui,Arial,sans-serif;background:#081430;color:#fff;text-align:center;padding:40px 16px}}
h1{{color:#ffd600;font-size:28px;margin:0 0 6px}}p{{color:#c8d7f0;margin:0 0 28px}}
.b{{display:block;max-width:420px;margin:14px auto;padding:18px 20px;border-radius:16px;background:#fff;color:#1565c0;
font-weight:700;font-size:20px;text-decoration:none}}.b span{{display:block;font-size:14px;color:#e65100;margin-top:4px}}
.f{{margin-top:30px;font-size:14px}}.f a{{color:#00d4ff}}</style></head><body>
<h1>Today's Free Mock Papers</h1><p>{paper_date}</p>{rows}
<p class="f"><a href="https://cbsemock.org.in">More free practice at cbsemock.org.in</a></p></body></html>
"""
    path = OUTPUT_DIR / "today.html"
    path.write_text(html, encoding="utf-8")
    return path


def publish(subject_key, pdf_path, pdf_url, paper_date, dry_run, bio_url=None):
    """Cover image + posts for one paper whose PDF is already built and pushed."""
    meta = SUBJECT_META[subject_key]
    img_path = build_cover_image(subject_key, paper_date, pdf_url)
    _git_commit_push([Path(img_path).relative_to(REPO_ROOT)],
                     f"feat: add cover image {Path(img_path).name}", dry_run)
    post_telegram(pdf_path, img_path, subject_key, pdf_url, paper_date, dry_run)
    post_facebook(img_path, subject_key, pdf_url, paper_date, dry_run)
    if not dry_run:
        import time
        print("⏳  Waiting 20s for GitHub raw URL to be available for Instagram...")
        time.sleep(20)
    post_instagram(img_path, subject_key, pdf_url, paper_date, dry_run, bio_url=bio_url)
    print(f"🎉  Done: Class {meta['class']} {meta['label']}  →  {pdf_url}")


def run_today(dry_run: bool):
    """
    Post the papers planned for today in question-bank/calendar.json:
    one Class 10 paper and one Class 12 paper, every Monday, Wednesday and Friday.
    Safe to run on any day and more than once: it skips days with nothing planned
    and papers that are already posted.
    """
    import mock_bank
    from mock_paper_pdf import build_mock_pdf

    d = mock_bank.today_ist()
    paper_date = d.strftime("%d %B %Y")
    entry = mock_bank.entry_for(d)
    if not entry:
        if d.weekday() in mock_bank.POST_WEEKDAYS:
            print(f"::error::No mock paper is planned for {paper_date}. The reviewed question stock has run out. "
                  f"Add questions and run: python3 mock_bank.py plan")
            sys.exit(1)
        print(f"[SKIP] {paper_date} is not a paper day (papers go out Mon/Wed/Fri).")
        return

    todo = [(cls, e) for cls, e in entry.items() if not e.get("posted")]
    if not todo:
        print(f"[SKIP] Today's papers ({paper_date}) are already posted.")
        return

    # 1) Build the PDFs and the page that links to both, then push them together
    built, paths = [], []
    for cls, e in todo:
        sk = e["subject_key"]
        meta, _ = mock_bank.paper_sections(sk, e["question_ids"], raw=True)
        pdf_path = OUTPUT_DIR / f"{sk}_{d.isoformat()}.pdf"
        build_mock_pdf(meta, str(pdf_path), paper_date, paper_id=e["paper_id"])
        print(f"📄  {e['paper_id']}: {pdf_path.name}")
        built.append((cls, sk, pdf_path, f"https://cbsemock.org.in/pyq-papers/{pdf_path.name}"))
        paths.append(pdf_path.relative_to(REPO_ROOT))
    page = _write_today_page([(sk, url) for _, sk, _, url in built], paper_date)
    paths.append(page.relative_to(REPO_ROOT))
    _git_commit_push(paths, f"feat: mock papers for {d.isoformat()}", dry_run)

    # 2) Post each paper, then record it as posted so it is never used again
    for n, (cls, sk, pdf_path, pdf_url) in enumerate(built):
        if n and not dry_run:
            import time; time.sleep(30)
        publish(sk, str(pdf_path), pdf_url, paper_date, dry_run, bio_url=TODAY_PAGE_URL)
        if not dry_run:
            mock_bank.mark_posted(d, cls)
            saved = ["question-bank/calendar.json"]
            try:                                    # add the paper to the portal's Free Mock Papers section
                import mock_papers_page
                saved.append(str(mock_papers_page.build().relative_to(REPO_ROOT)))
            except Exception as exc:
                print(f"::warning::Could not rebuild the Free Mock Papers page: {exc}")
            _git_commit_push(saved, f"chore: mark {sk} {d.isoformat()} as posted", dry_run)

    left = mock_bank.unposted_days() if not dry_run else mock_bank.unposted_days() - 1
    if left < 3:
        print(f"::warning::Only {left} more paper day(s) are planned. Add questions and run: python3 mock_bank.py plan")
    else:
        print(f"ℹ️  Paper days still planned: {left}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject",
                        choices=list(SUBJECT_META.keys()),
                        default=None,
                        help="OLD behaviour: one paper from the small legacy bank (questions repeat)")
    parser.add_argument("--today", action="store_true",
                        help="post today's planned Class 10 + Class 12 papers (no repeats)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.today or not args.subject:
        run_today(args.dry_run)
        return

    subject_key = args.subject
    dry_run     = args.dry_run
    meta        = SUBJECT_META[subject_key]
    paper_date  = date.today().strftime("%d %B %Y")
    date_slug   = date.today().strftime("%Y-%m-%d")

    print(f"\n🚀  CBSE Mock PYQ Post — Class {meta['class']} {meta['label']}")
    print(f"    Date: {paper_date}  |  Dry run: {dry_run}\n")

    # 1) Generate PDF
    from pyq_generator import build_pdf, SUBJECT_CHOICES
    pdf_filename = f"{subject_key}_{date_slug}.pdf"
    pdf_path = str(OUTPUT_DIR / pdf_filename)
    build_pdf(SUBJECT_CHOICES[subject_key], pdf_path, paper_date)

    # 2) Build public URL
    repo   = os.getenv("GITHUB_REPOSITORY", "compukidsdgp-creator/CBSE-PORTAL")
    branch = os.getenv("GITHUB_REF_NAME", "main")
    pdf_url = f"https://cbsemock.org.in/pyq-papers/{pdf_filename}"

    # 3) Commit + push PDF
    # Also commit the cover image after we create it
    commit_pdf(pdf_path, subject_key, dry_run)

    # 4) Build cover image
    img_path = build_cover_image(subject_key, paper_date, pdf_url)

    # Commit the cover image too
    img_rel = Path(img_path).relative_to(REPO_ROOT)
    if not dry_run:
        subprocess.run(
            ["git", "-C", str(REPO_ROOT), "add", str(img_rel)],
            capture_output=True
        )
        subprocess.run(
            ["git", "-C", str(REPO_ROOT), "commit", "-m",
             f"feat: add cover image {img_rel.name} [skip ci]\n\n"
             f"Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>\n"
             f"Claude-Session: https://claude.ai/code/session_01TuPQgyyjEsjE236cZyznix"],
            capture_output=True
        )
        result = subprocess.run(["git", "-C", str(REPO_ROOT), "push"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  git warning (cover): {result.stderr.strip()}")

    # 5) Post to all platforms
    post_telegram(pdf_path, img_path, subject_key, pdf_url, paper_date, dry_run)
    post_facebook(img_path, subject_key, pdf_url, paper_date, dry_run)

    # Wait for GitHub to serve the raw cover image URL before Instagram fetches it
    if not dry_run:
        import time
        print("⏳  Waiting 20s for GitHub raw URL to be available for Instagram...")
        time.sleep(20)
    post_instagram(img_path, subject_key, pdf_url, paper_date, dry_run)

    print(f"\n🎉  All done for Class {meta['class']} {meta['label']}!")
    print(f"    PDF URL: {pdf_url}")


if __name__ == "__main__":
    main()
