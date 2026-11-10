#!/usr/bin/env python3
"""
generate_formula_reel_v2.py
─────────────────────────
Generates a 7-sec animated MP4 reel (1080×1920) in the new reference style.
Each formula row slides in one by one, diagram draws itself in.
Branding: cbsemock.org.in

Uses: matplotlib (diagrams + frames) + FFmpeg (encode MP4)
Output: formula-posts/videos/

Usage:
  python3 generate_formula_reel_v2.py --topic em_induction
  python3 generate_formula_reel_v2.py --topic current_electricity
"""

import argparse
import math
import shutil
import subprocess
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

OUT_DIR   = Path(__file__).parent / "formula-posts" / "videos"
FRAME_DIR = Path(__file__).parent / "formula-posts" / "_reel_frames"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W_IN, H_IN = 10.80, 19.20   # 1080×1920 at 100 dpi
DPI = 100
FPS = 30
TOTAL_SEC = 8

BG      = "#050e1f"   # CBSEMock brand navy
CARD_BG = "#0a1628"
CYAN    = "#00d4ff"   # brand cyan
YELLOW  = "#f9c820"   # brand yellow
WHITE   = "#f0f0f0"
GREY    = "#8899aa"
GREEN   = "#00e676"
ORANGE  = "#ff6b35"
PINK    = "#ff4081"

LOGO_PATH = Path(__file__).parent / "formula-posts" / "_cbsemock_logo_dark.png"

LABEL_COLORS = ["#0d47a1","#1565c0","#1976d2","#1e88e5","#2196f3","#1976d2"]

# ── Subject-specific diagram library ──────────────────────────────────────────
from diagram_library import DIAGRAMS as DIAGRAM_FNS  # noqa: E402

# (old inline physics-only functions removed — library has all subjects)

def draw_flux_diagram(ax, progress=1.0):  # keep for any legacy direct call
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    n = max(1, int(6 * progress))
    for y in np.linspace(0.15, 0.85, n):
        ax.annotate("", xy=(0.9, y), xytext=(0.1, y),
                    arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.2))
    if progress > 0.4:
        p2 = (progress - 0.4) / 0.6
        ellipse = mpatches.Ellipse((0.5, 0.5), 0.25, 0.55, angle=25,
                                    fill=False, edgecolor=ORANGE,
                                    lw=2.5, alpha=min(1, p2*2))
        ax.add_patch(ellipse)


def draw_coil_magnet(ax, progress=1.0):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    if progress > 0.1:
        ax.add_patch(FancyBboxPatch((0.05, 0.38), 0.15, 0.24,
                                     boxstyle="round,pad=0.01",
                                     facecolor="#cc0000", edgecolor="white", lw=1,
                                     alpha=min(1, (progress-0.1)/0.3)))
        ax.add_patch(FancyBboxPatch((0.20, 0.38), 0.15, 0.24,
                                     boxstyle="round,pad=0.01",
                                     facecolor="#0055aa", edgecolor="white", lw=1,
                                     alpha=min(1, (progress-0.1)/0.3)))
        ax.text(0.125, 0.50, "N", color="white", fontsize=9, ha="center",
                va="center", fontweight="bold", alpha=min(1, (progress-0.1)/0.3))
        ax.text(0.275, 0.50, "S", color="white", fontsize=9, ha="center",
                va="center", fontweight="bold", alpha=min(1, (progress-0.1)/0.3))
    if progress > 0.3:
        x = np.linspace(0.4, 0.4 + 0.5*min(1,(progress-0.3)/0.5), 200)
        y = 0.5 + 0.18 * np.sin((x - 0.4) / 0.5 * 6 * math.pi)
        ax.plot(x, y, color=ORANGE, lw=2.5)
    if progress > 0.7:
        ax.annotate("", xy=(0.38, 0.50), xytext=(0.28, 0.50),
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=2,
                                   alpha=min(1.0, (progress-0.7)/0.3)))


def draw_lenz(ax, progress=1.0):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.02, 0.38), 0.14, 0.24,
                                 boxstyle="round,pad=0.01",
                                 facecolor="#cc0000", edgecolor="white", lw=1))
    ax.add_patch(FancyBboxPatch((0.16, 0.38), 0.14, 0.24,
                                 boxstyle="round,pad=0.01",
                                 facecolor="#0055aa", edgecolor="white", lw=1))
    ax.text(0.09, 0.50, "N", color="white", fontsize=8, ha="center",
            va="center", fontweight="bold")
    ax.text(0.23, 0.50, "S", color="white", fontsize=8, ha="center",
            va="center", fontweight="bold")
    end_x = 0.32 + 0.10 * min(1, progress / 0.5)
    ax.annotate("", xy=(end_x, 0.50), xytext=(0.32, 0.50),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.5))
    if progress > 0.4:
        x = np.linspace(0.44, 0.78, 150)
        y = 0.5 + 0.17 * np.sin((x - 0.44) / 0.34 * 5 * math.pi)
        ax.plot(x, y, color=ORANGE, lw=2.5)
    if progress > 0.7:
        ax.annotate("", xy=(0.60, 0.72), xytext=(0.70, 0.72),
                    arrowprops=dict(arrowstyle="->", color=PINK, lw=1.5))
        ax.text(0.62, 0.80, "Induced I", color=PINK, fontsize=6, ha="center")


def draw_motional(ax, progress=1.0):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.plot([0.1, 0.9], [0.25, 0.25], color=GREY, lw=2, alpha=min(1, progress*2))
    ax.plot([0.1, 0.9], [0.75, 0.75], color=GREY, lw=2, alpha=min(1, progress*2))
    if progress > 0.3:
        ax.plot([0.55, 0.55], [0.25, 0.75], color=CYAN, lw=4,
                alpha=min(1, (progress-0.3)/0.4))
    if progress > 0.6:
        ax.annotate("", xy=(0.70, 0.50), xytext=(0.57, 0.50),
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.5,
                                   alpha=(progress-0.6)/0.4))
        ax.text(0.73, 0.50, "v", color=GREEN, fontsize=10,
                va="center", fontweight="bold", style="italic",
                alpha=(progress-0.6)/0.4)
    for x in [0.20, 0.35]:
        for y in [0.35, 0.50, 0.65]:
            ax.plot(x, y, "o", color=CYAN, markersize=5,
                    alpha=min(1, progress*1.5))


def draw_inductor(ax, progress=1.0):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    n_points = max(2, int(400 * progress))
    x = np.linspace(0.1, 0.9, n_points)
    y = 0.5 + 0.20 * np.sin((x - 0.1) / 0.8 * 8 * math.pi)
    ax.plot(x, y, color=ORANGE, lw=3)
    if progress > 0.6:
        ax.annotate("", xy=(0.85, 0.30), xytext=(0.15, 0.30),
                    arrowprops=dict(arrowstyle="->", color=YELLOW, lw=2,
                                   alpha=(progress-0.6)/0.4))


def draw_ohm(ax, progress=1.0):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    triangle = plt.Polygon([[0.5, 0.85], [0.1, 0.20], [0.9, 0.20]],
                            fill=False, edgecolor=CYAN, lw=2, alpha=min(1, progress*1.5))
    ax.add_patch(triangle)
    if progress > 0.4:
        ax.text(0.50, 0.70, "V", color=YELLOW, fontsize=14,
                ha="center", va="center", fontweight="bold", alpha=(progress-0.4)/0.6)
        ax.text(0.27, 0.28, "I", color=GREEN, fontsize=12,
                ha="center", va="center", fontweight="bold", alpha=(progress-0.4)/0.6)
        ax.text(0.73, 0.28, "R", color=ORANGE, fontsize=12,
                ha="center", va="center", fontweight="bold", alpha=(progress-0.4)/0.6)


def draw_wire(ax, progress=1.0):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.1, 0.35), 0.8, 0.30,
                                 boxstyle="round,pad=0.02",
                                 facecolor="#334455", edgecolor=CYAN, lw=2,
                                 alpha=min(1, progress*1.5)))
    if progress > 0.5:
        end_x = 0.15 + 0.70 * min(1, (progress-0.5)/0.5)
        ax.annotate("", xy=(end_x, 0.50), xytext=(0.15, 0.50),
                    arrowprops=dict(arrowstyle="->", color=YELLOW, lw=2))


def draw_loop(ax, progress=1.0):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    theta = np.linspace(0, 2*math.pi*progress, 300)
    x = 0.5 + 0.33 * np.cos(theta)
    y = 0.52 + 0.33 * np.sin(theta)
    ax.plot(x, y, color=CYAN, lw=2.5)
    if progress > 0.7:
        ax.add_patch(mpatches.Rectangle((0.42, 0.14), 0.16, 0.08,
                                          facecolor="#444", edgecolor=YELLOW, lw=1.5,
                                          alpha=min(1.0, (progress-0.7)/0.3)))
        ax.text(0.5, 0.18, "ε", color=YELLOW, fontsize=10,
                ha="center", va="center", fontweight="bold",
                alpha=min(1.0, (progress-0.7)/0.3))


def draw_bridge(ax, progress=1.0):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    pts = {"A": (0.5, 0.88), "B": (0.15, 0.50),
           "C": (0.85, 0.50), "D": (0.5, 0.12)}
    for (a, b), label in [
        (("A", "B"), "P"), (("A", "C"), "Q"),
        (("B", "D"), "R"), (("C", "D"), "S"),
    ]:
        x1, y1 = pts[a]; x2, y2 = pts[b]
        ax.plot([x1, x2], [y1, y2], color=CYAN, lw=2, alpha=min(1, progress*1.5))
        ax.text((x1+x2)/2 - 0.07, (y1+y2)/2, label,
                color=YELLOW, fontsize=9, fontweight="bold",
                alpha=min(1, progress*1.5))
    if progress > 0.5:
        ax.plot([pts["B"][0], pts["C"][0]], [pts["B"][1], pts["C"][1]],
                color=GREEN, lw=1.5, ls="--", alpha=(progress-0.5)/0.5)
        ax.text(0.5, 0.52, "G", color=GREEN, fontsize=8, ha="center",
                alpha=(progress-0.5)/0.5)
    for name, (x, y) in pts.items():
        ax.plot(x, y, "o", color=WHITE, markersize=7, alpha=min(1, progress*1.5))


def draw_power(ax, progress=1.0):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    circle = plt.Circle((0.5, 0.60), 0.22, fill=False,
                         edgecolor=YELLOW, lw=2.5, alpha=min(1, progress*1.5))
    ax.add_patch(circle)
    if progress > 0.4:
        ax.plot([0.36, 0.64], [0.44, 0.76], color=YELLOW, lw=2,
                alpha=(progress-0.4)/0.6)
        ax.plot([0.64, 0.36], [0.44, 0.76], color=YELLOW, lw=2,
                alpha=(progress-0.4)/0.6)


from formula_topics_master import TOPICS



def ease_out(t):
    return 1 - (1 - min(1, t)) ** 3


def render_frame(data, global_t, frame_idx):
    """
    Animation timeline (global_t: 0 → 1):
      0.00–0.12 : title fade-in
      0.12–1.00 : rows slide in one by one (each gets equal share of remaining time)
      last 0.08 : footer appears
    """
    rows = data["rows"]
    n    = len(rows)

    fig = plt.figure(figsize=(W_IN, H_IN), facecolor=BG)

    logo_frac   = 0.070  # CBSEMock logo strip (taller for centred logo)
    top_frac    = 0.090  # title band
    footer_frac = 0.065
    row_frac    = (1.0 - logo_frac - top_frac - footer_frac) / n

    title_prog = min(1.0, global_t / 0.12)

    # ── CBSEMock logo header ────────────────────────────────────────────────────
    ax_logo = fig.add_axes([0, 1 - logo_frac, 1, logo_frac])
    ax_logo.set_facecolor(BG); ax_logo.axis("off")
    # Reel is 10.80 × (19.20 * 0.07) = 10.80 × 1.344 inches → ~8:1 aspect
    # Square logo: width = 0.13 in axes coords to keep it circular
    # Horizontal logo — left-aligned, takes ~45% width
    if LOGO_PATH.exists() and title_prog > 0:
        try:
            logo_img = matplotlib.image.imread(str(LOGO_PATH))
            li = ax_logo.inset_axes([0.01, 0.10, 0.44, 0.80])
            li.imshow(logo_img); li.axis("off")
            li.patch.set_alpha(title_prog)
        except Exception:
            ax_logo.text(0.5, 0.55, "CBSEMock", color=CYAN, fontsize=22,
                         fontweight="bold", ha="center", va="center", alpha=title_prog,
                         transform=ax_logo.transAxes)
    # Subject pill right side
    subject = data.get("subject","CBSE")
    subj_colors = {"Physics":"#1565c0","Chemistry":"#2e7d32",
                   "Mathematics":"#6a1b9a","Biology":"#c62828","CS":"#00695c"}
    sc = subj_colors.get(subject,"#1565c0")
    ax_logo.add_patch(FancyBboxPatch((0.73, 0.15), 0.25, 0.70,
        boxstyle="round,pad=0.02", facecolor=(*matplotlib.colors.to_rgb(sc), title_prog),
        edgecolor="none", transform=ax_logo.transAxes))
    ax_logo.text(0.855, 0.52, subject, color="white", fontsize=9, fontweight="bold",
                 ha="center", va="center", alpha=title_prog, transform=ax_logo.transAxes)
    ax_logo.axhline(0, color=CYAN, lw=2, alpha=0.8)

    # ── Title band ─────────────────────────────────────────────────────────────
    ax_title = fig.add_axes([0, 1 - logo_frac - top_frac, 1, top_frac])
    ax_title.set_facecolor(BG); ax_title.axis("off")
    ax_title.text(0.5, 0.78, data["title_line1"], color=WHITE,
                  fontsize=32, fontweight="bold", ha="center", va="center",
                  alpha=title_prog, transform=ax_title.transAxes)
    ax_title.text(0.5, 0.40, data["title_line2"], color=CYAN,
                  fontsize=32, fontweight="bold", ha="center", va="center",
                  alpha=title_prog, transform=ax_title.transAxes)
    ax_title.text(0.5, 0.08, data.get("board_note", "CBSE Board Exam"), color=YELLOW,
                  fontsize=11, ha="center", va="center",
                  alpha=title_prog, transform=ax_title.transAxes)

    # ── Rows ───────────────────────────────────────────────────────────────────
    row_window = (1.0 - 0.12 - 0.08) / n

    for i, row in enumerate(rows):
        row_start = 0.12 + i * row_window
        row_local = max(0.0, (global_t - row_start) / row_window)
        row_alpha = ease_out(min(1.0, row_local * 2))

        if row_alpha <= 0:
            continue

        y_bottom = footer_frac + (n - 1 - i) * row_frac
        pad = 0.008
        slide_offset = (1 - ease_out(min(1.0, row_local * 3))) * 0.03

        # Row card
        ax_card = fig.add_axes([pad, y_bottom + pad + slide_offset,
                                 1 - 2*pad, row_frac - 2*pad])
        ax_card.set_facecolor((*matplotlib.colors.to_rgb(CARD_BG), row_alpha))
        for spine in ax_card.spines.values():
            c = matplotlib.colors.to_rgb(LABEL_COLORS[i % len(LABEL_COLORS)])
            spine.set_edgecolor((*c, row_alpha))
            spine.set_linewidth(1.5)
        ax_card.set_xticks([]); ax_card.set_yticks([])

        # Label pill — coloured background via explicit patch
        ax_label = fig.add_axes([pad*2, y_bottom + pad*2 + slide_offset,
                                  0.28, row_frac - pad*4])
        ax_label.set_facecolor(BG); ax_label.axis("off")
        ax_label.set_xlim(0,1); ax_label.set_ylim(0,1)
        pill_col = LABEL_COLORS[i % len(LABEL_COLORS)]
        import matplotlib.patches as _mp2
        ax_label.add_patch(_mp2.FancyBboxPatch((0.03,0.03), 0.94, 0.94,
                            boxstyle="round,pad=0.04",
                            facecolor=(*matplotlib.colors.to_rgb(pill_col), row_alpha),
                            edgecolor="none", zorder=1))
        ax_label.text(0.5, 0.65, row["label"], color=WHITE, fontsize=10.5,
                      fontweight="bold", ha="center", va="center",
                      alpha=row_alpha, transform=ax_label.transAxes, wrap=True, zorder=2)
        ax_label.text(0.5, 0.22, row["note"], color="#ccddee", fontsize=8,
                      ha="center", va="center",
                      alpha=row_alpha, transform=ax_label.transAxes, zorder=2)

        # Diagram
        diag_prog = min(1.0, row_local * 1.5)
        ax_diag = fig.add_axes([0.29 + pad, y_bottom + pad*2 + slide_offset,
                                  0.34, row_frac - pad*4])
        ax_diag.set_facecolor((*matplotlib.colors.to_rgb(CARD_BG), row_alpha))
        ax_diag.axis("off")
        draw_fn = DIAGRAM_FNS.get(row["diagram"])
        if draw_fn:
            draw_fn(ax_diag, diag_prog)

        # Formula
        ax_form = fig.add_axes([0.66, y_bottom + pad + slide_offset,
                                  0.34 - pad, row_frac - pad*2])
        ax_form.set_facecolor((*matplotlib.colors.to_rgb(CARD_BG), row_alpha))
        ax_form.axis("off")
        ax_form.text(0.5, 0.52, row["formula"], color=(*matplotlib.colors.to_rgb(YELLOW),
                                                         row_alpha),
                     fontsize=16, fontweight="bold", ha="center", va="center",
                     transform=ax_form.transAxes, usetex=False)

    # ── Footer — CBSEMock branded ───────────────────────────────────────────────
    footer_alpha = ease_out(max(0, (global_t - 0.92) / 0.08))
    ax_foot = fig.add_axes([0, 0, 1, footer_frac])
    ax_foot.set_facecolor("#071020"); ax_foot.axis("off")
    ax_foot.axhline(0.97, color=(*matplotlib.colors.to_rgb("#1565c0"), footer_alpha), lw=2)
    # Yellow CTA pill
    ax_foot.text(0.50, 0.68, data.get("cta", "Save for Revision  •  cbsemock.org.in"), color="#1a1a1a", fontsize=10,
                 fontweight="bold", ha="center", va="center",
                 alpha=footer_alpha, transform=ax_foot.transAxes,
                 bbox=dict(boxstyle="round,pad=0.45",
                           facecolor=(*matplotlib.colors.to_rgb(YELLOW), footer_alpha),
                           edgecolor="none", lw=0))
    # Domain
    ax_foot.text(0.50, 0.28, "www  cbsemock.org.in", color=WHITE, fontsize=9,
                 ha="center", va="center", alpha=footer_alpha,
                 transform=ax_foot.transAxes)
    # Hashtags
    ax_foot.text(0.50, 0.08, data.get("hashtags", "#CBSEMock #FormulaFlash #CBSE"), color=GREY, fontsize=6.5,
                 ha="center", va="center", alpha=footer_alpha,
                 transform=ax_foot.transAxes)

    # Save frame
    out_path = FRAME_DIR / f"frame_{frame_idx:05d}.png"
    fig.savefig(out_path, dpi=DPI, bbox_inches="tight",
                facecolor=BG, pad_inches=0)
    plt.close(fig)


def generate_reel(topic_id: str) -> Path:
    data = TOPICS[topic_id]
    total_frames = FPS * TOTAL_SEC

    if FRAME_DIR.exists():
        shutil.rmtree(FRAME_DIR)
    FRAME_DIR.mkdir(parents=True)

    print(f"[INFO] Rendering {total_frames} frames for '{topic_id}'...")
    for i in range(total_frames):
        t = i / (total_frames - 1)
        render_frame(data, t, i)
        if i % 30 == 0:
            print(f"  frame {i}/{total_frames}")

    out_path = OUT_DIR / f"{topic_id}_reel_v2.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAME_DIR / "frame_%05d.png"),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(out_path),
    ]
    print("[INFO] Encoding MP4...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] FFmpeg: {result.stderr[-600:]}")
    else:
        size_mb = out_path.stat().st_size / 1024 / 1024
        print(f"[OK] Saved: {out_path}  ({size_mb:.1f} MB)")

    shutil.rmtree(FRAME_DIR)
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="em_induction")
    parser.add_argument("--all",   action="store_true")
    args = parser.parse_args()

    if args.all:
        for t in TOPICS:
            generate_reel(t)
    else:
        generate_reel(args.topic)


if __name__ == "__main__":
    main()
