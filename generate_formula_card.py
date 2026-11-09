#!/usr/bin/env python3
"""
generate_formula_card.py
─────────────────────────
Generates a high-quality formula card image (720×1280) matching the
reference style: dark bg, rounded formula rows, diagrams, cyan title.
Saves to formula-posts/images/

Usage:
  python3 generate_formula_card.py --topic em_induction
  python3 generate_formula_card.py --topic current_electricity
"""

import argparse
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
from pathlib import Path

OUT_DIR = Path(__file__).parent / "formula-posts" / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W_IN, H_IN = 7.2, 12.8   # inches at 100 dpi = 720×1280
DPI = 100

BG      = "#1a1a2e"
CARD_BG = "#16213e"
CARD_BD = "#0f3460"
CYAN    = "#00d4ff"
YELLOW  = "#ffd700"
WHITE   = "#f0f0f0"
GREY    = "#888888"
GREEN   = "#00ff88"
ORANGE  = "#ff6b35"
PINK    = "#e94560"

LABEL_COLORS = [
    "#0077b6", "#0096c7", "#00b4d8", "#48cae4",
    "#90e0ef", "#0077b6", "#0096c7",
]

# ── Topic data ─────────────────────────────────────────────────────────────────
TOPICS = {
    "em_induction": {
        "title": "Electromagnetic",
        "subtitle": "Induction",
        "subject": "PHYSICS · Class XII · Chapter 6",
        "tagline": "⚡ 5–6 marks in Boards every year",
        "rows": [
            {
                "label": "Magnetic Flux",
                "formula": r"$\Phi = BA\cos\theta$",
                "diagram": "flux",
                "note": "Φ in Weber (Wb)",
            },
            {
                "label": "Faraday's Law",
                "formula": r"$\varepsilon = -N\dfrac{d\Phi}{dt}$",
                "diagram": "coil_magnet",
                "note": "ε in Volt (V)",
            },
            {
                "label": "Lenz's Law",
                "formula": r"$\varepsilon = -\dfrac{d\Phi}{dt}$",
                "diagram": "lenz",
                "note": "Opposes cause",
            },
            {
                "label": "Motional EMF",
                "formula": r"$\varepsilon = Blv$",
                "diagram": "motional",
                "note": "B·l·v",
            },
            {
                "label": "Self-Inductance",
                "formula": r"$\varepsilon = -L\dfrac{dI}{dt}$",
                "diagram": "inductor",
                "note": "L in Henry (H)",
            },
        ],
        "footer": "cbsemock.org.in  ·  Class X & XII Board Prep",
        "hashtags": "#Physics #EMI #CBSE #BoardExam2027 #ClassXII",
    },
    "current_electricity": {
        "title": "Current",
        "subtitle": "Electricity",
        "subject": "PHYSICS · Class XII · Chapter 3",
        "tagline": "⚡ 8–10 marks in Boards",
        "rows": [
            {
                "label": "Ohm's Law",
                "formula": r"$V = IR$",
                "diagram": "ohm",
                "note": "V·I·R triangle",
            },
            {
                "label": "Resistivity",
                "formula": r"$R = \rho\dfrac{l}{A}$",
                "diagram": "wire",
                "note": "ρ in Ω·m",
            },
            {
                "label": "Kirchhoff KVL",
                "formula": r"$\sum V = 0$",
                "diagram": "loop",
                "note": "Closed loop",
            },
            {
                "label": "Wheatstone",
                "formula": r"$\dfrac{P}{Q} = \dfrac{R}{S}$",
                "diagram": "bridge",
                "note": "Balanced bridge",
            },
            {
                "label": "Power",
                "formula": r"$P = \dfrac{V^2}{R} = I^2R$",
                "diagram": "power",
                "note": "P in Watt (W)",
            },
        ],
        "footer": "cbsemock.org.in  ·  Class X & XII Board Prep",
        "hashtags": "#Physics #Electricity #CBSE #BoardExam2027",
    },
}


def draw_flux_diagram(ax):
    """Magnetic flux: field lines through a tilted loop."""
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    for y in np.linspace(0.15, 0.85, 6):
        ax.annotate("", xy=(0.9, y), xytext=(0.1, y),
                    arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.2))
    # Tilted ellipse (loop)
    ellipse = mpatches.Ellipse((0.5, 0.5), 0.25, 0.55,
                                 angle=25, fill=False,
                                 edgecolor=ORANGE, lw=2.5)
    ax.add_patch(ellipse)
    ax.text(0.5, 0.05, "Φ = BAcosθ", color=YELLOW, fontsize=7,
            ha="center", fontweight="bold")


def draw_coil_magnet(ax):
    """Faraday: bar magnet approaching coil."""
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    # Coil (sine wave)
    x = np.linspace(0.4, 0.9, 200)
    y = 0.5 + 0.18 * np.sin((x - 0.4) / 0.5 * 6 * math.pi)
    ax.plot(x, y, color=ORANGE, lw=2.5)
    # Bar magnet
    ax.add_patch(FancyBboxPatch((0.05, 0.38), 0.15, 0.24,
                                 boxstyle="round,pad=0.01",
                                 facecolor="#cc0000", edgecolor="white", lw=1))
    ax.add_patch(FancyBboxPatch((0.20, 0.38), 0.15, 0.24,
                                 boxstyle="round,pad=0.01",
                                 facecolor="#0055aa", edgecolor="white", lw=1))
    ax.text(0.125, 0.50, "N", color="white", fontsize=9, ha="center",
            va="center", fontweight="bold")
    ax.text(0.275, 0.50, "S", color="white", fontsize=9, ha="center",
            va="center", fontweight="bold")
    ax.annotate("", xy=(0.38, 0.50), xytext=(0.28, 0.50),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))


def draw_lenz(ax):
    """Lenz's Law: induced current opposes."""
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    # Magnet
    ax.add_patch(FancyBboxPatch((0.02, 0.38), 0.14, 0.24,
                                 boxstyle="round,pad=0.01",
                                 facecolor="#cc0000", edgecolor="white", lw=1))
    ax.add_patch(FancyBboxPatch((0.16, 0.38), 0.14, 0.24,
                                 boxstyle="round,pad=0.01",
                                 facecolor="#0055aa", edgecolor="white", lw=1))
    ax.text(0.09, 0.50, "N", color="white", fontsize=8,
            ha="center", va="center", fontweight="bold")
    ax.text(0.23, 0.50, "S", color="white", fontsize=8,
            ha="center", va="center", fontweight="bold")
    # Arrow showing motion →
    ax.annotate("", xy=(0.42, 0.50), xytext=(0.32, 0.50),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.5))
    # Coil
    x = np.linspace(0.44, 0.78, 150)
    y = 0.5 + 0.17 * np.sin((x - 0.44) / 0.34 * 5 * math.pi)
    ax.plot(x, y, color=ORANGE, lw=2.5)
    # Induced current arrows (opposing)
    ax.annotate("", xy=(0.60, 0.72), xytext=(0.70, 0.72),
                arrowprops=dict(arrowstyle="->", color=PINK, lw=1.5))
    ax.text(0.62, 0.80, "Induced I", color=PINK, fontsize=6, ha="center")


def draw_motional(ax):
    """Motional EMF: rod moving in B field."""
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    # Rail lines
    ax.plot([0.1, 0.9], [0.25, 0.25], color=GREY, lw=2)
    ax.plot([0.1, 0.9], [0.75, 0.75], color=GREY, lw=2)
    # Moving rod
    ax.plot([0.55, 0.55], [0.25, 0.75], color=CYAN, lw=4)
    ax.annotate("", xy=(0.70, 0.50), xytext=(0.57, 0.50),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.5))
    ax.text(0.73, 0.50, "v", color=GREEN, fontsize=10,
            va="center", fontweight="bold", style="italic")
    # B field dots
    for x in [0.20, 0.35]:
        for y in [0.35, 0.50, 0.65]:
            ax.plot(x, y, "o", color=CYAN, markersize=5)
    ax.text(0.27, 0.15, "B ⊙", color=CYAN, fontsize=8, ha="center")


def draw_inductor(ax):
    """Self inductance: coil with current."""
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    # Coil
    x = np.linspace(0.1, 0.9, 400)
    y = 0.5 + 0.20 * np.sin((x - 0.1) / 0.8 * 8 * math.pi)
    ax.plot(x, y, color=ORANGE, lw=3)
    # Current arrow
    ax.annotate("", xy=(0.85, 0.30), xytext=(0.15, 0.30),
                arrowprops=dict(arrowstyle="->", color=YELLOW, lw=2))
    ax.text(0.50, 0.22, "I →", color=YELLOW, fontsize=9,
            ha="center", fontweight="bold")
    ax.text(0.50, 0.82, "L", color=CYAN, fontsize=12,
            ha="center", fontweight="bold", style="italic")


def draw_ohm(ax):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    # Triangle V I R
    triangle = plt.Polygon([[0.5, 0.85], [0.1, 0.20], [0.9, 0.20]],
                            fill=False, edgecolor=CYAN, lw=2)
    ax.add_patch(triangle)
    ax.plot([0.5, 0.5], [0.20, 0.85], color=GREY, lw=1, ls="--")
    ax.text(0.50, 0.70, "V", color=YELLOW, fontsize=14,
            ha="center", va="center", fontweight="bold")
    ax.text(0.27, 0.28, "I", color=GREEN, fontsize=12,
            ha="center", va="center", fontweight="bold")
    ax.text(0.73, 0.28, "R", color=ORANGE, fontsize=12,
            ha="center", va="center", fontweight="bold")


def draw_wire(ax):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.1, 0.35), 0.8, 0.30,
                                 boxstyle="round,pad=0.02",
                                 facecolor="#334455", edgecolor=CYAN, lw=2))
    ax.annotate("", xy=(0.85, 0.50), xytext=(0.15, 0.50),
                arrowprops=dict(arrowstyle="->", color=YELLOW, lw=2))
    ax.text(0.5, 0.80, "l", color=WHITE, fontsize=11,
            ha="center", fontweight="bold", style="italic")
    ax.annotate("", xy=(0.5, 0.33), xytext=(0.5, 0.20),
                arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.5))
    ax.text(0.5, 0.14, "A", color=GREEN, fontsize=9, ha="center")


def draw_loop(ax):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    circle = plt.Circle((0.5, 0.52), 0.33, fill=False,
                         edgecolor=CYAN, lw=2.5)
    ax.add_patch(circle)
    ax.annotate("", xy=(0.65, 0.84), xytext=(0.50, 0.85),
                arrowprops=dict(arrowstyle="->", color=CYAN, lw=2))
    # Batteries
    ax.add_patch(mpatches.Rectangle((0.42, 0.14), 0.16, 0.08,
                                      facecolor="#444", edgecolor=YELLOW, lw=1.5))
    ax.text(0.5, 0.18, "ε", color=YELLOW, fontsize=10,
            ha="center", va="center", fontweight="bold")
    ax.text(0.5, 0.06, "ΣV = 0", color=GREEN, fontsize=8, ha="center")


def draw_bridge(ax):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    pts = {"A": (0.5, 0.88), "B": (0.15, 0.50),
           "C": (0.85, 0.50), "D": (0.5, 0.12)}
    for (a, b), label in [
        (("A", "B"), "P"), (("A", "C"), "Q"),
        (("B", "D"), "R"), (("C", "D"), "S"),
    ]:
        x1, y1 = pts[a]; x2, y2 = pts[b]
        ax.plot([x1, x2], [y1, y2], color=CYAN, lw=2)
        ax.text((x1+x2)/2 - 0.07, (y1+y2)/2, label,
                color=YELLOW, fontsize=9, fontweight="bold")
    # Galvanometer (B-C)
    ax.plot([pts["B"][0], pts["C"][0]], [pts["B"][1], pts["C"][1]],
            color=GREEN, lw=1.5, ls="--")
    ax.text(0.5, 0.52, "G", color=GREEN, fontsize=8, ha="center")
    for name, (x, y) in pts.items():
        ax.plot(x, y, "o", color=WHITE, markersize=7)
        ax.text(x, y + 0.06, name, color=WHITE, fontsize=8, ha="center")


def draw_power(ax):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    # Bulb symbol
    circle = plt.Circle((0.5, 0.60), 0.22, fill=False,
                         edgecolor=YELLOW, lw=2.5)
    ax.add_patch(circle)
    ax.plot([0.36, 0.64], [0.44, 0.76], color=YELLOW, lw=2)
    ax.plot([0.64, 0.36], [0.44, 0.76], color=YELLOW, lw=2)
    ax.plot([0.5, 0.5], [0.38, 0.22], color=GREY, lw=2)
    ax.plot([0.5, 0.5], [0.82, 0.95], color=GREY, lw=2)
    ax.text(0.5, 0.12, "P = VI = I²R", color=YELLOW, fontsize=7,
            ha="center", fontweight="bold")


DIAGRAM_FNS = {
    "flux": draw_flux_diagram,
    "coil_magnet": draw_coil_magnet,
    "lenz": draw_lenz,
    "motional": draw_motional,
    "inductor": draw_inductor,
    "ohm": draw_ohm,
    "wire": draw_wire,
    "loop": draw_loop,
    "bridge": draw_bridge,
    "power": draw_power,
}


def generate_card(topic_id: str) -> Path:
    data = TOPICS[topic_id]
    rows = data["rows"]
    n    = len(rows)

    fig = plt.figure(figsize=(W_IN, H_IN), facecolor=BG)

    # Layout fractions
    top_frac   = 0.18   # title area
    footer_frac = 0.07
    row_frac   = (1.0 - top_frac - footer_frac) / n

    # ── Title block ────────────────────────────────────────────────────────────
    ax_title = fig.add_axes([0, 1 - top_frac, 1, top_frac])
    ax_title.set_facecolor(BG)
    ax_title.axis("off")

    ax_title.text(0.5, 0.80, data["title"], color=CYAN,
                  fontsize=28, fontweight="bold", ha="center", va="top",
                  transform=ax_title.transAxes)
    ax_title.text(0.5, 0.52, data["subtitle"], color=WHITE,
                  fontsize=26, fontweight="bold", ha="center", va="top",
                  transform=ax_title.transAxes)
    ax_title.text(0.5, 0.25, f"── {data['subject']} ──", color=GREY,
                  fontsize=8, ha="center", va="top",
                  transform=ax_title.transAxes)
    ax_title.text(0.5, 0.08, data["tagline"], color=YELLOW,
                  fontsize=8, ha="center", va="top",
                  transform=ax_title.transAxes)

    # ── Formula rows ───────────────────────────────────────────────────────────
    for i, row in enumerate(rows):
        y_bottom = footer_frac + (n - 1 - i) * row_frac
        pad = 0.008

        # Row background card
        ax_card = fig.add_axes([pad, y_bottom + pad,
                                 1 - 2*pad, row_frac - 2*pad])
        ax_card.set_facecolor(CARD_BG)
        for spine in ax_card.spines.values():
            spine.set_edgecolor(LABEL_COLORS[i % len(LABEL_COLORS)])
            spine.set_linewidth(1.5)
        ax_card.set_xticks([]); ax_card.set_yticks([])

        # Label pill (left ~30%)
        ax_label = fig.add_axes([pad*2, y_bottom + pad*2,
                                  0.30, row_frac - pad*4])
        ax_label.set_facecolor(LABEL_COLORS[i % len(LABEL_COLORS)])
        ax_label.axis("off")
        ax_label.text(0.5, 0.65, row["label"],
                      color=WHITE, fontsize=8.5, fontweight="bold",
                      ha="center", va="center",
                      transform=ax_label.transAxes, wrap=True)
        ax_label.text(0.5, 0.25, row["note"],
                      color="#dddddd", fontsize=6.5,
                      ha="center", va="center",
                      transform=ax_label.transAxes)

        # Diagram (middle ~35%)
        ax_diag = fig.add_axes([0.31 + pad, y_bottom + pad*2,
                                  0.34, row_frac - pad*4])
        ax_diag.set_facecolor(CARD_BG)
        ax_diag.axis("off")
        draw_fn = DIAGRAM_FNS.get(row["diagram"])
        if draw_fn:
            draw_fn(ax_diag)

        # Formula (right ~33%)
        ax_form = fig.add_axes([0.66, y_bottom + pad,
                                  0.34 - pad, row_frac - pad*2])
        ax_form.set_facecolor(CARD_BG)
        ax_form.axis("off")
        ax_form.text(0.5, 0.52, row["formula"],
                     color=YELLOW, fontsize=14, fontweight="bold",
                     ha="center", va="center",
                     transform=ax_form.transAxes,
                     usetex=False)

    # ── Footer ─────────────────────────────────────────────────────────────────
    ax_foot = fig.add_axes([0, 0, 1, footer_frac])
    ax_foot.set_facecolor("#0d0d1a")
    ax_foot.axis("off")
    # Top border line
    ax_foot.axhline(0.92, color=CYAN, lw=1.5)
    ax_foot.text(0.5, 0.58, data["footer"],
                 color=CYAN, fontsize=9, fontweight="bold",
                 ha="center", va="center",
                 transform=ax_foot.transAxes)
    ax_foot.text(0.5, 0.18, data["hashtags"],
                 color=GREY, fontsize=7,
                 ha="center", va="center",
                 transform=ax_foot.transAxes)

    out_path = OUT_DIR / f"{topic_id}_card.png"
    fig.savefig(out_path, dpi=DPI, bbox_inches="tight",
                facecolor=BG, pad_inches=0)
    plt.close(fig)
    print(f"[OK] Saved: {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="em_induction")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.all:
        for t in TOPICS:
            generate_card(t)
    else:
        generate_card(args.topic)


if __name__ == "__main__":
    main()
