#!/usr/bin/env python3
"""
generate_formula_image.py
─────────────────────────
Generates a branded formula reminder image (1080×1080) for Instagram/Facebook.
Saves to formula-posts/images/

Usage:
  python3 generate_formula_image.py --formula-id newton2
  python3 generate_formula_image.py --all
"""

import argparse
import os
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).parent / "formula-posts" / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SIZE = (1080, 1080)

# ── Colour palettes per subject ───────────────────────────────────────────────
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

# ── Formula data ───────────────────────────────────────────────────────────────
FORMULAS = {
    # ── Physics ───────────────────────────────────────────────────────────────
    "newton2": {
        "subject": "physics", "class": "Class 11 & 12",
        "chapter": "Laws of Motion",
        "title": "Newton's Second Law",
        "formula": "F  =  ma",
        "meaning": "Net Force  =  Mass × Acceleration",
        "units": "F in Newton (N)  |  m in kg  |  a in m/s²",
        "tip": "💡 If mass doubles, force must double to keep same acceleration.",
        "hashtags": "#Physics #CBSE #Newton #ClassXI #BoardExam2027",
    },
    "kinetic_energy": {
        "subject": "physics", "class": "Class 11",
        "chapter": "Work, Energy & Power",
        "title": "Kinetic Energy",
        "formula": "KE  =  ½ mv²",
        "meaning": "Energy of motion depends on mass and velocity squared",
        "units": "KE in Joule (J)  |  m in kg  |  v in m/s",
        "tip": "💡 Double the velocity → KE becomes 4× (not 2×).",
        "hashtags": "#Physics #CBSE #Energy #ClassXI #BoardExam2027",
    },
    "faraday": {
        "subject": "physics", "class": "Class 12",
        "chapter": "Electromagnetic Induction",
        "title": "Faraday's Law of Induction",
        "formula": "ε  =  −dΦ/dt",
        "meaning": "Induced EMF = −Rate of change of magnetic flux",
        "units": "ε in Volt (V)  |  Φ in Weber (Wb)  |  t in seconds",
        "tip": "💡 Negative sign = Lenz's Law (opposes the cause).",
        "hashtags": "#Physics #CBSE #EMI #ClassXII #BoardExam2027",
    },
    "ohms_law": {
        "subject": "physics", "class": "Class 10 & 12",
        "chapter": "Current Electricity",
        "title": "Ohm's Law",
        "formula": "V  =  IR",
        "meaning": "Voltage = Current × Resistance",
        "units": "V in Volt  |  I in Ampere (A)  |  R in Ohm (Ω)",
        "tip": "💡 V–I graph is a straight line for ohmic conductors.",
        "hashtags": "#Physics #CBSE #OhmsLaw #ClassX #BoardExam2027",
    },
}


def hex_to_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def draw_rounded_rect(draw, xy, radius, fill):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill)
    draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill)
    draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill)
    draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill)


def try_font(size, bold=False):
    """Try to load a system font, fall back to default."""
    candidates = [
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'‑Bold' if bold else ''}.ttf",
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


def generate_image(formula_id: str) -> Path:
    data = FORMULAS[formula_id]
    pal  = PALETTES[data["subject"]]
    bg   = hex_to_rgb(pal["bg"])
    acc  = hex_to_rgb(pal["accent"])
    glow = hex_to_rgb(pal["glow"])

    img  = Image.new("RGB", SIZE, bg)
    draw = ImageDraw.Draw(img)

    W, H = SIZE

    # ── Background grid lines (subtle) ────────────────────────────────────────
    grid_col = tuple(min(255, c + 15) for c in bg)
    for x in range(0, W, 60):
        draw.line([(x, 0), (x, H)], fill=grid_col, width=1)
    for y in range(0, H, 60):
        draw.line([(0, y), (W, y)], fill=grid_col, width=1)

    # ── Accent top bar ─────────────────────────────────────────────────────────
    draw.rectangle([0, 0, W, 8], fill=acc)

    # ── Subject tag pill ──────────────────────────────────────────────────────
    tag_text = f"  {data['subject'].upper()}  ·  {data['class']}  "
    tag_font = try_font(28, bold=True)
    tb = draw.textbbox((0, 0), tag_text, font=tag_font)
    tw = tb[2] - tb[0]
    draw_rounded_rect(draw, [60, 50, 60 + tw + 20, 100], 20,
                      hex_to_rgb(pal["tag_bg"]))
    draw.text((70, 58), tag_text, font=tag_font,
              fill=hex_to_rgb(pal["tag_fg"]))

    # ── Chapter ───────────────────────────────────────────────────────────────
    chap_font = try_font(26)
    draw.text((60, 118), data["chapter"], font=chap_font,
              fill=tuple(min(255, c + 100) for c in bg))

    # ── Title ─────────────────────────────────────────────────────────────────
    title_font = try_font(52, bold=True)
    draw.text((60, 160), data["title"], font=title_font, fill=(240, 240, 240))

    # ── Divider ───────────────────────────────────────────────────────────────
    draw.rectangle([60, 232, 60 + 80, 238], fill=acc)

    # ── Formula box ───────────────────────────────────────────────────────────
    box_y1, box_y2 = 265, 450
    # Glow effect — draw several semi-transparent rectangles
    for i in range(5, 0, -1):
        alpha_col = tuple(max(0, c - i * 15) for c in glow)
        draw_rounded_rect(draw, [60 - i*4, box_y1 - i*4,
                                  W - 60 + i*4, box_y2 + i*4],
                          24, alpha_col)
    draw_rounded_rect(draw, [60, box_y1, W - 60, box_y2], 20,
                      tuple(min(255, c + 25) for c in bg))

    formula_font = try_font(96, bold=True)
    fb = draw.textbbox((0, 0), data["formula"], font=formula_font)
    fw = fb[2] - fb[0]
    fh = fb[3] - fb[1]
    fx = (W - fw) // 2
    fy = box_y1 + ((box_y2 - box_y1) - fh) // 2 - 10
    # Shadow
    draw.text((fx + 3, fy + 3), data["formula"], font=formula_font,
              fill=(0, 0, 0))
    draw.text((fx, fy), data["formula"], font=formula_font, fill=acc)

    # ── Meaning ───────────────────────────────────────────────────────────────
    mean_font = try_font(32)
    mb = draw.textbbox((0, 0), data["meaning"], font=mean_font)
    mw = mb[2] - mb[0]
    draw.text(((W - mw) // 2, 470), data["meaning"],
              font=mean_font, fill=(200, 200, 200))

    # ── Units ─────────────────────────────────────────────────────────────────
    unit_font = try_font(26)
    ub = draw.textbbox((0, 0), data["units"], font=unit_font)
    uw = ub[2] - ub[0]
    draw.text(((W - uw) // 2, 520), data["units"],
              font=unit_font, fill=(150, 150, 150))

    # ── Divider ───────────────────────────────────────────────────────────────
    draw.rectangle([60, 575, W - 60, 577], fill=grid_col)

    # ── Tip ───────────────────────────────────────────────────────────────────
    tip_font = try_font(30)
    wrapped = textwrap.fill(data["tip"], width=48)
    draw.text((60, 595), wrapped, font=tip_font, fill=(220, 200, 100))

    # ── Bottom: branding ──────────────────────────────────────────────────────
    draw.rectangle([0, H - 110, W, H], fill=tuple(min(255, c + 10) for c in bg))
    draw.rectangle([0, H - 112, W, H - 110], fill=acc)

    brand_font = try_font(34, bold=True)
    draw.text((60, H - 85), "cbsemock.org.in",
              font=brand_font, fill=acc)

    sub_font = try_font(24)
    draw.text((60, H - 48), "Class X & XII Board Exam Preparation Hub",
              font=sub_font, fill=(150, 150, 150))

    # ── Hashtags ──────────────────────────────────────────────────────────────
    hash_font = try_font(22)
    hb = draw.textbbox((0, 0), data["hashtags"], font=hash_font)
    hw = hb[2] - hb[0]
    draw.text(((W - hw) // 2, H - 155), data["hashtags"],
              font=hash_font, fill=tuple(min(255, c + 60) for c in glow))

    out_path = OUT_DIR / f"{formula_id}.png"
    img.save(out_path, "PNG", quality=95)
    print(f"[OK] Saved: {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--formula-id", help="Specific formula ID")
    parser.add_argument("--all", action="store_true", help="Generate all")
    args = parser.parse_args()

    if args.all:
        for fid in FORMULAS:
            generate_image(fid)
    elif args.formula_id:
        generate_image(args.formula_id)
    else:
        # Default: generate all
        for fid in FORMULAS:
            generate_image(fid)


if __name__ == "__main__":
    main()
