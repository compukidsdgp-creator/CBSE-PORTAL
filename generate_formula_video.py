#!/usr/bin/env python3
"""
generate_formula_video.py
─────────────────────────
Generates a 6-8 sec animated MP4 reel for Instagram/Facebook.
Animation: title fades in → formula zooms in with glow → meaning slides up → tip pops → branding.

Uses: Pillow (frames) + FFmpeg (encode to MP4)
Output: formula-posts/videos/

Usage:
  python3 generate_formula_video.py --formula-id newton2
  python3 generate_formula_video.py --all
"""

import argparse
import os
import shutil
import subprocess
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR   = Path(__file__).parent / "formula-posts" / "videos"
FRAME_DIR = Path(__file__).parent / "formula-posts" / "_frames"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SIZE = (1080, 1920)   # Vertical / Reel format
FPS  = 30

PALETTES = {
    "physics":   {"bg": "#0d1117", "accent": "#58a6ff", "glow": "#1f6feb",
                  "tag_bg": "#1f6feb", "tag_fg": "#ffffff"},
    "chemistry": {"bg": "#0d1117", "accent": "#3fb950", "glow": "#238636",
                  "tag_bg": "#238636", "tag_fg": "#ffffff"},
    "maths":     {"bg": "#0d1117", "accent": "#f78166", "glow": "#da3633",
                  "tag_bg": "#da3633", "tag_fg": "#ffffff"},
    "biology":   {"bg": "#0d1117", "accent": "#56d364", "glow": "#2ea043",
                  "tag_bg": "#2ea043", "tag_fg": "#ffffff"},
}

FORMULAS = {
    "newton2": {
        "subject": "physics", "class": "Class 11 & 12",
        "chapter": "Laws of Motion",
        "title": "Newton's 2nd Law",
        "formula": "F = ma",
        "meaning": "Force = Mass × Acceleration",
        "tip": "Double velocity → 4× Kinetic Energy!",
        "hashtags": "#Physics #CBSE #Newton #BoardExam2027",
    },
    "faraday": {
        "subject": "physics", "class": "Class 12",
        "chapter": "Electromagnetic Induction",
        "title": "Faraday's Law",
        "formula": "ε = −dΦ/dt",
        "meaning": "EMF = −Rate of change of flux",
        "tip": "Negative sign = Lenz's Law in action!",
        "hashtags": "#Physics #CBSE #EMI #BoardExam2027",
    },
    "ohms_law": {
        "subject": "physics", "class": "Class 10 & 12",
        "chapter": "Current Electricity",
        "title": "Ohm's Law",
        "formula": "V = IR",
        "meaning": "Voltage = Current × Resistance",
        "tip": "V–I graph straight line = Ohmic conductor",
        "hashtags": "#Physics #CBSE #OhmsLaw #BoardExam2027",
    },
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def try_font(size, bold=False):
    candidates = [
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def lerp(a, b, t):
    return a + (b - a) * t


def ease_out(t):
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    return t * t * (3 - 2 * t)


def draw_grid(draw, W, H, bg):
    grid_col = tuple(min(255, c + 18) for c in bg)
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=grid_col, width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=grid_col, width=1)


def draw_rounded_rect(draw, xy, radius, fill):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    for corner in [(x1, y1), (x2 - 2*radius, y1),
                   (x1, y2 - 2*radius), (x2 - 2*radius, y2 - 2*radius)]:
        draw.ellipse([corner[0], corner[1],
                      corner[0] + 2*radius, corner[1] + 2*radius], fill=fill)


def render_frame(data, pal, frame_idx, total_frames):
    W, H = SIZE
    bg  = hex_to_rgb(pal["bg"])
    acc = hex_to_rgb(pal["accent"])
    glow = hex_to_rgb(pal["glow"])

    img  = Image.new("RGB", SIZE, bg)
    draw = ImageDraw.Draw(img)

    t_total = frame_idx / total_frames   # 0.0 → 1.0 overall progress

    # Phase timings (fraction of total)
    # 0.00–0.15 : subject tag + chapter fade in
    # 0.15–0.35 : title slides in
    # 0.35–0.65 : formula box zoom + glow pulse
    # 0.65–0.80 : meaning + tip slide up
    # 0.80–1.00 : branding + hashtags

    draw_grid(draw, W, H, bg)

    # ── Accent bar ────────────────────────────────────────────────────────────
    bar_w = int(W * min(1.0, t_total / 0.1))
    draw.rectangle([0, 0, bar_w, 10], fill=acc)

    # ── Subject tag ───────────────────────────────────────────────────────────
    tag_alpha = min(1.0, t_total / 0.15)
    if tag_alpha > 0:
        tag_text = f"  {data['subject'].upper()}  ·  {data['class']}  "
        tag_font = try_font(36, bold=True)
        tb = draw.textbbox((0, 0), tag_text, font=tag_font)
        tw = tb[2] - tb[0]
        tag_y = int(lerp(H * 0.05 - 60, H * 0.05, ease_out(tag_alpha)))
        draw_rounded_rect(draw, [80, tag_y, 80 + tw + 24, tag_y + 56], 24,
                          hex_to_rgb(pal["tag_bg"]))
        draw.text((90, tag_y + 10), tag_text, font=tag_font,
                  fill=hex_to_rgb(pal["tag_fg"]))

        chap_font = try_font(30)
        chap_y = tag_y + 72
        draw.text((80, chap_y), data["chapter"], font=chap_font,
                  fill=tuple(min(255, c + 100) for c in bg))

    # ── Title ─────────────────────────────────────────────────────────────────
    title_alpha = max(0.0, min(1.0, (t_total - 0.15) / 0.20))
    if title_alpha > 0:
        title_font = try_font(80, bold=True)
        title_col = tuple(int(lerp(0, 240, title_alpha)) for _ in range(3))
        slide_x = int(lerp(-200, 80, ease_out(title_alpha)))
        draw.text((slide_x, int(H * 0.18)), data["title"],
                  font=title_font, fill=title_col)

    # ── Formula box ───────────────────────────────────────────────────────────
    formula_alpha = max(0.0, min(1.0, (t_total - 0.35) / 0.30))
    if formula_alpha > 0:
        # Glow pulse
        pulse = 0.5 + 0.5 * abs((t_total - 0.5) * 2 % 2 - 1)
        box_cx, box_cy = W // 2, int(H * 0.46)
        box_w = int(lerp(100, W - 120, ease_out(formula_alpha)))
        box_h = int(lerp(60, 280, ease_out(formula_alpha)))
        bx1 = box_cx - box_w // 2
        bx2 = box_cx + box_w // 2
        by1 = box_cy - box_h // 2
        by2 = box_cy + box_h // 2

        # Glow layers
        for i in range(6, 0, -1):
            g = tuple(max(0, c - i * 12 + int(pulse * 20)) for c in glow)
            draw_rounded_rect(draw,
                              [bx1 - i*5, by1 - i*5, bx2 + i*5, by2 + i*5],
                              28, g)
        inner_bg = tuple(min(255, c + 22) for c in bg)
        draw_rounded_rect(draw, [bx1, by1, bx2, by2], 24, inner_bg)

        # Formula text
        f_size = int(lerp(20, 130, ease_out(formula_alpha)))
        formula_font = try_font(max(20, f_size), bold=True)
        fb = draw.textbbox((0, 0), data["formula"], font=formula_font)
        fw = fb[2] - fb[0]
        fh = fb[3] - fb[1]
        fx = (W - fw) // 2
        fy = box_cy - fh // 2
        f_col = tuple(int(lerp(100, c, formula_alpha)) for c in acc)
        draw.text((fx + 4, fy + 4), data["formula"],
                  font=formula_font, fill=(0, 0, 0))
        draw.text((fx, fy), data["formula"],
                  font=formula_font, fill=f_col)

    # ── Meaning + tip ─────────────────────────────────────────────────────────
    info_alpha = max(0.0, min(1.0, (t_total - 0.65) / 0.15))
    if info_alpha > 0:
        mean_font = try_font(38)
        mean_col = tuple(int(lerp(0, 200, info_alpha)) for _ in range(3))
        slide_y = int(lerp(H * 0.68 + 60, H * 0.68, ease_out(info_alpha)))
        mb = draw.textbbox((0, 0), data["meaning"], font=mean_font)
        mw = mb[2] - mb[0]
        draw.text(((W - mw) // 2, slide_y), data["meaning"],
                  font=mean_font, fill=mean_col)

        tip_alpha = max(0.0, min(1.0, (t_total - 0.72) / 0.10))
        if tip_alpha > 0:
            tip_font = try_font(32)
            tip_col = (220, 200, 100)
            tip_col_a = tuple(int(c * tip_alpha) for c in tip_col)
            tip_slide = int(lerp(H * 0.76 + 50, H * 0.76, ease_out(tip_alpha)))
            wrapped = textwrap.fill("💡 " + data["tip"], width=36)
            draw.text((80, tip_slide), wrapped, font=tip_font, fill=tip_col_a)

    # ── Branding ──────────────────────────────────────────────────────────────
    brand_alpha = max(0.0, min(1.0, (t_total - 0.80) / 0.15))
    if brand_alpha > 0:
        draw.rectangle([0, H - 160, W, H],
                       fill=tuple(min(255, c + 10) for c in bg))
        draw.rectangle([0, H - 162, W, H - 160], fill=acc)

        brand_font = try_font(44, bold=True)
        b_col = tuple(int(c * brand_alpha) for c in acc)
        draw.text((80, H - 130), "cbsemock.org.in", font=brand_font, fill=b_col)

        sub_font = try_font(28)
        s_col = tuple(int(150 * brand_alpha) for _ in range(3))
        draw.text((80, H - 78),
                  "Class X & XII Board Prep Hub", font=sub_font, fill=s_col)

        hash_alpha = max(0.0, min(1.0, (t_total - 0.88) / 0.10))
        if hash_alpha > 0:
            hash_font = try_font(26)
            hb = draw.textbbox((0, 0), data["hashtags"], font=hash_font)
            hw = hb[2] - hb[0]
            h_col = tuple(int(lerp(0, min(255, c + 60), hash_alpha))
                          for c in glow)
            draw.text(((W - hw) // 2, H - 185),
                      data["hashtags"], font=hash_font, fill=h_col)

    return img


def generate_video(formula_id: str) -> Path:
    data  = FORMULAS[formula_id]
    pal   = PALETTES[data["subject"]]
    duration = 7   # seconds
    total_frames = FPS * duration

    # Clean frame dir
    if FRAME_DIR.exists():
        shutil.rmtree(FRAME_DIR)
    FRAME_DIR.mkdir(parents=True)

    print(f"[INFO] Rendering {total_frames} frames for {formula_id}...")
    for i in range(total_frames):
        frame = render_frame(data, pal, i, total_frames)
        frame.save(FRAME_DIR / f"frame_{i:04d}.png")
        if i % 30 == 0:
            print(f"  frame {i}/{total_frames}")

    out_path = OUT_DIR / f"{formula_id}.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAME_DIR / "frame_%04d.png"),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(out_path)
    ]
    print(f"[INFO] Encoding MP4...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] FFmpeg: {result.stderr[-500:]}")
    else:
        print(f"[OK] Saved: {out_path}")

    # Cleanup frames
    shutil.rmtree(FRAME_DIR)
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--formula-id")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.all:
        for fid in FORMULAS:
            generate_video(fid)
    elif args.formula_id:
        generate_video(args.formula_id)
    else:
        generate_video("newton2")


if __name__ == "__main__":
    main()
