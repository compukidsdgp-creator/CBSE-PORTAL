"""WHY? — How does data TRAVEL across the internet?  (Class 12 Computer Science · Computer Networks)"""
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "How does data TRAVEL across the internet?"
TAGS = "Class 12 Computer Science"
BEATS = [
    ("hook",   "When you send a photo, how does it travel across the internet? In tiny pieces!",
               "When you send a photo, how does it travel across the internet? In tiny PIECES!", 4.0),
    ("split",  "The data is broken into small packets. Each packet is labelled with the destination address, and its number.",
               "The data is split into PACKETS — each labelled with the destination address and its number.", 5.6),
    ("routes", "Packets hop through routers, and each one can take a different path.",
               "Packets hop through ROUTERS — each can take a different path.", 4.4),
    ("arrive", "So they may arrive out of order. Three, then one, then four.",
               "They may arrive OUT OF ORDER: 3… 1… 4…", 3.8),
    ("fix",    "The receiver uses the numbers to put them back in order, and asks again for any packet that got lost.",
               "The receiver reorders them by number — and asks again for any lost packet.", 5.4),
    ("proto",  "This teamwork is T C P and I P. I P handles addresses and routing. T C P makes sure everything arrives, in order.",
               "TCP/IP: IP handles addresses & routing, TCP makes sure everything arrives in order.", 6.0),
    ("end",    "Follow C B S E Mock for more why videos.",
               "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🌐 WHY? — How does data TRAVEL across the internet?

1️⃣ Your photo is split into small PACKETS 📦 — each with the destination IP address + a number
2️⃣ Packets hop through ROUTERS, each taking its own path 🛣️
3️⃣ They can arrive out of order (3, 1, 4…)
4️⃣ The receiver reorders them and asks again for any lost packet ✅

That's TCP/IP: IP = addressing & routing · TCP = order & reliability

CS Class 12 Computer Networks — packet switching made visual. 🧠

💾 Save it · 📤 Share with your CS batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #ComputerNetworks #TCPIP #Internet #ComputerScience #CSClass12 #CBSE"""

PCOL = [CYAN, GOLD, PINK, GREEN, PURPLE, "#ff9f43"]
SEND, RECV = (-3.3, 0.0), (3.3, 0.0)
NODES = {"A": (-1.6, 1.7), "B": (-1.4, -1.5), "C": (0.1, 0.3), "D": (1.6, 1.8), "E": (1.5, -1.6), "F": (0.0, 2.4)}
PATHS = [["A", "F", "D"], ["B", "C", "E"], ["A", "C", "D"], ["B", "E"], ["A", "D"], ["B", "C", "D"]]
ARRIVE = [2, 0, 3, 5, 1, 4]                 # packet index order of arrival (0-based)
LOST = 4                                     # packet #5 gets lost, then is re-sent


def packet(dax, x, y, k, a, s=1.0, z=8):
    dax.add_patch(FancyBboxPatch((x - 0.32 * s, y - 0.24 * s), 0.64 * s, 0.48 * s, boxstyle="round,pad=0,rounding_size=0.08",
                                 facecolor=PCOL[k], edgecolor=WHITE, lw=1.8, alpha=a, zorder=z))
    dax.text(x, y, str(k + 1), ha="center", va="center", fontsize=19 * s, fontweight="bold", color=NAVY, alpha=a, zorder=z + 1)


def along(path, f):
    pts = [SEND] + [NODES[n] for n in path] + [RECV]
    seg = np.array([np.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)])
    L = seg.sum() * max(0, min(1, f))
    for i, s in enumerate(seg):
        if L <= s:
            t = L / s
            return pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t
        L -= s
    return RECV


def draw(c):
    dax = c.area(0.0, 0.2, 7.8)
    na = ease(c.phase("routes", 0.0, 0.3))
    # network
    if na > 0:
        edges = set()
        for p in PATHS:
            pts = ["S"] + p + ["R"]
            for i in range(len(pts) - 1):
                edges.add(tuple(sorted((pts[i], pts[i + 1]))))
        pos = dict(NODES, S=SEND, R=RECV)
        for a_, b_ in edges:
            dax.plot([pos[a_][0], pos[b_][0]], [pos[a_][1], pos[b_][1]], color="#2b3f66", lw=3, alpha=na, zorder=2)
        for n, (x, y) in NODES.items():
            dax.add_patch(Circle((x, y), 0.28, facecolor="#13264d", edgecolor=CYAN, lw=2.5, alpha=na, zorder=4))
            dax.text(x, y, "R", ha="center", va="center", fontsize=16, fontweight="bold", color=CYAN, alpha=na, zorder=5)
        outline(dax.text(-0.3, -2.25, "routers", ha="center", fontsize=22, fontweight="bold", color=CYAN,
                         alpha=na * (1 - ease(c.phase("end", 0.0, 0.2))), zorder=6))
    # sender / receiver
    ha = ease(c.phase("hook", 0.2, 0.6))
    for (x, y), lab in [(SEND, "you"), (RECV, "friend")]:
        dax.add_patch(FancyBboxPatch((x - 0.55, y - 0.45), 1.1, 0.9, boxstyle="round,pad=0,rounding_size=0.15",
                                     facecolor="#1d3a6b", edgecolor=WHITE, lw=2.5, alpha=ha, zorder=5))
        dax.text(x, y + 0.02, "📱" if False else "▭", ha="center", va="center", fontsize=30, color=WHITE, alpha=ha, zorder=6)
        outline(dax.text(x, y - 0.75, lab, ha="center", fontsize=22, fontweight="bold", color=WHITE, alpha=ha, zorder=6))

    # the photo, then split into packets
    sp = ease(c.phase("split", 0.1, 0.55))
    if c.at("hook") and not c.at("routes"):
        pa = ease(c.phase("hook", 0.3, 0.7))
        if sp < 1:
            for k in range(6):
                r, q = divmod(k, 3)
                x0 = -0.95 + q * 0.62 + sp * (q - 1) * 0.35
                y0 = 1.25 - r * 0.62 - sp * (r - 0.5) * 0.35
                dax.add_patch(FancyBboxPatch((x0 - 0.31, y0 - 0.31), 0.62, 0.62, boxstyle="round,pad=0,rounding_size=0.04",
                                             facecolor=PCOL[k], edgecolor=NAVY if sp < 0.1 else WHITE, lw=1.5,
                                             alpha=pa, zorder=6))
        if sp > 0.3:
            la = ease((sp - 0.3) / 0.7)
            for k in range(6):
                r, q = divmod(k, 3)
                x, y = -1.35 + q * 1.3, 1.6 - r * 1.25
                packet(dax, x, y, k, la, s=1.5)
                dax.text(x, y - 0.55, "to: 142.250.x.x", ha="center", fontsize=12, color=LTGREY, alpha=la * 0.9, zorder=9)
    # packets travelling
    if c.at("routes"):
        for k in range(6):
            st = 0.1 + k * 0.1
            f = c.phase("routes", st, st + 0.55) + 0.0
            if k == LOST:
                f = min(f, 0.45)
            fr = c.phase("arrive", 0.0, 1.0)
            f_arr = f
            # arrival order trickles across the arrive beat
            ia = ARRIVE.index(k)
            if c.at("arrive"):
                f_arr = max(f, ease(c.phase("arrive", ia * 0.14, ia * 0.14 + 0.25)) if k != LOST else 0.45)
            if c.at("fix"):
                f_arr = 1.0 if k != LOST else max(0.45, ease(c.phase("fix", 0.35, 0.8)))
            if f_arr <= 0:
                continue
            x, y = along(PATHS[k], f_arr * 0.92)
            if f_arr >= 0.92 or (c.at("fix") and k != LOST):
                # parked at the receiver, in arrival order (then sorted)
                srt = ease(c.phase("fix", 0.0, 0.35))
                slot_arr = ia
                slot_sorted = k
                slot = lerp(slot_arr, slot_sorted, srt)
                x, y = 1.85 + (slot % 3) * 0.72, -1.55 - (slot // 3) * 0.58
                x = lerp(2.55 - 1.4 + slot * 0.0, x, 1.0)
            lost = k == LOST and not c.at("fix") and f_arr <= 0.45 and c.at("arrive")
            packet(dax, x, y, k, 1.0 if not lost else 0.35)
            if k == LOST and c.at("arrive") and not c.at("fix"):
                outline(dax.text(x, y + 0.45, "lost!", ha="center", fontsize=20, fontweight="bold", color=PINK, zorder=10))
        if c.at("fix"):
            ra = ease(c.phase("fix", 0.3, 0.5)) * (1 - ease(c.phase("fix", 0.85, 1.0)))
            if ra > 0:
                outline(dax.text(-0.2, 1.05 + 1.6, "resend #5", ha="center", fontsize=22, fontweight="bold", color=PURPLE,
                                 alpha=ra, zorder=10))
            ok = back_out(c.phase("fix", 0.8, 0.95))
            if ok > 0.01:
                c.pill(0.5, 0.385, 0.50 * min(1, ok), 0.058, GREEN, alpha=min(1, ok) * (1 - ease(c.phase("proto", 0, 0.2))),
                       dark="#06261a")
                c.text(0.5, 0.385, "photo rebuilt  ✓", size=36, color=GREEN, alpha=min(1, ok) * (1 - ease(c.phase("proto", 0, 0.2))))
    c.steps([("IP  →  addresses & routing", 0.1, CYAN), ("TCP  →  order & reliability", 0.45, GOLD)],
            ys=(0.355, 0.288), beat="proto")
