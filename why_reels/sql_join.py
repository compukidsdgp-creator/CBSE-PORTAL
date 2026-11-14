"""WHY? — How does an SQL JOIN match rows?  (Class 12 Computer Science · SQL)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "How does SQL JOIN match rows?"
TAGS = "Class 12 Computer Science"
BEATS = [
    ("hook",      "How does a SQL JOIN combine two tables? It's all about one matching column.",
                  "How does an SQL JOIN combine two tables? It's all about ONE matching column.", 4.0),
    ("tables",    "Here's a Students table, and a Marks table. Both have a roll number column.",
                  "A Students table and a Marks table — both have a ROLL column.", 4.2),
    ("match",     "JOIN looks for rows where the roll numbers are equal.",
                  "JOIN looks for rows where the roll numbers are EQUAL.", 3.6),
    ("result",    "Matching rows are glued together into one result. Aman with ninety two. Riya with eighty eight.",
                  "Matching rows are glued together: Aman → 92, Riya → 88.", 5.0),
    ("unmatched", "Kabir has no marks, and roll four has no student, so an inner join leaves them out.",
                  "Kabir has no marks, roll 4 has no student → an INNER JOIN leaves them out.", 5.0),
    ("left",      "A left join keeps every student, and fills the missing marks with null.",
                  "A LEFT JOIN keeps every student and fills missing marks with NULL.", 4.4),
    ("math",      "In SQL, you write: select name, marks, from Students join Marks, on the roll numbers.",
                  "SELECT name, marks FROM Students JOIN Marks ON Students.roll = Marks.roll;", 5.0),
    ("end",       "Follow C B S E Mock for more why videos.",
                  "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🗄️ WHY? — How does an SQL JOIN match rows?

Students(roll, name) + Marks(roll, marks)
JOIN finds rows where roll = roll and glues them together 🔗
Aman → 92 ✅  Riya → 88 ✅
Kabir (no marks) & roll 4 (no student) → left out by INNER JOIN ❌
LEFT JOIN keeps every student → missing marks = NULL

SELECT name, marks FROM Students JOIN Marks ON Students.roll = Marks.roll;

CS Class 12 SQL — joins finally make sense. 🧠

💾 Save it · 📤 Share with your CS batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #SQL #MySQL #Database #ComputerScience #CSClass12 #CBSE"""

MONO = "DejaVu Sans Mono"
STU = [(1, "Aman"), (2, "Riya"), (3, "Kabir")]
MRK = [(2, 88), (1, 92), (4, 75)]
RH = 0.55
END_Y = 0.369


def table(dax, x, y, title, head, rows, a, col, hl=None, dim=None):
    w = 2.9
    dax.text(x + w / 2, y + 0.55, title, ha="center", va="center", fontsize=26, fontweight="bold", color=col,
             alpha=a, zorder=6)
    dax.add_patch(Rectangle((x, y - RH / 2), w, RH, facecolor=col, edgecolor=NAVY, lw=1.5, alpha=a * 0.9, zorder=5))
    for j, h in enumerate(head):
        dax.text(x + 0.7 + j * 1.5, y, h, ha="center", va="center", fontsize=21, fontweight="bold", color=NAVY,
                 alpha=a, zorder=6)
    for i, r in enumerate(rows):
        yy = y - (i + 1) * RH
        al = a * (0.3 if dim and i in dim else 1.0)
        face = "#1d3a6b" if hl and i in hl else "#13264d"
        dax.add_patch(Rectangle((x, yy - RH / 2), w, RH, facecolor=face, edgecolor="#2b3f66", lw=1.5, alpha=al, zorder=5))
        for j, v in enumerate(r):
            dax.text(x + 0.7 + j * 1.5, yy, str(v), ha="center", va="center", fontsize=22, fontweight="bold",
                     color=WHITE if v != "NULL" else PINK, family=MONO if j == 0 else None, alpha=al, zorder=6)
    return w


def draw(c):
    dax = c.area(0.0, 0.0, 7.4)
    ta = ease(c.phase("tables", 0.0, 0.4))
    Lx, Rx, Ty = -3.45, 0.55, 1.85
    unm = c.at("unmatched")
    if ta > 0:
        table(dax, Lx, Ty, "Students", ["roll", "name"], STU, ta, CYAN, dim={2} if unm and not c.at("left") else None)
        table(dax, Rx, Ty, "Marks", ["roll", "marks"], MRK, ta, GOLD, dim={2} if unm else None)
        ra = ease(c.phase("tables", 0.5, 0.8)) * (1 - ease(c.phase("result", 0.0, 0.2)))
        if ra > 0:
            for x in (Lx + 0.7, Rx + 0.7):
                dax.add_patch(Rectangle((x - 0.42, Ty - 3 * RH - RH / 2), 0.84, 4 * RH, fill=False, edgecolor=PINK,
                                        lw=3, alpha=ra, zorder=7))
    # matching lines
    ma = ease(c.phase("match", 0.1, 0.6))
    if ma > 0:
        for si, (sr, _) in enumerate(STU):
            for mi, (mr, _) in enumerate(MRK):
                if sr == mr:
                    y1 = Ty - (si + 1) * RH
                    y2 = Ty - (mi + 1) * RH
                    p = ease(c.phase("match", 0.1 + si * 0.2, 0.5 + si * 0.2))
                    x1, x2 = Lx + 2.9, Rx
                    dax.plot([x1, lerp(x1, x2, p)], [y1, lerp(y1, y2, p)], color=GREEN, lw=4, alpha=ma, zorder=8)
                    if p > 0.9:
                        dax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.18, "=", ha="center", fontsize=26,
                                 fontweight="bold", color=GREEN, zorder=9)
    if unm:
        ua = ease(c.phase("unmatched", 0.15, 0.45)) * (1 - ease(c.phase("left", 0.0, 0.2)))
        for x, y in [(Lx + 3.05, Ty - 3 * RH), (Rx + 3.05, Ty - 3 * RH)]:
            outline(dax.text(x, y, "✗", ha="left", va="center", fontsize=30, fontweight="bold", color=PINK,
                             alpha=max(ua, 0.0), zorder=9))
    # result table
    rs = ease(c.phase("result", 0.1, 0.5))
    if rs > 0:
        rows = [(1, "Aman", 92), (2, "Riya", 88)]
        if c.at("left"):
            rows.append((3, "Kabir", "NULL"))
        ry = -0.92
        title = "RESULT (INNER JOIN)" if not c.at("left") else "RESULT (LEFT JOIN)"
        w = 4.4
        x0 = -w / 2
        dax.text(0, ry + 0.55, title, ha="center", va="center", fontsize=24, fontweight="bold", color=GREEN,
                 alpha=rs, zorder=6)
        dax.add_patch(Rectangle((x0, ry - RH / 2), w, RH, facecolor=GREEN, edgecolor=NAVY, lw=1.5, alpha=rs * 0.9, zorder=5))
        for j, h in enumerate(["roll", "name", "marks"]):
            dax.text(x0 + 0.7 + j * 1.5, ry, h, ha="center", va="center", fontsize=21, fontweight="bold", color=NAVY,
                     alpha=rs, zorder=6)
        for i, r in enumerate(rows):
            a = ease(c.phase("result", 0.3 + i * 0.25, 0.55 + i * 0.25)) if i < 2 else ease(c.phase("left", 0.2, 0.5))
            yy = ry - (i + 1) * RH
            dax.add_patch(Rectangle((x0, yy - RH / 2), w, RH, facecolor="#13264d", edgecolor="#2b3f66", lw=1.5,
                                    alpha=a, zorder=5))
            for j, v in enumerate(r):
                dax.text(x0 + 0.7 + j * 1.5, yy, str(v), ha="center", va="center", fontsize=22, fontweight="bold",
                         color=PINK if v == "NULL" else WHITE, alpha=a, zorder=6)
    if c.at("math"):
        rows = [("SELECT name, marks", WHITE), ("FROM Students JOIN Marks", CYAN),
                ("ON Students.roll = Marks.roll;", GOLD)]
        for k, (s_, col) in enumerate(rows):
            a = ease(c.phase("math", 0.05 + k * 0.2, 0.25 + k * 0.2))
            if a > 0:
                c.ax.text(0.5, 0.322 - k * 0.043, s_, ha="center", va="center", fontsize=30, color=col, family=MONO,
                          fontweight="bold", alpha=a, zorder=10, transform=c.ax.transAxes)
