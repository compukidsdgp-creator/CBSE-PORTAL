"""Shared helper for code-panel WHY? reels (CS topics): a dark editor box with syntax-tinted lines."""
import re
from matplotlib.patches import FancyBboxPatch, Rectangle
from why_kit import CYAN, GOLD, PINK, GREEN, PURPLE, WHITE, LTGREY, GREY

KW = {"for", "in", "if", "elif", "else", "def", "return", "print", "range", "while", "True", "False", "and", "or",
      "not", "int", "input", "len", "sum", "float", "str", "bool"}


def code(dax, x0, y_top, lines, a, w=6.4, size=26, line_h=0.5, hl=None, hl_col=GOLD, title=None, show=None):
    """Draw an editor panel. lines: list of str (leading spaces kept). hl: index of highlighted line.
    show: number of lines visible so far (typing effect)."""
    if a <= 0.01:
        return
    n = len(lines)
    h = n * line_h + 0.35 + (0.35 if title else 0)
    dax.add_patch(FancyBboxPatch((x0, y_top - h), w, h, boxstyle="round,pad=0,rounding_size=0.15",
                                 facecolor="#0b1530", edgecolor="#2a3d6b", lw=2.5, alpha=a, zorder=5))
    y = y_top - 0.32
    if title:
        dax.text(x0 + 0.2, y, title, ha="left", va="center", fontsize=size - 5, color=GREY, alpha=a, zorder=6,
                 family="DejaVu Sans Mono")
        y -= 0.35
    shown = n if show is None else max(0, min(n, int(show)))
    for i, s in enumerate(lines[:shown]):
        yy = y - i * line_h
        if hl is not None and i == hl:
            dax.add_patch(Rectangle((x0 + 0.08, yy - line_h / 2 + 0.03), w - 0.16, line_h - 0.06, facecolor=hl_col,
                                    edgecolor="none", alpha=0.18 * a, zorder=5.5))
        stripped = s.lstrip(" ")
        indent = len(s) - len(stripped)
        first = re.match(r"[A-Za-z_]+", stripped)
        col = WHITE
        if stripped.startswith("#"):
            col = GREY
        elif first and first.group(0) in KW:
            col = PINK if first.group(0) in {"for", "if", "elif", "else", "def", "return", "while"} else CYAN
        dax.text(x0 + 0.25 + indent * size * 0.0054, yy, stripped, ha="left", va="center", fontsize=size, color=col,
                 alpha=a, zorder=6, family="DejaVu Sans Mono")
