#!/usr/bin/env python3
"""
generate_voice_reel.py — Formula Flash reels WITH NARRATION (style A, sample).

Same look as generate_formula_reel_v3.py, plus:
  * a spoken sentence for every formula (offline voice, voiceover.py)
  * each card lasts exactly as long as its sentence (no fixed 5 s)
  * the sentence is shown as a caption, words lighting up as they are spoken
  * the formula writes itself in left-to-right while the diagram draws in
  * a recap screen with all formulas before the save / follow screen
  * music kept low underneath the voice

    python3 generate_voice_reel.py --sample electricity --out reel.mp4
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
import generate_formula_reel_v3 as R                      # noqa: E402
from voiceover import synth, write_wav, SR                # noqa: E402

W, H, DPI, FPS = R.W, R.H, R.DPI, R.FPS
LEAD, TAIL = 0.35, 0.55          # silence before / after each sentence (s)

# ── Script for the sample reel ───────────────────────────────────────────────
# "say" is what the voice speaks (spelled for the voice), "cap" is what is shown.
SAMPLES = {
    "electricity": {
        "topic": "electricity_class10",
        "intro": "Four Electricity formulas you must know for your class ten boards.",
        "cards": [
            {"say": "Ohm's law. V equals I R. The current through a conductor is proportional "
                    "to the voltage across it.",
             "cap": "Ohm's law: V = IR. Current is proportional to the voltage across the conductor."},
            {"say": "Resistance. R equals rho, L by A. A longer wire resists more, "
                    "a thicker wire resists less.",
             "cap": "R = ρL/A. A longer wire resists more, a thicker wire resists less."},
            {"say": "In series, resistances simply add up, and the same current flows through each one.",
             "cap": "In series, resistances simply add up. The same current flows through each one."},
            {"say": "In parallel, add the reciprocals. Every resistor gets the same voltage, "
                    "so the total resistance drops.",
             "cap": "In parallel, add the reciprocals. Same voltage across each, total resistance drops."},
        ],
        "recap": "That's Electricity in four formulas. Save this reel for your revision.",
        "outro": "Share it with your batchmates, and follow C B S E Mock for more.",
    },
}

G = {}   # filled in each worker: rows, segments, data


def _init(g):
    G.update(g)


# ── Text helpers ─────────────────────────────────────────────────────────────
def text_w(s, size, weight="bold"):
    """Width of `s` in axes fractions."""
    if R._MFIG is None:
        R._MFIG = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    t = R._MFIG.text(0.5, 0.5, s, fontsize=size, fontweight=weight)
    bb = t.get_window_extent(R._MFIG.canvas.get_renderer())
    t.remove()
    return bb.width / W


def karaoke(ax, text, frac, y0, acc, size=27, width=35, line_h=0.040):
    """Caption whose words turn white as they are spoken (frac = 0..1 of speech)."""
    lines = textwrap.wrap(text, width)[:3]
    total = sum(len(l) for l in lines) or 1
    done = frac * total
    for k, line in enumerate(lines):
        y = y0 - k * line_h
        lw = text_w(line, size)
        x0 = 0.5 - lw / 2
        ax.text(x0, y, line, ha="left", va="center", fontsize=size, fontweight="bold",
                color=R.GREY, alpha=0.55, zorder=10, transform=ax.transAxes)
        n = int(max(0, min(len(line), done)))
        if n:
            cut = line[:n]
            if n < len(line) and line[n] != " ":        # light up whole words only
                cut = cut[:cut.rfind(" ")] if " " in cut else ""
            if cut:
                ax.text(x0, y, cut, ha="left", va="center", fontsize=size, fontweight="bold",
                        color=R.WHITE, zorder=11, transform=ax.transAxes)
        done -= len(line)


def wipe_formula(ax, s, y, size, frac, alpha=1.0):
    """Hero formula revealed left-to-right like a pen writing it."""
    if frac <= 0:
        return
    fw = text_w(s, size) * 1.06
    clip = Rectangle((0.5 - fw / 2 - 0.02, 0), (fw + 0.04) * min(1.0, frac), 1,
                     transform=ax.transAxes)
    o = ax.text(0.5, y, s, ha="center", va="center", fontsize=size, fontweight="bold",
                color=R.BG, alpha=alpha, zorder=11, transform=ax.transAxes)
    o.set_path_effects([pe.withStroke(linewidth=7, foreground=R.rgba("#000814", 0.8)), pe.Normal()])
    w = ax.text(0.5, y, s, ha="center", va="center", fontsize=size, fontweight="bold",
                color=R.WHITE, alpha=alpha, zorder=12, transform=ax.transAxes)
    w.set_path_effects([pe.withStroke(linewidth=2.0, foreground=R.WHITE), pe.Normal()])
    o.set_clip_path(clip); w.set_clip_path(clip)
    if frac < 1:                                        # the "pen" glow at the writing edge
        x = 0.5 - fw / 2 - 0.02 + (fw + 0.04) * frac
        ax.plot([x, x], [y - 0.045, y + 0.045], color=R.GOLD, lw=4, alpha=0.8,
                solid_capstyle="round", transform=ax.transAxes, zorder=13)


# ── Screens ──────────────────────────────────────────────────────────────────
def draw_vcard(ax, row, cap, num, total, prog, speech_frac, t, acc):
    p = R.eo(prog * 3)
    ax.add_patch(FancyBboxPatch((0.015, 0.075), 0.970, 0.835, boxstyle="square,pad=0",
                                facecolor=R.CARD_BG, edgecolor="none", alpha=min(.97, p),
                                zorder=2, transform=ax.transAxes))
    ax.add_patch(FancyBboxPatch((0.015, 0.075), 0.009, 0.835, boxstyle="square,pad=0",
                                facecolor=acc, edgecolor="none", alpha=p, zorder=3,
                                transform=ax.transAxes))
    R.flat_text(ax, 0.09, 0.878, f"Formula {num} of {total}", size=15, color=acc,
                weight="normal", ha="left", alpha=p * 0.85)
    R.flat_text(ax, 0.09, 0.850, row["label"].upper(), size=26, color=R.WHITE,
                ha="left", alpha=p, max_w=0.84)
    ax.plot([0.06, 0.94], [0.830, 0.830], color=acc, lw=0.8, alpha=p * 0.3,
            transform=ax.transAxes, zorder=5)
    R.draw_diagram(ax.figure, row.get("diagram"), (prog - 0.06) / 0.60)
    ax.plot([0.06, 0.94], [0.420, 0.420], color=acc, lw=0.8, alpha=p * 0.25,
            transform=ax.transAxes, zorder=5)
    fsize = R.fit_size(row["formula"], 72, 0.86, 0.140)
    wipe_formula(ax, row["formula"], 0.335, fsize, R.eo((prog - 0.04) / 0.30),
                 alpha=0.93 + 0.07 * R.pulse(t, 1.4))
    # caption panel
    cp = R.eo((prog - 0.02) / 0.10)
    R.pill(ax, 0.5, 0.170, 0.92, 0.150, fill=R.rgba("#000814", 0.55),
           edge=R.rgba(acc, 0.55), lw=1.4, alpha=cp, zorder=8)
    if cp > 0:
        karaoke(ax, cap, speech_frac, 0.210, acc)


def draw_recap(ax, rows, prog, t):
    p = R.eo(prog * 3)
    R.flat_text(ax, 0.5, 0.855, "QUICK RECAP", size=40, color=R.GOLD, alpha=p)
    R.flat_text(ax, 0.5, 0.815, "Screenshot this!", size=19, color=R.LTGREY,
                weight="normal", alpha=p * 0.9)
    cells = [(0.27, 0.62), (0.73, 0.62), (0.27, 0.37), (0.73, 0.37)]
    for k, row in enumerate(rows[:4]):
        cx, cy = cells[k]
        a = R.back_out((prog - 0.08 - k * 0.10) / 0.18) if prog > 0.08 + k * 0.10 else 0
        if a <= 0:
            continue
        acc = R.ACCENTS[k % len(R.ACCENTS)]
        R.pill(ax, cx, cy, 0.42 * min(1, a), 0.20, fill=R.rgba(R.CARD_BG, 1.0),
               edge=R.rgba(acc, 0.95), lw=2.2, alpha=min(1, a), zorder=7)
        R.flat_text(ax, cx, cy + 0.065, row["label"].upper(), size=19, color=acc,
                    alpha=min(1, a), max_w=0.36)
        fs = R.fit_size(row["formula"], 40, 0.36, 0.075)
        R.flat_text(ax, cx, cy - 0.015, row["formula"], size=fs, color=R.WHITE, alpha=min(1, a))


def render_frame(fi):
    t = fi / FPS
    seg = next(s for s in G["segments"] if s["start"] <= t < s["end"] or s is G["segments"][-1])
    prog = (t - seg["start"]) / (seg["end"] - seg["start"])
    sp = seg.get("speech", 0.0)
    speech_frac = min(1.0, max(0.0, (t - seg["start"] - LEAD) / sp)) if sp else 1.0

    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    fig.patch.set_facecolor(R.BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    rows, n = G["rows"], len(G["rows"])
    if seg["kind"] == "intro":
        acc = R.BRAND_CYAN; R.draw_bg(ax, t, acc)
        R.draw_intro(ax, G["data"], 1, 1, n, min(1.0, t / 2.5), t, G["topic"])
    elif seg["kind"] == "card":
        i = seg["i"]; acc = R.ACCENTS[i % len(R.ACCENTS)]
        R.draw_bg(ax, t, acc)
        draw_vcard(ax, rows[i], seg["cap"], i + 1, n, prog, speech_frac, t, acc)
        R.draw_dots(ax, i, n, acc)
    elif seg["kind"] == "recap":
        acc = R.GOLD; R.draw_bg(ax, t, acc); draw_recap(ax, rows, prog, t)
    else:
        acc = R.GOLD; R.draw_bg(ax, t, acc); R.draw_outro(ax, 1, 1, prog, t)
    R.draw_logo_bar(ax, acc)
    R.draw_footer(ax, t, acc)
    fig.savefig(str(Path(G["frame_dir"]) / f"frame_{fi:05d}.png"), dpi=DPI, facecolor=R.BG)
    plt.close(fig)


# ── Build ────────────────────────────────────────────────────────────────────
def build(sample, out, workers=None):
    S = SAMPLES[sample]
    data = R.TOPICS[S["topic"]]
    rows = data["rows"][:len(S["cards"])]
    parts = [("intro", S["intro"], None, 2.8)]
    parts += [("card", c["say"], (k, c["cap"]), 4.0) for k, c in enumerate(S["cards"])]
    parts += [("recap", S["recap"], None, 4.5), ("outro", S["outro"], None, 4.0)]

    segments, clips, t = [], [], 0.0
    for kind, say, extra, min_d in parts:
        a = synth(say)
        sp = len(a) / SR
        d = max(min_d, LEAD + sp + TAIL)
        seg = {"kind": kind, "start": t, "end": t + d, "speech": sp}
        if extra:
            seg["i"], seg["cap"] = extra
        segments.append(seg); clips.append((t + LEAD, a)); t += d
        print(f"  {kind:6s} {d:5.2f}s  speech {sp:4.2f}s  | {say[:60]}")
    total = t
    voice = np.zeros(int(total * SR) + SR, dtype=np.float32)
    for st, a in clips:
        i0 = int(st * SR); voice[i0:i0 + len(a)] += a
    voice = voice[:int(total * SR)]
    voice *= 0.95 / max(1e-6, np.abs(voice).max())

    tmp = Path(tempfile.mkdtemp(prefix="vreel_"))
    frame_dir = tmp / "f"; frame_dir.mkdir()
    write_wav(tmp / "voice.wav", voice)
    nframes = int(round(total * FPS))
    print(f"[INFO] {nframes} frames ({total:.1f}s)")
    g = {"rows": rows, "segments": segments, "data": data, "topic": S["topic"],
         "frame_dir": str(frame_dir)}
    with Pool(workers or os.cpu_count() or 1, initializer=_init, initargs=(g,)) as pool:
        pool.map(render_frame, range(nframes), chunksize=10)
    mux(frame_dir, tmp / "voice.wav", total, out)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[OK] {out} ({Path(out).stat().st_size / 1048576:.1f} MB, {total:.1f}s)")


def mux(frame_dir, voice_wav, total, out, music_vol=0.10):
    cmd = ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
           "-i", str(Path(frame_dir) / "frame_%05d.png"), "-i", str(voice_wav)]
    if R.BG_MUSIC.exists():
        cmd += ["-stream_loop", "-1", "-i", str(R.BG_MUSIC), "-filter_complex",
                f"[2:a]volume={music_vol},afade=t=in:st=0:d=1.5,afade=t=out:st={total - 2:.2f}:d=2[m];"
                f"[1:a]volume=1.0[v];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
                "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-profile:v", "main", "-level", "4.0", "-preset", "slow",
            "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            "-c:a", "aac", "-ar", "44100", "-b:a", "128k", "-t", f"{total:.2f}", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr[-800:])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", default="electricity", choices=list(SAMPLES))
    ap.add_argument("--out", default="voice_reel_sample.mp4")
    a = ap.parse_args()
    build(a.sample, a.out)
