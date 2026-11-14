#!/usr/bin/env python3
"""
generate_why_reel.py — "WHY?" series (style B, sample): one concept told as one
continuous, narrated animation.

Sample: Why is the area of a circle πr² ?
  circle → slice into rings → cut and unroll every ring → the strips stack into a
  triangle (base 2πr, height r) → ½ × 2πr × r = πr²

    python3 generate_why_reel.py --out why_circle.mp4
"""
import argparse
import math
import os
import shutil
import tempfile
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, Polygon, Circle

import generate_formula_reel_v3 as R
import generate_voice_reel as V
from voiceover import synth, write_wav, SR

W, H, DPI, FPS = R.W, R.H, R.DPI, R.FPS
LEAD, TAIL = 0.35, 0.50
NAVY = "#070f24"
CYAN, GOLD, PINK, GREEN = "#2ad4ff", "#ffd23f", "#ff5fa2", "#3ddc97"
N_RINGS = 16
DRAW_BOX = [0.0, 0.405, 1.0, 0.425]            # where the animation lives (figure fractions)
ASPECT = DRAW_BOX[3] * H / (DRAW_BOX[2] * W)   # data height per data width

BEATS = [
    ("hook",   "Why is the area of a circle, pi r squared? Let's see it, instead of memorising it.",
               "Why is the area of a circle πr²? Let's see it, instead of memorising it.", 4.0),
    ("radius", "Take a circle of radius r.",
               "Take a circle of radius r.", 2.6),
    ("rings",  "Slice it into thin rings, like the layers of an onion.",
               "Slice it into thin rings, like the layers of an onion.", 3.6),
    ("outer",  "The outermost ring is as long as the circumference. Two pi r.",
               "The outermost ring is as long as the circumference: 2πr.", 3.6),
    ("unroll", "Now cut every ring at the bottom, and straighten it out.",
               "Now cut every ring at the bottom… and straighten it out.", 5.2),
    ("tri",    "The strips stack up into a triangle. Its base is two pi r, and its height is r.",
               "The strips stack up into a triangle. Base 2πr, height r.", 4.2),
    ("math",   "Area of a triangle is half, base times height. Half of two pi r, times r, "
               "is pi r squared.",
               "Area = ½ × base × height = ½ × 2πr × r = πr²", 5.5),
    ("end",    "That's why. Follow C B S E Mock for more why videos.",
               "That's why! Follow @cbsemock for more WHY? videos.", 3.4),
]

G = {}


def _init(g):
    G.update(g)


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def lerp(a, b, x):
    return a + (b - a) * x


def ring_color(j):
    """Inner rings cyan → outer rings gold, alternate shades so each ring is visible."""
    f = j / (N_RINGS - 1)
    c0, c1 = np.array(matplotlib.colors.to_rgb(CYAN)), np.array(matplotlib.colors.to_rgb(GOLD))
    c = c0 * (1 - f) + c1 * f
    return tuple(c * (1.0 if j % 2 else 0.78))


def ring_polygon(r, curl, dr):
    """Band of radius r and thickness dr; curl 1 = closed ring, 0 = straight strip.
    The ring is cut at its bottom point, which stays fixed at (0, -r)."""
    L = 2 * math.pi * r
    s = np.linspace(-L / 2, L / 2, 140)
    if curl < 1e-4:
        x, y = s, np.zeros_like(s)
        nx, ny = np.zeros_like(s), np.ones_like(s)
    else:
        k = curl / r
        x, y = np.sin(k * s) / k, (1 - np.cos(k * s)) / k
        nx, ny = -np.sin(k * s), np.cos(k * s)
    h = dr * 0.46
    outer = np.c_[x - nx * h, -r + y - ny * h]
    inner = np.c_[x + nx * h, -r + y + ny * h]
    return np.vstack([outer, inner[::-1]])


def timeline_pos(t):
    for b in G["beats"]:
        if t < b["end"]:
            return b, (t - b["start"]) / (b["end"] - b["start"])
    b = G["beats"][-1]
    return b, 1.0


def beat(name):
    return next(b for b in G["beats"] if b["name"] == name)


def phase(t, name, a=0.0, z=1.0):
    """Progress 0..1 of the window [a, z] inside beat `name` (clamped; before → 0, after → 1)."""
    b = beat(name)
    d = b["end"] - b["start"]
    return max(0.0, min(1.0, (t - b["start"] - a * d) / max(1e-6, (z - a) * d)))


def draw_header(ax):
    ax.add_patch(FancyBboxPatch((0, 0.918), 1, 0.082, boxstyle="square,pad=0",
                                facecolor=R.BAR_BG, edgecolor="none", zorder=5, transform=ax.transAxes))
    ax.plot([0, 1], [0.918, 0.918], color=GOLD, lw=2, alpha=0.75, transform=ax.transAxes, zorder=6)
    img = R.logo_img()
    if img is not None:
        lax = ax.figure.add_axes([0.012, 0.9225, 0.50, 0.0735]); lax.imshow(img); lax.axis("off")
    R.flat_text(ax, 0.97, 0.969, "WHY? series", size=16, color=GOLD, ha="right")
    R.flat_text(ax, 0.97, 0.948, "cbsemock.org.in", size=13, color=R.LTGREY, weight="normal", ha="right")


def render_frame(fi):
    t = fi / FPS
    cur, prog = timeline_pos(t)
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(NAVY)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.scatter(G["stars"][:, 0], G["stars"][:, 1], s=G["stars"][:, 2], color="white",
               alpha=0.22, transform=ax.transAxes, zorder=0, linewidths=0)

    # ── question box ──
    qp = R.back_out(phase(t, "hook", 0.0, 0.18))
    q = r"Why is circle area $= \pi r^{2}$ ?"
    R.pill(ax, 0.5, 0.868, 0.80 * min(1, qp), 0.058, fill=R.rgba("#1a1400", 0.85),
           edge=R.rgba(GOLD, 1.0), lw=2.2, alpha=min(1, qp), zorder=7)
    if qp > 0.4:
        R.flat_text(ax, 0.5, 0.868, q, size=R.fit_size(q, 36, 0.74), color=GOLD, alpha=min(1, qp))

    # ── camera ──
    zo = ease(phase(t, "unroll", 0.10, 0.85))
    push = math.sin(math.pi * phase(t, "outer")) * 0.18            # small push-in on the outer ring
    width = lerp(3.05, 6.75, zo) - push
    cx, cy = 0.0, lerp(0.0, -0.05, zo)
    dax = fig.add_axes(DRAW_BOX); dax.axis("off"); dax.patch.set_visible(False)
    dax.set_xlim(cx - width / 2, cx + width / 2)
    dax.set_ylim(cy - width * ASPECT / 2, cy + width * ASPECT / 2)
    dax.set_aspect("equal", adjustable="box")

    dr = 1.0 / N_RINGS
    rings_on = phase(t, "rings", 0.05, 0.85)
    outer_hl = phase(t, "outer", 0.0, 0.25) * (1 - phase(t, "unroll", 0.0, 0.15))

    if rings_on <= 0:
        # one solid disc, outline drawn on during the hook
        draw = ease(phase(t, "hook", 0.15, 0.75))
        th = np.linspace(-math.pi / 2, -math.pi / 2 + 2 * math.pi * draw, 200)
        dax.plot(np.cos(th), np.sin(th), color=CYAN, lw=4, solid_capstyle="round", zorder=5)
        fill = phase(t, "hook", 0.65, 1.0)
        dax.add_patch(Circle((0, 0), 1, facecolor=CYAN, edgecolor="none", alpha=0.25 * fill, zorder=2))
    else:
        for j in range(N_RINGS):
            r = (j + 0.5) * dr
            appear = ease(rings_on * N_RINGS - (N_RINGS - 1 - j))            # outer rings first
            if appear <= 0:
                continue
            st = (N_RINGS - 1 - j) / N_RINGS * 0.55                            # outer rings unroll first
            curl = 1 - ease((phase(t, "unroll", 0.05, 0.95) - st) / 0.45)
            a = appear * (1 - 0.72 * outer_hl * (j != N_RINGS - 1))
            dax.add_patch(Polygon(ring_polygon(r, curl, dr), closed=True, facecolor=ring_color(j),
                                  edgecolor=NAVY, lw=0.6, alpha=a, zorder=3 + j / 100))
        if rings_on < 1:   # the un-sliced disc fades as the rings take over
            dax.add_patch(Circle((0, 0), 1, facecolor=CYAN, edgecolor=CYAN, lw=3,
                                 alpha=0.25 * (1 - rings_on), zorder=2))

    # radius line + label
    rp = phase(t, "radius", 0.1, 0.6) * (1 - phase(t, "unroll", 0.0, 0.12))
    if rp > 0:
        L = ease(rp)
        dax.plot([0, L], [0, 0], color="white", lw=4, zorder=20, solid_capstyle="round")
        dax.plot([0], [0], "o", color="white", ms=10, zorder=21)
        if rp > 0.6:
            dax.text(0.5, 0.09, "r", color="white", fontsize=46, fontweight="bold", ha="center",
                     style="italic", zorder=22, alpha=min(1, (rp - 0.6) / 0.3))
    # outer ring label
    if outer_hl > 0.05:
        txt = dax.text(0.0, -1.32, r"length $= 2\pi r$", color=GOLD, fontsize=40, ha="center",
                       fontweight="bold", zorder=22, alpha=outer_hl)
        txt.set_path_effects([pe.withStroke(linewidth=6, foreground=NAVY), pe.Normal()])

    # triangle outline, base and height
    tp = ease(phase(t, "tri", 0.0, 0.45))
    if tp > 0:
        bx, by, ay = math.pi, -1.0, 0.0
        tri = np.array([[-bx, by - dr / 2], [bx, by - dr / 2], [0, ay], [-bx, by - dr / 2]])
        n = max(2, int(len(tri) * 40 * tp))
        pts = np.vstack([np.linspace(tri[k], tri[k + 1], 40) for k in range(3)])[:n]
        dax.plot(pts[:, 0], pts[:, 1], color="white", lw=3.5, zorder=30)
        lp = phase(t, "tri", 0.30, 0.70)
        if lp > 0:
            dax.annotate("", xy=(bx, by - 0.22), xytext=(-bx, by - 0.22),
                         arrowprops=dict(arrowstyle="<->", color=GOLD, lw=3), zorder=31)
            b = dax.text(0, by - 0.62, r"base $= 2\pi r$", color=GOLD, fontsize=38, ha="center",
                         fontweight="bold", zorder=32, alpha=lp)
            b.set_path_effects([pe.withStroke(linewidth=6, foreground=NAVY), pe.Normal()])
        hp = phase(t, "tri", 0.55, 0.95)
        if hp > 0:
            dax.plot([0, 0], [by - dr / 2, ay], color=PINK, lw=3, ls=(0, (4, 3)), zorder=31, alpha=hp)
            h = dax.annotate(r"height $= r$", xy=(0.04, -0.45), xytext=(1.45, -0.05), color=PINK,
                             fontsize=36, ha="left", va="center", fontweight="bold", zorder=32, alpha=hp,
                             arrowprops=dict(arrowstyle="-", color=PINK, lw=2, alpha=hp))
            h.set_path_effects([pe.withStroke(linewidth=6, foreground=NAVY), pe.Normal()])

    # the original circle, small, above the triangle: same area, new shape
    gp = ease(phase(t, "tri", 0.15, 0.6))
    if gp > 0:
        for j in range(N_RINGS):
            rr = (j + 0.5) * dr * 0.75
            dax.add_patch(Polygon(ring_polygon(rr, 1.0, dr * 0.75) + [0, 1.35], closed=True,
                                  facecolor=ring_color(j), edgecolor=NAVY, lw=0.4, alpha=gp, zorder=3))
        sa = dax.text(1.05, 1.35, "same area,\nnew shape", color=R.LTGREY, fontsize=30, ha="left",
                      va="center", fontweight="bold", zorder=32, alpha=gp)
        dax.annotate("", xy=(0, 0.25), xytext=(0, 0.52), zorder=31,
                     arrowprops=dict(arrowstyle="-|>", color=R.LTGREY, lw=2.5, alpha=gp, mutation_scale=28))

    # ── working, below the drawing ──
    steps = [(r"Area $= \frac{1}{2}\times$ base $\times$ height", 0.05, R.WHITE),
             (r"$= \frac{1}{2}\times 2\pi r \times r$", 0.40, CYAN),
             (r"$= \pi r^{2}$", 0.68, GOLD)]
    ys = [0.352, 0.300, 0.248]
    for (s, at, col), y in zip(steps, ys):
        a = ease(phase(t, "math", at, at + 0.15))
        if a > 0:
            size = 44 if col != GOLD else 58
            if col == GOLD:
                R.pill(ax, 0.5, y, 0.40 * R.back_out(a), 0.056, fill=R.rgba("#2a2000", 0.9),
                       edge=R.rgba(GOLD, 1), lw=2.5, alpha=a, zorder=8)
            R.flat_text(ax, 0.5, y - 0.008 * (1 - a), s, size=size, color=col, alpha=a)

    # ending pill
    ep = R.back_out(phase(t, "end", 0.15, 0.45)) if t >= beat("end")["start"] else 0
    if ep > 0:
        R.pill(ax, 0.5, 0.418, 0.70 * min(1, ep), 0.046, fill=R.rgba("#00b4d8", 1),
               edge=R.rgba(CYAN, 1), lw=2, alpha=min(1, ep), zorder=9)
        R.flat_text(ax, 0.5, 0.418, "Follow for more WHY? videos", size=25, color="white",
                    alpha=min(1, ep))

    # caption with words lighting up as they are spoken
    sp = cur["speech"]
    frac = min(1.0, max(0.0, (t - cur["start"] - LEAD) / sp)) if sp else 1.0
    R.pill(ax, 0.5, 0.140, 0.92, 0.120, fill=R.rgba("#000814", 0.6), edge=R.rgba(GOLD, 0.45),
           lw=1.3, zorder=8)
    V.karaoke(ax, cur["cap"], frac, 0.168, GOLD, size=26, width=38, line_h=0.038)

    draw_header(ax)
    R.draw_footer(ax, t, GOLD)
    fig.savefig(str(Path(G["frame_dir"]) / f"frame_{fi:05d}.png"), dpi=DPI, facecolor=NAVY)
    plt.close(fig)


def build(out, workers=None, only_frames=None):
    beats, clips, t = [], [], 0.0
    for name, say, cap, min_d in BEATS:
        a = synth(say)
        sp = len(a) / SR
        d = max(min_d, LEAD + sp + TAIL)
        beats.append({"name": name, "start": t, "end": t + d, "speech": sp, "cap": cap})
        clips.append((t + LEAD, a)); t += d
        print(f"  {name:7s} {d:5.2f}s  speech {sp:4.2f}s")
    total = t
    rng = np.random.default_rng(7)
    stars = np.c_[rng.random(160), rng.random(160) * 0.85 + 0.07, rng.random(160) * 6 + 1]
    tmp = Path(tempfile.mkdtemp(prefix="why_"))
    frame_dir = tmp / "f"; frame_dir.mkdir()
    g = {"beats": beats, "stars": stars, "frame_dir": str(frame_dir)}
    if only_frames is not None:                      # quick layout check
        _init(g); g["frame_dir"] = only_frames; _init(g)
        for b in beats:
            for f in (0.3, 0.95):
                render_frame(int((b["start"] + f * (b["end"] - b["start"])) * FPS))
        return
    voice = np.zeros(int(total * SR) + SR, dtype=np.float32)
    for st, a in clips:
        i0 = int(st * SR); voice[i0:i0 + len(a)] += a
    voice = voice[:int(total * SR)]
    voice *= 0.95 / max(1e-6, np.abs(voice).max())
    write_wav(tmp / "voice.wav", voice)
    nframes = int(round(total * FPS))
    print(f"[INFO] {nframes} frames ({total:.1f}s)")
    with Pool(workers or os.cpu_count() or 1, initializer=_init, initargs=(g,)) as pool:
        pool.map(render_frame, range(nframes), chunksize=10)
    V.mux(frame_dir, tmp / "voice.wav", total, out)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[OK] {out} ({Path(out).stat().st_size / 1048576:.1f} MB, {total:.1f}s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="why_circle_area.mp4")
    ap.add_argument("--preview-dir", default=None, help="only render 2 still frames per beat here")
    a = ap.parse_args()
    build(a.out, only_frames=a.preview_dir)
