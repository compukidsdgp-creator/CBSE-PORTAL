"""WHY? — Why does total internal reflection only happen from a denser to a rarer medium?  (Class 12 Ray Optics)"""
import numpy as np
from matplotlib.patches import Circle, Rectangle, Wedge
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why is TIR only from DENSER to RARER?"
TAGS = "Class 12 Physics"
BEATS = [
    ("hook",    "Total internal reflection powers optical fibres and makes diamonds sparkle. But it only works one way. Why?",
                "TIR powers optical fibres and diamond sparkle… but only works ONE way. Why?", 5.0),
    ("away",    "When light goes from glass into air, it bends away from the normal. The refracted ray is always at a bigger angle.",
                "Glass → air: light bends AWAY from the normal — the refracted angle is always BIGGER.", 5.6),
    ("tilt",    "Tilt the ray more. The refracted ray swings closer and closer to the surface.",
                "Tilt the ray more… the refracted ray swings closer to the surface.", 4.0),
    ("critical", "At the critical angle, the refracted ray just grazes the surface, at ninety degrees.",
                 "At the CRITICAL angle, it grazes the surface at 90°.", 4.0),
    ("tir",     "Go beyond it, and refraction would need more than ninety degrees. Impossible! So all the light reflects back.",
                "Beyond it, refraction would need MORE than 90° — impossible! ALL light reflects back.", 5.4),
    ("other",   "Going from air into glass, light bends towards the normal. The angle never reaches ninety. So no T I R.",
                "Air → glass bends TOWARDS the normal — never reaches 90° → NO TIR.", 5.0),
    ("math",    "Sine C equals one by mu. Only from denser to rarer.",
                "sin C = 1 / μ  — only from DENSER to RARER.", 3.6),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """💎 WHY? — Why does total internal reflection only happen from DENSER to RARER?

Glass → air: light bends AWAY from the normal (refracted angle > incident angle)
Tilt more → refracted ray reaches 90° at the CRITICAL angle C
Beyond C → refraction would need > 90° 🚫 → ALL light reflects = TIR ✨

Air → glass: light bends TOWARDS the normal — never reaches 90° → no TIR

sin C = 1/μ · Uses: optical fibres, diamond sparkle 💎

Ray Optics — Class 12 Physics. 📗

💾 Save it · 📤 Share with your batchmates

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #TotalInternalReflection #RayOptics #Class12Physics #CriticalAngle #JEE #CBSE"""

MU = 1.5
C_DEG = np.degrees(np.arcsin(1 / MU))     # ≈ 41.8°


def ray(dax, p, q, col, a, lw=4, z=6):
    dax.plot([p[0], q[0]], [p[1], q[1]], color=col, lw=lw, alpha=a, zorder=z, solid_capstyle="round")
    m = (0.55 * p[0] + 0.45 * q[0], 0.55 * p[1] + 0.45 * q[1])
    d = np.array(q) - np.array(p); d = d / (np.linalg.norm(d) + 1e-9)
    dax.annotate("", xy=(m[0] + 0.12 * d[0], m[1] + 0.12 * d[1]), xytext=m,
                 arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, alpha=a, mutation_scale=26), zorder=z)


def draw(c):
    dax = c.area(0.0, 0.0, 7.0)
    a0 = ease(c.phase("hook", 0.05, 0.35))
    ot = ease(c.phase("other", 0.0, 0.25))
    ma = ease(c.phase("math", 0.0, 0.3))
    # media: glass bottom (denser), air top
    top_lab, bot_lab = ("glass (denser)", "air (rarer)") if ot > 0.5 else ("air (rarer)", "glass (denser)")
    dax.add_patch(Rectangle((-3.5, -2.6), 7.0, 2.6, facecolor="#1d4e7a" if ot < 0.5 else "#0b1530", edgecolor="none",
                            alpha=a0 * 0.7 * (1 - ma), zorder=2))
    dax.add_patch(Rectangle((-3.5, 0.0), 7.0, 2.6, facecolor="#0b1530" if ot < 0.5 else "#1d4e7a", edgecolor="none",
                            alpha=a0 * 0.7 * (1 - ma), zorder=2))
    dax.plot([-3.5, 3.5], [0, 0], color=LTGREY, lw=2, alpha=a0 * (1 - ma), zorder=3)
    dax.plot([0, 0], [-2.4, 2.4], color=GREY, lw=2, ls=(0, (5, 4)), alpha=a0 * (1 - ma), zorder=3)
    outline(dax.text(-3.3, 2.2, top_lab, ha="left", fontsize=20, color=LTGREY, fontweight="bold", alpha=a0 * (1 - ma), zorder=8))
    outline(dax.text(-3.3, -2.4, bot_lab, ha="left", fontsize=20, color=CYAN, fontweight="bold", alpha=a0 * (1 - ma), zorder=8))
    if ot < 0.99 and a0 > 0.01:
        b = a0 * (1 - ot)
        # incident angle sweeps up through the beats
        if c.at("tir"):
            th = lerp(C_DEG, 60, ease(c.phase("tir", 0.0, 0.4)))
        elif c.at("critical"):
            th = lerp(35, C_DEG, ease(c.phase("critical", 0.0, 0.4)))
        elif c.at("tilt"):
            th = lerp(22, 35, ease(c.phase("tilt", 0.0, 0.8)))
        else:
            th = 22
        r = np.radians(th)
        L = 2.3
        p = (-L * np.sin(r), -L * np.cos(r))
        ray(dax, p, (0, 0), GOLD, b)
        s = MU * np.sin(r)
        if s < 0.999:
            rr = np.arcsin(s)
            ray(dax, (0, 0), (L * np.sin(rr), L * np.cos(rr)), PINK, b * ease(c.phase("away", 0.0, 0.4)) if c.at("away") or True else b)
            dax.add_patch(Wedge((0, 0), 0.8, 90 - np.degrees(rr), 90, facecolor=PINK, alpha=0.25 * b, zorder=4))
            outline(dax.text(0.9 * np.sin(rr / 2) + 0.15, 1.1, f"{np.degrees(rr):.0f}°", fontsize=20, color=PINK,
                             fontweight="bold", alpha=b, zorder=8))
        elif s < 1.02:
            ray(dax, (0, 0), (3.2, 0.03), PINK, b)
            outline(dax.text(1.7, 0.3, "90° (grazing)", ha="center", fontsize=20, color=PINK, fontweight="bold", alpha=b, zorder=8))
        # weak/strong reflected ray
        refl = 0.25 if s < 0.999 else 1.0
        ray(dax, (0, 0), (L * np.sin(r), -L * np.cos(r)), GREEN, b * refl, lw=4 if refl == 1 else 2)
        dax.add_patch(Wedge((0, 0), 0.7, 270 - th, 270, facecolor=GOLD, alpha=0.25 * b, zorder=4))
        outline(dax.text(-0.75, -1.05, f"{th:.0f}°", fontsize=20, color=GOLD, fontweight="bold", alpha=b, zorder=8))
        if c.at("critical") and not c.at("tir"):
            outline(dax.text(1.8, -1.0, f"C ≈ {C_DEG:.0f}°", ha="center", fontsize=26, color=WHITE, fontweight="bold",
                             alpha=b * ease(c.phase("critical", 0.4, 0.7)), zorder=8))
        if c.at("tir"):
            outline(dax.text(1.9, 1.2, "> 90°?\nimpossible", ha="center", va="center", fontsize=22, color=PINK,
                             fontweight="bold", alpha=b * ease(c.phase("tir", 0.3, 0.6)), zorder=8))
            outline(dax.text(1.9, -1.9, "ALL reflected", ha="center", fontsize=24, color=GREEN, fontweight="bold",
                             alpha=b * ease(c.phase("tir", 0.4, 0.7)), zorder=8))
    if ot > 0.01:
        o = ot * (1 - ma)
        # now light goes from air (bottom, rarer) into glass (top, denser)
        th = lerp(20, 80, ease(c.phase("other", 0.15, 0.85)))
        r = np.radians(th)
        L = 2.3
        ray(dax, (-L * np.sin(r), -L * np.cos(r)), (0, 0), GOLD, o)
        rr = np.arcsin(np.sin(r) / MU)
        ray(dax, (0, 0), (L * np.sin(rr), L * np.cos(rr)), PINK, o)
        outline(dax.text(1.9, 1.3, f"{np.degrees(rr):.0f}°  (< {C_DEG:.0f}°)", ha="center", fontsize=21, color=PINK,
                         fontweight="bold", alpha=o, zorder=8))
        outline(dax.text(1.8, -1.2, "never reaches 90°", ha="center", fontsize=22, color=WHITE, fontweight="bold",
                         alpha=o * ease(c.phase("other", 0.4, 0.7)), zorder=8))
    if ma > 0.01:
        outline(dax.text(0, 0.7, r"$\sin C = \dfrac{1}{\mu}$", ha="center", va="center", fontsize=54, color=GOLD,
                         alpha=ma, zorder=8))
        outline(dax.text(0, -0.9, "denser → rarer only", ha="center", fontsize=30, color=CYAN, fontweight="bold",
                         alpha=ease(c.phase("math", 0.3, 0.6)), zorder=8))
    c.steps([("$\\sin C = 1/\\mu$", 0.0, WHITE),
             ("TIR: denser → rarer, angle > C", 0.3, GOLD)], ys=(0.345, 0.285))
