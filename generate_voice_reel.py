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

from reel_narration import NARRATION, line      # noqa: E402

# How the narrator says each topic's name (the on-screen titles are not always speakable)
SPOKEN_TITLE = {
    "em_induction": "Electromagnetic Induction", "current_electricity": "Current Electricity",
    "electrostatics": "Electrostatics", "optics": "Optics", "semiconductor": "Semiconductor",
    "magnetism": "Magnetism", "dual_nature": "Dual Nature", "atoms_nuclei": "Atoms and Nuclei",
    "light_class10": "Light", "electricity_class10": "Electricity",
    "chemical_kinetics": "Chemical Kinetics", "electrochemistry": "Electrochemistry",
    "solutions": "Solutions", "coordination": "Coordination Compounds", "solid_state": "Solid State",
    "chemical_reactions_cl10": "Chemical Reactions", "genetics": "Genetics",
    "photosynthesis": "Photosynthesis", "reproduction": "Human Reproduction", "ecology": "Ecology",
    "life_processes_cl10": "Life Processes", "calculus": "Calculus", "vectors_3d": "Vectors and 3 D",
    "probability": "Probability", "matrices_determinants": "Matrices and Determinants",
    "linear_programming": "Linear Programming", "quadratic_cl10": "Quadratic Equations",
    "trigonometry_cl10": "Trigonometry", "boolean_algebra": "Boolean Algebra",
    "networking": "Computer Networks", "python_basics": "Python", "dbms": "Database",
}
NUM = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five"}


def script(topic_id, part):
    """Intro / cards / recap / outro narration for one reel (one part of a topic)."""
    data = R.TOPICS[topic_id]
    chunks = R.split_rows(data["rows"])
    rows = chunks[part - 1]
    offset = sum(len(c) for c in chunks[:part - 1])
    title = SPOKEN_TITLE.get(topic_id, data["title_line1"])
    cls = {"Class 10": "class ten", "Class 12": "class twelve", "Class 11": "class eleven"}.get(
        R.class_label(data.get("chapter_tag", "")), "")
    what = "key points" if data["subject"] == "CS" else "formulas"
    n, nparts = len(rows), len(chunks)
    boards = f" for your {cls} boards" if cls else ""
    if part == 1:
        intro = f"{NUM[n]} {title} {what} you must know{boards}."
    else:
        intro = f"{NUM[n]} more {title} {what}{boards}. Part {NUM[part].lower()}."
    recap = (f"That's part {NUM[part].lower()} of {title}. Save this reel for your revision."
             if nparts > 1 else f"That's {title} in {NUM[n].lower()} {what}. Save this reel for your revision.")
    outro = (f"Follow C B S E Mock, so you don't miss part {NUM[part + 1].lower()}."
             if part < nparts else "Share it with your batchmates, and follow C B S E Mock for more.")
    cards = [dict(zip(("say", "cap"), line(topic_id, offset + k))) for k in range(n)]
    return {"data": data, "rows": rows, "offset": offset, "total": len(data["rows"]),
            "part": part, "nparts": nparts, "intro": intro, "cards": cards,
            "recap": recap, "outro": outro}


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
    cells = {1: [(0.5, 0.50)], 2: [(0.27, 0.50), (0.73, 0.50)],
             3: [(0.27, 0.62), (0.73, 0.62), (0.5, 0.37)]}.get(
        len(rows), [(0.27, 0.62), (0.73, 0.62), (0.27, 0.37), (0.73, 0.37)])
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
        R.draw_intro(ax, G["data"], G["part"], G["nparts"], n, min(1.0, t / 2.5), t, G["topic"])
    elif seg["kind"] == "card":
        i = seg["i"]; acc = R.ACCENTS[(G["offset"] + i) % len(R.ACCENTS)]
        R.draw_bg(ax, t, acc)
        draw_vcard(ax, rows[i], seg["cap"], G["offset"] + i + 1, G["total"], prog, speech_frac, t, acc)
        R.draw_dots(ax, i, n, acc)
    elif seg["kind"] == "recap":
        acc = R.GOLD; R.draw_bg(ax, t, acc); draw_recap(ax, rows, prog, t)
    else:
        acc = R.GOLD; R.draw_bg(ax, t, acc); R.draw_outro(ax, G["part"], G["nparts"], prog, t)
    R.draw_logo_bar(ax, acc)
    R.draw_footer(ax, t, acc)
    fig.savefig(str(Path(G["frame_dir"]) / f"frame_{fi:05d}.png"), dpi=DPI, facecolor=R.BG)
    plt.close(fig)


# ── Build ────────────────────────────────────────────────────────────────────
def build(topic_id, part, out, workers=None):
    S = script(topic_id, part)
    rows = S["rows"]
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
    print(f"[INFO] {topic_id} part {part}/{S['nparts']}: {nframes} frames ({total:.1f}s)")
    g = {"rows": rows, "segments": segments, "data": S["data"], "topic": topic_id,
         "part": part, "nparts": S["nparts"], "offset": S["offset"], "total": S["total"],
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


def main():
    ap = argparse.ArgumentParser(description="Voiced Formula Flash reels")
    ap.add_argument("--topic", action="append", help="topic id (repeatable); default: all")
    ap.add_argument("--part", type=int, default=None)
    ap.add_argument("--out-dir", default=str(R.OUT_DIR / "voiced"))
    ap.add_argument("--only-in", default=None,
                    help="render only reels whose queue file name exists in this folder")
    ap.add_argument("--out", default=None, help="single output file (with --topic and --part)")
    a = ap.parse_args()
    topics = a.topic or list(R.TOPICS)
    for tid in topics:
        missing = [k for k in NARRATION if k not in R.TOPICS]
        if tid not in NARRATION or len(NARRATION[tid]) != len(R.TOPICS[tid]["rows"]):
            sys.exit(f"Narration missing or incomplete for '{tid}'")
    out_dir = Path(a.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    have = set(os.listdir(a.only_in)) if a.only_in else None
    for tid in topics:
        nparts = len(R.split_rows(R.TOPICS[tid]["rows"]))
        for pn in ([a.part] if a.part else range(1, nparts + 1)):
            name = R.queue_name(tid, pn, nparts)
            if have is not None and name not in have:
                print(f"[SKIP] {name} not in {a.only_in}"); continue
            out = Path(a.out) if a.out else out_dir / name
            if out.exists() and not a.out:
                print(f"[SKIP] {name} already rendered"); continue
            build(tid, pn, out)


if __name__ == "__main__":
    main()
