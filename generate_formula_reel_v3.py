#!/usr/bin/env python3
"""
generate_formula_reel_v3.py
───────────────────────────
Formula Flash reels — "one formula per screen" style (V5 design).

  * 1080 x 1920, 30 fps
  * 2.5 s hook intro  +  5 s per formula card  +  5 s save/share outro
  * At most 4 formulas per reel. Topics with more rows are split into
    balanced parts (5 rows -> Part 1 with 3, Part 2 with 2).
  * Works for every topic in formula_topics_master.TOPICS and every diagram in
    diagram_library.DIAGRAMS (all subjects).

Usage:
  python3 generate_formula_reel_v3.py --topic chemical_kinetics
  python3 generate_formula_reel_v3.py --topic genetics --part 1
  python3 generate_formula_reel_v3.py --all
  python3 generate_formula_reel_v3.py --topic optics --out-dir /some/dir

The older generate_formula_reel_v2.py is untouched; this script does not write
into formula-posts/videos/queue/ unless --out-dir points there.
"""
import argparse
import math
import os
import shutil
import subprocess
import sys
import tempfile
from functools import lru_cache
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.image
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, Circle

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from formula_topics_master import TOPICS          # noqa: E402
from diagram_library import DIAGRAMS              # noqa: E402

# ── Paths ────────────────────────────────────────────────────────────────────
OUT_DIR   = ROOT / "formula-posts" / "videos"
LOGO_PATH = ROOT / "formula-posts" / "_cbsemock_logo_dark.png"
BG_MUSIC  = ROOT / "formula-posts" / "bg_music.mp3"

# ── Canvas / timing ──────────────────────────────────────────────────────────
W, H, DPI, FPS = 1080, 1920, 100, 30
INTRO_SEC, CARD_SEC, OUTRO_SEC = 2.5, 5.0, 5.0
MAX_PER_REEL = 4

# ── Palette ──────────────────────────────────────────────────────────────────
BG         = "#050e1f"
CARD_BG    = "#0a1a30"
BAR_BG     = "#020c1a"
BRAND_CYAN = "#00d4ff"
GOLD       = "#ffd700"
WHITE      = "#ffffff"
LTGREY     = "#ccddee"
GREY       = "#7a90a8"
ACCENTS    = [BRAND_CYAN, "#ff8c00", "#00e676", "#ff4db8"]

matplotlib.rcParams["mathtext.fontset"] = "dejavusans"

_LOGO = None
def logo_img():
    global _LOGO
    if _LOGO is None and LOGO_PATH.exists():
        _LOGO = matplotlib.image.imread(str(LOGO_PATH))[:, 100:705]
    return _LOGO


# ── Small helpers ────────────────────────────────────────────────────────────
def eo(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3

def pulse(t, speed=1.0):
    return 0.5 + 0.5 * math.sin(t * speed * math.pi * 2)

def rgba(col, a):
    return (*matplotlib.colors.to_rgb(col), a)

def split_rows(rows, max_per=MAX_PER_REEL):
    """Balanced split: 5 -> [3, 2], 6 -> [3, 3], 4 -> [4]."""
    n = len(rows)
    parts = max(1, math.ceil(n / max_per))
    base, extra = divmod(n, parts)
    out, i = [], 0
    for p in range(parts):
        k = base + (1 if p < extra else 0)
        out.append(rows[i:i + k]); i += k
    return out

def note_text(note):
    """Notes such as 's^{-1}' are pseudo-LaTeX; render them as mathtext."""
    if not note:
        return ""
    if "$" not in note and ("^" in note or "_{" in note):
        return r"$\mathrm{" + note.replace(" ", r"\ ") + "}$"
    return note

def class_label(chapter_tag):
    tag = chapter_tag or ""
    if "XII" in tag or "12" in tag:
        return "Class 12"
    if "X" in tag or "10" in tag:
        return "Class 10"
    return "CBSE"


# ── Text measuring (auto-fit so long formulas / titles never overflow) ───────
_MFIG = None
@lru_cache(maxsize=None)
def fit_size(text, size, max_w, max_h=1.0, weight="bold"):
    """Largest font size <= `size` at which `text` fits max_w x max_h (axes fractions)."""
    global _MFIG
    if _MFIG is None:
        _MFIG = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    t = _MFIG.text(0.5, 0.5, text, fontsize=size, fontweight=weight)
    bb = t.get_window_extent(_MFIG.canvas.get_renderer())
    t.remove()
    scale = min(1.0, max_w * W / max(bb.width, 1), max_h * H / max(bb.height, 1))
    return size * scale

def flat_text(ax, x, y, s, size, color=WHITE, weight="bold",
              ha="center", va="center", alpha=1.0, max_w=None):
    if max_w:
        size = fit_size(s, size, max_w, 1.0, weight)
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, fontweight=weight,
            color=color, alpha=max(0.0, min(1.0, alpha)), zorder=10,
            transform=ax.transAxes)

def hero_text(ax, x, y, s, size, alpha=1.0):
    """Giant formula: dark outline + pure white (no glow, no colour bleed)."""
    alpha = max(0.0, min(1.0, alpha))
    o = ax.text(x, y, s, ha="center", va="center", fontsize=size,
                fontweight="bold", color=BG, alpha=alpha, zorder=11,
                transform=ax.transAxes)
    o.set_path_effects([pe.withStroke(linewidth=7, foreground=rgba("#000814", 0.80)),
                        pe.Normal()])
    w = ax.text(x, y, s, ha="center", va="center", fontsize=size,
                fontweight="bold", color=WHITE, alpha=alpha, zorder=12,
                transform=ax.transAxes)
    # mathtext ignores fontweight; a thin white stroke gives the bold look
    w.set_path_effects([pe.withStroke(linewidth=2.0, foreground=WHITE), pe.Normal()])

def pill(ax, cx, cy, w, h, fill, edge, lw=1.5, alpha=1.0, zorder=8):
    r = min(h, w) * 0.4
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                facecolor=(*fill[:3], fill[3] * alpha),
                                edgecolor=(*edge[:3], edge[3] * alpha), linewidth=lw,
                                zorder=zorder, transform=ax.transAxes))


# ── Shared chrome ────────────────────────────────────────────────────────────
def draw_bg(ax, t, acc):
    ax.set_facecolor(BG)
    p = pulse(t, 0.4)
    for r, a in [(0.55, 0.05), (0.35, 0.08), (0.18, 0.12)]:
        ax.add_patch(Circle((0.5, 0.95), r, facecolor=acc, edgecolor="none",
                            alpha=a * (0.85 + 0.15 * p), transform=ax.transAxes, zorder=0))
    for r, a in [(0.4, 0.04), (0.22, 0.07)]:
        ax.add_patch(Circle((0.5, 0.0), r, facecolor=acc, edgecolor="none",
                            alpha=a, transform=ax.transAxes, zorder=0))

def draw_logo_bar(ax, acc):
    ax.add_patch(FancyBboxPatch((0, 0.918), 1.0, 0.082, boxstyle="square,pad=0",
                                facecolor=BAR_BG, edgecolor="none", zorder=5,
                                transform=ax.transAxes))
    ax.plot([0, 1], [0.918, 0.918], color=acc, lw=2.0, alpha=0.75, zorder=6,
            transform=ax.transAxes)
    img = logo_img()
    if img is not None:
        lax = ax.figure.add_axes([0.012, 0.9225, 0.50, 0.0735])
        lax.imshow(img, interpolation="lanczos"); lax.axis("off")
    else:
        flat_text(ax, 0.04, 0.960, "CBSEMock", size=24, color=WHITE, ha="left")
    flat_text(ax, 0.97, 0.969, "Formula Flash", size=15, color=acc, ha="right", alpha=0.95)
    flat_text(ax, 0.97, 0.948, "cbsemock.org.in", size=13, color=LTGREY,
              weight="normal", ha="right", alpha=0.85)

def draw_dots(ax, idx, n, acc):
    sp = 0.055
    x0 = 0.5 - (n - 1) * sp / 2
    for i in range(n):
        filled, active = i <= idx, i == idx
        ax.add_patch(Circle((x0 + i * sp, 0.910), 0.013 if active else 0.009,
                            facecolor=acc if filled else GREY, edgecolor="none",
                            alpha=1.0 if active else (0.6 if filled else 0.25),
                            zorder=9, transform=ax.transAxes))

def draw_footer(ax, t, acc):
    ax.add_patch(FancyBboxPatch((0, 0), 1.0, 0.065, boxstyle="square,pad=0",
                                facecolor=BAR_BG, edgecolor="none", zorder=5,
                                transform=ax.transAxes))
    ax.plot([0, 1], [0.065, 0.065], color=acc, lw=1.2, alpha=0.4, zorder=6,
            transform=ax.transAxes)
    flat_text(ax, 0.5, 0.045, "cbsemock.org.in  •  Free Practice Papers & Notes",
              size=14, color=LTGREY, weight="normal", alpha=0.85)
    flat_text(ax, 0.5, 0.020, "@cbsemock  |  Save & Share this reel!",
              size=14, color=acc, weight="normal", alpha=0.70 + 0.20 * pulse(t, 0.5))


# ── Diagram (any diagram_library function, scaled up for the big card) ───────
DIAG_BOX   = (0.14, 0.455, 0.72, 0.335)   # left, bottom, width, height (figure fractions)
TEXT_SCALE = 2.5
LINE_SCALE = 2.0

def draw_diagram(fig, key, prog):
    fn = DIAGRAMS.get(key)
    if fn is None or prog <= 0:
        return
    ax2 = fig.add_axes(list(DIAG_BOX))
    ax2.set_facecolor(CARD_BG)
    ax2.patch.set_visible(False)
    try:
        fn(ax2, progress=max(0.05, min(1.0, prog)))
    except Exception as e:                       # a broken diagram must not kill a reel
        print(f"[WARN] diagram '{key}' failed: {e}")
        ax2.remove(); return
    ax2.axis("off")
    # Library diagrams were sized for a small cell — scale strokes and labels up.
    for tx in ax2.texts:
        tx.set_fontsize(tx.get_fontsize() * TEXT_SCALE)
        ap = getattr(tx, "arrow_patch", None)
        if ap is not None:
            ap.set_linewidth(ap.get_linewidth() * LINE_SCALE)
            ap.set_mutation_scale(ap.get_mutation_scale() * LINE_SCALE)
    for ln in ax2.lines:
        ln.set_linewidth(ln.get_linewidth() * LINE_SCALE)
        ln.set_markersize(ln.get_markersize() * LINE_SCALE)
    for pt in ax2.patches:
        pt.set_linewidth(pt.get_linewidth() * LINE_SCALE)
        if hasattr(pt, "set_mutation_scale") and hasattr(pt, "get_mutation_scale") \
                and not isinstance(pt, FancyBboxPatch):
            pt.set_mutation_scale(pt.get_mutation_scale() * LINE_SCALE)
    for col in ax2.collections:
        try:
            col.set_sizes(np.asarray(col.get_sizes()) * LINE_SCALE ** 2)
        except Exception:
            pass
        try:
            col.set_linewidths(np.asarray(col.get_linewidths()) * LINE_SCALE)
        except Exception:
            pass


# ── Screens ──────────────────────────────────────────────────────────────────
def draw_card(ax, row, num, total, prog, t, acc):
    p = eo(prog)
    card_a = min(0.97, eo(min(1.0, prog * 4)))
    ax.add_patch(FancyBboxPatch((0.015, 0.075), 0.970, 0.835, boxstyle="square,pad=0",
                                facecolor=CARD_BG, edgecolor="none", alpha=card_a,
                                zorder=2, transform=ax.transAxes))
    ax.add_patch(FancyBboxPatch((0.015, 0.075), 0.009, 0.835, boxstyle="square,pad=0",
                                facecolor=acc, edgecolor="none", alpha=card_a * 0.95,
                                zorder=3, transform=ax.transAxes))

    flat_text(ax, 0.09, 0.878, f"Formula {num} of {total}", size=15, color=acc,
              weight="normal", ha="left", alpha=p * 0.85)
    flat_text(ax, 0.09, 0.850, row["label"].upper(), size=26, color=WHITE,
              ha="left", alpha=p, max_w=0.84)
    ax.plot([0.06, 0.94], [0.830, 0.830], color=acc, lw=0.8, alpha=p * 0.3,
            transform=ax.transAxes, zorder=5)

    draw_diagram(ax.figure, row.get("diagram"), (prog - 0.12) / 0.55)

    ax.plot([0.06, 0.94], [0.420, 0.420], color=acc, lw=0.8, alpha=p * 0.25,
            transform=ax.transAxes, zorder=5)

    if prog >= 0.10:
        fp  = min(1.0, eo((prog - 0.10) / 0.50))
        pls = 0.93 + 0.07 * pulse(t, 1.4)
        fsize = fit_size(row["formula"], 72, 0.86, 0.150)
        hero_text(ax, 0.5, 0.320, row["formula"], size=fsize, alpha=fp * pls)

        note = note_text(row.get("note", ""))
        if note:
            nsize = fit_size(note, 21, 0.50, 1.0)
            # solid accent pill with dark text (white on bright accents is hard to read)
            pill(ax, 0.5, 0.185, 0.58, 0.052, fill=rgba(acc, 1.0),
                 edge=rgba(acc, 1.0), lw=1.5, alpha=fp)
            flat_text(ax, 0.5, 0.185, note, size=nsize, color=BAR_BG, alpha=fp)


HOOKS = ["YOU MUST KNOW", "DON'T SKIP THESE", "REVISE BEFORE THE EXAM", "EXAMINERS LOVE THESE"]

def back_out(t, s=2.2):
    """Ease with a small overshoot — gives the 'pop' feel."""
    t = max(0.0, min(1.0, t)) - 1
    return t * t * ((s + 1) * t + s) + 1

def draw_intro(ax, data, part, nparts, nrows, prog, t, topic_id=""):
    """Hook screen: giant count + punch line + topic. Readable from frame 0."""
    prog = min(1.0, prog * 1.5)      # everything lands by 60% so the full hook holds ~1 s
    pls = pulse(t, 1.0)
    cx, cy = 0.5, 0.640

    # Rotating sunburst behind the number (x scaled so rays are round on a 9:16 canvas)
    rot = t * 0.35
    for k in range(14):
        a0 = rot + k * 2 * math.pi / 14
        a1 = a0 + math.pi / 14 * 0.9
        R = 0.62
        pts = [(cx, cy)] + [(cx + R * math.cos(a) * H / W, cy + R * math.sin(a)) for a in (a0, a1)]
        ax.add_patch(plt.Polygon(pts, closed=True, facecolor=BRAND_CYAN, edgecolor="none",
                                 alpha=0.055, zorder=1, transform=ax.transAxes))
    for r, a in [(0.20, 0.10), (0.12, 0.16)]:
        ax.add_patch(Circle((cx, cy), r * (0.95 + 0.05 * pls), facecolor=GOLD, edgecolor="none",
                            alpha=a, transform=ax.transAxes, zorder=1))

    # Subject chip (top)
    c1 = eo(prog / 0.20)
    cls = class_label(data.get("chapter_tag", ""))
    chip = f"{data['subject'].upper()}  •  {cls.upper()}"
    pill(ax, 0.5, 0.790, 0.56, 0.042, fill=rgba(BRAND_CYAN, 0.16),
         edge=rgba(BRAND_CYAN, 0.85), lw=1.8, alpha=c1)
    flat_text(ax, 0.5, 0.790, chip, size=19, color=BRAND_CYAN, alpha=c1, max_w=0.50)

    # Giant number — pops in with overshoot, already visible on frame 0
    ns = 0.55 + 0.45 * back_out(prog / 0.22)
    ns *= 1.0 + 0.025 * pls
    num = ax.text(cx, cy, str(nrows), ha="center", va="center", fontsize=230 * ns,
                  fontweight="bold", color=GOLD, zorder=12, transform=ax.transAxes)
    num.set_path_effects([pe.withStroke(linewidth=14, foreground=rgba("#3a2a00", 0.9)),
                          pe.withStroke(linewidth=5, foreground=WHITE), pe.Normal()])

    # "FORMULAS" — slides up
    w1 = eo((prog - 0.06) / 0.22)
    word = "MORE FORMULAS" if part > 1 else ("FORMULAS" if nrows != 1 else "FORMULA")
    flat_text(ax, 0.5, 0.525 - 0.02 * (1 - w1), word, size=70, color=WHITE,
              alpha=min(1.0, 0.35 + w1), max_w=0.88)

    # Highlighter bar sweeps left-to-right, then the punch line lands on it
    hk = HOOKS[sum(map(ord, topic_id)) % len(HOOKS)]
    hsize = fit_size(hk, 34, 0.74)
    bw = 0.84
    sw = eo((prog - 0.20) / 0.22)
    if sw > 0:
        ax.add_patch(FancyBboxPatch((0.5 - bw / 2, 0.437), bw * sw, 0.052,
                                    boxstyle="square,pad=0", facecolor=GOLD, edgecolor="none",
                                    zorder=8, transform=ax.transAxes))
        if sw > 0.55:
            flat_text(ax, 0.5, 0.463, hk, size=hsize, color=BAR_BG,
                      alpha=(sw - 0.55) / 0.45)

    # Topic title
    tp = eo((prog - 0.38) / 0.22)
    if tp > 0:
        title = f"{data['title_line1']} {data['title_line2']}".strip()
        flat_text(ax, 0.5, 0.398, "from", size=17, color=LTGREY, weight="normal", alpha=tp * 0.9)
        flat_text(ax, 0.5, 0.352 - 0.012 * (1 - tp), title, size=44, color=BRAND_CYAN,
                  alpha=tp, max_w=0.90)

    # Marks chip + part chip
    mp = back_out((prog - 0.55) / 0.20) if prog > 0.55 else 0
    if mp > 0:
        marks = (data.get("board_note", "").split("·")[0]).strip().upper()
        chips = [c for c in [marks, f"PART {part} OF {nparts}" if nparts > 1 else ""] if c]
        cw, gap = 0.34, 0.04
        x0 = 0.5 - ((len(chips) - 1) * (cw + gap)) / 2
        for k, c in enumerate(chips):
            x = x0 + k * (cw + gap)
            col = "#ff4db8" if k == 0 else GOLD
            pill(ax, x, 0.270, cw * mp, 0.044, fill=rgba(col, 0.16), edge=rgba(col, 0.9),
                 lw=1.8, alpha=min(1.0, mp))
            flat_text(ax, x, 0.270, c, size=18, color=col, alpha=min(1.0, mp), max_w=cw * 0.86)

    # Bouncing "watch till the end" cue
    wp = eo((prog - 0.70) / 0.20)
    if wp > 0:
        b = 0.008 * math.sin(t * 2 * math.pi * 2.0)
        flat_text(ax, 0.5, 0.190, "Watch till the end", size=19, color=WHITE,
                  weight="normal", alpha=wp * 0.92)
        flat_text(ax, 0.5, 0.150 + b, "▼", size=24, color=GOLD, alpha=wp)


def draw_outro(ax, part, nparts, prog, t):
    p, pls = eo(prog), pulse(t, 0.9)
    for r, a in [(0.38, 0.06), (0.24, 0.11), (0.12, 0.17)]:
        ax.add_patch(Circle((0.5, 0.52), r * (0.92 + 0.08 * pls), facecolor=GOLD,
                            alpha=a * p, transform=ax.transAxes, zorder=1))
    flat_text(ax, 0.5, 0.640, "SAVE THIS REEL!", size=38, color=GOLD,
              alpha=p * (0.88 + 0.12 * pls))
    sub = (f"Follow for Part {part + 1}" if part < nparts
           else "Share with your batchmates")
    flat_text(ax, 0.5, 0.577, sub, size=21, color=WHITE, weight="normal", alpha=p * 0.92)
    if prog > 0.25:
        bp = eo((prog - 0.25) / 0.75)
        pill(ax, 0.5, 0.510, 0.65, 0.065, fill=rgba("#00b4d8", 1.0),
             edge=rgba(BRAND_CYAN, 1.0), lw=2.0, alpha=bp)
        flat_text(ax, 0.5, 0.510, "CBSEMock", size=32, color=WHITE, alpha=bp)
        flat_text(ax, 0.5, 0.465, "cbsemock.org.in", size=18, color=BRAND_CYAN,
                  alpha=bp * 0.95)
    if prog > 0.50:
        lp = eo((prog - 0.50) / 0.50)
        for txt, y in [("Free Notes & Practice Tests  —  cbsemock.org.in", 0.408),
                       ("Instagram: @cbsemock", 0.368),
                       ("Telegram:  t.me/cbsemockportal", 0.328)]:
            flat_text(ax, 0.5, y, txt, size=17, color=LTGREY, weight="normal",
                      alpha=lp * 0.88)


# ── Frame render (top-level so it can run in a worker pool) ──────────────────
def render_frame(job):
    topic_id, part, fi, frame_dir = job
    data   = TOPICS[topic_id]
    chunks = split_rows(data["rows"])
    rows   = chunks[part - 1]
    offset = sum(len(c) for c in chunks[:part - 1])
    total  = len(data["rows"])
    cards_end = INTRO_SEC + CARD_SEC * len(rows)
    t = fi / FPS

    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    if t < INTRO_SEC:
        acc = BRAND_CYAN
        draw_bg(ax, t, acc)
        draw_intro(ax, data, part, len(chunks), len(rows), t / INTRO_SEC, t, topic_id)
    elif t >= cards_end:
        acc = GOLD
        draw_bg(ax, t, acc)
        draw_outro(ax, part, len(chunks), (t - cards_end) / OUTRO_SEC, t)
    else:
        i    = min(len(rows) - 1, int((t - INTRO_SEC) // CARD_SEC))
        prog = ((t - INTRO_SEC) - i * CARD_SEC) / CARD_SEC
        acc  = ACCENTS[(offset + i) % len(ACCENTS)]
        draw_bg(ax, t, acc)
        draw_card(ax, rows[i], offset + i + 1, total, prog, t, acc)
        draw_dots(ax, i, len(rows), acc)
    draw_logo_bar(ax, acc)
    draw_footer(ax, t, acc)

    fig.savefig(str(Path(frame_dir) / f"frame_{fi:05d}.png"), dpi=DPI, facecolor=BG)
    plt.close(fig)


def queue_name(topic_id, part, nparts):
    """Poster-friendly file name: post_formula_reel.py turns the stem into the caption title."""
    import re
    d = TOPICS[topic_id]
    slug = re.sub(r"[^a-z0-9]+", "_", f"{d['title_line1']} {d['title_line2']}".lower()).strip("_")
    return f"{slug}_part_{part}.mp4" if nparts > 1 else f"{slug}.mp4"


def generate_reel(topic_id, part=None, out_dir=OUT_DIR, workers=None, queue_names=False):
    """Render one topic. Returns the list of MP4 paths (one per part)."""
    data   = TOPICS[topic_id]
    chunks = split_rows(data["rows"])
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for pn in ([part] if part else range(1, len(chunks) + 1)):
        secs    = INTRO_SEC + CARD_SEC * len(chunks[pn - 1]) + OUTRO_SEC
        nframes = int(round(secs * FPS))
        suffix  = f"_p{pn}" if len(chunks) > 1 else ""
        out     = out_dir / (queue_name(topic_id, pn, len(chunks)) if queue_names
                             else f"{topic_id}_reel_v3{suffix}.mp4")
        if queue_names and out.exists():
            print(f"[SKIP] {out.name} exists"); outputs.append(out); continue
        frame_dir = Path(tempfile.mkdtemp(prefix="reel_v3_"))
        print(f"[INFO] {topic_id} part {pn}/{len(chunks)}: {nframes} frames ({secs:.0f}s)")
        jobs = [(topic_id, pn, fi, str(frame_dir)) for fi in range(nframes)]
        with Pool(workers or os.cpu_count() or 1) as pool:
            pool.map(render_frame, jobs, chunksize=15)

        base = ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frame_dir / "frame_%05d.png")]
        venc = ["-c:v", "libx264", "-profile:v", "main", "-level", "4.0", "-preset", "slow",
                "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
        ok = False
        if BG_MUSIC.exists():
            cmd = base + ["-stream_loop", "-1", "-i", str(BG_MUSIC)] + venc + [
                "-c:a", "aac", "-ar", "44100", "-b:a", "96k",
                "-af", f"afade=t=in:st=0:d=1.5,afade=t=out:st={secs - 2}:d=2,volume=0.4",
                "-t", f"{secs}", str(out)]
            r = subprocess.run(cmd, capture_output=True, text=True)
            ok = r.returncode == 0
            if not ok:
                print(f"[WARN] audio mux failed, encoding silent: {r.stderr[-300:]}")
        if not ok:
            r = subprocess.run(base + venc + [str(out)], capture_output=True, text=True)
            if r.returncode != 0:
                shutil.rmtree(frame_dir, ignore_errors=True)
                raise RuntimeError(f"ffmpeg failed: {r.stderr[-600:]}")
        shutil.rmtree(frame_dir, ignore_errors=True)
        print(f"[OK] {out}  ({out.stat().st_size / 1048576:.1f} MB)")
        outputs.append(out)
    return outputs


def main():
    ap = argparse.ArgumentParser(description="Formula Flash reel generator (V5 design)")
    ap.add_argument("--topic", default="current_electricity")
    ap.add_argument("--part", type=int, default=None, help="render only this part")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out-dir", default=str(OUT_DIR))
    ap.add_argument("--list", action="store_true", help="list topics and their parts")
    ap.add_argument("--queue-names", action="store_true",
                    help="name files the way post_formula_reel.py expects (title_part_N.mp4)")
    a = ap.parse_args()
    if a.list:
        for k, v in TOPICS.items():
            print(f"{k:28s} {v['subject']:12s} parts={[len(c) for c in split_rows(v['rows'])]}")
        return
    for tid in (TOPICS if a.all else [a.topic]):
        if tid not in TOPICS:
            sys.exit(f"Unknown topic '{tid}'. Use --list.")
        generate_reel(tid, a.part, a.out_dir, queue_names=a.queue_names)


if __name__ == "__main__":
    main()
