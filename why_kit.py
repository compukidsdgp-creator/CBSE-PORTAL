#!/usr/bin/env python3
"""
why_kit.py — the shared engine for "WHY?" reels (locked design, Nov 2026).

Every WHY? reel is a small module in why_reels/ with:
    TITLE    question shown in the gold box (mathtext allowed)
    BEATS    [(name, spoken, caption, min_seconds), ...]  — the last beat should be "end"
    CAPTION  social media caption (Instagram / Facebook)
    TAGS     short subject label, e.g. "Class 10 Maths"
    draw(c)  draws one frame; `c` gives time helpers and a camera-controlled drawing area

The kit does the rest: narration (voiceover.py), beat timing from the voice, background,
header, question box, word-by-word captions, the follow pill on the "end" beat, footer,
parallel frame rendering and the final MP4 with music under the voice.

    python3 why_kit.py --reel circle_area --preview /tmp/frames   # 2 stills per beat
    python3 why_kit.py --reel circle_area --out reel.mp4
    python3 why_kit.py --reel circle_area --queue 1               # -> formula-posts/why/queue/01_why_circle_area.mp4 (+ .txt)
"""
import argparse
import importlib
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
from matplotlib.patches import FancyBboxPatch

import generate_formula_reel_v3 as R
import generate_voice_reel as V
from voiceover import synth, write_wav, SR

ROOT = Path(__file__).parent
W, H, DPI, FPS = R.W, R.H, R.DPI, R.FPS
LEAD, TAIL = 0.35, 0.50
NAVY = "#070f24"
CYAN, GOLD, PINK, GREEN, PURPLE, ORANGE = "#2ad4ff", "#ffd23f", "#ff5fa2", "#3ddc97", "#a98bff", "#ff9f43"
WHITE, LTGREY, GREY = R.WHITE, R.LTGREY, R.GREY
DRAW_BOX = [0.0, 0.405, 1.0, 0.425]             # default drawing area (figure fractions)
QUEUE = ROOT / "formula-posts" / "why" / "queue"

G = {}


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def lerp(a, b, x):
    return a + (b - a) * x


def back_out(x):
    return R.back_out(x)


def outline(artist, w=6):
    """Dark outline so labels stay readable over drawings."""
    artist.set_path_effects([pe.withStroke(linewidth=w, foreground=NAVY), pe.Normal()])
    return artist


class Ctx:
    """What a reel's draw() gets for one frame."""

    def __init__(self, t, beats, fig, ax):
        self.t, self.beats, self.fig, self.ax = t, beats, fig, ax
        self.cur = next((b for b in beats if t < b["end"]), beats[-1])

    def beat(self, name):
        return next(b for b in self.beats if b["name"] == name)

    def phase(self, name, a=0.0, z=1.0):
        """Progress 0..1 through the window [a, z] of beat `name` (before → 0, after → 1)."""
        b = self.beat(name)
        d = b["end"] - b["start"]
        return max(0.0, min(1.0, (self.t - b["start"] - a * d) / max(1e-6, (z - a) * d)))

    def at(self, name):
        """True from the start of beat `name` onwards."""
        return self.t >= self.beat(name)["start"]

    def area(self, cx=0.0, cy=0.0, width=3.0, box=None):
        """A drawing area with equal x/y scale; (cx, cy, width) is the camera."""
        box = box or DRAW_BOX
        aspect = box[3] * H / (box[2] * W)
        dax = self.fig.add_axes(box)
        dax.axis("off"); dax.patch.set_visible(False)
        dax.set_xlim(cx - width / 2, cx + width / 2)
        dax.set_ylim(cy - width * aspect / 2, cy + width * aspect / 2)
        dax.set_aspect("equal", adjustable="box")
        return dax

    # text on the full-frame axes (fractions of the frame)
    def text(self, x, y, s, size=30, color=WHITE, alpha=1.0, max_w=None, weight="bold", ha="center"):
        R.flat_text(self.ax, x, y, s, size=size, color=color, alpha=max(0, min(1, alpha)),
                    max_w=max_w, weight=weight, ha=ha)

    def pill(self, x, y, w, h, color, alpha=1.0, fill_alpha=0.9, dark="#141000", lw=2.2):
        R.pill(self.ax, x, y, w, h, fill=R.rgba(dark, fill_alpha), edge=R.rgba(color, 1.0),
               lw=lw, alpha=max(0, min(1, alpha)), zorder=8)

    def steps(self, items, ys=(0.352, 0.300, 0.248), beat="math"):
        """Working shown line by line under the drawing: items = [(text, start_frac, color)].
        The last GOLD item is boxed as the answer."""
        for (s, at, col), y in zip(items, ys):
            a = ease(self.phase(beat, at, at + 0.15))
            if a <= 0:
                continue
            if col == GOLD:
                size = R.fit_size(s, 50, 0.80)
                w = max(0.40, V.text_w(s, size) + 0.10)
                self.pill(0.5, y, min(0.90, w * back_out(a)), 0.056, GOLD, alpha=a, dark="#2a2000")
                self.text(0.5, y - 0.008 * (1 - a), s, size=size, color=GOLD, alpha=a)
            else:
                self.text(0.5, y - 0.008 * (1 - a), s, size=40, color=col, alpha=a, max_w=0.9)


def _init(g):
    G.update(g)
    G["mod"] = importlib.import_module(f"why_reels.{g['reel']}")


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
    mod, beats = G["mod"], G["beats"]
    t = fi / FPS
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(NAVY)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    st = G["stars"]
    ax.scatter(st[:, 0], st[:, 1], s=st[:, 2], color="white", alpha=0.22,
               transform=ax.transAxes, zorder=0, linewidths=0)
    c = Ctx(t, beats, fig, ax)

    # question box
    qp = back_out(c.phase(beats[0]["name"], 0.0, 0.18))
    R.pill(ax, 0.5, 0.868, 0.84 * min(1, qp), 0.058, fill=R.rgba("#1a1400", 0.85),
           edge=R.rgba(GOLD, 1.0), lw=2.2, alpha=min(1, qp), zorder=7)
    if qp > 0.4:
        R.flat_text(ax, 0.5, 0.868, mod.TITLE, size=R.fit_size(mod.TITLE, 36, 0.78),
                    color=GOLD, alpha=min(1, qp))

    mod.draw(c)

    # follow pill on the last beat
    if any(b["name"] == "end" for b in beats) and c.at("end"):
        ep = back_out(c.phase("end", 0.15, 0.45))
        y = getattr(mod, "END_Y", 0.418)
        R.pill(ax, 0.5, y, 0.70 * min(1, ep), 0.046, fill=R.rgba("#00b4d8", 1),
               edge=R.rgba(CYAN, 1), lw=2, alpha=min(1, ep), zorder=9)
        R.flat_text(ax, 0.5, y, "Follow for more WHY? videos", size=25, color="white", alpha=min(1, ep))

    # caption, words lighting up as they are spoken
    cur = c.cur
    sp = cur["speech"]
    frac = min(1.0, max(0.0, (t - cur["start"] - LEAD) / sp)) if sp else 1.0
    R.pill(ax, 0.5, 0.140, 0.92, 0.120, fill=R.rgba("#000814", 0.6), edge=R.rgba(GOLD, 0.45),
           lw=1.3, zorder=8)
    V.karaoke(ax, cur["cap"], frac, 0.168, GOLD, size=26, width=38, line_h=0.038)

    draw_header(ax)
    R.draw_footer(ax, t, GOLD)
    fig.savefig(str(Path(G["frame_dir"]) / f"frame_{fi:05d}.png"), dpi=DPI, facecolor=NAVY)
    plt.close(fig)


def build(reel, out=None, preview=None, workers=None):
    mod = importlib.import_module(f"why_reels.{reel}")
    beats, clips, t = [], [], 0.0
    for name, say, cap, min_d in mod.BEATS:
        a = synth(say)
        sp = len(a) / SR
        d = max(min_d, LEAD + sp + TAIL)
        beats.append({"name": name, "start": t, "end": t + d, "speech": sp, "cap": cap})
        clips.append((t + LEAD, a)); t += d
    total = t
    rng = np.random.default_rng(7)
    stars = np.c_[rng.random(160), rng.random(160) * 0.85 + 0.07, rng.random(160) * 6 + 1]
    g = {"reel": reel, "beats": beats, "stars": stars}
    if preview:
        Path(preview).mkdir(parents=True, exist_ok=True)
        g["frame_dir"] = str(preview); _init(g)
        for b in beats:
            for f in (0.35, 0.97):
                render_frame(int((b["start"] + f * (b["end"] - b["start"])) * FPS))
        print(f"[preview] {reel}: {total:.1f}s, stills in {preview}")
        return total
    tmp = Path(tempfile.mkdtemp(prefix="why_"))
    frame_dir = tmp / "f"; frame_dir.mkdir()
    g["frame_dir"] = str(frame_dir)
    voice = np.zeros(int(total * SR) + SR, dtype=np.float32)
    for st, a in clips:
        i0 = int(st * SR); voice[i0:i0 + len(a)] += a
    voice = voice[:int(total * SR)]
    voice *= 0.95 / max(1e-6, np.abs(voice).max())
    write_wav(tmp / "voice.wav", voice)
    nframes = int(round(total * FPS))
    print(f"[INFO] {reel}: {nframes} frames ({total:.1f}s)")
    with Pool(workers or os.cpu_count() or 1, initializer=_init, initargs=(g,)) as pool:
        pool.map(render_frame, range(nframes), chunksize=10)
    V.mux(frame_dir, tmp / "voice.wav", total, out)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[OK] {out} ({Path(out).stat().st_size / 1048576:.1f} MB, {total:.1f}s)")
    return total


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--reel", required=True)
    ap.add_argument("--out")
    ap.add_argument("--preview")
    ap.add_argument("--queue", type=int, help="write into the WHY? posting queue with this order number")
    a = ap.parse_args()
    if a.queue:
        QUEUE.mkdir(parents=True, exist_ok=True)
        out = QUEUE / f"{a.queue:02d}_why_{a.reel}.mp4"
        build(a.reel, out=out)
        mod = importlib.import_module(f"why_reels.{a.reel}")
        out.with_suffix(".txt").write_text(mod.CAPTION.strip() + "\n", encoding="utf-8")
    else:
        build(a.reel, out=a.out or f"why_{a.reel}.mp4", preview=a.preview)
