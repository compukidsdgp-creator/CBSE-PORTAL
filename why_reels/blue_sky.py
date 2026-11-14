"""WHY? — Why is the sky BLUE?  (Class 10 Science · Human Eye & the Colourful World)"""
import math
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle
from why_kit import ease, lerp, outline, back_out, CYAN, GOLD, PINK, GREEN, PURPLE, NAVY, WHITE, LTGREY, GREY

TITLE = "Why is the sky BLUE?"
TAGS = "Class 10 Science"
BEATS = [
    ("hook",    "Why is the sky blue? Not violet, not white, but blue. It's all about scattering.",
                "Why is the sky BLUE — not violet, not white? It's all about SCATTERING.", 4.2),
    ("white",   "Sunlight looks white, but it's a mix of all the colours.",
                "Sunlight looks white, but it's a mix of ALL the colours.", 3.4),
    ("air",     "In the air, it meets tiny gas molecules, far smaller than the light's wavelength.",
                "In the air it meets tiny gas molecules — far smaller than light's wavelength.", 4.4),
    ("scatter", "Short wavelengths like blue get scattered much more than long ones like red. "
                "Scattering goes as one by wavelength to the power four.",
                "Short-wavelength BLUE scatters far more than long-wavelength red: scattering ∝ 1/λ⁴", 6.4),
    ("eyes",    "So blue light reaches our eyes from every direction. Violet scatters even more, "
                "but our eyes are more sensitive to blue. The sky looks blue.",
                "Blue reaches our eyes from EVERY direction. (Violet scatters more, but our eyes favour blue.)", 6.6),
    ("sunset",  "At sunset, light crosses much more air. Most of the blue is scattered away, leaving reds and oranges.",
                "At sunset, light crosses much more air → blue is scattered away → reds and oranges remain.", 5.6),
    ("end",     "Follow C B S E Mock for more why videos.",
                "Follow @cbsemock for more WHY? videos.", 3.0),
]
CAPTION = """🌤️ WHY? — Why is the sky BLUE?

Sunlight = a mix of all colours 🌈
Tiny air molecules scatter SHORT wavelengths (blue) far more than long ones (red): scattering ∝ 1/λ⁴
→ blue light reaches our eyes from every part of the sky 💙
(Violet scatters even more, but our eyes are more sensitive to blue!)
🌅 Sunset: light crosses more air → blue is scattered away → reds & oranges remain

Class 10 Science — Human Eye & the Colourful World (scattering of light). 🧠

💾 Save it · 📤 Share with your science group

🌐 Free notes & mock papers → https://cbsemock.org.in
📲 Telegram: t.me/cbsemockportal

#WhySeries #CBSEMock #Physics #ScatteringOfLight #Class10Science #BoardExam2027 #CBSE #ScienceFacts"""

RAINBOW = ["#ff4b4b", "#ff9f43", "#ffd23f", "#3ddc97", "#2ad4ff", "#4f6bff", "#a98bff"]
rng = np.random.default_rng(11)
END_Y = 0.392
MOL = np.c_[rng.uniform(-3.4, 3.4, 26), rng.uniform(-0.6, 2.2, 26)]


def wave(dax, x0, x1, y, lam, amp, col, a, phase=0.0, lw=3.5):
    xs = np.linspace(x0, x1, 400)
    dax.plot(xs, y + amp * np.sin(2 * math.pi * (xs - phase) / lam), color=col, lw=lw, alpha=a, zorder=6)


def draw(c):
    dax = c.area(0.0, 0.0, 7.6)
    t = c.t
    sunset = ease(c.phase("sunset", 0.05, 0.5))

    # sky background tint
    sky_blue = ease(c.phase("eyes", 0.3, 0.7))
    if sky_blue > 0 or sunset > 0:
        col = np.array(matplotlib_rgb("#2a6fdb")) * (1 - sunset) + np.array(matplotlib_rgb("#ff7a3d")) * sunset
        dax.add_patch(Rectangle((-4, -1.4), 8, 4.4, facecolor=tuple(col), edgecolor="none",
                                alpha=0.35 * max(sky_blue, sunset), zorder=1))

    # 1) white light → rainbow
    wa = ease(c.phase("white", 0.0, 0.3)) * (1 - ease(c.phase("air", 0.0, 0.25)))
    if wa > 0:
        dax.add_patch(Circle((-3.2, 1.6), 0.55, color=GOLD, alpha=wa, zorder=5))
        dax.plot([-2.6, -0.4], [1.6, 1.6], color=WHITE, lw=10, alpha=wa, zorder=5, solid_capstyle="round")
        sp = ease(c.phase("white", 0.35, 0.8))
        for k, col in enumerate(RAINBOW):
            y1 = 1.6 + (k - 3) * 0.32 * sp
            dax.plot([-0.4, 3.4], [1.6, y1], color=col, lw=6, alpha=wa * max(0.2, sp), zorder=5)
        outline(dax.text(0.3, 0.4, "white = all colours", ha="center", fontsize=28, fontweight="bold",
                         color=WHITE, alpha=wa * sp, zorder=7))

    # 2) molecules + waves of different wavelength
    ma = ease(c.phase("air", 0.15, 0.5)) * (1 - ease(c.phase("sunset", 0.0, 0.2)))
    if ma > 0:
        dax.scatter(MOL[:, 0], MOL[:, 1], s=60, color=LTGREY, alpha=ma * 0.8, zorder=4)
        outline(dax.text(3.4, 2.65, "air molecules", ha="right", fontsize=22, fontweight="bold", color=LTGREY,
                         alpha=ma, zorder=7))
    if c.at("scatter") and not c.at("eyes"):
        sa = ease(c.phase("scatter", 0.0, 0.2))
        hit = c.phase("scatter", 0.25, 0.7)
        # red: long wavelength sails through
        wave(dax, -3.6, 3.6, 1.95, 1.4, 0.22, "#ff4b4b", sa, phase=t * 2.2)
        outline(dax.text(-3.6, 2.45, "red: long λ → passes through", ha="left", fontsize=22, fontweight="bold",
                         color="#ff4b4b", alpha=sa, zorder=7))
        # blue: short wavelength gets scattered by a molecule
        mx, my = 0.4, 0.3
        wave(dax, -3.6, lerp(-3.6, mx, min(1, hit * 2 + 0.3)), my, 0.45, 0.2, "#2ad4ff", sa, phase=t * 2.2)
        dax.add_patch(Circle((mx, my), 0.13, color=WHITE, alpha=sa, zorder=7))
        if hit > 0.3:
            ha = ease((hit - 0.3) / 0.4)
            for k in range(10):
                ang = k * 2 * math.pi / 10 + 0.3
                r = 0.3 + 1.3 * ha
                dax.annotate("", xy=(mx + r * math.cos(ang), my + r * math.sin(ang) * 0.85),
                             xytext=(mx + 0.2 * math.cos(ang), my + 0.2 * math.sin(ang)), zorder=6,
                             arrowprops=dict(arrowstyle="-|>", color="#2ad4ff", lw=3, alpha=ha, mutation_scale=22))
            outline(dax.text(0.4, -1.55, "blue: short λ → scattered everywhere", ha="center", fontsize=22,
                             fontweight="bold", color="#2ad4ff", alpha=ha, zorder=7))
        la = ease(c.phase("scatter", 0.65, 0.9))
        if la > 0:
            c.pill(0.5, 0.385, 0.48, 0.058, GOLD, alpha=la, dark="#2a2000")
            c.text(0.5, 0.385, r"scattering $\propto \dfrac{1}{\lambda^{4}}$", size=36, color=GOLD, alpha=la)

    # 3) observer, blue from every direction
    ground_a = ease(c.phase("eyes", 0.0, 0.3))
    if ground_a > 0:
        dax.add_patch(Rectangle((-4, -2.9), 8, 1.5, facecolor="#1b3a2a", edgecolor="none", alpha=ground_a, zorder=3))
        ox, oy = 0.0, -1.15
        dax.add_patch(Circle((ox, oy + 0.32), 0.17, color=WHITE, alpha=ground_a, zorder=8))
        dax.plot([ox, ox], [oy + 0.15, oy - 0.3], color=WHITE, lw=5, alpha=ground_a, zorder=8)
        if not c.at("sunset"):
            ea = ease(c.phase("eyes", 0.2, 0.6))
            for k in range(9):
                ang = math.radians(25 + k * 16.25)
                sx, sy = ox + 3.2 * math.cos(ang), oy + 3.2 * math.sin(ang)
                dax.annotate("", xy=(ox + 0.35 * math.cos(ang), oy + 0.45 + 0.35 * math.sin(ang)),
                             xytext=(sx, sy), zorder=6,
                             arrowprops=dict(arrowstyle="-|>", color="#2ad4ff", lw=3, alpha=ea, mutation_scale=22))
            va = ease(c.phase("eyes", 0.55, 0.8))
            if va > 0:
                c.text(0.5, 0.385, "violet: scatters more, but our eyes favour blue", size=28, color=PURPLE, alpha=va,
                       max_w=0.92)
    # 4) sunset: low sun, long path
    if sunset > 0:
        sx, sy = -3.4, -1.25
        dax.add_patch(Circle((sx, sy), 0.5, color="#ff7a3d", alpha=sunset, zorder=4))
        dax.plot([sx + 0.5, -0.2], [sy + 0.05, -0.85], color="#ff9f43", lw=7, alpha=sunset, zorder=5)
        dax.annotate("", xy=(-0.25, -0.85), xytext=(-0.9, -0.92), zorder=6,
                     arrowprops=dict(arrowstyle="-|>", color="#ff9f43", lw=4, alpha=sunset, mutation_scale=26))
        outline(dax.text(-1.9, -0.35, "long path through air", ha="center", fontsize=22, fontweight="bold",
                         color="#ffb37a", alpha=sunset, zorder=7))
        for k in range(6):
            ang = math.radians(60 + k * 15)
            px = -2.2 + k * 0.35
            dax.annotate("", xy=(px + 0.9 * math.cos(ang), -1.05 + 0.9 * math.sin(ang)), xytext=(px, -1.05), zorder=6,
                         arrowprops=dict(arrowstyle="-|>", color="#2ad4ff", lw=2.5, alpha=sunset * 0.8, mutation_scale=18))
        c.steps([("blue scattered away on the long path", 0.45, CYAN),
                 ("reds & oranges reach us → sunset", 0.62, GOLD)], ys=(0.338, 0.280), beat="sunset")


def matplotlib_rgb(h):
    import matplotlib.colors as mc
    return mc.to_rgb(h)
