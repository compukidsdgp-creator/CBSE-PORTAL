"""
diagram_library.py
──────────────────
Subject-specific, topic-relevant diagram functions for Formula Flash cards & reels.

Each function signature: draw_XYZ(ax, progress=1.0)
  ax       — matplotlib Axes (already has facecolor set by caller)
  progress — 0.0→1.0 animation progress (1.0 = static / fully drawn)

Colour constants match the v2 palette from generate_formula_card_v2.py /
generate_formula_reel_v2.py so callers just import this module.

Usage:
  from diagram_library import DIAGRAMS
  fn = DIAGRAMS["chem_reaction_coordinate"]
  fn(ax, progress=0.8)
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc, FancyArrowPatch

# ── Shared palette ─────────────────────────────────────────────────────────────
CYAN   = "#00d4ff"
YELLOW = "#f9c820"
ORANGE = "#ff6b35"
WHITE  = "#f0f4ff"
GREY   = "#6a7f99"
GREEN  = "#00ff88"
PINK   = "#ff4da6"
PURPLE = "#8b5cf6"
RED    = "#ef5350"
BLUE   = "#1565c0"

# ═══════════════════════════════════════════════════════════════════════════════
#  PHYSICS
# ═══════════════════════════════════════════════════════════════════════════════

def draw_field_lines(ax, progress=1.0):
    """Uniform electric / magnetic field lines with arrows."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    n = max(1, int(5 * progress))
    for y in np.linspace(0.15, 0.85, n):
        ax.annotate("", xy=(0.88, y), xytext=(0.12, y),
                    arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.4))
    if progress > 0.6:
        # Test charge
        ax.plot(0.5, 0.5, "o", color=YELLOW, markersize=10, zorder=3)
        ax.text(0.5, 0.50, "+", color="#111", fontsize=8,
                ha="center", va="center", fontweight="bold", zorder=4)

def draw_parallel_plates(ax, progress=1.0):
    """Parallel plate capacitor with field lines."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot([0.15,0.15],[0.15,0.85], color=RED,  lw=5, solid_capstyle="round")
    ax.plot([0.85,0.85],[0.15,0.85], color=BLUE, lw=5, solid_capstyle="round")
    ax.text(0.11, 0.50, "+", color=RED,  fontsize=14, ha="center", va="center", fontweight="bold")
    ax.text(0.89, 0.50, "−", color=BLUE, fontsize=18, ha="center", va="center", fontweight="bold")
    if progress > 0.4:
        for y in np.linspace(0.25, 0.75, 4):
            ax.annotate("", xy=(0.82, y), xytext=(0.18, y),
                        arrowprops=dict(arrowstyle="->", color=CYAN,
                                        lw=1.2, alpha=min(1,(progress-0.4)/0.6)))

def draw_circuit_loop(ax, progress=1.0):
    """Simple closed circuit loop."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    rect = FancyBboxPatch((0.15,0.20), 0.70, 0.60,
                           boxstyle="round,pad=0.04",
                           facecolor="none", edgecolor=CYAN, lw=2.5)
    ax.add_patch(rect)
    # Battery symbol
    ax.plot([0.15,0.15],[0.44,0.56], color=YELLOW, lw=4)
    ax.plot([0.15,0.15],[0.38,0.62], color=YELLOW, lw=2)
    # Current arrow
    if progress > 0.5:
        ax.annotate("", xy=(0.60,0.80), xytext=(0.40,0.80),
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
        ax.text(0.50, 0.90, "I", color=GREEN, fontsize=10, ha="center", fontweight="bold")

def draw_wheatstone(ax, progress=1.0):
    """Wheatstone bridge diamond."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    pts = {"A":(0.50,0.88),"B":(0.15,0.50),"C":(0.85,0.50),"D":(0.50,0.12)}
    labels = {("A","B"):"P", ("A","C"):"Q", ("B","D"):"R", ("C","D"):"S"}
    for (a,b), lbl in labels.items():
        x1,y1 = pts[a]; x2,y2 = pts[b]
        ax.plot([x1,x2],[y1,y2], color=CYAN, lw=2, alpha=min(1,progress*1.5))
        ax.text((x1+x2)/2-0.07,(y1+y2)/2, lbl, color=YELLOW, fontsize=8, fontweight="bold")
    if progress > 0.5:
        ax.plot([pts["B"][0],pts["C"][0]],[pts["B"][1],pts["C"][1]],
                color=GREEN, lw=1.5, ls="--")
        ax.text(0.50,0.52,"G", color=GREEN, fontsize=8, ha="center")
    for _,(x,y) in pts.items():
        ax.plot(x,y,"o", color=WHITE, markersize=7)

def draw_power_triangle(ax, progress=1.0):
    """P=VI triangle."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    tri = plt.Polygon([[0.5,0.85],[0.10,0.20],[0.90,0.20]],
                      fill=False, edgecolor=CYAN, lw=2.5)
    ax.add_patch(tri)
    ax.text(0.50,0.68,"P", color=YELLOW, fontsize=14, ha="center", va="center", fontweight="bold")
    ax.text(0.27,0.28,"V", color=GREEN,  fontsize=12, ha="center", fontweight="bold")
    ax.text(0.73,0.28,"I", color=ORANGE, fontsize=12, ha="center", fontweight="bold")

def draw_mirror_optics(ax, progress=1.0):
    """Concave mirror with ray diagram."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    theta = np.linspace(math.pi*0.55, math.pi*1.45, 60)
    x = 0.90 + 0.35*np.cos(theta)
    y = 0.50 + 0.45*np.sin(theta)
    ax.plot(x, y, color=CYAN, lw=3)
    ax.axhline(0.50, color=GREY, lw=0.8, ls="--", alpha=0.5)
    if progress > 0.4:
        ax.annotate("", xy=(0.72,0.50), xytext=(0.20,0.50),
                    arrowprops=dict(arrowstyle="->", color=YELLOW, lw=1.5))
        ax.annotate("", xy=(0.72,0.50), xytext=(0.20,0.70),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))
    if progress > 0.7:
        ax.annotate("", xy=(0.30,0.30), xytext=(0.72,0.50),
                    arrowprops=dict(arrowstyle="->", color=YELLOW, lw=1.5))
        ax.annotate("", xy=(0.30,0.30), xytext=(0.72,0.50),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))

def draw_snell(ax, progress=1.0):
    """Snell's law refraction diagram."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.50, color=GREY, lw=1, ls="--")
    ax.axvline(0.50, color=GREY, lw=0.8, ls=":", alpha=0.5)
    ax.fill_between([0,1],[0,0],[0.50,0.50], color="#0d2040", alpha=0.6)
    ax.text(0.08,0.40,"n₁", color=CYAN, fontsize=9, fontweight="bold")
    ax.text(0.08,0.15,"n₂", color=PURPLE, fontsize=9, fontweight="bold")
    if progress > 0.3:
        ax.annotate("", xy=(0.50,0.50), xytext=(0.25,0.80),
                    arrowprops=dict(arrowstyle="->", color=YELLOW, lw=2))
    if progress > 0.6:
        ax.annotate("", xy=(0.72,0.20), xytext=(0.50,0.50),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2))

def draw_young_fringes(ax, progress=1.0):
    """Young's double slit fringe pattern."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot([0.25,0.25],[0.30,0.46], color=CYAN, lw=3)
    ax.plot([0.25,0.25],[0.54,0.70], color=CYAN, lw=3)
    if progress > 0.3:
        x = np.linspace(0.30, 0.90, 200)
        y = 0.5 + 0.35*np.sinc(6*(x-0.60))**2
        alpha = min(1,(progress-0.3)/0.7)
        ax.fill_between(x, 0.5, y, color=YELLOW, alpha=alpha*0.7)
        ax.plot(x, y, color=YELLOW, lw=1.5, alpha=alpha)
    ax.annotate("", xy=(0.60,0.68), xytext=(0.60,0.50),
                arrowprops=dict(arrowstyle="<->", color=WHITE, lw=1.2))
    ax.text(0.63,0.60,"β", color=WHITE, fontsize=9, va="center")

def draw_pn_junction(ax, progress=1.0):
    """P-N junction diode."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.05,0.30),0.42,0.40,
                                boxstyle="round,pad=0.02",
                                facecolor="#1a0a3a", edgecolor=PURPLE, lw=2))
    ax.add_patch(FancyBboxPatch((0.53,0.30),0.42,0.40,
                                boxstyle="round,pad=0.02",
                                facecolor="#0a1a2a", edgecolor=CYAN, lw=2))
    ax.text(0.26,0.50,"P", color=PURPLE, fontsize=18, ha="center", va="center", fontweight="bold")
    ax.text(0.74,0.50,"N", color=CYAN,   fontsize=18, ha="center", va="center", fontweight="bold")
    if progress > 0.5:
        ax.annotate("", xy=(0.70,0.18), xytext=(0.30,0.18),
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))
        ax.text(0.50,0.11,"I (forward)", color=GREEN, fontsize=7, ha="center")

def draw_transistor(ax, progress=1.0):
    """NPN transistor symbol."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot([0.40,0.40],[0.20,0.80], color=CYAN, lw=3)
    ax.plot([0.15,0.40],[0.50,0.50], color=YELLOW, lw=2)
    ax.text(0.08,0.50,"B", color=YELLOW, fontsize=9, ha="center", va="center", fontweight="bold")
    ax.plot([0.40,0.75],[0.65,0.85], color=ORANGE, lw=2)
    ax.plot([0.40,0.75],[0.35,0.15], color=GREEN,  lw=2)
    if progress > 0.5:
        ax.annotate("", xy=(0.70,0.82), xytext=(0.57,0.73),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))
    ax.text(0.78,0.85,"C", color=ORANGE, fontsize=9, ha="center", fontweight="bold")
    ax.text(0.78,0.14,"E", color=GREEN,  fontsize=9, ha="center", fontweight="bold")

def draw_de_broglie(ax, progress=1.0):
    """de Broglie wave around nucleus."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot(0.50,0.50,"o", color=YELLOW, markersize=12)
    ax.text(0.50,0.50,"+", color="#111", fontsize=9, ha="center", va="center", fontweight="bold")
    n_waves = max(1, int(8*progress))
    theta = np.linspace(0, 2*math.pi*min(1,progress), 300)
    r = 0.32 + 0.04*np.sin(n_waves*theta)
    ax.plot(0.50+r*np.cos(theta), 0.50+r*np.sin(theta), color=CYAN, lw=2)

def draw_photoelectric(ax, progress=1.0):
    """Photoelectric effect — photon hitting metal surface."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.fill_between([0,1],[0,0],[0.30,0.30], color="#1a2a1a", alpha=0.8)
    ax.text(0.50,0.17,"Metal", color=GREY, fontsize=8, ha="center")
    if progress > 0.2:
        ax.annotate("", xy=(0.40,0.30), xytext=(0.20,0.70),
                    arrowprops=dict(arrowstyle="->", color=YELLOW, lw=2.5,
                                   alpha=min(1,(progress-0.2)/0.4)))
        ax.text(0.22,0.78,"hν", color=YELLOW, fontsize=11, fontweight="bold")
    if progress > 0.6:
        ax.annotate("", xy=(0.72,0.65), xytext=(0.42,0.32),
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=2,
                                   alpha=min(1,(progress-0.6)/0.4)))
        ax.text(0.78,0.68,"e⁻", color=GREEN, fontsize=10, fontweight="bold")

def draw_bohr_atom(ax, progress=1.0):
    """Bohr model — electron orbit."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot(0.50,0.50,"o", color=RED, markersize=10)
    ax.text(0.50,0.50,"p", color=WHITE, fontsize=7, ha="center", va="center")
    for i,r in enumerate([0.18,0.28,0.38]):
        alpha = min(1, progress*(i+1)/3*2)
        circ = plt.Circle((0.5,0.5), r, fill=False, edgecolor=CYAN, lw=1.5, alpha=alpha)
        ax.add_patch(circ)
        ax.text(0.5+r*0.70, 0.5+r*0.70, f"n={i+1}", color=GREY, fontsize=6, alpha=alpha)
    if progress > 0.7:
        theta = 2*math.pi*0.25
        r = 0.28
        ax.plot(0.5+r*math.cos(theta), 0.5+r*math.sin(theta),
                "o", color=CYAN, markersize=5)

def draw_radioactive_decay(ax, progress=1.0):
    """Exponential decay curve."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.15, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.12, color=GREY, lw=0.8, alpha=0.4)
    ax.text(0.08,0.85,"N", color=WHITE, fontsize=9, ha="center")
    ax.text(0.55,0.10,"t", color=WHITE, fontsize=9, ha="center")
    x = np.linspace(0, 1*progress, 200)
    y = 0.15 + 0.70*np.exp(-3*x)
    ax.plot(0.12+x*0.80, y, color=GREEN, lw=2.5)
    if progress > 0.5:
        ax.axvline(0.12+0.80*(0.231), color=YELLOW, lw=1.2, ls="--", alpha=0.7)
        ax.text(0.33,0.60,"t½", color=YELLOW, fontsize=8)

# ═══════════════════════════════════════════════════════════════════════════════
#  CHEMISTRY
# ═══════════════════════════════════════════════════════════════════════════════

def draw_reaction_coordinate(ax, progress=1.0):
    """Energy profile / reaction coordinate curve."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.15, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.10, color=GREY, lw=0.8, alpha=0.4)
    ax.text(0.06,0.90,"E", color=WHITE, fontsize=8, ha="center")
    ax.text(0.55,0.08,"Reaction coordinate", color=GREY, fontsize=6, ha="center")
    x = np.linspace(0, progress, 200)
    y = 0.20 + 0.15*x/progress + 0.55*np.exp(-((x-0.45*progress)**2)/(0.04*progress**2))
    ax.plot(0.12+x*0.80, y, color=ORANGE, lw=2.5)
    if progress > 0.5:
        peak_x = 0.12 + 0.45*0.80
        ax.annotate("", xy=(peak_x,0.74), xytext=(peak_x,0.35),
                    arrowprops=dict(arrowstyle="<->", color=YELLOW, lw=1.5))
        ax.text(peak_x+0.04,0.55,"Eₐ", color=YELLOW, fontsize=8, fontweight="bold")

def draw_first_order_decay(ax, progress=1.0):
    """First-order ln[A] vs t linear plot."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.15, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.12, color=GREY, lw=0.8, alpha=0.4)
    ax.text(0.05,0.88,"ln[A]", color=WHITE, fontsize=7, ha="center")
    ax.text(0.55,0.08,"t", color=WHITE, fontsize=9, ha="center")
    end_x = 0.12 + 0.80*min(1,progress)
    ax.plot([0.12, end_x], [0.80, 0.80-0.60*min(1,progress)], color=GREEN, lw=2.5)
    if progress > 0.6:
        ax.text(0.65,0.42,"slope = −k", color=YELLOW, fontsize=7)

def draw_half_life(ax, progress=1.0):
    """Half-life steps on concentration vs time plot."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.12, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.10, color=GREY, lw=0.8, alpha=0.4)
    x = np.linspace(0, progress, 200)
    y = 0.12 + 0.72*np.exp(-2.5*x)
    ax.plot(0.12+x*0.82, y, color=CYAN, lw=2.5)
    for i,t in enumerate([0.277,0.554,0.831]):
        if progress > t:
            conc = 0.12 + 0.72*np.exp(-2.5*t)
            ax.plot([0.12,0.12+t*0.82],[conc,conc], color=YELLOW, lw=1, ls="--", alpha=0.7)
            ax.plot([0.12+t*0.82,0.12+t*0.82],[0.12,conc], color=YELLOW, lw=1, ls="--", alpha=0.7)

def draw_arrhenius(ax, progress=1.0):
    """Arrhenius plot: ln k vs 1/T."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.15, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.12, color=GREY, lw=0.8, alpha=0.4)
    ax.text(0.06,0.88,"ln k", color=WHITE, fontsize=7, ha="center")
    ax.text(0.50,0.07,"1/T", color=WHITE, fontsize=8, ha="center")
    end_x = 0.12 + 0.80*min(1,progress)
    ax.plot([0.12, end_x], [0.80, 0.80-0.60*min(1,progress)], color=ORANGE, lw=2.5)
    if progress > 0.5:
        ax.text(0.65,0.42,"slope = −Eₐ/R", color=YELLOW, fontsize=6.5)

def draw_electrolytic_cell(ax, progress=1.0):
    """Electrolytic cell with electrodes."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.15,0.20),0.70,0.55,
                                boxstyle="round,pad=0.03",
                                facecolor="#071828", edgecolor=GREY, lw=1.5))
    ax.fill_between([0.16,0.84],[0.21,0.21],[0.52,0.52], color="#0d3050", alpha=0.6)
    ax.text(0.50,0.38,"Electrolyte", color=GREY, fontsize=7, ha="center")
    ax.plot([0.25,0.25],[0.52,0.78], color=RED,  lw=5, solid_capstyle="round")
    ax.plot([0.75,0.75],[0.52,0.78], color=BLUE, lw=5, solid_capstyle="round")
    ax.text(0.25,0.82,"Anode(+)", color=RED,  fontsize=6.5, ha="center")
    ax.text(0.75,0.82,"Cathode(−)",color=BLUE, fontsize=6.5, ha="center")
    if progress > 0.6:
        ax.annotate("", xy=(0.60,0.38), xytext=(0.40,0.38),
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
        ax.text(0.50,0.28,"ions", color=GREEN, fontsize=6.5, ha="center")

def draw_conductance_plot(ax, progress=1.0):
    """Molar conductance vs √C plot."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.15, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.10, color=GREY, lw=0.8, alpha=0.4)
    ax.text(0.05,0.88,"Λm", color=WHITE, fontsize=7, ha="center")
    ax.text(0.55,0.07,"√C", color=WHITE, fontsize=8, ha="center")
    x = np.linspace(0, progress*0.88, 200)
    y = 0.80 - 0.55*x
    ax.plot(0.12+x*0.82, y, color=CYAN, lw=2.5)
    if progress > 0.4:
        ax.plot(0.12, 0.80, "o", color=YELLOW, markersize=7)
        ax.text(0.09,0.86,"Λ∞", color=YELLOW, fontsize=7)

def draw_vapour_pressure(ax, progress=1.0):
    """Raoult's law — vapour pressure lowering."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.15, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.10, color=GREY, lw=0.8, alpha=0.4)
    ax.text(0.05,0.88,"p", color=WHITE, fontsize=9, ha="center")
    ax.text(0.55,0.07,"x₁", color=WHITE, fontsize=8, ha="center")
    end_x = 0.12 + 0.80*min(1,progress)
    ax.plot([0.12, end_x],[0.15, 0.15+0.65*min(1,progress)], color=ORANGE, lw=2.5)
    if progress > 0.6:
        ax.plot(0.12+0.80, 0.80, "o", color=YELLOW, markersize=7)
        ax.text(0.94,0.80,"p°", color=YELLOW, fontsize=8)

def draw_boiling_point(ax, progress=1.0):
    """ΔTb elevation diagram."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.40, color=GREY, lw=1, ls="--", alpha=0.5)
    ax.axhline(0.60, color=GREY, lw=1, ls="--", alpha=0.5)
    ax.plot([0.20,0.50],[0.40,0.40], color=BLUE, lw=3)
    ax.text(0.35,0.32,"Solvent Tb", color=BLUE, fontsize=6.5, ha="center")
    if progress > 0.4:
        ax.plot([0.50,0.80],[0.60,0.60], color=ORANGE, lw=3,
                alpha=min(1,(progress-0.4)/0.6))
        ax.text(0.65,0.68,"Solution Tb", color=ORANGE, fontsize=6.5, ha="center")
    if progress > 0.7:
        ax.annotate("", xy=(0.65,0.60), xytext=(0.65,0.40),
                    arrowprops=dict(arrowstyle="<->", color=YELLOW, lw=2))
        ax.text(0.70,0.50,"ΔTb", color=YELLOW, fontsize=8, fontweight="bold")

def draw_osmosis(ax, progress=1.0):
    """Osmosis — semipermeable membrane."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot([0.50,0.50],[0.10,0.90], color=CYAN, lw=3, ls="--")
    ax.text(0.25,0.88,"Solvent", color=GREY,  fontsize=7, ha="center")
    ax.text(0.75,0.88,"Solution", color=ORANGE,fontsize=7, ha="center")
    ax.fill_between([0.08,0.49],[0.15,0.15],[0.45,0.45], color="#0a2a4a", alpha=0.5)
    ax.fill_between([0.51,0.92],[0.15,0.15],[0.65,0.65], color="#1a0a3a", alpha=0.5)
    if progress > 0.4:
        for y in [0.28,0.35]:
            ax.annotate("", xy=(0.48,y), xytext=(0.35,y),
                        arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
    if progress > 0.7:
        ax.annotate("", xy=(0.65,0.60), xytext=(0.65,0.42),
                    arrowprops=dict(arrowstyle="<->", color=YELLOW, lw=1.5))
        ax.text(0.70,0.52,"π", color=YELLOW, fontsize=10, fontweight="bold")

def draw_crystal_lattice(ax, progress=1.0):
    """Simple cubic crystal lattice."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    for i in range(3):
        for j in range(3):
            x = 0.20 + i*0.28
            y = 0.22 + j*0.28
            alpha = min(1, progress*3 - i*0.3 - j*0.2)
            if alpha > 0:
                ax.plot(x, y, "o", color=CYAN, markersize=10, alpha=alpha)
    if progress > 0.5:
        for i in range(3):
            for j in range(2):
                ax.plot([0.20+i*0.28,0.20+i*0.28],[0.22+j*0.28,0.22+(j+1)*0.28],
                        color=GREY, lw=1, alpha=0.5)
                ax.plot([0.20+j*0.28,0.20+(j+1)*0.28],[0.22+i*0.28,0.22+i*0.28],
                        color=GREY, lw=1, alpha=0.5)

def draw_coordination_sphere(ax, progress=1.0):
    """Octahedral coordination complex."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot(0.50,0.50,"o", color=ORANGE, markersize=14, zorder=3)
    ax.text(0.50,0.50,"M", color=WHITE, fontsize=9, ha="center", va="center", zorder=4)
    ligand_pos = [(0.50,0.82),(0.50,0.18),(0.18,0.50),(0.82,0.50),(0.73,0.73),(0.27,0.27)]
    for k,(x,y) in enumerate(ligand_pos):
        alpha = min(1, progress*(k+1)/6*2)
        ax.plot(x,y,"o", color=CYAN, markersize=9, alpha=alpha, zorder=3)
        ax.plot([0.50,x],[0.50,y], color=GREY, lw=1.5, alpha=alpha*0.7)
        ax.text(x+(x-0.5)*0.18, y+(y-0.5)*0.18, "L", color=CYAN, fontsize=7,
                ha="center", va="center", alpha=alpha)

# ═══════════════════════════════════════════════════════════════════════════════
#  BIOLOGY
# ═══════════════════════════════════════════════════════════════════════════════

def draw_punnett_square(ax, progress=1.0):
    """2×2 Punnett square."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot([0.30,0.30],[0.20,0.80], color=GREY, lw=1.5)
    ax.plot([0.30,0.80],[0.50,0.50], color=GREY, lw=1.5)
    ax.plot([0.80,0.80],[0.20,0.80], color=GREY, lw=1.5)
    ax.plot([0.30,0.80],[0.20,0.20], color=GREY, lw=1.5)
    ax.text(0.42,0.90,"A", color=CYAN,  fontsize=11, ha="center", fontweight="bold")
    ax.text(0.68,0.90,"a", color=CYAN,  fontsize=11, ha="center", fontweight="bold")
    ax.text(0.18,0.65,"A", color=ORANGE,fontsize=11, ha="center", fontweight="bold")
    ax.text(0.18,0.35,"a", color=ORANGE,fontsize=11, ha="center", fontweight="bold")
    if progress > 0.4:
        for (x,y,txt,col) in [(0.42,0.65,"AA",YELLOW),(0.68,0.65,"Aa",WHITE),
                               (0.42,0.35,"Aa",WHITE),(0.68,0.35,"aa",PINK)]:
            ax.text(x,y,txt, color=col, fontsize=10, ha="center", va="center",
                    alpha=min(1,(progress-0.4)/0.6), fontweight="bold")

def draw_dna_helix(ax, progress=1.0):
    """Simplified DNA double helix."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    t = np.linspace(0, 2*math.pi*min(1,progress)*2.5, 300)
    x1 = 0.50 + 0.22*np.cos(t)
    y1 = 0.10 + 0.80*(t/(2*math.pi*2.5))
    x2 = 0.50 - 0.22*np.cos(t)
    ax.plot(x1, y1, color=CYAN,   lw=2.5)
    ax.plot(x2, y1, color=ORANGE, lw=2.5)
    # Base pair rungs
    if progress > 0.3:
        for i in range(0,len(t),25):
            if y1[i] > 0.12 and y1[i] < 0.88:
                ax.plot([x1[i],x2[i]],[y1[i],y1[i]],
                        color=GREY, lw=1.2, alpha=0.6)

def draw_cell_division(ax, progress=1.0):
    """Mitosis — cell dividing."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    if progress < 0.5:
        # One cell
        circ = plt.Circle((0.50,0.50), 0.32, fill=False, edgecolor=GREEN, lw=2.5)
        ax.add_patch(circ)
        ax.plot(0.50,0.50,"o", color=PURPLE, markersize=12)
    else:
        # Two daughter cells
        alpha = min(1,(progress-0.5)/0.5)
        offset = 0.20*alpha
        for cx in [0.50-offset, 0.50+offset]:
            circ = plt.Circle((cx,0.50), 0.22, fill=False,
                              edgecolor=GREEN, lw=2, alpha=alpha)
            ax.add_patch(circ)
            ax.plot(cx,0.50,"o", color=PURPLE, markersize=8, alpha=alpha)

def draw_leaf_cross_section(ax, progress=1.0):
    """Leaf cross-section showing chloroplasts."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    # Epidermis
    ax.fill_between([0.08,0.92],[0.72,0.72],[0.80,0.80], color="#1a3a1a", alpha=0.8)
    ax.fill_between([0.08,0.92],[0.20,0.20],[0.28,0.28], color="#1a3a1a", alpha=0.8)
    # Mesophyll cells
    if progress > 0.3:
        for x in [0.20,0.38,0.56,0.74]:
            ax.add_patch(FancyBboxPatch((x,0.50),0.14,0.18,
                                        boxstyle="round,pad=0.02",
                                        facecolor="#0a2a0a", edgecolor=GREEN, lw=1.5,
                                        alpha=min(1,(progress-0.3)/0.7)))
            # Chloroplasts
            if progress > 0.6:
                for y in [0.54,0.62]:
                    ax.plot(x+0.07, y, "o", color=GREEN, markersize=4,
                            alpha=min(1,(progress-0.6)/0.4))
    # Stomata
    if progress > 0.7:
        ax.add_patch(FancyBboxPatch((0.44,0.18),0.12,0.04,
                                    boxstyle="round,pad=0.01",
                                    facecolor="#071807", edgecolor=GREEN, lw=1))
        ax.text(0.50,0.11,"Stomata", color=GREEN, fontsize=6.5, ha="center")

def draw_food_chain(ax, progress=1.0):
    """Food chain / trophic pyramid."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    levels = [
        (0.10,0.28,0.80,0.14,GREEN,"Producers (plants)"),
        (0.18,0.46,0.64,0.14,YELLOW,"Primary consumers"),
        (0.26,0.62,0.48,0.13,ORANGE,"Secondary consumers"),
        (0.34,0.78,0.32,0.12,RED,"Tertiary consumers"),
    ]
    for i,(x,y,w,h,col,lbl) in enumerate(levels):
        alpha = min(1, progress*(i+1)/4*2)
        ax.add_patch(FancyBboxPatch((x,y),w,h,
                                    boxstyle="round,pad=0.01",
                                    facecolor=(*plt.matplotlib.colors.to_rgb(col),0.25*alpha),
                                    edgecolor=col, lw=1.5, alpha=alpha))
        ax.text(x+w/2, y+h/2, lbl, color=col, fontsize=5.5,
                ha="center", va="center", alpha=alpha, fontweight="bold")
    ax.text(0.50,0.07,"10% energy transfer", color=GREY, fontsize=6.5, ha="center")

def draw_population_growth(ax, progress=1.0):
    """J-curve (exponential) vs S-curve (logistic)."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.15, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.10, color=GREY, lw=0.8, alpha=0.4)
    ax.text(0.05,0.88,"N", color=WHITE, fontsize=9, ha="center")
    ax.text(0.55,0.07,"t", color=WHITE, fontsize=8, ha="center")
    x = np.linspace(0, progress, 200)
    # J-curve
    ax.plot(0.12+x*0.80, 0.15+0.70*(np.exp(2.5*x)-1)/
            (np.exp(2.5)-1), color=CYAN, lw=2, label="J")
    # S-curve
    if progress > 0.3:
        y_s = 0.15 + 0.65/(1+np.exp(-8*(x-0.5)))
        ax.plot(0.12+x*0.80, y_s, color=GREEN, lw=2, ls="--")
        ax.axhline(0.80, color=YELLOW, lw=1, ls=":", alpha=0.7)
        ax.text(0.88,0.82,"K", color=YELLOW, fontsize=8, fontweight="bold")
    ax.text(0.78,0.52,"J", color=CYAN, fontsize=8, fontweight="bold")
    ax.text(0.78,0.68,"S", color=GREEN, fontsize=8, fontweight="bold")

def draw_hormone_feedback(ax, progress=1.0):
    """Negative feedback loop — endocrine."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    boxes = [(0.30,0.72,"Hypothalamus",CYAN),(0.30,0.50,"Pituitary",ORANGE),(0.30,0.28,"Target",GREEN)]
    for (x,y,lbl,col) in boxes:
        ax.add_patch(FancyBboxPatch((x,y-0.08),0.40,0.14,
                                    boxstyle="round,pad=0.02",
                                    facecolor="none", edgecolor=col, lw=1.8))
        ax.text(x+0.20, y, lbl, color=col, fontsize=7.5, ha="center", va="center")
    if progress > 0.4:
        ax.annotate("", xy=(0.50,0.56), xytext=(0.50,0.64),
                    arrowprops=dict(arrowstyle="->", color=GREY, lw=1.5))
        ax.annotate("", xy=(0.50,0.34), xytext=(0.50,0.42),
                    arrowprops=dict(arrowstyle="->", color=GREY, lw=1.5))
    if progress > 0.7:
        ax.annotate("", xy=(0.28,0.65), xytext=(0.28,0.35),
                    arrowprops=dict(arrowstyle="->", color=PINK, lw=1.5,
                                   connectionstyle="arc3,rad=0.4"))
        ax.text(0.10,0.50,"−ve", color=PINK, fontsize=8, ha="center", fontweight="bold")

# ═══════════════════════════════════════════════════════════════════════════════
#  MATHEMATICS
# ═══════════════════════════════════════════════════════════════════════════════

def draw_function_curve(ax, progress=1.0):
    """Generic smooth function curve on axes."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.50, color=GREY, lw=0.8, alpha=0.5)
    ax.axvline(0.12, color=GREY, lw=0.8, alpha=0.5)
    x = np.linspace(0, progress, 200)
    y = 0.50 + 0.30*np.sin(x*2*math.pi*1.5)*np.exp(-x*0.5)
    ax.plot(0.12+x*0.82, y, color=CYAN, lw=2.5)

def draw_tangent_line(ax, progress=1.0):
    """Curve with tangent line — derivative."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.15, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.10, color=GREY, lw=0.8, alpha=0.4)
    x = np.linspace(0,1,200)
    y = 0.15 + 0.70*x**2
    ax.plot(0.10+x*0.82, y, color=CYAN, lw=2.5)
    if progress > 0.5:
        # Tangent at x=0.5
        tx = 0.10 + 0.5*0.82
        ty = 0.15 + 0.70*0.25
        slope_vis = 0.70*0.82
        ax.plot([tx-0.20,tx+0.20],[ty-0.20*slope_vis,ty+0.20*slope_vis],
                color=YELLOW, lw=2, alpha=min(1,(progress-0.5)/0.5))
        ax.plot(tx,ty,"o", color=YELLOW, markersize=7)

def draw_integration_area(ax, progress=1.0):
    """Area under curve (shaded)."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.15, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.10, color=GREY, lw=0.8, alpha=0.4)
    x = np.linspace(0,1,200)
    y = 0.20 + 0.55*np.sin(x*math.pi)
    ax.plot(0.10+x*0.82, y, color=CYAN, lw=2.5)
    if progress > 0.3:
        fill_end = int(200*min(1,(progress-0.3)/0.7))
        if fill_end > 1:
            ax.fill_between(0.10+x[:fill_end]*0.82,
                            0.15, y[:fill_end],
                            color=YELLOW, alpha=0.30)
    if progress > 0.8:
        ax.axvline(0.10+0.25*0.82, color=ORANGE, lw=1.2, ls="--")
        ax.axvline(0.10+0.75*0.82, color=ORANGE, lw=1.2, ls="--")
        ax.text(0.10+0.25*0.82-0.03, 0.08,"a", color=ORANGE, fontsize=8)
        ax.text(0.10+0.75*0.82-0.03, 0.08,"b", color=ORANGE, fontsize=8)

def draw_vector_diagram(ax, progress=1.0):
    """Two vectors and their resultant."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.20, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.15, color=GREY, lw=0.8, alpha=0.4)
    if progress > 0.1:
        ax.annotate("", xy=(0.60,0.55), xytext=(0.15,0.20),
                    arrowprops=dict(arrowstyle="->", color=CYAN, lw=2.5,
                                   alpha=min(1,(progress-0.1)/0.4)))
        ax.text(0.30,0.44,"a⃗", color=CYAN, fontsize=10, fontweight="bold")
    if progress > 0.4:
        ax.annotate("", xy=(0.82,0.30), xytext=(0.60,0.55),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.5,
                                   alpha=min(1,(progress-0.4)/0.4)))
        ax.text(0.75,0.50,"b⃗", color=ORANGE, fontsize=10, fontweight="bold")
    if progress > 0.7:
        ax.annotate("", xy=(0.82,0.30), xytext=(0.15,0.20),
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=2,
                                   ls="dashed", alpha=min(1,(progress-0.7)/0.3)))
        ax.text(0.45,0.20,"a⃗+b⃗", color=GREEN, fontsize=8, fontweight="bold")

def draw_cross_product(ax, progress=1.0):
    """Cross product — right hand rule."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.annotate("", xy=(0.72,0.35), xytext=(0.30,0.35),
                arrowprops=dict(arrowstyle="->", color=CYAN, lw=2.5))
    ax.text(0.50,0.27,"a⃗", color=CYAN, fontsize=10, ha="center", fontweight="bold")
    if progress > 0.3:
        ax.annotate("", xy=(0.60,0.68), xytext=(0.30,0.35),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.5,
                                   alpha=min(1,(progress-0.3)/0.4)))
        ax.text(0.38,0.58,"b⃗", color=ORANGE, fontsize=10, fontweight="bold")
    if progress > 0.6:
        ax.annotate("", xy=(0.30,0.75), xytext=(0.30,0.35),
                    arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.5,
                                   alpha=min(1,(progress-0.6)/0.4)))
        ax.text(0.19,0.60,"a⃗×b⃗", color=GREEN, fontsize=8, fontweight="bold")

def draw_probability_tree(ax, progress=1.0):
    """Binary probability tree."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot(0.15,0.50,"o", color=WHITE, markersize=8)
    if progress > 0.2:
        ax.annotate("", xy=(0.45,0.72), xytext=(0.17,0.52),
                    arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.8,
                                   alpha=min(1,(progress-0.2)/0.3)))
        ax.text(0.28,0.68,"p", color=CYAN, fontsize=9, fontweight="bold")
        ax.annotate("", xy=(0.45,0.28), xytext=(0.17,0.48),
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8,
                                   alpha=min(1,(progress-0.2)/0.3)))
        ax.text(0.28,0.33,"q", color=ORANGE, fontsize=9, fontweight="bold")
    if progress > 0.6:
        for y_start, y_ends, col in [(0.72,[(0.88,0.84),(0.88,0.60)],CYAN),
                                      (0.28,[(0.88,0.40),(0.88,0.16)],ORANGE)]:
            for y_end in y_ends:
                ax.annotate("", xy=(y_end[0],y_end[1]),
                            xytext=(0.47,y_start),
                            arrowprops=dict(arrowstyle="->", color=col, lw=1.2,
                                           alpha=min(1,(progress-0.6)/0.4)))

def draw_matrix_grid(ax, progress=1.0):
    """2×2 matrix visual."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot([0.25,0.25],[0.20,0.80], color=GREY, lw=1.5, alpha=0.6)
    ax.plot([0.75,0.75],[0.20,0.80], color=GREY, lw=1.5, alpha=0.6)
    ax.plot([0.25,0.75],[0.50,0.50], color=GREY, lw=1.5, alpha=0.6)
    # Brackets
    ax.plot([0.18,0.18,0.18],[0.78,0.20,0.20], color=CYAN, lw=2.5)
    ax.plot([0.82,0.82,0.82],[0.78,0.20,0.20], color=CYAN, lw=2.5)
    entries = [("a","b","c","d")]
    for txt, pos in zip(["a","b","c","d"],
                        [(0.42,0.65),(0.60,0.65),(0.42,0.35),(0.60,0.35)]):
        ax.text(pos[0],pos[1], txt, color=YELLOW, fontsize=14,
                ha="center", va="center", fontweight="bold",
                alpha=min(1,progress*2))

def draw_lp_feasible(ax, progress=1.0):
    """Linear programming — feasible region."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.15, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.12, color=GREY, lw=0.8, alpha=0.4)
    if progress > 0.3:
        pts = np.array([[0.12,0.15],[0.12,0.68],[0.52,0.44],[0.72,0.15]])
        poly = plt.Polygon(pts, closed=True,
                           facecolor=(*plt.matplotlib.colors.to_rgb(CYAN),0.15),
                           edgecolor=CYAN, lw=1.8,
                           alpha=min(1,(progress-0.3)/0.4))
        ax.add_patch(poly)
    if progress > 0.7:
        for x,y in [(0.12,0.68),(0.52,0.44),(0.72,0.15)]:
            ax.plot(x,y,"o", color=YELLOW, markersize=7, zorder=3)
        ax.text(0.42,0.60,"optimal", color=YELLOW, fontsize=6.5)

def draw_quadratic_parabola(ax, progress=1.0):
    """Parabola y = ax²+bx+c with roots."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.50, color=GREY, lw=0.8, alpha=0.5)
    ax.axvline(0.50, color=GREY, lw=0.8, alpha=0.5)
    x = np.linspace(0, progress, 200)
    y = 0.80 - 1.20*(x-0.5*progress)**2 / (0.5*progress+0.01)**2 * 0.60
    ax.plot(0.08+x*0.84, y, color=CYAN, lw=2.5)
    if progress > 0.6:
        ax.plot(0.08+0.18*0.84, 0.50,"o", color=YELLOW, markersize=7)
        ax.plot(0.08+0.82*0.84, 0.50,"o", color=YELLOW, markersize=7)
        ax.text(0.22,0.44,"α", color=YELLOW, fontsize=9, ha="center")
        ax.text(0.78,0.44,"β", color=YELLOW, fontsize=9, ha="center")

def draw_trig_circle(ax, progress=1.0):
    """Unit circle with sin/cos labels."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.axhline(0.50, color=GREY, lw=0.8, alpha=0.4)
    ax.axvline(0.50, color=GREY, lw=0.8, alpha=0.4)
    circ = plt.Circle((0.50,0.50), 0.35, fill=False, edgecolor=CYAN, lw=2)
    ax.add_patch(circ)
    theta = math.pi/4 * min(1,progress)
    px = 0.50 + 0.35*math.cos(theta)
    py = 0.50 + 0.35*math.sin(theta)
    if progress > 0.2:
        ax.plot([0.50,px],[0.50,py], color=YELLOW, lw=2.5)
        ax.plot(px,py,"o", color=YELLOW, markersize=7)
    if progress > 0.6:
        ax.plot([px,px],[0.50,py], color=GREEN, lw=2, ls="--")
        ax.plot([0.50,px],[0.50,0.50], color=ORANGE, lw=2, ls="--")
        ax.text(px+0.05, (0.50+py)/2, "sin θ", color=GREEN, fontsize=7)
        ax.text((0.50+px)/2, 0.42, "cos θ", color=ORANGE, fontsize=7)

# ═══════════════════════════════════════════════════════════════════════════════
#  COMPUTER SCIENCE
# ═══════════════════════════════════════════════════════════════════════════════

def draw_logic_gate_and(ax, progress=1.0):
    """AND gate symbol."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    # Body
    body = mpatches.FancyBboxPatch((0.28,0.30),0.28,0.40,
                                    boxstyle="round,pad=0.02",
                                    facecolor="#0d1e38", edgecolor=CYAN, lw=2.5)
    ax.add_patch(body)
    # D-shape arc
    arc = Arc((0.56,0.50),0.30,0.40, angle=0, theta1=-90, theta2=90,
              color=CYAN, lw=2.5)
    ax.add_patch(arc)
    # Inputs
    ax.plot([0.08,0.28],[0.62,0.62], color=GREY, lw=2)
    ax.plot([0.08,0.28],[0.38,0.38], color=GREY, lw=2)
    ax.text(0.05,0.62,"A", color=CYAN, fontsize=9, ha="center", va="center", fontweight="bold")
    ax.text(0.05,0.38,"B", color=CYAN, fontsize=9, ha="center", va="center", fontweight="bold")
    # Output
    if progress > 0.5:
        ax.plot([0.71,0.92],[0.50,0.50], color=GREEN, lw=2)
        ax.text(0.95,0.50,"Y", color=GREEN, fontsize=9, ha="center", va="center", fontweight="bold")
    ax.text(0.42,0.50,"AND", color=WHITE, fontsize=7, ha="center", va="center")

def draw_logic_gate_or(ax, progress=1.0):
    """OR gate symbol."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot([0.08,0.28],[0.62,0.62], color=GREY, lw=2)
    ax.plot([0.08,0.28],[0.38,0.38], color=GREY, lw=2)
    ax.text(0.05,0.62,"A", color=CYAN, fontsize=9, ha="center", fontweight="bold")
    ax.text(0.05,0.38,"B", color=CYAN, fontsize=9, ha="center", fontweight="bold")
    # Curved body
    theta = np.linspace(-math.pi/3, math.pi/3, 50)
    ax.plot(0.28+0.40*np.cos(theta), 0.50+0.60*np.sin(theta), color=PURPLE, lw=2.5)
    ax.plot([0.28,0.28],[0.30,0.70], color=PURPLE, lw=2.5)
    # Curved back
    ax.plot(0.18+0.15*np.cos(theta), 0.50+0.60*np.sin(theta), color=PURPLE, lw=2.5)
    if progress > 0.5:
        ax.plot([0.68,0.92],[0.50,0.50], color=GREEN, lw=2)
        ax.text(0.95,0.50,"Y", color=GREEN, fontsize=9, ha="center", fontweight="bold")

def draw_truth_table(ax, progress=1.0):
    """Truth table grid 2-input."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    headers = ["A","B","Y"]
    rows = [("0","0","0"),("0","1","1"),("1","0","1"),("1","1","0")]
    ax.plot([0.08,0.92],[0.82,0.82], color=CYAN, lw=1.5)
    ax.plot([0.08,0.92],[0.68,0.68], color=GREY, lw=0.8, alpha=0.4)
    for i,h in enumerate(headers):
        x = 0.20 + i*0.26
        ax.text(x,0.88,h, color=CYAN, fontsize=10, ha="center", fontweight="bold")
    n_rows = max(1, int(4*progress))
    for r,(a,b,y) in enumerate(rows[:n_rows]):
        yr = 0.70 - r*0.15
        for i,v in enumerate([a,b,y]):
            x = 0.20 + i*0.26
            col = GREEN if v=="1" else RED
            ax.text(x, yr, v, color=col, fontsize=10, ha="center", fontweight="bold")

def draw_binary_tree(ax, progress=1.0):
    """Binary search tree."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    nodes = [(0.50,0.82,"5"),(0.28,0.60,"3"),(0.72,0.60,"8"),
             (0.17,0.38,"1"),(0.39,0.38,"4"),(0.61,0.38,"7"),(0.83,0.38,"9")]
    edges = [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]
    n_show = max(1, int(len(nodes)*progress))
    for i,j in edges:
        if i < n_show and j < n_show:
            ax.plot([nodes[i][0],nodes[j][0]],[nodes[i][1],nodes[j][1]],
                    color=GREY, lw=1.5, alpha=0.6)
    for k,(x,y,lbl) in enumerate(nodes[:n_show]):
        ax.plot(x,y,"o", color=BLUE, markersize=16)
        ax.text(x,y,lbl, color=WHITE, fontsize=8, ha="center", va="center", fontweight="bold")

def draw_network_topology(ax, progress=1.0):
    """Star network topology."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.plot(0.50,0.50,"s", color=ORANGE, markersize=14)
    ax.text(0.50,0.50,"Hub", color=WHITE, fontsize=6, ha="center", va="center")
    nodes = [(0.50,0.85),(0.85,0.65),(0.80,0.25),(0.50,0.14),(0.20,0.25),(0.15,0.65)]
    n_show = max(1, int(len(nodes)*progress))
    for x,y in nodes[:n_show]:
        ax.plot([0.50,x],[0.50,y], color=CYAN, lw=1.5, alpha=0.7)
        ax.plot(x,y,"o", color=CYAN, markersize=9)

def draw_ip_address(ax, progress=1.0):
    """IPv4 address structure."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    octets = ["192","168","1","1"]
    for i,o in enumerate(octets):
        alpha = min(1, progress*(i+1)/4*2)
        x = 0.10 + i*0.22
        ax.add_patch(FancyBboxPatch((x,0.38),0.18,0.24,
                                    boxstyle="round,pad=0.02",
                                    facecolor="#0d1e38", edgecolor=CYAN, lw=1.8,
                                    alpha=alpha))
        ax.text(x+0.09, 0.50, o, color=YELLOW, fontsize=11,
                ha="center", va="center", fontweight="bold", alpha=alpha)
        if i < 3:
            ax.text(x+0.21, 0.50, ".", color=WHITE, fontsize=14,
                    ha="center", va="center", alpha=alpha)
    ax.text(0.50,0.80,"IPv4 Address", color=GREY, fontsize=8, ha="center")
    ax.text(0.50,0.22,"32 bits = 4 octets × 8 bits", color=GREY, fontsize=7, ha="center")

def draw_sql_table(ax, progress=1.0):
    """Mini SQL table grid."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    cols = ["ID","Name","Marks"]
    data = [("1","Arjun","95"),("2","Priya","88"),("3","Raj","76")]
    # Header
    for i,c in enumerate(cols):
        x = 0.15 + i*0.27
        ax.add_patch(FancyBboxPatch((x-0.01,0.75),0.24,0.14,
                                    boxstyle="round,pad=0.01",
                                    facecolor=BLUE, edgecolor="none"))
        ax.text(x+0.11,0.82,c, color=WHITE, fontsize=8, ha="center", va="center", fontweight="bold")
    n_rows = max(1,int(3*progress))
    for r,row in enumerate(data[:n_rows]):
        y = 0.60 - r*0.17
        for i,v in enumerate(row):
            x = 0.15 + i*0.27
            col = YELLOW if i==0 else WHITE
            ax.text(x+0.11, y, v, color=col, fontsize=8, ha="center", va="center")
        ax.axhline(y-0.07, color=GREY, lw=0.6, alpha=0.4, xmin=0.12, xmax=0.92)

def draw_code_block(ax, progress=1.0):
    """Python code snippet visual."""
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.05,0.10),0.90,0.80,
                                boxstyle="round,pad=0.02",
                                facecolor="#0a0f1a", edgecolor=GREY, lw=1.5))
    lines = [
        ("def ",PURPLE),("  result",WHITE),("  return",CYAN),("  #list",GREEN),
    ]
    n_show = max(1,int(4*progress))
    for i,(txt,col) in enumerate(lines[:n_show]):
        ax.text(0.12, 0.78-i*0.17, txt, color=col, fontsize=8,
                fontfamily="monospace", va="center")

# ═══════════════════════════════════════════════════════════════════════════════
#  MASTER REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════

DIAGRAMS: dict[str, callable] = {
    # Physics
    "field_lines":        draw_field_lines,
    "parallel_plates":    draw_parallel_plates,
    "circuit_loop":       draw_circuit_loop,
    "wheatstone":         draw_wheatstone,
    "power_triangle":     draw_power_triangle,
    "mirror_optics":      draw_mirror_optics,
    "snell":              draw_snell,
    "young_fringes":      draw_young_fringes,
    "pn_junction":        draw_pn_junction,
    "transistor":         draw_transistor,
    "de_broglie":         draw_de_broglie,
    "photoelectric":      draw_photoelectric,
    "bohr_atom":          draw_bohr_atom,
    "radioactive_decay":  draw_radioactive_decay,
    # Legacy physics (kept for backward compat)
    "flux":               draw_field_lines,
    "coil_magnet":        draw_circuit_loop,
    "lenz":               draw_snell,
    "motional":           draw_parallel_plates,
    "inductor":           draw_radioactive_decay,
    "ohm":                draw_power_triangle,
    "wire":               draw_circuit_loop,
    "loop":               draw_circuit_loop,
    "bridge":             draw_wheatstone,
    "power":              draw_power_triangle,
    # Chemistry
    "reaction_coordinate": draw_reaction_coordinate,
    "first_order_decay":   draw_first_order_decay,
    "half_life_chem":      draw_half_life,
    "arrhenius":           draw_arrhenius,
    "electrolytic_cell":   draw_electrolytic_cell,
    "conductance_plot":    draw_conductance_plot,
    "vapour_pressure":     draw_vapour_pressure,
    "boiling_point":       draw_boiling_point,
    "osmosis":             draw_osmosis,
    "crystal_lattice":     draw_crystal_lattice,
    "coordination_sphere": draw_coordination_sphere,
    # Biology
    "punnett_square":      draw_punnett_square,
    "dna_helix":           draw_dna_helix,
    "cell_division":       draw_cell_division,
    "leaf_cross_section":  draw_leaf_cross_section,
    "food_chain":          draw_food_chain,
    "population_growth":   draw_population_growth,
    "hormone_feedback":    draw_hormone_feedback,
    # Mathematics
    "function_curve":      draw_function_curve,
    "tangent_line":        draw_tangent_line,
    "integration_area":    draw_integration_area,
    "vector_diagram":      draw_vector_diagram,
    "cross_product":       draw_cross_product,
    "probability_tree":    draw_probability_tree,
    "matrix_grid":         draw_matrix_grid,
    "lp_feasible":         draw_lp_feasible,
    "quadratic_parabola":  draw_quadratic_parabola,
    "trig_circle":         draw_trig_circle,
    # CS
    "logic_gate_and":      draw_logic_gate_and,
    "logic_gate_or":       draw_logic_gate_or,
    "truth_table":         draw_truth_table,
    "binary_tree":         draw_binary_tree,
    "network_topology":    draw_network_topology,
    "ip_address":          draw_ip_address,
    "sql_table":           draw_sql_table,
    "code_block":          draw_code_block,
}
