#!/usr/bin/env python3
"""
generate_formula_card_v2.py  —  VIBRANCE UPGRADE SAMPLE
────────────────────────────────────────────────────────
Multi-formula reference card (1080×1350) with:
  • Neon-glow formula boxes  (cyan border + inner glow fill)
  • Gradient row backgrounds
  • Yellow "Formula Flash" pill + subject/chapter tags in header
  • Brighter label pills with accent edge
  • "SAVE FOR REVISION • cbsemock.org.in" footer bar

Usage:
  python3 generate_formula_card_v2.py --topic em_induction
"""

import argparse, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path

OUT_DIR   = Path(__file__).parent / "formula-posts" / "images"
LOGO_PATH = Path(__file__).parent / "formula-posts" / "_cbsemock_logo_dark.png"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W_IN, H_IN = 10.80, 13.50
DPI = 100

# ── Colour palette ──────────────────────────────────────────────────────────────
BG          = "#050e1f"      # near-black navy
ROW_BG      = "#0a1628"      # row card bg
ROW_BG2     = "#0d1e38"      # slight gradient end
CYAN        = "#00d4ff"      # neon cyan
CYAN_DIM    = "#0088aa"
PURPLE      = "#8b5cf6"      # neon purple
YELLOW      = "#f9c820"      # brand yellow
ORANGE      = "#ff6b35"
WHITE       = "#f0f4ff"
GREY        = "#6a7f99"
GREEN       = "#00ff88"
PINK        = "#ff4da6"
BLUE_PILL   = "#1565c0"

# Per-row accent colours — alternating cyan/purple/blue family
ACCENTS = ["#00d4ff", "#8b5cf6", "#00d4ff", "#8b5cf6", "#00d4ff"]

TOPICS = {
    "em_induction": {
        "subject":      "Physics",
        "chapter_tag":  "Chapter 6 · Class XII",
        "title_line1":  "Electromagnetic",
        "title_line2":  "Induction",
        "board_note":   "⚡  5–6 marks · Every Board Exam",
        "rows": [
            {"label": "Magnetic Flux",   "formula": r"$\Phi = BA\cos\theta$",              "diagram": "flux",        "note": "Weber (Wb)"},
            {"label": "Faraday's Law",   "formula": r"$\varepsilon = -N\dfrac{d\Phi}{dt}$","diagram": "coil_magnet", "note": "Volt (V)"},
            {"label": "Lenz's Law",      "formula": r"$\varepsilon = -\dfrac{d\Phi}{dt}$", "diagram": "lenz",        "note": "Opposes cause"},
            {"label": "Motional EMF",    "formula": r"$\varepsilon = Blv$",                "diagram": "motional",    "note": "B·l·v"},
            {"label": "Self-Inductance", "formula": r"$\varepsilon = -L\dfrac{dI}{dt}$",   "diagram": "inductor",    "note": "Henry (H)"},
        ],
        "cta":      "SAVE FOR REVISION",
        "hashtags": "#Physics #EMI #CBSE #BoardExam2027 #ClassXII",
    },
}

# ── Diagram functions (same as v1, unchanged) ──────────────────────────────────
def draw_flux_diagram(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    for y in np.linspace(0.15, 0.85, 6):
        ax.annotate("", xy=(0.9,y), xytext=(0.1,y),
                    arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.4))
    el = mpatches.Ellipse((0.5,0.5), 0.25, 0.55, angle=25,
                           fill=False, edgecolor=ORANGE, lw=2.5)
    ax.add_patch(el)

def draw_coil_magnet(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.04,0.38),0.14,0.24, boxstyle="round,pad=0.01",
                                 facecolor="#cc0000", edgecolor="white", lw=1))
    ax.add_patch(FancyBboxPatch((0.18,0.38),0.14,0.24, boxstyle="round,pad=0.01",
                                 facecolor="#0055aa", edgecolor="white", lw=1))
    ax.text(0.11,0.50,"N",color="white",fontsize=9,ha="center",va="center",fontweight="bold")
    ax.text(0.25,0.50,"S",color="white",fontsize=9,ha="center",va="center",fontweight="bold")
    ax.annotate("", xy=(0.40,0.50), xytext=(0.34,0.50),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
    x = np.linspace(0.42,0.92,200)
    y = 0.5 + 0.18*np.sin((x-0.42)/0.5*6*math.pi)
    ax.plot(x, y, color=ORANGE, lw=2.5)

def draw_lenz(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.02,0.38),0.13,0.24, boxstyle="round,pad=0.01",
                                 facecolor="#cc0000", edgecolor="white", lw=1))
    ax.add_patch(FancyBboxPatch((0.15,0.38),0.13,0.24, boxstyle="round,pad=0.01",
                                 facecolor="#0055aa", edgecolor="white", lw=1))
    ax.text(0.085,0.50,"N",color="white",fontsize=8,ha="center",va="center",fontweight="bold")
    ax.text(0.215,0.50,"S",color="white",fontsize=8,ha="center",va="center",fontweight="bold")
    ax.annotate("", xy=(0.42,0.50), xytext=(0.30,0.50),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.5))
    x = np.linspace(0.44,0.78,150)
    y = 0.5 + 0.17*np.sin((x-0.44)/0.34*5*math.pi)
    ax.plot(x, y, color=ORANGE, lw=2.5)
    ax.annotate("", xy=(0.60,0.74), xytext=(0.70,0.74),
                arrowprops=dict(arrowstyle="->", color=PINK, lw=1.5))
    ax.text(0.63,0.82,"Induced I",color=PINK,fontsize=5.5,ha="center")

def draw_motional(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot([0.1,0.9],[0.25,0.25],color=GREY,lw=2)
    ax.plot([0.1,0.9],[0.75,0.75],color=GREY,lw=2)
    ax.plot([0.55,0.55],[0.25,0.75],color=CYAN,lw=4)
    ax.annotate("", xy=(0.72,0.50), xytext=(0.57,0.50),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.5))
    ax.text(0.76,0.50,"v",color=GREEN,fontsize=10,va="center",fontweight="bold",style="italic")
    for x in [0.20,0.35]:
        for y in [0.35,0.50,0.65]:
            ax.plot(x,y,"o",color=CYAN,markersize=5)
    ax.text(0.27,0.14,"B ⊙",color=CYAN,fontsize=8,ha="center")

def draw_inductor(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    x = np.linspace(0.1,0.9,400)
    y = 0.5 + 0.20*np.sin((x-0.1)/0.8*8*math.pi)
    ax.plot(x,y,color=ORANGE,lw=3)
    ax.annotate("", xy=(0.85,0.28), xytext=(0.15,0.28),
                arrowprops=dict(arrowstyle="->", color=YELLOW, lw=2))
    ax.text(0.50,0.82,"L",color=CYAN,fontsize=12,ha="center",fontweight="bold",style="italic")

DIAGRAM_FNS = {
    "flux": draw_flux_diagram, "coil_magnet": draw_coil_magnet,
    "lenz": draw_lenz, "motional": draw_motional, "inductor": draw_inductor,
}

# ── Neon glow helper ────────────────────────────────────────────────────────────
def draw_neon_box(ax, x, y, w, h, color, lw_outer=4, lw_inner=1.5):
    """Draw a rounded rect with a glowing neon border (outer dim + inner bright)."""
    # Outer glow (wide, dim, alpha)
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.012",
        facecolor="none",
        edgecolor=color, linewidth=lw_outer,
        alpha=0.25, transform=ax.transAxes, clip_on=False))
    # Inner bright line
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.012",
        facecolor=(0, 0, 0, 0.35),
        edgecolor=color, linewidth=lw_inner,
        alpha=0.95, transform=ax.transAxes, clip_on=False))

# ── Header ──────────────────────────────────────────────────────────────────────
def draw_header(ax, subject, chapter_tag, title1, title2, board_note):
    ax.set_facecolor(BG); ax.axis("off")
    ax.set_xlim(0,1); ax.set_ylim(0,1)

    # Logo — horizontal strip, left-aligned
    if LOGO_PATH.exists():
        try:
            logo_img = matplotlib.image.imread(str(LOGO_PATH))
            li = ax.inset_axes([0.01, 0.55, 0.42, 0.40])
            li.imshow(logo_img); li.axis("off")
        except Exception:
            ax.text(0.02, 0.80, "CBSEMock", color=CYAN, fontsize=16, fontweight="bold",
                    va="center", transform=ax.transAxes)

    # "Formula Flash" yellow pill — centre-right of logo row
    ax.add_patch(FancyBboxPatch((0.44, 0.60), 0.26, 0.32,
        boxstyle="round,pad=0.02", facecolor=YELLOW,
        edgecolor="none", transform=ax.transAxes))
    ax.text(0.57, 0.76, "Formula Flash", color="#111111",
            fontsize=9, fontweight="bold", ha="center", va="center",
            transform=ax.transAxes)

    # Subject pill — right side
    subj_colors = {"Physics":"#1565c0","Chemistry":"#2e7d32",
                   "Mathematics":"#6a1b9a","Biology":"#c62828"}
    sc = subj_colors.get(subject, "#1565c0")
    ax.add_patch(FancyBboxPatch((0.72, 0.60), 0.27, 0.32,
        boxstyle="round,pad=0.02", facecolor=sc,
        edgecolor="none", transform=ax.transAxes))
    ax.text(0.855, 0.76, subject, color=WHITE,
            fontsize=9, fontweight="bold", ha="center", va="center",
            transform=ax.transAxes)

    # Title row
    ax.text(0.03, 0.34, title1 + " " + title2, color=WHITE,
            fontsize=22, fontweight="bold", va="center", transform=ax.transAxes)

    # Board note + chapter tag
    ax.text(0.03, 0.10, board_note + "   |   " + chapter_tag,
            color=YELLOW, fontsize=8.5, va="center", transform=ax.transAxes)

    # Bottom divider — cyan glow line
    ax.axhline(0.01, color=CYAN, lw=2.5, alpha=0.8)

# ── Footer ───────────────────────────────────────────────────────────────────────
def draw_footer(ax, cta, hashtags):
    ax.set_facecolor("#030b18"); ax.axis("off")
    # Top cyan accent line
    ax.axhline(0.97, color=CYAN, lw=2, alpha=0.6)
    # CTA pill
    ax.add_patch(FancyBboxPatch((0.05, 0.42), 0.90, 0.42,
        boxstyle="round,pad=0.02", facecolor=YELLOW,
        edgecolor="none", transform=ax.transAxes))
    ax.text(0.50, 0.63, f"{cta}  •  cbsemock.org.in",
            color="#111111", fontsize=11, fontweight="bold",
            ha="center", va="center", transform=ax.transAxes)
    ax.text(0.50, 0.15, hashtags, color=GREY, fontsize=6.5,
            ha="center", va="center", transform=ax.transAxes)

# ── Main card generator ──────────────────────────────────────────────────────────
def generate_card(topic_id: str) -> Path:
    data = TOPICS[topic_id]
    rows = data["rows"]
    n    = len(rows)

    fig = plt.figure(figsize=(W_IN, H_IN), facecolor=BG)

    hdr_frac  = 0.130
    foot_frac = 0.080
    rows_frac = 1.0 - hdr_frac - foot_frac
    row_h     = rows_frac / n

    # ── Header
    ax_hdr = fig.add_axes([0, 1 - hdr_frac, 1, hdr_frac])
    draw_header(ax_hdr, data["subject"], data["chapter_tag"],
                data["title_line1"], data["title_line2"], data["board_note"])

    # ── Rows
    for i, row in enumerate(rows):
        yb     = foot_frac + (n - 1 - i) * row_h
        pad    = 0.007
        accent = ACCENTS[i % len(ACCENTS)]

        # Row card — slightly lighter background
        ax_c = fig.add_axes([pad, yb + pad, 1 - 2*pad, row_h - 2*pad])
        ax_c.set_facecolor(ROW_BG2)
        for sp in ax_c.spines.values():
            sp.set_edgecolor(accent)
            sp.set_linewidth(1.8)
            sp.set_alpha(0.7)
        ax_c.set_xticks([]); ax_c.set_yticks([])

        # ── Label pill (28%) — gradient-like fill with accent edge
        ax_l = fig.add_axes([pad*2, yb + pad*2, 0.27, row_h - pad*4])
        ax_l.set_facecolor(BG); ax_l.axis("off")
        ax_l.set_xlim(0,1); ax_l.set_ylim(0,1)
        # Dark pill with bright accent border
        ax_l.add_patch(FancyBboxPatch((0.05,0.05), 0.90, 0.90,
            boxstyle="round,pad=0.04",
            facecolor="#0d1e38", edgecolor=accent, linewidth=2.5, zorder=1))
        # Accent top stripe
        ax_l.add_patch(FancyBboxPatch((0.05,0.72), 0.90, 0.23,
            boxstyle="round,pad=0.02",
            facecolor=accent, edgecolor="none", alpha=0.25, zorder=2))
        ax_l.text(0.5, 0.60, row["label"], color=WHITE, fontsize=10,
                  fontweight="bold", ha="center", va="center",
                  transform=ax_l.transAxes, zorder=3)
        ax_l.text(0.5, 0.26, row["note"], color=accent, fontsize=8,
                  ha="center", va="center", transform=ax_l.transAxes, zorder=3)

        # ── Diagram (33%)
        ax_d = fig.add_axes([0.28 + pad, yb + pad*2, 0.33, row_h - pad*4])
        ax_d.set_facecolor(ROW_BG2); ax_d.axis("off")
        fn = DIAGRAM_FNS.get(row["diagram"])
        if fn: fn(ax_d)

        # ── Formula box (37%) — NEON GLOW
        fx = 0.62
        fw = 0.37 - pad
        ax_f = fig.add_axes([fx, yb + pad, fw, row_h - pad*2])
        ax_f.set_facecolor("#060f20"); ax_f.axis("off")
        ax_f.set_xlim(0,1); ax_f.set_ylim(0,1)

        # Neon border via patch inside axes
        ax_f.add_patch(FancyBboxPatch((0.04, 0.08), 0.92, 0.84,
            boxstyle="round,pad=0.04",
            facecolor="#000d1a", edgecolor=accent,
            linewidth=3.5, alpha=0.9, zorder=1))
        # Faint inner glow fill
        ax_f.add_patch(FancyBboxPatch((0.04, 0.08), 0.92, 0.84,
            boxstyle="round,pad=0.04",
            facecolor=accent, edgecolor="none",
            linewidth=0, alpha=0.06, zorder=2))

        ax_f.text(0.5, 0.50, row["formula"], color=YELLOW,
                  fontsize=15, fontweight="bold",
                  ha="center", va="center", transform=ax_f.transAxes, zorder=3)

    # ── Footer
    ax_ft = fig.add_axes([0, 0, 1, foot_frac])
    draw_footer(ax_ft, data["cta"], data["hashtags"])

    out_path = OUT_DIR / f"{topic_id}_card_v2.png"
    fig.savefig(out_path, dpi=DPI, bbox_inches="tight",
                facecolor=BG, pad_inches=0)
    plt.close(fig)
    print(f"[OK] {out_path}")
    return out_path

TOPICS.update({
    "genetics": {
        "subject":      "Biology",
        "chapter_tag":  "Chapter 5 · Class XII",
        "title_line1":  "Principles of",
        "title_line2":  "Inheritance",
        "board_note":   "🧬  5–6 marks · Every Board Exam",
        "rows": [
            {"label": "Monohybrid Ratio",   "formula": r"$3 : 1$",                             "diagram": "flux",        "note": "F₂ phenotype ratio"},
            {"label": "Dihybrid Ratio",     "formula": r"$9 : 3 : 3 : 1$",                     "diagram": "coil_magnet", "note": "F₂ phenotype ratio"},
            {"label": "Hardy-Weinberg",     "formula": r"$p^2 + 2pq + q^2 = 1$",              "diagram": "lenz",        "note": "Allele frequency"},
            {"label": "Chi-Square",         "formula": r"$\chi^2 = \sum\dfrac{(O-E)^2}{E}$",   "diagram": "motional",    "note": "Goodness of fit"},
            {"label": "Mutation Rate",      "formula": r"$\mu = \dfrac{\text{mutations}}{\text{gametes}}$", "diagram": "inductor", "note": "per generation"},
        ],
        "cta":      "SAVE FOR REVISION",
        "hashtags": "#Biology #Genetics #CBSE #BoardExam2027 #ClassXII",
    },
    "chemical_kinetics": {
        "subject":      "Chemistry",
        "chapter_tag":  "Chapter 3 · Class XII",
        "title_line1":  "Chemical",
        "title_line2":  "Kinetics",
        "board_note":   "⚗️  5–6 marks · Every Board Exam",
        "rows": [
            {"label": "Rate Law",           "formula": r"$r = k[A]^m[B]^n$",                   "diagram": "flux",        "note": "mol L⁻¹ s⁻¹"},
            {"label": "1st Order",          "formula": r"$k = \dfrac{2.303}{t}\log\dfrac{[A]_0}{[A]}$", "diagram": "coil_magnet", "note": "s⁻¹"},
            {"label": "Half Life (1st)",    "formula": r"$t_{1/2} = \dfrac{0.693}{k}$",         "diagram": "lenz",        "note": "Independent of [A]"},
            {"label": "Arrhenius Eq.",      "formula": r"$k = A e^{-E_a/RT}$",                  "diagram": "motional",    "note": "Activation energy"},
            {"label": "Activation Energy",  "formula": r"$\ln\dfrac{k_2}{k_1} = \dfrac{E_a}{R}\left(\dfrac{1}{T_1}-\dfrac{1}{T_2}\right)$", "diagram": "inductor", "note": "J mol⁻¹"},
        ],
        "cta":      "SAVE FOR REVISION",
        "hashtags": "#Chemistry #Kinetics #CBSE #BoardExam2027 #ClassXII",
    },
    "calculus": {
        "subject":      "Mathematics",
        "chapter_tag":  "Chapter 5–7 · Class XII",
        "title_line1":  "Calculus",
        "title_line2":  "Quick Reference",
        "board_note":   "📐  12–15 marks · Every Board Exam",
        "rows": [
            {"label": "Chain Rule",         "formula": r"$\dfrac{dy}{dx} = \dfrac{dy}{du}\cdot\dfrac{du}{dx}$", "diagram": "flux",        "note": "Composite fn"},
            {"label": "Product Rule",       "formula": r"$(uv)' = u'v + uv'$",                 "diagram": "coil_magnet", "note": "Leibniz rule"},
            {"label": "Integration by Parts","formula": r"$\int u\,dv = uv - \int v\,du$",      "diagram": "lenz",        "note": "ILATE order"},
            {"label": "Definite Integral",  "formula": r"$\int_a^b f(x)\,dx = F(b)-F(a)$",     "diagram": "motional",    "note": "Newton-Leibniz"},
            {"label": "Area Under Curve",   "formula": r"$A = \int_a^b |f(x)|\,dx$",           "diagram": "inductor",    "note": "sq. units"},
        ],
        "cta":      "SAVE FOR REVISION",
        "hashtags": "#Maths #Calculus #CBSE #BoardExam2027 #ClassXII",
    },
    "boolean_algebra": {
        "subject":      "CS",
        "chapter_tag":  "Chapter 3 · Class XII",
        "title_line1":  "Boolean Algebra",
        "title_line2":  "& Logic Gates",
        "board_note":   "💻  4–5 marks · Every Board Exam",
        "rows": [
            {"label": "De Morgan I",        "formula": r"$\overline{A+B} = \bar{A}\cdot\bar{B}$","diagram": "flux",        "note": "NOR = AND of NOT"},
            {"label": "De Morgan II",       "formula": r"$\overline{A\cdot B} = \bar{A}+\bar{B}$","diagram": "coil_magnet","note": "NAND = OR of NOT"},
            {"label": "Absorption Law",     "formula": r"$A + AB = A$",                         "diagram": "lenz",        "note": "Simplification"},
            {"label": "Half Adder SOP",     "formula": r"$S=A\oplus B,\ C=A\cdot B$",           "diagram": "motional",    "note": "Sum & Carry"},
            {"label": "POS / SOP",          "formula": r"$f=\sum m_i = \prod M_i$",             "diagram": "inductor",    "note": "Canonical forms"},
        ],
        "cta":      "SAVE FOR REVISION",
        "hashtags": "#ComputerScience #BooleanAlgebra #CBSE #BoardExam2027 #ClassXII",
    },
})
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="em_induction")
    args = parser.parse_args()
    generate_card(args.topic)

if __name__ == "__main__":
    main()

# ── Additional topic data ────────────────────────────────────────────────────────
