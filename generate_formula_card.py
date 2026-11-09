#!/usr/bin/env python3
"""
generate_formula_card.py
─────────────────────────
Generates a branded formula card image (1080×1350 — Instagram portrait)
with full CBSEMock branding:
  • Top: CBSEMock logo strip (from social image asset)
  • Middle: multi-row formula table with actual physics diagrams
  • Bottom: yellow CTA pill + globe + cbsemock.org.in

Usage:
  python3 generate_formula_card.py --topic em_induction
  python3 generate_formula_card.py --all
"""

import argparse
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.image import imread
from pathlib import Path
from PIL import Image
import io

OUT_DIR   = Path(__file__).parent / "formula-posts" / "images"
LOGO_PATH = Path(__file__).parent / "formula-posts" / "_cbsemock_logo_dark.png"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Canvas: 1080×1350 at 100 dpi
W_IN, H_IN = 10.80, 13.50
DPI = 100

# CBSEMock brand colours
BRAND_NAVY  = "#0a1628"   # deep navy (bg)
BRAND_BLUE  = "#1565c0"   # royal blue accent
BRAND_CYAN  = "#00b4d8"   # bright cyan (logo colour)
BRAND_YELL  = "#f9c820"   # brand yellow
BRAND_ORNG  = "#ff6b35"   # orange accent
WHITE       = "#f0f0f0"
GREY        = "#8899aa"
GREEN       = "#00e676"
PINK        = "#ff4081"

# Row label pill colours (blue family matching brand)
LABEL_COLS = ["#0d47a1","#1565c0","#1976d2","#1e88e5","#2196f3","#1976d2"]

TOPICS = {
    "em_induction": {
        "chapter_tag": "Chapter 6 · Class XII",
        "title_line1": "Electromagnetic",
        "title_line2": "Induction",
        "board_note":  "⚡  5–6 marks · Every Board Exam",
        "rows": [
            {"label": "Magnetic Flux",   "formula": r"$\Phi = BA\cos\theta$",             "diagram": "flux",        "note": "Weber (Wb)"},
            {"label": "Faraday's Law",   "formula": r"$\varepsilon = -N\dfrac{d\Phi}{dt}$","diagram": "coil_magnet", "note": "Volt (V)"},
            {"label": "Lenz's Law",      "formula": r"$\varepsilon = -\dfrac{d\Phi}{dt}$", "diagram": "lenz",        "note": "Opposes cause"},
            {"label": "Motional EMF",    "formula": r"$\varepsilon = Blv$",                "diagram": "motional",    "note": "B·l·v"},
            {"label": "Self-Inductance", "formula": r"$\varepsilon = -L\dfrac{dI}{dt}$",   "diagram": "inductor",    "note": "Henry (H)"},
        ],
        "cta":      "Practice EMI Questions →",
        "hashtags": "#Physics #EMI #CBSE #BoardExam2027 #ClassXII",
    },
    "current_electricity": {
        "chapter_tag": "Chapter 3 · Class XII",
        "title_line1": "Current",
        "title_line2": "Electricity",
        "board_note":  "⚡  8–10 marks · Every Board Exam",
        "rows": [
            {"label": "Ohm's Law",    "formula": r"$V = IR$",                       "diagram": "ohm",    "note": "V·I·R"},
            {"label": "Resistivity",  "formula": r"$R = \rho\dfrac{l}{A}$",          "diagram": "wire",   "note": "Ω·m"},
            {"label": "KVL",          "formula": r"$\sum V = 0$",                   "diagram": "loop",   "note": "Closed loop"},
            {"label": "Wheatstone",   "formula": r"$\dfrac{P}{Q}=\dfrac{R}{S}$",    "diagram": "bridge", "note": "Balanced bridge"},
            {"label": "Power",        "formula": r"$P = \dfrac{V^2}{R} = I^2R$",    "diagram": "power",  "note": "Watt (W)"},
        ],
        "cta":      "Practice Electricity Questions →",
        "hashtags": "#Physics #CurrentElectricity #CBSE #BoardExam2027",
    },
    "newton_laws": {
        "chapter_tag": "Chapter 5 · Class XI",
        "title_line1": "Laws of",
        "title_line2": "Motion",
        "board_note":  "⚡  6–8 marks · Class XI & XII",
        "rows": [
            {"label": "Newton 1st",   "formula": r"$F_{net}=0 \Rightarrow a=0$",     "diagram": "newton1",  "note": "Inertia"},
            {"label": "Newton 2nd",   "formula": r"$F = ma$",                         "diagram": "newton2",  "note": "N = kg·m/s²"},
            {"label": "Newton 3rd",   "formula": r"$F_{AB}=-F_{BA}$",                "diagram": "newton3",  "note": "Action-Reaction"},
            {"label": "Momentum",     "formula": r"$p = mv$",                         "diagram": "momentum", "note": "kg·m/s"},
            {"label": "Impulse",      "formula": r"$J = F\Delta t = \Delta p$",       "diagram": "impulse",  "note": "N·s"},
        ],
        "cta":      "Practice Motion Questions →",
        "hashtags": "#Physics #NewtonLaws #CBSE #BoardExam2027",
    },
}

# ─────────────────────────── diagram functions ────────────────────────────────

def draw_flux_diagram(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    for y in np.linspace(0.15, 0.85, 6):
        ax.annotate("", xy=(0.9,y), xytext=(0.1,y),
                    arrowprops=dict(arrowstyle="->", color=BRAND_CYAN, lw=1.2))
    el = mpatches.Ellipse((0.5,0.5), 0.25, 0.55, angle=25,
                           fill=False, edgecolor=BRAND_ORNG, lw=2.5)
    ax.add_patch(el)
    ax.text(0.5,0.05, "Φ = BAcosθ", color=BRAND_YELL, fontsize=6.5,
            ha="center", fontweight="bold")

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
    ax.plot(x, y, color=BRAND_ORNG, lw=2.5)

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
    ax.plot(x, y, color=BRAND_ORNG, lw=2.5)
    ax.annotate("", xy=(0.60,0.74), xytext=(0.70,0.74),
                arrowprops=dict(arrowstyle="->", color=PINK, lw=1.5))
    ax.text(0.63,0.82,"Induced I",color=PINK,fontsize=5.5,ha="center")

def draw_motional(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot([0.1,0.9],[0.25,0.25],color=GREY,lw=2)
    ax.plot([0.1,0.9],[0.75,0.75],color=GREY,lw=2)
    ax.plot([0.55,0.55],[0.25,0.75],color=BRAND_CYAN,lw=4)
    ax.annotate("", xy=(0.72,0.50), xytext=(0.57,0.50),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.5))
    ax.text(0.76,0.50,"v",color=GREEN,fontsize=10,va="center",fontweight="bold",style="italic")
    for x in [0.20,0.35]:
        for y in [0.35,0.50,0.65]:
            ax.plot(x,y,"o",color=BRAND_CYAN,markersize=5)
    ax.text(0.27,0.14,"B ⊙",color=BRAND_CYAN,fontsize=8,ha="center")

def draw_inductor(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    x = np.linspace(0.1,0.9,400)
    y = 0.5 + 0.20*np.sin((x-0.1)/0.8*8*math.pi)
    ax.plot(x,y,color=BRAND_ORNG,lw=3)
    ax.annotate("", xy=(0.85,0.28), xytext=(0.15,0.28),
                arrowprops=dict(arrowstyle="->", color=BRAND_YELL, lw=2))
    ax.text(0.50,0.20,"I →",color=BRAND_YELL,fontsize=9,ha="center",fontweight="bold")
    ax.text(0.50,0.82,"L",color=BRAND_CYAN,fontsize=12,ha="center",fontweight="bold",style="italic")

def draw_ohm(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    t = plt.Polygon([[0.5,0.86],[0.1,0.20],[0.9,0.20]],
                    fill=False,edgecolor=BRAND_CYAN,lw=2)
    ax.add_patch(t)
    ax.plot([0.5,0.5],[0.20,0.86],color=GREY,lw=1,ls="--")
    ax.text(0.50,0.68,"V",color=BRAND_YELL,fontsize=14,ha="center",va="center",fontweight="bold")
    ax.text(0.27,0.28,"I",color=GREEN,fontsize=12,ha="center",va="center",fontweight="bold")
    ax.text(0.73,0.28,"R",color=BRAND_ORNG,fontsize=12,ha="center",va="center",fontweight="bold")

def draw_wire(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.1,0.35),0.8,0.30, boxstyle="round,pad=0.02",
                                 facecolor="#1a2a40", edgecolor=BRAND_CYAN, lw=2))
    ax.annotate("", xy=(0.85,0.50), xytext=(0.15,0.50),
                arrowprops=dict(arrowstyle="->", color=BRAND_YELL, lw=2))
    ax.text(0.5,0.80,"l",color=WHITE,fontsize=11,ha="center",fontweight="bold",style="italic")
    ax.text(0.5,0.14,"A",color=GREEN,fontsize=9,ha="center")

def draw_loop(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    c = plt.Circle((0.5,0.52),0.33,fill=False,edgecolor=BRAND_CYAN,lw=2.5)
    ax.add_patch(c)
    ax.annotate("", xy=(0.65,0.84), xytext=(0.50,0.85),
                arrowprops=dict(arrowstyle="->", color=BRAND_CYAN, lw=2))
    ax.add_patch(mpatches.Rectangle((0.42,0.14),0.16,0.08,
                                     facecolor="#333", edgecolor=BRAND_YELL, lw=1.5))
    ax.text(0.5,0.18,"ε",color=BRAND_YELL,fontsize=10,ha="center",va="center",fontweight="bold")

def draw_bridge(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    pts = {"A":(0.5,0.88),"B":(0.15,0.50),"C":(0.85,0.50),"D":(0.5,0.12)}
    for (a,b),lbl in [(("A","B"),"P"),(("A","C"),"Q"),(("B","D"),"R"),(("C","D"),"S")]:
        x1,y1=pts[a]; x2,y2=pts[b]
        ax.plot([x1,x2],[y1,y2],color=BRAND_CYAN,lw=2)
        ax.text((x1+x2)/2-0.07,(y1+y2)/2,lbl,color=BRAND_YELL,fontsize=9,fontweight="bold")
    ax.plot([pts["B"][0],pts["C"][0]],[pts["B"][1],pts["C"][1]],
            color=GREEN,lw=1.5,ls="--")
    ax.text(0.5,0.52,"G",color=GREEN,fontsize=8,ha="center")
    for _,(x,y) in pts.items():
        ax.plot(x,y,"o",color=WHITE,markersize=7)

def draw_power(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    c = plt.Circle((0.5,0.60),0.22,fill=False,edgecolor=BRAND_YELL,lw=2.5)
    ax.add_patch(c)
    ax.plot([0.36,0.64],[0.44,0.76],color=BRAND_YELL,lw=2)
    ax.plot([0.64,0.36],[0.44,0.76],color=BRAND_YELL,lw=2)
    ax.plot([0.5,0.5],[0.38,0.22],color=GREY,lw=2)
    ax.plot([0.5,0.5],[0.82,0.95],color=GREY,lw=2)

def draw_newton1(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    # Ball moving at constant velocity (no net force)
    ax.add_patch(plt.Circle((0.25,0.55),0.12,color=BRAND_CYAN,zorder=3))
    ax.annotate("", xy=(0.75,0.55), xytext=(0.40,0.55),
                arrowprops=dict(arrowstyle="->", color=BRAND_YELL, lw=2.5))
    ax.text(0.5,0.72,"v = const",color=GREEN,fontsize=8,ha="center",fontweight="bold")
    ax.text(0.5,0.25,"Fnet = 0",color=PINK,fontsize=8,ha="center",fontweight="bold")

def draw_newton2(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.add_patch(mpatches.Rectangle((0.3,0.38),0.4,0.28,
                                     facecolor="#1a2a40", edgecolor=BRAND_CYAN, lw=2, zorder=3))
    ax.text(0.5,0.52,"m",color=WHITE,fontsize=12,ha="center",va="center",fontweight="bold")
    ax.annotate("", xy=(0.84,0.52), xytext=(0.70,0.52),
                arrowprops=dict(arrowstyle="->", color=BRAND_YELL, lw=3))
    ax.text(0.88,0.52,"F",color=BRAND_YELL,fontsize=10,va="center",fontweight="bold")
    ax.annotate("", xy=(0.70,0.30), xytext=(0.50,0.30),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
    ax.text(0.72,0.30,"a",color=GREEN,fontsize=9,va="center",fontweight="bold",style="italic")

def draw_newton3(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.add_patch(mpatches.Rectangle((0.08,0.38),0.32,0.24,
                                     facecolor="#1a2a40", edgecolor=BRAND_CYAN, lw=2))
    ax.add_patch(mpatches.Rectangle((0.60,0.38),0.32,0.24,
                                     facecolor="#1a2a40", edgecolor=BRAND_ORNG, lw=2))
    ax.text(0.24,0.50,"A",color=BRAND_CYAN,fontsize=11,ha="center",va="center",fontweight="bold")
    ax.text(0.76,0.50,"B",color=BRAND_ORNG,fontsize=11,ha="center",va="center",fontweight="bold")
    ax.annotate("", xy=(0.60,0.56), xytext=(0.40,0.56),
                arrowprops=dict(arrowstyle="->", color=BRAND_CYAN, lw=2.5))
    ax.annotate("", xy=(0.40,0.44), xytext=(0.60,0.44),
                arrowprops=dict(arrowstyle="->", color=BRAND_ORNG, lw=2.5))
    ax.text(0.5,0.78,"FAB",color=BRAND_CYAN,fontsize=7.5,ha="center")
    ax.text(0.5,0.22,"FBA",color=BRAND_ORNG,fontsize=7.5,ha="center")

def draw_momentum(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.add_patch(plt.Circle((0.28,0.55),0.14,color=BRAND_BLUE,zorder=3))
    ax.text(0.28,0.55,"m",color=WHITE,fontsize=10,ha="center",va="center",fontweight="bold")
    ax.annotate("", xy=(0.80,0.55), xytext=(0.44,0.55),
                arrowprops=dict(arrowstyle="->", color=BRAND_YELL, lw=2.5))
    ax.text(0.63,0.68,"v",color=BRAND_YELL,fontsize=10,ha="center",fontweight="bold",style="italic")
    ax.text(0.5,0.22,"p = mv",color=GREEN,fontsize=8,ha="center",fontweight="bold")

def draw_impulse(ax):
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    # F-t rectangle = impulse
    ax.add_patch(mpatches.Rectangle((0.15,0.3),0.7,0.38,
                                     facecolor="#1a3a60", edgecolor=BRAND_CYAN, lw=1.5, alpha=0.7))
    ax.text(0.5,0.49,"F · Δt",color=BRAND_YELL,fontsize=10,ha="center",va="center",fontweight="bold")
    ax.text(0.5,0.78,"= Δp",color=GREEN,fontsize=9,ha="center",fontweight="bold")
    ax.plot([0.15,0.85],[0.30,0.30],color=GREY,lw=2)
    ax.text(0.5,0.14,"Δt",color=GREY,fontsize=8,ha="center")

DIAGRAM_FNS = {
    "flux": draw_flux_diagram, "coil_magnet": draw_coil_magnet,
    "lenz": draw_lenz, "motional": draw_motional, "inductor": draw_inductor,
    "ohm": draw_ohm, "wire": draw_wire, "loop": draw_loop,
    "bridge": draw_bridge, "power": draw_power,
    "newton1": draw_newton1, "newton2": draw_newton2, "newton3": draw_newton3,
    "momentum": draw_momentum, "impulse": draw_impulse,
}

# ────────────────────────────── header / footer ───────────────────────────────

def draw_brand_header(ax, chapter_tag):
    """Draw CBSEMock logo + chapter tag in the header axis."""
    ax.set_facecolor(BRAND_NAVY); ax.axis("off")
    # Load logo image
    if LOGO_PATH.exists():
        try:
            logo_img = matplotlib.image.imread(str(LOGO_PATH))
            # Place logo left side
            logo_ax = ax.inset_axes([0.01, 0.05, 0.42, 0.90])
            logo_ax.imshow(logo_img)
            logo_ax.axis("off")
        except Exception:
            ax.text(0.02, 0.60, "CBSEMock", color=BRAND_CYAN,
                    fontsize=18, fontweight="bold", va="center",
                    transform=ax.transAxes)
            ax.text(0.02, 0.22, "org.in", color=WHITE, fontsize=10,
                    va="center", transform=ax.transAxes)
    else:
        ax.text(0.02, 0.60, "CBSEMock", color=BRAND_CYAN,
                fontsize=18, fontweight="bold", va="center",
                transform=ax.transAxes)
    # Chapter tag pill — right side
    ax.text(0.98, 0.65, chapter_tag, color=BRAND_CYAN, fontsize=9,
            ha="right", va="center", transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#0d2a4a",
                      edgecolor=BRAND_CYAN, lw=1.5))
    # Thin divider line at bottom
    ax.axhline(0, color=BRAND_BLUE, lw=2)


def draw_title_band(ax, line1, line2, board_note):
    ax.set_facecolor(BRAND_NAVY); ax.axis("off")
    ax.text(0.5, 0.80, line1, color=WHITE, fontsize=24, fontweight="bold",
            ha="center", va="center", transform=ax.transAxes)
    ax.text(0.5, 0.42, line2, color=BRAND_CYAN, fontsize=24, fontweight="bold",
            ha="center", va="center", transform=ax.transAxes)
    ax.text(0.5, 0.08, board_note, color=BRAND_YELL, fontsize=8,
            ha="center", va="center", transform=ax.transAxes)


def draw_footer(ax, cta, hashtags):
    ax.set_facecolor("#071020"); ax.axis("off")
    ax.axhline(0.98, color=BRAND_BLUE, lw=1.5)
    # Yellow CTA pill
    ax.text(0.50, 0.68, cta, color="#1a1a1a", fontsize=10, fontweight="bold",
            ha="center", va="center", transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor=BRAND_YELL,
                      edgecolor=BRAND_YELL, lw=0))
    # Globe + domain
    ax.text(0.50, 0.26, "www  cbsemock.org.in", color=WHITE, fontsize=9,
            ha="center", va="center", transform=ax.transAxes)
    # Hashtags
    ax.text(0.50, 0.06, hashtags, color=GREY, fontsize=6.5,
            ha="center", va="center", transform=ax.transAxes)


# ───────────────────────────── main generator ─────────────────────────────────

def generate_card(topic_id: str) -> Path:
    data = TOPICS[topic_id]
    rows = data["rows"]
    n    = len(rows)

    fig = plt.figure(figsize=(W_IN, H_IN), facecolor=BRAND_NAVY)

    # Height fractions
    hdr_frac   = 0.085   # logo strip
    title_frac = 0.095   # title band
    foot_frac  = 0.090   # footer
    rows_frac  = 1.0 - hdr_frac - title_frac - foot_frac
    row_h      = rows_frac / n

    # ── Header ─────────────────────────────────────────────────────────────────
    ax_hdr = fig.add_axes([0, 1 - hdr_frac, 1, hdr_frac])
    draw_brand_header(ax_hdr, data["chapter_tag"])

    # ── Title band ─────────────────────────────────────────────────────────────
    ax_ttl = fig.add_axes([0, 1 - hdr_frac - title_frac, 1, title_frac])
    draw_title_band(ax_ttl, data["title_line1"], data["title_line2"], data["board_note"])

    # ── Formula rows ───────────────────────────────────────────────────────────
    for i, row in enumerate(rows):
        yb  = foot_frac + (n - 1 - i) * row_h
        pad = 0.006
        col = LABEL_COLS[i % len(LABEL_COLS)]

        # Card bg
        ax_c = fig.add_axes([pad, yb + pad, 1 - 2*pad, row_h - 2*pad])
        ax_c.set_facecolor("#0d1e35")
        for sp in ax_c.spines.values():
            sp.set_edgecolor(col); sp.set_linewidth(1.5)
        ax_c.set_xticks([]); ax_c.set_yticks([])

        # Left label pill (28%) — draw filled rectangle explicitly
        ax_l = fig.add_axes([pad*2, yb + pad*2, 0.28, row_h - pad*4])
        ax_l.set_facecolor(BRAND_NAVY); ax_l.axis("off")
        ax_l.set_xlim(0,1); ax_l.set_ylim(0,1)
        import matplotlib.patches as _mp
        ax_l.add_patch(_mp.FancyBboxPatch((0.04,0.04), 0.92, 0.92,
                        boxstyle="round,pad=0.04",
                        facecolor=col, edgecolor="none", zorder=1))
        ax_l.text(0.5, 0.64, row["label"], color=WHITE, fontsize=8,
                  fontweight="bold", ha="center", va="center",
                  transform=ax_l.transAxes, wrap=True, zorder=2)
        ax_l.text(0.5, 0.22, row["note"], color="#ccddee", fontsize=6.5,
                  ha="center", va="center", transform=ax_l.transAxes, zorder=2)

        # Centre diagram (35%)
        ax_d = fig.add_axes([0.29 + pad, yb + pad*2, 0.35, row_h - pad*4])
        ax_d.set_facecolor("#0d1e35"); ax_d.axis("off")
        fn = DIAGRAM_FNS.get(row["diagram"])
        if fn:
            fn(ax_d)

        # Right formula (35%)
        ax_f = fig.add_axes([0.65, yb + pad, 0.35 - pad, row_h - pad*2])
        ax_f.set_facecolor("#0d1e35"); ax_f.axis("off")
        ax_f.text(0.5, 0.52, row["formula"], color=BRAND_YELL,
                  fontsize=13, fontweight="bold",
                  ha="center", va="center", transform=ax_f.transAxes)

    # ── Footer ─────────────────────────────────────────────────────────────────
    ax_ft = fig.add_axes([0, 0, 1, foot_frac])
    draw_footer(ax_ft, data["cta"], data["hashtags"])

    out_path = OUT_DIR / f"{topic_id}_card.png"
    fig.savefig(out_path, dpi=DPI, bbox_inches="tight",
                facecolor=BRAND_NAVY, pad_inches=0)
    plt.close(fig)
    print(f"[OK] {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="em_induction")
    parser.add_argument("--all",   action="store_true")
    args = parser.parse_args()
    if args.all:
        for t in TOPICS: generate_card(t)
    else:
        generate_card(args.topic)

if __name__ == "__main__":
    main()
