"""
diagrams_feb.py — extra Formula Flash diagrams for the Jan–Feb 2027 chapters.

Same contract as diagram_library: draw_xyz(ax, progress=1.0) on a 0..1 box; the reel
scales text ×2.5 and lines ×2.0. Factories (rx, fn_tangent, ...) return a draw function
so one style can show different content. Importing this module registers everything
in diagram_library.DIAGRAMS.
"""
import math
from functools import partial

import numpy as np
from matplotlib.patches import Ellipse, Rectangle, Polygon, Circle, FancyBboxPatch, Wedge, Arc

from diagram_library import (DIAGRAMS, CYAN, YELLOW, ORANGE, WHITE, GREY, GREEN, PINK, PURPLE, RED, BLUE,
                             _setup, _fade, _arrow, _ball, _ring, _zig, _t, _K)

NAVY = "#06101f"


def _box(ax, x, y, w, h, color, fill=None, lw=1.6, alpha=1.0, r=0.03):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                facecolor=fill or "#0e1d3f", edgecolor=color, linewidth=lw, alpha=alpha, zorder=3))


def _axes(ax, x0=0.10, y0=0.14, x1=0.92, y1=0.88, color=GREY):
    _arrow(ax, (x0, y0), (x1, y0), color, lw=1.3)
    _arrow(ax, (x0, y0), (x0, y1), color, lw=1.3)


def _sub(s):
    return s.translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))


# ═══ PHYSICS ═════════════════════════════════════════════════════════════════
def draw_ac_sine(ax, progress=1.0):
    _setup(ax); _axes(ax, y0=0.5, y1=0.92)
    ax.plot([0.10, 0.10], [0.08, 0.5], color=GREY, lw=1.3)
    n = max(2, int(300 * min(1, progress * 1.3)))
    x = np.linspace(0.10, 0.90, 300)[:n]
    ax.plot(x, 0.5 + 0.33 * np.sin((x - 0.10) / 0.8 * 4 * math.pi), color=CYAN, lw=2)
    a = _fade(progress, 0.4)
    ax.plot([0.10, 0.90], [0.5 + 0.33, 0.5 + 0.33], color=YELLOW, lw=1, ls=":", alpha=a)
    ax.plot([0.10, 0.90], [0.5 + 0.233, 0.5 + 0.233], color=GREEN, lw=1.4, ls="--", alpha=a)
    _t(ax, 0.95, 0.83, "I₀", YELLOW, fs=8, alpha=a); _t(ax, 0.96, 0.73, "Iᵣₘₛ", GREEN, fs=8, alpha=a)


def draw_impedance_triangle(ax, progress=1.0):
    _setup(ax)
    a = _fade(progress, 0.0)
    ax.plot([0.15, 0.80], [0.18, 0.18], color=GREEN, lw=2.2)
    ax.plot([0.80, 0.80], [0.18, 0.18 + 0.62 * a], color=ORANGE, lw=2.2)
    if a > 0.5:
        ax.plot([0.15, 0.80], [0.18, 0.80], color=CYAN, lw=2.4)
        _t(ax, 0.40, 0.56, "Z", CYAN, fs=11, fontweight="bold")
    _t(ax, 0.48, 0.09, "R", GREEN, fs=10, fontweight="bold")
    _t(ax, 0.92, 0.49, "Xₗ − Xc", ORANGE, fs=8, rotation=90)
    ax.add_patch(Arc((0.15, 0.18), 0.22, 0.26, theta1=0, theta2=44, color=YELLOW, lw=1.4))
    _t(ax, 0.31, 0.24, "φ", YELLOW, fs=9)


def draw_resonance_curve(ax, progress=1.0):
    _setup(ax); _axes(ax)
    x = np.linspace(0.12, 0.90, 300)
    n = max(2, int(300 * min(1, progress * 1.3)))
    y = 0.16 + 0.66 / (1 + ((x - 0.5) / 0.07) ** 2)
    ax.plot(x[:n], y[:n], color=PINK, lw=2)
    a = _fade(progress, 0.5)
    ax.plot([0.5, 0.5], [0.14, 0.82], color=YELLOW, lw=1, ls="--", alpha=a)
    _t(ax, 0.5, 0.07, "ω₀", YELLOW, fs=9, alpha=a); _t(ax, 0.94, 0.07, "ω", GREY, fs=8); _t(ax, 0.05, 0.88, "I", GREY, fs=8)
    _t(ax, 0.72, 0.80, "max current", PINK, fs=7, alpha=a)


def draw_transformer(ax, progress=1.0):
    _setup(ax)
    ax.add_patch(Rectangle((0.30, 0.20), 0.40, 0.60, fill=False, edgecolor=GREY, linewidth=7))
    for k in range(5):
        ax.add_patch(Ellipse((0.30, 0.32 + k * 0.09), 0.12, 0.05, fill=False, edgecolor=CYAN, linewidth=1.6))
    for k in range(8):
        ax.add_patch(Ellipse((0.70, 0.27 + k * 0.065), 0.12, 0.04, fill=False, edgecolor=ORANGE, linewidth=1.6))
    _t(ax, 0.14, 0.50, "Nₚ\nprimary", CYAN, fs=7); _t(ax, 0.87, 0.50, "Nₛ\nsecondary", ORANGE, fs=7)
    _t(ax, 0.50, 0.08, "step-up: Nₛ > Nₚ", GREEN, fs=7, alpha=_fade(progress, 0.4))


def draw_em_wave(ax, progress=1.0):
    _setup(ax)
    ax.plot([0.06, 0.94], [0.5, 0.5], color=GREY, lw=1)
    n = max(2, int(300 * min(1, progress * 1.3)))
    x = np.linspace(0.08, 0.92, 300)[:n]
    s = np.sin((x - 0.08) / 0.84 * 4 * math.pi)
    ax.plot(x, 0.5 + 0.32 * s, color=CYAN, lw=2)
    ax.plot(x + 0.06 * s, 0.5 - 0.10 * s, color=PINK, lw=1.8)
    _t(ax, 0.30, 0.90, "E (electric)", CYAN, fs=7); _t(ax, 0.72, 0.18, "B (magnetic)", PINK, fs=7)
    _arrow(ax, (0.78, 0.92), (0.95, 0.92), YELLOW, lw=1.6); _t(ax, 0.86, 0.84, "c", YELLOW, fs=9)


def draw_wave_lambda(ax, progress=1.0):
    _setup(ax)
    n = max(2, int(300 * min(1, progress * 1.3)))
    x = np.linspace(0.06, 0.94, 300)[:n]
    ax.plot(x, 0.5 + 0.25 * np.sin((x - 0.06) / 0.88 * 6 * math.pi), color=CYAN, lw=2)
    a = _fade(progress, 0.5)
    lam = 0.88 / 3
    _arrow(ax, (0.06 + lam * 0.25, 0.84), (0.06 + lam * 1.25, 0.84), YELLOW, lw=1.4, style="<->", alpha=a)
    _t(ax, 0.06 + lam * 0.75, 0.92, "λ", YELLOW, fs=10, alpha=a)
    _t(ax, 0.50, 0.10, "ν waves pass per second", GREEN, fs=7, alpha=a)


def draw_em_spectrum(ax, progress=1.0):
    _setup(ax)
    names = ["Radio", "Micro", "IR", "Visible", "UV", "X-ray", "γ"]
    cols = [RED, ORANGE, "#ff9f43", GREEN, PURPLE, BLUE, PINK]
    show = max(1, int(7 * min(1.0, progress * 1.3)))
    for i in range(show):
        x = 0.10 + i * 0.13
        ax.add_patch(Rectangle((x - 0.06, 0.42), 0.12, 0.22, facecolor=cols[i], edgecolor="none", alpha=0.9))
        _t(ax, x, 0.53, names[i], NAVY, fs=5.5, fontweight="bold", rotation=90 if len(names[i]) > 4 else 0)
    a = _fade(progress, 0.5)
    _arrow(ax, (0.06, 0.28), (0.94, 0.28), YELLOW, lw=1.4, alpha=a); _t(ax, 0.50, 0.20, "λ decreases →  energy increases", YELLOW, fs=7, alpha=a)


def draw_single_slit(ax, progress=1.0):
    _setup(ax)
    ax.plot([0.25, 0.25], [0.08, 0.44], color=WHITE, lw=3); ax.plot([0.25, 0.25], [0.56, 0.92], color=WHITE, lw=3)
    for y in (0.3, 0.5, 0.7):
        ax.plot([0.04, 0.24], [y, y], color=YELLOW, lw=1, alpha=0.6)
    ax.plot([0.88, 0.88], [0.06, 0.94], color=GREY, lw=1.2)
    a = _fade(progress, 0.2)
    y = np.linspace(0.06, 0.94, 200)
    I = np.sinc((y - 0.5) * 9) ** 2
    ax.plot(0.88 - 0.25 * I * a, y, color=CYAN, lw=1.8)
    _t(ax, 0.20, 0.50, "a", YELLOW, fs=9); _t(ax, 0.62, 0.92, "central max", CYAN, fs=7, alpha=a)


def draw_brewster(ax, progress=1.0):
    _setup(ax)
    ax.add_patch(Rectangle((0.0, 0.0), 1.0, 0.45, facecolor="#123a66", edgecolor="none", alpha=0.7))
    ax.plot([0.5, 0.5], [0.15, 0.95], color=GREY, lw=1, ls="--")
    _arrow(ax, (0.18, 0.88), (0.5, 0.45), YELLOW, lw=2)
    a = _fade(progress, 0.3)
    _arrow(ax, (0.5, 0.45), (0.82, 0.88), GREEN, lw=2, alpha=a)
    _arrow(ax, (0.5, 0.45), (0.64, 0.08), CYAN, lw=2, alpha=a)
    _t(ax, 0.86, 0.94, "fully polarised", GREEN, fs=7, alpha=a)
    _t(ax, 0.42, 0.66, "iB", YELLOW, fs=8); _t(ax, 0.72, 0.30, "90°", PINK, fs=8, alpha=a)


def draw_malus(ax, progress=1.0):
    _setup(ax)
    for x, ang, lab in ((0.30, 0, "P₁"), (0.68, 50 * progress, "P₂")):
        ax.add_patch(Ellipse((x, 0.52), 0.16, 0.56, fill=False, edgecolor=CYAN, linewidth=2))
        r = math.radians(ang)
        ax.plot([x - 0.0, x], [0.52 - 0.22, 0.52 + 0.22], color=GREY, lw=0.8, alpha=0.4)
        ax.plot([x - 0.18 * math.sin(r) * _K, x + 0.18 * math.sin(r) * _K], [0.52 - 0.22 * math.cos(r), 0.52 + 0.22 * math.cos(r)],
                color=YELLOW, lw=2)
        _t(ax, x, 0.12, lab, CYAN, fs=8)
    ax.plot([0.04, 0.22], [0.52, 0.52], color=WHITE, lw=2.5)
    ax.plot([0.38, 0.60], [0.52, 0.52], color=WHITE, lw=2)
    ax.plot([0.76, 0.96], [0.52, 0.52], color=WHITE, lw=2 * max(0.2, math.cos(math.radians(50 * progress)) ** 2), alpha=0.9)
    _t(ax, 0.68, 0.92, "θ", YELLOW, fs=9)


def draw_gauss_sphere(ax, progress=1.0):
    _setup(ax)
    _ball(ax, 0.5, 0.5, 0.06, YELLOW, "+q", fs=7)
    _ring(ax, 0.5, 0.5, 0.30, CYAN, lw=1.8, ls="--")
    a = _fade(progress, 0.2)
    for k in range(12):
        t = 2 * math.pi * k / 12
        _arrow(ax, (0.5 + 0.08 * math.cos(t) * _K, 0.5 + 0.08 * math.sin(t)),
               (0.5 + 0.42 * math.cos(t) * _K, 0.5 + 0.42 * math.sin(t)), ORANGE, lw=1.2, alpha=a)
    _t(ax, 0.84, 0.12, "Gaussian surface", CYAN, fs=7)


def draw_line_charge(ax, progress=1.0):
    _setup(ax)
    ax.plot([0.5, 0.5], [0.04, 0.96], color=YELLOW, lw=3)
    for y in np.linspace(0.12, 0.88, 7):
        _t(ax, 0.5, y, "+", NAVY, fs=7, fontweight="bold")
    a = _fade(progress, 0.2)
    for y in np.linspace(0.18, 0.82, 4):
        _arrow(ax, (0.53, y), (0.88, y), ORANGE, lw=1.3, alpha=a); _arrow(ax, (0.47, y), (0.12, y), ORANGE, lw=1.3, alpha=a)
    ax.add_patch(Ellipse((0.5, 0.5), 0.5, 0.55, fill=False, edgecolor=CYAN, lw=1.4, ls="--"))
    _t(ax, 0.5, 0.0, "r", CYAN, fs=8); _t(ax, 0.66, 0.95, "λ (C/m)", YELLOW, fs=7)


def draw_charged_sheet(ax, progress=1.0):
    _setup(ax)
    ax.add_patch(Polygon([[0.42, 0.10], [0.58, 0.22], [0.58, 0.94], [0.42, 0.82]], closed=True, facecolor=YELLOW,
                         edgecolor="none", alpha=0.6))
    a = _fade(progress, 0.2)
    for y in np.linspace(0.25, 0.75, 4):
        _arrow(ax, (0.6, y + 0.05), (0.92, y + 0.05), ORANGE, lw=1.4, alpha=a)
        _arrow(ax, (0.4, y), (0.08, y), ORANGE, lw=1.4, alpha=a)
    _t(ax, 0.5, 0.04, "σ (C/m²)", YELLOW, fs=7); _t(ax, 0.82, 0.94, "same E\nboth sides", GREEN, fs=6, alpha=a)


def draw_dipole(ax, progress=1.0):
    _setup(ax)
    _ball(ax, 0.32, 0.5, 0.07, RED, "−q", tcolor=WHITE, fs=7); _ball(ax, 0.68, 0.5, 0.07, BLUE, "+q", tcolor=WHITE, fs=7)
    a = _fade(progress, 0.2)
    th = np.linspace(0.15, math.pi - 0.15, 60)
    for s in (0.18, 0.30):
        ax.plot(0.5 - 0.18 * np.cos(th) * 1.0, 0.5 + s * np.sin(th), color=CYAN, lw=1, alpha=a)
        ax.plot(0.5 - 0.18 * np.cos(th) * 1.0, 0.5 - s * np.sin(th), color=CYAN, lw=1, alpha=a)
    _arrow(ax, (0.36, 0.22), (0.64, 0.22), YELLOW, lw=1.6); _t(ax, 0.5, 0.13, "p = q·2a", YELLOW, fs=8)
    ax.plot([0.75, 0.97], [0.5, 0.5], color=GREEN, lw=1, ls=":", alpha=a); _t(ax, 0.88, 0.58, "axis", GREEN, fs=7, alpha=a)


def _cap(ax, x, y, h=0.18, color=CYAN, lab=""):
    ax.plot([x - 0.02, x - 0.02], [y - h / 2, y + h / 2], color=color, lw=2.4)
    ax.plot([x + 0.02, x + 0.02], [y - h / 2, y + h / 2], color=color, lw=2.4)
    if lab:
        _t(ax, x, y + h / 2 + 0.07, lab, color, fs=7)


def draw_cap_series(ax, progress=1.0):
    _setup(ax)
    ax.plot([0.06, 0.30], [0.55, 0.55], color=WHITE, lw=1.4); ax.plot([0.34, 0.66], [0.55, 0.55], color=WHITE, lw=1.4)
    ax.plot([0.70, 0.94], [0.55, 0.55], color=WHITE, lw=1.4)
    _cap(ax, 0.32, 0.55, lab="C₁"); _cap(ax, 0.68, 0.55, lab="C₂", color=ORANGE)
    _t(ax, 0.5, 0.20, "same charge Q on each", GREEN, fs=7, alpha=_fade(progress, 0.4))


def draw_cap_parallel(ax, progress=1.0):
    _setup(ax)
    ax.plot([0.10, 0.10], [0.30, 0.78], color=WHITE, lw=1.4); ax.plot([0.90, 0.90], [0.30, 0.78], color=WHITE, lw=1.4)
    for y, c, lab in ((0.78, CYAN, "C₁"), (0.30, ORANGE, "C₂")):
        ax.plot([0.10, 0.48], [y, y], color=WHITE, lw=1.4); ax.plot([0.52, 0.90], [y, y], color=WHITE, lw=1.4)
        _cap(ax, 0.5, y, h=0.14, color=c, lab=lab)
    _t(ax, 0.5, 0.10, "same voltage V across each", GREEN, fs=7, alpha=_fade(progress, 0.4))


def draw_circular_motion_B(ax, progress=1.0):
    _setup(ax)
    for x in np.linspace(0.1, 0.9, 6):
        for y in np.linspace(0.1, 0.9, 6):
            _t(ax, x, y, "×", GREY, fs=7, alpha=0.5)
    ang = 2 * math.pi * min(1, progress * 1.2)
    t = np.linspace(0, ang, 120)
    ax.plot(0.5 + 0.3 * np.cos(t) * _K, 0.5 + 0.3 * np.sin(t), color=CYAN, lw=2)
    _ball(ax, 0.5 + 0.3 * math.cos(ang) * _K, 0.5 + 0.3 * math.sin(ang), 0.04, YELLOW, "+", fs=7)
    ax.plot([0.5, 0.5 + 0.3 * _K], [0.5, 0.5], color=PINK, lw=1.2, ls="--"); _t(ax, 0.62, 0.45, "r", PINK, fs=8)
    _t(ax, 0.88, 0.95, "B into page", GREY, fs=6)


def draw_parallel_wires(ax, progress=1.0):
    _setup(ax)
    for x in (0.32, 0.68):
        ax.plot([x, x], [0.08, 0.92], color=ORANGE, lw=3)
        _arrow(ax, (x + 0.05, 0.45), (x + 0.05, 0.70), YELLOW, lw=1.4)
    _t(ax, 0.40, 0.58, "I₁", YELLOW, fs=8); _t(ax, 0.76, 0.58, "I₂", YELLOW, fs=8)
    a = _fade(progress, 0.3)
    _arrow(ax, (0.30, 0.30), (0.42, 0.30), GREEN, lw=2, alpha=a); _arrow(ax, (0.70, 0.30), (0.58, 0.30), GREEN, lw=2, alpha=a)
    _arrow(ax, (0.32, 0.14), (0.68, 0.14), CYAN, lw=1.2, style="<->"); _t(ax, 0.5, 0.06, "d", CYAN, fs=8)
    _t(ax, 0.5, 0.94, "same direction → attract", GREEN, fs=7, alpha=a)


def draw_coil_torque(ax, progress=1.0):
    _setup(ax)
    ax.add_patch(Rectangle((0.06, 0.25), 0.12, 0.5, facecolor=RED, edgecolor="none")); _t(ax, 0.12, 0.5, "N", fs=9, fontweight="bold")
    ax.add_patch(Rectangle((0.82, 0.25), 0.12, 0.5, facecolor=BLUE, edgecolor="none")); _t(ax, 0.88, 0.5, "S", fs=9, fontweight="bold")
    w = 0.22 * abs(math.cos(progress * 1.2))
    ax.add_patch(Rectangle((0.5 - w, 0.30), 2 * w + 0.005, 0.40, fill=False, edgecolor=CYAN, linewidth=2.2))
    _arrow(ax, (0.36, 0.82), (0.64, 0.82), YELLOW, lw=1.6, style="->"); _t(ax, 0.5, 0.92, "rotates (τ)", YELLOW, fs=7)
    _t(ax, 0.5, 0.15, "B →", GREY, fs=8)


def draw_galvanometer(ax, progress=1.0):
    _setup(ax)
    _ball(ax, 0.5, 0.65, 0.12, "#0e1d3f", "G", tcolor=YELLOW, fs=11, ec=YELLOW)
    ax.plot([0.12, 0.38], [0.65, 0.65], color=WHITE, lw=1.4); ax.plot([0.62, 0.88], [0.65, 0.65], color=WHITE, lw=1.4)
    a = _fade(progress, 0.2)
    ax.plot([0.20, 0.20, 0.38], [0.65, 0.28, 0.28], color=WHITE, lw=1.4, alpha=a)
    ax.plot([0.62, 0.80, 0.80], [0.28, 0.28, 0.65], color=WHITE, lw=1.4, alpha=a)
    _zig(ax, 0.38, 0.62, 0.28, GREEN, amp=0.04)
    _t(ax, 0.5, 0.16, "shunt S (small)", GREEN, fs=7, alpha=a)
    _t(ax, 0.5, 0.90, "Iɡ through G", YELLOW, fs=7)


# ═══ CHEMISTRY ═══════════════════════════════════════════════════════════════
def draw_unpaired_electrons(ax, progress=1.0):
    _setup(ax)
    show = max(1, int(5 * min(1, progress * 1.4)))
    for k in range(5):
        x = 0.18 + k * 0.16
        ax.add_patch(Rectangle((x - 0.065, 0.40), 0.13, 0.22, fill=False, edgecolor=CYAN, linewidth=1.8))
        if k < show:
            _t(ax, x, 0.51, "↑", YELLOW, fs=12, fontweight="bold")
    _t(ax, 0.5, 0.76, "3d⁵ (e.g. Mn²⁺)", CYAN, fs=8)
    _t(ax, 0.5, 0.20, f"n = {show} unpaired", GREEN, fs=8)


def draw_orbital_boxes(ax, progress=1.0):
    _setup(ax)
    _t(ax, 0.13, 0.55, "ns", PINK, fs=9)
    ax.add_patch(Rectangle((0.20, 0.44), 0.10, 0.22, fill=False, edgecolor=PINK, linewidth=1.8)); _t(ax, 0.25, 0.55, "↑↓", YELLOW, fs=9)
    _t(ax, 0.40, 0.80, "(n−1)d", CYAN, fs=9)
    fill = int(10 * min(1, progress * 1.3))
    for k in range(5):
        x = 0.42 + k * 0.105
        ax.add_patch(Rectangle((x - 0.05, 0.44), 0.10, 0.22, fill=False, edgecolor=CYAN, linewidth=1.8))
        arr = ("↑" if fill > k else "") + ("↓" if fill > k + 5 else "")
        _t(ax, x, 0.55, arr, YELLOW, fs=9)
    _t(ax, 0.5, 0.18, "d-block: filling inner d orbitals", GREEN, fs=7, alpha=_fade(progress, 0.4))


def draw_size_trend(ax, progress=1.0):
    _setup(ax)
    els = ["La", "Ce", "Nd", "Sm", "Gd", "Dy", "Er", "Lu"]
    show = max(1, int(len(els) * min(1, progress * 1.3)))
    for k in range(show):
        x = 0.12 + k * 0.108
        r = 0.075 - k * 0.006
        _ball(ax, x, 0.55, r, CYAN if k < 7 else PINK, els[k], fs=6)
    _arrow(ax, (0.10, 0.25), (0.92, 0.25), YELLOW, lw=1.4, alpha=_fade(progress, 0.5))
    _t(ax, 0.5, 0.15, "atomic size decreases", YELLOW, fs=7, alpha=_fade(progress, 0.5))


def draw_ph_scale(ax, progress=1.0):
    _setup(ax)
    cols = ["#ff1f1f", "#ff4b2b", "#ff7a2b", "#ffa52b", "#ffd12b", "#e6f02b", "#9ce02b", "#3ddc97", "#2bd4c9",
            "#2bb0f0", "#2b7cf0", "#4b5cf0", "#6b45e0", "#8a35d0", "#a52bc0"]
    show = max(1, int(15 * min(1, progress * 1.3)))
    for k in range(show):
        x = 0.06 + k * 0.059
        ax.add_patch(Rectangle((x, 0.42), 0.057, 0.22, facecolor=cols[k], edgecolor="none"))
        if k % 2 == 0:
            _t(ax, x + 0.028, 0.34, str(k), WHITE, fs=6)
    a = _fade(progress, 0.6)
    _t(ax, 0.18, 0.78, "acidic", RED, fs=8, alpha=a); _t(ax, 0.5, 0.78, "7 neutral", GREEN, fs=8, alpha=a)
    _t(ax, 0.84, 0.78, "basic", PURPLE, fs=8, alpha=a)


def draw_carbon_chain(kind, ax, progress=1.0):
    _setup(ax)
    _ball(ax, 0.36, 0.5, 0.08, GREY, "C", tcolor=WHITE, fs=9); _ball(ax, 0.64, 0.5, 0.08, GREY, "C", tcolor=WHITE, fs=9)
    bonds = {"single": 1, "double": 2, "triple": 3}[kind]
    for k in range(bonds):
        dy = (k - (bonds - 1) / 2) * 0.05
        ax.plot([0.43, 0.57], [0.5 + dy, 0.5 + dy], color=YELLOW, lw=2.2)
    nH = {"single": 3, "double": 2, "triple": 1}[kind]
    a = _fade(progress, 0.2)
    angs = {3: (135, 180, 225), 2: (150, 210), 1: (180,)}[nH]
    for side, cx in ((-1, 0.36), (1, 0.64)):
        for g in angs:
            t = math.radians(g if side < 0 else 180 - g)
            hx, hy = cx + 0.20 * math.cos(t) * _K, 0.5 + 0.22 * math.sin(t)
            ax.plot([cx + 0.07 * math.cos(t) * _K, hx - 0.03 * math.cos(t)], [0.5 + 0.07 * math.sin(t), hy - 0.03 * math.sin(t)],
                    color=WHITE, lw=1.4, alpha=a)
            _ball(ax, hx, hy, 0.045, WHITE, "H", fs=6, alpha=a)
    name = {"single": "ethane C₂H₆", "double": "ethene C₂H₄", "triple": "ethyne C₂H₂"}[kind]
    _t(ax, 0.5, 0.10, name, CYAN, fs=8, alpha=a)


def draw_reactivity_ladder(ax, progress=1.0):
    _setup(ax)
    els = ["K", "Na", "Ca", "Mg", "Al", "Zn", "Fe", "Pb", "H", "Cu", "Ag", "Au"]
    show = max(1, int(len(els) * min(1, progress * 1.3)))
    for k in range(show):
        y = 0.93 - k * 0.072
        col = PINK if k < 3 else (ORANGE if k < 8 else (GREY if els[k] == "H" else YELLOW))
        ax.add_patch(Rectangle((0.32, y - 0.03), 0.20, 0.058, facecolor=col, edgecolor="none", alpha=0.85))
        _t(ax, 0.42, y, els[k], NAVY, fs=6.5, fontweight="bold")
    a = _fade(progress, 0.5)
    _arrow(ax, (0.68, 0.10), (0.68, 0.92), CYAN, lw=1.6, alpha=a)
    _t(ax, 0.84, 0.52, "more\nreactive", CYAN, fs=7, alpha=a)


def draw_rx(react, reagent, prod, ax, progress=1.0):
    """Reaction card: reactants → (reagent) → products."""
    _setup(ax)
    _box(ax, 0.5, 0.78, 0.86, 0.22, CYAN)
    _t(ax, 0.5, 0.78, react, WHITE, fs=8, fontweight="bold")
    a = _fade(progress, 0.15)
    _arrow(ax, (0.5, 0.64), (0.5, 0.38), YELLOW, lw=2.2, alpha=a)
    _t(ax, 0.53, 0.51, reagent, YELLOW, fs=7, ha="left", alpha=a)
    b = _fade(progress, 0.45)
    _box(ax, 0.5, 0.22, 0.86, 0.22, GREEN, alpha=b)
    _t(ax, 0.5, 0.22, prod, WHITE, fs=8, fontweight="bold", alpha=b)


# ═══ MATHS ═══════════════════════════════════════════════════════════════════
def draw_fn_tangent(f, df, label, x0, xr, ax, progress=1.0):
    """Graph of f with a tangent at x0 (xr = x-range)."""
    _setup(ax); _axes(ax, x0=0.08, y0=0.12)
    xs = np.linspace(xr[0], xr[1], 300); ys = f(xs)
    lo, hi = np.nanmin(ys), np.nanmax(ys)
    X = lambda x: 0.10 + (x - xr[0]) / (xr[1] - xr[0]) * 0.82
    Y = lambda y: 0.16 + (y - lo) / (hi - lo + 1e-9) * 0.70
    n = max(2, int(300 * min(1, progress * 1.3)))
    ax.plot(X(xs[:n]), Y(ys[:n]), color=CYAN, lw=2)
    a = _fade(progress, 0.5)
    m = df(x0) * (0.70 / (hi - lo)) / (0.82 / (xr[1] - xr[0]))
    px, py = X(x0), Y(f(x0))
    ax.plot([px - 0.16, px + 0.16], [py - 0.16 * m, py + 0.16 * m], color=YELLOW, lw=1.8, alpha=a)
    _ball(ax, px, py, 0.025, YELLOW, alpha=a)
    _t(ax, 0.72, 0.94, label, CYAN, fs=8)


def draw_area_fn(f, label, a_, b_, xr, ax, progress=1.0):
    _setup(ax); _axes(ax, x0=0.08, y0=0.12)
    xs = np.linspace(xr[0], xr[1], 300); ys = f(xs)
    lo, hi = min(0, np.nanmin(ys)), np.nanmax(ys)
    X = lambda x: 0.10 + (x - xr[0]) / (xr[1] - xr[0]) * 0.82
    Y = lambda y: 0.14 + (y - lo) / (hi - lo + 1e-9) * 0.72
    ax.plot(X(xs), Y(ys), color=CYAN, lw=2)
    sa = _fade(progress, 0.2)
    xa = np.linspace(a_, a_ + (b_ - a_) * sa, 100)
    if len(xa) > 1:
        ax.fill_between(X(xa), Y(0), Y(f(xa)), color=YELLOW, alpha=0.35)
    _t(ax, 0.70, 0.94, label, CYAN, fs=8)


def draw_slope_field(ax, progress=1.0):
    _setup(ax); _axes(ax)
    a = _fade(progress, 0.0)
    for x in np.linspace(0.18, 0.86, 7):
        for y in np.linspace(0.22, 0.82, 6):
            m = (y - 0.14) * 1.8
            d = 0.035 / math.sqrt(1 + m * m)
            ax.plot([x - d, x + d], [y - m * d, y + m * d], color=GREY, lw=1, alpha=a)
    xs = np.linspace(0.12, 0.90, 200)
    b = _fade(progress, 0.4)
    ax.plot(xs, 0.18 + 0.05 * np.exp((xs - 0.12) * 3.2), color=GREEN, lw=2, alpha=b)
    _t(ax, 0.62, 0.92, "solution curve", GREEN, fs=7, alpha=b)


def draw_inverse_sine(ax, progress=1.0):
    _setup(ax)
    ax.plot([0.08, 0.92], [0.5, 0.5], color=GREY, lw=1.2); ax.plot([0.5, 0.5], [0.06, 0.94], color=GREY, lw=1.2)
    x = np.linspace(-1, 1, 200)
    n = max(2, int(200 * min(1, progress * 1.3)))
    ax.plot(0.5 + x[:n] * 0.32, 0.5 + np.arcsin(x[:n]) / (math.pi / 2) * 0.38, color=CYAN, lw=2.2)
    a = _fade(progress, 0.5)
    _t(ax, 0.86, 0.90, "π/2", YELLOW, fs=8, alpha=a); _t(ax, 0.16, 0.10, "−π/2", YELLOW, fs=8, alpha=a)
    _t(ax, 0.84, 0.44, "1", WHITE, fs=8); _t(ax, 0.17, 0.56, "−1", WHITE, fs=8)
    _t(ax, 0.30, 0.86, "y = sin⁻¹x", CYAN, fs=8)


def draw_inc_dec(ax, progress=1.0):
    _setup(ax); _axes(ax)
    xs = np.linspace(0.12, 0.90, 300)
    ys = 0.5 + 0.30 * np.sin((xs - 0.12) / 0.78 * 2 * math.pi - 0.6)
    n = max(2, int(300 * min(1, progress * 1.3)))
    up = np.gradient(ys) >= 0
    for i in range(1, n):
        ax.plot(xs[i - 1:i + 1], ys[i - 1:i + 1], color=GREEN if up[i] else PINK, lw=2.4)
    a = _fade(progress, 0.6)
    _t(ax, 0.24, 0.84, "f′ > 0 ↑", GREEN, fs=8, alpha=a); _t(ax, 0.62, 0.84, "f′ < 0 ↓", PINK, fs=8, alpha=a)


def draw_ap_steps(ax, progress=1.0):
    _setup(ax)
    show = max(1, int(6 * min(1, progress * 1.3)))
    for k in range(show):
        h = 0.10 + k * 0.12
        x = 0.12 + k * 0.135
        ax.add_patch(Rectangle((x, 0.12), 0.11, h, facecolor=CYAN if k else YELLOW, edgecolor=NAVY, alpha=0.85))
        _t(ax, x + 0.055, 0.12 + h + 0.05, ["a", "a+d", "a+2d", "a+3d", "a+4d", "a+5d"][k], WHITE, fs=6)
    a = _fade(progress, 0.6)
    _t(ax, 0.5, 0.94, "each step adds d", GREEN, fs=8, alpha=a)


def draw_coord_distance(ax, progress=1.0):
    _setup(ax); _axes(ax)
    A, B = (0.24, 0.26), (0.78, 0.74)
    a = _fade(progress, 0.2)
    ax.plot([A[0], B[0], B[0]], [A[1], A[1], B[1]], color=GREY, lw=1.2, ls="--", alpha=a)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=CYAN, lw=2.2)
    _ball(ax, *A, 0.025, YELLOW); _ball(ax, *B, 0.025, YELLOW)
    _t(ax, A[0] - 0.04, A[1] + 0.07, "A(x₁,y₁)", YELLOW, fs=7); _t(ax, B[0] - 0.02, B[1] + 0.07, "B(x₂,y₂)", YELLOW, fs=7)
    _t(ax, 0.51, 0.19, "x₂ − x₁", GREEN, fs=7, alpha=a); _t(ax, 0.87, 0.50, "y₂ − y₁", ORANGE, fs=7, rotation=90, alpha=a)


def draw_coord_section(ax, progress=1.0):
    _setup(ax)
    A, B = (0.12, 0.30), (0.88, 0.70)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=CYAN, lw=2)
    f = 0.4
    P = (A[0] + (B[0] - A[0]) * f, A[1] + (B[1] - A[1]) * f)
    a = _fade(progress, 0.3)
    _ball(ax, *A, 0.025, YELLOW, alpha=1); _ball(ax, *B, 0.025, YELLOW); _ball(ax, *P, 0.03, PINK, alpha=a)
    _t(ax, A[0], A[1] - 0.09, "A", YELLOW, fs=9); _t(ax, B[0], B[1] + 0.09, "B", YELLOW, fs=9)
    _t(ax, P[0] - 0.02, P[1] + 0.10, "P", PINK, fs=9, alpha=a)
    _t(ax, 0.26, 0.48, "m", GREEN, fs=10, alpha=a); _t(ax, 0.70, 0.66, "n", GREEN, fs=10, alpha=a)


def draw_histogram(ax, progress=1.0):
    _setup(ax); _axes(ax)
    h = [0.18, 0.34, 0.62, 0.46, 0.24]
    show = max(1, int(5 * min(1, progress * 1.3)))
    for k in range(show):
        col = PINK if k == 2 else CYAN
        ax.add_patch(Rectangle((0.16 + k * 0.15, 0.14), 0.15, h[k], facecolor=col, edgecolor=NAVY, alpha=0.85))
    a = _fade(progress, 0.6)
    _t(ax, 0.535, 0.84, "modal class", PINK, fs=7, alpha=a)
    _t(ax, 0.30, 0.06, "class intervals", GREY, fs=6)


def draw_ogive(ax, progress=1.0):
    _setup(ax); _axes(ax)
    xs = np.linspace(0.14, 0.90, 200)
    ys = 0.14 + 0.72 / (1 + np.exp(-(xs - 0.5) * 12))
    n = max(2, int(200 * min(1, progress * 1.3)))
    ax.plot(xs[:n], ys[:n], color=CYAN, lw=2.2)
    a = _fade(progress, 0.6)
    ax.plot([0.10, 0.5, 0.5], [0.50, 0.50, 0.14], color=YELLOW, lw=1.2, ls="--", alpha=a)
    _t(ax, 0.22, 0.56, "n/2", YELLOW, fs=8, alpha=a); _t(ax, 0.5, 0.07, "median", YELLOW, fs=7, alpha=a)


def draw_sector(ax, progress=1.0):
    _setup(ax)
    _ring(ax, 0.5, 0.5, 0.36, GREY, lw=1.4)
    th = 100 * min(1, progress * 1.3)
    ax.add_patch(Wedge((0.5, 0.5), 0.36, 0, th, facecolor=CYAN, edgecolor=WHITE, alpha=0.5, transform=ax.transData))
    _t(ax, 0.58, 0.56, "θ", YELLOW, fs=10)
    _t(ax, 0.72, 0.42, "r", WHITE, fs=9)
    _t(ax, 0.62, 0.92, "arc", ORANGE, fs=8, alpha=_fade(progress, 0.5))


def draw_ring(ax, progress=1.0):
    _setup(ax)
    a = _fade(progress, 0.0)
    ax.add_patch(Ellipse((0.5, 0.5), 0.8 * _K, 0.8, facecolor=CYAN, edgecolor=WHITE, alpha=0.5 * a))
    ax.add_patch(Ellipse((0.5, 0.5), 0.44 * _K, 0.44, facecolor="#0b1630", edgecolor=WHITE, alpha=1.0))
    ax.plot([0.5, 0.5 + 0.40 * _K], [0.5, 0.5], color=YELLOW, lw=1.4); _t(ax, 0.68, 0.55, "R", YELLOW, fs=9)
    ax.plot([0.5, 0.5], [0.5, 0.28], color=PINK, lw=1.4); _t(ax, 0.46, 0.38, "r", PINK, fs=9)


def _solid(ax, kind, progress):
    _setup(ax)
    a = _fade(progress, 0.0)
    if kind == "cylinder":
        ax.add_patch(Rectangle((0.30, 0.22), 0.40, 0.56, facecolor=CYAN, edgecolor="none", alpha=0.35))
        ax.add_patch(Ellipse((0.5, 0.78), 0.40, 0.12, facecolor="#2a8cff", edgecolor=WHITE, lw=1.6))
        ax.add_patch(Arc((0.5, 0.22), 0.40, 0.12, theta1=180, theta2=360, color=WHITE, lw=1.6))
        ax.plot([0.30, 0.30], [0.22, 0.78], color=WHITE, lw=1.6); ax.plot([0.70, 0.70], [0.22, 0.78], color=WHITE, lw=1.6)
        _t(ax, 0.78, 0.50, "h", YELLOW, fs=10); ax.plot([0.5, 0.70], [0.78, 0.78], color=PINK, lw=1.4); _t(ax, 0.60, 0.84, "r", PINK, fs=9)
    elif kind == "cone":
        ax.add_patch(Polygon([[0.30, 0.22], [0.70, 0.22], [0.5, 0.86]], closed=True, facecolor=CYAN, edgecolor="none", alpha=0.35))
        ax.plot([0.30, 0.5, 0.70], [0.22, 0.86, 0.22], color=WHITE, lw=1.6)
        ax.add_patch(Ellipse((0.5, 0.22), 0.40, 0.12, fill=False, edgecolor=WHITE, lw=1.6))
        ax.plot([0.5, 0.5], [0.22, 0.86], color=YELLOW, lw=1.2, ls="--", alpha=a); _t(ax, 0.46, 0.50, "h", YELLOW, fs=9)
        _t(ax, 0.66, 0.58, "l", GREEN, fs=10); ax.plot([0.5, 0.70], [0.22, 0.22], color=PINK, lw=1.4); _t(ax, 0.60, 0.15, "r", PINK, fs=9)
    elif kind == "sphere":
        ax.add_patch(Ellipse((0.5, 0.5), 0.62 * _K, 0.62, facecolor=CYAN, edgecolor=WHITE, lw=1.6, alpha=0.4))
        ax.add_patch(Ellipse((0.5, 0.5), 0.62 * _K, 0.16, fill=False, edgecolor=WHITE, lw=1, ls="--"))
        ax.plot([0.5, 0.5 + 0.31 * _K], [0.5, 0.5], color=PINK, lw=1.4); _t(ax, 0.62, 0.55, "r", PINK, fs=9)
    elif kind == "hemisphere":
        ax.add_patch(Wedge((0.5, 0.40), 0.32, 0, 180, facecolor=CYAN, edgecolor=WHITE, lw=1.6, alpha=0.4))
        ax.add_patch(Ellipse((0.5, 0.40), 0.64, 0.14, facecolor="#2a8cff", edgecolor=WHITE, lw=1.4, alpha=0.8))
        ax.plot([0.5, 0.82], [0.40, 0.40], color=PINK, lw=1.4); _t(ax, 0.66, 0.34, "r", PINK, fs=9)
        _t(ax, 0.5, 0.12, "curved 2πr² + base πr²", GREEN, fs=7, alpha=_fade(progress, 0.4))


def draw_factor_tree(ax, progress=1.0):
    _setup(ax)
    _t(ax, 0.5, 0.88, "12 = 2² × 3", CYAN, fs=8); _t(ax, 0.5, 0.74, "18 = 2 × 3²", ORANGE, fs=8)
    a = _fade(progress, 0.3)
    _box(ax, 0.27, 0.40, 0.40, 0.18, GREEN, alpha=a); _t(ax, 0.27, 0.40, "HCF = 6", GREEN, fs=8, alpha=a)
    _box(ax, 0.73, 0.40, 0.40, 0.18, YELLOW, alpha=a); _t(ax, 0.73, 0.40, "LCM = 36", YELLOW, fs=8, alpha=a)
    b = _fade(progress, 0.6)
    _t(ax, 0.5, 0.14, "6 × 36 = 216 = 12 × 18 ✓", WHITE, fs=8, alpha=b)


def draw_cubic_graph(ax, progress=1.0):
    _setup(ax)
    ax.plot([0.06, 0.94], [0.5, 0.5], color=GREY, lw=1.2); ax.plot([0.5, 0.5], [0.06, 0.94], color=GREY, lw=1.0)
    x = np.linspace(-2.2, 2.2, 300); y = (x + 1.6) * (x - 0.2) * (x - 1.8)
    n = max(2, int(300 * min(1, progress * 1.3)))
    ax.plot(0.5 + x[:n] * 0.19, 0.5 + np.clip(y[:n], -4, 4) * 0.10, color=CYAN, lw=2.2)
    a = _fade(progress, 0.6)
    for r, lab in ((-1.6, "α"), (0.2, "β"), (1.8, "γ")):
        _ball(ax, 0.5 + r * 0.19, 0.5, 0.022, YELLOW, alpha=a); _t(ax, 0.5 + r * 0.19, 0.42, lab, YELLOW, fs=9, alpha=a)


def draw_two_lines(kind, ax, progress=1.0):
    _setup(ax); _axes(ax, x0=0.08, y0=0.10)
    a = _fade(progress, 0.0)
    if kind == "intersect":
        ax.plot([0.12, 0.88], [0.20, 0.82], color=CYAN, lw=2.2); ax.plot([0.12, 0.88], [0.80, 0.24], color=ORANGE, lw=2.2, alpha=a)
        _ball(ax, 0.5, 0.511, 0.025, YELLOW, alpha=_fade(progress, 0.5)); _t(ax, 0.5, 0.64, "one solution", YELLOW, fs=7, alpha=_fade(progress, 0.5))
    else:
        ax.plot([0.12, 0.80], [0.20, 0.80], color=CYAN, lw=2.2); ax.plot([0.28, 0.92], [0.18, 0.74], color=ORANGE, lw=2.2, alpha=a)
        _t(ax, 0.70, 0.30, "parallel:\nno solution", PINK, fs=7, alpha=_fade(progress, 0.5))


# ═══ COMPUTER SCIENCE ════════════════════════════════════════════════════════
def draw_sql_result(query, cols, rows, ax, progress=1.0):
    _setup(ax)
    _box(ax, 0.5, 0.86, 0.94, 0.18, CYAN, fill="#0b1222")
    _t(ax, 0.5, 0.86, query, YELLOW, fs=6.5, family="DejaVu Sans Mono", fontweight="bold")
    a = _fade(progress, 0.25)
    w = 0.84 / len(cols)
    for j, cname in enumerate(cols):
        x = 0.08 + j * w
        ax.add_patch(Rectangle((x, 0.60), w, 0.10, facecolor=GREEN, edgecolor=NAVY, alpha=a))
        _t(ax, x + w / 2, 0.65, cname, NAVY, fs=6.5, fontweight="bold", alpha=a)
        for i, row in enumerate(rows):
            b = _fade(progress, 0.35 + i * 0.12)
            y = 0.50 - i * 0.10
            ax.add_patch(Rectangle((x, y), w, 0.10, facecolor="#13264d", edgecolor="#2b3f66", alpha=b))
            _t(ax, x + w / 2, y + 0.05, str(row[j]), WHITE, fs=6.5, alpha=b)


DIAGRAMS.update({
    "ac_sine": draw_ac_sine, "impedance_triangle": draw_impedance_triangle, "resonance_curve": draw_resonance_curve,
    "transformer": draw_transformer, "em_wave": draw_em_wave, "wave_lambda": draw_wave_lambda,
    "em_spectrum": draw_em_spectrum, "single_slit": draw_single_slit, "brewster": draw_brewster, "malus": draw_malus,
    "gauss_sphere": draw_gauss_sphere, "line_charge": draw_line_charge, "charged_sheet": draw_charged_sheet,
    "dipole": draw_dipole, "cap_series": draw_cap_series, "cap_parallel": draw_cap_parallel,
    "circular_motion_B": draw_circular_motion_B, "parallel_wires": draw_parallel_wires, "coil_torque": draw_coil_torque,
    "galvanometer": draw_galvanometer,
    "unpaired_electrons": draw_unpaired_electrons, "orbital_boxes": draw_orbital_boxes, "size_trend": draw_size_trend,
    "ph_scale": draw_ph_scale, "reactivity_ladder": draw_reactivity_ladder,
    "ethane": partial(draw_carbon_chain, "single"), "ethene": partial(draw_carbon_chain, "double"),
    "ethyne": partial(draw_carbon_chain, "triple"),
    "slope_field": draw_slope_field, "inverse_sine": draw_inverse_sine, "inc_dec": draw_inc_dec,
    "ap_steps": draw_ap_steps, "coord_distance": draw_coord_distance, "coord_section": draw_coord_section,
    "histogram": draw_histogram, "ogive": draw_ogive, "sector": draw_sector, "ring_area": draw_ring,
    "cylinder3d": partial(_solid, kind="cylinder"), "cone3d": partial(_solid, kind="cone"),
    "sphere3d": partial(_solid, kind="sphere"), "hemisphere3d": partial(_solid, kind="hemisphere"),
    "factor_tree": draw_factor_tree, "cubic_graph": draw_cubic_graph,
    "lines_intersect": partial(draw_two_lines, "intersect"), "lines_parallel": partial(draw_two_lines, "parallel"),
})

# functions with their own graph
_FN = {
    "fn_sin": (np.sin, np.cos, "y = sin x", 1.0, (-3.2, 3.2)),
    "fn_exp": (np.exp, np.exp, "y = eˣ", 0.6, (-2.0, 1.6)),
    "fn_ln": (np.log, lambda x: 1 / x, "y = ln x", 1.5, (0.15, 4.0)),
    "fn_tan": (np.tan, lambda x: 1 / np.cos(x) ** 2, "y = tan x", 0.5, (-1.2, 1.2)),
    "fn_asin": (np.arcsin, lambda x: 1 / np.sqrt(1 - x * x), "y = sin⁻¹x", 0.4, (-0.99, 0.99)),
    "fn_quot": (lambda x: x / (1 + x * x), lambda x: (1 - x * x) / (1 + x * x) ** 2, "y = u/v", -0.8, (-3, 3)),
}
for k, (f, df, lab, x0, xr) in _FN.items():
    DIAGRAMS[k] = partial(draw_fn_tangent, f, df, lab, x0, xr)
_AREA = {
    "area_xn": (lambda x: x ** 2, "∫xⁿ dx", 0.0, 1.6, (-0.2, 1.8)),
    "area_inv": (lambda x: 1 / x, "∫(1/x) dx", 1.0, 3.0, (0.3, 3.5)),
    "area_exp": (np.exp, "∫eˣ dx", -1.0, 1.0, (-1.8, 1.4)),
    "area_sin": (np.sin, "∫sin x dx", 0.0, math.pi, (-0.3, 3.5)),
    "area_atan": (lambda x: 1 / (1 + x * x), "∫1/(1+x²) dx", -1.5, 1.5, (-3, 3)),
    "area_asin": (lambda x: 1 / np.sqrt(1 - x * x), "∫1/√(1−x²) dx", -0.8, 0.8, (-0.95, 0.95)),
}
for k, (f, lab, a_, b_, xr) in _AREA.items():
    DIAGRAMS[k] = partial(draw_area_fn, f, lab, a_, b_, xr)

_RX = {
    "rx_cannizzaro": ("2 HCHO", "conc. NaOH", "CH₃OH + HCOONa"),
    "rx_aldol": ("2 CH₃CHO", "dil. NaOH", "CH₃CH(OH)CH₂CHO"),
    "rx_wurtz": ("2 R–X + 2 Na", "dry ether", "R–R + 2 NaX"),
    "rx_kolbe": ("phenol (C₆H₅OH)", "1. NaOH  2. CO₂, H⁺", "salicylic acid"),
    "rx_hoffmann": ("R–CONH₂", "Br₂ + 4 NaOH", "R–NH₂ (one C less)"),
    "rx_clemmensen": ("R–CO–R′", "Zn–Hg / conc. HCl", "R–CH₂–R′"),
    "rx_neutral": ("acid + base", "neutralisation", "salt + water"),
    "rx_naoh_hcl": ("NaOH + HCl", "", "NaCl + H₂O"),
    "rx_baking": ("2 NaHCO₃", "heat", "Na₂CO₃ + H₂O + CO₂"),
    "rx_pop": ("CaSO₄·2H₂O (gypsum)", "heat 373 K", "CaSO₄·½H₂O (Plaster of Paris)"),
    "rx_bleach": ("Ca(OH)₂ + Cl₂", "", "CaOCl₂ + H₂O"),
    "rx_combust": ("CH₄ + 2 O₂", "burn", "CO₂ + 2 H₂O + heat"),
    "rx_ester": ("CH₃COOH + C₂H₅OH", "conc. H₂SO₄", "CH₃COOC₂H₅ + H₂O"),
    "rx_sapon": ("ester + NaOH", "heat", "soap (sodium salt) + alcohol"),
    "rx_metal_acid": ("Zn + 2 HCl", "", "ZnCl₂ + H₂↑"),
    "rx_thermite": ("Fe₂O₃ + 2 Al", "ignite", "2 Fe + Al₂O₃ + heat"),
    "rx_roast": ("2 ZnS + 3 O₂", "roasting", "2 ZnO + 2 SO₂"),
    "rx_calcine": ("ZnCO₃", "calcination", "ZnO + CO₂"),
    "rx_rust": ("4 Fe + 3 O₂ + x H₂O", "moist air", "2 Fe₂O₃·xH₂O (rust)"),
    "rx_kmno4": ("MnO₄⁻ + 8H⁺ + 5e⁻", "acidic medium", "Mn²⁺ + 4 H₂O"),
    "rx_dichromate": ("Cr₂O₇²⁻ + 14H⁺ + 6e⁻", "acidic medium", "2 Cr³⁺ + 7 H₂O"),
}
for k, v in _RX.items():
    DIAGRAMS[k] = partial(draw_rx, *v)

_SQL = {
    "sql_count": ("SELECT COUNT(*) FROM Student;", ["COUNT(*)"], [[40]]),
    "sql_avg": ("SELECT AVG(Marks), SUM(Marks) ...", ["AVG", "SUM"], [[78.5, 3140]]),
    "sql_maxmin": ("SELECT MAX(Marks), MIN(Marks) ...", ["MAX", "MIN"], [[99, 41]]),
    "sql_group": ("... GROUP BY Class HAVING COUNT(*) > 10;", ["Class", "COUNT"], [["XII-A", 14], ["XII-B", 12]]),
    "sql_order": ("... ORDER BY Marks DESC;", ["Name", "Marks"], [["Riya", 99], ["Aman", 92], ["Kabir", 88]]),
    "sql_like": ("... WHERE Name LIKE 'A%';", ["Name"], [["Aman"], ["Anika"], ["Arjun"]]),
}
for k, v in _SQL.items():
    DIAGRAMS[k] = partial(draw_sql_result, *v)
