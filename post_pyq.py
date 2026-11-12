#!/usr/bin/env python3
"""
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

def build_cover_image(subject_key: str, paper_date: str, pdf_url: str) -> str:
    """Create a 1080×1080 branded cover image. Returns path to PNG."""
    meta    = SUBJECT_META[subject_key]
    cls     = meta["class"]
    subject = meta["label"]

    W, H = 1080, 1080
    img  = Image.new("RGB", (W, H), color=BRAND_BLUE)
    draw = ImageDraw.Draw(img)

    # ── Background gradient effect using rectangles ──────────────────────────
    for i in range(H):
        t = i / H
        r = int(BRAND_BLUE[0] * (1 - t) + 10 * t)
        g = int(BRAND_BLUE[1] * (1 - t) + 20 * t)
        b = int(BRAND_BLUE[2] * (1 - t) + 60 * t)
        draw.line([(0, i), (W, i)], fill=(r, g, b))

    # ── Decorative top stripe ────────────────────────────────────────────────
    draw.rectangle([0, 0, W, 12], fill=BRAND_ORANGE)

    # ── Top-right accent circle ──────────────────────────────────────────────
    draw.ellipse([W - 320, -200, W + 100, 220], fill=(255, 255, 255, 20))
    draw.ellipse([W - 220, -120, W + 60, 160], fill=(230, 81, 0, 40))

    # ── Helper: load font with fallback ──────────────────────────────────────
    def font(size, bold=False):
        for name in (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ):
            if Path(name).exists():
                try:
                    return ImageFont.truetype(name, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    # ── CBSEMOCK logo text ────────────────────────────────────────────────────
    logo_fnt = font(42, bold=True)
    draw.text((54, 30), "CBSE", font=logo_fnt, fill=WHITE)
    draw.text((54 + 120, 30), "MOCK", font=logo_fnt, fill=GOLD)
    draw.text((54 + 240, 30), ".ORG.IN", font=font(28), fill=(200, 230, 255))

    # ── Orange label badge ───────────────────────────────────────────────────
    badge_y = 110
    draw.rounded_rectangle([44, badge_y, 460, badge_y + 54], radius=8, fill=BRAND_ORANGE)
    badge_text = "FREE PRE-BOARD PRACTICE PAPER"
    draw.text((52, badge_y + 10), badge_text, font=font(20, bold=True), fill=WHITE)

    # ── Class chip ───────────────────────────────────────────────────────────
    draw.rounded_rectangle([44, 185, 170, 230], radius=6, fill=GOLD)
    draw.text((52, 192), f"CLASS {cls}", font=font(22, bold=True), fill=(50, 30, 0))

    # ── Subject name ─────────────────────────────────────────────────────────
    draw.text((44, 250), subject.upper(), font=font(78, bold=True), fill=WHITE)

    # ── Horizontal rule ───────────────────────────────────────────────────────
    draw.rectangle([44, 355, W - 44, 360], fill=BRAND_ORANGE)

    # ── Date ─────────────────────────────────────────────────────────────────
    draw.text((44, 374), f"★  {paper_date}", font=font(26), fill=(200, 230, 255))

    # ── Main headline ─────────────────────────────────────────────────────────
    headline_lines = [
        "Get our Free",
        "Pre-Board Practice Paper",
        "Every Day for Your Practice!",
    ]
    y = 440
    for i, line in enumerate(headline_lines):
        fnt = font(50 if i == 0 else (54 if i == 1 else 42), bold=True)
        col = WHITE if i < 2 else GOLD
        draw.text((54, y), line, font=fnt, fill=col)
        y += 68

    # ── Commitment line ───────────────────────────────────────────────────────
    draw.text((54, y + 10),
              "We are committed to your success.",
              font=font(28), fill=(200, 230, 255))

    # ── CTA box ───────────────────────────────────────────────────────────────
    cta_y = H - 230
    draw.rounded_rectangle([44, cta_y, W - 44, cta_y + 160],
                            radius=14, fill=(255, 255, 255, 240))
    draw.rounded_rectangle([44, cta_y, W - 44, cta_y + 160],
                            radius=14, outline=BRAND_ORANGE, width=3)

    cta_fnt_sm = font(22, bold=False)
    cta_fnt_lg = font(30, bold=True)
    draw.text((W // 2, cta_y + 22), "▼  Get today's paper link below  ▼",
              font=cta_fnt_sm, fill=DARK_GREY, anchor="mm")
    draw.text((W // 2, cta_y + 72), "CBSEMOCK.org.in",
              font=cta_fnt_lg, fill=BRAND_BLUE, anchor="mm")
    draw.text((W // 2, cta_y + 110),
              "Also available on our Telegram channel",
              font=cta_fnt_sm, fill=DARK_GREY, anchor="mm")
    draw.text((W // 2, cta_y + 140),
              "New paper EVERY DAY — absolutely FREE!",
              font=font(22, bold=True), fill=BRAND_ORANGE, anchor="mm")

    # ── Bottom rule ───────────────────────────────────────────────────────────
    draw.rectangle([0, H - 12, W, H], fill=BRAND_ORANGE)

    # ── Save ──────────────────────────────────────────────────────────────────
    date_slug = date.today().strftime("%Y-%m-%d")
    img_path  = str(OUTPUT_DIR / f"cover_{subject_key}_{date_slug}.png")
    img.save(img_path, "PNG", optimize=True)
    print(f"🖼️   Cover image: {img_path}")
    return img_path


# ─── Git commit + push PDF ────────────────────────────────────────────────────

def commit_pdf(pdf_path: str, subject_key: str, dry_run: bool = False):
    """Add the PDF to git and push so it's live at cbsemock.org.in/pyq-papers/."""
    rel_path = Path(pdf_path).relative_to(REPO_ROOT)
    if dry_run:
        print(f"[DRY] Would commit: {rel_path}")
        return

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
        f"📄 *Class {meta['class']} {meta['label']} — Pre-Board Practice Paper*\n"
        f"📅 Date: {paper_date}\n\n"
        f"🎯 Get our FREE pre-board practice paper every day for your practice\\!\n"
        f"We are committed to your success\\.\n\n"
        f"📥 *Download today's paper here:*\n"
        f"{pdf_url}\n\n"
        f"💡 More free resources: www\\.cbsemock\\.org\\.in\n"
        f"📲 Join our Telegram: https://t\\.me/cbsemockportal\n"
        f"👍 Follow on Facebook: https://www\\.facebook\\.com/profile\\.php?id=61596243964780\n"
        f"📸 Follow on Instagram: https://www\\.instagram\\.com/cbsemock/\n\n"
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
        f"🎯 Get our FREE pre-board practice paper EVERY DAY for your practice!\n"
        f"We are committed to your success. 💪\n\n"
        f"📥 Download today's paper:\n{pdf_url}\n\n"
        f"🌐 More free resources: www.cbsemock.org.in\n"
        f"📲 Join our Telegram for daily papers: https://t.me/cbsemockportal\n"
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
                   pdf_url: str, paper_date: str, dry_run: bool):
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
        f"🎯 FREE Pre-Board Practice Paper — Every Day!\n"
        f"We are committed to your success 💪\n\n"
        f"📥 Link in bio to download today's paper!\n"
        f"🌐 www.cbsemock.org.in\n"
        f"📲 Telegram: t.me/cbsemockportal\n"
        f"👍 Facebook: facebook.com/profile.php?id=61596243964780\n\n"
        f"#CBSE #PreBoard #Class{meta['class']} #{meta['label'].replace(' ','')} "
        f"#FreeStudyMaterial #CBSEExam #StudyWithUs #CBSEMock #BoardExam"
    )

    if dry_run:
        print(f"[DRY] Instagram: would post {img_filename} (IG URL: {ig_img_url})")
        return

    if not ig_id or not token:
        print("⚠️  INSTAGRAM_ACCOUNT_ID / INSTAGRAM_ACCESS_TOKEN not set — skipping Instagram")
        return

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject",
                        choices=list(SUBJECT_META.keys()),
                        default="science10")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

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
        subprocess.run(["git", "-C", str(REPO_ROOT), "push"], capture_output=True)

    # 5) Post to all platforms
    post_telegram(pdf_path, img_path, subject_key, pdf_url, paper_date, dry_run)
    post_facebook(img_path, subject_key, pdf_url, paper_date, dry_run)
    post_instagram(img_path, subject_key, pdf_url, paper_date, dry_run)

    print(f"\n🎉  All done for Class {meta['class']} {meta['label']}!")
    print(f"    PDF URL: {pdf_url}")


if __name__ == "__main__":
    main()
